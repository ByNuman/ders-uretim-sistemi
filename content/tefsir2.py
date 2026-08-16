# -*- coding: utf-8 -*-
"""TEFSİR II — Görsel Ders Notu Kitabı, içerik tanımı.
Kaynak: '8_TEFSİR 2_FİNAL ÖZET(10).pdf' (ham metin özet, 17 sayfa).

TEKNİK NOT (Arapça desteği): Sistemde başlangıçta Arapça glyph render eden
bir font kurulu değildi ve internet erişimi kapalı olduğu için yeni font
indirilemiyordu. Kullanıcının PDF'i tekrar yüklemesi üzerine, o PDF'in
içine gömülü TrueType fontlar (pikepdf ile) çıkarıldı ve incelendi; bu
sırada sistemde zaten kurulu olan DejaVu Sans fontunun TAM Arapça harf
kapsamına ve otomatik harf-bitiştirme (GSUB: init/medi/fina) desteğine
sahip olduğu keşfedildi ve test edildi. Bu sayede AYETLERİN orijinal
Arapça metni (sabit, doğrulanabilir Mushaf metni olduğu için güvenle
yazılabilir) bu sürümde eklenmiştir. Müfessirlerin tefsir alıntılarının
Arapça orijinali ise eklenmemiştir -- kaynak PDF'teki bu kısımların metin
katmanı RTL sıralama hatasıyla bozuk çıkmış, ve bu spesifik alıntılar
ezbere bilinen sabit metinler olmadığından uydurma riski taşımaktadır;
onlar için kaynaktaki Türkçe çeviri kullanılmaya devam edilmiştir.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from content_model import (
    Person, KeyTerm, Callout, FlowStep, FlowDiagram, ComparisonTable,
    InfoCard, BulletBlock, Chapter, ChapterPage, Concept, CoursePack,
    QAItem, DistinctionPair, MatchRow, Ayah,
)

TAHIR_IBN_ASHUR = Person(
    id="tahir", name="Tâhir b. Âşûr", years="1879–1973",
    tagline="et-Tahrîr ve't-Tenvîr Müellifi",
    bio=["Tunus Zeytûne Üniversitesi'nde rektörlük yapmış; ayetlerin <b>edebi ve belâgat</b> yönlerini eşsiz bir "
         "titizlikle incelemiş, İsrailiyat'ı reddederek akıl ve nakli dengeli birleştirmiştir."],
    key_work="et-Tahrîr ve't-Tenvîr",
    initials="İA",
)
IBN_JUZAYY = Person(
    id="ibn_cuzey", name="İbn Cüzey el-Kelbî", years="1294–1340",
    tagline="et-Teshîl li-ʿulûmi't-tenzîl Müellifi",
    bio=["Gırnata'da imam-hatiplik yapmış, Tarîf Savaşı'nda şehit düşmüştür. Sahih hadisleri merkeze alıp "
         "İsrailiyat'a temkinli yaklaşan, sade ve sistematik bir üslup benimsemiştir."],
    key_work="et-Teshîl li-ʿulûmi't-tenzîl",
    initials="İC",
)
NASAFI = Person(
    id="nesefi", name="Ebü'l-Berekât en-Nesefî", years="1223–1310",
    tagline="Medârikü't-Tenzîl (Nesefî Tefsiri) Müellifi",
    bio=["Moğol istilası döneminde Nesef'ten Kirman'a göç etmiş; Hanefî fıkhının ve Mâtürîdî itikadının kilit "
         "isimlerindendir. Eserleri Osmanlı coğrafyasında asırlarca ders kitabı olarak okutulmuştur."],
    key_work="Medârikü't-Tenzîl ve Hakâiku't-Te'vîl",
    initials="N",
)
DARWAZA = Person(
    id="derveze", name="Muhammed İzzet Derveze", years="1888–1984",
    tagline="et-Tefsîrü'l-Hadîs Müellifi",
    bio=["Filistin davasına derin bağlılığıyla tanınan 20. yüzyıl düşünürü. Klasik tefsir sıralamasından ayrılarak "
         "Kur'an'ı <b>Nüzul Sırasına Göre</b> yorumlamış, tarihsel bağlamı öne çıkarmıştır."],
    key_work="et-Tefsîrü'l-Hadîs",
)
AL_KHAZIN = Person(
    id="hazin", name="Ali b. Muhammed el-Hâzin", years="1279–1341",
    tagline="Lübâbü't-Te'vîl (Hâzin Tefsiri) Müellifi",
    bio=["Dımaşk'taki Sümeysâtiyye Kütüphanesi'nin yöneticiliğini yapmış, bu yüzden 'el-Hâzin' lakabıyla anılmıştır. "
         "Ansiklopedik bir âlim olarak eserinde dört büyük tefsirden derleme yapmıştır."],
    key_work="Lübâbü't-Te'vîl fî Meʿâni't-Tenzîl",
    initials="H",
)


def get_pack() -> CoursePack:

    # =====================================================================
    # BÖLÜM 1 — Kur'an'da Güzel Ahlâk
    # =====================================================================
    ch1 = Chapter(
        number=1,
        title="Kur'an'da Güzel Ahlâk",
        subtitle="Cahiliye mürüvvetinden evrensel erdemler sistemine; ahlakın Kur'ânî temelleri",
        key_terms=[
            KeyTerm("Ma'rûf", "Akıl ve dinin iyi kabul ettiği, toplumun ortak vicdanında 'tanıdık' ve 'güzel' karşılanan her şey."),
            KeyTerm("Ahsen-i Takvim", "İnsanın 'en güzel kıvamda' yaratılmış olması; ancak hem kötülüğe (fücûr) hem de sakınmaya (takvâ) meyilli çift kutuplu fıtratı."),
            KeyTerm("Mürüvvet", "Cahiliye Arap toplumunda kabile asabiyetine dayalı; cesaret, misafirperverlik ve intikamı kapsayan eski erdem anlayışı."),
            KeyTerm("İstiare (Belâgat)", "Bir kavramı, maddi bir olgudan ödünç alınan bir kelimeyle anlatma sanatı — Kur'an'da soyut yüceliği somutlaştırmak için kullanılır."),
        ],
    )
    ch1.pages.append(
        ChapterPage()
        .add_terms(ch1.key_terms)
        .add_block(BulletBlock(1, "Cahiliyeden İslam'a Ahlâkî Dönüşüm", [
            "İslam öncesi Arap toplumunda ahlâk, kabile asabiyetine ve bedevi yaşam tarzına dayalı <b>'Mürüvvet'</b> "
            "kavamıyla ifade edilirdi — cesaret, misafirperverlik ve intikam gibi erdemleri kapsar ama temeli kabile "
            "gururuydu. İslam, bu kalıbı kırarak ahlâkı, temeli 'Allah korkusu ve rızası' olan, kibre değil "
            "tevazuya dayanan evrensel bir erdemler sistemine dönüştürmüştür.",
            "<b>İnsanın Ahlâkî Fıtratı:</b> Kur'an insanı en güzel kıvamda (Ahsen-i Takvim) yaratılmış tanımlar; "
            "ancak ona hem kötülüğe meyil (Fücûr) hem de sakınma yeteneği (Takvâ) ilham edilmiştir. Nefsini "
            "arındıran kurtuluşa erer, fücura daldıran ise 'Esfel-i Sâfilîn'e (aşağıların aşağısına) yuvarlanır.",
        ]))
    )
    ch1.pages.append(
        ChapterPage(continue_tag="Ayet-i Kerîmeler")
        .add_ayat("Ayet-i Kerîmeler", [
            Ayah(
                "Lokmân 17",
                "يَا بُنَيَّ أَقِمِ الصَّلَاةَ وَأْمُرْ بِالْمَعْرُوفِ وَانْهَ عَنِ الْمُنكَرِ وَاصْبِرْ عَلَىٰ مَا أَصَابَكَ ۖ إِنَّ ذَٰلِكَ مِنْ عَزْمِ الْأُمُورِ",
                "Yavrum! Namazı dosdoğru kıl, iyiliği emret, kötülükten sakındır. Başına gelen musibetlere karşı sabırlı ol. Şüphesiz bunlar, azmedilmeye değer işlerdendir.",
                "<b>Ma'rûf:</b> Akıl ve dinin iyi kabul ettiği, toplumun ortak vicdanında güzel karşılanan şey.",
            ),
            Ayah(
                "Furkân 63",
                "وَعِبَادُ الرَّحْمَٰنِ الَّذِينَ يَمْشُونَ عَلَى الْأَرْضِ هَوْنًا وَإِذَا خَاطَبَهُمُ الْجَاهِلُونَ قَالُوا سَلَامًا",
                "Rahmân'ın has kulları, yeryüzünde tevazu ve vakâr ile yürüyen kimselerdir. Cahiller onlara laf attığında 'Selâm!' derler.",
                "<b>Hevnen:</b> Kendini beğenmişlikten uzak, ağırbaşlı ve mütevazı bir duruş.",
            ),
            Ayah(
                "Kalem 4",
                "وَإِنَّكَ لَعَلَىٰ خُلُقٍ عَظِيمٍ",
                "Ve şüphesiz sen yüce bir ahlâk üzeresin.",
                "<b>Azîm:</b> Kadri, kıymeti ve etkisi çok büyük; takdir edilemeyecek kadar yüce.",
            ),
        ])
    )
    ch1.pages.append(
        ChapterPage(continue_tag="Konu Anlatımı: Ahlâkın Kur'ânî Temelleri")
        .add_table(ComparisonTable(
            "Değerlerin Kaynağı Tartışması (Sınavlık Mezhep Ayrımı)",
            ["Ekol", "Görüş"],
            [
                ["Mu'tezile (Akılcılar)", "Ahlâkî değerler objektiftir ve akılla bilinebilir; akıl, vahiy olmasa bile iyiyi-kötüyü bulabilir."],
                ["Eş'ariyye (Vahiyciler)", "Ahlâkın tek kaynağı vahiydir; bir şey Allah emrettiği için 'iyi', yasakladığı için 'kötü'dür."],
                ["Mâtürîdîyye (Sentezciler)", "Akıl değerlerin bir kısmını kavrayabilir; ama 'sevap/günah' hükmü için vahyin bildirimi şarttır."],
            ]
        ))
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "İslam'da ahlâk, ibadetten bağımsız düşünülemez. Kur'an'a göre namaz insanı <b>'fahşâ ve münkerden'</b> "
            "alıkoyan bir eylemdir. İslâm ahlâkının en yüksek gayesi faydacı bir beklenti değil, Allah'ın "
            "hoşnutluğunu kazanmaktır."))
    )
    ch1.pages.append(
        ChapterPage(continue_tag="Örnek Metin ve Müfessir")
        .add_block(BulletBlock(2, "Örnek Tefsir Metni: Tâhir b. Âşûr — Kalem Suresi 4 Tefsiri", [
            "Allah, elçisinin nefsini mükâfat vaadiyle rahatlattıktan sonra, düşmanların 'mecnun' demeleri gibi "
            "beyhude sözlerini çürütmeye döndü; onun yüce bir ahlâka büründüğünü ispat etti — ki bu, deliliğin "
            "tam zıddıdır.",
            "<b>Huluk (ahlâk):</b> Nefsin kalıcı tabiatlarıdır; ardından bir sıfat gelmezse çoğu zaman iyi tabiat ve "
            "erdemler için kullanılır.",
            "<b>'Azîm' kelimesi</b> kadri yüksek olan demektir; aslında cisimlerin iriliğinden ödünç alınmış bir "
            "mecazdır, ama o kadar yaygınlaşmıştır ki artık manevi yücelik için hakikat seviyesine ulaşmıştır.",
            "Bu yüce ahlâk, tüm erdemleri kendinde topladığı için en kapsamlı tefsiri Hz. Âişe'nin (r.a.) verdiği "
            "cevaptır: <b>'Onun ahlâkı Kur'an idi.'</b>",
        ]))
        .add_callout(Callout("focus", "Nahiv ve Belâgat Nüktesi",
            "<b>Nahiv (Temekkün):</b> 'Alâ' edatı sıradan bir 'üzerinde olma' değil, atın sırtına sağlamca oturan "
            "bir binici gibi Hz. Peygamber'in o ahlâka bütünüyle hâkim olduğunu gramer yoluyla ispatlar. "
            "<b>Belâgat (İstiare):</b> 'Azîm' kelimesinin maddi büyüklükten soyut karakter yüceliğine taşınması, "
            "manevi büyüklüğü zihne kazıyan güçlü bir istiaredir."))
        .add_person(TAHIR_IBN_ASHUR)
        .add_summary("Kur'an'da güzel ahlâk, cahiliyenin kabileci mürüvvet anlayışını aşan evrensel bir erdemler "
            "sistemidir. İnsanın fücur-takvâ arasındaki iradi tercihine dayanır; değerlerin kaynağı konusunda "
            "Mu'tezile aklı, Eş'ariyye vahyi, Mâtürîdiyye ise ikisinin dengesini esas alır.")
    )

    # =====================================================================
    # BÖLÜM 2 — Kur'an'da Yerilen Olumsuz Davranışlar
    # =====================================================================
    ch2 = Chapter(
        number=2,
        title="Kur'an'da Yerilen Olumsuz Davranışlar",
        subtitle="Tecessüsten gıybete: toplumsal dokuyu tahrip eden davranışların kavramsal haritası",
        key_terms=[
            KeyTerm("Tecessüs", "İnsanların gizli hallerini, ayıp ve kusurlarını kötü niyetle araştırmak, casusluk yapmak."),
            KeyTerm("Hümeze ve Lümeze", "Hümeze arkadan çekiştirmek, kaş-göz işaretiyle ayıplamak; lümeze ise yüze karşı küçük düşürmek ve alay etmek."),
            KeyTerm("Hevâ", "Bencil ve nefsani arzular; hakkı görmeyi engelleyen, insanı adaletten saptıran zifiri bir perde."),
            KeyTerm("Gıybet", "Bir kimseden, duyduğunda hoşlanmayacağı şekilde bahsetmek; Kur'an'da 'ölü kardeşinin etini yemek' teşbihiyle kınanır."),
        ],
    )
    ch2.pages.append(
        ChapterPage()
        .add_terms(ch2.key_terms)
        .add_block(BulletBlock(1, "Kötü Ahlâkın Kavramsal Ağı ve Çift Kutupluluk", [
            "Kur'an, yerilen davranışları ifade etmek için geniş bir kavramsal yapı kullanır: günah (ism), sapıklık "
            "(dalâl), hayasızlık (fahşâ), haddi aşma (bağy), kötü iş (seyyie), yoldan çıkma (fısk) ve günahkârlık "
            "(fücûr). Bu kötü huylar genel olarak 'sûü'l-huluk' veya 'el-ahlâku'z-zemîme' terimleriyle anılır.",
            "<b>Hevâ Engeli:</b> İnsan fıtratı gereği çift kutupludur (fücûr-takvâ). Ahlâki çöküşün en büyük sebebi "
            "Hevâ'dır — Kur'an, kötü arzularının esiri olanı 'hevâsını ilah edinen' kişi olarak niteler.",
        ]))
    )
    ch2.pages.append(
        ChapterPage(continue_tag="Ayet-i Kerîmeler")
        .add_ayat("Ayet-i Kerîmeler", [
            Ayah(
                "Hucurât 12",
                "يَا أَيُّهَا الَّذِينَ آمَنُوا اجْتَنِبُوا كَثِيرًا مِنَ الظَّنِّ إِنَّ بَعْضَ الظَّنِّ إِثْمٌ ۖ وَلَا تَجَسَّسُوا وَلَا يَغْتَب بَّعْضُكُم بَعْضًا ۚ أَيُحِبُّ أَحَدُكُمْ أَن يَأْكُلَ لَحْمَ أَخِيهِ مَيْتًا فَكَرِهْتُمُوهُ",
                "Ey iman edenler! Zannın birçoğundan sakının. Çünkü bazı zanlar günahtır. Birbirinizin gizli hallerini araştırmayın ve biriniz diğerinizi gıybet etmesin. Sizden biri, ölü kardeşinin etini yemekten hoşlanır mı? İşte bundan iğrendiniz.",
                "<b>Tecessüs:</b> İnsanların gizli hallerini kötü niyetle araştırmak, casusluk yapmak.",
            ),
            Ayah(
                "Hümeze 1-3",
                "وَيْلٌ لِّكُلِّ هُمَزَةٍ لُّمَزَةٍ الَّذِي جَمَعَ مَالًا وَعَدَّدَهُ يَحْسَبُ أَنَّ مَالَهُ أَخْلَدَهُ",
                "Arkadan çekiştirmeyi, yüze karşı alay etmeyi âdet edinen herkesin vay haline! O ki, mal toplamış ve onu tekrar tekrar saymıştır. Malının kendisini ebedi kılacağını zanneder.",
                "<b>Hümeze/Lümeze:</b> Arkadan çekiştirme / yüze karşı küçük düşürüp alay etme.",
            ),
        ])
    )
    ch2.pages.append(
        ChapterPage(continue_tag="Konu Anlatımı: Kötü Ahlâkın Kavramsal Ağı")
        .add_table(ComparisonTable(
            "Toplumsal Çöküşün Sebepleri (Yerilen Temel Davranışlar)",
            ["Davranış", "Açıklama"],
            [
                ["Haksızlık ve Zulüm", "Kabile gururu veya şahsi menfaat için başkasının hakkını gasp etmek; cahiliyede en çok eleştirilen husus."],
                ["Cimrilik (İsarın Terki)", "Muhtaçlara yardım etmemek ve el açıp isteyeni azarlamak; merhamet eksikliğinin nişanesi."],
                ["Kibir ve Serkeşlik", "Kendini üstün görmek, asaletle övünmek; takvânın tam zıddı olan Câhiliye tutuculuğu."],
                ["Haset ve Gıybet", "Haset, Allah'a sığınılması gereken karanlık bir duygu; gıybet 'ölü kardeş eti yemek' teşbihiyle kınanır."],
            ]
        ))
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "İslam'da ahlâki terakki, olumsuz davranışlardan tam manasıyla hicret etmekle başlar. İnsanın iyilik "
            "yaptığında sevinç, kötülük yaptığında vicdanen rahatsızlık duyabilmesi, <b>kâmil imanın en temel "
            "göstergesi</b> kabul edilir."))
    )
    ch2.pages.append(
        ChapterPage(continue_tag="Örnek Metin ve Müfessir")
        .add_block(BulletBlock(2, "Örnek Tefsir Metni: İbn Cüzey — Hucurât Suresi 12 Tefsiri", [
            "'Zannın birçoğundan sakının' ayeti, Müslümanlar hakkında kötü zan (suizân) beslemeyi ifade eder; iyi "
            "zan (hüsnüzan) ise güzel bir davranıştır.",
            "'Bazı zanlar günahtır' — denildi ki buradaki günah manası 'yalan' demektir; zira Hz. Peygamber "
            "'Zandan sakının, çünkü zan sözlerin en yalanıdır' buyurmuştur.",
            "'Tecessüs etmeyin' — Hasan-ı Basrî bu kelimeyi 'tahassüs' şeklinde okumuştur: 'cim' ile tecessüs "
            "kötülükleri, 'ha' ile tahassüs ise iyilikleri araştırmaktır.",
            "Allah gıybeti, insan etini ölü iken yemeye benzetmiştir; leş iğrenç bir şey olduğu için onu 'ölü' "
            "yaparak bu çirkinliği daha da vurgulamıştır.",
        ]))
        .add_callout(Callout("focus", "Nahiv ve Belâgat Nüktesi",
            "<b>Nahiv (Hâl ve Kıraat):</b> 'Meyten' (ölü) kelimesi cümlede Hâl'dir — 'kardeşinin etini ölü olduğu "
            "halde yeme' demektir. <b>Belâgat (Mübalağa ve Temsilî Teşbih):</b> Gıybetin çirkinliği katman katman "
            "artırılmıştır: Et yemek → İnsan eti → Ölü insan eti → Kendi ölü kardeşinin eti! 'Sever misiniz?' "
            "fiili ile güçlü bir <b>Tezat Sanatı (İstifhâm-ı İnkârî)</b> yapılmıştır."))
        .add_person(IBN_JUZAYY)
        .add_summary("Kur'an'ın yerdiği davranışlar bireysel günahtan öte, toplumun sosyal dokusunu tahrip eden "
            "bir 'virüs' olarak ele alınır. Haksızlık, cimrilik, kibir ve gıybet gibi davranışlardan hicret etmek, "
            "kâmil imanın göstergesi sayılır.")
    )

    # =====================================================================
    # BÖLÜM 3 — Kur'an'da Adalet
    # =====================================================================
    ch3 = Chapter(
        number=3,
        title="Kur'an'da Adalet",
        subtitle="Şahitlikten savaşa, kozmik bir ilkeden vicdani eğitime uzanan adalet tasavvuru",
        key_terms=[
            KeyTerm("Adl", "Denk olmak, eşitlik, insaf etmek; terazinin kefelerini eşitleyip ifrat-tefrit arasında orta yolu bulmak."),
            KeyTerm("Kıst", "Pay, nasip ve hakkaniyet; hakkı sahibine eksiksiz ve pratik olarak teslim etmek."),
            KeyTerm("Zulüm", "Adaletin tam zıddı; bir şeyi ait olduğu bağlamdan koparmak ve hakkı sahibinden esirgemek."),
            KeyTerm("Kozmik Adalet", "Kur'an'ın adaleti yalnız beşeri bir erdem değil, kâinatın üzerine bina edildiği evrensel ilke olarak sunması."),
        ],
    )
    ch3.pages.append(
        ChapterPage()
        .add_terms(ch3.key_terms)
        .add_block(BulletBlock(1, "Adaletin Kavramsal Boyutları ve Kozmik İlke Olması", [
            "Kur'an'da adalet; 'adl', 'kıst', 'keyl' (ölçü) ve 'hak' gibi kavramlarla ifade edilir: <b>'İnsanlar "
            "arasında bir tarafa meyletmeden davranmak ve herkese hak ettiğini vermek.'</b> Tam zıddı ise Zulüm, "
            "cevr ve insafsızlıktır.",
            "Kur'an, adaleti yalnızca beşeri bir erdem değil, kâinatın üzerine bina edildiği <b>'kozmik bir "
            "ilke'</b> olarak takdim eder. Allah gökleri ve yeri 'hak' ile yaratmış, evrendeki düzeni adalet "
            "üzerine bina etmiştir.",
        ]))
    )
    ch3.pages.append(
        ChapterPage(continue_tag="Ayet-i Kerîmeler")
        .add_ayat("Ayet-i Kerîmeler", [
            Ayah(
                "Nisâ 135",
                "يَا أَيُّهَا الَّذِينَ آمَنُوا كُونُوا قَوَّامِينَ بِالْقِسْطِ شُهَدَاءَ لِلَّهِ وَلَوْ عَلَىٰ أَنفُسِكُمْ أَوِ الْوَالِدَيْنِ وَالْأَقْرَبِينَ ۚ إِن يَكُنْ غَنِيًّا أَوْ فَقِيرًا فَاللَّهُ أَوْلَىٰ بِهِمَا",
                "Ey iman edenler! Allah için hakkı titizlikle ayakta tutan, adalet ile şahitlik eden kimseler olun. Şahitliğiniz kendi aleyhinize, anne-babanızın ve yakın akrabanızın aleyhine dahi olsa adaletten şaşmayın.",
                "<b>Kıst:</b> Pay, nasip ve hakkaniyet; hakkı sahibine eksiksiz teslim etmek.",
            ),
            Ayah(
                "Nisâ 58",
                "إِنَّ اللَّهَ يَأْمُرُكُمْ أَن تُؤَدُّوا الْأَمَانَاتِ إِلَىٰ أَهْلِهَا وَإِذَا حَكَمْتُم بَيْنَ النَّاسِ أَن تَحْكُمُوا بِالْعَدْلِ ۚ إِنَّ اللَّهَ نِعِمَّا يَعِظُكُم بِهِ",
                "Şüphesiz Allah, emanetleri ehline teslim etmenizi ve insanlar arasında hükmettiğiniz zaman adaletle hükmetmenizi emreder.",
                "<b>Adl:</b> Denk olmak, eşitlik, ifrat ile tefrit arasında orta yolu bulmak.",
            ),
            Ayah(
                "Mâide 8",
                "وَلَا يَجْرِمَنَّكُمْ شَنَآنُ قَوْمٍ عَلَىٰ أَلَّا تَعْدِلُوا ۚ اعْدِلُوا هُوَ أَقْرَبُ لِلتَّقْوَىٰ",
                "Bir topluluğa olan kininiz, sizi adaletsizliğe itmesin. Adil olun; bu, takvaya daha uygundur.",
                "",
            ),
        ])
    )
    ch3.pages.append(
        ChapterPage(continue_tag="Konu Anlatımı: Adaletin Kozmik Boyutu")
        .add_block(BulletBlock(2, "Ahiret İnancı ve Vicdani Eğitim", [
            "Adaletin fiziki müeyyidelerden önce insanın kalbinde kök "
            "salması amaçlanır; hesaba çekilme inancı, otoritenin bulunmadığı gizli yerlerde bile zulümden "
            "uzaklaştıran en büyük denetim gücüdür.",
        ]))
        .add_table(ComparisonTable(
            "Kur'an'da Adaletin Temel Uygulama Alanları",
            ["Alan", "Açıklama"],
            [
                ["Hüküm ve Şahitlikte Adalet", "Şahitlik kendi/anne-baba/akraba aleyhine dahi olsa objektiflik bozulmaz; zengin-fakir statüsü adaleti değiştiremez."],
                ["Cezada Adalet", "Suç-ceza dengesi esastır; kötülüğün cezası misliyledir, ama affetme kapısı daima açıktır."],
                ["Savaşta Adalet", "Cihad sömürü veya ganimet amaçlı değil, zulmü ve fitneyi ortadan kaldırmak içindir."],
                ["Toplumsal-Ekonomik Adalet", "Irk/soy üstünlüğü reddedilir, üstünlük yalnız takvâdadır; zekât ve sadaka ile servet tabana yayılır."],
            ]
        ))
    )
    ch3.pages.append(
        ChapterPage(continue_tag="Örnek Metin ve Müfessir")
        .add_block(BulletBlock(2, "Örnek Tefsir Metni: Nesefî — Nisâ Suresi 135 Tefsiri", [
            "'Şühedâe' (şahitlik edenler) kelimesi, şahitliklerinizi sadece Allah'ın rızası için yerine "
            "getirirsiniz anlamındadır. 'Kendi aleyhinize dahi olsa' — kişinin kendi nefsine karşı şahitliği, "
            "aslında kendi aleyhine yaptığı bir ikrardır (kabullenmedir).",
            "'Zengin ise' onun zenginliği, rızasını arama gayesiyle şahitliğe engel olmasın. 'Fakir ise' ona "
            "acımak sizi şahitlikten alıkoymasın — Allah ikisine de (sizden) daha yakındır.",
            "'Eğer eğip bükerseniz' — bu kelime iki farklı kıraatle okunur: bir okuyuşta 'Siyasi/Yönetimsel "
            "Adalet' (vali olursanız), diğerinde 'Dili eğip bükerek yalan şahitlik yapma' bağlamına oturur.",
        ]))
        .add_callout(Callout("focus", "Nahiv ve Belâgat Nüktesi",
            "<b>Nahiv (Kıraat ve Gramer Etkisi):</b> 'Ve in telvû' kelimesinin iki farklı okunuşu, ayetin manasını "
            "katmanlandırır — bir harekenin dahi manayı nasıl derinleştirdiğini gösterir. <b>Nahiv (Zamir "
            "Uyumu):</b> 'Hümâ' (o ikisi) ikil zamiri, zengin ve fakirin şahıs değil iki farklı 'sınıf' olarak "
            "kastedildiğini ispatlar."))
        .add_person(NASAFI)
        .add_summary("Kur'an'da adalet, adl-kıst-hak kavramlarıyla örülü, kozmik bir ilke düzeyine yükseltilmiş "
            "bir değerdir. Hüküm-şahitlik, ceza, savaş ve toplumsal-ekonomik alanlarda somutlaşır; nihai güvence "
            "ise Allah'ın her an gördüğü şuuruna sahip vicdanlı insan modelidir.")
    )

    # =====================================================================
    # BÖLÜM 4 — Kur'an'da İnsan Özgürlüğü ve Sorumluluğu
    # =====================================================================
    ch4 = Chapter(
        number=4,
        title="Kur'an'da İnsan Özgürlüğü ve Sorumluluğu",
        subtitle="Hilâfet ve Emanet'ten ef'âlü'l-ibâd tartışmasına özgürlüğün Kur'ânî sınırları",
        key_terms=[
            KeyTerm("Hilâfet", "Allah'ın insanı yeryüzüne halife kılıp ona tasarrufta bulunma yetkisi vermesi."),
            KeyTerm("Emanet", "Ahzâb 72'de göklerin, yerin ve dağların çekindiği; insanın hür iradesiyle üstlendiği sorumluluk."),
            KeyTerm("İstitaat", "Ehl-i Sünnet/Mâtürîdiyye'ye göre insanın eylem anında Allah'ın verdiği gücü kullanarak özgür seçim yapması."),
            KeyTerm("Vizr", "Ağır yük, vebal, günah; İslam hukukundaki 'suçun ve cezanın şahsiliği' ilkesinin teolojik dayanağı."),
        ],
    )
    ch4.pages.append(
        ChapterPage()
        .add_terms(ch4.key_terms)
        .add_block(BulletBlock(1, "Özgürlüğün İki Kur'ânî Temeli: Hilâfet ve Emanet", [
            "Kur'an'da insanın özgürlüğü ve sorumluluğu iki sembol üzerinden temellendirilir: <b>Hilâfet</b> — "
            "Allah insanı yeryüzüne halife kılıp tasarruf yetkisi vermiştir; <b>Emanet</b> — Ahzâb 72'de göklerin, "
            "yerin ve dağların yüklenmekten çekindiği emaneti insan hür iradesiyle üstlenmiştir. Emaneti hakkıyla "
            "taşımamak Kur'an'da 'zulüm' ve 'cehalet' olarak nitelendirilir.",
        ]))
    )
    ch4.pages.append(
        ChapterPage(continue_tag="Ayet-i Kerîmeler")
        .add_ayat("Ayet-i Kerîmeler", [
            Ayah(
                "İsrâ 15",
                "مَّنِ اهْتَدَىٰ فَإِنَّمَا يَهْتَدِي لِنَفْسِهِ ۖ وَمَن ضَلَّ فَإِنَّمَا يَضِلُّ عَلَيْهَا ۚ وَلَا تَزِرُ وَازِرَةٌ وِزْرَ أُخْرَىٰ",
                "Kim doğru yola ererse ancak kendi nefsi lehine ermiş olur. Kim de saparsa ancak kendi aleyhine sapmış olur. Hiçbir günahkâr başkasının günah yükünü yüklenmez.",
                "<b>Vizr:</b> Ağır yük, vebal, günah — suçun şahsiliği ilkesinin dayanağı.",
            ),
            Ayah(
                "Fussilet 46",
                "مَنْ عَمِلَ صَالِحًا فَلِنَفْسِهِ ۖ وَمَنْ أَسَاءَ فَعَلَيْهَا ۗ وَمَا رَبُّكَ بِظَلَّامٍ لِّلْعَبِيدِ",
                "Kim salih bir iş yaparsa kendi lehinedir. Kim de kötülük yaparsa kendi aleyhinedir. Rabbin kullarına asla zulmedici değildir.",
                "<b>Zallâm:</b> Çokça zulmeden — Allah'ın adaletinin mutlaklığına vurgu.",
            ),
        ])
    )
    ch4.pages.append(
        ChapterPage(continue_tag="Konu Anlatımı: Hilâfet, Emanet ve Fiillerin Yaratıcısı")
        .add_table(ComparisonTable(
            "Fiillerin Yaratıcısı Kimdir? (Sınavlık Mezhep Tartışması — Ef'âlü'l-İbâd)",
            ["Ekol", "Görüş"],
            [
                ["Cebriyye (Kaderciler)", "İnsanın hiçbir iradesi yoktur; rüzgâr önündeki yaprak gibidir. Ulemanın çoğunluğu bunu reddetmiştir — iradesiz birinin cezalandırılması adalete aykırıdır."],
                ["Mu'tezile (Mutlak Özgürlükçüler)", "İnsan mutlak özgürdür, kendi fiillerinin yaratıcısıdır. Ehl-i Sünnet bunu, Allah'ın Hâlık sıfatına ortak koşma riski taşıdığı gerekçesiyle reddetmiştir."],
                ["Ehl-i Sünnet / Mâtürîdiyye", "Dengeyi kurar: fiilin yaratılması (halk) Allah'a, irade edip yapması (kesb) insana aittir. İnsan, Allah'ın verdiği gücü (İstitaat) kullanarak özgürce seçer."],
            ]
        ))
        .add_callout(Callout("caution", "Sorumluluğun Engelleri: Nefis ve Şeytan",
            "İnsan iradesini kullanırken iki engelle karşılaşır: <b>Nefis</b> (fücûr-takvâ çift kutupluluğu, Şems "
            "Suresi) ve <b>Şeytan</b> — ancak Kur'an, şeytanın insan üzerinde zorlayıcı bir otoritesi (sultan) "
            "olmadığını, sadece vesvese vererek kötülüğü süslediğini vurgular."))
    )
    ch4.pages.append(
        ChapterPage(continue_tag="Örnek Metin ve Müfessir")
        .add_block(BulletBlock(2, "Örnek Tefsir Metni: M. İzzet Derveze — Bakara Suresi 6-7 Tefsiri", [
            "Bu iki ayette, Peygamber uyarsa da uyarmasa da kâfirlerin iman etmeyecekleri karara bağlanmıştır; "
            "çünkü onların kalpleri hakkı anlamaya karşı kapalıdır (mühürlüdür).",
            "Bu ayetlerin özel bir iniş sebebine rastlanmamıştır; akla ilk gelen, kâfirlerin tutumunu "
            "gerekçelendiren bir konu arası geçiş (istidrad) olarak geldiğidir — amaç, müttakilerin samimi "
            "arzusuyla kâfirlerin inatçı tutumu arasında bir karşılaştırma yapmaktır.",
            "Kâfirlerde iyi niyet ve hidayet arzusu tamamen kaybolmuştur; sanki kalpleri kilitlenmiş, kulakları "
            "tıkanmış, gözleri O'nun nurunu görmekten kör olmuştur — ve bu inatları yüzünden büyük azabı hak "
            "etmişlerdir.",
        ]))
        .add_callout(Callout("focus", "Nahiv ve Belâgat Nüktesi",
            "<b>Nahiv (Kader ve İrade Bağlamı):</b> Derveze, 'kalplerin mühürlenmesinin' Allah'ın insanı zorla "
            "kâfir yapması (Cebriyye görüşü) anlamına gelmediğini ispatlar; mühürlenme, kâfirlerin hür "
            "iradeleriyle hidayet arzusunu kaybetmelerinin doğal sonucudur. <b>Belâgat (Kinaye ve Temsil):</b> "
            "'Gözlerinde perde, kalpleri mühürlü' ibaresi fiziksel değil, inatları yüzünden hakikati algılama "
            "yetisini yitiren insanları anlatan bir Kinaye ve Temsil sanatıdır."))
        .add_person(DARWAZA)
        .add_summary("İnsan özgürlüğü Kur'an'da Hilâfet ve Emanet kavramlarıyla temellenir; Ehl-i Sünnet/"
            "Mâtürîdiyye, Cebriyye'nin cebrî ile Mu'tezile'nin mutlak özgürlükçülüğü arasında 'halk-kesb' "
            "dengesini kurar. Nefis ve şeytan, bu özgürlüğün önündeki iki temel engeldir.")
    )

    # =====================================================================
    # BÖLÜM 5 — Kur'an'da Namaz
    # =====================================================================
    ch5 = Chapter(
        number=5,
        title="Kur'an'da Namaz",
        subtitle="Evrensel bir ibadetten Mi'râc'a: namazın koruyucu işlevi ve farziyet süreci",
        key_terms=[
            KeyTerm("Salât", "Sözlükte 'dua etmek, ibadet etmek, bağışlanma dilemek'; namazın her rüknünün fiili-sözlü bir dua niteliği taşıması buradan gelir."),
            KeyTerm("Mevkût", "Vakti tayin edilmiş, zamanı Allah tarafından belirli kurallara bağlanmış farziyet."),
            KeyTerm("İkame", "Namazın şekli bir hareketten öte; eksiksiz, huşû içinde ve vaktine riayetle 'ayakta tutulması' gereken bir bilinç hali."),
            KeyTerm("Fahşâ ve Münker", "Hayasızlık ve kötülük; namazın Ankebût 45'e göre insanı alıkoyduğu iki temel kötülük türü."),
        ],
    )
    ch5.pages.append(
        ChapterPage()
        .add_terms(ch5.key_terms)
        .add_block(BulletBlock(1, "Evrensel Bir İbadet Olarak Namaz ve Farziyet Süreci", [
            "Namaz, yalnız Hz. Muhammed'in ümmetine has yeni bir yükümlülük değildir; Hz. Âdem, Nuh, İbrahim, "
            "İsmail, İsa ve Musa gibi peygamberlerin tebliğlerinde de bulunan <b>evrensel ve kadim</b> bir "
            "ibadettir. İslam öncesi Hanifler namaz kılarken, müşriklerin Kâbe etrafındaki 'salât'ı ıslık çalıp "
            "el çırpmaktan ibaret bozulmuş bir ritüeldi.",
        ]))
    )
    ch5.pages.append(
        ChapterPage(continue_tag="Ayet-i Kerîmeler")
        .add_ayat("Ayet-i Kerîmeler", [
            Ayah(
                "Ankebût 45",
                "اتْلُ مَا أُوحِيَ إِلَيْكَ مِنَ الْكِتَابِ وَأَقِمِ الصَّلَاةَ ۖ إِنَّ الصَّلَاةَ تَنْهَىٰ عَنِ الْفَحْشَاءِ وَالْمُنكَرِ ۗ وَلَذِكْرُ اللَّهِ أَكْبَرُ",
                "Kitaptan sana vahyolunanı oku ve namazı dosdoğru kıl. Şüphesiz namaz, hayâsızlıktan ve kötülükten alıkoyar. Allah'ı anmak elbette en büyük ibadettir.",
                "<b>Salât:</b> Dua etmek, ibadet etmek, bağışlanma dilemek.",
            ),
            Ayah(
                "Nisâ 103",
                "فَإِذَا قَضَيْتُمُ الصَّلَاةَ فَاذْكُرُوا اللَّهَ قِيَامًا وَقُعُودًا وَعَلَىٰ جُنُوبِكُمْ ۚ إِنَّ الصَّلَاةَ كَانَتْ عَلَى الْمُؤْمِنِينَ كِتَابًا مَّوْقُوتًا",
                "Namazı kıldığınızda, ayaktayken, otururken ve yanlarınız üzerindeyken Allah'ı anın... Şüphesiz namaz, müminler üzerine vakitleri belirlenmiş bir farzdır.",
                "<b>Mevkût:</b> Vakti tayin edilmiş, zamanı belirli kurallara bağlanmış farziyet.",
            ),
        ])
    )
    ch5.pages.append(
        ChapterPage(continue_tag="Konu Anlatımı: Namazın Evrenselliği ve İşlevi")
        .add_block(BulletBlock(2, "Namazın Farziyet Süreci", [
            "İlk dönemlerde sabah-akşam iki vakit kılınıyordu; sonra gece namazı "
            "(teheccüd) farz kılındı. Bugünkü beş vakitlik form, Hicret'ten yaklaşık 1,5 yıl önceki <b>Mi'râc</b> "
            "hadisesiyle sabit olmuştur. Kur'an'da 'ikame' kelimesiyle ifade edilen namaz, şekli bir hareketten "
            "çok, huşû içinde 'ayakta tutulması' gereken bir bilinç halidir.",
        ]))
        .add_callout(Callout("insight", "Bireysel ve Toplumsal İşlevi",
            "Namaz, mümini günde beş kez Allah'ın huzuruna çıkararak fıtratının bozulmasına engel olur. "
            "'Hayâsızlıktan ve kötülükten alıkoymayan' bir namaz sadece şeklî bir spordur. Sosyolojik açıdan "
            "cemaatle kılınan namaz; ırk, dil, renk ve makam farkı gözetmeksizin tüm müminleri aynı safta "
            "eşitleyen bir <b>toplumsal barış ve dayanışma nizamı</b> kurar."))
        .add_block(BulletBlock(3, "Örnek Tefsir Metni: el-Hâzin — Ankebût Suresi 45 Tefsiri", [
            "Kulun yerine getirmekle yükümlü olduğu ibadetler üç kısımdır: <b>Kalbî</b> (itikat/inanç), "
            "<b>Lisânî</b> (güzel zikir) ve <b>Bedenî</b> (salih amel). Kur'an okumak ve namazı ikame etmek, "
            "bedeni ve lisanı kapsar.",
            "İtikat tekrar edilmez — kişi bir şeye inandığında bu sürekli devam eder; geriye zikir ve bedenî "
            "ibadet kalır ki bunların tekrarı mümkündür. İşte bu yüzden Allah bu sürekli tekrarı emretmiştir.",
        ]))
    )
    ch5.pages.append(
        ChapterPage(continue_tag="Örnek Metnin Devamı ve Müfessir")
        .add_block(BulletBlock(3, "Örnek Tefsir Metni (devamı)", [
            "İbn Mes'ûd ve İbn Abbas demişlerdir ki: Namazın içinde Allah'a isyandan alıkoyan bir güç vardır. "
            "Kimin namazı ona iyiliği emretmez ve onu hayâsızlıktan alıkoymazsa, o namaz kişiyi Allah'tan yalnızca "
            "daha da uzaklaştırır.",
        ]))
        .add_callout(Callout("focus", "Nahiv ve Belâgat Nüktesi",
            "<b>Nahiv (İstimrâr ve Tekrâr Bağlamı):</b> İmanın ayette emredilmemesinin sebebi, itikadın kesintisiz "
            "bir süreklilik bildirip yeniden yapılamamasıdır; namaz ve okuma ise vakitlere bağlı olarak defalarca "
            "yenilenen fiillerdir. <b>Belâgat (Teşhis ve İstiare):</b> 'Namaz insanı hayâsızlıktan alıkoyar' "
            "ibaresinde namaz, insana konuşan, kötülük yapmamasını emreden manevi bir bekçi gibi kişileştirilmiştir."))
        .add_person(AL_KHAZIN)
        .add_summary("Namaz, tüm peygamberlerin tebliğinde bulunan evrensel bir ibadettir ve bugünkü beş vakitlik "
            "formuna Mi'râc ile kavuşmuştur. Kalbî-lisânî-bedenî ibadet üçlüsünün bedensel ve sözel ayağını "
            "oluşturur; hayâsızlık ve kötülükten alıkoyduğu ölçüde hem bireysel hem toplumsal anlamını bulur.")
    )

    chapters = [ch1, ch2, ch3, ch4, ch5]

    # =====================================================================
    # SÖZLÜK
    # =====================================================================
    glossary = [
        Concept("Ma'rûf", "Akıl ve dinin iyi kabul ettiği, toplumca tanıdık ve güzel karşılanan şey.", "Güzel Ahlâk", 1),
        Concept("Ahsen-i Takvim", "İnsanın en güzel kıvamda, çift kutuplu (fücûr-takvâ) fıtratla yaratılması.", "Güzel Ahlâk", 1),
        Concept("Mürüvvet", "Cahiliye Arap toplumunun kabile asabiyetine dayalı eski erdem anlayışı.", "Güzel Ahlâk", 1),
        Concept("Mu'tezile (Ahlâkta)", "Ahlâkî değerlerin objektif ve akılla bilinebilir olduğunu savunan ekol.", "Güzel Ahlâk", 1),
        Concept("Tecessüs", "İnsanların gizli hallerini kötü niyetle araştırmak.", "Yerilen Davranışlar", 2),
        Concept("Hümeze ve Lümeze", "Arkadan çekiştirme ve yüze karşı alay etme.", "Yerilen Davranışlar", 2),
        Concept("Hevâ", "Hakkı görmeyi engelleyen bencil, nefsani arzular.", "Yerilen Davranışlar", 2),
        Concept("Gıybet", "Kişiyi duyduğunda hoşlanmayacağı şekilde anmak.", "Yerilen Davranışlar", 2),
        Concept("Adl", "Denk olmak, eşitlik, ifrat-tefrit arası orta yol.", "Adalet", 3),
        Concept("Kıst", "Hakkı sahibine eksiksiz teslim etmek; hakkaniyet.", "Adalet", 3),
        Concept("Zulüm", "Bir şeyi bağlamından koparıp hakkı sahibinden esirgemek.", "Adalet", 3),
        Concept("Kozmik Adalet", "Adaletin kâinatın üzerine bina edildiği evrensel ilke olması.", "Adalet", 3),
        Concept("Hilâfet", "Allah'ın insanı yeryüzüne halife kılıp tasarruf yetkisi vermesi.", "Özgürlük ve Sorumluluk", 4),
        Concept("Emanet", "İnsanın hür iradesiyle üstlendiği, göklerin çekindiği sorumluluk.", "Özgürlük ve Sorumluluk", 4),
        Concept("İstitaat", "İnsanın eylem anında Allah'ın verdiği gücü kullanarak özgür seçim yapması.", "Özgürlük ve Sorumluluk", 4),
        Concept("Vizr", "Ağır yük, günah; suçun şahsiliği ilkesinin dayanağı.", "Özgürlük ve Sorumluluk", 4),
        Concept("Cebriyye", "İnsanın hiçbir iradesi olmadığını savunan, çoğunlukla reddedilen ekol.", "Özgürlük ve Sorumluluk", 4),
        Concept("Salât", "Dua etmek, ibadet etmek, bağışlanma dilemek.", "Namaz", 5),
        Concept("Mevkût", "Vakti Allah tarafından tayin edilmiş farziyet.", "Namaz", 5),
        Concept("İkame", "Namazın huşû içinde, eksiksiz 'ayakta tutulması' gereken bilinç hali.", "Namaz", 5),
        Concept("Fahşâ ve Münker", "Namazın alıkoyduğu hayâsızlık ve kötülük.", "Namaz", 5),
        Concept("Mi'râc", "Beş vakit namazın farz kılındığı, Hicret'ten ~1,5 yıl önceki hadise.", "Namaz", 5),
        Concept("Fücûr", "Nefse ilham edilen kötülüğe meyil; takvânın karşıtı (Şems Suresi).", "Güzel Ahlâk", 1),
        Concept("Takvâ", "Nefse ilham edilen kötülükten sakınma yeteneği; fücûrun karşıtı.", "Güzel Ahlâk", 1),
        Concept("Kesb", "Ehl-i Sünnet/Mâtürîdiyye'ye göre insanın, Allah'ın verdiği gücü kullanarak fiili irade edip yapması.", "Özgürlük ve Sorumluluk", 4),
        Concept("Keyl", "Kur'an'da adaletle birlikte anılan 'ölçü' kavramı.", "Adalet", 3),
    ]

    # =====================================================================
    # SINAV HAZIRLIK
    # =====================================================================
    distinctions = [
        DistinctionPair("Adl", "Kıst", "Adl genel bir dengeyi ifade eder; Kıst hakkı sahibine eksiksiz ve pratik olarak teslim etmeyi ifade eder."),
        DistinctionPair("Mu'tezile (Ahlâkta)", "Eş'ariyye (Ahlâkta)", "Mu'tezile ahlâkî değerleri akılla bilinebilir objektif gerçekler sayar; Eş'ariyye tek kaynağın vahiy olduğunu savunur."),
        DistinctionPair("Cebriyye", "Mu'tezile (İrade Tartışmasında)", "Cebriyye insanın hiçbir iradesi olmadığını savunur; Mu'tezile ise insanın mutlak özgür ve fiillerinin yaratıcısı olduğunu savunur."),
        DistinctionPair("Hilâfet", "Emanet", "Hilâfet Allah'ın insana yeryüzünde tasarruf yetkisi vermesidir; Emanet, göklerin çekindiği sorumluluğu insanın hür iradeyle üstlenmesidir."),
        DistinctionPair("Hümeze", "Lümeze", "Hümeze kişiyi arkasından çekiştirmek; Lümeze ise yüzüne karşı küçük düşürüp alay etmektir."),
        DistinctionPair("Tecessüs", "Tahassüs", "Tecessüs ('cim' ile) kötülükleri araştırmayı; Tahassüs ('ha' ile, Hasan-ı Basrî okuyuşu) iyilikleri araştırmayı ifade eder."),
    ]

    match_table = [
        MatchRow("Tâhir b. Âşûr", "et-Tahrîr ve't-Tenvîr — belâgat odaklı tefsir", "Kalem 4 tefsiri, 'Azîm' kelimesinde istiare analizi"),
        MatchRow("İbn Cüzey el-Kelbî", "et-Teshîl li-ʿulûmi't-tenzîl — sade, sistematik tefsir", "Hucurât 12 tefsiri, gıybetin mübalağalı teşbihi"),
        MatchRow("Ebü'l-Berekât en-Nesefî", "Medârikü't-Tenzîl — Hanefî-Mâtürîdî çizgide tefsir", "Nisâ 135 tefsiri, kıraat farkları analizi"),
        MatchRow("Muhammed İzzet Derveze", "et-Tefsîrü'l-Hadîs — Nüzul sırasına göre tefsir", "Bakara 6-7 tefsiri, kalplerin mühürlenmesi meselesi"),
        MatchRow("Ali b. Muhammed el-Hâzin", "Lübâbü't-Te'vîl — dört tefsirden derleme", "Ankebût 45 tefsiri, namazın üç ibadet türü analizi"),
    ]

    qa_items = [
        QAItem("Cahiliye döneminde ahlâkın temeli olan kavram nedir?", "Mürüvvet — kabile asabiyetine dayalı; cesaret, misafirperverlik ve intikamı kapsar."),
        QAItem("Ahsen-i Takvim ne anlama gelir?", "İnsanın hem fücûra hem takvâya meyilli, en güzel kıvamda yaratılmış çift kutuplu fıtratı."),
        QAItem("Ahlâkın kaynağı konusunda Mâtürîdiyye'nin görüşü nedir?", "Akıl değerlerin bir kısmını kavrar, ama sevap/günah hükmü için vahyin bildirimi şarttır."),
        QAItem("Hasan-ı Basrî 'tecessüs' kelimesini nasıl okumuştur?", "'Tahassüs' şeklinde — 'ha' ile iyilikleri araştırmak anlamında."),
        QAItem("Kur'an'a göre adaletin zıddı olan kavramlar nelerdir?", "Zulüm, cevr ve insafsızlık."),
        QAItem("Ef'âlü'l-ibâd tartışmasında Ehl-i Sünnet'in çözümü nedir?", "Fiilin yaratılması (halk) Allah'a, irade edip yapması (kesb) insana aittir — istitaat dengesi."),
        QAItem("Şeytanın insan üzerindeki etkisi Kur'an'da nasıl tanımlanır?", "Zorlayıcı bir otoritesi (sultan) yoktur; sadece vesvese vererek kötülüğü süsler."),
        QAItem("Namaz kaç vakit olarak ve hangi hadiseyle farz kılınmıştır?", "Beş vakit; Hicret'ten ~1,5 yıl önceki Mi'râc hadisesiyle."),
        QAItem("Kur'an'da 'ikame' kelimesiyle kastedilen nedir?", "Namazın şekli bir hareketten öte, huşû içinde 'ayakta tutulması' gereken bilinç hali."),
        QAItem("Ankebût 45'e göre namaz neyi engeller?", "Fahşâ (hayâsızlık) ve münker (kötülük)."),
    ]

    return CoursePack(
        course_code="TEFSİR",
        title='Tefsir <span class="accent-word">II</span>',
        subtitle="Kur'an'ın Ahlâk, Adalet, Özgürlük ve İbadet Eksenli Final Özeti",
        description=(
            "Kur'an'da güzel ahlâktan yerilen davranışlara, adalet tasavvurundan insan özgürlüğü ve sorumluluğuna, "
            "namazın evrensel işlevine uzanan; orijinal ayet metni, konu anlatımı, müfessir alıntısı ve biyografi "
            "eksenli final sınavı özeti."
        ),
        theme="plum",
        icon_text="K",
        chapters=chapters,
        glossary=glossary,
        distinctions=distinctions,
        match_table=match_table,
        qa_items=qa_items,
        overview_lead=(
            "Bu ders; Kur'an'ın bireysel ve toplumsal hayatı inşa eden <b>evrensel ahlâk nizamını</b>, "
            "<b>adalet tasavvurunu</b>, insanın <b>özgürlük ve sorumluluk</b> dengesini ve ibadetlerin kalbi olan "
            "<b>namazı</b> ayet, tefsir ve müfessir biyografisi eksenli olarak ele alır."
        ),
        overview_cards=[
            {"title": "Güzel Ahlâk", "text": "Mürüvvetten evrensel erdemlere; ahlâkın kaynağı tartışması."},
            {"title": "Yerilen Davranışlar", "text": "Tecessüs, gıybet, hased ve toplumsal çöküşün sebepleri."},
            {"title": "Adalet", "text": "Adl-kıst kavramları, kozmik ilke ve uygulama alanları."},
            {"title": "Özgürlük ve Sorumluluk", "text": "Hilâfet, Emanet ve ef'âlü'l-ibâd tartışması."},
            {"title": "Namaz", "text": "Evrensel ibadet, farziyet süreci ve bireysel-toplumsal işlevi."},
            {"title": "Müfessirler", "text": "Tâhir b. Âşûr, İbn Cüzey, Nesefî, Derveze, el-Hâzin biyografileri."},
        ],
        overview_flow=[
            ("Ahlâk", "Güzel / yerilen"),
            ("Adalet", "Kozmik ilke"),
            ("Özgürlük", "Hilâfet / Emanet"),
            ("İbadet", "Namaz"),
        ],
        overview_note=(
            "Sınavda en çok karıştırılan yer, <b>mezhep tartışmalarının hangi konuya ait olduğudur:</b> "
            "Mu'tezile/Eş'ariyye/Mâtürîdiyye ayrımı <u>ahlâkın kaynağı</u> tartışmasına, Cebriyye/Mu'tezile/"
            "Ehl-i Sünnet ayrımı ise <u>fiillerin yaratıcısı (ef'âlü'l-ibâd)</u> tartışmasına aittir."
        ),
    )
