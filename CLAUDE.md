# CLAUDE.md — Görsel Ders Notu Üretim Sistemi

## KRİTİK KURAL: Birleşik Kitaba Otomatik Ekleme Yasağı

Yeni bir ders (görsel ders notu PDF'i) üretildiğinde veya güncellendiğinde,
bu dersi birleşik "10 ders" kitabına (veya ileride oluşacak başka bir
birleşik kitaba) OTOMATİK OLARAK EKLEME. Birleştirme scriptini çalıştırma.

Kural:
- Tekil ders kitabı üretimi ve birleşik kitap üretimi birbirinden
  TAMAMEN AYRI, birbirini tetiklemeyen iki iştir.
- Bir ders için "işle", "anlat", "görsel not hazırla" gibi bir istek
  geldiğinde, sonucu sadece o dersin kendi PDF'i olarak üret ve
  ilgili sınav döneminin `gorsel_ders_notlari/<DERS ADI>/` klasörüne koy.
  Birleştirme
  scriptine (merge/combine script) DOKUNMA.
- Birleşik kitaba bir dersin eklenmesi/çıkarılması/yeniden sıralanması
  SADECE kullanıcı açıkça "birleşik kitaba ekle", "kitabı güncelle",
  "birleştirmeyi çalıştır" gibi bir talimat verdiğinde yapılır.
- Bu yasak HER SINAV DÖNEMİ İÇİN AYRI AYRI geçerlidir: her dönemin kendi
  `src/kitap.py`'si ve kendi birleşik kitabı vardır; bir dönemin kitabını
  derlemek başka bir dönemi etkilemez, ama hiçbiri otomatik tetiklenmez.
- Emin değilsen (istek belirsizse), birleştirmeyi ÇALIŞTIRMADAN ÖNCE
  kullanıcıya sor: "Bu dersi birleşik kitaba da eklememi ister misiniz?"
- Yeni bir ders üretirken sayfa boyutu (trim) ayarı olarak varsayılan
  tekil-kitap trim boyutunu kullan, birleşik kitabın trim boyutunu
  DEĞİL — bu iki değer birbirinden bağımsız olmalı ve
  build.py'de ayrı ayrı config/parametre olarak tutulmalı, tek bir
  global sabitle yönetilmemeli.

Bu dosya, bu repodaki "Görsel Ders Notu Kitabı" üretim sistemini kullanarak
yeni bir ders işlerken Claude Code'un izlemesi gereken talimatları içerir.
Kullanıcı sana bir ders özeti (PDF/metin) verip "bunu görsel ders notuna
çevir" dediğinde, bu dosyadaki süreci baştan sona uygula.

## KRİTİK KURAL 2: Sınav Dönemi Varsayılmaz — Her Zaman Sorulur

Bu repo artık dosyaları **sınıf / dönem / sınav dönemi** ağacında tutar.
Hiçbir script'in varsayılan dönemi YOKTUR ve sen de varsayma:

- Kullanıcı bir ders işlemeni isterken sınıf/dönem/sınav belirtmediyse
  **derlemeden ÖNCE sor**: "Bu ders hangi sınıf / dönem / sınav dönemine
  ait? (ör. 3. sınıf · 1. dönem · vize)".
- Tahmin etme, "en son hangisini kullandıysak" deme, `2-sinif/2-donem/final`
  varsayma. Yanlış döneme yazılan bir ders, sessizce yanlış birleşik kitaba
  girer — geri alması zordur.
- Her komut üç parametreyi birlikte alır: `--sinif {2,3} --donem {1,2}
  --sinav {vize,final}`. Parametre verilmezse script interaktif sorar;
  soramıyorsa (TTY yok) net bir hatayla durur, asla varsayıma düşmez.
- Aynı ders adı farklı dönemlerde ayrı ayrı bulunabilir ve bunlar birbirinden
  TAMAMEN bağımsızdır (ayrı `src/`, ayrı çıktı, ayrı birleşik kitap).

## Klasör yapısı: sınıf / dönem / sınav / DERS

```
<sinif>-sinif/<donem>-donem/<sinav>/
├── kaynaklar/
│   ├── ders_kaynaklari/<DERS ADI>/     # GİRDİ: ham ders metni / kaynak PDF
│   ├── ogretmen_notlari/<DERS ADI>/    # GİRDİ: öğretmenin dağınık dikte notu
│   └── özetlenmiş_dersler/<DERS ADI>/  # ARA:   yukarıdakilerden çıkarılan YAZILI özet
├── gorsel_ders_notlari/                # ÇIKTI: build.py / build_kitap.py
│   ├── <DERS ADI>/                     #   tekil ders (.pdf + .html)
│   └── <kitap-slug>.pdf                #   birleşik kitap (KÖKTE — tek bir derse ait değil)
├── src/                                # <ders_slug>.py içerik modülleri + kitap.py
├── calisma_rehberleri/<DERS ADI>/      # ÇIKTI: ders-anlatim skill'i Mod 2
└── ders_anlatimlari/<DERS ADI>/        # ÇIKTI: ders-anlatim skill'i Mod 1
```

`<sinif>` ∈ {2, 3} · `<donem>` ∈ {1, 2} · `<sinav>` ∈ {vize, final} —
8 dönem klasörünün hepsi mevcut (boşlar `.gitkeep` ile tutuluyor).

### KRİTİK KURAL 3: Üretim zinciri ve `<DERS ADI>` alt klasörü

```
ders_kaynaklari/ + ogretmen_notlari/  ->  özetlenmiş_dersler/  ->  gorsel_ders_notlari/
      (ham girdi)                          (yazılı özet)            (kitap formatı, build.py)
```

Bu üç aşama **ayrı şeylerdir, birbirinin yerine geçmez**:

* `özetlenmiş_dersler/` = ham kaynağın/öğretmen notunun **yazılı** özeti.
  build.py'nin ÇIKTISI DEĞİL, GİRDİSİDİR.
* `gorsel_ders_notlari/` = build.py'nin ürettiği **kitap formatındaki** görsel
  ders notu PDF'i. Tek gerçek çıktı klasörü budur.

**Her üç klasörde de dosyalar doğrudan köke DEĞİL, dersin adını taşıyan bir
alt klasörün içine konur.** Örnek tam yol:

```
3-sinif/1-donem/final/kaynaklar/özetlenmiş_dersler/SİSTEMATİK KELAM I/sistematik-kelam-1-ozet.pdf
3-sinif/1-donem/final/gorsel_ders_notlari/SİSTEMATİK KELAM I/sistematik-kelam-i.pdf
```

`build.py` bu alt klasörü **otomatik oluşturur** (yoksa) ve çıktıyı oraya
yazar; bu davranış TÜM sınıf/dönem/sınav kombinasyonlarında geçerlidir.
Aynı kural `ders-anlatim` skill'inin çıktı klasörleri (`ders_anlatimlari/`,
`calisma_rehberleri/`) için de geçerlidir — bkz.
`.claude/skills/ders-anlatim/SKILL.md`.
Klasör adı `CoursePack.ders_klasoru` alanından okunur — bkz. aşağıdaki
"`ders_klasoru`" başlığı. Tek istisna birleşik kitaptır: tek bir derse ait
olmadığı için `gorsel_ders_notlari/` **köküne** yazılır.

### `ders_klasoru` — her yeni derste ZORUNLU

`CoursePack`'e ders programındaki **BÜYÜK HARFLİ tam adı** yazın:

```python
return CoursePack(
    ders_klasoru="SİSTEMATİK KELAM I",   # <- klasör adı; kaynaklar/ altındakiyle BİREBİR aynı olmalı
    course_code="SİST. KELAM I",
    ...
)
```

Boş bırakılırsa build.py başlık slug'ına düşer (`kelâm-tarihi/` gibi) — bu
sadece geriye dönük uyumluluk içindir ve klasör adının `kaynaklar/` altındaki
ders klasörüyle eşleşmemesine yol açar. **Yeni derste her zaman doldurun.**

### Neyin nerede olduğu

