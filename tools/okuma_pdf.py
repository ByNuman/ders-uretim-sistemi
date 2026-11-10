# -*- coding: utf-8 -*-
#
# Görsel Ders Notu Üretim Sistemi
# Copyright (C) 2026 Numan Gözdaş
#
# Bu program özgür yazılımdır: Özgür Yazılım Vakfı'nın yayımladığı GNU Genel
# Kamu Lisansı'nın 3. sürümü koşulları altında yeniden dağıtabilir ve/veya
# değiştirebilirsiniz.
#
"""
tools/okuma_pdf.py — OKUMA PDF ÜRETİM MOTORU
=============================================
Yazılı ders özetlerini (.md) görsel ders notu tipografik standartlarıyla
(bordo/kurumsal renkli ünite banner'ları, hiyerarşik rozetler, BiDi izoleli iri
Arapça metinler, nass levhaları, sınav uyarı kutuları, zebra desenli tablolar ve
özel sayfa altlıkları) yüksek prestijli bir "Okuma PDF" dokümanına dönüştürür.

Kullanım:
    python tools/okuma_pdf.py <dosya_veya_ders_adi> [--sinif X] [--donem Y] [--sinav Z]
    python tools/okuma_pdf.py "3-sinif/1-donem/vize/ders_anlatimlari/ARAP DİLİ VE EDEBİYATI V/Arap Dili ve Edebiyatı V - Vize Sınavı Konu Özeti (Sarf-Nahiv ve Alıştırmasız).md"
"""

import os
import re
import sys
import shutil
import argparse
from pathlib import Path
import markdown
from playwright.sync_api import sync_playwright
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cekirdek import donem as donem_mod
from cekirdek.renk_uretici import ders_rengi

sys.stdout.reconfigure(encoding='utf-8')

# Regex ve Semboller
ARABIC_RE = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')

UNIT_ICONS = {
    "1. ÜNİTE": "📚",
    "2. ÜNİTE": "⚔️",
    "3. ÜNİTE": "📜",
    "4. ÜNİTE": "💡",
    "5. ÜNİTE": "🕊️",
    "6. ÜNİTE": "🏛️",
    "7. ÜNİTE": "⚖️",
    "8. ÜNİTE": "🔍",
    "9. ÜNİTE": "📖",
    "10. ÜNİTE": "✨"
}

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def darken_color(hex_code, factor=0.75):
    r, g, b = hex_to_rgb(hex_code)
    return f"#{int(r*factor):02x}{int(g*factor):02x}{int(b*factor):02x}"

def lighten_color(hex_code, factor=0.15):
    r, g, b = hex_to_rgb(hex_code)
    nr = int(r + (255 - r) * factor)
    ng = int(g + (255 - g) * factor)
    nb = int(b + (255 - b) * factor)
    return f"#{nr:02x}{ng:02x}{nb:02x}"

