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

python build.py sosyoloji --sinif 2 --donem 2 --sinav final
```

Son komut 22 sayfalık örnek bir ders PDF'i üretir. Ürettiyse kurulum
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

Dosyalar **sınıf / dönem / sınav dönemi** ağacında tutulur. Hiçbir script'in
varsayılan dönemi yoktur; her komut `--sinif` `--donem` `--sinav` üçlüsünü
birlikte alır.

```
<sinif>-sinif/<donem>-donem/<sinav>/
├── kaynaklar/
│   ├── ders_kaynaklari/<DERS ADI>/     # GİRDİ: ham ders metni / kaynak PDF
│   ├── ogretmen_notlari/<DERS ADI>/    # GİRDİ: öğretmenin dağınık dikte notu
│   └── özetlenmiş_dersler/<DERS ADI>/  # ARA:   yukarıdakilerden çıkarılan yazılı özet
├── src/                                # <ders_slug>.py içerik modülleri + kitap.py
├── gorsel_ders_notlari/<DERS ADI>/     # ÇIKTI: PDF + HTML
├── calisma_rehberleri/<DERS ADI>/      # ÇIKTI: çalışma rehberi
└── ders_anlatimlari/<DERS ADI>/        # ÇIKTI: ders anlatımı
```

Paylaşılan altyapı kökte durur ve tüm dönemler tarafından ortak kullanılır:
`build.py` · `build_kitap.py` · `content_model.py` · `theme_engine.py` ·
`renk_uretici.py` · `pdfx.py` · `templates/` · `tools/` · `fonts/`

## İlk dersinizi üretmek

1. `<dönem>/src/yeni_ders.py` dosyasını yazın. Şablon olarak
   `2-sinif/2-donem/final/src/sosyoloji.py` iyi bir orta-karmaşıklıkta
   örnektir. Tek dışa verilen şey `get_pack() -> CoursePack` fonksiyonudur.
2. Derleyin:
   ```bash
   python build.py yeni_ders --sinif 2 --donem 2 --sinav final
   ```
3. Konsoldaki **taşma denetimi** çıktısını okuyun. Taşma varsa sayfaları
   otomatik yeniden dağıtın:
   ```bash
   python tools/dengele.py yeni_ders --sinif 2 --donem 2 --sinav final
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
python tools/kapak_onizleme.py --sinif 3     # kapakları tek PDF'te gör
```

## Araçlar

```bash
python tools/olcum.py <slug>  --sinif X --donem Y --sinav Z   # sayfa doluluğunu ölçer
python tools/dengele.py <slug> --sinif X --donem Y --sinav Z  # sayfaları yeniden dağıtır
python tools/kalibre.py        --sinif X --donem Y --sinav Z  # sayfa boyutu değiştiyse
```

## Lisans

Belirlenmedi. Depodaki kod ve tasarım sistemi yazarına aittir; ders
içerikleri ve ham kaynaklar depoya dahil değildir.
