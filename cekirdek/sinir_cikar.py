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
SINIR ÇIKARMA — Commons haritasındaki alanı gerçek koordinata çevirir
======================================================================

Amaç: bir tarihî haritanın **sınırını** kartograftan alıp geri kalan her şeyi
kendimiz çizmek. Sonuç `MapBox.territory` poligonudur; harita bundan sonra
`cekirdek/harita_cizim.py` ile çizilir — yani bütün etiketler Türkçe ve
vektör olur, PDF'e 16 MB'lık raster gömülmez, hiçbir kredi harcanmaz.

ZİNCİR
------
    kaynak raster + çapa noktaları
        -> izdüşüm çöz (piksel <-> lon/lat, EN KÜÇÜK KARELER)
        -> renk maskesi (toprak örtüsü)
        -> gürültü temizliği + bağlantılı bileşenler
        -> Moore sınır izleme -> Douglas-Peucker sadeleştirme
        -> lon/lat halkaları  +  kaynağın üstüne BİNDİRME görseli (gözle denetim)

NEDEN ÇAPA NOKTASI GEREKİR (ölçüldü, 2026-08-31)
------------------------------------------------
Tarihî haritaların izdüşümü dosyada YAZMAZ. Memlük haritasında yalnızca
3 çapayla (Kahire, Şam, Halep — üçü de kuzeyde kümelenmiş) çözülen afin
dönüşüm, güneye inildikçe sistematik olarak doğuya kaydı:

    İskenderiye ~25 px · Uswan ~130 px · Sawakin ~200 px · Makka ~240 px

240 px, kırpılmış görselin %22'si ≈ 4-5° boylamdır — yani Mekke'yi Kızıldeniz'in
karşı kıyısına atar. Sebep: kaynak eşuzaklık değil, meridyenleri güneye doğru
açılan koni benzeri bir izdüşümdedir.

ÇÖZÜM: çapaları haritanın DÖRT BİR YANINA dağıtın (en az 6, tercihen 8-10) ve
`ARTIK_ESIGI`'ni okuyun. Araç her çapanın artık hatasını piksel cinsinden
basar; büyük artık, o çapanın yanlış okunduğunu ya da izdüşümün daha yüksek
dereceli olduğunu söyler.

