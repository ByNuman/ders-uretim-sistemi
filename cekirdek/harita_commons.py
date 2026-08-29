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
        desen = re.compile(r"(>)(\s*)" + re.escape(eski) + r"(\s*)(</(?:text|tspan)>)")
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
    - id="..." öznitelikleri: bu dosyada hiçbir url(#) referansı yok, ama beş
      harita tek HTML'e gömüldüğü için id çakışması riskini kökten kesiyoruz.
    """
    svg = re.sub(r"<metadata[^>]*>.*?</metadata>", "", svg, flags=re.S)
    svg = re.sub(r"<(?:sodipodi|inkscape):[^>]*?/>", "", svg)
    svg = re.sub(r'\s(?:sodipodi|inkscape):[\w-]+\s*=\s*"[^"]*"', "", svg)
    svg = re.sub(r'\sid\s*=\s*"[^"]*"', "", svg)
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    svg = re.sub(r"\n\s*\n+", "\n", svg)
    return svg


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


def uyarla(kaynak: CommonsKaynak, tema_hex: str) -> tuple[str, str, list]:
    """Commons SVG'sini derse uyarlar.

    Dönen: (svg_metni, css_en_boy_orani, bulunamayan_metin_anahtarlari)
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
    svg = re.sub(r"(font-family\s*:\s*)([^;\"']+)", r"\1" + kaynak.yazitipi, svg)
    svg = re.sub(r'font-family\s*=\s*"[^"]*"', f'font-family="{kaynak.yazitipi}"', svg)
    if kaynak.hale:
        # paint-order:stroke -> hale metnin ALTINA çizilir, harfleri inceltmez.
        # Tek <style> ile bütün etiketlere uygulanır; kaynak dosyaya dokunulmaz.
        stil = ("<style>text,tspan{paint-order:stroke;stroke:#FFFFFF;"
                "stroke-width:2.6px;stroke-linejoin:round;stroke-opacity:.92;}</style>")
        svg = re.sub(r"(<svg\b[^>]*?>)", lambda m: m.group(1) + stil, svg, count=1)

    oran, _vb = _olcu(svg)
    # Kutuya sığsın: sabit width/height yerine %100 (viewBox ölçeği korur).
    svg = re.sub(r'(<svg\b[^>]*?)\swidth\s*=\s*"[^"]*"', r"\1", svg, count=1)
    svg = re.sub(r'(<svg\b[^>]*?)\sheight\s*=\s*"[^"]*"', r"\1", svg, count=1)
    svg = svg.replace("<svg", '<svg width="100%" height="100%"', 1)
    return svg, oran, bulunmayan
