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
HARİTA ARACI — kaynak bulur, indirir, adayları tarar, önizler, imleç denetler
==============================================================================

    python tools/harita.py --veri-indir
    python tools/harita.py --commons "Memlûk Devleti"
    python tools/harita.py --commons "Memlûk Devleti" --sec 1 --ders islam_tarihi_3
    python tools/harita.py --tara islam_tarihi_3 --sinif 2 --donem 2 --sinav final
    python tools/harita.py --onizle islam_tarihi_3 --sinif 2 --donem 2 --sinav final
    python tools/harita.py --sinir-cikar mogol-imparatorlugu-genisleme-1206-1294.svg

--veri-indir  Natural Earth 1:50m katmanlarını (kamu malı / CC0)
              assets/harita/ altına indirir. Bir kez yapılır; dosyalar
              .gitignore'dadır (3 MB, koddan üretilemez ama her an
              yeniden indirilebilir).

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

--tara        Hangi bölümlerin harita adayı olduğunu puanlar. İçerik
              ÜRETMEZ; şehir/komşu listesini ve yaklaşık sınır poligonunu
              kaynağa bakarak siz yazarsınız.

--onizle      Dersin haritalarını tek tek dönemin gorsel_ders_notlari/preview/
              klasörüne yazar; tarayıcıda açıp koordinatları denetlemek için.
              (Derleme gerekmez.)

--sinir-cikar Bir Commons haritasındaki renkli alanı GERÇEK lon/lat poligonuna
              çevirir; sonuç `MapBox.territory` olur ve harita bizim
              motorumuzla çizilir. Kaynak SVG ise önce Chromium'la basılır.
              Çıkan `bindirme.png`ye GÖZLE bakmak zorunludur.

NOT: Harita bir görüntü modeliyle ÜRETİLMEZ ve hazır bir harita görüntüsü
kitaba GÖMÜLMEZ. Tek yol var: sınır kaynaktan çıkarılır, geri kalan her şey
(kıyı, nehir, şehir, etiket) kendi motorumuzla her derlemede yeniden çizilir
(bkz. cekirdek/harita_cizim.py). Ücretsiz, deterministik, etiketler Türkçe
ve baskıda vektör. Atıf yine ZORUNLUDUR: sınır CC BY-SA bir haritadan
türetilmiştir.
Renklendirme için bir görüntü modeli kullanma yolu 2026-08-31'de ÖLÇÜLÜP
terk edildi: hem seedream hem gpt-image-2 kartografın yazılarını bozuyor
(bkz. CLAUDE.md "Neden görüntü modeli yok").
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
from cekirdek import harita_cizim as HC        # noqa: E402
from cekirdek import commons_ara as CA         # noqa: E402
from cekirdek import sinir_cikar as SC         # noqa: E402
import build as B                              # noqa: E402


