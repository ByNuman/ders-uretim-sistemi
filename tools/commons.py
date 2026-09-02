# -*- coding: utf-8 -*-
#
# Görsel Ders Notu Üretim Sistemi
# Copyright (C) 2026 Numan Gözdaş
# GNU Genel Kamu Lisansı v3 altında dağıtılır — bkz. LICENSE.
#
"""
WIKIMEDIA COMMONS GÖRSEL ARACI
==============================
Ders notlarına konacak harita/portre görsellerini YALNIZCA Wikimedia
Commons'tan arar ve indirir. Genel web araması YAPILMAZ — kaynak tek ve
lisansı denetlenebilir olsun diye.

    python tools/commons.py ara "Seljuk Empire map"
    python tools/commons.py bilgi "File:Map of the Seljuk Empire (1092).png"
    python tools/commons.py indir "File:Map of the Seljuk Empire (1092).png" \
        --ad selcuklu-haritasi --genislik 1500

`indir` iki dosya bırakır (assets/gorsel/ altında):
    <ad>.<uzanti>   -> görselin kendisi (Commons thumb'ı, DEĞİŞTİRİLMEDEN)
    <ad>.json       -> lisans/atıf künyesi (build sırasında alt nota basılır)

Görsel üzerinde HİÇBİR işlem yapılmaz: renklendirme, yeniden çizim, sınır
düzeltme yoktur. Yalnızca Commons'ın kendi thumb servisinden daha küçük bir
ölçekte istenir (baskı için 1500 px yeterli, PDF'i şişirmez).
"""

from __future__ import annotations

import argparse
import html
import io
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GORSEL_DIR = ROOT / "assets" / "gorsel"

API = "https://commons.wikimedia.org/w/api.php"
# Commons API kuralı: her istek kendini tanıtan bir User-Agent taşımalıdır.
UA = ("DersUretimSistemi/1.0 (https://github.com/ByNuman; egitim amacli gorsel "
      "ders notu uretimi) Python-urllib")


def _api(params: dict) -> dict:
    params = {**params, "format": "json"}
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.load(resp)


def _cikti(satir: str) -> None:
    """Windows konsolu (cp1254) Commons başlıklarını basamayabilir; kodlanamayan
    karakterleri '?' ile değiştirip yine de okunur bir çıktı ver."""
    enc = sys.stdout.encoding or "utf-8"
    sys.stdout.write(satir.encode(enc, errors="replace").decode(enc) + "\n")


# ---------------------------------------------------------------------------
# ara
# ---------------------------------------------------------------------------

def ara(terim: str, adet: int = 12) -> list[str]:
    d = _api({"action": "query", "list": "search", "srsearch": terim,
              "srnamespace": 6, "srlimit": adet})
    return [it["title"] for it in d.get("query", {}).get("search", [])]


# ---------------------------------------------------------------------------
# bilgi
# ---------------------------------------------------------------------------

def _temizle(deger: str) -> str:
    """extmetadata alanları HTML parçacığı olabilir; düz metne indir."""
    metin = re.sub(r"<[^>]+>", " ", deger or "")
    return re.sub(r"\s+", " ", html.unescape(metin)).strip()


def bilgi(baslik: str, genislik: int = 0) -> dict:
    """genislik verilirse Commons'ın kendi thumb servisinden o genişlikte bir
    kopya URL'si de döner (iiurlwidth). Elle thumb yolu KURMA: Commons artık
    yalnızca kendi listelediği ölçüleri veriyor, uydurma genişlik 400 döner."""
    sorgu = {"action": "query", "titles": baslik,
             "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata"}
    if genislik:
        sorgu["iiurlwidth"] = genislik
    d = _api(sorgu)
    sayfalar = d.get("query", {}).get("pages", {})
    for _, sayfa in sayfalar.items():
        if "imageinfo" not in sayfa:
            continue
        ii = sayfa["imageinfo"][0]
        em = ii.get("extmetadata", {})
        # API, url'ye izleme parametreleri (?utm_source=...) ekliyor; thumb yolu
        # kurarken dosya adının sonuna yapışmasınlar diye kırpılır.
        ii["url"] = ii["url"].split("?")[0]
        g = lambda k: _temizle(em.get(k, {}).get("value", ""))
        return {
            "baslik": sayfa["title"],
            "url": ii["url"],
            "thumb_url": ii.get("thumburl", "").split("?")[0],
            "thumb_genislik": ii.get("thumbwidth"),
            "aciklama_sayfasi": ii["descriptionurl"],
            "genislik": ii.get("width"), "yukseklik": ii.get("height"),
            "mime": ii.get("mime", ""),
            "lisans": g("LicenseShortName") or g("License"),
            "lisans_url": em.get("LicenseUrl", {}).get("value", ""),
            "yazar": g("Artist"),
            "kaynak": g("Credit"),
            "ad": g("ObjectName"),
        }
    raise SystemExit(f"[commons] Bulunamadi: {baslik}")


