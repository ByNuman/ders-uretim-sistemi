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
tools/okuma_birlestir.py — OKUMA PDF BİRLEŞTİRME MOTORU (ÇİFT TARAFLI BASKI UYUMLU)
===================================================================================
Belirli bir sınav döneminin `ders_anlatimlari/okuma pdf/` klasöründeki Okuma PDF
dosyalarını iddialı vektörel Ana Kapak, tıklanabilir İçindekiler sayfası ve her
dersin kendi resmî tema rengine/armasına sahip baskı dostu lüks Ders Kapaklarıyla
tek bir ciltte birleştirir.

Kullanım:
    python tools/okuma_birlestir.py --sinif 3 --donem 1 --sinav vize
"""

from __future__ import annotations

import argparse
import colorsys
import html
import re
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import pymupdf
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cekirdek import donem as donem_mod  # noqa: E402
from cekirdek.renk_uretici import ders_rengi, normalize_ders_adi  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


VARSAYILAN_SIRA = [
    "ISLAMFELSEFESITARIHI",
    "ISLAMMEDENIYETITARIHI",
    "SISTEMATIKKELAM",
    "SINIFYONETIMI",
    "ARAPDILIVEEDEBIYATI",
    "HADIS",
    "TURKMUTASAVVIFLAR",
    "ISLAMHUKUKU",
    "DINEGITIMI",
    "TASAVVUF",
    "TEFSIR",
]

DOSYA_DERS_ADI_HARITASI = {
    "ARAPDILIVEEDEBIYATI": ("ARAP DİLİ VE EDEBİYATI V", "Câhiliye Nesri, Hutbe ve Şiir"),
    "DINEGITIMI": ("DİN EĞİTİMİ", "İslam Eğitim Tarihi ve Din Öğretimi"),
    "ISLAMFELSEFESITARIHI": ("İSLAM FELSEFESİ TARİHİ I", "Din–Felsefe ve İlk Ekoller"),
    "ISLAMHUKUKU": ("İSLAM HUKUKU I", "Fıkıh Tarihi, Ekoller ve Ceza Hukuku"),
    "ISLAMMEDENIYETITARIHI": ("İSLAM MEDENİYETİ TARİHİ", "Medeniyet Havzaları ve Teşkilat"),
    "SINIFYONETIMI": ("SINIF YÖNETİMİ", "Sınıf Yönetimi ve Öğretim Teknikleri"),
    "SISTEMATIKKELAM": ("SİSTEMATİK KELAM I", "Usûl, Bilgi Teorisi ve Ontoloji"),
    "TASAVVUF": ("TASAVVUF I", "Zühd, Kavram Tahlili ve Bâtın İlmi"),
    "TEFSIR": ("TEFSİR III", "Hucurât Sûresi Tahlili ve Çağdaş Akımlar"),
    "HADIS": ("HADİS III", "Hadis Metinleri ve İsnad Tahlili"),
    "TURKMUTASAVVIFLAR": ("TÜRK MUTASAVVIFLAR", "Anadolu İrfan Geleneği"),
}

UNIT_EMOJIS = ("📚", "⚔️", "⚔", "📜", "💡", "🕊️", "🕊", "⚖️", "⚖", "🏛️", "🏛", "🔍", "📖", "✨")
_ROMEN_VEYA_RAKAM = {"I", "II", "III", "IV", "V", "VI", "1", "2", "3", "4", "5", "6"}
_TR_UPPER_MAP = str.maketrans({"i": "İ", "ı": "I"})
_TR_LOWER_MAP = str.maketrans({"İ": "i", "I": "ı"})
_TITLE_LOWER_WORDS = {"ve", "ile", "veya", "ya", "da", "de", "için", "b."}
_ROMAN_TOKENS = {"I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"}


def _tr_upper(s: str) -> str:
    return s.translate(_TR_UPPER_MAP).upper()


def _tr_lower(s: str) -> str:
    return s.translate(_TR_LOWER_MAP).lower()


def _tr_cap_word(w: str) -> str:
    for i, ch in enumerate(w):
        if ch.isalpha():
            return w[:i] + _tr_upper(ch) + _tr_lower(w[i + 1:])
    return w


@dataclass
class CourseEntry:
    index: int
    family: str
    pdf_path: Path
    title: str
    subtitle: str
    theme_hex: str
    theme_dark: str
    theme_tint: str
    theme_border: str
    content_pages: int
    units: list[tuple[int, str]] = field(default_factory=list)
    cover_page: int = 0
    first_content: int = 0
    last_content: int = 0
    end_blank: bool = False
    last_page: int = 0
    has_existing_cover: bool = False


def _hex_to_rgb(hex_code: str) -> tuple[int, int, int]:
    h = hex_code.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _darken(hex_code: str, factor: float = 0.72) -> str:
    r, g, b = _hex_to_rgb(hex_code)
    return f"#{int(r * factor):02x}{int(g * factor):02x}{int(b * factor):02x}"


def _hsl_tint(hex_code: str, lightness: float = 0.96, sat_factor: float = 0.80) -> str:
    r, g, b = [x / 255.0 for x in _hex_to_rgb(hex_code)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    ts = min(1.0, max(s * sat_factor, 0.35))
    tr, tg, tb = colorsys.hls_to_rgb(h, lightness, ts)
    return f"#{int(tr * 255 + 0.5):02x}{int(tg * 255 + 0.5):02x}{int(tb * 255 + 0.5):02x}"


def _aile_anahtari_stem(stem: str) -> str:
    raw = re.split(r"\s+-\s+|\(", stem, maxsplit=1)[0].strip()
    if raw.lower().startswith("tefsir"):
        return "TEFSIR"
    kelimeler = raw.replace("-", " ").split()
    while kelimeler and kelimeler[-1].upper() in _ROMEN_VEYA_RAKAM:
        kelimeler.pop()
    return normalize_ders_adi(" ".join(kelimeler))


def resolve_course_meta(name_or_stem: str, sinif: str, donem: str, sinav: str) -> tuple[str, str, str, str]:
    sinav_label = _tr_cap_word(sinav.strip()) if sinav else "Vize"
    family = _aile_anahtari_stem(name_or_stem)
    if family in DOSYA_DERS_ADI_HARITASI:
        title, topic = DOSYA_DERS_ADI_HARITASI[family]
        if family == "ARAPDILIVEEDEBIYATI" and _tr_lower(sinav_label) == "final":
            topic = "Sadru'l-İslâm ve Emevî Edebiyatı"
        subtitle = f"{sinav_label} Özeti · {topic}"
    else:
        raw_title = re.split(r"\s+-\s+|\(", name_or_stem, maxsplit=1)[0].strip()
        title = _tr_upper(raw_title)
        subtitle = f"{sinav_label} Özeti · Sınav Odaklı Konu Anlatımı"
    hex_color = ders_rengi(title, sinif, donem, sinav)
    return family, title, subtitle, hex_color


def _resolve_course_meta(pdf_path: Path, sinif: str, donem: str, sinav: str) -> tuple[str, str, str, str]:
    return resolve_course_meta(pdf_path.stem, sinif, donem, sinav)


def _format_unit_title(txt: str) -> str:
    txt = re.sub(r",([^\s])", r", \1", txt)
    txt = re.sub(r"\s+/\s*(\d)", r" / \1", txt)
    txt = re.sub(r"^(ÜNİTE|BÖLÜM|HAFTA)\s+(\d+)\s*:", lambda m: f"{m.group(2)}. {_tr_cap_word(m.group(1))}:", txt, flags=re.IGNORECASE)
    txt = re.sub(r"^(\d+\.)\s*(ÜNİTE|BÖLÜM|HAFTA)\s*:", lambda m: f"{m.group(1)} {_tr_cap_word(m.group(2))}:", txt, flags=re.IGNORECASE)

    if ":" in txt:
        prefix, body = txt.split(":", 1)
        prefix = re.sub(r"\b(ÜNİTE|BÖLÜM|HAFTA)\b", lambda m: _tr_cap_word(m.group(1)), prefix, flags=re.IGNORECASE)
    else:
        prefix, body = "", txt

    letters = [ch for ch in body if ch.isalpha()]
    upper_ratio = (sum(1 for ch in letters if ch.isupper()) / len(letters)) if letters else 0.0

    # Önce büyük/küçük oranı kontrol edilip Title Case uygulanır, ardından (s. X) -> (Ders Kitabı s. X) çevrilir
    if upper_ratio > 0.70:
        tokens = re.split(r"(\s+)", body.strip())
        out = []
        at_clause_start = True
        for tok in tokens:
            if not tok or tok.isspace():
                out.append(tok)
                continue
            core = tok.strip("()[].,:;\"'’“”")
            if core in _ROMAN_TOKENS:
                out.append(tok)
                at_clause_start = False
                continue
            low = _tr_lower(tok)
            if not at_clause_start and low.strip("(),") in _TITLE_LOWER_WORDS:
                out.append(low)
                at_clause_start = False
                continue
            parts = re.split(r"([-'’/])", tok)
            new_parts = []
            for p_idx, part in enumerate(parts):
                if p_idx == 0:
                    new_parts.append(_tr_cap_word(part))
                elif part in {"-", "'", "’", "/"}:
                    new_parts.append(part)
                else:
                    prev_sep = parts[p_idx - 1]
                    pl = _tr_lower(part)
                    if prev_sep in {"'", "’"}:
                        new_parts.append(pl)
                    elif prev_sep == "-":
                        if pl in {"i", "l"}:
                            new_parts.append(pl)
                        else:
                            new_parts.append(_tr_cap_word(part))
                    else:
                        new_parts.append(_tr_cap_word(part))
            res_tok = "".join(new_parts)
            res_tok = re.sub(r"\b(El|Er|Et|Eş|Es|Ez|En|Ed)-([A-ZÇĞİÖŞÜÂÎÛ])", lambda m: f"{_tr_lower(m.group(1))}-{m.group(2)}", res_tok)
            out.append(res_tok)
            at_clause_start = tok.endswith(("—", "-", "(", ":"))
        body_fmt = "".join(out)
    else:
        body_fmt = body.strip()

    body_fmt = re.sub(r"\(s\.\s*([^)]+)\)", r"(Ders Kitabı s. \1)", body_fmt, flags=re.IGNORECASE)
    res = f"{prefix}: {body_fmt}" if prefix else body_fmt
    return " ".join(res.split())


def _clean_unit_title(raw: str) -> str:
    txt = " ".join(raw.split())
    for ic in UNIT_EMOJIS:
        if txt.startswith(ic):
            txt = txt[len(ic):].strip()
    txt = re.sub(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+", "", txt)
    txt = re.sub(r"\(\s*[—\-–:,]*\s*", "(", txt)
    txt = re.sub(r"\s*[—\-–:,]*\s*\)", ")", txt)
    txt = re.sub(r"\(\s*\)", "", txt)
    txt = re.sub(r":\s*[—–-]+\s*", ": ", txt)
    txt = re.sub(r"\b(Hz|b)\.(?=[A-ZÇĞİÖŞÜÂÎÛ])", r"\1. ", txt)
    txt = re.sub(r"([A-ZÇĞİÖŞÜÂÎÛ])['’]N([IİUÜ])N([A-ZÇĞİÖŞÜÂÎÛ])", r"\1'N\2N \3", txt)
    txt = _format_unit_title(" ".join(txt.split()))
    if len(txt) > 125:
        txt = txt[:122].rstrip() + "..."
    return txt


def _course_svg_icon(family: str) -> str:
    """Her dersin ruhuna uygun altın aksanlı vektörel SVG amblem."""
    icons = {
        "ISLAMFELSEFESITARIHI": (
            '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="32" cy="34" r="19"/><circle cx="32" cy="34" r="13" stroke-dasharray="3 3"/>'
            '<circle cx="32" cy="11" r="3.5"/><line x1="32" y1="15" x2="32" y2="53"/><line x1="13" y1="34" x2="51" y2="34"/>'
            '<polygon points="32,20 37,34 32,48 27,34" fill="#d9b466" stroke="#d9b466" stroke-width="1"/>'
            '</svg>'
        ),
        "ISLAMMEDENIYETITARIHI": (
            '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M14 50 V30 C14 20 22 14 32 10 C42 14 50 20 50 30 V50"/>'
            '<path d="M22 50 V34 C22 27 26 23 32 20 C38 23 42 27 42 34 V50"/>'
            '<line x1="10" y1="50" x2="54" y2="50"/><line x1="32" y1="5" x2="32" y2="10"/>'
            '<circle cx="32" cy="32" r="3.2" fill="#d9b466" stroke="none"/>'
            '</svg>'
        ),
        "SISTEMATIKKELAM": (
            '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M32 9 L49 16 V32 C49 43 41 51 32 55 C23 51 15 43 15 32 V16 Z"/>'
            '<rect x="24" y="23" width="16" height="16" stroke="#d9b466" stroke-width="1.9"/>'
            '<rect x="24" y="23" width="16" height="16" transform="rotate(45 32 31)" stroke="#d9b466" stroke-width="1.9"/>'
            '</svg>'
        ),
        "SINIFYONETIMI": (
            '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<rect x="12" y="13" width="40" height="24" rx="2.5"/>'
            '<line x1="20" y1="21" x2="44" y2="21" stroke="#d9b466" stroke-width="2.2"/><line x1="20" y1="29" x2="38" y2="29"/>'
            '<circle cx="20" cy="48" r="3.5"/><circle cx="32" cy="48" r="3.5" fill="#d9b466" stroke="#d9b466"/><circle cx="44" cy="48" r="3.5"/>'
            '</svg>'
        ),
        "ARAPDILIVEEDEBIYATI": (
            '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M47 12 L22 37 L16 50 L29 44 L54 19 Z"/>'
            '<line x1="16" y1="50" x2="25" y2="41" stroke="#d9b466" stroke-width="2.3"/>'
            '<path d="M14 54 H50" stroke="#d9b466"/><circle cx="39" cy="25" r="2.2" fill="#d9b466" stroke="none"/>'
            '</svg>'
        ),
        "ISLAMHUKUKU": (
            '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<line x1="32" y1="12" x2="32" y2="51"/><line x1="20" y1="51" x2="44" y2="51"/>'
            '<line x1="14" y1="20" x2="50" y2="20" stroke="#d9b466" stroke-width="2.2"/>'
            '<path d="M14 20 L9 35 H19 Z"/><path d="M50 20 L45 35 H55 Z"/>'
            '<path d="M9 35 C9 40 19 40 19 35"/><path d="M45 35 C45 40 55 40 55 35"/>'
            '</svg>'
        ),
        "DINEGITIMI": (
            '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M32 34 V52 M32 34 C24 30 16 31 12 34 V50 C16 47 24 47 32 52 C40 47 48 47 52 50 V34 C48 31 40 30 32 34 Z"/>'
            '<path d="M32 30 V16" stroke="#d9b466"/><path d="M32 22 C32 16 40 12 44 16 C40 22 35 23 32 22 Z" fill="#d9b466" stroke="#d9b466"/>'
            '<path d="M32 26 C32 20 24 16 20 20 C24 26 29 27 32 26 Z"/>'
            '</svg>'
        ),
        "TASAVVUF": (
            '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="32" cy="32" r="20" stroke-dasharray="2.5 3"/>'
            '<path d="M32 14 C37 22 37 28 32 32 C27 28 27 22 32 14 Z"/>'
            '<path d="M32 50 C37 42 37 36 32 32 C27 36 27 42 32 50 Z"/>'
            '<path d="M14 32 C22 27 28 27 32 32 C28 37 22 37 14 32 Z"/>'
            '<path d="M50 32 C42 27 36 27 32 32 C36 37 42 37 50 32 Z"/>'
            '<circle cx="32" cy="32" r="4.5" fill="#d9b466" stroke="#d9b466"/>'
            '</svg>'
        ),
        "TEFSIR": (
            '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M32 21 V41 M32 21 C24 16 16 17 11 20 V39 C16 36 24 36 32 41 C40 36 48 36 53 39 V20 C48 17 40 16 32 21 Z"/>'
            '<path d="M18 43 L32 53 L46 43" stroke="#d9b466" stroke-width="2.2"/>'
            '<path d="M22 53 L32 45 L42 53" stroke="#d9b466" stroke-width="2.2"/>'
            '</svg>'
        ),
        "HADIS": (
            '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<rect x="16" y="13" width="32" height="38" rx="3"/>'
            '<line x1="23" y1="22" x2="41" y2="22" stroke="#d9b466" stroke-width="2.2"/>'
            '<circle cx="24" cy="31" r="2.2" fill="#d9b466" stroke="none"/>'
            '<circle cx="32" cy="31" r="2.2" fill="#d9b466" stroke="none"/>'
            '<circle cx="40" cy="31" r="2.2" fill="#d9b466" stroke="none"/>'
            '<line x1="26" y1="31" x2="30" y2="31"/><line x1="34" y1="31" x2="38" y2="31"/>'
            '<line x1="23" y1="40" x2="41" y2="40"/>'
            '</svg>'
        ),
        "TURKMUTASAVVIFLAR": (
            '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M32 51 C20 43 13 35 13 26 C13 19.5 18 15 24 15 C27.8 15 30.5 17 32 19.8 C33.5 17 36.2 15 40 15 C46 15 51 19.5 51 26 C51 35 44 43 32 51 Z"/>'
            '<path d="M32 25 V41" stroke="#d9b466" stroke-width="2.2"/>'
            '<circle cx="32" cy="32" r="3" fill="#d9b466" stroke="none"/>'
            '</svg>'
        ),
    }
    return icons.get(family, icons["TEFSIR"])


def _main_cover_emblem_svg() -> str:
    """Ana kapak için özgün İslâmî hilal ve çift minareli kubbe (külliye) arması."""
    return (
        '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.8" '
        'stroke-linecap="round" stroke-linejoin="round">'
        # Üstte zarif altın hilal
        '<path d="M35.5 7.5 A8.5 8.5 0 1 0 38.5 22.8 A6.6 6.6 0 1 1 35.5 7.5 Z" '
        'fill="#eccb7e" stroke="#eccb7e" stroke-width="1"/>'
        # Merkezi kubbe ve alem
        '<line x1="32" y1="22" x2="32" y2="26" stroke="#eccb7e"/>'
        '<path d="M21 37 C21 28 26 25.5 32 25.5 C38 25.5 43 28 43 37" '
        'fill="rgba(217,180,102,0.16)" stroke="#f3d999"/>'
        # Ana gövde ve kemerli kapı
        '<rect x="20" y="37" width="24" height="14" stroke="#f3d999"/>'
        '<path d="M28.5 51 V44 C28.5 41.2 35.5 41.2 35.5 44 V51" stroke="#eccb7e"/>'
        # Sol minare (külah ve şerefe)
        '<line x1="14" y1="51" x2="14" y2="25"/>'
        '<line x1="17" y1="51" x2="17" y2="25"/>'
        '<line x1="12.5" y1="30" x2="18.5" y2="30" stroke="#eccb7e"/>'
        '<path d="M13.5 25 L15.5 18.5 L17.5 25 Z" fill="#eccb7e" stroke="#eccb7e" stroke-width="1.2"/>'
        # Sağ minare (külah ve şerefe)
        '<line x1="47" y1="51" x2="47" y2="25"/>'
        '<line x1="50" y1="51" x2="50" y2="25"/>'
        '<line x1="45.5" y1="30" x2="51.5" y2="30" stroke="#eccb7e"/>'
        '<path d="M46.5 25 L48.5 18.5 L50.5 25 Z" fill="#eccb7e" stroke="#eccb7e" stroke-width="1.2"/>'
        # Zemin çizgisi
        '<line x1="9" y1="51" x2="55" y2="51" stroke="#eccb7e" stroke-width="2"/>'
        '</svg>'
    )


def _corner_ornament_svg(color: str) -> str:
    """Baskı dostu lüks köşe tezhip SVG süsü."""
    return (
        f'<svg viewBox="0 0 40 40" fill="none">'
        f'<path d="M2 38 V10 C2 5.6 5.6 2 10 2 H38" stroke="{color}" stroke-width="1.6"/>'
        f'<path d="M7 34 V12 C7 9.2 9.2 7 12 7 H34" stroke="#d4af5a" stroke-width="1"/>'
        f'<circle cx="10" cy="10" r="2.2" fill="#d4af5a"/>'
        f'</svg>'
    )


def _pdf_has_baski_lux_cover(doc: pymupdf.Document) -> bool:
    """Kaynak PDF zaten Baskı Dostu Lüks ders kapağı ile başlıyorsa True döner."""
    if len(doc) < 2:
        return False
    p0_txt = doc[0].get_text("text")
    return (
        "İlahiyat Çalışma Külliyatı ·" in p0_txt
        and "İÇERİK SAYFASI" in p0_txt
        and "SAYFA ARALIĞI" in p0_txt
    )


def _extract_units(doc: pymupdf.Document, start_page_idx: int = 0) -> list[tuple[int, str]]:
    units: list[tuple[int, str]] = []
    seen_titles: set[str] = set()
    unit_pat = re.compile(
        r"^(?:\d+\.\s*(?:ÜNİTE|BÖLÜM|HAFTA)|(?:ÜNİTE|BÖLÜM|HAFTA)\s*\d+|ÇÖZÜMLÜ\s+CEVAP\s+ANAHTARI)",
        re.IGNORECASE,
    )
    for idx in range(start_page_idx, len(doc)):
        page = doc[idx]
        local_content_pg = (idx - start_page_idx) + 1
        blocks = [b for b in page.get_text("dict")["blocks"] if b["type"] == 0]
        blocks.sort(key=lambda b: (round(b["bbox"][1], 1), b["bbox"][0]))
        i = 0
        while i < len(blocks):
            block = blocks[i]
            txt = " ".join("".join(span["text"] for span in line["spans"]).strip() for line in block["lines"]).strip()
            txt_norm = " ".join(txt.split())
            if not txt_norm:
                i += 1
                continue
            max_sz = max((span["size"] for line in block["lines"] for span in line["spans"]), default=0.0)
            has_emoji = any(txt_norm.startswith(ic) for ic in UNIT_EMOJIS)
            if not (has_emoji or max_sz >= 13.0):
                i += 1
                continue

            combined = txt_norm
            last_y1 = block["bbox"][3]
            if has_emoji and len(txt_norm) <= 3 and i + 1 < len(blocks):
                nxt = blocks[i + 1]
                nxt_txt = " ".join(" ".join("".join(s["text"] for s in l["spans"]).strip() for l in nxt["lines"]).split())
                if nxt_txt and nxt["bbox"][1] - block["bbox"][1] < 24:
                    combined = f"{txt_norm} {nxt_txt}"
                    last_y1 = max(last_y1, nxt["bbox"][3])
                    i += 1

            while i + 1 < len(blocks):
                nxt = blocks[i + 1]
                nxt_txt = " ".join(" ".join("".join(s["text"] for s in l["spans"]).strip() for l in nxt["lines"]).split())
                nxt_sz = max((s["size"] for l in nxt["lines"] for s in l["spans"]), default=0.0)
                if nxt_sz < 10.5 and nxt["bbox"][0] > 420 and (nxt["bbox"][1] - last_y1) < 16.0:
                    # Banner sağındaki küçük sayfa aralığı kapsülünü (s. 80 · 96) atlayıp alt satıra devam et
                    i += 1
                    continue
                if (
                    nxt_txt
                    and not any(nxt_txt.startswith(ic) for ic in UNIT_EMOJIS)
                    and not re.match(r"^\d+\.\d+", nxt_txt)
                    and (nxt["bbox"][1] - last_y1) < 10.0
                    and nxt_sz >= 12.0
                ):
                    combined = f"{combined} {nxt_txt}"
                    last_y1 = max(last_y1, nxt["bbox"][3])
                    i += 1
                else:
                    break

            cleaned = _clean_unit_title(combined)
            if unit_pat.match(cleaned) and cleaned not in seen_titles:
                seen_titles.add(cleaned)
                units.append((local_content_pg, cleaned))
            i += 1
    return units


def _collect_courses(input_dir: Path, output_path: Path, sinif: str, donem: str, sinav: str) -> list[CourseEntry]:
    pdfs = sorted(
        p for p in input_dir.glob("*.pdf")
        if p.resolve() != output_path.resolve() and not p.name.startswith("00 - ")
    )
    if not pdfs:
        raise FileNotFoundError(f"Klasörde birleştirilecek PDF bulunamadı: {input_dir}")

    temp_records = []
    for p in pdfs:
        family, title, subtitle, hex_c = _resolve_course_meta(p, sinif, donem, sinav)
        try:
            order_idx = VARSAYILAN_SIRA.index(family)
        except ValueError:
            order_idx = 999
        doc = pymupdf.open(p)
        has_cover = _pdf_has_baski_lux_cover(doc)
        start_idx = 1 if has_cover else 0
        n_pages = len(doc) - start_idx
        units = _extract_units(doc, start_page_idx=start_idx)
        doc.close()
        temp_records.append((order_idx, family, title, p, subtitle, hex_c, n_pages, units, has_cover))

    temp_records.sort(key=lambda r: (r[0], r[2]))

    courses: list[CourseEntry] = []
    for i, (_, family, title, p, subtitle, hex_c, n_pages, units, has_cover) in enumerate(temp_records, start=1):
        courses.append(
            CourseEntry(
                index=i,
                family=family,
                pdf_path=p,
                title=title,
                subtitle=subtitle,
                theme_hex=hex_c,
                theme_dark=_darken(hex_c, 0.58),
                theme_tint=_hsl_tint(hex_c, 0.96, 0.72),
                theme_border=_hsl_tint(hex_c, 0.78, 0.62),
                content_pages=n_pages,
                units=units,
                has_existing_cover=has_cover,
            )
        )
    return courses


def _assign_duplex_pages(courses: list[CourseEntry]) -> int:
    # s.1: Ana Kapak, s.2: Boş sayfa -> İlk ders s.3 (sağ sayfa) ile başlar
    cursor = 3
    for c in courses:
        assert cursor % 2 == 1, f"Ders kapağı tek sayfada başlamalıydı: {c.title} -> s.{cursor}"
        c.cover_page = cursor
        c.first_content = cursor + 1
        c.last_content = cursor + c.content_pages
        total_course_pages = 1 + c.content_pages
        if total_course_pages % 2 == 1:
            c.end_blank = True
            c.last_page = c.last_content + 1
        else:
            c.end_blank = False
            c.last_page = c.last_content
        cursor = c.last_page + 1
    total_pages = cursor - 1
    assert total_pages % 2 == 0, f"Toplam sayfa çift olmalıydı: {total_pages}"
    return total_pages


_BASE_COVER_PAGE_CSS = """
  @page { size: 210mm 297mm; margin: 0; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: "Segoe UI", "DejaVu Sans", Arial, sans-serif;
    color: #0f172a;
    background: #ffffff;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .page {
    position: relative;
    width: 210mm;
    height: 297mm;
    overflow: hidden;
    page-break-after: always;
    break-after: page;
  }
  .page:last-child { page-break-after: auto; }
