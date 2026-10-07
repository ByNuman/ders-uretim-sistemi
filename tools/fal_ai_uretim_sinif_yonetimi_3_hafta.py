import os
import json
import time
import urllib.request
import urllib.error

FAL_KEY = os.environ.get("FAL_KEY", "")
MODEL_ENDPOINT = "openai/gpt-image-2.5/sunburst/text-to-image"

OUTPUT_DIRS = [
    r"c:\Users\ASUS\OneDrive\OKUL\ders-uretim-sistemi\3-sinif\1-donem\vize\gorsel_ders_notlari\SINIF YÖNETİMİ\3. Hafta\görseller",
]

TASKS = [
    {
        "filename": "etkili dönüt döngüsü.jpg",
        "title": "Bölüm 1 - Sf 1: Etkili Dönüt Döngüsü (3 Boyut)",
        "prompt": (
            "Clean and minimalist vector academic infographic diagram, 4:3 aspect ratio, elegant light parchment ivory background. "
            "A triangular continuous feedback cycle connecting three prominent circular nodes. "
            "Only three large bold Turkish text labels on the nodes: "
            "Top node: 'BİLİŞSEL DÖNÜT (KAVRAM & BİLGİ)', "
            "Left node: 'DUYUŞSAL DÖNÜT (ÖZGÜVEN & ÇABA)', "
            "Right node: 'DAVRANIŞSAL DÖNÜT (KURALLAR & KATILIM)'. "
            "In the center of the triangle, a glowing gold box labeled: 'ETKİLİ GERİBİLDİRİM DÖNGÜSÜ'. "
            "STRICT MANDATORY RULE: All text labels strictly in Turkish. Bold, giant legible typography. "
            "Absolutely NO small paragraphs, NO bullet points, NO tiny explanatory text. "
            "High contrast, theme colors deep porcelain navy (#1F4775) and warm gold accents."
        )
    },
    {
        "filename": "dönüt ilkeleri.jpg",
        "title": "Bölüm 1 - Sf 2: Etkili Dönüt İlkeleri & Karşılaştırma",
        "prompt": (
            "Clean minimalist vector comparison infographic, 4:3 aspect ratio, light ivory parchment background. "
            "Two distinct side-by-side columns comparing feedback styles. "
            "Left column in deep navy (#1F4775) labeled: 'GELİŞTİRİCİ DÖNÜT (ÇABAYA ÖVGÜ)'. Sub-labels: 'ZAMANINDA MÜDAHALE', 'YOL GÖSTERİCİ (FEEDFORWARD)', 'SANDVİÇ YÖNTEMİ'. "
            "Right column in subtle red warning tint labeled: 'YIKICI ELEŞTİRİ (KİŞİLİĞE SALDIRI)'. Sub-labels: 'GECİKMİŞ YARGILAMA', 'ÖĞRENİLMİŞ ÇARESİZLİK'. "
            "STRICT MANDATORY RULE: All text labels strictly in Turkish. Giant bold legible typography. "
            "Absolutely NO small paragraphs, NO tiny explanatory text. Max readability at small scale."
        )
    },
    {
        "filename": "derse hazırlık boyutları.jpg",
        "title": "Bölüm 2 - Sf 1: Derse Yeterince Hazırlığın 4 Boyutu",
        "prompt": (
            "Minimalist 4-quadrant geometric vector diagram, 4:3 aspect ratio, clean light parchment background. "
            "Four large rounded concept cards arranged in a 2x2 grid around a central compass motif labeled 'KEŞFETME YOLCULUĞU': "
            "1. Top-Left: '1. ALAN BİLGİSİ (KONUYA HÂKİMİYET)', "
            "2. Top-Right: '2. YÖNTEM & TEKNİK (AKTİF ÖĞRETİM)', "
            "3. Bottom-Left: '3. MATERYAL & B PLANI (KRİZ GÜVENCESİ)', "
            "4. Bottom-Right: '4. GÜNCEL BAĞLAM (HAYATLA KÖPRÜ)'. "
            "STRICT MANDATORY RULE: All text labels strictly in Turkish. Bold, giant typography. "
            "No paragraphs, no tiny side notes. Theme colors: porcelain navy (#1F4775) and warm gold."
        )
    },
    {
        "filename": "zaman yönetimi şeması.jpg",
        "title": "Bölüm 2 - Sf 2: Öğretmenin Zaman Yönetimi & Öğrenci Planlama Piramidi",
        "prompt": (
            "Clean hierarchical vector pyramid and clock diagram, 4:3 aspect ratio, light parchment ivory background. "
            "A stylized wall clock alongside a 3-tier pyramid. "
            "Pyramid tiers labeled in large bold Turkish: "
            "Base tier: 'HAFTALIK ÇALIŞMA TAKVİMİ', "
            "Middle tier: 'DÖNEMLİK HEDEF HARİTASI', "
            "Top golden peak: 'KİTAP OKUMA DİSİPLİNİ'. "
            "A banner below the clock labeled: '0 ÖLÜ ZAMAN = 0 DİSİPLİN KRİZİ'. "
            "STRICT MANDATORY RULE: All text labels strictly in Turkish. Giant bold typography. "
            "Theme colors: deep navy (#1F4775) and gold. Uncluttered, crisp lines."
        )
    },
    {
        "filename": "öğrenciye destek alanları.jpg",
        "title": "Bölüm 3 - Sf 1: Öğrenci Destek Çemberi & Psikolojik Güvenlik",
        "prompt": (
            "Minimalist circular flower/shield vector diagram, 4:3 aspect ratio, light ivory parchment background. "
            "A protective central golden core labeled: 'PSİKOLOJİK GÜVENLİK İKLİMİ'. "
            "Four surrounding interconnected satellite nodes in deep navy (#1F4775): "
            "Node 1: 'ÇEKİNGENLERE MİKRO-GÖREV', "
            "Node 2: 'HATA = ÖĞRENME FIRSATI', "
            "Node 3: 'GAYRET ODAKLI TAKDİR', "
            "Node 4: 'GELECEK HEDEFİ REHBERLİĞİ'. "
            "STRICT MANDATORY RULE: All text labels strictly in Turkish. Giant bold legible typography. "
            "No small sentences, no tiny notes. Maximum contrast and readability."
        )
    },
    {
        "filename": "saygı aynası modeli.jpg",
        "title": "Bölüm 3 - Sf 2: Saygı Bir Aynadır & Saygın Otorite İnşası",
        "prompt": (
            "Clean vector conceptual illustration of an ornate mirror reflecting light, 4:3 aspect ratio, elegant light parchment background. "
            "Top banner in large bold Turkish: 'SAYGI BİR AYNADIR (YANSIYAN DEĞER)'. "
            "Two large interacting pillars flanking the mirror: "
            "Left pillar: 'ÖĞRETMENİN NEZAKETİ & ÖZRÜ' -> reflective beam -> Right pillar: 'ÖĞRENCİNİN HAKİKİ HÜRMETİ'. "
            "Bottom summary badge: 'KORKU DAYATMASI DEĞİL, ADALET VE ŞEFKAT OTORİTESİ'. "
            "STRICT MANDATORY RULE: All text labels strictly in Turkish. Giant bold typography. "
            "Theme colors: porcelain navy (#1F4775) and warm gold."
        )
    },
    {
        "filename": "altı şapka renkleri.jpg",
        "title": "Bölüm 4 - Sf 1: Edward de Bono 6 Şapkalı Düşünme Renk Matrisi",
        "prompt": (
            "Clean and elegant vector infographic showcasing 6 distinct classic hats arranged in a circle, 4:3 aspect ratio, light parchment background. "
            "Each hat has its prominent bold Turkish concept label right next to it: "
            "1. White Hat: 'BEYAZ: TARAFIZ BİLGİ & VERİLER', "
            "2. Red Hat: 'KIRMIZI: DUYGULAR & SEZGİLER', "
            "3. Black Hat: 'SİYAH: KÖTÜMSER RİSK ANALİZİ', "
            "4. Yellow Hat: 'SARI: İYİMSER FIRSAT BAKIŞI', "
            "5. Green Hat: 'YEŞİL: YARATICI ALTERNATİFLER', "
            "6. Blue Hat: 'MAVİ: SÜREÇ YÖNETİCİSİ & KARAR'. "
            "Center label: 'PARALEL DÜŞÜNME'. "
            "STRICT MANDATORY RULE: All text labels strictly in Turkish. Giant bold typography. "
            "High contrast, clean vectors, zero paragraphs, zero tiny text."
        )
    },
    {
        "filename": "beyin fırtınası aşamaları.jpg",
        "title": "Bölüm 4 - Sf 2: Beyin Fırtınası 2 Aşamalı Akış Şeması",
        "prompt": (
            "Clean linear two-stage vector process flow diagram, 4:3 aspect ratio, light parchment background. "
            "Two large sequential process blocks connected by a dynamic bold golden arrow: "
            "Stage 1 Box (Deep Navy): '1. AŞAMA: FİKİR ÜRETME'. Sub-badge: 'ELEŞTİRİ KESİNLİKLE YASAK! MİKTAR KALİTEYİ DOĞURUR'. "
            "Stage 2 Box (Warm Gold): '2. AŞAMA: DEĞERLENDİRME'. Sub-badge: 'GRUPLAMA, ELEME VE UYGULANABİLİR ÇÖZÜMLERİ SEÇME'. "
            "STRICT MANDATORY RULE: All text labels strictly in Turkish. Giant bold legible typography. "
            "No tiny body text, no bullet points. Theme colors: porcelain navy (#1F4775) and gold."
        )
    },
    {
        "filename": "balık kılçığı şablonu.jpg",
        "title": "Bölüm 5 - Sf 1: Kaoru Ishikawa Balık Kılçığı Neden-Sonuç Şeması",
        "prompt": (
            "Clean academic vector Ishikawa fishbone diagram, 4:3 aspect ratio, light ivory parchment background. "
            "Fish head on the right labeled in large bold text: 'PROBLEM (DİKKAT DAĞINIKLIĞI)'. "
            "Central horizontal spine with 4 prominent angled diagonal ribs: "
            "Top rib 1: 'YÖNTEM / DERS', Top rib 2: 'ÖĞRETMEN / İLETİŞİM', "
            "Bottom rib 1: 'AİLE / ÇEVRE', Bottom rib 2: 'DİJİTAL MEDYA'. "
            "Each rib has 2 small horizontal sub-branches with short labels: 'Monotonluk', 'Boşluk', 'Uykusuzluk', 'Ekran'. "
            "STRICT MANDATORY RULE: All text labels strictly in Turkish. Giant bold legible typography. "
            "Colors: porcelain navy (#1F4775), antique gold and bone white."
        )
    },
    {
        "filename": "arkası yarın ve ben kimim.jpg",
        "title": "Bölüm 5 - Sf 2: Arkası Yarın Süreci & Ben Kimim Kartı",
        "prompt": (
            "Clean side-by-side vector infographic, 4:3 aspect ratio, light ivory parchment background. "
            "Left half: 'ARKASI YARIN (ZEİGARNİK ETKİSİ)'. Illustration of a video play button paused at a cliffhanger, leading to a student writing a script. "
            "Right half: 'BEN KİMİM? (PEKİŞTİRME & KAYNAŞMA)'. Illustration of a deck of concept clue cards with a question mark badge. "
            "Center connective banner: 'MERAK VE PEKİŞTİRME PEDAGOJİSİ'. "
            "STRICT MANDATORY RULE: All text labels strictly in Turkish. Giant bold typography. "
            "Theme colors: deep navy (#1F4775) and warm gold accents."
        )
    },
    {
        "filename": "Edward de Bono.jpg",
        "title": "Kişi Portresi: Edward de Bono",
        "prompt": (
            "Historical and academic portrait illustration of Edward de Bono, 4:3 aspect ratio, elegant light parchment ivory background. "
            "Distinguished thinker, gentle scholarly smile, wearing formal suit with a subtle colored lapel pin reflecting the six thinking hats. "
            "Theme colors: porcelain navy (#1F4775) and warm antique gold frame. Classic editorial portrait style."
        )
    },
    {
        "filename": "Kaoru Ishikawa.jpg",
        "title": "Kişi Portresi: Kaoru Ishikawa",
        "prompt": (
            "Historical and academic portrait illustration of Kaoru Ishikawa, 4:3 aspect ratio, elegant light parchment ivory background. "
            "Japanese engineering and management scholar with spectacles and formal academic suit, dignified and calm demeanor. "
            "Theme colors: porcelain navy (#1F4775) and warm antique gold frame. Minimalist scholarly editorial portrait style."
        )
    }
]

