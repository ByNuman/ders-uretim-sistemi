# -*- coding: utf-8 -*-
"""SOSYOLOJİYE GİRİŞ — Görsel Ders Notu Kitabı, içerik tanımı.
Kaynak: 'SOSYOLOJİYE GİRİŞ ÖZET.pdf' (ham metin özet, 10 sayfa).
"""
import sys
from pathlib import Path
# Proje kökü: src/ -> <sinav> -> <donem> -> <sinif> -> KÖK (4 seviye yukarı)
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from content_model import (
    Person, KeyTerm, Callout, FlowStep, FlowDiagram, ComparisonTable,
    InfoCard, BulletBlock, Chapter, ChapterPage, Concept, CoursePack,
    QAItem, DistinctionPair, MatchRow, TestQuestion, AnswerItem,
)

TYLOR = Person(
    id="tylor", name="Edward B. Tylor", years="1832–1917",
    tagline="Kültür Antropolojisinin Kurucu İsmi",
    bio=["<b>İlkel Kültür</b> adlı eserinde kültürün rastgele değil doğal yasalara bağlı olduğunu ve biyolojik değil "
         "<b>sosyal yolla</b> (toplum içinde yaşayarak) kazanıldığını savunmuştur."],
)


def get_pack() -> CoursePack:

    # =====================================================================
    # BÖLÜM 1 — Kültür
    # =====================================================================
    ch1 = Chapter(
        number=1,
        title="Kültür",
        subtitle="Tanımından işlevlerine, kavramlarından değişim süreçlerine bütüncül bakış",
        key_terms=[
            KeyTerm("Kültür", "Bir toplumun üyesi olan insanın kazandığı bilgi, inanç, sanat, ahlak, hukuk ve gelenekleri içeren karmaşık bütün."),
            KeyTerm("Kültürel Gecikme", "Ogburn'e göre maddi kültürün (teknoloji) hızlı, manevi kültürün (değerler) yavaş değişmesinden doğan uyumsuzluk."),
            KeyTerm("Etnosentrizm", "Kişinin kendi kültürünü merkeze alıp diğer kültürleri bu ölçütle yargılamasıdır."),
            KeyTerm("Kültürel Relativizm", "Bir kültürü kendi yapısı ve değerleri içinde, yargılamadan anlamaya çalışma tutumu."),
        ],
    )
    ch1.pages.append(
        ChapterPage()
        .add_terms(ch1.key_terms)
        .add_person(TYLOR)
        .add_block(BulletBlock(1, "Kültürün Tanımı ve Doğası", [
            "Kültür; bilimsel veya estetik anlamının ötesinde, sosyolojik olarak toplumun üyesi olan insanın kazandığı "
            "bilgi, inanç, sanat, ahlak, hukuk ve geleneklerin karmaşık bütünüdür.",
        ]))
        .add_block(BulletBlock(2, "Kültürün 5 Temel Özelliği", [
            "<b>Her Şeyi Kapsayıcıdır:</b> Toplumun paylaştığı maddi/manevi tüm ögelerin toplamıdır; kültürsüz toplum düşünülemez.",
            "<b>Öğrenilir:</b> Doğuştan gelmez — bilinçli öğretim, gözlem ve birikimsellikle kazanılır.",
            "<b>Simgeseldir:</b> Dil, kültürün taşıyıcısıdır; nesnelere anlam yükleme (simgeleştirme) yeteneğiyle başlar.",
            "<b>Paylaşılır:</b> Bireysel değil toplumsaldır; grupça ortaklaşa yaratılır.",
            "<b>Örüntülüdür:</b> Gelişigüzel değil, 'çekirdek değerler' etrafında bütünleşmiş bir sistemdir.",
        ]))
        .add_callout(Callout("focus", "Kritik Odak: Fichter'e Göre Kültürün İşlevleri",
            "Toplumsal davranışları düzenler ve bütünleştirir · toplumsal dayanışmayı sağlar · toplumun kimliği olur · "
            "değerleri yorumlar · kişiliğin oluşmasında başat faktördür."))
    )
    ch1.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Kültürün Ögeleri ve Kültürel Gecikme",
            ["Kavram", "Açıklama"],
            [
                ["Maddi Ögeler", "Teknoloji, binalar, araç-gereçler gibi fiziksel nesneler."],
                ["Manevi Ögeler", "Değerler, inançlar, kurallar, gelenek ve görenekler."],
                ["Kültürel Gecikme (Ogburn)", "Maddi kültür hızlı, manevi kültür yavaş değişir — bu fark uyumsuzluk yaratır."],
            ]
        ))
        .add_table(ComparisonTable(
            "Kültürel Kavramlar",
            ["Kavram", "Açıklama"],
            [
                ["Kültürel Evrensellik", "Her toplumda aile, hukuk, ahlak gibi yapısal kurumlar vardır; içerikleri değişir."],
                ["Etnosentrizm (Bizmerkezcilik)", "Kendi kültürünü merkeze alıp diğerlerini yargılama (ör. boğa güreşini vahşet görmek)."],
                ["Kültürel Relativizm", "Bir kültürü kendi değerleri içinde, yargılamadan anlama çabası."],
                ["Alt Kültür / Karşıt Kültür", "Alt kültür egemen kültürden kısmen farklılaşır; karşıt kültür normları reddeder."],
                ["İdeal vs. Gerçek Kültür", "İdeal 'olması gereken' kurallar, gerçek ise 'fiilen uygulanan'dır."],
                ["Yüksek vs. Popüler Kültür", "Yüksek kültür seçkinlere (güzel sanatlar), popüler kültür halk kitlelerine hitap eder."],
            ]
        ))
        .add_table(ComparisonTable(
            "Kültürel Süreçler",
            ["Süreç", "Açıklama"],
            [
                ["Kültürleme (Enkültürasyon)", "Bireyin doğuştan ölüme kadar kültürü öğrenmesi, eğitilmesi."],
                ["Kültürleşme (Akkültürasyon)", "Farklı kültürlerin etkileşimiyle her ikisinin de değişmesi."],
                ["Kültürlenme (Kültürasyon)", "Etkileşim sonucu, asıl kültürlerde olmayan yeni bir sentezin oluşması (ör. gecekondu kültürü)."],
                ["Kültürel Yayılma (Difüzyon)", "Kültür ögelerinin bir toplumdan diğerine geçmesi."],
                ["Kültür Şoku", "Başka bir kültüre giren bireyin yaşadığı uyum sıkıntısı."],
            ]
        ))
        .add_summary("Kültür, öğrenilen, paylaşılan ve örüntülü bir bütündür; maddi ve manevi ögelerden oluşur. "
            "Maddi kültürün manevi kültürden hızlı değişmesi 'kültürel gecikme' yaratır. Etnosentrizm ile kültürel "
            "relativizm, bir kültürü değerlendirirken alınabilecek iki karşıt tutumdur.")
    )

    # =====================================================================
    # BÖLÜM 2 — Toplumsallaşma ve Davranış Kalıpları
    # =====================================================================
    ch2 = Chapter(
        number=2,
        title="Toplumsallaşma ve Davranış Kalıpları",
        subtitle="Bireyin toplumsal bir varlığa dönüşümünden, toplumun ortak davranış örüntülerine",
        key_terms=[
            KeyTerm("Toplumsallaşma", "Bireyin toplumun kural ve değerlerini öğrenerek biyolojik varlıktan toplumsal varlığa dönüşme süreci."),
            KeyTerm("Yeniden Toplumsallaşma", "Bireyin değer ve davranışlarını temelden değiştirmesi (ör. evlilikten dulluğa geçiş)."),
            KeyTerm("Davranış Kalıbı", "Toplumda genelleşmiş, düzenlilik kazanmış, yinelenen düşünüş ve eylem biçimi."),
            KeyTerm("Propaganda", "Fikirleri tek taraflı olarak benimsetmeyi ve 'kabul ettirmeyi' amaçlayan yapay etkileme aracı."),
        ],
    )
    ch2.pages.append(
        ChapterPage()
        .add_terms(ch2.key_terms)
        .add_block(BulletBlock(1, "Toplumsallaşmanın Tanımı ve Amaçları", [
            "Bireyin toplumun kurallarını ve değerlerini öğrenerek biyolojik bir varlıktan toplumsal bir varlığa "
            "dönüşmesi, kişilik ve benlik kazanması sürecidir. Doğumla başlar, ölüme kadar sürer.",
            "<b>Amaçlar:</b> Temel davranışları öğretmek, özlemler oluşturmak, toplumsal rolleri öğretmek, kimlik "
            "kazandırmak ve toplumun sürekliliğini sağlamak.",
        ]))
        .add_table(ComparisonTable(
            "Toplumsallaşma Tipleri",
            ["Tip", "Açıklama"],
            [
                ["Başarılı Toplumsallaşma", "Birey davranışları ayırt edebilir, ödül-ceza sistemiyle eğitilir, bunalımları yönetilebilir."],
                ["Başarısız Toplumsallaşma", "Kuralların öğrenilememesi/çelişkili aktarılması sonucu sapkın (patolojik) davranışlar gelişir."],
            ]
        ))
        .add_block(BulletBlock(2, "Toplumsallaşma Araçları", [
            "<b>Aile:</b> İlk ve en etkili araçtır; duygusal boyutu benlik oluşumunda kritiktir.",
            "<b>Arkadaş Grupları:</b> Aileden farklı olarak eşitlikçidir; çocuğa bağımsız bir kimlik alanı sağlar.",
            "<b>Okul:</b> Resmi, örgütlü, otorite ve disiplin içerir; öğretmen profesyonel bir modeldir.",
            "<b>Kitle İletişim Araçları:</b> Dünya görüşünü etkiler, rol modelleri sunar (TV vb.).",
        ]))
        .add_callout(Callout("caution", "Dikkat: Toplumsallaşma Çocuklukla Bitmez",
            "Askerlik, evlilik gibi yeni rollerle yetişkinler de değişir. Bireyin değer ve davranışlarını temelden "
            "değiştirmesine <b>Yeniden Toplumsallaşma (Resocialization)</b> denir."))
    )
    ch2.pages.append(
        ChapterPage()
        .add_block(BulletBlock(3, "Davranış Kalıplarının Tanımı", [
            "Toplumda genelleşmiş, düzenlilik kazanmış, yinelenen düşünüş ve eylem biçimleridir; bireysel değil "
            "toplumsaldır. Birey bunları düşünmeden otomatik yapar ('Herkes öyle yaptığı için').",
            "Biyolojik değil öğrenilmiştir — acıkmak biyolojik, domuz eti yememek kültürel bir kalıptır. Üç boyutu "
            "vardır: Toplumsal Yaptırım (baskı), Toplumsal Değer (önem) ve Genellik (yaygınlık).",
        ]))
        .add_table(ComparisonTable(
            "Dışsal ve İçsel Davranış Kalıpları",
            ["Tür", "Açıklama"],
            [
                ["Dışsal — Yüksek Baskılı", "Gözlemlenebilir eylemler; uymamak şiddetli tepki görür (ör. adam öldürme)."],
                ["Dışsal — Düşük Baskılı", "Gözlemlenebilir ama hafif yaptırımlı eylemler (ör. nezaket kuralları)."],
                ["İçsel Davranış Kalıpları", "Düşünce ve inanç biçimleridir, doğrudan gözlenemez; dışsaldan daha süreklidir."],
            ]
        ))
        .add_table(ComparisonTable(
            "Tan'ın İçsel Davranış Kalıpları Sınıflandırması (1981)",
            ["Kalıp", "Açıklama"],
            [
                ["Toplumsal İnançlar", "Bilgi (doğrulanabilir), İman (doğrulanamaz, ör. melek), Kanaat (geleceğe dair özel inanç)."],
                ["Toplumsal Tutumlar", "Eyleme hazır olma durumu."],
                ["Toplumsal İdealler", "'Olması gereken' — doğru-yanlış ölçütü."],
                ["Toplumsal Tercihler", "Arzu edilen, beğenilen şeyler."],
            ]
        ))
        .add_table(ComparisonTable(
            "Davranış Kalıplarının Sonuçları ve Değiştirme Yolları",
            ["Kavram", "Açıklama"],
            [
                ["Moda", "Onaylanan geçici değişikliklerdir; hem topluma uyma hem farklılaşma ihtiyacını karşılar."],
                ["İdeoloji", "Bir rejimin ilkeleri/toplumun dünya görüşüdür; doğruluğundan çok kabul edilmesi önemlidir."],
                ["Kamuoyu", "Halkın bir kesiminin belli bir konudaki görüşüdür (tüm nüfusun görüşü değildir)."],
                ["Propaganda", "Fikirleri tek taraflı benimsetmeye çalışan yapay etkileme; 'kabul ettirmeyi' amaçlar."],
                ["Reklam", "Ticari etkinliktir; tercih ve arzu yaratarak satın aldırmayı hedefler."],
            ]
        ))
    )
    ch2.pages.append(
        ChapterPage()
        .add_summary("Toplumsallaşma, bireyi biyolojik varlıktan toplumsal varlığa dönüştüren yaşam boyu bir süreçtir; "
            "aile, akran grubu, okul ve medya bu sürecin başlıca araçlarıdır. Davranış kalıpları ise toplumun "
            "ortaklaşa ürettiği, bireyin sorgulamadan uyduğu yinelenen eylem ve düşünüş biçimleridir.")
    )

    # =====================================================================
    # BÖLÜM 3 — Toplumsal Değişme
    # =====================================================================
    ch3 = Chapter(
        number=3,
        title="Toplumsal Değişme",
        subtitle="Tanımından kuramlarına, geleneksel toplumdan sanayi toplumuna geçişin dinamikleri",
        key_terms=[
            KeyTerm("Toplumsal Değişme", "Toplumun yapısında, ilişkiler ağında ve kurumlarında meydana gelen, değer yargısı içermeyen farklılaşma."),
            KeyTerm("Sosyo-kültürel Değişme", "Toplumsal (yapı) ve kültürel (değerler) değişmenin iç içe geçmiş halinin ortak adı."),
            KeyTerm("Evrimci Kuram", "Toplumsal değişmeyi tarihsel birikim ve ilerleme olarak açıklayan yaklaşım (Comte, Durkheim)."),
            KeyTerm("Çatışma Yaklaşımı", "Çatışmanın kaçınılmaz olduğunu ve değişimin itici gücü olduğunu savunan yaklaşım (Dahrendorf)."),
        ],
    )
    ch3.pages.append(
        ChapterPage()
        .add_terms(ch3.key_terms)
        .add_block(BulletBlock(1, "Tanım ve Temel Dinamikler", [
            "Toplumun yapısında, ilişkiler ağında ve kurumlarında meydana gelen farklılaşmadır. Hiçbir toplum statik "
            "değildir. İki temel dinamiği vardır: <b>Teknoloji</b> (insan-doğa çelişkisi) ve <b>İdeoloji</b> (insan-insan çelişkisi).",
        ]))
        .add_table(ComparisonTable(
            "Toplumsal Değişme ile Karıştırılan Kavramlar",
            ["Kavram", "Fark"],
            [
                ["Gelişme", "Olumlu yönde katedilen mesafedir; değer yargısı içerir."],
                ["Kalkınma / Büyüme", "Genellikle ekonomik ve ölçülebilir değişimdir."],
                ["Modernleşme", "Az gelişmişlerin gelişmişlere yetişmesi, batılılaşmadır."],
                ["Evrim", "Çok uzun süreli değişimlerin tümüdür."],
            ]
        ))
        .add_callout(Callout("insight", "Ortak Payda",
            "Toplumsal değişme bu dört kavramın hepsini kapsayan, <b>nesnel</b> (iyi/kötü yargısı içermeyen) bir çatı "
            "kavramdır — Gelişme, Kalkınma, Modernleşme ve Evrim onun özel görünümleridir."))
        .add_block(BulletBlock(2, "Değişmenin Ögeleri ve Faktörleri", [
            "Değişimin üç temel ögesi: <b>İnsan, Zaman ve Mekân</b> (fiziksel ortam).",
            "<b>Faktörler:</b> Demografik (nüfus), Coğrafi (afetler), Teknolojik (doğanın denetimi), Kültürel (tutumlar), Toplumsal Çevre (savaşlar).",
            "<b>Kaynaklar:</b> İç kaynaklar (iç göç, keşifler) ve dış kaynaklar (planlı fetihler veya plansız etkileşimler).",
        ]))
    )
    ch3.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Toplumsal Değişme Kuramları",
            ["Ölçek", "Yaklaşım", "Temsilciler"],
            [
                ["Büyük Boy (Tarihsel)", "Evrimci: tarihsel birikim ve ilerleme.", "Comte, Durkheim"],
                ["Büyük Boy (Tarihsel)", "Diyalektik: zıtlıkların çatışmasıyla doğan yeni.", "Marx"],
                ["Büyük Boy (Tarihsel)", "Organizmacı: toplumlar doğar, büyür, ölür.", "İbni Haldun"],
                ["Orta Boy (Ulusal)", "Yapısal Fonksiyonel: toplum ahenkli bir bütündür.", "Parsons"],
                ["Orta Boy (Ulusal)", "Çatışma Yaklaşımı: çatışma değişimin itici gücüdür.", "Dahrendorf"],
                ["Küçük Boy", "Sosyal psikoloji odaklı değişim.", "—"],
            ]
        ))
        .add_table(ComparisonTable(
            "Gelenekselden Sanayi Toplumuna Geçiş",
            ["Alan", "Dönüşüm"],
            [
                ["Nüfus", "Hızla artıp sonra dengeye girmiştir."],
                ["Aile", "Geniş aileden çekirdek aileye geçilmiştir."],
                ["Eğitim", "Laik, bilimsel ve okul sistemine dayalı hale gelmiştir."],
                ["Ekonomi", "Tarımdan sanayi ve hizmetlere geçilmiştir."],
                ["Siyaset", "Geleneksel otoriteden 'Yasal Otorite'ye geçilmiştir (Weber)."],
                ["Tabakalaşma", "'Atfedilen statü' yerine 'Kazanılmış statü' önem kazanmıştır."],
            ]
        ))
        .add_summary("Toplumsal değişme, gelişme-kalkınma-modernleşme-evrim gibi kavramları kapsayan nesnel bir çatı "
            "kavramdır; insan, zaman ve mekân ekseninde gerçekleşir. Evrimci, diyalektik ve çatışmacı kuramlar bu "
            "değişimi farklı açılardan açıklarken, sanayileşme aile, eğitim, ekonomi ve tabakalaşmayı kökten dönüştürmüştür.")
    )

    # =====================================================================
    # BÖLÜM 4 — Modernizm ve Postmodernizm
    # =====================================================================
    ch4 = Chapter(
        number=4,
        title="Modernizm ve Postmodernizm",
        subtitle="Akılcılaşmadan simülasyona: iki çağın karşıt paradigmaları",
        key_terms=[
            KeyTerm("Modernlik", "'Hemen şimdi' kökünden gelir; 17. yüzyılda eski toplum tipinden kopuşu, akılcılaşma ve uzmanlaşmayı ifade eder."),
            KeyTerm("Postmodernizm", "Lyotard'a göre (1979) modernliğin kesinlik ve evrensellik iddialarına karşı çıkan, belirsizliği ve çoğulculuğu savunan yaklaşım."),
            KeyTerm("Simülasyon", "Baudrillard'a göre gerçeğin yerini imajların alması; artık ekonomik/politik gerçeklik değil, kültürel ürünler ve imajlar vardır."),
            KeyTerm("Eklektisizm", "Postmodern düşüncede parçalanmışlık ilkesi ve seçmecilik — farklı unsurların bir arada, hiyerarşisiz kullanılması."),
        ],
    )
    ch4.pages.append(
        ChapterPage()
        .add_terms(ch4.key_terms)
        .add_block(BulletBlock(1, "Modernleşme", [
            "<b>Modernlik Nedir?</b> 'Modernus' (hemen şimdi) kökünden gelir; eski toplum tipinden kopuşu (17. yy) "
            "ifade eder — farklılaşma, uzmanlaşma, bilim ve teknolojinin başat olduğu yaşamdır.",
            "<b>Temel Nitelikleri:</b> Akılcılaşma (dünyanın akılla yönetilmesi), Ayrışma (din-devlet ayrımı), Özgürlük ve Öznelleştirme.",
        ]))
        .add_info_cards("Modernliğin Öncü Kuramcıları", [
            InfoCard("Karl Marx", "Kapitalizm çözümlemesiyle modernliğin ekonomik boyutunu açıklar.", "1"),
            InfoCard("Émile Durkheim", "İş bölümü kavramıyla toplumsal dayanışmanın dönüşümünü inceler.", "2"),
            InfoCard("Max Weber", "Akılcılık ve bürokrasi kavramlarıyla modern kurumsallaşmayı çözümler.", "3"),
        ])
        .add_table(ComparisonTable(
            "Modernliğin Boyutları (Tekeli)",
            ["Boyut", "İçerik"],
            [
                ["Ekonomik", "Kapitalizm."],
                ["Bilgi", "Nesnel bilim."],
                ["Birey", "Aklıyla kendini yöneten özne."],
                ["Kurumsal", "Ulus devlet, demokrasi."],
            ]
        ))
    )
    ch4.pages.append(
        ChapterPage()
        .add_block(BulletBlock(2, "Postmodernizm", [
            "<b>Nedir?</b> Modernizmin sonrası veya ötesidir (Lyotard, 1979); modernliğin kesinlik, evrensellik gibi "
            "parametrelerine karşı çıkar, belirsizliği, farklılığı ve çoğulculuğu savunur.",
            "<b>Belirsizlik ve Yerellik:</b> Evrenselliği reddeder. <b>Çoğulculuk:</b> Kültürler arası üstünlük yoktur. "
            "<b>'Her Şey Gider':</b> Ne üretilirse tüketilir. <b>Simülasyon:</b> Gerçeğin yerini imajlar alır (Baudrillard). "
            "<b>Eklektisizm:</b> Parçalanmışlık ve seçmecilik.",
        ]))
        .add_callout(Callout("insight", "Baudrillard'ın Tezi",
            "Postmodern dönemde artık ekonomik veya politik bir gerçeklik yoktur; yalnızca <b>kültürel ürünler ve "
            "imajlar</b> vardır. Dönüşüm; üretimden tüketime, emekten bilgiye, bilimsellikten simülasyona doğrudur."))
        .add_summary("Modernizm; akılcılaşma, ayrışma ve özgürleşme ekseninde 17. yüzyılda başlayan bir kopuştur ve "
            "Marx, Durkheim, Weber gibi kuramcılarca ekonomik-toplumsal-kurumsal boyutlarıyla çözümlenmiştir. "
            "Postmodernizm ise bu kesinlik iddialarına karşı çıkarak belirsizliği, çoğulculuğu ve simülasyonu öne çıkarır.")
    )

    # =====================================================================
    # BÖLÜM 5 — Toplumsal Statü
    # =====================================================================
    ch5 = Chapter(
        number=5,
        title="Toplumsal Statü",
        subtitle="Bireyin toplumdaki konumunu belirleyen verilmiş ve kazanılmış ölçütler",
        key_terms=[
            KeyTerm("Statü", "Bireyin içinde yaşadığı grupta işgal ettiği konum (mevki); başkalarının statüleriyle ilişkilendiğinde anlam kazanır."),
            KeyTerm("Statüsel Saygınlık", "Bireyin işgal ettiği konuma toplumun genel olarak verdiği değer."),
            KeyTerm("Verilmiş (Ascribed) Statü", "Bireyin kendi çabası dışında, genellikle doğumla kazandığı statü türü."),
            KeyTerm("Kazanılmış (Achieved) Statü", "Kişinin kendi yetenek, eğitim ve çabasıyla elde ettiği statü türü."),
        ],
    )
    ch5.pages.append(
        ChapterPage()
        .add_terms(ch5.key_terms)
        .add_block(BulletBlock(1, "Tanım ve Mahiyeti", [
            "Toplum rastgele bir insan yığını değildir; her bireyin grupta işgal ettiği bir konuma <b>statü</b> denir.",
            "<b>İlişkisel Nitelik:</b> Bir statü tek başına değil, ancak başka kişilerin statüleriyle karşılaştırıldığında "
            "anlam kazanır — bu ilişki statülerin kendisi arasında değil, onları taşıyan insanlar arasındadır.",
        ]))
        .add_table(ComparisonTable(
            "Statü ile Saygınlık (Prestij) Ayrımı",
            ["Kavram", "Açıklama", "Örnek"],
            [
                ["Statüsel Saygınlık", "Bireyin işgal ettiği konuma toplumun genel olarak verdiği değerdir.", "Doktorluk mesleğinin toplumdaki genel itibarı."],
                ["Kişisel Saygınlık", "Bireyin statünün gereklerini ne kadar başarıyla yerine getirdiğiyle ilgilidir.", "Alkol bağımlısı bir doktor kişisel saygınlığını yitirebilir; işini iyi yapan bir temizlik işçisi yüksek kişisel saygınlık kazanabilir."],
            ]
        ))
        .add_table(ComparisonTable(
            "Verilmiş (Ascribed) Statünün Belirleyicileri",
            ["Faktör", "Açıklama"],
            [
                ["Soy Bağı", "Ailenin şöhreti, etnik kökeni veya bir yerde ikamet süresi."],
                ["Yaş", "Belirli toplumsal davranışların (seçme/seçilme gibi) sınırlarını çizer."],
                ["Cinsiyet", "Evrensel bir faktördür; değeri tarihsel süreçte değişebilir."],
                ["Biyolojik Nitelikler", "Irk, fiziksel görünüm, zekâ veya engellilik gibi doğuştan gelen özellikler."],
            ]
        ))
    )
    ch5.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Kazanılmış (Achieved) Statünün Belirleyicileri",
            ["Faktör", "Açıklama"],
            [
                ["Servet", "Nesnel ve sayılabilir bir ölçüttür; miktarı kadar kaynağı da önemlidir."],
                ["Eğitim", "Süresi, derecesi ve diplomanın alındığı kurumun prestiji statüyü belirler."],
                ["Meslek", "İş bölümü sonucu ortaya çıkar; zihinsel meslekler kas gücüne dayalı olanlara göre daha yüksek statü sağlar."],
            ]
        ))
        .add_callout(Callout("caution", "Dikkat / Sınav Ayrımı",
            "Geleneksel toplumlarda <b>Verilmiş</b> statüler, çağdaş sanayi toplumlarında ise <b>Kazanılmış</b> statüler "
            "daha ön plandadır."))
        .add_block(BulletBlock(2, "Anahtar Statü ve Statü Aktarımı", [
            "<b>Anahtar Statü (Master Status):</b> Bireyin sahip olduğu statülerden birinin diğerlerine baskın çıkarak "
            "kimliğini ve toplumdaki yerini belirlemesidir — genellikle toplumdaki en baskın kuruma göre şekillenir "
            "(ör. ekonomi öncelikli toplumlarda kişinin mesleği).",
            "<b>Statü Aktarımı:</b> Bir statünün saygınlığının, o statüye sahip kişi üzerinden yakınlarına geçmesidir. "
            "Geleneksel yapıda aile reisi ailenin dış temsilcisidir; kadın ve çocuklar onun statüsüne göre değerlendirilir.",
        ]))
        .add_summary("Statü, bireyin toplumdaki konumudur ve ancak başka statülerle ilişkilendiğinde anlam kazanır. "
            "Verilmiş statüler doğuştan (soy, yaş, cinsiyet), kazanılmış statüler ise çabayla (servet, eğitim, meslek) "
            "elde edilir; anahtar statü bunlardan kimliği en çok belirleyenidir.")
    )

    # =====================================================================
    # BÖLÜM 6 — Toplumsal Rol
    # =====================================================================
    ch6 = Chapter(
        number=6,
        title="Toplumsal Rol",
        subtitle="Statünün davranışa dökülmüş hali: edinme biçimleri, kavramlar ve yaptırımlar",
        key_terms=[
            KeyTerm("Toplumsal Rol", "Belirli bir statünün gerektirdiği görevleri yapma, hak ve ayrıcalıkları kullanma biçimi."),
            KeyTerm("Rol Takımı (Role Set)", "Bir kişinin tek bir statüye bağlı olarak yerine getirmesi gereken birden fazla rolün tümü."),
            KeyTerm("Rol Çatışması", "Kişinin sahip olduğu bir rolün başka bir gruptaki rolüyle uyumsuz olması."),
            KeyTerm("Anahtar Rol", "Bireyin rolleri arasında en önemli olanı; genellikle anahtar statüyle paraleldir."),
        ],
    )
    ch6.pages.append(
        ChapterPage()
        .add_terms(ch6.key_terms)
        .add_block(BulletBlock(1, "Tanım ve Statü-Rol İlişkisi", [
            "Toplumsal rol, statünün davranışa dökülmüş, dinamik halidir. Statü 'nerede olunduğunu', rol ise "
            "'ne yapıldığını' gösterir.",
            "<b>Hak ve Görev Dengesi:</b> Roller karşılıklıdır; birinin hakkı diğerinin görevidir (Kral-Uyruk, Anne-Çocuk, Vekil-Seçmen gibi).",
            "Roller toplumun sunduğu 'hazır reçeteler' gibidir; ancak bireyler kendi yorumlarını katarak oynar — bu "
            "yüzden aynı rolü farklı kişiler farklı biçimde canlandırır.",
        ]))
        .add_table(ComparisonTable(
            "Rollerin Edinilme Biçimleri",
            ["Biçim", "Açıklama", "Örnek"],
            [
                ["Tahsis Etme (Allocation)", "Rolün kişiye dışarıdan, otomatik olarak verilmesi.", "Evlat veya teyze olmak."],
                ["Üstlenme (Assumption)", "Bireyin kendi iradesi ve gönüllülüğüyle bir rolü alması.", "Bir meslek seçmek veya evlenmek."],
            ]
        ))
    )
    ch6.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Rol Kavramları ve Terimleri",
            ["Kavram", "Açıklama"],
            [
                ["Rol Takımı", "Bir statüye bağlı yerine getirilmesi gereken tüm rollerin toplamı (ör. profesörün ders + araştırma + danışmanlık rolleri)."],
                ["Rol Beklentileri", "Bir konuma dair toplumun beklediği standart davranış kalıpları."],
                ["Rol Çatışması", "Bir rolün başka bir gruptaki rolle uyumsuz olması (ör. iyi baba – iyi öğretmen çatışması)."],
                ["Roller Arası Pekiştirme", "Farklı rollerin çatışmak yerine birbirini desteklemesi (ör. avukatın hitabetinin siyasetçiliğini güçlendirmesi)."],
                ["Anahtar Rol", "Bireyin rolleri arasında en önemli olanı; genellikle anahtar statüyle paraleldir."],
                ["Genel Rol", "Bireyin oynadığı tüm rollerin toplam bileşimi."],
                ["Rol Uzmanlaşması", "Bireyin bir statüdeki rollerden bazılarına özel ilgi gösterip diğerlerini ihmal etmesi; kişiye doyum sağlar."],
            ]
        ))
        .add_block(BulletBlock(2, "Rolün İçeriği", [
            "Bir rol yalnızca eylemleri değil, o role uygun düşünce ve tutumları da (ör. bir öğretmen gibi düşünmeyi) kapsar.",
        ]))
        .add_callout(Callout("route", "Bölüm İçi Bağlantı",
            "Statü ile Rol arasındaki fark sınavda en sık sorulan ayrımlardan biridir: <b>Statü konumdur, Rol o "
            "konumun gerektirdiği eylemdir.</b> Bir kişinin anahtar statüsü genellikle onun anahtar rolüyle örtüşür."))
        .add_table(ComparisonTable(
            "Toplumun Rol Davranışlarını Yargılama Kategorileri",
            ["Kategori", "Açıklama", "Örnek"],
            [
                ["Beklenen Davranış (Zorunlu)", "Rolün gerçekleşmesi için şarttır; yapılmazsa rol oynanmış sayılmaz.", "Öğrencinin derse girmesi, sınava katılması."],
                ["İzin Verilen Davranış (Esnek)", "Toplumun katı kural koymadığı alandır.", "Öğrencinin seçmeli ders alabilmesi."],
                ["Yasaklanan Davranış (Cezalı)", "Toplumun ceza uyguladığı davranışlardır.", "Öğrencinin okul eşyasına zarar vermesi."],
            ]
        ))
        .add_summary("Toplumsal rol, statünün somutlaşmış, edimsel halidir; tahsis etme veya üstlenme yoluyla kazanılır. "
            "Rol takımı, rol çatışması ve anahtar rol gibi kavramlar bireyin çoklu rollerini analiz etmeyi sağlar; "
            "toplum ise rol davranışlarını beklenen, izin verilen ve yasaklanan olmak üzere üç kategoride yargılar.")
    )

    chapters = [ch1, ch2, ch3, ch4, ch5, ch6]

    # =====================================================================
    # SÖZLÜK
    # =====================================================================
    glossary = [
        Concept("Kültür", "Toplum üyesinin kazandığı bilgi, inanç, sanat, ahlak, hukuk ve geleneklerin bütünü.", "Kültür", 1),
        Concept("Kültürel Gecikme", "Maddi kültürün hızlı, manevi kültürün yavaş değişmesinden doğan uyumsuzluk.", "Ogburn", 1),
        Concept("Etnosentrizm", "Kendi kültürünü merkeze alıp diğerlerini yargılama.", "Kültürel Kavramlar", 1),
        Concept("Kültürel Relativizm", "Bir kültürü kendi değerleri içinde, yargılamadan anlama.", "Kültürel Kavramlar", 1),
        Concept("Alt Kültür", "Egemen kültürden kısmen farklılaşan gruplar.", "Kültürel Kavramlar", 1),
        Concept("Karşıt Kültür", "Toplumun normlarını reddeden, ters düşen kültür.", "Kültürel Kavramlar", 1),
        Concept("Enkültürasyon", "Bireyin doğuştan ölüme kadar kültürü öğrenmesi.", "Kültürel Süreçler", 1),
        Concept("Akkültürasyon", "Farklı kültürlerin etkileşimiyle her ikisinin de değişmesi.", "Kültürel Süreçler", 1),
        Concept("Kültür Şoku", "Başka kültüre giren bireyin yaşadığı uyum sıkıntısı.", "Kültürel Süreçler", 1),
        Concept("Toplumsallaşma", "Bireyin biyolojik varlıktan toplumsal varlığa dönüşme süreci.", "Toplumsallaşma", 2),
        Concept("Yeniden Toplumsallaşma", "Bireyin değer ve davranışlarını temelden değiştirmesi.", "Toplumsallaşma", 2),
        Concept("Davranış Kalıbı", "Toplumda genelleşmiş, yinelenen düşünüş ve eylem biçimi.", "Davranış Kalıpları", 2),
        Concept("Moda", "Onaylanan geçici değişiklikler; uyma ve farklılaşma ihtiyacını birlikte karşılar.", "Davranış Kalıpları", 2),
        Concept("İdeoloji", "Bir rejimin ilkeleri veya toplumun dünya görüşü.", "Davranış Kalıpları", 2),
        Concept("Propaganda", "Fikirleri tek taraflı benimsetmeye çalışan yapay etkileme.", "Davranış Kalıpları", 2),
        Concept("Toplumsal Değişme", "Toplumun yapı, ilişki ve kurumlarındaki nesnel farklılaşma.", "Toplumsal Değişme", 3),
        Concept("Evrimci Kuram", "Değişmeyi tarihsel birikim ve ilerleme olarak açıklar.", "Comte, Durkheim", 3),
        Concept("Diyalektik Kuram", "Değişmeyi zıtlıkların çatışmasıyla açıklar.", "Marx", 3),
        Concept("Çatışma Yaklaşımı", "Çatışmanın değişimin itici gücü olduğunu savunur.", "Dahrendorf", 3),
        Concept("Yasal Otorite", "Geleneksel otoritenin yerini alan, sanayi toplumuna özgü otorite biçimi.", "Weber", 3),
        Concept("Modernlik", "17. yüzyılda başlayan, akılcılaşma ve uzmanlaşmayla tanımlanan kopuş.", "Modernizm", 4),
        Concept("Postmodernizm", "Modernliğin kesinlik iddialarına karşı çıkan, çoğulculuğu savunan yaklaşım.", "Lyotard", 4),
        Concept("Simülasyon", "Gerçeğin yerini imajların alması.", "Baudrillard", 4),
        Concept("Eklektisizm", "Postmodern düşüncede parçalanmışlık ve seçmecilik ilkesi.", "Postmodernizm", 4),
        Concept("Statü", "Bireyin grupta işgal ettiği, ilişkisel anlam kazanan konum.", "Toplumsal Statü", 5),
        Concept("Statüsel Saygınlık", "Bireyin işgal ettiği konuma toplumun verdiği değer.", "Toplumsal Statü", 5),
        Concept("Verilmiş Statü", "Doğumla, çaba dışı kazanılan statü.", "Toplumsal Statü", 5),
        Concept("Kazanılmış Statü", "Yetenek, eğitim ve çabayla elde edilen statü.", "Toplumsal Statü", 5),
        Concept("Anahtar Statü", "Bireyin kimliğini belirleyen, diğerlerine baskın statü.", "Toplumsal Statü", 5),
        Concept("Toplumsal Rol", "Statünün gerektirdiği görevleri yapma biçimi; statünün davranışa dökülmüş hali.", "Toplumsal Rol", 6),
        Concept("Rol Takımı", "Bir statüye bağlı yerine getirilmesi gereken tüm rollerin toplamı.", "Toplumsal Rol", 6),
        Concept("Rol Çatışması", "Bir rolün başka bir gruptaki rolle uyumsuz olması.", "Toplumsal Rol", 6),
        Concept("Anahtar Rol", "Bireyin rolleri arasında en önemli olanı.", "Toplumsal Rol", 6),
    ]

    # =====================================================================
    # TEST — 20 Soruluk Genel Değerlendirme
    # =====================================================================
    test_questions = [
        TestQuestion(1, "Aşağıdakilerden hangisi kültürün beş temel özelliğinden biri değildir?",
            {"A": "Kapsayıcı olması", "B": "Öğrenilmesi", "C": "Kalıtsal olması", "D": "Paylaşılması", "E": "Örüntülü olması"}),
        TestQuestion(2, "Maddi kültür ögelerinin manevi kültür ögelerinden daha hızlı değişmesi sonucu ortaya çıkan uyumsuzluğa ne ad verilir?",
            {"A": "Kültürel Relativizm", "B": "Kültürel Gecikme", "C": "Kültürleşme", "D": "Kültür Şoku", "E": "Etnosentrizm"}),
        TestQuestion(3, "Bir kişinin kendi kültürünü merkeze alıp başka kültürleri bu ölçütle yargılamasına ne ad verilir?",
            {"A": "Kültürel Relativizm", "B": "Kültürel Evrensellik", "C": "Etnosentrizm", "D": "Akkültürasyon", "E": "Difüzyon"}),
        TestQuestion(4, "Aşağıdakilerden hangisi 'kültürel süreçler' arasında yer almaz?",
            {"A": "Enkültürasyon", "B": "Akkültürasyon", "C": "Difüzyon", "D": "Anahtar Statü", "E": "Kültür Şoku"}),
        TestQuestion(5, "Fichter'e göre aşağıdakilerden hangisi kültürün işlevlerinden biri değildir?",
            {"A": "Toplumsal dayanışmayı sağlamak", "B": "Değerleri yorumlamak", "C": "Bireyin genetik yapısını belirlemek", "D": "Toplumun kimliği olmak", "E": "Kişiliğin oluşmasında başat faktör olmak"}),
        TestQuestion(6, "Bireyin biyolojik bir varlıktan toplumsal bir varlığa dönüşmesi sürecine ne ad verilir?",
            {"A": "Enkültürasyon", "B": "Toplumsallaşma", "C": "Statü Aktarımı", "D": "Modernleşme", "E": "Kültürleşme"}),
        TestQuestion(7, "Bir bireyin emeklilik sonrası yeni bir yaşam düzenine uyum sağlayarak değer ve davranışlarını temelden değiştirmesi hangi kavramla açıklanır?",
            {"A": "Başarısız Toplumsallaşma", "B": "Rol Çatışması", "C": "Yeniden Toplumsallaşma", "D": "Kültürel Gecikme", "E": "Statü Aktarımı"}),
        TestQuestion(8, "Aşağıdakilerden hangisi toplumsallaşma araçlarından biri değildir?",
            {"A": "Aile", "B": "Okul", "C": "Arkadaş grupları", "D": "Kitle iletişim araçları", "E": "Genetik kalıtım"}),
        TestQuestion(9, "Fikirleri tek taraflı olarak benimsetmeyi ve 'kabul ettirmeyi' amaçlayan yapay etkileme aracına ne ad verilir?",
            {"A": "Reklam", "B": "Kamuoyu", "C": "Propaganda", "D": "İdeoloji", "E": "Moda"}),
        TestQuestion(10, "Toplumsal değişme kavramıyla ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
            {"A": "Nesnel bir kavramdır, değer yargısı içermez", "B": "Teknoloji ve ideoloji iki temel dinamiğidir",
             "C": "Gelişme ile eş anlamlıdır ve daima olumlu bir yönü ifade eder", "D": "İnsan, zaman ve mekân üç temel ögesidir",
             "E": "İç ve dış kaynaklardan beslenir"}),
        TestQuestion(11, "Toplumsal değişmeyi zıtlıkların çatışmasıyla açıklayan diyalektik kuramın temsilcisi kimdir?",
            {"A": "Auguste Comte", "B": "Émile Durkheim", "C": "Karl Marx", "D": "Talcott Parsons", "E": "İbni Haldun"}),
        TestQuestion(12, "Geleneksel toplumdan sanayi toplumuna geçişte tabakalaşma alanındaki temel dönüşüm nedir?",
            {"A": "Kazanılmış statü yerine atfedilen statünün önem kazanması", "B": "Atfedilen statü yerine kazanılmış statünün önem kazanması",
             "C": "Statü kavramının tamamen ortadan kalkması", "D": "Geniş ailenin çekirdek aileye üstünlük sağlaması", "E": "Dinî otoritenin güçlenmesi"}),
        TestQuestion(13, "Max Weber'e göre sanayi toplumuna özgü, geleneksel otoritenin yerini alan otorite biçimi hangisidir?",
            {"A": "Karizmatik Otorite", "B": "Yasal Otorite", "C": "Babaerkil Otorite", "D": "Teokratik Otorite", "E": "Doğal Otorite"}),
        TestQuestion(14, "Lyotard'a göre postmodernizm, modernliğin hangi iddialarına karşı çıkar?",
            {"A": "Bireyselliğe ve özgürlüğe", "B": "Kesinlik ve evrensellik iddialarına", "C": "Bilim ve teknolojiye", "D": "Kapitalizme", "E": "Ulus devlete"}),
        TestQuestion(15, "Baudrillard'ın 'simülasyon' teziyle ilgili aşağıdakilerden hangisi doğrudur?",
            {"A": "Gerçeklik hiçbir zaman imajlarla yer değiştirmez", "B": "Postmodern dönemde gerçeğin yerini imajlar ve kültürel ürünler alır",
             "C": "Simülasyon yalnızca sanayi toplumlarında görülür", "D": "Simülasyon, modernliğin ekonomik boyutunu açıklar", "E": "Simülasyon kavramı Weber'e aittir"}),
        TestQuestion(16, "Bir bireyin toplumdaki konumuna, yani içinde yaşadığı grupta işgal ettiği mevkiye ne ad verilir?",
            {"A": "Rol", "B": "Statü", "C": "Norm", "D": "Kimlik", "E": "Kişilik"}),
        TestQuestion(17, "İşini iyi yapan bir temizlik işçisinin çevresinde yüksek saygınlık kazanması, hangi kavramla açıklanır?",
            {"A": "Statüsel Saygınlık", "B": "Anahtar Statü", "C": "Kişisel Saygınlık", "D": "Statü Aktarımı", "E": "Verilmiş Statü"}),
        TestQuestion(18, "Aşağıdakilerden hangisi 'verilmiş (ascribed) statü' belirleyicilerinden biri değildir?",
            {"A": "Yaş", "B": "Soy bağı", "C": "Cinsiyet", "D": "Eğitim", "E": "Biyolojik nitelikler"}),
        TestQuestion(19, "Bir kişinin sahip olduğu statülerden birinin diğerlerine baskın çıkarak kimliğini belirlemesine ne ad verilir?",
            {"A": "Rol Takımı", "B": "Anahtar Statü", "C": "Statü Aktarımı", "D": "Rol Çatışması", "E": "Genel Rol"}),
        TestQuestion(20, "'İyi bir baba olan birinin aynı zamanda iyi bir öğretmen olamaması' durumu hangi kavramla açıklanır?",
            {"A": "Roller Arası Pekiştirme", "B": "Rol Uzmanlaşması", "C": "Rol Çatışması", "D": "Rol Takımı", "E": "Anahtar Rol"}),
    ]

    answer_key_items = [
        AnswerItem(1, "C", "Kültür <b>öğrenilir</b>, doğuştan (kalıtsal) gelmez — bu, kültürü biyolojik özelliklerden ayıran en temel niteliktir."),
        AnswerItem(2, "B", "<b>Kültürel Gecikme</b> (Ogburn), maddi kültürün hızlı, manevi kültürün yavaş değişmesinden doğan boşluğu tanımlar."),
        AnswerItem(3, "C", "<b>Etnosentrizm</b>, kişinin kendi kültürünü ölçüt alıp diğerlerini yargılamasıdır; kültürel relativizm bunun tam tersidir."),
        AnswerItem(4, "D", "<b>Anahtar Statü</b> bir statü/rol kavramıdır, kültürel süreçlerle (enkültürasyon, akkültürasyon, difüzyon, kültür şoku) ilgili değildir."),
        AnswerItem(5, "C", "Fichter'e göre kültürün işlevleri toplumsaldır (dayanışma, kimlik, değer yorumlama, kişilik); genetik yapı biyolojik bir konudur, kültürün işlevi değildir."),
        AnswerItem(6, "B", "<b>Toplumsallaşma</b>, bireyin biyolojik varlıktan toplumsal varlığa dönüşme sürecinin tanımıdır."),
        AnswerItem(7, "C", "<b>Yeniden Toplumsallaşma (Resocialization)</b>, bireyin değer ve davranışlarını temelden değiştirmesidir; emeklilik gibi yeni roller bu sürece örnektir."),
        AnswerItem(8, "E", "Genetik kalıtım biyolojik bir aktarımdır; toplumsallaşma araçları aile, okul, arkadaş grupları ve kitle iletişim araçlarıdır."),
        AnswerItem(9, "C", "<b>Propaganda</b>, fikirleri tek taraflı benimsetmeyi ve 'kabul ettirmeyi' amaçlayan yapay etkileme aracıdır; reklam ise ticari amaçlıdır."),
        AnswerItem(10, "C", "Toplumsal değişme <b>nesnel</b> bir çatı kavramdır; gelişme ise değer yargısı içerir ve toplumsal değişmenin yalnızca özel (olumlu) bir görünümüdür, eş anlamlısı değildir."),
        AnswerItem(11, "C", "<b>Karl Marx</b>, toplumsal değişmeyi zıtlıkların çatışmasıyla açıklayan diyalektik kuramın temsilcisidir."),
        AnswerItem(12, "B", "Sanayi toplumunda doğuştan gelen (atfedilen) statüler yerine çabayla elde edilen (kazanılmış) statüler önem kazanır."),
        AnswerItem(13, "B", "Weber'e göre sanayi toplumuna özgü otorite biçimi <b>Yasal Otorite</b>dir; geleneksel otoritenin yerini alır."),
        AnswerItem(14, "B", "Lyotard'a göre postmodernizm, modernliğin kesinlik ve evrensellik iddialarına karşı çıkar, belirsizliği ve çoğulculuğu savunur."),
        AnswerItem(15, "B", "Baudrillard'a göre postmodern dönemde artık ekonomik/politik bir gerçeklik yoktur; yalnızca <b>kültürel ürünler ve imajlar</b> vardır."),
        AnswerItem(16, "B", "<b>Statü</b>, bireyin içinde yaşadığı grupta işgal ettiği konumdur; rol ise bu konumun gerektirdiği eylemdir."),
        AnswerItem(17, "C", "<b>Kişisel Saygınlık</b>, bireyin statüsünün gereklerini ne kadar başarıyla yerine getirdiğiyle ilgilidir — düşük statülü bir işte bile yüksek olabilir."),
        AnswerItem(18, "D", "Eğitim, kazanılmış (achieved) statünün belirleyicisidir; verilmiş statü doğuştan gelen özelliklere (yaş, soy, cinsiyet, biyolojik nitelikler) dayanır."),
        AnswerItem(19, "B", "<b>Anahtar Statü (Master Status)</b>, bireyin sahip olduğu statülerden birinin diğerlerine baskın çıkarak kimliğini belirlemesidir."),
        AnswerItem(20, "C", "<b>Rol Çatışması</b>, kişinin sahip olduğu bir rolün başka bir gruptaki rolüyle uyumsuz olması durumudur."),
    ]

    return CoursePack(
        course_code="SOSYOLOJİ",
        title='Sosyoloji<span class="accent-word">ye</span> Giriş',
        subtitle="Kültür, Toplumsallaşma, Değişme ve Statü-Rol Kuramlarına Bütüncül Bakış",
        description=(
            "Kültürün tanımından toplumsallaşma süreçlerine, davranış kalıplarından toplumsal değişme kuramlarına; "
            "modernizm-postmodernizm karşıtlığından statü ve rol kavramlarına uzanan final sınavı özeti."
        ),
        theme="forest",
        icon_text="S",
        chapters=chapters,
        glossary=glossary,
        test_title="Genel Değerlendirme Testi",
        test_subtitle="Kültür, toplumsallaşma, değişme, statü ve rol üzerine kapsamlı çoktan seçmeli test",
        test_instructions="Aşağıdaki sorularda beş seçenekten yalnızca birini işaretleyiniz. Süre: 30 dakika.",
        test_questions=test_questions,
        answer_key_intro="Her sorunun doğru cevabı ve kısa gerekçesi aşağıda yer almaktadır.",
        answer_key_items=answer_key_items,
        overview_lead=(
            "Bu ders; bireyin <b>kültürle biçimlenmesinden</b> toplumun yapısal <b>değişimine</b>, gündelik "
            "hayattaki <b>statü ve rollere</b> uzanan sosyolojik bakış açısının temel araçlarını bir bütün olarak sunar."
        ),
        overview_cards=[
            {"title": "Kültür", "text": "Tanımı, 5 temel özelliği, ögeleri ve kültürel süreçler."},
            {"title": "Toplumsallaşma", "text": "Bireyin toplumsal varlığa dönüşümü ve davranış kalıpları."},
            {"title": "Toplumsal Değişme", "text": "Değişmenin dinamikleri, kuramları ve sanayileşme süreci."},
            {"title": "Modernizm / Postmodernizm", "text": "Akılcılaşmadan simülasyona iki karşıt paradigma."},
            {"title": "Toplumsal Statü", "text": "Verilmiş ve kazanılmış statülerin belirleyicileri."},
            {"title": "Toplumsal Rol", "text": "Statünün davranışa dökülmüş hali ve rol kavramları."},
        ],
        overview_flow=[
            ("Kültür", "Tanım ve süreçler"),
            ("Birey & Toplum", "Toplumsallaşma / kalıplar"),
            ("Yapısal Değişim", "Değişme / modernizm"),
            ("Statü & Rol", "Konum ve eylem"),
        ],
        overview_note=(
            "Sınavda en çok karıştırılan yer, <b>Statü ile Rol</b> ayrımıdır: statü bireyin toplumdaki konumu, "
            "rol ise o konumun gerektirdiği eylemdir — 'nerede olunduğu' ile 'ne yapıldığı' birbirine karıştırılmamalıdır."
        ),
    )
