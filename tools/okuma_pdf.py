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
    "1": "book",
    "2": "sword",
    "3": "scroll",
    "4": "bulb",
    "5": "dove",
    "6": "scale",
    "7": "pillar",
    "8": "search",
    "9": "book",
    "10": "sparkle",
}

_SVG_ICONS = {
    "book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 5.5A2.5 2.5 0 0 1 4.5 3H10a2 2 0 0 1 2 2v15a1.5 1.5 0 0 0-1.5-1.5H4.5A2.5 2.5 0 0 1 2 16V5.5Z"/><path d="M22 5.5A2.5 2.5 0 0 0 19.5 3H14a2 2 0 0 0-2 2v15a1.5 1.5 0 0 1 1.5-1.5h6A2.5 2.5 0 0 0 22 16V5.5Z"/><path d="M5.5 7.5h3.5M5.5 11h3.5M15 7.5h3.5M15 11h3.5" stroke="#e6c36e"/></svg>',
    "sword": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 17.5 3 6V3h3l11.5 11.5"/><path d="M13 19l6-6" stroke="#e6c36e"/><path d="M16 16l4 4"/><path d="M19 21l2-2"/></svg>',
    "scroll": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M8 21h12a2 2 0 0 0 2-2v-2H10v2a2 2 0 1 1-4 0V5a2 2 0 1 0-4 0v3h4"/><path d="M19 17V5a2 2 0 0 0-2-2H4"/><path d="M9 7h6M9 11h6" stroke="#e6c36e"/></svg>',
    "bulb": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6M10 22h4" stroke="#e6c36e"/></svg>',
    "dove": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M16 7h.01M3.4 18H12a8 8 0 0 0 8-8V7a4 4 0 0 0-7.28-2.3L2 20"/><path d="m20 7 2 .5-2 .5M10 18v3M14 17.75V21" stroke="#e6c36e"/></svg>',
    "scale": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18M7 21h10" stroke="#e6c36e"/><path d="M4 7h16"/><path d="M6 7l-3 8h6L6 7Z"/><path d="M18 7l-3 8h6l-3-8Z"/><path d="M3 15a3 3 0 0 0 6 0M15 15a3 3 0 0 0 6 0"/></svg>',
    "pillar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M4 18h16M5 9v9M9.5 9v9M14.5 9v9M19 9v9" /><path d="M3 9l9-6 9 6H3Z" stroke="#e6c36e"/></svg>',
    "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5" stroke="#e6c36e"/></svg>',
    "sparkle": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l2.6 7.4L22 12l-7.4 2.6L12 22l-2.6-7.4L2 12l7.4-2.6L12 2Z"/><circle cx="12" cy="12" r="2.2" fill="#e6c36e" stroke="none"/></svg>',
    "tree": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="3" width="6" height="4" rx="1" stroke="#e6c36e"/><path d="M12 7v5M5 12h14M5 12v4M12 12v4M19 12v4"/><rect x="3" y="16" width="4" height="4" rx="1"/><rect x="10" y="16" width="4" height="4" rx="1"/><rect x="17" y="16" width="4" height="4" rx="1"/></svg>',
    "globe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3.6 9h16.8M3.6 15h16.8" stroke="#e6c36e"/><path d="M12 3a13 13 0 0 0 0 18M12 3a13 13 0 0 1 0 18"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 17v5"/><path d="M9 10.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24V16h14v-.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 10.76V6a1 1 0 0 1 1-1V3H8v2a1 1 0 0 1 1 1Z"/></svg>',
    "star": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 14.9 8.6 22 9.3 16.6 14 18.2 21 12 17.3 5.8 21 7.4 14 2 9.3 9.1 8.6 12 2"/></svg>',
    "target": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/></svg>',
    "chart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 20h18"/><rect x="5" y="11" width="3.5" height="6" rx="0.8"/><rect x="10.25" y="7" width="3.5" height="10" rx="0.8" stroke="#e6c36e"/><rect x="15.5" y="4" width="3.5" height="13" rx="0.8"/></svg>',
    "note": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9Z"/><path d="M14 3v6h6M8 13h8M8 17h5" stroke="#e6c36e"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 4 6v6c0 5 3.4 8.5 8 10 4.6-1.5 8-5 8-10V6l-8-3Z"/><path d="m9 12 2 2 4-4" stroke="#e6c36e"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="m8.5 12.5 2.4 2.4 4.8-5.2"/></svg>',
    "cross": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="m9.5 9.5 5 5m0-5-5 5"/></svg>',
    "diamond": '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 1 10.2 5.8 15 8 10.2 10.2 8 15 5.8 10.2 1 8 5.8 5.8Z"/></svg>',
    "warn": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 3.8 2.2 18a2 2 0 0 0 1.7 3h16.2a2 2 0 0 0 1.7-3L13.7 3.8a2 2 0 0 0-3.4 0Z"/><path d="M12 9v4M12 17h.01"/></svg>',
}

_EMOJI_TO_SVG_KEY = {
    "📚": "book",
    "📖": "book",
    "⚔️": "sword",
    "⚔": "sword",
    "📜": "scroll",
    "💡": "bulb",
    "🕊️": "dove",
    "🕊": "dove",
    "⚖️": "scale",
    "⚖": "scale",
    "🏛️": "pillar",
    "🏛": "pillar",
    "🔍": "search",
    "✨": "sparkle",
    "🌿": "tree",
    "🌍": "globe",
    "📌": "pin",
    "⭐": "star",
    "🎯": "target",
    "📊": "chart",
    "📝": "note",
    "🛡️": "shield",
    "🛡": "shield",
    "⚠️": "warn",
    "⚠": "warn",
}


def _svg_icon(key: str, cls: str = "svg-ic") -> str:
    svg = _SVG_ICONS.get(key, _SVG_ICONS["book"])
    return f'<span class="{cls}" aria-hidden="true">{svg}</span>'


def _replace_leading_emoji_with_svg(text: str, cls: str = "banner-svg-ic") -> str:
    stripped = text.lstrip()
    for em, key in sorted(_EMOJI_TO_SVG_KEY.items(), key=lambda x: -len(x[0])):
        if stripped.startswith(em):
            rest = stripped[len(em):].lstrip()
            return f'{_svg_icon(key, cls)}<span>{rest}</span>' if rest else _svg_icon(key, cls)
    return text


def _find_matching_div(html_str: str, start_idx: int) -> tuple[int, int] | None:
    """verilen <div ...> başlangıç indeksinden eşleşen </div> son indeksini döndürür."""
    open_end = html_str.find('>', start_idx)
    if open_end == -1:
        return None
    depth = 1
    pos = open_end + 1
    tag_re = re.compile(r'<(/?)div\b[^>]*>', re.IGNORECASE)
    for m in tag_re.finditer(html_str, pos):
        if m.group(1) == '/':
            depth -= 1
            if depth == 0:
                return start_idx, m.end()
        else:
            depth += 1
    return None


