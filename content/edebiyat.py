# -*- coding: utf-8 -*-
"""TÜRK DİLİ VE EDEBİYATI 5, 6 VE 8 — Görsel Ders Notu Kitabı, içerik tanımı.
Kaynak: 'edebiyat 5-6-8.pdf' (ham metin özet, 11 sayfa).

Not: Kaynak PDF'in kendi fihristi 6 bölüm vaat eder, ancak ham metin yalnızca
5 bölümü kapsar — 6. Bölüm (Deneme, Söylev/Nutuk Türleri, Anlatım Biçimleri ve
Düşünceyi Geliştirme Yolları) kaynak metinde hiç yer almaz. Uydurma içerik
eklememek için bu kitap kaynakta fiilen bulunan 5 bölüme dayanır.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from content_model import (
    Person, KeyTerm, Callout, FlowStep, FlowDiagram, ComparisonTable,
    InfoCard, BulletBlock, Chapter, ChapterPage, Concept, CoursePack,
    QAItem, DistinctionPair, MatchRow, TestQuestion, AnswerItem,
)

SAIT_FAIK = Person(
    id="saitfaik", name="Sait Faik Abasıyanık", years="1906–1954",
    tagline="Durum Hikâyesinin Türk Edebiyatındaki Öncüsü",
    bio=["Klasik serim-düğüm-çözüm kalıbını kırarak insan yaşamından anlık <b>kesitler</b> sunan durum hikâyesi "
         "tarzını Türk edebiyatına kazandırmış, olayı değil bireyin iç dünyasını ve yalnızlığını merkeze almıştır."],
    key_work="Semaver, Lüzumsuz Adam",
)

MEHMET_AKIF = Person(
    id="mehmetakif", name="Mehmet Âkif Ersoy", years="1873–1936",
    tagline="Manzum Hikâyenin Büyük Ustası",
    bio=["Şiirin ölçü ve uyak gibi biçimsel özelliklerini korurken içine olay, zaman ve mekân barındıran "
         "<b>manzum hikâye</b> türünün en büyük ustası kabul edilir; bu tarzın en tanınmış örneği <b>Küfe</b> "
         "adlı eseridir."],
    key_work="Safahat, Küfe",
)

RUSEN_ESREF = Person(
    id="rusenesref", name="Ruşen Eşref Ünaydın", years="1892–1959",
    tagline="Türk Edebiyatında İlk Mülakatın Yazarı",
    bio=["<b>Diyorlar ki</b> adlı eseriyle Türk edebiyatındaki ilk mülakat örneğini vermiş; Mustafa Kemal "
         "Atatürk'ü Türk basınına tanıtan 'Anafartalar Kumandanı Mustafa Kemal'le Mülakat' röportajıyla da "
         "tanınır."],
    key_work="Diyorlar ki",
)

OGUZ_ATAY = Person(
    id="oguzatay", name="Oğuz Atay", years="1934–1977",
    tagline="Türk Edebiyatında Biyografik Romanın Öncüsü",
    bio=["<b>Bir Bilim Adamının Romanı</b> adlı eserinde kendi hocası olan Prof. Dr. Mustafa İnan'ın "
         "yoksulluktan bilimsel zirveye uzanan hayatını anlatarak Türk edebiyatının en önemli biyografik "
         "romanlarından birini kaleme almış; modernist anlatım teknikleriyle de tanınır."],
    key_work="Bir Bilim Adamının Romanı, Tutunamayanlar",
)


def get_pack() -> CoursePack:

    # =====================================================================
    # BÖLÜM 1 — (Edebiyat 5) Edebiyat-Toplum İlişkisi, Akımlar, Hikâye ve Temel Ögeler
    # =====================================================================
    ch1 = Chapter(
        number=1,
        title="Edebiyat-Toplum İlişkisi, Akımlar, Hikâye ve Temel Ögeler",
        subtitle="Edebiyatın toplumla kurduğu köprüden Cumhuriyet dönemi hikâyeciliğine ve cümlenin iskeletine",
        key_terms=[
            KeyTerm("Edebî Akım", "Belli bir sanatkâr grubunun aynı dönemde ortak bir dünya görüşü ve estetik anlayış çerçevesinde oluşturduğu hareketlerin bütünü."),
            KeyTerm("Durum Hikâyesi", "Çehov tarzı hikâyede serim-düğüm-çözüm planı olmadan insan yaşamından anlık bir kesit sunulmasıdır; öncüsü Sait Faik Abasıyanık'tır."),
            KeyTerm("Yüklem", "Kip ve zaman bildirerek yargıyı ortaya koyan, cümlenin bulunmazsa olmaz temel unsuru."),
            KeyTerm("Sözde Özne", "Edilgen çatılı cümlelerde işten etkilenen nesnenin zorunlu olarak özne görevini almasıdır."),
        ],
    )
    ch1.pages.append(
        ChapterPage()
        .add_terms(ch1.key_terms)
        .add_block(BulletBlock(1, "Edebiyat ve Toplum İlişkisi", [
            "Edebiyat ilhamını toplumdan alır; kültürü gelecek nesillere aktararak toplumsal birliğin sağlanmasına aracı olur.",
            "Edebiyatı insandan, insanı da toplumdan ayırmak imkânsızdır — savaşlar, göçler, ekonomik krizler gibi toplumsal olaylar doğrudan romanların ve hikâyelerin konusunu oluşturur.",
            "<b>Edebî Akım (Sanat Akımı):</b> Belli bir sanatkâr grubunun belli bir dönemde, müşterek dünya görüşü ve edebiyat anlayışı çerçevesinde oluşturduğu hareketlerin bütünüdür; her akım ortaya çıktığı toplumun sosyal ve siyasal hayatının bir sonucudur, farklılaşma ihtiyacından doğar.",
        ]))
        .add_table(ComparisonTable(
            "Türk Edebiyatına Özgü Şiir Akımları",
            ["Akımın Adı", "Temel Özellikleri", "Temsilcileri"],
            [
                ["Türkî-i Basit (Basit Türkçe)", "Divan şiirinde Türkçe kelimeler kullanmayı amaçlamış; atasözü ve halk tabirleri şiire girmiştir.", "Aydınlı Visali, Edirneli Nazmi"],
                ["Mahallîleşme", "Biçimde yerlilik ve İstanbul ağzı esas alınmış; âşık tarzı ile divan tarzı birleşmiştir.", "Necati, Nedim, Enderunlu Vasıf"],
                ["Sebk-i Hindi", "Şiirde anlam derinleşmiş ve kapalı (soyut) hâle gelmiş; tasavvufa geniş yer verilmiştir.", "Şeyh Galip, Neşati, Naili"],
                ["Garip Akımı", "Ölçü, uyak ve tüm nazım kurallarına karşı çıkılmış; halkın günlük dili kullanılmıştır.", "Orhan Veli, Melih Cevdet Anday, Oktay Rifat"],
            ]
        ))
    )
    ch1.pages.append(
        ChapterPage(continue_tag="Cumhuriyet Dönemi Hikâyesi")
        .add_block(BulletBlock(2, "Cumhuriyet Dönemi'nde Hikâye (1923-1960)", [
            "<b>1923-1940 Arası:</b> Gözleme dayalı gerçekçiliğe önem verilmiştir; modern yaşayışın yanlış anlaşılması, geçim sıkıntısı ve kadınların durumu işlenir (Reşat Nuri, Yakup Kadri vb.).",
            "<b>1940-1960 Arası — Dört Eğilim:</b> Klasik olay hikâyesi dışında dört farklı hikâye türü ortaya çıkar.",
            "<b>Toplumcu Gerçekçiler:</b> İşçilerin, köylülerin sorunlarını ve büyük şehre göçü ideolojik bir bakışla anlatırlar (Orhan Kemal, Yaşar Kemal, Sabahattin Ali).",
            "<b>Bireyin İç Dünyasını Esas Alanlar:</b> Toplumsal olaylardan çok bireyin ruhsal durumunu işlerler (Peyami Safa, A. Hamdi Tanpınar).",
            "<b>Modernizmi Esas Alanlar:</b> Serim-düğüm-çözüm kuralını yıkarlar; insanın yalnızlığını ve yabancılaşmasını kurgularlar (Sait Faik, Haldun Taner, Oğuz Atay).",
            "<b>Millî ve Dinî Duyarlılıkları Yansıtanlar:</b> Kültürel bağlara ve dinî motiflere odaklanırlar.",
        ]))
        .add_person(SAIT_FAIK)
        .add_callout(Callout("caution", "Dikkat / Püf Noktası: Olay Hikâyesi mi, Durum Hikâyesi mi?",
            "Olay Hikâyesinde (Maupassant tarzı) 'serim, düğüm, çözüm' planına katı uyma zorunluluğu vardır. "
            "Durum Hikâyesinde (Çehov tarzı) ise bu bölümler yoktur, insan yaşamından anlık bir <b>kesit</b> "
            "sunulur, olaylar sonuçlanmadan bitebilir. Türk edebiyatında durum hikâyesinin öncüsü "
            "<b>Sait Faik Abasıyanık</b>'tır."))
    )
    ch1.pages.append(
        ChapterPage(continue_tag="Cümlenin Temel Ögeleri")
        .add_block(BulletBlock(3, "Cümlenin Temel Ögeleri", [
            "Bir cümleyi oluşturan iskelete <b>temel ögeler</b> denir; yalnızca Yüklem ve Özne'den oluşur.",
            "<b>Yüklem:</b> Kip ve zaman bildirerek yargıyı ortaya koyan temel unsurdur; yüklemsiz cümle olmaz. "
            "Yalnızca fiiller değil isimler, tamlamalar, deyimler ve edatlar da yüklem olabilir (Örn: Onları "
            "büyüleyen manzara, yemyeşil kırlardı — sıfat tamlaması yüklem olmuştur).",
            "<b>Özne:</b> Yüklemin bildirdiği işi yapan veya oluş içinde bulunan ögedir; yükleme 'Kim?' veya "
            "'Ne?' sorularak bulunur. Dört çeşit özne vardır.",
        ]))
        .add_table(ComparisonTable(
            "Özne Çeşitleri",
            ["Özne Türü", "Açıklama", "Örnek"],
            [
                ["Gerçek (Açık) Özne", "Cümlede kelime olarak açıkça yazılan öznedir.", "Öğrenciler top oynuyordu."],
                ["Gizli Özne", "Cümlede yazmayan ama yüklemin şahıs ekinden anlaşılan öznedir.", "Ne annesine ne babasına söyler. (Gizli özne: O)"],
                ["Sözde Özne", "Edilgen çatılı cümlelerde işten etkilenen nesnenin zorunlu olarak özne görevi almasıdır.", "Yeni alınan ev temizlendi. (Sözde özne: Ev)"],
                ["Ortak Özne", "Sıralı veya bağlı cümlelerde birden çok yüklemin aynı özneye bağlanmasıdır.", "Mustafa olayı duymuş, hemen yola çıkmıştı."],
            ]
        ))
        .add_summary("Edebiyat toplumdan ayrı düşünülemez; sanat akımları da toplumların sosyal ve siyasal "
            "koşullarının bir ürünüdür. Cumhuriyet dönemi hikâyeciliği 1940 sonrasında toplumcu gerçekçilik, "
            "bireyin iç dünyası, modernizm ve millî-dinî duyarlılık olmak üzere dört eğilime ayrılır. Dil "
            "bilgisinde cümlenin temel ögeleri yalnızca yüklem ve özneden oluşur; özne gerçek, gizli, sözde ve "
            "ortak özne olmak üzere dört çeşittir.")
    )

    # =====================================================================
    # BÖLÜM 2 — (Edebiyat 5) Şiir, Makale, Sohbet/Fıkra ve Cümlenin Yardımcı Ögeleri
    # =====================================================================
    ch2 = Chapter(
        number=2,
        title="Şiir, Makale, Sohbet/Fıkra Türleri ve Cümlenin Yardımcı Ögeleri",
        subtitle="Dönemsel şiir anlayışlarından öğretici metinlere, cümlenin yardımcı öge ve dışı unsurlarına",
        key_terms=[
            KeyTerm("Manzum Hikâye", "Yaşanmış veya yaşanması muhtemel olayların şiir biçiminde, ölçü ve uyakla ama içinde olay-zaman-mekân barındıracak şekilde anlatılmasıdır."),
            KeyTerm("Makale", "Bilgi vermek, bir tezi kanıtlamak veya bir düşünceyi bilimsel verilerle savunmak amacıyla yazılan, anlatımı nesnel ve ciddi olan yazı türü."),
            KeyTerm("Ara Söz (Ara Cümle)", "Cümle içinde fazladan bilgi veren, iki virgül veya iki kısa çizgi arasında gösterilen ve çıkarıldığında anlamı bozulmayan ifade."),
            KeyTerm("Dolaylı Tümleç", "İsmin -e, -de, -den ekini alarak yüklemin yerini bildiren, 'kime/nereye, kimde/nerede, kimden/nereden' sorularıyla bulunan yardımcı öge."),
        ],
    )
    ch2.pages.append(
        ChapterPage()
        .add_terms(ch2.key_terms)
        .add_block(BulletBlock(1, "Şiir: Tanzimat'tan Servetifünun'a", [
            "<b>Tanzimat Şiiri (1. Dönem):</b> 'Toplum için sanat' anlayışı hâkimdir; hürriyet, eşitlik, adalet, "
            "vatan gibi yeni temalar işlenir. Biçim eskidir — kaside, gazel gibi divan nazım biçimleri "
            "sürdürülür (Örn: Namık Kemal).",
            "<b>Servetifünun Şiiri:</b> 'Sanat sanat içindir' anlayışı hâkimdir; siyasal baskılar nedeniyle "
            "toplumsal konulardan kaçılmış, melankoli, doğa ve bireysel yalnızlık işlenmiştir. Parnasizm ve "
            "Sembolizm etkilidir; dil Arapça-Farsça kelimelerle ağırdır (Örn: Tevfik Fikret, Cenap Şahabettin).",
            "<b>Fecr-i Âti Şiiri:</b> Servetifünun'a tepki olarak doğsa da onu taklit etmekten öteye "
            "geçememiştir; dil ağır, temalar (aşk, doğa) bireyseldir (Örn: Ahmet Haşim).",
        ]))
    )
    ch2.pages.append(
        ChapterPage(continue_tag="Saf Şiir, Millî Edebiyat ve Manzum Hikâye")
        .add_block(BulletBlock(2, "Saf Şiir'den Türk Dünyası Edebiyatına", [
            "<b>Saf (Öz) Şiir Anlayışı:</b> İdeolojiye ve öğüt vermeye (didaktizme) kesinlikle karşı çıkılır; "
            "amaç yalnızca estetik haz ve 'musiki/ahenk' yaratmaktır. Dili imge ve çağrışımlarla doludur; "
            "'sanat sanat içindir' ilkesine bağlıdır (Örn: Ahmet Haşim, Yahya Kemal, Necip Fazıl Kısakürek).",
            "<b>Millî Edebiyat Dönemi Şiiri:</b> 'Toplum için sanat' anlayışı hâkimdir; İstanbul Türkçesiyle, "
            "sade bir dille ve hece ölçüsüyle yazılır. Türkçülük, vatan sevgisi ve kahramanlık temaları öne "
            "çıkar (Örn: Ziya Gökalp, Mehmet Emin Yurdakul).",
            "<b>Türk Dünyası Edebiyatında Şiir:</b> Türkiye dışındaki Türk devletlerinde millî bilinci uyanık "
            "tutmak için yazılan eserlerdir; özgürlük ve anadile bağlılık işlenir (Örn: Bahtiyar Vahapzade).",
        ]))
        .add_person(MEHMET_AKIF)
        .add_callout(Callout("insight", "Kavram: Manzum Hikâye",
            "Yaşanmış veya yaşanması muhtemel olayların şiir (nazım) biçiminde anlatılmasıdır. Metin dışarıdan "
            "şiir gibi görünür — ölçüsü ve uyağı vardır — ama içinde olay, zaman ve mekân barındıran bir "
            "hikâyedir. En büyük ustası, <b>Küfe</b> adlı eseriyle Mehmet Âkif Ersoy'dur."))
    )
    ch2.pages.append(
        ChapterPage(continue_tag="Makale, Sohbet ve Fıkra")
        .add_block(BulletBlock(3, "Makale", [
            "Bilgi vermek, bir tezi kanıtlamak veya bir düşünceyi bilimsel verilerle savunmak amacıyla yazılan "
            "yazılara <b>makale</b> denir. Anlatımı nesnel (objektif) ve ciddidir; açıklayıcı ve tartışmacı "
            "anlatım biçimleri kullanılır, ileri sürülen fikir mutlaka kanıtlanmalıdır.",
            "<b>İlk Makale:</b> Türk edebiyatında ilk makale, Tanzimat Dönemi'nde (1860) Şinasi'nin çıkardığı "
            "Tercüman-ı Ahval gazetesinde yayımlanan 'Tercüman-ı Ahval Mukaddimesi'dir.",
        ]))
        .add_table(ComparisonTable(
            "Sohbet (Söyleşi) ile Fıkra (Köşe Yazısı) Farkı",
            ["Özellik", "Sohbet (Söyleşi)", "Fıkra (Köşe Yazısı)"],
            [
                ["Dil ve Üslup", "Yazar karşısında biri varmış gibi 'senli benli' konuşur, okura sorular sorar.", "Daha ciddi, güncel bir dille okuru ve kamuoyunu yönlendirmeyi amaçlar."],
                ["Konu ve Ömür", "Gündelik veya kalıcı herhangi bir konu işlenebilir; yazının ömrü uzundur.", "Sadece güncel olaylar işlenir; konu eskiyince fıkranın da ömrü biter."],
                ["Önemli Temsilciler", "Şevket Rado (Eşref Saat), Ahmet Rasim (Ramazan Sohbetleri).", "Haldun Taner, Ahmet Rasim, Peyami Safa."],
            ]
        ))
        .add_callout(Callout("focus", "Dikkat / Püf Noktası: Makale ile Fıkra/Sohbet Farkı",
            "Sınavda bu ayrım kesin gelir: Makalede yazarın iddiasını <b>kanıtlama ve ispatlama</b> zorunluluğu "
            "vardır. Sohbet ve Fıkra türlerinde ise yazarın kişisel görüşleri ağır basar, okuyucuya tezi "
            "ispatlama zorunluluğu kesinlikle yoktur."))
    )
    ch2.pages.append(
        ChapterPage(continue_tag="Cümlenin Yardımcı Ögeleri")
        .add_block(BulletBlock(4, "Cümlenin Yardımcı Ögeleri ve Cümle Dışı Unsurlar", [
            "<b>Nesne (Düz Tümleç):</b> Öznenin yaptığı işten etkilenen ögedir. 'Neyi?, Kimi?' soruları "
            "Belirtili Nesneyi (-i hâli); 'Ne?' sorusu ise Belirtisiz Nesneyi (yalın hâl) buldurur.",
            "<b>Dolaylı Tümleç (Yer Tamlayıcısı):</b> İsmin -e, -de, -den (yönelme, bulunma, ayrılma) eklerini "
            "alarak yüklemin yerini bildirir; kime/kimde/kimden, nereye/nerede/nereden sorularıyla bulunur.",
            "<b>Zarf Tümleci:</b> Yüklemi zaman, durum, miktar veya sebep yönünden niteler; nasıl, ne zaman, "
            "ne kadar sorularına cevap verir.",
            "<b>Cümle Dışı Unsurlar (CDU):</b> Cümlenin ana ögelerinden (özne, yüklem, nesne vb.) hiçbiri "
            "olmayan bağlaçlar ('fakat, ancak'), ünlemler ('Hey!') ve hitaplardır.",
            "<b>Ara Söz / Ara Cümle:</b> Cümle içinde fazladan bilgi veren veya bir ögeyi açıklayan, iki "
            "virgül veya iki kısa çizgi arasında gösterilen; cümleden çıkarıldığında anlamı bozulmayan ifadedir.",
        ]))
        .add_summary("Edebiyat 5 müfredatı, şiirin sanat için yazılan süslü dönemlerinden (Servetifünun) "
            "kurtulup heceyle halka inmesini (Millî Edebiyat), nesir türünde ise edebiyatın bilimsel "
            "makaleler ve senli benli sohbetlerle okuru eğitmesini (Şevket Rado, Tanpınar) merkeze alır. Dil "
            "bilgisinde nesne, dolaylı tümleç ve zarf tümleci cümlenin yardımcı ögelerini; ara söz ise cümle "
            "dışı unsurları oluşturur.")
    )

    # =====================================================================
    # BÖLÜM 3 — (Edebiyat 6) Roman ve Tiyatro (1923-1980) ile Anlatım Bozuklukları
    # =====================================================================
    ch3 = Chapter(
        number=3,
        title="Roman ve Tiyatro (1923-1980 Evresi) ile Anlatım Bozuklukları",
        subtitle="Cumhuriyet dönemi romanından modern tiyatro türlerine, sık çıkan anlatım bozukluklarına",
        key_terms=[
            KeyTerm("Trajedi", "Konusunu tarih ve mitolojiden alan, kişilerinin soylu ve tanrısal olduğu, üç birlik kuralına uyulan; kötü söz ve çirkin olayların sahnede gösterilmediği tiyatro türü."),
            KeyTerm("Dram", "Hayatın hem acıklı hem gülünç yönlerini bir arada veren, her kesimden insanın yer aldığı ve üç birlik kuralına uyma zorunluluğu olmayan modern tiyatro türü."),
            KeyTerm("Epik Tiyatro", "Türk edebiyatında Haldun Taner'in Keşanlı Ali Destanı ile en önemli örneğini verdiği tiyatro anlayışı."),
            KeyTerm("Anlatım Bozukluğu", "Cümlede anlatımın açık, duru ve yalın olmamasından kaynaklanan; gereksiz kelime, çelişen kelime veya yanlış yerde kullanılan sözcüklerden doğan anlamsal hata."),
        ],
    )
    ch3.pages.append(
        ChapterPage()
        .add_terms(ch3.key_terms)
        .add_block(BulletBlock(1, "Cumhuriyet Dönemi Romanı (1923-1980)", [
            "<b>1. Evre (1923-1950):</b> Anadolu'ya yöneliş, Kurtuluş Savaşı yılları, aydın-köylü çatışması ve "
            "yanlış Batılılaşma ana konulardır.",
            "<b>Önemli Eser — Yaban (Yakup Kadri Karaosmanoğlu):</b> Aydın bir subay olan Ahmet Celâl'in "
            "gözünden Anadolu köylüsünün sefaleti, cehaleti ve aydın-halk kopukluğu en sert biçimde anlatılır.",
            "<b>2. Evre (1950-1980):</b> Köy Enstitüsü çıkışlı yazarların etkisiyle ağa-köylü çatışması, "
            "köyden kente göç, Almanya'ya işçi göçü ve topraksız köylünün sorunları işlenir.",
            "<b>Önemli Eserler:</b> <b>İnce Memed</b> (Yaşar Kemal) — Çukurova'da zalim Abdi Ağa'ya karşı "
            "dağa çıkan Memed'in efsaneleşen isyanı; <b>Yılkı Atı</b> (Abbas Sayar) — yaşlanıp işe yaramadığı "
            "için doğaya salınan Dorukısrak adlı atın hikâyesi üzerinden doğa-insan ve emek ilişkisi işlenir.",
        ]))
    )
    ch3.pages.append(
        ChapterPage(continue_tag="Cumhuriyet Dönemi Tiyatrosu")
        .add_callout(Callout("insight", "Dünya Edebiyatında Roman",
            "Roman türünün dünyadaki ilk başarılı örneği <b>Cervantes'in Don Kişot</b> adlı eseridir. "
            "Sınavlarda sıkça sorulan <b>Yaşlı Adam ve Deniz</b> ise Ernest Hemingway'e aittir; Santiago adlı "
            "yaşlı balıkçının doğayla (kılıçbalığıyla) olan varoluşsal mücadelesini anlatır."))
        .add_block(BulletBlock(2, "Cumhuriyet Dönemi Tiyatrosu ve Yazar-Eser Eşleştirmeleri", [
            "Çağdaş Türk tiyatrosunun kurumsallaşmasında ve Batı seviyesine ulaşmasında en büyük pay, "
            "<b>Küçük Sahne Tiyatrosu</b>'nu kuran <b>Muhsin Ertuğrul</b>'a aittir.",
        ]))
        .add_table(ComparisonTable(
            "Sınavlık Yazar - Eser - Tür Eşleştirmeleri",
            ["Yazar", "Eser", "Tür / Konu"],
            [
                ["Turan Oflazoğlu", "Genç Osman", "Trajedi — Osmanlı tarihinden alınan, devletin bozulan yapısını düzeltmek isterken öldürülen padişahın hikâyesi."],
                ["Orhan Asena", "Gılgameş", "Dram — Sümer mitolojisinden alınan, insanın ölümsüzlük arayışı ve acizliği."],
                ["Ahmet Kutsi Tecer", "Bir Pazar Günü", "Komedi (Modern orta oyunu) — Toplumdaki ikiyüzlülük ve paranın gücü."],
                ["Haldun Taner", "Keşanlı Ali Destanı", "Türk edebiyatında Epik Tiyatro'nun en önemli örneği."],
            ]
        ))
    )
    ch3.pages.append(
        ChapterPage(continue_tag="Modern Tiyatro Türleri ve Anlatım Bozuklukları")
        .add_table(ComparisonTable(
            "Trajedi, Komedi ve Dram Arasındaki Farklar",
            ["Tür", "Konu ve Kişiler", "Kural"],
            [
                ["Trajedi", "Tarih ve mitolojiden alınır; kişiler soylular ve tanrılardır. Kötü söz ve çirkin olaylar sahnede gösterilmez.", "Üç birlik kuralına (yer, zaman, olay) uyulur."],
                ["Komedi", "Günlük hayattan alınır; kişiler sıradan halktır. Kaba şakalara yer verilir, çirkin olaylar sahnede gösterilir.", "Üç birlik kuralına uyulur."],
                ["Dram", "Hayatın hem acıklı hem gülünç yönlerini bir arada verir; her kesimden insan vardır.", "Üç birlik kuralına uyma zorunluluğu YOKTUR."],
            ]
        ))
        .add_block(BulletBlock(3, "Anlatım Bozuklukları (Hap Bilgiler)", [
            "<b>Gereksiz Kelime Kullanılması:</b> Eş veya yakın anlamlı kelimelerin aynı cümlede kullanılmasıdır "
            "(Hatalı: 'faydasız, lüzumsuz olduklarına hükmetmek' — ikisi de aynı anlama gelir).",
            "<b>Anlamca Çelişen Kelimelerin Kullanılması:</b> Kesinlik ve ihtimal bildiren kelimelerin bir "
            "arada kullanılmasıdır (Hatalı: 'Elbette istediğin kitabı sana belki getirebilirim.').",
            "<b>Kelimenin Yanlış Anlamda Kullanılması:</b> Anlamca veya sesçe birbirine benzeyen kelimelerin "
            "karıştırılmasıdır (Hatalı: 'yaklaşık olması' yerine 'yakın olması' gerekir).",
            "<b>Kelimenin Yanlış Yerde Kullanılması:</b> Genellikle zarf ve sıfatların yer değiştirmesinden "
            "kaynaklanır (Hatalı: 'Yeni eve geldim ki...' yerine 'Eve yeni geldim ki...').",
            "<b>Deyim ve Atasözlerinin Yanlış Kullanılması:</b> Deyimlerin kalıbının bozulması veya bağlama "
            "uygun olmayan deyim kullanılmasıdır.",
        ]))
        .add_summary("Edebiyat 6 müfredatı; romanda Anadolu'nun ve insanın gerçek yüzünü acımasızca çizen "
            "(Yaban, İnce Memed), tiyatroda ise insanın zaaflarını ve tarihî gerçekliklerini sahneleyen "
            "(Genç Osman, Gılgameş) 'gerçekçi' bir edebî dönüşümü sınavın merkezine alır. Trajedi-Komedi-Dram "
            "ayrımı ile anlatım bozuklukları, dil bilgisi sorularının en sık çıkan başlıklarıdır.")
    )

    # =====================================================================
    # BÖLÜM 4 — (Edebiyat 6) Eleştiri (Tenkit), Mülakat ve Röportaj Türleri
    # =====================================================================
    ch4 = Chapter(
        number=4,
        title="Eleştiri (Tenkit), Mülakat ve Röportaj Türleri",
        subtitle="Öğretici metin türlerinin tanımları, alt türleri ve edebiyatımızdaki ilk örnekleri",
        key_terms=[
            KeyTerm("Eleştiri (Tenkit)", "Bir sanat ya da düşünce eserini tanıtırken zayıf ve güçlü yönlerini belirtme, eserin gerçek değerini yansıtma amacıyla yazılan yazı türü."),
            KeyTerm("İzlenimsel (Empresyonist) Eleştiri", "Eleştirmenin eseri tamamen kendi zevkine, algısına ve ölçülerine göre öznel biçimde değerlendirdiği eleştiri türü."),
            KeyTerm("Mülakat (Görüşme)", "Bir gazetecinin ünlü ya da uzman bir kişiyle yaptığı, soru-cevap tekniğine dayalı görüşmeleri aktardığı yazı türü."),
            KeyTerm("Röportaj", "Bir sorunu dile getirmek, toplumu aydınlatmak amacıyla bilgi, belge ve fotoğraflardan yararlanılarak hazırlanan araştırmaya dayalı metin türü."),
        ],
    )
    ch4.pages.append(
        ChapterPage()
        .add_terms(ch4.key_terms)
        .add_block(BulletBlock(1, "Eleştiri (Tenkit) ve Türleri", [
            "<b>Eleştiri (Tenkit):</b> Bir sanat ya da düşünce eserini tanıtırken zayıf ve güçlü yönlerini "
            "belirtme, yazarın veya eserin gerçek değerini yansıtma amacıyla yazılır.",
            "<b>Otokritik (Özeleştiri):</b> Bir kimsenin kendi eserini veya kendini eleştirmesi durumudur.",
            "<b>Eleştirmen Tavrına Göre:</b> İzlenimsel (Empresyonist) Eleştiri — eleştirmen eseri kendi "
            "zevkine göre öznel değerlendirir; Nesnel (Bilimsel) Eleştiri — eleştirmen kişisel hislerini bir "
            "kenara bırakıp bilimsel ölçütlerle tarafsız değerlendirir.",
        ]))
        .add_table(ComparisonTable(
            "Konusuna Göre Eleştiri Türleri",
            ["Tür", "Odak Noktası"],
            [
                ["Eseri Konu Alan", "Eserin kurgusu, teması ve anlatım tekniği incelenir."],
                ["Sanatçıya Yönelik", "Eser ile yazarın hayatı ve psikolojisi arasındaki ilişki incelenir."],
                ["Topluma Yönelik", "Eserin doğduğu toplumsal şartlar (sosyolojik yapı) merkeze alınır."],
                ["Okura Dönük", "Eserin okurda uyandırdığı etki ve coşku ifade edilir."],
                ["Tarihsel Eleştiri", "Eser, yazıldığı dönemin tarihsel şartları dikkate alınarak incelenir."],
            ]
        ))
        .add_callout(Callout("focus", "Dikkat / Sınav Püf Noktası: Eleştiride İlkler",
            "Türk edebiyatında Batılı anlamda ilk eleştiri yazısı, <b>Namık Kemal</b>'in yazdığı 'Lisan-ı "
            "Osmanînin Edebiyatı Hakkında Bazı Mülâhâzâtı Şâmildir' makalesidir. Yine Namık Kemal'in Ziya "
            "Paşa'ya karşı yazdığı 'Tahrib-i Harabat' adlı eseri ise Türk edebiyatındaki <b>ilk eleştiri "
            "kitabı</b>dır."))
    )
    ch4.pages.append(
        ChapterPage(continue_tag="Mülakat ve Röportaj")
        .add_block(BulletBlock(2, "Mülakat (Görüşme) ve Röportaj", [
            "<b>Mülakat (Görüşme):</b> Bir gazetecinin ünlü ya da uzman bir kişiyle yaptığı görüşmeleri "
            "aktardığı yazılardır; soru-cevap tekniği esastır.",
            "<b>İlk Örnek:</b> Türk edebiyatında ilk mülakat örneği, Ruşen Eşref Ünaydın'ın 'Diyorlar ki' "
            "adlı eseridir.",
            "<b>Kritik Bilgi:</b> Mustafa Kemal Atatürk'ü Türk basınına tanıtan mülakatı ('Anafartalar "
            "Kumandanı Mustafa Kemal'le Mülakat') da yine Ruşen Eşref Ünaydın yapmıştır.",
            "<b>Röportaj:</b> Bir sorunu dile getirmek, toplumu aydınlatmak amacıyla bilgi, belge ve "
            "fotoğraflardan yararlanılarak hazırlanan araştırmaya yönelik metinlerdir (Önemli temsilcisi: "
            "Yaşar Kemal).",
        ]))
        .add_person(RUSEN_ESREF)
        .add_table(ComparisonTable(
            "Mülakat ve Röportaj Farkı",
            ["Özellik", "Mülakat (Görüşme)", "Röportaj"],
            [
                ["Odak Noktası", "Kişi ön plana çıkartılır.", "Konu (toplumsal sorun) ön plana çıkartılır."],
                ["Muhatap", "Alanında uzman veya ünlü kişilerle yapılır.", "Herhangi bir kişiyle (sıradan vatandaş, sokak çocukları vb.) yapılabilir, uzmanlık gerekmez."],
                ["Yazarın Tutumu", "Yazar kendi görüşlerini ve yorumunu yansıtabilir; öznel bilgiler içerebilir.", "Yazar kendi görüşünü yansıtmaz, anlatımda nesnel kalmak zorundadır."],
                ["Görsel Kullanımı", "Sadece kişi ile çekilmiş bir fotoğraf kullanılır.", "Konuyu yansıtacak belge, resim ve birden fazla fotoğrafla zenginleştirilir."],
            ]
        ))
        .add_summary("Edebiyat 6'daki öğretici metinler (eleştiri, mülakat, röportaj), edebiyatın yalnızca "
            "hayal ürünü olmadığını; aynı zamanda bir sanat eserini bilimsel olarak tarttığını (eleştiri) ve "
            "sokağın nabzını gazete sayfalarına taşıdığını (mülakat/röportaj) kanıtlayan gerçekçi türlerdir. "
            "Sınavda mülakat ile röportaj sıkça birbirine karıştırılarak sorulur.")
    )

    # =====================================================================
    # BÖLÜM 5 — (Edebiyat 8) Cumhuriyet ve Dünya Romanı, Tiyatro Türleri, Paragrafta Yapı
    # =====================================================================
    ch5 = Chapter(
        number=5,
        title="Cumhuriyet ve Dünya Romanı, Tiyatro Türleri (Radyo Tiyatrosu) ve Paragrafta Yapı",
        subtitle="Roman türlerinden radyo tiyatrosuna, paragrafın giriş-gelişme-sonuç yapısına",
        key_terms=[
            KeyTerm("Biyografik Roman", "Tanınan bir sanatçının ya da ünlü bir şahsın hayat hikâyesini roman türünün imkânlarını kullanarak, genellikle kronolojik sırayla anlatan roman türü."),
            KeyTerm("Radyo Tiyatrosu", "Sahnede izlenmek için değil sadece dinlenmek için hazırlanan; dekor, kostüm, ışık gibi görsel unsurları bulunmayan tiyatro türü."),
            KeyTerm("Giriş Cümlesi", "Paragrafın konusunu veren, kendinden önceki bir cümleye bağlı olduğunu gösteren bağlayıcı kelime/zamir barındırmayan cümle."),
            KeyTerm("Sonuç Cümlesi", "Kesin bir yargı bildiren, genellikle 'demek ki, sonuç olarak, öyleyse' gibi toparlayıcı ifadelerle başlayan son cümle."),
        ],
    )
    ch5.pages.append(
        ChapterPage()
        .add_terms(ch5.key_terms)
        .add_block(BulletBlock(1, "Roman Türleri ve Yazar-Eser Eşleştirmeleri I", [
            "<b>Biyografik Roman:</b> Tanınan bir sanatçının ya da ünlü bir şahsın hayat hikâyesini roman "
            "türünün imkânlarını kullanarak ele alan eserlerdir; olaylar genellikle kronolojik sırayla anlatılır.",
            "<b>Oğuz Atay - Bir Bilim Adamının Romanı:</b> Türk edebiyatındaki en önemli biyografik "
            "romanlardandır; yazar, kendi hocası olan Prof. Dr. Mustafa İnan'ın yoksulluktan zirveye uzanan "
            "hayatını anlatır.",
            "<b>İlk Biyografik Roman:</b> Türk edebiyatında biyografik roman türünde yazılan ilk eser, Hasan "
            "Ali Yücel'in kaleme aldığı 'Goethe - Bir Dehanın Romanı'dır. Diğer önemli örnekler: Gazi Paşa "
            "(Attilâ İlhan), Hava Kurşun Gibi Ağır (Hıfzı Topuz).",
        ]))
        .add_person(OGUZ_ATAY)
    )
    ch5.pages.append(
        ChapterPage(continue_tag="Toplumcu Gerçekçi ve Dünya Romanı")
        .add_block(BulletBlock(2, "Toplumcu Gerçekçi, Türk Dünyası ve Dünya Romanı", [
            "<b>Toplumcu Gerçekçi Roman — Sabahattin Ali, Kuyucaklı Yusuf:</b> Toplumsal gerçekçi akımın en "
            "başarılı ve ilk örneklerinden kabul edilir; yazarın etkili betimleme gücüyle kişileri, olayı ve "
            "sonuç bağlantılarını ustaca ortaya koyduğu vurgulanarak sorulur.",
            "<b>Türk Dünyası Edebiyatında Roman — Cengiz Aytmatov, Elveda Gülsarı:</b> Kırgızların millî "
            "değerlerini ve göçebe kültürünün yok edilişini Tanabay adlı kahraman ve atı Gülsarı üzerinden "
            "anlatır. Diğer sınavlık eserleri: Gün Olur Asra Bedel, Beyaz Gemi, Toprak Ana.",
            "<b>Dünya Edebiyatında Roman:</b> Roman türünün ilk başarılı örneği Cervantes'in Don Kişot adlı "
            "eseridir. Paulo Coelho'nun Simyacı'sı ise Endülüslü çoban Santiago'nun Mısır Piramitleri'ne "
            "giderek 'Kişisel Menkıbe'sini bulmasını anlatan, alegorik bir dünya edebiyatı şaheseridir.",
        ]))
        .add_table(ComparisonTable(
            "Edebiyat 8 Roman Eşleştirmeleri (Hızlı Bakış)",
            ["Yazar", "Eser", "Anahtar Kavram"],
            [
                ["Hasan Ali Yücel", "Goethe - Bir Dehanın Romanı", "İlk biyografik roman"],
                ["Oğuz Atay", "Bir Bilim Adamının Romanı", "Mustafa İnan'ın biyografisi"],
                ["Sabahattin Ali", "Kuyucaklı Yusuf", "Toplumsal gerçekçiliğin ilk örneği"],
                ["Cengiz Aytmatov", "Elveda Gülsarı", "Türk dünyası / göçebe kültür"],
                ["Paulo Coelho", "Simyacı", "Alegorik dünya romanı"],
            ]
        ))
    )
    ch5.pages.append(
        ChapterPage(continue_tag="Tiyatro Türleri ve Radyo Tiyatrosu")
        .add_block(BulletBlock(3, "Tiyatroda Yazar-Eser-Tür Eşleştirmeleri ve Radyo Tiyatrosu", [
            "<b>Turan Oflazoğlu - Genç Osman:</b> Osmanlı tarihinden alınan, devlet yapısındaki bozulmaları "
            "anlatan Trajedi türünde bir eserdir.",
            "<b>Orhan Asena - Gılgameş:</b> Sümer mitolojisinden alınan, insanın ölümsüzlük sırrını aramasını "
            "anlatan Dram türünde bir eserdir.",
            "<b>Ahmet Kutsi Tecer - Bir Pazar Günü:</b> Aile ve kadın-erkek ilişkilerinde paranın ve "
            "ikiyüzlülüğün eleştirildiği Komedi türünde bir eserdir.",
        ]))
        .add_callout(Callout("caution", "Radyo Tiyatrosu (Sınav Püf Noktası)",
            "Normal tiyatrodan en büyük farkı, sahnede izlenmek için değil sadece <b>dinlenmek için "
            "(işitsel)</b> hazırlanmasıdır. Dekor, kostüm, ışık, sahne veya mimik/jest gibi görsel unsurlar "
            "KESİNLİKLE yoktur. Zaman ve mekân geçişleri, olayların değişimi sadece <b>müzik ve ses "
            "efektleriyle</b> (kapı gıcırtısı, rüzgâr sesi vb.) sağlanır."))
        .add_table(ComparisonTable(
            "Sık Çıkan Tiyatro Terimleri",
            ["Terim", "Açıklama"],
            [
                ["Dekor", "Sahneye konulan eserin yazıldığı yerin ve geçtiği çağın özelliklerini belirleyen perde, aksesuar vb. ögelerin bütünüdür."],
                ["Mizansen", "Tiyatro eserinin sahneye göre düzenlenip uygulanmasıdır."],
            ]
        ))
        .add_block(BulletBlock(4, "Dil Bilgisi: Paragrafta Yapı", [
            "Bir paragraf tıpkı bir kompozisyon gibi giriş, gelişme ve sonuç bölümlerinden oluşur; sınavda "
            "cümle sıralama veya 'Hangisi giriş cümlesi olamaz?' şeklinde çıkar.",
            "<b>Giriş Cümlesi:</b> Paragrafın konusunu verir; kendinden önceki bir cümleye bağlı olduğunu "
            "gösteren (bu yüzden, oysa, çünkü, ama, kısacası vb.) bağlayıcı kelime/zamir barındırmaz.",
            "<b>Gelişme Cümleleri:</b> Giriş cümlesindeki fikrin detaylandırıldığı, örnekleme, karşılaştırma "
            "veya sayısal verilerin kullanıldığı orta kısımdır.",
            "<b>Sonuç Cümlesi:</b> Kesin bir yargı bildiren son sözdür; genellikle 'demek ki, sonuç olarak, "
            "öyleyse, özetle, bundan dolayı' gibi toparlayıcı ifadelerle başlar.",
            "<b>Paragrafta Başlık:</b> Paragrafta ele alınan konuyu ve ana düşünceyi en net özetleyen bir, "
            "iki veya üç kelimelik söz grubudur.",
        ]))
        .add_summary("Edebiyat 8 dersinde roman ve tiyatro salt bir eğlence aracı olarak değil; tarihi "
            "gerçeklerin (Genç Osman), bilimsel ideallerin (Mustafa İnan) veya kültürel çöküşlerin (Kuyucaklı "
            "Yusuf) okura aktarıldığı 'toplumsal bir ayna' olarak işlenir. Radyo tiyatrosunun görsel unsurdan "
            "tamamen yoksun oluşu ile paragrafta giriş-gelişme-sonuç yapısı, bu bölümün en sık sorulan iki "
            "başlığıdır.")
    )

    chapters = [ch1, ch2, ch3, ch4, ch5]

    # =====================================================================
    # SÖZLÜK
    # =====================================================================
    glossary = [
        Concept("Edebî Akım", "Belli bir sanatkâr grubunun aynı dönemde ortak dünya görüşü ve estetik anlayışla oluşturduğu hareketlerin bütünü.", "Edebiyat-Toplum İlişkisi", 1),
        Concept("Türkî-i Basit", "Divan şiirinde Türkçe kelimeler kullanmayı amaçlayan, atasözü ve halk tabirlerini şiire sokan akım.", "Aydınlı Visali, Edirneli Nazmi", 1),
        Concept("Mahallîleşme", "Biçimde yerlilik ve İstanbul ağzının esas alındığı, âşık tarzı ile divan tarzını birleştiren akım.", "Necati, Nedim", 1),
        Concept("Sebk-i Hindi", "Şiirde anlamın derinleştiği, kapalı ve soyut hâle geldiği, tasavvufa geniş yer veren akım.", "Şeyh Galip, Naili", 1),
        Concept("Garip Akımı", "Ölçü, uyak ve tüm nazım kurallarına karşı çıkan, halkın günlük dilini kullanan akım.", "Orhan Veli, Oktay Rifat", 1),
        Concept("Durum Hikâyesi", "Serim-düğüm-çözüm olmadan insan yaşamından anlık bir kesit sunan hikâye türü.", "Sait Faik Abasıyanık", 1),
        Concept("Sözde Özne", "Edilgen çatılı cümlelerde işten etkilenen nesnenin zorunlu olarak özne görevi alması.", "Cümlenin Temel Ögeleri", 1),
        Concept("Manzum Hikâye", "Olayın, ölçü ve uyaklı şiir biçiminde ama içinde olay-zaman-mekân barındıracak şekilde anlatılması.", "Mehmet Âkif Ersoy", 2),
        Concept("Saf (Öz) Şiir", "İdeolojiye ve didaktizme karşı çıkan, yalnızca estetik haz ve ahenk yaratmayı amaçlayan şiir anlayışı.", "Ahmet Haşim, Yahya Kemal", 2),
        Concept("Servetifünun Şiiri", "'Sanat sanat içindir' anlayışıyla melankoli ve bireysel yalnızlığı işleyen, ağır dilli şiir anlayışı.", "Tevfik Fikret, Cenap Şahabettin", 2),
        Concept("Makale", "Bilgi vermek veya bir tezi kanıtlamak amacıyla nesnel ve ciddi bir anlatımla yazılan öğretici yazı türü.", "Şinasi", 2),
        Concept("Fıkra (Köşe Yazısı)", "Güncel olayları ciddi bir dille işleyen, konu eskiyince ömrü biten gazete yazısı türü.", "Haldun Taner", 2),
        Concept("Dolaylı Tümleç", "İsmin -e, -de, -den ekini alarak yüklemin yerini bildiren cümle ögesi.", "Cümlenin Yardımcı Ögeleri", 2),
        Concept("Ara Söz (Ara Cümle)", "Cümle içinde fazladan bilgi veren, iki virgül veya çizgi arasında gösterilen ifade.", "Cümle Dışı Unsurlar", 2),
        Concept("Yaban", "Aydın bir subayın gözünden Anadolu köylüsünün sefaletini ve aydın-halk kopukluğunu anlatan roman.", "Yakup Kadri Karaosmanoğlu", 3),
        Concept("İnce Memed", "Çukurova'da zalim Abdi Ağa'ya karşı dağa çıkan Memed'in isyanını anlatan roman.", "Yaşar Kemal", 3),
        Concept("Trajedi", "Tarih ve mitolojiden konu alan, üç birlik kuralına uyulan, çirkin olayların sahnede gösterilmediği tiyatro türü.", "Genç Osman", 3),
        Concept("Dram", "Hayatın acıklı ve gülünç yönlerini bir arada veren, üç birlik kuralına uyma zorunluluğu olmayan tiyatro türü.", "Gılgameş", 3),
        Concept("Epik Tiyatro", "Türk edebiyatında Keşanlı Ali Destanı ile en önemli örneğini veren tiyatro anlayışı.", "Haldun Taner", 3),
        Concept("Duruluk İlkesine Aykırılık", "Eş veya yakın anlamlı kelimelerin aynı cümlede gereksiz yere kullanılmasından doğan anlatım bozukluğu.", "Anlatım Bozuklukları", 3),
        Concept("Otokritik (Özeleştiri)", "Bir kimsenin kendi eserini veya kendisini eleştirmesi durumu.", "Eleştiri Türleri", 4),
        Concept("İzlenimsel (Empresyonist) Eleştiri", "Eleştirmenin eseri kendi zevk ve algısına göre öznel biçimde değerlendirdiği eleştiri türü.", "Eleştiri Türleri", 4),
        Concept("Nesnel (Bilimsel) Eleştiri", "Eleştirmenin kişisel hislerini bir kenara bırakıp bilimsel ölçütlerle tarafsız değerlendirme yaptığı eleştiri türü.", "Eleştiri Türleri", 4),
        Concept("Tahrib-i Harabat", "Namık Kemal'in Ziya Paşa'ya karşı yazdığı, Türk edebiyatındaki ilk eleştiri kitabı.", "Namık Kemal", 4),
        Concept("Diyorlar ki", "Türk edebiyatında ilk mülakat örneği kabul edilen eser.", "Ruşen Eşref Ünaydın", 4),
        Concept("Bir Bilim Adamının Romanı", "Oğuz Atay'ın hocası Prof. Dr. Mustafa İnan'ın hayatını anlattığı, Türk edebiyatının en önemli biyografik romanı.", "Oğuz Atay", 5),
        Concept("Goethe - Bir Dehanın Romanı", "Türk edebiyatında biyografik roman türünde yazılan ilk eser.", "Hasan Ali Yücel", 5),
        Concept("Kuyucaklı Yusuf", "Toplumsal gerçekçi akımın en başarılı ve ilk örneklerinden kabul edilen roman.", "Sabahattin Ali", 5),
        Concept("Elveda Gülsarı", "Kırgızların millî değerlerini ve göçebe kültürünün yok edilişini anlatan Türk dünyası edebiyatı romanı.", "Cengiz Aytmatov", 5),
        Concept("Radyo Tiyatrosu", "Sahnede izlenmek için değil sadece dinlenmek için hazırlanan, görsel unsurları bulunmayan tiyatro türü.", "Tiyatro Türleri", 5),
        Concept("Dekor", "Sahneye konulan eserin yazıldığı yerin ve geçtiği çağın özelliklerini belirleyen ögelerin bütünü.", "Tiyatro Terimleri", 5),
        Concept("Mizansen", "Tiyatro eserinin sahneye göre düzenlenip uygulanması.", "Tiyatro Terimleri", 5),
        Concept("Paragrafta Başlık", "Paragrafta ele alınan konuyu en net özetleyen bir-üç kelimelik söz grubu.", "Paragrafta Yapı", 5),
    ]

    # =====================================================================
    # TEST — 20 Soruluk Genel Değerlendirme
    # =====================================================================
    test_questions = [
        TestQuestion(1, "Aşağıdakilerden hangisi Türk edebiyatına özgü şiir akımlarından biri değildir?",
            {"A": "Mahallîleşme", "B": "Sebk-i Hindi", "C": "Garip Akımı", "D": "Sembolizm", "E": "Türkî-i Basit"}),
        TestQuestion(2, "Divan şiirinde Türkçe kelimeler kullanmayı amaçlayan, atasözü ve halk tabirlerini şiire sokan akımın adı nedir?",
            {"A": "Sebk-i Hindi", "B": "Mahallîleşme", "C": "Türkî-i Basit", "D": "Garip Akımı", "E": "Millî Edebiyat"}),
        TestQuestion(3, "Çehov tarzı olarak da bilinen, serim-düğüm-çözüm bölümü olmadan insan yaşamından anlık bir kesit sunan hikâye türüne ne ad verilir?",
            {"A": "Olay Hikâyesi", "B": "Durum Hikâyesi", "C": "Manzum Hikâye", "D": "Biyografik Hikâye", "E": "Toplumcu Hikâye"}),
        TestQuestion(4, "'Yeni alınan ev temizlendi.' cümlesindeki 'ev' sözcüğü hangi özne türüne örnektir?",
            {"A": "Gerçek Özne", "B": "Gizli Özne", "C": "Sözde Özne", "D": "Ortak Özne", "E": "Belirtili Özne"}),
        TestQuestion(5, "'Sanat sanat içindir' anlayışıyla melankoli, doğa ve bireysel yalnızlığı işleyen, Arapça-Farsça kelimelerle ağır bir dile sahip şiir anlayışı hangisidir?",
            {"A": "Tanzimat Şiiri", "B": "Millî Edebiyat Şiiri", "C": "Servetifünun Şiiri", "D": "Saf Şiir", "E": "Türk Dünyası Edebiyatı Şiiri"}),
        TestQuestion(6, "Mehmet Âkif Ersoy'un 'Küfe' adlı eseriyle ustası olduğu, ölçü ve uyaklı ama içinde olay-zaman-mekân barındıran tür hangisidir?",
            {"A": "Makale", "B": "Manzum Hikâye", "C": "Sohbet", "D": "Fıkra", "E": "Röportaj"}),
        TestQuestion(7, "Türk edebiyatında ilk makale örneği olan 'Tercüman-ı Ahval Mukaddimesi'ni kim yazmıştır?",
            {"A": "Namık Kemal", "B": "Şinasi", "C": "Ziya Paşa", "D": "Ahmet Rasim", "E": "Tevfik Fikret"}),
        TestQuestion(8, "Sohbet (Söyleşi) ile Fıkra (Köşe Yazısı) arasındaki temel fark için aşağıdakilerden hangisi söylenebilir?",
            {"A": "Sohbet sadece güncel olayları işler, fıkra her konuyu işleyebilir", "B": "Fıkra senli benli bir dille yazılır, sohbet ciddi bir dille yazılır",
             "C": "Sohbette gündelik veya kalıcı her konu işlenebilir, fıkrada sadece güncel olaylar işlenir", "D": "İkisi de kanıtlama zorunluluğu taşır", "E": "Sohbetin ömrü fıkradan kısadır"}),
        TestQuestion(9, "Aydın bir subay olan Ahmet Celâl'in gözünden Anadolu köylüsünün sefaletini ve aydın-halk kopukluğunu anlatan roman hangisidir?",
            {"A": "İnce Memed", "B": "Yaban", "C": "Yılkı Atı", "D": "Kuyucaklı Yusuf", "E": "Bir Bilim Adamının Romanı"}),
        TestQuestion(10, "Konusunu tarih ve mitolojiden alan, kişilerinin soylu ve tanrısal olduğu, çirkin olayların sahnede gösterilmediği tiyatro türü hangisidir?",
            {"A": "Komedi", "B": "Dram", "C": "Trajedi", "D": "Epik Tiyatro", "E": "Radyo Tiyatrosu"}),
        TestQuestion(11, "Üç birlik kuralına uyma zorunluluğu olmayan, hayatın hem acıklı hem gülünç yönlerini bir arada veren tiyatro türü hangisidir?",
            {"A": "Trajedi", "B": "Komedi", "C": "Dram", "D": "Epik Tiyatro", "E": "Mizansen"}),
        TestQuestion(12, "'Onun faydasız, lüzumsuz olduklarına hükmetmek...' cümlesindeki anlatım bozukluğu türü hangisidir?",
            {"A": "Anlamca çelişen kelimelerin kullanılması", "B": "Kelimenin yanlış yerde kullanılması", "C": "Gereksiz kelime kullanılması", "D": "Deyimin yanlış kullanılması", "E": "Kelimenin yanlış anlamda kullanılması"}),
        TestQuestion(13, "Eleştirmenin kişisel hislerini bir kenara bırakıp bilimsel ölçütlerle tarafsız bir gözle değerlendirme yaptığı eleştiri türü hangisidir?",
            {"A": "İzlenimsel Eleştiri", "B": "Otokritik", "C": "Nesnel (Bilimsel) Eleştiri", "D": "Tarihsel Eleştiri", "E": "Sanatçıya Yönelik Eleştiri"}),
        TestQuestion(14, "Türk edebiyatında Batılı anlamda ilk eleştiri yazısını kim yazmıştır?",
            {"A": "Ziya Paşa", "B": "Namık Kemal", "C": "Ahmet Rasim", "D": "Ruşen Eşref Ünaydın", "E": "Şinasi"}),
        TestQuestion(15, "Türk edebiyatında ilk mülakat örneği olan 'Diyorlar ki' adlı eseri kim yazmıştır?",
            {"A": "Yaşar Kemal", "B": "Namık Kemal", "C": "Ruşen Eşref Ünaydın", "D": "Haldun Taner", "E": "Ahmet Rasim"}),
        TestQuestion(16, "Mülakat ile röportaj arasındaki farkla ilgili aşağıdakilerden hangisi yanlıştır?",
            {"A": "Mülakatta kişi, röportajda konu ön plandadır", "B": "Röportaj herhangi bir kişiyle yapılabilir, uzmanlık gerekmez",
             "C": "Mülakatta yazar kendi görüşünü yansıtabilir", "D": "Röportajda yazar öznel bilgiler vererek yorum katar", "E": "Röportaj birden fazla fotoğraf ve belgeyle zenginleştirilir"}),
        TestQuestion(17, "Türk edebiyatında biyografik roman türünde yazılan ilk eser hangisidir?",
            {"A": "Bir Bilim Adamının Romanı", "B": "Goethe - Bir Dehanın Romanı", "C": "Gazi Paşa", "D": "Hava Kurşun Gibi Ağır", "E": "Kuyucaklı Yusuf"}),
        TestQuestion(18, "Toplumsal gerçekçi akımın en başarılı ve ilk örneklerinden kabul edilen 'Kuyucaklı Yusuf' romanının yazarı kimdir?",
            {"A": "Yaşar Kemal", "B": "Sabahattin Ali", "C": "Yakup Kadri Karaosmanoğlu", "D": "Oğuz Atay", "E": "Cengiz Aytmatov"}),
        TestQuestion(19, "Radyo tiyatrosuyla ilgili aşağıdakilerden hangisi yanlıştır?",
            {"A": "Sadece dinlenmek için hazırlanır", "B": "Dekor ve kostüm gibi görsel unsurlar bulunmaz", "C": "Mekân geçişleri müzik ve ses efektleriyle sağlanır", "D": "Sahne, ışık ve mimik unsurları vurguludur", "E": "İşitsel bir tiyatro türüdür"}),
        TestQuestion(20, "Kendinden önceki bir cümleye bağlı olduğunu gösteren bağlayıcı kelime/zamir barındırmayan, paragrafın konusunu veren cümleye ne ad verilir?",
            {"A": "Sonuç Cümlesi", "B": "Gelişme Cümlesi", "C": "Giriş Cümlesi", "D": "Paragrafta Başlık", "E": "Ara Cümle"}),
    ]

    answer_key_items = [
        AnswerItem(1, "D", "<b>Sembolizm</b>, Servetifünun şiirini etkileyen Batılı bir akımdır; diğerleri (Türkî-i Basit, Mahallîleşme, Sebk-i Hindi, Garip Akımı) Türk edebiyatına özgü şiir akımlarıdır."),
        AnswerItem(2, "C", "<b>Türkî-i Basit (Basit Türkçe)</b>, divan şiirinde Türkçe kelime kullanmayı amaçlamış, atasözü ve halk tabirlerini şiire sokmuştur."),
        AnswerItem(3, "B", "<b>Durum Hikâyesi</b> (Çehov tarzı), serim-düğüm-çözüm olmadan insan yaşamından anlık bir kesit sunar; öncüsü Sait Faik Abasıyanık'tır."),
        AnswerItem(4, "C", "Edilgen çatılı cümlede işten etkilenen nesne ('ev'), işi yapan belli olmadığı için zorunlu olarak özne görevi alır — bu, <b>Sözde Özne</b>dir."),
        AnswerItem(5, "C", "<b>Servetifünun Şiiri</b>, 'sanat sanat içindir' anlayışıyla melankoli ve bireysel yalnızlığı işler; dili Arapça-Farsça kelimelerle ağırdır."),
        AnswerItem(6, "B", "<b>Manzum Hikâye</b>, ölçü ve uyaklı olmasına rağmen içinde olay-zaman-mekân barındıran hikâyedir; en büyük ustası Mehmet Âkif Ersoy'dur."),
        AnswerItem(7, "B", "Türk edebiyatında ilk makale, Tanzimat Dönemi'nde <b>Şinasi</b>'nin Tercüman-ı Ahval gazetesinde yayımladığı 'Tercüman-ı Ahval Mukaddimesi'dir."),
        AnswerItem(8, "C", "<b>Sohbet</b>te gündelik veya kalıcı herhangi bir konu işlenebilirken, <b>Fıkra</b>da yalnızca güncel olaylar işlenir ve konu eskiyince fıkranın ömrü de biter."),
        AnswerItem(9, "B", "<b>Yaban</b> (Yakup Kadri Karaosmanoğlu), aydın subay Ahmet Celâl'in gözünden Anadolu köylüsünün sefaletini ve aydın-halk kopukluğunu anlatır."),
        AnswerItem(10, "C", "<b>Trajedi</b>, tarih ve mitolojiden konu alır; kişileri soylu ve tanrısaldır, çirkin olaylar sahnede gösterilmez."),
        AnswerItem(11, "C", "<b>Dram</b>, hayatın hem acıklı hem gülünç yönlerini bir arada verir ve üç birlik kuralına uyma zorunluluğu yoktur; Trajedi ve Komedi'de bu kural geçerlidir."),
        AnswerItem(12, "C", "'Faydasız' ve 'lüzumsuz' eş anlamlı kelimelerin aynı cümlede kullanılmasıdır — bu, <b>Gereksiz Kelime Kullanılması</b> (duruluk ilkesine aykırılık) örneğidir."),
        AnswerItem(13, "C", "<b>Nesnel (Bilimsel) Eleştiri</b>de eleştirmen kişisel hislerini bir kenara bırakıp bilimsel ölçütlerle tarafsız bir değerlendirme yapar."),
        AnswerItem(14, "B", "Türk edebiyatında Batılı anlamda ilk eleştiri yazısı, <b>Namık Kemal</b>'in 'Lisan-ı Osmanînin Edebiyatı Hakkında Bazı Mülâhâzâtı Şâmildir' makalesidir."),
        AnswerItem(15, "C", "Türk edebiyatında ilk mülakat örneği, <b>Ruşen Eşref Ünaydın</b>'ın 'Diyorlar ki' adlı eseridir."),
        AnswerItem(16, "D", "Röportajda yazar kendi görüşünü yansıtmaz, anlatımda nesnel kalmak zorundadır; öznel yorum katmak mülakatın özelliğidir, röportajın değil."),
        AnswerItem(17, "B", "Türk edebiyatında biyografik roman türünde yazılan ilk eser, Hasan Ali Yücel'in <b>'Goethe - Bir Dehanın Romanı'</b>dır."),
        AnswerItem(18, "B", "<b>Kuyucaklı Yusuf</b>, Sabahattin Ali'nin toplumsal gerçekçi akımın en başarılı ve ilk örneklerinden kabul edilen romanıdır."),
        AnswerItem(19, "D", "Radyo tiyatrosunda sahne, ışık, kostüm ve mimik/jest gibi görsel unsurlar KESİNLİKLE yoktur; bu tür yalnızca işitseldir."),
        AnswerItem(20, "C", "<b>Giriş Cümlesi</b>, paragrafın konusunu verir ve kendinden önceki bir cümleye bağlı olduğunu gösteren bağlayıcı kelime/zamir barındırmaz."),
    ]

    return CoursePack(
        course_code="EDEBİYAT 5-6-8",
        title='Türk Dili ve Edebiyat<span class="accent-word">a</span> Final Kampı',
        subtitle="Edebiyat 5, 6 ve 8 Derslerinin Sınavlık Kavram, Eşleştirme ve Kurallarına Bütüncül Bakış",
        description=(
            "Edebiyat-toplum ilişkisinden akımlara, hikâye ve roman türlerinden tiyatroya, eleştiri-mülakat-"
            "röportaja ve cümle/paragraf bilgisine uzanan, Açık Öğretim Lisesi final sınavına yönelik yoğunlaştırılmış özet."
        ),
        theme="burgundy",
        theme_color="#5A6732",
        icon_text="E",
        chapters=chapters,
        glossary=glossary,
        test_title="Genel Değerlendirme Testi",
        test_subtitle="Edebiyat 5, 6 ve 8 müfredatını kapsayan kapsamlı çoktan seçmeli test",
        test_instructions="Aşağıdaki sorularda beş seçenekten yalnızca birini işaretleyiniz. Süre: 30 dakika.",
        test_questions=test_questions,
        answer_key_intro="Her sorunun doğru cevabı ve kısa gerekçesi aşağıda yer almaktadır.",
        answer_key_items=answer_key_items,
        overview_lead=(
            "Bu kitap; edebiyatın <b>toplumla kurduğu bağdan</b> akımlara ve hikâye türlerine, roman ve "
            "<b>tiyatronun</b> gerçekçi dönüşümünden öğretici metin türlerine, cümle ve paragraf bilgisine "
            "uzanan üç dersi (Edebiyat 5, 6, 8) tek bir sınav kampında birleştirir."
        ),
        overview_cards=[
            {"title": "Edebiyat ve Akımlar", "text": "Toplum ilişkisi, Türk edebiyatına özgü şiir akımları ve Cumhuriyet dönemi hikâyeciliği."},
            {"title": "Şiir ve Öğretici Metinler", "text": "Dönemsel şiir anlayışları, makale, sohbet ve fıkra türleri."},
            {"title": "Roman ve Tiyatro (1923-1980)", "text": "Anadolu romanı, modern tiyatro türleri ve anlatım bozuklukları."},
            {"title": "Eleştiri, Mülakat, Röportaj", "text": "Öğretici metin türleri ile edebiyatımızdaki ilk örnekler."},
            {"title": "Cumhuriyet ve Dünya Romanı", "text": "Biyografik roman, radyo tiyatrosu ve paragrafta yapı."},
            {"title": "Dil Bilgisi Notları", "text": "Cümlenin temel/yardımcı ögeleri, cümle dışı unsurlar ve paragraf yapısı."},
        ],
        overview_flow=[
            ("Akımlar & Türler", "Edebiyat 5"),
            ("Roman & Tiyatro", "Edebiyat 6"),
            ("Cumhuriyet & Dünya", "Edebiyat 8"),
            ("Dil Bilgisi", "Cümle & Paragraf"),
        ],
        overview_note=(
            "Sınavda en sık karıştırılan yerlerden biri <b>Mülakat ile Röportaj</b> ayrımıdır: mülakatta kişi "
            "ve yazarın öznel yorumu, röportajda ise konu ve yazarın nesnel tutumu ön plandadır — 'kiminle' "
            "değil 'ne amaçla' yapıldığı karıştırılmamalıdır."
        ),
    )
