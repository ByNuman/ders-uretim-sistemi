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
COMMONS HARİTA ARAMA — bir Vikipedi maddesinin GERÇEKTEN kullandığı haritalar
==============================================================================

Bir harita eklerken en çok vakit yiyen adım, doğru dosyayı BULMAKTI. İki tuzak
ölçüldü:

* **Commons araması yanlış aracı veriyor.** Sorguyu `filemime:image/svg+xml`
  ile daraltınca yalnızca vektör dosyalar geliyor; oysa Vikipedi maddelerindeki
  tarihî haritaların ÇOĞU PNG/JPG'dir. Memlük maddesi
  `Mamluk Sultanate of Cairo 1317 AD.jpg` kullanıyor ve SVG filtresi bunu hiç
  göremiyordu -- yerine sınır DEĞİL sefer gösteren bir harita seçilmişti.
* **Maddedeki görsellerin çoğu harita değildir.** "Memlûk Devleti" maddesinde
  34 görsel var; 33'ü bayrak, arma, sikke, fotoğraf ve arayüz ikonu.

Bu modül ikisini birden çözer: maddenin görsel listesini alır ve **Commons
kategorilerine** bakarak haritaları ayıklar. Ölçüldü (2026-08-31): haritaların
"Maps of ..." kategorisi var, bayrak/fotoğraf/ikonların yok -- ad kalıbına
(map/karte/harita) bakan bir filtreden çok daha güvenilir.

ATIF BURADAN ÜRETİLİR. `kunye()` yazar/lisans/bağlantı bilgisini Commons'ın
`extmetadata` alanından okur; elle yazılmaz, yani yanlış atıf riski yoktur.
"""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import date

# Wikimedia API'si tarayıcı dışı isteklerde gerçek bir User-Agent ister;
# olmadan 403 döner (ölçüldü). Kimliği açıkça bildirmek Wikimedia'nın
# kullanım koşullarının da gereğidir.
UA = {"User-Agent": "ders-uretim-sistemi/1.0 (egitim amacli; harita kaynagi dogrulama)"}

# Ad kalıbıyla elenenler: kategori denetiminden önce çalışır, yani boşuna
# API isteği yapılmaz. Bunlar hiçbir maddede harita olmaz.
ELE = re.compile(
    r"commons-logo|ooui|oojs|\bicon\b|cc-by|cc[ _]by|wiki(media|pedia)-logo"
    r"|question[ _]book|edit-ltr|ambox|disambig",
    re.I)


class MaddeYok(LookupError):
    """Verilen Vikipedi maddesi bulunamadı."""


@dataclass
class Aday:
    """Maddede geçen, harita olduğu doğrulanmış bir Commons dosyası."""
    baslik: str                 # "File:Mamluk Sultanate of Cairo 1317 AD.jpg"
    url: str                    # upload.wikimedia.org tam yolu
    genislik: int
    yukseklik: int
    mime: str
    yazar: str                  # extmetadata Artist (etiketlerden arındırılmış)
    lisans: str                 # "CC BY-SA 4.0"
    kategoriler: list = field(default_factory=list)

    @property
    def ad(self) -> str:
        return self.baslik.split(":", 1)[1]

    @property
    def vektor(self) -> bool:
        return self.mime == "image/svg+xml"

    @property
    def sayfa_url(self) -> str:
        return "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(
            self.baslik.replace(" ", "_"), safe=":/")

    @property
    def oran(self) -> float:
        return self.genislik / self.yukseklik if self.yukseklik else 0.0


def _api(host: str, **kw) -> dict:
    kw.setdefault("format", "json")
    kw.setdefault("action", "query")
    url = f"https://{host}/w/api.php?" + urllib.parse.urlencode(kw)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return json.load(r)


def _duz(html: str) -> str:
    """extmetadata alanları HTML'dir (yazar adı çoğunlukla bir <a> etiketi)."""
    metin = re.sub(r"<[^>]+>", "", html or "")
    return re.sub(r"\s+", " ", metin).strip()


def madde_gorselleri(madde: str, wiki: str = "tr") -> list[str]:
    """Maddede kullanılan görsel başlıklarını döndürür (elenmişler hariç).

    `prop=images` maddenin GERÇEKTEN gömdüğü dosyaları verir -- Commons'ta
    arama yapmaz. Aradığımız tam olarak budur: "bu maddedeki harita hangisi?"
    """
    # redirects=1 ŞART: "Harezmşahlar" bir yönlendirmedir ve izlenmezse API
    # görselsiz bir yönlendirme sayfası döndürür (ölçüldü: 0 görsel).
    d = _api(f"{wiki}.wikipedia.org", prop="images", titles=madde,
             imlimit="200", redirects="1")
    sayfalar = d.get("query", {}).get("pages", {})
    if not sayfalar or all("missing" in p for p in sayfalar.values()):
        raise MaddeYok(f"{wiki}.wikipedia.org'da '{madde}' maddesi yok")
    adlar = []
    for p in sayfalar.values():
        for im in p.get("images", []):
            t = im["title"]
            # Yerel dildeki "Dosya:" öneki Commons'ta "File:" olmalı.
            t = re.sub(r"^[^:]+:", "File:", t, count=1)
            if not ELE.search(t):
                adlar.append(t)
    return adlar


