# Görsel Ders Notu Üretim Sistemi

Üniversite derslerinin ham metin özetlerini, baskıya hazır **görsel ders notu
kitabı** PDF'ine çeviren bir üretim hattı. Çıktı; kapak, içindekiler, genel
bakış, numaralı bölümler (terim kutuları, kişi kartları, karşılaştırma
tabloları, akış şemaları, vurgu kutuları), kavramlar sözlüğü ve 20 soruluk
çoktan seçmeli test + çözümlü cevap anahtarından oluşur.

Ders içeriği HTML/CSS'te değil, **Python veri modelinde** yazılır
(`content_model.py`). Tasarım tek bir yerde durur (`templates/`), içerik ise
her ders için ayrı bir modülde. Bu yüzden tasarımda yapılan bir düzeltme tüm
derslere birden uygulanır.

## Hızlı başlangıç

Sistemi yeni indirdiyseniz sırasıyla şunları yapın (~10-15 dk):

```bash
git clone https://github.com/ByNuman/ders-uretim-sistemi.git
cd ders-uretim-sistemi

pip install -r requirements.txt      # Python paketleri
npm install                          # PDF'i Chromium render eder
npx playwright install chromium      # ~150 MB, sadece ilk kurulumda

python build.py ornek_ders            # örnek dersi derle
```

Son komut 13 sayfalık örnek bir ders PDF'i üretir. Ürettiyse kurulum
tamamdır. Ayrıca **Ghostscript** kurmanız önerilir (matbaa için CMYK
dönüşümü) — yoksa sistem yine çalışır, PDF sadece RGB kalır.

**Adım adım anlatım, işletim sistemine göre kurulum ve sorun giderme için:
[`KURULUM.md`](KURULUM.md)**

## Ne üretir

| Çıktı | Komut |
|---|---|
| Tek dersin görsel ders notu PDF'i | `python build.py <slug> --sinif X --donem Y --sinav Z` |
| Bir dönemin tüm derslerini içeren birleşik kitap | `python build_kitap.py --sinif X --donem Y --sinav Z` |
| Bir sınıfın tüm ders kapaklarının renk önizlemesi | `python tools/kapak_onizleme.py --sinif 3` |

Baskı özellikleri: **175 × 250 mm** bitmiş (trim) ölçü, 3 mm taşma payı,
ayna simetrik kenar boşlukları, gerçek PDF yer imleri ve otomatik
**PDF/X-4 (DeviceCMYK)** dönüşümü.

## Depoda ders PDF'leri neden yok?

Bu depo **sistemi** içerir, ders çıktılarını değil. İki sebeple:

1. **Çıktılar yeniden üretilebilir.** Bir dersin gerçek içeriği
   `<dönem>/src/<ders>.py` modülüdür; PDF her zaman ondan yeniden derlenir.
   Üretilmiş PDF'i depoda tutmak, aynı bilgiyi ikinci kez ve ikili (binary)
   biçimde saklamak olurdu — git ikili dosyaları sıkıştıramadığı için her
   yeniden derleme depoya tam bir kopya daha eklerdi.
2. **Ham ders kaynakları kişiseldir.** `kaynaklar/` altındaki materyal
   başkalarının ders notları/telifli metinleri olabilir; yayınlanmaz.

Bu yüzden `gorsel_ders_notlari/`, `calisma_rehberleri/`, `ders_anlatimlari/`
ve `kaynaklar/` altındaki dosyalar `.gitignore`'dadır; yalnızca klasör
iskeleti (`.gitkeep`) depoda durur. **Kendi kaynak dosyalarınızın yedeğini
ayrıca alın — bu depo onların yedeği değildir.**

## Kurulum

Ayrıntılı, adım adım kurulum rehberi ayrı bir dosyadadır:
**[`KURULUM.md`](KURULUM.md)** — işletim sistemine göre komutlar, her adım
için doğrulama ve sık karşılaşılan hatalar.

Özet gereksinimler:

