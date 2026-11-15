# AGENTS.md — Görsel Ders Notu Üretim Sistemi Kuralları

Bu dosya, Antigravity ve bu depoda çalışan tüm yapay zekâ asistanları için **bağlayıcı temel işletim kurallarını** içerir.
Detaylı sistem kılavuzu için ayrıca `CLAUDE.md` dosyasına bakınız.

---

## KRİTİK KURAL 0: Tüm Üretimlerde Otomatik ve Kesintisiz Kural Uyumu (Hatırlatma Bekleme Yasağı)
- **Bağlayıcılık İlkesi:** Asistan, kullanıcıdan herhangi bir uyarı veya hatırlatma beklemeksizin; bundan sonra üretilecek veya güncellenecek istisnasız **HER görsel ders notunda (`src/<ders>.py` -> `build.py`) ve Okuma PDF dokümanında (`tools/okuma_pdf.py`)** bu belgede (`AGENTS.md`) ve `CLAUDE.md`'de yer alan **15 Kritik Kuralın ve Standartların tamamını** doğrudan, eksiksiz ve otomatik olarak uygulamakla yükümlüdür.
- **Tavizsiz Kalite Standartları:** Vektörel kapak (`cover_image=""`), 0 mm taşma (%90–100 doluluk), BiDi izolasyonu, şık eşitliği ve tüyo yasağı, İçindekiler ve Sözlük altına tablo ekleme yasağı (`toc_footer_html` ve `glossary_footer_html` KULLANILMAZ), tam sayfa kapsamlı Anahtar Kavramlar Sözlüğü (18–22 zengin kavram) ve çözümlü cevap anahtarında her soruda `.ans-page-ref` («Tekrar için: s. …») yönlendirmesi her derste zorunlu bileşendir; "sonradan eklenir" denilerek atlanamaz.
- **Otomatik Doğrulama Şartı:** Kod yazımı bittiğinde `python tools/olcum.py <slug> --sinif X --donem Y --sinav Z` ve `python build.py <slug> --sinif X --donem Y --sinav Z` komutları çalıştırılarak 0 mm taşma ve sayfa verimliliği doğrulanmadan iş tamamlanmış sayılamaz.

## KRİTİK KURAL 1: Birleşik Kitaba Otomatik Ekleme Yasağı
- Tekil ders üretildiğinde veya güncellendiğinde birleşik kitaba otomatik EKLEME. Birleştirme scriptini çalıştırma.
- Çıktı sadece o dersin kendi PDF'i olarak üretilir (`<dönem>/gorsel_ders_notlari/<DERS ADI>/<slug>.pdf`).
- Birleşik kitaba ekleme yalnızca kullanıcı açıkça talep ettiğinde yapılır.

## KRİTİK KURAL 2: Sınav Dönemi Varsayılmaz — Her Zaman Sorulur
- Hiçbir script'in varsayılan dönemi yoktur.
- Kullanıcı belirtmediyse `--sinif {2,3} --donem {1,2} --sinav {vize,final}` parametrelerini sormadan derleme yapma.

## KRİTİK KURAL 3: Girdi ve Çıktı Hiyerarşisi (`<DERS ADI>` Alt Klasörü)
- `kaynaklar/ders_kaynaklari/<DERS ADI>/` -> Ham kaynak
- `kaynaklar/özetlenmiş_dersler/<DERS ADI>/` -> Yazılı konu anlatımı özeti (build.py çıktısı değil, girdisidir)
- `gorsel_ders_notlari/<DERS ADI>/` -> Görsel ders notu PDF'i (build.py çıktısı)
- `ders_anlatimlari/<DERS ADI>/` -> Kapsamlı yazılı konu anlatımı dokümanı (.md / .pdf)
- Dosyalar köke değil, mutlaka dersin adını taşıyan alt klasöre yazılır.

## KRİTİK KURAL 4: İçindekiler TEK SAYFADIR
- İçindekiler asla 2. sayfaya taşmaz (`TOC_MAX_ROWS = 14`).

## KRİTİK KURAL 5: Kapak Tasarımı — Standart Vektörel Kapaktır (`cover_image=""`)
- Kapak her zaman sistemin yerel CSS/SVG vektörel kapağı ile üretilir (`cover_image=""`).
- Harici görsel aranmaz, difüzyon görseli üretilmez. Özel görsel sadece kullanıcı açıkça isterse atanır.
- **Kapak Açıklaması (`description`):** Kapak sayfasında başlığın altındaki açıklama/tanıtım metni daima **kısa ve öz 1–2 cümle** olmalıdır; asla uzun paragraflar yazılmaz.
- **`KAPAK/` Klasörü ve Ana Kapak Görsellerinin Dokunulmazlığı (KESİN SİLME YASAĞI):** `gorsel_ders_notlari/KAPAK/` klasörü her dersin ana kapak görsellerini barındırır. Bu klasördeki ana kapak görselleri KESİNLİKLE SİLİNMEZ, silme scriptlerine/temizlik komutlarına dâhil edilmez, taşınmaz veya ezilemez. Yalnızca ilgili dersin hangi haftası işleniyorsa o haftaya ait materyaller değiştirilirken haftalık dosyalar silinebilir; `KAPAK/` klasöründeki dosyalara asla dokunulmaz.

## KRİTİK KURAL 6: Sayfa Düzeni ve Ön Kısım Mimarisi (Senaryo A — Kapak Arkası Boş Sayfa)
- **Genel Bakış Sayfası Kaldırılmıştır:** Tekil görsel ders notlarında "Genel Bakış" sayfası okunmadan atlandığı ve sayfa israfı oluşturduğu için tamamen kaldırılmıştır.
- **Kapak Arkası Boş Sayfa (Çift Taraflı Baskı / Forma Uyumu):** Hem tekil derslerde hem birleşik kitapta kapağın arkasına boş sayfa (`<section class="page blank-page ...">`) yerleştirilir. Böylece çift taraflı baskıda içindekiler sağ sayfada açılır.
- **Tekil Ders Notu Sayfa Akışı:** `s.1 Kapak` → `s.2 Boş Sayfa` → `s.3 İçindekiler` → `s.4 Bölüm 1` (Bölümler daima 4. sayfadan başlar).
- **Birleşik Kitap Ön Kısım Sadeleştirmesi:** Birleşik kitapta atlanan ve sayfa israfı oluşturan "Künye", "Bu Kitap Nasıl Kullanılır" ve "Sayfa Rehberi" sayfaları kaldırılmıştır.
- **Birleşik Kitap Sayfa Akışı:** `s.1 Ana Kapak` → `s.2 Boş Sayfa` → `s.3-4 Ana İçindekiler` → `s.5 1. Ders Başlangıcı` (1. ders kapağı s.5 → s.6 Boş Sayfa → s.7 İçindekiler → s.8 Bölüm 1...).

