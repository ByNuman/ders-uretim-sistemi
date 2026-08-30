# -*- coding: utf-8 -*-
#
# Görsel Ders Notu Üretim Sistemi
# Copyright (C) 2026 Numan Gözdaş
#
# Bu program özgür yazılımdır: Özgür Yazılım Vakfı'nın yayımladığı GNU Genel
# Kamu Lisansı'nın 3. sürümü koşulları altında yeniden dağıtabilir ve/veya
# değiştirebilirsiniz.
#
# Bu program yararlı olacağı umuduyla dağıtılmaktadır, ancak HİÇBİR GARANTİ
# VERİLMEZ; SATILABİLİRLİK veya BELİRLİ BİR AMACA UYGUNLUK zımni garantileri
# dahi verilmez. Ayrıntılar için GNU Genel Kamu Lisansı'na bakın.
#
# Lisansın bir kopyasını bu depodaki LICENSE dosyasında bulabilirsiniz;
# ayrıca <https://www.gnu.org/licenses/> adresinden edinebilirsiniz.
#
"""
HARİTA RENKLENDİRME ARACI — Commons raster haritasını dersin rengine çeker
==========================================================================

    python tools/harita_uret.py islam_tarihi_3 --bolum 3 \
           --sinif 2 --donem 2 --sinav final --kuru
    python tools/harita_uret.py islam_tarihi_3 --bolum 3 \
           --sinif 2 --donem 2 --sinav final --sonuc <url|dosya>

NE YAPAR: gerçek bir kartografın çizdiği Commons haritasının TOPRAK RENGİNİ
dersin tonuna çeker. Coğrafyayı model ÜRETMEZ, kaynaktan gelir.

NE YAPMAZ: harita ÇİZDİRMEZ (o yol 2026 Ağustos'ta terk edildi -- görüntü
modeli kıyıyı ezberden benzetiyor, şehri uyduruyor). Türkçe yer adlarını da
YAZDIRMAZ: onlar `Isaret` HTML katmanı olarak binerler, çünkü modeller Türkçe
diyakritikleri bozuyor (Gürgenç -> Gurgenc) ve etiketi yanlış şehre koyabiliyor.

KURAL: bu araç build.py'nin İÇİNDEN ASLA çağrılmaz. Elle, tek seferlik
çalıştırılır; build yalnızca assets/harita/uretilmis/ altındaki HAZIR dosyayı
gömer. Aksi hâlde her derleme para harcar ve farklı harita üretir.

İKİ AŞAMA (fal.ai anahtarı ortamda olmadığı için bilerek ayrık):

  1. HAZIRLIK (--kuru ya da varsayılan): dersi çözer, kaynağı kırpar, prompt'u
     kurar, `<ad>.istek.json` yazar ve kırpılmış kaynağı diske koyar. Model
     çağrısı YAPILMAZ.
  2. KABUL (--sonuc): dışarıda üretilmiş görüntüyü (URL ya da yerel dosya)
     alır, DENETİM KAPISINDAN geçirir, geçerse uretilmis/ altına yazar ve
     üretim künyesini (.json) kaydeder. Geçmezse dosyayı YAZMAZ.

Ortamda FAL_KEY varsa `--calistir` ile 1. ve 2. aşama tek komutta yapılır.
"""

import argparse
import base64
import io
import json
import os
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from cekirdek import donem as donem_mod          # noqa: E402
from cekirdek import renk_uretici                # noqa: E402
from cekirdek.harita_commons import COMMONS, CommonsGorsel   # noqa: E402
import build as B                                # noqa: E402

URETILMIS = ROOT / "assets" / "harita" / "uretilmis"

# Kutu genişlikleri (mm). Yan sütun ölçüsü CLAUDE.md'de ölçülmüş değerdir;
# gereken piksel bundan türer, KAYNAĞIN boyutundan değil -- 1K çıktı bilerek
# kaynaktan küçüktür ve bu bir kusur değildir (bkz. "Çözünürlük" bölümü).
KUTU_MM = {"sag": 82.0, "sol": 82.0, "tam": 186.0}

