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
HARİTA ARACI — veri indirir, aday bölümleri tarar, haritayı önizler
=====================================================================

    python tools/harita.py --veri-indir
    python tools/harita.py --tara islam_tarihi_3 --sinif 2 --donem 2 --sinav final
    python tools/harita.py --onizle islam_tarihi_3 --sinif 2 --donem 2 --sinav final

--veri-indir  Natural Earth 1:50m katmanlarını (kamu malı / CC0)
              assets/harita/ altına indirir. Bir kez yapılır; dosyalar
              .gitignore'dadır (3 MB, koddan üretilemez ama her an
              yeniden indirilebilir).

--tara        Hangi bölümlerin harita adayı olduğunu puanlar. İçerik
              ÜRETMEZ; şehir/komşu listesini ve yaklaşık sınır poligonunu
              kaynağa bakarak siz yazarsınız.

--onizle      Dersin haritalarını tek tek .svg olarak dönemin
              gorsel_ders_notlari/preview/ klasörüne yazar; tarayıcıda açıp
              koordinatları denetlemek için. (Derleme gerekmez.)

NOT: Harita artık bir görüntü modeliyle ÜRETİLMEZ; her derlemede gerçek
veriden yeniden çizilir (bkz. cekirdek/harita_cizim.py). Bu yüzden burada
"üret" ya da "maliyet" komutu yoktur -- çizim ücretsiz ve deterministiktir.
"""

import argparse
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


def komut_onizle(modules: list[str]) -> None:
    hedef_kok = B.DONEM.gorsel_ders_notlari / "preview"
    hedef_kok.mkdir(parents=True, exist_ok=True)
    for m in modules:
        pack = B.DONEM.import_ders(m).get_pack()
        sonuc = B.haritalari_coz(pack)
        B.harita_raporu(pack, sonuc)
        for ch in pack.chapters:
            for pg in ch.pages:
                for kind, data in pg.items:
                    if kind != "mapsplit":
                        continue
                    mb = data[0]
                    if not mb.svg:
                        continue
                    yol = hedef_kok / f"harita-{m}-b{ch.number}.svg"
                    yol.write_text(mb.svg, encoding="utf-8")
                    print(f"  Bölüm {ch.number}: {yol}  ({len(mb.svg) // 1024} KB)")
                    print(f"      çerçeve {mb.bbox} · {len(mb.cities)} şehir · "
                          f"{len(mb.territory)} yaklaşık alan")


def main() -> None:
    ap = argparse.ArgumentParser(prog="tools/harita.py")
    # NOT: konumsal argümanın adı BİLEREK `dersler` -- olcum/dengele/kalibre
    # ile aynı; `--duz` bayrağıyla çakışmaz (bkz. CLAUDE.md "DÜZ KİP").
    ap.add_argument("dersler", nargs="*", help="ders modülleri (çıplak ad)")
    ap.add_argument("--veri-indir", action="store_true",
                    help="Natural Earth 1:50m katmanlarını indir (bir kez)")
    ap.add_argument("--tara", action="store_true", help="harita adayı bölümleri puanla")
    ap.add_argument("--onizle", action="store_true", help="haritaları .svg olarak yaz")
    ap.add_argument("--hepsi", action="store_true", help="dönemin kitap.py'sindeki tüm dersler")
    donem_mod.add_args(ap)
    a = ap.parse_args()

    if a.veri_indir:
        komut_veri_indir()
        if not (a.tara or a.onizle):
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