---

## KRİTİK KURAL 7: Öğretmen / Hoca İsimlerinin Kullanım Yasağı (Tüm Not ve Okuma PDF Dokümanlarında Kesin Yasak)
- **Hoca / Öğretmen İsmi Kullanılmaz (KESİN YASAK):** Hocaların izni olmadan isimlerini veya unvanlarını görsel ders notlarında (`src/*.py` -> PDF / HTML), Okuma PDF dokümanlarında (`tools/okuma_pdf.py` -> `.md` / `.pdf`), özetlerde, konu anlatımlarında veya soru metinlerinde geçirmek KESİNLİKLE YASAKTIR.
- **Pedagojik İfade Zorunluluğu:** Kapaklarda, künyelerde, ünite başlıklarında, soru köklerinde, çözümlü test cevap anahtarlarında (`AnswerItem`) veya açıklamalarda hoca isimleri ve unvanları zikredilmez; yalnızca "ders anlatımında", "ders içi sınav yönergesinde", "müfredat standartlarında", "ders içi tahta notlarında" gibi nesnel ve pedagojik ifadeler kullanılır.

---

## KRİTİK KURAL 8: Görsel Ders Notu Üretiminde 7 Temel Standart ve Kalite Protokolü (ZORUNLU)

Herhangi bir ders veya hafta için görsel ders notu (`src/<ders>.py` -> `build.py`) üretilirken aşağıdaki 7 standart İSTİSNASIZ uygulanacaktır:

### 1. Standart: Resmî Ders Renk Teması
- Her dersin tema rengi `cekirdek/renk_uretici.py` içindeki `DERS_RENKLERI` sözlüğünden birebir alınır (ör. HADİS / HADİS III için `#664324` / Koyu Deri Cilt `theme="leather"`, KELAM için `#14665a` vb.).
- Başka bir dersten kalan şablon/yeşil renk asla rastgele atanamaz.

### 2. Standart: Vektörel Kapak Düzeni
- Kapak her zaman yerel CSS/SVG vektörel kapak (`cover_image=""`) olarak kalır. Altın köşe süsleri, usturlap motifi, amblem harfi, ders kodu ve şeffaf istatistik kutuları kusursuz çizilir.

### 3. Standart: Sayfa Verimliliği & Sıfır Sayfa İsrafı (0 mm Taşma)
- Sayfalarda gereksiz boşluk, seyreklik ve sayfa israfı yasaktır. Her bölüm sayfası `%90–100` dolulukta olmalıdır.
- Her üretimden sonra `python tools/olcum.py <slug> --sinif X --donem Y --sinav Z` ile doluluk ölçülür; `build.py` taşma denetiminde `0 mm taşma` ("tüm sayfalar 210x297mm sınırları içinde ✓") görülmeden ders tamamlanmış sayılamaz.

### 4. Standart: Tipografik Hiyerarşi ve Görsel Vurgu Düzeni
- Kuru markdown metinleri yerine:
  - `.k-badge` (`.gold`, `.alert`, `.subtle`) ile kategori rozetleri
  - `.k-title` ile koyu belirgin madde başlıkları
  - `.k-subitem` ile sol kenarı tema renkli çizgili açıklama gövdesi
  - `.k-nass` ile Arapça nass ve meal kutuları (`.ar` ve `.meal`)
  - Temel hüküm, kural ve sınavda puan getirecek kavramlar `<u>` ile altı çizili vurgulanır.
- **Çift Liste İmi (`–`) Önleme Kuralı:** Kutu kullanılan maddelerde (`.k-nass`, `.k-subitem`), `li:has(> .k-nass:first-child)::before { display: none !important; }` defansı uygulanır ve `k-badge` ile altındaki kutular tekil bir `<li>` içinde hiyerarşik yapılandırılır; kutu kenarlıklarına çakışan çift tireler kesin olarak engellenir.

### 5. Standart: Kelime ve Font Büyüklüğü Hiyerarşisi (2026-09 Ölçeği)
- **Arapça ve Harekeli İbareler (`bdi`, `.ar`, `[dir="rtl"]`):** Harekelerin ve harflerin net seçilebilmesi için `%128–132` daha büyük (`font-size: 1.28em–1.32em`) ve ferah satır aralığıyla (`line-height: 1.68`) render edilir. 4'lü anahtar terim kutuları (`KeyTerm`), tablolar, sözlük ve metin içi âyet şahitleri (`﴿...﴾`) kesinlikle `<bdi class="ar">` ile sarılır; çıplak Latin font boyutunda bırakılmaz. Nass kutusu nassı `font-size: 12.0pt` olarak öne çıkar.
- **BiDi İzolasyonu & Parantez Kuralı:** LTR akış içerisinde raw Arapça karakterler nedeniyle cümlenin sağına veya başına sıçrayan liste noktaları (`•`), iki noktalar (`:`), tireler (`-`), tırnaklar ve parantezler `<bdi class="ar">` ile sarılarak izole edilir. Parantez içi açıklamalarda parantez yönünün ve noktalama işaretlerinin ters dönmesini önlemek için: daima önce Türkçe ifade yazılır, ardından parantez içinde izole Arapça terim (`(<bdi class="ar">...</bdi>)`) verilir.
- **Türkçe Gövde:** Gövde metinleri 9.35pt, tablo hücreleri 8.65pt, kutu metinleri 9.15pt.
- **SÖZLÜK, TEST VE CEVAP ANAHTARINDA KÜÇÜK PUNTO YASAĞI (İSTİSNASIZ İRİ PUNTO STANDARDI):**
  - Asistan kullanıcıdan *"harfler küçük kalmış büyüt"* uyarısı beklemeden; istisnasız **HER DERS VE SINAV KİTAPÇIĞINDA** aşağıdaki asgari punto değerlerini doğrudan inşa etmekle yükümlüdür:
    1. **Anahtar Kavramlar Sözlüğü:**
       - Terim (`.gloss-term`): **`9.60pt – 10.0pt`** (kalın, kurumsal renk)
       - Tanım (`.gloss-def`): **`8.70pt – 9.00pt`** (ferah satır aralığı: `line-height: 1.32–1.36`)
       - Referans (`.gloss-ref`): **`7.50pt – 7.80pt`** (italik, zarif)
    2. **Genel Değerlendirme Testi:**
       - Soru Kökü (`.tq-stem`): **`8.40pt – 8.65pt`** (line-height: `1.22`, yarı kalın okunur metin)
       - Şık Metinleri (`.tq-options li`): **`7.90pt – 8.15pt`** (line-height: `1.20`)
       - Şık Harf Rozetleri (`.opt-letter`): **`7.2pt`** (3.8mm x 3.8mm daire, belirgin)
       - Soru Numarası (`.tq-num`): **`7.6pt`** (5.0mm x 5.0mm daire)
    3. **Çözümlü Cevap Anahtarı:**
       - Çözüm Metni (`.ans-explain`): **`8.25pt – 8.50pt`** (line-height: `1.22–1.24`)
       - Arapça Meal Kutucuğu (`.ans-trans`): **`7.75pt – 8.00pt`**
       - Sayfa Yönlendirmesi (`.ans-page-ref`): **`7.30pt – 7.50pt`** (kalın, belirgin rozet)
       - Doğru Şık Rozeti (`.ans-correct`): **`7.30pt – 7.50pt`**
       - Numara Rozeti (`.ans-num`): **`7.4pt – 7.6pt`** (4.8mm x 4.8mm daire)
  - `7.0pt – 7.6pt` gibi göz yoran ve okunması zor cılız/mikro puntolar KESİNLİKLE KULLANILAMAZ.

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

