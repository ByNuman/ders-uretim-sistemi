"""Hazır Commons haritasını OLDUĞU GİBİ sayfaya gömer.

TEK İŞ: kaynağı aç, (istenirse) kırp, sütun genişliğine küçült, gömülebilir
bir veri URI'si üret. Görüntünün İÇİNE dokunulmaz -- çeviri yok, renk kaydırma
yok, etiket silme yok. Eklenecek her şey (Türkçe ad anahtarı, açıklama, künye)
haritanın ALTINA HTML olarak biner, görüntüye yakılmaz.

Neden bu kadar dar: bu sistemde bir kez daha geniş bir yol denendi ve
kapatıldı. 2026-08-31'de 716 satırlık `harita_commons.py` (SVG metin
değiştirme, ton kaydırma, lejant sökme) söküldü; ondan önce de bir görüntü
modeline harita çizdirme/renklendirme yolu ölçülüp terk edildi (model bir
haritada "(Occupied in 1426)" ibaresini sessizce "1405" yapmıştı). Kaynağa
dokunmayan bu yol, o hataların hiçbirini yapamaz -- çünkü piksellere hiç
bakmaz, yalnızca ölçekler.

Maliyet dürüstçe: etiketler kaynağın dilinde (genelde İngilizce) kalır.
Karşılığı `MapBox.ad_anahtari` ile kutunun altına basılan Türkçe okuma
anahtarıdır ("Manzikert = Malazgirt").
"""
from __future__ import annotations

import base64
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMONS = ROOT / "assets" / "harita" / "commons"
LISANS = COMMONS / "LISANS.md"

# Yan sütun kipinde (taraf="sag"/"sol") harita sütunu: metin alanı 186mm,
# grid 1.2fr/1fr + 5mm boşluk -> (186-5)/2.2 = 82.3mm. Tam kipte 186mm.
GENISLIK_YAN_MM = 82.3
GENISLIK_TAM_MM = 186.0
DPI = 300
JPEG_KALITE = 88

# Kaynak SVG ise Chromium ile bir kez rasterleştirilip yanına önbelleklenir.
RASTER_GENISLIK = 2400


class KaynakYok(FileNotFoundError):
    """Commons kaynağı diskte yok (`.gitignore`'da; --commons ile indirilir)."""


def kaynak_yolu(dosya: str) -> Path:
    p = COMMONS / dosya
    if not p.exists():
        raise KaynakYok(
            f"{dosya} bulunamadı -- python tools/harita.py --commons \"<madde>\" ile indirin")
    return p