def generate_and_download():
    for d in OUTPUT_DIRS:
        os.makedirs(d, exist_ok=True)
    urls = [
        f"https://fal.run/{MODEL_ENDPOINT}",
        f"https://fal.run/fal-ai/{MODEL_ENDPOINT}"
    ]

    total = len(TASKS)
    print(f"=== FAL.AI GÖRSEL ÜRETİMİ BAŞLATILIYOR (Toplam {total} Görsel) ===")
    print(f"Standart: 4:3 Oran, Low Kalite, JPEG Formatı, Çini Laciverti (#1F4775) & Altın")
    
    for idx, item in enumerate(TASKS, 1):
        target_path = os.path.join(OUTPUT_DIRS[0], item["filename"])
        if os.path.exists(target_path) and os.path.getsize(target_path) > 10000:
            print(f"[{idx}/{total}] Zaten mevcut, atlanıyor: {item['filename']}")
            continue
            
        print(f"[{idx}/{total}] Başlatılıyor: {item['title']} -> {item['filename']}")
        
        payload = {
            "prompt": item["prompt"],
            "quality": "low",
            "image_size": "landscape_4_3",
            "output_format": "jpeg",
            "num_images": 1
        }
        
        success = False
        for url in urls:
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
                with urllib.request.urlopen(req, timeout=90) as resp:
                    res_data = json.loads(resp.read().decode("utf-8"))
                    images = res_data.get("images", [])
                    if not images:
                        print(f"  HATA: Görsel URL'si dönmedi! Yanıt: {res_data}")
                        continue
                    img_url = images[0].get("url")
                    print(f"  Görsel oluşturuldu: {img_url}")
                    
                    urllib.request.urlretrieve(img_url, target_path)
                    print(f"  BAŞARILI: Kaydedildi -> {target_path}")
                    success = True
                    break
                    
            except urllib.error.HTTPError as e:
                err = e.read().decode('utf-8')
                print(f"  HTTPError {e.code} ({url}): {err[:150]}")
            except Exception as e:
                print(f"  Hata ({url}): {e}")
                
        time.sleep(1)

    print("=== TÜM GÖRSELLER TAMAMLANDI ===")

if __name__ == "__main__":
    generate_and_download()