### 7. Standart: Görsel Ekleme Kutuları, Harici Prompt Teslimi ve KUTU N İsimlendirme Standardı (4:3)
- Her bölüme en az bir adet `add_block_gorsel(BulletBlock(...), baslik="KUTU N: ...", image=None)` şablonuyla 4:3 oranında görsel çerçevesi eklenir.

#### A) Kutu Üzeri Sade Başlık Kuralı (Uzun Prompt Yazma Yasağı):
- PDF içerisindeki görsel kutusunun üzerine (`baslik` parametresi) kesinlikle uzun paragraf promptları YAZILMAZ.
- Kutu üzerine yalnızca kutu numarası ve kısa şema adı yazılır (örn. `baslik="KUTU 1: Din ve Felsefe Telif Mimarisi"`, `baslik="KUTU 2: İslam Medeniyet Havzası"`).
- Böylece PDF sayfasında kutu üstü ferah, derli toplu kalır; uzun metinlerin sağa yaslı (float) çerçeveyi aşağı itmesi ve sayfa taşması oluşturması kesin olarak engellenir.

#### B) Ders Bitimi Otomatik Harici Prompt Teslim Protokolü:
- Görsel ders notu derlemesi tamamlandığında, asistan tüm kutuların kristal netlikteki ayrıntılı yapay zekâ promptlarını:
  1. Hem sohbet çıktısında doğrudan kopyalanabilir bir metin bloğu olarak sunar,
  2. Hem de `gorsel_ders_notlari/<DERS ADI>/gorsel_promptlari.md` dosyasına kaydeder.
- Bu prompt metni; kolaj yasağı, 4:3 oranı, minimalist parşömen infografik dili ve sıfır mikro-metin ilkelerini içeren **Resmî Kullanıcı Meta-Promptu** ile başlar. Kullanıcı bu tek metni kopyalayıp harici yapay zekâya (ChatGPT, Claude, Gemini vb.) yapıştırdığında tüm görseller tek seferde kesintisiz üretilir.

#### C) Standart Dosya İsimlendirme ve Otomatik Bağlama (`kutu_1.jpg`, `kutu_2.jpg`):
- Kullanıcı harici yapay zekâda ürettiği görselleri ilgili dersin `görseller/` klasörüne sırasıyla **`kutu_1.jpg`**, **`kutu_2.jpg`**, **`kutu_3.jpg`** (veya `KUTU 1.jpg`, `KUTU 2.jpg`) adıyla kaydeder.
- Asistan kullanıcı "görselleri ekledim" dediğinde hiçbir karmaşa yaşamadan; 1. kutuya `image=_foto("kutu_1.jpg")`, 2. kutuya `image=_foto("kutu_2.jpg")` atamasını yapar ve kutu üzerindeki `baslik=""` yaparak resmi tam hizasında PDF'e bağlar.

#### D) Pedagojik Görsel Matrisi ve Zengin Şema Çeşitliliği (11 Temel Tür):
Görseller kuru bir süs değil; öğrenciye doğrudan kavram, usûl veya sınav bilgisi kazandıran araçlardır. Asistan dersin ve konunun doğasına göre aşağıdaki pedagojik şablonlardan yararlanır:
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

#### E) AI Üretim & Prompt İlkeleri:
- **Tipografik İrilik ve Sıfır Mikro-Metin Kuralı:** Görsel kutusu kompakt bir çerçevede (`~75x56 mm`) yer aldığından, görsel içine minik paragraflar, madde işaretli küçük açıklamalar ve yan metinler koymak **KESİNLİKLE YASAKTIR**. Yalnızca **iri, kalın, net 1–3 kelimelik kavram kutuları ve akış okları** kullanılır.
- **Dil Zorunluluğu:** Tüm şema başlıkları, kutucuklar ve kavram etiketleri **kesinlikle Türkçe** (Arapça derslerinde Arapça) olacaktır; İngilizce etiket kesinlikle yasaktır.
- **Stil & En-Boy Oranı:** Modern vektörel infografik, minimalist parşömen arka plan, dersin tema rengi + altın sarısı tonları ve mutlaka **4:3 en-boy oranı**.
- **Hürmet & Mahremiyet:** İslâmî ilimler vakarına uygun; mahrem veya uygunsuz tasvir yapılmaz.

#### F) Kullanıcı Meta-Prompt Standardı (Otomatik & Kesintisiz Tekil Üretim):
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

#### G) Sayfa Yerleşimi ve Float Metin Akışı:
- Görsel kutusu (`add_block_gorsel`), `float: right` ile sağa yaslanır. Metin başlığı ve ilk maddeler görselin solunda akarken, görselin bittiği hizada sonraki maddeler görselin altındaki boşluğa taşarak sayfanın tam genişliğine (`100%`) yayılır.
- **BFC ve Taşma Önleme Standardı (`display: flow-root;`):** Sağa yaslanan görsel kutusunun yanındaki kutuların (`.k-nass`, `.k-subitem`) görsel çerçevesi arkasına taşmaması için CSS'te `display: flow-root;` kuralı zorunludur.

#### H) HADİS III Dersi Özel İstisnası (Görsel Ekleme Kutusu Yasağı):
- Kullanıcı talimatı gereğince, **HADİS III** dersinin görsel notlarında **görsel ekleme kutusu (`add_block_gorsel`) KESİNLİKLE KULLANILMAZ**.
- Bunun yerine zengin hadis levhaları (`_hadis_board`), terceme-i bâb levhaları (`_nass_board`), isnad zincirleri (`_isnad_section`) ve bâb fıkhı analizleri doğrudan tam sayfa genişliğinde (`add_block`) tanzim edilir.

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

## KRİTİK KURAL 11: Disk Alanı Tasarrufu — Ara HTML, Ham Görseller ve Kapak Dosyalarının Temizlenmesi

