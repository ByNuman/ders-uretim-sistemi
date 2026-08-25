# -*- coding: utf-8 -*-
"""
DERS ÜRETİM SİSTEMİ — build.py
================================
Kullanım:
    python build.py psikoloji --sinif 2 --donem 2 --sinav final

Sınıf/dönem/sınav VARSAYILAN DEĞİLDİR: verilmezse sorulur (bkz. donem.py).
Ders modülü, seçilen dönemin src/ klasöründen okunur; çıktı aynı dönemin
gorsel_ders_notlari/<DERS ADI>/ klasörüne yazılır.

CoursePack nesnesini alır -> Jinja2 ile HTML üretir -> Playwright/Chromium
ile 175x250mm (+3mm bleed) PDF'e render eder -> sayfa kutularını (TrimBox)
yazar -> Ghostscript ile PDF/X-4 CMYK'ya çevirir.
Çıktı: <sinif>-sinif/<donem>-donem/<sinav>/gorsel_ders_notlari/<DERS ADI>/<slug>.pdf
(CMYK, baskıya hazır) ve (denetim için) aynı klasörde .html

<DERS ADI> klasörü CoursePack.ders_klasoru alanından gelir ve yoksa
otomatik oluşturulur. Bu kural TÜM sınıf/dönem/sınav kombinasyonlarında
geçerlidir.
"""

import sys
import argparse
import subprocess
from dataclasses import dataclass
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from theme_engine import resolve_theme_css
from renk_uretici import pack_rengi
import pdfx
import donem as donem_mod

ROOT = Path(__file__).parent
TEMPLATES = ROOT / "templates"

# ÇIKTI KLASÖRÜ ARTIK SABİT DEĞİL: seçilen sınav dönemine bağlıdır.
# set_donem() çağrılana kadar None kalır -- böylece "hangi döneme yazdığı
# belirsiz" bir build yapısal olarak imkânsızdır (sessizce output/'a düşmez).
DONEM: "donem_mod.Donem | None" = None
OUTPUT: "Path | None" = None


def set_donem(d: "donem_mod.Donem") -> "donem_mod.Donem":
    """Aktif sınav dönemini ayarlar: çıktı klasörünü ve modül arama yolunu kurar.

    build_kitap.py ve tools/*.py bu fonksiyonu çağırıp ardından B.OUTPUT'u
    kullanır; tek kaynak burasıdır.
    """
    global DONEM, OUTPUT
    DONEM = d.ensure().activate()
    OUTPUT = d.gorsel_ders_notlari
    return d


def ders_klasoru_of(pack) -> str:
    """Bir dersin klasör adı: CoursePack.ders_klasoru, yoksa başlık slug'ı.

    Yeni derslerde ders_klasoru'nu HER ZAMAN doldurun (ders programındaki
    büyük harfli tam ad); slug'a düşmek yalnızca geriye dönük uyumluluk
    içindir ve klasör adının dönem ağacındaki diğer isimlerle eşleşmemesine
    yol açar.
    """
    ad = (getattr(pack, "ders_klasoru", "") or "").strip()
    return ad or slugify(pack.title)


def course_out_dir(pack) -> Path:
    """Bu dersin görsel ders notu çıktı klasörü (yoksa oluşturulur):
    <dönem>/gorsel_ders_notlari/<DERS ADI>/"""
    if DONEM is None:
        out_dir()      # dönem seçilmediyse net hatayla durur
    return DONEM.ders_cikti_dizini(ders_klasoru_of(pack))


def out_dir() -> Path:
    """Aktif dönemin çıktı KÖKÜ (gorsel_ders_notlari/).

    Tekil ders dosyaları buraya değil, course_out_dir() ile dersin kendi alt
    klasörüne yazılır; burası birleşik kitabın ve geçici render/ölçüm
    dosyalarının yeridir. Dönem seçilmediyse net bir hatayla durur."""
    if OUTPUT is None:
        raise SystemExit(
            "[hata] Önce sınav dönemi seçilmeli.\n"
            "        Komut satırından: --sinif 2 --donem 2 --sinav final\n"
            "        Kod içinden:      build.set_donem(donem.resolve(args))"
        )
    OUTPUT.mkdir(parents=True, exist_ok=True)
    return OUTPUT