def komut_veri_indir() -> None:
    HC.VERI.mkdir(parents=True, exist_ok=True)
    for ad, dosya in HC.KATMANLAR.items():
        hedef = HC.VERI / dosya
        if hedef.exists():
            print(f"[harita] {dosya} zaten var ({hedef.stat().st_size // 1024} KB)")
            continue
        url = HC.VERI_KAYNAGI + dosya
        print(f"[harita] indiriliyor: {dosya}")
        with urllib.request.urlopen(url, timeout=180) as r:
            hedef.write_bytes(r.read())
        print(f"[harita]   -> {hedef} ({hedef.stat().st_size // 1024} KB)")
    print("[harita] Natural Earth 1:50m hazır (kamu malı / CC0).")


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
    SC.COMMONS.mkdir(parents=True, exist_ok=True)
    yol, n = CA.indir(a, SC.COMMONS)
    print("")
    print(f"[indirildi] {yol.relative_to(ROOT)}  ({n // 1024} KB)")

    lisans_yol = SC.COMMONS / "LISANS.md"
    kullanan = f"src/{ders}.py" if ders else "(dersi yazınca burayı doldurun)"
    mevcut = lisans_yol.read_text(encoding="utf-8") if lisans_yol.exists() else ""
    lisans_yol.write_text(mevcut + CA.kunye(a, yol.name, kullanan), encoding="utf-8")
    print(f"[künye]     {lisans_yol.relative_to(ROOT)} güncellendi "
          f"(yazar/lisans/bağlantı API'den okundu)")

    print("")
    print("[sonraki adım] Sınırı bu haritadan ÇIKARIN (harita gömülmez, çizilir):")
    print("")
    print(f"  1. Çapa dosyası yazın: {yol.stem}.capa.json")
    print("       {\"kirp\": [sol, ust, sag, alt], \"ton\": [alt_derece, ust_derece],")
    print("        \"capalar\": [{\"ad\": \"Kahire\", \"lon\": 31.235, \"lat\": 30.044,")
    print("                      \"x\": 0.195, \"y\": 0.392}, ...]}")
    print("     x/y = KIRPILMIŞ görselin oranı. En az 6, tercihen 8-12 çapa;")
    print("     haritanın DÖRT BİR YANINA dağıtın (kümelenmiş çapa sistematik")
    print("     kayma verir: ölçüldü, 3 çapayla Mekke %22 kaymıştı).")
    if a.vektor:
        print("     Kaynak VEKTÖR: oranları gözle OKUMAYIN -- dosyanın kendi şehir")
        print("     noktalarının (<use>/<circle> transform matrisi) tam değerlerini")
        print("     viewBox ölçüsüne bölün. Ölçüldü: gözle okuma Moğol haritasında")
        print("     ortalama %2,77 artık verirken dosyadan okuma %0,66'ya indi.")
    print(f"  2. python tools/harita.py --sinir-cikar {yol.name}")
    print("  3. assets/harita/sinir/*.bindirme.png dosyasına GÖZLE bakın.")
    print("  4. Derse yapıştırın:")
    print("")
    print("        .add_map(MapBox(")
    print(f'            region="{madde}",')
    print('            label="Coğrafi konum",')
    print("            bbox=(batı, güney, doğu, kuzey),")
    print(f'            territory=sinir_yukle("{yol.stem}"),')
    print('            cities=[Place("Şehir", lon, lat)],')
    print(f'            source="Sınır: {CA.atif(a)}",')
    print('            caption="...",')
    print('        ), yan=[...], taraf="sag")')


