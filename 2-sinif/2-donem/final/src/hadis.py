# -*- coding: utf-8 -*-
"""HADİS — Görsel Ders Notu Kitabı, içerik tanımı.

Kaynak: 'kaynaklar/ders_kaynaklari/HADİS/Hadis Metinleri.pdf' (Metûnü'l-Hadîs,
51 sayfa, 3 kitâb / 114 rivayet). Bu ders notu SORUMLU OLUNAN KAPSAMI işler:
    Kitâbü'l-İlm  23–29  (s. 12–15,  7 rivayet)
    Kitâbü'l-Îmân  1–23  (s. 16–24, 23 rivayet)
Toplam 30 rivayet, 7 bölüm.

TEKNİK NOT (Arapça metnin çıkarılması):
  * pdfplumber ve PyMuPDF bu PDF'te ligatürleri BOZUYOR ("الله"→"هللا",
    "الحديث"→"احلديث", "في"→"يف" gibi: ligatür glifleri TERS sırada veriliyor).
  * Poppler'ın `pdftotext -enc UTF-8` çıktısı ise ligatürleri DOĞRU çözüyor;
    Arapça metinlerin tamamı bu yolla alınmıştır.
  * Kaynak fontun kendi eksiklikleri elle tamamlandı: "الل"→"الله",
    "ي"→"يا", "النب"→"النبي", "ث"→"ثم", "ل"→"لي", "الزن"→"الزنا",
    "نئم"→"نائم", "وأدنها"→"وأدناها", "أخبرن"→"أخبرنا".
  * Senedler kısaltıldı; her rivayette SON RÂVİ + METİN esas alındı.
  * Rivayetler `Ayah` kartıyla (Arapça + tercüme + kaynak/şerh notu) render
    edilir — DejaVu Sans'ın Chromium'daki native shaping'i (HarfBuzz) ile
    harfler doğru bitişir, harekeler doğru yerleşir.
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

MUAZ = Person(
    id="muaz", name="Muâz b. Cebel", years="605–638 (h. 17)",
    tagline="Yemen'e Gönderilen Elçi, Zekât Memuru ve Kadı",
    bio=["Hicretten 18 yıl önce Medine'de doğdu, 18 yaşındayken müslüman oldu ve <b>II. Akabe biatına</b> "
         "katılanlar arasında yer aldı; hicretten sonra Hz. Peygamber onunla Abdullah b. Mes'ûd arasında "
         "kardeşlik bağı kurdu. Hicretin 9. yılında <b>Yemen'e</b> elçi, zekât memuru ve kadı olarak gönderildi; "
         "nasıl hüküm vereceği sorulduğunda <b>Kitap → Sünnet → kendi içtihadı</b> sıralamasını söyleyince "
         "Hz. Peygamber memnuniyetini dile getirdi. H. 17'de Ürdün'deki <b>vebâ salgınında</b> iki oğlu ve iki "
         "hanımıyla birlikte vefat etti."],
    key_work="Yemen kadılığı — Kitap/Sünnet/re'y sıralaması", initials="MC",
)
EBU_HUREYRE = Person(
    id="ebu_hureyre", name="Ebû Hüreyre", years="?–678 (h. 58)",
    tagline="En Çok Hadis Rivayet Eden Sahâbî — 5374 Hadis",
    bio=["Yemen'de yaşayan Ezd kabilesinin <b>Devs</b> koluna mensuptur; hicretin 7. yılında müslüman olmuş ve "
         "kendisini tamamen ilme vermiştir. <b>Suffe ashabındandır</b> ve sahâbîler arasında Hz. Peygamber'den "
         "<b>en çok hadis rivayet eden</b> kişidir (5374 hadis). Çok rivayetle itham edildiğinde Bakara 159 ve "
         "174. ayetleri okuyarak cevap vermiş, 'Ensardan kardeşlerimizi bağ-bahçe işleri meşgul ediyordu; Ebû "
         "Hüreyre ise karın tokluğuna Rasûlullah'ın ardından koşuyordu' demiştir. Kendisinden nakledilen "
         "<b>Sahîfe-i Sahîha</b>'nın bir bölümü, talebesi Hemmâm b. Münebbih kanalıyla <b>Sahîfetü Hemmâm</b> "
         "adıyla günümüze ulaşmıştır (138 hadis)."],
    key_work="Sahîfe-i Sahîha (→ Sahîfetü Hemmâm)", initials="EH",
)
UMMU_SULEYM = Person(
    id="ummu_suleym", name="Ümmü Süleym bint Milhân", years="?–? (Rumeysâ)",
    tagline="Kadınların Fıkhî Sorularını Sormaktan Çekinmeyen Sahâbiye",
    bio=["Ümmü Harâm el-Ensâriyye'nin kız kardeşi, <b>Ebû Talha el-Ensârî'nin hanımı ve Enes b. Mâlik'in "
         "annesidir</b>; kendisine Rumeysâ da denir. İslâm'dan önce Mâlik b. Nadr ile evliydi; müslüman olunca "
         "kocasına İslâm'ı tebliğ etti, o kabul etmeyip Şam'a gitti ve orada öldü. Hz. Peygamber Medine'ye hicret "
         "edince hizmetinde bulunması için oğlu Enes'i ona gönderdi. Hadis öğrenmeye çok istekliydi; "
         "<b>kadınların özel hallerine dair soruları çekinmeden sorarak</b> bu konuların öğrenilmesinde pay "
         "sahibi oldu. <b>14 hadis</b> rivayet ettiği belirtilir."],
    key_work="14 rivayet — ilimde hayâ bâbının merkez şahsiyeti", initials="ÜS",
)
UBADE = Person(
    id="ubade", name="Ubâde b. es-Sâmit", years="?–? (Bedir ehli)",
    tagline="Akabe Gecesi Nakiblerinden — Biat Hadisinin Râvisi",
    bio=["<b>Bedir Savaşı'na katılmış</b> ve <b>Akabe gecesi seçilen nakiblerden</b> biri olmuş Ensar "
         "büyüklerindendir. Rivayet ettiği <b>biat hadisi</b>, İslâm'ın yasakladığı temel suçların (şirk, "
         "hırsızlık, zinâ, çocuk katli, iftira, ma'rûfta isyan) tek metinde sıralandığı ve <b>had cezalarının "
         "keffâret oluşu</b> ile <b>Allah'ın günahı örtmesi (setr)</b> ilkesinin dayandırıldığı ana metindir."],
    key_work="Biat hadisi (Buhârî, Îmân, 11)", initials="US",
)
EBU_ZERR = Person(
    id="ebu_zerr", name="Ebû Zerr el-Gıfârî", years="?–652 (h. 32)",
    tagline="Soruyu Israrla Tekrarlayan Sahâbî — Kebîre Meselesinin Râvisi",
    bio=["Gıfâr kabilesine mensup, ilk müslümanlardan ve <b>zühd hayatının</b> sahâbe içindeki en belirgin "
         "temsilcilerindendir. Kitâbü'l-İlm'de nakledilen <b>Samsâme</b> sözü (mevkûf rivayet örneği) ile "
         "Kitâbü'l-Îmân'daki <b>'zinâ etse de hırsızlık yapsa da'</b> hadisinin râvisidir. Bu ikinci rivayette "
         "soruyu üç kez tekrarlaması ve Hz. Peygamber'in 'Ebû Zerr'in burnu sürtülse bile!' cevabı, "
         "<b>büyük günah sahibinin âkıbeti</b> tartışmasının en çok atıf yapılan metnini oluşturur."],
    key_work="Kebîre hadisi (Buhârî, Libâs, 24)", initials="EZ",
)
ABDULLAH_B_AMR = Person(
    id="abdullah_amr", name="Abdullah b. Amr b. el-Âs", years="?–684 (h. 65)",
    tagline="Hadisleri YAZAN Sahâbî — es-Sahîfetü's-Sâdıka",
    bio=["Ebû Hüreyre'nin, 'Benden daha çok hadis rivayet eden yoktur; <b>ancak Abdullah b. Amr müstesna, çünkü "
         "o yazıyordu ben yazmıyordum</b>' diyerek istisna ettiği sahâbîdir. Bu ifade, <b>kitâbetü'l-ilm</b> "
         "(ilmin yazıyla tespiti) tartışmasının en güçlü delillerindendir. Bu ünitede <b>ilmin kabzedilmesi</b> "
         "(İlim 29), <b>münafığın dört alâmeti</b> (İman 8) ve <b>'İslâm'ın hangisi hayırlıdır?'</b> (İman 13) "
         "rivayetlerinin râvisidir."],
    key_work="es-Sahîfetü's-Sâdıka", initials="AA",
)

PERSONS = {p.id: p for p in [MUAZ, EBU_HUREYRE, UMMU_SULEYM, UBADE, EBU_ZERR, ABDULLAH_B_AMR]}


def get_pack() -> CoursePack:
    # =======================================================================
    # 1. BÖLÜM — İlmin Tebliği ve İlimde Hayâ (Kitâbü'l-İlm 23–27)
    # =======================================================================
    ch1 = Chapter(
        number=1,
        title="İlmin Tebliği ve İlimde Hayâ",
        subtitle="Kitâbü'l-İlm 23–27 · Muhatabın seviyesi, ilmi gizlemenin günahı ve hayânın iki yüzü",
        key_terms=[
            KeyTerm("Mevkūf", "Senedi sahâbîde duran, yani Hz. Peygamber'e değil bir sahâbîye nispet edilen söz veya fiil. Hz. Ali'nin 'Halka anlayacakları şeyi anlatın' sözü bunun örneğidir."),
            KeyTerm("Muallak (Ta'lîk)", "Senedin baş tarafı (bir ya da birkaç râvi) hazfedilerek 'وقال فلان' kalıbıyla nakledilen rivayet. Buhârî bâb başlarında sık kullanır."),
            KeyTerm("Te'essüm", "Günaha girme korkusu. Muâz, hadisi gizlemenin günahından korktuğu için onu ancak vefatı sırasında açıklamıştır."),
            KeyTerm("Hayâ", "Utanma duygusu. İlim talebine engel olduğunda <b>kötülenir</b>; saygı ve ta'zim (tevkīr-iclâl) kaynaklı olduğunda <b>övülür</b> — bu bölümün ana ayrımıdır."),
        ],
    )
    ch1.pages.append(
        ChapterPage()
        .add_terms(ch1.key_terms)
        .add_ayat("Hadis Metinleri — Bâb: Anlayışı Kıt Olan Daha Kötüsüne Düşmesin Diye", [
            Ayah(
                "İlim 23 — Hz. Ali'nin Sözü (MEVKŪF)",
                "وَقَالَ عَلِيٌّ: حَدِّثُوا النَّاسَ بِمَا يَعْرِفُونَ، أَتُحِبُّونَ أَنْ يُكَذَّبَ اللهُ وَرَسُولُهُ؟",
                "Ali (r.a.) dedi ki: “İnsanlara bildikleri (anlayabilecekleri) şeyleri anlatın. Allah'ın ve Resûlü'nün yalanlanmasını ister misiniz?”",
                "<b>Buhârî, İlm, 49.</b> Rivayet Hz. Ali'ye nispet edildiği için <b>mevkūf</b>; senedi hazfedilip “وقال علي” kalıbıyla verildiği için <b>muallak</b>tır.",
            ),
        ])
        .add_block(BulletBlock(1, "Muhatabın Seviyesini Gözetme İlkesi", [
            "Anlayamayacağı bir bilgiyle karşılaşan kişi onu <b>reddedebilir</b>; bu da hadisin ve dolayısıyla "
            "Hz. Peygamber'in yalanlanması sonucunu doğurur. Bu yüzden ilim, muhatabın <b>kavrayış düzeyine</b> "
            "göre aktarılır.",
            "Aynı ilke bir önceki bâbda Hz. Âişe–Kâbe rivayetiyle örneklenmiştir: Hz. Peygamber, halkın "
            "<b>küfürden yeni çıkmış olması</b> sebebiyle Kâbe'yi yıkıp yeniden inşa etme fikrinden vazgeçmiştir. "
            "el-Mühelleb'in şerhi: <b>fitneye sebep olacaksa bir emr-i bi'l-ma'rûf terk edilebilir.</b>",
        ]))
    )
    ch1.pages.append(
        ChapterPage()
        .add_ayat("Hadis Metinleri (devam)", [
            Ayah(
                "İlim 24 — “Bunu duyarlarsa güvenip amelden kalırlar”",
                "عَنْ أَنَسِ بْنِ مَالِكٍ أَنَّ النَّبِيَّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ وَمُعَاذٌ رَدِيفُهُ عَلَى الرَّحْلِ قَالَ: يَا مُعَاذَ بْنَ جَبَلٍ. قَالَ: لَبَّيْكَ يَا رَسُولَ اللهِ وَسَعْدَيْكَ — ثَلَاثًا — قَالَ: مَا مِنْ أَحَدٍ يَشْهَدُ أَنْ لَا إِلَهَ إِلَّا اللهُ وَأَنَّ مُحَمَّدًا رَسُولُ اللهِ صِدْقًا مِنْ قَلْبِهِ إِلَّا حَرَّمَهُ اللهُ عَلَى النَّارِ. قَالَ: يَا رَسُولَ اللهِ أَفَلَا أُخْبِرُ بِهِ النَّاسَ فَيَسْتَبْشِرُوا؟ قَالَ: إِذًا يَتَّكِلُوا. وَأَخْبَرَ بِهَا مُعَاذٌ عِنْدَ مَوْتِهِ تَأَثُّمًا.",
                "Enes b. Mâlik'ten: Nebî (s.a.v.) — Muâz da terkisinde iken — “Ey Muâz b. Cebel!” dedi. Muâz: “Buyur ey Allah'ın Resûlü, emrine âmâdeyim” dedi (bu üç defa tekrarlandı). Sonra buyurdu: “Kim kalbinden gelen bir doğrulukla ‘Allah'tan başka ilah yoktur ve Muhammed Allah'ın Resûlüdür’ diye şehâdet ederse, Allah onu ateşe haram kılar.” Muâz: “Ey Allah'ın Resûlü, bunu insanlara haber vereyim de sevinsinler mi?” dedi. “O zaman buna güvenip (amelden) geri kalırlar” buyurdu. Muâz bu hadisi, günaha girme korkusuyla ölümü sırasında haber verdi.",
                "<b>Buhârî, İlm, 49; Müslim, Îmân, 53.</b> İbn Hacer: <i>“izen yettekilû”</i> = buna dayanıp amelden vazgeçerler. İbnü'l-Esîr: <i>“te'essümen”</i> = bu ilmi gizlemenin <b>günahından</b> korkarak.",
            ),
        ])
        .add_callout(Callout(
            "insight", "İki İlkenin Dengesi",
            "Bu hadis, birbirini sınırlayan iki ilkeyi aynı anda kurar: <b>(1)</b> Sonucu iyi olmayacaksa bir "
            "bilginin açıklanması <u>geciktirilebilir</u>; <b>(2)</b> ama ilmi <u>tümüyle gizlemek günahtır</u> "
            "— Muâz tam da bu yüzden vefatından önce hadisi açıklamıştır. Sınavda “Muâz hadisi neyi gösterir?” "
            "sorusunun cevabı bu ikisinin <b>dengesidir</b>, tek başına biri değil."
        ))
        .add_person(MUAZ)
    )
    ch1.pages.append(
        ChapterPage()
        .add_ayat("Bâb: el-Hayâ fi'l-İlm (İlimde Hayâ)", [
            Ayah(
                "İlim 25 — Ümmü Süleym: “Allah hakkı söylemekten utanmaz”",
                "عَنْ أُمِّ سَلَمَةَ قَالَتْ: جَاءَتْ أُمُّ سُلَيْمٍ إِلَى رَسُولِ اللهِ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ فَقَالَتْ: يَا رَسُولَ اللهِ، إِنَّ اللهَ لَا يَسْتَحْيِي مِنَ الْحَقِّ، فَهَلْ عَلَى الْمَرْأَةِ مِنْ غُسْلٍ إِذَا احْتَلَمَتْ؟ قَالَ النَّبِيُّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ: إِذَا رَأَتِ الْمَاءَ. فَغَطَّتْ أُمُّ سَلَمَةَ — تَعْنِي وَجْهَهَا — وَقَالَتْ: يَا رَسُولَ اللهِ وَتَحْتَلِمُ الْمَرْأَةُ؟ قَالَ: نَعَمْ، تَرِبَتْ يَمِينُكِ، فَبِمَ يُشْبِهُهَا وَلَدُهَا؟",
                "Ümmü Seleme anlatıyor: Ümmü Süleym, Resûlullah'a (s.a.v.) gelip: “Ey Allah'ın Resûlü, Allah hakkı (söylemekten) utanmaz; kadın ihtilâm olursa ona gusül gerekir mi?” dedi. Nebî (s.a.v.): “(Suyu/ıslaklığı) gördüğü zaman (gerekir)” buyurdu. Ümmü Seleme yüzünü örttü ve: “Ey Allah'ın Resûlü, kadın da ihtilâm olur mu?” dedi. “Evet, elin toprak olsun! Yoksa çocuk anasına neden benzesin?” buyurdu.",
                "<b>Buhârî, İlm, 50; Mâlik, Tahâret, 116; Müslim, Hayz, 32.</b> “إن الله لا يستحيي من الحق” ifadesi <b>Ahzâb 33/53</b>'e dayanır.",
            ),
            Ayah(
                "İlim 26 — Hurma Ağacı Meseli ve İbn Ömer'in Susması",
                "عَنْ عَبْدِ اللهِ بْنِ عُمَرَ أَنَّ رَسُولَ اللهِ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ قَالَ: إِنَّ مِنَ الشَّجَرِ شَجَرَةً لَا يَسْقُطُ وَرَقُهَا وَهِيَ مَثَلُ الْمُسْلِمِ، حَدِّثُونِي مَا هِيَ؟ فَوَقَعَ النَّاسُ فِي شَجَرِ الْبَادِيَةِ، وَوَقَعَ فِي نَفْسِي أَنَّهَا النَّخْلَةُ. قَالَ عَبْدُ اللهِ: فَاسْتَحْيَيْتُ. فَقَالُوا: يَا رَسُولَ اللهِ أَخْبِرْنَا بِهَا. فَقَالَ: هِيَ النَّخْلَةُ. قَالَ عَبْدُ اللهِ: فَحَدَّثْتُ أَبِي بِمَا وَقَعَ فِي نَفْسِي فَقَالَ: لَأَنْ تَكُونَ قُلْتَهَا أَحَبُّ إِلَيَّ مِنْ أَنْ يَكُونَ لِي كَذَا وَكَذَا.",
                "Abdullah b. Ömer'den: Resûlullah (s.a.v.): “Ağaçlar içinde bir ağaç vardır ki yaprağı dökülmez ve o müslümanın misalidir. Bana onun ne olduğunu söyleyin” buyurdu. İnsanlar çöl ağaçlarını saymaya koyuldular; benim aklıma ise hurma ağacı geldi. Abdullah der ki: “Utandım (söyleyemedim).” Sonra “Ey Allah'ın Resûlü, bize sen söyle” dediler; “O hurma ağacıdır” buyurdu. Abdullah: “Aklımdan geçeni babama anlattım. Babam: ‘Onu söylemiş olman benim için şu şu şeylere sahip olmamdan daha sevimli olurdu’ dedi.”",
                "<b>Buhârî, İlm, 50; Müslim, Sıfâtü'l-Münâfikîn, 63; Tirmizî, Emsâl, 4.</b>",
            ),
        ])
        .add_callout(Callout(
            "focus", "Allah'tan Hayâ ≠ İnsanlardan Hayâ",
            "İbn Battâl: “Allah'tan hayâ etmek” ile “yaratılmışlardan hayâ etmek” aynı şey değildir. Allah "
            "hakkında hayâ, <b>terk etmek</b> anlamındadır — nitekim müfessirler <b>Bakara 2/26</b>'daki "
            "“إن الله لا يستحيي أن يضرب مثلا ما بعوضة” ayetini böyle açıklamıştır."
        ))
    )
    ch1.pages.append(
        ChapterPage()
        .add_ayat("Bâb: el-Hayâ fi'l-İlm (devam)", [
            Ayah(
                "İlim 27 — Hz. Ali ve Mezî Meselesi",
                "عَنْ عَلِيٍّ قَالَ: كُنْتُ رَجُلًا مَذَّاءً، فَأَمَرْتُ الْمِقْدَادَ بْنَ الْأَسْوَدِ أَنْ يَسْأَلَ النَّبِيَّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ، فَسَأَلَهُ فَقَالَ: فِيهِ الْوُضُوءُ.",
                "Ali (r.a.) dedi ki: “Ben çok mezî gelen bir adamdım. Mikdâd b. Esved'e, Nebî'ye (s.a.v.) bunu sormasını söyledim. O da sordu; Nebî: ‘Onda abdest (gerekir)’ buyurdu.”",
                "<b>Buhârî, İlm, 51.</b> Hz. Ali, Hz. Peygamber'in damadı olduğu için hayâ edip <b>aracı koymuştur</b>. Hüküm: <b>mezî gusül gerektirmez, abdesti bozar</b> (menî ise gusül gerektirir — krş. İlim 25).",
            ),
        ])
        .add_table(ComparisonTable(
            "Bâbın Ana Ayrımı — Hayânın İki Yüzü (İbn Battâl'ın Şerhi)",
            ["Kötülenen Hayâ", "Övülen Hayâ"],
            [
                ["<b>İlim talebine engel olan</b> hayâ", "<b>Tevkīr ve iclâl</b> (saygı ve ta'zim) kaynaklı hayâ"],
                ["İbn Ömer'in doğru cevabı bildiği halde <b>susması</b> (İlim 26)", "Ümmü Seleme'nin soru sorulurken <b>yüzünü örtmesi</b> (İlim 25)"],
                ["Sonuç: <b>bilgi kaybı</b> — babası bile buna üzülmüştür", "Sonuç: <b>edep korunur</b>, bilgi yine de öğrenilir"],
                ["Çare: Ümmü Süleym gibi <b>açıkça sormak</b>", "Çare: Hz. Ali gibi <b>aracı koyup yine de öğrenmek</b> (İlim 27)"],
            ],
        ))
        .add_person(UMMU_SULEYM)
        .add_summary(
            "Bu bölüm ilmin aktarım âdâbını kurar: muhatabın seviyesi gözetilir (İlim 23), bilgi "
            "geciktirilebilir ama gizlenemez (İlim 24), ilim talebine engel olan hayâ kötülenir (İlim 26) "
            "buna karşılık ta'zim kaynaklı hayâ övülür (İlim 25) ve hayâ, öğrenmeyi engellemeyecek "
            "bir yol bulunarak aşılır (İlim 27)."
        )
    )

    # =======================================================================
    # 2. BÖLÜM — Ref'u'l-İlm (Kitâbü'l-İlm 28–29)
    # =======================================================================
    ch2 = Chapter(
        number=2,
        title="Ref'u'l-İlm: İlmin Kaldırılması",
        subtitle="Kitâbü'l-İlm 28–29 · Cehaletin yayılması, câhil reisler ve rivayet usûlü terimleri",
        key_terms=[
            KeyTerm("Ref'u'l-ilm", "İlmin kaldırılması. Aynî'ye göre bu, ilmin <b>kalplerden silinmesi değil</b>, ehlinin (âlimlerin) vefatıyla ortadan kalkmasıdır."),
            KeyTerm("Kabz", "Alma, tutma. Hadiste ilmin “kabzedilmesi”, âlimlerin <b>vefat ettirilmesi</b> yoluyla gerçekleşir."),
            KeyTerm("Nahvehu", "“Onun benzeri”. Senedin sonunda metin yerine kullanılır; metnin bir öncekinin <b>lafzen aynısı değil benzeri</b> olduğunu, aralarında küçük farklar bulunduğunu gösterir."),
            KeyTerm("Mislehu", "“Onun aynısı”. Senedin sonunda metin yerine kullanılır; metnin bir öncekinin <b>lafzen aynı</b> olduğunu gösterir."),
        ],
    )
    ch2.pages.append(
        ChapterPage()
        .add_terms(ch2.key_terms)
        .add_ayat("Bâb: Ref'u'l-İlm ve Zuhûru'l-Cehl", [
            Ayah(
                "İlim 28 — Kıyamet Alâmetlerinden Dördü",
                "عَنْ أَنَسٍ قَالَ: قَالَ رَسُولُ اللهِ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ: إِنَّ مِنْ أَشْرَاطِ السَّاعَةِ أَنْ يُرْفَعَ الْعِلْمُ، وَيَثْبُتَ الْجَهْلُ، وَيُشْرَبَ الْخَمْرُ، وَيَظْهَرَ الزِّنَا.",
                "Enes'ten: Resûlullah (s.a.v.) buyurdu: “Kıyamet alâmetlerindendir: ilmin kaldırılması, cehaletin yerleşmesi, içkinin içilmesi ve zinanın açıkça yayılması.”",
                "<b>Buhârî, İlm, 21; Müslim, İlm, 8.</b> Dört alâmet: <b>ref'u'l-ilm · sübûtü'l-cehl · şürbü'l-hamr · zuhûru'z-zinâ.</b>",
            ),
            Ayah(
                "İlim 29 — EZBER (احفظ): İlim Âlimlerin Alınmasıyla Kabzedilir",
                "عَنْ عَبْدِ اللهِ بْنِ عَمْرِو بْنِ الْعَاصِ قَالَ: سَمِعْتُ رَسُولَ اللهِ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ يَقُولُ: إِنَّ اللهَ لَا يَقْبِضُ الْعِلْمَ انْتِزَاعًا يَنْتَزِعُهُ مِنَ الْعِبَادِ، وَلَكِنْ يَقْبِضُ الْعِلْمَ بِقَبْضِ الْعُلَمَاءِ، حَتَّى إِذَا لَمْ يُبْقِ عَالِمًا اتَّخَذَ النَّاسُ رُؤُوسًا جُهَّالًا، فَسُئِلُوا فَأَفْتَوْا بِغَيْرِ عِلْمٍ، فَضَلُّوا وَأَضَلُّوا.",
                "Abdullah b. Amr b. el-Âs'tan: Resûlullah'ı (s.a.v.) şöyle buyururken işittim: “Allah ilmi, kullardan çekip almak suretiyle kabzetmez; fakat ilmi âlimleri almak (vefat ettirmek) suretiyle kabzeder. Nihayet hiçbir âlim bırakmayınca insanlar câhil kimseleri baş edinirler; onlara sorulur, onlar da ilimsiz fetva verirler; böylece hem kendileri sapar hem de başkalarını saptırırlar.”",
                "<b>Buhârî, İlm, 34; Müslim, İlm, 13; İbn Mâce, Mukaddime, 8.</b> Kaynak metinde <b>(احفظ)</b> = “ezberle” işaretlidir.",
            ),
        ])
    )
    ch2.pages.append(
        ChapterPage()
        .add_block(BulletBlock(1, "Aynî'nin Şerhi — “Ref'” Neyin Kaldırılmasıdır?", [
            "Hadis, <b>ref'u'l-ilm</b>'in ne anlama geldiğini bizzat kendisi açıklar: bu, ilmin insanların "
            "<b>göğüslerinden/hafızalarından silinmesi değildir</b>; ilim <b>ehlinin ölümüyle</b> ortadan kalkar.",
            "Süreç zincirlemedir: <b>âlimlerin vefatı → câhillerin reis edinilmesi → ilimsiz fetva → hem kendi "
            "sapması hem başkalarını saptırması.</b> Aynî'nin ifadesiyle: “Allah'ın dininde <b>kendi "
            "re'yleriyle</b> hüküm verir ve cehaletle fetva verirler.”",
            "Bu yüzden İlim 28 ile İlim 29 <b>aynı olguyu</b> iki ayrı açıdan anlatır: biri alâmeti "
            "(<b>ne olacak</b>), diğeri mekanizmayı (<b>nasıl olacak</b>) verir.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("Âlimlerin Vefatı", "İlim “kabz” edilir"),
            FlowStep("Câhil Reisler", "İnsanlar rüûsen cühhâlâ edinir"),
            FlowStep("İlimsiz Fetva", "Bilmeden hüküm verilir"),
            FlowStep("Dalâlet", "Hem sapar hem saptırır"),
        ], caption="İlim 29'un tarif ettiği çöküş zinciri"))
        .add_table(ComparisonTable(
            "Bu Bölümde Geçen Rivayet Usûlü Terimleri",
            ["Terim", "Anlamı", "Nerede geçer"],
            [
                ["<b>Nahvehu</b> (نحوه)", "Metin, bir öncekinin <b>benzeri</b>; lafızda az da olsa fark var", "İlim 29'un sonunda"],
                ["<b>Mislehu</b> (مثله)", "Metin, bir öncekinin <b>lafzen aynısı</b>", "Karşıt terim olarak"],
                ["<b>Mevkūf</b>", "Söz <b>sahâbîye</b> ait", "İlim 23 (Hz. Ali)"],
                ["<b>Muallak</b>", "Senedin başı hazfedilmiş", "İlim 23 (“وقال علي”)"],
            ],
        ))
        .add_callout(Callout(
            "caution", "Nüsha Bilgisi — Firebrî ve Yûnînî",
            "Buhârî eserini yazdıktan sonra öğrencileri asıl nüshadan kendi nüshalarını istinsah etti. En meşhur "
            "nüshalardan biri <b>Nesefî</b>'ye, bir diğeri <b>Firebrî</b>'ye aittir. Firebrî'ye ait önemli "
            "nüshaların karşılaştırılmasıyla oluşan <b>Yûnînî nüshası</b> Abdülhamit Han tarafından bastırılmıştır "
            "— <b>bugün elimizdeki matbu Buhârî budur.</b>"
        ))
        .add_summary(
            "İlmin kaybı ani bir silinme değil, kuşak kaybıdır: âlim öldükçe ilim çekilir, boşluğu "
            "câhil otoriteler doldurur ve ilimsiz fetva toplumu saptırır. Bu yüzden bölüm, Kitâbü'l-İlm'i "
            "bir uyarı ile kapatır ve ilim öğrenmeyi/öğretmeyi bir süreklilik sorumluluğu hâline getirir."
        )
    )

    # =======================================================================
    # 3. BÖLÜM — İman, İslâm, İhsan (Kitâbü'l-Îmân 1–2)
    # =======================================================================
    ch3 = Chapter(
        number=3,
        title="İman, İslâm ve İhsan",
        subtitle="Kitâbü'l-Îmân 1–2 · Cibrîl hadisi, dinin üç mertebesi ve İslâm'ın beş esası",
        key_terms=[
            KeyTerm("Îmân", "Kalben tasdik. Cibrîl hadisinde altı esasla tarif edilir: Allah, melekler, Kitap, <b>likā'</b> (O'na kavuşma), resuller ve <b>ba's</b> (öldükten sonra diriliş)."),
            KeyTerm("İslâm", "Amelî boyut. Cibrîl hadisinde dört rükünle sayılır: şirksiz kulluk, farz namaz, farz zekât ve ramazan orucu."),
            KeyTerm("İhsan", "“Allah'a, sanki O'nu görüyormuşsun gibi kulluk etmen; sen O'nu görmesen de O seni görmektedir.” Kulluğun <b>murâkabe</b> mertebesi."),
            KeyTerm("Eşrâtu's-sâa", "Kıyamet alâmetleri. Cibrîl hadisinde üçü sayılır: cariyenin efendisini doğurması, çıplak-yalınayakların baş olması, çobanların bina yarışı."),
        ],
    )
    ch3.pages.append(
        ChapterPage()
        .add_terms(ch3.key_terms)
        .add_ayat("Bâb: Beyânü'l-Îmân ve'l-İslâm ve'l-İhsân", [
            Ayah(
                "İman 1 — CİBRÎL HADİSİ (Dinin Tarifi)",
                "عَنْ أَبِي هُرَيْرَةَ قَالَ: كَانَ رَسُولُ اللهِ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ يَوْمًا بَارِزًا لِلنَّاسِ، فَأَتَاهُ رَجُلٌ فَقَالَ: يَا رَسُولَ اللهِ! مَا الْإِيمَانُ؟ قَالَ: أَنْ تُؤْمِنَ بِاللهِ وَمَلَائِكَتِهِ وَكِتَابِهِ وَلِقَائِهِ وَرُسُلِهِ وَتُؤْمِنَ بِالْبَعْثِ الْآخِرِ. قَالَ: يَا رَسُولَ اللهِ! مَا الْإِسْلَامُ؟ قَالَ: الْإِسْلَامُ أَنْ تَعْبُدَ اللهَ وَلَا تُشْرِكَ بِهِ شَيْئًا، وَتُقِيمَ الصَّلَاةَ الْمَكْتُوبَةَ، وَتُؤَدِّيَ الزَّكَاةَ الْمَفْرُوضَةَ، وَتَصُومَ رَمَضَانَ. قَالَ: يَا رَسُولَ اللهِ! مَا الْإِحْسَانُ؟ قَالَ: أَنْ تَعْبُدَ اللهَ كَأَنَّكَ تَرَاهُ، فَإِنَّكَ إِنْ لَا تَرَاهُ فَإِنَّهُ يَرَاكَ.",
                "Ebû Hüreyre'den: Resûlullah (s.a.v.) bir gün insanların karşısına çıkmıştı. Bir adam gelip: “Ey Allah'ın Resûlü, iman nedir?” dedi. Buyurdu: “Allah'a, meleklerine, Kitabına, O'na kavuşmaya, resullerine iman etmen ve öldükten sonra dirilmeye inanmandır.” — “Ey Allah'ın Resûlü, İslâm nedir?” dedi. Buyurdu: “İslâm, Allah'a kulluk edip O'na hiçbir şeyi ortak koşmaman, farz namazı kılman, farz zekâtı vermen ve ramazan orucunu tutmandır.” — “Ey Allah'ın Resûlü, ihsan nedir?” dedi. Buyurdu: “Allah'a, sanki O'nu görüyormuşsun gibi kulluk etmendir; her ne kadar sen O'nu görmüyorsan da O seni görmektedir.”",
                "<b>Müslim, Îmân, 5; İbn Mâce, Mukaddime, 9.</b> Râvi: Ebû Hüreyre. Hadisin senedinde <b>Ebû Bekr b. Ebî Şeybe</b> (el-Musannef sahibi) yer alır.",
            ),
        ])
    )
    ch3.pages.append(
        ChapterPage()
        .add_ayat(None, [
            Ayah(
                "İman 1 (devamı) — Kıyamet Sorusu ve “Bu Cibrîl'di”",
                "قَالَ: يَا رَسُولَ اللهِ! مَتَى السَّاعَةُ؟ قَالَ: مَا الْمَسْؤُولُ عَنْهَا بِأَعْلَمَ مِنَ السَّائِلِ، وَلَكِنْ سَأُحَدِّثُكَ عَنْ أَشْرَاطِهَا: إِذَا وَلَدَتِ الْأَمَةُ رَبَّهَا فَذَاكَ مِنْ أَشْرَاطِهَا، وَإِذَا كَانَتِ الْعُرَاةُ الْحُفَاةُ رُؤُوسَ النَّاسِ فَذَاكَ مِنْ أَشْرَاطِهَا، وَإِذَا تَطَاوَلَ رِعَاءُ الْبَهْمِ فِي الْبُنْيَانِ فَذَاكَ مِنْ أَشْرَاطِهَا. فِي خَمْسٍ لَا يَعْلَمُهُنَّ إِلَّا اللهُ. ثُمَّ أَدْبَرَ الرَّجُلُ فَقَالَ: رُدُّوا عَلَيَّ الرَّجُلَ. فَأَخَذُوا لِيَرُدُّوهُ فَلَمْ يَرَوْا شَيْئًا. فَقَالَ: هَذَا جِبْرِيلُ جَاءَ لِيُعَلِّمَ النَّاسَ دِينَهُمْ.",
                "“Ey Allah'ın Resûlü, kıyamet ne zaman?” dedi. Buyurdu: “Bu konuda kendisine sorulan, sorandan daha bilgili değildir. Ama sana onun alâmetlerinden haber vereyim: cariyenin efendisini doğurması, çıplak ve yalınayak kimselerin insanların başı olması, koyun çobanlarının bina yapmakta birbiriyle yarışması — bunlar onun alâmetlerindendir. (Kıyamet ilmi,) Allah'tan başka kimsenin bilmediği beş şey içindedir.” Sonra adam dönüp gitti; “Adamı bana geri getirin” buyurdu. Ardından gittiler ama bir şey göremediler. Bunun üzerine: “Bu Cibrîl'di; insanlara dinlerini öğretmeye geldi” buyurdu.",
                "Hz. Peygamber bu noktada <b>Lokmân 31/34</b> ayetini okumuştur (“beş şey” = mugayyebât-ı hamse).",
            ),
        ])
        .add_ayat("Bâb: Beyânü'l-Îmân (devam)", [
            Ayah(
                "İman 2 — “İslâm Beş Esas Üzerine Bina Edilmiştir”",
                "عَنِ ابْنِ عُمَرَ رَضِيَ اللهُ عَنْهُمَا قَالَ: قَالَ رَسُولُ اللهِ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ: بُنِيَ الْإِسْلَامُ عَلَى خَمْسٍ: شَهَادَةِ أَنْ لَا إِلَهَ إِلَّا اللهُ وَأَنَّ مُحَمَّدًا رَسُولُ اللهِ، وَإِقَامِ الصَّلَاةِ، وَإِيتَاءِ الزَّكَاةِ، وَالْحَجِّ، وَصَوْمِ رَمَضَانَ.",
                "İbn Ömer'den: Resûlullah (s.a.v.) buyurdu: “İslâm beş (esas) üzerine bina edilmiştir: Allah'tan başka ilah olmadığına ve Muhammed'in Allah'ın Resûlü olduğuna şehâdet etmek, namazı dosdoğru kılmak, zekâtı vermek, hac ve ramazan orucu.”",
                "<b>Buhârî, Îmân, 1; Müslim, Îmân, 21; Tirmizî, Îmân, 3; Nesâî, Îmân, 13.</b> Bu rivayette sıralama <b>hac → oruç</b> şeklindedir.",
            ),
        ])
        .add_table(ComparisonTable(
            "SINAVIN EN KRİTİK KARŞILAŞTIRMASI — İki Rivayetin Farkı",
            ["", "İman 1 (Cibrîl hadisi · Müslim)", "İman 2 (Büniye'l-İslâm · Buhârî)"],
            [
                ["<b>Konu</b>", "Dinin üç mertebesi: îmân–İslâm–ihsan", "Sadece <b>İslâm</b>'ın yapısı"],
                ["<b>Rükün sayısı</b>", "İslâm için <b>4</b>", "İslâm için <b>5</b>"],
                ["<b>Hac</b>", "<b>ZİKREDİLMEZ</b>", "<b>Zikredilir</b> (oruçtan önce)"],
                ["<b>İman esasları</b>", "Allah · melekler · Kitap · <b>likā'</b> · resuller · <b>ba's</b>", "Konu edilmez"],
                ["<b>Kader</b>", "Bu rivayette <b>geçmez</b> (yerine likā')", "Konu edilmez"],
                ["<b>Râvi</b>", "Ebû Hüreyre", "Abdullah b. Ömer"],
            ],
        ))
    )
    ch3.pages.append(
        ChapterPage()
        .add_callout(Callout(
            "focus", "Dikkat: “Kader” Nerede?",
            "Cibrîl hadisinin <b>bu rivayetinde</b> iman esasları arasında kader <u>geçmez</u>; onun yerine "
            "<b>likāullah</b> (Allah'a kavuşma) sayılır. Kadere iman, Kitâbü'l-Îmân'ın ilerideki ayrı bir "
            "bâbında (el-Îmân bi'l-kader) işlenir. Sınavda “Cibrîl hadisinde aşağıdakilerden hangisi "
            "sayılmamıştır?” sorusunun cevabı çoğunlukla <b>hac</b> ya da <b>kader</b>'dir."
        ))
        .add_person(EBU_HUREYRE)
        .add_summary(
            "Cibrîl hadisi dini üç katmanda tarif eder: îmân (kalbin tasdiki), İslâm (bedenin "
            "ameli) ve ihsan (niyetin kalitesi/murâkabe). İman 2 ise İslâm katmanının beş rüknünü "
            "verir. İki metnin farkı tesadüf değildir: biri dinin bütününü, diğeri yalnızca "
            "amelî yapısını anlatır."
        )
    )

    # =======================================================================
    # 4. BÖLÜM — İmanın Alâmeti, Tadı ve Şubeleri (Kitâbü'l-Îmân 3–7)
    # =======================================================================
    ch4 = Chapter(
        number=4,
        title="İmanın Alâmeti, Tadı ve Şubeleri",
        subtitle="Kitâbü'l-Îmân 3–7 · Nefyü'l-kemâl kaidesi, halâvetü'l-îmân ve amelde derece farkı",
        key_terms=[
            KeyTerm("Nefyü'l-kemâl", "“لا يؤمن أحدكم حتى…” kalıbında nefyedilen, imanın <b>aslı değil kemâlidir</b>. Nevevî: muhakkiklerin benimsediği sahih görüş budur."),
            KeyTerm("Halâvetü'l-îmân", "İmanın tadı. Üç haslette bulunur: Allah ve Resûlünü her şeyden çok sevmek, kişiyi yalnız Allah için sevmek, küfre dönmekten ateşe atılmak gibi nefret etmek."),
            KeyTerm("Şuabü'l-îmân", "İmanın şubeleri. “Bid'un ve sittûn” = altmış küsur şube; en üstü kelime-i tevhid, en altı yoldan eziyeti kaldırmaktır."),
            KeyTerm("Tahvîl hâ'sı (ح)", "Senedde bir hadisin <b>birden çok senedle</b> geldiğini, râvinin bir senedden diğerine geçtiğini gösteren işaret."),
        ],
    )
    ch4.pages.append(
        ChapterPage()
        .add_terms(ch4.key_terms)
        .add_ayat("Bâb: Alâmetü'l-Îmân (İmanın Alâmeti)", [
            Ayah(
                "İman 3 — Peygamber Sevgisinin Önceliği",
                "عَنْ أَنَسٍ قَالَ: قَالَ النَّبِيُّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ: لَا يُؤْمِنُ أَحَدُكُمْ حَتَّى أَكُونَ أَحَبَّ إِلَيْهِ مِنْ وَالِدِهِ وَوَلَدِهِ وَالنَّاسِ أَجْمَعِينَ.",
                "Enes'ten: Nebî (s.a.v.) buyurdu: “Ben kendisine babasından, evladından ve bütün insanlardan daha sevimli olmadıkça hiçbiriniz (gerçek anlamda) iman etmiş olmaz.”",
                "<b>Buhârî, Îmân, 8; Müslim, Îmân, 69; Nesâî, Îmân, 19.</b> Bu hadisin senedinde <b>tahvîl hâ'sı (ح)</b> bulunur.",
            ),
            Ayah(
                "İman 4 — Kardeşi İçin de İstemek",
                "عَنْ أَنَسٍ رَضِيَ اللهُ عَنْهُ عَنِ النَّبِيِّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ قَالَ: لَا يُؤْمِنُ أَحَدُكُمْ حَتَّى يُحِبَّ لِأَخِيهِ مَا يُحِبُّ لِنَفْسِهِ.",
                "Enes'ten: Nebî (s.a.v.) buyurdu: “Sizden biriniz, kendisi için istediğini kardeşi için de istemedikçe (gerçek anlamda) iman etmiş olmaz.”",
                "<b>Buhârî, Îmân, 7; Müslim, Îmân, 71; Tirmizî, Sıfâtü'l-Kıyâme, 59.</b> İman 3 ile <b>aynı kalıptadır</b>: “لا يؤمن أحدكم حتى…”.",
            ),
        ])
    )
    ch4.pages.append(
        ChapterPage()
        .add_callout(Callout(
            "insight", "Anahtar Kaide: Nefyedilen İmanın Aslı Değil, Kemâlidir",
            "Bu bölümdeki (ve 5. bölümdeki) “iman etmiş olmaz” ifadeleri, kişiyi <b>dinden çıkarmaz</b>. Nevevî'nin "
            "ifadesiyle: <b>“Muhakkiklerin söylediği sahih görüş, bunun ‘kâmil iman sahibi olarak yapmaz’ "
            "anlamına geldiğidir.”</b> Aynı üslup Arapçada “<i>lâ ayşe illâ ayşe'l-âhira</i>” (âhiret hayatından "
            "başka hayat yoktur) denmesine benzer."
        ))
        .add_ayat("Bâb: Halâvetü'l-Îmân ve Şuabü'l-Îmân", [
            Ayah(
                "İman 5 — İmanın Tadını Aldıran Üç Haslet",
                "عَنْ أَنَسٍ عَنِ النَّبِيِّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ قَالَ: ثَلَاثٌ مَنْ كُنَّ فِيهِ وَجَدَ حَلَاوَةَ الْإِيمَانِ: أَنْ يَكُونَ اللهُ وَرَسُولُهُ أَحَبَّ إِلَيْهِ مِمَّا سِوَاهُمَا، وَأَنْ يُحِبَّ الْمَرْءَ لَا يُحِبُّهُ إِلَّا لِلَّهِ، وَأَنْ يَكْرَهَ أَنْ يَعُودَ فِي الْكُفْرِ كَمَا يَكْرَهُ أَنْ يُقْذَفَ فِي النَّارِ.",
                "Enes'ten: Nebî (s.a.v.) buyurdu: “Üç haslet vardır ki kimde bulunursa imanın tadını alır: (1) Allah ve Resûlünün ona bunlardan başka her şeyden daha sevimli olması, (2) bir kimseyi yalnızca Allah için sevmesi, (3) ateşe atılmaktan hoşlanmadığı gibi küfre dönmekten de hoşlanmaması.”",
                "<b>Buhârî, Îmân, 9; Müslim, Îmân, 67; Nesâî, Îmân, 3.</b> Özet: <b>muhabbetullah · hubb fillâh · küfürden nefret.</b>",
            ),
            Ayah(
                "İman 6 — “İman Altmış Küsur Şubedir”",
                "عَنْ أَبِي هُرَيْرَةَ قَالَ: قَالَ رَسُولُ اللهِ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ: الْإِيمَانُ بِضْعٌ وَسِتُّونَ شُعْبَةً، فَأَفْضَلُهَا قَوْلُ لَا إِلَهَ إِلَّا اللهُ، وَأَدْنَاهَا إِمَاطَةُ الْأَذَى عَنِ الطَّرِيقِ، وَالْحَيَاءُ شُعْبَةٌ مِنَ الْإِيمَانِ.",
                "Ebû Hüreyre'den: Resûlullah (s.a.v.) buyurdu: “İman altmış küsur şubedir. En üstünü ‘Lâ ilâhe illallâh’ sözü, en aşağısı yoldan eziyet veren şeyi kaldırmaktır. Hayâ da imandan bir şubedir.”",
                "<b>Müslim, Îmân, 58; Ebû Dâvûd, Sünne, 15; Nesâî, Îmân, 16.</b> <b>“Bid'un”</b> = 3–9 arası sayı; yani “altmış küsur”.",
            ),
        ])
        .add_block(BulletBlock(1, "İmanın Şubeleri Ne Anlatır?", [
            "Hadis imanı <b>tek parçalı bir evet/hayır</b> olarak değil, <b>dereceli ve amelî</b> bir bütün "
            "olarak tarif eder: en üst uçta <b>kelime-i tevhid</b> (kalbin ve dilin işi), en alt uçta "
            "<b>yoldan eziyeti kaldırmak</b> (bedenin ve toplumun işi) vardır.",
            "<b>Hayânın</b> imandan bir şube sayılması, 1. bölümdeki hayâ tartışmasıyla doğrudan bağlantılıdır: "
            "hayâ, ilim talebine engel olmadığı sürece <b>imanî bir değerdir</b>.",
        ]))
    )
    ch4.pages.append(
        ChapterPage()
        .add_ayat("Bâb: Tefâdulü Ehli'l-Îmân fi'l-A'mâl", [
            Ayah(
                "İman 7 — Hardal Tanesi Kadar İman",
                "عَنْ أَبِي سَعِيدٍ الْخُدْرِيِّ رَضِيَ اللهُ عَنْهُ عَنِ النَّبِيِّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ قَالَ: يَدْخُلُ أَهْلُ الْجَنَّةِ الْجَنَّةَ وَأَهْلُ النَّارِ النَّارَ، ثُمَّ يَقُولُ اللهُ تَعَالَى: أَخْرِجُوا مَنْ كَانَ فِي قَلْبِهِ مِثْقَالُ حَبَّةٍ مِنْ خَرْدَلٍ مِنْ إِيمَانٍ. فَيَخْرُجُونَ مِنْهَا قَدِ اسْوَدُّوا، فَيُلْقَوْنَ فِي نَهَرِ الْحَيَا، فَيَنْبُتُونَ كَمَا تَنْبُتُ الْحِبَّةُ فِي جَانِبِ السَّيْلِ، أَلَمْ تَرَ أَنَّهَا تَخْرُجُ صَفْرَاءَ مُلْتَوِيَةً.",
                "Ebû Saîd el-Hudrî'den: Nebî (s.a.v.) buyurdu: “Cennet ehli cennete, cehennem ehli cehenneme girer. Sonra Allah Teâlâ: ‘Kalbinde hardal tanesi ağırlığınca iman bulunan kimseleri (ateşten) çıkarın’ buyurur. Onlar kapkara kesilmiş hâlde çıkarılır ve hayâ nehrine atılırlar; sel kenarındaki tohumun bittiği gibi biterler. Görmez misin, o (tohum) sapsarı ve kıvrım kıvrım çıkar.”",
                "<b>Buhârî, Îmân, 15; Müslim, Îmân, 304; İbn Mâce, Mukaddime, 9.</b> Râvi: Ebû Saîd el-Hudrî.",
            ),
        ])
        .add_table(ComparisonTable(
            "Aynî'nin “Üç Faydası” — Hadis Hangi Fırkaya Karşı Delildir?",
            ["Fırka / İlke", "Görüşü", "Hadisin cevabı"],
            [
                ["<b>Mürcie</b>", "“İmanla birlikte günah zarar vermez; âsi ateşe girmez.”", "Âsi mü'minlerden bir kısmının <b>ateşe gireceği</b> anlaşılır"],
                ["<b>Mu'tezile</b>", "“Büyük günah işleyen ateşte <b>ebedî</b> kalır.”", "Âsinin ateşte <b>ebedî kalması gerekmediği</b> gösterilir"],
                ["<b>Tefâdul ilkesi</b>", "—", "İman ehlinin <b>amelde derece derece</b> olduğunun delilidir"],
            ],
        ))
        .add_summary(
            "İman ne tek parçadır ne de eşit dağılmıştır: alâmeti vardır (İman 3–4), tadı vardır "
            "(İman 5), şubeleri vardır (İman 6) ve sahipleri arasında derece farkı vardır "
            "(İman 7). Bu dört adım, Ehl-i Sünnet'in iman anlayışını hem Mürcie'ye hem "
            "Mu'tezile'ye karşı konumlandırır."
        )
    )

    # =======================================================================
    # 5. BÖLÜM — Kâmil İmana Aykırı Davranışlar (Kitâbü'l-Îmân 8–12)
    # =======================================================================
    ch5 = Chapter(
        number=5,
        title="Kâmil İmana Aykırı Davranışlar",
        subtitle="Kitâbü'l-Îmân 8–12 · Amelî nifak, mecazi küfür ve mütâbaat kavramı",
        key_terms=[
            KeyTerm("Nifâk-ı amelî", "Kişiyi dinden çıkarmayan, ancak <b>kâmil imana aykırı</b> davranış nifakı. Münafığın dört alâmeti bu kapsamdadır — bâb başlığı da bunu söyler."),
            KeyTerm("Füsûk", "Sözlükte “çıkmak”; şer'an <b>Allah ve Resûlüne itaatten çıkmak</b>. “Müslümana sövmek füsûktur.”"),
            KeyTerm("Mütâbaat", "Bir hadisin lafzına/manasına uygun başka bir rivayetin, <b>farklı bir râvi</b> tarafından aynı senedle (tamamen veya kısmen) nakledilmesi; iki rivayetin birbirini desteklemesi."),
            KeyTerm("Şâhid", "Herhangi bir hadise, aynı sahâbîden ya da <b>başka bir sahâbîden</b> gelen benzer muhtevalı ikinci hadis."),
        ],
    )
    ch5.pages.append(
        ChapterPage()
        .add_terms(ch5.key_terms)
        .add_ayat("Bâb: el-Umûru'lletî Tuhâlifü'l-Îmâne'l-Kâmil", [
            Ayah(
                "İman 8 — EZBER (احفظ): Münafığın Dört Alâmeti",
                "عَنْ عَبْدِ اللهِ بْنِ عَمْرٍو أَنَّ النَّبِيَّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ قَالَ: أَرْبَعٌ مَنْ كُنَّ فِيهِ كَانَ مُنَافِقًا خَالِصًا، وَمَنْ كَانَتْ فِيهِ خَصْلَةٌ مِنْهُنَّ كَانَتْ فِيهِ خَصْلَةٌ مِنَ النِّفَاقِ حَتَّى يَدَعَهَا: إِذَا اؤْتُمِنَ خَانَ، وَإِذَا حَدَّثَ كَذَبَ، وَإِذَا عَاهَدَ غَدَرَ، وَإِذَا خَاصَمَ فَجَرَ.",
                "Abdullah b. Amr'dan: Nebî (s.a.v.) buyurdu: “Dört şey vardır ki kimde bulunursa o kimse hâlis (katıksız) münafıktır. Kimde bunlardan biri bulunursa, onu terk edinceye kadar kendisinde nifaktan bir haslet var demektir: (1) kendisine bir şey emanet edildiğinde hıyanet eder, (2) konuştuğunda yalan söyler, (3) söz verdiğinde sözünden döner, (4) düşmanlık ettiğinde haddi aşar.”",
                "<b>Buhârî, Îmân, 24; Müslim, Îmân, 106.</b> Metnin sonundaki <b>“تابعه شعبة عن الأعمش”</b> ifadesi bir <b>mütâbaat</b> örneğidir. Kaynak metinde <b>(احفظ)</b> işaretlidir.",
            ),
        ])
    )
    ch5.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Mütâbaat Ailesi — Dipnotta Hatırlatılan Dört Terim",
            ["Terim", "Tanımı"],
            [
                ["<b>Mütâbaat</b>", "Bir hadisin lafzına/manasına uygun başka bir rivayetin, <b>farklı bir râvi</b> tarafından aynı senedle nakledilmesi"],
                ["<b>Mütâbi'</b>", "Bu destekleyici rivayeti yapan <b>râvi</b>"],
                ["<b>Mütâbâ' aleyh</b>", "Kendisine mütâbaat edilen râvi ya da hadis"],
                ["<b>Şâhid</b>", "Aynı veya <b>başka bir sahâbîden</b> gelen benzer muhtevalı ikinci hadis"],
                ["<b>Âdıd</b>", "Bir hadisi destekleyen, ya da kusuru bulunan bir haberin bu kusurunu <b>gideren</b> diğer haber"],
            ],
        ))
        .add_person(ABDULLAH_B_AMR)
        .add_ayat("Bâb: Kâmil İmana Aykırı İşler (devam)", [
            Ayah(
                "İman 9 — “Zinâ eden, zinâ ederken mü'min olarak zinâ etmez”",
                "عَنْ أَبِي هُرَيْرَةَ أَنَّ رَسُولَ اللهِ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ قَالَ: لَا يَزْنِي الزَّانِي حِينَ يَزْنِي وَهُوَ مُؤْمِنٌ، وَلَا يَشْرَبُ الْخَمْرَ حِينَ يَشْرَبُ وَهُوَ مُؤْمِنٌ، وَلَا يَسْرِقُ حِينَ يَسْرِقُ وَهُوَ مُؤْمِنٌ، وَلَا يَنْتَهِبُ نُهْبَةً يَرْفَعُ النَّاسُ إِلَيْهِ فِيهَا أَبْصَارَهُمْ وَهُوَ مُؤْمِنٌ.",
                "Ebû Hüreyre'den: Resûlullah (s.a.v.) buyurdu: “Zinâ eden kimse zinâ ettiği sırada mü'min olduğu hâlde zinâ etmez; içki içen içtiği sırada mü'min olduğu hâlde içmez; hırsızlık yapan yaptığı sırada mü'min olduğu hâlde çalmaz; insanların gözlerini kendisine çevirecekleri bir yağmayı yapan da bunu mü'min olduğu hâlde yapmaz.”",
                "<b>Buhârî, Hudûd, 1; Müslim, Îmân, 100; Nesâî, Kat'u's-Sârik, 1.</b> Aynî bu hadisi <b>Nisâ 4/116</b> ve <b>İman 23</b> ile birlikte tartışır.",
            ),
        ])
    )
    ch5.pages.append(
        ChapterPage()
        .add_ayat(None, [
            Ayah(
                "İman 10 — “Müslümana sövmek füsûk, onunla savaşmak küfürdür”",
                "عَنْ زُبَيْدٍ قَالَ: سَأَلْتُ أَبَا وَائِلٍ عَنِ الْمُرْجِئَةِ، فَقَالَ: حَدَّثَنِي عَبْدُ اللهِ أَنَّ النَّبِيَّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ قَالَ: سِبَابُ الْمُسْلِمِ فُسُوقٌ، وَقِتَالُهُ كُفْرٌ.",
                "Zübeyd der ki: Ebû Vâil'e Mürcie hakkında sordum; şöyle dedi: Bana Abdullah (b. Mes'ûd) anlattı ki Nebî (s.a.v.): “Müslümana sövmek fâsıklık, onunla savaşmak küfürdür” buyurdu.",
                "<b>Buhârî, Îmân, 36; Müslim, Îmân, 116; Tirmizî, Birr ve's-Sıla, 52.</b> Sorunun <b>Mürcie bağlamında</b> sorulmuş olması dikkat çekicidir.",
            ),
        ])
        .add_block(BulletBlock(1, "İbn Hacer: “Kıtâlühû küfr” Ne Demek Değildir?", [
            "Burada <b>milletten çıkaran hakiki küfür</b> kastedilmemiştir. Üç izah yapılır:",
            "<b>(1) Mübalağa fi't-tahzîr:</b> Sakındırmada mübalağa için “küfür” denmiştir; şefaat hadisi ve "
            "Nisâ 116 gibi yerleşik kaideler bunun milletten çıkarmadığını gösterir.",
            "<b>(2) Benzetme:</b> “Mü'minle savaşmak <b>kâfirin işidir</b>” — fiil, faile benzetilerek "
            "isimlendirilmiştir.",
            "<b>(3) Lugavî küfür:</b> Küfür sözlükte <b>“örtmek”</b>tir. Müslümanın müslüman üzerindeki hakkı "
            "ona yardım etmektir; onunla savaşan bu hakkı <b>örtmüş</b> olur.",
        ]))
        .add_ayat("Bâb: Kâmil İmana Aykırı İşler (devam)", [
            Ayah(
                "İman 11 — “Bize silah çeken bizden değildir”",
                "عَنْ أَبِي هُرَيْرَةَ أَنَّ رَسُولَ اللهِ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ قَالَ: مَنْ حَمَلَ عَلَيْنَا السِّلَاحَ فَلَيْسَ مِنَّا، وَمَنْ غَشَّنَا فَلَيْسَ مِنَّا.",
                "Ebû Hüreyre'den: Resûlullah (s.a.v.) buyurdu: “Bize silah çeken bizden değildir; bizi aldatan da bizden değildir.”",
                "<b>Müslim, Îmân, 164.</b> İbn Hacer: <b>“leyse minnâ”</b> = “bizim <b>yolumuz/tarîkatımız</b> üzere değildir, bize tâbi değildir” demektir — dinden çıkma anlamı taşımaz.",
            ),
        ])
    )
    ch5.pages.append(
        ChapterPage()
        .add_ayat(None, [
            Ayah(
                "İman 12 — Allah'ın Konuşmayacağı Üç Kişi",
                "عَنْ أَبِي ذَرٍّ عَنِ النَّبِيِّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ قَالَ: ثَلَاثَةٌ لَا يُكَلِّمُهُمُ اللهُ يَوْمَ الْقِيَامَةِ، وَلَا يَنْظُرُ إِلَيْهِمْ، وَلَا يُزَكِّيهِمْ، وَلَهُمْ عَذَابٌ أَلِيمٌ. قَالَ أَبُو ذَرٍّ: خَابُوا وَخَسِرُوا! مَنْ هُمْ يَا رَسُولَ اللهِ؟ قَالَ: الْمُسْبِلُ، وَالْمَنَّانُ، وَالْمُنَفِّقُ سِلْعَتَهُ بِالْحَلِفِ الْكَاذِبِ.",
                "Ebû Zerr'den: Nebî (s.a.v.) buyurdu: “Üç kişi vardır ki kıyamet günü Allah onlarla konuşmaz, onlara bakmaz, onları temize çıkarmaz; onlar için can yakıcı bir azap vardır.” (Bunu üç kez tekrar etti.) Ebû Zerr: “Hüsrana uğradılar, kaybettiler! Kimdir onlar ey Allah'ın Resûlü?” dedi. Buyurdu: “Elbisesini (kibirle) yerlerde sürüyen, verdiğini başa kakan ve yalan yeminle malını pazarlayan.”",
                "<b>Müslim, Îmân, 171; Ebû Dâvûd, Libâs, 28; Tirmizî, Büyû', 4.</b> Üçlü: <b>müsbil · mennân · yalan yeminle mal satan.</b>",
            ),
        ])
        .add_callout(Callout(
            "caution", "Bâb Başlığını Okuyun — Bütün Bölümün Anahtarı Orada",
            "Bâbın adı <b>“Kâmil imana AYKIRI işler”</b>dir. Bu başlık, içindeki bütün sert ifadeleri "
            "(“münafıktır”, “küfürdür”, “bizden değildir”, “mü'min olarak yapmaz”) tek bir çerçeveye oturtur: "
            "hiçbiri kişiyi <u>dinden çıkarmaz</u>; hepsi <b>imanın kemâline</b> zarar verir. Sınavda bu "
            "hadislerden biri sorulduğunda doğru şık neredeyse her zaman <b>“amelî nifak / kemâlin nefyi / "
            "mecazi küfür”</b> yönündedir."
        ))
        .add_summary(
            "Beş rivayet aynı mantığı beş farklı ifadeyle kurar: emanete hıyanet ve yalan amelî nifaktır "
            "(8), büyük günahlar kemâl-i imanı askıya alır (9), müslümanla savaşmak mecazi küfürdür "
            "(10), silah çekmek ve aldatmak kişiyi Peygamber'in yolundan çıkarır (11), kibir-minnet-yalan "
            "yemin ise ilahî iltifattan mahrum bırakır (12)."
        )
    )

    # =======================================================================
    # 6. BÖLÜM — İslâm'ın İşleri ve En Faziletli Amel (Kitâbü'l-Îmân 13–16)
    # =======================================================================
    ch6 = Chapter(
        number=6,
        title="İslâm'ın İşleri ve En Faziletli Amel",
        subtitle="Kitâbü'l-Îmân 13–16 · İmanın ahlâkî sonuçları ve “efdalü'l-a'mâl” rivayetlerinin cem'i",
        key_terms=[
            KeyTerm("Efdalü'l-a'mâl", "Amellerin en faziletlisi. Farklı rivayetlerde farklı cevaplar verildiği için <b>cem' ve te'lîf</b> gerektiren klasik bir örnektir."),
            KeyTerm("Cem' ve te'lîf", "Görünüşte çelişen rivayetleri uzlaştırma yöntemi. Kaffâl el-Kebîr iki vecih sunar: hâllerin/şahısların farklılığı, ya da ifadede <b>“min”</b> takdiri."),
            KeyTerm("Hacc-ı mebrûr", "Makbul hac; içine günah ve riya karışmamış, kabul edilmiş hac. İman 16'da cihaddan sonra üçüncü sırada zikredilir."),
            KeyTerm("İr'â'", "Acıma, saygı gösterip esirgeme. İbn Mes'ûd, “daha fazla sormayı ancak <b>ona saygı gösterip esirgediğim için</b> bıraktım” demiştir."),
        ],
    )
    ch6.pages.append(
        ChapterPage()
        .add_terms(ch6.key_terms)
        .add_ayat("Bâb: Umûru'l-İslâm evi'l-Îmân", [
            Ayah(
                "İman 13 — “İslâm'ın hangisi daha hayırlıdır?”",
                "عَنْ عَبْدِ اللهِ بْنِ عَمْرٍو رَضِيَ اللهُ عَنْهُمَا أَنَّ رَجُلًا سَأَلَ النَّبِيَّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ: أَيُّ الْإِسْلَامِ خَيْرٌ؟ قَالَ: تُطْعِمُ الطَّعَامَ، وَتَقْرَأُ السَّلَامَ عَلَى مَنْ عَرَفْتَ وَمَنْ لَمْ تَعْرِفْ.",
                "Abdullah b. Amr'dan: Bir adam Nebî'ye (s.a.v.): “İslâm'ın hangisi daha hayırlıdır?” diye sordu. Buyurdu: “Yemek yedirmen ve tanıdığın-tanımadığın herkese selam vermendir.”",
                "<b>Buhârî, Îmân, 5; Müslim, Îmân, 63; Ebû Dâvûd, Edeb, 142; İbn Mâce, Et'ime, 1.</b>",
            ),
            Ayah(
                "İman 14 — “Allah'a ve âhiret gününe iman eden…”",
                "عَنْ أَبِي هُرَيْرَةَ قَالَ: قَالَ رَسُولُ اللهِ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ: مَنْ كَانَ يُؤْمِنُ بِاللهِ وَالْيَوْمِ الْآخِرِ فَلَا يُؤْذِ جَارَهُ، وَمَنْ كَانَ يُؤْمِنُ بِاللهِ وَالْيَوْمِ الْآخِرِ فَلْيُكْرِمْ ضَيْفَهُ، وَمَنْ كَانَ يُؤْمِنُ بِاللهِ وَالْيَوْمِ الْآخِرِ فَلْيَقُلْ خَيْرًا أَوْ لِيَصْمُتْ.",
                "Ebû Hüreyre'den: Resûlullah (s.a.v.) buyurdu: “Allah'a ve âhiret gününe iman eden komşusuna eziyet etmesin. Allah'a ve âhiret gününe iman eden misafirine ikram etsin. Allah'a ve âhiret gününe iman eden ya hayır söylesin ya da sussun.”",
                "<b>Buhârî, Edeb, 31; Müslim, Îmân, 74; Tirmizî, Birr ve's-Sıla, 43.</b> Üç şart: <b>komşu hakkı · misafir ikramı · dil muhafazası.</b>",
            ),
        ])
    )
    ch6.pages.append(
        ChapterPage()
        .add_ayat("Bâb: Umûru'l-İslâm ve el-Îmân billâh", [
            Ayah(
                "İman 15 — Amellerin En Faziletlisi (İbn Mes'ûd rivayeti)",
                "عَنْ عَبْدِ اللهِ بْنِ مَسْعُودٍ قَالَ: سَأَلْتُ رَسُولَ اللهِ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ: أَيُّ الْعَمَلِ أَفْضَلُ؟ قَالَ: الصَّلَاةُ لِوَقْتِهَا. قُلْتُ ثُمَّ أَيٌّ؟ قَالَ: بِرُّ الْوَالِدَيْنِ. قُلْتُ ثُمَّ أَيٌّ؟ قَالَ: الْجِهَادُ فِي سَبِيلِ اللهِ. فَمَا تَرَكْتُ أَسْتَزِيدُهُ إِلَّا إِرْعَاءً عَلَيْهِ.",
                "İbn Mes'ûd'dan: Resûlullah'a (s.a.v.) “Amellerin hangisi daha faziletlidir?” diye sordum. “Vaktinde kılınan namaz” buyurdu. “Sonra hangisi?” dedim; “Ana-babaya iyilik” buyurdu. “Sonra hangisi?” dedim; “Allah yolunda cihad” buyurdu. Daha fazla sormayı ancak ona saygı gösterip esirgediğim için bıraktım.",
                "<b>Müslim, Îmân, 137; Buhârî, Tevhîd, 48.</b> Sıra: <b>namaz → birru'l-vâlideyn → cihad.</b>",
            ),
            Ayah(
                "İman 16 — Amellerin En Faziletlisi (Ebû Hüreyre rivayeti)",
                "عَنْ أَبِي هُرَيْرَةَ أَنَّ رَسُولَ اللهِ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ سُئِلَ: أَيُّ الْعَمَلِ أَفْضَلُ؟ فَقَالَ: إِيمَانٌ بِاللهِ وَرَسُولِهِ. قِيلَ: ثُمَّ مَاذَا؟ قَالَ: الْجِهَادُ فِي سَبِيلِ اللهِ. قِيلَ: ثُمَّ مَاذَا؟ قَالَ: حَجٌّ مَبْرُورٌ.",
                "Ebû Hüreyre'den: Resûlullah'a (s.a.v.) “Amellerin hangisi daha faziletlidir?” diye soruldu. “Allah'a ve Resûlüne iman” buyurdu. “Sonra hangisi?” denildi; “Allah yolunda cihad” buyurdu. “Sonra hangisi?” denildi; “Makbul (mebrûr) bir hac” buyurdu.",
                "<b>Buhârî, Îmân, 16; Hac, 4; Müslim, Îmân, 135; Nesâî, Menâsikü'l-Hac, 4.</b> Sıra: <b>iman → cihad → hacc-ı mebrûr.</b>",
            ),
        ])
        .add_table(ComparisonTable(
            "“En Faziletli Amel” Rivayetleri — Dört Farklı Cevap (Aynî, Umde)",
            ["Râvi / Rivayet", "Soru", "Verilen cevap"],
            [
                ["<b>İbn Mes'ûd</b> (İman 15)", "Eyyü'l-ameli efdal?", "Vaktinde namaz → ana-babaya iyilik → cihad"],
                ["<b>Abdullah b. Amr</b> (İman 13)", "Eyyü'l-İslâmi hayr?", "Yemek yedirmek + tanıdık-tanımadık herkese selam"],
                ["<b>Ebû Mûsâ</b>", "Eyyü'l-İslâmi efdal?", "“Müslümanların, elinden ve dilinden selâmette olduğu kimse”"],
                ["<b>Ebû Hüreyre / Ebû Zerr</b> (İman 16)", "Eyyü'l-ameli efdal?", "Allah ve Resûlüne iman → cihad → hacc-ı mebrûr"],
            ],
        ))
    )
    ch6.pages.append(
        ChapterPage()
        .add_block(BulletBlock(1, "Kaffâl el-Kebîr eş-Şâfiî'nin İki Cem' Vechi", [
            "<b>Birinci vecih — Hâllerin ve şahısların farklılığı:</b> Cevaplar, soranın durumuna ve içinde "
            "bulunulan şartlara göre verilmiştir. Herkese aynı “en faziletli” gösterilmez; kişiye <b>en çok "
            "ihtiyaç duyduğu</b> amel söylenir.",
            "<b>İkinci vecih — İfadede “مِنْ” takdiri:</b> Kastedilen “amellerin <b>en faziletlilerinden "
            "biri</b>”dir. Nitekim “<i>hayruküm hayruküm li-ehlih</i>” (sizin en hayırlınız ailesine karşı en "
            "hayırlı olanınızdır) hadisinde de kişi mutlak olarak <b>“insanların en hayırlısı”</b> olmuş sayılmaz.",
            "Aynî'nin naklettiği bu izah, ders boyunca karşılaşılan <b>ihtilâfü'l-hadîs</b> problemini çözmenin "
            "standart yöntemidir; aynı yöntem İman 9 ↔ İman 23 çelişkisinde de kullanılır.",
        ]))
        .add_callout(Callout(
            "route", "Bölüm Rotası",
            "İman 13–14 imanın <b>ahlâkî sonucunu</b> (yemek, selam, komşu, misafir, dil) verir; İman 15–16 ise "
            "aynı soruyu <b>ibadet ekseninde</b> cevaplar. İkisi arasındaki fark bir çelişki değil, "
            "<b>muhataba göre cevap</b>tır."
        ))
        .add_summary(
            "Bu bölüm iki şey öğretir: (1) iman soyut bir tasdik değil, komşuya-misafire-dile yansıyan "
            "somut bir ahlâk programıdır; (2) aynı soruya verilen farklı cevaplar cem' ve "
            "te'lîf ile uzlaştırılır — hadis usûlünün en sık işletilen kuralıdır."
        )
    )

    # =======================================================================
    # 7. BÖLÜM — Allah'a İman: Biat, Davet ve Kebâir (Kitâbü'l-Îmân 17–23)
    # =======================================================================
    ch7 = Chapter(
        number=7,
        title="Allah'a İman: Biat, Davet ve Kebâir",
        subtitle="Kitâbü'l-Îmân 17–23 · Had cezalarının keffâreti, tedrîcî davet ve büyük günah tartışması",
        key_terms=[
            KeyTerm("Biat", "Bağlılık sözleşmesi. Ubâde b. es-Sâmit'in rivayetinde altı yasak üzerine yapılır; muhtevası <b>Mümtehine 60/12</b> ile örtüşür."),
            KeyTerm("Setr", "Allah'ın kulun günahını örtmesi. Örtülen günahın hükmü Allah'a kalmıştır: “dilerse affeder, dilerse cezalandırır.”"),
            KeyTerm("Seb'u'l-mûbikāt", "Yedi helâk edici büyük günah: şirk, sihir, haksız yere adam öldürme, faiz, yetim malı, savaştan kaçma, iffetli kadına iftira."),
            KeyTerm("Mûcibetân", "“İki gerektirici”: şirksiz ölmek <b>cenneti</b>, şirkle ölmek <b>cehennemi</b> gerektirir."),
        ],
    )
    ch7.pages.append(
        ChapterPage()
        .add_terms(ch7.key_terms)
        .add_ayat("Bâb: el-Îmân billâh (Allah'a İman)", [
            Ayah(
                "İman 17 — Biat Hadisi (Ubâde b. es-Sâmit)",
                "عَنْ عُبَادَةَ بْنِ الصَّامِتِ رَضِيَ اللهُ عَنْهُ أَنَّ رَسُولَ اللهِ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ قَالَ وَحَوْلَهُ عِصَابَةٌ مِنْ أَصْحَابِهِ: بَايِعُونِي عَلَى أَنْ لَا تُشْرِكُوا بِاللهِ شَيْئًا، وَلَا تَسْرِقُوا، وَلَا تَزْنُوا، وَلَا تَقْتُلُوا أَوْلَادَكُمْ، وَلَا تَأْتُوا بِبُهْتَانٍ تَفْتَرُونَهُ بَيْنَ أَيْدِيكُمْ وَأَرْجُلِكُمْ، وَلَا تَعْصُوا فِي مَعْرُوفٍ. فَمَنْ وَفَى مِنْكُمْ فَأَجْرُهُ عَلَى اللهِ، وَمَنْ أَصَابَ مِنْ ذَلِكَ شَيْئًا فَعُوقِبَ فِي الدُّنْيَا فَهُوَ كَفَّارَةٌ لَهُ، وَمَنْ أَصَابَ مِنْ ذَلِكَ شَيْئًا ثُمَّ سَتَرَهُ اللهُ فَهُوَ إِلَى اللهِ، إِنْ شَاءَ عَفَا عَنْهُ وَإِنْ شَاءَ عَاقَبَهُ. فَبَايَعْنَاهُ عَلَى ذَلِكَ.",
                "Ubâde b. es-Sâmit'ten: Resûlullah (s.a.v.), etrafında ashabından bir topluluk varken buyurdu: “Bana şunlar üzerine biat edin: Allah'a hiçbir şeyi ortak koşmayacaksınız, hırsızlık yapmayacaksınız, zinâ etmeyeceksiniz, çocuklarınızı öldürmeyeceksiniz, elleriniz ve ayaklarınız arasında uydurduğunuz bir iftira getirmeyeceksiniz, ma'rûf olan hiçbir işte (bana) isyan etmeyeceksiniz. Kim buna vefa gösterirse ecri Allah'a aittir. Kim bunlardan birini işler de dünyada cezalandırılırsa bu onun için keffârettir. Kim bunlardan birini işler de Allah onu örterse, işi Allah'a kalmıştır: dilerse affeder, dilerse cezalandırır.” Biz de bunun üzerine ona biat ettik.",
                "<b>Buhârî, Îmân, 11; Müslim, Hudûd, 41; Tirmizî, Hudûd, 12; Nesâî, Bey'a, 9.</b> <b>Had cezalarının keffâret olması</b> ilkesinin ana delilidir.",
            ),
        ])
    )
    ch7.pages.append(
        ChapterPage()
        .add_person(UBADE)
        .add_ayat(None, [
            Ayah(
                "İman 18 — Bedevînin Sorusu: “Beni cennete sokacak ameli göster”",
                "عَنْ أَبِي هُرَيْرَةَ رَضِيَ اللهُ عَنْهُ أَنَّ أَعْرَابِيًّا أَتَى النَّبِيَّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ فَقَالَ: دُلَّنِي عَلَى عَمَلٍ إِذَا عَمِلْتُهُ دَخَلْتُ الْجَنَّةَ. قَالَ: تَعْبُدُ اللهَ وَلَا تُشْرِكُ بِهِ شَيْئًا، وَتُقِيمُ الصَّلَاةَ الْمَكْتُوبَةَ، وَتُؤَدِّي الزَّكَاةَ الْمَفْرُوضَةَ، وَتَصُومُ رَمَضَانَ. قَالَ: وَالَّذِي نَفْسِي بِيَدِهِ لَا أَزِيدُ عَلَى هَذَا. فَلَمَّا وَلَّى قَالَ النَّبِيُّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ: مَنْ سَرَّهُ أَنْ يَنْظُرَ إِلَى رَجُلٍ مِنْ أَهْلِ الْجَنَّةِ فَلْيَنْظُرْ إِلَى هَذَا.",
                "Ebû Hüreyre'den: Bir bedevî Nebî'ye (s.a.v.) gelip: “Bana, yaptığım takdirde cennete gireceğim bir amel göster” dedi. Buyurdu: “Allah'a kulluk edersin, O'na hiçbir şeyi ortak koşmazsın; farz namazı kılarsın; farz zekâtı verirsin; ramazan orucunu tutarsın.” Adam: “Nefsim elinde olana yemin ederim ki buna hiçbir şey eklemeyeceğim” dedi. Adam dönüp gidince Nebî (s.a.v.): “Cennet ehlinden bir adama bakmak kimi sevindirirse şuna baksın” buyurdu.",
                "<b>Buhârî, Zekât, 1; Müslim, Îmân, 15.</b> Sayılan dört rükün, <b>Cibrîl hadisindeki İslâm tarifiyle birebir aynıdır</b> (hac yok).",
            ),
        ])
        .add_ayat("Bâb: el-Îmân billâh (devam)", [
            Ayah(
                "İman 19 — Muâz'ın Yemen'e Gönderilişi (Tedrîcî Davet)",
                "عَنِ ابْنِ عَبَّاسٍ رَضِيَ اللهُ عَنْهُمَا أَنَّ النَّبِيَّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ بَعَثَ مُعَاذًا إِلَى الْيَمَنِ فَقَالَ: ادْعُهُمْ إِلَى شَهَادَةِ أَنْ لَا إِلَهَ إِلَّا اللهُ وَأَنِّي رَسُولُ اللهِ، فَإِنْ هُمْ أَطَاعُوا لِذَلِكَ فَأَعْلِمْهُمْ أَنَّ اللهَ قَدِ افْتَرَضَ عَلَيْهِمْ خَمْسَ صَلَوَاتٍ فِي كُلِّ يَوْمٍ وَلَيْلَةٍ، فَإِنْ هُمْ أَطَاعُوا لِذَلِكَ فَأَعْلِمْهُمْ أَنَّ اللهَ افْتَرَضَ عَلَيْهِمْ صَدَقَةً فِي أَمْوَالِهِمْ تُؤْخَذُ مِنْ أَغْنِيَائِهِمْ وَتُرَدُّ عَلَى فُقَرَائِهِمْ.",
                "İbn Abbâs'tan: Nebî (s.a.v.) Muâz'ı Yemen'e gönderirken buyurdu: “Onları, Allah'tan başka ilah olmadığına ve benim Allah'ın Resûlü olduğuma şehâdet etmeye çağır. Buna itaat ederlerse, Allah'ın onlara her gün ve gecede beş vakit namazı farz kıldığını bildir. Buna da itaat ederlerse, Allah'ın onlara mallarında, zenginlerinden alınıp fakirlerine verilecek bir sadakayı (zekâtı) farz kıldığını bildir.”",
                "<b>Buhârî, Zekât, 1; Müslim, Îmân, 29; Ebû Dâvûd, Zekât, 4; İbn Mâce, Zekât, 1.</b> Zekâtın işleyişi: <b>“zenginden alınır, fakire verilir.”</b>",
            ),
        ])
    )
    ch7.pages.append(
        ChapterPage()
        .add_ayat(None, [
            Ayah(
                "İman 20 — Allah'ın Hakkı, Kulların Hakkı",
                "عَنْ مُعَاذِ بْنِ جَبَلٍ رَضِيَ اللهُ عَنْهُ قَالَ: بَيْنَا أَنَا رَدِيفُ النَّبِيِّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ لَيْسَ بَيْنِي وَبَيْنَهُ إِلَّا آخِرَةُ الرَّحْلِ، فَقَالَ: يَا مُعَاذُ! قُلْتُ: لَبَّيْكَ رَسُولَ اللهِ وَسَعْدَيْكَ. قَالَ: هَلْ تَدْرِي مَا حَقُّ اللهِ عَلَى عِبَادِهِ؟ قُلْتُ: اللهُ وَرَسُولُهُ أَعْلَمُ. قَالَ: حَقُّ اللهِ عَلَى عِبَادِهِ أَنْ يَعْبُدُوهُ وَلَا يُشْرِكُوا بِهِ شَيْئًا. ثُمَّ قَالَ: هَلْ تَدْرِي مَا حَقُّ الْعِبَادِ عَلَى اللهِ إِذَا فَعَلُوهُ؟ قُلْتُ: اللهُ وَرَسُولُهُ أَعْلَمُ. قَالَ: حَقُّ الْعِبَادِ عَلَى اللهِ أَنْ لَا يُعَذِّبَهُمْ.",
                "Muâz b. Cebel'den: Ben Nebî'nin (s.a.v.) terkisinde, aramızda semerin arka kaşından başka bir şey yokken bana: “Ey Muâz!” dedi. “Buyur ey Allah'ın Resûlü, emrine âmâdeyim” dedim. Buyurdu: “Allah'ın kulları üzerindeki hakkı nedir, bilir misin?” “Allah ve Resûlü daha iyi bilir” dedim. “Allah'ın kulları üzerindeki hakkı, O'na kulluk etmeleri ve hiçbir şeyi O'na ortak koşmamalarıdır” buyurdu. Sonra: “Kullar bunu yaptıklarında, kulların Allah üzerindeki hakkı nedir, bilir misin?” dedi. “Allah ve Resûlü daha iyi bilir” dedim. “Kulların Allah üzerindeki hakkı, onlara azap etmemesidir” buyurdu.",
                "<b>Buhârî, Libâs, 101; Müslim, Îmân, 48.</b> <b>İlim 24 ile aynı sahnedir</b> (Muâz terkide, üç kez seslenme) — ikisi birlikte sorulabilir.",
            ),
        ])
        .add_ayat("Bâb: el-Îmân billâh (devam)", [
            Ayah(
                "İman 21 — Yedi Helâk Edici (Seb'u'l-Mûbikāt)",
                "عَنْ أَبِي هُرَيْرَةَ رَضِيَ اللهُ عَنْهُ عَنِ النَّبِيِّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ قَالَ: اجْتَنِبُوا السَّبْعَ الْمُوبِقَاتِ. قَالُوا: يَا رَسُولَ اللهِ! وَمَا هُنَّ؟ قَالَ: الشِّرْكُ بِاللهِ، وَالسِّحْرُ، وَقَتْلُ النَّفْسِ الَّتِي حَرَّمَ اللهُ إِلَّا بِالْحَقِّ، وَأَكْلُ الرِّبَا، وَأَكْلُ مَالِ الْيَتِيمِ، وَالتَّوَلِّي يَوْمَ الزَّحْفِ، وَقَذْفُ الْمُحْصَنَاتِ الْمُؤْمِنَاتِ الْغَافِلَاتِ.",
                "Ebû Hüreyre'den: Nebî (s.a.v.) buyurdu: “Helâk edici yedi şeyden sakının.” “Ey Allah'ın Resûlü, onlar nelerdir?” dediler. Buyurdu: “Allah'a şirk koşmak, sihir, Allah'ın haram kıldığı canı haksız yere öldürmek, faiz yemek, yetim malı yemek, savaş günü (düşmandan) kaçmak ve iffetli, mü'mine, habersiz kadınlara zinâ iftirası atmak.”",
                "<b>Buhârî, Vesâyâ, 24; Müslim, Îmân, 145; Ebû Dâvûd, Vesâyâ, 10.</b> <b>Kebâir</b> konusunun temel metnidir.",
            ),
            Ayah(
                "İman 22 — İki Gerektirici (el-Mûcibetân)",
                "عَنْ جَابِرٍ قَالَ: أَتَى النَّبِيَّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ رَجُلٌ فَقَالَ: يَا رَسُولَ اللهِ مَا الْمُوجِبَتَانِ؟ فَقَالَ: مَنْ مَاتَ لَا يُشْرِكُ بِاللهِ شَيْئًا دَخَلَ الْجَنَّةَ، وَمَنْ مَاتَ يُشْرِكُ بِاللهِ شَيْئًا دَخَلَ النَّارَ.",
                "Câbir'den: Nebî'ye (s.a.v.) bir adam gelip: “Ey Allah'ın Resûlü, iki gerektirici nedir?” diye sordu. Buyurdu: “Kim Allah'a hiçbir şeyi ortak koşmadan ölürse cennete girer; kim de Allah'a bir şeyi ortak koşarak ölürse cehenneme girer.”",
                "<b>Müslim, Îmân, 151.</b> Terim olarak sorulabilir: <b>mûcibetân</b> = cenneti ve cehennemi <b>gerektiren</b> iki şey.",
            ),
        ])
    )
    ch7.pages.append(
        ChapterPage()
        .add_ayat("Bâb: el-Îmân billâh — Bölümün Son Rivayeti", [
            Ayah(
                "İman 23 — Ebû Zerr: “Zinâ etse de, hırsızlık yapsa da”",
                "عَنْ أَبِي ذَرٍّ رَضِيَ اللهُ عَنْهُ قَالَ: أَتَيْتُ النَّبِيَّ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ وَعَلَيْهِ ثَوْبٌ أَبْيَضُ وَهُوَ نَائِمٌ، ثُمَّ أَتَيْتُهُ وَقَدِ اسْتَيْقَظَ فَقَالَ: مَا مِنْ عَبْدٍ قَالَ لَا إِلَهَ إِلَّا اللهُ ثُمَّ مَاتَ عَلَى ذَلِكَ إِلَّا دَخَلَ الْجَنَّةَ. قُلْتُ: وَإِنْ زَنَى وَإِنْ سَرَقَ؟ قَالَ: وَإِنْ زَنَى وَإِنْ سَرَقَ. (ثَلَاثًا) ... قَالَ: وَإِنْ زَنَى وَإِنْ سَرَقَ عَلَى رَغْمِ أَنْفِ أَبِي ذَرٍّ. وَكَانَ أَبُو ذَرٍّ إِذَا حَدَّثَ بِهَذَا قَالَ: وَإِنْ رَغِمَ أَنْفُ أَبِي ذَرٍّ.",
                "Ebû Zerr'den: Nebî'ye (s.a.v.), üzerinde beyaz bir elbise varken uyur hâlde geldim; sonra uyanmış olarak tekrar geldim. Buyurdu: “‘Lâ ilâhe illallâh’ deyip sonra bunun üzere ölen hiçbir kul yoktur ki cennete girmesin.” “Zinâ etse ve hırsızlık yapsa da mı?” dedim. “Zinâ etse de hırsızlık yapsa da” buyurdu. (Bunu üç kez tekrarladım.) Üçüncüsünde: “Zinâ etse de hırsızlık yapsa da — Ebû Zerr'in burnu sürtülse bile!” buyurdu. Ebû Zerr bu hadisi rivayet ettiğinde: “Ebû Zerr'in burnu sürtülse de” derdi.",
                "<b>Buhârî, Libâs, 24; Müslim, Îmân, 154.</b> Buhârî (Ebû Abdillah) ekler: “Bu, ölüm anında veya öncesinde <b>tevbe edip pişman olarak</b> ‘Lâ ilâhe illallâh’ dediğinde olur; ona mağfiret edilir.”",
            ),
        ])
        .add_table(ComparisonTable(
            "Kebîre Meselesi — Fırkaların Konumu (Aynî'nin Şerhi)",
            ["Fırka", "Büyük günah işleyen mü'min hakkında görüşü"],
            [
                ["<b>Hâricîler</b>", "<b>Kâfir olur</b> — dinden çıkar"],
                ["<b>Mu'tezile</b>", "Ne mü'min ne kâfir; ateşte <b>ebedî kalır</b>"],
                ["<b>Mürcie</b>", "İmanla birlikte günah <b>zarar vermez</b>; ateşe girmez"],
                ["<b>Ehl-i Sünnet</b>", "Ateşe girmesi <b>kesin değildir</b>; girse bile <b>çıkarılır</b>, ebedî kalmaz"],
            ],
        ))
    )
    ch7.pages.append(
        ChapterPage()
        .add_callout(Callout(
            "insight", "İman 9 ↔ İman 23: Görünen Çelişki Nasıl Çözülür?",
            "İman 9 “zinâ eden mü'min olarak zinâ etmez” der; İman 23 ise “zinâ etse de cennete girer” der. Cem': "
            "İman 9'da nefyedilen <b>kemâl-i imandır</b> (nefyü'l-kemâl), İman 23'te ispat edilen ise "
            "<b>aslü'l-îmândır</b>. Ayrıca Aynî, hadiste iki tür kebîrenin özellikle seçildiğini söyler: "
            "<b>zinâ</b> ile <u>Allah hakkına</u>, <b>hırsızlık</b> ile <u>kul hakkına</u> işaret edilmiştir."
        ))
        .add_person(EBU_ZERR)
        .add_summary(
            "Bölüm, Allah'a imanı üç halkada tamamlar: sözleşme (biat ve had-keffâret ilkesi), "
            "davet (tevhid → namaz → zekât sıralaması) ve sınır (yedi mûbika, mûcibetân). "
            "Son rivayet ise tevhidin, en ağır günahlar karşısında bile nihaî kurtuluş zemini "
            "olduğunu — ama bunun cezasızlık anlamına gelmediğini — gösterir."
        )
    )

    chapters = [ch1, ch2, ch3, ch4, ch5, ch6, ch7]

    # =======================================================================
    # KAVRAMLAR SÖZLÜĞÜ
    # =======================================================================
    glossary = [
        Concept("Metûnü'l-Hadîs", "Hadis metinleri derlemesi; senediyle birlikte verilen rivayetler, Arapça şerh alıntıları ve usûl dipnotlarından oluşan ders kitabı türü.", "Ders kaynağı", 1),
        Concept("Kitâb", "Hadis eserlerinde ana bölüm. Kitâbü'l-İlm, Kitâbü'l-Îmân gibi.", "Tasnif terimi", 1),
        Concept("Bâb", "Bir eserde ana bölümden (kitâbdan) sonra gelen alt bölüm.", "Tasnif terimi", 1),
        Concept("Terceme", "Kitaplardaki ana bölüm (kitâb) ve alt bölüm (bâb) başlığına verilen isim.", "Tasnif terimi", 1),
        Concept("Mevkūf", "Senedi sahâbîde duran rivayet; Hz. Peygamber'e değil bir sahâbîye nispet edilir. Örnek: Hz. Ali'nin “halka anlayacaklarını anlatın” sözü.", "İlim 23", 1),
        Concept("Muallak (Ta'lîk)", "Senedin baş tarafı hazfedilerek “وقال فلان” kalıbıyla nakledilen rivayet.", "İlim 23", 1),
        Concept("Te'essüm", "Günaha girme korkusu; Muâz'ın hadisi vefatı sırasında açıklamasının gerekçesi.", "İlim 24", 1),
        Concept("Tevkīr–İclâl", "Saygı ve ta'zim. Bu kaynaktan doğan hayâ övülür; ilim talebine engel olan hayâ ise kötülenir.", "İlim 25–26", 1),
        Concept("Mezî", "Şehvetle gelen ince akıntı; gusül gerektirmez, abdesti bozar. Menî ise gusül gerektirir.", "İlim 27", 1),
        Concept("Ref'u'l-ilm", "İlmin kaldırılması; kalplerden silinmesi değil, âlimlerin vefatıyla ortadan kalkması.", "İlim 28–29", 2),
        Concept("Kabz", "Alma/tutma. İlmin kabzı, âlimlerin vefat ettirilmesiyle gerçekleşir.", "İlim 29", 2),
        Concept("Nahvehu", "“Onun benzeri”; metnin bir öncekinin lafzen aynısı değil benzeri olduğunu gösterir.", "İlim 29", 2),
        Concept("Mislehu", "“Onun aynısı”; metnin bir öncekinin lafzen aynı olduğunu gösterir.", "İlim 29", 2),
        Concept("Firebrî nüshası", "Buhârî'nin öğrencisi Firebrî'ye ait nüsha; Yûnînî baskısının dayandığı ana koldur.", "İlim 29 dipnotu", 2),
        Concept("Yûnînî nüshası", "Firebrî'ye ait önemli nüshaların karşılaştırılmasıyla oluşan ve Abdülhamit Han tarafından bastırılan matbu Buhârî.", "İlim 29 dipnotu", 2),
        Concept("Îmân", "Kalbin tasdiki; Cibrîl hadisinde Allah, melekler, Kitap, likā', resuller ve ba's ile tarif edilir.", "İman 1", 3),
        Concept("İslâm", "Dinin amelî katmanı; Cibrîl hadisinde dört, “büniye'l-İslâm” hadisinde beş rükünle sayılır.", "İman 1–2", 3),
        Concept("İhsan", "“Allah'ı görüyormuşçasına kulluk”; kulluğun murâkabe mertebesi.", "İman 1", 3),
        Concept("Likāullah", "Allah'a kavuşma. Cibrîl hadisinin bu rivayetinde iman esasları arasında sayılır; kader ise burada zikredilmez.", "İman 1", 3),
        Concept("Mugayyebât-ı hamse", "Yalnız Allah'ın bildiği beş şey; Cibrîl hadisinde Lokmân 31/34 ile delillendirilir.", "İman 1", 3),
        Concept("Eşrâtu's-sâa", "Kıyamet alâmetleri; cariyenin efendisini doğurması, çıplak-yalınayakların baş olması, çobanların bina yarışı.", "İman 1", 3),
        Concept("Nefyü'l-kemâl", "“لا يؤمن أحدكم حتى…” kalıbında nefyedilenin imanın aslı değil kemâli olması. Nevevî bunu muhakkiklerin sahih görüşü sayar.", "İman 3–4, 9", 4),
        Concept("Halâvetü'l-îmân", "İmanın tadı; üç haslette bulunur (muhabbetullah, hubb fillâh, küfürden nefret).", "İman 5", 4),
        Concept("Şuabü'l-îmân", "İmanın şubeleri; “bid'un ve sittûn” = altmış küsur şube.", "İman 6", 4),
        Concept("Bid'", "Arapçada 3–9 arası belirsiz sayı; “bid'un ve sittûn” bu yüzden “altmış küsur” demektir.", "İman 6", 4),
        Concept("Tahvîl hâ'sı (ح)", "Senedde bir hadisin birden çok senedle geldiğini, râvinin bir senedden diğerine geçtiğini gösteren işaret.", "İman 3–4, 11", 4),
        Concept("Tefâdul", "Derece farkı; iman ehlinin amelde birbirinden üstün olması.", "İman 7", 4),
        Concept("Mürcie", "“Amel imandan bir cüz değildir; imanla birlikte günah zarar vermez” diyen fırka.", "İman 7, 10", 4),
        Concept("Mu'tezile", "Büyük günah işleyenin ateşte ebedî kalacağını savunan fırka; “hardal tanesi” hadisi buna karşı delildir.", "İman 7, 23", 4),
        Concept("Nifâk-ı amelî", "Kişiyi dinden çıkarmayan, kâmil imana aykırı davranış nifakı; münafığın dört alâmeti bu kapsamdadır.", "İman 8", 5),
        Concept("Füsûk", "Sözlükte “çıkmak”; şer'an Allah ve Resûlüne itaatten çıkmak.", "İman 10", 5),
        Concept("Küfr-i lugavî", "Sözlük anlamıyla küfür, yani “örtmek”. “Kıtâlühû küfr” ifadesinin izahlarından biridir.", "İman 10", 5),
        Concept("Mütâbaat", "Bir hadisin, farklı bir râvi tarafından aynı senedle desteklenmesi.", "İman 8", 5),
        Concept("Mütâbi'", "Destekleyici rivayeti yapan râvi.", "İman 8", 5),
        Concept("Mütâbâ' aleyh", "Kendisine mütâbaat edilen râvi ya da hadis.", "İman 8", 5),
        Concept("Şâhid", "Aynı veya başka bir sahâbîden gelen benzer muhtevalı ikinci hadis.", "İman 8", 5),
        Concept("Âdıd", "Bir hadisi destekleyen, kusurlu bir haberin kusurunu gideren ikinci haber.", "İman 8", 5),
        Concept("Müsbil", "Elbisesini kibirle yerlerde sürüyen kimse; kıyamette Allah'ın konuşmayacağı üç kişiden biri.", "İman 12", 5),
        Concept("Mennân", "Verdiğini başa kakan kimse.", "İman 12", 5),
        Concept("Efdalü'l-a'mâl", "Amellerin en faziletlisi; farklı rivayetlerde farklı cevaplar verildiği için cem' gerektirir.", "İman 13–16", 6),
        Concept("Cem' ve te'lîf", "Görünüşte çelişen rivayetleri uzlaştırma yöntemi; Kaffâl iki vecih sunar.", "İman 16", 6),
        Concept("İhtilâfü'l-hadîs", "Rivayetler arasında görünen uyuşmazlık; cem', tercih ya da nesih ile çözülür.", "İman 16", 6),
        Concept("Hacc-ı mebrûr", "Makbul hac; içine günah ve riya karışmamış hac.", "İman 16", 6),
        Concept("İr'â'", "Acıyıp esirgeme; İbn Mes'ûd'un soru sormayı bırakma gerekçesi.", "İman 15", 6),
        Concept("Biat", "Bağlılık sözleşmesi; Ubâde rivayetinde altı yasak üzerine yapılır.", "İman 17", 7),
        Concept("Setr", "Allah'ın kulun günahını örtmesi; örtülen günahın hükmü Allah'a kalır.", "İman 17", 7),
        Concept("Keffâret", "Örtücü ceza; dünyada uygulanan had, o günahın keffâreti sayılır.", "İman 17", 7),
        Concept("Seb'u'l-mûbikāt", "Yedi helâk edici büyük günah.", "İman 21", 7),
        Concept("Kazf", "İffetli, mü'mine ve habersiz kadınlara zinâ iftirası atmak; yedi mûbikadan biridir.", "İman 21", 7),
        Concept("Tevellî yevme'z-zahf", "Savaş günü düşmandan kaçmak; yedi mûbikadan biridir.", "İman 21", 7),
        Concept("Mûcibetân", "“İki gerektirici”: şirksiz ölmek cenneti, şirkle ölmek cehennemi gerektirir.", "İman 22", 7),
        Concept("Kebîre", "Büyük günah; sahibinin âkıbeti Hâricî, Mu'tezilî, Mürciî ve Sünnî fırkalar arasındaki ana tartışma konusudur.", "İman 23", 7),
        Concept("Aslü'l-îmân", "İmanın aslı/temeli; kemâl-i imandan ayrılır. İman 23 aslı, İman 9 kemâli konu edinir.", "İman 9 ↔ 23", 7),
    ]

    # =======================================================================
    # TEST
    # =======================================================================
    test_questions = [
        TestQuestion(1, "Hz. Ali'nin “İnsanlara bildikleri şeyleri anlatın; Allah ve Resûlü'nün yalanlanmasını ister misiniz?” sözü, rivayet türü bakımından ne olarak nitelenir?", {
            "A": "Merfû", "B": "Mevkūf", "C": "Maktû'", "D": "Kudsî", "E": "Mütevâtir"}),
        TestQuestion(2, "Muâz b. Cebel'e söylenen “Lâ ilâhe illallâh” müjdesiyle ilgili olarak Hz. Peygamber'in “إذا يتكلوا” demesinin sebebi aşağıdakilerden hangisidir?", {
            "A": "Hadisin sahih olmaması", "B": "Muâz'ın bunu anlayamayacak olması",
            "C": "İnsanların buna güvenip amelden geri kalma ihtimali", "D": "Müjdenin sadece Muâz'a özel olması",
            "E": "Bilginin henüz tamamlanmamış olması"}),
        TestQuestion(3, "Muâz'ın bu hadisi ancak ölümü sırasında haber vermesi “تأثما” (te'essümen) ile açıklanır. Bu kelime ne anlama gelir?", {
            "A": "Sevap kazanma ümidiyle", "B": "İlmi gizlemenin günahından korkarak",
            "C": "Vasiyet olarak", "D": "Unutmuş olma ihtimaline karşı", "E": "İcazet vermek için"}),
        TestQuestion(4, "İbn Battâl'ın şerhine göre Buhârî'nin “el-Hayâ fi'l-ilm” bâbıyla göstermek istediği temel ayrım hangisidir?", {
            "A": "Kadın ve erkeğin soru sorma biçimi farkı",
            "B": "İlim talebine engel olan hayânın kötülenmesi, ta'zim kaynaklı hayânın övülmesi",
            "C": "Hayânın imandan bir şube olmadığı", "D": "Hayânın yalnızca kadınlara özgü olduğu",
            "E": "Soru sormanın edebe aykırı sayıldığı"}),
        TestQuestion(5, "Hz. Ali'nin mezî meselesini Mikdâd b. Esved aracılığıyla sordurması ve alınan cevap hangisidir?", {
            "A": "Gusül gerekir", "B": "Hiçbir şey gerekmez", "C": "Abdest gerekir",
            "D": "Sadece elbise yıkanır", "E": "Oruç bozulur"}),
        TestQuestion(6, "“İlmin kaldırılması” (ref'u'l-ilm) hadisinde Aynî'ye göre bu kaldırma nasıl gerçekleşir?", {
            "A": "İlmin insanların hafızalarından silinmesiyle", "B": "Kitapların yok olmasıyla",
            "C": "Âlimlerin vefat ettirilmesiyle", "D": "Vahyin kesilmesiyle", "E": "Fitnelerin çoğalmasıyla"}),
        TestQuestion(7, "Senedin sonunda metin zikredilmeksizin kullanılan ve metnin bir öncekinin lafzen aynısı DEĞİL benzeri olduğunu bildiren tabir hangisidir?", {
            "A": "Mislehu", "B": "Nahvehu", "C": "Tâbeahû", "D": "Ravâhu", "E": "Ahracehû"}),
        TestQuestion(8, "Cibrîl hadisinde (Müslim, Îmân, 5) İSLÂM tarif edilirken aşağıdakilerden hangisi ZİKREDİLMEZ?", {
            "A": "Şirksiz kulluk", "B": "Farz namaz", "C": "Farz zekât", "D": "Ramazan orucu", "E": "Hac"}),
        TestQuestion(9, "Cibrîl hadisinin bu rivayetinde iman esasları sayılırken “kader” yerine hangisi zikredilmiştir?", {
            "A": "Likāullah (Allah'a kavuşma)", "B": "Cennet ve cehennem", "C": "Şefaat",
            "D": "Kitâbet", "E": "Mîzân"}),
        TestQuestion(10, "“İhsan” Cibrîl hadisinde nasıl tarif edilmiştir?", {
            "A": "Farzları eksiksiz yerine getirmek", "B": "Allah'ı görüyormuşçasına kulluk etmek",
            "C": "İnsanlara iyilik yapmak", "D": "Nafile ibadetleri çoğaltmak", "E": "Sabır ve şükür"}),
        TestQuestion(11, "“Sizden biriniz, kendisi için istediğini kardeşi için istemedikçe iman etmiş olmaz” hadisinde nefyedilen nedir?", {
            "A": "İmanın aslı", "B": "İmanın kemâli", "C": "İslâm'ın rükünleri",
            "D": "Amelin geçerliliği", "E": "Namazın sıhhati"}),
        TestQuestion(12, "İmanın şubeleriyle ilgili hadiste “en aşağı” (ednâhâ) mertebe olarak zikredilen nedir?", {
            "A": "Lâ ilâhe illallâh sözü", "B": "Hayâ", "C": "Yoldan eziyet veren şeyi kaldırmak",
            "D": "Selam vermek", "E": "Yemek yedirmek"}),
        TestQuestion(13, "Aynî'ye göre “kalbinde hardal tanesi kadar iman bulunanların ateşten çıkarılması” hadisi hangi fırkanın “âsi ateşe girmez” görüşüne karşı delildir?", {
            "A": "Hâricîler", "B": "Mürcie", "C": "Cebriyye", "D": "Kaderiyye", "E": "Bâtıniyye"}),
        TestQuestion(14, "Münafığın dört alâmetini bildiren hadiste aşağıdakilerden hangisi YER ALMAZ?", {
            "A": "Emanete hıyanet etmek", "B": "Konuştuğunda yalan söylemek",
            "C": "Söz verdiğinde sözünden dönmek", "D": "Namazı terk etmek",
            "E": "Düşmanlık ettiğinde haddi aşmak"}),
        TestQuestion(15, "İbn Hacer'e göre “Müslümanla savaşmak küfürdür” ifadesinde “küfür” ile kastedilen ne DEĞİLDİR?", {
            "A": "Sakındırmada mübalağa", "B": "Kâfirin işine benzetme",
            "C": "Lugavî küfür, yani örtmek", "D": "Kişiyi milletten çıkaran hakiki küfür",
            "E": "Hakkı örtbas etme anlamı"}),
        TestQuestion(16, "“Üç kişi vardır ki Allah kıyamet günü onlarla konuşmaz…” hadisinde sayılanlar hangileridir?", {
            "A": "Müsbil, mennân, yalan yeminle mal satan", "B": "Yalancı, hırsız, zâni",
            "C": "Sihirbaz, faizci, yetim malı yiyen", "D": "Münafık, kâfir, müşrik",
            "E": "Gıybetçi, nemmâm, müfterî"}),
        TestQuestion(17, "Kaffâl el-Kebîr'in “en faziletli amel” rivayetlerini uzlaştırmak için sunduğu iki vecihten biri, ifadede hangi edatın takdir edilmesidir?", {
            "A": "إلا", "B": "من", "C": "حتى", "D": "لكن", "E": "أو"}),
        TestQuestion(18, "Ubâde b. es-Sâmit'in rivayet ettiği biat hadisine göre, biat edilen bir yasağı çiğneyip DÜNYADA cezalandırılan kimse için bu ceza nedir?", {
            "A": "Sadece dünyevi bir yaptırımdır, âhirete etkisi yoktur",
            "B": "Onun için keffârettir", "C": "Tevbe şartına bağlıdır",
            "D": "Şefaatle kaldırılır", "E": "Cezanın iki katı olarak âhirette de uygulanır"}),
        TestQuestion(19, "Hz. Peygamber'in Muâz'ı Yemen'e gönderirken emrettiği davet sıralaması hangisidir?", {
            "A": "Namaz → zekât → şehâdet", "B": "Şehâdet → zekât → namaz",
            "C": "Şehâdet → namaz → zekât", "D": "Zekât → şehâdet → namaz",
            "E": "Namaz → şehâdet → oruç"}),
        TestQuestion(20, "Aynî'ye göre Ebû Zerr hadisinde büyük günahlardan özellikle “zinâ” ve “hırsızlık”ın seçilmesinin sebebi nedir?", {
            "A": "Cahiliyede en yaygın günahlar olmaları",
            "B": "Biri Allah hakkına, diğeri kul hakkına işaret ettiği için",
            "C": "Had cezası gerektiren tek günahlar olmaları",
            "D": "Ebû Zerr'in bunları özellikle sorması",
            "E": "Diğer günahların affedilmemesi"}),
    ]

    answer_key_items = [
        AnswerItem(1, "B", "Söz Hz. Peygamber'e değil <b>sahâbî</b> olan Hz. Ali'ye nispet edildiği için <b>mevkūf</b>tur; ayrıca senedi hazfedilip “وقال علي” kalıbıyla verildiği için <b>muallak</b>tır."),
        AnswerItem(2, "C", "İbn Hacer'in izahına göre <b>“izen yettekilû”</b> = “buna dayanıp amelden geri kalırlar”. Müjde, ameli terk etme gerekçesine dönüşmesin diye yayılması geciktirilmiştir."),
        AnswerItem(3, "B", "<b>Te'essüm</b>, günaha girme korkusudur. İbnü'l-Esîr: “bu ilmi <b>gizlemenin günahından</b> korkarak”. Bilgi geciktirilebilir ama tümüyle gizlenemez."),
        AnswerItem(4, "B", "İbn Battâl: ilim talebine engel olan hayâ <b>mezmûm</b>dur (İbn Ömer'in susması); <b>tevkīr-iclâl</b> kaynaklı hayâ ise güzeldir (Ümmü Seleme'nin yüzünü örtmesi)."),
        AnswerItem(5, "C", "Cevap “<b>fîhi'l-vudû'</b>” yani <b>abdest gerekir</b>. Mezî gusül gerektirmez; menî ise gusül gerektirir (krş. İlim 25: “إذا رأت الماء”)."),
        AnswerItem(6, "C", "Hadis kendini açıklar: Allah ilmi kullardan çekip almaz, <b>âlimleri kabzederek</b> (vefat ettirerek) alır. Aynî: bu, ilmin göğüslerden silinmesi değildir."),
        AnswerItem(7, "B", "<b>Nahvehu</b> (نحوه) = benzeri; lafızlar arasında az da olsa fark vardır. <b>Mislehu</b> (مثله) ise lafzen <b>aynı</b> olduğunu gösterir."),
        AnswerItem(8, "E", "Cibrîl hadisinin bu rivayetinde İslâm <b>dört</b> rükünle sayılır ve <b>hac zikredilmez</b>. Hac, “büniye'l-İslâmü alâ hams” hadisinde (İman 2) geçer."),
        AnswerItem(9, "A", "Bu rivayette iman esasları: Allah, melekler, Kitap, <b>likā'</b> (O'na kavuşma), resuller ve ba's. <b>Kader burada zikredilmez</b>; ayrı bir bâbda işlenir."),
        AnswerItem(10, "B", "“<b>En ta'büdallâhe keenneke terâhu, fe-inneke in lâ terâhu fe-innehû yerâk</b>” — kulluğun <b>murâkabe</b> mertebesi."),
        AnswerItem(11, "B", "Nevevî: “Muhakkiklerin söylediği sahih görüş, bunun <b>kâmil iman sahibi olarak</b> yapmaz anlamına geldiğidir.” Nefyedilen <b>kemâldir</b>, asıl değil."),
        AnswerItem(12, "C", "En üstü (<b>efdalühâ</b>) “Lâ ilâhe illallâh” sözü, en aşağısı (<b>ednâhâ</b>) <b>yoldan eziyeti kaldırmak</b>tır; hayâ ise şubelerden biri olarak ayrıca zikredilir."),
        AnswerItem(13, "B", "<b>Mürcie</b>, “imanla birlikte günah zarar vermez, âsi ateşe girmez” der. Hadis, âsi mü'minlerden bir kısmının ateşe gireceğini gösterdiği için buna karşı delildir."),
        AnswerItem(14, "D", "Dört alâmet: <b>hıyanet, yalan, sözden dönme, husûmette haddi aşma</b>. Namazı terk etmek bu hadiste yer almaz."),
        AnswerItem(15, "D", "İbn Hacer, buradaki küfrün <b>milletten çıkaran hakiki küfür OLMADIĞINI</b> söyler; mübalağa, benzetme veya lugavî küfür (örtmek) olarak açıklanır."),
        AnswerItem(16, "A", "<b>el-Müsbil</b> (elbisesini kibirle sürüyen), <b>el-mennân</b> (verdiğini başa kakan) ve <b>malını yalan yeminle pazarlayan</b> (Müslim, Îmân, 171)."),
        AnswerItem(17, "B", "Kaffâl'in ikinci vechi: ifadede “<b>مِنْ</b>” takdir edilir; yani “amellerin <b>en faziletlilerinden biri</b>”. Birinci vecih ise hâllerin/şahısların farklılığıdır."),
        AnswerItem(18, "B", "“<b>Fe-huve keffâretün leh</b>” — dünyada uygulanan ceza o günahın <b>keffâreti</b>dir. Örtülen (setr edilen) günahın hükmü ise Allah'a kalmıştır."),
        AnswerItem(19, "C", "Tedrîcî davet: önce <b>şehâdet</b>, itaat ederlerse <b>beş vakit namaz</b>, ona da itaat ederlerse <b>zekât</b> (zenginden alınıp fakire verilir)."),
        AnswerItem(20, "B", "Aynî: günah ya <b>Allah hakkı</b>dır — buna <b>zinâ</b> ile işaret edilmiştir — ya da <b>kul hakkı</b>dır — buna <b>hırsızlık</b> ile işaret edilmiştir."),
    ]

    return CoursePack(
        ders_klasoru="HADİS",
        course_code="HADİS",
        title='Hadis <span class="accent-word">Metinleri</span>',
        subtitle="Kitâbü'l-İlm 23–29 · Kitâbü'l-Îmân 1–23 — Final Özeti",
        description=(
            "Metûnü'l-Hadîs'in sorumlu olunan otuz rivayetini; ilmin tebliği ve ilimde hayâdan başlayıp "
            "ilmin kaldırılmasına, oradan Cibrîl hadisiyle açılan iman-İslâm-ihsan tasnifine, kâmil imana "
            "aykırı davranışlara ve büyük günah tartışmasına uzanan bir çizgide; her rivayette orijinal "
            "Arapça metin, tercüme ve klasik şerh notuyla sunan nokta atışı bir final yol haritası."
        ),
        theme="forest",
        theme_color="#8E3B1F",
        icon_text="H",
        chapters=chapters,
        glossary=glossary,
        persons=PERSONS,
        test_title="Genel Değerlendirme Testi",
        test_subtitle="Kitâbü'l-İlm 23–29 ve Kitâbü'l-Îmân 1–23 üzerine kapsamlı çoktan seçmeli test",
        test_instructions="Aşağıdaki sorularda beş seçenekten yalnızca birini işaretleyiniz. Süre: 30 dakika.",
        test_questions=test_questions,
        answer_key_intro="Her sorunun doğru cevabı, dayandığı rivayet ve şerh gerekçesiyle birlikte aşağıda verilmiştir.",
        answer_key_items=answer_key_items,
        overview_lead=(
            "Bu ders notu, <b>Metûnü'l-Hadîs</b>'in sorumlu olunan kısmını — <b>Kitâbü'l-İlm 23–29</b> ve "
            "<b>Kitâbü'l-Îmân 1–23</b>, toplam <b>30 rivayet</b> — yedi bölümde işler. Her rivayet önce "
            "<b>orijinal Arapça metniyle</b>, ardından <b>Türkçe tercümesiyle</b> ve altında <b>kaynak "
            "künyesi + klasik şerh notuyla</b> verilir; senedler kısaltılıp son râvi ve metin öne çıkarılmıştır."
        ),
        overview_cards=[
            {"title": "İlmin Tebliği ve Hayâ", "text": "Muhatabın seviyesi, ilmi gizlemenin günahı ve hayânın kötülenen/övülen iki yüzü."},
            {"title": "Ref'u'l-İlm", "text": "İlmin âlimlerin vefatıyla kabzedilmesi, câhil reisler ve ilimsiz fetva zinciri."},
            {"title": "İman–İslâm–İhsan", "text": "Cibrîl hadisi ile “büniye'l-İslâm” hadisinin rükün farkı: hac ve kader nerede?"},
            {"title": "Alâmet, Tat ve Şubeler", "text": "Nefyü'l-kemâl kaidesi, üç haslet, altmış küsur şube ve amelde derece farkı."},
            {"title": "Kâmil İmana Aykırılık", "text": "Amelî nifak, mecazi küfür, “bizden değildir” ve mütâbaat kavram ailesi."},
            {"title": "Biat, Davet ve Kebâir", "text": "Had-keffâret ilkesi, tedrîcî davet sıralaması, yedi mûbika ve kebîre tartışması."},
        ],
        overview_flow=[
            ("Arapça Metin", "Onarılmış orijinal lafız"),
            ("Tercüme", "Akademik Türkçe karşılık"),
            ("Kaynak", "Buhârî/Müslim künyesi"),
            ("Şerh", "Aynî · İbn Hacer · Nevevî"),
            ("Sınav Notu", "Karşılaştırma ve tuzak"),
        ],
        overview_note=(
            "Sınavda en çok karıştırılan iki nokta: <b>(1)</b> <u>Cibrîl hadisi</u> ile <u>“büniye'l-İslâm”</u> "
            "hadisinin farkı — birincisinde <b>hac yoktur</b> ve iman esasları arasında <b>kader yerine likā'</b> "
            "sayılır; <b>(2)</b> <u>İman 9</u> (“zinâ eden mü'min olarak zinâ etmez”) ile <u>İman 23</u> "
            "(“zinâ etse de cennete girer”) çelişkisi — birincisinde <b>kemâl</b>, ikincisinde <b>asıl</b> "
            "söz konusudur."
        ),
    )
