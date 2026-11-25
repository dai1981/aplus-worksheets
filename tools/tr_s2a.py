# -*- coding: utf-8 -*-
"""Türkiye 2. sınıf (Maarif Modeli, İlkokul Matematik 2024)。100’e kadar（toplama eldeli, çarpma 5’e kadar tablo, bölme 20’ye kadar kalansız）。短い文、絵を多く。問題関数は tr_p12。"""
from tr_s3a import unit
from tr_common import num
import tr_s3b as B
from tr_p12 import *  # noqa: F401,F403


def setup(rnd):
    B.setup(rnd)


def from_unit(ufun, name):
    d = ufun()
    for _, parts in d["sets"]:
        for m, _n in parts:
            if m.__name__ == name:
                return m
    raise KeyError(name)


def m_say100():
    def f():
        n = ri(21, 99)
        t, o = divmod(n, 10)
        if rnd() < 0.5:
            return mq("Kaç tane küp var?%s" % onluk(t, o), num(n), [num(n + 1), num(n - 1), num(o * 10 + t) if o else num(n + 10), num(t + o)],
                      "%d onluk ve %d birlik: <b>%d</b>." % (t, o, n))
        return mq("Kaç nokta var? (Her onluk çerçevede 10 nokta)%s" % pic(P.tenframe_svg(n, (n + 9) // 10), "%d nokta" % n) if n <= 50 else "%d onluk ve %d birlik kaç eder?" % (t, o),
                  num(n), [num(n + 1), num(n - 10), num(o * 10 + t) if o else num(n + 2), num(n + 10)], "%d onluk ve %d birlik: <b>%d</b>." % (t, o, n))
    return named(f, "say100")


def m_kap_kiyas():
    def f():
        x, y = sh(["sürahi", "kova", "tencere", "şişe", "termos", "kavanoz"])[:2]
        a, c = ri(2, 12), ri(2, 12)
        if a == c:
            return None
        bar = ch(["bardak", "fincan", "kepçe"])
        k = ri(0, 1)
        if k == 0:
            big = rnd() < 0.5
            g = cap(x) if (a > c) == big else cap(y)
            return mq("Bir %s %d %s, bir %s %d %s su alıyor. Hangisi daha %s su alır?" % (x, a, bar, y, c, bar, "çok" if big else "az"), g,
                      [cap(y) if g == cap(x) else cap(x), "İkisi eşit", "Bilinemez"], "%d ile %d karşılaştırılır: <b>%s</b>." % (a, c, g))
        return mq("Bir %s %d %s, bir %s %d %s su alıyor. %s, %s kabından kaç %s fazla su alır?" % (x, a, bar, y, c, bar, cap(x if a > c else y), y if a > c else x, bar),
                  "%d %s" % (abs(a - c), bar), ["%d %s" % (v, bar) for v in (a + c, abs(a - c) + 1, max(a, c)) if v != abs(a - c)] + ["%d %s" % (abs(a - c) + 2, bar)],
                  "%d − %d = <b>%d %s</b>." % (max(a, c), min(a, c), abs(a - c), bar))
    return named(f, "kap_kiyas")


def m_birim_farki():
    def f():
        x, y = G.K.two()
        a, c = ri(3, 9), ri(3, 9)
        if a == c:
            return None
        bar = ch(["küçük bardak", "büyük bardak"])
        return mq("%s ve %s aynı sürahiyi dolduruyor. %s küçük bardakla %d kez, %s büyük bardakla %d kez dolduruyor. Kim daha büyük bardak kullanıyor?" % (x, y, x, max(a, c), y, min(a, c)) if False else
                  "Aynı sürahi, %s ile %d bardakla, %s ile %d bardakla doluyor. Kimin bardağı daha büyüktür?" % (x, a, y, c),
                  x if a < c else y, [y if a < c else x, "İkisinin bardağı eşit", "Bilinemez"],
                  "Bardak büyükse daha az sayıda bardak gerekir. %d ile %d: <b>%s</b>." % (a, c, x if a < c else y))
    return named(f, "birim_farki")


def u1():
    sets = [("Onluk ve birliklerle sayma", [(m_say100(), 20)]),
            ("Okuma ve yazma", [(m_okunus(21, 100), 20)]),
            ("Önce ve sonra", [(m_once_sonra(20, 100), 20)]),
            ("10 fazlası, 10 eksiği", [(m_once_sonra(20, 90, (10,)), 20)]),
            ("Eksik sayılar", [(m_eksik(20, 100), 20)])]
    return unit("100e-kadar-sayilar", "S", "MAT.2.1.1", 1, "100’e Kadar Sayılar: Okuma, Yazma ve Sayma", "100’e Kadar Sayılar",
                "100’e kadar olan niceliklerin büyüklüklerini temsil etmede sayıların sembolik temsillerinden yararlanır; sayıları okur, yazar ve onluk ve birliklerle sayar.",
                "2. sınıf 100’e kadar sayılar çalışma kâğıdı: onluk ve birliklerle sayma, sayıları okuma ve yazma, önce ve sonra gelen sayı, 10 fazlası ve 10 eksiği, eksik sayılar. 100 soru ve cevap anahtarı.",
                "Önce onlukları, sonra birlikleri say", "47: 4 onluk 7 birlik, okunuşu kırk yedi.", sets,
                ["İki basamaklı sayılar onluk ve birliklerden oluşur: 47 = 4 onluk ve 7 birlik.",
                 "Sayıyı okurken önce onlukları, sonra birlikleri okuruz: kırk yedi.",
                 "Bir sayının 10 fazlası için onlar basamağı 1 artar: 47 → 57."],
                [("62 sayısını oku", ["6 onluk → altmış", "2 birlik → iki"], "altmış iki"), ("38 sayısının 10 fazlası", ["Onlar 3’ten 4’e"], "48")],
                [["Kırk yediyi 407 yazmak", "4 onluk 7 birlik: 47"], ["Onlar ile birleri ters yazmak", "Önce onlar, sonra birler"],
                 ["10 fazlası yerine 1 fazlası bulmak", "10 fazlasında onlar basamağı değişir"]],
                [("100 kaç onluktur?", "10 onluktur."), ("Onluk blok nedir?", "10 tane birlik küpün birleşmiş hâlidir."),
                 ("99’dan sonra hangi sayı gelir?", "100 gelir: yüz.")])


def u2():
    sets = [("Basamak değeri", [(m_onluk_birlik((0,)), 20)]),
            ("Çözümleme", [(m_onluk_birlik((1,)), 20)]),
            ("Onluk ve birlik", [(m_onluk_birlik((2,)), 20)]),
            ("Bloklar", [(m_onluk_birlik((3,)), 20)]),
            ("Basamak tablosu", [(m_onluk_birlik((4,)), 20)])]
    return unit("iki-basamakli-sayilar", "S", "MAT.2.1.2", 2, "İki Basamaklı Sayılar: Onluk, Birlik ve Basamak Değeri", "Basamak Değeri",
                "İki basamaklı sayıları çözümler; onlar ve birler basamağını, basamak değerini ve sayının onluk ve birliklere ayrılışını belirler.",
                "2. sınıf iki basamaklı sayılar çalışma kâğıdı: onlar ve birler basamağı, basamak değeri, sayıları çözümleme, onluk ve birlik bloklar, basamak tablosu. 100 soru ve cevap anahtarı.",
                "Onlar basamağı × 10 + birler", "58 = 50 + 8: 5 onluk, 8 birlik.", sets,
                ["İki basamaklı sayıda soldaki rakam onlar, sağdaki rakam birler basamağındadır.",
                 "Rakamın basamak değeri bulunduğu basamağa göre değişir: 58 sayısında 5 rakamının değeri 50’dir.",
                 "Sayıyı çözümlemek, onu onluk ve birliklerin toplamı olarak yazmaktır: 58 = 50 + 8."],
                [("73 sayısında 7 rakamı", ["Onlar basamağında"], "70"), ("6 onluk 4 birlik", ["60 + 4"], "64")],
                [["Basamak değeri yerine rakamın kendisini yazmak", "Onlardaki 7 = 70"], ["Çözümlemede 7 + 3 yazmak", "73 = 70 + 3"],
                 ["Onluk ve birlikleri karıştırmak", "Uzun çubuk onluk, küçük küp birlik"]],
                [("Basamak değeri ile sayı değeri farkı nedir?", "Sayı değeri rakamın kendisidir; basamak değeri yerine göre değişir."),
                 ("Sıfır ne işe yarar?", "Boş basamağı gösterir: 40 sayısında birler basamağı boştur."),
                 ("Çözümleme nasıl kontrol edilir?", "Onlukları ve birlikleri toplarsın; sayıyı bulmalısın.")])


def u3():
    sets = [("Büyük mü küçük mü?", [(m_karsilastir(10, 99), 20)]),
            ("En büyük ve en küçük", [(m_en(10, 99), 20)]),
            ("Sıralama", [(m_sirala(10, 99), 20)]),
            ("Arada kalan sayı", [(m_once_sonra(10, 99), 20)]),
            ("Karışık", [(m_karsilastir(10, 99), 7), (m_en(10, 99), 7), (m_sirala(10, 99), 6)])]
    return unit("sayilari-karsilastirma-ve-siralama", "S", "MAT.2.1.3", 3, "Sayıları Karşılaştırma ve Sıralama", "Sıralama",
                "Sayıların sırasını belirler; 100’e kadar sayıları büyüktür, küçüktür ve eşittir işaretiyle karşılaştırır, küçükten büyüğe ve büyükten küçüğe sıralar.",
                "2. sınıf sayıları karşılaştırma ve sıralama çalışma kâğıdı: büyüktür, küçüktür, eşittir, en büyük ve en küçük sayı, sıralama, iki sayı arasındaki sayı. 100 soru ve cevap anahtarı.",
                "Önce onlar basamağını karşılaştır", "Onlar eşitse birlere bak.", sets,
                ["İki basamaklı sayıları karşılaştırırken önce onlar basamağına bakarız: 58 &gt; 49.",
                 "Onlar basamakları eşitse birler basamağına bakarız: 63 &lt; 67.",
                 "Sıralarken önce en küçüğü (ya da en büyüğü) buluruz, sonra devam ederiz."],
                [("72 ○ 68", ["7 onluk &gt; 6 onluk"], "72 &gt; 68"), ("45, 54, 40 sıralama", ["40 &lt; 45 &lt; 54"], "40, 45, 54")],
                [["Birlere bakıp karar vermek", "Önce onlara bak"], ["İşaretin yönünü karıştırmak", "Açık ağız büyüğe bakar"],
                 ["Sıralamada bir sayıyı unutmak", "Sayıları işaretleyerek sırala"]],
                [("Hangi basamağa önce bakılır?", "Soldaki en büyük basamağa, yani onlar basamağına."),
                 ("Eşit sayılar nasıl gösterilir?", "= işaretiyle: 50 = 50."),
                 ("Sayı doğrusunda büyük sayı nerededir?", "Sağ taraftadır.")])


def u4():
    sets = [("İkişer ve beşer", [(m_ritmik(100, (2, 5)), 20)]),
            ("Üçer ve dörder", [(m_ritmik(60, (3, 4)), 20)]),
            ("Onar", [(m_ritmik(100, (10,)), 10), (m_atlama_kac(100, (2, 3, 4, 5, 10)), 10)]),
            ("Geriye doğru", [(m_ritmik(100, (2, 3, 5, 10), True), 20)]),
            ("Tek ve çift sayılar", [(m_tek_cift(), 20)])]
    return unit("ritmik-sayma", "S", "MAT.2.1.4", 4, "Ritmik Sayma: İkişer, Üçer, Dörder, Beşer, Onar", "Ritmik Sayma",
                "İleriye ve geriye doğru ikişer, üçer, dörder, beşer ve onar ritmik sayar; ikişer sayarken tek ve çift sayıları fark eder.",
                "2. sınıf ritmik sayma çalışma kâğıdı: ikişer, üçer, dörder, beşer ve onar ileriye ve geriye sayma, kaç adım, tek ve çift sayılar. 100 soru ve cevap anahtarı.",
                "Her adımda aynı sayı kadar ilerle", "Çift sayılar 0, 2, 4, 6, 8 ile biter.", sets,
                ["Ritmik saymada her adımda aynı sayıyı ekleriz ya da çıkarırız.",
                 "Üçer sayarken 3, dörder sayarken 4 ekleriz: 4, 8, 12, 16…",
                 "Sıfırdan ikişer sayınca çift sayıları buluruz. Çift sayıların birler basamağı 0, 2, 4, 6 ya da 8’dir; diğerleri tektir."],
                [("3, 6, 9, …", ["Üçer artıyor"], "12"), ("47 tek mi çift mi?", ["Birler basamağı 7"], "Tek")],
                [["Üçer sayarken 2 eklemek", "Adım sayısını kontrol et"], ["Geriye sayarken eklemek", "Geriye: çıkar"],
                 ["Onlar basamağına bakıp tek-çift demek", "Birler basamağına bak"]],
                [("Ritmik sayma neden önemli?", "Çarpma işlemini öğrenmeye hazırlar."),
                 ("0 çift sayı mıdır?", "Evet, 0 çift sayıdır."),
                 ("Dörder saymanın kolay yolu var mı?", "İkişer sayıp birer atlayabilirsin: 2, 4, 6, 8 → 4, 8.")])


def u5():
    sets = [("Şekil örüntüleri", [(m_oruntu(), 20)]),
            ("Artan sayı örüntüleri", [(m_eksik(0, 100, (2, 3, 4, 5, 10), False), 20)]),
            ("Azalan sayı örüntüleri", [(m_eksik(0, 100, (2, 3, 5, 10), True), 20)]),
            ("Şekilden sayıya", [(m_sekil_say_oruntu(), 20)]),
            ("Karışık", [(m_oruntu(), 10), (m_ritmik(100, (3, 4, 5)), 10)])]
    return unit("oruntuler", "S", "MAT.2.1.5", 5, "Örüntüler: Sayı ve Şekil Örüntüleri", "Örüntüler",
                "Sayı ve sayı temsiline dönüşen şekil örüntülerine dayalı çıkarım yapar; örüntünün kuralını bulur ve eksik ya da sonraki ögeyi belirler.",
                "2. sınıf örüntüler çalışma kâğıdı: tekrarlayan şekil örüntüleri, artan ve azalan sayı örüntüleri, şekil örüntüsünden sayı örüntüsüne geçiş. 100 soru ve cevap anahtarı.",
                "Kuralı bul, sonra devam et", "Örüntüdeki artış ya da azalış her adımda aynıdır.", sets,
                ["Örüntünün kuralını bulmak için ardışık iki ögeyi karşılaştırırız.",
                 "Artan örüntüde her adımda aynı sayı eklenir, azalan örüntüde aynı sayı çıkarılır.",
                 "Şekil örüntüsündeki kareleri sayınca bir sayı örüntüsü elde ederiz: 2, 4, 6, 8."],
                [("12, 16, 20, …", ["Dörder artıyor"], "24"), ("Kareler 3, 5, 7", ["İkişer artıyor"], "4. adımda 9")],
                [["İlk iki sayıya bakıp kuralı kesinleştirmek", "Bütün adımları kontrol et"], ["Azalan örüntüde eklemek", "Sayılar küçülüyorsa çıkar"],
                 ["Örüntü birimini eksik yazmak", "Tekrar eden kısmın tamamını bul"]],
                [("Örüntü nerede görülür?", "Takvimde, halı desenlerinde, merdiven basamaklarında."),
                 ("Bir örüntünün tek kuralı mı vardır?", "Bazen farklı kurallar bulunabilir; verilen bütün sayılara uyan kural doğrudur."),
                 ("Şekil örüntüsü sayı örüntüsüne nasıl dönüşür?", "Her adımdaki şekilleri sayarız.")])


def u6():
    sets = [("Yaklaşık kaç?", [(m_tahmin(50, 10), 20)]),
            ("Bilinen grupla karşılaştır", [(m_tahmin_kiyas(50), 20)]),
            ("Tahmin et ve say", [(m_tahmin(50, 10), 10), (m_say100(), 10)]),
            ("Onluklarla tahmin", [(m_tahmin(50, 5), 20)]),
            ("Karışık", [(m_tahmin(50, 10), 10), (m_tahmin_kiyas(50), 10)])]
    return unit("nesne-sayisini-tahmin-etme", "S", "MAT.2.1.6", 6, "Nesne Sayısını Tahmin Etme: 50’ye Kadar", "Tahmin Etme",
                "Bir çokluktaki ilişkilerden yararlanarak 50’ye kadar olan nesnelerin sayısını tahmin eder ve tahminini sayarak kontrol eder.",
                "2. sınıf tahmin etme çalışma kâğıdı: 50’ye kadar nesne sayısını saymadan tahmin etme, onluk gruplarla tahmin, bilinen bir çoklukla karşılaştırma, tahmin edip sayma. 100 soru ve cevap anahtarı.",
                "Bilinen bir grupla karşılaştır", "Önce 10 nesnelik bir grubu gözünde canlandır.", sets,
                ["Tahmin, saymadan söylenen yaklaşık sayıdır.",
                 "Önce yaklaşık 10 nesnelik bir grubu buluruz, sonra kaç tane böyle grup olduğunu düşünürüz.",
                 "Tahminden sonra sayarak kontrol ederiz; tahmin gerçek sayıya yakın olmalıdır."],
                [("Resimde yaklaşık 3 grup 10", ["10 + 10 + 10"], "Yaklaşık 30"), ("Tahmin 40, sayınca 38", ["Fark 2"], "İyi bir tahmin")],
                [["Tahmini tam sayı sanmak", "Tahmin yaklaşıktır"], ["Çok uzak bir tahmin yapmak", "10’luk gruplarla düşün"],
                 ["Kontrol etmemek", "Sayarak tahminini kontrol et"]],
                [("Tahmin ne zaman işe yarar?", "Çok nesne olduğunda hızlıca fikir edinmek için."),
                 ("İyi tahmin nasıl yapılır?", "Bilinen bir grubu ölçü olarak kullan."),
                 ("Tahminim tutmazsa ne olur?", "Sorun değil; saydıkça tahminlerin iyileşir.")])


def u7():
    sets = [("Boyalı kısım", [(m_yarim((0,)), 10), (m_yarim((2,)), 10)]),
            ("Bir çokluğun yarısı ve çeyreği", [(m_yarim((1,)), 20)]),
            ("Bütün, yarım, çeyrek", [(m_yarim((2,)), 2), (m_yarim((0,)), 3), (m_yarim((1,)), 15)]),
            ("Yarım ve çeyrek ilişkisi", [(m_yarim((1,)), 20)]),
            ("Karışık", [(m_yarim((0, 1)), 20)])]
    return unit("butun-yarim-ve-ceyrek", "S", "MAT.2.1.7", 7, "Bütün, Yarım ve Çeyrek", "Bütün, Yarım, Çeyrek",
                "Bütün, yarım ve çeyrek arasındaki ilişkiyi çözümler; bir bütünü ve bir çokluğu iki ve dört eş parçaya ayırır.",
                "2. sınıf bütün, yarım ve çeyrek çalışma kâğıdı: boyalı kısmın yarım ya da çeyrek olduğunu bulma, bir çokluğun yarısı ve çeyreği, 2 yarım = 1 bütün, 4 çeyrek = 1 bütün. 100 soru ve cevap anahtarı.",
                "2 yarım = 1 bütün, 4 çeyrek = 1 bütün", "Parçalar eş (aynı büyüklükte) olmalı.", sets,
                ["Bir bütün 2 eş parçaya bölününce her parça yarımdır. 2 yarım bir bütün eder.",
                 "Bir bütün 4 eş parçaya bölününce her parça çeyrektir. 4 çeyrek bir bütün, 2 çeyrek bir yarım eder.",
                 "Bir çokluğun yarısını bulmak için 2 eş gruba, çeyreğini bulmak için 4 eş gruba ayırırız."],
                [("12 elmanın yarısı", ["2 eş grup: 6 ve 6"], "6"), ("8 kalemin çeyreği", ["4 eş grup: 2, 2, 2, 2"], "2")],
                [["Eş olmayan parçalara yarım demek", "Parçalar aynı büyüklükte olmalı"], ["Çeyreği yarımdan büyük sanmak", "Çeyrek, yarımın yarısıdır"],
                 ["Çokluğun yarısını bulurken 2 çıkarmak", "2 eş gruba ayır"]],
                [("Yarım ile çeyrek arasındaki fark nedir?", "Yarım 2 eş parçadan biri, çeyrek 4 eş parçadan biridir."),
                 ("Yarım saat ne kadardır?", "30 dakikadır; çeyrek saat 15 dakikadır."),
                 ("Bir pizzanın 4 çeyreği yenirse ne kalır?", "Hiç kalmaz; bütün pizza yenmiştir.")])


def u8():
    PAIRS = [(10, 5), (20, 10), (20, 5), (50, 10), (50, 5), (100, 50), (100, 20), (100, 10), (200, 100), (200, 50), (10, 1), (5, 1), (50, 20), (200, 20)]
    sets = [("Paraları sayma", [(m_para_say((1, 5, 10, 20, 50), 100, (2, 4)), 20)]),
            ("Para bozdurma", [(m_para_bozdur(PAIRS), 20)]),
            ("Hangisi daha değerli?", [(m_para_karsilastir(), 8), (m_para_say((5, 10, 20), 100, (3, 4)), 12)]),
            ("Alışveriş ve para üstü", [(m_para_alisveris(100), 20)]),
            ("Eksik para", [(m_para_eksik(100), 20)])]
    return unit("paralarimiz", "S", "MAT.2.1.8", 8, "Paralarımız: Paraları Sayma ve Bozdurma", "Paralarımız",
                "Paraları değerlerine göre ilişkilendirerek çözümler; madenî ve kâğıt paraları sayar, bozdurur ve alışveriş problemlerinde kullanır.",
                "2. sınıf paralarımız çalışma kâğıdı: kâğıt ve madenî paraları sayma, para bozdurma, hangisi daha değerli, alışverişte para üstü, eksik parayı bulma. 100 soru ve cevap anahtarı.",
                "Büyük paradan başlayarak say", "Bir 10 TL = iki 5 TL = on 1 TL.", sets,
                ["Paraları sayarken en değerli paradan başlarız: 20 + 10 + 5 = 35 TL.",
                 "Bir parayı aynı değerdeki küçük paralarla değiştirmeye bozdurma denir: 50 TL = 20 + 20 + 10.",
                 "Para üstü, verilen paradan ürünün fiyatı çıkarılarak bulunur."],
                [("20 TL, 10 TL, 5 TL", ["20 + 10 + 5"], "35 TL"), ("50 TL verdi, 32 TL ödedi", ["50 − 32"], "18 TL para üstü")],
                [["Para sayısını değeri sanmak", "Değerleri topla"], ["Para üstünü bulurken toplamak", "Verilen paradan fiyatı çıkar"],
                 ["Bozdururken toplamı kontrol etmemek", "Küçük paraların toplamı eşit olmalı"]],
                [("Hangi madenî paralar var?", "1 TL ve kuruşlar madenî paradır; 5 TL’den itibaren kâğıt paralar vardır."),
                 ("Para üstünü nasıl kontrol ederim?", "Fiyat ile para üstünü topla; verdiğin parayı bulmalısın."),
                 ("Neden para bozdururuz?", "Küçük alışverişlerde tam ödeme yapabilmek için.")])


def u9():
    sets = [("Tam ve yarım saatler", [(m_saat((0, 30)), 20)]),
            ("Çeyrek saatler", [(m_saat((15, 45)), 20)]),
            ("Dijital saat", [(m_saat((0, 15, 30, 45)), 20)]),
            ("Gün, hafta, ay", [(m_takvim(), 20)]),
            ("Karışık", [(m_saat((0, 15, 30, 45)), 10), (m_takvim(), 10)])]
    return unit("zaman-olcme", "S", "MAT.2.1.9", 9, "Zaman Ölçme: Saat, Gün, Hafta, Ay ve Yıl", "Zaman Ölçme",
                "Zaman ölçü birimlerini okur ve yazar; tam, yarım ve çeyrek saatleri okur, saat, dakika, gün, hafta, ay ve yıl arasındaki ilişkileri kullanır.",
                "2. sınıf zaman ölçme çalışma kâğıdı: tam, yarım ve çeyrek saatleri okuma, dijital saat, günler, haftalar, aylar ve yıl, takvim soruları. 100 soru ve cevap anahtarı.",
                "Kısa ibre saat, uzun ibre dakika", "1 saat = 60 dakika, 1 hafta = 7 gün, 1 yıl = 12 ay.", sets,
                ["Saatin kısa ibresi (akrep) saati, uzun ibresi (yelkovan) dakikayı gösterir.",
                 "Yelkovan 12’deyse tam saat, 6’daysa buçuk (yarım), 3’teyse çeyrek geçiyor, 9’daysa çeyrek var.",
                 "1 gün 24 saat, 1 hafta 7 gün, 1 yıl 12 aydır. Günler ve aylar belli bir sırayla gelir."],
                [("Akrep 4, yelkovan 12", ["Tam saat"], "Saat dört"), ("Bugün cuma, 2 gün sonra", ["Cumartesi, pazar"], "Pazar")],
                [["Akrep ile yelkovanı karıştırmak", "Kısa ibre saati gösterir"], ["Buçukta akrebi tam sayıda sanmak", "Akrep iki sayının arasındadır"],
                 ["Günlerin sırasını karıştırmak", "Pazartesiden başlayarak say"]],
                [("Çeyrek saat kaç dakikadır?", "15 dakikadır."), ("Yılın en kısa ayı hangisidir?", "Şubattır."),
                 ("Dijital saatte 07.30 ne demek?", "Saat yedi buçuk demektir.")])


def u10():
    sets = [("Cetvelle ölçme", [(m_cetvel(), 20)]),
            ("Uygun birim", [(m_birim_sec(), 10), (m_kac_birim(), 10)]),
            ("Tahmin etme", [(m_uzunluk_tahmin(), 14), (m_cetvel(), 6)]),
            ("Ağır ve hafif", [(m_agir(), 10), (m_denge(), 10)]),
            ("Karışık", [(m_cetvel(), 10), (m_kac_birim(), 10)])]
    return unit("uzunluk-ve-kutle-olcme", "S", "MAT.2.1.10, MAT.2.1.11", 10, "Uzunluk ve Kütle Ölçme: Metre, Santimetre ve Kilogram", "Uzunluk ve Kütle",
                "Standart uzunluk ve kütle ölçme araçlarının ve birimlerinin gerekliliğini yansıtır; metre, santimetre ve kilogram cinsinden uzunlukları ve kütleleri tahmin eder ve ölçer.",
                "2. sınıf uzunluk ve kütle ölçme çalışma kâğıdı: cetvelle santimetre ölçme, metre ve santimetre, kilogram, uygun birimi seçme, uzunluk ve kütle tahmini. 100 soru ve cevap anahtarı.",
                "Cetvelde sıfırdan başla", "Kısa uzunluk cm, uzun uzunluk m, kütle kg.", sets,
                ["Herkesin karışı farklı olduğu için standart birimlere ihtiyaç duyarız: metre (m), santimetre (cm), kilogram (kg).",
                 "Cetvelle ölçerken nesnenin bir ucunu sıfıra koyarız ve diğer ucun karşısındaki sayıyı okuruz.",
                 "Kısa nesneleri santimetre, uzun mesafeleri metre ile ölçeriz. Kütleyi kilogram ile ölçeriz."],
                [("Kalem 0’dan 9’a kadar", ["Bitiş 9"], "9 cm"), ("Sınıfın uzunluğu", ["Uzun bir mesafe"], "Metre")],
                [["Cetveli 1’den başlatmak", "Sıfırdan başla"], ["Uzun mesafeyi cm ile ölçmek", "Uzun mesafede metre kullan"],
                 ["Kütle için metre kullanmak", "Kütle kg ile ölçülür"]],
                [("1 metre kaç santimetredir?", "100 santimetredir."),
                 ("Neden standart birim kullanırız?", "Herkes aynı sonucu bulsun diye."),
                 ("Kütle ve ağırlık aynı mı?", "Günlük dilde aynı anlamda kullanılır; matematikte kütle kg ile ölçülür.")])


def u11():
    sets = [("Eldesiz toplama", [(m_islem("+", 20, 99, False), 20)]),
            ("Eldeli toplama", [(m_islem("+", 20, 100, True), 20)]),
            ("Zihinden toplama", [(m_islem("+", 10, 100), 20)]),
            ("Tahmin etme", [(m_tahmin_islem(11, 60), 20)]),
            ("Noktalı yer", [(m_bos(100, 10), 20)])]
    return unit("toplama-islemi", "I", "MAT.2.2.1, MAT.2.2.2", 11, "Toplama İşlemi: 100’e Kadar Eldeli ve Eldesiz", "Toplama İşlemi",
                "Toplamları 100’ü geçmeyen eldeli ve eldesiz toplama işlemleri yapar; sonucu tahminde bulunarak ve zihinden işlem yaparak muhakeme eder.",
                "2. sınıf toplama işlemi çalışma kâğıdı: 100’e kadar eldesiz ve eldeli toplama, zihinden toplama, en yakın onluğa yuvarlayarak tahmin, eksik toplanan. 100 soru ve cevap anahtarı.",
                "Önce birlikleri topla", "Birlikler 10 ya da daha fazla olursa 1 onluk elde edilir.", sets,
                ["Toplama yaparken önce birlikleri, sonra onlukları toplarız.",
                 "Birlikler toplamı 10 ya da daha fazla olursa 10 birliği 1 onluk yaparız; buna elde denir.",
                 "Tahmin için sayıları en yakın onluğa yuvarlarız: 38 + 21 → 40 + 20 = 60."],
                [("36 + 27", ["6 + 7 = 13 → 3 birlik, 1 onluk elde", "3 + 2 + 1 = 6 onluk"], "63"), ("48 + 31 tahmini", ["50 + 30"], "Yaklaşık 80")],
                [["Eldeyi eklemeyi unutmak", "Elde onluklara eklenir"], ["Onluk ile birliği alt alta yazmamak", "Basamakları hizala"],
                 ["Yuvarlarken 5’i aşağı yuvarlamak", "Birler 5 ve üstüyse yukarı yuvarla"]],
                [("Elde nedir?", "Birlikler 10’u geçince oluşan onluğun bir üst basamağa aktarılmasıdır."),
                 ("Toplananların yeri değişirse ne olur?", "Toplam değişmez."),
                 ("Zihinden toplamanın kolay yolu nedir?", "Önce onlukları, sonra birlikleri toplayabilirsin: 34 + 25 → 50 + 9.")])


def u12():
    sets = [("Onluk bozmadan çıkarma", [(m_islem("-", 20, 99, False), 20)]),
            ("Onluk bozarak çıkarma", [(m_islem("-", 21, 99, True), 20)]),
            ("Zihinden çıkarma", [(m_islem("-", 11, 100), 20)]),
            ("Tahmin etme", [(m_tahmin_islem(20, 90), 20)]),
            ("Toplama ile kontrol", [(m_iliski(100), 20)])]
    return unit("cikarma-islemi", "I", "MAT.2.2.1, MAT.2.2.2, MAT.2.2.3", 12, "Çıkarma İşlemi: 100’e Kadar Onluk Bozarak", "Çıkarma İşlemi",
                "100’e kadar sayılarla onluk bozmadan ve onluk bozarak çıkarma yapar; sonucu tahmin eder ve toplama ile çıkarma arasındaki ilişkiyi kullanarak kontrol eder.",
                "2. sınıf çıkarma işlemi çalışma kâğıdı: 100’e kadar onluk bozmadan ve onluk bozarak çıkarma, zihinden çıkarma, tahmin, toplama ile kontrol. 100 soru ve cevap anahtarı.",
                "Birlikler yetmezse 1 onluk boz", "Çıkarmayı toplama ile kontrol et.", sets,
                ["Çıkarmada önce birlikleri, sonra onlukları çıkarırız.",
                 "Eksilenin birlikleri az gelirse 1 onluğu 10 birliğe bozarız: 52 − 27 → 12 − 7 = 5, 4 − 2 = 2.",
                 "Sonucu kontrol etmek için fark ile çıkanı toplarız; eksileni bulmalıyız."],
                [("64 − 28", ["14 − 8 = 6", "5 − 2 = 3"], "36"), ("36 + 28 = 64 ile kontrol", ["Toplam eksilene eşit"], "Doğru")],
                [["Küçük birlikten büyüğü çıkarmak için ters çevirmek", "Onluk boz"], ["Bozduğun onluğu unutmak", "Onlar basamağı 1 azalır"],
                 ["Kontrol için çıkarma yapmak", "Kontrol için topla"]],
                [("Onluk bozmak ne demek?", "1 onluğu 10 birliğe çevirmek demektir."),
                 ("Çıkarmada sayıların yeri değişir mi?", "Hayır, büyük sayı önce yazılır."),
                 ("Tahmin neden yapılır?", "Sonucun yaklaşık doğru olup olmadığını anlamak için.")])


def u13():
    sets = [("Toplama problemleri", [(m_problem(100, "+"), 20)]),
            ("Çıkarma problemleri", [(m_problem(100, "-"), 20)]),
            ("Karşılaştırma problemleri", [(m_problem(100, "="), 20)]),
            ("Alışveriş problemleri", [(m_para_alisveris(100), 10), (m_para_eksik(100), 10)]),
            ("Karışık", [(m_problem(100, "+-="), 20)])]
    return unit("toplama-ve-cikarma-problemleri", "I", "MAT.2.2.1", 13, "Toplama ve Çıkarma Problemleri", "Problemler",
                "Toplama ve çıkarma işlemleri gerektiren günlük yaşam problemlerini çözer; problemi anlar, uygun işlemi seçer ve sonucu kontrol eder.",
                "2. sınıf toplama ve çıkarma problemleri çalışma kâğıdı: birleştirme, eksiltme ve karşılaştırma problemleri, alışveriş ve para üstü problemleri. 100 soru ve cevap anahtarı.",
                "Oku, anla, işlemi seç", "Birleşirse topla, eksilirse ya da fark sorulursa çıkar.", sets,
                ["Problemi okuruz; verilenleri ve isteneni buluruz.",
                 "Birleştirme ve ekleme varsa toplarız; eksilme, ayırma ya da fark varsa çıkarırız.",
                 "Sonucu kontrol eder ve cevabı birimiyle yazarız."],
                [("Rafta 38 kitap var, 25 kitap daha kondu.", ["38 + 25"], "63 kitap"), ("45 balon vardı, 17’si patladı.", ["45 − 17"], "28 balon")],
                [["Her problemde toplamak", "İpucu sözcüklere bak"], ["Fark sorusunda toplamak", "Fark için çıkar"], ["Birimi yazmamak", "Cevabın yanına birimi yaz"]],
                [("Problemi anlamak için ne yapabilirim?", "Şekil ya da şema çizebilirsin."),
                 ("Cevabımı nasıl kontrol ederim?", "Ters işlem yap: çıkarmayı toplamayla kontrol et."),
                 ("“Kaç fazla” ne demek?", "İki sayı arasındaki farkı sorar; çıkarma yapılır.")])


def u14():
    sets = [("Eşit gruplar", [(m_carpma_resim(5), 20)]),
            ("Tekrarlı toplama", [(m_tekrarli(5), 20)]),
            ("Çarpım tablosu", [(m_carpim(), 20)]),
            ("Çarpma problemleri", [(m_carpma_problem(5), 20)]),
            ("Karışık", [(m_carpim(), 10), (m_carpma_resim(5), 10)])]
    return unit("carpma-islemi", "I", "MAT.2.2.4, MAT.2.2.5", 14, "Çarpma İşlemi: Tekrarlı Toplama ve 5’e Kadar Çarpım Tablosu", "Çarpma İşlemi",
                "Çarpma işlemini toplama işlemine dayalı olarak çözümler; 10’a kadar sayıları 1, 2, 3, 4 ve 5 ile çarpar ve sonuçları muhakeme eder.",
                "2. sınıf çarpma işlemi çalışma kâğıdı: eşit gruplar ve dizi modeli, tekrarlı toplama, 1, 2, 3, 4 ve 5 çarpım tablosu, çarpma problemleri. 100 soru ve cevap anahtarı.",
                "Çarpma = tekrarlı toplama", "3 × 4 = 4 + 4 + 4 = 12.", sets,
                ["Eşit grupları toplarken çarpma kullanırız: 3 grupta 4’er nesne → 3 × 4.",
                 "3 × 4 ifadesi “3 kere 4” diye okunur ve 4 + 4 + 4 toplamına eşittir.",
                 "Çarpanların yeri değişince sonuç değişmez: 3 × 4 = 4 × 3."],
                [("5 grupta 2’şer kalem", ["2 + 2 + 2 + 2 + 2", "5 × 2"], "10"), ("4 × 3", ["3 + 3 + 3 + 3"], "12")],
                [["3 × 4 yerine 3 + 4 yapmak", "× kere demektir"], ["Grup sayısını eksik saymak", "Grupları tek tek işaretle"],
                 ["1 ile çarpınca 1 bulmak", "Bir sayının 1 katı kendisidir"]],
                [("Çarpma neden kolaylık sağlar?", "Aynı sayıyı tekrar tekrar toplamak yerine hızlıca sonuca ulaştırır."),
                 ("0 ile çarpınca ne olur?", "Sonuç 0 olur."),
                 ("Çarpım tablosunu nasıl ezberlerim?", "Ritmik sayma yaparak: beşer sayınca 5’in katlarını bulursun.")])


def u15():
    sets = [("Eşit paylaştırma", [(m_bolme_resim(), 20)]),
            ("Tekrarlı çıkarma", [(m_tekrarli_cikarma(), 14), (m_bolum(), 6)]),
            ("Bölme işlemi", [(m_bolum(), 12), (m_bolme_iliski(), 8)]),
            ("Bölme problemleri", [(m_bolme_problem(), 20)]),
            ("Karışık", [(m_bolme_iliski(), 7), (m_bolme_resim(), 7), (m_carpim((2, 3, 4, 5)), 6)])]
    return unit("bolme-islemi", "I", "MAT.2.2.4, MAT.2.2.5", 15, "Bölme İşlemi: Paylaştırma ve Gruplama", "Bölme İşlemi",
                "Bölme işlemini çıkarma işlemine dayalı olarak çözümler; 20’ye kadar sayıları 2, 3, 4 ve 5’e kalansız böler ve sonucu muhakeme eder.",
                "2. sınıf bölme işlemi çalışma kâğıdı: eşit paylaştırma, eşit gruplama, tekrarlı çıkarma, 20’ye kadar kalansız bölme, bölme problemleri. 100 soru ve cevap anahtarı.",
                "Bölme = eşit paylaştırma", "12 ÷ 3 = 4, çünkü 3 × 4 = 12.", sets,
                ["Bölme, bir çokluğu eşit gruplara ayırmaktır. ÷ işareti “bölü” diye okunur.",
                 "Bölmeyi tekrarlı çıkarma ile de yaparız: 12 − 3 − 3 − 3 − 3 = 0, yani 4 kez.",
                 "Bölme, çarpmanın tersidir: 3 × 4 = 12 ise 12 ÷ 3 = 4."],
                [("15 ceviz 3 çocuğa", ["Her çocuğa birer birer dağıt", "15 ÷ 3"], "5 ceviz"), ("10 − 2 − 2 − 2 − 2 − 2", ["5 kez çıkarıldı"], "10 ÷ 2 = 5")],
                [["Bölmede toplamak ya da çıkarmak", "Eşit gruplara ayır"], ["Grupların eşit olmadığını fark etmemek", "Her grupta aynı sayıda olmalı"],
                 ["Bölünen ile böleni karıştırmak", "Büyük sayı bölünendir"]],
                [("Kalansız bölme ne demek?", "Hiç nesne artmadan eşit paylaştırmak demektir."),
                 ("Bölmeyi nasıl kontrol ederim?", "Bölüm ile böleni çarparsın; bölüneni bulmalısın."),
                 ("Paylaştırma ile gruplama farkı nedir?", "Paylaştırmada grup sayısı, gruplamada her gruptaki nesne sayısı bilinir.")])


def u16():
    sets = [("Eşittir işareti", [(m_esit(20), 20)]),
            ("Dört işlemde eşitlik", [(m_esit_dort(), 20)]),
            ("Noktalı yer", [(m_bos(100, 10), 20)]),
            ("Terazi dengede", [(m_terazi_sayi(18), 20)]),
            ("İşlemler arası ilişki", [(m_iliski(100), 20)])]
    return unit("esitlik", "I", "MAT.2.2.6", 16, "Dört İşlem Bağlamında Eşitlik", "Eşitlik",
                "Dört işlem bağlamında eşitliğin farklı anlamlarını yorumlar; eşittir işaretinin iki yanının aynı değeri gösterdiğini kullanarak eksik sayıları bulur.",
                "2. sınıf eşitlik çalışma kâğıdı: eşittir işaretinin anlamı, toplama, çıkarma, çarpma ve bölmede eşitlik, noktalı yere gelen sayı, dengede terazi. 100 soru ve cevap anahtarı.",
                "= işaretinin iki yanı aynı değer", "8 + 5 = 10 + 3; iki yan da 13.", sets,
                ["Eşittir işareti iki yanın aynı değerde olduğunu gösterir; sağ tarafta da bir işlem olabilir.",
                 "Bir yandaki sayı artarsa diğer sayı aynı miktarda azalırsa toplam değişmez: 8 + 5 = 10 + 3.",
                 "Dengede bir terazi eşitliği gösterir: iki kefedeki toplam aynıdır."],
                [("9 + 6 = 10 + …", ["9 + 6 = 15", "10 + 5 = 15"], "5"), ("2 × 6 = 3 × …", ["2 × 6 = 12", "3 × 4 = 12"], "4")],
                [["Eşittirden sonra sonucu yazmak", "Sağ taraf da işlem olabilir"], ["Yalnızca sol tarafı hesaplamak", "İki tarafı da hesapla"],
                 ["Teraziyi dengesiz bırakmak", "Kefelerin toplamı eşit olmalı"]],
                [("Eşittir işareti “sonuç” mu demektir?", "Hayır, “aynı değerde” demektir."),
                 ("Eşitlik bozulursa ne olur?", "Bir yana ne eklersek diğer yana da eklemeliyiz."),
                 ("Terazi neden kullanılır?", "Eşitliği görmemize yardım eder.")])


def u17():
    sets = [("Cismin adı", [(m_cisim_ad(), 20)]),
            ("Çevremizdeki cisimler", [(m_cisim_gercek(), 20)]),
            ("Yuvarlanır mı?", [(m_yuvarlanir(), 20)]),
            ("Cisim ve şekil", [(m_cisim_ad(), 10), (m_sekil_ad(("circle", "triangle", "square", "rectangle", "hexagon")), 10)]),
            ("Karışık", [(m_cisim_gercek(), 10), (m_yuvarlanir(), 10)])]
    return unit("geometrik-cisimler", "G", "MAT.2.3.1, MAT.2.3.2", 17, "Geometrik Cisimler: Küp, Küre, Silindir, Koni ve Prizma", "Geometrik Cisimler",
                "Günlük yaşamda kullanılan nesneleri biçimsel özelliklerine göre geometrik cisim olarak sınıflandırır; geometrik cisim modellerini kullanarak yapılar oluşturur.",
                "2. sınıf geometrik cisimler çalışma kâğıdı: küp, küre, silindir, koni ve dikdörtgenler prizması, çevremizdeki nesneleri sınıflandırma, yuvarlanabilen cisimler. 100 soru ve cevap anahtarı.",
                "Yüzleri düz mü, eğri mi?", "Eğri yüzeyli cisimler yuvarlanır.", sets,
                ["Geometrik cisimleri yüzlerine göre ayırırız: küp ve prizmanın yüzleri düz; küre, silindir ve koninin eğri yüzeyi vardır.",
                 "Silindirin iki daire yüzü, koninin bir daire yüzü ve bir sivri ucu vardır.",
                 "Düz yüzleri olan cisimlerle kuleler ve yapılar kurabiliriz."],
                [("Konserve kutusu", ["İki daire yüzü ve eğri yan yüzü"], "Silindir"), ("Zar", ["6 kare yüzü"], "Küp")],
                [["Küreyi daire sanmak", "Küre bir cisimdir"], ["Silindiri prizma sanmak", "Silindirin tabanı dairedir"],
                 ["Koniyi üçgen sanmak", "Koni bir cisim, üçgen bir şekildir"]],
                [("Küpün kaç yüzü vardır?", "6 yüzü vardır; hepsi karedir."),
                 ("Hangi cisimler yuvarlanır?", "Küre, silindir ve koni."),
                 ("Prizma nerede görülür?", "Kutularda, tuğlalarda ve dolaplarda.")])


def u18():
    sets = [("Şeklin adı", [(m_sekil_ad(("circle", "triangle", "square", "rectangle", "hexagon")), 20)]),
            ("Kenar ve köşe", [(m_kenar(), 20)]),
            ("Döndürülmüş şekiller", [(m_sekil_bul(("circle", "triangle", "square", "rectangle", "hexagon")), 20)]),
            ("Eş şekiller", [(m_es(), 20)]),
            ("Şekilleri sayma", [(m_sekil_say(), 20)])]
    return unit("geometrik-sekiller", "G", "MAT.2.3.3, MAT.2.3.4", 18, "Geometrik Şekiller: Kenar, Köşe ve Eş Şekiller", "Geometrik Şekiller",
                "Geometrik şekiller kullanarak modeller oluşturur; şekillerin yön, konum veya büyüklükleri değiştiğinde biçimsel özelliklerinin değişmediğini yorumlar.",
                "2. sınıf geometrik şekiller çalışma kâğıdı: üçgen, kare, dikdörtgen, daire ve altıgen, kenar ve köşe sayısı, döndürülmüş şekiller, eş şekiller, şekilleri sayma. 100 soru ve cevap anahtarı.",
                "Döndürünce şeklin adı değişmez", "Kenar ve köşe sayısı aynı kalır.", sets,
                ["Bir şekli döndürür ya da yerini değiştirirsek adı, kenar ve köşe sayısı değişmez.",
                 "Büyüklüğü değişen bir üçgen yine üçgendir; ama artık ilk şekille eş değildir.",
                 "Eş şekiller aynı biçim ve büyüklüktedir; üst üste konunca tam örtüşür."],
                [("Altıgen", ["6 kenar, 6 köşe"], "6"), ("Ters çevrilmiş üçgen", ["3 kenarı var"], "Yine üçgen")],
                [["Döndürülen kareyi baklava sanmak", "Kenarları yine eşit; kare"], ["Büyük şekli farklı şekil sanmak", "Kenar sayısına bak"],
                 ["Eş şekillerde renge bakmak", "Biçim ve büyüklük önemli"]],
                [("Kare ile dikdörtgen arasındaki fark nedir?", "Karenin bütün kenarları eşittir."),
                 ("Altıgen nerede görülür?", "Arı peteklerinde."),
                 ("Şekiller birleşip yeni şekil oluşturur mu?", "Evet, iki üçgen birleşip bir kare oluşturabilir.")])


def u19():
    sets = [("Hangisi daha çok su alır?", [(m_kap(), 20)]),
            ("Bardakla ölçme", [(m_kap_kiyas(), 20)]),
            ("Farklı bardaklar", [(m_birim_farki(), 20)]),
            ("Karşılaştırma", [(m_kap_kiyas(), 20)]),
            ("Karışık", [(m_kap(), 10), (m_kap_kiyas(), 10)])]
    return unit("sivi-olcme", "G", "MAT.2.3.5", 19, "Sıvı Ölçme: Bardakla, Kepçeyle Tahmin", "Sıvı Ölçme",
                "Standart olmayan sıvı ölçme araçları ile sıvı miktarını tahmin eder; kapların aldığı sıvı miktarlarını karşılaştırır.",
                "2. sınıf sıvı ölçme çalışma kâğıdı: hangi kap daha çok su alır, bardak ve kepçe ile ölçme, farklı büyüklükte bardaklar, kapları karşılaştırma. 100 soru ve cevap anahtarı.",
                "Aynı bardakla ölç ve karşılaştır", "Büyük bardakla daha az sayıda dolar.", sets,
                ["Kapların aldığı sıvı miktarını bardak, fincan ya da kepçe ile ölçebiliriz.",
                 "Karşılaştırırken hep aynı bardağı kullanırız; daha çok bardak alan kap daha çok sıvı alır.",
                 "Büyük bardak kullanırsak daha az bardakla doldururuz."],
                [("Sürahi 6 bardak, şişe 4 bardak", ["6, 4 sayısından büyük"], "Sürahi daha çok alır"), ("Kova 12, sürahi 5 bardak", ["12 − 5"], "7 bardak fazla")],
                [["Uzun kabı her zaman daha çok alır sanmak", "Genişliğe de bak"], ["Farklı bardaklarla karşılaştırmak", "Aynı bardağı kullan"],
                 ["Bardağı tam doldurmamak", "Her seferinde tam doldur"]],
                [("Standart olmayan ölçü nedir?", "Bardak, fincan ya da kepçe gibi herkeste farklı olabilen ölçülerdir."),
                 ("Sıvıyı ölçmek için standart birim var mı?", "Evet, litre; 3. sınıfta öğreneceksin."),
                 ("Neden sonuçlar farklı çıkar?", "Kullanılan bardakların büyüklüğü farklı olabilir.")])


def u20():
    sets = [("Yönergeyi izle", [(m_yonerge(6), 20)]),
            ("Yolu bul", [(m_yon_bul(6), 20)]),
            ("Sağ ve sol", [(m_sag_sol(), 20)]),
            ("Konum", [(m_raf(), 10), (m_kutu_konum(), 10)]),
            ("Karışık", [(m_yonerge(6), 10), (m_yon_bul(6), 10)])]
    return unit("yon-ve-konum", "G", "MAT.2.3.6", 20, "Yön ve Konum: Yönergeleri İzleme", "Yön ve Konum",
                "Mesafe ve yönleri içerecek şekilde hedefe ulaşmak için uygun stratejilere karar verir; kareli zeminde sağa, sola, yukarı ve aşağı yönergeleri izler ve oluşturur.",
                "2. sınıf yön ve konum çalışma kâğıdı: kareli zeminde yönergeleri izleme, hedefe giden yolu bulma, sağ ve sol, raflarda ve kutunun çevresinde konum. 100 soru ve cevap anahtarı.",
                "Önce yön, sonra kare sayısı", "Başladığın kareyi sayma.", sets,
                ["Yönergede yön (sağa, sola, yukarı, aşağı) ve adım (kare) sayısı vardır.",
                 "Hedefe giderken yatay ve dikey adımları ayrı ayrı sayarız.",
                 "Başladığımız kareyi saymayız; her geçtiğimiz kare bir adımdır."],
                [("2 sağa, 3 yukarı", ["Yatay 2 kare", "Dikey 3 kare"], "Hedef kare"), ("Hedef 1 sola, 2 aşağı", ["Sola 1", "Aşağı 2"], "1 kare sola, 2 kare aşağı")],
                [["Sağ ile solu karıştırmak", "Kâğıda göre sağ ve sol"], ["Başlangıç karesini saymak", "Bir sonraki kareden say"],
                 ["Yönleri sırasız uygulamak", "Yönergedeki sırayı izle"]],
                [("Kareli zemin ne işe yarar?", "Adımları saymayı kolaylaştırır."),
                 ("Bir hedefe farklı yollardan gidilir mi?", "Evet, önce yukarı sonra sağa gitmek de aynı yere varır."),
                 ("Yönerge oluşturmak nasıl yapılır?", "Kaç kare ve hangi yöne gidileceğini sırayla yazarız.")])


def u21():
    d = B.u21
    hangisi, tamamla, harf = from_unit(d, "hangisi"), from_unit(d, "tamamla"), from_unit(d, "harf")
    sets = [("Simetrik şekli bulma", [(hangisi, 20)]),
            ("Doğru tamamlanmış şekil", [(tamamla, 20)]),
            ("Harflerde simetri", [(harf, 20)]),
            ("Simetrik mi?", [(hangisi, 10), (harf, 10)]),
            ("Karışık", [(hangisi, 7), (tamamla, 7), (harf, 6)])]
    return unit("simetri", "G", "MAT.2.3.7", 21, "Simetri: Simetrik Şekilleri Ayırt Etme", "Simetri",
                "Verilen şekiller arasından simetrik olanları ayırt eder; simetri doğrusunun iki yanındaki parçaların eş olduğunu fark eder.",
                "2. sınıf simetri çalışma kâğıdı: kareli zeminde simetrik şekli bulma, doğru tamamlanmış simetrik şekil, harflerde simetri. 100 soru ve cevap anahtarı.",
                "Katla: iki yarı üst üste gelir mi?", "Simetri doğrusunun iki yanı ayna görüntüsüdür.", sets,
                ["Bir şekil bir doğru boyunca katlandığında iki yarısı tam üst üste geliyorsa şekil simetriktir.",
                 "Bu doğruya simetri doğrusu denir. Doğrunun iki yanındaki parçalar eştir.",
                 "Kareli zeminde her kare, simetri doğrusuna eşit uzaklıkta diğer tarafa düşer."],
                [("A harfi", ["Ortadan dikey katlanınca örtüşür"], "Simetrik"), ("F harfi", ["Hiçbir katlamada örtüşmez"], "Simetrik değil")],
                [["Kaydırılmış şekli simetrik sanmak", "Ayna görüntüsü gibi olmalı"], ["Kareleri farklı uzaklığa koymak", "Doğruya eşit uzaklık"],
                 ["Yalnızca dikey doğruya bakmak", "Yatay simetri de olabilir"]],
                [("Simetri nerede görülür?", "Kelebek kanatlarında, yapraklarda, binalarda."),
                 ("Daire simetrik midir?", "Evet, merkezden geçen her doğruya göre simetriktir."),
                 ("Ayna simetriyi nasıl gösterir?", "Aynayı simetri doğrusuna koyarsan şeklin tamamını görürsün.")])


def u22():
    sets = [("Çetele", [(m_cetele(25), 20)]),
            ("Nesne grafiği", [(m_veri(9, "nesne", (0, 1)), 20)]),
            ("Sütun grafiği", [(m_veri(9, "sutun", (0, 1)), 20)]),
            ("Fark ve toplam", [(m_veri(12, "nesne", (2, 3), (2,)), 10), (m_veri(12, "sutun", (2, 3), (2,)), 10)]),
            ("Veriye dayalı karar", [(m_karar(9), 10), (m_veri(15, "cetele", (2, 3), (2,)), 10)])]
    return unit("veri-toplama-ve-grafikler", "V", "MAT.2.4.1", 22, "Veri Toplama: Çetele, Nesne ve Sütun Grafiği", "Veri Toplama",
                "Kategorik veriye dayalı en çok iki veri grubu ile çalışır; veriyi çetele, nesne grafiği ve sütun grafiğiyle düzenler, yorumlar ve veriye dayalı karar verir.",
                "2. sınıf veri toplama çalışma kâğıdı: çetele, nesne grafiği, sütun grafiği okuma, iki veri grubunu karşılaştırma, fark ve toplam, veriye dayalı karar. 100 soru ve cevap anahtarı.",
                "Grafiği oku, sonra karşılaştır", "En uzun sütun en çok seçileni gösterir.", sets,
                ["Verileri çetele ile toplar, sonra nesne grafiği ya da sütun grafiğiyle gösteririz.",
                 "Sütun grafiğinde sütunun yüksekliği o seçeneğin sayısını gösterir.",
                 "İki veri grubunu karşılaştırırken farkı çıkarma ile, toplamı toplama ile buluruz."],
                [("Kedi 8, kuş 5", ["8 − 5"], "Kedi 3 fazla"), ("Elma 6, muz 4", ["6 + 4"], "10 öğrenci")],
                [["Sütunun ucunu yanlış okumak", "Sütunun ucundan sola yatay bak"], ["Fark yerine toplam bulmak", "“Kaç fazla” çıkarma ister"],
                 ["Çetelenin beşli grubunu 4 saymak", "Bir grup 5 eder"]],
                [("Sütun grafiği nedir?", "Verileri farklı yükseklikteki sütunlarla gösteren grafiktir."),
                 ("Nesne grafiği ile sütun grafiği farkı?", "Nesne grafiğinde simgeler, sütun grafiğinde sütunlar kullanılır."),
                 ("Veriye dayalı karar ne demek?", "Toplanan bilgilere bakarak seçim yapmaktır.")])


UNITS = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12, u13, u14, u15, u16, u17, u18, u19, u20, u21, u22]