1. **Otomatik Ara HTML Temizliği:** `build.py` ve `build_kitap.py` PDF üretimini başarıyla tamamladıktan sonra ara `.html` dosyasını otomatik olarak siler (yüzlerce MB disk tasarrufu sağlar). İnceleme/hata ayıklama gerekirse `--keep-html` bayrağı kullanılır.
2. **Ham Görsellerin Temizliği:** Görsel kutuları için görseller `image=_foto(...)` ile bağlanıp PDF üretildikten sonra; görseller doğrudan PDF ikili dosyasına gömüldüğünden, projede ve bulutta gereksiz yer kaplamaması adına `görseller/` klasöründeki ham görsel dosyaları temizlenir/silinir.
3. **Ham Kapak Görsellerinin Temizliği:** Kullanıcı özel bir kapak görseli (`*kapak.{png,jpg,jpeg,webp,jfif}`) eklediğinde, bu görsel `cover_image` olarak bağlanıp PDF başarıyla üretildikten sonra; kapak görseli de doğrudan PDF dosyasına kalıcı olarak gömüldüğünden, diskte ve bulutta (OneDrive) gereksiz yer kaplamaması adına ham kapak görseli dosyası silinir/temizlenir.

---

## KRİTİK KURAL 12: Şahsiyet / Düşünür Kartları (`Person`) Kullanım Protokolü ve Otomatik Ekleme Yasağı

Şahsiyet kartları (`Person`, `add_person`, `add_person_row`), sayfa mizanpajında 35 mm dikey yer kaplayan ve öğrencinin görsel dikkatini doğrudan üzerine çeken son derece stratejik ve ağırlıklı bileşenlerdir. Bu bileşenin kullanımı aşağıdaki katı kurallara bağlanmıştır:

1. **Otomatik / Hafızadan / Şablondan Rastgele Şahsiyet Kartı Ekleme Yasağı (KESİN YASAK):**
   - Geçmiş ders şablonlarından, yapay zekânın genel kelâm/fıkıh/tarih hafızasından veya "sayfada boşluk kaldı / kelâm dersidir bir âlim bulunsun" denilerek rastgele veya otomatik olarak şahsiyet kartı KESİNLİKLE EKLENEMEZ.
   - Her dersin kodu sıfırdan, o haftanın doğrudan ders içeriği ve verileri esas alınarak kurulur.

2. **Kaynakta Doğrudan Geçme ve Dersin Odak Konusu Olma Şartı:**
   - Bir şahıs kartı **YALNIZCA VE YALNIZCA** o haftanın öğretmen ders notunda veya temel kaynak metninde o şahsiyet doğrudan, tarihsel, ekol kurucu veya biyografik bir odak olarak işleniyorsa / geçiyorsa eklenebilir.
   - Eğer derste veya notta şahsın biyografisi, ekoldeki kurucu rolü veya müstakil bir bahsi geçmiyorsa (konu salt kavram, epistemoloji, semantik veya hüküm teorisiyse); `add_person` **KESİNLİKLE KULLANILMAZ**. Bu alan doğrudan dersin analitik maddelerine, nasslarına veya karşılaştırma tablolarına tahsis edilir.

3. **Doyurucu, Genel Bilgi Verici & Akademik Derinlik Standardı (Kısa / Yüzeysel Metin Yasağı):**
   - Şahıs kartı meşru olarak kullanıldığında; içindeki metin (`tagline`, `bio`, `key_work`) asla kuru, 1 cümlelik veya yüzeysel bir unvan geçiştirmesi olamaz.
   - `tagline`: Şahsın ilim tarihindeki ve mezhep/ekol içerisindeki kurucu unvanını ve dönemini net yansıtır (ör. *"Ehl-i Sünnet Kelâmının Kurucusu ve Mütekaddimîn Dönemi İmamı"*).
   - `bio`: Yalnızca doğum-ölüm tarihi değil; şahsın ilgili ilim dalındaki devrimsel metodolojisini, savunduğu ana tezi, akıl-nakil dengesindeki duruşunu ve o dersteki temel ağırlığını anlatan **dolu, genel bilgi verici ve öğretici tam bir paragraf** olarak yazılır.
   - `key_work`: Şahsın o ilim dalındaki en temel şaheseri ve literatürdeki yeriyle birlikte zikredilir (ör. *"Kitâbü't-Tevhîd & Te'vîlâtü'l-Kur'ân"*).

4. **Şahsiyet Kartı Olmadığında Sayfa Dengeleme:**
   - Şahıs kartı kullanılmadığında sayfalarda boşluk kalmaması için, sayfanın asıl ders içeriği genişletilir; nass kutuları (`.k-nass`), karar ağaçları, karşılaştırma tabloları, `BulletBlock` içi analitik maddeler veya odak uyarı kutuları (`Callout`) ile sayfa %90–100 doluluk ve 0 mm taşma sınırında tutulur.

---

## KRİTİK KURAL 13: Sınav Hazırlık Protokolü ve Dengeli Sınav Kitapçığı Mimarisi (Yazılı Temel + Görsel Sınav Kitapçığı)

Kullanıcı herhangi bir ders için vize veya final sınavı odaklı ders anlatımı / çalışma notu talep ettiğinde; asistan kullanıcıdan hatırlatma veya ek uyarı beklemeksizin istisnasız **HER DERS İÇİN** aşağıdaki pedagojik protokolü ve dengeli sınav kitapçığı mantığını uygular:

1. **İki Aşamalı Üretim Sıralaması (Zorunlu İş Akışı):**
   - **1. Aşama (Yazılı Temel Dokümanı):** Görsel ders notuna geçilmeden önce, ilgili dersin işlenen tüm haftalık anlatımları ve resmî kaynakları taranır. Konu anlatımı başlık sırasına sadık kalınarak; kelimesi kelimesine kuru aktarma yapmadan fakat hiçbir sınav detayını, nassı, fıkhî/kelâmî ayrımı, filozof doktrinini ve mukayeseyi atlamadan `ders_anlatimlari/<DERS ADI>/<Ders Adı> - Vize Konu Anlatımı Kitapçığı.md` ve `kaynaklar/özetlenmiş_dersler/<DERS ADI>/<slug>-vize-ozeti.md` hazırlanır. Yüzeysel özetleme kesinlikle yasaktır; her bilgi bir sınav sorusu hassasiyetiyle işlenir.
   - **2. Aşama (Görsel Sınav Kitapçığı):** Yazılı anlatım tamamlandıktan sonra, bu sağlam yazılı dokümana dayanarak görsel ders notu (`src/<ders>_vize.py` -> `build.py`) üretilir.