| Ne | Nerede |
|---|---|
| Ham ders metni / kaynak PDF (girdi) | `<dönem>/kaynaklar/ders_kaynaklari/<DERS ADI>/` |
| Öğretmenin ham dikte notu (girdi) | `<dönem>/kaynaklar/ogretmen_notlari/<DERS ADI>/` |
| Yazılı özet (ara ürün, build.py'nin girdisi) | `<dönem>/kaynaklar/özetlenmiş_dersler/<DERS ADI>/` |
| Dersin Python içerik modülü | `<dönem>/src/<ders_slug>.py` |
| Birleşik kitap tanımı | `<dönem>/src/kitap.py` |
| **Üretilmiş görsel ders notu (tekil)** | `<dönem>/gorsel_ders_notlari/<DERS ADI>/` |
| **Üretilmiş birleşik kitap** | `<dönem>/gorsel_ders_notlari/` (kökte) |
| ders-anlatim skill'i çıktıları | `<dönem>/ders_anlatimlari/<DERS ADI>/` (Mod 1) · `<dönem>/calisma_rehberleri/<DERS ADI>/` (Mod 2) |

> Eski `ders_ozetleri/` klasörü KALKTI — adı `özetlenmiş_dersler` ile
> karışıyordu. Tüm çıktılar artık `gorsel_ders_notlari/` altındadır.

### DÜZ KİP (`dersler/`) — sınıf ağacı olmayan kurulumlar

Bu depo GitHub'da yalnızca boş bir `dersler/` iskeletiyle yayımlanır; sınıf
ağaçları (`2-sinif/`, `3-sinif/`) `.gitignore`'dadır ve klonlayan kişide hiç
bulunmaz. `cekirdek/donem.py` bunu algılar:

- Sınıf ağacı diskte YOKSA ve kullanıcı sınıf/dönem/sınav vermediyse →
  kendiliğinden `dersler/` köküne geçer ve bunu konsola yazar.
- `--duz` bayrağı verilirse → her koşulda `dersler/` kullanılır.
- Sınıf ağacı VARSA (bu makinede var) → hiçbir şey değişmez, dönem yine
  sorulur. KRİTİK KURAL 2 aynen geçerlidir.

**Bayrağın adı `--duz`, `--dersler` DEĞİL.** `tools/olcum.py`,
`tools/dengele.py` ve `tools/kalibre.py` dosyalarında `dersler` adında
KONUMSAL bir argüman (ölçülecek ders listesi) zaten var; aynı adı kullanmak
argparse `dest`'ini ezip o üç aracı bozuyor.

`dersler/src/ornek_ders.py` yayımlanan tek ders modülüdür: içeriği sistemin
kendi belgelerinden yazılmış özgün bir metindir (bir ders kitabından
türetilmediği için GPL kapsamındadır) ve kurulum doğrulaması olarak kullanılır.

### Çıktılar ve kaynaklar git'e GİRMEZ

`gorsel_ders_notlari/`, `calisma_rehberleri/`, `ders_anlatimlari/` ve
`kaynaklar/` altındaki dosyalar `.gitignore`'dadır — depoda yalnızca klasör
iskeleti (`.gitkeep`) durur. Bir ders ürettikten sonra PDF'i commit etmeye
ÇALIŞMA; git onu zaten yok sayar.

Sebep: bir dersin gerçek içeriği `src/<ders>.py` modülüdür, PDF ondan her
zaman yeniden üretilebilir. PDF ikili dosya olduğu için git sıkıştıramaz;
her yeniden derleme depoya tam bir kopya daha eklerdi (bu depo bir kez 345
MB'a çıkmıştı, %98.5'i çıktı dosyalarıydı).

Pratik sonuçları:
- Bir ders "kayboldu" diye endişelenme — `src/<ders>.py` duruyorsa
  `python build.py <slug> --sinif X --donem Y --sinav Z` onu geri getirir.
- `kaynaklar/` altındaki ham materyal koddan ÜRETİLEMEZ ve git'te yedeği
  YOKTUR. Kullanıcıya bu dosyaları silmesini/taşımasını önerme.
- Yeni bir çıktı türü eklersen (`.docx` gibi) `.gitignore`'a kuralını da
  ekle; kurallar UZANTI bazlıdır, klasör bazlı değil (yoksa `.gitkeep`
  iskeleti de yok sayılır ve dizin yapısı depodan silinir).

### Paylaşılan altyapı (döneme ait DEĞİL, asla kopyalanmaz)

```
build.py · build_kitap.py · cekirdek/ · templates/ · tools/ · assets/
```

Bu dosyalar TÜM dönemler tarafından paylaşılır. `templates/style.css` veya
`templates/_ders_govde.html.j2` üzerinde bir düzeltme yaparsan **her sınıfın
her döneminin** çıktısını etkilersin — bu kasıtlıdır (tasarım tek kaynaktır),
ama dönem-özel bir "düzeltme" yapmaya çalışma.

### Ders modülleri neden noktalı yolla import edilmiyor?

`2-sinif` geçerli bir Python paket adı değildir, bu yüzden eski
`content.kelam_tarihi` biçimi artık kullanılamaz. `cekirdek/donem.py`, seçilen dönemin
`src/` klasörünü `sys.path`'in başına koyar ve modül **çıplak adıyla**
(`kelam_tarihi`) import edilir. Eski noktalı yazım yine de kabul edilir
(önek atılır), ama yeni kodda çıplak ad kullan.

Bir `src/*.py` dosyasının başındaki

```python
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
```

satırı **proje köküne** çıkar (`cekirdek/` paketinin bulunduğu yere) —
`src/ -> <sinav> -> <donem> -> <sinif> -> KÖK` = 4 seviye. Düz kipte
(`dersler/src/`) bu sayı **2**'dir. Yeni bir ders dosyası yazarken doğru
seviyeyi say; yanlış sayarsan `cekirdek` paketi bulunamaz.

Veri şeması `cekirdek` paketinden import edilir:

```python
from cekirdek.content_model import KeyTerm, Chapter, ChapterPage, CoursePack
```

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
`templates/_ders_govde.html.j2` üzerinde kalıcı bir düzeltme yap, çünkü bu
dosyalar TÜM derslerde paylaşılır. (`master.html.j2` artık sadece 13 satırlık
bir sarmalayıcıdır; bir dersin gerçek sayfa yapısı `_ders_govde.html.j2`
içindedir ve tek ders PDF'i ile birleşik kitap ONU ortak kullanır — düzeltmeyi
oraya yapınca her iki çıktı birden düzelir.)

Ayrıca tüm dersleri **tek bir cilt** halinde birleştiren ikinci bir çıktı
vardır: `python build_kitap.py --sinif X --donem Y --sinav Z`
(bkz. aşağıdaki "Birleşik Kitap" bölümü). Birleştirme HER ZAMAN tek bir
sınav dönemi içindedir; dönemler asla tek ciltte karışmaz.

## Sayfa boyutu ve kenar boşlukları (SAYFA GEOMETRİSİ)

Çıktı **A4'tür ve FOTOKOPİ içindir** — matbaa/kesim/ciltleme yoktur
(2026 Ağustos'unda kullanıcı matbaa fikrinden vazgeçti; önceki 175 × 250 mm
+ 3 mm bleed kitap ölçüsü terk edildi):

| | |
|---|---|
| Sayfa ölçüsü | **210 × 297 mm (A4 dikey)** |
| Taşma payı (bleed) | **0 mm — YOK.** Kesim olmadığı için render/MediaBox = A4 |
| Üst / alt kenar | 12 mm / 15 mm (alt, sayfa numarası payı dahil) |
| İç / dış kenar | 12 mm / 12 mm — **simetrik** (tek yüz fotokopi) |
| Metin alanı | **186 × 270 mm** |
| Gövde punto | **9,6 pt** (tasarımın orijinal A4 ölçeği) |

Kenarlar bilinçli olarak DAR. Daha da daraltmayın: fotokopi makineleri ve
ofis yazıcıları kağıdın kenarından **~5 mm** basamaz, 10 mm'nin altına
inmek kenardaki içeriği kırpma riskine sokar.

**Fotokopi kipinin iki sonucu:**
- **Bleed 0'dır.** Kapak gradyanı ve `--paper` zemin tonu hâlâ tam sayfayı
  kaplar, ama fotokopide dış ~5 mm'de ince beyaz bir çerçeve kalır. Bu
  makinenin fiziksel sınırıdır, bir hata değildir.
- **Ayna simetri etkisizdir** (iç = dış = 12 mm). Arkalı-önlü çekip
  spiral/zımba yapacaksanız `PageGeometry.mg_inner`'ı 18 mm'ye çıkarmanız
  yeterli; `odd_page_gutter` hangi tarafın sırt olduğunu zaten söyler.

`templates/style.css` içindeki tipografi/boşluk/çizgi ölçüleri bir dönem
0,8229 ile küçültülmüştü (175 × 250 mm sayfa için, gövde 9,6 → 7,9 pt);
A4'e dönülürken bu küçültme **birebir geri alındı** (209 satır, ×1,2152) —
yani tasarım yeniden çizildiği orijinal A4 ölçeğindedir. Yeni bir bileşen
eklerken ölçüleri bu skalaya uydurun, küçültülmüş değerlere değil.

**İKİ AYRI CONFIG vardır ve birbirinden bağımsızdır** (bkz. en üstteki
KRİTİK KURAL). `build.py`'nin başındaki `PageGeometry` dataclass'ından iki
örnek üretilir:

| Config | Kullanan | Şu anki trim |
|---|---|---|
| `SINGLE_GEOMETRY` | `python build.py <slug> --sinif X --donem Y --sinav Z` (tekil ders) | 210 × 297 mm |
| `BOOK_GEOMETRY` | `python build_kitap.py --sinif X --donem Y --sinav Z` (birleşik kitap) | 210 × 297 mm |

Değerleri şu an aynıdır ama TEK BİR GLOBAL SABİT DEĞİLDİR: birini
değiştirmek diğerini etkilemez. `page_geometry_css(geo)` verilen config'ten
CSS değişkenlerini üretip `style.css`'in sonuna ekler; `style.css`'teki aynı
adlı `:root` değerleri yalnızca varsayılandır. `load_css(geo)`,
`render_pdf(..., geo=)` ve `finalize_for_print(..., geo=)` hep bu config'i
taşır — tekil ders çağrılarında varsayılan `SINGLE_GEOMETRY`, kitap
build'inde açıkça `BOOK_GEOMETRY`. Modül düzeyindeki eski `TRIM_W_MM` /
`PAGE_H_MM` gibi isimler `SINGLE_GEOMETRY`'nin takma adlarıdır ve sadece
`tools/olcum.py` + `tools/kalibre.py` geriye dönük uyumluluğu içindir.

Bir çıktının ölçüsünü değiştirecekseniz SADECE ilgili config'i düzenleyin —
sonra mutlaka:

```bash
python tools/kalibre.py --sinif X --donem Y --sinav Z        # sabitleri yeniden ölçer
python tools/dengele.py --hepsi --sinif X --donem Y --sinav Z   # sayfaları yeniden dağıtır
```

Sırtın hangi tarafta olduğunu değiştirmek için tek satır yeter:
`ODD_PAGE_GUTTER = "right"` (sağdan sola açılan cilt için).

Bleed 0 olduğu için `pdfx.set_print_boxes()` artık CropBox/BleedBox/TrimBox'ın
üçünü de aynı yere, **210×297 mm**'ye yazar. (ArtBox bilerek yazılmaz — PDF/X
bir sayfada TrimBox VEYA ArtBox ister, ikisini birden değil.) Chromium levhayı
kendi piksel yuvarlamasıyla bir kenarda ~0,1 mm eksik üretebilir; `pdfx.py`
yarım milimetreye kadar sapmayı sessizce levhaya sığdırır, uyarı yalnızca
gerçek bir eksiklikte çıkar.

## PDF/X-4 CMYK dönüşümü — VARSAYILAN OLARAK KAPALI

**Çıktı artık RGB'dir.** Fotokopi makineleri ve ofis yazıcıları renk
dönüşümünü kendi sürücülerinde yapar; dosyayı önceden CMYK'ya çevirmek
renkleri donuklaştırır, boyutu büyütür ve her derlemeye Ghostscript'in
dakikalarını ekler. `finalize_for_print()` bu yüzden sayfa kutularını HER
ZAMAN yazar ama `pdfx.convert_or_warn()`'u yalnızca CMYK istendiğinde çağırır.

Matbaaya iş göndereceğiniz gün tek bayrak yeter — her iki build de aynı
bayrağı `build.add_cikti_args()` üzerinden paylaşır:

```bash
python build.py <slug> --sinif X --donem Y --sinav Z --cmyk
python build_kitap.py --sinif X --donem Y --sinav Z --cmyk
```

`--rgb` varsayılanı açıkça yazmak içindir. Kalıcı olarak değiştirmek
isterseniz `build.py`'deki `CMYK_DEFAULT` sabitini çevirin. Aşağıdaki
maddeler yalnızca `--cmyk` verildiğinde geçerlidir:

* **Ghostscript kurulu değilse build DURMAZ**: işletim sistemine göre kurulum
  komutunu içeren net bir uyarı basılır ve dosya RGB bırakılır
  (macOS `brew install ghostscript` · Ubuntu `sudo apt install ghostscript` ·
  Windows ghostscript.com installer). Kurulu ama PATH'te değilse tam yolu
  `DERS_GS` ortam değişkenine yazın.
* **ICC çıktı profili**: `assets/icc/ISOcoated_v2_eci.icc` (FOGRA39) varsa o
  kullanılır; yoksa Ghostscript'in genel `default_cmyk.icc`'sine düşülür ve
  uyarı basılır. Profil eci.org'dan lisans onaylı indirilir, bkz.
  `assets/icc/README.md`. Farklı bir yol için `DERS_ICC` ortam değişkeni.
* Dönüşüm sonrası doğrulanır: sayfa sayısı korunuyor mu, çıktıda RGB nesne
  kaldı mı, TrimBox duruyor mu, XMP'de PDF/X-4 kimliği var mı. Sayfa sayısı
  değişirse dönüşüm iptal edilir ve RGB dosya bırakılır.

## Dizin yapısı

