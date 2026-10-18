# AGENTS.md — Görsel Ders Notu Üretim Sistemi Kuralları

Bu dosya, Antigravity ve bu depoda çalışan tüm yapay zekâ asistanları için **bağlayıcı temel işletim kurallarını** içerir.
Detaylı sistem kılavuzu için ayrıca `CLAUDE.md` dosyasına bakınız.

---

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

## KRİTİK KURAL 7: Öğretmen İsimleri Ders Programındaki Resmî İsimlerle Birebir Yazılır & Görsel Notlarda İsim Yasağı
- **Yazılı Anlatımlarda Resmî İsim Zorunluluğu:** Yazılı ders anlatımı künyelerinde (`ders_anlatimlari/`) veya dönem planlama analizlerinde öğretim elemanı adı geçecekse; rastgele veya tahmini adlandırma yapılamaz. Doğrudan haftalık ders programındaki resmî unvan ve isim (ör. "Doç. Dr. Nevzat AYDIN", "Dr. Öğr. Üyesi Adem GÜNEŞ", "Öğr. Gör. Muhammed Salih SÜRÜCÜ") birebir esas alınır.
- **Görsel Ders Notlarında Hoca İsmi Kullanılmaz (KESİN YASAK):** Hocaların izni olmadan isimlerini görsel ders notlarında (`src/*.py` -> PDF / HTML) geçirmek kesinlikle yasaktır. Kapaklarda, açıklamalarda (`description`), soru köklerinde, çözümlü test cevap anahtarlarında (`AnswerItem`) veya arka kapaklarda hoca isimleri zikredilmez; yalnızca "ders anlatımında", "ders içi sınav yönergesinde" gibi pedagojik ifadeler kullanılır.

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
- **Türkçe Gövde:** Gövde metinleri 9.35pt, tablo hücreleri 8.65pt, kutu metinleri 9.15pt, sözlük tanımları 8.75pt.

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
- **Tipografik İrilik ve Sıfır Mikro-Metin Kuralı (Küçük Kutu Okunabilirlik Standardı):**
  - Görsel kutusu sayfa sağında kompakt bir çerçevede (`~75x56 mm`) yer aldığından, görsel içine minik paragraflar, madde işaretli küçük açıklamalar, ayet mealleri ve yan metinler koymak **KESİNLİKLE YASAKTIR** (küçüldüğünde okunaksız karınca yazısına dönüşür).
  - Açıklamaları öğrenci zaten sol taraftaki ders metninden okur. Görselin yegâne gayesi; zihinde hiyerarşiyi, sacayağını veya karar akışını **iri, kalın, net ve ferah 1–3 kelimelik kavram kutuları ve akış oklarıyla** tek bakışta canlandırmaktır.
  - Promptlarda modele: *"Extremely minimalist and uncluttered composition. Bold and large legible typography. Absolutely NO small paragraphs, NO bullet points, NO tiny explanatory text. Only 3 to 5 prominent, large Turkish concept labels (1-3 words each), clean boxes and flow arrows. High contrast, maximum readability at small box scale"* talimatı zorunlu olarak verilir.
- **Görsel İçi Dil Kuralı (Türkçe ve Arapça Zorunluluğu):**
  - Görsel üzerindeki tüm şema başlıkları, kutucuklar ve kavram etiketleri **kesinlikle Türkçe** olacaktır (İngilizce etiket kullanımı kesinlikle yasaktır).
  - **Arapça Dersleri İstisnası:** Arap Dili ve Edebiyatı (Sarf, Nahiv, Belâgat vb.) derslerinde veya nass/terim odaklı şemalarda görsel içi metinler doğrudan **Arapça** (veya Türkçe-Arapça çift dilli) üretilebilir.
  - Promptlarda modele: *"All text labels and titles inside the infographic must be strictly in Turkish (or Arabic for Arabic courses); no English text labels"* talimatı zorunlu olarak verilir.
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

## KRİTİK KURAL 13: Vize Konu Anlatımı Görsel Ders Notu Üretim Standartları (Bütünleşik Model & Birleşik Kitap Hazırlığı)

Vize dönemine ait görsel ders notları, dönem sonunda tek bir ciltte birleştirilip öğrencilere ve çalışma gruplarına dağıtılacağından, her dersin aynı kurumsal prestijde ve sıfır hata toleransıyla üretilmesi zorunludur:

