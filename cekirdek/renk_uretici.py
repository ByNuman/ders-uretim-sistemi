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
DERS ÜRETİM SİSTEMİ — renk_uretici.py  (DERSE ÖZEL VURGU RENGİ — TEK KAYNAK)
===========================================================================
Bir dersin rengi, hangi sistemle üretilirse üretilsin AYNI olmalıdır:

    build.py / build_kitap.py   ->  görsel ders notu kitabı (kapak, banner, tablo)
    .claude/skills/ders-anlatim ->  anlatım / çalışma rehberi PDF'i (python-docx)

Bu modül o rengin TEK kaynağıdır. İki sistem de buradan okur; renk üretme
mantığı hiçbir yerde kopyalanmaz (kopyalanırsa biri güncellenir, diğeri
güncellenmez ve renkler birbirinden sapar).

Renk nereden gelir? (öncelik sırası)
------------------------------------
1. **Kayıtlı ders modülü** — o dönemin `src/<ders>.py` dosyasında
   `ders_klasoru=` alanı bu derse eşitse, dersin rengi orada elle seçilmiş
   `theme_color=` hex'idir. (LEGACY ders, yani `theme_color` vermeyip sadece
   `theme="slate"` gibi sabit tema kullanan ders ise, o sabit temanın
   `templates/style.css`'teki `--accent` değeri kullanılır.)
   Yani görsel kitap sistemi HER ZAMAN otoritedir: bir dersin görsel kitapta
   hangi rengi varsa, anlatım PDF'i de o rengi alır.
2. **Önceden belirlenmiş ders rengi** — `DERS_RENKLERI` tablosu. Henüz
   `src/<ders>.py` yazılmamış dersler için renk baştan sabitlenmiştir; ilke
   "RENK = DERS AİLESİ"dir (Tefsir hep yeşil, Hadis hep kiremit...). Yeni bir
   ders modülü yazarken `theme_color=` alanına buradaki hex'i kopyalayın.
3. **Deterministik türetme** — ders ne kayıtlı ne de tabloda ise,
   renk ders adının karakterlerinden sabit bir hash ile türetilir (aynı ders
   adı her zaman aynı rengi verir; rastgelelik yok). Türetme, görsel kitabın
   dinamik tema motorunun (`theme_engine.generate_theme_vars`) ta kendisiyle
   yapılır — yani üretilen ton, elle seçilmiş temalarla aynı okunabilirlik/
   baskı aralığındadır (ne beyaza ne siyaha yakın, orta doygunlukta).

Kullanım
--------
    from renk_uretici import ders_rengi, ders_rengi_rgb, pack_rengi

    ders_rengi("HADİS", "2", "2", "final")        # -> "#8E3B1F"
    ders_rengi_rgb("HADİS", "2", "2", "final")    # -> (142, 59, 31)  (RGBColor için)
    pack_rengi(pack)                              # -> bir CoursePack'in efektif rengi

Komut satırı:
    python renk_uretici.py "HADİS" --sinif 2 --donem 2 --sinav final
    python renk_uretici.py --liste --sinif 2 --donem 2 --sinav final
