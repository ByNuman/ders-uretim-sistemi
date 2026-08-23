# -*- coding: utf-8 -*-
"""
DERS ÜRETİM SİSTEMİ — pdfx.py  (BASKI ÖNCESİ / PREPRESS)
=========================================================
İki iş yapar:

  1. set_print_boxes()  -> PDF'in sayfa kutularını baskıya uygun kurar.
     Chromium'un ürettiği sayfa, trim + her kenardan 3mm bleed kadar
     BÜYÜK render edilir. Matbaanın "nerede keseceğim?" sorusunu ancak
     TrimBox cevaplar; bu fonksiyon CropBox/BleedBox = render kutusu,
     TrimBox = 3mm içerideki bitmiş sayfa olacak şekilde yazar.
     (PDF/X, her sayfada TrimBox veya ArtBox bulunmasını ZORUNLU kılar.)

  2. to_pdfx4_cmyk()    -> Ghostscript ile RGB -> PDF/X-4 (DeviceCMYK).
     build.py bunu PDF üretiminin hemen ardından otomatik çağırır; RGB
     ara dosya geçici klasöre alınır ve silinir, kullanıcının elinde
     doğrudan CMYK dosya kalır.

Ghostscript kurulu değilse GhostscriptMissing fırlatılır; mesajı işletim
sistemine göre kurulum komutunu içerir.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

MM = 72.0 / 25.4          # 1mm kaç PostScript puntosu

ROOT = Path(__file__).parent

# ICC profili aranırken kullanılacak dosya adı kalıpları (öncelik sırasıyla).
# FOGRA39 / "ISO Coated v2 (ECI)" Avrupa kuşe baskının fiili standardıdır ve
# lisansı gereği Ghostscript ile BİRLİKTE GELMEZ — eci.org'dan indirilip
# assets/icc/ altına konmalıdır.
ICC_SEARCH_DIRS = [ROOT / "assets" / "icc", ROOT / "icc", ROOT]
ICC_PREFERRED = [
    "ISOcoated_v2_eci.icc",
    "ISOcoated_v2_300_eci.icc",
    "CoatedFOGRA39.icc",
    "FOGRA39L.icc",
]

INSTALL_HINT = {
    "darwin": "brew install ghostscript",
    "linux": "sudo apt install ghostscript",
    "win32": "https://ghostscript.com/releases/gsdnld.html adresinden "
             "Windows installer'ını indirip kurun (kurulumdan sonra yeni bir "
             "terminal açın ki gswin64c PATH'e gelsin)",
}


class GhostscriptMissing(RuntimeError):
    """Ghostscript bulunamadı — mesajı kurulum komutunu içerir."""


class GhostscriptFailed(RuntimeError):
    """Ghostscript çalıştı ama hata döndürdü / geçerli çıktı üretmedi."""


# ---------------------------------------------------------------------------
# 1) Sayfa kutuları
# ---------------------------------------------------------------------------

def set_print_boxes(pdf_path: Path, trim_w_mm: float, trim_h_mm: float,
                    bleed_mm: float, quiet: bool = False) -> None:
    """CropBox/BleedBox = render kutusu (trim + 2*bleed), TrimBox = bitmiş
    sayfa. MediaBox'a DOKUNULMAZ, ArtBox silinir.

    Neden MediaBox'a dokunmuyoruz: Chromium sayfayı istenen ölçüden ~0.02-0.12mm
    BÜYÜK üretiyor (kendi cihaz-pikseli yuvarlaması) ve içeriği bu levhanın
    SOL-ÜST köşesine yaslıyor. Bu yüzden kutuları levhanın sol-üst köşesinden
    ölçerek yazıyoruz; sonuç, TrimBox'ın tam olarak istenen mm değerinde ve
    doğru yerde olmasıdır. (MediaBox'ı BleedBox'tan birkaç yüzde mm büyük
    bırakmak baskı iş akışlarında olağandır.)

    PyMuPDF'in set_bleedbox/set_trimbox/set_artbox metodları rect'i MediaBox'ın
    ÜST kenarından aşağı doğru ölçer -- yani burada verdiğimiz koordinatlar
    doğrudan "levhanın sol-üst köşesinden itibaren" demektir."""
    import pymupdf
    doc = pymupdf.open(str(pdf_path))
    w_pt = (trim_w_mm + 2 * bleed_mm) * MM
    h_pt = (trim_h_mm + 2 * bleed_mm) * MM
    b = bleed_mm * MM
    too_small = 0
    for page in doc:
        mb = page.mediabox
        # Levha beklenenden küçükse kutuyu levhaya sığdır (aksi halde PyMuPDF
        # "not in MediaBox" hatası verir) ve sayacı artır.
        pw, ph = min(w_pt, mb.width), min(h_pt, mb.height)
        if pw < w_pt - 0.01 or ph < h_pt - 0.01:
            too_small += 1
        bleed_rect = pymupdf.Rect(0, 0, pw, ph)
        trim_rect = pymupdf.Rect(b, b, pw - b, ph - b)
        page.set_cropbox(bleed_rect)
        page.set_bleedbox(bleed_rect)
        page.set_trimbox(trim_rect)
        # ArtBox BİLEREK yazılmıyor: PDF/X, bir sayfada TrimBox VEYA ArtBox
        # bulunmasını ister -- ikisi birden compliance hatasıdır.
        doc.xref_set_key(page.xref, "ArtBox", "null")
    tmp = pdf_path.with_name(pdf_path.stem + "._boxes.pdf")
    doc.save(str(tmp), garbage=0, deflate=True)
    doc.close()
    os.replace(str(tmp), str(pdf_path))
    if too_small and not quiet:
        print(f"[UYARI] {too_small} sayfanın levhası beklenen "
              f"{trim_w_mm + 2 * bleed_mm:g}x{trim_h_mm + 2 * bleed_mm:g}mm'den küçük -- "
              "kutular levhaya sığdırıldı, trim ölçüsü hedeflenenden ufak olabilir.")
    if not quiet:
        print(f"[prepress] Sayfa kutuları yazıldı: CropBox/BleedBox "
              f"{trim_w_mm + 2 * bleed_mm:g}x{trim_h_mm + 2 * bleed_mm:g}mm · "
              f"TrimBox {trim_w_mm:g}x{trim_h_mm:g}mm ({bleed_mm:g}mm bleed) ✓")


def read_boxes(pdf_path: Path, page_no: int = 0) -> dict:
    """Doğrulama/raporlama için tek bir sayfanın kutularını mm cinsinden okur."""
    import pymupdf
    doc = pymupdf.open(str(pdf_path))
    page = doc[page_no]
    out = {}
    for name in ("mediabox", "bleedbox", "trimbox", "artbox", "cropbox"):
        r = getattr(page, name)
        out[name] = (round(r.width / MM, 2), round(r.height / MM, 2))
    doc.close()
    return out


# ---------------------------------------------------------------------------
# 2) Ghostscript'i bul
# ---------------------------------------------------------------------------

def find_ghostscript() -> str:
    """gs / gswin64c / gswin32c çalıştırılabilirini bulur.

    Sıra: DERS_GS ortam değişkeni -> PATH -> (Windows) tipik kurulum dizinleri
    -> (Windows) kayıt defteri. Bulunamazsa GhostscriptMissing fırlatır."""
    env = os.environ.get("DERS_GS")
    if env and Path(env).exists():
        return env

    for name in ("gs", "gswin64c", "gswin32c"):
        found = shutil.which(name)
        if found:
            return found

    if sys.platform == "win32":
        for base in (r"C:\Program Files\gs", r"C:\Program Files (x86)\gs"):
            root = Path(base)
            if not root.is_dir():
                continue
            # en yüksek sürüm önce
            for ver in sorted(root.iterdir(), reverse=True):
                for exe in ("gswin64c.exe", "gswin32c.exe"):
                    cand = ver / "bin" / exe
                    if cand.exists():
                        return str(cand)
        try:
            import winreg
            for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
                for key in (r"SOFTWARE\GPL Ghostscript", r"SOFTWARE\Artifex Ghostscript"):
                    try:
                        with winreg.OpenKey(hive, key) as k:
                            ver = winreg.EnumKey(k, 0)
                            with winreg.OpenKey(k, ver) as vk:
                                dll = winreg.QueryValueEx(vk, "GS_DLL")[0]
                                cand = Path(dll).parent / "gswin64c.exe"
                                if cand.exists():
                                    return str(cand)
                    except OSError:
                        continue
        except ImportError:
            pass

    hint = INSTALL_HINT.get(sys.platform, INSTALL_HINT["linux"])
    raise GhostscriptMissing(
        "Ghostscript bulunamadı — PDF/X-4 CMYK dönüşümü yapılamıyor.\n"
        f"  Kurulum ({sys.platform}):  {hint}\n"
        "  Diğer sistemler:  macOS -> brew install ghostscript · "
        "Ubuntu/Debian -> sudo apt install ghostscript · "
        "Windows -> https://ghostscript.com/releases/gsdnld.html\n"
        "  Kurulu ama PATH'te değilse tam yolu DERS_GS ortam değişkenine yazın, ör.:\n"
        "      set DERS_GS=C:\\Program Files\\gs\\gs10.03.1\\bin\\gswin64c.exe"
    )


def ghostscript_version(gs: str) -> tuple[int, int]:
    try:
        out = subprocess.run([gs, "--version"], capture_output=True, text=True,
                             timeout=30).stdout.strip()
        m = re.match(r"(\d+)\.(\d+)", out)
        if m:
            return int(m.group(1)), int(m.group(2))
    except Exception:
        pass
    return (0, 0)


# ---------------------------------------------------------------------------
# 3) ICC çıktı profili
# ---------------------------------------------------------------------------

def find_icc_profile(gs: str) -> tuple[Path, str, bool]:
    """(profil yolu, insan-okunur ad, fogra39_mu) döner.

    Arama sırası:
      1. DERS_ICC ortam değişkeni
      2. assets/icc/ (ve icc/, repo kökü) altındaki bilinen FOGRA39 dosya adları
      3. aynı klasörlerdeki HERHANGİ bir .icc
      4. Ghostscript'in kendi iccprofiles/default_cmyk.icc dosyası (SON ÇARE)

    4. seçenek PDF/X açısından geçerli bir çıktı profilidir ama FOGRA39
    DEĞİLDİR; matbaanız FOGRA39 istiyorsa uyarı verilir."""
    env = os.environ.get("DERS_ICC")
    if env and Path(env).exists():
        return Path(env), Path(env).stem, True

    for d in ICC_SEARCH_DIRS:
        for name in ICC_PREFERRED:
            cand = d / name
            if cand.exists():
                return cand, cand.stem, True
    for d in ICC_SEARCH_DIRS:
        if d.is_dir():
            for cand in sorted(d.glob("*.icc")):
                return cand, cand.stem, True

    # Ghostscript kurulumuyla gelen yedek CMYK profili
    gs_root = Path(gs).resolve().parent.parent
    for cand in (gs_root / "iccprofiles" / "default_cmyk.icc",
                 gs_root / "share" / "ghostscript"):
        if cand.is_file():
            return cand, "Ghostscript default_cmyk", False
        if cand.is_dir():
            hits = sorted(cand.glob("*/iccprofiles/default_cmyk.icc"))
            if hits:
                return hits[0], "Ghostscript default_cmyk", False

    raise GhostscriptFailed(
        "CMYK ICC çıktı profili bulunamadı. FOGRA39 profilini eci.org'dan "
        "(\"ISO Coated v2 (ECI)\") indirip assets/icc/ISOcoated_v2_eci.icc "
        "olarak kaydedin ya da yolunu DERS_ICC ortam değişkenine yazın."
    )


def _ps_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace("(", r"\(").replace(")", r"\)")


def write_pdfx_def(path: Path, icc: Path, title: str, condition: str,
                   condition_id: str) -> None:
    """PDF/X-4 tanım dosyasını (PDFX_def.ps) üretir.

    Ghostscript kurulumuyla gelen lib/PDFX_def.ps'i ELLE düzenlemek yerine
    kendi kopyamızı üretiyoruz: sistem dosyasına dokunmadan ICC profilini,
    çıktı koşulunu ve başlığı her build'de doğru değerlerle yazabiliyoruz."""
    icc_ps = _ps_escape(str(icc.resolve()).replace("\\", "/"))
    ps = f"""%!
%% PDF/X-4 tanım dosyası — pdfx.py tarafından üretildi, elle düzenlemeyin.
%% Çıktı profili: {icc.name}

systemdict /ProcessColorModel known {{
  systemdict /ProcessColorModel get dup /DeviceGray ne
  exch /DeviceCMYK ne and
}} {{ true }} ifelse
{{
  (ProcessColorModel /DeviceCMYK ya da /DeviceGray olmalı.) ==
  flush Quit
}} if

/ICCProfile ({icc_ps}) def

[ /GTS_PDFXVersion (PDF/X-4)
  /Title ({_ps_escape(title)})
  /Trapped /False
  /DOCINFO pdfmark

[/_objdef {{icc_PDFX}} /type /stream /OBJ pdfmark
[{{icc_PDFX}} <<
  /N systemdict /ProcessColorModel get /DeviceGray eq {{1}} {{4}} ifelse
>> /PUT pdfmark
[{{icc_PDFX}} ICCProfile (r) file /PUT pdfmark

[/_objdef {{OutputIntent_PDFX}} /type /dict /OBJ pdfmark
[{{OutputIntent_PDFX}} <<
  /Type /OutputIntent
  /S /GTS_PDFX
  /OutputCondition ({_ps_escape(condition)})
  /OutputConditionIdentifier ({_ps_escape(condition_id)})
  /RegistryName (http://www.color.org)
  /Info ({_ps_escape(condition)})
  /DestOutputProfile {{icc_PDFX}}
>> /PUT pdfmark
[{{Catalog}} <</OutputIntents [ {{OutputIntent_PDFX}} ]>> /PUT pdfmark
"""
    path.write_text(ps, encoding="utf-8")


