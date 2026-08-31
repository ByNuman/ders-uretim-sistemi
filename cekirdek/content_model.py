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
DERS ÜRETİM SİSTEMİ — İçerik Veri Modeli
==========================================
Bu modül, herhangi bir dersin görsel ders notu kitabına dönüştürülmesi için
kullanılan ortak şemayı tanımlar. Tasarım (HTML/CSS) sabittir; her ders bu
şemaya veri doldurarak farklı bir kitap üretir.

Önceki (ChatGPT tabanlı) sistemin tespit edilen zaaflarını gidermek için
buradaki modelde bilinçli olarak şu kurallar var:

1. TEK KAYNAK İLKESİ: Bir kişinin doğum/ölüm tarihi, eseri gibi bilgiler
   sadece Person nesnesinde TANIMLANIR. Sözlük, eşleştirme tablosu, biyografi
   kartı gibi her yer aynı Person nesnesine referans verir — aynı bilgi iki
   yerde elle iki kez yazılmaz. Böylece "iki farklı sayfada iki farklı tarih"
   türü hatalar yapısal olarak imkansız hale gelir.

2. OTOMATİK SAYIM: Kapaktaki "X Bölüm / Y Kavram" gibi istatistikler elle
   yazılmaz; build.py içerik listesinin uzunluğundan otomatik hesaplar.

3. AÇIK KAYNAK ATIFI: Her Concept, hangi bölümden geldiğini chapter_ref
   üzerinden otomatik alır — elle "3. Bölüm" yazılıp bölüm numarası
   değişince güncellenmeyi unutma riski ortadan kalkar.
"""

from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Temel / paylaşılan varlıklar
# ---------------------------------------------------------------------------

@dataclass
class Person:
    """Bir düşünür/bilim insanı/yazar. TEK KAYNAK: tarihler burada tanımlanır,
    başka hiçbir yerde elle tekrar yazılmaz."""
    id: str                      # örn. "freud" — Concept/Chapter'lardan referans için
    name: str                    # "Sigmund Freud"
    years: str                   # "1856–1939" ya da tek tarih "1856"
    tagline: str                 # kartta isim altında tek satır etiket
    bio: list[str]               # biyografi maddeleri (madde imli)
    key_work: Optional[str] = None   # başyapıtı / en önemli eseri
    initials: Optional[str] = None   # avatar baş harfleri; boşsa isimden türetilir

    def avatar(self) -> str:
        if self.initials:
            return self.initials
        parts = [p for p in self.name.replace(".", " ").split() if p]
        return "".join(p[0] for p in parts[:2]).upper()


@dataclass
class KeyTerm:
    """Bölüm başında verilen 4'lü tanım kutularından biri."""
    term: str
    definition: str


@dataclass
class Callout:
    """Renkli vurgu kutusu. kind: 'focus' | 'caution' | 'insight' | 'route'"""
    kind: str
    title: str
    text: str


@dataclass
class FlowStep:
    title: str
    text: str = ""


@dataclass
class FlowDiagram:
    """Yatay ok'lu süreç/aşama şeması."""
    steps: list[FlowStep]
    caption: Optional[str] = None


@dataclass
class ComparisonTable:
    caption: str
    headers: list[str]
    rows: list[list[str]]


@dataclass
class InfoCard:
    """Küçük 2-3'lü istatistik/bilgi kartı grid'i (ör. 'Saint-Simon ile çalışma: 7 yıl')."""
    title: str
    text: str
    badge: Optional[str] = None   # sağ üstte küçük sayı/etiket


@dataclass
class Ayah:
    """Bir ayet-i kerime kartı: orijinal Arapça metin + referans + Türkçe meal + etimoloji.
    Arapça metin DejaVu Sans ile (tam GSUB/Arabic-shaping desteği doğrulanmış) render edilir."""
    reference: str        # "Lokmân 17" gibi
    arabic: str            # orijinal Arapça metin (RTL render edilir)
    meal: str               # Türkçe akademik meal
    etymology: str = ""      # kilit etimoloji notu (opsiyonel)