def generate_okuma_pdf(md_path: Path, output_pdf_path: Path = None, course_name: str = "", theme_hex: str = "#8C2F21"):
    """Tek bir Markdown özet dosyasından yüksek estetikli Okuma PDF üretir."""
    if not md_path.exists():
        raise FileNotFoundError(f"Markdown dosyası bulunamadı: {md_path}")

    raw_text = md_path.read_text(encoding="utf-8")

    # Ünite başlangıç noktasını tespit et (Ön kapak, künye, içindekiler atlanır)
    u1_match = re.search(r'^#\s+1\.\s+ÜNİTE', raw_text, flags=re.MULTILINE)
    start_idx = u1_match.start() if u1_match else 0

    # Sınav kontrol tablosu veya ekstra kısımlar varsa bitiş noktasını tespit et
    end_match = re.search(r'^#\s+7\.\s+SINAV', raw_text, flags=re.MULTILINE)
    end_idx = end_match.start() if end_match else len(raw_text)

    pure_md = raw_text[start_idx:end_idx].strip()
    pure_md = re.sub(r'---+\s*$', '', pure_md).strip()

    # H2 başlıklarını rozetli hale getir (## X.Y. Başlık -> ## <span class="h2-badge">X.Y.</span> Başlık)
    def format_h2(match):
        prefix = match.group(1)
        title = match.group(2)
        return f'## <span class="h2-badge">{prefix}</span> {title}'

    pure_md = re.sub(r'^##\s+(\d+\.\d+\.?)\s+(.+)$', format_h2, pure_md, flags=re.MULTILINE)

    # Markdown -> HTML
    html_body = markdown.markdown(pure_md, extensions=['tables', 'fenced_code', 'sane_lists'])

    # Ünite başlıklarını (H1) banner levhalarına dönüştür
    def replace_h1(match):
        content = match.group(1).strip()
        is_first = "1. ÜNİTE" in content or "1. BÖLÜM" in content
        cls = "unit-banner-container first-unit" if is_first else "unit-banner-container"
        icon = "📖"
        for k, v in UNIT_ICONS.items():
            if k in content:
                icon = v
                break
        return f'''<div class="{cls}">
            <div class="unit-banner-inner">
                <span class="unit-icon">{icon}</span>
                <h1 class="unit-title">{content}</h1>
            </div>
        </div>'''

    html_body = re.sub(r'<h1>([\s\S]*?)</h1>', replace_h1, html_body)

    # H3 başlıklarına altın elmas imi ekle
    def replace_h3(match):
        content = match.group(1).strip()
        return f'<h3 class="h3-styled"><span class="h3-diamond">◆</span> {content}</h3>'

    html_body = re.sub(r'<h3>([\s\S]*?)</h3>', replace_h3, html_body)

    # Ünite öncesi <hr> temizliği
    html_body = re.sub(r'<hr\s*/?>\s*(<div class="unit-banner-container)', r'\1', html_body)

    # Inline Arapça kod blokları
    def tag_arabic_code(match):
        code_text = match.group(1)
        if ARABIC_RE.search(code_text):
            return f'<code class="ar" dir="rtl"><bdi>{code_text}</bdi></code>'
        return f'<code>{code_text}</code>'

    html_body = re.sub(r'<code>([^<]+)</code>', tag_arabic_code, html_body)

    # Çift tırnaklı Arapça ibareler « ... »
    def tag_arabic_quotes(match):
        inside = match.group(1).strip()
        if ARABIC_RE.search(inside):
            return f'<span class="ar-quote">«<bdi class="ar" dir="rtl">{inside}</bdi>»</span>'
        return f'«{inside}»'

    html_body = re.sub(r'«([^»]+)»', tag_arabic_quotes, html_body)

    # Callout / Alıntı kutuları (📌 Sınav & Dipnot vs Arapça Nass)
    def tag_blockquotes(match):
        content = match.group(1)
        if '📌' in content:
            clean_content = content.replace('📌', '').strip()
            return f'''<blockquote class="callout callout-pinned">
                <div class="pinned-header"><span class="pinned-tag">📌 KİTAP DİPNOTU &amp; SINAV UYARISI</span></div>
                {clean_content}
            </blockquote>'''
        elif '«' in content or ARABIC_RE.search(content):
            return f'''<blockquote class="callout callout-nass">
                {content}
            </blockquote>'''
        return f'<blockquote class="callout">\n{content}\n</blockquote>'

    html_body = re.sub(r'<blockquote>([\s\S]*?)</blockquote>', tag_blockquotes, html_body)

    # Madde başlıklarını vurgula
    html_body = re.sub(r'<li>\s*•\s*<strong>', r'<li><strong class="item-title">', html_body)

    # Renk türevleri
    c_dark = darken_color(theme_hex, 0.72)
    c_light = lighten_color(theme_hex, 0.88)
    c_tint = lighten_color(theme_hex, 0.94)
    c_badge_grad = darken_color(theme_hex, 0.85)

    title_display = course_name or md_path.stem.replace(" - Vize Sınavı Konu Özeti (Sarf-Nahiv ve Alıştırmasız)", "")

    full_html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_display} — Okuma PDF</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 18mm 14mm 18mm 14mm;
        }}

        * {{
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            font-size: 9.8pt;
            line-height: 1.58;
            color: #1e293b;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
        }}

        .ar, [dir="rtl"], bdi.ar {{
            font-family: 'Amiri', 'Traditional Arabic', 'Arabic Typesetting', 'Segoe UI', serif;
            font-size: 1.28em;
            line-height: 1.70;
            direction: rtl;
            unicode-bidi: isolate;
        }}

        code {{
            font-family: Consolas, "Courier New", monospace;
            font-size: 8.8pt;
            background-color: #f1f5f9;
            color: #0f172a;
            padding: 1.5px 4.5px;
            border-radius: 4px;
            border: 1px solid #e2e8f0;
        }}

        code.ar {{
            font-family: 'Amiri', 'Traditional Arabic', serif;
            font-size: 1.16em;
            font-weight: 700;
            color: {theme_hex};
            background-color: {c_tint};
            border: 1px solid {c_light};
            padding: 0 5px;
            border-radius: 4px;
            display: inline-block;
            vertical-align: middle;
            line-height: 1.35;
            direction: rtl;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
        }}

        .ar-quote {{
            unicode-bidi: isolate;
        }}

        .ar-quote bdi.ar {{
            font-family: 'Amiri', 'Traditional Arabic', serif;
            font-size: 1.28em;
            font-weight: 700;
            line-height: 1.68;
            margin: 0 3px;
            color: {c_dark};
        }}

        /* ÜNİTE BANNER'LARI */
        .unit-banner-container {{
            break-before: page;
            page-break-before: always;
            margin-top: 0;
            margin-bottom: 22px;
        }}

        .unit-banner-container.first-unit {{
            break-before: avoid;
            page-break-before: avoid;
            margin-top: 0;
        }}

        .unit-banner-inner {{
            background: linear-gradient(135deg, {theme_hex} 0%, {c_dark} 100%);
            color: #ffffff;
            padding: 14px 20px;
            border-radius: 8px;
            border-left: 6px solid #d97706;
            border-bottom: 2px solid {darken_color(theme_hex, 0.5)};
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .unit-icon {{
            font-size: 18pt;
            display: inline-block;
            line-height: 1;
        }}

        .unit-title {{
            font-size: 13.5pt;
            font-weight: 800;
            margin: 0;
            color: #ffffff;
            letter-spacing: -0.2px;
            line-height: 1.3;
        }}

        /* BAŞLIKLAR */
        h2 {{
            font-size: 11.8pt;
            font-weight: 700;
            color: {theme_hex};
            margin-top: 24px;
            margin-bottom: 12px;
            padding-bottom: 5px;
            border-bottom: 2px solid {c_light};
            break-after: avoid;
            page-break-after: avoid;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
        }}

        .h2-badge {{
            background: linear-gradient(135deg, {theme_hex} 0%, {c_badge_grad} 100%);
            color: #ffffff;
            font-size: 8.5pt;
            font-weight: 800;
            letter-spacing: 0.5px;
            padding: 2.5px 8px;
            border-radius: 4px;
            margin-right: 8px;
            display: inline-block;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
        }}

        h3.h3-styled {{
            font-size: 10.5pt;
            font-weight: 700;
            color: #1e293b;
            margin-top: 18px;
            margin-bottom: 8px;
            break-after: avoid;
            page-break-after: avoid;
        }}

        .h3-diamond {{
            color: #d97706;
            font-size: 8.5pt;
            margin-right: 4px;
            vertical-align: middle;
        }}

        p {{
            margin-top: 0;
            margin-bottom: 10px;
        }}

        strong {{
            color: #0f172a;
        }}

        strong.item-title {{
            color: {theme_hex};
        }}

        /* TABLOLAR */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0 22px 0;
            font-size: 8.85pt;
            line-height: 1.48;
            break-inside: avoid;
            page-break-inside: avoid;
            border-radius: 7px;
            overflow: hidden;
            border: 1.5px solid #cbd5e1;
            box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        }}

        th {{
            background: linear-gradient(135deg, {theme_hex} 0%, {c_dark} 100%);
            color: #ffffff;
            font-weight: 700;
            text-align: left;
            padding: 8.5px 11px;
            border: 1px solid {c_dark};
            border-bottom: 2.5px solid #c49a45;
            font-size: 9.0pt;
            letter-spacing: 0.25px;
        }}

        th[align="center"], td[align="center"] {{
            text-align: center;
        }}

        td {{
            padding: 7.5px 11px;
            border: 1px solid #e2e8f0;
            vertical-align: top;
        }}

        tr:nth-child(even) {{
            background-color: #fbf8f7;
        }}

        tr:hover {{
            background-color: #f8eeeb;
        }}

        /* CALLOUT KUTULARI */
        blockquote.callout {{
            margin: 14px 0;
            padding: 12px 16px;
            border-radius: 0 8px 8px 0;
            background-color: #f8fafc;
            border-left: 4.5px solid #64748b;
            font-size: 9.6pt;
            line-height: 1.58;
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        blockquote.callout-nass {{
            background-color: #fcf8f7;
            border-left: 4.5px solid {theme_hex};
            border-top: 1px solid {c_light};
            border-right: 1px solid {c_light};
            border-bottom: 1px solid {c_light};
            border-radius: 0 8px 8px 0;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
            padding: 12px 18px;
        }}

        blockquote.callout-nass p {{
            margin-bottom: 6px;
        }}

        blockquote.callout-nass p:last-child {{
            margin-bottom: 0;
        }}

        blockquote.callout-pinned {{
            background-color: #fffdf5;
            border-left: 4.5px solid #d97706;
            border-top: 1px solid #fed7aa;
            border-right: 1px solid #fed7aa;
            border-bottom: 1px solid #fed7aa;
            border-radius: 0 8px 8px 0;
            box-shadow: 0 2px 8px rgba(217, 119, 6, 0.07);
            padding: 12px 18px;
        }}

        .pinned-header {{
            margin-bottom: 8px;
        }}

        .pinned-tag {{
            background-color: #fef3c7;
            color: #92400e;
            font-size: 7.8pt;
            font-weight: 800;
            letter-spacing: 0.6px;
            padding: 2.5px 8px;
            border-radius: 4px;
            border: 1px solid #fde68a;
            display: inline-block;
        }}

        blockquote.callout-pinned strong {{
            color: #9a3412;
        }}

        /* LİSTELER */
        ul {{
            margin-top: 4px;
            margin-bottom: 12px;
            padding-left: 18px;
            list-style: none;
        }}

        ul li {{
            margin-bottom: 5.5px;
            line-height: 1.54;
            position: relative;
        }}

        ul li::before {{
            content: "▪";
            color: {theme_hex};
            font-size: 1.15em;
            display: inline-block;
            width: 14px;
            margin-left: -14px;
            vertical-align: baseline;
        }}

        ol {{
            margin-top: 4px;
            margin-bottom: 12px;
            padding-left: 20px;
        }}

        ol li {{
            margin-bottom: 5px;
            line-height: 1.54;
        }}

        hr {{
            border: 0;
            height: 1px;
            background: linear-gradient(90deg, #f1f5f9 0%, #cbd5e1 50%, #f1f5f9 100%);
            margin: 18px 0;
        }}
    </style>
</head>
<body>

{html_body}

</body>
</html>
"""

    # HTML'i geçici/hedef konuma yaz
    html_out = md_path.with_suffix(".html")
    html_out.write_text(full_html, encoding="utf-8")

    if not output_pdf_path:
        output_pdf_path = md_path.with_suffix(".pdf")

    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Playwright Chromium ile Okuma PDF üretiliyor: {output_pdf_path.name}")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file:///{str(html_out.resolve()).replace('\\\\', '/')}", wait_until="load")
        
        page.pdf(
            path=str(output_pdf_path),
            format="A4",
            print_background=True,
            margin={
                "top": "18mm",
                "bottom": "18mm",
                "left": "14mm",
                "right": "14mm"
            },
            display_header_footer=True,
            header_template=f"""
                <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 8.0pt; color: #64748b; width: 100%; border-bottom: 1px solid #ebd3cd; padding-bottom: 4px; margin: 0 14mm; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; color: {theme_hex};">{title_display} — Okuma PDF</span>
                    <span style="font-weight: 500; color: #475569;">Eksiksiz Konu Akışı</span>
                </div>
            """,
            footer_template="""
                <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 8.0pt; color: #64748b; width: 100%; border-top: 1px solid #e2e8f0; padding-top: 4px; margin: 0 14mm; display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #64748b;">Görsel Ders Notu Tipografi Standardı</span>
                    <span style="background-color: #f1f5f9; border: 1px solid #cbd5e1; color: #0f172a; padding: 1.5px 8px; border-radius: 12px; font-weight: 700;">Sayfa <span class="pageNumber"></span> / <span class="totalPages"></span></span>
                </div>
            """
        )
        browser.close()

    # Sayfa sayısını ve boyutunu doğrula
    doc = pymupdf.open(output_pdf_path)
    page_count = len(doc)
    doc.close()
    print(f"✓ Başarıyla üretildi: {output_pdf_path} ({page_count} sayfa, {output_pdf_path.stat().st_size:,} bayt)")

    # Eğer kaynaklar/özetlenmiş_dersler altında karşılığı varsa oraya da kopyala
    mirror_target = None
    if "ders_anlatimlari" in md_path.parts:
        parts = list(md_path.parts)
        idx = parts.index("ders_anlatimlari")
        # yerine kaynaklar/özetlenmiş_dersler
        mirror_parts = parts[:idx] + ["kaynaklar", "özetlenmiş_dersler"] + parts[idx+1:]
        mirror_target = Path(*mirror_parts).with_suffix(".pdf")
        mirror_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(output_pdf_path, mirror_target)
        print(f"✓ Yedek kopya senkronize edildi: {mirror_target}")

    return output_pdf_path

def main():
    parser = argparse.ArgumentParser(description="Okuma PDF Üretim Motoru")
    parser.add_argument("hedef", help="Markdown dosya yolu veya ders adı / slug")
    parser.add_argument("--sinif", default="3", help="Sınıf (2, 3)")
    parser.add_argument("--donem", default="1", help="Dönem (1, 2)")
    parser.add_argument("--sinav", default="vize", help="Sınav (vize, final)")
    parser.add_argument("--renk", default=None, help="Özel tema rengi hex (örn: #8C2F21)")
    args = parser.parse_args()

    hedef_path = Path(args.hedef)
    if not hedef_path.exists():
        # Belki dönem klasöründedir
        klasor = donem_mod.aktif_donem_klasoru(args.sinif, args.donem, args.sinav)
        # Önce ders_anlatimlari içinde ara
        matches = list((klasor / "ders_anlatimlari").glob(f"**/*{args.hedef}*.md"))
        if not matches:
            matches = list((klasor / "kaynaklar" / "özetlenmiş_dersler").glob(f"**/*{args.hedef}*.md"))
        if matches:
            hedef_path = matches[0]
        else:
            print(f"Hata: '{args.hedef}' dosyası bulunamadı.")
            sys.exit(1)

    course_folder = hedef_path.parent.name
    theme_hex = args.renk or ders_rengi(course_folder, args.sinif, args.donem, args.sinav)

    print(f"Ders: {course_folder}")
    print(f"Girdi: {hedef_path}")
    print(f"Tema Rengi: {theme_hex}")

    generate_okuma_pdf(hedef_path, course_name=course_folder, theme_hex=theme_hex)

if __name__ == "__main__":
    main()
