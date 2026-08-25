# -*- coding: utf-8 -*-
"""
DERS ÜRETİM SİSTEMİ — tools/kapak_onizleme.py  (RENK ÖNİZLEMESİ)
================================================================
Bir sınıfın TÜM derslerinin kapağını, küçültülmüş hâlde tek bir PDF'te
ızgara düzeninde gösterir. Amaç: bir ders üretmeden ÖNCE renk seçimini
görsel olarak doğrulamak (hangi ton hangi derse gidiyor, yan yana
ayrışıyorlar mı, kapaktaki altın vurgu okunuyor mu).

Bu bir ÜRETİM çıktısı değildir — gorsel_ders_notlari/ ağacına dokunmaz,
birleşik kitabı tetiklemez.

Tasarım TEK KAYNAKTAN gelir: kapak markup'ı templates/_ders_govde.html.j2
içindeki gerçek <section class="page cover"> bloğundan ÇALIŞMA ZAMANINDA
okunur (kopyalanmaz). Şablondaki kapak değişirse önizleme de değişir.
Renkler renk_uretici.ders_rengi()'nden gelir — yani görsel kitabın ve
ders-anlatim skill'inin kullanacağı rengin ta kendisi.

Kullanım:
    python tools/kapak_onizleme.py --sinif 3
    python tools/kapak_onizleme.py --sinif 3 --sutun 3 --satir 3
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from jinja2 import Environment, FileSystemLoader                    # noqa: E402
from build import load_css, SINGLE_GEOMETRY, page_geometry_css      # noqa: E402
from theme_engine import resolve_theme_css                          # noqa: E402
from renk_uretici import ders_rengi                                 # noqa: E402

TEMPLATES = ROOT / "templates"

# Kapak oranı = bleed dahil render ölçüsü (181 x 256 mm)
COVER_W_MM = SINGLE_GEOMETRY.page_w
COVER_H_MM = SINGLE_GEOMETRY.page_h


# ---------------------------------------------------------------------------
# Kapak markup'ını gerçek şablondan çek (tek kaynak — kopyalama yok)
# ---------------------------------------------------------------------------
def kapak_markup() -> str:
    """_ders_govde.html.j2 içindeki kapak <section>'ını olduğu gibi döner."""
    t = (TEMPLATES / "_ders_govde.html.j2").read_text(encoding="utf-8")
    bas = t.index('<section class="page cover')
    son = t.index("</section>", bas) + len("</section>")
    return t[bas:son]


# ---------------------------------------------------------------------------
# Kapağın ihtiyaç duyduğu asgari "pack" — gerçek CoursePack kurmaya gerek yok
# ---------------------------------------------------------------------------
class OnizlemePack:
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def chapter_count(self):
        return self.bolum

    def concept_count(self):
        return self.kavram


class OnizlemeCtx:
    prefix = ""
    pagecls = ""


# ---------------------------------------------------------------------------
# 3. SINIF DERS KATALOĞU
# ---------------------------------------------------------------------------
# (ders_klasoru, course_code, başlık, alt başlık, ikon harfi)
SINIF3_D1 = [
    ("TEFSİR III",               "TEFSİR III",      "Tefsir III",              "Kur'an'ı Anlama Usulü",           "T"),
    ("HADİS III",                "HADİS III",       "Hadis III",               "Rivayet ve Metin Tahlili",        "H"),
    ("SİSTEMATİK KELAM I",       "SİST. KELAM I",   "Sistematik Kelam I",      "İtikadın Aklî Temelleri",         "K"),
    ("İSLAM FELSEFESİ TARİHİ I", "İSL. FELSEFE I",  "İslam Felsefesi Tarihi I","Meşşâîlikten İşrâk'a",            "F"),
    ("İSLAM HUKUKU I",           "İSL. HUKUKU I",   "İslam Hukuku I",          "Usûl ve Hüküm Teorisi",           "U"),
    ("İSLAM MEDENİYETİ TARİHİ",  "İSL. MEDENİYETİ", "İslam Medeniyeti Tarihi", "Şehir, İlim ve Kurumlar",         "M"),
    ("TASAVVUF I",               "TASAVVUF I",      "Tasavvuf I",              "Zühdden Tarikatlara",             "S"),
    ("SINIF YÖNETİMİ",           "SINIF YÖNETİMİ",  "Sınıf Yönetimi",          "Öğrenme Ortamının Düzeni",        "Y"),
    ("DİN EĞİTİMİ",              "DİN EĞİTİMİ",     "Din Eğitimi",             "Kuram, Yöntem ve Uygulama",       "E"),
    ("ARAP DİLİ VE EDEBİYATI V", "ARAPÇA V",        "Arap Dili ve Edebiyatı V","Metin, Sarf ve Nahiv",            "A"),
    ("KUR'AN OKUMA VE TECVİD V", "TECVİD V",        "Kur'an Okuma ve Tecvid V","Tilavet ve Tecvid Kuralları",     "Q"),
]

