# Kurulum ve İlk Çalıştırma

Bu dosya, sistemi bilgisayarına yeni indiren biri için baştan sona kurulum
rehberidir. Sırayla takip edin; her adımın sonunda doğrulama komutu vardır.

Toplam süre: **10-15 dakika** (çoğu Chromium indirmesi). Kapladığı yer:
depo 4 MB + Node paketleri ~20 MB + Chromium ~150 MB + Ghostscript ~60 MB.

---

## Neye ihtiyacınız var

| Yazılım | Sürüm | Ne işe yarıyor | Zorunlu mu? |
|---|---|---|---|
| **Python** | 3.10+ | Üretim hattının kendisi | **Evet** |
| **Node.js** | 18+ | PDF render'ı Chromium yapar (Playwright üzerinden) | **Evet** |
| **Ghostscript** | 9+ | RGB → PDF/X-4 CMYK dönüşümü, yalnızca `--cmyk` verilirse | Hayır — matbaaya iş göndermeyecekseniz gereksiz |

Python 3.10 alt sınırı keyfi değil: kod `int | None` biçimli tip
gösterimlerini çalışma zamanında kullanıyor, bu söz dizimi 3.10 ile geldi.

---

## 1. Adım — Depoyu indirin

```bash
git clone https://github.com/ByNuman/ders-uretim-sistemi.git
cd ders-uretim-sistemi
```

Git kullanmıyorsanız GitHub'daki **Code → Download ZIP** ile indirip açın.

**Doğrulama:** `ls` çıktısında `build.py`, `templates/`, `2-sinif/` görmelisiniz.

---

## 2. Adım — Python paketleri