def write_pdfx_xmp(pdf_path: Path, title: str, version: str = "PDF/X-4") -> None:
    """PDF/X kimliğini XMP paketi olarak dosyaya yazar.

    NEDEN GEREKLİ: ISO 15930-7 (PDF/X-4) dosyayı XMP'deki
    pdfxid:GTS_PDFXVersion ile tanımlar. Ghostscript bunu yalnızca -dPDFX
    kipinde yazıyor, o kip de bizi PDF/X-3'e (PDF 1.3, düzleştirilmiş
    saydamlık, ~6 kat dosya) düşürüyor -- bkz. to_pdfx4_cmyk. Bu yüzden
    dönüşümden sonra XMP'yi burada kendimiz kuruyoruz; değer, DocInfo'daki
    GTS_PDFXVersion ile birebir aynıdır.

    NEDEN pypdf: PyMuPDF'in set_xml_metadata() + save() yolu bu ardışık
    düzende (Ghostscript çıktısı, aynı süreç içinde) metadata nesnesini
    sessizce düşürüyordu -- bellekte görünüyor, diske yazılmıyordu.
    pypdf'in clone_from'u sayfaları, yer imlerini, OutputIntent'i ve
    TrimBox'ı bozmadan taşıyor."""
    import uuid
    import datetime
    from pypdf import PdfReader, PdfWriter

    now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")

    def esc(t: str) -> str:
        return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    xmp = f"""<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="" xmlns:pdfxid="http://www.npes.org/pdfx/ns/id/">
   <pdfxid:GTS_PDFXVersion>{version}</pdfxid:GTS_PDFXVersion>
  </rdf:Description>
  <rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/">
   <dc:title><rdf:Alt><rdf:li xml:lang="x-default">{esc(title)}</rdf:li></rdf:Alt></dc:title>
   <dc:format>application/pdf</dc:format>
  </rdf:Description>
  <rdf:Description rdf:about="" xmlns:xmp="http://ns.adobe.com/xap/1.0/">
   <xmp:CreateDate>{now}</xmp:CreateDate>
   <xmp:ModifyDate>{now}</xmp:ModifyDate>
   <xmp:MetadataDate>{now}</xmp:MetadataDate>
  </rdf:Description>
  <rdf:Description rdf:about="" xmlns:pdf="http://ns.adobe.com/pdf/1.3/">
   <pdf:Trapped>False</pdf:Trapped>
  </rdf:Description>
  <rdf:Description rdf:about="" xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/">
   <xmpMM:DocumentID>uuid:{uuid.uuid4()}</xmpMM:DocumentID>
   <xmpMM:InstanceID>uuid:{uuid.uuid4()}</xmpMM:InstanceID>
   <xmpMM:VersionID>1</xmpMM:VersionID>
   <xmpMM:RenditionClass>default</xmpMM:RenditionClass>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>"""

    reader = PdfReader(str(pdf_path))
    writer = PdfWriter(clone_from=reader)
    # pypdf varsayılan olarak %PDF-1.3 başlığı yazar; Ghostscript'in ürettiği
    # sürümü (PDF/X-4 için 1.6) koruyoruz.
    writer.pdf_header = reader.pdf_header
    writer.xmp_metadata = xmp.encode("utf-8")
    tmp = pdf_path.with_name(pdf_path.stem + "._xmp.pdf")
    with open(tmp, "wb") as fh:
        writer.write(fh)
    os.replace(str(tmp), str(pdf_path))

    # Sessiz kayıp olmasın: PDF/X kimliği dosyada gerçekten duruyor mu?
    import pymupdf
    check = pymupdf.open(str(pdf_path))
    written = check.get_xml_metadata()
    check.close()
    if version not in written:
        print(f"[UYARI] XMP PDF/X kimliği yazılamadı ({len(written)} bayt okundu) — "
              "dosya CMYK ama PDF/X-4 olarak tanınmayabilir.")