SINIF3_D2 = [
    ("TEFSİR IV",                "TEFSİR IV",       "Tefsir IV",               "Sûre ve Âyet Tahlilleri",         "T"),
    ("HADİS IV",                 "HADİS IV",        "Hadis IV",                "Şerh Geleneği ve Tenkit",         "H"),
    ("SİSTEMATİK KELAM II",      "SİST. KELAM II",  "Sistematik Kelam II",     "Nübüvvet, Kader ve Âhiret",       "K"),
    ("İSLAM FELSEFESİ TARİHİ II","İSL. FELSEFE II", "İslam Felsefesi Tarihi II","Gazzâlî Sonrası Düşünce",        "F"),
    ("İSLAM HUKUKU II",          "İSL. HUKUKU II",  "İslam Hukuku II",         "Muâmelât ve Furû",                "U"),
    ("İSLAM MEZHEPLERİ TARİHİ I","MEZHEPLER I",     "İslam Mezhepleri Tarihi I","Fırkaların Doğuşu",              "Z"),
    ("TASAVVUF II",              "TASAVVUF II",     "Tasavvuf II",             "Tasavvuf Klasikleri",             "S"),
    ("EĞİTİMDE ÖLÇME VE DEĞERLENDİRME", "ÖLÇME VE DEĞ.", "Eğitimde Ölçme ve Değerlendirme", "Ölçüt, Araç ve Analiz", "O"),
    ("DİN HİZMETLERİNDE REHBERLİK VE İLETİŞİM", "REHBERLİK", "Din Hizmetlerinde Rehberlik", "İletişim ve Manevî Danışmanlık", "R"),
    ("ARAP DİLİ VE EDEBİYATI VI","ARAPÇA VI",       "Arap Dili ve Edebiyatı VI","İleri Metin ve Belâgat",         "A"),
    ("KUR'AN OKUMA VE TECVİD VI","TECVİD VI",       "Kur'an Okuma ve Tecvid VI","Makam ve İleri Tatbikat",        "Q"),
]

TON_ADI = {
    "#206040": "mushaf yeşili",   "#1D6363": "turkuaz",
    "#664324": "deri cildi",      "#592F79": "mor",
    "#2F2D76": "gece mavisi",     "#7A2433": "vişne",
    "#7B3260": "gül",             "#776931": "bronz",
    "#8C2F21": "terracotta",      "#1F4775": "çini laciverti",
    "#51662E": "zeytin",
}

KATALOG = {"3": [("1. Dönem", "1", SINIF3_D1), ("2. Dönem", "2", SINIF3_D2)]}


def kartlari_hazirla(sinif: str):
    kartlar = []
    for donem_adi, donem_no, dersler in KATALOG[sinif]:
        for klasor, kod, baslik, alt, ikon in dersler:
            renk = ders_rengi(klasor, sinif, donem_no, "final")
            kartlar.append({
                "pack": OnizlemePack(
                    sinav_etiketi="Final", icon_text=ikon, course_code=kod,
                    title=baslik, subtitle=alt,
                    description="Bölümler, kavram sözlüğü ve 20 soruluk "
                                "değerlendirme testiyle sınava hazırlık.",
                    bolum=7, kavram=32),
                "renk": renk,
                "ton": TON_ADI.get(renk.upper(), ""),
                "etiket": f"{sinif}/{donem_no} · {klasor}",
                "donem": donem_adi,
            })
    return kartlar


# ---------------------------------------------------------------------------
# Izgara sayfası — A4 dikey, her hücrede küçültülmüş gerçek kapak
# ---------------------------------------------------------------------------
SAYFA_W, SAYFA_H = 210.0, 297.0     # A4 dikey (önizleme sayfası — ders kapağı DEĞİL)
KENAR, ARA, BASLIK_H, ETIKET_H = 8.0, 4.0, 11.0, 7.0


