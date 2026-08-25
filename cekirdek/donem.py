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
DERS ÜRETİM SİSTEMİ — donem.py  (SINIF / DÖNEM / SINAV ÇÖZÜMLEYİCİ)
====================================================================
Proje artık dosyaları sınav dönemine göre ayrı ağaçlarda tutar:

    <sinif>-sinif/<donem>-donem/<sinav>/
        kaynaklar/
            ders_kaynaklari/<DERS ADI>/     # GİRDİ: ham ders metni
            ogretmen_notlari/<DERS ADI>/    # GİRDİ: ham dikte notu
            özetlenmiş_dersler/<DERS ADI>/  # ARA:   bunlardan çıkarılan YAZILI özet
        gorsel_ders_notlari/                # ÇIKTI: build.py'nin kitap formatındaki PDF'i
            <DERS ADI>/                     #        tekil ders (.pdf + .html)
            <kitap>.pdf                     #        birleşik kitap (dersi olmadığı için kökte)
        src/                                # <ders_slug>.py içerik modülleri + kitap.py
        calisma_rehberleri/                 # ders-anlatim skill'i Mod 2 çıktısı
        ders_anlatimlari/                   # ders-anlatim skill'i Mod 1 çıktısı

Üretim zinciri:
    ders_kaynaklari/ + ogretmen_notlari/  ->  özetlenmiş_dersler/  ->  gorsel_ders_notlari/
          (ham girdi)                          (yazılı özet)            (kitap formatı)

Bu modül, bütün build/ölçüm scriptlerinin AYNI şekilde dönem seçmesini sağlar.
VARSAYILAN DÖNEM YOKTUR: parametre verilmezse kullanıcıya sorulur, sorulamıyorsa
(TTY yoksa) build hata ile durur — sessizce yanlış döneme yazmak yasaktır.

Kullanım (script içinde):

    import donem
    p = argparse.ArgumentParser()
    donem.add_args(p)
    args = p.parse_args()
    d = donem.resolve(args)          # -> Donem
    mod = d.import_ders("kelam_tarihi")

