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
  (17,5×25cm) DEĞİL — bu iki değer birbirinden bağımsız olmalı ve
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

### Kökte kalan paylaşılan altyapı (döneme ait DEĞİL, asla kopyalanmaz)

```
build.py · build_kitap.py · donem.py · content_model.py · theme_engine.py
pdfx.py · renk_uretici.py · arabic_reshape.py · templates/ · tools/ · fonts/ · assets/
```

Bu dosyalar TÜM dönemler tarafından paylaşılır. `templates/style.css` veya
`templates/_ders_govde.html.j2` üzerinde bir düzeltme yaparsan **her sınıfın
her döneminin** çıktısını etkilersin — bu kasıtlıdır (tasarım tek kaynaktır),
ama dönem-özel bir "düzeltme" yapmaya çalışma.

### Ders modülleri neden noktalı yolla import edilmiyor?

`2-sinif` geçerli bir Python paket adı değildir, bu yüzden eski
`content.kelam_tarihi` biçimi artık kullanılamaz. `donem.py`, seçilen dönemin
`src/` klasörünü `sys.path`'in başına koyar ve modül **çıplak adıyla**
(`kelam_tarihi`) import edilir. Eski noktalı yazım yine de kabul edilir
(önek atılır), ama yeni kodda çıplak ad kullan.

Bir `src/*.py` dosyasının başındaki

```python
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
```

