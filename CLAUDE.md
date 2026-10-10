# CLAUDE.md — Görsel Ders Notu Üretim Sistemi

Bu dosya, bu repodaki "Görsel Ders Notu Kitabı" üretim sistemini kullanarak yeni
bir ders işlerken Claude Code'un izlemesi gereken **işletim talimatlarını** içerir.
Kullanıcı sana bir ders özeti (PDF/metin) verip "bunu görsel ders notuna çevir"
dediğinde, buradaki süreci baştan sona uygula.

## Nerede ne yazıyor

Bu dosya *ne yapacağını* söyler. *Neden öyle olduğunu* öğrenmen gerekirse:

| Soru | Dosya |
|---|---|
| "Bu sabiti değiştirebilir miyim? Bu sayı nereden geldi?" | `docs/OLCUMLER.md` — sayfa geometrisi, sayfalama sabitleri, İçindekiler kapasitesi, PDF/X-4 CMYK |
| "Bu CSS kuralına neden dokunmamalıyım?" | `docs/TUZAKLAR.md` — 19 madde, geçmişte düzeltilmiş buglar |
| "Renk motoru nasıl çalışıyor? Tasarım nasıl kurulu?" | `docs/TASARIM.md` — tema motoru, `DERS_RENKLERI`, tasarım sistemi |
| "Bu yön kararı neden alındı?" | Bu deponun dışında — sürdürenin kişisel karar arşivinde. Klonlayan biri için erişilebilir değildir; kodu kullanmak için gerekmez. |

**Bir tasarım/ölçüm sorunu bildirilirse ilgili `docs/` dosyasını AÇ** — oradaki
gerekçeyi okumadan `templates/style.css` veya `build.py` sabitlerine dokunma.

---

## KRİTİK KURAL 1: Birleşik Kitaba Otomatik Ekleme Yasağı

Yeni bir ders üretildiğinde veya güncellendiğinde, bu dersi birleşik kitaba
OTOMATİK OLARAK EKLEME. Birleştirme scriptini çalıştırma.

- Tekil ders üretimi ve birleşik kitap üretimi **tamamen ayrı, birbirini
  tetiklemeyen** iki iştir.
- Bir ders için "işle", "anlat", "görsel not hazırla" isteği geldiğinde sonucu
  sadece o dersin kendi PDF'i olarak üret ve ilgili dönemin
  `gorsel_ders_notlari/<DERS ADI>/` klasörüne koy. Birleştirme scriptine DOKUNMA.
- Birleşik kitaba ekleme/çıkarma/sıralama SADECE kullanıcı açıkça "birleşik kitaba
  ekle", "kitabı güncelle", "birleştirmeyi çalıştır" dediğinde yapılır.
- Bu yasak HER SINAV DÖNEMİ İÇİN AYRI geçerlidir; her dönemin kendi `src/kitap.py`'si
  ve kendi birleşik kitabı vardır.
- İstek belirsizse, birleştirmeyi ÇALIŞTIRMADAN ÖNCE sor: "Bu dersi birleşik kitaba
  da eklememi ister misiniz?"
- Yeni ders üretirken **tekil-kitap trim boyutunu** kullan, birleşik kitabınkini
  DEĞİL — iki config birbirinden bağımsızdır (`SINGLE_GEOMETRY` / `BOOK_GEOMETRY`).

## KRİTİK KURAL 2: Sınav Dönemi Varsayılmaz — Her Zaman Sorulur

Hiçbir script'in varsayılan dönemi YOKTUR ve sen de varsayma:

- Kullanıcı sınıf/dönem/sınav belirtmediyse **derlemeden ÖNCE sor**:
  "Bu ders hangi sınıf / dönem / sınav dönemine ait? (ör. 3. sınıf · 1. dönem · vize)"
- Tahmin etme, "en son hangisini kullandıysak" deme, `2-sinif/2-donem/final` varsayma.
  Yanlış döneme yazılan ders sessizce yanlış birleşik kitaba girer — geri alması zordur.
- Her komut üç parametreyi birlikte alır: `--sinif {2,3} --donem {1,2} --sinav {vize,final}`.
  Parametre verilmezse script interaktif sorar; soramıyorsa net bir hatayla durur.
- Aynı ders adı farklı dönemlerde ayrı ayrı bulunabilir ve bunlar TAMAMEN bağımsızdır
  (ayrı `src/`, ayrı çıktı, ayrı birleşik kitap).

## KRİTİK KURAL 3: Üretim zinciri ve `<DERS ADI>` alt klasörü

```
ders_kaynaklari/ + ogretmen_notlari/  ->  özetlenmiş_dersler/  ->  gorsel_ders_notlari/
      (ham girdi)                          (yazılı özet)            (kitap formatı, build.py)
```

Bu üç aşama **ayrı şeylerdir, birbirinin yerine geçmez**:

* `özetlenmiş_dersler/` = ham kaynağın **yazılı** özeti. build.py'nin ÇIKTISI DEĞİL,
  GİRDİSİDİR.
* `gorsel_ders_notlari/` = build.py'nin ürettiği kitap formatındaki PDF. Tek gerçek
  çıktı klasörü budur.

**Her üç klasörde de dosyalar köke DEĞİL, dersin adını taşıyan alt klasöre konur:**

```
3-sinif/1-donem/final/kaynaklar/özetlenmiş_dersler/SİSTEMATİK KELAM I/sistematik-kelam-1-ozet.pdf
3-sinif/1-donem/final/gorsel_ders_notlari/SİSTEMATİK KELAM I/sistematik-kelam-i.pdf
```

`build.py` bu alt klasörü otomatik oluşturur. Klasör adı `CoursePack.ders_klasoru`
alanından okunur. Aynı kural `ders-anlatim` skill'inin çıktı klasörleri için de
geçerlidir. Birleşik kitaplarda:
- **Dönem Birleşik Kitabı:** Tek bir derse ait olmadığı için `gorsel_ders_notlari/` **köküne** yazılır (`donem-ders-notlari-kitabi.pdf`).
- **Haftalık Birleşik Kitaplar (Kullanıcı Kuralı 2026-09):** Kullanıcı haftalık dersleri birleştirmeyi istediğinde, çıktı mutlaka `gorsel_ders_notlari/HAFTALIK DERSLER/<N>. Hafta/` klasörüne yazılır (ör. `HAFTALIK DERSLER/1. Hafta/haftalik-ders-1-hafta.pdf`). `BookPack.cikti_klasoru="HAFTALIK DERSLER/<N>. Hafta"` alanı bunu yönetir. İlgili haftanın kapak görseli (`haftalik-ders-<N>-hafta-kapak.png`) varsa `cover_image` olarak atanır.

Dönem boyunca ders haftalık işlenir ve `<DERS ADI>/` altında `NN-hafta/` alt
klasörleri birikir; ham haftalık materyal `ders_kaynaklari/<DERS ADI>/NN-hafta/`,
o haftanın **çalışma belgesi** (işlenen içeriğin derinlemesine anlatımı + ders takip
başlığı) `özetlenmiş_dersler/<DERS ADI>/NN-hafta/` altına konur. Sınav özeti ve
görsel ders notu üretilirken bu haftalık belgeler + (varsa) kitap birlikte kullanılır.
Ayrıntı: "Haftalık ders akışı" bölümü.

## KRİTİK KURAL 4: İçindekiler TEK SAYFADIR

Ders kaç bölümlü olursa olsun İçindekiler ASLA ikinci sayfaya taşmaz.
`toc_page_count()` sabit `1` döndürür; "İçindekiler · Devam" diye bir sayfa
ÜRETİLMEZ. Sığdırmayı sayfa bölme değil **CSS sıkışık kipi** yapar (satır sayısı
`TOC_COMPACT_THRESHOLD`'u aşınca devreye girer; alt başlık tek satıra kırpılır ve
satır yüksekliği sabitlenir, böylece taşma yapısal olarak imkânsızlaşır).

**14 satır (= 12 bölüm) aşılırsa** `validate()` derlemeden önce uyarı basar
(`TOC_MAX_ROWS`); o noktada satırı daha da sıkıştırmak yerine dersi bölmeyi
değerlendir. `.toc-compact` değerlerini elle küçültme — ölçümle bağlıdırlar.

Ölçümler ve eşiklerin nereden geldiği: `docs/OLCUMLER.md`.

## KRİTİK KURAL 5: Kapak Tasarımı — Varsayılan Klasik Vektörel Kapaktır (cover_image="")

Görsel ders notu üretilirken kapak için **her zaman sistemin yerel CSS/HTML vektörel kapağı kullanılır (`cover_image=""`)**:
- Harici bir kapak görseli (`cover_image`) otomatik olarak aranmaz, resim/difüzyon yapay zekasıyla üretilmez veya görsel manipülasyonla yamalanmaz.
- Klasik vektörel kapak; dersin renk temasında degrade zemin, usturlap amblemi, altın köşe süsleri, amblem harfi, başlık/alt başlık, cam efektli istatistik kutuları ve kurumsal alt bilgiyi kusursuz, jilet gibi net vektörel formatta otomatik çizer.
- **Kapak Açıklaması (`description`):** Kapak sayfasında başlığın altındaki açıklama/tanıtım metni daima **kısa ve öz 1–2 cümle** olmalıdır; asla uzun paragraflar yazılmaz.

## KRİTİK KURAL 5.1: Sayfa Düzeni ve Ön Kısım Mimarisi (Senaryo A — Kapak Arkası Boş Sayfa)

- **Genel Bakış Sayfası Kaldırılmıştır:** Tekil görsel ders notlarında "Genel Bakış" sayfası okunmadan atlandığı ve sayfa israfı oluşturduğu için tamamen kaldırılmıştır (`OVERVIEW_PAGES = 0`).
- **Kapak Arkası Boş Sayfa (Çift Taraflı Baskı / Forma Uyumu):** Hem tekil derslerde hem birleşik kitapta kapağın arkasına boş sayfa (`<section class="page blank-page ...">`) yerleştirilir. Böylece çift taraflı baskıda içindekiler sağ sayfada açılır.
- **Tekil Ders Notu Sayfa Akışı:** `s.1 Kapak` → `s.2 Boş Sayfa` → `s.3 İçindekiler` → `s.4 Bölüm 1` (Bölümler daima 4. sayfadan başlar).
- **Birleşik Kitap Ön Kısım Sadeleştirmesi:** Birleşik kitapta atlanan ve sayfa israfı oluşturan "Künye", "Bu Kitap Nasıl Kullanılır" ve "Sayfa Rehberi" sayfaları kaldırılmıştır (`FRONT_FIXED_PAGES = 2`).
- **Birleşik Kitap Sayfa Akışı:** `s.1 Ana Kapak` → `s.2 Boş Sayfa` → `s.3-4 Ana İçindekiler` → `s.5 1. Ders Başlangıcı` (1. ders kapağı s.5 → s.6 Boş Sayfa → s.7 İçindekiler → s.8 Bölüm 1...).

## KRİTİK KURAL 6: Müfredat Bilgi Paketleri Eski ve Bağlayıcı Değildir — Tek Bağlayıcı Kaynak Ders Kitapları ve Öğretmenin Verdiği Ek Kaynaklardır (Tüm Dersler İçin Geçerli)

Üniversite bilgi sistemi / Bologna müfredat bilgi paketleri (`<ders> MÜFREDAT BİLGİ PAKETİ.pdf`) sıklıkla eski, revize edilmemiş ve fiili ders işleyişiyle uyuşmayan evraklardır. **Bu paketler bağlayıcı DEĞİLDİR.**
- Ders notu, haftalık çalışma belgesi veya görsel ders notu üretilirken **asla "müfredat–kitap karşılaştırması", "metin sapması", "müfredat vs. kitap çelişkisi" gibi bölümler, tablolar veya uyarılar eklenmez**.
- Sorumlu olunan yegâne kaynak: `<D>/kaynaklar/ders_kaynaklari/` altındaki ders kitapları / materyalleri ve öğretmenin doğrudan bildirdiği ek kaynaklardır.
- Öğretmen ek bir kaynak veya farklı bir metin bildirirse, kullanıcı bunu belirtecektir. Aksi takdirde ders kitabının ünite ve konu akışı doğrudan esas alınır.
- Bu kural sistemdeki **TÜM DERSLER** için istisnasız geçerlidir.

## KRİTİK KURAL 7: Öğretmen İsimleri Ders Programındaki Resmî İsimlerle Birebir Yazılır & Görsel Notlarda İsim Yasağı

- **Yazılı Anlatımlarda Resmî İsim Zorunluluğu:** Yazılı ders anlatımı künyelerinde (`ders_anlatimlari/`) veya dönem planlama analizlerinde öğretim elemanı adı geçecekse; rastgele veya tahmini adlandırma yapılamaz. Doğrudan haftalık ders programındaki resmî unvan ve isim (ör. "Doç. Dr. Nevzat AYDIN", "Dr. Öğr. Üyesi Adem GÜNEŞ", "Öğr. Gör. Muhammed Salih SÜRÜCÜ") birebir esas alınır.
- **Görsel Ders Notlarında Hoca İsmi Kullanılmaz (KESİN YASAK):** Hocaların izni olmadan isimlerini görsel ders notlarında (`src/*.py` -> PDF / HTML) geçirmek kesinlikle yasaktır. Kapaklarda, açıklamalarda (`description`), soru köklerinde, çözümlü test cevap anahtarlarında (`AnswerItem`) veya arka kapaklarda hoca isimleri zikredilmez; yalnızca "ders anlatımında", "ders içi sınav yönergesinde" gibi pedagojik ifadeler kullanılır.

## KRİTİK KURAL 8: Görsel Ders Notu Üretiminde 7 Temel Standart ve Kalite Protokolü (Tüm Dersler İçin Zorunlu)

Herhangi bir ders veya hafta için görsel ders notu (`src/<ders>.py` -> `build.py`) üretilirken veya güncellenirken aşağıdaki **7 temel standart istisnasız uygulanmak zorundadır**:

### 1. Standart: Resmî Ders Renk Teması
- Her dersin resmî tema rengi `cekirdek/renk_uretici.py` içindeki `DERS_RENKLERI` tablosundan birebir alınır (ör. HADİS / HADİS III için `#664324` / Koyu Deri Cilt `theme="leather"`, KELAM için `#14665a` vb.).
- Asla başka bir dersin rengi (ör. Hadis için yeşil/forest) kopyalanıp yapıştırılamaz veya varsayılan bir renk uydurulamaz.

### 2. Standart: Vektörel Kapak Düzeni
- Kapak her zaman sistemin yerel CSS/SVG vektörel kapağı ile üretilir: `cover_image=""`.
- Harici bir kapak görseli aranmaz veya üretilmez. Usturlap motifi, altın köşe süsleri, amblem harfi, başlık, ders kodu ve şeffaf istatistik kutularını içeren native vektörel kapak esastır (Kritik Kural 5). Özel kapak sadece kullanıcı açıkça talep ederse atanır.