1. **İki Aşamalı Üretim Standardı (Yazılı Temel Zorunluluğu):**
   - Görsel ders notu üretilmeden önce, ilgili dersin tüm haftalık anlatımları ve resmî kaynakları analiz edilerek `ders_anlatimlari/<DERS ADI>/` altında **Kapsamlı Vize Konu Anlatımı Dokümanı** (.md ve .pdf) hazırlanır. Yüzeysel özetleme kesinlikle yasaktır; nasslar, fıkhî tahliller ve akademik tartışmalar eksiksiz işlenir.
   - Görsel ders notu (`src/<ders>.py` -> `build.py`), bu sağlam yazılı dokümana dayanarak inşa edilir.
2. **Esnek Sayfa Mimarisi ve Sayfa Sınırı Yoktur:**
   - Vize notları katı bir 20 sayfa kalıbına sıkıştırılamaz. Dersin 7 haftalık müfredatı ve nass yoğunluğu gerektiriyorsa sayfa sayısı 20, 24, 28, 30 veya daha fazla sayfa olabilir.
   - Temel hedef: Konuların hiçbir detayı atlanmadan tam kavranması, çift taraflı kitap baskısına (forma uyumu) uygun olarak sayfa sayısının ÇİFT olması ve her sayfada **0.0 mm taşma ile %90–100 doluluk** sağlanmasıdır.
3. **Mevcut Vize Notlarının Korunması ve Genişletilmesi:**
   - Üretilen vize modülleri silinmez; sınav dönemine kadar yeni haftalar (5, 6, 7. haftalar) işlendikçe mevcut dosya üzerine yeni bölümler eklenerek genişletilir.
4. **Tipografik Hiyerarşi, BiDi İzolasyonu ve Okunabilir Punto:**
   - Gövde metinleri 9.15–9.35pt, tablo hücreleri 8.65pt, kutu metinleri 9.15pt, sözlük tanımları 8.15–9.1pt, test soruları 7.85–8.1pt, cevap anahtarı 8.0pt standardında tutulur.
   - Arapça harekeli metinler %128–130 ölçek ve `line-height: 1.68` ile büyütülür; daima `<bdi class="ar">` ile çift yönlü BiDi izolasyonuna alınır.
   - Parantez yönü kuralı: Daima önce Türkçe terim, ardından parantez içinde izole Arapça metin (`(<bdi class="ar">...</bdi>)`) verilir.
5. **Dört Bileşenli Zenginleştirilmiş Sözlük:**
   - Kuru kelime tanımları yerine; konunun **Kavramları, Kurucu Şahsiyetleri, Klasik Kütüb-i Usûl Eserleri ve Tarihî Yapı/Mekânları** dengeli ve doyurucu bir şekilde tanzim edilir.
6. **Sınav Kalitesinde 20 Soruluk Test & Çözümlü Cevap Anahtarı:**
   - Boşluk doldurma / cümle tamamlama, olumsuz kökler (değildir / söylenemez / bağdaşmaz), kavram/ekol eşleştirmeleri ve `I, II, III` öncüllü akademik sorular dengelenir.
   - Şıklar eşit hacimde tutulur, parantez içi Türkçe tüyo verilmez ve tam sayfa çözümlü cevap anahtarında Arapça terimlerin Türkçe mealleri (`.ans-trans`) verilir.
7. **Hoca İsmi Dokunulmazlığı:**
   - Görsel ders notlarında hocaların izni olmadan isimleri ve akademik unvanları asla zikredilmez.

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

5. **Sayfa 3 «Bu Levhalar Nasıl Okunur?» Rehberi (`CoursePack.toc_footer_html`) ve Sözlük Altı Karşılaştırma Tablosu (`CoursePack.glossary_footer_html`):**
   - İçindekiler sayfasının (s. 3) altındaki boş alan, **`toc_footer_html`** ile *"Bu Kitaptaki Sened ve Metin Levhaları Nasıl Okunur?"* (veya dersin şema okuma anahtarı) rehberi olarak değerlendirilir. Renkler, ok yönü, kesik çizgi, ortak râvi etiketi, tabaka numaraları ve anlam grupları burada topluca açıklandığından her sayfada tekrar edilmez.
   - Sözlük bölümünün son sayfasının altında **`glossary_footer_html`** ile birbirine karıştırılan kilit usûl kavramlarını (örn. *Medâr – Mütâbaat – Tahvîl – Ta‘lîk*) kitaptaki sayfa ve örnek numaralarıyla karşılaştıran özet tablo sunulur.

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