"""

# --- doğrudan çalıştırma desteği ------------------------------------------
# Bu modül hem paket olarak (`from cekirdek.X import ...`) hem de doğrudan
# (`python cekirdek/X.py`) çalıştırılabilir. Doğrudan çalıştırıldığında
# sys.path[0] `cekirdek/` olur ve kardeş modüller `cekirdek.` önekiyle
# bulunamaz; bu blok proje kökünü path'e ekleyerek ikisini de çalıştırır.
import sys as _sys
from pathlib import Path as _Path
if __package__ in (None, ""):
    _sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
# ---------------------------------------------------------------------------

import hashlib
import re
from pathlib import Path

from cekirdek.theme_engine import (generate_theme_vars,
                                   generate_theme_vars_from_hex)

ROOT = Path(__file__).resolve().parents[1]   # cekirdek/ -> proje kökü
STYLE_CSS = ROOT / "templates" / "style.css"

# theme_color vermeyen LEGACY dersler için son çare (style.css okunamazsa)
_VARSAYILAN_SABIT_ACCENT = "#3D5568"   # .theme-slate


# ---------------------------------------------------------------------------
# Ders adı normalizasyonu — "TEFSİR II", "Tefsir II", "tefsir-ii" aynı derstir
# ---------------------------------------------------------------------------
_TR_FOLD = str.maketrans({
    "İ": "I", "ı": "i", "Ş": "S", "ş": "s", "Ğ": "G", "ğ": "g",
    "Ü": "U", "ü": "u", "Ö": "O", "ö": "o", "Ç": "C", "ç": "c",
    "Â": "A", "â": "a", "Î": "I", "î": "i", "Û": "U", "û": "u",
})


def normalize_ders_adi(ad: str) -> str:
    """Karşılaştırma için ders adını sadeleştirir (büyük/küçük harf, Türkçe
    karakter, boşluk/noktalama farkını yok sayar)."""
    ad = (ad or "").translate(_TR_FOLD).upper()
    return re.sub(r"[^A-Z0-9]+", "", ad)


# ---------------------------------------------------------------------------
# 1.5. yol: ÖNCEDEN BELİRLENMİŞ DERS RENKLERİ  (ilke: RENK = DERS AİLESİ)
# ---------------------------------------------------------------------------
# Her rengin gerekçesi DERSİN KENDİ RUHUDUR, bir üst sınıftan miras DEĞİL:
# Tefsir mushaf yeşili (vahyin metni), Tecvid turkuaz (tilavetin akışı), Hadis
# koyu deri cilt kahvesi (rivayet, isnad, el yazması), Kelam mor (soyut akıl),
# İslam Felsefesi gece mavisi (serin akıl, hikmet), İslam Hukuku vişne (mühür,
# hüküm), Tasavvuf gül (aşk, sema), Tarih bronz (altın çağ), Arap Dili
# terracotta (çöl toprağı, hat), Sınıf Yönetimi/Ölçme çini laciverti (düzen,
# güven), Din Eğitimi/Rehberlik zeytin (fide, yetiştirme).
#
# Aynı ders ailesi farklı dönemlerde tekrar ettiğinde renk de tekrar eder
# (Tefsir III = Tefsir IV), çünkü ruh aynıdır. Hue dağılımı:
# 8/28/48/82/150/180/212/242/274/322/350 derece — aralar en az 20°, yani bir
# dönem kitabındaki 11 ders birbirinden ayrışır.
#
# Anahtarlar ders adının NORMALİZE edilmiş hâlidir; sondaki Roma rakamı
# ("TEFSİR III" -> "TEFSIR") atılır, yani bir aile için TEK satır yeter.
#
# ÖNCELİK: bir dersin `src/<ders>.py` dosyası varsa oradaki `theme_color` her
# zaman kazanır (bkz. kayitli_ders_rengi). Bu tablo, HENÜZ YAZILMAMIŞ dersler
# için rengi baştan sabitler — yeni bir `src/<ders>.py` yazarken `theme_color=`
# alanına buradaki hex'i kopyalayın ki iki sistem sapmasın.
DERS_RENKLERI = {
    # --- Vahiy metni ------------------------------------------------------
    "TEFSIR":                   "#206040",  # mushaf yesili        H150
    "KURANOKUMAVETECVID":       "#1D6363",  # turkuaz / tilavet    H180
    # --- Rivayet ----------------------------------------------------------
    "HADIS":                    "#664324",  # koyu deri cilt       H28
    # --- Akil / itikad ----------------------------------------------------
    "SISTEMATIKKELAM":          "#592F79",  # mor / soyut akil     H274
    "ISLAMFELSEFESITARIHI":     "#2F2D76",  # gece mavisi          H242
    # --- Hukum ------------------------------------------------------------
    "ISLAMHUKUKU":              "#7A2433",  # visne / muhur        H350
    "ISLAMHUKUKUSULU":          "#7A2433",  # (ayni aile: fikih usulu)
    # --- Kalp -------------------------------------------------------------
    "TASAVVUF":                 "#7B3260",  # gul / erik           H322
    # --- Tarih ------------------------------------------------------------
    "ISLAMMEDENIYETITARIHI":    "#776931",  # bronz / altin cag    H48
    "ISLAMMEZHEPLERITARIHI":    "#776931",  # (ayni ruh, farkli donem)
    # Siyasi tarih ayri bir ailedir: medeniyet/mezhep tarihi kulturel bir
    # birikimi (bronz), siyasi tarih ise devlet-ordu-sinir eksenini anlatir.
    # Cini laciverti bu eksenin rengidir; 2-sinif/2-donem/final'deki
    # islam_tarihi_3.py bu tonla basildi, vize kitabi da ayni tonu surdurur.
    "ISLAMTARIHI":              "#1D4E79",  # cini laciverti       H212
    "ISLAMTARIHI3":             "#1D4E79",  # (Arap rakamli yazim: "ISLAM TARIHI 3")
    # --- Akil aleti -------------------------------------------------------
    # Mantik "alet ilmi"dir; klasik amblemi Porphyrios agacidir (cins-tur
    # dallanmasi). Defne/yaprak yesili bu agacin rengidir. H112 -- mushaf
    # yesilinden (Tefsir, H150) ve zeytinden (Din Egitimi, H82) 30 dereceden
    # fazla uzaktir, ayni kitapta yan yana gelince ayrisir.
    "MANTIK":                   "#2E5E26",  # Porphyrios agaci yesili  H112
    # --- Dil / edebiyat ---------------------------------------------------
    "ARAPDILIVEEDEBIYATI":      "#8C2F21",  # terracotta / col     H8
    # --- Egitim / din hizmetleri -----------------------------------------
    "SINIFYONETIMI":                       "#1F4775",  # cini laciverti  H212
    "EGITIMDEOLCMEVEDEGERLENDIRME":        "#1F4775",  # (ayni ruh, farkli donem)
    "DINEGITIMI":                          "#51662E",  # zeytin / fide   H82
    "DINHIZMETLERINDEREHBERLIKVEILETISIM": "#51662E",  # (ayni ruh, farkli donem)
}

_ROMEN = {"I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"}


def _aile_anahtari(ders_adi: str) -> str:
    """Ders adını aile anahtarına çevirir: sondaki Roma rakamı AYRI BİR KELİME
    ise atılır, kalan kısım normalize edilir.

    Roma rakamı ayıklaması kelime bazında yapılır; normalize edilmiş metnin
    sonundan harf kırpmak "DİN EĞİTİMİ" -> "DINEGITIM" gibi yanlış anahtar
    üretirdi (sondaki 'I' rakam değil, kelimenin parçası)."""
    kelimeler = (ders_adi or "").split()
    while kelimeler and kelimeler[-1].translate(_TR_FOLD).upper() in _ROMEN:
        kelimeler.pop()
    return normalize_ders_adi(" ".join(kelimeler))


def belirlenmis_renk(ders_adi: str):
    """Tabloda önceden belirlenmiş renk (hex) ya da None."""
    return DERS_RENKLERI.get(_aile_anahtari(ders_adi))


# ---------------------------------------------------------------------------
# 2. yol: ders adından deterministik renk
# ---------------------------------------------------------------------------
def _hsl_from_ad(ders_adi: str):
    """Ders adından sabit (h, s, l) üretir. hashlib kullanılır: Python'ın
    yerleşik hash()'i her süreçte farklı tohumla çalışır, deterministik
    DEĞİLDİR — burada kullanılamaz."""
    key = normalize_ders_adi(ders_adi).encode("utf-8")
    dg = hashlib.sha256(key).digest()
    hue = ((dg[0] << 8) | dg[1]) % 360          # 0-359
    sat = 38 + (dg[2] % 26)                     # 38-63  (canlı ama "neon" değil)
    light = 26 + (dg[3] % 14)                   # 26-39  (kağıtta net, siyaha yakın değil)
    return hue, sat, light


def deterministik_renk(ders_adi: str) -> str:
    """Ders adından türetilen vurgu rengi (hex). Görsel kitabın tema motoruyla
    AYNI fonksiyondan (`generate_theme_vars`) geçer; o motor sarı/sarı-yeşil
    bandında doygunluğu kısar ve parlaklığı okunur aralığa kelepçeler, yani
    çıkan ton her zaman baskıya uygundur."""
    hue, sat, light = _hsl_from_ad(ders_adi)
    return generate_theme_vars(hue, sat, light)["--accent"]


# ---------------------------------------------------------------------------
# 1. yol: görsel kitap sisteminde kayıtlı ders rengi
# ---------------------------------------------------------------------------
def sabit_tema_rengi(theme_adi: str) -> str:
    """style.css'teki sabit `.theme-XXXX` bloğunun --accent değeri.
    (theme_color vermeyen LEGACY dersler bu rengi kullanır.)"""
    try:
        css = STYLE_CSS.read_text(encoding="utf-8")
    except OSError:
        return _VARSAYILAN_SABIT_ACCENT
    m = re.search(r"\.theme-%s\s*\{(.*?)\}" % re.escape(theme_adi or ""), css, re.S)
    if m:
        a = re.search(r"--accent:\s*(#[0-9a-fA-F]{6})", m.group(1))
        if a:
            return a.group(1).upper()
    return _VARSAYILAN_SABIT_ACCENT


def pack_rengi(pack) -> str:
    """Bir CoursePack'in EFEKTİF vurgu rengi — build.py'nin gerçekte
    kullandığı renk. theme_color varsa odur; yoksa sabit temanın accent'i."""
    return (getattr(pack, "theme_color", None) or
            sabit_tema_rengi(getattr(pack, "theme", "")))