### 3. Standart: Sayfa Verimliliği & Sıfır Sayfa İsrafı (0 mm Taşma)
- Sayfalarda yapay boşluklar, seyreklik ve sayfa israfı kesinlikle yasaktır. Her bölüm sayfası `%90–100` doluluk bandında dengelenmelidir.
- Her derleme sonrasında `python tools/olcum.py <slug> --sinif X --donem Y --sinav Z` çalıştırılarak sayfa dolulukları kontrol edilir; `build.py` taşma denetiminde `0 mm taşma` ("tüm sayfalar 210x297mm sınırları içinde ✓") görülmeden üretim tamamlanmış sayılamaz.

### 4. Standart: Tipografik Hiyerarşi ve Görsel Vurgu Düzeni
- Madde metinlerinde sıradan markdown (`**`, `*`) ile kuru metin dizilmez.
- Her madde mutlaka `.k-badge` (kategoriye göre `.gold`, `.alert`, `.subtle`), `.k-title` (başlık) ve sol çizgili `.k-subitem` hiyerarşisiyle sunulur.
- Arapça nass ve metin alıntılarında `.k-nass` kartı (içinde `.ar` ve `.meal`) kullanılır.
- Hayati kaideler, terim tanımları ve sınavda puan getirecek anahtar ibareler `<u>` ile altı çizilerek vurgulanır.
- **Çift Liste İmi (`–`) Önleme Kuralı:** Kutu kullanılan maddelerde (`.k-nass`, `.k-subitem`), `li:has(> .k-nass:first-child)::before { display: none !important; }` defansı uygulanır ve `k-badge` ile altındaki kutular tekil bir `<li>` içinde hiyerarşik yapılandırılır; kutu kenarlıklarına çakışan çift tireler kesin olarak engellenir.

### 5. Standart: Kelime ve Font Büyüklüğü Hiyerarşisi (2026-09 Ölçeği)
- **Arapça ve Harekeli İbareler (`bdi`, `.ar`, `[dir="rtl"]`):** Harekelerin ve harflerin net seçilebilmesi için `%128–132` daha büyük (`font-size: 1.28em–1.32em`) ve ferah satır aralığıyla (`line-height: 1.68`) render edilir. 4'lü anahtar terim kutuları (`KeyTerm`), tablolar, sözlük ve metin içi âyet şahitleri (`﴿...﴾`) kesinlikle `<bdi class="ar">` ile sarılır; çıplak Latin font boyutunda bırakılmaz. Nass kutusu nassı `font-size: 12.0pt` olarak öne çıkar.
- **BiDi İzolasyonu & Parantez Kuralı:** LTR akış içerisinde raw Arapça karakterler nedeniyle cümlenin sağına veya başına sıçrayan liste noktaları (`•`), iki noktalar (`:`), tireler (`-`), tırnaklar ve parantezler `<bdi class="ar">` ile sarılarak izole edilir. Parantez içi açıklamalarda parantez yönünün ve noktalama işaretlerinin ters dönmesini önlemek için: daima önce Türkçe ifade yazılır, ardından parantez içinde izole Arapça terim (`(<bdi class="ar">...</bdi>)`) verilir.
- **Türkçe Gövde ve Metin Alanları:** Gövde metinleri 9.35pt, tablo hücreleri 8.65pt, kutu metinleri 9.15pt, sözlük tanımları 8.75pt olarak hiyerarşik okunabilirlik standartlarına tam uyar.

### 6. Standart: Yenilenen Test ve Çözümlü Cevap Anahtarı Mimarisi (Pedagojik Zorluk Piramidi & Tipografik Ferahlık)
- **20 Soruluk Pedagojik Zorluk Piramidi:**
  - **1–6. Sorular (Kolay):** Doğrudan kavram, terim ve isim bilgisi.
  - **7–14. Sorular (Orta):** Karşılaştırma, usûl tahlili, sebep-sonuç ilişkileri.
  - **15–20. Sorular (Zor):** Öncüllü sorular (Roman rakamlı `I, II, III`), olumsuz soru kökleri ve Arapça ibare çözümlemeleri.
- **%70 Düşündürücü & Akademik Derinlik Standardı:**
  - Soruların en az %70'i kuru ezber yerine; usûl tahlili, mezhep/ekol mukayesesi, neden-sonuç bağıntıları ve öncüllü derinlik taşımalıdır.
  - Çeldiriciler uydurma veya basit olamaz; konunun püf noktasını bilmeyi gerektiren kardeş ıstılahlar, zıt mezhep görüşleri veya benzer kaidelerden kurulur.
- **Şık Boyutu Eşitliği & Homojenliği (Uzun Şık İpucu Yasağı):**
  - "En uzun şık doğru cevaptır" yanılsaması KESİNLİKLE YASAKTIR.
  - 5 seçeneğin (`A, B, C, D, E`) tamamı paralel cümle yapısında, birbirine denk kelime sayısında ve eşit satır/hacim dengesinde yazılır.
- **Parantez İçi Tüyo Yasağı:**
  - Soru kökünde veya şıklarda terimin Türkçe anlamını parantez içinde vermek (ör. `«الأَثَرَةُ» (bencillik)`, `cevâbü't-taleb (emrin cevabı)`) KESİNLİKLE YASAKTIR.
  - Sadece BiDi standardı gereği izole edilen Arapça ibareler (`<bdi class="ar">...</bdi>`) yer alabilir; anlam ve izahlar çözümlü cevap anahtarında öğretici olarak verilir.
- **Test Sayfa Mimarisi (10 + 10 Soru & Çizgisiz Ferah Boşluk):**
  - Test tam **2 sayfaya (10 + 10 soru)** dengelenir.
  - Sorular arasında göz yoran kesik/düz çizgiler KULLANILMAZ. Sorular birbirinden temiz ve ferah dikey beyaz boşlukla (`margin-bottom: 1.0–2.0mm`) ayrılır; soruların ve seçeneklerin birbirine yapışması kesin olarak engellenir.
  - Soru başlığı (`.tq-head`) ve şıklar (`.tq-options`) arasında nefes alan mikro-mesafeler korunarak iki sütuna dengeli yayılır. Soruların sadece tepeye sıkışıp sayfa altında gereksiz devasa boşluk bırakması önlenir.
- **Çözümlü Cevap Anahtarı Mimarisi (Genişletilmiş Punto ve Sayfa Dengesi):**
  - Tam **1 sayfaya** dengeli sığdırılır; sayfanın alt yarısının boş kalması engellenerek `%85–95` doluluk sağlanır.
  - Çözüm metinleri minik punto yerine gövde standardına yakın (`9.2pt`), ferah satır aralığı (`line-height: 1.34`), belirgin doğru cevap hap rozetleri (`8.2pt`) ve maddeler arası nefes alan aralıklarla (`.ans-item: 2.6mm`) sunulur.
  - Her soruda doğru şıkkın yanında analitik gerekçesi ve geçen Arapça ibarelerin `<span class="ans-trans">` Türkçe mealleri eksiksiz verilir. Öğrenci soruyu yanlış yapsa dahi cevap anahtarını okuduğunda konuyu tam olarak öğrenir.

### 7. Standart: Görsel Ekleme Kutuları, Pedagojik Görsel Matrisi ve Esneklik Kuralı (4:3)
- Her bölüme en az bir adet `add_block_gorsel(BulletBlock(...), baslik="...")` şablonuyla 4:3 oranında görsel çerçevesi (`image=None`) eklenir.

#### A) Temel İlke ve Sınırsız Esneklik Kuralı:
- Görseller kuru bir süs değil; öğrenciye doğrudan kavram, usûl veya sınav bilgisi kazandıran araçlardır.
- **Sistem ASLA sadece belirli şablonlarla sınırlı DEĞİLDİR.** Asistan dersin ve konunun doğasına göre aşağıdaki pedagojik şablonlardan yararlanır; ancak konu somut bir el yazması sayfası, arşiv vesikası, kitabe, arkeolojik sikke, mimari rölöve/külliye planı, ordugâh krokisi, ses/mahreç anatomisi veya istatistik grafiği gerektiriyorsa tamamen konuya özel özgün görsel önerisi getirilir.

