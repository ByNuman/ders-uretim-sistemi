# -*- coding: utf-8 -*-
"""
DERS ÜRETİM SİSTEMİ — tools/olcum.py  (SAYFA DOLULUK ÖLÇÜMÜ)
=============================================================
Bir dersin HTML'ini Chromium'da açar ve HER bölüm sayfası için:

  * sayfanın kullanılabilir içerik yüksekliği (mm)
  * sabit giderler (pageband, bölüm banner'ı)
  * o sayfadaki HER `.add_*()` bloğunun gerçek yüksekliği (mm)

bilgisini JSON olarak döker. Sayfa boyutu değiştiğinde "hangi bloğu hangi
sayfaya taşırsam %90-95 doluluk çıkar?" sorusunu tahminle değil ÖLÇÜMLE
cevaplamak için vardır (bkz. CLAUDE.md adım 6b).

Kullanım:
    python tools/olcum.py psikoloji --sinif 2 --donem 2 --sinav final
    python tools/olcum.py psikoloji --json --sinif 2 --donem 2 --sinav final
    python tools/olcum.py --hepsi --sinif 2 --donem 2 --sinav final
    python tools/olcum.py --hepsi                      # o dönemin src/kitap.py'sindeki tüm dersler

Ölçüm, şablondaki `<!--item N kind-->` yorum düğümlerine dayanır — bunlar
`_ders_govde.html.j2` içinde bölüm sayfası döngüsünde üretilir ve render'ı
etkilemez.
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


MEASURE_JS = """
const {{ chromium }} = require('playwright');
(async () => {{
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file:///{html}', {{ waitUntil: 'networkidle' }});
  const out = await page.evaluate((PAGE_H_MM) => {{
    const first = document.querySelector('.page');
    const mm = first.getBoundingClientRect().height / PAGE_H_MM;
    const h = (el) => {{
      const cs = getComputedStyle(el);
      return el.getBoundingClientRect().height
           + parseFloat(cs.marginTop) + parseFloat(cs.marginBottom);
    }};
    const pages = [];
    document.querySelectorAll('section.page[data-ch]').forEach((pg) => {{
      const cs = getComputedStyle(pg);
      const avail = pg.clientHeight
                  - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
      let overhead = 0;
      const items = [];
      let cur = null;
      for (const n of pg.childNodes) {{
        if (n.nodeType === 8) {{
          const m = /^item (\\d+) (\\w+)$/.exec(n.data.trim());
          if (m) {{ cur = {{ i: +m[1], kind: m[2], h: 0, parts: [] }}; items.push(cur); }}
        }} else if (n.nodeType === 1) {{
          if (n.classList.contains('footer')) continue;
          if (cur) {{ const v = h(n); cur.h += v; cur.parts.push(v); }}
          else overhead += h(n);
        }}
      }}
      pages.push({{
        ch: +pg.dataset.ch,
        cp: +pg.dataset.cp,
        availMm: avail / mm,
        overheadMm: overhead / mm,
        usedMm: (pg.scrollHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom)) / mm,
        items: items.map((it) => ({{
          i: it.i, kind: it.kind, mm: it.h / mm,
          parts: it.parts.map((v) => v / mm),
        }})),
      }});
    }});
    return pages;
  }}, {PAGE_H_MM});
  console.log('__DATA__' + JSON.stringify(out));
  await browser.close();
}})();
"""


def render_html(module_name: str) -> tuple[Path, object]:
    """build.py ile BİREBİR aynı HTML'i üretir (aynı css + aynı ctx)."""
    pack = B.DONEM.import_ders(module_name).get_pack()
    ctx = B.course_context(pack)
    env = Environment(loader=FileSystemLoader(str(B.TEMPLATES)))
    html = env.get_template("master.html.j2").render(
        pack=pack, css=B.load_css(),
        theme_override_css=resolve_theme_css(pack.theme_color), ctx=ctx,
    )
    path = B.OUTPUT / f"_olcum_{module_name.split('.')[-1]}.html"
    path.write_text(html, encoding="utf-8")
    return path, pack


def measure(module_name: str) -> list[dict]:
    html_path, pack = render_html(module_name)
    script = MEASURE_JS.format(html=html_path.resolve().as_posix(),
                               PAGE_H_MM=B.PAGE_H_MM)
    js = B.OUTPUT / "_olcum.js"
    js.write_text(script, encoding="utf-8")
    res = subprocess.run(["node", str(js)], capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    if res.returncode != 0:
        print(res.stdout)
        print(res.stderr)
        raise RuntimeError("ölçüm render'ı başarısız")
    for line in res.stdout.splitlines():
        if line.startswith("__DATA__"):
            data = json.loads(line[len("__DATA__"):])
            html_path.unlink(missing_ok=True)
            js.unlink(missing_ok=True)
            return data
    raise RuntimeError("ölçüm verisi bulunamadı")


def summary(module_name: str, data: list[dict]) -> None:
    print(f"\n=== {module_name} ===")
    print(f"{'blm':>3} {'sf':>3} {'kullanılan':>10} {'sınır':>7} {'doluluk':>8}   bloklar (mm)")
    for pg in data:
        pct = pg["usedMm"] / pg["availMm"] * 100
        flag = "TAŞMA" if pct > 100 else ("seyrek" if pct < 88 else "")
        blocks = " ".join(f"{it['kind'][:5]}:{it['mm']:.0f}" for it in pg["items"])
        print(f"{pg['ch']:>3} {pg['cp'] + 1:>3} {pg['usedMm']:9.1f}mm {pg['availMm']:6.1f}mm "
              f"{pct:6.1f}% {flag:6s} ov{pg['overheadMm']:.0f} {blocks}")


def main():
    ap = argparse.ArgumentParser(prog="tools/olcum.py")
    ap.add_argument("dersler", nargs="*", help="ölçülecek ders modülleri")
    ap.add_argument("--json", action="store_true", help="ham JSON bas")
    ap.add_argument("--hepsi", action="store_true",
                    help="dönemin kitap.py'sindeki tüm dersleri ölç")
    donem_mod.add_args(ap)
    a = ap.parse_args()

    d = donem_mod.resolve(a)
    B.set_donem(d)
    print(f"[olcum] Dönem: {d}  ({d.etiket})")
    as_json = a.json
    if a.hepsi:
        modules = d.import_ders("kitap").get_book().course_modules
    elif a.dersler:
        modules = a.dersler
    else:
        raise SystemExit("[hata] ölçülecek ders verilmedi (ya da --hepsi kullanın)")
    allout = {}
    for m in modules:
        data = measure(m)
        allout[m] = data
        if not as_json:
            summary(m, data)
    if as_json:
        print(json.dumps(allout, ensure_ascii=False))


if __name__ == "__main__":
    main()
