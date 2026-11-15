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
tools/okuma_pdf.py — OKUMA PDF ÜRETİM MOTORU (KRİTİK KURAL 15)
=============================================================
Yazılı ders özetlerini (.md) görsel ders notu tipografik standartlarıyla
(kurumsal renkli ünite banner'ları, hiyerarşik h2 rozetleri, BiDi izoleli iri
Arapça metinler, nass levhaları, kehribar sınav uyarı kutuları, zebra desenli tablolar
ve şık sayfa altlıkları) yüksek prestijli bir "Okuma PDF" dokümanına dönüştürür.
Referans Model: Arap Dili ve Edebiyatı V - Vize Sınavı Konu Özeti (Sarf-Nahiv ve Alıştırmasız).pdf

Kullanım:
    python tools/okuma_pdf.py <dosya_veya_ders_adi> [--sinif X] [--donem Y] [--sinav Z]
"""

import os
import re
import sys
import shutil
import tempfile
import argparse
import colorsys
from pathlib import Path
import markdown
from playwright.sync_api import sync_playwright
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cekirdek import donem as donem_mod
from cekirdek.renk_uretici import ders_rengi
from tools.okuma_birlestir import (
    _darken as _cover_darken,
    _hsl_tint as _cover_hsl_tint,
    _extract_units as _extract_pdf_units,
    _render_footers_overlay_html,
    _redact_old_footer,
    attach_course_cover_links,
    render_single_course_cover_html,
    resolve_course_meta,
)

sys.stdout.reconfigure(encoding='utf-8')

# Regex ve Semboller
ARABIC_RE = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')

UNIT_ICONS = {
    "1": "📚",
    "2": "⚔️",
    "3": "📜",
    "4": "💡",
    "5": "🕊️",
    "6": "⚖️",
    "7": "🏛️",
    "8": "🔍",
    "9": "📖",
    "10": "✨"
}

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def darken_color(hex_code, factor=0.72):
    r, g, b = hex_to_rgb(hex_code)
    return f"#{int(r*factor):02x}{int(g*factor):02x}{int(b*factor):02x}"

def lighten_color(hex_code, factor=0.15):
    r, g, b = hex_to_rgb(hex_code)
    nr = int(r + (255 - r) * factor)
    ng = int(g + (255 - g) * factor)
    nb = int(b + (255 - b) * factor)
    return f"#{nr:02x}{ng:02x}{nb:02x}"

def theme_hsl_tint(hex_code, lightness=0.965, min_saturation=0.50, sat_factor=0.9):
    """Dersin tema renginden zengin, pastel ve ferah bir ton türetir (griye kaçmaz, temanın rengini korur)."""
    r, g, b = [x / 255.0 for x in hex_to_rgb(hex_code)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    target_s = min(1.0, max(s * sat_factor, min_saturation))
    tr, tg, tb = colorsys.hls_to_rgb(h, lightness, target_s)
    return f"#{int(tr*255+0.5):02x}{int(tg*255+0.5):02x}{int(tb*255+0.5):02x}"

def _infer_donem_from_path(md_path: Path, sinif: str | None, donem: str | None, sinav: str | None) -> tuple[str, str, str]:
    """Dosya yolundan (sinif, donem, sinav) bilgisini çıkarır."""
    s_val, d_val, sv_val = sinif, donem, sinav
    for part in md_path.parts:
        low = part.lower()
        if not s_val:
            m = re.match(r'^(\d+)-sinif$', low)
            if m:
                s_val = m.group(1)
        if not d_val:
            m = re.match(r'^(\d+)-donem$', low)
            if m:
                d_val = m.group(1)
        if not sv_val and low in {'vize', 'final'}:
            sv_val = low
    return s_val or "3", d_val or "1", sv_val or "vize"


def generate_okuma_pdf(
    md_path: Path,
    output_pdf_path: Path = None,
    course_name: str = "",
    theme_hex: str = "#8C2F21",
    son_unite: int = None,
    haric_unite: int = None,
    sinif: str = None,
    donem: str = None,
    sinav: str = None,
    with_cover: bool = True,
):
    """Tek bir Markdown özet dosyasından yüksek estetikli (Baskı Dostu Lüks kapaklı) Okuma PDF üretir."""
    if not md_path.exists():
        raise FileNotFoundError(f"Markdown dosyası bulunamadı: {md_path}")

    raw_text = md_path.read_text(encoding="utf-8")

    # Ünite başlangıç noktasını tespit et (Kural 15: Ön kapak, künye, içindekiler atlanır; doğrudan 1. Ünite başlar)
    u1_match = re.search(r'^#\s+(?:1\.\s*(?:ÜNİTE|BÖLÜM|HAFTA)|(?:ÜNİTE|BÖLÜM|HAFTA)\s*1\b)', raw_text, flags=re.MULTILINE | re.IGNORECASE)
    start_idx = u1_match.start() if u1_match else 0

    # Sınav kontrol tablosu veya ekstra kısımlar varsa bitiş noktasını tespit et
    end_match = re.search(r'^#\s+(?:\d+\.\s*)?SINAV\s+KONTROL', raw_text, flags=re.MULTILINE | re.IGNORECASE)
    end_idx = end_match.start() if end_match else len(raw_text)

    # Hariç tutulacak veya son ünite sınırı varsa bitiş noktasını ayarla
    if haric_unite is not None:
        u_exclude_match = re.search(
            rf'^#\s+(?:{haric_unite}\.\s*(?:ÜNİTE|BÖLÜM|HAFTA)|(?:ÜNİTE|BÖLÜM|HAFTA)\s*{haric_unite}\b)',
            raw_text,
            flags=re.MULTILINE | re.IGNORECASE
        )
        if u_exclude_match and u_exclude_match.start() < end_idx:
            end_idx = u_exclude_match.start()
    elif son_unite is not None:
        next_unit = son_unite + 1
        u_next_match = re.search(
            rf'^#\s+(?:{next_unit}\.\s*(?:ÜNİTE|BÖLÜM|HAFTA)|(?:ÜNİTE|BÖLÜM|HAFTA)\s*{next_unit}\b)',
            raw_text,
            flags=re.MULTILINE | re.IGNORECASE
        )
        if u_next_match and u_next_match.start() < end_idx:
            end_idx = u_next_match.start()

    pure_md = raw_text[start_idx:end_idx].strip()
    pure_md = re.sub(r'---+\s*$', '', pure_md).strip()

    # LaTeX ok ve sembollerini temiz Unicode karşılıklarına çevir (Kullanıcı talebi: $\rightarrow$ temizliği)
    pure_md = re.sub(r'\$\\rightarrow\$', '→', pure_md)
    pure_md = re.sub(r'\$\\to\$', '→', pure_md)
    pure_md = re.sub(r'\\rightarrow', '→', pure_md)
    pure_md = re.sub(r'\$\\leftrightarrow\$', '↔', pure_md)
    pure_md = re.sub(r'\\leftrightarrow', '↔', pure_md)
    pure_md = re.sub(r'\$10\^\{?(\d+)\}?\$', r'10<sup>\1</sup>', pure_md)

    # ==kavram== etiketlerini lüks ders renkli .badge-tr hap kutucuğuna dönüştür
    pure_md = re.sub(r'==([^=\n]+)==', r'<span class="badge-tr">\1</span>', pure_md)

    # H2 ve H3 alt başlıklarını evrensel rozetli hale getir (## 1.1. veya ### 1.1. veya ## A) -> ## <span class="h2-badge">...</span> Başlık)
    def format_subheading(match):
        prefix = match.group(1).rstrip('.').strip()
        title = match.group(2).strip()
        # Eğer başlık zaten bir badge içeriyorsa dokunma
        if '<span class=' in title or 'h2-badge' in title:
            return match.group(0)
        # Ünite veya bölüm başlığı ise H1 olarak korunmalıdır
        if re.search(r'(?:ÜNİTE|BÖLÜM|HAFTA)\b', title, re.IGNORECASE):
            return match.group(0)
        return f'## <span class="h2-badge">{prefix}</span> {title}'

    pure_md = re.sub(
        r'^(?:##|###)\s+(\d+(?:\.\d+)*\.?|[A-Z][\).]|(?:[IVXLCDM]+)[\).])\s+(.+)$',
        format_subheading,
        pure_md,
        flags=re.MULTILINE
    )

    # Alt liste maddelerinin (2-3 boşluk) Python-Markdown için 4 boşluk standardına normalize edilmesi
    pure_md = re.sub(r'^(\s{2,3})([*+-]|\d+\.)', r'    \2', pure_md, flags=re.MULTILINE)

    # Madde listelerinden hemen önce boşluk yoksa otomatik boşluk ekle (alt listelere dokunmaz)
    pure_md = re.sub(r'([^\n])\n([-*]\s)', r'\1\n\n\2', pure_md)
    pure_md = re.sub(r'([^\n])\n(\d+\.\s)', r'\1\n\n\2', pure_md)

    # Markdown -> HTML
    html_body = markdown.markdown(pure_md, extensions=['tables', 'fenced_code', 'sane_lists'])

    # Kod bloklarını (Arapça Nass Levhası vs Monospace Şema/Diyagram Kutusu) biçimlendir
    def format_code_blocks(match):
        code_attr = match.group(1) or ""
        code_content = match.group(2).strip()
        if "arabic" in code_attr.lower() or ARABIC_RE.search(code_content):
            return f'''<div class="nass-board" dir="rtl">
                <div class="nass-board-inner">
                    <p class="nass-arabic-text"><bdi>{code_content}</bdi></p>
                </div>
            </div>'''
        else:
            return f'''<div class="diagram-box">
                <pre><code>{code_content}</code></pre>
            </div>'''

    html_body = re.sub(r'<pre><code(?:\s+class="([^"]*)")?>([\s\S]*?)</code></pre>', format_code_blocks, html_body)

    # Ünite başlıklarını (H1) banner levhalarına dönüştür
    def replace_h1(match):
        content = match.group(1).strip()
        is_first = bool(re.search(r'(?:1\.\s*(?:ÜNİTE|BÖLÜM|HAFTA)|(?:ÜNİTE|BÖLÜM|HAFTA)\s*1\b)', content, re.IGNORECASE))
        cls = "unit-banner-container first-unit" if is_first else "unit-banner-container"
        
        # Ünite numarasına göre ikon seçimi
        icon = "📖"
        m_num = re.search(r'(?:(\d+)\.\s*(?:ÜNİTE|BÖLÜM|HAFTA)|(?:ÜNİTE|BÖLÜM|HAFTA)\s*(\d+))', content, re.IGNORECASE)
        if m_num:
            num = m_num.group(1) or m_num.group(2)
            icon = UNIT_ICONS.get(num, "📖")
        elif "EK BÖLÜM" in content or "EK" in content:
            icon = "📊"
        elif "GİRİŞ" in content:
            icon = "📚"
        elif "SORU" in content or "SINAV" in content:
            icon = "📝"
        elif "İNKÂR" in content or "FELSEFE" in content:
            icon = "🛡️"

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
        return f'<h3 class="h3-styled"><span class="h3-diamond">◆</span> <span class="h3-content">{content}</span></h3>'

    html_body = re.sub(r'<h3>([\s\S]*?)</h3>', replace_h3, html_body)

    # Ünite öncesi <hr> temizliği
    html_body = re.sub(r'<hr\s*/?>\s*(<div class="unit-banner-container)', r'\1', html_body)

    # Manuel sayfa sonu imi desteği (<!-- pagebreak -->)
    html_body = re.sub(r'<!--\s*pagebreak\s*-->', '<div style="break-before: page; page-break-before: always;"></div>', html_body, flags=re.IGNORECASE)

    # Callout / Alıntı kutuları (📌 Sınav & Dipnot vs Arapça Nass)
    def tag_blockquotes(match):
        content = match.group(1)
        alert_match = re.search(r'\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]', content)
        is_warn = any(kw in content for kw in ['Önemli Hatırlatma', 'Hayati Kelâmî Kaide', 'Püf Noktası', 'Altın Kural', 'Sınav Uyarısı', 'Ders İçi İkaz'])
        if '📌' in content or alert_match or is_warn:
            alert_type = alert_match.group(1) if alert_match else ""
            clean_content = re.sub(r'<p>\s*\[!(?:NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*', '<p>', content)
            clean_content = clean_content.replace('📌', '').strip()
            if any(kw in content for kw in ['Önemli Hatırlatma', 'Ders İçi İkaz', 'Sınav Uyarısı']):
                tag_title = "📌 DERS İÇİ İKAZ &amp; SINAV UYARISI"
            elif any(kw in content for kw in ['Hayati Kelâmî Kaide', 'Altın Kural']):
                tag_title = "⭐ HAYATİ KELÂMÎ KAİDE &amp; İLKE"
            elif 'Püf Noktası' in content:
                tag_title = "🎯 KELÂMÎ PÜF NOKTASI"
            elif alert_type in ("NOTE", "TIP"):
                tag_title = "📌 AKADEMİK DEĞERLENDİRME &amp; SINAV NOTU"
            else:
                tag_title = "📌 KİTAP DİPNOTU &amp; SINAV UYARISI"
            return f'''<blockquote class="callout callout-pinned">
                <div class="pinned-header"><span class="pinned-tag">{tag_title}</span></div>
                {clean_content}
            </blockquote>'''
        elif '«' in content or ARABIC_RE.search(content):
            def wrap_nass_quote(m):
                q = m.group(1).strip()
                return f'<div class="nass-ar" dir="rtl"><bdi>« {q} »</bdi></div>'
            clean_content = re.sub(r'<p>\s*(?:<strong>\s*)?«\s*([^»]+?)\s*»(?:\s*</strong>)?\s*</p>', wrap_nass_quote, content)
            return f'''<blockquote class="callout callout-nass">
                {clean_content}
            </blockquote>'''
        return f'<blockquote class="callout">\n{content}\n</blockquote>'

    html_body = re.sub(r'<blockquote>([\s\S]*?)</blockquote>', tag_blockquotes, html_body)

    # Inline Arapça kod blokları (`terim`)
    def tag_arabic_code(match):
        code_text = match.group(1)
        if ARABIC_RE.search(code_text):
            return f'<code class="ar" dir="rtl"><bdi>{code_text}</bdi></code>&lrm;'
        return f'<code>{code_text}</code>'

    html_body = re.sub(r'<code>([^<]+)</code>', tag_arabic_code, html_body)

    # Var olan <bdi class="ar"> etiketleri (BiDi izoleli ve LTR korumalı)
    def tag_existing_bdi(match):
        full_match = match.group(0)
        content = match.group(1).strip()
        words = content.split()
        if len(words) <= 4 and not any(w in content for w in ['حَدَّثَنَا', 'أَخْبَرَنَا', 'أَنْبَأَنَا']):
            clean = content.replace('«', '').replace('»', '').strip()
            return f'<code class="ar" dir="rtl"><bdi>{clean}</bdi></code>&lrm;'
        return f'{full_match}&lrm;'

    html_body = re.sub(r'<bdi class="ar"[^>]*>([\s\S]*?)</bdi>', tag_existing_bdi, html_body)

    # Çift tırnaklı Arapça ibareler « ... » (BiDi izoleli ve LTR korumalı)
    def tag_arabic_quotes(match):
        inside = match.group(1).strip()
        if ARABIC_RE.search(inside):
            clean = re.sub(r'</?bdi[^>]*>', '', inside).replace('«', '').replace('»', '').strip()
            words = clean.split()
            if len(words) <= 4 and not any(w in clean for w in ['حَدَّثَنَا', 'أَخْبَرَنَا', 'أَنْبَأَنَا']):
                return f'<code class="ar" dir="rtl"><bdi>{clean}</bdi></code>&lrm;'
            return f'<span class="ar-quote">«<bdi class="ar" dir="rtl">{clean}</bdi>»</span>&lrm;'
        return f'«{inside}»'

    html_body = re.sub(r'«([^»\n]+)»', tag_arabic_quotes, html_body)

    # Müstakil Not paragraflarını zengin callout kutusuna çevir
    def replace_standalone_notes(match):
        note_body = match.group(1).strip()
        return f'''<div class="callout callout-pinned" style="margin: 10px 0;">
            <div class="pinned-header"><span class="pinned-tag">📌 KİTAP DİPNOTU &amp; SINAV UYARISI</span></div>
            <p style="margin: 0;">{note_body}</p>
        </div>'''

    html_body = re.sub(r'<p><em>\((?:Not|Önemli Not):\s*([\s\S]*?)\)</em></p>', replace_standalone_notes, html_body)

    # Madde başlıklarını vurgula
    def repl_item_title(m):
        prefix = m.group(1) or ""
        return f'<li>{prefix}<strong class="item-title">'

    html_body = re.sub(r'<li>\s*(<p>\s*)?(?:[•▪]\s*)?<strong>', repl_item_title, html_body)

    # Sened Rozetleri (Medâr Râvi, Mütâbaat, Tahvîl, Usûl Notu)
    html_body = re.sub(r'<strong>(?:★\s*)?MEDÂR RÂVİ[^:]*:</strong>\s*([^<\n]+)',
                       r'<span class="badge-medar">★ MEDÂR RÂVİ</span> <strong>\1</strong>', html_body)
    html_body = re.sub(r'<strong>(?:⮑\s*)?MÜTÂBAAT[^:]*:</strong>\s*([^<\n]+)',
                       r'<span class="badge-mutabaat">⮑ MÜTÂBAAT</span> <strong>\1</strong>', html_body)
    html_body = re.sub(r'<strong>(?:«ح»\s*)?TAHVÎL(?:-İ İSNÂD)?[^:]*:</strong>\s*([^<\n]+)',
                       r'<span class="badge-tahvil">«ح» TAHVÎL</span> <strong>\1</strong>', html_body)
    html_body = re.sub(r'<li>\s*<strong>(?:⚖️\s*)?Sened Sıhhati[^:]*:</strong>\s*([\s\S]*?)</li>',
                       r'<li class="isnad-note-li"><div class="isnad-note">⚖️ <strong>Sened Sıhhati &amp; Usûl Notu:</strong> \1</div></li>', html_body)

    # Sınav Püf Noktası ve Hoca Notu Rozetleri
    html_body = re.sub(r'<strong>(?:🎯\s*)?Sınav Püf Noktası:</strong>',
                       r'<span class="badge-sinav">🎯 SINAV PÜF NOKTASI</span>', html_body)
    html_body = re.sub(r'<strong>(?:📌\s*)?Hoca(?:nın)? Sınav Notu:</strong>',
                       r'<span class="badge-sinav">📌 HOCA SINAV NOTU</span>', html_body)
    html_body = re.sub(r'<strong>(?:⚠️\s*)?Sınav İkaz(?:ı|ları)?:</strong>',
                       r'<span class="badge-sinav">⚠️ SINAV İKAZI</span>', html_body)
    html_body = re.sub(r'<strong>(?:💡\s*)?Hoca Notu:</strong>',
                       r'<span class="badge-hoca">💡 HOCA NOTU</span>', html_body)

    # Hadis bölümlerini (H3 + UL) bölünmez bütün bloklar haline getir
    html_body = re.sub(
        r'(<h3 class="h3-styled"><span class="h3-diamond">◆</span>\s*(?:<span class="h3-content">\s*)?Hadis\s*\d+:[\s\S]*?</h3>\s*<ul>[\s\S]*?</ul>)',
        r'<div class="hadis-card">\1</div>',
        html_body
    )

    # Soru ve Cevap Modellerini (Klasik ve Çoktan Seçmeli) Kart Mimarisine Dönüştür
    def repl_classic(m):
        q_num = m.group(1)
        q_stem = m.group(2).strip()
        ans_body = m.group(3).strip()
        return f'''<div class="q-card q-card-classic">
            <div class="q-header"><span class="q-badge">{q_num}</span><span class="q-stem">{q_stem}</span></div>
            <div class="q-ans">{ans_body}</div>
        </div>'''

    html_body = re.sub(
        r'<p><strong>(S\d+)\.\s*(.+?)</strong>\s*</p>\s*<blockquote[^>]*>([\s\S]*?)</blockquote>',
        repl_classic,
        html_body
    )
    html_body = re.sub(r'<hr\s*/?>\s*(<div class="q-card)', r'\1', html_body)

    def repl_mc(m):
        q_num = m.group(1)
        q_stem = m.group(2).strip()
        raw_options = m.group(3).strip()
        ans_body = m.group(4).strip() if (m.lastindex and m.lastindex >= 4 and m.group(4)) else ""

        opt_lines = [opt.strip() for opt in re.split(r'<br\s*/?>', raw_options) if opt.strip()]
        context_lines = []
        option_lines = []
        is_option_phase = False
        for line in opt_lines:
            if re.match(r'^[A-E]\)', line):
                is_option_phase = True
            if is_option_phase:
                option_lines.append(line)
            else:
                context_lines.append(line)

        context_html = ""
        if context_lines:
            context_html = f'<div class="q-context">{"<br />".join(context_lines)}</div>'

        opts_html = []
        is_long = any(len(re.sub(r'<[^>]+>', '', opt)) > 48 for opt in option_lines)
        for line in option_lines:
            opt_match = re.match(r'^([A-E]\))\s*(.+)$', line)
            if opt_match:
                letter = opt_match.group(1)
                opt_text = opt_match.group(2).strip()
                is_correct = '✔' in opt_text
                clean_text = opt_text.replace('✔', '').strip()
                cls = 'q-opt opt-correct' if is_correct else 'q-opt'
                chk = '<span class="opt-check">✔</span>' if is_correct else ''
                opts_html.append(f'<div class="{cls}"><span class="opt-badge">{letter}</span><span class="opt-text">{clean_text}</span>{chk}</div>')
            else:
                opts_html.append(f'<div class="q-opt">{line}</div>')

        grid_cls = "q-options q-options-single" if is_long else "q-options"
        options_block = ''.join(opts_html)
        ans_html = f'<div class="q-ans">{ans_body}</div>' if ans_body else ""
        return f'''<div class="q-card q-card-mc">
            <div class="q-header"><span class="q-badge">{q_num}</span><span class="q-stem">{q_stem}</span></div>
            {context_html}
            <div class="{grid_cls}">{options_block}</div>
            {ans_html}
        </div>'''

    html_body = re.sub(
        r'<p><strong>(S\d+)\.\s*(.+?)</strong><br />([\s\S]*?)</p>(?:\s*<blockquote[^>]*>([\s\S]*?)</blockquote>)?',
        repl_mc,
        html_body
    )

    # Renk türevleri (Dersin tema renginden zengin, pastel ve BiDi uyumlu palet)
    c_dark = darken_color(theme_hex, 0.65)
    c_bg_tint = theme_hsl_tint(theme_hex, lightness=0.965, min_saturation=0.50)
    c_bg_end = theme_hsl_tint(theme_hex, lightness=0.985, min_saturation=0.35)
    c_border = theme_hsl_tint(theme_hex, lightness=0.82, min_saturation=0.40)
    c_pill_bg = theme_hsl_tint(theme_hex, lightness=0.945, min_saturation=0.55)
    c_pill_border = theme_hsl_tint(theme_hex, lightness=0.78, min_saturation=0.45)
    c_light = c_border
    c_tint = c_pill_bg
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
            margin: 24mm 14mm 22mm 14mm;
        }}

        * {{
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            font-size: 9.8pt;
            line-height: 1.56;
            color: #1e293b;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
        }}

        .ar, [dir="rtl"], bdi.ar {{
            font-family: 'Amiri', 'Traditional Arabic', 'Scheherazade New', 'Arabic Typesetting', serif;
            font-size: 1.25em;
            line-height: 1.5;
            direction: rtl;
            unicode-bidi: isolate;
            color: {c_dark};
        }}

        code.ar, span.ar-badge {{
            font-family: 'Amiri', 'Traditional Arabic', serif;
            font-size: 1.15em;
            font-weight: 700;
            direction: rtl;
            unicode-bidi: isolate;
            color: {c_dark};
            background: {c_pill_bg} !important;
            border: 1px solid {c_pill_border} !important;
            border-right: 3px solid {theme_hex} !important;
            border-radius: 4px !important;
            padding: 1px 6px 1.5px 6px !important;
            margin: 0 1.5px !important;
            display: inline-block !important;
            vertical-align: baseline !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
            line-height: 1.35 !important;
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

        .badge-tr, .tr-badge, code.tr {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 8.6pt;
            font-weight: 700;
            color: {c_dark};
            background: {c_pill_bg};
            border: 1px solid {c_pill_border};
            border-left: 3px solid {theme_hex};
            padding: 1px 6px;
            border-radius: 4px;
            display: inline-block;
            vertical-align: baseline;
            margin: 0 1.5px;
            line-height: 1.35;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
        }}

        .badge-sinav {{
            display: inline-block;
            background-color: #fef2f2;
            color: #991b1b;
            border: 1px solid #fecaca;
            padding: 1px 6.5px;
            border-radius: 4px;
            font-size: 7.6pt;
            font-weight: 800;
            margin-right: 5px;
            vertical-align: baseline;
            line-height: 1.35;
        }}

        .badge-hoca {{
            display: inline-block;
            background-color: #fffbeb;
            color: #b45309;
            border: 1px solid #fde68a;
            padding: 1px 6.5px;
            border-radius: 4px;
            font-size: 7.6pt;
            font-weight: 800;
            margin-right: 5px;
            vertical-align: baseline;
            line-height: 1.35;
        }}

        .ar-quote {{
            unicode-bidi: isolate;
            display: inline-block;
            padding: 1.5px 8px;
            background: {c_bg_tint};
            border-radius: 5px;
            border: 1px solid {c_border};
            border-right: 3px solid {theme_hex};
            margin: 2px 0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
        }}

        .nass-arabic-text .ar-quote, .nass-ar .ar-quote,
        .nass-arabic-text code.ar, .nass-ar code.ar {{
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            margin: 0 !important;
            box-shadow: none !important;
            display: inline !important;
            font-size: inherit !important;
            line-height: inherit !important;
            color: inherit !important;
        }}

        .ar-quote bdi.ar {{
            font-family: 'Amiri', 'Traditional Arabic', serif;
            font-size: 1.25em;
            font-weight: 700;
            line-height: 1.60;
            margin: 0 3px;
            color: {c_dark};
        }}

        .nass-arabic-text .ar-quote bdi.ar, .nass-ar .ar-quote bdi.ar {{
            font-size: inherit !important;
            line-height: inherit !important;
            margin: 0 !important;
            color: inherit !important;
        }}

        /* ÜNİTE BANNER'LARI (KURAL 15: İlk ünite 1. sayfada; sonrakiler yeni sayfada açılır) */
        .unit-banner-container {{
            break-before: page;
            page-break-before: always;
            margin-top: 0;
            margin-bottom: 16px;
        }}

        .unit-banner-container.first-unit {{
            break-before: avoid;
            page-break-before: avoid;
            margin-top: 0;
            margin-bottom: 10px;
        }}

        .unit-banner-inner {{
            background: {theme_hex};
            color: #ffffff;
            padding: 9.5px 16px;
            border-radius: 8px;
            border-left: 5px solid #d97706;
            border-bottom: 2px solid #c49a45;
            box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08);
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
            font-size: 13.2pt;
            font-weight: 800;
            margin: 0;
            color: #ffffff;
            letter-spacing: -0.2px;
            line-height: 1.25;
        }}

        /* BAŞLIKLAR (KURAL 15: H2 Rozetli ve Alt Çizgili; H3 Altın Elmas İmli) */
        h2 {{
            font-size: 11.5pt;
            font-weight: 700;
            color: {theme_hex};
            margin-top: 13px;
            margin-bottom: 5px;
            padding-bottom: 3.5px;
            border-bottom: 2px solid {c_light};
            break-after: avoid !important;
            page-break-after: avoid !important;
        }}

        .h2-badge {{
            background: {theme_hex};
            color: #ffffff;
            font-size: 8.5pt;
            font-weight: 800;
            letter-spacing: 0.5px;
            padding: 2.5px 8px;
            border-radius: 4px;
            margin-right: 8px;
            display: inline-block;
            vertical-align: middle;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
        }}

        h3.h3-styled {{
            font-size: 10.0pt;
            font-weight: 700;
            color: {c_dark};
            margin-top: 13px;
            margin-bottom: 6px;
            padding: 3.5px 10px;
            background: {c_bg_tint};
            border-left: 3.5px solid #d97706;
            border-radius: 0 4px 4px 0;
            display: flex;
            align-items: flex-start;
            gap: 6px;
            break-after: avoid !important;
            page-break-after: avoid !important;
        }}

        .h3-diamond {{
            color: #d97706;
            font-size: 8pt;
            display: inline-block;
            margin-top: 2.5px;
            flex-shrink: 0;
        }}

        .h3-content {{
            flex: 1;
            display: inline;
        }}

        h4 {{
            font-size: 10.0pt;
            font-weight: 700;
            color: {theme_hex};
            margin-top: 12px;
            margin-bottom: 4px;
            padding-left: 6px;
            border-left: 3px solid {theme_hex};
            break-after: avoid !important;
            page-break-after: avoid !important;
        }}

        h4 strong {{
            color: {theme_hex};
        }}

        p {{
            margin-top: 0;
            margin-bottom: 5.5px;
            orphans: 3;
            widows: 3;
        }}

        strong {{
            color: #0f172a;
        }}

        strong.item-title {{
            color: {theme_hex};
            font-size: 1.02em;
            display: inline-block;
            margin-bottom: 2px;
        }}

        /* TABLOLAR (KURAL 15: Zebra desenli, altın çizgili kurumsal başlık) */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 8px 0 12px 0;
            font-size: 8.85pt;
            line-height: 1.42;
            break-inside: auto;
            page-break-inside: auto;
            border-radius: 7px;
            overflow: hidden;
            border: 1.5px solid {c_border};
            box-shadow: 0 2px 6px rgba(0,0,0,0.04);
            word-break: normal;
            overflow-wrap: break-word;
        }}

        thead {{
            display: table-header-group;
        }}

        tr {{
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        th {{
            background: {theme_hex};
            color: #ffffff;
            font-weight: 700;
            text-align: left;
            padding: 6px 9px;
            border: 1px solid {c_dark};
            border-bottom: 2.5px solid #c49a45;
            font-size: 8.9pt;
            letter-spacing: 0.25px;
        }}

        th[align="center"], td[align="center"] {{
            text-align: center;
        }}

        td {{
            padding: 5px 9px;
            border: 1px solid #e2e8f0;
            vertical-align: top;
        }}

        td:first-child strong {{
            color: {theme_hex};
            font-weight: 700;
        }}

        tr:nth-child(even) {{
            background-color: {c_bg_end};
        }}

        tr:hover {{
            background-color: {c_bg_tint};
        }}

        /* CALLOUT KUTULARI (KURAL 15: Nass levhaları ve kehribar sınav kutuları) */
        blockquote.callout {{
            margin: 10px 0;
            padding: 10px 16px;
            border-radius: 0 8px 8px 0;
            background-color: #f8fafc;
            border-left: 4.5px solid {theme_hex};
            border-top: 1px solid #e2e8f0;
            border-right: 1px solid #e2e8f0;
            border-bottom: 1px solid #e2e8f0;
            font-size: 9.6pt;
            line-height: 1.56;
            break-inside: avoid;
            page-break-inside: avoid;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02);
        }}

        blockquote.callout-nass {{
            background: {c_bg_tint};
            border-left: 4.5px solid {theme_hex};
            border-top: 1px solid {c_border};
            border-right: 1px solid {c_border};
            border-bottom: 1px solid {c_border};
            border-radius: 0 8px 8px 0;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
            padding: 10px 16px;
            margin: 8px 0;
            break-inside: avoid;
            page-break-inside: avoid;
            direction: ltr;
            text-align: left;
        }}

        blockquote.callout-nass p {{
            margin: 0 0 4px 0;
            line-height: 1.54;
            direction: ltr;
            text-align: left;
            color: #2b2b2b;
        }}

        blockquote.callout-nass p:last-child {{
            margin-bottom: 0;
        }}

        blockquote.callout-nass .nass-ar {{
            font-family: 'Amiri', 'Traditional Arabic', serif;
            font-size: 1.30em;
            line-height: 1.70;
            direction: rtl;
            unicode-bidi: isolate;
            color: {c_dark};
            text-align: center;
            display: block;
            margin-bottom: 5px;
            font-weight: 700;
        }}

        blockquote.callout-pinned {{
            background-color: #fffdf5;
            border-left: 4.5px solid #d97706;
            border-top: 1px solid #fed7aa;
            border-right: 1px solid #fed7aa;
            border-bottom: 1px solid #fed7aa;
            border-radius: 0 8px 8px 0;
            box-shadow: 0 2px 8px rgba(217, 119, 6, 0.07);
            padding: 8px 14px;
            margin: 7px 0;
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        .pinned-header {{
            margin-bottom: 6px;
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

        /* NASS LEVHALARI VE DİYAGRAM KUTULARI (TEFSİR III REFERANSLI) */
        .nass-board {{
            background: {c_bg_tint};
            border: 1px solid {c_border};
            border-left: 5px solid {theme_hex};
            border-radius: 7px;
            padding: 8px 14px;
            margin: 7px 0;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        .nass-board.gold-accent {{
            border-left-color: #d97706;
            background: #fffdf5;
            border-color: #fde68a;
        }}

        .nass-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 5px;
            padding-bottom: 3.5px;
            border-bottom: 1px solid {c_border};
        }}

        .nass-badge {{
            font-size: 7.2pt;
            font-weight: 800;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            color: #ffffff;
            background: {theme_hex};
            padding: 1.5px 6.5px;
            border-radius: 4px;
            display: inline-block;
        }}

        .nass-badge.gold {{
            background: #d97706;
        }}

        .nass-badge.subtle {{
            background: #475569;
        }}

        .nass-source {{
            font-size: 7.4pt;
            font-weight: 600;
            color: #64748b;
            font-style: italic;
        }}

        .nass-arabic-text {{
            font-family: 'Amiri', 'Traditional Arabic', serif;
            font-size: 1.26em;
            line-height: 1.55;
            color: {c_dark};
            margin: 3px 0;
            unicode-bidi: isolate;
            font-weight: 700;
            direction: rtl;
            text-align: center;
        }}

        .nass-divider {{
            height: 1px;
            background: {c_border};
            margin: 5px 0;
        }}

        .nass-trans-box {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 5px;
            padding: 6px 10px;
            margin-top: 4px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        }}

        .nass-trans-badge {{
            font-size: 7.2pt;
            font-weight: 800;
            letter-spacing: 0.5px;
            color: #92400e;
            background: #fef3c7;
            border: 1px solid #fde68a;
            padding: 1.5px 6px;
            border-radius: 3px;
            display: inline-block;
            margin-bottom: 4px;
        }}

        .nass-trans-text {{
            font-size: 9.3pt;
            line-height: 1.50;
            color: #334155;
            margin: 0;
        }}

        .nass-trans-text strong {{
            color: {c_dark};
        }}

        .nass-trans-text em {{
            color: #64748b;
            font-size: 8.7pt;
        }}

        /* Kök Fiil Kartı */
        .root-verb-card {{
            background: {c_bg_tint};
            border: 1px solid {c_border};
            border-left: 4.5px solid {theme_hex};
            border-radius: 8px;
            padding: 10px 16px;
            margin: 10px 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 15px;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
            break-inside: avoid;
        }}

        .root-ar-part {{
            font-family: 'Amiri', 'Traditional Arabic', serif;
            font-size: 1.42em;
            font-weight: 700;
            color: {c_dark};
            direction: rtl;
            unicode-bidi: isolate;
        }}

        .root-tr-part {{
            font-size: 8.9pt;
            color: #475569;
            text-align: right;
        }}

        /* Şema 1: Kelâm Usûl Akışı */
        .kelam-usul-flow {{
            margin: 12px 0;
            display: flex;
            flex-direction: column;
            gap: 3px;
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        .usul-step {{
            border-radius: 7px;
            padding: 9px 14px;
            border: 1px solid {c_border};
            border-left: 5px solid {theme_hex};
            background: {c_bg_tint};
            box-shadow: 0 1px 4px rgba(0,0,0,0.02);
        }}

        .usul-step.usul-mesail {{
            border-left-color: #d97706;
            background: #fffdf5;
            border-color: #fde68a;
        }}

        .usul-step-header {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 3.5px;
        }}

        .usul-badge {{
            font-size: 7.4pt;
            font-weight: 800;
            padding: 1.5px 6.5px;
            border-radius: 4px;
            background: {theme_hex};
            color: #ffffff;
            letter-spacing: 0.3px;
        }}

        .usul-badge.gold {{
            background: #d97706;
        }}

        .usul-title {{
            font-weight: 800;
            font-size: 9.7pt;
            color: {c_dark};
        }}

        .usul-center-tag {{
            font-size: 7.5pt;
            font-weight: 700;
            color: #475569;
            margin-left: auto;
            background: #f1f5f9;
            padding: 1.5px 7px;
            border-radius: 4px;
            border: 1px solid #e2e8f0;
        }}

        .usul-center-tag.gold {{
            background: #fef3c7;
            color: #92400e;
            border-color: #fde68a;
        }}

        .usul-desc {{
            font-size: 8.85pt;
            line-height: 1.44;
            color: #334155;
            margin: 0;
        }}

        .usul-arrow {{
            text-align: center;
            color: {theme_hex};
            font-size: 10pt;
            font-weight: 800;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            margin: 1.5px 0;
        }}

        .arrow-label {{
            font-size: 7.2pt;
            color: #64748b;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        /* Şema 2: Varlık Sahası Ontolojisi */
        .ontology-card-wrap {{
            margin: 12px 0;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid {c_border};
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        .ontology-main-banner {{
            background: {theme_hex};
            color: #ffffff;
            padding: 8px 14px;
            display: flex;
            align-items: center;
            gap: 10px;
            border-bottom: 2px solid #c49a45;
        }}

        .ont-icon {{
            font-size: 13pt;
        }}

        .ont-title {{
            font-size: 9.8pt;
            font-weight: 800;
            letter-spacing: 0.3px;
        }}

        .ont-sub {{
            font-size: 7.6pt;
            color: #f1f5f9;
            margin-left: auto;
            font-weight: 500;
        }}

        .ontology-branches {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1px;
            background: {c_border};
        }}

        .ont-branch {{
            background: #ffffff;
            padding: 10px 14px;
        }}

        .branch-header {{
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 3px;
        }}

        .branch-pill {{
            font-size: 7.2pt;
            font-weight: 800;
            padding: 1.5px 6px;
            border-radius: 4px;
            text-transform: uppercase;
        }}

        .branch-pill.gold {{
            background: #fef3c7;
            color: #92400e;
            border: 1px solid #fde68a;
        }}

        .branch-pill.purple {{
            background: {c_bg_tint};
            color: {theme_hex};
            border: 1px solid {c_border};
        }}

        .branch-name {{
            font-size: 9.2pt;
            font-weight: 800;
            color: {c_dark};
        }}

        .branch-target {{
            font-size: 8.2pt;
            font-weight: 700;
            color: #64748b;
            margin-bottom: 6px;
            padding-bottom: 4px;
            border-bottom: 1px solid #f1f5f9;
        }}

        .branch-list {{
            margin: 0;
            padding-left: 14px;
            list-style: none;
        }}

        .branch-list li {{
            font-size: 8.5pt;
            line-height: 1.40;
            color: #334155;
            margin-bottom: 3.5px;
            position: relative;
        }}

        .branch-list li::before {{
            content: "•";
            color: {theme_hex};
            font-size: 1.1em;
            position: absolute;
            left: -12px;
            top: -1px;
        }}

        /* Şema 3: Hâdis Varlıkların Üç Formu */
        .hadis-entities-wrap {{
            margin: 12px 0;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid {c_border};
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        .entities-banner {{
            background: {theme_hex};
            color: #ffffff;
            padding: 7.5px 14px;
            display: flex;
            align-items: center;
            gap: 9px;
            border-bottom: 2px solid #c49a45;
        }}

        .ent-icon {{
            font-size: 13pt;
        }}

        .ent-title {{
            font-size: 9.6pt;
            font-weight: 800;
            letter-spacing: 0.3px;
        }}

        .entities-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 1px;
            background: {c_border};
        }}

        .entity-card {{
            background: #ffffff;
            padding: 10px 12px;
            display: flex;
            flex-direction: column;
        }}

        .ent-card-header {{
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 3px;
        }}

        .ent-num {{
            width: 17px;
            height: 17px;
            background: {theme_hex};
            color: #ffffff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 7.5pt;
            font-weight: 800;
        }}

        .ent-name {{
            font-size: 9.3pt;
            font-weight: 800;
            color: {c_dark};
        }}

        .ent-ar {{
            font-family: 'Amiri', 'Traditional Arabic', serif;
            font-size: 1.15em;
            color: {theme_hex};
            margin-left: auto;
            font-weight: 700;
        }}

        .ent-tag {{
            font-size: 7.5pt;
            font-weight: 700;
            color: #64748b;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 1px 5px;
            border-radius: 3px;
            margin-bottom: 6px;
        }}

        .ent-text {{
            font-size: 8.4pt;
            line-height: 1.40;
            color: #334155;
            margin: 0;
        }}

        .ent-text em {{
            color: #991b1b;
            font-style: normal;
            font-weight: 600;
        }}

        /* Şema 4: Varlık Doktrini Mukayesesi */
        .doktrin-compare-wrap {{
            margin: 12px 0;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid {c_border};
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        .doktrin-banner {{
            background: {theme_hex};
            color: #ffffff;
            padding: 7.5px 14px;
            display: flex;
            align-items: center;
            gap: 9px;
            border-bottom: 2px solid #c49a45;
        }}

        .dok-icon {{
            font-size: 13pt;
        }}

        .dok-title {{
            font-size: 9.6pt;
            font-weight: 800;
            letter-spacing: 0.3px;
        }}

        .doktrin-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1px;
            background: {c_border};
        }}

        .dok-card {{
            background: #ffffff;
            padding: 11px 14px;
        }}

        .dok-card-header {{
            margin-bottom: 6px;
        }}

        .dok-pill {{
            font-size: 7.3pt;
            font-weight: 800;
            padding: 1.5px 7px;
            border-radius: 4px;
            display: inline-block;
            margin-bottom: 2px;
        }}

        .dok-pill.green {{
            background: #dcfce7;
            color: #166534;
            border: 1px solid #bbf7d0;
        }}

        .dok-pill.red {{
            background: #fee2e2;
            color: #991b1b;
            border: 1px solid #fecaca;
        }}

        .dok-sub {{
            display: block;
            font-size: 7.6pt;
            color: #64748b;
            font-weight: 600;
        }}

        .dok-principle {{
            font-family: 'Amiri', 'Traditional Arabic', serif;
            font-size: 1.25em;
            font-weight: 700;
            color: {c_dark};
            direction: rtl;
            margin: 4px 0 2px 0;
            text-align: center;
            unicode-bidi: isolate;
        }}

        .dok-meaning {{
            font-size: 8.5pt;
            font-weight: 700;
            color: #1e293b;
            text-align: center;
            margin-bottom: 7px;
            padding-bottom: 5px;
            border-bottom: 1px dashed #e2e8f0;
        }}

        .dok-points {{
            margin: 0;
            padding-left: 14px;
            list-style: none;
        }}

        .dok-points li {{
            font-size: 8.4pt;
            line-height: 1.40;
            color: #334155;
            margin-bottom: 4px;
            position: relative;
        }}

        .dok-points li::before {{
            content: "▪";
            color: {theme_hex};
            position: absolute;
            left: -12px;
        }}

        /* 0-100 Zihnî Kanaat Skalası Barem Göstergesi */
        .certainty-scale-bar {{
            margin: 10px 0 6px 0;
            border-radius: 6px;
            overflow: hidden;
            display: flex;
            height: 18px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            border: 1px solid #cbd5e1;
        }}

        .scale-segment {{
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 6.8pt;
            font-weight: 800;
            color: #ffffff;
            text-transform: uppercase;
            letter-spacing: 0.2px;
        }}

        .scale-segment.cehl {{ width: 10%; background: #64748b; }}
        .scale-segment.vehm {{ width: 25%; background: #ea580c; }}
        .scale-segment.sek  {{ width: 15%; background: #eab308; color: #713f12; }}
        .scale-segment.zan  {{ width: 25%; background: #0284c7; }}
        .scale-segment.zann-galib {{ width: 15%; background: #7c3aed; }}
        .scale-segment.yakin {{ width: 10%; background: #16a34a; }}

        /* Kelâm Formül ve Süreç Akış Kartları */
        .formula-card {{
            margin: 9px 0;
            padding: 9px 14px;
            background: {c_bg_tint};
            border: 1px solid {c_border};
            border-left: 4.5px solid {theme_hex};
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            font-size: 9.3pt;
            font-weight: 700;
            color: {c_dark};
            box-shadow: 0 1px 4px rgba(0,0,0,0.03);
            break-inside: avoid;
            page-break-inside: avoid;
            flex-wrap: wrap;
        }}

        .formula-flow {{
            margin: 6px 0;
            padding: 6px 10px;
            background: #ffffff;
            border: 1px solid {c_border};
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            break-inside: avoid;
            page-break-inside: avoid;
            flex-wrap: wrap;
        }}

        .flow-node {{
            padding: 4px 10px;
            border-radius: 5px;
            font-size: 8.4pt;
            font-weight: 700;
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            color: #334155;
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        .flow-node.origin {{
            background: {c_bg_tint};
            border-color: {c_border};
            color: {c_dark};
        }}

        .flow-node.stage {{
            background: #fef3c7;
            border-color: #fde68a;
            color: #92400e;
        }}

        .flow-node.target {{
            background: #dcfce7;
            border-color: #bbf7d0;
            color: #166534;
        }}

        .flow-arrow {{
            color: {theme_hex};
            font-size: 11pt;
            font-weight: 800;
        }}

        /* --- EVRENSEL PEDAGOJİK MATERYAL KÜTÜPHANESİ --- */

        /* 1. Hiyerarşik Değerler & Kademeler Piramidi (İbn Rüşd, Makāsıd, Müdahale) */
        .concept-pyramid {{
            margin: 8px auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 3px;
            width: 100%;
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        .pyramid-tier {{
            border-radius: 5px;
            padding: 5px 12px;
            text-align: center;
            border: 1px solid;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 7px;
            box-sizing: border-box;
        }}

        .pyramid-tier.top {{
            width: 52%;
            background: {theme_hex};
            color: #ffffff;
            border-color: {c_dark};
        }}

        .pyramid-tier.middle {{
            width: 74%;
            background: {c_bg_tint};
            color: {c_dark};
            border-color: {c_border};
            border-left: 4.5px solid #d97706;
        }}

        .pyramid-tier.base {{
            width: 96%;
            background: #ffffff;
            color: #334155;
            border-color: #cbd5e1;
            border-left: 4.5px solid {theme_hex};
        }}

        .pyr-badge {{
            font-size: 7.2pt;
            font-weight: 800;
            padding: 1.5px 6.5px;
            border-radius: 4px;
            text-transform: uppercase;
        }}

        .pyr-badge.gold {{ background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }}
        .pyr-badge.purple {{ background: {c_bg_tint}; color: {theme_hex}; border: 1px solid {c_border}; }}
        .pyr-badge.white {{ background: rgba(255,255,255,0.25); color: #ffffff; border: 1px solid rgba(255,255,255,0.4); }}

        .pyr-title {{
            font-size: 9.1pt;
            font-weight: 800;
        }}

        .pyr-desc {{
            font-size: 8.2pt;
            color: inherit;
            opacity: 0.92;
        }}

        /* 2. Döngüsel / Çevrimsel Süreç Modeli (İbn Haldun, İletişim, Çevrim) */
        .cycle-flow-wrap {{
            margin: 12px 0;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid {c_border};
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        .cycle-banner {{
            background: {theme_hex};
            color: #ffffff;
            padding: 7.5px 14px;
            display: flex;
            align-items: center;
            gap: 9px;
            border-bottom: 2px solid #c49a45;
            font-size: 9.6pt;
            font-weight: 800;
        }}

        .cycle-steps {{
            display: flex;
            flex-direction: row;
            background: #ffffff;
            padding: 10px 10px;
            gap: 5px;
            align-items: stretch;
            justify-content: space-between;
            flex-wrap: wrap;
        }}

        .cycle-step {{
            flex: 1;
            min-width: 105px;
            padding: 8px 9px;
            background: {c_bg_tint};
            border: 1px solid {c_border};
            border-radius: 6px;
            display: flex;
            flex-direction: column;
            box-sizing: border-box;
        }}

        .cycle-step-num {{
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: {theme_hex};
            color: #ffffff;
            font-size: 7.5pt;
            font-weight: 800;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 4px;
        }}

        .cycle-step-title {{
            font-size: 8.8pt;
            font-weight: 800;
            color: {c_dark};
            margin-bottom: 2.5px;
        }}

        .cycle-step-desc {{
            font-size: 7.9pt;
            line-height: 1.36;
            color: #475569;
        }}

        .cycle-arrow {{
            display: flex;
            align-items: center;
            color: {theme_hex};
            font-size: 11pt;
            font-weight: 800;
        }}

        /* 3. 2x2 Eksen Matrisi (Liderlik / Disiplin Stilleri) */
        .axis-matrix-2x2 {{
            margin: 12px 0;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid {c_border};
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        .axis-banner {{
            background: {theme_hex};
            color: #ffffff;
            padding: 7.5px 14px;
            display: flex;
            align-items: center;
            gap: 9px;
            border-bottom: 2px solid #c49a45;
            font-size: 9.6pt;
            font-weight: 800;
        }}

        .axis-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1px;
            background: {c_border};
        }}

        .axis-cell {{
            background: #ffffff;
            padding: 10px 12px;
            box-sizing: border-box;
        }}

        .axis-cell.highlight {{
            background: #f0fdf4;
            border-left: 3.5px solid #16a34a;
        }}

        .axis-cell-badge {{
            font-size: 7.2pt;
            font-weight: 800;
            padding: 1.5px 6px;
            border-radius: 4px;
            display: inline-block;
            margin-bottom: 3px;
        }}

        .axis-cell-badge.green {{ background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }}
        .axis-cell-badge.red {{ background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }}
        .axis-cell-badge.amber {{ background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }}
        .axis-cell-badge.gray {{ background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }}

        .axis-cell-title {{
            font-size: 9.1pt;
            font-weight: 800;
            color: {c_dark};
            margin-bottom: 3px;
        }}

        .axis-cell-desc {{
            font-size: 8.3pt;
            line-height: 1.38;
            color: #334155;
        }}

        /* 4. İsnad Akış Şeridi (Hadis III ve Tefsir Râvi Zincirleri) */
        .isnad-flow-strip {{
            margin: 8px 0;
            padding: 8px 12px;
            background: {c_bg_tint};
            border: 1px solid {c_border};
            border-left: 4.5px solid {theme_hex};
            border-radius: 6px;
            display: flex;
            align-items: center;
            gap: 6px;
            flex-wrap: wrap;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        .isnad-node {{
            padding: 3.5px 8px;
            border-radius: 4px;
            font-size: 8.3pt;
            font-weight: 700;
            background: #ffffff;
            border: 1px solid #cbd5e1;
            color: #334155;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1px;
        }}

        .isnad-node.sahabi {{
            background: #fef3c7;
            border-color: #fde68a;
            color: #92400e;
        }}

        .isnad-node.peygamber {{
            background: #dcfce7;
            border-color: #bbf7d0;
            color: #166534;
        }}

        .isnad-role {{
            font-size: 6.8pt;
            font-weight: 800;
            color: #64748b;
            text-transform: uppercase;
        }}

        .isnad-arrow {{
            color: {theme_hex};
            font-size: 10pt;
            font-weight: 800;
        }}

        /* 5. Tarihsel Dönemler Zaman Çizelgesi */
        .timeline-bar {{
            margin: 7px 0;
            padding: 7px 10px;
            background: #ffffff;
            border: 1px solid {c_border};
            border-radius: 6px;
            display: flex;
            align-items: stretch;
            gap: 6px;
            flex-wrap: wrap;
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        .timeline-node {{
            flex: 1;
            min-width: 100px;
            background: {c_bg_tint};
            border: 1px solid {c_border};
            border-top: 3.5px solid {theme_hex};
            border-radius: 5px;
            padding: 5px 8px;
            box-sizing: border-box;
        }}

        .timeline-date {{
            font-size: 7.2pt;
            font-weight: 800;
            color: #d97706;
            text-transform: uppercase;
            margin-bottom: 2px;
        }}

        .timeline-title {{
            font-size: 8.8pt;
            font-weight: 800;
            color: {c_dark};
            margin-bottom: 2px;
        }}

        .timeline-desc {{
            font-size: 8.0pt;
            line-height: 1.35;
            color: #475569;
        }}

        /* 6. Evrensel Kavram Matrisi (2'li, 3'lü, 4'lü) ve Doktrin Uyumluluğu */
        .entity-matrix-wrap {{
            margin: 12px 0;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid {c_border};
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        .doctrine-compare-wrap {{
            margin: 12px 0;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid {c_border};
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        .entity-grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1px; background: {c_border}; }}
        .entity-grid-3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1px; background: {c_border}; }}
        .entity-grid-4 {{ display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 1px; background: {c_border}; }}

        /* 7. Genel Barem / Yelpaze Skalası (Teklîfî Hükümler, Sıhhat, Kanaat) */
        .spectrum-bar {{
            margin: 10px 0 6px 0;
            border-radius: 6px;
            overflow: hidden;
            display: flex;
            height: 18px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            border: 1px solid #cbd5e1;
        }}

        .spectrum-item {{
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 6.8pt;
            font-weight: 800;
            color: #ffffff;
            text-transform: uppercase;
            letter-spacing: 0.2px;
        }}

        /* 8. Hiyerarşik Ağaç Şeması (İslam Toplumu, Devlet Yapısı, Soy Ağacı vb.) */
        .tree-diagram-wrap {{
            margin: 12px 0;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid {c_border};
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
            break-inside: avoid;
            page-break-inside: avoid;
            background: #ffffff;
        }}

        .tree-diagram-banner {{
            background: {theme_hex};
            color: #ffffff;
            padding: 7px 14px;
            font-size: 9.6pt;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 8px;
            border-bottom: 2px solid #c49a45;
        }}

        .tree-body {{
            padding: 12px 14px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
        }}

        .tree-root-node {{
            background: {c_bg_tint};
            border: 2px solid {theme_hex};
            border-radius: 6px;
            padding: 5px 16px;
            font-size: 9.3pt;
            font-weight: 800;
            color: {c_dark};
            box-shadow: 0 1px 4px rgba(0,0,0,0.04);
            text-align: center;
        }}

        .tree-connector-down {{
            width: 2px;
            height: 8px;
            background: {theme_hex};
        }}

        .tree-main-branches {{
            display: flex;
            justify-content: space-around;
            width: 100%;
            gap: 12px;
        }}

        .tree-main-branch {{
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 7px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 7px;
            padding: 8px 10px;
        }}

        .tree-branch-header {{
            width: 100%;
            text-align: center;
            padding: 4.5px 8px;
            border-radius: 5px;
            font-size: 8.8pt;
            font-weight: 800;
            color: #ffffff;
            background: {theme_hex};
        }}

        .tree-branch-header.alt {{
            background: #475569;
        }}

        .tree-branch-header.accent {{
            background: #d97706;
        }}

        .tree-subnodes {{
            display: flex;
            gap: 6px;
            width: 100%;
            justify-content: center;
            flex-wrap: wrap;
        }}

        .tree-subnode-card {{
            flex: 1;
            min-width: 85px;
            background: #ffffff;
            border: 1px solid {c_border};
            border-top: 3px solid {theme_hex};
            border-radius: 5px;
            padding: 5px 7px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        }}

        .tree-subnode-card.accent {{
            border-top-color: #d97706;
        }}

        .tree-subnode-card.alt {{
            border-top-color: #64748b;
        }}

        .tree-subnode-title {{
            font-size: 8.5pt;
            font-weight: 800;
            color: {c_dark};
            margin-bottom: 2px;
        }}

        .tree-subnode-desc {{
            font-size: 7.5pt;
            color: #64748b;
            line-height: 1.28;
        }}

        /* --- EVRENSEL PEDAGOJİK MATERYAL KÜTÜPHANESİ BİTİŞ --- */

        .diagram-box {{
            background-color: #f8fafc;
            border: 1px solid #cbd5e1;
            border-left: 4.5px solid #c49a45;
            border-radius: 8px;
            padding: 10px 14px;
            margin: 10px 0;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02);
            break-inside: avoid;
            page-break-inside: avoid;
            overflow-x: auto;
        }}

        .diagram-box pre {{
            margin: 0;
            padding: 0;
            background: transparent;
            border: none;
            font-family: 'JetBrains Mono', 'Cascadia Code', Consolas, 'Courier New', monospace;
            font-size: 8.5pt;
            line-height: 1.38;
            color: #334155;
            white-space: pre;
        }}

        .diagram-box code {{
            background: transparent;
            border: none;
            padding: 0;
            font-size: inherit;
            color: inherit;
        }}

        /* LİSTELER (KURAL 15: Özel kare imler ▪) */
        ul {{
            margin-top: 3px;
            margin-bottom: 8px;
            padding-left: 18px;
            list-style: none;
        }}

        ul li {{
            margin-bottom: 4px;
            line-height: 1.50;
            position: relative;
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        ul li p, ol li p {{
            margin: 0;
            display: inline;
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
            margin-top: 3px;
            margin-bottom: 8px;
            padding-left: 20px;
        }}

        ol li {{
            margin-bottom: 4px;
            line-height: 1.50;
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        li > ul, li > ol {{
            margin-top: 1.5px;
            margin-bottom: 3px;
        }}

        hr {{
            border: 0;
            height: 1px;
            background: {c_border};
            margin: 14px 0;
        }}

        /* HADİS KARTLARI */
        .hadis-card {{
            break-inside: avoid;
            page-break-inside: avoid;
            margin-bottom: 7px;
            background: #ffffff;
            border: 1px solid #dcfce7;
            border-left: 4.5px solid {theme_hex};
            border-radius: 7px;
            padding: 7px 12px;
            box-shadow: 0 1px 6px rgba(0, 0, 0, 0.03);
        }}

        .hadis-card h3.h3-styled {{
            margin-top: 0;
            margin-bottom: 3.5px;
            font-size: 10.2pt;
        }}

        /* SENED VE RÂVİ ROZETLERİ */
        .badge-medar {{
            background: #fff8e6;
            border: 1px solid #d4af37;
            color: #8c6209;
            font-weight: 800;
            padding: 1.5px 6px;
            border-radius: 4px;
            display: inline-block;
            font-size: 8.0pt;
            letter-spacing: 0.3px;
        }}

        .badge-mutabaat {{
            background: #edfbf3;
            border: 1px solid #2e7d32;
            color: #1b5e20;
            font-weight: 800;
            padding: 1.5px 6px;
            border-radius: 4px;
            display: inline-block;
            font-size: 8.0pt;
            letter-spacing: 0.3px;
        }}

        .badge-tahvil {{
            background: #fdf2f4;
            border: 1px solid #c2185b;
            color: #880e4f;
            font-weight: 800;
            padding: 1.5px 6px;
            border-radius: 4px;
            display: inline-block;
            font-size: 8.0pt;
            letter-spacing: 0.3px;
        }}

        .isnad-note-li {{
            list-style: none !important;
            margin-left: -14px !important;
        }}

        .isnad-note {{
            background: #fdfbf7;
            border: 1px solid #ebdcd0;
            border-left: 3.5px solid #d4af37;
            padding: 6px 11px;
            font-size: 8.8pt;
            color: #334155;
            margin-top: 5px;
            margin-bottom: 5px;
            border-radius: 0 5px 5px 0;
            line-height: 1.45;
        }}

        .hadis-card h3.h3-styled {{
            margin-top: 0;
            margin-bottom: 8px;
            color: {theme_hex};
            font-size: 10.8pt;
        }}

        .hadis-card ul {{
            margin: 0;
            padding-left: 14px;
        }}

        /* SORU KARTLARI (KURAL 15) */
        .q-card {{
            break-inside: avoid;
            page-break-inside: avoid;
            margin-bottom: 9px;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 7px;
            padding: 7px 11px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        }}

        .q-card-classic {{
            border-left: 4.5px solid {theme_hex};
            background: #fafcfb;
        }}

        .q-header {{
            display: flex;
            align-items: flex-start;
            gap: 8px;
            margin-bottom: 4px;
        }}

        .q-badge {{
            background: {theme_hex};
            color: #ffffff;
            font-size: 7.8pt;
            font-weight: 800;
            padding: 1.5px 6.5px;
            border-radius: 4px;
            flex-shrink: 0;
            line-height: 1.3;
        }}

        .q-stem {{
            font-size: 9.25pt;
            font-weight: 700;
            color: #0f172a;
            line-height: 1.38;
        }}

        .q-ans {{
            background-color: {c_bg_tint};
            border: 1px solid {c_light};
            border-radius: 5px;
            padding: 5px 9px;
            margin-top: 3px;
            font-size: 8.85pt;
            line-height: 1.45;
            color: #1e293b;
        }}

        .q-ans p {{
            margin: 0;
        }}

        .q-context {{
            font-size: 9.0pt;
            line-height: 1.45;
            color: #334155;
            margin: 5px 0 7px 0;
            padding: 5px 10px;
            background-color: #f8fafc;
            border-left: 3.5px solid #94a3b8;
            border-radius: 0 4px 4px 0;
        }}

        .q-options-single {{
            grid-template-columns: 1fr !important;
            gap: 4px 0 !important;
        }}

        .q-options {{
            margin-top: 4px;
            padding-left: 20px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2.5px 16px;
        }}

        .q-opt {{
            font-size: 8.75pt;
            line-height: 1.32;
            color: #334155;
            display: flex;
            align-items: baseline;
            gap: 5px;
        }}

        .opt-badge {{
            font-weight: 700;
            font-size: 8.0pt;
            color: {theme_hex};
            flex-shrink: 0;
        }}

        .q-opt.opt-correct {{
            font-weight: 700;
            color: #15803d;
        }}

        .q-opt.opt-correct .opt-badge {{
            color: #15803d;
        }}

        .opt-check {{
            color: #16a34a;
            font-weight: 900;
            margin-left: 3px;
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
    sinif_val, donem_val, sinav_val = _infer_donem_from_path(md_path, sinif, donem, sinav)

    with tempfile.TemporaryDirectory() as tmp_dir_str:
        tmp_dir = Path(tmp_dir_str)
        content_target = (tmp_dir / "content.pdf") if with_cover else output_pdf_path

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"file:///{str(html_out.resolve()).replace('\\\\', '/')}", wait_until="load")
            page.evaluate("() => document.fonts.ready")

            page.pdf(
                path=str(content_target),
                format="A4",
                print_background=True,
                margin={
                    "top": "24mm",
                    "bottom": "22mm",
                    "left": "14mm",
                    "right": "14mm"
                },
                display_header_footer=True,
                header_template=f"""
                    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 8.0pt; color: #64748b; width: 100%; border-bottom: 1px solid {c_light}; padding-top: 5mm; padding-bottom: 4px; margin: 0 14mm; display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; color: {theme_hex};">{title_display} — Okuma PDF</span>
                        <span style="font-weight: 500; color: #475569;">Ders Anlatımı &amp; İbare Şerhleri</span>
                    </div>
                """,
                footer_template=f"""
                    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 8.0pt; color: #64748b; width: 100%; border-top: 1px solid #e2e8f0; padding-top: 4px; padding-bottom: 4mm; margin: 0 14mm; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #64748b;">{title_display} — Akademik Çalışma Notu</span>
                        <span style="background-color: {c_bg_tint}; border: 1px solid {c_border}; color: {theme_hex}; padding: 1.5px 8px; border-radius: 12px; font-weight: 700;">Sayfa <span class="pageNumber"></span> / <span class="totalPages"></span></span>
                    </div>
                """
            )

            if with_cover:
                content_doc = pymupdf.open(content_target)
                content_pages = len(content_doc)
                units = _extract_pdf_units(content_doc, start_page_idx=0)
                content_doc.close()

                _fam, resolved_title, _sub, resolved_hex = resolve_course_meta(
                    course_name or md_path.stem, sinif_val, donem_val, sinav_val
                )
                use_hex = theme_hex or resolved_hex
                cover_html = render_single_course_cover_html(
                    course_name=course_name or md_path.stem,
                    theme_hex=use_hex,
                    content_pages=content_pages,
                    units=units,
                    sinif=sinif_val,
                    donem=donem_val,
                    sinav=sinav_val,
                )
                cover_html_path = tmp_dir / "cover.html"
                cover_pdf_path = tmp_dir / "cover.pdf"
                cover_html_path.write_text(cover_html, encoding="utf-8")

                cover_tab = browser.new_page()
                cover_tab.goto(f"file:///{str(cover_html_path.resolve()).replace(chr(92), '/')}", wait_until="load")
                cover_tab.evaluate("() => document.fonts.ready")
                cover_tab.pdf(
                    path=str(cover_pdf_path),
                    format="A4",
                    print_background=True,
                    margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
                )

                total_pages = 1 + content_pages
                tint_c = _cover_hsl_tint(use_hex, 0.96, 0.72)
                border_c = _cover_hsl_tint(use_hex, 0.78, 0.62)
                footer_specs = [
                    (1 + idx, resolved_title, use_hex, tint_c, border_c, idx, content_pages, total_pages)
                    for idx in range(1, content_pages + 1)
                ]
                footers_html_path = tmp_dir / "footers.html"
                footers_pdf_path = tmp_dir / "footers.pdf"
                footers_html_path.write_text(_render_footers_overlay_html(footer_specs), encoding="utf-8")
                footer_tab = browser.new_page()
                footer_tab.goto(f"file:///{str(footers_html_path.resolve()).replace(chr(92), '/')}", wait_until="load")
                footer_tab.evaluate("() => document.fonts.ready")
                footer_tab.pdf(
                    path=str(footers_pdf_path),
                    format="A4",
                    print_background=True,
                    margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
                )
            browser.close()

        if with_cover:
            cover_doc = pymupdf.open(cover_pdf_path)
            content_doc = pymupdf.open(content_target)
            footers_doc = pymupdf.open(footers_pdf_path)
            out_doc = pymupdf.open()
            out_doc.insert_pdf(cover_doc)
            out_doc.insert_pdf(content_doc)
            for idx in range(len(content_doc)):
                pg = out_doc[1 + idx]
                _redact_old_footer(pg)
                pg.show_pdf_page(pg.rect, footers_doc, idx, overlay=True)
            attach_course_cover_links(out_doc[0], units, first_content_page=2)
            toc = [[1, resolved_title, 1]] + [[2, utitle, 1 + local_pg] for local_pg, utitle in units]
            if toc:
                out_doc.set_toc(toc)
            out_doc.save(output_pdf_path, garbage=4, deflate=True)
            cover_doc.close()
            content_doc.close()
            footers_doc.close()
            out_doc.close()

    # Sayfa sayısını ve boyutunu doğrula
    doc = pymupdf.open(output_pdf_path)
    page_count = len(doc)
    doc.close()
    print(f"✓ Başarıyla üretildi: {output_pdf_path} ({page_count} sayfa, {output_pdf_path.stat().st_size:,} bayt)")

    # Eğer kaynaklar/özetlenmiş_dersler veya ders_anlatimlari altında karşılığı varsa oraya da kopyala
    mirror_target = None
    if "ders_anlatimlari" in md_path.parts:
        parts = list(md_path.parts)
        idx = parts.index("ders_anlatimlari")
        mirror_parts = parts[:idx] + ["kaynaklar", "özetlenmiş_dersler"] + parts[idx+1:]
        mirror_target = Path(*mirror_parts).with_suffix(".pdf")
        mirror_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(output_pdf_path, mirror_target)
        print(f"✓ Yedek kopya senkronize edildi: {mirror_target}")
    elif "özetlenmiş_dersler" in md_path.parts:
        parts = list(md_path.parts)
        idx = parts.index("özetlenmiş_dersler")
        if idx > 0 and parts[idx-1] == "kaynaklar":
            mirror_parts = parts[:idx-1] + ["ders_anlatimlari"] + parts[idx+1:]
        else:
            mirror_parts = parts[:idx] + ["ders_anlatimlari"] + parts[idx+1:]
        mirror_target = Path(*mirror_parts).with_suffix(".pdf")
        mirror_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(output_pdf_path, mirror_target)
        print(f"✓ Yedek kopya senkronize edildi: {mirror_target}")

    return output_pdf_path

def main():
    parser = argparse.ArgumentParser(description="Okuma PDF Üretim Motoru (Kural 15)")
    parser.add_argument("hedef", help="Markdown dosya yolu veya ders adı / slug")
    parser.add_argument("--sinif", default="3", help="Sınıf (2, 3)")
    parser.add_argument("--donem", default="1", help="Dönem (1, 2)")
    parser.add_argument("--sinav", default="vize", help="Sınav (vize, final)")
    parser.add_argument("--renk", default=None, help="Özel tema rengi hex (örn: #8C2F21)")
    parser.add_argument("--son-unite", type=int, default=None, help="Dahil edilecek son ünite numarası")
    parser.add_argument("--haric-unite", type=int, default=None, help="Hariç tutulacak ilk ünite numarası")
    parser.add_argument("--kapaksiz", action="store_true", help="Ders kapağı eklemeden yalnızca içerik PDF üretir")
    args = parser.parse_args()

    hedef_path = Path(args.hedef)
    if not hedef_path.exists():
        d_obj = donem_mod.Donem(args.sinif, args.donem, args.sinav)
        # Önce doğrudan ders klasörü var mı kontrol et
        target_dir = d_obj.ders_anlatimlari / args.hedef
        if not target_dir.exists():
            target_dirs = [p for p in d_obj.ders_anlatimlari.iterdir() if p.is_dir() and args.hedef.lower() in p.name.lower()]
            if target_dirs:
                target_dir = target_dirs[0]

        if target_dir.exists() and target_dir.is_dir():
            ozet_files = [f for f in target_dir.glob("*.md") if any(k in f.name.lower() for k in ['özet', 'ozet', 'sınav', 'sinav', 'kitapçık', 'kitapcik'])]
            if ozet_files:
                hedef_path = ozet_files[0]
            else:
                md_files = list(target_dir.glob("*.md"))
                if md_files:
                    hedef_path = md_files[0]

        if not hedef_path.exists():
            matches = list(d_obj.ders_anlatimlari.glob(f"**/*{args.hedef}*.md"))
            if not matches:
                matches = list(d_obj.ozetlenmis_dersler.glob(f"**/*{args.hedef}*.md"))
            if matches:
                ozet_matches = [m for m in matches if any(k in m.name.lower() for k in ['özet', 'ozet', 'sınav', 'sinav', 'kitapçık', 'kitapcik'])]
                hedef_path = ozet_matches[0] if ozet_matches else matches[0]
            else:
                print(f"Hata: '{args.hedef}' dosyası bulunamadı.")
                sys.exit(1)

    course_folder = hedef_path.parent.name
    theme_hex = args.renk or ders_rengi(course_folder, args.sinif, args.donem, args.sinav)

    print(f"Ders: {course_folder}")
    print(f"Girdi: {hedef_path}")
    print(f"Tema Rengi: {theme_hex}")

    generate_okuma_pdf(
        hedef_path,
        course_name=course_folder,
        theme_hex=theme_hex,
        son_unite=args.son_unite,
        haric_unite=args.haric_unite,
        sinif=args.sinif,
        donem=args.donem,
        sinav=args.sinav,
        with_cover=not args.kapaksiz,
    )

if __name__ == "__main__":
    main()
