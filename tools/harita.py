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
HARİTA ARACI — hazır Commons haritası bulur, indirir, adayları tarar, önizler
==============================================================================

    python tools/harita.py --commons "Memlûk Devleti"
    python tools/harita.py --commons "Memlûk Devleti" --sec 1 --ders islam_tarihi_3
    python tools/harita.py --tara   islam_tarihi_3 --sinif 2 --donem 2 --sinav final
    python tools/harita.py --onizle islam_tarihi_3 --sinif 2 --donem 2 --sinav final

--commons     Bir VİKİPEDİ MADDESİNİN gerçekten kullandığı haritaları listeler.
              Commons'ta ARAMA YAPMAZ: maddenin gömdüğü dosyalara bakar, çünkü
              arama (özellikle `filemime:image/svg+xml` ile daraltılmış olanı)
              maddedeki raster haritayı hiç göremiyor -- bir kez bu yüzden
              sınır DEĞİL sefer gösteren yanlış harita seçilmişti.
              Adayları Commons KATEGORİSİNDEN ayıklar; bayrak, arma, sikke,
              fotoğraf ve arayüz ikonu elenir.
              `--sec N` seçileni indirir, LISANS.md künyesini API'den OTOMATİK
              yazar (yazar/lisans/bağlantı elle yazılmaz) ve derse
              yapıştırılacak MapBox parçasını basar.
              Dönem SORULMAZ: bu komut hiçbir döneme dosya yazmaz.

--tara        Hangi bölümlerin harita adayı olduğunu puanlar. İçerik ÜRETMEZ;
              hangi haritanın uyduğuna kaynağa bakarak siz karar verirsiniz.

--onizle      Dersin haritalarını, sayfaya gömüleceği ÖLÇÜDE, dönemin
              gorsel_ders_notlari/preview/ klasörüne JPEG olarak yazar.
              Etiketler bu ölçüde okunuyor mu -- gözle bakmak için.
              (Derleme gerekmez.)

NOT: Harita bir görüntü modeliyle ÜRETİLMEZ, ÇİZİLMEZ ve İÇİNE DOKUNULMAZ.
Tek yol var: Commons'taki hazır harita olduğu gibi gömülür, yalnızca sütun
genişliğine küçültülür (bkz. cekirdek/harita_gomme.py). Etiketler kaynağın
dilinde kalır; Türkçe karşılıkları `MapBox.ad_anahtari` ile kutunun ALTINA
basılır. Atıf ZORUNLUDUR -- artık türetilmiş bir poligon değil, görüntünün
kendisi dağıtılıyor.

Terk edilen iki yol, geri getirmeyin:
  · Görüntü modeliyle çizme/renklendirme (2026-08-31 ölçüldü): kartografın
    yazılarını bozuyor, bir haritada tarihi sessizce değiştirdi.
  · Sınır çıkarıp kendi motorumuzla çizme (2026-09-01 söküldü): sonucu
    güzeldi ama harita başına 6-34 çapa noktasının elle kalibrasyonunu
    gerektiriyordu; asıl maliyet oradaydı.
