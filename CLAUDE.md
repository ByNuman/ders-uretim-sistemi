# CLAUDE.md — Görsel Ders Notu Üretim Sistemi

Bu dosya, bu repodaki "Görsel Ders Notu Kitabı" üretim sistemini kullanarak
yeni bir ders işlerken Claude Code'un izlemesi gereken talimatları içerir.
Kullanıcı sana bir ders özeti (PDF/metin) verip "bunu görsel ders notuna
çevir" dediğinde, bu dosyadaki süreci baştan sona uygula.

## Sistemin amacı

Kullanıcı, üniversite derslerinin ham metin özetlerini (genelde 5-25 sayfalık
PDF'ler) alıp bunları tasarım açısından zengin, sınava hazırlık odaklı "Görsel
Ders Notu Kitabı" formatına çeviren bir üretim hattı istiyor: kapak, içindekiler,
genel bakış, numaralı bölümler (terim kutuları, kişi kartları, karşılaştırma
tabloları, akış şemaları, vurgu kutuları, bölüm özetleri), kavramlar sözlüğü ve
20 soruluk çoktan seçmeli test + çözümlü cevap anahtarından oluşan çok
sayfalı bir PDF.

Tasarım (HTML şablonu + CSS) sabittir ve zaten olgunlaşmıştır — **tasarımı
değiştirme, sadece içerik ekle.** Kullanıcı tasarımda bir sorun bildirirse
(kesilme, kontrast, taşma) o zaman `templates/style.css` veya
`templates/master.html.j2` üzerinde kalıcı bir düzeltme yap, çünkü bu dosyalar
TÜM derslerde paylaşılır.

## Dizin yapısı

```
ders_sistemi/
├── content_model.py       # Veri şeması (dataclass'lar) — API referansı aşağıda
├── build.py                # HTML üret → Playwright ile PDF'e render et → bookmark ekle
├── theme_engine.py         # Sınırsız renk teması motoru (tek hex'ten tam tema üretir)
├── kaynaklar/               # Kullanıcının ham ders özeti PDF'leri (bkz. Adım 0)
│   ├── sosyoloji-ozet.pdf
│   └── psikoloji-ozet.pdf
├── templates/
│   ├── master.html.j2      # Jinja2 şablonu (sabit — dokunma, sadece bug varsa düzelt)
│   └── style.css            # Tasarım sistemi (sabit — dokunma, sadece bug varsa düzelt)
├── content/
│   ├── __init__.py
│   ├── psikoloji.py         # Örnek: tamamlanmış bir ders (indigo tema, Test+Cevap Anahtarı formatı)
│   ├── sosyoloji.py         # Örnek (forest tema, Test+Cevap Anahtarı formatı)
│   ├── ogretim_teknolojileri.py  # Örnek (slate tema, LEGACY Sınav Hazırlık formatı)
│   ├── sanat_tarihi.py      # Örnek (burgundy tema, LEGACY Sınav Hazırlık formatı)
│   └── tefsir2.py           # Örnek: Arapça ayet içeren ders (add_ayat kullanımı, LEGACY format)
└── output/                  # build.py çıktıları buraya yazılır (.html + .pdf)
```

Her ders, `content/` altında kendi Python dosyasında yaşar ve tek bir
`get_pack() -> CoursePack` fonksiyonu dışa verir.

**Not — iki nesil örnek var:** `psikoloji.py`/`sosyoloji.py` GÜNCEL standardı
(Test + Cevap Anahtarı, sınırsız renk teması) kullanır; diğer 3 örnek henüz
eski "Sınav Hazırlık" (distinctions/match_table/qa_items) formatındadır ve
geriye dönük uyumluluk için bozulmadan çalışmaya devam eder (bkz. aşağıdaki
"Test + Cevap Anahtarı" ve "Renk Teması" bölümleri). **Yeni bir ders
yazarken her zaman psikoloji.py/sosyoloji.py'yi şablon alın, diğer 3'ünü
değil.**

## Uçtan uca iş akışı

Kullanıcı sana bir ders PDF'i / ham metni verdiğinde (ya da sadece bir ders
adı söylediğinde) şu adımları sırayla uygula:

### 0. Kaynağı bul: `kaynaklar/` klasörüne bak
Kullanıcı bir dosya eklemeden sadece bir ders adı söylerse (ör. "sosyoloji
dersini işle" veya "tarih özetini görsel not yap"), önce PDF/metin eklenip
eklenmediğini kontrol et; eklenmediyse **kullanıcıya sormadan önce**
`kaynaklar/` klasörünü tara:
```bash
ls kaynaklar/
```
Ders adıyla eşleşen (esnek eşleştir — büyük/küçük harf, Türkçe karakter,
"-özet"/"-ozet" gibi ekleri göz ardı ederek) bir dosya varsa onu kaynak
olarak kullan, kullanıcıya tekrar sorma. Eşleşen dosya yoksa kullanıcıdan
PDF'i ya sürükle-bırak yapmasını ya da `kaynaklar/` klasörüne koyup dosya
adını söylemesini iste.

`kaynaklar/` klasörü, kullanıcının ham ders özetlerini tek tek her seferinde
sohbete eklemek zorunda kalmadan biriktirdiği yerdir — dosya adı serbesttir
ama tutarlı bir kalıp (`<ders-slug>-ozet.pdf` gibi) aramayı kolaylaştırır.
İşlenen bir dersin kaynağını bu klasörden SİLME — kullanıcı ileride revizyon
isteyebilir.

### 1. Ham içeriği oku ve Arapça kontrolü yap
```bash
python3 -c "
import pdfplumber
with pdfplumber.open('kaynaklar/<bulunan-dosya>.pdf') as pdf:
    for i, page in enumerate(pdf.pages):
        print(f'=== SAYFA {i+1} ===')
        print(page.extract_text())
"
```
Metnin TAMAMINI oku (görme aracıyla dosyayı görüntüle, kesme). Arapça karakter
(ayet, hadis) varsa sorun değil — sistem `add_ayat()` ile bunu destekliyor
(bkz. aşağıdaki API referansı ve `content/tefsir2.py` örneği).

### 2. İçeriği 5-7 bölüme planla
Ham metnin doğal başlık yapısını takip et (uydurma bölümleme yapma). Her bölüm
için: 4 anahtar terim, en az 1-2 tablo veya blok, mümünse bir callout ve her
zaman bir bölüm özeti planla. Bölüm başına ortalama 2 sayfa hedefle (1-3 sayfa
arası kabul edilebilir) — çok yoğun bölümleri en baştan 2-3 `ChapterPage`'e
böl, tek dev sayfaya sıkıştırmaya çalışma.

### 3. `content/<ders_slug>.py` dosyasını yaz
Aşağıdaki "content_model.py API Referansı" bölümüne birebir uyarak yaz.
Mevcut derslerden birini (`content/sosyoloji.py` iyi bir orta-karmaşıklıkta
örnektir) şablon olarak kopyalayıp değiştirmek en hızlı yoldur.

Her ders için ayrıca:
- **Renk teması sınırsızdır**: `theme_color="#7A2438"` gibi TEK bir hex renk
  verin — `theme_engine.py` tüm tonları (kapak gradyanı, banner, tablo
  başlığı, kart kenarlığı vb.) otomatik türetir. Kolaylık için
  `theme_engine.PALETTE_HUES` içinde 16 hazır isimlendirilmiş ton var
  (`from theme_engine import PALETTE_HUES, generate_theme_vars` ile
  önizleyip hex'e çevirebilir ya da doğrudan `theme_color=` alanına
  istediğiniz herhangi bir hex'i yazabilirsiniz). Zaten kullanılmış
  renklere çok yakın bir ton seçmeyin — `content/` dizinindeki diğer
  dosyalara bakıp görsel olarak ayrışan bir renk seçin. `theme=` alanı
  (ör. `"forest"`) hâlâ zorunludur (geriye dönük uyumluluk ve `body`
  class'ı için) ama `theme_color` verildiğinde onun ürettiği renkler
  geçersiz kılınır — `theme=` için mevcut 5 isimden herhangi birini
  yazmanız yeterli, görsel sonucu etkilemez.
- `icon_text`: kapaktaki amblem harfi. **Tek bir Latin harf** kullan (dersin
  baş harfi gibi). Yunanca/özel semboller büyük punto boyutunda çarpık/tanınmaz
  görünüyor — kullanma. (İstisna: Psikoloji'de "Ψ" zaten kullanılıyor ve
  çalışıyor çünkü tek bir Unicode karakteri — asıl kural "tek karakter,
  karmaşık ligature değil" anlamına gelir.)
- `course_code`: üstteki kısa etiket. Başlıkla neredeyse aynı uzunlukta uzun
  bir ifade OLMASIN (örn. "ÖĞRETİM TEKNOLOJİLERİ" başlığın kendisiyle
  neredeyse özdeş olduğu için "ÖĞR. TEKNOLOJİLERİ" gibi kısaltılmalı).
- **Sınav bölümü artık Test + Cevap Anahtarı'dır** (LEGACY Sınav Hazırlık
  değil — bkz. aşağıdaki ayrı bölüm): 20 soruluk çoktan seçmeli test +
  her soru için çözümlü cevap anahtarı yazın.

### 4. Derle
```bash
cd ders_sistemi && python3 build.py content.<ders_slug>
```
Bu tek komut şunları otomatik yapar: HTML üretir → tutarlılık denetimi
(`validate()`: bölüm numaraları ardışık mı, sözlük referansları geçerli mi,
tekrar eden terim var mı) → Playwright ile PDF'e render eder → **her sayfanın
gerçek render yüksekliğini A4 sınırıyla karşılaştırır** → PDF'e gerçek
bookmark/outline ekler.

### 5. Taşma çıktısını oku — bu adım ASLA atlanmaz
Build çıktısı ya şunu verir:
```
[build] Taşma denetimi: tüm sayfalar A4 sınırları içinde. ✓
```
ya da:
```
[TAŞMA UYARISI] N sayfa A4 sınırını aşıyor -- içerik kesiliyor olabilir:
    - Sayfa (fiziksel sıra) X: ~Ymm taşma
```
Taşma varsa PDF'i sayfa numarasına göre PNG'ye çevirip (`pdftoppm -png -r 100
-f X -l X output/<slug>.pdf output/preview/pgX`) görme aracıyla incele, hangi
`ChapterPage`'in aşırı yüklü olduğunu belirle, o sayfanın içeriğini iki (gerekirse
üç) `ChapterPage`'e böl, yeniden derle. "✓" görene kadar tekrarla. Asla taşma
uyarısını görmezden gelip devam etme — bu, üretilen PDF'in sessizce içerik
kaybettiği anlamına gelir.

**Neden bu kadar sıkı?** Sayfalar `flex-direction:column` düzeninde ve
`overflow:hidden`. Eskiden tarayıcı, sayfa sınıra çok yaklaştığında elemanları
sessizce küçültüp taşmayı gizliyordu (`flex-shrink:1` varsayılanı) — bu da
banner ve kutuların içindeki metnin görünmeden kesilmesine yol açıyordu.
`style.css` içinde artık `.body-page > *` ve `.cover-top/.cover-bottom` için
`flex-shrink: 0` zorunlu kılınmış durumda — yani artık taşma her zaman
GERÇEK ve build çıktısında GÖRÜNÜR. Bu satırı asla kaldırma.

### 6. Görsel olarak baştan sona kontrol et
Taşma denetimi "✓" demiş olsa bile, en az şunları PNG'ye çevirip (100 DPI
yeterli) görme aracıyla tek tek kontrol et:
- Kapak (amblem, başlık, motif harfi çakışması var mı)
- İçindekiler (sayfa numaraları doğru mu)
- Genel Bakış
- Her bölümün İLK sayfası (banner subtitle'ı kesiliyor mu)
- En az bir tablo-ağırlıklı sayfa (başlık satırı okunur mu — özellikle ilk
  sütun, bkz. aşağıdaki "Bilinen tuzaklar")
- Sözlüğün SON sayfası (çok seyrek kalmış mı — 1-2 kavramlık yalnız bir sayfa
  kötü görünür; ders içeriğinden gerçek, ilgili birkaç kavram daha ekleyerek
  dengelenebilir — bkz. aşağıdaki not)
- Test'in SON sayfası (son soru düzgün bitiyor mu) ve Cevap Anahtarı'nın SON
  sayfası (LEGACY derslerde: Sınav Hazırlık ve varsa devam sayfaları)

Otomatik taşma denetimi "içerik kesiliyor mu" sorusunu cevaplar; görsel kontrol
"iyi görünüyor mu" sorusunu cevaplar — ikisi de gereklidir, biri diğerinin
yerini tutmaz.

### 6b. Sayfa denge kontrolü (boşluk dengeleme) — taşma kadar rutin bir adım
Taşma "✓" demiş olması sayfaların İYİ kullanıldığı anlamına gelmez — sadece
taşmadığı anlamına gelir. Bir sayfanın içeriği erken bitip altında büyük boş
alan kalması da ayrı bir kalite sorunudur (kağıt israfı, dağınık okuma
deneyimi). Bu yüzden HER ders build edildikten sonra (taşma denetiminin hemen
ardından, adım 6'daki görsel kontrolle birlikte) şunu yap:

1. Her bölümün TÜM fiziksel sayfalarını (özellikle `continue_tag`'li devam
   sayfalarını — ilk sayfalar genelde terms+person+block ile zaten dolu
   olduğundan asıl israf devam sayfalarında birikir) PNG'ye çevirip tek tek
   görme aracıyla incele.
2. İçeriğin sayfanın **yarısından önce** bittiği (altında sayfanın %50'sinden
   fazlası boş kalan) sayfaları işaretle — bunlar gerçek adaylardır. İçerik
   %55-70 civarında bitiyorsa bu normaldir, dokunma.
3. İşaretlediğin bir sayfa için, AYNI bölümün komşu bir sayfasından mevcut bir
   `.add_*()` bloğunu (bir `BulletBlock`, `ComparisonTable`, `FlowDiagram`,
   `KeyTerm` listesi...) o sayfaya taşı — asla yeni madde/callout/cümle UYDURMA
   ("doldurmak" için içerik icat etmek, taşma kadar ciddi bir hatadır, çünkü
   kaynakta olmayan bilgi üretmiş olursun). İki komşu sayfa da zaten orta
   doluluktaysa (~%60+) ve biri diğerine göre daha boşsa, aralarında içerik
   taşımak yerine o iki sayfayı TEK sayfada BİRLEŞTİRMeyi dene (bir
   `ChapterPage()` çağrısını tamamen kaldırıp içeriğini bir öncekine ekle) —
   bu, sayfa sayısını gerçekten azaltan tek yöntemdir.
4. Her denemeden sonra yeniden derle ve taşma çıktısını oku. Taşarsa (çoğu
   zaman taşar — pratikte denenen birleştirmelerin fazlası taşmayla
   sonuçlanıyor) değişikliği geri al ve sayfayı olduğu gibi bırak. Zorla
   sıkıştırmaya çalışıp elemanlar arası boşlukları (`gap`, `margin`) küçültme
   — tasarım sistemi sabit kalmalı.
5. Emin olamadığın (birleşince taşıp taşmayacağını kestiremediğin, ya da
   taşımanın başka bir sayfayı daha da seyrekleştireceği) durumlarda hiçbir
   şey yapma — mevcut boşluk seviyesini koru. Riskli bir "iyileştirme",
   iyileştirmemekten daha kötüdür.

Pratikte: bu kontrol çoğu zaman "temiz bir kazanç yok, olduğu gibi bırak"
sonucuna varır — bu BAŞARISIZLIK değildir, adımın kendisi zaten riskli
birleştirmeleri elemek için var. Sadece gerçekten güvenli (taşmayan, madde
icat etmeyen, komşu sayfayı yeni bir israf noktasına çevirmeyen) değişiklikleri
kalıcı yap.

### 7. Bookmark/link doğrulaması
```bash
python3 -c "
from pypdf import PdfReader
r = PdfReader('output/<slug>.pdf')
for it in r.outline:
    print(it.title, '->', r.get_destination_page_number(it)+1)
annots = r.pages[1].get('/Annots')
print(len(annots), 'link on TOC page')
"
```
Bölüm sayısı + 2 (sözlük + test — GÜNCEL formatta cevap anahtarı ayrı bir
outline girdisi daha eklerse de İçindekiler sayfasında hâlâ tek satır
olarak görünür, bkz. "Test + Cevap Anahtarı" bölümü) kadar TOC linki olmalı.

### 8. Teslim et
PDF'i kullanıcının erişebileceği çıktı konumuna kopyala ve sun.

## content_model.py API Referansı

```python
from content_model import (
    Person, KeyTerm, Callout, FlowStep, FlowDiagram, ComparisonTable,
    InfoCard, Ayah, BulletBlock, Chapter, ChapterPage, Concept, CoursePack,
    TestQuestion, AnswerItem,               # GÜNCEL sınav formatı — yeni derslerde bunları kullan
    QAItem, DistinctionPair, MatchRow,       # LEGACY sınav formatı — yeni derslerde KULLANMA
)
```

- **`Person(id, name, years, tagline, bio, key_work=None, initials=None)`**
  Bir düşünür/kişi kartı. `bio` bir liste ama sadece `bio[0]` render edilir —
  tek, dolu bir paragraf yaz. **Tek kaynak ilkesi**: bir kişinin
  tarihleri/eserleri sadece burada tanımlanır; sözlükte veya eşleştirme
  tablosunda o kişiden bahsedeceksen aynı bilgiyi elle tekrar yazma, bu
  nesneden türet.

- **`KeyTerm(term, definition)`** — bölüm başındaki 4'lü terim kutusu.
  Her `Chapter.key_terms` tam 4 eleman içermeli (tasarım 2x2 grid varsayar).

- **`Callout(kind, title, text)`** — `kind` ∈ `"focus"` (sarı/dikkat),
  `"caution"` (mavi/uyarı), `"insight"` (koyu lacivert/içgörü), `"route"`
  (mor/bölüm rotası). `text` içinde `<b>...</b>` kullanılabilir (HTML olarak
  render edilir, `| safe` filtresiyle).

- **`FlowStep(title, text="")`** ve **`FlowDiagram(steps, caption=None)`** —
  yatay ok'lu süreç şeması. 3-5 adım idealdir; fazlası dar sütunlara sıkışır.

- **`ComparisonTable(caption, headers, rows)`** — `rows`, her biri
  `len(headers)` uzunluğunda string listesi. Hücrelerde `<b>` kullanılabilir.
  2 veya 3 sütunlu tablolar en iyi sonucu verir.

- **`InfoCard(title, text, badge=None)`** — küçük 2-3'lü kart grid'i
  (`ChapterPage.add_info_cards(başlık, [InfoCard(...), ...])` ile eklenir).

- **`Ayah(reference, arabic, meal, etymology="")`** — bir ayet/hadis kartı.
  `arabic` RTL olarak, DejaVu Sans ile doğru şekillendirmeyle render edilir
  (Arapça glyph desteği bizzat görsel olarak doğrulanmıştır — harfler doğru
  bitişiyor, harekeler doğru yerleşiyor; tereddüt etmeden kullan).
  `ChapterPage.add_ayat(başlık, [Ayah(...), ...])` ile eklenir. Örnek kullanım
  için `content/tefsir2.py` dosyasına bak. Ham Arapça Unicode metni doğrudan
  `arabic=` alanına yaz — ekstra bir işlem gerekmez.

  > **Not:** Repoda `arabic_reshape.py` ve `fonts/ArabicExtracted-*.ttf`
  > dosyaları bulunur ama hiçbir yerden import edilmez — DejaVu Sans'ın
  > Chromium'daki native shaping'i (HarfBuzz) tek başına yeterli çıktığı için
  > kullanılmadan kalmış bir yedek/deneme. Bu dosyaları kullanmana gerek yok;
  > CSS zaten `font-family: "DejaVu Sans"` + `direction: rtl` ile doğru
  > sonucu veriyor.

- **`BulletBlock(number, title, bullets, subtitle=None)`** — numaralı
  alt-başlık + madde listesi. `bullets` içindeki her madde `<b>vurgu</b>`
  içerebilir. `number` alanı sayfa/bölüm içinde SIRALI olmalı (1, 2, 3…) —
  bir `ChapterPage`'e bölündüğünde numaralandırmayı elle takip et, bir blok
  ikiye bölünürse aynı numarayı kullanma (yanıltıcı olur, tek blok gibi
  görünsün istiyorsan tek `BulletBlock` olarak tut ve gerekirse bir sonraki
  sayfaya taşı).

- **`ChapterPage(continue_tag=None)`** — bir bölümün TEK fiziksel sayfası.
  Zincirlenebilir `.add_*()` metodları: `add_terms(list[KeyTerm])`,
  `add_person(Person)`, `add_person_row(list[Person])`, `add_block(BulletBlock)`,
  `add_callout(Callout)`, `add_flow(FlowDiagram)`, `add_table(ComparisonTable)`,
  `add_ayat(title, list[Ayah])`, `add_info_cards(title, list[InfoCard])`,
  `add_summary(text)`. İlk sayfa hariç her `ChapterPage`'e `continue_tag`
  ver — bu, sayfa üstündeki "N. Bölüm · Devam" rozetinin yanında görünen
  kısa başlıktır. **Kısa tut** (tek satırda kalsın, iki satıra sarılırsa
  rozetle hizası bozulur — ~40 karakterin altında tut).

- **`Chapter(number, title, subtitle, pages=[], key_terms=[])`** —
  `pages` listesine `ChapterPage` nesnelerini sırayla ekle. `key_terms`
  SADECE ilk sayfadaki 4'lü kutu için değil, aynı zamanda
  `concept_count()` gibi otomatik sayımlar için de kaynak.

- **`Concept(term, definition, context, chapter_ref)`** — sözlük satırı.
  `chapter_ref`, o kavramın geldiği `Chapter.number`'a eşit bir tam sayı
  olmalı (uydurma numara verme; `validate()` bunu denetler).

- **`QAItem(question, answer)`**, **`DistinctionPair(left, right, text)`**,
  **`MatchRow(key, detail, reference)`** — **LEGACY.** Eski "Sınav Hazırlık"
  bölümünün üç bileşeniydi. Yeni derslerde KULLANMAYIN — yerine
  `TestQuestion`/`AnswerItem` kullanın (aşağıda). Sadece geriye dönük
  uyumluluk için `content_model.py`'da duruyorlar; `pack.test_questions`
  boş bırakılırsa şablon otomatik olarak bu LEGACY formatı render eder.

- **`TestQuestion(number, stem, options)`** — **GÜNCEL sınav formatı.**
  `options` tam olarak `{"A": "...", "B": "...", "C": "...", "D": "...", "E": "..."}`
  biçiminde bir dict olmalı (4 veya 5 seçenek; `validate()` bunu denetler).
  `number` alanı 1'den başlayıp ardışık artmalı ve karşılık gelen
  `AnswerItem.number` ile birebir eşleşmeli.

- **`AnswerItem(number, correct, explanation)`** — `TestQuestion.number` ile
  eşleşen tek bir çözüm. `correct`, o sorunun `options` dict'indeki
  anahtarlardan biri olmalı (ör. `"C"`) — `validate()` bunu denetler.
  `explanation` içinde `<b>...</b>` kullanılabilir.

- **`CoursePack(...)`** — dersin tamamı. Zorunlu alanlar: `course_code`,
  `title` (HTML span içerebilir, örn.
  `'Sosyoloji<span class="accent-word">ye</span> Giriş'` — bir kelimenin
  bir kısmını altın renkte vurgulamak için), `subtitle`, `description`,
  `theme`, `icon_text`, `chapters`, `glossary`. Opsiyonel ama HER ZAMAN
  doldurulması gereken: `theme_color` (bkz. "Renk Teması" bölümü),
  `test_title`, `test_subtitle`, `test_instructions`, `test_questions`
  (20 soru önerilir), `answer_key_intro`, `answer_key_items`,
  `overview_lead`, `overview_cards` (tam 6 eleman — 3x2 grid), `overview_flow`
  (3-5 `(başlık, alt_metin)` tuple), `overview_note`. `distinctions`/
  `match_table`/`qa_items` LEGACY'dir, yeni derslerde boş bırakın.

## Renk Teması (sınırsız — `theme_engine.py`)

5 sabit tema (`indigo/burgundy/forest/slate/plum`) hâlâ çalışıyor, ama
YENİ derslerde bunlarla sınırlı kalmanıza gerek yok. `theme_engine.py`,
TEK bir hex renkten (`--accent`, `--accent-dark`, kapak gradyanı, `--paper`
zemin tonu dahil) tüm CSS değişkenlerini otomatik türetir — mevcut 5
temanın HSL değerleri geriye doğru analiz edilerek kalibre edilmiştir,
yani üretilen her yeni ton AYNI görsel kalite çizgisindedir.

```python
return CoursePack(
    ...,
    theme="forest",              # hâlâ zorunlu (body class için) — hangi isim olursa olsun fark etmez
    theme_color="#7A2438",       # VERİLİRSE theme='in ürettiği renkleri geçersiz kılar
    ...,
)
```

Hazır palet için (opsiyonel kolaylık):
```python
from theme_engine import PALETTE_HUES, generate_theme_vars, _hsl_to_hex
hue, sat, light = PALETTE_HUES["murdum"]
```
16 hazır isim: `cam-yesili, lacivert, bordo, antrasit, murdum, petrol, kahve,
kiremit, zeytin, indigo-koyu, celik-mavisi, gul-kurusu, turkuaz, visne,
hardal, orman-yesili`. Palet bir kolaylıktır, zorunlu değildir — dilediğiniz
herhangi bir hex'i doğrudan `theme_color=` alanına yazabilirsiniz.

**Dikkat:** 35-85° (sarı/sarı-yeşil) hue aralığında motor doygunluğu
otomatik kısar (yoksa "trafik konisi" gibi durur) — bu aralıkta biraz
"topraksı/hardal" bir sonuç almanız normaldir, bug değildir.

**Kontrast notu:** Sıcak (turuncu/kırmızı) hue'larda sabit altın vurgu rengi
(`--gold`) arka planla biraz düşük kontrastta kalabilir (bkz. kapak eyebrow
metni). Şimdilik bilinen bir sınırlama olarak kabul edin; çok sorun
oluyorsa o dersin hue'sunu birkaç derece kaydırmayı deneyin.

## Test + Cevap Anahtarı (sınav bölümü — GÜNCEL format)

`pack.test_questions` doluysa şablon otomatik olarak bu formatı render eder
(banner + 3'lü bilgi çubuğu "20 Soru / Çoktan Seçmeli / 5 Seçenek" + talimat
kutusu + numaralı sorular; ardından ayrı bir "Cevap Anahtarı ve Çözümler"
bölümü). 20 soru standarttır ama sayı serbesttir. Her soru 4 veya 5 seçenekli
olabilir. `content/sosyoloji.py` ve `content/psikoloji.py`'deki
`test_questions`/`answer_key_items` listelerini şablon olarak kullanın.

`pack.test_questions` boş bırakılırsa (yazmazsanız) şablon otomatik olarak
eski LEGACY "Sınav Hazırlık" formatına düşer — bu sadece 3 eski örnek
dersin (ogretim_teknolojileri/sanat_tarihi/tefsir2) bozulmadan çalışmaya
devam etmesi içindir. **Yeni bir ders yazarken her zaman `test_questions`/
`answer_key_items` kullanın, `distinctions`/`match_table`/`qa_items` değil.**

## `get_pack()` fonksiyonunun iskeleti

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from content_model import (...)

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
        ChapterPage(continue_tag="...")
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

## Sayfalama sabitleri (build.py)

```python
GLOSSARY_PER_PAGE = 18     # sözlük sayfası başına kavram (2 sütun x 9 satır)
QA_PER_PAGE = 10           # LEGACY — soru-cevap sayfası başına madde
DISTINCTIONS_PER_PAGE = 6  # LEGACY — ayrım kartı sayfası başına
MATCHTABLE_PER_PAGE = 9    # LEGACY — eşleştirme tablosu sayfası başına
TEST_PER_PAGE = 6          # test sayfası başına soru (2 sütunlu düzen, 5 seçenekli MCQ)
ANSWER_PER_PAGE = 16       # cevap anahtarı sayfası başına çözüm (2 sütunlu düzen)
```
Test ve Cevap Anahtarı bölümleri artık **2 sütunlu** düzende render edilir
(`templates/style.css` içinde `.tq-list`/`.ans-list` → `column-count: 2`,
`column-fill: balance`; her madde `break-inside: avoid` ile bir sütunda
bölünmeden kalır). Bu sayılar, tanım uzunluğu ortalama olduğunda güvenlik
paylıdır. Bir ders alışılmadık uzun soru/cevap metinleri kullanıyorsa yine de
`[TAŞMA UYARISI]` seni uyarır — o durumda sabiti küçültme, bunun yerine
görsel olarak sayfanın gerçekten sığıp sığmadığını kontrol et.
`TEST_PER_PAGE=6`, ilk test sayfasında (bilgi çubuğu + talimat kutusu
yüzünden daha az yer var) taşmayı önlemek için TÜM test sayfalarına
uygulanan tek bir sabittir — bu yüzden devam sayfalarında biraz boş alan
kalması normaldir (7 denendiğinde bazı derslerde ilk sayfa taştı, bkz.
"Bilinen tuzaklar" #7). Sözlüğün son sayfası kavram sayısı %20'nin altında
kalacak kadar seyrekse (örn. 20 kavram → 18+2), ders içeriğinden gerçek,
atlanmış birkaç kavram (önemli bir tarih, kişi, savaş adı vb.) daha
ekleyerek dengele — bu hem daha iyi görünür hem sözlüğü zenginleştirir.

## Bilinen tuzaklar / geçmişte düzeltilen buglar

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

4. **Uzun `continue_tag`**: İki satıra sarılırsa yanındaki rozetle dikey
   hizası bozulur. Kısa tut.

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

7. **`TEST_PER_PAGE` çok yüksek olursa ilk test sayfası taşar**: İlk sayfada
   banner + 3'lü bilgi çubuğu + talimat kutusu da olduğu için, devam
   sayfalarına göre daha az yer kalır. 2 sütunlu düzene geçildiğinde `8`
   denendi, bazı derslerde ilk sayfa taştı; `7`'de bile başka bir derste
   taştı; `6`'da üç ders de (Felsefe/Sosyoloji/Psikoloji) taşmadan geçti —
   bu yüzden sabit `6`'da tutuluyor (bkz. yukarıdaki "Sayfalama sabitleri").
   Yeni bir ders TEST_PER_PAGE'i global olarak değiştirmemeli — sabit zaten
   birden fazla dersin en sıkı senaryosuna göre kalibredir; sadece o dersin
   soru metinleri alışılmadık uzunsa yine de taşma çıkabilir, o zaman
   metni kısaltmayı düşün, sabiti değil.

8. **Test/Cevap Anahtarı 2 sütunlu düzen**: `column-count:2` ile CSS çoklu
   sütun düzeni kullanılıyor (CSS Grid değil) çünkü tarayıcı önce birinci
   sütunu doldurup sonra ikinciye geçiyor (`column-fill: balance` ile iki
   sütun dengeli yükseklikte kalıyor) — bu, gerçek bir sınav kağıdının okuma
   sırasına benzer. Her `.tq`/`.ans-item`'a `break-inside: avoid` şart,
   yoksa bir soru/cevap sütun sınırında ortadan bölünebilir.

## Tasarım sistemi özeti (referans amaçlı — değiştirmen gerekmemeli)

- Gövde fontu DejaVu Sans, başlıklar DejaVu Serif (kitap/akademik his).
- Her tema kendi `--accent`, `--accent-dark`, `--gold`, `--paper` (hafif
  tonlu, beyaz değil) setini tanımlar; callout renkleri
  (`focus/caution/insight/route`) tema-bağımsız sabittir. 5 sabit isimli
  tema (`indigo/burgundy/forest/slate/plum`) hâlâ var, ama `theme_color`
  ile `theme_engine.py` üzerinden SINIRSIZ sayıda özel renk üretilebilir
  (bkz. "Renk Teması" bölümü) — sabit sınıflar artık bir seçenek, zorunluluk
  değil.
- Kapak: çok katmanlı gradient + nokta dokusu + döner amblem (halka + saat
  çentikleri + sunburst) + 4 köşede ince "cilt" süsü + dev soluk motif harfi.
- Her sayfa A4 (210×297mm), `.page` sınıfı `overflow:hidden` — taşma her
  zaman görünür/yakalanabilir olmalı (bkz. yukarıdaki flex-shrink notu).
- İçindekiler hem sayfa-içi tıklanabilir linkler (`<a href="#ch-N">`) hem
  gerçek PDF outline paneli (`build.py`'deki `add_bookmarks()`) üretir —
  ikisi de otomatik, dokunmana gerek yok.
- Sınav bölümü GÜNCEL formatta Test (`#exam` anchor) + ayrı bir Cevap
  Anahtarı (`#answer-key` anchor) sayfa grubundan oluşur; LEGACY formatta
  tek bir "Sınav Hazırlık" (`#exam` anchor) sayfa grubudur — hangisinin
  render edileceğine `pack.test_questions` doluluğu karar verir.

## Hızlı komut özeti

```bash
# Derle
cd ders_sistemi && python3 build.py content.<slug>

# Belirli sayfaları PNG'ye çevirip incele
pdftoppm -png -r 100 -f <ilk> -l <son> output/<slug>.pdf output/preview/pg

# Tüm sayfaları çevir
pdftoppm -png -r 100 output/<slug>.pdf output/preview/pg

# Bookmark/link doğrulaması
python3 -c "
from pypdf import PdfReader
r = PdfReader('output/<slug>.pdf')
for it in r.outline: print(it.title, '->', r.get_destination_page_number(it)+1)
"

# Tema paleti önizlemesi (hangi renklerin kullanıldığını görmek için)
python3 theme_engine.py
```

## Özet — bir ders eklerken zihinsel kontrol listesi

- [ ] Kaynak eklenmediyse `kaynaklar/` klasöründe ders adıyla eşleşen dosyayı
      aradım (yoksa kullanıcıdan istedim)
- [ ] Ham metni tamamen okudum (atlamadım)
- [ ] 5-7 bölüme, ham içeriğin doğal yapısını takip ederek ayırdım
- [ ] Kullanılmamış bir renk seçtim (`theme_color=` hex, `content/`
      dizinindeki diğer derslerden görsel olarak ayrışan), tek harfli
      Latin `icon_text` verdim
- [ ] `content/<slug>.py` yazdım, `content_model.py` API'sine birebir uydum
- [ ] 20 soruluk `test_questions` + eşleşen `answer_key_items` yazdım
      (LEGACY `distinctions`/`match_table`/`qa_items` DEĞİL)
- [ ] `python3 build.py content.<slug>` çalıştırdım
- [ ] "[TAŞMA UYARISI]" çıkmayana kadar sayfa böldüm (ya da TEST_PER_PAGE
      taşıyorsa soru sayısını/sayfa dağılımını) ve yeniden derledim
- [ ] Kapak (yeni renk doğru mu?) + içindekiler + genel bakış + her bölüm
      ilk sayfası + en az bir tablo sayfası + sözlük son sayfası + test
      son sayfası + cevap anahtarı son sayfası görsel kontrol ettim
- [ ] Her bölümün TÜM sayfalarını (özellikle devam sayfalarını) tek tek
      inceleyip içeriğin sayfanın yarısından önce bitmediğini (büyük boş alan
      kalmadığını) doğruladım; gerekirse komşu sayfalar arasında mevcut
      içeriği taşıdım/birleştirdim — asla yeni içerik uydurmadım, taşan
      denemeleri geri aldım
- [ ] Bookmark/link sayısını doğruladım
- [ ] PDF'i kullanıcıya sundum