@dataclass
class Place:
    """Haritadaki tek bir işaret: şehir noktası ya da komşu bölge etiketi.

    Koordinat GERÇEKTİR ve doğrulanabilir olmalıdır (WGS84, ondalık derece).
    GeoJSON düzeniyle uyum için sıra `lon, lat`'tır — enlem/boylamı ters
    yazmak haritayı sessizce bozar, yazarken dikkat edin.
    """
    name: str
    lon: float                 # doğu +, batı -
    lat: float                 # kuzey +, güney -
    sag: bool = True           # etiket noktanın sağında mı yazılsın (kalabalıkta False yapın)


@dataclass
class MapBox:
    """Bölümün yanında duran coğrafi harita kutusu.

    Harita BUILD SIRASINDA, gerçek kartografik veriden çizilir
    (`cekirdek/harita_cizim.py`): kıyı/göl/nehir katmanları Natural Earth
    1:50m (kamu malı), şehirler aşağıdaki gerçek koordinatlar. Üretim
    ücretsiz ve deterministiktir; bir görüntü modeline sorulmaz.

    Alanlar:
        region      Kutunun tanımladığı devlet/bölge adı (Türkçe)
        bbox        (batı, güney, doğu, kuzey) ondalık derece — haritanın çerçevesi
        cities      list[Place] — kırmızı nokta + etiket
        neighbors   list[Place] — gri metin etiketi (nokta yok); "\\n" ile satır böl
        territory   list[list[(lon, lat)]] — YAKLAŞIK alan poligon(lar)ı

    `territory` DÜRÜSTLÜK MESELESİDİR: ortaçağ siyasi sınırları için serbest
    ve yetkeli bir veri kümesi yoktur (Natural Earth bugünün sınırlarıdır,
    CShapes 1886'da başlar, Euratlas lisanslıdır). Poligon elle, kaba hatlarla
    yazılır ve kutuda HER ZAMAN "yaklaşık" ibaresiyle görünür (`source`).
    Sahte bir atlas künyesi (sayfa numaralı uydurma atıf) YAZMAYIN.

    ÖNEMLİ: cities/neighbors listelerine yalnızca ham kaynakta GEÇEN yer
    adlarını yazın. Harita, metinde olmayan bir şehri göstermemelidir.
    Bütün etiketler TÜRKÇE yazılır ("Gürgenç", "Semerkant", "Kara-Hıtaylar").
    """
    region: str
    bbox: tuple = ()                                          # (batı, güney, doğu, kuzey)
    cities: list = field(default_factory=list)                # list[Place]
    neighbors: list = field(default_factory=list)             # list[Place]
    territory: list = field(default_factory=list)             # list[list[(lon, lat)]]
    # ÇOK KATMANLI alan: bir devletin dönem dönem genişlemesi. Her katman
    # {"halkalar": [[(lon,lat), ...]], "etiket": "1240'a kadar"} biçimindedir
    # ve liste ESKİDEN YENİYE sıralanır; çizim en eskiyi en koyu tonla basar
    # ve etiketleri HTML lejanta taşır. `territory` ile birlikte KULLANILMAZ.
    #
    # Gerek: tarihî haritaların çoğu tek sınır değil, genişleme evreleri
    # gösterir (Rum Selçuklu 4 bant, Moğol İmparatorluğu 7 bant). Hepsini tek
    # poligona indirmek kaynaktaki asıl bilgiyi -- NE ZAMAN nereye yayıldığını
    # -- yok eder.
    katmanlar: list = field(default_factory=list)
    label: str = "Coğrafi konum"                              # kutu üstündeki başlık etiketi
    caption: str = ""                                         # kutunun altındaki açıklama
    source: str = ("Sınırlar yaklaşıktır (temsilî). Coğrafya: Natural Earth "
                   "1:50m, kamu malı.")

    # --- Hazır Commons haritası (opsiyonel) ---
    # Doluysa harita SIFIRDAN ÇİZİLMEZ: Wikimedia Commons'tan alınmış
    # profesyonel bir tarihî harita derse uyarlanır (lejant Türkçeye, renkler
    # temaya). O zaman bbox/cities/territory KULLANILMAZ ve `source` alanı
    # `CommonsKaynak.atif` ile EZİLİR -- CC BY-SA atfı zorunludur, bkz.
    # cekirdek/harita_commons.py ve assets/harita/commons/LISANS.md.
    commons: object = None                                    # CommonsKaynak | None

    # --- build.py tarafından doldurulur (elle yazılmaz) ---
    svg: str = ""             # çizilmiş harita; boşsa veri eksiktir (yer tutucu basılır)
    gorsel_oran: str = "4 / 3"
    # Haritanın ALTINA HTML olarak basılan lejant: [(renk_hex, "etiket"), ...].
    # Yalnızca `CommonsKaynak.lejant=True` iken dolar; lejant o zaman kaynak
    # SVG'den sökülüp buraya taşınır, böylece harita küçültülünce lejant
    # onunla birlikte küçülmez (bkz. cekirdek/harita_commons.py).
    lejant: list = field(default_factory=list)