satırı proje köküne (`content_model.py`'nin bulunduğu yere) çıkar —
`src/ -> <sinav> -> <donem> -> <sinif> -> KÖK` = 4 seviye. Yeni bir ders
dosyası yazarken bu satırı olduğu gibi kopyala; `parents[1]` yazarsan
`content_model` bulunamaz.

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

## Sayfa boyutu, taşma payı ve kenar boşlukları (BASKI GEOMETRİSİ)

Çıktı **A4 DEĞİLDİR**. Kitap kapağıyla eşleşen ölçü:

| | |
|---|---|
| Bitmiş (trim) ölçü | **175 × 250 mm** |
| Taşma payı (bleed) | **3 mm** (her kenar) — render/MediaBox 181 × 256 mm |
| Üst / alt kenar | 11 mm / 19 mm (alt, sayfa numarası payı dahil) |
| İç (sırt/gutter) / dış kenar | 14 mm / 9 mm — **ayna simetrik** |
| Metin alanı | 152 × 220 mm |
| Gövde punto | **7,9 pt** (eski 9,6 pt'nin 0,8229 katı) |

Ayna simetri: TEK sayfalar (1, 3, 5…) sağ yapraktır, sırtı SOLDADIR; çift
sayfalarda tersi. PUR Amerikan cilt için iç kenar dıştan 5 mm geniştir.
(DİKKAT: 14 mm sırt payı PUR cilt için sıkıdır — matbaa 15-18 mm isterse
`MARGIN_INNER_MM`'i artırıp `tools/kalibre.py` + `tools/dengele.py --hepsi`
zincirini tekrar çalıştırın.)

`templates/style.css` içindeki tüm tipografi/boşluk/çizgi ölçüleri 2026
Ağustos'unda tek seferde **0,8229 ile ölçeklendi** (gövde 9,6 → 7,9 pt);
kapak sayfası ve sayfa geometrisi bu ölçeklemenin dışında bırakıldı. Yeni
bir bileşen eklerken ölçüleri bu skalaya uydurun.

**İKİ AYRI CONFIG vardır ve birbirinden bağımsızdır** (bkz. en üstteki
KRİTİK KURAL). `build.py`'nin başındaki `PageGeometry` dataclass'ından iki
örnek üretilir:

| Config | Kullanan | Şu anki trim |
|---|---|---|
| `SINGLE_GEOMETRY` | `python build.py <slug> --sinif X --donem Y --sinav Z` (tekil ders) | 175 × 250 mm |
| `BOOK_GEOMETRY` | `python build_kitap.py --sinif X --donem Y --sinav Z` (birleşik kitap) | 175 × 250 mm |

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

Bleed GEREKLİDİR: hem kapak gradyanı hem gövde sayfalarının `--paper` zemin
tonu tam sayfayı kaplar (full-bleed). `pdfx.set_print_boxes()` PDF'e
CropBox/BleedBox = 181×256 mm, **TrimBox = 175×250 mm** yazar; matbaa kesim
yerini TrimBox'tan okur. (ArtBox bilerek yazılmaz — PDF/X bir sayfada
TrimBox VEYA ArtBox ister, ikisini birden değil.)

## Otomatik PDF/X-4 CMYK dönüşümü

`build.py` ve `build_kitap.py`, PDF'i üretip yer imlerini ekledikten hemen
sonra `pdfx.convert_or_warn()` çağırır: çıktı Ghostscript ile **RGB'den
PDF/X-4 (DeviceCMYK)**'ya çevrilir. Ara RGB dosya geçici klasörde kalır ve
silinir — kullanıcının elindeki
`<D>/gorsel_ders_notlari/<DERS ADI>/<slug>.pdf` doğrudan CMYK'dır.

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
├── donem.py                # SINIF/DÖNEM/SINAV çözümleyici — tüm scriptlerin ortak girişi
├── content_model.py        # Veri şeması (dataclass'lar) — API referansı aşağıda
├── build.py                # TEK DERS: HTML üret → PDF render → küçült → bookmark → kutular → CMYK
├── build_kitap.py          # BİRLEŞİK KİTAP: bir dönemin tüm derslerini tek ciltte birleştirir
├── pdfx.py                 # BASKI ÖNCESİ: TrimBox/BleedBox + Ghostscript ile PDF/X-4 CMYK
├── theme_engine.py         # Sınırsız renk teması motoru (tek hex'ten tam tema üretir)
├── renk_uretici.py         # DERSE ÖZEL VURGU RENGİ — build.py + ders-anlatim skill'inin ORTAK kaynağı
├── tools/
│   ├── olcum.py            # Her bloğun GERÇEK yüksekliğini (mm) Chromium'da ölçer
│   ├── dengele.py          # Ölçüme göre ChapterPage bölünmelerini yeniden dağıtır
│   └── kalibre.py          # Sözlük/Test/Cevap sayfa başına öğe sabitlerini kalibre eder
├── templates/
│   ├── _ders_govde.html.j2      # BİR DERSİN GÖVDESİ — asıl şablon, tek kaynak (sabit)
│   ├── master.html.j2            # Tek ders sarmalayıcısı (13 satır — _ders_govde'yi çağırır)
│   ├── kitap.html.j2             # Kitap sarmalayıcısı (ön kısım + tüm dersler)
│   ├── _kitap_on_kisim.html.j2   # Kitabın kapak/künye/önsöz/rehber/içindekiler/harita sayfaları
│   └── style.css                  # Tasarım sistemi (sabit — dokunma, sadece bug varsa düzelt)
├── assets/icc/             # FOGRA39 ("ISO Coated v2") ICC profili buraya konur (bkz. README)
├── fonts/
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
Aşağıdaki "content_model.py API Referansı" bölümüne birebir uyarak yaz.
Mevcut derslerden birini (`2-sinif/2-donem/final/src/sosyoloji.py` iyi bir orta-karmaşıklıkta
örnektir) şablon olarak kopyalayıp değiştirmek en hızlı yoldur.

Her ders için ayrıca:
- **Renk teması sınırsızdır**: `theme_color="#7A2438"` gibi TEK bir hex renk
  verin — `theme_engine.py` tüm tonları (kapak gradyanı, banner, tablo
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
tekrar eden terim var mı) → Playwright ile PDF'e render eder → **her sayfanın
gerçek render yüksekliğini 181×256mm sınırıyla karşılaştırır** → PDF'e gerçek
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
  için o dönemin `src/tefsir2.py` dosyasına bak. Ham Arapça Unicode metni doğrudan
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
TOC_ROWS_FIRST = 7         # İçindekiler ilk sayfası
TOC_ROWS_REST = 8          # İçindekiler devam sayfaları
OVERVIEW_PAGES = 1         # Genel Bakış TEK sayfa
```

Bu değerler **175×250mm için `tools/kalibre.py` ile ÖLÇÜLDÜ**: her aday sayı
10 dersin hepsinde render edilip taşma denetiminden geçirildi, taşmayan en
büyük değer alındı. Tahminle değiştirmeyin — sayfa boyutu değişirse
`python tools/kalibre.py` çalıştırıp bloğu yenileyin.

Bölme işini `paginate_capped()` yapar, düz `paginate()` değil: önce gereken
en az sayfa sayısını bulur, sonra öğeleri **dengeli** dağıtır. Böylece 30
kavram `12+12+6` yerine `10+10+10` olur — son sayfa yarı boş kalmaz. Tek
istisna İçindekiler'dir (`balanced=False`): bir kitabın içindekiler sayfası
dolu başlayıp kısa bir taşmayla biter, ortadan ikiye bölünmüş iki yarım
sayfa yanlış görünür.

Test ve Cevap Anahtarı bölümleri **2 sütunlu** düzende render edilir
(`templates/style.css` içinde `.tq-list`/`.ans-list` → `column-count: 2`,
`column-fill: balance`; her madde `break-inside: avoid` ile bir sütunda
bölünmeden kalır).

**İçindekiler çok sayfalı olabilir; Genel Bakış tek sayfadır.** Küçültülmüş
punto + genişletilmiş metin alanında Genel Bakış'ın dört bloğu (hero + 6 kart
+ çalışma akışı + sınav notu) tek sayfaya sığar (`OVERVIEW_PAGES = 1`); en
yüklü ders olan Öğretim İlke ve Yöntemleri'nde ~%97 doluluk verir, yani
marj dardır — Genel Bakış'a blok eklerseniz taşma denetimini mutlaka okuyun.
İçindekiler `ctx.toc_pages` üzerinden sayfalanır. Sayfa numaraları
`compute_page_numbers()` içinde buna göre hesaplanır — bir dersin ön
sayfaları artık sabit 3 değil, `1 + toc_page_count(pack) + OVERVIEW_PAGES`
tanedir.

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
    OutputIntent) 3.9 MB / PDF 1.6 / 22 sn. `pdfx.py` bilerek `-dPDFX`
    KULLANMAZ; geri eklerseniz dosya şişer ve kapak gradyanları rasterleşir.

14. **Ghostscript'in varsayılan görsel ayarları kapak gradyanını 22 dpi'a
    düşürüyordu**: `pdfwrite`'ın downsample varsayılanları Chromium'un gömdüğü
    tam sayfa rasterleri eziyor. `pdfx.py` bu yüzden `-dDownsample*Images=false`
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
    köşesinden ölçtüğü için TrimBox tam 175×250mm çıkıyor. (Chromium levhayı
    yine ~0.02-0.12mm büyük üretir; MediaBox bu yüzden BleedBox'tan birkaç
    yüzde mm büyüktür — bu normaldir, MediaBox'a dokunulmaz.)

17. **Dar sayfada flex sütunlarında uzun kelimeler taşıyor**: 175mm'de 5
    adımlı akış şemasında sütun ~22mm'ye düşüyor ve "Varoluşçuluğa" gibi
    kelimeler kutunun dışına sarkıyordu (flex öğesi min-content'in altına
    inemez). `.ov-flow-step` ve `.flowdiag .fstep` bu yüzden
    `min-width: 0; overflow-wrap: break-word;` taşır — kaldırmayın.

18. **`add_ayat()` başlığı artık opsiyoneldir**: uzun bir ayet grubu (Tefsir
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
  ile `theme_engine.py` üzerinden SINIRSIZ sayıda özel renk üretilebilir
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
# Tek dersi derle (PDF/X-4 CMYK çıktı dahil)
python build.py <slug> --sinif X --donem Y --sinav Z

# Sayfa doluluğunu ölç / bölüm sayfalarını yeniden dağıt / sabitleri kalibre et
python tools/olcum.py <slug> --sinif X --donem Y --sinav Z
python tools/dengele.py <slug> --sinif X --donem Y --sinav Z   # --kuru = sadece raporla
python tools/kalibre.py --sinif X --donem Y --sinav Z          # sayfa boyutu değiştiyse

# Ghostscript + ICC profili teşhisi
python pdfx.py

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
python3 theme_engine.py
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
- [ ] `<D>/src/<slug>.py` yazdım, `content_model.py` API'sine birebir uydum
      (başındaki `sys.path` satırı `parents[4]` olmalı)
- [ ] `ders_klasoru=` alanını doldurdum ve `kaynaklar/` altındaki ders
      klasörü adıyla BİREBİR aynı yazdım
- [ ] 20 soruluk `test_questions` + eşleşen `answer_key_items` yazdım
      (LEGACY `distinctions`/`match_table`/`qa_items` DEĞİL)
- [ ] `python build.py <slug> --sinif X --donem Y --sinav Z` çalıştırdım
- [ ] "[TAŞMA UYARISI]" çıkmayana kadar `tools/dengele.py` çalıştırıp
      yeniden derledim (gerekirse elle sayfa böldüm)
- [ ] Konsoldaki "[SONUÇ] Bitmiş (trim) ölçü : 175 x 250 mm" satırını ve
      PDF/X-4 CMYK dönüşümünün "✓" verdiğini gördüm
- [ ] Kapak (yeni renk doğru mu?) + içindekiler + genel bakış + her bölüm
      ilk sayfası + en az bir tablo sayfası + sözlük son sayfası + test
      son sayfası + cevap anahtarı son sayfası görsel kontrol ettim
- [ ] Her bölümün TÜM sayfalarını (özellikle devam sayfalarını) tek tek
      inceleyip devam sayfalarının (son sayfa hariç) %90-95 dolulukta
      olduğunu doğruladım; gerekirse komşu sayfalar arasında mevcut
      içeriği taşıdım/birleştirdim — asla yeni içerik uydurmadım, taşan
      denemeleri geri aldım
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
