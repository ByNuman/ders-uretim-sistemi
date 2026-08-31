# -*- coding: utf-8 -*-
#
# Görsel Ders Notu Üretim Sistemi
# Copyright (C) 2026 Numan Gözdaş
#
# Bu program özgür yazılımdır: Özgür Yazılım Vakfı'nın yayımladığı GNU Genel
# Kamu Lisansı'nın 3. sürümü koşulları altında yeniden dağıtabilir ve/veya
# değiştirebilirsiniz.
#
# Bu program yararlı olacağı umuduyla dağıtılmaktadır, ancak HİÇBİR GARANTİ
# VERİLMEZ; SATILABİLİRLİK veya BELİRLİ BİR AMACA UYGUNLUK zımni garantileri
# dahi verilmez. Ayrıntılar için GNU Genel Kamu Lisansı'na bakın.
#
# Lisansın bir kopyasını bu depodaki LICENSE dosyasında bulabilirsiniz;
# ayrıca <https://www.gnu.org/licenses/> adresinden edinebilirsiniz.
#
"""
HARİTA ÇİZİMİ — gerçek coğrafya verisinden SVG üretir
=======================================================

Bu modül, harita kutusundaki görseli ÜRETİR: yapay zekâ ile değil, gerçek
kartografik veriyle.

NEDEN DEĞİŞTİ
-------------
Önceki sürüm haritayı fal.ai / gpt-image-2 ile "çizdiriyordu". O yol
terk edildi çünkü görüntü modeli bir harita motoru değildir: kıyı çizgisini
ezberden benzetir, sınırı uydurur. Ölçülen hatalar (2026 Ağustos, İslam
Tarihi III): Hazar Denizi üç haritada imparatorluk sınırının İÇİNDE kaldı;
Ammuriye önce Suriye kıyısına, sonra güneydoğu Anadolu'ya kondu (doğru yere
gelmesi için elle koordinat ipucu gerekti); Cend, Seyhun yerine Hazar
kıyısına düştü. Bir ders kitabında bu, sessiz bir yanlış bilgi kaynağıdır.

ŞİMDİ NE OLUYOR
---------------
| Katman | Kaynak | Güvenilirlik |
|---|---|---|
| Kıyı, kara, göl, nehir | Natural Earth 1:50m (KAMU MALI / CC0) | gerçek veri |
| Şehir konumları | `Place(ad, lon, lat)` — elle yazılan gerçek koordinat | doğrulanabilir |
| Devlet/bölge alanı | `MapBox.territory` — YAKLAŞIK poligon | **temsilî** |

Üçüncü satır dürüstlük meselesidir: ortaçağ siyasi sınırları için serbest ve
yetkeli bir veri kümesi YOKTUR (Natural Earth bugünün sınırlarıdır, CShapes
1886'da başlar, Euratlas lisanslıdır). Bu yüzden alan poligonu elle, kaba
hatlarla yazılır ve harita kutusunda HER ZAMAN "yaklaşık" ibaresiyle
gösterilir. Uydurma bir atıf (sayfa numaralı sahte atlas künyesi) YAZMAYIN;
`MapBox.source` alanının varsayılanı zaten iddiayı doğru biçimde kurar.

Çıktı SVG'dir: baskıda keskin, dosya küçük, üretim ücretsiz ve
DETERMİNİSTİK — aynı girdi her derlemede aynı haritayı verir (görüntü
modelinde her çağrı farklı sonuç veriyordu, bu da taşma denetimini
güvenilmez kılıyordu).

Bağımlılık yoktur: GeoJSON `json` ile okunur, izdüşüm ve SVG saf Python'dur.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERI = ROOT / "assets" / "harita"

# Natural Earth 1:50m — kamu malı (CC0). tools/harita.py --veri-indir ile gelir.
KATMANLAR = {
    "kara": "ne_50m_land.geojson",
    "goller": "ne_50m_lakes.geojson",
    "nehirler": "ne_50m_rivers_lake_centerlines.geojson",
}
VERI_KAYNAGI = ("https://raw.githubusercontent.com/nvkelso/natural-earth-vector"
                "/master/geojson/")

# Harita kutusunun en-boy oranı (SVG viewBox). Kutu CSS'i de bunu kullanır.
ORAN = (4, 3)          # varsayılan/yedek; asıl oran bbox'tan türetilir

# Kutu oranının izin verilen aralığı (genişlik / yükseklik). Sabit 4:3, DİKEY
# coğrafyalarda (Memlük: Mısır+Şam+Hicaz · Delhi: Hint alt kıtası) haritayı
# kutunun ortasına küçük bir şerit hâlinde sıkıştırıyor, sağını solunu boş
# bırakıyor ve sayfanın altında büyük bir boşluk açıyordu.
#
# Sınırlar KEYFİ DEĞİL, yerleşimden geliyor: yan sütun 82 mm geniştir;
# 0.72 oranında kutu 114 mm olur ki metin sütunuyla birlikte sayfaya sığan
# üst sınırdır. 1.60'ın üstünde ise kutu 51 mm'ye iner ve harita okunmaz.
ORAN_EN_DAR = 0.72
ORAN_EN_GENIS = 1.60
GENISLIK = 800.0          # viewBox birimi; mm değil, ölçek serbest

_ONBELLEK: dict[str, list] = {}


class VeriYok(FileNotFoundError):
    """Natural Earth katmanı diskte yok."""


# ---------------------------------------------------------------------------
# Veri yükleme
# ---------------------------------------------------------------------------
def veri_var_mi() -> bool:
    return all((VERI / ad).exists() for ad in KATMANLAR.values())


def _yukle(katman: str) -> list:
    """Bir katmanı (feature listesi) yükler; süreç boyunca önbellekte tutar."""
    if katman in _ONBELLEK:
        return _ONBELLEK[katman]
    yol = VERI / KATMANLAR[katman]
    if not yol.exists():
        raise VeriYok(
            f"Harita verisi yok: {yol}\n"
            f"İndirmek için: python tools/harita.py --veri-indir")
    with yol.open(encoding="utf-8") as f:
        veri = json.load(f)
    _ONBELLEK[katman] = veri["features"]
    return _ONBELLEK[katman]


# ---------------------------------------------------------------------------
# İzdüşüm
# ---------------------------------------------------------------------------
class Cerceve:
    """Eşuzaklıklı silindirik izdüşüm (standart paralel = kutunun orta enlemi).

    Bölgesel haritalar için yeterlidir ve tek satırdır; Mercator'ın yüksek
    enlemlerde şişirme sorunu yoktur. Verilen bbox, kutunun en-boy oranına
    uyacak şekilde GENİŞLETİLİR (kırpılmaz) — böylece harita çerçeveyi
    doldurur ama şekiller ezilmez.
    """

    def __init__(self, bbox, genislik: float = GENISLIK, oran=ORAN):
        bati, guney, dogu, kuzey = bbox
        self.yukseklik = genislik * oran[1] / oran[0]
        self.genislik = genislik

        self.lat0 = (guney + kuzey) / 2.0
        self.lon0 = (bati + dogu) / 2.0
        self.k = math.cos(math.radians(self.lat0))    # boylam kısalması

        dx = (dogu - bati) * self.k
        dy = kuzey - guney
        hedef = genislik / self.yukseklik
        if dx / dy < hedef:
            dx = dy * hedef
        else:
            dy = dx / hedef
        self.dx, self.dy = dx, dy
        self.olcek = genislik / dx

        # görünür bbox (genişletilmiş) — özellik ayıklamada kullanılır
        yari_lon = (dx / self.k) / 2.0
        yari_lat = dy / 2.0
        self.gorunur = (self.lon0 - yari_lon, self.lat0 - yari_lat,
                        self.lon0 + yari_lon, self.lat0 + yari_lat)

    def nokta(self, lon: float, lat: float) -> tuple[float, float]:
        x = (lon - self.lon0) * self.k * self.olcek + self.genislik / 2.0
        y = -(lat - self.lat0) * self.olcek + self.yukseklik / 2.0
        return x, y


def oran_hesapla(bbox) -> tuple[float, float]:
    """bbox'ın izdüşümdeki en-boy oranını kutu oranı olarak verir.

    `Cerceve` bbox'ı kutuya uyacak şekilde GENİŞLETİR; kutu oranı içeriğe
    yakınsa bu genişletme küçük kalır, yani harita çerçeveyi doldurur.
    Sonuç [ORAN_EN_DAR, ORAN_EN_GENIS] aralığına kırpılır.
    """
    bati, guney, dogu, kuzey = bbox
    lat0 = (guney + kuzey) / 2.0
    dx = (dogu - bati) * math.cos(math.radians(lat0))
    dy = (kuzey - guney) or 1e-9
    return (max(ORAN_EN_DAR, min(ORAN_EN_GENIS, dx / dy)), 1.0)


def _kesisiyor(bbox_a, bbox_b) -> bool:
    return not (bbox_a[2] < bbox_b[0] or bbox_a[0] > bbox_b[2] or
                bbox_a[3] < bbox_b[1] or bbox_a[1] > bbox_b[3])


# Bu ölçünün (viewBox birimi) altında kalan halkalar hiç çizilmez: Ege'deki
# yüzlerce kayalık ada ve küçük göl, baskıda tek bir noktadan küçük görünür
# ama SVG'nin yarısını kaplar. Eşiksiz sürümde beş harita 1,8 MB tutuyordu.
EN_KUCUK_HALKA = 1.6


def _cizilir_mi(halka, cerceve: "Cerceve") -> bool:
    b = _halka_bbox(halka)
    x0, y0 = cerceve.nokta(b[0], b[1])
    x1, y1 = cerceve.nokta(b[2], b[3])
    return abs(x1 - x0) >= EN_KUCUK_HALKA or abs(y1 - y0) >= EN_KUCUK_HALKA


def _halka_bbox(halka) -> tuple:
    lons = [p[0] for p in halka]
    lats = [p[1] for p in halka]
    return (min(lons), min(lats), max(lons), max(lats))


def _halkalar(geometri, tipler=("Polygon", "MultiPolygon")):
    """GeoJSON geometrisinden dış+iç halkaları düz liste olarak verir."""
    t = geometri["type"]
    if t not in tipler:
        return
    if t == "Polygon":
        for halka in geometri["coordinates"]:
            yield halka
    elif t == "MultiPolygon":
        for poligon in geometri["coordinates"]:
            for halka in poligon:
                yield halka
    elif t == "LineString":
        yield geometri["coordinates"]
    elif t == "MultiLineString":
        for cizgi in geometri["coordinates"]:
            yield cizgi


def _cizgiler(geometri):
    t = geometri["type"]
    if t == "LineString":
        yield geometri["coordinates"]
    elif t == "MultiLineString":
        for cizgi in geometri["coordinates"]:
            yield cizgi


# ---------------------------------------------------------------------------
# SVG yolu üretimi
# ---------------------------------------------------------------------------
def _kirp_poligon(nokta_px, w: float, h: float, pay: float = 12.0):
    """Sutherland-Hodgman: poligonu görüş dikdörtgenine kırpar.

    ŞART, süs değil: Natural Earth'te Avrasya+Afrika TEK bir halkadır ve
    hangi bölgeye bakarsanız bakın çerçeveyle kesişir. Kırpma olmadan her
    harita bütün Avrasya kıyısını (on binlerce nokta) gömüyordu -- beş harita
    1,8 MB tutuyor, PDF gereksiz şişiyordu. Kırpma dolgunun şeklini
    bozmaz çünkü kesim çerçevenin dışındadır.
    """
    kenarlar = (
        ("x>", -pay), ("x<", w + pay), ("y>", -pay), ("y<", h + pay),
    )
    cikti = list(nokta_px)
    for tip, deger in kenarlar:
        if not cikti:
            return []
        girdi, cikti = cikti, []

        def icerde(p):
            if tip == "x>":
                return p[0] >= deger
            if tip == "x<":
                return p[0] <= deger
            if tip == "y>":
                return p[1] >= deger
            return p[1] <= deger

        def kesisim(a, b):
            if tip in ("x>", "x<"):
                t = (deger - a[0]) / (b[0] - a[0]) if b[0] != a[0] else 0.0
                return (deger, a[1] + t * (b[1] - a[1]))
            t = (deger - a[1]) / (b[1] - a[1]) if b[1] != a[1] else 0.0
            return (a[0] + t * (b[0] - a[0]), deger)

        onceki = girdi[-1]
        for simdiki in girdi:
            if icerde(simdiki):
                if not icerde(onceki):
                    cikti.append(kesisim(onceki, simdiki))
                cikti.append(simdiki)
            elif icerde(onceki):
                cikti.append(kesisim(onceki, simdiki))
            onceki = simdiki
    return cikti


def _kirp_cizgi(nokta_px, w: float, h: float, pay: float = 12.0):
    """Açık çizgiyi (nehir) parçalara ayırarak kırpar."""
    kutu = (-pay, -pay, w + pay, h + pay)

    def ic(p):
        return kutu[0] <= p[0] <= kutu[2] and kutu[1] <= p[1] <= kutu[3]

    parcalar, simdi = [], []
    for p in nokta_px:
        if ic(p):
            simdi.append(p)
        else:
            if len(simdi) > 1:
                parcalar.append(simdi)
            simdi = []
    if len(simdi) > 1:
        parcalar.append(simdi)
    return parcalar


def _yol(noktalar, cerceve: Cerceve, kapali: bool = True,
         en_kucuk_adim: float = 0.7) -> str:
    """Halkayi/cizgiyi SVG path'ine cevirir.

    Iki asama: once GORUS ALANINA KIRPILIR (bkz. _kirp_poligon gerekcesi),
    sonra 0,7 birimden yakin noktalar atilir. Esik piksel altidir, gorunur
    kayip yoktur; kazanc dosya boyutundadir.
    """
    px = [cerceve.nokta(lon, lat) for lon, lat in noktalar]
    W, H = cerceve.genislik, cerceve.yukseklik

    if kapali:
        parcalar_ham = [_kirp_poligon(px, W, H)]
    else:
        parcalar_ham = _kirp_cizgi(px, W, H)

    yollar = []
    for parca in parcalar_ham:
        if len(parca) < 2:
            continue
        adimlar = []
        sx = sy = None
        for x, y in parca:
            if sx is None:
                adimlar.append(f"M{x:.1f},{y:.1f}")
                sx, sy = x, y
            elif abs(x - sx) + abs(y - sy) >= en_kucuk_adim:
                adimlar.append(f"L{x:.1f},{y:.1f}")
                sx, sy = x, y
        if len(adimlar) < 2:
            continue
        yollar.append(" ".join(adimlar) + ("Z" if kapali else ""))
    return " ".join(yollar)


def _kacis(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# ---------------------------------------------------------------------------
# Renk paleti (tema renginden türetilir)
# ---------------------------------------------------------------------------
def _hsl(hexcolor: str) -> tuple[float, float, float]:
    h = hexcolor.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    if mx == mn:
        return 0.0, 0.0, l
    d = mx - mn
    s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == r:
        hh = ((g - b) / d) % 6
    elif mx == g:
        hh = (b - r) / d + 2
    else:
        hh = (r - g) / d + 4
    return hh * 60, s * 100, l * 100


def _hex(h: float, s: float, l: float) -> str:
    h = h % 360; s = max(0.0, min(100.0, s)) / 100; l = max(0.0, min(100.0, l)) / 100
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    r, g, b = [(c, x, 0), (x, c, 0), (0, c, x), (0, x, c), (x, 0, c), (c, 0, x)][int(h // 60) % 6]
    return "#%02X%02X%02X" % (round((r + m) * 255), round((g + m) * 255), round((b + m) * 255))


def palet(tema_hex: str) -> dict:
    """Dersin tema renginden haritanın tüm katman renklerini türetir.

    Deniz bilerek NÖTR açık mavi-gri: alan dolgusuyla aynı aileden olursa
    "deniz de imparatorluk toprağı" izlenimi doğuyor (görüntü modelinde
    tekrar tekrar yaşanan hata buydu).
    """
    h, s, _ = _hsl(tema_hex or "#3d5568")
    return {
        # Deniz bilerek SOLUK ve nötr: dolgu rengiyle yarışırsa alan "su" gibi
        # okunuyor (ilk sürümde tam olarak bu oldu).
        "deniz":      "#E6EDF2",
        "kara":       "#F2EFE9",
        "kara_kenar": "#C6C1B7",
        "nehir":      "#A8C4D6",
        "alan":       _hex(h, max(30, min(58, s)), 66),
        "alan_kenar": _hex(h, min(62, s), 36),
        "sehir":      "#C0392B",
        "yazi":       "#2A2A28",
        "yazi_soluk": "#6B6B66",
        "hale":       "#F7F5F1",
    }


def _yumusat(poligon, tur: int = 2):
    """Chaikin köşe kesme: elle yazılan kaba poligonu yumuşak bir eğriye çevirir.

    İki işi birden yapar. (1) Görsel: 15-25 noktalı bir poligon, yanındaki
    hassas kıyı çizgisinin yanında kırık dökük duruyordu. (2) Anlam: yumuşak,
    genelleştirilmiş bir hat "yaklaşık" olduğunu kendiliğinden söyler; keskin
    köşeli bir çokgen ölçülmüş bir sınır gibi görünür.
    """
    nokta = list(poligon)
    if len(nokta) < 4:
        return nokta
    kapali = nokta[0] == nokta[-1]
    if kapali:
        nokta = nokta[:-1]
    for _ in range(tur):
        yeni = []
        n = len(nokta)
        for i in range(n):
            (x0, y0), (x1, y1) = nokta[i], nokta[(i + 1) % n]
            yeni.append((0.75 * x0 + 0.25 * x1, 0.75 * y0 + 0.25 * y1))
            yeni.append((0.25 * x0 + 0.75 * x1, 0.25 * y0 + 0.75 * y1))
        nokta = yeni
    return nokta + [nokta[0]]


# ---------------------------------------------------------------------------
# Ana çizim
# ---------------------------------------------------------------------------
def svg_uret(mb, tema_hex: str, genislik: float = GENISLIK, oran=None) -> str:
    """Bir MapBox'tan tam SVG metni üretir.

    `oran` verilmezse bbox'tan türetilir (bkz. oran_hesapla) -- dikey
    coğrafyalar dikey kutu alır.
    """
    if not mb.bbox:
        raise ValueError(f"MapBox.bbox boş: {mb.region!r} -- harita çizilemez.")
    c = Cerceve(mb.bbox, genislik, oran or oran_hesapla(mb.bbox))
    p = palet(tema_hex)
    # SVG'ler tek bir HTML belgesine GÖMÜLÜ olarak yan yana durur; clipPath
    # id'si belge genelinde benzersiz olmak zorundadır, yoksa beş harita da
    # ilk haritanın kara maskesiyle kırpılır (sessiz, çok yanıltıcı bir hata).
    kimlik = "kara-" + hashlib.sha1(mb.region.encode("utf-8")).hexdigest()[:8]
    W, H = c.genislik, c.yukseklik
    gb = c.gorunur

    parca = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" '
        f'width="100%" height="100%" role="img" '
        f'aria-label="{_kacis(mb.region)} haritası">',
        f'<rect width="{W:.0f}" height="{H:.0f}" fill="{p["deniz"]}"/>',
    ]

    # --- kara ---
    kara_yollari = []
    for ft in _yukle("kara"):
        for halka in _halkalar(ft["geometry"]):
            if not _kesisiyor(_halka_bbox(halka), gb) or not _cizilir_mi(halka, c):
                continue
            y = _yol(halka, c)
            if y:
                kara_yollari.append(y)
    kara_d = " ".join(kara_yollari)
    if kara_d:
        parca.append(
            f'<path d="{kara_d}" fill="{p["kara"]}" '
            f'stroke="{p["kara_kenar"]}" stroke-width="0.8" fill-rule="evenodd"/>')

    gol_yollari = []
    for ft in _yukle("goller"):
        for halka in _halkalar(ft["geometry"]):
            if not _kesisiyor(_halka_bbox(halka), gb) or not _cizilir_mi(halka, c):
                continue
            y = _yol(halka, c)
            if y:
                gol_yollari.append(y)

    # --- YAKLAŞIK devlet/bölge alanı (temsilî) ---
    # KARAYA KIRPILIR. Elle yazılan kaba poligon kıyıyı birebir izleyemez;
    # kırpma olmadan dolgu denize sarkar ve "deniz de bu devletin toprağıydı"
    # gibi okunur (görüntü modelinin tekrar tekrar yaptığı hata buydu).
    # Kırpmayla kıyı kenarı GERÇEK veriden gelir, yaklaşıklık yalnızca kara
    # içindeki sınırlarda kalır. Göller hemen ardından ÜSTE çizilir.
    if mb.katmanlar and kara_d:
        # ÇOK KATMANLI: dönem dönem genişleme. En eski en KOYU tonla basılır;
        # ton merdiveni tema renginden türer, yani harita dersin rengiyle
        # aynı ailede kalır. Etiketler HTML lejanta taşınır (mb.lejant).
        parca.append(f'<clipPath id="{kimlik}"><path d="{kara_d}" '
                     f'clip-rule="evenodd"/></clipPath>')
        parca.append(f'<g clip-path="url(#{kimlik})">')
        h, sat, _l = _hsl(tema_hex)
        n = len(mb.katmanlar)
        lejant = []
        for i, katman in enumerate(mb.katmanlar):
            # 34 -> 68 açıklık merdiveni. Üst uç 76 DEĞİL: orada en açık bant
            # denizin soluk mavisine yaklaşıyor ve "burası da su mu?" diye
            # okunuyordu (ölçüldü: Rum Selçuklu, 4 bant). 68'de bantlar hem
            # birbirinden hem denizden ayrışıyor.
            aciklik = 34.0 + (34.0 * i / max(1, n - 1))
            renk = _hex(h, max(28.0, min(56.0, sat)), aciklik)
            for poligon in katman.get("halkalar", []):
                y = _yol(_yumusat(poligon), c, en_kucuk_adim=0.0)
                if y:
                    parca.append(f'<path d="{y}" fill="{renk}" fill-opacity="0.88" '
                                 f'stroke="{p["alan_kenar"]}" stroke-width="1.4" '
                                 f'stroke-dasharray="7 4.5" stroke-linejoin="round"/>')
            if katman.get("etiket"):
                lejant.append((renk, katman["etiket"]))
        parca.append("</g>")
        if lejant and not mb.lejant:
            mb.lejant = lejant

    if mb.territory and kara_d:
        parca.append(f'<clipPath id="{kimlik}"><path d="{kara_d}" '
                     f'clip-rule="evenodd"/></clipPath>')
        parca.append(f'<g clip-path="url(#{kimlik})">')
        for poligon in mb.territory:
            y = _yol(_yumusat(poligon), c, en_kucuk_adim=0.0)
            if y:
                # KESİKLİ kenar: kartografyada "sınır kesin değil" demektir.
                # Düz çizgi, ölçülmüş bir sınır iddiası gibi okunurdu.
                parca.append(f'<path d="{y}" fill="{p["alan"]}" fill-opacity="0.72" '
                             f'stroke="{p["alan_kenar"]}" stroke-width="2.0" '
                             f'stroke-dasharray="7 4.5" stroke-linejoin="round"/>')
        parca.append("</g>")

    # --- göller (alanın ÜSTÜNE: dolgu bir gölü boyayamasın) ---
    if gol_yollari:
        parca.append(f'<path d="{" ".join(gol_yollari)}" fill="{p["deniz"]}" '
                     f'stroke="{p["kara_kenar"]}" stroke-width="0.6"/>')

    # --- nehirler ---
    nehir_yollari = []
    for ft in _yukle("nehirler"):
        for cizgi in _cizgiler(ft["geometry"]):
            if not _kesisiyor(_halka_bbox(cizgi), gb) or not _cizilir_mi(cizgi, c):
                continue
            y = _yol(cizgi, c, kapali=False)
            if y:
                nehir_yollari.append(y)
    if nehir_yollari:
        parca.append(f'<path d="{" ".join(nehir_yollari)}" fill="none" '
                     f'stroke="{p["nehir"]}" stroke-width="1.1"/>')

    # --- komşu bölge etiketleri ---
    for yer in (mb.neighbors or []):
        x, yy = c.nokta(yer.lon, yer.lat)
        satirlar = yer.name.split("\n")
        for i, satir in enumerate(satirlar):
            parca.append(
                f'<text x="{x:.1f}" y="{yy + i * 15:.1f}" text-anchor="middle" '
                f'font-family="DejaVu Sans, sans-serif" font-size="13" '
                f'fill="{p["yazi_soluk"]}" stroke="{p["hale"]}" stroke-width="2.6" '
                f'paint-order="stroke">{_kacis(satir)}</text>')

    # --- şehirler ---
    for yer in (mb.cities or []):
        x, yy = c.nokta(yer.lon, yer.lat)
        parca.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="3.4" '
                     f'fill="{p["sehir"]}" stroke="#FFFFFF" stroke-width="1"/>')
        hiza, dx = ("start", 6.5) if yer.sag else ("end", -6.5)
        parca.append(
            f'<text x="{x + dx:.1f}" y="{yy + 4.2:.1f}" text-anchor="{hiza}" '
            f'font-family="DejaVu Sans, sans-serif" font-size="13.5" font-weight="600" '
            f'fill="{p["yazi"]}" stroke="{p["hale"]}" stroke-width="2.8" '
            f'paint-order="stroke">{_kacis(yer.name)}</text>')

    parca.append("</svg>")
    return "".join(parca)
