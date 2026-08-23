# -*- coding: utf-8 -*-
"""TÜRK İSLAM SANAT TARİHİ — Görsel Ders Notu Kitabı, içerik tanımı.
Kaynak: 'İSLAM SANAT TARİHİ ÖZET.pdf' (ham metin özet, 7 sayfa).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from content_model import (
    Person, KeyTerm, Callout, FlowStep, FlowDiagram, ComparisonTable,
    InfoCard, BulletBlock, Chapter, ChapterPage, Concept, CoursePack,
    QAItem, DistinctionPair, MatchRow,
)


def get_pack() -> CoursePack:

    # =====================================================================
    # BÖLÜM 1 — Orta Asya'da Türk-İslam Sanatına Giriş
    # =====================================================================
    ch1 = Chapter(
        number=1,
        title="Orta Asya'da Türk-İslam Sanatına Giriş",
        subtitle="İslamlaşma sürecinden ilk Türk-İslam mimarisinin özgün karakterine",
        key_terms=[
            KeyTerm("Talas Savaşı (751)", "Karluk Türklerinin Araplara yardımıyla Çin'in mağlup edildiği, Türklerin İslamlaşmasına giden yolu açan dönüm noktası."),
            KeyTerm("Kitlevi Geçiş", "10. yüzyılda Oğuzların Müslüman olmasıyla başlayan, Türklerin Sünni Hanefiliği tercih ettiği yeni dönem."),
            KeyTerm("Kübik Yapı Anlayışı", "Uygur mezar mimarisinden gelen etkiyle ilk Türk-İslam eserlerinde görülen mimari yenilik."),
            KeyTerm("Silindirik Minare", "İlk Türk-İslam mimarisinde ortaya çıkan, sonraki dönemlerde gelişecek özgün minare formu."),
        ],
    )
    ch1.pages.append(
        ChapterPage()
        .add_terms(ch1.key_terms)
        .add_block(BulletBlock(1, "Tarihsel Dönüşüm ve İslamlaşma", [
            "<b>İlişkiler:</b> Hz. Ömer (ra) döneminde başlayan temaslar, Emeviler döneminde gergin geçmiş, Abbasiler "
            "döneminde yumuşamıştır.",
            "<b>Talas Savaşı (751):</b> Müslüman Arap orduları ile Çin arasındaki bu savaşta, Karluk Türklerinin "
            "Araplara yardım etmesiyle Çin mağlup edilmiştir. Bu olay, Türklerin Müslüman olmasına giden yolu açan "
            "tarihi bir dönüm noktasıdır.",
            "<b>Kitlevi Geçiş:</b> 10. yüzyılda Oğuzların Müslüman olmasıyla Türk tarihinde yeni bir dönem "
            "başlamıştır. Türkler, İslam'ın Sünni Hanefilik yorumunu tercih etmişlerdir.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("İlk Temaslar", "Hz. Ömer dönemi"),
            FlowStep("Gerginlik", "Emeviler dönemi"),
            FlowStep("Yumuşama", "Abbasiler dönemi"),
            FlowStep("Talas Savaşı", "751 — dönüm noktası"),
            FlowStep("Kitlevi Geçiş", "10. yy — Oğuzlar"),
        ], caption="Türklerin İslamlaşma süreci, aşama aşama."))
        .add_block(BulletBlock(2, "İlk Türk-İslam Sanatı Özellikleri", [
            "Türklerin İslamiyeti kabul ettikten sonra verdikleri ilk eserlerde, göçebelikten gelen özgür tutumun ve "
            "özgünlüğün izleri görülür. Bu dönemin mimarisinde göze çarpan üç temel yenilik şöyledir:",
        ]))
        .add_table(ComparisonTable(
            "İlk Dönem Mimarisinin Üç Temel Yeniliği",
            ["Yenilik", "Açıklama"],
            [
                ["Kübik Yapı Anlayışı", "Uygur mezar mimarisinden gelen etkiyle biçimlenmiştir."],
                ["Silindirik Minare Formu", "Sonraki dönemlerde 'Doğu Minareleri' olarak gelişecek ilk örnekleridir."],
                ["Medrese Mimarisi", "İlk örneklerin ortaya çıkışı bu döneme rastlar."],
            ]
        ))
    )
    ch1.pages.append(
        ChapterPage()
        .add_summary("Türklerin İslamlaşması, Hz. Ömer döneminden başlayıp Talas Savaşı (751) ile dönüm noktasına "
            "ulaşan, 10. yüzyılda Oğuzların kitlevi geçişiyle tamamlanan bir süreçtir. Bu sürecin ürünü olan ilk "
            "Türk-İslam eserleri, göçebe geleneğin özgünlüğünü kübik yapı, silindirik minare ve ilk medrese "
            "örnekleriyle mimariye taşımıştır.")
    )

    # =====================================================================
    # BÖLÜM 2 — Karahanlı Devri Mimarisi (960-1212)
    # =====================================================================
    ch2 = Chapter(
        number=2,
        title="Karahanlı Devri Mimarisi",
        subtitle="960-1212 · Orta Asya'nın ilk Müslüman Türk devletinde cami, minare, türbe ve kervansaray",
        key_terms=[
            KeyTerm("Çifte Hakimiyet", "Karahanlıların eski Türk geleneğine bağlı olarak Doğu ve Batı olmak üzere ikili sistemle yönetilmesi."),
            KeyTerm("Merkezi Kubbe Şeması", "Hazara Degaron Camii'nde görülen, ortada ana kubbe ve köşelerde küçük kubbelerden oluşan; Osmanlı cami mimarisine öncülük eden plan tipi."),
            KeyTerm("Doğu Minareleri", "Türklerin Orta Asya'da geliştirdiği; silindirik, tuğla, cami kütlesinden bağımsız yeni minare tipi."),
            KeyTerm("Ribat", "Güvenlik ve konaklama amaçlı inşa edilen, kale görünümlü kervansaray yapıları."),
        ],
    )
    ch2.pages.append(
        ChapterPage()
        .add_terms(ch2.key_terms)
        .add_block(BulletBlock(1, "Tarihsel ve Kültürel Çerçeve", [
            "<b>Siyasi Tarih:</b> Karahanlılar (840-1212), Orta Asya'da kurulan ilk Müslüman Türk devleti olarak "
            "kabul edilir. Eski Türk geleneklerine bağlı kalarak 'çifte hakimiyet' (Doğu ve Batı) sistemiyle "
            "yönetilmişlerdir.",
            "<b>İslamlaşma Süreci:</b> Hükümdarları Satuk Buğra Han'ın (ö. 955) İslamiyet'i kabul etmesiyle devlet "
            "büyük bir değişim yaşamış ve Türkler büyük topluluklar halinde İslamiyet'e girmiştir.",
        ]))
        .add_info_cards("Dönemin Kültürel Şahsiyetleri", [
            InfoCard("Yusuf Has Hacip", "Kutadgu Bilig'in yazarıdır.", "1"),
            InfoCard("Kaşgarlı Mahmut", "Divân-ı Lügâti't-Türk'ün yazarıdır.", "2"),
            InfoCard("Fârâbî", "Büyük İslam filozofudur.", "3"),
        ])
        .add_table(ComparisonTable(
            "Cami Mimarisi — Öne Çıkan Üç Örnek",
            ["Eser", "Özellik"],
            [
                ["Hazara Degaron Camii (XI. yy)", "Semerkant yakınında; klasik Arap camilerinin aksine kare planlı, 'Merkezi Kubbe' şemalı — bu şema ileride Osmanlı cami mimarisinde gelişecektir."],
                ["Talhatan Baba Camii (XI-XII. yy)", "Tamamı tuğladan; merkezi kubbenin çapraz tonozlarla genişletildiği 'enine cami planı' — Edirne Üç Şerefeli Camii'ni çağrıştırır."],
                ["Buhara Muğak Attari Camii (XII. yy)", "Cephe düzeni (geometrik/bitkisel süsleme, taç kapı) Anadolu Selçuklu camilerini hatırlatır; büyük bir geleneğin başlangıcıdır."],
            ]
        ))
    )
    ch2.pages.append(
        ChapterPage()
        .add_block(BulletBlock(2, "Minare Mimarisi — 'Doğu Minareleri'", [
            "Erken devir Arap minarelerinin (kilise çan kulelerini andıran kare/çokgen kuleler) aksine, Türkler Orta "
            "Asya'da yeni bir tip geliştirmiştir: genellikle tuğla malzemeli, silindirik formlu ve yukarı doğru "
            "incelen, cami kütlesinden bağımsız inşa edilen, gövdesi geometrik-bitkisel motifler ve yazı "
            "kuşaklarıyla süslenen minareler.",
        ]))
        .add_table(ComparisonTable(
            "Önemli Doğu Minaresi Örnekleri",
            ["Eser", "Tarih"],
            [
                ["Özkent Minaresi", "XI. yüzyıl"],
                ["Buhara Kalan (Kalyan) Minaresi", "1127"],
                ["Vabkent Minaresi", "1197"],
                ["Gazne Sultan Mesut Minaresi", "1100"],
                ["Delhi Kutub Minar", "1206"],
            ]
        ))
        .add_block(BulletBlock(3, "Türbe Mimarisi", [
            "Karahanlı türbeleri genellikle tuğla malzemelidir; süslemelerde alçı (stuk) ve bazen çini kullanılır. "
            "Kare veya kareye yakın bir alt mekan üzerine oturan kubbe ana taslağı oluşturur.",
            "<b>Cephe ve Portal:</b> Kubbe kasnağından daha yükseğe çıkan portal (taç kapı), yapıya heybetli bir "
            "görünüm kazandırır; girintili-çıkıntılı hacim oyunları karakteristiktir.",
        ]))
        .add_callout(Callout("focus", "Önemli Türbe Örnekleri",
            "Tim'de <b>Arap Atâ Türbesi</b> (978) · Talas'ta <b>Ayşe Bibi Türbesi</b> (XII. yy) · Özkent'te "
            "<b>Nasr bin Ali</b> (1012), <b>Celaleddin Hüseyin</b> (1152) ve <b>Muhammed bin Nasr</b> (1187) türbeleri."))
        .add_block(BulletBlock(4, "Medrese Mimarisi", [
            "Eyvanlı medreselerin bilinen ilk örneklerinin Karahanlılar döneminde ortaya çıktığı tahmin edilmektedir.",
        ]))
        .add_block(BulletBlock(5, "Kervansaray (Ribat) Mimarisi", [
            "Türk mimarisinin en eski kervansaray örneklerine bu dönemde rastlanır. 'Ribat' adı verilen bu yapılar "
            "güvenlik ve konaklama amaçlıdır. Kerpiç ve tuğla kullanılır; kare veya dikdörtgen planlıdır. Ortada "
            "bir avlu ve etrafında kubbe/tonozlu kapalı mekanlar bulunur; dış cepheleri kale görünümünde sağlamdır.",
        ]))
    )
    ch2.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Ribât-ı Melik (1078) — Öne Çıkan Örnek",
            ["Özellik", "Açıklama"],
            [
                ["Bani", "Karahanlı hükümdarı Nasr bin İbrahim, Buhara-Semerkant yolu üzerinde yaptırmıştır."],
                ["Mimari", "Kare planlı, kerpiç ve tuğla malzemeli; ortada avlu, çevresinde tonozlu odalar."],
                ["Cephe Düzeni", "Dış duvarlarında yarım silindir biçimli yivler ve köşe kuleleri — kale görüntüsü verir."],
                ["Önemi", "Sivri kemerli giriş portalı, Türk mimarisinin klasik taç kapı anlayışını erken bir dönemde ortaya koyar."],
            ]
        ))
        .add_summary("Karahanlılar, Orta Asya'nın ilk Müslüman Türk devleti olarak cami, minare, türbe, medrese ve "
            "kervansaray mimarisinde özgün bir dil kurmuştur. Hazara Degaron'un merkezi kubbe şeması ve Ribât-ı "
            "Melik'in taç kapı anlayışı, sonraki Türk-İslam mimarisinin temel referans noktaları olmuştur.")
    )

    # =====================================================================
    # BÖLÜM 3 — Gazneliler Devri Mimarisi (962-1186)
    # =====================================================================
    ch3 = Chapter(
        number=3,
        title="Gazneliler Devri Mimarisi",
        subtitle="962-1186 · Fars kültürünün etkisindeki Türk devletinde cami, minare ve saray sanatı",
        key_terms=[
            KeyTerm("Leşkergâh Sarayı", "Afganistan'da, dört eyvanlı ve avlulu plana sahip; fresklerinde Türk tipi insan yüzü betimlenen Gazneli saray yapısı."),
            KeyTerm("Kûfi Yazı", "Gazneli minarelerinin gövdesinde geometrik ve bitkisel süslemelerle birlikte kullanılan erken dönem Arap yazı stili."),
            KeyTerm("Fresk", "Duvar üzerine yapılan resim tekniği; Leşkergâh Sarayı'nda Türk tipi yüz ve kıyafetlerin betimlendiği sanat formu."),
            KeyTerm("Stuko", "Saray ve yapı süslemelerinde kullanılan alçı işçiliği tekniği."),
        ],
    )
    ch3.pages.append(
        ChapterPage()
        .add_terms(ch3.key_terms)
        .add_block(BulletBlock(1, "Tarihsel ve Kültürel Arka Plan", [
            "<b>Kuruluş:</b> Samani devletinde ordu komutanı olan Memluk Türklerinden Alp Tekin'in, Gazne şehrini "
            "başkent yaparak yönetimi ele almasıyla kurulmuştur.",
            "<b>Coğrafya:</b> Maverâünnehir, Horasan ve Hindistan'ın kuzeyinde hüküm sürmüşlerdir.",
            "<b>Kültürel Etkileşim:</b> Bir Türk devleti olmasına rağmen, yerine geçtikleri Samani devletinin "
            "etkisiyle Fars (İran) kültürü sosyal yaşamda oldukça etkili olmuştur.",
        ]))
        .add_table(ComparisonTable(
            "Cami ve Minare Mimarisi",
            ["Eser", "Özellik"],
            [
                ["Leşkeri Bazar Ulu Camii (XI. yy)", "86×11 m, enine dikdörtgen planlı; sıcak hava nedeniyle avluya bakan kenarları açık bırakılmıştır. Bu tarz daha sonra Delhi Cuma Mescidi'nde de görülür."],
                ["Gazneli Mahmut III Minaresi", "48 m boyunda; alt kademe taş kaide üzerinde sekiz köşeli yıldız biçimli tuğla, üst kademe silindirik (deprem nedeniyle yıkılmış). Gövdesinde Kûfi yazılar ve süslemeler yer alır."],
            ]
        ))
        .add_block(BulletBlock(2, "Saray Mimarisi (Sivil Mimari)", [
            "Gazneliler sivil mimaride, özellikle saray yapımında önemli eserler bırakmışlardır.",
        ]))
    )
    ch3.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Öne Çıkan Saray Yapıları",
            ["Eser", "Özellik"],
            [
                ["Leşkergâh Sarayı (XI. yy başı)", "Helmand nehri yakınında, dört eyvanlı ve avlulu; kerpiç-tuğla, stuko ve terrakota işçiliği. Taht salonu fresklerinde Türk tipi yüz (yuvarlak yüz, çekik göz) ve kıyafetler betimlenir — Uygur duvar resimleriyle benzerlik gösterir."],
                ["Sultan Mesut III Sarayı (1112)", "Gazne'de, dört eyvanlı ve avlulu; 250 m uzunluğunda mermer kaplama (friz) ve dilimli kemerlerden oluşan süslemeleriyle Leşkeri Bazar'dan daha gösterişlidir."],
            ]
        ))
        .add_block(BulletBlock(3, "Kervansaray ve Diğer Yapılar", [
            "<b>Ribât-ı Mâhî (1020):</b> İran-Türkmenistan yolu üzerinde; kare planlı, dört eyvanlı, kale gibi "
            "müstahkem cepheli. Eyvanlarda kubbe kullanımıyla Gazneli üslubunu yansıtır; Karahanlı ile Büyük "
            "Selçuklu kervansarayları arasında bir geçiş dönemi eseridir.",
            "<b>Medreseler:</b> Varlığı bilinmekle birlikte günümüze ulaşan kalıntı yoktur.",
            "<b>Türbeler:</b> Çok gelişmiş örnekleri yoktur; Sultan Mahmut ve Aslan Câzip türbeleri dönemin bilinen "
            "yegane mezar yapılarıdır.",
        ]))
        .add_summary("Gazneliler, Fars kültürünün güçlü etkisi altında; Leşkeri Bazar Camii, Sultan Mahmut III "
            "Minaresi ve özellikle Leşkergâh ile Sultan Mesut III saraylarıyla sivil mimaride öne çıkmıştır. "
            "Fresklerdeki Türk tipi betimlemeler, dönemin kültürel kimliğinin görsel izidir.")
    )

    # =====================================================================
    # BÖLÜM 4 — Hindistan'da Türk Mimarisi (XI-XIX. yy)
    # =====================================================================
    ch4 = Chapter(
        number=4,
        title="Hindistan'da Türk Mimarisi",
        subtitle="XI-XIX. yüzyıl · Dokuz asırlık hakimiyetin bıraktığı anıtsal miras",
        key_terms=[
            KeyTerm("Delhi Türk Sultanlığı", "Gaznelilerden sonra Hindistan'da Türk hakimiyetini sürdüren siyasi yapı."),
            KeyTerm("Babürlüler (Mughals)", "Delhi Türk Sultanlığı'ndan sonra Hindistan'da hüküm süren, Tac Mahal gibi eserlerin sahibi Türk-Moğol hanedanı."),
            KeyTerm("Kutup Minar", "Kuvvetü'l-İslam Camii'ne sonradan eklenen, 1229 tarihli anıtsal minare."),
            KeyTerm("Tac Mahal", "1648 tarihli, Agra'da bulunan ve Babürlü mimarisinin zirvesi sayılan anıt mezar."),
        ],
    )
    ch4.pages.append(
        ChapterPage()
        .add_terms(ch4.key_terms)
        .add_block(BulletBlock(1, "İslamiyet'in Yayılışı ve Türk Hakimiyeti", [
            "<b>Başlangıç:</b> İslamiyet Hindistan'a ilk kez 712 yılında Araplar eliyle ulaşmış olsa da, asıl kalıcı "
            "ve etkin hakimiyet 11. yüzyıldan itibaren Türkler (Gazneliler) eliyle başlamıştır.",
            "<b>Süreç:</b> Gazneliler, Delhi Türk Sultanlığı ve Babürlüler (Mughals) dönemleri boyunca, 1858'de "
            "İngiliz sömürgesi olana kadar yaklaşık 9 asır boyunca İslam kültürü bölgeye hakim olmuştur.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("712", "Arapların ilk teması"),
            FlowStep("XI. yy", "Gazneli hakimiyeti"),
            FlowStep("Delhi Sultanlığı", "Kalıcı Türk hakimiyeti"),
            FlowStep("Babürlüler", "Mimari zirve"),
            FlowStep("1858", "İngiliz sömürgesi"),
        ], caption="Hindistan'da Türk-İslam hakimiyetinin yaklaşık 9 asırlık seyri."))
        .add_table(ComparisonTable(
            "Önemli Eserler",
            ["Eser", "Tarih", "Not"],
            [
                ["Kuvvetü'l-İslam Camii", "1193", "Delhi Sultanlarından Kutbettin Aybek tarafından yaptırılmıştır."],
                ["Kutup Minar", "1229", "Kuvvetü'l-İslam Camii'ne sonradan eklenen anıtsal minaredir."],
                ["Delhi Cuma Mescidi", "1650", "Babürlüler döneminden kalma önemli bir eserdir."],
                ["Tac Mahal", "1648", "Agra'da; Babürlü mimarisinin zirvesi sayılan anıt mezardır."],
            ]
        ))
        .add_callout(Callout("insight", "Bölge İçi Süreklilik",
            "Hindistan'daki Türk mimarisi, Gaznelilerin başlattığı hakimiyetin devamıdır — bu yüzden Kutup Minar gibi "
            "erken eserlerde, bir önceki bölümde görülen <b>Gazneli minare geleneğinin</b> izleri sürülebilir."))
    )
    ch4.pages.append(
        ChapterPage()
        .add_summary("Hindistan'da Türk mimarisi, Gaznelilerle başlayıp Delhi Türk Sultanlığı ve Babürlüler ile "
            "gelişerek 9 asır süren bir mirastır. Kutup Minar'dan Tac Mahal'e uzanan bu çizgi, Türk-İslam mimari "
            "geleneğinin coğrafi olarak en uzağa taşındığı ve en görkemli örneklerini verdiği hattır.")
    )

    # =====================================================================
    # BÖLÜM 5 — Büyük Selçuklu Devri Mimarisi (1040-1157)
    # =====================================================================
    ch5 = Chapter(
        number=5,
        title="Büyük Selçuklu Devri Mimarisi",
        subtitle="1040-1157 · Mescid-i Cuma tipinden kümbet mimarisine klasik Selçuklu üslubu",
        key_terms=[
            KeyTerm("Mescid-i Cuma Tipi", "Karahanlı ve Gazneli geleneklerini harmanlayan, 'dört eyvanlı ve avlulu' Büyük Selçuklu cami planı."),
            KeyTerm("Tromp", "Kubbeye geçişi sağlayan mimari eleman; İsfahan Mescid-i Cuma'da Selçuklu kubbe mimarisine damgasını vurmuştur."),
            KeyTerm("Kümbet", "Türklerin İslamiyet öncesi mezar geleneğinin yansıması olan, silindir/sekizgen/kare gövdeli anıt mezar yapısı."),
            KeyTerm("Selçuklu Sülüsü", "Dönemin cami süslemelerinde Kûfi yazıyla birlikte kullanılan yazı stili."),
        ],
    )
    ch5.pages.append(
        ChapterPage()
        .add_terms(ch5.key_terms)
        .add_block(BulletBlock(1, "Tarihsel Çerçeve", [
            "<b>Kuruluş:</b> Selçuk Bey'in torunları Tuğrul ve Çağrı Beyler, 1040 Dandanakan Savaşı'nda Gaznelileri "
            "yenerek devleti kurmuş, Tuğrul Bey Sultan ilan edilmiş ve Nişabur başkent yapılmıştır.",
            "<b>Yayılım:</b> Devlet; doğuda Balkaş Gölü ve Tarım havzasından, batıda Ege ve Akdeniz'e; kuzeyde Aral "
            "ve Kafkasya'dan güneyde Umman denizine kadar 10 milyon km²'lik bir alana hükmetmiştir.",
            "<b>Bölünme:</b> Sultan Melikşah'ın 1092'de ölümünden sonra devlet; Kirman, Irak, Suriye ve Anadolu "
            "Selçukluları olarak kollara ayrılmıştır.",
        ]))
        .add_block(BulletBlock(2, "Cami Mimarisi (Mescid-i Cuma Tipi)", [
            "Büyük Selçuklular, Karahanlı ve Gazneli geleneklerini harmanlayarak 'Dört eyvanlı ve avlulu' cami "
            "tipini (Mescid-i Cuma) geliştirmiştir.",
        ]))
        .add_table(ComparisonTable(
            "Mescid-i Cuma Örnekleri",
            ["Eser", "Not"],
            [
                ["İsfahan Mescid-i Cuma", "Sultan Melikşah yaptırmıştır; mihrap önü kubbesi ve trompları Selçuklu kubbe mimarisine damgasını vurmuştur."],
                ["Gülpâyegân (1118), Kazvin (1119), Zevvare (1135), Ardistan", "Geleneğin devamıdır; Zevvare'den sonra dört eyvanlı şema standartlaşmıştır."],
            ]
        ))
        .add_callout(Callout("caution", "Süsleme Malzemeleri",
            "Ana malzeme tuğladır. <b>Çini</b>, <b>stuk</b> (alçı) süslemeler, tuğlaların alegorik dizilişi, "
            "<b>Kûfi</b> ve <b>Selçuklu Sülüsü</b> yazılar kullanılmıştır."))
    )
    ch5.pages.append(
        ChapterPage()
        .add_block(BulletBlock(3, "Minare Mimarisi", [
            "Karahanlı ve Gazneli minarelerine göre daha ince ve zarif, yukarı doğru daralan silindirik yapılar "
            "inşa etmişlerdir. <b>Damgan Camii Minaresi</b> (1058), Tuğrul Bey zamanında yapılmış; mavi-firuze "
            "çinilerin kullanıldığı, Selçuklu mimarisindeki ilk çini örneğini barındıran eserdir.",
        ]))
        .add_table(ComparisonTable(
            "Mezar Mimarisi (Kümbet ve Türbeler)",
            ["Özellik / Örnek", "Açıklama"],
            [
                ["Yapı", "Genellikle silindir, sekizgen veya kare gövde üzerine; tek/çift katlı kubbe veya konik çatı ile örtülüdür."],
                ["Kümbed-i Ali (1056)", "Erken dönem örneklerindendir."],
                ["Sultan Sencer Türbesi (1157)", "Dönemin önemli anıt mezarlarındandır."],
                ["Mümine Hatun (1186)", "Geç dönem kümbet örneğidir."],
            ]
        ))
        .add_block(BulletBlock(4, "Medrese ve Kervansaray", [
            "<b>Medrese:</b> Devlet memuru yetiştirmek ve Sünni İslam anlayışını yaymak amacıyla ilk olarak Tuğrul "
            "Bey zamanında Bağdat, Tus, İsfahan gibi şehirlerde başlatılmıştır; Hargird ve Rey medreselerinden "
            "hareketle avlulu-eyvanlı plan şemasına sahip oldukları anlaşılmaktadır.",
            "<b>Ribât-ı Şerif (1115):</b> Nişabur-Merv arasında; dıştan kale gibi masif ve sade, içten ise saray "
            "kadar süslü ve zengin (avlulu, eyvanlı) bir mimariye sahiptir.",
        ]))
        .add_summary("Büyük Selçuklular, Dandanakan Zaferi'yle (1040) kurdukları devlette Mescid-i Cuma tipini "
            "standartlaştırmış; İsfahan'ın kubbe-tromp mimarisi, Damgan'ın ilk çinili minaresi ve Sultan Sencer "
            "Türbesi gibi eserlerle klasik Selçuklu üslubunun temelini atmıştır.")
    )

    # =====================================================================
    # BÖLÜM 6 — Anadolu'da Selçuklu Beylikleri Mimarisi (1071-1190)
    # =====================================================================
    ch6 = Chapter(
        number=6,
        title="Anadolu'da Selçuklu Beylikleri Mimarisi",
        subtitle="1071-1190 · Malazgirt sonrası ilk beyliklerde Anadolu Türk üslubunun doğuşu",
        key_terms=[
            KeyTerm("Danişmendliler", "Sivas, Tokat, Kayseri ve Malatya'da hüküm süren; Anadolu Selçuklu ve Osmanlı mimarisine zemin hazırlayan ilk beylik."),
            KeyTerm("Artuklular", "Mardin, Diyarbakır ve Harput'ta hüküm süren; taş işçiliğiyle öne çıkan, ilk açık avlulu medrese örneklerini veren beylik."),
            KeyTerm("Külliye", "Cami ve medresenin bir arada tasarlandığı yapı kompleksi; ilk denemeleri Danişmendlilerde görülür."),
            KeyTerm("Kümbet", "Beylikler döneminde de devam eden, kubbeli anıt mezar geleneği."),
        ],
    )
    ch6.pages.append(
        ChapterPage()
        .add_terms(ch6.key_terms)
        .add_block(BulletBlock(1, "Genel Özellikler", [
            "1071 Malazgirt Zaferi'nden sonra Anadolu'da kurulan ilk beyliklerdir. Henüz ortak bir 'Anadolu Türk "
            "Üslubu'ndan bahsedilemez; Orta Asya geleneği, yerel malzemeler ve farklı kültürlerin (Ermeni, Gürcü, "
            "Bizans) etkileşimi söz konusudur.",
        ]))
        .add_table(ComparisonTable(
            "Danişmendliler (Sivas, Tokat, Kayseri, Malatya)",
            ["Eser", "Not"],
            [
                ["Tokat Garipler Camii", "En erken Danişmendli camisidir."],
                ["Niksar Ulu Camii (1145)", "Çok destekli, ahşap çatılı; Bursa Ulu Camii tipinin Anadolu'daki en erken öncüsüdür."],
                ["Kayseri Kölük Camii ve Medresesi", "Cami-medresenin birleştirildiği ilk 'külliye' denemelerindendir."],
                ["Sivas Ulu Camii (XII. yy)", "Anadolu'daki ilk avlulu cami örneğidir."],
                ["Yağıbasan Medreseleri", "Anadolu'daki ilk kubbeli medrese örnekleridir."],
                ["Çağlayan Köprüsü (Amasya)", "Tuğla hatıllı yapı sistemiyle inşa edilen ilk köprüdür."],
            ]
        ))
        .add_table(ComparisonTable(
            "Artuklular (Mardin, Diyarbakır, Harput)",
            ["Yapı Türü", "Özellik / Örnekler"],
            [
                ["Camiler", "Enine dikdörtgen planlı, mihrap önü kubbeli, avlulu — Harput Ulu, Silvan Ulu (1157), Mardin Ulu, Kızıltepe Ulu."],
                ["Medreseler", "Anadolu'daki ilk açık avlulu medrese örnekleri — Mardin Hatuniye, Diyarbakır Zinciriye ve Mesudiye."],
                ["Köprüler", "Malabadi Köprüsü en meşhur eserleridir."],
            ]
        ))
    )
    ch6.pages.append(
        ChapterPage()
        .add_info_cards("Diğer Anadolu Beylikleri", [
            InfoCard("Saltuklular (Erzurum)", "Erzurum Ulu Camii (1179) — kareye yakın dikdörtgen planlı, mihraba dik 7 nefli, düz çatılı; minaresi Asya geleneğini yansıtır.", "1"),
            InfoCard("Mengücekler (Erzincan, Divriği)", "Divriği Ulu Camii ve Şifahanesi (1229) — 25 farklı tonoz/kubbe, 4 farklı taç kapısıyla eşsiz bir eserdir.", "2"),
        ])
        .add_callout(Callout("route", "Bölümler Arası Bağlantı",
            "Danişmendlilerin <b>külliye</b> denemesi, Artukluların <b>açık avlulu medrese</b> yeniliği ve Sivas Ulu "
            "Camii'nin <b>avlulu plan</b>ı — hepsi, birkaç on yıl sonra klasikleşecek olan Anadolu Selçuklu ve "
            "Osmanlı mimarisinin ilk denemeleridir."))
        .add_summary("Malazgirt sonrası Anadolu beylikleri (Danişmendliler, Artuklular, Saltuklular, Mengücekler), "
            "henüz ortak bir üslup oluşturmasa da külliye, açık avlulu medrese ve avlulu cami gibi yenilikleriyle "
            "Anadolu Selçuklu ve Osmanlı mimarisinin temelini atmıştır.")
    )

    chapters = [ch1, ch2, ch3, ch4, ch5, ch6]

    # =====================================================================
    # SÖZLÜK
    # =====================================================================
    glossary = [
        Concept("Talas Savaşı", "751, Türklerin İslamlaşmasına giden yolu açan dönüm noktası.", "Giriş", 1),
        Concept("Kitlevi Geçiş", "10. yy'da Oğuzların Müslüman olmasıyla başlayan dönem.", "Giriş", 1),
        Concept("Kübik Yapı Anlayışı", "Uygur mezar mimarisinden gelen ilk dönem yeniliği.", "Giriş", 1),
        Concept("Çifte Hakimiyet", "Karahanlıların Doğu-Batı ikili yönetim sistemi.", "Karahanlılar", 2),
        Concept("Merkezi Kubbe Şeması", "Hazara Degaron Camii'nde görülen, Osmanlı'ya öncülük eden plan.", "Karahanlılar", 2),
        Concept("Doğu Minareleri", "Silindirik, tuğla, cami kütlesinden bağımsız Türk minare tipi.", "Karahanlılar", 2),
        Concept("Ribat", "Güvenlik ve konaklama amaçlı kale görünümlü kervansaray.", "Karahanlılar", 2),
        Concept("Leşkergâh Sarayı", "Dört eyvanlı Gazneli sarayı; fresklerinde Türk yüzü betimlenir.", "Gazneliler", 3),
        Concept("Kûfi Yazı", "Gazneli minarelerinde kullanılan erken dönem yazı stili.", "Gazneliler", 3),
        Concept("Stuko", "Alçı işçiliği tekniği.", "Gazneliler", 3),
        Concept("Delhi Türk Sultanlığı", "Hindistan'da Gaznelilerden sonraki Türk hakimiyeti.", "Hindistan", 4),
        Concept("Babürlüler", "Tac Mahal'in sahibi Türk-Moğol hanedanı.", "Hindistan", 4),
        Concept("Kutup Minar", "1229, Kuvvetü'l-İslam Camii'ne eklenen anıtsal minare.", "Hindistan", 4),
        Concept("Mescid-i Cuma Tipi", "Büyük Selçukluların dört eyvanlı-avlulu cami planı.", "Büyük Selçuklu", 5),
        Concept("Tromp", "Kubbeye geçişi sağlayan mimari eleman.", "Büyük Selçuklu", 5),
        Concept("Kümbet", "Silindir/sekizgen/kare gövdeli Selçuklu anıt mezarı.", "Büyük Selçuklu", 5),
        Concept("Selçuklu Sülüsü", "Dönem süslemelerinde kullanılan yazı stili.", "Büyük Selçuklu", 5),
        Concept("Danişmendliler", "Sivas-Tokat-Kayseri-Malatya beyliği; ilk külliye denemeleri.", "Anadolu Beylikleri", 6),
        Concept("Artuklular", "Mardin-Diyarbakır-Harput beyliği; ilk açık avlulu medrese.", "Anadolu Beylikleri", 6),
        Concept("Külliye", "Cami ve medresenin bir arada tasarlandığı kompleks.", "Anadolu Beylikleri", 6),
        Concept("Satuk Buğra Han", "İslamiyet'i kabul ederek Karahanlıların kitlevi İslamlaşmasını başlatan hükümdar (ö. 955).", "Karahanlılar", 2),
        Concept("Dandanakan Savaşı", "1040, Tuğrul ve Çağrı Beylerin Gaznelileri yenerek Büyük Selçuklu Devleti'ni kurduğu savaş.", "Büyük Selçuklu", 5),
        Concept("Sultan Melikşah", "İsfahan Mescid-i Cuma'yı yaptıran Büyük Selçuklu hükümdarı.", "Büyük Selçuklu", 5),
        Concept("Malazgirt Zaferi", "1071, Anadolu'da ilk Türk beyliklerinin kurulmasının önünü açan zafer.", "Anadolu Beylikleri", 6),
    ]

    # =====================================================================
    # SINAV HAZIRLIK
    # =====================================================================
    distinctions = [
        DistinctionPair("Karahanlı Minaresi", "Gazneli Minaresi", "Karahanlı 'Doğu Minaresi' silindirik ve bağımsızdır; Gazneli minare (Mahmut III) alt kademede sekiz köşeli yıldız, üstte silindirik iki kademeli formdadır."),
        DistinctionPair("Kümbet", "Türbe", "İkisi de anıt mezardır; kümbet terimi özellikle Büyük Selçuklu döneminin silindir/sekizgen gövdeli, kubbe veya konik çatılı mezar yapıları için kullanılır."),
        DistinctionPair("Danişmendliler", "Artuklular", "Danişmendliler Sivas-Tokat-Kayseri-Malatya'da külliye denemeleriyle; Artuklular Mardin-Diyarbakır-Harput'ta taş işçiliği ve açık avlulu medreseyle öne çıkar."),
        DistinctionPair("Mescid-i Cuma Tipi", "Merkezi Kubbe Şeması", "Mescid-i Cuma Büyük Selçuklu'nun dört eyvanlı-avlulu cami planıdır; Merkezi Kubbe Şeması Karahanlı Hazara Degaron Camii'nin kare planlı, tek büyük kubbeli düzenidir."),
    ]

    match_table = [
        MatchRow("Karahanlılar (960-1212)", "Merkezi Kubbe Şeması, Doğu Minareleri", "Hazara Degaron Camii, Ribât-ı Melik"),
        MatchRow("Gazneliler (962-1186)", "Fars etkili sivil mimari, fresk", "Leşkergâh Sarayı, Sultan Mesut III Sarayı"),
        MatchRow("Delhi Türk Sultanlığı / Babürlüler", "Hindistan'da 9 asırlık Türk mimarisi", "Kutup Minar (1229), Tac Mahal (1648)"),
        MatchRow("Büyük Selçuklular (1040-1157)", "Mescid-i Cuma tipi, kümbet mimarisi", "İsfahan Mescid-i Cuma, Sultan Sencer Türbesi"),
        MatchRow("Danişmendliler", "İlk külliye denemesi", "Kayseri Kölük Camii ve Medresesi"),
        MatchRow("Artuklular", "İlk açık avlulu medrese", "Mardin Hatuniye, Diyarbakır Zinciriye"),
    ]

    qa_items = [
        QAItem("Türklerin İslamlaşmasında dönüm noktası kabul edilen savaş hangisidir?", "Talas Savaşı (751)."),
        QAItem("Karahanlılar hangi yönetim sistemini benimsemiştir?", "Çifte Hakimiyet (Doğu ve Batı)."),
        QAItem("Hazara Degaron Camii'nin plan özelliği nedir?", "Kare planlı ve Merkezi Kubbe şemalı; Osmanlı cami mimarisine öncülük eder."),
        QAItem("Doğu Minarelerinin temel özellikleri nelerdir?", "Tuğla malzemeli, silindirik, yukarı doğru incelen, cami kütlesinden bağımsız."),
        QAItem("Gazneli saray fresklerinde ne betimlenmiştir?", "Türk tipi insan yüzü (yuvarlak yüz, çekik göz) ve kıyafetler."),
        QAItem("Hindistan'da Türk mimarisinin zirvesi sayılan eser hangisidir?", "Tac Mahal (1648)."),
        QAItem("Büyük Selçukluların geliştirdiği cami tipi nedir?", "Mescid-i Cuma tipi — dört eyvanlı ve avlulu."),
        QAItem("Selçuklu mimarisindeki ilk çini örneği hangi eserde görülür?", "Damgan Camii Minaresi (1058)."),
        QAItem("Anadolu'daki ilk avlulu cami örneği hangisidir?", "Sivas Ulu Camii (XII. yy)."),
        QAItem("Anadolu'daki ilk açık avlulu medrese örneklerini hangi beylik vermiştir?", "Artuklular (Mardin Hatuniye, Diyarbakır Zinciriye ve Mesudiye)."),
    ]

    checklist = [
        "Türklerin İslamlaşma sürecini (Hz. Ömer'den Kitlevi Geçiş'e) sıralayabiliyorum.",
        "Karahanlı dönemi cami, minare, türbe, medrese ve kervansaray örneklerini biliyorum.",
        "Gazneli saray mimarisinin (Leşkergâh, Sultan Mesut III) özelliklerini açıklayabiliyorum.",
        "Hindistan'daki Türk hakimiyetinin süreç ve önemli eserlerini sayabiliyorum.",
        "Büyük Selçuklu Mescid-i Cuma tipini ve kümbet mimarisini tanımlayabiliyorum.",
        "Anadolu beyliklerini (Danişmendli, Artuklu, Saltuklu, Mengücek) coğrafyalarıyla eşleştirebiliyorum.",
        "Karahanlı ve Gazneli minare formlarını karşılaştırabiliyorum.",
        "Her dönemin öne çıkan taç kapı / portal geleneğini örnekleyebiliyorum.",
        "Dönemler arası mimari süreklilikleri (ör. Gazneli-Hint, Selçuklu-Anadolu) açıklayabiliyorum.",
        "Her devletin kuruluş tarihini ve kurucusunu doğru eşleştirebiliyorum.",
    ]

    return CoursePack(
        course_code="SANAT TARİHİ",
        title='Türk <span class="accent-word">İslam</span> Sanat Tarihi',
        subtitle="Orta Asya'dan Anadolu'ya Türk-İslam Mimarisinin Kuruluş Yılları",
        description=(
            "Türklerin İslamlaşmasından Karahanlı ve Gazneli mimarisine; Hindistan'daki Türk mirasından Büyük "
            "Selçuklu klasik üslubuna ve Anadolu beyliklerinin ilk denemelerine uzanan final sınavı özeti."
        ),
        theme="burgundy",
        icon_text="T",
        chapters=chapters,
        glossary=glossary,
        distinctions=distinctions,
        match_table=match_table,
        qa_items=qa_items,
        overview_lead=(
            "Bu ders; Türklerin İslamiyet'i kabulüyle başlayan <b>kültürel dönüşümü</b>, Karahanlı ve Gazneli "
            "mimarisindeki <b>özgün üslup arayışını</b> ve bu mirasın Büyük Selçuklu ile Anadolu beyliklerine "
            "uzanan <b>klasikleşme sürecini</b> bir bütün olarak ele alır."
        ),
        overview_cards=[
            {"title": "Giriş: İslamlaşma", "text": "Talas Savaşı, Kitlevi Geçiş ve ilk mimari yenilikler."},
            {"title": "Karahanlı Mimarisi", "text": "Merkezi kubbe şeması, Doğu Minareleri, Ribât-ı Melik."},
            {"title": "Gazneli Mimarisi", "text": "Fars etkili sivil mimari; Leşkergâh ve Sultan Mesut III sarayları."},
            {"title": "Hindistan'da Türk Sanatı", "text": "Kutup Minar'dan Tac Mahal'e 9 asırlık miras."},
            {"title": "Büyük Selçuklu Mimarisi", "text": "Mescid-i Cuma tipi, kümbet mimarisi, ilk çini örneği."},
            {"title": "Anadolu Beylikleri", "text": "Danişmendli, Artuklu, Saltuklu ve Mengücek ilk denemeleri."},
        ],
        overview_flow=[
            ("İslamlaşma", "Talas Savaşı / Kitlevi Geçiş"),
            ("Orta Asya", "Karahanlı / Gazneli"),
            ("Yayılma", "Hindistan / Büyük Selçuklu"),
            ("Anadolu", "İlk beylikler"),
        ],
        overview_note=(
            "Sınavda en çok karıştırılan yer, <b>dönemlerin minare ve cami plan tiplerinin birbirine karışmasıdır:</b> "
            "Karahanlı 'Merkezi Kubbe Şeması' ile Büyük Selçuklu 'Mescid-i Cuma (dört eyvanlı) tipi' farklı devirlerin "
            "farklı çözümleridir."
        ),
    )
