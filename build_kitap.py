# -*- coding: utf-8 -*-
"""
DERS ÜRETİM SİSTEMİ — build_kitap.py  (BİRLEŞİK KİTAP)
======================================================
Kullanım:
    python build_kitap.py                # content/kitap.py'deki ders sırasını kullanır
    python build_kitap.py content.kitap  # (aynısı, açıkça)

content/kitap.py'de listelenen derslerin hepsini TEK bir HTML'e dizip tek
seferde 175x250mm (+3mm bleed) PDF/X-4 CMYK dosyaya render eder. build.py ile aynı şablon gövdesini
(_ders_govde.html.j2) ve aynı sayfalama fonksiyonlarını kullanır; tek fark,
her derse bir SAYFA OFFSET'i verilmesidir:

  * ders 1 -> offset 0        (kapağı s.1)
  * ders 2 -> offset 32       (kapağı s.33)
  * ...

Bu sayede alt bilgideki numara, dersin kendi İçindekiler'indeki "s.12"
referansı ve ana içindekiler kitap boyunca AYNI kesintisiz numarayı gösterir.
Derslerin offset'i, kitabın ön kısmı (kapak/künye/önsöz/rehber/ana
içindekiler/ders haritası) kadar kaydırılmış olarak başlar.
"""

import sys
import importlib
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

import build as B                       # noqa: E402  (sayfalama/render/validate tek kaynak)
from theme_engine import resolve_theme_css, generate_theme_vars_from_hex   # noqa: E402


# --- Ön kısım sayfa düzeni ---------------------------------------------------
# 175x250mm'de "Sayfa Rehberi" 8 örneğiyle tek sayfaya sığmıyor (ölçüldü:
# ~274mm / 215mm), bu yüzden 4+4 olarak iki sayfaya bölündü.
FRONT_FIXED_PAGES = 5      # ana kapak + künye + önsöz + sayfa rehberi (2 sayfa)
TOC_PER_PAGE = 11          # ana içindekilerde sayfa başına ders satırı
                           # (küçültülmüş puntoda satır ~15mm + başlık bloğu
                           #  ~42mm: 11 satır ~209mm < 220mm metin alanı;
                           #  10 ders -> tek sayfa)