def _transform_div_blocks(html_str: str, class_token: str, transformer) -> str:
    """İç içe <div> yapısını bozmadan belirli sınıfa sahip blokları dönüştürür."""
    pat = re.compile(rf'<div\b[^>]*class="[^"]*\b{re.escape(class_token)}\b[^"]*"[^>]*>', re.IGNORECASE)
    out = []
    cursor = 0
    while True:
        m = pat.search(html_str, cursor)
        if not m:
            out.append(html_str[cursor:])
            break
        bounds = _find_matching_div(html_str, m.start())
        if not bounds:
            out.append(html_str[cursor:])
            break
        s_idx, e_idx = bounds
        out.append(html_str[cursor:s_idx])
        out.append(transformer(html_str[s_idx:e_idx]))
        cursor = e_idx
    return "".join(out)

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

    # Satır başında "7. Ünite" gibi sıra bildiren paragrafların sahte numaralı liste (<ol>) olmasını önle
    pure_md = re.sub(r'^(\d+)\.(\s+(?:Ünite|Hafta|Yüzyıl|Asır)\b)', r'\1\\.\2', pure_md, flags=re.MULTILINE)

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

    # Ünite başlıklarını (H1) çok katmanlı vektörel banner levhalarına dönüştür
    def replace_h1(match):
        content = match.group(1).strip()
        is_first = bool(re.search(r'(?:(?<!\d)1\.\s*(?:ÜNİTE|BÖLÜM|HAFTA)|(?:ÜNİTE|BÖLÜM|HAFTA)\s*1\b)', content, re.IGNORECASE))
        cls = "unit-banner-container first-unit" if is_first else "unit-banner-container"

        icon_key = "book"
        m_num = re.search(r'(?:(\d+)\.\s*(?:ÜNİTE|BÖLÜM|HAFTA)|(?:ÜNİTE|BÖLÜM|HAFTA)\s*(\d+))', content, re.IGNORECASE)
        if m_num:
            num = m_num.group(1) or m_num.group(2)
            icon_key = UNIT_ICONS.get(num, "book")
        elif "EK BÖLÜM" in content or "EK" in content:
            icon_key = "chart"
        elif "GİRİŞ" in content:
            icon_key = "book"
        elif "SORU" in content or "SINAV" in content:
            icon_key = "note"
        elif "İNKÂR" in content or "FELSEFE" in content:
            icon_key = "shield"

        # Başlık sonundaki sayfa / ünite parantezini sağ kapsüle taşı (h1.unit-title 13.2pt korunur)
        title_main = content
        meta_pill_html = ""
        m_meta = re.search(r'\s*\(([^)]*(?:ÜNİTE|BÖLÜM|HAFTA|s\.)[^)]*)\)\s*$', content, re.IGNORECASE)
        if m_meta:
            meta_txt = m_meta.group(1).strip()
            title_main = content[:m_meta.start()].strip()
            meta_txt = re.sub(r'\s*[—–-]\s*', ' · ', meta_txt)
            meta_pill_html = f'<span class="unit-meta-pill">{meta_txt}</span>'

        watermark_svg = (
            '<svg class="unit-watermark" viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="1">'
            '<circle cx="60" cy="60" r="50"/><circle cx="60" cy="60" r="36" stroke-dasharray="3 3"/>'
            '<polygon points="60,12 72,48 108,60 72,72 60,108 48,72 12,60 48,48"/>'
            '<circle cx="60" cy="60" r="14"/>'
            '</svg>'
        )

        return f'''<div class="{cls}">
            <div class="unit-banner-inner">
                {watermark_svg}
                <div class="unit-icon-box">{_svg_icon(icon_key, "unit-svg-ic")}</div>
                <div class="unit-title-wrap">
                    <h1 class="unit-title">{title_main}</h1>
                </div>
                {meta_pill_html}
            </div>
        </div>'''

    html_body = re.sub(r'<h1>([\s\S]*?)</h1>', replace_h1, html_body)

    # H2 alt başlıklarında metni tek parça inline kapsama al (flex boşluk sıçramasını önler)
    def replace_h2(match):
        inner = match.group(1).strip()
        m_b = re.match(r'^(\s*<span class="h2-badge">[\s\S]*?</span>)\s*([\s\S]*)$', inner)
        if m_b:
            return f'<h2>{m_b.group(1)} <span class="h2-text">{m_b.group(2).strip()}</span></h2>'
        return f'<h2><span class="h2-text">{inner}</span></h2>'

    html_body = re.sub(r'<h2>([\s\S]*?)</h2>', replace_h2, html_body)

    # H3 başlıklarına vektörel altın yıldız/elmas imi ekle
    def replace_h3(match):
        content = match.group(1).strip()
        return f'<h3 class="h3-styled">{_svg_icon("diamond", "h3-diamond")} <span class="h3-content">{content}</span></h3>'

    html_body = re.sub(r'<h3>([\s\S]*?)</h3>', replace_h3, html_body)

    # Ünite öncesi <hr> temizliği
    html_body = re.sub(r'<hr\s*/?>\s*(<div class="unit-banner-container)', r'\1', html_body)

    # Manuel sayfa sonu imi desteği (<!-- pagebreak -->)
    html_body = re.sub(r'<!--\s*pagebreak\s*-->', '<div style="break-before: page; page-break-before: always;"></div>', html_body, flags=re.IGNORECASE)

    # Callout / Alıntı kutuları (Sınav & Dipnot vs Arapça Nass)
    def tag_blockquotes(match):
        content = match.group(1)
        alert_match = re.search(r'\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]', content)
        is_warn = any(kw in content for kw in ['Önemli Hatırlatma', 'Hayati Kelâmî Kaide', 'Püf Noktası', 'Altın Kural', 'Sınav Uyarısı', 'Ders İçi İkaz'])
        if '📌' in content or alert_match or is_warn:
            alert_type = alert_match.group(1) if alert_match else ""
            clean_content = re.sub(r'<p>\s*\[!(?:NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*', '<p>', content)
            clean_content = clean_content.replace('📌', '').strip()
            if any(kw in content for kw in ['Önemli Hatırlatma', 'Ders İçi İkaz', 'Sınav Uyarısı']):
                tag_html = f'{_svg_icon("warn", "tag-svg-ic")}<span>DERS İÇİ İKAZ &amp; SINAV UYARISI</span>'
            elif any(kw in content for kw in ['Hayati Kelâmî Kaide', 'Altın Kural']):
                tag_html = f'{_svg_icon("star", "tag-svg-ic")}<span>HAYATİ KELÂMÎ KAİDE &amp; İLKE</span>'
            elif 'Püf Noktası' in content:
                tag_html = f'{_svg_icon("target", "tag-svg-ic")}<span>KELÂMÎ PÜF NOKTASI</span>'
            elif alert_type in ("NOTE", "TIP"):
                tag_html = f'{_svg_icon("pin", "tag-svg-ic")}<span>AKADEMİK DEĞERLENDİRME &amp; SINAV NOTU</span>'
            else:
                tag_html = f'{_svg_icon("pin", "tag-svg-ic")}<span>KİTAP DİPNOTU &amp; SINAV UYARISI</span>'
            return f'''<blockquote class="callout callout-pinned">
                <div class="pinned-header"><span class="pinned-tag">{tag_html}</span></div>
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
            <div class="pinned-header"><span class="pinned-tag">{_svg_icon("pin", "tag-svg-ic")}<span>KİTAP DİPNOTU &amp; SINAV UYARISI</span></span></div>
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
                       lambda m: f'<li class="isnad-note-li"><div class="isnad-note">{_svg_icon("scale", "inline-svg-ic")} <strong>Sened Sıhhati &amp; Usûl Notu:</strong> {m.group(1)}</div></li>',
                       html_body)

    # Sınav Püf Noktası ve Not Rozetleri
    html_body = re.sub(r'<strong>(?:🎯\s*)?Sınav Püf Noktası:</strong>',
                       f'<span class="badge-sinav">{_svg_icon("target", "tag-svg-ic")}<span>SINAV PÜF NOKTASI</span></span>', html_body)
    html_body = re.sub(r'<strong>(?:📌\s*)?Hoca(?:nın)? Sınav Notu:</strong>',
                       f'<span class="badge-sinav">{_svg_icon("pin", "tag-svg-ic")}<span>SINAV NOTU</span></span>', html_body)
    html_body = re.sub(r'<strong>(?:⚠️\s*)?Sınav İkaz(?:ı|ları)?:</strong>',
                       f'<span class="badge-sinav">{_svg_icon("warn", "tag-svg-ic")}<span>SINAV İKAZI</span></span>', html_body)
    html_body = re.sub(r'<strong>(?:💡\s*)?Hoca Notu:</strong>',
                       f'<span class="badge-hoca">{_svg_icon("bulb", "tag-svg-ic")}<span>DERS NOTU</span></span>', html_body)

    # Hadis bölümlerini (H3 + UL) bölünmez bütün bloklar haline getir
    html_body = re.sub(
        r'(<h3 class="h3-styled">[\s\S]*?Hadis\s*\d+:[\s\S]*?</h3>\s*<ul>[\s\S]*?</ul>)',
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

    # --- GÖRSEL & GRAFİK BİLEŞEN YÜKSELTİCİ (STANDART KALİTE MOTORU) ---
    # 1. Banner içindeki sistem emojilerini vektörel SVG ikonlara çevir
    html_body = re.sub(
        r'<span class="(dok-icon|ent-icon|ont-icon)">([\s\S]*?)</span>',
        lambda m: f'<span class="{m.group(1)}">{_replace_leading_emoji_with_svg(m.group(2).strip(), "banner-svg-ic")}</span>',
        html_body,
    )
    for banner_cls in ("tree-diagram-banner", "axis-banner", "cycle-banner"):
        def _upgrade_banner_emoji(m, bcls=banner_cls):
            inner = m.group(1)
            inner_new = re.sub(
                r'<span>([\s\S]*?)</span>',
                lambda sm: f'<span class="banner-title-flex">{_replace_leading_emoji_with_svg(sm.group(1), "banner-svg-ic")}</span>',
                inner,
                count=1,
            )
            return f'<div class="{bcls}">{inner_new}</div>'
        html_body = re.sub(rf'<div class="{banner_cls}">([\s\S]*?)</div>', _upgrade_banner_emoji, html_body)

    # 2. Zaman Çizelgesi (.timeline-bar): Kronoloji rayı, düğüm noktaları, oklar ve ODAK DÖNEM vurgusu
    def _enhance_timeline(block: str) -> str:
        nodes = []
        cursor = 0
        node_pat = re.compile(r'<div\b[^>]*class="[^"]*\btimeline-node\b[^"]*"[^>]*>', re.IGNORECASE)
        while True:
            m = node_pat.search(block, cursor)
            if not m:
                break
            b = _find_matching_div(block, m.start())
            if not b:
                break
            node_html = block[b[0]:b[1]]
            is_active = ('★' in node_html) or ('#d97706' in m.group(0))
            node_html = re.sub(r'^<div\b[^>]*>', '<div class="timeline-node timeline-node-active">' if is_active else '<div class="timeline-node">', node_html, count=1)
            node_html = node_html.replace('★', '').strip()
            if is_active:
                node_html = re.sub(
                    r'(<div class="timeline-date">[\s\S]*?</div>)',
                    r'\1<span class="timeline-focus-pill">ODAK DÖNEM</span>',
                    node_html,
                    count=1,
                )
            # Her düğümün tepesine kronoloji dairesi yerleştir
            node_html = re.sub(
                r'^(<div class="timeline-node[^"]*">)',
                r'\1<div class="timeline-dot-row"><span class="timeline-dot"></span></div>',
                node_html,
                count=1,
            )
            nodes.append(node_html)
            cursor = b[1]
        if not nodes:
            return block
        joined = '<div class="timeline-connector"><span class="timeline-arrow">→</span></div>'.join(nodes)
        return f'<div class="timeline-bar"><div class="timeline-rail"></div><div class="timeline-nodes-row">{joined}</div></div>'

    html_body = _transform_div_blocks(html_body, "timeline-bar", _enhance_timeline)

    # 3. Hiyerarşik Piramit (.concept-pyramid): Gerçek yamuk kademeli piramit + sağda bütünleşik açıklama panelleri
    def _enhance_pyramid(block: str) -> str:
        inner = re.sub(r'^<div\b[^>]*>', '', block, count=1)
        inner = re.sub(r'</div>\s*$', '', inner, count=1).strip()
        tiers = []
        pos = 0
        tier_pat = re.compile(r'<div\b[^>]*class="[^"]*\bpyramid-tier\b([^"]*)"[^>]*>', re.IGNORECASE)
        while True:
            m = tier_pat.search(inner, pos)
            if not m:
                break
            b = _find_matching_div(inner, m.start())
            if not b:
                break
            tier_cls = "top" if "top" in m.group(1) else ("middle" if "middle" in m.group(1) else "base")
            tier_html = inner[b[0]:b[1]]
            tier_inner = re.sub(r'^<div\b[^>]*>', '', tier_html, count=1)
            tier_inner = re.sub(r'</div>\s*$', '', tier_inner, count=1).strip()
            pos = b[1]
            # Hemen ardından bir açıklama div'i geliyorsa yakala
            rest = inner[pos:].lstrip()
            desc_html = ""
            if rest.startswith('<div') and not rest.startswith('<div class="pyramid-tier'):
                offset = len(inner) - len(rest)
                db = _find_matching_div(inner, offset)
                if db:
                    d_raw = inner[db[0]:db[1]]
                    d_raw = re.sub(r'^<div\b[^>]*>', '', d_raw, count=1)
                    desc_html = re.sub(r'</div>\s*$', '', d_raw, count=1).strip()
                    pos = db[1]
            tiers.append((tier_cls, tier_inner, desc_html))
        if not tiers:
            return block
        rows_html = []
        for idx_t, (tcls, t_inner, d_html) in enumerate(tiers, start=1):
            # Piramit başlığındaki "TR (Arapça)" yapısını iki dengeli satıra böl (kesilme ve yalnız parantez önlenir)
            t_clean = re.sub(
                r'<span class="pyr-title">([^<(]+?)\s*\(\s*(<code class="ar"[^>]*>[\s\S]*?</code>(?:&lrm;)?)\s*\)\s*</span>',
                r'<span class="pyr-title"><span class="pyr-tr">\1</span><span class="pyr-ar">\2</span></span>',
                t_inner,
            )
            desc_part = f'<div class="pyr-leader"></div><div class="pyr-desc-card pyr-desc-{tcls}">{d_html}</div>' if d_html else ''
            rows_html.append(
                f'<div class="pyr-row pyr-row-{tcls}">'
                f'<div class="pyr-wedge-col"><div class="pyr-wedge pyr-wedge-{tcls}">{t_clean}</div></div>'
                f'{desc_part}'
                f'</div>'
            )
        has_desc = any(d for _, _, d in tiers)
        panel_cls = "pyramid-panel pyramid-with-desc" if has_desc else "pyramid-panel"
        return f'<div class="{panel_cls}">{"".join(rows_html)}</div>'

    html_body = _transform_div_blocks(html_body, "concept-pyramid", _enhance_pyramid)

    # 4. Doktrin / Mukayese Kartları (.dok-card): Üst başlık şeridi + vektörel simge + temiz liste
    def _enhance_dok_card(block: str) -> str:
        is_red = 'dok-pill red' in block
        is_green = 'dok-pill green' in block
        variant = "dok-card-red" if is_red else ("dok-card-green" if is_green else "dok-card-theme")
        out = re.sub(r'^<div\b[^>]*>', f'<div class="dok-card {variant}">', block, count=1)
        if is_red:
            out = out.replace('<span class="dok-pill red">', f'<span class="dok-pill red">{_svg_icon("cross", "pill-svg-ic")} ', 1)
        elif is_green:
            out = out.replace('<span class="dok-pill green">', f'<span class="dok-pill green">{_svg_icon("check", "pill-svg-ic")} ', 1)
        # Ham <p>• ...<br>...</p> satırlarını yapılandırılmış <ul class="dok-points"> listesine dönüştür
        def _p_bullets_to_ul(pm):
            p_inner = pm.group(1)
            if '•' not in p_inner:
                return pm.group(0)
            parts = [seg.strip() for seg in re.split(r'<br\s*/?>', p_inner) if seg.strip()]
            lis = []
            for seg in parts:
                seg_clean = re.sub(r'^•\s*', '', seg).strip()
                if seg_clean:
                    lis.append(f'<li>{seg_clean}</li>')
            return f'<ul class="dok-points">{"".join(lis)}</ul>' if lis else pm.group(0)
        out = re.sub(r'<p\b[^>]*>([\s\S]*?)</p>', _p_bullets_to_ul, out)
        return out

    html_body = _transform_div_blocks(html_body, "dok-card", _enhance_dok_card)

    # 5. Hiyerarşik Ağaç Şeması (.tree-diagram-wrap): Gerçek çok kollu SVG bağlantı ağacı ve dengeli sütunlar
    def _enhance_tree(block: str) -> str:
        # Kaç ana dal olduğunu say
        branch_matches = list(re.finditer(r'<div\b[^>]*class="[^"]*\btree-main-branch\b[^"]*"[^>]*>', block, re.IGNORECASE))
        n_branches = len(branch_matches)
        out = block
        if n_branches in (2, 3, 4):
            xs = [round((i + 0.5) * 600.0 / n_branches, 1) for i in range(n_branches)]
            x_first, x_last = xs[0], xs[-1]
            stems = "".join(
                f'<line x1="{x}" y1="12" x2="{x}" y2="23"/>'
                f'<polygon points="{x-3.5},20 {x+3.5},20 {x},26" class="tree-svg-arrow"/>'
                for x in xs
            )
            svg_conn = (
                f'<div class="tree-svg-connector">'
                f'<svg viewBox="0 0 600 26" preserveAspectRatio="none">'
                f'<line x1="300" y1="0" x2="300" y2="12"/>'
                f'<line x1="{x_first}" y1="12" x2="{x_last}" y2="12"/>'
                f'{stems}'
                f'</svg></div>'
            )
            out = out.replace('<div class="tree-connector-down"></div>', svg_conn, 1)
            out = out.replace('<div class="tree-main-branches">', f'<div class="tree-main-branches tree-cols-{n_branches}">', 1)

        # Her dalın inline stillerini uyumlu tema varyantlarına dönüştür
        branch_idx = [0]
        def _clean_branch(b_html: str) -> str:
            idx_b = branch_idx[0]
            branch_idx[0] += 1
            var_cls = ["branch-theme", "branch-gold", "branch-sage", "branch-slate"][idx_b % 4]
            res = re.sub(r'^<div\b[^>]*>', f'<div class="tree-main-branch {var_cls}">', b_html, count=1)
            res = re.sub(r'<div class="tree-branch-header[^"]*"[^>]*>', '<div class="tree-branch-header">', res)
            res = re.sub(r'<div class="tree-subnode-card[^"]*"[^>]*>', '<div class="tree-subnode-card">', res)
            return res
        out = _transform_div_blocks(out, "tree-main-branch", _clean_branch)
        return out

    html_body = _transform_div_blocks(html_body, "tree-diagram-wrap", _enhance_tree)

    # 6. 3'lü / 2'li / 4'lü Kavram Kartları (.entity-card): Arapça ibareyi ayrı üst banda al
    def _enhance_entity_card(block: str) -> str:
        ar_m = re.search(r'<span class="ent-ar"[^>]*>([\s\S]*?)</span>', block)
        if not ar_m:
            return block
        ar_inner = ar_m.group(1).strip()
        out = block[:ar_m.start()] + block[ar_m.end():]
        out = re.sub(
            r'(<div class="ent-card-header">[\s\S]*?</div>)',
            rf'\1<div class="ent-ar-band" dir="rtl">{ar_inner}</div>',
            out,
            count=1,
        )
        return out

    html_body = _transform_div_blocks(html_body, "entity-card", _enhance_entity_card)

    # 7. 2x2 Eksen Matrisi (.axis-matrix-2x2): Numara madalyonu ve tema uyumlu 4 hücre rengi
    def _enhance_axis_grid(block: str) -> str:
        cell_idx = [0]
        def _clean_axis_cell(c_html: str) -> str:
            idx_c = cell_idx[0]
            cell_idx[0] += 1
            v_cls = f"axis-cell-v{(idx_c % 4) + 1}"
            return re.sub(r'^<div\b[^>]*>', f'<div class="axis-cell {v_cls}">', c_html, count=1)
        return _transform_div_blocks(block, "axis-cell", _clean_axis_cell)

    html_body = _transform_div_blocks(html_body, "axis-matrix-2x2", _enhance_axis_grid)

    # 8. Nass Levhaları (.nass-board): Arapça metin iç çerçevesi ve çoklu âyet meal rozetleri
    def _enhance_nass_board(block: str) -> str:
        out = block
        # Arapça metni zarif iç parşömen çerçeveye al
        out = re.sub(
            r'(<div class="nass-arabic-text"[^>]*>[\s\S]*?</div>)',
            r'<div class="nass-arabic-frame">\1</div>',
            out,
            count=1,
        )
        # Çoklu âyet meali (125. Âyet: ... <br> 126. Âyet: ...) varsa ayırıcı satırlar üret
        def _split_ayah_trans(tm):
            inner = tm.group(1).strip()
            ayah_hits = re.findall(r'<strong>\s*(\d+\.\s*Âyet)\s*:?\s*</strong>', inner)
            if len(ayah_hits) < 2:
                return tm.group(0)
            segs = re.split(r'(?=<strong>\s*\d+\.\s*Âyet\s*:?\s*</strong>)', inner)
            rows = []
            for seg in segs:
                seg = re.sub(r'(?:<br\s*/?>\s*)+$', '', seg.strip()).strip()
                if not seg:
                    continue
                m_a = re.match(r'^<strong>\s*(\d+\.\s*Âyet)\s*:?\s*</strong>\s*([\s\S]*)$', seg)
                if m_a:
                    rows.append(
                        f'<div class="ayah-trans-row">'
                        f'<span class="ayah-num-pill">{m_a.group(1)}</span>'
                        f'<span class="ayah-body">{m_a.group(2).strip()}</span>'
                        f'</div>'
                    )
                else:
                    rows.append(f'<div class="ayah-trans-row"><span class="ayah-body">{seg}</span></div>')
            return f'<div class="ayah-trans-list">{"".join(rows)}</div>'
        out = re.sub(r'<p class="nass-trans-text">([\s\S]*?)</p>', _split_ayah_trans, out)
        return out

    html_body = _transform_div_blocks(html_body, "nass-board", _enhance_nass_board)

    # 9. Lügat Şerhi Listeleri (<ul> içinde >= 4 maddesi de `<code class="ar">...</code> :` olan listeleri 2 sütunlu sözlük kartına dönüştür)
    def _upgrade_lugat_ul(m):
        ul_inner = m.group(1)
        items = re.findall(r'<li>([\s\S]*?)</li>', ul_inner)
        if len(items) < 4:
            return m.group(0)
        parsed = []
        for it in items:
            it_clean = re.sub(r'^<p>([\s\S]*?)</p>$', r'\1', it.strip()).strip()
            m_kv = re.match(r'^(<code class="ar"[^>]*>[\s\S]*?</code>(?:&lrm;)?)\s*:\s*([\s\S]+)$', it_clean)
            if not m_kv:
                return m.group(0)
            parsed.append((m_kv.group(1), m_kv.group(2).strip()))
        cards = [
            f'<div class="lugat-item"><div class="lugat-head">{k}</div><div class="lugat-def">{v}</div></div>'
            for k, v in parsed
        ]
        return f'<div class="lugat-grid-2">{"".join(cards)}</div>'

    html_body = re.sub(r'<ul>([\s\S]*?)</ul>', _upgrade_lugat_ul, html_body)

    # 10. İkili Terim Kapsülü (badge-tr + Arapça karşılığı), Yumuşak Parantez, ﷺ ve Diyagram Giriş Koruması
    # 1) Dış parantez içinde birleşik: (<span class="badge-tr">X</span> — <code class="ar">Y</code>)
    html_body = re.sub(
        r'\(\s*<span class="badge-tr">([^<]+)</span>\s*(?:[-—–,]\s*|/\s*)(<code class="ar"[^>]*><bdi>(?:(?!</bdi>)[\s\S])*?</bdi></code>)(?:&lrm;)?\s*\)',
        lambda m: f'<span class="dual-pill"><span class="dual-pill-tr">{m.group(1).strip()}</span><span class="dual-pill-ar">{m.group(2)}</span></span>&lrm;',
        html_body,
    )
    # 2) Rozet ardından parantez içinde Arapça: <span class="badge-tr">X</span> (<code class="ar">Y</code>)
    html_body = re.sub(
        r'<span class="badge-tr">([^<]+)</span>\s*\(\s*(<code class="ar"[^>]*><bdi>(?:(?!</bdi>)[\s\S])*?</bdi></code>)(?:&lrm;)?\s*\)',
        lambda m: f'<span class="dual-pill"><span class="dual-pill-tr">{m.group(1).strip()}</span><span class="dual-pill-ar">{m.group(2)}</span></span>&lrm;',
        html_body,
    )
    # 3) Rozet ardından tire ile Arapça: <span class="badge-tr">X</span> — <code class="ar">Y</code>
    html_body = re.sub(
        r'<span class="badge-tr">([^<]+)</span>\s*[—–]\s*(<code class="ar"[^>]*><bdi>(?:(?!</bdi>)[\s\S])*?</bdi></code>)(?:&lrm;)?',
        lambda m: f'<span class="dual-pill"><span class="dual-pill-tr">{m.group(1).strip()}</span><span class="dual-pill-ar">{m.group(2)}</span></span>&lrm;',
        html_body,
    )

    # Rozet/ibare etrafındaki kaba siyah parantezleri yumuşat ve kısa kalıpların satır sonunda tek parantez bırakmasını önle
    def _wrap_ar_paren(m):
        inner = m.group(1)
        plain = re.sub(r'<[^>]+>', '', inner).replace('&lrm;', '').strip()
        wrapped = f'<span class="ar-paren">(</span>{inner}<span class="ar-paren">)</span>'
        if len(plain) <= 45:
            return f'<span class="ar-paren-group">{wrapped}</span>'
        return wrapped

    html_body = re.sub(
        r'\(\s*((?:<code class="ar"[^>]*>[\s\S]*?</code>|<span class="ar-quote">[\s\S]*?</span>)(?:&lrm;)?)\s*\)',
        _wrap_ar_paren,
        html_body,
    )

    # Rozet sonrası sarkan iki nokta boşluklarını temizle (örn: </span> :) ve kısa Arapça pill sonrası noktalama (. , ; :) satır başına düşmesin
    html_body = re.sub(r'(</span>|</code>(?:&lrm;)?)\s+:', r'\1:', html_body)
    def _glue_ar_punc(m):
        tag, punc = m.group(1), m.group(2)
        plain = re.sub(r'<[^>]+>', '', tag).replace('&lrm;', '').strip()
        if len(plain) <= 45:
            return f'<span class="ar-paren-group">{tag}{punc}</span>'
        return f'{tag}&#8288;{punc}'
    html_body = re.sub(
        r'(<code class="ar"[^>]*>(?:(?!</code>)[\s\S])*?</code>(?:&lrm;)?)([.,;:])(?=\s|<|$)',
        _glue_ar_punc,
        html_body,
    )

    # ﷺ glifini Amiri fontuyla netleştir (renk kalıtımı banner içinde görünür kalmasını sağlar)
    html_body = html_body.replace('ﷺ', '<span class="sallallahu">ﷺ</span>')

    # Görsel şema veya tablodan hemen önceki tanıtım paragrafını + başlığı birbirine bağla (sayfa altında öksüz kalmasını önler)
    _visual_target_re = r'(?:<div class="(?:nass-board|tree-diagram-wrap|doctrine-compare-wrap|entity-matrix-wrap|axis-matrix-2x2|pyramid-panel|timeline-bar|formula-card|lugat-grid-2)\b|<table>)'
    html_body = re.sub(
        rf'<p>((?:(?!<p\b|</p>)[\s\S]){{1,340}}?)</p>(\s*{_visual_target_re})',
        r'<p class="diagram-intro">\1</p>\2',
        html_body,
    )
    html_body = re.sub(
        rf'(<(h[23])\b[^>]*>(?:(?!</h[23]>)[\s\S])*?</\2>\s*<p class="diagram-intro">(?:(?!</p>)[\s\S])*?</p>)(\s*{_visual_target_re})',
        r'<div class="section-lead">\1</div>\3',
        html_body,
    )

    # Tablo hücrelerindeki çıplak Arapça (<strong>مَنْهَج</strong> veya saf Arapça) terimleri Amiri/BiDi ile büyüt
    def _wrap_td_arabic(m):
        tag_open, inner, tag_close = m.group(1), m.group(2), m.group(3)
        if 'class="ar"' in inner or 'td-ar-term' in inner:
            return m.group(0)
        plain = re.sub(r'<[^>]+>', '', inner).strip()
        if plain and ARABIC_RE.search(plain) and not re.search(r'[A-Za-zÇĞİÖŞÜçğıöşü]', plain):
            inner_clean = re.sub(r'</?strong>', '', inner).strip()
            return f'{tag_open}<span class="td-ar-term" dir="rtl"><bdi>{inner_clean}</bdi></span>{tag_close}'
        return m.group(0)

    html_body = re.sub(r'(<td\b[^>]*>)([\s\S]*?)(</td>)', _wrap_td_arabic, html_body)

    # Renk türevleri (Dersin tema renginden zengin, pastel ve BiDi uyumlu palet)
    c_dark = darken_color(theme_hex, 0.62)
    c_deep = darken_color(theme_hex, 0.44)
    c_mid = lighten_color(theme_hex, 0.14)
    c_bg_tint = theme_hsl_tint(theme_hex, lightness=0.962, min_saturation=0.50)
    c_bg_end = theme_hsl_tint(theme_hex, lightness=0.974, min_saturation=0.45)
    c_border = theme_hsl_tint(theme_hex, lightness=0.81, min_saturation=0.42)
    c_pill_bg = theme_hsl_tint(theme_hex, lightness=0.945, min_saturation=0.56)
    c_pill_border = theme_hsl_tint(theme_hex, lightness=0.77, min_saturation=0.48)
    c_light = c_border
    c_tint = c_pill_bg
    c_badge_grad = darken_color(theme_hex, 0.85)
    c_gold = "#c49a45"
    c_gold_bright = "#e6c36e"
    c_gold_dark = "#8a6212"
    c_gold_bg = "#fdf8ec"
    c_gold_border = "#ead296"

    sinif_val, donem_val, sinav_val = _infer_donem_from_path(md_path, sinif, donem, sinav)
    sinav_label = "Final" if sinav_val.lower() == "final" else "Vize"
    title_display = course_name or re.sub(r'\s*-\s*(?:Vize|Final)\s+Sınavı\s+Konu\s+Özeti.*$', '', md_path.stem, flags=re.IGNORECASE).strip()

    full_html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_display} — {sinav_label} Okuma PDF</title>
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
            font-size: 9.7pt;
            line-height: 1.56;
            color: #1e293b;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
        }}

        .svg-ic, .banner-svg-ic, .unit-svg-ic, .tag-svg-ic, .pill-svg-ic, .inline-svg-ic {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            vertical-align: middle;
        }}
        .unit-svg-ic svg {{ width: 19px; height: 19px; }}
        .banner-svg-ic svg {{ width: 15px; height: 15px; }}
        .tag-svg-ic svg {{ width: 11px; height: 11px; }}
        .pill-svg-ic svg {{ width: 10.5px; height: 10.5px; }}
        .inline-svg-ic svg {{ width: 13px; height: 13px; }}

        .sallallahu {{
            font-family: 'Amiri', 'Traditional Arabic', serif;
            font-size: 1.18em;
            font-weight: 400;
            color: inherit !important;
            vertical-align: baseline;
            margin: 0 1px;
        }}

        .diagram-intro {{
            break-after: avoid !important;
            page-break-after: avoid !important;
            margin-bottom: 6px;
        }}

        .section-lead {{
            break-inside: avoid !important;
            page-break-inside: avoid !important;
            break-after: avoid !important;
            page-break-after: avoid !important;
        }}
        .section-lead > h2 {{
            margin-bottom: 5px;
        }}
        .section-lead > p:last-child {{
            margin-bottom: 6px;
        }}

        .ar, [dir="rtl"], bdi.ar {{
            font-family: 'Amiri', 'Traditional Arabic', 'Scheherazade New', 'Arabic Typesetting', serif;
            font-size: 1.30em;
            line-height: 1.48;
            direction: rtl;
            unicode-bidi: isolate;
            color: {c_dark};
        }}
        p [dir="rtl"], li [dir="rtl"], td [dir="rtl"] {{
            font-size: 1.24em;
            line-height: 1.26;
        }}
        h2 [dir="rtl"], h3 [dir="rtl"] {{
            font-size: 1.18em;
            line-height: 1.22;
        }}

        /* ROZETLER: Köşe bükülmesi yapmayan, yan çizgisiz ve taban çizgisini (baseline) koruyan yumuşak hap vurgular */
        code.ar, span.ar-badge {{
            position: relative !important;
            overflow: visible !important;
            font-family: 'Amiri', 'Traditional Arabic', serif;
            font-size: 1.26em;
            font-weight: 700;
            direction: rtl;
            unicode-bidi: isolate;
            color: {c_dark};
            background: linear-gradient(180deg, #ffffff 0%, {c_pill_bg} 100%) !important;
            border: 1px solid {c_pill_border} !important;
            border-radius: 4.5px !important;
            padding: 1px 6.5px !important;
            margin: 0 1.5px !important;
            display: inline-block !important;
            vertical-align: baseline !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
            line-height: 1.26 !important;
        }}
        code.ar::after, span.ar-badge::after {{
            display: none !important;
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
            position: relative;
            overflow: visible;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 8.6pt;
            font-weight: 700;
            color: {c_dark};
            background: linear-gradient(180deg, #ffffff 0%, {c_pill_bg} 100%);
            border: 1px solid {c_pill_border};
            padding: 1.5px 7px;
            border-radius: 4.5px;
            display: inline-block;
            vertical-align: baseline;
            margin: 0 1.5px;
            line-height: 1.36;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
        }}
        .badge-tr::before, .tr-badge::before, code.tr::before {{
            display: none !important;
        }}
        .badge-tr code.ar, .tr-badge code.ar {{
            font-size: 1.24em !important;
            line-height: 1.28 !important;
            padding: 1px 6.5px 1.5px 5px !important;
            margin: 0 2px 0 0 !important;
            vertical-align: baseline !important;
        }}

        /* İkili Türkçe + Arapça Terim Kapsülü (Parantez karmaşasını önler) */
        .dual-pill {{
            position: relative;
            overflow: visible;
            display: inline-flex;
            align-items: baseline;
            vertical-align: baseline;
            border: 1px solid {c_pill_border};
            border-radius: 5px;
            background: #ffffff;
            margin: 0 2px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
            line-height: 1.34;
        }}
        .dual-pill::before {{
            display: none !important;
        }}
        .dual-pill-tr {{
            font-size: 8.55pt;
            font-weight: 700;
            color: {c_dark};
            padding: 1.5px 6.5px;
            border-radius: 4px 0 0 4px;
            background: linear-gradient(180deg, #ffffff 0%, {c_pill_bg} 100%);
        }}
        .dual-pill-ar {{
            border-left: 1px solid {c_pill_border};
            border-radius: 0 4px 4px 0;
            background: {c_bg_tint};
            padding: 1px 7px 1px 7px;
        }}
        .dual-pill-ar code.ar {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
            font-size: 1.28em !important;
            line-height: 1.28 !important;
        }}
        .dual-pill-ar code.ar::after {{
            display: none !important;
        }}

        .ar-paren {{
            color: #64748b;
            font-weight: 400;
            font-size: 0.92em;
            margin: 0 1px;
        }}

        .ar-paren-group {{
            display: inline-block;
            overflow: visible;
            white-space: nowrap;
        }}

        .badge-sinav {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            background-color: #fef2f2;
            color: #991b1b;
            border: 1px solid #fecaca;
            padding: 1.5px 7px;
            border-radius: 4.5px;
            font-size: 7.5pt;
            font-weight: 800;
            margin-right: 5px;
            vertical-align: baseline;
            line-height: 1.35;
        }}

        .badge-hoca {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            background-color: #fffbeb;
            color: #b45309;
            border: 1px solid #fde68a;
            padding: 1.5px 7px;
            border-radius: 4.5px;
            font-size: 7.5pt;
            font-weight: 800;
            margin-right: 5px;
            vertical-align: baseline;
            line-height: 1.35;
        }}

        .ar-quote {{
            position: relative;
            overflow: visible;
            unicode-bidi: isolate;
            display: inline-block;
            vertical-align: baseline;
            padding: 1.5px 8px;
            background: linear-gradient(180deg, #ffffff 0%, {c_bg_tint} 100%);
            border-radius: 5px;
            border: 1px solid {c_border};
            margin: 2px 0;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
        }}
        .ar-quote::after {{
            display: none !important;
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
        .nass-arabic-text code.ar::after, .nass-ar code.ar::after,
        .nass-arabic-text .ar-quote::after, .nass-ar .ar-quote::after {{
            display: none !important;
        }}

        .ar-quote bdi.ar {{
            font-family: 'Amiri', 'Traditional Arabic', serif;
            font-size: 1.34em;
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

        /* ÜNİTE BANNER'LARI (Çok katmanlı degrade + geometrik filigran + altın kesme şerit) */
        .unit-banner-container {{
            break-before: page;
            page-break-before: always;
            margin-top: 0;
            margin-bottom: 14px;
        }}

        .unit-banner-container.first-unit {{
            break-before: avoid;
            page-break-before: avoid;
            margin-top: 0;
            margin-bottom: 11px;
        }}

        .unit-banner-inner {{
            position: relative;
            overflow: hidden;
            background: linear-gradient(135deg, {c_deep} 0%, {c_dark} 26%, {theme_hex} 75%, {c_mid} 100%);
            color: #ffffff;
            padding: 11px 16px 12px 18px;
            border-radius: 9px;
            border: 1px solid {c_dark};
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.12);
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .unit-banner-inner::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 5px;
            background: linear-gradient(180deg, {c_gold_bright} 0%, {c_gold} 100%);
            z-index: 2;
        }}
        .unit-banner-inner::after {{
            content: "";
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 2.5px;
            background: linear-gradient(90deg, {c_gold_bright} 0%, {c_gold} 45%, rgba(230, 195, 110, 0.22) 100%);
            z-index: 2;
        }}

        .unit-watermark {{
            position: absolute;
            right: -12px;
            top: 50%;
            transform: translateY(-50%);
            width: 108px;
            height: 108px;
            color: #ffffff;
            opacity: 0.09;
            pointer-events: none;
            z-index: 0;
        }}

        .unit-icon-box {{
            position: relative;
            z-index: 1;
            width: 34px;
            height: 34px;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.12);
            border: 1px solid rgba(230, 195, 110, 0.55);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.18);
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}

        .unit-title-wrap {{
            position: relative;
            z-index: 1;
            flex: 1;
            min-width: 0;
        }}

        .unit-title {{
            font-family: Georgia, "DejaVu Serif", "Liberation Serif", serif;
            font-size: 13.2pt;
            font-weight: 700;
            margin: 0;
            color: #ffffff;
            letter-spacing: -0.15px;
            line-height: 1.24;
        }}

        .unit-meta-pill {{
            position: relative;
            z-index: 1;
            flex-shrink: 0;
            font-size: 7.7pt;
            font-weight: 700;
            letter-spacing: 0.4px;
            color: #fef3c7;
            background: rgba(0, 0, 0, 0.22);
            border: 1px solid rgba(230, 195, 110, 0.52);
            padding: 3.5px 9px;
            border-radius: 999px;
            white-space: nowrap;
        }}

        /* BAŞLIKLAR (H2 Serif + İkili Çizgi; H3 Degrade Şerit + Altın Yıldız) */
        h2 {{
            position: relative;
            font-family: Georgia, "DejaVu Serif", "Liberation Serif", serif;
            font-size: 11.4pt;
            font-weight: 700;
            color: {c_dark};
            margin-top: 14px;
            margin-bottom: 6px;
            padding-bottom: 4.5px;
            border-bottom: 1.5px solid {c_border};
            break-inside: avoid !important;
            page-break-inside: avoid !important;
            break-after: avoid !important;
            page-break-after: avoid !important;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 6px;
        }}
        h2::after {{
            content: "";
            position: absolute;
            left: 0;
            bottom: -1.5px;
            width: 48px;
            height: 2.2px;
            background: linear-gradient(90deg, {theme_hex} 0%, {c_gold} 100%);
        }}

        .h2-badge {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, {c_dark} 0%, {theme_hex} 100%);
            color: #ffffff;
            font-size: 8.2pt;
            font-weight: 800;
            letter-spacing: 0.5px;
            padding: 2px 8px;
            border-radius: 4.5px;
            border-bottom: 1.8px solid {c_gold_bright};
            display: inline-block;
            vertical-align: middle;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.14);
        }}

        h3.h3-styled {{
            position: relative;
            overflow: hidden;
            font-size: 10.0pt;
            font-weight: 700;
            color: {c_dark};
            margin-top: 12px;
            margin-bottom: 6px;
            padding: 4px 10px 4px 12px;
            background: linear-gradient(90deg, {c_bg_tint} 0%, rgba(255, 255, 255, 0) 88%);
            border-radius: 5px;
            display: flex;
            align-items: center;
            gap: 7px;
            break-after: avoid !important;
            page-break-after: avoid !important;
        }}
        h3.h3-styled::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3.5px;
            background: linear-gradient(180deg, {c_gold} 0%, {theme_hex} 100%);
        }}

        .h3-diamond {{
            color: {c_gold};
            display: inline-flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}
        .h3-diamond svg {{
            width: 10px;
            height: 10px;
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
            padding-left: 7px;
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
            color: {c_dark};
            font-size: 1.01em;
            display: inline-block;
            margin-bottom: 1.5px;
        }}

        /* TABLOLAR (Çok sayfalı bölünmede temiz kenarlık, degrade başlık, belirgin zebra & iri Arapça) */
        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 8px 0 11px 0;
            font-size: 8.85pt;
            line-height: 1.42;
            break-inside: auto;
            page-break-inside: auto;
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
            background: linear-gradient(135deg, {c_dark} 0%, {theme_hex} 100%);
            color: #ffffff;
            font-weight: 700;
            text-align: left;
            padding: 6.5px 9.5px;
            border-top: 1px solid {c_dark};
            border-right: 1px solid rgba(255, 255, 255, 0.14);
            border-bottom: 2.5px solid {c_gold};
            font-size: 8.85pt;
            letter-spacing: 0.25px;
        }}
        th:first-child {{
            border-left: 1px solid {c_dark};
            border-top-left-radius: 7px;
        }}
        th:last-child {{
            border-right: 1px solid {c_dark};
            border-top-right-radius: 7px;
        }}

        th[align="center"], td[align="center"] {{
            text-align: center;
        }}

        td {{
            padding: 5.5px 9.5px;
            border-right: 1px solid #e2e8f0;
            border-bottom: 1px solid #e2e8f0;
            vertical-align: top;
            background-color: #ffffff;
        }}
        td:first-child {{
            border-left: 1px solid {c_border};
        }}
        td:last-child {{
            border-right: 1px solid {c_border};
        }}
        tbody tr:last-child td {{
            border-bottom: 1px solid {c_border};
        }}
        tbody tr:last-child td:first-child {{
            border-bottom-left-radius: 7px;
        }}
        tbody tr:last-child td:last-child {{
            border-bottom-right-radius: 7px;
        }}

        td:first-child strong {{
            color: {c_dark};
            font-weight: 700;
        }}
        td:first-child strong:has(> .ar), td .ar, td code.ar {{
            font-size: 1.32em !important;
        }}
        .td-ar-term {{
            font-family: 'Amiri', 'Traditional Arabic', serif;
            font-size: 1.50em;
            font-weight: 700;
            color: {c_dark};
            direction: rtl;
            unicode-bidi: isolate;
            display: inline-block;
            line-height: 1.48;
        }}

        tbody tr:nth-child(even) td {{
            background-color: {c_bg_end};
        }}

        /* CALLOUT KUTULARI (Köşe bükülmesi olmayan şeritli kutular) */
        blockquote.callout {{
            position: relative;
            overflow: hidden;
            margin: 9px 0;
            padding: 9px 14px 9px 16px;
            border-radius: 7px;
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            font-size: 9.5pt;
            line-height: 1.54;
            break-inside: avoid;
            page-break-inside: avoid;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
        }}
        blockquote.callout::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4.5px;
            background: {theme_hex};
        }}

        blockquote.callout-nass {{
            position: relative;
            overflow: hidden;
            background: {c_bg_tint};
            border: 1px solid {c_border};
            border-radius: 7px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
            padding: 9px 15px 9px 17px;
            margin: 8px 0;
            break-inside: avoid;
            page-break-inside: avoid;
            direction: ltr;
            text-align: left;
        }}
        blockquote.callout-nass::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4.5px;
            background: {theme_hex};
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
            font-size: 1.32em;
            line-height: 1.75;
            direction: rtl;
            unicode-bidi: isolate;
            color: {c_dark};
            text-align: center;
            display: block;
            margin-bottom: 5px;
            font-weight: 700;
        }}

        blockquote.callout-pinned, div.callout.callout-pinned {{
            position: relative;
            overflow: hidden;
            background: linear-gradient(180deg, #fffdf6 0%, #fef9eb 100%);
            border: 1px solid #f3d08a;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(217, 119, 6, 0.08);
            padding: 9px 14px 9px 17px;
            margin: 8px 0;
            break-inside: avoid;
            page-break-inside: avoid;
        }}
        blockquote.callout-pinned::before, div.callout.callout-pinned::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4.5px;
            background: linear-gradient(180deg, #f59e0b 0%, #b45309 100%);
        }}

        .pinned-header {{
            margin-bottom: 5px;
            padding-bottom: 4px;
            border-bottom: 1px dashed #f3d08a;
        }}

        .pinned-tag {{
            background-color: #fef3c7;
            color: #92400e;
            font-size: 7.5pt;
            font-weight: 800;
            letter-spacing: 0.6px;
            padding: 2px 8px;
            border-radius: 4px;
            border: 1px solid #fcd34d;
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }}

        blockquote.callout-pinned strong {{
            color: #9a3412;
        }}

        /* NASS LEVHALARI (Mushaf/Hadis çerçeveli, ferah harekeli hat, numaralı meal satırları) */
        .nass-board {{
            position: relative;
            overflow: hidden;
            background: linear-gradient(180deg, {c_bg_tint} 0%, #ffffff 100%);
            border: 1px solid {c_border};
            border-radius: 9px;
            padding: 0;
            margin: 8px 0;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
            break-inside: avoid;
            page-break-inside: avoid;
        }}
        .nass-board::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4.5px;
            background: linear-gradient(180deg, {c_dark} 0%, {theme_hex} 100%);
            z-index: 1;
        }}

        .nass-board.gold-accent {{
            background: linear-gradient(180deg, {c_gold_bg} 0%, #ffffff 100%);
            border-color: {c_gold_border};
        }}
        .nass-board.gold-accent::before {{
            background: linear-gradient(180deg, #f59e0b 0%, {c_gold_dark} 100%);
        }}

        .nass-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 6px 13px 6px 16px;
            background: rgba(255, 255, 255, 0.68);
            border-bottom: 1px solid {c_border};
        }}
        .nass-board.gold-accent .nass-header {{
            border-bottom-color: {c_gold_border};
        }}

        .nass-badge {{
            font-size: 7.2pt;
            font-weight: 800;
            letter-spacing: 0.55px;
            text-transform: uppercase;
            color: #ffffff;
            background: linear-gradient(135deg, {c_dark} 0%, {theme_hex} 100%);
            padding: 2px 7.5px;
            border-radius: 4px;
            display: inline-block;
        }}

        .nass-badge.gold {{
            background: linear-gradient(135deg, #b45309 0%, #d97706 100%);
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

        .nass-arabic-frame {{
            margin: 8px 13px 7px 16px;
            padding: 8px 14px;
            background: #ffffff;
            border: 1px solid {c_border};
            border-radius: 6px;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.02);
        }}
        .nass-board.gold-accent .nass-arabic-frame {{
            border-color: {c_gold_border};
        }}

        .nass-arabic-text {{
            font-family: 'Amiri', 'Traditional Arabic', serif;
            font-size: 1.44em;
            line-height: 1.90;
            color: {c_dark};
            margin: 0;
            unicode-bidi: isolate;
            font-weight: 700;
            direction: rtl;
            text-align: center;
        }}

        .nass-divider {{
            display: none;
        }}

        .nass-trans-box {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 7px 11px;
            margin: 0 13px 9px 16px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        }}

        .nass-trans-badge {{
            font-size: 7.1pt;
            font-weight: 800;
            letter-spacing: 0.5px;
            color: #92400e;
            background: #fef3c7;
            border: 1px solid #fcd34d;
            padding: 1.5px 7px;
            border-radius: 3.5px;
            display: inline-block;
            margin-bottom: 5px;
        }}

        .nass-trans-text {{
            font-size: 9.2pt;
            line-height: 1.50;
            color: #334155;
            margin: 0;
        }}

        .ayah-trans-list {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        .ayah-trans-row {{
            display: flex;
            align-items: baseline;
            gap: 7px;
            padding-bottom: 3.5px;
            border-bottom: 0.5px dashed #e2e8f0;
            font-size: 9.05pt;
            line-height: 1.46;
            color: #334155;
        }}
        .ayah-trans-row:last-child {{
            padding-bottom: 0;
            border-bottom: none;
        }}
        .ayah-num-pill {{
            flex-shrink: 0;
            font-size: 7.2pt;
            font-weight: 800;
            color: {c_dark};
            background: {c_pill_bg};
            border: 1px solid {c_pill_border};
            padding: 1px 5.5px;
            border-radius: 4px;
            white-space: nowrap;
        }}
        .ayah-body {{
            flex: 1;
        }}

        .nass-trans-text strong, .ayah-body strong {{
            color: {c_dark};
        }}

        .nass-trans-text em {{
            color: #64748b;
            font-size: 8.7pt;
        }}

        /* LÜGAT ŞERHİ 2 SÜTUNLU KART IZGARA */
        .lugat-grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4.5px 8px;
            margin: 5px 0 8px 0;
        }}
        .lugat-item {{
            position: relative;
            overflow: hidden;
            background: #ffffff;
            border: 1px solid {c_border};
            border-radius: 6px;
            padding: 4px 8px 4.5px 10px;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
            break-inside: avoid;
            page-break-inside: avoid;
        }}
        .lugat-item::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3px;
            background: linear-gradient(180deg, {theme_hex} 0%, {c_gold} 100%);
        }}
        .lugat-head {{
            margin-bottom: 1.5px;
        }}
        .lugat-def {{
            font-size: 8.45pt;
            line-height: 1.35;
            color: #334155;
        }}

        /* Kök Fiil Kartı */
        .root-verb-card {{
            position: relative;
            overflow: hidden;
            background: {c_bg_tint};
            border: 1px solid {c_border};
            border-radius: 8px;
            padding: 10px 16px 10px 18px;
            margin: 10px 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 15px;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
            break-inside: avoid;
        }}
        .root-verb-card::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4.5px;
            background: {theme_hex};
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
            position: relative;
            overflow: hidden;
            border-radius: 7px;
            padding: 9px 14px 9px 16px;
            border: 1px solid {c_border};
            background: {c_bg_tint};
            box-shadow: 0 1px 4px rgba(0,0,0,0.02);
        }}
        .usul-step::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4.5px;
            background: {theme_hex};
        }}

        .usul-step.usul-mesail {{
            background: #fffdf5;
            border-color: #fde68a;
        }}
        .usul-step.usul-mesail::before {{
            background: #d97706;
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
            margin: 10px 0;
            border-radius: 9px;
            overflow: hidden;
            border: 1px solid {c_border};
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        .ontology-main-banner {{
            background: linear-gradient(135deg, {c_dark} 0%, {theme_hex} 100%);
            color: #ffffff;
            padding: 8px 14px;
            display: flex;
            align-items: center;
            gap: 9px;
            border-bottom: 2px solid {c_gold};
        }}

        .ont-icon, .ent-icon, .dok-icon {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 24px;
            height: 24px;
            border-radius: 6px;
            background: rgba(255, 255, 255, 0.14);
            border: 1px solid rgba(230, 195, 110, 0.45);
            color: #ffffff;
            flex-shrink: 0;
        }}

        .ont-title {{
            font-size: 9.5pt;
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

        .banner-title-flex {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}

        /* Şema 3: Evrensel Kavram / Varlık Kartları */
        .hadis-entities-wrap {{
            margin: 12px 0;
            border-radius: 9px;
            overflow: hidden;
            border: 1px solid {c_border};
            box-shadow: 0 3px 10px rgba(15, 23, 42, 0.05);
            break-inside: avoid;
            page-break-inside: avoid;
            background: #ffffff;
        }}

        .entities-banner {{
            position: relative;
            background: linear-gradient(135deg, {c_deep} 0%, {c_dark} 32%, {theme_hex} 100%);
            color: #ffffff;
            padding: 8.5px 14px 8.5px 16px;
            display: flex;
            align-items: center;
            gap: 9px;
            border-bottom: 2px solid {c_gold};
        }}
        .entities-banner::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background: {c_gold_bright};
        }}

        .ent-icon {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 24px;
            height: 24px;
            border-radius: 6px;
            background: rgba(255, 255, 255, 0.14);
            border: 1px solid rgba(230, 195, 110, 0.48);
            color: #ffffff;
            flex-shrink: 0;
        }}

        .ent-title {{
            font-size: 9.4pt;
            font-weight: 800;
            letter-spacing: 0.25px;
        }}

        .entities-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 1px;
            background: {c_border};
        }}

        .entity-card {{
            position: relative;
            background: #ffffff;
            padding: 10px 11.5px;
            display: flex;
            flex-direction: column;
            box-sizing: border-box;
        }}

        .ent-card-header {{
            display: flex;
            align-items: center;
            gap: 6.5px;
            margin-bottom: 5px;
        }}

        .ent-num {{
            width: 19px;
            height: 19px;
            background: linear-gradient(135deg, {theme_hex} 0%, {c_dark} 100%);
            color: #ffffff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 7.6pt;
            font-weight: 800;
            flex-shrink: 0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.14);
        }}

        .ent-name {{
            font-size: 9.2pt;
            font-weight: 800;
            color: {c_dark};
            line-height: 1.25;
        }}

        .ent-ar {{
            font-family: 'Amiri', 'Traditional Arabic', serif;
            font-size: 1.15em;
            color: {theme_hex};
            margin-left: auto;
            font-weight: 700;
        }}

        .ent-ar-band {{
            font-family: 'Amiri', 'Traditional Arabic', serif;
            font-size: 1.38em;
            font-weight: 700;
            color: {c_dark};
            background: linear-gradient(180deg, #ffffff 0%, {c_bg_tint} 100%);
            border: 1px solid {c_border};
            border-right: 3px solid {theme_hex};
            border-radius: 5px;
            padding: 2.5px 9px;
            margin: 0 0 6px 0;
            text-align: center;
            direction: rtl;
            unicode-bidi: isolate;
            line-height: 1.5;
        }}

        .ent-tag {{
            font-size: 7.4pt;
            font-weight: 700;
            color: {c_gold_dark};
            background: {c_gold_bg};
            border: 1px solid {c_gold_border};
            padding: 2px 6.5px;
            border-radius: 4px;
            margin-bottom: 6px;
            display: inline-block;
            align-self: flex-start;
        }}

        .ent-text {{
            font-size: 8.4pt;
            line-height: 1.44;
            color: #334155;
            margin: 0;
        }}

        .ent-text em {{
            color: #991b1b;
            font-style: normal;
            font-weight: 600;
        }}

        /* Şema 4: Varlık Doktrini & İkili Mukayese Kartları */
        .doktrin-compare-wrap {{
            margin: 12px 0;
            border-radius: 9px;
            overflow: hidden;
            border: 1px solid {c_border};
            box-shadow: 0 3px 10px rgba(15, 23, 42, 0.05);
            break-inside: avoid;
            page-break-inside: avoid;
            background: #ffffff;
        }}

        .doktrin-banner {{
            position: relative;
            background: linear-gradient(135deg, {c_deep} 0%, {c_dark} 32%, {theme_hex} 100%);
            color: #ffffff;
            padding: 8.5px 14px 8.5px 16px;
            display: flex;
            align-items: center;
            gap: 9px;
            border-bottom: 2px solid {c_gold};
        }}
        .doktrin-banner::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background: {c_gold_bright};
        }}

        .dok-icon {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 24px;
            height: 24px;
            border-radius: 6px;
            background: rgba(255, 255, 255, 0.14);
            border: 1px solid rgba(230, 195, 110, 0.48);
            color: #ffffff;
            flex-shrink: 0;
        }}

        .dok-title {{
            font-size: 9.4pt;
            font-weight: 800;
            letter-spacing: 0.25px;
        }}

        .doktrin-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1px;
            background: {c_border};
        }}

        .dok-card {{
            position: relative;
            overflow: hidden;
            background: #ffffff;
            padding: 11px 14px 10px 14px;
        }}
        .dok-card::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: {theme_hex};
        }}
        .dok-card-red {{
            background: linear-gradient(180deg, #fffafa 0%, #ffffff 38%);
        }}
        .dok-card-red::before {{
            background: linear-gradient(90deg, #dc2626 0%, #f87171 100%);
        }}
        .dok-card-green {{
            background: linear-gradient(180deg, #f6fef9 0%, #ffffff 38%);
        }}
        .dok-card-green::before {{
            background: linear-gradient(90deg, #16a34a 0%, #4ade80 100%);
        }}

        .dok-card-header {{
            margin-bottom: 6px;
        }}

        .dok-pill {{
            font-size: 7.4pt;
            font-weight: 800;
            padding: 2px 7.5px;
            border-radius: 4.5px;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            margin-bottom: 3px;
        }}

        .dok-pill.green {{
            background: #dcfce7;
            color: #166534;
            border: 1px solid #86efac;
        }}

        .dok-pill.red {{
            background: #fee2e2;
            color: #991b1b;
            border: 1px solid #fca5a5;
        }}

        .dok-sub {{
            display: block;
            font-size: 7.7pt;
            color: #64748b;
            font-weight: 600;
            margin-top: 1px;
        }}

        .dok-principle {{
            font-family: 'Amiri', 'Traditional Arabic', serif;
            font-size: 1.26em;
            font-weight: 700;
            color: {c_dark};
            direction: rtl;
            margin: 5px 0 3px 0;
            padding: 3px 8px;
            background: #fafbfc;
            border: 1px solid #e2e8f0;
            border-radius: 5px;
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
            border-bottom: 1px dashed #cbd5e1;
        }}

        .dok-points {{
            margin: 0;
            padding-left: 15px;
            list-style: none;
        }}

        .dok-points li {{
            font-size: 8.45pt;
            line-height: 1.44;
            color: #334155;
            margin-bottom: 4.5px;
            position: relative;
        }}

        .dok-points li::before {{
            content: "◆";
            font-size: 0.72em;
            color: {theme_hex};
            position: absolute;
            left: -13px;
            top: 2px;
        }}
        .dok-card-red .dok-points li::before {{
            color: #dc2626;
        }}
        .dok-card-green .dok-points li::before {{
            color: #16a34a;
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

        /* Kelâm / Belâgat Formül ve Süreç Akış Kartları */
        .formula-card {{
            position: relative;
            overflow: hidden;
            margin: 10px 0;
            padding: 9px 12px 9px 15px;
            background: linear-gradient(135deg, {c_bg_tint} 0%, #ffffff 100%);
            border: 1px solid {c_border};
            border-radius: 7px;
            display: flex;
            align-items: stretch;
            justify-content: center;
            gap: 9px;
            font-size: 9.0pt;
            font-weight: 700;
            color: {c_dark};
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
            break-inside: avoid;
            page-break-inside: avoid;
            flex-wrap: nowrap;
        }}
        .formula-card::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4.5px;
            background: linear-gradient(180deg, {theme_hex} 0%, {c_gold} 100%);
        }}

        .formula-flow {{
            margin: 7px 0;
            padding: 7px 10px;
            background: #ffffff;
            border: 1px solid {c_border};
            border-radius: 7px;
            display: flex;
            align-items: stretch;
            justify-content: center;
            gap: 8px;
            box-shadow: 0 1px 4px rgba(15, 23, 42, 0.03);
            break-inside: avoid;
            page-break-inside: avoid;
            flex-wrap: nowrap;
        }}

        .flow-node {{
            flex: 1 1 0;
            min-width: 0;
            padding: 6px 10px;
            border-radius: 6px;
            font-size: 8.4pt;
            font-weight: 700;
            line-height: 1.44;
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            color: #334155;
            display: block;
            text-align: center;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
        }}

        .flow-node.origin {{
            background: linear-gradient(180deg, #ffffff 0%, {c_bg_tint} 100%);
            border-color: {c_border};
            color: {c_dark};
        }}

        .flow-node.stage {{
            background: linear-gradient(180deg, #fffdf5 0%, #fef3c7 100%);
            border-color: #f5d076;
            color: #92400e;
        }}

        .flow-node.target {{
            background: linear-gradient(180deg, #f8fffb 0%, #dcfce7 100%);
            border-color: #86efac;
            color: #166534;
        }}

        .flow-arrow {{
            align-self: center;
            flex-shrink: 0;
            min-width: 26px;
            height: 24px;
            padding: 0 7px;
            border-radius: 999px;
            background: linear-gradient(135deg, {theme_hex} 0%, {c_dark} 100%);
            color: #ffffff;
            border: 1px solid {c_gold};
            font-size: 7.5pt;
            font-weight: 800;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 1px 4px rgba(15, 23, 42, 0.12);
        }}

        /* --- EVRENSEL PEDAGOJİK MATERYAL KÜTÜPHANESİ --- */

        /* 1. Hiyerarşik Değerler & Kademeler Piramidi (Yamuk kademeler + bütünleşik yan açıklama panelleri) */
        .pyramid-panel {{
            margin: 10px 0 12px 0;
            padding: 11px 13px;
            background: linear-gradient(180deg, #ffffff 0%, {c_bg_end} 100%);
            border: 1px solid {c_border};
            border-radius: 9px;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
            display: flex;
            flex-direction: column;
            gap: 5px;
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        .pyr-row {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0;
        }}
        .pyramid-with-desc .pyr-row {{
            display: grid;
            grid-template-columns: 310px 14px 1fr;
            align-items: center;
        }}

        .pyr-wedge-col {{
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .pyr-wedge {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            gap: 2px;
            box-sizing: border-box;
            line-height: 1.25;
        }}

        .pyr-wedge-top {{
            width: 78%;
            padding: 6px 18px 5px 18px;
            background: linear-gradient(135deg, {c_deep} 0%, {theme_hex} 100%);
            color: #ffffff;
            clip-path: polygon(9% 0%, 91% 0%, 100% 100%, 0% 100%);
            filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.14));
        }}

        .pyr-wedge-middle {{
            width: 90%;
            padding: 6px 20px 5.5px 20px;
            background: linear-gradient(135deg, #fdf3d7 0%, #f9e3ad 100%);
            color: {c_dark};
            clip-path: polygon(6% 0%, 94% 0%, 100% 100%, 0% 100%);
            filter: drop-shadow(0 1px 2px rgba(138, 98, 18, 0.14));
        }}

        .pyr-wedge-base {{
            width: 100%;
            padding: 6.5px 22px 6px 22px;
            background: linear-gradient(135deg, {c_pill_bg} 0%, #e9edf3 100%);
            color: {c_dark};
            clip-path: polygon(4% 0%, 96% 0%, 100% 100%, 0% 100%);
            filter: drop-shadow(0 1px 2px rgba(15, 23, 42, 0.10));
        }}

        .pyr-wedge code.ar {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 2px !important;
            margin: 0 !important;
            font-size: 1.22em !important;
        }}
        .pyr-wedge code.ar::after {{
            display: none !important;
        }}
        .pyr-wedge-top code.ar, .pyr-wedge-top bdi.ar {{
            color: #fff8e6 !important;
        }}

        .pyr-leader {{
            height: 2px;
            background: linear-gradient(90deg, {c_gold} 0%, {c_border} 100%);
            position: relative;
        }}
        .pyr-leader::after {{
            content: "";
            position: absolute;
            right: -2px;
            top: 50%;
            transform: translateY(-50%);
            width: 5px;
            height: 5px;
            border-radius: 50%;
            background: {c_gold};
        }}

        .pyr-desc-card {{
            position: relative;
            overflow: hidden;
            background: #ffffff;
            border: 1px solid {c_border};
            border-radius: 6px;
            padding: 6.5px 10px 6.5px 12px;
            font-size: 8.2pt;
            line-height: 1.40;
            color: #334155;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
        }}
        .pyr-desc-card::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3.5px;
            background: {theme_hex};
        }}
        .pyr-desc-middle::before {{
            background: {c_gold};
        }}
        .pyr-desc-base::before {{
            background: #64748b;
        }}

        .concept-pyramid {{
            margin: 8px auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
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
        }}

        .pyramid-tier.base {{
            width: 96%;
            background: #ffffff;
            color: #334155;
            border-color: #cbd5e1;
        }}

        .pyr-badge {{
            font-size: 6.9pt;
            font-weight: 800;
            padding: 1px 6px;
            border-radius: 3.5px;
            text-transform: uppercase;
            letter-spacing: 0.25px;
        }}

        .pyr-badge.gold {{ background: #ffffff; color: {c_gold_dark}; border: 1px solid {c_gold}; }}
        .pyr-badge.purple {{ background: {theme_hex}; color: #ffffff; border: 1px solid {c_dark}; }}
        .pyr-badge.white {{ background: rgba(255, 255, 255, 0.22); color: #ffffff; border: 1px solid rgba(255, 255, 255, 0.45); }}

        .pyr-title {{
            font-size: 8.35pt;
            font-weight: 800;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1px;
            line-height: 1.25;
        }}
        .pyr-tr {{
            display: block;
        }}
        .pyr-ar {{
            display: block;
            font-size: 1.12em;
            margin-top: 1px;
        }}

        .pyr-desc {{
            font-size: 8.1pt;
            color: inherit;
            opacity: 0.92;
        }}

        /* 2. Döngüsel / Çevrimsel Süreç Modeli (İbn Haldun, İletişim, Çevrim) */
        .cycle-flow-wrap {{
            margin: 12px 0;
            border-radius: 9px;
            overflow: hidden;
            border: 1px solid {c_border};
            box-shadow: 0 3px 10px rgba(15, 23, 42, 0.05);
            break-inside: avoid;
            page-break-inside: avoid;
            background: #ffffff;
        }}

        .cycle-banner {{
            position: relative;
            background: linear-gradient(135deg, {c_deep} 0%, {c_dark} 32%, {theme_hex} 100%);
            color: #ffffff;
            padding: 8.5px 14px 8.5px 16px;
            display: flex;
            align-items: center;
            gap: 9px;
            border-bottom: 2px solid {c_gold};
            font-size: 9.4pt;
            font-weight: 800;
        }}
        .cycle-banner::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background: {c_gold_bright};
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
            background: linear-gradient(180deg, #ffffff 0%, {c_bg_tint} 100%);
            border: 1px solid {c_border};
            border-radius: 6px;
            display: flex;
            flex-direction: column;
            box-sizing: border-box;
        }}

        .cycle-step-num {{
            width: 19px;
            height: 19px;
            border-radius: 50%;
            background: linear-gradient(135deg, {theme_hex} 0%, {c_dark} 100%);
            color: #ffffff;
            font-size: 7.6pt;
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
            line-height: 1.38;
            color: #475569;
        }}

        .cycle-arrow {{
            display: flex;
            align-items: center;
            color: {theme_hex};
            font-size: 11pt;
            font-weight: 800;
        }}

        /* 3. 2x2 Eksen Matrisi (Liderlik / Disiplin Stilleri / Edebî Tesir) */
        .axis-matrix-2x2 {{
            margin: 12px 0;
            border-radius: 9px;
            overflow: hidden;
            border: 1px solid {c_border};
            box-shadow: 0 3px 10px rgba(15, 23, 42, 0.05);
            break-inside: avoid;
            page-break-inside: avoid;
            background: #ffffff;
        }}

        .axis-banner {{
            position: relative;
            background: linear-gradient(135deg, {c_deep} 0%, {c_dark} 32%, {theme_hex} 100%);
            color: #ffffff;
            padding: 8.5px 14px 8.5px 16px;
            display: flex;
            align-items: center;
            gap: 9px;
            border-bottom: 2px solid {c_gold};
            font-size: 9.4pt;
            font-weight: 800;
        }}
        .axis-banner::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background: {c_gold_bright};
        }}

        .axis-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1px;
            background: {c_border};
        }}

        .axis-cell {{
            position: relative;
            overflow: hidden;
            background: #ffffff;
            padding: 10px 12px 10px 14px;
            box-sizing: border-box;
        }}
        .axis-cell::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3.5px;
            background: {theme_hex};
        }}
        .axis-cell-v1 {{
            background: linear-gradient(180deg, #ffffff 0%, {c_bg_tint} 100%);
        }}
        .axis-cell-v1::before {{ background: {theme_hex}; }}
        .axis-cell-v2 {{
            background: linear-gradient(180deg, #ffffff 0%, #fdf8ec 100%);
        }}
        .axis-cell-v2::before {{ background: {c_gold}; }}
        .axis-cell-v3 {{
            background: linear-gradient(180deg, #ffffff 0%, #f4faf7 100%);
        }}
        .axis-cell-v3::before {{ background: #2e7d5b; }}
        .axis-cell-v4 {{
            background: linear-gradient(180deg, #ffffff 0%, #f6f8fb 100%);
        }}
        .axis-cell-v4::before {{ background: #475569; }}

        .axis-cell.highlight {{
            background: #f0fdf4;
        }}

        .axis-cell-badge {{
            font-size: 7.2pt;
            font-weight: 800;
            padding: 1.5px 6.5px;
            border-radius: 4px;
            display: inline-block;
            margin-bottom: 4px;
            background: {c_pill_bg};
            color: {c_dark};
            border: 1px solid {c_pill_border};
        }}

        .axis-cell-badge.green {{ background: #dcfce7; color: #166534; border: 1px solid #86efac; }}
        .axis-cell-badge.red {{ background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; }}
        .axis-cell-badge.amber {{ background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }}
        .axis-cell-badge.gray {{ background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }}

        .axis-cell-title {{
            font-size: 9.1pt;
            font-weight: 800;
            color: {c_dark};
            margin-bottom: 3.5px;
        }}

        .axis-cell-desc {{
            font-size: 8.35pt;
            line-height: 1.42;
            color: #334155;
        }}

        /* 4. İsnad Akış Şeridi (Hadis III ve Tefsir Râvi Zincirleri) */
        .isnad-flow-strip {{
            position: relative;
            overflow: hidden;
            margin: 8px 0;
            padding: 8px 12px 8px 14px;
            background: linear-gradient(135deg, {c_bg_tint} 0%, #ffffff 100%);
            border: 1px solid {c_border};
            border-radius: 7px;
            display: flex;
            align-items: center;
            gap: 6px;
            flex-wrap: wrap;
            box-shadow: 0 1px 4px rgba(15, 23, 42, 0.03);
            break-inside: avoid;
            page-break-inside: avoid;
        }}
        .isnad-flow-strip::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4.5px;
            background: {theme_hex};
        }}

        .isnad-node {{
            padding: 3.5px 8px;
            border-radius: 4.5px;
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

        /* 5. Tarihsel Dönemler Zaman Çizelgesi (Kronoloji Rayı + Odak Dönem Vurgusu) */
        .timeline-bar {{
            position: relative;
            margin: 10px 0 12px 0;
            padding: 10px 10px 10px 10px;
            background: linear-gradient(180deg, #ffffff 0%, {c_bg_end} 100%);
            border: 1px solid {c_border};
            border-radius: 9px;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        .timeline-rail {{
            position: absolute;
            top: 19px;
            left: 34px;
            right: 34px;
            height: 2.5px;
            background: linear-gradient(90deg, {c_border} 0%, {c_gold} 35%, {theme_hex} 65%, {c_border} 100%);
            z-index: 0;
        }}

        .timeline-nodes-row {{
            position: relative;
            z-index: 1;
            display: flex;
            align-items: stretch;
            gap: 5px;
        }}

        .timeline-dot-row {{
            display: flex;
            justify-content: center;
            margin-top: -15px;
            margin-bottom: 5px;
        }}

        .timeline-dot {{
            width: 11px;
            height: 11px;
            border-radius: 50%;
            background: #ffffff;
            border: 2.5px solid {theme_hex};
            box-shadow: 0 0 0 2px #ffffff;
        }}

        .timeline-node {{
            position: relative;
            flex: 1 1 0;
            min-width: 0;
            background: #ffffff;
            border: 1px solid {c_border};
            border-top: 3px solid {theme_hex};
            border-radius: 6px;
            padding: 8px 8px 7px 8px;
            margin-top: 9px;
            box-sizing: border-box;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
        }}

        .timeline-node.timeline-node-active {{
            background: linear-gradient(180deg, {c_gold_bg} 0%, #ffffff 100%) !important;
            border: 1.5px solid {c_gold} !important;
            border-top: 3.5px solid {c_gold_dark} !important;
            box-shadow: 0 3px 9px rgba(196, 154, 69, 0.16);
        }}
        .timeline-node-active .timeline-dot {{
            background: {c_gold_dark};
            border-color: {c_gold_bright};
            width: 13px;
            height: 13px;
            margin-top: -1px;
        }}

        .timeline-focus-pill {{
            display: inline-block;
            font-size: 6.2pt;
            font-weight: 800;
            letter-spacing: 0.4px;
            color: #ffffff;
            background: linear-gradient(135deg, {c_gold_dark} 0%, {c_gold} 100%);
            padding: 1px 5px;
            border-radius: 3px;
            margin-bottom: 3px;
        }}

        .timeline-connector {{
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            margin-top: 9px;
        }}

        .timeline-arrow {{
            width: 15px;
            height: 15px;
            border-radius: 50%;
            background: {c_bg_tint};
            border: 1px solid {c_border};
            color: {theme_hex};
            font-size: 7.5pt;
            font-weight: 800;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }}

        .timeline-date {{
            font-size: 6.9pt;
            font-weight: 800;
            color: {c_gold_dark};
            text-transform: uppercase;
            letter-spacing: 0.2px;
            margin-bottom: 2px;
        }}

        .timeline-title {{
            font-size: 8.6pt;
            font-weight: 800;
            color: {c_dark};
            margin-bottom: 2.5px;
            line-height: 1.25;
        }}

        .timeline-desc {{
            font-size: 7.75pt;
            line-height: 1.36;
            color: #475569;
        }}

        /* 6. Evrensel Kavram Matrisi (2'li, 3'lü, 4'lü) ve Doktrin Uyumluluğu */
        .entity-matrix-wrap {{
            margin: 12px 0;
            border-radius: 9px;
            overflow: hidden;
            border: 1px solid {c_border};
            box-shadow: 0 3px 10px rgba(15, 23, 42, 0.05);
            break-inside: avoid;
            page-break-inside: avoid;
            background: #ffffff;
        }}

        .doctrine-compare-wrap {{
            margin: 12px 0;
            border-radius: 9px;
            overflow: hidden;
            border: 1px solid {c_border};
            box-shadow: 0 3px 10px rgba(15, 23, 42, 0.05);
            break-inside: avoid;
            page-break-inside: avoid;
            background: #ffffff;
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

        /* 8. Hiyerarşik Ağaç Şeması (Çok kollu SVG bağlantı ağacı + dikey alt kartlar) */
        .tree-diagram-wrap {{
            margin: 12px 0;
            border-radius: 9px;
            overflow: hidden;
            border: 1px solid {c_border};
            box-shadow: 0 3px 10px rgba(15, 23, 42, 0.05);
            break-inside: avoid;
            page-break-inside: avoid;
            background: #ffffff;
        }}

        .tree-diagram-banner {{
            position: relative;
            background: linear-gradient(135deg, {c_deep} 0%, {c_dark} 32%, {theme_hex} 100%);
            color: #ffffff;
            padding: 8.5px 14px 8.5px 16px;
            font-size: 9.4pt;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 8px;
            border-bottom: 2px solid {c_gold};
        }}
        .tree-diagram-banner::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background: {c_gold_bright};
        }}

        .tree-body {{
            padding: 12px 13px 13px 13px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0;
            background: linear-gradient(180deg, #ffffff 0%, {c_bg_end} 100%);
        }}

        .tree-root-node {{
            background: linear-gradient(180deg, #ffffff 0%, {c_pill_bg} 100%);
            border: 1.5px solid {theme_hex};
            border-bottom: 2.5px solid {c_gold};
            border-radius: 7px;
            padding: 6px 18px;
            font-size: 9.2pt;
            font-weight: 800;
            color: {c_dark};
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.06);
            text-align: center;
        }}

        .tree-connector-down {{
            width: 2px;
            height: 10px;
            background: {theme_hex};
        }}

        .tree-svg-connector {{
            width: 100%;
            height: 26px;
            display: block;
            margin: 0;
            padding: 0;
        }}
        .tree-svg-connector svg {{
            width: 100%;
            height: 26px;
            display: block;
        }}
        .tree-svg-connector line {{
            stroke: {theme_hex};
            stroke-width: 1.8;
            stroke-linecap: round;
        }}
        .tree-svg-arrow {{
            fill: {c_gold_dark};
        }}

        .tree-main-branches {{
            display: flex;
            justify-content: space-between;
            width: 100%;
            gap: 9px;
            align-items: stretch;
        }}
        .tree-main-branches.tree-cols-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }}
        .tree-main-branches.tree-cols-3 {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 9px;
        }}
        .tree-main-branches.tree-cols-4 {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 7px;
        }}

        .tree-main-branch {{
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: stretch;
            gap: 6.5px;
            background: #ffffff;
            border: 1px solid {c_border};
            border-radius: 7px;
            padding: 8px 8.5px;
            box-shadow: 0 1px 4px rgba(15, 23, 42, 0.03);
        }}

        .tree-branch-header {{
            width: 100%;
            text-align: center;
            padding: 5px 7px;
            border-radius: 5px;
            font-size: 8.5pt;
            font-weight: 800;
            color: #ffffff;
            background: linear-gradient(135deg, {c_dark} 0%, {theme_hex} 100%);
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.10);
        }}

        .branch-gold {{ background: #fffdf8; border-color: {c_gold_border}; }}
        .branch-gold .tree-branch-header {{
            background: linear-gradient(135deg, {c_gold_dark} 0%, {c_gold} 100%);
        }}
        .branch-sage {{ background: #f8fbfa; border-color: #b7d7c8; }}
        .branch-sage .tree-branch-header {{
            background: linear-gradient(135deg, #1b4d3e 0%, #2e7d5b 100%);
        }}
        .branch-slate {{ background: #f8fafc; border-color: #cbd5e1; }}
        .branch-slate .tree-branch-header {{
            background: linear-gradient(135deg, #334155 0%, #475569 100%);
        }}

        .tree-subnodes {{
            display: flex;
            flex-direction: column;
            gap: 5.5px;
            width: 100%;
        }}

        .tree-subnode-card {{
            position: relative;
            overflow: hidden;
            background: #ffffff;
            border: 1px solid {c_border};
            border-radius: 5.5px;
            padding: 5.5px 8px 5.5px 10px;
            text-align: left;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
        }}
        .tree-subnode-card::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3px;
            background: {theme_hex};
        }}
        .branch-gold .tree-subnode-card {{ border-color: {c_gold_border}; }}
        .branch-gold .tree-subnode-card::before {{ background: {c_gold}; }}
        .branch-sage .tree-subnode-card {{ border-color: #c5ded2; }}
        .branch-sage .tree-subnode-card::before {{ background: #2e7d5b; }}
        .branch-slate .tree-subnode-card {{ border-color: #cbd5e1; }}
        .branch-slate .tree-subnode-card::before {{ background: #475569; }}

        .tree-subnode-title {{
            font-size: 8.3pt;
            font-weight: 800;
            color: {c_dark};
            margin-bottom: 1.5px;
            line-height: 1.25;
        }}
        .tree-subnode-title code.ar {{
            font-size: 1.20em !important;
            padding: 0 5px 0.5px 4px !important;
        }}
        .tree-subnode-desc code.ar {{
            font-size: 1.24em !important;
        }}
        .tree-root-node code.ar {{
            font-size: 1.30em !important;
        }}

        .tree-subnode-desc {{
            font-size: 7.6pt;
            color: #475569;
            line-height: 1.32;
        }}

        /* --- EVRENSEL PEDAGOJİK MATERYAL KÜTÜPHANESİ BİTİŞ --- */

        .diagram-box {{
            position: relative;
            overflow: hidden;
            background-color: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 10px 14px 10px 16px;
            margin: 10px 0;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02);
            break-inside: avoid;
            page-break-inside: avoid;
            overflow-x: auto;
        }}
        .diagram-box::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4.5px;
            background: {c_gold};
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

        /* LİSTELER (Zarif elmas imler ◆ & numaralı rozetler) */
        ul {{
            margin-top: 3px;
            margin-bottom: 8px;
            padding-left: 17px;
            list-style: none;
        }}

        ul li {{
            margin-bottom: 4.5px;
            line-height: 1.52;
            position: relative;
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        ul li p, ol li p {{
            margin: 0;
            display: inline;
        }}

        ul > li::before {{
            content: "◆";
            color: {theme_hex};
            font-size: 0.72em;
            display: inline-block;
            width: 14px;
            margin-left: -14px;
            vertical-align: 1px;
        }}

        ol {{
            margin-top: 4px;
            margin-bottom: 9px;
            padding-left: 24px;
            list-style: none;
            counter-reset: ol-num;
        }}

        ol > li {{
            counter-increment: ol-num;
            position: relative;
            margin-bottom: 4px;
            line-height: 1.48;
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        ol > li::before {{
            content: counter(ol-num);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 16.5px;
            height: 16.5px;
            padding: 0 3.5px;
            margin-left: -23.5px;
            margin-right: 7px;
            border-radius: 4px;
            background: {c_pill_bg};
            border: 1px solid {c_pill_border};
            color: {theme_hex};
            font-size: 7.4pt;
            font-weight: 800;
            line-height: 1;
            vertical-align: 0.5px;
            box-sizing: border-box;
        }}

        li > ul, li > ol {{
            margin-top: 2.5px;
            margin-bottom: 3.5px;
        }}

        hr {{
            border: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent 0%, {c_border} 18%, {c_gold} 50%, {c_border} 82%, transparent 100%);
            margin: 14px 0;
        }}

        /* HADİS KARTLARI */
        .hadis-card {{
            position: relative;
            overflow: hidden;
            break-inside: avoid;
            page-break-inside: avoid;
            margin-bottom: 8px;
            background: #ffffff;
            border: 1px solid {c_border};
            border-radius: 7.5px;
            padding: 8px 12px 8px 15px;
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
        }}
        .hadis-card::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4.5px;
            background: linear-gradient(180deg, {theme_hex} 0%, {c_gold} 100%);
        }}

        .hadis-card h3.h3-styled {{
            margin-top: 0;
            margin-bottom: 5px;
            color: {theme_hex};
            font-size: 10.4pt;
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
        .isnad-note-li::before {{
            display: none !important;
        }}

        .isnad-note {{
            position: relative;
            overflow: hidden;
            background: #fdfbf7;
            border: 1px solid #ebdcd0;
            padding: 6.5px 11px 6.5px 13px;
            font-size: 8.8pt;
            color: #334155;
            margin-top: 5px;
            margin-bottom: 5px;
            border-radius: 5.5px;
            line-height: 1.46;
        }}
        .isnad-note::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3.5px;
            background: #d4af37;
        }}

        .hadis-card ul {{
            margin: 0;
            padding-left: 14px;
        }}

        /* SORU KARTLARI (KURAL 15) */
        .q-card {{
            position: relative;
            overflow: hidden;
            break-inside: avoid;
            page-break-inside: avoid;
            margin-bottom: 9px;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 7.5px;
            padding: 8px 11.5px;
            box-shadow: 0 1px 4px rgba(15, 23, 42, 0.03);
        }}

        .q-card-classic {{
            padding-left: 15px;
            background: linear-gradient(180deg, #ffffff 0%, #fafcfb 100%);
        }}
        .q-card-classic::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4.5px;
            background: linear-gradient(180deg, {theme_hex} 0%, {c_gold} 100%);
        }}

        .q-header {{
            display: flex;
            align-items: flex-start;
            gap: 8px;
            margin-bottom: 4px;
        }}

        .q-badge {{
            background: linear-gradient(135deg, {theme_hex} 0%, {c_dark} 100%);
            color: #ffffff;
            font-size: 7.8pt;
            font-weight: 800;
            padding: 2px 7px;
            border-radius: 4.5px;
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
            padding: 5.5px 9.5px;
            margin-top: 4px;
            font-size: 8.85pt;
            line-height: 1.46;
            color: #1e293b;
        }}

        .q-ans p {{
            margin: 0;
        }}

        .q-context {{
            position: relative;
            overflow: hidden;
            font-size: 9.0pt;
            line-height: 1.46;
            color: #334155;
            margin: 5px 0 7px 0;
            padding: 6px 10px 6px 13px;
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 5px;
        }}
        .q-context::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3.5px;
            background: #94a3b8;
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
                    <div style="-webkit-print-color-adjust: exact; print-color-adjust: exact; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 7.8pt; color: #475569; width: 100%; margin: 5mm 14mm 0 14mm; padding: 0 0 4.5px 0; border-bottom: 1.5px solid {c_border}; display: flex; justify-content: space-between; align-items: center;">
                        <span style="display: inline-flex; align-items: center; gap: 6px;">
                            <span style="display: inline-block; width: 10px; height: 3.5px; border-radius: 2px; background: {c_gold};"></span>
                            <span style="font-weight: 800; color: {c_dark}; letter-spacing: 0.15px;">{title_display}</span>
                        </span>
                        <span style="display: inline-flex; align-items: center; gap: 6px; font-weight: 700; color: {theme_hex}; background: {c_bg_tint}; border: 1px solid {c_pill_border}; padding: 1px 7.5px; border-radius: 999px; font-size: 7.1pt;">{sinav_label} • Okuma PDF</span>
                    </div>
                """,
                footer_template=f"""
                    <div style="-webkit-print-color-adjust: exact; print-color-adjust: exact; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 7.8pt; color: #64748b; width: 100%; margin: 0 14mm 4mm 14mm; padding: 5px 0 0 0; border-top: 1px solid {c_border}; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #64748b; font-weight: 500;">{title_display} — Ders Anlatımı &amp; İbare Şerhleri</span>
                        <span style="background: {theme_hex}; border: 1px solid {c_dark}; border-bottom: 2px solid {c_gold}; color: #ffffff; padding: 1.5px 9px; border-radius: 999px; font-weight: 800; font-size: 7.3pt; letter-spacing: 0.2px;">Sayfa <span class="pageNumber"></span> / <span class="totalPages"></span></span>
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