def olcu_hesapla(sutun: int, satir: int):
    """Kapak genişliğini hem yatay hem dikey bütçeye sığacak şekilde seçer;
    en/boy oranı (181:256) her zaman korunur."""
    w_yatay = (SAYFA_W - 2 * KENAR - (sutun - 1) * ARA) / sutun
    # BASLIK_H'nin ALTINDAKİ boşluk (.sheet-head margin-bottom = ARA) da
    # düşülmeli; yoksa son satır sayfa dibinden birkaç mm kırpılır.
    h_dikey = ((SAYFA_H - 2 * KENAR - BASLIK_H - ARA - (satir - 1) * ARA) / satir) - ETIKET_H
    w = min(w_yatay, h_dikey * COVER_W_MM / COVER_H_MM)
    return w, w * COVER_H_MM / COVER_W_MM


ONIZLEME_CSS = """
@page {{ size: {sw}mm {sh}mm; margin: 0; }}
html, body {{ background: #e9e6e0; }}
body {{ margin: 0; font-family: "DejaVu Sans", sans-serif; }}
.sheet {{
  width: {sw}mm; height: {sh}mm; box-sizing: border-box;
  padding: {kenar}mm; background: #e9e6e0;
  display: flex; flex-direction: column; overflow: hidden;
  break-after: page; page-break-after: always;
}}
.sheet:last-child {{ break-after: auto; page-break-after: auto; }}
.sheet-head {{
  height: {bh}mm; flex: none; display: flex; align-items: baseline;
  justify-content: space-between; color: #3a3630;
  border-bottom: 0.4mm solid #bdb6ab; margin-bottom: {ara}mm;
}}
.sheet-head b {{ font-size: 4.2mm; letter-spacing: 0.06em; }}
.sheet-head span {{ font-size: 2.9mm; color: #6d675e; }}
.grid {{ display: grid; grid-template-columns: repeat({sutun}, {cw}mm); gap: {ara}mm; align-content: start; }}
.cell {{ width: {cw}mm; }}
.shot {{
  width: {cw}mm; height: {ch}mm; overflow: hidden;
  box-shadow: 0 0.6mm 1.6mm rgba(0,0,0,.28);
}}
/* `transform: scale()` DEĞİL, `zoom`: transform yalnızca görüntüyü küçültür,
   düzen kutusu 181x256mm kalır ve .shot'tan taşar; Chromium baskıda taşan
   belgeyi sayfaya sığdırmak için TÜM sayfayı ~0.71 oranında küçültüyordu
   (ekranda doğru, PDF'te küçük). `zoom` düzen kutusunu da küçültür. */
.scaler {{
  width: {pw}mm; height: {ph}mm;
  zoom: {olcek};
}}
/* Izgara içindeki kapak, kendi sayfa sonunu ZORLAMAMALI */
.scaler .page {{
  margin: 0 !important; break-after: auto !important;
  page-break-after: auto !important; box-shadow: none !important;
}}
.cap {{
  height: {eh}mm; padding-top: 1.1mm; font-size: 2.5mm; line-height: 1.28;
  color: #4a453d; overflow: hidden;
}}
/* Uzun ders adi iki satira sarinca altindaki hex satiri .cap'in
   overflow'una takilip kayboluyordu -- oysa onizlemenin amaci o kod. */
.cap b {{ display: block; font-size: 2.6mm; color: #241f19;
         white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.cap i {{ font-style: normal; color: #6d675e; }}
.swatch {{
  display: inline-block; width: 2.3mm; height: 2.3mm; border-radius: 50%;
  vertical-align: -0.25mm; margin-right: 1mm; border: 0.2mm solid rgba(0,0,0,.25);
}}
"""


