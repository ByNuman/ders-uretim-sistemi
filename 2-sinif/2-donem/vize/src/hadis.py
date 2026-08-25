# -*- coding: utf-8 -*-
"""HADİS (VİZE) — Görsel Ders Notu Kitabı, içerik tanımı.

Kaynak: 'kaynaklar/ders_kaynaklari/HADİS/Hadis Metinleri.pdf' (Metûnü'l-Hadîs,
51 sayfa, 3 kitâb / 114 rivayet). Bu ders notu VİZE KAPSAMINI işler:
    Kitâbü'l-İlm 1–22  (s. 2–12, 12 bâb, 22 rivayet)
Final kapsamı 23. rivayetten başlar ve ayrı bir kitaptır
(bkz. 2-sinif/2-donem/final/src/hadis.py).

TEKNİK NOT (Arapça metnin çıkarılması):
  * pdfplumber ve PyMuPDF bu PDF'te ligatürleri BOZUYOR; Poppler'ın
    `pdftotext -enc UTF-8` çıktısı ligatürleri DOĞRU çözüyor — Arapça
    metinlerin tamamı bu yolla alınmıştır.
  * Kaynak fontun kendi eksiklikleri elle tamamlandı: "الل"→"الله",
    "ي"→"يا", "النب"→"النبي", "ث"→"ثم", "ف"→"في", "ل"→"لي",
    "نئم"→"نائم", "أخبرن"→"أخبرنا", "يحي"→"يحيى", "وأثن"→"وأثنى",
    "قبورن"→"قبورنا", "وعندن كناب"→"وعندنا كتاب", "اتئوني"→"ائتوني".
  * Metinler ayrıca tam harekeli hâle getirildi; senedler kısaltıldı,
    kaynağın isnad örneği olarak tam verdiği yerlerde korundu.
  * Rivayetler `Ayah` kartıyla (Arapça + tercüme + kaynak/şerh notu)
    render edilir.
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
# SAHÂBÎLER VE ÂLİMLER (TEK KAYNAK) — tarihler/eserler yalnızca burada tanımlanır
# ---------------------------------------------------------------------------

EBU_ZERR = Person(
    id="ebu_zerr", name="Ebû Zerr el-Gıfârî", years="?–652 (h. 32)",
    tagline="Samsâme Sözünün Sahibi — Mevkūf Rivayetin Ders İçindeki İlk Örneği",
    bio=["Gıfâr kabilesine mensup, ilk müslümanlardan ve <b>zühd hayatının</b> sahâbe içindeki en belirgin "
         "temsilcilerindendir. Kitâbü'l-İlm'in ikinci rivayetinde, <b>ensesine keskin kılıç (samsâme) "
         "dayansa bile</b> Hz. Peygamber'den işittiği bir sözü ulaştırmaktan vazgeçmeyeceğini söyler. "
         "Kitabın dipnotu bu rivayeti özellikle işaretler: söz <b>bir sahâbîye nispet edildiği için "
         "hadis mevkūftur</b>. Bu yönüyle metin hem <b>tebliğ cesaretinin</b> hem de <b>rivayet "
         "türü tasnifinin</b> ilk örneği olarak okunur."],
    key_work="Samsâme sözü (Buhârî, İlm, 10) — mevkūf örneği", initials="EZ",
)
IBN_MESUD = Person(
    id="ibn_mesud", name="Abdullah b. Mes'ûd", years="?–653 (h. 32)",
    tagline="Öğretimde Ölçüyü Sahâbe Pratiğine Taşıyan Âlim — Ebû Abdirrahmân",
    bio=["İlk müslümanlardandır; Hz. Peygamber'e yakınlığı ve Kur'an bilgisiyle tanınır, künyesi "
         "<b>Ebû Abdirrahmân</b>'dır. Bu ünitede üç ayrı yerde karşımıza çıkar: Hz. Peygamber'in "
         "<b>usanç gelmesin diye öğüdü günlere yaydığını</b> haber verir (İlim 6), aynı ölçüyü kendisi "
         "uygulayarak <b>insanlara yalnızca perşembe günleri</b> ders verir (İlim 7) ve <b>“iki şey "
         "dışında gıbta yoktur”</b> hadisini rivayet eder (İlim 11). Ayrıca bâbın sonundaki âsârda, "
         "“amellerin en faziletlisi hangisidir?” sorusuna ısrarla <b>“ilim”</b> cevabını verir."],
    key_work="İlim 6–7–11 rivayetleri — sünnetin sahâbî pratiğine yansıması", initials="İM",
)
EBU_MUSA = Person(
    id="ebu_musa", name="Ebû Mûsâ el-Eş'arî", years="?–665 (h. 44 civarı)",
    tagline="Yağmur Meselinin Râvisi — Yemen Valisi ve Kur'an Okuyucusu",
    bio=["Yemen asıllı sahâbîdir; Habeşistan'a hicret edenler arasında sayılır, sonra Medine'ye gelmiştir. "
         "Hz. Peygamber onu <b>Muâz b. Cebel ile birlikte Yemen'e</b> göndermiştir. Güzel sesi ve Kur'an "
         "okuyuşuyla tanınır. Bu ünitede, ilmin üç farklı insan tipinde bıraktığı izi anlatan "
         "<b>yağmur meselinin</b> (nakıyye–ecâdib–kî'ân) râvisidir; kaynak, dipnotta hakkında ayrıca "
         "<b>bilgi edinilmesini</b> ister."],
    key_work="Yağmur meseli (Buhârî, İlm, 20)", initials="EM",
)
EBU_HUREYRE = Person(
    id="ebu_hureyre", name="Ebû Hüreyre", years="?–678 (h. 58)",
    tagline="En Çok Hadis Rivayet Eden Sahâbî — 5374 Hadis",
    bio=["Yemen'de yaşayan Ezd kabilesinin <b>Devs</b> koluna mensuptur; hicretin 7. yılında müslüman olmuş ve "
         "kendisini tamamen ilme vermiştir. <b>Suffe ashabındandır</b> ve sahâbîler arasında Hz. Peygamber'den "
         "<b>en çok hadis rivayet eden</b> kişidir (5374 hadis). Hadise düşkünlüğü bizzat Hz. Peygamber "
         "tarafından takdir edilmiştir (İlim 18). Çok rivayetle itham edildiğinde Bakara 159 ve 174. ayetleri "
         "okuyarak cevap vermiş, 'Ensardan kardeşlerimizi bağ-bahçe işleri meşgul ediyordu; Ebû Hüreyre ise "
         "karın tokluğuna Rasûlullah'ın ardından koşuyordu' demiştir. Kendisinden nakledilen "
         "<b>Sahîfe-i Sahîha</b>'nın bir bölümü, talebesi Hemmâm b. Münebbih kanalıyla <b>Sahîfetü Hemmâm</b> "
         "adıyla günümüze ulaşmıştır (138 hadis)."],
    key_work="Sahîfe-i Sahîha (→ Sahîfetü Hemmâm, 138 hadis)", initials="EH",
)
ABDULLAH_B_AMR = Person(
    id="abdullah_amr", name="Abdullah b. Amr b. el-Âs", years="?–684 (h. 65)",
    tagline="Hadisleri YAZAN Sahâbî — es-Sahîfetü's-Sâdıka",
    bio=["Ebû Hüreyre'nin, 'Benden daha çok hadis rivayet eden yoktur; <b>ancak Abdullah b. Amr müstesna, çünkü "
         "o yazıyordu ben yazmıyordum</b>' diyerek istisna ettiği sahâbîdir (İlim 20). Bu ifade, "
         "<b>kitâbetü'l-ilm</b> (ilmin yazıyla tespiti) tartışmasının en güçlü delillerindendir; yazdığı "
         "sahîfe <b>es-Sahîfetü's-Sâdıka</b> adıyla anılır. Aynı ünitede ayrıca <b>“Vay o topuklara "
         "ateşten!”</b> uyarısının (İlim 16) râvisidir — orada uyarının <b>iki ya da üç kez</b> "
         "tekrarlandığını kaydeder."],
    key_work="es-Sahîfetü's-Sâdıka", initials="AA",
)
ZUHRI = Person(
    id="zuhri", name="İbn Şihâb ez-Zührî", years="50–124",
    tagline="Tedvînin Adıyla Özdeşleşen Tâbiî — Siğâr-ı Tâbiîn",
    bio=["Tam adı <b>Ebû Bekr Muhammed b. Müslim b. Ubeydillah b. Şihâb ez-Zührî</b>'dir; tâbiûnun "
         "meşhurlarından ve <b>siğâr-ı tâbiîn</b>den sayılır. Hâfızasının çok güçlü olduğu belirtilir. "
         "<b>Hadislerin yazılması ve toplanmasına iştirak eden</b> âlimlerden biridir; sünnetleri ve "
         "sahâbeden gelen rivayetleri henüz öğrencilik yıllarında yazmıştır. Arkadaşı Sâlih b. Keysân, "
         "sahâbe sözlerini yazma tartışmasını anlatırken <b>“Neticede o kazandı, ben kaybettim”</b> der. "
         "Ebû'z-Zinâd ise onun için <b>“Bizler sadece helâl ve haramı yazardık; İbn Şihâb ise duyduğu her "
         "şeyi yazardı”</b> demiştir. Bu ünitede <b>4, 9 ve 21. rivayetlerin</b> senedinde yer alır."],
    key_work="Tedvîn faaliyetinin merkez ismi", initials="ZÜ",
)
HUMEYDI = Person(
    id="humeydi", name="el-Humeydî", years="?–834 (ö. 219)",
    tagline="Buhârî'nin Hocası, Mekkeli Müsned Musannıfı — Şeyhu'l-Harem",
    bio=["Tam adı <b>Ebû Bekir Abdullah b. ez-Zübeyr b. Îsâ el-Humeydî el-Esedî</b>'dir. "
         "<b>Süfyân b. Uyeyne</b>'nin uzun yıllar talebeliğini yapmış, <b>İmam Buhârî'ye hocalık</b> "
         "etmiştir; fıkıh ve hadiste Buhârî'yi en çok etkileyen hocasının Humeydî olduğu belirtilir. "
         "<b>Şeyhu'l-Harem</b> diye de anılır. Günümüze ulaşan tek eseri <b>el-Müsned</b>'dir: müsnedlerin "
         "genel karakterine uygun olarak <b>Hz. Ebû Bekir'in rivayetleriyle başlar</b>, son kısımda Ebû "
         "Hüreyre, Enes b. Mâlik ve Câbir b. Abdillah'ın rivayetleri yer alır; <b>179 sahâbîye</b> ait, "
         "mükerrerleriyle birlikte <b>1390 rivayet</b> içerir. Bu ünitede 11. rivayetin senedinin "
         "başındadır."],
    key_work="el-Müsned (179 sahâbî · 1390 rivayet)", initials="HU",
)

PERSONS = {p.id: p for p in [
    EBU_ZERR, IBN_MESUD, EBU_MUSA, EBU_HUREYRE, ABDULLAH_B_AMR, ZUHRI, HUMEYDI]}


def get_pack() -> CoursePack:
    # =======================================================================
    # 1. BÖLÜM — İlmin Fazileti (Kitâbü'l-İlm 1–4)
    # =======================================================================
    ch1 = Chapter(
        number=1,
        title="İlmin Fazileti ve İlmin Kaynağı",
        subtitle="Kitâbü'l-İlm 1–4 · Bâb: Fazlü'l-ilm — öğrenmenin değeri, verâsetü'l-enbiyâ ve rivayet türleri",
        key_terms=[
            KeyTerm("Muallak (Ta'lîk)", "Senedin baş tarafı (bir, birkaç ya da tüm râviler) hazfedilerek “وقال فلان” kalıbıyla nakledilen rivayet. Buhârî bâb başlarında sık kullanır; bu bâbın <b>ilk üç rivayeti</b> muallaktır."),
            KeyTerm("Mevkūf", "Senedi sahâbîde duran, yani Hz. Peygamber'e değil bir sahâbîye nispet edilen söz. Kaynak, <b>Ebû Zerr'in samsâme sözünü</b> bunun örneği olarak dipnotta işaretler."),
            KeyTerm("Verâsetü'l-enbiyâ", "“Âlimler peygamberlerin vârisleridir.” Bırakılan miras mal değil <b>ilim</b>dir; onu alan “bol bir nasip” almış olur."),
            KeyTerm("Rabbânî", "İbn Abbâs'ın tarifiyle <b>hilim sahibi fakih</b>; ayrıca “insanları ilmin büyüğünden önce küçüğüyle yetiştiren” kimse — yani <b>tedrîc</b> ilkesinin adı."),
        ],
    )
    ch1.pages.append(
        ChapterPage()
        .add_terms(ch1.key_terms)
        .add_ayat("Bâb: Fazlü'l-İlm (İlmin Fazileti)", [
            Ayah(
                "İlim 1 — “Allah kimin hakkında hayır dilerse onu dinde fakih kılar” (MUALLAK)",
                "وَقَالَ النَّبِيُّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ: مَنْ يُرِدِ اللهُ بِهِ خَيْرًا يُفَقِّهْهُ فِي الدِّينِ. وَإِنَّمَا الْعِلْمُ بِالتَّعَلُّمِ. وَإِنَّ الْعُلَمَاءَ هُمْ وَرَثَةُ الْأَنْبِيَاءِ، وَرَّثُوا الْعِلْمَ، مَنْ أَخَذَهُ أَخَذَ بِحَظٍّ وَافِرٍ. وَمَنْ سَلَكَ طَرِيقًا يَطْلُبُ بِهِ عِلْمًا سَهَّلَ اللهُ لَهُ طَرِيقًا إِلَى الْجَنَّةِ.",
                "Nebî (s.a.v.) buyurdu: “Allah kimin hakkında hayır dilerse onu dinde fakih (anlayış sahibi) kılar. İlim ancak öğrenmekle elde edilir.” Ve: “Âlimler peygamberlerin vârisleridir; onlar ilmi miras bıraktılar. Kim onu alırsa bol bir nasip almış olur. Kim ilim aramak için bir yola girerse Allah ona cennete giden bir yolu kolaylaştırır.”",
                "<b>Buhârî, İlm, 10.</b> Bâb başlığında senedi hazfedilerek “وقال النبي” kalıbıyla verildiği için <b>muallak</b>tır; kesinlik sîgasıyla nakledildiği için bu, rivayeti burada zayıf yapmaz.",
            ),
        ])
    )
    ch1.pages.append(
        ChapterPage()
        .add_ayat(None, [
            Ayah(
                "İlim 2 — Ebû Zerr: “Boynuma kılıcı koysanız yine tebliğ ederdim” (MEVKŪF)",
                "وَقَالَ أَبُو ذَرٍّ: لَوْ وَضَعْتُمُ الصَّمْصَامَةَ عَلَى هَذِهِ — وَأَشَارَ إِلَى قَفَاهُ — ثُمَّ ظَنَنْتُ أَنِّي أُنْفِذُ كَلِمَةً سَمِعْتُهَا مِنَ النَّبِيِّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ قَبْلَ أَنْ تُجِيزُوا عَلَيَّ لَأَنْفَذْتُهَا.",
                "Ebû Zerr dedi ki: “Şunun (ensemin) üzerine keskin kılıcı koysanız, sonra siz beni öldürmeden önce Nebî'den (s.a.v.) işittiğim bir sözü ulaştırabileceğimi zannetsem, mutlaka onu ulaştırırdım.”",
                "<b>Buhârî, İlm, 10.</b> Dipnot: “Dikkat edilirse burada hadis Ebû Zerr'e nisbet edilmektedir; Ebû Zerr sahâbî olduğu için hadis <b>mevkūf</b> olmaktadır.” <i>Samsâme</i> = keskin, kesici kılıç.",
            ),
        ])
        .add_ayat("Bâb: Fazlü'l-İlm (devam)", [
            Ayah(
                "İlim 3 — İbn Abbâs: “Rabbânî” kimdir? (MEVKŪF · Âl-i İmrân 3/79)",
                "وَقَالَ ابْنُ عَبَّاسٍ: كُونُوا رَبَّانِيِّينَ: حُلَمَاءَ فُقَهَاءَ. وَيُقَالُ: الرَّبَّانِيُّ الَّذِي يُرَبِّي النَّاسَ بِصِغَارِ الْعِلْمِ قَبْلَ كِبَارِهِ.",
                "İbn Abbâs dedi ki: “Rabbânîler olun” (âyeti) yani hilim sahibi fakihler olun (demektir). Şöyle de denir: Rabbânî, insanları ilmin büyüğünden önce küçüğüyle yetiştiren kimsedir.",
                "<b>Buhârî, İlm, 10.</b> Âyet: <b>Âl-i İmrân 3/79</b>. Eğitimde <b>tedrîc</b> (basitten karmaşığa) ilkesinin klasik delilidir.",
            ),
            Ayah(
                "İlim 4 — Süt Rüyası: “Onu ilim olarak yorumladım”",
                "حَدَّثَنَا سَعِيدُ بْنُ عُفَيْرٍ قَالَ: حَدَّثَنِي اللَّيْثُ قَالَ: حَدَّثَنِي عُقَيْلٌ عَنِ ابْنِ شِهَابٍ عَنْ حَمْزَةَ بْنِ عَبْدِ اللهِ بْنِ عُمَرَ أَنَّ ابْنَ عُمَرَ قَالَ: سَمِعْتُ رَسُولَ اللهِ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ قَالَ: بَيْنَا أَنَا نَائِمٌ أُتِيتُ بِقَدَحِ لَبَنٍ فَشَرِبْتُ حَتَّى إِنِّي لَأَرَى الرِّيَّ يَخْرُجُ فِي أَظْفَارِي، ثُمَّ أَعْطَيْتُ فَضْلِي عُمَرَ بْنَ الْخَطَّابِ. قَالُوا: فَمَا أَوَّلْتَهُ يَا رَسُولَ اللهِ؟ قَالَ: الْعِلْمَ.",
                "İbn Ömer'den: Resûlullah'ı (s.a.v.) şöyle buyururken işittim: “Ben uyurken bana bir bardak süt getirildi; içtim, öyle ki kanmanın tırnaklarımdan çıktığını görüyordum. Sonra artanını Ömer b. Hattâb'a verdim.” Ashâb: “Bunu nasıl yorumladın ey Allah'ın Resûlü?” dediler. “İlim olarak” buyurdu.",
                "<b>Buhârî, İlm, 22; Tirmizî, Rü'yâ, 9.</b> Kaynak bu rivayetin <b>senedini bilerek tam verir</b>: Saîd b. Ufeyr ← Leys ← Ukayl ← İbn Şihâb ← Hamza b. Abdillah ← İbn Ömer. Dipnotta ayrıca <b>Hz. Ömer'in hadis konusundaki tavrının</b> araştırılması istenir.",
            ),
        ])
        .add_callout(Callout(
            "focus", "Neden Tam Sened? — “Semi'tü” Lafzı",
            "Bu bâbın ilk üç rivayeti <b>muallak</b> (senetsiz) verilirken dördüncüsünün senedi <u>baştan sona</u> "
            "yazılmıştır. Sebep, dipnotun kendisidir: burada <b>tahammül ve edâ sîgaları</b> araştırılmak üzere "
            "verilir. İbn Ömer'in kullandığı <b>“سمعت”</b> (işittim), hocadan bizzat dinlemeyi bildirdiği için "
            "edâ sîgalarının <b>en kuvvetlisidir</b>; buna karşılık bağlantıyı belirsiz bırakan <b>“عن”</b> "
            "(an'ane) en zayıfıdır."
        ))
    )
    ch1.pages.append(
        ChapterPage()
        .add_ayat("Bâbın Sonundaki Şerh ve Âsâr Metinleri", [
            Ayah(
                "Şerh — Âlimlerin Derecesi ve Mirası",
                "شَرْحٌ: جَاءَ فِي كَثِيرٍ مِنَ الْآثَارِ أَنَّ دَرَجَاتِ الْعُلَمَاءِ تَتْلُو دَرَجَاتِ الْأَنْبِيَاءِ وَدَرَجَاتِ أَصْحَابِهِمْ، وَالْعُلَمَاءُ وَرَثَةُ الْأَنْبِيَاءِ، وَإِنَّمَا وَرِثُوا الْعِلْمَ وَبَيَّنُوهُ لِلْأُمَّةِ وَذَبُّوا عَنْهُ وَحَمَوْهُ مِنْ تَحْرِيفِ الْجَاهِلِينَ وَانْتِحَالِ الْمُبْطِلِينَ.",
                "Pek çok âsârda gelmiştir ki âlimlerin dereceleri peygamberlerin ve ashâbının derecelerini takip eder. Âlimler peygamberlerin vârisleridir; ilmi miras aldılar, ümmete açıkladılar, onu savundular ve câhillerin tahrîfinden, bâtıl ehlinin intihâlinden korudular.",
                "<b>İbn Battâl, Şerhu Sahîhi'l-Buhârî, I, 133.</b> Metindeki <b>“âsâr”</b> kullanımı, dipnottaki <b>hadis–haber–eser</b> ayrımının canlı örneğidir.",
            ),
            Ayah(
                "Âsâr — İbn Mes'ûd: “Amellerin en faziletlisi ilimdir”",
                "عَنِ الْأَوْزَاعِيِّ قَالَ: جَاءَ رَجُلٌ إِلَى ابْنِ مَسْعُودٍ فَقَالَ: يَا أَبَا عَبْدِ الرَّحْمَنِ، أَيُّ الْأَعْمَالِ أَفْضَلُ؟ قَالَ: الْعِلْمُ. ثُمَّ سَأَلَهُ: أَيُّ الْأَعْمَالِ أَفْضَلُ؟ قَالَ: الْعِلْمُ. قَالَ: أَنَا أَسْأَلُكَ عَنْ أَفْضَلِ الْأَعْمَالِ وَأَنْتَ تَقُولُ: الْعِلْمُ؟ قَالَ: وَيْحَكَ! إِنَّ مَعَ الْعِلْمِ بِاللهِ يَنْفَعُكَ قَلِيلُ الْعَمَلِ وَكَثِيرُهُ، وَمَعَ الْجَهْلِ بِاللهِ لَا يَنْفَعُكَ قَلِيلُ الْعَمَلِ وَلَا كَثِيرُهُ.",
                "Evzâî'den: Bir adam İbn Mes'ûd'a gelip “Ey Ebû Abdirrahmân, amellerin en faziletlisi hangisidir?” dedi. “İlim” dedi. Adam tekrar sordu, yine “İlim” dedi. Adam: “Ben sana amellerin en faziletlisini soruyorum, sen ‘ilim’ diyorsun!” deyince şöyle dedi: “Yazık sana! Allah'ı bilmekle beraber az amel de çok amel de sana fayda verir; Allah'ı bilmemekle beraber ne az amel ne de çok amel fayda verir.”",
                "<b>İbn Battâl, a.g.e., I, 133.</b> Sonuç: <b>ilim amelden önce gelir</b>, çünkü amelin sıhhati ilme bağlıdır. Dipnotta “<i>eyyü'l-a'mâli efdal</i>” ifadesinin anlamı ödev olarak sorulur.",
            ),
        ])
        .add_table(ComparisonTable(
            "Müntehâsına Göre Hadis Çeşitleri — ve Bu Bâbdaki Karşılıkları",
            ["Çeşit", "Kime nispet edilir?", "Bu üniteden örnek"],
            [
                ["<b>Merfû'</b>", "Hz. Peygamber'e", "İlim 1, 4, 5, 8, 9, 11, 12…"],
                ["<b>Mevkūf</b>", "Sahâbîye", "<b>İlim 2</b> (Ebû Zerr), <b>3</b> (İbn Abbâs), <b>10</b> (Hz. Ömer)"],
                ["<b>Maktû'</b>", "Tâbiîye", "Ünitede rivayet olarak yok; şerh nakilleri bu türdendir"],
                ["<b>Kudsî</b>", "Lafzı Peygamber'e, mânası Allah'a", "Bu ünitede örneği yoktur"],
            ],
        ))
    )
    ch1.pages.append(
        ChapterPage()
        .add_person(EBU_ZERR)
        .add_summary(
            "Bâb, ilmi üç cümlede tanımlar: ilim bir hayır alâmetidir (men yüridillâhu bihî hayran), "
            "öğrenmekle kazanılır (innemâ'l-ilmu bi't-teallüm) ve peygamber mirasıdır "
            "(verâsetü'l-enbiyâ). Ebû Zerr bunun tebliğ tarafını, İbn Abbâs öğretim tarafını (tedrîc), "
            "İbn Ömer'in rüyası ise ilmin bizzat bir nimet olarak tasvirini verir. Bâbın dört "
            "rivayetinden üçü muallak, ikisi mevkūftur — yani bâb aynı zamanda bir "
            "rivayet türü dersidir."
        )
    )

    # =======================================================================
    # 2. BÖLÜM — Tebliğ ve Öğretim Âdâbı (Kitâbü'l-İlm 5–8)
    # =======================================================================
    ch2 = Chapter(
        number=2,
        title="Tebliğ ve Öğretim Âdâbı",
        subtitle="Kitâbü'l-İlm 5–8 · İki bâb: “Rubbe mübelliğin ev'â min sâmi'” ve usandırmadan öğretmek",
        key_terms=[
            KeyTerm("Rubbe mübelliğin ev'â min sâmi'", "“Nice kendisine tebliğ edilen, işitenden daha kavrayışlıdır.” Bâb başlığı hadisin son cümlesinden alınmıştır; <b>rivayetin sürekliliğinin</b> gerekçesidir."),
            KeyTerm("Tehavvül", "Uygun zamanı gözeterek, <b>aralıklarla</b> öğüt vermek. Hz. Peygamber “yetehavvelünâ bi'l-mev'ıza” — öğüdü günlere yayardı."),
            KeyTerm("Se'âme", "Usanç, bıkkınlık. Öğüdün aralıklı verilmesinin gerekçesi <b>“kerâhete's-se'âme aleynâ”</b> — bize usanç gelmesinden hoşlanmamasıdır."),
            KeyTerm("Teysîr", "Kolaylaştırma. “Yessirû ve lâ tuassirû, beşşirû ve lâ tüneffirû” — bâbın “keylâ yenfirû” (nefret etmesinler diye) başlığının özeti."),
        ],
    )
    ch2.pages.append(
        ChapterPage()
        .add_terms(ch2.key_terms)
        .add_ayat("Bâb: Kavlü'n-Nebî — “Rubbe mübelliğin ev'â min sâmi'”", [
            Ayah(
                "İlim 5 — Vedâ Hutbesi: “Burada bulunan bulunmayana ulaştırsın”",
                "عَنْ عَبْدِ الرَّحْمَنِ بْنِ أَبِي بَكْرَةَ عَنْ أَبِيهِ: ذَكَرَ النَّبِيَّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ قَعَدَ عَلَى بَعِيرِهِ وَأَمْسَكَ إِنْسَانٌ بِخِطَامِهِ، قَالَ: أَيُّ يَوْمٍ هَذَا؟ فَسَكَتْنَا حَتَّى ظَنَنَّا أَنَّهُ سَيُسَمِّيهِ سِوَى اسْمِهِ. قَالَ: أَلَيْسَ يَوْمَ النَّحْرِ؟ قُلْنَا: بَلَى. قَالَ: فَأَيُّ شَهْرٍ هَذَا؟ فَسَكَتْنَا حَتَّى ظَنَنَّا أَنَّهُ سَيُسَمِّيهِ بِغَيْرِ اسْمِهِ، فَقَالَ: أَلَيْسَ بِذِي الْحِجَّةِ؟ قُلْنَا: بَلَى. قَالَ: فَإِنَّ دِمَاءَكُمْ وَأَمْوَالَكُمْ وَأَعْرَاضَكُمْ بَيْنَكُمْ حَرَامٌ كَحُرْمَةِ يَوْمِكُمْ هَذَا فِي شَهْرِكُمْ هَذَا فِي بَلَدِكُمْ هَذَا. لِيُبَلِّغِ الشَّاهِدُ الْغَائِبَ، فَإِنَّ الشَّاهِدَ عَسَى أَنْ يُبَلِّغَ مَنْ هُوَ أَوْعَى لَهُ مِنْهُ.",
                "Ebû Bekre'den: Nebî (s.a.v.) devesine oturmuş, biri yularını tutmuştu. “Bu hangi gündür?” buyurdu. Sustuk; başka bir isim vereceğini sandık. “Kurban günü değil mi?” dedi. “Evet” dedik. “Bu hangi aydır?” dedi… “Zilhicce değil mi?” dedi. “Evet” dedik. Sonra: “Kanlarınız, mallarınız ve ırzlarınız, bu ayınızda, bu beldenizde, bu gününüzün haramlığı gibi birbirinize haramdır. Burada bulunan bulunmayana ulaştırsın; çünkü burada bulunan, belki kendisinden daha kavrayışlı birine ulaştırır.”",
                "<b>Buhârî, İlm, 9; Dârimî, Mukaddime, 72.</b> Sened: Müsedded ← Bişr ← İbn Avn ← <b>İbn Sîrîn</b> ← Abdurrahmân b. Ebî Bekre ← babası. Dipnotta <b>İbn Sîrîn'in isnad hakkındaki sözü</b> araştırılmak üzere verilir.",
            ),
        ])
        .add_callout(Callout(
            "insight", "Aynî'nin Şerhi: Tebliğ Bir Mîsâktır",
            "<i>Umdetü'l-Kārî</i>, II, 38: “Bu hadiste, <b>âlimin ilmi kendisine ulaşmayana tebliğ etmesinin ve "
            "anlamayana açıklamasının vâcip olduğu</b> vardır; bu, Allah'ın âlimlerden aldığı, <u>onu insanlara "
            "açıklayacaklar ve gizlemeyecekler</u> mîsâkıdır.” — Krş. <b>Âl-i İmrân 3/187</b>."
        ))
    )
    ch2.pages.append(
        ChapterPage()
        .add_block(BulletBlock(1, "Hutbede Kullanılan Öğretim Tekniği", [
            "Hz. Peygamber hükmü doğrudan söylemek yerine önce <b>soru sorar</b> (“Bu hangi gündür?”), "
            "sahâbe susar, sonra <b>bilinen cevabı kendisi verir</b>. Bu bekleme, muhatabın dikkatini "
            "toplayıp söylenecek hükmü <b>zihinde çakılı</b> hâle getirir.",
            "Hüküm, üç <b>bilinen kutsal</b> (gün, ay, belde) üzerine kurulur: kan, mal ve ırz dokunulmazlığı "
            "somut bir benzetmeyle anlatılır — soyut bir kural değil, <b>hissedilen bir haram</b> hâline gelir.",
            "Son cümle bâbın adını verir: <b>“li-yübelliği'ş-şâhidü'l-gāib”</b>. Rivayetin kuşaktan kuşağa "
            "aktarılması buradan meşrûiyet alır; hadis tahsili bir <b>emirdir</b>.",
        ]))
        .add_ayat("Bâb: Mâ kâne'n-Nebî Yetehavvelühüm bi'l-Mev'ıza… Keylâ Yenfirû", [
            Ayah(
                "İlim 6 — “Usanmayalım diye öğüdü günlere yayardı”",
                "عَنِ ابْنِ مَسْعُودٍ قَالَ: كَانَ النَّبِيُّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ يَتَخَوَّلُنَا بِالْمَوْعِظَةِ فِي الْأَيَّامِ كَرَاهَةَ السَّآمَةِ عَلَيْنَا.",
                "İbn Mes'ûd'dan: “Nebî (s.a.v.), bize usanç gelmesin diye öğüdü günlere yayarak (aralıklı olarak) verirdi.”",
                "<b>Buhârî, İlm, 11; Müslim, Sıfâtü'l-Münâfikîn, 82.</b> Dipnotta bu vesileyle <b>kavlî / fiilî / takrîrî sünnet</b> ayrımı hatırlatılır; bu rivayet <b>fiilî sünnet</b>tir.",
            ),
            Ayah(
                "İlim 7 — İbn Mes'ûd'un haftada bir gün ders vermesi",
                "عَنْ أَبِي وَائِلٍ قَالَ: كَانَ عَبْدُ اللهِ يُذَكِّرُ النَّاسَ فِي كُلِّ خَمِيسٍ، فَقَالَ لَهُ رَجُلٌ: يَا أَبَا عَبْدِ الرَّحْمَنِ، لَوَدِدْتُ أَنَّكَ ذَكَّرْتَنَا كُلَّ يَوْمٍ. قَالَ: أَمَا إِنَّهُ يَمْنَعُنِي مِنْ ذَلِكَ أَنِّي أَكْرَهُ أَنْ أُمِلَّكُمْ، وَإِنِّي أَتَخَوَّلُكُمْ بِالْمَوْعِظَةِ كَمَا كَانَ النَّبِيُّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ يَتَخَوَّلُنَا بِهَا مَخَافَةَ السَّآمَةِ عَلَيْنَا.",
                "Ebû Vâil'den: Abdullah (b. Mes'ûd) insanlara her perşembe öğüt verirdi. Bir adam ona: “Ey Ebû Abdirrahmân, keşke bize her gün öğüt versen” dedi. Şöyle cevap verdi: “Beni bundan alıkoyan, sizi usandırmaktan hoşlanmamamdır. Nebî'nin (s.a.v.) bize usanç gelmesinden çekinerek öğüdü aralıklı vermesi gibi ben de size öyle yapıyorum.”",
                "<b>Buhârî, İlm, 12.</b> Senedin başındaki <b>Osman b. Ebî Şeybe</b>, meşhur “<b>İbn Ebî Şeybe kardeşler</b>”in büyüğüdür; küçük kardeşi <b>Ebû Bekr b. Ebî Şeybe</b> (ö. 235/849) el-Musannef sahibidir.",
            ),
        ])
        .add_ayat("Bâbın Özet Cümlesi", [
            Ayah(
                "İlim 8 — “Kolaylaştırın, zorlaştırmayın”",
                "عَنْ أَنَسٍ عَنِ النَّبِيِّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ قَالَ: يَسِّرُوا وَلَا تُعَسِّرُوا، وَبَشِّرُوا وَلَا تُنَفِّرُوا.",
                "Enes'ten, Nebî (s.a.v.) buyurdu: “Kolaylaştırın, zorlaştırmayın; müjdeleyin, nefret ettirmeyin.”",
                "<b>Buhârî, İlm, 11; Müslim, Cihâd, 6; Ebû Dâvûd, Edeb, 6.</b> Dört emir kalıbı hâlinde ezberlenir: <i>yessirû – lâ tuassirû · beşşirû – lâ tüneffirû</i>.",
            ),
        ])
    )
    ch2.pages.append(
        ChapterPage()
        .add_flow(FlowDiagram([
            FlowStep("Tehavvül", "Uygun zamanı gözet"),
            FlowStep("Tedrîc", "Küçükten büyüğe"),
            FlowStep("Teysîr", "Kolaylaştır"),
            FlowStep("Tebşîr", "Müjdeleyerek yaklaş"),
            FlowStep("Tebliğ", "Ulaştırmayı sürdür"),
        ], caption="Kitâbü'l-İlm'in ilk üç bâbından çıkan öğretim zinciri — her adımın bir rivayeti vardır."))
        .add_person(IBN_MESUD)
        .add_summary(
            "Bu iki bâb birlikte bir öğretim politikası kurar. Tebliğ zorunludur ve bir mîsâka "
            "dayanır (İlim 5); ama zorunluluk, bıktırmayı mübah kılmaz: öğüt aralıklı verilir "
            "(İlim 6), sahâbî bunu bizzat uygular (İlim 7) ve ilke dört kelimeye indirgenir: "
            "kolaylaştır, müjdele (İlim 8). Bâb başlığındaki “keylâ yenfirû” ile hadisteki "
            "“lâ tüneffirû” aynı kökten gelir — Buhârî'nin bâb başlığını hadisin lafzından "
            "kurduğunun açık örneğidir."
        )
    )

    # =======================================================================
    # 3. BÖLÜM — Fıkh Nimeti ve İlimde Gıbta (Kitâbü'l-İlm 9–11)
    # =======================================================================
    ch3 = Chapter(
        number=3,
        title="Fıkh Nimeti ve İlimde Gıbta",
        subtitle="Kitâbü'l-İlm 9–11 · “İnnemâ ene kāsim”, tefakkuh emri ve hased ile gıbtanın ayrımı",
        key_terms=[
            KeyTerm("Fıkh", "Derin anlayış. “Men yüridillâhu bihî hayran yüfakkıhhu fi'd-dîn” — dinde anlayış sahibi kılınmak, kul hakkında <b>hayır dilenmiş olmasının</b> alâmetidir."),
            KeyTerm("Kāsım", "Taksim eden. “<b>İnnemâ ene kāsim va'llâhu yu'tî</b>” — Hz. Peygamber ilmi ve malı taksim eder; hakiki <b>veren Allah'tır</b>."),
            KeyTerm("Tefakkuh kable't-tesevvüd", "Hz. Ömer'in emri: “<b>Baş yapılmadan önce fıkıh öğrenin.</b>” İki yorumu vardır: evlenip aile reisi olmadan önce; ve toplumda lider olmadan önce."),
            KeyTerm("İğtibât (Gıbta)", "Nimetin <b>sahibinden gitmesini istemeden</b> benzerine sahip olmayı temenni etmek. Hasedden farklıdır ve <b>meşrûdur</b>; bâbın adı buradan gelir."),
        ],
    )
    ch3.pages.append(
        ChapterPage()
        .add_terms(ch3.key_terms)
        .add_ayat("Bâb: Men Yüridillâhu bihî Hayran Yüfakkıhhu fi'd-Dîn", [
            Ayah(
                "İlim 9 — “Ben ancak taksim ediciyim, veren Allah'tır”",
                "سَمِعْتُ مُعَاوِيَةَ خَطِيبًا يَقُولُ: سَمِعْتُ النَّبِيَّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ يَقُولُ: مَنْ يُرِدِ اللهُ بِهِ خَيْرًا يُفَقِّهْهُ فِي الدِّينِ، وَإِنَّمَا أَنَا قَاسِمٌ وَاللهُ يُعْطِي، وَلَنْ تَزَالَ هَذِهِ الْأُمَّةُ قَائِمَةً عَلَى أَمْرِ اللهِ لَا يَضُرُّهُمْ مَنْ خَالَفَهُمْ حَتَّى يَأْتِيَ أَمْرُ اللهِ.",
                "Muâviye'yi hutbe verirken şöyle derken işittim: Nebî'yi (s.a.v.) şöyle buyururken işittim: “Allah kimin hakkında hayır dilerse onu dinde fakih kılar. Ben ancak taksim ediciyim, veren ise Allah'tır. Bu ümmet, Allah'ın emri gelinceye kadar Allah'ın emri üzere ayakta kalmaya devam edecek; kendilerine muhalefet edenler onlara zarar veremeyecektir.”",
                "<b>Buhârî, İlm, 13; Müslim, Zekât, 98; Tirmizî, İlm, 1; İbn Mâce, Mukaddime, 17.</b> Sened: Saîd b. Ufeyr ← İbn Vehb ← Yûnus ← <b>ez-Zührî</b> ← Humeyd b. Abdirrahmân ← Muâviye.",
            ),
        ])
        .add_callout(Callout(
            "caution", "Sınav Tuzağı: Aynı Metin, İki Farklı Sened Durumu",
            "<b>İlim 1</b>'de “men yüridillâhu bihî hayran…” cümlesi <u>muallak</u> olarak (senetsiz, bâb "
            "başlığında) geçmişti. <b>İlim 9</b>'da aynı cümle <u>mevsûl</u> olarak, tam senediyle gelir. "
            "Bu, muallak rivayetlerin <b>başka bir yerde senediyle bulunabileceğinin</b> ders içindeki en "
            "temiz örneğidir — “muallak = zayıf” demek olmadığının delili."
        ))
    )
    ch3.pages.append(
        ChapterPage()
        .add_ayat("Bâb: el-İğtibât fi'l-İlm ve'l-Hikme", [
            Ayah(
                "İlim 10 — Hz. Ömer: “Baş olmadan önce fıkıh öğrenin” (MEVKŪF)",
                "وَقَالَ عُمَرُ: تَفَقَّهُوا قَبْلَ أَنْ تُسَوَّدُوا.",
                "Ömer dedi ki: “Baş (seyyid/reis) yapılmadan önce fıkıh öğrenin.”",
                "<b>Buhârî, İlm, 15.</b> Senedi hazfedilerek “وقال عمر” kalıbıyla verildiği için hem <b>muallak</b> hem <b>mevkūf</b>tur.",
            ),
            Ayah(
                "İlim 11 — “İki şey dışında (kimseye) gıbta edilmez”",
                "عَنْ عَبْدِ اللهِ بْنِ مَسْعُودٍ قَالَ: قَالَ النَّبِيُّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ: لَا حَسَدَ إِلَّا فِي اثْنَتَيْنِ: رَجُلٌ آتَاهُ اللهُ مَالًا فَسُلِّطَ عَلَى هَلَكَتِهِ فِي الْحَقِّ، وَرَجُلٌ آتَاهُ اللهُ الْحِكْمَةَ فَهُوَ يَقْضِي بِهَا وَيُعَلِّمُهَا.",
                "İbn Mes'ûd'dan: Nebî (s.a.v.) buyurdu: “İki kişi dışında (kimseye) gıbta edilmez: Allah'ın kendisine mal verdiği ve onu hak yolunda harcamaya muvaffak kıldığı kimse; bir de Allah'ın kendisine hikmet verdiği, onunla hükmeden ve onu öğreten kimse.”",
                "<b>Buhârî, İlm, 15; Müslim, Salâtü'l-Müsâfirîn, 266.</b> Sened kaynakta tam verilir: <b>el-Humeydî</b> ← Süfyân ← İsmâil b. Ebî Hâlid ← Kays b. Ebî Hâzim ← İbn Mes'ûd.",
            ),
        ])
        .add_block(BulletBlock(1, "“Tüsevvedû” Kelimesinin İki Şerhi (Lisânü'l-Arab, III, 224)", [
            "<b>Birinci yorum:</b> “<i>Evlenip ev sahibi olmadan</i>, yani evlilik sizi ilimden alıkoymadan "
            "önce fıkıh öğrenin.” Burada <b>tesevvüd</b>, aile reisi olmak anlamındadır.",
            "<b>İkinci yorum (Ebû Ubeyd):</b> “<i>Küçükken, kendinize bakılan reisler hâline gelmeden</i> "
            "önce ilim öğrenin. Öncesinde öğrenmezseniz <b>büyüdükten sonra öğrenmekten utanır</b>, câhil "
            "kalır, ilmi <b>sizden küçüklerden</b> almak zorunda kalırsınız; bu da sizi küçük düşürür.”",
            "Her iki yorumun ortak sonucu aynıdır: <b>ilim tahsili gençlikte ve makam gelmeden yapılır.</b>",
        ]))
        .add_table(ComparisonTable(
            "Hased ↔ Gıbta (İğtibât) — İbn Manzûr, Lisânü'l-Arab, “ğbt” md., VII, 358",
            ["Ölçüt", "HASED", "GIBTA (iğtibât)"],
            [
                ["İstenen şey", "Nimetin <b>ondan gitmesi</b> ve kendine geçmesi", "Nimetin <b>benzerinin</b> kendisinde de olması"],
                ["Nimetin zevâli", "<b>İstenir</b>", "<b>İstenmez</b>"],
                ["Hüküm", "Haram, kötülenmiş", "<b>Meşrû — hased değildir</b>"],
                ["Metindeki karşılığı", "—", "Hadisteki “lâ hasede” ifadesi teknik olarak <b>gıbta</b>yı kasteder; bâbın adı da <b>el-iğtibât</b>tır"],
            ],
        ))
    )
    ch3.pages.append(
        ChapterPage()
        .add_callout(Callout(
            "focus", "Gıbtanın İki Konusu — ve İkisinin Ortak Yönü",
            "<b>(1) Hak yolunda harcanan mal</b>, <b>(2) öğretilen hikmet.</b> Her ikisi de <u>sahibinde "
            "kalmayan</u>, başkasına akan nimetlerdir — bu yüzden gıbtaya konu olurlar. Dikkat: hikmet "
            "burada tek başına “bilmek” değil, <b>ilim + onunla hükmetmek + onu öğretmek</b> üçlüsüdür "
            "(“<i>fe-hüve yakdî bihâ ve yuallimuhâ</i>”)."
        ))
        .add_person(HUMEYDI)
        .add_summary(
            "Bölüm, ilmin kaynağı ve zamanı sorularını cevaplar: ilim Allah'ın bir "
            "taksimidir, Peygamber taksim edici, veren Allah'tır (İlim 9); bu yüzden ilim talebi "
            "ertelenmez, makam gelmeden yapılır (İlim 10); ve ilim, kıskanılması değil "
            "özenilmesi gereken tek iki nimetten biridir (İlim 11)."
        )
    )

    # =======================================================================
    # 4. BÖLÜM — Öğrenip Öğretmek ve Öğretimde Öfke (Kitâbü'l-İlm 12–14)
    # =======================================================================
    ch4 = Chapter(
        number=4,
        title="Öğrenip Öğretmek ve Öğretimde Öfke",
        subtitle="Kitâbü'l-İlm 12–14 · Yağmur meseli, “hayruküm men tealleme'l-Kur'ân” ve lukata bâbı",
        key_terms=[
            KeyTerm("Alime ve alleme", "“Öğrendi ve öğretti.” Bâbın adı bu ikiliden gelir; üstünlük tek başına öğrenmeye ya da öğretmeye değil, <b>ikisinin birleşmesine</b> bağlanır."),
            KeyTerm("Ecâdib", "Suyu emmeyip <b>tutan</b> sert toprak. Yağmur meselinde, anlamasa da <b>lafzı koruyup nakleden</b> râvi tipini temsil eder: kendi içmez, başkalarını sular."),
            KeyTerm("Kî'ân", "Ne su tutan ne ot bitiren <b>düz kayalık</b>. İlme başını kaldırmayan, hidayeti kabul etmeyen kimsenin misalidir."),
            KeyTerm("Lukata", "Buluntu mal. Hükmü: <b>vikā'</b> ve <b>ifâs</b>ını bellemek → <b>bir yıl ilan</b> (ta'rîf) → sonra faydalanmak; sahibi gelirse iade etmek."),
        ],
    )
    ch4.pages.append(
        ChapterPage()
        .add_terms(ch4.key_terms)
        .add_ayat("Bâb: Fazlü men Alime ve Alleme", [
            Ayah(
                "İlim 12 — Yağmur Meseli: Üç Tür Toprak",
                "عَنْ أَبِي مُوسَى عَنِ النَّبِيِّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ قَالَ: مَثَلُ مَا بَعَثَنِيَ اللهُ بِهِ مِنَ الْهُدَى وَالْعِلْمِ كَمَثَلِ الْغَيْثِ الْكَثِيرِ أَصَابَ أَرْضًا، فَكَانَ مِنْهَا نَقِيَّةٌ قَبِلَتِ الْمَاءَ فَأَنْبَتَتِ الْكَلَأَ وَالْعُشْبَ الْكَثِيرَ، وَكَانَتْ مِنْهَا أَجَادِبُ أَمْسَكَتِ الْمَاءَ فَنَفَعَ اللهُ بِهَا النَّاسَ فَشَرِبُوا وَسَقَوْا وَزَرَعُوا، وَأَصَابَتْ مِنْهَا طَائِفَةً أُخْرَى إِنَّمَا هِيَ قِيعَانٌ لَا تُمْسِكُ مَاءً وَلَا تُنْبِتُ كَلَأً. فَذَلِكَ مَثَلُ مَنْ فَقُهَ فِي دِينِ اللهِ وَنَفَعَهُ مَا بَعَثَنِيَ اللهُ بِهِ فَعَلِمَ وَعَلَّمَ، وَمَثَلُ مَنْ لَمْ يَرْفَعْ بِذَلِكَ رَأْسًا وَلَمْ يَقْبَلْ هُدَى اللهِ الَّذِي أُرْسِلْتُ بِهِ.",
                "Ebû Mûsâ'dan, Nebî (s.a.v.) buyurdu: “Allah'ın benimle gönderdiği hidayet ve ilmin misali, bir araziye düşen bol yağmurun misali gibidir. Toprağın bir kısmı temizdi; suyu kabul etti ve bol ot bitirdi. Bir kısmı sertti (ecâdib); suyu tuttu ve Allah onunla insanları faydalandırdı: içtiler, suladılar, ekin ektiler. Bir başka kısmına da isabet etti ki orası düz kayalıktı (kî'ân): ne su tutar ne ot bitirir. İşte bu, Allah'ın dininde fakih olan, benimle gönderilenden faydalanan, öğrenen ve öğreten kimse ile buna hiç başını kaldırmayan, hidayeti kabul etmeyen kimsenin misalidir.”",
                "<b>Buhârî, İlm, 20.</b> Sened: Muhammed b. Alâ ← Hammâd b. Üsâme ← Büreyd b. Abdillah ← Ebû Bürde ← <b>Ebû Mûsâ el-Eş'arî</b>.",
            ),
        ])
    )
    ch4.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Yağmur Meselinin Üç Toprağı — İnsan Tipleri",
            ["Toprak", "Karşılığı", "Sonuç"],
            [
                ["<b>Nakıyye</b> (temiz/verimli)", "Öğrenip <b>anlayan ve üreten</b> âlim", "Hem kendi faydalanır hem ürün verir"],
                ["<b>Ecâdib</b> (suyu tutan sert toprak)", "Ezberleyip <b>nakleden</b> râvi", "Kendisi içmez ama <b>başkalarını sular</b>"],
                ["<b>Kî'ân</b> (düz kayalık)", "İlme <b>başını kaldırmayan</b>", "Ne alır ne verir"],
            ],
        ))
        .add_ayat("Bâbın İkinci Rivayeti", [
            Ayah(
                "İlim 13 — “Sizin en hayırlınız Kur'ân'ı öğrenen ve öğretendir”",
                "عَنْ عُثْمَانَ عَنِ النَّبِيِّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ قَالَ: خَيْرُكُمْ مَنْ تَعَلَّمَ الْقُرْآنَ وَعَلَّمَهُ.",
                "Hz. Osman'dan, Nebî (s.a.v.) buyurdu: “Sizin en hayırlınız, Kur'ân'ı öğrenen ve onu öğretendir.”",
                "<b>Ebû Dâvûd, Vitr, 14; Tirmizî, Fedâilü'l-Kur'ân, 15.</b> Sened: Hafs b. Ömer ← Şu'be ← Alkame b. Mersed ← Sa'd b. Ubeyde ← Ebû Abdirrahmân ← Hz. Osman.",
            ),
        ])
        .add_callout(Callout(
            "insight", "“Hayruküm” Kalıbı Neyi Söyler?",
            "Hadis üstünlüğü tek bir fiile değil, <b>iki fiilin birleşmesine</b> bağlar: <u>tealleme</u> "
            "(öğrendi) <b>ve</b> <u>allemehû</u> (öğretti). Yağmur meselindeki <b>ecâdib</b> toprağı da tam "
            "burayı açıklar: kişi kendisi tam anlamasa bile <b>naklederek</b> ilme hizmet edebilir — ama "
            "en hayırlı olan, <b>nakıyye</b> toprağı gibi hem alan hem verendir."
        ))
        .add_person(EBU_MUSA)
    )
    ch4.pages.append(
        ChapterPage()
        .add_ayat("Bâb: el-Gadab fi'l-Mev'ıza ve't-Ta'lîm izâ Raâ mâ Yekrah", [
            Ayah(
                "İlim 14 — Lukata ve Hz. Peygamber'in Öfkelenmesi",
                "عَنْ زَيْدِ بْنِ خَالِدٍ الْجُهَنِيِّ أَنَّ النَّبِيَّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ سَأَلَهُ رَجُلٌ عَنِ اللُّقَطَةِ فَقَالَ: اعْرِفْ وِكَاءَهَا — أَوْ قَالَ وِعَاءَهَا — وَعِفَاصَهَا، ثُمَّ عَرِّفْهَا سَنَةً، ثُمَّ اسْتَمْتِعْ بِهَا، فَإِنْ جَاءَ رَبُّهَا فَأَدِّهَا إِلَيْهِ. قَالَ: فَضَالَّةُ الْإِبِلِ؟ فَغَضِبَ حَتَّى احْمَرَّتْ وَجْنَتَاهُ — أَوْ قَالَ احْمَرَّ وَجْهُهُ — فَقَالَ: وَمَا لَكَ وَلَهَا؟ مَعَهَا سِقَاؤُهَا وَحِذَاؤُهَا، تَرِدُ الْمَاءَ وَتَرْعَى الشَّجَرَ، فَذَرْهَا حَتَّى يَلْقَاهَا رَبُّهَا. قَالَ: فَضَالَّةُ الْغَنَمِ؟ قَالَ: لَكَ أَوْ لِأَخِيكَ أَوْ لِلذِّئْبِ.",
                "Zeyd b. Hâlid el-Cühenî'den: Bir adam Nebî'ye (s.a.v.) buluntu mal hakkında sordu. Buyurdu: “Bağını — ya da kabını — ve kılıfını belle, sonra bir yıl ilan et, sonra ondan faydalan; sahibi gelirse ona ver.” Adam: “Yitik deve ne olacak?” dedi. Bunun üzerine yanakları kızarıncaya — ya da “yüzü kızarıncaya” — kadar öfkelendi ve: “Senin ondan ne istediğin var? Yanında su tulumu ve ayakkabısı vardır; suya gider, ağaçtan otlanır. Bırak onu, sahibi bulana kadar” buyurdu. Adam: “Yitik koyun ne olacak?” dedi. “O ya senindir, ya kardeşinindir, ya da kurdundur” buyurdu.",
                "<b>Buhârî, İlm, 28; Müslim, Lukata, 2; İbn Mâce, İkāmetü's-Salât, 48.</b> Dipnot bu rivayet vesilesiyle <b>hadislerin lafzen ve manen rivayeti</b>nin araştırılmasını ister.",
            ),
        ])
        .add_table(ComparisonTable(
            "Yitik Malın Üç Hükmü",
            ["Yitik", "Hüküm", "Gerekçe"],
            [
                ["<b>Lukata</b> (para/eşya)", "Vikā' ve ifâsını belle → <b>1 yıl ilan</b> → sonra faydalan; sahibi gelirse iade et", "Sahibi aranabilir"],
                ["<b>Dâlletü'l-ibil</b> (deve)", "<b>Dokunma, bırak</b>", "“Su tulumu ve ayakkabısı yanında” — kendini korur"],
                ["<b>Dâlletü'l-ganem</b> (koyun)", "<b>Al</b>", "“Ya senin, ya kardeşinin, ya kurdun” — korunmasızdır"],
            ],
        ))
        .add_callout(Callout(
            "caution", "Bâbın Asıl Konusu Fıkıh Değil, ÖFKEDİR",
            "Bu rivayet lukata hükümleriyle dolu olmasına rağmen Buhârî onu <b>“öğretimde öfke”</b> bâbına "
            "koymuştur: Hz. Peygamber, hoşlanmadığı bir soru karşısında <u>yanakları kızaracak kadar</u> "
            "öfkelenmiştir — yani <b>hakkı öğretirken öfke meşrûdur</b>. Râvinin “<i>vikāehâ ev kāle "
            "vi'âehâ</i>” diyerek şüphesini kaydetmesi ise <b>lafız titizliğinin</b> göstergesidir."
        ))
        .add_summary(
            "Bölüm ilmin alıcısını ve vericisini aynı anda tarif eder: yağmur meseli üç insan "
            "tipini ayırır (İlim 12), “hayruküm” hadisi en hayırlıyı öğrenen + öğreten olarak "
            "belirler (İlim 13) ve son rivayet, öğretenin duygusal tavrına dair sınırı çizer: "
            "yanlış bir tutum karşısında öfke, öğretimin bir parçası olabilir (İlim 14)."
        )
    )

    # =======================================================================
    # 5. BÖLÜM — Tekrar, Kadınların Eğitimi ve Hadise Düşkünlük (İlim 15–18)
    # =======================================================================
    ch5 = Chapter(
        number=5,
        title="Tekrar, Kadınların Eğitimi ve Hadise Düşkünlük",
        subtitle="Kitâbü'l-İlm 15–18 · Üç bâb: sözü üç kez tekrarlamak, kadınlara ayrı gün ve hırs ale'l-hadîs",
        key_terms=[
            KeyTerm("Tekrâr (selâsen)", "Sözün <b>üç kez</b> tekrarlanması. Bâb başlığı gerekçeyi verir: <b>“li-yüfheme anh”</b> — kendisinden anlaşılsın diye."),
            KeyTerm("İsbâğu'l-vudû'", "Abdesti <b>tam alma</b>, uzuvları eksiksiz yıkama. “Veylün li'l-a'kābi mine'n-nâr” uyarısının hükmü budur."),
            KeyTerm("A'kāb", "Topuklar. Aceleyle mesh edilip kuru bırakılan topuklar, abdestin eksik kaldığının işaretidir — uyarı bu yüzden <b>yüksek sesle</b> yapılmıştır."),
            KeyTerm("Hırs ale'l-hadîs", "Hadise düşkünlük. Bâbın adı, Hz. Peygamber'in Ebû Hüreyre'ye söylediği <b>“hırsıke ale'l-hadîs”</b> ifadesinden alınmıştır."),
        ],
    )
    ch5.pages.append(
        ChapterPage()
        .add_terms(ch5.key_terms)
        .add_ayat("Bâb: Men Eâde'l-Hadîse Selâsen li-Yüfheme anh", [
            Ayah(
                "İlim 15 — Sözü Üç Kez Tekrarlaması",
                "عَنْ أَنَسٍ عَنِ النَّبِيِّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ أَنَّهُ كَانَ إِذَا سَلَّمَ سَلَّمَ ثَلَاثًا، وَإِذَا تَكَلَّمَ بِكَلِمَةٍ أَعَادَهَا ثَلَاثًا.",
                "Enes'ten, Nebî (s.a.v.) hakkında: “Selâm verdiğinde üç kez selâm verir, bir söz söylediğinde onu üç kez tekrar ederdi.”",
                "<b>Buhârî, İlm, 30; Tirmizî, İsti'zân, 28.</b> Üçlemenin iki uygulaması ayrı ayrı ezberlenir: <b>selâmda</b> ve <b>sözde</b>.",
            ),
            Ayah(
                "İlim 16 — “Vay o topuklara ateşten!”",
                "عَنْ عَبْدِ اللهِ بْنِ عَمْرٍو قَالَ: تَخَلَّفَ رَسُولُ اللهِ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ فِي سَفَرٍ سَافَرْنَاهُ فَأَدْرَكَنَا وَقَدْ أَرْهَقْنَا الصَّلَاةَ صَلَاةَ الْعَصْرِ وَنَحْنُ نَتَوَضَّأُ فَجَعَلْنَا نَمْسَحُ عَلَى أَرْجُلِنَا، فَنَادَى بِأَعْلَى صَوْتِهِ: وَيْلٌ لِلْأَعْقَابِ مِنَ النَّارِ. أَسْبِغُوا الْوُضُوءَ. مَرَّتَيْنِ أَوْ ثَلَاثًا.",
                "Abdullah b. Amr'dan: Çıktığımız bir yolculukta Resûlullah (s.a.v.) geride kalmıştı; ikindi namazını geciktirmiş hâlde abdest alırken bize yetişti; biz ayaklarımıza (aceleyle) mesh ediyorduk. Bunun üzerine sesinin var gücüyle seslendi: “Vay o topuklara ateşten! Abdesti tam alın!” — bunu iki veya üç kez (söyledi).",
                "<b>Buhârî, İlm, 30.</b> Abdestin tam alınmasıyla ilgili olarak ayrıca: <b>Müslim, Tahâret, 27; Nesâî, Tahâret, 89; Ebû Dâvûd, Tahâret, 46.</b>",
            ),
        ])
    )
    ch5.pages.append(
        ChapterPage()
        .add_ayat("Bâb: Hel Yüc'alü li'n-Nisâi Yevmün alâ Hıdetin fi'l-İlm?", [
            Ayah(
                "İlim 17 — Kadınlara Ayrı Bir Öğretim Günü",
                "عَنْ أَبِي سَعِيدٍ الْخُدْرِيِّ قَالَ: قَالَتِ النِّسَاءُ لِلنَّبِيِّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ: غَلَبَنَا عَلَيْكَ الرِّجَالُ، فَاجْعَلْ لَنَا يَوْمًا مِنْ نَفْسِكَ. فَوَعَدَهُنَّ يَوْمًا لَقِيَهُنَّ فِيهِ فَوَعَظَهُنَّ وَأَمَرَهُنَّ. فَكَانَ فِيمَا قَالَ لَهُنَّ: مَا مِنْكُنَّ امْرَأَةٌ تُقَدِّمُ ثَلَاثَةً مِنْ وَلَدِهَا إِلَّا كَانَ لَهَا حِجَابًا مِنَ النَّارِ. فَقَالَتِ امْرَأَةٌ: وَاثْنَيْنِ؟ فَقَالَ: وَاثْنَيْنِ.",
                "Ebû Saîd el-Hudrî'den: Kadınlar Nebî'ye (s.a.v.): “Erkekler seni bizden aldı; kendinden bize de bir gün ayır” dediler. O da onlara bir gün vaad etti; o gün onlarla buluştu, öğüt verdi ve (bazı şeyleri) emretti. Onlara söyledikleri arasında şu da vardı: “İçinizden hangi kadın çocuklarından üçünü (kendinden) önce gönderirse, o çocuklar onun için ateşe karşı bir perde olur.” Bir kadın: “Ya iki olursa?” dedi. “İki de (öyledir)” buyurdu.",
                "<b>Buhârî, İlm, 35.</b> Bâb başlığı <b>soru kipindedir</b> (“…ayrılır mı?”) ve hadis bu soruyu <b>olumlu</b> cevaplar.",
            ),
        ])
        .add_block(BulletBlock(1, "Bâbdan Çıkan İki Sonuç", [
            "<b>Kadınların eğitim hakkı:</b> Talep kadınlardan gelmiş, Hz. Peygamber talebi <b>kabul edip "
            "gün tayin etmiştir</b>. Buhârî bâbı soru kipiyle kurarak hükmü hadise söyletir — bu, "
            "<b>terceme</b> tekniğinin tipik örneğidir.",
            "<b>Soru sorma serbestliği:</b> Bir kadının “<i>ve'sneteyn?</i>” (ya iki olursa?) sorusu üzerine "
            "hüküm <b>genişletilmiştir</b>. Aynı serbestlik, öğrenmenin önündeki çekingenliğin nasıl "
            "aşılacağını gösterir.",
            "Terimler: <b>“tükaddimu selâseten min veledihâ”</b> = üç çocuğunu (ölümle) önden göndermek; "
            "<b>“hicâben mine'n-nâr”</b> = ateşe karşı perde.",
        ]))
        .add_ayat("Bâb: el-Hırs ale'l-Hadîs", [
            Ayah(
                "İlim 18 — Şefaate En Çok Nail Olacak Kimdir?",
                "عَنْ أَبِي هُرَيْرَةَ أَنَّهُ قَالَ: قُلْتُ يَا رَسُولَ اللهِ، مَنْ أَسْعَدُ النَّاسِ بِشَفَاعَتِكَ يَوْمَ الْقِيَامَةِ؟ قَالَ رَسُولُ اللهِ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ: لَقَدْ ظَنَنْتُ — يَا أَبَا هُرَيْرَةَ — أَنْ لَا يَسْأَلَنِي عَنْ هَذَا الْحَدِيثِ أَحَدٌ أَوَّلَ مِنْكَ، لِمَا رَأَيْتُ مِنْ حِرْصِكَ عَلَى الْحَدِيثِ. أَسْعَدُ النَّاسِ بِشَفَاعَتِي يَوْمَ الْقِيَامَةِ مَنْ قَالَ لَا إِلَهَ إِلَّا اللهُ خَالِصًا مِنْ قَلْبِهِ أَوْ نَفْسِهِ.",
                "Ebû Hüreyre'den: “Ey Allah'ın Resûlü, kıyamet günü şefaatinle en mesut olacak kimdir?” dedim. Resûlullah (s.a.v.): “Ey Ebû Hüreyre! Hadise olan düşkünlüğünü gördüğüm için, bu hadisi bana senden önce kimsenin sormayacağını zaten tahmin ediyordum. Kıyamet günü şefaatimle en mesut olacak kişi, kalbinden — ya da nefsinden — hâlis olarak ‘Lâ ilâhe illallâh' diyendir” buyurdu.",
                "<b>Buhârî, Rikāk, 5; İlm, 33.</b> Kaynak, Ebû Hüreyre'nin dipnot biyografisinde bu diyalogu, <b>çok hadis rivayet etmesinin bizzat Hz. Peygamber tarafından takdir edildiğinin</b> delili olarak gösterir.",
            ),
        ])
    )
    ch5.pages.append(
        ChapterPage()
        .add_person(EBU_HUREYRE)
        .add_summary(
            "Üç kısa bâb, öğretimin üç ayrı yönünü tamamlar: tekrar (anlaşılsın diye söz üç kez "
            "söylenir, önemli bir hata yüksek sesle düzeltilir — İlim 15–16), muhatap çeşitliliği "
            "(kadınlara ayrı gün ayrılır ve soruları hükmü genişletir — İlim 17) ve talebenin "
            "hırsı (öğrenme isteği, öğretmenin ilgisini çeker ve rivayet zincirini besler — İlim 18). "
            "Son rivayet aynı zamanda şefaatin şartını verir: ihlâs."
        )
    )

    # =======================================================================
    # 6. BÖLÜM — İlmin Yazılması ve Anlayışı Gözetmek (İlim 19–22)
    # =======================================================================
    ch6 = Chapter(
        number=6,
        title="İlmin Yazılması ve Anlayışı Gözetmek",
        subtitle="Kitâbü'l-İlm 19–22 · Ebû Şâh, mutâbaat kaydı, Kırtâs hâdisesi ve vizeyi kapatan Kâbe rivayeti",
        key_terms=[
            KeyTerm("Kitâbetü'l-ilm", "İlmin <b>yazıyla tespiti</b>. Bâb, hem yazma iznini (Ebû Şâh) hem yazmama örneğini (Ebû Hüreyre) hem de Kırtâs hâdisesini <b>aynı yerde</b> toplar."),
            KeyTerm("Mutâbaat", "Bir hadisin, <b>farklı bir râvî</b> tarafından tamamen veya kısmen <b>aynı senedle</b> rivayet edilerek desteklenmesi. Metinde “tâbeahû Ma'mer” kaydıyla görünür."),
            KeyTerm("Şâhid", "Aynı ya da başka bir sahâbîden gelen <b>benzer muhtevalı</b> ikinci hadis. Ayırt etme ipucu: mutâbaat <b>sened</b>, şâhid <b>metin</b> benzerliğidir."),
            KeyTerm("Reziyye", "Musibet. İbn Abbâs'ın Kırtâs hâdisesi için kullandığı ifade: <b>“inne'r-reziyyete külle'r-reziyye”</b> — asıl musibet, Resûlullah ile yazısı arasına girilmesidir."),
        ],
    )
    ch6.pages.append(
        ChapterPage()
        .add_terms(ch6.key_terms)
        .add_ayat("Bâb: Kitâbetü'l-İlm (İlmin Yazılması)", [
            Ayah(
                "İlim 19 — Mekke'nin Fethi Hutbesi ve “Ebû Şâh için yazın!”",
                "عَنْ أَبِي هُرَيْرَةَ قَالَ: لَمَّا فَتَحَ اللهُ عَزَّ وَجَلَّ عَلَى رَسُولِ اللهِ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ مَكَّةَ قَامَ فِي النَّاسِ فَحَمِدَ اللهَ وَأَثْنَى عَلَيْهِ ثُمَّ قَالَ: إِنَّ اللهَ حَبَسَ عَنْ مَكَّةَ الْفِيلَ وَسَلَّطَ عَلَيْهَا رَسُولَهُ وَالْمُؤْمِنِينَ، وَإِنَّهَا لَمْ تَحِلَّ لِأَحَدٍ كَانَ قَبْلِي، وَإِنَّهَا أُحِلَّتْ لِي سَاعَةً مِنْ نَهَارٍ، وَإِنَّهَا لَنْ تَحِلَّ لِأَحَدٍ بَعْدِي. فَلَا يُنَفَّرُ صَيْدُهَا وَلَا يُخْتَلَى شَوْكُهَا وَلَا تَحِلُّ سَاقِطَتُهَا إِلَّا لِمُنْشِدٍ. وَمَنْ قُتِلَ لَهُ قَتِيلٌ فَهُوَ بِخَيْرِ النَّظَرَيْنِ: إِمَّا أَنْ يُفْدَى وَإِمَّا أَنْ يُقْتَلَ. فَقَالَ الْعَبَّاسُ: إِلَّا الْإِذْخِرَ يَا رَسُولَ اللهِ، فَإِنَّا نَجْعَلُهُ فِي قُبُورِنَا وَبُيُوتِنَا. فَقَالَ: إِلَّا الْإِذْخِرَ. فَقَامَ أَبُو شَاهٍ — رَجُلٌ مِنْ أَهْلِ الْيَمَنِ — فَقَالَ: اكْتُبُوا لِي يَا رَسُولَ اللهِ. فَقَالَ رَسُولُ اللهِ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ: اكْتُبُوا لِأَبِي شَاهٍ.",
                "Ebû Hüreyre'den: Allah, Resûlü'ne Mekke'nin fethini nasip edince ayağa kalkıp Allah'a hamd ve senâ etti, sonra buyurdu: “Allah Mekke'den fili alıkoydu ve oraya Resûlü'nü ve mü'minleri musallat etti. Orası benden önce hiç kimseye helâl olmamıştır; bana da gündüzün bir saati helâl kılınmıştır ve benden sonra hiç kimseye helâl olmayacaktır. Av hayvanı ürkütülmez, dikeni koparılmaz, düşmüş eşyası — ilan edecek kimse dışında — kimseye helâl olmaz. Kimin bir yakını öldürülürse iki şıktan hayırlısını seçer: ya diyet alır ya da kısas yapar.” Abbâs: “İzhir otu müstesna olsun ey Allah'ın Resûlü; çünkü biz onu kabirlerimizde ve evlerimizde kullanıyoruz” dedi. “İzhir müstesna” buyurdu. Sonra Yemen halkından Ebû Şâh adlı bir adam kalkıp: “Bunu bana yazın ey Allah'ın Resûlü” dedi. Resûlullah (s.a.v.): “Ebû Şâh için yazın!” buyurdu.",
                "<b>Müslim, Hac, 447; Buhârî, İlm, 39.</b> Sened: Züheyr b. Harb + Ubeydullah b. Saîd ← Velîd b. Müslim ← <b>el-Evzâî</b> ← Yahyâ b. Ebî Kesîr ← Ebû Seleme ← Ebû Hüreyre.",
            ),
        ])
    )
    ch6.pages.append(
        ChapterPage()
        .add_callout(Callout(
            "focus", "Ezberlenecek Cümle: “Üktübû li-Ebî Şâh”",
            "Bu üç kelime, <b>kitâbetü'l-ilm</b> tartışmasının anahtarıdır: hadisin yazılmasına <u>açık ve "
            "sözlü izin</u> verildiğinin en meşhur delilidir. Rivayet ayrıca <b>Mekke'nin haram kılınışına</b> "
            "dair hükümleri (av, diken, lukata, kısas–diyet muhayyerliği ve <b>izhir</b> istisnası) tek "
            "metinde toplar."
        ))
        .add_ayat("Bâb: Kitâbetü'l-İlm (devam)", [
            Ayah(
                "İlim 20 — “O yazıyordu, ben yazmıyordum”",
                "عَنْ أَبِي هُرَيْرَةَ يَقُولُ: مَا مِنْ أَصْحَابِ النَّبِيِّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ أَحَدٌ أَكْثَرُ حَدِيثًا عَنْهُ مِنِّي إِلَّا مَا كَانَ مِنْ عَبْدِ اللهِ بْنِ عَمْرٍو، فَإِنَّهُ كَانَ يَكْتُبُ وَلَا أَكْتُبُ. تَابَعَهُ مَعْمَرٌ عَنْ هَمَّامٍ عَنْ أَبِي هُرَيْرَةَ.",
                "Ebû Hüreyre şöyle derdi: “Nebî'nin (s.a.v.) ashâbı içinde ondan benden daha çok hadis rivayet eden yoktur — ancak Abdullah b. Amr müstesna; çünkü o yazıyordu, ben yazmıyordum.” — Bu rivayette Ma'mer, Hemmâm'dan, o da Ebû Hüreyre'den (aynı yolla) ona mutâbaat etmiştir.",
                "<b>Buhârî, İlm, 39.</b> Metnin sonundaki <b>“تَابَعَهُ مَعْمَرٌ”</b> bir <b>mutâbaat</b> kaydıdır; kaynak tam bu noktada mutâbaat kavram ailesini dipnotta tanımlar.",
            ),
        ])
        .add_table(ComparisonTable(
            "Mutâbaat Ailesi — Kaynağın 49. Dipnotundaki Beş Terim",
            ["Terim", "Tanım"],
            [
                ["<b>Mutâbaat</b>", "Bir hadisin lafızlarına veya mânasına uygun başka bir hadisin, <b>farklı bir râvî</b> tarafından tamamen veya kısmen <b>aynı senedle</b> rivayet edilmesi; iki hadis ve râvî birbirini destekler"],
                ["<b>Âdıd</b>", "Bir hadisi <b>destekleyen ikinci hadis</b>; ya da kusurlu bir haberin <b>bu kusurunu gideren</b> diğer haber"],
                ["<b>Şâhid</b>", "Bir hadise, aynı sahâbîden ya da <b>başka bir sahâbîden</b> gelen <b>benzer muhtevalı</b> ikinci hadis"],
                ["<b>Mutâbi'</b>", "Bir hadisin <b>benzerini rivayet eden râvî</b>"],
                ["<b>Mutâba' aleyh</b>", "Benzeri <b>başka bir râvî tarafından da rivayet edilmiş olan</b> hadis ya da râvî"],
            ],
        ))
        .add_person(ABDULLAH_B_AMR)
    )
    ch6.pages.append(
        ChapterPage()
        .add_ayat("Bâb: Kitâbetü'l-İlm — Kırtâs Hâdisesi", [
            Ayah(
                "İlim 21 — “Bana bir yazı malzemesi getirin”",
                "عَنِ ابْنِ عَبَّاسٍ قَالَ: لَمَّا اشْتَدَّ بِالنَّبِيِّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ وَجَعُهُ قَالَ: ائْتُونِي بِكِتَابٍ أَكْتُبْ لَكُمْ كِتَابًا لَا تَضِلُّوا بَعْدَهُ. قَالَ عُمَرُ: إِنَّ النَّبِيَّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ غَلَبَهُ الْوَجَعُ وَعِنْدَنَا كِتَابُ اللهِ حَسْبُنَا. فَاخْتَلَفُوا وَكَثُرَ اللَّغَطُ. قَالَ: قُومُوا عَنِّي، وَلَا يَنْبَغِي عِنْدِي التَّنَازُعُ. فَخَرَجَ ابْنُ عَبَّاسٍ يَقُولُ: إِنَّ الرَّزِيَّةَ كُلَّ الرَّزِيَّةِ مَا حَالَ بَيْنَ رَسُولِ اللهِ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ وَبَيْنَ كِتَابِهِ.",
                "İbn Abbâs'tan: Nebî'nin (s.a.v.) hastalığı ağırlaşınca: “Bana bir yazı malzemesi getirin; size bir yazı yazayım da ondan sonra sapmayasınız” buyurdu. Ömer: “Nebî'ye (s.a.v.) ağrı galebe çaldı; yanımızda Allah'ın Kitabı var, o bize yeter” dedi. Bunun üzerine ihtilâf ettiler ve gürültü çoğaldı. (Hz. Peygamber): “Yanımdan kalkın; benim yanımda çekişme yakışık almaz” buyurdu. İbn Abbâs dışarı çıkarken şöyle diyordu: “Asıl musibet, Resûlullah (s.a.v.) ile yazısı arasına girilmesidir.”",
                "<b>Buhârî, İlm, 39; Müslim, Vasiyyet, 20; İbn Hibbân, Sahîh, XIV, 562.</b> Sened: Yahyâ b. Süleymân ← İbn Vehb ← Yûnus ← <b>ez-Zührî</b> ← Ubeydullah b. Abdillah ← İbn Abbâs. <i>Legat</i> = karışık gürültü.",
            ),
        ])
        .add_callout(Callout(
            "insight", "Buhârî Neden Üçünü Aynı Bâbda Topladı?",
            "Bâb, yazma meselesinin <b>üç ayrı yüzünü</b> yan yana koyar: <b>(1)</b> açık izin — “Ebû Şâh "
            "için yazın” (İlim 19); <b>(2)</b> yazmayan bir sahâbînin, yazan bir sahâbîyi <u>üstün</u> "
            "sayması (İlim 20); <b>(3)</b> yazma teklifinin <u>gerçekleşmediği</u> Kırtâs hâdisesi "
            "(İlim 21). Ezberlenecek üç ifade: <b>“üktübû li-Ebî Şâh”</b> · <b>“hasbünâ kitâbullâh”</b> "
            "(Hz. Ömer) · <b>“er-reziyyete külle'r-reziyye”</b> (İbn Abbâs)."
        ))
        .add_person(ZUHRI)
    )
    ch6.pages.append(
        ChapterPage()
        .add_ayat("Bâb: Men Tereke Ba'da'l-İhtiyâr Mehâfete en Yaksura Fehmu Ba'di'n-Nâs anh", [
            Ayah(
                "İlim 22 — Hz. Âişe'ye Kâbe Sırrı (VİZENİN SON RİVAYETİ)",
                "عَنِ الْأَسْوَدِ قَالَ: قَالَ لِي ابْنُ الزُّبَيْرِ: كَانَتْ عَائِشَةُ تُسِرُّ إِلَيْكَ كَثِيرًا، فَمَا حَدَّثَتْكَ فِي الْكَعْبَةِ؟ قُلْتُ: قَالَتْ لِي: قَالَ النَّبِيُّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ: يَا عَائِشَةُ، لَوْلَا قَوْمُكِ حَدِيثٌ عَهْدُهُمْ — قَالَ ابْنُ الزُّبَيْرِ: بِكُفْرٍ — لَنَقَضْتُ الْكَعْبَةَ فَجَعَلْتُ لَهَا بَابَيْنِ: بَابٌ يَدْخُلُ النَّاسُ وَبَابٌ يَخْرُجُونَ. فَفَعَلَهُ ابْنُ الزُّبَيْرِ.",
                "el-Esved'den: İbnü'z-Zübeyr bana: “Âişe sana çok sır verirdi; Kâbe hakkında sana ne anlattı?” dedi. Dedim ki: Bana şöyle demişti: Nebî (s.a.v.) buyurdu ki: “Ey Âişe! Kavmin (Kureyş) yakın zamanda — İbnü'z-Zübeyr: ‘küfürden’ (çıkmış) — olmasaydı, Kâbe'yi yıkar ve ona iki kapı yapardım: bir kapıdan insanlar girer, bir kapıdan çıkarlardı.” İbnü'z-Zübeyr bunu (sonradan) uyguladı.",
                "<b>Buhârî, İlm, 48.</b> Sened: Ubeydullah b. Mûsâ ← İsrâîl ← Ebû İshâk ← el-Esved. İbnü'z-Zübeyr, halifeliği döneminde Kâbe'yi bu hadise dayanarak <b>iki kapılı</b> inşa etmiş, sonra Haccâc eski hâline döndürmüştür.",
            ),
            Ayah(
                "Şerh — el-Mühelleb: Fitne Korkusuyla Terk",
                "شَرْحٌ: قَالَ الْمُهَلَّبُ: فِيهِ أَنَّهُ قَدْ يُتْرَكُ شَيْءٌ مِنَ الْأَمْرِ بِالْمَعْرُوفِ إِذَا خُشِيَ مِنْهُ أَنْ يَكُونَ سَبَبًا لِفِتْنَةِ قَوْمٍ يُنْكِرُونَهُ وَيُسْرِعُونَ إِلَى خِلَافِهِ وَاسْتِبْشَاعِهِ. وَفِيهِ: أَنَّ النُّفُوسَ تُحِبُّ أَنْ تُسَاسَ بِمَا تَأْنَسُ إِلَيْهِ فِي دِينِ اللهِ مِنْ غَيْرِ الْفَرَائِضِ، بِأَنْ يُتْرَكَ وَيُرْفَعَ عَنِ النَّاسِ مَا يُنْكِرُونَ مِنْهَا.",
                "Mühelleb dedi ki: Bu hadiste, bir emr-i bi'l-ma'rûfun, onu yadırgayacak ve hemen karşı çıkıp çirkin görecek bir topluluğun fitnesine sebep olmasından korkulduğunda terk edilebileceği vardır. Yine bunda, nefislerin, Allah'ın dininde farzlar dışındaki hususlarda ülfet ettikleri şeyle yönetilmeyi sevdiği — yani yadırgadıkları şeyin onlardan kaldırılması gerektiği — vardır.",
                "<b>İbn Battâl, Şerhu Sahîhi'l-Buhârî, I, 205.</b> Anahtar ilke: <b>maslahat–mefsedet dengesi</b>. Dikkat: bu, <b>farzlar dışındaki</b> hususlar için geçerlidir.",
            ),
        ])
        .add_callout(Callout(
            "route", "Buradan Sonrası Finalin Konusu",
            "22. rivayetin bulunduğu bu bâb, <b>finalin de ilk bâbıdır</b>. Final kitabı aynı bâbın devamı "
            "olan <b>İlim 23</b> (Hz. Ali: “İnsanlara anlayacaklarını anlatın”) ve <b>İlim 24</b> (Muâz b. "
            "Cebel'e söylenen sır) rivayetleriyle açılır. Üç rivayet birlikte tek bir ilkeyi kurar: "
            "<b>muhatabın kavrayış seviyesi gözetilir</b>; anlaşılmayacak bir doğru, daha büyük bir "
            "yanlışa kapı aralıyorsa geciktirilebilir."
        ))
        .add_summary(
            "Bölüm iki tartışmayı kapatır. Kitâbetü'l-ilm: yazmaya açık izin vardır (İlim 19), yazan "
            "sahâbî yazmayan tarafından üstün sayılır (İlim 20), ama Kırtâs hâdisesi meselenin sahâbe "
            "içinde de tartışıldığını gösterir (İlim 21). Anlayışı gözetmek: Kâbe rivayeti, doğru bir "
            "tercihin bile fitne doğuracaksa terk edilebileceğini söyler (İlim 22)."
        )
    )

    chapters = [ch1, ch2, ch3, ch4, ch5, ch6]

    # =======================================================================
    # KAVRAMLAR SÖZLÜĞÜ
    # =======================================================================
    glossary = [
        Concept("Metûnü'l-Hadîs", "Hadis metinleri derlemesi; senediyle verilen rivayetler, Arapça şerh alıntıları ve usûl dipnotlarından oluşan ders kitabı türü.", "Ders kaynağı", 1),
        Concept("Kitâb", "Hadis eserlerinde ana bölüm. Kitâbü'l-İlm, Kitâbü'l-Îmân gibi.", "Tasnif terimi", 1),
        Concept("Bâb", "Bir eserde ana bölümden (kitâbdan) sonra gelen alt bölüm.", "Tasnif terimi", 1),
        Concept("Terceme", "Kitaplardaki ana bölüm (kitâb) ve alt bölüm (bâb) başlığına verilen isim. “Buhârî'nin fıkhı terâcimindedir” sözü buna dayanır.", "Tasnif terimi", 1),
        Concept("Muallak (Ta'lîk)", "Senedin baş tarafı hazfedilerek “وقال فلان” kalıbıyla nakledilen rivayet. Bu ünitede İlim 1, 2, 3 ve 10 muallaktır.", "İlim 1–3, 10", 1),
        Concept("Mevkūf", "Senedi sahâbîde duran rivayet; Hz. Peygamber'e değil bir sahâbîye nispet edilir.", "İlim 2, 3, 10", 1),
        Concept("Merfû'", "Hz. Peygamber'e nispet edilen söz, fiil veya takrir.", "İlim 1, 4–9, 11–22", 1),
        Concept("Maktû'", "Tâbiîye nispet edilen söz veya fiil. Bu ünitede rivayet olarak yoktur; şerh nakilleri bu türdendir.", "Usûl dipnotu", 1),
        Concept("Kudsî", "Lafzı Hz. Peygamber'e, mânası Allah'a ait olan hadis. Bu ünitede örneği yoktur.", "Usûl dipnotu", 1),
        Concept("Samsâme", "Keskin, kesici kılıç. Ebû Zerr'in tebliğ kararlılığını anlattığı sözde geçer.", "İlim 2", 1),
        Concept("Verâsetü'l-enbiyâ", "“Âlimler peygamberlerin vârisleridir” ilkesi; bırakılan miras mal değil ilimdir.", "İlim 1", 1),
        Concept("Rabbânî", "Hilim sahibi fakih; insanları ilmin küçüğünden büyüğüne doğru yetiştiren kimse.", "İlim 3", 1),
        Concept("Tedrîc", "Öğretimde basitten karmaşığa ilerleme ilkesi; “sıgāru'l-ilm kable kibârih” ifadesiyle anlatılır.", "İlim 3", 1),
        Concept("Tahammül ve edâ", "Hadisi hocadan alma (tahammül) ve başkasına nakletme (edâ). Nakilde kullanılan kalıplara edâ sîgaları denir.", "İlim 4 dipnotu", 1),
        Concept("Semi'tü", "“İşittim” — hocadan bizzat dinlemeyi bildiren, edâ sîgalarının en kuvvetlisi.", "İlim 4", 1),
        Concept("An'ane", "“عن” ile yapılan nakil; bağlantıyı belirsiz bıraktığı için sîgaların en zayıfı sayılır, tedlîs şüphesi taşır.", "İlim 4 dipnotu", 1),
        Concept("Âsâr", "Sahâbe ve tâbiîn sözleri; hadis–haber–eser ayrımında “eser”in çoğuludur.", "İlim 4 şerhi", 1),
        Concept("Rubbe mübelliğin ev'â min sâmi'", "“Nice kendisine tebliğ edilen, işitenden daha kavrayışlıdır.” Rivayetin sürdürülmesinin gerekçesi.", "İlim 5", 2),
        Concept("Mîsâk (âlimlerden alınan)", "Allah'ın âlimlerden aldığı, ilmi açıklama ve gizlememe sözü; Âl-i İmrân 3/187'ye dayandırılır.", "İlim 5 şerhi", 2),
        Concept("Tehavvül", "Uygun zamanı gözeterek, aralıklarla öğüt verme.", "İlim 6–7", 2),
        Concept("Se'âme", "Usanç, bıkkınlık; öğüdün aralıklı verilmesinin gerekçesidir.", "İlim 6–7", 2),
        Concept("Teysîr", "Kolaylaştırma; “yessirû ve lâ tuassirû” emrinin adı.", "İlim 8", 2),
        Concept("Kavlî sünnet", "Hz. Peygamber'in Kur'an dışındaki sözleri.", "İlim 6 dipnotu", 2),
        Concept("Fiilî sünnet", "Hz. Peygamber'in davranış ve uygulamalarının anlatımı.", "İlim 6 dipnotu", 2),
        Concept("Takrîrî sünnet", "Hz. Peygamber'in muttali olduğu bir olayı ya da sahâbî uygulamasını tasvip etmesi.", "İlim 6 dipnotu", 2),
        Concept("Musannef", "İbâdet, muâmelât ve diğer konulara ait hadisleri bâblar hâlinde toplayan eser türü; Abdürrezzâk ve İbn Ebî Şeybe örnekleri.", "İlim 7 dipnotu", 2),
        Concept("Fıkh", "Derin anlayış; “yüfakkıhhu fi'd-dîn” ifadesiyle hayır alâmeti sayılır.", "İlim 1, 9", 3),
        Concept("Kāsım", "Taksim eden. “İnnemâ ene kāsim va'llâhu yu'tî” — veren Allah'tır.", "İlim 9", 3),
        Concept("Tâife-i mansûra", "Hak üzere sebat edip muhaliflerin zarar veremeyeceği topluluk; İlim 9'un son cümlesinde geçer.", "İlim 9", 3),
        Concept("Tesevvüd", "Baş/reis olmak; aile reisi olmak. “Tefakkahû kable en tüsevvedû” emrinin anahtar kelimesi.", "İlim 10", 3),
        Concept("İğtibât (Gıbta)", "Nimetin sahibinden gitmesini istemeden benzerini temenni etmek; hased değildir, meşrûdur.", "İlim 11", 3),
        Concept("Hased", "Nimetin sahibinden gitmesini ve kendine geçmesini istemek; haramdır.", "İlim 11", 3),
        Concept("Hikmet", "Bu hadiste ilim + onunla hükmetmek + onu öğretmek üçlüsü; gıbtaya konu olan iki nimetten biridir.", "İlim 11", 3),
        Concept("Alime ve alleme", "“Öğrendi ve öğretti”; bâbın adı ve üstünlüğün şartı.", "İlim 12–13", 4),
        Concept("Nakıyye", "Suyu kabul edip bol ürün veren temiz toprak; öğrenip öğreten âlimin misali.", "İlim 12", 4),
        Concept("Ecâdib", "Suyu emmeyip tutan sert toprak; anlamasa da nakleden râvinin misali.", "İlim 12", 4),
        Concept("Kî'ân", "Ne su tutan ne ot bitiren düz kayalık; ilme başını kaldırmayanın misali.", "İlim 12", 4),
        Concept("Lukata", "Buluntu mal; bir yıl ilan edildikten sonra faydalanılır, sahibi gelirse iade edilir.", "İlim 14", 4),
        Concept("Vikā'", "Kesenin ağız bağı; lukatanın tanınması için bellenmesi gereken alâmetlerden.", "İlim 14", 4),
        Concept("İfâs", "Lukatanın kabı/kılıfı; vikā' ile birlikte bellenir.", "İlim 14", 4),
        Concept("Ta'rîf", "Buluntu malın bir yıl boyunca ilan edilmesi.", "İlim 14", 4),
        Concept("Dâlletü'l-ibil", "Yitik deve; kendini koruyabildiği için alınmaz, bırakılır.", "İlim 14", 4),
        Concept("Lafzen rivayet", "Hadisin kelimesi kelimesine nakledilmesi.", "İlim 14 dipnotu", 4),
        Concept("Manen rivayet", "Hadisin mânası korunarak nakledilmesi.", "İlim 14 dipnotu", 4),
        Concept("Tekrâr (selâsen)", "Anlaşılsın diye sözün üç kez tekrarlanması.", "İlim 15", 5),
        Concept("İsbâğu'l-vudû'", "Abdesti tam alma, uzuvları eksiksiz yıkama.", "İlim 16", 5),
        Concept("A'kāb", "Topuklar; kuru bırakılması abdestin eksikliğine işaret eder.", "İlim 16", 5),
        Concept("Hicâben mine'n-nâr", "“Ateşe karşı perde”; önden gönderilen çocukların annesi için oluşturduğu koruma.", "İlim 17", 5),
        Concept("Hırs ale'l-hadîs", "Hadise düşkünlük; Ebû Hüreyre'nin bu vasfı bizzat Hz. Peygamber tarafından takdir edilmiştir.", "İlim 18", 5),
        Concept("İhlâs", "“Hâlisan min kalbihî” — şefaate nail olmanın şartı olarak zikredilen kalp samimiyeti.", "İlim 18", 5),
        Concept("Sahîfe-i Sahîha", "Ebû Hüreyre'den nakledilen hadis sahîfesi; bir bölümü Sahîfetü Hemmâm adıyla (138 hadis) günümüze ulaşmıştır.", "İlim 18 dipnotu", 5),
        Concept("Kitâbetü'l-ilm", "İlmin yazıyla tespiti; bâb hem izni hem tartışmayı bir arada verir.", "İlim 19–21", 6),
        Concept("İzhir", "Mekke'nin haram kılınışında istisna edilen ot; kabirlerde ve evlerde kullanılırdı.", "İlim 19", 6),
        Concept("Münşid", "İlan eden kimse; Mekke'de düşmüş eşya yalnızca onun için helâldir.", "İlim 19", 6),
        Concept("Mutâbaat", "Bir hadisin, farklı bir râvî tarafından aynı senedle desteklenmesi; metinde “tâbeahû” ile görünür.", "İlim 20", 6),
        Concept("Mutâbi'", "Bir hadisin benzerini rivayet eden râvî.", "İlim 20", 6),
        Concept("Mutâba' aleyh", "Benzeri başka bir râvî tarafından da rivayet edilmiş olan hadis ya da râvî.", "İlim 20", 6),
        Concept("Şâhid", "Aynı ya da başka bir sahâbîden gelen benzer muhtevalı ikinci hadis.", "İlim 20", 6),
        Concept("Âdıd", "Bir hadisi destekleyen, kusurlu bir haberin kusurunu gideren ikinci haber.", "İlim 20", 6),
        Concept("es-Sahîfetü's-Sâdıka", "Abdullah b. Amr'ın yazdığı hadis sahîfesi; kitâbetü'l-ilmin en erken örneklerinden.", "İlim 20", 6),
        Concept("Legat", "Karışık gürültü, bağrışma; Kırtâs hâdisesinde ihtilâfın çıktığı anı anlatır.", "İlim 21", 6),
        Concept("Reziyye", "Musibet; İbn Abbâs'ın Kırtâs hâdisesi için kullandığı ifade.", "İlim 21", 6),
        Concept("Maslahat–mefsedet dengesi", "Bir doğrunun, daha büyük bir zarara yol açacaksa terk edilebilmesi ilkesi.", "İlim 22", 6),
        Concept("Mü'telif ve muhtelif", "Yazılışı aynı, okunuşu farklı râvi isimleri; en geniş eseri İbn Mâkûlâ'nın el-İkmâl'idir.", "Râvi kimlikleri dipnotu", 6),
        Concept("Künye", "“Eb”, “ümm”, “İbn”, “bint” ile başlayan adlar; genellikle ilk erkek çocuğa nisbetle verilir.", "Râvi kimlikleri dipnotu", 6),
        Concept("Lakab", "Asıl isim dışında övmek, yermek veya bir özelliği belirtmek için takılan tanıtıcı isim.", "Râvi kimlikleri dipnotu", 6),
        Concept("Nisbe", "Kişinin kabile, soy, memleket veya mezhebe bağlılığını gösteren kelime.", "Râvi kimlikleri dipnotu", 6),
    ]

    # =======================================================================
    # TEST
    # =======================================================================
    test_questions = [
        TestQuestion(1, "Kitâbü'l-İlm'in ilk bâbında yer alan “وقال أبو ذر” kalıbıyla nakledilen samsâme sözü, rivayet türü bakımından ne olarak nitelenir?", {
            "A": "Merfû'", "B": "Mevkūf", "C": "Maktû'", "D": "Kudsî", "E": "Mütevâtir"}),
        TestQuestion(2, "“Kitâb”, “bâb” ve “terceme” terimleriyle ilgili olarak aşağıdakilerden hangisi DOĞRUDUR?", {
            "A": "Terceme, hadisin başka dile çevrilmesidir",
            "B": "Bâb, eserdeki ana bölümün adıdır",
            "C": "Terceme, kitâb ve bâb başlığına verilen isimdir",
            "D": "Kitâb, bâbdan sonra gelen alt bölümdür",
            "E": "Üç terim de aynı anlamda kullanılır"}),
        TestQuestion(3, "İbn Abbâs'ın “Rabbânî” tarifine göre rabbânî kimdir?", {
            "A": "Yalnızca Kur'an ezberleyen kimse",
            "B": "İnsanları ilmin büyüğünden önce küçüğüyle yetiştiren, hilim sahibi fakih",
            "C": "Devlet yönetiminde görev alan âlim",
            "D": "Hadisleri yazıya geçiren râvi",
            "E": "Yalnız nafile ibadetle meşgul olan zâhid"}),
        TestQuestion(4, "Kaynak, İlim 4 (süt rüyası) rivayetinin senedini bilerek tam vermiştir. Dipnotta bu vesileyle araştırılması istenen usûl konusu hangisidir?", {
            "A": "Cerh ve ta'dîl", "B": "Nâsih ve mensûh", "C": "Tahammül ve edâ yolları ile sîgaları",
            "D": "Garîbü'l-hadîs", "E": "İlelü'l-hadîs"}),
        TestQuestion(5, "Vedâ hutbesindeki “لِيُبَلِّغِ الشَّاهِدُ الْغَائِبَ” cümlesinden Aynî'nin çıkardığı hüküm nedir?", {
            "A": "Hutbenin yalnızca Mina'da okunacağı",
            "B": "Âlimin ilmi ulaşmayana tebliğ etmesinin ve anlamayana açıklamasının vâcip olduğu",
            "C": "Hadis rivayetinin sahâbeye özgü olduğu",
            "D": "Kan ve mal dokunulmazlığının yalnız hac günlerinde geçerli olduğu",
            "E": "Hadisin yalnızca yazıyla nakledilebileceği"}),
        TestQuestion(6, "Hz. Peygamber'in öğüdü “günlere yayarak” vermesinin (tehavvül) gerekçesi hadiste nasıl ifade edilmiştir?", {
            "A": "Vahyin aralıklı gelmesi", "B": "Sahâbenin çalışması gerektiği",
            "C": "Bize usanç (se'âme) gelmesinden hoşlanmaması",
            "D": "Mescidin dar olması", "E": "Yolculuk hâlinde bulunulması"}),
        TestQuestion(7, "İbn Mes'ûd'un insanlara yalnızca perşembe günleri öğüt vermesi, sünnetin hangi türünün sahâbî tarafından uygulanmasıdır?", {
            "A": "Kavlî sünnet", "B": "Fiilî sünnet", "C": "Takrîrî sünnet",
            "D": "Terkî sünnet", "E": "Kudsî sünnet"}),
        TestQuestion(8, "“Men yüridillâhu bihî hayran yüfakkıhhu fi'd-dîn” cümlesi bu ünitede iki kez geçer. Bu iki geçiş arasındaki temel fark nedir?", {
            "A": "Biri Arapça, diğeri tercümedir",
            "B": "Biri muallak (senetsiz), diğeri mevsûl (tam senetli) gelmiştir",
            "C": "Biri merfû', diğeri mevkūftur",
            "D": "Biri Buhârî'de, diğeri sadece Müslim'dedir",
            "E": "İkisinin lafızları tamamen farklıdır"}),
        TestQuestion(9, "Hz. Ömer'in “تَفَقَّهُوا قَبْلَ أَنْ تُسَوَّدُوا” sözü için Lisânü'l-Arab'da verilen iki yorumdan biri hangisidir?", {
            "A": "Hacca gitmeden önce ilim öğrenin",
            "B": "Evlenip ev sahibi olmadan, evlilik sizi ilimden alıkoymadan önce fıkıh öğrenin",
            "C": "Savaşa çıkmadan önce fıkıh öğrenin",
            "D": "Kur'an'ı ezberlemeden hadis öğrenmeyin",
            "E": "Hicret etmeden önce ilim öğrenin"}),
        TestQuestion(10, "“Lâ hasede illâ fî isneteyn” hadisindeki “hased” kelimesi ile teknik olarak kastedilen nedir ve nimetin zevâli istenir mi?", {
            "A": "Gerçek hased; nimetin zevâli istenir",
            "B": "Gıbta (iğtibât); nimetin zevâli istenmez",
            "C": "Buğz; nimetin zevâli istenir",
            "D": "Kibir; nimetin zevâli söz konusu değildir",
            "E": "Riya; nimetin artması istenir"}),
        TestQuestion(11, "Yağmur meselinde suyu emmeyip TUTAN ve böylece insanların içmesini, sulamasını ve ekin ekmesini sağlayan toprağın adı nedir?", {
            "A": "Nakıyye", "B": "Ecâdib", "C": "Kî'ân", "D": "Sahsah", "E": "Cürüz"}),
        TestQuestion(12, "“Hayruküm men tealleme'l-Kur'âne ve allemehû” hadisi üstünlüğü neye bağlar?", {
            "A": "Yalnız Kur'an'ı ezberlemeye", "B": "Yalnız Kur'an öğretmeye",
            "C": "Öğrenmek ile öğretmenin birleşmesine", "D": "Çok nafile kılmaya",
            "E": "Uzun süre itikâfa girmeye"}),
        TestQuestion(13, "Buhârî, lukata (buluntu mal) rivayetini hangi bâbda zikretmiştir?", {
            "A": "Kitâbetü'l-ilm", "B": "el-Hırs ale'l-hadîs",
            "C": "el-Gadab fi'l-mev'ıza ve't-ta'lîm (öğüt ve öğretimde öfke)",
            "D": "Fazlü'l-ilm", "E": "el-İğtibât fi'l-ilm"}),
        TestQuestion(14, "Yitik deve (dâlletü'l-ibil) hakkında verilen hüküm ve gerekçesi hangisidir?", {
            "A": "Alınır; kurda yem olmaması için",
            "B": "Bir yıl ilan edilir; sahibi bulunsun diye",
            "C": "Bırakılır; su tulumu ve ayakkabısı yanındadır, kendini korur",
            "D": "Beytülmâle teslim edilir", "E": "Kesilip fakirlere dağıtılır"}),
        TestQuestion(15, "“Men eâde'l-hadîse selâsen” bâbının başlığında tekrarın gerekçesi olarak zikredilen ifade hangisidir?", {
            "A": "Li-yuhfeza (ezberlensin diye)", "B": "Li-yüfheme anh (kendisinden anlaşılsın diye)",
            "C": "Li-yüktebe (yazılsın diye)", "D": "Li-yüştehera (yayılsın diye)",
            "E": "Li-yütlâ (okunsun diye)"}),
        TestQuestion(16, "“Veylün li'l-a'kābi mine'n-nâr” uyarısında hangi iki husus öne çıkar?", {
            "A": "Uyarının fısıltıyla yapılması ve bir kez söylenmesi",
            "B": "Abdestin tam alınması (isbâğ) ve uyarının yüksek sesle iki-üç kez tekrarlanması",
            "C": "Mest üzerine mesh edilmesi ve namazın kazaya bırakılması",
            "D": "Teyemmümün yeterli olması", "E": "Namazın cem edilmesi"}),
        TestQuestion(17, "Kadınların “Erkekler seni bizden aldı, bize de bir gün ayır” talebi karşısında Hz. Peygamber ne yapmıştır?", {
            "A": "Talebi reddetmiştir", "B": "Talebi Ebû Bekir'e havale etmiştir",
            "C": "Onlara bir gün vaad edip o gün buluşmuş, öğüt vermiş ve emirler vermiştir",
            "D": "Yalnızca mektupla cevap vermiştir", "E": "Talebi mescide gelmeleri şartına bağlamıştır"}),
        TestQuestion(18, "İlmin yazılmasına açık izin verildiğinin en meşhur delili sayılan ifade hangisidir?", {
            "A": "Hasbünâ kitâbullâh", "B": "Üktübû li-Ebî Şâh",
            "C": "Naddarallâhu imraen", "D": "Bellığû annî velev âyeten",
            "E": "İnne'r-reziyyete külle'r-reziyye"}),
        TestQuestion(19, "İlim 20'nin sonundaki “تَابَعَهُ مَعْمَرٌ عَنْ هَمَّامٍ” kaydı hangi usûl kavramına örnektir?", {
            "A": "Şâhid", "B": "Mutâbaat", "C": "Nesih", "D": "İdrâc", "E": "Tedlîs"}),
        TestQuestion(20, "Hz. Âişe'nin Kâbe rivayetinden el-Mühelleb'in çıkardığı temel ilke nedir?", {
            "A": "Kâbe'nin hiçbir şekilde tamir edilemeyeceği",
            "B": "Emr-i bi'l-ma'rûfun, bir topluluğun fitnesine sebep olacağından korkulduğunda terk edilebileceği",
            "C": "Farzların da maslahat gereği terk edilebileceği",
            "D": "Sırların hiçbir şekilde açıklanamayacağı",
            "E": "Kureyş'in imtiyazlı sayıldığı"}),
    ]

    answer_key_items = [
        AnswerItem(1, "B", "Söz, sahâbî olan Ebû Zerr'e nispet edildiği için <b>mevkūf</b>tur; kaynağın dipnotu bunu özellikle belirtir. Senedi hazfedildiği için ayrıca <b>muallak</b>tır."),
        AnswerItem(2, "C", "<b>Kitâb</b> = ana bölüm, <b>bâb</b> = alt bölüm, <b>terceme</b> = bu başlıklara verilen isimdir. Buhârî'nin fıkhının “terâciminde” olması bu terimle ilgilidir."),
        AnswerItem(3, "B", "İki tanım birlikte verilir: <b>hulemâ' fukahâ'</b> (hilim sahibi fakihler) ve <b>“sıgāru'l-ilm kable kibârih”</b> — yani <b>tedrîc</b> ilkesi."),
        AnswerItem(4, "C", "Dipnot, <b>tahammül ve edâ</b> yolları ile sîgalarını sorar. İbn Ömer'in kullandığı <b>“سمعت”</b> en kuvvetli sîgadır."),
        AnswerItem(5, "B", "<i>Umdetü'l-Kārî</i>, II, 38: âlimin tebliğ ve tebyîni <b>vâciptir</b>; bu, Allah'ın âlimlerden aldığı <b>mîsâk</b>tır (krş. Âl-i İmrân 3/187)."),
        AnswerItem(6, "C", "Metindeki ifade <b>“kerâhete's-se'âme aleynâ”</b>: usanç gelmesinden hoşlanmadığı için öğüdü aralıklı vermiştir."),
        AnswerItem(7, "B", "Hz. Peygamber'in <b>uygulaması</b> söz konusu olduğu için <b>fiilî sünnet</b>tir; İbn Mes'ûd bu uygulamayı gerekçesiyle birlikte devam ettirmiştir."),
        AnswerItem(8, "B", "<b>İlim 1</b>'de cümle bâb başlığında <b>muallak</b>, <b>İlim 9</b>'da <b>tam senediyle (mevsûl)</b> gelir. Bu, “muallak = zayıf” olmadığının delilidir."),
        AnswerItem(9, "B", "Birinci yorum: <b>evlenip ev sahibi olmadan</b> önce öğrenin. Ebû Ubeyd'in ikinci yorumu ise: <b>reis olmadan</b> önce öğrenin, sonra öğrenmekten utanırsınız."),
        AnswerItem(10, "B", "Hadisteki “hased”, teknik olarak <b>gıbta</b>dır; bâbın adı da <b>el-iğtibât</b>tır. Gıbtada <b>nimetin zevâli istenmez</b>, yalnız benzeri temenni edilir."),
        AnswerItem(11, "B", "<b>Ecâdib</b>: suyu emmez, <b>tutar</b>. Karşılığı, anlamasa da <b>nakleden</b> râvidir: kendisi içmez, başkalarını sular."),
        AnswerItem(12, "C", "“<b>Tealleme … ve allemehû</b>” — üstünlük iki fiilin <b>birleşmesine</b> bağlanmıştır; tek başına öğrenmek ya da öğretmek yeterli sayılmamıştır."),
        AnswerItem(13, "C", "Bâbın adı <b>“el-Gadab fi'l-mev'ıza ve't-ta'lîm”</b>dir: rivayet fıkhî hükümlerle dolu olsa da bâbın konusu <b>öğretimde öfke</b>dir."),
        AnswerItem(14, "C", "“<b>Meahâ sikāuhâ ve hizâuhâ</b>” — su tulumu ve ayakkabısı yanındadır; suya gider, ağaçtan otlanır. Bu yüzden <b>bırakılır</b>. Koyun ise korunmasız olduğu için alınır."),
        AnswerItem(15, "B", "Gerekçe metinde değil <b>bâb başlığındadır</b>: <b>“li-yüfheme anh”</b> — kendisinden anlaşılsın diye. Tekrarın iki uygulaması: selâmda ve sözde."),
        AnswerItem(16, "B", "Hüküm <b>isbâğu'l-vudû'</b>; uyarı ise <b>“bi-a'lâ savtihî”</b> ve <b>“merrateyni ev selâsen”</b> — yüksek sesle ve tekrarlanarak."),
        AnswerItem(17, "C", "Talebi kabul edip <b>gün tayin etmiş</b>, o gün öğüt vermiştir. Ayrıca bir kadının “<i>ve'sneteyn?</i>” sorusuyla hüküm <b>genişletilmiştir</b>."),
        AnswerItem(18, "B", "<b>“Üktübû li-Ebî Şâh”</b> — Mekke'nin fethi hutbesinin yazılı olarak verilmesi emri, <b>kitâbetü'l-ilm</b> tartışmasının anahtar delilidir."),
        AnswerItem(19, "B", "<b>Mutâbaat</b>: aynı hadisin <b>farklı bir râvî</b> tarafından <b>aynı senedle</b> desteklenmesi. İpucu: “tâbeahû” = mutâbaat. <b>Şâhid</b> ise metin benzerliğidir."),
        AnswerItem(20, "B", "el-Mühelleb: bir emr-i bi'l-ma'rûf, <b>fitneye sebep olacaksa terk edilebilir</b>. Dikkat: bu, <b>farzlar dışındaki</b> hususlar için geçerlidir."),
    ]

    return CoursePack(
        ders_klasoru="HADİS",
        course_code="HADİS",
        title='Hadis <span class="accent-word">Metinleri</span>',
        subtitle="Kitâbü'l-İlm 1–22 · Metûnü'l-Hadîs, s. 2–12",
        sinav_etiketi="Vize",
        description=(
            "Metûnü'l-Hadîs'in vize kapsamındaki yirmi iki rivayetini; ilmin faziletinden başlayıp tebliğ ve "
            "öğretim âdâbına, oradan fıkh nimeti ve ilimde gıbtaya, öğrenip öğretmenin misallerine, kadınların "
            "eğitimi ve hadise düşkünlüğe, nihayet ilmin yazılması tartışmasına uzanan bir çizgide; her "
            "rivayette orijinal Arapça metin, tercüme ve klasik şerh notuyla sunan nokta atışı bir vize yol "
            "haritası."
        ),
        theme="forest",
        theme_color="#1D5B4C",
        icon_text="H",
        chapters=chapters,
        glossary=glossary,
        persons=PERSONS,
        test_title="Genel Değerlendirme Testi",
        test_subtitle="Kitâbü'l-İlm 1–22 ve bu kısmın usûl dipnotları üzerine kapsamlı çoktan seçmeli test",
        test_instructions="Aşağıdaki sorularda beş seçenekten yalnızca birini işaretleyiniz. Süre: 30 dakika.",
        test_questions=test_questions,
        answer_key_intro="Her sorunun doğru cevabı, dayandığı rivayet ve şerh/dipnot gerekçesiyle birlikte aşağıda verilmiştir.",
        answer_key_items=answer_key_items,
        overview_lead=(
            "Bu ders notu, <b>Metûnü'l-Hadîs</b>'in vize kapsamını — <b>Kitâbü'l-İlm 1–22</b>, on iki bâb, "
            "toplam <b>22 rivayet</b> — altı bölümde işler. Her rivayet önce <b>orijinal Arapça metniyle</b>, "
            "ardından <b>Türkçe tercümesiyle</b> ve altında <b>kaynak künyesi + klasik şerh notuyla</b> "
            "verilir. Bu kısım aynı zamanda kitabın <b>usûl dipnotlarının en yoğun olduğu</b> bölgedir; "
            "muallak, mevkūf, tahammül-edâ ve mutâbaat gibi terimler rivayetlerin içine yerleştirilmiştir."
        ),
        overview_cards=[
            {"title": "İlmin Fazileti", "text": "Öğrenmenin değeri, verâsetü'l-enbiyâ, rabbânî tarifi ve muallak–mevkūf ayrımı."},
            {"title": "Tebliğ ve Öğretim Âdâbı", "text": "Vedâ hutbesindeki tebliğ mîsâkı, tehavvül, se'âme ve “kolaylaştırın” emri."},
            {"title": "Fıkh ve Gıbta", "text": "“İnnemâ ene kāsim”, tefakkuh kable't-tesevvüd ve hased ile gıbtanın farkı."},
            {"title": "Öğrenmek ve Öğretmek", "text": "Yağmur meselinin üç toprağı, “hayruküm” hadisi ve öğretimde öfke bâbı."},
            {"title": "Tekrar ve Muhatap", "text": "Sözü üç kez tekrarlamak, kadınlara ayrı öğretim günü ve hırs ale'l-hadîs."},
            {"title": "İlmin Yazılması", "text": "Ebû Şâh izni, mutâbaat kaydı, Kırtâs hâdisesi ve anlayışı gözetme ilkesi."},
        ],
        overview_flow=[
            ("Arapça Metin", "Onarılmış, harekeli lafız"),
            ("Tercüme", "Akademik Türkçe karşılık"),
            ("Kaynak", "Buhârî/Müslim künyesi"),
            ("Şerh", "İbn Battâl · Aynî · Lisân"),
            ("Sınav Notu", "Karşılaştırma ve tuzak"),
        ],
        overview_note=(
            "Sınavda en çok karıştırılan üç nokta: <b>(1)</b> <u>muallak</u> ile <u>mevkūf</u> aynı şey "
            "değildir — biri <b>senedin durumu</b>, diğeri <b>sözün kime ait olduğu</b> ile ilgilidir ve bir "
            "rivayet ikisi birden olabilir (İlim 2, 3, 10); <b>(2)</b> <u>mutâbaat</u> <b>sened</b> "
            "benzerliği, <u>şâhid</u> ise <b>metin</b> benzerliğidir; <b>(3)</b> lukata rivayeti fıkıh "
            "bâbında değil <b>“öğretimde öfke”</b> bâbındadır — Buhârî'nin bâb başlığı, hadisin hangi "
            "yönüyle delil getirildiğini söyler."
        ),
    )