2. **Dengeli Sınav Kitapçığı Mantığı (Esnek Forma Uyumu: 24, 28, 32 veya 36 Sayfa):**
   - **Rijit Sayfa Dogması Yoktur:** Sistem kendini katı bir tekil sayfa sayısına zorlamaz; kitapçık hacmi dersin işlenen hafta sayısına (4 hafta, 6 hafta, 8 hafta vb.) ve nass/bilgi yoğunluğuna göre doğal olarak şekillenir.
   - **Temel Mantık ve İki Uçtan Kaçınma:**
     - *Aşırı Sıkıştırma Yasağı:* Konular yapay olarak 20 sayfaya sıkıştırılıp öğrenciye soru kaçırtacak özetlemelere gidilemez.
     - *Aşırı Hacim Yasağı:* Haftalık notların ham birleşimi olan 45+ sayfalık hacim tekil sınav tekrarı için ağır olduğundan, sınav notu olarak değil 'arşiv külliyatı' olarak saklanır.
     - *Altın Denge:* Konular haftalık ortalama **4–6 sayfa doymuş anlatımla** işlenir; çift taraflı baskı ve matbaa forma kuralına (`sayfa_sayisi % 4 == 0`) uygun olarak genellikle **24, 28, 32 veya 36 sayfa** aralığında dengelenir.
   - **Standart Bileşenler:**
     - **Ön Kısım (3 sf):** Vektörel Kapak (`cover_image=""`, kısa 1-2 cümlelik `description`), Kapak Arkası Boş Sayfa, Tek Sayfa İçindekiler (`TOC_MAX_ROWS = 14`).
     - **Doymuş Konu Anlatımı:** Hafta sayısına göre 16–26 sayfa doymuş metin (ilişkili başlıklar lehimlenmiş, sıfır konu kaybı, `%100.0 doluluk`, `0.0 mm taşma`).
     - **Zengin Vize Sözlüğü:** 1 veya 2 sayfa (20–30 kilit kavram, sayfa başına dengeli dağıtım).
     - **Pedagojik Vize Testi:** Tam 2 sayfa (20 soru; 1-6 Kolay, 7-14 Orta, 15-20 Zor; şık boyutu eşitliği, parantez içi tüyo yasağı, dengeli 4'er A, B, C, D, E dağılımı).
     - **Çözümlü Cevap Anahtarı:** Tam 1 sayfa (20 analitik çözüm, `<span class="ans-trans">` terim mealleri ve kitapçıktaki yerini gösteren `.ans-page-ref` sayfa yönlendirmesi).
     - **Kapanış:** Tamamlayıcı Boş Sayfa + Vektörel Arka Kapak.

3. **Kapsamlı Külliyat ile Sınav Kitapçığı Ayrımı ve İsimlendirme:**
   - Haftalık tüm derslerin ham birleşimi olan geniş külliyat ana modülde (`src/<ders>.py` -> `<slug>.pdf`) korunur, ezilmez veya silinmez.
   - Sınav odaklı optimize edilmiş kitapçık ise `src/<ders>_vize.py` -> `<slug>-vize.pdf` olarak üretilir. Böylece öğrencinin elinde hem tam arşiv külliyatı hem de sınav masasında tek oturuşta bitirebileceği dengeli sınav kitapçığı bulunur.

4. **Otomatik Ölçüm ve Taşma Doğrulaması:**
   - Üretim tamamlandığında `python tools/olcum.py <ders>_vize --sinif X --donem Y --sinav Z` ve `python build.py <ders>_vize --sinif X --donem Y --sinav Z` çalıştırılarak tüm bölüm sayfalarında **0.0 mm taşma** ve **%100.0 doluluk** teyit edilmeden iş teslim edilmiş sayılamaz.

---

## KRİTİK KURAL 14: Modern Levha, Sened/Şema, Anlam Gruplu Kelime Çevirisi ve Ferah Mizanpaj Standardı (Tüm Dersler İçin Kalıcı Mimari)

Arapça nass/metin içeren dersler (Hadis, Arap Dili ve Edebiyatı, Tefsir, Fıkıh, Kelâm vb.) ile şema/kavram odaklı tüm normal derslerde okuyucuyu yormayan, görsel hiyerarşisi net ve pedagojik olarak kolaylaştırıcı aşağıdaki **8 Mimari Standart** kalıcı olarak uygulanır (Referans uygulama: `3-sinif/1-donem/vize/src/hadis_3.py`):

1. **Standart Râvi / Aktör / Kavram Kutuları ve Ok Üstü Bağlantı Lafızları (`_svg_rich_card` & `_svg_lafiz_badge`):**
   - Sened ve akış şemalarındaki her kutuda aynı sabit hiyerarşi uygulanır: **1) Arapça İsim / Kavram → 2) Türkçe İsim → 3) Nesil ve Tabaka / Kategori Bilgisi → 4) Varsa Ortak Râvi (`ORTAK RÂVİ · MEDÂR`) veya Konum Etiketi (`Sahâbî Râvi`, `Merfû Nass`, `Musannif`)**.
   - Tekrarlayan uzun biyografiler veya genel sîga açıklamaları küçük kutuların içine sıkıştırılmaz; ayrı tanıtım kutusunda (`Person`) veya Sayfa 3'teki ortak okuma rehberinde tutulur. Böylece kutu içi yazılar büyük, net ve okunaklı kalır.
   - **Tariklerin Renk Tutarlılığı ve Ortak Râvi Vurgusu:** Çok tarikli/kollu şemalarda her yol birleşme noktasına kadar kendi rengiyle (`#6d4626` kahverengi, `#1d615c` çini yeşili, `#694f73` mürdüm) ilerler; yolların birleştiği kavşak noktası kalın kehribar çerçeve (`#b87b14`) ve **`ORTAK RÂVİ · MEDÂR`** rozetiyle vurgulanır. Aktarım lafızları (<bdi class="ar">حَدَّثَنَا</bdi>, <bdi class="ar">أَخْبَرَنَا</bdi>, <bdi class="ar">عَنْ</bdi>, <bdi class="ar">سَمِعْتُ</bdi>, <bdi class="ar">وَقَالَ</bdi>) doğrudan okların üzerinde gösterilir.

2. **Anlam Gruplu ve Ton Farklı Kelime Kelime Çeviri (`_w(ar, tr, g)` & `.w-token.tone-1/2/3`):**
   - Kelime kelime çeviri levhalarında (`❷ METİN` / `_hadis_board`, `_nass_board`) Arapça kelime/ibare ile Türkçe karşılığı aynı küçük kart biriminde (`.w-token`) tutulur.
   - Cümleyi oluşturan kelime birimleri tek tek kopuk bırakılmaz; anlam grupları (cümlecikler/terkipler) hâlinde `g=1, 2, 3` parametresiyle sağdan sola **hafif arka plan ton farklarıyla** (`.tone-1` ferah krem, `.tone-2` sıcak parşömen, `.tone-3` hafif çini tonu) gruplandırılır.
   - Kelime kartlarının hemen altında **`BÜTÜNCÜL MEAL`** şeridi ayrı ve belirgin olarak yer alır.