```
ders-uretim-sistemi/
│
│  ── PAYLAŞILAN ALTYAPI (döneme ait değil) ────────────────────────────────
├── build.py                # TEK DERS: HTML üret → PDF render → küçült → bookmark → kutular → CMYK
├── build_kitap.py          # BİRLEŞİK KİTAP: bir dönemin tüm derslerini tek ciltte birleştirir
├── cekirdek/               # KÜTÜPHANE — doğrudan çalıştırılmaz, yukarıdakiler kullanır
│   ├── donem.py            # SINIF/DÖNEM/SINAV (ve düz `dersler/`) çözümleyici
│   ├── content_model.py    # Veri şeması (dataclass'lar) — API referansı aşağıda
│   ├── theme_engine.py     # Sınırsız renk teması motoru (tek hex'ten tam tema üretir)
│   ├── renk_uretici.py     # DERSE ÖZEL VURGU RENGİ — build + ders-anlatim ORTAK kaynağı
│   ├── harita.py           # HARİTA KUTUSU: hangi bölüm harita adayı (tespit)
│   ├── harita_cizim.py     # HARİTA ÇİZİMİ: Natural Earth + gerçek koordinat -> SVG
│   ├── sinir_cikar.py      # SINIR ÇIKARMA: Commons haritasının alanı -> lon/lat poligonu
│   ├── commons_ara.py      # KAYNAK BULMA: bir Vikipedi maddesinin kullandığı haritalar
│   └── pdfx.py             # BASKI ÖNCESİ: TrimBox/BleedBox + Ghostscript ile PDF/X-4 CMYK
├── tools/
│   ├── olcum.py            # Her bloğun GERÇEK yüksekliğini (mm) Chromium'da ölçer
│   ├── dengele.py          # Ölçüme göre ChapterPage bölünmelerini yeniden dağıtır
│   ├── harita.py           # HARİTA: kaynak bul/indir · sınır çıkar · aday tara · önizle
│   └── kalibre.py          # Sözlük/Test/Cevap sayfa başına öğe sabitlerini kalibre eder
├── templates/
│   ├── _ders_govde.html.j2      # BİR DERSİN GÖVDESİ — asıl şablon, tek kaynak (sabit)
│   ├── master.html.j2            # Tek ders sarmalayıcısı (13 satır — _ders_govde'yi çağırır)
│   ├── kitap.html.j2             # Kitap sarmalayıcısı (ön kısım + tüm dersler)
│   ├── _kitap_on_kisim.html.j2   # Kitabın kapak/künye/önsöz/rehber/içindekiler/harita sayfaları
│   └── style.css                  # Tasarım sistemi (sabit — dokunma, sadece bug varsa düzelt)
├── assets/icc/             # FOGRA39 ("ISO Coated v2") ICC profili buraya konur (bkz. README)
├── docs/                   # KURULUM.md · TELIF.md · README ekran görüntüleri
│
│  ── DÖNEM AĞAÇLARI (8 sınav dönemi) ──────────────────────────────────────
├── 2-sinif/{1,2}-donem/{vize,final}/
└── 3-sinif/{1,2}-donem/{vize,final}/
        ├── kaynaklar/
        │   ├── ders_kaynaklari/<DERS ADI>/    # GİRDİ: ham ders metni
        │   ├── ogretmen_notlari/<DERS ADI>/   # GİRDİ: ham dikte notu
        │   └── özetlenmiş_dersler/<DERS ADI>/ # ARA:   yazılı özet
        ├── src/                   # ders modülleri + kitap.py (bu dönemin)
        ├── gorsel_ders_notlari/   # ÇIKTI: <DERS ADI>/<slug>.pdf + .html
        ├── calisma_rehberleri/<DERS ADI>/  # ÇIKTI: ders-anlatim Mod 2
        └── ders_anlatimlari/<DERS ADI>/    # ÇIKTI: ders-anlatim Mod 1
```

Şu an **yalnızca `2-sinif/2-donem/final/` doludur** (11 ders); diğer 7 dönem
klasörü boş iskelet olarak hazır bekliyor.

```
2-sinif/2-donem/final/src/
├── __init__.py
├── kitap.py                 # BİRLEŞİK KİTAP tanımı: ders sırası + kitabın ön kısım metinleri
├── psikoloji.py             # Örnek: tamamlanmış bir ders (indigo tema, Test+Cevap Anahtarı formatı)
├── sosyoloji.py             # Örnek (forest tema, Test+Cevap Anahtarı formatı)
├── cagdas_felsefe.py        # Örnek (theme_color #1C5C69, Test+Cevap Anahtarı formatı)
├── edebiyat.py              # Örnek (theme_color #5A6732, Test+Cevap Anahtarı formatı)
├── felsefe_tarihi_2.py      # Örnek (theme_color #724C31, Test+Cevap Anahtarı formatı)
├── kelam_tarihi.py          # Örnek (Test+Cevap Anahtarı formatı)
├── islam_tarihi_3.py        # Örnek (theme_color #1D4E79, Test+Cevap Anahtarı formatı)
├── ogretim_ilke_yontem.py   # Örnek (theme_color #863C5E, Test+Cevap Anahtarı formatı)
├── tefsir2.py               # Örnek: Arapça ayet içeren ders (theme_color #246038, add_ayat)
├── ogretim_teknolojileri.py # Örnek (slate tema, LEGACY Sınav Hazırlık formatı)
└── sanat_tarihi.py          # Örnek (burgundy tema, LEGACY Sınav Hazırlık formatı)
```

Her ders, ilgili dönemin `src/` klasöründe kendi Python dosyasında yaşar ve
tek bir `get_pack() -> CoursePack` fonksiyonu dışa verir.

**Not — iki nesil örnek var:** `psikoloji.py`/`sosyoloji.py`/`cagdas_felsefe.py`/
`edebiyat.py`/`felsefe_tarihi_2.py`/`kelam_tarihi.py`/`islam_tarihi_3.py`/
`ogretim_ilke_yontem.py`/`tefsir2.py` GÜNCEL standardı (Test + Cevap Anahtarı,
sınırsız renk teması) kullanır; kalan 2 örnek (`ogretim_teknolojileri.py`,
`sanat_tarihi.py`) henüz eski "Sınav Hazırlık"
(distinctions/match_table/qa_items) formatındadır ve geriye dönük uyumluluk
için bozulmadan çalışmaya devam eder (bkz. aşağıdaki "Test + Cevap Anahtarı"
ve "Renk Teması" bölümleri). **Yeni bir ders yazarken her zaman GÜNCEL
gruptaki dosyalardan birini şablon alın, LEGACY 2'sini değil.**

## Uçtan uca iş akışı

Kullanıcı sana bir ders PDF'i / ham metni verdiğinde (ya da sadece bir ders
adı söylediğinde) şu adımları sırayla uygula:

### 0. Dönemi belirle, sonra kaynağı bul
**Önce dönem** (bkz. KRİTİK KURAL 2): kullanıcı sınıf/dönem/sınav
belirtmediyse SOR. Bundan sonraki her komutta `--sinif X --donem Y --sinav Z`
kullan; dönemin kökünü kısaca `<D>` diye anacağız:

```
<D> = <sinif>-sinif/<donem>-donem/<sinav>
```