def html_uret(kartlar, sutun, satir, baslik) -> str:
    cw, ch = olcu_hesapla(sutun, satir)
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)))
    kapak_tpl = env.from_string(kapak_markup())

    onizleme_css = ONIZLEME_CSS.format(
        sw=SAYFA_W, sh=SAYFA_H, kenar=KENAR, ara=ARA, bh=BASLIK_H, eh=ETIKET_H,
        sutun=sutun, cw=round(cw, 3), ch=round(ch, 3),
        pw=COVER_W_MM, ph=COVER_H_MM, olcek=round(cw / COVER_W_MM, 6))

    tema_css, hucreler = [], []
    for i, k in enumerate(kartlar):
        ctx = OnizlemeCtx()
        ctx.pagecls = f" ders-{i}"
        tema_css.append(resolve_theme_css(k["renk"], f".ders-{i}"))
        hucreler.append(
            '<div class="cell">'
            f'<div class="shot"><div class="scaler">{kapak_tpl.render(pack=k["pack"], ctx=ctx)}</div></div>'
            f'<div class="cap"><b>{k["etiket"]}</b>'
            f'<span class="swatch" style="background:{k["renk"]}"></span>'
            f'{k["renk"]} <i>{k["ton"]}</i></div></div>')

    per = sutun * satir
    sayfalar, toplam = [], (len(hucreler) + per - 1) // per
    for n in range(toplam):
        parca = "".join(hucreler[n * per:(n + 1) * per])
        sayfalar.append(
            f'<div class="sheet"><div class="sheet-head"><b>{baslik}</b>'
            f'<span>Kapak renk önizlemesi · sayfa {n + 1}/{toplam}</span></div>'
            f'<div class="grid">{parca}</div></div>')

    # style.css + geometri bloğu İKİ tane `@page { size: 181mm 256mm }` içerir
    # (ders sayfasının ölçüsü). Önizleme sayfası A4'tür; iki kural yan yana
    # kalırsa Chromium levhayı doğru üretse bile içeriği küçültüp sol-üste
    # yaslıyor. Bu yüzden ders @page'leri SÖKÜLÜR, tek @page bizimki olur.
    ders_css = re.sub(r"@page[^{]*\{[^}]*\}", "", load_css(SINGLE_GEOMETRY))

    return ("<!DOCTYPE html><html lang='tr'><head><meta charset='utf-8'>"
            f"<title>{baslik}</title><style>{ders_css}</style>"
            f"<style>{''.join(tema_css)}</style><style>{onizleme_css}</style>"
            f"</head><body>{''.join(sayfalar)}</body></html>")


def render(html_path: Path, pdf_path: Path):
    js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file:///{html_path.resolve().as_posix()}', {{ waitUntil: 'networkidle' }});
  await page.pdf({{ path: '{pdf_path.resolve().as_posix()}',
                    preferCSSPageSize: true, printBackground: true }});
  await browser.close();
}})();
"""
    # node_modules proje kökünde -> script de KÖKTE olmalı, yoksa
    # "Cannot find module 'playwright'" hatası alınır.
    tmp = ROOT / "_kapak_onizleme.js"
    tmp.write_text(js, encoding="utf-8")
    r = subprocess.run(["node", str(tmp)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(r.stdout, r.stderr)
        raise RuntimeError("render başarısız")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        prog="tools/kapak_onizleme.py",
        description="Bir sınıfın tüm derslerinin kapağını tek PDF'te ızgara "
                    "hâlinde gösterir (renk seçimini doğrulamak için).")
    ap.add_argument("--sinif", default="3", choices=sorted(KATALOG))
    ap.add_argument("--sutun", type=int, default=3)
    ap.add_argument("--satir", type=int, default=3)
    ap.add_argument("--cikti", default=None)
    a = ap.parse_args()

    kartlar = kartlari_hazirla(a.sinif)
    baslik = f"{a.sinif}. Sınıf · Ders Kapakları"
    cikti = Path(a.cikti) if a.cikti else ROOT / f"{a.sinif}-sinif" / "kapak-renk-onizleme.pdf"
    cikti.parent.mkdir(parents=True, exist_ok=True)

    html = html_uret(kartlar, a.sutun, a.satir, baslik)
    html_path = cikti.with_suffix(".html")
    html_path.write_text(html, encoding="utf-8")
    render(html_path, cikti)

    per = a.sutun * a.satir
    cw, ch = olcu_hesapla(a.sutun, a.satir)
    print(f"[onizleme] {len(kartlar)} kapak · sayfa başına {per} "
          f"({a.sutun}x{a.satir}) · kapak {cw:.1f}x{ch:.1f}mm")
    print(f"[onizleme] Renkler: {len({k['renk'] for k in kartlar})} farklı ton")
    print(f"[onizleme] PDF: {cikti}")