def haritalari_ayikla(basliklar: list[str], en_az_px: int = 600) -> list[Aday]:
    """Başlık listesinden yalnızca HARİTA olanları döndürür.

    Ölçüt Commons kategorisidir ("Maps of ...", "Historical maps of ...").
    Ad kalıbına bakmak yanıltıcıydı: bir maddede "Map" geçmeyen harita da,
    "Mapa" geçen bir tablo fotoğrafı da olabiliyor.
    """
    adaylar = []
    for i in range(0, len(basliklar), 40):        # API başlık sınırı
        d = _api("commons.wikimedia.org", titles="|".join(basliklar[i:i + 40]),
                 prop="categories|imageinfo", cllimit="500",
                 iiprop="url|size|mime|extmetadata")
        for p in d.get("query", {}).get("pages", {}).values():
            ii = (p.get("imageinfo") or [{}])[0]
            if not ii.get("url"):
                continue
            kats = [c["title"].replace("Category:", "")
                    for c in p.get("categories", [])]
            if not any(re.search(r"\bmaps?\b", k, re.I) for k in kats):
                continue
            if min(ii.get("width", 0), ii.get("height", 0)) < en_az_px:
                continue
            meta = ii.get("extmetadata", {})
            adaylar.append(Aday(
                baslik=p["title"],
                url=ii["url"].split("?")[0],
                genislik=ii["width"], yukseklik=ii["height"], mime=ii["mime"],
                yazar=_duz(meta.get("Artist", {}).get("value", "")) or "(bilinmiyor)",
                lisans=_duz(meta.get("LicenseShortName", {}).get("value", ""))
                       or "(lisans okunamadı)",
                kategoriler=kats))
    # Vektör önce (uyarlanabilir), sonra büyük olan.
    return sorted(adaylar, key=lambda a: (not a.vektor, -a.genislik * a.yukseklik))


TR = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosucgiosu")


def slug(ad: str) -> str:
    """Dosya adını depo kuralına uydurur: küçük harf, tireli, ASCII."""
    govde = ad.rsplit(".", 1)[0].translate(TR).lower()
    govde = re.sub(r"[^a-z0-9]+", "-", govde).strip("-")
    return govde


def indir(aday: Aday, hedef_klasor, yeni_ad: str = "") -> "tuple":
    """Dosyayı assets/harita/commons/ altına indirir. (yol, bayt) döndürür."""
    uzanti = "." + aday.ad.rsplit(".", 1)[-1].lower()
    ad = (yeni_ad or slug(aday.ad)) + uzanti
    yol = hedef_klasor / ad
    with urllib.request.urlopen(
            urllib.request.Request(aday.url, headers=UA), timeout=300) as r:
        veri = r.read()
    yol.write_bytes(veri)
    return yol, len(veri)


def atif(aday: Aday) -> str:
    """CommonsKaynak/CommonsGorsel `atif` alanı -- API'den üretilir, elle yazılmaz."""
    return (f"Harita: {aday.yazar}, Wikimedia Commons, {aday.lisans} — "
            f"{aday.sayfa_url} · uyarlama da aynı lisanstadır.")


def kunye(aday: Aday, dosya_adi: str, kullanan: str, uyarlama: str = "") -> str:
    """assets/harita/commons/LISANS.md'ye eklenecek künye bloğu."""
    bicim = ("Gerçek vektör SVG" if aday.vektor
             else f"Raster {aday.ad.rsplit('.', 1)[-1].upper()}")
    return (
        f"\n### `{dosya_adi}`\n\n"
        f"| | |\n|---|---|\n"
        f"| Özgün ad | {aday.ad} |\n"
        f"| Yazar | {aday.yazar} |\n"
        f"| Lisans | **{aday.lisans}** |\n"
        f"| Kaynak | {aday.sayfa_url} |\n"
        f"| İndirilme | {date.today().isoformat()} |\n"
        f"| Biçim | {bicim}, {aday.genislik} × {aday.yukseklik} |\n"
        f"| Kullanan | `{kullanan}` |\n"
        f"| Uyarlama | {uyarlama or '(henüz yazılmadı — kırpma/lejant kararını buraya yazın)'} |\n")

def en_karsiligi(madde: str, wiki: str = "tr") -> str:
    """Maddenin İngilizce Vikipedi'deki başlığını dil bağlantısından okur.

    Türkçe başlığı olduğu gibi en.wikipedia'ya sormak İŞE YARAMAZ
    ("Harezmşahlar Devleti" orada "Khwarazmian Empire"dır). Dil bağlantısı
    doğru karşılığı verir; yoksa boş döner.
    """
    d = _api(f"{wiki}.wikipedia.org", prop="langlinks", titles=madde,
             lllang="en", redirects="1")
    for p in d.get("query", {}).get("pages", {}).values():
        for ll in p.get("langlinks", []):
            return ll.get("*", "")
    return ""


def oner(madde: str, wiki: str = "tr", kac: int = 5) -> list[str]:
    """Yazılan ada en yakın madde başlıklarını önerir.

    Gerek: "Harezmşahlar" yazınca API onu "Hârezmşâh" adlı GÖRSELSİZ bir
    sayfaya yönlendiriyor (ölçüldü); doğru madde "Harezmşahlar Devleti".
    Kullanıcıyı "harita yok" diyip yalnız bırakmak yerine adayları göster.
    """
    d = _api(f"{wiki}.wikipedia.org", action="query", list="search",
             srsearch=madde, srlimit=str(kac))
    return [s["title"] for s in d.get("query", {}).get("search", [])]