Kullanıcı bir dosya eklemeden sadece bir ders adı söylerse (ör. "sosyoloji
dersini işle"), önce PDF/metin eklenip eklenmediğini kontrol et; eklenmediyse
**kullanıcıya sormadan önce** o dönemin girdi klasörlerini tara:
```bash
ls "<D>/kaynaklar/ders_kaynaklari/"       # ders adı alt klasörleri
ls "<D>/kaynaklar/ogretmen_notlari/"
ls "<D>/kaynaklar/özetlenmiş_dersler/"    # varsa hazır yazılı özet
```
Ders adıyla eşleşen (esnek eşleştir — büyük/küçük harf, Türkçe karakter,
"-özet"/"-ozet" gibi ekleri göz ardı ederek) bir dosya varsa onu kaynak
olarak kullan, kullanıcıya tekrar sorma. Eşleşen dosya yoksa **başka
dönemlere bakma** (yanlış dönemin kaynağını kullanmak sessiz bir hatadır);
kullanıcıdan PDF'i ya sürükle-bırak yapmasını ya da doğru dönemin
`kaynaklar/ders_kaynaklari/` klasörüne koyup dosya adını söylemesini iste.

`kaynaklar/ders_kaynaklari/` klasörü, kullanıcının ham ders özetlerini tek tek
her seferinde sohbete eklemek zorunda kalmadan biriktirdiği yerdir — dosya
adı serbesttir ama tutarlı bir kalıp (`<ders-slug>-ozet.pdf` gibi) aramayı
kolaylaştırır. İşlenen bir dersin kaynağını bu klasörden SİLME — kullanıcı
ileride revizyon isteyebilir.

(Not: `kaynaklar/ogretmen_notlari/` ve `<D>/calisma_rehberleri/` +
`<D>/ders_anlatimlari/` klasörleri bu görsel PDF sistemine değil, tamamen
ayrı çalışan `ders-anlatim` skill'ine aittir, bkz.
`.claude/skills/ders-anlatim/SKILL.md`. Aynı dönem ağacını paylaşırlar ama
birbirlerini tetiklemezler.)

### 1. Ham içeriği oku ve Arapça kontrolü yap
```bash
python3 -c "
import pdfplumber
with pdfplumber.open('<D>/kaynaklar/ders_kaynaklari/<bulunan-dosya>.pdf') as pdf:
    for i, page in enumerate(pdf.pages):
        print(f'=== SAYFA {i+1} ===')
        print(page.extract_text())
"
```
Metnin TAMAMINI oku (görme aracıyla dosyayı görüntüle, kesme). Arapça karakter
(ayet, hadis) varsa sorun değil — sistem `add_ayat()` ile bunu destekliyor
(bkz. aşağıdaki API referansı ve `<D>/src/tefsir2.py` örneği).

**Arapça (RTL) metinde pdfplumber'a GÜVENME.** pdfplumber bu tür PDF'lerde
Arapçayı harf harf ters çıkarabilir; aynı sayfayı PyMuPDF ile de çıkar ve
karşılaştır:
```bash
python -c "
import pymupdf, io
d = pymupdf.open('<D>/kaynaklar/ders_kaynaklari/<dosya>.pdf')
out = io.open('cikti.txt','w',encoding='utf-8')   # Windows konsolu Arapça basamaz
for i in range(len(d)): out.write(f'=== SAYFA {i+1} ===\n' + d[i].get_text('text') + '\n')
out.close()"
```
Metni doğrulamak için bilinen bir çapa kullan: alıntıların içindeki **ayet
parçaları** sabit Mushaf metnidir; senin çıkardığın metin onlarla birebir
örtüşüyorsa yöntem güvenilirdir. Font ToUnicode hataları için tipik onarımlar:
`هللا→الله`, `اْل→الأ`, `اإل→الإ`, `اال→الا`, fatha-lam bağı `→لا`. Bir sayfa
satır içi *döndürülmüş* (cümle parçaları kaymış) geliyorsa doğru sırayı `﴿﴾`
parantez dengesi ve kaynaktaki Türkçe çeviriyle kur. Her alıntıyı üretilen
PDF üzerinde görsel olarak oku; emin olamadığın kısmı EKLEME.

### 2. İçeriği 5-7 bölüme planla
Ham metnin doğal başlık yapısını takip et (uydurma bölümleme yapma). Her bölüm
için: 4 anahtar terim, en az 1-2 tablo veya blok, mümünse bir callout ve her
zaman bir bölüm özeti planla. Bölüm başına ortalama 2 sayfa hedefle (1-3 sayfa
arası kabul edilebilir) — çok yoğun bölümleri en baştan 2-3 `ChapterPage`'e
böl, tek dev sayfaya sıkıştırmaya çalışma.

### 3. `<D>/src/<ders_slug>.py` dosyasını yaz
Aşağıdaki "cekirdek/content_model.py API Referansı" bölümüne birebir uyarak yaz.
Mevcut derslerden birini (`2-sinif/2-donem/final/src/sosyoloji.py` iyi bir orta-karmaşıklıkta
örnektir) şablon olarak kopyalayıp değiştirmek en hızlı yoldur.

Her ders için ayrıca:
- **Renk teması sınırsızdır**: `theme_color="#7A2438"` gibi TEK bir hex renk
  verin — `cekirdek/theme_engine.py` tüm tonları (kapak gradyanı, banner, tablo
  başlığı, kart kenarlığı vb.) otomatik türetir. Kolaylık için
  `theme_engine.PALETTE_HUES` içinde 16 hazır isimlendirilmiş ton var
  (`from theme_engine import PALETTE_HUES, generate_theme_vars` ile
  önizleyip hex'e çevirebilir ya da doğrudan `theme_color=` alanına
  istediğiniz herhangi bir hex'i yazabilirsiniz). Zaten kullanılmış
  renklere çok yakın bir ton seçmeyin — AYNI DÖNEMİN `src/` dizinindeki diğer
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
python build.py <ders_slug> --sinif X --donem Y --sinav Z
```
Bu tek komut şunları otomatik yapar: HTML üretir → tutarlılık denetimi
(`validate()`: bölüm numaraları ardışık mı, sözlük referansları geçerli mi,
tekrar eden terim var mı, İçindekiler satır sayısı kapasiteyi aşıyor mu,
**içerik metinlerinde kapatılmamış HTML etiketi var mı**) → Playwright ile PDF'e render eder → **her sayfanın
gerçek render yüksekliğini 210×297mm sınırıyla karşılaştırır** → PDF'e gerçek
bookmark/outline ekler → TrimBox/BleedBox yazar → Ghostscript ile PDF/X-4
CMYK'ya çevirir → **toplam sayfa sayısını ve bitmiş ölçüyü konsola basar.**

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
Taşma varsa **önce `python tools/dengele.py <slug> --sinif X --donem Y --sinav Z`
çalıştır** — bu araç
her bloğun gerçek yüksekliğini Chromium'da ölçer ve `ChapterPage`
bölünmelerini taşmayacak EN AZ sayfaya, boşluğu sona iterek yeniden dağıtır
(blokların içine ve sırasına dokunmaz, içerik uydurmaz). `--kuru` ile önce
sadece raporlatabilirsin. Elle karar vermen gerekirse PDF'i sayfa numarasına
göre PNG'ye çevirip (`pdftoppm -png -r 100 -f X -l X
"<D>/gorsel_ders_notlari/<DERS ADI>/<slug>.pdf" "<D>/gorsel_ders_notlari/preview/pgX"`)
görme aracıyla incele, aşırı yüklü `ChapterPage`'i ikiye
(gerekirse üçe) böl, yeniden derle. "✓" görene kadar tekrarla. Asla taşma
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

**Bu adımın otomatik hali `tools/dengele.py`'dir** — önce onu çalıştır, elle
düzeltmeyi yalnızca onun ulaşamadığı yerlerde yap. `tools/olcum.py` de her
sayfanın doluluk oranını ve içindeki blokların mm cinsinden yüksekliğini
tablo halinde basar; "hangi bloğu taşısam?" sorusunu tahminle değil ölçümle
cevaplamak için kullan.

**HEDEF: %90-95 doluluk.** Bir bölümün/testin/cevap anahtarının **DEVAM
sayfaları** — yani o bölümün/section'ın `ChapterPage`/sayfa listesinde İLK
sırada olmayan (bölüm banner'ıyla değil doğrudan içerikle başlayan) VE
fiziksel son sayfası da OLMAYAN sıradan ara sayfalar — ortalama %90-95
doluluk oranına sahip olmalı. (Not: bölüm devam sayfalarında artık görsel
bir "N. Bölüm · Devam" rozeti YOK — bu rozet kaldırıldı, bkz. aşağıdaki
ChapterPage notu — ama Sözlük/Test/Cevap Anahtarı devam sayfalarında hâlâ
var; hangisi olursa olsun "DEVAM sayfası" tanımı sayfanın section içindeki
SIRASINA göre yapılır, rozetin varlığına göre değil.) Buna ulaşmanın TEK
yolu, mevcut `ChapterPage` bölünmelerini bölüm içinde **yeniden dağıtmaktır**
(bir sayfadan diğerine mevcut bir blok taşımak veya iki sayfayı birleştirmek).
Mekanizma HER ZAMAN "içeriği yeniden dağıt" olmalı, ASLA "aynı içeriği daha
az yere sıkıştır" değil — element aralarındaki `gap`/`margin` değerlerini
küçültmek veya madde aralarını sıkıştırmak yasaktır, tasarım sistemi sabit
kalmalı.

**İSTİSNALAR — bu sayfalarda %90-95 hedefini ZORLAMA, doğal doluluğunu koru:**
- Bir bölümün/section'ın **SON fiziksel sayfası** (bir devam sayfası olsa
  bile) — örn. sadece bölüm özeti kutusu kalmışsa bu normaldir, doldurmaya
  çalışma.
- **Açılış sayfaları** — her bölümün/section'ın İLK fiziksel sayfası (Kapak,
  İçindekiler, Genel Bakış dahil); bunlar zaten terms+person+block ile
  doğal olarak dolu olma eğilimindedir ve bu kuralın hedef kitlesi değildir.
- **Sözlüğün son sayfası** (aşağıdaki ayrı nottaki kural geçerli).

1. Her bölümün TÜM fiziksel sayfalarını, özellikle yukarıdaki tanıma uyan
   DEVAM sayfalarını, PNG'ye çevirip tek tek görme aracıyla incele.
2. Doluluk oranını gözle tahmin et (sayfanın alt kenarına göre içeriğin
   nerede bittiği). %90'ın altındaki her DEVAM sayfası (istisnalar hariç)
   bir aday demektir — önceki gevşek "%55-70 normaldir" eşiği artık
   GEÇERLİ DEĞİL, bu daha sıkı hedefle değiştirildi.
3. İşaretlediğin bir sayfa için, AYNI bölümün komşu bir sayfasından mevcut bir
   `.add_*()` bloğunu (bir `BulletBlock`, `ComparisonTable`, `FlowDiagram`,
   `KeyTerm` listesi...) o sayfaya taşı — asla yeni madde/callout/cümle UYDURMA
   ("doldurmak" için içerik icat etmek, taşma kadar ciddi bir hatadır, çünkü
   kaynakta olmayan bilgi üretmiş olursun). %90-95 hedefine, çoğu zaman
   sayfaları TEK sayfada BİRLEŞTİRMek gerekir (bir `ChapterPage()` çağrısını
   tamamen kaldırıp içeriğini bir öncekine/sonrakine ekle) — bu, hem sayfa
   sayısını azaltıp hem de kalan sayfaları hedef aralığa taşıyan asıl
   yöntemdir; tek blok taşımak çoğu zaman yetmez.
4. Her denemeden sonra yeniden derle ve taşma çıktısını oku. Taşarsa
   değişikliği geri al ve farklı bir birleştirme/dağıtım dene (örn. daha az
   blok taşı, ya da iki sayfa yerine üç sayfa arasında dağıt). Zorla
   sıkıştırmaya çalışıp elemanlar arası boşlukları (`gap`, `margin`)
   küçültme — tasarım sistemi sabit kalmalı.
5. Emin olamadığın (birleşince taşıp taşmayacağını kestiremediğin, ya da
   taşımanın başka bir sayfayı daha da seyrekleştireceği) durumlarda,
   birkaç farklı dağıtımı dene; hiçbiri güvenli şekilde %90-95'e
   ulaştıramıyorsa mevcut boşluk seviyesini koru — riskli bir "iyileştirme",
   iyileştirmemekten daha kötüdür. Ama %90-95 hedefi eskisinden daha sıkı
   olduğu için, "temiz kazanç yok" sonucuna eskisinden daha az sıklıkla
   varman beklenir — çoğu devam sayfası gerçekten yeniden dağıtılabilir.

Sadece gerçekten güvenli (taşmayan, madde icat etmeyen, komşu sayfayı yeni
bir israf noktasına çevirmeyen) değişiklikleri kalıcı yap.

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
Bölüm sayısı + 2 (sözlük + test — GÜNCEL formatta cevap anahtarı ayrı bir
outline girdisi daha eklerse de İçindekiler sayfasında hâlâ tek satır
olarak görünür, bkz. "Test + Cevap Anahtarı" bölümü) kadar TOC linki olmalı.
Bu linklerin **tamamı 2. fiziksel sayfadadır** — İçindekiler tek sayfa
olduğu için linkler birden fazla sayfaya dağılmaz (bkz. "KRİTİK KURAL 4").
`r.pages[1]` dışında bir sayfada TOC linki görürsen kural bozulmuş demektir.

### 8. Teslim et
PDF'i kullanıcının erişebileceği çıktı konumuna kopyala ve sun.

## cekirdek/content_model.py API Referansı

```python
from cekirdek.content_model import (
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

- **`Place(name, lon, lat, sag=True)`** — haritadaki tek işaret (şehir noktası
  ya da komşu bölge etiketi). Koordinat GERÇEK ve doğrulanabilir olmalıdır;
  sıra `lon, lat`'tır (GeoJSON düzeni), ters yazmak haritayı sessizce bozar.

- **`MapBox(region, bbox, cities, neighbors, territory, label, caption, source)`**
  Coğrafi harita kutusu; `ChapterPage.add_map(mb, yan=[...], taraf="sag")` ile
  eklenir. Harita build sırasında GERÇEK VERİDEN çizilir (bkz. aşağıdaki
  "Harita Kutusu" bölümü); `svg`/`gorsel_oran` alanlarını build.py doldurur,
  elle yazmayın. `territory` YAKLAŞIKTIR ve öyle etiketlenir.

- **`InfoCard(title, text, badge=None)`** — küçük 2-3'lü kart grid'i
  (`ChapterPage.add_info_cards(başlık, [InfoCard(...), ...])` ile eklenir).

- **`Ayah(reference, arabic, meal, etymology="")`** — bir ayet/hadis kartı.
  `arabic` RTL olarak, DejaVu Sans ile doğru şekillendirmeyle render edilir
  (Arapça glyph desteği bizzat görsel olarak doğrulanmıştır — harfler doğru
  bitişiyor, harekeler doğru yerleşiyor; tereddüt etmeden kullan).
  `ChapterPage.add_ayat(başlık, [Ayah(...), ...])` ile eklenir. Örnek kullanım
  için o dönemin `src/tefsir2.py` dosyasına bak. Ham Arapça Unicode metni doğrudan
  `arabic=` alanına yaz — ekstra bir işlem gerekmez.

  > **Not:** Arapça için ek bir kütüphaneye GEREK YOKTUR — DejaVu Sans'ın
  > Chromium'daki native shaping'i (HarfBuzz) tek başına yeterlidir; CSS
  > zaten `font-family: "DejaVu Sans"` + `direction: rtl` ile doğru sonucu
  > veriyor. Bir zamanlar burada `arabic_reshape.py` ve
  > `fonts/ArabicExtracted-*.ttf` dosyaları vardı; 2026 Ağustos'unda
  > SİLİNDİLER. `arabic_reshape.py` hiçbir yerden import edilmiyordu;
  > fontların içinde ise hiç telif/lisans kaydı yoktu (bir PDF'ten çıkarılmış
  > alt küme olduklarına işaret eder), yani kaynağı belirsiz içerik
  > dağıtılıyordu. Geri getirme.

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
  `add_summary(text)`. `continue_tag` parametresi hâlâ mevcuttur ama artık
  GÖRSEL OLARAK RENDER EDİLMEZ — devam sayfalarındaki "N. Bölüm · Devam"
  rozeti+başlık bloğu, gereksiz yer kapladığı için kaldırıldı (bölüm/sayfa
  kimliği zaten üstteki `pageband`'de "Bölüm N" olarak görünüyor). Yeni bir
  ders yazarken `continue_tag` vermek ARTIK ZORUNLU DEĞİL — vermemeniz
  içerik/görünümü etkilemez; sadece geriye dönük uyumluluk için parametre
  hâlâ kabul ediliyor.

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
  uyumluluk için `cekirdek/content_model.py`'da duruyorlar; `pack.test_questions`
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
  doldurulması gereken: `ders_klasoru` (çıktı klasörünün adı — bkz.
  "KRİTİK KURAL 3"), `theme_color` (bkz. "Renk Teması" bölümü),
  `test_title`, `test_subtitle`, `test_instructions`, `test_questions`
  (20 soru önerilir), `answer_key_intro`, `answer_key_items`,
  `overview_lead`, `overview_cards` (tam 6 eleman — 3x2 grid), `overview_flow`
  (3-5 `(başlık, alt_metin)` tuple), `overview_note`. `distinctions`/
  `match_table`/`qa_items` LEGACY'dir, yeni derslerde boş bırakın.

- **`sinav_etiketi`** (opsiyonel, varsayılan `"Final"`) — kapaktaki sınav
  adı. Kapak kickerinde ("Görsel Ders Notu Kitabı · **Final** Özeti"), kapak
  istatistik kutusunda ve kapak alt bilgisinde ("N Bölüm · **Final** Sınavı
  Hazırlığı") görünür; LEGACY "Sınav Hazırlık" bölümünün pageband etiketi
  ("**Final** Tekrarı") de buradan türer. **`--sinav vize` ile derlenen bir
  ders için `sinav_etiketi="Vize"` yazın** — yoksa vize kitabının kapağında
  "Final" yazar. Varsayılan "Final" olduğu için mevcut final dersleri
  etkilenmez; `subtitle`'a ayrıca "— Vize Özeti" eklemeyin, tekrar olur.

## Renk Teması (sınırsız — `cekirdek/theme_engine.py`)

5 sabit tema (`indigo/burgundy/forest/slate/plum`) hâlâ çalışıyor, ama
YENİ derslerde bunlarla sınırlı kalmanıza gerek yok. `cekirdek/theme_engine.py`,
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

### Rengi SEN seçme — `DERS_RENKLERI` tablosuna bak

`cekirdek/renk_uretici.py` içindeki `DERS_RENKLERI` tablosu, hangi dersin hangi rengi
alacağını **önceden sabitler**. İlke: **RENK = DERSİN RUHU** — her ton o dersin
kendi anlamından seçilmiştir, bir üst sınıftan miras alınmamıştır:

| Ders | Renk | Gerekçe |
|---|---|---|
| Tefsir | `#206040` | mushaf yeşili — vahyin metni |
| Kur'an Okuma ve Tecvid | `#1D6363` | turkuaz — tilavetin akışı |
| Hadis | `#664324` | koyu deri cilt — rivayet, isnad, el yazması |
| Sistematik Kelam | `#592F79` | mor — soyut akıl, akide |
| İslam Felsefesi Tarihi | `#2F2D76` | gece mavisi — serin akıl, hikmet |
| İslam Hukuku | `#7A2433` | vişne — mühür, hüküm, otorite |
| Tasavvuf | `#7B3260` | gül — aşk, sema, kalp |
| İslam Medeniyeti / Mezhepleri Tarihi | `#776931` | bronz — altın çağ, kadim |
| Arap Dili ve Edebiyatı | `#8C2F21` | terracotta — çöl toprağı, hat |
| Sınıf Yönetimi · Ölçme ve Değerlendirme | `#1F4775` | çini laciverti — düzen, güven |
| Din Eğitimi · Rehberlik ve İletişim | `#51662E` | zeytin — fide, yetiştirme |

Aynı ders ailesi farklı dönemde tekrar ederse renk de tekrar eder (Tefsir III =
Tefsir IV), çünkü ruh aynıdır. Hue dağılımı 8/28/48/82/150/180/212/242/274/322/350
derecedir — aralar en az 20°, yani bir dönem kitabındaki 11 ders ayrışır.

Yeni bir `src/<ders>.py` yazarken:

```bash
python cekirdek/renk_uretici.py "TEFSİR III" --sinif 3 --donem 1 --sinav final
python cekirdek/renk_uretici.py --tablo        # tüm önceden belirlenmiş renkler
```

Çıkan hex'i `theme_color=` alanına **birebir** kopyala. Kendi kafandan renk
seçme — seçersen görsel kitap ile `ders-anlatim` skill'inin ürettiği anlatım
PDF'i farklı renkte çıkar (skill de aynı tablodan okur).

Bir ders tabloda yoksa (yeni bir aile) önce tabloya bir satır ekle, sonra o
hex'i kullan. Tabloya renk eklerken AYNI DÖNEMDEKİ diğer derslerin hue'larından
en az ~25° uzak bir ton seç.

Öncelik sırası: `src/<ders>.py`'deki `theme_color` → `DERS_RENKLERI` →
ders adından deterministik türetme (son çare).

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

## Harita Kutusu (coğrafi bölümler — `MapBox` + `ChapterPage.add_map`)

İçeriği mekânsal olan bölümlere (yer adları, devletler, sınırlar, sefer/göç
rotaları) metnin YANINDA duran bir harita kutusu konur: iki sütunlu düzen,
metin sütunu 1.2 / harita sütunu 1 oranında.

### TEK KURAL

> **Kaynağın içeriğini bir modele yeniden çizdirme.** Kaynaktan yalnızca
> SİLEBİLİRSİN (etiket ayıklama) ya da BİREBİR EŞLEŞMEYLE değiştirebilirsin
> (sözlükle çeviri). Eklemek istediğin her şey — Türkçe yer adı, lejant —
> haritanın ÜSTÜNE HTML katmanı olarak biner, görüntünün içine yakılmaz.

Bu kural sistemi deterministik tutar: `build.py` hiçbir zaman internete
çıkmaz, para harcamaz ve aynı girdi her derlemede aynı haritayı verir.

### TEK YOL VAR: sınırı kaynaktan çıkar, geri kalanını biz çizelim

```
tools/harita.py --commons     Vikipedi maddesinin kullandığı haritayı bul/indir
        ↓
tools/harita.py --sinir-cikar Renkli alanı gerçek lon/lat poligonuna çevir
        ↓
cekirdek/harita_cizim.py      Natural Earth üzerine BİZİM motorumuzla çiz
```

Üç dosya tek bir hattır, birbirinin alternatifi değildir: `sinir_cikar`
çizimini `harita_cizim`e yaptırır, çıkaracağı kaynağı `commons_ara`dan alır.

Sonuç: sınır kartografın, geri kalan her şey bizim. Bütün etiketler Türkçe,
baskıda vektör, PDF'e megabaytlık raster gömülmüyor, harita kitabın kendi
tipografisiyle basılıyor ve her derleme aynı çıktıyı veriyor.

> **2026-08-31 — hazır harita GÖMME yolu söküldü.** Eskiden ikinci bir yol
> vardı: Commons haritasını (SVG veya raster) olduğu gibi sayfaya gömüp
> etiketlerini çevirmek/kırpmak (`cekirdek/harita_commons.py`,
> `CommonsKaynak`, `CommonsGorsel`, `Isaret`, `--imlec`). Silindi. Raster
> yarısı zaten ölü koddu — dört raster harita sınır çıkarmaya geçince hiçbir
> ders kullanmıyordu. SVG yarısını yalnızca Moğol haritası tutuyordu ve o da
> artık çiziliyor (aşağıdaki nota bakın). Geri getirmeyin: gömülü harita
> yabancı dilde etiket, raster şişkinlik ve ikinci bir tipografi demekti.

`MapBox.territory` (tek sınır) ya da `MapBox.katmanlar` (genişleme evreleri)
alanına konan poligon **kartografın çizgisidir**, elle tahmin değildir — ama
kesikli kenar yine kalır, çünkü kaynağın kendisi de sınırı yaklaşık ilan eder.
Atıf ZORUNLUDUR (bkz. "`territory` dürüstlük meselesidir").


### Harita eklemenin yolu: `tools/harita.py --commons`

Bir Vikipedi maddesinin **gerçekten kullandığı** haritayı bulmak eskiden en çok
vakit yiyen adımdı. Artık tek komut:

```bash
python tools/harita.py --commons "Memlûk Devleti"
python tools/harita.py --commons "Memlûk Devleti" --sec 1 --ders islam_tarihi_3
```

Yaptıkları: maddenin gömdüğü görselleri listeler → Commons **kategorisinden**
haritaları ayıklar (bayrak/arma/sikke/fotoğraf/ikon elenir) → seçileni
`assets/harita/commons/` altına indirir → `LISANS.md` künyesini yazar/lisans/
bağlantı bilgisiyle **API'den otomatik** yazar → derse yapıştırılacak `MapBox`
parçasını basar. Dönem SORULMAZ (hiçbir döneme dosya yazmaz).

Ölçülmüş üç davranış — bunlara güvenin:

* **Commons'ta ARAMA yapmaz, maddeye bakar.** Arama (özellikle
  `filemime:image/svg+xml` ile daraltılmış olanı) maddedeki raster haritayı hiç
  göremiyor; bir kez bu yüzden sınır DEĞİL sefer gösteren yanlış harita
  seçilmişti. Memlük maddesi `Mamluk Sultanate of Cairo 1317 AD.jpg` kullanıyor.
* **Ayıklama ölçütü kategoridir, ad değil.** "Memlûk Devleti" maddesinde 34
  görselin 33'ü harita değil; haritaların "Maps of ..." kategorisi var,
  diğerlerinin yok.
* **Yönlendirme ve dil farkı yakalanır.** "Harezmşahlar" görselsiz bir
  yönlendirmedir (doğrusu "Harezmşahlar Devleti"); Türkçe maddede harita yoksa
  dil bağlantısından İngilizce karşılığına bakılır, o da yoksa başlık önerisi
  basılır. Yanlış başlık verirseniz araç **yanlış haritayı da bulabilir** —
  listede yazar/lisans/ölçüyle birlikte gösterilir, seçim SİZİNDİR.

### Neden görüntü modeli yok (ÖLÇÜLDÜ — geri getirmeyin)

Bir görüntü modeline harita **çizdirme** yolu 2026 Ağustos'ta terk edildi:
model kıyıyı ezberden benzetiyor, şehri uyduruyor. Ölçülen hatalar: Hazar
Denizi üç haritada imparatorluk sınırının İÇİNDE kaldı; Cend, Seyhun yerine
Hazar kıyısına düştü.

Sonra "hiç değilse gerçek bir haritanın RENGİNİ değiştirsin" diye daha dar bir
yol denendi. **O da 2026-08-31'de ölçülüp kapatıldı** — iki modelde birden:

| Model | Sonuç |
|---|---|
| `bytedance/seedream/v5/pro/edit` | Etiketler eridi: `Al-Ruha` → "Aldbla", `Harran` → "Idbrran" |
| `openai/gpt-image-2/edit` | Renk ve coğrafya iyi, kesikli sınır korundu — **ama yazılar yine bozuldu**: `HALAB (ALEPPO)` → "MALAK ALAKFBD)", `Ba'albakk` → "Bathaslih", `Dimashq` → "Aagmub" ve **`(Occupied in 1426)` → `(occupied in 1405)`** |

Sonuncusu kritiktir: model bir **tarihi sessizce değiştirdi**. Ders kitabında
bu, taşmadan beterdir — sayfa düzgün görünür, öğrenci yanlış bilgiyi doğru
sanır.

Sayısal bir kapı da bunu kurtaramaz. gpt-image-2 çıktısı çözünürlük (1792 px)
ve en-boy (%0,33 sapma) ölçütlerini geçti, toprak IoU'da **%94,1** ile
%95 eşiğinin 0,9 puan altında kaldı — yani reddedildi ama **alakasız bir
gerekçeyle**. Yazıların erimesini üç ölçütten hiçbiri görmüyor; IoU %95,2
çıksaydı "1405" yazan harita kitaba girecekti.

`tools/harita_uret.py` ve `assets/harita/uretilmis/` bu yüzden SİLİNDİ.
Dersin rengine çekme işi determinist yolla yapılır (aşağıda) — o yol tonu
kaydırıp parlaklığı koruduğu için bir harfe dokunması fiziksel olarak
mümkün değildir.


### Sınır çıkarma: `--sinir-cikar`

Kaynağın renkli alanını gerçek koordinata çevirir; sonuç `territory`
olur ve harita `harita_cizim.py` ile ÇİZİLİR.

```bash
python tools/harita.py --sinir-cikar memluk-sultanligi-1317.jpg
```

Yaptığı: çapalardan izdüşümü çözer → artık hataları basar → renk maskesini
çıkarır → gürültüyü temizler → Moore sınır izleme + Douglas-Peucker →
`assets/harita/sinir/<ad>.json` (lon/lat halkaları) + **bindirme görseli** yazar.
Sonuç `MapBox.territory` alanına konur ve harita `harita_cizim.py` ile ÇİZİLİR.

#### Çapa noktaları — işin tek elle yapılan kısmı

Tarihî haritaların izdüşümü dosyada YAZMAZ, çıkarımı yapmak için haritada yeri
bilinen noktalar gerekir. Bunlar kaynağın YANINDA, metin olarak yaşar:
`assets/harita/commons/<dosya>.capa.json`. Bir kez yazılır, git'e girer,
kaynak değişmedikçe yeniden kullanılır.

```json
{"kirp": [700, 80, 1780, 1500], "ton": [140, 175], "capalar": [
  {"ad": "Kahire", "lon": 31.235, "lat": 30.044, "x": 0.195, "y": 0.392}
]}
```

`x`/`y` KIRPILMIŞ görselin oranıdır (vektör kaynakta dosyadan okunur,
bkz. aşağısı). `ton`,
kaynağın toprak renginin derece aralığıdır; ÖLÇÜN, tahmin etmeyin.

**Gürültü halkalarına dikkat:** kaynağın dağ gölgeleri toprak rengiyle aynı
ton aralığına düşebilir (ölçüldü: Hârezmşâhlar haritasında Zagros ve Hindukuş
gölgeleri 4 sahte halka üretti). `--en-az <piksel>` ile küçük bileşenleri
eleyin; `--en-az 3000` o haritada yalnız gerçek sınırı bıraktı.

**En az 6 çapa verin (tercihen 8-12) ve HARİTANIN DÖRT BİR YANINA DAĞITIN.**
6'nın altında araç yalnızca afin çözüme düşer ve bunu uyarı olarak söyler.
Ölçüldü (2026-08-31, Memlük haritası): kuzeyde kümelenmiş **3 çapayla** afin
çözüm güneye inildikçe sistematik olarak doğuya kaydı —

| Nokta | Kayma |
|---|---|
| İskenderiye | ~25 px |
| Uswan | ~130 px |
| Sawakin | ~200 px |
| **Mekke** | **~240 px = %22 ≈ 4-5° boylam** |

Sebep: kaynak eşuzaklık değil, meridyenleri güneye doğru açılan koni benzeri
bir izdüşümdedir. **12 çapa + 2. derece polinom** ile aynı harita: en büyük
artık %1,18, ortalama %0,37 (≈4 px).

#### Artık raporunu OKUYUN

Araç her çapanın artığını basar ve `ARTIK_ESIGI`'ni (%1,2) aşanı işaretler.
Büyük artık üç şeyden birini söyler: (a) o çapanın oranı yanlış okundu,
(b) lon/lat yanlış, (c) çapalar kümelenmiş. Ölçülen örnek: "Ibrim" çapası
%2,36 artık verdi, listeden çıkarılınca en büyük artık %1,18'e indi —
yani araç yanlış okumamı kendisi buldurdu.

#### Polinom derecesi: KUADRATİK TAVANDIR (kübiği denemeyin)

Araç 6+ çapada 2. dereceye geçer, daha yükseğine ÇIKMAZ. Hârezmşâhlar
haritasında (15 çapa, ~25° boylam) ölçülen en büyük artıklar: afin %2,44 ·
kuadratik %1,49 · **kübik %1,16**. Sayıya bakıp kübiğe geçmek cazip görünüyor
ve bir kez geçildi de — ama `bindirme.png` şunu gösterdi: kübik uyum
**çapaların dışında savruluyor** (Runge olgusu). Kuzey sınırı haritanın
dışına düz bir çizgi hâlinde fırladı, güney sınırı Basra Körfezi'ne taştı.
Kuadratik aynı haritada her yerde alanı düzgün izliyor.

**Ders:** artık hatası yalnızca ÇAPA NOKTALARINDA ölçülür; çapasız bölgede ne
olduğunu söylemez. Bu yüzden sayısal ölçüt tek başına asla yetmez.

#### Çok katmanlı alan: genişleme evreleri

Tarihî haritaların çoğu tek sınır değil, **dönem dönem genişleme** gösterir
(Rum Selçuklu 4 bant: 1100/1174/1182/1240 · Moğol 7 bant). Hepsini tek
poligona indirmek kaynağın asıl bilgisini — NE ZAMAN nereye yayıldığını —
yok eder. Bunun yerine her renk bandı ayrı çıkarılır ve `MapBox.katmanlar`
alanına ESKİDEN YENİYE konur; çizim en eskiyi en koyu tonla basar ve
etiketleri kutunun altındaki HTML lejanta taşır.

```python
katmanlar=katman_yukle("rum-selcuklu-genisleme-1100-1240"),
```

**Vektör kaynakta renk BİREBİR eşlenir**, ton penceresiyle değil:
`svg_rasterlestir()` SVG'yi Chromium ile 1800 px'e basar, `renk_maskesi()`
kaynağın düz vektör rengini tam değerle arar. Raster kaynaklarda pencere
gerekiyordu çünkü arazi gölgesi rengi sürekli kaydırıyordu. Tolerans ÖNEMLİ:
Moğol haritasında komşu bantlar kanal başına yalnızca ~9 birim farklıdır;
tolerans 8'de iki bandın maskesi 1526 pikselde çakışırken **tolerans 4'te
çakışma sıfırdır**.

#### Çapaları GÖZLE okumayın — vektör kaynakta dosyadan okuyun

Moğol İmparatorluğu haritası bir kez "çıkarılamaz" ilan edilmişti: 17 çapa
küçültülmüş ızgaradan gözle okunmuş, ortalama artık %2,77 / en büyük %8,3
çıkmıştı. Boylam eğimi ölçülüp (Kostantiniyye→Bağdat 0,247 %/derece,
Kaifeng→Hangzhou 1,947 %/derece — sekiz kat fark) "sorun izdüşümde değil
OKUMADA" teşhisi konmuştu. **Teşhis doğruydu, sonuç yanlıştı:** çözüm haritadan
vazgeçmek değil, okumayı bırakmaktı.

Kaynak VEKTÖRSE çapa koordinatı dosyanın içinde tam değer olarak yazılıdır.
Bu haritada şehirler `<use xlink:href="#New_Symbol_2" transform="matrix(...)">`
ile basılmış; 65 noktanın konumu matristen alınıp en yakın `<text>` etiketiyle
eşleştirildi (çoğu 4 px içinde eşleşti, ikinci en yakın etiket 20+ px uzakta —
yani eşleşmeler tekildi). Aynı harita, aynı izdüşüm modeli:

| | gözle okuma (17 çapa) | dosyadan okuma (34 çapa) |
|---|---|---|
| ortalama artık | %2,77 | **%0,66** |
| en büyük artık | %8,3 | **%1,79** |

`Capa.x/y` hâlâ kırpılmış görselin oranıdır; değişen tek şey o oranın nereden
geldiği. Raster kaynakta gözle okumak zorundasınız — orada çapaları dört bir
yana dağıtmak (bkz. yukarıdaki Memlük ölçümü) tek savunmanızdır.

Kalan %1,79'u kovalamayın: 34 çapa haritanın dört bir yanına dağılmış
durumda, yani artık modelin yarım küre ölçeğindeki sınırıdır, okuma hatası
değil. Üç çapayı (Esztergom, Bolgar, Seul) tek tek çıkarmak denendi — en
büyük artık %1,83 ve %1,89'a ÇIKTI. Kuadratik hâlâ tavandır (bkz. yukarısı).


#### Sahte halkalar: `--tek-parca`

Kaynağın arazi gölgeleri toprakla AYNI ton aralığına düşebilir ve mutlak
eşikle (`--en-az`) elenemeyecek kadar büyük sahte parçalar üretir. Ölçüldü
(Delhi haritası): Himalayalar 11.039 ve 3.768 pikselik iki halka verdi —
gerçek sınırın %34'ü ve %12'si. Devlet tek parçaysa `--tek-parca` verin,
yalnızca en büyük alan tutulur. Ada/eksklav içeren bir devlette KULLANMAYIN.

#### Bindirme görseli atlanamaz

`assets/harita/sinir/<ad>.bindirme.png` çıkarılan sınırı KAYNAĞIN ÜSTÜNE
çizer. Sayısal hiçbir ölçüt "maske yanlış yeri seçti" demez: kaynakta komşu
bir devlet AYNI tonda boyanmışsa maske onu da alır ve sonuç sessizce yanlış
olur. Kırmızı çizgi kaynağın renkli alanını izliyor mu — gözle bakın.

#### Atıf yükümlülüğü DEVAM EDER

Sınır CC BY-SA bir haritadan türetilmiştir. Kendi motorumuzla çizmek onu
"bizim çizimimiz" yapmaz; `MapBox.source` alanına kaynağın künyesi yazılır.
Bu, `territory`nin normalde "yaklaşık" olan durumundan da farklıdır: burada
sınır ELLE TAHMİN EDİLMEMİŞTİR, kartografın çizgisidir — ama kesikli kenar
yine de kalır, çünkü kaynağın kendisi de sınırı yaklaşık ilan ediyor.

### Kendi çizdiğimiz haritanın kullanımı

```python
.add_map(MapBox(
    region="Hârezmşâhlar Devleti (1097-1231)",
    bbox=(46.0, 28.5, 75.0, 48.5),          # (batı, güney, doğu, kuzey)
    cities=[
        Place("Gürgenç", 59.15, 42.34),      # DİKKAT: sıra lon, lat
        Place("Buhara", 64.42, 39.77, sag=False),   # etiket noktanın soluna
    ],
    neighbors=[Place("Kara-Hıtaylar", 72.0, 44.5)], # "\n" ile satır bölünür
    territory=[[(52.5, 40.5), (54.5, 44.0), ...]],  # YAKLAŞIK, (lon, lat)
    caption="Kutunun altındaki tek satır açıklama",
), yan=[BulletBlock(1, "Coğrafi Bağlam", [...])], taraf="sag")
```

Çizimi `cekirdek/harita_cizim.py` yapar: bağımlılık yoktur (GeoJSON `json`
ile okunur, izdüşüm ve SVG saf Python'dur), çıktı SVG'dir, üretim ücretsiz
ve **deterministiktir**.

**Kutu oranı `bbox`'tan TÜRETİLİR**, sabit değildir (`oran_hesapla`). Eskiden
sabit 4:3'tü ve dikey coğrafyaları eziyordu: Memlük (Mısır+Şam+Hicaz) ve Delhi
(Hint alt kıtası) kutunun ortasına dar bir şerit hâlinde sıkışıp sağını solunu
boş bırakıyor, sayfanın altında da büyük bir boşluk açıyordu. Ölçülen düzelme:
82 mm'lik sütunda Memlük kutusu 62 -> **107 mm**, Delhi 62 -> **89 mm**.
Oran `ORAN_EN_DAR` (0,72) ile `ORAN_EN_GENIS` (1,60) arasına kırpılır —
alt sınır kutunun sayfaya sığdığı, üst sınır haritanın okunur kaldığı yerdir.

| Katman | Kaynak | Güvenilirlik |
|---|---|---|
| Kıyı, kara, göl, nehir | Natural Earth 1:50m (kamu malı / CC0) | gerçek veri |
| Şehir konumları | `Place(ad, lon, lat)` — elle yazılan gerçek koordinat | doğrulanabilir |
| Devlet/bölge alanı | `MapBox.territory` — elle yazılan kaba poligon | **yaklaşık** |

`yan=` listesi BulletBlock, Callout, ComparisonTable, FlowDiagram, Person ve
`list[KeyTerm]` kabul eder. Tüm çağrı TEK bir item'dır: `tools/olcum.py` ve
`tools/dengele.py` onu bölünemez blok olarak görür (ölçülen yükseklik: yan
yana kipte ~88-104mm, `taraf="tam"` kipinde harita oranına bağlı).

`taraf`: `"sag"` (varsayılan) / `"sol"` — metnin yanında iki sütun;
`"tam"` — sayfa genişliğinde, metin altında akar.

**Koordinat sırası `lon, lat`'tır** (GeoJSON düzeni). Ters yazarsanız harita
sessizce bozulur; `validate()` çerçeve dışına düşen her işareti uyarı olarak
basar, ama doğru çerçeve içinde yanlış yere düşen bir noktayı yakalayamaz —
`--onizle` ile gözle denetleyin.

### `territory` dürüstlük meselesidir

Ortaçağ siyasi sınırları için **serbest ve yetkeli bir veri kümesi yoktur**:
Natural Earth bugünün sınırlarıdır, CShapes 1886'da başlar, Euratlas
lisanslıdır, OpenHistoricalMap'in kapsamı deliktir. Bu yüzden alan poligonu
elle, kaba hatlarla yazılır ve çizimde üç şeyle "yaklaşık" olduğu söylenir:

1. **Kesikli kenar** — kartografyada "sınır kesin değil" demektir.
2. **Yumuşatma** (Chaikin) — genelleştirilmiş hat, ölçülmüş sınır gibi durmaz.
3. **Kutu altındaki kaynak satırı** (`MapBox.source`, `.geomap-source`) —
   her kutuda basılır, kaldırmayın.

**Sahte atıf YAZMAYIN** (sayfa numaralı uydurma atlas künyesi). `source`
alanının varsayılanı iddiayı zaten doğru kurar.

Alan dolgusu **karaya kırpılır** (`clipPath`): elle yazılan kaba poligon
kıyıyı birebir izleyemez, kırpma olmadan denize sarkar ve "deniz de bu
devletin toprağıydı" gibi okunur. Göller dolgunun ÜSTÜNE çizilir, böylece
bir göl boyanamaz.

### Komutlar

```bash
python tools/harita.py --veri-indir                                     # bir kez (Natural Earth)
python tools/harita.py --commons "<Vikipedi maddesi>"                   # kaynak harita ara
python tools/harita.py --commons "<madde>" --sec N --ders <slug>        # indir + künye + kod parçası
python tools/harita.py --sinir-cikar <dosya.jpg>                        # sınırı lon/lat poligonuna çevir
python tools/harita.py --tara   <slug> --sinif X --donem Y --sinav Z    # aday bölümler
python tools/harita.py --onizle <slug> --sinif X --donem Y --sinav Z    # haritaları dosyaya yaz
```

`assets/harita/*.geojson` (3 MB) ve Commons raster kaynakları `.gitignore`'dadır;
klonlayan kişi `--veri-indir` / `--commons` ile alır. Veri yoksa **build
DURMAZ** — aynı ölçüde bir yer tutucu basılır ve indirme komutunu söyleyen bir
uyarı verilir. SVG kaynaklar METİN olduğu için git'te kalır.

### Otomatik tespit — ÖNERİR, İÇERİK ÜRETMEZ

`--tara` her bölümü puanlar ama harita içeriğini (şehir listesi, koordinat,
sınır) ASLA otomatik doldurmaz; onu kaynağa bakarak siz yazarsınız — harita
metinde geçmeyen bir şehri göstermemelidir.

Puanlama **önce kapı, sonra puan** çalışır. Kapıdan geçmek için gerçek mekân
kanıtı gerekir: "Coğraf..." ile başlayan bir alt başlık, VEYA en az 2 farklı
*çekimli* mekân ismi ("Hazar **Denizi**", "Ceyhun **Nehri**"), VEYA 1 mekân
ismi + 1 toprak hareketi ("fethetti", "istila"). Kapı kapalıysa puan 0'dır.

İki tuzak bilerek kapatıldı — kaldırmayın:
* **Özel ad yoğunluğu tek başına yeterli DEĞİLDİR.** Her bölümde onlarca
  büyük harfli sözcük (kişi adı, kavram, eser) vardır; yalnızca ona bakan
  ilk sürüm Psikoloji'nin 5 bölümünü de "aday" ilan etmişti.
* **Niteleyici mekân isimleri önlerinde ÖZEL AD ister.** "Hârezm bölgesi"
  coğrafyadır, "beynin bölgesi" değildir. Ayrıca hareket kelimeleri kelime
  sınırıyla aranır — düz arama "akın"ı **y**akın içinde buluyordu.

Ölçülen ayrım: İslam Tarihi III 5/5 bölüm aday · Psikoloji, Sosyoloji,
Edebiyat, Öğretim İlke ve Yöntemleri 0 · Çağdaş Felsefe 1/7.

## Test + Cevap Anahtarı (sınav bölümü — GÜNCEL format)

`pack.test_questions` doluysa şablon otomatik olarak bu formatı render eder
(banner + 3'lü bilgi çubuğu "20 Soru / Çoktan Seçmeli / 5 Seçenek" + talimat
kutusu + numaralı sorular; ardından ayrı bir "Cevap Anahtarı ve Çözümler"
bölümü). 20 soru standarttır ama sayı serbesttir. Her soru 4 veya 5 seçenekli
olabilir. Aynı dönemin `src/sosyoloji.py` ve `src/psikoloji.py`'sindeki
`test_questions`/`answer_key_items` listelerini şablon olarak kullanın.

`pack.test_questions` boş bırakılırsa (yazmazsanız) şablon otomatik olarak
eski LEGACY "Sınav Hazırlık" formatına düşer — bu sadece 2 eski örnek
dersin (ogretim_teknolojileri/sanat_tarihi) bozulmadan çalışmaya
devam etmesi içindir. **Yeni bir ders yazarken her zaman `test_questions`/
`answer_key_items` kullanın, `distinctions`/`match_table`/`qa_items` değil.**

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
        ders_klasoru="SİSTEMATİK KELAM I",   # klasör adı — kaynaklar/ altındakiyle birebir
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
GLOSSARY_PER_PAGE = 22     # sözlük sayfası başına kavram (2 sütun)
QA_PER_PAGE = 12           # LEGACY
DISTINCTIONS_PER_PAGE = 8  # LEGACY
MATCHTABLE_PER_PAGE = 11   # LEGACY
TEST_PER_PAGE_FIRST = 7    # ilk test sayfası (bilgi çubuğu + talimat kutusu var)
TEST_PER_PAGE = 8          # test devam sayfaları
ANSWER_PER_PAGE = 23       # cevap anahtarı sayfası başına çözüm (20 soru -> tek sayfa)
TOC_COMPACT_THRESHOLD = 7  # bu kadar satırı aşınca İçindekiler sıkışık kipe geçer
OVERVIEW_PAGES = 1         # Genel Bakış TEK sayfa
```

Bu değerler **175×250mm için `tools/kalibre.py` ile ÖLÇÜLDÜ**: her aday sayı
10 dersin hepsinde render edilip taşma denetiminden geçirildi, taşmayan en
büyük değer alındı. Tahminle değiştirmeyin — sayfa boyutu değişirse
`python tools/kalibre.py` çalıştırıp bloğu yenileyin.

Bölme işini `paginate_capped()` yapar, düz `paginate()` değil: önce gereken
en az sayfa sayısını bulur, sonra öğeleri **dengeli** dağıtır. Böylece 30
kavram `12+12+6` yerine `10+10+10` olur — son sayfa yarı boş kalmaz.
İçindekiler bu mekanizmayı hiç kullanmaz, çünkü asla bölünmez (bkz. aşağıdaki
"İçindekiler TEK SAYFADIR" kuralı).

Test ve Cevap Anahtarı bölümleri **2 sütunlu** düzende render edilir
(`templates/style.css` içinde `.tq-list`/`.ans-list` → `column-count: 2`,
`column-fill: balance`; her madde `break-inside: avoid` ile bir sütunda
bölünmeden kalır).

### KRİTİK KURAL 4: İçindekiler TEK SAYFADIR

**İçindekiler ASLA ikinci bir sayfaya taşmaz** — ders kaç bölümlü olursa
olsun, kapaktan sonra tek bir İçindekiler sayfası gelir. `toc_page_count()`
sabit `1` döndürür ve `ctx.toc_pages` tek parçadır; "İçindekiler · Devam"
diye bir sayfa artık ÜRETİLMEZ.

Sığdırma işini sayfa bölme değil, **CSS sıkışık kipi** yapar. Satır sayısı
(`bölüm sayısı + 2`) `TOC_COMPACT_THRESHOLD`'u aşarsa şablon `toc-list`'e
`toc-compact` sınıfını ekler ve şunlar olur:

- `toc-lede` (alt başlık cümlesi) gizlenir
- satır dolgusu 4.6mm → 3mm, numara dairesi 9.4mm → 7.6mm küçülür
- **alt başlık tek satıra kırpılır** (`white-space:nowrap` + ellipsis)

Son madde kritiktir: uzun bir alt başlık ferah kipte iki-üç satıra sarıp
satırı ~29.6mm'ye çıkarabilir; kırpma sayesinde sıkışık kipte satır
yüksekliği **sabittir** ve taşma yapısal olarak imkânsızdır.

**A4 ölçümü** (Chromium, Kelâm Tarihi / 11 satır üzerinde):

| | |
|---|---|
| Sayfada satırlara kalan yer | **232,4 mm** |
| Ferah satır | 20,7 mm (sarma ile ~29,6 mm — belirsiz) |
| Sıkışık satır | **16,4 mm — sabit** (alt başlık kırpık) |
| Ferah kapasite (en kötü satıra göre) | 232,4 / 29,6 = **7 satır** → `TOC_COMPACT_THRESHOLD = 7` |
| Sıkışık kapasite (kesin) | 232,4 / 16,4 = **14 satır** → `TOC_MAX_ROWS = 14` |

Eşik neden 7'de kalıyor: ferah kipte alt başlık sarabildiği için satır
yüksekliği ÖNCEDEN bilinemez, bu yüzden eşik en kötü satıra göre hesaplanır.
Sıkışık kipte kırpma yüzünden yükseklik sabit olduğundan kapasite kesindir —
ferahlık, eşiği yükselterek değil sıkışık kipin kendisini rahatlatarak
kazanılır (2026 Ağustos: `.toc-compact` blok değerleri A4 ölçeğine çekildi;
Kelâm Tarihi'nin listesi 133,6 → 178,2 mm oldu, punto 8,23 → 10 pt).

**14 satır (= 12 bölüm) aşılırsa** `validate()` derlemeden önce net bir uyarı
basar (`TOC_MAX_ROWS`); o noktada satırı daha da sıkıştırmak yerine dersi
bölmeyi değerlendirin. `.toc-compact` değerlerini elle küçültmeyin — bu
sabitler ölçümle bağlıdır, birini değiştirirseniz diğerini de yeniden ölçün.

**Genel Bakış da tek sayfadır.** Dört bloğu (hero + 6 kart + çalışma akışı +
sınav notu) A4'te rahat sığar (`OVERVIEW_PAGES = 1`) — Genel Bakış'a blok
eklerseniz taşma denetimini yine de okuyun.

Sayfa numaraları `compute_page_numbers()` içinde buna göre hesaplanır; bir
dersin ön sayfaları `1 + toc_page_count(pack) + OVERVIEW_PAGES` = **her zaman
3** tanedir (kapak + içindekiler + genel bakış).

## Birleşik Kitap (`build_kitap.py`)

Tek tek üretilen derslerin hepsini, **kesintisiz sayfa numaralarına sahip tek
bir cilt** halinde birleştirir. Dersleri kopyalamaz — her dersin
aynı dönemin `src/<slug>.py` dosyasını taze okur; bir derste düzeltme yapıp kitabı
yeniden derlemek, tüm numaraları/içindekileri/yer imlerini otomatik günceller.

```bash
python build_kitap.py --sinif X --donem Y --sinav Z   # o dönemin src/kitap.py sırasına göre
```

### Kitaba yeni ders eklemek
> Bu bölüm YALNIZCA kullanıcı açıkça "birleşik kitaba ekle / kitabı güncelle /
> birleştirmeyi çalıştır" dediğinde uygulanır (bkz. en üstteki KRİTİK KURAL).
> Bir ders üretmek, bu adımı kendiliğinden TETİKLEMEZ.

İLGİLİ DÖNEMİN `src/kitap.py` dosyasındaki `COURSE_MODULES` listesine
**tek satır** ekle (çıplak modül adı, `content.` öneki YOK):
```python
COURSE_MODULES = [
    "tefsir2",
    ...
    "yeni_ders",     # <- eklenen
]
```
Başka hiçbir yeri elle güncellemek gerekmez (sayfa numaraları, ana
içindekiler, ders haritası, kapak istatistikleri, yer imleri — hepsi hesaplanır).

### Kitabın yapısı
| Bölüm | İçerik |
|---|---|
| Ön kısım | Ana kapak · Künye · Bu Kitap Nasıl Kullanılır · Sayfa Rehberi · Ana İçindekiler · Ders Haritası |
| Gövde | Her ders, tek ders PDF'iyle BİREBİR aynı sayfalarla (kapak → içindekiler → genel bakış → bölümler → sözlük → test → cevap anahtarı) |

Ön kısım sayfa sayısı ders sayısına göre kendini ayarlar: 11 derse kadar ana
içindekiler tek sayfa (ön kısım 6 sayfa), 12+ derste dengeli iki sayfa
(ön kısım 7 sayfa). Bu sayı `front_matter_page_count()` ile derslerden ÖNCE
hesaplanır, çünkü ilk dersin sayfa offset'i buna bağlıdır.

### Kitabın metinleri
Kapak başlığı, künye satırları, önsöz kartları, rehber ve harita açıklamaları
o dönemin `src/kitap.py` dosyasındaki `BookPack` alanlarındadır. Ders içeriğiyle
karıştırma — orada bir dersin bilgisi DEĞİL, kitabın kendi tanıtımı yazılır.

### Mimari: iki çıktı, tek şablon
```
_ders_govde.html.j2   (bir dersin tüm sayfaları — TEK KAYNAK)
    ├── master.html.j2   -> tek ders PDF'i (offset=0, anchor öneki yok)
    └── kitap.html.j2    -> kitap (her derse offset + "d3-" anchor öneki + tema kapsamı)
```
`build.py`'deki `course_context(pack, offset, prefix, pagecls)` her iki yolu da
besler; sayfalama mantığı ikiye ayrılmadığı için "tek derste doğru, kitapta
yanlış numara" durumu yapısal olarak imkânsızdır.

### Otomatik denetimler (hepsi build çıktısında görünür)
1. **Taşma denetimi** — tek derstekiyle aynı; kitapta ayrıca taşan sayfanın
   HANGİ dersin kaçıncı sayfası olduğu yazdırılır.
2. **Sayfa numarası zinciri** — dersler boşluksuz/çakışmasız mı, hesaplanan
   toplam PDF'in gerçek sayfa sayısıyla ve kapaktaki istatistikle aynı mı.
3. **Render doğrulaması** — bkz. aşağıdaki 10 numaralı tuzak.
4. **Boyut optimizasyonu** — `optimize_pdf()`, tekrar eden görsel nesneleri
   birleştirir (kitapta 36.4 MB → 20.0 MB, tek derste ~%26). Sayfa ya da yer
   imi sayısı değişirse değişikliği geri alır.

Bunlardan biri hata verirse **PDF'i teslim etme** — önce sebebini bul.

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

## Tasarım sistemi özeti (referans amaçlı — değiştirmen gerekmemeli)

- Gövde fontu DejaVu Sans, başlıklar DejaVu Serif (kitap/akademik his).
- Her tema kendi `--accent`, `--accent-dark`, `--gold`, `--paper` (hafif
  tonlu, beyaz değil) setini tanımlar; callout renkleri
  (`focus/caution/insight/route`) tema-bağımsız sabittir. 5 sabit isimli
  tema (`indigo/burgundy/forest/slate/plum`) hâlâ var, ama `theme_color`
  ile `cekirdek/theme_engine.py` üzerinden SINIRSIZ sayıda özel renk üretilebilir
  (bkz. "Renk Teması" bölümü) — sabit sınıflar artık bir seçenek, zorunluluk
  değil.
- Kapak: çok katmanlı gradient + döner amblem (halka + saat çentikleri +
  sunburst) + 4 köşede ince "cilt" süsü + dev soluk motif harfi.
- **SAYFA ARKA PLANI DÜZDÜR — nokta deseni/doku YOKTUR.** Hem kapakta hem iç
  sayfalarda (içindekiler, genel bakış, bölümler, sözlük, test, cevap
  anahtarı) eskiden düşük opaklıklı bir nokta matrisi (`.body-page::before`
  ve `.cover::before` üzerinde tekrarlayan `radial-gradient`) vardı; 2026
  Ağustos'unda kullanıcı isteğiyle KALDIRILDI. İç sayfaların zemini artık
  yalnızca `--paper` tonu, kapağınki yalnızca gradyan katmanlarıdır. Yeni bir
  bileşen eklerken sayfa arka planına nokta/doku/desen **ekleme**; bu iki
  kuralı geri getirme. (Bölüm banner'ının kendi içindeki çok hafif doku
  `.chbanner::before` bir KUTU dokusudur, sayfa zemini değildir ve bilerek
  bırakılmıştır.)
- Her sayfa A4 (210×297mm, bleed yok), `.page` sınıfı `overflow:hidden` — taşma her
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
# Tek dersi derle (A4, RGB — fotokopi için)
python build.py <slug> --sinif X --donem Y --sinav Z

# Aynı ders, matbaa için PDF/X-4 CMYK olarak
python build.py <slug> --sinif X --donem Y --sinav Z --cmyk

# Sayfa doluluğunu ölç / bölüm sayfalarını yeniden dağıt / sabitleri kalibre et
python tools/olcum.py <slug> --sinif X --donem Y --sinav Z
python tools/dengele.py <slug> --sinif X --donem Y --sinav Z   # --kuru = sadece raporla
python tools/kalibre.py --sinif X --donem Y --sinav Z          # sayfa boyutu değiştiyse

# Harita: hazır kaynak bul/indir · veriyi indir · aday tara · önizle · imleç denetle
python tools/harita.py --commons "<Vikipedi maddesi>"
python tools/harita.py --commons "<madde>" --sec N --ders <slug>
python tools/harita.py --sinir-cikar <dosya.jpg>
python tools/harita.py --veri-indir
python tools/harita.py --tara <slug> --sinif X --donem Y --sinav Z
python tools/harita.py --onizle <slug> --sinif X --donem Y --sinav Z

# Ghostscript + ICC profili teşhisi
python cekirdek/pdfx.py

# BİR DÖNEMİN tüm derslerini tek kitap halinde derle (src/kitap.py sırasına göre)
python build_kitap.py --sinif X --donem Y --sinav Z

# Belirli sayfaları PNG'ye çevirip incele
pdftoppm -png -r 100 -f <ilk> -l <son> "<D>/gorsel_ders_notlari/<DERS ADI>/<slug>.pdf" "<D>/gorsel_ders_notlari/preview/pg"

# Tüm sayfaları çevir
pdftoppm -png -r 100 "<D>/gorsel_ders_notlari/<DERS ADI>/<slug>.pdf" "<D>/gorsel_ders_notlari/preview/pg"

# Bookmark/link doğrulaması
python3 -c "
from pypdf import PdfReader
r = PdfReader('<D>/gorsel_ders_notlari/<DERS ADI>/<slug>.pdf')
for it in r.outline: print(it.title, '->', r.get_destination_page_number(it)+1)
"

# Tema paleti önizlemesi (hangi renklerin kullanıldığını görmek için)
python cekirdek/theme_engine.py
```

## Özet — bir ders eklerken zihinsel kontrol listesi

- [ ] Sınıf/dönem/sınav'ı kullanıcıya SORDUM (varsaymadım)
- [ ] Kaynak eklenmediyse o dönemin `kaynaklar/ders_kaynaklari/` (ve
      `ogretmen_notlari/`) klasöründe ders adıyla eşleşen dosyayı aradım
      (yoksa kullanıcıdan istedim — başka döneme BAKMADIM)
- [ ] Ham metni tamamen okudum (atlamadım)
- [ ] 5-7 bölüme, ham içeriğin doğal yapısını takip ederek ayırdım
- [ ] Kullanılmamış bir renk seçtim (`theme_color=` hex, aynı dönemin
      `src/` dizinindeki diğer derslerden görsel olarak ayrışan), tek harfli
      Latin `icon_text` verdim
- [ ] `<D>/src/<slug>.py` yazdım, `cekirdek/content_model.py` API'sine birebir uydum
      (başındaki `sys.path` satırı `parents[4]` olmalı — düz kipte `parents[2]`;
      import `from cekirdek.content_model import ...` biçimindedir)
- [ ] `ders_klasoru=` alanını doldurdum ve `kaynaklar/` altındaki ders
      klasörü adıyla BİREBİR aynı yazdım
- [ ] 20 soruluk `test_questions` + eşleşen `answer_key_items` yazdım
      (LEGACY `distinctions`/`match_table`/`qa_items` DEĞİL)
- [ ] `python build.py <slug> --sinif X --donem Y --sinav Z` çalıştırdım
- [ ] "[TAŞMA UYARISI]" çıkmayana kadar `tools/dengele.py` çalıştırıp
      yeniden derledim (gerekirse elle sayfa böldüm)
- [ ] Konsoldaki "[SONUÇ] Bitmiş (trim) ölçü : 210 x 297 mm" satırını gördüm
      (renk kipi: "[prepress] Çıktı RGB bırakıldı (fotokopi kipi)" — matbaa
      için --cmyk verildiyse onun yerine PDF/X-4 dönüşümünün "✓"sü)
- [ ] Kapak (yeni renk doğru mu?) + içindekiler + genel bakış + her bölüm
      ilk sayfası + en az bir tablo sayfası + sözlük son sayfası + test
      son sayfası + cevap anahtarı son sayfası görsel kontrol ettim
- [ ] Her bölümün TÜM sayfalarını (özellikle devam sayfalarını) tek tek
      inceleyip devam sayfalarının (son sayfa hariç) %90-95 dolulukta
      olduğunu doğruladım; gerekirse komşu sayfalar arasında mevcut
      içeriği taşıdım/birleştirdim — asla yeni içerik uydurmadım, taşan
      denemeleri geri aldım
- [ ] Coğrafi bölüm varsa `tools/harita.py --tara` ile adayları gördüm; hazır
      harita gerekiyorsa `--commons "<madde>"` ile buldum (LISANS.md künyesi
      otomatik yazıldı) ve build çıktısındaki "[harita] N harita kutusu ...
      0 eksik" satırını gördüm
- [ ] Yeni bir sınır çıkardıysam `assets/harita/sinir/<ad>.bindirme.png`
      dosyasına GÖZLE baktım (kırmızı çizgi kaynağın renkli alanını izliyor
      mu) ve artık raporunu okudum — yanlış bir maske SESSİZDİR, ne taşma
      denetimi ne validate() onu yakalar
- [ ] Bookmark/link sayısını doğruladım
- [ ] (SADECE kullanıcı açıkça istediyse — bkz. en üstteki KRİTİK KURAL;
      istemediyse bu adımı ATLA ve kitaba dokunma) Yeni dersi
      O DÖNEMİN `src/kitap.py` dosyasındaki `COURSE_MODULES` listesine
      çıplak adıyla ekledim ve `python build_kitap.py --sinif X --donem Y --sinav Z`
      ile o dönemin birleşik kitabını yeniden derledim; taşma,
      sayfa zinciri ve render doğrulamalarının hepsi "✓" verdi
- [ ] Çıktının `<D>/gorsel_ders_notlari/<DERS ADI>/` altına düştüğünü
      konsoldaki "[build] Ders klasörü:" satırından doğruladım
- [ ] PDF'i kullanıcıya sundum