def toc_chunks(courses: list) -> list[list]:
    """Ders listesini ana içindekiler sayfalarına DENGELİ böler: 10 ders ->
    5+5, 14 ders -> 7+7. Düz paginate() 8+2 gibi yamuk bir son sayfa
    bırakırdı; ön kısım kitabın vitrini olduğu için burada denge önemli."""
    n = len(courses)
    pages = max(1, -(-n // TOC_PER_PAGE))
    size = -(-n // pages)
    return [courses[i:i + size] for i in range(0, n, size)]


def front_matter_page_count(n_courses: int) -> int:
    """Derslerin offset'i buna bağlı olduğu için ders sayısından ÖNCE
    hesaplanabilir olmalı: sabit sayfalar + içindekiler + ders haritası."""
    pages = max(1, -(-n_courses // TOC_PER_PAGE))
    return FRONT_FIXED_PAGES + pages + 1


def theme_accents_from_css(css: str) -> dict:
    """style.css'teki sabit .theme-XXXX bloklarından --accent/--accent-dark
    okur. LEGACY derslerin (theme_color'ı olmayan) rengi ana içindekiler ve
    ders haritası için gerekir; renk değerini Python'a elle kopyalamak yerine
    TEK kaynaktan (style.css) okuyoruz."""
    import re
    out = {}
    for m in re.finditer(r"\.theme-([a-z]+)\s*\{(.*?)\}", css, re.S):
        name, blok = m.group(1), m.group(2)
        a = re.search(r"--accent:\s*([^;]+);", blok)
        ad = re.search(r"--accent-dark:\s*([^;]+);", blok)
        if a:
            out[name] = (a.group(1).strip(), (ad.group(1) if ad else a.group(1)).strip())
    return out


def collect_courses(book, offset: int = 0, css: str = "") -> list[dict]:
    """Her dersi sırayla yükler, offset zincirini kurar ve tema kapsamını
    ayırır. Dönen her kayıt: pack, ctx, theme_css, prefix, sayfa aralığı,
    ayrıca ön kısmın ihtiyaç duyduğu renk/sayım bilgileri."""
    courses = []
    fixed = theme_accents_from_css(css) if css else {}
    for i, module_name in enumerate(book.course_modules, start=1):
        pack = importlib.import_module(module_name).get_pack()

        # Tema kapsamı: theme_color veren dersler kendi .ders-N sınıfını alır;
        # LEGACY dersler (theme_color'ı olmayan) style.css'teki sabit
        # .theme-XXXX sınıfını doğrudan .page üzerinde kullanır.
        if pack.theme_color:
            pagecls = f" ders-{i}"
            theme_css = resolve_theme_css(pack.theme_color, f".ders-{i}")
            tv = generate_theme_vars_from_hex(pack.theme_color)
            accent, accent_dark = tv["--accent"], tv["--accent-dark"]
        else:
            pagecls = f" theme-{pack.theme}"
            theme_css = ""
            accent, accent_dark = fixed.get(pack.theme, ("#3d5568", "#24333f"))

        ctx = B.course_context(pack, offset=offset, prefix=f"d{i}-", pagecls=pagecls)
        courses.append({
            "index": i,
            "module": module_name,
            "pack": pack,
            "ctx": ctx,
            "theme_css": theme_css,
            "accent": accent,
            "accent_dark": accent_dark,
            "plain_title": B.strip_tags(pack.title),
            "question_count": len(pack.test_questions) or len(pack.qa_items),
            "page_count": ctx["page_starts"]["total"],
            "first_page": ctx["page_starts"]["cover"],
            "last_page": ctx["page_starts"]["end"],
        })
        offset += ctx["page_starts"]["total"]

    # ders haritasındaki çubuk uzunlukları (en uzun ders = %100)
    longest = max((c["page_count"] for c in courses), default=1)
    for c in courses:
        c["bar_pct"] = round(c["page_count"] / longest * 100, 1)
    return courses


def build_front_matter(book, courses: list[dict], fm_pages: int) -> dict:
    """Ön kısım sayfa numaraları + kitap geneli sayımlar. Şablonda tek bir
    sayfa numarası bile elle yazılmaz; hepsi buradan gelir."""
    chunks = toc_chunks(courses)
    fm = {
        "cover": 1, "imprint": 2, "preface": 3, "guide": 4,
        # rehber FRONT_FIXED_PAGES-3 sayfa tutar (şu an 2: s.4 ve s.5)
        "toc": FRONT_FIXED_PAGES + 1, "map": FRONT_FIXED_PAGES + 1 + len(chunks),
        "toc_chunks": chunks,
        "total": fm_pages,
        "stats": {
            "courses": len(courses),
            "chapters": sum(c["pack"].chapter_count() for c in courses),
            "concepts": sum(c["pack"].concept_count() for c in courses),
            "questions": sum(c["question_count"] for c in courses),
            "pages": fm_pages + sum(c["page_count"] for c in courses),
        },
    }
    assert fm["map"] == fm_pages, (
        f"Ön kısım sayfa hesabı tutarsız: harita s.{fm['map']}, toplam {fm_pages}")
    return fm


def add_book_bookmarks(pdf_path: Path, courses: list[dict], fm: dict):
    """İç içe yer imi ağacı: önce ön kısım sayfaları düz girdi olarak, sonra
    her ders bir üst düğüm ve altında kendi bölümleri, sözlüğü, testi."""
    from pypdf import PdfReader, PdfWriter
    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    writer.append(reader)
    total = 0
    for label, key in [("Künye", "imprint"), ("Bu Kitap Nasıl Kullanılır", "preface"),
                       ("Sayfa Rehberi", "guide"), ("Ana İçindekiler", "toc"),
                       ("Ders Haritası", "map")]:
        writer.add_outline_item(label, fm[key] - 1)
        total += 1
    for c in courses:
        pack, ps = c["pack"], c["ctx"]["page_starts"]
        parent = writer.add_outline_item(
            f"{c['index']}. {B.strip_tags(pack.title)}", ps["cover"] - 1
        )
        total += 1
        for ch in pack.chapters:
            writer.add_outline_item(f"{ch.number}. {ch.title}", ps[ch.number] - 1, parent=parent)
            total += 1
        writer.add_outline_item("Anahtar Kavramlar Sözlüğü", ps["glossary"] - 1, parent=parent)
        total += 1
        if pack.test_questions:
            writer.add_outline_item(pack.test_title, ps["test"] - 1, parent=parent)
            writer.add_outline_item("Cevap Anahtarı ve Çözümler", ps["answer_key"] - 1, parent=parent)
            total += 2
        else:
            writer.add_outline_item("Sınav Hazırlık", ps["exam"] - 1, parent=parent)
            total += 1
    with open(pdf_path, "wb") as f:
        writer.write(f)
    return total


def report_overflow(overflow: list, courses: list[dict]):
    """Taşan fiziksel sayfa numarasını 'hangi dersin kaçıncı sayfası'na çevirir --
    370 sayfalık bir kitapta çıplak sayfa numarası tek başına işe yaramaz."""
    if not overflow:
        return
    print("[KİTAP] Taşan sayfaların ders karşılıkları:")
    for b in overflow:
        pg = b["index"]
        owner = next((c for c in courses if c["first_page"] <= pg <= c["last_page"]), None)
        if owner is None and pg <= courses[0]["first_page"] - 1:
            print(f"    - s.{pg} -> KİTABIN ÖN KISMI, ~{b['overflowMm']}mm")
            continue
        if owner:
            local = pg - owner["first_page"] + 1
            print(f"    - s.{pg} -> {B.strip_tags(owner['pack'].title)} "
                  f"(dersin {local}. sayfası), ~{b['overflowMm']}mm")
        else:
            print(f"    - s.{pg} -> (ders eşleşmedi), ~{b['overflowMm']}mm")


def verify_page_numbers(courses: list[dict], pdf_path: Path, fm: dict):
    """Numaralandırma zincirini programatik doğrular: dersler boşluksuz ve
    üst üste binmeden dizilmiş mi, toplam sayfa PDF'in gerçek sayfa sayısıyla
    aynı mı? Sessiz numara kaymasını yakalayan asıl güvenlik ağı budur."""
    from pypdf import PdfReader
    problems = []
    expected = fm["total"] + 1      # dersler ön kısmın hemen ardından başlar
    for c in courses:
        if c["first_page"] != expected:
            problems.append(
                f"{B.strip_tags(c['pack'].title)}: s.{c['first_page']}'den başlıyor, "
                f"s.{expected} olmalıydı")
        expected = c["last_page"] + 1
    real_pages = len(PdfReader(str(pdf_path)).pages)
    if real_pages != expected - 1:
        problems.append(f"Hesaplanan toplam {expected - 1} sayfa, PDF'te {real_pages} sayfa var")
    if fm["stats"]["pages"] != real_pages:
        problems.append(f"Kapaktaki '{fm['stats']['pages']} sayfa' istatistiği "
                        f"gerçek {real_pages} sayfayla uyuşmuyor")
    for p in problems:
        print(f"[NUMARA HATASI] {p}")
    if not problems:
        print(f"[kitap] Sayfa numarası zinciri tutarlı: {real_pages} sayfa "
              f"({fm['total']} ön kısım + {len(courses)} ders), boşluk/çakışma yok. ✓")
    return problems


def build_book(module_name: str = "content.kitap"):
    book = importlib.import_module(module_name).get_book()
    css = B.load_css()

    fm_pages = front_matter_page_count(len(book.course_modules))
    courses = collect_courses(book, offset=fm_pages, css=css)
    fm = build_front_matter(book, courses, fm_pages)

    print(f"[kitap] Ön kısım {fm_pages} sayfa (kapak s.1, künye s.{fm['imprint']}, "
          f"önsöz s.{fm['preface']}, rehber s.{fm['guide']}, "
          f"içindekiler s.{fm['toc']}, harita s.{fm['map']})")
    print(f"[kitap] {len(courses)} ders birleştiriliyor:")
    for c in courses:
        print(f"    {c['index']:2d}. {B.strip_tags(c['pack'].title):42s} "
              f"s.{c['first_page']}-{c['last_page']}  ({c['ctx']['page_starts']['total']} sayfa)")

    for c in courses:
        for w in B.validate(c["pack"]):
            print(f"[UYARI] {B.strip_tags(c['pack'].title)}: {w}")

    env = Environment(loader=FileSystemLoader(str(B.TEMPLATES)))
    html = env.get_template("kitap.html.j2").render(
        book=book, css=css, courses=courses, fm=fm,
        front_theme_css=resolve_theme_css(book.theme_color, ".kitap"),
    )

    slug = B.slugify(book.title)
    html_path = B.OUTPUT / f"{slug}.html"
    pdf_path = B.OUTPUT / f"{slug}.pdf"
    html_path.write_text(html, encoding="utf-8")
    print(f"[kitap] HTML yazıldı: {html_path} ({len(html) // 1024} KB)")

    overflow = B.render_pdf(html_path, pdf_path, expected_pages=fm["stats"]["pages"])
    report_overflow(overflow, courses)
    B.optimize_pdf(pdf_path)
    verify_page_numbers(courses, pdf_path, fm)
    n = add_book_bookmarks(pdf_path, courses, fm)
    B.finalize_for_print(pdf_path, B.strip_tags(book.title))
    size_mb = pdf_path.stat().st_size / 1024 / 1024
    print(f"[kitap] Yer imi ağacı: {n} girdi ({len(courses)} ders düğümü + alt başlıklar)")
    print(f"[kitap] PDF üretildi: {pdf_path} ({size_mb:.1f} MB)")
    B.report_page_count(pdf_path)
    return pdf_path


if __name__ == "__main__":
    build_book(sys.argv[1] if len(sys.argv) > 1 else "content.kitap")
