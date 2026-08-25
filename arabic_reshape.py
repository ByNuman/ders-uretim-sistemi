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
Arapça Reshaping Motoru
========================
Çıkardığımız gömülü font GSUB (otomatik harf bitiştirme) tablosuna sahip
değil. Bu modül, normal Arapça Unicode metnini alıp, Arabic Presentation
Forms-B bloğundaki (U+FE70-FEFF) doğru pozisyonel (isolated/initial/
medial/final) glyph'lere önceden çeviren bir "reshaper"dır -- tarayıcının
otomatik shaping yapmasını beklemek yerine, doğru glyph'i biz seçip veririz.
"""

# Her harf için (isolated, final, initial, medial) Presentation Forms-B kod noktaları.
# Sadece isolated/final varsa (right-joining harfler) initial/medial None'dır.
PRES_FORMS = {
    "ء": (0xFE80, None, None, None),
    "آ": (0xFE81, 0xFE82, None, None),
    "أ": (0xFE83, 0xFE84, None, None),
    "ؤ": (0xFE85, 0xFE86, None, None),
    "إ": (0xFE87, 0xFE88, None, None),
    "ئ": (0xFE89, 0xFE8A, 0xFE8B, 0xFE8C),
    "ا": (0xFE8D, 0xFE8E, None, None),
    "ب": (0xFE8F, 0xFE90, 0xFE91, 0xFE92),
    "ة": (0xFE93, 0xFE94, None, None),
    "ت": (0xFE95, 0xFE96, 0xFE97, 0xFE98),
    "ث": (0xFE99, 0xFE9A, 0xFE9B, 0xFE9C),
    "ج": (0xFE9D, 0xFE9E, 0xFE9F, 0xFEA0),
    "ح": (0xFEA1, 0xFEA2, 0xFEA3, 0xFEA4),
    "خ": (0xFEA5, 0xFEA6, 0xFEA7, 0xFEA8),
    "د": (0xFEA9, 0xFEAA, None, None),
    "ذ": (0xFEAB, 0xFEAC, None, None),
    "ر": (0xFEAD, 0xFEAE, None, None),
    "ز": (0xFEAF, 0xFEB0, None, None),
    "س": (0xFEB1, 0xFEB2, 0xFEB3, 0xFEB4),
    "ش": (0xFEB5, 0xFEB6, 0xFEB7, 0xFEB8),
    "ص": (0xFEB9, 0xFEBA, 0xFEBB, 0xFEBC),
    "ض": (0xFEBD, 0xFEBE, 0xFEBF, 0xFEC0),
    "ط": (0xFEC1, 0xFEC2, 0xFEC3, 0xFEC4),
    "ظ": (0xFEC5, 0xFEC6, 0xFEC7, 0xFEC8),
    "ع": (0xFEC9, 0xFECA, 0xFECB, 0xFECC),
    "غ": (0xFECD, 0xFECE, 0xFECF, 0xFED0),
    "ف": (0xFED1, 0xFED2, 0xFED3, 0xFED4),
    "ق": (0xFED5, 0xFED6, 0xFED7, 0xFED8),
    "ك": (0xFED9, 0xFEDA, 0xFEDB, 0xFEDC),
    "ل": (0xFEDD, 0xFEDE, 0xFEDF, 0xFEE0),
    "م": (0xFEE1, 0xFEE2, 0xFEE3, 0xFEE4),
    "ن": (0xFEE5, 0xFEE6, 0xFEE7, 0xFEE8),
    "ه": (0xFEE9, 0xFEEA, 0xFEEB, 0xFEEC),
    "و": (0xFEED, 0xFEEE, None, None),
    "ى": (0xFEEF, 0xFEF0, None, None),
    "ي": (0xFEF1, 0xFEF2, 0xFEF3, 0xFEF4),
}

# Right-joining: yalnız önceki harfe bağlanır, kendinden sonrakine bağlanmaz.
RIGHT_JOINING = set("ءآأؤإادذرزوى")
# Bu harfler kümesinden olmayan ve PRES_FORMS içinde bulunanlar dual-joining sayılır.

# Hareke ve diğer birleşen işaretler (bağlanma hesabına dahil edilmez, olduğu gibi geçer).
COMBINING_MARKS = set("\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652\u0653\u0654\u0655\u0670")

# Lam+Elif ligatürleri (isteğe bağlı ama geleneksel Arapça yazımda beklenir).
LAM_ALEF_LIGATURES = {
    ("ل", "ا"): (0xFEFB, 0xFEFC),   # isolated, final
    ("ل", "أ"): (0xFEF7, 0xFEF8),
    ("ل", "إ"): (0xFEF9, 0xFEFA),
    ("ل", "آ"): (0xFEF5, 0xFEF6),
}


def _is_connectable(ch: str) -> bool:
    return ch in PRES_FORMS


def _real_letters_with_marks(text: str):
    """Metni [(harf, [ardındaki harekeler])] listesine ayırır; boşluk/noktalama
    harf olmayan tek karakterlik 'blok' olarak (None, [tek karakter]) döner."""
    out = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch in COMBINING_MARKS:
            # başlangıçta yalnız hareke gelmemeli ama güvenlik için atla
            i += 1
            continue
        if _is_connectable(ch):
            marks = []
            j = i + 1
            while j < n and text[j] in COMBINING_MARKS:
                marks.append(text[j])
                j += 1
            out.append((ch, marks))
            i = j
        else:
            out.append((None, [ch]))
            i += 1
    return out


def reshape_arabic(text: str) -> str:
    """Normal Arapça Unicode metnini, çıkardığımız fontun desteklediği
    Presentation Forms-B pozisyonel glyph dizisine çevirir. Lam+Elif
    ligatürlerini de uygular."""
    tokens = _real_letters_with_marks(text)
    result_chars = []
    i = 0
    n = len(tokens)
    while i < n:
        letter, marks = tokens[i]
        if letter is None:
            result_chars.append(marks[0])
            i += 1
            continue

        prev_letter = tokens[i - 1][0] if i > 0 else None
        next_letter = tokens[i + 1][0] if i + 1 < n else None

        # Lam+Elif ligatür kontrolü
        if letter == "ل" and next_letter in ("ا", "أ", "إ", "آ"):
            key = (letter, next_letter)
            if key in LAM_ALEF_LIGATURES:
                iso_cp, fin_cp = LAM_ALEF_LIGATURES[key]
                connects_from_prev = (
                    prev_letter is not None
                    and prev_letter not in RIGHT_JOINING
                    and _is_connectable(prev_letter)
                )
                cp = fin_cp if connects_from_prev else iso_cp
                result_chars.append(chr(cp))
                result_chars.extend(marks)
                i += 2  # lam + elif birlikte tüketildi
                continue

        connects_from_prev = (
            prev_letter is not None
            and prev_letter not in RIGHT_JOINING
            and _is_connectable(prev_letter)
        )
        connects_to_next = (
            letter not in RIGHT_JOINING
            and next_letter is not None
            and _is_connectable(next_letter)
        )

        iso, fin, ini, med = PRES_FORMS[letter]
        if connects_from_prev and connects_to_next and med is not None:
            cp = med
        elif connects_from_prev and not connects_to_next:
            cp = fin if fin is not None else iso
        elif not connects_from_prev and connects_to_next and ini is not None:
            cp = ini
        else:
            cp = iso

        result_chars.append(chr(cp))
        result_chars.extend(marks)
        i += 1

    # Sonuç, PDF/HTML'de ayrı bir CSS ile (direction:rtl) gösterilecek;
    # glyph'ler zaten görsel sıraya göre değil mantıksal sırada üretildi,
    # tarayıcı RTL yönünü CSS ile uygular.
    return "".join(result_chars)
