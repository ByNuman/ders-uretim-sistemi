# -*- coding: utf-8 -*-
"""
BİRLEŞİK KİTAP TANIMI
=====================
Hangi derslerin hangi SIRAYLA tek kitapta birleşeceğini ve kitabın kendi
ön kısmını (kapak, künye, önsöz, sayfa rehberi, ana içindekiler, ders
haritası) burası belirler.

Yeni bir ders üretildiğinde tek yapılacak iş, COURSE_MODULES listesine bir
satır eklemektir — kitap kendini baştan numaralar, ana içindekilerini,
haritasını, istatistiklerini ve yer imlerini otomatik günceller.

    python build_kitap.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from content_model import BookPack


# Ders sırası — kitapta bu sırayla yer alırlar.
COURSE_MODULES = [
    "content.tefsir2",
    "content.islam_tarihi_3",
    "content.kelam_tarihi",
    "content.sanat_tarihi",
    "content.felsefe_tarihi_2",
    "content.cagdas_felsefe",
    "content.psikoloji",
    "content.sosyoloji",
    "content.edebiyat",
    "content.ogretim_ilke_yontem",
    "content.ogretim_teknolojileri",
]


def get_book() -> BookPack:
    return BookPack(
        title="Dönem Ders Notları Kitabı",
        subtitle="Dönemin bütün derslerinin görsel ders notları tek ciltte",
        description=(
            "Her ders kendi kapağı, içindekileri, genel bakışı, numaralı bölümleri, "
            "anahtar kavramlar sözlüğü ve çözümlü testiyle bu kitapta eksiksiz yer "
            "alır. Sayfa numaraları kitabın başından sonuna kesintisiz akar."
        ),
        course_modules=COURSE_MODULES,
        theme="slate",
        theme_color="#2E3B4E",
        icon_text="D",
        cover_kicker="Görsel Ders Notu Kitabı · Dönem Cildi",
        cover_code="FİNAL DÖNEMİ",

        # --- Künye ---
        imprint_rows=[
            ("Kitap", "Dönem Ders Notları Kitabı"),
            ("Tür", "Görsel ders notu · final sınavı hazırlık cildi"),
            ("Kaynak", "Her dersin kendi ders özeti; içerik doğrudan bu özetlerden çıkarılmıştır"),
            ("Yapı", "Ders başına: kapak · içindekiler · genel bakış · bölümler · sözlük · test · cevap anahtarı"),
            ("Sayfa Düzeni", "A4 · her ders kendi renk temasını korur"),
        ],
        imprint_note=(
            "Bu cilt, derslerin tek tek üretilmiş görsel not kitaplarının birleşimidir. "
            "Bir derste düzeltme yapıldığında kitap yeniden derlenir ve tüm sayfa "
            "numaraları, içindekiler ve yer imleri kendiliğinden güncellenir — "
            "hiçbir numara elle yazılmaz."
        ),

        # --- Önsöz ---
        preface_lead=(
            "Bu kitap baştan sona okunmak için değil, <b>sınavdan önce hızlı ve hedefli "
            "çalışmak</b> için tasarlandı. Her ders bağımsız bir bütündür: bir dersi "
            "çalışırken diğerlerine bakmanız gerekmez. Aradığınız yere ana "
            "içindekilerden ya da PDF'in sol panelindeki yer imi ağacından tek "
            "tıkla ulaşabilirsiniz."
        ),
        preface_cards=[
            ("Her ders kendi kitabı",
             "Ders kapağıyla başlar, <b>genel bakış</b> sayfasıyla büyük resmi verir, "
             "numaralı bölümlerle ilerler, kavram sözlüğü ve çözümlü testle biter. "
             "Bir dersin tamamı ardışık sayfalardadır, araya başka ders girmez."),
            ("Renk = ders",
             "Her dersin kendine ait bir rengi vardır; sayfa üstündeki çizgi, tablo "
             "başlıkları ve alt bilgideki sayfa rozeti hep o rengi taşır. Kitabı "
             "hızlı çevirirken hangi derste olduğunuzu <b>renginden</b> anlarsınız."),
            ("Sayfa numaraları tek akış",
             "Numaralar kitabın ilk sayfasından son sayfasına kesintisiz gider. "
             "Ana içindekilerdeki numara ile dersin kendi içindekilerindeki numara "
             "<b>aynı sayfayı</b> gösterir."),
            ("Önce sınav, sonra konu",
             "Zaman darsa dersin sonundaki <b>testten</b> başlayın: yanlış yaptığınız "
             "sorunun çözümü sizi ilgili bölüme yönlendirir. Böylece bildiğiniz "
             "konulara vakit harcamazsınız."),
        ],
        preface_note=(
            "Bir ders için önerilen sıra: <b>Genel Bakış</b> → bölümlerin "
            "<b>Bölüm Özeti</b> kutuları → <b>Anahtar Kavramlar Sözlüğü</b> → "
            "<b>Test</b> → yanlışlarınızın geldiği bölümü baştan okuyun."
        ),

        # --- Sayfa rehberi ---
        guide_lede=(
            "Bütün derslerde aynı görsel dil kullanılır. Bir kutunun rengi ve biçimi, "
            "içindeki bilginin ne işe yaradığını söyler."
        ),
        guide_note=(
            "Bunların dışında bölümlerde <b>kişi kartları</b> (bir düşünürün tarihleri, "
            "eseri ve katkısı tek yerde) ve Tefsir gibi derslerde <b>ayet kartları</b> "
            "(orijinal metin, meali ve kilit kelime açıklaması) yer alır."
        ),

        # --- Ana içindekiler / harita ---
        toc_lede=(
            "Her satır o dersin ilk sayfasına götürür. Sağdaki sayı dersin kitaptaki "
            "başlangıç sayfasıdır."
        ),
        map_lede=(
            "Derslerin kitap içindeki ağırlığı ve yeri. Çubuğun uzunluğu dersin "
            "sayfa sayısıyla orantılıdır."
        ),
        map_note=(
            "Renkler kitabın tamamında sabittir: bir derse ait her sayfa, haritada "
            "o dersin yanında görünen rengi taşır."
        ),
    )