# ---------------------------------------------------------------------------
# 4) Dönüşüm
# ---------------------------------------------------------------------------

def to_pdfx4_cmyk(pdf_path: Path, title: str = "", trim_w_mm: float | None = None,
                  trim_h_mm: float | None = None, bleed_mm: float = 0.0,
                  keep_rgb: Path | None = None) -> dict:
    """pdf_path'i YERİNDE PDF/X-4 (DeviceCMYK) sürümüyle değiştirir.

    RGB orijinal geçici klasöre alınır; keep_rgb verilirse oraya kopyalanır,
    verilmezse işlem bitince silinir. Sayfa sayısı korunmuyorsa değişiklik
    geri alınır ve GhostscriptFailed fırlatılır — eksik bir baskı dosyası
    teslim etmektense RGB dosyayı bırakmak yeğdir.

    Döner: {'gs', 'gs_version', 'icc', 'icc_name', 'is_fogra39', 'pages',
            'size_before', 'size_after', 'rgb_objects'}"""
    from pypdf import PdfReader

    gs = find_ghostscript()
    ver = ghostscript_version(gs)
    icc, icc_name, is_fogra = find_icc_profile(gs)

    pages_before = len(PdfReader(str(pdf_path)).pages)
    size_before = pdf_path.stat().st_size

    tmpdir = Path(tempfile.mkdtemp(prefix="ders_pdfx_"))
    try:
        rgb_src = tmpdir / "rgb.pdf"
        shutil.copy2(pdf_path, rgb_src)
        defs = tmpdir / "PDFX_def.ps"
        write_pdfx_def(defs, icc,
                       title=title or pdf_path.stem,
                       condition=icc_name,
                       condition_id="FOGRA39" if is_fogra else icc_name)
        out = tmpdir / "cmyk.pdf"

        cmd = [gs]
        # -dPDFX BİLEREK KULLANILMIYOR: Ghostscript'te bu bayrak PDF/X-3
        # kipidir -- CompatibilityLevel'ı zorla 1.3'e çeker, saydamlığı
        # düzleştirir. Ölçüldü: aynı ders 23.7 MB / ~5 dk (PDF 1.3) yerine
        # 3.9 MB / 22 sn (PDF 1.6) çıkıyor ve kapak gradyanları bozulmuyor.
        # PDF/X-4 kimliği zaten PDFX_def.ps'teki GTS_PDFXVersion + OutputIntent
        # ve dönüşüm sonrası yazılan XMP ile veriliyor.
        cmd += [
            "-dCompatibilityLevel=1.6",
            "-dBATCH", "-dNOPAUSE", "-dNOOUTERSAVE", "-dQUIET",
            "-sDEVICE=pdfwrite",
            "-sColorConversionStrategy=CMYK",
            "-sProcessColorModel=DeviceCMYK",
            "-dOverrideICC=false",
            "-dPreserveOverprintSettings=true",
            "-dTransferFunctionInfo=/Apply",
            "-dUCRandBGInfo=/Preserve",
            "-dEmbedAllFonts=true", "-dSubsetFonts=true",
            "-dAutoRotatePages=/None",
            # Görsellere dokunma: Chromium'un gömdüğü gradyan/doku rasterleri
            # zaten sınırlı çözünürlükte, gs'in varsayılanı bunları 22 dpi'a
            # kadar düşürüyordu.
            "-dDownsampleColorImages=false",
            "-dDownsampleGrayImages=false",
            "-dDownsampleMonoImages=false",
            "-dAutoFilterColorImages=false", "-dColorImageFilter=/FlateEncode",
            "-dAutoFilterGrayImages=false", "-dGrayImageFilter=/FlateEncode",
            f"-sOutputFile={out}",
        ]
        # gs 9.50+ SAFER varsayılan; ICC ve tanım dosyasını okuyabilmesi için izin
        if ver >= (9, 50):
            for path in (icc.resolve().parent, tmpdir):
                cmd.insert(1, f"--permit-file-read={path.as_posix()}/")
        cmd += [str(defs), str(rgb_src)]

        res = subprocess.run(cmd, capture_output=True, text=True,
                             encoding="utf-8", errors="replace")
        if res.returncode != 0 or not out.exists():
            raise GhostscriptFailed(
                "Ghostscript PDF/X-4 dönüşümü başarısız oldu "
                f"(çıkış kodu {res.returncode}).\n"
                f"  Komut: {' '.join(cmd)}\n"
                f"  stdout: {res.stdout[-2000:]}\n"
                f"  stderr: {res.stderr[-2000:]}"
            )

        pages_after = len(PdfReader(str(out)).pages)
        if pages_after != pages_before:
            raise GhostscriptFailed(
                f"CMYK çıktı {pages_after} sayfa, orijinali {pages_before} sayfaydı "
                "— dönüşüm iptal edildi, RGB dosya olduğu gibi bırakıldı.")

        if keep_rgb:
            shutil.copy2(rgb_src, keep_rgb)
        shutil.copy2(out, pdf_path)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    # Ghostscript pdfwrite TrimBox'ı her zaman taşımaz — PDF/X için zorunlu,
    # eksikse yeniden yazıyoruz.
    if trim_w_mm and bleed_mm:
        boxes = read_boxes(pdf_path)
        want = (round(trim_w_mm, 2), round(trim_h_mm, 2))
        if boxes["trimbox"] != want:
            set_print_boxes(pdf_path, trim_w_mm, trim_h_mm, bleed_mm, quiet=True)
            print("[prepress] Ghostscript TrimBox'ı düşürdü — yeniden yazıldı.")

    write_pdfx_xmp(pdf_path, title or pdf_path.stem)

    return {
        "gs": gs,
        "gs_version": ".".join(str(x) for x in ver),
        "icc": icc,
        "icc_name": icc_name,
        "is_fogra39": is_fogra,
        "pages": pages_before,
        "size_before": size_before,
        "size_after": pdf_path.stat().st_size,
        "rgb_objects": count_rgb_objects(pdf_path),
    }