@dataclass
class BulletBlock:
    """Numaralı alt-başlık altındaki düz anlatım: başlık + madde listesi."""
    number: int
    title: str
    bullets: list[str]           # her biri düz metin; "**vurgu**" markdown-benzeri kalın için kullanılabilir
    subtitle: Optional[str] = None


def _item_kind(obj) -> str:
    """Bir içerik nesnesini şablonun tanıdığı item tipine çevirir.

    `ChapterPage.add_map(..., yan=[...])` için gerekir: orada bloklar
    `.add_block()` gibi tip adıyla değil, doğrudan nesne olarak verilir.
    """
    if isinstance(obj, BulletBlock):
        return "block"
    if isinstance(obj, Callout):
        return "callout"
    if isinstance(obj, ComparisonTable):
        return "table"
    if isinstance(obj, FlowDiagram):
        return "flow"
    if isinstance(obj, Person):
        return "person"
    if isinstance(obj, list) and obj and all(isinstance(x, KeyTerm) for x in obj):
        return "terms"
    raise TypeError(
        f"add_map(yan=[...]) bu tipi tanımıyor: {type(obj).__name__}. "
        "Desteklenenler: BulletBlock, Callout, ComparisonTable, FlowDiagram, "
        "Person, list[KeyTerm]."
    )


@dataclass
class ChapterPage:
    """Bir bölümün TEK fiziksel sayfası. items sırayla render edilir.
    Her item şu tuple biçimindedir: (tip, veri)
    tip ∈ {"terms","person","person_row","block","callout","flow","table",
           "info_cards","summary","continue_tag"}
    Yükseklik önceden bilinemediği için (CSS render-zamanlı) sayfa bölünmesine
    içerik yazarken KENDİM karar veririm — bu, önceki sistemdeki taşma/kesilme
    risklerini ortadan kaldırır.
    """
    items: list[tuple] = field(default_factory=list)
    continue_tag: Optional[str] = None   # "1. BÖLÜM · DEVAM" gibi ikinci+ sayfa etiketi

    def add_terms(self, terms: list[KeyTerm]):
        self.items.append(("terms", terms)); return self
    def add_person(self, person: Person):
        self.items.append(("person", person)); return self
    def add_person_row(self, persons: list[Person]):
        self.items.append(("person_row", persons)); return self
    def add_block(self, block: BulletBlock):
        self.items.append(("block", block)); return self
    def add_callout(self, callout: Callout):
        self.items.append(("callout", callout)); return self
    def add_flow(self, flow: FlowDiagram):
        self.items.append(("flow", flow)); return self
    def add_table(self, table: ComparisonTable):
        self.items.append(("table", table)); return self
    def add_ayat(self, title: str, ayat: list[Ayah]):
        self.items.append(("ayat", (title, ayat))); return self
    def add_info_cards(self, title: str, cards: list[InfoCard]):
        self.items.append(("info_cards", (title, cards))); return self
    def add_summary(self, text: str):
        self.items.append(("summary", text)); return self

    def add_map(self, harita: "MapBox", yan: list | None = None, taraf: str = "sag"):
        """Harita kutusunu, YANINDAKİ metin bloklarıyla birlikte iki sütuna koyar.

            .add_map(MapBox(...), yan=[BulletBlock(1, "Coğrafi Bağlam", [...])])

        `yan` listesindeki nesneler metin sütununda, normal sayfa akışındaki
        gibi render edilir (BulletBlock, Callout, ComparisonTable, KeyTerm
        listesi, Person, FlowDiagram desteklenir). `taraf` "sag" ya da "sol":
        haritanın hangi sütuna düşeceğini belirler.

        Bu çağrı TEK bir item üretir; ölçüm/dengeleme araçları (tools/olcum.py,
        tools/dengele.py) onu bölünemez tek blok olarak görür.
        """
        if taraf not in ("sag", "sol", "tam"):
            raise ValueError(f"taraf 'sag', 'sol' veya 'tam' olmalı, verilen: {taraf!r}")
        yan_items = [(_item_kind(o), o) for o in (yan or [])]
        self.items.append(("mapsplit", (harita, yan_items, taraf)))
        return self


