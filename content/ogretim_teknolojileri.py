# -*- coding: utf-8 -*-
"""ÖĞRETİM TEKNOLOJİLERİ — Görsel Ders Notu Kitabı, içerik tanımı.
Kaynak: 'ÖĞRETİM TEKNOLOJİLERİ ÖZET.pdf' (ham metin özet, 5 sayfa).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from content_model import (
    Person, KeyTerm, Callout, FlowStep, FlowDiagram, ComparisonTable,
    InfoCard, BulletBlock, Chapter, ChapterPage, Concept, CoursePack,
    QAItem, DistinctionPair, MatchRow,
)

DALE = Person(
    id="dale", name="Edgar Dale", years="1900–1985",
    tagline="Yaşantı Piramidi'nin Kurucusu",
    bio=["1946'da tanıttığı <b>Yaşantı (Deneyim) Piramidi</b> ile öğrenmeye katılan duyu organı sayısı arttıkça "
         "öğrenme kalitesinin arttığını ve unutmanın azaldığını göstermiştir."],
)


def get_pack() -> CoursePack:

    # =====================================================================
    # BÖLÜM 1 — Materyal Kavramı, Öğrenme Piramidi ve Yaklaşımlar
    # =====================================================================
    ch1 = Chapter(
        number=1,
        title="Materyal Kavramı ve Öğrenme Piramidi",
        subtitle="Eğitim materyalinin tanımından Dale'in piramidine, çağdaş öğretim yaklaşımlarına temel çerçeve",
        key_terms=[
            KeyTerm("Materyal", "Öğrenme ve öğretme sürecinde yardımcı olan yazılı, sözlü ve görüntülü her türlü eğitsel belge."),
            KeyTerm("Yaşantı Piramidi", "Dale'e göre öğrenmeye katılan duyu organı sayısı arttıkça öğrenme kalitesinin artması ve unutmanın azalması ilkesi."),
            KeyTerm("Yapılandırmacı Yaklaşım", "Bilginin öğretmenden öğrenciye aktarılması değil, öğrencinin zihninde kendisinin yapılandırması esasına dayanan yaklaşım."),
            KeyTerm("Özel Hedef", "Genel hedefler doğrultusunda belirlenen, her bir derse özgü öğrenme hedefi."),
        ],
    )
    ch1.pages.append(
        ChapterPage()
        .add_terms(ch1.key_terms)
        .add_block(BulletBlock(1, "Materyal Tanımı ve Yararları", [
            "<b>Tanım:</b> Genel anlamda her türlü araç, gereç ve malzeme; eğitim açısından ise öğrenme-öğretme "
            "süreçlerinde yardımcı olan yazılı, sözlü ve görüntülü her türlü eğitsel belgedir.",
            "<b>Yararları:</b> Materyaller genel eğitimde ve din eğitiminde bilişsel (bilgi), duyuşsal (duygu) ve "
            "psiko-motor (davranış/beceri) alanlarda fayda sağlar — tekdüzeliği giderip dersi canlı kılar, zamanı "
            "etkili kullandırır ve vakit kaybını önler.",
        ]))
        .add_person(DALE)
    )
    ch1.pages.append(
        ChapterPage(continue_tag="Öğrenme Oranları ve Eğitimsel Yaklaşımlar")
        .add_table(ComparisonTable(
            "Dale'in Öğrenme Oranları",
            ["Etkinlik", "Hatırlama Oranı"],
            [
                ["Okuduklarımız", "%10"],
                ["İşittiklerimiz", "%20"],
                ["Gördüklerimiz", "%30"],
                ["Yapıp Söylediklerimiz", "%90"],
            ]
        ))
        .add_callout(Callout("insight", "Piramidin Mantığı",
            "Öğretim <b>'Basitten Karmaşığa'</b> ve <b>'Somuttan Soyuta'</b> doğru ilerlemelidir. En kalıcı öğrenme, "
            "<b>'yaparak ve yaşayarak'</b> gerçekleşendir."))
        .add_table(ComparisonTable(
            "Eğitimsel Yaklaşımların 4 Temel Unsuru",
            ["Unsur", "Açıklama"],
            [
                ["Yapılandırmacı Yaklaşım", "Bilgi öğretmenden aktarılmaz; öğrenci zihninde kendisi yapılandırır."],
                ["Çoklu Zeka", "Öğretim; sözel, görsel, içsel ve sosyal gibi farklı zeka türlerine hitap etmelidir."],
                ["Öğrenci Merkezlilik", "Öğrenci pasif alıcı değil, sürecin aktif katılımcısıdır."],
                ["Etkinlik ve Materyal", "Dersler yalnızca anlatımla değil; inceleme, araştırma ve tartışmayla işlenmelidir."],
            ]
        ))
    )
    ch1.pages.append(
        ChapterPage(continue_tag="Hedeflerin Sınıflandırılması")
        .add_block(BulletBlock(2, "Öğretimde Hedeflerin Sınıflandırılması", [
            "Eğitim faaliyetlerinde hedefler üç düzeyde ele alınır:",
            "<b>Uzak Hedef:</b> Devletin eğitim politikası ve felsefesidir.",
            "<b>Genel Hedef:</b> Uzak hedefler doğrultusunda okulların (kurumların) hedefleridir.",
            "<b>Özel Hedef:</b> Genel hedefler doğrultusunda her bir dersin kendine ait hedefleridir.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("Uzak Hedef", "Devlet politikası"),
            FlowStep("Genel Hedef", "Kurumun hedefi"),
            FlowStep("Özel Hedef", "Dersin hedefi"),
        ], caption="Hedefler, genelden özele doğru daralarak sınıfa iner."))
        .add_summary("Materyal, öğrenmeyi bilişsel, duyuşsal ve psiko-motor alanlarda destekleyen her türlü eğitsel "
            "araçtır. Dale'in Yaşantı Piramidi, en kalıcı öğrenmenin yaparak-yaşayarak gerçekleştiğini gösterir; "
            "yapılandırmacı, çoklu zeka ve öğrenci merkezli yaklaşımlar bu ilkeyi sınıfa taşır.")
    )

    # =====================================================================
    # BÖLÜM 2 — Bloom Taksonomisi ve Materyal Hazırlama İlkeleri
    # =====================================================================
    ch2 = Chapter(
        number=2,
        title="Bloom Taksonomisi ve Materyal İlkeleri",
        subtitle="Bilişsel, duyuşsal ve psiko-motor amaçlardan materyal hazırlamanın altı ilkesine",
        key_terms=[
            KeyTerm("Taksonomi", "Bloom'un, öğretim hedeflerini basitten karmaşığa, somuttan soyuta aşamalı sıraladığı sınıflandırma sistemi."),
            KeyTerm("Bilişsel Amaç", "Bilgi, kavrama, uygulama, analiz, sentez ve değerlendirme düzeylerini kapsayan zihinsel süreç hedefleri."),
            KeyTerm("Duyuşsal Amaç", "Alma, tepkide bulunma, değer verme, örgütleme ve kişilik düzeylerini kapsayan duygusal tepki hedefleri."),
            KeyTerm("Psiko-motor Amaç", "Hazır olma, taklit etme ve beceri haline getirmeyi kapsayan bedensel beceri hedefleri."),
        ],
    )
    ch2.pages.append(
        ChapterPage()
        .add_terms(ch2.key_terms)
        .add_callout(Callout("route", "Bölümün Rotası",
            "Bloom'un taksonomisi hedefleri üç alanda basitten karmaşığa sıralar: <b>Bilişsel</b> (zihin), "
            "<b>Duyuşsal</b> (duygu) ve <b>Psiko-motor</b> (beden). Ardından materyal hazırlamanın 6 temel ilkesine geçilir."))
        .add_table(ComparisonTable(
            "A. Bilişsel Amaçlar (Zihinsel Süreçler) — Basitten Karmaşığa",
            ["Düzey", "Açıklama"],
            [
                ["1. Bilgi", "Tanımlama, ezberleme, söyleme, tanıma (Hatırlama düzeyi)."],
                ["2. Kavrama", "Yorumlama, özetleme, açıklama, yordama yapma (Anlama düzeyi)."],
                ["3. Uygulama", "Yöntem kullanma, problem çözme, tahmin etme (Transfer etme)."],
                ["4. Analiz", "Ayrıştırma, bölümlere ayırma, ilişkileri belirleme (Parçalara bölme)."],
                ["5. Sentez", "Birleştirme, fikir oluşturma, ilişkilendirme, yeni bir bütün oluşturma."],
                ["6. Değerlendirme", "Yargılama, hüküm verme, kritize etme (Karar verme)."],
            ]
        ))
    )
    ch2.pages.append(
        ChapterPage(continue_tag="Duyuşsal ve Psiko-Motor Amaçlar")
        .add_table(ComparisonTable(
            "B. Duyuşsal Amaçlar (Basitten Karmaşığa)",
            ["Düzey", "Açıklama"],
            [
                ["1. Alma", "Farkında olma, dikkat etme, seçme."],
                ["2. Tepkide Bulunma", "İstekli olma, katılma, zevk alma, onaylama."],
                ["3. Değer Verme", "Destekleme, bir konuya düşkün olma, kendine iş edinme."],
                ["4. Örgütleme", "Kararlı olma, savunma, hayata geçirme, düzenleme."],
                ["5. Kişilik (Nitelenmişlik)", "Davranışı kişilik haline getirme, adanma, sürekli yapma (karakter haline gelmesi)."],
            ]
        ))
        .add_table(ComparisonTable(
            "C. Psiko-Motor Amaçlar (Basitten Karmaşığa)",
            ["Düzey", "Açıklama"],
            [
                ["1. Uyarılma", "Algılama, izleme (Gözlem aşaması)."],
                ["2. Hazır Olma", "Uygun konuma gelme (Kurulma)."],
                ["3. Kılavuz Denetiminde Yapma", "Yardımla yapabilme, taklit etme."],
                ["4. Beceri Haline Getirme", "Kendi başına yapabilme, icra etme."],
                ["5. Duruma Uydurma", "Değiştirme, dönüştürme, yeni durumlara adapte etme."],
                ["6. Yaratma", "Kendine özgü bir tarzla yapma, orijinal bir şey ortaya koyma."],
            ]
        ))
    )
    ch2.pages.append(
        ChapterPage(continue_tag="Materyal Hazırlamada 6 Temel İlke")
        .add_block(BulletBlock(1, "Materyal Hazırlamada 6 Temel İlke", [
            "<b>Amaca Uygunluk:</b> Materyal, dersin kazanımlarıyla örtüşmelidir.",
            "<b>Öğrenci Özellikleri:</b> Öğrencinin yaşı, hazır bulunuşluğu ve sosyo-kültürel yapısı dikkate alınmalıdır.",
            "<b>Sadelik:</b> Gösterişten uzak, basit ve anlaşılır olmalıdır.",
            "<b>Odaklayıcılık:</b> Derse odaklanmayı sağlamalı ve öğrenmeyi teşvik etmelidir.",
            "<b>Görsel Ögeler ve Vurgu:</b> Resim, grafik ve renkler önemli noktaları vurgulamak için yeteri kadar kullanılmalıdır.",
            "<b>Öğrenci Aktifliği:</b> Öğrenciye alıştırma ve uygulama imkânı vererek onu aktif kılmalıdır.",
        ]))
        .add_callout(Callout("insight", "Materyal İlkelerinin Ortak Paydası",
            "Altı ilkenin tümü tek bir soruya indirgenebilir: <b>Bu materyal, bu öğrenciye, bu kazanımı en sade ve "
            "en etkin biçimde ulaştırıyor mu?</b> Amaç, öğrenci ve sadelik üçgeni her materyal kararının merkezindedir."))
        .add_summary("Bloom'un taksonomisi; bilişsel, duyuşsal ve psiko-motor alanlarda hedefleri basitten karmaşığa "
            "sıralar. Bu üç alan için hazırlanacak materyaller ise amaca uygunluk, öğrenci özellikleri, sadelik, "
            "odaklayıcılık, görsellik ve öğrenci aktifliği ilkelerine uymalıdır.")
    )

    # =====================================================================
    # BÖLÜM 3 — Görsel Tasarım ve Ders Planları
    # =====================================================================
    ch3 = Chapter(
        number=3,
        title="Görsel Tasarım ve Ders Planları",
        subtitle="Tasarımın temel ögelerinden, ilkelerine ve ders planının beş bölümüne",
        key_terms=[
            KeyTerm("Tasarım Ögesi", "Çizgi, şekil, alan, doku, boyut ve renk gibi bir görselin yapı taşlarını oluşturan temel bileşenler."),
            KeyTerm("Denge (Simetrik/Asimetrik)", "Nesneler arası uyum; simetrik dengede ögeler eşit dağılır, asimetrikte bir taraf diğerinden görsel olarak daha 'dolu'dur."),
            KeyTerm("Vurgu", "Dikkat çekilmek istenen noktaya odaklanılmasını sağlayan tasarım ilkesi."),
            KeyTerm("Kazanım Yazma", "Kazanımların öğretmen değil, öğrenci davranışı olarak yazılması ilkesi."),
        ],
    )
    ch3.pages.append(
        ChapterPage()
        .add_terms(ch3.key_terms)
        .add_table(ComparisonTable(
            "Tasarımı Oluşturan Ögeler",
            ["Öge", "Açıklama"],
            [
                ["Çizgi", "Tek boyutlu görseldir. Yatay çizgiler durgunluk/sakinlik, dikey çizgiler güç/kuvvet hissi verir."],
                ["Şekil", "İki boyutlu biçimlerdir."],
                ["Alan", "Görselin anlaşılabilir olmasını sağlayan boşluk ve yerleşimidir."],
                ["Doku", "Görsele üçüncü boyut hissi katmak için desenlerin kullanılmasıdır."],
                ["Boyut", "Cisimlerin diğer cisimlerle kıyaslanarak büyüklüklerinin algılanmasıdır."],
                ["Renk", "Materyale canlılık katar, dikkat çeker ve iletişimde önemlidir."],
            ]
        ))
        .add_table(ComparisonTable(
            "Görsel Tasarım İlkeleri",
            ["İlke", "Açıklama"],
            [
                ["Denge", "Nesneler arası uyumdur — Simetrik (eşit dağılım) veya Asimetrik (farklı görsel doluluk)."],
                ["Bütünlük", "Ögelerin ilişkili ve bir bütün halinde görünmesidir."],
                ["Yakınlık", "Birbirine yakın duran ögelerin ilişkili algılanmasıdır."],
                ["Vurgu", "Dikkat çekilmek istenen noktaya odaklanılmasını sağlamaktır."],
                ["Hizalama / Ritim", "Gözün bir objeden diğerine rahatça kayabilmesidir."],
            ]
        ))
    )
    ch3.pages.append(
        ChapterPage(continue_tag="Ders Planlarının Bölümleri")
        .add_block(BulletBlock(1, "Ders Planı Nedir?", [
            "Öğretim etkinliklerinin kâğıt üzerinde planlanmasıdır.",
            "<b>Kazanım Yazma:</b> Kazanımlar öğretmen değil, öğrenci davranışı olarak yazılmalıdır. Bir ders için "
            "birden fazla kazanım belirlenebilir ve öğrencinin ne öğreneceği tek tek belirtilmelidir.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("Dersin Kimliği", "Tanıtım"),
            FlowStep("Yöntem/Teknik", "Soru-cevap, tartışma vb."),
            FlowStep("Giriş", "Dikkat çekme, güdüleme"),
            FlowStep("Gelişme", "Konunun işlenmesi"),
            FlowStep("Sonuç", "Özet, ölçme-değerlendirme"),
        ], caption="Ders planının beş temel bölümü."))
        .add_table(ComparisonTable(
            "Giriş ve Sonuç Bölümlerinin Alt Ögeleri",
            ["Bölüm", "Alt Öge", "Açıklama"],
            [
                ["Giriş", "Dikkat Çekme", "Dersin başlangıcıdır."],
                ["Giriş", "Güdüleme", "Dersin öğrenciye ne yarar sağlayacağının açıklanmasıdır."],
                ["Giriş", "Hedeften Haberdar Etme", "Kazanımların öğrenciye duyurulmasıdır."],
                ["Giriş", "Önceki Dersin Hatırlanması", "Önceki konuyla bağlantı kurma / tekrar."],
                ["Sonuç", "Son Özet", "Konunun genel tekrarıdır."],
                ["Sonuç", "Ölçme ve Değerlendirme", "Kazanımlara ulaşılma düzeyinin tespitidir."],
            ]
        ))
        .add_callout(Callout("focus", "Kritik Odak: Gelişme Bölümü",
            "Konunun ayrıntılarıyla işlendiği ana kısımdır. <b>Ara özet</b> ile o ana kadar işlenen kısım özetlenir "
            "— bu, son özetten farklı olarak dersin ortasında yapılır."))
        .add_summary("Görsel tasarım; çizgi, şekil, alan, doku, boyut ve renk gibi ögelerin denge, bütünlük, yakınlık "
            "ve vurgu ilkeleriyle bir araya gelmesidir. Ders planı ise bu ilkelerin sınıfa taşındığı; kimlik, yöntem, "
            "giriş, gelişme ve sonuç bölümlerinden oluşan yazılı bir çerçevedir.")
    )

    # =====================================================================
    # BÖLÜM 4 — Sunu İlkeleri ve Kavram Öğretimi
    # =====================================================================
    ch4 = Chapter(
        number=4,
        title="Sunu İlkeleri ve Kavram Öğretimi",
        subtitle="PowerPoint'in 6x6 kuralından kavram haritalarına ve zihin haritalarına",
        key_terms=[
            KeyTerm("6x6 Kuralı", "Bir sunu sayfasında en fazla 6 satır, her satırda en fazla 6 kelime bulunması ilkesi."),
            KeyTerm("Kavram", "Belli parçaların oluşturduğu bütün; bilgiyi sistematik hale getiren zihinsel unsur."),
            KeyTerm("Kavram Haritası", "Novak'ın (1979) geliştirdiği; anahtar kavramın merkezde olduğu, diğer kavramlarla ilişkilerin gösterildiği görsel bilgi organizasyon aracı."),
            KeyTerm("Kavram Karikatürü", "Naylor ve McMurdo'nun tasarladığı, kavram yanılgılarını ortaya çıkarmayı amaçlayan, genelde 3 karakterin tartıştığı görsel araç."),
        ],
    )
    ch4.pages.append(
        ChapterPage()
        .add_terms(ch4.key_terms)
        .add_table(ComparisonTable(
            "PowerPoint (PPT) Sunu İlkeleri",
            ["İlke", "Açıklama"],
            [
                ["6x6 Kuralı", "Her sayfada en fazla 6 satır, her satırda en fazla 6 kelime."],
                ["Yazı Tipi", "Başlıklar 40–44 punto, metinler 24–28 punto."],
                ["Renk", "Zıtlık ilkesi — zemin koyuysa yazı açık, zemin açıksa yazı koyu olmalı."],
                ["Görsellik", "Konuyu destekleyen görsel kullanılmalı ama sayfa boğulmamalı."],
                ["İçerik", "Kitabın aynısı olmamalı; özet ve anahtar kelimeler içermeli."],
            ]
        ))
        .add_block(BulletBlock(1, "Kavram Öğretimi", [
            "<b>Kavram:</b> Belli parçaların oluşturduğu bütündür; bilgiyi sistematik hale getiren unsurdur.",
            "<b>Yararları:</b> İletişimi kolaylaştırır, soyut düşünceyi somutlaştırır, zihinsel gelişime katkı sağlar.",
            "<b>Aşamaları:</b> Planlama, Uygulama, Değerlendirme.",
        ]))
    )
    ch4.pages.append(
        ChapterPage(continue_tag="Kavram Öğretim Araçları")
        .add_table(ComparisonTable(
            "Kavram Öğretim Araçları",
            ["Araç", "Açıklama"],
            [
                ["Kavram Ağları (Şematik Ağ)", "İlişkili bilgilerin kategorize edildiği görsel haritalardır."],
                ["Anlam Çözümleme Tabloları (ACT)", "İki boyutlu çizelgelerdir; varlıkların özelliklerini ayırt etmek için kullanılır (ör. Müslüman bilim adamları ve alanları tablosu)."],
                ["Kavram Haritaları", "Novak (1979) geliştirmiştir. Anahtar kavram merkezdedir; diğer kavramlarla ilişkiler gösterilir, bilgiyi organize edip somutlaştırır."],
                ["Kavram Karikatürü", "Naylor ve McMurdo tasarlamıştır. Amaç güldürmek değil kavram yanılgılarını ortaya çıkarmaktır; genelde 3 karakterden biri doğruyu, diğerleri yaygın yanlışları savunur."],
                ["Zihin Haritaları", "Sperry'nin beyin (sağ/sol lob) araştırmalarına dayanır; analitik ve görsel zekâyı aynı anda çalıştırır."],
            ]
        ))
        .add_callout(Callout("caution", "Dikkat: Kavram Haritası Türleri",
            "Kavram haritalarının başlıca türleri: Akış Çizgesi, Dönen Diyagramlar, Dayandırılabilir Ağaçlar, "
            "Örümcek Ağı, Hiyerarşik Harita, Sistemler Haritası, Zincir Haritası ve <b>Balık Kılçığı</b>."))
        .add_summary("Etkili bir sununun temeli 6x6 kuralı, punto ve renk kontrastı ilkeleridir. Kavram öğretimi ise "
            "soyut bilgiyi somutlaştırmayı hedefler; kavram ağları, ACT, kavram haritaları, kavram karikatürü ve "
            "zihin haritaları bu amaçla kullanılan başlıca araçlardır.")
    )

    # =====================================================================
    # BÖLÜM 5 — Görsel ve Etkinlik Materyalleri
    # =====================================================================
    ch5 = Chapter(
        number=5,
        title="Görsel ve Etkinlik Materyalleri",
        subtitle="Resim, karikatür ve afişten bulmacalara; materyal hazırlamanın genel ilkeleriyle kapanış",
        key_terms=[
            KeyTerm("İçerik Analizi", "Bir görselin konusuyla ilişkisini incelemeye yönelik analiz kavramı."),
            KeyTerm("Karikatür", "Sanat (çizim), Fikir (mesaj) ve Mizah (araç) unsurlarını bir arada barındıran, düşüncenin mizahla yoğrulmasıyla oluşan görsel."),
            KeyTerm("Afiş", "Tek anlama sahip, hatırlanabilir; mesaj, imge ve sözel unsurdan oluşan sunum materyali."),
            KeyTerm("Çalışma Yaprağı", "Çoktan seçmeli, açık uçlu, eşleştirme gibi çeşitli etkinlik türlerini barındıran etkinlik materyali."),
        ],
    )
    ch5.pages.append(
        ChapterPage()
        .add_terms(ch5.key_terms)
        .add_block(BulletBlock(1, "Resim Materyalleri", [
            "Paint/Photoshop gibi araçlarla öğrenciler kendi materyallerini üretebilir.",
            "<b>Hareket Özelliği:</b> Durağan, hareketli (animated gif) ve hareket hissi veren durağan resimler olarak ayrılır.",
        ]))
        .add_table(ComparisonTable(
            "Resim Analiz Kavramları",
            ["Kavram", "Açıklama"],
            [
                ["İç Konsantrasyon", "Resmin olumlu/olumsuz etkilerini ortaya koymaktır."],
                ["İçerik Analizi", "Konu ile ilişkiyi incelemektir."],
                ["Resimle Bütünleşme", "Resmin içine dalıp hissetmektir."],
            ]
        ))
        .add_info_cards("Karikatürün Üç Unsuru", [
            InfoCard("Sanat", "Çizim yeteneğidir.", "1"),
            InfoCard("Fikir", "Verilmek istenen mesajdır.", "2"),
            InfoCard("Mizah", "Mesajı iletme aracıdır — mizah yoksa karikatür sayılmaz.", "3"),
        ])
    )
    ch5.pages.append(
        ChapterPage(continue_tag="Afişler ve Etkinlik Materyalleri")
        .add_table(ComparisonTable(
            "Afişler",
            ["Unsur / Tür", "Açıklama"],
            [
                ["Sosyal Afiş", "Toplumu bilgilendirme amaçlıdır."],
                ["Kültürel Afiş", "Etkinlik duyurusu amaçlıdır."],
                ["Reklam Afişi", "Ürün tanıtımı amaçlıdır."],
                ["Mesaj / İmge / Sözel Unsur", "Sırasıyla ana fikir, yardımcı görsel ve slogan-başlık-ayet/hadis gibi metinlerdir."],
            ]
        ))
        .add_block(BulletBlock(2, "Etkinlik Materyalleri", [
            "<b>Bulmacalar:</b> Aktif ve kalıcı öğrenme sağlar, merak uyandırır.",
            "<b>Çalışma Yaprağı Etkinlik Listesi:</b> Çoktan seçmeli, açık uçlu, doğru/yanlış, eşleştirme, boşluk "
            "doldurma, sıraya koyma, 5N1K, A'dan Z'ye etkinlikleri, boyama, broşürler vb.",
        ]))
    )
    ch5.pages.append(
        ChapterPage(continue_tag="Materyal Hazırlama İlkeleri — Genel Özet")
        .add_table(ComparisonTable(
            "Materyal Hazırlama İlkeleri — Genel Özet",
            ["İlke", "Açıklama"],
            [
                ["Amaç ve Kazanıma Uygunluk", "Materyal dersin kazanımıyla örtüşmelidir."],
                ["Öğrenci Seviyesine Uygunluk", "Yaş ve hazır bulunuşluk dikkate alınmalıdır."],
                ["Basitlik ve Sadelik", "Gösterişten uzak olmalıdır."],
                ["Vurgu Kullanımı", "Renk, çizgi gibi ögelerle önemli noktalar vurgulanmalıdır."],
                ["Öğrenciyi Aktif Kılması", "Uygulama imkânı vermelidir."],
                ["Gerçek Hayatla İlişki", "Hayatilik taşımalıdır."],
                ["Dayanıklılık ve Güncellenebilirlik", "Uzun süre kullanılabilir olmalıdır."],
                ["Kullanım Yönergesinin Olması", "Nasıl kullanılacağı açık olmalıdır."],
            ]
        ))
        .add_summary("Görsel materyaller (resim, karikatür, afiş) ile etkinlik materyalleri (bulmaca, çalışma "
            "yaprağı), kavramları somutlaştıran ve öğrenciyi aktif kılan araçlardır. Tüm materyal hazırlama süreci "
            "nihayetinde amaca uygunluk, sadelik, vurgu, aktiflik, hayatilik, dayanıklılık ve yönerge ilkelerinde birleşir.")
    )

    chapters = [ch1, ch2, ch3, ch4, ch5]

    # =====================================================================
    # SÖZLÜK
    # =====================================================================
    glossary = [
        Concept("Materyal", "Öğrenme-öğretme sürecinde yardımcı olan her türlü eğitsel belge.", "Materyal Kavramı", 1),
        Concept("Yaşantı Piramidi", "Duyu organı sayısı arttıkça öğrenme kalitesinin artması ilkesi.", "Edgar Dale", 1),
        Concept("Yapılandırmacı Yaklaşım", "Bilginin öğrenci zihninde kendisince yapılandırılması.", "Eğitimsel Yaklaşımlar", 1),
        Concept("Uzak Hedef", "Devletin eğitim politikası ve felsefesi.", "Hedeflerin Sınıflandırılması", 1),
        Concept("Genel Hedef", "Okulların (kurumların) hedefleri.", "Hedeflerin Sınıflandırılması", 1),
        Concept("Özel Hedef", "Her bir derse özgü hedef.", "Hedeflerin Sınıflandırılması", 1),
        Concept("Taksonomi", "Hedefleri basitten karmaşığa sıralayan sınıflandırma.", "Bloom", 2),
        Concept("Bilişsel Amaç", "Bilgi, kavrama, uygulama, analiz, sentez, değerlendirme düzeyleri.", "Bloom", 2),
        Concept("Duyuşsal Amaç", "Alma, tepkide bulunma, değer verme, örgütleme, kişilik düzeyleri.", "Bloom", 2),
        Concept("Psiko-motor Amaç", "Uyarılma, hazır olma, taklit, beceri haline getirme, yaratma düzeyleri.", "Bloom", 2),
        Concept("Çizgi", "Tek boyutlu görsel; yatay durgunluk, dikey güç hissi verir.", "Tasarım Ögeleri", 3),
        Concept("Denge", "Nesneler arası uyum; simetrik veya asimetrik olabilir.", "Tasarım İlkeleri", 3),
        Concept("Vurgu", "Dikkat çekilmek istenen noktaya odaklanma.", "Tasarım İlkeleri", 3),
        Concept("Kazanım Yazma", "Kazanımların öğrenci davranışı olarak yazılması.", "Ders Planı", 3),
        Concept("Ara Özet", "Gelişme bölümünde o ana kadarki kısmın özetlenmesi.", "Ders Planı", 3),
        Concept("6x6 Kuralı", "Sunuda en fazla 6 satır, satırda en fazla 6 kelime.", "PPT İlkeleri", 4),
        Concept("Kavram Haritası", "Novak'ın (1979) geliştirdiği, anahtar kavram merkezli görsel bilgi organizasyonu.", "Kavram Öğretimi", 4),
        Concept("Kavram Karikatürü", "Naylor ve McMurdo'nun kavram yanılgılarını ortaya çıkarma aracı.", "Kavram Öğretimi", 4),
        Concept("Zihin Haritası", "Sperry'nin beyin araştırmalarına dayanan, analitik ve görsel zekâyı birleştiren araç.", "Kavram Öğretimi", 4),
        Concept("Anlam Çözümleme Tablosu (ACT)", "Varlıkların özelliklerini ayırt etmek için kullanılan iki boyutlu çizelge.", "Kavram Öğretimi", 4),
        Concept("İçerik Analizi", "Görselin konusuyla ilişkisini inceleme.", "Resim Materyalleri", 5),
        Concept("Karikatür", "Sanat, fikir ve mizah unsurlarını barındıran görsel.", "Görsel Materyaller", 5),
        Concept("Afiş", "Mesaj, imge ve sözel unsurdan oluşan tek-anlamlı sunum materyali.", "Görsel Materyaller", 5),
    ]

    # =====================================================================
    # SINAV HAZIRLIK
    # =====================================================================
    distinctions = [
        DistinctionPair("Uzak Hedef", "Özel Hedef", "Uzak hedef devletin eğitim felsefesidir; özel hedef her bir dersin kendine ait, somut hedefidir."),
        DistinctionPair("Bilişsel Amaç", "Psiko-motor Amaç", "Bilişsel amaç zihinsel süreçleri (bilgi-kavrama-analiz), psiko-motor amaç bedensel becerileri (taklit-icra) hedefler."),
        DistinctionPair("Simetrik Denge", "Asimetrik Denge", "Simetrik dengede ögeler eşit dağılır; asimetrik dengede bir taraf diğerinden görsel olarak daha 'dolu'dur."),
        DistinctionPair("Ara Özet", "Son Özet", "Ara özet gelişme bölümünde ara sırada yapılır; son özet dersin sonundaki genel tekrardır."),
        DistinctionPair("Kavram Haritası", "Zihin Haritası", "Kavram haritası Novak'ın bilgiyi hiyerarşik organize eden aracıdır; zihin haritası Sperry'nin sağ-sol lobu birlikte çalıştıran aracıdır."),
        DistinctionPair("Kavram Karikatürü", "Karikatür", "Kavram karikatürü kavram yanılgısını ortaya çıkarmayı hedefler; genel karikatür sanat-fikir-mizah üçlüsüyle mesaj iletir."),
    ]

    match_table = [
        MatchRow("Edgar Dale", "Yaşantı (Deneyim) Piramidi", "Yaparak-yaşayarak öğrenme %90 hatırlanır"),
        MatchRow("Benjamin Bloom", "Amaçlar Taksonomisi", "Bilişsel-Duyuşsal-Psikomotor, basitten karmaşığa"),
        MatchRow("Joseph Novak", "Kavram Haritaları (1979)", "Anahtar kavram merkezde, ilişkiler etrafında"),
        MatchRow("Naylor ve McMurdo", "Kavram Karikatürü", "3 karakter tartışır, kavram yanılgısını ortaya çıkarır"),
        MatchRow("Roger Sperry", "Zihin Haritalarının bilimsel temeli", "Sağ-sol lob (beyin) araştırmaları"),
    ]

    qa_items = [
        QAItem("Dale'e göre yapıp-söylediklerimizin yüzde kaçını hatırlarız?", "%90 — en kalıcı öğrenme yaparak-yaşayarak gerçekleşir."),
        QAItem("Eğitimsel yaklaşımların 4 temel unsuru nedir?", "Yapılandırmacı yaklaşım, çoklu zeka, öğrenci merkezlilik, etkinlik ve materyal."),
        QAItem("Bloom'un bilişsel amaçlar sıralamasında en üst düzey hangisidir?", "Değerlendirme — yargılama, hüküm verme, kritize etme."),
        QAItem("Materyal hazırlamada dikkat edilmesi gereken 6 temel ilke nedir?", "Amaca uygunluk, öğrenci özellikleri, sadelik, odaklayıcılık, görsel ögeler, öğrenci aktifliği."),
        QAItem("Yatay ve dikey çizgiler hangi hissi verir?", "Yatay çizgi durgunluk/sakinlik, dikey çizgi güç/kuvvet hissi verir."),
        QAItem("Ders planının 5 bölümü nedir?", "Dersin kimliği, yöntem ve teknikler, giriş, gelişme, sonuç."),
        QAItem("PowerPoint'te 6x6 kuralı nedir?", "Her sayfada en fazla 6 satır, her satırda en fazla 6 kelime."),
        QAItem("Kavram haritalarını kim ve ne zaman geliştirmiştir?", "Joseph Novak, 1979."),
        QAItem("Karikatürün üç unsuru nedir?", "Sanat (çizim), Fikir (mesaj), Mizah (araç)."),
        QAItem("Afişin üç unsuru nedir?", "Mesaj (ana fikir), İmge (yardımcı görsel), Sözel Unsur (slogan/başlık)."),
    ]

    checklist = [
        "Materyalin tanımını ve bilişsel-duyuşsal-psikomotor yararlarını açıklayabiliyorum.",
        "Dale'in Yaşantı Piramidi'ndeki öğrenme oranlarını sıralayabiliyorum.",
        "Eğitimsel yaklaşımların 4 unsurunu ve hedef sınıflandırmasını (uzak-genel-özel) biliyorum.",
        "Bloom'un bilişsel, duyuşsal ve psiko-motor amaçlarını düzeyleriyle sıralayabiliyorum.",
        "Materyal hazırlamanın 6 temel ilkesini sayabiliyorum.",
        "Tasarım ögelerini (çizgi, şekil, alan, doku, boyut, renk) ve ilkelerini ayırt edebiliyorum.",
        "Ders planının 5 bölümünü ve giriş/sonuç alt ögelerini biliyorum.",
        "PPT 6x6 kuralını ve kavram öğretim araçlarını (harita, karikatür, ACT) ayırt edebiliyorum.",
        "Karikatür ve afişin unsurlarını sayabiliyorum.",
        "Materyal hazırlamanın genel özet ilkelerini (8 madde) açıklayabiliyorum.",
    ]

    return CoursePack(
        course_code="ÖĞR. TEKNOLOJİLERİ",
        title='Öğretim <span class="accent-word">Teknolojileri</span>',
        subtitle="Materyal Tasarımından Kavram Öğretimine Bütüncül Bakış",
        description=(
            "Eğitim materyalinin tanımından Dale'in Yaşantı Piramidi'ne, Bloom'un taksonomisinden görsel tasarım "
            "ilkelerine; ders planlarından kavram haritalarına uzanan final sınavı özeti."
        ),
        theme="slate",
        icon_text="Ö",
        chapters=chapters,
        glossary=glossary,
        distinctions=distinctions,
        match_table=match_table,
        qa_items=qa_items,
        overview_lead=(
            "Bu ders; etkili bir eğitim materyalinin <b>kuramsal temellerinden</b> (Dale, Bloom) <b>somut tasarım "
            "ilkelerine</b> (görsel tasarım, ders planı, sunu, kavram haritaları) uzanan bütüncül bir çerçeve sunar."
        ),
        overview_cards=[
            {"title": "Materyal ve Piramit", "text": "Materyal tanımı, Dale'in öğrenme oranları ve eğitimsel yaklaşımlar."},
            {"title": "Bloom Taksonomisi", "text": "Bilişsel, duyuşsal, psiko-motor amaçlar ve materyal ilkeleri."},
            {"title": "Görsel Tasarım", "text": "Tasarım ögeleri, ilkeleri ve ders planının beş bölümü."},
            {"title": "Sunu ve Kavram Öğretimi", "text": "PPT 6x6 kuralı, kavram haritaları ve kavram karikatürü."},
            {"title": "Görsel Materyaller", "text": "Resim, karikatür ve afiş analizleri."},
            {"title": "Etkinlik Materyalleri", "text": "Bulmacalar, çalışma yaprakları ve genel hazırlama ilkeleri."},
        ],
        overview_flow=[
            ("Kuram", "Dale / Bloom"),
            ("Tasarım", "Ögeler / ilkeler"),
            ("Uygulama", "Ders planı / sunu"),
            ("Materyal", "Görsel / etkinlik"),
        ],
        overview_note=(
            "Sınavda en çok karıştırılan yer, <b>Bloom'un üç amaç alanının basitten karmaşığa sıralamasıdır:</b> "
            "bilişsel (bilgi→değerlendirme), duyuşsal (alma→kişilik) ve psiko-motor (uyarılma→yaratma) düzeyleri "
            "birbirine karıştırılmamalıdır."
        ),
    )
