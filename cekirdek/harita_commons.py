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
WIKIMEDIA COMMONS HARİTALARI — hazır tarihî haritayı derse uyarlar
===================================================================

`cekirdek/harita_cizim.py` haritayı SIFIRDAN çizer (Natural Earth + gerçek
koordinat); bu modül ise Commons'taki PROFESYONEL bir tarihî haritayı alır ve
ders kitabına uyarlar: lejantı Türkçeleştirir, renkleri dersin temasına çeker,
yazı tipini kitabınkiyle eşler.

NE ZAMAN HANGİSİ?
-----------------
* `harita_cizim` — konum/çerçeve göstermek yeterliyse; sınırlar YAKLAŞIKtır
  ve öyle etiketlenir. Bağımlılığı ve lisans yükümlülüğü yoktur (CC0 veri).
* `harita_commons` — bölüm gerçek bir tarihî sınır/genişleme anlatıyorsa.
  Sınırlar kaynağın kartografının çizimidir; bizim tahminimiz değildir.

LİSANS — CİDDİYE ALIN
---------------------
Kullanılan dosyalar çoğunlukla **CC BY-SA 4.0**'dır. İki yükümlülük doğurur:

1. **Atıf**: yazar + lisans + kaynak bağlantısı görünür olmalıdır. Bu yüzden
   `CommonsKaynak.atif` ZORUNLU alandır ve harita kutusunun altındaki
   `.geomap-source` satırında HER ZAMAN basılır (bkz. build.haritalari_coz).
2. **Aynı lisansla paylaşım (ShareAlike)**: burada yaptığımız her şey
   (lejantı çevirmek, rengi değiştirmek) bir UYARLAMADIR; uyarlanmış harita
   da CC BY-SA 4.0'dır. Bu, deponun GPL-3.0 lisansını değiştirmez -- harita
   ayrı bir varlıktır ve kendi lisansını taşır. `assets/harita/commons/
   LISANS.md` her dosyanın künyesini tutar; yeni dosya eklerken oraya da
   satır ekleyin.

Kaynak SVG'yi ELLE DÜZENLEMEYİN: dosya Commons'tan geldiği gibi durur,
dönüşüm burada, kod içinde yapılır. Böylece dosya güncellenirse uyarlama
yeniden uygulanabilir ve neyi değiştirdiğimiz kayıt altındadır.
"""

from __future__ import annotations

import base64
import re
from dataclasses import dataclass, field
from pathlib import Path

from cekirdek.harita_cizim import _hex, _hsl

ROOT = Path(__file__).resolve().parents[1]
COMMONS = ROOT / "assets" / "harita" / "commons"

# Eskiden CommonsKaynak/CommonsGorsel alanıydılar; hiçbir ders varsayılandan
# başka bir değer vermediği için sabitleştirildiler (2026-08-31). Gerçekten
# derse göre değişmesi gerekirse alan olarak geri eklenebilirler.
YAZITIPI = "'DejaVu Sans', sans-serif"   # kitabın gövde yazı tipiyle aynı
HALE_KALINLIK = 2.6      # etiket çevresindeki beyaz hale (viewBox birimi)
EN_FAZLA_PX = 1400       # raster: 82mm sütunda ~430 dpi, fotokopi için fazlasıyla yeter
JPEG_KALITE = 88
TON_PARLAKLIK = 0.86     # <1 koyulaştırır
TON_DOYGUNLUK = 0.55     # hedef doygunluk tavanı


@dataclass
class CommonsKaynak:
    """Commons'tan alınmış bir haritanın derse uyarlanma tarifi."""
    dosya: str                                   # assets/harita/commons/ altındaki ad
    atif: str                                    # ZORUNLU: yazar + lisans + bağlantı
    metin: dict = field(default_factory=dict)    # {"eski etiket": "yeni etiket"}
    # Etiket rengi değişimi: {eski_hex: yeni_hex}. Renk uyarlaması kontrastı
    # BOZABİLİR -- kaynak haritada sarı etiketler koyu bordo zemine göre
    # seçilmişti; zemini açık maviye çekince okunmaz oldular.
    metin_renk: dict = field(default_factory=dict)

    # ---------------- YAN SÜTUN KİPİ (add_map(..., taraf="sag"/"sol")) -----
    # Bir tarihî harita genelde GENİŞTİR ve tam sayfa genişliği (186mm) için
    # çizilmiştir; 82mm'lik metin-yanı sütuna olduğu gibi konursa okunmaz.
    # ÖLÇÜLDÜ (Rum Selçuklu haritası, viewBox 1577.9 x 721.3 = 2.19:1):
    # 82mm sütunda yükseklik 37mm'ye, şehir etiketi 19.5 birimden ~2.9pt'ye
    # düşüyor.
    #
    # Üç ayar BİRLİKTE çalışır, biri tek başına yetmez:
    #   kirp        -> yakınlaştırır (aynı etiket daha az birimlik alana düşer)
    #   sil_desen   -> ikincil etiketleri atıp kalabalığı azaltır
    #   yazi_olcek  -> etiketi FİZİKSEL olarak tam sayfadakiyle aynı boya çıkarır
    #
    # Ölçüt basit: `yazi_olcek` ≈ kırpmanın yakınlaştırma katsayısı
    # (eski genişlik / yeni genişlik). O zaman etiketler haritaya ORANLA aynı
    # kalır -- yani kalabalıklaşmaz -- ama kutu küçüldüğü için sayfada daha az
    # yer kaplar.
    kirp: tuple = ()          # (x, y, genişlik, yükseklik) -- viewBox'ı daraltır
    yazi_olcek: float = 1.0   # her font-size değeri bununla çarpılır
    # `yazi_araligi=(alt, ust)` verilirse çarpan yerine ARALIK SIKIŞTIRMA
    # uygulanır: kaynağın punto sıralaması korunur ama hepsi bu aralığa
    # (viewBox birimi) çekilir. Kaynak geniş bir yelpaze kullanıyorsa
    # (Moğol haritası: şehir 8px, ülke 21px) düz çarpan işe yaramaz --
    # şehri okunur yapan çarpan ülke adını haritanın üstüne taşırır.
    yazi_araligi: tuple = ()
    sil_desen: str = ""       # bu regex'e uyan <text>/<tspan> içerikleri silinir
    # `koru` doluysa TERSİ çalışır: yalnızca listedeki etiketler kalır, geri
    # kalan bütün <text> düğümleri silinir. Çok etiketli kaynak haritalar için
    # (Moğol haritasında 139 etiket var; 82mm sütunda okunabilir üst sınır
    # ~16). Karşılaştırma boşluktan bağımsızdır: kaynakta iki satıra bölünmüş
    # "Mamluk"/"Sultanate" tspan'leri "Mamluk Sultanate" yazımıyla eşleşir.
    koru: list = field(default_factory=list)
    # Lejantı SVG'den söküp HTML'e taşır. Yan sütunda ŞART: kaynaktaki lejant
    # kutusu haritanın %43'ü kadar geniştir; küçülünce hem kendisi okunmaz olur
    # hem de haritanın güneydoğusunu kapatır. HTML'e taşınınca sayfanın kendi
    # tipografisiyle (7pt) basılır, yani her ölçekte okunur kalır.
    lejant: bool = False
    # Kaynakta ÇİZİLİ bir lejant kutusu yoksa (bazı haritalarda renklerin
    # anlamı yalnızca Commons dosya sayfasında yazar) lejant elle verilir:
    # {kaynak_hex: "Türkçe açıklama"}. Anahtarlar KAYNAK renkleridir; tema
    # eşlemesinden geçirilir, yani HTML lejant haritadaki son renkleri gösterir.
    # `lejant=True` ile birlikte kullanılırsa sökülen lejantın yerine geçer.
    lejant_elle: dict = field(default_factory=dict)