# ---------------------------------------------------------------------------
# indir
# ---------------------------------------------------------------------------

def indir(baslik: str, ad: str, genislik: int = 1500) -> Path:
    meta = bilgi(baslik, genislik)
    url = meta.get("thumb_url") or meta["url"]
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as resp:
        veri = resp.read()

    uzanti = {"image/jpeg": ".jpg", "image/png": ".png",
              "image/svg+xml": ".png"}.get(meta["mime"], ".png")
    if url.lower().endswith(".jpg") or url.lower().endswith(".jpeg"):
        uzanti = ".jpg"
    elif url.lower().endswith(".png"):
        uzanti = ".png"

    GORSEL_DIR.mkdir(parents=True, exist_ok=True)
    hedef = GORSEL_DIR / f"{ad}{uzanti}"
    hedef.write_bytes(veri)

    meta["indirilen_url"] = url
    meta["yerel_dosya"] = hedef.name
    (GORSEL_DIR / f"{ad}.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    try:
        from PIL import Image
        with Image.open(io.BytesIO(veri)) as im:
            meta["px"] = f"{im.width}x{im.height}"
    except Exception:
        meta["px"] = "?"
    _cikti(f"[commons] indirildi: {hedef}  ({len(veri)//1024} KB, {meta['px']})")
    _cikti(f"[commons] lisans   : {meta['lisans']}  |  {meta['yazar'][:60]}")
    return hedef


# ---------------------------------------------------------------------------
# yenile — künyesi olup dosyası olmayan görselleri geri indirir
# ---------------------------------------------------------------------------

def yenile() -> int:
    """Görsel ikilileri (.png/.jpg) depoda TUTULMAZ; git'te yalnızca `<ad>.json`
    künyesi durur. Temiz bir klonda ya da dosya silindiğinde bu komut künyedeki
    Commons başlığından hepsini yeniden indirir — görsel koddan üretilemez ama
    kaynağı tek ve sabit olduğu için yeniden ÇEKİLEBİLİR."""
    n = 0
    for kunye_yolu in sorted(GORSEL_DIR.glob("*.json")):
        ad = kunye_yolu.stem
        if any((GORSEL_DIR / f"{ad}{uz}").exists() for uz in (".png", ".jpg", ".jpeg", ".webp")):
            continue
        meta = json.loads(kunye_yolu.read_text(encoding="utf-8"))
        genislik = meta.get("thumb_genislik") or 1500
        indir(meta["baslik"], ad, genislik)
        n += 1
    _cikti(f"[commons] {n} gorsel yeniden indirildi." if n
           else "[commons] Eksik gorsel yok. ✓")
    return n


# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description="Wikimedia Commons gorsel araci")
    alt = ap.add_subparsers(dest="komut", required=True)

    p = alt.add_parser("ara"); p.add_argument("terim"); p.add_argument("--adet", type=int, default=12)
    p = alt.add_parser("bilgi"); p.add_argument("baslik")
    alt.add_parser("yenile", help="kunyesi olup dosyasi olmayan gorselleri geri indir")
    p = alt.add_parser("indir"); p.add_argument("baslik")
    p.add_argument("--ad", required=True, help="assets/gorsel/ altindaki dosya adi (uzantisiz)")
    p.add_argument("--genislik", type=int, default=1500)

    a = ap.parse_args()
    if a.komut == "ara":
        for t in ara(a.terim, a.adet):
            _cikti("  " + t)
    elif a.komut == "bilgi":
        _cikti(json.dumps(bilgi(a.baslik), ensure_ascii=False, indent=2))
    elif a.komut == "yenile":
        yenile()
    else:
        indir(a.baslik, a.ad, a.genislik)


if __name__ == "__main__":
    main()
