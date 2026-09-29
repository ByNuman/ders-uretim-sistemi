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

### 5. Standart: Kelime ve Font Büyüklüğü Hiyerarşisi (2026-09 Ölçeği)
- **Arapça ve Harekeli İbareler (`bdi`, `.ar`, `[dir="rtl"]`):** Harekelerin net seçilebilmesi için `%125` daha büyük (`font-size: 1.25em`) ve çakışmayı önlemek için ferah satır aralığıyla (`line-height: 1.68`) render edilir.
- **Türkçe Gövde:** Gövde metinleri 9.35pt, tablo hücreleri 8.65pt, kutu metinleri 9.15pt, sözlük tanımları 8.75pt.

### 6. Standart: Yenilenen Test Sistemi (Pedagojik Zorluk Piramidi)
- 20 soruluk test 3 kademeli piramide göre hazırlanır:
  - **1–6. Sorular (Kolay):** Doğrudan kavram, terim ve isim bilgisi.
  - **7–14. Sorular (Orta):** Karşılaştırma, usûl tahlili, sebep-sonuç ilişkileri.
  - **15–20. Sorular (Zor):** Öncüllü sorular (Roman rakamlı `I, II, III`), olumsuz soru kökleri ve Arapça ibare çözümlemeleri.
- **Sayfa Mimarisi:** Test tam **2 sayfaya (10 + 10 soru)** dengelenir.
- **Çözümlü Cevap Anahtarı:** Tam **1 sayfaya** sığdırılır. Doğru şıkkın yanında analitik gerekçesi ve geçen Arapça ibarelerin `<span class="ans-trans">` Türkçe mealleri eksiksiz verilir.

### 7. Standart: Görsel Ekleme Kutuları (AI Görsel Yer Tutucuları)
- Her bölüme en az bir adet `add_block_gorsel(BulletBlock(...), baslik="AI görsel önerisi: <çizilebilir somut sahne>")` şablonuyla 4:3 oranında görsel çerçevesi eklenir.
- Öneri soyut veya belirsiz değil; tarihî sahneyi, el yazmasını veya sened şemasını somut tarif eden çizilebilir bir yönerge olmalıdır.