@dataclass
class Chapter:
    number: int
    title: str
    subtitle: str
    pages: list[ChapterPage] = field(default_factory=list)
    key_terms: list[KeyTerm] = field(default_factory=list)   # sadece concept_count() için tutulur

    def concept_count(self) -> int:
        return len(self.key_terms)

    def page_count(self) -> int:
        return len(self.pages)


@dataclass
class Concept:
    """Sözlük satırı. chapter_ref otomatik "N. Bölüm" biçimine dönüştürülür."""
    term: str
    definition: str
    context: str                 # "Sigmund Freud" gibi bağlam etiketi
    chapter_ref: int             # hangi bölümden geldiği (otomatik "N. Bölüm" yazılır)


@dataclass
class QAItem:
    question: str
    answer: str


@dataclass
class DistinctionPair:
    """'En sık karıştırılanlar' kartı: A ↔ B ve farkları."""
    left: str
    right: str
    text: str


@dataclass
class MatchRow:
    key: str          # düşünür / kavram
    detail: str        # temel kavram/teori
    reference: str      # öne çıkan eser/ifade


@dataclass
class TestQuestion:
    """20 soruluk çoktan seçmeli testte tek bir soru."""
    number: int
    stem: str
    options: dict            # {"A": "...", "B": "...", "C": "...", "D": "...", "E": "..."}


@dataclass
class AnswerItem:
    """Cevap anahtarında TestQuestion.number ile eşleşen tek bir çözüm."""
    number: int
    correct: str              # "A".."E"
    explanation: str


@dataclass
class BookPack:
    """BİRLEŞİK KİTAP — 13-14 dersin tek ciltte toplanmış hali.

    Ders içeriğini KOPYALAMAZ; sadece hangi derslerin hangi sırayla
    birleşeceğini ve kitabın kendi kimliğini (kapak, önsöz vb.) tutar.
    Dersler her zaman kendi content/<slug>.py dosyalarından taze okunur —
    bir derste yapılan düzeltme, kitap yeniden derlendiğinde otomatik gelir.
    (Kitabın ön kısmı — kapak/künye/önsöz/rehber/ana içindekiler — Faz 2'de
    eklenecek; bu sınıf o alanlarla genişletilecek.)
    """
    title: str
    subtitle: str
    description: str
    course_modules: list[str]          # ["content.tefsir2", "content.psikoloji", ...] — SIRA önemlidir
    theme: str = "slate"               # kitabın kendi ön kısmı için (dersler kendi temasını korur)
    theme_color: Optional[str] = None
    icon_text: str = "K"

    # --- Ön kısım (kapak / künye / önsöz / rehber / ana içindekiler / harita) ---
    cover_kicker: str = "Görsel Ders Notu Kitabı · Dönem Cildi"
    cover_code: str = ""                          # kapakta başlığın üstündeki küçük etiket
    imprint_rows: list[tuple] = field(default_factory=list)   # [("Dönem", "2025-2026 Bahar"), ...]
    imprint_note: str = ""
    preface_lead: str = ""                        # önsözün koyu zeminli giriş paragrafı
    preface_cards: list[tuple] = field(default_factory=list)  # [(başlık, metin), ...] 2x2 kart
    preface_note: str = ""                        # önsöz altındaki vurgu kutusu metni
    guide_lede: str = ""
    guide_note: str = ""
    toc_lede: str = ""
    map_lede: str = ""
    map_note: str = ""

    def course_count(self) -> int:
        return len(self.course_modules)


