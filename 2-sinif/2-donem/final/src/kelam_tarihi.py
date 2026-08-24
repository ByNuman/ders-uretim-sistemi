# -*- coding: utf-8 -*-
"""KELÂM TARİHİ — Görsel Ders Notu Kitabı, içerik tanımı.
Kaynak: 'KELAM TARİHİ_FİNAL ÖZET.pdf' (ham metin özet, 24 sayfa, 9 bölüm).
"""
import sys
from pathlib import Path
# Proje kökü: src/ -> <sinav> -> <donem> -> <sinif> -> KÖK (4 seviye yukarı)
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from content_model import (
    Person, KeyTerm, Callout, FlowStep, FlowDiagram, ComparisonTable,
    InfoCard, BulletBlock, Chapter, ChapterPage, Concept, CoursePack,
    TestQuestion, AnswerItem,
)

# ---------------------------------------------------------------------------
# KİŞİLER (TEK KAYNAK) — tarihler/eserler yalnızca burada tanımlanır
# ---------------------------------------------------------------------------

VASIL = Person(
    id="vasil", name="Vâsıl b. Atâ", years="ö. 131/748",
    tagline="Mu'tezile'nin Kurucusu, Fâsık Formülünün Mucidi",
    bio=["Aslen Fârisî bir <b>mevâlî</b> olan Vâsıl, \"r\" harfini telaffuz edemediği hâlde konuşurken bu harfi "
         "hiç kullanmayacak kadar üstün bir hitabet gücüne sahipti. Hasan-ı Basrî'nin ders halkasında büyük "
         "günah tartışması sırasında <b>el-menzile beyne'l-menzileteyn</b> tezini ortaya atarak meclisten "
         "ayrılmış; İslâm'ı düalist inançlara karşı savunmak için farklı bölgelere özel davetçiler göndermiştir."],
    key_work="Kitâbu Elfi Mes'ele fi'r-Red ale'l-Mâneviyye", initials="VA",
)
AMR = Person(
    id="amr", name="Amr b. Ubeyd", years="ö. 144/761",
    tagline="Ekolün İkinci Kurucusu, Zâhid Muhalif",
    bio=["Dokumacılıkla geçinen, zühd ve takvasıyla Abbâsî halifesi <b>Mansûr</b>'un bile saygısını kazanmış bir "
         "isimdir. Vâsıl'dan farklı olarak Cemel Savaşı'na katılan <b>her iki grubun da toptan fâsık</b> "
         "olduğunu ve cehennemde ebedî kalacaklarını sert bir dille savunmuştur."],
    key_work="er-Red ale'l-Kaderiyye · Kitâbü'l-'Adl ve't-tevhîd",
)
ALLAF = Person(
    id="allaf", name="Ebü'l-Hüzeyl el-Allâf", years="ö. 235/849-50",
    tagline="Usûl-i Hamse'nin Mimarı, Basra Ekolünün Kurucusu",
    bio=["Beş temel esası (<b>Usûl-i Hamse</b>) ilk defa kavramsallaştırıp bir inanç sistemi hâline getiren asıl "
         "mimardır; hayvan yemi ticareti yaptığı için \"Allâf\" lakabını almıştır. <b>Atomcu felsefeyi</b> "
         "(cüz lâ yetecezzâ) İslâm'a uyarlayarak âlemin hâdis olduğunu temellendirmiş; âhirette cennet ve "
         "cehennem ehlinin hareketlerinin \"dâimî bir sükûna\" gireceğini savunmuştur."],
    key_work="Usûl-i Hamse'nin sistemleştirilmesi", initials="EH",
)
NAZZAM = Person(
    id="nazzam", name="İbrâhim en-Nazzâm", years="ö. 231/845",
    tagline="Tafra, Kümûn ve Sarfe Teorilerinin Sahibi",
    bio=["Ebü'l-Hüzeyl'in yeğeni olan Nazzâm, İslâm'ı Dehriyye ve Sümeniyye'ye karşı müdafaa etmiş parlak bir "
         "felsefecidir. Allah'ın kullarına yalnızca iyilik yaratabileceğini, <b>kötülük yaratmaya gücünün "
         "yetmeyeceğini</b> iddia etmiş; tafra, kümûn-zuhûr ve sarfe nazariyeleriyle İslâm düşüncesinde en çok "
         "tartışılan dört teoriyi üretmiştir."],
    key_work="el-Cüz (Kitâbü'z-zerre) · Hareketü'l-ecsâm",
)
CAHIZ = Person(
    id="cahiz", name="Câhiz", years="ö. 255/869",
    tagline="Mu'tezile'nin Edebiyatçı Dehâsı",
    bio=["Cehennemliklerin azabının sonsuz olmayacağını, belli bir süre sonra <b>ateşin tabiatına uygun hâle "
         "gelerek</b> acı hissetmeyeceklerini savunmuştur. Eserleri günümüze ulaşan nadir Mu'tezilîlerdendir: "
         "<b>Kitâbü'l-Hayevân</b> canlı türleri üzerinden sosyolojik-ontolojik bir analiz, <b>el-Beyân ve't-"
         "tebyîn</b> ise Arap hitabet ve edebiyatının ilk büyük eserlerindendir."],
    key_work="Kitâbü'l-Hayevân · el-Beyân ve't-tebyîn · el-Buhalâ",
)
EBU_HASIM = Person(
    id="ebuhasim", name="Ebû Hâşim el-Cübbâî", years="ö. 321/933",
    tagline="Ahvâl Teorisinin Kurucusu",
    bio=["Ebû Ali el-Cübbâî'nin oğlu olan bu son derece zeki ve sorgulayıcı kelâmcı, Allah'ın sıfatlarını "
         "açıklamak için <b>Ahvâl (Hâller)</b> teorisini kurmuştur: sıfatlar Allah'ın zâtının ötesinde hususi "
         "birer \"hâl\"dir; ne tam olarak vardır ne de yoktur, ne kadîmdir ne hâdistir. Böylece "
         "<b>teaddüd-i kudemâ</b> problemini aşmayı hedeflemiştir."],
    key_work="Ahvâl (Hâller) Teorisi", initials="EC",
)
ABDULCEBBAR = Person(
    id="abdulcebbar", name="Kâdî Abdülcebbâr", years="ö. 415/1025",
    tagline="Mu'tezile'nin Son Büyük Ansiklopedisti",
    bio=["Büveyhî veziri <b>Sâhib b. Abbâd</b> tarafından başkadı (kâdılkudât) yapılmıştır. Eserleri, Mu'tezile "
         "hakkında günümüze ulaşan en temel <b>birinci el kaynaklardır</b>: yirmi cüzlük <b>el-Muğnî</b> Basra "
         "kelâmının bütün sistematiğini aktarır, <b>Şerhu'l-Usûli'l-Hamse</b> ise beş esasın temel kitabıdır."],
    key_work="el-Muğnî · Şerhu'l-Usûli'l-Hamse",
)
BISR = Person(
    id="bisr", name="Bişr b. Mu'temir", years="ö. 210/825",
    tagline="Bağdat Ekolünün Kurucusu, Tevellüd Teorisyeni",
    bio=["Hârun Reşîd ve Me'mûn dönemlerinde sarayda büyük hürmet gören Bişr, Basra'nın \"Allah kulları için "
         "daima <b>aslah</b>ı yaratmak zorundadır\" tezine karşı çıkmış; bunun zorunluluk değil ilâhî bir ihsan "
         "(<b>Lütuf teorisi</b>) olduğunu söylemiştir. İnsanın kendi kudretiyle başka bir şey üzerinde etki "
         "oluşturmasını açıklayan <b>Tevellüd</b> (bağımlı fiiller) teorisini geliştirmiştir."],
    key_work="Tevellüd (bağımlı fiiller) teorisi",
)
ESARI = Person(
    id="esari", name="Ebü'l-Hasan el-Eş'arî", years="ö. 324/935",
    tagline="Kırk Yaşında Mu'tezile'yi Terk Eden Sentezci",
    bio=["Sahâbî Ebû Mûsâ el-Eş'arî'nin soyundan gelir. Annesinin Mu'tezile imamı <b>Ebû Ali el-Cübbâî</b> ile "
         "evlenmesi üzerine üvey babasının ders halkasında yetişmiş, kırk yaşına kadar koyu bir Mu'tezilî "
         "olmuştur. <b>Rü'yetullah'ın inkârı</b> ve <b>kulun kendi fiilini yaratması</b> meselelerindeki "
         "şüpheleri sebebiyle uzun bir uzletin ardından Basra Merkez Camii'nde i'tizâlden ayrıldığını ilan "
         "etmiş; <b>Kesb</b> teorisiyle akıl-nakil dengesini kurmuştur."],
    key_work="Kitâbü'l-Luma' · Makâlâtü'l-İslâmiyyîn", initials="EE",
)
BAKILLANI = Person(
    id="bakillani", name="Ebûbekir el-Bâkıllânî", years="ö. 403/1013",
    tagline="Ehl-i Sünnet'in Keskin Kılıcı, Eş'arîliğin Sistemcisi",
    bio=["\"Hicrî IV. asrın müceddidi\" ve \"Ehl-i Sünnet'in keskin kılıcı\" unvanlarını taşır; Eş'arîliği "
         "sistemleştiren en önemli isimdir. <b>Atom</b> düşüncesini İslâm tabiat felsefesinin merkezine "
         "oturtmuş, mucizeleri temellendirmek için tabiatta zorunlu bir determinizm olmadığını savunarak "
         "<b>Âdet Teorisi</b>'ni kurmuş ve <b>in'ikâsü'l-edille</b> ilkesini geliştirmiştir."],
    key_work="Temhîdü'l-evâ'il · İ'câzü'l-Kur'ân",
)
CUVEYNI = Person(
    id="cuveyni", name="İmâmü'l-Haremeyn el-Cüveynî", years="ö. 478/1085",
    tagline="Mütekaddimûn'dan Müteahhirûn'a Geçişin Köprüsü",
    bio=["Nizâmülmülk tarafından Nîşâbur Nizâmiyye Medresesi'nin başına getirilmiş ve <b>Gazzâlî'yi "
         "yetiştirmiştir</b>; Mekke ve Medine'de kaldığı için \"İmâmü'l-Haremeyn\" adını almıştır. Bâkıllânî'nin "
         "<b>in'ikâsü'l-edille</b> ilkesini sertçe reddetmiş, Mu'tezile'nin icadı olan Ahvâl teorisini bir dönem "
         "benimsemiş ve âlemdeki zorunlu nedensellik bağını tamamen yıkmıştır."],
    key_work="eş-Şâmil fi usûli'd-dîn · el-Akîdetü'n-Nizâmiyye",
)
GAZZALI = Person(
    id="gazzali", name="Ebû Hâmid el-Gazzâlî", years="ö. 505/1111",
    tagline="Hüccetü'l-İslâm, Felsefi Kelâmın Kapısını Açan İmam",
    bio=["Mütekaddimûn devrini kapatıp <b>müteahhirûn</b> dönemini başlatan kişidir. Bâtınîlik ve felsefeyle "
         "sert hesaplaşmalara girmiş, filozofları ilâhiyat meselelerindeki görüşlerinden dolayı <b>tekfir</b> "
         "etmiştir. Filozofların zorunlu illiyet (determinizm) prensibini reddederek tabiattaki düzenin "
         "zorunlu değil, yalnızca Allah'ın iradesine bağlı bir <b>\"alışkanlık\"</b> olduğunu savunmuştur."],
    key_work="Tehâfütü'l-felâsife · İhyâ'ü 'ulûmi'd-dîn", initials="GZ",
)
RAZI = Person(
    id="razi", name="Fahreddin er-Râzî", years="ö. 606/1210",
    tagline="Felsefi Kelâm Sisteminin Esas Kurucusu",
    bio=["Felsefe ile kelâmın konularını birleştirerek felsefi kelâm sisteminin esas kurucusu olmuştur. "
         "İsbât-ı vâcibde hudûs delili yerine <b>\"ihkâm ve itkân\"</b> (gaye ve nizam) delilini merkeze almış; "
         "insan iradesi konusunda Mu'tezile'ye karşı çıkarak tamamen <b>determinist (cebrî)</b> bir çizgiye "
         "kaymış ve Allah'ın kelâmını <b>Lafzî</b> (hâdis) ile <b>Nefsî</b> (kadîm) olarak ikiye ayırmıştır."],
    key_work="Mefâtîhu'l-ğayb · el-Metâlibü'l-'âliye · Muhassal",
)
MATURIDI = Person(
    id="maturidi", name="Ebû Mansûr el-Mâtürîdî", years="ö. 333/944",
    tagline="Akıl-Nakil Sentezinin Kurucusu, Semerkand'ın İmamı",
    bio=["Dârü'l-Cüzcâniyye'de yetişip ders veren Mâtürîdî, Ebû Hanîfe'nin itikadî mirasını kelâmın rasyonel "
         "argümanlarıyla yeniden inşa etmiştir. Kelâm sistemini doğrudan bir <b>bilgi teorisiyle</b> (duyular, "
         "haber, istidlâl) başlatarak dönemine göre devrim niteliğinde bir adım atmış; Allah'ın varlığını "
         "bilmenin <b>vahiy gelmese bile aklen vacip</b> olduğunu ve <b>Tekvin</b>'in müstakil bir sıfat "
         "olduğunu savunmuştur."],
    key_work="Kitâbü't-Tevhîd · Te'vîlâtü'l-Kur'ân", initials="MT",
)
NESEFI = Person(
    id="nesefi", name="Ebü'l-Muîn en-Nesefî", years="ö. 508/1115",
    tagline="Mâtürîdîliği Müstakil Mezhep Hâline Getiren İsim",
    bio=["Mâtürîdîlik uzun süre yalnızca \"Hanefîliğin itikadî bir kolu\" gibi algılanmıştır. Ekolün fıkıh "
         "gölgesinden çıkarak Eş'arîlik gibi <b>müstakil bir kelâm mezhebi</b> hâlinde vücut bulmasını ve "
         "literatürde Mâtürîdiyye adıyla resmen tescillenmesini sağlayan asıl kırılma noktası, Nesefî'nin "
         "<b>Tebsıratü'l-edille</b> adlı eseriyle yaptığı devasa katkıdır."],
    key_work="Tebsıratü'l-edille",
)


