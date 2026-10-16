# -*- coding: utf-8 -*-
"""
4. HAFTA BİRLEŞİK DERS NOTLARI KİTABI ÜRETİCİSİ
================================================
Kullanıcı Kuralları:
  1. Ana Kapak daima önce CSS/SVG vektörel olarak yapılır (cover_image="").
     Yalnızca kullanıcı açıkça "değiştir" dediğinde veya özel kapak görseli
     eklediğinde (haftalik-ders-4-hafta-kapak.png) görsel kapak atanır.
  2. 10 dersin mevcut PDF'leri (kapakları, görsel kutularındaki tüm görselleri
     ve zengin içerikleri %100 korunarak) haftalık ders programı sırasıyla birleştirilir.
  3. Sayfa numaraları kesintisiz (s. 1 – 190) ve vektörel temizlikle damgalanır.
"""

import sys
from pathlib import Path
import pymupdf
from jinja2 import Environment, FileSystemLoader

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import build as B
from cekirdek import donem as donem_mod
from cekirdek.theme_engine import resolve_theme_css
import build_kitap

BASE_DIR = ROOT / "3-sinif" / "1-donem" / "vize" / "gorsel_ders_notlari"
OUT_PDF = BASE_DIR / "HAFTALIK DERSLER" / "4. HAFTA" / "haftalik-ders-4-hafta.pdf"
OUT_PDF.parent.mkdir(parents=True, exist_ok=True)

CUSTOM_COVER_PNG = BASE_DIR / "HAFTALIK DERSLER" / "4. HAFTA" / "haftalik-ders-4-hafta-kapak.png"

# 10 Dersin Ders Programı Sırasıyla Listesi: (Başlık, PDF Yolu, Varsayılan Tema Rengi RGB)
COURSES = [
    (
        "1. Arap Dili ve Edebiyatı V · 3. Ünite",
        BASE_DIR / "ARAP DİLİ VE EDEBİYATI V" / "3. Ünite" / "arap-dili-ve-edebiyati-v-3-unite.pdf",
        (0.5686, 0.1686, 0.1098),  # #8C2F21
    ),
    (
        "2. Tasavvuf I — 4. Hafta",
        BASE_DIR / "TASAVVUF I" / "4. Hafta" / "tasavvuf-4-hafta.pdf",
        (0.5098, 0.1686, 0.3843),  # #7B3260
    ),
    (
        "3. Hadis III — 4. Hafta",
        BASE_DIR / "HADİS III" / "4. Hafta" / "hadis-3-hafta-4.pdf",
        (0.4196, 0.2627, 0.1216),  # #664324
    ),
    (
        "4. Tefsir III — 4. Hafta",
        BASE_DIR / "TEFSİR III" / "4. Hafta" / "tefsir-3-hafta-4.pdf",
        (0.1059, 0.3961, 0.2510),  # #206040
    ),
    (
        "5. Sınıf Yönetimi — 4. Hafta",
        BASE_DIR / "SINIF YÖNETİMİ" / "4. Hafta" / "sinif-yonetimi-hafta-4.pdf",
        (0.1020, 0.2784, 0.4784),  # #1F4775
    ),
    (
        "6. İslam Felsefesi Tarihi I — 4. Hafta",
        BASE_DIR / "İSLAM FELSEFESİ TARİHİ I" / "4. Hafta" / "islam-felsefesi-tarihi-1-hafta-4.pdf",
        (0.1608, 0.1490, 0.4902),  # #2F2D76
    ),
    (
        "7. Sistematik Kelâm I — 4. Hafta",
        BASE_DIR / "SİSTEMATİK KELAM I" / "4. Hafta" / "sistematik-kelam-1-hafta-4.pdf",
        (0.3529, 0.1569, 0.5020),  # #592F79
    ),
    (
        "8. İslam Medeniyeti Tarihi — 4. Hafta",
        BASE_DIR / "İSLAM MEDENİYETİ TARİHİ" / "4. Hafta" / "islam_medeniyeti_tarihi_hafta_4.pdf",
        (0.4667, 0.4118, 0.1922),  # #776931
    ),
    (
        "9. Din Eğitimi — 4. Hafta",
        BASE_DIR / "DİN EĞİTİMİ" / "4. Hafta" / "din-egitimi-4-hafta.pdf",
        (0.3216, 0.4118, 0.1686),  # #51662E
    ),
    (
        "10. İslâm Hukuku I — 4. Hafta",
        BASE_DIR / "İSLAM HUKUKU I" / "4. Hafta" / "islam-hukuku-4-hafta.pdf",
        (0.4863, 0.0863, 0.1765),  # #7A2433
    ),
]