@dataclass
class CoursePack:
    """Bir dersin tüm görsel kitabı."""
    course_code: str            # "PSİ 102" gibi küçük üst etiket (opsiyonel)
    title: str
    subtitle: str
    description: str
    theme: str                  # tema anahtarı: "indigo" | "burgundy" | "forest" ... (theme_color boşsa kullanılır)
    icon_text: str               # kapaktaki daire logo harfi/sembolü
    chapters: list[Chapter]
    glossary: list[Concept]
    theme_color: Optional[str] = None   # hex (ör. "#7A2438") verilirse `theme` yerine bunu kullan — sınırsız tema
    distinctions: list[DistinctionPair] = field(default_factory=list)   # LEGACY — yeni derslerde kullanmayın
    match_table: list[MatchRow] = field(default_factory=list)           # LEGACY — yeni derslerde kullanmayın
    qa_items: list[QAItem] = field(default_factory=list)                 # LEGACY — yeni derslerde kullanmayın
    persons: dict = field(default_factory=dict)   # id -> Person (tek kaynak kayıt defteri)
    subtitle_short: str = ""
    # --- Genel Bakış sayfası içeriği ---
    overview_lead: str = ""                          # üstteki koyu-zemin özet paragrafı
    overview_cards: list[dict] = field(default_factory=list)   # [{"title":..,"text":..}, ...] 3'lü grid
    overview_flow: list[tuple] = field(default_factory=list)   # [(başlık, alt_metin), ...] yatay ok akışı
    overview_note: str = ""                           # alt kısımdaki "Sınavda Ana Ayrım" callout metni
    # --- Test + Cevap Anahtarı (STANDART sınav bölümü — distinctions/match/qa'nın yerini alır) ---
    test_title: str = "Genel Değerlendirme Testi"
    test_subtitle: str = ""
    test_instructions: str = "Aşağıdaki sorularda beş seçenekten yalnızca birini işaretleyiniz."
    test_questions: list[TestQuestion] = field(default_factory=list)
    answer_key_intro: str = "Her sorunun doğru cevabı ve kısa gerekçesi aşağıda yer almaktadır."
    answer_key_items: list[AnswerItem] = field(default_factory=list)
    # --- Çıktı klasörü ---
    # Bu dersin, dönem ağacındaki klasör adı (kaynaklar/ders_kaynaklari/<ders_klasoru>/,
    # kaynaklar/özetlenmiş_dersler/<ders_klasoru>/, gorsel_ders_notlari/<ders_klasoru>/).
    # Ders programındaki BÜYÜK HARFLİ tam ad yazılır, ör. "KELÂM TARİHİ".
    # Boş bırakılırsa build.py başlıktan türetilen slug'a düşer (geriye dönük uyumluluk).
    ders_klasoru: str = ""

    # --- Kapaktaki sınav etiketi ---
    # Kapak kickerinde ("Görsel Ders Notu Kitabı · <X> Özeti"), kapak istatistik
    # kutusunda ve alt bilgide görünen sınav adı. Varsayılan "Final"dir; vize
    # kitapları için "Vize" yazılır. LEGACY "Sınav Hazırlık" bölümünün pageband
    # etiketi de ("<X> Tekrarı") bu değerden türetilir.
    sinav_etiketi: str = "Final"

    # --- Otomatik hesaplanan istatistikler (elle yazılmaz) ---
    def chapter_count(self) -> int:
        return len(self.chapters)

    def concept_count(self) -> int:
        return len(self.glossary)

    def total_pages_estimate(self) -> int:
        # kapak + içindekiler + genel bakış + bölümler(ortalama 2 sayfa) + sözlük + sınav hazırlık
        return 3 + len(self.chapters) * 2 + 2