def _donem_kokleri(sinif=None, donem=None, sinav=None):
    """Taranacak dönem klasörleri. Üçü de verilmişse tek klasör, verilmemişse
    (ders adı tek başına sorulduysa) tüm dönemler sıralı biçimde taranır."""
    if sinif and donem and sinav:
        return [ROOT / f"{sinif}-sinif" / f"{donem}-donem" / str(sinav)]
    return sorted(p.parent for p in ROOT.glob("*-sinif/*-donem/*/src"))


def _src_kayitlari(donem_root: Path):
    """Bir dönemin src/*.py dosyalarını ÇALIŞTIRMADAN tarar (import etmek tüm
    ders içeriğini kurar, gereksiz ve yavaştır). Her ders modülü için
    (ders_klasoru, theme_color, theme) üçlüsünü döner."""
    src = donem_root / "src"
    if not src.is_dir():
        return []
    out = []
    for f in sorted(src.glob("*.py")):
        if f.stem in ("__init__", "kitap"):
            continue
        try:
            t = f.read_text(encoding="utf-8")
        except OSError:
            continue
        klas = re.search(r'ders_klasoru\s*=\s*["\'](.+?)["\']', t)
        if not klas:
            continue
        tc = re.search(r'theme_color\s*=\s*["\'](#[0-9a-fA-F]{6})["\']', t)
        th = re.search(r'\btheme\s*=\s*["\']([a-z]+)["\']', t)
        out.append({
            "modul": f.stem,
            "ders_klasoru": klas.group(1),
            "theme_color": tc.group(1).upper() if tc else None,
            "theme": th.group(1) if th else "",
        })
    return out


