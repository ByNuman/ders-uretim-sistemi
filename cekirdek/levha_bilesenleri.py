# -*- coding: utf-8 -*-
"""Modern Levha, Sened/Şema, Anlam Gruplu Kelime Çevirisi ve Ferah Mizanpaj Bileşenleri.

KRİTİK KURAL 14 kapsamında tüm derslerde (Hadis, Tefsir, Arap Dili ve Edebiyatı, Fıkıh,
Kelâm vb.) ortak kullanılabilecek vektörel SVG şema, anlam gruplu satır altı (interlinear)
kelime kartları, Bâb–Hadis bağlantılı nass levhaları, USÛL/ANLAM/DİKKAT açıklama kutuları,
Sayfa 3 okuma rehberi ve Sözlük karşılaştırma tablosu yardımcıları.
"""
from __future__ import annotations

import re

_LAFIZ_MAP = {
    "Mevsûl Tahdîs": "حَدَّثَنَا",
    "Tahdîs": "حَدَّثَنَا",
    "Tahvîl Tahdîsi": "وَحَدَّثَنَا",
    "İhbâr": "أَخْبَرَنَا",
    "İhbâr (Tekil)": "أَخْبَرَنِي",
    "An'ane": "عَنْ",
    "An‘ane": "عَنْ",
    "Semâ'": "سَمِعْتُ",
    "Enne": "أَنَّ",
    "Kāle": "قَالَ",
}

_TABAKA_NESIL_MAP = {
    "(10)": "Şeyhü’l-Buhârî · 10. Tabaka",
    "(9)": "Tebe-i Tâbiîn · 9. Tabaka",
    "(8)": "Tebe-i Tâbiîn · 8. Tabaka",
    "(7)": "Tebe-i Tâbiîn · 7. Tabaka",
    "(6)": "Tebe-i Tâbiîn · 6. Tabaka",
    "(5)": "Küçük Tâbiîn · 5. Tabaka",
    "(4)": "Orta Tâbiîn · 4. Tabaka",
    "(3)": "Orta Tâbiîn · 3. Tabaka",
    "(2)": "Büyük Tâbiîn · 2. Tabaka",
    "(1)": "Sahâbî · 1. Tabaka",
}


def _w(ar: str, tr: str, g: int = 0) -> str:
    """Kelime veya kelime öbeği modern satır altı kartı (anlam grubu tonlamalı: g=1,2,3...)."""
    tone_cls = f" tone-{((g - 1) % 3) + 1}" if g > 0 else ""
    return f'<div class="w-token{tone_cls}"><span class="w-ar">{ar}</span><span class="w-tr">{tr}</span></div>'


def _auto_group_tokens(tokens: list[str] | str) -> str:
    """Kelime birimlerini cümle ve anlam gruplarına göre hafif ton farklarıyla düzenler."""
    if isinstance(tokens, str):
        return tokens
    out = []
    grp = 1
    for t in tokens:
        if "tone-" not in t:
            t_toned = t.replace('<div class="w-token">', f'<div class="w-token tone-{((grp - 1) % 3) + 1}">', 1)
        else:
            t_toned = t
        out.append(t_toned)
        if any(p in t for p in ("،", ";", ":", "»", "«")):
            grp += 1
    return "".join(out)


def _normalize_nesil(role: str, cls: str = "") -> str:
    """Râvi/kavram kutusundaki 3. satırı standart 'Nesil ve Tabaka Bilgisi' formatına dönüştürür."""
    if cls == "merfu" or "Resûlullah" in role:
        return "Resûlullah ﷺ"
    if cls == "muellif" or "Müellif" in role:
        return "Musannif (H. 194–256)"
    if cls == "mevkuf" or "Sahâbî" in role:
        return "Sahâbî · 1. Tabaka"
    for code, nesil_str in _TABAKA_NESIL_MAP.items():
        if code in role:
            return nesil_str
    return role


def _isnad_token(ar: str, name_tr: str, role: str, hukum: str, cls: str = "", lafiz: str = "") -> dict:
    """İsnad zincirindeki tekil râvi verisi (Standart sıra: Arapça isim → Türkçe isim → Nesil bilgisi → Varsa ortak râvi/konum etiketi)."""
    if cls == "mevkuf" or hukum in ("Mevkūf Râvi", "Sahâbî Râvi"):
        hukum_display = "Sahâbî Râvi"
    elif cls == "merfu" or hukum == "MERFÛ NASS":
        hukum_display = "Merfû Nass"
    elif cls == "medar" or "MEDÂR" in hukum or "ORTAK" in hukum:
        hukum_display = "ORTAK RÂVİ · MEDÂR"
    elif cls == "muellif":
        hukum_display = "Musannif"
    else:
        hukum_display = ""

    inferred_lafiz = lafiz or _LAFIZ_MAP.get(hukum, "عَنْ")
    return {
        "ar": ar,
        "name": name_tr,
        "role": _normalize_nesil(role, cls),
        "hukum": hukum_display,
        "cls": cls,
        "lafiz": inferred_lafiz,
    }