3. **Bâb ve Bölüm Başlıklarında Üçlü Kademe ve «Bâb–Hadis Bağlantısı» (`.bab-board`):**
   - Bâb ve ana nass başlıklarında: 1) Üst sağda iri puntoyla tam Arapça başlık (`.bab-full-ar`), 2) Ortada anlam gruplu kelime karşılıkları, 3) Altta kalın ve belirgin **`BÂB TERCÜMESİ`** ile onun altında özlü **`BÂB–HADİS BAĞLANTISI`** açıklaması yer alır. Başlık, tercüme ve açıklama birbirine karışmaz.

4. **Standart «USÛL», «ANLAM» ve «DİKKAT» Açıklama Kutuları (`_mukayese_box`):**
   - Ders ve nass açıklamaları tekdüze paragraflar yerine; **`USÛL`** (sened/metodoloji, `#6d4626`), **`ANLAM`** (fıkıh/kelâm/mesaj, `#1d615c`) ve **`DİKKAT`** (sınav uyarısı/kavram farkı, `#8c2f21`) rozetleriyle sınıflandırılır.
   - Maddeler arasında ince kesik ayırıcı çizgi (`border-bottom: 0.5px dashed`) ve ferah dikey boşluk bırakılır; aynı bilgiyi tekrar eden kutular birleştirilir.

5. **İçindekiler ve Kavramlar Sözlüğü Altına Tablo Ekleme Yasağı & Kapsamlı Tam Sayfa Sözlük Kuralı:**
   - **Footer Tablo/Kutu Yasağı:** İçindekiler sayfasının (s. 3) ve Kavramlar Sözlüğünün (s. 14) altına kesinlikle tablo, levha rehberi veya mukayese kutusu (`toc_footer_html`, `glossary_footer_html`) YERLEŞTİRİLMEZ; bu sayfalar sade ve ferah bırakılır.
   - **Kapsamlı Tam Sayfa Sözlük Standardı:** Sözlük sayfası (s. 14), alt kutular olmaksızın tam sayfayı dolduracak şekilde; dersin tüm ünitelerini kapsayan **en az 18–22 kilit kavramla**, zengin tanımlar, BiDi izoleli Arapça asılları (`<bdi class="ar">«...»</bdi>`), bağlam etiketleri ve ilgili bölüm referanslarıyla (`N. Bölüm`) eksiksiz olarak hazırlanır.

6. **Test ve Çözümlü Cevap Anahtarında «Tekrar için: s. …» Yönlendirmesi (`.ans-page-ref`):**
   - Testte soru kökü ile seçenekler arasında rahat okuma boşluğu bırakılır.
   - Çözümlü cevap anahtarındaki her açıklamanın sonuna **`Tekrar için: s. …`** rozeti (`.ans-page-ref`) eklenerek öğrencinin yanlış yaptığı sorudan doğrudan ilgili konu sayfasına dönmesi sağlanır.

7. **Ferah Mizanpaj ve Kutu İçi Nefes Payı Disiplini (Sıkışıklık Yasağı):**
   - Kutuların, kartların ve tabloların üzerinde dış tepe çizgisi (`border-top` şeridi) kullanılmaz; sade, modern ve tam çerçeveli (`1px solid`) tasarım korunur.
   - Kutu içi dolgular (`padding`), satır aralıkları (`line-height: 1.28–1.38`) ve kartlar arası mesafeler (`gap`, `margin`) asla yazıları birbirine yapıştıracak kadar daraltılmaz; tüm sayfalarda **0 mm taşma** korunarak ferah ve göz yormayan bir okuma deneyimi sağlanır.

8. **Hadis Levhaları ve Materyallerin Boyut Dokunulmazlığı & Sayfa Genişletme Protokolü (5. ve Sonraki Haftalar Standardı):**
   - Hadis levhaları (`.mod-isnad-container`, `.mod-tree-svg`, `.hadis-board`, `.w-token`, `.w-ar`, `.w-tr`, `.mukayese-box` vb.) sayfaya sığdırmak amacıyla asla küçültülemez (`max-height: 52mm`, `0.94em`, `7.5pt` vb. yapay micro-font ve sıkıştırma kuralları KESİNLİKLE YASAKTIR).
   - Bir hadisin sened ağacı, Arapça metin satırları, kelime kartları ve tahlili tek sayfaya sığmıyorsa; levhaları küçültmek yerine içerik mantıksal olarak bölünür: **Usûl & Anlam tahlil kutusu bir sonraki sayfaya taşınır, yetmezse metin kısmı da sonraki sayfaya taşınır**.
   - Sayfa sayısı, çift taraflı baskı forma uyumu (`sayfa_sayisi % 4 == 0`) gözetilerek genişletilir (örn. 20 → 24 → 28 sayfa).
   - 5. hafta veya sonraki haftalarda yeni hadisler ve bâblar eklenirken de bu ferah mimari zorunludur; materyallerin boyutları daima tam standart ölçekte tutulur.


---

## KRİTİK KURAL 15: Okuma PDF Standardı (Yazılı Konu Anlatımı / Özet Mizanpajı)

Kullanıcı herhangi bir ders veya konu özeti için *"okuma pdf üret"*, *"[Ders Adı] okuma pdf'ini çıkar"* veya benzeri bir talepte bulunduğunda; asistan `tools/okuma_pdf.py` motorunu veya eşdeğer Playwright mimarisini kullanarak istisnasız aşağıdaki standartlara tam uyumla çıktı üretir (Referans model: `Arap Dili ve Edebiyatı V - Vize Sınavı Konu Özeti (Sarf-Nahiv ve Alıştırmasız).pdf`):

1. **Ön/Arka Sayfaların Sadeleştirilmesi ve Ders Kapağı Mimarisi:**
   - Ekranda ve mobilde kesintisiz okuma deneyimi sağlamak adına; boş sayfa, ayrı içindekiler sayfası ve 7. Bölüm gibi hızlı kontrol/sınav tabloları çıkarılır.
   - Her tekil Okuma PDF doğrudan 1 sayfalık **Seçenek 1 — Baskı Dostu Lüks** ders kapağı (`s. 1`, tıklanabilir ünite planı + yer imleri) ile açılır ve hemen ardından **1. Ünite** (`s. 2`) kesintisiz olarak başlar (`--kapaksiz` verilmediği sürece varsayılan standart budur).
   - İlk ünitede boş sayfa oluşmasını önlemek için `first-unit` sınıfı ve `break-before: avoid;` uygulanır; sonraki üniteler ise sayfa başından (`break-before: page;`) başlar.

