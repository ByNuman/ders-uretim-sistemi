# Bilinen tuzaklar / geçmişte düzeltilen buglar

Bu dosya, `templates/style.css` ve `build.py` üzerinde geçmişte yaşanmış ve
**halihazırda düzeltilmiş** hataların kaydıdır. Buradaki hiçbir maddeyi
uygulamak zorunda değilsiniz — düzeltmeler zaten yerinde. Amaç, şablonu
değiştirirken aynı hataya yeniden düşmemektir.

> Bu dosya CLAUDE.md'den ayrıldı: içeriği her oturumda okunması gereken bir
> işletim kuralı değil, gerektiğinde başvurulacak bir gerekçe kaydı.

---

Bunlar `templates/style.css` içinde zaten düzeltilmiş durumda — sadece
şablonu DEĞİŞTİRİRSEN tekrar bu hatalara düşmemek için bilgi amaçlı:

1. **Tablo başlığı görünmezliği**: `table.ctable th:first-child` için ayrı
   bir kural OLMAMALI — `td:first-child` ile aynı seçiciyi paylaşırsa
   başlık hücresi (koyu gradient zemin) `--ink` (koyu) renk alır ve
   okunmaz hale gelir. Başlık hücreleri her zaman `color:#fff` kalmalı.

2. **flex-shrink kesilmesi**: `.body-page` ve `.cover`, `.page`'in
   `flex-direction:column` özelliğini miras alır. Doğrudan çocuklarına
   (`.body-page > *`, `.cover-top`, `.cover-bottom`) `flex-shrink: 0`
   verilmezse, tarayıcı sayfa sınıra yaklaştığında elemanları sessizce
   küçültüp `overflow:hidden` ile kesiyordu — hem görsel bir hata hem de
   taşma denetimini yanıltan bir durumdu (küçültülmüş öğeler sayfaya
   "sığıyormuş" gibi ölçülüyordu). Bu kural olmadan asla ders üretme.

3. **Kapak amblem harfi**: Yunanca/özel semboller (örn. Σ) büyük punto'da
   X gibi çarpık görünür. Her zaman düz bir Latin harfi kullan.

4. **(ARTIK GEÇERLİ DEĞİL) Uzun `continue_tag`**: Bölüm devam sayfalarındaki
   "N. Bölüm · Devam" rozeti+başlık bloğu tamamen kaldırıldığı için
   `ChapterPage(continue_tag=...)` artık hiç render edilmiyor — bu tuzak
   sadece tarihi referans olarak duruyor. Sözlük/Test/Cevap Anahtarı devam
   sayfalarındaki sabit etiketler ("Sözlük · Devam" vb.) zaten kısa
   olduğundan bu risk onlarda hiç yaşanmadı.

5. **Aşırı yüklü tek sayfa**: Bir `ChapterPage`'e terms + person + 2 büyük
   tablo + callout + summary gibi çok fazla şey eklemek neredeyse her zaman
   taşmaya yol açar. Kesin bir sınır yoktur (içerik uzunluğuna bağlıdır) —
   bu yüzden adım 4-6'daki derle→kontrol et→böl döngüsü zorunludur, tahminle
   ilerleme.

6. **`:root` tema override'ı `.theme-XXXX` sınıfı tarafından ezilir**:
   `theme_color` ile dinamik tema enjekte edilirken, override CSS bloğu
   `:root{--accent:...}` şeklinde `<html>` elementini hedefler; ama
   `.theme-forest{--accent:...}` gibi sabit tema sınıfı `<body>` üzerinde
   tanımlıdır. `<body>`, `<html>`'den DAHA YAKIN bir ancestor olduğu için
   normal CSS inheritance'ta `.theme-forest` her zaman kazanır — specificity
   veya source order önemli değildir (inherited bir custom property, en
   yakın açık tanıma bakar). Çözüm: `theme_color` verildiğinde `<body>`
   class'ı hiçbir CSS kuralıyla eşleşmeyen bir isme (`theme-custom`) çevrilir
   (`master.html.j2`'de zaten uygulanmış durumda: `class="theme-{{ 'custom'
   if pack.theme_color else pack.theme }}"`). Bu satırı bozarsan
   `theme_color` sessizce hiçbir şey yapmaz (hata vermez, sadece eski tema
   görünür) — bu yüzden yeni bir renk denerken HER ZAMAN kapak sayfasını
   görsel kontrol et.

