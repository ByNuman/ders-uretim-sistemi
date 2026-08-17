# -*- coding: utf-8 -*-
"""ÇAĞDAŞ FELSEFE — Görsel Ders Notu Kitabı, içerik tanımı.
Kaynak: 'Felsefe Tarihi Öğretmen Notları.pdf' (öğretmenin toparlanmış çalışma
rehberi, 18 sayfa, 10 bölüm — Comte'tan Marx'a çağdaş felsefe tarihi).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from content_model import (
    Person, KeyTerm, Callout, FlowStep, FlowDiagram, ComparisonTable,
    InfoCard, BulletBlock, Chapter, ChapterPage, Concept, CoursePack,
    QAItem, DistinctionPair, MatchRow, TestQuestion, AnswerItem,
)

COMTE = Person(
    id="comte", name="Auguste Comte", years="1798–1857",
    tagline="Pozitivizmin Kurucusu, Sosyoloji Biliminin İsim Babası",
    bio=["Katolik bir ailede yetişmiş, 14 yaşında kiliseden ayrılmış; Politeknik Okulu'nda okuduktan sonra "
         "<b>Saint-Simon</b>'un yanında 7 yıl sekreterlik yaparak yetişmiş, başyapıtı <b>Olgusal (Pozitif) "
         "Felsefe Dersleri</b>'nde bilimi tek geçerli bilgi sistemi ilan etmiştir."],
    key_work="Olgusal (Pozitif) Felsefe Dersleri",
)
SCHOPENHAUER = Person(
    id="schopenhauer", name="Arthur Schopenhauer", years="1788–1860",
    tagline="Kötümser İrade Felsefesinin Kurucusu",
    bio=["Başyapıtı <b>İsteme ve Tasarım Olarak Dünya</b>'da evrenin ve insanın temelinde doyumsuz, amaçsız "
         "bir 'irade' (Wille) bulunduğunu; mutluluğun ise pozitif bir durum değil yalnızca acının yokluğu "
         "('negatif hedonizm') olduğunu savunarak yaşamı köklü bir kötümserlikle yorumlamıştır."],
    key_work="İsteme ve Tasarım Olarak Dünya",
)
DARWIN = Person(
    id="darwin", name="Charles Darwin", years="1809–1882",
    tagline="Doğal Seçilim Yoluyla Evrim Teorisinin Kurucusu",
    bio=["HMS Beagle gemisiyle 22 yaşında çıktığı ve 5 yıl süren dünya turunda, özellikle Galapagos "
         "Adaları'nda topladığı kanıtlarla türlerin ortak bir atadan <b>Doğal Seçilim</b> yoluyla "
         "evrimleştiğini, başyapıtı <b>İnsanın Türeyişi</b>'nde ortaya koymuştur."],
    key_work="İnsanın Türeyişi",
)
FREUD = Person(
    id="freud", name="Sigmund Freud", years="1856–1939",
    tagline="Psikanalizin (Ruhçözümlemenin) Kurucusu",
    bio=["Davranışlarımızın çoğu zaman akıl değil bilinçdışı, akıl dışı dürtüler tarafından yönetildiğini "
         "savunmuş; zihni İd-Ego-Süperego üçlüsüyle modelleyip <b>Rüyaların Yorumu</b> ile bilinçdışına "
         "ulaşmanın yollarını ('ruh arkeolojisi') sistemleştirmiştir."],
    key_work="Rüyaların Yorumu",
)
RUSSELL = Person(
    id="russell", name="Bertrand Russell", years="1872–1970",
    tagline="Modern Analitik Felsefenin Kurucularından, Hümanist Filozof",
    bio=["G. E. Moore ile birlikte modern analitik felsefenin kurucularından biridir; Whitehead ile yazdığı "
         "<b>Principia Mathematica</b> ile matematiği mantığa indirgemeye çalışmış, 1949'da Liyakat Nişanı, "
         "1950'de ise insan hakları ve özgür düşünce üzerine yazdığı yazılar nedeniyle Nobel Edebiyat "
         "Ödülü'nü kazanmıştır."],
    key_work="Principia Mathematica",
)
KIERKEGAARD = Person(
    id="kierkegaard", name="Søren Kierkegaard", years="1813–1855",
    tagline="Varoluşçuluğun Öncüsü, 'İman Şövalyesi' Kavramının Sahibi",
    bio=["Doğruyu 'nesnel' ve 'öznel' olarak ikiye ayırıp inanan insan için öznel doğrunun (Tanrı inancının) "
         "her zaman üstün olduğunu savunmuş; insanın estetik, etik ve dinsel aşamalardan geçip akla değil "
         "'İnanç Sıçraması'na dayanan bir 'İman Şövalyesi' olması gerektiğini öne sürmüştür."],
    key_work="Korku ve Titreme",
)
HUSSERL = Person(
    id="husserl", name="Edmund Husserl", years="1859–1938",
    tagline="Fenomenolojinin Kurucusu",
    bio=["Felsefenin görevinin nesnelerin bilince nasıl göründüğünü, yani deneyimin özünü incelemek olduğunu "
         "savunmuş; kesin bilgiye ancak önyargılardan sıyrılıp yalnızca bilincin deneyimine odaklanan "
         "<b>Fenomenolojik İndirgeme</b> yöntemiyle ulaşılabileceğini öne sürmüştür."],
    key_work="Mantıksal Araştırmalar",
)
HEIDEGGER = Person(
    id="heidegger", name="Martin Heidegger", years="1889–1976",
    tagline="'Dasein' Kavramıyla Varlığı Sorgulayan Filozof",
    bio=["Husserl'in öğrencisi olarak fenomenolojiyi Husserl'den farklı biçimde, varlık sorusunu merkeze "
         "alarak yeniden şekillendirmiş; insanın dünyada 'orada-varlık' (<b>Dasein</b>) olarak bulunduğunu, "
         "varoluşun ancak zaman, ölüm ve kaygı üzerinden çözümlenebileceğini savunmuştur."],
    key_work="Varlık ve Zaman",
)
SARTRE = Person(
    id="sartre", name="Jean-Paul Sartre", years="1905–1980",
    tagline="'Önce Varoluş, Sonra Öz' İlkesinin Sahibi",
    bio=["'İnsan önce var olur, sonra kendi özünü kendi eylemleriyle oluşturur' ilkesiyle insanın tamamen "
         "özgür ve bu özgürlükten sorumlu olduğunu savunmuş; özgürlükten ve onun getirdiği sorumluluktan "
         "kaçma çabasına <b>'kötü niyet' (mauvaise foi)</b> adını vermiştir."],
    key_work="Varlık ve Hiçlik",
)
CAMUS = Person(
    id="camus", name="Albert Camus", years="1913–1960",
    tagline="Absürdizm ve Sisifos Miti",
    bio=["Varoluşçuluğa 'absürdizm' kavramını katmış; insanın anlam arayışı ile evrenin sessizliği "
         "arasındaki uyumsuzluğu 'absürt' olarak tanımlamış, bu absürtlüğe rağmen insanın hayatı "
         "anlamlandırmaya ve mücadeleyi sürdürmeye devam etmesi gerektiğini <b>Sisifos Miti</b> ile "
         "simgeleştirmiştir."],
    key_work="Sisifos Söyleni",
)
NIETZSCHE = Person(
    id="nietzsche", name="Friedrich Nietzsche", years="1844–1900",
    tagline="'Tanrı Öldü' Diyen Yaşam Filozofu",
    bio=["13 yaşında kötülük sorunu üzerine düşünmeye başlamış, Schopenhauer'in <b>İsteme ve Tasarım Olarak "
         "Dünya</b> kitabından derinden etkilenmiş; felsefesinin özü eleştiridir — Kant, Hegel, Schopenhauer, "
         "Katolik Hristiyanlığı ve Avrupa kültürünün yürürlükteki tüm değerlerini sertçe eleştirmiştir."],
    key_work="Güç İstenci",
)
BENTHAM = Person(
    id="bentham", name="Jeremy Bentham", years="1748–1832",
    tagline="Klasik (Niceliksel) Faydacılığın Kurucusu",
    bio=["İngiliz filozof, hukukçu ve sosyal reformcu; 'en büyük mutluluk ilkesi'ni savunarak eylemlerin "
         "ahlaki değerinin sonuçlarının yarattığı ölçülebilir haz/acı dengesiyle belirlendiğini iddia etmiş, "
         "gözetim mimarisi <b>Panoptikon</b>'u tasarlamıştır."],
    key_work="Panoptikon (mimari tasarım)",
)
MILL = Person(
    id="mill", name="John Stuart Mill", years="1806–1873",
    tagline="Özgürlükçü (Liberal) Faydacılığın Öncüsü",
    bio=["İngiliz filozof, ekonomist ve siyasetçi; Bentham'ın faydacılığını 'hazlar arasında nitelik farkı "
         "vardır (zihinsel hazlar bedensel hazlardan üstündür)' ilkesiyle geliştirmiş, <b>Özgürlük "
         "Üzerine</b>'de bireysel özgürlüğü, <b>Kadınların Boyunduruk Altında</b>'da toplumsal cinsiyet "
         "eşitliğini savunmuştur."],
    key_work="Özgürlük Üzerine",
)
MARX = Person(
    id="marx", name="Karl Marx", years="1818–1883",
    tagline="Tarihsel ve Diyalektik Maddeciliğin Kurucusu",
    bio=["Toplumu, maddi/ekonomik ilişkilerden oluşan 'alt yapı' ile siyaset, hukuk, din ve felsefeden oluşan "
         "'üst yapı' arasındaki çatışma üzerinden açıklamış; Friedrich Engels ile birlikte yayımladığı "
         "<b>Komünist Manifesto</b>'da proletarya diktatörlüğü yoluyla sınıfsız bir düzen hedeflemiştir."],
    key_work="Komünist Manifesto",
)


def get_pack() -> CoursePack:

    # =====================================================================
    # BÖLÜM 1 — Auguste Comte ve Schopenhauer: Pozitivizm ve Kötümser Felsefe
    # =====================================================================
    ch1 = Chapter(
        number=1,
        title="Pozitivizm ve Kötümser Felsefe",
        subtitle="Comte'un bilim temelli iyimserliğinden Schopenhauer'ın irade kötümserliğine",
        key_terms=[
            KeyTerm("Pozitivizm", "Bilginin yalnızca gözlem, deney ve bilimsel yöntemle elde edilebileceğini savunan görüş."),
            KeyTerm("Üç Hal Yasası", "Comte'un insan düşüncesinin tarihsel gelişimini teolojik–metafizik–pozitif üç aşamada açıkladığı yasa."),
            KeyTerm("İnsanlık Dini", "Comte'un, toplumu bilim etrafında birleştirmek için önerdiği, tanrısız ama dinsel biçimde örgütlenmiş ahlaki sistem."),
            KeyTerm("İrade (Wille)", "Schopenhauer'e göre evrenin ve insanın temelinde yatan, doyumsuz, amaçsız itki."),
        ],
    )
    ch1.pages.append(
        ChapterPage()
        .add_terms(ch1.key_terms)
        .add_person(COMTE)
        .add_block(BulletBlock(1, "Hayatı ve Entelektüel Kökleri", [
            "Katolik bir ailede yetişmiş; 14 yaşında kiliseden ayrılmış, bu ailesinin büyük tepkisini çekmiştir.",
            "Politeknik Okulu'nda (École Polytechnique) okumuş; pozitivizmin kurucusu sayılan Saint-Simon ile "
            "tanışıp yanında 7 yıl boyunca asistanlık ve sekreterlik yapmıştır.",
            "<b>Montesquieu, Kant ve Hume</b>'un düşünceleri, Comte'un fikirlerini şekillendiren başlıca "
            "etkiler arasında sayılır.",
            "Felsefi sisteminin mottosu: <b>'İlke olarak aşk, temel olarak düzen, amaç olarak ilerleme.'</b>",
        ]))
        .add_callout(Callout("caution", "Notlardaki Bir Hata: Doğum Yılı",
            "Öğretmenin ham dikte notlarında Comte'un doğum yılı yanlışlıkla '1989 – Fransa' olarak "
            "geçmişti; bu, Comte'un 1857'de öldüğü bilgisiyle çelişir (1989 kronolojik olarak imkânsızdır). "
            "Doğrusu <b>1798'dir</b> ve bu kitapta düzeltilmiş haliyle kullanılmıştır."))
    )
    ch1.pages.append(
        ChapterPage(continue_tag="Üç Hal Yasası, İnsanlık Dini ve Schopenhauer")
        .add_flow(FlowDiagram([
            FlowStep("Teolojik Aşama", "Her şey Tanrı/tanrısal güçlerle açıklanır"),
            FlowStep("Metafizik Aşama", "Tanrılar devre dışıdır; hak, hukuk, eşitlik gibi soyut kavramlarla açıklanır"),
            FlowStep("Pozitif Aşama", "Bilimsel yöntem ve doğrulanabilir teorilerle açıklanır"),
        ], caption="Comte'un Üç Hal Yasası: İnsan Düşüncesinin Tarihsel Gelişimi"))
        .add_block(BulletBlock(2, "İnsanlık Dini", [
            "Comte, topluma faydalı ve çağın ruhuna uygun bir din geliştirilmesi gerektiğini savunmuş, buna "
            "<b>'İnsanlık Dini'</b> adını vermiştir: 'Benim dinim, insanları bilimle aydınlatan bir dindir.'",
            "Bu dinin ibadethaneleri üniversiteler, din adamları ise bilim insanlarıdır; Yüce Varlık, Büyük "
            "Fetiş ve Büyük Ortam bu dinin sembolik unsurlarıdır.",
        ]))
        .add_callout(Callout("insight", "Kritik Odak: Comte'un 'Dini' Neyi Kastediyor?",
            "Comte'un 'din' derken kastettiği tanrı inancı değil, bilimi merkeze alan ahlaki/toplumsal bir "
            "örgütlenme biçimidir — sınavlarda bu ayrım sıkça karıştırılır."))
        .add_person(SCHOPENHAUER)
    )
    ch1.pages.append(
        ChapterPage(continue_tag="Schopenhauer: İrade ve Kötümserlik")
        .add_block(BulletBlock(3, "İrade, Acı ve Negatif Hedonizm", [
            "Felsefesinin temelini insanın içsel arzuları ve iradesi oluşturur: <b>'Çok mutsuz olmanın en "
            "güvenilir yolu, mutlu olmayı istememektir.'</b>",
            "Felsefesi kötümser (pesimist) ve karamsardır: yaşam acıdan, tatminsizlikten ve karşılanması güç "
            "arzulardan ibarettir; gerçekçi olmayan beklentilerin kaynağı, aşırı mutluluk arzusudur.",
            "Acı ve ızdırabın yokluğu en yüksek iyiliktir — bu görüşe <b>'negatif hedonizm'</b> denir. "
            "Leibniz'in iyimserliğini eleştirir: 'Dünya, ızdırabı ve acıyı içinde barındırır; mutluluk ise "
            "yalnızca acının yokluğudur.'",
        ]))
        .add_block(BulletBlock(4, "Yalnızlık ve Özgürlük", [
            "Acıyı azaltmanın yolu olarak ılımlılığı ve çileciliği teşvik eder; gençlerin yalnızlığa "
            "katlanmayı öğrenmesi gerektiğini söyler — yalnızlık, mutluluğun ve içsel huzurun kaynağıdır.",
            "<b>'İnsan, yalnız kaldığı sürece kendisi olur.' 'Yalnızlığı sevmeyen, özgürlüğü sevemez.'</b> "
            "Yalnızlık her insanın temel bir ihtiyacıdır; mutluluk, kendini keşfetmek ve acıdan kaçınmakla "
            "mümkündür.",
        ]))
        .add_table(ComparisonTable(
            "Karşılaştırma: Comte ve Schopenhauer",
            ["Ölçüt", "Auguste Comte", "Arthur Schopenhauer"],
            [
                ["Dünya görüşü", "İyimser — bilim ve akıl yoluyla toplumsal ilerleme mümkündür.", "Kötümser (pesimist) — yaşam özünde acı ve tatminsizliktir."],
                ["Temel kavram", "Pozitif bilgi / Üç Hal Yasası.", "İrade (Wille)."],
                ["Çözüm önerisi", "Bilim temelli 'İnsanlık Dini' ile toplumsal düzen.", "Çilecilik, ılımlılık, yalnızlık yoluyla acıdan kaçınma."],
            ]
        ))
        .add_summary("Comte, insanlığın teolojik ve metafizik aşamalardan bilimsel/pozitif aşamaya evrildiğini "
            "savunarak toplumu bilim etrafında yeniden örgütlemeyi önerirken; Schopenhauer, yaşamın "
            "temelinde doyumsuz bir irade olduğunu, mutluluğun ancak bu iradenin doğurduğu acıdan kaçınmakla "
            "(yalnızlık, ılımlılık, çilecilik) mümkün olduğunu savunur.")
    )

    # =====================================================================
    # BÖLÜM 2 — Darwin ve Freud: Evrim Teorisi ve Psikanaliz
    # =====================================================================
    ch2 = Chapter(
        number=2,
        title="Evrim Teorisi ve Psikanaliz",
        subtitle="Darwin'in doğal seçilimi ile Freud'un bilinçdışı keşfi, dönemin dinî ve akılcı güvenini sarsar",
        key_terms=[
            KeyTerm("Doğal Seçilim", "Çevreye en uyumlu bireylerin hayatta kalıp üreme şansını artırdığı, türlerin zamanla değiştiği süreç."),
            KeyTerm("Bilinçdışı (İd/Es)", "Freud'a göre haz ilkesine göre çalışan, akıl dışı dürtülerin bulunduğu zihinsel katman."),
            KeyTerm("Süperego (Üst-Ben)", "Çevrenin ahlaki beklentilerinin içselleştirilmesiyle oluşan zihinsel katman."),
            KeyTerm("Serbest Çağrışım", "Freud'un bilinçdışına ulaşmak için kullandığı, danışanın aklına gelen her şeyi sansürsüz söylemesini istediği yöntem."),
        ],
    )
    ch2.pages.append(
        ChapterPage()
        .add_terms(ch2.key_terms)
        .add_person(DARWIN)
        .add_block(BulletBlock(1, "Hayatı ve Dünya Turu", [
            "Babası doktordu; küçükken böcek koleksiyonu yapmış, okula bu böcekleri götürmüştür. Doğa "
            "bilimleriyle ve jeolojiyle ilgilenmiş, Güney Amerika haritasını çıkarmıştır.",
            "HMS Beagle gemisiyle <b>22 yaşında yola çıkmış</b>, 5 yıl süren dünya turunda özellikle Güney "
            "Amerika'daki Galapagos Adaları'nda çalışmalarını yapmış, İngiltere'ye ~27 yaşında dönmüştür.",
        ]))
    )
    ch2.pages.append(
        ChapterPage(continue_tag="Darwin'in Kanıtları")
        .add_callout(Callout("caution", "Notlardaki Bir Hata: Beagle Seferi ve Soy Karışıklığı",
            "Ham notlarda Beagle seferinin yaş sırası belirsizdi ('22 yaşında İngiltere'ye dönmüş' gibi "
            "yazılmıştı); doğrusu Darwin <b>22 yaşında yola çıkmış, 5 yıl sonra dönmüştür</b>. Ayrıca "
            "notlarda 'Jean de Lamarck / Erasmus torunu' ifadesi kime ait olduğu belirsiz yazılmıştı: Darwin, "
            "erken bir evrim fikri öne süren dedesi <b>Erasmus Darwin</b>'in torunuydu; Lamarck ise ondan "
            "önce yaşamış, farklı bir evrim mekanizması öneren ayrı bir zoologtur."))
        .add_block(BulletBlock(2, "Evrim Teorisinin İki Tezi ve Kanıtları", [
            "Teorisi iki temel tezi özetler: <b>(1)</b> biyolojik evrim gerçekleşir, <b>(2)</b> bu evrim doğal "
            "seçilim yoluyla gerçekleşir.",
            "<b>Kanıtlar:</b> deniz fosillerinin dağların tepesinde bulunması; canlı türlerinin coğrafi "
            "dağılımı ('Tanrı her ada için ayrı bir kaplumbağa türü mü yarattı?'); köpek, yarasa, tavşan ve "
            "insan embriyolarının ilk gelişim evrelerinde birbirine çok benzemesi.",
            "İnsanların çiftçilikte iyi örnekleri seçip zayıfları elemesi (yapay seçilim) doğadaki doğal "
            "seçilime ilham kaynağı olmuş; Thomas Malthus'un <b>Nüfus İlkesi Üzerine Bir Deneme</b> adlı "
            "eseri Darwin'e evrimin nasıl gerçekleştiğine dair açıklayıcı bir çerçeve sunmuştur.",
        ]))
    )
    ch2.pages.append(
        ChapterPage(continue_tag="Sigmund Freud ve Psikanaliz")
        .add_person(FREUD)
        .add_block(BulletBlock(3, "Zihnin Yapısı", [
            "İnsanların ihtiyaçları/içgüdüleriyle çevrenin dayattıkları arasında bir gerilim olduğunu savunur; "
            "düşüncelerimizi, rüyalarımızı ve eylemlerimizi çoğu zaman akıl dışı dürtüler belirler ('ruh "
            "arkeolojisi').",
            "<b>İd (Es):</b> doğuştan gelen, haz ilkesine göre çalışan katman. İnsan büyüdükçe <b>gerçeklik "
            "ilkesi</b>, haz ilkesini dengelemeye başlar; çevrenin ahlaki beklentileri içimizde yer edip "
            "<b>süperego</b>yu (üst-ben) oluşturur.",
        ]))
        .add_callout(Callout("caution", "Notlardaki Bir Hata: İd ile Haz İlkesi",
            "Ham notlarda \"'O' ya da Haz ilkesi\" ifadesi İd (O) ile haz ilkesini eş anlamlıymış gibi "
            "sunuyordu; doğrusu <b>haz ilkesi, İd'in çalışma prensibidir, İd'in kendisi değildir</b> — bu "
            "kitapta ilişki bu şekilde netleştirilmiştir."))
        .add_table(ComparisonTable(
            "Freud'un Mekânsal Zihin Metaforu",
            ["Mekân", "Karşılığı"],
            [
                ["Salon", "Bilinç — farkında olduğumuz, düşündüğümüz şeyler."],
                ["Koridor", "Bilinçdışı — bastırılmaya çalışılan düşünceler; geçişi 'yansıtma' denen savunma mekanizması kontrol eder."],
            ]
        ))
    )
    ch2.pages.append(
        ChapterPage(continue_tag="Serbest Çağrışım ve Karşılaştırma")
        .add_block(BulletBlock(4, "Serbest Çağrışım ve Travma", [
            "İnsan bir konuyu ne kadar çok unutmak isterse, o konuyu o kadar çok düşünür (bastırma "
            "paradoksu) — Freud bu yüzden <b>serbest çağrışım</b> yöntemini geliştirmiştir.",
            "Travma, ruhsal bir yaralanmayı ifade eder ('yara' anlamına gelir).",
        ]))
        .add_table(ComparisonTable(
            "Karşılaştırma: Darwin ve Freud",
            ["Ölçüt", "Darwin", "Freud"],
            [
                ["Alan", "Biyoloji / doğa bilimleri.", "Psikoloji / psikanaliz."],
                ["Temel iddia", "İnsan da dahil türler, doğal seçilimle zaman içinde evrilir.", "Davranışları akıl değil, çoğunlukla bilinçdışı/akıl dışı dürtüler yönetir."],
                ["Döneme etkisi", "Kutsal kitaplardaki 'türler değişmez' görüşünü sarsar.", "İnsanın kendi aklına tam hakim olduğu görüşünü sarsar."],
            ]
        ))
        .add_summary("Darwin, türlerin doğal seçilim yoluyla ortak bir atadan evrildiğini göstererek insanın "
            "doğadaki konumunu; Freud ise davranışlarımızın büyük ölçüde bilinçdışı, akıl dışı dürtülerce "
            "yönetildiğini göstererek insanın kendi aklına hakimiyeti konusundaki güvenini sarsmıştır.")
    )

    # =====================================================================
    # BÖLÜM 3 — Çağdaş Felsefeye Giriş ve Bertrand Russell: Analitik Felsefe
    # =====================================================================
    ch3 = Chapter(
        number=3,
        title="Analitik Felsefe",
        subtitle="Analitik-Kıta Felsefesi ayrımından Russell'ın mantıksal atomculuğuna ve din eleştirisine",
        key_terms=[
            KeyTerm("Çağdaş Felsefe", "20. yüzyıl başlarından günümüze uzanan, disiplinler arası, eleştirel ve çoğulcu felsefe dönemi."),
            KeyTerm("Analitik Felsefe", "Dilin, mantığın ve bilimsel yöntemin analizine odaklanan felsefe geleneği."),
            KeyTerm("Kıta Felsefesi", "Tarihsel, kültürel ve varoluşsal konuları merkeze alan Avrupa kökenli felsefe geleneği."),
            KeyTerm("Mantıksal Atomculuk", "Dil ile dünya arasında yapısal bir benzerlik olduğunu savunan görüş."),
        ],
    )
    ch3.pages.append(
        ChapterPage()
        .add_terms(ch3.key_terms)
        .add_block(BulletBlock(1, "Çağdaş Felsefenin İki Büyük Geleneği", [
            "Çağdaş felsefe, 20. yüzyıl başlarından günümüze kadar gelişen; disiplinler arası, eleştirel ve "
            "çoğulcu bir felsefe alanıdır.",
            "20. yüzyıl felsefesi büyük ölçüde pozitivizmin sınırlarına bir tepki olarak ortaya çıkmıştır: "
            "insan deneyimini, anlamı, dili ve toplumu daha derinlemesine ele alan yaklaşımlar (fenomenoloji, "
            "varoluşçuluk, hermeneutik, yapısalcılık, postyapısalcılık gibi) bu dönemde gelişmiştir.",
        ]))
        .add_table(ComparisonTable(
            "Karşılaştırma: Analitik Felsefe – Kıta Felsefesi",
            ["Ölçüt", "Analitik Felsefe", "Kıta Felsefesi"],
            [
                ["Coğrafya", "İngiltere ve Amerika.", "Avrupa (kıta)."],
                ["Odak", "Dilin, mantığın ve bilimsel yöntemin analizi.", "Tarihsel, kültürel ve varoluşsal konular."],
                ["Önde gelen isimler", "Bertrand Russell, Ludwig Wittgenstein, G. E. Moore.", "—"],
                ["İçerdiği akımlar", "Mantıksal atomculuk, dil felsefesi.", "Fenomenoloji, varoluşçuluk, hermeneutik, postyapısalcılık."],
            ]
        ))
    )
    ch3.pages.append(
        ChapterPage(continue_tag="Bertrand Russell'ın Hayatı")
        .add_person(RUSSELL)
        .add_block(BulletBlock(2, "Hayatı ve Aktivist Kişiliği", [
            "İngiliz, hümanist bir filozoftur: <b>'Düşüncelerim için ölmeyi göze almam, çünkü yanılıyor "
            "olabilirim.'</b> Cambridge Trinity College'daki 'Havariler' (Apostles) grubuna alınmıştır.",
            "Matematik üzerine çalışmalar yapmış, kendi adıyla bilinen <b>Russell Paradoksu</b>'nu geliştirmiş; "
            "Whitehead ile yazdığı <b>Principia Mathematica</b> ile matematiği tamamen mantıksal ilkelerden "
            "türetmeye çalışmıştır.",
            "Bertrand Russell Barış Vakfı'nı ve Atlantik Vakfı'nı kurmuş; ABD'nin Vietnam'a saldırısına karşı "
            "çıkarak Uluslararası Savaş Suçları Mahkemesi'ni toplamıştır.",
        ]))
        .add_callout(Callout("caution", "Notlardaki Bir Hata: İki Ayrı Ödül",
            "Ham notlarda '1949'da... liyakat nişanı almış... nedeniyle Nobel Edebiyat Ödülü'nü almış' "
            "yazıyordu; bu, iki ayrı ödülü tek bir olay gibi sunuyordu. Doğrusu: Russell <b>1949'da Order of "
            "Merit</b> (Liyakat Nişanı), <b>1950'de ise</b> insan hakları ve özgür düşünce üzerine yazdığı "
            "yazıları nedeniyle <b>Nobel Edebiyat Ödülü'nü</b> ayrı ayrı kazanmıştır."))
    )
    ch3.pages.append(
        ChapterPage(continue_tag="Russell'ın Felsefi Katkıları")
        .add_block(BulletBlock(3, "Russell'ın Felsefesinin Temel Başlıkları", [
            "<b>Mantıksal atomculuk:</b> dil ve dünya arasında yapısal bir benzerlik vardır. 'Bir insanın neyi "
            "kastettiğini anlamak için, neyi söylediğine değil, nasıl söylediğine bak.'",
            "<b>Bilgi teorisi:</b> bilginin temelinde duyusal deneyim vardır; bazı şeyleri doğrudan "
            "deneyimleyerek, bazılarını çıkarım yaparak biliriz — kesin bilgiye mantıksal analizle ulaşılır.",
            "<b>Din eleştirisi:</b> ateisttir. <b>Neden Hristiyan Değilim</b> adlı eserinde Tanrı'nın varlığına "
            "dair delilleri çürütmeye çalışır; ona göre din akla değil korkuya dayanır ve ilerlemeye engeldir.",
            "<b>Etik ve siyaset:</b> kapitalizm ve din bireysel düşünceyi bastırır; akıl ve eğitim özgür bir "
            "toplumun gelişmesine katkıda bulunur. Hayatı boyunca aşk özlemi, bilgi arayışı ve insanlığın "
            "ızdırabına duyduğu merhamet tarafından yönlendirildiğini söylemiştir.",
        ]))
        .add_callout(Callout("focus", "Russell'ı Yönlendiren Üç His",
            "Russell, hayatı boyunca kendisini yönlendiren üç büyük his ve arzu tanımlamıştır: <b>aşk özlemi, "
            "bilgi arayışı</b> ve <b>insanlığın ızdırabına karşı duyduğu merhamet.</b>"))
        .add_summary("Çağdaş felsefe, dil ve mantığın kesinliğine odaklanan Analitik Felsefe ile insan "
            "deneyimini ve tarihselliği merkeze alan Kıta Felsefesi olmak üzere iki ana damardan beslenir; "
            "Russell, G. E. Moore ile birlikte kurduğu mantıksal atomculuk ve dilin mantıksal analiziyle bu "
            "geleneğin en önemli temsilcilerinden biri olmuştur.")
    )

    # =====================================================================
    # BÖLÜM 4 — Søren Kierkegaard: Varoluşçuluğun Öncüsü
    # =====================================================================
    ch4 = Chapter(
        number=4,
        title="Varoluşçuluğun Öncüsü: Kierkegaard",
        subtitle="Nesnel ve öznel doğru ayrımından İman Şövalyesi'ne giden üç aşamaya",
        key_terms=[
            KeyTerm("Nesnel Doğru", "Herkes tarafından kabul edilen, üzerinde tartışılmayan doğrular (ör. 2×2=4)."),
            KeyTerm("Öznel Doğru", "Kişinin kendi iç dünyasında doğru kabul ettiği şeyler (ör. din/Tanrı inancı)."),
            KeyTerm("İman Şövalyesi", "Gerçek dindarlık formuna bürünmüş insan."),
            KeyTerm("İnanç Sıçraması", "Anlama akıl yoluyla değil, aklı devre dışı bırakıp doğrudan inancı seçerek ulaşmak."),
        ],
    )
    ch4.pages.append(
        ChapterPage()
        .add_terms(ch4.key_terms)
        .add_block(BulletBlock(1, "Doğrunun İkiye Ayrımı", [
            "Kierkegaard'a göre inanmak ve sorgulamak, iki düşman eylemdir. İnanan insanlar öznel doğruları "
            "nesnel doğrulardan daha üstün tutar (Öznel doğru > Nesnel doğru); çünkü nesnel doğruların "
            "sınırları vardır ve inanan insana tek başına yetmez.",
            "Kierkegaard, inanan insanları da ikiye ayırır: <b>Yobazlar</b>, dini nesnel bir doğru gibi "
            "görüp Tanrı'nın varlığını 'kanıtlamak' için evrimi çürütmeye çalışırlar; <b>Dindarlar</b> ise "
            "inancı öznel bir doğru olarak görür, Tanrı'yı mantık yoluyla kanıtlamaya çalışmazlar.",
        ]))
        .add_table(ComparisonTable(
            "Karşılaştırma: Nesnel Doğru – Öznel Doğru",
            ["Ölçüt", "Nesnel Doğru", "Öznel Doğru"],
            [
                ["Tanım", "Herkes tarafından kabul edilen, tartışılmayan konular.", "Kişinin kendi iç dünyasında doğru kabul ettiği şeyler."],
                ["Örnek", "2 × 2 = 4", "Din ve Tanrı inancı"],
                ["İnanan insan için önceliği", "İkincil — tek başına yeterli gelmez, sınırlıdır.", "Birincil — inanan insan öznel doğruyu nesnel doğrudan üstün tutar."],
            ]
        ))
    )
    ch4.pages.append(
        ChapterPage(continue_tag="İman Şövalyesi'ne Giden Üç Aşama")
        .add_flow(FlowDiagram([
            FlowStep("Estetik Aşama", "Haz arayışı; beraberinde can sıkıntısı gelir"),
            FlowStep("Etik Aşama", "Eylemleri doğru-yanlış diye ayırma"),
            FlowStep("Dinsel Aşama", "İnanç Sıçraması ile anlama ulaşma"),
        ], caption="İman Şövalyesi Olabilmek İçin Geçilmesi Gereken Üç Aşama"))
        .add_block(BulletBlock(2, "Aşamaların İçeriği", [
            "<b>Estetik aşama:</b> kişi zevkini en yüksek seviyeye çıkarmak, acısını en aza indirmek ister. "
            "Bu aşamada can sıkıntısı çok tehlikeli bir olgudur; kişi acıdan kaçmamalı, onunla yüzleşmelidir "
            "— acı, kişinin ruhsal gelişiminde çok önemlidir, insana farkındalık katar, 'ben ne haldeyim' "
            "diye sorgulamasını sağlar. Bu sorguyu soran kişi bir sonraki aşamaya geçer.",
            "<b>Etik aşama:</b> kişi eylemlerini doğru ve yanlış diye ayırır; bu insanın son formu değildir — "
            "anlamlı yaşama akılla ulaşılamaz, akıl bir kenara konup bir sonraki aşamaya geçilmelidir.",
            "<b>Dinsel aşama:</b> anlam kavramına sorgulayarak değil, inanarak ulaşılır — buna 'inanç "
            "sıçraması' denir.",
        ]))
        .add_callout(Callout("caution", "Notlardaki Boşluk: Estetik Aşama Cümlesi",
            "Öğretmenin ham notlarında 'Kişi acıdan kaçmamalı, acısını içine…' cümlesi yarım kalmıştı — "
            "cümle tamamlanmadan bırakılmış. Bu kitapta, takip eden cümlelerle (acının farkındalık kattığı, "
            "sorgulamaya yol açtığı) tutarlı olacak biçimde <b>'acısını içine atıp bastırmamalı, onunla "
            "yüzleşmelidir'</b> şeklinde tamamlanmıştır; bu tamamlama yorumsaldır."))
        .add_callout(Callout("insight", "Kritik Odak: Şüphe ve Gerçek Dindarlık",
            "Dindar bir insan inancına karşı şüphe duymalıdır — Kierkegaard'a göre asıl dindarlık, şüpheye "
            "rağmen inanmaya devam etmektir. Bu, sınav sorularında en çok karıştırılan noktadır: dindarlık, "
            "şüphenin yokluğu değil, <b>şüpheye rağmen sürdürülen inançtır.</b>"))
        .add_summary("Kierkegaard, doğruyu nesnel ve öznel olarak ikiye ayırarak inancın öznel bir doğru "
            "olduğunu savunur; insanın gerçek dindarlığa (iman şövalyeliğine) ulaşması için estetik, etik ve "
            "dinsel aşamalardan geçip son aşamada aklı bir kenara bırakarak 'inanç sıçraması' yapması "
            "gerektiğini öne sürer.")
    )

    # =====================================================================
    # BÖLÜM 5 — Fenomenoloji ve Varoluşçuluk: Husserl, Heidegger, Sartre, Camus
    # =====================================================================
    ch5 = Chapter(
        number=5,
        title="Fenomenoloji ve Varoluşçuluk",
        subtitle="Husserl'in bilinç deneyiminden Heidegger'in Dasein'ına; Sartre'ın özgürlüğünden Camus'nün absürdizmine",
        key_terms=[
            KeyTerm("Fenomenoloji", "Nesnelerin bilince nasıl göründüğünü, yani deneyimin özünü inceleyen felsefe akımı."),
            KeyTerm("Dasein (orada-varlık)", "Heidegger'in insanı tanımlamak için kullandığı, 'dünyada orada bulunan varlık' anlamına gelen kavram."),
            KeyTerm("Kötü Niyet (mauvaise foi)", "Sartre'a göre insanın özgürlükten ve onun getirdiği sorumluluktan kaçma çabası."),
            KeyTerm("Absürdizm", "Camus'ye göre insanın anlam arayışı ile evrenin sessizliği arasındaki uyumsuzluktan doğan durum."),
        ],
    )
    ch5.pages.append(
        ChapterPage()
        .add_terms(ch5.key_terms)
        .add_person_row([HUSSERL, HEIDEGGER])
        .add_block(BulletBlock(1, "Husserl: Bilincin Deneyimi", [
            "Fenomenoloji, Husserl tarafından geliştirilmiştir. Felsefenin görevi, nesnelerin bilince nasıl "
            "göründüğünü, yani deneyimin özünü incelemektir. <b>Fenomenolojik indirgeme</b> adlı yöntem: "
            "önyargılardan sıyrılarak yalnızca bilincin deneyimine odaklanmak — felsefe kesin bilgiye ancak "
            "bu yolla ulaşır.",
        ]))
    )
    ch5.pages.append(
        ChapterPage(continue_tag="Heidegger: Dasein ve Varlık Sorusu")
        .add_block(BulletBlock(2, "Heidegger: Varlık Sorusu ve Dasein", [
            "Husserl'in öğrencisi olan Heidegger, fenomenolojiyi varlık sorusunu merkeze alarak yeniden "
            "şekillendirmiştir. İnsan, dünyada 'orada-varlık' (<b>Dasein</b>) olarak bulunur: kendi varlığına "
            "dair anlayışından yola çıkarak, genel olarak varlığı anlayıp anlamlandırabilme yetisi.",
            "Varlığı anlamak, varoluşun koşullarını çözümlemekle mümkündür; zaman, ölüm, kaygı gibi kavramlar "
            "üzerinden insanın özgür varoluşunu inceler.",
        ]))
        .add_table(ComparisonTable(
            "Karşılaştırma: Husserl – Heidegger",
            ["Ölçüt", "Edmund Husserl", "Martin Heidegger"],
            [
                ["Fenomenolojinin odağı", "Bilincin deneyimi, nesnelerin bilince görünüşü.", "Varlık sorusu (insanın varoluşu)."],
                ["Anahtar kavram", "Fenomenolojik indirgeme.", "Dasein (orada-varlık)."],
                ["Yöntem", "Önyargılardan sıyrılıp saf deneyime odaklanmak.", "Zaman, ölüm, kaygı üzerinden varoluşu çözümlemek."],
            ]
        ))
    )
    ch5.pages.append(
        ChapterPage(continue_tag="Varoluşçuluk: Sartre ve Camus")
        .add_person_row([SARTRE, CAMUS])
        .add_block(BulletBlock(3, "Sartre: Özgürlük ve Kötü Niyet", [
            "Fransız filozoftur. <b>'İnsan önce var olur, sonra kendi özünü kendi eylemleriyle oluşturur.'</b> "
            "İnsan tamamen özgürdür ve bu özgürlük aynı zamanda sorumluluk taşımasına neden olur.",
            "İnsanlar özgürlükten, yani bu özgürlüğün getirdiği sorumluluktan kaçmak isteyebilirler — buna "
            "<b>'kötü niyet'</b> adını vermiştir.",
        ]))
        .add_block(BulletBlock(4, "Camus: Absürdizm ve Sisifos", [
            "'Absürdizm' kavramını varoluşçuluğa katar: insanların evrende anlam bulma çabasının saçma "
            "olduğunu, bu anlam arayışının eninde sonunda başarısızlıkla sonuçlanacağını anlatır — insanın "
            "anlam arayışı ile dünyanın sessizliği arasındaki bu uyumsuzluğa 'absürt' denir.",
            "Bütün bu absürtlüğe rağmen insan hayatı anlamlandırmaya çalışmalı, yaşamı seçmelidir: <b>Sisifos "
            "Miti</b> — anlam olmasa bile mücadele devam eder.",
        ]))
        .add_table(ComparisonTable(
            "Karşılaştırma: Sartre – Camus",
            ["Ölçüt", "Jean-Paul Sartre", "Albert Camus"],
            [
                ["Anahtar kavram", "Özgürlük ve sorumluluk / kötü niyet.", "Absürt / absürdizm."],
                ["Temel tez", "İnsan özünü kendi eylemleriyle oluşturur, özgürlükten kaçmamalıdır.", "Evrende anlam yoktur, ama insan yine de yaşamı anlamlandırmaya çalışmalı, mücadeleyi sürdürmelidir."],
                ["Simge", "—", "Sisifos Miti"],
            ]
        ))
        .add_summary("Husserl, fenomenolojiyi bilincin deneyimini önyargısız incelemenin bir yöntemi olarak "
            "kurarken; öğrencisi Heidegger bu yöntemi insanın 'orada-varlık' (Dasein) olarak varoluşunu "
            "çözümlemeye yöneltmiştir. Bu zemin üzerinde Sartre, insanın özünü özgür eylemleriyle "
            "oluşturduğunu ve bu özgürlükten kaçışın 'kötü niyet' olduğunu savunurken; Camus, evrenin "
            "anlamsız sessizliği karşısında insanın yine de yaşamı ve mücadeleyi (Sisifos Miti) seçmesi "
            "gerektiğini öne sürer.")
    )

    # =====================================================================
    # BÖLÜM 6 — Friedrich Nietzsche: Güç İstenci, Üstinsan ve Nihilizm
    # =====================================================================
    ch6 = Chapter(
        number=6,
        title="Güç İstenci, Üstinsan ve Nihilizm",
        subtitle="Nietzsche'nin eleştiri felsefesinden Tanrı'nın ölümüne ve Üstinsan idealine",
        key_terms=[
            KeyTerm("Güç İstenci", "Nietzsche'ye göre her canlıda bulunan, sadece var olmayı değil güçlü olmayı isteyen temel itki."),
            KeyTerm("Üstinsan (Übermensch)", "Tutkularının kölesi olmaktan kurtulup kendi değerlerini yaratan, güçlü insan."),
            KeyTerm("'Tanrı Öldü'", "Nietzsche'nin, Avrupa'nın geleneksel ahlak, değer ve düzen kaynağı olarak Tanrı'ya artık ihtiyaç duymadığını ifade eden sözü."),
            KeyTerm("Nihilizm", "Hayatın, ahlakın, bilginin ve değerlerin nesnel bir temeli ve anlamı olmadığını savunan, her türlü otoriteyi ve toplumsal kuralı reddeden görüş."),
        ],
    )
    ch6.pages.append(
        ChapterPage()
        .add_terms(ch6.key_terms)
        .add_person(NIETZSCHE)
        .add_block(BulletBlock(1, "Hayatı ve Entelektüel Dönüşümü", [
            "Ona göre yeryüzündeki bütün dinler ve politik görüşler insanoğlunun özgür gelişmesini engeller; "
            "bu yüzden hepsi yıkılmalıdır. 13 yaşındayken kötülük sorunu üzerine düşünmeye başlamıştır: "
            "'Madem Tanrı iyiyse, dünyadaki bu kadar acı neden var?'",
            "Frengi hastasıdır. Schopenhauer'in <b>İsteme ve Tasarım Olarak Dünya</b> kitabını okuduktan sonra "
            "ondan derinden etkilenmiştir; 24 yaşında Basel Üniversitesi'nde görev yapmıştır.",
            "Savaşa katılmış, subaylardan etkilenmiştir: 'En güçlü ve en yüksek yaşama isteminin, sefil bir "
            "var oluş mücadelesinde değil, savaş isteminde, güç isteminde, yenmek isteminde olduğunu ilk kez "
            "orada hissettim.' Savaşta gördüğü vahşetler yüzünden sağlığı bozulup askeriyeden ayrılmıştır.",
        ]))
        .add_block(BulletBlock(2, "Lou Andreas-Salomé ve Sonu", [
            "1882'de tanıştığı, evlenme teklif edip reddedildiği Rus yazar/psikanalist Lou Andreas-Salomé ile "
            "kısa süren yoğun entelektüel ilişkisi Nietzsche üzerinde derin bir etki bırakmış, yaşadığı hayal "
            "kırıklığı <b>Böyle Buyurdu Zerdüşt</b> eserinin yazımına ilham vermiştir.",
            "1887'de Dostoyevski'yi okurken bir atın kırbaçlandığı bölümden etkilenmiş; gerçek hayatta da bir "
            "atın kırbaçlandığını görünce atın boynuna sarılıp 'Seni anlıyorum' demiş ve orada bayılmıştır. "
            "Gözünü bir akıl hastanesinde açmış, delirmiş ve 1900'de ölmüştür.",
        ]))
    )
    ch6.pages.append(
        ChapterPage(continue_tag="Eleştiri, İnsan Tipleri ve Güç İstenci")
        .add_block(BulletBlock(3, "Eleştiri ve Üç İnsan Tipi", [
            "Felsefesinin özü eleştiridir — Kant'ı, Hegel'i, Schopenhauer'i, Katolik Hristiyanlığı, Avrupa "
            "kültürünü ve yürürlükteki değerleri eleştirir. Felsefesinin baş kahramanı insandır: insan bir "
            "güçtür, özgürlüğünü ele alabilecek tek güçtür.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("Sürü İnsanı", "Kendisini yönetecek bir çobana/başa ihtiyaç duyar"),
            FlowStep("Özgür İnsan", "Sürüden ayrılmış, dünyayı kendi gözleriyle görmek ister"),
            FlowStep("Trajik İnsan", "Geçmişini tüm yönleriyle kabul edip yaşamı olumlar"),
        ], caption="Nietzsche'ye Göre İnsan Tipleri"))
        .add_block(BulletBlock(4, "Güç İstenci ve Üstinsan", [
            "Yaşamda özgür olmanın, hiçbir şeye boyun eğmemenin tek yolu güç istemidir. Mutluluk hazda değil "
            "güçtedir — güç istemi herkeste bulunur: filozof ve bilim insanı için hakikatin izindedir, "
            "sanatçılar eserlerinde, iş insanları zengin olmakla güç istencini bulur.",
            "<b>Üstinsan:</b> evrenin gerçek efendisidir; bedensel ve akıl bakımından güçlüdür, çıkarına "
            "ulaşmak için bencillikten çekinmez (acımak insanı zayıflatan bir duygudur). Ahlak ve Tanrı gibi "
            "güçlü görünen kavramları yıkar; tutkularının kölesi olmaktan kurtulup kendi efendisi olmuş "
            "insandır. Üstinsan kavramı Böyle Buyurdu Zerdüşt'te dile getirilmiştir.",
        ]))
        .add_block(BulletBlock(5, "Tanrı'nın Ölümü", [
            "Nietzsche, Tanrı'nın yerine insanı koymuş ve 'Tanrı öldü' sözünü <b>Şen Bilim</b> adlı kitabında "
            "dile getirmiştir: Avrupa, evrendeki tüm ahlak, değer ve düzenin kaynağı olarak artık Tanrı'ya "
            "ihtiyaç duymamaktadır — felsefe ve bilim bu işlevi zaten görebilmektedir.",
            "Tanrı, uzun yıllar insanların üzerine gölgesini bırakmaya devam edecektir; insanlığı bu durumdan "
            "kurtaracak olanlar üstinsanlardır.",
        ]))
        .add_callout(Callout("insight", "Kritik Odak: Nihilizm Bir Övgü Değil, Bir Teşhistir",
            "Nihilizm, hayatın, ahlakın, bilginin ve değerlerin nesnel bir temeli ve anlamı olmadığını "
            "savunan, her türlü otoriteyi ve sistemi reddeden görüştür. Nietzsche'nin 'Tanrı öldü' tespiti "
            "bir nihilizm övgüsü değil, tam tersine <b>Avrupa'nın içine düştüğü nihilist krizin bir "
            "teşhisidir</b> — üstinsan kavramı, bu krizi aşmanın yolu olarak önerilir."))
        .add_summary("Nietzsche, geleneksel ahlakı ve dini 'Tanrı'nın ölümü' tespitiyle eleştirerek, insanın "
            "anlamı dışarıdan (Tanrı, ahlak) değil kendi güç istenciyle yaratması gerektiğini savunur; bu "
            "yaratımı başarabilen insan tipine 'üstinsan' adını verir.")
    )

    # =====================================================================
    # BÖLÜM 7 — Faydacılık ve Marx: Toplum, Ahlak ve Ekonomi Felsefesi
    # =====================================================================
    ch7 = Chapter(
        number=7,
        title="Faydacılık ve Tarihsel Maddecilik",
        subtitle="Bentham'ın niceliksel ve Mill'in niteliksel faydacılığından Marx'ın alt yapı-üst yapı çatışmasına",
        key_terms=[
            KeyTerm("Faydacılık (Utilitarizm)", "Bir eylemin ahlaki değerinin, yarattığı mutluluğa/faydaya göre belirlendiğini savunan görüş."),
            KeyTerm("En Büyük Mutluluk İlkesi", "Mümkün olan en çok sayıda insan için en büyük mutluluğu sağlamayı amaçlayan ilke."),
            KeyTerm("Alt Yapı ve Üst Yapı", "Alt yapı toplumun maddi/ekonomik üretim ilişkilerini; üst yapı toplumun düşünüş tarzı, kurumları, hukuku, dini, ahlakı ve felsefesini kapsar."),
            KeyTerm("Diyalektik Materyalizm", "Alt yapı ile üst yapı arasındaki çatışmaya dayanan, Marx'ın tarih ve toplum anlayışı."),
        ],
    )
    ch7.pages.append(
        ChapterPage()
        .add_terms(ch7.key_terms)
        .add_person_row([BENTHAM, MILL])
        .add_block(BulletBlock(1, "Jeremy Bentham: Klasik Faydacılık", [
            "İngiliz filozof, hukukçu ve sosyal reformcudur; faydacılık felsefesinin kurucusudur. <b>En büyük "
            "mutluluk ilkesi:</b> en çok sayıda insan için en büyük mutluluğu sağlamak.",
            "Hedonist yaklaşım: mutluluk = haz + acının yokluğu. Ahlaki kararlar nesnel olmalı, ahlaki "
            "eylemler ölçülebilir olmalıdır; yasaların amacı toplumda en fazla faydayı sağlamak, cezalar "
            "suçun topluma verdiği zarara göre şekillenmelidir. <b>Panoptikon</b> hapishane tasarımıyla "
            "tanınır.",
        ]))
    )
    ch7.pages.append(
        ChapterPage(continue_tag="Mill'in Liberal Faydacılığı ve Karşılaştırma")
        .add_block(BulletBlock(2, "John Stuart Mill: Liberal Faydacılık", [
            "İngiliz filozof, ekonomist ve siyasetçidir; liberal düşüncenin öncülerindendir, Bentham'ın "
            "düşüncelerini geliştirmiştir. Bentham'dan farklı olarak hazlar arasında niteliksel bir ayrım "
            "yapar: zihinsel hazlar bedensel hazlardan üstündür.",
            "<b>Özgürlük Üzerine</b>'de bireysel özgürlüğün korunması gerektiğini savunur — başkasına zarar "
            "vermediği sürece her birey özgürdür; <b>Kadınların Boyunduruk Altında</b> adlı eseri de vardır. "
            "Empiristtir, ama bilimsel yönteme de büyük önem verir.",
        ]))
        .add_table(ComparisonTable(
            "Karşılaştırma: Bentham – Mill",
            ["Ölçüt", "Jeremy Bentham", "John Stuart Mill"],
            [
                ["Haz anlayışı", "Niceliksel — tüm hazlar eşit sayılır, önemli olan miktardır.", "Niteliksel — zihinsel hazlar bedensel hazlardan üstündür."],
                ["Vurgu", "Ölçülebilirlik, yasa ve ceza reformu.", "Bireysel özgürlük, başkasına zarar vermeme ilkesi."],
                ["Temel katkı", "Faydacılığın kurucusu, Panoptikon.", "Faydacılığı geliştirdi, liberal düşüncenin öncüsü."],
            ]
        ))
        .add_summary("Bentham, bir eylemin ahlakiliğini yarattığı hazza göre ölçülebilir biçimde değerlendiren "
            "faydacılığı kurarken; Mill bu görüşü geliştirip hazlar arasında nitelik farkı gözeterek bireysel "
            "özgürlüğü de faydacı çerçeveye eklemiştir.")
    )
    ch7.pages.append(
        ChapterPage(continue_tag="Karl Marx ve Tarihsel Maddecilik")
        .add_person(MARX)
        .add_block(BulletBlock(3, "Alt Yapı ve Üst Yapı", [
            "Marx, toplumda iki temel yapı olduğunu söyler: <b>alt yapı</b>, toplumdaki maddi, ekonomik ve "
            "toplumsal (üretim) ilişkileri kapsar; <b>üst yapı</b> ise toplumun düşünüş tarzı, politik "
            "kurumlar, yasalar, din, ahlak, sanat, felsefe ve bilimdir.",
            "Alt yapı ile üst yapı arasında bir çatışma vardır — bu yüzden Marx'ın görüşü <b>diyalektik "
            "materyalizm</b> olarak adlandırılır. Ahlak açısından neyin doğru olacağı, toplumsal alt yapının "
            "bir ürünüdür.",
        ]))
        .add_table(ComparisonTable(
            "Alt Yapının İç Hiyerarşisi",
            ["Katman", "İçerik"],
            [
                ["Doğal Üretim Koşulları", "Doğal kaynaklar, iklim koşulları, hammaddeler — en temel katman."],
                ["Üretici Güçler", "İnsanların sahip olduğu araç, gereç, aletler, makineler."],
            ]
        ))
    )
    ch7.pages.append(
        ChapterPage(continue_tag="Sınıf Çatışması ve Komünist Manifesto")
        .add_block(BulletBlock(4, "Sınıf Çatışması ve Yabancılaşma", [
            "Marx'ın döneminde burjuvazi (kapitalistler) ile proletarya (işçiler) arasında bir çatışma vardır: "
            "'Bana ne iş yaptığını söyle, sana kim olduğunu söyleyeyim.' Nasıl çalıştığımız bilincimizi, "
            "bilincimiz de nasıl çalıştığımızı etkiler.",
            "İşçi, başkası adına çalışarak kendi emeğine ve kendine <b>yabancılaşır</b>. Marx'a göre emek "
            "halkın kendisine aittir — bu düzende emeğe yabancılaşma yoktur.",
        ]))
        .add_block(BulletBlock(5, "Komünist Manifesto ve Proletarya Diktatörlüğü", [
            "Friedrich Engels ile birlikte <b>Komünist Manifesto</b>'yu yayımlamıştır. Avrupa'da bir "
            "'komünizm hayaleti' dolaşmaktadır; komünistler toplum düzenini zorla devirmeyi hedefler: işçi "
            "sınıfının başkaldırıp üretim araçlarını ele geçireceğine inanır.",
            "<b>Proletarya diktatörlüğü:</b> işçi sınıfının burjuva sınıfını baskı altında tutması.",
        ]))
        .add_callout(Callout("route", "Kritik Odak: Marx Sonrası Komünist Hareket",
            "Marx'tan sonra komünizm hareketi ikiye ayrılır: <b>(1) Sosyal demokrasi</b> ve <b>(2) "
            "Leninizm.</b>"))
        .add_summary("Marx, toplumu maddi/ekonomik ilişkilerden oluşan alt yapı ile düşünce, hukuk ve "
            "kültürden oluşan üst yapının çatışması (diyalektik materyalizm) üzerinden açıklar; bu çatışmayı "
            "burjuvazi–proletarya mücadelesi ve işçinin emeğine yabancılaşması üzerinden somutlaştırır, "
            "çözüm olarak proletarya diktatörlüğünü önerir.")
    )

    chapters = [ch1, ch2, ch3, ch4, ch5, ch6, ch7]

    # =====================================================================
    # SÖZLÜK
    # =====================================================================
    glossary = [
        Concept("Pozitivizm", "Bilginin yalnızca gözlem, deney ve bilimsel yöntemle elde edilebileceğini savunan görüş.", "Auguste Comte", 1),
        Concept("Üç Hal Yasası", "İnsan düşüncesinin teolojik–metafizik–pozitif üç aşamada geliştiğini açıklayan yasa.", "Auguste Comte", 1),
        Concept("İnsanlık Dini", "Toplumu bilim etrafında birleştirmeyi hedefleyen, tanrısız ama dinsel biçimde örgütlenmiş ahlaki sistem.", "Auguste Comte", 1),
        Concept("İrade (Wille)", "Evrenin ve insanın temelinde yatan, doyumsuz, amaçsız itki.", "Arthur Schopenhauer", 1),
        Concept("Negatif Hedonizm", "Mutluluğun pozitif bir haz değil, yalnızca acı ve ızdırabın yokluğu olduğunu savunan görüş.", "Arthur Schopenhauer", 1),
        Concept("Doğal Seçilim", "Çevreye en uyumlu bireylerin hayatta kalıp üreme şansını artırdığı süreç.", "Charles Darwin", 2),
        Concept("Yapay Seçilim", "İnsanların çiftçilik/hayvancılıkta iyi örnekleri seçip zayıfları elemesi; doğal seçilime ilham kaynağı.", "Charles Darwin", 2),
        Concept("Bilinçdışı (İd/Es)", "Haz ilkesine göre çalışan, akıl dışı dürtülerin bulunduğu zihinsel katman.", "Sigmund Freud", 2),
        Concept("Süperego (Üst-Ben)", "Çevrenin ahlaki beklentilerinin içselleştirilmesiyle oluşan zihinsel katman.", "Sigmund Freud", 2),
        Concept("Serbest Çağrışım", "Danışanın aklına gelen her şeyi sansürsüz söylemesini isteyen, bilinçdışına ulaşma yöntemi.", "Sigmund Freud", 2),
        Concept("Çağdaş Felsefe", "20. yüzyıl başlarından günümüze uzanan, disiplinler arası, eleştirel ve çoğulcu felsefe dönemi.", "Genel", 3),
        Concept("Analitik Felsefe", "Dilin, mantığın ve bilimsel yöntemin analizine odaklanan felsefe geleneği.", "Bertrand Russell", 3),
        Concept("Kıta Felsefesi", "Tarihsel, kültürel ve varoluşsal konuları merkeze alan Avrupa kökenli felsefe geleneği.", "Genel", 3),
        Concept("Mantıksal Atomculuk", "Dil ile dünya arasında yapısal bir benzerlik olduğunu savunan görüş.", "Bertrand Russell", 3),
        Concept("Russell Paradoksu", "Kümeler kuramında kendini içermeyen kümeler kümesiyle ilgili çelişki.", "Bertrand Russell", 3),
        Concept("Nesnel Doğru", "Herkes tarafından kabul edilen, üzerinde tartışılmayan doğrular.", "Søren Kierkegaard", 4),
        Concept("Öznel Doğru", "Kişinin kendi iç dünyasında doğru kabul ettiği şeyler.", "Søren Kierkegaard", 4),
        Concept("İman Şövalyesi", "Gerçek dindarlık formuna bürünmüş, şüpheye rağmen inanmaya devam eden insan.", "Søren Kierkegaard", 4),
        Concept("İnanç Sıçraması", "Aklı devre dışı bırakıp doğrudan inancı seçerek anlama ulaşma.", "Søren Kierkegaard", 4),
        Concept("Fenomenoloji", "Nesnelerin bilince nasıl göründüğünü, deneyimin özünü inceleyen felsefe akımı.", "Edmund Husserl", 5),
        Concept("Fenomenolojik İndirgeme", "Önyargılardan sıyrılıp yalnızca bilincin deneyimine odaklanma yöntemi.", "Edmund Husserl", 5),
        Concept("Dasein (orada-varlık)", "İnsanın dünyada bulunuş hali; kendi varlığını anlayıp anlamlandırabilme yetisi.", "Martin Heidegger", 5),
        Concept("Kötü Niyet (mauvaise foi)", "İnsanın özgürlükten ve onun getirdiği sorumluluktan kaçma çabası.", "Jean-Paul Sartre", 5),
        Concept("Absürdizm", "İnsanın anlam arayışı ile evrenin sessizliği arasındaki uyumsuzluktan doğan durum.", "Albert Camus", 5),
        Concept("Sisifos Miti", "Anlam olmasa bile mücadelenin devam etmesi gerektiğini anlatan simge.", "Albert Camus", 5),
        Concept("Güç İstenci", "Her canlıda bulunan, sadece var olmayı değil güçlü olmayı isteyen temel itki.", "Friedrich Nietzsche", 6),
        Concept("Üstinsan (Übermensch)", "Tutkularının kölesi olmaktan kurtulup kendi değerlerini yaratan, güçlü insan.", "Friedrich Nietzsche", 6),
        Concept("'Tanrı Öldü'", "Avrupa'nın geleneksel ahlak, değer ve düzen kaynağı olarak Tanrı'ya artık ihtiyaç duymadığını ifade eden söz.", "Friedrich Nietzsche", 6),
        Concept("Nihilizm", "Hayatın, ahlakın ve değerlerin nesnel bir temeli ve anlamı olmadığını savunan görüş.", "Friedrich Nietzsche", 6),
        Concept("Faydacılık (Utilitarizm)", "Bir eylemin ahlaki değerinin yarattığı mutluluğa/faydaya göre belirlendiğini savunan görüş.", "Bentham / Mill", 7),
        Concept("En Büyük Mutluluk İlkesi", "Mümkün olan en çok sayıda insan için en büyük mutluluğu sağlamayı amaçlayan ilke.", "Jeremy Bentham", 7),
        Concept("Panoptikon", "Tek bir gözetmenin merkezi bir kuleden tüm hücreleri görebildiği hapishane modeli.", "Jeremy Bentham", 7),
        Concept("Alt Yapı ve Üst Yapı", "Toplumun maddi/ekonomik zemini (alt yapı) ile düşünce, hukuk ve kültürden oluşan kurumlar (üst yapı).", "Karl Marx", 7),
        Concept("Diyalektik Materyalizm", "Alt yapı ile üst yapı arasındaki çatışmaya dayanan tarih ve toplum anlayışı.", "Karl Marx", 7),
        Concept("Proletarya Diktatörlüğü", "İşçi sınıfının burjuva sınıfını baskı altında tuttuğu geçiş dönemi.", "Karl Marx", 7),
        Concept("Yabancılaşma", "İşçinin başkası adına çalışarak kendi emeğine ve kendine uzaklaşması durumu.", "Karl Marx", 7),
    ]

    # =====================================================================
    # TEST — 20 Soruluk Genel Değerlendirme
    # =====================================================================
    test_questions = [
        TestQuestion(1, "Comte'un 'Üç Hal Yasası'na göre insan düşüncesi hangi sırayla ilerler?",
            {"A": "Metafizik → Teolojik → Pozitif", "B": "Pozitif → Metafizik → Teolojik",
             "C": "Teolojik → Metafizik → Pozitif", "D": "Teolojik → Pozitif → Metafizik",
             "E": "Metafizik → Pozitif → Teolojik"}),
        TestQuestion(2, "Comte'un 'İnsanlık Dini' anlayışında ibadethaneler ve din adamları sırasıyla neye karşılık gelir?",
            {"A": "Kiliseler / Rahipler", "B": "Üniversiteler / Bilim insanları", "C": "Meclisler / Politikacılar",
             "D": "Fabrikalar / Mühendisler", "E": "Okullar / Öğretmenler"}),
        TestQuestion(3, "Schopenhauer'e göre mutluluk nedir?",
            {"A": "Sürekli haz arayışının sonucu", "B": "Kendi başına var olan pozitif bir durum",
             "C": "Acı ve ızdırabın yokluğu", "D": "Toplumsal statünün getirdiği tatmin",
             "E": "İradenin sınırsızca tatmin edilmesi"}),
        TestQuestion(4, "Schopenhauer'e göre yalnızlık ile hangi kavram arasında kopmaz bir bağ vardır?",
            {"A": "Özgürlük", "B": "Zenginlik", "C": "Bilgi", "D": "İktidar", "E": "Toplumsal statü"}),
        TestQuestion(5, "Darwin'in evrim teorisine kanıt olarak sunduğu gözlemlerden biri aşağıdakilerden hangisidir?",
            {"A": "Tüm türlerin ayrı ayrı yaratıldığının kanıtlanması", "B": "Farklı hayvan embriyolarının ilk evrelerde birbirine benzemesi",
             "C": "Fosillerin yalnızca deniz seviyesinde bulunması", "D": "Türlerin coğrafyadan bağımsız olarak aynı olması",
             "E": "İnsan zekâsının hayvanlardan tamamen farklı kökenden gelmesi"}),
        TestQuestion(6, "Darwin'e evrimin nasıl gerçekleştiğine dair açıklayıcı bir çerçeve sunan eser ve yazarı hangisidir?",
            {"A": "Malthus'un Nüfus İlkesi Üzerine Bir Deneme'si", "B": "Lamarck'ın evrim kuramı",
             "C": "Erasmus Darwin'in şiirleri", "D": "Mendel'in kalıtım yasaları", "E": "Lyell'in jeoloji ilkeleri"}),
        TestQuestion(7, "Freud'un zihin modelinde, İd'in haz ilkesini dengelemeye başlayan katman hangisidir?",
            {"A": "Süperego", "B": "Bilinçdışı", "C": "Gerçeklik ilkesi (Ego)", "D": "Dasein", "E": "Ön bilinç"}),
        TestQuestion(8, "Freud'un zihin metaforunda 'koridor' neyi temsil eder?",
            {"A": "Bilinci", "B": "Ön bilinci", "C": "Bilinçdışını", "D": "Süperego'yu", "E": "Serbest çağrışımı"}),
        TestQuestion(9, "Bertrand Russell ve G. E. Moore'un öncülerinden olduğu, dilin ve mantığın analizine odaklanan çağdaş felsefe geleneği hangisidir?",
            {"A": "Kıta Felsefesi", "B": "Analitik Felsefe", "C": "Fenomenoloji", "D": "Varoluşçuluk", "E": "Pozitivizm"}),
        TestQuestion(10, "Russell'ın Whitehead ile birlikte yazdığı, matematiği mantıksal ilkelerden türetmeyi amaçlayan eseri hangisidir?",
            {"A": "Neden Hristiyan Değilim", "B": "Principia Mathematica", "C": "Mantıksal Araştırmalar",
             "D": "Varlık ve Zaman", "E": "Sisifos Söyleni"}),
        TestQuestion(11, "Russell'a göre din, aşağıdakilerden hangisine dayanır ve bu yüzden ilerlemeye engeldir?",
            {"A": "Akla", "B": "Bilime", "C": "Korkuya", "D": "Mantığa", "E": "Deneyime"}),
        TestQuestion(12, "Kierkegaard'a göre inanan insanlar için hangi ifade doğrudur?",
            {"A": "Nesnel doğrular öznel doğrulardan daima üstündür", "B": "Öznel doğrular nesnel doğrulardan daima üstündür",
             "C": "Nesnel ve öznel doğrular arasında fark yoktur", "D": "Din, nesnel bir bilimsel olgu olarak kanıtlanmalıdır",
             "E": "Şüphe, gerçek imanla bağdaşmaz"}),
        TestQuestion(13, "Kierkegaard'ın 'İman Şövalyesi'ne giden üç aşaması hangi sırayla ilerler?",
            {"A": "Etik → Estetik → Dinsel", "B": "Dinsel → Etik → Estetik", "C": "Estetik → Etik → Dinsel",
             "D": "Estetik → Dinsel → Etik", "E": "Etik → Dinsel → Estetik"}),
        TestQuestion(14, "Heidegger'in insanın dünyadaki bulunuş halini ve kendi varlığını anlamlandırma kapasitesini ifade etmek için kullandığı kavram hangisidir?",
            {"A": "Fenomenolojik İndirgeme", "B": "Dasein", "C": "Kötü Niyet", "D": "İnanç Sıçraması", "E": "Absürdizm"}),
        TestQuestion(15, "Sartre'a göre insanın özgürlüğünden ve bu özgürlüğün getirdiği sorumluluktan kaçma çabasına ne ad verilir?",
            {"A": "Absürdizm", "B": "Kötü niyet (mauvaise foi)", "C": "Nihilizm", "D": "Fenomenolojik indirgeme", "E": "İnanç sıçraması"}),
        TestQuestion(16, "Camus'nün 'Sisifos Miti' ile özetlediği absürdizm anlayışına göre insan nasıl davranmalıdır?",
            {"A": "Anlamsızlık karşısında hayata küsmelidir", "B": "Anlam arayışından tamamen vazgeçmelidir",
             "C": "Her şeye inat hayatı anlamlandırmaya çalışmalı, mücadeleyi sürdürmelidir", "D": "Dinsel bir otoriteye sığınmalıdır",
             "E": "Toplumsal kurallara mutlak biçimde uymalıdır"}),
        TestQuestion(17, "Nietzsche 'Tanrı Öldü' söylemini hangi eseriyle felsefe literatürüne kazandırmıştır?",
            {"A": "Böyle Buyurdu Zerdüşt", "B": "Şen Bilim", "C": "Güç İstenci",
             "D": "Ecce Homo", "E": "Putların Alacakaranlığı"}),
        TestQuestion(18, "Nietzsche'ye göre insan tiplerinden 'Trajik İnsan' nasıl tanımlanır?",
            {"A": "Bir çobana, kendisini yönetecek bir başa ihtiyaç duyan insan", "B": "Sürüden ayrılmış, dünyayı kendi gözleriyle görmek isteyen insan",
             "C": "Geçmişini tüm yönleriyle kabul edip yaşamı olumlayan insan", "D": "Tanrı'ya mutlak biçimde bağlı kalan insan",
             "E": "Yalnızca bilimsel bilgiye güvenen insan"}),
        TestQuestion(19, "Bentham ve Mill'in haz anlayışı karşılaştırıldığında, aşağıdakilerden hangisi Mill'e (niteliksel faydacılığa) aittir?",
            {"A": "Bütün hazlar temelde aynıdır", "B": "Önemli olan hazzın miktarıdır",
             "C": "Zihinsel hazlar bedensel hazlardan üstündür", "D": "Bedensel ve zihinsel hazlar eşdeğerdir",
             "E": "Haz matematiksel olarak ölçülemez"}),
        TestQuestion(20, "Marx'ın toplum modelinde siyaset, hukuk, din, ahlak ve felsefe gibi kurumlar hangi katmanda yer alır?",
            {"A": "Alt Yapı", "B": "Üst Yapı", "C": "Doğal Üretim Koşulları", "D": "Proletarya", "E": "Üretici Güçler"}),
    ]

    answer_key_items = [
        AnswerItem(1, "C", "Comte'a göre insan düşüncesi <b>Teolojik → Metafizik → Pozitif</b> sırasıyla, hiyerarşik ve zorunlu bir şekilde ilerler."),
        AnswerItem(2, "B", "Comte'un İnsanlık Dini'nde ibadethaneler <b>üniversiteler</b>, din adamları ise <b>bilim insanlarıdır</b>."),
        AnswerItem(3, "C", "Schopenhauer'e göre mutluluk kendi başına pozitif bir durum değildir, yalnızca <b>'acı ve ızdırabın yokluğu'</b>dur (negatif hedonizm)."),
        AnswerItem(4, "A", "Schopenhauer'e göre <b>'yalnızlığı sevmeyen, özgürlüğü sevemez'</b> — yalnızlık ile özgürlük arasında kopmaz bir bağ vardır."),
        AnswerItem(5, "B", "Köpek, yarasa, tavşan ve insan embriyolarının ilk evrelerde birbirinin aynısı olması, Darwin'e göre ortak kökenden gelme tezini güçlendiren kanıtlardan biridir."),
        AnswerItem(6, "A", "Thomas <b>Malthus'un Nüfus İlkesi Üzerine Bir Deneme</b> adlı eseri, Darwin'e evrimin nasıl gerçekleştiğine dair açıklayıcı bir çerçeve sunmuştur."),
        AnswerItem(7, "C", "<b>Gerçeklik ilkesi (Ego)</b>, insan büyüdükçe gelişip İd'in haz ilkesini dengelemeye başlayan katmandır."),
        AnswerItem(8, "C", "Freud'un metaforunda 'koridor', bastırılan düşünce ve travmaların hapsedildiği <b>Bilinçdışı</b>nı temsil eder."),
        AnswerItem(9, "B", "<b>Analitik Felsefe</b>, Russell, Wittgenstein ve Moore'un öncülerinden olduğu, dilin ve mantığın analizine odaklanan çağdaş felsefe geleneğidir."),
        AnswerItem(10, "B", "Russell'ın Whitehead ile birlikte kaleme aldığı <b>Principia Mathematica</b>, matematiği mantıksal ilkelerden türetmeyi amaçlar."),
        AnswerItem(11, "C", "Russell'a göre din akla değil <b>korkuya</b> dayanır ve ilerlemeye engeldir; bu görüşünü Neden Hristiyan Değilim'de savunur."),
        AnswerItem(12, "B", "Kierkegaard'a göre inanan insanlar için <b>öznel doğrular nesnel doğrulardan daima üstündür</b>, çünkü nesnel bilgi varoluşsal anlam için yeterli değildir."),
        AnswerItem(13, "C", "İman Şövalyesi'ne giden yol <b>Estetik → Etik → Dinsel</b> aşamalar sırasıyla ilerler."),
        AnswerItem(14, "B", "<b>Dasein (orada-varlık)</b>, Heidegger'in insanın dünyadaki bulunuş halini ve varlığı anlamlandırma yetisini ifade etmek için kullandığı kavramdır."),
        AnswerItem(15, "B", "Sartre, insanın özgürlükten ve bu özgürlüğün getirdiği sorumluluktan kaçma çabasına <b>'kötü niyet' (mauvaise foi)</b> adını vermiştir."),
        AnswerItem(16, "C", "Camus'ye göre absürtlüğe rağmen insan hayata küsmemeli, <b>her şeye inat hayatı anlamlandırmaya çalışmalı ve mücadeleyi sürdürmelidir</b> — Sisifos'un ebedi mücadelesi gibi."),
        AnswerItem(17, "B", "Nietzsche, 'Tanrı Öldü' söylemini <b>Şen Bilim</b> adlı eseriyle felsefe literatürüne kazandırmıştır; 'Üstinsan' ise Böyle Buyurdu Zerdüşt'te sistemleşir."),
        AnswerItem(18, "C", "<b>Trajik İnsan</b>, geçmişini iyi ve kötü tüm yönleriyle kabul edip yaşamı olumlayan, yaşamın anlamsızlığını anlayan insan tipidir."),
        AnswerItem(19, "C", "Mill'in niteliksel faydacılığına göre <b>zihinsel hazlar</b>, bedensel hazlardan her zaman daha üstündür; Bentham ise tüm hazları nicelik olarak eşit sayar."),
        AnswerItem(20, "B", "Siyaset, hukuk, din, ahlak ve felsefe gibi kurumlar Marx'ın modelinde <b>Üst Yapı</b>'yı oluşturur; alt yapı ise maddi üretim koşullarını kapsar."),
    ]

    return CoursePack(
        course_code="ÇAĞD. FELSEFE",
        title='Çağdaş <span class="accent-word">Felsefe</span>',
        subtitle="Öğretmen Notlarıyla Pozitivizmden Varoluşçuluğa 20. Yüzyıl Düşünce Akımları",
        description=(
            "Öğretmenin kendi dikte notlarından toparlanmış çalışma rehberi: Comte'un pozitivizminden "
            "Schopenhauer'ın kötümserliğine, Darwin ve Freud'un bilimsel devrimlerinden Russell'ın analitik "
            "felsefesine, Kierkegaard'ın varoluşçu öncülüğünden Nietzsche'nin Üstinsan idealine ve "
            "faydacılıktan Marx'ın tarihsel maddeciliğine uzanan, sınavda en çok karıştırılan noktaların "
            "ayrıca işaretlendiği kapsamlı bir çağdaş felsefe özeti."
        ),
        theme="slate",
        theme_color="#1C5C69",
        icon_text="Ç",
        chapters=chapters,
        glossary=glossary,
        test_title="Genel Değerlendirme Testi",
        test_subtitle="Comte'tan Marx'a, çağdaş felsefe tarihi üzerine kapsamlı çoktan seçmeli test",
        test_instructions="Aşağıdaki sorularda beş seçenekten yalnızca birini işaretleyiniz. Süre: 30 dakika.",
        test_questions=test_questions,
        answer_key_intro="Her sorunun doğru cevabı ve kısa gerekçesi aşağıda yer almaktadır.",
        answer_key_items=answer_key_items,
        overview_lead=(
            "Bu ders, bir öğretmenin kendi dikte notlarını toparlayıp düzelttiği bir çalışma rehberine "
            "dayanır: <b>Comte'un pozitivizminden</b> <b>Schopenhauer'ın kötümserliğine</b>, "
            "<b>Darwin ve Freud'un bilimsel devrimlerinden</b> <b>Russell'ın analitik felsefesine</b>, "
            "<b>Kierkegaard'dan Sartre ve Camus'ye uzanan varoluşçuluğa</b> ve <b>Nietzsche'den Marx'a</b> "
            "kadar çağdaş felsefenin yedi temel durağını bir bütün olarak sunar."
        ),
        overview_cards=[
            {"title": "Pozitivizm ve Kötümser Felsefe", "text": "Comte'un bilim temelli Üç Hal Yasası ile Schopenhauer'ın irade kötümserliği."},
            {"title": "Evrim ve Psikanaliz", "text": "Darwin'in doğal seçilimi ile Freud'un bilinçdışı keşfi."},
            {"title": "Analitik Felsefe", "text": "Çağdaş felsefenin iki damarı ve Russell'ın mantıksal atomculuğu, din eleştirisi."},
            {"title": "Varoluşçuluğun Kökleri", "text": "Kierkegaard'ın öznel doğrusundan Husserl ve Heidegger'in fenomenolojisine."},
            {"title": "Varoluşçuluk", "text": "Sartre'ın özgürlük/sorumluluk anlayışı ve Camus'nün Sisifos Miti ile absürdizmi."},
            {"title": "Güç İstenci, Faydacılık ve Marx", "text": "Nietzsche'nin Üstinsan idealinden Bentham/Mill'in faydacılığına ve Marx'ın tarihsel maddeciliğine."},
        ],
        overview_flow=[
            ("Pozitivizm & Kötümserlik", "Comte, Schopenhauer"),
            ("Evrim & Psikanaliz", "Darwin, Freud"),
            ("Analitik Felsefe", "Russell"),
            ("Kıta Felsefesi", "Kierkegaard, Husserl, Heidegger, Sartre, Camus"),
            ("Güç İstenci & Toplum Felsefesi", "Nietzsche, Bentham, Mill, Marx"),
        ],
        overview_note=(
            "Bu kitaptaki <b>mavi 'Notlardaki Bir Hata'</b> kutucukları, öğretmenin kendi dikte "
            "notlarındaki hataları (yanlış tarih, karıştırılan kavram, yarım kalan cümle) fark edip "
            "düzelttiği noktaları işaretler — sınavda en çok karıştırılan ayrımlar genelde tam da bu "
            "noktalarda gizlidir."
        ),
    )
