import os
import json
import time
import urllib.request
import urllib.error

FAL_KEY = os.environ.get("FAL_KEY", "fal_sk_c217e0df40a141deb539143fb2995359:3177c261a8b0173cd99440fd011a9720")
MODEL_ENDPOINT = "openai/gpt-image-2.5/sunburst/text-to-image"

OUTPUT_DIRS = [
    r"c:\Users\ASUS\OneDrive\OKUL\ders-uretim-sistemi\3-sinif\1-donem\vize\görseller",
    r"c:\Users\ASUS\OneDrive\OKUL\ders-uretim-sistemi\3-sinif\1-donem\vize\gorsel_ders_notlari\TASAVVUF I\3. Hafta\görseller",
    r"c:\Users\ASUS\OneDrive\OKUL\ders-uretim-sistemi\3-sinif\1-donem\vize\gorsel_ders_notlari\TASAVVUF I\görseller",
]

TASKS = [
    {
        "filename": "1_cibril_hadisi_ihsan_sacayagi.jpg",
        "title": "Bölüm 1: Nebevî Zühd ve Cibrîl Hadisi İhsan Sacayağı",
        "prompt": (
            "Educational clean vector infographic diagram, 4:3 aspect ratio, elegant ivory parchment background. "
            "Three classical Islamic marble columns supporting an arch, symbolizing the three foundational pillars of religion from the Hadith of Gabriel: "
            "Left column labeled 'İSLÂM / FIKIH' (actions and law), Middle column labeled 'İMAN / KELÂM' (creed and heart), "
            "Right glowing golden column labeled 'İHSAN / TASAVVUF' (spiritual excellence, worshipping Allah as if seeing Him). "
            "Arch apex with golden crest labeled 'CİBRÎL HADİSİ'. Minimalist Islamic geometric design, deep plum purple (#7B3260) and gold accents, clear scholastic visual."
        )
    },
    {
        "filename": "2_hadisi_veli_kurbiyet_piramidi.jpg",
        "title": "Bölüm 2: Hadis-i Velî ve Kurbiyet Piramidi",
        "prompt": (
            "Educational 3-tier hierarchical pyramid infographic in 4:3 aspect ratio, light parchment background. "
            "Base tier: 'ÂMM VELÂYET' (General Sainthood of all believers). "
            "Middle wide tier: 'KURB-I FERÂİZ' (Obligatory deeds - foundation of divine proximity). "
            "Top illuminated golden apex: 'KURB-I NEVÂFİL & HÂSS VELÂYET' (Supererogatory deeds - seeing eye, hearing ear of the beloved servant). "
            "Decorated with a subtle vintage Sufi traveler staff and manuscript scrolls on the side. "
            "Deep plum purple (#7B3260) and antique gold vector styling, clear typography."
        )
    },
    {
        "filename": "3_ihlas_ve_riya_terazisi.jpg",
        "title": "Bölüm 3: İbadette İhlâs ve Riyâ Terazisi",
        "prompt": (
            "A conceptual comparison infographic in 4:3 aspect ratio featuring a golden mizan balance scale on parchment. "
            "Left heavy glowing pan labeled 'İHLÂS (GÖNÜL DERVİŞLİĞİ)' with pure heart and sincere prayer rug icon, shining with warm light. "
            "Right light tilted pan in shadow labeled 'RİYÂ (GÖSTERİŞ)' with superficial cloaks and showing-off symbols. "
            "At the bottom, a subtle historic dawn mosque doorway with a dog silhouette referencing the story of sincerity in dawn prayer. "
            "Minimalist Islamic scholarly vector art, deep plum purple and gold."
        )
    },
    {
        "filename": "4_insanin_ontolojisi_melek_hayvan.jpg",
        "title": "Bölüm 4: İnsanın Ontolojik Konumu (Melek, Hayvan, İnsan)",
        "prompt": (
            "Vertical ontological hierarchy infographic diagram in 4:3 aspect ratio, parchment backdrop. "
            "Top sphere: 'MELEK' (Angels: Pure Intellect, no desires). "
            "Bottom sphere: 'HAYVAN' (Animals: Pure Desires, no intellect). "
            "Center prominent sphere: 'İNSAN' (Human: Endowed with both intellect and desires). "
            "Two clear pathway arrows: Upward golden arrow pointing to 'AHSEN-İ TAKVÎM' (transcending angels through spiritual purification), "
            "Downward arrow pointing to 'ESFEL-İ SÂFİLÎN' (falling lower than beasts). "
            "Centered with 'Men arefe nefsehu' self-knowledge mirror motif. Scholarly vector illustration."
        )
    },
    {
        "filename": "5_sufi_kelimesinin_kok_tahlili.jpg",
        "title": "Bölüm 5: Sûfî Kelimesinin 9 Kök Tahlili",
        "prompt": (
            "Etymological linguistic elimination tree chart in 4:3 aspect ratio on clean parchment background. "
            "Header in fine calligraphy: 'SÛFÎ VE TASAVVUF'. "
            "Branches showing rejected root claims with clear red strike badges: 'Suffe -> Suffî (Geçersiz)', "
            "'Safâ -> Safevî (Geçersiz)', 'Saff -> Saffî (Geçersiz)', 'Sufâne (Geçersiz)', 'Sophia (Geçersiz)'. "
            "Branch leading to ONE prominent, golden highlighted victor branch: 'ES-SÛF (الصُّوف - KABA YÜN)' "
            "verified by morphological rules (Tasavvefe - wearing wool). Deep plum purple and gold accents, crisp academic infographic."
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