"""

import argparse
import json
import pathlib
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from cekirdek import donem as donem_mod        # noqa: E402
from cekirdek import harita as H               # noqa: E402
from cekirdek import commons_ara as CA         # noqa: E402
from cekirdek import harita_gomme as HG        # noqa: E402
import build as B                              # noqa: E402


def komut_commons(madde: str, sec: int, ders: str, wiki: str) -> None:
    """Bir Vikipedi maddesinin kullandığı haritaları listeler / indirir."""
    try:
        basliklar = CA.madde_gorselleri(madde, wiki)
    except CA.MaddeYok as e:
        if wiki == "tr":
            print(f"[commons] {e} -- İngilizce Vikipedi deneniyor.")
            wiki = "en"
            basliklar = CA.madde_gorselleri(madde, "en")
        else:
            raise SystemExit(f"[hata] {e}")

    adaylar = CA.haritalari_ayikla(basliklar)
    # Türkçe madde haritayı gömmüyor olabilir: ölçüldü (2026-08-31), "Delhi
    # Sultanlığı" maddesinde Halacî haritası YOK, İngilizcesinde var. Aday
    # çıkmazsa sessizce pes etmek yerine en.wikipedia'ya bakılır.
    if not adaylar and wiki == "tr":
        # Türkçe başlığı olduğu gibi en.wikipedia'ya sormak işe yaramaz
        # ("Harezmşahlar Devleti" orada "Khwarazmian Empire"dır) -- dil
        # bağlantısından gerçek karşılığı al.
        en_ad = CA.en_karsiligi(madde)
        if en_ad:
            print(f'[commons] Türkçe maddede harita yok — İngilizcesi deneniyor: "{en_ad}"')
            try:
                basliklar_en = CA.madde_gorselleri(en_ad, "en")
                adaylar_en = CA.haritalari_ayikla(basliklar_en)
            except CA.MaddeYok:
                adaylar_en = []
            if adaylar_en:
                wiki, madde, basliklar, adaylar = "en", en_ad, basliklar_en, adaylar_en

    print(f'[commons] {wiki}.wikipedia.org · "{madde}" · '
          f"{len(basliklar)} görsel tarandı, {len(adaylar)} harita bulundu")
    print("")
    if not adaylar:
        print("[hata] Bu maddede harita kategorisinde dosya yok.")
        adaylar_madde = [b for b in CA.oner(madde) if b != madde]
        if adaylar_madde:
            print("       Başlık yanlış olabilir — şunları deneyin:")
            for b in adaylar_madde:
                print(f'         python tools/harita.py --commons "{b}"')
        raise SystemExit("       (ya da haritayı elle indirip LISANS.md künyesini yazın)")

    for i, a in enumerate(adaylar, 1):
        tur = ("SVG (vektör — etiketi çevrilebilir)" if a.vektor
               else f"raster {a.mime.split('/')[-1].upper()}")
        print(f"  [{i}] {a.ad}")
        print(f"      {a.genislik} x {a.yukseklik} px · oran {a.oran:.2f} · {tur}")
        print(f"      {a.yazar} · {a.lisans}")
        print(f"      {a.sayfa_url}")
    if not sec:
        print("")
        print("[commons] İndirmek için: --sec <numara> [--ders <ders_slug>]")
        return

    if not 1 <= sec <= len(adaylar):
        raise SystemExit(f"[hata] --sec {sec} yok (1..{len(adaylar)})")
    a = adaylar[sec - 1]
    HG.COMMONS.mkdir(parents=True, exist_ok=True)
    yol, n = CA.indir(a, HG.COMMONS)
    print("")
    print(f"[indirildi] {yol.relative_to(ROOT)}  ({n // 1024} KB)")

    lisans_yol = HG.COMMONS / "LISANS.md"
    kullanan = f"src/{ders}.py" if ders else "(dersi yazınca burayı doldurun)"
    mevcut = lisans_yol.read_text(encoding="utf-8") if lisans_yol.exists() else ""
    # Aynı dosya ikinci kez indirilirse künye TEKRAR EKLENMEZ: build.py künyeyi
    # ilk eşleşmeden okur, ikinci blok sessizce ölü kayıt olurdu.
    if f"### `{yol.name}`" in mevcut:
        print(f"[künye]     {yol.name} zaten kayıtlı, künye tekrar yazılmadı")
    else:
        lisans_yol.write_text(mevcut + CA.kunye(a, yol.name, kullanan), encoding="utf-8")
        print(f"[künye]     {lisans_yol.relative_to(ROOT)} güncellendi "
              f"(yazar/lisans/bağlantı API'den okundu)")

    print("")
    print("[sonraki adım] Haritayı derse yapıştırın -- görüntüye DOKUNULMAZ:")
    print("")
    print("        .add_map(MapBox(")
    print(f'            region="{madde}",')
    print('            label="Coğrafi konum",')
    print(f'            kaynak="{yol.name}",')
    print('            # kirp=(sol, üst, sağ, alt),   # kaynağın ilgisiz kenarlarını atar')
    print('            ad_anahtari=[("Manzikert", "Malazgirt"), ("Baghdad", "Bağdat")],')
    print('            caption="...",')
    print('        ), yan=[...], taraf="sag")')
    print("")
    print("  · `source` YAZMAYIN: build.py künyeyi LISANS.md'den doldurur.")
    print("  · `ad_anahtari`: haritada İngilizce görünen ama Türkçesi FARKLI olan")
    print("    yer adları. Aynı yazılanları (Herat, Merv) yazmayın.")
    print("  · Etiketler yan sütunda küçük kalıyorsa `taraf=\"tam\"` deneyin ya da")
    print("    `kirp` ile ilgisiz kenarları atın; sonra --onizle ile GÖZLE bakın.")


def komut_tara(modules: list[str]) -> None:
    for m in modules:
        pack = B.DONEM.import_ders(m).get_pack()
        print(f"\n=== {B.strip_tags(pack.title)} ({m}) ===")
        for ch in pack.chapters:
            s = H.cografi_sinyal(ch)
            durum = ("HARİTA VAR" if s["harita_var"]
                     else "ADAY  <-- harita eklenebilir" if s["aday"] else "hayır")
            print(f"  Bölüm {ch.number}: puan {s['puan']:>2}  {durum}")
            for g in s["gerekceler"]:
                print(f"      · {g}")


def _harita_kutulari(pack, bolum: int = 0):
    """(bölüm_no, MapBox) çiftlerini sırayla verir."""
    for ch in pack.chapters:
        if bolum and ch.number != bolum:
            continue
        for pg in ch.pages:
            for kind, data in pg.items:
                if kind == "mapsplit":
                    yield ch.number, data[0]


def komut_onizle(modules: list[str]) -> None:
    """Haritaları sayfaya gömülecek ÖLÇÜDE dosyaya yazar.

    Gömme kipinde denetlenecek tek şey okunabilirliktir: kaynak 3800 px
    genişken sayfada 82mm sütuna (972 px) iniyor. Etiketler o ölçüde
    okunuyor mu -- sayısal bir ölçüt bunu söylemez, gözle bakmak gerekir.
    """
    import base64
    hedef_kok = B.DONEM.gorsel_ders_notlari / "preview"
    hedef_kok.mkdir(parents=True, exist_ok=True)
    for m in modules:
        pack = B.DONEM.import_ders(m).get_pack()
        sonuc = B.haritalari_coz(pack)
        B.harita_raporu(pack, sonuc)
        for no, mb in _harita_kutulari(pack):
            if not mb.gorsel_src:
                continue
            yol = hedef_kok / f"harita-{m}-b{no}.jpg"
            yol.write_bytes(base64.b64decode(mb.gorsel_src.split(",", 1)[1]))
            en, boy = mb.gorsel_oran.split(" / ")
            print(f"  Bölüm {no}: {yol}  ({yol.stat().st_size // 1024} KB)")
            print(f"      kaynak {mb.kaynak} · gömülen {en}x{boy} px · "
                  f"{len(mb.ad_anahtari)} ad anahtarı")


def main() -> None:
    ap = argparse.ArgumentParser(prog="tools/harita.py")
    # NOT: konumsal argümanın adı BİLEREK `dersler` -- olcum/dengele/kalibre
    # ile aynı; `--duz` bayrağıyla çakışmaz (bkz. CLAUDE.md "DÜZ KİP").
    ap.add_argument("dersler", nargs="*", help="ders modülleri (çıplak ad)")
    ap.add_argument("--commons", metavar="MADDE",
                    help="bir Vikipedi maddesinin kullandığı haritaları listele")
    ap.add_argument("--sec", type=int, default=0,
                    help="--commons listesinden indirilecek adayın numarası")
    ap.add_argument("--wiki", default="tr", help="hangi Vikipedi (varsayılan tr)")
    ap.add_argument("--ders", default="",
                    help="--sec ile: LISANS.md künyesine yazılacak ders slug'ı")
    ap.add_argument("--tara", action="store_true", help="harita adayı bölümleri puanla")
    ap.add_argument("--onizle", action="store_true",
                    help="haritaları gömülecek ölçüde dosyaya yaz (okunabilirlik denetimi)")
    ap.add_argument("--hepsi", action="store_true", help="dönemin kitap.py'sindeki tüm dersler")
    donem_mod.add_args(ap)
    a = ap.parse_args()

    # --commons DÖNEMDEN BAĞIMSIZDIR: harita ararken ortada henüz bir ders
    # olmayabilir. KRİTİK KURAL 2 (dönem varsayılmaz) ders ÜRETİMİ içindir;
    # bu komut hiçbir döneme dosya yazmaz, yalnızca paylaşılan assets/'a indirir.
    if a.commons:
        komut_commons(a.commons, a.sec, a.ders, a.wiki)
        return

    d = donem_mod.resolve(a)
    B.set_donem(d)

    if a.hepsi:
        modules = d.import_ders("kitap").get_book().course_modules
    elif a.dersler:
        modules = a.dersler
    else:
        raise SystemExit("[hata] ders verilmedi (ya da --hepsi kullanın)")

    if a.tara:
        komut_tara(modules)
    elif a.onizle:
        komut_onizle(modules)
    else:
        raise SystemExit("[hata] --tara ya da --onizle verin")


if __name__ == "__main__":
    main()