#### B) Fakülte ve 3. Sınıf Ders Havuzuna Uygun Pedagojik Görsel Matrisi:
1. **İnfografik Harita (Coğrafya & Havzalar):** Tefsir, Tasavvuf, İslâm Tarihi ve Medeniyeti. *(Örn: Mekke-Medine-Kûfe tefsir ekolleri, tasavvuf havzaları veya fetih yolları haritası)*.
2. **Kronolojik Zaman Çizelgesi (Dönemler & Evreler):** Hadis, Kelâm, Fıkıh ve Düşünce Tarihi. *(Örn: Hadis tedvin/tasnif asırları veya Kelâm'da Mütekaddimîn → Müteahhirîn → Yeni İlm-i Kelâm evreleri)*.
3. **İsnad & Sened Ağacı Şeması (Hadis & Tefsir):** Hadis rivayet zincirleri, âlî/nâzil kollar ve Medârü'l-Hadîs (müşterek râvi) kavşağı.
4. **Hüküm Karar Ağacı (İslâm Hukuku & Fıkıh Usûlü):** Şartlar, rükünler ve mânilere göre dallanan hüküm akışı *(Teklîfî/Vaz'î; sahih, fâsid, bâtıl)*.
5. **Hiyerarşik Değerler & Deliller Piramidi (Usûl & Ahlâk):** Tabanı geniş, zirvesi daralan öncelik piramitleri *(Makāsıdü'ş-Şerîa: Tahsîniyyât → Hâciyyât → Zarûriyyât-ı Hamse)*.
6. **Çoklu Mezhep / Ekol Matrisi (Kelâm & Mezhepler Tarihi):** İtikadî bir meselede 3-4 farklı mezhebin duruşunu gösteren mukayese şeması *(Örn: Büyük günah meselesinde Hâricî, Mu'tezile, Mürcie ve Ehl-i Sünnet)*.
7. **İki Kutuplu Karşılaştırma Şeması (Münazara & Usûl):** İki zıt görüşün mukayesesi *(Sekr vs. Sahv, Gazâlî vs. İbn Rüşd Tehâfüt münazarası, Fukahâ vs. Mütekellimîn usûlü)*.
8. **Silsile & İlim/Eser Ağacı (Kıraat, Hadis, Tasavvuf):** 7/10 Kıraat imamı ve râvileri silsilesi, tarikat mürşid halkası veya Kütüb-i Sitte müellifleri bağı.
9. **Kavram & Nitelik Şeması (Felsefe, Kelâm, Mantık):** Bir şahsiyetin veya doktrinin kavram matrisi *(Örn: Şems'in zâhirî ilimleri, Allah'ın sıfatları, Fârâbî'nin Faal Akıl teorisi)*.
10. **Döngüsel / Çevrimsel Süreç Modeli (Din Psikolojisi, Sosyoloji, Ahlâk):** Birbirini besleyen dairesel gelişim döngüleri *(Nefsin 7 mertebesi çarkı, inanç ve şüphe gelişim çevrimi, iletişim döngüsü)*.
11. **Yapısal Kesit & Eser Mimarisi (Hadis, Tefsir, Arap Dili):** Sahîh-i Buhârî bâb mimarisi, klasik el yazması metin-şerh-haşiye anatomisi veya tecvid harf mahreçleri anatomisi.

#### C) AI Üretim & Prompt İlkeleri:
- Görsel içi metinlerde harf bozulmalarını önlemek için uzun cümleler yasaktır; yalnızca 1-3 kelimelik net başlıklar, kavram etiketleri ve oklar hedeflenir.
- Mahremiyet/hürmet filtrelerine titizlikle uyulur.
- Görseller dersin resmî tema rengiyle (`theme_color`) uyumlu vektörel infografik ve minimalist tarihi illüstrasyon dilinde üretilir.
- Çerçeve CSS'te `aspect-ratio: 4 / 3` olduğundan tüm görseller mutlaka **4:3** oranında üretilir.

#### D) Görsel Bağlama Kuralı:
- Kullanıcı görselleri `görseller/` klasörüne eklediğinde `baslik=""` yapılır (başlık silinir) ve `image=_foto("<dosya>.jpg")` atanır.

#### E) Kullanıcı Meta-Prompt Standardı (Otomatik & Kesintisiz Tekil Üretim Şablonu):
Kullanıcının harici yapay zekâ araçlarına (ChatGPT, Claude, Gemini vb.) görsel ürettirirken kullandığı; **kolaj yapmayı kesin olarak yasaklayan**, kullanıcıdan onay beklemeden **her kutu için arka arkaya bağımsız ve müstakil 4:3 görsel üreten** resmî yönergedir:

```text
Bu PDF'teki görsel kutularını analiz et. Her kutunun üzerinde ne olması gerektiği şema/infografik promptu yazıyor.

KOLAJ YASAĞI (EN ÖNEMLİ KURAL):
Tüm konuları tek bir görselde, paneller halinde veya poster şeklinde ASLA BİRLEŞTİRME! Her kutu için tamamen AYRI, BAĞIMSIZ ve TEKİL birer görsel dosyası oluşturacaksın.

OTOMATİK ÜRETİM PROTOKOLÜ (KESİNTİSİZ & ONAYSIZ):
- Benden "devam", "sıradaki" veya onay BEKLEME!
- Sırayla duraksamadan; önce 1. kutunun bağımsız görselini üret, hemen peşinden 2. kutunun bağımsız görselini üret, ardından sıradaki diğer tüm kutuları tek tek, art arda kendin oluştur ve tamamla.
- Her kutu kendi başına tam bağımsız bir çıktı olmalıdır.

GÖRSEL STANDARTLARI:
- ORAN: Her görsel mutlaka bağımsız 4:3 en-boy oranında olmalıdır.
- STİL: Dersin konusuna uygun modern vektörel infografik, şema ve minimalist illüstrasyon tarzında; ferah parşömen arka plan. Dersin tema rengi ve altın sarısı tonları hâkim olsun.
- METİN DİSİPLİNİ: Sade ve okunaklı olsun. Asla uzun cümle yazma; yalnızca 1-3 kelimelik net başlıklar, kavram kutucukları ve akış okları kullan.
- HÜRMET & MAHREMİYET: İslâmî ilimler vakarına uygun olsun; mahrem veya uygunsuz tasvir yapma.
- TESLİM: Sen PDF'e ekleme yapma; bana yalnızca bağımsız 4:3 görselleri peş peşe oluşturup teslim et.
```

#### F) Sayfa Yerleşimi ve Metin Akışı (Float Metin Sarmalama Düzeni):
- Görsel kutusu (`add_block_gorsel`), rijit 2 sütunlu grid yerine `float: right` ile sağa yaslanır.
- Metin başlığı ve ilk maddeler görselin solunda akarken, görselin bittiği hizada sonraki maddeler görselin altındaki boşluğa taşarak sayfanın tam genişliğine (`100%`) yayılır.
- Böylece görselin altında atıl/ölü boşluk kalmaz ve sayfa alanı en yüksek verimle kullanılır.
- **Görsel Yanı Kutularında BFC ve Taşma Önleme Standardı (`display: flow-root;`):** Sağa yaslanan görsel kutusunun yanındaki nass (`.k-nass`) veya açıklama kutularının (`.k-subitem`) görsel çerçevesinin arkasına/içine taşmasını engellemek için, CSS'te `display: flow-root;` kuralı zorunludur. Bu sayede kutu görselin sol sınırında temizce sonlanır; görsel altına inen maddeler ise otomatikman %100 genişliğe açılır.

#### G) Görselleri Yapay Zekâ Asistanının Üretmemesi & Şema Promptu Açıklık Standardı:
- **Asistan Görsel Üretmez & Harici Anahtar Bulundurmaz:** Asistan görsel üretiminde kesinlikle hiçbir harici API (fal.ai vb.) çalıştırmaz veya görsel üretimi yapmaz. Sistemde veya ortamda harici görsel üretim anahtarları (fal.ai vb.) tutulmaz ve kullanılmaz.
- **Boş Çerçeve ve Şema Promptu Hazırlama (`image=None`):** Asistan yalnızca görsel ekleme kutularını (`add_block_gorsel(BulletBlock(...), baslik="...", image=None)`) 4:3 oranında yerleştirir ve kutunun `baslik` parametresine konuya tam uygun pedagojik infografik/şema prompt yönergesini yazar. Görsellerin üretimini kullanıcı bağımsız olarak kendisi üstlenir.
- **Tüm Görsel Türlerinde Yüksek Açıklık ve Ayrıntı Standardı (Pedagojik Matris Entegrasyonu):**
  Kullanıcının paylaştığı örnekler görsel türünü iki şablonla sınırlamaz; **Pedagojik Görsel Matrisindeki tüm çeşitlerin (11 temel şablon + özgün türler)** promptlarının yapay zekâya aktarılırken taşıması gereken **kristal netlikteki ayrıntı derinliğini** belirler:
  1. **Şema/Görsel Türünün Açıkça Belirtilmesi:** Rastgele bir başlık yerine matristeki somut tür adıyla başlar (örn. `İnfografik Harita`, `Kronolojik Zaman Çizelgesi`, `Hüküm Karar Ağacı`, `İsnad Ağacı`, `İki Kutuplu Karşılaştırma Şeması`, `Silsile & İlim Ağacı`, `Kavram Şeması`, `Döngüsel Süreç Modeli`, `Hiyerarşik Değerler Piramidi` vb.).
  2. **Yapısal ve Semantik Bileşenlerin Somut Dökümü:** Kompozisyondaki sol/sağ sütunlar, basamaklar, dallar, zıtlık okları, aktörler veya noktalı virgülle (` ; `) ayrılmış kilit kavram kümeleri açıkça yazılır; yapay zekânın kompozisyonda neyi nereye koyacağı tartışmaya yer bırakmayacak netlikte tanımlanır.
  3. **Biçimsel ve Renk Parametreleri:** Prompt içerisinde `4:3 en-boy oranı` açıkça zikredilir; gerekli durumlarda dersin kurumsal tema rengi ve altın sarısı vurgu tonu eklenir.
  *(Örnek 1 - Karşılaştırma Matrisi: `ŞEMA PROMPTU (4:3): İLİM VE MARİFET / İRFAN DİKOTOMİ MATRİSİ — Sol sütun İlim (Tafsilatlı, Ezelî/Hâdis, Zıddı Cehl, Esmâ: Âlim). Sağ sütun Marifet (Tanımak, Yalnızca Kesbî, Zıddı İnkâr, Esmâ: Ârif Denilmez). Ortada zıtlık ve bağ okları. Vurgu rengi erguvan moru (#592F79) ve altın sarısı.`)*
  *(Örnek 2 - Coğrafi / Tarihî İnfografik: `İnfografik Şema: Kadim Nehir Havzaları ve Kur'anî Atlas (Mezopotamya / Cezîre Dicle-Fırat ve Mısır Nil havzaları; Hz. İbrahim, Hz. Nûh, Hz. Yûnus ve Hz. Mûsâ; 4:3 en-boy oranı)`)*
  *(Örnek 3 - Karar Ağacı: `Hüküm Karar Ağacı: Şartlar, Rükünler ve Butlan Dalları (Girdi: Akit İradesi; Dallanma: Sıhhat Şartları Tam → Sahih / Rükün Eksik → Bâtıl / Vasıf Bozuk → Fâsid; 4:3 en-boy oranı)`)*
  *(Örnek 4 - İsnad Zinciri: `İsnad Ağacı Şeması (4:3): Medârü'l-Hadîs Kavşağı ve Tarîkler — Zührî kavşağı; yukarıda 3 talebe (Mâlik, Süfyân, Ma'mer); aşağıda sahâbî Enes b. Mâlik; âlî ve nâzil isnad kolları. Vurgu rengi deri cilt (#664324) ve altın sarısı.`)*
- **Tipografik ve Görsel Kutu Mizanpajı:**
  - Prompt başlığı (`.gk-baslik`): `"DejaVu Serif", serif` fontlu, kalın (`font-weight: 700`), ortalanmış, dersin koyu aksan renginde (`var(--accent-dark)`), dış çerçevesiz ve arka plan şeritsiz olarak kutunun hemen üzerinde yer alır.
  - Görsel alanı (`.gk-alan`): `aspect-ratio: 4 / 3;`, `border: 1px solid var(--line);`, `border-radius: 8px;`, `background: var(--paper);`, `box-shadow: var(--shadow-sm);` özelliklerinde şık, parşömen zeminli boş çerçevedir.
- **Görsel Bağlama:** Kullanıcı görselleri ilgili dersin `görseller/` klasörüne ekleyip açıkça bağlanmasını istediğinde `image=_foto("<dosya>.jpg")` ve `baslik=""` yapılarak bağlanır. Asistan kendiliğinden görsel üretip bağlamaz.


---

## KRİTİK KURAL 9: Arap Dili ve Edebiyatı Görsel Ders Notu Üretim Standartları (Bütünleşik Model)

Arap Dili ve Edebiyatı dersleri üretilirken veya güncellenirken aşağıdaki kurallar İSTİSNASIZ uygulanacaktır:

1. **Açılış Kelime Fihristi Mimarisi (`_vocab_section` & `_vcard`):**
   - Kitap başındaki yeni kelimeler (örn. s. 23 fihristi) kuru metin veya basit maddeler olarak bırakılamaz (`sade kalma yasağı`).
   - Kelimeler tematik gruplara ayrılarak (`Askerî ve Ahlâkî`, `Edebî ve Gramatikal`, `Savaş`, `Ecel ve Hikmet`), 4 sütunlu estetik kelime kartları (`.vocab-grid-4`, `.v-card`) halinde tanzim edilir.
   - Her kartta Arapça kelime iri/harekeli ve ders renginde (`#8C2F21`), sağ üstte sarf/vezin/tekil-çoğul hap rozeti (`.v-card-tag`), altta Türkçe karşılığı verilir.
2. **Kelime Kelime Satır Altı (Interlinear) Çeviri ve Metin Düzeni:**
   - Kitaptaki tüm metinler, şiirler, dipnotlar ve alıştırmalar `_w(ar, tr)` interlinear belirteçleriyle kelime kelime çevrilir.
   - Ana metinler `_board` (çift sütunlu levha), alıştırmalar ve diyaloglar `_box` (satır altı kutusu) ile sunulur.
   - Alıştırma kutularında ders rengi (`#8C2F21`) ve altın aksan (`#c49a45`) esastır. Farklı rastgele renkler kullanılmaz.
3. **Alıştırma Boşluklarında Düz Çizgili Vurgu:**
   - Boşluk doldurma hedeflerinde dalgalı çizgi (`underline wavy`) yerine kurumsal renkte düz alt çizgi (`text-decoration: underline solid #8C2F21 !important;`) kullanılır.
4. **Pedagojik Görsel Matrisi ve Çeşitlilik Kuralı:**
   - Her bölümün görseli konunun pedagojik yapısına özel üretilir. Birbiri ardına gelen bölümlerde aynı şablon (örn. iki adet yatay süreç oku) tekrar edilmez; aktör üçgeni, kavram şeması, karar ağacı, mukayese matrisi vb. pedagojik çeşitlilik korunur.
5. **Sayfa Verimliliği & 0 mm Taşma:**
   - Tüm sayfalar %90–100 dolulukta tutulur, `build.py` taşma denetiminde `0 mm taşma` şartı aranır.

---

## KRİTİK KURAL 10: Arapça Nass ve İbare Geçen Tüm Derslerde Bütünleşik ve İnterlinear Mimari Standardı

Bu kural; nass odaklı olan **Arap Dili ve Edebiyatı**, **Hadis**, **Tefsir** dersleri başta olmak üzere, **içerisinde âyet, hadis, fıkhî kaide, kelâmî delil veya klasik metin gibi Arapça ibare geçen TÜM DERSLERDE (Fıkıh, Kelâm, İslâm Felsefesi, Tasavvuf vb.) İSTİSNASIZ ZORUNLUDUR**. Bu derslerde kuru özet veya satır atlamalı anlatım kesinlikle yasaktır; aşağıdaki 7 temel prensip eksiksiz uygulanır:

1. **Kelime Kelime Satır Altı (Interlinear) Anlatım Standardı (`_w(ar, tr)`):**
   - Ayetler, hadisler, senedler, terceme-i bâblar, şiirler ve klasik ibareler kuru metin olarak bırakılamaz.
   - Her nass öbeği kelime kelime satır altı belirteçleriyle (`_w(ar, tr)`) tanzim edilir.
   - Kelime kelime çevirinin hemen altına/yanına akıcı toplu Türkçe meal/anlam eklenir. Bu üslup kesinlikle korunur ve kaldırılmaz.

2. **Kitap Bütünlüğü ve Kronolojik Akış (Besmeleden İtibaren Eksiksiz İbareler):**
   - Kaynak kitapta veya derste yer alan metin sırası birebir takip edilir.
   - İlk sayfadaki Besmele, terceme-i bâb (bölüm başlığı), nasslar ve şerhler eksiksiz Arapça lafızlarıyla yer alır. Metinden ibare atlanamaz.
   - İlgili ayetlerin hangi sûre ve âyet numarası olduğu Arapça ibarenin hemen altına/yanına metin akışı içinde işlenir.

3. **Çoklu İsnad Kanalları ve Tahlil Mimarisi (`[الإِسْنَادُ ١]`, `[الإِسْنَادُ ٢]`, `[الإِسْنَادُ ٣]`):**
   - Bir hadisin 2 veya 3 farklı isnad kanalı (mütâbaat, ta'lîkāt, farklı tarîkler) varsa, bunlar Arapça metnin tam başında kristal netliğinde ayrılır:
     - Arapça lafızların önünde `[الإِسْنَادُ ١]`, `[الإِسْنَادُ ٢]`, `[الإِسْنَادُ ٣]` rozet ve belirteçleri kullanılır.
     - Türkçe açıklamada her isnadın kaçıncı kanal olduğu ve ravilerin silsilesi açıkça numaralandırılarak karşılaştırılır.
     - **Tüm Çoklu Senedlerde Râvi Hüviyet Kartı Zorunluluğu:** Yalnızca ana senedde değil, ta'lîk ve mütâbaat gibi ikincil/üçüncül tüm kanallarda da her râvi müstakil hüviyet kartıyla (`_isnad_token`) tanzim edilir. Kuru kelime listesiyle bırakılamaz.

4. **İsnadın Hadisin Üstünde Yer Alması ve Bütünleşik Râvi Analizi (`.isnad-token` & `.isnad-subdesc`):**
   - İsnad zinciri daima hadis metninin (metn-i hadîs) hemen üstünde yer alır.
   - Senetteki her bir râvi müstakil bir kartta (`.isnad-token`): Arapça adı, Türkçe okunuşu, râvi tabakası/sıfatı, hadisin sıhhat rozeti (`Mevkūf Râvi`, `Maktû Ta'lîk`, `MERFÛ NASS`, `MEDÂRÜ'L-İSNÂD`, `Tahdîs`, `İhbâr`, `An'ane`) ve rozetin hemen altında tahmîl sîgasının Türkçe anlamı (`.isnad-subdesc`: *Doğrudan İşitme*, *Bizzat Semâ*, *Hocaya Arz/Okuma*, *«...den» Nakil*, *Kavşak Râvi*, *Sahâbî Rivayeti*, *Nebevî Nass*) ile eksiksiz gösterilir.
   - **Bölüm Sonu İsnad Usûlü Rehberi:** Hadis isnadlarının başladığı bölümlerin sonunda veya ilgili odak kutularında sened ıstılahlarının (Mevsûl Tahdîs, İhbâr, An'ane, Medâr, Mevkûf, Merfû, Maktû) sınav ve usûl odaklı analitik izahı zorunlu olarak verilir.

5. **Prestijli Bâb Başlığı ve Nass Levhaları (`.bab-board`, `.bab-badge`):**
   - Buhârî'nin fıkhî ictihadını yansıtan **Tercemetü'l-Bâb** bölümlerine özel altın sarısı degrade rozetler (`.bab-badge`) ve sıcak parşömen kart tasarımı uygulanır; **«BÂB TERCÜMESİ»** ve **«USÛL & İSTİNBAT»** kurumsal hap rozetleriyle nass ve fıkhî istinbat birbirinden net şekilde ayrılır.

6. **Sistem Tasarımıyla %100 Bütünlük (Yerel Tema Değişkenleri):**
   - Kelime kelime levhalar ve kutular sistemin yerel tasarım kimliğiyle (`var(--accent)`, `var(--accent-tint)`, `var(--line)`, `var(--gold)`, `var(--paper)`) tam uyumlu olmalıdır.
   - Gözü yoran yapay, yabancı veya aşırı kontrastlı bordürler yerine sistemin `.k-badge`, `.k-nass` ve `.k-subitem` estetiği kullanılır; görsel bir bütünlük sağlanır.

7. **Pedagojik Görsel ve Karar Ağaçları:**
   - Hadislerin isnad ağaçları (medârü'l-hadîs), tefsir rivayet-dirayet şemaları ve nahiv/sarf karar ağaçları konuya özel pedagojik görsel matrisine uygun olarak hazırlanır.

8. **Sayfa Verimliliği & 0 mm Taşma:**
   - Yoğun nass, râvi kartları ve satır altı çevirilerin yer aldığı sayfalar titizlikle dengelenir; %90–100 doluluk ve `build.py` taşma denetiminde `0 mm taşma` şartı aranır.

---

## Sistemin amacı

Üniversite derslerinin ham metin özetlerini (5-25 sayfalık PDF'ler) alıp tasarım
açısından zengin, sınava hazırlık odaklı "Görsel Ders Notu Kitabı" formatına çeviren
bir üretim hattı: kapak, içindekiler, genel bakış, numaralı bölümler (terim kutuları,
kişi kartları, karşılaştırma tabloları, akış şemaları, vurgu kutuları, bölüm
özetleri), kavramlar sözlüğü ve 20 soruluk çoktan seçmeli test + çözümlü cevap
anahtarı.

**Tasarım sabittir — değiştirme, sadece içerik ekle.** Kullanıcı tasarımda bir sorun
bildirirse (kesilme, kontrast, taşma) `templates/style.css` veya
`templates/_ders_govde.html.j2` üzerinde kalıcı düzeltme yap; bu dosyalar TÜM
derslerde paylaşılır. Önce `docs/TUZAKLAR.md`'yi oku.

(`master.html.j2` artık 13 satırlık bir sarmalayıcıdır; bir dersin gerçek sayfa yapısı
`_ders_govde.html.j2` içindedir ve tek ders PDF'i ile birleşik kitap ONU ortak
kullanır — düzeltmeyi oraya yapınca her iki çıktı birden düzelir.)

## Çıktı formatı (özet)

A4 dikey (210 × 297 mm), bleed YOK, **RGB** — fotokopi için. Kenarlar üst 12 / alt 15 /
iç 12 / dış 12 mm (simetrik), metin alanı 186 × 270 mm, gövde 9,6 pt. Matbaa için
`--cmyk` bayrağı var (varsayılan kapalı; Ghostscript yoksa build DURMAZ, uyarı basıp
RGB bırakır). Kenarları daha da daraltmayın: fotokopi makineleri kağıt kenarından
~5 mm basamaz. Ayrıntı ve gerekçe: `docs/OLCUMLER.md`.

**Üretilen belgelerdeki ürün etiketi "Ders Notu"dur, "Görsel Ders Notu" DEĞİL**
(2026-09-10 kullanıcı kararı). Ders kapağı kicker'ı "Ders Notu Kitabı · <Sınav> Özeti",
birleşik kitap kicker'ı "Ders Notu Kitabı · Dönem Cildi" yazar. Sistemin/komutun/
skill'in adı ("görsel ders notu üretim sistemi", "görsel ders notu oluştur") ve
kod içi teknik terimler ("görsel kutusu", "görsel dil") AYNEN kalır — değişen yalnız
son kullanıcının gördüğü belge metnidir. Kaynak: `templates/_ders_govde.html.j2`
cover-kicker + `cekirdek/content_model.py` `cover_kicker` varsayılanı. Yeni bir
`src/kitap.py` yazarken `cover_kicker`/`imprint` metinlerine "görsel" KOYMA.

---

## Klasör yapısı: sınıf / dönem / sınav / DERS

```
<sinif>-sinif/<donem>-donem/<sinav>/
├── kaynaklar/
│   ├── ders_kaynaklari/<DERS ADI>/     # GİRDİ: ham ders metni / kaynak PDF
│   ├── ogretmen_notlari/<DERS ADI>/    # GİRDİ: öğretmenin dağınık dikte notu
│   └── özetlenmiş_dersler/<DERS ADI>/  # ARA:   yukarıdakilerden çıkarılan YAZILI özet
├── src/                                # <ders_slug>.py içerik modülleri + kitap.py
├── gorsel_ders_notlari/                # ÇIKTI: <DERS ADI>/*.pdf + kökte birleşik kitap
├── calisma_rehberleri/<DERS ADI>/      # ÇIKTI: ders-anlatim skill'i Mod 2
└── ders_anlatimlari/<DERS ADI>/        # ÇIKTI: ders-anlatim skill'i Mod 1
```

`<sinif>` ∈ {2, 3} · `<donem>` ∈ {1, 2} · `<sinav>` ∈ {vize, final} — 8 dönem
klasörünün hepsi mevcut. Şu an **yalnızca `2-sinif/2-donem/final/` doludur** (11 ders).

**Paylaşılan altyapı** (döneme ait DEĞİL, asla kopyalanmaz):
`build.py` · `build_kitap.py` · `cekirdek/` · `templates/` · `tools/` · `assets/`

Bunlarda bir düzeltme yaparsan **her sınıfın her dönemini** etkilersin — bu kasıtlıdır
(tasarım tek kaynaktır), ama dönem-özel bir "düzeltme" yapmaya çalışma.

`cekirdek/` bir kütüphanedir, doğrudan çalıştırılmaz: `donem.py` (sınıf/dönem/sınav
çözümleyici) · `content_model.py` (veri şeması) · `theme_engine.py` (renk teması
motoru) · `renk_uretici.py` (derse özel vurgu rengi) · `pdfx.py` (baskı öncesi).

### `ders_klasoru` — her yeni derste ZORUNLU

`CoursePack`'e ders programındaki **BÜYÜK HARFLİ tam adı** yazın:

```python
return CoursePack(
    ders_klasoru="SİSTEMATİK KELAM I",   # <- kaynaklar/ altındakiyle BİREBİR aynı
    course_code="SİST. KELAM I",
    ...
)
```

Boş bırakılırsa build.py başlık slug'ına düşer (`kelâm-tarihi/` gibi) — bu sadece
geriye dönük uyumluluk içindir ve klasör adının `kaynaklar/` altındakiyle
eşleşmemesine yol açar. **Yeni derste her zaman doldurun.**

### DÜZ KİP (`dersler/`) — sınıf ağacı olmayan kurulumlar

Bu depo GitHub'da yalnızca boş bir `dersler/` iskeletiyle yayımlanır; sınıf ağaçları
`.gitignore`'dadır ve klonlayan kişide hiç bulunmaz. `cekirdek/donem.py` bunu algılar:
sınıf ağacı diskte YOKSA ve dönem verilmediyse kendiliğinden `dersler/` köküne geçer
ve bunu konsola yazar. `--duz` bayrağı her koşulda `dersler/` kullandırır. Sınıf ağacı
VARSA (bu makinede var) hiçbir şey değişmez, dönem yine sorulur.

**Bayrağın adı `--duz`, `--dersler` DEĞİL** — `tools/olcum.py`, `tools/dengele.py` ve
`tools/kalibre.py`'de `dersler` adında KONUMSAL bir argüman (ölçülecek ders listesi)
zaten var; aynı adı kullanmak argparse `dest`'ini ezip o üç aracı bozuyor.

`dersler/src/ornek_ders.py` yayımlanan tek ders modülüdür ve kurulum doğrulaması
olarak kullanılır.

### AÇIK ÖĞRETİM LİSESİ (AÖL) KİPİ (`acik-ogretim-lisesi/`)

Üniversite derslerinden bağımsız Açık Öğretim Lisesi üretim hattı:

```
acik-ogretim-lisesi/<donem>/
├── kaynaklar/
│   ├── ders_kaynaklari/<DERS ADI>/     # GİRDİ: MEB resmi ders kitabı (PDF)
│   └── özetlenmiş_dersler/<DERS ADI>/  # ARA:   kazanım odaklı yazılı özet
├── src/                                # <ders>.py modülleri + kitap.py
└── gorsel_ders_notlari/<DERS ADI>/     # ÇIKTI: tekil ders PDF'i + kökte birleşik kitap
```

**Önemli Kurallar:**
1. **Yalın Yapı:** Gereksiz ara katmanlar (sınav klasörü, öğretmen notları, ders anlatımları) yoktur; doğrudan `<donem>/` altında `kaynaklar/`, `src/` ve `gorsel_ders_notlari/` bulunur.
2. **Ders Yeniden Kullanımı (Dönemler Arası Paylaşım):** Bir ders bir dönemde (ör. `2026-1`) üretildikten sonra öğrenci o dersi sonraki dönemde (ör. `2026-2`) tekrar alıyorsa, dersi sıfırdan yeniden üretme; mevcut ders modülünü doğrudan yeni dönemin `kitap.py` dosyasına dahil et.
3. **Komutlar:**
   ```bash
   python build.py <ders_slug> --aol --donem 2026-1
   python build_kitap.py --aol --donem 2026-1
   ```
4. **4 Seçenekli Test:** MEB Açık Öğretim Lisesi sınav formatında testler 4 seçeneklidir (A, B, C, D).

### Çıktılar ve kaynaklar git'e GİRMEZ

`gorsel_ders_notlari/`, `calisma_rehberleri/`, `ders_anlatimlari/` ve `kaynaklar/`
`.gitignore`'dadır — depoda yalnızca `.gitkeep` iskeleti durur. Bir ders ürettikten
sonra PDF'i commit etmeye ÇALIŞMA; git onu zaten yok sayar.

Sebep: bir dersin gerçek içeriği `src/<ders>.py` modülüdür, PDF ondan her zaman
yeniden üretilebilir. PDF ikili olduğu için git sıkıştıramaz; her yeniden derleme
depoya tam bir kopya daha eklerdi (bu depo bir kez 345 MB'a çıkmıştı, %98,5'i çıktıydı).

- Bir ders "kayboldu" diye endişelenme — `src/<ders>.py` duruyorsa
  `python build.py <slug> --sinif X --donem Y --sinav Z` onu geri getirir.
- `kaynaklar/` altındaki ham materyal koddan ÜRETİLEMEZ ve git'te yedeği YOKTUR.
  Kullanıcıya bu dosyaları silmesini/taşımasını önerme.
- Yeni bir çıktı türü eklersen (`.docx` gibi) `.gitignore` kuralını da ekle; kurallar
  UZANTI bazlıdır, klasör bazlı değil (yoksa `.gitkeep` iskeleti de yok sayılır).

### Ders modülleri neden noktalı yolla import edilmiyor?

`2-sinif` geçerli bir Python paket adı değildir, bu yüzden eski `content.kelam_tarihi`
biçimi kullanılamaz. `cekirdek/donem.py` seçilen dönemin `src/`'sini `sys.path`'in
başına koyar ve modül **çıplak adıyla** (`kelam_tarihi`) import edilir. Eski noktalı
yazım yine kabul edilir (önek atılır), ama yeni kodda çıplak ad kullan.

Bir `src/*.py` dosyasının başındaki

```python
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
```

satırı **proje köküne** çıkar: `src/ -> <sinav> -> <donem> -> <sinif> -> KÖK` = 4
seviye. Düz kipte (`dersler/src/`) bu sayı **2**'dir. Yanlış sayarsan `cekirdek`
paketi bulunamaz. Veri şeması hep `from cekirdek.content_model import ...` ile gelir.

---

## Haftalık ders akışı (dönem boyunca biriken katman)

Her ders haftada bir işlenir. Kullanıcı ders çıkışında o hafta işlenen materyali —
**işlenen kitap bölümü/sayfaları/slaytları VE kendi ders notları (foto/metin)
birlikte** — yükler ve **o içeriğin kendisine anlatılmasını** ister. Senin işin, o
haftanın öğrenme belgesini üretmek (aşağıda). Bu, dönem başındaki müfredat paketinin
ve (belliyse) tam kitabın **üstüne** biriken bir katmandır; onların yerine geçmez.

### Haftalık materyal nereye konur

Kullanıcı "1. hafta", "bu hafta" vb. diyerek dosya verdiğinde:

```
<D>/kaynaklar/ders_kaynaklari/<DERS ADI>/
├── <ders> MÜFREDAT BİLGİ PAKETİ.pdf      # dönem başı (varsa)
├── <tam kitap ...>.pdf                    # kitap belli olunca (varsa)
├── 01-hafta/                              # o haftanın ham materyali
│   ├── kitap/    → işlenen bölüm / sayfalar
│   └── notlar/   → kullanıcının kendi ders notları
├── 02-hafta/
└── ...
```

- Klasör adı **`NN-hafta`** — iki haneli, sıfır dolgulu (`01`..`14`) ki dosya sistemi
  doğru sıralasın. Klasör yoksa sen aç.
- `kitap/` ve `notlar/` alt ayrımı **önerilir ama zorunlu değil**; kullanıcı karışık
  attıysa tek klasörde bırak, içerikten ayırt et.
- Bir dersin haftalık materyalini **başka dersin veya başka haftanın** klasörüne KOYMA.
- Hangi hafta olduğu belirsizse SOR; tahminle numaralandırma. Aynı hafta klasörüne
  sonradan ek dosya gelebilir (üstüne yaz değil, yanına ekle).

### Derse özel yöntem dosyası: `00-YONTEM.md`

Bir dersin `<D>/kaynaklar/özetlenmiş_dersler/<DERS ADI>/` klasöründe **`00-YONTEM.md`**
varsa, o ders için haftalık belge veya sınav özeti üretmeden ÖNCE onu baştan sona OKU.
Orası dersin kendi üretim talimatıdır: kaynağın nasıl okunacağı, ünite/hafta eşlemesi,
o derse özel belge katmanları, çözülmemiş belirsizlikler. **Çelişirse `00-YONTEM.md`
kazanır** (yalnız o ders için); buradaki genel akış onun üstüne binmez, altına serilir.

Neden var: bu dosyalar farklı AI araçlarıyla çalışıldığında bile haftalar arasında
biçim/derinlik farkı oluşmasın diye yazılır. Dosya varsa formatı kendi kafana göre
"iyileştirme" — aynen uygula; gerçekten değişmesi gerekiyorsa önce dosyayı güncelle,
sonuna "Değişiklik kaydı" satırı düş, sonra üret.

Yeni bir ders bu formatta ilerleyecekse (özellikle **metin tahlili / dil dersleri**
gibi standart "bölüm özeti" kalıbının yetmediği dersler) ilk haftayla birlikte bir
`00-YONTEM.md` de yaz. İçinde en az şunlar bulunmalı: kaynağın kimliği ve okunma
yöntemi (taranmışsa render DPI'ı ve sayfa ofseti) · ünite↔hafta eşleme tablosu ·
sınav kapsamı · haftalık belgenin zorunlu katmanları · yasaklar · kontrol listesi.
Örnek: `3-sinif/1-donem/vize/kaynaklar/özetlenmiş_dersler/ARAP DİLİ VE EDEBİYATI V/00-YONTEM.md`.

**Bu dosyalar `kaynaklar/` altında olduğu için git'e GİRMEZ** — tek kopyadır, silme.

### Her hafta yüklemesinden sonra: haftalık çalışma belgesi

`<D>/kaynaklar/özetlenmiş_dersler/<DERS ADI>/NN-hafta/<slug>-NN-hafta.md`
(kullanıcı isterse ayrıca `.pdf` — basit md→pdf).

Kullanıcı ders çıkışında o haftanın 30–50 sayfalık kitap bölümünü / slaytını + kendi
notunu atar ve **o materyalin KENDİSİNE anlatılmasını** bekler. Yani haftalık belge
bir "log" değil, **o haftanın öğrenme belgesidir** — dersin devamsız gelinmiş gibi
tek başına çalışılabilir olmalı.

Belgenin iki kısmı var:

**A) Ders takip başlığı** (kısa, belgenin başında):
1. **Kapsam kaydı:** Bu hafta kitabın hangi bölümü / hangi başlıkları işlendi (sayfa
   aralığıyla). Atlanan/hızlı geçilen yerler. Bir sonraki hafta ne olacağı.
2. **Hocanın vurgusu:** Derste özellikle üstünde durulan noktalar.
3. **Sınav sinyalleri:** "Bu çıkar", "not alın", "önemli" gibi açık işaretler.
4. **Kullanıcının kendi notundaki** soru / karışıklık — belgede cevaplanır, gerekiyorsa
   "hocaya teyit ettir" notu düşülür.

**B) Anlatım gövdesi** (belgenin ASIL kısmı):
- İşlenen içeriği **bölüm bölüm, derinlemesine ANLAT** — tanımlar, bağlamlar, örnekler,
  neden-sonuç. Kaynağı özetleyip geçme; öğreten bir metin yaz.
- **Uzunluk materyale göredir, sabit değil.** 30–50 sayfalık bir bölüm için tipik olarak
  6–15 sayfalık bir anlatım çıkar. "1–2 sayfa" HEDEF DEĞİL — yalnızca giriş/tanışma
  dersi gibi gerçekten az materyal olan haftalarda kısa olması normaldir.
- Derste geçip kitapta olmayan ek bilgi/örnekleri anlatımın içine yerleştir, ama
  "(derste hoca ekledi)" gibi işaretle.
- Kavram yoğun yerlerde tablo, karşılaştırma, kısa madde listesi kullan; kuru duvar
  metin yazma.
- **İçerik UYDURMA:** yalnızca yüklenen materyalde (kitap + not) olan. Materyal
  gelmeyen haftayı ATLA; eksikliği ilgili sınav özeti hazırlanırken belirt.
- Bu, `ders-anlatim` skill'inin felsefesiyle (kesintisiz, kısaltmasız derinlemesine
  anlatım) aynıdır; sadece çıktı yeri farklı (`özetlenmiş_dersler/<DERS>/NN-hafta/`)
  ve başına "ders takip" bölümü eklenir.

### Sınav (vize/final) özeti ve görsel ders notu — haftalık belgelerle

Sınav zamanı geldiğinde (KRİTİK KURAL 2: dönem/hafta kapsamı yine SORULUR):

- **ANA KAYNAK = kitabın ilgili bölümleri** (varsa) + **haftalık çalışma belgeleri**.
  Haftalık belgeler zaten o haftanın anlatımını içerdiği için sınav özetinin
  gövdesi büyük ölçüde onlardan derlenir; kitap, boşlukları doldurmak ve yapıyı
  doğrulamak için kullanılır.
- **Haftalık belgeler iki işi görür:**
  - **Kapsam süzgeci:** Sınav özetine SADECE haftalık belgelerde "işlendi" diye geçen
    bölümleri al. Kitapta olup derste işlenmeyen kısmı DAHİL ETME.
  - **Vurgu katmanı:** Hocanın vurguladığı yerleri öne çıkar; sınav sinyallerini
    `Callout` (`focus`) veya özel not olarak işaretle.
- Sınav özeti, haftalık belgelerin **damıtılmış** hâlidir (14 hafta × 10 sayfa = tek
  tek okunmaz); ama haftalık belgelerdeki hiçbir vurgu/sınav sinyali kaybolmamalı.
- Kitap hiç yüklenmediyse: haftalık belgelerin birleşimi + müfredat iskeleti ile üret;
  kullanıcıya "kitap gelince gözden geçirilecek" olduğunu bildir.

---

## Uçtan uca iş akışı

### 0. Dönemi belirle, sonra kaynağı bul

**Önce dönem** (KRİTİK KURAL 2). Bundan sonraki her komutta
`--sinif X --donem Y --sinav Z`; dönemin kökünü `<D>` diye anacağız:

```
<D> = <sinif>-sinif/<donem>-donem/<sinav>
```

Kullanıcı dosya eklemeden sadece ders adı söylerse, **sormadan önce** o dönemin girdi
klasörlerini tara:

```bash
ls "<D>/kaynaklar/ders_kaynaklari/"
ls "<D>/kaynaklar/ogretmen_notlari/"
ls "<D>/kaynaklar/özetlenmiş_dersler/"
```

Ders adıyla eşleşen (esnek eşleştir — büyük/küçük harf, Türkçe karakter,
"-özet"/"-ozet" ekleri) bir dosya varsa onu kullan, tekrar sorma. Eşleşen yoksa
**başka dönemlere BAKMA** (yanlış dönemin kaynağını kullanmak sessiz bir hatadır);
kullanıcıdan PDF'i eklemesini ya da doğru dönemin `kaynaklar/ders_kaynaklari/`
klasörüne koymasını iste.

Dersin `özetlenmiş_dersler/<DERS ADI>/` klasöründe **`00-YONTEM.md`** varsa, başka
hiçbir şey yapmadan ÖNCE onu oku — o dersin üretim talimatı odur.

Dersin `<DERS ADI>/` klasöründe **`NN-hafta/` alt klasörleri** varsa: haftalık
akış işliyor demektir (bkz. "Haftalık ders akışı"). Sınav özeti / görsel ders notu
üretirken haftalık çalışma belgeleri + (varsa) kitabı birlikte kullan; belgeler
kapsam süzgeci + vurgu katmanıdır. Kullanıcı sadece "bu haftayı işle / anlat"
diyorsa yeni `NN-hafta/` klasörüne materyali koy, çalışma belgesini üret, sınav
üretimine GEÇME.

İşlenen bir dersin kaynağını bu klasörden SİLME — revizyon istenebilir.

(`ogretmen_notlari/` + `calisma_rehberleri/` + `ders_anlatimlari/` bu görsel PDF
sistemine değil, ayrı çalışan `ders-anlatim` skill'ine aittir — bkz.
`.claude/skills/ders-anlatim/SKILL.md`. Aynı ağacı paylaşırlar, birbirlerini
tetiklemezler.)

### 1. Ham içeriği oku ve Arapça kontrolü yap

```bash
python3 -c "
import pdfplumber
with pdfplumber.open('<D>/kaynaklar/ders_kaynaklari/<dosya>.pdf') as pdf:
    for i, page in enumerate(pdf.pages):
        print(f'=== SAYFA {i+1} ===')
        print(page.extract_text())
"
```

Metnin TAMAMINI oku, kesme. Arapça (ayet, hadis) varsa sorun değil — `add_ayat()`
destekliyor (örnek: `<D>/src/tefsir2.py`).

**Arapça (RTL) metinde pdfplumber'a GÜVENME** — bu tür PDF'lerde Arapçayı harf harf
ters çıkarabilir. Aynı sayfayı PyMuPDF ile de çıkar ve karşılaştır:

```bash
python -c "
import pymupdf, io
d = pymupdf.open('<D>/kaynaklar/ders_kaynaklari/<dosya>.pdf')
out = io.open('cikti.txt','w',encoding='utf-8')   # Windows konsolu Arapça basamaz
for i in range(len(d)): out.write(f'=== SAYFA {i+1} ===\n' + d[i].get_text('text') + '\n')
out.close()"
```

Doğrulama çapası: alıntı içindeki **ayet parçaları** sabit Mushaf metnidir; çıkardığın
metin onlarla birebir örtüşüyorsa yöntem güvenilirdir. Tipik ToUnicode onarımları:
`هللا→الله`, `اْل→الأ`, `اإل→الإ`, `اال→الا`, fatha-lam bağı `→لا`. Bir sayfa satır içi
*döndürülmüş* geliyorsa doğru sırayı `﴿﴾` parantez dengesi ve kaynaktaki Türkçe
çeviriyle kur. Her alıntıyı üretilen PDF üzerinde görsel olarak oku; **emin olamadığın
kısmı EKLEME.**

**Kaynakta Arapça varsa görsel ders notuna da eklenir — transliterasyon TEK BAŞINA
YETMEZ.** Öğretmen notunda/kaynakta bir ayet, hadis veya Arapça ıstılah gerçek Arapça
harflerle yazılıysa ("يَد", "قُلْ هُوَ اللّٰهُ أَحَدٌ" gibi), bunu Latin harfli okunuşa
("Kul hüvallâhu ehad") indirgeyip Arapçasını atlama — ikisini birlikte ver. Kaynak
sadece transliterasyon içeriyorsa (Arapça harf yoksa) uydurma; yalnızca kaynakta
GERÇEKTEN Arapça yazılmış yerler için geçerlidir.

- **Bağımsız bir ayet/hadis kartı** olacaksa (`ChapterPage.add_ayat`) `Ayah(reference,
  arabic, meal, etymology)` kullan — RTL yerleşim ve büyük punto zaten `.ayah-arabic`
  CSS sınıfıyla sağlanır, ekstra işlem gerekmez.
- **Bir bloğun/tablonun/callout'un içine serpiştirilmiş kısa destekleyici alıntılar**
  için (çoğu sıfat/delil cümlesi bu haldedir) tam bir `Ayah` kartı açmak sayfa dengesini
  bozar; bunun yerine Arapçayı **`<bdi>...</bdi>` ile sarıp** transliterasyonun yanına
  parantezle ekle: `"<bdi>لَيْسَ كَمِثْلِهٖ شَيْءٌ</bdi> ('Leyse ke-mislihî şey')"`. `<bdi>`
  (bidirectional isolate) tarayıcının kendi HTML5 elemanıdır; Türkçe cümle içine gömülü
  Arapçanın yön karışıklığı yaşamadan sağdan sola akmasını sağlar, `style.css`'e
  dokunmaya GEREK YOKTUR (gövde fontu zaten `"DejaVu Sans"` — Arapça glif desteği var).
- Bunu değiştirdikten sonra `tools/olcum.py` ile taşma/doluluk kontrolünü tekrarla —
  Arapça ekleme metni uzatır, önceden dengelenmiş bir sayfa yeniden taşabilir.
- **Arapça hiçbir yerde Türkçesiz bırakılmaz** (2026-09-14 kullanıcı kararı). Bu, Arapça
  ekleme kuralının ikiz kardeşidir: Arapçayı atlamak da, Arapçayı karşılıksız bırakmak da
  öğrenmeyi durdurur. Kelime listelerinde ayrı Türkçe sütunu; alıştırma soru/cevaplarında
  Arapçanın altına italik çeviri; şık, kısa öge ve kelime havuzlarında parantez içinde
  inline karşılık. Bir alıştırmanın yalnız cevabını çevirip sorusunu Arapça bırakma.
  Haftalık çalışma belgeleri ve görsel ders notları için aynen geçerlidir.
- Tek tek Arapça ıstılah adları (istitaat, kesb, meşiet gibi) zaten Türkçe teolojik
  yazımda transliterasyonla kullanılır — kaynakta bunlar Arapça harfle yazılmadıysa
  zorla Arapça ekleme; kural yalnızca kaynağın GERÇEKTEN Arapça yazdığı yerler içindir.

### 2. İçeriği 5-7 bölüme planla

Ham metnin doğal başlık yapısını takip et (uydurma bölümleme yapma). Her bölüm için:
4 anahtar terim, en az 1-2 tablo/blok, mümkünse bir callout, her zaman bir bölüm
özeti. Bölüm başına ortalama 2 sayfa hedefle (1-3 kabul edilebilir) — yoğun bölümleri
en baştan 2-3 `ChapterPage`'e böl, tek dev sayfaya sıkıştırmaya çalışma.

Bu planlama sırasında her bölüm için **görsel destek türünü de belirle** — bkz.
"Görsel destek: haritadan kavramsal illüstrasyona" bölümü: sıralı önerme/süreç
zincirleri `FlowDiagram`'a (native, AI gerekmez), somut yer/yapı/eser
`add_block_gorsel` boş kutusuna, tamamen soyut ama görselleştirilebilir kavramsal
ilişkiler ise AI-üretimi görsel kutusuna (öneri metni yazılır, sonra kullanıcının
görseliyle bağlanır) aday olur.

### 3. `<D>/src/<ders_slug>.py` dosyasını yaz

Aşağıdaki API referansına birebir uy. En hızlı yol: mevcut bir dersi
(`2-sinif/2-donem/final/src/sosyoloji.py` iyi bir orta-karmaşıklık örneği) kopyalayıp
değiştirmek. **Şablonu GÜNCEL gruptan seç** — `ogretim_teknolojileri.py` ve
`sanat_tarihi.py` LEGACY formattadır.

Ayrıca:

- **Rengi SEN seçme.** `cekirdek/renk_uretici.py` içindeki `DERS_RENKLERI` tablosu
  hangi dersin hangi rengi alacağını önceden sabitler (ilke: RENK = DERSİN RUHU):

  ```bash
  python cekirdek/renk_uretici.py "TEFSİR III" --sinif 3 --donem 1 --sinav final
  python cekirdek/renk_uretici.py --tablo        # tüm önceden belirlenmiş renkler
  ```

  Çıkan hex'i `theme_color=` alanına **birebir** kopyala. Kendi kafandan seçersen
  görsel kitap ile `ders-anlatim` skill'inin çıktısı farklı renkte olur (skill de aynı
  tablodan okur). Ders tabloda yoksa önce tabloya bir satır ekle (aynı dönemdeki
  hue'lardan en az ~25° uzak bir ton). `theme=` alanı hâlâ zorunludur (body class'ı
  için) ama `theme_color` verildiğinde görsel sonucu etkilemez. Motorun iç işleyişi:
  `docs/TASARIM.md`.
- `icon_text`: kapaktaki amblem harfi. **Tek bir Latin harf** (dersin baş harfi).
  Yunanca/özel semboller büyük puntoda çarpık/tanınmaz görünür.
- `course_code`: üstteki kısa etiket. Başlıkla neredeyse aynı uzunlukta OLMASIN
  ("ÖĞRETİM TEKNOLOJİLERİ" → "ÖĞR. TEKNOLOJİLERİ").
- **Sınav bölümü Test + Cevap Anahtarı'dır** (LEGACY "Sınav Hazırlık" değil):
  20 soruluk çoktan seçmeli test + her soru için çözümlü cevap anahtarı.
  **Test = 2 sayfa (10+10), cevap anahtarı = 1 sayfa** (2026-09: sınav bölümü sıkıştırıldı).
  **Zorluk Dengesi:** 5–6 kolay (%25–30 motivasyon), 8–9 orta (%40–45 kavrama), 5–6 zor/tam sınav
  sorusu (%25–30 öncüllü, çeldiricisi güçlü, metin/ibare analizi).
  **Arapça Kuralı:** Ders Arapça ağırlıklı ise en az 6–10 soru doğrudan Arapça kök/şık veya hibrit
  metin olmalı; cevap anahtarında Türkçe çevirisi (`.ans-trans`) ve kural gerekçesi eksiksiz verilmeli.
  Soru KÖKLERİNİ ve ŞIKLARINI öz ve vurucu yaz: uzun tam-cümle şıklar 10/sayfa düzenini taşırır.
  Bir şık 2 satırı geçiyorsa kısalt. Detaylar: "Test + Cevap Anahtarı" bölümü.
- Vize dersinde `sinav_etiketi="Vize"` yaz (varsayılan "Final"); `subtitle`'a ayrıca
  "— Vize Özeti" ekleme, tekrar olur.

### 4. Derle

```bash
python build.py <ders_slug> --sinif X --donem Y --sinav Z
```

Tek komut şunları yapar: HTML üret → `validate()` (bölüm numaraları ardışık mı, sözlük
referansları geçerli mi, tekrar eden terim var mı, İçindekiler kapasitesi aşıldı mı,
**içerik metinlerinde kapatılmamış HTML etiketi var mı**) → Playwright ile PDF render →
**her sayfanın gerçek render yüksekliğini A4 sınırıyla karşılaştır** → PDF'e gerçek
bookmark/outline ekle → TrimBox/BleedBox yaz → toplam sayfa sayısını ve bitmiş ölçüyü
konsola bas.

### 5. Taşma çıktısını oku — bu adım ASLA atlanmaz

```
[build] Taşma denetimi: tüm sayfalar A4 sınırları içinde. ✓
```

ya da:

```
[TAŞMA UYARISI] N sayfa A4 sınırını aşıyor -- içerik kesiliyor olabilir:
    - Sayfa (fiziksel sıra) X: ~Ymm taşma
```

Taşma varsa **önce `python tools/dengele.py <slug> --sinif X --donem Y --sinav Z`**
çalıştır — her bloğun gerçek yüksekliğini Chromium'da ölçer ve `ChapterPage`
bölünmelerini taşmayacak EN AZ sayfaya, boşluğu sona iterek yeniden dağıtır (blokların
içine ve sırasına dokunmaz, içerik uydurmaz). `--kuru` ile önce raporlatabilirsin.

Elle karar gerekirse sayfayı PNG'ye çevirip görme aracıyla incele, aşırı yüklü
`ChapterPage`'i ikiye (gerekirse üçe) böl, yeniden derle. **"✓" görene kadar tekrarla.**
Asla taşma uyarısını görmezden gelip devam etme — bu, üretilen PDF'in sessizce içerik
kaybettiği anlamına gelir.

*(Neden bu kadar sıkı olduğu — `flex-shrink` kesilmesi: `docs/TUZAKLAR.md` madde 2.)*

### 6. Görsel olarak baştan sona kontrol et

Taşma "✓" demiş olsa bile şunları PNG'ye çevirip (100 DPI yeterli) görme aracıyla tek
tek kontrol et:

- Kapak (amblem, başlık, motif harfi çakışması, **yeni renk doğru mu**)
- İçindekiler (sayfa numaraları doğru mu)
- Genel Bakış
- Her bölümün İLK sayfası (banner subtitle kesiliyor mu)
- En az bir tablo-ağırlıklı sayfa (başlık satırı okunur mu — `docs/TUZAKLAR.md` md. 1)
- Sözlüğün SON sayfası (1-2 kavramlık yalnız bir sayfa kötü görünür)
- Test'in SON sayfası ve Cevap Anahtarı'nın SON sayfası

Otomatik taşma denetimi "içerik kesiliyor mu"yu, görsel kontrol "iyi görünüyor mu"yu
cevaplar — ikisi de gereklidir, biri diğerinin yerini tutmaz.

### 6b. Sayfa denge kontrolü — taşma kadar rutin bir adım

Taşmamak, sayfaların İYİ kullanıldığı anlamına gelmez. İçeriğin erken bitip altında
büyük boş alan kalması ayrı bir kalite sorunudur (kağıt israfı, dağınık okuma).

**Önce `tools/dengele.py`'yi çalıştır**, elle düzeltmeyi yalnızca onun ulaşamadığı
yerlerde yap. `tools/olcum.py` her sayfanın doluluk oranını ve içindeki blokların mm
cinsinden yüksekliğini tablo halinde basar — "hangi bloğu taşısam?" sorusunu tahminle
değil ölçümle cevapla.

**HEDEF: %90-95 doluluk**, bölümlerin/section'ların **DEVAM sayfalarında** — yani o
section'ın sayfa listesinde İLK sırada olmayan VE fiziksel son sayfası da olmayan
sıradan ara sayfalar.

**İSTİSNALAR — bu sayfalarda hedefi ZORLAMA, doğal doluluğunu koru:**
- Bir bölümün/section'ın **SON fiziksel sayfası** (sadece özet kutusu kalmışsa normal)
- **Açılış sayfaları** — her section'ın İLK fiziksel sayfası (Kapak, İçindekiler,
  Genel Bakış dahil)
- **Sözlüğün son sayfası**

**Mekanizma HER ZAMAN "içeriği yeniden dağıt" olmalı**, ASLA "aynı içeriği daha az
yere sıkıştır" değil — `gap`/`margin` küçültmek veya madde aralarını sıkıştırmak
YASAKTIR, tasarım sistemi sabit kalmalı.

1. Devam sayfalarını PNG'ye çevirip tek tek incele, doluluğu gözle tahmin et.
2. %90'ın altındaki her devam sayfası (istisnalar hariç) bir adaydır.
3. AYNI bölümün komşu sayfasından mevcut bir `.add_*()` bloğunu taşı — **asla yeni
   madde/callout/cümle UYDURMA**; "doldurmak" için içerik icat etmek taşma kadar
   ciddi bir hatadır, çünkü kaynakta olmayan bilgi üretmiş olursun. Çoğu zaman
   sayfaları TEK sayfada BİRLEŞTİRMEK gerekir (bir `ChapterPage()` çağrısını tamamen
   kaldırıp içeriğini komşusuna eklemek) — asıl yöntem budur, tek blok taşımak çoğu
   zaman yetmez.
4. Her denemeden sonra yeniden derle ve taşma çıktısını oku. Taşarsa değişikliği geri
   al ve farklı bir birleştirme/dağıtım dene.
5. Hiçbir dağıtım güvenli şekilde %90-95'e ulaştıramıyorsa mevcut boşluk seviyesini
   koru — riskli bir "iyileştirme" iyileştirmemekten kötüdür. Ama çoğu devam sayfası
   gerçekten yeniden dağıtılabilir; "temiz kazanç yok" sonucuna nadiren varmalısın.

### 7. Bookmark/link doğrulaması

```bash
python3 -c "
from pypdf import PdfReader
r = PdfReader('<D>/gorsel_ders_notlari/<DERS ADI>/<slug>.pdf')
for it in r.outline:
    print(it.title, '->', r.get_destination_page_number(it)+1)
annots = r.pages[1].get('/Annots')
print(len(annots), 'link on TOC page')
"
```

Bölüm sayısı + 2 (sözlük + test) kadar TOC linki olmalı. Bu linklerin **tamamı 2.
fiziksel sayfadadır** (İçindekiler tek sayfa — KRİTİK KURAL 4). `r.pages[1]` dışında
bir sayfada TOC linki görürsen kural bozulmuş demektir.

### 8. Teslim et

PDF'i kullanıcının erişebileceği çıktı konumuna kopyala ve sun.

---

## cekirdek/content_model.py API Referansı

```python
from cekirdek.content_model import (
    Person, KeyTerm, Callout, FlowStep, FlowDiagram, ComparisonTable,
    InfoCard, Ayah, BulletBlock, Chapter, ChapterPage, Concept, CoursePack,
    TestQuestion, AnswerItem,               # GÜNCEL sınav formatı — bunları kullan
    QAItem, DistinctionPair, MatchRow,       # LEGACY — yeni derslerde KULLANMA
)
```

- **`Person(id, name, years, tagline, bio, key_work=None, initials=None)`**
  Bir düşünür/kişi kartı. `bio` bir liste ama sadece `bio[0]` render edilir — tek,
  dolu bir paragraf yaz. **Tek kaynak ilkesi**: bir kişinin tarihleri/eserleri sadece
  burada tanımlanır; sözlükte veya eşleştirme tablosunda aynı bilgiyi elle tekrar
  yazma, bu nesneden türet.

- **`KeyTerm(term, definition)`** — bölüm başındaki 4'lü terim kutusu. Her
  `Chapter.key_terms` **tam 4 eleman** içermeli (tasarım 2x2 grid varsayar).

- **`Callout(kind, title, text)`** — `kind` ∈ `"focus"` (sarı/dikkat), `"caution"`
  (mavi/uyarı), `"insight"` (koyu lacivert/içgörü), `"route"` (mor/bölüm rotası).
  `text` içinde `<b>...</b>` kullanılabilir (HTML olarak render edilir).

- **`FlowStep(title, text="")`** / **`FlowDiagram(steps, caption=None)`** — yatay oklu
  süreç şeması. 3-5 adım idealdir; fazlası dar sütunlara sıkışır.

- **`ComparisonTable(caption, headers, rows)`** — `rows`, her biri `len(headers)`
  uzunluğunda string listesi. Hücrelerde `<b>` kullanılabilir. 2 veya 3 sütunlu
  tablolar en iyi sonucu verir.

- **`InfoCard(title, text, badge=None)`** — küçük 2-3'lü kart grid'i
  (`ChapterPage.add_info_cards(başlık, [InfoCard(...), ...])` ile eklenir).

- **`Ayah(reference, arabic, meal, etymology="")`** — bir ayet/hadis kartı. `arabic`
  RTL olarak, DejaVu Sans ile doğru şekillendirmeyle render edilir (Arapça glyph
  desteği bizzat görsel olarak doğrulanmıştır — harfler doğru bitişiyor, harekeler
  doğru yerleşiyor; tereddüt etmeden kullan). Ham Arapça Unicode metnini doğrudan
  `arabic=` alanına yaz, ekstra bir işlem gerekmez.
  `ChapterPage.add_ayat(başlık, [Ayah(...), ...])` ile eklenir; başlık opsiyoneldir
  (`None` verilirse tekrar edilmez). Örnek: `src/tefsir2.py`.

- **`BulletBlock(number, title, bullets, subtitle=None)`** — numaralı alt-başlık +
  madde listesi. Her madde `<b>vurgu</b>` içerebilir. `number` sayfa/bölüm içinde
  SIRALI olmalı (1, 2, 3…); bir blok ikiye bölünürse aynı numarayı kullanma
  (yanıltıcı olur — tek blok gibi görünsün istiyorsan tek `BulletBlock` olarak tut).

- **`ChapterPage(continue_tag=None)`** — bir bölümün TEK fiziksel sayfası.
  Zincirlenebilir `.add_*()` metodları: `add_terms(list[KeyTerm])`,
  `add_person(Person)`, `add_person_row(list[Person])`, `add_block(BulletBlock)`,
  `add_callout(Callout)`, `add_flow(FlowDiagram)`, `add_table(ComparisonTable)`,
  `add_ayat(title, list[Ayah])`, `add_info_cards(title, list[InfoCard])`,
  `add_block_gorsel(BulletBlock, baslik="")`, `add_summary(text)`.
  `continue_tag` artık **render EDİLMEZ** ("N. Bölüm · Devam" rozeti kaldırıldı) —
  vermek ZORUNLU DEĞİL, sadece geriye dönük uyumluluk için kabul ediliyor.
  **`add_summary(text)` içinde `<b>` KULLANMA:** özet kutusu bold'u blok seviyeli,
  büyük harfli bir "anahtar kelime çipi" olarak render eder ve cümleyi satır satır
  böler. Özet düz metin yazılır. (`<b>` yalnızca `Callout.text`, `BulletBlock`
  maddeleri ve `AnswerItem.explanation` içinde güvenli.)

- **`Chapter(number, title, subtitle, pages=[], key_terms=[])`** — `pages` listesine
  `ChapterPage` nesnelerini sırayla ekle. `key_terms` hem ilk sayfadaki 4'lü kutunun
  hem de `concept_count()` gibi otomatik sayımların kaynağıdır.

- **`Concept(term, definition, context, chapter_ref)`** — sözlük satırı. `chapter_ref`,
  gerçek bir `Chapter.number`'a eşit tam sayı olmalı (`validate()` denetler).

- **`TestQuestion(number, stem, options)`** — `options` tam olarak
  `{"A": "...", "B": "...", "C": "...", "D": "...", "E": "..."}` biçiminde bir dict
  (4 veya 5 seçenek; `validate()` denetler). `number` 1'den başlayıp ardışık artmalı
  ve karşılık gelen `AnswerItem.number` ile birebir eşleşmeli.

- **`AnswerItem(number, correct, explanation)`** — `correct`, o sorunun `options`
  anahtarlarından biri olmalı (ör. `"C"`; `validate()` denetler). `explanation`
  içinde `<b>...</b>` kullanılabilir.

- **`QAItem` / `DistinctionPair` / `MatchRow`** — **LEGACY.** Eski "Sınav Hazırlık"
  bölümünün bileşenleriydi. Yeni derslerde KULLANMAYIN.
  `pack.test_questions` boş bırakılırsa şablon otomatik olarak bu eski formatı render
  eder; bu sadece 2 eski örnek dersin (`ogretim_teknolojileri`, `sanat_tarihi`)
  bozulmadan çalışmaya devam etmesi içindir.

- **`CoursePack(...)`** — dersin tamamı. Zorunlu alanlar: `course_code`, `title` (HTML
  span içerebilir, örn. `'Sosyoloji<span class="accent-word">ye</span> Giriş'`),
  `subtitle`, `description`, `theme`, `icon_text`, `chapters`, `glossary`.
  Opsiyonel ama HER ZAMAN doldurulması gereken: `ders_klasoru`, `theme_color`,
  `test_title`, `test_subtitle`, `test_instructions`, `test_questions` (20 soru),
  `answer_key_intro`, `answer_key_items`, `overview_lead`, `overview_cards`
  (**tam 6 eleman** — 3x2 grid), `overview_flow` (3-5 `(başlık, alt_metin)` tuple),
  `overview_note`. `sinav_etiketi` varsayılan `"Final"`.

## `get_pack()` fonksiyonunun iskeleti

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))   # düz kipte parents[2]
from cekirdek.content_model import (...)

def get_pack() -> CoursePack:
    ch1 = Chapter(number=1, title="...", subtitle="...", key_terms=[
        KeyTerm("...", "..."), KeyTerm("...", "..."),
        KeyTerm("...", "..."), KeyTerm("...", "..."),
    ])
    ch1.pages.append(
        ChapterPage()
        .add_terms(ch1.key_terms)
        .add_block(BulletBlock(1, "...", ["...", "..."]))
        .add_table(ComparisonTable("...", ["...", "..."], [["...", "..."]]))
    )
    ch1.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(...))
        .add_callout(Callout("focus", "...", "..."))
        .add_summary("...")
    )
    # ... ch2, ch3, ...

    chapters = [ch1, ch2, ...]
    glossary = [Concept(...), ...]

    test_questions = [
        TestQuestion(1, "...?", {"A": "...", "B": "...", "C": "...", "D": "...", "E": "..."}),
        # ... 20 soru
    ]
    answer_key_items = [
        AnswerItem(1, "C", "<b>...</b> ..."),
        # ... aynı sayı ve sırada
    ]

    return CoursePack(
        ders_klasoru="SİSTEMATİK KELAM I",   # kaynaklar/ altındakiyle birebir
        course_code="...", title="...", subtitle="...", description="...",
        theme="forest", theme_color="#0F5148", icon_text="...",
        chapters=chapters, glossary=glossary,
        test_title="Genel Değerlendirme Testi", test_subtitle="...",
        test_instructions="...", test_questions=test_questions,
        answer_key_intro="...", answer_key_items=answer_key_items,
        overview_lead="...", overview_cards=[{"title":"...","text":"..."}, ...],
        overview_flow=[("...", "..."), ...], overview_note="...",
    )
```

---

## Tipografik Hiyerarşi ve Görsel Estetik Standartları (2026-09 Standardı)

Görsel ders notlarının tekdüze metin yığınlarına dönüşmesini engellemek, okuma hızını ve görsel akılda kalıcılığı en üst düzeye çıkarmak için `templates/style.css`'te tanımlı şu tipografik bileşenler **tüm derslerde standarttır**:

### 1. Kategori Rozetleri (`.k-badge`)
Maddelerin veya kavramların kategorisini/türünü belirtmek için `li` veya başlık başında kullanılır:
- `<span class="k-badge">...</span>`: Temel tema renginde standart rozet (örn: `[Şart 1]`, `[Madde 1]`).
- `<span class="k-badge gold">...</span>`: Altın sarısı/amber rozet; ilâhî nass, âyet veya yüksek kıymetli ilkeler için (örn: `[Âyet 1]`, `[1. Din]`).
- `<span class="k-badge alert">...</span>`: Kırmızı/mercan rozet; cezalar, yasaklar, kritik problemler veya zıtlıklar için (örn: `[1. Ceza]`, `[Problem 1]`, `[Haram]`).
- `<span class="k-badge subtle">...</span>`: Yumuşak pastel zeminli rozet; tarihsel aşamalar, hadisler veya usûl adımları için (örn: `[Hadis 1]`, `[Dönüşüm]`, `[Kök 1]`).

### 2. Belirgin Madde Başlıkları (`.k-title`)
Her `li` maddesi düz metin yerine açık, kalın ve serif bir başlıkla açılır:
`<b class="k-title">Kavram / Madde Başlığı:</b>`

### 3. Girintili ve Sol Kenar Çizgili Alt Maddeler (`.k-subitem`)
Açıklama, pedagojik analiz veya fıkhî gerekçeler başlığın altına blok olarak yerleştirilir:
`<div class="k-subitem">Açıklama metni, <u>can alıcı kural</u> ve fıkhî çıkarım.</div>`
- Sol tarafında `var(--accent)` renginde 2px dikey çizgi ve girinti bulunur.
- Başlık ile açıklama görsel olarak ayrılır; öğrenci nereye odaklanacağını hemen görür.

### 4. Arapça Nass / Âyet / Hadis / Kural Kartı (`.k-nass`)
Önemli âyetler, hadisler veya klasik fıkıh/kelâm metinleri için:
```html
<div class="k-nass">
  <span class="ar">﴿Arapça Harekeli Metin﴾</span>
  <span class="meal">«Türkçe meal veya tercüme»</span>
</div>
```
Yumuşak tema zeminine (`var(--accent-tint)`) ve sol dikey renk çizgisine sahiptir.

### 5. Vurgulama Kuralları (`<b>`, `<i>`, `<u>`)
- **Ham Markdown Yasaktır:** İçerik metinlerinde raw `**kalın**` veya `*eğik*` ASLA bırakılmaz; daima HTML etiketleri (`<b>`, `<i>`, `<u>`) kullanılır.
- **`<u>...</u>` (Renkli Alt Çizgi):** Maddelerde ve `KeyTerm` tanımlarında can alıcı yüklem veya temel kural için kullanılır (`--accent` veya `--gold` renginde ince alt çizgiyle şık bir kontrast oluşturur).
- **`<b>...</b>` (Koyu):** Önemli terimler, isimler ve anahtar kelimeler.
- **`<i>...</i>` (Eğik):** Arapça terim telaffuzları, eser adları veya doğrudan alıntılar.

---

## Sayfalama sabitleri (build.py)

```python
GLOSSARY_PER_PAGE = 22     # sözlük sayfası başına kavram (2 sütun)
TEST_PER_PAGE_FIRST = 10   # 2026-09: sınav 3 -> 2 sayfaya indirildi (20 soru = 10+10)
TEST_PER_PAGE = 10         # test devam sayfaları
ANSWER_PER_PAGE = 23       # cevap anahtarı (20 soru -> tek sayfa)
TOC_COMPACT_THRESHOLD = 7  # bu kadar satırı aşınca İçindekiler sıkışık kipe geçer
OVERVIEW_PAGES = 0         # Senaryo A: Genel Bakış kalktı, kapaktan sonra boş sayfa
QA_PER_PAGE = 12 · DISTINCTIONS_PER_PAGE = 8 · MATCHTABLE_PER_PAGE = 11   # LEGACY
```

**Bu değerler ölçüldü, tahminle değiştirmeyin.** Bir ders bu sabitleri global olarak
değiştirmemeli — sabitler zaten birden fazla dersin en sıkı senaryosuna göre
kalibredir; o dersin metinleri alışılmadık uzunsa metni kısaltmayı düşün, sabiti
değil. Sayfa boyutu değişirse `python tools/kalibre.py` çalıştırıp yeniden ölç.
Nasıl ölçüldükleri: `docs/OLCUMLER.md`.

Bölme işini `paginate_capped()` yapar, düz `paginate()` değil: önce gereken en az
sayfa sayısını bulur, sonra öğeleri **dengeli** dağıtır (30 kavram `12+12+6` değil
`10+10+10` olur). İçindekiler bu mekanizmayı hiç kullanmaz (KRİTİK KURAL 4).

Test ve Cevap Anahtarı **2 sütunlu** render edilir (`column-count: 2` +
`column-fill: balance`; her madde `break-inside: avoid`).

## Test + Cevap Anahtarı (sınav bölümü — GÜNCEL format)

`pack.test_questions` doluysa şablon otomatik bu formatı render eder: banner + 3'lü
bilgi çubuğu ("20 Soru / Çoktan Seçmeli / 5 Seçenek") + talimat kutusu + numaralı
sorular; ardından ayrı bir "Cevap Anahtarı ve Çözümler" bölümü. 20 soru standarttır.

### 1. Pedagojik Zorluk Piramidi (20 Soru Dağılımı)

Soruların tümü basit bilgi/tanım sorusu olamaz. Gerçek sınav ağırlığını yakalamak
için 20 soru şu üç seviyeye dengeli dağıtılır:

- **Kolay (Seviye 1 — %25–30 / 5–6 soru):** Temel kavram tanımları, anahtar eser-müellif
  bilgisi. Öğrencinin özgüvenini ve motivasyonunu pekiştirir.
- **Orta (Seviye 2 — %40–45 / 8–9 soru):** İki kavram/ekol arası kıyas, neden-sonuç
  ilişkisi, temel kural tatbiki, boşluk doldurma. Kavrama ve uygulama düzeyini ölçer.
- **Zor / Tam Sınav Formatı (Seviye 3 — %25–30 / 5–6 soru):**
  - **Öncüllü sorular:** `I. ...`, `II. ...`, `III. ...` maddeleri verilerek "hangisi
    doğrudur / yanlıştır?" kurgusu.
  - **Metin / İbare analizi:** Verilen bir metin, ayet, hadis veya düşünür alıntısı
    üzerinden derinlikli çıkarım.
  - **Güçlü çeldiriciler:** Sınavda öğrencilerin en çok karıştırdığı ince ayrımları
    sorgulayan ve yüzeysel ezberi eleyen tuzaklar.
  - **Olumsuz soru kökleri:** "Hangisi söylenemez?", "Hangisi bu kapsamda yer almaz?".

### 2. Arapça ve İslami İlimler Derslerinde Soru Standartları

Ders Arapça ağırlıklı ise (Arap Dili ve Edebiyatı) veya Arapça metin/ıstılah içeriyorsa
(Tefsir, Hadis, Fıkıh, Kelam), sorular salt Türkçe sorulamaz:

- **Denge Kuralı:** 20 sorunun en az 6–10'u doğrudan Arapça metin, ibare veya dil kuralı
  içermelidir. Denge şu 3 modelle kurulur:
  1. **Tam Arapça Soru (Kök + Şıklar Arapça):** Özellikle sarf kalıpları, nahiv/irab,
     eş/zıt anlam, edat kullanımı veya cümle tamamlama için.
     Örnek stem: `«مَا رَأَيْتُ إِلَّا زَيْدًا» - مَا إِعْرَابُ كَلِمَةِ (زَيْدًا) فِي الْجُمْلَةِ؟`
     Şıklar: `A) فَاعِلٌ مَرْفُوعٌ`, `B) مَفْعُولٌ بِهِ مَنْصُوبٌ` vb.
  2. **Hibrit Soru (Arapça Metin/Öncül + Türkçe Analiz):** Arapça ayet, hadis, şiir
     veya nesir pasajı verilir; Türkçe soru köküyle edebi sanat, tefsir/kelam hükmü
     veya dilbilgisi özelliği sorulur.
  3. **Türkçe Kök + Arapça Şıklar:** Türkçe tarif edilen bir kaideye uygun Arapça
     cümle veya ibarenin şıklardan bulunması istenir.
- **Tipografi ve Yazım:** Arapça kısımlar `<span class="ar">...</span>` veya `<bdi class="ar">...`
  ile sarılır. Harekeler (özellikle irab veya sarf sorularında) eksiksiz konur.
- **Cevap Anahtarı Zorunluluğu ("Arapça hiçbir yerde Türkçesiz bırakılmaz"):**
  Arapça sorulan veya Arapça öncüllü her sorunun `AnswerItem.explanation` alanında:
  1. Sorunun ve ibarenin **tam Türkçe çevirisi** (`<span class="ans-trans">"..."</span>`).
  2. Doğru şıkkın dilbilgisi / edebi / mantıksal **analitik gerekçesi**
  mutlaka birlikte verilir. Öğrenci sınavda zorlanır ancak çözüm sayfasında tam kavrar.

### 3. Sayfalama ve Taşma Disiplini (Hayati!)

- **Test = 2 sayfa (10+10), Cevap Anahtarı = 1 sayfa (20 çözüm):**
  Zor veya Arapça soru yazarken cümleleri gereksiz uzatma. Uzun paragraflar yerine
  yoğun, vurucu ve net öncüller kullan. Bir şık 2 satırı geçiyorsa sadeleştir.
- Öncüllü sorularda şablon:
  `<div class="tq-lead">...</div><ul class="tq-premises"><li><span class="tq-roman">I.</span> ...</li>...</ul>Yukarıdakilerden hangileri doğrudur?`

## Tipografi ve Okunabilirlik Hiyerarşisi (2026-09 Kullanıcı Kuralı)

Kullanıcının 2026-09 tarihli doğrudan talimatı gereği, görsel ders notlarında küçük yazıların ve özellikle Arapça harekeli ibarelerin rahat okunabilmesi için aşağıdaki boyut hiyerarşisi esas alınır:

### 1. Arapça ve Harekeli İbareler (`<bdi>`, `.ar`, `[dir="rtl"]`)
- **Ölçek:** Bulunduğu ebeveyn elemanın font boyutuna göre **`%125` (`1.25em`)** oranında büyütülür (madde imlerinde ~11.7 pt, tablolarda ~10.6 pt).
- **Satır Yüksekliği (`line-height`):** En az **`1.65 – 1.68`** olmalıdır. Böylece üstteki fetha/şedde ile alttaki kesre işaretleri birbirine veya satır sınırlarına yapışmaz, fotokopide silikleşmez.
- **Etiketleme Disiplini:** Madde imleri, tablolar, soru kökleri ve şıklardaki tüm Arapça ibareler `<bdi>` (veya `.ar`) ile sarılır.

### 2. Genel Metin ve Küçük Punto İyileştirmesi
- **Madde Metinleri (`.block li`):** `9.35 pt` (line-height: `1.50`, margin-bottom: `1.4mm`).
- **Tablo Hücreleri (`table.ctable td`):** `8.65 pt` (line-height: `1.38`, padding: `2.0mm 3.2mm`).
- **Tablo Başlıkları (`table.ctable th`):** `8.3 pt` (padding: `2.1mm 3.2mm`).
- **Anahtar Terim Kutuları (`.term-box`):** Terim adı `9.7 pt`, tanım `8.75 pt` (line-height: `1.44`).
- **Sözlük (`.gloss-*`):** Terim başlığı `10.4 pt`, tanım `8.75 pt` (line-height: `1.44`), bağlam `7.7 pt`.
- **Vurgu/Uyarı Kutuları (`.callout`):** Başlık `8.8 pt`, metin `9.15 pt` (line-height: `1.50`, padding: `3.4mm 4.4mm`).
- **Test ve Seçenekler (`.tq-*`):** Soru kökü `8.65 pt` (line-height: `1.22`), şıklar `8.2 pt` (line-height: `1.18`), şık harfi `7.0 pt`, soru alt boşluğu `3.2mm` (kesik çizgisiz ferah dikey boşluk), şık aralığı `0.65mm`.
- **Çözümlü Cevap Anahtarı (`.ans-*`):** Açıklama `9.2 pt` (line-height: `1.34`), tercüme `.ans-trans` `8.1 pt`, doğru cevap rozeti `8.2 pt`, madde aralığı `2.6mm` (%85–95 tam sayfa dengesi).

### 3. Teknik Uygulama ve Taşma Güvencesi
- `CoursePack.custom_css` alanı üzerinden ders bazlı enjekte edilir (`master.html.j2` ve `kitap.html.j2` tarafından otomatik dahil edilir).
- Punto büyütüldüğünde sayfa taşmasını önlemek için tablo dikey dolguları (`padding: 2.0mm 3.2mm`) ve blok üst boşlukları (`margin-top: 4.4mm – 4.6mm`) dengelenir.
- Her derlemeden sonra `build.py`'nin taşma denetimi (`[build] Taşma denetimi: tüm sayfalar 210x297mm sınırları içinde. ✓`) mutlaka teyit edilir.

## Birleşik Kitap (`build_kitap.py`)

Tek tek üretilen derslerin hepsini **kesintisiz sayfa numaralarına sahip tek cilt**
halinde birleştirir. Dersleri kopyalamaz — her dersin `src/<slug>.py`'sini taze okur;
bir derste düzeltme yapıp kitabı yeniden derlemek tüm numaraları/içindekileri/yer
imlerini otomatik günceller.

```bash
python build_kitap.py --sinif X --donem Y --sinav Z
```

### Kitaba yeni ders eklemek

> YALNIZCA kullanıcı açıkça "birleşik kitaba ekle / kitabı güncelle / birleştirmeyi
> çalıştır" dediğinde (KRİTİK KURAL 1). Bir ders üretmek bunu TETİKLEMEZ.

İlgili dönemin `src/kitap.py`'sindeki `COURSE_MODULES` listesine **tek satır** ekle
(çıplak modül adı, `content.` öneki YOK):

```python
COURSE_MODULES = ["tefsir2", ..., "yeni_ders"]
```

Başka hiçbir yeri elle güncellemek gerekmez — sayfa numaraları, ana içindekiler,
kapak istatistikleri, yer imleri hepsi hesaplanır.

### Yapısı ve denetimleri

| Bölüm | İçerik |
|---|---|
| Ön kısım | Ana kapak · Künye · Nasıl Kullanılır · Sayfa Rehberi · Ana İçindekiler |
| Gövde | Her ders, tek ders PDF'iyle BİREBİR aynı sayfalarla |

Ön kısım **5 sayfadır** (kapak · künye · önsöz · rehber · ana içindekiler);
11'den fazla ders olursa ana içindekiler dengeli biçimde ikinci sayfaya bölünür
ve ön kısım 6 sayfa olur (`front_matter_page_count()` — ilk dersin sayfa
offset'i buna bağlı).
Kitabın kendi metinleri (kapak başlığı, künye, önsöz, rehber) `src/kitap.py`'deki
`BookPack` alanlarındadır; ders içeriğiyle karıştırma. Kapak isteğe bağlı olarak
tam sayfa görsel olabilir (`BookPack.cover_image` — bkz. `docs/TASARIM.md`).

Mimari: `_ders_govde.html.j2` TEK KAYNAKTIR; `master.html.j2` (tek ders) ve
`kitap.html.j2` (kitap) onu ortak kullanır — "tek derste doğru, kitapta yanlış numara"
durumu yapısal olarak imkânsızdır.

Build çıktısındaki **dört denetim**: taşma (kitapta ayrıca hangi dersin kaçıncı
sayfası olduğu yazılır) · sayfa numarası zinciri · render doğrulaması · boyut
optimizasyonu. Biri hata verirse **PDF'i teslim etme**, önce sebebini bul.

---

## Görsel destek: haritadan kavramsal illüstrasyona

Her ders planlanırken (adım 2, bölümlere ayırma sırasında) **her bölüm için iki
soru sor**: "(A) bu bölümde sıralı bir önerme/süreç/mantık zinciri var mı?" ve
"(B) bu bölümde tek bir görselde özetlenebilecek soyut/kavramsal bir ilişki var
mı?" Cevap evet ise ilgili aracı kullan — aşağıdaki iki yol birbirinden bağımsız,
aynı derste ikisi de olabilir (bkz. `sistematik_kelam_ogretmen_notlari.py`: 2
`FlowDiagram` + 7 `add_block_gorsel` kutusu bir arada).

### A) Akış şeması (`FlowDiagram`) — native, AI GEREKMEZ

Metin **sıralı bir önerme zinciri veya süreç** içeriyorsa (öncül→öncül→sonuç,
aşama aşama ilerleyen bir süreç) `add_flow(FlowDiagram(...))` ile doğrudan kodla
üret — görsel arama/üretme gerekmez, `FlowStep` listesi yeterli. Örnekler: bir
delilin mantık zinciri ("Âlem hâdistir → her hâdisin muhdisi vardır → muhdis
Allah'tır"), bilginin oluşum aşamaları (cehalet→vehm→şek→zan→yakîn), bir
istidlal yönteminin adım adım işleyişi. 3-5 adım idealdir. **Dallanan (ağaç/karar
ağacı) yapılar için bu bileşen UYGUN DEĞİL** — `FlowDiagram` tek sıra yatay
oktur, dallanma göstermez; dallanan ilişkiler B'ye gider.

### B) Soyut/kavramsal konular için AI-üretimi görsel

Bölüm **somut bir yer/yapı/eser içermiyor ama** (kavram haritası, karar ağacı,
karşılaştırmalı diyagram, süreç illüstrasyonu ile) görselleştirilebilecek soyut
bir ilişki anlatıyorsa — klasik "harita/resim" kutusunun (aşağıda) kapsamına
girmez ama yine de görsel destekten faydalanır. Bu durumda görseli SEN ÜRETMEZSİN;
kullanıcı kendi AI aracıyla üretecektir. İki aşamalı iş akışı:

1. **Öneri aşaması:** `add_block_gorsel(block, baslik="<Tür>: <Konu> (<Kavramlar>) — 4:3")` — `baslik`
   alanına rastgele sahne yerine, konuya uygun **5 Pedagojik Görsel Çeşidinden biri** seçilerek doğrudan
   AI'a verilebilecek hazır bir yönerge yazılır:
   - **1. İnfografik Harita:** Havzalar, yayılış yolları, ekol merkezleri ve ilkeleri.
   - **2. Kronolojik Zaman Çizelgesi:** Tarihî dönemler, evreler, öncü âlimler ve eserlerin akış çizgisi.
   - **3. Kavram / Nitelik Şeması:** Bir şahsiyetin ilimleri, doktrini, zâhirî-bâtınî özellikleri matrisi.
   - **4. İki Kutuplu Karşılaştırma Şeması:** Karşıt kavramlar, münazaralar (Sekr vs Sahv, Dar Kadeh vs Umman vb.).
   - **5. Silsile & İlim/Eser Ağacı:** Mürşid-halife zinciri, hoca-talebe halkası ve eserlerin dallanması.
   *Prompt İlkeleri:* Görsel modellerinde harf bozulmalarını önlemek için uzun cümleler yazdırılmaz;
   1-3 kelimelik net başlıklar, kavram etiketleri ve akış okları istenir. Mahremiyet/hürmet filtresi
   ve dersin `theme_color` renk dili belirtilir.
2. **Bağlama aşaması:** kullanıcı görselleri üretip `görseller/` klasörüne koyup
   "ekle" dediğinde, HER `add_block_gorsel` çağrısındaki `baslik` metnini SİL
   (kaldır, `baslik=""` yap) ve yerine `image=_foto("<dosya-adı>.jpg")` ekle — `_foto()`/
   `_GORSELLER` helper'ı dosyanın başına eklenir (bkz. `turk_mutasavviflar_hafta_2.py`).
   Kullanıcı dosya adlarını açıklayıcı seçtiyse (`"Zaman Çizelgesi Tasavvuf Tarihinin 3 Evresi.jpg"`)
   hangi görselin hangi bloğa ait olduğu otomatik eşleşir.

**Bu, yalnız soyut derslerde devreye girer** — ders zaten somut yer/yapı/eser
içeriyorsa (tarih, coğrafya ağırlıklı) önce aşağıdaki harita/resim akışını
kullan; B sadece hiçbir alt türün uymadığı, tamamen soyut bölümler içindir.

## Harita/resim: SADECE boş kutu bırak

**Görsel ARAMA, İNDİRME, GÖMME.** Harita ve resimleri üretilen PDF'e kullanıcı
kendisi yerleştirir. Senin işin, gerektiği yerde metnin yanında doğru ölçüde bir
boşluk bırakmak:

```python
.add_block_gorsel(BulletBlock(1, "Coğrafi Bağlam", [...]), "Hârezmşâh İmparatorluğu (1215)")
```

Solda numaralı blok, sağda üstte küçük başlık + altında **4:3** boş çerçeve
(≈88 × 66 mm). `baslik` opsiyoneldir ve **ders metninden** yazılır; kutunun
altına açıklama satırı KONMAZ — onu yazmak görselin içindekini bilmeyi
gerektirir, o da bu sistemin işi değildir. (İstisna: yukarıdaki B akışında
`baslik`, kullanıcının AI aracına vereceği bir tarif olarak kasıtlı doldurulur,
sonra görsel gelince silinir — bu, "ders metninden yaz" kuralının bilinçli
istisnasıdır.)

- Nereye konacağına ham metin karar verir: coğrafya/yayılma/sınır anlatan bir
  blok varsa kutuyu onun yanına koy, başka yere serpme.
- Kutu **bölünemez bir bloktur** — sayfa dengelemesini tetikler. Ekledikten
  sonra taşma çıktısını oku ve sayfayı gözle kontrol et.
- **Şahsiyet kartlarına dokunma.** Yuvarlak baş harf rozeti zaten resmin yerini
  gösteriyor; oraya ekstra kutu/alan açma.

---

## Hızlı komut özeti

```bash
# Tek dersi derle (A4, RGB — fotokopi için)
python build.py <slug> --sinif X --donem Y --sinav Z