def _svg_rich_card(
    x: float,
    y: float,
    w: float,
    h: float,
    ar: str,
    name_tr: str,
    role: str,
    hukum: str = "",
    subdesc: str = "",
    kind: str = "normal",
) -> str:
    """Standartlaştırılmış ferah SVG râvi/kavram kartı:
    Sıra: 1) Arapça isim → 2) Türkçe isim → 3) Nesil/Tabaka bilgisi → 4) Varsa Ortak Râvi / Konum etiketi.
    """
    nesil_txt = _normalize_nesil(role, kind)
    is_ortak = kind == "medar" or "ORTAK RÂVİ" in hukum.upper()

    if kind == "merfu":
        fill, stroke, sw = "#f2f8f3", "#65a875", "1.35"
        name_col = "#1b5e2b"
        p_fill, p_stroke, p_col = "#dff2e3", "#589e68", "#155224"
    elif kind == "mevkuf":
        fill, stroke, sw = "#f2f7fc", "#7aaad4", "1.35"
        name_col = "#154c75"
        p_fill, p_stroke, p_col = "#dfeefb", "#6499c7", "#10436b"
    elif is_ortak:
        fill, stroke, sw = "#fdf5e2", "#b87b14", "2.15"
        name_col = "#6d3f0b"
        p_fill, p_stroke, p_col = "#f9e3b0", "#b87b14", "#5c3305"
    elif kind == "muellif":
        fill, stroke, sw = "#f5efe6", "#b8a896", "1.35"
        name_col = "#5c3818"
        p_fill, p_stroke, p_col = "#e8dfd1", "#afa08e", "#4f2f12"
    elif kind == "teal":
        fill, stroke, sw = "#edf6f5", "#7ab3ac", "1.45"
        name_col = "#144f4a"
        p_fill, p_stroke, p_col = "#d8efec", "#569c94", "#0f423e"
    elif kind == "purple":
        fill, stroke, sw = "#f5f0f8", "#a88eb8", "1.45"
        name_col = "#51355c"
        p_fill, p_stroke, p_col = "#e9ddf0", "#9575a8", "#43294d"
    else:
        fill, stroke, sw = "#ffffff", "#cfc5b7", "1.2"
        name_col = "#5a3515"
        p_fill, p_stroke, p_col = "#f3ede3", "#c9baa6", "#5c3b1e"

    cx = x + w / 2.0
    show_pill = bool(hukum and hukum not in ("Mevsûl Tahdîs", "Tahdîs", "An‘ane", "An'ane", "İhbâr", "İhbâr (Tekil)"))

    if show_pill:
        y_ar = y + h * 0.25
        y_name = y + h * 0.47
        y_role = y + h * 0.65
        pill_w = min(w - 6.0, w * 0.93)
        pill_x = cx - pill_w / 2.0
        pill_y = y + h * 0.73
        pill_h = h * 0.22
        y_pill_txt = pill_y + pill_h * 0.74

        ar_fs = min(15.4, max(11.6, (w - 7.0) / max(1, len(ar) * 0.41)))
        name_fs = min(12.6, max(9.5, (w - 7.0) / max(1, len(name_tr) * 0.56)))
        role_fs = min(10.2, max(8.1, (w - 6.0) / max(1, len(nesil_txt) * 0.52)))
        pill_fs = min(10.0, max(7.9, (pill_w - 5.0) / max(1, len(hukum) * 0.54)))

        pill_svg = (
            f'<rect x="{pill_x:.1f}" y="{pill_y:.1f}" width="{pill_w:.1f}" height="{pill_h:.1f}" rx="3.5" fill="{p_fill}" stroke="{p_stroke}" stroke-width="0.95" />'
            f'<text x="{cx:.1f}" y="{y_pill_txt:.1f}" font-family="\'DejaVu Sans\', \'Segoe UI\', sans-serif" font-size="{pill_fs:.1f}" font-weight="700" fill="{p_col}" text-anchor="middle">{hukum}</text>'
        )
    else:
        y_ar = y + h * 0.31
        y_name = y + h * 0.59
        y_role = y + h * 0.83
        ar_fs = min(16.4, max(12.2, (w - 7.0) / max(1, len(ar) * 0.40)))
        name_fs = min(13.2, max(10.0, (w - 7.0) / max(1, len(name_tr) * 0.54)))
        role_fs = min(10.6, max(8.3, (w - 6.0) / max(1, len(nesil_txt) * 0.51)))
        pill_svg = ""

    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" />'
        f'<text x="{cx:.1f}" y="{y_ar:.1f}" font-family="\'DejaVu Sans\', \'Amiri\', serif" font-size="{ar_fs:.1f}" font-weight="700" fill="#261407" text-anchor="middle">{ar}</text>'
        f'<text x="{cx:.1f}" y="{y_name:.1f}" font-family="\'DejaVu Sans\', \'Segoe UI\', sans-serif" font-size="{name_fs:.1f}" font-weight="700" fill="{name_col}" text-anchor="middle">{name_tr}</text>'
        f'<text x="{cx:.1f}" y="{y_role:.1f}" font-family="\'DejaVu Sans\', \'Segoe UI\', sans-serif" font-size="{role_fs:.1f}" font-weight="600" fill="#5a4e42" text-anchor="middle">{nesil_txt}</text>'
        f'{pill_svg}'
    )