7. **`TEST_PER_PAGE_FIRST` çok yüksek olursa ilk test sayfası taşar**: İlk
   sayfada banner + 3'lü bilgi çubuğu + talimat kutusu da olduğu için, devam
   sayfalarına göre daha az yer kalır. Bu yüzden ilk sayfanın kapasitesi
   devam sayfalarınınkinden (`TEST_PER_PAGE = 8`) AYRI bir sabitte tutulur.
   175x250mm sürümünde bu sabit elle `6`'ya çekilmişti; A4'e geçilirken
   `tools/kalibre.py`'ye eklenip İLK KEZ ÖLÇÜLDÜ ve dönemin bütün dersleri
   üzerinde **`7`** çıktı (`8`'de bazı derslerin uzun soru metinleri ilk
   sayfayı taşırıyor). Sabit bu yüzden `7`'dir — bkz. yukarıdaki "Sayfalama
   sabitleri" ve `build.py`'deki `TEST_PER_PAGE_FIRST`.
   Yeni bir ders bu sabiti global olarak değiştirmemeli — sabit zaten
   birden fazla dersin en sıkı senaryosuna göre kalibredir; sadece o dersin
   soru metinleri alışılmadık uzunsa yine de taşma çıkabilir, o zaman
   metni kısaltmayı düşün, sabiti değil. Sayfa boyutu değişirse tahminle
   düzeltme yapma: `python tools/kalibre.py` çalıştırıp yeniden ölç.

8. **Test/Cevap Anahtarı 2 sütunlu düzen**: `column-count:2` ile CSS çoklu
   sütun düzeni kullanılıyor (CSS Grid değil) çünkü tarayıcı önce birinci
   sütunu doldurup sonra ikinciye geçiyor (`column-fill: balance` ile iki
   sütun dengeli yükseklikte kalıyor) — bu, gerçek bir sınav kağıdının okuma
   sırasına benzer. Her `.tq`/`.ans-item`'a `break-inside: avoid` şart,
   yoksa bir soru/cevap sütun sınırında ortadan bölünebilir.

9. **Bölüm devam başlığı kaldırıldı + alt bilgi artık gerçek sayfa numarası
   gösteriyor**: Eskiden bölüm devam sayfalarında "N. Bölüm · Devam" rozeti
   + `continue_tag` başlığı vardı — kullanıcı bunun gereksiz yer kapladığını
   bildirdi, bu yüzden `_ders_govde.html.j2`'deki `{% else %}` dalı (chcontinue
   bloğu) chapter döngüsünden tamamen kaldırıldı (bkz. yukarıdaki
   `ChapterPage` notu — Sözlük/Test/Cevap Anahtarı/LEGACY Sınav Hazırlık
   devam sayfalarında bu rozet hâlâ var, sadece bölüm sayfalarından
   kaldırıldı). Ayrıca Sözlük/Test/Cevap Anahtarı/LEGACY Sınav Hazırlık alt
   bilgilerindeki "A"/"A.2"/"B"/"B.2"/"C"/"C.2" gibi harf-bazlı sahte sayfa
   numaraları, İçindekiler'deki gerçek sayılarla (`page_starts`) eşleşmiyordu
   — bunlar da `page_starts["glossary"|"test"|"answer_key"|"exam"]`'den
   başlayan, chapter döngüsündeki `pageno` namespace'iyle AYNI desende
   artan gerçek tam sayı sayaçlarına çevrildi. Yeni bir sınav/sözlük
   sayfa türü eklenirse aynı deseni (namespace + her sayfa sonunda +1)
   kullan, harf-bazlı placeholder'a asla geri dönme.

10. **Chromium PDF çıktısını SESSİZCE kesebilir (kritik)**: 200+ sayfalık
    dokümanlarda `page.pdf()`, hiçbir hata vermeden eksik PDF üretebiliyor —
    aynı HTML bir denemede 273 sayfa, bir sonrakinde 132 sayfa verdi. Dosya
    sorunsuz açıldığı için fark edilmesi neredeyse imkânsızdır. Bu yüzden
    `render_pdf()` artık `expected_pages` alır, çıktının sayfa sayısını
    doğrular ve tutmuyorsa 3 kez yeniden dener, yine tutmazsa build'i
    hatayla durdurur. **Bu parametreyi kaldırma** — kaldırırsan kitabın
    yarısının eksik olduğu bir PDF sessizce teslim edilebilir.

11. **Kitapta tema `:root` ile enjekte edilemez**: 14 dersin teması tek HTML'de
    yan yana durduğu için her ders kendi kapsamını alır —
    `resolve_theme_css(hex, ".ders-3")` ve o sınıf `.page` elementinin
    ÜZERİNE yazılır (custom property'ler tanımlandıkları elementte ve altında
    geçerlidir, bu yüzden çalışır). `theme_color`'ı olmayan LEGACY dersler
    aynı yere `.theme-slate` gibi sabit sınıfı alır. Kitapta bir dersin rengi
    yanlış çıkıyorsa ilk bakılacak yer burasıdır (bkz. 6 numaralı tuzak —
    aynı problemin tek ders hâli).

12. **Ön kısım sayfa sayısı, ilk dersin offset'idir**: `front_matter_page_count()`
    ders sayısından ÖNCE hesaplanabilir olmak zorundadır (ana içindekiler kaç
    sayfa tutacak → dersler nereden başlayacak). Ön kısma yeni bir sayfa
    eklersen `FRONT_FIXED_PAGES` sabitini de artır; unutursan `build_front_matter()`
    içindeki assert derhal patlar (harita sayfası ile toplam uyuşmaz) — bu
    kasıtlıdır, sessiz kaymaya izin verme.

