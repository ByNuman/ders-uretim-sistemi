# -*- coding: utf-8 -*-
"""TEFSİR II — Görsel Ders Notu Kitabı, içerik tanımı.
Kaynak: 'kaynaklar/ders_ozetleri/TEFSİR 2_FİNAL ÖZET.pdf' (ham metin özet, 17 sayfa, 5 bölüm).

TEKNİK NOT (Arapça desteği): Hem ayetlerin hem de MÜFESSİR ALINTILARININ
orijinal Arapça metni eklenmiştir; DejaVu Sans'ın Chromium'daki native
shaping'i (HarfBuzz) ile harfler doğru bitişir.

Müfessir alıntıları şu şekilde kurtarıldı (kaynak PDF'in metin katmanı
sorunluydu):
  * pdfplumber bu PDF'te Arapçayı harf harf TERS çıkarıyor — kullanılamaz.
    PyMuPDF (`page.get_text("text")`) ise 1-4. bölümlerin alıntılarını
    DOĞRU mantıksal sırada veriyor. Doğrulama çapası: Nesefî alıntısındaki
    ayet parçaları bilinen Mushaf metniyle birebir örtüştü.
  * Kaynak fontun ToUnicode eşlemesi bazı bağları bozuyor; şu onarımlar
    yapıldı: "هللا"→"الله", "اْل"→"الأ", "اإل"→"الإ", "اال"→"الا",
    fatha-lam bağı → "لا".
  * 5. bölüm (el-Hâzin) sayfası ayrıca satır içi DÖNDÜRÜLMÜŞ (rotated)
    çıkıyordu: cümle parçaları kaydırılmıştı. Doğru sıra, ﴿﴾ parantez
    dengesi + kaynaktaki Türkçe çeviri karşılaştırmasıyla geri kuruldu.
Her alıntı, üretilen PDF üzerinde görsel olarak okunup doğrulanmıştır.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from content_model import (
    Person, KeyTerm, Callout, FlowStep, FlowDiagram, ComparisonTable,
    InfoCard, BulletBlock, Chapter, ChapterPage, Concept, CoursePack,
    Ayah, TestQuestion, AnswerItem,
)

# ---------------------------------------------------------------------------
# MÜFESSİRLER (TEK KAYNAK) — tarihler/eserler yalnızca burada tanımlanır
# ---------------------------------------------------------------------------

TAHIR_IBN_ASHUR = Person(
    id="tahir", name="Tâhir b. Âşûr", years="1879–1973",
    tagline="et-Tahrîr ve't-Tenvîr Müellifi",
    bio=["Tunus'ta doğmuş, Fas asıllı köklü bir aileye mensuptur. Meşhur <b>Zeytûne Üniversitesi</b>'nde "
         "rektörlük yapmış; fizik ve matematik gibi modern fen bilimlerinin ilahiyat müfredatına girmesi için "
         "cesur bir mücadele vermiştir. Yalnız müfessir değil, aynı zamanda ufuk açıcı bir İslam hukukçusu ve "
         "dil bilimcidir; Tunus'un bağımsızlık mücadelesinde aktif rol almıştır."],
    key_work="et-Tahrîr ve't-Tenvîr", initials="İA",
)
IBN_JUZAYY = Person(
    id="ibn_cuzey", name="İbn Cüzey el-Kelbî", years="1294–1340",
    tagline="et-Teshîl li-'ulûmi't-tenzîl Müellifi",
    bio=["Endülüs'ün ilim merkezi <b>Gırnata</b>'da doğmuş, Yemen asıllı Benî Kelb kabilesine mensuptur. Genç "
         "yaşta Gırnata Ulucamii'nde imam-hatiplik yapmış; 741/1340'ta İspanyol ve Portekiz kuvvetlerine karşı "
         "Cebelitarık yakınlarındaki <b>Tarîf Savaşı</b>'nda şehit düşmüştür. Sahih hadisleri merkeze alıp "
         "İsrailiyat'a temkinli yaklaşan, sade ve sistematik bir üslup benimsemiştir."],
    key_work="et-Teshîl li-'ulûmi't-tenzîl", initials="İC",
)
NASAFI = Person(
    id="nesefi", name="Ebü'l-Berekât en-Nesefî", years="1223–1310",
    tagline="Medârikü't-Tenzîl (Nesefî Tefsiri) Müellifi",
    bio=["Buhara yakınlarındaki <b>Nesef</b> şehrinde doğmuş, Moğol istilalarının şehirleri harabeye çevirdiği "
         "buhranlı bir dönemde ilmî faaliyetini sürdürmüştür. Moğol yağması üzerine Kirman'a göç edip "
         "Kutbiyye-Sultâniyye Medresesi'nde uzun yıllar ders vermiş, memleketine dönerken Hûzistan'da vefat "
         "etmiştir. <b>Hanefî fıkhının ve Mâtürîdî itikadının</b> kilit isimlerindendir."],
    key_work="Medârikü't-Tenzîl ve Hakâiku't-Te'vîl", initials="N",
)
DARWAZA = Person(
    id="derveze", name="Muhammed İzzet Derveze", years="1888–1984",
    tagline="et-Tefsîrü'l-Hadîs Müellifi — Nüzul Sırasına Göre Tefsir",
    bio=["Filistin'in <b>Nablus</b> şehrinde doğmuş, Şam'da vefat etmiştir. 20. yüzyılın en önemli aksiyoner "
         "âlimlerinden biridir; hayatı boyunca Filistin davasına bağlı kalmış, siyasi mücadele ile ilmî "
         "faaliyeti aynı potada birleştirmiştir. Klasik sıralamadan ayrılıp Kur'an'ı <b>nüzul sırasına göre</b> "
         "tefsir ederek ayetlerin tarihsel bağlamını öne çıkarmıştır."],
    key_work="et-Tefsîrü'l-Hadîs", initials="İD",
)
AL_KHAZIN = Person(
    id="hazin", name="Ali b. Muhammed el-Hâzin", years="1279–1341",
    tagline="Lübâbü't-Te'vîl (Hâzin Tefsiri) Müellifi",
    bio=["Bağdat'ta doğmuş; Dımaşk'taki <b>Sümeysâtiyye Kütüphanesi</b>'nin yöneticiliğini (hâzinliğini) yaptığı "
         "için 'el-Hâzin' lakabıyla anılmıştır. Kaynaklara sınırsız erişimi onu ansiklopedik bir derlemeci "
         "yapmış; ayetlerin edebî, dilsel, şer'î ve ahlâkî yönlerini harmanlamıştır. Ancak İsrâiliyat'a ve "
         "tarihî kıssalara fazla yer verdiği için ciddi eleştirilere maruz kalmıştır."],
    key_work="Lübâbü't-Te'vîl fî Me'âni't-Tenzîl", initials="H",
)


def get_pack() -> CoursePack:

    # =====================================================================
    # BÖLÜM 1 — Kur'ân'da Güzel Ahlâk
    # =====================================================================
    ch1 = Chapter(
        number=1,
        title="Kur'ân'da Güzel Ahlâk",
        subtitle="Cahiliye mürüvvetinden evrensel erdemler sistemine: ahlâkın Kur'ânî temelleri",
        key_terms=[
            KeyTerm("Ma'rûf", "Akıl ve dinin iyi kabul ettiği, toplumun ortak vicdanında 'tanıdık' ve güzel karşılanan her şey."),
            KeyTerm("Mürüvvet", "Cahiliye Arap toplumunda kabile asabiyetine dayalı; cesaret, misafirperverlik ve intikamı kapsayan eski erdem anlayışı."),
            KeyTerm("Ahsen-i Takvim", "İnsanın 'en güzel kıvamda' yaratılması; ancak hem fücûra hem takvâya meyilli çift kutuplu fıtratla donatılması."),
            KeyTerm("Huluk", "Nefsin kalıcı tabiatları/huyları; tek başına kullanıldığında çoğunlukla iyi tabiat ve erdemleri ifade eder."),
        ],
    )
    ch1.pages.append(
        ChapterPage()
        .add_terms(ch1.key_terms)
        .add_ayat("Ayet-i Kerîmeler", [
            Ayah(
                "Lokmân 17 — Sosyal İlişkilerin Temeli",
                "يَا بُنَيَّ أَقِمِ الصَّلَاةَ وَأْمُرْ بِالْمَعْرُوفِ وَانْهَ عَنِ الْمُنكَرِ وَاصْبِرْ عَلَىٰ مَا أَصَابَكَ ۖ إِنَّ ذَٰلِكَ مِنْ عَزْمِ الْأُمُورِ",
                "Yavrum! Namazı dosdoğru kıl, iyiliği emret, kötülükten sakındır. Başına gelen musibetlere karşı sabırlı ol. Şüphesiz bunlar, azmedilmeye değer (kararlılık gerektiren) işlerdendir.",
                "<b>Ma'rûf:</b> Akıl ve dinin iyi kabul ettiği, toplumun ortak vicdanında 'tanıdık' ve güzel karşılanan her şey.",
            ),
        ])
        .add_ayat(None, [
            Ayah(
                "Furkân 63 — Tevazu ve Vakâr",
                "وَعِبَادُ الرَّحْمَٰنِ الَّذِينَ يَمْشُونَ عَلَى الْأَرْضِ هَوْنًا وَإِذَا خَاطَبَهُمُ الْجَاهِلُونَ قَالُوا سَلَامًا",
                "Rahmân'ın (has) kulları, yeryüzünde tevazu ve vakâr ile yürüyen kimselerdir. Cahiller onlara laf attığında 'Selâm!' derler.",
                "<b>Hevnen:</b> Kendini beğenmişlikten uzak, ağırbaşlı, vakar sahibi ve mütevazı bir duruş.",
            ),
            Ayah(
                "Kalem 4 — Ahlâkın Özeti ve Zirvesi",
                "وَإِنَّكَ لَعَلَىٰ خُلُقٍ عَظِيمٍ",
                "Ve şüphesiz sen yüce bir ahlâk üzeresin.",
                "<b>Azîm:</b> Kadri, kıymeti ve etkisi çok büyük; takdir edilemeyecek kadar yüce olan.",
            ),
        ])
    )
    ch1.pages.append(
        ChapterPage()
        .add_block(BulletBlock(1, "Cahiliyeden İslam'a Ahlâkî Dönüşüm", [
            "İslam öncesi Arap toplumunda ahlâk, kabile asabiyetine (ırkçılığına) ve bedevî yaşam tarzına dayalı "
            "<b>'Mürüvvet'</b> kavramıyla ifade edilirdi. Mürüvvet; cesaret, misafirperverlik ve intikam gibi "
            "erdemleri kapsardı — ancak bunun temeli <b>kabile gururuydu</b>. İslam bu kabileci kalıbı kırarak "
            "ahlâkı; temeli <b>'Allah korkusu ve rızası'</b> olan, kibre değil tevazuya dayanan <b>evrensel bir "
            "erdemler sistemine</b> dönüştürmüştür.",
            "<b>İnsanın Ahlâkî Fıtratı (Çift Kutupluluk):</b> Kur'an insanı en güzel kıvamda (Ahsen-i Takvim) "
            "yaratılmış olarak tanımlar; ancak ona hem kötülüğe meyil (<b>Fücûr</b>) hem de ondan sakınma "
            "yeteneği (<b>Takvâ</b>) ilham edilmiştir. Ahlâk, bu iki güç arasındaki <b>iradî bir tercihtir</b>: "
            "nefsini arındıran kurtuluşa erer, fücura daldıran ise ahlâken <b>'Esfel-i Sâfilîn'e</b> (aşağıların "
            "aşağısına) yuvarlanır.",
        ]))
        .add_table(ComparisonTable(
            "Değerlerin Kaynağı Tartışması (Sınavlık Mezhep Ayrımı)",
            ["Ekol", "Ahlâkî değerlerin kaynağı hakkındaki görüşü"],
            [
                ["Mu'tezile <br>(Akılcılar)", "Ahlâkî değerler <b>objektiftir</b> ve akılla bilinebilir. İyi ve kötü nesnelerin kendi özünde vardır; akıl, vahiy olmasa bile neyin iyi neyin kötü olduğunu bulabilir."],
                ["Eş'ariyye <br>(Vahiyciler)", "Ahlâkın <b>tek kaynağı vahiydir</b>. Bir şeyin özünde iyilik veya kötülük yoktur; Allah emrettiği için o şey 'iyi', yasakladığı için 'kötü'dür."],
                ["Mâtürîdiyye <br>(Sentezciler)", "İnsan aklı değerlerin bir kısmını kavrayabilir; ancak bir eylemin <b>'sevap' veya 'günah'</b> olması için vahyin bildirimi şarttır. Allah'ın yaratması hikmetin dışına çıkmaz."],
            ]
        ))
        .add_callout(Callout("insight", "Kritik Çıkarım: Ahlâk–İbadet Bütünlüğü",
            "İslam'da ahlâk, ibadetten bağımsız düşünülemez. Kur'an'a göre namaz insanı <b>'fahşâ ve "
            "münkerden'</b> (hayasızlık ve kötülükten) alıkoyan bir eylemdir; ibadet, ahlâkı güzelleştirdiği "
            "ölçüde gerçek amacına ulaşır. İslâm ahlâkının en yüksek gayesi faydacı bir beklenti değil, "
            "<b>Allah'ın hoşnutluğunu</b> kazanmaktır."))
        .add_ayat("Örnek Metin — Tâhir b. Âşûr, Kalem Suresi 4 Tefsiri (et-Tahrîr ve't-Tenvîr)", [
            Ayah(
                "1 — Ayetin Siyakı: Düşmanın İftirasının Çürütülmesi",
                "وَبَعْدَ أَنْ أَنَسَ نَفْسَ رَسُولِهِ بِالْوَعْدِ عَادَ إِلَى تَسْفِيهِ قَوْلِ الْأَعْدَاءِ فَحَقَّقَ أَنَّهُ مُتَلَبِّسٌ بِخُلُقٍ عَظِيمٍ وَذَلِكَ ضِدُّ الْجُنُونِ",
                "(Allah), elçisinin nefsini mükâfat vaadiyle teskin edip rahatlattıktan sonra, düşmanların (ona mecnun/deli demeleri gibi) beyhude sözlerini çürütmeye döndü. Ve onun yüce bir ahlâka büründüğünü ispat etti; ki bu durum deliliğin tam zıddıdır.",
                "",
            ),
        ])
    )
    ch1.pages.append(
        ChapterPage()
        .add_ayat("Örnek Metin (devamı) — Tâhir b. Âşûr, Kalem 4 Tefsiri", [
            Ayah(
                "2 — 'Huluk' Kelimesinin Tahlili",
                "وَالْخُلُقُ طِبَاعُ النَّفْسِ، وَأَكْثَرُ إِطْلَاقِهِ عَلَى طِبَاعِ الْخَيْرِ إِذَا لَمْ يُتْبَعْ بِنَعْتٍ",
                "Huluk (ahlâk), nefsin kalıcı tabiatları/huylarıdır. Eğer ardından bir sıfat gelmezse (mutlak olarak kullanılırsa), çoğu zaman iyi tabiatlar ve erdemler için kullanılır.",
                "",
            ),
            Ayah(
                "3 — 'Azîm' Kelimesi: İstiareden Hakikate",
                "وَالْعَظِيمُ الرَّفِيعُ الْقَدْرِ وَهُوَ مُسْتَعَارٌ مِنْ ضَخَامَةِ الْجِسْمِ، وَشَاعَتْ هَذِهِ الِاسْتِعَارَةُ حَتَّى سَاوَتِ الْحَقِيقَةَ",
                "'Azîm' kelimesi, kadri ve kıymeti pek yüksek olan demektir. Bu kelime aslında cisimlerin iriliğinden (fiziksel büyüklükten) ödünç alınmış bir mecazdır; ancak bu kullanım o kadar yaygınlaşmıştır ki artık hakikat seviyesine ulaşmıştır.",
                "",
            ),
            Ayah(
                "4 — 'Alâ' Edatı ve Temekkün",
                "وَ(عَلَى) لِلِاسْتِعْلَاءِ الْمَجَازِيِّ الْمُرَادُ بِهِ التَّمَكُّنُ كَقَوْلِهِ: (أُولَئِكَ عَلَى هُدًى مِنْ رَبِّهِمْ)",
                "'Alâ' edatı, mecazî bir üstünlük (isti'lâ) ifade eder. Bununla kastedilen 'temekkün'dür (o ahlâka sarsılmaz şekilde yerleşmiş, hâkim olmaktır). Tıpkı 'Onlar Rablerinden bir hidayet üzeredirler' ayetinde olduğu gibi.",
                "",
            ),
        ])
        .add_ayat(None, [
            Ayah(
                "5 — En Kapsamlı Tefsir: Hz. Âişe'nin Cevabı",
                "وَلَمَّا كَانَ هَذَا الْخُلُقُ الْعَظِيمُ قَدْ جَمَعَ مَكَارِمَ الْأَخْلَاقِ كُلَّهَا، كَانَ تَفْسِيرُهُ الْجَامِعُ هُوَ مَا رَوَتْهُ عَائِشَةُ رَضِيَ اللَّهُ عَنْهَا لَمَّا سُئِلَتْ عَنْ خُلُقِهِ ﷺ فَقَالَتْ: «كَانَ خُلُقُهُ الْقُرْآنَ»",
                "Bu 'yüce ahlâk', ahlâkî erdemlerin tamamını kendisinde topladığı için, onun en kapsamlı (câmi) tefsiri, Hz. Âişe'nin (r.a.) kendisinden Hz. Peygamber'in (s.a.v.) ahlâkı sorulduğunda verdiği şu cevap olmuştur: «Onun ahlâkı Kur'an idi.»",
                "",
            ),
            Ayah(
                "6 — Şeriatın Gayesi: Bu Ahlâkla Ahlâklanmak",
                "فَكَمَا جَعَلَ اللَّهُ رَسُولَهُ عَلَى خُلُقٍ عَظِيمٍ جَعَلَ شَرِيعَتَهُ لِحَمْلِ النَّاسِ عَلَى التَّخَلُّقِ بِالْخُلُقِ الْعَظِيمِ بِمُنْتَهَى الِاسْتِطَاعَةِ",
                "Tıpkı Allah'ın kendi resulünü yüce bir ahlâk üzere kıldığı gibi, O'nun şeriatını da insanları güçleri yettiği son noktaya kadar bu yüce ahlâkla ahlâklanmaya sevk etmek için kılmıştır.",
                "",
            ),
        ])
    )
    ch1.pages.append(
        ChapterPage()
        .add_callout(Callout("focus", "Akademik Nahiv ve Belâgat Nüktesi",
            "<b>Nahiv (Temekkün / Harf-i Cer Analizi):</b> Tâhir b. Âşûr, <b>'Alâ'</b> edatının sıradan bir "
            "'üzerinde olma' bildirmediğini açıklar. Bu edat, atın sırtına sağlamca oturan bir binici gibi, Hz. "
            "Peygamber'in de o yüce ahlâka bütünüyle hâkim olduğunu ve o ahlâkın onun ayrılmaz bir parçası "
            "haline geldiğini <b>gramer yoluyla</b> ispatlar.<br><br>"
            "<b>Belâgat (İstiare):</b> 'Azîm' kelimesinin, dağ gibi maddi varlıkların gözle görülen "
            "büyüklüğünden alınarak soyut bir karakter yüceliği için kullanılması güçlü bir <b>İstiare</b> "
            "sanatıdır; manevi büyüklük, maddi büyüklük üzerinden somutlaştırılarak zihne kazınmıştır."))
        .add_person(TAHIR_IBN_ASHUR)
        .add_info_cards("Tâhir b. Âşûr'un Tefsir Metodu ve Eserleri", [
            InfoCard("Metodu", "Ayetlerin edebî ve belâgat yönlerini eşsiz bir titizlikle inceler; Kur'an'ın her "
                     "çağın anlayışına hitap eden evrensel bir metin olduğunu savunarak <b>ilmî tefsiri</b> "
                     "benimsemiş, İsrailiyat'ı reddedip akıl ve nakli dengeli birleştirmiştir.", "Metot"),
            InfoCard("et-Tahrîr ve't-Tenvîr", "Kur'an'ı dilsel, edebî, tarihsel ve fıkhî boyutlarıyla ele alan "
                     "kapsamlı şaheseri. <b>İşlenen örnek metin buradan alınmıştır.</b>", "Tefsir"),
            InfoCard("Makâsıdü'ş-şerî'ati'l-İslâmiyye", "Şeriatın temel gayelerini sistemleştiren, modern fıkıh "
                     "düşüncesine yön veren başyapıtı.", "Usul"),
        ])
        .add_summary("Kur'an'da güzel ahlâk, cahiliyenin kabileci mürüvvet anlayışını aşan evrensel bir erdemler "
            "sistemidir ve insanın fücûr–takvâ arasındaki iradî tercihine dayanır. Değerlerin kaynağı konusunda "
            "Mu'tezile aklı, Eş'ariyye vahyi, Mâtürîdiyye ise ikisinin dengesini esas alır; Kalem 4'te "
            "Peygamber'e nispet edilen 'huluk-ı azîm' ise Hz. Âişe'nin ifadesiyle 'Kur'an ahlâkı'nın ta kendisidir.")
    )

    # =====================================================================
    # BÖLÜM 2 — Kur'ân'da Yerilen Olumsuz Davranışlar
    # =====================================================================
    ch2 = Chapter(
        number=2,
        title="Kur'ân'da Yerilen Olumsuz Davranışlar",
        subtitle="Tecessüsten gıybete: toplumsal dokuyu tahrip eden davranışların kavramsal haritası",
        key_terms=[
            KeyTerm("Tecessüs", "İnsanların gizli hallerini, ayıp ve kusurlarını kötü niyetle araştırmak, casusluk yapmak."),
            KeyTerm("Hümeze / Lümeze", "Hümeze arkadan çekiştirmek, kaş-göz işaretiyle ayıplamak; lümeze yüze karşı küçük düşürüp alay etmek."),
            KeyTerm("Hevâ", "Bencil ve nefsanî arzular; hakkı görmeyi engelleyen, insanı adaletten saptıran zifiri bir perde."),
            KeyTerm("Gıybet", "Bir kimseden, duyduğunda hoşlanmayacağı şekilde bahsetmek; 'ölü kardeşinin etini yemek' teşbihiyle kınanır."),
        ],
    )
    ch2.pages.append(
        ChapterPage()
        .add_terms(ch2.key_terms)
        .add_ayat("Ayet-i Kerîmeler", [
            Ayah(
                "Hucurât 12 — Toplumsal Mahremiyetin İhlali",
                "يَا أَيُّهَا الَّذِينَ آمَنُوا اجْتَنِبُوا كَثِيرًا مِنَ الظَّنِّ إِنَّ بَعْضَ الظَّنِّ إِثْمٌ ۖ وَلَا تَجَسَّسُوا وَلَا يَغْتَب بَّعْضُكُم بَعْضًا ۚ أَيُحِبُّ أَحَدُكُمْ أَن يَأْكُلَ لَحْمَ أَخِيهِ مَيْتًا فَكَرِهْتُمُوهُ",
                "Ey iman edenler! Zannın birçoğundan sakının. Çünkü bazı zanlar günahtır. Birbirinizin gizli hallerini (kusurlarını) araştırmayın ve biriniz diğerinizi gıybet etmesin. Sizden biri, ölü kardeşinin etini yemekten hoşlanır mı? İşte bundan iğrendiniz.",
                "<b>Tecessüs:</b> İnsanların gizli hallerini, ayıp ve kusurlarını kötü niyetle araştırmak, casusluk yapmak. İslâm ahlâkı tecessüsü, sosyal barışı zehirleyen bir hastalık olarak reddeder.",
            ),
        ])
        .add_ayat(None, [
            Ayah(
                "Hümeze 1-3 — Mal Hırsı ve Alaycılık",
                "وَيْلٌ لِّكُلِّ هُمَزَةٍ لُّمَزَةٍ الَّذِي جَمَعَ مَالًا وَعَدَّدَهُ يَحْسَبُ أَنَّ مَالَهُ أَخْلَدَهُ",
                "Arkadan çekiştirmeyi (hümeze), yüze karşı alay etmeyi (lümeze) âdet edinen herkesin vay haline! O ki, mal toplamış ve onu tekrar tekrar saymıştır. Malının kendisini ebedî kılacağını zanneder.",
                "<b>Hümeze ve Lümeze:</b> Hümeze, birini arkasından çekiştirmek ve kaş-göz işaretiyle ayıplamak; lümeze ise kişinin yüzüne karşı onu küçük düşürmek ve alay etmektir.",
            ),
        ])
    )
    ch2.pages.append(
        ChapterPage()
        .add_block(BulletBlock(1, "Kötü Ahlâkın Kavramsal Ağı ve Hevâ Engeli", [
            "Kur'an-ı Kerîm, yerilen olumsuz davranışları ifade etmek için çok geniş bir kavramsal yapı kullanır: "
            "günah (<b>ism</b>), sapıklık (<b>dalâl</b>), hayasızlık (<b>fahşâ</b>), haddi aşma/zulüm "
            "(<b>bağy</b>), kötü iş (<b>seyyie</b>), yoldan çıkma (<b>fısk</b>) ve günahkârlık (<b>fücûr</b>). "
            "İslâmî kaynaklarda bu huylar genel olarak <b>'sûü'l-huluk'</b>, <b>'el-ahlâku'z-zemîme'</b> veya "
            "<b>'el-ahlâku's-seyyie'</b> terimleriyle adlandırılır.",
            "<b>Çift Kutupluluk:</b> Şems Suresi'nde vurgulandığı üzere Allah, insan nefsine hem kötülüğün "
            "kaynağı olan fücûru hem de ondan korunma yeteneği olan takvâyı ilham etmiştir.",
            "<b>Hevâ Engeli:</b> Ahlâkî çöküşe sebep olan en büyük engel Hevâ'dır (bencil ve nefsanî arzular). "
            "Kur'an, kötü arzularının esiri olan insanı <b>'hevâsını ilah edinen'</b> kişi olarak nitelendirir; "
            "zira hevâ, hakkı görmeyi engelleyen ve insanı adaletten saptıran zifiri bir perdedir.",
        ]))
        .add_table(ComparisonTable(
            "Toplumsal Çöküşün Sebepleri — Kur'an'da Yerilen Temel Davranışlar",
            ["Davranış", "Kur'ânî Değerlendirme"],
            [
                ["Haksızlık ve Zulüm", "Kabile gururu veya şahsi menfaat için başkasının hakkını gasp etmek; Kur'an'ın cahiliye toplumunda <b>en çok eleştirdiği</b> husustur."],
                ["Cimrilik (İsârın Terki)", "Muhtaçlara yardım etmemek ve el açıp isteyeni azarlamak, <b>merhamet eksikliğinin</b> nişanesidir."],
                ["Kibir ve Serkeşlik", "Kendini üstün görmek ve asaletle övünmek; takvânın tam zıddı olan <b>Câhiliye hamiyyesi</b> (tutuculuğu) olarak yerilir."],
                ["Haset ve Gıybet", "Haset, doğrudan Allah'a sığınılması gereken karanlık bir duygudur; gıybet ise <b>'ölmüş kardeşinin etini yemek'</b> teşbihiyle kınanır."],
            ]
        ))
        .add_ayat("Örnek Metin — İbn Cüzey, Hucurât 12 Tefsiri (et-Teshîl li-ulûmi't-tenzîl)", [
            Ayah(
                "1 — Suizân ve Hüsnüzan Ayrımı",
                "اجْتَنِبُوا كَثِيرًا مِنَ الظَّنِّ: يَعْنِي ظَنَّ السُّوءِ بِالْمُسْلِمِينَ، وَأَمَّا ظَنُّ الْخَيْرِ فَهُوَ حَسَنٌ",
                "'Zannın birçoğundan sakının' ayeti; Müslümanlar hakkında kötü zan (suizân) beslemeyi ifade eder. Hayır (iyi) zan beslemeye (hüsnüzan) gelince, o güzel bir davranıştır.",
                "",
            ),
            Ayah(
                "2 — 'İsm' (Günah) Kelimesinin Manası",
                "إِنَّ بَعْضَ الظَّنِّ إِثْمٌ: قِيلَ: فِي مَعْنَى الْإِثْمِ هُنَا الْكَذِبُ لِقَوْلِهِ: «الظَّنُّ أَكْذَبُ الْحَدِيثِ» لِأَنَّهُ قَدْ لَا يَكُونُ مُطَابِقًا لِلْأَمْرِ",
                "'Çünkü bazı zanlar günahtır.' Denildi ki: Buradaki günah (ism) manası 'yalan' demektir. Zira Hz. Peygamber (s.a.v.) «Zandan sakının; çünkü zan, sözlerin en yalanıdır» buyurmuştur. Çünkü zan her zaman gerçeğe uygun düşmeyebilir.",
                "",
            ),
        ])
    )
    ch2.pages.append(
        ChapterPage()
        .add_ayat("Örnek Metin (devamı) — İbn Cüzey, Hucurât 12 Tefsiri", [
            Ayah(
                "3 — Zannın Ne Zaman Günah Olduğu",
                "وَقِيلَ: إِنَّمَا يَكُونُ إِثْمًا إِذَا تَكَلَّمَ بِهِ، وَأَمَّا إِذَا لَمْ يَتَكَلَّمْ بِهِ فَهُوَ فِي فُسْحَةٍ لِأَنَّهُ لَا يَقْدِرُ عَلَى دَفْعِ الْخَوَاطِرِ",
                "Şöyle de denilmiştir: Zan ancak kişinin bunu dillendirmesi (konuşması) halinde günah olur. Eğer konuşmazsa kişi için bir genişlik (ruhsat) vardır; zira insan kalbine gelen düşünceleri (havâtır) defetmeye güç yetiremez.",
                "",
            ),
            Ayah(
                "4 — Tecessüs / Tahassüs Kıraat Farkı",
                "وَلَا تَجَسَّسُوا: أَيْ لَا تَبْحَثُوا عَنْ مَخْبَآتِ النَّاسِ... وَقَرَأَ الْحَسَنُ «تَحَسَّسُوا» بِالْحَاءِ، وَالتَّجَسُّسُ بِالْجِيمِ فِي الشَّرِّ وَبِالْحَاءِ فِي الْخَيْرِ",
                "'Birbirinizin gizli hallerini araştırmayın (tecessüs etmeyin).' Yani insanların gizli hallerini ve ayıplarını araştırmayın... Hasan-ı Basrî bu kelimeyi 'ha' harfiyle «tahassüs» şeklinde okumuştur. 'Cim' ile tecessüs kötülükleri araştırmak, 'ha' ile tahassüs ise iyilikleri araştırmaktır.",
                "",
            ),
            Ayah(
                "5 — Gıybetin Tanımı",
                "وَلَا يَغْتَبْ بَعْضُكُمْ بَعْضًا: الْمَعْنَى: لَا يَذْكُرُ أَحَدُكُمْ مِنْ أَخِيهِ الْمُسْلِمِ مَا يَكْرَهُ لَوْ سَمِعَهُ، وَالْغِيبَةُ هِيَ مَا يَكْرَهُ الْإِنْسَانُ ذِكْرَهُ مِنْ خَلْقِهِ أَوْ خُلُقِهِ أَوْ دِينِهِ أَوْ أَفْعَالِهِ",
                "'Biriniz diğerinizi gıybet etmesin.' Anlamı şudur: Hiçbiriniz Müslüman kardeşinden, onun duyduğunda hoşlanmayacağı bir şekilde bahsetmesin. Gıybet; insanın yaratılışıyla (fiziksel), ahlakıyla, diniyle veya eylemleriyle anılmasından hoşlanmadığı şeydir.",
                "",
            ),
        ])
        .add_ayat(None, [
            Ayah(
                "6 — 'Ölü Kardeş Eti' Teşbihi",
                "أَيُحِبُّ أَحَدُكُمْ أَنْ يَأْكُلَ لَحْمَ أَخِيهِ مَيْتًا فَكَرِهْتُمُوهُ: شَبَّهَ اللَّهُ الْغِيبَةَ بِأَكْلِ لَحْمِ ابْنِ آدَمَ مَيْتًا، وَالْعَرَبُ تُشَبِّهُ الْغِيبَةَ بِأَكْلِ اللَّحْمِ، ثُمَّ زَادَ فِي تَقْبِيحِهِ أَنْ جَعَلَهُ مَيْتًا لِأَنَّ الْجِيفَةَ مُسْتَقْذَرَةٌ",
                "'Sizden biri, ölü kardeşinin etini yemekten hoşlanır mı? İşte bundan iğrendiniz.' Allah, gıybeti insanoğlunun etini ölü iken yemeye benzetmiştir. Zaten Araplar da gıybeti et yemeye benzetirlerdi. Sonra, leş (cîfe) iğrenç bir şey olduğu için onu 'ölü' yaparak bu çirkinliği daha da artırmıştır.",
                "",
            ),
        ])
    )
    ch2.pages.append(
        ChapterPage()
        .add_callout(Callout("focus", "Akademik Nahiv ve Belâgat Nüktesi",
            "<b>Nahiv (Hâl ve Kıraat):</b> Ayette geçen <b>'meyten' (ölü)</b> kelimesi irab bakımından "
            "<b>Hâl</b>'dir (durum zarfı) — yani 'Kardeşinin etini <u>ölü olduğu halde</u> yeme' demektir. "
            "Ayrıca Nâfi' bu kelimeyi şeddeli olarak <b>'meyyiten'</b> okumuştur.<br><br>"
            "<b>Belâgat (Mübalağa ve Temsilî Teşbih):</b> Zemahşerî'nin tespit ettiği üzere gıybetin çirkinliği "
            "katman katman artırılmıştır: <b>Et yemek → İnsan eti yemek → Ölü insan eti yemek → Kendi ölü "
            "kardeşinin etini yemek!</b> Ayrıca en iğrenç şey sorulurken <b>'Sever misiniz?'</b> fiilinin "
            "kullanılması muazzam bir <b>Tezat Sanatı (İstifhâm-ı İnkârî)</b>dır."))
        .add_person(IBN_JUZAYY)
        .add_info_cards("İbn Cüzey el-Kelbî'nin Eserleri", [
            InfoCard("et-Teshîl li-'ulûmi't-tenzîl", "Kur'an ilimlerini sadeleştiren şaheseri. <b>İşlenen örnek "
                     "metin buradan alınmıştır.</b>", "Tefsir"),
            InfoCard("el-Kavânînü'l-fıkhıyye", "Sadece kendi mezhebini değil, <b>dört Sünnî mezhebin</b> ve diğer "
                     "müçtehitlerin görüşlerini içeren mukayeseli fıkıh kitabı.", "Fıkıh"),
            InfoCard("Takrîbü'l-vüsûl", "Fıkıh usulüne dair eseri; ayrıca hadis alanında "
                     "<b>el-Envârü's-seniyye fi'l-kelimâti's-sünniyye</b> adlı çalışması vardır.", "Usul"),
        ])
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "İslam'da ahlâkî terakki (yükseliş), olumsuz davranışlardan tam manasıyla <b>hicret etmekle</b> "
            "başlar. İnsanın iyilik yaptığında sevinç, kötülük yaptığında ise vicdanen rahatsızlık duyabilmesi, "
            "<b>kâmil imanın en temel göstergesi</b> kabul edilmektedir."))
        .add_callout(Callout("route", "Müfessirin Mirası",
            "İbn Cüzey el-Kelbî, hayatıyla <b>'ilmiyle âmil olmak'</b> kavramının canlı bir tablosunu çizmiştir. "
            "İlmî mirası sadece Endülüs ile sınırlı kalmamış; mukayeseli metodolojisi ve duru üslubu sayesinde "
            "tüm İslam coğrafyasında asırlar boyu başucu kaynağı olarak kullanılmıştır."))
        .add_summary("Kur'an'ın yerdiği davranışlar bireysel bir günahtan öte, toplumun sosyal dokusunu tahrip "
            "eden birer virüs olarak ele alınır. Zan, tecessüs, gıybet, haset, kibir ve cimrilik bu ağın temel "
            "halkalarıdır; Hucurât 12, gıybeti katmanlı bir mübalağayla en iğrenç fiile benzeterek toplumsal "
            "mahremiyeti Kur'ânî bir güvence altına alır.")
    )

    # =====================================================================
    # BÖLÜM 3 — Kur'ân'da Adalet
    # =====================================================================
    ch3 = Chapter(
        number=3,
        title="Kur'ân'da Adalet",
        subtitle="Şahitlikten savaşa, kozmik bir ilkeden vicdanî eğitime uzanan adalet tasavvuru",
        key_terms=[
            KeyTerm("Adl", "(Kök: 'a-d-l) Denk olmak, eşitlik, insaf etmek; terazinin kefelerini eşitleyip ifrat ile tefrit arasında orta yolu bulmak."),
            KeyTerm("Kıst", "Pay, nasip ve hakkaniyet; hakkı sahibine eksiksiz ve pratik olarak teslim etmek."),
            KeyTerm("Zulüm", "Adaletin tam zıddı; bir şeyi ait olduğu asıl bağlamdan koparmak ve hakkı sahibinden esirgemek."),
            KeyTerm("Kozmik Adalet", "Adaletin yalnız beşerî bir erdem değil, kâinatın üzerine bina edildiği evrensel ilke olarak sunulması."),
        ],
    )
    ch3.pages.append(
        ChapterPage()
        .add_terms(ch3.key_terms)
        .add_ayat("Ayet-i Kerîmeler", [
            Ayah(
                "Nisâ 135 — Hüküm ve Şahitlikte Mutlak Objektiflik",
                "يَا أَيُّهَا الَّذِينَ آمَنُوا كُونُوا قَوَّامِينَ بِالْقِسْطِ شُهَدَاءَ لِلَّهِ وَلَوْ عَلَىٰ أَنفُسِكُمْ أَوِ الْوَالِدَيْنِ وَالْأَقْرَبِينَ ۚ إِن يَكُنْ غَنِيًّا أَوْ فَقِيرًا فَاللَّهُ أَوْلَىٰ بِهِمَا",
                "Ey iman edenler! Allah için hakkı titizlikle ayakta tutan, adalet ile şahitlik eden kimseler olun. Şahitliğiniz kendi aleyhinize, anne-babanızın ve yakın akrabanızın aleyhine dahi olsa adaletten şaşmayın. Şahitlik ettiğiniz kişi ister zengin ister fakir olsun, Allah onlara (sizden) daha yakındır.",
                "<b>Kıst:</b> Pay, nasip ve hakkaniyet. 'Adl' genel bir dengeyi ifade ederken 'Kıst' hakkı sahibine eksiksiz ve pratik olarak teslim etmeyi ifade eder.",
            ),
        ])
        .add_ayat(None, [
            Ayah(
                "Nisâ 58 — Emanet ve Liyakat",
                "إِنَّ اللَّهَ يَأْمُرُكُمْ أَن تُؤَدُّوا الْأَمَانَاتِ إِلَىٰ أَهْلِهَا وَإِذَا حَكَمْتُم بَيْنَ النَّاسِ أَن تَحْكُمُوا بِالْعَدْلِ ۚ إِنَّ اللَّهَ نِعِمَّا يَعِظُكُم بِهِ",
                "Şüphesiz Allah, emanetleri ehline (layık olanlara) teslim etmenizi ve insanlar arasında hükmettiğiniz zaman adaletle hükmetmenizi emreder. Allah size ne güzel öğüt veriyor!",
                "<b>Adl:</b> Denk olmak, eşitlik, insaf etmek; terazinin kefelerini eşitlemek ve ifrat ile tefrit arasında orta yolu bulmak.",
            ),
        ])
    )
    ch3.pages.append(
        ChapterPage()
        .add_ayat("Ayet-i Kerîmeler · Devam", [
            Ayah(
                "Mâide 8 — Düşmana Karşı Bile Adalet",
                "وَلَا يَجْرِمَنَّكُمْ شَنَآنُ قَوْمٍ عَلَىٰ أَلَّا تَعْدِلُوا ۚ اعْدِلُوا هُوَ أَقْرَبُ لِلتَّقْوَىٰ",
                "Bir topluluğa olan kininiz, sizi adaletsizliğe itmesin. Adil olun; bu, takvaya daha uygundur.",
                "<b>Şeneân:</b> Şiddetli kin ve buğz. Ayet, duygusal öfkeyi hukukun dışında tutarak adaleti düşmanlık ilişkisinden bağımsızlaştırır.",
            ),
        ])
        .add_block(BulletBlock(1, "Adaletin Kavramsal Boyutları, Kozmik İlke ve Vicdanî Eğitim", [
            "Kur'an-ı Kerîm'de adalet; <b>'adl'</b>, <b>'kıst'</b>, <b>'keyl'</b> (ölçü) ve <b>'hak'</b> gibi "
            "birbirini tamamlayan kavramlarla ifade edilir: <b>'İnsanlar arasında bir tarafa meyletmeden "
            "davranmak ve herkese hak ettiğini vermek.'</b> Tam zıddı ise <b>zulüm</b>, <b>cevr</b> ve "
            "insafsızlıktır.",
            "<b>Kozmik Bir İlke Olarak Adalet:</b> Kur'an adaleti sadece beşerî/hukukî bir erdem olarak değil, "
            "kâinatın üzerine bina edildiği <b>kozmik bir ilke</b> olarak takdim eder. Allah gökleri ve yeri "
            "<b>'hak' ile</b> yaratmıştır; Zemahşerî'nin de vurguladığı gibi Allah'ın adaleti (<b>el-Adl</b> "
            "sıfatı) evrendeki düzenin temel unsurudur.",
            "<b>Ahiret İnancı ve Vicdanî Eğitim:</b> Adaletin, fizikî müeyyidelerden önce insanın derununda kök "
            "salması amaçlanır. Hesaba çekileceği inancı, insanı <b>hiçbir otoritenin bulunmadığı gizli "
            "yerlerde bile</b> zulümden uzaklaştıran en büyük denetim gücüdür.",
        ]))
        .add_table(ComparisonTable(
            "Kur'an'da Adaletin Temel Uygulama Alanları (Medine Dönemi)",
            ["Alan", "Kur'ânî İlke"],
            [
                ["Hüküm ve Şahitlikte", "Şahitlik kendi, anne-baba veya akraba aleyhine dahi olsa objektiflik bozulmaz; <b>zengin-fakir statüsü</b> adaletin seyrini değiştiremez, düşmana duyulan öfke mazeret olamaz."],
                ["Cezada", "Suç ile ceza arasında <b>denge</b> esastır; kötülüğün cezası misliyle mukabeledir, ancak toplumsal barışı tesis edecek <b>affetme kapısı</b> daima açık tutulur."],
                ["Savaşta", "Cihad sömürü veya <b>ganimet amaçlı değil</b>, zulmü ve fitneyi ortadan kaldırmak içindir."],
                ["Toplumsal-Ekonomik", "Irk ve soy üstünlüğü reddedilir, üstünlük yalnız <b>takvâdadır</b>; servetin sadece zenginler arasında dönmesi reddedilip zekât ve sadaka ile sermayenin tabana yayılması emredilir."],
            ]
        ))
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "İslam'da adaletin gerçekleştirilmesi sadece kanun maddelerine değil, her an Allah tarafından "
            "denetlendiği şuuruna sahip <b>'vicdanlı insan' modeline</b> emanet edilmiştir."))
    )
    ch3.pages.append(
        ChapterPage()
        .add_ayat("Örnek Metin — Nesefî, Nisâ 135 Tefsiri (Medârikü't-Tenzîl)", [
            Ayah(
                "1 — 'Kıst ile Kāim Olmak'",
                "﴿يَا أَيُّهَا الَّذِينَ آمَنُوا كُونُوا قَوَّامِينَ بِالْقِسْطِ شُهَدَاءَ لِلَّهِ﴾ مُجْتَهِدِينَ فِي إِقَامَةِ الْعَدْلِ حَتَّى لَا تَجُورُوا",
                "'Ey iman edenler! Allah için hakkı titizlikle ayakta tutan, adalet ile şahitlik eden kimseler olun.' (Yani:) Zulmetmeyesiniz (cevr etmeyesiniz) diye adaleti ikame etmede tüm gayretini gösterenler (müçtehitler) olun.",
                "",
            ),
        ])
        .add_ayat(None, [
            Ayah(
                "2 — 'Şühedâe' Kelimesinin İrabı",
                "﴿شُهَدَاءَ﴾ خَبَرٌ بَعْدَ خَبَرٍ لِلَّهِ، أَيْ تُقِيمُونَ شَهَادَاتِكُمْ لِوَجْهِ اللَّهِ ﴿وَلَوْ عَلَى أَنْفُسِكُمْ﴾ وَلَوْ كَانَتِ الشَّهَادَةُ عَلَى أَنْفُسِكُمْ",
                "'Şühedâe' (şahitlik edenler) kelimesi, Allah lafzından ('lillâhi') sonra gelen ikinci bir haberdir. Yani: Şahitliklerinizi sadece Allah'ın vechi (rızası) için kāim kılarsınız. 'Kendi aleyhinize dahi olsa' — şahitlik kendi aleyhinize olsa bile.",
                "",
            ),
            Ayah(
                "3 — Kendi Aleyhine Şahitlik = İkrar",
                "وَهَذَا لِأَنَّ الدَّعْوَى وَالشَّهَادَةَ عَلَى نَفْسِهِ هِيَ الْإِقْرَارُ عَلَى نَفْسِهِ، لِأَنَّهُ فِي مَعْنَى الشَّهَادَةِ عَلَيْهَا بِإِلْزَامِ الْحَقِّ",
                "Bunun sebebi şudur: Kişinin kendi nefsine karşı açtığı dava ve şahitlik, aslında kendi aleyhine yaptığı bir 'ikrar'dır (kabullenmektir). Zira ikrar da hakkın zorunlu kılınması yönüyle kendi aleyhine şahitlik etme manasındadır.",
                "",
            ),
            Ayah(
                "4 — Akrabanın Aleyhine Şahitlik",
                "﴿أَوِ الْوَالِدَيْنِ وَالْأَقْرَبِينَ﴾ أَيْ وَلَوْ كَانَتْ عَلَى آبَائِكُمْ وَأُمَّهَاتِكُمْ وَأَقَارِبِكُمْ",
                "'Veya anne-babanızın ve yakın akrabanızın aleyhine dahi olsa.' Yani şahitlik babalarınızın, annelerinizin ve akrabalarınızın aleyhine olsa bile (adaletten şaşmayın).",
                "",
            ),
        ])
        .add_ayat(None, [
            Ayah(
                "5 — Zengin ve Fakir Karşısında Objektiflik",
                "﴿إِنْ يَكُنْ﴾ الْمَشْهُودُ عَلَيْهِ ﴿غَنِيًّا﴾ فَلَا يَمْنَعُكُمُ الشَّهَادَةُ عَلَيْهِ لِغِنَاهُ طَلَبًا لِمَرْضَاتِهِ ﴿أَوْ فَقِيرًا﴾ فَلَا يَمْنَعُكُمْ تَرَحُّمًا عَلَيْهِ ﴿فَاللَّهُ أَوْلَى بِهِمَا﴾ بِالْغَنِيِّ وَالْفَقِيرِ أَيْ بِالنَّظَرِ لَهُمَا وَالرَّحْمَةِ",
                "'Eğer aleyhine şahitlik edilen kimse zengin ise', onun zenginliği, rızasını aramak gayesiyle şahitliğe engel olmasın. 'Yahut fakir ise', ona acımanız sizi şahitlikten alıkoymasın. 'Allah o ikisine (sizden) daha yakındır' — zengine ve fakire, yani her ikisini de gözetme ve merhamet etme bakımından.",
                "",
            ),
        ])
    )
    ch3.pages.append(
        ChapterPage()
        .add_ayat("Örnek Metin (devamı) — Nesefî, Nisâ 135 Tefsiri", [
            Ayah(
                "6 — 'Ve İn Telvû' Kıraat Farkı",
                "﴿وَإِنْ تَلْوُوا﴾ بِوَاوٍ وَاحِدَةٍ وَضَمِّ اللَّامِ: شَامِيٌّ وَحَمْزَةُ مِنَ الْوِلَايَةِ، أَيْ وَإِنْ وُلِّيتُمْ إِقَامَةَ الْعَدْلِ ﴿أَوْ تُعْرِضُوا﴾ عَنْ إِقَامَتِهِ. غَيْرُهُمَا «تَلْوُوا» بِوَاوَيْنِ وَسُكُونِ اللَّامِ مِنَ اللَّيِّ، أَيْ وَإِنْ تَلْوُوا أَلْسِنَتَكُمْ عَنِ الشَّهَادَةِ أَوْ تُعْرِضُوا عَنْ أَدَائِهَا",
                "'Ve eğer eğip bükerseniz.' Şâmî (İbn Âmir) ve Hamza bu kelimeyi tek vav ve lâm'ın ötresiyle 'velayet' kökünden okumuşlardır: 'Eğer adaleti kāim kılmakla görevlendirilirseniz (vali olursanız).' Diğer imamlar ise iki vav ve lâm'ın sükunuyla 'leyy' (bükmek) kökünden okumuştur: 'Eğer dillerinizi şahitlikten eğip bükerseniz veya onu ifa etmekten yüz çevirirseniz.'",
                "",
            ),
        ])
        .add_callout(Callout("focus", "Akademik Nahiv ve Belâgat Nüktesi",
            "<b>Nahiv (Kıraat ve Gramer Etkisi):</b> 'Ve in telvû' kelimesi iki farklı kıraatle okunur. İbn Âmir "
            "ve Hamza'nın okuyuşunda (<b>tülû</b>) ayet <b>'siyasi/yönetimsel adalet'</b> bağlamına kayarken; "
            "diğer imamların okuyuşunda (<b>telvû</b>) <b>'dili eğip bükerek yalan şahitlik yapma'</b> bağlamına "
            "oturur.<br><br>"
            "<b>Nahiv (Zamir Uyumu):</b> 'Fallâhu evlâ bi-<b>himâ</b>' cümlesindeki <b>tesniye (ikil) zamir</b> "
            "ince bir nüktedir: ayetin başında 'ev' (veya) edatıyla tekil bir bağlam varken zamirin ikil gelmesi, "
            "zengin ve fakirin şahıs olarak değil <b>iki farklı cins/sınıf</b> olarak kastedilmesindendir."))
        .add_person(NASAFI)
        .add_info_cards("Nesefî'nin Metodu ve Eserleri", [
            InfoCard("Metodu", "Dilsel ve edebî yönlere dikkat çeker; sahih hadisleri merkeze alırken "
                     "<b>İsrailiyat'a</b> yer vermez.", "Metot"),
            InfoCard("Eserleri", "<b>Medârikü't-Tenzîl</b> (örnek metnin kaynağı), usulde "
                     "<b>Menârü'l-envâr</b>, fıkıhta <b>Kenzü'd-dekā'ik</b>.", "Eserler"),
        ])
        .add_summary("Kur'an'da adalet; adl, kıst, keyl ve hak kavramlarıyla örülü, kozmik bir ilke "
            "düzeyine yükseltilmiş bir değerdir. Hüküm-şahitlik, ceza, savaş ve toplumsal-ekonomik "
            "alanlarda somutlaşır; nihai güvencesi ise vicdanlı insandır.")
    )

    # =====================================================================
    # BÖLÜM 4 — Kur'ân'da İnsan Özgürlüğü ve Sorumluluğu
    # =====================================================================
    ch4 = Chapter(
        number=4,
        title="Kur'ân'da İnsan Özgürlüğü ve Sorumluluğu",
        subtitle="Hilâfet ve Emanet'ten ef'âlü'l-ibâd tartışmasına özgürlüğün Kur'ânî sınırları",
        key_terms=[
            KeyTerm("Hilâfet", "Allah'ın insanı yeryüzüne halife kılıp ona tasarrufta bulunma yetkisi vermesi."),
            KeyTerm("Emanet", "Ahzâb 72'de göklerin, yerin ve dağların yüklenmekten çekindiği; insanın hür iradesiyle üstlendiği sorumluluk."),
            KeyTerm("İstitâat", "İnsanın eylem anında Allah'ın kendisine verdiği gücü kullanarak özgür seçimini yapması."),
            KeyTerm("Vizr", "Ağır yük, vebal ve günah; 'suçun ve cezanın şahsîliği' ilkesinin temel teolojik dayanağı."),
        ],
    )
    ch4.pages.append(
        ChapterPage()
        .add_terms(ch4.key_terms)
        .add_ayat("Ayet-i Kerîmeler", [
            Ayah(
                "İsrâ 15 — Sorumluluğun Şahsîliği İlkesi",
                "مَّنِ اهْتَدَىٰ فَإِنَّمَا يَهْتَدِي لِنَفْسِهِ ۖ وَمَن ضَلَّ فَإِنَّمَا يَضِلُّ عَلَيْهَا ۚ وَلَا تَزِرُ وَازِرَةٌ وِزْرَ أُخْرَىٰ",
                "Kim doğru yola (hidayete) ererse ancak kendi nefsi lehine ermiş olur. Kim de saparsa ancak kendi aleyhine sapmış olur. Hiçbir günahkâr başkasının günah yükünü yüklenmez. Biz, bir peygamber göndermedikçe (kimseye) azap ediciler değiliz.",
                "<b>Vizr:</b> Ağır yük, vebal ve günah. İslam hukukundaki <b>'suçun ve cezanın şahsîliği'</b> ilkesinin temel teolojik dayanağıdır.",
            ),
        ])
        .add_ayat(None, [
            Ayah(
                "Fussilet 46 — İrade ve Özgürlüğün Bedeli",
                "مَنْ عَمِلَ صَالِحًا فَلِنَفْسِهِ ۖ وَمَنْ أَسَاءَ فَعَلَيْهَا ۗ وَمَا رَبُّكَ بِظَلَّامٍ لِّلْعَبِيدِ",
                "Kim salih (iyi) bir iş yaparsa kendi lehinedir. Kim de kötülük yaparsa kendi aleyhinedir. Rabbin kullarına asla zulmedici değildir.",
                "<b>Zallâm:</b> 'Çokça zulmeden' demektir. Allah'ın adaleti mutlaktır; kula irade verilmiş, seçtiği fiillerin neticesi de kendisine bırakılmıştır.",
            ),
        ])
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "İslâm'da insan, eylemlerini Allah'ın belirlediği imkân alanı (<b>istitâat</b>) içinde gerçekleştiren "
            "özgür bir varlıktır. Özgürlük insanın yeryüzündeki <b>en büyük sermayesi</b>; sorumluluk ise bu "
            "sermayeyi doğru kullanıp kullanmadığının <b>yegâne ölçüsüdür</b>."))
    )
    ch4.pages.append(
        ChapterPage()
        .add_block(BulletBlock(1, "Özgürlüğün İki Kur'ânî Temeli ve Sorumluluğun Engelleri", [
            "<b>Hilâfet:</b> Allah insanı yeryüzüne <b>halife</b> kılmış, ona tasarrufta bulunma yetkisi "
            "vermiştir. Bu yetki, insanın seçme kabiliyetinin ve dolayısıyla sorumluluğunun ilk temelidir.",
            "<b>Emanet:</b> Ahzâb 72. ayette göklerin, yerin ve dağların yüklenmekten çekindiği emaneti "
            "(sorumluluğu) insanın <b>hür iradesiyle</b> üstlendiği ifade edilir. Emaneti hakkıyla taşımamak ise "
            "Kur'an'da <b>'zulüm' ve 'cehalet'</b> olarak nitelendirilir.",
            "<b>Engel 1 — Nefis:</b> İnsanın iradesini kullanırken karşılaştığı ilk engel kendi içindeki "
            "nefistir; Şems suresine göre nefse hem fücûr hem de takvâ ilham edilmiştir.",
            "<b>Engel 2 — Şeytan:</b> Kur'an, şeytanın insan üzerinde <b>zorlayıcı bir otoritesinin (sultan) "
            "olmadığını</b>, onun sadece vesvese vererek kötülüğü süslü gösterdiğini vurgular. Böylece sorumluluk "
            "her hâlükârda insanın kendisinde kalır.",
        ]))
        .add_table(ComparisonTable(
            "Fiillerin Yaratıcısı Kimdir? — Ef'âlü'l-İbâd Tartışması (Sınavlık)",
            ["Ekol", "Görüşü ve Eleştirisi"],
            [
                ["Cebriyye <br>(Kaderciler)", "İnsanın hiçbir iradesi yoktur; Allah'ın iradesi karşısında <b>rüzgâr önündeki bir yaprak</b> gibidir. Ulemanın büyük çoğunluğu bunu reddetmiştir: iradesi olmayan birinin cezalandırılması ilahi adalete aykırıdır."],
                ["Mu'tezile <br>(Mutlak Özgürlükçüler)", "İnsan mutlak özgürdür ve <b>kendi fiillerinin yaratıcısıdır</b>. Ehl-i Sünnet bu görüşü, Allah'ın mutlak yaratıcılığına (Hâlık sıfatına) <b>ortak koşma riski</b> taşıdığı gerekçesiyle reddetmiştir."],
                ["Ehl-i Sünnet <br>/ Mâtürîdiyye", "Dengeyi kuran ekoldür: fiilin <b>yaratılması (halk)</b> Allah'a, o fiili <b>irade edip yapması (kesb)</b> insana aittir. İnsan, eylem anında Allah'ın verdiği gücü (<b>istitâat</b>) kullanarak özgür seçimini yapar ve sorumlu olur."],
            ]
        ))
        .add_ayat("Örnek Metin — M. İzzet Derveze, Bakara 6-7 Tefsiri (et-Tefsîrü'l-Hadîs)", [
            Ayah(
                "Bakara 6-7 — Tefsir Edilen Ayetler",
                "﴿إِنَّ الَّذِينَ كَفَرُوا سَوَاءٌ عَلَيْهِمْ أَأَنْذَرْتَهُمْ أَمْ لَمْ تُنْذِرْهُمْ لَا يُؤْمِنُونَ ۞ خَتَمَ اللَّهُ عَلَى قُلُوبِهِمْ وَعَلَى سَمْعِهِمْ وَعَلَى أَبْصَارِهِمْ غِشَاوَةٌ وَلَهُمْ عَذَابٌ عَظِيمٌ﴾",
                "Şüphesiz inkâr edenleri uyarsan da uyarmasan da onlar için birdir, iman etmezler. Allah onların kalplerini ve kulaklarını mühürlemiştir. Gözleri üzerinde de bir perde vardır ve onlar için büyük bir azap vardır.",
                "",
            ),
            Ayah(
                "1 — Takrîr: İman Etmeyeceklerinin Karara Bağlanması",
                "فِي هَاتَيْنِ الْآيَتَيْنِ تَقْرِيرٌ بِأَنَّ الْكُفَّارَ لَا يُؤْمِنُونَ سَوَاءٌ أَأَنْذَرَهُمُ النَّبِيُّ أَمْ لَمْ يُنْذِرْهُمْ؛ لِأَنَّ قُلُوبَهُمْ مُغْلَقَةٌ عَنْ فَهْمِ الْحَقِّ...",
                "Bu iki ayette, Peygamber onları uyarsa da uyarmasa da kâfirlerin iman etmeyecekleri karara bağlanmıştır (takrîr). Çünkü onların kalpleri hakkı anlamaya karşı kapalıdır (mühürlüdür)...",
                "",
            ),
        ])
    )
    ch4.pages.append(
        ChapterPage()
        .add_ayat("Örnek Metin (devamı) — Derveze, Bakara 6-7 Tefsiri", [
            Ayah(
                "2 — Nüzul Sebebi ve İstidrad",
                "وَلَمْ نَطَّلِعْ عَلَى رِوَايَةٍ خَاصَّةٍ بِنُزُولِ الْآيَتَيْنِ، وَالْمُتَبَادِرُ أَنَّهُمَا جَاءَتَا اسْتِطْرَادًا تَعْلِيلِيًّا لِمَوْقِفِ الْكُفَّارِ",
                "Bu iki ayetin nüzulüne (iniş sebebine) dair özel bir rivayete rastlamadık. Akla ilk gelen (mütebâdir) şudur ki; bu ayetler kâfirlerin tutumunu gerekçelendiren (ta'lîlî) bir konu arası geçiş (istidrad) olarak gelmiştir.",
                "",
            ),
            Ayah(
                "3 — İstidradın Amacı: Müttakilerle Mukayese",
                "لِلْمُقَابَلَةِ بَيْنَ مَوْقِفِهِمْ وَمَوْقِفِ الْمُتَّقِينَ الَّذِينَ اهْتَدَوْا بِهُدَى الْقُرْآنِ. فَهَؤُلَاءِ ذَوُو رَغْبَةٍ صَادِقَةٍ فِي...",
                "(Bu istidradın amacı), Kur'an'ın hidayetiyle doğru yolu bulan müttakilerin tutumu ile onların (kâfirlerin) inatçı tutumları arasında bir mukayese yapmaktır. Zira müttakiler, hakikati öğrenmede samimi bir arzuya sahip olanlardır...",
                "",
            ),
            Ayah(
                "4 — Müttakilerin Tasdiki, Kâfirlerin Kaybı",
                "فَحِينَمَا سَمِعُوا الْقُرْآنَ وَرَأَوْا أَعْلَامَ الْحَقِّ، صَدَّقُوا وَآمَنُوا. فِي حِينِ فُقِدَتِ النِّيَّةُ الْحَسَنَةُ وَالْهُدَى... يَخْشَوْنَ اللَّهَ فَآمَنُوا",
                "Onlar Kur'an'ı işittiklerinde ve hakkın işaretlerini (delillerini) gördüklerinde, tasdik ettiler ve inandılar. Buna karşılık (kâfirlerde) iyi niyet ve hidayet arzusu tamamen kaybolmuştur. (Müttakiler ise) Allah'tan korkarak iman etmişlerdir.",
                "",
            ),
        ])
        .add_ayat(None, [
            Ayah(
                "5 — Mühürlenmenin Sonucu",
                "وَكَأَنَّمَا أُغْلِقَتْ قُلُوبُهُمْ، وَسُدَّتْ آذَانُهُمْ، وَعَمِيَتْ أَبْصَارُهُمْ عَنْ رُؤْيَةِ نُورِهِ، وَقَدِ اسْتَحَقُّوا مِنْ أَجْلِ ذَلِكَ عَذَابَ اللَّهِ الْعَظِيمَ",
                "Sanki kâfirlerin kalpleri kilitlenmiş, kulakları tıkanmış ve gözleri O'nun nurunu görmekten kör olmuştur. Ve onlar sırf bu (inatları) yüzünden Allah'ın o büyük azabını hak etmişlerdir.",
                "",
            ),
        ])
        .add_callout(Callout("focus", "Akademik Nahiv ve Belâgat Nüktesi",
            "<b>Nahiv (Kader ve İrade Bağlamı):</b> Derveze, <b>'kalplerin mühürlenmesinin'</b> Allah'ın insanı "
            "zorla kâfir yapması (<b>Cebriyye görüşü</b>) anlamına gelmediğini ispatlar. Nahiv ve bağlam "
            "kurallarına göre mühürlenme, kâfirlerin <b>hür iradeleriyle</b> iyi niyeti ve hidayet arzusunu "
            "kaybetmelerinin doğal bir sonucu olarak meydana gelmiş ilahî bir tecellidir.<br><br>"
            "<b>Belâgat (Kinaye ve Temsil):</b> 'Gözlerinde perde vardır, kalpleri mühürlüdür' ibaresi fiziksel "
            "bir körlük veya mühür değil; inatları yüzünden hakikati algılama yetilerini yitiren insanları "
            "anlatan muazzam bir <b>Kinaye ve Temsil</b> sanatıdır."))
    )
    ch4.pages.append(
        ChapterPage()
        .add_person(DARWAZA)
        .add_info_cards("Derveze'nin Tefsir Metodu ve Eserleri", [
            InfoCard("Nüzul Sırasına Göre Tefsir", "Klasik gelenekten (Fâtiha'dan başlayıp Nâs'ta bitiren "
                     "sistemden) ayrılarak Kur'an'ı <b>ayetlerin iniş sırasına göre</b> tefsir etmiş; bu metodun "
                     "ayetlerin tarihsel bağlamını daha iyi anlattığını savunmuştur.", "Metot"),
            InfoCard("et-Tefsîrü'l-Hadîs", "Modern dönemin en dikkat çeken tefsiri. <b>İşlenen örnek metin "
                     "buradan alınmıştır.</b>", "Tefsir"),
            InfoCard("Târîhu'l-Arab ve'l-İslâm", "Arap tarihini ve İslam medeniyetinin doğuşunu, İslam'ın toplum "
                     "üzerindeki evrensel etkileriyle birlikte inceleyen başucu kitabı.", "Tarih"),
        ])
        .add_summary("İnsan özgürlüğü Kur'an'da Hilâfet ve Emanet kavramlarıyla temellendirilir; İsrâ 15 ile "
            "sorumluluğun şahsîliği, Fussilet 46 ile amelin sahibine ait olduğu ilan edilir. Ef'âlü'l-ibâd "
            "tartışmasında Ehl-i Sünnet/Mâtürîdiyye, Cebriyye'nin cebri ile Mu'tezile'nin mutlak özgürlükçülüğü "
            "arasında halk–kesb dengesini kurar.")
    )

    # =====================================================================
    # BÖLÜM 5 — Kur'ân'da Namaz
    # =====================================================================
    ch5 = Chapter(
        number=5,
        title="Kur'ân'da Namaz",
        subtitle="Evrensel bir ibadetten Mi'râc'a: namazın farziyet süreci ve koruyucu işlevi",
        key_terms=[
            KeyTerm("Salât", "Sözlükte 'dua etmek, ibadet etmek, bağışlanma dilemek'; namazın her rüknünün fiilî ve sözlü bir dua niteliği taşıması buradan gelir."),
            KeyTerm("Mevkût", "Vakti tayin edilmiş; sınırları ve zamanı Allah tarafından belirli kurallara bağlanmış farziyet."),
            KeyTerm("İkame", "Namazın şeklî bir hareketten öte; eksiksiz, huşû içinde ve vaktine riayet edilerek 'ayakta tutulması' gereken bilinç hali."),
            KeyTerm("Fahşâ ve Münker", "Hayâsızlık ve kötülük; Ankebût 45'e göre namazın insanı alıkoyduğu iki temel kötülük alanı."),
        ],
    )
    ch5.pages.append(
        ChapterPage()
        .add_terms(ch5.key_terms)
        .add_block(BulletBlock(1, "Evrensel ve Kadim Bir İbadet Olarak Namaz", [
            "Kur'ân-ı Kerîm'e göre namaz, sadece Hz. Muhammed'in (s.a.s.) ümmetine has yeni bir yükümlülük "
            "değildir; Hz. Âdem, Nûh, İbrahim, İsmail, İsa ve Musa gibi peygamberlerin tebliğlerinde de bulunan "
            "<b>evrensel ve kadim</b> bir ibadettir.",
            "İslam öncesi Hicaz bölgesinde <b>Hanifler</b> (Ebû Zer el-Gıfârî, Zeyd b. Amr gibi) namaz kılıyor "
            "olsalar da, müşriklerin Kâbe etrafındaki 'salât'ları sadece <b>ıslık çalmak ve el çırpmaktan</b> "
            "ibaret olan bozulmuş bir ritüeldi.",
            "Kur'ân'da <b>'ikame'</b> kelimesiyle ifade edilen namaz, şeklî bir hareketten ziyade; eksiksiz, huşû "
            "içinde ve vaktine riayet edilerek <b>'ayakta tutulması'</b> gereken bir bilinç halidir.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("İlk Dönem", "Sabah ve akşam olmak üzere günde <b>iki vakit</b> namaz"),
            FlowStep("Ara Dönem", "Bir süreliğine <b>gece namazı (teheccüd)</b> farz kılındı"),
            FlowStep("Mi'râc", "Hicret'ten <b>~1,5 yıl önce</b> gerçekleşen hadise"),
            FlowStep("Bugünkü Form", "<b>Beş vakit</b> namazın farziyeti sabit oldu"),
        ], caption="Namazın Farziyet Süreci"))
        .add_callout(Callout("insight", "Bireysel ve Toplumsal İşlevi",
            "Namaz, mümini günde beş kez Allah'ın huzuruna çıkararak <b>fıtratının bozulmasına engel olur</b>. "
            "Kur'ân'ın ifadesiyle 'hayâsızlıktan ve kötülükten alıkoymayan' bir namaz, sadece şeklî bir spordan "
            "ibaret kalır. Sosyolojik açıdan ise cemaatle kılınan namaz; <b>ırk, dil, renk ve makam farkı "
            "gözetmeksizin</b> tüm müminleri aynı safta eşitleyerek muazzam bir toplumsal barış ve dayanışma "
            "nizamı kurar."))
    )
    ch5.pages.append(
        ChapterPage()
        .add_ayat("Ayet-i Kerîmeler", [
            Ayah(
                "Ankebût 45 — Namazın Ahlâkî ve Koruyucu İşlevi",
                "اتْلُ مَا أُوحِيَ إِلَيْكَ مِنَ الْكِتَابِ وَأَقِمِ الصَّلَاةَ ۖ إِنَّ الصَّلَاةَ تَنْهَىٰ عَنِ الْفَحْشَاءِ وَالْمُنكَرِ ۗ وَلَذِكْرُ اللَّهِ أَكْبَرُ",
                "Kitaptan sana vahyolunanı oku ve namazı dosdoğru kıl. Şüphesiz namaz, hayâsızlıktan ve kötülükten alıkoyar. Allah'ı anmak elbette en büyük (ibadet)tir. Allah yaptıklarınızı bilir.",
                "<b>Salât:</b> Arapça'da sözlük olarak 'dua etmek, ibadet etmek, bağışlanma dilemek'. Namazın her rüknünün fiilî ve sözlü bir dua niteliği taşıması, kelimenin etimolojisiyle derin bir bağ kurar.",
            ),
        ])
        .add_ayat(None, [
            Ayah(
                "Nisâ 103 — Zamanı Belirlenmiş Bir Farz",
                "فَإِذَا قَضَيْتُمُ الصَّلَاةَ فَاذْكُرُوا اللَّهَ قِيَامًا وَقُعُودًا وَعَلَىٰ جُنُوبِكُمْ ۚ إِنَّ الصَّلَاةَ كَانَتْ عَلَى الْمُؤْمِنِينَ كِتَابًا مَّوْقُوتًا",
                "Namazı kıldığınızda, ayaktayken, otururken ve yanlarınız üzerindeyken Allah'ı anın. Güvenliğe kavuştuğunuzda namazı dosdoğru kılın. Şüphesiz namaz, müminler üzerine vakitleri belirlenmiş bir farzdır.",
                "<b>Mevkût:</b> Vakti tayin edilmiş, sınırları ve zamanı Allah tarafından belirli kurallara bağlanmış farziyet.",
            ),
        ])
        .add_ayat("Örnek Metin — el-Hâzin, Ankebût 45 Tefsiri (Lübâbü't-Te'vîl)", [
            Ayah(
                "1 — Soru: Neden Sadece Bu İki Emir?",
                "وَقَوْلُهُ تَعَالَى: ﴿اتْلُ مَا أُوحِيَ إِلَيْكَ مِنَ الْكِتَابِ﴾ يَعْنِي الْقُرْآنَ ﴿وَأَقِمِ الصَّلَاةَ﴾. فَإِنْ قُلْتَ: لِمَ أَمَرَ بِهَذَيْنِ الشَّيْئَيْنِ — تِلَاوَةِ الْكِتَابِ وَإِقَامَةِ الصَّلَاةِ — فَقَطْ؟",
                "Yüce Allah'ın 'Kitaptan sana vahyedileni oku' sözü Kur'an'ı kastetmektedir; 'Namazı dosdoğru kıl' emrine gelince — eğer dersen ki: Neden sadece bu iki şeyi (Kitabın tilâveti ile namazın ikamesini) emretti?",
                "",
            ),
            Ayah(
                "2 — Cevap: İbadetin Üç Kısmı",
                "قُلْتُ: لِأَنَّ الْعِبَادَةَ الْمُخْتَصَّةَ بِالْعَبْدِ ثَلَاثَةٌ: قَلْبِيَّةٌ وَهِيَ الِاعْتِقَادُ الْحَقُّ، وَلِسَانِيَّةٌ وَهِيَ الذِّكْرُ الْحَسَنُ، وَبَدَنِيَّةٌ وَهِيَ الْعَمَلُ الصَّالِحُ",
                "Derim ki: Kulun yerine getirmekle yükümlü olduğu ibadetler üç kısımdır. İlki kalbîdir, o da hak olan inançtır (itikattır). İkincisi lisânîdir (dille olandır), o da güzel zikirdir. Üçüncüsü ise bedenîdir, o da salih ameldir.",
                "",
            ),
        ])
    )
    ch5.pages.append(
        ChapterPage()
        .add_ayat("Örnek Metin (devamı) — el-Hâzin, Ankebût 45 Tefsiri", [
            Ayah(
                "3 — İtikat Tekrar Edilmez, Zikir ve Amel Edilir",
                "لَكِنَّ الِاعْتِقَادَ لَا يَتَكَرَّرُ، فَإِنِ اعْتَقَدَ شَيْئًا لَا يُمْكِنُهُ أَنْ يَعْتَقِدَهُ مَرَّةً أُخْرَى بَلْ ذَلِكَ يَدُومُ مُسْتَمِرًّا، فَبَقِيَ الذِّكْرُ وَالْعِبَادَةُ الْبَدَنِيَّةُ وَهُمَا مُمْكِنَا التَّكْرَارِ فَأَمَرَ بِهِمَا لِذَلِكَ",
                "Fakat itikat (inanç) tekrar edilmez; zira kişi bir şeye inandığında onu bir daha (yeni baştan) inanamaz, o sürekli devam eder. Geriye ise zikir ve bedenî ibadet kalır ki bu ikisinin tekrar edilmesi mümkündür. İşte bu yüzden (Allah) bu ikisini emretmiştir.",
                "",
            ),
            Ayah(
                "4 — Fahşâ ve Münkerin Tanımı",
                "﴿إِنَّ الصَّلَاةَ تَنْهَى عَنِ الْفَحْشَاءِ﴾ أَيْ مَا قَبُحَ مِنَ الْأَعْمَالِ ﴿وَالْمُنْكَرِ﴾ أَيْ مَا لَا يُعْرَفُ فِي الشَّرْعِ",
                "'Şüphesiz namaz hayâsızlıktan alıkoyar.' Yani amellerden çirkin olanlardan. 'Ve münkerden.' Yani şeriatta (dinde) bilinmeyen/kabul görmeyen şeylerden.",
                "",
            ),
            Ayah(
                "5 — İbn Mes'ûd ve İbn Abbas'ın Sözü",
                "ابْنُ مَسْعُودٍ وَابْنُ عَبَّاسٍ: فِي الصَّلَاةِ مُنْتَهًى وَمُزْدَجَرٌ عَنْ مَعَاصِي اللَّهِ، فَمَنْ لَمْ تَأْمُرْهُ صَلَاتُهُ بِالْمَعْرُوفِ وَلَمْ تَنْهَهُ عَنِ الْفَحْشَاءِ وَالْمُنْكَرِ لَمْ تَزِدْهُ صَلَاتُهُ مِنَ اللَّهِ إِلَّا بُعْدًا",
                "İbn Mes'ûd ve İbn Abbas şöyle demişlerdir: 'Namazın içinde Allah'a isyan etmekten alıkoyan ve (kötülükleri) engelleyen bir güç vardır. Kimin namazı ona iyiliği emretmez ve onu hayâsızlık ile kötülükten alıkoymazsa, o namaz o kişinin Allah'tan sadece daha da uzaklaşmasını artırır.'",
                "",
            ),
        ])
        .add_ayat(None, [
            Ayah(
                "6 — Zikrin Taatlerin En Faziletlisi Oluşu",
                "﴿وَلَذِكْرُ اللَّهِ أَكْبَرُ﴾ أَيْ أَنَّهُ أَفْضَلُ الطَّاعَاتِ، فَلِلصَّلَاةِ لَا بُدَّ وَأَنْ يَكُونَ أَبْعَدَ عَنِ الْفَحْشَاءِ وَالْمُنْكَرِ مِمَّنْ لَا يُرَاعِيهَا",
                "'Allah'ı zikretmek ise elbette en büyüktür.' Yani: Namaz kılan kişinin, namazı gözetmeyen kişiye göre hayâsızlıktan ve kötülükten daha uzak olması kaçınılmazdır. Çünkü o (Allah'ı zikretmek), taatlerin en faziletlisidir.",
                "",
            ),
            Ayah(
                "7 — İlahî Muhasebenin Kapsamı",
                "﴿وَاللَّهُ يَعْلَمُ مَا تَصْنَعُونَ﴾ يَعْنِي لَا يَخْفَى عَلَيْهِ شَيْءٌ مِنْ أَمْرِكُمْ",
                "'Allah yaptıklarınızı bilir.' Yani: İşlerinizden (durumunuzdan) hiçbir şey O'na gizli kalmaz.",
                "",
            ),
        ])
    )
    ch5.pages.append(
        ChapterPage()
        .add_callout(Callout("focus", "Akademik Nahiv ve Belâgat Nüktesi",
            "<b>Nahiv (İstimrâr ve Tekrâr Bağlamı):</b> el-Hâzin'e göre imanın (kalbî ibadetin) ayette "
            "emredilmemesinin sebebi, itikat eyleminin kesintisiz bir <b>süreklilik (istimrâr)</b> bildirmesi ve "
            "defalarca yeniden yapılamamasıdır; namaz ve okuma eylemleri ise vakitlere bağlı olarak defalarca "
            "yenilenen (<b>tekrâr</b>) fiillerdir.<br><br>"
            "<b>Belâgat (Teşhis ve İstiare):</b> 'Namaz insanı hayâsızlıktan alıkoyar' ibaresinde namaz, sadece "
            "bir hareket dizisi değil; insana konuşan, ona kötülükleri yapmamasını emreden <b>manevi bir "
            "bekçi/murakıp</b> gibi kişileştirilmiş ve canlı bir otorite olarak sunulmuştur."))
        .add_callout(Callout("route", "Kritik Çıkarım",
            "Namaz; Allah'ın büyüklüğünü (<b>tekbir</b>) itiraf, O'na teslimiyeti (<b>kıyam, rükû, secde</b>) "
            "bedensel olarak kanıtlama ve ruhu günah kirlerinden her gün düzenli olarak yıkama (<b>tövbe</b>) "
            "ameliyesidir."))
        .add_person(AL_KHAZIN)
        .add_info_cards("el-Hâzin'in İlmî Çizgisi ve Eseri", [
            InfoCard("Derlemeci Metodu", "Kütüphane yöneticiliği ona kaynaklara sınırsız erişim sağlamış; "
                     "ayetlerin edebî, dilsel, şer'î ve ahlâkî yönlerini bir arada harmanlamıştır.", "Metot"),
            InfoCard("Eleştirildiği Nokta", "Tefsirinde <b>İsrâiliyat'a</b> ve tarihî kıssalara çok fazla yer "
                     "verdiği için ilim çevrelerince ciddi eleştirilere maruz kalmıştır.", "Tenkit"),
            InfoCard("Lübâbü't-Te'vîl", "Kendi ifadesiyle Begavî'nin <b>Me'âlimü't-tenzîl</b>, Zemahşerî'nin "
                     "<b>el-Keşşâf</b>, Râzî'nin <b>Mefâtîhu'l-gayb</b> ve Beyzâvî'nin <b>Envârü't-tenzîl</b> "
                     "tefsirlerinden seçerek derlediği eseri.", "Tefsir"),
        ])
        .add_summary("Namaz, tüm peygamberlerin tebliğinde bulunan evrensel bir ibadettir ve bugünkü beş vakitlik "
            "formuna Mi'râc ile kavuşmuştur. Kalbî–lisânî–bedenî ibadet üçlüsünün sözel ve bedensel ayağını "
            "oluşturur; Ankebût 45'e göre kişiyi fahşâ ve münkerden alıkoyduğu ölçüde hem bireysel hem toplumsal "
            "anlamını bulur.")
    )

    chapters = [ch1, ch2, ch3, ch4, ch5]

    # =====================================================================
    # KAVRAMLAR SÖZLÜĞÜ
    # =====================================================================
    glossary = [
        Concept("Ma'rûf", "Akıl ve dinin iyi kabul ettiği, toplumca 'tanıdık' ve güzel karşılanan her şey.", "Lokmân 17", 1),
        Concept("Münker", "Aklın ve dinin reddettiği, toplum vicdanında çirkin görülen davranış; ma'rûfun zıddı.", "Lokmân 17", 1),
        Concept("Hevnen", "Kendini beğenmişlikten uzak, ağırbaşlı ve mütevazı bir duruş.", "Furkân 63", 1),
        Concept("Azîm", "Kadri, kıymeti ve etkisi çok büyük; takdir edilemeyecek kadar yüce.", "Kalem 4", 1),
        Concept("Huluk", "Nefsin kalıcı tabiatları; tek başına kullanıldığında iyi tabiat ve erdemleri ifade eder.", "Tâhir b. Âşûr", 1),
        Concept("Mürüvvet", "Cahiliye'de kabile asabiyetine dayalı cesaret-misafirperverlik-intikam erdemleri.", "Ahlâkî dönüşüm", 1),
        Concept("Ahsen-i Takvim", "İnsanın en güzel kıvamda, çift kutuplu fıtratla yaratılması.", "Ahlâkî fıtrat", 1),
        Concept("Fücûr", "Nefse ilham edilen kötülüğe meyil; takvânın karşıtı.", "Şems Suresi", 1),
        Concept("Takvâ", "Nefse ilham edilen, kötülükten sakınma yeteneği.", "Şems Suresi", 1),
        Concept("Şems Suresi", "Nefse hem fücûrun hem takvânın ilham edildiğini bildiren, çift kutupluluğun dayanağı olan sure.", "Ahlâkî fıtrat", 1),
        Concept("Esfel-i Sâfilîn", "Nefsini fücura daldıran insanın yuvarlandığı 'aşağıların aşağısı' hali.", "Ahlâkî fıtrat", 1),
        Concept("Temekkün", "Bir vasfa sarsılmaz şekilde yerleşmiş, ona bütünüyle hâkim olma hali.", "Nahiv nüktesi", 1),
        Concept("İstiare", "Maddi bir büyüklükten ödünç alınan kelimeyle soyut bir yüceliği anlatma sanatı.", "Belâgat", 1),
        Concept("Tecessüs", "İnsanların gizli hallerini ve kusurlarını kötü niyetle araştırmak, casusluk.", "Hucurât 12", 2),
        Concept("Tahassüs", "Hasan-ı Basrî kıraatinde 'ha' ile okunan biçim; iyilikleri araştırmak.", "Kıraat farkı", 2),
        Concept("Hümeze / Lümeze", "Arkadan çekiştirme ve yüze karşı küçük düşürüp alay etme.", "Hümeze 1-3", 2),
        Concept("Gıybet", "Kişiyi, duyduğunda hoşlanmayacağı şekilde anmak.", "Hucurât 12", 2),
        Concept("Hevâ", "Hakkı görmeyi engelleyen bencil, nefsanî arzular; 'hevâsını ilah edinmek'.", "Ahlâkî çöküş", 2),
        Concept("Suizân / Hüsnüzan", "Kötü zan yasaklanmış, iyi zan ise güzel bir davranış olarak övülmüştür.", "İbn Cüzey", 2),
        Concept("Havâtır", "Kalbe gelen ve defedilmesine güç yetirilemeyen düşünceler.", "İbn Cüzey", 2),
        Concept("Sûü'l-huluk", "Kötü huyların genel adı; el-ahlâku'z-zemîme ve el-ahlâku's-seyyie ile eş anlamlı.", "Kavramsal ağ", 2),
        Concept("Câhiliye Hamiyyesi", "Asaletle övünüp kendini üstün görme tutuculuğu; takvânın zıddı.", "Yerilen davranışlar", 2),
        Concept("Hâl (Durum Zarfı)", "'Meyten' kelimesinin irabdaki konumu: 'ölü olduğu halde' anlamını verir.", "Nahiv", 2),
        Concept("Nâfi' Kıraati", "Hucurât 12'deki 'meyten' kelimesini şeddeli olarak 'meyyiten' okuyan kıraat.", "Kıraat farkı", 2),
        Concept("Mübalağa", "Gıybetin çirkinliğinin katman katman artırılmasında kullanılan abartı sanatı.", "Zemahşerî", 2),
        Concept("İstifhâm-ı İnkârî", "İnkâr ve tiksinti bildiren soru sanatı ('Sever misiniz?').", "Belâgat", 2),
        Concept("Adl", "Denk olmak, eşitlik; ifrat ile tefrit arasında orta yolu bulmak.", "Nisâ 58", 3),
        Concept("Kıst", "Hakkı sahibine eksiksiz ve pratik olarak teslim etmek; hakkaniyet.", "Nisâ 135", 3),
        Concept("Keyl", "Kur'an'da adaletle birlikte anılan 'ölçü' kavramı.", "Adalet kavramları", 3),
        Concept("Zulüm / Cevr", "Bir şeyi bağlamından koparmak ve hakkı sahibinden esirgemek; adaletin zıddı.", "Adalet kavramları", 3),
        Concept("Kozmik Adalet", "Adaletin, kâinatın üzerine bina edildiği evrensel ilke olması.", "Zemahşerî", 3),
        Concept("Ehliyet (Liyakat)", "Nisâ 58'de emanetlerin 'ehline' verilmesi emri; adaletin idarî boyutu.", "Nisâ 58", 3),
        Concept("Şeneân", "Bir topluluğa duyulan şiddetli kin; Mâide 8'de adalete mazeret sayılmaz.", "Mâide 8", 3),
        Concept("İkrar", "Kişinin kendi aleyhine şahitliği; hakkın zorunlu kılınması anlamında kabul.", "Nesefî", 3),
        Concept("Telvû / Tülû", "Nisâ 135'teki iki kıraat: dili eğip bükmek / yönetici (vali) olmak.", "Nesefî", 3),
        Concept("Hilâfet", "Allah'ın insanı yeryüzüne halife kılıp tasarruf yetkisi vermesi.", "Özgürlüğün temeli", 4),
        Concept("Emanet", "Göklerin ve dağların çekindiği, insanın hür iradesiyle üstlendiği sorumluluk.", "Ahzâb 72", 4),
        Concept("Vizr", "Ağır yük, vebal, günah; suçun şahsîliği ilkesinin dayanağı.", "İsrâ 15", 4),
        Concept("Zallâm", "'Çokça zulmeden'; Allah'ın kullarına asla zulmetmediğini vurgular.", "Fussilet 46", 4),
        Concept("Ef'âlü'l-ibâd", "Kulların fiillerinin kim tarafından yaratıldığına dair kelâm tartışması.", "Kelâm", 4),
        Concept("Kesb", "Fiili irade edip yapmanın insana ait olması; halk (yaratma) ise Allah'a aittir.", "Mâtürîdiyye", 4),
        Concept("İstitâat", "İnsanın eylem anında Allah'ın verdiği gücü kullanarak özgür seçim yapması.", "Mâtürîdiyye", 4),
        Concept("Cebriyye", "İnsanın hiçbir iradesi olmadığını savunan, çoğunlukça reddedilen ekol.", "Kelâm", 4),
        Concept("İstidrad", "Bir konu anlatılırken araya giren, açıklayıcı/ta'lîlî geçiş.", "Derveze", 4),
        Concept("Kinaye", "Kalp mührü ve göz perdesi ifadelerinde olduğu gibi dolaylı anlatım sanatı.", "Belâgat", 4),
        Concept("Salât", "Dua etmek, ibadet etmek, bağışlanma dilemek.", "Ankebût 45", 5),
        Concept("Mevkût", "Vakti Allah tarafından tayin edilmiş farziyet.", "Nisâ 103", 5),
        Concept("İkame", "Namazın huşû içinde, eksiksiz 'ayakta tutulması' gereken bilinç hali.", "Namaz", 5),
        Concept("Fahşâ ve Münker", "Namazın alıkoyduğu hayâsızlık ve (şeriatça kabul görmeyen) kötülük.", "Ankebût 45", 5),
        Concept("Hanifler", "İslam öncesi Hicaz'da namaz kılan tevhid ehli (Zeyd b. Amr, Ebû Zer).", "Namazın tarihi", 5),
        Concept("Mi'râc", "Beş vakit namazın farz kılındığı, Hicret'ten ~1,5 yıl önceki hadise.", "Farziyet süreci", 5),
        Concept("İstimrâr", "İtikadın kesintisiz sürekliliği; tekrar edilemez oluşu.", "el-Hâzin", 5),
        Concept("Teşhis", "Namazın, kötülüğü engelleyen manevi bir bekçi gibi kişileştirilmesi.", "Belâgat", 5),
        Concept("İsrâiliyat", "Yahudi-Hıristiyan kaynaklı asılsız rivayetler; el-Hâzin'in eleştirildiği nokta.", "Tefsir usulü", 5),
    ]

    # =====================================================================
    # TEST — 24 Soruluk Genel Değerlendirme
    # =====================================================================
    test_questions = [
        TestQuestion(1, "Cahiliye Arap toplumunda ahlâkı ifade eden, cesaret ve misafirperverliği kapsamakla birlikte temeli kabile gururuna dayanan kavram hangisidir?",
            {"A": "Takvâ", "B": "Mürüvvet", "C": "Ma'rûf", "D": "Hevnen", "E": "Huluk"}),
        TestQuestion(2, "Lokmân 17'de geçen \"ma'rûf\" kavramının Kur'ânî anlamı aşağıdakilerden hangisidir?",
            {"A": "Yalnızca vahiyle bildirilen ibadet şekli", "B": "Kabilenin çıkarına uygun olan davranış",
             "C": "Akıl ve dinin iyi kabul ettiği, toplum vicdanında güzel karşılanan her şey",
             "D": "Yöneticinin emrettiği her iş", "E": "Sadece maddi yardım ve sadaka"}),
        TestQuestion(3, "Kur'an'a göre insanın ahlâkî fıtratıyla ilgili aşağıdakilerden hangisi doğrudur?",
            {"A": "İnsan yalnızca iyiliğe meyilli yaratılmıştır", "B": "İnsana hem fücûr hem takvâ ilham edilmiştir; ahlâk bu ikisi arasında iradî bir tercihtir",
             "C": "İnsanın ahlâkî tercihi doğuştan belirlenmiştir", "D": "Ahlâk yalnız toplumsal şartların ürünüdür",
             "E": "Ahsen-i takvim, insanın günah işleyemeyeceği anlamına gelir"}),
        TestQuestion(4, "\"Ahlâkî değerler objektiftir ve akılla bilinebilir; vahiy olmasa bile akıl iyiyi ve kötüyü bulabilir\" görüşü hangi ekole aittir?",
            {"A": "Eş'ariyye", "B": "Mâtürîdiyye", "C": "Cebriyye", "D": "Mu'tezile", "E": "Selefiyye"}),
        TestQuestion(5, "Ahlâkın kaynağı tartışmasında \"akıl değerlerin bir kısmını kavrayabilir, ancak sevap-günah hükmü için vahyin bildirimi şarttır\" diyen sentezci ekol hangisidir?",
            {"A": "Mu'tezile", "B": "Eş'ariyye", "C": "Mâtürîdiyye", "D": "Cebriyye", "E": "Zâhiriyye"}),
        TestQuestion(6, "Hz. Âişe'nin (r.a.) Hz. Peygamber'in ahlâkı sorulduğunda verdiği ve \"huluk-ı azîm\"in en kapsamlı tefsiri sayılan cevap hangisidir?",
            {"A": "\"O, insanların en cömerdiydi\"", "B": "\"Onun ahlâkı Kur'an idi\"", "C": "\"O, hiç öfkelenmezdi\"",
             "D": "\"O, geceleri hep namaz kılardı\"", "E": "\"O, mürüvvetin zirvesiydi\""}),
        TestQuestion(7, "Tâhir b. Âşûr'un Kalem 4 tefsirinde \"Alâ\" edatıyla ilgili yaptığı nahiv analizinin sonucu nedir?",
            {"A": "Edat mecazî değil hakiki bir üstünlük bildirir", "B": "Edat, Peygamber'in o ahlâka sarsılmaz şekilde yerleştiğini (temekkün) gösterir",
             "C": "Edat, ahlâkın geçici bir hâl olduğunu gösterir", "D": "Edat zaid (fazladan) olup manaya etki etmez",
             "E": "Edat, ayetin Mekkî olduğunu ispatlar"}),
        TestQuestion(8, "Hucurât 12'de yasaklanan \"tecessüs\" kavramının sözlük anlamı aşağıdakilerden hangisidir?",
            {"A": "Kişiyi yüzüne karşı küçük düşürmek", "B": "Mal biriktirip tekrar tekrar saymak",
             "C": "İnsanların gizli hallerini ve kusurlarını kötü niyetle araştırmak, casusluk yapmak",
             "D": "Zannın tamamından sakınmak", "E": "Kalbe gelen düşünceleri defetmek"}),
        TestQuestion(9, "Hasan-ı Basrî'nin kıraatine göre kelimenin \"ha\" harfiyle okunuşu (tahassüs) hangi anlama gelir?",
            {"A": "Kötülükleri araştırmak", "B": "İyilikleri araştırmak", "C": "Gıybet etmek",
             "D": "Zannı dillendirmek", "E": "Alay etmek"}),
        TestQuestion(10, "Hümeze suresinde geçen \"hümeze\" ve \"lümeze\" kavramları hangi seçenekte doğru açıklanmıştır?",
            {"A": "Hümeze yüze karşı alay etmek, lümeze arkadan çekiştirmek",
             "B": "Hümeze arkadan çekiştirmek ve kaş-göz işaretiyle ayıplamak, lümeze yüze karşı küçük düşürmek",
             "C": "İkisi de mal biriktirme hırsını ifade eder", "D": "Hümeze zan, lümeze tecessüstür",
             "E": "Hümeze haset, lümeze kibirdir"}),
        TestQuestion(11, "İbn Cüzey'e göre \"zan\"ın günah olması hususunda nakledilen görüşlerden biri aşağıdakilerden hangisidir?",
            {"A": "Zan her hâlükârda günahtır, ruhsat yoktur", "B": "Zan ancak kişi onu dillendirirse günah olur; konuşmazsa genişlik vardır",
             "C": "Zan yalnızca kâfirler hakkında günahtır", "D": "Zan, kalbe geldiği anda küfre yol açar",
             "E": "Zan, yalnızca hâkimler için yasaktır"}),
        TestQuestion(12, "Zemahşerî'nin tespitine göre Hucurât 12'de gıybetin çirkinliğinin katman katman artırıldığı mübalağa sıralaması hangisidir?",
            {"A": "İnsan eti → Ölü eti → Et yemek → Kardeş eti", "B": "Et yemek → İnsan eti → Ölü insan eti → Kendi ölü kardeşinin eti",
             "C": "Kardeş eti → Et yemek → İnsan eti → Ölü eti", "D": "Ölü eti → Kardeş eti → İnsan eti → Et yemek",
             "E": "Et yemek → Kardeş eti → Ölü eti → İnsan eti"}),
        TestQuestion(13, "\"Adl\" ile \"Kıst\" arasındaki fark aşağıdakilerden hangisinde doğru verilmiştir?",
            {"A": "Adl yalnız ekonomiye, kıst yalnız hukuka aittir", "B": "Adl hakkı eksiksiz teslim etmek, kıst genel dengedir",
             "C": "Adl genel bir dengeyi, kıst ise hakkı sahibine eksiksiz ve pratik olarak teslim etmeyi ifade eder",
             "D": "İkisi de tamamen eş anlamlıdır", "E": "Adl ahiretle, kıst dünyayla ilgilidir"}),
        TestQuestion(14, "Nisâ 135'e göre şahitlikle ilgili aşağıdakilerden hangisi söylenemez?",
            {"A": "Şahitlik kişinin kendi aleyhine dahi olsa yapılmalıdır", "B": "Anne-baba ve akraba aleyhine de olsa adaletten şaşılmaz",
             "C": "Şahitlik edilen kişinin zenginliği veya fakirliği hükmü değiştirmez",
             "D": "Nefsin arzusuna (hevâya) uyup adaletten sapmak yasaklanmıştır",
             "E": "Yakın akraba söz konusuysa şahitlikten çekinmek caizdir"}),
        TestQuestion(15, "Nisâ 58'de emredilen ve adaletin idarî boyutunu oluşturan ilke aşağıdakilerden hangisidir?",
            {"A": "Emanetlerin ehline (layık olanlara) teslim edilmesi", "B": "Ganimetin eşit paylaştırılması",
             "C": "Şahitlerin sayısının artırılması", "D": "Cezaların misliyle uygulanması",
             "E": "Zekâtın yalnız akrabaya verilmesi"}),
        TestQuestion(16, "Nesefî'nin Nisâ 135 tefsirinde \"fallâhu evlâ bi-himâ\" ifadesindeki ikil (tesniye) zamirin gerekçesi nedir?",
            {"A": "Anne ve babanın kastedilmesi", "B": "Zengin ve fakirin şahıs olarak değil, iki farklı cins/sınıf olarak kastedilmesi",
             "C": "İki şahidin şart koşulması", "D": "İki kıraat imamına işaret edilmesi", "E": "Dünya ve ahiretin kastedilmesi"}),
        TestQuestion(17, "Mâide 8'in adalet anlayışına kattığı temel ilke aşağıdakilerden hangisidir?",
            {"A": "Adalet yalnız müminler arasında geçerlidir", "B": "Bir topluluğa duyulan kin dahi adaletsizliğe mazeret olamaz",
             "C": "Savaş halinde adalet askıya alınır", "D": "Zenginlere ayrı, fakirlere ayrı ölçü uygulanır",
             "E": "Adalet yalnızca yöneticileri bağlar"}),
        TestQuestion(18, "Ahzâb 72'de göklerin, yerin ve dağların yüklenmekten çekindiği; insanın ise hür iradesiyle üstlendiği kavram hangisidir?",
            {"A": "Hilâfet", "B": "Emanet", "C": "İstitâat", "D": "Vizr", "E": "Kesb"}),
        TestQuestion(19, "İsrâ 15'te geçen \"vizr\" kavramı, İslam hukukunda hangi ilkenin teolojik dayanağıdır?",
            {"A": "Kanunîlik ilkesi", "B": "Suçun ve cezanın şahsîliği ilkesi", "C": "Masumiyet karinesi",
             "D": "Kıyas ilkesi", "E": "Maslahat ilkesi"}),
        TestQuestion(20, "Ef'âlü'l-ibâd tartışmasında Ehl-i Sünnet/Mâtürîdiyye'nin kurduğu denge hangi seçenekte doğru verilmiştir?",
            {"A": "Fiilin yaratılması da yapılması da insana aittir", "B": "Fiilin yaratılması (halk) Allah'a, irade edip yapılması (kesb) insana aittir",
             "C": "İnsanın hiçbir iradesi yoktur, her şey cebrîdir", "D": "İnsan fiillerinin yaratıcısıdır, Allah sadece bilir",
             "E": "Fiiller ne yaratılır ne kesbedilir; tesadüfîdir"}),
        TestQuestion(21, "Derveze'nin Bakara 6-7 tefsirinde \"kalplerin mühürlenmesi\" ifadesiyle ilgili vardığı sonuç nedir?",
            {"A": "Allah insanları zorla kâfir yapmıştır (Cebriyye görüşü doğrudur)",
             "B": "Mühürlenme, kâfirlerin hür iradeleriyle hidayet arzusunu kaybetmelerinin doğal bir sonucudur",
             "C": "Ayet fiziksel bir körlük ve sağırlıktan söz eder", "D": "Ayetin özel bir nüzul sebebi kesin olarak bilinmektedir",
             "E": "Ayet yalnızca Ehl-i Kitap hakkında inmiştir"}),
        TestQuestion(22, "İslam öncesi Hicaz bölgesinde namazla ilgili durum hangi seçenekte doğru verilmiştir?",
            {"A": "Hiç kimse namaz kılmıyordu", "B": "Hanifler namaz kılıyordu; müşriklerin Kâbe'deki 'salât'ı ise ıslık çalıp el çırpmaktan ibaretti",
             "C": "Müşrikler beş vakit namaz kılıyordu", "D": "Namaz yalnızca Ehl-i Kitap'a farzdı",
             "E": "Namaz sadece Mi'râc'dan sonra bilinmeye başlandı"}),
        TestQuestion(23, "Namazın bugünkü beş vakitlik formda farz kılınması hangi hadiseyle sabit olmuştur?",
            {"A": "Hicret'in ilk yılı", "B": "Bedir Savaşı", "C": "Hicret'ten yaklaşık 1,5 yıl önce gerçekleşen Mi'râc",
             "D": "Hudeybiye Antlaşması", "E": "Veda Haccı"}),
        TestQuestion(24, "el-Hâzin'e göre Ankebût 45'te imanın (kalbî ibadetin) ayrıca emredilmemesinin sebebi nedir?",
            {"A": "İman ibadet sayılmadığı için", "B": "İtikat kesintisiz bir süreklilik (istimrâr) bildirir ve tekrar edilemez; namaz ve okuma ise tekrarlanabilir fiillerdir",
             "C": "İman yalnızca peygamberlerden istendiği için", "D": "Ayetin muhatabı yalnızca münafıklar olduğu için",
             "E": "İman, zikirle aynı anlama geldiği için"}),
    ]

    answer_key_items = [
        AnswerItem(1, "B", "<b>Mürüvvet</b>, cesaret-misafirperverlik-intikam erdemlerini kapsayan ama temeli <b>kabile gururu</b> olan cahiliye ahlâk anlayışıdır."),
        AnswerItem(2, "C", "<b>Ma'rûf</b>, akıl ve dinin iyi kabul ettiği, toplumun ortak vicdanında 'tanıdık' ve güzel karşılanan her şeydir; zıddı <b>münker</b>dir."),
        AnswerItem(3, "B", "Kur'an insanı <b>ahsen-i takvim</b> üzere yaratılmış sayar; nefse hem <b>fücûr</b> hem <b>takvâ</b> ilham edilmiştir ve ahlâk bu iki güç arasındaki <b>iradî tercihtir</b>."),
        AnswerItem(4, "D", "Bu, <b>Mu'tezile</b>'nin (akılcıların) görüşüdür; Eş'ariyye ise ahlâkın tek kaynağının vahiy olduğunu savunur."),
        AnswerItem(5, "C", "<b>Mâtürîdiyye</b> sentezci ekoldür: akıl değerlerin bir kısmını kavrar, ancak dinî hüküm (sevap/günah) için <b>vahyin bildirimi şarttır</b>."),
        AnswerItem(6, "B", "Hz. Âişe'nin (r.a.) <b>\"Onun ahlâkı Kur'an idi\"</b> cevabı, huluk-ı azîmin en kapsamlı (câmi) tefsiri kabul edilir."),
        AnswerItem(7, "B", "Tâhir b. Âşûr'a göre 'Alâ' edatı mecazî bir isti'lâ bildirir ve kastedilen <b>temekkün</b>'dür: atın sırtına sağlamca oturan binici gibi o ahlâka bütünüyle hâkim olmak."),
        AnswerItem(8, "C", "<b>Tecessüs</b>, insanların gizli hallerini ve kusurlarını kötü niyetle araştırmak, casusluk yapmaktır; İslâm ahlâkı bunu sosyal barışı zehirleyen bir hastalık sayar."),
        AnswerItem(9, "B", "'Cim' ile <b>tecessüs</b> kötülükleri, 'ha' ile <b>tahassüs</b> ise iyilikleri araştırmaktır; ikinci okuyuş Hasan-ı Basrî'ye aittir."),
        AnswerItem(10, "B", "<b>Hümeze</b> arkadan çekiştirmek ve kaş-göz işaretiyle ayıplamak; <b>lümeze</b> ise yüze karşı küçük düşürmek ve alay etmektir."),
        AnswerItem(11, "B", "İbn Cüzey'in naklettiği görüşe göre zan ancak <b>dillendirilirse</b> günah olur; zira insan kalbine gelen düşünceleri (<b>havâtır</b>) defetmeye güç yetiremez."),
        AnswerItem(12, "B", "Mübalağa şu sırayla katmanlanır: <b>Et yemek → İnsan eti → Ölü insan eti → Kendi ölü kardeşinin eti</b>; ayrıca 'Sever misiniz?' sorusu istifhâm-ı inkârîdir."),
        AnswerItem(13, "C", "<b>Adl</b> genel bir dengeyi, <b>kıst</b> ise hakkı sahibine eksiksiz ve pratik olarak teslim etmeyi (pay/hakkaniyet) ifade eder."),
        AnswerItem(14, "E", "Ayet tam tersini emreder: şahitlik <b>anne-baba ve yakın akraba aleyhine</b> dahi olsa adaletten şaşılmaz; bu yüzden E söylenemez."),
        AnswerItem(15, "A", "Nisâ 58, <b>emanetlerin ehline (layık olanlara)</b> verilmesini ve insanlar arasında adaletle hükmedilmesini emreder — liyakat ilkesinin Kur'ânî dayanağıdır."),
        AnswerItem(16, "B", "Nesefî'ye göre zamirin ikil gelmesi, zengin ve fakirin birer şahıs olarak değil <b>iki farklı cins/sınıf</b> olarak kastedilmesindendir."),
        AnswerItem(17, "B", "Mâide 8, <b>şeneân</b> (bir topluluğa duyulan şiddetli kin) dahi olsa adaletsizliğe mazeret olamayacağını bildirir: 'Adil olun, bu takvaya daha uygundur.'"),
        AnswerItem(18, "B", "<b>Emanet</b>, Ahzâb 72'de göklerin, yerin ve dağların yüklenmekten çekindiği sorumluluktur; insan bunu hür iradesiyle üstlenmiştir."),
        AnswerItem(19, "B", "<b>Vizr</b> (ağır yük, vebal); 'Hiçbir günahkâr başkasının yükünü yüklenmez' ilkesiyle <b>suçun ve cezanın şahsîliğinin</b> teolojik dayanağıdır."),
        AnswerItem(20, "B", "Ehl-i Sünnet/Mâtürîdiyye dengesi: fiilin <b>yaratılması (halk)</b> Allah'a, <b>irade edip yapılması (kesb)</b> insana aittir; insan <b>istitâat</b> ile seçer."),
        AnswerItem(21, "B", "Derveze'ye göre mühürlenme, Cebriyye'nin iddia ettiği gibi zorlama değil; kâfirlerin <b>hür iradeleriyle</b> iyi niyeti ve hidayet arzusunu kaybetmelerinin doğal sonucudur."),
        AnswerItem(22, "B", "Hicaz'da <b>Hanifler</b> (Zeyd b. Amr, Ebû Zer) namaz kılıyordu; müşriklerin Kâbe etrafındaki 'salât'ı ise <b>ıslık çalmak ve el çırpmaktan</b> ibaret bozulmuş bir ritüeldi."),
        AnswerItem(23, "C", "Beş vakit namaz, Hicret'ten yaklaşık <b>1,5 yıl önce</b> gerçekleşen <b>Mi'râc</b> hadisesiyle farz kılınmıştır; öncesinde sabah-akşam iki vakit ve bir süre teheccüd vardı."),
        AnswerItem(24, "B", "el-Hâzin'e göre itikat <b>istimrâr</b> (kesintisiz süreklilik) bildirir ve tekrar edilemez; ayette emredilenler ise tekrarı mümkün olan <b>lisânî (okuma) ve bedenî (namaz)</b> ibadetlerdir."),
    ]

    return CoursePack(
        course_code="TEFSİR II",
        title='Tefsir <span class="accent-word">II</span>',
        subtitle="Kur'ân'da Ahlâk, Adalet, Özgürlük ve Namaz — Final Özeti",
        description=(
            "Kur'an'ın bireysel ve toplumsal hayatı inşa eden evrensel ahlâk nizamını, sakındırdığı kötülükleri, "
            "adalet tasavvurunu, insanın özgürlük ve sorumluluk dengesini ve ibadetlerin kalbi olan namazı; "
            "orijinal ayet metni, akademik meal, konu anlatımı, müfessir alıntısı ve biyografi ekseninde sunan "
            "nokta atışı bir final yol haritası."
        ),
        theme="forest",
        theme_color="#246038",
        icon_text="T",
        chapters=chapters,
        glossary=glossary,
        test_title="Genel Değerlendirme Testi",
        test_subtitle="Güzel ahlâktan namaza, Tefsir II üzerine kapsamlı çoktan seçmeli test",
        test_instructions="Aşağıdaki sorularda beş seçenekten yalnızca birini işaretleyiniz. Süre: 35 dakika.",
        test_questions=test_questions,
        answer_key_intro="Her sorunun doğru cevabı ve kısa gerekçesi aşağıda yer almaktadır.",
        answer_key_items=answer_key_items,
        overview_lead=(
            "Bu ders; Kur'an'ın bireysel ve toplumsal hayatı inşa eden <b>evrensel ahlâk nizamını</b>, "
            "sakındırdığı <b>olumsuz davranışları</b>, kozmik bir ilke düzeyine yükselttiği <b>adalet "
            "tasavvurunu</b>, insanın <b>özgürlük ve sorumluluk</b> dengesini ve ibadetlerin kalbi olan "
            "<b>namazı</b>; her bölümde ayet → konu anlatımı → müfessir metni → biyografi sırasıyla ele alır."
        ),
        overview_cards=[
            {"title": "Güzel Ahlâk", "text": "Mürüvvetten evrensel erdemlere; fücûr-takvâ fıtratı ve ahlâkın kaynağı tartışması."},
            {"title": "Yerilen Davranışlar", "text": "Zan, tecessüs, gıybet, haset ve kibrin toplumsal dokuyu tahrip eden ağı."},
            {"title": "Adalet", "text": "Adl-kıst ayrımı, kozmik ilke ve dört temel uygulama alanı."},
            {"title": "Özgürlük ve Sorumluluk", "text": "Hilâfet, Emanet ve ef'âlü'l-ibâd tartışmasında halk-kesb dengesi."},
            {"title": "Namaz", "text": "Evrensel ibadetten Mi'râc'a farziyet süreci; fahşâ ve münkerden alıkoyan işlevi."},
            {"title": "Beş Müfessir", "text": "Tâhir b. Âşûr, İbn Cüzey, Nesefî, Derveze ve el-Hâzin'in metot ve eserleri."},
        ],
        overview_flow=[
            ("Ayet", "Orijinal metin + akademik meal"),
            ("Konu Anlatımı", "Kavram ağı ve mezhep ayrımları"),
            ("Örnek Metin", "Müfessirden doğrudan alıntı"),
            ("Nahiv-Belâgat", "Gramer ve sanat nüktesi"),
            ("Biyografi", "Müfessirin çizgisi ve eserleri"),
        ],
        overview_note=(
            "Sınavda en çok karıştırılan yer, <b>mezhep tartışmalarının hangi konuya ait olduğudur:</b> "
            "Mu'tezile / Eş'ariyye / Mâtürîdiyye ayrımı <u>ahlâkın kaynağı</u> tartışmasına; Cebriyye / "
            "Mu'tezile / Ehl-i Sünnet ayrımı ise <u>fiillerin yaratıcısı (ef'âlü'l-ibâd)</u> tartışmasına aittir."
        ),
    )