def _svg_lafiz_badge(cx: float, cy: float, lafiz: str, color: str = "#6d4626") -> str:
    """Bağlantı çizgisi / ok üzerinde aktarım lafzını (حَدَّثَنَا, أَخْبَرَنَا, عَنْ, سَمِعْتُ) gösteren etiket."""
    ty = cy - 4.2
    return (
        f'<text x="{cx:.1f}" y="{ty:.1f}" font-family="\'DejaVu Sans\', \'Amiri\', serif" font-size="10.5" font-weight="700" '
        f'fill="{color}" stroke="#ffffff" stroke-width="3.2" paint-order="stroke" stroke-linejoin="round" text-anchor="middle">{lafiz}</text>'
    )


def _svg_markers() -> str:
    """Açık V-ok (chevron) uçları tanımları."""
    return (
        '<defs>'
        '<marker id="chv-brown" viewBox="0 0 8 8" refX="6.5" refY="4" markerWidth="5.8" markerHeight="5.8" orient="auto">'
        '<path d="M 1.2 1.2 L 6.5 4 L 1.2 6.8" fill="none" stroke="#6d4626" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round" />'
        '</marker>'
        '<marker id="chv-teal" viewBox="0 0 8 8" refX="6.5" refY="4" markerWidth="5.8" markerHeight="5.8" orient="auto">'
        '<path d="M 1.2 1.2 L 6.5 4 L 1.2 6.8" fill="none" stroke="#1d615c" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round" />'
        '</marker>'
        '<marker id="chv-purple" viewBox="0 0 8 8" refX="6.5" refY="4" markerWidth="5.8" markerHeight="5.8" orient="auto">'
        '<path d="M 1.2 1.2 L 6.5 4 L 1.2 6.8" fill="none" stroke="#694f73" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round" />'
        '</marker>'
        '<marker id="chv-gold" viewBox="0 0 8 8" refX="6.5" refY="4" markerWidth="5.8" markerHeight="5.8" orient="auto">'
        '<path d="M 1.2 1.2 L 6.5 4 L 1.2 6.8" fill="none" stroke="#b87b14" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round" />'
        '</marker>'
        '</defs>'
    )


def _sened_legend_bar(extra_note: str = "") -> str:
    """Çok tarikli levhalara özgü 1 satırlık alt açıklama çubuğu."""
    if not extra_note:
        return ""
    return f'<div class="mod-sened-legend"><span>{extra_note}</span></div>'