class KaynakYok(FileNotFoundError):
    """Commons SVG'si diskte yok."""


def _renkleri_degistir(svg: str, esleme: dict) -> str:
    """fill="#xxx" ve fill:#xxx biçimlerinin ikisini de değiştirir.

    Inkscape çıktısı aynı rengi iki ayrı sözdiziminde yazabiliyor; yalnızca
    birini aramak haritanın yarısını eski renkte bırakır.
    """
    def degis(m):
        yeni = esleme.get(m.group(2).lower())
        return f"{m.group(1)}{yeni}" if yeni else m.group(0)
    return re.sub(r'(fill\s*[:=]\s*"?)(#[0-9a-fA-F]{6})', degis, svg)


def _metinleri_degistir(svg: str, esleme: dict) -> tuple[str, list]:
    """<text>/<tspan> içeriklerini birebir eşleşmeye göre değiştirir.

    Bulunamayan her anahtar RAPORLANIR: kaynak dosya Commons'ta güncellenip
    bir etiket değişirse, çeviri sessizce düşmesin (harita İtalyanca lejantla
    basılmasın) diye build uyarı verir.
    """
    bulunmayan = []
    for eski, yeni in esleme.items():
        # textPath: etiket düz değil, bir eğri boyunca akıyor (Moğol haritası).
        desen = re.compile(r"(>)(\s*)" + re.escape(eski) + r"(\s*)(</(?:text|tspan|textPath)>)")
        svg, n = desen.subn(lambda m: m.group(1) + m.group(2) + yeni + m.group(3) + m.group(4), svg)
        if n == 0:
            bulunmayan.append(eski)
    return svg, bulunmayan