DÜRÜSTLÜK
---------
Sınır kartografın çizimidir, bizim tahminimiz DEĞİLDİR — ama CC BY-SA bir
haritadan türetilmiştir. **Atıf yükümlülüğü devam eder**; `MapBox.source`
alanına kaynağın künyesi yazılır. "Artık bizim çizimimiz" denemez.
"""

from __future__ import annotations

import colorsys
import json
import math
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMONS = ROOT / "assets" / "harita" / "commons"
SINIR = ROOT / "assets" / "harita" / "sinir"

# Çapa artığı bu eşiği aşarsa araç UYARIR (kırpılmış görselin genişliğine oranla).
ARTIK_ESIGI = 0.012          # %1,2 — 1080 px'lik bir kırpmada ~13 px
TARAMA_GENISLIK = 360        # maske/kontur bu ölçekte çalışır (hız)


class CapaYok(FileNotFoundError):
    """Kaynak haritanın yanında `<dosya>.capa.json` yok."""


@dataclass
class Capa:
    """Kaynak haritada yeri BİLİNEN bir nokta: adı, gerçek koordinatı, oranı.

    `x`/`y` KIRPILMIŞ görselin oranıdır (0-1) — `Isaret` ile aynı düzen, yani
    `tools/harita.py --imlec` ızgarasından okunabilir.
    """
    ad: str
    lon: float
    lat: float
    x: float
    y: float


@dataclass
class Kalibrasyon:
    """Çözülmüş izdüşüm: iki yönlü polinom + artık hatalar."""
    ileri: list                      # (lon,lat) -> (x,y) katsayıları
    geri: list                       # (x,y) -> (lon,lat) katsayıları
    derece: int                      # 1 = afin, 2 = ikinci derece
    artiklar: list = field(default_factory=list)   # [(ad, piksel_oran), ...]

    @property
    def en_buyuk_artik(self) -> float:
        return max((a for _, a in self.artiklar), default=0.0)


# ---------------------------------------------------------------------------
# Doğrusal cebir (saf Python — depoda numpy yok, olmasını da gerektirmiyoruz)
# ---------------------------------------------------------------------------

def _coz(A: list, b: list) -> list:
    """A·c = b (kare sistem), kısmi pivotlu Gauss."""
    n = len(A)
    m = [satir[:] + [sag] for satir, sag in zip(A, b)]
    for i in range(n):
        piv = max(range(i, n), key=lambda r: abs(m[r][i]))
        if abs(m[piv][i]) < 1e-12:
            raise ValueError("izdüşüm çözülemedi: çapalar doğrusal bağımlı "
                             "(hepsi aynı hat üzerinde olabilir)")
        m[i], m[piv] = m[piv], m[i]
        for r in range(n):
            if r != i:
                f = m[r][i] / m[i][i]
                for c in range(i, n + 1):
                    m[r][c] -= f * m[i][c]
    return [m[i][n] / m[i][i] for i in range(n)]


def _terimler(u: float, v: float, derece: int) -> list:
    """Polinom taban fonksiyonları (1 = afin, 2 = kuadratik, 3 = kübik).

    Derece çapa sayısına göre seçilir; daha yükseğini ZORLAMAYIN. Yüksek
    dereceli bir polinom çapaların dışında savrulur (Runge olgusu) ve
    haritanın çapasız köşelerinde sınırı sessizce bozar -- bu yüzden
    `bindirme.png` denetimi kübik uyumda daha da kritiktir.
    """
    t = [1.0, u, v]
    if derece >= 2:
        t += [u * u, u * v, v * v]
    if derece >= 3:
        t += [u * u * u, u * u * v, u * v * v, v * v * v]
    return t


def _en_kucuk_kareler(girdi: list, cikti: list, derece: int) -> list:
    """Normal denklemlerle en küçük kareler: cikti ≈ katsayı · terimler(girdi)."""
    n = len(_terimler(0, 0, derece))
    A = [[0.0] * n for _ in range(n)]
    b = [0.0] * n
    for (u, v), hedef in zip(girdi, cikti):
        t = _terimler(u, v, derece)
        for i in range(n):
            b[i] += t[i] * hedef
            for j in range(n):
                A[i][j] += t[i] * t[j]
    return _coz(A, b)


def izdusum_coz(capalar: list[Capa]) -> Kalibrasyon:
    """Çapalardan iki yönlü izdüşümü çözer ve artık hataları ölçer.

    İki yön de AYRI AYRI uydurulur (birinin tersini almak yerine): ikinci
    dereceden bir polinomun analitik tersi yoktur, ama ters yönü doğrudan
    uydurmak hem daha basit hem de aynı doğrulukta.
    """
    if len(capalar) < 3:
        raise ValueError(f"en az 3 çapa gerekir, {len(capalar)} verildi")
    # KUADRATİK TAVANDIR — kübiği DENEMEYİN, ölçülüp reddedildi.
    #
    # Hârezmşâhlar haritası (15 çapa, ~25° boylam) üzerinde ölçülen en büyük
    # artıklar: afin %2,44 · kuadratik %1,49 · kübik %1,16. Sayıya bakıp kübiğe
    # geçmek CAZİP görünüyor ve bir kez geçildi de -- ama `bindirme.png` şunu
    # gösterdi: kübik uyum ÇAPALARIN DIŞINDA savruluyor (Runge olgusu). Kuzey
    # sınırı haritanın dışına düz bir çizgi hâlinde fırladı, güney sınırı Basra
    # Körfezi'ne taştı. Kuadratik aynı haritada her yerde alanı düzgün izliyor.
    #
    # DERS: artık hatası yalnızca ÇAPA NOKTALARINDA ölçülür; çapasız bölgede
    # ne olduğunu söylemez. Bu yüzden sayısal ölçüt tek başına yetmez ve
    # bindirme denetimi zorunludur.
    derece = 2 if len(capalar) >= 6 else 1

    cografi = [(c.lon, c.lat) for c in capalar]
    piksel = [(c.x, c.y) for c in capalar]
    ileri = [_en_kucuk_kareler(cografi, [c.x for c in capalar], derece),
             _en_kucuk_kareler(cografi, [c.y for c in capalar], derece)]
    geri = [_en_kucuk_kareler(piksel, [c.lon for c in capalar], derece),
            _en_kucuk_kareler(piksel, [c.lat for c in capalar], derece)]

    artiklar = []
    for c in capalar:
        t = _terimler(c.lon, c.lat, derece)
        tx = sum(k * v for k, v in zip(ileri[0], t))
        ty = sum(k * v for k, v in zip(ileri[1], t))
        artiklar.append((c.ad, math.hypot(tx - c.x, ty - c.y)))
    return Kalibrasyon(ileri=ileri, geri=geri, derece=derece, artiklar=artiklar)


def oran_to_lonlat(kal: Kalibrasyon, x: float, y: float) -> tuple:
    t = _terimler(x, y, kal.derece)
    return (sum(k * v for k, v in zip(kal.geri[0], t)),
            sum(k * v for k, v in zip(kal.geri[1], t)))


def lonlat_to_oran(kal: Kalibrasyon, lon: float, lat: float) -> tuple:
    t = _terimler(lon, lat, kal.derece)
    return (sum(k * v for k, v in zip(kal.ileri[0], t)),
            sum(k * v for k, v in zip(kal.ileri[1], t)))


# ---------------------------------------------------------------------------
# Maske -> kontur
# ---------------------------------------------------------------------------

def maske_uret(im, ton: tuple, en_az_doygunluk: float = 0.12) -> tuple:
    """Tonu `ton` aralığına düşen pikselleri işaretler. (maske, W, H)."""
    oran = im.width / im.height
    W = TARAMA_GENISLIK
    H = max(1, round(W / oran))
    from PIL import Image
    px = im.resize((W, H), Image.LANCZOS).load()
    m = bytearray(W * H)
    alt, ust = ton
    for j in range(H):
        for i in range(W):
            r, g, b = px[i, j]
            h, _l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            if s >= en_az_doygunluk and alt <= h * 360 <= ust:
                m[j * W + i] = 1
    return m, W, H


def temizle(m: bytearray, W: int, H: int, tur: int = 3) -> bytearray:
    """Çoğunluk filtresi: yalnız pikselleri atar, küçük delikleri doldurur.

    Gerek: JPEG sıkıştırması ve arazi gölgesi maskede tuz-biber gürültüsü
    bırakıyor; temizlenmezse kontur yüzlerce sahte girinti üretir.
    """
    for _ in range(tur):
        yeni = bytearray(m)
        for j in range(H):
            for i in range(W):
                n = 0
                for dj in (-1, 0, 1):
                    for di in (-1, 0, 1):
                        if di or dj:
                            x, y = i + di, j + dj
                            if 0 <= x < W and 0 <= y < H and m[y * W + x]:
                                n += 1
                k = j * W + i
                if m[k] and n <= 2:
                    yeni[k] = 0
                elif not m[k] and n >= 6:
                    yeni[k] = 1
        m = yeni
    return m


def bilesenler(m: bytearray, W: int, H: int) -> list:
    """4-komşuluk bağlantılı bileşenler, büyükten küçüğe."""
    gor = bytearray(W * H)
    cikti = []
    for j0 in range(H):
        for i0 in range(W):
            if not m[j0 * W + i0] or gor[j0 * W + i0]:
                continue
            yigin = [(i0, j0)]
            gor[j0 * W + i0] = 1
            hucre = []
            while yigin:
                i, j = yigin.pop()
                hucre.append((i, j))
                for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    x, y = i + di, j + dj
                    if 0 <= x < W and 0 <= y < H and m[y * W + x] and not gor[y * W + x]:
                        gor[y * W + x] = 1
                        yigin.append((x, y))
            cikti.append(hucre)
    return sorted(cikti, key=len, reverse=True)


_YON = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]


def kontur(hucreler: list) -> list:
    """Moore-Neighbor sınır izleme; bileşenin dış halkasını sırayla verir."""
    kume = set(hucreler)
    bas = min(hucreler, key=lambda t: (t[1], t[0]))       # en üst-sol

    def tara(merkez, girilen):
        for k in range(1, 9):
            y = (girilen + k) % 8
            di, dj = _YON[y]
            aday = (merkez[0] + di, merkez[1] + dj)
            if aday in kume:
                return aday, (y + 4) % 8
        return None, None

    halka = [bas]
    simdi, geri = tara(bas, 4)                             # batıdan girildi
    if simdi is None:
        return halka
    for _ in range(len(hucreler) * 8 + 1000):
        halka.append(simdi)
        simdi, geri = tara(simdi, geri)
        if simdi is None or (simdi == bas and len(halka) > 2):
            break
    return halka


def sadelestir(nokta: list, eps: float) -> list:
    """Douglas-Peucker."""
    if len(nokta) < 3:
        return nokta
    x0, y0 = nokta[0]
    x1, y1 = nokta[-1]
    dx, dy = x1 - x0, y1 - y0
    uz = math.hypot(dx, dy) or 1e-9
    en_uzak, idx = 0.0, 0
    for i in range(1, len(nokta) - 1):
        x, y = nokta[i]
        d = abs(dy * x - dx * y + x1 * y0 - y1 * x0) / uz
        if d > en_uzak:
            en_uzak, idx = d, i
    if en_uzak <= eps:
        return [nokta[0], nokta[-1]]
    return sadelestir(nokta[:idx + 1], eps)[:-1] + sadelestir(nokta[idx:], eps)


# ---------------------------------------------------------------------------
# Uçtan uca
# ---------------------------------------------------------------------------

def capa_yolu(dosya: str) -> Path:
    return COMMONS / (Path(dosya).stem + ".capa.json")


def capalari_oku(dosya: str) -> tuple:
    """`<dosya>.capa.json` okur. Dönen: (çapalar, ton, kırpma).

    Kalibrasyon kaynak haritanın YANINDA, metin olarak durur: bir kez yapılır,
    git'e girer, kaynak dosya değişmedikçe yeniden kullanılır.
    """
    yol = capa_yolu(dosya)
    if not yol.exists():
        raise CapaYok(
            f"Çapa dosyası yok: {yol.name}\n"
            f"Şu iskeletle oluşturun (koordinatları --imlec ızgarasından okuyun):\n"
            f'{{"ton": [140, 175], "kirp": [sol, ust, sag, alt], "capalar": [\n'
            f'  {{"ad": "Kahire", "lon": 31.235, "lat": 30.044, "x": 0.195, "y": 0.392}}\n'
            f"]}}")
    d = json.loads(yol.read_text(encoding="utf-8"))
    capalar = [Capa(**c) for c in d["capalar"]]
    return capalar, tuple(d.get("ton", (140, 175))), tuple(d.get("kirp", ()))


def cikar(dosya: str, en_az_hucre: int = 60, eps: float = 1.6,
          tek_parca: bool = False) -> dict:
    """Sınırı çıkarır. Dönen sözlük: kalibrasyon, halkalar (lon/lat), maske bilgisi."""
    from PIL import Image
    kaynak = COMMONS / dosya
    if not kaynak.exists():
        raise FileNotFoundError(f"Kaynak harita yok: {kaynak}")
    capalar, ton, kirp = capalari_oku(dosya)
    kal = izdusum_coz(capalar)

    im = Image.open(kaynak).convert("RGB")
    if kirp:
        im = im.crop(tuple(int(v) for v in kirp))
    m, W, H = maske_uret(im, ton)
    ham = sum(m)
    m = temizle(m, W, H)

    parcalar = bilesenler(m, W, H)
    # Kaynağın arazi gölgeleri toprakla AYNI ton aralığına düşebilir ve mutlak
    # eşikle elenemeyecek kadar büyük sahte parçalar üretir (ölçüldü: Delhi
    # haritasında Himalayalar 11.039 ve 3.768 pikselik iki halka verdi -- gerçek
    # sınırın %34'ü ve %12'si). Devlet tek parçaysa çözüm nettir: en büyüğü tut.
    if tek_parca and parcalar:
        parcalar = parcalar[:1]
    halkalar, parca_bilgi = [], []
    for p in parcalar:
        if len(p) < en_az_hucre:
            continue
        h = kontur(p)
        s = sadelestir(h, eps)
        if len(s) < 8:
            continue
        halkalar.append([oran_to_lonlat(kal, (i + 0.5) / W, (j + 0.5) / H)
                         for i, j in s])
        parca_bilgi.append((len(p), len(h), len(s)))
    return {"kalibrasyon": kal, "halkalar": halkalar, "parcalar": parca_bilgi,
            "maske_ham": ham, "maske_temiz": sum(m), "olcu": (W, H),
            "gorsel": im, "ton": ton}


def bindirme_yaz(sonuc: dict, yol: Path) -> None:
    """Çıkarılan sınırı KAYNAĞIN ÜSTÜNE çizer — zorunlu gözle denetim adımı.

    Sayısal hiçbir ölçüt "maske yanlış yeri seçti" demez: kaynağın komşu bir
    devleti aynı tonda boyanmışsa maske onu da alır ve sonuç sessizce yanlış
    olur. Bindirme görseli bunu bir bakışta gösterir.
    """
    from PIL import ImageDraw
    im = sonuc["gorsel"].copy()
    kal = sonuc["kalibrasyon"]
    W, H = im.size
    d = ImageDraw.Draw(im)
    for halka in sonuc["halkalar"]:
        nokta = [lonlat_to_oran(kal, lon, lat) for lon, lat in halka]
        piksel = [(x * W, y * H) for x, y in nokta]
        if len(piksel) > 2:
            d.line(piksel + [piksel[0]], fill=(230, 0, 0), width=max(2, W // 400))
    im.save(yol)

def cizim_onizle(sonuc: dict, yol: Path, tema_hex: str = "#1D4E79") -> tuple:
    """Çıkarılan sınırı KENDİ MOTORUMUZLA çizip .svg olarak yazar.

    İki denetim birbirini tamamlar:
      * `bindirme.png` -> "çıkarım kaynağa uyuyor mu?"  (doğruluk)
      * `cizim.svg`    -> "sayfada nasıl görünecek?"     (kullanılabilirlik)

    Burada şehir konmaz ve çerçeve poligondan türetilir; amaç dersin nihai
    haritası değil, sınırın kendi motorumuzda makul durup durmadığını
    ders dosyasını yazmadan ÖNCE görmektir. Çıktı SVG'dir: tarayıcıda açılır,
    ek bir bağımlılık (Playwright vb.) gerekmez.
    """
    from cekirdek import harita_cizim
    from cekirdek.content_model import MapBox

    tum = [nokta for halka in sonuc["halkalar"] for nokta in halka]
    if not tum:
        return (), 0
    lons = [p[0] for p in tum]
    lats = [p[1] for p in tum]
    pay_x = (max(lons) - min(lons)) * 0.08 or 1.0
    pay_y = (max(lats) - min(lats)) * 0.08 or 1.0
    bbox = (min(lons) - pay_x, min(lats) - pay_y,
            max(lons) + pay_x, max(lats) + pay_y)
    mb = MapBox(region="(sınır önizlemesi)", bbox=bbox,
                territory=[[(a, b) for a, b in h] for h in sonuc["halkalar"]])
    try:
        yol.write_text(harita_cizim.svg_uret(mb, tema_hex), encoding="utf-8")
    except harita_cizim.VeriYok:
        return (), 0
    return bbox, len(tum)

def yukle(ad: str) -> list:
    """Çıkarılmış sınırı `MapBox.territory` biçiminde döndürür.

    Ders modüllerinin tek ihtiyacı budur:

        from cekirdek.sinir_cikar import yukle
        ...
        territory=yukle("memluk-sultanligi-1317"),

    Dosya yoksa BOŞ liste döner ve uyarı basar -- build DURMAZ. Gerekçe:
    `assets/harita/sinir/*.json` git'te durur ama üretmek için gereken raster
    kaynak `.gitignore`'dadır; depoyu klonlayan biri sınırı yeniden üretemez,
    o yüzden eksik bir sınır dersi çökertmemeli. Harita o zaman alanı boş,
    yalnızca coğrafya ve şehirlerle çizilir.
    """
    yol = SINIR / f"{ad}.json"
    if not yol.exists():
        print(f"[UYARI] Sınır dosyası yok: {yol.name} -- harita alansız çizilecek. "
              f"Üretmek için: python tools/harita.py --sinir-cikar <kaynak>")
        return []
    veri = json.loads(yol.read_text(encoding="utf-8"))
    return [[(lon, lat) for lon, lat in halka] for halka in veri["halkalar"]]

# ---------------------------------------------------------------------------
# VEKTÖR KAYNAK: SVG'yi rasterleştirip BİREBİR RENKLE bant çıkarma
# ---------------------------------------------------------------------------
# Commons'taki SVG haritalar düz vektör renkleri kullanır (Rum Selçuklu:
# #412424/#754142/#a3595b/#bf8b8c). Raster kaynaklarda ton PENCERESİ gerekiyordu
# çünkü arazi gölgesi rengi sürekli kaydırıyordu; burada renk TAM olduğu için
# birebir eşleme yapılır ve maske çok daha temiz çıkar.
#
# Neden SVG'yi doğrudan parse etmiyoruz: path'ler transform zincirleri, clip
# ve grup opaklıklarıyla birlikte gelir; hepsini doğru çözmek bir SVG motoru
# yazmak demektir. Rasterleştirip renk eşlemek aynı sonucu verir ve zaten
# elimizde olan boru hattını (maske -> kontur -> sadeleştir) yeniden kullanır.

def renk_maskesi(im, hedef_hex: str, tolerans: int = 26) -> tuple:
    """Verilen RENGE yakın pikselleri işaretler. (maske, W, H).

    `tolerans` kanal başına en büyük sapmadır; kenar yumuşatma (anti-aliasing)
    ve JPEG olmayan rasterleştirmede 26 ölçülü bir değerdir -- bandın içini
    tamamen alır, komşu bandı almaz (Rum Selçuklu'da en yakın iki ton arasında
    kanal farkı ~50'dir).
    """
    from PIL import Image
    oran = im.width / im.height
    W = TARAMA_GENISLIK
    H = max(1, round(W / oran))
    px = im.resize((W, H), Image.LANCZOS).load()
    hr, hg, hb = (int(hedef_hex[i:i + 2], 16) for i in (1, 3, 5))
    m = bytearray(W * H)
    for j in range(H):
        for i in range(W):
            r, g, b = px[i, j]
            if abs(r - hr) <= tolerans and abs(g - hg) <= tolerans and abs(b - hb) <= tolerans:
                m[j * W + i] = 1
    return m, W, H


def svg_rasterlestir(dosya: str, genislik: int = 1800):
    """Commons SVG'sini PIL görüntüsüne çevirir (Chromium ile).

    Playwright zaten build.py'nin bağımlılığıdır, yani yeni bir gereksinim
    getirmez. Genişlik yüksek tutulur: kontur hassasiyeti buradan gelir.
    """
    import asyncio, tempfile
    from PIL import Image
    from playwright.async_api import async_playwright

    svg = (COMMONS / dosya).read_text(encoding="utf-8")
    gecici = Path(tempfile.gettempdir()) / f"_sinir_{Path(dosya).stem}.html"
    gecici.write_text(
        f'<html><body style="margin:0;background:#fff">'
        f'<div style="width:{genislik}px">{svg}</div></body></html>', encoding="utf-8")
    png = gecici.with_suffix(".png")

    async def calis():
        async with async_playwright() as pw:
            b = await pw.chromium.launch()
            pg = await b.new_page(viewport={"width": genislik, "height": 1200})
            await pg.goto(gecici.as_uri())
            await pg.wait_for_timeout(400)
            await pg.screenshot(path=str(png), full_page=True)
            await b.close()

    asyncio.run(calis())
    return Image.open(png).convert("RGB")


def katman_cikar(dosya: str, renkler: list, etiketler: list,
                 en_az_hucre: int = 40, eps: float = 1.6,
                 tolerans: int = 26) -> dict:
    """SVG kaynağından HER RENK BANDINI ayrı katman olarak çıkarır.

    `renkler` ESKİDEN YENİYE (koyudan açığa) sıralı kaynak hex listesidir;
    `etiketler` aynı sırada Türkçe lejant metinleridir.
    """
    capalar, _ton, kirp = capalari_oku(dosya)
    kal = izdusum_coz(capalar)
    im = svg_rasterlestir(dosya)
    if kirp:
        im = im.crop(tuple(int(v) for v in kirp))

    katmanlar, bilgi = [], []
    for renk, etiket in zip(renkler, etiketler):
        m, W, H = renk_maskesi(im, renk, tolerans)
        ham = sum(m)
        m = temizle(m, W, H, tur=2)
        halkalar = []
        for parca in bilesenler(m, W, H):
            if len(parca) < en_az_hucre:
                continue
            sade = sadelestir(kontur(parca), eps)
            if len(sade) < 8:
                continue
            halkalar.append([oran_to_lonlat(kal, (i + 0.5) / W, (j + 0.5) / H)
                             for i, j in sade])
        katmanlar.append({"halkalar": halkalar, "etiket": etiket})
        bilgi.append((renk, etiket, ham, len(halkalar)))
    return {"kalibrasyon": kal, "katmanlar": katmanlar, "bilgi": bilgi,
            "gorsel": im, "olcu": (TARAMA_GENISLIK, 0)}

def katman_yukle(ad: str) -> list:
    """Çok katmanlı sınırı `MapBox.katmanlar` biçiminde döndürür.

        katmanlar=katman_yukle("rum-selcuklu-genisleme-1100-1240"),

    `yukle()` ile aynı gerekçeyle dosya yoksa boş liste döner ve uyarır.
    """
    yol = SINIR / f"{ad}.json"
    if not yol.exists():
        print(f"[UYARI] Katman dosyası yok: {yol.name} -- harita alansız çizilecek.")
        return []
    veri = json.loads(yol.read_text(encoding="utf-8"))
    return [{"etiket": k["etiket"],
             "halkalar": [[(lon, lat) for lon, lat in h] for h in k["halkalar"]]}
            for k in veri.get("katmanlar", [])]
