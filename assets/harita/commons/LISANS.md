# Wikimedia Commons haritaları — künye ve lisans

Bu klasördeki dosyalar **depoya değil, kendi lisanslarına tabidir**. Deponun
GPL-3.0 lisansı bu dosyaları kapsamaz; her biri aşağıdaki künyeyle gelir.

Dosyalar Commons'tan geldiği gibi durur — **elle düzenlemeyin**.

Bu haritaların hiçbiri kitaba GÖMÜLMEZ. Her biri yalnızca **sınır çıkarma**
girdisidir: `cekirdek/sinir_cikar.py` kaynağın renkli alanını gerçek lon/lat
poligonuna çevirir (`assets/harita/sinir/<ad>.json`), harita sonra
`cekirdek/harita_cizim.py` ile Natural Earth coğrafyası üzerine BİZİM
motorumuzla çizilir. Böylece bütün yer adları Türkçe ve baskıda vektör olur,
PDF'e megabaytlık raster girmez. Çıkarımın kalibrasyonu kaynağın yanındaki
`<ad>.capa.json` dosyasında, metin olarak durur.

## CC BY-SA 4.0 yükümlülüğü

1. **Atıf**: yazar + lisans + bağlantı görünür olmalıdır. Sistem bunu
   `MapBox.source` alanından harita kutusunun altına basar.
2. **ShareAlike**: sınırı çıkarıp kendi motorumuzla çizmek onu "bizim
   çizimimiz" YAPMAZ — türetilmiş bir eserdir ve CC BY-SA kalır. Ders PDF'ini
   dağıtırsanız haritanın bu durumu atıf satırında yazılıdır.

## Dosyalar

### `harezmsahlar-devleti-1215.png`

| | |
|---|---|
| Özgün ad | File:Map of the Khwarazmian Empire.png |
| Yazar | Wikimedia Commons kullanıcısı **Ktrinko** |
| Lisans | **CC BY-SA 4.0** |
| Kaynak | https://commons.wikimedia.org/wiki/File:Map_of_the_Khwarazmian_Empire.png |
| İndirilme | 2026-08-30 |
| Biçim | Raster PNG, 3370 × 2175 (16 MB) |
| Kullanan | `2-sinif/2-donem/final/src/islam_tarihi_3.py` — Bölüm 1 |
| Kullanım | **Sınır çıkarma girdisi.** Görüntü kitaba girmez; `sinir/harezmsahlar-devleti-1215.json` poligonu bu dosyadan çıkarıldı ve harita kendi motorumuzla çizilir. Kaynağın kendi (İngilizce) etiketleri kullanılmaz — şehirler Türkçe adları ve gerçek koordinatlarıyla basılır. |

### `memluk-sultanligi-1317.jpg`

| | |
|---|---|
| Özgün ad | File:Mamluk Sultanate of Cairo 1317 AD.jpg |
| Yazar | Wikimedia Commons kullanıcısı **Ro4444** |
| Lisans | **CC BY-SA 4.0** |
| Kaynak | https://commons.wikimedia.org/wiki/File:Mamluk_Sultanate_of_Cairo_1317_AD.jpg |
| İndirilme | 2026-08-30 |
| Biçim | Raster JPG, 1800 × 1698 |
| Kullanan | `2-sinif/2-donem/final/src/islam_tarihi_3.py` — Bölüm 3 |
| Kullanım | **Sınır çıkarma girdisi.** Görüntü kitaba girmez; `sinir/memluk-sultanligi-1317.json` poligonu bu dosyadan çıkarıldı (12 çapa, 2. derece polinom, en büyük artık %1,18) ve harita kendi motorumuzla çizilir. |

### `delhi-sultanligi-halaci.png`

| | |
|---|---|
| Özgün ad | File:Map of the Khalji Sultanate.png |
| Yazar | Wikimedia Commons — taban harita **DEMIS Mapserver** (kamu malı) |
| Lisans | **CC BY-SA 3.0** |
| Kaynak | https://commons.wikimedia.org/wiki/File:Map_of_the_Khalji_Sultanate.png |
| İndirilme | 2026-08-30 |
| Biçim | Raster PNG, 2324 × 2151 (7 MB) |
| Kullanan | `2-sinif/2-donem/final/src/islam_tarihi_3.py` — Bölüm 4 |
| Kullanım | **Sınır çıkarma girdisi.** Görüntü kitaba girmez; `sinir/delhi-sultanligi-halaci.json` poligonu bu dosyadan çıkarıldı (`--tek-parca`: Himalaya gölgeleri gerçek sınırın %34'ü kadar sahte halka üretiyordu) ve harita kendi motorumuzla çizilir. |

### `mogol-imparatorlugu-genisleme-1206-1294.svg`

| | |
|---|---|
| Özgün ad | File:Expansion of the Mongol Empire.svg |
| Yazar | Wikimedia Commons kullanıcısı **Cattette** |
| Lisans | **CC BY-SA 4.0** |
| Kaynak | https://commons.wikimedia.org/wiki/File:Expansion_of_the_Mongol_Empire.svg |
| İndirilme | 2026-08-30 |
| Biçim | Gerçek vektör SVG (375 path, 139 `<text>`, gömülü raster yok), viewBox 992,13 × 595,28 |
| Kullanan | `2-sinif/2-donem/final/src/islam_tarihi_3.py` — Bölüm 5 |
| Kullanım | **Sınır çıkarma girdisi.** 2026-08-31'e kadar bu harita derse GÖMÜLÜYORDU (etiketleri çevrilerek); artık o yol yok. Yedi genişleme bandı tek sınırda birleştirilip (`ton` 19-52°) `sinir/mogol-imparatorlugu-genisleme-1206-1294.json` üretildi. Çapalar GÖZLE OKUNMADI: dosyanın kendi `<use>` şehir noktalarının transform matrisinden alındı — 34 çapa, 2. derece polinom, ortalama artık %0,66 / en büyük %1,79. (Aynı harita bir kez gözle okunan 17 çapayla %2,77 ortalama verip "çıkarılamaz" sayılmıştı.) |

### `rum-selcuklu-genisleme-1100-1240.svg`

| | |
|---|---|
| Özgün ad | File:Espansione del Sultanato di Rum (1100-1240).svg |
| Yazar | Wikimedia Commons kullanıcısı **Unochepassava94** |
| Lisans | **CC BY-SA 4.0** |
| Kaynak | https://commons.wikimedia.org/wiki/File:Espansione_del_Sultanato_di_Rum_(1100-1240).svg |
| İndirilme | 2026-08-30 |
| Biçim | Gerçek vektör SVG (226 path, 18 `<text>`, gömülü raster yok), viewBox 1577.9 × 721.3 |
| Kullanan | `2-sinif/2-donem/final/src/islam_tarihi_3.py` — Bölüm 2 |
| Kullanım | **Sınır çıkarma girdisi.** Dört genişleme bandı ayrı ayrı çıkarılıp `sinir/rum-selcuklu-genisleme-1100-1240.json` içinde katman olarak tutulur (11 çapa, en büyük artık %0,95); harita kendi motorumuzla çizilir, evre etiketleri kutunun altındaki HTML lejanttadır. |
