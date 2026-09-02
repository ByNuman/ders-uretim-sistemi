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
DERS ÜRETİM SİSTEMİ — tools/dengele.py  (SAYFA DENGELEME)
==========================================================
`tools/olcum.py`'nin ölçtüğü GERÇEK blok yüksekliklerini kullanarak bir dersin
Seçilen dönemin `src/<slug>.py` dosyasındaki `ChapterPage` bölünmelerini
yeniden dağıtır.

Ne YAPAR:
  * Bir bölümün tüm `.add_*()` bloklarını sırasıyla toplar,
  * sayfa sınırını aşmayacak ve mümkün olan EN AZ sayfaya sığacak şekilde
    yeniden gruplar (eşit dolulukta kalsınlar diye artan boşluğun karesi
    minimize edilir; son sayfa cezalandırılmaz — CLAUDE.md adım 6b),
  * o dönemin `src/<slug>.py`'sini bu yeni gruplamayla yeniden yazar.

Ne YAPMAZ (kasıtlı):
  * Blokların İÇİNİ değiştirmez — metin birebir taşınır, tek bir madde bile
    uydurulmaz veya kısaltılmaz.
  * Blokların SIRASINI değiştirmez; sadece sayfa sınırlarını kaydırır.
  * Bölümler arasında blok taşımaz.

