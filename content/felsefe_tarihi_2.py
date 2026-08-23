# -*- coding: utf-8 -*-
"""FELSEFE TARİHİ II — Görsel Ders Notu Kitabı, içerik tanımı.
Kaynak: 'FELSEFE TARİHİ 2_FİNAL ÖZET.pdf' (ham metin özet, 17 sayfa, 9 bölüm).
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
    tagline="Pozitivizmin Kurucusu, Sosyolojinin İsim Babası",
    bio=["Başyapıtı <b>Pozitif Felsefe Dersleri</b>'nde bilimsel bilgiyi tek geçerli bilgi sistemi ilan etmiş; "
         "Saint-Simon'un yanında yıllarca sekreterlik yaparak yetişmiş ve 'Sosyoloji' adını verdiği bilimin "
         "kurucusu olmuştur."],
    key_work="Pozitif Felsefe Dersleri",
)
SCHOPENHAUER = Person(
    id="schopenhauer", name="Arthur Schopenhauer", years="1788–1860",
    tagline="Kötümser İrade Felsefesinin Kurucusu",
    bio=["Başyapıtı <b>İsteme ve Tasarım Olarak Dünya</b>'da evrenin temelinde doymak bilmeyen bir 'irade' "
         "bulunduğunu, mutluluğun ise yalnızca acının yokluğu olduğunu savunarak yaşamı köklü bir kötümserlikle "
         "yorumlamıştır."],
    key_work="İsteme ve Tasarım Olarak Dünya",
)
NIETZSCHE = Person(
    id="nietzsche", name="Friedrich Nietzsche", years="1844–1900",
    tagline="'Tanrı Öldü' Diyen Yaşam Filozofu",
    bio=["Başyapıtı <b>Böyle Buyurdu Zerdüşt</b>'te 'Üst İnsan' idealini sistemleştirmiş; 'Tanrı Öldü' söylemini "
         "<b>Şen Bilim</b> ile felsefe literatürüne kazandırarak geleneksel ahlakı ve Hristiyanlığı sertçe "
         "eleştirmiştir."],
    key_work="Böyle Buyurdu Zerdüşt",
)
BENTHAM = Person(
    id="bentham", name="Jeremy Bentham", years="1748–1832",
    tagline="Klasik (Niceliksel) Faydacılığın Kurucusu",
    bio=["'En büyük mutluluk ilkesi'ni savunarak eylemlerin ahlaki değerinin, sonuçlarının yarattığı haz/acı "
         "dengesiyle matematiksel biçimde ölçülebileceğini iddia etmiş; gözetim mimarisi <b>Panoptikon</b>'u "
         "tasarlamıştır."],
    key_work="Panoptikon (mimari tasarım)",
)
MILL = Person(
    id="mill", name="John Stuart Mill", years="1806–1873",
    tagline="Özgürlükçü (Liberal) Faydacılığın Öncüsü",
    bio=["Bentham'ın faydacılığını 'hazlar arasında nitelik farkı vardır' ilkesiyle geliştirmiş; "
         "<b>Özgürlük Üzerine</b> adlı eserinde bireysel özgürlüğü, <b>Kadınların Boyunduruk Altında</b> adlı "
         "eserinde toplumsal cinsiyet eşitliğini savunmuştur."],
    key_work="Özgürlük Üzerine",
)
MARX = Person(
    id="marx", name="Karl Marx", years="1818–1883",
    tagline="Diyalektik Materyalizmin Kurucusu",
    bio=["Toplumu alt yapı (ekonomi) ile üst yapı (kurumlar) arasındaki çatışma olarak yorumlamış; Friedrich "
         "Engels ile birlikte yayımladığı <b>Komünist Manifesto</b>'da proletarya diktatörlüğü yoluyla sınıfsız "
         "bir düzen hedeflemiştir."],
    key_work="Komünist Manifesto",
)
DARWIN = Person(
    id="darwin", name="Charles Darwin", years="1809–1882",
    tagline="Doğal Seçilim Yoluyla Evrim Teorisinin Kurucusu",
    bio=["5 yıllık dünya turunda, özellikle Galapagos adalarında topladığı kanıtlarla türlerin ortak bir "
         "kökenden <b>Doğal Seçilim</b> yoluyla evrimleştiğini, başyapıtı <b>İnsanın Türeyişi</b>'nde ortaya "
         "koymuştur."],
    key_work="İnsanın Türeyişi",
)
FREUD = Person(
    id="freud", name="Sigmund Freud", years="1856–1939",
    tagline="Psikanalizin Kurucusu",
    bio=["İnsan davranışlarının akıl değil bilinçdışı dürtüler tarafından yönetildiğini savunmuş; zihni "
         "İd-Ego-Süperego üçlüsüyle modellemiş ve <b>Rüya Yorumu</b> ile bilinçdışına ulaşmanın yollarını "
         "sistemleştirmiştir."],
    key_work="Rüya Yorumu",
)
RUSSELL = Person(
    id="russell", name="Bertrand Russell", years="1872–1970",
    tagline="Modern Analitik Felsefenin Kurucularından",
    bio=["G. E. Moore ile birlikte analitik felsefeyi kurmuş; Whitehead ile yazdığı <b>Principia Mathematica</b> "
         "ile matematiği mantığa indirgemeye çalışmış, savaş karşıtı eylemciliği nedeniyle Nobel Edebiyat "
         "Ödülü'nü kazanmıştır."],
    key_work="Principia Mathematica",
)
KIERKEGAARD = Person(
    id="kierkegaard", name="Søren Kierkegaard", years="1813–1855",
    tagline="Varoluşçuluğun Öncüsü, 'İman Şövalyesi' Kavramının Sahibi",
    bio=["İnsanın estetik, etik ve dinsel aşamalardan geçerek akla değil <b>İnanç Sıçraması</b>'na dayanan "
         "öznel bir hakikate ulaşması gerektiğini savunmuş; bu tutkulu inancı taşıyan ideal bireyi 'İman "
         "Şövalyesi' olarak adlandırmıştır."],
    key_work="Korku ve Titreme",
)
HUSSERL = Person(
    id="husserl", name="Edmund Husserl", years="1859–1938",
    tagline="Fenomenolojinin Kurucusu",
    bio=["Kesin bilgiye ulaşmak için önyargılardan sıyrılıp yalnızca bilincin deneyimine odaklanılmasını "
         "öngören <b>Fenomenolojik İndirgeme</b> yöntemini geliştirmiştir."],
    key_work="Mantıksal Araştırmalar",
)
HEIDEGGER = Person(
    id="heidegger", name="Martin Heidegger", years="1889–1976",
    tagline="'Dasein' Kavramıyla Varlığı Sorgulayan Filozof",
    bio=["Husserl'ın öğrencisi olarak fenomenolojiyi varlık sorusu etrafında yeniden şekillendirmiş; insanı "
         "zaman, ölüm ve kaygı üzerinden çözümlediği başyapıtı <b>Varlık ve Zaman</b>'ı yazmıştır."],
    key_work="Varlık ve Zaman",
)
SARTRE = Person(
    id="sartre", name="Jean-Paul Sartre", years="1905–1980",
    tagline="'Önce Varoluş, Sonra Öz' İlkesinin Sahibi",
    bio=["İnsanın mutlak biçimde özgür ve bu özgürlükten sorumlu olduğunu savunmuş; bu sorumluluktan kaçışı "
         "'kötü niyet' kavramıyla adlandırdığı başyapıtı <b>Varlık ve Hiçlik</b>'te temellendirmiştir."],
    key_work="Varlık ve Hiçlik",
)
CAMUS = Person(
    id="camus", name="Albert Camus", years="1913–1960",
    tagline="Absürdizm ve Sisifos Miti",
    bio=["İnsanın anlam arayışı ile dünyanın sessizliği arasındaki uyumsuzluğu 'absürt' olarak tanımlamış; "
         "<b>Sisifos Söyleni</b> adlı denemesinde bu anlamsızlığa rağmen yaşamı seçmenin bir başkaldırı "
         "olduğunu savunmuştur."],
    key_work="Sisifos Söyleni",
)


def get_pack() -> CoursePack:

    # =====================================================================
    # BÖLÜM 1 — Pozitivizm ve Sosyolojinin Doğuşu (Auguste Comte)
    # =====================================================================
    ch1 = Chapter(
        number=1,
        title="Pozitivizm ve Sosyolojinin Doğuşu",
        subtitle="Auguste Comte'un bilimsel bilgiyle toplumu yeniden inşa etme projesi",
        key_terms=[
            KeyTerm("Pozitivizm", "Olgulara dayanan, yalnızca deney ve gözlem yoluyla doğrulanabilir bilimsel bilgiyi geçerli sayan felsefi akım."),
            KeyTerm("Sosyal Fizik", "Comte'un başlangıçta toplum bilimi için kullandığı, daha sonra 'Sosyoloji' adını verdiği kavram."),
            KeyTerm("Üç Hal Yasası", "İnsan düşüncesinin ve toplumsal evrimin teolojik, metafizik ve bilimsel olmak üzere üç zorunlu aşamadan geçtiğini savunan felsefi kural."),
            KeyTerm("İnsanlık Dini", "Bilime ve akla dayalı, toplumun birliğini ve ilerlemesini sağlamak için kurgulanmış, geleneksel dinlerin yerini alması hedeflenen seküler din anlayışı."),
        ],
    )
    ch1.pages.append(
        ChapterPage()
        .add_terms(ch1.key_terms)
        .add_person(COMTE)
        .add_block(BulletBlock(1, "Hayatı ve Entelektüel Kökleri", [
            "1798'de Fransa'da doğmuş, Katolik bir ailede yetişmiş ancak 14 yaşında kiliseden ayrılarak ailesinin "
            "büyük tepkisini çekmiştir.",
            "Pozitivizmin öncülerinden Saint-Simon ile tanışmış, onun yanında asistanlık ve 7 yıl boyunca "
            "sekreterlik yapmıştır.",
            "Felsefi düşüncelerinin şekillenmesinde <b>Montesquieu, Immanuel Kant ve David Hume</b>'un önemli "
            "etkileri olmuştur.",
        ]))
    )
    ch1.pages.append(
        ChapterPage()
        .add_block(BulletBlock(2, "Sosyolojinin Doğuşu ve Pozitif Felsefe", [
            "Comte, sosyoloji biliminin isim babasıdır; 'Sosyal Fizik' adını verdiği bu alanın bağımsız bir "
            "bilim olarak ortaya çıkmasını sağlamıştır.",
            "Felsefi sisteminin mottosu: <b>'İlke olarak aşk, temel olarak düzen, amaç olarak ilerleme.'</b>",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("Teolojik Aşama", "Açıklamalar Tanrı/tanrısal güçlerle yapılır"),
            FlowStep("Metafizik Aşama", "Soyut kavramlarla (hak, hukuk, eşitlik) açıklanır"),
            FlowStep("Pozitif Aşama", "Bilimsel, doğrulanabilir yöntemlerle açıklanır"),
        ], caption="Comte'un Üç Hal Yasası: İnsan Düşüncesinin ve Toplumun Evrimi"))
        .add_table(ComparisonTable(
            "İnsanlık Dini'nin Kutsalları",
            ["Kavram", "Karşılığı"],
            [
                ["Yüce Varlık", "İnsanlığın kendisi"],
                ["Büyük Fetiş", "Dünya / Doğa"],
                ["Büyük Ortam", "Uzay"],
            ]
        ))
        .add_callout(Callout("insight", "Kritik Odak: Pozitif Felsefe Dersleri",
            "Comte'un 6 ciltlik başyapıtı, bilimsel bilginin tek geçerli sistem olduğunu kanıtlamaya çalışır. "
            "3. (Pozitif) aşamada toplumu bir arada tutmak için önerdiği <b>İnsanlık Dini</b>'nin ibadethaneleri "
            "üniversiteler, din adamları ise bilim insanlarıdır."))
        .add_summary("Auguste Comte, bilimi tek geçerli bilgi kaynağı (Pozitivizm) olarak konumlandırıp Üç Hal "
            "Yasası ile insanlığın gelişimini sistemleştirmiş; toplumsal düzeni sağlamak için 'Sosyoloji' "
            "bilimini kurmuş ve geleneksel dinlerin yerini alacak bilime dayalı bir 'İnsanlık Dini' inşa "
            "etmiştir.")
    )

    # =====================================================================
    # BÖLÜM 2 — Kötümserlikten Güç İstencine (Schopenhauer & Nietzsche)
    # =====================================================================
    ch2 = Chapter(
        number=2,
        title="Kötümserlikten Güç İstencine",
        subtitle="Schopenhauer'ın irade felsefesinden Nietzsche'nin Üst İnsan idealine",
        key_terms=[
            KeyTerm("İrade (İsteme)", "Schopenhauer felsefesinde evrenin ve insanın temelini oluşturan, doymak bilmeyen içsel arzu."),
            KeyTerm("Pesimizm (Kötümserlik)", "Yaşamın özünde acı ve tatminsizlik olduğunu savunan, Schopenhauer'un felsefesine yön veren karamsar bakış açısı."),
            KeyTerm("Güç İstenci (İstemi)", "Nietzsche'ye göre insanın ve doğadaki her canlının sadece hayatta kalmayı değil, gücünü artırmayı ve kendini aşmayı arzuladığı temel yaşam enerjisi."),
            KeyTerm("Üst İnsan (Übermensch)", "Nietzsche'de geleneksel ahlakı ve değerleri aşmış, kendi değerlerini kendisi yaratan, yaşamı bütünüyle olumlayan ideal insan modeli."),
        ],
    )
    ch2.pages.append(
        ChapterPage()
        .add_terms(ch2.key_terms)
        .add_person(SCHOPENHAUER)
    )
    ch2.pages.append(
        ChapterPage()
        .add_block(BulletBlock(1, "Hayatı ve Felsefesinin Temeli", [
            "1788 yılında doğmuş, felsefesinin merkezine insanın içsel arzularını ve 'irade' kavramını "
            "yerleştirmiştir.",
            "Leibniz'in iyimser felsefesini sert bir dille eleştirir: ona göre dünya ızdırap ve acıyı içinde "
            "barındırır; mutluluk ise pozitif bir durum değil, yalnızca <b>'acı ve ızdırabın yokluğu'</b>dur.",
        ]))
        .add_block(BulletBlock(2, "Yaşam, Acı ve Beklentiler", [
            "Ona göre yaşam; acıdan, tatminsizlikten ve karşılanması güç arzulardan ibarettir.",
            "Gerçekçi olmayan beklentilerin asıl kaynağı, insanların içindeki aşırı mutluluk arzusudur — bu "
            "yüzden çok mutsuz olmanın en güvenilir yolu, mutlu olmayı istemektir.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("Aşırı Arzu", "Karşılanması güç beklentiler"),
            FlowStep("Acı ve Mutsuzluk", "Beklenti karşılanmayınca doğan sonuç"),
            FlowStep("Ilımlılık + Çilecilik", "Arzuların bastırılması, kendini keşfetme"),
            FlowStep("En Yüksek İyilik", "Acı ve ızdırabın yokluğu"),
        ], caption="Schopenhauer'a Göre Mutluluğa Ulaşma Yolu"))
        .add_block(BulletBlock(3, "Yalnızlık ve Özgürlük İlişkisi", [
            "Gençler yalnızlığa katlanmayı öğrenmelidir; yalnızlık, mutluluğun ve içsel huzurun yegane "
            "kaynağıdır — insan ancak yalnız kaldığı sürece kendisi olabilir.",
            "Yalnızlık ile özgürlük arasında kopmaz bir bağ vardır: <b>yalnızlığı sevmeyen, özgürlüğü de "
            "sevemez.</b>",
        ]))
        .add_callout(Callout("focus", "Kritik Odak: İsteme ve Tasarım Olarak Dünya",
            "Schopenhauer'un başyapıtı; mutluluğun kendi başına var olan pozitif bir durum değil, yalnızca "
            "<b>'acı ve ızdırabın yokluğu'</b> olduğunu savunur."))
    )
    ch2.pages.append(
        ChapterPage()
        .add_terms([
            KeyTerm("Nihilizm (Hiççilik)", "Hayatın, ahlakın, bilginin ve değerlerin nesnel bir temeli veya içsel bir anlamı olmadığını savunan felsefi görüş."),
            KeyTerm("Sürü İnsanı", "Kendi kararlarını alamayan, yönetilmek için sürekli bir lidere veya otoriteye ihtiyaç duyan itaatkâr insan tipi."),
            KeyTerm("Trajik İnsan", "Nietzsche'ye göre geçmişini kabul eden, yaşamı tüm acılarına rağmen olumlayan nihai insan evresi."),
            KeyTerm("Özgür İnsan", "Sürüden ayrılmayı başarmış, dünyayı kendi gözleriyle görmek ve anlamlandırmak isteyen insan."),
        ])
        .add_person(NIETZSCHE)
        .add_block(BulletBlock(1, "Hayatı ve Entelektüel Dönüşümü", [
            "1844'te Saksonya'da doğmuş; daha 13 yaşındayken kötülük olgusu üzerine düşünmeye başlamış, "
            "gençliğinde Schopenhauer'un felsefesinden derinden etkilenmiştir.",
            "1882'de Lou Andreas-Salomé ile tanışmış, evlenme teklifi reddedilmiş; bu hayal kırıklığı sonraki "
            "eserlerine ilham vermiştir.",
            "1889'da Torino'da yaşadığı zihinsel çöküşle akıl hastanesine kaldırılmış, 1900'de vefat etmiştir.",
        ]))
        .add_block(BulletBlock(2, "Felsefi Yıkım: Eleştiri ve Din Karşıtlığı", [
            "Felsefesinin kalbinde 'eleştiri' yatar; Kant, Hegel ve Schopenhauer'ın yanı sıra Avrupa kültürünü "
            "ve Katolik Hristiyanlığını sertçe eleştirir.",
            "Yeryüzündeki tüm dinlerin ve politik görüşlerin insanoğlunun özgürce gelişmesini engellediğini, bu "
            "yüzden yıkılması gerektiğini savunur.",
        ]))
    )
    ch2.pages.append(
        ChapterPage()
        .add_block(BulletBlock(3, "Güç İstenci ve Mutluluk Anlayışı", [
            "Nietzsche'ye göre her canlı sadece var olmak değil, güçlü olmak da ister; mutluluk pasif bir "
            "hazda değil, güçtedir. Güç istenci herkes için geçerlidir: <b>filozof</b> hakikatin peşinde "
            "koşarak, <b>sanatçı</b> eser üreterek, <b>iş insanı</b> zengin olarak güç istencini bulur.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("Sürü İnsanı", "Bir çobana / otoriteye ihtiyaç duyar"),
            FlowStep("Özgür İnsan", "Dünyayı kendi gözleriyle görür"),
            FlowStep("Trajik İnsan", "Yaşamı tüm acılarına rağmen olumlar"),
        ], caption="İnsanın Zihinsel Evrimi: Sürüden Üst İnsana"))
        .add_callout(Callout("route", "Kritik Odak: 'Tanrı Öldü' ve Üst İnsan",
            "Nietzsche, 'Tanrı Öldü' söylemini <b>Şen Bilim</b> ile felsefe literatürüne kazandırmıştır. "
            "İnsanlığı anlamsızlıktan (Nihilizm) kurtaracak yegane güç olarak <b>'Üst İnsan'</b> kavramını, "
            "başyapıtı <b>Böyle Buyurdu Zerdüşt</b>'te sistemleştirmiştir."))
        .add_summary("Arthur Schopenhauer, evrenin temelindeki içsel arzuların doymak bilmez doğası yüzünden "
            "yaşamı bir acı ve tatminsizlik süreci olarak tanımlarken; onun öğrencisi sayılan Friedrich "
            "Nietzsche bu kötümserliği tersine çevirir: geleneksel ahlakı yıkıcı biçimde eleştirip 'Tanrı "
            "Öldü' fikrini ortaya atmış, yaşamın itici gücünün acıdan kaçış değil 'Güç İstenci' olduğunu "
            "savunarak insanın sürü psikolojisinden kurtulup kendi değerlerini yaratan 'Üst İnsan' mertebesine "
            "ulaşması gerektiğini müjdelemiştir.")
    )

    # =====================================================================
    # BÖLÜM 3 — Faydacılık (Jeremy Bentham ve John Stuart Mill)
    # =====================================================================
    ch3 = Chapter(
        number=3,
        title="Faydacılık (Utilitarizm)",
        subtitle="Jeremy Bentham'ın niceliksel ve John Stuart Mill'in niteliksel faydacılığı",
        key_terms=[
            KeyTerm("Faydacılık (Utilitarizm)", "Bir eylemin ahlaki değerini, en çok sayıda insan için en yüksek düzeyde fayda ve mutluluk sağlama kapasitesine göre ölçen felsefi yaklaşım."),
            KeyTerm("Hedonizm (Hazcılık)", "Mutluluğu hazza (zevk) ulaşıp acıdan kaçınmak olarak tanımlayan yaklaşım."),
            KeyTerm("Panoptikon", "Bentham tarafından tasarlanan; merkezdeki tek bir gözlemcinin, mahkumların kendilerini her an izleniyormuş gibi hissetmesini sağlayan mimari gözetim modeli."),
            KeyTerm("Zarar İlkesi", "Mill'in felsefesinde, bireyin özgürlüğünün tek sınırının 'başkalarına zarar vermemek' olduğunu savunan kural."),
        ],
    )
    ch3.pages.append(
        ChapterPage()
        .add_terms(ch3.key_terms)
        .add_person_row([BENTHAM, MILL])
    )
    ch3.pages.append(
        ChapterPage()
        .add_block(BulletBlock(1, "Jeremy Bentham: Klasik Faydacılık ve Toplumsal Hukuk", [
            "1748–1832 yıllarında yaşamış İngiliz filozof, hukukçu ve sosyal reformcudur; Faydacılık "
            "felsefesinin kurucusu kabul edilir.",
            "Temel mottosu: <b>'En büyük mutluluk ilkesi, en çok sayıda insan için en büyük mutluluğu "
            "sağlamaktır.'</b> Eylemlerin ahlaki değeri, niyetlere göre değil sonuçlarına göre değerlendirilir.",
            "Yasaların tek amacının toplumda en yüksek faydayı sağlamak olduğunu, cezaların intikam değil "
            "suçun topluma verdiği zarara orantılı olması gerektiğini savunur.",
        ]))
        .add_block(BulletBlock(2, "John Stuart Mill: Özgürlükçü (Liberal) Faydacılık", [
            "1806–1873 yıllarında yaşamış İngiliz filozof, ekonomist ve liberal düşüncenin en büyük "
            "öncülerinden biridir.",
            "Bentham'ın sistemini devralarak geliştirmiş; ahlaki eylemin temelini yine 'en büyük mutluluk "
            "ilkesi'ne bağlamıştır (Mutluluk = Hazların artması + Acıların azalması).",
            "<b>Özgürlük Üzerine</b> adlı eserinde bireysel özgürlüklerin mutlak korunması gerektiğini, "
            "başkasına zarar vermediği sürece her bireyin tamamen özgür olması gerektiğini vurgular.",
        ]))
        .add_table(ComparisonTable(
            "Karşılaştırma Tablosu: Bentham ve Mill'in 'Haz' Anlayışındaki Fark",
            ["Özellik", "Jeremy Bentham (Niceliksel)", "John Stuart Mill (Niteliksel)"],
            [
                ["Hazzın Doğası", "Bütün hazlar temelde aynıdır; önemli olan hazzın miktarıdır.", "Hazlar arasında kalite farkı vardır; niteliği miktarından daha önemlidir."],
                ["Haz Türleri", "Bedensel ve zihinsel hazlar eşdeğerdir.", "Zihinsel/entelektüel hazlar bedensel hazlardan her zaman üstündür."],
            ]
        ))
        .add_callout(Callout("caution", "Dikkat: Zarar İlkesi",
            "Mill'e göre bireyin özgürlüğünün tek sınırı <b>'başkalarına zarar vermemek'</b>tir; "
            "<b>Kadınların Boyunduruk Altında</b> adlı eserinde ise toplumsal cinsiyet eşitliğini ateşli bir "
            "şekilde savunmuştur."))
    )
    ch3.pages.append(
        ChapterPage()
        .add_summary("Jeremy Bentham, eylemlerin ahlaki ve hukuki değerini toplumun çoğunluğuna sağladığı "
            "matematiksel 'haz/fayda' hesabı üzerine inşa ederken; halefi John Stuart Mill bu görüşü revize "
            "ederek zihinsel hazları bedensel hazlardan üstün tutmuş ve faydacılığı bireysel özgürlükleri "
            "merkeze alan liberal bir temele oturtmuştur.")
    )

    # =====================================================================
    # BÖLÜM 4 — Diyalektik Materyalizm ve Yabancılaşma (Karl Marx)
    # =====================================================================
    ch4 = Chapter(
        number=4,
        title="Diyalektik Materyalizm ve Yabancılaşma",
        subtitle="Karl Marx'ta alt yapı-üst yapı çatışması, sınıf mücadelesi ve yabancılaşma",
        key_terms=[
            KeyTerm("Alt Yapı ve Üst Yapı", "Alt yapı toplumun maddi üretim koşullarını ve üretici güçlerini; üst yapı ise siyaset, hukuk, din, ahlak ve felsefe gibi bu zemin üzerinde yükselen kurumları kapsar."),
            KeyTerm("Diyalektik Materyalizm", "Evrendeki ve toplumdaki değişimi, maddi unsurların (alt yapı ve üst yapı) birbiriyle olan çatışması üzerinden açıklayan felsefi yöntem."),
            KeyTerm("Yabancılaşma", "Kapitalist düzende işçinin ürettiği ürüne, kendi emeğine ve en nihayetinde kendi öz doğasına (insanlığına) giderek uzaklaşması durumu."),
            KeyTerm("Proletarya ve Burjuvazi", "Üretim araçlarına sahip olmayıp emeğini satan işçi sınıfı (Proletarya) ile üretim araçlarını elinde tutan sermaye sınıfı (Burjuvazi)."),
        ],
    )
    ch4.pages.append(
        ChapterPage()
        .add_terms(ch4.key_terms)
        .add_person(MARX)
        .add_block(BulletBlock(1, "Alt Yapı ve Üst Yapı Modeli", [
            "Marx, toplumsal yapıyı birbiriyle sürekli etkileşim ve çatışma halinde olan iki ana katmana "
            "ayırır. Ahlak açısından neyin doğru ya da yanlış kabul edileceği doğrudan toplumsal 'alt "
            "yapı'nın bir ürünüdür — bu yüzden felsefesi 'Diyalektik Materyalizm' olarak adlandırılır.",
        ]))
    )
    ch4.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Alt Yapının İç Hiyerarşisi",
            ["Katman", "İçerik"],
            [
                ["Doğal Üretim Koşulları", "Doğal kaynaklar, iklim koşulları ve hammaddeler — sistemin en temeli."],
                ["Üretici Güçler", "İnsanların üretimde kullandığı araç, gereç, alet ve makineler."],
                ["Üst Yapı (Toplumsal Bilinç)", "Toplumun düşünüş tarzı, politik kurumları, yasaları, dini, ahlakı, sanatı ve felsefesi."],
            ]
        ))
        .add_block(BulletBlock(2, "Sınıf Çatışması ve Yabancılaşma", [
            "İçinde bulunulan dönem, Burjuvazi (Kapitalistler) ile Proletarya (İşçiler) arasındaki büyük bir "
            "sınıf çatışması dönemidir. İnsanın bilinci çalışma koşulları tarafından belirlenir: <b>'Bana ne "
            "iş yaptığını söyle, sana kim olduğunu söyleyeyim.'</b>",
            "Kapitalist üretim ilişkilerinde işçi kendisi için değil, sermayedar adına çalışmak zorundadır — bu "
            "durum işçinin kendi ürettiği emeğine, değerine ve kendi doğasına <b>yabancılaşmasına</b> neden olur.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("İşçi Sınıfının Başkaldırısı"),
            FlowStep("Üretim Araçlarının Ele Geçirilmesi"),
            FlowStep("Proletarya Diktatörlüğü", "Burjuvazinin baskı altına alınması"),
            FlowStep("Yabancılaşmanın Sona Ermesi", "Emeğin halka ait olması"),
        ], caption="Proletarya Devrimi Akış Şeması"))
        .add_callout(Callout("insight", "Marx Sonrası Komünist Hareket",
            "Marx, yakın çalışma arkadaşı Friedrich Engels ile birlikte <b>Komünist Manifesto</b>'yu "
            "yayımlamıştır. Fikirleri doğrultusunda gelişen hareket ilerleyen dönemde iki ana kola "
            "ayrılmıştır: <b>Sosyal Demokrasi</b> ve <b>Leninizm</b>."))
    )
    ch4.pages.append(
        ChapterPage()
        .add_summary("Karl Marx, tarihi alt yapı (ekonomi) ve üst yapı (kurumlar) arasındaki çatışma olarak "
            "yorumlamış; kapitalizmin işçiyi kendi emeğine yabancılaştırdığını savunarak, proletarya "
            "diktatörlüğü aracılığıyla üretim araçlarının halka geçeceği sınıfsız bir komünist düzen hedefini "
            "'Komünist Manifesto' ile sistemleştirmiştir.")
    )

    # =====================================================================
    # BÖLÜM 5 — Bilimsel Devrimler: Evrim ve Psikanaliz (Charles Darwin ve Sigmund Freud)
    # =====================================================================
    ch5 = Chapter(
        number=5,
        title="Bilimsel Devrimler: Evrim ve Psikanaliz",
        subtitle="Charles Darwin'in doğal seçilimi ve Sigmund Freud'un bilinçdışı keşfi",
        key_terms=[
            KeyTerm("Doğal Seçilim", "Doğada çevre şartlarına en iyi uyum sağlayan canlıların hayatta kalması ve üremesi, zayıf olanların ise elenmesi süreci."),
            KeyTerm("Psikanaliz (Ruh Çözümlemesi)", "Freud tarafından geliştirilen, insan davranışlarının temelinde yatan bilinçdışı süreçleri ve akıl dışı dürtüleri inceleyen psikolojik kuram."),
            KeyTerm("İd-Ego-Süperego", "Freud'un zihin modeli: İlkel haz dürtüleri (İd), gerçekliği dengeleyen akıl (Ego) ve içselleştirilmiş ahlaki beklentiler (Süperego)."),
            KeyTerm("Bilinçdışı (Karanlık Koridor)", "Bastırılmaya çalışılan düşüncelerin, travmaların ve unutulmak istenen anıların hapsedildiği zihinsel alan."),
        ],
    )
    ch5.pages.append(
        ChapterPage()
        .add_terms(ch5.key_terms)
        .add_person(DARWIN)
        .add_block(BulletBlock(1, "Charles Darwin ve Evrim Teorisi", [
            "1809'da doktor bir babanın çocuğu olarak doğmuş; küçük yaşlardan itibaren doğa bilimlerine ve "
            "jeolojiye ilgi duymuştur.",
            "5 yıl süren bir dünya turuna çıkmış, Güney Amerika'nın haritasını çıkarmış ve özellikle Galapagos "
            "adalarında kritik çalışmalar yapmıştır.",
        ]))
    )
    ch5.pages.append(
        ChapterPage()
        .add_block(BulletBlock(2, "Doğal Seçilim ve Evrimin Kanıtları", [
            "Teorisi iki temel tez üzerine kuruludur: biyolojik evrimin varlığı ve bu evrimin 'Doğal Seçilim' "
            "yoluyla gerçekleştiği.",
            "<b>Kanıtlar:</b> Deniz hayvanı fosillerinin yüksek dağların tepesinde bulunması, canlı türlerinin "
            "coğrafi dağılımı ve köpek-yarasa-tavşan-insan embriyolarının ilk evrelerde birbirinin aynısı "
            "olması, tüm canlıların ortak bir kökenden geldiği tezini güçlendirir.",
            "Doğal seçilimin nasıl işlediğini kavraması, Thomas Malthus'un 'Nüfus İlkesi Üzerine Bir Deneme' "
            "adlı kitabını okumasıyla mümkün olmuştur.",
        ]))
        .add_person(FREUD)
        .add_block(BulletBlock(3, "Freud ve Ruh Arkeolojisi", [
            "1856'da doğan Freud, davranışlarımızın her zaman aklımız tarafından değil, çoğu zaman 'akıl dışı "
            "dürtüler' tarafından yönetildiğini savunmuştur.",
            "İnsanın doğuştan gelen ihtiyaçları ile çevresinin dayattığı kurallar arasında sürekli bir gerilim "
            "vardır.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("İd", "Haz İlkesi — anında tatmin ister"),
            FlowStep("Ego", "Gerçeklik İlkesi — haz ilkesini dengeler"),
            FlowStep("Süperego", "Üst Ben — ahlaki beklentileri içselleştirir"),
        ], caption="Freud'un Zihin Modeli: İnsan Zihninin Katmanları ve Çatışma"))
    )
    ch5.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Freud'un Mekansal Zihin Metaforu",
            ["Mekân", "Karşılığı"],
            [
                ["Oturma Salonu", "Bilinç — farkında olduğumuz, yaşadığımız ve düşündüğümüz şeyler."],
                ["Karanlık Koridor", "Bilinçdışı — bastırılmaya çalışılan düşünceler, travmalar ve unutulmak istenen anılar."],
            ]
        ))
        .add_block(BulletBlock(4, "Çatışma ve Anahtar Yöntem", [
            "İnsan bir konuyu (koridordakileri) ne kadar çok unutmak ve bastırmak isterse, aslında o konuyu o "
            "kadar çok düşünür.",
        ]))
        .add_callout(Callout("focus", "Kritik Odak: Serbest Çağrışım ve Rüya Yorumu",
            "Freud, bilinçdışına giden yolda <b>Serbest Çağrışım</b> yöntemini ve kendi yazdığı <b>Rüya "
            "Yorumu</b> adlı eserdeki rüya analizlerini anahtar olarak kullanır."))
        .add_summary("Charles Darwin, 'Doğal Seçilim' ile canlıların ortak bir kökenden değişerek evrimleştiğini "
            "kanıtlarken; Sigmund Freud, insan davranışlarının temelinde 'İd' ve 'Süperego' çatışmasıyla "
            "şekillenen karanlık 'Bilinçdışı' süreçlerin yattığını ortaya koymuştur.")
    )

    # =====================================================================
    # BÖLÜM 6 — Çağdaş Felsefe ve Analitik Gelenek (Bertrand Russell)
    # =====================================================================
    ch6 = Chapter(
        number=6,
        title="Çağdaş Felsefe ve Analitik Gelenek",
        subtitle="Bertrand Russell ve dilin, mantığın analiziyle kesinliğe ulaşma arayışı",
        key_terms=[
            KeyTerm("Çağdaş Felsefe", "20. yüzyıl başlarından günümüze uzanan; dil, toplum, anlam ve deneyim gibi konuları eleştirel ve çoğulcu bir yaklaşımla inceleyen felsefi dönem."),
            KeyTerm("Analitik Felsefe", "Ağırlıklı olarak İngiltere ve Amerika'da gelişen; anlam karmaşalarını çözmek için dilin, mantığın ve bilimsel yöntemin analizine odaklanan çağdaş felsefe geleneği."),
            KeyTerm("Kıta Felsefesi", "Avrupa'da gelişen; tarihsel, kültürel ve varoluşsal sorunları (fenomenoloji, varoluşçuluk, hermeneutik) merkeze alan çağdaş felsefe geleneği."),
            KeyTerm("Mantıksal Atomculuk", "Russell'ın felsefesinde, dilin yapısı ile dünyanın yapısı arasında kopmaz bir yapısal benzerlik bulunduğunu savunan görüş."),
        ],
    )
    ch6.pages.append(
        ChapterPage()
        .add_terms(ch6.key_terms)
        .add_person(RUSSELL)
    )
    ch6.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "İki Ana Gelenek: Çağdaş Felsefenin İki Kolu",
            ["Gelenek", "Odak"],
            [
                ["Analitik Felsefe", "Dilin ve mantığın analiziyle kesin, rasyonel çözümler (Russell, Wittgenstein, G. E. Moore)."],
                ["Kıta Felsefesi", "İnsanın dünyadaki konumu, kaygıları, varoluşsal meseleler (fenomenoloji, varoluşçuluk)."],
            ]
        ))
        .add_block(BulletBlock(1, "Hayatı ve Aktivist Kişiliği", [
            "1872–1970 yılları arasında yaşamış İngiliz filozof, hümanist ve sosyalist düşünürdür; G. E. Moore "
            "ile birlikte modern analitik felsefenin kurucularından kabul edilir.",
            "Dogmatizme şiddetle karşı çıkar: <b>'Düşüncelerim için ölmeyi göze almam, çünkü yanılıyor "
            "olabilirim.'</b>",
            "Savaş karşıtı duruşuyla 'Bertrand Russell Barış Vakfı'nı kurmuş; insan hakları ve özgür düşünce "
            "üzerine yazıları nedeniyle Nobel Edebiyat Ödülü'nü kazanmıştır.",
        ]))
        .add_block(BulletBlock(2, "Temel Teorileri ve Felsefi Katkıları", [
            "<b>Matematik ve Mantık:</b> Kendi adıyla bilinen 'Russell Paradoksu'nu geliştirmiş; Whitehead ile "
            "kaleme aldığı <b>Principia Mathematica</b> ile matematiği tamamen mantıksal ilkelerden türetmeye "
            "çalışmıştır.",
            "<b>Dilin Mantıksal Analizi:</b> Bir insanın neyi kastettiğini anlamak için sadece neyi söylediğine "
            "değil, nasıl söylediğine bakılması gerektiğini vurgular.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("Duyusal Deneyim", "Temel"),
            FlowStep("Birleştirme / Çıkarım Yapma"),
            FlowStep("Mantıksal Analiz"),
            FlowStep("Kesin Bilgiye Ulaşma"),
        ], caption="Russell'ın Bilgi Teorisi (Epistemoloji) Akış Şeması"))
    )
    ch6.pages.append(
        ChapterPage()
        .add_callout(Callout("caution", "Din ve Siyaset Eleştirisi",
            "Bir ateist olan Russell, <b>'Neden Hristiyan Değilim'</b> adlı kitabında Tanrı'nın varlığına dair "
            "delilleri çürütmeye çalışmış; dinin akla değil 'korkuya' dayandığını ve ilerlemeye engel "
            "olduğunu iddia etmiştir."))
        .add_summary("Bertrand Russell, G.E. Moore ile birlikte çağdaş felsefenin en önemli damarlarından biri "
            "olan Analitik felsefeyi kurmuş; Principia Mathematica ile matematiği mantığa indirgeyerek devrim "
            "yapmış ve yaşamı boyunca dogmalara karşı çıkarak aklı ve mantıksal çözümlemeyi felsefesinin "
            "merkezine yerleştirmiştir.")
    )

    # =====================================================================
    # BÖLÜM 7 — İman ve Varoluş (Kierkegaard'dan Husserl, Heidegger, Sartre ve Camus'ye)
    # =====================================================================
    ch7 = Chapter(
        number=7,
        title="İman ve Varoluş",
        subtitle="Kierkegaard'ın öznel doğrusundan Husserl, Heidegger, Sartre ve Camus'nün varoluşçuluğuna",
        key_terms=[
            KeyTerm("Öznel Doğru", "Kişinin kendi iç dünyasında, varoluşuyla bütünleştirerek tutkuyla benimsediği ve uğruna yaşayabileceği hakikat (özellikle inanç)."),
            KeyTerm("İman Şövalyesi", "Kierkegaard'da varoluşun dinsel aşamasına ulaşmış, aklın sınırlarına ve içindeki şüpheye rağmen inancına tutkuyla bağlanan ideal birey."),
            KeyTerm("Fenomenolojik İndirgeme", "Husserl'a göre önyargılardan sıyrılarak yalnızca bilincin deneyimine odaklanma yöntemi."),
            KeyTerm("Absürdizm (Uyumsuzluk)", "Camus'ye göre, insanın anlam arayışı ile dünyanın ona sunduğu sessizlik/anlamsızlık arasındaki çatışma durumu."),
        ],
    )
    ch7.pages.append(
        ChapterPage()
        .add_terms(ch7.key_terms)
        .add_person(KIERKEGAARD)
    )
    ch7.pages.append(
        ChapterPage()
        .add_block(BulletBlock(1, "Nesnel ve Öznel Doğrular", [
            "Kierkegaard'a göre inanmak ve sorgulamak birbirine düşman iki eylemdir. <b>Nesnel doğrular</b> "
            "herkesçe kabul edilen dışsal gerçeklerdir (ör. 2×2=4); ancak insan ruhunu doyurma noktasında "
            "sınırları vardır. <b>Öznel doğrular</b> ise kişinin kendi iç dünyasında doğru kabul ettiği "
            "varoluşsal şeylerdir (ör. Din ve Tanrı).",
            "İnanan insanlar için öznel doğrular, nesnel doğrulardan daima daha üstündür — çünkü hiçbir nesnel "
            "bilgi (bilim veya mantık), inanan insana varoluşu için yeterli anlamı sunamaz.",
        ]))
        .add_table(ComparisonTable(
            "İnanan İnsan Tipleri: Yobazlar ve Dindarlar",
            ["Tip", "Yaklaşımı"],
            [
                ["Yobazlar", "Dini nesnel bir doğru (bilimsel bir olgu) gibi görür, mantıkla kanıtlamaya çalışır."],
                ["Dindarlar", "Dini öznel bir doğru olarak kabul eder; inanç onlar için içsel, tutkulu bir yaşantıdır."],
            ]
        ))
        .add_flow(FlowDiagram([
            FlowStep("Estetik Aşama", "Haz arayışı; beraberinde can sıkıntısı gelir"),
            FlowStep("Etik Aşama", "Akılla 'doğru-yanlış' (ahlaki görev) ayrımı"),
            FlowStep("Dinsel Aşama", "İnanç Sıçraması ile Tanrı'ya tutkuyla bağlanma"),
        ], caption="İman Şövalyesi Mertebesine Giden Üç Zorunlu Aşama"))
        .add_block(BulletBlock(2, "Şüphe ve Gerçek İman İlişkisi", [
            "Kierkegaard için inanç, kesin ve rahatlatıcı bir bilgi durumu değildir; aksine dindar bir insan "
            "inancına karşı şüphe duymalıdır.",
            "Asıl dindarlık; aklın sınırlarına ve içindeki şüpheye rağmen inanmaya devam etmektir.",
        ]))
        .add_callout(Callout("insight", "Kritik Odak: İman Şövalyesi",
            "Aklın sınırlarına ve içindeki şüpheye rağmen inanmaya devam eden birey, Kierkegaard'a göre en "
            "üstün ve gerçek dindarlık formu olan <b>'İman Şövalyesi'</b> mertebesine ulaşır."))
    )
    ch7.pages.append(
        ChapterPage()
        .add_terms([
            KeyTerm("Dasein (Orada-Varlık)", "Heidegger'e göre insanın dünyadaki bulunuş hali ve kendi varlığını anlayıp anlamlandırabilme kapasitesi."),
            KeyTerm("Kötü Niyet", "Sartre'ın felsefesinde, insanın kendi özgürlüğünden ve bu özgürlüğün getirdiği ağır sorumluluktan kaçma eğilimi."),
            KeyTerm("İnanç Sıçraması", "Kierkegaard'da, aklın ve mantığın sınırlarının bittiği yerde doğrudan inanca yönelme eylemi."),
            KeyTerm("Varoluşun Üç Aşaması", "Kierkegaard'da bireyin İman Şövalyesi mertebesine ulaşması için geçmesi gereken Estetik, Etik ve Dinsel aşamalar."),
        ])
        .add_block(BulletBlock(3, "20. Yüzyıl Felsefesinde Yönelimler", [
            "20. yüzyıl felsefesi, pozitivizmin katı sınırlarına bir tepki olarak ortaya çıkmıştır; bu "
            "dönemde insan deneyimini, yaşamın anlamını, dili ve toplumu derinlemesine ele alan yaklaşımlar "
            "öne çıkmıştır.",
            "Fenomenoloji, varoluşçuluk, hermeneutik, yapısalcılık ve eleştirel teori gibi akımlar bu dönemin "
            "belirleyici unsurlarıdır.",
        ]))
        .add_person_row([HUSSERL, HEIDEGGER])
    )
    ch7.pages.append(
        ChapterPage()
        .add_block(BulletBlock(4, "Fenomenoloji: Bilincin Özüne Dönüş", [
            "Husserl tarafından geliştirilen fenomenolojinin temel görevi, nesnelerin bilince nasıl "
            "göründüğünü (deneyimin özünü) incelemektir. Felsefenin kesin bilgiye ulaşabilmesi için "
            "inançlardan ve önyargılardan tamamen sıyrılıp yalnızca bilincin deneyişine odaklanılması gerekir "
            "(<b>Fenomenolojik İndirgeme</b>).",
        ]))
        .add_block(BulletBlock(5, "Varlık ve Zaman: Heidegger'in Dasein'ı", [
            "Husserl'ın öğrencisi olan Heidegger, fenomenolojiyi doğrudan 'varlık sorusunu' merkeze alarak "
            "yeniden şekillendirmiştir. İnsan, dünyaya fırlatılmış bir <b>'Dasein'</b> (orada-varlık) olarak "
            "bulunur; varlığı gerçek manada anlamak, ancak zaman, ölüm ve kaygı gibi trajik koşulları "
            "çözümlemekle mümkündür.",
        ]))
        .add_person_row([SARTRE, CAMUS])
        .add_block(BulletBlock(6, "Sartre: Özgürlüğün Sorumluluğu", [
            "Sartre'ın varoluşçu felsefesinin temeli: <b>'İnsan önce var olur, daha sonra kendi özünü "
            "tamamen kendi eylemleri ve seçimleriyle oluşturur.'</b> İnsan mutlak anlamda özgürdür ve bu "
            "sınırsız özgürlük, tüm eylemlerinden ötürü sorumluluk taşımasına neden olur.",
            "İnsanların bu ağır sorumluluktan kaçma eğilimine Sartre <b>'kötü niyet'</b> (kendini kandırma) "
            "adını vermiştir.",
        ]))
    )
    ch7.pages.append(
        ChapterPage()
        .add_block(BulletBlock(7, "Camus: Uyumsuzluk ve Başkaldırı", [
            "Camus, varoluşçuluğa 'absürdizm' (uyumsuzluk) kavramını katmıştır: insanın derin anlam arayışı "
            "ile dünyanın ona verdiği anlamsız sessizlik arasında kesin bir uyumsuzluk vardır ve işte bu "
            "durum 'absürt'tür.",
            "Camus'ye göre bu absürtlüğe rağmen insan hayata küsmemeli, hayatı anlamlandırmaya çalışmalı ve "
            "her şeye inat yaşama eylemini seçmelidir.",
        ]))
        .add_callout(Callout("route", "Kritik Odak: Sisifos Miti",
            "Kayayı sürekli dağın tepesine taşıyan ancak taşıdığı kaya her defasında aşağı yuvarlanan Sisifos "
            "gibi, hayatın evrensel bir anlamı olmasa bile insanın yaşama mücadelesi kendi içinde bir "
            "başkaldırıdır ve ebediyen devam etmelidir."))
        .add_summary("Søren Kierkegaard'ın öznel doğruya tutkuyla bağlanan 'İman Şövalyesi' idealiyle açılan bu "
            "yolculuk, 20. yüzyılda fenomenoloji ve varoluşçulukla derinleşir: Husserl fenomenolojik "
            "indirgemeyle bilincin özünü aramış, Heidegger 'Dasein' kavramıyla varlığı zaman ve ölüm "
            "üzerinden sorgulamış, Sartre insanın tamamen özgür olup kendi özünü yarattığını vurgulamış, "
            "Camus ise dünyanın 'absürtlüğüne' rağmen insanın Sisifos gibi yılmadan yaşamı seçip mücadele "
            "etmesi gerektiğini savunmuştur.")
    )

    chapters = [ch1, ch2, ch3, ch4, ch5, ch6, ch7]

    # =====================================================================
    # SÖZLÜK
    # =====================================================================
    glossary = [
        Concept("Pozitivizm", "Yalnızca deney ve gözlemle doğrulanabilir bilimsel bilgiyi geçerli sayan felsefi akım.", "Auguste Comte", 1),
        Concept("Sosyal Fizik", "Comte'un toplum bilimi için kullandığı, sonradan 'Sosyoloji' adını verdiği kavram.", "Auguste Comte", 1),
        Concept("Üç Hal Yasası", "İnsan düşüncesinin teolojik, metafizik ve pozitif olmak üzere üç aşamadan geçtiği kural.", "Auguste Comte", 1),
        Concept("İnsanlık Dini", "Bilime dayalı, geleneksel dinlerin yerini alması hedeflenen seküler din anlayışı.", "Auguste Comte", 1),
        Concept("İrade (İsteme)", "Evrenin ve insanın temelini oluşturan, doymak bilmeyen içsel arzu.", "Arthur Schopenhauer", 2),
        Concept("Pesimizm (Kötümserlik)", "Yaşamın özünde acı ve tatminsizlik olduğunu savunan karamsar bakış açısı.", "Arthur Schopenhauer", 2),
        Concept("Çilecilik (Asketizm)", "İradenin isteklerini bastırıp acıyı en aza indirme pratiği.", "Arthur Schopenhauer", 2),
        Concept("Yalnızlık", "İnsanın kendini bulması için zorunlu, özgürlükle kopmaz biçimde bağlı ihtiyaç.", "Arthur Schopenhauer", 2),
        Concept("Güç İstenci", "Canlıların hayatta kalmanın ötesinde gücünü artırmayı arzuladığı yaşam enerjisi.", "Friedrich Nietzsche", 2),
        Concept("Üst İnsan (Übermensch)", "Kendi değerlerini kendisi yaratan, yaşamı bütünüyle olumlayan ideal insan.", "Friedrich Nietzsche", 2),
        Concept("Nihilizm (Hiççilik)", "Hayatın ve değerlerin nesnel bir temeli olmadığını savunan görüş.", "Friedrich Nietzsche", 2),
        Concept("Sürü İnsanı", "Yönetilmek için sürekli bir otoriteye ihtiyaç duyan itaatkâr insan tipi.", "Friedrich Nietzsche", 2),
        Concept("Faydacılık (Utilitarizm)", "Eylemin ahlaki değerini en çok kişi için sağladığı faydayla ölçen yaklaşım.", "Bentham / Mill", 3),
        Concept("Hedonizm (Hazcılık)", "Mutluluğu hazza ulaşıp acıdan kaçınmak olarak tanımlayan yaklaşım.", "Bentham / Mill", 3),
        Concept("Panoptikon", "Tek gözlemcinin mahkumlarda otokontrol yaratmasını amaçlayan gözetim mimarisi.", "Jeremy Bentham", 3),
        Concept("Zarar İlkesi", "Bireyin özgürlüğünün tek sınırının başkalarına zarar vermemek olduğu kuralı.", "John Stuart Mill", 3),
        Concept("Alt Yapı ve Üst Yapı", "Toplumun maddi üretim zemini (alt yapı) ile üzerindeki kurumlar (üst yapı).", "Karl Marx", 4),
        Concept("Diyalektik Materyalizm", "Değişimi maddi unsurların çatışması üzerinden açıklayan yöntem.", "Karl Marx", 4),
        Concept("Yabancılaşma", "İşçinin ürettiği ürüne ve kendi doğasına giderek uzaklaşması durumu.", "Karl Marx", 4),
        Concept("Proletarya ve Burjuvazi", "Emeğini satan işçi sınıfı ile üretim araçlarını elinde tutan sermaye sınıfı.", "Karl Marx", 4),
        Concept("Doğal Seçilim", "Çevreye en iyi uyum sağlayan canlıların hayatta kalıp üremesi süreci.", "Charles Darwin", 5),
        Concept("Psikanaliz", "İnsan davranışlarının temelindeki bilinçdışı süreçleri inceleyen kuram.", "Sigmund Freud", 5),
        Concept("İd-Ego-Süperego", "Freud'un zihin modeli: haz dürtüsü, gerçeklik dengesi ve ahlaki beklentiler.", "Sigmund Freud", 5),
        Concept("Bilinçdışı (Karanlık Koridor)", "Bastırılan düşünce, travma ve anıların hapsedildiği zihinsel alan.", "Sigmund Freud", 5),
        Concept("Çağdaş Felsefe", "20. yüzyıl başlarından günümüze uzanan, dil ve anlamı inceleyen felsefi dönem.", "Bertrand Russell", 6),
        Concept("Analitik Felsefe", "Dilin ve mantığın analiziyle kesin çözümler bulmayı amaçlayan gelenek.", "Bertrand Russell", 6),
        Concept("Kıta Felsefesi", "İnsanın dünyadaki konumunu ve varoluşsal meselelerini merkeze alan gelenek.", "Bertrand Russell", 6),
        Concept("Mantıksal Atomculuk", "Dilin yapısı ile dünyanın yapısı arasında benzerlik bulunduğu görüşü.", "Bertrand Russell", 6),
        Concept("Öznel Doğru", "Kişinin iç dünyasında tutkuyla benimsediği, uğruna yaşanabilecek hakikat.", "Søren Kierkegaard", 7),
        Concept("İnanç Sıçraması", "Aklın sınırının bittiği yerde doğrudan inanca yönelme eylemi.", "Søren Kierkegaard", 7),
        Concept("İman Şövalyesi", "Aklın sınırlarına ve şüpheye rağmen inancına tutkuyla bağlanan ideal birey.", "Søren Kierkegaard", 7),
        Concept("Varoluşun Üç Aşaması", "İman Şövalyesi'ne giden Estetik, Etik ve Dinsel aşamalardan oluşan evrim.", "Søren Kierkegaard", 7),
        Concept("Fenomenolojik İndirgeme", "Önyargılardan sıyrılıp yalnızca bilincin deneyimine odaklanma yöntemi.", "Edmund Husserl", 7),
        Concept("Dasein (Orada-Varlık)", "İnsanın dünyadaki bulunuş hali ve kendi varlığını anlamlandırma kapasitesi.", "Martin Heidegger", 7),
        Concept("Kötü Niyet", "İnsanın özgürlüğünden ve sorumluluğundan kaçma eğilimi.", "Jean-Paul Sartre", 7),
        Concept("Absürdizm (Uyumsuzluk)", "İnsanın anlam arayışı ile dünyanın sessizliği arasındaki çatışma.", "Albert Camus", 7),
    ]

    # =====================================================================
    # TEST — 20 Soruluk Genel Değerlendirme
    # =====================================================================
    test_questions = [
        TestQuestion(1, "Comte'un 'Üç Hal Yasası'na göre insan düşüncesi hangi sırayla ilerler?",
            {"A": "Metafizik → Teolojik → Pozitif", "B": "Pozitif → Metafizik → Teolojik",
             "C": "Teolojik → Metafizik → Pozitif", "D": "Teolojik → Pozitif → Metafizik",
             "E": "Metafizik → Pozitif → Teolojik"}),
        TestQuestion(2, "Comte'un 'İnsanlık Dini' anlayışında 'Büyük Fetiş' neyi simgeler?",
            {"A": "İnsanlığın kendisini", "B": "Uzayı", "C": "Dünya / Doğa'yı",
             "D": "Bilim insanlarını", "E": "Üniversiteleri"}),
        TestQuestion(3, "Schopenhauer felsefesinde evrenin ve insanın temelini oluşturan, doymak bilmeyen içsel arzuya ne ad verilir?",
            {"A": "Güç İstenci", "B": "İrade (İsteme)", "C": "Nihilizm", "D": "Kötü Niyet", "E": "Dasein"}),
        TestQuestion(4, "Schopenhauer'a göre mutluluk nedir?",
            {"A": "Sürekli haz arayışının sonucu", "B": "Kendi başına var olan pozitif bir durum",
             "C": "Acı ve ızdırabın yokluğu", "D": "Toplumsal statünün getirdiği tatmin",
             "E": "İradenin sınırsızca tatmin edilmesi"}),
        TestQuestion(5, "Nietzsche'ye göre 'Güç İstenci' bir iş insanında nasıl ortaya çıkar?",
            {"A": "Hakikatin peşinde koşarak", "B": "Eser üreterek", "C": "Zengin olarak",
             "D": "Sürüye liderlik ederek", "E": "Dini otoriteye bağlanarak"}),
        TestQuestion(6, "Nietzsche 'Tanrı Öldü' söylemini hangi eseriyle felsefe literatürüne kazandırmıştır?",
            {"A": "Böyle Buyurdu Zerdüşt", "B": "Şen Bilim", "C": "İyinin ve Kötünün Ötesinde",
             "D": "Ecce Homo", "E": "Putların Alacakaranlığı"}),
        TestQuestion(7, "Nietzsche'nin insanın zihinsel evrimindeki üç aşaması hangi sırayla ilerler?",
            {"A": "Trajik İnsan → Özgür İnsan → Sürü İnsanı", "B": "Sürü İnsanı → Trajik İnsan → Özgür İnsan",
             "C": "Sürü İnsanı → Özgür İnsan → Trajik İnsan", "D": "Özgür İnsan → Sürü İnsanı → Trajik İnsan",
             "E": "Trajik İnsan → Sürü İnsanı → Özgür İnsan"}),
        TestQuestion(8, "Merkezdeki tek bir gözlemcinin mahkûmlarda otokontrol geliştirmesini amaçlayan mimari gözetim modeli Bentham tarafından ne adıyla tasarlanmıştır?",
            {"A": "Zarar İlkesi", "B": "Panoptikon", "C": "Sosyal Fizik", "D": "Dasein", "E": "Üç Hal Yasası"}),
        TestQuestion(9, "Mill'e göre bireyin özgürlüğünün tek sınırı nedir?",
            {"A": "Devletin belirlediği yasalar", "B": "Dini kurallar", "C": "Başkalarına zarar vermemek",
             "D": "Toplumsal geleneklere uymak", "E": "Ailenin onayı"}),
        TestQuestion(10, "Bentham ve Mill'in haz anlayışı karşılaştırıldığında, aşağıdakilerden hangisi Mill'e (niteliksel faydacılığa) aittir?",
            {"A": "Bütün hazlar temelde aynıdır", "B": "Önemli olan hazzın miktarıdır",
             "C": "Zihinsel hazlar bedensel hazlardan üstündür", "D": "Bedensel ve zihinsel hazlar eşdeğerdir",
             "E": "Haz matematiksel olarak ölçülemez"}),
        TestQuestion(11, "Marx'ın toplum modelinde siyaset, hukuk, din, ahlak ve felsefe gibi kurumlar hangi katmanda yer alır?",
            {"A": "Alt Yapı", "B": "Üst Yapı", "C": "Doğal Üretim Koşulları", "D": "Proletarya", "E": "Diyalektik Materyalizm"}),
        TestQuestion(12, "Kapitalist düzende işçinin ürettiği ürüne ve kendi doğasına giderek uzaklaşması durumuna ne ad verilir?",
            {"A": "Diyalektik Materyalizm", "B": "Yabancılaşma", "C": "Proletarya Diktatörlüğü",
             "D": "Sosyal Demokrasi", "E": "Üst Yapı"}),
        TestQuestion(13, "Darwin'in evrim teorisine kanıt olarak sunduğu gözlemlerden biri aşağıdakilerden hangisidir?",
            {"A": "Tüm türlerin ayrı ayrı yaratıldığının kanıtlanması", "B": "Farklı hayvan embriyolarının ilk evrelerde birbirine benzemesi",
             "C": "Fosillerin yalnızca deniz seviyesinde bulunması", "D": "Türlerin coğrafyadan bağımsız olarak aynı olması",
             "E": "İnsan zekâsının hayvanlardan tamamen farklı kökenden gelmesi"}),
        TestQuestion(14, "Freud'un zihin modelinde 'Gerçeklik İlkesi'ni temsil eden, haz ilkesini dengeleyen katman hangisidir?",
            {"A": "İd", "B": "Ego", "C": "Süperego", "D": "Bilinçdışı", "E": "Dasein"}),
        TestQuestion(15, "Freud, insan zihnini 'Oturma Salonu' ve 'Karanlık Koridor' metaforuyla açıklarken, 'Karanlık Koridor' neyi temsil eder?",
            {"A": "Bilinci", "B": "Ön bilinci", "C": "Bilinçdışını", "D": "Süperego'yu", "E": "Serbest çağrışımı"}),
        TestQuestion(16, "Bertrand Russell ve G. E. Moore'un öncülerinden olduğu, dilin ve mantığın analizine odaklanan çağdaş felsefe geleneği hangisidir?",
            {"A": "Kıta Felsefesi", "B": "Analitik Felsefe", "C": "Fenomenoloji", "D": "Varoluşçuluk", "E": "Pozitivizm"}),
        TestQuestion(17, "Russell'ın Whitehead ile birlikte yazdığı, matematiği mantıksal ilkelerden türetmeyi amaçlayan eseri hangisidir?",
            {"A": "Neden Hristiyan Değilim", "B": "Principia Mathematica", "C": "Mantıksal Araştırmalar",
             "D": "Varlık ve Zaman", "E": "Sisifos Söyleni"}),
        TestQuestion(18, "Kierkegaard'a göre inanan insanlar için hangi ifade doğrudur?",
            {"A": "Nesnel doğrular öznel doğrulardan daima üstündür", "B": "Öznel doğrular nesnel doğrulardan daima üstündür",
             "C": "Nesnel ve öznel doğrular arasında fark yoktur", "D": "Din, nesnel bir bilimsel olgu olarak kanıtlanmalıdır",
             "E": "Şüphe, gerçek imanla bağdaşmaz"}),
        TestQuestion(19, "Aklın devre dışı bırakılıp doğrudan inancın seçilmesine Kierkegaard hangi kavramı verir?",
            {"A": "Fenomenolojik İndirgeme", "B": "Kötü Niyet", "C": "İnanç Sıçraması", "D": "Absürdizm", "E": "Güç İstenci"}),
        TestQuestion(20, "Camus'nün 'Sisifos Miti' ile özetlediği absürdizm anlayışına göre insan nasıl davranmalıdır?",
            {"A": "Anlamsızlık karşısında hayata küsmelidir", "B": "Anlam arayışından tamamen vazgeçmelidir",
             "C": "Her şeye inat yaşama eylemini seçmelidir", "D": "Dinsel bir otoriteye sığınmalıdır",
             "E": "Toplumsal kurallara mutlak biçimde uymalıdır"}),
    ]

    answer_key_items = [
        AnswerItem(1, "C", "Comte'a göre insan düşüncesi <b>Teolojik → Metafizik → Pozitif</b> sırasıyla, hiyerarşik ve zorunlu bir şekilde ilerler."),
        AnswerItem(2, "C", "İnsanlık Dini'nde 'Yüce Varlık' insanlığı, <b>'Büyük Fetiş' Dünya/Doğa'yı</b>, 'Büyük Ortam' ise Uzay'ı simgeler."),
        AnswerItem(3, "B", "<b>İrade (İsteme)</b>, Schopenhauer felsefesinde evrenin ve insanın temelini oluşturan doymak bilmeyen içsel arzudur; Güç İstenci ise Nietzsche'ye aittir."),
        AnswerItem(4, "C", "Schopenhauer'a göre mutluluk kendi başına pozitif bir durum değildir, yalnızca <b>'acı ve ızdırabın yokluğu'</b>dur."),
        AnswerItem(5, "C", "Nietzsche'ye göre güç istenci mesleklere göre farklı biçimlerde ortaya çıkar: iş insanı <b>zengin olarak</b> güç istencini bulur."),
        AnswerItem(6, "B", "Nietzsche, 'Tanrı Öldü' söylemini <b>Şen Bilim</b> adlı eseriyle felsefe literatürüne kazandırmıştır; 'Üst İnsan' ise Böyle Buyurdu Zerdüşt'te sistemleşir."),
        AnswerItem(7, "C", "İnsanın zihinsel evrimi <b>Sürü İnsanı → Özgür İnsan → Trajik İnsan</b> sırasıyla ilerler."),
        AnswerItem(8, "B", "<b>Panoptikon</b>, Bentham'ın tasarladığı, mahkûmların sürekli izleniyormuş hissiyle otokontrol geliştirmesini amaçlayan mimari gözetim modelidir."),
        AnswerItem(9, "C", "Mill'in <b>Zarar İlkesi</b>'ne göre bireyin özgürlüğünün tek sınırı başkalarına zarar vermemektir."),
        AnswerItem(10, "C", "Mill'in niteliksel faydacılığına göre <b>zihinsel ve entelektüel hazlar</b>, bedensel hazlardan her zaman daha üstündür; Bentham ise tüm hazları nicelik olarak eşit sayar."),
        AnswerItem(11, "B", "Siyaset, hukuk, din, ahlak ve felsefe gibi kurumlar Marx'ın modelinde <b>Üst Yapı</b>'yı oluşturur; alt yapı ise maddi üretim koşullarını kapsar."),
        AnswerItem(12, "B", "<b>Yabancılaşma</b>, kapitalist düzende işçinin ürettiği ürüne, emeğine ve kendi doğasına giderek uzaklaşması durumudur."),
        AnswerItem(13, "B", "Köpek, yarasa, tavşan ve insan embriyolarının ilk evrelerde birbirinin aynısı olması, Darwin'e göre ortak kökenden gelme tezini güçlendiren kanıtlardan biridir."),
        AnswerItem(14, "B", "<b>Ego (Gerçeklik İlkesi)</b>, insan büyüdükçe gerçekliğin farkına vararak İd'in haz ilkesini dengelemeye başladığı katmandır."),
        AnswerItem(15, "C", "Freud'un metaforunda 'Karanlık Koridor', bastırılan düşünce ve travmaların hapsedildiği <b>Bilinçdışı</b>nı temsil eder."),
        AnswerItem(16, "B", "<b>Analitik Felsefe</b>, Russell, Wittgenstein ve Moore'un öncülerinden olduğu, dilin ve mantığın analizine odaklanan çağdaş felsefe geleneğidir."),
        AnswerItem(17, "B", "Russell'ın Whitehead ile birlikte kaleme aldığı <b>Principia Mathematica</b>, matematiği mantıksal ilkelerden türetmeyi amaçlar."),
        AnswerItem(18, "B", "Kierkegaard'a göre inanan insanlar için <b>öznel doğrular nesnel doğrulardan daima üstündür</b>, çünkü nesnel bilgi varoluşsal anlam için yeterli değildir."),
        AnswerItem(19, "C", "Aklın devre dışı bırakılıp doğrudan inancın seçilmesine <b>İnanç Sıçraması</b> denir; bu, dinsel aşamanın eylemidir."),
        AnswerItem(20, "C", "Camus'ye göre absürtlüğe rağmen insan hayata küsmemeli, <b>her şeye inat yaşama eylemini seçmelidir</b> — Sisifos'un ebedi mücadelesi gibi."),
    ]

    return CoursePack(
        course_code="FELSEFE TAR. II",
        title='Modern Felsefe<span class="accent-word"> Tarihi</span>',
        subtitle="Pozitivizmden Varoluşçuluğa: 19. ve 20. Yüzyıl Düşünce Akımları",
        description=(
            "19. yüzyılın pozitivist, faydacı ve materyalist kuramlarından başlayarak Darwin ve Freud'un "
            "sarsıcı bilimsel devrimlerine, oradan da 20. yüzyılın analitik kesinliğine ve varoluşçu krizlerine "
            "kadar uzanan; insanı, toplumu, inancı ve gerçeği yeniden tanımlayan modern felsefe tarihinin "
            "final sınavı özeti."
        ),
        theme="slate",
        theme_color="#724C31",
        icon_text="F",
        chapters=chapters,
        glossary=glossary,
        test_title="Genel Değerlendirme Testi",
        test_subtitle="Comte'tan Camus'ye, 19. ve 20. yüzyıl felsefe tarihi üzerine kapsamlı çoktan seçmeli test",
        test_instructions="Aşağıdaki sorularda beş seçenekten yalnızca birini işaretleyiniz. Süre: 30 dakika.",
        test_questions=test_questions,
        answer_key_intro="Her sorunun doğru cevabı ve kısa gerekçesi aşağıda yer almaktadır.",
        answer_key_items=answer_key_items,
        overview_lead=(
            "Bu ders; 19. yüzyılın <b>pozitivist ve materyalist</b> kuramlarından başlayarak, Darwin ve "
            "Freud'un <b>bilimsel devrimlerine</b>, oradan da 20. yüzyılın <b>analitik kesinliği</b> ile "
            "<b>varoluşçu krizlerine</b> uzanan modern felsefe tarihinin yedi temel durağını bir bütün "
            "olarak sunar."
        ),
        overview_cards=[
            {"title": "Pozitivizm ve Toplum", "text": "Comte'un bilime dayalı Üç Hal Yasası ve İnsanlık Dini projesi."},
            {"title": "Kötümserlik ve Güç İstenci", "text": "Schopenhauer'ın irade felsefesinden Nietzsche'nin Üst İnsan idealine."},
            {"title": "Faydacılık", "text": "Bentham'ın niceliksel ve Mill'in niteliksel faydacılık anlayışları."},
            {"title": "Materyalizm ve Yabancılaşma", "text": "Marx'ın alt yapı-üst yapı çatışması ve sınıf mücadelesi."},
            {"title": "Bilimsel Devrimler", "text": "Darwin'in doğal seçilimi ve Freud'un bilinçdışı keşfi."},
            {"title": "Çağdaş Felsefe", "text": "Russell'ın analitik geleneğinden Kierkegaard ve varoluşçulara uzanan yol."},
        ],
        overview_flow=[
            ("Pozitivizm", "Bilim ve toplum (Comte)"),
            ("Kötümserlik → Güç İstenci", "Schopenhauer, Nietzsche"),
            ("Faydacılık & Materyalizm", "Bentham, Mill, Marx"),
            ("Bilimsel Devrimler", "Darwin, Freud"),
            ("Çağdaş Felsefe", "Russell'dan Varoluşçuluğa"),
        ],
        overview_note=(
            "Sınavda en çok karıştırılan yer, <b>Nietzsche'nin Güç İstenci</b> ile <b>Schopenhauer'ın "
            "İradesi</b> arasındaki farktır: Schopenhauer'da irade körü körüne acı çektiren bir güç iken, "
            "Nietzsche'de Güç İstenci yaşamı olumlayan, aşan ve yaratan olumlu bir enerjidir."
        ),
    )