def kayitli_ders_rengi(ders_adi: str, sinif=None, donem=None, sinav=None):
    """Görsel kitap sisteminde bu ders için kayıtlı renk. Bulunamazsa None.
    Dönen: (hex, kaynak_aciklamasi)."""
    hedef = normalize_ders_adi(ders_adi)
    if not hedef:
        return None
    bulunan = []
    for kok in _donem_kokleri(sinif, donem, sinav):
        for kayit in _src_kayitlari(kok):
            if normalize_ders_adi(kayit["ders_klasoru"]) == hedef:
                renk = kayit["theme_color"] or sabit_tema_rengi(kayit["theme"])
                bulunan.append((renk, kayit["modul"]))
    if not bulunan:
        return None
    renk, modul = bulunan[0]                      # sıralı tarama -> deterministik
    diger = {r for r, _ in bulunan[1:] if r != renk}
    kaynak = f"src/{modul}.py"
    if diger:
        moduller = ", ".join(m for _, m in bulunan)
        kaynak += (f"  [UYARI: aynı ders adı için farklı renk veren birden çok "
                   f"modül var ({moduller}); ilki kullanıldı]")
    return renk, kaynak


# ---------------------------------------------------------------------------
# Genel giriş noktası
# ---------------------------------------------------------------------------
def ders_rengi(ders_adi: str, sinif=None, donem=None, sinav=None,
               *, kaynakla: bool = False):
    """Dersin vurgu rengi (hex, ör. '#8E3B1F').

    Önce görsel kitap sisteminde kayıtlı renk aranır (src/<ders>.py), yoksa
    ders adından deterministik olarak türetilir. `kaynakla=True` verilirse
    (hex, kaynak_aciklamasi) çifti döner.
    """
    kayit = kayitli_ders_rengi(ders_adi, sinif, donem, sinav)
    if kayit:
        renk, kaynak = kayit
    elif belirlenmis_renk(ders_adi):
        renk = belirlenmis_renk(ders_adi)
        kaynak = f"DERS_RENKLERI['{_aile_anahtari(ders_adi)}']"
    else:
        renk, kaynak = deterministik_renk(ders_adi), "ders adından türetildi"
    return (renk, kaynak) if kaynakla else renk


