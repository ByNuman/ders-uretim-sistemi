import os
import json
import time
import urllib.request
import urllib.error

FAL_KEY = os.environ.get("FAL_KEY", "fal_sk_c217e0df40a141deb539143fb2995359:3177c261a8b0173cd99440fd011a9720")
MODEL_ENDPOINT = "openai/gpt-image-2.5/sunburst/text-to-image"

OUTPUT_DIRS = [
    r"c:\Users\ASUS\OneDrive\OKUL\ders-uretim-sistemi\3-sinif\1-donem\vize\gorsel_ders_notlari\TASAVVUF I\3. Hafta\görseller",
    r"c:\Users\ASUS\OneDrive\OKUL\ders-uretim-sistemi\3-sinif\1-donem\vize\gorsel_ders_notlari\TASAVVUF I\görseller",
]

TASKS = [
    {
        "filename": "1_cibril_hadisi_ihsan_sacayagi.jpg",
        "title": "Bölüm 1: Nebevî Zühd ve Cibrîl Hadisi İhsan Sacayağı",
        "prompt": (
            "Extremely clean and minimalist academic vector infographic diagram, 4:3 aspect ratio, elegant light parchment ivory background. "
            "A classical Islamic arch supported by three prominent marble pillars. "
            "Only three large, bold Turkish text labels on the pillars: Left pillar: 'İSLÂM (FIKIH)', Middle pillar: 'İMAN (KELÂM)', Right pillar glowing in gold: 'İHSAN (TASAVVUF)'. "
            "Arch crest labeled 'CİBRÎL HADİSİ'. Bold flow arrows connecting them. "
            "STRICT MANDATORY RULE: All text labels must be strictly in Turkish. Bold and large legible typography. "
            "Absolutely NO small paragraphs, NO bullet points, NO tiny explanatory text. Only 3 to 4 prominent, huge Turkish concept labels and clean boxes. "
            "Theme colors: deep plum purple (#7B3260) and warm gold. Maximum readability at small scale."
        )
    },
    {
        "filename": "2_hadisi_veli_kurbiyet_piramidi.jpg",
        "title": "Bölüm 2: Hadis-i Velî ve Kurbiyet Piramidi",
        "prompt": (
            "Minimalist 3-tier hierarchical pyramid vector diagram, 4:3 aspect ratio, clean light parchment background. "
            "Only three bold Turkish text tiers in large legible font: "
            "Base tier: 'ÂMM VELÂYET (TÜM MÜMİNLER)', Middle prominent tier: 'KURB-I FERÂİZ (FARZLAR)', Top glowing golden peak: 'KURB-I NEVÂFİL (HÂSS VELÂYET)'. "
            "Upward golden direction arrow on the side labeled 'KURBİYET (YAKINLIK)'. "
            "STRICT MANDATORY RULE: All text labels strictly in Turkish. Bold, giant legible typography. "
            "Absolutely NO small paragraphs, NO tiny explanatory text, NO bullet points, NO tiny side notes. "
            "High contrast, clean geometric cards, theme colors deep plum purple (#7B3260) and gold. Maximum readability at small scale."
        )
    },
    {
        "filename": "3_ihlas_ve_riya_terazisi.jpg",
        "title": "Bölüm 3: İbadette İhlâs ve Riyâ Terazisi",
        "prompt": (
            "Clean minimalist vector comparison diagram, 4:3 aspect ratio, light parchment background. "
            "A large golden balance scale (mizan) in the center. "
            "Left heavy pan glowing with light labeled with large bold Turkish text: 'İHLÂS (GÖNÜL DERVİŞLİĞİ)'. "
            "Right light pan tilted upward in shadow labeled with large bold Turkish text: 'RİYÂ (GÖSTERİŞ)'. "
            "Two contrasting large concept boxes: 'TENHADA SAMİMİYET' versus 'GÖSTERİŞLİ KİSVE'. "
            "STRICT MANDATORY RULE: All text labels strictly in Turkish. Giant bold legible typography. "
            "Absolutely NO small paragraphs, NO bullet points, NO tiny quotes or explanatory text. "
            "Only 3 to 4 prominent, huge Turkish concept labels. Theme colors: deep plum purple (#7B3260) and gold."
        )
    },
    {
        "filename": "4_insanin_ontolojisi_melek_hayvan.jpg",
        "title": "Bölüm 4: İnsanın Ontolojik Konumu (Melek, Hayvan, İnsan)",
        "prompt": (
            "Vertical ontological vector hierarchy diagram, 4:3 aspect ratio, clean ivory parchment backdrop. "
            "Extremely minimalist, uncluttered layout. Three prominent circular concept nodes: "
            "Top: 'MELEK (AKIL)', Center: 'İNSAN (AKIL + NEFİS)', Bottom: 'HAYVAN (ŞEHVET)'. "
            "Two large bold directional arrows from center: Upward golden arrow labeled 'AHSEN-İ TAKVÎM ⬆', Downward arrow labeled 'ESFEL-İ SÂFİLÎN ⬇'. "
            "Center mirror motif labeled: 'NEFSİNİ BİLMEK'. "
            "STRICT MANDATORY RULE: All text labels strictly in Turkish. Giant bold legible typography. "
            "Absolutely NO side paragraphs, NO small quotes, NO tiny bullet text, NO explanatory sentences. "
            "Only 5 large prominent Turkish concept labels. Maximum readability at small box scale. Deep plum purple and gold."
        )
    },
    {
        "filename": "5_sufi_kelimesinin_kok_tahlili.jpg",
        "title": "Bölüm 5: Sûfî Kelimesinin 9 Kök Tahlili",
        "prompt": (
            "Minimalist etymological decision tree vector infographic, 4:3 aspect ratio, clean parchment background. "
            "Top title in large bold Turkish lettering: 'SÛFÎ KELİMESİNİN KÖKENİ'. "
            "Left branch with red strike marks: 'SUFFE / SAFÂ / SAFF (GEÇERSİZ)'. "
            "Right branch glowing in bold gold box: 'ES-SÛF / YÜN (TEK GEÇERLİ KÖK)'. "
            "Result box below: 'TASAVVEFE (YÜN GİYDİ)'. "
            "STRICT MANDATORY RULE: All text labels strictly in Turkish. Giant bold typography. "
            "Absolutely NO small sentences, NO tiny notes, NO paragraphs. "
            "Only large, bold Turkish concept cards and flow arrows. High contrast, maximum legibility at small scale, deep plum purple (#7B3260) and antique gold."
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

    for idx, item in enumerate(TASKS, 1):
        print(f"[{idx}/5] Başlatılıyor: {item['title']} -> {item['filename']}")
        
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
                    
                    # Tüm hedef dizinlere kaydet
                    primary_path = os.path.join(OUTPUT_DIRS[0], item["filename"])
                    urllib.request.urlretrieve(img_url, primary_path)
                    for extra_dir in OUTPUT_DIRS[1:]:
                        extra_path = os.path.join(extra_dir, item["filename"])
                        import shutil
                        shutil.copy(primary_path, extra_path)
                    print(f"  BAŞARILI: Kaydedildi ({len(OUTPUT_DIRS)} konuma) -> {primary_path}")
                    success = True
                    break
                    
            except urllib.error.HTTPError as e:
                err = e.read().decode('utf-8')
                print(f"  HTTPError {e.code} ({url}): {err[:150]}")
            except Exception as e:
                print(f"  Hata ({url}): {e}")
                
        time.sleep(1)

if __name__ == "__main__":
    generate_and_download()
