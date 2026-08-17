---
name: ders-anlatim
description: Bir ders kaynağını (kaynaklar/ders_kaynaklari/) ya da öğretmenin dağınık/eksik dikte notlarını (kaynaklar/ogretmen_notlari/) fihristleyip bölüm bölüm, otomatik ve kesintisiz şekilde derinlemesine anlatır veya toparlar. Kullanıcı bir ders adı verip "anlat", "işle" veya "notlarımı toparla/düzenle" dediğinde devreye girer. Görsel PDF ders notu kitabı sisteminden bağımsızdır.
---

# Ders Anlatım Otomasyonu

Bu talimat seti, `ders-uretim-sistemi` projesine entegre bir alt sistemdir. Mevcut görsel PDF ders notu kitabı sisteminden **tamamen bağımsız** çalışır. Girdinin türüne göre iki farklı modu **otomatik olarak** seçer, ve her iki modda da nihai çıktı doğrudan bir **PDF** dosyasıdır:

- **Mod 1 — Kaynak Anlatımı:** elde tam bir kaynak/kitap/PDF varsa; kaynağa sıkı sadakatle, derinlemesine anlatır.
- **Mod 2 — Not Toparlama:** elde sadece öğretmenin yazdırdığı dağınık/eksik/hatalı notlar varsa; notları mantıklı sıraya koyar, akademik doğrusuyla tamamlar/düzeltir.

## Kurulum (bir kerelik)

Proje kökünde şu klasör yapısını oluştur:

```
kaynaklar/
├── ders_kaynaklari/     # Mod 1 girdisi: tam ders metinleri
├── ogretmen_notlari/    # Mod 2 girdisi: dağınık/dikte öğretmen notları
└── ders_ozetleri/       # mevcut görsel PDF sisteminin girdisi (değişmedi)

ders_anlatimlari/        # Mod 1 çıktısı: <ders adı>.pdf
calisma_rehberleri/      # Mod 2 çıktısı: <ders adı>.pdf
```

`.calisma/` adında gizli bir çalışma klasörü de kullanılır (bkz. "PDF Üretimi" bölümü) — bunu elle oluşturman gerekmez, sistem otomatik yönetir.

Var olan ham ders özeti dosyalarını `kaynaklar/` kökünden `kaynaklar/ders_ozetleri/` içine taşı. Bu dosyayı CLAUDE.md içinden referans verebilirsin (örn. "Ders anlatımı/toparlaması isteniyorsa `ders-anlatim-otomasyonu.md`'deki talimatları uygula").

## Tetiklenme ve Mod Seçimi

Kullanıcı sadece ders adını verir (örn. "Modern Felsefe Tarihi'ni anlat" veya "Hadis Usulü notlarımı toparla"). Sistem dosyanın hangi klasörde bulunduğuna bakarak modu otomatik seçer:

- `kaynaklar/ders_kaynaklari/` içindeyse → **Mod 1**
- `kaynaklar/ogretmen_notlari/` içindeyse → **Mod 2**

Her iki modda da süreç baştan sona **otomatik** ilerler — hiçbir aşamada kullanıcıdan "devam edeyim mi?" onayı istenmez.

## Bağlam (Context) Tazeliği — her iki mod için ortak kural

Uzun bir kaynağı/not yığınını tek oturumda birçok bölüm halinde işlerken, konuşma büyüdükçe Claude Code eski içerikleri otomatik olarak sıkıştırabilir veya özetleyebilir. Bu özellikle Mod 1'in "sadece kaynağa sadakat" kuralı için risklidir: kaynağın tam metni bağlamdan silinirse anlatım kaynaktan kayabilir.

Bunu önlemek için:

- **Her bölüm işlenmeden hemen önce, o bölüme karşılık gelen kaynak/not parçası dosyadan yeniden okunur.** Konuşma geçmişinde kaldığına güvenilmez, kaynak metin dosyadan taze çekilir.
- Fihrist ve Adım 1 analizinden çıkan derse özel ek kurallar, `.calisma/` taslağının en başına yazılır — böylece bunlar da diskte kalıcı olur, gerekirse oradan tekrar okunabilir.
- Bu basit "dosyadan taze oku" kuralı yeterlidir; bu ölçekteki bir görev için ayrıca subagent veya manuel /compact yönetimi kurmaya gerek yok.
- **Kullanım limiti veya oturum kesintisi yüzünden yarıda kalırsa:** yeni bir oturumda baştan başlama. `.calisma/<ders adı>.md` taslağı zaten kısmen doluysa, en son tamamlanmış bölümü tespit et, fihristten kalan bölümleri belirle ve kaldığın yerden devam et.

## PDF Üretimi — her iki mod için ortak

Anlatım/toparlama tamamlandıktan sonra, biriken taslak doğrudan işlenmiş bir PDF'e dönüştürülür — ara `.md` dosyası çıktı klasörlerinde **bırakılmaz**, sadece PDF kalır.

