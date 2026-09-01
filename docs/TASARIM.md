# Tasarım sistemi ve renk motoru

Tasarım (HTML şablonu + CSS) **sabittir ve olgunlaşmıştır.** Yeni bir ders
üretirken tasarımı değiştirmeyin, sadece içerik ekleyin. Bu dosya, tasarımın
nasıl kurulduğunu ve renk motorunun nasıl çalıştığını anlatır — bir bileşen
eklemeniz veya bildirilen bir tasarım hatasını düzeltmeniz gerekirse
başvuru kaynağıdır.

Düzeltme yapılacak yerler (TÜM derslerde paylaşılır):
`templates/style.css` · `templates/_ders_govde.html.j2`

> Bu dosya CLAUDE.md'den ayrıldı: renk motorunun iç işleyişi her oturumda
> gerekmez. Ders yazarken gereken tek şey, doğru hex'i tablodan almaktır —
> o komut CLAUDE.md'de duruyor.

---

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