# =============================================================================
# BASKI GEOMETRİSİ — İKİ AYRI ÇIKTI, İKİ AYRI CONFIG
# =============================================================================
# Sayfa ölçüsü, taşma payı ve kenar boşlukları burada TANIMLANIR. Birbirinden
# BAĞIMSIZ iki config vardır (bkz. CLAUDE.md'nin en üstündeki KRİTİK KURAL):
#
#     SINGLE_GEOMETRY -> `python build.py <slug> --sinif X --donem Y --sinav Z`
#                        ile üretilen TEKİL
#                        ders PDF'i.
#     BOOK_GEOMETRY   -> `python build_kitap.py` ile üretilen BİRLEŞİK kitap.
#
# Şu anda ikisinin değerleri aynıdır (175x250mm trim); ama TEK BİR GLOBAL
# SABİT DEĞİLLERDİR: birini değiştirmek diğerini etkilemez. Bir çıktının
# ölçüsünü değiştirdikten sonra sayfalama sabitleri (GLOSSARY_PER_PAGE vb.) ve
# ChapterPage dağılımları o ölçüye göre yeniden ölçülmelidir:
#     python tools/kalibre.py && python tools/dengele.py --hepsi
#
# style.css içindeki aynı adlı :root değişkenleri yalnızca varsayılandır;
# page_geometry_css(geo) seçilen config'ten üretilen bloğu CSS'in SONUNA
# ekleyerek onları ezer. Böylece "CSS'te 175mm ama Chromium'a 210mm verilmiş"
# türü sessiz uyumsuzluk yapısal olarak imkânsızdır.


@dataclass(frozen=True)
class PageGeometry:
    """Tek bir çıktının (tekil ders / birleşik kitap) baskı geometrisi."""

    name: str
    trim_w: float               # bitmiş (kesilmiş) sayfa genişliği (mm)
    trim_h: float               # bitmiş (kesilmiş) sayfa yüksekliği (mm)
    bleed: float = 3.0          # taşma payı (her kenar) — full-bleed zeminler için
    mg_top: float = 11.0
    mg_bottom: float = 19.0     # sayfa numarası payı dahil
    mg_inner: float = 14.0      # sırt/gutter tarafı — PUR Amerikan cilt payı
    mg_outer: float = 9.0
    # Ayna simetri yönü. Standart kitap ciltlemesinde TEK (1, 3, 5...) sayfa
    # sağ yapraktır, dolayısıyla sırtı SOLDA kalır -> "left".  Ciltçiniz
    # tersini istiyorsa tek kelimeyi "right" yapmak yeterlidir.
    odd_page_gutter: str = "left"

    # Fiziksel render ölçüsü (bleed box) — Chromium'a verilen ve PDF MediaBox'ı
    # olan boyut. Trim kutusu bunun `bleed` kadar içindedir (set_print_boxes()).
    @property
    def page_w(self) -> float:
        return self.trim_w + 2 * self.bleed

    @property
    def page_h(self) -> float:
        return self.trim_h + 2 * self.bleed


SINGLE_GEOMETRY = PageGeometry(name="tekil ders", trim_w=175.0, trim_h=250.0)
BOOK_GEOMETRY = PageGeometry(name="birleşik kitap", trim_w=175.0, trim_h=250.0)

# Geriye dönük uyumluluk: tools/olcum.py ve tools/kalibre.py tekil ders
# sayfalarını ölçtükleri için TEKİL config'in değerlerini okur. Yeni kod bu
# modül sabitleri yerine doğrudan bir PageGeometry geçirmelidir.
TRIM_W_MM = SINGLE_GEOMETRY.trim_w
TRIM_H_MM = SINGLE_GEOMETRY.trim_h
BLEED_MM = SINGLE_GEOMETRY.bleed
MARGIN_TOP_MM = SINGLE_GEOMETRY.mg_top
MARGIN_BOTTOM_MM = SINGLE_GEOMETRY.mg_bottom
MARGIN_INNER_MM = SINGLE_GEOMETRY.mg_inner
MARGIN_OUTER_MM = SINGLE_GEOMETRY.mg_outer
ODD_PAGE_GUTTER = SINGLE_GEOMETRY.odd_page_gutter
PAGE_W_MM = SINGLE_GEOMETRY.page_w
PAGE_H_MM = SINGLE_GEOMETRY.page_h


def _mm(v: float) -> str:
    return f"{v:g}mm"


