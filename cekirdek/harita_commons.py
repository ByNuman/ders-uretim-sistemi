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

import re
from dataclasses import dataclass, field
from pathlib import Path

from cekirdek.harita_cizim import _hex, _hsl

ROOT = Path(__file__).resolve().parents[1]
COMMONS = ROOT / "assets" / "harita" / "commons"


@dataclass
class CommonsKaynak:
    """Commons'tan alınmış bir haritanın derse uyarlanma tarifi."""
    dosya: str                                   # assets/harita/commons/ altındaki ad
    atif: str                                    # ZORUNLU: yazar + lisans + bağlantı
    metin: dict = field(default_factory=dict)    # {"eski etiket": "yeni etiket"}
    renkler: list = field(default_factory=list)  # koyudan açığa sıralı kaynak hex listesi
    aciklik: tuple = (28.0, 44.0, 60.0, 78.0)    # temadan türetilecek tonların açıklığı
    # TEK TIRNAK ŞART: bu değer style="..." özniteliğinin İÇİNE yazılıyor;
    # çift tırnaklı bir font yığını özniteliği erkenden kapatıp SVG'yi
    # geçersiz XML yapıyor (ölçüldü: Chromium dosyayı hiç açmadı).
    yazitipi: str = "'DejaVu Sans', sans-serif"
    # Etiket rengi değişimi: {eski_hex: yeni_hex}. Renk uyarlaması kontrastı
    # BOZABİLİR -- kaynak haritada sarı etiketler koyu bordo zemine göre
    # seçilmişti; zemini açık maviye çekince okunmaz oldular.
    metin_renk: dict = field(default_factory=dict)
    # Beyaz hale: etiketi hem açık hem koyu zeminde okunur kılar. Tek bir
    # <style> ile bütün metinlere uygulanır; kaynak dosyaya dokunulmaz.
    hale: bool = True

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


class KaynakYok(FileNotFoundError):
    """Commons SVG'si diskte yok."""


def _renk_esle(kaynak_renkler: list, tema_hex: str, aciklik: tuple) -> dict:
    """Kaynaktaki dönem tonlarını dersin tema rengiyle aynı aileden tonlara eşler.

    Sıra ÖNEMLİDİR: `renkler` listesi koyudan açığa yazılır, `aciklik` da
    aynı sırada; böylece haritadaki "en eski çekirdek en koyu" hiyerarşisi
    korunur, yalnızca renk ailesi değişir.
    """
    h, s, _ = _hsl(tema_hex or "#3d5568")
    doygunluk = max(26.0, min(52.0, s))
    return {eski.lower(): _hex(h, doygunluk, aciklik[i] if i < len(aciklik) else 78.0)
            for i, eski in enumerate(kaynak_renkler)}


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


def uyarla(kaynak: CommonsKaynak, tema_hex: str) -> tuple[str, str, list, list]:
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
    if kaynak.renkler:
        svg = _renkleri_degistir(svg, _renk_esle(kaynak.renkler, tema_hex, kaynak.aciklik))
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
    svg, _silinen = _yaziyi_sil(svg, kaynak.sil_desen, kaynak.koru)
    svg = re.sub(r"(font-family\s*:\s*)([^;\"']+)", r"\1" + kaynak.yazitipi, svg)
    svg = re.sub(r'font-family\s*=\s*"[^"]*"', f'font-family="{kaynak.yazitipi}"', svg)
    if kaynak.yazi_araligi:
        if len(kaynak.yazi_araligi) != 2:
            raise ValueError(
                f"CommonsKaynak.yazi_araligi (alt, ust) olmalı; "
                f"verilen: {kaynak.yazi_araligi!r}")
        svg = _yazi_araligina_sikistir(svg, *kaynak.yazi_araligi)
    svg = _yazi_olcekle(svg, kaynak.yazi_olcek)
    if kaynak.hale:
        # paint-order:stroke -> hale metnin ALTINA çizilir, harfleri inceltmez.
        # Tek <style> ile bütün etiketlere uygulanır; kaynak dosyaya dokunulmaz.
        # Hale kalınlığı yazıyla birlikte ölçeklenir, yoksa büyütülmüş etiketin
        # çevresinde saç teli gibi kalır.
        stil = ("<style>text,tspan{paint-order:stroke;stroke:#FFFFFF;"
                "stroke-width:%.2fpx;stroke-linejoin:round;stroke-opacity:.92;}</style>"
                % (2.6 * kaynak.yazi_olcek))
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
