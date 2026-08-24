# -*- coding: utf-8 -*-
"""
DERS ÜRETİM SİSTEMİ — donem.py  (SINIF / DÖNEM / SINAV ÇÖZÜMLEYİCİ)
====================================================================
Proje artık dosyaları sınav dönemine göre ayrı ağaçlarda tutar:

    <sinif>-sinif/<donem>-donem/<sinav>/
        kaynaklar/ders_kaynaklari/   # ham ders metinleri / özet PDF'leri (GİRDİ)
        kaynaklar/ogretmen_notlari/  # ham dikte notları (GİRDİ)
        src/                         # <ders_slug>.py içerik modülleri + kitap.py
        ders_ozetleri/               # build.py / build_kitap.py ÇIKTISI (.pdf + .html)
        calisma_rehberleri/          # ders-anlatim skill'i Mod 2 çıktısı
        ders_anlatimlari/            # ders-anlatim skill'i Mod 1 çıktısı

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

ROOT = Path(__file__).resolve().parent

SINIFLAR = ("2", "3")
DONEMLER = ("1", "2")
SINAVLAR = ("vize", "final")

# Bir dönem klasörünün alt yapısı — iskeleti kurarken de bu liste kullanılır.
ALT_KLASORLER = (
    "kaynaklar/ders_kaynaklari",
    "kaynaklar/ogretmen_notlari",
    "src",
    "ders_ozetleri",
    "calisma_rehberleri",
    "ders_anlatimlari",
)


@dataclass(frozen=True)
class Donem:
    """Tek bir sınav döneminin (sınıf + dönem + sınav) klasör kökü."""

    sinif: str
    donem: str
    sinav: str

    # --- yollar -------------------------------------------------------------
    @property
    def root(self) -> Path:
        return ROOT / f"{self.sinif}-sinif" / f"{self.donem}-donem" / self.sinav

    @property
    def src(self) -> Path:
        return self.root / "src"

    @property
    def ders_ozetleri(self) -> Path:
        """build.py / build_kitap.py ÇIKTI klasörü (.pdf + .html)."""
        return self.root / "ders_ozetleri"

    @property
    def ders_kaynaklari(self) -> Path:
        return self.root / "kaynaklar" / "ders_kaynaklari"

    @property
    def ogretmen_notlari(self) -> Path:
        return self.root / "kaynaklar" / "ogretmen_notlari"

    @property
    def calisma_rehberleri(self) -> Path:
        return self.root / "calisma_rehberleri"

    @property
    def ders_anlatimlari(self) -> Path:
        return self.root / "ders_anlatimlari"

    def __str__(self) -> str:
        return f"{self.sinif}. sınıf / {self.donem}. dönem / {self.sinav}"

    @property
    def etiket(self) -> str:
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

    d = Donem(al("sinif", SINIFLAR), al("donem", DONEMLER), al("sinav", SINAVLAR))
    if ensure:
        d.ensure()
    d.activate()
    return d