2. **Dersin Tema Rengine Göre Ünite Levhaları (Unit Banners):**
   - Her ünite başında `cekirdek/renk_uretici.py` içindeki ders rengiyle uyumlu, degrade arka planlı, altın kenarlıklı ve ünite emojisi taşıyan lüks kart başlıkları (`.unit-banner-container`) yer alır.

3. **Tipografik Hiyerarşi & Rozet Standartları (İstisnasız İri ve Renkli Rozetleme):**
   - **Gövde Metni:** 9.8pt net font boyutu, 1.58 ferah satır aralığı.
   - **Evrensel Alt Başlık Rozetleri (H2/H3 Zorunluluğu):** Yazar ister `## 1.1.` ister `### 1.1.` ister `## A)` yazsın; motor bunu otomatik olarak yakalar ve dersin kurumsal renginde degrade rozetli (`.h2-badge`, örn. `1.1`, `1.2`), alt çizgili lüks başlığa dönüştürür. Çıplak ve rozetsiz alt başlık üretimi KESİNLİKLE YASAKTIR. Alt başlıklara bağlı ikincil başlıklar da kehribar şeritli ve soft zeminli lüks kutu başlık (`.h3-styled`) olarak tanzim edilir.
   - **Kavram ve Istılah Hap Kutuları (`.badge-tr` & `==kavram==`):** Önemli terimler, şahıslar, eserler, kurumlar, ekoller ve sınav anahtar kelimeleri kuru düz metin bırakılamaz. Yazar ister doğrudan `==kavram==` sözdizimini ister `<span class="badge-tr">` etiketini kullansın; terimler dersin resmi tema renginden türeyen 3px sol şeritli, pastel zeminli lüks hap kutucuk (`.badge-tr`) içine alınmak zorundadır (Din Eğitimi standardı).
   - **Özel Liste İmleri:** Standart madde noktası yerine kurumsal renkte kare imler (`▪`) kullanılır.

4. **Arapça ve Nass Tipografisi (%128 İrilik, Renkli Rozetler & BiDi İzolasyonu):**
   - **Renkli Arapça Rozetler (`<code class="ar">` & `«...»`):** Metin, liste ve tablolarda geçen tekil veya kısa Arapça kavramlar/ıstılahlar (`«...»`, `` `...` ``, `<bdi>`), ders rengi zeminli (`c_pill_bg`), sağdan 3px ders renkli şeritli (`theme_hex`), zarif bordürlü, hafif gölgeli ve `Amiri` fontlu **renkli Arapça hap rozet** (`<code class="ar" dir="rtl"><bdi>...</bdi></code>`) olarak otomatik render edilir. Çıplak veya şeffaf bırakılamaz.
   - **Bütünleşik Nass Levhaları (`.nass-board` Zorunluluğu):** Âyetler, hadisler ve klasik metin tahlilleri satır içi metinlere veya çıplak listelere sıkıştırılamaz. Tefsir III ve Sistematik Kelâm modellerinde olduğu gibi; ders renkli başlık rozeti, iri ve harekeli Arapça nass (`1.28em`, `Traditional Arabic / Amiri`), BiDi izolasyonu ve altında Türkçe meal/şerh kutucuğu (`.nass-trans-box` / `.nass-meal-box`) içeren lüks `.nass-board` mimarisiyle sunulur. Sınav dipnotları ise kehribar/altın vurgulu ve `📌 KİTAP DİPNOTU & SINAV UYARISI` etiketli kutularda (`.callout-pinned`) verilir.

5. **Sıkı Tipografi, Doğal Metin Akışı ve Sayfa Tasarrufu:**
   - **Beyaz Nehirleri Önleme (`text-align: left`):** Satır aralarında ve kelimeler arasında yapay boşluklar/yırtılmalar oluşturan `text-align: justify` kesinlikle kullanılmaz; doğal ve dengeli sol hizalama uygulanır.
   - **Sıkı Aralıklar (Sıfır Sayfa İsrafı):** Bilgi veya cümle silinmeden; paragraflar `margin-bottom: 7.5px`, listeler `3.5px`, satır yüksekliği `1.50–1.56` tutularak yapay sayfa uzamaları engellenir ve kompakt/dolgun sayfa düzeni sağlanır.

6. **Tablo Tasarımı & Sayfa Altlıkları:**
   - Tablolar ders renkli degrade başlıklı, altın ayırıcı çizgili ve zebra desenli okunaklı hücrelerle tanzim edilir.
   - Her sayfanın üstünde ders adı ve kapsam bilgisi; altında ise şık sayfa numarası kapsülü (`Sayfa X / Toplam`) yer alır.

7. **Çift Konum Senkronizasyonu & Tek Seferde Üretim:**
   - Asistan, kullanıcıdan yeni bir komut veya hatırlatma beklemeden doğrudan `python tools/okuma_pdf.py <slug> --sinif X --donem Y --sinav Z` motorunu çalıştırır.
   - Üretilen PDF doğrudan hem `ders_anlatimlari/<DERS ADI>/` altına hem de `kaynaklar/özetlenmiş_dersler/<DERS ADI>/` altına otomatik olarak senkronize edilir.