def page_geometry_css(geo: PageGeometry = SINGLE_GEOMETRY) -> str:
    """style.css'in sonuna eklenen, verilen config'ten türetilmiş geometri
    bloğu. Tek/çift sayfa ayna simetrisi burada kurulur: tüm .page'ler <body>'nin
    doğrudan <section> çocukları olduğu için :nth-of-type() sırası PDF'teki
    fiziksel sayfa sırasıyla birebir aynıdır."""
    inner_side = "left" if geo.odd_page_gutter == "left" else "right"
    outer_side = "right" if inner_side == "left" else "left"
    return f"""
/* ===== build.py tarafından üretildi — elle düzenlemeyin ===================
   Config: {geo.name} ·
   Trim {_mm(geo.trim_w)} x {_mm(geo.trim_h)} · bleed {_mm(geo.bleed)} ·
   kenarlar: üst {_mm(geo.mg_top)} / alt {_mm(geo.mg_bottom)} /
   iç {_mm(geo.mg_inner)} / dış {_mm(geo.mg_outer)} ·
   tek sayfa sırtı: {geo.odd_page_gutter}
   ========================================================================= */
@page {{ size: {_mm(geo.page_w)} {_mm(geo.page_h)}; margin: 0; }}
:root {{
  --trim-w: {_mm(geo.trim_w)};
  --trim-h: {_mm(geo.trim_h)};
  --bleed: {_mm(geo.bleed)};
  --page-w: {_mm(geo.page_w)};
  --page-h: {_mm(geo.page_h)};
  --mg-top: {_mm(geo.mg_top)};
  --mg-bottom: {_mm(geo.mg_bottom)};
  --mg-inner: {_mm(geo.mg_inner)};
  --mg-outer: {_mm(geo.mg_outer)};
  --pad-top: {_mm(geo.bleed + geo.mg_top)};
  --pad-bottom: {_mm(geo.bleed + geo.mg_bottom)};
  --pad-inner: {_mm(geo.bleed + geo.mg_inner)};
  --pad-outer: {_mm(geo.bleed + geo.mg_outer)};
}}
/* Ayna simetri — tek sayfada sırt {inner_side}, çift sayfada {outer_side} */
body > section.page:nth-of-type(odd) {{
  --pad-{inner_side}: var(--pad-inner);
  --pad-{outer_side}: var(--pad-outer);
}}
body > section.page:nth-of-type(even) {{
  --pad-{inner_side}: var(--pad-outer);
  --pad-{outer_side}: var(--pad-inner);
}}
"""


def load_css(geo: PageGeometry = SINGLE_GEOMETRY) -> str:
    """style.css + verilen config'ten türetilen geometri bloğu. Tek ders ve
    kitap build'i AYNI fonksiyonu kullanır, ama KENDİ geometry config'iyle."""
    return (TEMPLATES / "style.css").read_text(encoding="utf-8") + page_geometry_css(geo)


def strip_tags(s: str) -> str:
    """Başlıktaki HTML etiketlerini (accent-word span'ı vb.) atar — dosya adı,
    yer imi ve konsol çıktısı gibi düz metin gereken yerler için."""
    import re
    return re.sub(r"<[^>]+>", "", s)


def slugify(s: str) -> str:
    s = strip_tags(s)
    m = {"ı": "i", "ğ": "g", "ü": "u", "ş": "s", "ö": "o", "ç": "c",
         "İ": "i", "Ğ": "g", "Ü": "u", "Ş": "s", "Ö": "o", "Ç": "c"}
    out = "".join(m.get(c, c) for c in s)
    out = "".join(c.lower() if c.isalnum() else "-" for c in out)
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")


def paginate(items: list, per_page: int) -> list[list]:
    """Herhangi bir listeyi (sözlük, soru-cevap, kontrol listesi ...) sabit
    boyutlu sayfalara böler. Önceki sistemin tespit edilen en ciddi kusuru
    -- taşan içeriğin sayfa dışında sessizce kaybolması -- bu fonksiyonla
    yapısal olarak imkansız hale gelir: her öğe mutlaka bir sayfaya girer.

    NOT: Doğrudan kullanmayın; paginate_capped() bunun DENGELİ sürümüdür ve
    üretimde o kullanılır. Bu fonksiyon geriye dönük uyumluluk için durur."""
    return [items[i:i + per_page] for i in range(0, len(items), per_page)] or [[]]