def _isnad_section(badge_title: str, ar_text: str, tr_text: str, tokens: list[dict], hint: str = "Okuma rehberi: s. 3") -> str:
    """Tek kanallı senedler için standart râvi kutuları + ok üstü aktarım lafızlarıyla SVG şeması."""
    header_title = badge_title if badge_title.startswith("SENED /") else f"SENED / {badge_title}"
    all_nodes = [
        {
            "ar": "البُخَارِيُّ",
            "name": "İmam Buhârî",
            "role": "Musannif (H. 194–256)",
            "hukum": "Musannif",
            "cls": "muellif",
            "lafiz": "",
        }
    ] + list(tokens)

    n = len(all_nodes)
    total_w = 922.0
    gap = 20.0 if n <= 7 else 16.5
    box_w = (total_w - (n - 1) * gap) / n
    box_h = 80.0
    y0 = 3.0
    cy = y0 + box_h * 0.55

    svg_els = [_svg_markers()]
    for idx, nd in enumerate(all_nodes):
        x = 4.0 + idx * (box_w + gap)
        cls = nd.get("cls", "")
        kind = cls if cls in ("muellif", "medar", "mevkuf", "merfu") else "normal"
        name_str = nd["name"].replace(" (r.a.)", "")
        svg_els.append(
            _svg_rich_card(
                x,
                y0,
                box_w,
                box_h,
                ar=nd["ar"],
                name_tr=name_str,
                role=nd["role"],
                hukum=nd["hukum"],
                kind=kind,
            )
        )
        if idx < n - 1:
            x1 = x + box_w
            x2 = x1 + gap - 2.2
            mid_x = x1 + gap / 2.0
            next_lafiz = all_nodes[idx + 1].get("lafiz", "عَنْ")
            svg_els.append(
                f'<line x1="{x1:.1f}" y1="{cy:.1f}" x2="{x2:.1f}" y2="{cy:.1f}" '
                f'stroke="#6d4626" stroke-width="1.65" marker-end="url(#chv-brown)" />'
            )
            svg_els.append(_svg_lafiz_badge(mid_x, cy, next_lafiz))

    svg_html = f'<svg class="mod-tree-svg" viewBox="0 0 930 86" xmlns="http://www.w3.org/2000/svg">{"".join(svg_els)}</svg>'
    return (
        f'<div class="mod-isnad-container">'
        f'<div class="mod-isnad-header">'
        f'<div class="mod-isnad-title-box">'
        f'<span class="mod-isnad-num">1</span>'
        f'<span class="mod-isnad-title">{header_title}</span>'
        f'</div>'
        f'<span class="mod-isnad-hint">{hint}</span>'
        f'</div>'
        f'<div class="mod-sened-list">'
        f'<div class="mod-sened-row">'
        f'<span class="mod-sened-badge b-brown">1</span>'
        f'<div class="mod-sened-ar c-brown" dir="rtl">{ar_text}</div>'
        f'</div>'
        f'</div>'
        f'<div class="mod-tree-wrapper">{svg_html}</div>'
        f'</div>'
    )


def _hadis_board(title: str, tokens: list[str] | str, meal: str, ref: str = "", matn: str = "") -> str:
    """Metinler için modern '❷ METİN / Kelime kelime çeviri' (anlam grupları tonlamalı) kart levhası."""
    tokens_html = _auto_group_tokens(tokens)
    clean_meal = meal.strip()
    if not (clean_meal.startswith("«") or clean_meal.startswith('"')):
        clean_meal = f"«{clean_meal}»"

    ref_text = f"{ref} · Anlam gruplu çeviri" if ref else "Anlam gruplu çeviri (sağdan sola)"
    return (
        f'<div class="hadis-board">'
        f'<div class="hadis-head">'
        f'<div class="hadis-head-left">'
        f'<span class="mod-isnad-num">2</span>'
        f'<span class="hadis-title">METİN / {title}</span>'
        f'</div>'
        f'<span class="mod-isnad-hint">{ref_text}</span>'
        f'</div>'
        f'<div class="hadis-tokens">{tokens_html}</div>'
        f'<div class="hadis-meal">'
        f'<span class="hadis-meal-pill">BÜTÜNCÜL MEAL</span>'
        f'<div class="meal-text">{clean_meal}</div>'
        f'</div>'
        f'</div>'
    )


def _extract_ar_from_tokens(tokens: list[str]) -> str:
    ar_parts = re.findall(r'<span class="w-ar">(.*?)</span>', "".join(tokens))
    return " ".join(ar_parts)


def _nass_board(title: str, tokens: list[str], meal: str = "", note: str = "", tag: str = "", tag_cls: str = "gold") -> str:
    """Kelime kelime satır altı (interlinear) nass ve Terceme-i Bâb levhası."""
    tokens_html = _auto_group_tokens(tokens)
    is_bab = "BÂB" in tag.upper() or "BÂB" in title.upper()

    board_cls = "nass-board bab-board" if is_bab else "nass-board"
    tag_badge_cls = "bab-badge" if is_bab else tag_cls
    tag_html = f'<span class="k-badge {tag_badge_cls}">{tag}</span> ' if tag else ""
    title_cls = "k-title bab-title" if is_bab else "k-title"

    bab_full_ar_html = ""
    if is_bab:
        full_ar = _extract_ar_from_tokens(tokens)
        if full_ar:
            bab_full_ar_html = f'<span class="bab-full-ar" dir="rtl">{full_ar}</span>'

    meal_html = ""
    if meal:
        clean_meal = meal.strip()
        if not (clean_meal.startswith("«") or clean_meal.startswith('"')):
            clean_meal = f"«{clean_meal}»"
        meal_pill_cls = "meal-pill bab-meal-pill" if is_bab else "meal-pill"
        meal_label = "BÂB TERCÜMESİ" if is_bab else "TERCÜME &amp; MEAL"
        meal_html = (
            f'<div class="nass-meal{" bab-meal-row" if is_bab else ""}">'
            f'<span class="{meal_pill_cls}">{meal_label}</span>'
            f'<div class="meal-text{" bab-meal-text" if is_bab else ""}">{clean_meal}</div>'
            f'</div>'
        )

    note_html = ""
    if note:
        note_pill_cls = "note-pill bab-note-pill" if is_bab else "note-pill"
        note_label = "BÂB–HADİS BAĞLANTISI" if is_bab else "USÛL &amp; TAHLİL"
        clean_note = re.sub(r"^<b>[^<]*?([Bb]âb|[Mm]etodu|[İi]ctihadı)[^<]*?:</b>\s*", "", note).strip() if is_bab else note
        note_html = (
            f'<div class="nass-note">'
            f'<span class="{note_pill_cls}">{note_label}</span>'
            f'<div class="note-text">{clean_note}</div>'
            f'</div>'
        )

    head_left_title = "" if is_bab else f'<span class="{title_cls}">{title}</span>'
    return (
        f'<div class="{board_cls}">'
        f'<div class="nass-board-head">'
        f'<div style="display:flex;align-items:center;gap:1.2mm;min-width:0;">{tag_html}{head_left_title}</div>'
        f'{bab_full_ar_html if is_bab else "<span class=\"mod-isnad-hint\">Anlam gruplu çeviri (sağdan sola)</span>"}'
        f'</div>'
        f'<div class="nass-tokens">{tokens_html}</div>'
        f'{meal_html}'
        f'{note_html}'
        f'</div>'
    )


