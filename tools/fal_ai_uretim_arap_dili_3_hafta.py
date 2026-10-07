# -*- coding: utf-8 -*-
"""fal.ai Visual Generation Pipeline for Arap Dili ve Edebiyatı V — 3. Hafta (Zû Kār Hutbesi).
Generates 7 pedagogical 4:3 vector infographics and downloads them directly into all required image directories.
"""
import os
import json
import time
import urllib.request
import urllib.error
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

FAL_KEY = os.environ.get("FAL_KEY", "")
MODEL_ENDPOINT = "openai/gpt-image-2.5/sunburst/text-to-image"

ROOT = os.path.abspath(".")
OUTPUT_DIRS = [
    os.path.join(ROOT, "3-sinif", "1-donem", "vize", "görseller"),
    os.path.join(ROOT, "3-sinif", "1-donem", "vize", "gorsel_ders_notlari", "ARAP DİLİ VE EDEBİYATI V", "3. Hafta", "görseller"),
    os.path.join(ROOT, "3-sinif", "1-donem", "vize", "gorsel_ders_notlari", "ARAP DİLİ VE EDEBİYATI V", "görseller"),
]

TASKS = [
    {
        "filename": "1_zu_kar_siyasi_aktorler_ucgeni.jpg",
        "title": "Bölüm 1: Siyasî Arka Plan ve Aktörler Dinamiği Üçgeni",
        "prompt": (
            "Academic vector infographic diagram, 4:3 aspect ratio, elegant light parchment ivory background. "
            "A triangular power dynamic diagram connecting three major political entities: "
            "Top node with royal crown motif: 'KİSRÂ (SASANİ İMPARATORLUĞU)'. "
            "Bottom left node: 'NU'MÂN B. MÜNZİR (HÎRE KRALI)'. "
            "Bottom right node in glowing burgundy box: 'HÂNÎ B. KABÎSA (BENÎ ŞEYBÂN REİSİ)'. "
            "Between them bold directional arrows labeled: 'GASBEDİLEN HÜKÜMRANLIK', 'EMANETİN KUTSALLIĞI', 'DİRENİŞ VE MEYDAN OKUMA'. "
            "Center seal motif: 'ZÛ KĀR ÖNCESİ KRİZ'. "
            "STRICT MANDATORY RULE: All text labels strictly in Turkish. Giant, bold legible typography. "
            "Absolutely NO small paragraphs, NO bullet points, NO tiny explanatory text. "
            "Only 4 to 5 prominent, huge concept labels and clean boxes. "
            "Theme colors: deep burgundy red (#8C2F21) and warm antique gold (#c49a45). High contrast, maximum readability at small box scale."
        )
    },
    {
        "filename": "2_zu_kar_zafer_surec_cizelgesi.jpg",
        "title": "Bölüm 2: Zû Kār Zaferi Tarihî Süreç Çizelgesi",
        "prompt": (
            "Clean minimalist chronological process timeline vector infographic, 4:3 aspect ratio, light ivory parchment background. "
            "Horizontal flow of three prominent numbered cards connected by bold golden direction arrows: "
            "Card 1: '1. SASANİ BASKISI (m. 609)' with imperial crest. "
            "Card 2: '2. HÂNÎ'NİN TARİHÎ HUTBESİ' in prominent burgundy frame with rhetoric scroll motif. "
            "Card 3: '3. ZÛ KĀR ZAFERİ (İNTİSAF)' in glowing golden victory wreath. "
            "Bottom summary banner: 'ARAPLARIN ACEM'E İLK BÜYÜK GALİBİYETİ'. "
            "STRICT MANDATORY RULE: All text labels strictly in Turkish. Giant bold typography. "
            "Absolutely NO tiny sentences, NO paragraphs, NO small bullet points. "
            "Only 3 prominent process cards and 1 banner. Theme colors: deep burgundy (#8C2F21) and antique gold (#c49a45). Maximum readability at small scale."
        )
    },
    {
        "filename": "3_yara_semantigi_seref_vs_zillet.jpg",
        "title": "Bölüm 3: Beden Dili ve Yara Semantiği (Şeref vs. Zillet)",
        "prompt": (
            "Clean minimalist vector comparison balance diagram, 4:3 aspect ratio, light parchment ivory backdrop. "
            "A balanced contrast between two moral stances: "
            "Left card glowing in warm gold: 'ŞEREF YARASI (GÖĞÜS & BOYUN)' with subtitle 'İZZET VE SEBAT'. "
            "Right card in muted gray shadow: 'ZİLLET YARASI (SIRT & FIRAR)' with subtitle 'EBEDÎ AYIP VE KORKAKLIK'. "
            "In the center a golden balance scale weighing: 'KABİLE ONURU'. "
            "STRICT MANDATORY RULE: All text labels strictly in Turkish. Giant, bold, legible typography. "
            "Absolutely NO tiny text, NO bullet lists, NO paragraphs. "
            "Only 4 prominent, huge concept labels. Theme colors: deep burgundy red (#8C2F21) and warm gold (#c49a45). High contrast, maximum readability."
        )
    },
    {
        "filename": "4_ecelin_mutlakligi_karar_agaci.jpg",
        "title": "Bölüm 4: Ecelin Mutlaklığı Mantıkî Karar Ağacı",
        "prompt": (
            "Clean minimalist logical decision tree vector infographic, 4:3 aspect ratio, light ivory parchment background. "
            "Root concept box at top: 'ÖLÜM (KAÇINILMAZ ECEL)'. "
            "Two branching paths: "
            "Left branch with red cross mark: 'KAÇMAK (FIRAR) ➔ ZİLLET + MUTLAK ÖLÜM'. "
            "Right branch in prominent glowing gold box: 'DİRENMEK (SEBAT) ➔ ŞEREF VEYA ZAFER'. "
            "Bottom conclusion badge: 'AKLIN VE ŞEREFİN TEK TERCİHİ'. "
            "STRICT MANDATORY RULE: All text labels strictly in Turkish. Giant bold legible typography. "
            "Absolutely NO small explanatory paragraphs, NO tiny bullet points. "
            "Only 4 clean prominent concept nodes and flow arrows. Theme colors: deep burgundy (#8C2F21) and antique gold (#c49a45). High contrast, maximum legibility."
        )
    },
    {
        "filename": "5_hitabetin_dort_temel_sutunu.jpg",
        "title": "Bölüm 5: Câhiliye Hitabet Sanatının 4 Temel Sütunu",
        "prompt": (
            "Architectural vector infographic, 4:3 aspect ratio, light parchment background. "
            "A classical colonnade supported by four prominent pillars labeled with large bold Turkish typography: "
            "Pillar 1: 'ÎCÂZ (AZ SÖZLE ÇOK MANA)'. "
            "Pillar 2: 'SECİ' (NESİR KAFİYESİ VE AHENK)'. "
            "Pillar 3: 'MÜNASEBET (MUTLAK HEDEF ODAKLILIK)'. "
            "Pillar 4: 'HİKMET (DARBIMESEL DERİNLİĞİ)'. "
            "Pediment crest on top: 'CÂHİLİYE HİTABET MİMARİSİ'. "
            "STRICT MANDATORY RULE: All text labels strictly in Turkish. Giant, bold typography on each pillar. "
            "Absolutely NO side text, NO small paragraphs, NO bullet points. "
            "Only 4 pillar labels and 1 crest title. Theme colors: deep burgundy red (#8C2F21) and gold (#c49a45)."
        )
    },
    {
        "filename": "6_siir_ve_hutbe_karsilastirma.jpg",
        "title": "Bölüm 6: Şiir ↔ Hutbe Köprüsü (Hânî ve Mütenebbî)",
        "prompt": (
            "Minimalist intertextual comparison matrix vector infographic, 4:3 aspect ratio, light parchment background. "
            "Two large parallel conceptual cards connected by a central golden bridge: "
            "Left card: 'HUTBE (HÂNÎ B. KABÎSA)' with key quote label 'فَمَا لِلْمَنَايَا مِنْ بُدٍّ (ÖLÜMDEN KAÇIŞ YOKTUR)'. "
            "Right card: 'ŞİİR (EL-MÜTENEBBÎ)' with key quote label 'وَإِذَا لَمْ يَكُنْ مِنَ المَوْتِ بُدٌّ (MADEMKİ ÖLÜM KAÇINILMAZDIR)'. "
            "Center golden bridge arch: 'ORTAK HAKİKAT: ŞEREFLİ FEDAKÂRLIK'. "
            "STRICT MANDATORY RULE: Labels in Turkish and Arabic. Giant bold legible typography. "
            "Absolutely NO small notes, NO tiny commentary, NO paragraphs. "
            "Only 3 prominent concept blocks. Theme colors: deep burgundy (#8C2F21) and antique gold (#c49a45). High contrast, maximum readability."
        )
    },
    {
        "filename": "7_soru_turetme_sentaks_akisi.jpg",
        "title": "Bölüm 7: Soru Türetme Algoritması ve Sentaks Karar Akışı",
        "prompt": (
            "Minimalist syntactic decision flowchart vector infographic, 4:3 aspect ratio, light ivory parchment background. "
            "Top input node: 'ARAPÇA CEVAP CÜMLESİ'. "
            "Two branching condition cards with bold arrows: "
            "Rule A card: 'İLLET BİLDİREN LAFIZ (طَلَباً / لِـ) ➔ لِمَاذَا (NEDEN?)'. "
            "Rule B card: 'MUKAYESE KALIBI (أَكْرَمُ مِنْ) ➔ أَيُّهُمَا ... أَمْ ... (HANGİSİ?)'. "
            "Bottom output badge: 'DOĞRU SORU KALIBI'. "
            "STRICT MANDATORY RULE: Labels in Turkish and Arabic. Giant bold typography. "
            "Absolutely NO tiny paragraphs, NO small bullets, NO complex clutter. "
            "Only 4 clean geometric flowchart boxes. Theme colors: deep burgundy red (#8C2F21) and warm gold (#c49a45). Maximum readability at small scale."
        )
    }
]

