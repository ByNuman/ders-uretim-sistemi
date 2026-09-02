# -*- coding: utf-8 -*-
#
# Görsel Ders Notu Üretim Sistemi
# Copyright (C) 2026 Numan Gözdaş
# GNU Genel Kamu Lisansı v3 altında dağıtılır — bkz. LICENSE.
#
"""
GÖRSEL VARLIK KATMANI (harita / portre)
=======================================
`assets/gorsel/` altındaki Commons görsellerini sayfaya hazır hale getirir:

    hazirla("selcuklu-1092", 1200) -> "file:///.../_onbellek/selcuklu-1092-1200.jpg"
    atif("selcuklu-1092")          -> "Wikimedia Commons · Ktrinko MapMaster · CC BY-SA 4.0"

Neden ara bir katman var:

* **Boyut.** Commons orijinalleri 3-5 MB olabiliyor; Chromium onu PDF'e
  olduğu gibi gömer. Baskıda 90 mm genişliğe basılan bir harita için ~1200 px
  (≈340 dpi) fazlasıyla yeter. Ölçeklenmiş kopya `_onbellek/`e bir kez yazılır,
  sonraki derlemeler onu kullanır.
* **Görselin kendisine dokunulmaz.** Yapılan tek işlem ORANTILI KÜÇÜLTMEdir;
  renk, sınır, içerik değiştirilmez, yeniden çizilmez.
* **Atıf zorunlu.** Her görselin yanında `tools/commons.py`nin bıraktığı
  `<ad>.json` künyesi bulunur; atıf metni oradan üretilir. Künye yoksa
  `atif()` derlemeyi net bir hatayla durdurur — kaynaksız görsel basılmaz.

`file:///` yolu döndürülür (data-URI değil): Chromium file:// sayfasından
yerel görseli sorunsuz yükler, HTML de şişmez.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GORSEL_DIR = ROOT / "assets" / "gorsel"
ONBELLEK = GORSEL_DIR / "_onbellek"

UZANTILAR = (".png", ".jpg", ".jpeg", ".webp")

# Baskı hedefi: 90 mm genişlikte 1200 px ≈ 340 dpi.
VARSAYILAN_PX = 1200


def _kaynak_dosya(ad: str) -> Path:
    for uz in UZANTILAR:
        p = GORSEL_DIR / f"{ad}{uz}"
        if p.exists():
            return p
    raise SystemExit(
        f"[gorsel] '{ad}' assets/gorsel/ altında yok.\n"
        f"         Commons'tan indirin:\n"
        f"         python tools/commons.py ara \"<terim>\"\n"
        f"         python tools/commons.py indir \"File:...\" --ad {ad}")


def kunye(ad: str) -> dict:
    p = GORSEL_DIR / f"{ad}.json"
    if not p.exists():
        raise SystemExit(
            f"[gorsel] '{ad}' için lisans künyesi ({p.name}) yok. Görseli "
            f"tools/commons.py ile indirin — künyeyi o yazar. Kaynağı "
            f"belirsiz görsel ders notuna konmaz.")
    return json.loads(p.read_text(encoding="utf-8"))


def atif(ad: str) -> str:
    """Görselin altına basılacak tek satırlık Commons atfı."""
    k = kunye(ad)
    parcalar = ["Wikimedia Commons"]
    if k.get("ad"):
        parcalar.append(k["ad"])
    if k.get("yazar"):
        parcalar.append(k["yazar"])
    if k.get("lisans"):
        parcalar.append(k["lisans"])
    return " · ".join(parcalar)


def hazirla(ad: str, px: int = VARSAYILAN_PX) -> str:
    """Görseli en fazla `px` genişliğe orantılı küçültüp file:/// yolunu döndürür.
    Kaynak zaten küçükse dokunulmaz, doğrudan kendisi verilir."""
    from PIL import Image, PngImagePlugin
    # Commons PNG'lerinde büyük metin (zTXt) parçaları olabiliyor; Pillow'un
    # varsayılan sınırı bunları "zip bombası" sanıp açmayı reddediyor.
    PngImagePlugin.MAX_TEXT_CHUNK = 64 * 1024 * 1024

    kaynak = _kaynak_dosya(ad)
    with Image.open(kaynak) as im:
        if im.width <= px:
            return kaynak.resolve().as_uri()
        seffaf = im.mode in ("RGBA", "LA", "P")
        uzanti = ".png" if seffaf else ".jpg"
        hedef = ONBELLEK / f"{ad}-{px}{uzanti}"
        if hedef.exists() and hedef.stat().st_mtime >= kaynak.stat().st_mtime:
            return hedef.resolve().as_uri()
        ONBELLEK.mkdir(parents=True, exist_ok=True)
        kucuk = im.copy()
        kucuk.thumbnail((px, px * 4), Image.LANCZOS)
        if seffaf:
            kucuk.convert("RGBA").save(hedef)
        else:
            kucuk.convert("RGB").save(hedef, quality=92, subsampling=0)
    return hedef.resolve().as_uri()
