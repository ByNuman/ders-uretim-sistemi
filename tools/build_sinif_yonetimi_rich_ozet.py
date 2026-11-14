# -*- coding: utf-8 -*-
"""
tools/build_sinif_yonetimi_rich_ozet.py
======================================
Sınıf Yönetimi Vize Hazırlık Özeti için zenginleştirilmiş, pedagojik materyal kartları,
kavram rozetleri (==kavram==), çeldirici uyarı kutuları ve çift katmanlı mimariye sahip
master Markdown ve Okuma PDF üreticisi.
"""

import sys
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.okuma_pdf import generate_okuma_pdf

MD_TARGET_1 = ROOT / "3-sinif/1-donem/vize/ders_anlatimlari/SINIF YÖNETİMİ/Sınıf Yönetimi - Vize Sınavı Hazırlık Özeti.md"
MD_TARGET_2 = ROOT / "3-sinif/1-donem/vize/kaynaklar/özetlenmiş_dersler/SINIF YÖNETİMİ/sinif-yonetimi-vize-ozeti.md"

def get_content():
    return """# PFD309 SINIF YÖNETİMİ — VİZE SINAVI HAZIRLIK ÖZETİ
### (1. Hafta Kuramsal Temeller + Bölüm I: Strateji 1–25 + Bölüm V: Etkinlik 1–30 + Vaka/Kitap/Film Analizleri)

> [!IMPORTANT]
> **Pedagojik Metot ve Kapsam:** Bu doküman; Amasya Üniversitesi İlahiyat Fakültesi 3. Sınıf 1. Dönem **PFD309 Sınıf Yönetimi** dersi vize müfredatını (1–7. Haftalar) eksiksiz kapsar. Her ana konunun başında kavramı zihinde berraklaştıran **modern vektörel infografik materyaller (süreç döngüleri, hiyerarşik değer piramitleri, 2x2 eksen matrisleri, doktrin mukayese levhaları, zaman çizelgeleri ve formül kartları)** yer almakta; materyallerin hemen altında ise sınavda soru değeri taşıyan tüm **terim, tanım, kuramcı, model, yöntem ve basamaklar** sıfır bilgi kaybı standardıyla sunulmaktadır.

---

## İÇİNDEKİLER

1. [Ünite 1: Sınıf Yönetiminin Kuramsal Temelleri, Boyutları ve Modelleri (1. Hafta)](#ünite-1-sınıf-yönetiminin-kuramsal-temelleri-boyutları-ve-modelleri-1-hafta)
2. [Ünite 2: Öz Farkındalık, İletişim ve Aktif Öğretim Teknikleri 1–5 (2. Hafta / 1. Grup)](#ünite-2-öz-farkındalık-iletişim-ve-aktif-öğretim-teknikleri-15-2-hafta--1-grup)
3. [Ünite 3: Geribildirim, Planlama, Hazırlık ve Düşünme Becerileri 6–10 (3. Hafta / 2. Grup)](#ünite-3-geribildirim-planlama-hazırlık-ve-düşünme-becerileri-610-3-hafta--2-grup)
4. [Ünite 4: Sınıf İklîmi, Kurallar, Mahremiyet ve Pekiştirme Teknikleri 11–15 (4. Hafta / 3. Grup)](#ünite-4-sınıf-iklîmi-kurallar-mahremiyet-ve-pekiştirme-teknikleri-1115-4-hafta--3-grup)
5. [Ünite 5: Sosyal Sorumluluk, Sorun Çözme, Mizah, Hayal ve Zaman Yönetimi 16–20 (5. Hafta / 4. Grup)](#ünite-5-sosyal-sorumluluk-sorun-çözme-mizah-hayal-ve-zaman-yönetimi-1620-5-hafta--4-grup)
6. [Ünite 6: Motivasyon, Öğrenmeyi Öğretmek, Liderlik, Entelektüel Öğretmen ve Öğretmenler Odası 21–25 (6. Hafta / 5. Grup)](#ünite-6-motivasyon-öğrenmeyi-öğretmek-liderlik-entelektüel-öğretmen-ve-öğretmenler-odası-2125-6-hafta--5-grup)
7. [Ünite 7: İleri Düzey Aktif Öğretim Teknikleri 26–30 (7. Hafta)](#ünite-7-ileri-düzey-aktif-öğretim-teknikleri-2630-7-hafta)

---

# ÜNİTE 1: SINIF YÖNETİMİNİN KURAMSAL TEMELLERİ, BOYUTLARI VE MODELLERİ (1. HAFTA)

## 1.1. Yönetim, Sınıf Yönetimi ve Açık Sistem Olarak Sınıf

<div class="tree-diagram-wrap">
    <div class="tree-diagram-banner">
        <span>🏛️ SİSTEM YAKLAŞIMI: AÇIK SİSTEM OLARAK SINIFIN YAPISAL ANATOMİSİ</span>
    </div>
    <div class="tree-body">
        <div class="tree-root-node">
            <strong>AÇIK SİSTEM OLARAK SINIF</strong><br>
            <small>Sürekli Girdi Alan, İşleyen, Çevreyle Etkileşen Dinamik Sosyal Ekosistem</small>
        </div>
        <div class="tree-connector-down"></div>
        <div class="tree-main-branches">
            <div class="tree-main-branch">
                <div class="tree-branch-header">1. GİRDİLER (KAYNAKLAR)</div>
                <div class="tree-subnodes">
                    <div class="tree-subnode-card">
                        <div class="tree-subnode-title">İNSAN GÜCÜ</div>
                        <div class="tree-subnode-desc">Öğretmen niteliği, öğrenci hazırbulunuşluğu, ilgi, gelişim basamağı ve beklentiler.</div>
                    </div>
                    <div class="tree-subnode-card">
                        <div class="tree-subnode-title">MADİ &amp; PROGRAM</div>
                        <div class="tree-subnode-desc">Müfredat kazanımları, ders araç-gereçleri, fiziksel donanım, ısı, ışık ve oturma düzeni.</div>
                    </div>
                </div>
            </div>
            <div class="tree-main-branch" style="background: #fffdf5; border-color: #fde68a;">
                <div class="tree-branch-header" style="background: #b45309;">2. SÜREÇ (6 YAPISAL ÖZELLİK)</div>
                <div class="tree-subnodes">
                    <div class="tree-subnode-card">
                        <div class="tree-subnode-title" style="color: #b45309;">ÇOK BOYUTLULUK &amp; EŞ ZAMANLILIK</div>
                        <div class="tree-subnode-desc">Aynı anda çok farklı eylemlerin eşzamanlı cereyan etmesi.</div>
                    </div>
                    <div class="tree-subnode-card">
                        <div class="tree-subnode-title" style="color: #b45309;">ANINDALIK &amp; KESTİRİLEMEZLİK</div>
                        <div class="tree-subnode-desc">Beklenmedik krizler ve öğretmenin anında karar mecburiyeti.</div>
                    </div>
                    <div class="tree-subnode-card">
                        <div class="tree-subnode-title" style="color: #b45309;">AÇIKLIK &amp; TARİHSELLİK</div>
                        <div class="tree-subnode-desc">Tüm eylemlerin sahnede olması ve ortak geçmişin bugünü etkilemesi.</div>
                    </div>
                </div>
            </div>
            <div class="tree-main-branch" style="background: #f0fdf4; border-color: #bbf7d0;">
                <div class="tree-branch-header" style="background: #166534;">3. ÇIKTILAR &amp; DÖNÜT</div>
                <div class="tree-subnodes">
                    <div class="tree-subnode-card">
                        <div class="tree-subnode-title" style="color: #166534;">AKADEMİK &amp; AHLAKİ</div>
                        <div class="tree-subnode-desc">Kalıcı öğrenme, üstbilişsel beceri, sorumluluk ve değerler kazanımı.</div>
                    </div>
                    <div class="tree-subnode-card">
                        <div class="tree-subnode-title" style="color: #166534;">ÖZ-DİSİPLİN &amp; İKLİM</div>
                        <div class="tree-subnode-desc">Otokontrol sahibi bireyler ve güvenli, demokratik sınıf iklimi.</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

### Tam ve Eksiksiz Konu Anlatımı:
* **Yönetim Kavramı:** Belirli örgütsel hedeflere ulaşmak amacıyla maddi ve beşerî kaynakları ==planlama==, ==örgütleme== (organize etme), ==yöneltme== (sevk ve idare), ==eşgüdümleme== (koordinasyon) ve ==denetleme== (kontrol) süreçlerinin bütünüdür.
* **Sınıf Yönetimi:** Sınıfta yalnızca asayiş ve sessizliği sağlamak (gardiyanlık) değil; etkili bir öğretme-öğrenme ekosistemini **planlama, kurma, geliştirme ve sürdürme** sanatıdır.
* **Açık Sistem Olarak Sınıf ve 6 Temel Karakteristiği:** Sınıf; çevresinden sürekli girdi alan, girdileri ders sürecinde işleyen ve topluma çıktı veren yaşayan bir açık sistemdir. Kendine has **6 yapısal özelliği** sınavların temel soru kaynağıdır:
  1. **Çok Boyutluluk (Multidimensionality):** Sınıfta aynı anda birbirinden bağımsız pek çok olayın cereyan etmesidir (öğretmen tahtaya yazar, bir öğrenci not tutar, diğeri camdan bakar, arkadaki fısıldaşır).
  2. **Eş Zamanlılık (Simultaneity):** Bu çok boyutlu olayların peş peşe değil, aynı zaman diliminde eşzamanlı yaşanması ve öğretmenin hepsini takip etme zorunluluğudur.
  3. **Anındalık / Çabukluk (Immediate Reaction):** Sınıf olaylarının aniden patlak vermesi; öğretmenin uzun uzadıya düşünme lüksü olmadan anında pedagojik karar vermesini zorunlu kılmasıdır.
  4. **Kestirilemezlik / Öngörülemezlik (Unpredictability):** Ders ne kadar kusursuz planlanırsa planlansın, sınıfta her an beklenmedik bir kriz, şaka veya teknik arızanın ortaya çıkabilmesidir.
  5. **Açıklık / Aleniyet (Publicness):** Sınıfta gizlilik yoktur; öğretmenin bir öğrenciye verdiği ödül, ceza veya gösterdiği jest tüm sınıfın gözü önünde (adeta sahnede) cereyan eder.
  6. **Tarihsellik / Ortak Geçmiş (History):** İlk haftalarda konulan kurallar, yaşanan krizler veya paylaşılan espriler zamanla ortak bir sınıf kültürü inşa eder; geçmiş yaşantılar sonraki haftaların iklimini doğrudan belirler.

---

## 1.2. Sınıf Yönetimi ile Sınıf Disiplini Arasındaki Fark

<div class="doctrine-compare-wrap">
    <div class="cycle-banner">
        <span>⚖️ SINIF YÖNETİMİ (GENİŞ &amp; PROAKTİF) vs SINIF DİSİPLİNİ (DAR &amp; REAKTİF)</span>
    </div>
    <div class="entity-grid-2">
        <div class="dok-card" style="border-left: 4px solid #1F4775;">
            <div class="dok-card-header">
                <span class="dok-pill" style="background: #1F4775; color: #fff;">GENİŞ VE BÜTÜNCÜL ŞEMSİYE</span>
                <strong style="color: #1F4775; display: block; margin-top: 4px; font-size: 10.5pt;">SINIF YÖNETİMİ (PROAKTİF)</strong>
            </div>
            <p style="font-size: 8.8pt; line-height: 1.45; color: #334155;">
                • <strong>Temel Amaç:</strong> Öğrenmeye elverişli ortamı baştan tasarlamak ve sürdürmek.<br>
                • <strong>Zamanlama:</strong> Sorunlar ortaya çıkmadan önce tedbir alma (Önlemsel).<br>
                • <strong>Kapsam:</strong> Fiziksel düzen, plan, iklim, iletişim, zaman ve motivasyon.<br>
                • <strong>Öğrenci Rolü:</strong> Sürecin aktif ortağı, sorumluluk sahibi bağımsız <strong>özne</strong>.<br>
                • <strong>Hedef:</strong> Dış baskı olmaksızın <strong>öz-disiplin (otokontrol)</strong> inşası.
            </p>
        </div>
        <div class="dok-card" style="border-left: 4px solid #dc2626;">
            <div class="dok-card-header">
                <span class="dok-pill" style="background: #dc2626; color: #fff;">DAR VE MÜDAHALE ODAKLI</span>
                <strong style="color: #dc2626; display: block; margin-top: 4px; font-size: 10.5pt;">SINIF DİSİPLİNİ (REAKTİF)</strong>
            </div>
            <p style="font-size: 8.8pt; line-height: 1.45; color: #334155;">
                • <strong>Temel Amaç:</strong> Kural ihlalini bastırmak ve bozulan düzeni geri kazanmak.<br>
                • <strong>Zamanlama:</strong> İstenmeyen davranış gerçekleştikten sonra (Tepkisel).<br>
                • <strong>Kapsam:</strong> Yalnızca kurallar, sınırlar ve yaptırım mekanizmaları.<br>
                • <strong>Öğrenci Rolü:</strong> Kurallara mutlak uyması beklenen edilgen <strong>nesne</strong>.<br>
                • <strong>Hedef:</strong> Dışsal denetimle anlık sessizlik ve itaat sağlama.
            </p>
        </div>
    </div>
</div>

> 🎯 **Altın İlke:** İyi planlanmış, öğrencinin aktif kılındığı bir sınıfta disiplin sorunlarının **%80'i kendiliğinden ortadan kalkar**. Sınıf yönetimi proaktif bir şemsiyedir; disiplin ise onun yalnızca kural ve davranış boyutudur.

---

## 1.3. Sınıf Yönetiminin Beş Temel Boyutu (Prof. Dr. Hüseyin Başar Ekolü)

<div class="doctrine-compare-wrap">
    <div class="cycle-banner">
        <span>📐 TÜRKİYE'DE ÇAĞDAŞ SINIF YÖNETİMİNİN 5 TEMEL BOYUTU</span>
    </div>
    <div class="entity-grid-3">
        <div class="dok-card" style="border-top: 3.5px solid #0284c7;">
            <strong style="color: #0284c7; font-size: 9.6pt;">1. FİZİKSEL DÜZEN</strong>
            <p style="font-size: 8.5pt; line-height: 1.4; color: #475569; margin-top: 4px;">
                Isı, ışık, renk, gürültü, temizlik ve oturma düzenleri: <em>Sıra düzeni</em> (sunuş), <em>U düzeni</em> (tartışma/yüz yüze), <em>Küme düzeni</em> (işbirlikli grup).
            </p>
        </div>
        <div class="dok-card" style="border-top: 3.5px solid #16a34a;">
            <strong style="color: #16a34a; font-size: 9.6pt;">2. PLAN-PROGRAM</strong>
            <p style="font-size: 8.5pt; line-height: 1.4; color: #475569; margin-top: 4px;">
                Yıllık/günlük plan, kazanım hiyerarşisi, uygun yöntem ve materyal seçimi ile etkinlikler arası pürüzsüz geçişlerin tasarlanması.
            </p>
        </div>
        <div class="dok-card" style="border-top: 3.5px solid #d97706;">
            <strong style="color: #d97706; font-size: 9.6pt;">3. İLİŞKİLER (İKLİM)</strong>
            <p style="font-size: 8.5pt; line-height: 1.4; color: #475569; margin-top: 4px;">
                Öğretmen-öğrenci ve akran iletişimi, empati, karşılıklı güven, aidiyet ve ortak sınıf normlarının demokratik inşası.
            </p>
        </div>
    </div>
    <div class="entity-grid-2" style="border-top: 1px solid #e2e8f0;">
        <div class="dok-card" style="border-top: 3.5px solid #7c3aed;">
            <strong style="color: #7c3aed; font-size: 9.6pt;">4. DAVRANIŞ DÜZENLEMELERİ</strong>
            <p style="font-size: 8.5pt; line-height: 1.4; color: #475569; margin-top: 4px;">
                Olumlu davranışın pekiştirilmesi, kriz anında yapıcı müdahale, sorunun kök nedenine inme ve mantıksal sonuçların işletilmesi.
            </p>
        </div>
        <div class="dok-card" style="border-top: 3.5px solid #dc2626;">
            <strong style="color: #dc2626; font-size: 9.6pt;">5. ZAMAN YÖNETİMİ</strong>
            <p style="font-size: 8.5pt; line-height: 1.4; color: #475569; margin-top: 4px;">
                40 dakikalık sürenin bürokratik engellerle (yoklama, defter) eritilmeyip doğrudan <strong>akademik öğrenme zamanına</strong> dönüştürülmesi.
            </p>
        </div>
    </div>
</div>

---

## 1.4. Yönetim Kuramlarının Sınıf Yönetimine Yansıması

<div class="timeline-bar">
    <div class="timeline-node">
        <div class="timeline-date">1900 – 1930</div>
        <div class="timeline-title">1. KLASİK (GELENEKSEL) KURAM</div>
        <div class="timeline-desc"><strong>Taylor, Fayol, Weber:</strong> Katı hiyerarşi, mutlak otorite, yazılı kurallar, dış denetim. <em>Sınıfta:</em> "İyi sınıf çıt çıkmayan sınıftır" anlayışı, itaat ve ceza.</div>
    </div>
    <div class="timeline-node" style="border-top-color: #d97706;">
        <div class="timeline-date" style="color: #d97706;">1930 – 1960</div>
        <div class="timeline-title">2. NEO-KLASİK (İNSAN İLİŞKİLERİ)</div>
        <div class="timeline-desc"><strong>Elton Mayo (Hawthorne):</strong> İnsan duygusal ve sosyal varlıktır. Moral ve informal gruplar esastır. <em>Sınıfta:</em> Öğrencinin psikososyal ihtiyaçları ve sınıf iklimi.</div>
    </div>
    <div class="timeline-node" style="border-top-color: #16a34a;">
        <div class="timeline-date" style="color: #16a34a;">1960 ve Sonrası</div>
        <div class="timeline-title">3. ÇAĞDAŞ (SİSTEM &amp; DURUMSALLIK)</div>
        <div class="timeline-desc"><strong>Bertalanffy, Katz &amp; Kahn:</strong> Sınıf açık bir sistemdir. "Her durumda geçerli tek bir en iyi yol yoktur"; duruma ve öğrenciye göre esnek strateji seçilir.</div>
    </div>
</div>

---

## 1.5. Dört Temel Sınıf Yönetimi Modeli

<div class="concept-pyramid" style="margin: 14px 0;">
    <div class="pyramid-tier top" style="background: #f0fdf4; border-color: #16a34a; width: 68%;">
        <strong style="color: #166534; font-size: 9.6pt;">4. BÜTÜNSEL (İNTEGRATİF / SİSTEMCİ) MODEL</strong><br>
        <small style="color: #334155;">En ideal çağdaş model: Önlem ve gelişimi temel alır; kaçınılmaz krizlerde yapıcı müdahale eder.</small>
    </div>
    <div class="pyramid-tier middle" style="background: #eff6ff; border-color: #2563eb; width: 80%;">
        <strong style="color: #1e40af; font-size: 9.4pt;">3. GELİŞİMSEL MODEL</strong><br>
        <small style="color: #334155;">Kuralları ve yöntemleri öğrencinin yaş, bilişsel basamak ve olgunluk düzeyine uyarlar.</small>
    </div>
    <div class="pyramid-tier middle" style="background: #fffdf5; border-color: #d97706; width: 90%;">
        <strong style="color: #b45309; font-size: 9.4pt;">2. ÖNLEMSEL (PROAKTİF) MODEL</strong><br>
        <small style="color: #334155;">Sorun ortaya çıkmadan önce ortamı, planı ve rutinleri kurarak krizi baştan engeller.</small>
    </div>
    <div class="pyramid-tier base" style="background: #fef2f2; border-color: #dc2626; width: 100%;">
        <strong style="color: #991b1b; font-size: 9.2pt;">1. TEPKİSEL (REAKTİF) MODEL</strong><br>
        <small style="color: #334155;">Sorun çıktıktan sonra ceza/ödülle müdahale eder; kök nedeni çözmeyen en ilkel "yangın söndürme" modelidir.</small>
    </div>
</div>

---

## 1.6. Jacob Kounin Ekolü ve Etkili Ders Akışı Kavramları

<div class="doctrine-compare-wrap">
    <div class="cycle-banner">
        <span>🎬 KOUNİN (1970) VİDEO ANALİZ BULGULARI: AKIŞ VE UYANIKLIK</span>
    </div>
    <div class="entity-grid-3">
        <div class="dok-card" style="border-top: 3.5px solid #1F4775;">
            <strong style="color: #1F4775; font-size: 9.5pt;">WITHITNESS (Uyanıklık)</strong>
            <p style="font-size: 8.4pt; line-height: 1.4; color: #475569; margin-top: 4px;">
                Öğretmenin "gözünün arkasında olması"; sınıftaki her fısıltıyı, kıpırdanmayı hissettiğini beden diliyle öğrenciye yansıtmasıdır.
            </p>
        </div>
        <div class="dok-card" style="border-top: 3.5px solid #0284c7;">
            <strong style="color: #0284c7; font-size: 9.5pt;">OVERLAPPING (Binişiklik)</strong>
            <p style="font-size: 8.4pt; line-height: 1.4; color: #475569; margin-top: 4px;">
                Dersi bölmeden aynı anda iki olayı yönetebilmedir (tahtada soru çözerken arkada konuşana yaklaşarak göz teması kurma).
            </p>
        </div>
        <div class="dok-card" style="border-top: 3.5px solid #16a34a;">
            <strong style="color: #16a34a; font-size: 9.5pt;">MOMENTUM &amp; SMOOTHNESS</strong>
            <p style="font-size: 8.4pt; line-height: 1.4; color: #475569; margin-top: 4px;">
                <strong>Momentum:</strong> Canlı ders akış hızı.<br>
                <strong>Smoothness:</strong> Pürüzsüz geçiş (Tuzaklar: <em>Dangle</em> konuyu yarım bırakma; <em>Flip-flop</em> bitmiş konuya geri dönme).
            </p>
        </div>
    </div>
    <div class="entity-grid-2" style="border-top: 1px solid #e2e8f0;">
        <div class="dok-card" style="border-top: 3.5px solid #d97706;">
            <strong style="color: #d97706; font-size: 9.5pt;">GROUP ALERTING (Grubu Tetikte Tutma)</strong>
            <p style="font-size: 8.4pt; line-height: 1.4; color: #475569; margin-top: 4px;">
                Soruyu doğrudan bir kişiye sorup diğerlerini pasifleştirmek yerine; önce soruyu tüm sınıfa sorup herkesi düşündürmek, ardından rastgele söz vermektir.
            </p>
        </div>
        <div class="dok-card" style="border-top: 3.5px solid #7c3aed;">
            <strong style="color: #7c3aed; font-size: 9.5pt;">RIPPLE EFFECT (Dalga / Serpinti Etkisi)</strong>
            <p style="font-size: 8.4pt; line-height: 1.4; color: #475569; margin-top: 49x;">
                Bir öğrenciye yapılan sakin, yerinde ve adil pedagojik uyarının, sınıftaki diğer tüm öğrencilerin davranışlarını da kendiliğinden düzeltmesidir.
            </p>
        </div>
    </div>
</div>

---

## 1.7. Çağdaş Kuramcılar, Formüller ve Problem Çözme Döngüleri

### A. Thomas Gordon — "Ben Dili" İletişim Formülü

<div class="formula-card" style="justify-content: space-around; width: 100%; margin: 12px 0;">
    <div class="flow-node origin">
        <span style="font-size: 7.2pt; color: #64748b; display: block;">1. BİLEŞEN</span>
        <strong>SOMUT DAVRANIŞ</strong><br><small>Yargısız &amp; Nesnel Durum</small>
    </div>
    <span class="flow-arrow">➕</span>
    <div class="flow-node stage">
        <span style="font-size: 7.2pt; color: #92400e; display: block;">2. BİLEŞEN</span>
        <strong>SOMUT ETKİSİ</strong><br><small>Ders &amp; Zaman Kaybı</small>
    </div>
    <span class="flow-arrow">➕</span>
    <div class="flow-node stage">
        <span style="font-size: 7.2pt; color: #92400e; display: block;">3. BİLEŞEN</span>
        <strong>DUYGU İFADESİ</strong><br><small>Öğretmenin Samimi Hissi</small>
    </div>
    <span class="flow-arrow">➔</span>
    <div class="flow-node target">
        <span style="font-size: 7.2pt; color: #166534; display: block;">SONUÇ</span>
        <strong>BEN DİLİ ETKİSİ</strong><br><small>Savunmasız İçselleştirme</small>
    </div>
</div>

> 📌 **Örnek Kalıp:** *"Ders anlatılırken konuşulduğunda [davranış], dikkatim dağılıyor ve sesimi duyurmakta zorlanıyorum [somut etki]; bu yüzden konuları yetiştiremeyeceğim diye endişeleniyorum [duygu]."* Suçlayıcı ==Sen Dili== öğrenciyi savunmaya ve dirence iter; ==Ben Dili== ise empatik farkındalık üretir.

### B. Thomas Gordon — Kaybedeni Olmayan (No-Lose / III. Yol) Problem Çözme Döngüsü

<div class="cycle-flow-wrap">
    <div class="cycle-banner">
        <span>🔄 GORDON 6 ADIMLI KAYBEDENİ OLMAYAN (NO-LOSE) ÇÖZÜM DÖNGÜSÜ</span>
    </div>
    <div class="cycle-steps">
        <div class="cycle-step"><span class="cycle-step-num">1</span><span class="cycle-step-title">Sorunu Tanımla</span><span class="cycle-step-desc">İhtiyaçları netleştir</span></div>
        <div class="cycle-arrow">➔</div>
        <div class="cycle-step"><span class="cycle-step-num">2</span><span class="cycle-step-title">Fikir Üret</span><span class="cycle-step-desc">Beyin fırtınası yap</span></div>
        <div class="cycle-arrow">➔</div>
        <div class="cycle-step"><span class="cycle-step-num">3</span><span class="cycle-step-title">Değerlendir</span><span class="cycle-step-desc">Fikirleri ele</span></div>
        <div class="cycle-arrow">➔</div>
        <div class="cycle-step"><span class="cycle-step-num">4</span><span class="cycle-step-title">Ortak Karar</span><span class="cycle-step-desc">En iyi çözümü seç</span></div>
        <div class="cycle-arrow">➔</div>
        <div class="cycle-step"><span class="cycle-step-num">5</span><span class="cycle-step-title">Uygula</span><span class="cycle-step-desc">İş bölümü yap</span></div>
        <div class="cycle-arrow">➔</div>
        <div class="cycle-step" style="border-left: 3.5px solid #16a34a;"><span class="cycle-step-num">6</span><span class="cycle-step-title">Takip Et</span><span class="cycle-step-desc">Sonucu denetle</span></div>
    </div>
</div>

### C. William Glasser — Seçim Kuramı: İnsanın 5 Temel Genetik/Psikolojik İhtiyacı

<div class="concept-pyramid" style="margin: 12px 0;">
    <div class="pyramid-tier top" style="background: #fdf2f8; border-color: #db2777; width: 55%;">
        <strong style="color: #9d174d; font-size: 9.3pt;">5. EĞLENCE İHTİYACI</strong><br>
        <small style="color: #475569;">Gülme, oyun, mizah ve keyif alma ihtiyacı.</small>
    </div>
    <div class="pyramid-tier middle" style="background: #faf5ff; border-color: #9333ea; width: 68%;">
        <strong style="color: #6b21a8; font-size: 9.3pt;">4. ÖZGÜRLÜK İHTİYACI</strong><br>
        <small style="color: #475569;">Seçim yapabilme, bağımsızlık ve özerklik arzusu.</small>
    </div>
    <div class="pyramid-tier middle" style="background: #eff6ff; border-color: #2563eb; width: 80%;">
        <strong style="color: #1e40af; font-size: 9.3pt;">3. GÜÇ / STATÜ / DEĞER GÖRME</strong><br>
        <small style="color: #475569;">Önemli hissetme, takdir edilme ve söz hakkı bulma.</small>
    </div>
    <div class="pyramid-tier middle" style="background: #f0fdf4; border-color: #16a34a; width: 90%;">
        <strong style="color: #166534; font-size: 9.3pt;">2. SEVGİ VE AİT OLMA İHTİYACI</strong><br>
        <small style="color: #475569;">Gruba dahil olma, kabul görme ve ilişki kurma.</small>
    </div>
    <div class="pyramid-tier base" style="background: #fffbeb; border-color: #d97706; width: 100%;">
        <strong style="color: #b45309; font-size: 9.3pt;">1. HAYATTA KALMA (FİZYOLOJİK GÜVENLİK)</strong><br>
        <small style="color: #475569;">Beslenme, uyku, fiziksel emniyet ve biyolojik ihtiyaçlar.</small>
    </div>
</div>

> ⚠️ **Glasser Püf Noktası:** Glasser'e göre istenmeyen öğrenci davranışları "kötü niyetten" değil; bu 5 temel ihtiyaçtan birinin sınıfta doyurulamamasından kaynaklanır. Sınıfta aidiyet, güç ve eğlence bulamayan çocuk kural yıkar (*Başarısızlık Olmayan Okul* ilkesi).

### D. Rudolf Dreikurs — Sosyal Disiplin: Ceza vs. Mantıksal Sonuç

<div class="doctrine-compare-wrap">
    <div class="cycle-banner">
        <span>⚖️ DREIKURS: CEZA vs MANTIKSAL SONUÇ ARASINDAKİ DERİN AYRIM</span>
    </div>
    <div class="entity-grid-2">
        <div class="dok-card" style="border-left: 4px solid #dc2626;">
            <strong style="color: #dc2626; font-size: 10pt;">CEZA (Keyfî &amp; İntikamcı)</strong>
            <p style="font-size: 8.6pt; line-height: 1.4; color: #475569; margin-top: 4px;">
                • Davranışla hiçbir mantıksal bağı yoktur (sırayı karalayana teneffüse çıkmama cezası vermek).<br>
                • Öğretmenin öfkesini ve otorite kibrini yansıtır.<br>
                • Öğrencide öfke, intikam, haksızlık ve kurnazlık duygusu üretir.<br>
                • Davranışın sorumluluğunu öğretmez.
            </p>
        </div>
        <div class="dok-card" style="border-left: 4px solid #16a34a;">
            <strong style="color: #16a34a; font-size: 10pt;">MANTIKSAL SONUÇ (Onarıcı &amp; İlgili)</strong>
            <p style="font-size: 8.6pt; line-height: 1.4; color: #475569; margin-top: 4px;">
                • Davranışla doğrudan ve mantıksal olarak bağlantılıdır (sırayı karalayanın sırayı silip temizlemesi).<br>
                • Sakin, nesnel ve önceden bilinen bir kural sonucudur.<br>
                • Öğrencide telafi, adalet ve <strong>öz-disiplin</strong> bilinci uyandırır.<br>
                • Sosyal normları onarır.
            </p>
        </div>
    </div>
</div>

---

# ÜNİTE 2: ÖZ FARKINDALIK, İLETİŞİM VE AKTİF ÖĞRETİM TEKNİKLERİ 1–5 (2. HAFTA / 1. GRUP)

## 2.1. Mesleki Stratejiler (Strateji 1–5)

### Strateji 1: Kendini Tanımak (Öz Farkındalık ve Kişisel SWOT Analizi)

<div class="axis-matrix-2x2">
    <div class="axis-banner">
        <span>📊 ÖĞRETMENİN MESLEKİ SWOT ANALİZİ EKSEN MATRİSİ</span>
    </div>
    <div class="axis-grid">
        <div class="axis-cell highlight">
            <span class="axis-cell-badge">İÇSEL · OLUMLU</span>
            <div class="axis-cell-title">GÜÇLÜ YÖNLER (Strengths - S)</div>
            <div class="axis-cell-desc">Zengin alan bilgisi, güçlü diksiyon ve hitabet, yüksek empati, gelişmiş teknoloji hâkimiyeti, sabır ve güleryüz.</div>
        </div>
        <div class="axis-cell" style="border-left: 3.5px solid #dc2626; background: #fffaf0;">
            <span class="axis-cell-badge" style="background: #dc2626;">İÇSEL · OLUMSUZ</span>
            <div class="axis-cell-title" style="color: #991b1b;">ZAYIF YÖNLER (Weaknesses - W)</div>
            <div class="axis-cell-desc">Gürültüye çabuk öfkelenme/parlama, zamanı yetiştirememe (sarkma), çekingen öğrencileri fark edememe, evrak yorgunluğu.</div>
        </div>
        <div class="axis-cell" style="border-left: 3.5px solid #0284c7; background: #f0f9ff;">
            <span class="axis-cell-badge" style="background: #0284c7;">DIŞSAL · FIRSAT</span>
            <div class="axis-cell-title" style="color: #0369a1;">FIRSATLAR (Opportunities - O)</div>
            <div class="axis-cell-desc">Destekleyici okul idaresi ve zümre dayanışması, zengin kütüphane, akıllı tahta donanımı, hizmet içi pedagojik seminerler.</div>
        </div>
        <div class="axis-cell" style="border-left: 3.5px solid #ea580c; background: #fff7ed;">
            <span class="axis-cell-badge" style="background: #ea580c;">DIŞSAL · TEHDİT</span>
            <div class="axis-cell-title" style="color: #c2410c;">TEHDİTLER (Threats - T)</div>
            <div class="axis-cell-desc">Kalabalık sınıf mevcudu (40+), aşırı müdahaleci veya ilgisiz veli profili, çevresel dikkat dağıtıcılar, ağır bürokratik yük.</div>
        </div>
    </div>
</div>

* **Kavramsal Öz:** Yunus Emre'nin *"İlim ilim bilmektir, ilim kendin bilmektir"* ilkesinden hareketle; sınıf yönetiminin başlangıç noktası öğretmenin kendi sabır sınırlarını, zaaflarını ve öfke tetikleyicilerini tanımasıdır (==Öz farkındalık==).
* **Sınav Uygulaması:** Gürültü karşısında çabuk öfkelendiğini (W) bilen bir öğretmen, gürültü anında sınıfa bağırmak yerine önceden sessizlik işareti, fısıltı tekniği veya ritim uyarısı planlayarak krizleri önler.

### Strateji 2: Hedef Kitle Analizi: Öğrencilerini Tanımak
* **Kavramsal Öz:** Öğrencisini tanımadan derse giren öğretmen, karanlıkta hedefi görmeden ok atan avcıya benzer (Şahin, 2015). Öğrenci üç temel boyutta tanınır:
  1. **Bilişsel Boyut:** Hazırbulunuşluk, soyut düşünme seviyesi, dikkat süresi ve çoklu zekâ alanları (Gardner).
  2. **Duyuşsal Boyut:** Derse karşı önyargı, kaygı, özgüven, ilgi ve motivasyon kaynakları.
  3. **Sosyokültürel Boyut:** Aile tutumu (demokratik/baskıcı), ekonomik düzey, göç/boşanma gibi travmalar.
* **Tanıma Araçları:** Doğal gözlem (teneffüs ve oyun rolleri), tanıma formları, rehberlik servisiyle koordinasyon ve ==BEP== (Bireyselleştirilmiş Eğitim Programı).

### Strateji 3: Ajanda Oluşturmak (Mesleki Hafıza ve Pusula)
* *"Söz uçar, yazı kalır."* Yüzlerce öğrenciyle çalışan öğretmenin hafızasına güvenmesi yetmez. Ajandada yer alan **5 temel kayıt**:
  1. Haftalık kazanım, sınav ve telafi planı.
  2. Öğrenci gelişim ve gözlem notları.
  3. Özel durum kayıtları (astım, alerji, ailevi travma).
  4. Veli görüşme kayıtları ve verilen taahhütler.
  5. Anlık etkinlik fikirleri ve dersten çıkarılan pedagojik dersler.

### Strateji 4: İyi Bir Diksiyon ve Hitabet
* **Ses Tonunun Önemi:** Monoton bir ses tonu uykuyu, aşırı yüksek ses gerginliği tetikler. Vurgu, tonlama, nefes kontrolü ve göz teması disiplin sorunlarını başlamadan çözer.

### Strateji 5: Aktif Dinleme (Empatik Dinleme ve Açımlama)

<div class="cycle-flow-wrap">
    <div class="cycle-banner">
        <span>👂 AKTİF DİNLENME VE AÇIMLAMA (PARAPHRASING) DÖNGÜSÜ</span>
    </div>
    <div class="cycle-steps">
        <div class="cycle-step"><span class="cycle-step-num">1</span><span class="cycle-step-title">Fiziksel Yönel</span><span class="cycle-step-desc">Göz hizasına in</span></div>
        <div class="cycle-arrow">➔</div>
        <div class="cycle-step"><span class="cycle-step-num">2</span><span class="cycle-step-title">Yargısız Dinle</span><span class="cycle-step-desc">Sözünü kesme</span></div>
        <div class="cycle-arrow">➔</div>
        <div class="cycle-step"><span class="cycle-step-num">3</span><span class="cycle-step-title">İhtiyacı Teşhis Et</span><span class="cycle-step-desc">Duyguyu sez</span></div>
        <div class="cycle-arrow">➔</div>
        <div class="cycle-step"><span class="cycle-step-num">4</span><span class="cycle-step-title">Açımlama Yap</span><span class="cycle-step-desc">Kendi cümlenle özetle</span></div>
        <div class="cycle-arrow">➔</div>
        <div class="cycle-step" style="border-left: 3.5px solid #16a34a;"><span class="cycle-step-num">5</span><span class="cycle-step-title">Teyit Al</span><span class="cycle-step-desc">"Doğru mu anladım?"</span></div>
    </div>
</div>

* **Açımlama (Paraphrasing):** Öğrencinin söylediğini anlamını değiştirmeden kendi cümlelerimizle özetleyip ona geri yansıtmaktır (*Örnek:* *"Herkes testi bitirdi, ben yapamadım"* diyen öğrenciye *"Arkadaşlarının gerisinde kaldığını düşündüğün için şu an kaygılı hissediyorsun, doğru mu?"* diyerek ayna tutmak).

---

## 2.2. Aktif Öğretim Teknikleri (Etkinlik 1–5)
1. **Etkinlik 1 — 5N 1K Tekniği:** Olayı *Ne, Neden, Nasıl, Nerede, Ne Zaman, Kim* sorularıyla analiz etme tekniğidir. Tahta 6 sütuna bölünür, gruplar parçaları birleştirir.
2. **Etkinlik 2 — A'dan Z'ye Tekniği:** Alfabenin 29 harfiyle işlenen üniteye dair birer kavram bulma; ders başında ön bilgiyi yoklama, ders sonunda hızlı tekrar için uygulanır.
3. **Etkinlik 3 — Adam Asmaca (Pedagojik Dönüşüm):** Şiddet/intihar çağrışımlı darağacı yerine **eriyen kardan adam, yaprak döken ağaç veya roket** görseli kullanılır.
4. **Etkinlik 4 — Akıl / Zihin Haritası (Tony Buzan):** Beynin iki lobunu çalıştıran **radyant (merkezden dışa yayılan) düşünme** tekniğidir. Merkezde renkli imge, merkezden kalın ana dallar, ince alt dallar ve tek anahtar kelimeler kullanılır.
5. **Etkinlik 5 — Akvaryum Tekniği (Fishbowl):** İç çember (4–5 kişi) tartışır; dış çember gözlemleyip not alır. Boş bırakılan **Sıcak Sandalye**ye dışarıdan söz almak isteyen oturup katkı verir ve yerine döner.

---

## 2.3. Vaka, Kitap ve Film Analizi (1. Grup)
* **Kitap — Doğan Cüceloğlu, *Öğretmenim Bir Bakar Mısın?*:**

<div class="doctrine-compare-wrap">
    <div class="cycle-banner">
        <span>📖 DOĞAN CÜCELOĞLU: CAN CANA VAROLUŞ VE TANIKLIK</span>
    </div>
    <div class="entity-grid-2">
        <div class="dok-card" style="border-left: 4px solid #dc2626;">
            <strong style="color: #dc2626;">KALIPLAYAN ÖĞRETMEN</strong>
            <p style="font-size: 8.5pt; line-height: 1.4; color: #475569; margin-top: 4px;">
                Öğrenciyi kendi zihnindeki tek tip şablona girmeye zorlar; farklılıkları hata, itirazları isyan sayar. Korku ve dış denetim iklimi üretir.
            </p>
        </div>
        <div class="dok-card" style="border-left: 4px solid #16a34a;">
            <strong style="color: #16a34a;">GELİŞTİREN ÖĞRETMEN</strong>
            <p style="font-size: 8.5pt; line-height: 1.4; color: #475569; margin-top: 4px;">
                Kendi çocukluk yaralarının farkındadır; öğrenciyi koşulsuz kabul eder, yeteneğine alan açar ve onun potansiyeline tanıklık eder.
            </p>
        </div>
    </div>
</div>

* **Film — *Dead Poets Society (Ölü Ozanlar Derneği, 1989)* (Robin Williams – John Keating):** Welton Akademisi'nin baskıcı kalıplarına karşı Keating sıraların üstüne çıkarak bakış açısı değiştirmeyi (Carpe Diem) öğretir; empatik dinlemesi ve coşkulu hitabetiyle öğrencilerin kendi özgün seslerini bulmalarını sağlar.

---

# ÜNİTE 3: GERİBİLDİRİM, PLANLAMA, HAZIRLIK VE DÜŞÜNME BECERİLERİ 6–10 (3. HAFTA / 2. GRUP)

## 3.1. Mesleki Stratejiler (Strateji 6–10)

### Strateji 6: Geribildirim (Feedback vs. Feedforward)

<div class="doctrine-compare-wrap">
    <div class="cycle-banner">
        <span>🔄 GERİ BİLDİRİM (FEEDBACK) vs İLERİ BİLDİRİM (FEEDFORWARD)</span>
    </div>
    <div class="entity-grid-2">
        <div class="dok-card" style="border-left: 4px solid #d97706;">
            <strong style="color: #d97706; font-size: 9.8pt;">GERİ BİLDİRİM (FEEDBACK - Geçmiş Odaklı)</strong>
            <p style="font-size: 8.5pt; line-height: 1.4; color: #475569; margin-top: 4px;">
                Öğrencinin geçmişte yaptığı eyleme, performansa veya hataya ayna tutar. Hatayı tespit eder (<em>"Bu soruda formülü yanlış uyguladın"</em>).
            </p>
        </div>
        <div class="dok-card" style="border-left: 4px solid #16a34a;">
            <strong style="color: #16a34a; font-size: 9.8pt;">İLERİ BİLDİRİM (FEEDFORWARD - Gelecek Odaklı)</strong>
            <p style="font-size: 8.5pt; line-height: 1.4; color: #475569; margin-top: 4px;">
                Sadece hatayı söylemekle kalmaz; bir sonraki sefere daha iyi nasıl yapılacağını yol gösterici şekilde inşa eder (<em>"Gelecek sefere önce değişkenleri listelersen hata yapmazsın"</em>).
            </p>
        </div>
    </div>
</div>

### Strateji 7: Derse Hazırlıklı Girmek ve Planlama
* Plansız derse giren öğretmen rotasız gemiye benzer. Alternatif plan (B Planı) bulundurmak teknik arıza veya erken bitme anında sınıf kontrolünün kaybedilmesini önler.

### Strateji 8: Farklı Düşünme Becerileri (Edward de Bono — Altı Şapkalı Düşünme)

<div class="doctrine-compare-wrap">
    <div class="cycle-banner">
        <span>🎩 DE BONO: 6 ŞAPKALI DÜŞÜNME VE PEDAGOJİK RENK KODLARI</span>
    </div>
    <div class="entity-grid-3">
        <div class="dok-card" style="border-top: 3.5px solid #64748b;">
            <strong style="color: #475569;">⚪ BEYAZ ŞAPKA</strong>
            <p style="font-size: 8.3pt; color: #334155; margin-top: 3px;"><strong>Tarafsız &amp; Nesnel:</strong> Rakamlar, istatistikler, somut veriler ve kanıtlanmış gerçekler.</p>
        </div>
        <div class="dok-card" style="border-top: 3.5px solid #dc2626;">
            <strong style="color: #dc2626;">🔴 KIRMIZI ŞAPKA</strong>
            <p style="font-size: 8.3pt; color: #334155; margin-top: 3px;"><strong>Duygusal &amp; Sezgisel:</strong> Mantıksal gerekçe sunmadan içgüdüleri ve hisleri ifade etme.</p>
        </div>
        <div class="dok-card" style="border-top: 3.5px solid #1e293b;">
            <strong style="color: #0f172a;">⚫ SİYAH ŞAPKA</strong>
            <p style="font-size: 8.3pt; color: #334155; margin-top: 3px;"><strong>Kötümser &amp; Tedbirli:</strong> Riskler, tehlikeler, zayıf noktalar ve hukuki/etik engeller.</p>
        </div>
    </div>
    <div class="entity-grid-3" style="border-top: 1px solid #e2e8f0;">
        <div class="dok-card" style="border-top: 3.5px solid #eab308;">
            <strong style="color: #ca8a04;">🟡 SARI ŞAPKA</strong>
            <p style="font-size: 8.3pt; color: #334155; margin-top: 3px;"><strong>İyimser &amp; Umutlu:</strong> Fırsatlar, avantajlar, faydalar ve pozitif katma değerler.</p>
        </div>
        <div class="dok-card" style="border-top: 3.5px solid #16a34a;">
            <strong style="color: #16a34a;">🟢 YEŞİL ŞAPKA</strong>
            <p style="font-size: 8.3pt; color: #334155; margin-top: 3px;"><strong>Yaratıcı &amp; Yenilikçi:</strong> Yeni fikirler, alternatif yollar ve yanal (lateral) düşünme.</p>
        </div>
        <div class="dok-card" style="border-top: 3.5px solid #2563eb;">
            <strong style="color: #2563eb;">🔵 MAVİ ŞAPKA</strong>
            <p style="font-size: 8.3pt; color: #334155; margin-top: 3px;"><strong>Üstbilişsel &amp; Yönetici:</strong> Süreci yönetme, şapkaları sıraya koyma ve son kararı özetleme.</p>
        </div>
    </div>
</div>

### Strateji 9: Öğrenciye Destek Olma (Koşulsuz Kabul)
* Başarısız veya sorunlu öğrenciyi dışlamak direnç üretir; rehberlik ve şefkat temelli destek aidiyet oluşturur.

### Strateji 10: Düşünme Becerileri (Eleştirel, Yaratıcı, Üstbiliş)
* ==Eleştirel Düşünme== (kanıt arama, sorgulama), ==Yaratıcı Düşünme== (özgün ürün çıkarma) ve ==Üstbiliş / Metacognition== (öğrencinin kendi düşünme ve öğrenme sürecini denetleyip yönetmesi).

---

## 3.2. Aktif Öğretim Teknikleri (Etkinlik 6–10)
6. **Etkinlik 6 — Altı Şapkalı Düşünme:** Karar süreçlerinde konunun 6 farklı boyuttan sistematik tahlili.
7. **Etkinlik 7 — Arkası Yarın (Zeigarnik Etkisi):** Olay veya metnin en heyecanlı yerinde kesilerek öğrencilere *"Sizce ne oldu / ne olmalı?"* diye sorulmasıdır. Rus psikolog Bluma Zeigarnik'in kanıtladığı gibi; **tamamlanmamış işler zihinde daha canlı ve merakla hatırlanır**.
8. **Etkinlik 8 — Atasözü ve Deyimlerle Öğretim:** Kültürel kodlarla soyut kavramların somutlaştırılması.
9. **Etkinlik 9 — Balık Kılçığı (Ishikawa — Neden-Sonuç Şeması):** Karmaşık bir problemin kök nedenlerini kategorik ayrıştırma tekniğidir. Balığın başı **problem**, ana kılçıklar **kategoriler** (insan, yöntem, çevre, malzeme), alt kılçıklar **alt nedenler**dir.
10. **Etkinlik 10 — Kartopu Tekniği:** Önce bireysel düşünme (1) $\rightarrow$ eşle birleşme (2) $\rightarrow$ 4 kişilik grup $\rightarrow$ 8 kişilik grup $\rightarrow$ tüm sınıfça ortak fikrin sunumu (1-2-4-8 geometrik büyüme).

---

## 3.3. Vaka, Kitap ve Film Analizi (2. Grup)
* **Kitap — Doğan Cüceloğlu, *Öğretmen Olmak*:** Hizmetli İrfan Bey'in hürmetkâr, sevgi dolu ve adanmış yaklaşımı; mesleğini sadece teknik memuriyet gören Şevket Bey'in mekanik katılığını dönüştürür.
* **Film — *Taare Zameen Par (Her Çocuk Özeldir, 2007)* (Aamir Khan – Nikumbh):** Okuma-yazma güçlüğü çeken 8 yaşındaki İshaan'ın disleksi olduğunu fark eden Nikumbh Hoca; ceza ve etiketleme yerine kum havuzunda harf çizdirerek, plastilinle modelleterek ve resim yeteneğini keşfederek çocuğu hayata kazandırır.

---

# ÜNİTE 4: SINIF İKLÎMİ, KURALLAR, MAHREMİYET VE PEKİŞTİRME TEKNİKLERİ 11–15 (4. HAFTA / 3. GRUP)

## 4.1. Mesleki Stratejiler (Strateji 11–15)

### Strateji 11: Sınıf Kuralları Oluşturma Metodolojisi

<div class="cycle-flow-wrap">
    <div class="cycle-banner">
        <span>📜 DEMOKRATİK SINIF KURALI İNŞA ETMENİN 4 AŞAMALI SÜRECİ</span>
    </div>
    <div class="cycle-steps">
        <div class="cycle-step"><span class="cycle-step-num">1</span><span class="cycle-step-title">Bireysel Liste</span><span class="cycle-step-desc">Öğrenci kural önerir</span></div>
        <div class="cycle-arrow">➔</div>
        <div class="cycle-step"><span class="cycle-step-num">2</span><span class="cycle-step-title">Beyin Fırtınası</span><span class="cycle-step-desc">Gerekçeleri tartış</span></div>
        <div class="cycle-arrow">➔</div>
        <div class="cycle-step"><span class="cycle-step-num">3</span><span class="cycle-step-title">Sınıfça Oylama</span><span class="cycle-step-desc">Ortak uzlaşma sağla</span></div>
        <div class="cycle-arrow">➔</div>
        <div class="cycle-step" style="border-left: 3.5px solid #16a34a;"><span class="cycle-step-num">4</span><span class="cycle-step-title">İlan &amp; Taahhüt</span><span class="cycle-step-desc">Panoya as ve imzala</span></div>
    </div>
</div>

* **Kural Yazım İlkeleri:** Kurallar yasaklayıcı/olumsuz değil (örn. *"Koşma!"* yerine); **olumlu, eylemsel ve 1. çoğul şahısla** yazılmalıdır (*"Koridorda yürürüz", "Söz alarak konuşuruz"*). Kural sayısı 5–7'yi geçmemelidir.
* **Kural ile Rutin Ayrımı:** ==Kural== genel ahlak ve davranış standardıdır; ==Rutin== ise derse giriş, ödev toplama, tahta silme gibi tekrarlanan işlerin standart yapılış usulüdür.

### Strateji 12: Sınıfı Ev / Aile Ortamına Yaklaştırma (Psikolojik Güvenlik)
* Soğuk ve kışla havasındaki sınıfta öğrenme kilitlenir; hata yapmaktan korkulmayan, alay edilme riski olmayan **psikolojik güvenlik iklimi** başarıyı getirir.

### Strateji 13: Öğretimi Okul Dışına Taşıma (Tersyüz Sınıf / Flipped Classroom)
* Teorik bilginin evde video/dijital materyalle öğrenildiği, sınıf ortamının ise tartışma, problem çözme ve uygulamaya ayrıldığı modern modeldir.

### Strateji 14: Sürekli Nasihat Yerine Örnek Olmak (Hâl Dili vs. Kâl Dili)
* Öğrenciler söylenen sözden ziyade (==kâl dili==), öğretmenin sergilediği ahlakı, adaleti ve tutumu (==hâl dili==) model alırlar.

### Strateji 15: Olumlu Davranışları Pekiştirmek (Pekiştirme ve Ceza Matrisi)

<div class="axis-matrix-2x2">
    <div class="axis-banner">
        <span>⚡ SKINNER EDİMSEL KOŞULLANMA: PEKİŞTİRME VE CEZA MATRİSİ</span>
    </div>
    <div class="axis-grid">
        <div class="axis-cell highlight">
            <span class="axis-cell-badge">UYARICI EKLEME (+)</span>
            <div class="axis-cell-title">I. OLUMLU PEKİŞTİRME</div>
            <div class="axis-cell-desc">Ortama istenen hoş bir uyarıcı eklenir (Aferin, yıldız, tebrik, yüksek sözlü notu). Davranışın sıklığı <strong>artar</strong>.</div>
        </div>
        <div class="axis-cell" style="border-left: 3.5px solid #16a34a; background: #f0fdf4;">
            <span class="axis-cell-badge" style="background: #16a34a;">UYARICI ÇIKARMA (-)</span>
            <div class="axis-cell-title" style="color: #166534;">II. OLUMSUZ PEKİŞTİRME</div>
            <div class="axis-cell-desc">Ortamdan rahatsız edici itici uyarıcı çıkarılır (Kaygıyı giderme, fazla ödevi iptal etme). Davranışın sıklığı <strong>artar</strong>.</div>
        </div>
        <div class="axis-cell" style="border-left: 3.5px solid #dc2626; background: #fef2f2;">
            <span class="axis-cell-badge" style="background: #dc2626;">İTİCİ UYARICI VERME</span>
            <div class="axis-cell-title" style="color: #991b1b;">III. I. TİP CEZA</div>
            <div class="axis-cell-desc">Ortama hoşa gitmeyen ceza eklenir (Azarlama, rencide etme, ek ceza ödevi). Davranışı geçici bastırır, korku üretir.</div>
        </div>
        <div class="axis-cell" style="border-left: 3.5px solid #ea580c; background: #fff7ed;">
            <span class="axis-cell-badge" style="background: #ea580c;">HOŞ UYARICIYI ALMA</span>
            <div class="axis-cell-title" style="color: #c2410c;">IV. II. TİP CEZA (Mahrumiyet)</div>
            <div class="axis-cell-desc">Öğrencinin sevdiği hoş bir şey elinden alınır (Teneffüse çıkarmama, sevdiği oyundan mahrum etme).</div>
        </div>
    </div>
</div>

---

## 4.2. Aktif Öğretim Teknikleri (Etkinlik 11–15)
11. **Etkinlik 11 — Ben Kimim? Tekniği:** Öğrencinin sırtına veya alnına yapıştırılan kavramı/şahsiyeti genelden özele sorularla (*"Tarihi bir şahsiyet miyim?", "Savaşta mı bulundum?"*) tahmin etme tekniğidir.
12. **Etkinlik 12 — Beyin Fırtınası (Alex Osborn):** Kısa sürede çok sayıda fikir üretme tekniğidir. **Temel Kural:** İlk aşamada fikirler asla eleştirilemez, yargılanamaz; miktar esastır, sınıflandırma sonra yapılır.
13. **Etkinlik 13 — Bölünmüş Metinler Tekniği:** Uzun metnin parçalara bölünerek uzman gruplarca incelenmesi ve birleştirilmesidir (Jigsaw mantığı).
14. **Etkinlik 14 — Burada Herkes Öğretmen:** Her öğrenci bir soru ve arkasına cevabını yazar; kâğıtlar toplanıp rastgele dağıtılır ve herkes sırayla öğretmen rolüne girerek soruyu sorar ve tartışmayı yönetir.
15. **Etkinlik 15 — Bunu Kim Yapar? Etkinliği:** Öğrenciler ellerindeki 8–10 soruluk kağıtla sınıfta dolaşır; **her arkadaşına yalnızca TEK BİR SORU çözdürür ve imzalattırır**. Akran etkileşimini ve sosyalleşmeyi maksimize eder.

---

## 4.3. Vaka, Kitap ve Film Analizi (3. Grup)
* **Kitap — Thomas Gordon, *Etkili Öğretmenlik Eğitimi (T.E.T.)*:** İletişim engelleri (emir, ahlak dersi, nutuk, alay) yerine Sorunun Mülkiyeti ilkesiyle yaklaşma; sorun öğrencideyse ==Aktif Dinleme==, öğretmendeyse ==Ben Dili==, çatışmada ==No-Lose III. Yol==.
* **Film — *Beyond the Blackboard (Tahtanın Ötesinde, 2011)* (Emily VanCamp – Stacey Bess):** Evsiz ve yoksul çocukların sığındığı barınak okulunda (School with No Name) Stacey Öğretmen; virane odayı boyar, piyano getirir, velileri sürece katar ve çocuklara aile şefkati vererek sınıf ikliminin mucizeler yaratacağını kanıtlar.

---

# ÜNİTE 5: SOSYAL SORUMLULUK, SORUN ÇÖZME, MİZAH, HAYAL VE ZAMAN YÖNETİMİ 16–20 (5. HAFTA / 4. GRUP)

## 5.1. Mesleki Stratejiler (Strateji 16–20)

### Strateji 16: Sosyal Sorumluluk ve Yardımlaşma (Diğerkâmlık)
* Başkalarının derdiyle dertlenme (==diğerkâmlık / özgecilik==) bilinci; huzurevi ziyareti, kütüphane kurma ve kardeş okul projeleriyle kazandırılır.

### Strateji 17: Karşılaşılan Sorunlara Çözüm Odaklı Yaklaşmak (Örtük Müfredat)
* Öğretmenin kriz anındaki sakinliği, problem çözme becerisi resmi müfredatta yazmayan ama kalıcı öğrenilen ==örtük müfredat==tır.

### Strateji 18: Mizahı Sınıf Yönetiminde Kullanmak
* Alaycı veya kırıcı olmayan pedagojik mizah; kaygıyı düşürür, dikkati toplar ve beyinde dopamin salgılatarak öğrenmeyi pekiştirir.

### Strateji 19: Hayal Kurmak ve Kurdurmak (Zihinsel Canlandırma)
* **Murphy (1997) Golf Deneyi:** Vuruştan önce topun hedefe girdiğini zihninde canlandıran (hayal eden) sporcuların performansı **%30 artmıştır**. Zihinde canlandırma eylemi ateşleyen muharrik güçtür.

### Strateji 20: Zaman Yönetimi (Stephen Covey Matrisi)

<div class="axis-matrix-2x2">
    <div class="axis-banner">
        <span>⏳ STEPHEN COVEY: ZAMAN YÖNETİMİ ÖNCELİK EKSEN MATRİSİ</span>
    </div>
    <div class="axis-grid">
        <div class="axis-cell" style="border-left: 3.5px solid #dc2626; background: #fff5f5;">
            <span class="axis-cell-badge" style="background: #dc2626;">I. ÇEYREK</span>
            <div class="axis-cell-title" style="color: #991b1b;">ÖNEMLİ VE ACİL (Krizler)</div>
            <div class="axis-cell-desc">Yangın söndürme, patlak veren krizler, son gün teslim baskısı. Sürekli bu çeyrekte yaşamak tükenmişlik üretir.</div>
        </div>
        <div class="axis-cell highlight">
            <span class="axis-cell-badge">II. ÇEYREK · HEDEF SAHA</span>
            <div class="axis-cell-title">ÖNEMLİ AMA ACİL DEĞİL (Lider Öğretmen)</div>
            <div class="axis-cell-desc"><strong>Proaktif Alan:</strong> Ders planlama, önleyici tedbirler, pedagojik gelişim, materyal hazırlığı ve ilişki inşası.</div>
        </div>
        <div class="axis-cell" style="border-left: 3.5px solid #ea580c; background: #fff7ed;">
            <span class="axis-cell-badge" style="background: #ea580c;">III. ÇEYREK</span>
            <div class="axis-cell-title" style="color: #c2410c;">ÖNEMSİZ AMA ACİL (Aldatıcı)</div>
            <div class="axis-cell-desc">Araya giren gereksiz telefonlar, aniden gelen ziyaretçiler, başkalarının acil işleri; acil görünür ama verimsizdir.</div>
        </div>
        <div class="axis-cell" style="border-left: 3.5px solid #64748b; background: #f8fafc;">
            <span class="axis-cell-badge" style="background: #64748b;">IV. ÇEYREK</span>
            <div class="axis-cell-title" style="color: #475569;">ÖNEMSİZ VE ACİL DEĞİL (Tuzak)</div>
            <div class="axis-cell-desc">Sosyal medyada kaybolma, dedikodu, amaçsız sohbetler ve zaman israfı; tamamen kaçınılması gereken sahadır.</div>
        </div>
    </div>
</div>

* **Zaman Hırsızları (Döş & Uysal):** Derse geç girme, yoklamayla vakit kaybetme, tahta silme ve disiplinsiz bölünmeler akademik öğrenme süresini eriten temel hırsızlardır.

---

## 5.2. Aktif Öğretim Teknikleri (Etkinlik 16–20)
16. **Etkinlik 16 — Canlandırma (Drama & Rol Oynama):** Öğrencinin bir durumu bedensel ve duygusal olarak canlandırarak empati kurmasıdır.
17. **Etkinlik 17 — Cümle Tamamlama:** *"Eğer ben öğretmen olsaydım..."* gibi açık uçlu köklerle öğrencinin iç dünyasını ve tutumlarını ortaya çıkarma tekniğidir.
18. **Etkinlik 18 — Değerlendirme Kartları / Çıkış Bileti:** Dersin son 5 dakikasında öğrencinin kâğıda *"Bugün ne öğrendim?", "Nerede zorlandım?"* yazıp kapıdan çıkarken teslim ettiği biçimlendirici değerlendirme tekniğidir.
19. **Etkinlik 19 — Düşün-Eşleş-Paylaş (Frank Lyman):** Önce bireysel düşünme (1–2 dk) $\rightarrow$ yanındaki eşle fikirleri tartışıp olgunlaştırma $\rightarrow$ sınıf geneline sunma. Çekingen öğrencilerin katılımını garanti eder.
20. **Etkinlik 20 — Eğitsel Oyunlar:** Kurallı yarışma ve oyunlarla bilginin pekiştirilmesidir.

---

## 5.3. Vaka, Kitap ve Film Analizi (4. Grup)
* **Kitap — Stephen R. Covey, *Etkili İnsanların 7 Alışkanlığı*:**
  1. *Proaktif Ol* (Reaktif mazeretler yerine etki alanına odaklan).
  2. *Sonunu Düşünerek İşe Başla* (Dersin hedefini baştan netleştir).
  3. *Önemli İşlere Öncelik Ver* (II. Çeyrekte yaşa).
  4. *Kazan-Kazan Düşün* (Gordon'un No-Lose mantığı).
* **Film — *The Ron Clark Story (Zafer Benimdir, 2006)* (Matthew Perry – Ron Clark):** Harlem'in en sorunlu sınıfını alan Clark; kuralları rap şarkısıyla öğretir, süt içme iddialarıyla dikkat çeker ve sınıfa bir aile olduğunu hissettirerek eyalet sınavında birinci çıkarır.

---

# ÜNİTE 6: MOTİVASYON, ÖĞRENMEYİ ÖĞRETMEK, LİDERLİK, ENTELEKTÜEL ÖĞRETMEN VE ÖĞRETMENLER ODASI 21–25 (6. HAFTA / 5. GRUP)

## 6.1. Mesleki Stratejiler (Strateji 21–25)

### Strateji 21: Öğrenci Motivasyonunu Artırmak
* **İçsel vs. Dışsal Motivasyon:** Not, ödül ve ceza ==dışsal motivasyon==dur; geçicidir. Merak, özerklik, keşif ve başarma hazzı ise ==içsel motivasyon==dur ve kalıcı başarıyı getirir.

### Strateji 22: Öğrenmeyi Öğretmek ve VARK Öğrenme Stilleri

<div class="spectrum-bar">
    <div class="spectrum-item" style="flex: 65; background: #1F4775;">%65 GÖRSEL (Şema, Resim, Renk, Harita)</div>
    <div class="spectrum-item" style="flex: 30; background: #d97706;">%30 İŞİTSEL (Anlatım, Tartışma)</div>
    <div class="spectrum-item" style="flex: 5; background: #dc2626;">%5 KİNESTETİK</div>
</div>

* **VARK Dağılımı (Neil Fleming):** Sınıfın **%65'i Görsel**, **%30'u İşitsel**, **%5'i Kinestetik / Dokunsal** öğrenir. Sadece kürsüden konuşan öğretmen sınıfın %70'ini kaybeder.
* **Bilişsel Öğrenme Stratejileri:**
  * ==Yineleme==: Altını çizme, sesli okuma, aynen yazma (en yüzeysel).
  * ==Anlamlandırma==: Eski bilgiyle bağ kurma, analoji yapma, kendi cümlesiyle özetleme.
  * ==Örgütleme==: Zihin haritası, tablo, balık kılçığı ve şemaya dökme (en kalıcı).

### Strateji 23: Sınıf Yönetimi Becerilerini Sürekli Geliştirmek
* Mesleki kıdem tek başına ustalık getirmez; pedagojik yayınları okumak, zümre gözlemleri ve özyansıtma esastır.

### Strateji 24: Entelektüel (Münevver) Bir Öğretmen Olmak (Nurettin Topçu)

<div class="doctrine-compare-wrap">
    <div class="cycle-banner">
        <span>📚 NURETTİN TOPÇU: TÜRKİYE'NİN MAARİF DAVASI</span>
    </div>
    <div class="entity-grid-2">
        <div class="dok-card" style="border-left: 4px solid #dc2626;">
            <strong style="color: #dc2626; font-size: 10pt;">MAAŞLI MEMUR &amp; TEKNİSYEN</strong>
            <p style="font-size: 8.5pt; line-height: 1.4; color: #475569; margin-top: 4px;">
                Dersi saatini doldurup maaşını alacağı bir angarya sayar. Bilgi tüccarıdır; öğrencinin ruhuna dokunmaz, zihinsel ezber yükler.
            </p>
        </div>
        <div class="dok-card" style="border-left: 4px solid #1F4775;">
            <strong style="color: #1F4775; font-size: 10pt;">MUALLİM (RUH SANATKÂRI &amp; MÜNEVVER)</strong>
            <p style="font-size: 8.5pt; line-height: 1.4; color: #475569; margin-top: 4px;">
                Bir milletin karakterini yoğuran idealist aydındır. Mektebi ibadethane ciddiyetinde bir irfan ocağı, öğretmenliği mukaddes bir dava bilir.
            </p>
        </div>
    </div>
</div>

### Strateji 25: Öğretmenler Odası ve Kolektif Bilinç

<div class="doctrine-compare-wrap">
    <div class="cycle-banner">
        <span>🧩 ÖĞRETMENLER ODASI KÜLTÜRÜ: SİNERJİ vs TÜKENMİŞLİK</span>
    </div>
    <div class="entity-grid-2">
        <div class="dok-card" style="border-left: 4px solid #16a34a;">
            <strong style="color: #166534; font-size: 10pt;">PUZZLE (YAPBOZ) METAFORU &amp; MEŞVERET</strong>
            <p style="font-size: 8.5pt; line-height: 1.4; color: #475569; margin-top: 4px;">
                Okuldaki her öğretmenin yeri bir yapboz parçası gibi eşsizdir; onun boşluğunu başkası dolduramaz. Öğretmenler odası dedikodu yeri değil, ortak çözüm aranan meşveret meclisidir.
            </p>
        </div>
        <div class="dok-card" style="border-left: 4px solid #dc2626;">
            <strong style="color: #991b1b; font-size: 10pt;">ÜMİTSİZLİK VİRÜSÜ (Mesleki Zehirlenme)</strong>
            <p style="font-size: 8.5pt; line-height: 1.4; color: #475569; margin-top: 4px;">
                Kıdemli öğretmenlerin <em>"Bu çocuklardan hiçbir şey olmaz"</em> diyerek genç meslektaşlarının şevkini kırması ve kolektif bilinci zehirlemesidir; derhal bertaraf edilmelidir.
            </p>
        </div>
    </div>
</div>

---

## 6.2. Aktif Öğretim Teknikleri (Etkinlik 21–25)
21. **Etkinlik 21 — Elma-Armut Etkinliği:** Öğretmenin okuduğu yargıya sınıf korosunun hep bir ağızdan **"Elma!" (Doğru)** veya **"Armut!" (Yanlış)** diyerek katıldığı eğlenceli ve hızlı toplu dönüt tekniğidir.
22. **Etkinlik 22 — Eşini Bul:** Ters kapatılmış kartlardan ilişkili kavram çiftlerini bulup eşleştirme ve açıklama oyunudur.
23. **Etkinlik 23 — Eşleştirme:** İki farklı sütundaki kavram ile tanımı/örneği oklarla bağlama.
24. **Etkinlik 24 — Farkı Bul:** Birbirine çok benzeyen iki durum, kavram veya resim arasındaki ince pedagojik farkları ayırt etme.
25. **Etkinlik 25 — Fırıldak / Çarkıfelek:** Üzerinde konular yazılı çarkın döndürülerek gelen soruya grubun cevap vermesi.

---

## 6.3. Vaka, Kitap ve Film Analizi (5. Grup)
* **Kitap — Nurettin Topçu, *Türkiye'nin Maarif Davası*:** Maarif davası mektep, muallim ve talebe sacayağı üzerinde yükselir. Muallim ruh mimarıdır.
* **Film — *Stand and Deliver (Kalk ve Diren, 1988)* (Edward James Olmos – Jaime Escalante):** Yoksul Hispanik öğrencilere zümrenin *"Bunlardan bir şey olmaz"* önyargısına karşı Escalante elma keserek kesirleri öğretir, ileri kalkülüs (AP Calculus) sınavını kazandırır ve öğrencilerine her engeli aşan **"Ganas" (İçsel istek, azim ve şevk)** ruhunu aşılar.

---

# ÜNİTE 7: İLERİ DÜZEY AKTİF ÖĞRETİM TEKNİKLERİ 26–30 (7. HAFTA)

## 7.1. İleri Düzey Aktif Öğretim Teknikleri ve Uygulama Protokolleri

26. **Etkinlik 26 — Fikir Tepsisi Etkinliği (Kitap s. 178):**  
   Farklı problem veya vaka sorularının yazılı olduğu kâğıtlar tepsi içinde sınıfta dolaştırılır. Her öğrenci tepsiden bir kâğıt çeker, kendi çözüm önerisini yazar ve kâğıdı yanındakine devreder. Sonraki öğrenci **önceki fikri okuyup üzerine yeni ve özgün bir fikir ekler**. Yazılı ve aşamalı kolektif fikir üretimidir.

27. **Etkinlik 27 — Flaş Kart Etkinliği (s. 178):**  
   Ön yüzünde **soru veya anahtar kavram**, arka yüzünde **kısa cevap veya şematik görsel** bulunan hızlı tekrar kartlarıdır. Eşler birbirini yoklar; doğru bilinen kartlar ayrılır, bilinmeyenler destenin arkasına konarak öğrenilene kadar çevrilir.

28. **Etkinlik 28 — Fotoğraf Etkinlikleri (s. 178–179):**  
   Görsel okuryazarlık, empati ve tahmin tekniğidir:

<div class="doctrine-compare-wrap">
    <div class="cycle-banner">
        <span>📸 FOTOĞRAF ETKİNLİĞİ: 3 FOTOĞRAF TÜRÜ VE 9 PEDAGOJİK İŞLEM</span>
    </div>
    <div class="entity-grid-3">
        <div class="dok-card" style="border-top: 3.5px solid #0284c7;">
            <strong style="color: #0284c7;">1. BETİMLEYİCİ FOTOĞRAFLAR</strong>
            <p style="font-size: 8.3pt; color: #475569; margin-top: 3px;">Tarihi bir olayı, doğa olayını veya fiziki mekânı nesnel olarak tasvir eden görseller.</p>
        </div>
        <div class="dok-card" style="border-top: 3.5px solid #dc2626;">
            <strong style="color: #dc2626;">2. YARGILAYICI FOTOĞRAFLAR</strong>
            <p style="font-size: 8.3pt; color: #475569; margin-top: 3px;">Ahlaki, sosyal, adalet veya vicdani çelişkilere temas eden, tartışma açan görseller.</p>
        </div>
        <div class="dok-card" style="border-top: 3.5px solid #16a34a;">
            <strong style="color: #16a34a;">3. ESTETİK FOTOĞRAFLAR</strong>
            <p style="font-size: 8.3pt; color: #475569; margin-top: 3px;">Sanatsal kompozisyon derinliği olan, duygu ve ilham uyandıran kareler.</p>
        </div>
    </div>
</div>

* **Fotoğraf Üzerinde Yapılan 9 Pedagojik İşlem:**  
  1. Karakterlerin psikolojik tahlili  
  2. Olayın öncesi ve sonrasını tahmin etme  
  3. Kadraj dışını hayal edip tamamlama  
  4. Özgün başlık koyma  
  5. Detaylara soru sorma  
  6. Görselden öykü/senaryo yazma  
  7. Fotoğrafı sınıfta dramatize etme  
  8. Karakterle empati kurma  
  9. Fotoğrafa şiir yazma

29. **Etkinlik 29 — Gazete Hazırlama Etkinliği (s. 179–180):**  
   Dönem veya ünite sonunda kazanımların grupça bir gazete mizanpajına dönüştürüldüğü proje tekniğidir. Görev dağılımıyla *Manşet/Başyazı, Röportaj, Bilim/Kültür, Mizah/Karikatür ve Bulmaca* sayfaları hazırlanır ve okul panosunda sergilenir.

30. **Etkinlik 30 — Grupla Hikâye Etkinliği (s. 180):**  
   4–5 kişilik gruplarda boş bir kâğıt elden ele döner. İlk öğrenci konuyla ilgili giriş cümlesini yazar; sonraki öğrenciler **önceki cümleleri okuyup akışa uygun birer cümle ekleyerek** 3–4 turda kolektif hikâyeyi tamamlar. En yaratıcı hikâye sınıfta alkışlanır.
"""

def main():
    content = get_content()
    
    # 1. Dosyalara yaz
    MD_TARGET_1.parent.mkdir(parents=True, exist_ok=True)
    MD_TARGET_1.write_text(content, encoding="utf-8")
    print(f"✓ Yazıldı: {MD_TARGET_1}")
    
    MD_TARGET_2.parent.mkdir(parents=True, exist_ok=True)
    MD_TARGET_2.write_text(content, encoding="utf-8")
    print(f"✓ Yazıldı: {MD_TARGET_2}")
    
    # 2. Okuma PDF motorunu çalıştır
    print("Okuma PDF derleniyor...")
    pdf_path = generate_okuma_pdf(
        MD_TARGET_1,
        course_name="SINIF YÖNETİMİ",
        theme_hex="#1F4775"
    )
    print(f"✓ Okuma PDF başarıyla üretildi: {pdf_path}")

if __name__ == "__main__":
    main()