**Taslak akışı:** Bölüm bölüm üretilen içerik, nihai çıktı klasörlerine değil gizli bir çalışma dosyasına yazılır: `.calisma/<ders adı>.md`. Bu hem kesintiye dayanıklılığı sağlar (yarıda kalırsa buradan devam edilir) hem de PDF'e çevrilmeden önceki ham içeriktir. Tüm bölümler bitince bu taslaktan PDF üretilir; ardından taslak ve varsa ara `.docx` dosyası silinir.

**Görsel stil (kullanıcının paylaştığı referans PDF'e göre belirlendi):**
- Sayfa: A4, tek sütun, renk/tema yok (siyah-beyaz, sade akademik görünüm)
- Gövde metni: Times New Roman, ~11-12pt
- Bölüm başlıkları ("Bölüm N: ..."): kalın, büyük punto; her bölüm **yeni bir sayfada** başlar
- Alt başlıklar (1. ..., 2. ... gibi numaralı bölümler): kalın, orta punto
- Anahtar terimler ve önemli kelimeler: kalın
- Doğrudan alıntılar: blockquote kutusu değil, düz metin içinde italik
- 🔑 Anahtar Kavramlar Sözlüğü / Terim Açıklamaları, ⚠️ Kritik Odak / Dikkat-Püf Noktası, 💡 Bölüm Özeti / Kritik Çıkarım: emoji + kalın başlık aynen korunur
- Tablolar: sade, kenarlıklı, başlık satırı kalın — süsleme yok
- Üstbilgi, altbilgi, sayfa numarası yok

**Teknik yöntem:** `python-docx` ile yukarıdaki stile uygun bir `.docx` oluştur, ardından `docx2pdf` paketiyle (Windows'ta Word'ü COM üzerinden kullanarak) PDF'e çevir. Bu yöntem, referans PDF'in zaten Word ile üretilmiş olmasından dolayı emoji ve fontların birebir aynı görünmesini garanti eder — özellikle emoji ikonları (🔑 ⚠️ 💡) düz PDF kütüphaneleriyle (reportlab, fpdf2 vb.) doğru render edilemeyebilir, Word/docx2pdf yolu bunu bypass eder. Gerekli paketler kurulu değilse `pip install python-docx docx2pdf --break-system-packages` ile kur. Word veya `docx2pdf` çalışmazsa yedek yöntem olarak `soffice --headless --convert-to pdf` (LibreOffice) kullanılabilir.

Nihai `.pdf` dosyası ilgili çıktı klasörüne (`ders_anlatimlari/` veya `calisma_rehberleri/`) `<ders adı>.pdf` adıyla kaydedilir; ara `.docx` ve `.calisma/` içindeki taslak silinir.

---

## MOD 1: Kaynak Anlatımı

### 1. Kaynak Analizi (sessiz — çıktıya yazılmaz)

Kaynak metni oku ve kendi kendine belirle:

- Metin hangi disipline ait? (tarih, felsefe, fıkıh, hadis, tefsir, dil bilgisi, vb.)
- Metnin ana iskeleti neyin üzerine kurulu?
- Disipline özgü ek yapısal araç gerekir mi? Örnekler:
  - **Tarih** → dönemleri zaman çizelgesi (timeline) formatında ver
  - **Fıkıh** → farklı mezhep/görüşleri hüküm karşılaştırma tablosunda ver
  - **Hadis** → isnad zincirini (ravi sırasını) şema olarak göster
  - **Tefsir** → ayetin nüzul sebebini/bağlamını ayrı bir kutuda belirt
  - **Felsefe** → düşünürler arası görüş farklarını karşıt sütunlarda ver
  - Uygun örnek yoksa metnin yapısına göre kendi ek kuralını türet

Bu analizden çıkan 2-4 derse özel ek kural, Temel Kurallar'a ek olarak tüm bölümlerde uygulanır.

### 2. Fihrist Çıkarma
Metnin ana başlıklarından "Konu Omurgası" (fihrist) çıkar, `.calisma/<ders adı>.md` taslağının en başına kısa bir tanıtımla yaz.

### 3. Bölüm Bölüm Anlatım (otomatik, kesintisiz)
Fihristteki her bölümü sırayla işle, `.calisma/<ders adı>.md` taslağına ekleye ekleye ilerle; bölüm bitince otomatik olarak sıradakine geç.

### 4. Çıktı
Tüm bölümler bitince taslağı "PDF Üretimi" bölümündeki stile göre `ders_anlatimlari/<ders adı>.pdf` dosyasına dönüştür; taslağı ve ara dosyaları sil.

### Mod 1 Temel Kuralları

1. **Sadece Kaynağa Sadakat (genel ilke):** Anlatımın tamamı — olaylar, isimler, tarihler, örnekler, terim açıklamaları, yazarın argümanları — yalnızca kaynak metinde geçenlere dayanmalı. Kaynakta bulunmayan hiçbir dış bilgiyi ekleme.
2. **Derinlemesine ve Eksiksiz Çıkarım:** Hiçbir detayı atlamadan anlat.
3. **Arapça/Yabancı İbareler ve Etimolojik Çeviri:** Orijinal haliyle yaz, akademik çevirisini ve gerekirse etimolojik kökenini ekle.
4. **Kavram ve Terim Açıklamaları:** Yazar tarafından tanımlanmışsa parantez içinde belirt.
5. **Dikkat / Püf Noktası:** Kritik/karıştırılabilir noktaları "⚠️ **Dikkat / Püf Noktası:**" ile vurgula.
6. **Görselleştirme ve Tablolar:** Karşılaştırmaları tabloya, sebep-sonucu "A ➡️ B ➡️ C" okuna dönüştür.
7. **Önemli Alıntılar:** Kritik 1-2 cümleyi italik olarak ver.
8. **Yapı:** Kısa paragraf, kalın yazı, liste, hiyerarşik başlık.
9. **Kritik Çıkarım:** Alt başlık sonuna "💡 **Kritik Çıkarım:**" ekle.
10. **[Derse Özel Kurallar]** — Adım 1'de belirlenenler.

---

## MOD 2: Not Toparlama

### 1. Kaos Analizi (sessiz — çıktıya yazılmaz)

Dağınık notları oku ve belirle:

- Notlar hangi disipline/derse ait?
- Temel kavramlar ve ana temalar neler?
- Hangi konularda mantıksal kopukluk/yarım kalmış cümle var?
- Kaosu en iyi hangi yapısal şablon toparlar (kronolojik, sebep-sonuç, hiyerarşik)?
- Disipline özgü ek kural gerekir mi? Örnekler:
  - **Tıp/Biyoloji** → Semptom-Teşhis-Tedavi üçgenini netleştir
  - **Matematik** → formülleri LaTeX ile yaz, değişkenleri tanımla
  - **Tarih** → dönemleri zaman çizelgesi formatında ver
  - **Fıkıh** → hüküm karşılaştırma tablosu
  - Uygun örnek yoksa notların yapısına göre kendi ek kuralını türet

Bu analizden çıkan 2-4 derse özel ek kural, Temel Kurallar'a ek olarak tüm bölümlerde uygulanır.

### 2. Zihin Haritası ve Fihrist
Dağınık notlardan mantıklı bir "Konu Omurgası" kur — notların orijinal sırasına bağlı kalma zorunluluğu yok, doğru olan sırayı sen kur. `.calisma/<ders adı>.md` taslağının en başına yaz.

### 3. Bölüm Bölüm Toparlama (otomatik, kesintisiz)
Fihristteki her bölümü sırayla düzenle/tamamla, `.calisma/<ders adı>.md` taslağına ekleye ekleye ilerle; bölüm bitince otomatik olarak sıradakine geç.

### 4. Çıktı
Tüm bölümler bitince taslağı "PDF Üretimi" bölümündeki stile göre `calisma_rehberleri/<ders adı>.pdf` dosyasına dönüştür; taslağı ve ara dosyaları sil.

### Mod 2 Temel Kuralları

1. **Doğru Bilgiyi Metne Yedirme:** Yarım kalmış, eksik veya yanlış notları disiplinin akademik gerçekliğine uygun tamamla/düzelt; doğru bilgiyi akıcı ana metnin içine yaz. Eğer konu karıştırılmaya müsaitse veya kısa bir açıklama okuyucuya gerçekten fayda sağlayacaksa, aynı yerin altına bir alt satıra geçip **sadece bilgilendirici bir not** ekle — notlarda aslında ne yazdığından veya neyin/nasıl değiştirildiğinden **bahsetme**, editörlük sürecini okuyucuya yansıtma, sadece faydalı/açıklayıcı bilgiyi ver:
   `↳ ❓ *[sadece açıklayıcı/faydalı bilgi]*`
2. **Belirsizlik Kaçışı:** Orijinal not o kadar eksik/belirsiz ki güvenle tamamlanamıyorsa, uydurma yapma. Bunun yerine şu formatta işaretle:
   `❓ Belirsiz — bu kısım orijinal notlarda çok eksik, kontrol etmen önerilir.`
3. **Terimler ve Jargon Ayıklama:** Her bölümün başında "🔑 **Anahtar Kavramlar Sözlüğü**" ile terimleri kısaca tanımla.
4. **Format ve Düzenleme:** Uzun paragrafları madde imlerine böl; yazım/noktalama/anlatım bozukluklarını tamamen düzelt.
5. **Dağınıklığı Görselleştirme:** Süreçleri "A ➡️ B ➡️ C" akış şemasına, iç içe kavramları karşılaştırma tablosuna dönüştür.
6. **Odak Noktası Çıkarımı:** Tekrarlardan/yarım vurgulardan yola çıkarak kritik noktaları "⚠️ **Kritik Odak:**" ile vurgula.
7. **Özetleyici Kapanış:** Her bölüm sonuna "💡 **Bölüm Özeti:**" ile tek cümlelik özet ekle.
8. **[Derse Özel Kurallar]** — Adım 1'de belirlenenler.