def paginate_capped(items: list, first_cap: int, rest_cap: int | None = None,
                    balanced: bool = True) -> list[list]:
    """Kapasite sınırını aşmadan, öğeleri sayfalara DENGELİ dağıtır.

    Düz paginate() "doldur, kalanı son sayfaya at" mantığıyla çalışır: 30
    kavram / 12 = 12+12+6, yani son sayfa yarı boş kalır. Bu sürüm önce
    gereken en az sayfa sayısını bulur (ilk sayfanın kapasitesi ayrı olabilir --
    testin ilk sayfasında bilgi çubuğu ve talimat kutusu da vardır), sonra
    öğeleri oransal doluluğa göre dağıtır: 30 kavram -> 10+10+10.

    Sayfa sayısı düz paginate() ile aynı ya da ondan azdır; hiçbir sayfa
    kapasitesini aşmaz, dolayısıyla taşma riski artmaz.

    balanced=False: dengelemez, ilk sayfayı DOLDURUP kalanı sonrakine taşır.
    İçindekiler için bu doğru davranıştır -- okuyucu listeyi baştan aşağı
    okur, bir kitabın içindekiler sayfası dolu başlayıp kısa bir taşmayla
    biter; ortadan ikiye bölünmüş yarım dolu iki sayfa yanlış görünür."""
    rest_cap = first_cap if rest_cap is None else rest_cap
    n = len(items)
    if n == 0:
        return [[]]
    pages = 1
    while first_cap + (pages - 1) * rest_cap < n:
        pages += 1
    caps = [first_cap] + [rest_cap] * (pages - 1)
    if not balanced:
        out, k = [], 0
        for c in caps:
            out.append(items[k:k + c])
            k += c
            if k >= n:
                break
        return [chunk for chunk in out if chunk] or [[]]
    counts = [0] * pages
    for _ in range(n):
        # kapasitesi dolmamış sayfalar arasında ORANSAL olarak en boş olana ekle
        cand = [i for i in range(pages) if counts[i] < caps[i]]
        best = min(cand, key=lambda i: (counts[i] / caps[i], i))
        counts[best] += 1
    out, k = [], 0
    for c in counts:
        out.append(items[k:k + c])
        k += c
    return out


def compute_page_numbers(pack, offset: int = 0) -> dict:
    """Her bölümün gerçek başlangıç sayfa numarasını hesaplar. Tek ders
    build'inde offset=0 -> kapak=1, içindekiler=2, genel bakış=3, sonra
    bölümler sırayla kendi page_count() kadar yer kaplar.

    KİTAP build'inde offset, o dersten ÖNCE gelen tüm sayfaların toplamıdır --
    böylece hem alt bilgideki numara hem dersin kendi İçindekiler'i hem de
    ana içindekiler kitap boyunca kesintisiz akan AYNI numarayı gösterir.

    Dönen sözlükteki ek anahtarlar:
      cover/toc/overview/chapters -> dersin ön sayfalarının numaraları
      end                          -> dersin son fiziksel sayfa numarası
      total                        -> dersin toplam sayfa sayısı (offset zinciri için)
    """
    n = offset + 1
    starts = {"cover": n}
    n += 1
    starts["toc"] = n
    n += toc_page_count(pack)
    starts["overview"] = n
    n += OVERVIEW_PAGES
    starts["chapters"] = n
    for ch in pack.chapters:
        starts[ch.number] = n
        n += ch.page_count()
    starts["glossary"] = n
    n += len(paginate_capped(pack.glossary, GLOSSARY_PER_PAGE))
    if pack.test_questions:
        starts["test"] = n
        n += len(paginate_capped(pack.test_questions, TEST_PER_PAGE_FIRST, TEST_PER_PAGE))
        starts["answer_key"] = n
        n += len(paginate_capped(pack.answer_key_items, ANSWER_PER_PAGE))
    else:
        starts["exam"] = n
        n += exam_page_count(pack)
    starts["end"] = n - 1
    starts["total"] = n - offset - 1
    return starts


def toc_rows(pack, page_starts: dict) -> list[dict]:
    """İçindekiler satırları -- bölümler + sözlük + test. Şablon bunları elle
    dizmek yerine buradan alır ki sayfalara bölünebilsinler."""
    rows = [{"num": str(ch.number), "alt": False, "anchor": f"ch-{ch.number}",
             "title": ch.title, "sub": ch.subtitle, "page": page_starts[ch.number]}
            for ch in pack.chapters]
    rows.append({"num": "A", "alt": True, "anchor": "glossary",
                 "title": "Anahtar Kavramlar Sözlüğü",
                 "sub": f"Tanımlı ve bağlamlandırılmış {pack.concept_count()} kavram",
                 "page": page_starts["glossary"]})
    if pack.test_questions:
        rows.append({"num": "B", "alt": True, "anchor": "exam", "title": pack.test_title,
                     "sub": f"{len(pack.test_questions)} soruluk çoktan seçmeli test "
                            "ve çözümlü cevap anahtarı",
                     "page": page_starts["test"]})
    else:
        rows.append({"num": "B", "alt": True, "anchor": "exam", "title": "Sınav Hazırlık",
                     "sub": "Karıştırılan ayrımlar, eşleştirmeler ve son kontrol",
                     "page": page_starts["exam"]})
    return rows


def toc_page_count(pack) -> int:
    """İçindekiler HER ZAMAN TEK SAYFADIR (proje kuralı, bkz. CLAUDE.md).
    Satır sayısı ne olursa olsun bölünmez; sığdırma işini CSS'teki
    `.toc-compact` kipi yapar (bkz. TOC_COMPACT_THRESHOLD)."""
    return 1


