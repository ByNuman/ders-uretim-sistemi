# -*- coding: utf-8 -*-
"""İSLAM TARİHİ III — Görsel Ders Notu Kitabı, içerik tanımı.
Kaynak: 'İSLAM TARİHİ 3_FİNAL ÖZET.pdf' (ham metin özet, 14 sayfa, 5 bölüm).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from content_model import (
    Person, KeyTerm, Callout, FlowStep, FlowDiagram, ComparisonTable,
    InfoCard, BulletBlock, Chapter, ChapterPage, Concept, CoursePack,
    TestQuestion, AnswerItem,
)

# ---------------------------------------------------------------------------
# KİŞİLER (TEK KAYNAK) — tarihler/eserler yalnızca burada tanımlanır
# ---------------------------------------------------------------------------

ANUSTEGIN = Person(
    id="anustegin", name="Anûştegin", years="ö. 1097 öncesi",
    tagline="Hânedanın Atası, Köle-Askerlikten Taşt-dârlığa",
    bio=["Aslen bir Türk <b>memlûku</b> (köle-asker) olup Selçuklu Emîri Bilge Tegin tarafından satın alınarak "
         "Selçuklu sarayına getirilmiş; zekâsı ve çalışkanlığıyla yükselerek <b>Taşt-dâr</b> olmuş ve Hârezm "
         "bölgesinin gelirlerinden yararlanmıştır. Hânedan onun adıyla anılır."],
    key_work="Hârezmşâh hânedanının atası", initials="AN",
)
ATSIZ = Person(
    id="atsiz", name="Atsız", years="1128–1156",
    tagline="Bağımsızlığın İlk Adımlarını Atan Hârezmşâh",
    bio=["Başlangıçta Büyük Selçuklu Sultanı <b>Sencer</b>'e sadakatle bağlı kalmış, sonradan Cend ve Mangışlak "
         "gibi stratejik askerî merkezleri ele geçirerek bağımsızlık emareleri göstermiş; 1141 <b>Katvan "
         "Savaşı</b>'nda Sencer'in zayıflamasından yararlanıp Merv ve Nişâbûr'u zapt etmiştir."],
    key_work="Merv ve Nişâbûr'un zaptı (1141)", initials="AZ",
)
TEKIS = Person(
    id="tekis", name="Alâeddîn Tekiş", years="1172–1200",
    tagline="Devleti İmparatorluğa Dönüştüren Sultan",
    bio=["Üvey annesi Terken Hâtûn'un oğlu Sultan-şâh'ı tahta çıkarması üzerine Kara-Hıtaylara sığınmış, "
         "onlardan aldığı orduyla savaşmadan Gürgenç'e girip tahta oturmuştur. <b>1194</b>'te Irak Selçuklu "
         "Sultanı III. Tuğrul'u Rey civarında ağır bir yenilgiye uğratarak bu devleti ortadan kaldırmıştır."],
    key_work="Irak Selçuklularının ortadan kaldırılması (1194)",
)
CELALEDDIN = Person(
    id="celaleddin", name="Celâleddîn Hârezmşâh", years="ö. 1231",
    tagline="Moğollara Karşı Son Direniş, Yassıçimen'in Mağlubu",
    bio=["Babası Sultan Alâeddîn Muhammed'in ölümünden sonra Moğollara karşı direnişi devralmış, kahramanca "
         "savaşmasına rağmen diplomatik hatalar yapmıştır: 1230'da <b>Ahlat</b>'ı kuşatıp tahrip etmesi, "
         "Türkiye Selçukluları ve Eyyubîlerin ona karşı birleşmesine yol açmıştır."],
    key_work="Yassıçimen Savaşı (1230)",
)
CAGRI_BEY = Person(
    id="cagri", name="Çağrı Bey", years="Keşif seferi: 1018",
    tagline="Anadolu'yu Türklere Rapor Eden Selçuklu Şehzadesi",
    bio=["3.000 kişilik atlı okçu birliğiyle Anadolu'ya yaptığı uzun soluklu keşif seferinde, ağır zırhlı Bizans "
         "piyadeleri karşısında <b>vur-kaç</b> taktiğinin etkisini görmüş; Tuğrul Bey'e sunduğu rapor "
         "Selçuklu'nun Anadolu politikasını belirlemiştir."],
    key_work="1018 Anadolu keşif seferi raporu",
)
ALP_ARSLAN = Person(
    id="alparslan", name="Sultan Alp Arslan", years="1063–1072",
    tagline="Malazgirt'in Fatihi, Anadolu'nun Kapılarını Açan Sultan",
    bio=["Hârezm bölgesini zapt eden ve 1064'te 'asla düşmez' denilen <b>Ani Kalesi</b>'ni fetheden sultandır. "
         "1071 <b>Malazgirt</b>'te 40.000 kişilik ordusuyla 200.000'i aşan Bizans ordusunu Hilal Taktiği'yle "
         "imha etmiş, İmparator Romanos Diogenes'i esir almıştır."],
    key_work="Malazgirt Meydan Muharebesi (1071)",
)
ZENGI = Person(
    id="zengi", name="İmâdüddin Zengî", years="Zengîler: 1127–1233",
    tagline="Haçlılara Karşı İlk Büyük Zaferin Sahibi",
    bio=["Irak Selçuklu Sultanı Mahmud tarafından 1127'de Musul valiliğine atanarak devletini kurmuş; Haçlılara "
         "karşı mücadeleyi temel amaç edinmiş ve <b>1144</b>'te Urfa'yı alarak buradaki Haçlı idaresine son "
         "vermesiyle İslam dünyasının kahramanı olmuştur."],
    key_work="Urfa'nın fethi (1144)",
)
SELAHADDIN = Person(
    id="selahaddin", name="Selâhaddin Eyyûbî", years="Eyyûbîler: 1171–1462",
    tagline="Kudüs'ün Fatihi, Fâtımî Hilafetinin Sonu",
    bio=["Amcası Şîrkûh ile birlikte Mısır'daki Şiî-İsmâilî <b>Fâtımî</b> hilafetine son vererek bölgeyi "
         "Sünni-Zengî nüfuzuna sokmuş (1171); Nureddin Zengî'nin ölümünden (1174) sonra bağımsızlığını ilan "
         "etmiş ve <b>1187 Hıttin</b> zaferiyle Kudüs'ü 88 yıllık işgalden kurtarmıştır."],
    key_work="Hıttin Savaşı ve Kudüs'ün fethi (1187)",
)
BAYBARS = Person(
    id="baybars", name="Baybars el-Bundukdârî", years="Memlük Sultanı: 1260–1277",
    tagline="Hilafeti İhya Eden Memlük Sultanı",
    bio=["Turan Şah'ın memlükleri tasfiye girişimine karşı isyanın öncüsü olmuş; sultanlığı döneminde, "
         "Moğolların 1258'de Bağdat'ı yıkmasıyla ortadan kalkan <b>Abbâsî hilafetini Mısır'da yeniden tesis "
         "ederek</b> İslam dünyasının manevi liderliğini kurtarmıştır."],
    key_work="Hilafetin Mısır'da ihyası",
)
AYBEG = Person(
    id="aybeg", name="Kutbeddîn Aybeg", years="Delhi Sultanlığı: 1206–1526",
    tagline="Hindistan'da Türk Hâkimiyetinin Kurucusu",
    bio=["Gûrluların Hindistan'daki fetihlerinin ardından bölgedeki kontrolü sağlayan Türk komutan olarak "
         "<b>1206</b>'da Delhi merkezli bağımsız bir devletin temellerini atmıştır. Kurduğu sultanlık üç "
         "asırdan uzun süre Türk komutanların ve köklü hânedanların elinde kalmıştır."],
    key_work="Delhi Sultanlığı'nın kuruluşu (1206)",
)
BABUR = Person(
    id="babur", name="Bâbür Şah", years="Bâbürlüler: 1526–1858",
    tagline="Hindistan'daki İhtişamın Kurucusu, Şair-Sultan",
    bio=["Timur hânedanından gelen, çok yönlü bir devlet adamı, usta bir komutan ve parlak bir edebiyatçıdır. "
         "<b>1526 Panipat Savaşı</b>'nın ardından Delhi'ye girerek Delhi Sultanlığı'na son vermiş; Türkçe "
         "kaleme aldığı otobiyografik eseri <b>Bâbürnâme</b> dönemin en önemli kaynaklarındandır."],
    key_work="Bâbürnâme",
)
CENGIZ = Person(
    id="cengiz", name="Cengiz Han (Temuçin)", years="Kuruluş: 1206 — ö. 1227",
    tagline="Bozkır Kabilelerini Cihan İmparatorluğuna Dönüştüren Han",
    bio=["Naymanlar, Kereyitler, Merkitler ve Tatarlar gibi dağınık boyları tek tek bertaraf ettikten sonra "
         "1206 baharında Onon Nehri kaynağında topladığı <b>Kurultay</b>'da dokuz parçalı tuğ dikilerek 'Büyük "
         "Han' ilan edilmiş; deniz/okyanus ve evrensel anlamına gelen <b>Cengiz</b> unvanını almıştır."],
    key_work="Cengiz Yasası (Mavi Defter)", initials="CG",
)
HULAGU = Person(
    id="hulagu", name="Hülâgû Han", years="İlhanlılar: 1256–1353",
    tagline="Bağdat'ı Yıkan, Abbâsî Hilafetini Bitiren Han",
    bio=["Haşhaşîlerin <b>Alamut</b> kalesini (1256) ve Abbâsî başkenti <b>Bağdat</b>'ı (1258) yıkarak 500 "
         "yıllık Sünnî hilafete son vermiştir; kurduğu İlhanlı Devleti, Gazân Han devrinde İslamiyet'i resmen "
         "benimseyerek Anadolu'yu da hâkimiyeti altına almıştır."],
    key_work="Bağdat'ın yıkılışı (1258)",
)


def get_pack() -> CoursePack:
    # =====================================================================
    # BÖLÜM 1 — Hârezm'de Türk-Müslüman Hanedanı: Hârezmşâhlar
    # =====================================================================
    ch1 = Chapter(
        number=1,
        title="Hârezm'de Türk-Müslüman Hânedanı",
        subtitle="Hârezmşâhlar: Ceyhun kıyısındaki bir vilayetten imparatorluğa, Otrar'dan Yassıçimen'e",
        key_terms=[
            KeyTerm("Hârezm", "Hazar Denizi'nin doğusunda, Ceyhun (Amû-Deryâ) Nehri'nin aşağı mecrasının her iki tarafında yer alan bereketli ve stratejik ticaret bölgesi."),
            KeyTerm("Taşt-dâr", "Hükümdar elini yıkarken leğen ve ibrik tutan, saray temizliğinden sorumlu görevli; Anûştegin bu makamla yükselmiştir."),
            KeyTerm("Otrar Faciası (1218)", "Otrar valisi İnalcık'ın Moğol ticaret kervanını yağmalayıp tüccarları öldürmesi; Moğol istilasının fitilini ateşleyen olay."),
            KeyTerm("Yassıçimen Savaşı (1230)", "Erzincan Yassıçimen Ovası'nda Hârezmşâh ordusunun Selçuklu-Eyyubî ittifakına yenilerek yıkıma sürüklendiği meydan savaşı."),
        ],
    )
    ch1.pages.append(
        ChapterPage()
        .add_terms(ch1.key_terms)
        .add_block(BulletBlock(1, "Coğrafi Bağlam ve Haritalandırma", [
            "<b>Hârezm:</b> Hazar Denizi'nin doğusunda, Ceyhun (Amû-Deryâ) Nehri'nin aşağı mecrasının her iki "
            "tarafında yer alan, bereketli ve stratejik ticaret bölgesidir.",
            "<b>Gürgenç (Gürgânc-Ürgenç):</b> Bölgenin ve Hârezmşâhlar Devleti'nin efsanevi başkentidir.",
            "<b>Otrar:</b> Moğol kervanının yağmalanarak dünya tarihinin seyrinin değiştiği sınır şehridir.",
            "<b>Yassıçimen (Erzincan):</b> Hârezmşâhların, Selçuklu ve Eyyubî ittifak ordusuna karşı varlık "
            "yokluk mücadelesi verip yıkıma sürüklendiği ovadır.",
        ]))
    )
    ch1.pages.append(
        ChapterPage()
        .add_person(ANUSTEGIN)
        .add_block(BulletBlock(2, "Köken, Kuruluş ve Hânedanlar", [
            "Hârezm bölgesine hâkim olan veya burayı idare eden yöneticilere <b>\"Hârezmşâh\"</b> unvanı "
            "verilirdi; tarihçiler bu unvanı taşıyanları dört esas döneme ayırır.",
            "Selçuklu Sultanı <b>Alp Arslan</b> döneminde (1063–1072) Hârezm zapt edilmiş, buranın gelirleri "
            "sarayda görev yapan <b>Taşt-dâr</b>'ların tahsisatına ayrılmıştı.",
            "Devletin fiilî kuruluşu <b>1097</b>'de, Selçuklu Sultanı Berkyaruk zamanında Anûştegin'in oğlu "
            "<b>Kutbeddîn Muhammed</b>'in Hârezmşâh tayin edilmesiyle gerçekleşmiştir.",
        ]))
        .add_table(ComparisonTable(
            "Hârezmşâh Unvanını Taşıyan Dört Dönem",
            ["Hânedan", "Dönemi ve Niteliği"],
            [
                ["Afrigîler", "İslam öncesinden 995'e kadar süren en eski dönem."],
                ["Me'mûnîler", "995–1017 arası kısa fakat kültürel açıdan parlak dönem."],
                ["Altıntaş ve oğulları", "1017–1041 arası Gazneli nüfuzu altındaki idare."],
                ["Hârezmşâhlar Devleti", "1097–1231; İslam tarihine damga vuran asıl hânedan."],
            ]
        ))
    )
    ch1.pages.append(
        ChapterPage()
        .add_person(ATSIZ)
        .add_block(BulletBlock(3, "Siyasi Gelişim: Atsız ve İl-Arslan Dönemleri", [
            "Atsız'ın Cend ve Mangışlak'ı ele geçirip nüfuzunu artırması, Sultan Sencer'in <b>1138</b>'de "
            "Hârezm'e sefere çıkıp onu mağlup etmesine neden olmuştur.",
            "Atsız geri dönmüş, <b>1141 Katvan Savaşı</b>'nda Sencer'in zayıflamasından faydalanarak Merv ve "
            "Nişâbûr'u zapt etmiştir.",
            "Yerine geçen oğlu <b>İl-Arslan</b> (1156–1172), Kara-Hıtayların saldırılarını su bentlerini açıp "
            "araziyi sular altında bırakarak dâhiyane bir taktikle durdurmuştur.",
        ]))
        .add_person(TEKIS)
        .add_callout(Callout("caution", "Dikkat / Püf Noktası: Otrar Faciası ve Yıkımın Başlangıcı",
            "Tekiş'ten sonra başa geçen Sultan <b>Alâeddîn Muhammed</b> (1200–1220) zamanında devlet en geniş "
            "sınırlarına ulaşmış olsa da, dünya tarihinin kaderini değiştiren bir siyasi hata yapılmıştır. "
            "Başlangıçta Cengiz Han ile barış ve ticari münasebetler kurulmuşken, Otrar'a gelen Moğol ticaret "
            "kervanının vali <b>İnalcık</b> tarafından yağmalanıp tüccarların öldürülmesi (1218) yıkımın "
            "fitilini ateşlemiştir."))
    )
    ch1.pages.append(
        ChapterPage()
        .add_flow(FlowDiagram([
            FlowStep("Otrar Yağması", "Vali İnalcık kervanı yağmalatır"),
            FlowStep("Kibirli Ret", "Suçluların teslimi talebi reddedilir"),
            FlowStep("Moğol Seferi", "Devasa orduyla saldırı, yüz binlerce ölü"),
            FlowStep("Medeniyet Yıkımı", "Kütüphane, şehir ve eserler harabeye döner"),
        ], caption="Çöküş Süreci: Bir Diplomatik Hatadan Küresel Felakete"))
        .add_person(CELALEDDIN)
        .add_block(BulletBlock(4, "Son Direniş: Celâleddîn Hârezmşâh", [
            "Moğollara karşı birleşmek yerine <b>1230</b>'da Ahlat'ı kuşatıp tahrip etmesi, Türkiye Selçuklu "
            "Sultanı I. Alâeddin Keykubad ve Eyyubîlerin ona karşı birleşmesine sebep olmuştur.",
            "<b>1230 Ağustos</b>'unda Erzincan Yassıçimen Ovası'nda yapılan savaşta Hârezmşâh ordusu ağır bir "
            "bozguna uğramış; zayıflayan Celâleddîn'in ölümüyle (<b>1231</b>) devlet tarih sahnesinden "
            "silinmiştir.",
        ]))
        .add_block(BulletBlock(5, "Zaman Çizelgesi: Hârezmşâhların Serüveni", [
            "<b>1097:</b> Kutbeddîn Muhammed'in Hârezmşâh tayin edilmesi (kuruluş).",
            "<b>1141:</b> Katvan Savaşı; Atsız'ın Merv ile Nişâbûr'u zapt etmesi.",
            "<b>1172:</b> Alâeddîn Tekiş'in Gürgenç'te tahtı ele geçirmesi.",
            "<b>1194:</b> Tekiş'in Irak Selçuklularını ortadan kaldırması.",
            "<b>1218:</b> Otrar Faciası. — <b>1230:</b> Ahlat kuşatması ve Yassıçimen bozgunu.",
        ]))
    )
    ch1.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Medeniyet ve Kurumlar: Hârezmşâh İdarî, Askerî ve Adlî Teşkilatı",
            ["Kurum / Makam", "Görev ve Açıklaması"],
            [
                ["Büyük Divan", "Vezirin başkanlığında hükümet idaresinin en yüksek organı."],
                ["Dîvân-ı İnşâ / İstifâ / İşraf / 'Arz", "Sırasıyla idarî, malî, teftiş ve ordu maaş/kayıt divanları."],
                ["Hassa ve Eyalet Askerleri", "İktâ sahiplerinden müteşekkil düzenli süvari birlikleri."],
                ["Haşar", "Şehir ve kalelerin savunmasında kullanılan gönüllü kuvvetler."],
                ["Akza'l-kuzât (Baş Kadı)", "Hükümdar tarafından atanan, şer'î yargı mekanizmasının başındaki âlim."],
                ["Örfî Mahkemeler", "Asayişi bozanları ve kanunlara itaat etmeyenleri cezalandıran dünyevi mahkemeler."],
            ]
        ))
        .add_block(BulletBlock(6, "İlim, Kültür ve Tasavvuf Hayatı", [
            "XII. yüzyılda Hârezm'de ilim ve sanat büyük bir gelişme göstermiş; başkent <b>Gürgenç</b> ve Merv, "
            "Horasan'ın büyük şehirleriyle boy ölçüşecek seviyeye gelmiştir.",
            "<b>Tasavvuf:</b> Meşhur şeyh <b>Necmeddîn Kübrâ</b> (1145–1221) büyük nüfuz kazanmış; Mecdeddîn "
            "Bağdadî, Sadeddîn Hamûyî ve (Mevlânâ'nın babası) <b>Bahâeddîn Veled</b> gibi halefler yetiştirmiştir.",
            "<b>İlim:</b> Kadı Ebu'l-Fazl Kirmânî, \"Fahr-ı Hârezm\" lakaplı <b>Zemahşerî</b>, şair Reşîd Vatvat, "
            "Fahreddîn Râzî ve tarihçi <b>Nesevî</b> bu dönemin armağanlarıdır.",
            "<b>Mimari:</b> Moğol fırtınası yüzünden günümüze yalnızca Aksaray-ding kümbeti ile Gürgenç'teki "
            "Fahreddîn Râzî ve Sultan Tekiş kümbetleri kalabilmiştir.",
        ]))
    )
    ch1.pages.append(
        ChapterPage()
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "Hârezmşâhlar, İslam dünyası ile Orta Asya stepleri arasında güçlü bir kültürel, ticari ve askerî "
            "<b>kalkan (tampon)</b> vazifesi görmüşlerdir. Ancak Sultan Alâeddin'in diplomatik kibri ve "
            "Moğolların gücünü yanlış okuması, ardından Celâleddin'in İslamî ittifaklar kurmak yerine "
            "Yassıçimen'de Selçuklu ve Eyyubîlerle savaşması, bu savunma hattının kendi kendini yok etmesine "
            "ve Moğol istilasının Ortadoğu'ya engelsizce akmasına neden olmuştur."))
        .add_summary("Ceyhun kıyısındaki bir vilayette Selçuklu sarayının Taşt-dâr'ı Anûştegin'in soyundan "
            "doğan Hârezmşâhlar, Atsız'ın bağımsızlık hamleleri ve Tekiş'in fetihleriyle devasa bir "
            "imparatorluğa dönüşmüş; Sencer devrini örnek alan güçlü bir divan-iktâ teşkilatı ve Necmeddîn "
            "Kübrâ ile Zemahşerî gibi isimlerin yetiştiği parlak bir ilim hayatı kurmuştur. Ne var ki Otrar "
            "Faciası'yla başlayan diplomatik körlük ve Celâleddîn'in Yassıçimen'deki ittifak hatası, İslam "
            "dünyasının bu doğu kalkanını 1231'de tarih sahnesinden silmiştir.")
    )

    # =====================================================================
    # BÖLÜM 2 — Anadolu'nun İslamlaşması ve Türkler
    # =====================================================================
    ch2 = Chapter(
        number=2,
        title="Anadolu'nun İslamlaşması ve Türkler",
        subtitle="Emevî akınlarından Malazgirt'e, beyliklerden dervişlere: bir yurdun kalıcı dönüşümü",
        key_terms=[
            KeyTerm("Thema Anatolikon", "Bizans'ın başkente göre doğuda kalan idarî birimi; Grekçe 'doğu' anlamındaki Anatole'den türeyip halk ağzında Natolia → Anadolu formuna evrilmiştir."),
            KeyTerm("Savâif ve Şevâtî", "Emevîler döneminde Bizans'ı yıpratmak için yılda iki kez düzenlenen yaz (savâif) ve kış (şevâtî) seferleri."),
            KeyTerm("Avâsım ve Suğûr", "Abbâsîlerin sınır güvenliği için Tarsus-Maraş hattında kurduğu askerî valilikler (avâsım) ve en ön saftaki uç bölgeler (suğûr)."),
            KeyTerm("Hilal (Turan) Taktiği", "Malazgirt'te uygulanan, sahte geri çekilmeyle düşman merkezini kuşatıp imha etmeye dayanan klasik Türk savaş taktiği."),
        ],
    )
    ch2.pages.append(
        ChapterPage()
        .add_terms(ch2.key_terms)
        .add_block(BulletBlock(1, "İsim Kökeni ve Coğrafi Bağlam", [
            "<b>Anatolia / Anatole:</b> Grekçe \"doğu\" anlamındaki Anatole'den türemiştir. Bizans döneminde "
            "başkente göre doğuda kalan bölgeye idarî terim olarak <b>Thema Anatolikon</b> denmiş; bu isim halk "
            "ağzında Natolia ve nihayet Anadolu formuna evrilmiştir.",
            "<b>Minor Asia:</b> Antik çağda kullanılan, coğrafyanın büyük Asya kıtasının bir parçası olduğunu "
            "vurgulayan \"Küçük Asya\" tanımıdır.",
            "<b>Rûm Merkezli İsimlendirmeler:</b> Klasik İslam literatüründe bölge Doğu Roma egemenliğinde "
            "olduğu için \"Rûm\" kavramıyla anılmıştır: <b>Bilâd-ı Rûm</b>, <b>Diyar-ı Rûm</b> ve <b>Arz-ı Rûm</b>.",
            "<b>Folklorik Etimoloji (Ana-Dolu):</b> \"Kırmızı Ebe\" efsanesinde askerlere ayran dağıtan ve tası "
            "hiç boşalmayan yaşlı kadına \"Ana, dolu!\" denmesiyle adın türediğine inanılır — Anadolu'nun "
            "şefkat, bereket ve misafirperver bir <b>ana</b> figürüyle özdeşleştirilmesidir.",
        ]))
    )
    ch2.pages.append(
        ChapterPage()
        .add_block(BulletBlock(2, "Arap-İslam Fetihleri Dönemi", [
            "Müslümanların Anadolu'ya gelişi Selçuklulardan yüzyıllar önce başlamıştır. Emevîler döneminde hızlı "
            "İslamlaştırma yerini <b>yıpratma savaşlarına</b> bırakmış; sert iklim ve coğrafyayı aşmak için "
            "yılda iki kez <b>Savâif</b> (yaz) ve <b>Şevâtî</b> (kış) seferleri düzenlenmiştir.",
            "Abbâsîler devrinde sınır güvenliği için Tarsus-Maraş hattında <b>Avâsım</b> (askerî valilikler) "
            "kurulmuş, ön saftaki <b>Suğûr</b> (uç bölgeler) tahkim edilerek Bizans vergiye bağlanmıştır.",
            "Ancak Abbâsîler bölgeyi yalnızca askerî harekât sahası olarak kullanmış, kalıcı bir <b>iskân "
            "(yerleşim)</b> politikası gütmedikleri için tam bir İslamlaşma sağlanamamıştır.",
        ]))
        .add_block(BulletBlock(3, "Zaman Çizelgesi: Anadolu'ya Yönelik İslam ve Türk Akınları", [
            "<b>634–636:</b> Hz. Ömer dönemi Ecnâdeyn ve Yermük zaferleriyle Suriye/Filistin fethedilmiş, "
            "Bizans Toros Dağları'nın gerisine püskürtülerek doğal sınır oluşturulmuştur.",
            "<b>669–670:</b> Emevîler döneminde karadan ve denizden desteklenen ilk büyük İstanbul kuşatması "
            "yapılmış, <b>Ebû Eyyûb el-Ensârî</b> surlar önünde şehit düşmüştür.",
            "<b>838:</b> Abbâsî Halifesi Mu'tasım devrinde Türk komutanların önderliğinde Ankara ve en "
            "müstahkem kalelerden <b>Ammuriye</b> (Amorion/Emirdağ) fethedilmiştir.",
            "<b>1018:</b> Selçuklu şehzadesi Çağrı Bey'in 3.000 kişilik atlı okçu birliğiyle yaptığı keşif seferi.",
            "<b>1048:</b> <b>Pasinler Savaşı</b> — İbrahim Yınal ve Kutalmış'ın Bizans'a karşı kazandığı ilk "
            "büyük meydan savaşı.",
            "<b>1064:</b> Alp Arslan'ın \"asla düşmez\" denilen <b>Ani Kalesi</b>'ni fethetmesi.",
            "<b>1071:</b> <b>Malazgirt Meydan Muharebesi</b> ve Anadolu kapılarının Türklere kesin olarak açılması.",
        ]))
        .add_person(CAGRI_BEY)
    )
    ch2.pages.append(
        ChapterPage()
        .add_callout(Callout("focus", "Dikkat / Püf Noktası: Çağrı Bey'in Raporu ve Vur-Kaç Taktiği",
            "Türklerin Anadolu'ya sistemli yönelişindeki en önemli kırılma, 1018'deki uzun soluklu keşif "
            "seferidir. Ağır zırhlı Bizans piyadeleri karşısında mobil atlı okçuların <b>vur-kaç</b> taktikleri "
            "Bizans'ı şaşırtıp felç etmiştir. Çağrı Bey'in Tuğrul Bey'e sunduğu rapor Selçuklu'nun devlet "
            "politikasını belirlemiştir: <b>\"Burada bize karşı koyabilecek bir güç yoktur; bu topraklar hem "
            "iklimi hem de otlaklarıyla halkımız için ideal bir vatandır.\"</b>"))
        .add_person(ALP_ARSLAN)
        .add_block(BulletBlock(4, "Malazgirt Meydan Muharebesi (1071)", [
            "Sultan Alp Arslan, Halep kuşatmasındayken İmparator <b>Romanos Diogenes</b>'in devasa bir orduyla "
            "Anadolu'ya girdiğini öğrenip hızla geri dönmüştür. 200.000'i aşan Frank, Ermeni, Rum ve paralı "
            "askerden oluşan Bizans ordusuna karşı <b>40.000 kişilik</b> Selçuklu ordusu çıkmıştır.",
            "<b>Kritik gelişme:</b> Savaşın kaderini değiştiren temel sebep, Bizans ordusundaki <b>Peçenek ve "
            "Uz (Guz)</b> Türklerinin karşılarındakilerin kendi soydaşları olduğunu anlayarak Selçuklu safına "
            "geçmesidir.",
            "<b>Taktik ve sonuç:</b> <b>Hilal (Turan) Taktiği</b> ile Bizans merkez kuvvetleri kuşatılıp imha "
            "edilmiş, İmparator Diogenes esir alınmıştır. Alp Arslan'ın komutanlarına verdiği emir asırlar "
            "sürecek Türkleşmenin fitilini ateşlemiştir: <b>\"Fethettiğiniz yerler sizin kılıcınızın hakkıdır.\"</b>",
        ]))
    )
    ch2.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Birinci Beylikler Dönemi (Malazgirt Sonrası): Kılıç Hakkı Olarak İktâ",
            ["Beylik", "Bölgesi", "Tarihî ve Stratejik Önemi"],
            [
                ["Saltuklular", "Erzurum ve çevresi", "Malazgirt sonrası kurulan <b>ilk</b> Türk beyliğidir. Mama Hatun Külliyesi ve Çifte Minareli Medrese eserlerindendir."],
                ["Dânişmendliler", "Sivas, Tokat, Malatya", "Dönemin <b>en güçlü</b> beyliğidir. Anadolu'nun ilk medresesi olan Yağıbasan Medresesi'ni inşa etmişlerdir."],
                ["Mengücekliler", "Erzincan, Kemah, Divriği", "Dönemin mimari şaheseri sayılan Divriği Ulu Camii ve Darüşşifası'nı bırakmışlardır."],
                ["Artuklular", "Diyarbakır, Mardin, Hasankeyf", "Kudüs fatihi Artuk Bey'in soyundan gelenler kurmuştur; taş işçiliğinde zirveye ulaşmışlardır."],
                ["Dilmaçoğulları", "Bitlis, Erzen", "300 yıl varlığını sürdürmüş, Haçlılar ve Gürcülere karşı Doğu Anadolu'yu savunmuştur."],
            ]
        ))
        .add_callout(Callout("route", "İkinci Beylikler Dönemi (Kösedağ Sonrası)",
            "<b>1243 Kösedağ</b> yenilgisi sonrası Moğol tahakkümü altındaki Selçuklu otoritesinin çökmesiyle, "
            "Bizans sınırındaki <b>\"Uç\"</b> bölgelerinde yığılan Türkmenlerin bağımsızlığını ilan etmesiyle "
            "oluşmuştur: Karamanoğulları, Osmanoğulları, Aydınoğulları ve diğerleri."))
        .add_block(BulletBlock(5, "Türkleşme ve İslamlaşma Süreci: Demografik ve Kültürel Dönüşüm", [
            "Anadolu'nun Türkleşmesi askerî bir işgal değil; <b>göç, iskân ve kültürel dönüşüm</b> sürecidir. "
            "XI. yüzyılda Anadolu nüfusu yoğun değildi; Sâsânî-Bizans savaşları ve Bizans'ın ağır vergileri "
            "yüzünden köyler harap olmuş (\"viran\", \"ören\", \"höyük\") durumdaydı.",
            "<b>Oğuz boyları</b> dalgalar hâlinde aileleri ve hayvanlarıyla gelerek kırsal alanlara yerleşmiş, "
            "harap şehirleri yeniden imar etmiş, kervansaraylar kurarak ticareti ve tarımı (pamuk, pirinç) "
            "canlandırmışlardır.",
        ]))
    )
    ch2.pages.append(
        ChapterPage()
        .add_flow(FlowDiagram([
            FlowStep("Muhaceret", "Moğol istilasından kaçan Türk-Müslüman kitleler sığınır"),
            FlowStep("Alp + Gazâ Sentezi", "Savaşçı 'alp' ruhu mücahit anlayışıyla birleşir"),
            FlowStep("Derviş Diplomasisi", "Sıcak sosyal-ticari ilişkiler, kiliselerin camiye dönüşü"),
            FlowStep("Kalıcı İslamlaşma", "Adil vergi sistemi Hristiyan ahaliyi entegre eder"),
        ], caption="İslamlaşma Dinamiği: Kılıçtan Çok İskân, Ticaret ve Tasavvuf"))
        .add_table(ComparisonTable(
            "Manevi Fatihler: Anadolu'nun Dinî ve Sosyal Mimarları",
            ["Zümre", "Akademik / Kavramsal Açıklama"],
            [
                ["Gaziyân-ı Rûm (Alperenler)", "Eski Türklerdeki \"alp\"lık (savaşçılık) ruhunu İslam'ın \"mücahitlik\" anlayışıyla sentezleyen, dervişlikle askerliği harmanlayan zümre."],
                ["Abdâlân-ı Rûm (Abdallar)", "Kendilerini Allah yoluna adayan, dünyevi ilgilerden uzaklaşarak manevi fethi gerçekleştiren derviş topluluğu (Geyikli Baba, Abdal Musa)."],
                ["Ahiyân-ı Rûm (Ahiler)", "Ticari ve ekonomik hayatı ahlaki-dinî bir zemine oturtarak toplumsal dayanışmayı ve huzuru sağlayan esnaf teşkilatı."],
                ["Tasavvuf Erbabı", "Hacı Bektaş-ı Velî, Mevlânâ ve Yunus Emre gibi halkı motive eden, hoşgörü aşılayan ve sivil toplumu rehabilite eden manevi rehberler."],
            ]
        ))
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "Anadolu'nun Türkleşmesi ve İslamlaşması birbirini tamamlayan <b>paralel süreçlerdir</b>. Sadece "
            "kılıçla yapılan fetihlerle değil; Oğuz boylarının sistematik iskânı, Ahilik teşkilatının ekonomik "
            "adaleti sağlaması, dervişlerin tekke/zaviyeler üzerinden inşa ettiği sosyal rehabilitasyon ve "
            "Bizans'ın ağır vergilerinden bunalan yerli halkın hoşgörülü Selçuklu sistemine gösterdiği uyum "
            "sayesinde kalıcı bir medeniyet inşası gerçekleşmiştir."))
    )
    ch2.pages.append(
        ChapterPage()
        .add_summary("Anadolu, Grekçe \"doğu\" anlamındaki Anatole'den adını alan bir Bizans temasından, "
            "Emevî-Abbâsî akınlarıyla tanışıp Çağrı Bey'in 1018 raporu ve 1071 Malazgirt zaferiyle Türklere "
            "açılmıştır. Malazgirt sonrası kılıç hakkı olarak dağıtılan iktâlarla kurulan Birinci Beylikler, "
            "1243 Kösedağ sonrasında uçlarda doğan İkinci Beylikler dönemine evrilmiş; Oğuz göçleri, Ahilik "
            "teşkilatı ve Gaziyân/Abdâlân/Ahiyân zümrelerinin manevi fethi sayesinde Anadolu askerî bir işgalle "
            "değil, organik bir kültürel dönüşümle kalıcı Türk-İslam yurdu hâline gelmiştir.")
    )

    # =====================================================================
    # BÖLÜM 3 — Bilâdü'ş-Şâm'da Türkler: Memlükler
    # =====================================================================
    ch3 = Chapter(
        number=3,
        title="Bilâdü'ş-Şâm'da Türkler: Memlükler",
        subtitle="Zengîlerden Eyyûbîlere, kölelikten sultanlığa: Haçlı ve Moğollara karşı üç asırlık kalkan",
        key_terms=[
            KeyTerm("Memlük", "Köle pazarlarından satın alınıp askerî eğitimle yetiştirilen Türk atlı birlikleri; 'köle-asker / kölemen' anlamındadır."),
            KeyTerm("İktâ", "Devlet topraklarının gelirlerinin asker ve memurlara maaş karşılığı tahsis edilmesi sistemi; Selçuklu ve Zengîlerden devralınmıştır."),
            KeyTerm("Bahrî Memlükler", "1250–1382 arası I. dönem; Nil Nehri (Bahr) üzerindeki Ravza Adası'na yerleştirilen ağırlıklı olarak Türk memlükleri."),
            KeyTerm("Burcî Memlükler", "1382–1517 arası II. dönem; Sultan Kalavun'un Kahire kalesinin burçlarına yerleştirdiği ağırlıklı olarak Çerkez memlükleri."),
        ],
    )
    ch3.pages.append(
        ChapterPage()
        .add_terms(ch3.key_terms)
        .add_person_row([ZENGI, SELAHADDIN])
    )
    ch3.pages.append(
        ChapterPage()
        .add_block(BulletBlock(1, "Coğrafi ve Tarihsel Bağlam: Zengîler ve Eyyûbîler Mirası", [
            "Orta Doğu (Mısır, Suriye ve Cezîre) coğrafyasında Haçlılar ve Moğollara karşı İslam dünyasını "
            "savunan Türk-İslam devletleri, birbirinin içinden doğan <b>kesintisiz bir tarihsel silsile</b> "
            "oluşturmuştur: Zengîler temeli atmış, Eyyûbîler devralıp genişletmiş, nihayet ordudaki köle-askerler "
            "yönetimi tamamen ele geçirmiştir.",
            "<b>Zengîler (1127–1233):</b> Kurucusu İmâdüddin Zengî'nin oğlu <b>Nureddin Mahmud Zengî</b>, "
            "Mısır, Suriye ve Cezîre'yi birleştirerek Haçlılara karşı çok daha kuvvetli bir birlik oluşturmuştur.",
            "<b>Eyyûbîler (1171–1462):</b> Aile kökeni Arap-Kürt-Türk karışımı olsa da, <b>yönetim şekli ve "
            "komuta kadrosu bakımından tam bir Türk devleti</b> niteliğindedir.",
        ]))
        .add_callout(Callout("focus", "Dikkat / Püf Noktası: Hıttin Savaşı (1187)",
            "Eyyûbîler tarihinin en önemli kırılma noktası, Selâhaddin Eyyûbî'nin Haçlı ordusunu büyük bir "
            "bozguna uğrattığı <b>Hıttin Savaşı</b>'dır. I. Haçlı Seferi (1099) ile kaybedilen <b>Kudüs</b>, "
            "88 yıllık işgalin ardından tekrar Müslümanların kontrolüne geçmiş; bu zafer Batı'da şok etkisi "
            "yaratarak İngiliz Kralı <b>Aslan Yürekli Richard</b> komutasındaki III. Haçlı Seferi'nin "
            "başlamasına neden olmuştur."))
        .add_block(BulletBlock(2, "Memlüklerin Doğuşu: Kölelikten Efendiliğe Geçiş", [
            "Eyyûbîler, büyük bir ordu kurabilmek adına Selçuklu ve Zengîlerden devraldıkları <b>İktâ</b> "
            "sistemini yaygınlaştırdılar; bu ordunun belkemiğini köle pazarlarından satın alınan Türk atlı "
            "birlikleri, yani <b>Memlükler</b> oluşturuyordu.",
            "Mısır Eyyûbî Sultanı <b>el-Melikü's-Sâlih</b> (1240–1249) döneminde Türk memlüklerinin ordudaki "
            "etkinliği ve sayısı zirveye çıkmıştır.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("Tasfiye Girişimi", "Turan Şah memlükleri saf dışı bırakmak ister"),
            FlowStep("İsyan (1250)", "Baybars öncülüğünde Turan Şah öldürülür"),
            FlowStep("Şecerüddürr", "Tahta bir kadın sultan çıkarılır"),
            FlowStep("Aybek ve Yeni Çağ", "Şecerüddürr saltanattan feragat eder, Memlükler Çağı başlar"),
        ], caption="İktidar Değişimi (1250): Eyyûbî Yönetiminin Sonu"))
    )
    ch3.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Memlük Devletinin İki Dönemi",
            ["Dönem", "İsim ve Etimolojik Kökeni", "Etnik Yapı"],
            [
                ["I. Dönem (1250–1382)", "<b>Bahrî Memlükler:</b> Nil Nehri (Bahr) üzerindeki Ravza Adası'na yerleştirilmelerinden dolayı bu ismi almışlardır.", "Türk memlükleri"],
                ["II. Dönem (1382–1517)", "<b>Burcî Memlükler:</b> Sultan Kalavun'un özel birliklerini Kahire kalesinin burçlarına yerleştirmesinden dolayı bu ismi almışlardır.", "Çerkez memlükleri"],
            ]
        ))
        .add_callout(Callout("caution", "Dikkat / Püf Noktası: Veraset Değil, Liyakat",
            "Memlük devlet yapısında geleneksel Türk veraset sistemi (babadan oğula geçiş) çoğunlukla "
            "<b>uygulanmamış</b>; orduda yetişen ve gücü elinde bulunduran <b>\"en güçlü emîrler\"</b> arasından "
            "çıkan kişiler sultan olmuştur."))
        .add_person(BAYBARS)
        .add_block(BulletBlock(3, "İslam Dünyasının Kaderini Değiştiren Üç Başarı", [
            "<b>Moğol İlerleyişinin Durdurulması (1260):</b> Komutan <b>Kutuz</b> idaresindeki Memlük ordusu, "
            "<b>Aynicâlût Savaşı</b>'nda Moğollara tarihî bir mağlubiyet yaşatarak onların Orta Doğu'daki "
            "yenilmezlik efsanesini yıkmış ve ilerleyişlerini kesin olarak durdurmuştur.",
            "<b>Hilafetin İhyası:</b> 1258'de Moğolların Bağdat'ı yıkarak Abbâsî hilafetini ortadan kaldırması "
            "üzerine Sultan <b>Baybars</b>, hilafeti Mısır'da (sembolik ve dinî bir mahiyette de olsa) yeniden "
            "tesis ederek İslam dünyasının manevi liderliğini kurtarmıştır.",
            "<b>Haçlı Varlığının Kesin Sonu (1291):</b> Sultan <b>el-Melikü'l-Eşref Halîl</b>, Akkâ kalesini ele "
            "geçirerek bölgedeki iki asırlık Haçlı işgaline tamamen son vermiştir.",
        ]))
    )
    ch3.pages.append(
        ChapterPage()
        .add_block(BulletBlock(4, "Zaman Çizelgesi: Zengîlerden Memlüklere Kritik Olaylar", [
            "<b>1144:</b> İmâdüddin Zengî'nin Urfa'yı Haçlılardan geri alması.",
            "<b>1171:</b> Şîrkûh ve Selâhaddin Eyyûbî'nin Mısır'daki Fâtımî hilafetine son vermesi.",
            "<b>1187:</b> Hıttin Savaşı ve Kudüs'ün Selâhaddin Eyyûbî tarafından fethedilmesi.",
            "<b>1250:</b> İzzeddin Aybek'in tahta geçmesiyle Memlükler döneminin başlaması.",
            "<b>1260:</b> Aynicâlût Savaşı ile Moğolların ilerleyişinin durdurulması.",
            "<b>1291:</b> Akkâ'nın fethi ve Orta Doğu'daki Haçlı varlığının sona ermesi.",
            "<b>1516–1517:</b> Mercidâbık ve Ridâniye savaşlarında Yavuz Sultan Selim'in Memlükleri mağlup "
            "ederek Mısır, Suriye ve Kutsal Toprakları Osmanlı idaresine katması ve devletin yıkılışı.",
        ]))
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "Zengîler ve Eyyûbîler devrinde kurumsallaşan <b>iktâ ve memlük sistemi</b>, Mısır coğrafyasında "
            "öylesine güçlü bir askerî sınıf yaratmıştır ki bu sınıf en sonunda kendi efendilerini devirerek "
            "devleti ele geçirmiştir. Kurdukları <b>\"güçlünün tahta geçtiği\"</b> liyakat ve bilek gücüne "
            "dayalı sistem sayesinde Memlükler; hem Moğolları hem Haçlıları Orta Doğu'dan söküp atarak üç asır "
            "boyunca Sünnî İslam medeniyetinin yegâne koruyucu kalkanı olmuşlardır."))
        .add_summary("1127'de Musul'da kurulan Zengîler Urfa'yı geri alarak Haçlı karşıtı mücadelenin temelini "
            "atmış, Selâhaddin Eyyûbî Fâtımî hilafetine son verip 1187 Hıttin'de Kudüs'ü kurtarmıştır. "
            "Eyyûbîlerin yaygınlaştırdığı iktâ sistemiyle güçlenen köle-asker sınıfı 1250'de yönetimi ele "
            "geçirmiş; Bahrî ve Burcî dönemleri boyunca 1260 Aynicâlût'ta Moğolları durduran, hilafeti Mısır'da "
            "ihya eden ve 1291'de Akkâ ile Haçlı varlığını bitiren Memlükler, 1517 Ridâniye'ye kadar İslam "
            "dünyasının yegâne koruyucu gücü olmuştur.")
    )

    # =====================================================================
    # BÖLÜM 4 — Hindistan'da Türkler: Delhi Sultanlığı ve Bâbürlüler
    # =====================================================================
    ch4 = Chapter(
        number=4,
        title="Hindistan'da Türkler",
        subtitle="Delhi Sultanlığı ve Bâbürlüler: Moğol fırtınasından korunan bir medeniyet vahası",
        key_terms=[
            KeyTerm("Hint Alt Kıtası", "Asya'nın güneyinde yer alan, Moğol istilasından korunmayı başaran ve İslam dünyasının en güvenli sığınaklarından biri hâline gelen bereketli coğrafya."),
            KeyTerm("Delhi Sultanlığı", "Kutbeddîn Aybeg'in 1206'da kurduğu, üç asırdan uzun süre Türk komutan ve hânedanların elinde kalan (1206–1526) devlet."),
            KeyTerm("Panipat Savaşı (1526)", "Bâbür Şah'ın ateşli silahlar ve taktik üstünlüğüyle Delhi Sultanlığı'na son verip Bâbürlü İmparatorluğu'nu başlattığı savaş."),
            KeyTerm("Bâbürnâme", "Bâbür Şah'ın Türkçe kaleme aldığı otobiyografik eser; dönemin Hindistan coğrafyasını, siyasi ve sosyal yapısını anlatan en önemli kaynaklardandır."),
        ],
    )
    ch4.pages.append(
        ChapterPage()
        .add_terms(ch4.key_terms)
        .add_block(BulletBlock(1, "Coğrafi Bağlam ve Moğol İstilasının Ters Etkisi", [
            "<b>Hint Alt Kıtası:</b> Asya'nın güneyinde yer alan, Moğol istilasından korunmayı başaran ve bu "
            "sayede İslam dünyasının en güvenli sığınaklarından biri hâline gelen devasa ve bereketli coğrafya.",
            "<b>Delhi:</b> Türk komutanların kurduğu sultanlığa başkentlik yapan, asırlar boyunca İslam "
            "dünyasının en önemli ilim, kültür ve siyaset merkezlerinden birine dönüşen stratejik şehir.",
            "Hindistan'daki kalıcı Türk tarihi, dışarıdaki bir felaketin — Moğol istilasının — <b>demografik bir "
            "avantaja</b> dönüşmesiyle ivme kazanmıştır.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("Moğol Yıkımı", "Orta Asya, Hârezm ve İran yakılıp yıkılır"),
            FlowStep("Güneye Göç", "Komutan, âlim ve sanatkârlar sığınak arar"),
            FlowStep("Açık Kapı", "Hindistan mülteci kitlelere kapılarını açar"),
            FlowStep("Kültürel Sıçrama", "Türk/Müslüman nüfus ve birikim muazzam artar"),
        ], caption="Demografik Dönüşüm: Felaketin Avantaja Çevrilmesi"))
    )
    ch4.pages.append(
        ChapterPage()
        .add_person(AYBEG)
        .add_block(BulletBlock(2, "Delhi Sultanlığı (1206–1526): Türk Hâkimiyetinin Kökleşmesi", [
            "Gûrluların Hindistan'daki fetihlerinin ardından bölgedeki kontrolü sağlayan Kutbeddîn Aybeg, "
            "1206'da Delhi merkezli bağımsız bir devletin temellerini atmış; bu sultanlık üç asırdan uzun süre "
            "<b>Mu'izzîler, Halacîler, Tuğluklular</b> gibi köklü hânedanların elinde kalmıştır.",
            "<b>Moğol Kalkanı:</b> Devletin İslam tarihi açısından en büyük askerî başarısı, Asya'yı kasıp "
            "kavuran Moğol tehdidini Hindistan sınırlarında savuşturarak buradaki İslam birikiminin yok "
            "edilmesine izin vermemesidir.",
            "<b>İlim ve Kültür Merkezi:</b> Sığınmacı âlimlerin ve mutasavvıfların katkısıyla Delhi, İslam "
            "dünyasının en önemli ilim ve kültür merkezlerinden biri hâline getirilmiştir.",
        ]))
        .add_person(BABUR)
    )
    ch4.pages.append(
        ChapterPage()
        .add_block(BulletBlock(3, "Bâbürlüler İmparatorluğu (1526–1858): İhtişamın Zirvesi", [
            "<b>Zirve Dönemleri:</b> İmparatorluk, bilhassa mimariye büyük önem veren <b>Şah Cihan</b> ve "
            "sınırları en uç noktalara taşıyan oğlu <b>Evrengzib (Âlemgîr)</b> dönemlerinde altın çağını "
            "yaşamış, Hindistan'ın neredeyse tamamında mutlak hâkimiyet kurmuştur.",
            "<b>Çöküş ve İngiliz Sömürgesi:</b> Bu devasa Türk imparatorluğu 18. yüzyıldan itibaren iç isyanlar, "
            "zayıf yöneticiler ve Batılı güçlerin sızmasıyla zayıflamış; <b>1858</b>'de Hindistan'ın tamamen "
            "İngiliz sömürgesi hâline gelmesiyle tarih sahnesinden trajik biçimde çekilmiştir.",
        ]))
        .add_callout(Callout("focus", "Dikkat / Püf Noktası: Kılıçtan Ziyade Sığınak Olma Avantajı",
            "Hindistan'da kalıcı bir Türk-İslam medeniyetinin tesis edilmesindeki <b>temel sebep</b>, sadece "
            "askerî fetihler değil; Hindistan'ın <b>Moğol teröründen azade bir vaha</b> olarak kalmasıdır. "
            "Moğol istilasından kaçan nitelikli Türk-İslam aydınının, sanatkârının ve devlet adamının buraya "
            "akması, sıfırdan bir medeniyet inşa etmek yerine <b>Orta Asya'daki köklü medeniyetin transfer "
            "edilmesini</b> ve Hindistan'ın İslamlaşmasını büyük ölçüde kolaylaştırmıştır."))
        .add_table(ComparisonTable(
            "Hindistan'daki İki Büyük Türk Devleti",
            ["Devlet (Kurucu / Tarih)", "Temel Başarısı ve Misyonu", "Yıkılış Sebebi"],
            [
                ["<b>Delhi Sultanlığı</b><br>Kutbeddîn Aybeg (1206)", "Moğol akınlarını durdurarak Hindistan'ı istiladan korumuş, Delhi'yi İslamî ilimlerin beşiği yapmıştır.", "Bâbür Şah'ın ateşli silahlar ve taktik üstünlüğüyle Panipat'ta galip gelmesi."],
                ["<b>Bâbürlü İmparatorluğu</b><br>Bâbür Şah (1526)", "Hindistan'ın tamamına yakınında hâkimiyet kurarak Türk-İslam mimarisini ve sanatını (Tâc Mahal vb.) zirveye taşımıştır.", "İç taht kavgaları ve 19. yüzyılda İngiliz sömürgeciliğinin Hindistan'ı işgal etmesi."],
            ]
        ))
    )
    ch4.pages.append(
        ChapterPage()
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "Hint Alt Kıtası, İslam coğrafyasının geri kalanının Moğol atları altında ezildiği bir dönemde "
            "<b>izole kalabilme avantajını</b> çok iyi kullanmıştır. Delhi Sultanlığı'nın kurduğu güçlü "
            "siyasi/askerî altyapı ve ardından Bâbürlülerin inşa ettiği emsalsiz ihtişam sayesinde Hindistan, "
            "asırlar boyunca Türk-İslam medeniyetinin doğudaki en güçlü, en estetik ve en kalabalık kalesi "
            "olma misyonunu başarıyla yerine getirmiştir."))
        .add_summary("Moğol istilasının Orta Asya'yı yakıp yıkması, nitelikli Türk-İslam nüfusunu Hindistan'a "
            "sürerek bu coğrafyayı bir medeniyet sığınağına çevirmiştir. Kutbeddîn Aybeg'in 1206'da kurduğu "
            "Delhi Sultanlığı Moğol tehdidini sınırda durdurup Delhi'yi ilim merkezi yapmış; 1526 Panipat "
            "Savaşı'yla gelen Bâbür Şah ise Bâbürnâme'siyle kaynak, Şah Cihan ve Evrengzib dönemleriyle "
            "ihtişam bırakmıştır. Bu üç asırlık zirve, 1858'de İngiliz sömürgeciliğiyle son bulmuştur.")
    )

    # =====================================================================
    # BÖLÜM 5 — Moğollar ve Yeni Dünya Düzeni
    # =====================================================================
    ch5 = Chapter(
        number=5,
        title="Moğollar ve Yeni Dünya Düzeni",
        subtitle="Cengiz Han'dan dört hanlığa: kıyametten Pax Mongolica'ya uzanan çift yönlü miras",
        key_terms=[
            KeyTerm("Kurultay", "Moğol ve Türk devlet geleneğinde han seçimi ile büyük kararların alındığı meclis; 1206'da Temuçin burada 'Cengiz' unvanını almıştır."),
            KeyTerm("Cengiz Yasası (Yasa/Yasağ)", "Alınan kuralların yazılı hâle getirilip 'Mavi Defter' (Kıoko Debter) adıyla kanunlaştırıldığı, mutlak disiplini sağlayan hukuk düzeni."),
            KeyTerm("Kösedağ Savaşı (1243)", "Anadolu Selçuklu Devleti'nin Moğollara yenilerek İlhanlılara tâbi hâle geldiği, İkinci Beylikler dönemini başlatan savaş."),
            KeyTerm("Pax Mongolica", "Moğol hâkimiyetinin kurduğu asayiş ağı sayesinde doğu-batı ticaretinin (İpek Yolu) doruğa ulaştığı 'Moğol Barışı' çağı."),
        ],
    )
    ch5.pages.append(
        ChapterPage()
        .add_terms(ch5.key_terms)
        .add_block(BulletBlock(1, "Coğrafi Bağlam ve Haritalandırma", [
            "<b>Onon ve Kerulen Nehirleri:</b> Cengiz Han'dan önce dağınık Moğol kabilelerinin yaşadığı ve "
            "1206'da devletin kuruluşunun ilan edildiği anayurt.",
            "<b>Burhan-Haldun Dağı:</b> Cengiz Han'ın mezarının gizlendiğine inanılan, nehirlerin kaynaklarında "
            "bulunan kutsal dağ.",
            "<b>Karakurum:</b> Moğol İmparatorluğu'nun Mengü Han dönemine kadar yönetildiği tek ve merkezî başkent.",
            "<b>Bağdat:</b> 1258'de Hülâgû tarafından yerle bir edilerek 500 yıllık Sünnî Abbâsî hilafetinin sona "
            "erdirildiği, nehirlerinden günlerce mürekkep aktığı söylenen ilim başkenti.",
        ]))
    )
    ch5.pages.append(
        ChapterPage()
        .add_block(BulletBlock(2, "Kavramsal Kökler: \"Moğol\" mu, \"Tatar\" mı?", [
            "Başlangıçta hem Moğol hem Türk toplulukları arasında <b>ayrı birer boy adı</b> olan \"Tatar\" "
            "(Orhon yazıtlarında Otuz Tatar, Tokuz Tatar), Çinliler tarafından Moğolca konuşan tüm boyları "
            "genelleyici bir terim olan <b>\"Ta-ta\"</b> olarak kullanılmıştır.",
            "Çinliler bu toplulukları medeniyet seviyelerine göre <b>Ak Tatarlar, Kara Tatarlar ve Yabanî "
            "Tatarlar</b> olarak üçe ayırmıştır; Cengiz Han'ın mensup olduğu <b>Börçeginler</b> kolu \"Kara "
            "Tatarlar\" arasında yer alıyordu.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("İntikam", "Cengiz, babasını zehirleyen Tatar boyunu dağıtıp yok eder"),
            FlowStep("İsim Yaşar", "Çin, Rus ve İslam dünyası tüm Moğollara 'Tatar' demeye devam eder"),
            FlowStep("Türk Çoğunluk", "İmparatorluk nüfusunun çoğunluğu Kıpçak ve Uygur Türkleridir"),
            FlowStep("Türk Kimliği", "Moğollar bu kitlede erir; 'Tatar' bir Türk boyunun adı olur"),
        ], caption="\"Tatar\" Kimliğinin Türkleşmesi: Bir İsmin Sahip Değiştirmesi"))
        .add_table(ComparisonTable(
            "Karşılaştırmalı Tablo: Türkler ve Moğollar",
            ["Özellik", "Türkler", "Moğollar"],
            [
                ["Köken ve Dil", "Altay dil ailesi; Türkçe konuşurlar.", "Altay dil ailesi; Moğolca konuşurlar. İki dil birbirini doğrudan anlayamaz."],
                ["Yayılım Alanı", "Erken dönemde Batı'ya (Mâverâünnehir, Anadolu, Avrupa) yönelmiş, yerli halklarla (Fars, Rum, Slav) kaynaşmışlardır.", "Çekirdek coğrafyalarında kalmış, daha çok Doğu Asya (Çin, Tibet) hattıyla etkileşime girmişlerdir."],
                ["İnanç Sistemi", "Başlangıçta Gök Tanrı inancı; 8. ve 10. yy'dan itibaren kitleler hâlinde İslamiyet'i benimsemişlerdir.", "Başlangıçta Gök Tanrı (Tengrizm); sonrasında Budizm ve bir kısmı İslamiyet'i benimsemiştir."],
                ["Ortak Bozkır Kültürü", "Atlı göçebe yaşam, çadır kültürü, onluk askerî sistem ortaktır.", "Aynı unsurlara ek olarak binlerce ortak askerî/siyasi kelime (kağan, kurultay, ulus) mevcuttur."],
            ]
        ))
    )
    ch5.pages.append(
        ChapterPage()
        .add_person(CENGIZ)
        .add_block(BulletBlock(3, "Kuruluş ve Cihan Devleti Telakkisi", [
            "Moğollar, Temuçin'den önce kendi aralarında sürekli rekabet hâlinde olan <b>Naymanlar, Kereyitler, "
            "Merkitler ve Tatarlar</b> gibi dağınık boylardan oluşuyordu.",
            "Temuçin, rakiplerini tek tek bertaraf ettikten sonra <b>1206</b> baharında Onon Nehri'nin "
            "kaynağında büyük bir <b>Kurultay</b> topladı; dokuz parçalı tuğ dikilerek \"Büyük Han\" ilan "
            "edildi ve deniz/okyanus ile evrensel anlamına gelen <b>Cengiz (Çingiz)</b> unvanını aldı.",
        ]))
        .add_block(BulletBlock(4, "Cihan İmparatorluğuna Giden Dört Stratejik Teşkilat", [
            "<b>Onlu Askerî Sistem:</b> Ordu onbaşı, yüzbaşı, binbaşı, tümenbaşı şeklinde teşkilatlandırıldı.",
            "<b>Muhafız Tümeni (Gündüz ve Gece Bekçileri):</b> Kendi güvenliğini sağlamak ve komutanların "
            "çocuklarını rehin tutarak itaati garantilemek için 10.000 kişilik seçme bir birlik kuruldu.",
            "<b>Cengiz Yasası (Yasa/Yasağ):</b> Alınan kurallar yazılı hâle getirilip <b>\"Mavi Defter\" (Kıoko "
            "Debter)</b> adıyla kanunlaştırıldı; mutlak disiplin sağlandı.",
            "<b>Uygur Bürokrasisi:</b> Kendi yazıları olmayan Moğollar, medeniyetçe üstün olan <b>Uygur "
            "Türklerini</b> itaat altına alarak onların kâtiplerini ve alfabesini devlet bürokrasisinde kullandılar.",
        ]))
    )
    ch5.pages.append(
        ChapterPage()
        .add_block(BulletBlock(5, "Zaman Çizelgesi: Bozkırdan Cihana Seferler", [
            "<b>1209 / 1225–1227 (Tangut Seferleri):</b> İpek Yolu üzerindeki zengin Tangut Krallığı hedef "
            "alındı; ihanetleri üzerine ikinci sefer düzenlendi ve Cengiz Han'ın ölüm döşeğindeki emriyle bu "
            "halk tamamen yeryüzünden silindi.",
            "<b>1211–1215 (Kuzey Çin / Jin Hanedanlığı):</b> Kendisine kibirle yaklaşan Çin imparatoru mağlup "
            "edildi; 1215'te Pekin zapt edilip saray yerle bir edildi.",
            "<b>1218 (Karahitay Devleti):</b> Doğu Türkistan'da Müslümanlara baskı yapan Nayman prensi "
            "<b>Küçlüg</b>'ün üzerine Cebe Noyan gönderildi; <b>dinî serbestî taktiğiyle</b> bölge tek kurşun "
            "atılmadan fethedildi.",
            "<b>1219–1223 (Hârezmşâhlar ve İslam Dünyasının Yıkımı):</b> Otrar Faciası üzerine devasa bir "
            "orduyla Türkistan'a girildi; Otrar, Buhara, Semerkant ve Ürgenç düşürüldü, milyonlarca insan "
            "kılıçtan geçirildi.",
            "<b>1222–1224 (Kafkasya ve Kalka Zaferi):</b> Kuzey Kafkasya'daki Kıpçak-Rus ittifakı, Kalka Nehri "
            "civarında <b>sahte geri çekilme</b> taktiğiyle darmadağın edilerek Doğu Avrupa Moğollara açıldı.",
        ]))
        .add_callout(Callout("route", "Cengiz Han'ın Ölümü ve Büyük Sırrı",
            "Ağustos 1227'de hastalanan Cengiz Han şu vasiyeti bırakmıştır: <b>\"Ölümümü kimsenin öğrenmesine "
            "izin vermeyin. Hiçbir zaman ağlamayın ve yas tutmayın, böylece düşmanlarımızın hiçbir şeyden "
            "haberi olmaz.\"</b> Mezarının yeri bugün bile çözülememiş bir sırdır; <b>Moğolların Gizli "
            "Tarihi</b> adlı ana kaynakta dahi ölümü geçmez. Efsaneye göre Burhan-Haldun Dağı'na gömülmüş, "
            "defin kafilesini gören herkes öldürülmüş, mezarın üzerinden binlerce at geçirilmiş ve bir nehrin "
            "yönü değiştirilerek mezar sular altında bırakılmıştır."))
        .add_block(BulletBlock(6, "Cengiz Han Sonrası Bölünme", [
            "Ölümünden sonra imparatorluk parçalanmamış, oğulları (<b>Cuci, Çağatay, Ögedey, Tuluy</b>) devleti "
            "iki katına çıkarmıştır.",
            "Ancak <b>Mengü Han</b>'ın 1259'da ölümünden sonra çıkan taht kavgası (Kubilay - Arık Böke) merkezî "
            "otoriteyi parçalamış ve imparatorluk devasa <b>dört bağımsız hanlığa</b> bölünmüştür.",
        ]))
    )
    ch5.pages.append(
        ChapterPage()
        .add_person(HULAGU)
        .add_table(ComparisonTable(
            "Cengiz Han Sonrası Dört Büyük Hanlık",
            ["Hanlık (Kuruluş)", "Bölge ve Etkin Lider", "Temel Özellik ve Yıkılış"],
            [
                ["Yuan Hanedanlığı (1271)", "Çin ve Moğolistan — <b>Kubilay Han</b>", "Çin'i tamamen fethedip merkezi Pekin'e taşıdı; Çin kültürü ve Budizm etkisinde kaldılar. 1368'de isyanla yıkılıp bozkıra döndüler."],
                ["Altın Orda Hanlığı (1227)", "Rusya ve Deşt-i Kıpçak — <b>Batu Han</b>", "Rus knezliklerini vergiye bağladı. Berke ve Özbek Han dönemlerinde İslam'ı kabul edip Kıpçaklaşarak (Türkleşerek) eridiler."],
                ["Çağatay Hanlığı (1227)", "Türkistan ve Mâverâünnehir — <b>Çağatay soyu</b>", "Tarmaşirin Han vasıtasıyla İslam'ı benimsedi. Zamanla Türkmen kitleleri içinde eriyerek yerini Timur İmparatorluğu'na bıraktı."],
                ["İlhanlılar (1256)", "İran, Irak ve Anadolu — <b>Hülâgû Han</b>", "Haşhaşîlerin Alamut kalesini (1256) ve Abbâsî başkenti Bağdat'ı (1258) yıktı. Gazân Han devrinde İslamiyet'i resmen benimsediler."],
            ]
        ))
        .add_block(BulletBlock(7, "Moğolların İslam Dünyasındaki Çift Yönlü Etkisi", [
            "<b>Fiziksel ve İlmî Çöküş:</b> 1258'de Bağdat'ın düşüp Halife <b>Musta'sım</b>'ın öldürülmesiyle "
            "500 yıllık Abbâsî hilafeti yıkıldı. Milyonlarca insan, asırlık kütüphaneler (<b>Beytülhikme</b>) ve "
            "tarımsal altyapılar yok edildi; rasyonel ilimler geriledi, çaresizlik psikolojisi tasavvufî ve "
            "mistik hareketlerin yükselmesine zemin hazırladı.",
            "<b>Siyasi Merkezin Kayması:</b> Sünnî otoritenin Irak'ta sarsılması ve Şiî nüfuzunun artması, "
            "Ortadoğu'daki liderliği <b>1260 Aynicâlût</b> Savaşı'nda Moğolları durduran Mısır'daki "
            "<b>Memlüklere</b> kaydırmıştır.",
        ]))
    )
    ch5.pages.append(
        ChapterPage()
        .add_callout(Callout("focus", "Dikkat / Püf Noktası: Pax Mongolica",
            "Başlangıçta yıkım getiren Moğollar (özellikle <b>Altın Orda ve İlhanlılar</b>) zamanla İslam'ı "
            "kabul ettiler. Kurdukları asayiş ağı sayesinde Asya ile Avrupa arasında doğu-batı ticareti (İpek "
            "Yolu) doruğa ulaştı. Yıktıkları yerleri imar ettiler; <b>Tebriz, Sultâniye</b> gibi yeni merkezler "
            "ve İslam dünyasının en büyük rasathanelerinden <b>Merâga Rasathanesi</b>'ni kurarak bilime katkı "
            "sağladılar."))
        .add_block(BulletBlock(8, "İlhanlı Hâkimiyetinde Anadolu'nun Dönüşümü", [
            "<b>1243 Kösedağ Savaşı</b>'nda Anadolu Selçuklu Devleti'nin mağlup olmasıyla Anadolu, İlhanlı "
            "Devleti'ne tâbi hâle geldi.",
            "<b>Demografik Türk Göçü:</b> Moğol önünden kaçan Uygur, Kıpçak ve yoğun Oğuz-Türkmen boyları "
            "Anadolu uçlarına yığıldı; bu, Anadolu'nun hızla ve kalıcı olarak Türkleşmesini ve ilerideki "
            "Osmanlı'nın demografik tabanının oluşmasını sağladı.",
            "<b>İran Kültürünün Tesiri:</b> Devlet hizmetine giren mülteci İranlı bürokrat ve aydınlar sayesinde "
            "Anadolu'da Farsça ve İran mimarisi (örn. <b>Sivas Gök Medrese</b>) kökleşti.",
            "<b>Tasavvufî Rehabilitasyon:</b> Güvensizlik kaosunda <b>Yunus Emre</b> ve <b>Mevlânâ</b> gibi "
            "isimler halka psikolojik direnç verirken; Ahiler, Alperenler ve <b>Bacıyân-ı Rûm</b> sivil savunma "
            "ve İslamlaştırma misyonunu üstlendi.",
            "<b>Devlet Teşkilatında İzler:</b> \"Kurultay\", \"ulus\", \"yasak\" gibi Moğolca kelimeler ve idarî "
            "gelenekler Anadolu beyliklerine miras kaldı.",
        ]))
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "Moğol istilası, Orta Çağ İslam dünyası için bir <b>kıyamet senaryosu</b> olarak başlamış; asırlık "
            "ilim merkezlerini ve Abbâsî hilafetini yok etmiştir. Ancak bu büyük yıkım, devasa Türkmen "
            "göçlerini Anadolu'ya iterek buranın ebedî bir Türk yurdu olmasına sebep olmuş ve Moğolların da "
            "zamanla Türkleşip İslamlaşmasıyla <b>\"Pax Mongolica\"</b> (Moğol Barışı) denilen küresel ticaret "
            "ve kültür entegrasyonu çağını başlatmıştır."))
    )
    ch5.pages.append(
        ChapterPage()
        .add_summary("Onon ve Kerulen kıyılarındaki dağınık boyları 1206 Kurultayı'nda birleştiren Temuçin, "
            "onlu askerî sistem, Muhafız Tümeni, Cengiz Yasası ve Uygur bürokrasisiyle bir cihan imparatorluğu "
            "kurmuş; Tangut, Çin, Karahitay, Hârezm ve Kalka seferleriyle dünyanın haritasını değiştirmiştir. "
            "Mengü Han'ın ölümüyle Yuan, Altın Orda, Çağatay ve İlhanlı olmak üzere dört hanlığa bölünen "
            "imparatorluk; 1258'de Bağdat'ı yıkarak Abbâsî hilafetine son verirken liderliği Memlüklere "
            "devretmiş, ancak Türkmen göçlerini Anadolu'ya iterek Osmanlı'nın demografik tabanını hazırlamış ve "
            "Pax Mongolica ile küresel bir ticaret çağı açmıştır.")
    )

    chapters = [ch1, ch2, ch3, ch4, ch5]

    # =====================================================================
    # SÖZLÜK — 36 kavram (18 x 2 sayfa)
    # =====================================================================
    glossary = [
        Concept("Hârezmşâh", "Hârezm bölgesine hâkim olan veya burayı idare eden yöneticilere verilen unvan.", "Hârezmşâhlar", 1),
        Concept("Taşt-dâr", "Hükümdar elini yıkarken leğen ve ibrik tutan, saray temizliğinden sorumlu görevli.", "Anûştegin", 1),
        Concept("Gürgenç", "Hârezm bölgesinin ve Hârezmşâhlar Devleti'nin efsanevi başkenti (Gürgânc-Ürgenç).", "Hârezmşâhlar", 1),
        Concept("Katvan Savaşı (1141)", "Sultan Sencer'in zayıflamasından yararlanan Atsız'ın Merv ve Nişâbûr'u zapt ettiği dönemeç.", "Atsız", 1),
        Concept("Otrar Faciası (1218)", "Vali İnalcık'ın Moğol ticaret kervanını yağmalayıp tüccarları öldürmesi; istilanın fitili.", "Alâeddîn Muhammed", 1),
        Concept("Yassıçimen Savaşı (1230)", "Hârezmşâh ordusunun Selçuklu-Eyyubî ittifakına yenilerek yıkıma sürüklendiği savaş.", "Celâleddîn Hârezmşâh", 1),
        Concept("Haşar", "Şehir ve kalelerin savunmasında kullanılan gönüllü kuvvetler.", "Hârezmşâh teşkilatı", 1),
        Concept("Akza'l-kuzât", "Hükümdar tarafından atanan, şer'î yargı mekanizmasının başındaki baş kadı.", "Hârezmşâh teşkilatı", 1),
        Concept("Thema Anatolikon", "Bizans'ın doğu idarî birimi; Anatole → Natolia → Anadolu evriminin kaynağı.", "Anadolu adlandırması", 2),
        Concept("Bilâd-ı Rûm", "Klasik İslam literatüründe Doğu Roma egemenliğindeki Anadolu için kullanılan ad.", "Anadolu adlandırması", 2),
        Concept("Savâif ve Şevâtî", "Emevîlerin Bizans'ı yıpratmak için yılda iki kez düzenlediği yaz ve kış seferleri.", "Emevî dönemi", 2),
        Concept("Avâsım", "Abbâsîlerin sınır güvenliği için Tarsus-Maraş hattında kurduğu askerî valilikler.", "Abbâsî dönemi", 2),
        Concept("Suğûr", "Avâsım'ın önündeki, tahkim edilmiş uç bölgeler / sınır hatları.", "Abbâsî dönemi", 2),
        Concept("Hilal (Turan) Taktiği", "Sahte geri çekilmeyle düşman merkezini kuşatıp imha etmeye dayanan Türk savaş taktiği.", "Malazgirt 1071", 2),
        Concept("Gaziyân-ı Rûm", "Alp'lık ruhunu mücahitlikle sentezleyen, dervişlikle askerliği harmanlayan zümre.", "Manevi fatihler", 2),
        Concept("Abdâlân-ı Rûm", "Dünyevi ilgilerden uzaklaşıp manevi fethi gerçekleştiren derviş topluluğu.", "Manevi fatihler", 2),
        Concept("Ahiyân-ı Rûm", "Ekonomik hayatı ahlaki-dinî zemine oturtan, dayanışmayı sağlayan esnaf teşkilatı.", "Manevi fatihler", 2),
        Concept("Kösedağ Savaşı (1243)", "Anadolu Selçuklu'nun Moğollara yenilip İlhanlılara tâbi olduğu, beyliklerin doğduğu savaş.", "İlhanlı hâkimiyeti", 2),
        Concept("Memlük", "Köle pazarlarından satın alınıp askerî eğitimle yetiştirilen Türk atlı birlikleri.", "Memlükler", 3),
        Concept("İktâ", "Devlet topraklarının gelirlerinin asker ve memurlara maaş karşılığı tahsis edilmesi.", "Selçuklu-Zengî mirası", 3),
        Concept("Bahrî Memlükler", "1250–1382 arası, Nil (Bahr) üzerindeki Ravza Adası'na yerleştirilen Türk memlükleri.", "Memlükler I. dönem", 3),
        Concept("Burcî Memlükler", "1382–1517 arası, Kahire kalesinin burçlarına yerleştirilen Çerkez memlükleri.", "Memlükler II. dönem", 3),
        Concept("Hıttin Savaşı (1187)", "Selâhaddin Eyyûbî'nin Haçlıları bozguna uğratıp Kudüs'ü 88 yıl sonra geri aldığı savaş.", "Selâhaddin Eyyûbî", 3),
        Concept("Aynicâlût Savaşı (1260)", "Kutuz idaresindeki Memlüklerin Moğol yenilmezlik efsanesini yıktığı savaş.", "Memlükler", 3),
        Concept("Şecerüddürr", "1250'de memlüklerin tahta çıkardığı, Aybek ile evlenip saltanattan feragat eden kadın sultan.", "İktidar değişimi 1250", 3),
        Concept("Akkâ'nın Fethi (1291)", "el-Melikü'l-Eşref Halîl'in iki asırlık Haçlı işgaline son verdiği fetih.", "Memlükler", 3),
        Concept("Delhi Sultanlığı", "Kutbeddîn Aybeg'in 1206'da kurduğu, Moğol tehdidini sınırda durduran Türk devleti.", "Hindistan", 4),
        Concept("Gûrlular", "Hindistan'daki fetihleriyle Delhi Sultanlığı'nın önünü açan hânedan.", "Hindistan", 4),
        Concept("Panipat Savaşı (1526)", "Bâbür Şah'ın ateşli silah üstünlüğüyle Delhi Sultanlığı'na son verdiği savaş.", "Bâbür Şah", 4),
        Concept("Bâbürnâme", "Bâbür Şah'ın Türkçe kaleme aldığı, dönemin Hindistan'ını anlatan otobiyografik eser.", "Bâbür Şah", 4),
        Concept("Evrengzib (Âlemgîr)", "Bâbürlü sınırlarını en uç noktalara taşıyan, Şah Cihan'ın oğlu hükümdar.", "Bâbürlüler", 4),
        Concept("Kurultay", "Han seçimi ve büyük kararların alındığı meclis; 1206'da Cengiz unvanı burada verilmiştir.", "Cengiz Han", 5),
        Concept("Cengiz Yasası (Yasağ)", "Yazılı hâle getirilip 'Mavi Defter' adıyla kanunlaşan, mutlak disiplini sağlayan hukuk düzeni.", "Cengiz Han", 5),
        Concept("Muhafız Tümeni", "Komutanların çocuklarını rehin tutarak itaati garantileyen 10.000 kişilik seçme birlik.", "Cengiz Han", 5),
        Concept("Kalka Savaşı (1223)", "Kıpçak-Rus ittifakının sahte geri çekilmeyle dağıtıldığı, Doğu Avrupa'yı açan zafer.", "Moğol seferleri", 5),
        Concept("Pax Mongolica", "Moğol asayiş ağı sayesinde İpek Yolu ticaretinin doruğa ulaştığı 'Moğol Barışı' çağı.", "Moğol mirası", 5),
    ]

    # =====================================================================
    # TEST — 20 Soruluk Genel Değerlendirme
    # =====================================================================
    test_questions = [
        TestQuestion(1, "Hârezmşâhlar Devleti'nin fiilî kuruluşu, 1097'de hangi Selçuklu sultanı zamanında Kutbeddîn Muhammed'in Hârezmşâh tayin edilmesiyle gerçekleşmiştir?",
            {"A": "Alp Arslan", "B": "Melikşah", "C": "Berkyaruk", "D": "Sencer", "E": "III. Tuğrul"}),
        TestQuestion(2, "Hânedanın atası Anûştegin'in Selçuklu sarayında yükseldiği, hükümdar elini yıkarken leğen ve ibrik tutan görev hangisidir?",
            {"A": "Akza'l-kuzât", "B": "Taşt-dâr", "C": "Haşar", "D": "Dîvân-ı İşraf", "E": "Emîr-i Hâcib"}),
        TestQuestion(3, "Atsız'ın Merv ve Nişâbûr'u zapt etmesine imkân veren, Sultan Sencer'in zayıflamasıyla sonuçlanan 1141 tarihli savaş hangisidir?",
            {"A": "Katvan Savaşı", "B": "Pasinler Savaşı", "C": "Yassıçimen Savaşı", "D": "Malazgirt Savaşı", "E": "Kösedağ Savaşı"}),
        TestQuestion(4, "Moğol istilasının fitilini ateşleyen Otrar Faciası'nda (1218) Moğol ticaret kervanını yağmalatan vali kimdir?",
            {"A": "Küçlüg", "B": "Cebe Noyan", "C": "Sultan-şâh", "D": "İnalcık", "E": "Bilge Tegin"}),
        TestQuestion(5, "Celâleddîn Hârezmşâh'ın 1230'da Ahlat'ı kuşatıp tahrip etmesinin doğrudan sonucu aşağıdakilerden hangisidir?",
            {"A": "Kara-Hıtayların Hârezm'e saldırması", "B": "Türkiye Selçuklu ve Eyyubîlerin ona karşı birleşmesi",
             "C": "Irak Selçuklularının ortadan kalkması", "D": "Moğollarla barış antlaşması imzalanması",
             "E": "Bağdat'ta hilafetin yeniden tesisi"}),
        TestQuestion(6, "\"Anadolu\" adının kökeni olan, Bizans'ın başkente göre doğuda kalan idarî birimine verilen ad nedir?",
            {"A": "Minor Asia", "B": "Arz-ı Rûm", "C": "Thema Anatolikon", "D": "Diyar-ı Rûm", "E": "Bilâd-ı Rûm"}),
        TestQuestion(7, "Abbâsîlerin sınır güvenliğini sağlamak amacıyla Tarsus ve Maraş hattında kurduğu askerî valiliklere ne ad verilir?",
            {"A": "Suğûr", "B": "Savâif", "C": "Şevâtî", "D": "Avâsım", "E": "İktâ"}),
        TestQuestion(8, "Malazgirt Meydan Muharebesi'nin kaderini değiştiren temel gelişme aşağıdakilerden hangisidir?",
            {"A": "Bizans ordusundaki Peçenek ve Uz Türklerinin Selçuklu safına geçmesi",
             "B": "Alp Arslan'ın Halep kuşatmasını sürdürmesi", "C": "Ani Kalesi'nin daha önce fethedilmiş olması",
             "D": "Haçlıların Bizans'a yardıma gelmemesi", "E": "Bizans ordusunun sayıca az olması"}),
        TestQuestion(9, "Malazgirt sonrası kurulan ilk Türk beyliği ve merkezî bölgesi hangi seçenekte doğru verilmiştir?",
            {"A": "Dânişmendliler — Sivas", "B": "Artuklular — Mardin", "C": "Saltuklular — Erzurum",
             "D": "Mengücekliler — Divriği", "E": "Dilmaçoğulları — Bitlis"}),
        TestQuestion(10, "Anadolu'nun ilk medresesi olan Yağıbasan Medresesi'ni inşa eden, dönemin en güçlü beyliği hangisidir?",
            {"A": "Saltuklular", "B": "Dânişmendliler", "C": "Mengücekliler", "D": "Artuklular", "E": "Karamanoğulları"}),
        TestQuestion(11, "Ticari ve ekonomik hayatı ahlaki-dinî bir zemine oturtarak toplumsal dayanışmayı sağlayan esnaf teşkilatı hangi zümredir?",
            {"A": "Gaziyân-ı Rûm", "B": "Abdâlân-ı Rûm", "C": "Ahiyân-ı Rûm", "D": "Bacıyân-ı Rûm", "E": "Tasavvuf Erbabı"}),
        TestQuestion(12, "1144'te Urfa'yı Haçlılardan geri alarak İslam dünyasının kahramanı olan devlet adamı kimdir?",
            {"A": "Nureddin Mahmud Zengî", "B": "İmâdüddin Zengî", "C": "Selâhaddin Eyyûbî", "D": "Şîrkûh", "E": "Baybars"}),
        TestQuestion(13, "Memlüklerin I. dönemine \"Bahrî\" denmesinin sebebi nedir?",
            {"A": "Kahire kalesinin burçlarına yerleştirilmeleri", "B": "Çerkez kökenli olmaları",
             "C": "Nil Nehri (Bahr) üzerindeki Ravza Adası'na yerleştirilmeleri", "D": "Deniz seferleriyle ün kazanmaları",
             "E": "Bahreyn'den getirilmiş olmaları"}),
        TestQuestion(14, "1250'de Turan Şah'ın öldürülmesinden sonra tahta çıkarılan ve Memlük emîri İzzeddin Aybek ile evlenerek saltanattan onun lehine feragat eden kişi kimdir?",
            {"A": "Terken Hâtûn", "B": "Şecerüddürr", "C": "Mama Hatun", "D": "Bacıyân-ı Rûm", "E": "el-Melikü's-Sâlih"}),
        TestQuestion(15, "Moğolların Orta Doğu'daki yenilmezlik efsanesini yıkan 1260 tarihli savaş ve Memlük komutanı hangi seçenekte doğru eşleştirilmiştir?",
            {"A": "Hıttin — Selâhaddin", "B": "Kalka — Cebe Noyan", "C": "Aynicâlût — Kutuz",
             "D": "Panipat — Bâbür Şah", "E": "Ridâniye — Yavuz Sultan Selim"}),
        TestQuestion(16, "Hindistan'da kalıcı bir Türk-İslam medeniyetinin tesis edilmesindeki temel sebep aşağıdakilerden hangisidir?",
            {"A": "Yalnızca askerî fetihlerin başarısı", "B": "Hindistan'ın Moğol teröründen azade bir vaha olarak kalması",
             "C": "İngilizlerin bölgeden çekilmesi", "D": "Fâtımî hilafetinin desteği",
             "E": "Delhi'nin deniz ticaret yolları üzerinde bulunması"}),
        TestQuestion(17, "Bâbür Şah'ın Türkçe kaleme aldığı, dönemin Hindistan coğrafyasını ve sosyal yapısını anlatan otobiyografik eseri hangisidir?",
            {"A": "Moğolların Gizli Tarihi", "B": "Mavi Defter", "C": "Bâbürnâme", "D": "Tâc Mahal", "E": "Kıoko Debter"}),
        TestQuestion(18, "Cengiz Han'ın, kendi yazıları olmayan Moğolların devlet bürokrasisini kurmak için kâtiplerinden ve alfabesinden yararlandığı Türk topluluğu hangisidir?",
            {"A": "Kıpçaklar", "B": "Naymanlar", "C": "Uygurlar", "D": "Kereyitler", "E": "Merkitler"}),
        TestQuestion(19, "Aşağıdaki hanlık-lider eşleştirmelerinden hangisi yanlıştır?",
            {"A": "Yuan Hanedanlığı — Kubilay Han", "B": "Altın Orda Hanlığı — Batu Han",
             "C": "İlhanlılar — Hülâgû Han", "D": "Çağatay Hanlığı — Tarmaşirin Han",
             "E": "Altın Orda Hanlığı — Gazân Han"}),
        TestQuestion(20, "Moğol istilasının İslam dünyasındaki uzun vadeli etkileriyle ilgili aşağıdakilerden hangisi söylenemez?",
            {"A": "Abbâsî hilafetinin yıkılmasıyla siyasi liderlik Memlüklere kaymıştır",
             "B": "Türkmen göçleri Anadolu'nun kalıcı Türkleşmesini hızlandırmıştır",
             "C": "Pax Mongolica ile İpek Yolu ticareti doruğa ulaşmıştır",
             "D": "Rasyonel ilimler gerilemiş, tasavvufî hareketler güçlenmiştir",
             "E": "Moğollar İslam'ı hiçbir zaman benimsememiş, Budizm'de kalmışlardır"}),
    ]

    answer_key_items = [
        AnswerItem(1, "C", "Devletin fiilî kuruluşu <b>1097</b>'de, Selçuklu Sultanı <b>Berkyaruk</b> zamanında Anûştegin'in oğlu Kutbeddîn Muhammed'in Hârezmşâh tayin edilmesiyle gerçekleşmiştir."),
        AnswerItem(2, "B", "<b>Taşt-dâr</b>, hükümdar elini yıkarken leğen ve ibrik tutan, saray temizliğinden sorumlu görevlidir; Anûştegin bu makamla Hârezm gelirlerinden yararlanmıştır."),
        AnswerItem(3, "A", "<b>1141 Katvan Savaşı</b>'nda Sencer'in zayıflamasından faydalanan Atsız, Merv ve Nişâbûr'u zapt etmiştir."),
        AnswerItem(4, "D", "Otrar valisi <b>İnalcık</b>, Moğol ticaret kervanını yağmalatıp tüccarları öldürtmüş; bu olay (Otrar Faciası, 1218) istilanın fitilini ateşlemiştir."),
        AnswerItem(5, "B", "Moğollara karşı birleşmek yerine Ahlat'ı tahrip etmesi, <b>I. Alâeddin Keykubad ve Eyyubîlerin</b> ona karşı savaş açmasına ve Yassıçimen bozgununa yol açmıştır."),
        AnswerItem(6, "C", "Grekçe \"doğu\" anlamındaki Anatole'den türeyen <b>Thema Anatolikon</b>, halk ağzında Natolia ve nihayet Anadolu formuna evrilmiştir."),
        AnswerItem(7, "D", "<b>Avâsım</b> askerî valilikleri, <b>Suğûr</b> ise onların önündeki uç bölgeler/sınır hatlarıdır; Savâif ve Şevâtî ise Emevî yaz-kış seferleridir."),
        AnswerItem(8, "A", "Bizans ordusundaki <b>Peçenek ve Uz (Guz)</b> Türklerinin karşılarındakilerin soydaşları olduğunu anlayıp Selçuklu safına geçmesi savaşın kaderini belirlemiştir."),
        AnswerItem(9, "C", "<b>Saltuklular</b> (Erzurum ve çevresi), Malazgirt sonrası kurulan ilk Türk beyliğidir; Mama Hatun Külliyesi ve Çifte Minareli Medrese eserlerindendir."),
        AnswerItem(10, "B", "Anadolu'nun ilk medresesi olan <b>Yağıbasan Medresesi</b>'ni, dönemin en güçlü beyliği olan Dânişmendliler inşa etmiştir."),
        AnswerItem(11, "C", "<b>Ahiyân-ı Rûm (Ahiler)</b>, ekonomik hayatı ahlaki-dinî bir zemine oturtan esnaf teşkilatıdır; Gaziyân savaşçı, Abdâlân ise derviş zümresidir."),
        AnswerItem(12, "B", "1127'de Musul valiliğine atanan <b>İmâdüddin Zengî</b>, 1144'te Urfa'yı alarak buradaki Haçlı idaresine son vermiştir."),
        AnswerItem(13, "C", "I. dönem memlükleri, Nil Nehri (<b>Bahr</b>) üzerindeki Ravza Adası'na yerleştirildikleri için \"Bahrî\" adını almışlardır; Burcî ise kale burçlarından gelir."),
        AnswerItem(14, "B", "<b>Şecerüddürr</b> tahta çıkarılmış, ardından Memlük emîri İzzeddin Aybek ile evlenip saltanattan onun lehine feragat etmiştir."),
        AnswerItem(15, "C", "Komutan <b>Kutuz</b> idaresindeki Memlük ordusu <b>1260 Aynicâlût Savaşı</b>'nda Moğolların yenilmezlik efsanesini yıkmıştır."),
        AnswerItem(16, "B", "Temel sebep askerî fetihler değil, Hindistan'ın <b>Moğol teröründen azade bir vaha</b> kalarak Orta Asya medeniyetinin buraya transfer edilmesini sağlamasıdır."),
        AnswerItem(17, "C", "<b>Bâbürnâme</b>, Bâbür Şah'ın Türkçe kaleme aldığı otobiyografik eserdir; Moğolların Gizli Tarihi ve Mavi Defter Moğollara aittir."),
        AnswerItem(18, "C", "Kendi yazıları olmayan Moğollar, medeniyetçe üstün olan <b>Uygur Türklerini</b> itaat altına alarak kâtiplerini ve alfabelerini bürokraside kullanmışlardır."),
        AnswerItem(19, "E", "<b>Gazân Han</b> Altın Orda'nın değil <b>İlhanlıların</b> hükümdarıdır; Altın Orda'da İslamlaşma Berke ve Özbek Han dönemlerinde gerçekleşmiştir."),
        AnswerItem(20, "E", "Moğollar, özellikle <b>Altın Orda ve İlhanlılar</b> üzerinden zamanla İslam'ı kabul etmişlerdir; bu yüzden E seçeneği yanlıştır."),
    ]

    return CoursePack(
        course_code="İSL. TARİHİ III",
        title='İslam Tarihi<span class="accent-word"> III</span>',
        subtitle="Hârezmşâhlardan Moğol İstilasına: Türk-İslam Devletleri",
        description=(
            "Ceyhun Nehri'nin bereketli sularından beslenen bir vilayetten devasa bir imparatorluğa dönüşen "
            "Hârezmşâhlar ile başlayıp, Anadolu'nun Türkleşmesine, Mısır'daki Memlük direnişine, Hindistan'daki "
            "Delhi ve Bâbürlü ihtişamına ve nihayet Moğol kasırgasına kadar uzanan; Türk-İslam medeniyetinin "
            "kılıç ve kalemle yazılmış serüveninin final sınavı özeti."
        ),
        theme="slate",
        theme_color="#1D4E79",
        icon_text="İ",
        chapters=chapters,
        glossary=glossary,
        test_title="Genel Değerlendirme Testi",
        test_subtitle="Hârezmşâhlardan Pax Mongolica'ya, İslam Tarihi III üzerine kapsamlı çoktan seçmeli test",
        test_instructions="Aşağıdaki sorularda beş seçenekten yalnızca birini işaretleyiniz. Süre: 30 dakika.",
        test_questions=test_questions,
        answer_key_intro="Her sorunun doğru cevabı ve kısa gerekçesi aşağıda yer almaktadır.",
        answer_key_items=answer_key_items,
        overview_lead=(
            "Bu ders; <b>Hârezmşâhların</b> Ceyhun kıyısındaki yükselişi ve Otrar Faciası'yla gelen çöküşünden "
            "başlayarak, <b>Anadolu'nun Türkleşmesine</b>, Mısır'daki <b>Memlük kalkanına</b>, Hindistan'daki "
            "<b>Delhi ve Bâbürlü ihtişamına</b> ve nihayet dünyanın haritasını yeniden çizen <b>Moğol "
            "kasırgasına</b> uzanan beş temel durağı bir bütün olarak sunar."
        ),
        overview_cards=[
            {"title": "Hârezmşâhlar", "text": "Taşt-dâr Anûştegin'in soyundan imparatorluğa; Otrar Faciası'ndan Yassıçimen yıkımına."},
            {"title": "Anadolu'nun Dönüşümü", "text": "Emevî akınlarından Malazgirt'e, iktâ beyliklerinden dervişlerin manevi fethine."},
            {"title": "Memlükler", "text": "Zengî-Eyyûbî mirasından doğan köle-asker sınıfının üç asırlık koruyucu kalkanı."},
            {"title": "Hindistan'da Türkler", "text": "Delhi Sultanlığı'nın Moğol kalkanı ve Bâbürlülerin Tâc Mahal'e uzanan ihtişamı."},
            {"title": "Cengiz Han ve Teşkilat", "text": "Onlu sistem, Muhafız Tümeni, Cengiz Yasası ve Uygur bürokrasisiyle kurulan cihan devleti."},
            {"title": "Dört Hanlık ve Pax Mongolica", "text": "Yuan, Altın Orda, Çağatay ve İlhanlılar; yıkımın ardından gelen Moğol Barışı."},
        ],
        overview_flow=[
            ("Hârezmşâhlar", "Ceyhun'dan imparatorluğa (1097–1231)"),
            ("Anadolu", "Malazgirt ve Türkleşme (1071 sonrası)"),
            ("Memlükler", "Aynicâlût kalkanı (1250–1517)"),
            ("Hindistan", "Delhi ve Bâbürlüler (1206–1858)"),
            ("Moğollar", "Cengiz Han'dan Pax Mongolica'ya"),
        ],
        overview_note=(
            "Sınavda en çok karıştırılan yer, <b>Moğol istilasının dört farklı coğrafyadaki zıt sonuçlarıdır</b>: "
            "aynı istila Hârezmşâhları <b>yıkmış</b>, Anadolu'yu Türkmen göçleriyle <b>Türkleştirmiş</b>, "
            "Memlükleri Aynicâlût zaferiyle <b>İslam dünyasının lideri yapmış</b> ve Hindistan'ı mülteci "
            "âlim-sanatkâr akınıyla <b>zenginleştirmiştir</b>."
        ),
    )