13. **Ghostscript'te `-dPDFX` PDF/X-3 kipidir, PDF/X-4 değil**: bu bayrak
    `CompatibilityLevel`'ı zorla 1.3'e çeker ve saydamlığı düzleştirir.
    Ölçüldü: aynı ders `-dPDFX` ile 23.7 MB / PDF 1.3 / ~5 dk, bayraksız
    (`-dCompatibilityLevel=1.6` + PDFX_def.ps'teki `GTS_PDFXVersion` +
    OutputIntent) 3.9 MB / PDF 1.6 / 22 sn. `cekirdek/pdfx.py` bilerek `-dPDFX`
    KULLANMAZ; geri eklerseniz dosya şişer ve kapak gradyanları rasterleşir.

14. **Ghostscript'in varsayılan görsel ayarları kapak gradyanını 22 dpi'a
    düşürüyordu**: `pdfwrite`'ın downsample varsayılanları Chromium'un gömdüğü
    tam sayfa rasterleri eziyor. `cekirdek/pdfx.py` bu yüzden `-dDownsample*Images=false`
    ve `-d*ImageFilter=/FlateEncode` veriyor (kayıpsız). Bu satırları silmeyin.

15. **PyMuPDF'in `set_xml_metadata()`'sı Ghostscript çıktısında sessizce
    düşüyordu**: bellekte görünüyor, `save()` sonrası dosyada yok. PDF/X-4
    kimliği (XMP `pdfxid:GTS_PDFXVersion`) bu yüzden pypdf ile yazılıyor
    (`pdfx.write_pdfx_xmp`) ve hemen ardından dosyadan okunarak DOĞRULANIYOR.
    pypdf varsayılan olarak `%PDF-1.3` başlığı yazdığı için
    `writer.pdf_header = reader.pdf_header` satırı şart.

16. **`page.pdf()`'e width/height vermek yerine `preferCSSPageSize: true`**:
    elle ölçü verildiğinde Chromium sayfayı ~0.35mm büyütüp içeriği 0.26mm
    sağa kaydırıyordu. `@page` kuralından okunduğunda içerik tam sol-üst
    köşeye oturuyor; `pdfx.set_print_boxes()` kutuları levhanın SOL-ÜST
    köşesinden ölçtüğü için TrimBox tam 210×297mm çıkıyor. (Chromium levhayı
    yine ~0.02-0.12mm büyük üretir; MediaBox bu yüzden BleedBox'tan birkaç
    yüzde mm büyüktür — bu normaldir, MediaBox'a dokunulmaz.)

17. **Dar sayfada flex sütunlarında uzun kelimeler taşıyor**: (175mm'lik eski
    sayfada tespit edildi, A4'te riski azaldı ama koruma duruyor) 5
    adımlı akış şemasında sütun ~22mm'ye düşüyor ve "Varoluşçuluğa" gibi
    kelimeler kutunun dışına sarkıyordu (flex öğesi min-content'in altına
    inemez). `.ov-flow-step` ve `.flowdiag .fstep` bu yüzden
    `min-width: 0; overflow-wrap: break-word;` taşır — kaldırmayın.

18. **Kapatılmamış tek bir `<b>` sayfa düzenini sessizce çökertir**: şablon
    içerik metinlerini KAÇIRMADAN basar (`<b>vurgu</b>` yazabilmeniz için).
    Bedeli, dengesiz bir etiketin geçerli HTML üretmesi ama tarayıcının hata
    kurtarma algoritmasını tetiklemesidir: etiket, kendinden sonraki KARDEŞ
    düğümleri kendi içine alır. Ölçüldü (`ornek_ders`, 2026 Ağustos): sözlükteki
    tek bir açık `<b>`, 2 sütunlu ızgarayı 4/10'a bölmüş, bir hücreyi 17,6mm
    yerine 123,5mm yapmış ve alt bilgiyi metnin ortasında bırakmıştı. Aynı tuzak
    `<ders>` gibi **köşeli parantezli yer tutucularda** da geçerlidir — tarayıcı
    bunu bilinmeyen bir etiket sayar ve yutar (`src/<ders>.py` ekranda
    `src/.py` görünüyordu). Metinde etiketi DÜZ METİN olarak göstermek
    istiyorsanız `&lt;b&gt;` yazın. **Ne taşma denetimi ne CI bunu yakalar**
    (çıktı taşmıyor, sadece yanlış); bu yüzden `validate()` artık `CoursePack`
    ağacındaki bütün metinleri gezip etiket dengesini denetler.

19. **`add_ayat()` başlığı artık opsiyoneldir**: uzun bir ayet grubu (Tefsir
    II'de 279mm'ye kadar) tek sayfaya sığmadığında `tools/dengele.py` grubu
    Ayah kartları arasından bölüyor; devam parçası `add_ayat(None, [...])`
    olarak basılıyor ve şablondaki `{% if title %}` koruması sayesinde başlık
    TEKRAR EDİLMİYOR (uydurma "devamı" başlığı üretilmiyor).