def get_pack() -> CoursePack:
    # =====================================================================
    # BÖLÜM 1 — Mu'tezile: İsimlendirme, Doğuş ve Tarihsel Gelişim
    # =====================================================================
    ch1 = Chapter(
        number=1,
        title="Mu'tezile'nin Doğuşu ve Tarihsel Serüveni",
        subtitle="Bir mescit tartışmasından devletin resmî ideolojisine, oradan da tarih sahnesinden silinişe",
        key_terms=[
            KeyTerm("İ'tizâl", "Arapça 'a-z-l' kökünden; ayrılmak, uzaklaşmak, bir köşeye çekilmek. Ekolün adı bu kökten türemiştir."),
            KeyTerm("Mürtekib-i Kebîre", "Büyük günah işleyen kişi. Hâricî-Mürciî kutuplaşmasının ve Mu'tezile'nin doğuşunun merkezindeki tartışma konusu."),
            KeyTerm("Mihne", "Me'mûn'la başlayıp Mu'tasım ve Vâsık'la süren, ulemaya Halku'l-Kur'an tezinin devlet zoruyla dayatıldığı engizisyon dönemi."),
            KeyTerm("Halku'l-Kur'an", "Kur'an'ın kadîm değil mahlûk (sonradan yaratılmış) olduğu tezi; Mihne'nin sınav sorusu hâline gelmiştir."),
        ],
    )
    ch1.pages.append(
        ChapterPage()
        .add_terms(ch1.key_terms)
        .add_block(BulletBlock(1, "İsimlendirme ve Köken Bilgisi", [
            "<b>Siyasi Tarafsızlık (İlk Kullanım):</b> Hz. Ali ile Muâviye arasındaki savaşlarda taraf tutmayıp "
            "iç savaştan uzaklaşan <b>Sa'd b. Ebî Vakkâs</b> ve <b>Abdullah b. Ömer</b> gibi isimlere verilen "
            "siyasi bir sıfattı.",
            "<b>Meşhur \"Ayrılış\" Hadisesi:</b> Hasan-ı Basrî'nin mescidinde \"Büyük günah işleyenin dinî "
            "durumu nedir?\" sorusuna talebesi <b>Vâsıl b. Atâ</b> atılarak cevap verir: \"Ne tam mümindir ne "
            "kâfirdir; o kişi <b>fâsık</b>tır.\" Ardından meclisten ayrılıp bir köşeye geçince Katâde b. Diâme "
            "\"Bunlar bizden i'tizâl etti\" demiş ve ekol bu ismi almıştır.",
            "<b>Ekolün İsmi Sahiplenmesi:</b> Mu'tezile âlimleri bu ismi sonradan gururla taşımıştır. "
            "<b>Kâdî Abdülcebbâr</b> Fazlü'l-İ'tizâl'de bunu meşrulaştırmış; <b>İbnü'l-Murtazâ</b> ismin "
            "\"şirkten ve küfürden ayrılmak\" anlamına geldiğini ve Meryem 19/48 âyetiyle bağdaştığını "
            "savunmuştur.",
        ]))
        .add_person(VASIL)
    )
    ch1.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Mu'tezile'ye Verilen Diğer İsimler ve Sebepleri",
            ["Verilen İsim", "İsimlendirme Sebebi ve Arka Planı"],
            [
                ["Ehlü'l-Adl ve't-Tevhîd", "Kendi verdikleri isimdir: sıfatları zâttan ayırmamaları (Tevhid) ve insanın hür iradesini savunmaları (Adalet)."],
                ["Kaderiyye", "Ehl-i Sünnet'in verdiği yerme lakabı; insanın eylemini kendi kudretiyle yarattığını söylemeleri sebep olmuştur."],
                ["Seneviyye — Mecûsîler", "\"Hayrın fâili Allah, şerrin fâili insandır\" dedikleri için düalist inançlara benzetilmişlerdir."],
                ["Cehmiyye", "Sıfatların kadîmliğini reddetmeleri, rü'yetullahı inkârları ve Halku'l-Kur'an tezinde Cehmiyye ile aynı düşünmeleri."],
                ["Vaîdiyye — Havâric", "Tövbesiz ölen büyük günah sahibinin cehennemde ebedî kalacağını savundukları için Hâricîlerle eş tutulmuşlardır."],
            ]
        ))
        .add_block(BulletBlock(2, "İç Faktörler: Siyasi Krizlerin Teolojiye Dönüşümü", [
            "Hz. Osman'ın şehâdeti, ardından <b>Cemel</b> ve <b>Sıffîn</b> savaşları, \"Müslüman kanı "
            "dökenlerin durumu ne olacak?\" sorusunu ve <b>büyük günah (kebîre)</b> tartışmasını doğurmuştur.",
            "<b>Hâricîler</b> günah işleyeni kâfir sayarken, <b>Mürcie</b> eylemi önemsizleştirip \"mümin\" "
            "sayıyordu. Vâsıl b. Atâ ise toplumsal barışı sağlamak için ikisinin ortası olan <b>fâsık</b> "
            "nitelemesini icat etmiştir.",
            "<b>Cebriyye'ye İsyan:</b> Emevîler zulümlerini \"Bu Allah'ın kaderidir\" diyerek Cebriyye "
            "felsefesiyle meşrulaştırmaya çalıştı. Buna ilk karşı çıkanlar <b>Ma'bed el-Cühenî</b> ve "
            "<b>Gaylân ed-Dımaşkî</b>; bayrağı devralan Vâsıl b. Atâ ise Adalet ilkesinin temelini atmıştır.",
        ]))
        .add_block(BulletBlock(3, "Dış Faktörler: Felsefe ve Diğer Dinlerle Temas", [
            "Yeni fethedilen topraklarda Hristiyan ve Yahudi <b>antropomorfizmine</b> (teşbih-tecsim) karşı "
            "İslâm inancını <b>Tenzih</b> prensibiyle koruma gayreti.",
            "İran ve Hint kökenli <b>Maniheizm, Mecûsîlik ve Sümeniyye</b> gibi düalist dinlerle entelektüel "
            "savaş; Vâsıl bu inançları çürütmek için özel davetçi grupları kurmuştur.",
            "<b>Aristo felsefesi ve Yunan mantığının</b> tercüme hareketleriyle İslâm dünyasına girmesi; "
            "kelâmcılar gnostik ve bâtıl inançlarla savaşmak için bu denetlenebilir rasyonel metodu "
            "kullanmışlardır.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("Siyasi Kriz", "Hz. Osman'ın şehâdeti, Cemel ve Sıffîn"),
            FlowStep("Teolojik Soru", "Büyük günah işleyenin statüsü nedir?"),
            FlowStep("Üç Farklı Cevap", "Hâricî: kâfir · Mürciî: mümin · Vâsıl: fâsık"),
            FlowStep("Ekolleşme", "İ'tizâl hadisesi ve Mu'tezile'nin doğuşu"),
        ], caption="Siyasi Krizden Teolojik Ekole: Mu'tezile'nin Doğuş Zinciri"))
    )
    ch1.pages.append(
        ChapterPage()
        .add_block(BulletBlock(4, "Altın Çağ, Mihne ve Çöküş", [
            "Mu'tezile Vâsıl b. Atâ ile doğsa da ekolün asıl <b>sistematik kurucusu Ebü'l-Hüzeyl el-Allâf</b>'tır; "
            "beş temel esası (Usûl-i Hamse) bir sistem hâline getiren odur.",
            "Emevîlerin son dönemlerinde kısmen devlet kademelerine giren ekol, gerçek <b>Altın Çağı</b>'nı "
            "Abbâsî halifesi <b>Me'mûn</b> döneminde yaşamış ve akım devletin <b>resmî ideolojisi</b> hâline "
            "gelmiştir.",
            "<b>Çöküş:</b> Halife <b>Mütevekkil</b> başa gelince Mihne'ye son vermiş, Mu'tezile'yi bürokrasiden "
            "temizlemiş ve <b>Karşı-Mihne</b>'yi başlatmıştır.",
            "Büveyhîler zamanında Vezir <b>Sâhib b. Abbâd</b> eliyle kısa bir canlanma yaşansa da; Büyük "
            "Selçuklu'da <b>Alparslan</b> ve veziri <b>Nizâmülmülk</b>'ün Nizâmiyye medreselerini devlet "
            "politikası yapmasıyla Mu'tezile Horasan'dan sürülmüş ve yalnızca Yemen'deki <b>Zeydiyye</b> "
            "içinde erimiştir.",
        ]))
        .add_callout(Callout("caution", "Dikkat / Püf Noktası: Mihne Olayı",
            "İslâm tarihinde engizisyon benzeri bir baskı dönemi olan <b>Mihne</b>, Me'mûn döneminde başlamış, "
            "Mu'tasım ve Vâsık dönemlerinde devam etmiştir. Baş kadı <b>Ahmed b. Ebî Duâd</b>'ın teşvikiyle "
            "devletin askerî ve siyasi gücü kullanılarak bütün ulemaya <b>Halku'l-Kur'an</b> tezi "
            "dayatılmıştır. Bunu reddeden Ehl-i Hadis âlimleri (özellikle <b>Ahmed b. Hanbel</b>) "
            "kırbaçlanmış, zindana atılmış veya sürgüne gönderilmiştir. Mihne, rasyonalist geçinen bir ekolün "
            "siyasi güç bulunca ne kadar otoriterleşebileceğini göstermiş ve halkın nefretini çekerek ekolün "
            "sonunu hazırlamıştır."))
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "Mu'tezile başlangıçta İslâm akîdesini iç (Cebriyye) ve dış (Mecûsîlik, Hristiyanlık) fikrî "
            "saldırılara karşı üstün bir rasyonaliteyle savunan, son derece faydalı bir aydınlanma "
            "hareketiydi. Ancak siyasi iktidarı ve devlet mekanizmasını eline geçirince felsefi tartışmayı "
            "<b>\"devlet terörüne\"</b> (Mihne) dönüştürdü. Bu tahammülsüzlük, sosyolojik ve ilmî bir "
            "intihara neden oldu."))
        .add_summary("Mu'tezile, Hasan-ı Basrî'nin ders halkasında büyük günah tartışmasıyla başlayan bir "
            "\"ayrılış\" hikâyesinden doğmuş; iç faktör olarak Cemel-Sıffîn krizinin ürettiği kebîre "
            "tartışmasından ve Emevî Cebriyyeciliğine isyandan, dış faktör olarak da düalist dinler ve Yunan "
            "mantığıyla temastan beslenmiştir. Ebü'l-Hüzeyl el-Allâf'ın sistemleştirmesiyle olgunlaşan ekol, "
            "Me'mûn döneminde devletin resmî ideolojisi olmuş; ancak Mihne'de kendi rasyonalizmini devlet "
            "zorbalığına çevirince Mütevekkil'in Karşı-Mihne'siyle tasfiye edilmiş ve Selçuklu-Nizâmiyye "
            "politikasıyla tarih sahnesinden silinerek yalnızca Zeydiyye içinde varlığını sürdürmüştür.")
    )

    # =====================================================================
    # BÖLÜM 2 — Basra ve Bağdat Ekolleri
    # =====================================================================
    ch2 = Chapter(
        number=2,
        title="Basra ve Bağdat Ekolleri ve Temsilcileri",
        subtitle="Aynı beş esas, 155 farklı görüş: teorik akademisyenlerle saray kelâmcılarının ayrışması",
        key_terms=[
            KeyTerm("Basriyyûn", "Ebü'l-Hüzeyl el-Allâf'ın kurduğu, iktidardan uzak durup ilme odaklanan teorik Mu'tezile kanadı."),
            KeyTerm("Bağdâdiyyûn", "Bişr b. Mu'temir'in kurduğu, Abbâsî sarayıyla iç içe geçmiş, siyaset-teoloji eksenli kanat."),
            KeyTerm("Tevellüd", "İnsanın kendi kudretiyle başka bir şey üzerinde etki oluşturması (birine vurup kör etmesi gibi) — bağımlı fiiller teorisi."),
            KeyTerm("Ahvâl Teorisi", "Ebû Hâşim el-Cübbâî'nin sıfat problemini çözmek için ürettiği, ne var ne yok olan 'hâller' nazariyesi."),
        ],
    )
    ch2.pages.append(
        ChapterPage()
        .add_terms(ch2.key_terms)
        .add_block(BulletBlock(1, "Ayrışmanın Coğrafyası ve Ölçeği", [
            "Ekol Vâsıl b. Atâ ile <b>Basra</b>'da doğmuş olsa da, Abbâsîler döneminde düşünsel ve siyasi "
            "farklılıklar sebebiyle <b>Basra (Basriyyûn)</b> ve <b>Bağdat (Bağdâdiyyûn)</b> olmak üzere iki ana "
            "ekole ayrılmıştır.",
            "Basra ekolünün sistematik kurucusu <b>Ebü'l-Hüzeyl el-Allâf</b>, bu fikirleri Bağdat'a taşıyıp "
            "orada yeni bir merkez inşa eden ise <b>Bişr b. Mu'temir</b>'dir.",
            "İki ekol, temel prensip olan <b>beş esas (Usûl-i Hamse)</b> üzerinde ittifak etseler de; özellikle "
            "kozmoloji (dakîk) ve siyasî meselelerde derin ayrılıklar yaşamışlardır.",
            "<b>Ebû Reşîd en-Nîsâbûrî</b>'nin <b>el-Mesâ'il fi'l-hilâf beyne'l-Basriyyîn ve'l-Bağdâdiyyîn</b> "
            "adlı eserinde iki ekol arasında tam <b>155 farklı görüş ayrılığı</b> tespit edilmiştir.",
        ]))
        .add_table(ComparisonTable(
            "Basra ve Bağdat Ekolleri Arasındaki Temel Farklar",
            ["Ölçüt", "Basra Ekolü (Basriyyûn)", "Bağdat Ekolü (Bağdâdiyyûn)"],
            [
                ["Kurucu İsim", "Ebü'l-Hüzeyl el-Allâf", "Bişr b. el-Mu'temir"],
                ["Siyasete Yaklaşım", "İktidar ilişkilerinden ve siyasi tartışmalardan uzak, ilme odaklı.", "Siyasetle iç içe, devlet kademelerinde aktif."],
                ["İmâmetin Mahiyeti", "İmâmeti Allah'ın bir <b>lutuf</b>u (ikramı) olarak görür.", "İmam tayin etmeyi <b>aslah</b> (kullar için en faydalı olan) kapsamında zorunlu görür."],
                ["Sahâbenin Fazileti", "Üstünlük kronolojik hilafet sırasına göredir (Ebûbekir → Ömer → Osman).", "Ümmetin en faziletlisi, Hz. Peygamber'den sonra doğrudan <b>Hz. Ali</b>'dir."],
            ]
        ))
    )
    ch2.pages.append(
        ChapterPage()
        .add_person(ALLAF)
        .add_block(BulletBlock(2, "Basra Ekolü: İlk Kuşak", [
            "<b>Vâsıl b. Atâ (ö. 131/748):</b> <b>el-menzile beyne'l-menzileteyn</b> ilkesinin kurucusudur. "
            "Cemel ve Sıffîn'e katılanlardan bir grubun kesinlikle hatalı olduğunu ama hangisi olduğunu "
            "bilemeyeceğimiz için her iki tarafın da fâsık sayılacağını, bu sebeple şahitliklerinin kabul "
            "edilmeyeceğini savunmuştur.",
            "<b>Amr b. Ubeyd (ö. 144/761):</b> İkinci kurucu isimdir; Vâsıl'dan farklı olarak Cemel'e katılan "
            "<b>her iki grubun da toptan fâsık</b> olduğunu ve cehennemde ebedî kalacaklarını iddia etmiştir.",
            "<b>Ebü'l-Hüzeyl el-Allâf (ö. 235/849):</b> Usûl-i Hamse'nin mimarıdır. <b>Atomcu felsefeyi</b> "
            "(cüz lâ yetecezzâ) İslâm'a uyarlamış; <b>ecel</b>in kesin bir vakit olduğunu, maktûlün "
            "öldürülmeseydi de yine tam o saatte öleceğini savunmuştur.",
        ]))
        .add_person(NAZZAM)
        .add_block(BulletBlock(3, "Nazzâm'ın Dört Meşhur Teorisi", [
            "<b>Zulüm İmkânsızlığı:</b> Allah kullarına yalnızca \"iyilik\" yaratabilir; kötülük yaratmaya "
            "gücü yetmez, çünkü kötülük yaratmak zulüm anlamına gelir ve Allah bundan münezzehtir.",
            "<b>Tafra (Sıçrama):</b> Bir cismin bulunduğu yerden başka bir yere, aradaki mekânlara uğramadan "
            "\"sıçrayarak\" geçebilmesi.",
            "<b>Kümûn-Zuhûr (Gizlenme ve Ortaya Çıkma):</b> Allah bütün varlıkları tek seferde yaratmış ancak "
            "bir kısmını gizlemiştir (kümûn); varlıkların zamanla ortaya çıkması yeni bir yaratılış değil, "
            "gizlendikleri yerden belirmeleridir (zuhûr).",
            "<b>Sarfe Nazariyesi (Engelleme):</b> Kur'an'ın benzerinin getirilememesinin sebebi lafzî "
            "üstünlüğü değil; Allah'ın Arapların buna güç yetirme kabiliyetini ellerinden alarak onları "
            "<b>âciz bırakmasıdır</b> (sarfe).",
        ]))
        .add_block(BulletBlock(4, "Basra Ekolü: Sonraki Kuşak", [
            "<b>Câhiz (ö. 255/869):</b> Cehennemliklerin azabının sonsuz olmayacağını, belli bir süre sonra "
            "ateşin tabiatına uygun hâle gelerek acı hissetmeyeceklerini savunmuştur.",
            "<b>Ebû Ali el-Cübbâî (ö. 303/916):</b> <b>Eş'arî'nin hocası</b> ve üvey babasıdır; dinî "
            "emirlerin/hükümlerin tamamının Allah'ın insana lütfu olduğunu savunur.",
            "<b>Ebû Hâşim el-Cübbâî (ö. 321/933):</b> Babasının yolunu sürdüren, çok zeki ve sorgulayıcı bir "
            "kelâmcıdır; sıfat problemini çözmek için <b>Ahvâl</b> teorisini kurmuştur.",
            "<b>Kâdî Abdülcebbâr (ö. 415/1025):</b> Büveyhî veziri Sâhib b. Abbâd tarafından başkadı yapılan, "
            "Mu'tezile'nin <b>son büyük ansiklopedisti</b>dir.",
        ]))
    )
    ch2.pages.append(
        ChapterPage()
        .add_callout(Callout("caution", "Dikkat / Püf Noktası: Ahvâl Teorisi",
            "Ebû Hâşim, Allah'ın sıfatlarını açıklamak için <b>\"Ahvâl\" (Hâller)</b> teorisini kurmuştur. Bu "
            "teoriye göre Allah'ın sıfatları (ilim, kudret vb.) Allah'ın zâtının ötesinde hususi birer "
            "\"hâl\"dir. Bu hâller ne tam olarak vardır (mevcûd) ne de tam olarak yoktur (ma'dûm); kadîm de "
            "değillerdir, hâdis de değillerdir. Çünkü onlara kadîm dersek <b>\"birden çok kadîmin varlığı\" "
            "(teaddüd-i kudemâ)</b> problemi doğar ve Tevhid bozulur."))
        .add_person(ABDULCEBBAR)
        .add_person(BISR)
        .add_block(BulletBlock(5, "Bağdat Ekolünün Önemli Temsilcileri", [
            "<b>Sümâme b. Eşres (ö. 213/828):</b> Halife Me'mûn'un hocasıdır, vezirlik teklifini reddetmiştir. "
            "<b>Mütevellid</b> (dolaylı doğan) fiillerin fâili olmadığını savunur; çünkü sebebi oluşturan kişi "
            "ölse bile fiil sonuç doğurmaya devam edebilir. Zındıkların, Mecûsîlerin ve Hristiyanların âhirette "
            "azap görmeyip <b>hayvanlar gibi toprağa dönüşeceğini</b> iddia etmiştir.",
            "<b>Ebû Mûsâ el-Murdâr (ö. 226/841):</b> Zühd hayatı sebebiyle <b>\"Mu'tezile'nin rahibi\"</b> "
            "unvanını almıştır. Allah'ın yalan söylemeye ve zulmetmeye <b>gücünün yettiğini</b> (yaparsa zalim "
            "olacağını) iddia ederek diğerlerinden ayrılır; Nazzâm'ın aksine insanların Kur'an'ın benzerini "
            "getirmeye güç yetirebileceğini savunmuş, sultanla senli benli olan herkesi tekfir etmiştir.",
            "<b>Ebü'l-Hüseyin el-Hayyât (ö. 300/913):</b> İtikadî meselelerde \"zan\" ifade ettiği için "
            "<b>âhâd hadislerin</b> delil olmasını reddeder; <b>ma'dûm</b>u (yokluğu) sadece şey veya cevher "
            "değil bir <b>cisim</b> olarak kabul eder. Eseri <b>Kitâbü'l-İntisâr</b>, mülhid İbnü'r-Râvendî'ye "
            "yazılan meşhur reddiyedir ve günümüze ulaşmıştır.",
            "<b>Ebü'l-Kâsım el-Belhî el-Ka'bî (ö. 319/931):</b> Allah'ın <b>iradesini</b> bağımsız bir vasıf "
            "değil, fiillerini kendi <b>ilmi</b> gereğince yaratması olarak izah eder.",
        ]))
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "Mu'tezile'nin Basra kanadı meselelere soyut bir <b>teorik kelâmcı ve akademisyen</b> gözüyle "
            "bakarken; Bağdat kanadı, devlet merkezinde bulunmanın getirdiği pratiklikle meseleleri "
            "<b>siyaset-teoloji ekseninde</b> ele almıştır. Nazzâm'ın metafizik sıçramaları (Tafra), Ebû "
            "Hâşim'in sıfatları ontolojik krizden kurtarma çabası (Ahvâl) ve Bişr'in fiziksel nedenselliği "
            "açıklayan teorisi (Tevellüd) ile bu iki kanat birlikte İslâm'ın <b>ilk rasyonel bilim felsefesini "
            "ve fizik kozmolojisini</b> inşa etmişlerdir."))
    )
    ch2.pages.append(
        ChapterPage()
        .add_summary("Basra'da doğan Mu'tezile, Abbâsîler döneminde Ebü'l-Hüzeyl el-Allâf'ın teorik Basra "
            "kanadı ile Bişr b. Mu'temir'in saray merkezli Bağdat kanadına ayrılmış; beş esasta ittifak "
            "etmelerine rağmen kozmoloji, imâmet ve sahâbe fazileti gibi konularda 155 ayrı görüş ayrılığı "
            "üretmişlerdir. Vâsıl ve Amr'ın fâsık tartışması, Allâf'ın atomculuğu, Nazzâm'ın tafra-kümûn-sarfe "
            "üçlüsü, Ebû Hâşim'in Ahvâl'i ve Kâdî Abdülcebbâr'ın ansiklopedik derlemesi Basra'nın; Bişr'in "
            "tevellüdü, Sümâme'nin mütevellid fiilleri ve Hayyât'ın âhâd hadis reddi ise Bağdat'ın kalıcı "
            "mirasıdır.")
    )

    # =====================================================================
    # BÖLÜM 3 — Usûl-i Hamse
    # =====================================================================
    ch3 = Chapter(
        number=3,
        title="Mu'tezile'nin Beş Temel İlkesi (Usûl-i Hamse)",
        subtitle="Tevhîd, Adâlet, el-Va'd ve'l-Vaîd, el-Menzile beyne'l-Menzileteyn ve Emir bi'l-Ma'rûf",
        key_terms=[
            KeyTerm("Teaddüd-i Kudemâ", "Birden fazla kadîm varlığın kabulü; Mu'tezile'ye göre zâttan ayrı kadîm sıfat kabul etmenin doğurduğu şirk problemi."),
            KeyTerm("Aslah", "Allah'ın kulları için daima 'en iyi ve en faydalı olanı' yaratmak zorunda oluşu; Adâlet ilkesinin uzantısı."),
            KeyTerm("Hüsün ve Kubuh", "İyilik ve kötülüğün fiilin bizzat zâtında bulunması ve aklın bunu vahiy gelmeden bulabilmesi."),
            KeyTerm("Rü'yetullah", "Allah'ın âhirette gözle görülmesi; Mu'tezile bunu yön ve mekân gerektirdiği için aklen imkânsız sayar."),
        ],
    )
    ch3.pages.append(
        ChapterPage()
        .add_terms(ch3.key_terms)
        .add_block(BulletBlock(1, "Tevhîd: Allah'ın Birlik ve Tekliği", [
            "<b>Sıfatlar Meselesi:</b> Mu'tezile, Allah'ın zâtından ayrı ezelî (kadîm) sıfatların varlığını "
            "kesinlikle reddeder; kabul edilirse <b>teaddüd-i kudemâ</b> doğar ve Tevhid bozulur. Onlara göre "
            "Allah, zâtından ayrı bir ilimle değil <b>bizzat kendi zâtıyla âlimdir</b>. \"Kadîm bir sıfat veya "
            "mânanın kabulü, iki ilâh kabul etmek anlamına gelir.\"",
            "<b>Halku'l-Kur'an:</b> Tevhid'in doğal sonucu olarak Allah'ın kelâmı kadîm değil <b>mahlûktur</b>; "
            "çünkü kelâm harf ve seslerden oluşur, fiilî bir sıfat olduğu için hâdistir.",
            "<b>Teşbih ve Tecsîm'in Reddi:</b> Allah'ı bir varlığa benzeten (teşbih) ve O'na cisim atfeden "
            "(tecsîm) tüm inançlar <b>şirk</b> sayılarak reddedilmiştir.",
            "<b>Rü'yetullah'ın İmkânsızlığı:</b> Görme eylemi, görülecek nesnenin bir yön ve mekânda olmasını "
            "gerektirir; Allah mekândan ve cisimlikten münezzeh olduğu için âhirette gözle görülmesi "
            "<b>aklen imkânsızdır</b>.",
        ]))
        .add_callout(Callout("insight", "Kritik Çıkarım: Tevhid'in Sınırı",
            "Mu'tezile'nin Tevhid ilkesi, Allah'ı öylesine mutlak ve soyut bir birliğe taşır ki; O'na zâtından "
            "ayrı bir sıfat, fiziksel bir kelâm veya gözle görülebilir bir form atfetmek doğrudan <b>şirk</b> "
            "(ikinci bir Tanrı icat etmek) kabul edilir."))
        .add_block(BulletBlock(2, "Adâlet: İlâhî Adalet ve İnsan Hürriyeti", [
            "<b>İnsan Fiilleri ve Hür İrade:</b> İnsan, kendi fiillerinin <b>yaratıcısı ve fâilidir</b>; "
            "aklıyla düşünür, hür iradesiyle seçtiği eylemi kendi kudretiyle meydana getirir ve bu yüzden "
            "sorumludur. Allah yalnızca iyi fiiller üzerinde irade sahibidir, kötülükleri O yaratmaz.",
            "<b>Teklif-i mâ lâ yutak'ın Reddi:</b> Allah, insanın gücünün yetmeyeceği bir şeyi ona yüklemez; "
            "bunu yapmak ilâhî adalete sığmaz.",
            "<b>Salâh ve Aslah Teorisi:</b> Allah kulları için daima <b>en iyi ve en faydalı olanı</b> "
            "yaratmak zorundadır. Allah Hakîm'dir ve kendi çıkarı olamayacağına göre fiilleri kullarının "
            "menfaatine olmak zorundadır.",
            "<b>Hüsün ve Kubuh:</b> Eylemlerin iyi (hasen) veya kötü (kabîh) olması ilâhî bir emirle sonradan "
            "belirlenmez; iyilik/kötülük fiilin <b>bizzat zâtındadır</b> ve akıl bunu vahiy gelmeden de "
            "bulabilir.",
        ]))
    )
    ch3.pages.append(
        ChapterPage()
        .add_block(BulletBlock(3, "el-Va'd ve'l-Vaîd: Söz ve Tehdit", [
            "Allah'ın iyilik yapanları ödüllendireceğine dair sözüne <b>Va'd</b>, kötülük yapanları "
            "cezalandıracağına dair tehdidine ise <b>Vaîd</b> denir.",
            "Büyük günah işleyip <b>tövbe etmeden ölen</b> kimse kesinlikle cehennemde ebedî kalacaktır; ancak "
            "azabı kâfirlerinkinden daha hafif olacaktır.",
            "Mizan <b>adalet</b>, sırat ise <b>doğru yol</b> olarak rasyonel biçimde te'vil edilir.",
        ]))
        .add_callout(Callout("caution", "Dikkat / Püf Noktası: Şefaatin Reddi",
            "Ekolün en sarsıcı görüşlerinden biri şefaat meselesindedir. Mu'tezile'ye göre Allah'ın "
            "tehdidinden (vaîd) dönmesi <b>adaletsizliktir</b>. Bu sebeple büyük günahkârların cehennemden "
            "çıkarılması anlamındaki <b>şefaat inancını tamamen reddederler</b>; şefaati yalnızca "
            "\"cennettekilerin makamlarının yükseltilmesi\" olarak kabul ederler. <b>Âhâd hadislerin</b> "
            "itikatta delil olamayacağını savunarak şefaat hadislerini dikkate almazlar."))
        .add_block(BulletBlock(4, "el-Menzile beyne'l-Menzileteyn: İki Konum Arasındaki Konum", [
            "Vâsıl b. Atâ tarafından formüle edilen bu ilke, büyük günah işleyen (<b>mürtekib-i kebîre</b>) "
            "kişinin dinî statüsünü belirler.",
            "Bu kişi ne tam mümindir ne de tam kâfirdir; ikisi arasında bir yerdedir ve <b>fâsık</b> olarak "
            "adlandırılır.",
            "Ölmeden önce <b>tövbe ederse mümin</b> olarak ölür; tövbe etmezse kâfir hükmüyle cehennemde ebedî "
            "kalır.",
        ]))
        .add_table(ComparisonTable(
            "Büyük Günah İşleyenin (Mürtekib-i Kebîre) Durumu: Mezheplere Göre",
            ["Mezhep / Âlim", "Savunduğu Statü"],
            [
                ["Hâricîler", "<b>Kâfir</b> — dinden çıkar, ebedî cehennemliktir."],
                ["Mürcie", "<b>Mümin</b> — amel imandan parça değildir, imanı zarar görmez."],
                ["Hasan-ı Basrî", "<b>Münafık</b> — küfrü gizlediği için."],
                ["Mu'tezile (Vâsıl b. Atâ)", "<b>Fâsık</b> — el-menzile beyne'l-menzileteyn: iman ile küfür arasında."],
            ]
        ))
        .add_block(BulletBlock(5, "Emir bi'l-Ma'rûf Nehiy ani'l-Münker", [
            "Aklın iyi gördüğünü emretmek, kötü gördüğünü engellemek Kur'an'ın nassıyla <b>tüm ümmete "
            "vaciptir</b>.",
            "Ancak Mu'tezile bu ahlâkî ilkeyi zamanla çok sert bir <b>siyasi ideolojiye</b> dönüştürmüştür: "
            "iktidara muhalifken \"zalim sultana başkaldırı\" aracı olarak kullanmışlar; iktidarı (Abbâsî/Mihne "
            "dönemi) ele geçirdiklerinde ise muhalifleri sorgulamak için bir <b>devlet terörü aparatı</b> "
            "olarak işletmişlerdir.",
        ]))
        .add_callout(Callout("insight", "Kritik Çıkarım: Fâsık Formülünün Sosyolojisi",
            "Vâsıl b. Atâ'nın <b>fâsık</b> formülü, Hâricîlerin sebep olduğu toplumsal terörü (insanların "
            "kanını ve malını helâl saymayı) durdurmak; aynı zamanda Mürcie'nin ameli önemsizleştiren ahlâkî "
            "gevşekliğine mâni olmak için üretilmiş çok zekice bir <b>\"sosyolojik denge\"</b> stratejisidir."))
    )
    ch3.pages.append(
        ChapterPage()
        .add_block(BulletBlock(6, "Günümüze Ulaşan Mu'tezile Literatürü", [
            "Mu'tezile eserlerinin çoğu Büyük Selçuklu ve sonrası sürgün/yıkımlar sebebiyle kaybolmuştur; "
            "elimizdeki klasikler <b>Yemen kütüphanelerinde</b> sonradan keşfedilmiştir.",
            "<b>Kâdî Abdülcebbâr:</b> <b>el-Muğnî fî ebvâbi't-tevhîd ve'l-'adl</b> (mezhebin en hacimli "
            "şaheseri; 20 cüzden 16'sı elimizde), <b>Şerhu'l-Usûli'l-Hamse</b> (beş esasın temel kitabı), "
            "<b>Muhtasar fî usûli'd-dîn</b> (el-Muğnî'nin özeti) ve <b>Fazlü'l-İ'tizâl ve Tabakâtu'l-Mu'tezile</b>.",
            "<b>Câhiz:</b> <b>Kitâbü'l-Hayevân</b> (7 ciltlik zooloji-sosyoloji-felsefe şaheseri) ve "
            "<b>el-Beyân ve't-Tebyîn</b> (Arap edebiyatı ve hitabetinde ilk büyük eserlerden).",
            "<b>Diğerleri:</b> İbnü'l-Murtazâ'nın <b>Tabakâtu'l-Mu'tezile</b>'si (âlimleri 12 tabaka hâlinde "
            "anlatır), Ebû Reşîd en-Nîsâbûrî'nin <b>el-Mesâ'il fi'l-hilâf</b>'ı, Hayyât'ın "
            "<b>Kitâbü'l-İntisâr</b>'ı ve İbn Metteveyh'e nispet edilen <b>el-Mecmû' fi'l-Muhît bi't-Teklîf</b> "
            "ile <b>et-Tezkire fî ahkâmi'l-cevâhir ve'l-a'râz</b>.",
        ]))
        .add_person(CAHIZ)
        .add_summary("Mu'tezilî olmanın şartı, Usûl-i Hamse'yi kabul etmektir. Tevhid ilkesi zâttan ayrı "
            "kadîm sıfatları, Halku'l-Kur'an'ı ve rü'yetullahı belirlerken; Adâlet ilkesi insanı kendi "
            "fiillerinin yaratıcısı yapar, aslahı Allah'a zorunlu kılar ve hüsün-kubhu fiilin zâtına "
            "yerleştirir. el-Va'd ve'l-Vaîd tövbesiz büyük günahkârın ebedî cehennemini ve şefaatin reddini "
            "getirir; el-Menzile beyne'l-menzileteyn Hâricî-Mürciî kutuplaşmasına karşı fâsık formülünü "
            "üretir; Emir bi'l-ma'rûf ise başlangıçta ahlâkî bir ilkeyken Mihne'de devlet terörüne dönüşür.")
    )

    # =====================================================================
    # BÖLÜM 4 — Eş'arîliğin Arka Planı ve Eş'arî'nin Dönüşümü
    # =====================================================================
    ch4 = Chapter(
        number=4,
        title="Eş'arîliğin Arka Planı ve Eş'arî'nin Dönüşümü",
        subtitle="İki mihne arasında bir 'orta yol' arayışı: kırk yaşında değişen bir imamın hikâyesi",
        key_terms=[
            KeyTerm("Ta'rîb", "Abdülmelik b. Mervân'ın Arapçalaştırma politikası; Arap kökenli olmayan Müslümanlar (Mevâlî) üzerinde baskı kurmuştur."),
            KeyTerm("Karşı-Mihne", "Mütevekkil'le başlayan, Ehl-i Hadis'in devlet destekli olarak Mu'tezile'yi tasfiye ettiği dönem."),
            KeyTerm("Kesb", "Fiili Allah'ın yarattığı, kulun ise iradesiyle seçip kazandığı formül; Eş'arî'nin insan hürriyeti çözümü."),
            KeyTerm("Vücûb alellah", "Allah'a bir şeyin vacip olması nazariyesi; Mu'tezile savunur, Eş'arî reddeder."),
        ],
    )
    ch4.pages.append(
        ChapterPage()
        .add_terms(ch4.key_terms)
        .add_flow(FlowDiagram([
            FlowStep("Emevî Saltanatı", "Ta'rîb politikası ve Mevâlî baskısı"),
            FlowStep("Abbâsî İhtilali", "Mevâlî desteğiyle iktidar değişimi"),
            FlowStep("Emin — Me'mûn", "Arap ve Mevâlî kanatların taht kavgası"),
            FlowStep("Mihne", "Me'mûn'un zaferi ve devlet terörü"),
            FlowStep("Karşı-Mihne", "Mütevekkil ve Ehl-i Hadis'in intikamı"),
        ], caption="Hilafet Tartışmalarının Evrimi: Eş'arîliği Doğuran Siyasi İklim"))
        .add_block(BulletBlock(1, "Siyasi Arka Plan: İktidar Mücadelelerinin Teolojiye Yansıması", [
            "<b>Hilafetin Dönüşümü:</b> Hz. Ebûbekir'in hilafetin Kureyş'te kalması ısrarı dinî değil, dönemin "
            "Arap sosyolojisinde birliği sağlama amacı taşıyan <b>siyasi ve stratejik</b> bir refleksti. "
            "Emevîlerle birlikte hilafet babadan oğula geçen bir saltanata dönüşmüş, <b>Abdülmelik b. "
            "Mervân</b>'ın Ta'rîb politikasıyla Mevâlî üzerinde baskı kurulmuştur.",
            "<b>Abbâsîler ve Mihne:</b> Bu baskıya tepki olarak Abbâsîler, Ehl-i Beyt'in mağduriyetini ve "
            "Mevâlî'nin gücünü kullanarak iktidara gelmiştir. Hârun er-Reşîd'in Arap destekli oğlu <b>Emin</b> "
            "ile Mevâlî destekli oğlu <b>Me'mûn</b> arasındaki taht kavgasını Me'mûn kazanmış, onun Mu'tezile'ye "
            "yakınlığı devlet destekli bir engizisyona dönüşmüştür.",
            "<b>Büveyhîler ve Eş'arî'nin Dönemi:</b> Mihne'den sonra Mütevekkil ile Karşı-Mihne başlamış; siyasi "
            "otoritenin zayıflayıp Bağdat'ın Şiî <b>Büveyhîler</b> tarafından işgal edildiği bu kaotik dönemde "
            "Ebü'l-Hasan el-Eş'arî yaşamış ve eserlerini kaleme almıştır.",
        ]))
        .add_callout(Callout("insight", "Kritik Çıkarım: Neden 'Orta Yol'?",
            "Eş'arîlik; iktidar gücünü arkasına alıp muhaliflerine kan kusturan <b>Mu'tezile (Mihne)</b> ile "
            "aynı gücü ele geçirip rasyonel düşünceyi tamamen boğmaya çalışan <b>Ehl-i Hadis'in "
            "(Karşı-Mihne)</b> yol açtığı yorucu kutuplaşmanın ardından, ümmetin <b>\"merkez (vasat)\"</b> "
            "arayışının sosyolojik bir sonucudur."))
    )
    ch4.pages.append(
        ChapterPage()
        .add_block(BulletBlock(2, "İlmî ve Fikrî Arka Plan", [
            "Hicrî I. yüzyılın sonlarından itibaren İslâm toplumu, ana gövdeyi temsil eden <b>Ehl-i Sünnet</b> "
            "ve aşırılıkları temsil eden <b>Ehl-i bid'at</b> olarak ayrışmaya başlamıştır.",
            "Ehl-i Sünnet akaidinin ilk temelleri, Emevî halifesi Abdülmelik b. Mervân'a <b>Kader Risâlesi</b>'ni "
            "yazan ve siyasi çatışmalardan uzak duran <b>Hasan-ı Basrî</b> tarafından atılmıştır.",
            "Eş'arîlik öncesi Ehl-i Sünnet uleması, metodoloji açısından <b>iki ana damara</b> bölünmüştü.",
        ]))
        .add_table(ComparisonTable(
            "Eş'arîlik Öncesi Ehl-i Sünnet'te İki Ana Damar",
            ["Damar", "Temsilcileri", "Yöntem ve Özellikleri"],
            [
                ["Selefiyye / Muhafazakâr Damar (Ehl-i Hadis)", "İmam Mâlik, İmam Şâfiî, Ahmed b. Hanbel",
                 "İtikadî konularda nasların <b>zâhirini</b> esas alır; aklî çıkarımlara (kelâm metoduna) mesafelidir."],
                ["İlk Kelâmcılar (Erken Dönem Sünnî Kelâmı)", "Ebû Hanîfe, İbn Küllâb el-Basrî, Hâris el-Muhâsibî, Ebû Ali el-Kerâbîsî",
                 "Nasları merkeze almakla birlikte inanç meselelerini <b>aklî yöntemlerle</b> (mantık ve istidlâl) temellendirmeyi öngörür."],
            ]
        ))
        .add_person(ESARI)
        .add_block(BulletBlock(3, "Hayatı ve Fikrî Dönüşümü", [
            "<b>Mu'tezile Yılları:</b> Babası bir Ehl-i Hadis âlimi olan Eş'arî, babasını küçük yaşta "
            "kaybetmiştir. Annesinin, dönemin Mu'tezile imamı <b>Ebû Ali el-Cübbâî</b> ile evlenmesi hayatının "
            "kırılma noktasıdır; üvey babasının ders halkasında <b>kırk yaşına kadar</b> koyu bir Mu'tezilî "
            "olmuş, hatta hocası adına münazaralara katılmıştır.",
            "<b>Ayrılış:</b> Uzun bir uzlet döneminin ardından <b>Basra Merkez Camii</b>'ne çıkarak Mu'tezile'yi "
            "terk ettiğini ilan etmiştir. İki temel gerekçesi: <b>(1)</b> Mu'tezile'nin rü'yetullahı reddetmesi, "
            "<b>(2)</b> kulun kendi fiilinin yaratıcısı olduğu fikri.",
        ]))
        .add_callout(Callout("caution", "Dikkat / Püf Noktası: Hanbelîlerin Reddi",
            "Eş'arî, Mu'tezile'yi terk ettikten sonra Ehl-i Hadis'in merkezi olan Bağdat'a giderek Hanbelîlerin "
            "lideri <b>Berbahârî</b>'ye katıldığını bildirmiştir. Ancak Berbahârî onu <b>reddetmiştir!</b> "
            "Çünkü Eş'arî, Mu'tezile'nin inançlarını terk etmiş olsa da onların kullandığı <b>kelâm "
            "(akıl/istidlâl) yöntemini</b> kullanmaya devam ediyordu. Ehl-i Hadis'ten yüz bulamayan Eş'arî'ye "
            "Şâfiî âlimlerinden <b>Ebû İshak el-Mervezî</b> sahip çıkmış ve Eş'arîlik Şâfiîler arasında hızla "
            "yayılmıştır."))
    )
    ch4.pages.append(
        ChapterPage()
        .add_block(BulletBlock(4, "Ayırt Edici Fikri: Kesb Teorisi", [
            "Mu'tezile'nin savunduğu ve Allah'a zorunluluk atfeden <b>\"Vücûb alellah\"</b> nazariyesini "
            "reddetmiştir.",
            "İnsan hürriyeti ile ilâhî kudret arasına <b>Kesb (Kazanım)</b> formülünü koymuştur: "
            "<b>\"Fiili yaratan Allah'tır, onu iradesiyle seçip kazanan (kesb) ise kuldur.\"</b>",
            "\"Eş'arî'nin, Ehl-i hadis ulemâsının aksine Ehl-i sünnet akâidini <b>kelâmî metotla</b> savunması "
            "büyük yankılar uyandırmış; Şâfiî ve Mâlikî âlimlerinin pek çoğu ile bazı Hanefî ve Hanbelî âlimleri "
            "üzerinde derin izler bırakmıştır.\"",
        ]))
        .add_block(BulletBlock(5, "Günümüze Ulaşan Beş Temel Eseri", [
            "<b>el-İbâne an usûli'd-diyâne:</b> Mu'tezile'den ilk ayrıldığı, zihninin netleşmediği dönemde "
            "Selefiyye'ye yaranmak için yazdığı, <b>Selefî izler</b> taşıyan eseri.",
            "<b>Risâle fî istihsâni'l-havz fî ilmi'l-kelâm:</b> Kendisini dışlayan Hanbelîlere karşı <b>kelâm "
            "ilminin gerekliliğini ve meşruiyetini</b> savunduğu risalesi.",
            "<b>Kitâbü'l-Luma':</b> Sünnî akîdeyi tamamen aklî/kelâmî delillerle ispatladığı, <b>Eş'arîliğin "
            "asıl omurgasını</b> oluşturan şaheseri.",
            "<b>Makâlâtü'l-İslâmiyyîn:</b> Mezhepler tarihinin en kıymetli eserlerinden; <b>Kâbe'ye yönelen "
            "kimsenin tekfir edilemeyeceğini</b> temellendirir.",
            "<b>Risâle ilâ ehli's-sağr:</b> Sınır boylarındaki (Bâbü'l-ebvâb) halkın kelâmî sorularına cevap "
            "veren erken dönem eseri.",
        ]))
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "Ebü'l-Hasan el-Eş'arî'nin başarısının sırrı, kırk yaşına kadar <b>Mu'tezile'nin içinde kalarak</b> "
            "rasyonel aklın (kelâmın) tüm diyalektik silahlarını çok iyi öğrenmesi; ardından bu silahları "
            "Ehl-i Sünnet'in geleneksel nass inancını savunmak için kusursuz bir <b>\"sentez\" (akıl-nakil "
            "dengesi)</b> hâlinde kullanmasıdır."))
        .add_summary("Eş'arîlik, Emevî Ta'rîb politikasından Abbâsî ihtilaline, Mihne'den Karşı-Mihne'ye uzanan "
            "siyasi kutuplaşmanın ve Selefiyye ile ilk kelâmcılar arasındaki metodolojik bölünmenin ortasında "
            "bir 'vasat' arayışı olarak doğmuştur. Kırk yaşına kadar Ebû Ali el-Cübbâî'nin halkasında yetişen "
            "Eş'arî, rü'yetullah ve kulun fiili yaratması meselelerindeki şüpheleriyle i'tizâlden ayrılmış; "
            "Berbahârî'nin reddine rağmen Şâfiîlerin desteğiyle mezhebini kurmuş ve Kesb teorisiyle ilâhî "
            "kudret ile insan sorumluluğu arasında kalıcı bir denge formülü üretmiştir.")
    )

    # =====================================================================
    # BÖLÜM 5 — Mütekaddimûn Dönemi
    # =====================================================================
    ch5 = Chapter(
        number=5,
        title="Eş'arîlikte Mütekaddimûn Dönemi",
        subtitle="Eş'arî'den Gazzâlî'ye: İslâm'a özgü bir kelâm mantığı inşa etme çağı",
        key_terms=[
            KeyTerm("Mütekaddimûn", "Eş'arî ile başlayıp Gazzâlî ile sona eren, yaklaşık iki yüzyıllık başlangıç ve sistemleşme evresi."),
            KeyTerm("Kıyâsü'l-gâib ale'ş-şâhid", "Duyu ötesini (görünmeyeni), duyulur âlemle (görünenle) karşılaştırarak ilâhî sıfatları anlama yöntemi."),
            KeyTerm("İn'ikâsü'l-edille", "Delilin geçersizliğiyle medlûlün (konunun) da geçersiz kabul edilişi; Bâkıllânî kurar, Cüveynî yıkar."),
            KeyTerm("Âdet Teorisi", "Tabiatta zorunlu determinizm olmadığı, düzenin Allah'ın iradesine bağlı bir alışkanlık olduğu görüşü."),
        ],
    )
    ch5.pages.append(
        ChapterPage()
        .add_terms(ch5.key_terms)
        .add_block(BulletBlock(1, "Dönemin Siyasi Çerçevesi ve Kelâm Metodolojisi", [
            "Dönem, Abbâsîlerin zayıfladığı, Bağdat'ın <b>334/945</b>'te Şiî Büveyhîlerin eline geçtiği ve "
            "<b>447/1055</b>'te Selçukluların bölgeye hâkim olduğu bir sultanlıklar devrine denk gelir.",
            "<b>Büveyhîler:</b> Şiî olmalarına rağmen Sünnî kitleyi karşılarına almamak için Eş'arî ulemâsına "
            "saygı duymuşlardır. Hükümdar <b>Fennâ Hüsrev</b>, Bâkıllânî'yi sarayında ağırlamış, oğluna hoca "
            "yapmış ve Bizans'a elçi olarak göndermiştir.",
            "<b>Selçuklular:</b> Vezir <b>Amîdülmülk el-Kündürî</b> döneminde Eş'arîlere kısa süreli bir baskı "
            "(<b>mihnetü'l-Eşâ'ire</b> / \"İkinci Mihne\") uygulanıp ders vermeleri yasaklanmışsa da; "
            "<b>Nizâmülmülk</b>'ün başa geçmesiyle Eş'arîlik altın çağını yaşamış ve <b>Nizâmiyye "
            "Medreseleri</b> aracılığıyla devlet destekli bir ekole dönüşmüştür.",
            "<b>İsbât-ı Vâcib:</b> Allah'ın varlığını ispatlamak için Mu'tezile gibi <b>hudûs</b> delilini "
            "kullanmışlar; atomcu (cevher-araz) tabiat felsefesiyle âlemin yaratılmışlığını, nübüvveti ve "
            "<b>ba's-ı cismânî</b>yi temellendirmişler; ancak katı determinizmi kesinlikle reddetmişlerdir.",
        ]))
        .add_table(ComparisonTable(
            "Mütekaddimûn Dönemi İstidlâl (Akıl Yürütme) Yöntemleri",
            ["Yöntem", "Kavramsal Karşılığı", "Kullanım Amacı"],
            [
                ["Kıyâsü'l-gâib ale'ş-şâhid", "Duyu ötesini, duyulur âlemle karşılaştırma.", "İnsan fiilleri veya tabiat kanunları üzerinden ilâhî sıfatları anlama çabası."],
                ["Sebr ve Taksîm", "İhtimalleri tartışma ve eleme usulü.", "Farklı teolojik iddiaları mantıksal olarak çürütmek."],
                ["İn'ikâsü'l-edille", "Delilin geçersizliğiyle medlûlün de geçersiz kabul edilişi.", "İnanca aracılık yapan delillerin bizzat inanç esası gibi mutlak kabul edilmesi."],
            ]
        ))
        .add_callout(Callout("focus", "Dönemin Özeti",
            "\"Bu dönemin en belirgin özelliği, klasik mantık ve felsefeden uzak durarak son tahlilde özü "
            "<b>Kur'ân ve sünnete dayanan bir akılcılığı</b> benimsemesi ve İslâmî ilkeleri bunun üzerine "
            "temellendirmesidir.\" Mütekaddimûn kelâmcıları, Aristo mantığı ve Yunan metafiziğinden bağımsız, "
            "tamamen <b>İslâm'a özgü bir usul</b> (kelâm mantığı) yaratmaya çalışmışlardır."))
    )
    ch5.pages.append(
        ChapterPage()
        .add_person(BAKILLANI)
        .add_block(BulletBlock(2, "Bâkıllânî ve İbn Fûrek", [
            "<b>Bâkıllânî (ö. 403/1013):</b> Atom düşüncesini (cüz lâ yetecezzâ) İslâm tabiat felsefesinin "
            "merkezine oturtmuş, mucizeleri ispatlamak için tabiatta zorunlu determinizm olmadığını savunarak "
            "<b>Âdet Teorisi</b>'ni kurmuştur. Haberî sıfatlar (vech, yed) hakkında zâhir-mecaz ayrımına "
            "girmeden <b>te'vili reddetmiştir</b>. Eserleri: <b>Temhîdü'l-evâ'il</b> (kelâm yöntemini sıkı "
            "uyguladığı ana eseri), <b>el-İnsâf</b> (naklî bilgiye daha çok yer veren pratik kelâm), "
            "<b>İ'câzü'l-Kur'ân</b>.",
            "<b>İbn Fûrek (ö. 406/1015):</b> Nîşâbur'da medrese kurarak ünlü sûfî <b>Abdülkerîm el-Kuşeyrî</b> "
            "dâhil yüzlerce talebe yetiştirmiş, zühd sahibi bir sûfî kelâmcıdır. Akıl vazgeçilmezdir ama aklın "
            "farklı hüküm verdiği yerde <b>sübûtu katî olan nass esastır</b>; <b>ilhamı</b> sübjektif olduğu "
            "için bilgi kaynağı saymaz ve haberî sıfatların <b>te'vilini zorunlu görür</b>. Eserleri: "
            "<b>Mücerredü makâlâti'ş-Şeyh Ebi'l-Hasan el-Eş'arî</b> (Eş'arî'nin görüşlerini günümüze taşıyan en "
            "önemli derleme) ve <b>Müşkilü'l-hadîs ve beyânüh</b>.",
        ]))
        .add_block(BulletBlock(3, "İsferâyînî ve Abdülkâhir el-Bağdâdî", [
            "<b>Ebû İshak el-İsferâyînî (ö. 418/1027):</b> Kâdî Abdülcebbâr gibi büyük Mu'tezilîleri münazarada "
            "mağlup etmiş, Eş'arî literatüründe <b>\"el-Üstâz\"</b> unvanını almıştır. Allah'ın mekân ve "
            "cihetten münezzeh olduğunu; ilâhî kelâmın harf ve sesten oluşmadığı için <b>âhirette "
            "işitilemeyeceğini</b> savunur. Velilerin keramet göstermesini imkânsız sayar; ona göre keramet, "
            "yalnızca Allah'ın onların <b>dualarını kabul etmesinden</b> ibarettir. Eseri: <b>el-Akîde</b>.",
            "<b>Abdülkâhir el-Bağdâdî (ö. 429/1037-38):</b> Diğer Eş'arîlerin aksine <b>ilhamı dördüncü bir "
            "bilgi kaynağı</b> olarak kabul eder. Allah'ın peygamberlere <b>günah işleme potansiyelini hiç "
            "vermediğini</b> ve ismet sıfatının bu şekilde oluştuğunu iddia eder. Eserleri: <b>el-Fark beyne'l-"
            "fırak</b> ve <b>el-Milel ve'n-nihal</b> (mezhepler tarihinin iki ana kaynağı), <b>Usûlü'd-dîn</b>.",
        ]))
        .add_person(CUVEYNI)
        .add_block(BulletBlock(4, "Cüveynî: Yöntemi Değiştiren Adam", [
            "Nizâmülmülk'ün başa geçmesiyle <b>Nîşâbur Nizâmiyye Medresesi</b>'nin başına getirilmiş ve "
            "<b>Gazzâlî'yi yetiştirmiştir</b>.",
            "Bâkıllânî'nin kurduğu <b>in'ikâsü'l-edille</b> ilkesini sertçe reddetmiştir.",
            "Allah'ın sıfatlarını açıklamak için Mu'tezile'nin icadı olan <b>Ahvâl</b> teorisini bir dönem "
            "benimsemiş; âlemdeki <b>determinizmi</b> (filozofların zorunlu nedensellik bağını) tamamen "
            "yıkmıştır.",
            "Eserleri: <b>eş-Şâmil fî usûli'd-dîn</b> (en hacimli kelâm eseri), <b>el-Akîdetü'n-Nizâmiyye</b> "
            "(Nizâmülmülk'e ithaf ettiği son eseri), <b>el-Burhân fî usûli'l-fıkh</b>.",
        ]))
    )
    ch5.pages.append(
        ChapterPage()
        .add_callout(Callout("caution", "Dikkat / Püf Noktası: İn'ikâsü'l-edille Çatışması",
            "Bâkıllânî'nin geliştirdiği <b>in'ikâsü'l-edille</b> (bir delil çürütülürse, o delilin ispatladığı "
            "inanç da çürütülmüş olur) prensibi mütekaddimûn döneminin belkemiğiydi. Ancak <b>Cüveynî</b> bu "
            "kuralın kelâmı çıkmaza soktuğunu ve zayıf bir delil çürüdü diye İslâm akîdesinin çürümüş "
            "sayılamayacağını belirterek bu kuralı yıkmış; öğrencisi <b>Gazzâlî</b> ise mantığı kelâma dâhil "
            "ederek yepyeni bir devir başlatmıştır."))
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "İmâmü'l-Haremeyn el-Cüveynî, <b>Mütekaddimûn</b> döneminin kapanışını ve <b>Müteahhirûn</b> "
            "döneminin felsefi kelâm şafağını başlatan bir <b>köprüdür</b>. Onun determinizmi yıkma stratejisi, "
            "Gazzâlî'nin filozofları tekfir edeceği sistemin temelini atmıştır."))
        .add_summary("Mütekaddimûn dönemi, Büveyhî hoşgörüsü ve Selçuklu-Nizâmiyye desteği arasında Eş'arîliğin "
            "sistemleştiği çağdır. Kıyâsü'l-gâib, sebr ve taksîm ile in'ikâsü'l-edille yöntemleri üzerine "
            "kurulan bu dönemde Bâkıllânî atomculuk ve Âdet teorisiyle mezhebin omurgasını, İbn Fûrek nass "
            "önceliği ve te'vil zorunluluğuyla dengesini, İsferâyînî ve Abdülkâhir el-Bağdâdî ise tenzih ve "
            "bilgi kaynağı tartışmalarını üretmiştir. Cüveynî, in'ikâsü'l-edilleyi yıkıp determinizmi "
            "kaldırarak dönemi kapatmış ve Gazzâlî'nin felsefi kelâmına kapıyı açmıştır.")
    )

    # =====================================================================
    # BÖLÜM 6 — Müteahhirûn Dönemi (Felsefi Kelâm)
    # =====================================================================
    ch6 = Chapter(
        number=6,
        title="Eş'arîlikte Müteahhirûn Dönemi (Felsefi Kelâm)",
        subtitle="Felsefeyi yenmek için felsefenin silahlarını kuşanmak: kelâmın varlık felsefesine dönüşümü",
        key_terms=[
            KeyTerm("Müteahhirûn", "VI/XII. asır ve sonrası; Gazzâlî'nin İbn Sînâ ile hesaplaşmasıyla başlayan felsefi kelâm dönemi."),
            KeyTerm("İlliyet", "Zorunlu nedensellik/determinizm; Gazzâlî bunu reddedip düzeni Allah'ın iradesine bağlı bir 'alışkanlık' sayar."),
            KeyTerm("Sıfât-ı Meânî", "Allah'ın zâtına ekli (ne aynı ne gayrı olan) ezelî sıfatlar; Eş'arî sıfat anlayışının merkezi."),
            KeyTerm("Ehl-i Kıble", "Namaz kılan ve temel esaslara inananlar; farklı te'villerinden dolayı kesinlikle tekfir edilemezler."),
        ],
    )
    ch6.pages.append(
        ChapterPage()
        .add_terms(ch6.key_terms)
        .add_block(BulletBlock(1, "Müteahhirûn Dönemine Geçiş", [
            "Kelâm ilminde <b>VI/XII. asır ve sonrasını</b> kapsayan, Gazzâlî'nin İslâm felsefesiyle (özellikle "
            "<b>İbn Sînâ</b>) hesaplaşmaya girişmesiyle başlayan döneme <b>Müteahhirûn</b> denir.",
            "Bu dönemde Eş'arîlik, felsefeyi mağlup etmek için <b>felsefenin silahlarını</b> (mantık ve "
            "terminoloji) kullanmış; bu sebeple döneme <b>\"Felsefi Kelâm Dönemi\"</b> de denilmiştir.",
            "<b>Kelâmın konusunun değişimi:</b> Mütekaddimûn'da \"Allah'ın zâtı ve sıfatları (usûlü'd-dîn)\" → "
            "Gazzâlî'de \"mevcut olmak bakımından mevcut varlıklar\" → sonraki dönemde <b>\"mâlûm\"</b> "
            "(bilginin alanına giren her şey).",
        ]))
        .add_table(ComparisonTable(
            "Mütekaddimûn ve Müteahhirûn Dönemlerinin Karşılaştırması",
            ["Ölçüt", "Mütekaddimûn (Öncekiler)", "Müteahhirûn (Sonrakiler)"],
            [
                ["Temel Disiplin", "Din usulü (usûlü'd-dîn) ve fıkıh eksenli.", "Küllî (kapsayıcı) ilim ve felsefe eksenli."],
                ["İstidlâl Yöntemi", "Kıyâsü'l-ğâib ale'ş-şâhid, in'ikâsü'l-edille.", "Klasik Aristo mantığı (tümevarım, tümdengelim, burhan)."],
                ["Varlık Anlayışı", "Hâdis-Kadîm ayrımı ve atomculuk (cevher/araz).", "Zorunlu-Mümkün (vâcip-mümkün) ve varlık-mahiyet ayrımı."],
                ["Muhatap / Hedef Kitle", "Hâricîler, Mu'tezile, Şîa ve Ehl-i Kitap.", "Filozoflar (felâsife), Bâtınîler ve marjinal gruplar."],
            ]
        ))
    )
    ch6.pages.append(
        ChapterPage()
        .add_callout(Callout("caution", "Dikkat / Püf Noktası: Gazzâlî'nin Kelâma Bakışı",
            "Gazzâlî, kelâm ilmini herkesin öğrenmesi gereken bir <b>gıda</b> değil; sadece şüpheleri gidermek "
            "ve bid'atlara karşı koymak için ihtiyaç duyulan bir <b>\"ilaç\"</b> olarak görmüştür. Ona göre "
            "kelâm tahsili, yalnızca zeki, dindar ve ahlâklı uzmanlarca yapılması gereken bir <b>farz-ı "
            "kifâye</b>dir. — <i>\"Mantık bilmeyenin ilmine güvenilmez.\"</i>"))
        .add_person(GAZZALI)
        .add_block(BulletBlock(2, "Gazzâlî ve Şehristânî", [
            "<b>Gazzâlî (ö. 505/1111):</b> <b>Hüccetü'l-İslâm</b> lakaplıdır; mütekaddimûn devrini kapatıp "
            "müteahhirûn dönemini başlatan kişidir. Bâtınîlik ve felsefeyle sert hesaplaşmalara girmiş, "
            "filozofları ilâhiyat meselelerindeki fikirlerinden dolayı <b>tekfir</b> etmiştir. Filozofların "
            "zorunlu <b>illiyet</b> prensibini reddederek tabiattaki düzenin zorunlu olmadığını, sadece "
            "Allah'ın iradesine bağlı bir <b>\"alışkanlık\"</b> olduğunu savunmuştur.",
            "<b>Eserleri:</b> <b>Tehâfütü'l-felâsife</b> (filozoflara efsanevi reddiye), <b>İhyâ'ü 'ulûmi'd-dîn</b> "
            "(fıkıh, kelâm, tasavvuf ve ahlakı harmanladığı şaheseri), <b>el-İktisâd fi'l-i'tikâd</b>, "
            "<b>el-Müstasfâ fî ilmi'l-usûl</b> ve <b>Fedâihu'l-Bâtıniyye</b>.",
            "<b>Şehristânî (ö. 548/1153):</b> Gazzâlî sonrasında felsefi kelâmın kilit isimlerindendir; "
            "mezhepler tarihini son derece <b>objektif</b> bir dille aktarmasıyla ünlüdür. Eserleri: "
            "<b>el-Milel ve'n-nihal</b> ve <b>Musâraatü'l-Felâsife</b> (İbn Sînâ'ya felsefi reddiye).",
        ]))
        .add_person(RAZI)
        .add_block(BulletBlock(3, "Âmidî, Beyzâvî ve Îcî", [
            "<b>Seyfüddîn el-Âmidî (ö. 631/1233):</b> Mantık ve felsefe eğitimini Bağdat'taki <b>Hristiyan ve "
            "Yahudi bilginlerden</b> almış, Râzî'nin felsefe-kelâm sentezini daha da ileri taşımıştır. İlâhî "
            "sıfatların aklî delillerle değil, <b>icmâ edilen naklî/sem'î delillerle</b> bilinebileceğini "
            "savunmuştur. Eserleri: <b>Ebkârü'l-efkâr</b>, <b>Gâyetü'l-merâm</b>, <b>el-İhkâm fî usûli'l-ahkâm</b>.",
            "<b>Kâdî Beyzâvî (ö. 685/1286):</b> Felsefe ile kelâm meselelerini ayrılamayacak şekilde "
            "harmanlamış <b>eklektik</b> bir âlimdir. Çoğu Eş'arî'nin aksine iman için sadece kalp ile tasdiki "
            "yeterli görmemiş, <b>dil ile ikrarı da şart koşmuştur</b>. Eserleri: <b>Envârü't-tenzîl ve "
            "esrârü't-te'vîl</b> (tefsir) ve <b>Tavâli'u'l-envâr</b> (kelâm).",
            "<b>Adûddîn el-Îcî (ö. 756/1355):</b> Metodolojisinin merkezinde <b>\"Tahkik\"</b> vardır; varlık "
            "konusunu ilâhiyat konularından bile önce ele alarak kelâmın çerçevesini belirlemiştir. "
            "Öğrencileri <b>Cürcânî ve Teftâzânî</b> ile birlikte Osmanlı medreselerinin ideal âlim modelini "
            "inşa etmiştir. Eseri: <b>el-Mevâkıf fî 'ilmi'l-kelâm</b>.",
        ]))
    )
    ch6.pages.append(
        ChapterPage()
        .add_block(BulletBlock(4, "Eş'arîliğin Temel İtikadî Görüşleri (Özet Çerçeve)", [
            "<b>Varlık ve Bilgi:</b> Âlem <b>hâdistir</b>. Varlık, birbirinin benzeri cevherlerden (atomlar) ve "
            "onların üzerinde duran arazlardan oluşur. Doğadaki kanunlar zorunlu değildir, <b>Allah'ın "
            "iradesine bağlıdır</b>.",
            "<b>Ulûhiyyet:</b> Allah'ın varlığı <b>hudûs, imkân veya nizam</b> delilleriyle aklen kanıtlanabilir. "
            "Allah'ın zâtına ekli (ne aynı ne gayrı olan) ezelî <b>Sıfât-ı Meânî</b>si vardır. Kelâmı "
            "<b>lafzen mahlûk, mâna olarak kadîmdir</b>. Haberî sıfatlar (vech, yed) Allah'ın şanına uygun "
            "olarak <b>te'vil edilir</b>. <b>Rü'yetullah haktır</b>.",
            "<b>İnsan Fiilleri (Kesb):</b> Fiili yaratan Allah, onu iradesiyle kazanan (kesb) ise kuldur; "
            "fiilin iyi/kötü vasfı kulun kudretiyle ilişkilidir.",
            "<b>İman ve Büyük Günah:</b> İman temel olarak <b>kalp ile tasdiktir</b>. Büyük günah işleyen, "
            "kalbinde tasdik olduğu sürece dinden çıkmaz, mümindir; tövbesiz ölürse durumu Allah'a kalır. "
            "<b>Ehl-i Kıble kesinlikle tekfir edilemez.</b>",
        ]))
        .add_callout(Callout("insight", "Kritik Çıkarım: Paradoksal Dönüşüm",
            "Eş'arîlik, tarih sahnesine Mu'tezile'nin aşırı akılcılığı ile Ehl-i Hadis'in aşırı nakilciliği "
            "arasında bir <b>\"vasat\"</b> bulmak için çıkmıştır. Ancak paradoksal biçimde, zaman ilerledikçe "
            "İslâm'ı felsefeye karşı korumak için <b>felsefenin metodolojisini kendi içine o kadar entegre "
            "etmiştir ki</b>, Gazzâlî sonrasında kelâm ilmi devasa bir <b>ontolojik varlık felsefesine</b> "
            "dönüşmüştür."))
        .add_summary("Müteahhirûn dönemi, Gazzâlî'nin Tehâfüt'üyle açılan ve kelâmın konusunu 'usûlü'd-dîn'den "
            "'mâlûm'a genişleten felsefi kelâm çağıdır. Aristo mantığı, vâcip-mümkün ontolojisi ve "
            "varlık-mahiyet ayrımı bu dönemin araçlarıdır. Gazzâlî illiyeti yıkıp filozofları tekfir etmiş, "
            "Şehristânî objektif mezhepler tarihini yazmış, Fahreddin er-Râzî felsefi kelâmın sistemini "
            "kurmuş, Âmidî sem'î delilleri öne çıkarmış, Beyzâvî ikrarı şart koşmuş, Îcî ise el-Mevâkıf ile "
            "Osmanlı medreselerinin âlim modelini şekillendirmiştir.")
    )

    # =====================================================================
    # BÖLÜM 7 — Mâtürîdîliğin Arka Planı ve Doğuşu
    # =====================================================================
    ch7 = Chapter(
        number=7,
        title="Mâtürîdîliğin Arka Planı, Hanefî Etkisi ve Doğuşu",
        subtitle="Sâmânîlerin özgür Semerkand'ında Ebû Hanîfe'nin mirasının kelâma dönüşmesi",
        key_terms=[
            KeyTerm("Mâverâünnehir", "Ceyhun nehrinin ötesi (Transaxonia); Sâmânîler yönetimindeki, ilim ve kültürde altın çağını yaşayan bölge."),
            KeyTerm("Dârü'l-Cüzcâniyye", "Hanefîliğin Semerkand'da kurumsallaştığı, Mâtürîdî'nin yetişip ders verdiği ilim merkezi."),
            KeyTerm("Re'y", "Hanefîliğin akla ve içtihada verdiği önem; Mâtürîdî kelâmının rasyonel karakterinin kaynağı."),
            KeyTerm("Tebsıratü'l-edille", "Ebü'l-Muîn en-Nesefî'nin eseri; Mâtürîdîliği müstakil bir kelâm mezhebi olarak tescilleyen kırılma noktası."),
        ],
    )
    ch7.pages.append(
        ChapterPage()
        .add_terms(ch7.key_terms)
        .add_block(BulletBlock(1, "Mâverâünnehir ve Semerkand'ın Siyasi-Dinî Ortamı", [
            "Mâtürîdîliğin doğduğu coğrafya olan <b>Mâverâünnehir</b> (Ceyhun nehrinin ötesi / Batı dillerinde "
            "Transaxonia), Abbâsîlerden ayrılarak bağımsızlığını ilan eden <b>Sâmânîler</b> devletinin yönetimi "
            "altındaydı; bölge ilim ve kültür açısından altın çağını yaşıyordu.",
            "<b>İlmî Rekabet:</b> Fıkıh ve usûl-i fıkıhta <b>Hanefî ve Şâfiî</b> fakihler arasında mescitlerde "
            "sürekli münazaralar yapılıyor; matem evleri bile bu ilmî tartışmalarla şenleniyordu.",
            "<b>Heterodoks Akımlara Karşı Sünnî Kale:</b> Sâmânîlerin sağladığı özgürlük ortamında akıl "
            "kisvesine bürünmüş heterodoks inançlar ve Mu'tezile yayılma eğilimindeydi. Bölgedeki Sünnî "
            "âlimler bu akımlara karşı ciddi bir entelektüel savaş vererek <b>Mu'tezile'nin dolaşım alanını "
            "daraltmış</b> ve Ehl-i Sünnet'in üstünlüğünü sağlamışlardır.",
        ]))
        .add_block(BulletBlock(2, "Hanefîliğin Bölgedeki Etkisi ve Dönüşümü", [
            "Abbâsîler döneminde <b>Hanefî kadıların</b> Irak, İran ve Mâverâünnehir'e atanması, mezhebin bu "
            "coğrafyalarda kök salmasını sağladı.",
            "Hanefîliğin <b>akla ve içtihada (re'y)</b> önem veren yapısı, Hicaz'ın katı Arap örfüne alışkın "
            "olmayan yeni toplum katmanları (özellikle <b>Türkler</b>) tarafından İslâm'ın çok daha kolay "
            "benimsenmesini sağladı.",
            "Ebû Hanîfe'nin akâid mirası coğrafi ve metodolojik olarak <b>iki farklı koldan</b> ilerlemiştir.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("Ebû Hanîfe", "İtikadî miras: akıl ve re'y"),
            FlowStep("Mısır — Tahâvî", "Selef (Ehl-i Hadis) çerçevesinde yorumlandı"),
            FlowStep("Mâverâünnehir — Mâtürîdî", "Kelâm yöntemi ve aklî istidlâlle sistemleşti"),
            FlowStep("Mâtürîdiyye", "Müstakil bir kelâm ekolüne dönüştü"),
        ], caption="Ebû Hanîfe'nin İtikadî Mirasının İki Kolu"))
    )
    ch7.pages.append(
        ChapterPage()
        .add_person(MATURIDI)
        .add_block(BulletBlock(3, "Dârü'l-Cüzcâniyye ve Semerkand Ekolü", [
            "Semerkand, İslâm öncesi ve sonrasında farklı din ve kültürlerin <b>kavşak noktasıydı</b>.",
            "Hanefîliğin Semerkand'da kurumsallaştığı en önemli ilim merkezi <b>Dârü'l-Cüzcâniyye</b>'dir; İmam "
            "Mâtürîdî'nin de yetiştiği ve ders verdiği bu okul, Ebû Hanîfe'nin fikirlerini doğrudan "
            "Mâverâünnehir'e taşıyan bir <b>köprü</b> vazifesi görmüştür.",
            "<b>Hoca-Talebe Silsilesi:</b> İmam Ebû Hanîfe → İmam Muhammed eş-Şeybânî → <b>Ebû Süleyman "
            "el-Cüzcânî</b> → Ebû Nasr el-İyâzî → <b>İmam Mâtürîdî</b>. Silsiledeki ilk hocaların \"Cüzcânî\" "
            "lakaplı olması, okula bu ismin verilmesini sağlamıştır.",
        ]))
        .add_block(BulletBlock(4, "Ekolleşme Süreci", [
            "<b>İlk İsimlendirmeler:</b> Mezhep ilk dönemlerde kurucu hocaların isimlerine nispetle "
            "<b>Cüzcâniyye</b> ve <b>İyâziyye</b> ekolü olarak anılmıştır.",
            "<b>Sistemleşme:</b> İmam Mâtürîdî, Ebû Hanîfe'nin fıkhî-itikadî mirasını kelâmın rasyonel "
            "argümanlarıyla o kadar güçlü biçimde yeniden inşa etti ki, <b>vefatından bir asır sonra</b> ekol "
            "tamamen onun adıyla (<b>Mâtürîdiyye</b>) anılmaya başlandı.",
        ]))
        .add_person(NESEFI)
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "Mâtürîdîlik; Ebû Hanîfe'nin <b>rasyonel/re'y merkezli</b> din anlayışının, Sâmânîler dönemindeki "
            "özgür tartışma ortamında ve Semerkand'ın kozmopolit yapısında, gnostik ve heterodoks akımlara "
            "karşı İslâm'ı savunmak üzere <b>kelâmî bir silaha (metodolojiye)</b> dönüşmüş hâlidir."))
        .add_summary("Mâtürîdîlik, Sâmânîlerin özgür ilim ortamındaki Mâverâünnehir'de, Hanefî kadılar "
            "eliyle kök salmış re'y merkezli bir geleneğin üzerine kurulmuştur. Ebû Hanîfe'nin itikadî mirası "
            "Mısır'da Tahâvî eliyle Selefî çizgide yorumlanırken, Semerkand'daki Dârü'l-Cüzcâniyye'de Mâtürîdî "
            "tarafından kelâmî istidlâlle sistemleştirilmiş; başlangıçta Cüzcâniyye ve İyâziyye adlarıyla "
            "anılan ekol, Mâtürîdî'nin vefatından bir asır sonra onun adını almış ve nihayet Ebü'l-Muîn "
            "en-Nesefî'nin Tebsıratü'l-edille'siyle müstakil bir kelâm mezhebi olarak tescillenmiştir.")
    )

    # =====================================================================
    # BÖLÜM 8 — Mâtürîdîliğin Temel Görüşleri
    # =====================================================================
    ch8 = Chapter(
        number=8,
        title="Mâtürîdîliğin Temel Görüşleri",
        subtitle="Bilgi teorisinden âhirete: akıl ile naklin muazzam dengesi üzerine kurulu bir sistem",
        key_terms=[
            KeyTerm("Temânu' Delili", "Birden fazla ilah olsaydı biri diğerinin iradesini engellerdi ve kâinatın düzeni kaosa dönerdi (Enbiyâ 21/22)."),
            KeyTerm("Tekvin", "Allah'ın yaratma eylemini ifade eden, Mâtürîdîlere göre zâta ekli ezelî ve müstakil bir sıfat."),
            KeyTerm("Cüz'î İrade", "İnsanın zihnî bir fonksiyon olan seçme gücü; Allah'ın yaratmasına konu teşkil etmez."),
            KeyTerm("Ba's-ı Cismânî", "Kıyamet sonrası dirilişin sadece ruhani değil, bizzat bedenle birlikte gerçekleşmesi."),
        ],
    )
    ch8.pages.append(
        ChapterPage()
        .add_terms(ch8.key_terms)
        .add_block(BulletBlock(1, "Bilgi Teorisi (Epistemoloji)", [
            "Mâtürîdî, kelâm sistemini doğrudan bir <b>bilgi teorisiyle</b> başlatarak dönemine göre devrim "
            "niteliğinde bir adım atmıştır.",
            "\"Akıl yürütmeyi inkâr eden kimsenin elinde onu reddetmek için <b>akıl yürütmekten başka bir "
            "kanıt yoktur</b>. Bu da istidlâlin gerekliliğinin bir delili olmuştur.\" (İmam Mâtürîdî)",
        ]))
        .add_table(ComparisonTable(
            "Mâtürîdî'nin Üç Bilgi Kaynağı",
            ["Kaynak", "Tanım ve Kapsamı", "Bilgi Değeri"],
            [
                ["1. Duyular ('Iyân)", "Beş duyu organı, iç duyular ve içgüdüleri kapsar.", "Dış dünyadaki fiziksel ve iç dünyadaki ruhsal objelerin kesin bilgi vasıtasıdır."],
                ["2. Haber (Vahiy ve Rivayet)", "Peygamberin haberi (Vahiy/Kur'an) mutlak doğru bilgidir.", "Kesinlik ifade eder (âhâd haberler hariç)."],
                ["3. Akıl Yürütme (İstidlâl)", "Duyuların ve haberin verilerini ölçen, işleyen hakem mekanizmasıdır.", "Doğru kullanıldığında (zarurî/bedîhî ve istidlâlî) kesin bilgi üretir."],
            ]
        ))
        .add_callout(Callout("caution", "Dikkat / Püf Noktası: Haber Çeşitlerindeki İnce Fark",
            "Mâtürîdî, <b>mütevatir haberi</b> diğer âlimlerden farklı tanımlar: ona göre mütevatir, "
            "\"yanılmaları ve yalan söylemeleri muhtemel bulunan kişiler yoluyla\" gelen ama <b>yalan üzerine "
            "birleşmeleri imkânsız</b> olan haberdir. <b>Âhâd haber</b> ise itikadî konularda "
            "(<b>ilmü'ş-şehâde</b>) kesin delil kabul edilmez; sadece fıkhî/amelî konularda "
            "(<b>ilmü'l-amel</b>) inceleme şartıyla kullanılabilir."))
    )
    ch8.pages.append(
        ChapterPage()
        .add_person(MATURIDI)
        .add_block(BulletBlock(2, "Ulûhiyet: Allah'ın Varlığı, Birliği ve Sıfatları", [
            "<b>Aklın Vacip Kılması:</b> Mâtürîdî'ye göre Allah <b>hiç peygamber göndermeseydi bile</b>, "
            "insanın sadece aklını kullanarak Allah'ın varlığını ve birliğini bulması <b>aklen vaciptir</b>.",
            "<b>Temânu' Delili:</b> Kâinatın yaratıcısı kesinlikle birdir; eğer birden fazla ilah olsaydı biri "
            "diğerinin iradesini engellemeye (temânu') çalışırdı ve kâinatın düzeni <b>kaosa dönerdi</b> "
            "(Enbiyâ 21/22 bağlamında).",
            "<b>Tekvin Sıfatı:</b> Mâtürîdîler, Eş'arîlerden farklı olarak Allah'ın yaratma eylemini ifade eden "
            "<b>Tekvin</b> sıfatını tıpkı ilim, irade ve kudret gibi zâta ekli (zâid) <b>ezelî ve müstakil</b> "
            "bir sıfat olarak kabul etmişlerdir.",
        ]))
        .add_block(BulletBlock(3, "Nübüvvet: Peygambere Aklen Duyulan İhtiyaç", [
            "Peygamber göndermek Allah'ın insanlara bir <b>lütfudur</b>.",
            "<b>(1)</b> İnsanlar arasındaki belirgin anlaşmazlıkları çözecek bir <b>hakem otoritesi</b> olması.",
            "<b>(2)</b> Aklın bulamayacağı, sadece Allah katında olan <b>âhiret ve gayb bilgilerinin</b> "
            "insanlara ulaştırılması.",
            "<b>(3)</b> Aklın çelişkiye düştüğü yerlerde doğruyu gösterecek bir <b>ölçüt</b> olması. "
            "Peygamberlerin <b>erkek olması şarttır</b> ve onlar günah işlemekten korunmuşlardır (<b>ismet</b>).",
        ]))
        .add_block(BulletBlock(4, "İman-Amel İlişkisi ve Büyük Günah", [
            "<b>İmanın Tanımı:</b> İman temelde <b>kalbin tasdikidir</b>; dil ile ikrar sadece kalpte olanın "
            "dışa vurumudur.",
            "<b>Amel İmandan Parça Değildir:</b> Dinî bir kuralın farz olduğuna <b>inanmamak küfürdür</b>; farz "
            "olduğuna inandığı hâlde onu yapmamak ise küfür değil, <b>günahtır</b>.",
            "<b>İmanda Artma ve Eksilme Olmaz:</b> İman bir bütün olarak artmaz veya eksilmez; artan şey imanın "
            "miktarı değil, <b>nûru, kuvveti ve kalpteki pekişmesidir</b> (basireti).",
            "<b>Büyük Günah:</b> Büyük günah işleyen kişi dinden çıkmaz, kâfir olmaz; <b>fâsıktır</b> (günahkâr "
            "mümin). Şirk ve küfür hariç, Allah dilerse onu affeder, dilerse cezalandırır.",
        ]))
        .add_block(BulletBlock(5, "Kazâ, Kader ve İnsan Fiilleri", [
            "<b>Kazâ:</b> Allah'ın bir şeye hükmedip karar vermesi, eşyayı mahiyetine uygun olarak "
            "oluşturmasıdır.",
            "<b>Kader:</b> Eşyanın oluşacağı zamanı, mekânı ve doğuracağı sonuçları <b>ezelde belirlemesidir</b>.",
            "İnsan <b>cüz'î irade</b> sahibidir; bu irade zihnî bir fonksiyondur ve Allah'ın yaratmasına konu "
            "teşkil etmez (yani Allah insanı belli bir seçime zorlamaz).",
            "İnsan <b>diler ve kazanır (kâsip)</b>, Allah ise o fiili <b>yaratır (hâlık)</b>; bu sebeple mükâfat "
            "veya ceza insanın kendi tercihinin sonucudur. Mâtürîdî'ye göre insan, rüzgârın önünde savrulan bir "
            "yaprak (Cebriyye) olmadığı gibi, kendi fiilinin mutlak yaratıcısı (Mu'tezile) da değildir.",
        ]))
    )
    ch8.pages.append(
        ChapterPage()
        .add_flow(FlowDiagram([
            FlowStep("İrade ve Karar", "İnsan"),
            FlowStep("Kesb / Kazanma", "İnsan"),
            FlowStep("Kudretle Yaratma", "Allah"),
            FlowStep("Sorumluluk", "İnsan"),
        ], caption="Mâtürîdî'ye Göre İnsan Fiilinin Oluşum Zinciri"))
        .add_block(BulletBlock(6, "Âhiret", [
            "Âhiretin varlığı <b>ilâhî adaletin aklî bir zorunluluğudur</b>: iyilik yapanla kötülük yapanın "
            "dünyada eşit şartlarda ölmesi adaletsizliktir; bu denge ancak âhirette sağlanır.",
            "<b>Kabir hayatı ve azabı haktır.</b>",
            "Kıyamet koptuktan sonra diriliş (<b>ba's</b>) sadece ruhani değil, bizzat bedenle birlikte "
            "(<b>ruhlu-bedenli cismânî diriliş</b>) gerçekleşecektir.",
        ]))
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "Mâtürîdîlik; Mu'tezile'nin aklı naklin üzerine çıkaran kibrine düşmeden, Selefiyye'nin de aklı "
            "tamamen reddeden taassubuna kaymadan muazzam bir <b>\"akıl-nakil sentezi\"</b> kurmuştur. İnsana "
            "eylem sorumluluğu yüklerken (cüz'î irade), Allah'ın mutlak yaratıcılığını (Tekvin) asla "
            "zedelememiştir."))
        .add_summary("Mâtürîdî, kelâmı bir bilgi teorisiyle (duyular, haber, istidlâl) başlatarak sistemini "
            "epistemolojik bir zemine oturtmuş; mütevatir-âhâd ayrımını inceltmiştir. Ulûhiyette aklın vahiy "
            "gelmeden Allah'ı bulmasını vacip saymış, temânu' deliliyle tevhidi ispatlamış ve Tekvin'i "
            "müstakil sıfat kabul etmiştir. Nübüvveti aklî üç gerekçeyle temellendirmiş; imanı kalbin tasdiki "
            "sayıp ameli imandan ayırmış; kazâ-kaderi tanımlayıp cüz'î irade ile kesb üzerinden insanı "
            "sorumlu, Allah'ı yaratıcı kılan bir denge kurmuş ve âhireti ilâhî adaletin aklî zorunluluğu "
            "olarak temellendirmiştir.")
    )

    # =====================================================================
    # BÖLÜM 9 — Eş'arîlik ile Mâtürîdîlik Arasındaki Farklar
    # =====================================================================
    ch9 = Chapter(
        number=9,
        title="Ehl-i Sünnet İçi İhtilaflar",
        subtitle="Eş'arîlik ve Mâtürîdîlik arasındaki temel farklar: kudret ile hikmet arasındaki denge tercihi",
        key_terms=[
            KeyTerm("Marifetullah", "Allah'ı bilmek; Mâtürîdî'de vahiy gelmese de aklen farz, Eş'arî'de yalnızca şeriatla mükellefiyet doğar."),
            KeyTerm("Teklif-i mâ lâ yutak", "Gücün yetmeyeceği şeyin yüklenmesi; Mâtürîdî'de imkânsız, Eş'arî'de aklen caiz."),
            KeyTerm("Azm-i Musammam", "Mâtürîdîlerin kesb tanımı: kesin kararlılık; fiilin vasfı insanın kudretiyle oluşur."),
            KeyTerm("İtibar Hâtimeyedir", "Eş'arîlere göre hükmün son nefese göre verilmesi; Mâtürîdîler kişiyi hâlihazırdaki durumuyla değerlendirir."),
        ],
    )
    ch9.pages.append(
        ChapterPage()
        .add_terms(ch9.key_terms)
        .add_block(BulletBlock(1, "İhtilafların Çerçevesi ve Sayısı", [
            "Sünnî kelâmın iki büyük kalesi olan Eş'arîlik ve Mâtürîdîlik, <b>temel inanç esaslarında tamamen "
            "aynı çizgide</b> yer alsalar da; aklın sınırı, ilâhî kudretin mutlaklığı ve insanın sorumluluk "
            "alanı gibi konularda birbirlerinden ayrılmışlardır.",
            "İhtilaflı meselelerin sayısı kelâmcılara göre farklılık gösterir: <b>Hâdimî 73</b>, <b>Beyâzî 50</b>, "
            "<b>Şeyhzâde 40</b>, <b>İbn Sübkî ise 13</b> mesele tespit etmiştir.",
            "Bu farklılıkların büyük bir kısmı teferruata veya kavramsal (lafzî) yorumlara dayansa da; "
            "özellikle <b>epistemoloji</b> ve <b>ilâhî sıfatlar</b> konusunda belirgin zıtlıklar mevcuttur.",
        ]))
        .add_table(ComparisonTable(
            "İhtilaflı Meseleler — I: Bilgi, Sıfat ve Kader",
            ["Mesele", "Mâtürîdîlik", "Eş'arîlik"],
            [
                ["Allah'ı Aklen Bilmek (Marifetullah)", "Vahiy gelmese dahi, aklın kendi başına Allah'ın varlığını bulması <b>farzdır</b>.", "Aklen farz değildir; sadece peygamber tebliğiyle (şeriatla) mükellefiyet doğar."],
                ["Hüsün ve Kubuh", "Akıl, vahiy gelmeden de iyilik ve kötülüğü idrak edebilir; çünkü bunlar fiilin <b>zâtındadır</b>.", "İyilik ve kötülük zâtî değildir; vahiy olmadan aklın bunları tespit imkânı yoktur."],
                ["Tekvin (Yaratma) Sıfatı", "Tıpkı kudret gibi <b>ezelî ve müstakil</b> bir sıfattır; mükevvenden ayrıdır.", "İtibarî bir şeydir, kudret sıfatının bir taallukudur (yansımasıdır); mükevvenin aynıdır."],
                ["Kazâ ve Kader Kavramları", "<b>Kader:</b> ezeldeki takdir. <b>Kazâ:</b> bu takdire göre eşyanın yaratılması.", "<b>Kazâ:</b> ezeldeki takdir. <b>Kader:</b> bu takdirin meydana çıkması."],
                ["İnsan Fiilleri ve Kesb", "Kesb, <b>azm-i musammamdır</b> (kesin kararlılık); fiilin vasfı insanın kudretiyle oluşur.", "İnsan kudretinin icatta tesiri yoktur; kesb, kudretin makdûra iktirânından (bitişmesinden) ibarettir."],
            ]
        ))
    )
    ch9.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "İhtilaflı Meseleler — II: İlâhî Fiiller, İman ve Nübüvvet",
            ["Mesele", "Mâtürîdîlik", "Eş'arîlik"],
            [
                ["Teklif-i mâ lâ yutak", "Allah'ın gücün yetmeyeceği bir şeyi teklif etmesi <b>imkânsızdır</b>.", "Allah'ın bunu teklif etmesi aklen <b>caiz ve mümkündür</b>."],
                ["İlâhî Fiillerde Hikmet ve İllet", "Allah'ın fiillerinde lüzum ve lütuf yoluyla <b>mutlaka</b> hikmet ve illetler vardır.", "Lüzum yoluyla değil, ancak cevaz yoluyla hikmetler olabilir veya olmayabilir."],
                ["Tehditten (Vaîd) Dönme", "Allah'ın verdiği ceza tehdidinden dönmesi <b>imkânsızdır</b>.", "Allah dilerse vaîdinden <b>dönebilir</b>."],
                ["Allah İçin \"Çirkinlik\"", "Allah çirkin bir şey yapmaz; mümini ebedî cehenneme, kâfiri cennete koyması aklen imkânsızdır.", "Allah'ın fiillerinde çirkinlik diye bir şey yoktur; mümini cehenneme, kâfiri cennete koyabilir."],
                ["Küfrün Affedilme İhtimali", "Küfür ve şirkin affı şer'an imkânsız olsa da <b>aklen caizdir</b>.", "Küfrün affı hem aklen hem şer'an <b>caiz değildir</b>."],
                ["İmanda Artma ve Eksilme", "İman bir bütündür, <b>artmaz ve eksilmez</b>.", "İman <b>artar ve eksilir</b>."],
                ["İmanda İstisna", "İman kesinlik gerektirdiği için \"İnşallah müminim\" demek <b>caiz değildir</b>.", "\"İnşallah müminim\" demek <b>caizdir</b>."],
                ["İtibar Hâtimeyedir", "Şu an mümin olan kişi Müslümandır; ömrünün sonunda dinden çıkarsa küfrü üzere ölmüş olur.", "İtibar son nefesedir; kâfir ölen kişi, geçmişte Müslüman olsa bile ömür boyu kâfir yaşamış sayılır."],
                ["Nübüvvette Cinsiyet", "Peygamberlik makamında <b>erkek olmak şarttır</b>.", "Peygamberlikte erkek olmak <b>şart değildir</b>."],
                ["Peygamberlerin Ölüm Sonrası Durumu", "Vefattan sonra da <b>hakikaten</b> peygamberdirler.", "Vefattan sonra <b>hükmen</b> peygamberdirler."],
                ["İnsan ve Meleklerin Üstünlüğü", "Avam müminler, avam meleklerden <b>daha üstündür</b>.", "Umum melekler, umum insanlardan <b>daha üstündür</b>."],
            ]
        ))
        .add_callout(Callout("caution", "Dikkat / Püf Noktası: Kader-Kazâ ve Teklif-i Mâ Lâ Yutak Sorunsalı",
            "Eş'arîlik ve Mâtürîdîlik arasındaki ayrımın en kilit noktası, Allah'ın <b>\"Kudreti\"</b> ile "
            "Allah'ın <b>\"Adaleti/Hikmeti\"</b> arasındaki denge tercihidir. Eş'arîler, Allah'ın mutlak "
            "kudretini her türlü mantıksal zorunluluğun üstünde tuttukları için \"Allah insana gücünün "
            "yetmeyeceği yükü yükleyebilir, dilerse mümini cehenneme kâfiri cennete atabilir, fiillerinde "
            "hikmet aramak zorunlu değildir\" demişlerdir. Mâtürîdîler ise insanın sorumluluğunu ve Allah'ın "
            "hikmetini merkeze aldıkları için \"Allah çirkin iş yapmaz, gücü aşan teklif yüklemez\" diyerek "
            "akla ve ilâhî adalete daha çok alan açmışlardır. Ayrıca <b>her iki mezhep Kazâ ve Kader "
            "kavramlarını tam zıt (yer değiştirmiş) anlamlarda kullanmışlardır.</b>"))
    )
    ch9.pages.append(
        ChapterPage()
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "Mâtürîdîlik, özellikle <b>bilgi teorisinde</b> (aklın vahiy gelmeden Allah'ı bulabilmesi ve "
            "iyi/kötüyü ayırabilmesi) ve <b>insan fiillerinde</b> (cüz'î iradeye ve kesbe daha fazla gerçeklik "
            "payı vermesi) akla daha geniş bir <b>otonomi</b> tanımış; Eş'arîlik ise Allah'ın zâtının "
            "sınırlandırılamaz <b>mutlak kudretini</b> vurgulayarak nassı aklın tartışmasız hakemi konumuna "
            "yükseltmiştir."))
        .add_summary("Sünnî kelâmın iki kalesi temel esaslarda aynı çizgide dursa da Hâdimî'ye göre 73, İbn "
            "Sübkî'ye göre 13 meselede ayrışır. Mâtürîdîlik marifetullahı aklen farz sayar, hüsün-kubhu fiilin "
            "zâtına yerleştirir, Tekvin'i müstakil sıfat kabul eder, teklif-i mâ lâ yutakı imkânsız görür, "
            "ilâhî fiillerde hikmeti zorunlu kılar ve imanı artıp eksilmeyen bir bütün sayar. Eş'arîlik ise "
            "mutlak ilâhî kudreti önceleyerek bunların karşıtını savunur; iki mezhep ayrıca kazâ ile kaderi "
            "tam zıt anlamlarda kullanır. Ayrımın özü, kudret ile hikmet arasındaki denge tercihidir.")
    )

    chapters = [ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8, ch9]

    # =====================================================================
    # SÖZLÜK
    # =====================================================================
    glossary = [
        Concept("İ'tizâl", "Arapça 'a-z-l' kökünden; ayrılmak, uzaklaşmak, bir köşeye çekilmek.", "Mu'tezile'nin adı", 1),
        Concept("Mürtekib-i Kebîre", "Büyük günah işleyen kişi; ilk dönem kelâm tartışmalarının merkezindeki figür.", "Kebîre tartışması", 1),
        Concept("Ehlü'l-Adl ve't-Tevhîd", "Mu'tezile'nin kendine verdiği isim; sıfat ve hür irade görüşlerini yansıtır.", "İsimlendirme", 1),
        Concept("Kaderiyye", "Ehl-i Sünnet'in Mu'tezile'ye verdiği yerme lakabı; insanın fiilini kendi kudretiyle yarattığı görüşünden.", "İsimlendirme", 1),
        Concept("Cebriyye", "İnsanın fiillerinde mecbur olduğunu savunan ekol; Emevîler zulümlerini bununla meşrulaştırmıştır.", "İç faktörler", 1),
        Concept("Hâricîler", "Büyük günah işleyeni dinden çıkmış (kâfir) sayan, ebedî cehennemlik kabul eden ekol.", "Kebîre tartışması", 1),
        Concept("Mürcie", "Ameli imandan parça saymayıp büyük günah işleyeni tam mümin kabul eden ekol.", "Kebîre tartışması", 1),
        Concept("Zeydiyye", "Yemen'deki Şiî fırka; sürgünlerden sonra Mu'tezile bu yapı içinde erimiştir.", "Çöküş", 1),
        Concept("Mihne", "Me'mûn'la başlayan, ulemaya Halku'l-Kur'an tezinin devlet zoruyla dayatıldığı engizisyon dönemi.", "Abbâsî dönemi", 1),
        Concept("Halku'l-Kur'an", "Kur'an'ın kadîm değil mahlûk olduğu tezi; Mihne'nin sınav sorusu.", "Tevhid ilkesi", 1),
        Concept("Karşı-Mihne", "Mütevekkil'le başlayan, Ehl-i Hadis'in devlet destekli tasfiye hareketi.", "Çöküş", 1),
        Concept("Basriyyûn", "Ebü'l-Hüzeyl el-Allâf'ın kurduğu, ilme odaklı teorik Mu'tezile kanadı.", "Ekol ayrışması", 2),
        Concept("Bağdâdiyyûn", "Bişr b. Mu'temir'in kurduğu, Abbâsî sarayıyla iç içe siyasi kanat.", "Ekol ayrışması", 2),
        Concept("Cüz lâ yetecezzâ", "Bölünemeyen parça (atom); Allâf ve Bâkıllânî'nin âlemin hâdisliğini ispat aracı.", "Atomculuk", 2),
        Concept("Tafra", "Nazzâm'ın teorisi: bir cismin aradaki mekânlara uğramadan sıçrayarak yer değiştirmesi.", "Nazzâm", 2),
        Concept("Kümûn-Zuhûr", "Varlıkların tek seferde yaratılıp bir kısmının gizlenmesi ve zamanla belirmesi.", "Nazzâm", 2),
        Concept("Sarfe", "Kur'an'ın benzerinin getirilememesinin, insanların bu güçten alıkonulmasıyla açıklanması.", "Nazzâm", 2),
        Concept("Ahvâl Teorisi", "Ebû Hâşim'in sıfat çözümü: ne var ne yok, ne kadîm ne hâdis olan 'hâller'.", "Ebû Hâşim el-Cübbâî", 2),
        Concept("Tevellüd", "İnsanın kendi kudretiyle başka bir şey üzerinde etki oluşturması (bağımlı fiiller).", "Bişr b. Mu'temir", 2),
        Concept("Ma'dûm", "Yokluk/yok olan; Hayyât bunu şey ve cevherin yanı sıra 'cisim' olarak da kabul eder.", "Hayyât", 2),
        Concept("Lütuf Teorisi", "Bişr'in görüşü: aslah Allah için bir zorunluluk değil, ilâhî bir ihsandır.", "Bişr b. Mu'temir", 2),
        Concept("Mütevellid Fiiller", "Dolaylı olarak doğan fiiller; Sümâme bunların bir fâili olmadığını savunur.", "Sümâme b. Eşres", 2),
        Concept("Usûl-i Hamse", "Mu'tezilî olmanın şartı olan beş temel ilke; ekol bunlarda tam ittifak etmiştir.", "Mu'tezile ilkeleri", 3),
        Concept("Teaddüd-i Kudemâ", "Birden fazla kadîm varlığın kabulü; zâttan ayrı kadîm sıfat kabulünün doğurduğu problem.", "Tevhîd", 3),
        Concept("Tenzih", "Allah'ı yaratılmışlara benzemekten ve kusurlardan arındırma prensibi.", "Tevhîd", 3),
        Concept("Teşbih ve Tecsîm", "Allah'ı bir varlığa benzetme ve O'na cisim atfetme; Mu'tezile bunları şirk sayar.", "Tevhîd", 3),
        Concept("Rü'yetullah", "Allah'ın âhirette gözle görülmesi; Mu'tezile reddeder, Eş'arîlik hak sayar.", "Tevhîd", 3),
        Concept("Aslah", "Allah'ın kulları için daima en faydalı olanı yaratmak zorunda oluşu.", "Adâlet", 3),
        Concept("Hüsün ve Kubuh", "İyilik ve kötülüğün fiilin zâtında bulunması ve aklın bunu vahiysiz bulabilmesi.", "Adâlet", 3),
        Concept("Teklif-i mâ lâ yutak", "İnsanın gücünün yetmeyeceği şeyin ona yüklenmesi.", "Adâlet", 3),
        Concept("el-Va'd ve'l-Vaîd", "Allah'ın ödül sözü (va'd) ile ceza tehdidi (vaîd); şefaatin reddinin dayanağı.", "Usûl-i Hamse", 3),
        Concept("el-Menzile beyne'l-Menzileteyn", "Büyük günah işleyenin ne mümin ne kâfir, 'fâsık' sayılması.", "Vâsıl b. Atâ", 3),
        Concept("Emir bi'l-Ma'rûf", "İyiliği emredip kötülüğü yasaklama ilkesi; Mihne'de devlet aparatına dönüşmüştür.", "Usûl-i Hamse", 3),
        Concept("Ta'rîb", "Abdülmelik b. Mervân'ın Arapçalaştırma politikası; Mevâlî üzerinde baskı kurmuştur.", "Emevî siyaseti", 4),
        Concept("Mevâlî", "Arap kökenli olmayan Müslümanlar; Abbâsî ihtilalinin ve Me'mûn'un temel desteği.", "Siyasi arka plan", 4),
        Concept("Ehl-i Bid'at", "Ana gövdeyi temsil eden Ehl-i Sünnet'in karşısında aşırılıkları temsil eden gruplar.", "İlmî arka plan", 4),
        Concept("Kesb", "Fiili Allah'ın yarattığı, kulun iradesiyle seçip kazandığı formül.", "Eş'arî", 4),
        Concept("Vücûb alellah", "Allah'a bir şeyin vacip olması nazariyesi; Eş'arî bunu reddeder.", "Eş'arî", 4),
        Concept("Mütekaddimûn", "Eş'arî'den Gazzâlî'ye uzanan iki yüzyıllık başlangıç ve sistemleşme evresi.", "Dönemlendirme", 5),
        Concept("Kıyâsü'l-gâib ale'ş-şâhid", "Duyu ötesini duyulur âlemle karşılaştırarak ilâhî sıfatları anlama yöntemi.", "İstidlâl", 5),
        Concept("Sebr ve Taksîm", "İhtimalleri tartışıp eleyerek karşı iddiaları çürütme usulü.", "İstidlâl", 5),
        Concept("İn'ikâsü'l-edille", "Delil çürürse medlûlün de çürüdüğü ilkesi; Bâkıllânî kurar, Cüveynî yıkar.", "İstidlâl", 5),
        Concept("Âdet Teorisi", "Tabiattaki düzenin zorunlu değil, Allah'ın iradesine bağlı bir alışkanlık olması.", "Bâkıllânî", 5),
        Concept("Nizâmiyye Medreseleri", "Nizâmülmülk'ün kurduğu, Eş'arîliği devlet destekli ekole dönüştüren medrese ağı.", "Selçuklu siyaseti", 5),
        Concept("Ba's-ı Cismânî", "Dirilişin ruhla birlikte bedenle de gerçekleşmesi.", "Ortak inanç esası", 5),
        Concept("Müteahhirûn", "Gazzâlî'yle başlayan felsefi kelâm dönemi (VI/XII. asır ve sonrası).", "Dönemlendirme", 6),
        Concept("İlliyet", "Zorunlu nedensellik; Gazzâlî bunu reddeder.", "Gazzâlî", 6),
        Concept("Sıfât-ı Meânî", "Allah'ın zâtına ekli, ne aynı ne gayrı olan ezelî sıfatlar.", "Eş'arî sıfat anlayışı", 6),
        Concept("İhkâm ve İtkân", "Râzî'nin isbât-ı vâcibde hudûs yerine öne çıkardığı gaye ve nizam delili.", "Fahreddin er-Râzî", 6),
        Concept("Lafzî ve Nefsî Kelâm", "Râzî'nin ayrımı: lafzî kelâm hâdis, nefsî kelâm kadîmdir.", "Fahreddin er-Râzî", 6),
        Concept("Ehl-i Kıble", "Namaz kılan ve temel esaslara inananlar; te'vil farkıyla tekfir edilemezler.", "Eş'arî görüşleri", 6),
        Concept("Mâverâünnehir", "Ceyhun nehrinin ötesi; Sâmânîler yönetimindeki ilim ve kültür merkezi.", "Mâtürîdîliğin coğrafyası", 7),
        Concept("Dârü'l-Cüzcâniyye", "Hanefîliğin Semerkand'daki kurumsal merkezi; Mâtürîdî burada yetişmiştir.", "Semerkand ekolü", 7),
        Concept("Re'y", "Hanefîliğin akla ve içtihada verdiği önem; Mâtürîdî kelâmının kaynağı.", "Hanefî etkisi", 7),
        Concept("Cüzcâniyye ve İyâziyye", "Mâtürîdîliğin ilk dönemlerde kurucu hocalara nispetle anıldığı adlar.", "Ekolleşme", 7),
        Concept("Tebsıratü'l-edille", "Nesefî'nin eseri; Mâtürîdîliği müstakil mezhep olarak tescilleyen kırılma.", "Ebü'l-Muîn en-Nesefî", 7),
        Concept("'Iyân (Duyular)", "Mâtürîdî'nin birinci bilgi kaynağı; beş duyu, iç duyular ve içgüdüler.", "Bilgi teorisi", 8),
        Concept("İstidlâl", "Duyu ve haber verilerini ölçen hakem mekanizması; üçüncü bilgi kaynağı.", "Bilgi teorisi", 8),
        Concept("Mütevatir Haber", "Yalan üzerine birleşmeleri imkânsız kişilerce nakledilen, kesinlik ifade eden haber.", "Bilgi teorisi", 8),
        Concept("Âhâd Haber", "Zan ifade eden haber; itikatta değil, yalnızca amelî konularda kullanılabilir.", "Bilgi teorisi", 8),
        Concept("Temânu' Delili", "Birden fazla ilah olsaydı iradeler çatışır ve düzen bozulurdu delili.", "Ulûhiyet", 8),
        Concept("Tekvin", "Allah'ın yaratma sıfatı; Mâtürîdîlere göre zâta ekli ezelî ve müstakil bir sıfat.", "Ulûhiyet", 8),
        Concept("Cüz'î İrade", "İnsanın zihnî bir fonksiyon olan seçme gücü; Allah'ın yaratmasına konu değildir.", "İnsan fiilleri", 8),
        Concept("İsmet", "Peygamberlerin günah işlemekten korunmuş olmaları.", "Nübüvvet", 8),
        Concept("Marifetullah", "Allah'ı bilmek; Mâtürîdî'de aklen farz, Eş'arî'de şeriatla mükellefiyet doğar.", "İhtilaflar", 9),
        Concept("Azm-i Musammam", "Mâtürîdîlerin kesb tanımı: kesin kararlılık.", "İhtilaflar", 9),
        Concept("İktirân", "Eş'arî kesb tanımı: kudretin makdûra bitişmesi; icatta tesir yoktur.", "İhtilaflar", 9),
        Concept("İtibar Hâtimeyedir", "Eş'arîlere göre hükmün son nefese göre verilmesi ilkesi.", "İhtilaflar", 9),
    ]

    # =====================================================================
    # TEST — 20 Soruluk Genel Değerlendirme
    # =====================================================================
    test_questions = [
        TestQuestion(1, "Hasan-ı Basrî'nin ders halkasında büyük günah işleyenin durumu sorulduğunda \"ne mümin ne kâfir, o fâsıktır\" diyerek meclisten ayrılan ve Mu'tezile'nin kurucusu sayılan isim kimdir?",
            {"A": "Amr b. Ubeyd", "B": "Vâsıl b. Atâ", "C": "Ebü'l-Hüzeyl el-Allâf", "D": "Katâde b. Diâme", "E": "Bişr b. Mu'temir"}),
        TestQuestion(2, "Mu'tezile'ye \"Seneviyye — Mecûsîler\" isminin verilme sebebi aşağıdakilerden hangisidir?",
            {"A": "Rü'yetullahı inkâr etmeleri", "B": "Kur'an'ın yaratılmışlığını savunmaları",
             "C": "\"Hayrın fâili Allah, şerrin fâili insandır\" demeleri", "D": "Büyük günahkârı ebedî cehennemlik saymaları",
             "E": "Zâttan ayrı kadîm sıfatları reddetmeleri"}),
        TestQuestion(3, "Mu'tezile'nin beş temel esasını (Usûl-i Hamse) ilk defa kavramsallaştırıp bir inanç sistemi hâline getiren, Basra ekolünün sistematik kurucusu kimdir?",
            {"A": "Vâsıl b. Atâ", "B": "Nazzâm", "C": "Ebü'l-Hüzeyl el-Allâf", "D": "Kâdî Abdülcebbâr", "E": "Câhiz"}),
        TestQuestion(4, "Mihne dönemiyle ilgili aşağıdakilerden hangisi yanlıştır?",
            {"A": "Me'mûn döneminde başlamış, Mu'tasım ve Vâsık dönemlerinde devam etmiştir",
             "B": "Baş kadı Ahmed b. Ebî Duâd'ın teşvikiyle yürütülmüştür",
             "C": "Ulemaya Halku'l-Kur'an tezi dayatılmıştır",
             "D": "Ahmed b. Hanbel bu dönemde kırbaçlanıp zindana atılmıştır",
             "E": "Halife Mütevekkil tarafından başlatılmıştır"}),
        TestQuestion(5, "Basra ve Bağdat ekollerinin farklarını inceleyen ve aralarında 155 görüş ayrılığı tespit eden eser ile müellifi hangi seçenekte doğru verilmiştir?",
            {"A": "el-Muğnî — Kâdî Abdülcebbâr", "B": "el-Mesâ'il fi'l-hilâf — Ebû Reşîd en-Nîsâbûrî",
             "C": "Kitâbü'l-İntisâr — Ebü'l-Hüseyin el-Hayyât", "D": "Tabakâtu'l-Mu'tezile — İbnü'l-Murtazâ",
             "E": "Makâlâtü'l-İslâmiyyîn — Ebü'l-Hasan el-Eş'arî"}),
        TestQuestion(6, "Kur'an'ın benzerinin getirilememesini, Allah'ın Arapların buna güç yetirme kabiliyetini ellerinden alarak onları âciz bırakmasıyla açıklayan teori hangisidir?",
            {"A": "Tafra", "B": "Kümûn-Zuhûr", "C": "Sarfe", "D": "Tevellüd", "E": "Ahvâl"}),
        TestQuestion(7, "Allah'ın sıfatlarını, \"ne mevcûd ne ma'dûm, ne kadîm ne hâdis olan hâller\" şeklinde açıklayan Ahvâl teorisinin sahibi kimdir?",
            {"A": "Ebû Ali el-Cübbâî", "B": "Ebû Hâşim el-Cübbâî", "C": "Nazzâm", "D": "Sümâme b. Eşres", "E": "el-Ka'bî"}),
        TestQuestion(8, "Basra ve Bağdat ekolleri arasındaki fark ile ilgili aşağıdaki ifadelerden hangisi doğrudur?",
            {"A": "Basra imâmeti aslah kapsamında zorunlu görür", "B": "Bağdat sahâbe üstünlüğünü kronolojik hilafet sırasına göre belirler",
             "C": "Basra siyasetle iç içe, devlet kademelerinde aktiftir", "D": "Bağdat'a göre Hz. Peygamber'den sonra en faziletli Hz. Ali'dir",
             "E": "İki ekol beş esas üzerinde de ihtilaf hâlindedir"}),
        TestQuestion(9, "Mu'tezile'nin Tevhîd ilkesiyle ilgili aşağıdakilerden hangisi söylenemez?",
            {"A": "Zâttan ayrı kadîm sıfatlar teaddüd-i kudemâya yol açtığı için reddedilir",
             "B": "Allah'ın kelâmı harf ve seslerden oluştuğu için mahlûktur",
             "C": "Allah zâtından ayrı bir ilimle değil, bizzat zâtıyla âlimdir",
             "D": "Rü'yetullah yön ve mekân gerektirdiği için aklen imkânsızdır",
             "E": "Haberî sıfatlar Allah'ın şanına uygun olarak te'vil edilir"}),
        TestQuestion(10, "Mu'tezile'nin şefaat anlayışı aşağıdakilerden hangisidir?",
            {"A": "Şefaat tamamen kabul edilir ve büyük günahkârlar cehennemden çıkarılır",
             "B": "Şefaat yalnızca cennettekilerin makamlarının yükseltilmesi olarak kabul edilir",
             "C": "Şefaat sadece peygamberler için geçerlidir", "D": "Şefaat konusu âhâd hadislerle sabittir ve delildir",
             "E": "Şefaat, mizan ve sırat gibi zâhirî anlamıyla kabul edilir"}),
        TestQuestion(11, "Büyük günah işleyenin statüsü konusunda \"Münafık\" görüşünü savunan isim kimdir?",
            {"A": "Vâsıl b. Atâ", "B": "Hasan-ı Basrî", "C": "Amr b. Ubeyd", "D": "Ebû Hanîfe", "E": "Ahmed b. Hanbel"}),
        TestQuestion(12, "Ebü'l-Hasan el-Eş'arî'nin Mu'tezile'den ayrılmasının iki temel gerekçesi aşağıdakilerden hangisinde birlikte verilmiştir?",
            {"A": "Halku'l-Kur'an ve şefaatin reddi", "B": "Aslah teorisi ve emir bi'l-ma'rûf",
             "C": "Rü'yetullah'ın inkârı ve kulun kendi fiilini yaratması", "D": "Teaddüd-i kudemâ ve hüsün-kubuh",
             "E": "Tafra teorisi ve ahvâl teorisi"}),
        TestQuestion(13, "Eş'arî'nin Mu'tezile'yi terk ettikten sonra Hanbelîlerin lideri Berbahârî tarafından reddedilmesinin sebebi nedir?",
            {"A": "Mu'tezilî inançlarını tamamen terk etmemiş olması", "B": "Şâfiî mezhebine geçmiş olması",
             "C": "Kelâm (akıl/istidlâl) yöntemini kullanmaya devam etmesi", "D": "Rü'yetullahı hâlâ reddetmesi",
             "E": "Halku'l-Kur'an tezini savunmayı sürdürmesi"}),
        TestQuestion(14, "Eş'arî'nin, Mu'tezile'den ilk ayrıldığı ve zihninin netleşmediği dönemde Selefiyye'ye yaranmak için yazdığı, Selefî izler taşıyan eseri hangisidir?",
            {"A": "Kitâbü'l-Luma'", "B": "el-İbâne an usûli'd-diyâne", "C": "Makâlâtü'l-İslâmiyyîn",
             "D": "Risâle ilâ ehli's-sağr", "E": "Risâle fî istihsâni'l-havz fî ilmi'l-kelâm"}),
        TestQuestion(15, "Bâkıllânî'nin geliştirdiği, \"bir delil çürütülürse o delilin ispatladığı inanç da çürütülmüş olur\" prensibi ve bu prensibi reddeden âlim hangi seçenekte doğru eşleştirilmiştir?",
            {"A": "Âdet Teorisi — Gazzâlî", "B": "Kıyâsü'l-gâib — İbn Fûrek", "C": "İn'ikâsü'l-edille — Cüveynî",
             "D": "Sebr ve Taksîm — İsferâyînî", "E": "Ahvâl Teorisi — Abdülkâhir el-Bağdâdî"}),
        TestQuestion(16, "Diğer Eş'arîlerin aksine ilhamı dördüncü bir bilgi kaynağı olarak kabul eden ve el-Fark beyne'l-fırak adlı eserin sahibi olan kelâmcı kimdir?",
            {"A": "İbn Fûrek", "B": "Ebû İshak el-İsferâyînî", "C": "Abdülkâhir el-Bağdâdî", "D": "Bâkıllânî", "E": "Şehristânî"}),
        TestQuestion(17, "Mütekaddimûn ve Müteahhirûn dönemlerinin karşılaştırılmasıyla ilgili aşağıdakilerden hangisi yanlıştır?",
            {"A": "Mütekaddimûn'da varlık anlayışı atomculuk (cevher/araz) temellidir",
             "B": "Müteahhirûn'da klasik Aristo mantığı kullanılır",
             "C": "Müteahhirûn'un temel muhatabı filozoflar ve Bâtınîlerdir",
             "D": "Mütekaddimûn'un temel disiplini küllî ilim ve felsefe eksenlidir",
             "E": "Müteahhirûn'da varlık anlayışı vâcip-mümkün ve varlık-mahiyet ayrımına dayanır"}),
        TestQuestion(18, "İsbât-ı vâcib konusunda hudûs delili yerine \"ihkâm ve itkân\" (gaye ve nizam) delilini merkeze alan ve Allah'ın kelâmını Lafzî-Nefsî olarak ikiye ayıran kelâmcı kimdir?",
            {"A": "Gazzâlî", "B": "Fahreddin er-Râzî", "C": "Seyfüddîn el-Âmidî", "D": "Kâdî Beyzâvî", "E": "Adûddîn el-Îcî"}),
        TestQuestion(19, "Mâtürîdîliğin, Hanefîliğin fıkıh gölgesinden çıkarak müstakil bir kelâm mezhebi olarak tescillenmesini sağlayan âlim ve eseri hangi seçenekte doğru verilmiştir?",
            {"A": "Ebû Ca'fer et-Tahâvî — el-Akîdetü't-Tahâviyye", "B": "Ebû Süleyman el-Cüzcânî — Dârü'l-Cüzcâniyye",
             "C": "Ebü'l-Muîn en-Nesefî — Tebsıratü'l-edille", "D": "Ebû Nasr el-İyâzî — İyâziyye",
             "E": "İmam Muhammed eş-Şeybânî — Kitâbü't-Tevhîd"}),
        TestQuestion(20, "Eş'arîlik ile Mâtürîdîlik arasındaki farklarla ilgili aşağıdakilerden hangisi doğrudur?",
            {"A": "Mâtürîdîlere göre teklif-i mâ lâ yutak aklen caiz ve mümkündür",
             "B": "Eş'arîlere göre Tekvin, kudretten ayrı ezelî ve müstakil bir sıfattır",
             "C": "Mâtürîdîlere göre iman artar ve eksilir",
             "D": "Mâtürîdîlere göre vahiy gelmese dahi aklın Allah'ın varlığını bulması farzdır",
             "E": "Eş'arîlere göre \"İnşallah müminim\" demek caiz değildir"}),
    ]

    answer_key_items = [
        AnswerItem(1, "B", "<b>Vâsıl b. Atâ</b>, \"ne mümin ne kâfir; o kişi <b>fâsık</b>tır\" tezini ortaya koyup meclisten ayrılmıştır."),
        AnswerItem(2, "C", "\"Hayrın fâili Allah, şerrin fâili insandır\" dedikleri için <b>düalist (seneviyye)</b> inançlara benzetilmişlerdir."),
        AnswerItem(3, "C", "Beş esası ilk defa kavramsallaştırıp inanç sistemi hâline getiren asıl mimar <b>Ebü'l-Hüzeyl el-Allâf</b>'tır."),
        AnswerItem(4, "E", "Mütevekkil Mihne'yi başlatmamış, <b>bitirmiştir</b>; <b>Karşı-Mihne</b>'yi başlatan odur."),
        AnswerItem(5, "B", "<b>Ebû Reşîd en-Nîsâbûrî</b>'nin <b>el-Mesâ'il fi'l-hilâf</b> adlı eserinde tam <b>155</b> görüş ayrılığı tespit edilmiştir."),
        AnswerItem(6, "C", "<b>Sarfe</b> Nazzâm'a aittir: sebep lafzî üstünlük değil, Allah'ın Arapları <b>âciz bırakmasıdır</b>."),
        AnswerItem(7, "B", "<b>Ebû Hâşim el-Cübbâî</b>, teaddüd-i kudemâyı aşmak için sıfatları <b>hâller</b> olarak tanımlamıştır."),
        AnswerItem(8, "D", "Bağdat'a göre en faziletli, Hz. Peygamber'den sonra doğrudan <b>Hz. Ali</b>'dir; kronolojik sıra Basra'ya aittir."),
        AnswerItem(9, "E", "Haberî sıfatların <b>te'vil edilmesi Eş'arîliğin</b> görüşüdür; Mu'tezile teşbih-tecsîmi doğrudan şirk sayar."),
        AnswerItem(10, "B", "Vaîdden dönmeyi adaletsizlik saydıkları için şefaati yalnızca <b>cennettekilerin makamlarının yükseltilmesi</b> olarak kabul ederler."),
        AnswerItem(11, "B", "<b>Hasan-ı Basrî</b> <b>münafık</b>; Hâricîler kâfir, Mürcie mümin, Vâsıl ise fâsık demiştir."),
        AnswerItem(12, "C", "İki temel gerekçe <b>rü'yetullahın inkârı</b> ve <b>kulun kendi fiilini yaratması</b> meseleleridir."),
        AnswerItem(13, "C", "İnançları terk etse de <b>kelâm yöntemini</b> sürdürdüğü için reddedilmiş; ona Şâfiî <b>Ebû İshak el-Mervezî</b> sahip çıkmıştır."),
        AnswerItem(14, "B", "<b>el-İbâne</b> Selefiyye'ye yaranmak için yazılan, Selefî izler taşıyan eserdir; Kitâbü'l-Luma' ise mezhebin omurgasıdır."),
        AnswerItem(15, "C", "<b>İn'ikâsü'l-edille</b> Bâkıllânî'ye aittir; <b>Cüveynî</b> kelâmı çıkmaza soktuğu gerekçesiyle bu kuralı reddetmiştir."),
        AnswerItem(16, "C", "<b>Abdülkâhir el-Bağdâdî</b>, diğerlerinin aksine ilhamı dördüncü bilgi kaynağı sayar."),
        AnswerItem(17, "D", "Küllî ilim ve <b>felsefe eksenli</b> olan Müteahhirûn'dur; Mütekaddimûn usûlü'd-dîn ve fıkıh eksenlidir."),
        AnswerItem(18, "B", "<b>Fahreddin er-Râzî</b>, <b>ihkâm ve itkân</b> delilini merkeze almış, kelâmı <b>Lafzî</b> ve <b>Nefsî</b> olarak ayırmıştır."),
        AnswerItem(19, "C", "<b>Nesefî</b>'nin <b>Tebsıratü'l-edille</b>'si, Mâtürîdîliğin müstakil mezhep olmasını sağlayan kırılma noktasıdır."),
        AnswerItem(20, "D", "Mâtürîdî'ye göre <b>marifetullah</b> vahiy gelmese dahi aklen farzdır; diğer şıklar iki mezhep arasında yer değiştirmiştir."),
    ]

    return CoursePack(
        ders_klasoru="KELÂM TARİHİ",
        course_code="KELÂM TARİHİ",
        title='Kelâm<span class="accent-word"> Tarihi</span>',
        subtitle="Mu'tezile'den Eş'arîliğe ve Mâtürîdîliğe: İslâm Düşüncesinde Akıl-Nakil Mücadelesi",
        description=(
            "Kur'ân'ın akletmeyi emreden ilkesiyle yola çıkan kelâm âlimlerinin, Emevî ve Abbâsî siyasetinin "
            "gölgesinde İslâm'ı savunma çabası; rasyonalist teolojinin zirvesi Mu'tezile'nin doğuşundan "
            "Eş'arîliğin dengeleyici sistemine ve Mâtürîdîliğin akıl-nakil sentezine uzanan tarihsel ve "
            "teolojik çatışmaların kaynaklar ışığında final sınavı özeti."
        ),
        theme="plum",
        theme_color="#4A2E7A",
        icon_text="K",
        chapters=chapters,
        glossary=glossary,
        test_title="Genel Değerlendirme Testi",
        test_subtitle="Mu'tezile'nin doğuşundan Eş'arî-Mâtürîdî ihtilaflarına, Kelâm Tarihi üzerine kapsamlı çoktan seçmeli test",
        test_instructions="Aşağıdaki sorularda beş seçenekten yalnızca birini işaretleyiniz. Süre: 30 dakika.",
        test_questions=test_questions,
        answer_key_intro="Her sorunun doğru cevabı ve kısa gerekçesi aşağıda yer almaktadır.",
        answer_key_items=answer_key_items,
        overview_lead=(
            "Bu ders; <b>Mu'tezile</b>'nin bir mescit tartışmasından doğup devletin resmî ideolojisi hâline "
            "gelişini ve Mihne'yle birlikte çöküşünü, ardından <b>Eş'arîliğin</b> iki kutuplaşma arasında "
            "kurduğu \"orta yolu\" ve Gazzâlî'yle felsefi kelâma dönüşümünü, nihayet Semerkand'da doğan "
            "<b>Mâtürîdîliğin</b> akıl-nakil sentezini ve iki Sünnî ekol arasındaki ihtilafları bir bütün "
            "olarak sunar."
        ),
        overview_cards=[
            {"title": "Mu'tezile'nin Doğuşu", "text": "İ'tizâl hadisesinden Usûl-i Hamse'ye; Me'mûn'un altın çağından Mihne'ye ve Karşı-Mihne'yle silinişe."},
            {"title": "Basra ve Bağdat", "text": "Teorik akademisyenlerle saray kelâmcılarının 155 meselede ayrıştığı iki kanat."},
            {"title": "Usûl-i Hamse", "text": "Tevhîd, Adâlet, Va'd-Vaîd, el-Menzile beyne'l-menzileteyn ve Emir bi'l-ma'rûf."},
            {"title": "Eş'arî'nin Dönüşümü", "text": "Kırk yaşında i'tizâlden ayrılış, Berbahârî'nin reddi ve Kesb teorisiyle kurulan denge."},
            {"title": "Mütekaddimûn — Müteahhirûn", "text": "Bâkıllânî'nin atomculuğundan Gazzâlî'nin Tehâfüt'üne, kelâmın varlık felsefesine dönüşümü."},
            {"title": "Mâtürîdîlik ve İhtilaflar", "text": "Semerkand'ın akıl-nakil sentezi ve Eş'arîlikle arasındaki kudret-hikmet ayrımı."},
        ],
        overview_flow=[
            ("Mu'tezile", "Doğuş, Usûl-i Hamse ve Mihne"),
            ("Eş'arîlik", "Orta yol ve Kesb teorisi"),
            ("Mütekaddimûn", "Bâkıllânî'den Cüveynî'ye"),
            ("Müteahhirûn", "Gazzâlî ve felsefi kelâm"),
            ("Mâtürîdîlik", "Akıl-nakil sentezi ve ihtilaflar"),
        ],
        overview_note=(
            "Sınavda en çok karıştırılan yer, <b>Eş'arîlik ile Mâtürîdîliğin kazâ-kader tanımlarını tam zıt "
            "(yer değiştirmiş) anlamlarda kullanmasıdır</b>. İkinci kritik nokta ise aynı kavramın üç ekolde "
            "farklı karşılık bulmasıdır: <b>kesb</b> Eş'arî'de kudretin makdûra bitişmesi, Mâtürîdî'de "
            "azm-i musammam, Mu'tezile'de ise hiç yoktur — çünkü orada fiili doğrudan <b>insan yaratır</b>."
        ),
    )
