# -*- coding: utf-8 -*-
#
# Görsel Ders Notu Üretim Sistemi
# Copyright (C) 2026 Numan Gözdaş
#
# Bu program özgür yazılımdır: Özgür Yazılım Vakfı'nın yayımladığı GNU Genel
# Kamu Lisansı'nın 3. sürümü koşulları altında yeniden dağıtabilir ve/veya
# değiştirebilirsiniz.
#
# Bu program yararlı olacağı umuduyla dağıtılmaktadır, ancak HİÇBİR GARANTİ
# VERİLMEZ; SATILABİLİRLİK veya BELİRLİ BİR AMACA UYGUNLUK zımni garantileri
# dahi verilmez. Ayrıntılar için GNU Genel Kamu Lisansı'na bakın.
#
# Lisansın bir kopyasını bu depodaki LICENSE dosyasında bulabilirsiniz;
# ayrıca <https://www.gnu.org/licenses/> adresinden edinebilirsiniz.
#
"""
DERS ÜRETİM SİSTEMİ — tools/kalibre.py  (SAYFALAMA SABİTİ KALİBRASYONU)
=======================================================================
Sözlük / Test / Cevap Anahtarı bölümleri sabit "sayfa başına N öğe"
sayılarıyla bölünür (build.py: GLOSSARY_PER_PAGE, TEST_PER_PAGE,
ANSWER_PER_PAGE ve LEGACY QA/DISTINCTIONS/MATCHTABLE). Sayfa boyutu
değiştiğinde bu sayılar da değişmek zorundadır.

Bu araç, aday değerleri GERÇEKTEN render edip taşıp taşmadığına bakar ve
her sabit için taşmayan EN BÜYÜK değeri bulur (tek tek denemek yerine).
Birden çok ders üzerinde çalışır: sabit hepsinde birden geçerli olmalı,
bu yüzden dersler arası MİNİMUM alınır.

Kullanım:
    python tools/kalibre.py                       # varsayılan ders kümesi
    python tools/kalibre.py --sinif 2 --donem 2 --sinav final
    python tools/kalibre.py psikoloji sosyoloji --sinif 2 --donem 2 --sinav final
"""

import json
import subprocess
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import donem as donem_mod   # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import build as B                                    # noqa: E402
from jinja2 import Environment, FileSystemLoader     # noqa: E402
from theme_engine import resolve_theme_css           # noqa: E402

# sabit adı -> (aday değerler, o bölümün ilk sayfasının anchor'ı)
CANDIDATES = {
    "GLOSSARY_PER_PAGE": list(range(26, 5, -1)),
    "TEST_PER_PAGE": list(range(12, 1, -1)),
    "ANSWER_PER_PAGE": list(range(24, 3, -1)),
    "QA_PER_PAGE": list(range(12, 2, -1)),
    "DISTINCTIONS_PER_PAGE": list(range(8, 1, -1)),
    "MATCHTABLE_PER_PAGE": list(range(11, 2, -1)),
}

# hangi sabit hangi sayfa aralığını etkiler (page_starts anahtarı, bitiş anahtarı)
SPANS = {
    "GLOSSARY_PER_PAGE": ("glossary", ("test", "exam")),
    "TEST_PER_PAGE": ("test", ("answer_key",)),
    "ANSWER_PER_PAGE": ("answer_key", ("end+1",)),
    "QA_PER_PAGE": ("exam", ("end+1",)),
    "DISTINCTIONS_PER_PAGE": ("exam", ("end+1",)),
    "MATCHTABLE_PER_PAGE": ("exam", ("end+1",)),
}

JS = """
const {{ chromium }} = require('playwright');
const files = {files};
(async () => {{
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const out = {{}};
  for (const f of files) {{
    await page.goto('file:///' + f.path, {{ waitUntil: 'load' }});
    const bad = await page.evaluate((PAGE_H_MM) => {{
      const mm = document.querySelector('.page').getBoundingClientRect().height / PAGE_H_MM;
      const res = [];
      document.querySelectorAll('.page').forEach((p, i) => {{
        if (p.scrollHeight > PAGE_H_MM * mm + 2)
          res.push([i + 1, Math.round((p.scrollHeight - PAGE_H_MM * mm) / mm * 10) / 10]);
      }});
      return res;
    }}, {PAGE_H_MM});
    out[f.key] = bad;
  }}
  console.log('__DATA__' + JSON.stringify(out));
  await browser.close();
}})();
"""


