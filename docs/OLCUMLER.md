# Ölçümler ve sabitler — bu sayılar nereden geldi

Sistemdeki sayfa geometrisi ve sayfalama sabitleri **tahminle değil ölçümle**
belirlendi: her aday değer Chromium'da render edilip taşma denetiminden
geçirildi, taşmayan en büyük değer alındı. Bu dosya o ölçümlerin ve
arkalarındaki kararların kaydıdır.

**Bir sabiti değiştirmeden önce burayı okuyun.** Sayfa boyutu değişirse
tahminle düzeltme yapmayın:

```bash
python tools/kalibre.py --sinif X --donem Y --sinav Z    # sabitleri yeniden ölçer
python tools/dengele.py --hepsi --sinif X --donem Y --sinav Z   # sayfaları yeniden dağıtır
```

> Bu dosya CLAUDE.md'den ayrıldı: ölçüm gerekçesi her oturumda gerekmez,
> sabiti değiştirirken gerekir.

---

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