def _mukayese_box(title: str, items: list[str], badge: str = "USÛL · ANLAM · DİKKAT") -> str:
    """Tutarlı 'USÛL', 'ANLAM' ve 'DİKKAT' başlık biçimleriyle yapılandırılmış açıklama kutusu."""
    std_tags = [
        ("USÛL", "exp-usul"),
        ("ANLAM", "exp-anlam"),
        ("DİKKAT", "exp-dikkat"),
        ("EK NOT", "exp-usul"),
    ]
    formatted_items = []
    for idx, it in enumerate(items):
        clean_it = re.sub(r"^[•\-]\s*", "", it.strip())
        if "exp-tag" not in clean_it:
            lbl, cls = std_tags[min(idx, len(std_tags) - 1)]
            clean_it = f'<span class="exp-tag {cls}">{lbl}</span> {clean_it}'
        formatted_items.append(f'<div class="mukayese-item">{clean_it}</div>')

    items_html = "".join(formatted_items)
    return (
        f'<div class="mukayese-box">'
        f'<div class="mukayese-head"><span class="k-badge alert">{badge}</span> <span class="k-title">{title}</span></div>'
        f'{items_html}'
        f'</div>'
    )


TOC_OKUMA_REHBERI_HTML = """
<div class="levha-guide-box">
  <div class="levha-guide-head">
    <span class="levha-guide-badge">GÖRSEL OKUMA ANAHTARI</span>
    <span class="levha-guide-title">Bu Kitaptaki Sened ve Metin Levhaları Nasıl Okunur?</span>
  </div>
  <div class="levha-guide-grid">
    <div class="lg-card">
      <div class="lg-card-title"><span class="lg-num">1</span> Râvi Kutuları ve Tabaka Numaraları</div>
      <div class="lg-card-text">Her râvi kutusunda yukarıdan aşağıya <b>aynı sıra</b> izlenir: <b>Arapça İsim → Türkçe İsim → Nesil ve Tabaka No → (Varsa) Ortak Râvi Etiketi</b>. Parantez içi rakamlar İbn Hacer’in <i>Takrîbü’t-Tehzîb</i> tabakasını gösterir: <b>(1)</b> Sahâbî · <b>(2–5)</b> Büyük/Orta/Küçük Tâbiîn · <b>(6–9)</b> Tebe-i Tâbiîn · <b>(10)</b> Buhârî’nin Hocaları.</div>
    </div>
    <div class="lg-card">
      <div class="lg-card-title"><span class="lg-num">2</span> Ok Yönü ve Aktarım Lafızları</div>
      <div class="lg-card-text">Sened okları soldan sağa (<b>İmam Buhârî → ... → Hz. Peygamber ﷺ</b>) ilerler; soldaki râvi, sağdaki hocasından okun üzerindeki sîga ile nakleder: <bdi class="ar">حَدَّثَنَا / سَمِعْتُ</bdi> bizzat işitme (semâ) · <bdi class="ar">أَخْبَرَنَا / أَخْبَرَنِي</bdi> ihbâr (semâ veya hocaya arz) · <bdi class="ar">عَنْ</bdi> an‘ane (Buhârî’de <i>sübût-i likā</i> şartıyla muttasıl).</div>
    </div>
    <div class="lg-card">
      <div class="lg-card-title"><span class="lg-num">3</span> Tarîk Renkleri, Kesik Çizgi ve Ortak Râvi</div>
      <div class="lg-card-text">Çok tarîkli hadislerde her yol birleşme noktasına kadar kendi rengiyle (<span class="lg-dot dot-brown"></span><b>1. Yol</b> · <span class="lg-dot dot-teal"></span><b>2. Yol</b> · <span class="lg-dot dot-purple"></span><b>3. Yol</b>) ilerler. <b>Kesik çizgi (---)</b> sened başından râvi atlanan <i>muallak (ta‘lîk)</i> yolu; <b>kalın kehribar çerçeveli «ORTAK RÂVİ · MEDÂR»</b> kutusu ise yolların birleştiği kavşak râviyi gösterir.</div>
    </div>
    <div class="lg-card">
      <div class="lg-card-title"><span class="lg-num">4</span> Anlam Gruplu Kelime Çevirisi ve Kutular</div>
      <div class="lg-card-text"><b>❷ METİN</b> levhalarında Arapça kelime ile Türkçe karşılığı aynı küçük birimde tutulur; cümleyi oluşturan anlam grupları sağdan sola <b>hafif ton farklarıyla</b> ayrılır, altta <b>Bütüncül Meal</b> verilir. Açıklama kutuları ise <b>USÛL</b> (sened/râvi), <b>ANLAM</b> (fıkıh/kelâm) ve <b>DİKKAT</b> (sınav uyarısı) başlıklarıyla sunulur.</div>
    </div>
  </div>
</div>
"""