| Yazılım | Sürüm | Zorunlu mu? |
|---|---|---|
| Python | 3.10+ | Evet |
| Node.js | 18+ | Evet (PDF render'ı Chromium yapar) |
| Ghostscript | 9+ | Hayır — yoksa PDF RGB kalır, build durmaz |

Kurulumu doğrulamak için:

```bash
python pdfx.py        # Ghostscript + ICC profili teşhisi
```

### ICC profili (matbaa için, opsiyonel)

CMYK dönüşümü `assets/icc/ISOcoated_v2_eci.icc` (FOGRA39) profilini kullanır.
Profil lisans onayı gerektirdiği için depoda gelmez; yoksa Ghostscript'in
genel CMYK profiline düşülür ve uyarı basılır. Bkz. `assets/icc/README.md`.

## Klasör yapısı

Bütün çalışma tek bir `dersler/` klasöründe olur:

```
dersler/
├── kaynaklar/
│   ├── ders_kaynaklari/<DERS ADI>/     # GİRDİ: ham ders metni / kaynak PDF
│   ├── ogretmen_notlari/<DERS ADI>/    # GİRDİ: dağınık dikte notu
│   └── özetlenmiş_dersler/<DERS ADI>/  # ARA:   yukarıdakilerden çıkarılan yazılı özet
├── src/                                # <ders>.py içerik modülleri
├── gorsel_ders_notlari/<DERS ADI>/     # ÇIKTI: PDF + HTML
├── calisma_rehberleri/<DERS ADI>/      # ÇIKTI: çalışma rehberi
└── ders_anlatimlari/<DERS ADI>/        # ÇIKTI: ders anlatımı
```

Paylaşılan altyapı kökte durur: `build.py` · `build_kitap.py` ·
`content_model.py` · `theme_engine.py` · `renk_uretici.py` · `pdfx.py` ·
`templates/` · `tools/`

### İsteğe bağlı: sınıf / dönem / sınav ağacı

Birden fazla sınıf ve sınav dönemini ayrı ayrı yönetmek isterseniz sistem
`<sinif>-sinif/<donem>-donem/<sinav>/` ağacını da destekler. Bu ağaç
kurulduğunda her komut üç parametreyi birlikte ister:

```bash
python build.py <ders> --sinif 2 --donem 2 --sinav final
```

Böylece aynı ders farklı dönemlerde bağımsız sürümler halinde tutulabilir
(ör. bir dersin vize ve final kitabı ayrı renkte ve ayrı içerikte olur) ve
`build_kitap.py` bir dönemin tüm derslerini tek ciltte birleştirir.

Sınıf ağacı diskte yoksa sistem kendiliğinden `dersler/` kipine geçer;
açıkça seçmek için `--duz` bayrağını kullanın.

## İlk dersinizi üretmek

1. `dersler/src/ornek_ders.py` dosyasını kopyalayın ve içeriğini değiştirin.
   Bu örnek, sistemin kendisini anlatır ve kullanılabilecek bütün blokları
   (terim kutusu, madde listesi, tablo, vurgu kutusu, akış şeması, sözlük,
   test) örnekler. Tek dışa verilen şey `get_pack() -> CoursePack`'tir.
2. Derleyin:
   ```bash
   python build.py yeni_ders
   ```
3. Konsoldaki **taşma denetimi** çıktısını okuyun. Taşma varsa sayfaları
   otomatik yeniden dağıtın:
   ```bash
   python tools/dengele.py yeni_ders
   ```

Veri modelinin tam API referansı ve üretim sürecinin adım adım kuralları
`CLAUDE.md` içindedir.

## Renkler

Her dersin vurgu rengi tek bir hex'ten türetilir; `theme_engine.py` kapak
gradyanından tablo başlığına kadar tüm tonları otomatik üretir. Ders renkleri
`renk_uretici.py` içindeki `DERS_RENKLERI` tablosunda **önceden
belirlenmiştir** ve ilke "renk = dersin ruhu"dur.

```bash
python renk_uretici.py --tablo               # belirlenmiş ders renkleri
python theme_engine.py                       # hazır palet önizlemesi
python tools/kapak_onizleme.py --sinif 3     # kapakları tek PDF'te gör (sınıf ağacı kipi)
```

## Araçlar

```bash
python tools/olcum.py <ders>     # sayfa doluluğunu ölçer
python tools/dengele.py <ders>   # sayfaları taşmayacak biçimde yeniden dağıtır
python tools/kalibre.py          # sayfa boyutu değiştiyse sabitleri yeniden ölçer
```

## Lisans

Bu depoda iki tür içerik vardır ve **ayrı ayrı** lisanslanmıştır:

| Ne | Lisans |
|---|---|
| **Sistem** — `build.py`, `templates/`, `theme_engine.py`, `tools/` … | **GNU GPL v3** ([`LICENSE`](LICENSE)) |
| **Ders içerikleri** — `<dönem>/src/*.py` içindeki metinler | Tüm hakları saklıdır |

Copyright (C) 2026 Numan Gözdaş

Sistemi kullanabilir, değiştirebilir ve dağıtabilirsiniz; karşılığında ondan
türettiğiniz çalışma da GPL v3 altında açık kalmak zorundadır. **Kendi ders
notlarınızı üretmek bu şartın kapsamına girmez** — yükümlülük ancak sistemi
(ya da ondan türeteni) başkasına dağıtırsanız doğar.

Ders modülleri depoda yalnızca **örnek** olarak bulunur; üniversite ders
kitaplarından türetilmiş özetler oldukları için serbest lisansla dağıtılamaz.
Yapılarını örnek alıp kendi derslerinizi yazabilirsiniz, metinleri
kopyalayamazsınız.

Ayrıntılı açıklama ve üçüncü taraf bileşenler: **[`TELIF.md`](TELIF.md)**
