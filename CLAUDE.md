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
geçerlidir. Tek istisna birleşik kitaptır: tek bir derse ait olmadığı için
`gorsel_ders_notlari/` **köküne** yazılır.

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

### 2. İçeriği 5-7 bölüme planla

Ham metnin doğal başlık yapısını takip et (uydurma bölümleme yapma). Her bölüm için:
4 anahtar terim, en az 1-2 tablo/blok, mümkünse bir callout, her zaman bir bölüm
özeti. Bölüm başına ortalama 2 sayfa hedefle (1-3 kabul edilebilir) — yoğun bölümleri
en baştan 2-3 `ChapterPage`'e böl, tek dev sayfaya sıkıştırmaya çalışma.

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
  `add_summary(text)`.
  `continue_tag` artık **render EDİLMEZ** ("N. Bölüm · Devam" rozeti kaldırıldı) —
  vermek ZORUNLU DEĞİL, sadece geriye dönük uyumluluk için kabul ediliyor.

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

## Sayfalama sabitleri (build.py)

```python
GLOSSARY_PER_PAGE = 22     # sözlük sayfası başına kavram (2 sütun)
TEST_PER_PAGE_FIRST = 7    # ilk test sayfası (bilgi çubuğu + talimat kutusu var)
TEST_PER_PAGE = 8          # test devam sayfaları
ANSWER_PER_PAGE = 23       # cevap anahtarı (20 soru -> tek sayfa)
TOC_COMPACT_THRESHOLD = 7  # bu kadar satırı aşınca İçindekiler sıkışık kipe geçer
OVERVIEW_PAGES = 1         # Genel Bakış TEK sayfa
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
sorular; ardından ayrı bir "Cevap Anahtarı ve Çözümler" bölümü. 20 soru standarttır
ama sayı serbesttir. Şablon olarak `src/sosyoloji.py` ve `src/psikoloji.py`'yi kullanın.

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

Başka hiçbir yeri elle güncellemek gerekmez — sayfa numaraları, ana içindekiler, ders
haritası, kapak istatistikleri, yer imleri hepsi hesaplanır.

### Yapısı ve denetimleri

| Bölüm | İçerik |
|---|---|
| Ön kısım | Ana kapak · Künye · Nasıl Kullanılır · Sayfa Rehberi · Ana İçindekiler · Ders Haritası |
| Gövde | Her ders, tek ders PDF'iyle BİREBİR aynı sayfalarla |

Ön kısım 11 derse kadar 6, 12+ derste 7 sayfadır (`front_matter_page_count()` — ilk
dersin sayfa offset'i buna bağlı). Kitabın kendi metinleri (kapak başlığı, künye,
önsöz, rehber) `src/kitap.py`'deki `BookPack` alanlarındadır; ders içeriğiyle
karıştırma.

Mimari: `_ders_govde.html.j2` TEK KAYNAKTIR; `master.html.j2` (tek ders) ve
`kitap.html.j2` (kitap) onu ortak kullanır — "tek derste doğru, kitapta yanlış numara"
durumu yapısal olarak imkânsızdır.

Build çıktısındaki **dört denetim**: taşma (kitapta ayrıca hangi dersin kaçıncı
sayfası olduğu yazılır) · sayfa numarası zinciri · render doğrulaması · boyut
optimizasyonu. Biri hata verirse **PDF'i teslim etme**, önce sebebini bul.

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
