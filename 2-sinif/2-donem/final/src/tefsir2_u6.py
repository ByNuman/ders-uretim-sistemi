# -*- coding: utf-8 -*-
"""TEFSİR II — 6. ÜNİTE: KUR'ÂN'DA GÜZEL AHLÂK
Görsel Ders Notu Kitabı, içerik tanımı.

Kaynak: 'kaynaklar/ders_kaynaklari/TEFSİR II/Tefsir II.pdf' (ders kitabı,
81 sayfa) — 6. ÜNİTE, s. 32-37 (PDF s. 36-41).

Ünitenin dört alt bölümü de bu modülde karşılık bulur:
  6.1 Ayet-i Kerîmeler   -> bölümlere dağıtılmış add_ayat() blokları (9 ayet kümesi)
  6.2 Kur'ân'da Güzel Ahlâk -> Bölüm 1-4'ün konu anlatımı
  6.3 Örnek Metin        -> Bölüm 5, Tâhir b. Âşûr / et-Tahrîr ve't-Tenvîr
  6.4 Tâhir b. Âşûr      -> Bölüm 5'teki Person kartı + biyografi bloğu

TEKNİK NOT (Arapça): Ayetlerin Arapça metni kaynak PDF'ten KOPYALANMAMIŞTIR —
o PDF'in metin katmanında fetha yerine üstün-elif basılıyor ve "الله"→"هللا",
"الم"→"اِل" gibi harf kaymaları var. Metinler sûre/âyet referanslarından
standart imlâ ile, tam harekeli olarak yeniden yazılmış; müfessir alıntıları
ise kaynaktan çıkarılıp bilinen ToUnicode bozulmaları onarılarak kurulmuştur.
Her Arapça parça üretilen PDF üzerinde görsel olarak doğrulanmıştır.
"""
import sys
from pathlib import Path
# Proje kökü: src/ -> <sinav> -> <donem> -> <sinif> -> KÖK (4 seviye yukarı)
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from content_model import (
    Person, KeyTerm, Callout, FlowStep, FlowDiagram, ComparisonTable,
    InfoCard, BulletBlock, Chapter, ChapterPage, Concept, CoursePack,
    Ayah, TestQuestion, AnswerItem,
)

# ---------------------------------------------------------------------------
# MÜFESSİR (TEK KAYNAK) — tarihler/eserler yalnızca burada tanımlanır
# ---------------------------------------------------------------------------

IBN_ASUR = Person(
    id="ibn_asur",
    name="Tâhir b. Âşûr",
    years="1879–1973",
    tagline="et-Tahrîr ve't-Tenvîr Müellifi · Zeytûne Rektörü",
    bio=[
        "1879'da Tunus'ta, Fas asıllı köklü bir aileye mensup olarak doğdu. "
        "1892'de orta ve yüksek öğretim kurumu olan Zeytûne Camii'ne girerek "
        "Arap dili ve edebiyatı, fıkıh usulü, hadis ve tefsir okudu; 1903'te "
        "Zeytûne Üniversitesi'ne öğretim elemanı olarak tayin edildi ve burada "
        "Arap dili ve edebiyatı, hukuk felsefesi ve İslamî ilimler dersleri verdi. "
        "1932'de rektörlüğe atandı, reform girişimlerine karşı çıkan çevreler "
        "yüzünden görevinden alındı, 1945 ve 1956'da yeniden aynı göreve getirildi. "
        "Eğitim sisteminin modernleşmesini ve İslamî ilimlerin daha kapsamlı ele "
        "alınmasını savunarak ders programlarına fen bilimlerini ekleme çabasında "
        "bulundu; mücadeleci kimliğiyle Tunus'un bağımsızlık sürecinde aktif rol "
        "aldı ve modern eğitim reformlarının öncülerinden biri oldu. 1973'te yine "
        "Tunus'ta vefat etti.",
    ],
    key_work="et-Tahrîr ve't-Tenvîr",
    initials="TÂ",
)


