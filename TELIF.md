# Telif ve Lisans

Bu depoda **iki farklı türde içerik** vardır ve bunlar **ayrı ayrı**
lisanslanmıştır. Depoyu kullanmadan önce ikisini de okuyun.

---

## 1. Sistem — GNU GPL v3

Aşağıdakiler **GNU Genel Kamu Lisansı 3. sürüm** ile lisanslanmıştır:

```
build.py · build_kitap.py · content_model.py · theme_engine.py
renk_uretici.py · pdfx.py · donem.py
templates/ (style.css ve tüm .j2 şablonları) · tools/
dersler/src/ornek_ders.py
```

`ornek_ders.py` bilerek GPL kapsamındadır: içeriği sistemin kendi
belgelerinden yazılmış özgün bir metindir, hiçbir ders kitabından
türetilmemiştir. Kendi dersinizi yazarken onu kopyalayabilirsiniz.

Copyright (C) 2026 Numan Gözdaş

Lisansın tam metni: [`LICENSE`](LICENSE)

**Ne yapabilirsiniz:** Kullanabilir, inceleyebilir, değiştirebilir,
dağıtabilir ve ticari olarak kullanabilirsiniz.

**Karşılığında ne yapmalısınız:** Bu sistemden türettiğiniz bir çalışmayı
dağıtırsanız, o çalışma da **GPL v3 altında ve kaynak koduyla birlikte** açık
kalmak zorundadır. Telif bildirimlerini kaldıramaz, lisansı değiştiremezsiniz.

Bu, tasarım sisteminin kapalı ticari bir ürüne dönüştürülmesini engeller.
Sistemi kendi ders notlarınızı üretmek için kullanmanızın önünde ise hiçbir
engel yoktur — kendi kullanımınız için ürettiğiniz PDF'ler bu şartın
kapsamına girmez; yükümlülük ancak **sistemi (ya da ondan türeteni) başkasına
dağıtırsanız** doğar.

---

## 2. Ders içerikleri — Tüm hakları saklıdır

Ders modüllerinin (`ornek_ders.py` hariç) **metinsel içeriği** (ders özetleri, bölüm metinleri, kavram tanımları, test
soruları ve çözümleri) **GPL kapsamı DIŞINDADIR** ve tüm hakları saklıdır.

Bu ayrımın sebebi: bu metinler üniversite ders kitaplarından ve öğretim
üyelerinin anlatımlarından türetilmiş özetlerdir. Yazarı olmadığım bir
materyalden türeyen içeriği özgür lisansla dağıtmak, sahip olmadığım hakları
devretmek olurdu.

Bu modüller **depoya dahil değildir** — sınıf ağaçlarıyla birlikte
`.gitignore` kapsamındadır ve yalnızca yazarın kendi bilgisayarında bulunur.
Bu madde, depoyu klonlayıp kendi derslerini yazacak kişiler için değil, o
içeriğin başka bir yolla eline geçtiği durumlar için geçerlidir.

Sisteme yeni bir ders eklerken örnek almanız gereken dosya
`dersler/src/ornek_ders.py`'dir; o dosya GPL kapsamındadır ve serbestçe
kopyalanabilir.

---

## 3. Depoda bulunmayanlar

Aşağıdakiler `.gitignore` kapsamındadır ve depoya dahil değildir:

- `kaynaklar/` — ham ders materyalleri (üçüncü taraf telifli olabilir)
- `gorsel_ders_notlari/`, `calisma_rehberleri/`, `ders_anlatimlari/` —
  üretilmiş PDF çıktıları
- `<n>-sinif/` — kişisel sınıf/dönem çalışma ağaçları ve içlerindeki
  ders modülleri

Gerekçe için `README.md` → "Depoda ders PDF'leri neden yok?" bölümüne bakın.

---

## 4. Üçüncü taraf bileşenler

**Fontlar depoda gelmez.** Tasarım DejaVu Sans / DejaVu Serif kullanır ve
bunlar işletim sisteminden okunur; depoda font dosyası dağıtılmaz.

> Not: `fonts/ArabicExtracted-*.ttf` dosyaları (ve onlarla birlikte hiç
> kullanılmayan `arabic_reshape.py`) 2026 Ağustos'unda silindi.
> Kodun hiçbir yerinden kullanılmıyorlardı ve içlerinde telif/lisans kaydı
> bulunmuyordu (bir PDF'ten çıkarılmış alt küme olduklarına işaret eder).
> Kaynağı belirsiz içeriği dağıtmamak için kaldırıldılar.

**ICC renk profili depoda gelmez.** FOGRA39 ("ISO Coated v2") profili lisans
onayı gerektirdiği için eci.org'dan ayrıca indirilir; bkz.
`assets/icc/README.md`.

**Çalışma zamanı bağımlılıkları** (jinja2, pypdf, pymupdf, pdfplumber,
Playwright, Ghostscript) depoda değildir, kurulum sırasında kendi
lisanslarıyla indirilir; bkz. `KURULUM.md`.

---

## İletişim

Lisans kapsamı dışında bir kullanım için (örneğin ders içeriklerini kullanmak
ya da sistemi GPL dışında bir lisansla kullanmak) telif sahibiyle iletişime
geçin.