Ortam değişkenleriyle de verilebilir: DERS_SINIF, DERS_DONEM, DERS_SINAV.
"""

import os
import sys
import importlib
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]   # cekirdek/ -> proje kökü

SINIFLAR = ("2", "3")
DONEMLER = ("1", "2")
SINAVLAR = ("vize", "final")

# DÜZ ("dersler/") KİPİ — sınıf/dönem/sınav ağacı OLMAYAN kurulumlar için.
# Bu depo GitHub'da yalnızca boş bir `dersler/` iskeletiyle yayımlanır; sınıf
# ağaçları (`2-sinif/`, `3-sinif/`) .gitignore'dadır ve klonlayan kişide hiç
# bulunmaz. O kişi tek bir çalışma klasörü kullanır: `dersler/`.
DUZ_KLASOR = "dersler"

# Bir dönem klasörünün alt yapısı — iskeleti kurarken de bu liste kullanılır.
ALT_KLASORLER = (
    "kaynaklar/ders_kaynaklari",      # GİRDİ  — ham ders metni      (ders adı alt klasörü)
    "kaynaklar/ogretmen_notlari",     # GİRDİ  — ham dikte notu      (ders adı alt klasörü)
    "kaynaklar/özetlenmiş_dersler",   # ARA    — yazılı özet         (ders adı alt klasörü)
    "gorsel_ders_notlari",            # ÇIKTI  — build.py kitap PDF  (ders adı alt klasörü)
    "src",
    "calisma_rehberleri",
    "ders_anlatimlari",
)


@dataclass(frozen=True)
class Donem:
    """Tek bir sınav döneminin (sınıf + dönem + sınav) klasör kökü."""

    sinif: str
    donem: str
    sinav: str
    duz: bool = False          # True ise sınıf/dönem/sınav yok, kök `dersler/`

    # --- yollar -------------------------------------------------------------
    @property
    def root(self) -> Path:
        if self.duz:
            return ROOT / DUZ_KLASOR
        return ROOT / f"{self.sinif}-sinif" / f"{self.donem}-donem" / self.sinav

    @property
    def src(self) -> Path:
        return self.root / "src"

    @property
    def gorsel_ders_notlari(self) -> Path:
        """build.py / build_kitap.py ÇIKTI kökü.

        Tekil ders PDF'leri buranın <DERS ADI>/ alt klasörüne yazılır
        (bkz. ders_cikti_dizini); birleşik kitap tek bir derse ait olmadığı
        için doğrudan bu klasörün köküne yazılır.
        """
        return self.root / "gorsel_ders_notlari"

    @property
    def ders_kaynaklari(self) -> Path:
        return self.root / "kaynaklar" / "ders_kaynaklari"

    @property
    def ogretmen_notlari(self) -> Path:
        return self.root / "kaynaklar" / "ogretmen_notlari"

    @property
    def ozetlenmis_dersler(self) -> Path:
        """ders_kaynaklari/ + ogretmen_notlari/ içeriğinden çıkarılan YAZILI
        özetler. Görsel ders notu ÜRETİLMEZ burada — bu klasör build.py'nin
        girdisidir, çıktısı değil."""
        return self.root / "kaynaklar" / "özetlenmiş_dersler"

    def ders_cikti_dizini(self, ders_klasoru: str) -> Path:
        """Bir dersin görsel ders notu çıktı klasörü; yoksa oluşturulur.

        `ders_klasoru`, CoursePack.ders_klasoru alanından gelir (ders
        programındaki BÜYÜK HARFLİ tam ad, ör. "KELÂM TARİHİ"). Bu kural TÜM
        sınıf/dönem/sınav kombinasyonlarında geçerlidir.
        """
        p = self.gorsel_ders_notlari / ders_klasoru
        p.mkdir(parents=True, exist_ok=True)
        return p

    def ders_kaynak_dizini(self, ders_klasoru: str) -> Path:
        """Bir dersin ham kaynak klasörü (girdi)."""
        return self.ders_kaynaklari / ders_klasoru

    def ders_ozet_dizini(self, ders_klasoru: str) -> Path:
        """Bir dersin yazılı özet klasörü (build.py'nin girdisi)."""
        return self.ozetlenmis_dersler / ders_klasoru

    @property
    def calisma_rehberleri(self) -> Path:
        return self.root / "calisma_rehberleri"

    @property
    def ders_anlatimlari(self) -> Path:
        return self.root / "ders_anlatimlari"

    def __str__(self) -> str:
        if self.duz:
            return "dersler (düz kip — sınıf/dönem ayrımı yok)"
        return f"{self.sinif}. sınıf / {self.donem}. dönem / {self.sinav}"

    @property
    def etiket(self) -> str:
        if self.duz:
            return DUZ_KLASOR
        return f"{self.sinif}-sinif/{self.donem}-donem/{self.sinav}"

    # --- kurulum / import ---------------------------------------------------
    def ensure(self) -> "Donem":
        """Dönemin alt klasörlerini (yoksa) oluşturur."""
        for alt in ALT_KLASORLER:
            (self.root / alt).mkdir(parents=True, exist_ok=True)
        return self

    def activate(self) -> "Donem":
        """Dönemin src/ klasörünü sys.path'in BAŞINA koyar.

        '2-sinif' geçerli bir Python paket adı olmadığı için ders modülleri
        noktalı yolla (content.kelam_tarihi) import EDİLEMEZ; bunun yerine
        src/ doğrudan path'e eklenip modül çıplak adıyla import edilir.
        Aynı anda iki dönem aktif olmasın diye önce eski src/ girdileri
        temizlenir.
        """
        src = str(self.src)
        for p in [p for p in sys.path if p.endswith(f"{os.sep}src")]:
            sys.path.remove(p)
        sys.path.insert(0, src)
        if str(ROOT) not in sys.path:
            sys.path.insert(1, str(ROOT))
        return self

    def import_ders(self, module_name: str):
        """Ders modülünü bu dönemin src/ klasöründen import eder.

        Eski 'content.kelam_tarihi' yazımı da kabul edilir (geriye dönük
        uyumluluk): noktalı önek atılıp çıplak ad kullanılır.
        """
        name = module_name.split(".")[-1]
        self.activate()
        path = self.src / f"{name}.py"
        if not path.exists():
            mevcut = sorted(
                f.stem for f in self.src.glob("*.py")
                if f.stem not in ("__init__", "kitap")
            )
            raise SystemExit(
                f"[hata] '{name}' dersi {self.etiket} döneminde yok:\n"
                f"        aranan dosya: {path}\n"
                f"        bu dönemdeki dersler: {', '.join(mevcut) or '(hiç yok)'}"
            )
        return importlib.import_module(name)


def add_args(parser) -> None:
    """--sinif / --donem / --sinav argümanlarını bir ArgumentParser'a ekler."""
    parser.add_argument("--sinif", choices=SINIFLAR,
                        help="Sınıf (2 veya 3). Verilmezse sorulur.")
    parser.add_argument("--donem", choices=DONEMLER,
                        help="Dönem (1 veya 2). Verilmezse sorulur.")
    parser.add_argument("--sinav", choices=SINAVLAR,
                        help="Sınav dönemi (vize veya final). Verilmezse sorulur.")
    # DİKKAT: bayrağın adı --duz'dur, --dersler DEĞİL. tools/olcum.py,
    # tools/dengele.py ve tools/kalibre.py'de `dersler` adında KONUMSAL bir
    # argüman (ölçülecek ders listesi) zaten var; aynı adı kullanmak argparse
    # dest'ini ezip o araçları bozuyordu.
    parser.add_argument("--duz", action="store_true",
                        help=f"Düz kip: sınıf/dönem/sınav ağacı yerine tek bir "
                             f"{DUZ_KLASOR}/ klasörü kullanılır. Sınıf ağacı hiç "
                             f"yoksa (temiz klon) zaten kendiliğinden bu kipe geçilir.")


def _sinif_agaci_var() -> bool:
    """Diskte en az bir `<n>-sinif/` klasörü var mı? Yoksa düz kipe geçilir."""
    return any((ROOT / f"{s}-sinif").is_dir() for s in SINIFLAR)


def _sorulamadi(alan: str) -> SystemExit:
    return SystemExit(
        f"[hata] --{alan} verilmedi ve interaktif olarak sorulamıyor.\n"
        f"        Varsayılan bir dönem YOKTUR; açıkça belirtin:\n"
        f"        --sinif 2 --donem 2 --sinav final\n"
        f"        (ya da DERS_{alan.upper()} ortam değişkenini ayarlayın)"
    )


def _sor(alan: str, secenekler: tuple) -> str:
    """Eksik bir alanı interaktif olarak sorar.

    Soramıyorsak (TTY yok, stdin kapalı/EOF, kullanıcı Ctrl-C) VARSAYIM
    YAPMADAN dururuz: yanlış döneme sessizce yazmaktansa durmak doğrudur.
    """
    if not sys.stdin.isatty():
        raise _sorulamadi(alan)
    liste = " / ".join(secenekler)
    while True:
        try:
            cevap = input(f"[soru] {alan} ({liste}): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            raise _sorulamadi(alan) from None
        if cevap in secenekler:
            return cevap
        print(f"       Geçersiz. Seçenekler: {liste}")


def resolve(args=None, *, ensure: bool = True) -> Donem:
    """Sınıf/dönem/sınav değerlerini çözer ve Donem döndürür.

    Öncelik sırası: komut satırı argümanı -> ortam değişkeni -> interaktif soru.
    Hiçbir aşamada varsayılan bir değer VARSAYILMAZ.
    """
    def al(alan, secenekler):
        deger = getattr(args, alan, None) if args is not None else None
        if not deger:
            deger = os.environ.get(f"DERS_{alan.upper()}")
        if deger:
            deger = str(deger).strip().lower()
            if deger not in secenekler:
                raise SystemExit(
                    f"[hata] geçersiz {alan}: {deger!r} "
                    f"(seçenekler: {', '.join(secenekler)})"
                )
            return deger
        return _sor(alan, secenekler)

    # --- DÜZ KİP -----------------------------------------------------------
    # İki yoldan girilir:
    #   1) --dersler açıkça verilmişse,
    #   2) sınıf ağacı DİSKTE HİÇ YOKSA (temiz klon) ve kullanıcı da sınıf/
    #      dönem/sınav vermemişse.
    # (2) KRİTİK KURAL 2'yi ("varsayım yapma") çiğnemez: ortada seçilebilecek
    # bir dönem yoktur, dolayısıyla yanlış döneme yazma riski de yoktur.
    # Sınıf ağacı varsa bu kip KENDİLİĞİNDEN devreye girmez; dönem yine sorulur.
    if getattr(args, "duz", False):
        d = Donem("", "", "", duz=True)
        if ensure:
            d.ensure()
        return d

    verilen = [getattr(args, a, None) if args is not None else None
               for a in ("sinif", "donem", "sinav")]
    if not any(verilen) and not _sinif_agaci_var():
        print(f"[donem] Sınıf/dönem ağacı bulunamadı; düz kipe geçildi "
              f"-> {DUZ_KLASOR}/  (açıkça seçmek için: --duz)")
        d = Donem("", "", "", duz=True)
        if ensure:
            d.ensure()
        return d

    d = Donem(al("sinif", SINIFLAR), al("donem", DONEMLER), al("sinav", SINAVLAR))
    if ensure:
        d.ensure()
    d.activate()
    return d