def get_pack() -> CoursePack:
    # ======================================================================
    # BÖLÜM 1 — AHLÂKIN KAVRAMSAL ÇERÇEVESİ VE CÂHİLİYE MİRASI
    # ======================================================================
    ch1 = Chapter(
        number=1,
        title="Ahlâkın Kavramsal Çerçevesi ve Câhiliye Mirası",
        subtitle="Hulukun'dan mürüvvete: bir kelimenin lügat kökünden İslâm'ın getirdiği gayeye",
        key_terms=[
            KeyTerm("Ahlâk", "Arapça'da <b>“seciye, tabiat, huy”</b> anlamlarına gelen "
                             "<i>hulukun</i> kelimesinin çoğulu."),
            KeyTerm("Istılahî ahlâk", "Tutum ve davranışların <b>kaynağı mahiyetindeki</b> "
                                      "ruhî ve mânevî melekeler."),
            KeyTerm("Mürûe (mürüvvet)", "Câhiliye dönemi Araplarında “ahlâk” kavramı yerine "
                                        "daha çok kullanılan tabir."),
            KeyTerm("Fahr · Mecd · Gazap", "Câhiliye ahlâkının temelinde tatmin edilmek istenen "
                                           "üç duygu: <b>kabile gururu</b>, <b>şeref</b>, <b>öfke</b>."),
        ],
    )
    ch1.pages.append(
        ChapterPage()
        .add_terms(ch1.key_terms)
        .add_block(BulletBlock(
            1, "Kelimenin Lügat ve Istılah Anlamı",
            [
                "<b>Lügatte:</b> Ahlâk kelimesi, Arapça'da “seciye, tabiat, huy” gibi anlamlara "
                "gelen <i>hulukun</i> kelimesinin <b>çoğuludur</b>.",
                "<b>Istılahta:</b> Ahlâk, tutum ve davranışların <b>kaynağı mahiyetindeki</b> "
                "ruhî ve mânevî melekeleri ifade eder.",
                "Tanımdaki kilit ifade <b>“kaynağı mahiyetindeki”</b>dir: ahlâk, tanım gereği "
                "<b>davranışın kendisi değil, davranışı doğuran iç yetidir</b>. Davranışlar "
                "dışarıda görünen sonuçtur; ahlâk ise onları üreten, nefiste yerleşik melekedir.",
            ],
            subtitle="Ahlâk görünmez; ahlâkın izleri görünür",
        ))
        .add_callout(Callout(
            "focus", "Tanımı Elde Tutun",
            "Bu ıstılah tanımı, ünitenin iki ayrı yerinde tekrar karşınıza çıkacak: "
            "<b>konu anlatımında</b> “güzel ahlâk mücerret bir davranış biçimi değildir” "
            "tespitinde ve <b>örnek metinde</b> İbn Âşûr'un “ahlâk nefiste gizlidir, "
            "tezahürleri ise kişinin tasarruflarıdır” cümlesinde.",
        ))
        .add_table(ComparisonTable(
            "Câhiliye ahlâkı ile İslâm ahlâkının karşılaştırması",
            ["Ölçüt", "Câhiliye", "İslâm"],
            [
                ["Kullanılan tabir", "<b>Mürûe</b> (mürüvvet)", "<b>Ahlâk</b>"],
                ["Öne çıkan erdemler", "Şecaat, kerem, vefâ", "Aynı erdemler + <b>yeni bir gaye</b>"],
                ["Erdemlerin karakteri", "<b>Kabileci ve dünyevî</b> bir karakterle sınırlı",
                 "Kabile sınırından çıkmış, <b>evrensel</b>"],
                ["Temelindeki saik", "Fahr, mecd ve gazabı <b>tatmin etme arzusu</b>",
                 "<b>Allah'ın rızasını hedeflemek</b> ve <b>nefsi dizginlemek</b>"],
            ],
        ))
    )
    ch1.pages.append(
        ChapterPage()
        .add_block(BulletBlock(
            2, "Câhiliye Ahlâkının Üç Duygusal Temeli",
            [
                "<b>Fahr (kabile gururu):</b> Erdemin ölçüsü kabilenin övünç kaynağı olmasıdır.",
                "<b>Mecd (şeref):</b> Cömertlik ve cesaret, şerefi yükselttiği ölçüde değerlidir.",
                "<b>Gazap (öfke):</b> Haksızlığa verilen karşılık, öfkenin tatmini üzerinden ölçülür.",
                "Câhiliye'de cesaret vardı, fakat <b>kabilenin cesaretiydi</b>; cömertlik vardı, "
                "fakat kabilenin <b>şerefini yükselten</b> cömertlikti.",
            ],
            subtitle="Erdemler mevcuttu, fakat gaye kabileyle sınırlıydı",
        ))
        .add_block(BulletBlock(
            3, "İslâm'ın Getirdiği Gaye",
            [
                "İslâm, bu geleneklerin karşısında insana <b>ahlakî eylemlerinde bir gaye</b> sunmuştur.",
                "Bu gayenin <b>iki bileşeni</b> vardır: <b>Allah'ın rızasını hedeflemek</b> ve "
                "<b>insanın nefsini dizginlemesi</b>.",
                "Bu ikisi birlikte, <b>ferdî ve sosyal planda ahlakî yücelmenin ölçüsü</b> olarak "
                "takdim edilmektedir.",
            ],
        ))
        .add_flow(FlowDiagram(
            [
                FlowStep("Aynı Erdemler", "Şecaat · Kerem · Vefâ"),
                FlowStep("Farklı Gaye", "Kabile gururu değil, Allah'ın rızası"),
                FlowStep("Evrenselleşme", "Erdem kabile sınırından çıkar"),
            ],
            caption="İslâm, erdemlerin listesini değil gayesini değiştirdi",
        ))
        .add_summary(
            "Câhiliye ile İslâm arasındaki fark <b>erdemlerin listesinde değil, erdemlerin "
            "gayesindedir</b>. Câhiliye de cesareti, cömertliği ve vefayı övüyordu; ama bunları "
            "fahr, mecd ve gazabı tatmin için yapıyordu. İslâm aynı erdemleri Allah'ın rızası ve "
            "nefsin dizginlenmesi eksenine bağlayarak onları evrenselleştirmiştir."
        )
    )

    # ======================================================================
    # BÖLÜM 2 — KUR'ÂN'IN İNSAN TASAVVURU VE AHLÂK-İBADET BÜTÜNLÜĞÜ
    # ======================================================================
    ch2 = Chapter(
        number=2,
        title="Kur'ân'ın İnsan Tasavvuru ve Ahlâk-İbadet Bütünlüğü",
        subtitle="Ahsen-i takvîm ile toprak arasında: çift kutuplu insan ve ibadetin ahlâkî işlevi",
        key_terms=[
            KeyTerm("Ahsen-i takvîm", "İnsanın <b>en güzel bir tabiatta yaratılmış</b> olması."),
            KeyTerm("Fücûr", "Allah'ın insan nefsine ilham ettiği <b>kötülük</b> kutbu."),
            KeyTerm("Takvâ", "Aynı nefse ilham edilen, kötülükten <b>sakınma yeteneği</b>."),
            KeyTerm("Kur'ân ahlâkı", "Hz. Âişe'nin, Hz. Peygamber'in ahlâkını nitelerken "
                                     "kullandığı ifade."),
        ],
    )
    ch2.pages.append(
        ChapterPage()
        .add_terms(ch2.key_terms)
        .add_block(BulletBlock(
            1, "İslâm Ahlâkının Kaynağı",
            [
                "İslâm ahlâkının <b>asıl kaynağı Kur'ân-ı Kerîm</b> ve <b>onun ışığında oluşan "
                "Sünnet'tir</b>.",
                "Nitekim <b>Hz. Âişe</b>, Hz. Peygamber'in ahlâkının <b>“Kur'ân ahlâkı”</b> "
                "olduğunu belirtmiştir.",
                "Bu söz ünitede iki ayrı yerde geçer: burada <b>kaynağı belirlemek</b> için; "
                "Bölüm 5'teki örnek metinde ise İbn Âşûr'un uzun uzun <b>tefsir ettiği rivayet</b> olarak.",
            ],
        ))
        .add_block(BulletBlock(
            2, "Kur'ân'ın İnsan Tasavvuru: Çift Kutupluluk",
            [
                "Kur'ân insanı iki nitelikle tanımlar: <b>en güzel bir tabiatta yaratılmış</b> "
                "(ahsen-i takvîm) ve <b>ilahî ruhtan üflenmiş</b> bir varlık.",
                "Ancak insanın <b>topraktan gelen beşerî cephesi</b>, onu ahlâkî bakımdan "
                "<b>çift kutuplu bir varlık</b> kılmıştır.",
                "Kur'ân'da bu durum, Allah'ın insan nefsine hem <b>kötülüğü (fücûr)</b> hem de "
                "<b>ondan sakınma yeteneğini (takvâ)</b> ilham etmesi şeklinde ifade edilir.",
                "Neticesi de aynı yerde bildirilir: <b>nefsini temiz tutan kurtuluşa erer</b>, "
                "<b>onu kirleten hüsrana uğrar</b>.",
            ],
        ))
        .add_flow(FlowDiagram(
            [
                FlowStep("Ahsen-i Takvîm", "İlahî ruhtan üflenmiş"),
                FlowStep("Beşerî Cephe", "Topraktan gelen yön"),
                FlowStep("Çift Kutup", "Fücûr / Takvâ"),
                FlowStep("Tercih", "Nefsi temizlemek ya da kirletmek"),
                FlowStep("Sonuç", "Kurtuluş / Hüsran"),
            ],
            caption="Ahlâkı mümkün kılan yapı: insanın iki yönlü yaratılışı",
        ))
    )
    ch2.pages.append(
        ChapterPage()
        .add_ayat("Ayet-i Kerîmeler", [
            Ayah(
                "Lokmân 31/17 — Ahlâkın Üç Ayağı",
                "يَا بُنَيَّ أَقِمِ الصَّلَاةَ وَأْمُرْ بِالْمَعْرُوفِ وَانْهَ عَنِ الْمُنْكَرِ وَاصْبِرْ عَلَى مَا أَصَابَكَ إِنَّ ذَلِكَ مِنْ عَزْمِ الْأُمُورِ",
                "Yavrum! Namazı dosdoğru kıl. İyiliği emret. Kötülükten alıkoy. Başına gelen "
                "musibetlere karşı sabırlı ol. Çünkü bunlar kesin olarak emredilmiş işlerdendir.",
                "<b>Ma'rûf:</b> Akıl ve dinin iyi kabul ettiği, toplumun ortak vicdanında güzel "
                "karşılanan her şey. Ayet <b>ibadet + toplumsal sorumluluk + sabrı</b> tek bir "
                "emir dizisinde toplar.",
            ),
            Ayah(
                "Furkān 25/63 — Tevazu ve Vakar",
                "وَعِبَادُ الرَّحْمَنِ الَّذِينَ يَمْشُونَ عَلَى الْأَرْضِ هَوْنًا وَإِذَا خَاطَبَهُمُ الْجَاهِلُونَ قَالُوا سَلَامًا",
                "Rahmân'ın kulları, yeryüzünde vakar ve tevazu ile yürüyen kimselerdir. Cahiller "
                "onlara laf attıkları zaman, “selâm” der (geçer)ler.",
                "<b>Hevnen:</b> Kendini beğenmişlikten uzak, ağırbaşlı ve mütevazı bir duruş. "
                "Ahlâk, <b>yürüyüşe kadar inen</b> bir bütünlüktür.",
            ),
        ])
        .add_block(BulletBlock(
            3, "Ahlâk-İman-İbadet Bütünlüğü",
            [
                "Kur'ân'da güzel ahlâk, <b>mücerret bir davranış biçimi olarak değil, iman ve "
                "ibadetle iç içe geçmiş bir sistem</b> olarak sunulur.",
                "<b>Ahlâkın konumu:</b> bireyin Allah'a olan bağlılığının <b>en somut göstergesidir</b>.",
                "<b>İbadetlerin konumu:</b> sadece şekilsel ritüellerden ibaret olmayıp, bireyin "
                "<b>ahlâkî gelişimini destekleyen birer eğitim aracıdır</b>.",
                "<b>Namaz:</b> Ankebût Sûresi'nde namazın insanı <b>hayâsızlıktan ve kötülükten "
                "alıkoyduğu</b> belirtilir (el-Ankebût 29/45).",
                "<b>Oruç:</b> <b>sabrı ve merhameti teşvik ederek</b> bireyin ahlâkî kontrolünü "
                "geliştirmeyi amaçlar.",
            ],
        ))
        .add_summary(
            "Kur'ân'ın insan tasavvuru ahlâkı <b>mümkün</b> kılan şeydir: insan yalnızca iyiliğe "
            "programlanmış olsaydı ahlâktan söz edilemezdi, yalnızca kötülüğe meyilli olsaydı "
            "ahlâk imkânsız olurdu. İbadet ise bu tercihi terbiye eden araçtır — namaz "
            "kötülükten alıkoyar, oruç sabrı ve merhameti öğretir."
        )
    )

    # ======================================================================
    # BÖLÜM 3 — KUR'ÂN'IN DÖRT EVRENSEL AHLÂK İLKESİ
    # ======================================================================
    ch3 = Chapter(
        number=3,
        title="Kur'ân'ın Dört Evrensel Ahlâk İlkesi",
        subtitle="Adalet, sıdk, merhamet ve sabır: toplumsal huzurun ve bireysel kemalin anahtarları",
        key_terms=[
            KeyTerm("Adalet", "Güzel ahlâkın <b>temel direği</b>; Kur'ân onu <b>takvâya en yakın</b> "
                              "davranış olarak niteler."),
            KeyTerm("Sıdk (doğruluk)", "İslâm ahlâkının <b>özü</b>; insanı iyiliğe ve nihayetinde "
                                       "cennete götüren yol."),
            KeyTerm("Merhamet", "Yetimi azarlamamak ve isteyeni geri çevirmemek; <b>toplumsal "
                                "sorumluluk bilincinin</b> tezahürü."),
            KeyTerm("Sabır", "Kur'ân'da <b>yüce bir erdem</b>; kötülüğü en güzel şekilde savmak "
                             "ve metaneti korumak."),
        ],
    )
    ch3.pages.append(
        ChapterPage()
        .add_terms(ch3.key_terms)
        .add_block(BulletBlock(
            1, "İlkelerin Konumu",
            [
                "Kur'ân'da güzel ahlâk, <b>belirli evrensel ilkeler etrafında şekillenir</b>.",
                "Bu ilkeler, <b>toplumsal huzurun ve bireysel kemalin anahtarlarıdır</b>.",
                "Kaynak bu ilkeleri <b>dört başlıkta</b> sıralar: adalet, doğruluk (sıdk), "
                "merhamet ve yardımseverlik, sabır ve hoşgörü.",
            ],
        ))
        .add_table(ComparisonTable(
            "Dört evrensel ahlâk ilkesi ve kaynaktaki delilleri",
            ["İlke", "Konumu", "Delili"],
            [
                ["<b>Adalet</b>", "Güzel ahlâkın <b>temel direği</b>; hem Allah'a hem insanlara "
                 "karşı bir sorumluluk", "Adalet, <b>takvâya en yakın</b> davranıştır (el-Mâide 5/8)"],
                ["<b>Doğruluk (Sıdk)</b>", "İslâm ahlâkının <b>özü</b>",
                 "el-Ahzâb 33/70; doğruluk iyiliğe ve cennete götüren yoldur (Müslim, “Birr” 105)"],
                ["<b>Merhamet ve Yardımseverlik</b>", "<b>Toplumsal sorumluluk bilincinin</b> tezahürü",
                 "Yetimi azarlamamak, isteyeni geri çevirmemek (ed-Duhâ 93/9-10)"],
                ["<b>Sabır ve Hoşgörü</b>", "<b>Yüce bir erdem</b>; müminin karakterini belirginleştirir",
                 "Kötülüğü en güzel şekilde savmak (Fussilet 41/34)"],
            ],
        ))
    )
    ch3.pages.append(
        ChapterPage()
        .add_ayat("Ayet-i Kerîmeler", [
            Ayah(
                "Nahl 16/90 — Üç Emir, Üç Yasak",
                "إِنَّ اللَّهَ يَأْمُرُ بِالْعَدْلِ وَالْإِحْسَانِ وَإِيتَاءِ ذِي الْقُرْبَى وَيَنْهَى عَنِ الْفَحْشَاءِ وَالْمُنْكَرِ وَالْبَغْيِ يَعِظُكُمْ لَعَلَّكُمْ تَذَكَّرُونَ",
                "Şüphesiz Allah adaleti, iyilik yapmayı, yakınlara yardım etmeyi emreder; "
                "hayâsızlığı, fenalık ve azgınlığı da yasaklar. O, düşünüp tutasınız diye size "
                "öğüt veriyor.",
                "<b>Bağy:</b> Haddi aşma, azgınlık — başkasının hakkına taşan tutum.",
            ),
            Ayah(
                "Ahzâb 33/70-71 — Kavl-i Sedîd",
                "يَا أَيُّهَا الَّذِينَ آمَنُوا اتَّقُوا اللَّهَ وَقُولُوا قَوْلًا سَدِيدًا يُصْلِحْ لَكُمْ أَعْمَالَكُمْ وَيَغْفِرْ لَكُمْ ذُنُوبَكُمْ وَمَنْ يُطِعِ اللَّهَ وَرَسُولَهُ فَقَدْ فَازَ فَوْزًا عَظِيمًا",
                "Ey iman edenler! Allah'a karşı gelmekten sakının ve doğru söz söyleyin ki Allah "
                "sizin işlerinizi düzeltsin ve günahlarınızı bağışlasın. Kim Allah'a ve Resûlüne "
                "itaat ederse, muhakkak büyük bir başarıya ulaşmıştır.",
                "<b>Sedîd:</b> Hedefi tam tutturan, isabetli ve sağlam söz. Doğru söz burada bir "
                "erdem olmakla kalmaz, <b>amellerin ıslahına ve mağfirete giden bir sebeptir</b>.",
            ),
        ])
        .add_table(ComparisonTable(
            "Nahl 16/90'ın emir ve yasak listesi",
            ["Emredilen üç şey", "Yasaklanan üç şey"],
            [
                ["<b>Adl</b> — adalet", "<b>Fahşâ</b> — hayâsızlık"],
                ["<b>İhsân</b> — iyilik yapmak", "<b>Münker</b> — fenalık"],
                ["<b>Îtâü zi'l-kurbâ</b> — yakınlara yardım", "<b>Bağy</b> — azgınlık"],
            ],
        ))
        .add_ayat("Ayet-i Kerîmeler", [
            Ayah(
                "Âl-i İmrân 3/134 — Muttakīlerin Portresi",
                "الَّذِينَ يُنْفِقُونَ فِي السَّرَّاءِ وَالضَّرَّاءِ وَالْكَاظِمِينَ الْغَيْظَ وَالْعَافِينَ عَنِ النَّاسِ وَاللَّهُ يُحِبُّ الْمُحْسِنِينَ",
                "Onlar bollukta ve darlıkta Allah yolunda harcayanlar, öfkelerini yenenler, "
                "insanları affedenlerdir. Allah iyilik edenleri sever.",
                "<b>Kâzımîne'l-gayz:</b> Öfkeyi yutup içeride tutmak — öfkenin yokluğu değil, "
                "<b>öfkeye hâkim olmak</b>.",
            ),
        ])
    )
    ch3.pages.append(
        ChapterPage()
        .add_ayat(None, [
            Ayah(
                "Bakara 2/177 — “Birr” Ayeti",
                "لَيْسَ الْبِرَّ أَنْ تُوَلُّوا وُجُوهَكُمْ قِبَلَ الْمَشْرِقِ وَالْمَغْرِبِ وَلَكِنَّ الْبِرَّ مَنْ آمَنَ بِاللَّهِ وَالْيَوْمِ الْآخِرِ وَالْمَلَائِكَةِ وَالْكِتَابِ وَالنَّبِيِّينَ",
                "İyilik, yüzlerinizi doğu ve batı taraflarına çevirmeniz(den ibaret) değildir. "
                "Asıl iyilik, Allah'a, ahiret gününe, meleklere, kitap ve peygamberlere iman "
                "edenlerin (tutum ve davranışlarıdır).",
                "<b>Birr:</b> Kapsayıcı iyilik. Ayet iyiliği <b>iman + mâlî fedakârlık + ibadet + "
                "ahde vefa + sabır</b> birlikteliği olarak tanımlar ve bunu gerçekleştirenleri "
                "iki kelimeyle niteler: <b>sadakū</b> (doğru olanlar) ve <b>el-müttekūn</b>.",
            ),
        ])
        .add_callout(Callout(
            "insight", "Hata Yapmayan Değil, Israr Etmeyen",
            "Âl-i İmrân 3/135, ahlâklı insanı tarif ederken önemli bir incelik taşır: ahlâklı "
            "insan <b>hata yapmayan</b> insan değil, hatasında <b>ısrar etmeyen</b> insandır — "
            "“bile bile işledikleri günah üzerinde ısrar etmezler”. Bu, Bölüm 2'deki "
            "<b>çift kutuplu insan</b> tasavvurunun doğrudan sonucudur.",
        ))
        .add_summary(
            "Dört ilke birbirinden bağımsız erdemler değil, tek bir sistemin ayaklarıdır: "
            "<b>adalet</b> hakkı yerine koyar, <b>sıdk</b> sözü hakikate bağlar, <b>merhamet</b> "
            "zayıfı gözetir, <b>sabır</b> ise bu üçünü zorluk anında ayakta tutar. Bakara 2/177 "
            "bu bütünlüğü tek bir ayette toplayıp “işte bunlar müttakīlerin ta kendileridir” der."
        )
    )

    # ======================================================================
    # BÖLÜM 4 — AHLÂKIN KELÂMÎ VE TASAVVUFÎ TEMELLERİ
    # ======================================================================
    ch4 = Chapter(
        number=4,
        title="Ahlâkın Kelâmî ve Tasavvufî Temelleri",
        subtitle="Değerin kaynağı akıl mı vahiy mi? Üç kelâm ekolü, tasavvufun cevabı ve nihaî gaye",
        key_terms=[
            KeyTerm("Mu'tezile'nin tezi", "Allah'ın <b>adalet ilkesinden</b> hareketle ahlâkî "
                                          "değerler <b>objektiftir</b>; akıl iyiyi kötüden ayırt eder."),
            KeyTerm("Eş'ariyye'nin tezi", "Ahlâkî değerin kaynağı <b>sadece din (vahiy)</b>; "
                                          "fiilin iyi/kötü oluşunu Allah'ın emir ve yasağı belirler."),
            KeyTerm("Mâtürîdiyye'nin konumu", "Allah'ın <b>irade ve kudretinin mutlaklığı</b> ile "
                                              "<b>ahlâkî kemali</b> aynı derecede dikkate alınır."),
            KeyTerm("Kalbin amelleri", "Tasavvufta güzel ahlâkın karşılığı: <b>ihlâs, niyet ve "
                                       "takvâ</b> gibi derunî haller."),
        ],
    )
    ch4.pages.append(
        ChapterPage()
        .add_terms(ch4.key_terms)
        .add_block(BulletBlock(
            1, "Tartışmanın Konusu",
            [
                "Kur'ân'daki ahlâkî ilkelerin <b>teorik temelleri</b>, kelâm ilminde "
                "<b>geniş tartışmalara</b> konu olmuştur.",
                "Tartışmanın ekseni şudur: ahlâkî değerin <b>kaynağı</b> nedir ve <b>akıl</b> "
                "iyi ile kötüyü kendi başına ayırt edebilir mi?",
            ],
        ))
        .add_table(ComparisonTable(
            "Üç kelâm ekolünün ahlâk anlayışı",
            ["Ölçüt", "Mu'tezile", "Eş'ariyye", "Mâtürîdiyye"],
            [
                ["Hareket noktası", "Allah'ın <b>adalet</b> ilkesi", "Allah'ın <b>emir ve yasağı</b>",
                 "Her ikisi <b>aynı derecede</b>"],
                ["Değerin kaynağı", "<b>Objektiftir</b>", "<b>Sadece din (vahiy)</b>",
                 "Fiilleri Allah yaratır, fakat bu yaratma <b>hikmetin dışına çıkmaz</b>"],
                ["Aklın rolü", "İyiyi kötüden <b>ayırt eder</b>", "Belirleyici değildir",
                 "Ahlâkî değerleri <b>kavrayacak güçte yaratılmıştır</b>"],
                ["İnsanın sorumluluğu", "—", "—",
                 "<b>Hür iradeye sahip</b> bir varlık olarak eylemlerinden <b>sorumludur</b>"],
            ],
        ))
        .add_callout(Callout(
            "caution", "“Orta Yol” Değil, İki İlkeyi Birden Koruma",
            "Mâtürîdiyye'nin konumu sık sık “iki görüş arasında orta yol” diye basitleştirilir; "
            "kaynağın ifadesi daha kesindir: Mâtürîdiyye iki hususu <b>aynı derecede dikkate "
            "almıştır</b>. Allah'ın mutlak kudreti korunur (fiilleri O yaratır), ama bu yaratma "
            "keyfî değildir (hikmetin dışına çıkmaz); dolayısıyla insan aklı ve iradesi "
            "anlamsız hâle gelmez.",
        ))
    )
    ch4.pages.append(
        ChapterPage()
        .add_block(BulletBlock(
            2, "Ahlâkın Tasavvuftaki Karşılığı",
            [
                "Tasavvufta güzel ahlâk, genel olarak <b>“kalbin amelleri”</b> şeklinde nitelenen "
                "<b>derunî hallerle</b> ilişkilendirilmiştir.",
                "Bu haller şunlardır: <b>ihlâs</b>, <b>niyet</b> ve <b>takvâ</b>.",
                "Sûfîlere göre tasavvuf, <b>“yalnızca ahlâktır”</b> veya <b>hüsnü'l-hulktan "
                "(güzel huy) ibarettir</b>.",
                "Kelâm ile tasavvuf birbirinin rakibi değildir: <b>kelâm</b> ahlâkî değerin "
                "<b>kaynağını ve bilinebilirliğini</b> tartışır; <b>tasavvuf</b> ise ahlâkın "
                "<b>yerini</b> (kalp) belirler ve onu dinin tamamına eşitler.",
            ],
        ))
        .add_block(BulletBlock(
            3, "Ahlâkın Nihaî Gayesi: Karşılık mı, Rızâ mı?",
            [
                "İslâm'da ahlâkî vazifeler <b>sadece dünyevî faydalarla değil, uhrevî "
                "karşılıklarla da desteklenmiştir</b>.",
                "Kur'ân'da <b>iyiler için cennet vaat edilmiş</b>, <b>kötüler cehennemle tehdit "
                "edilmiştir</b>.",
                "<b>Ancak</b> İslâm ahlâkının <b>en yüksek gayesi faydacı bir beklenti değil, "
                "Allah'ın hoşnutluğunu kazanmaktır</b>.",
                "Ahlâkî gelişim iki şartla mümkündür: insanın <b>gaye bakımından çıkar "
                "kaygılarını aşması</b> ve <b>cennet ümidi veya cehennem korkusunun ötesinde</b> "
                "her davranışını <b>Allah'ın rızasına uygunluk</b> açısından değerlendirmesi.",
            ],
        ))
        .add_callout(Callout(
            "focus", "Destek ile Gayeyi Karıştırmayın",
            "Kaynak, cennet vaadini ve cehennem tehdidini <b>inkâr etmez</b> — bunların ahlâkî "
            "vazifeleri <b>desteklediğini</b> açıkça söyler. Ayırdığı şey <b>destek</b> ile "
            "<b>gaye</b>dir: uhrevî karşılık ahlâkı destekleyen bir unsurdur, fakat ahlâkın en "
            "yüksek gayesi değildir. “İslâm ahlâkının nihaî gayesi nedir?” sorusunun cevabı "
            "<b>Allah'ın hoşnutluğudur</b>.",
        ))
        .add_summary(
            "Kelâm ahlâka <b>epistemolojik</b> olarak yaklaşır (değeri kim belirler, akıl mı "
            "vahiy mi?), tasavvuf <b>psikolojik</b> olarak yaklaşır (ahlâk kalpte oturur), "
            "gaye tartışması ise ahlâka <b>teleolojik</b> olarak yaklaşır (niçin ahlâklı "
            "olunur?). Üçünün ortak cevabı, ahlâkı insanın Allah'la ilişkisinin merkezine koyar."
        )
    )

    # ======================================================================
    # BÖLÜM 5 — PEYGAMBER AHLÂKI VE İBN ÂŞÛR'UN "HULK-İ AZÎM" TEFSİRİ
    # ======================================================================
    ch5 = Chapter(
        number=5,
        title="Peygamber Ahlâkı ve İbn Âşûr'un “Hulk-i Azîm” Tefsiri",
        subtitle="Tek bir harf-i cerden nübüvvetin ahlâkî gayesine: et-Tahrîr ve't-Tenvîr'den bir okuma",
        key_terms=[
            KeyTerm("Hulk-i azîm", "Ahlâk türü içinde <b>en kerim</b> olan; insan tabiatındaki "
                                   "övülmüş kemalin <b>en şiddetli derecesine</b> ulaşmış ahlâk."),
            KeyTerm("Mekârimü'l-ahlâk", "Üstün ahlâk; Peygamber'de <b>bir arada toplanmış</b> "
                                        "olması hulk-i azîmin sebebidir."),
            KeyTerm("Temekkün", "“Alâ” edatının bildirdiği mana: bir şeye <b>sağlamca yerleşmiş "
                                "olma, tam hâkimiyet</b>."),
            KeyTerm("Cevâmiu'l-kelim", "Peygamber'e has kılınan, <b>az sözle çok mana</b> ifade "
                                       "etme özelliği."),
        ],
    )
    ch5.pages.append(
        ChapterPage()
        .add_terms(ch5.key_terms)
        .add_person(IBN_ASUR)
        .add_ayat("Örnek Metnin Tefsir Ettiği Ayetler — el-Kalem 68/1-4", [
            Ayah(
                "Kalem 68/1-4",
                "ن وَالْقَلَمِ وَمَا يَسْطُرُونَ مَا أَنْتَ بِنِعْمَةِ رَبِّكَ بِمَجْنُونٍ وَإِنَّ لَكَ لَأَجْرًا غَيْرَ مَمْنُونٍ وَإِنَّكَ لَعَلَى خُلُقٍ عَظِيمٍ",
                "Nûn. Andolsun kaleme ve satır satır yazdıklarına ki, sen Rabbinin nimeti "
                "sayesinde bir deli değilsin. Şüphesiz sana tükenmez bir mükâfat vardır. Sen "
                "elbette yüce bir ahlâk üzeresin.",
                "<b>Memnûn:</b> Kesilen, tükenen. <b>Gayru memnûn</b> = tükenmez, başa kakılmaz.",
            ),
        ])
    )
    ch5.pages.append(
        ChapterPage()
        .add_ayat("Örnek Metin — Tâhir b. Âşûr, et-Tahrîr ve't-Tenvîr", [
            Ayah(
                "1 — Ayetin Siyakı: İftiranın Çürütülmesi",
                "وَبَعْدَ أَنْ آنَسَ نَفْسَ رَسُولِهِ بِالْوَعْدِ عَادَ إِلَى تَسْفِيهِ قَوْلِ الْأَعْدَاءِ، فَحَقَّقَ أَنَّهُ مُتَلَبِّسٌ بِخُلُقٍ عَظِيمٍ وَذَلِكَ ضِدُّ الْجُنُونِ، مُؤَكِّدًا ذَلِكَ بِثَلَاثَةِ مُؤَكِّدَاتٍ",
                "Allah, Resûlü'nün gönlünü vaat ile yatıştırdıktan sonra tekrar düşmanların "
                "sözünü akılsızlıkla nitelemeye döndü ve onun yüce bir ahlâka bürünmüş olduğunu "
                "kesinleştirdi; bu ise deliliğin zıddıdır. Bunu üç te'kit edatıyla pekiştirdi.",
                "<b>Üç te'kit:</b> <i>inne</i>, <i>lâm-ı ibtidâ</i> ve <b>isim cümlesi</b> yapısı. "
                "Hulk-i azîm burada soyut bir övgü değil, <b>somut bir iftiraya verilmiş cevaptır</b>.",
            ),
            Ayah(
                "2 — “Hulk” ve “Azîm” Kelimeleri",
                "وَالْخُلُقُ: طِبَاعُ النَّفْسِ، وَأَكْثَرُ إِطْلَاقِهِ عَلَى طِبَاعِ الْخَيْرِ إِذَا لَمْ يُتْبَعْ بِنَعْتٍ. وَالْعَظِيمُ: الرَّفِيعُ الْقَدْرِ، وَهُوَ مُسْتَعَارٌ مِنْ ضَخَامَةِ الْجِسْمِ",
                "“Hulk”: nefsin tabiatlarıdır; bir nitelemeyle birlikte kullanılmadığı takdirde "
                "çoğunlukla hayır tabiatları için kullanılır. “Azîm”: kadri yüce olan demektir; "
                "bu kelime cismin iriliğinden istiare yoluyla alınmıştır.",
                "Bu istiare o kadar yaygınlaşmıştır ki <b>hakikat (gerçek anlam) ile eşit hâle "
                "gelmiştir</b>.",
            ),
            Ayah(
                "3 — “Alâ” Harf-i Cerri: İstiʻlâ-i Mecâzî",
                "وَ(عَلَى) لِلِاسْتِعْلَاءِ الْمَجَازِيِّ الْمُرَادُ بِهِ التَّمَكُّنُ، كَقَوْلِهِ: أُولَئِكَ عَلَى هُدًى مِنْ رَبِّهِمْ",
                "“Alâ” edatı, kendisiyle temekkün (sağlamca yerleşmiş olma, tam hâkimiyet) "
                "kastedilen mecazî istiʻlâ içindir. Nitekim “İşte onlar Rablerinden gelen bir "
                "hidayet üzeredirler” (el-Bakara 2/5) sözü gibi.",
                "İbn Âşûr aynı kullanımı üç ayetle daha örnekler: <b>Neml 27/79</b>, "
                "<b>Zuhruf 43/43</b>, <b>Hac 22/67</b>. Ayet, Peygamber'in yüce ahlâka "
                "<b>sahip olduğunu</b> değil, ona <b>tam hâkim olduğunu</b> söyler.",
            ),
        ])
        .add_callout(Callout(
            "insight", "İki Yönlü Temekkün",
            "İbn Âşûr, “alâ” edatı üzerine kurduğu tahlili şöyle kapatır: Allah, Resûlü'nü yüce "
            "ahlâk üzere kıldığı gibi <b>şeriatını da</b> insanları yüce ahlâkla ahlâklanmaya "
            "sevk etmek için kılmıştır. Yani Peygamber yüce ahlâka <b>hem kendi nefsinde</b> "
            "hâkimdir (yaşar), <b>hem de dinî davetinde</b> (öğretir). Tek bir harf-i cerden "
            "başlayan tahlil, böylece <b>nübüvvetin ahlâkî gayesine</b> kadar genişler.",
        ))
    )
    ch5.pages.append(
        ChapterPage()
        .add_ayat("Örnek Metin — Devamı", [
            Ayah(
                "4 — Hz. Âişe'nin Cevabı",
                "وَفِي حَدِيثِ عَائِشَةَ: كَانَ خُلُقُهُ الْقُرْآنَ، أَيْ مَا تَضَمَّنَهُ الْقُرْآنُ مِنْ إِيقَاعِ الْفَضَائِلِ وَالْمَكَارِمِ وَالنَّهْيِ عَنْ أَضْدَادِهَا",
                "Hz. Âişe hadisinde: “Onun ahlâkı Kur'ân'dı” — yani Kur'ân'ın ihtivâ ettiği "
                "faziletleri ve kerem sahibi davranışları gerçekleştirmek, bunların zıtlarından "
                "ise nehyetmek demektir.",
                "Hz. Âişe sözünü şöyle sürdürür: <b>“Sen ‘Kad efleha'l-mü'minûn' (el-Mü'minûn "
                "23/1) ayetini ve devamındaki on ayeti okumuyor musun?”</b> — Peygamber'in "
                "ahlâkı, Kur'ân'ın mü'min tarifinin <b>yaşayan hâlidir</b>.",
            ),
            Ayah(
                "5 — Şeriatın Ahlâkî Gayesi",
                "قَالَ رَسُولُ اللَّهِ: إِنَّمَا بُعِثْتُ لِأُتَمِّمَ مَكَارِمَ الْأَخْلَاقِ، فَجَعَلَ أَصْلَ شَرِيعَتِهِ إِكْمَالَ مَا يَحْتَاجُهُ الْبَشَرُ مِنْ مَكَارِمِ الْأَخْلَاقِ فِي نُفُوسِهِمْ",
                "Allah Resûlü şöyle buyurmuştur: “Ben ancak üstün ahlâkı (mekârimü'l-ahlâk) "
                "tamamlamak için gönderildim.” Böylece şeriatının aslını, insanların "
                "nefislerinde üstün ahlâk adına muhtaç oldukları şeyi kemale erdirmek kılmıştır.",
                "İbn Âşûr için <b>ahlâk, şeriatın bir konusu değil, gayesidir</b>.",
            ),
        ])
        .add_table(ComparisonTable(
            "İbn Âşûr'un ayrımı: güzel ahlâk ile yüce ahlâk",
            ["Ölçüt", "el-Hulku'l-hasen (güzel ahlâk)", "el-Hulku'l-azîm (yüce ahlâk)"],
            [
                ["Derecesi", "Mutlak/genel güzel ahlâk", "<b>Daha üstün</b> (<i>erfa'</i>)"],
                ["Kapsamı", "Tek tek güzel huylar",
                 "<b>Mekârimü'l-ahlâkın Peygamber'de bir arada toplanması</b>"],
                ["Ölçütü", "Güzel davranış",
                 "<b>Hâller değişse de</b> muamelenin güzelliğinin bozulmaması"],
            ],
        ))
        .add_block(BulletBlock(
            1, "Hulk-i Azîmin Muhtevası: On Sekiz Haslet",
            [
                "<b>1-6:</b> Dindarlık · hakikatlerin bilgisi · nefsin hilmi (yumuşaklığı) · "
                "adalet · meşakkatlere sabır · iyilik edenin iyiliğini teslim etmek",
                "<b>7-12:</b> Tevazu · zühd · iffet · af · cömertlik · hayâ",
                "<b>13-18:</b> Şecaat · güzel bir şekilde susmak · teennî (acele etmemek) · "
                "vakar · merhamet · muamele ile muaşeretin güzelliği",
                "Dikkat: listenin <b>ilk iki maddesi eylem değil, hâl ve bilgidir</b> — "
                "<b>dindarlık</b> ve <b>hakikatlerin bilgisi</b>. İbn Âşûr'a göre yüce ahlâk, "
                "<b>doğru inanç ve doğru bilgi</b> üzerine kurulur; davranış hasletleri bundan "
                "sonra gelir.",
            ],
            subtitle="İbn Âşûr'un “cümâʻu'l-hulki'l-azîm” dediği toplam",
        ))
    )
    ch5.pages.append(
        ChapterPage()
        .add_block(BulletBlock(
            2, "Ahlâk Nerede Gizlidir, Nerede Görünür?",
            [
                "<b>Ahlâk nefiste gizlidir (kâmine)</b>; onun <b>tezahürleri</b> ise sahibinin "
                "tasarruflarıdır.",
                "<b>Tezahür alanları:</b> konuşması · yüzünün açıklığı (güler yüzlülük) · sebatı · "
                "hükmü · hareketi ve durgunluğu · yemesi ve içmesi · ailesini ve gözetimi "
                "altındakileri terbiye etmesi.",
                "<b>Buna bağlı sonuçlar:</b> insanlar nezdinde saygınlık kazanması, hakkında "
                "güzel şekilde övgüyle söz edilmesi ve iyi bir şöhrete sahip olması.",
                "<b>Peygamber'deki tezahürleri</b> bunların hepsinde, ayrıca <b>ümmetini "
                "yönetmesinde (siyasetinde)</b> ve kendisine has kılınan <b>konuşmasının "
                "fesâhati</b> ile <b>cevâmiu'l-kelimde</b> görülür.",
            ],
        ))
        .add_summary(
            "Pasajın kapanışı, ünitenin en başındaki ıstılah tanımıyla birebir örtüşür: orada "
            "ahlâk “davranışların kaynağı mahiyetindeki ruhî melekeler” diye tanımlanmıştı, "
            "burada İbn Âşûr “ahlâk nefiste gizlidir, tezahürleri ise tasarruflarıdır” diyor. "
            "İkisi aynı şeyi söyler: <b>ahlâk görünmez, ahlâkın izleri görünür</b> — ve bu izler "
            "insanın en gösterişsiz anlarında (yemesinde, susmasında, yüz ifadesinde) ölçülür."
        )
    )

    chapters = [ch1, ch2, ch3, ch4, ch5]

    # ======================================================================
    # KAVRAMLAR SÖZLÜĞÜ
    # ======================================================================
    glossary = [
        Concept("Ahlâk", "“Seciye, tabiat, huy” anlamlarındaki <i>hulukun</i> kelimesinin çoğulu.",
                "Lügat", 1),
        Concept("Istılahî ahlâk", "Tutum ve davranışların kaynağı mahiyetindeki ruhî ve mânevî melekeler.",
                "Tanım", 1),
        Concept("Mürûe (mürüvvet)", "Câhiliye Araplarında “ahlâk” yerine daha çok kullanılan tabir.",
                "Câhiliye", 1),
        Concept("Fahr", "Kabile gururu; Câhiliye ahlâkının temelindeki üç duygudan biri.", "Câhiliye", 1),
        Concept("Mecd", "Şeref; Câhiliye ahlâkının temelindeki üç duygudan biri.", "Câhiliye", 1),
        Concept("Gazap", "Öfke; Câhiliye ahlâkının temelindeki üç duygudan biri.", "Câhiliye", 1),
        Concept("Şecaat · Kerem · Vefâ", "Câhiliye'de mevcut olan, fakat kabileci ve dünyevî bir "
                "karakterle sınırlı kalan erdemler.", "Câhiliye", 1),
        Concept("Ahsen-i takvîm", "İnsanın en güzel bir tabiatta yaratılmış olması.", "İnsan tasavvuru", 2),
        Concept("Fücûr", "Allah'ın insan nefsine ilham ettiği kötülük kutbu.", "İnsan tasavvuru", 2),
        Concept("Takvâ", "Aynı nefse ilham edilen, kötülükten sakınma yeteneği.", "İnsan tasavvuru", 2),
        Concept("Kur'ân ahlâkı", "Hz. Âişe'nin, Hz. Peygamber'in ahlâkını nitelerken kullandığı ifade.",
                "Hz. Âişe", 2),
        Concept("Ma'rûf", "Akıl ve dinin iyi kabul ettiği, toplumun ortak vicdanında güzel "
                "karşılanan her şey.", "Lokmân 31/17", 2),
        Concept("Hevnen", "Kendini beğenmişlikten uzak, ağırbaşlı ve mütevazı bir duruş.",
                "Furkān 25/63", 2),
        Concept("Adalet", "Güzel ahlâkın temel direği; Kur'ân onu takvâya en yakın davranış olarak niteler.",
                "Dört ilke", 3),
        Concept("Sıdk", "Doğruluk; İslâm ahlâkının özü ve insanı cennete götüren yol.", "Dört ilke", 3),
        Concept("Merhamet ve yardımseverlik", "Yetimi azarlamamak, isteyeni geri çevirmemek; "
                "toplumsal sorumluluk bilincinin tezahürü.", "Dört ilke", 3),
        Concept("Sabır ve hoşgörü", "Kötülüğü en güzel şekilde savmak ve zorluk karşısında "
                "metaneti korumak.", "Dört ilke", 3),
        Concept("Bağy", "Haddi aşma, azgınlık; Nahl 16/90'da yasaklanan üç şeyden biri.", "Nahl 16/90", 3),
        Concept("Fahşâ", "Hayâsızlık; Nahl 16/90'da yasaklanan üç şeyden biri.", "Nahl 16/90", 3),
        Concept("İhsân", "İyilik yapmak; Nahl 16/90'da emredilen üç şeyden biri.", "Nahl 16/90", 3),
        Concept("Kavl-i sedîd", "Hedefi tam tutturan, isabetli ve sağlam söz.", "Ahzâb 33/70", 3),
        Concept("Kâzımîne'l-gayz", "Öfkesini yutup içeride tutanlar; öfkenin yokluğu değil, ona hâkim olmak.",
                "Âl-i İmrân 3/134", 3),
        Concept("Birr", "Kapsayıcı iyilik; Bakara 2/177'de iman, infak, ibadet, ahde vefa ve "
                "sabrın birlikteliği olarak tanımlanır.", "Bakara 2/177", 3),
        Concept("Mu'tezile'nin tezi", "Ahlâkî değerler objektiftir; akıl iyiyi kötüden ayırt edebilir.",
                "Kelâm", 4),
        Concept("Eş'ariyye'nin tezi", "Ahlâkî değerin kaynağı sadece dindir; fiilin iyi/kötü oluşunu "
                "Allah'ın emir ve yasağı belirler.", "Kelâm", 4),
        Concept("Mâtürîdiyye'nin konumu", "Allah'ın irade ve kudretinin mutlaklığı ile ahlâkî kemali "
                "aynı derecede dikkate alınır; yaratma hikmetin dışına çıkmaz.", "Kelâm", 4),
        Concept("Kalbin amelleri", "Tasavvufta güzel ahlâkın karşılığı: ihlâs, niyet ve takvâ gibi "
                "derunî haller.", "Tasavvuf", 4),
        Concept("Hüsnü'l-hulk", "Güzel huy; sûfîlere göre tasavvufun kendisi bundan ibarettir.",
                "Tasavvuf", 4),
        Concept("Hulk-i azîm", "Ahlâk türü içinde en kerim olan; insan tabiatındaki övülmüş kemalin "
                "en şiddetli derecesine ulaşmış ahlâk.", "İbn Âşûr", 5),
        Concept("Mekârimü'l-ahlâk", "Üstün ahlâk; Peygamber'de bir arada toplanmış olması hulk-i "
                "azîmin sebebidir.", "İbn Âşûr", 5),
        Concept("Temekkün", "“Alâ” edatının bildirdiği mana: bir şeye sağlamca yerleşmiş olma, "
                "tam hâkimiyet.", "İbn Âşûr", 5),
        Concept("İstiʻlâ-i mecâzî", "“Alâ” edatının hakiki üstte olma değil, mecazî hâkimiyet bildirmesi.",
                "İbn Âşûr", 5),
        Concept("Cevâmiu'l-kelim", "Peygamber'e has kılınan, az sözle çok mana ifade etme özelliği.",
                "İbn Âşûr", 5),
        Concept("et-Tahrîr ve't-Tenvîr", "İbn Âşûr'un, Kur'an'ı dilsel, edebî, tarihsel ve fıkhî "
                "boyutlarıyla ele alan kapsamlı tefsiri.", "Tâhir b. Âşûr", 5),
        Concept("Makâsıdü'ş-şerîa", "İbn Âşûr'un, şeriatın temel gayelerini sistematik biçimde ele "
                "aldığı eseri.", "Tâhir b. Âşûr", 5),
    ]

    # ======================================================================
    # TEST + CEVAP ANAHTARI
    # ======================================================================
    test_questions = [
        TestQuestion(1, "“Ahlâk” kelimesi, Arapça'da “seciye, tabiat, huy” anlamlarına gelen "
                        "hangi kelimenin çoğuludur?",
                     {"A": "Hulk (hulukun)", "B": "Halk", "C": "Hilkat", "D": "Mürûe", "E": "Sıdk"}),
        TestQuestion(2, "Ahlâkın ıstılahî tanımı aşağıdakilerden hangisidir?",
                     {"A": "Toplumun onayladığı davranış kalıplarının tamamı",
                      "B": "Tutum ve davranışların kaynağı mahiyetindeki ruhî ve mânevî melekeler",
                      "C": "Dinin emir ve yasaklarının pratiğe dökülmüş hâli",
                      "D": "Kişinin dış dünyada sergilediği davranışların bütünü",
                      "E": "Kalbin, aklın denetiminden bağımsız eğilimleri"}),
        TestQuestion(3, "Câhiliye dönemi Araplarında “ahlâk” kavramı yerine daha çok kullanılan "
                        "tabir hangisidir?",
                     {"A": "Takvâ", "B": "Birr", "C": "Mürûe (mürüvvet)", "D": "İhsân", "E": "Fütüvvet"}),
        TestQuestion(4, "Kaynağa göre Câhiliye ahlâkının temelinde tatmin edilmek istenen üç duygu "
                        "aşağıdakilerden hangisinde birlikte verilmiştir?",
                     {"A": "Fahr – mecd – gazap", "B": "Şecaat – kerem – vefâ",
                      "C": "Fücûr – takvâ – sıdk", "D": "Adl – ihsân – bağy",
                      "E": "İhlâs – niyet – takvâ"}),
        TestQuestion(5, "Câhiliye'deki şecaat, kerem ve vefâ gibi erdemlerin temel sınırlılığı nedir?",
                     {"A": "Yalnızca savaş zamanlarında geçerli olmaları",
                      "B": "Kabileci ve dünyevî bir karakterle sınırlı kalmaları",
                      "C": "Kadınları kapsam dışında bırakmaları",
                      "D": "Yazılı bir metne dayanmamaları",
                      "E": "Sadece kabile reislerinden beklenmeleri"}),
        TestQuestion(6, "İslâm'ın, Câhiliye geleneklerinin karşısında insana sunduğu gayenin iki "
                        "bileşeni aşağıdakilerden hangisidir?",
                     {"A": "Şeref kazanmak ve kabileyi yüceltmek",
                      "B": "Cennete girmek ve cehennemden korunmak",
                      "C": "Allah'ın rızasını hedeflemek ve nefsi dizginlemek",
                      "D": "Aklı işletmek ve tabiatı incelemek",
                      "E": "İlim tahsil etmek ve infakta bulunmak"}),
        TestQuestion(7, "Hz. Âişe, Hz. Peygamber'in ahlâkını nasıl nitelemiştir?",
                     {"A": "“Mürüvvetin zirvesi”", "B": "“Kur'ân ahlâkı”",
                      "C": "“Sabır ve şükür ahlâkı”", "D": "“Câhiliye'nin zıddı”",
                      "E": "“Peygamberlerin ortak ahlâkı”"}),
        TestQuestion(8, "Kur'ân'a göre insanı ahlâkî bakımdan “çift kutuplu” kılan husus nedir?",
                     {"A": "Meleklerden üstün kılınmış olması",
                      "B": "Kendisine isimlerin öğretilmiş olması",
                      "C": "Topraktan gelen beşerî cephesi",
                      "D": "Halife olarak yaratılmış olması",
                      "E": "Ölümlü bir varlık olması"}),
        TestQuestion(9, "Kur'ân'da Allah'ın insan nefsine ilham ettiği belirtilen iki şey nedir?",
                     {"A": "Akıl ve irade", "B": "Hayır ve şer bilgisi",
                      "C": "Fücûr ve takvâ", "D": "Sıdk ve kizb", "E": "İman ve amel"}),
        TestQuestion(10, "Kaynağa göre Kur'ân'da güzel ahlâk nasıl sunulmuştur?",
                      {"A": "Mücerret bir davranış biçimi olarak",
                       "B": "İman ve ibadetle iç içe geçmiş bir sistem olarak",
                       "C": "Yalnızca toplumsal bir düzen aracı olarak",
                       "D": "İbadetlerden tamamen bağımsız bir alan olarak",
                       "E": "Sadece peygamberlere mahsus bir hâl olarak"}),
        TestQuestion(11, "Namazın insanı hayâsızlıktan ve kötülükten alıkoyduğu hangi sûrede "
                         "belirtilmiştir?",
                      {"A": "Bakara", "B": "Lokmân", "C": "Ankebût", "D": "Nahl", "E": "Kalem"}),
        TestQuestion(12, "Kaynağa göre oruç ibadeti, bireyin ahlâkî kontrolünü geliştirmeyi hangi "
                         "iki hususu teşvik ederek amaçlar?",
                      {"A": "Sabır ve merhamet", "B": "Adalet ve doğruluk",
                       "C": "Zühd ve iffet", "D": "İhlâs ve niyet", "E": "Şecaat ve vefâ"}),
        TestQuestion(13, "Kur'ân, adaleti hangi nitelemeyle takdim eder?",
                      {"A": "İbadetlerin en faziletlisi", "B": "Takvâya en yakın davranış",
                       "C": "İmanın yarısı", "D": "Sabrın bir türü", "E": "Nübüvvetin şartı"}),
        TestQuestion(14, "Kaynağa göre İslâm ahlâkının “özü” olarak nitelenen ilke hangisidir?",
                      {"A": "Adalet", "B": "Sabır", "C": "Merhamet",
                       "D": "Doğruluk (sıdk)", "E": "Tevazu"}),
        TestQuestion(15, "Aşağıdaki eşleştirmelerden hangisi kaynağa göre YANLIŞTIR?",
                      {"A": "Mu'tezile — Ahlâkî değerler objektiftir, akıl iyiyi kötüden ayırt edebilir",
                       "B": "Eş'ariyye — Ahlâkî değerin kaynağı sadece din (vahiy)dir",
                       "C": "Mâtürîdiyye — İnsan hür iradeye sahip bir varlık olarak eylemlerinden sorumludur",
                       "D": "Mu'tezile — Hareket noktası Allah'ın adalet ilkesidir",
                       "E": "Eş'ariyye — İnsan fiillerinin yaratıcısı insanın kendi iradesidir"}),
        TestQuestion(16, "Mâtürîdiyye'nin kulların fiilleri konusundaki konumu için kaynakta ne "
                         "söylenmektedir?",
                      {"A": "Yalnızca Eş'ariyye'nin görüşünü benimsemiştir",
                       "B": "Yalnızca Mu'tezile'nin görüşünü benimsemiştir",
                       "C": "Allah'ın irade-kudretinin mutlaklığı ile ahlâkî kemalini aynı derecede "
                            "dikkate almıştır",
                       "D": "Konuyu tartışma dışı bırakmıştır",
                       "E": "İnsan fiillerinin yaratılmadığını savunmuştur"}),
        TestQuestion(17, "Tasavvufta güzel ahlâk, “kalbin amelleri” şeklinde nitelenen hangi derunî "
                         "hallerle ilişkilendirilmiştir?",
                      {"A": "İhlâs, niyet ve takvâ", "B": "Zühd, vera ve rıza",
                       "C": "Havf, recâ ve tevekkül", "D": "Sabır, şükür ve kanaat",
                       "E": "Fakr, fenâ ve bekā"}),
        TestQuestion(18, "Kaynağa göre Kur'ân'da mekârimü'l-ahlâkın zirve örnekleri olarak sunulan "
                         "peygamberler ve vasıfları hangisidir?",
                      {"A": "Hz. Nuh'un sabrı, Hz. Musa'nın cesareti",
                       "B": "Hz. Yusuf'un iffeti ve sabrı, Hz. İbrahim'in misafirperverliği ve sadakati",
                       "C": "Hz. İsa'nın zühdü, Hz. Davud'un adaleti",
                       "D": "Hz. Eyyub'un sabrı, Hz. Süleyman'ın şükrü",
                       "E": "Hz. Âdem'in tevbesi, Hz. Yakub'un tevekkülü"}),
        TestQuestion(19, "Kaynağa göre İslâm ahlâkının en yüksek gayesi nedir?",
                      {"A": "Cennete girmek", "B": "Cehennemden korunmak",
                       "C": "Toplumsal huzuru sağlamak", "D": "Allah'ın hoşnutluğunu kazanmak",
                       "E": "Dünyevî faydayı en üst düzeye çıkarmak"}),
        TestQuestion(20, "İbn Âşûr'a göre “ve inneke le-alâ hulukin azîm” ayetindeki “alâ” edatı "
                         "hangi manayı bildirir?",
                      {"A": "Hakiki üstte bulunma", "B": "Sebebiyet",
                       "C": "Temekkün (sağlamca yerleşmiş olma, tam hâkimiyet)",
                       "D": "İstisna", "E": "Beraberlik"}),
    ]

    answer_key_items = [
        AnswerItem(1, "A", "<b>Hulk (hulukun).</b> Ahlâk, “seciye, tabiat, huy” anlamlarına gelen "
                           "<i>hulukun</i> kelimesinin çoğuludur."),
        AnswerItem(2, "B", "Istılahta ahlâk, <b>tutum ve davranışların kaynağı mahiyetindeki ruhî "
                           "ve mânevî melekelerdir</b>. D şıkkı davranışın kendisini tarif ettiği "
                           "için yanlıştır; ahlâk davranışın kaynağıdır."),
        AnswerItem(3, "C", "<b>Mürûe (mürüvvet).</b> Câhiliye Araplarında “ahlâk” yerine daha çok "
                           "bu tabir kullanılmıştır."),
        AnswerItem(4, "A", "<b>Fahr (kabile gururu), mecd (şeref) ve gazap (öfke).</b> B şıkkındaki "
                           "şecaat-kerem-vefâ ise Câhiliye'nin <i>erdemleridir</i>, temelindeki "
                           "duygular değil."),
        AnswerItem(5, "B", "Bu erdemler mevcuttu, fakat <b>kabileci ve dünyevî bir karakterle "
                           "sınırlı kalmıştır</b>."),
        AnswerItem(6, "C", "<b>Allah'ın rızasını hedeflemek</b> ve <b>insanın nefsini dizginlemesi</b> "
                           "— bu ikisi birlikte ferdî ve sosyal planda ahlakî yücelmenin ölçüsüdür."),
        AnswerItem(7, "B", "Hz. Âişe, Hz. Peygamber'in ahlâkının <b>“Kur'ân ahlâkı”</b> olduğunu "
                           "belirtmiştir."),
        AnswerItem(8, "C", "Kur'ân insanı ahsen-i takvîm üzere ve ilahî ruhtan üflenmiş olarak "
                           "tanımlar; ancak <b>topraktan gelen beşerî cephesi</b> onu ahlâkî "
                           "bakımdan çift kutuplu kılmıştır."),
        AnswerItem(9, "C", "<b>Fücûr (kötülük)</b> ve <b>takvâ (ondan sakınma yeteneği)</b>. "
                           "Nefsini temiz tutan kurtuluşa erer, kirleten hüsrana uğrar."),
        AnswerItem(10, "B", "Güzel ahlâk, <b>mücerret bir davranış biçimi olarak değil, iman ve "
                            "ibadetle iç içe geçmiş bir sistem</b> olarak sunulmuştur."),
        AnswerItem(11, "C", "<b>Ankebût</b> Sûresi (29/45). Kaynak, bunun namazın ahlâkî bir "
                            "dönüşüm aracı olduğunun kanıtı olduğunu belirtir."),
        AnswerItem(12, "A", "Oruç, <b>sabrı ve merhameti</b> teşvik ederek bireyin ahlâkî "
                            "kontrolünü geliştirmeyi amaçlar."),
        AnswerItem(13, "B", "Kur'ân adaleti <b>takvâya en yakın davranış</b> olarak niteler "
                            "(el-Mâide 5/8)."),
        AnswerItem(14, "D", "<b>Doğruluk (sıdk)</b> İslâm ahlâkının özüdür. Adalet ise güzel "
                            "ahlâkın <i>temel direği</i> olarak nitelenir — iki ifade "
                            "karıştırılmamalıdır."),
        AnswerItem(15, "E", "<b>Yanlış olan E'dir.</b> Eş'ariyye'ye göre fiilin iyi veya kötü "
                            "oluşunu Allah'ın emir ve yasağı belirler; “insan fiillerinin "
                            "yaratıcısı insanın kendi iradesidir” görüşü Eş'ariyye'ye ait değildir."),
        AnswerItem(16, "C", "Mâtürîdiyye, <b>Eş'ariyye'nin öne çıkardığı Allah'ın irade ve "
                            "kudretinin mutlaklığı</b> ile <b>Mu'tezile'nin ağırlık verdiği "
                            "Allah'ın mutlak ve müteâl ahlâkî kemalini</b> aynı derecede dikkate "
                            "almıştır."),
        AnswerItem(17, "A", "<b>İhlâs, niyet ve takvâ.</b> Sûfîlere göre tasavvuf “yalnızca "
                            "ahlâktır” veya hüsnü'l-hulktan ibarettir."),
        AnswerItem(18, "B", "<b>Hz. Yusuf'un iffeti ve sabrı</b> ile <b>Hz. İbrahim'in "
                            "misafirperverliği ve sadakati</b>."),
        AnswerItem(19, "D", "<b>Allah'ın hoşnutluğunu kazanmak.</b> Cennet vaadi ve cehennem "
                            "tehdidi ahlâkî vazifeleri <i>destekler</i>, fakat en yüksek "
                            "<i>gaye</i> değildir."),
        AnswerItem(20, "C", "<b>Temekkün.</b> İbn Âşûr'a göre “alâ” burada istiʻlâ-i mecâzî için "
                            "olup tam hâkimiyet bildirir; Peygamber yüce ahlâka hem nefsinde hem "
                            "dinî davetinde hâkimdir."),
    ]

    return CoursePack(
        ders_klasoru="TEFSİR II",
        course_code="TEFSİR II · 6. ÜNİTE",
        title="Kur'ân'da Güzel <span class=\"accent-word\">Ahlâk</span>",
        subtitle="Tefsir II — 6. Ünite · Kavramdan Tefsire Bütün Bir Ahlâk Nizamı",
        subtitle_short="Kur'ân'da Güzel Ahlâk",
        description="Ahlâk kelimesinin lügat kökünden Câhiliye'nin mürüvvet anlayışına, Kur'ân'ın "
                    "çift kutuplu insan tasavvurundan dört evrensel ahlâk ilkesine, kelâm "
                    "ekollerinin değer tartışmasından Tâhir b. Âşûr'un “hulk-i azîm” tefsirine "
                    "kadar 6. ünitenin tamamı.",
        theme="burgundy",
        theme_color="#7A2438",
        icon_text="A",
        chapters=chapters,
        glossary=glossary,
        persons={IBN_ASUR.id: IBN_ASUR},
        test_title="Genel Değerlendirme Testi",
        test_subtitle="Kavramsal çerçeveden örnek metne, 6. ünite üzerine kapsamlı çoktan seçmeli test",
        test_instructions="Aşağıdaki soruların her birinde beş seçenekten yalnızca biri doğrudur. "
                          "Cevaplarınızı işaretledikten sonra Cevap Anahtarı bölümündeki çözümlerle "
                          "karşılaştırınız.",
        test_questions=test_questions,
        answer_key_intro="Her sorunun doğru cevabı, kaynak metindeki dayanağıyla birlikte aşağıda "
                         "verilmiştir. Özellikle karıştırılmaya müsait ayrımlara dikkat ediniz.",
        answer_key_items=answer_key_items,
        overview_lead="Bu ünite, ahlâkı tek bir yerden değil, <b>beş ayrı katmandan</b> ele alır: "
                      "kelimenin lügat kökü, Câhiliye'nin devraldığı miras, Kur'ân'ın insan "
                      "tasavvuru, dört evrensel ilke ve nihayet bir müfessirin tek bir ayet "
                      "üzerinden kurduğu bütünlüklü okuma. Ünitenin ana tezi baştan sona aynıdır: "
                      "<b>ahlâk, dinin yanında duran bir konu değil, dinin kendisini gösterdiği yerdir.</b>",
        overview_cards=[
            {"title": "Kavramın Kökü",
             "text": "Ahlâk, “seciye, tabiat, huy” anlamındaki <i>hulukun</i>'un çoğuludur. "
                     "Istılahta ise davranışın kendisi değil, <b>davranışı doğuran iç yeti</b>dir."},
            {"title": "Câhiliye Mirası",
             "text": "Câhiliye'de erdem vardı (şecaat, kerem, vefâ) ama gayesi fahr, mecd ve "
                     "gazaptı. İslâm <b>listeyi değil gayeyi</b> değiştirdi."},
            {"title": "Çift Kutuplu İnsan",
             "text": "Ahsen-i takvîm üzere yaratılan insanın topraktan gelen cephesi, ona "
                     "<b>fücûr ve takvâyı</b> birlikte verir. Ahlâkı mümkün kılan da budur."},
            {"title": "Dört Evrensel İlke",
             "text": "<b>Adalet</b> (takvâya en yakın), <b>sıdk</b> (ahlâkın özü), <b>merhamet</b> "
                     "(toplumsal sorumluluk) ve <b>sabır</b> (zorlukta metanet)."},
            {"title": "Kelâm ve Tasavvuf",
             "text": "Mu'tezile aklı, Eş'ariyye vahyi öne çıkarır; Mâtürîdiyye ikisini "
                     "<b>aynı derecede</b> dikkate alır. Tasavvuf ise ahlâkı <b>kalbe</b> yerleştirir."},
            {"title": "Hulk-i Azîm",
             "text": "İbn Âşûr, tek bir harf-i cerden (“alâ”) yola çıkıp <b>şeriatın gayesinin "
                     "mekârimü'l-ahlâkı tamamlamak</b> olduğu sonucuna varır."},
        ],
        overview_flow=[
            ("Kavram", "Hulukun → ahlâk"),
            ("Miras", "Câhiliye'nin mürüvveti"),
            ("İnsan", "Fücûr ve takvâ"),
            ("İlkeler", "Adalet · sıdk · merhamet · sabır"),
            ("Tefsir", "Hulk-i azîm"),
        ],
        overview_note="Kaynak, <b>“adalet”</b> için “güzel ahlâkın "
                      "<i>temel direği</i>”, <b>“doğruluk (sıdk)”</b> için ise “İslâm ahlâkının "
                      "<i>özü</i>” ifadesini kullanır — bu iki niteleme birbirinin yerine "
                      "yazılmamalıdır. Aynı şekilde uhrevî karşılık ahlâkı <b>destekler</b>, "
                      "fakat ahlâkın en yüksek <b>gayesi</b> Allah'ın hoşnutluğudur.",
    )
