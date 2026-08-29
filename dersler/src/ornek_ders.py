# -*- coding: utf-8 -*-
#
# Görsel Ders Notu Üretim Sistemi
# Copyright (C) 2026 Numan Gözdaş
#
# Bu program özgür yazılımdır: Özgür Yazılım Vakfı'nın yayımladığı GNU Genel
# Kamu Lisansı'nın 3. sürümü koşulları altında yeniden dağıtabilir ve/veya
# değiştirebilirsiniz.
#
# Bu program yararlı olacağı umuduyla dağıtılmaktadır, ancak HİÇBİR GARANTİ
# VERİLMEZ; SATILABİLİRLİK veya BELİRLİ BİR AMACA UYGUNLUK zımni garantileri
# dahi verilmez. Ayrıntılar için GNU Genel Kamu Lisansı'na bakın.
#
# Lisansın bir kopyasını bu depodaki LICENSE dosyasında bulabilirsiniz;
# ayrıca <https://www.gnu.org/licenses/> adresinden edinebilirsiniz.
#
"""
ÖRNEK DERS — sistemin nasıl kullanıldığını kendi üzerinden anlatan ders.
=======================================================================
Bu dosya iki iş görür:

1. **Kurulum doğrulaması.** Depoyu yeni klonlayan biri
   `python build.py ornek_ders` komutuyla eksiksiz bir PDF üretebiliyorsa
   kurulum tamamdır (bkz. KURULUM.md, 5. adım).

2. **Şablon.** Kendi dersinizi yazarken bu dosyayı kopyalayıp içeriğini
   değiştirin. Buradaki her yapı (KeyTerm, BulletBlock, ComparisonTable,
   Callout, FlowDiagram, Concept, TestQuestion, AnswerItem) gerçek bir derste
   nasıl kullanılıyorsa öyle kullanılmıştır.

İçeriği tamamen özgündür — sistemin kendi belgelerinden yazılmıştır, hiçbir
ders kitabından türetilmemiştir; bu yüzden GPL kapsamındadır (depodaki gerçek
ders modüllerinin aksine, bkz. TELIF.md).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from cekirdek.content_model import (                                      # noqa: E402
    KeyTerm, Callout, FlowStep, FlowDiagram, ComparisonTable,
    BulletBlock, Chapter, ChapterPage, Concept, CoursePack,
    TestQuestion, AnswerItem,
)


def get_pack() -> CoursePack:
    # =====================================================================
    # 1. BÖLÜM
    # =====================================================================
    ch1 = Chapter(
        number=1,
        title="Sistem Nasıl Çalışır",
        subtitle="Ham metinden baskıya hazır PDF'e giden yol",
        key_terms=[
            KeyTerm("CoursePack", "Bir dersin tamamını tutan veri nesnesi; "
                                  "her ders modülünün <b>get_pack()</b> fonksiyonu bunu döndürür."),
            KeyTerm("Chapter", "Numaralı bir bölüm. Kendi başlığı, alt başlığı ve "
                               "tam 4 anahtar terimi vardır."),
            KeyTerm("ChapterPage", "Bir bölümün TEK fiziksel sayfası. İçerik blokları "
                                   "zincirlenebilir <b>.add_*()</b> metotlarıyla eklenir."),
            KeyTerm("Tema rengi", "Tek bir hex renk; kapak gradyanından tablo başlığına "
                                  "kadar bütün tonlar ondan türetilir."),
        ],
    )
    ch1.pages.append(
        ChapterPage()
        .add_terms(ch1.key_terms)
        .add_block(BulletBlock(1, "İçerik koda yazılır, tasarıma değil", [
            "Ders içeriği HTML ya da CSS'te değil, <b>Python veri modelinde</b> tanımlanır.",
            "Tasarım tek bir yerde durur: <b>templates/</b>. İçerik ise her ders için ayrı bir modülde.",
            "Bu ayrım sayesinde tasarımda yapılan bir düzeltme <b>bütün derslere birden</b> uygulanır.",
            "Yeni bir ders eklemek, yeni bir <b>.py</b> dosyası yazmaktan ibarettir.",
        ]))
        .add_flow(FlowDiagram([
            FlowStep("Ham metin", "Ders kaynağı"),
            FlowStep("src/*.py", "CoursePack"),
            FlowStep("HTML", "Jinja şablonu"),
            FlowStep("PDF", "Chromium"),
            FlowStep("CMYK", "Ghostscript (--cmyk)"),
        ], caption="Üretim hattının beş adımı. Her adım bir öncekinin çıktısını girdi alır."))
    )
    ch1.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Üç klasörün rolü — birbirinin yerine geçmez",
            ["Klasör", "Rolü", "Kim yazar?"],
            [
                ["<b>kaynaklar/ders_kaynaklari</b>", "Ham ders metni, kaynak PDF", "Siz (girdi)"],
                ["<b>kaynaklar/özetlenmiş_dersler</b>", "Ham metinden çıkarılan yazılı özet", "Siz (ara ürün)"],
                ["<b>src/</b>", "Dersin Python içerik modülü", "Siz (asıl içerik)"],
                ["<b>gorsel_ders_notlari/</b>", "Üretilmiş PDF ve HTML", "build.py (çıktı)"],
            ]))
        .add_callout(Callout(
            "focus", "En sık yapılan hata",
            "<b>özetlenmiş_dersler/</b> klasörü build.py'nin ÇIKTISI değil, "
            "<b>GİRDİSİDİR</b>. Üretilen PDF'ler her zaman "
            "<b>gorsel_ders_notlari/</b> altına düşer."))
        .add_summary(
            "Sistem, içerik ile tasarımı birbirinden ayırır. Siz yalnızca içeriği "
            "yazarsınız; sayfa düzeni, tipografi, renk ve baskı geometrisi sizin "
            "sorumluluğunuz değildir.")
    )

    # =====================================================================
    # 2. BÖLÜM
    # =====================================================================
    ch2 = Chapter(
        number=2,
        title="Bir Ders Modülü Yazmak",
        subtitle="get_pack() fonksiyonunun anatomisi",
        key_terms=[
            KeyTerm("get_pack()", "Modülün dışa verdiği <b>tek</b> fonksiyon. "
                                  "Parametre almaz, bir CoursePack döndürür."),
            KeyTerm("ders_klasoru", "Çıktının yazılacağı klasörün adı. "
                                    "kaynaklar/ altındaki ders klasörüyle birebir aynı olmalıdır."),
            KeyTerm("Concept", "Kavramlar sözlüğünün bir satırı. <b>chapter_ref</b> "
                               "alanı geçerli bir bölüm numarasına işaret etmelidir."),
            KeyTerm("TestQuestion", "Çoktan seçmeli bir soru. Seçenekler 4 ya da 5 "
                                    "anahtarlı bir sözlüktür."),
        ],
    )
    ch2.pages.append(
        ChapterPage()
        .add_terms(ch2.key_terms)
        .add_block(BulletBlock(1, "Bölümleri planlama", [
            "Ham metnin <b>kendi başlık yapısını</b> takip edin; yapay bölümleme uydurmayın.",
            "Bölüm başına ortalama <b>2 sayfa</b> hedefleyin (1-3 sayfa kabul edilebilir).",
            "Her bölüm tam <b>4 anahtar terim</b> içermelidir — tasarım 2x2 ızgara varsayar.",
            "Yoğun bölümleri en baştan birkaç <b>ChapterPage</b>'e bölün.",
        ]))
        .add_block(BulletBlock(2, "Sınav bölümünü yazma", [
            "<b>test_questions</b> ve <b>answer_key_items</b> listeleri aynı uzunlukta ve aynı sırada olmalıdır.",
            "Her <b>AnswerItem.correct</b> değeri, o sorunun seçenek anahtarlarından biri olmalıdır.",
            "Numaralandırma 1'den başlar ve boşluksuz artar; <b>validate()</b> bunu denetler.",
        ]))
    )
    ch2.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Sayfaya eklenebilecek bloklar",
            ["Metot", "Ne üretir"],
            [
                ["<b>.add_terms()</b>", "Bölüm başındaki 4'lü terim kutusu"],
                ["<b>.add_block()</b>", "Numaralı alt başlık + madde listesi"],
                ["<b>.add_table()</b>", "Başlıklı karşılaştırma tablosu"],
                ["<b>.add_callout()</b>", "Renkli vurgu kutusu (focus / caution / insight / route)"],
                ["<b>.add_flow()</b>", "Yatay oklu süreç şeması"],
                ["<b>.add_summary()</b>", "Bölüm sonu özet kutusu"],
            ]))
        .add_callout(Callout(
            "caution", "Aşırı yüklü sayfa",
            "Tek bir sayfaya terim kutusu + iki büyük tablo + callout + özet "
            "koymak neredeyse her zaman <b>taşmaya</b> yol açar. Kesin bir sınır "
            "yoktur; derleyin, taşma uyarısını okuyun, gerekirse bölün."))
        .add_summary(
            "Bir ders modülü yazmak, veri yapılarını doldurmaktan ibarettir. "
            "Doğru doldurulup doldurulmadığını build.py derleme sırasında "
            "otomatik denetler.")
    )

    # =====================================================================
    # 3. BÖLÜM
    # =====================================================================
    ch3 = Chapter(
        number=3,
        title="Derleme ve Denetim",
        subtitle="Taşmayı yakalamak, sayfaları dengelemek",
        key_terms=[
            KeyTerm("Taşma denetimi", "Her sayfanın gerçek render yüksekliğini "
                                      "fiziksel sayfa sınırıyla karşılaştıran otomatik kontrol."),
            KeyTerm("dengele.py", "Blok yüksekliklerini ölçüp sayfa bölünmelerini "
                                  "taşmayacak biçimde yeniden dağıtan araç."),
            KeyTerm("Bleed", "Kesim payı. Yalnızca matbaada kesilecek işlerde "
                             "gerekir; fotokopi kipinde 0'dır."),
            KeyTerm("PDF/X-4", "Matbaanın beklediği baskı standardı. Çıktı "
                               "varsayılan olarak RGB'dir; --cmyk ile çevrilir."),
        ],
    )
    ch3.pages.append(
        ChapterPage()
        .add_terms(ch3.key_terms)
        .add_block(BulletBlock(1, "Taşma uyarısı asla görmezden gelinmez", [
            "Sayfalar <b>overflow: hidden</b> ile sınırlıdır: taşan içerik sessizce <b>kesilir</b>.",
            "Build çıktısı ya <b>✓</b> verir ya da hangi sayfanın kaç mm taştığını yazar.",
            "Uyarı varsa önce <b>tools/dengele.py</b> çalıştırın; o çözemezse sayfayı elle bölün.",
            "<b>✓</b> görene kadar derleyin — uyarıyla teslim edilen PDF içerik kaybetmiş demektir.",
        ]))
    )
    ch3.pages.append(
        ChapterPage()
        .add_table(ComparisonTable(
            "Baskı geometrisi",
            ["Ölçü", "Değer"],
            [
                ["Sayfa ölçüsü", "A4 — 210 × 297 mm"],
                ["Taşma payı (bleed)", "0 mm — fotokopide kesim yok"],
                ["Üst / alt kenar", "12 mm / 15 mm"],
                ["Sol / sağ kenar", "12 mm / 12 mm (dar)"],
                ["Gövde punto", "9,6 pt"],
            ]))
        .add_callout(Callout(
            "insight", "Taşma neden bu kadar önemli?",
            "Tarayıcı, sayfa sınıra yaklaştığında elemanları sessizce küçültüp "
            "taşmayı gizleyebiliyordu. Tasarımda <b>flex-shrink: 0</b> zorunlu "
            "kılınarak bu engellendi: artık taşma her zaman <b>gerçek</b> ve "
            "build çıktısında <b>görünür</b>."))
        .add_flow(FlowDiagram([
            FlowStep("Derle", "build.py"),
            FlowStep("Uyarıyı oku", "taşma var mı?"),
            FlowStep("Dengele", "dengele.py"),
            FlowStep("Görsel kontrol", "PNG'ye çevir"),
        ], caption="Bir ders bitene kadar tekrarlanan döngü."))
        .add_summary(
            "Derleme tek komuttur, ama teslim iki denetimden geçer: taşma "
            "denetimi 'içerik kesiliyor mu' sorusunu, görsel kontrol ise "
            "'iyi görünüyor mu' sorusunu cevaplar. Biri diğerinin yerini tutmaz.")
    )

    chapters = [ch1, ch2, ch3]

    # =====================================================================
    # KAVRAMLAR SÖZLÜĞÜ
    # =====================================================================
    glossary = [
        Concept("CoursePack", "Dersin tümünü tutan veri nesnesi.",
                "get_pack() bunu döndürür.", 1),
        Concept("Chapter", "Numaralı bölüm.",
                "Başlık, alt başlık ve 4 anahtar terim taşır.", 1),
        Concept("ChapterPage", "Bir bölümün tek fiziksel sayfası.",
                "Bloklar .add_*() ile eklenir.", 1),
        Concept("Tema motoru", "Tek hex renkten tüm tonları türetir.",
                "theme_engine.py.", 1),
        Concept("ders_klasoru", "Çıktı klasörünün adı.",
                "kaynaklar/ altındakiyle birebir aynı olmalı.", 2),
        Concept("KeyTerm", "Terim kutusu öğesi.",
                "Her bölümde tam 4 tane.", 2),
        Concept("BulletBlock", "Numaralı alt başlık + madde listesi.",
                "Maddeler &lt;b&gt; ile vurgu içerebilir.", 2),
        Concept("ComparisonTable", "Başlıklı karşılaştırma tablosu.",
                "2-3 sütun en iyi sonucu verir.", 2),
        Concept("Callout", "Renkli vurgu kutusu.",
                "focus / caution / insight / route.", 2),
        Concept("TestQuestion", "Çoktan seçmeli soru.",
                "4 ya da 5 seçenekli sözlük.", 2),
        Concept("AnswerItem", "Çözümlü cevap.",
                "Numara ve seçenek soruyla eşleşmeli.", 2),
        Concept("Taşma denetimi", "Sayfa sınırının aşılıp aşılmadığı.",
                "Render yüksekliği ölçülür.", 3),
        Concept("Bleed", "Kesim payı.",
                "Fotokopi kipinde 0 mm.", 3),
        Concept("PDF/X-4", "Baskı öncesi PDF standardı.",
                "--cmyk verilirse üretilir.", 3),
    ]

    # =====================================================================
    # TEST + CEVAP ANAHTARI
    # =====================================================================
    test_questions = [
        TestQuestion(1, "Bir ders modülünün dışa verdiği tek fonksiyon hangisidir?", {
            "A": "build()", "B": "get_pack()", "C": "render()",
            "D": "main()", "E": "validate()"}),
        TestQuestion(2, "Üretilen PDF'ler hangi klasöre yazılır?", {
            "A": "kaynaklar/ders_kaynaklari/", "B": "kaynaklar/özetlenmiş_dersler/",
            "C": "gorsel_ders_notlari/", "D": "src/", "E": "templates/"}),
        TestQuestion(3, "Her bölümde kaç anahtar terim bulunmalıdır?", {
            "A": "2", "B": "3", "C": "4", "D": "5", "E": "Sınır yoktur"}),
        TestQuestion(4, "Taşma uyarısı alındığında ilk yapılması gereken nedir?", {
            "A": "Uyarıyı görmezden gelmek", "B": "Punto ve boşlukları küçültmek",
            "C": "tools/dengele.py çalıştırmak", "D": "Sayfa boyutunu büyütmek",
            "E": "İçeriği silmek"}),
        TestQuestion(5, "Üretilen sayfanın ölçüsü nedir?", {
            "A": "A4 (210 × 297 mm)", "B": "175 × 250 mm", "C": "181 × 256 mm",
            "D": "148 × 210 mm", "E": "160 × 240 mm"}),
        TestQuestion(6, "Bir dersin tema rengi nasıl belirlenir?", {
            "A": "Her ton tek tek elle yazılır", "B": "Tek bir hex renkten türetilir",
            "C": "Rastgele seçilir", "D": "Şablonda sabittir",
            "E": "Ders adının uzunluğuna göre"}),
        TestQuestion(7, "özetlenmiş_dersler/ klasörünün rolü nedir?", {
            "A": "build.py'nin çıktısıdır", "B": "build.py'nin girdisidir",
            "C": "Geçici dosyalar içindir", "D": "Şablonları barındırır",
            "E": "Yalnızca yedektir"}),
        TestQuestion(8, "Bleed (taşma payı) neden gereklidir?", {
            "A": "Sayfa numaraları için", "B": "Cilt payı bırakmak için",
            "C": "Kesimde beyaz çizgi oluşmasını önlemek için",
            "D": "Dosya boyutunu küçültmek için", "E": "Gerekli değildir"}),
    ]

    answer_key_items = [
        AnswerItem(1, "B", "<b>get_pack()</b> — modül yalnızca bu fonksiyonu dışa verir "
                           "ve parametre almadan bir CoursePack döndürür."),
        AnswerItem(2, "C", "<b>gorsel_ders_notlari/</b> tek gerçek çıktı klasörüdür. "
                           "kaynaklar/ altındakiler girdi ya da ara üründür."),
        AnswerItem(3, "C", "<b>4</b> — tasarım 2x2 bir ızgara varsayar, bu yüzden sayı sabittir."),
        AnswerItem(4, "C", "<b>tools/dengele.py</b> blokları ölçüp sayfa bölünmelerini "
                           "yeniden dağıtır. Punto veya boşluk küçültmek yasaktır: "
                           "tasarım sistemi sabit kalmalıdır."),
        AnswerItem(5, "A", "<b>A4 (210 × 297 mm).</b> Çıktı fotokopiyle çoğaltıldığı "
                           "için kesim payı (bleed) yoktur; render ölçüsü de A4'tür."),
        AnswerItem(6, "B", "<b>theme_color</b> alanına yazılan tek bir hex renkten "
                           "theme_engine.py bütün tonları türetir."),
        AnswerItem(7, "B", "<b>Girdisidir.</b> Ham kaynaktan çıkarılan yazılı özet burada "
                           "durur; build.py onu okuyup görsel kitabı üretir."),
        AnswerItem(8, "C", "Zemin rengi sayfa kenarına kadar bassın diye içerik "
                           "kesim çizgisinin <b>dışına taşırılır</b>; böylece küçük kesim "
                           "kaymalarında beyaz çizgi oluşmaz."),
    ]

    return CoursePack(
        ders_klasoru="ÖRNEK DERS",
        course_code="ÖRNEK DERS",
        title='Görsel Ders Notu <span class="accent-word">Sistemi</span>',
        subtitle="Kendi dersinizi yazmak için başlangıç şablonu",
        description="Bu örnek ders, sistemin kendisini anlatır: bir ders modülünün "
                    "nasıl yazıldığını, hangi blokların kullanılabileceğini ve "
                    "derleme denetimlerinin ne işe yaradığını gösterir.",
        theme="forest",
        theme_color="#2F5D50",
        icon_text="O",
        chapters=chapters,
        glossary=glossary,
        test_title="Genel Değerlendirme Testi",
        test_subtitle="Sistemi doğru anladığınızı kontrol edin",
        test_instructions="Aşağıdaki sorularda beş seçenekten yalnızca birini işaretleyiniz.",
        test_questions=test_questions,
        answer_key_intro="Her sorunun doğru cevabı ve kısa gerekçesi aşağıda yer almaktadır.",
        answer_key_items=answer_key_items,
        overview_lead="Bu sistem, ders içeriği ile sayfa tasarımını birbirinden ayırır. "
                      "Siz yalnızca içeriği Python veri yapılarıyla yazarsınız; sayfa "
                      "düzeni, tipografi, renk ve baskı geometrisi otomatik uygulanır.",
        overview_cards=[
            {"title": "İçerik koddadır", "text": "Ders metni HTML'de değil, Python veri "
                                                 "modelinde tanımlanır."},
            {"title": "Tasarım tektir", "text": "Bütün dersler aynı şablonu paylaşır; "
                                                "bir düzeltme hepsine işler."},
            {"title": "Renk türetilir", "text": "Tek bir hex renkten kapak gradyanı dahil "
                                                "tüm tonlar üretilir."},
            {"title": "Taşma yakalanır", "text": "Sayfaya sığmayan içerik sessizce "
                                                 "kesilmez, build sırasında bildirilir."},
            {"title": "Baskıya hazırdır", "text": "A4 RGB çıktı doğrudan fotokopiye "
                                                  "gider; matbaa için --cmyk yeter."},
            {"title": "Yeniden üretilebilir", "text": "PDF kaybolsa da modül dursun; "
                                                      "tek komutla geri gelir."},
        ],
        overview_flow=[
            ("Kaynak", "Ham ders metni"),
            ("Modül", "src/&lt;ders&gt;.py"),
            ("Derle", "build.py"),
            ("Denetle", "Taşma + görsel"),
        ],
        overview_note="Bu dosyayı kopyalayıp içeriğini değiştirerek kendi dersinizi "
                      "yazabilirsiniz. Yapının tamamı burada örneklenmiştir.",
    )