`continue_tag=` argümanları düşürülür: şablon bunları artık render etmiyor
(bkz. CLAUDE.md "Bilinen tuzaklar" #4/#9), taşındıklarında yanıltıcı olurlar.

Kullanım:
    python tools/dengele.py psikoloji --sinif 2 --donem 2 --sinav final
    python tools/dengele.py psikoloji --kuru --sinif 2 --donem 2 --sinav final
    python tools/dengele.py --hepsi --sinif 2 --donem 2 --sinav final
    python tools/dengele.py --hepsi
"""

import re
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cekirdek import donem as donem_mod   # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import build as B                     # noqa: E402
from tools import olcum               # noqa: E402

SAFETY_MM = 4.0        # ölçüm/render oynamalarına karşı pay
NL = chr(10)
RE_APPEND = re.compile(r"^    (\w+)\.pages\.append\($")
RE_CTOR = re.compile(r"^        ChapterPage\(")
RE_ADD = re.compile(r"^        \.add_(\w+)\(")
RE_CLOSE = re.compile(r"^    \)\s*$")


# ---------------------------------------------------------------------------
# Kaynak dosyayı ayrıştır / yeniden yaz
# ---------------------------------------------------------------------------

class PageBlock:
    """Kaynaktaki tek bir `chN.pages.append( ChapterPage()... )` çağrısı."""

    def __init__(self, var, start, end, ctor, segments):
        self.var = var              # "ch1"
        self.start = start          # dosyadaki ilk satır indeksi
        self.end = end              # kapanış ")" satır indeksi (dahil)
        self.ctor = ctor            # ["        ChapterPage()"]
        self.segments = segments    # [[".add_terms(...)", ...], ...] satır listeleri


def parse_pages(lines: list[str]) -> list[PageBlock]:
    blocks, i, n = [], 0, len(lines)
    while i < n:
        m = RE_APPEND.match(lines[i])
        if not m:
            i += 1
            continue
        var, start = m.group(1), i
        j = i + 1
        if not RE_CTOR.match(lines[j]):
            raise SystemExit(f"beklenmeyen yapı, satır {j + 1}: {lines[j]!r}")
        ctor = [lines[j]]
        j += 1
        # ctor birden fazla satıra yayılmışsa parantez dengesine bak
        while ctor[0].count("(") - ctor[0].count(")") != 0 and not RE_ADD.match(lines[j]):
            ctor.append(lines[j])
            j += 1
        segments, cur = [], None
        while j < n and not RE_CLOSE.match(lines[j]):
            if RE_ADD.match(lines[j]):
                cur = [lines[j]]
                segments.append(cur)
            elif cur is None:
                raise SystemExit(f"add_ dışında satır, {j + 1}: {lines[j]!r}")
            else:
                cur.append(lines[j])
            j += 1
        if j >= n:
            raise SystemExit(f"kapanmayan append, satır {start + 1}")
        blocks.append(PageBlock(var, start, j, ctor, segments))
        i = j + 1
    return blocks



RE_AYAT_HEAD = re.compile(r"^        \.add_ayat\((.*), \[$")
RE_AYAH_OPEN = re.compile(r"^            Ayah\($")
RE_AYAT_TAIL = re.compile(r"^        \]\)$")


class Unit:
    """Sayfaya yerleştirilebilen EN KÜÇÜK parça.

    Çoğu `.add_*()` çağrısı tek bir Unit'tir. Tek istisna `.add_ayat()`:
    içindeki her `Ayah(...)` kartı ayrı ayrı taşınabilir, çünkü tek bir ayet
    grubu (Tefsir II'de 279mm'ye kadar çıkıyor) tek sayfaya sığmayabiliyor.
    Grubun ilk parçası başlığı taşır, devamı başlıksız basılır (şablonda
    `{% if title %}` koruması eklendi) -- böylece hiçbir başlık uydurulmaz."""

    __slots__ = ("h", "gid", "lines", "title_src", "first")

    def __init__(self, h, lines, gid=None, title_src=None, first=True):
        self.h, self.lines, self.gid = h, lines, gid
        self.title_src, self.first = title_src, first


def split_ayat(seg: list[str]) -> tuple[str, list[list[str]]] | None:
    """`.add_ayat("Başlık", [Ayah(...), ...])` segmentini
    (başlık_ifadesi, [Ayah blokları]) olarak ayırır. Beklenen biçimde
    değilse None döner (o zaman segment bölünmez, olduğu gibi taşınır)."""
    m = RE_AYAT_HEAD.match(seg[0])
    if not m or not RE_AYAT_TAIL.match(seg[-1]):
        return None
    blocks, cur = [], None
    for line in seg[1:-1]:
        if RE_AYAH_OPEN.match(line):
            cur = [line]
            blocks.append(cur)
        elif cur is None:
            return None
        else:
            cur.append(line)
    if not blocks:
        return None
    return m.group(1), blocks


def build_units(segs: list[list[str]], items: list[dict]) -> list[Unit]:
    """Kaynak segmentleri + ölçüm sonuçlarını Unit listesine çevirir."""
    units = []
    for gid, (seg, it) in enumerate(zip(segs, items)):
        parts = it.get("parts") or []
        parsed = split_ayat(seg) if it["kind"] == "ayat" else None
        if parsed and len(parts) == len(parsed[1]) + 1:
            title_src, blocks = parsed
            for k, blk in enumerate(blocks):
                h = parts[k + 1] + (parts[0] if k == 0 else 0.0)
                units.append(Unit(h, blk, gid=gid, title_src=title_src, first=(k == 0)))
        else:
            units.append(Unit(it["mm"], seg))
    return units


def emit_page(units: list[Unit]) -> list[str]:
    """Bir sayfadaki Unit'leri kaynak satırlarına çevirir; aynı ayet grubunun
    yan yana kalan parçaları TEK `.add_ayat()` çağrısında birleştirilir."""
    out, i = [], 0
    while i < len(units):
        u = units[i]
        if u.gid is None:
            out.extend(u.lines)
            i += 1
            continue
        j = i
        while j < len(units) and units[j].gid == u.gid:
            j += 1
        title = u.title_src if u.first else "None"
        out.append(f"        .add_ayat({title}, [")
        for c in units[i:j]:
            out.extend(c.lines)
        out.append("        ])")
        i = j
    return out


def emit(var: str, groups: list[list[Unit]]) -> list[str]:
    """Bir bölümün yeni sayfa gruplarını kaynak satırlarına çevirir."""
    out = []
    for units in groups:
        out.append(f"    {var}.pages.append(")
        out.append("        ChapterPage()")
        out.extend(emit_page(units))
        out.append("    )")
    return out


# ---------------------------------------------------------------------------
# Yeniden gruplama (DP)
# ---------------------------------------------------------------------------

def repack(heights: list[float], cap_first: float, cap_rest: float,
           where: str = "") -> list[int]:
    """Blok yüksekliklerini sayfalara böler.

    Ölçüt sırası: (1) EN AZ sayfa, (2) SON sayfa hariç her sayfada en az
    boşluk. İkinci ölçüt bilinçlidir: CLAUDE.md adım 6b devam sayfalarının
    %90-95 dolu olmasını, son sayfanın ise doğal boyutunda kalmasını ister --
    yani boşluk sona itilmelidir, sayfalara eşit dağıtılmamalıdır.

    Dönen: her sayfadaki blok sayısı."""
    n = len(heights)
    pre = [0.0]
    for h in heights:
        pre.append(pre[-1] + h)

    def cap(page_index):
        return cap_first if page_index == 0 else cap_rest

    INF = float("inf")
    # dp[i][p] = (maliyet) ilk i bloğu p sayfaya yerleştirmenin en iyi maliyeti
    dp = [[INF] * (n + 2) for _ in range(n + 1)]
    back = [[None] * (n + 2) for _ in range(n + 1)]
    dp[0][0] = 0.0
    for i in range(n + 1):
        for p in range(n + 1):
            if dp[i][p] == INF:
                continue
            c = cap(p)
            for j in range(i + 1, n + 1):
                used = pre[j] - pre[i]
                if used > c:
                    break
                # SON sayfanın boşluğu cezalandırılmaz -> boşluk sona itilir.
                penalty = 0.0 if j == n else (c - used) ** 2
                cost = dp[i][p] + penalty
                if cost < dp[j][p + 1]:
                    dp[j][p + 1] = cost
                    back[j][p + 1] = i
    best_p = None
    for p in range(1, n + 2):
        if dp[n][p] < INF:
            best_p = p
            break
    if best_p is None:
        big = [(i, h) for i, h in enumerate(heights) if h > cap_rest]
        detay = ", ".join(f"blok #{i + 1}: {h:.0f}mm" for i, h in big)
        raise SystemExit(
            f"{where}: tek başına sayfaya sığmayan blok var "
            f"(sayfa kapasitesi {cap_rest:.0f}mm) -> {detay}")
    # aynı sayfa sayısında en dengeli çözümü seç
    counts, j, p = [], n, best_p
    while p > 0:
        i = back[j][p]
        counts.append(j - i)
        j, p = i, p - 1
    counts.reverse()
    return counts


# ---------------------------------------------------------------------------
# Sürücü
# ---------------------------------------------------------------------------

def balance(module_name: str, dry: bool = False) -> bool:
    data = olcum.measure(module_name)
    by_ch = {}
    for pg in data:
        by_ch.setdefault(pg["ch"], []).append(pg)
    for pages in by_ch.values():
        pages.sort(key=lambda p: p["cp"])

    path = B.DONEM.src / (module_name.split(".")[-1] + ".py")
    lines = path.read_text(encoding="utf-8").split("\n")
    blocks = parse_pages(lines)

    # round-trip güvenlik denetimi: hiçbir şey değiştirmeden yeniden üretince
    # dosya birebir aynı çıkmalı (parser'ın sessizce satır yutmadığının kanıtı)
    for b in blocks:
        rebuilt = [f"    {b.var}.pages.append("] + b.ctor + \
                  [ln for seg in b.segments for ln in seg] + ["    )"]
        if rebuilt != lines[b.start:b.end + 1]:
            raise SystemExit(f"{path.name}: round-trip uyuşmazlığı, satır {b.start + 1}")

    by_var = {}
    for b in blocks:
        by_var.setdefault(b.var, []).append(b)

    edits, report = [], []
    for ch_no in sorted(by_ch):
        var = f"ch{ch_no}"
        if var not in by_var:
            raise SystemExit(f"{path.name}: {var} kaynakta bulunamadı")
        chb = by_var[var]
        # Bir bölümün ilk ve son pages.append'i arasındaki HER ŞEY yeniden
        # yazılır; aradaki başka kod (ör. bir MapBox tanımı) sessizce silinirdi.
        for onceki, sonraki in zip(chb, chb[1:]):
            arada = [l for l in lines[onceki.end + 1:sonraki.start] if l.strip()]
            if arada:
                raise SystemExit(
                    f"[dengele] {module_name}: {var} sayfa blokları arasında kod var "
                    f"(satır {onceki.end + 2}): {arada[0].strip()[:60]}" + NL +
                    f"          Bu satırlar yeniden yazımda kaybolurdu. Tanımları "
                    f"ilk `{var}.pages.append(` satırının ÜSTÜNE taşıyın.")
        segs = [seg for b in chb for seg in b.segments]
        meas = by_ch[ch_no]
        items = [it for pg in meas for it in pg["items"]]
        if len(items) != len(segs):
            raise SystemExit(f"{path.name} {var}: ölçümde {len(items)} blok, "
                             f"kaynakta {len(segs)} blok")
        units = build_units(segs, items)
        heights = [u.h for u in units]
        avail = meas[0]["availMm"]
        ov_first = meas[0]["overheadMm"]
        ov_rest = next((p["overheadMm"] for p in meas if p["cp"] > 0), ov_first)
        counts = repack(heights, avail - ov_first - SAFETY_MM,
                        avail - ov_rest - SAFETY_MM,
                        where=f"{module_name} bölüm {ch_no}")
        groups, k = [], 0
        for c in counts:
            groups.append(units[k:k + c])
            k += c
        fills, k = [], 0
        for idx, c in enumerate(counts):
            used = sum(heights[k:k + c]) + (ov_first if idx == 0 else ov_rest)
            fills.append(used / avail * 100)
            k += c
        report.append(f"    Bölüm {ch_no}: {len(chb)} -> {len(counts)} sayfa  "
                      f"doluluk {' '.join(f'{f:.0f}%' for f in fills)}")
        edits.append((chb[0].start, chb[-1].end, emit(var, groups)))

    print(f"\n=== {module_name} ===")
    for r in report:
        print(r)
    if dry:
        return False

    for start, end, new_lines in sorted(edits, reverse=True):
        lines[start:end + 1] = new_lines
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"    -> {path} güncellendi")
    return True


def main():
    ap = argparse.ArgumentParser(prog="tools/dengele.py")
    ap.add_argument("dersler", nargs="*", help="dengelenecek ders modülleri")
    ap.add_argument("--kuru", action="store_true", help="uygulama, sadece raporla")
    ap.add_argument("--hepsi", action="store_true",
                    help="dönemin kitap.py'sindeki tüm dersleri dengele")
    donem_mod.add_args(ap)
    a = ap.parse_args()

    d = donem_mod.resolve(a)
    B.set_donem(d)
    print(f"[dengele] Dönem: {d}  ({d.etiket})")
    dry = a.kuru
    if a.hepsi:
        modules = d.import_ders("kitap").get_book().course_modules
    elif a.dersler:
        modules = a.dersler
    else:
        raise SystemExit("[hata] dengelenecek ders verilmedi (ya da --hepsi kullanın)")
    for m in modules:
        balance(m, dry=dry)


if __name__ == "__main__":
    main()
