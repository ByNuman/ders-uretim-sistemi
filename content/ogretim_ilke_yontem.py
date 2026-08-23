# -*- coding: utf-8 -*-
"""ÖĞRETİM İLKE VE YÖNTEMLERİ — Görsel Ders Notu Kitabı, içerik tanımı.
Kaynak: 'ÖĞRETİM İLKE VE YÖNTEMLERİ_FİNAL ÖZET.pdf' (16 sayfa, 6 bölümlük
kendi fihristini taşıyan final özet — öğrenme/öğretme kuram ve modellerinden
öğretim yöntem, teknik ve düşünme biçimlerine).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from content_model import (
    Person, KeyTerm, Callout, FlowStep, FlowDiagram, ComparisonTable,
    InfoCard, BulletBlock, Chapter, ChapterPage, Concept, CoursePack,
    QAItem, DistinctionPair, MatchRow, TestQuestion, AnswerItem,
)


def get_pack() -> CoursePack:

    # =====================================================================
    # BÖLÜM 1 — Öğrenme-Öğretme Kuram ve Modelleri I
    # =====================================================================
    ch1 = Chapter(
        number=1,
        title="Öğrenme-Öğretme Kuram ve Modelleri I",
        subtitle="Tam Öğrenme'den Programlı Öğrenme'ye, Probleme Dayalı Öğrenmeden Yapılandırmacılığa",
        key_terms=[
            KeyTerm("Tam Öğrenme", "Olumlu öğrenme koşulları sağlanırsa herhangi birinin öğrenebileceğini herkesin öğrenebileceğini savunan, grupla öğretim modeli (Bloom)."),
            KeyTerm("Programlı Öğrenme", "Edimsel koşullanma ilkelerine dayanan, öğretimin bireyselleştirildiği, herkesin kendi hızında ilerlediği sistem (Skinner)."),
            KeyTerm("Probleme Dayalı Öğrenme", "İlgi ve merak uyandıran bir problemle başlanan, öğrencinin süreci baştan sona yönettiği öğrenci merkezli yaklaşım (Dewey)."),
            KeyTerm("Yapılandırmacılık", "Bilginin nesnel değil, bireyin kendi deneyimleriyle öznel olarak inşa ettiği bir şey olduğunu savunan kuram."),
        ],
    )
    ch1.pages.append(
        ChapterPage()
        .add_terms(ch1.key_terms)
        .add_block(BulletBlock(1, "Tam Öğrenme Modeli (B. Bloom)", [
            "<b>'Tam öğrenme modeline göre işin başında olumlu öğrenme koşulları sağlanmış ise herhangi bir kişinin öğrenebileceği bir şeyi herkes öğrenebilir.'</b>",
            "Bloom'un bu modeli, okuldaki başarıyı %90'a çıkaran (alt limit %70) <b>grupla öğretim</b> sürecidir. Öğrenciye ihtiyacı kadar zaman verilir ve konular küçük birimlere (ünitelere) ayrılır; bir birim öğrenilmeden diğerine geçilmez.",
            "<b>Öğrenmeyi Etkileyen Değişkenler:</b> süreç temelde Öğrenci Nitelikleri, Öğretim Hizmeti ve Öğrenme Ürünleri olarak işler. Öğrenci nitelikleri ikiye ayrılır: <b>Bilişsel Giriş Davranışları (%50 Etkili)</b> — bilişsel alan düzeyi, hazırbulunuşluk ve öğrenme stilleri (örn: çarpma için toplamayı bilmek); <b>Duyuşsal Giriş Özellikleri (%25 Etkili)</b> — derse, öğretmene, okula karşı tutumlar, ilgi ve özgüven.",
            "<b>Öğretim Hizmetinin Niteliği (ÖÇFRE):</b> öğretim hizmeti Pekiştirme, İpucu, Dönüt ve Düzeltme, Etkin Katılım unsurlarından oluşur.",
        ]))
    )
    ch1.pages.append(
        ChapterPage()
        .add_callout(Callout("caution", "Dikkat / Püf Noktası",
            "Tam öğrenme oldukça zaman alıcıdır ve bireysel farklar ihmal edilir. En büyük sınırlılığı, "
            "yavaş öğrenenlerin hızlı öğrenenleri engellemesi ve onları bekletmesidir. Ayrıca süreçte "
            "öğrenci-öğrenci etkileşimi yoktur; bu yüzden işbirlikli öğrenme ve tartışma gibi teknikler "
            "kullanılamaz."))
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "Zeka, kişilik, yetenek gibi faktörler değiştirilemeyen faktörlerken; zaman, ortam, "
            "bilişsel/duyuşsal özellikler değiştirilebilir faktörlerdir."))
        .add_block(BulletBlock(2, "Programlı Öğrenme (B.F. Skinner)", [
            "Davranışçı kuramın edimsel koşullanma ilkelerine (Skinner) dayanan, öğretimin bireyselleştirildiği "
            "sistemdir. En önemli özelliği, bireysel farklılıkları dikkate almasıdır; herkes kendi potansiyeline "
            "göre ilerler.",
            "<b>Programlı Öğrenme İlkeleri (KEBAB):</b> <b>K</b>üçük Adımlar (konuların anlamlı, küçük parçalara "
            "bölünmesi), <b>E</b>tkin Katılım (öğrencinin sürece bizzat dahil olması), <b>B</b>aşarı (başarı "
            "durumunda pekiştireç kullanılması ve bir birim bitmeden diğerine geçilmemesi), <b>A</b>nında "
            "Düzeltme (hatanın anında düzeltilerek en aza indirgenmesi), <b>B</b>ireysel Hız (her öğrenciye "
            "kendi hızında ilerleme fırsatı verilmesi — Tam Öğrenmeden ayıran en belirgin fark).",
        ]))
    )
    ch1.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Karşılaştırma: Tam Öğrenme vs. Programlı Öğrenme",
            ["Özellik", "Tam Öğrenme (Bloom)", "Programlı Öğretim (Skinner)"],
            [
                ["Süreç Türü", "Grupla öğretim", "Bireysel öğrenme"],
                ["Parçalara Bölme", "Konular ünitelere ayrılır", "Üniteler çok daha küçük parçalara ayrılır (küçük adımlar)"],
                ["Dönüt / Düzeltme", "Ünite sonlarındaki izleme testleriyle", "Her bir küçük adımın sonunda anında"],
                ["Hız Faktörü", "Hızlı öğrenenler, yavaşları beklemek zorundadır", "Herkes kendi hızında ilerler (at yarışı gibidir)"],
                ["Bireysel Farklar", "Ortadan kaldırır (deve kervanı gibidir)", "Daha belirginleştirir (arttırır)"],
            ]
        ))
        .add_block(BulletBlock(3, "Probleme Dayalı Öğrenme (J. Dewey)", [
            "İlerlemecilik eğitim felsefesinin savunucusu John Dewey ve Piaget'in yapısalcı çalışmaları "
            "doğrultusunda ortaya çıkmıştır. Problemin ilgi ve merak uyandırıcı olması en önemli önkoşuldur; "
            "Piaget'ye göre bu <b>'şaşkınlık ortamı'</b> öğrenmeyi tetikler ve güdülenmeyi (motivasyonu) artırır.",
            "Öğretime bir problem ile başlanır ve öğrencinin dünyasıyla bağlantı kurulur; problem disiplinler "
            "üzerinde değil, yalnızca konu üzerinde organize edilir.",
            "Öğretmen organize eden kişidir (rehber); konuyu ve kaynak materyalleri öğrenciyle bulur. "
            "Öğrenciler problemi baştan sona yönetmede tam yetkilidir.",
            "<b>Aşamaları:</b> Problemi Hissetme → Problemi Tanımlama → Bilgi Toplama → Hipotez Üretme → "
            "Veri Toplama → Hipotezleri Test Etme → Sonuca Ulaşma.",
        ]))
    )
    ch1.pages.append(
        ChapterPage()
        .add_block(BulletBlock(4, "Proje Tabanlı Öğrenme", [
            "Birden fazla disiplinin (dersin) öğrenme hedeflerini kapsayan, eğitim programının küçük bilgiler "
            "yığını olarak öğretilmesine karşı çıkan çağdaş bir modeldir.",
            "Esnek yapılı bir senaryo etrafında, küçük gruplarda işbirlikli öğrenmeyi temel alır; öğrenci "
            "yaratıcılık, bilgiye erişim ve yeniden harmanlama gibi üst düzey bilişsel aktiviteler yapar.",
            "Öğretmen danışman/yönlendiricidir; kaynakları ve konuyu öğrencilerin kendisi bulur. Teknoloji ve "
            "bilgisayar hedef değil, yalnızca bir araç olarak görülür. Sürecin sonunda ortaya somut ve "
            "gerçekçi bir ürün (ürün/rapor) konur.",
        ]))
        .add_callout(Callout("caution", "Dikkat / Püf Noktası — Proje Tabanlı ile Probleme Dayalı Öğrenme Farkı",
            "Proje tabanlı öğrenme, öğrenmenin ürün boyutundan çok süreç boyutu üzerinde durur, ancak "
            "sürecin ayrılmaz bir parçası olarak mutlaka somut bir sonuç/ürün de hedeflenir. Probleme dayalı "
            "öğrenmede ise somut ürün yoktur, sadece problemi çözme (süreç) önemlidir."))
        .add_block(BulletBlock(5, "Yapılandırmacılık", [
            "Öğrencinin belli bir konuda kendi anlayışını yaratmak için kendi deneyimlerini kullandığı, "
            "öğretimden çok 'bilgiyi öğrenmeyle' ilgili olan kuramdır. Bilgi nesnel değildir; bireylerin "
            "yarattığı şekilde var olur, yani sübjektif ve bireyseldir.",
            "Piaget'in zihinsel gelişim kuramı üzerine kuruludur ve öğretmenin 'öğreten' değil, öğrencilerin "
            "'öğrenmelerini sağlayan (rehber)' olduğu düşüncesi hakimdir. Evrensel mutlak gerçekler yoktur; "
            "bilgi işleyen hipotezlerdir. Daha çok Birincil Bilgi Kaynakları (öğrencinin kendi yaşantısıyla "
            "elde ettiği gözlem ve deneyimler) kullanılır.",
        ]))
    )
    ch1.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Yapılandırmacı Yaklaşım Türleri",
            ["Tür", "Açıklama"],
            [
                ["Bilişsel Yapılandırmacılık", "Bilginin oluşumunu Piaget'in özümleme, düzenleme ve denge ilkeleriyle açıklar."],
                ["Radikal Yapılandırmacılık", "Bilgi, doğru, gerçek gibi kavramların radikal değişimler geçirmesi gerektiğini savunur."],
                ["Sosyal Yapılandırmacılık", "Öğrenmede kültürün ve dilin büyük etkisi olduğunu, bilginin sosyal etkileşimle oluştuğunu savunur."],
                ["Eleştirel Yapılandırmacılık", "Bilginin oluştuğu çevreye eleştirel boyut katar; bireyin yapıyı oluşturma gerekçesini sorgular."],
            ]
        ))
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "Yapılandırmacılıkta program oldukça esnektir. Çünkü öğrencinin önceden var olan zihinsel "
            "yapılarıyla yeni bilgiyi nasıl anlamlandırıp yapılandıracağı baştan kesin olarak kestirilemez."))
        .add_summary("Bölüm 1, öğrenmeyi grup temelli ve zaman yoğun kılan Tam Öğrenme'den, bireysel hızı "
            "esas alan Programlı Öğrenme'ye; öğrenciyi problem çözme sürecinde tam yetkili kılan Probleme "
            "Dayalı Öğrenme'den, somut bir ürünle sonuçlanan Proje Tabanlı Öğrenme'ye ve bilginin öznel "
            "biçimde inşa edildiğini savunan Yapılandırmacılık'a uzanan beş temel kuram ve modeli ele alır.")
    )

    # =====================================================================
    # BÖLÜM 2 — Öğrenme-Öğretme Kuram ve Modelleri II
    # =====================================================================
    ch2 = Chapter(
        number=2,
        title="Öğrenme-Öğretme Kuram ve Modelleri II",
        subtitle="İşbirliğine Dayalı ve Aktif Öğrenmeden, Gagne'nin Öğretim Durumlarına ve Glasser'ın Modeline",
        key_terms=[
            KeyTerm("İşbirliğine Dayalı Öğrenme", "Öğrencilerin ortak bir hedef doğrultusunda heterojen küçük gruplar halinde birlikte çalıştığı model (Kubaşık/Kooperatif Öğrenme)."),
            KeyTerm("Aktif Öğrenme", "Öğrencinin dinlemekten çok derse katıldığı, öğrenme sürecinin sorumluluğunu taşıdığı süreç (Good)."),
            KeyTerm("Anlamlı Öğrenme", "Bireyin kavramlar arasındaki ilişkiyi fark etmesini içeren, kavram haritalarıyla desteklenen öğretmen merkezli öğrenme (Ausubel)."),
            KeyTerm("Öğretim Durumları Modeli", "8 aşamalı bir öğrenme türleri hiyerarşisi ve dersin işleniş sırasını tanımlayan model (Gagne)."),
        ],
    )
    ch2.pages.append(
        ChapterPage()
        .add_terms(ch2.key_terms)
        .add_block(BulletBlock(1, "İşbirliğine Dayalı Öğrenme (Kubaşık - Kooperatif Öğrenme)", [
            "Öğrencilerin kişisel olarak kendi öğrenmelerini ve birbirlerinin öğrenmelerini artırmak amacıyla, "
            "ortak bir hedef doğrultusunda küçük gruplar halinde birlikte çalışmasıdır. Kurt Lewin, Deutsch, "
            "Dewey, Slavin, Vygotsky ve Piaget gibi birçok araştırmacı bu modele katkı sağlamıştır.",
            "<b>Temel Özellikleri:</b> gruplar 2-6 kişiliktir ve heterojendir (yetenek, cinsiyet, akademik "
            "başarı, sosyal beceri açısından farklı öğrencilerden oluşur); öğrencilerin gruplar halinde yüz "
            "yüze etkileşim kurabileceği küme düzeninde oturtulması en uygun olanıdır; öğrenciler birbirleriyle "
            "yardımlaşır, öğrendiklerini paylaşır, birbirini destekler ve güdüler. Bu model öğrencilere çok "
            "yönlü ve empatik düşünme becerisi kazandırır.",
        ]))
    )
    ch2.pages.append(
        ChapterPage()
        .add_callout(Callout("caution", "Dikkat / Püf Noktası",
            "İşbirlikli öğrenmede liderlik rolü ya da tek başına inisiyatif alma yoktur; liderlik paylaşılır. "
            "Bireysellik geri plandadır. Öğrencilerin grubun tümünün başarısına etki ettiklerini kavramalarına "
            "<b>'olumlu bağlılık'</b> denir."))
        .add_table(ComparisonTable(
            "Karşılaştırma: Küme Çalışması vs. İşbirliğine Dayalı Öğrenme",
            ["Özellik", "Küme Çalışmaları", "İşbirliğine Dayalı Öğrenme"],
            [
                ["Grup Yapısı", "Homojen gruptur.", "Heterojen yetenekli gruptur."],
                ["Bağımlılık Durumu", "Bağımlılık yoktur.", "Olumlu bağlılık vardır."],
                ["Amaçlar", "Bireysel amaçlar vardır.", "Ortak grup amaçları vardır."],
                ["Liderlik", "Lider atanır.", "Liderlik paylaşımı vardır."],
                ["Sorumluluk", "Rastgele ortaya çıkabilir.", "Bireysel sorumluluk ön plandadır."],
            ]
        ))
        .add_block(BulletBlock(2, "Aktif Öğrenme (Good)", [
            "Aktif öğrenme, öğrencinin dinlemekten çok derse katıldığı, karmaşık öğretimsel işlerle zihinsel "
            "yeteneklerini kullanmaya zorlandığı bir süreçtir.",
            "Öğrenci, öğrenme sürecinin sorumluluğunu taşır; öğrenciye çeşitli yönlerle ilgili karar alma ve "
            "öz düzenleme yapma fırsatları verilir. Aktif olma, hem süreç hem de sonuçla ilgilidir; okuma, "
            "yazma ve tartışma gibi etkinliklerle desteklenir, öğrencilerin tutum ve değerleri dikkate alınır.",
        ]))
    )
    ch2.pages.append(
        ChapterPage()
        .add_block(BulletBlock(3, "Anlamlı Öğrenme (D. Ausubel)", [
            "Bireyin kavramlar arasındaki ilişkiyi fark etmesini içeren öğrenmedir. Öğretmen merkezlidir ve "
            "temel kavramların önce, ayrıntıların daha sonra öğretildiği tümdengelim yöntemi kullanılır.",
            "İçeriğin iyi yapılandırılmasına, öğrencinin zihinsel hazır oluşuna ve zihnin çalışma prensiplerine "
            "dikkat edilir. Kavram öğrenme ve kavram etrafında öğrenmelerin gerçekleşmesi esastır; bu modelde "
            "en çok <b>kavram haritaları</b> kullanılır.",
        ]))
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "Anlamlı öğrenmenin gerçekleşmesi için en kritik şart, öğrencinin daha önceki öğrendikleri "
            "(bilişsel yapısı) ile yeni öğrenecekleri arasında mutlaka bağ kurulmasıdır."))
        .add_block(BulletBlock(4, "Öğretim Durumları Modeli (Gagne)", [
            "Gagne, öğrenme sürecinde kazanılan beş temel davranıştan söz eder: Sözel bilgiler, Zihinsel "
            "beceriler, Psiko-motor beceriler, Tutumlar ve Bilişsel stratejiler. Zihinsel beceriler önemlidir "
            "ve basitten karmaşığa giden bir yol izlenir.",
            "<b>Öğrenme Türleri Hiyerarşisi:</b> ilk 5'i davranışçı kurama (klasik ve edimsel koşullanma), "
            "son 3'ü bilişsel kurama dayanan 8 aşamalı bir süreçtir: İşaret Öğrenme → Uyarıcı-Tepki Öğrenmesi "
            "→ Zincirleme Öğrenme → Sözel Öğrenme → Ayırt Etmeyi Öğrenme → Kavram Öğrenme → İlke Öğrenme → "
            "Problem Çözme.",
            "<b>Dersin İşleniş Aşamaları (Uygulama Adımları):</b> Dikkat Çekme → Hedeften Haberdar Etme → "
            "Ön Bilgileri Hatırlatma → Uyarıcı Materyal Sunma → Öğrenciye Rehberlik Etme → Davranışı Ortaya "
            "Çıkarma → Geribildirim ve Düzeltme Verme → Performans Değerlendirme → Kalıcılığı ve Transferi "
            "Sağlama.",
        ]))
        .add_block(BulletBlock(5, "Temel Öğretme Modeli (Glasser)", [
            "Okulda etkili öğretimi gerçekleştirmek için öğretme işinin öğretmen tarafından yapıldığını "
            "savunan ve dört temel öğeden oluşan bir modeldir.",
        ]))
    )
    ch2.pages.append(
        ChapterPage()
        .add_flow(FlowDiagram([
            FlowStep("Hedefler Saptanır"),
            FlowStep("Gerekli Giriş Davranışları Belirlenir"),
            FlowStep("Öğretme-Öğrenme Ortamı", "Seçilir ve Düzenlenir"),
            FlowStep("Değerlendirme Yapılır"),
        ], caption="Glasser'ın Temel Öğretme Modelinin Öğeleri (Akış Şeması)"))
        .add_callout(Callout("focus", "Sınavda Ana Ayrım — Gagne ile Glasser",
            "Gagne'nin modeli 8 aşamalı bir <b>öğrenme türleri hiyerarşisi</b> ve dersin işleniş sırasını "
            "tanımlarken; Glasser'ın modeli yalnızca 4 öğeden oluşan, öğretmenin hedef-giriş davranışı-ortam-"
            "değerlendirme sırasını izlediği daha sade bir akıştır."))
        .add_summary("Bölüm 2, öğrencilerin heterojen küçük gruplarda ortak hedef için çalıştığı İşbirliğine "
            "Dayalı Öğrenme'den, öğrencinin sürecin sorumluluğunu taşıdığı Aktif Öğrenme'ye; kavramlar arası "
            "ilişkiyi temel alan Ausubel'in Anlamlı Öğrenme'sinden, sekiz aşamalı hiyerarşisiyle Gagne'nin "
            "Öğretim Durumları Modeli'ne ve dört öğeli akışıyla Glasser'ın Temel Öğretme Modeli'ne uzanan beş "
            "kuram ve modeli ele alır.")
    )

    # =====================================================================
    # BÖLÜM 3 — Öğrenme-Öğretme Kuram ve Modelleri III
    # =====================================================================
    ch3 = Chapter(
        number=3,
        title="Öğrenme-Öğretme Kuram ve Modelleri III",
        subtitle="Yaşam Boyu ve Beyin Temelli Öğrenmeden, Çoklu Zeka'ya, Carroll/Slavin, Bandura ve Nunley'e",
        key_terms=[
            KeyTerm("Yaşam Boyu Öğrenme", "Bireyin neyi öğreneceğine kendi karar verdiği, eğitimi 'kurumsal/okul' yapısının dışına taşıyan, öğrenmeyi öğrenmenin ürünü olan yaklaşım."),
            KeyTerm("Beyin Temelli Öğrenme", "Öğretime insan beyni ve fonksiyonları üzerinden, gelişimsel ve sosyo-kültürel açıdan bakan model."),
            KeyTerm("Çoklu Zeka Kuramı", "Tek tip zeka anlayışını yıkan, bireylerin 8-9 farklı zeka boyutuyla dünyaya geldiğini savunan kuram (H. Gardner)."),
            KeyTerm("Basamaklı Öğretim Modeli", "Öğrenciyi pasif bilgi alıcıdan aktif bilgi üreticisine dönüştüren, C-B-A düzeylerinde ilerleyen sistem (Nunley)."),
        ],
    )
    ch3.pages.append(
        ChapterPage()
        .add_terms(ch3.key_terms)
        .add_block(BulletBlock(1, "Yaşam Boyu Öğrenme Modeli", [
            "Bilgi, modern dönemde hızlı bilimsel ve teknolojik gelişmelerin yol açtığı devinimler sonucunda "
            "çok çabuk eskimektedir. Yaşam boyu öğrenme, aslında 'öğrenmeyi öğrenmenin' bir ürünüdür.",
            "Birey neyi öğrenmesi gerektiğine bizzat kendisi karar verir, öğrenme sürecini kendisi yönlendirir "
            "ve eğitim olanaklarından kendi tercihiyle yararlanır. <b>7 temel ilkesi</b> vardır: Süreklilik, "
            "Değişim, Kendi Kendine Öğrenme, Araştırmacılık, Özdeğerlendirme, Sınıf Dışında Öğrenme ve "
            "Eğitimi Yönetme.",
        ]))
    )
    ch3.pages.append(
        ChapterPage()
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "Yaşam boyu öğrenme yaklaşımı, öğrenme-öğretme sürecine yepyeni bir boyut kazandırmış ve "
            "eğitim-öğretimi 'kurumsal/okul' yapısının dışına çıkartarak tüm hayata yaymıştır."))
        .add_block(BulletBlock(2, "Beyin Temelli Öğrenme Modeli", [
            "Öğretime gelişimsel ve sosyo-kültürel açıdan bakan, doğrudan insan beyni ve onun fonksiyonları "
            "üzerine temellendirilmiş bir modeldir.",
            "<b>İlkeleri:</b> her beyin tektir, bu yüzden öğrenme ortamları mutlaka bireysel farklılıklara "
            "yanıt verecek nitelikte düzenlenmelidir; beyin birçok işlevi aynı anda yapar, parça ve bütünleri "
            "eş zamanlı olarak işler; öğrenci için sunulan bilgi kesinlikle anlamlı olmalıdır; beyin, "
            "bilgileri anlamlaştırır ve bunları birbiriyle ilişkilendirerek zihinde örüntüler oluşturur.",
        ]))
        .add_callout(Callout("caution", "Dikkat / Püf Noktası",
            "Beyin temelli öğrenmede öğrenme süreci doğrudan insan fizyolojisi ile ilgilidir. Bu modeldeki "
            "en altın kural şudur: <b>öğrenme teşvikle (destekle) artar, korku (kaygı) ile azalır.</b>"))
        .add_block(BulletBlock(3, "Çoklu Zeka Kuramı (H. Gardner)", [
            "Howard Gardner tarafından 1983 yılında geliştirilen ve geleneksel tek tip zeka anlayışını yıkan "
            "devrim niteliğinde bir kuramdır: <b>'Gardner'a göre zeka; problem çözme kapasitesi ya da değerli "
            "bir veya birden çok kültürel yapı ürününe şekil vermektir.'</b>",
            "<b>Zekayı Etkileyen Faktörler:</b> zekanın oluşumunda hem biyolojik hem de çevresel etkenler "
            "(kaynaklara ulaşım şansı, kültürel, coğrafi, ailesel ve durumsal faktörler) rol oynar. Bireyler "
            "8 farklı zeka boyutu ile dünyaya gelirler ve her bireyde bu yetenekler az çok bulunur.",
        ]))
    )
    ch3.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Zeka Alanları ve Uygun Yöntemler",
            ["Zeka Alanı", "Özellik ve Uygun Yöntem"],
            [
                ["Sözel - Dilsel", "Konuşmayı sever, kelime oyunlarıyla ilgilenir, hitabet gücü yüksektir. (Tartışma, Anlatım, Rol Oynama)"],
                ["Sosyal - Kişilerarası", "Grup içinde başarılı ilişkiler kurar, doğal bir liderdir, empati yeteneği yüksektir. (İşbirlikli Öğrenme, Proje)"],
                ["Bedensel - Kinestetik", "Beden dilini iyi kullanır, denge ve esneklikte başarılıdır, yaparak-dokunarak öğrenir. (Eğitsel Oyun, Gösterip Yaptırma)"],
                ["Görsel - Uzamsal", "Zihinden resim çizmeyi, 3 boyutlu modellemeyi ve harita/tablo okumayı sever. (Resim Yapma, Tasarım)"],
                ["Özedönük - İçsel", "Bağımsızlık duygusu güçlüdür, yalnız çalışmayı sever, özgüveni ve özsaygısı yüksektir. (Bireysel Çalışma, Günlük Yazma)"],
                ["Mantıksal - Matematiksel", "Soyut düşünme, tümevarım/tümdengelimle çıkarım yapma ve sebep-sonuç ilişkisi kurmada ustadır. (Problem Çözme)"],
                ["Müzikal - Ritmik", "Seslere duyarlıdır, ritim tutar ve müzik aleti çalar. (Şarkı Söyleme/Yazma)"],
                ["Doğacı", "Hayvanları, bitkileri ve doğa olaylarını incelemekten hoşlanır. (Gezi, Gözlem)"],
                ["Varoluşçu (Yeni Eklenen 9. Boyut)", "Varlığın başı ve sonuyla ilgilenen, 'Biz kimiz?', 'Neden ölürüz?' gibi evrensel sorulara cevap arayan zeka türüdür."],
            ]
        ))
        .add_block(BulletBlock(4, "Okulda Öğrenme Modeli (Carroll)", [
            "Carroll, 1963 yılındaki makalesinde; her öğrenciye ihtiyaç duyduğu ek zaman verildiğinde tüm "
            "öğrencilerin hedeflenen öğrenme düzeyine ulaşabileceğini savunmuştur.",
            "Her öğrenci aynı düzeyde öğrenebilir fakat hızlı ve yavaş öğrenen öğrenciler vardır; öğrenmede "
            "belirleyici olan en temel değişken <b>zamandır</b>. Dört önemli değişkeni vardır: Kaliteli "
            "Öğretim, Yetenek, Fırsat ve Sebat.",
        ]))
    )
    ch3.pages.append(
        ChapterPage()
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "Carroll'un 'Okulda Öğrenme Modeli', kendisinden sonra gelen Bloom'un 'Tam Öğrenme Modeli'ne ve "
            "Slavin'in 'Etkili Öğretim Modeli'ne doğrudan esin kaynağı olmuştur."))
        .add_block(BulletBlock(5, "Etkili Öğretim Modeli (Slavin)", [
            "Öğrenme düzeyini etkileyen değişkenlerin çözümlenmesi yoluyla, öğrenme başarısının "
            "artırılabileceği varsayımına dayanır. Carroll'un modeliyle büyük benzerlikler taşır.",
        ]))
        .add_table(ComparisonTable(
            "Karşılaştırma: Carroll vs. Slavin",
            ["Özellik", "Okulda Öğrenme (Carroll)", "Etkili Öğretim (Slavin)"],
            [
                ["Temel Vurgu", "Zaman faktörü her şeyin merkezindedir.", "Değişkenlerin çözümlenmesi başarının anahtarıdır."],
                ["Ana Değişkenler", "Yetenek, Fırsat, Sebat, Kaliteli Öğretim.", "Öğretim Niteliği, Öğretim Düzeyine Uygunluk, Güdülenme, Zaman."],
                ["Ortak Nokta", "Öğretimin düzenlenmesiyle başarı artırılabilir.", "Öğretimin düzenlenmesiyle başarı artırılabilir."],
            ]
        ))
        .add_block(BulletBlock(6, "Model Alarak (Sosyal) Öğrenme Modeli (A. Bandura)", [
            "İnsanların diğer insanları gözleyerek öğrenebileceği (Platon ve Aristo'ya kadar uzanan) "
            "düşüncesini temel alır. Davranışçılardan Thorndike bu konuyu ilk kez deneysel açıklamış olsa da, "
            "süreci gözlem yollu öğrenme adıyla sistematik bir bütünlüğe ulaştıran kişi <b>Albert "
            "Bandura</b>'dır.",
            "Öğrenmede temel kavramlar; taklit, gözlem ve model almadır. Birey başkalarını gözlemleyerek ve "
            "deneyim kazanarak sadece beceri değil, yeni inanç ve değerler de oluşturabilir.",
        ]))
    )
    ch3.pages.append(
        ChapterPage()
        .add_block(BulletBlock(7, "Basamaklı Öğretim Modeli (Nunley)", [
            "Bilgi çağı kaynakları dikkate alınarak geliştirilen, bireysel farklılıklara göre öğretimin "
            "planlanması gerektiğini savunan sistemdir. Öğrenciyi 'bilgiyi alan' pasif durumdan çıkarıp, "
            "'bilgiye ulaşan ve yeni bilgi üreten' aktif duruma getirir. Süreç basitten karmaşığa 5 basamakta "
            "ve 3 düzeyde (C, B, A) gerçekleşir.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("1. Basamak", "Hedef Davranışların Sunulması ve Seçimi"),
            FlowStep("2. Basamak", "C Düzeyi"),
            FlowStep("3. Basamak", "B Düzeyi"),
            FlowStep("4. Basamak", "A Düzeyi"),
            FlowStep("5. Basamak", "Öğretmen Değerlendirmesi"),
        ], caption="Basamaklı Öğretimin Aşamaları"))
        .add_table(ComparisonTable(
            "Öğrenme Düzeylerinin Özellikleri (Sınav Püf Noktası)",
            ["Düzey", "Açıklama ve Örnek"],
            [
                ["C Basamağı (Bilgi ve Kavrama)", "Temel bilgilerin öğrenildiği aşamadır. (Örn: Öğrencinin İstanbul'un fethi ile ilgili salt bilgi edinmesi.)"],
                ["B Basamağı (Uygulama)", "Kazanılan temel bilgilerin uygulandığı, farklı örnekler üzerinde kullanıldığı basamaktır. (Örn: Öğrencinin İstanbul'un fethi ile ilgili bir slayt hazırlayıp sınıfa sunması.)"],
                ["A Basamağı (Analiz, Sentez, Değerlendirme)", "Yaratıcı ve eleştirel düşünme gibi üst düzey zihinsel süreçlerin kullanıldığı, sonuçların tartışıldığı en üst basamaktır. (Örn: Fethin çağın dünyası açısından önemi ile ilgili eleştirel bir makale yazması.)"],
            ]
        ))
        .add_summary("Bölüm 3, bilgiyi kurumsal sınırların dışına taşıyan Yaşam Boyu Öğrenme ve beyin "
            "fizyolojisini merkeze alan Beyin Temelli Öğrenme'den; Gardner'ın 9 zeka alanını kapsayan Çoklu "
            "Zeka Kuramı'na, zaman faktörünü öne çıkaran Carroll ve Slavin modellerine, gözlem yoluyla "
            "öğrenmeyi açıklayan Bandura'nın Sosyal Öğrenme Modeli'ne ve C-B-A düzeyleriyle ilerleyen "
            "Nunley'in Basamaklı Öğretim Modeli'ne uzanan yedi kuram ve modeli ele alır.")
    )

    # =====================================================================
    # BÖLÜM 4 — Öğretim Yöntemleri
    # =====================================================================
    ch4 = Chapter(
        number=4,
        title="Öğretim Yöntemleri",
        subtitle="Anlatım'dan Tartışma ve Örnek Olay'a, Gösterip Yaptırma'dan Problem Çözme ve Proje'ye",
        key_terms=[
            KeyTerm("Anlatım (Takrir) Yöntemi", "Eğitim tarihinin en yaygın ve en eski yöntemi; öğretmen merkezli, işiterek öğrenmeye dayanır, öğrenci pasiftir."),
            KeyTerm("Tartışma Yöntemi", "Öğrencilerin bir konu üzerinde düşünmesini, kendini ifade etmesini ve demokratik tutum kazanmasını sağlayan öğrenci merkezli yöntem."),
            KeyTerm("Örnek Olay Yöntemi", "Gerçek yaşamda karşılaşılan bir olayın sınıfa getirilip tartışılarak alternatif çözümler üretilmesini sağlayan yöntem."),
            KeyTerm("Gösterip Yaptırma", "Bir işin önce gösterilip sonra uygulatıldığı, psiko-motor becerilerin kazandırılmasında en etkili yöntem (Demonstrasyon ve Uygulama)."),
        ],
    )
    ch4.pages.append(
        ChapterPage()
        .add_terms(ch4.key_terms)
        .add_block(BulletBlock(1, "Anlatım (Takrir) Yöntemi", [
            "Eğitim tarihinde ve günümüzde en yaygın kullanılan 'en eski' öğretim yöntemidir. Öğretmen "
            "merkezlidir ve işiterek öğrenme temeline dayanır. Öğrenciler pasif konumdadır ve konuyu dinleyip "
            "not alırlar.",
            "<b>Ne Zaman Kullanılır?</b> Kısa zamanda kalabalık gruplara organize bilgi sunmak isteniyorsa, "
            "dersin girişinde (dikkat çekme/güdüleme), özetleme aşamasında veya soyut/anlaşılması güç "
            "kavramların aktarılmasında en ideal yöntemdir.",
            "<b>Sınırlılıkları:</b> sadece dinlemenin öğrenmedeki etkisi %20'dir; bu nedenle tek başına "
            "kullanıldığında öğrenme düşük düzeyde gerçekleşir. Görmeye dayalı ve psiko-motor (devinişsel) "
            "becerilerin öğretiminde etkisizdir. 'Konuşarak bilgi aktarma ihtiyacı sürekli olacaktır.'",
            "<b>Alt Türleri:</b> Düz anlatım, Sunu (Brifing — üst kurula bilgi verme), Konferans (uzman "
            "açıklaması), Söylev (Nutuk — coşku ve duygu ağırlıklı) ve Demeç.",
        ]))
    )
    ch4.pages.append(
        ChapterPage()
        .add_block(BulletBlock(2, "Tartışma Yöntemi", [
            "Öğrencilerin bir konu üzerinde düşünmelerini, kendilerini ifade etmelerini ve başkalarının "
            "görüşlerine saygı duymalarını (demokratik tutum) sağlayan öğrenci merkezli bir yöntemdir.",
            "<b>Özellikleri:</b> öğretmen-öğrenci ve öğrenci-öğrenci etkileşimi yüksektir. Öğrenciler analiz, "
            "sentez ve değerlendirme gibi üst düzey bilişsel beceriler gösterirler.",
            "<b>Uygulama Kuralları:</b> öğrenciler, tartışılacak konu hakkında en az 'bilgi düzeyinde' ön "
            "bilgiye (hazırbulunuşluğa) sahip olmalıdır. Bilgi düzeyindeki (kesin olgusal) konular tartışma "
            "konusu yapılamaz. Dersin tamamı tartışmaya ayrılmamalı ve mutlaka sonuç özetlenmelidir.",
        ]))
        .add_block(BulletBlock(3, "Soru - Cevap Yöntemi", [
            "Sokratik temellere dayanan, öğrencilerin bildiklerini/bilmediklerini ortaya çıkarmak ve onları "
            "düşünmeye sevk etmek için kullanılan tekniktir.",
            "<b>Uygulama Kuralları:</b> soru önce tüm sınıfa sorulmalı, herkesin düşünmesi için zaman (es "
            "payı) verilmeli, ardından cevaplayacak kişi seçilmelidir. Sorular numara/oturma sırasına göre "
            "değil, rastgele sorulmalıdır ki tüm sınıfın dikkati canlı kalsın.",
            "<b>Dönüt-Düzeltme:</b> doğru cevaplar anında pekiştirilmeli, yanlış cevaplarda ise öğrenci "
            "azarlanmamalı; doğruyu buldurucu ipuçları ve yan sorular kullanılmalıdır.",
        ]))
        .add_block(BulletBlock(4, "Örnek Olay Yöntemi", [
            "Gerçek yaşamda karşılaşılan veya karşılaşılması olası sorun niteliğindeki bir olayın "
            "(senaryonun) sınıf ortamına getirilerek tartışılmasıdır.",
            "<b>Özellikleri:</b> öğrenci merkezlidir. Öğrencilerin kavradıkları bilgileri gerçek bir durumda "
            "kullanmalarını ve alternatif çözüm yolları üretmelerini sağlar.",
        ]))
        .add_callout(Callout("caution", "Dikkat Edilmesi Gerekenler — Örnek Olay",
            "Sınıfa getirilen örnek olayın tek bir çözümü olmamalıdır; çünkü amaç öğrencilerin "
            "farklı/alternatif çözümler üretmesidir. Kalabalık sınıflarda tüm sınıfın katılımı zor "
            "olduğundan, sınıf küçük gruplara bölünerek uygulanmalıdır."))
    )
    ch4.pages.append(
        ChapterPage()
        .add_block(BulletBlock(5, "Gösterip Yaptırma (Demonstrasyon ve Uygulama)", [
            "Öğrenciye bir işin 'nasıl yapılacağının' önce gösterilip, sonra uygulatılmasıdır. Psiko-motor "
            "(devinişsel) becerilerin (örn: beden eğitimi dersinde nefes alma, tıp fakültesinde dikiş atma) "
            "ve uygulama düzeyindeki davranışların kazandırılmasında en etkili yöntemdir.",
            "<b>Uygulama Aşamaları:</b> 1. Aşama (Öğretmen Merkezli) — işlemin öğretmen tarafından "
            "gösterilmesi ve açıklanması (Gösteri); 2. Aşama (Öğrenci Merkezli) — öğrencinin gözetim altında "
            "alıştırma ve uygulama yapması (Yaptırma).",
        ]))
        .add_callout(Callout("caution", "Dikkat / Püf Noktası",
            "Öğrenci uygulama yaparken yaptığı hatalar anında düzeltilmelidir ve bir beceri tam olarak "
            "anlaşılmadan kesinlikle diğerine geçilmemelidir. Yaparak-yaşayarak öğrenme temelli olduğu için "
            "öğrenme çok kalıcıdır, ancak materyal gerektirdiği için maliyetli ve zaman alıcıdır."))
        .add_block(BulletBlock(6, "Problem Çözme Yöntemi", [
            "John Dewey'in ilerlemeci felsefesine dayanan, öğrencilere bilimsel düşünmeyi ve karşılaştıkları "
            "problemleri nasıl çözeceklerini öğreten yöntemdir. Üst düzey bilişsel fonksiyonlar (analiz, "
            "sentez) gerektirir.",
            "<b>Bilimsel Problem Çözme Basamakları:</b> Problemi Hissetme (Farkına Varma) → Problemi "
            "Tanımlama/Sınırlandırma → Veri Toplama → Hipotez (Denence) Kurma → Hipotezleri Test Etme → "
            "Sonuca Ulaşma ve Değerlendirme.",
        ]))
        .add_block(BulletBlock(7, "Proje ve Laboratuvar Yöntemleri", [
            "<b>Proje Yöntemi:</b> öğrencilerin bireysel veya gruplar halinde, kendi ilgi alanlarına göre "
            "seçtikleri bir konuda (disiplinlerarası bağ kurarak) araştırma yapmaları ve sonucunda somut bir "
            "ürün/rapor ortaya koymalarıdır. Okul ile gerçek hayat arasında bağ kurulmasını sağlar.",
            "<b>Laboratuvar Yöntemi:</b> öğrencilerin bilimsel bir bilgiyi gözlem ve deney yaparak, el "
            "becerilerini kullanarak elde ettikleri yöntemdir. Yaparak-yaşayarak öğrenme temellidir ve "
            "problem çözme becerisini geliştirir.",
        ]))
    )
    ch4.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Öğretmen Merkezli vs. Öğrenci Merkezli Yöntemler",
            ["Yöntem", "Merkez / Odak Noktası", "Etki Düzeyi"],
            [
                ["Anlatım", "Öğretmen / İşiterek Öğrenme", "Düşük (Pasif Dinleme)"],
                ["Gösterip Yaptırma", "Öğretmen + Öğrenci / Yaparak-Yaşayarak", "Yüksek (Psikomotor Beceriler)"],
                ["Tartışma", "Öğrenci / İşiterek ve Söyleyerek", "Orta-Yüksek (Demokratik Tutum)"],
                ["Örnek Olay", "Öğrenci / Görerek, İşiterek, Söyleyerek", "Yüksek (Alternatif Çözüm Üretme)"],
                ["Problem Çözme", "Öğrenci / Yaparak-Yaşayarak", "Çok Yüksek (Bilimsel Süreç)"],
            ]
        ))
        .add_callout(Callout("insight", "Kritik Çıkarım — Hedef Düzeyine Göre Yöntem Seçimi",
            "Dersin hedefleri 'Bilgi' düzeyinde (ezber) ise Anlatım; 'Kavrama' düzeyinde ise Tartışma/Örnek "
            "Olay; 'Uygulama' düzeyinde ise Gösterip Yaptırma; 'Analiz-Sentez' düzeyinde ise Problem Çözme / "
            "Proje yöntemleri tercih edilmelidir."))
        .add_summary("Bölüm 4, öğretmen merkezli ve pasif dinlemeye dayanan Anlatım'dan; öğrenci merkezli "
            "Tartışma, Soru-Cevap ve Örnek Olay yöntemlerine, psikomotor becerileri hedefleyen Gösterip "
            "Yaptırma'ya ve üst düzey bilişsel süreçler gerektiren Problem Çözme, Proje ve Laboratuvar "
            "yöntemlerine uzanan sekiz temel öğretim yöntemini, hedef düzeyine göre doğru yöntem seçimini "
            "vurgulayarak ele alır.")
    )

    # =====================================================================
    # BÖLÜM 5 — Öğretim Teknikleri
    # =====================================================================
    ch5 = Chapter(
        number=5,
        title="Öğretim Teknikleri",
        subtitle="Grupla Öğretim Tekniklerinden Bilişsel Çıraklığa, Tersine Eğitime ve Bireysel Tekniklere",
        key_terms=[
            KeyTerm("Altı Şapkalı Düşünme", "Öğrencilerin bir konuya çok farklı açılardan ve sistematik bakmalarını sağlayan, karar verme becerisini geliştiren teknik (E. De Bono)."),
            KeyTerm("Beyin Fırtınası", "Eleştiri ve yargılamanın kesinlikle yasak olduğu, fikirlerin niceliğinin önemli olduğu yaratıcı düşünce üretme tekniği."),
            KeyTerm("Mikro Öğretim", "Hizmet öncesi öğretmen adaylarına uygulama olanağı ve mesleki deneyim kazandırmak için kullanılan, kayda alıp izlemeye dayanan teknik."),
            KeyTerm("Keller Planı", "Sınıfın tümüne değil, hızları ve öğrenme stilleri benzeyen homojen küçük gruplara eğitim verilen bireyselleştirilmiş öğretim tekniği."),
        ],
    )
    ch5.pages.append(
        ChapterPage()
        .add_terms(ch5.key_terms)
        .add_block(BulletBlock(1, "Görüş Geliştirme", [
            "Öğrencilerin ucu açık, zıt kutupları olan konularda (katılıyorum, katılmıyorum, kararsızım vb.) "
            "fikir belirtmelerini ve birbirlerini dinleyerek görüşlerini değiştirebilme becerilerini "
            "kazandırmayı amaçlar.",
            "Öğrenciler neden o görüşü (seçeneği) seçtiklerini açıklarlar. Diğerlerini dinledikçe fikirleri "
            "değişebilir ve yer değiştirebilirler. Kazanan ya da kaybedeni (jürisi) yoktur; önemli olan "
            "alternatif ve esnek düşünebilmektir.",
        ]))
    )
    ch5.pages.append(
        ChapterPage()
        .add_block(BulletBlock(2, "Altı Şapkalı Düşünme (E. De Bono)", [
            "Öğrencilerin bir konuya çok farklı açılardan ve sistematik bakmalarını sağlayan, karar verme "
            "becerisini geliştiren bir tekniktir.",
        ]))
        .add_table(ComparisonTable(
            "Altı Şapkalı Düşünme Teknikleri",
            ["Şapka", "Temsil Ettiği"],
            [
                ["Beyaz Şapka (Tarafsız / Objektif)", "Tartışmasız kabul edilen net bilgileri ve sayıları temsil eder."],
                ["Kırmızı Şapka (Duygusal / Sübjektif)", "Tutkuları, hisleri ve sezgileri temsil eder."],
                ["Siyah Şapka (Kötümser / Objektif)", "Olumsuzlukları, tehlikeleri ve riskleri gösterir."],
                ["Sarı Şapka (İyimser / Objektif)", "Olayın avantajlarını, fırsatlarını ve yararlarını temsil eder."],
                ["Yeşil Şapka (Yaratıcı / Sübjektif)", "Üretkenliği, yepyeni fikirleri ve alternatifleri temsil eder."],
                ["Mavi Şapka (Karar Verici / Serinkanlı)", "Tüm süreci toparlayan, sonucu belirleyen ve durumu kontrol eden şapkadır."],
            ]
        ))
        .add_block(BulletBlock(3, "Altı Ayakkabılı Uygulama (E. De Bono)", [
            "Bireyin olaylara belirli bir davranış tarzına takılmadan yaklaşmasını ve esnek uygulama "
            "biçimleri geliştirmesini sağlar.",
        ]))
    )
    ch5.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Altı Ayakkabılı Uygulama",
            ["Ayakkabı", "Temsil Ettiği"],
            [
                ["Lacivert (Resmi)", "Rutin işleri, kuralı ve resmiyeti temsil eder."],
                ["Gri (Spor)", "Rahatlığı, tarafsız bilgi toplamayı simgeler."],
                ["Kahverengi (Yürüyüş)", "Pratikliği, esnekliği ve inisiyatif kullanarak sonuca varmayı anlatır."],
                ["Turuncu (Lastik Çizme)", "Aciliyet, kriz ve tehlike anlarında odaklanmayı temsil eder."],
                ["Pembe (Ev Terliği)", "İnsancıllığı, sıcaklığı, koruma ve acıma duygusunu ifade eder."],
                ["Mor (Binici Çizmesi)", "Otoriteyi, kişinin kendi yeteneğinden ziyade makam/yetki gücünü temsil eder."],
            ]
        ))
        .add_callout(Callout("caution", "Dikkat / Püf Noktası",
            "Altı 'Şapka' kafaya takıldığı için zihinsel düşünme becerilerini; Altı 'Ayakkabı' ise eyleme "
            "(harekete) geçmeyi simgelediği için uygulama becerilerini geliştirir. Ayrıca Altı 'Madalya' ise "
            "madalya değer taşıdığı için değerler öğretiminde kullanılır."))
        .add_block(BulletBlock(4, "İstasyon Tekniği", [
            "Sınıfın farklı köşelerinde kurulan 'istasyonlarda' (masalarda) öğrencilerin yarım bırakılan bir "
            "işi tamamlamayı, ona katkı sağlamayı ve süreç sonunda somut bir ürün (afiş, şiir vb.) ortaya "
            "koymayı öğrendikleri tekniktir. Çekingen öğrencilerin derse katılımını sağlar ve güdülenmeyi "
            "artırır.",
        ]))
    )
    ch5.pages.append(
        ChapterPage()
        .add_block(BulletBlock(5, "Beyin Fırtınası", [
            "Yaratıcı düşüncelerin ortaya çıkarılması amacıyla, eleştiri ve yargılamanın kesinlikle yasak "
            "olduğu, fikirlerin niteliğinden çok niceliğinin (sayısının) önemli olduğu tekniktir. Üç şekilde "
            "yapılabilir: <b>Benzerinden Yararlanma</b> (pamuk ırıştırma makinesinin kedinin tırnaklarından "
            "esinlenmesi), <b>Fikir Bağlantısı Kurma</b> (dikenlerden cırt cırt bantların icadı), "
            "<b>Zarardan Kâr Çıkarma</b> (beklemiş biradan hayvan yemi yapmak).",
        ]))
        .add_block(BulletBlock(6, "Konuşma Halkası", [
            "Öğrencilerin bir öyküdeki kişinin (kahramanın) yerine kendilerini koyarak çember şeklinde "
            "oturdukları tekniktir. Temel amaç empati kurmayı sağlamak ve duygularla düşünceleri birbirinden "
            "ayırt etmeyi öğretmektir.",
        ]))
        .add_block(BulletBlock(7, "Mikro Öğretim", [
            "Özellikle hizmet öncesi öğretmen adaylarına uygulama olanağı ve mesleki deneyim kazandırmak "
            "için kullanılır.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("Dersin Planlanması"),
            FlowStep("Mikro Dersin Uygulanması", "ve Kayda Alınması (Video/Teyp)"),
            FlowStep("Kayıtların İzlenmesi", "ve Dönüt Verilmesi"),
            FlowStep("Dersin Yeniden Düzenlenmesi"),
            FlowStep("Mikro Dersin Tekrar Uygulanması", "ve Kaydedilmesi"),
        ], caption="Mikro Öğretim Uygulama Basamakları"))
    )
    ch5.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Karıştırılan Teknikler",
            ["Karıştırılan Çift", "Temel Farklılıklar (Püf Noktası)"],
            [
                ["Rol Oynama ↔ Drama", "Rol oynamada başkasının kimliğine/penceresine bürünmek (kurgu) vardır. Drama ise öğrencinin kendi çözümünü/doğallığını katarak, gelecekte karşılaşacağı bir duruma çözüm bulması esastır."],
                ["Benzetim (Simülasyon) ↔ Analoji", "Benzetim, tehlikeli/maliyetli durumları öğretmek için gerçeğe birebir yapay ortam yaratmaktır (pilot, astronot eğitimi vb.). Analoji ise soyut/bilinmeyen bir kavramı, bilinen bir olaya/nesneye sözlü veya görsel benzetmektir (örn: kalbi su pompasına, kan dolaşımını şehir şebekesine benzetmek)."],
                ["Sokrat Tartışması ↔ Sokrat Semineri", "Sokrat Tartışması; ironi ve doğurtmaca aşamalarından oluşan, öğrencilerin yanlış bildiklerinden şüphe duymasını sağlayıp sorularla içlerindeki doğruyu buldurma (tümdengelim) tekniğidir. Sokrat Semineri ise ağır bir metnin/makalenin derse getirilip incelenmesine ve eleştirel tartışılmasına dayanır."],
            ]
        ))
        .add_block(BulletBlock(8, "Diğer Öğretim Teknikleri ve Yaklaşımları", [
            "<b>Bilişsel Çıraklık:</b> öğrencinin bir 'uzmanın' (usta) gözetiminde bir işe başladığı ve "
            "zamanla uzmanın desteğini yavaş yavaş çektiği öğretim sürecidir. Tarihimizdeki 'Ahilik' teşkilatı "
            "buna en güzel örnektir.",
            "<b>Tersine Eğitim (Flipped Classroom):</b> sistemin tamamen ters yüz edilmesidir. Normalde "
            "okulda bilgi verilir, evde ödev yapılırken; tersine eğitimde öğrenci 'ön bilgiyi' evde dijital "
            "ortamdan öğrenir, okula ise sadece derinlemesine proje, ödev ve tartışma yapmak için gelir.",
            "<b>Buz Kıran:</b> birbirini tanımayan katılımcıların bulunduğu ortamlarda, ortamı ısındırmak, "
            "stresi ve başarısızlık korkusunu kırmak için kullanılan başlangıç tekniğidir.",
        ]))
        .add_block(BulletBlock(9, "Bireysel Öğretim Teknikleri", [
            "<b>Bireyselleştirilmiş Öğretim (Keller Planı):</b> sınıftaki tüm öğrencilerin aynı hızda ve aynı "
            "etkinliklerle öğrenemeyeceği varsayımına dayanır. Bu yüzden öğretmen, sınıfın tümüne değil; "
            "hızları ve öğrenme stilleri birbirine benzeyen 3-4 öğrenciden oluşan 'homojen' küçük gruplara "
            "eğitim verir.",
            "<b>Tutor Destekli Öğretim:</b> öğrencinin eksik kaldığı konularda, sınıf öğretmeni dışında; "
            "konuya hakim üst sınıftan bir öğrenciden, bir stajyer öğretmenden veya bir etüt öğretmeninden "
            "(Tutor / Özel Öğretmen) birebir özel destek alması esasına dayanır.",
        ]))
    )
    ch5.pages.append(
        ChapterPage()
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "Öğretim teknikleri içerisinde 'bireysel hız' ön plana çıktığında Programlı Öğretim veya Keller "
            "Planı aranmalı; öğrenme engellerini ortadan kaldırmak için birebir destek vurgulandığında ise "
            "Tutor Destekli Öğretim akla gelmelidir."))
        .add_summary("Bölüm 5, sınıf içi grup dinamiklerini işleyen Görüş Geliştirme, Altı Şapkalı Düşünme, "
            "Altı Ayakkabılı Uygulama, İstasyon Tekniği, Beyin Fırtınası, Konuşma Halkası ve Mikro Öğretim "
            "gibi grupla öğretim tekniklerinden; Bilişsel Çıraklık ve Tersine Eğitim gibi yaklaşımlara, "
            "Keller Planı ve Tutor Destekli Öğretim gibi bireysel tekniklere uzanan geniş bir öğretim "
            "teknikleri yelpazesini, sık karıştırılan kavram çiftlerini netleştirerek ele alır.")
    )

    # =====================================================================
    # BÖLÜM 6 — Düşünme Biçimleri
    # =====================================================================
    ch6 = Chapter(
        number=6,
        title="Düşünme Biçimleri",
        subtitle="Yaratıcı ve Eleştirel Düşünmeden, Yansıtıcı, Analitik ve Metabilişsel Düşünmeye",
        key_terms=[
            KeyTerm("Yaratıcı Düşünme", "Bireyin yeni, farklı, orijinal, özgün (sentez düzeyi) ürünler veya düşünceler ortaya koymasıdır."),
            KeyTerm("Eleştirel Düşünme", "Sorgulayan bir yaklaşımla olayları ele alma, irdeleyici bir bakış açısıyla yorum yapma ve kanıt arama becerisidir."),
            KeyTerm("Yansıtıcı Düşünme", "Öğrencinin düşünerek ve araştırarak öğreneceği bilgi üzerinde durmasına olanak sağlayan, şüpheden aydınlanmaya uzanan düşünme yolu."),
            KeyTerm("Metabilişsel Düşünme", "Kişinin kendi düşünme süreçlerinin farkında olması ve bu süreçleri kontrol edebilmesi anlamına gelen üstbiliş becerisi."),
        ],
    )
    ch6.pages.append(
        ChapterPage()
        .add_terms(ch6.key_terms)
        .add_block(BulletBlock(1, "Yaratıcı Düşünme", [
            "Bireyin yeni, farklı, orijinal, özgün (sentez düzeyi), alternatifli ve ayrıştırıcı ürünler veya "
            "düşünceler ortaya koymasıdır.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("Hazırlık"),
            FlowStep("Kuluçka"),
            FlowStep("Aydınlanma"),
            FlowStep("Değerlendirme"),
        ], caption="Yaratıcı Düşünmenin Aşamaları"))
    )
    ch6.pages.append(
        ChapterPage()
        .add_block(BulletBlock(2, "Yaratıcı Düşünmenin Özellikleri ve Yolları", [
            "<b>Temel Özellikleri:</b> Esnek Düşünme (farklı yollar düşünebilme ve bunları deneme), Orijinal "
            "Düşünme (ortaya atılan yolun yeni ve mevcutlardan farklı olması), Akılcı Düşünme (zihinsel "
            "süreçlerin çok yönlü ve üst düzey olması), Ayrıştırıcı Düşünme (benzerlikleri ve farklılıkları "
            "ayrıştırabilme).",
            "<b>Yaratıcı Düşünme Yolları:</b> Sentezleme (hipotez kurma, plan yapma, analojik düşünme, "
            "başka araştırmalardan yararlanma), Eklemleme (büyük düşünme, düşünceyi hızla değiştirme, "
            "somutlaştırma ve geniş düşünme), İmgelemek (akılcılık, kestirimde bulunma, kuramsal düşünme, "
            "hayal etme, sezgileme).",
        ]))
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "Yaratıcı düşünme, Bloom taksonomisinin sentez düzeyine denk gelir. Yeni bir ürün, yeni bir "
            "fikir veya orijinal bir sentez oluşturmayı temel alır."))
        .add_block(BulletBlock(3, "Eleştirel Düşünme", [
            "Sorgulayan bir yaklaşımla olayları ve durumları ele alma, irdeleyici bir bakış açısıyla yorum "
            "yapma ve karar verme becerilerini içerir. Olayları olduğu gibi kabul etmez, kanıt arar.",
        ]))
        .add_table(ComparisonTable(
            "Eleştirel Düşünme vs. Yaratıcı Düşünme",
            ["Özellik", "Eleştirel Düşünme", "Yaratıcı Düşünme"],
            [
                ["Bilişsel Yapı", "Sol beyin etkindir", "Sağ beyin etkindir"],
                ["Yaklaşım Biçimi", "Analitik, nesnel, dikey", "Üretici, öznel, yatay"],
                ["Odak / Yayma", "Odaklama (derinleşme)", "Yayma (genişleme)"],
                ["İşlem Türü", "Birleştirici, sözel", "Ayırıcı, görsel"],
            ]
        ))
    )
    ch6.pages.append(
        ChapterPage()
        .add_block(BulletBlock(4, "Yansıtıcı Düşünme", [
            "İlerlemeci eğitim yaklaşımına dayanan ve öğrenciyi merkeze alan bir düşünme yoludur. Öğrencinin "
            "düşünerek ve araştırarak öğreneceği bilgi üzerinde durmasına olanak sağlar. Yapılandırmacılık, "
            "probleme dayalı öğrenme, proje temelli öğrenme, mikro öğretim ve günlük yazma gibi birçok "
            "çağdaş yöntemle geliştirilir.",
            "<b>Oluşumundaki İki Temel Aşama (Akış):</b> 1) İçine girilen merak, kuşku ve duraksama (şüphe) "
            "durumu; 2) Bu kuşkuyu açıklığa kavuşturacak araştırma ve sorgulama eğilimi.",
        ]))
        .add_callout(Callout("insight", "Kritik Çıkarım",
            "Yansıtıcı düşünme, kişinin kendi tecrübelerinden ders çıkarması ve bir şüphe durumundan "
            "araştırma yoluyla yeni bir anlamaya (aydınlanmaya) geçmesidir."))
        .add_block(BulletBlock(5, "Analitik Düşünme", [
            "Bir bütündeki her bir parçanın tek tek analiz edilerek, bütünle veya sistemle olan ilişkilerinin "
            "incelendiği düşünme becerisidir. Doğrudan analiz becerisi ile ilişkilidir.",
            "<b>Analitik Düşünmeyi Geliştiren Örnek Uygulamalar:</b> Balık Kılçığı Yöntemi (bir sorunu — "
            "örn. KPSS sorunu — tek bir kütle olarak değil, onu oluşturan parçalara/neden ve alt nedenlere "
            "tek tek ayırarak incelemek); parça-bütün ilişkisini yorumlamayı gerektiren yap-bozlar (puzzle) "
            "yapmak; 'İki resim arasındaki 8 farkı bulun' tarzı detaycı etkinlikler uygulamak.",
        ]))
        .add_block(BulletBlock(6, "Metabilişsel Düşünme (Üstbiliş)", [
            "Bilişsel psikoloji alanına 1970'li yıllarda John Flavell'in çalışmalarıyla girmiş olan en üst "
            "düzey düşünme becerilerinden biridir. En kısa tanımıyla kişinin 'kendi düşünme süreçlerinin "
            "farkında olması ve bu süreçleri kontrol edebilmesi' anlamına gelir.",
            "Birey kendi bilişsel süreçlerinin nasıl işlediğini anlar, öğrenme süreçlerini denetim altına "
            "alır ve daha nitelikli bir öğrenme için zihinsel süreçlerini yeniden düzenleyerek en etkili "
            "biçimde kullanır.",
        ]))
    )
    ch6.pages.append(
        ChapterPage()
        .add_callout(Callout("caution", "Dikkat / Püf Noktası",
            "Metabilişsel (üstbilişsel) düşünmede öğrencinin odaklandığı şey dışarıdaki ders konusu değil, "
            "bizzat kendi zihnidir. Kısacası öğrencinin 'Ben en iyi nasıl öğreniyorum?' sorusunun cevabını "
            "bilmesi ve kendi öğrenme stratejisini bizzat kendisinin yönetmesidir."))
        .add_summary("Bölüm 6, Bloom'un sentez düzeyine karşılık gelen Yaratıcı Düşünme'den, kanıt arayan "
            "ve sorgulayan Eleştirel Düşünme'ye; şüpheden aydınlanmaya uzanan Yansıtıcı Düşünme'den, bütünü "
            "parçalara ayırarak inceleyen Analitik Düşünme'ye ve kişinin kendi düşünme sürecini yönetmesini "
            "sağlayan Metabilişsel Düşünme'ye (üstbiliş) kadar beş temel düşünme biçimini ele alır.")
    )

    chapters = [ch1, ch2, ch3, ch4, ch5, ch6]

    # =====================================================================
    # SÖZLÜK
    # =====================================================================
    glossary = [
        Concept("Tam Öğrenme", "Olumlu koşullar sağlanırsa herkesin öğrenebileceğini savunan, %90'a varan başarı hedefleyen grupla öğretim modeli.", "B. Bloom", 1),
        Concept("Programlı Öğrenme (KEBAB)", "Küçük Adımlar, Etkin Katılım, Başarı, Anında Düzeltme, Bireysel Hız ilkelerine dayanan bireyselleştirilmiş öğretim sistemi.", "B.F. Skinner", 1),
        Concept("Probleme Dayalı Öğrenme", "İlgi ve merak uyandıran bir problemle başlanan, öğrencinin süreci yönettiği öğrenci merkezli yaklaşım.", "J. Dewey", 1),
        Concept("Proje Tabanlı Öğrenme", "Küçük gruplarda işbirlikli çalışılan, sonunda somut bir ürün/rapor ortaya konan çağdaş model.", "Genel", 1),
        Concept("Yapılandırmacılık", "Bilginin nesnel değil, bireyin kendi deneyimleriyle öznel olarak inşa ettiği bir şey olduğunu savunan kuram.", "J. Piaget", 1),
        Concept("İşbirliğine Dayalı Öğrenme", "Heterojen küçük gruplarda ortak hedef için birlikte çalışma; 'olumlu bağlılık' kavramıyla tanımlanır.", "Kubaşık Öğrenme", 2),
        Concept("Aktif Öğrenme", "Öğrencinin öğrenme sürecinin sorumluluğunu taşıdığı, karar alma ve öz düzenleme fırsatları verilen süreç.", "Good", 2),
        Concept("Anlamlı Öğrenme", "Kavramlar arası ilişkinin fark edilmesine dayanan, kavram haritalarıyla desteklenen öğretmen merkezli öğrenme.", "D. Ausubel", 2),
        Concept("Öğretim Durumları Modeli", "8 aşamalı öğrenme türleri hiyerarşisi ve dersin işleniş sırasını tanımlayan model.", "Gagne", 2),
        Concept("Temel Öğretme Modeli", "Hedefler, giriş davranışları, ortam ve değerlendirmeden oluşan 4 öğeli öğretme modeli.", "Glasser", 2),
        Concept("Yaşam Boyu Öğrenme", "Bireyin öğrenme sürecini kendi yönlendirdiği, eğitimi okul yapısının dışına taşıyan yaklaşım.", "Genel", 3),
        Concept("Beyin Temelli Öğrenme", "Öğrenmeyi doğrudan insan beyni ve fizyolojisi üzerinden açıklayan, 'öğrenme teşvikle artar' ilkesine dayanan model.", "Genel", 3),
        Concept("Çoklu Zeka Kuramı", "Bireylerin 9 farklı zeka boyutuyla dünyaya geldiğini savunan, tek tip zeka anlayışını yıkan kuram.", "H. Gardner", 3),
        Concept("Okulda Öğrenme Modeli", "Öğrenmede belirleyici en temel değişkenin zaman olduğunu savunan model.", "Carroll", 3),
        Concept("Model Alarak (Sosyal) Öğrenme", "Taklit, gözlem ve model alma yoluyla öğrenmeyi açıklayan, gözlem yollu öğrenmeyi sistematikleştiren model.", "A. Bandura", 3),
        Concept("Basamaklı Öğretim Modeli", "Öğrenciyi pasif bilgi alıcıdan aktif bilgi üreticisine dönüştüren, C-B-A düzeylerinde ilerleyen sistem.", "Nunley", 3),
        Concept("Anlatım (Takrir) Yöntemi", "Öğretmen merkezli, işiterek öğrenmeye dayanan, en eski ve en yaygın öğretim yöntemi.", "Öğretim Yöntemleri", 4),
        Concept("Tartışma Yöntemi", "Öğrencilerin en az bilgi düzeyinde ön bilgiye sahip olması gereken, demokratik tutum kazandıran öğrenci merkezli yöntem.", "Öğretim Yöntemleri", 4),
        Concept("Soru-Cevap Yöntemi", "Sokratik temellere dayanan, sorunun tüm sınıfa sorulup rastgele bir öğrenciye yöneltildiği teknik.", "Öğretim Yöntemleri", 4),
        Concept("Örnek Olay Yöntemi", "Gerçek yaşamdaki bir olayın sınıfa getirilip tek çözümü olmayan biçimde tartışılmasıdır.", "Öğretim Yöntemleri", 4),
        Concept("Gösterip Yaptırma", "Bir işin önce gösterilip sonra uygulatıldığı, psiko-motor becerilerin kazandırılmasında en etkili yöntem.", "Öğretim Yöntemleri", 4),
        Concept("Problem Çözme Yöntemi", "Bilimsel düşünmeyi ve problem çözme basamaklarını öğreten, üst düzey bilişsel fonksiyon gerektiren yöntem.", "J. Dewey", 4),
        Concept("Altı Şapkalı Düşünme", "Bir konuya beyaz, kırmızı, siyah, sarı, yeşil ve mavi şapka perspektifleriyle bakmayı sağlayan teknik.", "E. De Bono", 5),
        Concept("Altı Ayakkabılı Uygulama", "Bireyin olaylara farklı davranış tarzlarıyla (lacivert, gri, kahverengi, turuncu, pembe, mor) yaklaşmasını sağlayan teknik.", "E. De Bono", 5),
        Concept("Beyin Fırtınası", "Eleştirinin yasak olduğu, fikir niceliğinin önemli olduğu yaratıcı düşünce üretme tekniği.", "Öğretim Teknikleri", 5),
        Concept("Mikro Öğretim", "Dersin planlanıp kayda alındığı, izlenip dönüt verildiği ve yeniden uygulandığı öğretmen yetiştirme tekniği.", "Öğretim Teknikleri", 5),
        Concept("Bilişsel Çıraklık", "Öğrencinin bir uzmanın gözetiminde başladığı, desteğin zamanla azaltıldığı öğretim süreci (Ahilik örneği).", "Öğretim Teknikleri", 5),
        Concept("Tersine Eğitim (Flipped Classroom)", "Ön bilginin evde dijital ortamdan öğrenildiği, okulda ise proje/tartışma yapılan ters yüz edilmiş sistem.", "Öğretim Teknikleri", 5),
        Concept("Keller Planı", "Homojen 3-4 kişilik küçük gruplara, hız ve öğrenme stiline göre eğitim verilen bireyselleştirilmiş öğretim tekniği.", "Bireysel Öğretim Teknikleri", 5),
        Concept("Yaratıcı Düşünme", "Hazırlık-Kuluçka-Aydınlanma-Değerlendirme aşamalarıyla ilerleyen, Bloom'un sentez düzeyine karşılık gelen düşünme biçimi.", "Düşünme Biçimleri", 6),
        Concept("Eleştirel Düşünme", "Sol beyin etkinliğine dayanan, analitik ve kanıt arayan, olayları sorgulayarak ele alan düşünme biçimi.", "Düşünme Biçimleri", 6),
        Concept("Yansıtıcı Düşünme", "Şüphe durumundan araştırma yoluyla aydınlanmaya geçişi tanımlayan, öğrenciyi merkeze alan düşünme yolu.", "Düşünme Biçimleri", 6),
        Concept("Metabilişsel Düşünme (Üstbiliş)", "Kişinin kendi düşünme süreçlerinin farkında olması ve bu süreçleri kontrol edebilmesi.", "J. Flavell", 6),
    ]

    # =====================================================================
    # TEST — 20 Soruluk Genel Değerlendirme
    # =====================================================================
    test_questions = [
        TestQuestion(1, "Bloom'un Tam Öğrenme Modeli'ne göre, olumlu öğrenme koşulları sağlandığında okuldaki başarı hangi orana kadar çıkarılabilir?",
            {"A": "%50", "B": "%70", "C": "%80", "D": "%90", "E": "%100"}),
        TestQuestion(2, "Programlı Öğrenmeyi (Skinner) Tam Öğrenmeden (Bloom) ayıran en belirgin fark aşağıdakilerden hangisidir?",
            {"A": "Konuların küçük birimlere ayrılması", "B": "Pekiştireç kullanılması",
             "C": "Bireysel hız ilkesi", "D": "Öğretim hizmetinin niteliği", "E": "Dönüt-düzeltme verilmesi"}),
        TestQuestion(3, "Proje Tabanlı Öğrenme ile Probleme Dayalı Öğrenme arasındaki temel fark aşağıdakilerden hangisidir?",
            {"A": "Proje tabanlı öğrenmede somut bir ürün hedeflenirken, probleme dayalı öğrenmede yalnızca problemi çözme süreci önemlidir",
             "B": "Probleme dayalı öğrenmede grup çalışması yokken proje tabanlıda vardır",
             "C": "Proje tabanlı öğrenme öğretmen merkezlidir", "D": "Probleme dayalı öğrenmede teknoloji hedef kabul edilir",
             "E": "İkisi arasında hiçbir fark yoktur"}),
        TestQuestion(4, "Yapılandırmacı yaklaşım türlerinden, öğrenmede kültürün ve dilin büyük etkisi olduğunu, bilginin sosyal etkileşimle oluştuğunu savunan tür hangisidir?",
            {"A": "Bilişsel Yapılandırmacılık", "B": "Radikal Yapılandırmacılık", "C": "Sosyal Yapılandırmacılık",
             "D": "Eleştirel Yapılandırmacılık", "E": "Davranışçı Yapılandırmacılık"}),
        TestQuestion(5, "İşbirliğine Dayalı Öğrenmede, öğrencilerin grubun tümünün başarısına etki ettiklerini kavramalarına ne ad verilir?",
            {"A": "Olumlu bağlılık", "B": "Bireysel sorumluluk", "C": "Liderlik paylaşımı",
             "D": "Heterojen gruplaşma", "E": "Ortak amaç"}),
        TestQuestion(6, "Ausubel'in Anlamlı Öğrenmesinin gerçekleşmesi için en kritik şart aşağıdakilerden hangisidir?",
            {"A": "Öğrencinin bireysel hızda ilerlemesi", "B": "Öğrencinin önceki bilişsel yapısı ile yeni bilgi arasında bağ kurulması",
             "C": "Sınıfın homojen gruplara ayrılması", "D": "Öğretmenin sadece anlatım yöntemini kullanması",
             "E": "Konunun küçük parçalara bölünmesi"}),
        TestQuestion(7, "Gagne'nin 8 aşamalı Öğrenme Türleri Hiyerarşisi'nde ilk 5 aşama hangi kurama dayanır?",
            {"A": "Bilişsel kurama", "B": "Yapılandırmacı kurama", "C": "Davranışçı kurama",
             "D": "Hümanist kurama", "E": "Sosyal öğrenme kuramına"}),
        TestQuestion(8, "Glasser'ın Temel Öğretme Modeli'nde ilk adım aşağıdakilerden hangisidir?",
            {"A": "Değerlendirme yapılır", "B": "Öğretme-öğrenme ortamı seçilir", "C": "Hedefler saptanır",
             "D": "Gerekli giriş davranışları belirlenir", "E": "Dönüt ve düzeltme verilir"}),
        TestQuestion(9, "Beyin Temelli Öğrenme Modeli'ndeki 'en altın kural' aşağıdakilerden hangisidir?",
            {"A": "Öğrenme teşvikle (destekle) artar, korku (kaygı) ile azalır", "B": "Öğrenme yalnızca bireysel ortamda gerçekleşir",
             "C": "Beyin işlevleri sırayla, tek tek gerçekleşir", "D": "Bilgi mutlaka ezber yoluyla kalıcı hale gelir",
             "E": "Öğrenme sadece grup içinde gerçekleşebilir"}),
        TestQuestion(10, "Gardner'ın Çoklu Zeka Kuramı'na sonradan eklenen 9. zeka boyutu, 'Biz kimiz?', 'Neden ölürüz?' gibi evrensel sorularla ilgilenen hangi zeka türüdür?",
            {"A": "Doğacı Zeka", "B": "Özedönük-İçsel Zeka", "C": "Varoluşçu Zeka",
             "D": "Mantıksal-Matematiksel Zeka", "E": "Sosyal-Kişilerarası Zeka"}),
        TestQuestion(11, "Carroll'un Okulda Öğrenme Modeli'ne göre, öğrenmede belirleyici olan en temel değişken hangisidir?",
            {"A": "Yetenek", "B": "Fırsat", "C": "Sebat", "D": "Zaman", "E": "Kaliteli öğretim"}),
        TestQuestion(12, "Gözlem yollu öğrenmeyi sistematik bir bütünlüğe ulaştıran, 'Model Alarak (Sosyal) Öğrenme Modeli'nin öncüsü kimdir?",
            {"A": "Thorndike", "B": "Albert Bandura", "C": "Piaget", "D": "Skinner", "E": "Vygotsky"}),
        TestQuestion(13, "Nunley'in Basamaklı Öğretim Modeli'nde, öğrencinin 'İstanbul'un fethi ile ilgili bir slayt hazırlayıp sınıfa sunması' hangi düzeye örnektir?",
            {"A": "C Basamağı (Bilgi ve Kavrama)", "B": "B Basamağı (Uygulama)",
             "C": "A Basamağı (Analiz, Sentez, Değerlendirme)", "D": "Hedef Davranışların Sunulması",
             "E": "Öğretmen Değerlendirmesi"}),
        TestQuestion(14, "Anlatım (Takrir) Yönteminde, sadece dinlemenin öğrenmedeki etkisi yaklaşık yüzde kaçtır?",
            {"A": "%10", "B": "%20", "C": "%40", "D": "%60", "E": "%80"}),
        TestQuestion(15, "Soru-Cevap Yönteminin uygulama kurallarına göre, soru sorulduktan sonra cevaplayacak kişi nasıl seçilmelidir?",
            {"A": "Oturma sırasına göre", "B": "Numara sırasına göre", "C": "Rastgele",
             "D": "Her zaman gönüllü öğrenciler arasından", "E": "Sadece başarılı öğrenciler arasından"}),
        TestQuestion(16, "Örnek Olay Yönteminde dikkat edilmesi gereken en önemli nokta aşağıdakilerden hangisidir?",
            {"A": "Olayın tek bir doğru çözümü olmalıdır", "B": "Olayın tek bir çözümü olmamalı, alternatif çözümler üretilmelidir",
             "C": "Olay mutlaka öğretmen tarafından çözülmelidir", "D": "Olay kalabalık sınıfta tek grup halinde tartışılmalıdır",
             "E": "Olay yalnızca bilgi düzeyinde ele alınmalıdır"}),
        TestQuestion(17, "Altı Şapkalı Düşünme tekniğinde, tutkuları, hisleri ve sezgileri temsil eden şapka hangisidir?",
            {"A": "Beyaz Şapka", "B": "Kırmızı Şapka", "C": "Siyah Şapka", "D": "Sarı Şapka", "E": "Yeşil Şapka"}),
        TestQuestion(18, "Rol Oynama ile Drama tekniği arasındaki temel fark aşağıdakilerden hangisidir?",
            {"A": "Rol oynamada başkasının kimliğine bürünme (kurgu) vardır; drama ise öğrencinin kendi çözümünü/doğallığını katmasına dayanır",
             "B": "Drama bireysel, rol oynama grupla yapılır", "C": "Rol oynama yalnızca yazılı olarak yapılır",
             "D": "İkisi arasında hiçbir fark yoktur", "E": "Drama yalnızca psiko-motor beceriler için kullanılır"}),
        TestQuestion(19, "Keller Planı (Bireyselleştirilmiş Öğretim) hangi varsayıma dayanır?",
            {"A": "Tüm sınıfın aynı hızda ve aynı etkinliklerle öğrenebileceği", "B": "Sınıftaki tüm öğrencilerin aynı hızda öğrenemeyeceği",
             "C": "Öğrencilerin yalnızca grupla öğrenebileceği", "D": "Öğretmenin sınıfa hiç müdahale etmemesi gerektiği",
             "E": "Değerlendirmenin yalnızca yazılı sınavla yapılması gerektiği"}),
        TestQuestion(20, "Eleştirel Düşünme ile Yaratıcı Düşünme karşılaştırıldığında, aşağıdakilerden hangisi Eleştirel Düşünme için doğrudur?",
            {"A": "Sağ beyin etkindir, yayma (genişleme) odaklıdır", "B": "Sol beyin etkindir, odaklama (derinleşme) esastır",
             "C": "Üretici ve özneldir", "D": "Görsel işlem türü baskındır", "E": "Sentez düzeyine karşılık gelir"}),
    ]

    answer_key_items = [
        AnswerItem(1, "D", "Bloom'un Tam Öğrenme Modeli, okuldaki başarıyı <b>%90'a</b> çıkaran (alt limit %70) bir grupla öğretim sürecidir."),
        AnswerItem(2, "C", "<b>Bireysel Hız</b> ilkesi (KEBAB'ın son öğesi), Programlı Öğrenmeyi Tam Öğrenmeden ayıran en belirgin farktır."),
        AnswerItem(3, "A", "Proje tabanlı öğrenme sürecin sonunda somut bir ürün/rapor hedeflerken, probleme dayalı öğrenmede somut ürün yoktur; yalnızca <b>problemi çözme süreci</b> önemlidir."),
        AnswerItem(4, "C", "<b>Sosyal Yapılandırmacılık</b>, öğrenmede kültürün ve dilin büyük etkisi olduğunu, bilginin sosyal etkileşimle oluştuğunu savunur."),
        AnswerItem(5, "A", "Öğrencilerin grubun tümünün başarısına etki ettiklerini kavramalarına <b>'olumlu bağlılık'</b> denir."),
        AnswerItem(6, "B", "Anlamlı öğrenmenin en kritik şartı, öğrencinin <b>önceki bilişsel yapısı ile yeni öğrenecekleri arasında bağ kurulmasıdır.</b>"),
        AnswerItem(7, "C", "Gagne'nin 8 aşamalı hiyerarşisinde ilk 5 aşama <b>davranışçı kurama</b> (klasik ve edimsel koşullanma), son 3 aşama ise bilişsel kurama dayanır."),
        AnswerItem(8, "C", "Glasser'ın Temel Öğretme Modeli'nde ilk adım <b>hedeflerin saptanmasıdır</b>; ardından giriş davranışları belirlenir, ortam düzenlenir ve değerlendirme yapılır."),
        AnswerItem(9, "A", "Beyin Temelli Öğrenme'nin en altın kuralı: <b>'Öğrenme teşvikle (destekle) artar, korku (kaygı) ile azalır.'</b>"),
        AnswerItem(10, "C", "<b>Varoluşçu Zeka</b>, Gardner'ın kuramına sonradan eklenen 9. boyuttur ve varlığın başı-sonuyla ilgili evrensel sorularla ilgilenir."),
        AnswerItem(11, "D", "Carroll'un modeline göre öğrenmede belirleyici olan en temel değişken <b>zamandır.</b>"),
        AnswerItem(12, "B", "Gözlem yollu öğrenmeyi sistematik bir bütünlüğe ulaştıran kişi <b>Albert Bandura</b>'dır (Thorndike konuyu ilk kez deneysel olarak açıklamıştır, ancak sistemleştiren o değildir)."),
        AnswerItem(13, "B", "Kazanılan bilgiyi farklı bir örnekte (slayt hazırlama) uygulamak <b>B Basamağı (Uygulama)</b> düzeyine örnektir."),
        AnswerItem(14, "B", "Anlatım yönteminde sadece dinlemenin öğrenmedeki etkisi yaklaşık <b>%20</b>'dir."),
        AnswerItem(15, "C", "Sorular numara veya oturma sırasına göre değil, tüm sınıfın dikkatinin canlı kalması için <b>rastgele</b> sorulmalıdır."),
        AnswerItem(16, "B", "Örnek olayın amacı öğrencilerin farklı/alternatif çözümler üretmesi olduğundan, olayın <b>tek bir çözümü olmamalıdır.</b>"),
        AnswerItem(17, "B", "<b>Kırmızı Şapka</b>, tutkuları, hisleri ve sezgileri (duygusal/sübjektif boyutu) temsil eder."),
        AnswerItem(18, "A", "Rol oynamada başkasının kimliğine/penceresine bürünme (kurgu) vardır; <b>Drama'da ise öğrenci kendi çözümünü/doğallığını katar.</b>"),
        AnswerItem(19, "B", "Keller Planı, sınıftaki tüm öğrencilerin <b>aynı hızda ve aynı etkinliklerle öğrenemeyeceği</b> varsayımına dayanır; bu yüzden homojen küçük gruplar oluşturulur."),
        AnswerItem(20, "B", "Eleştirel Düşünmede <b>sol beyin etkindir</b> ve yaklaşım analitik, nesnel ve odaklama (derinleşme) esaslıdır; yaratıcı düşünme ise sağ beyin ve yayma (genişleme) odaklıdır."),
    ]

    return CoursePack(
        course_code="İLKE & YÖNTEM",
        title='Öğretim <span class="accent-word">İlke</span> ve Yöntemleri',
        subtitle="Öğrenme Kuramlarından Öğretim Yöntem, Teknik ve Düşünme Biçimlerine Final Özeti",
        description=(
            "Tam Öğrenme'den Programlı Öğrenmeye, Probleme Dayalı ve Proje Tabanlı Öğrenmeden "
            "Yapılandırmacılığa; İşbirlikli, Aktif ve Anlamlı Öğrenmeden Gagne ve Glasser'ın modellerine; "
            "Çoklu Zeka Kuramı'ndan Carroll, Slavin, Bandura ve Nunley'in modellerine; Anlatım, Tartışma ve "
            "Problem Çözme gibi öğretim yöntemlerinden Altı Şapkalı Düşünme, Beyin Fırtınası ve Mikro "
            "Öğretim gibi tekniklere ve son olarak Yaratıcı, Eleştirel, Yansıtıcı, Analitik ve Metabilişsel "
            "düşünme biçimlerine uzanan kapsamlı bir Öğretim İlke ve Yöntemleri final özeti."
        ),
        theme="burgundy",
        theme_color="#863C5E",
        icon_text="İ",
        chapters=chapters,
        glossary=glossary,
        test_title="Genel Değerlendirme Testi",
        test_subtitle="Öğrenme kuramlarından öğretim yöntem, teknik ve düşünme biçimlerine kapsamlı çoktan seçmeli test",
        test_instructions="Aşağıdaki sorularda beş seçenekten yalnızca birini işaretleyiniz. Süre: 30 dakika.",
        test_questions=test_questions,
        answer_key_intro="Her sorunun doğru cevabı ve kısa gerekçesi aşağıda yer almaktadır.",
        answer_key_items=answer_key_items,
        overview_lead=(
            "Bu ders, eğitimde başarının şans eseri değil doğru stratejilerin ürünü olduğu ilkesinden yola "
            "çıkarak; <b>öğrenme-öğretme kuram ve modellerinden</b> (Tam Öğrenme, Programlı Öğrenme, "
            "Yapılandırmacılık, Çoklu Zeka, Basamaklı Öğretim...), <b>öğretim yöntemlerine</b> (Anlatım, "
            "Tartışma, Problem Çözme, Proje...), <b>öğretim tekniklerine</b> (Altı Şapkalı Düşünme, Beyin "
            "Fırtınası, Mikro Öğretim, Keller Planı...) ve son olarak <b>düşünme biçimlerine</b> (Yaratıcı, "
            "Eleştirel, Yansıtıcı, Analitik, Metabilişsel) uzanan altı bölümlük kapsamlı bir sınav hazırlık "
            "rehberidir."
        ),
        overview_cards=[
            {"title": "Öğrenme-Öğretme Kuram ve Modelleri I", "text": "Tam Öğrenme, Programlı Öğrenme, Probleme Dayalı ve Proje Tabanlı Öğrenme, Yapılandırmacılık."},
            {"title": "Öğrenme-Öğretme Kuram ve Modelleri II", "text": "İşbirlikli, Aktif ve Anlamlı Öğrenme; Gagne'nin Öğretim Durumları ve Glasser'ın Temel Öğretme Modeli."},
            {"title": "Öğrenme-Öğretme Kuram ve Modelleri III", "text": "Yaşam Boyu ve Beyin Temelli Öğrenme, Çoklu Zeka Kuramı, Carroll, Slavin, Bandura ve Nunley'in modelleri."},
            {"title": "Öğretim Yöntemleri", "text": "Anlatım, Tartışma, Soru-Cevap, Örnek Olay, Gösterip Yaptırma, Problem Çözme, Proje ve Laboratuvar yöntemleri."},
            {"title": "Öğretim Teknikleri", "text": "Altı Şapkalı Düşünme, Altı Ayakkabılı Uygulama, İstasyon, Beyin Fırtınası, Mikro Öğretim, Keller Planı ve Tutor Destekli Öğretim."},
            {"title": "Düşünme Biçimleri", "text": "Yaratıcı, Eleştirel, Yansıtıcı, Analitik ve Metabilişsel (Üstbiliş) düşünme biçimleri."},
        ],
        overview_flow=[
            ("Kuram ve Modeller I", "Tam Öğrenme, Programlı Öğrenme, Yapılandırmacılık"),
            ("Kuram ve Modeller II", "İşbirlikli, Aktif, Anlamlı Öğrenme, Gagne, Glasser"),
            ("Kuram ve Modeller III", "Çoklu Zeka, Carroll, Slavin, Bandura, Nunley"),
            ("Öğretim Yöntemleri", "Anlatım, Tartışma, Problem Çözme, Proje"),
            ("Öğretim Teknikleri", "Altı Şapka, Beyin Fırtınası, Mikro Öğretim"),
            ("Düşünme Biçimleri", "Yaratıcı, Eleştirel, Yansıtıcı, Analitik, Metabilişsel"),
        ],
        overview_note=(
            "Bu kitaptaki <b>mavi 'Dikkat / Püf Noktası'</b> kutucukları, sınavlarda en sık karıştırılan "
            "kavram çiftlerini (Tam Öğrenme ↔ Programlı Öğrenme, Proje Tabanlı ↔ Probleme Dayalı Öğrenme, "
            "Rol Oynama ↔ Drama, Benzetim ↔ Analoji, Altı Şapka ↔ Altı Ayakkabı gibi) işaretler; sınav "
            "sorularının büyük bölümü tam da bu ayrımlar üzerine kuruludur."
        ),
    )