# Aynı ders, matbaa için PDF/X-4 CMYK olarak
python build.py <slug> --sinif X --donem Y --sinav Z --cmyk

# Sayfa doluluğunu ölç / bölüm sayfalarını yeniden dağıt / sabitleri kalibre et
python tools/olcum.py <slug> --sinif X --donem Y --sinav Z
python tools/dengele.py <slug> --sinif X --donem Y --sinav Z   # --kuru = sadece raporla
python tools/kalibre.py --sinif X --donem Y --sinav Z          # sayfa boyutu değiştiyse

# Dersin rengini tablodan al (kendi kafandan seçme)
python cekirdek/renk_uretici.py "<DERS ADI>" --sinif X --donem Y --sinav Z
python cekirdek/renk_uretici.py --tablo

# Ghostscript + ICC profili teşhisi
python cekirdek/pdfx.py

# BİR DÖNEMİN tüm derslerini tek kitap halinde derle (src/kitap.py sırasına göre)
python build_kitap.py --sinif X --donem Y --sinav Z

# Belirli sayfaları PNG'ye çevirip incele
pdftoppm -png -r 100 -f <ilk> -l <son> "<D>/gorsel_ders_notlari/<DERS ADI>/<slug>.pdf" "<D>/gorsel_ders_notlari/preview/pg"