def hex_to_rgb(hexcolor: str):
    h = (hexcolor or "").lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def ders_rengi_rgb(ders_adi: str, sinif=None, donem=None, sinav=None):
    """python-docx için (r, g, b) üçlüsü:  RGBColor(*ders_rengi_rgb(...))"""
    return hex_to_rgb(ders_rengi(ders_adi, sinif, donem, sinav))


def tema_degiskenleri(ders_adi: str, sinif=None, donem=None, sinav=None) -> dict:
    """Dersin renginden türeyen TÜM tema değişkenleri (accent-dark, kapak
    gradyanı, kağıt tonu...). Anlatım PDF'i sadece --accent kullanır, ama
    ileride koyu bir ton (başlık altı çizgisi vb.) gerekirse buradan alınır."""
    return generate_theme_vars_from_hex(ders_rengi(ders_adi, sinif, donem, sinav))


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(
        prog="renk_uretici.py",
        description="Bir dersin vurgu rengini gösterir (görsel kitap sistemi "
                    "ve ders-anlatim skill'i bu AYNI değeri kullanır).")
    ap.add_argument("ders", nargs="?", help='Ders adı, ör. "HADİS"')
    ap.add_argument("--sinif")
    ap.add_argument("--donem")
    ap.add_argument("--sinav")
    ap.add_argument("--liste", action="store_true",
                    help="Dönemdeki tüm kayıtlı derslerin rengini listeler")
    ap.add_argument("--tablo", action="store_true",
                    help="Önceden belirlenmiş ders renklerini (DERS_RENKLERI) listeler")
    a = ap.parse_args()

    if a.tablo:
        print()
        print("=== DERS_RENKLERI (onceden belirlenmis -- renk = dersin ruhu) ===")
        for k, v in DERS_RENKLERI.items():
            print(f"  {k:38s} {v}   RGB{hex_to_rgb(v)}")
    elif a.liste:
        for kok in _donem_kokleri(a.sinif, a.donem, a.sinav):
            kayitlar = _src_kayitlari(kok)
            if not kayitlar:
                continue
            print(f"\n=== {kok.relative_to(ROOT)} ===")
            for k in kayitlar:
                renk = k["theme_color"] or sabit_tema_rengi(k["theme"])
                nasil = "theme_color" if k["theme_color"] else f"theme-{k['theme']}"
                print(f"  {k['ders_klasoru']:32s} {renk}  ({nasil}, {k['modul']}.py)")
    elif a.ders:
        renk, kaynak = ders_rengi(a.ders, a.sinif, a.donem, a.sinav, kaynakla=True)
        print(f"{a.ders}  ->  {renk}   RGB{hex_to_rgb(renk)}   [{kaynak}]")
    else:
        ap.error("bir ders adı ya da --liste verin")