GLOSSARY_SENED_TABLOSU_HTML = """
<div class="gloss-compare-box">
  <div class="gloss-compare-head">
    <span class="k-badge gold">SENED OKUMA REHBERİ</span>
    <span class="gloss-compare-title">Medâr – Mütâbaat – Tahvîl – Ta‘lîk Karşılaştırma Tablosu</span>
  </div>
  <table class="ctable gloss-ctable">
    <thead>
      <tr>
        <th style="width:19%;">Usûl Kavramı</th>
        <th style="width:33%;">Seneddeki İşlevi ve Tanımı</th>
        <th style="width:22%;">Levhadaki Görsel İşareti</th>
        <th style="width:26%;">PDF’deki Hadis Örnekleri</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>Medârü’l-İsnâd (Ortak Râvi)</b></td>
        <td>Farklı tarîklerin ve sened kollarının kendisinde birleştiği müşterek kavşak râvi.</td>
        <td>Kalın kehribar çerçeve + <b>«ORTAK RÂVİ · MEDÂR»</b> rozeti</td>
        <td><b>Hadis 10:</b> eş-Şa‘bî (s. 10) · <b>Hadis 13:</b> Katâde (s. 13) · <b>Hadis 18:</b> ez-Zührî (s. 17)</td>
      </tr>
      <tr>
        <td><b>Mütâbaat (Takviye Kolu)</b></td>
        <td>Bir râvinin rivayetini, aynı şeyhten başka bir râvinin de rivayet ederek desteklemesi.</td>
        <td>Ortak râviden ayrılıp tekrar medârda birleşen 2. renkli kol</td>
        <td><b>Hadis 13:</b> Yahyâ el-Kattân → Şu‘be (1. Kol) ve Hüseyin el-Muallim (2. Kol) → Katâde (s. 13)</td>
      </tr>
      <tr>
        <td><b>Tahvîl Hâ’sı (<bdi class="ar">ح</bdi>)</b></td>
        <td>Aynı metne ait birinci senedden ikinci sened kanalına geçişi bildiren remiz.</td>
        <td>Sened sonunda <b>«(ح)»</b> harfi + <b>«2. Tarîk · Tahvîl (ح)»</b> rozeti</td>
        <td><b>Hadis 15:</b> Ya‘kûb → İbn Uleyye → Abdülazîz (ح) ve Âdem → Şu‘be → Katâde → Enes (s. 15)</td>
      </tr>
      <tr>
        <td><b>Ta‘lîk (Muallak Tarîk)</b></td>
        <td>Musannifin senedin başından râvi atlayarak cezm (<i>kāle</i>) veya temrîz ile nakli.</td>
        <td><b>Kesik çizgili ok (---)</b> + ok üzerinde <bdi class="ar">وَقَالَ</bdi> lafzı</td>
        <td><b>Hadis 10:</b> Ebû Muâviye (2. Yol) ve Abdüla‘lâ (3. Yol) → Dâvûd b. Ebî Hind (s. 10)</td>
      </tr>
    </tbody>
  </table>
</div>
"""