def course_context(pack, offset: int = 0, prefix: str = "", pagecls: str = "") -> dict:
    """_ders_govde.html.j2 makrosunun ihtiyaç duyduğu her şeyi tek sözlükte
    toplar. Tek ders build'i ve kitap build'i AYNI fonksiyonu kullanır --
    sayfalama mantığının iki yerde ayrışması böylece imkansız olur."""
    page_starts = compute_page_numbers(pack, offset)
    return {
        "page_starts": page_starts,
        # İçindekiler bölünmez -- tek sayfa, tek parça (bkz. toc_page_count).
        "toc_pages": [toc_rows(pack, page_starts)],
        "toc_compact": len(pack.chapters) + 2 > TOC_COMPACT_THRESHOLD,
        "glossary_pages": paginate_capped(pack.glossary, GLOSSARY_PER_PAGE),
        "qa_pages": paginate_capped(pack.qa_items, QA_PER_PAGE),
        "distinctions_pages": paginate_capped(pack.distinctions, DISTINCTIONS_PER_PAGE),
        "matchtable_pages": paginate_capped(pack.match_table, MATCHTABLE_PER_PAGE),
        "test_pages": paginate_capped(pack.test_questions, TEST_PER_PAGE_FIRST, TEST_PER_PAGE),
        "answer_pages": paginate_capped(pack.answer_key_items, ANSWER_PER_PAGE),
        "prefix": prefix,
        "pagecls": pagecls,
    }


# --- Sayfalama kapasiteleri ---------------------------------------------------
# 175x250mm sayfa için tools/kalibre.py ile ÖLÇÜLDÜ: her aday değer 10 dersin
# hepsinde render edilip taşma denetimine sokuldu, taşmayan en büyük değer
# alındı. Sayfa boyutunu değiştirirseniz `python tools/kalibre.py` çalıştırıp
# bu bloğu yenileyin -- tahminle değiştirmeyin.
GLOSSARY_PER_PAGE = 22     # 2 sütun x 6 satır
QA_PER_PAGE = 12            # LEGACY
DISTINCTIONS_PER_PAGE = 8  # LEGACY
MATCHTABLE_PER_PAGE = 11    # LEGACY
TEST_PER_PAGE_FIRST = 7    # ilk test sayfasında bilgi çubuğu + talimat kutusu da var
TEST_PER_PAGE = 8          # devam sayfalarında (2 sütunlu düzen, 5 seçenekli MCQ)
ANSWER_PER_PAGE = 23       # sayfa başına çözümlü cevap (2 sütunlu düzen)

# İÇİNDEKİLER HER ZAMAN TEK SAYFADIR (proje kuralı, bkz. CLAUDE.md).
# Eskiden TOC_ROWS_FIRST/REST ile sayfalara bölünüyordu; bu sabitler kalktı.
# Satır sayısı bu eşiği aşınca şablon `.toc-compact` sınıfını ekler: lede
# gizlenir, satır dolgusu ve numara dairesi küçülür, alt başlık TEK satıra
# kırpılır (böylece satır yüksekliği sabitlenir). Eşiğin altındaki dersler
# eski ferah görünümü aynen korur.
# Ölçüm: normal satır ~16mm (uzun alt başlıkta 30.8mm'ye çıkabiliyordu),
# compact satır ~11mm; sayfada satırlara ~190mm kalıyor -> 13 satır güvenli.
# En yüklü ders 9 bölüm = 11 satır (kelam_tarihi), yani pay var.
TOC_COMPACT_THRESHOLD = 7

# Genel Bakış 175x250mm'de tek sayfaya sığmıyor (ölçüldü: 214-264mm / 215mm).
# SABİT olarak ikiye bölünür: 1. sayfa hero + 6 kart, 2. sayfa akış + not.
# Ölçüye göre değil yapıya göre bölmek bilinçli: sayfa numaraları render'dan
# ÖNCE hesaplanabilir olmalı (bkz. compute_page_numbers).
OVERVIEW_PAGES = 1


def exam_page_count(pack) -> int:
    """Sınav Hazırlık bölümünün toplam fiziksel sayfa sayısı (Son Tekrar artık
    ayrı bir bölüm değil, bu sayının içinde otomatik olarak yer alır).
    Yapı: [distinctions+matchtable ana sayfa] + [devam sayfaları] + [QA sayfaları]."""
    dpages = paginate_capped(pack.distinctions, DISTINCTIONS_PER_PAGE)
    mpages = paginate_capped(pack.match_table, MATCHTABLE_PER_PAGE)
    qpages = paginate_capped(pack.qa_items, QA_PER_PAGE)
    n = 1  # ana sayfa (distinctions[0] + matchtable[0])
    n += max(0, len(dpages) - 1)
    n += max(0, len(mpages) - 1)
    n += sum(1 for p in qpages if p)
    return n