def _sadelestir(svg: str) -> str:
    """Inkscape artıklarını atar ve gömülmeye hazırlar.

    - <metadata> bloğu (RDF künyesi) sayfaya hiçbir şey katmaz, yüzlerce KB tutar.
      DİKKAT: atıf bilgisi buradan DEĞİL, CommonsKaynak.atif'ten gelir; künyeyi
      atmak atfı ortadan kaldırmaz.
    - sodipodi:/inkscape: öznitelikleri tarayıcı tarafından yok sayılır.
    - id="..." öznitelikleri: birden çok harita tek HTML'e gömüldüğü için id
      çakışması riskini kökten kesiyoruz -- AMA yalnızca hiçbir yerden
      REFERANS VERİLMEYEN id'ler atılır.

    Son madde ölçülmüş bir tuzaktır: Moğol haritasındaki eğri boyunca akan
    ülke adları `<textPath xlink:href="#SVGID_x5F_3_x5F_">` ile yazılmıştır.
    Bütün id'ler koşulsuz silinince o etiketlerin bağlandığı yol kayboluyor
    ve harita adsız kalıyordu. Bu yüzden önce belgedeki `href="#..."`,
    `xlink:href="#..."` ve `url(#...)` referansları toplanır; yalnızca
    kullanılmayan id'ler atılır.
    """
    svg = re.sub(r"<metadata[^>]*>.*?</metadata>", "", svg, flags=re.S)
    svg = re.sub(r"<(?:sodipodi|inkscape):[^>]*?/>", "", svg)
    svg = re.sub(r'\s(?:sodipodi|inkscape):[\w-]+\s*=\s*"[^"]*"', "", svg)
    kullanilan = set(re.findall(r'(?:xlink:)?href\s*=\s*"#([^"]+)"', svg))
    kullanilan |= set(re.findall(r"url\(#([^)]+)\)", svg))
    svg = re.sub(r'\sid\s*=\s*"([^"]*)"',
                 lambda m: m.group(0) if m.group(1) in kullanilan else "", svg)
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    svg = re.sub(r"\n\s*\n+", "\n", svg)
    return svg


# ---------------------------------------------------------------------------
# YAN SÜTUN KİPİ: küçültme dönüşümleri
# Hepsi kaynak dosyaya DOKUNMADAN, metin üzerinde çalışır; kaynak SVG diskte
# Commons'tan geldiği gibi durur (bkz. modül başlığı).
# ---------------------------------------------------------------------------

def _sayi(etiket: str, oznitelik: str) -> float | None:
    """Bir SVG etiketinden sayısal özniteliği okur (yoksa None)."""
    m = re.search(oznitelik + r'\s*=\s*"([-\d.eE]+)"', etiket)
    return float(m.group(1)) if m else None


def _konum(etiket: str) -> tuple | None:
    """Bir düğümün yerleşim noktasını (x, y) verir.

    İki yazım da kullanılıyor: Inkscape x="..." y="..." yazar (Rum Selçuklu
    haritası), Illustrator ise transform="matrix(a b c d e f)" ile taşır
    (Moğol haritası) -- orada nokta (e, f)'dir.
    """
    x, y = _sayi(etiket, "x"), _sayi(etiket, "y")
    if x is not None and y is not None:
        return x, y
    m = re.search(r"transform\s*=\s*\"matrix\(([^)]*)\)\"", etiket)
    if m:
        parcalar = [p for p in re.split(r"[\s,]+", m.group(1).strip()) if p]
        if len(parcalar) == 6:
            try:
                return float(parcalar[4]), float(parcalar[5])
            except ValueError:
                return None
    return None


def _sinif_dolgulari(svg: str) -> dict:
    """<style> bloğundaki `.stNN { fill:#XXXXXX }` kurallarını sözlüğe çevirir.

    Illustrator çıktısı rengi elemanın üstünde değil CSS sınıfında tutar;
    lejant kutusunu tanımak için sınıfın rengini çözebilmek gerekir.
    """
    stil = " ".join(re.findall(r"<style[^>]*>(.*?)</style>", svg, flags=re.S))
    sonuc = {}
    for ad, govde in re.findall(r"\.([\w-]+)\s*\{([^}]*)\}", stil):
        m = re.search(r"fill\s*:\s*(#[0-9a-fA-F]{6})", govde)
        if m:
            sonuc[ad] = m.group(1).lower()
    return sonuc


def _dolgu(etiket: str, sinif_dolgu: dict | None = None) -> str:
    """Elemanın dolgu rengi: önce üstündeki fill, yoksa CSS sınıfından."""
    m = re.search(r'fill\s*[:=]\s*"?(#[0-9a-fA-F]{6})', etiket)
    if m:
        return m.group(1).lower()
    if sinif_dolgu:
        for ad in re.findall(r'class\s*=\s*"([^"]*)"', etiket):
            for parca in ad.split():
                if parca in sinif_dolgu:
                    return sinif_dolgu[parca]
    return ""