def generate_and_download():
    for d in OUTPUT_DIRS:
        os.makedirs(d, exist_ok=True)
    
    url = f"https://fal.run/{MODEL_ENDPOINT}"

    print(f"Toplam {len(TASKS)} görsel üretilecek. fal.ai API başlatılıyor...")
    for idx, item in enumerate(TASKS, 1):
        print(f"\n[{idx}/{len(TASKS)}] Başlatılıyor: {item['title']} -> {item['filename']}")
        
        payload = {
            "prompt": item["prompt"],
            "quality": "low",
            "image_size": "landscape_4_3",
            "output_format": "jpeg",
            "num_images": 1
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Key {FAL_KEY}",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                res_data = json.loads(resp.read().decode("utf-8"))
                images = res_data.get("images", [])
                if not images:
                    print(f"  HATA: Görsel dönmedi! Yanıt: {res_data}")
                    continue
                img_url = images[0].get("url")
                print(f"  Görsel URL alındı: {img_url}")
                
                # İlk hedefe indir
                primary_path = os.path.join(OUTPUT_DIRS[0], item["filename"])
                urllib.request.urlretrieve(img_url, primary_path)
                
                # Diğer hedeflere kopyala
                for extra_dir in OUTPUT_DIRS[1:]:
                    extra_path = os.path.join(extra_dir, item["filename"])
                    shutil.copy2(primary_path, extra_path)
                
                print(f"  ✓ BAŞARILI: {item['filename']} kaydedildi ({len(OUTPUT_DIRS)} konuma).")
                
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="ignore")
            print(f"  HTTPError {e.code}: {err[:200]}")
        except Exception as e:
            print(f"  Hata: {e}")
            
        time.sleep(1)

    print("\n✓ Tüm görsellerin üretimi ve indirilmesi tamamlandı!")

if __name__ == "__main__":
    generate_and_download()
