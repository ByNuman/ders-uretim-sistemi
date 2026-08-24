# -*- coding: utf-8 -*-
"""
DERS ÜRETİM SİSTEMİ — Dinamik Tema Motoru
============================================
Sabit .theme-indigo / .theme-burgundy / ... sınıflarının yanına, TEK bir
marka renginden (hex) tüm CSS değişkenlerini otomatik türeten bir motor
ekler. Böylece 5 sabit temayla sınırlı kalmadan, istediğiniz kadar ders
için (13, 14, 50...) birbirinden ayrışan tema üretilebilir.

Formül, mevcut 5 sabit temanın (indigo/burgundy/forest/slate/plum) HSL
değerleri geriye doğru analiz edilerek kalibre edilmiştir — yani üretilen
yeni temalar, elle tasarlanmış 5 referans temayla AYNI görsel kalite
çizgisindedir (bkz. `_calibration_notes.txt` gerekmez, hesaplama aşağıda).

Kullanım (build.py içinde):
    from theme_engine import resolve_theme_css
    override_css = resolve_theme_css(pack.theme_color)   # None ise "" döner
"""
import colorsys

# Referans 5 temadan ölçülen, pratikte sabit kalan altın tonu (gold, gold-ink)
GOLD = "#d9b466"       # HSL≈(42, 56, 63) — 5 temanın ortalaması
GOLD_INK = "#6b5210"   # HSL≈(44, 74, 24)


def _hsl_to_hex(h: float, s: float, l: float) -> str:
    s = max(0.0, min(100.0, s)) / 100.0
    l = max(0.0, min(100.0, l)) / 100.0
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360.0, l, s)
    return "#%02X%02X%02X" % (round(r * 255), round(g * 255), round(b * 255))


def _hex_to_hsl(hexcolor: str):
    hexcolor = hexcolor.lstrip("#")
    r, g, b = (int(hexcolor[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360.0, s * 100.0, l * 100.0


def generate_theme_vars(hue: float, sat: float = 50.0, light: float = 34.0) -> dict:
    """Tek bir hue (0-360) + doygunluk + parlaklıktan tüm tema değişkenlerini üretir.
    sat/light varsayılanları, 5 referans temanın ortalamasına göre kalibredir."""
    # 20-70° (sarı/sarı-yeşil) aralığında yüksek doygunluk "trafik konisi" gibi
    # durur; bu aralıkta otomatik kısıyoruz (forest/olive gibi tonlar hariç tut).
    if 35 <= hue <= 85:
        sat = min(sat, 42)
    sat = max(24.0, min(70.0, sat))
    light = max(22.0, min(46.0, light))

    accent = _hsl_to_hex(hue, sat, light)
    accent_dark = _hsl_to_hex(hue, min(sat + 3, 78), max(light - 14, 10))
    accent_soft = _hsl_to_hex(hue, 45, 95.5)
    accent_tint = _hsl_to_hex(hue, 45, 97.5)
    g1 = _hsl_to_hex(hue, min(sat + 12, 78), 10)
    g2 = _hsl_to_hex(hue, sat, max(light - 5, 8))
    g3 = _hsl_to_hex(hue, max(sat - 8, 20), min(light + 10, 60))
    paper = _hsl_to_hex(hue, 35, 99)
    paper_tint = _hsl_to_hex(hue, 32, 96.8)
    line = _hsl_to_hex(hue, 28, 90.5)
    line_soft = _hsl_to_hex(hue, 30, 94.2)

    return {
        "--accent": accent, "--accent-dark": accent_dark,
        "--accent-soft": accent_soft, "--accent-tint": accent_tint,
        "--cover-grad-1": g1, "--cover-grad-2": g2, "--cover-grad-3": g3,
        "--gold": GOLD, "--gold-ink": GOLD_INK,
        "--paper": paper, "--paper-tint": paper_tint,
        "--line": line, "--line-soft": line_soft,
    }


def generate_theme_vars_from_hex(hexcolor: str) -> dict:
    """Herhangi bir marka rengini (ör. '#7A2438') tam bir temaya çevirir."""
    hue, sat, light = _hex_to_hsl(hexcolor)
    # Kaynak rengin doygunluk/parlaklık karakterini referans al ama okunur aralıkta tut
    sat = sat * 0.85 + 15
    light = light if 22 <= light <= 46 else 34
    return generate_theme_vars(hue, sat, light)


def theme_css_block(theme_vars: dict, selector: str = ":root") -> str:
    decls = "\n".join(f"  {k}: {v};" for k, v in theme_vars.items())
    return f"{selector} {{\n{decls}\n}}"


def resolve_theme_css(theme_color, selector: str = ":root") -> str:
    """pack.theme_color (hex ya da None) alır, enjekte edilecek CSS override
    bloğunu döner. theme_color yoksa boş string döner (sabit .theme-XXXX
    sınıfları geçerliliğini korur — geriye dönük uyumluluk).

    `selector`: tek ders build'inde ":root" (varsayılan, eski davranış). KİTAP
    build'inde her ders kendi kapsamını alır (".ders-3" gibi) — 14 ders tek
    HTML'de yan yana durduğu için ":root" hepsini birbirine karıştırırdı.
    Kapsam sınıfı `.page` elementinin ÜZERİNE yazılır: custom property'ler
    tanımlandıkları elementin kendisinde ve altında geçerli olduğu için bu,
    o dersin tüm sayfalarını (kapak dahil) doğru renge boyar."""
    if not theme_color:
        return ""
    return theme_css_block(generate_theme_vars_from_hex(theme_color), selector)


# ---------------------------------------------------------------------------
# Hazır palet — 16 isimlendirilmiş, birbirinden net ayrışan hue/sat çifti.
# src/<ders>.py dosyalarında theme_color=PALETTE["bordo"] gibi kullanılabilir,
# ya da doğrudan herhangi bir hex geçilebilir (palet bir kolaylık, zorunlu değil).
# ---------------------------------------------------------------------------
PALETTE_HUES = {
    "cam-yesili":   (160, 55, 24),   # forest'a yakın ama ayrışık
    "lacivert":     (227, 50, 40),   # indigo'ya yakın ama ayrışık
    "bordo":        (350, 54, 36),   # burgundy referansı
    "antrasit":     (208, 27, 30),   # slate referansı
    "murdum":       (275, 41, 39),   # plum referansı
    "petrol":       (190, 58, 26),
    "kahve":        (25,  40, 32),
    "kiremit":      (12,  50, 34),
    "zeytin":       (75,  35, 30),
    "indigo-koyu":  (245, 48, 32),
    "celik-mavisi": (204, 30, 33),
    "gul-kurusu":   (332, 38, 38),
    "turkuaz":      (178, 52, 26),
    "visne":        (358, 48, 32),
    "hardal":       (42,  40, 36),
    "orman-yesili": (140, 45, 26),
}


if __name__ == "__main__":
    for name, (h, s, l) in PALETTE_HUES.items():
        v = generate_theme_vars(h, s, l)
        print(f"{name:15s} accent={v['--accent']}  g2={v['--cover-grad-2']}  g1={v['--cover-grad-1']}")