def build(module_name: str, d: "donem_mod.Donem | None" = None):
    if d is not None:
        set_donem(d)
    if DONEM is None:
        out_dir()      # dönem seçilmediyse burada net hatayla durur
    mod = DONEM.import_ders(module_name)
    pack = mod.get_pack()

    ctx = course_context(pack)
    page_starts = ctx["page_starts"]

    css = load_css()
    theme_override_css = resolve_theme_css(pack.theme_color)

    # Dersin EFEKTİF vurgu rengi. ders-anlatim skill'i de aynı değeri
    # renk_uretici.ders_rengi(<DERS ADI>) ile okur — bir dersin rengi hangi
    # sistemle üretilirse üretilsin aynı kalmalı (bkz. renk_uretici.py).
    _vurgu = pack_rengi(pack)
    _vurgu_kaynak = "theme_color" if pack.theme_color else f"theme-{pack.theme}"
    print(f"[build] Ders vurgu rengi: {_vurgu}  ({_vurgu_kaynak})")

    env = Environment(loader=FileSystemLoader(str(TEMPLATES)))
    template = env.get_template("master.html.j2")
    html = template.render(
        pack=pack, css=css, theme_override_css=theme_override_css, ctx=ctx,
    )

    slug = slugify(pack.title)
    ders_dir = course_out_dir(pack)
    html_path = ders_dir / f"{slug}.html"
    pdf_path = ders_dir / f"{slug}.pdf"
    print(f"[build] Ders klasörü: {ders_dir}")
    html_path.write_text(html, encoding="utf-8")
    print(f"[build] HTML yazıldı: {html_path}")

    # Basit tutarlılık kontrolleri (önceki sistemdeki hataları yapısal olarak yakalamak için)
    warnings = validate(pack)
    for w in warnings:
        print(f"[UYARI] {w}")

    render_pdf(html_path, pdf_path, expected_pages=page_starts["end"])
    optimize_pdf(pdf_path)
    add_bookmarks(pdf_path, pack, page_starts)
    finalize_for_print(pdf_path, strip_tags(pack.title))
    print(f"[build] PDF üretildi: {pdf_path}")
    report_page_count(pdf_path)
    return pdf_path


def finalize_for_print(pdf_path: Path, title: str,
                       geo: PageGeometry = SINGLE_GEOMETRY):
    """Baskı öncesi son iki adım: sayfa kutularını (TrimBox/BleedBox) yaz ve
    Ghostscript ile PDF/X-4 CMYK'ya çevir. Ghostscript yoksa build durmaz --
    net bir kurulum uyarısı basılır ve dosya RGB kalır."""
    pdfx.set_print_boxes(pdf_path, geo.trim_w, geo.trim_h, geo.bleed)
    pdfx.convert_or_warn(pdf_path, title, geo.trim_w, geo.trim_h, geo.bleed)


def report_page_count(pdf_path: Path):
    """Build'in son satırı: gerçek toplam sayfa sayısı + bitmiş sayfa ölçüsü.
    Sayfa boyutu değiştiğinde içerik yeniden aktığı için bu sayı takip
    edilmesi gereken asıl çıktıdır."""
    from pypdf import PdfReader
    n = len(PdfReader(str(pdf_path)).pages)
    boxes = pdfx.read_boxes(pdf_path)
    print("=" * 66)
    print(f"[SONUÇ] Toplam sayfa: {n}")
    print(f"[SONUÇ] Bitmiş (trim) ölçü : {boxes['trimbox'][0]:g} x {boxes['trimbox'][1]:g} mm")
    print(f"[SONUÇ] Bleed dahil ölçü   : {boxes['bleedbox'][0]:g} x {boxes['bleedbox'][1]:g} mm "
          f"(levha/MediaBox {boxes['mediabox'][0]:g} x {boxes['mediabox'][1]:g} mm)")
    print("=" * 66)
    return n


def add_bookmarks(pdf_path: Path, pack, page_starts: dict):
    """PDF'e gerçek okuyucu-paneli yer imleri (outline) ekler -- Adobe/Preview/tarayıcı
    PDF görüntüleyicilerinin sol tarafında görünen native gezinme ağacı. Sayfa içi
    'İçindekiler'deki tıklanabilir linklerden AYRI, ekstra bir gezinme katmanıdır."""
    from pypdf import PdfReader, PdfWriter
    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    writer.append(reader)
    for ch in pack.chapters:
        writer.add_outline_item(f"{ch.number}. {ch.title}", page_starts[ch.number] - 1)
    writer.add_outline_item("Anahtar Kavramlar Sözlüğü", page_starts["glossary"] - 1)
    if pack.test_questions:
        writer.add_outline_item(pack.test_title, page_starts["test"] - 1)
        writer.add_outline_item("Cevap Anahtarı ve Çözümler", page_starts["answer_key"] - 1)
    else:
        writer.add_outline_item("Sınav Hazırlık", page_starts["exam"] - 1)
    with open(pdf_path, "wb") as f:
        writer.write(f)


