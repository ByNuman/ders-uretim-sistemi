# -*- coding: utf-8 -*-
"""PSİKOLOJİYE GİRİŞ — Görsel Ders Notu Kitabı, içerik tanımı.
Kaynak: 'PSİKOLOJİYE GİRİŞ ÖZET.pdf' (ham metin özet, 6 sayfa).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from content_model import (
    Person, KeyTerm, Callout, FlowStep, FlowDiagram, ComparisonTable,
    InfoCard, BulletBlock, Chapter, ChapterPage, Concept, CoursePack,
    QAItem, DistinctionPair, MatchRow, TestQuestion, AnswerItem,
)

# --- TEK KAYNAK: kişi kayıtları (tarihler burada bir kez tanımlanır) -------
FREUD = Person(
    id="freud", name="Sigmund Freud", years="1856–1939",
    tagline="Psikanalizin Kurucusu",
    bio=["Kişiliği İd, Ego ve Süperego üçlüsüyle açıklar; gelişimi <b>haz</b> ve <b>cinsellik</b> odaklı beş psikoseksüel döneme ayırır."],
)
ERIKSON = Person(
    id="erikson", name="Erik Erikson", years="1902–1994",
    tagline="Psikososyal Gelişim Kuramcısı",
    bio=["Freud'un öğrencisi; gelişimi ömür boyu süren, her evrede bir <b>kriz/çatışma</b> içeren sekiz <b>sosyal</b> evreye ayırır."],
)


def get_pack() -> CoursePack:

    # =====================================================================
    # BÖLÜM 1 — Gelişim Psikolojisine Giriş
    # =====================================================================
    ch1 = Chapter(
        number=1,
        title="Gelişim Psikolojisine Giriş",
        subtitle="Büyüme-gelişme ayrımından psikanalitik gelişim kuramlarına temel çerçeve",
        key_terms=[
            KeyTerm("Büyüme", "Sadece fiziksel/niceliksel değişimi ifade eder — boy uzaması, kilo artışı gibi bedence irileşme."),
            KeyTerm("Gelişme", "Büyümeyi de içine alan geniş kavram; fiziksel büyümeyle birlikte fonksiyonel beceri kazanımını kapsar."),
            KeyTerm("Haz Bölgesi (Erojen Bölge)", "Freud'a göre her psikoseksüel dönemde hazzın yoğunlaştığı beden bölgesi (ağız, anüs, cinsel organlar)."),
            KeyTerm("Psikososyal Kriz", "Erikson'a göre her gelişim evresinde bireyin çözmesi gereken, kişiliği şekillendiren temel çatışma."),
        ],
    )
    ch1.pages.append(
        ChapterPage()
        .add_terms(ch1.key_terms)
        .add_callout(Callout("route", "Bölümün Rotası",
            "Önce gelişimin biyolojik ve fonksiyonel yönlerini ayırıp <b>5 temel ilkesini</b> kuruyoruz; ardından psikanalitik geleneğin iki büyük kuramcısı "
            "<b>Freud</b> ve <b>Erikson</b>'ın evrelerini karşılaştırmalı işliyoruz."))
        .add_block(BulletBlock(1, "Büyüme ve Gelişme Arasındaki Fark", [
            "<b>Büyüme:</b> Çocuğun boyunun uzaması, kilonun artması gibi niceliksel/fiziksel değişimdir. Beyin hücresi sayısının artmayıp hacimce büyümesi de buna örnektir.",
            "<b>Gelişme:</b> Kemiklerin sadece uzaması değil, yapısının değişip sertleşmesi; çocuğun bedenen büyümesi değil duygularını kontrol edip uyumlu davranması gelişmedir.",
            "<b>Kapsamı:</b> Döllenmeden ölüme kadar süren, belli bir yöne doğru ilerleyen sürekli değişikliklerdir — sadece ileriye gidişi değil, yaşlılıktaki güçten düşmeyi de kapsar.",
        ]))
        .add_block(BulletBlock(2, "Gelişimin 5 Temel İlkesi", [
            "Gelişim dinamik bir olgudur.",
            "Gelişim, genetik bireyselliğin sonucudur.",
            "Gelişim, giderek artan bir özelleşme sürecidir.",
            "Gelişimde denge vardır.",
            "Gelişim, art arda görülen düzenli bir süreçtir.",
        ], subtitle="Sınavda maddeler halinde sorulabilir."))
    )
    ch1.pages.append(
        ChapterPage(continue_tag="Psikanalitik Gelişim Kuramları: Freud & Erikson")
        .add_person_row([FREUD, ERIKSON])
        .add_table(ComparisonTable(
            "Paralel Okuma: Freud'un Psikoseksüel Dönemleri ile Erikson'un Psikososyal Evreleri",
            ["Yaklaşık Yaş", "Freud — Psikoseksüel Dönem", "Erikson — Psikososyal Kriz"],
            [
                ["0–1,5 yaş", "<b>Oral Dönem:</b> Haz bölgesi ağızdır (emme, ısırma).", "<b>Temel Güven ↔ Güvensizlik:</b> Anne ilgiliyse güven oluşur."],
                ["1,5–3 yaş", "<b>Anal Dönem:</b> Tuvalet kontrolünden zevk alınır; baskı cimrilik/inatçılık doğurur.", "<b>Özerklik ↔ Kuşku/Utanç:</b> Aşırı kısıtlama utanç yaratır."],
                ["3–6 yaş", "<b>Fallik Dönem:</b> Haz bölgesi cinsel organlardır; cinsiyet farkındalığı başlar.", "<b>Girişimcilik ↔ Suçluluk</b> (4–5 yaş): Desteklenen amaç belirler."],
                ["6–12 yaş", "<b>Gizil (Latent) Dönem:</b> Cinsel dürtüler 'uykuya yatar', enerji okul/oyuna yönelir.", "<b>Çalışkanlık ↔ Aşağılık Duygusu:</b> Okul başarısı belirleyicidir."],
                ["12–18/20 yaş", "<b>Genital Dönem:</b> Karşı cinse ilgi başlar, cinsel kimlik olgunlaşır.", "<b>Kimlik Kazanma ↔ Rol Kargaşası:</b> 'Ben kimim?' sorusu merkezdedir."],
            ]
        ))
        .add_block(BulletBlock(3, "Erikson'un Yetişkinlik Evreleri", [
            "<b>Yakınlık ↔ Yalnızlık</b> (20–25 yaş): Kendi benliğini kaybetmeden biriyle 'biz' olabilmektir.",
            "<b>Üretkenlik ↔ Durağanlık</b> (25–65 yaş): Çocuk yetiştirmek veya iş üretmek esastır.",
            "<b>Benlik Bütünlüğü ↔ Umutsuzluk</b> (65+ yaş): Geçmişi kabullenen huzur bulur, 'keşke'leri olan korkar.",
        ]))
        .add_callout(Callout("caution", "Dikkat / Ayırt Etme",
            "Freud <b>haz</b> ve <b>cinsellik</b> odaklıyken, Erikson <b>sosyal ilişkiler</b> ve <b>krizler</b> odaklıdır. "
            "Freud'un dönemleri 18 yaşında biter; Erikson'un evreleri yaşam boyu (65 yaş sonrasına kadar) sürer."))
        .add_summary("Gelişim; büyümeyi de kapsayan, döllenmeden ölüme uzanan yönlü bir süreçtir. Freud bu süreci "
            "beş psikoseksüel döneme, Erikson ise sekiz psikososyal krize ayırarak açıklamıştır — ikisi de kişiliğin "
            "erken yaşlarda temellenip yaşam boyu şekillendiğini savunur.")
    )

    # =====================================================================
    # BÖLÜM 2 — Bebeklik ve Çocukluk Dönemi
    # =====================================================================
    ch2 = Chapter(
        number=2,
        title="Bebeklik ve Çocukluk Dönemi",
        subtitle="Prenatal gelişimden okul çağı davranış kalıplarına somut gelişim çizgisi",
        key_terms=[
            KeyTerm("Prenatal Gelişim", "Doğum öncesi, döllenmeden başlayıp zigot-blastula-gastrula evreleriyle ilerleyen hücresel gelişim süreci."),
            KeyTerm("Sefalokaudal İlke", "Gelişimin baştan kuyruk sokumuna doğru ilerlemesi ilkesi — önce baş/üst, sonra alt beden gelişir."),
            KeyTerm("Eko-Tepki", "Bebeğin ilk 6 ayında çıkardığı, henüz taklit içermeyen anlamsız hece dönemi."),
            KeyTerm("Olumsuzluk (Negativism)", "3 yaş civarı zirve yapan, otoriteye direnme ve inatçılıkla beliren çocukluk davranışı."),
        ],
    )
    ch2.pages.append(
        ChapterPage()
        .add_terms(ch2.key_terms)
        .add_block(BulletBlock(1, "Doğum Öncesi (Prenatal) Gelişim", [
            "<b>Hücresel evreler:</b> Zigot (döllenmiş yumurta) sırasıyla mitoz bölünme, blastula ve gastrula evrelerinden geçer.",
            "<b>Gastrula evresindeki tabakalar:</b> Endoderm (sindirim/solunum sistemleri), Ektoderm (sinir sistemi/deri), Mezoderm (iskelet/kas/dolaşım).",
            "<b>Gelişim yönü:</b> Baştan kuyruk sokumuna doğru ilerler (sefalokaudal ilke).",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("Zigot", "Döllenmiş yumurta"),
            FlowStep("Mitoz Bölünme", "Hücre çoğalması"),
            FlowStep("Blastula", "İçi boş hücre küresi"),
            FlowStep("Gastrula", "Üç tabaka oluşumu"),
        ], caption="Hücresel gelişim evreleri, döllenmeden itibaren sırayla."))
        .add_block(BulletBlock(2, "Doğum Sonrası Motor Gelişim", [
            "<b>3. Ay:</b> Nesnelere ulaşma.", "<b>7. Ay:</b> Desteksiz oturma.",
            "<b>10. Ay:</b> Emekleme.", "<b>15. Ay:</b> Tek başına yürüme.",
        ]))
        .add_block(BulletBlock(3, "Dil ve Duygusal Gelişim", [
            "<b>Dil:</b> İlk 6 ay 'Eko-Tepki' (anlamsız heceler) dönemidir, taklit yoktur. Taklit 1 yaş sonunda başlar; 2 yaşında kelime dağarcığı 272 kelimeye çıkar.",
            "<b>Gülümseme:</b> Önce 'Refleks Gülümseme' (2. ay, uykuda), sonra 'Sosyal Gülümseme' görülür.",
            "<b>Öfke:</b> 1,5–3 yaş arasında zirve yapar. Nedenleri arasında oturağa zorla oturtulma, yüz yıkanması, oyuncağın alınması sayılabilir.",
        ]))
    )
    ch2.pages.append(
        ChapterPage(continue_tag="Çocukluk Dönemi: Sosyalleşme Davranışları")
        .add_table(ComparisonTable(
            "Çocuğun Sosyalleşirken Sergilediği Tipik Davranış Kalıpları",
            ["Davranış", "Tanımı / Zirve Noktası", "Not"],
            [
                ["Olumsuzluk", "3 yaş civarı zirve yapar; otoriteye direnme ve inatçılıktır.", "4 yaşında ödül/ceza sisteminin anlaşılmasıyla azalır."],
                ["Kıskançlık", "İmrenmekten farklıdır — sevginin azalacağı korkusudur.", "Genelde büyük kardeş küçüğü kıskanır; yatak ıslatma, 'bebekleşme' görülebilir."],
                ["Kekeleme", "4–5 yaşlarında görülür, tamamen psikolojik (korku, baskı) kökenlidir.", "Çocuğa baskı yapılmamalıdır."],
                ["Kızdırma / Kabadayılık", "Aşağılık duygusu hisseden çocukların daha zayıflara saldırmasıdır.", "Altta yatan duygu, dışa saldırganlık olarak görünür."],
                ["Oyun", "Çocuğun işidir; terapötik değeri saldırganlığı boşaltmak, eğitimsel değeri kural/kavram öğretmektir.", "Hem duygusal hem bilişsel işlev görür."],
            ]
        ))
        .add_callout(Callout("focus", "Kritik Odak: Okul Başarısını Etkileyenler",
            "Okul başarısını üç grup etken belirler: <b>bireysel nedenler</b> (zeka), <b>öğretim sistemi</b> (ezberci sistem kötü etkiler) "
            "ve <b>aile/öğretmen tutumları</b>."))
        .add_summary("Bebeklik dönemi; hücresel evrelerden başlayarak sefalokaudal ilkeyle ilerleyen motor, dil ve duygusal "
            "gelişimi kapsar. Çocukluk döneminde ise olumsuzluk, kıskançlık, kekeleme gibi davranış kalıpları çocuğun "
            "sosyalleşme sürecinin doğal parçalarıdır ve genelde baskı değil, dengeli yaklaşım gerektirir.")
    )

    # =====================================================================
    # BÖLÜM 3 — Ergenlik, Ahlaki Gelişim ve Yaşam Boyu Değişim
    # =====================================================================
    ch3 = Chapter(
        number=3,
        title="Ergenlik, Ahlaki Gelişim ve Yaşam Boyu Değişim",
        subtitle="Fırtınalı geçişten ahlaki muhakemeye, yetişkinlikten ölüm kabulüne uzanan çizgi",
        key_terms=[
            KeyTerm("Heteronom Ahlak", "Piaget'e göre 10 yaş öncesi görülen, kuralları değişmez sayan ve sonuca bakan ahlak evresi."),
            KeyTerm("Otonom Ahlak", "Piaget'e göre 11 yaş sonrası görülen, kuralları esnek sayan ve niyeti önemseyen ahlak evresi."),
            KeyTerm("Gelenek Sonrası Ahlak", "Kohlberg'e göre yasaların insan hakkına aykırıysa değişebileceğini savunan en üst ahlak düzeyi."),
            KeyTerm("Levinson'ın Rüyası", "Genç yetişkinin geleceğini hayal edip buna uygun roller geliştirmesi süreci."),
        ],
    )
    ch3.pages.append(
        ChapterPage()
        .add_terms(ch3.key_terms)
        .add_block(BulletBlock(1, "Ergenlik Dönemi: Fiziksel ve Sosyal Görünüm", [
            "<b>Fiziksel belirtiler:</b> Kızlarda regl, erkeklerde ses kalınlaşması/tüylenme görülür. Kızlar (11–20 yaş) erkeklerden (13–20 yaş) daha erken olgunlaşır.",
            "<b>Temel sorunlar:</b> Kimlik arayışı, bedeni beğenmeme, güvensizlik ve otoriteyle çatışma.",
            "<b>Sosyal olgunlaşma:</b> Ergenliğin başında çok sayıda geçici arkadaş ve ailenin hiçe sayılması görülürken; sonunda az sayıda derin dostluk ve ailenin fikrinin önemsenmesi görülür.",
        ]))
        .add_table(ComparisonTable(
            "Ergenlik Kişilik Tipleri",
            ["Tip", "Tanım"],
            [
                ["Kuralcı", "Toplum beklentilerine uyan, görev alan tip."],
                ["İdealist", "Adalet duygusu yüksek, dünyayı düzeltmeye çalışan tip."],
                ["Hedonist", "Gününü gün eden, zevk düşkünü tip."],
                ["Psikopat Eğilimli", "Toplumu umursamayan, zarar veren tip."],
            ]
        ))
    )
    ch3.pages.append(
        ChapterPage(continue_tag="Ahlaki Gelişim Kuramları: Piaget & Kohlberg")
        .add_table(ComparisonTable(
            "Piaget'in Ahlaki Gelişim Evreleri",
            ["Evre", "Özellik", "Örnek"],
            [
                ["Heteronom (Dışa Bağlı) — 10 yaş altı", "Kurallar değişmezdir; sonuca bakılır.", "10 bardak kıran, bilerek 1 bardak kırandan daha suçlu görülür."],
                ["Otonom (Özerk) — 11 yaş üstü", "Kurallar esnektir; niyet önemlidir.", "Kazara kıran suçsuz görülebilir."],
            ]
        ))
        .add_table(ComparisonTable(
            "Kohlberg'in Ahlaki Gelişim Düzeyleri",
            ["Düzey", "Aşama", "Açıklama"],
            [
                ["Gelenek Öncesi (Çıkarcı)", "Ceza-İtaat", "Ceza almamak için kurala uyulur."],
                ["Gelenek Öncesi (Çıkarcı)", "Çıkarcılık", "'Kaz gelecek yerden tavuk esirgenmez' mantığı."],
                ["Geleneksel (Toplumsal)", "İyi Çocuk", "Gruba yaranmak, onay almak esastır."],
                ["Geleneksel (Toplumsal)", "Kanun ve Düzen", "Toplum kurallarına körü körüne uyulur."],
                ["Gelenek Sonrası (Evrensel)", "Toplumsal Anlaşma", "Yasalar insan hakkına aykırıysa değişebilir."],
                ["Gelenek Sonrası (Evrensel)", "Evrensel Ahlak", "Adalet, eşitlik, yaşam hakkı her şeyin üstündedir."],
            ]
        ))
        .add_callout(Callout("caution", "Dikkat / Ayırt Etme",
            "Piaget <b>iki evreli</b> (heteronom/otonom) basit bir geçişi anlatır; Kohlberg bunu <b>üç düzey altı aşamaya</b> "
            "genişletip yetişkinliğe kadar uzatır."))
    )
    ch3.pages.append(
        ChapterPage(continue_tag="Yetişkinlik, Yaşlılık ve Ölüm Psikolojisi")
        .add_block(BulletBlock(2, "Yetişkinlik, Yaşlılık ve Ölüm", [
            "<b>Genç Yetişkinlik (Levinson'ın Rüyası):</b> Birey geleceğini hayal eder ve buna uygun roller geliştirir.",
            "<b>Orta Yaş Krizleri:</b> Kadınlarda menopoz (doğurganlığın bitmesi), erkeklerde andropoz (hormon azalması, cinsel ilgi kayması).",
            "<b>Yaşlılık Kuramı — İlgiyi Kesme (Henry):</b> Yaşlının toplumdan kopmasının doğal ve mutluluk getirici olduğunu savunur; eleştirilmiş bir kuramdır.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("İnkâr", "'Bu ben olamam'"),
            FlowStep("Öfke", "'Neden ben?'"),
            FlowStep("Pazarlık", "'Biraz daha zaman ver'"),
            FlowStep("Depresyon", "İçe kapanma"),
            FlowStep("Kabullenme", "Huzur"),
        ], caption="Kübler-Ross'un Ölümün 5 Evresi."))
        .add_summary("Ergenlik; fiziksel olgunlaşmanın yanı sıra kimlik arayışı ve sosyal olgunlaşmayı da içeren geçiş "
            "dönemidir. Ahlaki gelişimde Piaget sonuç-niyet ayrımını, Kohlberg ise çıkardan evrensel ilkelere uzanan "
            "üç düzeyi vurgular. Yaşam çizgisi, Levinson'ın rüyasından Kübler-Ross'un beş ölüm evresine kadar uzanır.")
    )

    # =====================================================================
    # BÖLÜM 4 — Savunma Mekanizmaları
    # =====================================================================
    ch4 = Chapter(
        number=4,
        title="Savunma Mekanizmaları",
        subtitle="Bireyin kaygıyı azaltmak için bilinçsizce başvurduğu on yol",
        key_terms=[
            KeyTerm("Savunma Mekanizması", "Bireyin kaygıyı azaltmak için bilinçdışı biçimde başvurduğu psikolojik baş etme yolu."),
            KeyTerm("Rasyonalizasyon", "Mantığa bürüme; bir davranışa sonradan makul bir kılıf uydurma."),
            KeyTerm("Yansıtma (Projection)", "Kişinin kendi kusurunu başkasında görmesi."),
            KeyTerm("Yüceltme (Sublimation)", "Olumsuz bir dürtüyü toplumca kabul gören, faydalı bir işe çevirme."),
        ],
    )
    ch4.pages.append(
        ChapterPage()
        .add_terms(ch4.key_terms)
        .add_callout(Callout("caution", "Dikkat / Sınav Formatı",
            "Sınavda genellikle bir <b>vaka/örnek</b> verilir ve mekanizmanın adı sorulur. Bu yüzden her mekanizmayı "
            "tanımından çok, tipik örneğiyle birlikte ezberlemek daha güvenlidir."))
        .add_callout(Callout("insight", "Ortak Payda",
            "On mekanizmanın hepsi, egonun <b>kaygıyla doğrudan yüzleşmek yerine dolaylı bir yol bulması</b> ilkesine dayanır — "
            "farklı olan, kaygının hangi yöne saptırıldığıdır: davranışa (rasyonalizasyon), başkasına (yansıtma), "
            "farklı bir hedefe (yer değiştirme) veya üretken bir alana (yüceltme)."))
    )
    ch4.pages.append(
        ChapterPage(continue_tag="On Savunma Mekanizması — Tam Liste")
        .add_table(ComparisonTable(
            "On Savunma Mekanizması",
            ["Mekanizma", "Tanım", "Tipik Örnek"],
            [
                ["Mantığa Bürüme (Rasyonalizasyon)", "Davranışa kılıf uydurma.", "Borçlanan kişinin 'Borç yiğidin kamçısıdır' demesi."],
                ["Karşıt Tepki Geliştirme", "Hissedilenin tam tersini yapma.", "Nefret ettiği kişiye aşırı kibar davranmak."],
                ["Bastırma (Repression)", "Unutma, bilinç dışına itme.", "Ölüm korkusunu yok sayıp hiç ölmeyecekmiş gibi yaşamak."],
                ["Yansıtma (Projection)", "Kendi kusurunu başkasında görme.", "Cimri birinin 'Herkes çok bencil' demesi."],
                ["Özdeşleşme (Identification)", "Başkasının özelliklerini taklit etme.", "Film yıldızı gibi giyinmek."],
                ["Yer Değiştirme (Displacement)", "Öfkeyi asıl kaynağa değil, gücünün yettiğine yöneltme.", "Müdüre kızıp evde çocuğa bağırmak."],
                ["Yüceltme (Sublimation)", "Olumsuz dürtüyü faydalı bir işe çevirme.", "Saldırgan birinin boksör veya polis olması."],
                ["Düşünselleştirme", "Duyguyu soyut bilgiyle örtme.", "Hak yiyen patronun işçi hakları üzerine felsefe yapması."],
                ["Telafi (Compensation)", "Bir alandaki eksikliği başka alanla kapatma.", "Dersleri kötü olanın sporda şampiyon olması."],
                ["İnkâr (Denial)", "Gerçeği reddetme.", "'Ben yapmadım, öyle bir şey yok' demek."],
            ]
        ))
        .add_summary("Savunma mekanizmaları, egonun kaygıyla baş etmek için bilinçdışı olarak devreye soktuğu on "
            "farklı stratejidir. Ortak nokta, gerçeğin doğrudan değil dolaylı biçimde ele alınmasıdır — bu da onları "
            "sınavda vaka-eşleştirme sorularının klasik konusu yapar.")
    )

    # =====================================================================
    # BÖLÜM 5 — Psikolojik Bozukluklar ve Kişilik Kuramları
    # =====================================================================
    ch5 = Chapter(
        number=5,
        title="Psikolojik Bozukluklar ve Kişilik Kuramları",
        subtitle="Nevroz-psikoz ayrımından kişiliği açıklayan kuramlara",
        key_terms=[
            KeyTerm("Nevroz", "Gerçeklik algısının korunduğu, görece hafif seyreden psikolojik bozukluk grubu."),
            KeyTerm("Psikoz", "Gerçeklikle bağın koptuğu, ağır seyreden psikolojik bozukluk grubu."),
            KeyTerm("Mizaç (Huy)", "Biyolojik, doğuştan gelen ve değişmeyen kişilik bileşeni."),
            KeyTerm("Karakter", "Sosyal, sonradan kazanılan ve eğitimle değişebilen kişilik bileşeni."),
        ],
    )
    ch5.pages.append(
        ChapterPage()
        .add_terms(ch5.key_terms)
        .add_callout(Callout("route", "Bölümün Rotası",
            "Psikolojik bozukluklar <b>nevroz</b> (hafif, gerçeklik algısı korunur) ve <b>psikoz</b> (ağır, gerçeklikle "
            "bağ kopar) olarak ikiye ayrılır; ardından kişiliği açıklayan tip kuramlarına ve Freud'un yapısal modeline geçilir."))
        .add_table(ComparisonTable(
            "Nevrozlar (Psikonevrozlar) — Hafif Bozukluklar",
            ["Tip", "Belirti"],
            [
                ["Nevrasteni", "Sebepsiz yorgunluk, 'bitiklik' hali."],
                ["Psikasteni (OKB)", "Takıntılı düşünceler (obsesyon) ve tekrarlayan hareketler (kompulsiyon) — ör. kapıyı 10 kere kontrol etmek."],
                ["Histeri", "İlgi çekmek için fiziksel hastalık taklidi yapma (ör. psikolojik felç)."],
            ]
        ))
        .add_table(ComparisonTable(
            "Psikozlar — Ağır Bozukluklar",
            ["Tip", "Belirti"],
            [
                ["Şizofreni — Katatonik", "Donup kalma."],
                ["Şizofreni — Paranoid", "'Beni öldürecekler' kuşkusu."],
                ["Şizofreni — Dezorganize", "Saçma konuşma, çocuksu hareketler."],
                ["Paranoya", "Sistemli hezeyanlar (kıskançlık paranoyası, büyüklük/mehdi kompleksi)."],
                ["Mani-Depresif (İki Uçlu)", "Bir dönem aşırı neşe (mani), bir dönem derin üzüntü (depresyon)."],
            ]
        ))
    )
    ch5.pages.append(
        ChapterPage(continue_tag="Kişilik Kuramları")
        .add_block(BulletBlock(1, "Temel Tanımlar", [
            "<b>Persona:</b> Maske demektir.",
            "<b>Mizaç (Huy):</b> Biyolojiktir, doğuştan gelir, değişmez (ör. çabuk kızmak).",
            "<b>Karakter:</b> Sosyaldir, sonradan kazanılır, eğitimle değişir (ör. dürüstlük).",
        ]))
        .add_table(ComparisonTable(
            "Sınıflandırma (Tip) Kuramları",
            ["Kuramcı", "Sınıflandırma"],
            [
                ["Hipokrat (Sıvılar)", "Kan (canlı), Balgam (yavaş), Kara Safra (melankolik), Sarı Safra (öfkeli)."],
                ["Sheldon (Beden Tipleri)", "Endomorf (şişman/rahat), Mezomorf (kaslı/enerjik), Ektomorf (zayıf/içe dönük)."],
                ["Jung", "İçe dönük ve Dışa dönük."],
            ]
        ))
        .add_info_cards("Freud'un Psikanalitik Kişilik Yapısı", [
            InfoCard("İd (Altben)", "İlkeldir, haz ilkesiyle çalışır — 'Hemen istiyorum' der.", "1"),
            InfoCard("Ego (Ben)", "Mantıklıdır, gerçeklik ilkesiyle çalışır — İd ile Süperego'yu uzlaştırır.", "2"),
            InfoCard("Süperego (Üstben)", "Vicdandır, ahlak ilkesiyle çalışır — 'Ayıp, yasak' der.", "3"),
        ])
        .add_block(BulletBlock(2, "Kişiliği Etkileyen Faktörler", [
            "<b>Kalıtım:</b> Zeka büyük oranda kalıtsaldır.",
            "<b>Aile:</b> Demokratik tutum en sağlıklısıdır; aşırı koruyucu veya otoriter aile kişiliği bozar.",
            "<b>Din:</b> Benlik oluşumunda referans kaynağıdır, güven verir.",
        ]))
        .add_summary("Psikolojik bozukluklar gerçeklik algısının korunup korunmamasına göre nevroz-psikoz ekseninde "
            "sınıflanır. Kişilik ise hem biyolojik (mizaç) hem sosyal (karakter) bileşenlerden oluşur; Freud'un "
            "İd-Ego-Süperego modeli bu yapının iç dengesini, kalıtım-aile-din üçlüsü ise dış etkenlerini açıklar.")
    )

    chapters = [ch1, ch2, ch3, ch4, ch5]

    # =====================================================================
    # SÖZLÜK
    # =====================================================================
    glossary = [
        Concept("Büyüme", "Fiziksel/niceliksel değişim; boy ve kilo artışı.", "Gelişim Temelleri", 1),
        Concept("Gelişme", "Büyümeyi de kapsayan, fonksiyonel beceri kazanımını içeren geniş kavram.", "Gelişim Temelleri", 1),
        Concept("Oral Dönem", "0–1,5 yaş; haz bölgesi ağızdır.", "Freud", 1),
        Concept("Anal Dönem", "1,5–3 yaş; haz bölgesi anüstür, tuvalet kontrolü önemlidir.", "Freud", 1),
        Concept("Fallik Dönem", "3–6 yaş; haz bölgesi cinsel organlardır.", "Freud", 1),
        Concept("Gizil (Latent) Dönem", "6–12 yaş; cinsel dürtüler uykuya yatar.", "Freud", 1),
        Concept("Genital Dönem", "12–18/20 yaş; cinsel kimlik olgunlaşır.", "Freud", 1),
        Concept("Temel Güven vs. Güvensizlik", "0–1 yaş; anne ilgisi güven duygusunu belirler.", "Erikson", 1),
        Concept("Kimlik Kazanma vs. Rol Kargaşası", "12–20 yaş; 'Ben kimim?' sorusu merkezdedir.", "Erikson", 1),
        Concept("Sefalokaudal İlke", "Gelişimin baştan kuyruk sokumuna doğru ilerlemesi.", "Prenatal Gelişim", 2),
        Concept("Eko-Tepki", "İlk 6 ayda görülen, taklit içermeyen anlamsız hece dönemi.", "Dil Gelişimi", 2),
        Concept("Olumsuzluk (Negativism)", "3 yaş civarı zirve yapan otoriteye direnme davranışı.", "Çocukluk Dönemi", 2),
        Concept("Heteronom Ahlak", "10 yaş altı; kurallar değişmez, sonuca bakılır.", "Piaget", 3),
        Concept("Otonom Ahlak", "11 yaş üstü; kurallar esnektir, niyet önemlidir.", "Piaget", 3),
        Concept("Gelenek Öncesi Düzey", "Ceza-itaat ve çıkarcılık aşamalarını içeren ilk ahlak düzeyi.", "Kohlberg", 3),
        Concept("Gelenek Sonrası Düzey", "Toplumsal anlaşma ve evrensel ahlak aşamalarını içeren en üst düzey.", "Kohlberg", 3),
        Concept("Levinson'ın Rüyası", "Genç yetişkinin geleceğini hayal edip ona uygun roller geliştirmesi.", "Yetişkinlik", 3),
        Concept("Kübler-Ross'un Beş Evresi", "İnkâr, öfke, pazarlık, depresyon, kabullenme.", "Ölüm Psikolojisi", 3),
        Concept("Rasyonalizasyon", "Davranışa sonradan mantıklı bir kılıf uydurma.", "Savunma Mekanizmaları", 4),
        Concept("Yansıtma (Projection)", "Kendi kusurunu başkasında görme.", "Savunma Mekanizmaları", 4),
        Concept("Yer Değiştirme (Displacement)", "Öfkeyi asıl kaynağa değil, gücünün yettiğine yöneltme.", "Savunma Mekanizmaları", 4),
        Concept("Yüceltme (Sublimation)", "Olumsuz dürtüyü faydalı bir işe çevirme.", "Savunma Mekanizmaları", 4),
        Concept("Telafi (Compensation)", "Bir alandaki eksikliği başka alanla kapatma.", "Savunma Mekanizmaları", 4),
        Concept("Nevroz", "Gerçeklik algısının korunduğu hafif bozukluk grubu.", "Bozukluklar", 5),
        Concept("Psikoz", "Gerçeklikle bağın koptuğu ağır bozukluk grubu.", "Bozukluklar", 5),
        Concept("Şizofreni", "Gerçeklikten kopuşla giden; katatonik, paranoid, dezorganize tipleri vardır.", "Bozukluklar", 5),
        Concept("İd (Altben)", "Haz ilkesiyle çalışan, ilkel kişilik katmanı.", "Freud'un Kişilik Yapısı", 5),
        Concept("Ego (Ben)", "Gerçeklik ilkesiyle çalışan, dengeleyici kişilik katmanı.", "Freud'un Kişilik Yapısı", 5),
        Concept("Süperego (Üstben)", "Ahlak ilkesiyle çalışan, vicdan işlevi gören kişilik katmanı.", "Freud'un Kişilik Yapısı", 5),
        Concept("Mizaç", "Doğuştan gelen, değişmeyen kişilik bileşeni.", "Kişilik Kuramları", 5),
    ]

    # =====================================================================
    # TEST — 20 Soruluk Genel Değerlendirme
    # =====================================================================
    test_questions = [
        TestQuestion(1, "Çocuğun boyunun uzaması ve kilosunun artması gibi yalnızca niceliksel/fiziksel değişimlere ne ad verilir?",
            {"A": "Gelişme", "B": "Büyüme", "C": "Olgunlaşma", "D": "Öğrenme", "E": "Toplumsallaşma"}),
        TestQuestion(2, "Freud'a göre 3-6 yaş arasında haz bölgesinin cinsel organlar olduğu, cinsiyet farkındalığının başladığı dönem hangisidir?",
            {"A": "Oral Dönem", "B": "Anal Dönem", "C": "Fallik Dönem", "D": "Gizil Dönem", "E": "Genital Dönem"}),
        TestQuestion(3, "Erikson'a göre 0-1 yaş arasındaki psikososyal kriz hangisidir?",
            {"A": "Özerklik vs. Kuşku", "B": "Temel Güven vs. Güvensizlik", "C": "Girişimcilik vs. Suçluluk", "D": "Kimlik Kazanma vs. Rol Kargaşası", "E": "Yakınlık vs. Yalnızlık"}),
        TestQuestion(4, "Freud ile Erikson'un gelişim kuramları arasındaki temel fark nedir?",
            {"A": "Freud sosyal krizleri, Erikson cinselliği esas alır", "B": "Freud'un evreleri yaşam boyu, Erikson'unkiler 18 yaşında biter",
             "C": "Freud haz ve cinsellik odaklıdır, Erikson sosyal ilişkiler ve krizler odaklıdır", "D": "İkisi de aynı yaş aralıklarını kullanır", "E": "Erikson kişiliği İd-Ego-Süperego ile açıklar"}),
        TestQuestion(5, "Gelişimin baştan kuyruk sokumuna doğru ilerlemesi ilkesine ne ad verilir?",
            {"A": "Sefalokaudal İlke", "B": "Proksimodistal İlke", "C": "Kritik Dönem İlkesi", "D": "Süreklilik İlkesi", "E": "Bireyselleşme İlkesi"}),
        TestQuestion(6, "Bebeğin ilk 6 ayında çıkardığı, henüz taklit içermeyen anlamsız hecelere ne ad verilir?",
            {"A": "Sosyal Gülümseme", "B": "Refleks Gülümseme", "C": "Eko-Tepki", "D": "Olumsuzluk", "E": "Kekeleme"}),
        TestQuestion(7, "3 yaş civarında zirve yapan, otoriteye direnme ve inatçılıkla beliren çocukluk davranışına ne ad verilir?",
            {"A": "Kıskançlık", "B": "Olumsuzluk (Negativism)", "C": "Kekeleme", "D": "Kabadayılık", "E": "Kültür Şoku"}),
        TestQuestion(8, "Piaget'e göre 10 yaş altındaki çocuklar, kasıtlı olarak 1 bardak kıran ile kazara 10 bardak kıran arasında nasıl bir değerlendirme yapar?",
            {"A": "Niyete bakarak kasıtlı kıran daha suçlu bulunur", "B": "Sonuca bakarak 10 bardak kıran daha suçlu bulunur",
             "C": "İkisi de eşit suçlu bulunur", "D": "İkisi de suçsuz bulunur", "E": "Yaş bu değerlendirmeyi etkilemez"}),
        TestQuestion(9, "Kohlberg'in ahlaki gelişim kuramında yasaların insan hakkına aykırıysa değişebileceğini savunan en üst düzey hangisidir?",
            {"A": "Gelenek Öncesi Düzey", "B": "Geleneksel Düzey", "C": "Gelenek Sonrası Düzey", "D": "Heteronom Düzey", "E": "Otonom Düzey"}),
        TestQuestion(10, "Piaget'in ahlaki gelişim modeli ile Kohlberg'in modeli arasındaki temel fark nedir?",
            {"A": "Piaget üç düzeyli, Kohlberg iki evrelidir", "B": "Piaget iki evreli basit bir geçişi anlatır; Kohlberg üç düzey altı aşamaya genişletir",
             "C": "İkisi de aynı yaş aralığını kapsar", "D": "Kohlberg yalnızca çocukluğu inceler", "E": "Piaget yetişkinliğe kadar uzanır"}),
        TestQuestion(11, "Genç yetişkinin geleceğini hayal edip buna uygun roller geliştirmesi süreci hangi kavramla açıklanır?",
            {"A": "Levinson'ın Rüyası", "B": "Kübler-Ross'un Evreleri", "C": "Andropoz", "D": "Kimlik Kazanma", "E": "Yaşlılık Kuramı"}),
        TestQuestion(12, "Kübler-Ross'un ölümün beş evresi hangi sırayla ilerler?",
            {"A": "Öfke → İnkâr → Pazarlık → Kabullenme → Depresyon", "B": "İnkâr → Öfke → Pazarlık → Depresyon → Kabullenme",
             "C": "Pazarlık → İnkâr → Depresyon → Öfke → Kabullenme", "D": "Depresyon → İnkâr → Öfke → Pazarlık → Kabullenme", "E": "İnkâr → Depresyon → Öfke → Pazarlık → Kabullenme"}),
        TestQuestion(13, "Cimri bir kişinin 'Herkes çok bencil' demesi hangi savunma mekanizmasına örnektir?",
            {"A": "Rasyonalizasyon", "B": "Yansıtma (Projection)", "C": "Yüceltme (Sublimation)", "D": "Telafi (Compensation)", "E": "Bastırma (Repression)"}),
        TestQuestion(14, "Saldırgan bir kişinin boksör veya polis olmayı seçmesi hangi savunma mekanizmasına örnektir?",
            {"A": "Yer Değiştirme (Displacement)", "B": "Karşıt Tepki Geliştirme", "C": "Yüceltme (Sublimation)", "D": "İnkâr (Denial)", "E": "Düşünselleştirme"}),
        TestQuestion(15, "Müdürüne kızan bir kişinin eve gelip çocuğuna bağırması hangi savunma mekanizmasına örnektir?",
            {"A": "Yer Değiştirme (Displacement)", "B": "Yansıtma (Projection)", "C": "Telafi (Compensation)", "D": "Özdeşleşme (Identification)", "E": "Rasyonalizasyon"}),
        TestQuestion(16, "Gerçeklik algısının korunduğu, görece hafif seyreden psikolojik bozukluk grubuna ne ad verilir?",
            {"A": "Psikoz", "B": "Nevroz", "C": "Şizofreni", "D": "Paranoya", "E": "Mani-Depresif Bozukluk"}),
        TestQuestion(17, "Takıntılı düşünceler (obsesyon) ve tekrarlayan hareketler (kompulsiyon) ile belirgin nevroz türü hangisidir?",
            {"A": "Nevrasteni", "B": "Histeri", "C": "Psikasteni (OKB)", "D": "Paranoya", "E": "Şizofreni"}),
        TestQuestion(18, "Freud'un kişilik yapısında 'Hemen istiyorum' diyen, haz ilkesiyle çalışan ilkel katman hangisidir?",
            {"A": "Ego", "B": "Süperego", "C": "İd", "D": "Persona", "E": "Mizaç"}),
        TestQuestion(19, "Mizaç ile karakter arasındaki fark nedir?",
            {"A": "Mizaç sonradan kazanılır, karakter doğuştan gelir", "B": "Mizaç biyolojik ve değişmezdir; karakter sosyaldir ve eğitimle değişebilir",
             "C": "İkisi de tamamen değişmezdir", "D": "İkisi de tamamen sonradan kazanılır", "E": "Mizaç yalnızca yetişkinlikte oluşur"}),
        TestQuestion(20, "Sheldon'un beden tiplerine dayalı kişilik sınıflandırmasında 'kaslı/enerjik' tipe ne ad verilir?",
            {"A": "Endomorf", "B": "Mezomorf", "C": "Ektomorf", "D": "Melankolik", "E": "İçe Dönük"}),
    ]

    answer_key_items = [
        AnswerItem(1, "B", "<b>Büyüme</b>, boy/kilo artışı gibi yalnızca niceliksel/fiziksel değişimdir; gelişme ise buna fonksiyonel beceri kazanımını da ekler."),
        AnswerItem(2, "C", "<b>Fallik Dönem</b> (3-6 yaş), haz bölgesinin cinsel organlar olduğu, cinsiyet farkındalığının başladığı dönemdir."),
        AnswerItem(3, "B", "Erikson'un ilk psikososyal krizi <b>Temel Güven vs. Güvensizlik</b>'dir (0-1 yaş); anne ilgisi güven duygusunu belirler."),
        AnswerItem(4, "C", "Freud haz ve cinsellik odaklıyken, Erikson sosyal ilişkiler ve krizler odaklıdır; bu ayrım sınavda en sık sorulan noktadır."),
        AnswerItem(5, "A", "<b>Sefalokaudal İlke</b>, gelişimin baştan (baş/üst) kuyruk sokumuna (alt beden) doğru ilerlemesidir."),
        AnswerItem(6, "C", "<b>Eko-Tepki</b>, bebeğin ilk 6 ayında çıkardığı, henüz taklit içermeyen anlamsız hece dönemidir."),
        AnswerItem(7, "B", "<b>Olumsuzluk (Negativism)</b>, 3 yaş civarı zirve yapan, otoriteye direnme ve inatçılıkla beliren davranıştır."),
        AnswerItem(8, "B", "Heteronom (dışa bağlı) ahlak döneminde (10 yaş altı) niyet değil sonuç önemlidir; bu yüzden 10 bardak kıran daha suçlu bulunur."),
        AnswerItem(9, "C", "<b>Gelenek Sonrası Düzey</b>, Kohlberg'in en üst ahlak düzeyidir; yasaların insan hakkına aykırıysa değişebileceğini savunur."),
        AnswerItem(10, "B", "Piaget iki evreli (heteronom/otonom) basit bir geçişi anlatırken, Kohlberg bunu üç düzey altı aşamaya genişletip yetişkinliğe kadar uzatır."),
        AnswerItem(11, "A", "<b>Levinson'ın Rüyası</b>, genç yetişkinin geleceğini hayal edip buna uygun roller geliştirmesi sürecidir."),
        AnswerItem(12, "B", "Kübler-Ross'un sırası: <b>İnkâr → Öfke → Pazarlık → Depresyon → Kabullenme</b>."),
        AnswerItem(13, "B", "<b>Yansıtma (Projection)</b>, kişinin kendi kusurunu başkasında görmesidir; cimri kişinin başkalarını bencillikle suçlaması buna örnektir."),
        AnswerItem(14, "C", "<b>Yüceltme (Sublimation)</b>, olumsuz bir dürtüyü toplumca kabul gören faydalı bir işe çevirmedir (ör. saldırganlığın boksörlüğe dönüşmesi)."),
        AnswerItem(15, "A", "<b>Yer Değiştirme (Displacement)</b>, öfkeyi asıl kaynağa değil, gücünün yettiği bir hedefe yöneltmedir."),
        AnswerItem(16, "B", "<b>Nevroz</b>, gerçeklik algısının korunduğu, görece hafif seyreden bozukluk grubudur; psikozda ise gerçeklikle bağ kopar."),
        AnswerItem(17, "C", "<b>Psikasteni (OKB)</b>, takıntılı düşünceler (obsesyon) ve tekrarlayan hareketlerle (kompulsiyon) belirgindir."),
        AnswerItem(18, "C", "<b>İd (Altben)</b>, haz ilkesiyle çalışan, 'hemen istiyorum' diyen ilkel kişilik katmanıdır."),
        AnswerItem(19, "B", "<b>Mizaç</b> biyolojik ve değişmezdir (ör. çabuk kızmak); <b>karakter</b> ise sosyaldir ve eğitimle değişebilir (ör. dürüstlük)."),
        AnswerItem(20, "B", "Sheldon'un sınıflandırmasında <b>Mezomorf</b> kaslı/enerjik beden tipini; Endomorf şişman/rahat, Ektomorf zayıf/içe dönük tipi tanımlar."),
    ]

    return CoursePack(
        course_code="PSİKOLOJİ",
        title='Psikoloji<span class="accent-word">ye</span> Giriş',
        subtitle="Gelişim Psikolojisi, Kişilik Kuramları ve Ruhsal Bozukluklara Temel Bakış",
        description=(
            "Büyüme-gelişme ayrımından Freud ve Erikson'un gelişim kuramlarına; bebeklikten yaşlılığa yaşam boyu "
            "değişime, savunma mekanizmalarından kişilik kuramlarına uzanan final sınavı özeti."
        ),
        theme="indigo",
        icon_text="Ψ",
        chapters=chapters,
        glossary=glossary,
        test_title="Genel Değerlendirme Testi",
        test_subtitle="Gelişim, ahlaki gelişim, savunma mekanizmaları ve kişilik kuramları üzerine kapsamlı test",
        test_instructions="Aşağıdaki sorularda beş seçenekten yalnızca birini işaretleyiniz. Süre: 30 dakika.",
        test_questions=test_questions,
        answer_key_intro="Her sorunun doğru cevabı ve kısa gerekçesi aşağıda yer almaktadır.",
        answer_key_items=answer_key_items,
        overview_lead=(
            "Bu ders; insanın <b>döllenmeden ölüme</b> uzanan gelişim çizgisini, bu çizgiyi açıklayan başlıca "
            "kuramları ve kişiliği/ruh sağlığını konu alan temel kavramları bir bütün olarak ele alır."
        ),
        overview_cards=[
            {"title": "Gelişimin Temelleri", "text": "Büyüme-gelişme ayrımı ve gelişimin 5 temel ilkesi."},
            {"title": "Psikanalitik Kuramlar", "text": "Freud'un psikoseksüel dönemleri, Erikson'un psikososyal evreleri."},
            {"title": "Yaşam Evreleri", "text": "Bebeklik, çocukluk, ergenlik, yetişkinlik, yaşlılık ve ölüm."},
            {"title": "Ahlaki Gelişim", "text": "Piaget'in heteronom/otonom ayrımı, Kohlberg'in üç düzeyi."},
            {"title": "Savunma Mekanizmaları", "text": "Egonun kaygıyla baş etmek için kullandığı 10 bilinçdışı yol."},
            {"title": "Kişilik ve Bozukluklar", "text": "Nevroz-psikoz ayrımı, tip kuramları, İd-Ego-Süperego."},
        ],
        overview_flow=[
            ("Temel Kavramlar", "Büyüme / gelişme"),
            ("Gelişim Kuramları", "Freud / Erikson"),
            ("Yaşam Evreleri", "Bebeklikten yaşlılığa"),
            ("Savunma & Kişilik", "Mekanizmalar / tipler"),
        ],
        overview_note=(
            "Sınavda en çok karıştırılan yer, <b>kuramcı-kavram eşleştirmesidir:</b> Freud'un dönemleri cinsellik "
            "temelli ve 18 yaşında biter; Erikson'un evreleri sosyal kriz temelli ve yaşam boyu sürer."
        ),
    )