def _aydinlik(renk: str) -> float:
    """Kaba parlaklık (0-1). Lejant çerçevesi her zaman AÇIK bir kutudur."""
    if not renk:
        return 0.0
    r, g, b = (int(renk[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return 0.299 * r + 0.587 * g + 0.114 * b


def _duz_metin(dugum: str) -> str:
    """Bir <text> düğümünün etiketlerden arındırılmış içeriği."""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", dugum)).strip()


def _yaziyi_sil(svg: str, desen: str = "", koru: list | None = None) -> tuple[str, int]:
    """Etiket ayıklama: `desen`e uyanları siler, `koru` verilirse geri kalanı siler.

    İki ayrı ihtiyaç, tek işlev:

    * `desen` — İKİNCİL bir katmanı atmak için. Rum Selçuklu haritasında
      şehir adlarının altındaki antik karşılıklar (`(Sebaste)`, `(Iconio)`):
      yan sütun ölçeğinde okunmuyor, sadece asıl adı gölgeliyorlardı.
    * `koru` — kaynak harita ÇOK etiketliyse tersini yapmak için: yalnızca
      listedeki etiketler kalır. Moğol haritasında 139 etiket var; 82mm'lik
      sütunda okunabilir üst sınır ~16'dır, yani ayıklamak şart.

    Karşılaştırma boşluklardan bağımsızdır: kaynakta iki satıra bölünmüş
    `Mamluk`/`Sultanate` tspan'leri "Mamluk Sultanate" yazımıyla eşleşir.
    """
    sayac = 0
    d = re.compile(desen) if desen else None
    korunan = {re.sub(r"\s+", "", k) for k in (koru or [])}

    def text_ele(m):
        nonlocal sayac
        icerik = _duz_metin(m.group(0))
        if not icerik:
            return m.group(0)
        if korunan and re.sub(r"\s+", "", icerik) not in korunan:
            sayac += 1
            return ""
        if d and d.search(icerik):
            sayac += 1
            return ""
        return m.group(0)

    svg = re.sub(r"<text\b[^>]*>.*?</text>", text_ele, svg, flags=re.S)

    if d:
        def tspan_ele(m):
            nonlocal sayac
            if d.search(_duz_metin(m.group(0))):
                sayac += 1
                return ""
            return m.group(0)
        svg = re.sub(r"<tspan\b[^>]*>.*?</tspan>", tspan_ele, svg, flags=re.S)
    return svg, sayac


def _font_boylari(svg: str) -> list:
    """Belgedeki bütün font-size değerleri (style bloğu + öznitelik)."""
    return [float(v) for v in
            re.findall(r"font-size\s*[:=]\s*\"?([\d.]+)", svg)]


def _yazi_araligina_sikistir(svg: str, alt: float, ust: float) -> str:
    """Punto hiyerarşisini KORUR ama aralığını [alt, ust]'e sıkıştırır.

    Neden çarpan yetmiyor: kaynak haritalar geniş bir punto yelpazesi
    kullanır (Moğol haritasında şehir 8px, ülke 21px). Hepsini aynı sayıyla
    çarpınca ya şehir okunmaz kalıyor ya da ülke adı haritayı eziyor.
    Doğrusal yeniden eşleme en küçüğü okunur tabana çeker, en büyüğü tavanda
    tutar; sıralama (şehir < deniz < ülke) aynen korunur.
    """
    boylar = _font_boylari(svg)
    if not boylar:
        return svg
    kucuk, buyuk = min(boylar), max(boylar)

    def yeni(eski: float) -> float:
        if buyuk - kucuk < 1e-6:
            return (alt + ust) / 2
        return alt + (eski - kucuk) / (buyuk - kucuk) * (ust - alt)

    svg = re.sub(r"(font-size\s*:\s*)([\d.]+)(px)?",
                 lambda m: "%s%.3f%s" % (m.group(1), yeni(float(m.group(2))), m.group(3) or ""),
                 svg)
    svg = re.sub(r'(font-size\s*=\s*")([\d.]+)',
                 lambda m: "%s%.3f" % (m.group(1), yeni(float(m.group(2)))), svg)
    return svg


def _yazi_olcekle(svg: str, k: float) -> str:
    """Bütün font-size değerlerini k ile çarpar (hem style hem öznitelik)."""
    if k == 1.0:
        return svg
    svg = re.sub(r"(font-size\s*:\s*)([\d.]+)(px)?",
                 lambda m: "%s%.4f%s" % (m.group(1), float(m.group(2)) * k, m.group(3) or ""),
                 svg)
    svg = re.sub(r'(font-size\s*=\s*")([\d.]+)',
                 lambda m: "%s%.4f" % (m.group(1), float(m.group(2)) * k), svg)
    return svg


def _lejanti_cikar(svg: str) -> tuple[str, list]:
    """Lejant kutusunu SVG'den söker ve (renk, metin) çiftlerini döndürür.

    Kimlik GEOMETRİKTİR, id'ye bakmaz: kaynak dosya Commons'ta güncellenip
    id'leri değişse de çalışsın diye. Aranan şey, içinde en az iki RENKLİ
    dikdörtgen (örnek kutucuk) barındıran, AÇIK renkli küçük bir çerçevedir.

    Üç eleme ölçülerek kondu, gevşetmeyin:
    * **Alan sınırı (%0,3 - %25).** Moğol haritasının deniz zemini tüm
      levhayı kaplayan tek bir açık renkli dikdörtgendir ve lejant kutusunu
      da içine alır; sınır olmadan "çerçeve" o seçiliyordu.
    * **En KÜÇÜK aday kazanır.** Lejant kutusu küçüktür; büyükten başlamak
      onu içeren herhangi bir paneli seçme riski taşır.
    * **Dolgusu olmayan örnekler atlanır.** Illustrator kutucukların üstüne
      bir de `fill:none` çerçeve dikdörtgeni koyuyor; sayılsaydı lejant
      yedi yerine on dört satır çıkardı.

    Bulunamazsa SVG'ye DOKUNULMAZ ve boş liste döner; çağıran taraf uyarır.
    Böylece harita sessizce lejantsız -- yani anlamsız -- basılmaz.
    """
    sinif_dolgu = _sinif_dolgulari(svg)
    m_vb = re.search(r'viewBox\s*=\s*"([\d.\s+-]+)"', svg)
    levha = 0.0
    if m_vb:
        p = m_vb.group(1).split()
        if len(p) == 4:
            levha = float(p[2]) * float(p[3])

    kutular = []
    for m in re.finditer(r"<rect\b[^>]*/>", svg):
        etiket = m.group(0)
        x, y = _sayi(etiket, "x"), _sayi(etiket, "y")
        g, yuk = _sayi(etiket, "width"), _sayi(etiket, "height")
        if None in (x, y, g, yuk):
            continue
        kutular.append({"bas": m.start(), "son": m.end(), "x": x, "y": y,
                        "x2": x + g, "y2": y + yuk, "alan": g * yuk,
                        "renk": _dolgu(etiket, sinif_dolgu)})

    def icinde(k, cerceve):
        return (cerceve["x"] <= k["x"] and cerceve["y"] <= k["y"]
                and k["x2"] <= cerceve["x2"] and k["y2"] <= cerceve["y2"])

    cerceve, ornekler = None, []
    for aday in sorted(kutular, key=lambda k: k["alan"]):
        if _aydinlik(aday["renk"]) < 0.80:
            continue
        if levha and not (0.003 * levha <= aday["alan"] <= 0.25 * levha):
            continue
        icerdekiler = [k for k in kutular
                       if k is not aday and k["renk"] and icinde(k, aday)]
        if len(icerdekiler) >= 2:
            cerceve, ornekler = aday, sorted(icerdekiler, key=lambda k: k["y"])
            break
    if cerceve is None:
        return svg, []

    yazilar = []
    for m in re.finditer(r"<text\b[^>]*>.*?</text>", svg, flags=re.S):
        etiket = m.group(0)[:m.group(0).find(">") + 1]
        nokta = _konum(etiket)
        if nokta is None:
            continue
        x, y = nokta
        if cerceve["x"] <= x <= cerceve["x2"] and cerceve["y"] <= y <= cerceve["y2"]:
            yazilar.append({"bas": m.start(), "son": m.end(), "y": y,
                            "metin": _duz_metin(m.group(0))})

    ogeler = []
    for ornek in ornekler:
        orta = (ornek["y"] + ornek["y2"]) / 2
        eslesen = min(yazilar, key=lambda t: abs(t["y"] - orta), default=None)
        if eslesen is not None and eslesen["metin"]:
            ogeler.append((ornek["renk"], eslesen["metin"]))

    # Sökme SONDAN BAŞA: indeksler kaymasın. Çerçevenin içindeki HER
    # dikdörtgen gider -- dolgusuz olanlar lejant satırı saymıyor ama
    # sökülmezlerse haritanın üstünde boş kutucuk iskeleti kalır.
    icteki_hepsi = [k for k in kutular if k is not cerceve and icinde(k, cerceve)]
    kesitler = sorted([(k["bas"], k["son"]) for k in icteki_hepsi]
                      + [(cerceve["bas"], cerceve["son"])]
                      + [(t["bas"], t["son"]) for t in yazilar], reverse=True)
    for bas, son in kesitler:
        svg = svg[:bas] + svg[son:]
    # Lejant tek bir <g> içindeyse geriye boş bir kabuk kalır.
    svg = re.sub(r"<g\b[^>]*>\s*</g>", "", svg)
    return svg, ogeler


def _kirp(svg: str, kutu: tuple) -> str:
    """viewBox'ı daraltır: harita yakınlaşır, dışarısı kırpılır.

    SVG kökü kendi görüntü alanını zaten kırptığı için dışarıda kalan yollar
    SİLİNMEDEN gizlenir -- yani kaynağın geometrisi bozulmaz, yalnızca
    çerçeve daralır.
    """
    x, y, g, yuk = (float(v) for v in kutu)
    return re.sub(r'viewBox\s*=\s*"[^"]*"',
                  'viewBox="%.2f %.2f %.2f %.2f"' % (x, y, g, yuk), svg, count=1)


def _viewbox_tamamla(svg: str) -> str:
    """viewBox'ı olmayan dosyaya width/height'tan bir viewBox türetir.

    Her Commons dosyasında viewBox yok (Inkscape yalnızca width/height
    yazabiliyor). Kutuya sığdırmak için width/height'ı %100 yapıyoruz; viewBox
    yoksa o anda koordinat sistemi de kaybolur ve harita ya devasa ya da
    kırpılmış çıkar. Ölçüldü: Orta Doğu 1328 haritası ekrana sığmayan gri bir
    dikdörtgen olarak basılıyordu.
    """
    if re.search(r'viewBox\s*=\s*"', svg):
        return svg
    kok = svg[svg.find("<svg"): svg.find(">", svg.find("<svg")) + 1]
    g, y = _sayi(kok, "width"), _sayi(kok, "height")
    if not g or not y:
        return svg
    return svg.replace("<svg", f'<svg viewBox="0 0 {g:.4f} {y:.4f}"', 1)


def _olcu(svg: str) -> tuple[str, str]:
    """viewBox'tan (oran_metni, viewBox) döndürür; kutunun en-boy oranı budur."""
    m = re.search(r'viewBox\s*=\s*"([\d.\s+-]+)"', svg)
    if not m:
        return "4 / 3", ""
    parcalar = m.group(1).split()
    if len(parcalar) != 4:
        return "4 / 3", m.group(1)
    g, y = float(parcalar[2]), float(parcalar[3])
    return f"{g:.0f} / {y:.0f}", m.group(1)


def uyarla(kaynak: CommonsKaynak) -> tuple[str, str, list, list]:
    """Commons SVG'sini derse uyarlar.

    Dönen: (svg_metni, css_en_boy_orani, bulunamayan_metin_anahtarlari,
            lejant_ogeleri)

    `lejant_ogeleri` yalnızca `CommonsKaynak.lejant` açıkken doludur:
    [(renk_hex, "etiket"), ...] -- şablon bunları haritanın ALTINDA HTML
    lejant olarak basar (bkz. templates/_ders_govde.html.j2).
    """
    yol = COMMONS / kaynak.dosya
    if not yol.exists():
        raise KaynakYok(
            f"Commons haritası yok: {yol}\n"
            f"İndirmek için: python tools/harita.py --commons-indir")
    svg = yol.read_text(encoding="utf-8")

    svg = _sadelestir(svg)
    svg = _viewbox_tamamla(svg)
    svg, bulunmayan = _metinleri_degistir(svg, kaynak.metin)
    if kaynak.metin_renk:
        svg = _renkleri_degistir(svg, {k.lower(): v for k, v in kaynak.metin_renk.items()})
    # SIRA ÖNEMLİ: önce lejant sökülür, sonra etiketler ayıklanır.
    # Lejant çeviriden SONRA sökülür ki HTML'e Türkçe geçsin; ayıklamadan
    # ÖNCE sökülür ki `koru` listesi lejant satırlarını da yazmak zorunda
    # kalmasın (lejant zaten SVG'den çıkmış olur).
    lejant_ogeleri = []
    if kaynak.lejant:
        svg, lejant_ogeleri = _lejanti_cikar(svg)
    if kaynak.lejant_elle:
        # Elle yazılan lejant: anahtarlar haritadaki GERÇEK renklerdir --
        # kaynağın renkleri artık değiştirilmediği için kutucuk alanla aynı tonda.
        lejant_ogeleri = [(k.lower(), v) for k, v in kaynak.lejant_elle.items()]
    svg, _silinen = _yaziyi_sil(svg, kaynak.sil_desen, kaynak.koru)
    svg = re.sub(r"(font-family\s*:\s*)([^;\"']+)", r"\1" + YAZITIPI, svg)
    svg = re.sub(r'font-family\s*=\s*"[^"]*"', f'font-family="{YAZITIPI}"', svg)
    if kaynak.yazi_araligi:
        if len(kaynak.yazi_araligi) != 2:
            raise ValueError(
                f"CommonsKaynak.yazi_araligi (alt, ust) olmalı; "
                f"verilen: {kaynak.yazi_araligi!r}")
        svg = _yazi_araligina_sikistir(svg, *kaynak.yazi_araligi)
    svg = _yazi_olcekle(svg, kaynak.yazi_olcek)
    # paint-order:stroke -> hale metnin ALTINA çizilir, harfleri inceltmez.
    # Tek <style> ile bütün etiketlere uygulanır; kaynak dosyaya dokunulmaz.
    # Hale kalınlığı yazıyla birlikte ölçeklenir, yoksa büyütülmüş etiketin
    # çevresinde saç teli gibi kalır.
    stil = ("<style>text,tspan{paint-order:stroke;stroke:#FFFFFF;"
            "stroke-width:%.2fpx;stroke-linejoin:round;stroke-opacity:.92;}</style>"
            % (HALE_KALINLIK * kaynak.yazi_olcek))
    svg = re.sub(r"(<svg\b[^>]*?>)", lambda m: m.group(1) + stil, svg, count=1)
    if kaynak.kirp:
        if len(kaynak.kirp) != 4:
            raise ValueError(
                f"CommonsKaynak.kirp 4 sayı olmalı (x, y, genişlik, yükseklik); "
                f"verilen: {kaynak.kirp!r}")
        svg = _kirp(svg, kaynak.kirp)

    oran, _vb = _olcu(svg)
    # Kutuya sığsın: sabit width/height yerine %100 (viewBox ölçeği korur).
    svg = re.sub(r'(<svg\b[^>]*?)\swidth\s*=\s*"[^"]*"', r"\1", svg, count=1)
    svg = re.sub(r'(<svg\b[^>]*?)\sheight\s*=\s*"[^"]*"', r"\1", svg, count=1)
    svg = svg.replace("<svg", '<svg width="100%" height="100%"', 1)
    return svg, oran, bulunmayan, lejant_ogeleri


# ===========================================================================
# HAZIR RASTER HARİTA (PNG / JPG)
# ---------------------------------------------------------------------------
# Vikipedi maddelerindeki tarihî haritaların ÇOĞU vektör değil, raster'dır.
# SVG yolu (yukarısı) onları hiç göremiyordu; bu bölüm o boşluğu kapatır.
#
# NE KAYBEDERİZ: raster'da etiket çevrilemez, ayıklanamaz, renk değiştirilemez.
# Harita olduğu gibi, kendi dilinde ve kendi renkleriyle girer. Elimizde kalan
# tek uyarlama piksel KIRPMAsıdır (lejant kutusunu ya da boş kenarı atmak).
#
# NE KAZANIRIZ: kartografın asıl çizimi. Bir devletin gerçek sınırlarını
# gösteren en iyi harita çoğu zaman raster'dır.
# ===========================================================================

MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif"}


@dataclass
class Isaret:
    """Haritanın ÜSTÜNE bindirilen tek bir yer imleci (nokta + Türkçe etiket).

    `x`/`y` KIRPILMIŞ görselin oranıdır (0-1, sol üstten). Oran kullanılmasının
    sebebi: kırpmayı ya da küçültmeyi sonradan değiştirsek de imleç kaymaz.

    İmleç görüntünün İÇİNE ÇİZİLMEZ, üstüne HTML katmanı olarak konur. Üç
    sebeple: (1) baskıda vektör keskinliği -- 430 dpi'lık bir raster'a gömülen
    yazı bulanıklaşır; (2) etiket Türkçe ve sayfanın kendi yazı tipiyle olur;
    (3) yanlış yere düşen bir imleç tek satır düzenlemeyle taşınır, görüntü
    yeniden üretilmez.

    KURAL: yalnızca bölümün METNİNDE geçen yerler işaretlenir.
    """
    ad: str
    x: float
    y: float
    yan: str = "sag"          # etiketin noktaya göre yönü: "sag" | "sol"


@dataclass
class CommonsGorsel:
    """Commons'taki hazır RASTER haritanın derse bağlanma tarifi.

    `CommonsKaynak` (SVG) ile aynı yerde kullanılır: `MapBox.commons`.
    Fark, uyarlama imkânının yalnızca kırpma olmasıdır.
    """
    dosya: str                                   # assets/harita/commons/ altındaki ad
    atif: str                                    # ZORUNLU: yazar + lisans + bağlantı
    kirp: tuple = ()                             # (sol, üst, sağ, alt) PİKSEL
    # Kırpılan lejantın yerine Türkçe açıklama: {hex: "açıklama"}.
    lejant_elle: dict = field(default_factory=dict)

    # --- Determinist renk uyarlaması (görüntü modeli DEĞİL) ---
    # `renk_hedef` verilirse, tonu `renk_ton` aralığına düşen pikseller o renge
    # çekilir. PARLAKLIK KORUNUR: arazi gölgesi, kesikli sınır çizgisi ve
    # kaynağın kendi etiketleri olduğu gibi kalır -- bir görüntü modeliyle
    # yapıldığında bunların üçü de sessizce kayboluyordu (ölçüldü: Memlük
    # haritası, 2026 Ağustos).
    #
    # `renk_ton` KAYNAK tonlarının derece aralığıdır; ölçerek bulun, tahmin
    # etmeyin. Memlük haritasında toprak 140-175°, deniz 186°, komşu kara
    # 50-70° -- yani aralığı dar tutmak toprağı denizden ayırıyor.
    renk_hedef: str = ""              # hedef hex (genelde dersin tema rengi)
    renk_ton: tuple = ()              # (en_kucuk_derece, en_buyuk_derece)

    # Haritanın üstüne bindirilen yer imleçleri (bkz. Isaret)
    isaretler: list = field(default_factory=list)


def _gorsel_olcekle(veri: bytes, kaynak: CommonsGorsel) -> tuple[bytes, str, float]:
    """Kırpar, küçültür ve (veri, mime, en/boy oranı) döndürür.

    Pillow yoksa build DURMAZ: dosya olduğu gibi gömülür ve uyarı basılır.
    Çerçeve `object-fit: contain` kullandığı için yanlış orandan gelen tek
    sonuç kenarda boşluk olur; harita EZİLMEZ.
    """
    uzanti = Path(kaynak.dosya).suffix.lower()
    try:
        import io
        from PIL import Image
    except ImportError:
        print("[UYARI] Pillow kurulu değil: raster harita küçültülmeden gömülüyor "
              "(PDF şişebilir). Kurulum: pip install Pillow")
        return veri, MIME.get(uzanti, "image/png"), 0.0

    im = Image.open(io.BytesIO(veri))
    if kaynak.renk_hedef and kaynak.renk_ton:
        im = _tonu_kaydir(im, kaynak)
    if kaynak.kirp:
        if len(kaynak.kirp) != 4:
            raise ValueError(f"CommonsGorsel.kirp (sol, üst, sağ, alt) olmalı; "
                             f"verilen: {kaynak.kirp!r}")
        im = im.crop(tuple(int(v) for v in kaynak.kirp))
    if im.width > EN_FAZLA_PX:
        yeni_yuk = max(1, round(im.height * EN_FAZLA_PX / im.width))
        im = im.resize((EN_FAZLA_PX, yeni_yuk), Image.LANCZOS)

    tampon = io.BytesIO()
    saydam = im.mode in ("RGBA", "LA", "P")
    if saydam:
        im.convert("RGBA").save(tampon, format="PNG", optimize=True)
        mime = "image/png"
    else:
        im.convert("RGB").save(tampon, format="JPEG", quality=JPEG_KALITE, optimize=True)
        mime = "image/jpeg"
    return tampon.getvalue(), mime, im.width / im.height


def _tonu_kaydir(im, kaynak: CommonsGorsel):
    """Tonu `renk_ton` aralığında olan pikselleri `renk_hedef` ailesine çeker.

    PARLAKLIK KORUNUR (yalnızca `TON_PARLAKLIK` ile ölçeklenir): arazi gölgesi,
    kesikli sınır çizgisi ve kaynağın kendi etiketleri olduğu gibi kalır. Bir
    görüntü modeliyle yapılan aynı işte bu üçü de sessizce kaybolmuştu.

    Doygunluğu düşük pikseller (gri/krem komşu kara) hiç dokunulmadan geçer;
    yoksa haritanın yarısı maviye boyanırdı.
    """
    import colorsys
    hedef_h = colorsys.rgb_to_hls(*[int(kaynak.renk_hedef[i:i + 2], 16) / 255
                                    for i in (1, 3, 5)])[0]
    alt, ust = kaynak.renk_ton
    im = im.convert("RGB")
    px = im.load()
    g, y = im.size
    for j in range(y):
        for i in range(g):
            r, gg, b = px[i, j]
            h, l, sat = colorsys.rgb_to_hls(r / 255, gg / 255, b / 255)
            if sat < 0.12 or not (alt <= h * 360 <= ust):
                continue
            nr, ng, nb = colorsys.hls_to_rgb(hedef_h, l * TON_PARLAKLIK,
                                             min(TON_DOYGUNLUK, sat + 0.35))
            px[i, j] = (int(nr * 255), int(ng * 255), int(nb * 255))
    return im


def _isaret_html(isaretler: list) -> str:
    """İmleçleri görüntünün üstüne bindirilecek HTML olarak üretir."""
    parcalar = []
    for m in isaretler:
        if not (0.0 <= m.x <= 1.0 and 0.0 <= m.y <= 1.0):
            raise ValueError(f"Isaret('{m.ad}') koordinatı 0-1 aralığında olmalı "
                             f"(kırpılmış görselin oranı); verilen: {m.x}, {m.y}")
        sinif = "geomap-pin" + (" sol" if m.yan == "sol" else "")
        parcalar.append(f'<span class="{sinif}" style="left:{m.x * 100:.2f}%;'
                        f'top:{m.y * 100:.2f}%">{m.ad}</span>')
    return "".join(parcalar)


def gorsel_hazirla(kaynak: CommonsGorsel) -> tuple[str, str, list]:
    """Raster haritayı sayfaya gömülmeye hazır <img> olarak döndürür.

    Dönen: (html, css_en_boy_orani, lejant_ogeleri)
    """
    yol = COMMONS / kaynak.dosya
    if not yol.exists():
        raise KaynakYok(f"Commons haritası yok: {yol}")
    veri, mime, oran = _gorsel_olcekle(yol.read_bytes(), kaynak)
    b64 = base64.b64encode(veri).decode("ascii")
    html = f'<img alt="" src="data:{mime};base64,{b64}">' + _isaret_html(kaynak.isaretler)
    oran_metni = f"{oran:.4f} / 1" if oran else "4 / 3"
    lejant = [(k.lower(), v) for k, v in kaynak.lejant_elle.items()]
    return html, oran_metni, lejant