Sanal ortam kullanmanız önerilir (sistem Python'unuzu kirletmez):

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

Sonra bağımlılıkları kurun:

```bash
pip install -r requirements.txt
```

Kurulan paketler: `jinja2` (şablonlar), `pypdf` (yer imleri, doğrulama),
`pymupdf` (sayfa kutuları, optimizasyon), `pdfplumber` (kaynak PDF'lerden
metin çıkarma).

**Doğrulama:**
```bash
python -c "import jinja2, pypdf, pymupdf; print('Python paketleri tamam')"
```

---

## 3. Adım — Node.js ve Chromium

PDF'i tarayıcı motoru üretir, bu yüzden Node tarafı da gerekli.

```bash
npm install
npx playwright install chromium
```

İkinci komut ~150 MB indirir ve birkaç dakika sürebilir — **bu normaldir ve
yalnızca ilk kurulumda olur.** Chromium sisteminizde ortak bir önbelleğe
iner, depo klasörüne değil.

**Doğrulama:**
```bash
node -e "require('playwright'); console.log('Playwright tamam')"
```

---

## 4. Adım — Ghostscript (çoğu kullanıcı için gereksiz)

Yalnızca **matbaaya** gidecek CMYK çıktısı (`--cmyk`) için gerekir. Varsayılan
çıktı zaten **A4 RGB**'dir ve doğrudan fotokopiye/ofis yazıcısına gider —
fotokopi için bu adımı atlayabilirsiniz.

```bash
# macOS
brew install ghostscript

# Ubuntu / Debian
sudo apt install ghostscript

# Windows
# ghostscript.com/releases/gsdnld.html adresinden installer indirin
```

**Doğrulama:**
```bash
python cekirdek/pdfx.py
```

Bu komut Ghostscript'i ve ICC profilini bulup sürümlerini yazdırır.
Ghostscript kurulu ama bulunamıyorsa (PATH'te değilse), tam yolu bir ortam
değişkenine yazın:

```bash
# Windows (PowerShell)
$env:DERS_GS = "C:\Program Files\gs\gs10.07.1\bin\gswin64c.exe"

# macOS / Linux
export DERS_GS=/usr/local/bin/gs
```

---

## 5. Adım — İlk dersinizi üretin

Depoda `ornek_ders` adında, sistemin kendisini anlatan bir örnek ders gelir.
Onu derleyerek kurulumu uçtan uca test edin:

```bash
python build.py ornek_ders
```

Beklenen çıktının son satırları:

```
[build] Taşma denetimi: tüm sayfalar 210x297mm sınırları içinde. ✓
[prepress] Çıktı RGB bırakıldı (fotokopi kipi).
[SONUÇ] Toplam sayfa: 13
[SONUÇ] Bitmiş (trim) ölçü : 210 x 297 mm
```

PDF şuraya düşer:
`dersler/gorsel_ders_notlari/ÖRNEK DERS/gorsel-ders-notu-sistemi.pdf`

Bunu görüyorsanız **kurulum tamamdır.** Üretilen PDF aynı zamanda sistemin
kullanım kılavuzudur: kendi dersinizi yazarken `dersler/src/ornek_ders.py`
dosyasını kopyalayıp içeriğini değiştirin.

---

## Sık karşılaşılan sorunlar

### `Cannot find module 'playwright'`
`npm install` çalıştırılmamış ya da komutu deponun kök klasöründe
çalıştırmıyorsunuz. `package.json`'ın bulunduğu dizine geçip `npm install`
yapın.

### Playwright "tarayıcı bulunamadı / executable doesn't exist" diyor
`npm install` yapılmış ama tarayıcının kendisi indirilmemiş — bunlar ayrı iki
adımdır. `npx playwright install chromium` çalıştırın (3. adım).

### `[hata] --sinif verilmedi ve interaktif olarak sorulamıyor.`
Bu mesajı yalnızca **sınıf/dönem/sınav ağacını** kurduysanız görürsünüz. O
ağaç varken sistem varsayılan bir dönem seçmez — yanlış döneme sessizce
yazmak geri alması zor bir hatadır. Üç parametreyi birlikte verin:

```bash
python build.py <ders> --sinif 2 --donem 2 --sinav final
```

Terminalde çalışıyorsanız zaten size sorar. Script/CI içinde
`DERS_SINIF`, `DERS_DONEM`, `DERS_SINAV` ortam değişkenlerini de
kullanabilirsiniz. Düz `dersler/` klasörüne dönmek için: `--duz`.

### `[UYARI] FOGRA39 profili bulunamadı`
Normaldir, hata değil. Matbaa FOGRA39 istemiyorsa görmezden gelin. İstiyorsa
"ISO Coated v2 (ECI)" profilini eci.org'dan indirip
`assets/icc/ISOcoated_v2_eci.icc` olarak kaydedin (lisans onayı gerektirdiği
için depoda gelmez). Farklı bir konum için `DERS_ICC` ortam değişkeni.

### `[TAŞMA UYARISI] N sayfa ... sınırını aşıyor`
İçeriğiniz sayfaya sığmıyor demektir ve **görmezden gelinmemelidir** — PDF
sessizce içerik kaybeder. Otomatik çözüm:

```bash
python tools/dengele.py <ders> --sinif X --donem Y --sinav Z
```

### Ürettiğim PDF'i commit edemiyorum
Kasıtlı: `gorsel_ders_notlari/`, `calisma_rehberleri/`, `ders_anlatimlari/`
ve `kaynaklar/` altındaki dosyalar `.gitignore`'dadır. Sebebi ve gerekçesi
için `../README.md` → "Depoda ders PDF'leri neden yok?" bölümüne bakın.

### Windows'ta Türkçe karakterler bozuk görünüyor
Konsol kod sayfası sorunudur, üretilen PDF'i etkilemez. İsterseniz
`chcp 65001` ile konsolu UTF-8'e alabilirsiniz.

---

## Sırada ne var

- **Kendi dersinizi eklemek:** `dersler/src/ornek_ders.py` dosyasını
  kopyalayın; ayrıca `../README.md` → "İlk dersinizi üretmek"
- **Veri modelinin tam API referansı ve üretim kuralları:** `CLAUDE.md`
- **Ders renkleri:** `python cekirdek/renk_uretici.py --tablo`