# 240 dpi, 300 değil. GEREKÇESİ ÖNEMLİ: bu raster yalnızca COĞRAFYAYI ve RENGİ
# taşır -- okunması gereken Türkçe yer adları `Isaret` HTML katmanındadır ve
# baskıda VEKTÖRDÜR, yani görselin çözünürlüğünden bağımsız olarak keskindir.
# Metin taşımayan bir zemin görseli için 240 dpi fotokopide yeterlidir.
#
# DİKKAT: bir haritada KAYNAĞIN KENDİ etiketlerine güveniyorsanız (Delhi'de
# olduğu gibi -- Lahore/Daulatabad okunsun diye imleç koymamıştık) bu eşik
# YETMEZ, o harita için 300'e çıkarın (--dpi).
HEDEF_DPI = 240

# (endpoint, birim fiyat USD, notlar). Fiyatlar 2026-08-30'da fal.ai'den
# okundu; get_pricing ile teyit edin, sabit varsaymayın.
MODELLER = {
    "gpt-image-2":     ("openai/gpt-image-2/edit", 1.00),
    "seedream":        ("bytedance/seedream/v5/pro/edit", 0.0675),
    "nano-banana-pro": ("fal-ai/nano-banana-pro/edit", 0.15),
}
VARSAYILAN_MODEL = "gpt-image-2"      # 2026-08-30 kullanıcı kararı

# Yalnızca gpt-image-2 `quality` alanını kabul eder (auto/low/medium/high).
KALITE_DESTEKLI = {"gpt-image-2"}


# ---------------------------------------------------------------------------
# Dersi çöz: hangi bölümde hangi CommonsGorsel var, hangi renge çekilecek
# ---------------------------------------------------------------------------

def harita_bul(pack, bolum: int):
    """N. bölümdeki raster harita kutusunu (MapBox, taraf) olarak döndürür."""
    for ch in pack.chapters:
        if ch.number != bolum:
            continue
        for pg in ch.pages:
            for kind, data in pg.items:
                if kind != "mapsplit":
                    continue
                mb, _yan, taraf = data
                if isinstance(mb.commons, CommonsGorsel):
                    return mb, taraf
                raise SystemExit(
                    f"[hata] Bölüm {bolum}'in haritası raster değil "
                    f"({type(mb.commons).__name__}). Bu araç yalnızca "
                    f"CommonsGorsel (PNG/JPG) haritaları renklendirir; "
                    f"SVG kaynaklar zaten `renkler=` ile uyarlanıyor.")
        raise SystemExit(f"[hata] Bölüm {bolum}'de harita kutusu yok.")
    raise SystemExit(f"[hata] Derste {bolum}. bölüm yok.")


def kirpilmis_kaynak(g: CommonsGorsel):
    """Kaynağı açar, dersteki `kirp` kutusunu UYGULAR ve görüntüyü döndürür.

    Modele KIRPILMIŞ görüntü gönderilir: koruması gereken piksel azalır ve
    üretilen dosya doğrudan sayfaya girecek olan çerçevedir. Bunun sonucu
    olarak üretilmiş dosyayı kullanan `CommonsGorsel`'de `kirp` BOŞ olmalıdır
    -- yoksa kırpma iki kez uygulanır. Araç sonunda yapıştırılacak kod
    parçasını zaten `kirp`siz basar.
    """
    from PIL import Image
    yol = COMMONS / g.dosya
    if not yol.exists():
        raise SystemExit(f"[hata] Kaynak harita yok: {yol}")
    im = Image.open(yol).convert("RGB")
    if g.kirp:
        im = im.crop(tuple(int(v) for v in g.kirp))
    return im