# ---------------------------------------------------------------------------
# Künye: LISANS.md'den okunur, ELLE YAZILMAZ
# ---------------------------------------------------------------------------
def _tekille(ad: str) -> str:
    """Tam olarak ikiye katlanmış bir yazar adını tekilleştirir.

    Commons'ın Artist alanı bazı dosyalarda aynı metni iki kez döndürüyor
    ("Unknown authorUnknown author"); künye satırında bu okunmaz görünüyor.
    Yalnızca dizgi TAM ORTADAN ikiye bölündüğünde iki yarı birebir eşitse
    kısaltılır -- yani gerçek bir ada asla dokunmaz.
    """
    n = len(ad)
    return ad[: n // 2] if n and n % 2 == 0 and ad[: n // 2] == ad[n // 2:] else ad


def kunye(dosya: str) -> str:
    """`MapBox.source` satırını LISANS.md'deki künye tablosundan kurar.

    Atıf artık türetilmiş bir poligonun değil, DAĞITILAN GÖRÜNTÜNÜN kendisinin
    yükümlülüğüdür -- CC BY-SA yazar + lisans + bağlantı ister. Bu yüzden metin
    elle yazılmaz: künyenin tek kaynağı LISANS.md'dir, dosya orada kayıtlı
    değilse build uyarı basar (sahte atıf üretmez).
    """
    if not LISANS.exists():
        return ""
    metin = LISANS.read_text(encoding="utf-8")
    # "### `dosya.png`" başlığından bir sonraki "###"e kadar olan tablo
    kalip = re.compile(r"^### `" + re.escape(dosya) + r"`\s*$(.*?)(?=^### |\Z)",
                       re.M | re.S)
    m = kalip.search(metin)
    if not m:
        return ""
    blok = m.group(1)

    def alan(ad: str) -> str:
        a = re.search(r"^\|\s*" + ad + r"\s*\|\s*(.+?)\s*\|\s*$", blok, re.M)
        if not a:
            return ""
        # Markdown vurgusunu ve bağlantı sarmalayıcılarını at
        return re.sub(r"\*\*|\*|`", "", a.group(1)).strip()

    yazar = _tekille(alan("Yazar"))
    lisans = alan("Lisans")
    url = alan("Kaynak")
    parcalar = [p for p in (yazar, lisans, url) if p]
    if not parcalar:
        return ""
    return "Harita: " + " · ".join(parcalar) + " — ölçeklendirilmiş, başka değişiklik yapılmadı."


# ---------------------------------------------------------------------------
# Görüntü hazırlama
# ---------------------------------------------------------------------------
def _viewbox_tamamla(svg: str) -> str:
    """Kök etikette viewBox yoksa width/height'tan üretir.

    viewBox'ı olmayan bir SVG'de `width:100%` KUTUYU büyütür ama İÇERİĞİ
    büyütmez: çizim kullanıcı biriminde kalır ve sağ-alt tarafı boş beyaz
    olur. Ölçüldü (Transoxiana, Inkscape kaynağı): 2400 px'lik kutuda içerik
    1304 x 630'da kaldı, yani rasterin %70'i boştu. Bu bir GÖRÜNTÜLEME
    düzeltmesidir -- çizimin kendisine dokunmaz.
    """
    kok = re.search(r"<svg[^>]*>", svg, re.S)
    if not kok or "viewBox" in kok.group(0):
        return svg
    olcu = {}
    for ad in ("width", "height"):
        m = re.search(ad + r'\s*=\s*"([\d.]+)', kok.group(0))
        if not m:
            return svg
        olcu[ad] = m.group(1)
    yeni = kok.group(0)[:-1] + f' viewBox="0 0 {olcu["width"]} {olcu["height"]}">'
    return svg[:kok.start()] + yeni + svg[kok.end():]


def _svg_raster(yol: Path):
    """Commons SVG'sini bir kez rasterleştirir ve yanına önbellekler.

    Playwright zaten build.py'nin bağımlılığıdır. Kök etiketteki
    `width="992px"` sarmalayıcının genişliğini EZDİĞİ için CSS'te
    `width:100%!important` şart -- yoksa dosya kendi doğal ölçüsünde basılır
    (ölçüldü: istenen 2400 px yerine 992 px).

    `<meta charset>` de ŞARTTIR: Chromium yerel bir HTML'de charset yoksa
    Latin-1 varsayar ve SVG'nin UTF-8 etiketlerini bozar -- ölçüldü, Rum
    Selçuklu haritasında "Eskişehir" rasterde "EskiÅŸehir" çıktı. Kaynağa
    dokunmayan bu yolda böyle bir bozulma SESSİZDİR: ne taşma denetimi ne
    validate() görür, yalnızca göze çarpar.
    """
    from PIL import Image
    onbellek = yol.with_suffix(".raster.png")
    if onbellek.exists() and onbellek.stat().st_mtime >= yol.stat().st_mtime:
        return Image.open(onbellek).convert("RGB")

    import asyncio
    import tempfile
    from playwright.async_api import async_playwright

    svg = _viewbox_tamamla(yol.read_text(encoding="utf-8"))
    gecici = Path(tempfile.gettempdir()) / f"_gomme_{yol.stem}.html"
    gecici.write_text(
        f'<html><head><meta charset="utf-8">'
        f'<style>svg{{width:100%!important;height:auto!important}}'
        f'</style></head><body style="margin:0;background:#fff">'
        f'<div style="width:{RASTER_GENISLIK}px">{svg}</div></body></html>',
        encoding="utf-8")

    async def calis():
        async with async_playwright() as pw:
            b = await pw.chromium.launch()
            sayfa = await b.new_page(viewport={"width": RASTER_GENISLIK, "height": 1000})
            await sayfa.goto(gecici.as_uri())
            await sayfa.wait_for_timeout(400)
            await sayfa.locator("div").first.screenshot(path=str(onbellek))
            await b.close()

    asyncio.run(calis())
    gecici.unlink(missing_ok=True)
    return Image.open(onbellek).convert("RGB")


def gorsel(dosya: str, kirp: tuple = (), taraf: str = "sag") -> tuple[str, str]:
    """(veri_uri, "en / boy") döndürür. Görüntünün içeriğine DOKUNMAZ.

    `kirp` verilirse (sol, üst, sağ, alt) piksel kutusuyla kırpılır -- bu bir
    SİLME işlemidir (kaynağın ilgisiz kenarları), ekleme veya değiştirme
    değildir. Ardından hedef sütun genişliğine indirgenir; ASLA büyütülmez
    (büyütmek çözünürlük kazandırmaz, yalnızca dosyayı şişirir).
    """
    from PIL import Image

    yol = kaynak_yolu(dosya)
    im = _svg_raster(yol) if yol.suffix.lower() == ".svg" else Image.open(yol).convert("RGB")

    if kirp:
        sol, ust, sag, alt = (int(v) for v in kirp)
        im = im.crop((sol, ust, sag, alt))

    mm = GENISLIK_TAM_MM if taraf == "tam" else GENISLIK_YAN_MM
    hedef = int(mm / 25.4 * DPI)
    if im.width > hedef:
        im = im.resize((hedef, round(hedef * im.height / im.width)), Image.LANCZOS)

    tampon = io.BytesIO()
    im.save(tampon, "JPEG", quality=JPEG_KALITE, optimize=True, progressive=True)
    uri = "data:image/jpeg;base64," + base64.b64encode(tampon.getvalue()).decode("ascii")
    return uri, f"{im.width} / {im.height}"
