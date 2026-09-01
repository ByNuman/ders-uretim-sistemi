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
HARİTA ADAYI TESPİTİ — hangi bölüme harita konmalı?
=====================================================

Bu modül YALNIZCA tespit yapar: bir bölümün içeriği mekânsal mı, yani harita
kutusu hak ediyor mu? Haritanın kendisi Commons'tan hazır gelir
(Natural Earth verisi + gerçek koordinatlar).

Tespit bir ÖNERİ üretir, harita İÇERİĞİ üretmez: şehir/komşu listesini ve
yaklaşık sınır poligonunu ders modülünü yazan kişi kaynağa bakarak doldurur.
Sistemin "içerik uydurma yasağı" burada da geçerlidir -- tespit bir yer adı
ICAT ETMEZ.

TARİHÇE: 2026 Ağustos'a kadar bu dosyada fal.ai/gpt-image-2 ile harita
ÜRETEN bir bölüm vardı (prompt şablonu, önbellek, maliyet defteri). Kaldırıldı:
görüntü modeli sınırları ve şehir konumlarını uyduruyordu (gerekçe ve ölçülen
hatalar için bkz. harita_gomme.py başlığı). Eski üretim defteri
<dönem>/kaynaklar/haritalar/uretim_kaydi.jsonl'de tarihî kayıt olarak durur.
"""

from __future__ import annotations

import re

# --- OTOMATİK COĞRAFİ SİNYAL TESPİTİ -----------------------------------------
# Bu tespit bir ÖNERİ üretir, harita İÇERİĞİ üretmez: hangi bölümün harita
# adayı olduğunu söyler; şehir/komşu listesini ders modülünü yazan kişi (ya da
# Claude) kaynaktan doldurur. Sistemin "içerik uydurma" yasağı burada da
# geçerlidir — tespit bir yer adı ICAT ETMEZ.
# MEKÂN İSMİ (çekimli): "deniz" değil "denizi", "bölge" değil "bölgesinde".
# Çekimli biçimler bilerek seçildi -- yalın "bölge"/"rota"/"sınır" sözcükleri
# felsefe ve psikoloji metinlerinde MECAZ olarak sık geçiyor ("kavramın
# sınırları", "gelişim rotası") ve yalın listeyle Psikoloji'nin beş bölümü de
# harita adayı çıkıyordu. Çekimli coğrafya adları bu yanlış pozitifi keser.
# NİTELEYİCİ mekân ismi: yalnızca ÖNÜNDE ÖZEL AD varken sayılır.
# "Hazar denizi" / "Ceyhun nehri" / "Hârezm bölgesi" coğrafyadır; ama
# "beynin bölgesi" (Psikoloji) ya da "kavramın sınırları" (Sosyoloji)
# değildir. Önündeki sözcüğün büyük harfle başlaması şartı bu ikisini ayırır.
_MEKAN_NITELEYICI = (
    "denizi", "nehri", "ırmağı", "ovası", "ovasında", "havzası", "yarımadası",
    "körfezi", "boğazı", "çölü", "dağları", "vilayeti", "eyaleti", "şehri",
    "şehrinde", "şehrini", "kalesi", "başkenti", "bölgesi", "bölgesinde",
    "bölgesini", "coğrafyası",
)
# MUTLAK mekân ismi: tek başına da coğrafidir (yön/konum bildirir).
_MEKAN_MUTLAK = (
    "doğusunda", "batısında", "kuzeyinde", "güneyinde", "kıyısında",
    "kıyısına", "haritada", "topraklarına", "topraklarını",
)
# TOPRAK HAREKETİ: sınırların değiştiğini anlatan eylemler.
# Kelime SINIRIYLA aranır -- düz `in` araması "akın"ı "yakın" içinde bulup
# Psikoloji Bölüm 1'i harita adayı ilan ediyordu.
_HAREKET_KELIMELERI = (
    "fethet", "fethed", "fetih", "istila", "zapt", "akın", "hicret",
    "hâkimiyet", "hakimiyet", "işgal", "ele geçir", "göç et", "sefer düzenl",
)
_HAREKET_RE = re.compile(
    r"(?<![a-zâçğıîöşüû])(?:" + "|".join(_HAREKET_KELIMELERI) + r")", re.IGNORECASE)
_KELIME_RE = re.compile(r"[^\W\d_]+", re.UNICODE)
# Büyük harfle başlayıp yer adı SANILMAMASI gereken sık sözcükler.
_YER_DISI = {
    "Bu", "Bir", "Ancak", "Ayrıca", "Sultan", "Devlet", "Devleti", "İslam",
    "Türk", "Müslüman", "Hânedan", "Hanedan", "Böylece", "Nitekim", "Bölüm",
    "Başlangıçta", "Yerine", "Daha", "Onun", "Kendi",
}
_BUYUK_HARF = re.compile(r"\b([A-ZÂÇĞİÎÖŞÜÛ][a-zâçğıîöşüû]{2,})\b")

# Bir bölümün harita adayı sayılması için gereken en küçük puan.
SINYAL_ESIGI = 8


def _metinleri_topla(nesne, derinlik=0) -> list[str]:
    """Bir Chapter ağacındaki tüm düz metinleri toplar."""
    if derinlik > 8:
        return []
    if isinstance(nesne, str):
        return [nesne]
    if isinstance(nesne, (list, tuple, set)):
        out = []
        for x in nesne:
            out += _metinleri_topla(x, derinlik + 1)
        return out
    if isinstance(nesne, dict):
        out = []
        for x in nesne.values():
            out += _metinleri_topla(x, derinlik + 1)
        return out
    if hasattr(nesne, "__dict__"):
        out = []
        for x in vars(nesne).values():
            out += _metinleri_topla(x, derinlik + 1)
        return out
    return []


def _mekan_isimleri(metin: str) -> set[str]:
    """Metindeki gerçek mekân isimlerini bulur.

    Niteleyici isimler (bölgesi, nehri, denizi...) yalnızca ÖNLERİNDE büyük
    harfle başlayan bir sözcük varsa sayılır: "Hazar Denizi" evet, "beynin
    bölgesi" hayır. Mutlak isimler (doğusunda, kıyısında...) tek başına sayılır.
    """
    kelimeler = _KELIME_RE.findall(metin)
    bulunan: set[str] = set()
    for i, k in enumerate(kelimeler):
        dk = k.lower()
        if dk in _MEKAN_MUTLAK:
            bulunan.add(dk)
        elif dk in _MEKAN_NITELEYICI and i > 0:
            onceki = kelimeler[i - 1]
            if onceki[:1] in "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZÂÎÛ":
                bulunan.add(dk)
    return bulunan


def cografi_sinyal(chapter) -> dict:
    """Bir bölümün harita adayı olup olmadığını puanlar.

    Dönen dict: {"puan", "aday", "harita_var", "gerekceler"}

    ÖNCE KAPI, SONRA PUAN. Özel ad yoğunluğu TEK BAŞINA bir bölümü aday
    yapamaz -- her ders bölümü onlarca büyük harfli sözcük içerir (kişi
    adları, kavramlar, eser adları) ve yalnızca ona bakan bir eşik Psikoloji
    ile Çağdaş Felsefe'nin BÜTÜN bölümlerini harita adayı ilan ediyordu.
    Kapıdan geçmek için gerçek bir mekân kanıtı gerekir:

        · "Coğraf..." ile başlayan bir alt başlık, VEYA
        · en az 2 farklı çekimli mekân ismi ("Ceyhun nehri", "Hazar denizi"), VEYA
        · en az 1 mekân ismi + en az 1 toprak hareketi ("fethetti", "istila")

    Kapı kapalıysa puan 0'dır ve bölüm aday DEĞİLDİR. Kapı açıksa taban 6
    puan verilir, üstüne kanıt yoğunluğu eklenir (eşik SINYAL_ESIGI = 8).
    Zaten haritası olan bölüm aday sayılmaz (harita_var=True).
    """
    metinler = _metinleri_topla(chapter)
    duz = " ".join(metinler)
    dusuk = duz.lower()

    var = any(k == "mapsplit" for p in chapter.pages for k, _ in p.items)

    # --- kanıt toplama ---
    basliklar = [m for m in metinler
                 if m.lower().startswith(("coğraf", "cografi")) or "coğrafi bağlam" in m.lower()[:48]]
    mekanlar = sorted(_mekan_isimleri(duz))
    hareketler = sorted({m.group(0).lower() for m in _HAREKET_RE.finditer(dusuk)})

    # --- KAPI ---
    kapi = bool(basliklar) or len(mekanlar) >= 2 or (mekanlar and hareketler)
    if not kapi:
        return {
            "puan": 0, "aday": False, "harita_var": var,
            "gerekceler": ["mekân kanıtı yok (çekimli yer ismi/coğrafi başlık "
                           "bulunamadı) -- kavram ağırlıklı bölüm"],
        }

    gerekceler: list[str] = []
    puan = 6
    if basliklar:
        gerekceler.append(f"coğrafi alt başlık: “{basliklar[0][:46]}” (kapı)")
    else:
        gerekceler.append(f"mekân ismi: {', '.join(mekanlar[:4])} (kapı)")

    if mekanlar:
        katki = min(6, 2 * len(mekanlar))
        puan += katki
        gerekceler.append(f"{len(mekanlar)} çekimli mekân ismi "
                          f"({', '.join(mekanlar[:5])}) +{katki}")
    if hareketler:
        katki = min(4, 2 * len(hareketler))
        puan += katki
        gerekceler.append(f"{len(hareketler)} toprak hareketi "
                          f"({', '.join(hareketler[:4])}) +{katki}")

    # Özel adlar yalnızca DESTEKLEYİCİ kanıttır (en çok +2).
    adaylar = {w for w in _BUYUK_HARF.findall(duz) if w not in _YER_DISI}
    if len(adaylar) >= 6:
        puan += 2
        gerekceler.append(f"{len(adaylar)} özel ad +2 (destekleyici)")

    return {
        "puan": puan,
        "aday": puan >= SINYAL_ESIGI and not var,
        "harita_var": var,
        "gerekceler": gerekceler,
    }
