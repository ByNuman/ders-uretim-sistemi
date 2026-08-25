# -*- coding: utf-8 -*-
"""FELSEFE TARİHİ 2 — Görsel Ders Notu Kitabı, içerik tanımı (2. sınıf / 2. dönem / VİZE).
Kaynak: 'FELSEFE TARİHİ 2 VİZE DERS NOTU.pdf' (öğretmen notu, 16 sayfa).
Kapsam: 17. ve 18. yüzyıl Batı felsefesi — rasyonalizm, empirizm ve Aydınlanma.
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

# --------------------------------------------------------------------------
# KİŞİLER — tek kaynak ilkesi: tarih/eser bilgisi yalnızca burada tanımlanır
# --------------------------------------------------------------------------
DESCARTES = Person(
    id="descartes", name="René Descartes", years="1596–1650",
    tagline="Yeni Çağ Felsefesinin Kurucusu, İlk Büyük Sistem Kurucusu",
    bio=["Evrenin düzenini ve insanın doğasını anlamak için Avrupa'yı dolaşan; <b>şömine (baca) filozofu</b> "
         "olarak anılan Descartes, Orta Çağ'dan gelen bilgiye de duyulara da güvenilemeyeceğini savunarak "
         "her şeyden şüphe etmiş ve şüphe edilemeyen tek noktada — <b>cogito</b>'da — felsefesinin temelini "
         "kurmuştur. Spinoza, Leibniz, Locke, Berkeley, Hume ve Kant onun takipçisidir."],
    key_work="Yöntem Üzerine Konuşma · Meditasyonlar",
)
PASCAL = Person(
    id="pascal", name="Blaise Pascal", years="1623–1662",
    tagline="Matematikten Teolojiye Geçen Dâhi",
    bio=["Pascal teoremi, olasılık teorisi ve Pascal üçgeniyle matematiğe damga vuran; yirmili yaşlarında "
         "<b>ilk hesap makinesini</b> yaparak bilgisayarların atası sayılan bir isimdir. 1654'te yaşadığı "
         "yoğun dinî tecrübeyi <b>Memorial</b>'de kaydettikten sonra çalışmalarını ilahiyata çevirmiş ve "
         "ünlü <b>bahis argümanını</b> geliştirmiştir."],
    key_work="Düşünceler (Pensées)",
)
HOBBES = Person(
    id="hobbes", name="Thomas Hobbes", years="1588–1679",
    tagline="Modern Siyaset Felsefesinin Kurucusu",
    bio=["Avrupa'yı gezerken Galileo ve Descartes ile karşılaşmış, İngiliz iç savaşı nedeniyle Paris'e "
         "gidip yaklaşık on bir yıl orada kalmıştır. İnsanların bencil ve birbirine karşı eşit olduğu bir "
         "doğa durumundan yola çıkarak, herkesin herkesle anlaşıp bütün haklarını <b>Leviathan</b>'a "
         "devretmesiyle devletin doğduğunu savunmuştur."],
    key_work="Leviathan · Yurttaş Üzerine (De Cive)",
)
LEIBNIZ = Person(
    id="leibniz", name="Gottfried Wilhelm Leibniz", years="1646–1716",
    tagline="Monadlar ve En İyi Mümkün Dünya",
    bio=["Matematikçi ve bilim insanı olan Leibniz, varlığın temel taşlarını birbiriyle hiç etkileşmeyen "
         "ama Tanrı'nın <b>önceden kurduğu uyum</b> içinde hareket eden <b>monadlar</b> olarak tanımlamış; "
         "kötülük problemine <b>Teodise</b>'de rasyonel bir açıklama getirerek Tanrı'nın mümkün dünyaların "
         "en iyisini yarattığını savunmuştur."],
    key_work="Monadoloji · Teodise",
)
SPINOZA = Person(
    id="spinoza", name="Baruch Spinoza", years="1632–1677",
    tagline="Tanrı ile Doğayı Birleştiren Panteist",
    bio=["Portekiz kökenli Yahudi bir ailenin çocuğu olarak Hollanda'da yetişmiş, Descartes felsefesiyle "
         "tanıştıktan sonra kutsal kitaplardaki çelişkileri felsefeyle açıklamaya çalışmış ve bu yüzden "
         "<b>aforoz</b> edilmiştir. <b>Etika</b>'da Tanrı'nın dünyadan ayrı bir varlık olmadığını, evrendeki "
         "bütün maddelerin toplamı olan tek töz olduğunu savunmuştur."],
    key_work="Etika",
)
LOCKE = Person(
    id="locke", name="John Locke", years="1632–1704",
    tagline="Zihin Boş Bir Levhadır: Empirizmin Kurucusu",
    bio=["Descartes'ın doğuştan tasavvurlar görüşüne doğrudan karşı çıkarak insan zihninin doğuştan boş "
         "bir levha (<b>tabula rasa</b>) olduğunu, dünyaya dair bütün bilgileri duyularla edindiğimizi "
         "savunmuştur. Nesnelerin özelliklerini <b>birincil</b> ve <b>ikincil nitelikler</b> diye ikiye "
         "ayırması, kendisinden sonraki tüm empirizm tartışmasının zeminini kurmuştur."],
    key_work="İnsanın Anlama Yetisi Üzerine Bir Deneme",
)
BERKELEY = Person(
    id="berkeley", name="George Berkeley", years="1685–1753",
    tagline="Var Olmak Algılanmaktır",
    bio=["Döneminin gerçeklik anlayışının temellerine meydan okuyan Berkeley, Locke'un birincil–ikincil "
         "nitelik ayrımını reddederek <b>her iki nitelik türünün de zihinsel fenomen</b> olduğunu savunmuş; "
         "nesnelerin yalnızca algılandıkları ölçüde var olduğunu ileri sürerek <b>öznel idealizmi</b> "
         "kurmuştur."],
    key_work="Öznel idealizm — esse est percipi",
)
HUME = Person(
    id="hume", name="David Hume", years="1711–1776",
    tagline="En Büyük Empirist; Nedenselliğin Eleştirmeni",
    bio=["Bileşik tasavvurları reddedip basit tasavvurların peşine düşen Hume, iki olay arasındaki zorunlu "
         "bağın nesnelerde değil <b>bizim bilincimizde</b> yattığını göstermiş; Tanrı'nın varlığına dair her "
         "ispat girişimini reddederek <b>agnostik</b> kalmış ve ahlak alanında insanı akıl değil "
         "<b>duyguların</b> yönettiğini savunmuştur."],
    key_work="İnsan Doğası Üzerine Bir İnceleme",
)
VOLTAIRE = Person(
    id="voltaire", name="Voltaire", years="1694–1778",
    tagline="Akıl, Hoşgörü ve İfade Özgürlüğünün Savunucusu",
    bio=["Kilise ve din adamlarının toplum üzerindeki baskısını, despotizmi ve sansürü sertçe eleştiren "
         "Voltaire, <b>“Alçaklığı ezeceksiniz”</b> (Écrasez l'infâme) sloganıyla dinin suistimal edilmesine "
         "karşı çıkmış; ifade özgürlüğünü, bilimsel ilerlemeyi ve insan haklarını Aydınlanma'nın merkezine "
         "yerleştirmiştir."],
    key_work="Aydınlanma düşüncesinin sözcüsü",
)
ROUSSEAU = Person(
    id="rousseau", name="Jean-Jacques Rousseau", years="1712–1778",
    tagline="Medeniyet İnsanı Yozlaştırır",
    bio=["Cenevre doğumlu olup Paris'te insanların lüks içinde yaşamasını eleştiren Rousseau, yüzyılının "
         "ilerleme inancına karşı çıkarak medeniyetin ahlakı yıktığını savunmuştur. <b>Emile</b>'de "
         "çocukların doğuştan iyi olduğunu ve toplumun yozlaşmasından korunmaları gerektiğini söyleyerek "
         "<b>çocuk merkezli eğitimin</b> mucidi olmuştur."],
    key_work="Toplum Sözleşmesi · Emile",
)
KANT = Person(
    id="kant", name="Immanuel Kant", years="1724–1804",
    tagline="Rasyonalizm ile Empirizmi Birleştiren Filozof",
    bio=["Bilgilerimizin oluşmasında hem aklın hem duyu izlenimlerinin rol oynadığını göstererek iki büyük "
         "akımı uzlaştırmıştır. Tanrı'yı bilginin değil <b>ahlakın</b> konusu yapmış, ahlak yasasını hiçbir "
         "faydaya bağlı olmayan koşulsuz bir buyruk — <b>kategorik imperatif</b> — olarak tanımlayarak "
         "<b>ödev ahlakını</b> kurmuştur."],
    key_work="Kategorik imperatif · Pratik postulat",
)
MALEBRANCHE = Person(
    id="malebranche", name="Nicolas Malebranche", years="17. yüzyıl",
    tagline="Vesileciliğin (Occasionalizm) Temsilcisi",
    bio=["Descartes'ın cevher görüşünden etkilenen Fransız filozof, cevheri maddi ve manevi diye ikiye "
         "ayırmış ve aralarındaki ilişkiyi Tanrı'ya bağlamıştır. Ona göre bir topun diğerini hareket "
         "ettirmesinde gerçek fail Tanrı'dır; top yalnızca bir <b>vesiledir</b>. Bilginin asıl kaynağı da "
         "Tanrı'dır."],
    key_work="Vesilecilik (Occasionalizm)",
)


def get_pack() -> CoursePack:
    # ================= BÖLÜM 1 =================
    ch1 = Chapter(
        number=1, title="17. Yüzyıl: Akıl ve Deney",
        subtitle="Skolastiğin Sonu, Rasyonalizm ve Empirizmin Doğuşu",
        key_terms=[
            KeyTerm("Skolastik Düşünce", "Orta Çağ'ın, felsefeyi teolojinin hizmetinde kullanan okul geleneği."),
            KeyTerm("Rasyonalizm", "Bilginin tek güvenilir kaynağının akıl olduğunu savunan akım."),
            KeyTerm("Empirizm", "Bilginin duyu ve deney yoluyla kazanıldığını savunan akım."),
            KeyTerm("A posteriori", "Deneyimden sonra, deneyime dayanarak elde edilen bilgi."),
        ])
    ch1.pages.append(
        ChapterPage()
        .add_terms(ch1.key_terms)
        .add_block(BulletBlock(1, "Yüzyılın Genel Görünümü", [
            "Orta Çağ'ın <b>skolastik düşüncesi</b> geride bırakıldı; <b>akıl, deney ve bilim</b> ön plana çıktı.",
            "<b>Metafizik</b> ve <b>epistemoloji</b> alanlarında önemli gelişmeler yaşandı.",
            "Bilim, <b>Tanrı'nın planı ve amaçlarıyla</b> açıklanma zorunluluğundan kurtuldu.",
            "Yüzyıl, birbirine karşıt iki büyük akım etrafında ikiye ayrıldı.",
        ]))
        .add_table(ComparisonTable(
            "17. yüzyılın iki büyük akımı ve temsilcileri",
            ["Akım", "Temsilcileri"],
            [["<b>Rasyonalizm</b> (Akılcılık)", "Descartes, Spinoza, Leibniz"],
             ["<b>Empirizm</b> (Deneycilik)", "Bacon, Thomas Hobbes, John Locke"]]))
        .add_block(BulletBlock(2, "Rasyonalizm (Akılcılık)", [
            "Hayata yön vermenin tek aracı olarak <b>aklın doğru ve düzgün çalıştırılmasını</b> öne çıkarır.",
            "Dünyada ve evrende belirli bir <b>düzen</b> vardır; insan bu düzeni anlayacak akla sahiptir.",
            "İnsan, bilimi kullanarak yeryüzünü <b>cennete dönüştürebilir</b>.",
            "Bilgi ve bilimin tek kaynağı ve test yöntemi <b>akıldır</b>.",
        ]))
    )
    ch1.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Rasyonalizmin reddettiği dört şey",
            ["Reddedilen", "Gerekçe"],
            [["<b>İnanç, gelenek, bağnazlık, batıl inanç</b>", "Akıl ve bilim ön plandadır"],
             ["<b>Romantizm</b>", "Duyguyu ön plana çıkarır"],
             ["<b>Mistisizm</b>", "Bilginin Tanrı'dan, Tanrısal aydınlanmayla geldiğini iddia eder"],
             ["<b>Otoriteryanizm</b>", "Güçlü ve etkili kişilerin görüşlerine körü körüne bağlanmayı gerektirir"]]))
        .add_block(BulletBlock(3, "Empirizm (Deneycilik)", [
            "İnsan zihni doğuştan boştur (<b>tabula rasa</b>); bilgiler duyular ve deneyimle elde edilir (<b>a posteriori</b>).",
            "Akılcılığa doğrudan karşıttır.",
            "Deneyim yoluyla <b>veri toplamayı</b>, verileri değerlendirmeyi ve <b>gözlemden başlayarak "
            "tümevarımsal akıl yürütmeyi</b> zorunlu görür.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("Rasyonalizm", "Akıl → tümdengelim"),
            FlowStep("Empirizm", "Duyu → tümevarım"),
            FlowStep("Kant", "İkisinin sentezi"),
        ], caption="Yüzyılın hattı: iki karşıt akım, 18. yüzyılda Kant'ta birleşir."))
        .add_callout(Callout("focus", "Sınavda En Çok Karıştırılan Ayrım",
                             "Kısa formül: <b>rasyonalizm akıldan başlar ve tümdengelime</b> yaslanır; "
                             "<b>empirizm duyudan başlar ve tümevarıma</b> yaslanır."))
        .add_summary("17. yüzyıl, skolastiği bırakıp akıl ve deneyi merkeze alan; rasyonalizm ile empirizm "
                     "arasında bölünmüş bir geçiş yüzyılıdır.")
    )

    # ================= BÖLÜM 2 =================
    ch2 = Chapter(
        number=2, title="René Descartes",
        subtitle="Şüpheden Cogito'ya, Cogito'dan Düalizme",
        key_terms=[
            KeyTerm("Metodik Şüphe", "Kesin bilgiye ulaşmak için araç olarak kullanılan geçici şüphe."),
            KeyTerm("Cogito", "“Düşünüyorum o hâlde varım” — şüphe edilemeyen ilk kesinlik."),
            KeyTerm("Uzam", "Maddenin kapladığı alan; bedenin tanımlayıcı özelliği."),
            KeyTerm("Düalizm", "Ruh ile bedeni birbirinden ayrı iki töz sayan görüş."),
        ])
    ch2.pages.append(
        ChapterPage()
        .add_terms(ch2.key_terms)
        .add_person(DESCARTES)
        .add_table(ComparisonTable(
            "Çağlara göre sistem kurucuları",
            ["Dönem", "Sistem kurucusu"],
            [["<b>İlk Çağ</b>", "Sokrates – Platon – Aristoteles"],
             ["<b>Orta Çağ</b>", "Aquinolu Thomas"],
             ["<b>Yeni Çağ</b>", "Descartes (17. yüzyıl)"]]))
        .add_block(BulletBlock(1, "İlgilendiği İki Temel Mesele", [
            "Neyi bilebileceğimiz, yani <b>bilginin kesinliği</b>.",
            "<b>Ruh–beden ilişkisi</b>: ruhsal bir şey nasıl olur da maddesel bir şeye etki eder?",
            "Rasyonalist çizgi: <b>Sokrates → Platon → Augustinus → Descartes</b>.",
        ]))
        .add_block(BulletBlock(2, "Yöntemin Ruhu", [
            "Matematiksel yöntemi felsefeye uygulamak; felsefi doğruları bir <b>matematik önermesi gibi</b> kanıtlamak ister.",
            "Matematikte sayılar, duyulardan <b>daha güvenilir</b> bilgi verir.",
            "Karmaşık bir sorunu <b>en küçük parçalarına</b> ayır ve <b>basitten karmaşığa</b> ilerle.",
        ]))
    )
    ch2.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Descartes'ın dört adımlı yöntemi",
            ["Adım", "İçeriği"],
            [["<b>1. Apaçıklık</b>", "Doğruluğu kesin bilinmeyeni kabul etme; acele ve peşin hükümden uzak dur. "
                                     "Bir şey <b>şüphe edilemeyecek kadar açık ve seçik</b> olmalı."],
             ["<b>2. Analiz</b>", "Ele alınacak konuyu mümkün olduğunca yan unsurlarına ayır."],
             ["<b>3. Sentez</b>", "En basit ve bilinmesi en kolay olandan zora doğru düşünceleri sırala, düzenle, birleştir."],
             ["<b>4. Kontrol</b>", "Matematikteki <b>sağlama</b> gibidir: hiçbir şeyi ihmal etmediğinden emin olmak için "
                                   "önceki işlemleri gözden geçir."]]))
        .add_callout(Callout("caution", "Descartes Septik Değildir",
                             "Septikler için şüphe bir <b>varış noktasıdır</b>; Descartes için yalnızca bir "
                             "<b>yöntemdir</b> — sağlam zemine varınca terk edilir."))
        .add_block(BulletBlock(3, "Şüpheden Cogito'ya", [
            "Şüphenin yayılma sırası: <b>kendi varlığı → Tanrı'nın varlığı → dönemin bilgi yöntemleri</b>.",
            "Uyanıklık ile rüya arasında kesin ayırt edici bir fark yoktur.",
            "Kesinlikle emin olduğu tek şey <b>her şeyden şüphe ettiğidir</b>.",
            "Şüphe etmek için düşünmek gerekir; <b>var olmayan insan düşünemez</b>.",
            "<b>Cogito, ergo sum</b> — “Düşünüyorum, o hâlde varım.”",
            "<b>Çürük elma metaforu:</b> duyulardan ve geleneklerden gelen bilgiler bizi yanıltır.",
        ]))
        .add_table(ComparisonTable(
            "Kötü cin hipotezi — Meditasyonlar'daki iki şahıs",
            ["", "Sağduyu", "Şüpheci"],
            [["<b>Duyular</b>", "Duyulardan gelen bilgiler gerçektir", "Duyular bizi aldatır, yanıltıcıdır"],
             ["<b>Matematik</b>", "2 + 2 = 4", "Ya kötü bir cin seni kandırıyorsa, bunu nasıl bilebiliriz?"]]))
        .add_callout(Callout("insight", "Rüya Argümanı",
                             "Şu an rüyada olabilirsin — ama rüyayı gören <b>senin aklındır</b>. Rüyada da "
                             "olsan uyanık da olsan <b>kendi varlığından emin olabilirsin</b>. Sabit olan akıldır."))
        .add_block(BulletBlock(4, "Tanrı Kanıtı", [
            "Zihnimizde <b>mükemmel bir Tanrı kavramı</b> vardır; mükemmel varlık = Tanrı.",
            "Bu kavramı zihnimize koyan Tanrı'nın kendisidir; Tanrı fikri <b>doğuştan</b> gelir — "
            "tıpkı bir sanatçının eserine imza atması gibi.",
            "<b>Mükemmel Tanrı bizi aldatıyor olamaz</b>; aklımızla bildiğimizin gerçekte karşılığı vardır.",
        ]))
    )
    ch2.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "İki töz ve nitelikleri",
            ["Töz", "Özellikleri"],
            [["<b>Ruh / Tin</b>", "Bilinçlidir · uzamda yer kaplamaz · daha küçük parçalara bölünemez"],
             ["<b>Madde / Beden (Uzam)</b>", "Bilinçli değildir · uzamda yer kaplar · parçalara ayrılır"]]))
        .add_block(BulletBlock(5, "Düalizmin Sonuçları", [
            "İkisinin de kaynağı <b>Tanrı</b>'dır, ama birbirinden <b>bağımsızdırlar</b>.",
            "Ruh, beyindeki <b>epifiz bezine</b> yerleşmiştir; bedenin hareketini ve duygulanmasını buradan sağlar.",
            "<b>Hayvanlar</b> basit mekanik (otonom) varlıklardır, ruhları yoktur — bu, Descartes'ın "
            "olumsuz bir katkısı olmuştur.",
        ]))
        .add_summary("Descartes, metodik şüpheyle her şeyi yıkıp cogito'da sarsılmaz temeli bulmuş, oradan "
                     "Tanrı'ya ve ruh–beden düalizmine giden ilk büyük modern sistemi kurmuştur.")
    )

    # ================= BÖLÜM 3 =================
    ch3 = Chapter(
        number=3, title="Pascal ve Jansenizm",
        subtitle="İnayet Öğretisi ve Bahis Argümanı",
        key_terms=[
            KeyTerm("Eklektik", "Farklı sistemlerden alınan unsurların yeni bir sistemde birleştirilmesi."),
            KeyTerm("Jansenizm", "Augustinus'un inayet öğretisine dayanan katı dinî hareket."),
            KeyTerm("İnayet", "Tanrı'nın kurtarıcı lütfu; kutsal logos aracılığıyla elde edilir."),
            KeyTerm("Patristik", "Kilise babalarının dönemi ve düşüncesi."),
        ])
    ch3.pages.append(
        ChapterPage()
        .add_terms(ch3.key_terms)
        .add_block(BulletBlock(1, "Jansenizm", [
            "Piskopos <b>Cornelius Jansenius</b>'un adını taşıyan dinî bir tarikattır; <b>patristik</b> "
            "filozofların görüşünü benimser.",
            "İnsan <b>doğuştan günahkârdır</b>; Hz. Âdem'in yasak meyveyi yemesiyle insanın özü bozulmuştur.",
            "İnsan <b>öz olarak bozuktur</b> ve ancak Tanrı'nın yardımıyla kurtulur.",
            "<b>İnayet</b>, kutsal <b>logos</b> (Hz. İsa) aracılığıyla elde edilir.",
        ]))
        .add_callout(Callout("focus", "Descartes – Augustinus Ortaklığı",
                             "İkisinin ortak yönü, <b>her ikisinin de metodik şüphecilik yöntemini "
                             "kullanmış olmasıdır</b>."))
        .add_person(PASCAL)
        .add_block(BulletBlock(2, "Kumar (Bahis) Argümanının Mantığı", [
            "Bu bir <b>Tanrı'yı kanıtlama çabası değil</b>, bir akıl yürütmedir.",
            "Temel iddia: Tanrı'ya inanmak <b>rasyonel bir seçimdir</b>.",
            "Dayanağı: <b>potansiyel kazançlar potansiyel kayıplardan her zaman ağır basar</b>.",
        ]))
    )
    ch3.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Bahis argümanının dört olasılığı",
            ["", "Tanrı VARSA", "Tanrı YOKSA"],
            [["<b>İnanıyorsan</b>", "Sonsuz cennetle ödüllendirilirsin", "Sonlu bir kayıp"],
             ["<b>İnanmıyorsan</b>", "Sonsuz azaba düşersin", "Sonlu bir kazanç"]]))
        .add_callout(Callout("insight", "Argümanın Gücü Nereden Geliyor?",
                             "Asimetriden: bir sütunda sonuçlar <b>sonsuz</b>, diğerinde <b>sonludur</b>. "
                             "Sonsuz bir kazanç ihtimali, ne kadar küçük olursa olsun, sonlu bir bedeli aşar."))
        .add_callout(Callout("caution", "Argümanın Zayıf Noktası",
                             "Akıl yürütme yalnızca <b>pragmatik amaçlarla</b> yapılır; içten bir inanç "
                             "değildir. <b>Samimiyet ve çıkar</b> sorunu taşıdığı için eleştirilmiştir."))
        .add_summary("Pascal, inancı bir kanıt meselesi olmaktan çıkarıp sonsuz kazanç–sonlu kayıp hesabına "
                     "dayalı rasyonel bir tercih meselesine dönüştürmüştür.")
    )

    # ================= BÖLÜM 4 =================
    ch4 = Chapter(
        number=4, title="Thomas Hobbes ve Modern Devlet",
        subtitle="Doğa Durumundan Leviathan'a",
        key_terms=[
            KeyTerm("Leviathan", "Egemeni ya da devleti temsil eden deniz canavarı metaforu."),
            KeyTerm("Toplum Sözleşmesi", "Herkesin herkesle anlaşarak haklarını egemene devretmesi."),
            KeyTerm("Doğa Durumu", "Devlet öncesi, herkesin kendini korumak zorunda olduğu durum."),
            KeyTerm("Mekanik Evren", "Galileo ve Kepler'in, evreni yasalarla işleyen bir düzenek sayan anlayışı."),
        ])
    ch4.pages.append(
        ChapterPage()
        .add_terms(ch4.key_terms)
        .add_person(HOBBES)
        .add_table(ComparisonTable(
            "Hobbes'un düşüncesini biçimlendiren üç etken",
            ["Etken", "Katkısı"],
            [["<b>1. Bilimsel devrim</b>", "Galileo ve Kepler'in <b>mekanik evren</b> anlayışı, insan ve evren düşüncesini şekillendirdi"],
             ["<b>2. İngiliz iç savaşı</b>", "Siyaset felsefesinin gelişmesine neden oldu"],
             ["<b>3. Machiavelli'nin realizmi</b>", "<b>Güç ve otorite</b> anlayışından etkilendi"]]))
        .add_block(BulletBlock(1, "İnsan Doğası", [
            "<b>Her insan eşittir</b> — ancak bu <b>mutlak bir eşitlik değildir</b>: senin yapamadığını "
            "başkası yapabilir, herkesin kendine has özellikleri vardır.",
            "İnsanlar <b>bencildir</b>; doğa durumunda herkes kendini korumak zorundadır.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("Doğa durumu", "Bencillik, güvensizlik"),
            FlowStep("Sözleşme", "Herkes herkesle anlaşır"),
            FlowStep("Hak devri", "Bütün haklar devlete"),
            FlowStep("Leviathan", "Egemen doğar"),
        ], caption="Hobbes'ta devletin doğuşu."))
    )
    ch4.pages.append(
        ChapterPage()
        .add_block(BulletBlock(2, "Leviathan", [
            "<b>Leviathan</b>, egemeni ya da devleti temsil eden bir <b>deniz canavarı</b> metaforudur.",
            "Kitap iki soruyu yanıtlar: <b>Devlet nasıl ortaya çıktı? Devlet gücünü nereden alır?</b>",
            "<b>Birleşmiş birçok topluluğu</b> devlet olarak adlandırır.",
        ]))
        .add_callout(Callout("focus", "Eşitlik Neden Tehlikelidir?",
                             "Hobbes'taki eşitlik, insanları <b>birbirine karşı güvensiz</b> kılan bir "
                             "eşitliktir: herkes birbirini öldürebilecek kadar eşit olduğu için doğa durumu "
                             "tehlikelidir. Toplum sözleşmesinin gerekçesi tam olarak budur."))
        .add_summary("Hobbes, bencil ve eşit bireylerin güvenlik uğruna bütün haklarını Leviathan'a "
                     "devretmesiyle devletin doğduğunu savunarak modern siyaset felsefesini başlatmıştır.")
    )

    # ================= BÖLÜM 5 =================
    ch5 = Chapter(
        number=5, title="Ruh–Beden Sorunu ve Üç Rasyonalist",
        subtitle="Malebranche, Leibniz ve Spinoza",
        key_terms=[
            KeyTerm("Occasionalizm", "Nedenselliğin gerçek failinin Tanrı olduğu, olayların birer vesile sayıldığı görüş."),
            KeyTerm("Monad", "Basit, bölünemez, ruhsal varlık birimi."),
            KeyTerm("Teodise", "Tanrı'nın adaleti; kötülük problemine rasyonel açıklama getirme çabası."),
            KeyTerm("Panteizm", "Tanrı ile evreni birbirinden ayırmayan, Tanrı'yı evrenin bütünü sayan görüş."),
        ])
    ch5.pages.append(
        ChapterPage()
        .add_terms(ch5.key_terms)
        .add_person(MALEBRANCHE)
        .add_block(BulletBlock(1, "Vesilecilik", [
            "<b>Occasionalistler</b>, ruh–beden ayrımına ve ilişkisine değişik cevaplar aramışlardır.",
            "Cevheri <b>maddi</b> ve <b>manevi</b> diye ikiye ayırır; ilişkiyi <b>Tanrı'ya</b> bağlar.",
            "<b>Bilardo örneği:</b> siyah top beyaz topa çarpar, ama hareketi yapan <b>Tanrı'dır</b>; "
            "siyah top sadece bir <b>vesiledir</b>.",
            "Bilginin asıl kaynağı <b>Tanrı'dır</b>, diğerleri vesiledir.",
        ]))
        .add_table(ComparisonTable(
            "Ruh–beden sorununa üç farklı cevap",
            ["Filozof", "Çözümü"],
            [["<b>Descartes</b>", "Epifiz bezi üzerinden <b>gerçek etkileşim</b>"],
             ["<b>Malebranche</b>", "Her seferinde araya giren <b>Tanrı</b> (vesilecilik)"],
             ["<b>Leibniz</b>", "Hiç etkileşim yok — <b>önceden kurulmuş uyum</b>"]]))
    )
    ch5.pages.append(
        ChapterPage()
        .add_person(LEIBNIZ)
        .add_block(BulletBlock(2, "Monadoloji — Varlığın Temel Taşları", [
            "<b>Monadlar</b>, basit ve bölünemez <b>ruhsal</b> varlıklardır; yok edilemezler.",
            "Her birinin kendine özgü bir <b>iç dünyası</b> vardır.",
            "Monadlar birbiriyle <b>iletişime girmez</b>; Tanrı tarafından <b>önceden belirlenmiş bir uyum</b> "
            "içinde hareket ederler.",
        ]))
        .add_block(BulletBlock(3, "Teodise — En İyi Mümkün Dünya", [
            "Tanrı <b>en iyi mümkün dünyayı</b> yaratmıştır.",
            "Sonsuz bilgi ve kudret sahibi olduğu için mümkün dünyaların <b>en güzelini</b> seçmiştir.",
            "Kötülük tamamen kaldırılamaz, çünkü <b>daha büyük bir iyiliğe</b> sebep olabilir.",
            "İnsanlar <b>özgür iradelidir</b>; bu sebeple kötülük kaçınılmazdır.",
        ]))
        .add_callout(Callout("caution", "Monad ≠ Atom",
                             "Monadlar, maddenin bölünmesiyle ulaşılan <b>fiziksel atomlar değildir</b>. "
                             "Bölünemez olmalarının sebebi küçük olmaları değil, <b>hiç parçalarının "
                             "bulunmamasıdır</b> — bu yüzden maddi değil metafizik birimlerdir."))
        .add_person(SPINOZA)
        .add_block(BulletBlock(4, "Tanrı ve Evren", [
            "Evren, <b>fiziksel yasaların toplamıdır</b>.",
            "<b>Panteist</b>tir: Tanrı ile evreni ayırmaz; var olan her şeyde Tanrı'dan bir öz vardır.",
            "<b>Tanrı tözdür</b>; evrendeki bütün maddelerin toplamıdır.",
            "<b>Determinizm:</b> doğa belirli yasalara tabidir, evrende hiçbir şey nedensiz değildir.",
            "Evren <b>matematik ve geometri</b> ile açıklanabilir: evrenin düzenini anlarsan Tanrı'yı da anlarsın.",
        ]))
    )
    ch5.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Spinoza'nın Tanrı'sının OLMADIĞI şeyler",
            ["Yaygın inanç", "Spinoza'ya göre"],
            [["Duaları kabul eden Tanrı", "<b>Değildir</b>"],
             ["İnsanlara yardım eden Tanrı", "<b>Değildir</b>"],
             ["İnsan özellikleri taşıyan Tanrı", "İnsan özellikleri Tanrı'da <b>bulunmaz</b>"],
             ["İyiler ödüllendirilir, kötüler cezalandırılır", "<b>Batıl bir inançtır</b>"]]))
        .add_summary("Malebranche nedenselliğin failini Tanrı'ya, Leibniz uyumu önceden kurulmuş düzene "
                     "bağlamış; Spinoza ise Tanrı ile doğayı tek tözde birleştirerek panteizmi kurmuştur.")
    )

    # ================= BÖLÜM 6 =================
    ch6 = Chapter(
        number=6, title="18. Yüzyıl ve Britanya Empiristleri",
        subtitle="Aydınlanma, Locke, Berkeley ve Hume",
        key_terms=[
            KeyTerm("Aydınlanma", "Aklın ve bilimsel yöntemin her alana uygulanmasını savunan 18. yy hareketi."),
            KeyTerm("Deizm", "Tanrı'nın evreni yaratıp bir kenara çekildiği görüşü."),
            KeyTerm("Birincil Nitelik", "Nesnenin kendisine ait gerçek özellikler: yer kaplama, ağırlık, biçim."),
            KeyTerm("İkincil Nitelik", "Kişiden kişiye değişen özellikler: renk, koku, ses, tat."),
        ])
    ch6.pages.append(
        ChapterPage()
        .add_terms(ch6.key_terms)
        .add_block(BulletBlock(1, "Aydınlanma Yüzyılı", [
            "İnsanı ve doğayı <b>yeni bir bakış açısıyla</b> ele alır; insanın doğası, özgürlüğü ve toplumdaki "
            "konumu dönemin başlıca tartışmalarıdır.",
            "Temel ilke: <b>bilimsel yöntem tüm bilgi türlerine uygulanmalıdır</b>.",
            "<b>Rousseau:</b> insan ne zaman doğaya dönerse mutlu olur. <b>Montesquieu:</b> yasalar doğaya uygun yapılmalıdır.",
            "Modern siyasetin temeli atılır; <b>demokrasi, özgürlük, insan hakları</b> bu dönemde şekillenir.",
            "<b>Diderot</b> Ansiklopedi'yi oluşturmuş; filozofların görüşleri <b>Amerikan ve Fransız devrimlerine</b> ilham olmuştur.",
        ]))
        .add_table(ComparisonTable(
            "Dönemde şekillenen dinî görüşler",
            ["Görüş", "İçeriği", "Temsilci"],
            [["<b>Deizm</b>", "Tanrı evreni yaratmış, sonra bir kenara çekilmiştir", "—"],
             ["<b>Agnostisizm</b>", "Tanrı'nın var olup olmadığını bilemeyiz", "David Hume"],
             ["<b>Ateizm</b>", "Tanrı'nın varlığı reddedilir", "Diderot"]]))
        .add_person(LOCKE)
    )
    ch6.pages.append(
        ChapterPage()
        .add_block(BulletBlock(2, "Locke'un Temel Tezleri", [
            "<b>Doğuştan getirdiğimiz tasavvurlar yoktur</b> — doğrudan Descartes'a karşıdır.",
            "Dünya hakkındaki tüm bilgileri <b>duyularla</b> elde ederiz.",
            "Zihin, duyumlardan izlenimleri alıp <b>düşünme, yargılama, inanma, şüphe etme</b> işlemlerini yapar.",
            "Eserinde iki soru ele alınır: tasavvurlarımız nereden geliyor? Duyularımıza güvenebilir miyiz?",
        ]))
        .add_table(ComparisonTable(
            "Birincil ve ikincil nitelikler",
            ["Nitelik", "Örnekler", "Statüsü"],
            [["<b>Birincil</b>", "Yer kaplama, ağırlık, biçim, hareket, sayı", "Nesnenin <b>gerçek özelliklerini</b> yansıtır"],
             ["<b>İkincil</b>", "Renk, koku, ses, tat", "<b>Kişiden kişiye değişir</b>; nesnenin gerçek özelliği değildir"]]))
        .add_person(BERKELEY)
        .add_callout(Callout("focus", "Berkeley'in Locke'a İtirazı",
                             "Locke birincil nitelikleri nesnenin <b>kendisine ait</b> sayar; Berkeley bu "
                             "ayrımı reddeder — ona göre <b>ikisi de zihne bağlıdır</b>, dolayısıyla zihinden "
                             "bağımsız bir maddi dünya varsayımına gerek kalmaz. <b>Var olmak algılanmaktır.</b>"))
        .add_person(HUME)
        .add_block(BulletBlock(3, "Basit ve Bileşik Tasavvurlar", [
            "Dünyanın <b>ilk duyumsanış biçimine</b> dönmek ister; <b>bileşik tasavvurları reddeder</b>.",
            "<b>“Melek”</b> iki farklı deneyimden oluşur; bunları <b>zihnimiz birleştirir</b>.",
            "<b>“Baldan ırmaklar”</b>: bal basit, ırmak basit tasavvurdur — <b>baldan ırmaklar bileşiktir</b>.",
        ]))
    )
    ch6.pages.append(
        ChapterPage()
        .add_block(BulletBlock(4, "Hume'un Testi ve Nedensellik", [
            "Bir metin ① sayı/büyüklükle ilgili soyut düşünceye, ② deneyime dayanan bir düşünüşe yer vermiyorsa "
            "<b>işe yaramaz, çöp bilgidir</b>.",
            "Beklentinin <b>cisimlerde değil bizim bilincimizde</b> yattığını söyler.",
            "<b>Tümevarım problemi:</b> bütün kargaları siyah görmen, beyaz kargaların olmadığı anlamına gelmez.",
            "Tanrı'nın varlığına dair <b>her türlü ispat girişimini reddeder</b>; <b>agnostiktir</b>.",
            "Ahlakta rasyonalizme karşı çıkar: insanın yapıp ettiğini <b>akıl değil duygular</b> belirler.",
        ]))
        .add_callout(Callout("caution", "Hume Yerçekimini Reddetmez",
                             "İtirazı doğa yasalarının işlediğini inkâr etmek değildir. İtiraz, iki olay "
                             "arasındaki <b>zorunlu bağı</b> hiçbir zaman gözlemleyemediğimiz; yalnızca "
                             "ardışıklığı görüp <b>zorunluluğu kendimizin eklediği</b> yönündedir."))
        .add_summary("Britanya empiristleri zihni deneyime bağlamış; Locke nitelikleri ikiye ayırmış, "
                     "Berkeley bu ayrımı yıkmış, Hume ise nedenselliğin zorunluluğunu sorgulamıştır.")
    )

    # ================= BÖLÜM 7 =================
    ch7 = Chapter(
        number=7, title="Voltaire, Rousseau ve Kant",
        subtitle="Aydınlanmanın Zirvesi ve İlk İtirazı",
        key_terms=[
            KeyTerm("Despotizm", "Mutlak ve baskıcı yönetim biçimi."),
            KeyTerm("Soylu Vahşi", "Medeniyet tarafından bozulmamış, doğal hâlindeki insan."),
            KeyTerm("Kategorik İmperatif", "Hiçbir faydaya bağlı olmayan, koşulsuz kesin buyruk."),
            KeyTerm("Pratik Postulat", "Kanıtlanamayacak şeyleri olduğu gibi alıp kabul etme."),
        ])
    ch7.pages.append(
        ChapterPage()
        .add_terms(ch7.key_terms)
        .add_person_row([VOLTAIRE, ROUSSEAU])
        .add_block(BulletBlock(1, "Voltaire", [
            "<b>Akıl, bireysel özgürlük ve bilimsel ilerleme</b> gibi Aydınlanma ilkelerini savunur.",
            "Sloganı <b>“Alçaklığı ezeceksiniz”</b> (Écrasez l'infâme) — dinin <b>suistimal edilmesine</b> karşıdır.",
            "<b>Despotizme ve sansüre</b>, katı dinî yönetime, hurafeye ve kilisenin bilime engel olmasına karşıdır.",
        ]))
        .add_callout(Callout("caution", "Ünlü Söz Aslında Voltaire'in Değil",
                             "“Düşüncelerine katılmıyorum ama onları savunma hakkını ölene dek "
                             "destekleyeceğim” cümlesi onun tavrını iyi özetlese de kendi metinlerinde "
                             "geçmez; biyografi yazarı <b>Evelyn Beatrice Hall</b> tarafından formüle edilmiştir."))
    )
    ch7.pages.append(
        ChapterPage()
        .add_block(BulletBlock(2, "Rousseau: Medeniyet Eleştirisi", [
            "<b>Medeniyet ve ilerleme insanları geliştirmez</b>; bir zamanlar iyi olan ahlak üzerinde "
            "<b>yıkıcı bir etkiye</b> sahiptir.",
            "Doğa hâlindeyken insanlar <b>zihinlerini daha iyi anlayabiliyorlardı</b>.",
            "Şehirlere göçle insan <b>kendini başkalarıyla kıyaslamaya</b> başladı; <b>kıskançlık ve kibir</b> "
            "merkezli bir kendini sevme biçimi doğdu.",
            "<b>Emile:</b> çocuklar doğuştan <b>öz olarak iyidir</b>; onları toplumun yozlaşmasından korumak esastır.",
            "<b>Çocuk merkezli eğitimin</b> mucidi; <b>Romantizm</b> akımına mensuptur.",
        ]))
        .add_callout(Callout("focus", "Aydınlanma İçinde Aydınlanma Karşıtı",
                             "Rousseau, yüzyılının <b>ilerleme inancına karşı</b> çıkar. Aydınlanma aklı ve "
                             "medeniyeti yüceltirken o doğayı ve duyguyu yüceltir — bu yüzden hem "
                             "Aydınlanmacı hem Romantik sayılır."))
        .add_person(KANT)
        .add_table(ComparisonTable(
            "Kant'ın iki akım hakkındaki kararı",
            ["", "Rasyonalistler", "Empiristler"],
            [["<b>Bilginin temeli</b>", "İnsan bilincinde yatar", "Duyu izleniminde yatar"],
             ["<b>Kant'a göre haklı oldukları yer</b>", "Aklın, dünyayı <b>nasıl kavradığımızı belirlemesi</b>",
              "Bilgiyi <b>duyusal deneyime borçlu olmamız</b>"],
             ["<b>Gözden kaçırdıkları</b>", "Deneyimi göz ardı ettiler", "Aklın etkisini göz ardı ettiler"]]))
        .add_block(BulletBlock(3, "Bilgi Görüşü", [
            "<b>Gözlük örneği:</b> kırmızı gözlük takınca her yeri kırmızı görürüz — gözlük, dünyayı nasıl "
            "gördüğümüzü belirleyen <b>ön koşuldur</b>.",
            "<b>Su şişesi örneği:</b> su neye konursa onun şeklini alır; <b>şeyler bilince göre şekil alır</b>.",
            "<b>İnsan zihni boş bir levha değildir</b>; bilinç <b>yaratıcı ve biçim verici</b> bir rol oynar.",
            "<b>Dış koşullar</b> bilginin <b>ham maddesi</b>, <b>iç koşullar</b> (zaman, uzam, nedensellik) "
            "bilginin <b>biçimidir</b>.",
        ]))
    )
    ch7.pages.append(
        ChapterPage()
        .add_block(BulletBlock(4, "Tanrı ve Ahlak Görüşü", [
            "Tanrı'nın varlığını <b>aklımızla kanıtlayamayız</b>; ne akıl ne deneyim kanıt sunar.",
            "Tanrı'ya inanma, ruh ve özgür irade — bunlara <b>pratik postulat</b> adını verir.",
            "<b>Tanrı'nın var olduğunu kabul etmek ahlaki açıdan gereklidir.</b>",
            "Her insan <b>pratik bir akla</b> sahiptir; bu akıl iyiyi ve kötüyü bize bildirir.",
            "Ahlak yasası <b>kategorik imperatiftir</b>: her durumda geçerli, koşulsuz bir emir.",
            "Yapılan eylemde <b>niyet</b> önemlidir — bir şeyi <b>ödev olarak</b> yaparsan ahlaklı davranırsın.",
        ]))
        .add_callout(Callout("insight", "Kant'ta İki Alanı Karıştırma",
                             "<b>Bilgi alanında</b> Tanrı ve ruh hakkında kesin bilgi imkânsızdır; "
                             "<b>ahlak alanında</b> ise aynı Tanrı ve ruh, kanıt olarak değil "
                             "<b>postulat</b> olarak zorunludur. Kant Tanrı'yı bilgiden çıkarıp ahlaka yerleştirir."))
        .add_summary("Voltaire aklı ve hoşgörüyü, Rousseau doğaya dönüşü savunurken; Kant “bilgi duyuyla "
                     "başlar ama duyudan ibaret değildir” diyerek iki büyük akımı uzlaştırmıştır.")
    )

    chapters = [ch1, ch2, ch3, ch4, ch5, ch6, ch7]

    # ---------------------------------------------------------------- SÖZLÜK
    glossary = [
        Concept("Skolastik", "Felsefeyi teolojinin hizmetinde kullanan Orta Çağ okul geleneği.", "17. yy'da terk edildi.", 1),
        Concept("Rasyonalizm", "Bilginin tek güvenilir kaynağının akıl olduğu görüşü.", "Descartes, Spinoza, Leibniz.", 1),
        Concept("Empirizm", "Bilginin duyu ve deneyle kazanıldığı görüşü.", "Bacon, Hobbes, Locke.", 1),
        Concept("Tabula rasa", "“Boş levha”; zihnin doğuştan bilgi içermemesi.", "Locke'un temel tezi.", 1),
        Concept("A posteriori", "Deneyime dayanarak elde edilen bilgi.", "Empirizmin bilgi türü.", 1),
        Concept("Tümevarım", "Tekil gözlemlerden genel yargıya gitme.", "Empirizmin akıl yürütme biçimi.", 1),
        Concept("Otoriteryanizm", "Güçlü kişilerin görüşlerine körü körüne bağlanma.", "Rasyonalizm reddeder.", 1),
        Concept("Metodik şüphe", "Kesin bilgiye ulaşmak için kullanılan geçici şüphe.", "Descartes ve Augustinus.", 2),
        Concept("Cogito", "“Düşünüyorum o hâlde varım.”", "Şüphe edilemeyen ilk kesinlik.", 2),
        Concept("Töz (cevher)", "Var olmak için başka şeye ihtiyaç duymayan varlık.", "Descartes'ta iki, Spinoza'da tek.", 2),
        Concept("Uzam", "Maddenin kapladığı alan.", "Bedenin tanımlayıcı özelliği.", 2),
        Concept("Düalizm", "Ruh ile bedeni ayrı iki töz sayma.", "Descartes'ın çözümü.", 2),
        Concept("Epifiz bezi", "Descartes'a göre ruhun bedene bağlandığı nokta.", "Ruh–beden etkileşiminin yeri.", 2),
        Concept("Çürük elma metaforu", "Yanıltıcı bilgilerin ayıklanması benzetmesi.", "Descartes'ın yöntemi.", 2),
        Concept("Kötü cin hipotezi", "Yanlış karar verdiren durumlar için benzetme.", "Meditasyonlar'da geçer.", 2),
        Concept("Eklektik", "Farklı sistemlerden alınan unsurları birleştirme.", "Pascal bölümünde tanımlanır.", 3),
        Concept("Jansenizm", "Augustinus'un inayet öğretisine dayanan dinî hareket.", "Cornelius Jansenius.", 3),
        Concept("İnayet", "Tanrı'nın kurtarıcı lütfu.", "Kutsal logos aracılığıyla elde edilir.", 3),
        Concept("Memorial", "Pascal'ın 1654'teki dinî tecrübesini kaydettiği metin.", "Teolojiye dönüşünün başlangıcı.", 3),
        Concept("Bahis argümanı", "İnancı sonsuz kazanç–sonlu kayıp hesabına dayandırır.", "Kanıt değil, tercih.", 3),
        Concept("Leviathan", "Egemeni/devleti temsil eden deniz canavarı metaforu.", "Hobbes'un başyapıtı.", 4),
        Concept("Doğa durumu", "Devlet öncesi, herkesin kendini koruduğu durum.", "Sözleşmenin gerekçesi.", 4),
        Concept("Toplum sözleşmesi", "Herkesin anlaşıp haklarını egemene devretmesi.", "Devletin doğuşu.", 4),
        Concept("Occasionalizm", "Nedenselliğin gerçek failinin Tanrı olduğu görüşü.", "Vesilecilik; Malebranche.", 5),
        Concept("Monad", "Basit, bölünemez, ruhsal varlık birimi.", "Leibniz'in varlık anlayışı.", 5),
        Concept("Önceden kurulmuş uyum", "Zihin ve bedenin Tanrı'ca ayarlanmış uyumu.", "Leibniz'in çözümü.", 5),
        Concept("Teodise", "Kötülük problemine rasyonel açıklama; Tanrı'nın adaleti.", "En iyi mümkün dünya.", 5),
        Concept("Panteizm", "Tanrı ile evreni ayırmama.", "Spinoza'nın Etika'daki görüşü.", 5),
        Concept("Determinizm", "Evrende hiçbir şeyin nedensiz olmaması.", "Spinoza'nın doğa anlayışı.", 5),
        Concept("Deizm", "Tanrı'nın evreni yaratıp çekilmesi.", "18. yy dinî görüşü.", 6),
        Concept("Agnostisizm", "Tanrı'nın bilinemeyeceği görüşü.", "David Hume.", 6),
        Concept("Birincil nitelik", "Nesnenin gerçek özellikleri: yer kaplama, biçim, sayı.", "Locke'un ayrımı.", 6),
        Concept("İkincil nitelik", "Kişiden kişiye değişen: renk, koku, ses, tat.", "Locke'un ayrımı.", 6),
        Concept("Öznel idealizm", "Nesnelerin yalnızca algılandıkça var olması.", "Berkeley'in konumu.", 6),
        Concept("Bileşik tasavvur", "Zihnin basit izlenimleri birleştirmesiyle oluşan kurgu.", "Hume reddeder.", 6),
        Concept("Tümevarım problemi", "Gözlemin geleceği güvenceye alamaması.", "Siyah karga örneği.", 6),
        Concept("Soylu vahşi", "Medeniyetin bozmadığı doğal insan.", "Rousseau'nun ideali.", 7),
        Concept("Kategorik imperatif", "Koşulsuz, her durumda geçerli ahlak buyruğu.", "Kant'ın ahlak yasası.", 7),
        Concept("Pratik postulat", "Kanıtlanamayanı olduğu gibi kabul etme.", "Tanrı, ruh, özgür irade.", 7),
        Concept("Ödev ahlakı", "Ahlakiliği niyette ve ödevde arayan anlayış.", "Kant'ın etiği.", 7),
    ]

    # ------------------------------------------------------------------ TEST
    test_questions = [
        TestQuestion(1, "17. yüzyıl felsefesinin en belirgin özelliği aşağıdakilerden hangisidir?",
                     {"A": "Skolastik düşüncenin güçlenmesi", "B": "Akıl, deney ve bilimin ön plana çıkması",
                      "C": "Mistisizmin bilgi kaynağı sayılması", "D": "Romantizmin egemen olması",
                      "E": "Otoriteryanizmin benimsenmesi"}),
        TestQuestion(2, "“Tabula rasa” kavramı hangi akımın temel tezidir?",
                     {"A": "Rasyonalizm", "B": "Mistisizm", "C": "Empirizm", "D": "Panteizm", "E": "Determinizm"}),
        TestQuestion(3, "Descartes'ın yöntemindeki adımların doğru sırası hangisidir?",
                     {"A": "Analiz – Apaçıklık – Sentez – Kontrol", "B": "Apaçıklık – Analiz – Sentez – Kontrol",
                      "C": "Sentez – Analiz – Kontrol – Apaçıklık", "D": "Kontrol – Apaçıklık – Analiz – Sentez",
                      "E": "Apaçıklık – Sentez – Analiz – Kontrol"}),
        TestQuestion(4, "Descartes'ın şüpheciliği için aşağıdakilerden hangisi doğrudur?",
                     {"A": "Şüphe bir varış noktasıdır", "B": "Bilgiye ulaşmayı imkânsız kılar",
                      "C": "Kesin bilgiye giden bir araçtır", "D": "Yalnızca Tanrı'ya uygulanır",
                      "E": "Duyuları tümüyle güvenilir sayar"}),
        TestQuestion(5, "Descartes'a göre ruhun bedene bağlandığı nokta neresidir?",
                     {"A": "Kalp", "B": "Epifiz bezi", "C": "Beyin sapı", "D": "Kan", "E": "Uzam"}),
        TestQuestion(6, "Descartes'ın düalizminde “uzam” hangi töze aittir?",
                     {"A": "Ruh", "B": "Tin", "C": "Madde (beden)", "D": "Tanrı", "E": "Monad"}),
        TestQuestion(7, "Pascal'ın bahis argümanı için aşağıdakilerden hangisi doğrudur?",
                     {"A": "Tanrı'nın varlığının kesin kanıtıdır", "B": "Bir akıl yürütmedir, kanıt değildir",
                      "C": "Ateizmi savunur", "D": "Deneye dayanır", "E": "Tümevarımsaldır"}),
        TestQuestion(8, "Jansenizm'in dayandığı öğreti ve isim hangisidir?",
                     {"A": "Aquinolu Thomas'ın doğal teolojisi", "B": "Augustinus'un inayet öğretisi",
                      "C": "Aristoteles'in madde-form öğretisi", "D": "Platon'un idealar kuramı",
                      "E": "Descartes'ın düalizmi"}),
        TestQuestion(9, "Hobbes'un düşüncesini şekillendiren etkenler arasında aşağıdakilerden hangisi YOKTUR?",
                     {"A": "Galileo ve Kepler'in mekanik evren anlayışı", "B": "İngiliz iç savaşı",
                      "C": "Machiavelli'nin realizmi", "D": "Kant'ın kategorik imperatifi",
                      "E": "Descartes ile karşılaşması"}),
        TestQuestion(10, "Hobbes'a göre devletin ortaya çıkış biçimi nedir?",
                      {"A": "Tanrı'nın doğrudan buyruğu", "B": "Güçlünün zaferi",
                       "C": "Herkesin herkesle anlaşıp haklarını devretmesi", "D": "Doğal ayıklanma",
                       "E": "Kilise otoritesinin devri"}),
        TestQuestion(11, "Bilardo topları örneğinde hareketin gerçek failini Tanrı sayan görüş hangisidir?",
                      {"A": "Panteizm", "B": "Determinizm", "C": "Occasionalizm (vesilecilik)",
                       "D": "Öznel idealizm", "E": "Düalizm"}),
        TestQuestion(12, "Leibniz'in monadları için aşağıdakilerden hangisi YANLIŞTIR?",
                      {"A": "Basit ve bölünemezler", "B": "Birbirleriyle sürekli etkileşim hâlindedirler",
                       "C": "Yok edilemezler", "D": "Kendilerine özgü iç dünyaları vardır",
                       "E": "Önceden kurulmuş uyum içinde hareket ederler"}),
        TestQuestion(13, "Leibniz'in “Teodise”de çözmeye çalıştığı temel problem nedir?",
                      {"A": "Ruh–beden ilişkisi", "B": "Tümevarım problemi", "C": "Kötülük problemi",
                       "D": "Bilginin kaynağı", "E": "Devletin meşruiyeti"}),
        TestQuestion(14, "Spinoza'nın Tanrı anlayışı için aşağıdakilerden hangisi doğrudur?",
                      {"A": "Duaları kabul eden kişisel bir Tanrı", "B": "Evrenden ayrı, aşkın bir Tanrı",
                       "C": "Tanrı tözdür ve evrendeki bütün maddelerin toplamıdır",
                       "D": "Tanrı yalnızca bir vesiledir", "E": "Tanrı bilinemez"}),
        TestQuestion(15, "Locke'a göre aşağıdakilerden hangisi ikincil niteliktir?",
                      {"A": "Yer kaplama", "B": "Ağırlık", "C": "Biçim", "D": "Renk", "E": "Sayı"}),
        TestQuestion(16, "Berkeley'in Locke'tan ayrıldığı temel nokta nedir?",
                      {"A": "İkincil nitelikleri nesnel sayması", "B": "Birincil niteliklerin de öznel olduğunu savunması",
                       "C": "Doğuştan tasavvurları kabul etmesi", "D": "Deneyi reddetmesi",
                       "E": "Tümevarımı reddetmesi"}),
        TestQuestion(17, "Hume'a göre nedensellikteki zorunluluk beklentisi nerede yatar?",
                      {"A": "Nesnelerin kendisinde", "B": "Doğa yasalarında", "C": "Bizim bilincimizde",
                       "D": "Tanrı'nın iradesinde", "E": "Monadlarda"}),
        TestQuestion(18, "Hume'a göre insanın ahlaki eylemlerini belirleyen nedir?",
                      {"A": "Akıl", "B": "Duygular", "C": "Kategorik imperatif", "D": "Toplum sözleşmesi",
                       "E": "Doğuştan tasavvurlar"}),
        TestQuestion(19, "Rousseau'nun 18. yüzyılın genel ilerleme inancına karşı çıkışı hangi tezle özetlenir?",
                      {"A": "Bilim tüm sorunları çözer", "B": "Medeniyet insanı yozlaştırır",
                       "C": "Zihin boş bir levhadır", "D": "Var olmak algılanmaktır",
                       "E": "Tanrı en iyi dünyayı yaratmıştır"}),
        TestQuestion(20, "Kant'ın bilgi görüşünü en iyi özetleyen ifade hangisidir?",
                      {"A": "Bilgi yalnızca akıldan gelir", "B": "Bilgi yalnızca duyudan gelir",
                       "C": "Bilgi duyuyla başlar ama duyudan ibaret değildir",
                       "D": "Bilgi Tanrısal aydınlanmayla gelir", "E": "Bilgi imkânsızdır"}),
    ]
    answer_key_items = [
        AnswerItem(1, "B", "17. yüzyılda skolastik geride bırakılmış, <b>akıl, deney ve bilim</b> ön plana çıkmıştır."),
        AnswerItem(2, "C", "<b>Tabula rasa</b> (boş levha) empirizmin temel tezidir; Locke ile özdeşleşmiştir."),
        AnswerItem(3, "B", "Sıra: <b>Apaçıklık → Analiz → Sentez → Kontrol</b>. Kontrol, matematikteki sağlama gibidir."),
        AnswerItem(4, "C", "Descartes'ınki <b>metodik şüpheciliktir</b>: kesin bilgiye ulaşınca şüphe bırakılır."),
        AnswerItem(5, "B", "Ruh, beyindeki <b>epifiz bezine</b> yerleşmiştir; bedenin hareketini buradan sağlar."),
        AnswerItem(6, "C", "<b>Uzam</b> maddenin kapladığı alandır; ruh uzamda yer kaplamaz."),
        AnswerItem(7, "B", "Bahis argümanı bir <b>kanıt değil akıl yürütmedir</b>; inanmayı rasyonel bir tercih sayar."),
        AnswerItem(8, "B", "Jansenizm, <b>Augustinus'un inayet öğretisine</b> dayanır; adını Cornelius Jansenius'tan alır."),
        AnswerItem(9, "D", "Kant, Hobbes'tan sonraki bir filozoftur; onu etkilemesi mümkün değildir."),
        AnswerItem(10, "C", "Devlet, <b>herkesin herkesle anlaşıp</b> bütün hakları egemene devretmesiyle doğar."),
        AnswerItem(11, "C", "<b>Occasionalizm</b> (vesilecilik): gerçek fail Tanrı'dır, top yalnızca bir vesiledir."),
        AnswerItem(12, "B", "Monadlar birbiriyle <b>iletişime girmez</b>; aralarında etkileşim yoktur."),
        AnswerItem(13, "C", "<b>Teodise</b>, kötülük problemine rasyonel açıklama getirir: en iyi mümkün dünya."),
        AnswerItem(14, "C", "Spinoza <b>panteisttir</b>: Tanrı tözdür ve evrenden ayrı bir varlık değildir."),
        AnswerItem(15, "D", "<b>Renk</b> ikincil niteliktir; kişiden kişiye değişir. Diğerleri birincildir."),
        AnswerItem(16, "B", "Berkeley, <b>birincil niteliklerin de zihinsel</b> olduğunu savunarak ayrımı yıkar."),
        AnswerItem(17, "C", "Hume'a göre zorunluluk beklentisi cisimlerde değil <b>bizim bilincimizde</b> yatar."),
        AnswerItem(18, "B", "Hume ahlakta rasyonalizme karşıdır: eylemi <b>akıl değil duygular</b> belirler."),
        AnswerItem(19, "B", "Rousseau'ya göre <b>medeniyet ahlakı yıkar</b>; doğa hâli daha iyidir."),
        AnswerItem(20, "C", "Kant iki akımı birleştirir: bilgi <b>duyuyla başlar</b> ama akıl ona <b>biçim verir</b>."),
    ]

    return CoursePack(
        ders_klasoru="FELSEFE TARİHİ 2",
        course_code="17.–18. YÜZYIL",
        title='Felsefe Tarihi<span class="accent-word"> II</span>',
        subtitle="Descartes'tan Kant'a: 17. ve 18. Yüzyıl Batı Felsefesi",
        description=(
            "Skolastiğin bırakılmasıyla başlayan, rasyonalizm ile empirizm arasında bölünen 17. yüzyıldan; "
            "Aydınlanma'nın aklı, özgürlüğü ve insan haklarını merkeze aldığı 18. yüzyıla uzanan; Descartes'ın "
            "cogito'sundan Kant'ın kategorik imperatifine kadar modern düşüncenin temel duraklarını kapsayan "
            "vize sınavı özeti."
        ),
        sinav_etiketi="Vize",
        theme="plum",
        theme_color="#5A3A72",
        icon_text="F",
        chapters=chapters,
        glossary=glossary,
        test_title="Genel Değerlendirme Testi",
        test_subtitle="Descartes'tan Kant'a, 17. ve 18. yüzyıl felsefesi üzerine kapsamlı çoktan seçmeli test",
        test_instructions="Aşağıdaki sorularda beş seçenekten yalnızca birini işaretleyiniz. Süre: 30 dakika.",
        test_questions=test_questions,
        answer_key_intro="Her sorunun doğru cevabı ve kısa gerekçesi aşağıda yer almaktadır.",
        answer_key_items=answer_key_items,
        overview_lead=(
            "Bu ders; skolastiğin terk edildiği <b>17. yüzyıldan</b> Aydınlanma'nın zirvesine uzanan iki "
            "yüzyılı, <b>rasyonalizm ile empirizm</b> arasındaki büyük ayrım ekseninde izler ve bu ayrımın "
            "<b>Kant'ta</b> nasıl uzlaştırıldığını gösterir."
        ),
        overview_cards=[
            {"title": "Akıl ve Deney", "text": "Skolastiğin sonu; rasyonalizm ile empirizmin doğuşu ve karşıtlığı."},
            {"title": "Descartes'ın Sistemi", "text": "Metodik şüphe, cogito, Tanrı kanıtı ve ruh–beden düalizmi."},
            {"title": "İnanç ve Akıl", "text": "Jansenizm'in inayet öğretisi ve Pascal'ın bahis argümanı."},
            {"title": "Modern Devlet", "text": "Hobbes'ta doğa durumundan toplum sözleşmesine ve Leviathan'a."},
            {"title": "Üç Rasyonalist", "text": "Malebranche'ın vesileciliği, Leibniz'in monadları, Spinoza'nın panteizmi."},
            {"title": "Aydınlanma", "text": "Locke, Berkeley, Hume; Voltaire, Rousseau ve Kant'ın sentezi."},
        ],
        overview_flow=[
            ("17. Yüzyıl", "Akıl ve deney ayrışır"),
            ("Descartes", "Şüphe → cogito → düalizm"),
            ("Rasyonalistler", "Malebranche, Leibniz, Spinoza"),
            ("Empiristler", "Locke, Berkeley, Hume"),
            ("Kant", "İki akımın sentezi"),
        ],
        overview_note=(
            "Sınavda en çok karıştırılan üç nokta: <b>rasyonalizm–empirizm</b> ayrımı, <b>ruh–beden sorununa "
            "verilen üç farklı cevap</b> (Descartes / Malebranche / Leibniz) ve <b>Locke ile Berkeley'in "
            "nitelikler konusundaki anlaşmazlığı</b>."
        ),
    )