def prompt_kur(hex_renk: str) -> str:
    """Modele verilecek talimat.

    Üç şeyi ISRARLA söyler, çünkü Ağustos'ta kaybedilenler tam olarak bunlardı:
    kaynağın kendi etiketleri, KESİKLİ sınırların kesikliği ve arazi gölgesi.
    Ayrıca hiçbir yazı EKLENMEMESİ istenir -- Türkçe adlar HTML katmanında.
    """
    return (
        f"Recolor ONLY the highlighted territory/state area of this historical "
        f"map to the solid color {hex_renk}, preserving its internal shading and "
        f"terrain relief so the landscape texture stays visible.\n"
        f"Keep absolutely everything else identical to the input: coastlines, "
        f"rivers, lakes, neighbouring landmasses, sea color, terrain shading, "
        f"and every existing text label exactly as it appears.\n"
        f"CRITICAL: any border drawn as a DASHED line must remain DASHED — it "
        f"marks an uncertain frontier and must not become a solid line.\n"
        f"Do NOT add, remove, translate or move any text, label, legend, "
        f"caption, marker or symbol. Do not crop, rotate or restyle the map. "
        f"Output the same framing and aspect ratio as the input."
    )


# ---------------------------------------------------------------------------
# DENETİM KAPISI
# ---------------------------------------------------------------------------

def _toprak_maskesi(im, hue_araligi=None, hedef_hex=None):
    """Toprak örtüsü maskesini bit dizisi olarak döndürür.

    Kaynakta toprak, dersin `renk_ton` aralığındaki hue'dur; çıktıda ise hedef
    rengin hue'su. İkisini aynı ölçütle (doygunluk eşiği + hue penceresi)
    çıkarınca örtüşme (IoU) karşılaştırılabilir olur.
    """
    import colorsys
    if hedef_hex:
        h0 = colorsys.rgb_to_hls(*[int(hedef_hex[i:i + 2], 16) / 255
                                   for i in (1, 3, 5)])[0] * 360
        # Pencere DAR olmalı (+-10). ÖLÇÜLDÜ (Memlük, 2026-08-30): +-25 ile
        # denizin tonu (190 derece) hedef lacivertin (205 derece) penceresine
        # giriyor, maske denizi de topraktan sayıyor ve IoU %96,7 yerine
        # %64,4 çıkıyordu -- yani ölçüt, sağlam bir çıktıyı haksız yere
        # reddediyordu. Deniz ile toprak arasında 15 derece var; +-10 ayırıyor.
        alt, ust = h0 - 10, h0 + 10
    else:
        alt, ust = hue_araligi
    px = im.load()
    g, y = im.size
    mask = bytearray(g * y)
    for j in range(y):
        for i in range(g):
            r, gg, b = px[i, j]
            h, l, s = colorsys.rgb_to_hls(r / 255, gg / 255, b / 255)
            if s >= 0.12 and alt <= h * 360 <= ust:
                mask[j * g + i] = 1
    return mask, g, y


def denetle(kaynak_im, cikti_im, taraf: str, hue_araligi, hedef_hex: str,
            dpi: int = HEDEF_DPI) -> dict:
    """Dört ölçütü uygular. Üçü sayısal, dördüncüsü ZORUNLU insan adımı."""
    rapor = {}
    gereken_px = round(KUTU_MM[taraf] / 25.4 * dpi)
    rapor["gereken_px"] = gereken_px
    rapor["cikti_px"] = cikti_im.width
    rapor["cozunurluk_ok"] = cikti_im.width >= gereken_px

    k_oran = kaynak_im.width / kaynak_im.height
    c_oran = cikti_im.width / cikti_im.height
    rapor["kaynak_oran"] = round(k_oran, 4)
    rapor["cikti_oran"] = round(c_oran, 4)
    rapor["oran_sapma_yuzde"] = round(abs(c_oran - k_oran) / k_oran * 100, 2)
    rapor["oran_ok"] = rapor["oran_sapma_yuzde"] <= 1.0

    # IoU: iki maskeyi aynı ölçüye getirip karşılaştır.
    olcu = (400, max(1, round(400 / k_oran)))
    km, g, y = _toprak_maskesi(kaynak_im.resize(olcu), hue_araligi=hue_araligi)
    cm, _, _ = _toprak_maskesi(cikti_im.resize(olcu), hedef_hex=hedef_hex)
    kesisim = sum(1 for i in range(g * y) if km[i] and cm[i])
    birlesim = sum(1 for i in range(g * y) if km[i] or cm[i])
    rapor["iou_yuzde"] = round(kesisim / birlesim * 100, 1) if birlesim else 0.0
    rapor["iou_ok"] = rapor["iou_yuzde"] >= 95.0

    rapor["sayisal_gecti"] = all(
        (rapor["cozunurluk_ok"], rapor["oran_ok"], rapor["iou_ok"]))
    return rapor