def optimize_pdf(pdf_path: Path) -> tuple[int, int]:
    """PDF boyutunu, TEKRAR EDEN nesneleri birleştirerek küçültür.

    Chromium her sayfanın CSS gradyanlarını/nokta dokusunu ayrı birer görsel
    nesne olarak gömüyor: 272 sayfalık kitapta 5002 görsel nesnenin sadece
    1646'sı benzersizdi, 15 MB'ı birebir tekrardı. MuPDF'in garbage=4 modu
    aynı içerikli stream'leri tek nesnede birleştirir -- görüntü kalitesi
    hiç düşmez, sadece kopyalar silinir (36.6 MB -> 20.0 MB ölçüldü).

    Sayfa sayısı değişirse değişiklik geri alınır: küçültme uğruna içerik
    kaybetmektense büyük dosya yeğdir."""
    import os
    import pymupdf
    before = pdf_path.stat().st_size
    tmp = pdf_path.with_name(pdf_path.stem + "._opt.pdf")
    doc = pymupdf.open(str(pdf_path))
    pages_before, toc_before = len(doc), len(doc.get_toc())
    doc.save(str(tmp), garbage=4, deflate=True, clean=True)
    doc.close()
    check = pymupdf.open(str(tmp))
    ok = (len(check) == pages_before and len(check.get_toc()) == toc_before)
    check.close()
    if not ok:
        tmp.unlink(missing_ok=True)
        print("[UYARI] Boyut optimizasyonu içeriği değiştirdi -- atlandı, PDF olduğu gibi bırakıldı.")
        return before, before
    os.replace(str(tmp), str(pdf_path))
    after = pdf_path.stat().st_size
    print(f"[build] Boyut: {before/1024/1024:.1f} MB -> {after/1024/1024:.1f} MB "
          f"(%{round((1 - after / before) * 100)} küçüldü, tekrar eden nesneler birleştirildi)")
    return before, after


def validate(pack) -> list[str]:
    """Üretim öncesi otomatik tutarlılık denetimi."""
    warnings = []
    chapter_numbers = [c.number for c in pack.chapters]
    if chapter_numbers != list(range(1, len(chapter_numbers) + 1)):
        warnings.append(f"Bölüm numaraları sıralı/ardışık değil: {chapter_numbers}")
    for c in pack.glossary:
        if c.chapter_ref not in chapter_numbers:
            warnings.append(f"Sözlük terimi '{c.term}' var olmayan {c.chapter_ref}. Bölüme referans veriyor.")
    seen_terms = set()
    for c in pack.glossary:
        key = c.term.strip().lower()
        if key in seen_terms:
            warnings.append(f"Sözlükte tekrarlanan terim: '{c.term}'")
        seen_terms.add(key)
    if pack.test_questions:
        q_nums = [q.number for q in pack.test_questions]
        a_nums = [a.number for a in pack.answer_key_items]
        if q_nums != a_nums:
            warnings.append(f"Test soru numaraları ({q_nums}) ile cevap anahtarı numaraları ({a_nums}) eşleşmiyor.")
        for q in pack.test_questions:
            if not (4 <= len(q.options) <= 5):
                warnings.append(f"Soru {q.number}: {len(q.options)} seçenek var (4 veya 5 olmalı).")
        for a in pack.answer_key_items:
            q = next((q for q in pack.test_questions if q.number == a.number), None)
            if q and a.correct not in q.options:
                warnings.append(f"Cevap anahtarı {a.number}: '{a.correct}' seçeneği soruda yok.")
    return warnings