def render(module_name: str, tag: str):
    """Mevcut build sabitleriyle bir dersin HTML'ini üretir."""
    pack = B.DONEM.import_ders(module_name).get_pack()
    ctx = B.course_context(pack)
    env = Environment(loader=FileSystemLoader(str(B.TEMPLATES)))
    html = env.get_template("master.html.j2").render(
        pack=pack, css=B.load_css(),
        theme_override_css=resolve_theme_css(pack.theme_color), ctx=ctx)
    path = B.OUTPUT / f"_kal_{tag}.html"
    path.write_text(html, encoding="utf-8")
    return path, ctx["page_starts"]


def span_of(starts: dict, const: str):
    """Sabitin etkilediği fiziksel sayfa aralığı (1 tabanlı, dahil)."""
    first_key, end_keys = SPANS[const]
    if first_key not in starts:
        return None
    first = starts[first_key]
    last = starts["end"]
    for k in end_keys:
        if k == "end+1":
            continue
        if k in starts:
            last = starts[k] - 1
            break
    return first, last


def calibrate(modules: list[str]) -> dict:
    results = {}
    for const, values in CANDIDATES.items():
        # bu sabiti kullanan dersleri ayıkla
        original = getattr(B, const)
        jobs = []
        for value in values:
            setattr(B, const, value)
            for mi, m in enumerate(modules):
                tag = f"{const}_{value}_{mi}"
                try:
                    path, starts = render(m, tag)
                except Exception:
                    continue
                sp = span_of(starts, const)
                if sp is None:
                    path.unlink(missing_ok=True)
                    continue
                jobs.append({"key": tag, "path": path.resolve().as_posix(),
                             "const": const, "value": value, "module": m, "span": sp})
        setattr(B, const, original)
        if not jobs:
            results[const] = original
            continue
        data = run_js(jobs)
        best = None
        for value in values:
            ok = True
            for j in jobs:
                if j["value"] != value:
                    continue
                lo, hi = j["span"]
                if any(lo <= pg <= hi for pg, _ in data.get(j["key"], [])):
                    ok = False
                    break
            if ok:
                best = value
                break
        results[const] = best if best is not None else min(values)
        for j in jobs:
            Path(j["path"]).unlink(missing_ok=True)
        print(f"  {const:24s} {original:>3} -> {results[const]:>3}")
    return results


def run_js(jobs):
    script = JS.format(files=json.dumps([{"key": j["key"], "path": j["path"]} for j in jobs]),
                       PAGE_H_MM=B.PAGE_H_MM)
    js = B.OUTPUT / "_kal.js"
    js.write_text(script, encoding="utf-8")
    res = subprocess.run(["node", str(js)], capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    if res.returncode != 0:
        print(res.stdout, res.stderr)
        raise RuntimeError("kalibrasyon render'ı başarısız")
    for line in res.stdout.splitlines():
        if line.startswith("__DATA__"):
            js.unlink(missing_ok=True)
            return json.loads(line[len("__DATA__"):])
    raise RuntimeError("kalibrasyon verisi yok")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(prog="tools/kalibre.py")
    ap.add_argument("dersler", nargs="*",
                    help="kalibrasyonda kullanılacak dersler "
                         "(boşsa dönemin kitap.py'sindeki tüm dersler)")
    donem_mod.add_args(ap)
    a = ap.parse_args()

    d = donem_mod.resolve(a)
    B.set_donem(d)
    print(f"[kalibre] Dönem: {d}  ({d.etiket})")
    mods = a.dersler or d.import_ders("kitap").get_book().course_modules
    print(f"{len(mods)} ders üzerinde kalibrasyon (taşmayan en büyük değer):")
    out = calibrate(mods)
    print("\nbuild.py için önerilen sabitler:")
    for k, v in out.items():
        print(f"    {k} = {v}")