8. **Seçici ve Bağlamsal Pedagojik Materyal İlkesi (Şablon Dayatma Yasağı & Zengin Vektörel Anlatım):**
   - Okuma PDF dokümanlarında terminal tarzı ham ASCII şemalar (`+-----+`, `|`, `->`) bırakılamaz; bunların yerine dersin resmi kurumsal rengini otomatik alan modern HTML/CSS lüks kart ve şema modelleri kullanılır.
   - **Zorunluluk Yasağı:** Hiçbir derse sırf şekil olsun diye yapay şema dayatılamaz. Materyaller yalnızca anlatımı berraklaştıran, karşılaştırma veya hiyerarşi gerektiren kritik konularda seçici olarak kullanılır.
   - **Evrensel 12 Materyal Kütüphanesi (`tools/okuma_pdf.py`):**
     1. *Barem Skalası* (`.spectrum-bar`, `.certainty-scale-bar` - Kanaat, Hüküm veya Sıhhat dereceleri)
     2. *Hiyerarşik Değerler Piramidi* (`.concept-pyramid` - İbn Rüşd insan tipleri, Makāsıd, Müdahale basamakları)
     3. *Kavram Anatomisi Matrisi* (`.entity-matrix-wrap`, `.entity-grid-2/3/4` - 2'li, 3'lü, 4'lü kavram kartları)
     4. *Doktrin ve Ekol Karşılaştırma Levhası* (`.doctrine-compare-wrap` - Mezhep ve fikir münazaraları)
     5. *Ontoloji ve Sınıflandırma Ağacı* (`.ontology-card-wrap` - Varlık sahası, İlimler ağacı)
     6. *Döngüsel / Çevrimsel Süreç Modeli* (`.cycle-flow-wrap` - İbn Haldun 5 tavır döngüsü, İletişim döngüsü)
     7. *Süreç ve Oluşum Akış Zinciri* (`.formation-flow` - Hudûs akışı, Hüküm oluşumu)
     8. *İsnad Akış Şeridi* (`.isnad-flow-strip` - Râvi tabakaları, mütâbaat ve şâhid zincirleri)
     9. *Formül ve Küllî Kaide Kartı* (`.formula-card` - Varlık eşitlikleri, Fıkhî küllî kaideler, Ben Dili formülü)
     10. *Tarihsel Dönemler Zaman Çizelgesi* (`.timeline-bar` - Kurumsal evrim, Islahat kronolojisi)
     11. *2x2 Eksen Matrisi* (`.axis-matrix-2x2` - Liderlik ve yönetim stilleri)
     12. *Tefsir III Modeli Kurumsal Renkli Nass Levhaları* (`.nass-board` - Degrade zeminli, iri hatlı ve bütünleşik tercümeli nass paneli)
     13. *Hiyerarşik Ağaç Şeması* (`.tree-diagram-wrap` - Sosyal yapı, hanedan şeceresi, idarî ve hukukî sınıflandırma ağacı).

9. **Materyal Tasarımında Sıfır Bilgi Kaybı & Çift Katmanlı Mimari Standardı (Materyal + Tam ve Eksiksiz Konu Anlatımı):**
   - Görsel materyaller (şemalar, zaman çizelgeleri, akış kartları, hiyerarşik ağaçlar vb.) tasarlanırken kavramlar özetlenip kompakt kartlara dönüştürülebilir; **ANCAK hiçbir sınav bilgisi, fıkhî ayrım, ıstılah, âyet/hadis metni, isim, eser veya tarihsel detay atlanamaz veya eksiltilemez.**
   - **Çift Katmanlı Kural (Zorunlu):** Ya tüm detaylar doğrudan materyalin içine tam ve eksiksiz olarak yazılır YA DA (ferahlık ve estetik için tercih edilen yöntem) materyalin hemen altında `### ... Tam ve Eksiksiz Konu Anlatımı:` başlığı açılarak konunun tüm detayları, maddeleri ve tahlilleri eksiksizce yazıya dökülür.
   - Görsel materyaller tek başına kuru bir özet olarak bırakılamaz; altındaki konu anlatımı asla budanamaz veya atlanamaz. Öğrenci hem görsel şemadan konunun haritasını görmeli, hem de altındaki metinden sınavda çıkacak tüm ayrıntıları eksiksizce okuyabilmelidir.

---

## KRİTİK KURAL 16: Okuma PDF Ders Kapağı ve Birleşik Okuma Kitapçığı Ana Kapak Standardı

Bundan sonra üretilecek Final ve diğer tüm dönem **tekil Okuma PDF'leri** (`tools/okuma_pdf.py`) ile **Birleşik Okuma Kitapçıkları** (`tools/okuma_birlestir.py`) istisnasız aşağıdaki standart kapak mimarisi ile üretilir:

1. **Tekil Okuma PDF Ders Kapağı (`Seçenek 1 — Baskı Dostu Lüks`):**
   - `tools/okuma_pdf.py` varsayılan olarak her ders PDF'inin başına `tools/okuma_birlestir.py` içindeki paylaşımlı şablonla (`render_single_course_cover_html` + `attach_course_cover_links`) 1 sayfalık Baskı Dostu Lüks kapak ekler.
   - Kapak tasarımı: Beyaz baskı dostu zemin üzerinde çift çizgili zarif dış/iç çerçeve, altın-tema köşe süsleri, sağ üstte renkli sekme (`01`), üstte dersin `cekirdek/renk_uretici.py` tema renginden degrade banner, sağda dersin ruhuna özgü altın halkalı vektörel SVG simge (`_course_svg_icon`), 3'lü metrik şeridi (`Ünite / Konu`, `İçerik Sayfası`, `Sayfa Aralığı`), **tıklanabilir `LINK_GOTO` ünite/konu planı**, sayfa numaralı altlık ve PDF yer imi (outline/TOC) içerir.
   - Kapak üzerindeki sınav etiketi döneme göre dinamik üretilir (`VİZE SINAV HAZIRLIĞI` / `FİNAL SINAV HAZIRLIĞI`, `Vize Özeti · ...` / `Final Özeti · ...`).

2. **Birleşik Okuma Kitapçığı Ana Kapağı (`Seçenek 1 — Tam Vektörel Prestij`):**
   - Bir dönemdeki okuma PDF'leri `python tools/okuma_birlestir.py --sinif X --donem Y --sinav Z` ile tek ciltte birleştirildiğinde ana kapak (`s. 1`) daima **Tam Vektörel Prestij** şablonuyla üretilir (koyu lacivert degrade zemin, ince İslâmî kemer-daire kafes dokusu, altın köşe bezemeleri).
   - **İslâmî Ana Amblem Zorunluluğu (`_main_cover_emblem_svg`):** Ana kapak sağ üst amblemi **hilâl ve çift minareli kubbeli cami** İslâmî motifidir. Usturlap (Felsefe dersi ikonuyla çakışan) veya altı köşeli üst üste kare yıldız figürü KESİNLİKLE KULLANILMAZ.
   - **Dinamik Başlık:** `{SINAV} SINAVI HAZIRLIK KİTABI` (`VİZE` veya `FİNAL`), dönem kapsülü (`X. SINIF · Y. DÖNEM · {SINAV} · İLAHİYAT OKUMA KİTABI`) otomatik uyumlanır.
   - **Ayrı İçindekiler Sayfası Yoktur:** Ana kapakta tüm derslerin sayfa aralığı ve tıklanabilir `LINK_GOTO` kartları bulunduğu için ayrıca bir İçindekiler sayfası konmaz.
   - **Çift Taraflı Baskı (Duplex) ve Çift Kapak Önleme:** `s. 1` Ana Kapak, `s. 2` Boş Sayfa (yalnızca boş kalır, yazı/kutu eklenmez), her ders kapağı tek (sağ) sayfada başlar (`c.cover_page % 2 == 1`). Tekil okuma PDF'lerinde hâlihazırda Baskı Dostu Lüks kapak varsa `_pdf_has_baski_lux_cover` ilk sayfayı otomatik atlar ve çift kapak basılmasını engeller; tüm içerik altlıkları global sayfa numarasına (`Sayfa X / Toplam`) yenilenir.