def komut_sinir_cikar(dosya: str, eps: float, en_az: int, tek: bool) -> None:
    """Commons haritasindaki alani gercek koordinata cevirir (bkz. sinir_cikar)."""
    try:
        sonuc = SC.cikar(dosya, en_az_hucre=en_az, eps=eps, tek_parca=tek)
    except (SC.CapaYok, FileNotFoundError) as e:
        raise SystemExit(f"[hata] {e}")

    kal = sonuc["kalibrasyon"]
    tip = {1: "afin", 2: "2. derece polinom", 3: "3. derece polinom"}[kal.derece]
    print(f"[izdüşüm] {tip} · {len(kal.artiklar)} çapa")
    print("")
    print("  ARTIK HATALAR (kırpılmış görselin genişliğine oran):")
    for ad, a in sorted(kal.artiklar, key=lambda t: -t[1]):
        bayrak = "   <-- EŞİĞİ AŞIYOR" if a > SC.ARTIK_ESIGI else ""
        print(f"    {ad:12} %{a * 100:5.2f}{bayrak}")
    print("")
    if kal.en_buyuk_artik > SC.ARTIK_ESIGI:
        print(f"  [UYARI] En büyük artık %{kal.en_buyuk_artik * 100:.2f}, eşik "
              f"%{SC.ARTIK_ESIGI * 100:.1f}. Büyük artık şu ÜÇ şeyden birini söyler:")
        print("          (a) o çapanın x/y oranı yanlış okundu,")
        print("          (b) lon/lat yanlış (aynı adlı başka bir yer olabilir),")
        print("          (c) çapalar bir bölgede kümelenmiş — dört bir yana dağıtın.")
    if kal.derece == 1:
        print("  [UYARI] 6'dan az çapa: yalnızca afin çözüm. Tarihî haritaların çoğu")
        print("          eşuzaklık DEĞİLDİR; afin çözüm çapalardan uzaklaştıkça kayar")
        print("          (ölçüldü: 3 çapayla Mekke 240 px = %22 kaymıştı).")

    print(f"  maske   : {sonuc['maske_ham']} -> {sonuc['maske_temiz']} piksel "
          f"(tarama {sonuc['olcu'][0]}x{sonuc['olcu'][1]}, ton {sonuc['ton']})")
    for i, (px, ham, sade) in enumerate(sonuc["parcalar"], 1):
        print(f"  halka {i} : {px} piksel -> kontur {ham} -> sade {sade} nokta")
    if not sonuc["halkalar"]:
        raise SystemExit("[hata] Hiç halka çıkmadı. `ton` aralığı yanlış olabilir — "
                         "kaynağın toprak rengini ÖLÇÜN, tahmin etmeyin.")

    SC.SINIR.mkdir(parents=True, exist_ok=True)
    ad = pathlib.Path(dosya).stem
    veri = {"kaynak": dosya, "izdusum_derece": kal.derece,
            "en_buyuk_artik": round(kal.en_buyuk_artik, 5),
            "halkalar": [[[round(lo, 3), round(la, 3)] for lo, la in h]
                         for h in sonuc["halkalar"]]}
    hedef = SC.SINIR / f"{ad}.json"
    hedef.write_text(json.dumps(veri, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n[yazıldı] {hedef.relative_to(ROOT)}")

    bindirme = SC.SINIR / f"{ad}.bindirme.png"
    SC.bindirme_yaz(sonuc, bindirme)
    print(f"[bindirme] {bindirme.relative_to(ROOT)}")

    cizim = SC.SINIR / f"{ad}.cizim.svg"
    bbox, n = SC.cizim_onizle(sonuc, cizim)
    if n:
        print(f"[çizim]    {cizim.relative_to(ROOT)}  (tarayıcıda açın)")
        print(f"           çerçeve lon {bbox[0]:.1f}..{bbox[2]:.1f} · "
              f"lat {bbox[1]:.1f}..{bbox[3]:.1f} · {n} nokta")
    else:
        print("[çizim]    atlandı: Natural Earth verisi yok "
              "(python tools/harita.py --veri-indir)")
    print("  [ZORUNLU] Bu görsele GÖZLE bakın: kırmızı çizgi kaynağın renkli alanını")
    print("            izliyor mu? Kaynakta komşu bir devlet AYNI tonda boyanmışsa")
    print("            maske onu da alır ve sonuç sessizce yanlış olur.")

    print("\nDerse yapıştırın (harita artık ÇİZİLİR, raster gömülmez):")
    print(f'        .add_map(MapBox(')
    print(f'            region="...",')
    print(f'            bbox=(batı, güney, doğu, kuzey),')
    print(f'            cities=[Place("...", lon, lat)],')
    print(f'            territory=json.loads((ROOT / "assets/harita/sinir/{ad}.json")')
    print(f'                                 .read_text())["halkalar"],')
    print(f'            source="Sınır: <yazar>, Wikimedia Commons, CC BY-SA — ...",')
    print(f'        ), yan=[...], taraf="sag")')
    print("\nAtıf ZORUNLUDUR: sınır CC BY-SA bir haritadan türetilmiştir,")
    print("  'artık bizim çizimimiz' denemez.")


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
    hedef_kok = B.DONEM.gorsel_ders_notlari / "preview"
    hedef_kok.mkdir(parents=True, exist_ok=True)
    for m in modules:
        pack = B.DONEM.import_ders(m).get_pack()
        sonuc = B.haritalari_coz(pack)
        B.harita_raporu(pack, sonuc)
        for no, mb in _harita_kutulari(pack):
            if not mb.svg:
                continue
            yol = hedef_kok / f"harita-{m}-b{no}.svg"
            yol.write_text(mb.svg, encoding="utf-8")
            print(f"  Bölüm {no}: {yol}  ({len(mb.svg) // 1024} KB)")
            print(f"      çerçeve {mb.bbox} · {len(mb.cities)} şehir · "
                  f"{len(mb.territory) or len(mb.katmanlar)} alan")


def main() -> None:
    ap = argparse.ArgumentParser(prog="tools/harita.py")
    # NOT: konumsal argümanın adı BİLEREK `dersler` -- olcum/dengele/kalibre
    # ile aynı; `--duz` bayrağıyla çakışmaz (bkz. CLAUDE.md "DÜZ KİP").
    ap.add_argument("dersler", nargs="*", help="ders modülleri (çıplak ad)")
    ap.add_argument("--veri-indir", action="store_true",
                    help="Natural Earth 1:50m katmanlarını indir (bir kez)")
    ap.add_argument("--commons", metavar="MADDE",
                    help="bir Vikipedi maddesinin kullandığı haritaları listele")
    ap.add_argument("--sec", type=int, default=0,
                    help="--commons listesinden indirilecek adayın numarası")
    ap.add_argument("--wiki", default="tr", help="hangi Vikipedi (varsayılan tr)")
    ap.add_argument("--ders", default="",
                    help="--sec ile: LISANS.md künyesine yazılacak ders slug'ı")
    ap.add_argument("--tara", action="store_true", help="harita adayı bölümleri puanla")
    ap.add_argument("--onizle", action="store_true", help="haritaları dosyaya yaz")
    ap.add_argument("--sinir-cikar", metavar="DOSYA",
                    help="Commons haritasındaki alanı lon/lat poligonuna çevir")
    ap.add_argument("--eps", type=float, default=1.6,
                    help="--sinir-cikar: sadeleştirme toleransı (tarama pikseli)")
    ap.add_argument("--en-az", type=int, default=60,
                    help="--sinir-cikar: bu kadar pikselden küçük lekeleri at")
    ap.add_argument("--tek-parca", action="store_true",
                    help="--sinir-cikar: yalnız EN BÜYÜK alanı tut (arazi gölgesi "
                         "kaynaklı sahte halkaları eler; tek parçalı devletlerde)")
    ap.add_argument("--hepsi", action="store_true", help="dönemin kitap.py'sindeki tüm dersler")
    donem_mod.add_args(ap)
    a = ap.parse_args()

    if a.veri_indir:
        komut_veri_indir()
        if not (a.tara or a.onizle):
            return

    # --commons DÖNEMDEN BAĞIMSIZDIR: harita ararken ortada henüz bir ders
    # olmayabilir. KRİTİK KURAL 2 (dönem varsayılmaz) ders ÜRETİMİ içindir;
    # bu komut hiçbir döneme dosya yazmaz, yalnızca paylaşılan assets/'a indirir.
    if a.commons:
        komut_commons(a.commons, a.sec, a.ders, a.wiki)
        return

    # --sinir-cikar da dönemden BAĞIMSIZDIR: paylaşılan assets/ üzerinde çalışır.
    if a.sinir_cikar:
        komut_sinir_cikar(a.sinir_cikar, a.eps, a.en_az, a.tek_parca)
        return

    d = donem_mod.resolve(a)
    B.set_donem(d)

    if a.hepsi:
        modules = d.import_ders("kitap").get_book().course_modules
    elif a.dersler:
        modules = a.dersler
    else:
        raise SystemExit("[hata] ders verilmedi (ya da --hepsi / --veri-indir kullanın)")

    if a.tara:
        komut_tara(modules)
    elif a.onizle:
        komut_onizle(modules)
    else:
        raise SystemExit("[hata] --tara ya da --onizle verin")


if __name__ == "__main__":
    main()