MODERN_LEVHA_CSS = """
/* Liste imi defansı: nass, isnad, hadis ve modern bileşenlerde çift tireyi kesin kaldır */
li:has(> .nass-board), li:has(> .isnad-box), li:has(> .hadis-board), li:has(> .mukayese-box),
li:has(> .mod-isnad-container), li:has(> .mod-hadis-board), li:has(> .bab-bar) {
  list-style: none !important;
  margin-left: -3.5mm !important;
  padding-left: 0 !important;
}
li:has(> .nass-board)::before, li:has(> .isnad-box)::before, li:has(> .hadis-board)::before, li:has(> .mukayese-box)::before,
li:has(> .mod-isnad-container)::before, li:has(> .mod-hadis-board)::before, li:has(> .bab-bar)::before {
  display: none !important;
  content: "" !important;
}

.mod-isnad-container {
  background: #ffffff;
  border: 1px solid #dfd6c7;
  border-radius: 7px;
  padding: 1.25mm 2.2mm 1.15mm 2.2mm;
  margin: 0.70mm 0 0.90mm 0;
}
.mod-isnad-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 0.55mm;
  margin-bottom: 0.75mm;
  border-bottom: 0.7px solid #ede5d8;
}
.mod-isnad-title-box {
  display: flex;
  align-items: center;
  gap: 1.6mm;
}
.mod-isnad-num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 4.2mm;
  height: 4.2mm;
  background: var(--accent, #6d4626);
  color: #ffffff;
  font-size: 6.9pt;
  font-weight: 700;
  border-radius: 50%;
  flex-shrink: 0;
}
.mod-isnad-title {
  font-size: 8.9pt;
  font-weight: 700;
  color: var(--accent-dark, #6d4626);
}
.mod-isnad-hint {
  font-size: 7.15pt;
  color: #6b5e51;
  font-weight: 500;
  white-space: nowrap;
  flex-shrink: 0;
}
.mod-sened-list {
  display: flex;
  flex-direction: column;
  gap: 0.50mm;
  margin-bottom: 0.80mm;
}
.mod-sened-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2.0mm;
  padding: 0.18mm 0.3mm;
}
.mod-sened-badge {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 3.8mm;
  height: 3.8mm;
  border-radius: 50%;
  color: #ffffff;
  font-size: 6.5pt;
  font-weight: 700;
}
.mod-sened-badge.b-brown { background: #6d4626; }
.mod-sened-badge.b-teal { background: #1d615c; }
.mod-sened-badge.b-purple { background: #694f73; }
.mod-sened-ar {
  font-family: "DejaVu Sans", "Amiri", serif;
  font-size: 1.06em;
  font-weight: 600;
  line-height: 1.32;
  direction: rtl;
  color: #6d4626;
  flex-grow: 1;
  text-align: right;
}
.mod-sened-ar.c-brown { color: #6d4626; }
.mod-sened-ar.c-teal { color: #1d615c; }
.mod-sened-ar.c-purple { color: #694f73; }
.mod-tree-wrapper {
  width: 100%;
  margin: 0.35mm 0 0.45mm 0;
}
.mod-tree-svg {
  width: 100%;
  height: auto;
  display: block;
}
.mod-sened-legend {
  margin-top: 0.50mm;
  padding: 0.50mm 1.20mm;
  background: #faf6ef;
  border: 1px solid #e3d9c8;
  border-radius: 4.5px;
  font-size: 7.20pt;
  line-height: 1.28;
  color: #4f4134;
}

.w-token {
  position: relative;
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  background: #ffffff;
  border: 1.1px solid #cfc5b7;
  border-radius: 6px;
  padding: 0.65mm 1.25mm 0.60mm 1.25mm;
  gap: 0.42mm;
  flex: 1 1 auto;
  min-width: 13mm;
  max-width: 78mm;
}
.w-token.tone-1 { background: #ffffff; border-color: #d1c6b8; }
.w-token.tone-1 .w-tr { background: #f4eee4; border-color: #d6c8b5; color: #4a2c11; }
.w-token.tone-2 { background: #f8f4ec; border-color: #c2b29b; }
.w-token.tone-2 .w-tr { background: #ebe1d1; border-color: #c5b49b; color: #3f240c; }
.w-token.tone-3 { background: #f3f7f6; border-color: #b4cac6; }
.w-token.tone-3 .w-tr { background: #dfecea; border-color: #9ec0ba; color: #15453f; }
.w-ar {
  font-family: "DejaVu Sans", "Amiri", serif;
  font-size: 1.32em !important;
  font-weight: 700;
  line-height: 1.28;
  direction: rtl;
  color: #261407;
  margin-bottom: 0.22mm;
  white-space: nowrap;
}
.w-tr {
  font-size: 8.05pt !important;
  color: #4a2c11;
  font-weight: 700;
  line-height: 1.22;
  text-align: center;
  background: #f3ede3;
  border: 0.8px solid #d5c7b4;
  border-radius: 4px;
  padding: 0.30mm 0.80mm;
  width: 100%;
}

.hadis-board, .nass-board {
  display: block;
  background: #ffffff;
  border: 1px solid #dfd6c7;
  border-radius: 7px;
  padding: 1.15mm 1.9mm 1.20mm 1.9mm;
  margin: 0.70mm 0 0.90mm 0;
}
.bab-board {
  background: #fdfbf7;
  border: 1.2px solid #d5c7b2;
}
.hadis-head, .nass-board-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 0.50mm;
  margin-bottom: 0.75mm;
  border-bottom: 0.7px solid #ede5d8;
}
.hadis-head-left {
  display: flex;
  align-items: center;
  gap: 1.6mm;
}
.hadis-title {
  color: var(--accent-dark, #6d4626);
  font-weight: 700;
  font-size: 8.7pt;
}
.bab-full-ar {
  font-family: "DejaVu Sans", "Amiri", serif;
  font-size: 1.26em !important;
  font-weight: 700;
  color: #5c3412;
  direction: rtl;
  line-height: 1.28;
}
.bab-board .w-ar { font-size: 1.16em !important; }
.bab-board .w-tr {
  font-size: 7.55pt !important;
  background: #fdf5e2;
  border-color: #dfc387;
  color: #5c3a0f;
}
.hadis-tokens, .nass-tokens {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row-reverse;
  justify-content: flex-start;
  align-items: stretch;
  gap: 0.75mm 0.95mm;
  padding: 0.15mm 0 0.30mm 0;
  margin-bottom: 0.65mm;
}
.hadis-meal, .nass-meal {
  font-size: 8.20pt;
  line-height: 1.34;
  color: #2b2118;
  background: #f4efe6;
  border: 1px solid #d5cdc0;
  border-left: 3.5px solid var(--accent, #6d4626);
  border-radius: 5px;
  padding: 0.75mm 1.35mm;
  margin-top: 0.55mm;
  display: flex;
  align-items: flex-start;
  gap: 1.5mm;
}
.hadis-meal-pill, .meal-pill {
  flex-shrink: 0;
  display: inline-block;
  background: var(--accent, #6d4626);
  color: #ffffff;
  font-weight: 700;
  font-size: 6.2pt;
  padding: 0.20mm 0.80mm;
  border-radius: 3.5px;
  margin-top: 0.15mm;
}
.nass-note {
  background: #faf6f0;
  border: 1px solid #e5ddd0;
  border-left: 3.2px solid #9a6b26;
  border-radius: 5px;
  padding: 0.65mm 1.30mm;
  font-size: 7.80pt;
  line-height: 1.30;
  margin-top: 0.50mm;
  display: flex;
  align-items: flex-start;
  gap: 1.2mm;
}
.note-pill {
  background: rgba(154, 107, 38, 0.18);
  color: #6d4626;
  font-weight: 700;
  font-size: 6.1pt;
  padding: 0.18mm 0.72mm;
  border-radius: 3.5px;
  flex-shrink: 0;
}

.mukayese-box {
  background: #fbf9f6;
  border: 1px solid #dfd4c4;
  border-left: 3.5px solid var(--accent, #6d4626);
  border-radius: 6px;
  padding: 1.10mm 1.80mm 1.05mm 1.80mm;
  margin: 0.75mm 0 0.85mm 0;
}
.mukayese-head {
  display: flex;
  align-items: center;
  gap: 1.4mm;
  margin-bottom: 0.75mm;
  border-bottom: 0.8px solid #e8dccb;
  padding-bottom: 0.50mm;
}
.mukayese-item {
  font-size: 8.05pt;
  line-height: 1.34;
  color: #2b1f14;
  padding: 0.32mm 0;
  margin-bottom: 0.48mm;
  border-bottom: 0.5px dashed #ebe1d3;
}
.mukayese-item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}
.exp-tag {
  display: inline-block;
  font-size: 6.2pt;
  font-weight: 800;
  letter-spacing: 0.3px;
  padding: 0.16mm 0.80mm;
  border-radius: 3.5px;
  margin-right: 0.80mm;
  vertical-align: 0.15mm;
  color: #ffffff;
}
.exp-usul { background: #6d4626; }
.exp-anlam { background: #1d615c; }
.exp-dikkat { background: #8c2f21; }

.ans-page-ref {
  display: inline-block;
  margin-left: 1.2mm;
  padding: 0.12mm 0.90mm;
  font-size: 7.2pt;
  font-weight: 700;
  color: var(--accent-dark, #6d4626);
  background: #f3ede3;
  border: 0.8px solid #d4c4ae;
  border-radius: 3.5px;
  white-space: nowrap;
}
"""