# Bookmark/link doğrulaması
python3 -c "
from pypdf import PdfReader
r = PdfReader('<D>/gorsel_ders_notlari/<DERS ADI>/<slug>.pdf')
for it in r.outline: print(it.title, '->', r.get_destination_page_number(it)+1)
"
```

## Özet — bir ders eklerken zihinsel kontrol listesi

- [ ] Sınıf/dönem/sınav'ı kullanıcıya SORDUM (varsaymadım)
- [ ] Kaynak eklenmediyse o dönemin `kaynaklar/` klasörlerinde ders adıyla eşleşen
      dosyayı aradım (yoksa kullanıcıdan istedim — başka döneme BAKMADIM)
- [ ] Ham metni tamamen okudum (atlamadım)
- [ ] `özetlenmiş_dersler/<DERS ADI>/00-YONTEM.md` varsa onu baştan sona okudum ve
      formatına birebir uydum (yoksa ve ders metin tahlili/dil dersiyse yazdım)
- [ ] `NN-hafta/` klasörleri varsa: haftalık çalışma belgelerini okudum, kapsam
      süzgeci olarak SADECE işlenen bölümleri aldım, hocanın vurgu/örnek/sınav
      sinyallerini içine gömdüm; hiçbir vurgu kaybolmadı
- [ ] 5-7 bölüme, ham içeriğin doğal yapısını takip ederek ayırdım
- [ ] Rengi `cekirdek/renk_uretici.py` tablosundan aldım (kendim seçmedim), tek harfli
      Latin `icon_text` verdim
- [ ] `<D>/src/<slug>.py` yazdım, API'ye birebir uydum (`sys.path` satırı `parents[4]`,
      düz kipte `parents[2]`; import `from cekirdek.content_model import ...`)
- [ ] `ders_klasoru=` alanını `kaynaklar/` altındaki klasör adıyla BİREBİR yazdım
- [ ] 20 soruluk `test_questions` + eşleşen `answer_key_items` yazdım (LEGACY değil)
- [ ] `python build.py <slug> --sinif X --donem Y --sinav Z` çalıştırdım
- [ ] "[TAŞMA UYARISI]" çıkmayana kadar `tools/dengele.py` çalıştırıp yeniden derledim
      (gerekirse elle sayfa böldüm)
- [ ] Konsoldaki "[SONUÇ] Bitmiş (trim) ölçü : 210 x 297 mm" satırını gördüm
- [ ] Kapak (renk doğru mu?) + içindekiler + genel bakış + her bölüm ilk sayfası + en
      az bir tablo sayfası + sözlük/test/cevap anahtarı son sayfalarını görsel kontrol
      ettim
- [ ] Harita/resim gereken yerlere `add_block_gorsel(...)` ile BOŞ KUTU bıraktım
      (görsel aramadım/indirmedim; şahsiyet kartlarına dokunmadım)
- [ ] Her bölüm için görsel destek türünü değerlendirdim: sıralı önerme/süreç
      zincirleri için `FlowDiagram` (native) ekledim; tamamen soyut ama
      görselleştirilebilir kavramsal ilişkiler için AI-görsel kutusu (net,
      çizilebilir tarifle `baslik` alanına) açtım — zorlama kutu koymadım
- [ ] Her bölümün TÜM sayfalarını inceleyip devam sayfalarının (son sayfa hariç)
      %90-95 dolulukta olduğunu doğruladım; gerekirse mevcut içeriği taşıdım/
      birleştirdim — asla yeni içerik uydurmadım, taşan denemeleri geri aldım
- [ ] Bookmark/link sayısını doğruladım
- [ ] (SADECE kullanıcı açıkça istediyse — KRİTİK KURAL 1) Dersi o dönemin
      `src/kitap.py`'sindeki `COURSE_MODULES` listesine ekleyip
      `python build_kitap.py --sinif X --donem Y --sinav Z` çalıştırdım; dört denetim
      de "✓" verdi
- [ ] Çıktının `<D>/gorsel_ders_notlari/<DERS ADI>/` altına düştüğünü konsoldaki
      "[build] Ders klasörü:" satırından doğruladım
- [ ] PDF'i kullanıcıya sundum
