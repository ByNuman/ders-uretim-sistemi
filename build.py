# -*- coding: utf-8 -*-
"""
DERS ÜRETİM SİSTEMİ — build.py
================================
Kullanım:
    python3 build.py content.psikoloji

CoursePack nesnesini alır -> Jinja2 ile HTML üretir -> Playwright/Chromium
ile A4 PDF'e render eder. Çıktı: output/<slug>.pdf ve (denetim için) .html
"""

import sys
import subprocess
import importlib
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from theme_engine import resolve_theme_css

ROOT = Path(__file__).parent
TEMPLATES = ROOT / "templates"
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)


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
    yapısal olarak imkansız hale gelir: her öğe mutlaka bir sayfaya girer."""
    return [items[i:i + per_page] for i in range(0, len(items), per_page)] or [[]]


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
    starts = {"cover": n, "toc": n + 1, "overview": n + 2, "chapters": n + 3}
    n += 3
    for ch in pack.chapters:
        starts[ch.number] = n
        n += ch.page_count()
    glossary_pages_count = len(paginate(pack.glossary, GLOSSARY_PER_PAGE))
    starts["glossary"] = n
    n += glossary_pages_count
    if pack.test_questions:
        starts["test"] = n
        n += len(paginate(pack.test_questions, TEST_PER_PAGE))
        starts["answer_key"] = n
        n += len(paginate(pack.answer_key_items, ANSWER_PER_PAGE))
    else:
        starts["exam"] = n
        n += exam_page_count(pack)
    starts["end"] = n - 1
    starts["total"] = n - offset - 1
    return starts


def course_context(pack, offset: int = 0, prefix: str = "", pagecls: str = "") -> dict:
    """_ders_govde.html.j2 makrosunun ihtiyaç duyduğu her şeyi tek sözlükte
    toplar. Tek ders build'i ve kitap build'i AYNI fonksiyonu kullanır --
    sayfalama mantığının iki yerde ayrışması böylece imkansız olur."""
    return {
        "page_starts": compute_page_numbers(pack, offset),
        "glossary_pages": paginate(pack.glossary, GLOSSARY_PER_PAGE),
        "qa_pages": paginate(pack.qa_items, QA_PER_PAGE),
        "distinctions_pages": paginate(pack.distinctions, DISTINCTIONS_PER_PAGE),
        "matchtable_pages": paginate(pack.match_table, MATCHTABLE_PER_PAGE),
        "test_pages": paginate(pack.test_questions, TEST_PER_PAGE),
        "answer_pages": paginate(pack.answer_key_items, ANSWER_PER_PAGE),
        "prefix": prefix,
        "pagecls": pagecls,
    }


GLOSSARY_PER_PAGE = 18     # 2 sütun x 9 satır -- değişken tanım uzunluğuna karşı güvenlik paylı
QA_PER_PAGE = 10
DISTINCTIONS_PER_PAGE = 6
MATCHTABLE_PER_PAGE = 9
TEST_PER_PAGE = 6          # sayfa başına soru (2 sütunlu düzen, 5 seçenekli MCQ, ilk sayfada bilgi çubuğu+talimat da var — güvenlik paylı)
ANSWER_PER_PAGE = 16       # sayfa başına çözümlü cevap (2 sütunlu düzen)


def exam_page_count(pack) -> int:
    """Sınav Hazırlık bölümünün toplam fiziksel sayfa sayısı (Son Tekrar artık
    ayrı bir bölüm değil, bu sayının içinde otomatik olarak yer alır).
    Yapı: [distinctions+matchtable ana sayfa] + [devam sayfaları] + [QA sayfaları]."""
    dpages = paginate(pack.distinctions, DISTINCTIONS_PER_PAGE)
    mpages = paginate(pack.match_table, MATCHTABLE_PER_PAGE)
    qpages = paginate(pack.qa_items, QA_PER_PAGE)
    n = 1  # ana sayfa (distinctions[0] + matchtable[0])
    n += max(0, len(dpages) - 1)
    n += max(0, len(mpages) - 1)
    n += sum(1 for p in qpages if p)
    return n


def build(module_name: str):
    mod = importlib.import_module(module_name)
    pack = mod.get_pack()

    ctx = course_context(pack)
    page_starts = ctx["page_starts"]

    css = (TEMPLATES / "style.css").read_text(encoding="utf-8")
    theme_override_css = resolve_theme_css(pack.theme_color)
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)))
    template = env.get_template("master.html.j2")
    html = template.render(
        pack=pack, css=css, theme_override_css=theme_override_css, ctx=ctx,
    )

    slug = slugify(pack.title)
    html_path = OUTPUT / f"{slug}.html"
    pdf_path = OUTPUT / f"{slug}.pdf"
    html_path.write_text(html, encoding="utf-8")
    print(f"[build] HTML yazıldı: {html_path}")

    # Basit tutarlılık kontrolleri (önceki sistemdeki hataları yapısal olarak yakalamak için)
    warnings = validate(pack)
    for w in warnings:
        print(f"[UYARI] {w}")

    render_pdf(html_path, pdf_path, expected_pages=page_starts["end"])
    optimize_pdf(pdf_path)
    add_bookmarks(pdf_path, pack, page_starts)
    print(f"[build] PDF üretildi: {pdf_path}")
    return pdf_path


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
               attempts: int = 3):
    """PDF'i render eder ve (expected_pages verilmişse) çıktının GERÇEKTEN
    beklenen sayıda sayfa içerdiğini doğrular.

    NEDEN: Chromium, çok sayfalı (200+) dokümanlarda page.pdf() çıktısını
    ARALIKLI olarak sessizce kesebiliyor -- aynı HTML bir denemede 273, bir
    sonrakinde 132 sayfa üretti. Hata vermediği için fark edilmesi imkânsıza
    yakın; bu yüzden sayfa sayısı burada doğrulanır ve tutmuyorsa yeniden
    denenir. Hiçbir koşulda eksik PDF teslim edilmez."""
    for attempt in range(1, attempts + 1):
        overflow = _render_pdf_once(html_path, pdf_path)
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


def _render_pdf_once(html_path: Path, pdf_path: Path):
    script = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file:///{html_path.resolve().as_posix()}', {{ waitUntil: 'networkidle' }});

  // --- TAŞMA DENETİMİ: her .page 297mm'lik A4 yüksekliğini fiziksel olarak
  // aşıyor mu? Aşıyorsa içerik sessizce kesilir (önceki sistemin kör noktası) --
  // burada bunu build zamanında YAKALARIZ, PDF üretildikten sonra keşfetmeyiz.
  const overflow = await page.evaluate(() => {{
    const mmToPx = document.querySelector('.page').getBoundingClientRect().height
                   / 297; // 1mm kaç px render edildi
    const pages = Array.from(document.querySelectorAll('.page'));
    const bad = [];
    pages.forEach((p, i) => {{
      const limit = 297 * mmToPx;
      if (p.scrollHeight > limit + 2) {{  // 2px tolerans
        bad.push({{ index: i + 1, overflowMm: Math.round((p.scrollHeight - limit) / mmToPx * 10) / 10 }});
      }}
    }});
    return bad;
  }});
  console.log('__OVERFLOW__' + JSON.stringify(overflow));

  await page.pdf({{
    path: '{pdf_path.resolve().as_posix()}',
    width: '210mm', height: '297mm',
    printBackground: true,
    margin: {{ top: '0', bottom: '0', left: '0', right: '0' }}
  }});
  await browser.close();
}})();
"""
    tmp_js = OUTPUT / "_render.js"
    tmp_js.write_text(script, encoding="utf-8")
    result = subprocess.run(["node", str(tmp_js)], capture_output=True, text=True)
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
                print(f"[TAŞMA UYARISI] {len(bad)} sayfa A4 sınırını aşıyor -- içerik kesiliyor olabilir:")
                for b in bad:
                    print(f"    - Sayfa (fiziksel sıra) {b['index']}: ~{b['overflowMm']}mm taşma")
            else:
                print("[build] Taşma denetimi: tüm sayfalar A4 sınırları içinde. ✓")
    return overflow   # kitap build'i taşan sayfayı hangi dersin olduğuna çevirmek için kullanır


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    module_name = sys.argv[1] if len(sys.argv) > 1 else "content.psikoloji"
    build(module_name)
