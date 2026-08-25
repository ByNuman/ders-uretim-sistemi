# -*- coding: utf-8 -*-
#
# Görsel Ders Notu Üretim Sistemi
# Copyright (C) 2026 Numan Gözdaş
# GNU Genel Kamu Lisansı v3 altında dağıtılır — bkz. LICENSE.
#
"""
ÇEKİRDEK — sistemin kütüphane modülleri.
========================================
Doğrudan çalıştırılan komutlar (`build.py`, `build_kitap.py`, `tools/*.py`)
kökte durur; burası onların ortak kullandığı kod:

    content_model.py   Veri şeması (CoursePack, Chapter, ChapterPage ...)
    donem.py           Sınıf/dönem/sınav (ve düz `dersler/`) çözümleyicisi
    theme_engine.py    Tek hex renkten tam tema üreten motor
    renk_uretici.py    Derse özel vurgu rengi — build + ders-anlatim ortak kaynağı
    pdfx.py            Baskı öncesi: TrimBox/BleedBox + PDF/X-4 CMYK

Bu modüllerin üçü (`pdfx`, `renk_uretici`, `theme_engine`) doğrudan da
çalıştırılabilir (`python cekirdek/pdfx.py` gibi); bu yüzden her birinin
başında paket kökünü sys.path'e ekleyen küçük bir açılış bloğu vardır.
"""