"""

_COURSE_COVER_CSS = """
  /* ==================== DERS KAPAKLARI (BASKI DOSTU LÜKS) ==================== */
  .course-cover-page {
    background: #ffffff;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 18mm;
  }
  .cc-outer-frame {
    position: absolute;
    inset: 10mm;
    border: 1.4px solid #cbd5e1;
    border-radius: 3mm;
    pointer-events: none;
  }
  .cc-inner-frame {
    position: absolute;
    inset: 12.2mm;
    border: 2.5px solid #f1f5f9;
    border-radius: 2mm;
    pointer-events: none;
  }
  .cc-watermark {
    position: absolute;
    width: 148mm;
    height: 148mm;
    opacity: 0.045;
    pointer-events: none;
    z-index: 0;
  }
  .cc-corner {
    position: absolute;
    width: 12mm;
    height: 12mm;
    pointer-events: none;
    z-index: 1;
  }
  .cc-corner.tl { top: 9.2mm; left: 9.2mm; }
  .cc-corner.tr { top: 9.2mm; right: 9.2mm; transform: scaleX(-1); }
  .cc-corner.bl { bottom: 9.2mm; left: 9.2mm; transform: scaleY(-1); }
  .cc-corner.br { bottom: 9.2mm; right: 9.2mm; transform: scale(-1, -1); }

  .dc-card {
    position: relative;
    z-index: 2;
    width: 164mm;
    background: #ffffff;
    border: 1.5px solid #cbd5e1;
    border-radius: 4.5mm;
    overflow: hidden;
    box-shadow: 0 8px 28px rgba(15, 23, 42, 0.08);
  }
  .dc-hero {
    position: relative;
    padding: 10.5mm 9mm 9.5mm 9.5mm;
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 4.5mm;
    overflow: hidden;
  }
  .dc-hero-pattern {
    position: absolute;
    inset: 0;
    opacity: 0.10;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 40 40'%3E%3Ccircle cx='20' cy='20' r='12' fill='none' stroke='%23ffffff' stroke-width='0.8'/%3E%3Cpath d='M20 4 V36 M4 20 H36' stroke='%23ffffff' stroke-width='0.5'/%3E%3C/svg%3E");
    pointer-events: none;
  }
  .dc-hero-left {
    position: relative;
    z-index: 1;
    flex: 1;
    min-width: 0;
  }
  .dc-pill {
    display: inline-block;
    font-size: 7.5pt;
    font-weight: 700;
    letter-spacing: 1.4px;
    color: #f6df9f;
    border: 1px solid rgba(246, 223, 159, 0.55);
    background: rgba(0, 0, 0, 0.18);
    padding: 3.5px 10px;
    border-radius: 999px;
    margin-bottom: 3.5mm;
  }
  .dc-title {
    font-family: "Georgia", "DejaVu Serif", serif;
    font-size: 22pt;
    font-weight: 700;
    line-height: 1.18;
    color: #ffffff;
    letter-spacing: -0.2px;
  }
  .dc-sub {
    margin-top: 2.5mm;
    font-size: 9.4pt;
    color: rgba(255, 255, 255, 0.88);
    font-weight: 500;
  }
  .dc-hero-seal {
    position: relative;
    z-index: 1;
    flex-shrink: 0;
  }
  .dc-seal-ring {
    width: 24mm;
    height: 24mm;
    border-radius: 50%;
    border: 1.4px solid rgba(246, 223, 159, 0.72);
    background: rgba(0, 0, 0, 0.18);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 4mm;
    color: #ffffff;
    box-shadow: inset 0 0 0 2.5px rgba(255, 255, 255, 0.12);
  }
  .dc-seal-ring svg {
    width: 100%;
    height: 100%;
  }
  .dc-gold-bar {
    height: 2px;
    width: 100%;
    background: linear-gradient(90deg, #b88a28, #e8c772, #b88a28);
  }
  .dc-body {
    padding: 7.5mm 9.5mm 7mm 9.5mm;
  }
  .dc-metrics {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 3.5mm;
    margin-bottom: 5.5mm;
  }
  .dc-metric {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 2.4mm;
    padding: 2.8mm 3mm;
    text-align: center;
  }
  .dc-metric b {
    display: block;
    font-size: 11.5pt;
    line-height: 1.2;
  }
  .dc-metric span {
    font-size: 7.3pt;
    color: #64748b;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .cc-units {
    width: 100%;
    text-align: left;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #1F3A5F;
    border-radius: 2.6mm;
    padding: 5mm 5.8mm;
  }
  .cc-units-label {
    font-size: 7.6pt;
    font-weight: 800;
    letter-spacing: 1.1px;
    margin-bottom: 2.8mm;
  }
  .cc-unit-item {
    display: flex;
    align-items: baseline;
    gap: 7px;
    font-size: 8.6pt;
    line-height: 1.42;
    color: #1e293b;
    padding: 1.75mm 0;
    border-bottom: 0.5px dashed rgba(148, 163, 184, 0.45);
  }
  .cc-unit-item:last-child { border-bottom: none; }
  .cc-unit-dot {
    width: 5.5px;
    height: 5.5px;
    border-radius: 50%;
    flex-shrink: 0;
    transform: translateY(-1px);
  }
  .cc-unit-title { flex: 1; }
  .cc-unit-pg {
    font-weight: 700;
    font-size: 8.2pt;
    flex-shrink: 0;
    margin-left: 6px;
  }
  .dc-card-foot {
    margin-top: 5mm;
    padding-top: 3mm;
    border-top: 1px solid #e2e8f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 7.8pt;
    color: #64748b;
  }
  .dc-foot-tag {
    font-weight: 800;
    letter-spacing: 0.8px;
  }
  .edge-tab {
    position: absolute;
    right: 0;
    width: 12.5mm;
    height: 20mm;
    padding-left: 1.5mm;
    padding-right: 4.5mm;
    border-radius: 3.5mm 0 0 3.5mm;
    border-left: 2px solid #e8c772;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    font-size: 9pt;
    font-weight: 800;
    box-shadow: -2px 2px 8px rgba(0, 0, 0, 0.14);
    z-index: 3;
  }
  .cc-page-top {
    position: absolute;
    top: 15.5mm;
    font-size: 7.6pt;
    font-weight: 700;
    letter-spacing: 1.4px;
    opacity: 0.72;
    text-transform: uppercase;
  }
  .cc-page-foot {
    position: absolute;
    bottom: 14mm;
    font-size: 7.8pt;
    color: #64748b;
    letter-spacing: 0.5px;
  }
"""


def render_course_cover_section_html(
    *,
    family: str,
    title: str,
    subtitle: str,
    theme_hex: str,
    theme_dark: str,
    theme_tint: str,
    theme_border: str,
    content_pages: int,
    units: list[tuple[int, str]],
    cover_page: int,
    first_content_page: int,
    last_content_page: int,
    donem_etiket: str,
    sinav_upper: str,
    course_index: int | None = None,
    total_courses: int | None = None,
) -> str:
    """Seçenek 1 (Baskı Dostu Lüks) tekil veya birleşik ders kapağı HTML bölümü üretir."""
    svg_icon = _course_svg_icon(family)
    corner = _corner_ornament_svg(theme_hex)
    idx_display = course_index if course_index is not None else 1
    tab_top_mm = 26 + (idx_display - 1) * 26

    if course_index is not None and total_courses is not None:
        top_caption = f"{donem_etiket} · BÖLÜM {course_index:02d} / {total_courses:02d}"
        hero_pill = f"DERS {course_index:02d} / {total_courses:02d} · {sinav_upper} SINAV HAZIRLIĞI"
        edge_label = f"{course_index:02d}"
    else:
        top_caption = f"{donem_etiket} · OKUMA PDF ÇALIŞMA KİTAPÇIĞI"
        hero_pill = f"OKUMA PDF · {sinav_upper} SINAV HAZIRLIĞI"
        edge_label = "01"

    units_list_html = ""
    if units:
        items = []
        for local_pg, utitle in units[:8]:
            target_pg = first_content_page + local_pg - 1
            items.append(
                f'<div class="cc-unit-item">'
                f'<span class="cc-unit-dot" style="background:{theme_hex};"></span>'
                f'<span class="cc-unit-title">{html.escape(utitle)}</span>'
                f'<span class="cc-unit-pg" style="color:{theme_dark};">s. {target_pg}</span>'
                f'</div>'
            )
        units_list_html = f"""
        <div class="cc-units" style="background: {theme_tint}; border-color: {theme_border}; border-left-color: {theme_hex};">
          <div class="cc-units-label" style="color: {theme_dark};">BÖLÜM İÇERİĞİ VE SAYFA PLANI</div>
          {''.join(items)}
        </div>
        """

    return f"""
    <section class="page course-cover-page">
      <div class="cc-outer-frame" style="border-color: {theme_border};"></div>
      <div class="cc-inner-frame" style="border-color: {theme_tint};"></div>
      <div class="cc-watermark" style="color: {theme_hex};">
        <svg viewBox="0 0 200 200" fill="none" stroke="currentColor" stroke-width="1">
          <circle cx="100" cy="100" r="88"/><circle cx="100" cy="100" r="68" stroke-dasharray="4 4"/>
          <path d="M100 20 C130 55 130 145 100 180 C70 145 70 55 100 20 Z"/>
          <path d="M20 100 C55 70 145 70 180 100 C145 130 55 130 20 100 Z"/>
          <circle cx="100" cy="100" r="24"/>
        </svg>
      </div>
      <div class="cc-corner tl">{corner}</div>
      <div class="cc-corner tr">{corner}</div>
      <div class="cc-corner bl">{corner}</div>
      <div class="cc-corner br">{corner}</div>

      <div class="cc-page-top" style="color:{theme_dark};">{html.escape(top_caption)}</div>

      <div class="edge-tab" style="top: {tab_top_mm}mm; background: linear-gradient(180deg, {theme_hex}, {theme_dark});">
        <span>{edge_label}</span>
      </div>

      <div class="dc-card" style="border-color: {theme_border};">
        <div class="dc-hero" style="background: linear-gradient(135deg, {theme_dark} 0%, {theme_hex} 100%);">
          <div class="dc-hero-pattern"></div>
          <div class="dc-hero-left">
            <div class="dc-pill">{html.escape(hero_pill)}</div>
            <h1 class="dc-title">{html.escape(title)}</h1>
            <div class="dc-sub">{html.escape(subtitle)}</div>
          </div>
          <div class="dc-hero-seal">
            <div class="dc-seal-ring">{svg_icon}</div>
          </div>
        </div>
        <div class="dc-gold-bar"></div>

        <div class="dc-body">
          <div class="dc-metrics">
            <div class="dc-metric" style="border-color:{theme_border};">
              <b style="color:{theme_dark};">{len(units) if units else '—'}</b>
              <span>Ünite / Konu</span>
            </div>
            <div class="dc-metric" style="border-color:{theme_border};">
              <b style="color:{theme_dark};">{content_pages}</b>
              <span>İçerik Sayfası</span>
            </div>
            <div class="dc-metric" style="border-color:{theme_border};">
              <b style="color:{theme_dark};">s. {cover_page}–{last_content_page}</b>
              <span>Sayfa Aralığı</span>
            </div>
          </div>
          {units_list_html}
          <div class="dc-card-foot">
            <span>Çift taraflı baskı uyumlu · Konulara tıklayarak doğrudan gidebilirsiniz</span>
            <span class="dc-foot-tag" style="color:{theme_dark};">SAYFA {cover_page}</span>
          </div>
        </div>
      </div>

      <div class="cc-page-foot">İlahiyat Çalışma Külliyatı · {html.escape(title)}</div>
    </section>
    """


def render_single_course_cover_html(
    *,
    course_name: str,
    theme_hex: str,
    content_pages: int,
    units: list[tuple[int, str]],
    sinif: str,
    donem: str,
    sinav: str,
) -> str:
    """Tekil Okuma PDF için Baskı Dostu Lüks ders kapağı tam HTML belgesi üretir."""
    family, title, subtitle, resolved_hex = resolve_course_meta(course_name, sinif, donem, sinav)
    use_hex = theme_hex or resolved_hex
    donem_etiket = _tr_upper(f"{sinif}. SINIF · {donem}. DÖNEM · {sinav}")
    sinav_upper = _tr_upper(sinav or "VİZE")
    section = render_course_cover_section_html(
        family=family,
        title=title,
        subtitle=subtitle,
        theme_hex=use_hex,
        theme_dark=_darken(use_hex, 0.58),
        theme_tint=_hsl_tint(use_hex, 0.96, 0.72),
        theme_border=_hsl_tint(use_hex, 0.78, 0.62),
        content_pages=content_pages,
        units=units,
        cover_page=1,
        first_content_page=2,
        last_content_page=1 + content_pages,
        donem_etiket=donem_etiket,
        sinav_upper=sinav_upper,
    )
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<style>
{_BASE_COVER_PAGE_CSS}
{_COURSE_COVER_CSS}
</style>
</head>
<body>
{section}
</body>
</html>
"""


def attach_course_cover_links(
    cov_page: pymupdf.Page,
    units: list[tuple[int, str]],
    first_content_page: int,
) -> None:
    """Ders kapağındaki ünite satırlarına tıklanabilir LINK_GOTO bağlantıları ekler."""
    if not units:
        return
    unit_rects: list[tuple[int, pymupdf.Rect]] = []
    for local_pg, _utitle in units[:8]:
        target_pg = first_content_page + local_pg - 1
        matches = [r for r in cov_page.search_for(f"s. {target_pg}") if r.y0 > 340]
        if matches:
            unit_rects.append((target_pg, matches[-1]))
    for idx_u, (target_pg, r) in enumerate(unit_rects):
        max_y1 = r.y1 + 14
        if idx_u + 1 < len(unit_rects):
            max_y1 = min(max_y1, unit_rects[idx_u + 1][1].y0 - 2)
        cov_page.insert_link({
            "kind": pymupdf.LINK_GOTO,
            "from": pymupdf.Rect(88, r.y0 - 4, 508, max_y1),
            "page": target_pg - 1,
        })


def _render_front_and_covers_html(courses: list[CourseEntry], total_pages: int, donem_etiket: str, sinav_upper: str) -> str:
    total_content = sum(c.content_pages for c in courses)
    total_courses = len(courses)
    total_units = sum(len(c.units) for c in courses)

    # Ana kapaktaki ders renkli içerik matrisi
    main_course_pills = []
    for c in courses:
        ucnt_txt = f"{len(c.units)} ünite · " if c.units else ""
        main_course_pills.append(f"""
        <div class="mc-pill">
          <span class="mc-num-badge" style="background:{c.theme_hex};">{c.index:02d}</span>
          <div class="mc-text">
            <div class="mc-name">{html.escape(c.title)}</div>
            <div class="mc-meta">{ucnt_txt}{c.content_pages} sf · s. {c.cover_page}–{c.last_content}</div>
          </div>
        </div>
        """)

    # Ders kapakları (Baskı Dostu Lüks — paylaşılan şablon)
    course_covers_html = [
        render_course_cover_section_html(
            family=c.family,
            title=c.title,
            subtitle=c.subtitle,
            theme_hex=c.theme_hex,
            theme_dark=c.theme_dark,
            theme_tint=c.theme_tint,
            theme_border=c.theme_border,
            content_pages=c.content_pages,
            units=c.units,
            cover_page=c.cover_page,
            first_content_page=c.first_content,
            last_content_page=c.last_content,
            donem_etiket=donem_etiket,
            sinav_upper=sinav_upper,
            course_index=c.index,
            total_courses=total_courses,
        )
        for c in courses
    ]

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<style>
{_BASE_COVER_PAGE_CSS}
  /* ==================== 1. ANA KAPAK (TAM VEKTÖREL PRESTİJ) ==================== */
  .main-cover {{
    background:
      radial-gradient(circle at 82% 14%, rgba(217, 180, 102, 0.18), transparent 36%),
      radial-gradient(circle at 18% 88%, rgba(45, 92, 168, 0.28), transparent 44%),
      linear-gradient(155deg, #081224 0%, #112447 52%, #1b3869 100%);
    color: #ffffff;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 17mm 16mm 15mm 16mm;
  }}
  .mc-bg-pattern {{
    position: absolute;
    inset: 0;
    opacity: 0.06;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='56' height='56' viewBox='0 0 56 56'%3E%3Cg fill='none' stroke='%23d9b466' stroke-width='0.9'%3E%3Cpath d='M28 6 C38 16 38 40 28 50 C18 40 18 16 28 6 Z'/%3E%3Ccircle cx='28' cy='28' r='20' stroke-opacity='0.6'/%3E%3Ccircle cx='28' cy='28' r='5'/%3E%3C/g%3E%3C/svg%3E");
    pointer-events: none;
  }}
  .mc-border-outer {{
    position: absolute;
    inset: 8mm;
    border: 1.2px solid rgba(217, 180, 102, 0.55);
    pointer-events: none;
  }}
  .mc-border-inner {{
    position: absolute;
    inset: 10.5mm;
    border: 0.6px solid rgba(255, 255, 255, 0.22);
    pointer-events: none;
  }}
  .mc-corner {{
    position: absolute;
    width: 11mm;
    height: 11mm;
    pointer-events: none;
  }}
  .mc-corner.tl {{ top: 8mm; left: 8mm; }}
  .mc-corner.tr {{ top: 8mm; right: 8mm; transform: scaleX(-1); }}
  .mc-corner.bl {{ bottom: 8mm; left: 8mm; transform: scaleY(-1); }}
  .mc-corner.br {{ bottom: 8mm; right: 8mm; transform: scale(-1, -1); }}

  .mc-top {{
    position: relative;
    z-index: 2;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 2mm;
  }}
  .mc-kicker {{
    display: inline-block;
    font-size: 8.2pt;
    font-weight: 700;
    letter-spacing: 1.9px;
    color: #f3d999;
    border: 1px solid rgba(217, 180, 102, 0.6);
    background: rgba(217, 180, 102, 0.10);
    padding: 5px 14px;
    border-radius: 999px;
  }}
  .mc-emblem {{
    position: relative;
    width: 28mm;
    height: 28mm;
    border-radius: 50%;
    border: 1.2px solid rgba(217, 180, 102, 0.65);
    background: radial-gradient(circle at 35% 30%, rgba(217, 180, 102, 0.20), rgba(8, 18, 36, 0.65));
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .mc-emblem::before {{
    content: "";
    position: absolute;
    inset: 2.5mm;
    border-radius: 50%;
    border: 1px dashed rgba(217, 180, 102, 0.45);
  }}
  .mc-emblem svg {{
    width: 17mm;
    height: 17mm;
    color: #f3d999;
  }}

  .mc-hero {{
    position: relative;
    z-index: 2;
    text-align: center;
    padding: 2mm 6mm 0 6mm;
  }}
  .mc-pretitle {{
    font-size: 9.5pt;
    font-weight: 700;
    letter-spacing: 3px;
    color: #d9b466;
    text-transform: uppercase;
    margin-bottom: 3mm;
  }}
  .mc-title {{
    font-family: "Georgia", "DejaVu Serif", serif;
    font-size: 33pt;
    font-weight: 700;
    line-height: 1.12;
    letter-spacing: -0.3px;
    color: #ffffff;
    text-shadow: 0 3px 16px rgba(0, 0, 0, 0.35);
  }}
  .mc-title .gold {{
    color: #eccb7e;
  }}
  .mc-rule {{
    width: 44mm;
    height: 2.5px;
    background: linear-gradient(90deg, transparent, #d9b466, transparent);
    margin: 5mm auto 4.5mm auto;
  }}
  .mc-subtitle {{
    font-size: 10.6pt;
    line-height: 1.5;
    color: rgba(255, 255, 255, 0.88);
    max-width: 144mm;
    margin: 0 auto;
  }}

  /* Ana Kapak Merkez Vitrin Kartı */
  .mc-showcase {{
    position: relative;
    z-index: 2;
    background: rgba(255, 255, 255, 0.96);
    color: #0f172a;
    border-radius: 4mm;
    border: 1.5px solid #d9b466;
    padding: 6mm 7mm 5.5mm 7mm;
    box-shadow: 0 12px 34px rgba(0, 0, 0, 0.35);
  }}
  .mc-showcase-head {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1.5px solid #e2e8f0;
    padding-bottom: 3mm;
    margin-bottom: 4.5mm;
  }}
  .mc-showcase-title {{
    font-size: 8.6pt;
    font-weight: 800;
    letter-spacing: 1.3px;
    color: #112447;
    text-transform: uppercase;
  }}
  .mc-showcase-tag {{
    font-size: 7.8pt;
    font-weight: 700;
    color: #8b6914;
    background: #fef8e7;
    border: 1px solid #e6cb81;
    padding: 2px 9px;
    border-radius: 999px;
  }}
  .mc-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 3mm;
  }}
  .mc-pill {{
    display: flex;
    align-items: center;
    gap: 2.2mm;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 2.2mm;
    padding: 2.4mm 2.5mm;
  }}
  .mc-num-badge {{
    width: 5.5mm;
    height: 8.8mm;
    border-radius: 1.4mm;
    flex-shrink: 0;
    color: #ffffff;
    font-size: 7.5pt;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .mc-text {{ min-width: 0; }}
  .mc-name {{
    font-size: 7.35pt;
    font-weight: 800;
    letter-spacing: -0.15px;
    color: #0f172a;
    line-height: 1.2;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}
  .mc-meta {{
    font-size: 6.9pt;
    color: #64748b;
    margin-top: 0.6mm;
    white-space: nowrap;
  }}

  .mc-stats-row {{
    margin-top: 4.5mm;
    padding-top: 4mm;
    border-top: 1px dashed #cbd5e1;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 3mm;
  }}
  .mc-stat {{
    background: #f1f5f9;
    border-radius: 2mm;
    padding: 2.6mm 2mm;
    text-align: center;
    border-bottom: 2.5px solid #112447;
  }}
  .mc-stat b {{
    display: block;
    font-size: 13.5pt;
    color: #112447;
    line-height: 1.15;
  }}
  .mc-stat span {{
    font-size: 7pt;
    font-weight: 700;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}

  .mc-bottom {{
    position: relative;
    z-index: 2;
  }}
  .mc-features {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(217, 180, 102, 0.40);
    border-radius: 2.5mm;
    padding: 3mm 6mm;
    font-size: 8.4pt;
    color: #f8fafc;
    font-weight: 600;
  }}
  .mc-features .chk {{
    color: #eccb7e;
    font-weight: 800;
    margin-right: 4px;
  }}
  .mc-foot-bar {{
    margin-top: 3.5mm;
    display: flex;
    justify-content: space-between;
    font-size: 7.8pt;
    color: rgba(255, 255, 255, 0.68);
    letter-spacing: 0.8px;
    text-transform: uppercase;
  }}

{_COURSE_COVER_CSS}
</style>
</head>
<body>

<!-- SAYFA 1: ANA KAPAK -->
<section class="page main-cover">
  <div class="mc-bg-pattern"></div>
  <div class="mc-border-outer"></div>
  <div class="mc-border-inner"></div>
  <div class="mc-corner tl">{_corner_ornament_svg("#d9b466")}</div>
  <div class="mc-corner tr">{_corner_ornament_svg("#d9b466")}</div>
  <div class="mc-corner bl">{_corner_ornament_svg("#d9b466")}</div>
  <div class="mc-corner br">{_corner_ornament_svg("#d9b466")}</div>

  <div class="mc-top">
    <div class="mc-kicker">{html.escape(donem_etiket)} · İLAHİYAT OKUMA KİTABI</div>
    <div class="mc-emblem">{_main_cover_emblem_svg()}</div>
  </div>

  <div class="mc-hero">
    <div class="mc-pretitle">İlahiyat Fakültesi · Sınav Odaklı Okuma Külliyatı</div>
    <h1 class="mc-title">{html.escape(sinav_upper)} <span class="gold">SINAVI</span><br>HAZIRLIK KİTABI</h1>
    <div class="mc-rule"></div>
    <p class="mc-subtitle">
      Dönem içindeki <strong>{total_courses} dersin</strong> eksiksiz konu özetleri, ünite başlıkları,
      Arapça ibare şerhleri ve sınav uyarıları tek ciltte toplanmıştır.
    </p>
  </div>

  <div class="mc-showcase">
    <div class="mc-showcase-head">
      <div class="mc-showcase-title">Kitap İçindeki Dersler ve Sayfa Aralığı</div>
      <div class="mc-showcase-tag">TOPLAM {total_units} ÜNİTE · TAM METİN</div>
    </div>
    <div class="mc-grid">
      {''.join(main_course_pills)}
    </div>
    <div class="mc-stats-row">
      <div class="mc-stat"><b>{total_courses}</b><span>Ders</span></div>
      <div class="mc-stat"><b>{total_units}</b><span>Ünite / Bölüm</span></div>
      <div class="mc-stat"><b>{total_content}</b><span>İçerik Sayfası</span></div>
      <div class="mc-stat"><b>{total_pages}</b><span>Baskı Sayfası</span></div>
    </div>
  </div>

  <div class="mc-bottom">
    <div class="mc-features">
      <span><span class="chk">✓</span>Ünite Bazlı Tam Anlatım</span>
      <span><span class="chk">✓</span>İbare &amp; Kavram Şerhleri</span>
      <span><span class="chk">✓</span>Çift Taraflı Baskı &amp; Renkli Sekme</span>
    </div>
    <div class="mc-foot-bar">
      <span>İlahiyat Çalışma Külliyatı · Paylaşım Baskısı</span>
      <span>A4 Duplex Baskı Standardı · {total_pages} Sayfa</span>
    </div>
  </div>
</section>

<!-- SAYFA 2..N: DERS KAPAKLARI -->
{''.join(course_covers_html)}

</body>
</html>
"""


def _render_footers_overlay_html(footer_specs: list[tuple[int, str, str, str, str, int, int, int]]) -> str:
    pages_html = []
    for global_pg, title, hex_c, tint_c, border_c, local_pg, local_total, book_total in footer_specs:
        is_odd = (global_pg % 2 == 1)
        left_part = (
            f'<span class="f-course" style="color:{hex_c};">{html.escape(title)}</span>'
            f'<span class="f-local"> · Ders İçi {local_pg}/{local_total}</span>'
        )
        right_part = (
            f'<span class="f-pill" style="background:{tint_c}; border-color:{border_c}; color:{hex_c};">'
            f'Sayfa {global_pg} / {book_total}</span>'
        )
        content = f"<div>{left_part}</div><div>{right_part}</div>" if is_odd else f"<div>{right_part}</div><div>{left_part}</div>"
        pages_html.append(f'<div class="fpage"><div class="fbar">{content}</div></div>')

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<style>
  @page {{ size: 210mm 297mm; margin: 0; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: "Segoe UI", "DejaVu Sans", Arial, sans-serif;
    background: transparent;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  .fpage {{
    position: relative;
    width: 210mm;
    height: 297mm;
    page-break-after: always;
    break-after: page;
  }}
  .fpage:last-child {{ page-break-after: auto; }}
  .fbar {{
    position: absolute;
    left: 14mm;
    right: 14mm;
    bottom: 6.5mm;
    border-top: 0.75px solid #cbd5e1;
    padding-top: 3.5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 7.9pt;
  }}
  .f-course {{ font-weight: 700; }}
  .f-local {{ color: #64748b; font-weight: 500; }}
  .f-pill {{
    display: inline-block;
    border: 1px solid;
    padding: 1.5px 8.5px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 7.9pt;
  }}
</style>
</head>
<body>
{''.join(pages_html)}
</body>
</html>
"""


def _html_to_pdf(html_str: str, pdf_path: Path, work_dir: Path, name: str):
    html_file = work_dir / f"{name}.html"
    html_file.write_text(html_str, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file:///{str(html_file.resolve()).replace(chr(92), '/')}", wait_until="load")
        page.evaluate("() => document.fonts.ready")
        page.pdf(path=str(pdf_path), format="A4", print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        browser.close()


def _redact_old_footer(page: pymupdf.Page):
    h = page.rect.height
    w = page.rect.width
    footer_y0 = None
    for b in page.get_text("blocks"):
        if b[1] > h - 55 and "Sayfa" in b[4]:
            footer_y0 = b[1] if footer_y0 is None else min(footer_y0, b[1])
    cut_y = (footer_y0 - 8.0) if footer_y0 is not None else (h - 38.0)
    page.add_redact_annot(pymupdf.Rect(0, cut_y, w, h), fill=(1, 1, 1))
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE)


def merge_okuma_pdfs(d: donem_mod.Donem, output_path: Path | None = None) -> Path:
    input_dir = d.root / "ders_anlatimlari" / "okuma pdf"
    if not input_dir.is_dir():
        raise FileNotFoundError(f"Okuma PDF klasörü bulunamadı: {input_dir}")

    if output_path is None:
        output_path = d.root / "ders_anlatimlari" / f"{d.sinif}. Sınıf {d.donem}. Dönem {d.sinav.capitalize()} - Birleşik Okuma Kitapçığı.pdf"

    courses = _collect_courses(input_dir, output_path, d.sinif, d.donem, d.sinav)
    total_pages = _assign_duplex_pages(courses)
    donem_etiket = _tr_upper(f"{d.sinif}. SINIF · {d.donem}. DÖNEM · {d.sinav}")

    print(f"[birleştir] Dönem: {donem_etiket}")
    print(f"[birleştir] {len(courses)} ders bulundu, çift taraflı baskı toplamı: {total_pages} sayfa")
    for c in courses:
        blank_note = " (+1 boş)" if c.end_blank else ""
        print(f"   {c.index:02d}. {c.title:30s} [{c.theme_hex}] -> s.{c.cover_page:3d}–{c.last_content:3d} ({c.content_pages:2d} sf{blank_note})")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        front_pdf_path = tmp_dir / "front_and_covers.pdf"
        footers_pdf_path = tmp_dir / "footers.pdf"

        sinav_upper = _tr_upper(d.sinav or "vize")
        front_html = _render_front_and_covers_html(courses, total_pages, donem_etiket, sinav_upper)
        _html_to_pdf(front_html, front_pdf_path, tmp_dir, "front")

        footer_specs = []
        for c in courses:
            for local_i in range(1, c.content_pages + 1):
                global_pg = c.first_content + local_i - 1
                footer_specs.append((
                    global_pg, c.title, c.theme_hex, c.theme_tint,
                    c.theme_border, local_i, c.content_pages, total_pages
                ))

        footers_html = _render_footers_overlay_html(footer_specs)
        _html_to_pdf(footers_html, footers_pdf_path, tmp_dir, "footers")

        front_doc = pymupdf.open(front_pdf_path)
        footers_doc = pymupdf.open(footers_pdf_path)
        out_doc = pymupdf.open()

        a4_w, a4_h = front_doc[0].rect.width, front_doc[0].rect.height

        # s.1: Ana Kapak
        out_doc.insert_pdf(front_doc, from_page=0, to_page=0)
        # s.2: Boş sayfa (Ana kapağın arkası)
        out_doc.new_page(width=a4_w, height=a4_h)

        footer_cursor = 0
        for c in courses:
            cover_idx_in_front = 1 + (c.index - 1)
            out_doc.insert_pdf(front_doc, from_page=cover_idx_in_front, to_page=cover_idx_in_front)

            src_doc = pymupdf.open(c.pdf_path)
            start_out_idx = len(out_doc)
            if c.has_existing_cover:
                out_doc.insert_pdf(src_doc, from_page=1)
            else:
                out_doc.insert_pdf(src_doc)
            src_doc.close()

            for offset in range(c.content_pages):
                pg = out_doc[start_out_idx + offset]
                _redact_old_footer(pg)
                pg.show_pdf_page(pg.rect, footers_doc, footer_cursor, overlay=True)
                footer_cursor += 1

            if c.end_blank:
                out_doc.new_page(width=a4_w, height=a4_h)

        assert len(out_doc) == total_pages, f"Sayfa sayısı uyuşmuyor: {len(out_doc)} != {total_pages}"

        # Ana kapaktaki 9 ders kartını tıklanabilir yap
        main_cover_page = out_doc[0]
        for c in courses:
            rects = main_cover_page.search_for(c.title)
            if rects:
                r = rects[0]
                col = (c.index - 1) % 3
                col_x0 = [64, 224, 384][col]
                col_x1 = col_x0 + 148
                main_cover_page.insert_link({
                    "kind": pymupdf.LINK_GOTO,
                    "from": pymupdf.Rect(col_x0, r.y0 - 6, col_x1, r.y1 + 16),
                    "page": c.cover_page - 1,
                })

        # Ders kapaklarındaki her ünite satırını ilgili başlangıç sayfasına tıklanabilir yap
        for c in courses:
            if not c.units:
                continue
            attach_course_cover_links(out_doc[c.cover_page - 1], c.units, c.first_content)

        toc_tree = [
            [1, "Ana Kapak", 1],
        ]
        for c in courses:
            toc_tree.append([1, f"{c.index:02d}. {c.title}", c.cover_page])
            for local_pg, utitle in c.units:
                toc_tree.append([2, utitle, c.first_content + local_pg - 1])
        out_doc.set_toc(toc_tree)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        out_doc.save(output_path, garbage=4, deflate=True)

        front_doc.close()
        footers_doc.close()
        out_doc.close()

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"✓ Birleşik Okuma PDF üretildi: {output_path} ({total_pages} sayfa, {size_mb:.2f} MB)")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Okuma PDF klasöründeki PDF'leri kapak ve içindekilerle birleştirir.")
    donem_mod.add_args(parser)
    parser.add_argument("--cikti", default=None, help="Özel çıktı PDF yolu")
    args = parser.parse_args()
    d = donem_mod.resolve(args)
    out = Path(args.cikti) if args.cikti else None
    merge_okuma_pdfs(d, out)


if __name__ == "__main__":
    main()