def karsilastirma_yaz(kaynak_im, cikti_im, yol: Path) -> None:
    """Yan yana karşılaştırma PNG'si — silinen etiket ve düzleşen kesikli
    sınır SADECE böyle yakalanır, hiçbir sayısal ölçüt görmez."""
    from PIL import Image
    h = 900
    a = kaynak_im.resize((round(kaynak_im.width * h / kaynak_im.height), h))
    b = cikti_im.resize((round(cikti_im.width * h / cikti_im.height), h))
    tuval = Image.new("RGB", (a.width + b.width + 12, h), (255, 255, 255))
    tuval.paste(a, (0, 0))
    tuval.paste(b, (a.width + 12, 0))
    tuval.save(yol)


# ---------------------------------------------------------------------------
# Komutlar
# ---------------------------------------------------------------------------

def _cikti_adi(g: CommonsGorsel) -> str:
    return Path(g.dosya).stem + "-tr.png"


def komut_hazirla(slug, pack, bolum, model, cozunurluk, kalite, olcu, dpi, kuru) -> dict:
    mb, taraf = harita_bul(pack, bolum)
    g = mb.commons
    hex_renk = renk_uretici.pack_rengi(pack)
    im = kirpilmis_kaynak(g)
    gereken_px = round(KUTU_MM[taraf] / 25.4 * dpi)

    URETILMIS.mkdir(parents=True, exist_ok=True)
    ad = _cikti_adi(g)
    # Girdi JPEG yazılır: yükleme kanalının 1 MB sınırı var ve kırpılmış PNG
    # bunu aşıyor (1080x1420 -> 1,25 MB). Kayıp ihmal edilebilir -- raster
    # kaynaklarımızın kendisi zaten JPEG/terrain render'ı; q95'te harita
    # etiketleri bozulmuyor. Bu dosya yalnızca modele giden ara üründür,
    # sayfaya giren şey modelin ÇIKTISIDIR.
    girdi_yol = URETILMIS / (Path(ad).stem + ".girdi.jpg")
    im.save(girdi_yol, format="JPEG", quality=95, optimize=True)

    endpoint, fiyat = MODELLER[model]
    istek = {
        "ders": slug, "bolum": bolum, "bolge": mb.region,
        "kaynak_dosya": g.dosya, "kirp": list(g.kirp) if g.kirp else [],
        "kirp_uygulandi": bool(g.kirp),
        "taraf": taraf, "kutu_mm": KUTU_MM[taraf], "gereken_px": gereken_px,
        "tema_rengi": hex_renk, "renk_ton": list(g.renk_ton) if g.renk_ton else [],
        "model": endpoint, "cozunurluk": cozunurluk,
        "kalite": kalite if model in KALITE_DESTEKLI else None,
        "olcu": olcu,
        "prompt": prompt_kur(hex_renk),
        "girdi_gorsel": str(girdi_yol.relative_to(ROOT)),
        "tarih": date.today().isoformat(),
    }
    (URETILMIS / (Path(ad).stem + ".istek.json")).write_text(
        json.dumps(istek, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[hazırlık] {slug} · Bölüm {bolum} · {mb.region}")
    print(f"  kaynak      : {g.dosya}  ({Path(g.dosya).stat if False else ''}"
          f"{im.width}x{im.height} px, kırpma {'uygulandı' if g.kirp else 'yok'})")
    print(f"  tema rengi  : {hex_renk}")
    print(f"  yerleşim    : taraf={taraf} · kutu {KUTU_MM[taraf]:.0f} mm · "
          f"gereken ≥ {gereken_px} px ({dpi} dpi)")
    kalite_s = f" · kalite={kalite}" if model in KALITE_DESTEKLI else ""
    print(f"  model       : {endpoint} · ölçü {olcu}{kalite_s} · "
          f"~${fiyat:.4f}/görüntü")
    if model == "gpt-image-2":
        print("  [MALİYET] gpt-image-2 birim fiyatı $1,00 -- seedream'in "
              "(~$0,07) yaklaşık 15 katı. Bütçe sıkışıksa --model seedream.")
    print(f"  girdi yazıldı: {girdi_yol.relative_to(ROOT)}")
    if cozunurluk == "4K":
        print("  [UYARI] 4K istendi. build.py görseli zaten 1400 px'e küçültüyor; "
              "bu pikseller çöpe gider (bkz. CLAUDE.md 'Çözünürlük').")
    # Uzun kenar `olcu` ise, DİKEY bir haritada genişlik olcu*oran'a düşer.
    # Kapıdan geçip geçmeyeceğini ÜRETİMDEN ÖNCE söyle -- sonradan öğrenmek
    # boşa harcanmış bir çağrıdır.
    oran = im.width / im.height
    beklenen = olcu if oran >= 1 else round(olcu * oran)
    print(f"  beklenen    : ~{beklenen} px genişlik (oran {oran:.2f}) -> "
          f"{'kapıdan GEÇER' if beklenen >= gereken_px else 'kapıda KALIR'}")
    if beklenen < gereken_px:
        gerekli_olcu = round(gereken_px / (oran if oran < 1 else 1))
        print(f"  [UYARI] {olcu} px bu haritada yetmiyor. Ya ölçüyü "
              f"{gerekli_olcu}+ yapın, ya da kaynağın kendi etiketlerine "
              f"güvenmiyorsanız --dpi ile eşiği düşürün (Türkçe imleçler "
              f"zaten vektör, görselden bağımsız keskin).")
    print("\n--- PROMPT ---\n" + istek["prompt"] + "\n--------------")
    if kuru:
        print("\n[kuru] Model çağrılmadı. Üretilen görüntüyü şununla kabul edin:")
        print(f"  python tools/harita_uret.py {slug} --bolum {bolum} "
              f"--sinif ... --sonuc <url|dosya>")
    return istek


def komut_kabul(slug, pack, bolum, sonuc: str, zorla: bool) -> None:
    from PIL import Image
    mb, taraf = harita_bul(pack, bolum)
    g = mb.commons
    ad = _cikti_adi(g)
    istek_yol = URETILMIS / (Path(ad).stem + ".istek.json")
    if not istek_yol.exists():
        raise SystemExit(f"[hata] Önce hazırlık adımını çalıştırın "
                         f"(istek künyesi yok: {istek_yol.name})")
    istek = json.loads(istek_yol.read_text(encoding="utf-8"))

    if sonuc.startswith(("http://", "https://")):
        with urllib.request.urlopen(sonuc) as r:
            veri = r.read()
    else:
        veri = Path(sonuc).read_bytes()
    cikti_im = Image.open(io.BytesIO(veri)).convert("RGB")
    kaynak_im = kirpilmis_kaynak(g)

    hue = tuple(istek["renk_ton"]) if istek["renk_ton"] else (0, 360)
    rapor = denetle(kaynak_im, cikti_im, taraf, hue, istek["tema_rengi"])

    kars_yol = URETILMIS / (Path(ad).stem + ".karsilastirma.png")
    karsilastirma_yaz(kaynak_im, cikti_im, kars_yol)

    print(f"[denetim] {slug} · Bölüm {bolum}")
    print(f"  çözünürlük : {rapor['cikti_px']} px  (gereken ≥ "
          f"{rapor['gereken_px']})  {'✓' if rapor['cozunurluk_ok'] else '✗'}")
    print(f"  en-boy     : {rapor['cikti_oran']} vs kaynak "
          f"{rapor['kaynak_oran']}  (sapma %{rapor['oran_sapma_yuzde']})  "
          f"{'✓' if rapor['oran_ok'] else '✗'}")
    print(f"  toprak IoU : %{rapor['iou_yuzde']}  (gereken ≥ %95)  "
          f"{'✓' if rapor['iou_ok'] else '✗'}")
    print(f"  karşılaştırma görseli: {kars_yol.relative_to(ROOT)}")
    print("  [ZORUNLU] Bu görseli GÖZLE okuyun: silinen yer adı ve düz çizgiye "
          "dönmüş kesikli sınır hiçbir sayısal ölçütte görünmez.")

    if not rapor["sayisal_gecti"] and not zorla:
        raise SystemExit("\n[RET] Sayısal denetim başarısız -- dosya YAZILMADI. "
                         "Yeniden üretin ya da bilinçli bir istisna için --zorla verin.")

    hedef = URETILMIS / ad
    cikti_im.save(hedef)
    kunye = dict(istek)
    kunye.update({"cikti_dosya": ad, "cikti_px": [cikti_im.width, cikti_im.height],
                  "denetim": rapor, "zorlandi": bool(zorla),
                  "kabul_tarihi": date.today().isoformat()})
    (URETILMIS / (Path(ad).stem + ".json")).write_text(
        json.dumps(kunye, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n[KABUL] {hedef.relative_to(ROOT)}  ({cikti_im.width}x{cikti_im.height})")
    print(f"[künye] {(URETILMIS / (Path(ad).stem + '.json')).relative_to(ROOT)}")
    print("\nDerse yapıştırın (DİKKAT: `kirp` YOK -- kırpma üretimde uygulandı):\n")
    print(f'                commons=CommonsGorsel(')
    print(f'                    dosya="uretilmis/{ad}",')
    print(f'                    atif={g.atif!r},')
    if g.lejant_elle:
        print(f'                    lejant_elle={{"{istek["tema_rengi"]}": '
              f'"{list(g.lejant_elle.values())[0]}"}},')
    if g.isaretler:
        print(f'                    isaretler=[...],   # değişmez, aynen kalır')
    print(f'                ),')


def main() -> None:
    ap = argparse.ArgumentParser(prog="tools/harita_uret.py")
    ap.add_argument("dersler", nargs=1, help="ders modülü (çıplak ad)")
    ap.add_argument("--bolum", type=int, required=True, help="bölüm numarası")
    ap.add_argument("--model", default=VARSAYILAN_MODEL, choices=sorted(MODELLER))
    ap.add_argument("--cozunurluk", default="1K", choices=["1K", "2K", "4K"],
                    help="nano-banana/seedream için; gpt-image-2 --olcu kullanır")
    ap.add_argument("--olcu", type=int, default=1024,
                    help="uzun kenar piksel (varsayılan 1024)")
    ap.add_argument("--kalite", default="low",
                    choices=["auto", "low", "medium", "high"],
                    help="yalnızca gpt-image-2 (varsayılan low)")
    ap.add_argument("--dpi", type=int, default=HEDEF_DPI,
                    help=f"denetim eşiği (varsayılan {HEDEF_DPI})")
    ap.add_argument("--kuru", action="store_true",
                    help="yalnızca prompt/maliyet bas, çağrı yapma")
    ap.add_argument("--sonuc", help="üretilmiş görüntü (URL ya da yerel dosya)")
    ap.add_argument("--zorla", action="store_true",
                    help="sayısal denetim başarısız olsa da kabul et")
    donem_mod.add_args(ap)
    a = ap.parse_args()

    d = donem_mod.resolve(a)
    B.set_donem(d)
    slug = a.dersler[0]
    pack = d.import_ders(slug).get_pack()

    if a.sonuc:
        komut_kabul(slug, pack, a.bolum, a.sonuc, a.zorla)
    else:
        komut_hazirla(slug, pack, a.bolum, a.model, a.cozunurluk,
                      a.kalite, a.olcu, a.dpi, kuru=True)


if __name__ == "__main__":
    main()