def render_front_matter_pdf() -> Path:
    """Kullanıcı özel kapak eklediyse onu kullanır, yoksa Kural 5 gereği CSS kapak üretir."""
    d = donem_mod.Donem(sinif=3, donem=1, sinav="vize")
    B.set_donem(d)

    mod = d.import_ders("haftalik_ders_4_hafta")
    book = mod.get_book()

    if CUSTOM_COVER_PNG.exists():
        from cekirdek.content_model import resim_data_uri
        book.cover_image = resim_data_uri(CUSTOM_COVER_PNG)
        print(f"  ✓ Özel ana kapak görseli bağlandı: {CUSTOM_COVER_PNG.name}")
    else:
        book.cover_image = ""
        print("  ✓ Kural 5 gereği CSS vektörel kapak üretiliyor.")

    css = B.load_css(B.BOOK_GEOMETRY)
    fm_pages = build_kitap.front_matter_page_count(len(book.course_modules))
    courses = build_kitap.collect_courses(book, offset=fm_pages, css=css)
    fm = build_kitap.build_front_matter(book, courses, fm_pages)

    env = Environment(loader=FileSystemLoader(str(B.TEMPLATES)))
    front_html_template = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>{{ book.title }}</title>
<style>{{ css }}</style>
<style>{{ front_theme_css }}</style>
</head>
<body class="theme-custom">
{% import "_kitap_on_kisim.html.j2" as on %}
{{ on.front_matter(book, courses, fm) }}
</body>
</html>"""

    html = env.from_string(front_html_template).render(
        book=book,
        css=css,
        courses=courses,
        fm=fm,
        front_theme_css=resolve_theme_css(book.theme_color, ".kitap"),
    )

    tmp_dir = ROOT / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    html_path = tmp_dir / "front_matter_week4.html"
    pdf_path = tmp_dir / "front_matter_week4.pdf"
    html_path.write_text(html, encoding="utf-8")
    B.render_pdf(html_path, pdf_path, expected_pages=4, geo=B.BOOK_GEOMETRY)
    return pdf_path


def build_merged_book():
    print("[1/5] Mevcut ders PDF'leri ve sayfa sayıları kontrol ediliyor...")
    total_course_pages = 0
    course_data = []
    for title, path, color in COURSES:
        if not path.exists():
            raise FileNotFoundError(f"Ders PDF'i bulunamadı: {path}")
        doc = pymupdf.open(str(path))
        num_pages = len(doc)
        num_images = sum(len(page.get_images()) for page in doc)
        print(f"  ✓ {title:42s} -> {num_pages:2d} sayfa, {num_images:2d} görsel")
        total_course_pages += num_pages
        course_data.append((title, doc, color, num_pages))

    print(f"  Toplam ders sayfası: {total_course_pages}")

    print("\n[2/5] Ön kısım derleniyor...")
    front_pdf_path = render_front_matter_pdf()
    front_doc = pymupdf.open(str(front_pdf_path))

    out_doc = pymupdf.open()
    out_doc.insert_pdf(front_doc)
    front_doc.close()
    print("  ✓ Ön kısım eklendi (s.1 Ana Kapak, s.2 Boş Sayfa, s.3-4 Ana İçindekiler).")

    FRONT_MATTER_PAGES = 4
    current_offset = FRONT_MATTER_PAGES
    toc_tree = [[1, "Ana İçindekiler", 3]]

    print("\n[3/5] Derslerin sayfaları, kapakları ve görselleri korunarak kesintisiz numaralandırılıyor...")
    for title, doc, default_color, num_pages in course_data:
        start_page = current_offset + 1
        end_page = current_offset + num_pages
        print(f"  İşleniyor: {title:40s} -> s.{start_page}–{end_page} ({num_pages} sf)")

        # Ders üst yer imi
        toc_tree.append([1, title, start_page])

        # Alt yer imleri (bölümler, sözlük, test)
        orig_toc = doc.get_toc()
        for item in orig_toc:
            lvl, item_title, orig_pno = item[0], item[1], item[2]
            new_pno = orig_pno + current_offset
            toc_tree.append([lvl + 1, item_title, new_pno])

        # Sayfaları işle ve ekle
        for page_idx in range(num_pages):
            src_page = doc[page_idx]
            global_pno = current_offset + page_idx + 1

            # s.1 Kapak ve s.2 Boş sayfa hariç: s.3 ve sonrasındaki sayfalara numara güncellemesi yap
            if page_idx >= 2:
                # 1. Sayfadaki mevcut rozet rengini tespit et
                fill_color = default_color
                for d in src_page.get_drawings():
                    if d["rect"].y0 > 800 and d["rect"].x0 > 500 and d.get("fill"):
                        fill_color = d["fill"]
                        break

                # 2. Eski sayfa numarasını vektörel olarak temizle
                redact_rect = pymupdf.Rect(525, 800, 568, 822)
                src_page.add_redact_annot(redact_rect, fill=(1, 1, 1))
                src_page.apply_redactions()

                # 3. Yeni sayfa numarasını ders renginde rozet ile damgala
                num_str = str(global_pno)
                num_digits = len(num_str)
                w = 14.25 if num_digits == 1 else (18.75 if num_digits == 2 else 23.25)
                x0 = 561.0 - w
                badge_rect = pymupdf.Rect(x0, 803.25, 561.0, 816.75)
                src_page.draw_rect(badge_rect, color=None, fill=fill_color, radius=0.25)

                # 4. Beyaz metin
                text_len = pymupdf.get_text_length(num_str, fontname="helv", fontsize=7.6)
                tx = x0 + (w - text_len) / 2.0
                src_page.insert_text(
                    pymupdf.Point(tx, 812.25),
                    num_str,
                    fontname="helv",
                    fontsize=7.6,
                    color=(1, 1, 1),
                )

        # İşlenen ders sayfalarını birleşik dökümana ekle
        out_doc.insert_pdf(doc)
        current_offset += num_pages

    print("\n[4/5] PDF yer imleri (outline) kaydediliyor...")
    out_doc.set_toc(toc_tree)
    print(f"  ✓ Toplam {len(toc_tree)} yer imi düğümü ağaca eklendi.")

    print("\n[5/5] Birleşik PDF optimize edilip kaydediliyor...")
    out_doc.save(str(OUT_PDF), deflate=True, garbage=4)
    file_size_mb = OUT_PDF.stat().st_size / (1024 * 1024)
    total_pages = len(out_doc)
    out_doc.close()

    for _, doc, _, _ in course_data:
        doc.close()

    print(f"\n=======================================================")
    print(f"BAŞARIYLA TAMAMLANDI!")
    print(f"Çıktı Dosyası: {OUT_PDF}")
    print(f"Toplam Sayfa : {total_pages} (4 ön kısım + {total_course_pages} ders)")
    print(f"Dosya Boyutu : {file_size_mb:.2f} MB")
    print(f"=======================================================")


if __name__ == "__main__":
    build_merged_book()