def count_rgb_objects(pdf_path: Path) -> int:
    """Çıktıda kalan DeviceRGB/RGB görsel referanslarını sayar — dönüşümün
    gerçekten CMYK ürettiğini doğrulamanın hızlı yolu."""
    import pymupdf
    doc = pymupdf.open(str(pdf_path))
    n = 0
    for page in doc:
        for img in page.get_images(full=True):
            xref = img[0]
            try:
                cs = doc.xref_get_key(xref, "ColorSpace")[1] or ""
            except Exception:
                cs = ""
            if "RGB" in cs:
                n += 1
    doc.close()
    return n


def convert_or_warn(pdf_path: Path, title: str, trim_w_mm: float, trim_h_mm: float,
                    bleed_mm: float) -> bool:
    """build.py'nin çağırdığı sarmalayıcı: dönüşümü dener, Ghostscript yoksa
    build'i DÜŞÜRMEDEN net bir kurulum uyarısı basar (RGB PDF elde kalır)."""
    try:
        info = to_pdfx4_cmyk(pdf_path, title=title, trim_w_mm=trim_w_mm,
                             trim_h_mm=trim_h_mm, bleed_mm=bleed_mm)
    except GhostscriptMissing as e:
        print("\n[PDF/X-4 ATLANDI] " + str(e))
        print("  -> Çıktı RGB olarak bırakıldı; matbaaya göndermeden önce "
              "Ghostscript kurup build'i tekrar çalıştırın.\n")
        return False
    except GhostscriptFailed as e:
        print("\n[PDF/X-4 HATASI] " + str(e))
        print("  -> Çıktı RGB olarak bırakıldı.\n")
        return False

    print(f"[prepress] PDF/X-4 CMYK dönüşümü tamam (Ghostscript "
          f"{info['gs_version']}, profil: {info['icc_name']})")
    print(f"[prepress] Boyut: {info['size_before'] / 1024 / 1024:.1f} MB -> "
          f"{info['size_after'] / 1024 / 1024:.1f} MB · {info['pages']} sayfa korundu ✓")
    if info["rgb_objects"]:
        print(f"[UYARI] Çıktıda hâlâ {info['rgb_objects']} RGB görsel nesnesi var.")
    if not info["is_fogra39"]:
        print("[UYARI] FOGRA39 profili bulunamadı, Ghostscript'in genel CMYK "
              "profili kullanıldı. Matbaanız FOGRA39 istiyorsa "
              "\"ISO Coated v2 (ECI)\" profilini eci.org'dan indirip "
              "assets/icc/ISOcoated_v2_eci.icc olarak kaydedin.")
    return True


if __name__ == "__main__":
    # Teşhis: ortamda Ghostscript ve ICC profili var mı?
    try:
        gs = find_ghostscript()
        print(f"Ghostscript: {gs}  (sürüm {'.'.join(map(str, ghostscript_version(gs)))})")
        icc, name, fogra = find_icc_profile(gs)
        print(f"ICC profili : {icc}  ({name}, FOGRA39: {fogra})")
    except (GhostscriptMissing, GhostscriptFailed) as e:
        print(e)