def render_pdf(html_path: Path, pdf_path: Path, expected_pages: int | None = None,
               attempts: int = 3, geo: PageGeometry = SINGLE_GEOMETRY):
    """PDF'i render eder ve (expected_pages verilmişse) çıktının GERÇEKTEN
    beklenen sayıda sayfa içerdiğini doğrular.

    NEDEN: Chromium, çok sayfalı (200+) dokümanlarda page.pdf() çıktısını
    ARALIKLI olarak sessizce kesebiliyor -- aynı HTML bir denemede 273, bir
    sonrakinde 132 sayfa üretti. Hata vermediği için fark edilmesi imkânsıza
    yakın; bu yüzden sayfa sayısı burada doğrulanır ve tutmuyorsa yeniden
    denenir. Hiçbir koşulda eksik PDF teslim edilmez."""
    for attempt in range(1, attempts + 1):
        overflow = _render_pdf_once(html_path, pdf_path, geo)
        if expected_pages is None:
            return overflow
        from pypdf import PdfReader
        real = len(PdfReader(str(pdf_path)).pages)
        if real == expected_pages:
            return overflow
        print(f"[RENDER UYARISI] PDF {real} sayfa çıktı, {expected_pages} olmalıydı "
              f"(Chromium çıktıyı kesti) -- yeniden deneniyor {attempt}/{attempts}")
    raise RuntimeError(
        f"PDF {attempts} denemede de eksik render edildi ({real}/{expected_pages} sayfa).")


def _render_pdf_once(html_path: Path, pdf_path: Path,
                     geo: PageGeometry = SINGLE_GEOMETRY):
    script = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file:///{html_path.resolve().as_posix()}', {{ waitUntil: 'networkidle' }});

  // --- TAŞMA DENETİMİ: her .page render yüksekliğini (trim + 2*bleed)
  // fiziksel olarak aşıyor mu? Aşıyorsa içerik sessizce kesilir (önceki
  // sistemin kör noktası) -- burada bunu build zamanında YAKALARIZ.
  const overflow = await page.evaluate(() => {{
    const PAGE_H_MM = {geo.page_h};
    const mmToPx = document.querySelector('.page').getBoundingClientRect().height
                   / PAGE_H_MM; // 1mm kaç px render edildi
    const pages = Array.from(document.querySelectorAll('.page'));
    const bad = [];
    pages.forEach((p, i) => {{
      const limit = PAGE_H_MM * mmToPx;
      if (p.scrollHeight > limit + 2) {{  // 2px tolerans
        bad.push({{ index: i + 1, overflowMm: Math.round((p.scrollHeight - limit) / mmToPx * 10) / 10 }});
      }}
    }});
    return bad;
  }});
  console.log('__OVERFLOW__' + JSON.stringify(overflow));

  // preferCSSPageSize: sayfa ölçüsü CSS'teki @page kuralından okunur.
  // width/height'ı elle vermekten DAHA DOĞRU sonuç verir: Chromium elle
  // verilen ölçüde sayfayı ~0.35mm büyütüp içeriği 0.26mm sağa kaydırıyordu;
  // @page ile içerik tam sol-üst köşeye oturuyor (set_print_boxes() TrimBox'ı
  // buna göre hesaplıyor).
  await page.pdf({{
    path: '{pdf_path.resolve().as_posix()}',
    preferCSSPageSize: true,
    printBackground: true
  }});
  await browser.close();
}})();
"""
    tmp_js = out_dir() / "_render.js"
    tmp_js.write_text(script, encoding="utf-8")
    # encoding açıkça verilmeli: Windows varsayılanı (cp1254) node'un
    # UTF-8 hata çıktısını çözemeyip build'i asıl hatayı göstermeden düşürüyor.
    result = subprocess.run(["node", str(tmp_js)], capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
    if result.returncode != 0:
        print("[HATA] PDF render başarısız:")
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError("PDF render başarısız")

    overflow = []
    for line in result.stdout.splitlines():
        if line.startswith("__OVERFLOW__"):
            import json as _json
            bad = _json.loads(line[len("__OVERFLOW__"):])
            overflow = bad
            if bad:
                print(f"[TAŞMA UYARISI] {len(bad)} sayfa {geo.page_w:g}x{geo.page_h:g}mm sınırını aşıyor -- içerik kesiliyor olabilir:")
                for b in bad:
                    print(f"    - Sayfa (fiziksel sıra) {b['index']}: ~{b['overflowMm']}mm taşma")
            else:
                print(f"[build] Taşma denetimi: tüm sayfalar {geo.page_w:g}x{geo.page_h:g}mm sınırları içinde. ✓")
    return overflow   # kitap build'i taşan sayfayı hangi dersin olduğuna çevirmek için kullanır


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    ap = argparse.ArgumentParser(
        prog="build.py",
        description="Tek bir dersin görsel ders notu PDF'ini üretir.",
        epilog="Örnek: python build.py kelam_tarihi --sinif 2 --donem 2 --sinav final",
    )
    ap.add_argument("ders", help="Ders modülünün adı, ör. kelam_tarihi "
                                 "(eski 'content.kelam_tarihi' yazımı da kabul edilir)")
    donem_mod.add_args(ap)
    args = ap.parse_args()

    d = donem_mod.resolve(args)
    print(f"[build] Dönem: {d}  ({d.etiket})")
    build(args.ders, d)
