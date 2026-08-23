# CMYK çıktı profili (ICC)

`build.py`, PDF/X-4 dönüşümünde bu klasördeki ICC profilini **çıktı koşulu
(OutputIntent)** olarak PDF'e gömer.

## FOGRA39 profilini buraya koyun

Avrupa kuşe ofset baskının fiili standardı **"ISO Coated v2 (ECI)" /
FOGRA39L**'dir. Lisansı gereği Ghostscript ile birlikte GELMEZ, elle
indirilmesi gerekir:

1. <https://www.eci.org/en/downloads> → "eci_offset_2009" paketini indirin
   (indirme, lisans onayı gerektiren bir form üzerinden yapılır).
2. Paketin içinden `ISOcoated_v2_eci.icc` dosyasını çıkarın.
3. Bu klasöre `ISOcoated_v2_eci.icc` adıyla kopyalayın.

Sonraki `python build.py ...` çalıştırmasında profil otomatik bulunur ve
"[UYARI] FOGRA39 profili bulunamadı" satırı kaybolur.

## Aranan dosya adları (öncelik sırasıyla)

    ISOcoated_v2_eci.icc
    ISOcoated_v2_300_eci.icc
    CoatedFOGRA39.icc
    FOGRA39L.icc

Bu adlardan hiçbiri yoksa klasördeki HERHANGİ bir `.icc` kullanılır.
Profili başka bir yerde tutmak isterseniz tam yolu `DERS_ICC` ortam
değişkenine yazın.

## Profil yoksa ne olur?

Build durmaz: Ghostscript'in kendi genel CMYK profili
(`iccprofiles/default_cmyk.icc`) kullanılır ve konsola bir uyarı basılır.
Dosya geçerli bir CMYK PDF olur, ama matbaanız özellikle FOGRA39 istiyorsa
renkler birebir tutmayabilir.
