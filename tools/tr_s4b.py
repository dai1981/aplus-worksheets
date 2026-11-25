# -*- coding: utf-8 -*-
"""Türkiye 4. sınıf: İşlemlerden Cebirsel Düşünmeye — 12〜18 単元（tr_run.py 4）。"""
import tr_g as G
from tr_g import unit, cap, num, oku, tl, mcq, M, alt_alta, near
from tr_s3b import terazi


def setup(rnd):
    pass


def ri(a, b):
    return G.R.randint(a, b)


def ch(xs):
    return G.R.choice(list(xs))


def sh(xs):
    return G.sh(xs)


def r_(n, b):
    return (n + b // 2) // b * b


# ============================================================ 12. zihinden toplama ve çıkarma
def u12():
    def yuzluk():
        k = ri(0, 1)
        a = ri(11, 89) * 100
        b = ri(1, 9) * 100 + ch([0, 0, 50])
        if k == 0:
            if a + b > 9999:
                return None
            return mcq("Zihinden hesapla: %s + %s" % (num(a), num(b)), num(a + b), near(a + b, (100, -100, 1000, 50)),
                       "Yüzlükleri toplarız: %s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))
        if a - b <= 0:
            return None
        return mcq("Zihinden hesapla: %s − %s" % (num(a), num(b)), num(a - b), near(a - b, (100, -100, 1000, 50)),
                   "Yüzlükleri çıkarırız: %s − %s = <b>%s</b>." % (num(a), num(b), num(a - b)))

    def yakin():
        a = ri(1200, 8800)
        b = ch([99, 199, 299, 998, 999, 1999, 101, 1001, 98, 2001])
        k = ri(0, 1)
        r = r_(b, 100)
        d = r - b
        if k == 0:
            g = a + b
            e = "%s yerine %s ekle, sonra %s: %s %s %d = <b>%s</b>." % (num(b), num(r), "fazlasını çıkar" if d > 0 else "eksiğini ekle", num(a + r), "−" if d > 0 else "+", abs(d), num(g))
            return mcq("Zihinden hesapla: %s + %s" % (num(a), num(b)), num(g), near(g, (1, -1, 2, -2, 10, 100)), e.replace("  ", " "))
        if a - b <= 0:
            return None
        g = a - b
        e = "%s yerine %s çıkar, sonra %s: %s %s %d = <b>%s</b>." % (num(b), num(r), "fazla çıkardığını geri ekle" if d > 0 else "eksiğini de çıkar", num(a - r), "+" if d > 0 else "−", abs(d), num(g))
        return mcq("Zihinden hesapla: %s − %s" % (num(a), num(b)), num(g), near(g, (1, -1, 2, -2, 10, 100)), e)

    def parca():
        a = ri(21, 89) * 100 + ri(1, 9) * 10
        b = ri(1, 9) * 100 + ri(1, 9) * 10
        k = ri(0, 1)
        if k == 0:
            g = a + b
            return mcq("Zihinden hesapla: %s + %s" % (num(a), num(b)), num(g), near(g, (10, -10, 100, -100, 110)),
                       "Önce %s, sonra %s eklenir: %s + %s = %s, %s + %s = <b>%s</b>." % (num(b // 100 * 100), num(b % 100), num(a), num(b // 100 * 100), num(a + b // 100 * 100), num(a + b // 100 * 100), num(b % 100), num(g)))
        g = a - b
        return mcq("Zihinden hesapla: %s − %s" % (num(a), num(b)), num(g), near(g, (10, -10, 100, -100, 110)),
                   "Önce %s, sonra %s çıkarılır: <b>%s</b>." % (num(b // 100 * 100), num(b % 100), num(g)))

    def tamamla():
        t = ch([1000, 2000, 5000, 10000])
        a = ri(1, t // 10 - 1) * 10
        return mcq("%s sayısına kaç eklersek %s olur?" % (num(a), num(t)), num(t - a), near(t - a, (10, -10, 100, -100, 1000)),
                   "%s − %s = <b>%s</b>." % (num(t), num(a), num(t - a)))

    def uclu():
        xs = [ri(1, 9) * 100 + ch([25, 50, 75, 0]) for _ in range(3)]
        g = sum(xs)
        return mcq("Zihinden hesapla: %s" % " + ".join(num(x) for x in xs), num(g), near(g, (100, -100, 25, -25, 50)),
                   "Kolay toplanan sayıları önce topla (ör. 25 + 75 = 100): <b>%s</b>." % num(g))

    def problem():
        nm = G.K.next()
        a = ri(15, 80) * 100
        b = ri(1, 9) * 100 + ch([0, 50])
        k = ri(0, 2)
        if k == 0:
            q = "%s bisiklet almak için %s TL biriktirdi. Annesi %s TL daha verdi. %s kaç lirası oldu?" % (nm, num(a), num(b), "Toplam")
            g = a + b
        elif k == 1:
            q = "Bir okulun kütüphanesinde %s kitap vardı. %s kitap okullara bağışlandı. Kaç kitap kaldı?" % (num(a), num(b))
            g = a - b
        else:
            q = "Bir köprüden sabah %s, akşam %s araç geçti. Akşam sabahtan kaç araç fazla geçti?" % (num(b), num(a))
            g = a - b
        return mcq(q, num(g), near(g, (100, -100, 1000, 50)), "%s %s %s = <b>%s</b>." % (num(max(a, b) if k else a), "+" if k == 0 else "−", num(b if k < 2 else b), num(g)) if k < 2 else "%s − %s = <b>%s</b>." % (num(a), num(b), num(g)))

    sets = [("Yüzlüklerle zihinden işlem", [(yuzluk, 20)]),
            ("Yuvarlak sayıya tamamlama", [(yakin, 20)]),
            ("Parçalayarak işlem", [(parca, 20)]),
            ("Tamamlama ve kolay toplama", [(tamamla, 10), (uclu, 10)]),
            ("Problemler", [(problem, 20)])]
    return unit("zihinden-toplama-ve-cikarma", "I", "MAT.4.2.1", 12, "Zihinden Toplama ve Çıkarma Stratejileri", "Zihinden Toplama ve Çıkarma",
                "Zihinden toplama ve çıkarma işlemlerini sayıların uygun parçalarını belirleyerek ve parçaların özelliklerini ilişkilendirerek çözer.",
                "4. sınıf zihinden toplama ve çıkarma çalışma kâğıdı: yüzlüklerle işlem, yuvarlak sayıya tamamlama (998, 1999), parçalayarak toplama ve çıkarma, tamamlama ve problemler. 100 soru ve cevap anahtarı.",
                "Sayıyı kolay parçalara ayır", "998 yerine 1.000 ekle, sonra 2 çıkar.", sets,
                ["Zihinden işlemde sayıları kolay parçalara ayırırız: 3.450 + 230 = 3.450 + 200 + 30.",
                 "Yuvarlak sayıya yakın sayılarda önce yuvarlak sayıyla işlem yaparız: 2.400 + 999 = 2.400 + 1.000 − 1.",
                 "Çıkarmada fazla çıkardıysak farkı geri ekleriz: 5.300 − 998 = 5.300 − 1.000 + 2."],
                [("4.250 + 1.999", ["4.250 + 2.000 = 6.250", "6.250 − 1 = 6.249"], "6.249"), ("7.400 − 299", ["7.400 − 300 = 7.100", "7.100 + 1 = 7.101"], "7.101")],
                [["7.400 − 299: 7.400 − 300 − 1", "Fazla çıkardığın 1’i geri ekle: 7.101"], ["Basamakları karıştırmak", "Yüzlüğü yüzlükle, onluğu onlukla işle"],
                 ["Tamamlamada toplamak", "Kaç eklenirse olur: büyük sayıdan küçüğü çıkar"]],
                [("Zihinden işlem neden önemlidir?", "Kâğıt kalem olmadan hızlı hesap yapmamızı ve sonucu kontrol etmemizi sağlar."),
                 ("Hangi sayılar yuvarlak sayıdır?", "10, 100, 1.000 gibi sonu 0 ile biten ve kolay işlem yapılan sayılar."),
                 ("Her işlemde aynı strateji mi kullanılır?", "Hayır. Sayılara bakıp en kolay parçalamayı seçeriz.")])


# ============================================================ 13. dört basamaklı toplama ve çıkarma
def u13():
    def topla():
        a, b = ri(1000, 6999), ri(100, 2999)
        s = a + b
        noc = int("".join(str((int(x) + int(y)) % 10) for x, y in zip(str(a).rjust(4, "0"), str(b).rjust(4, "0"))))
        return mcq("Alt alta toplama yap." + alt_alta([str(a), str(b)], "+"), num(s), [num(noc) if noc != s else num(s + 1), num(s + 10), num(s - 100), num(s + 1000)],
                   "Birlerden başla, eldeyi bir sonraki basamağa ekle: <b>%s</b>." % num(s))

    def cikar():
        a = ri(2000, 9999)
        b = ri(500, a - 100)
        d = a - b
        bad = int("".join(str(abs(int(x) - int(y))) for x, y in zip(str(a).rjust(4, "0"), str(b).rjust(4, "0"))))
        return mcq("Alt alta çıkarma yap." + alt_alta([str(a), str(b)], "−"), num(d), [num(bad) if bad != d else num(d + 1), num(d + 10), num(d - 100), num(d + 1000)],
                   "Üstteki rakam küçükse bir üst basamaktan 1 onluk (yüzlük, binlik) bozarız: <b>%s</b>." % num(d))

    def sifirli():
        a = ch([1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]) + ch([0, 0, 100, 500])
        b = ri(101, a - 100)
        d = a - b
        return mcq("%s − %s işleminin sonucu kaçtır?" % (num(a), num(b)), num(d), [num(d + 1000), num(d + 10), num(d - 10), num(d + 100)],
                   "Sıfırlı sayıdan çıkarırken binliği, yüzlüğü ve onluğu sırayla bozarız: <b>%s</b>." % num(d))

    def eksik():
        a, b = ri(1000, 5000), ri(500, 4000)
        s = a + b
        k = ri(0, 2)
        if k == 0:
            return mcq("%s + ? = %s ise ? kaçtır?" % (num(a), num(s)), num(b), [num(s + a), num(b + 10), num(b - 100)], "Toplamdan bilinen toplanan çıkarılır: %s − %s = <b>%s</b>." % (num(s), num(a), num(b)))
        if k == 1:
            return mcq("? − %s = %s ise ? kaçtır?" % (num(b), num(a)), num(s), [num(a - b) if a > b else num(s + 100), num(s + 10), num(s - 100)], "Eksilen = fark + çıkan: %s + %s = <b>%s</b>." % (num(a), num(b), num(s)))
        return mcq("%s − ? = %s ise ? kaçtır?" % (num(s), num(a)), num(b), [num(s + a), num(b + 100), num(b - 10)], "Çıkan = eksilen − fark: %s − %s = <b>%s</b>." % (num(s), num(a), num(b)))

    def kontrol():
        a, b = ri(1000, 6000), ri(500, 3000)
        s = a + b
        k = ri(0, 1)
        if k == 0:
            return mcq("%s − %s = %s işleminin sağlaması hangi işlemle yapılır?" % (num(s), num(b), num(a)), "%s + %s = %s" % (num(a), num(b), num(s)),
                       ["%s − %s = %s" % (num(s), num(a), num(b)), "%s + %s = %s" % (num(s), num(b), num(s + b)), "%s − %s = %s" % (num(a), num(b), num(a - b)) if a > b else "%s × 2" % num(a)],
                       "Çıkarmanın sağlaması toplamayla yapılır: fark + çıkan = eksilen. <b>%s + %s = %s</b>." % (num(a), num(b), num(s)))
        wrong = s + ch([10, 100, -10])
        return mcq("Defne %s + %s = %s buldu. Sağlama yapınca ne fark eder?" % (num(a), num(b), num(wrong)), "Sonuç yanlış, doğrusu %s" % num(s),
                   ["Sonuç doğru", "Sonuç yanlış, doğrusu %s" % num(wrong + 10), "Sonuç yanlış, doğrusu %s" % num(a - b if a > b else s + 1)],
                   "%s − %s = %s, %s değil. Doğru toplam <b>%s</b>." % (num(wrong), num(b), num(wrong - b), num(a), num(s)))

    def problem():
        nm = G.K.next()
        k = ri(0, 3)
        a, b = ri(1200, 5800), ri(800, 3900)
        if k == 0:
            q, g = "Bir tiyatro salonunda cumartesi %s, pazar %s seyirci vardı. İki günde toplam kaç seyirci vardı?" % (num(a), num(b)), a + b
        elif k == 1:
            a = a + b
            q, g = "Bir çiftlikte %s tavuk var. %s tanesi satıldı. Kaç tavuk kaldı?" % (num(a), num(b)), a - b
        elif k == 2:
            q, g = "%s %s TL’lik bir bilgisayar için %s TL biriktirdi. Daha kaç lira biriktirmelidir?" % (nm, num(a + b), num(a)), b
        else:
            q, g = "Bir yolun %s metresi asfaltlandı, %s metresi kaldı. Yol kaç metredir?" % (num(a), num(b)), a + b
        return mcq(q, num(g), near(g, (10, -10, 100, -100, 1000)), "Doğru işlemi seç ve hesapla: <b>%s</b>." % num(g))

    sets = [("Dört basamaklı toplama", [(topla, 20)]),
            ("Dört basamaklı çıkarma", [(cikar, 20)]),
            ("Sıfırlı sayılardan çıkarma", [(sifirli, 20)]),
            ("Eksik sayı ve sağlama", [(eksik, 12), (kontrol, 8)]),
            ("Problemler", [(problem, 20)])]
    return unit("dort-basamakli-toplama-ve-cikarma", "I", "MAT.4.2.2", 13, "Dört Basamaklı Sayılarla Toplama ve Çıkarma", "Toplama ve Çıkarma",
                "En çok dört basamaklı sayılarla toplama ve çıkarma işlemlerini yapılandırır.",
                "4. sınıf toplama ve çıkarma çalışma kâğıdı: dört basamaklı sayılarla eldeli toplama, onluk bozarak çıkarma, sıfırlı sayılardan çıkarma, eksik sayı, sağlama ve problemler. 100 soru ve cevap anahtarı.",
                "Birlerden başla, basamakları hizala", "Çıkarmanın sağlaması: fark + çıkan = eksilen.", sets,
                ["Alt alta işlem yaparken birler birlerin, onlar onların altına gelir. İşleme birlerden başlarız.",
                 "Toplamada bir basamağın toplamı 10 veya fazlaysa 1 eldeyi bir sonraki basamağa ekleriz.",
                 "Çıkarmada üstteki rakam küçükse bir üst basamaktan 1 bozarız. 0 olan basamaklarda bozma bir üst basamaktan devam eder."],
                [("5.003 − 1.268", ["Birler için binlik → yüzlük → onluk bozulur", "13 − 8 = 5, 9 − 6 = 3, 9 − 2 = 7, 4 − 1 = 3"], "3.735"),
                 ("Sağlama: 3.735 + 1.268", ["Toplam eksileni vermeli"], "5.003")],
                [["Küçük rakamdan büyüğü ters çıkarmak (3 − 8 yerine 8 − 3)", "Üst basamaktan 1 boz: 13 − 8"], ["Bozduğun basamağı 1 azaltmayı unutmak", "Bozulan basamak 1 azalır"],
                 ["Eldeyi eklemeyi unutmak", "Elde bir sonraki basamağın toplamına eklenir"]],
                [("Sağlama ne işe yarar?", "Sonucun doğru olup olmadığını kontrol eder. Toplamanın sağlaması çıkarmayla, çıkarmanın sağlaması toplamayla yapılır."),
                 ("Sıfırlı sayıdan nasıl çıkarılır?", "5.000 − 1.268 gibi işlemlerde binlik bozulur; 0 olan yüzler ve onlar 9 olur, birler 10 olur."),
                 ("Problemde hangi işlemi seçeceğimi nasıl anlarım?", "“Toplam, hepsi” toplama; “kaldı, fark, daha kaç” çıkarma işaretidir.")])


# ============================================================ 14. çarpma ve bölmede tahmin
def u14():
    def carpim():
        a, b = ri(11, 98), ri(11, 49)
        if a % 10 in (5,) or b % 10 == 5:
            return None
        ra, rb = r_(a, 10), r_(b, 10)
        g = ra * rb
        return mcq("%d × %d işleminin sonucunu sayıları en yakın onluğa yuvarlayarak tahmin et." % (a, b), num(g), [num(g * 10), num(a * b), num((ra + 10) * rb), num(ra * rb // 10)],
                   "%d ≈ %d, %d ≈ %d. Tahmin: %d × %d = <b>%s</b>." % (a, ra, b, rb, ra, rb, num(g)))

    def carpim3():
        a, b = ri(110, 890), ri(2, 9)
        if a % 100 == 50:
            return None
        ra = r_(a, 100)
        g = ra * b
        return mcq("%d × %d işleminin sonucunu %d sayısını en yakın yüzlüğe yuvarlayarak tahmin et." % (a, b, a), num(g), [num(a * b), num(g + 100 * b), num(g // 10), num(ra + b)],
                   "%d ≈ %d. Tahmin: %d × %d = <b>%s</b>." % (a, ra, ra, b, num(g)))

    def bolum():
        b = ri(2, 9)
        q = ri(11, 99) * 10
        a = q * b + ri(1, b - 1) * ch([1, -1]) * ri(1, 4)
        if a <= 0:
            return None
        g = q
        return mcq("%s ÷ %d işleminin sonucunu tahmin etmek için en uygun işlem hangisidir?" % (num(a), b), "%s ÷ %d = %s" % (num(q * b), b, num(q)),
                   ["%s ÷ %d = %s" % (num(r_(a, 1000) or 1000), b, num((r_(a, 1000) or 1000) // b)) if (r_(a, 1000) or 1000) % b == 0 else "%s ÷ %d = %s" % (num(q * b + 100 * b), b, num(q + 100)),
                    "%s ÷ %d = %s" % (num(q * b * 10), b, num(q * 10)), "%s − %d = %s" % (num(q * b), b, num(q * b - b))],
                   "%s sayısına yakın ve %d ile kolay bölünen sayı %s: <b>%s ÷ %d = %s</b>." % (num(a), b, num(q * b), num(q * b), b, num(g)))

    def aralik():
        a, b = ri(21, 89), ri(21, 89)
        p = a * b
        lo, hi = a // 10 * 10 * (b // 10 * 10), (a // 10 + 1) * 10 * ((b // 10 + 1) * 10)
        return mcq("%d × %d çarpımı hangi iki sayı arasındadır?" % (a, b), "%s ile %s" % (num(lo), num(hi)),
                   ["%s ile %s" % (num(lo // 10), num(hi // 10)), "%s ile %s" % (num(hi), num(hi * 2)), "%s ile %s" % (num(lo * 10), num(hi * 10))],
                   "%d × %d = %s ve %d × %d = %s. Çarpım %s bu ikisi arasındadır." % (a // 10 * 10, b // 10 * 10, num(lo), (a // 10 + 1) * 10, (b // 10 + 1) * 10, num(hi), num(p)))

    def problem():
        nm = G.K.next()
        k = ri(0, 2)
        if k == 0:
            a, b = ri(18, 49), ri(19, 58)
            ra, rb = r_(a, 10), r_(b, 10)
            if a % 10 == 5 or b % 10 == 5:
                return None
            q = "Bir otobüste %d koltuk var. %d otobüs dolu olarak geziye gitti. Geziye yaklaşık kaç kişi katıldı?" % (a, b)
            return mcq(q, num(ra * rb), [num(ra * rb * 10), num(ra + rb), num(ra * rb // 10)], "%d ≈ %d, %d ≈ %d. Yaklaşık %d × %d = <b>%s</b> kişi." % (a, ra, b, rb, ra, rb, num(ra * rb)))
        if k == 1:
            b = ch([2, 3, 4, 5])
            q_ = ri(2, 9) * 100
            a = q_ * b + ri(-20, 20)
            q = "%s %s TL’yi %d kardeşe eşit paylaştırmak istiyor. Her kardeşe yaklaşık kaç lira düşer?" % (nm, num(a), b)
            return mcq(q, num(q_), [num(q_ * 10), num(q_ // 10), num(a - b)], "%s ≈ %s. %s ÷ %d = <b>%s</b>." % (num(a), num(q_ * b), num(q_ * b), b, num(q_)))
        a, b = ri(210, 790), ri(3, 9)
        if a % 100 == 50:
            return None
        ra = r_(a, 100)
        q = "Bir kitap %d sayfa. %s %d kitabı okursa yaklaşık kaç sayfa okumuş olur?" % (a, nm, b)
        return mcq(q, num(ra * b), [num(a + b), num(ra * b * 10), num(ra + 100 * b)], "%d ≈ %d. %d × %d = <b>%s</b>." % (a, ra, ra, b, num(ra * b)))

    sets = [("İki basamaklı sayılarla çarpımı tahmin", [(carpim, 20)]),
            ("Üç basamaklı sayılarla çarpımı tahmin", [(carpim3, 20)]),
            ("Bölümü tahmin", [(bolum, 20)]),
            ("Çarpım hangi aralıkta?", [(aralik, 20)]),
            ("Problemlerde tahmin", [(problem, 20)])]
    return unit("carpma-ve-bolmede-tahmin", "I", "MAT.4.2.3", 14, "Çarpma ve Bölme İşlemlerinin Sonucunu Tahmin Etme", "Çarpma ve Bölmede Tahmin",
                "Çarpma ve bölme işlemlerinin sonuçlarını tahmin eder; tahminini deneyimleriyle ilişkilendirerek çıkarım ve yargıda bulunur.",
                "4. sınıf çarpma ve bölmede tahmin çalışma kâğıdı: sayıları yuvarlayarak çarpımı ve bölümü tahmin etme, çarpımın aralığı ve tahmin problemleri. 100 soru ve cevap anahtarı.",
                "Önce yuvarla, sonra kolay işlem yap", "Bölmede bölünene yakın, kolay bölünen sayı seç.", sets,
                ["Çarpımı tahmin ederken çarpanları en yakın onluğa ya da yüzlüğe yuvarlarız: 48 × 21 ≈ 50 × 20 = 1.000.",
                 "Bölümü tahmin ederken bölüneni, bölene kolay bölünen yakın bir sayıya yuvarlarız: 812 ÷ 4 ≈ 800 ÷ 4 = 200.",
                 "Tahmin, gerçek sonucun yaklaşık değeridir. Sonucu kontrol ederken işe yarar."],
                [("38 × 52", ["38 ≈ 40, 52 ≈ 50", "40 × 50 = 2.000"], "yaklaşık 2.000"), ("1.796 ÷ 6", ["1.796 ≈ 1.800", "1.800 ÷ 6 = 300"], "yaklaşık 300")],
                [["Tahmini tam sonuç sanmak", "Tahmin yaklaşık değerdir; “yaklaşık” sözcüğüne dikkat et"], ["40 × 50 = 200", "Sıfırları da say: 4 × 5 = 20, iki sıfır: 2.000"],
                 ["Bölmede en yakın yüzlüğe yuvarlayıp zor bölme yapmak", "Bölene kolay bölünen sayıyı seç"]],
                [("Tahmin ne zaman kullanılır?", "Alışverişte paranın yetip yetmeyeceğini düşünürken ya da bir işlemin sonucunu kontrol ederken."),
                 ("Her zaman en yakın onluğa mı yuvarlarız?", "Hayır. Kolay hesap yapmamızı sağlayan yuvarlamayı seçeriz."),
                 ("Tahmin ile gerçek sonuç çok farklıysa ne yapmalıyım?", "İşlemi yeniden kontrol et; büyük olasılıkla bir hata vardır.")])


# ============================================================ 15. zihinden çarpma ve bölme
def u15():
    def on_yuz():
        a = ri(2, 999)
        b = ch([10, 100, 1000])
        k = ri(0, 1)
        if k == 0:
            if a * b > 999999:
                return None
            g = a * b
            return mcq("Zihinden hesapla: %s × %s" % (num(a), num(b)), num(g), [num(g * 10), num(g // 10) if g // 10 != a else num(a + b), num(a + b)],
                       "%s ile çarparken sayının sağına %d sıfır yazılır: <b>%s</b>." % (num(b), len(str(b)) - 1, num(g)))
        a = a * b
        if a > 999999:
            return None
        g = a // b
        return mcq("Zihinden hesapla: %s ÷ %s" % (num(a), num(b)), num(g), [num(g * 10), num(g // 10) if g >= 10 else num(g + 10), num(a - b)],
                   "Sondaki sıfırlardan %d tanesi silinir: <b>%s</b>." % (len(str(b)) - 1, num(g)))

    def sifirli():
        a = ri(2, 9) * ch([10, 100])
        b = ri(2, 9) * ch([10, 100])
        g = a * b
        return mcq("Zihinden hesapla: %s × %s" % (num(a), num(b)), num(g), [num(g * 10), num(g // 10), num(a // 10 * b // 10 if a >= 100 and b >= 100 else g + 100)],
                   "Sıfırsız kısımlar çarpılır (%d × %d = %d), sonra sıfırlar sona eklenir: <b>%s</b>." % (int(str(a).rstrip("0")), int(str(b).rstrip("0")), int(str(a).rstrip("0")) * int(str(b).rstrip("0")), num(g)))

    def kisayol():
        k = ri(0, 4)
        a = ri(12, 98)
        if k == 0:
            g = a * 5
            return mcq("%d × 5 işlemini kısa yoldan yap." % a, num(g), [num(a * 50), num(a + 5), num(a * 10)], "× 5 = × 10 ÷ 2: %s ÷ 2 = <b>%s</b>." % (num(a * 10), num(g)))
        if k == 1:
            a = ri(4, 40) * 2
            g = a * 25
            return mcq("%d × 25 işlemini kısa yoldan yap." % a, num(g), [num(g * 10), num(a * 20), num(g // 10)], "× 25 = × 100 ÷ 4: %s ÷ 4 = <b>%s</b>." % (num(a * 100), num(g)))
        if k == 2:
            g = a * 9
            return mcq("%d × 9 işlemini kısa yoldan yap." % a, num(g), [num(a * 10), num(a * 9 + a), num(g - 1)], "× 9 = × 10 − 1 kez: %s − %d = <b>%s</b>." % (num(a * 10), a, num(g)))
        if k == 3:
            g = a * 11
            return mcq("%d × 11 işlemini kısa yoldan yap." % a, num(g), [num(a * 10), num(g + 10), num(g - 10)], "× 11 = × 10 + 1 kez: %s + %d = <b>%s</b>." % (num(a * 10), a, num(g)))
        g = a * 4
        return mcq("%d × 4 işlemini “iki kez ikiye katla” yoluyla yap." % a, num(g), [num(a * 2), num(a * 8), num(g + 4)], "%d × 2 = %d, %d × 2 = <b>%d</b>." % (a, a * 2, a * 2, g))

    def bol_kisayol():
        k = ri(0, 1)
        if k == 0:
            a = ri(11, 99) * 10
            g = a // 5
            return mcq("%s ÷ 5 işlemini kısa yoldan yap." % num(a), num(g), [num(g * 10), num(a // 10), num(g + 5)], "÷ 5 = ÷ 10 × 2: %s × 2 = <b>%s</b>." % (num(a // 10), num(g)))
        a = ri(3, 40) * 4
        g = a // 4
        return mcq("%d ÷ 4 işlemini “iki kez yarıya böl” yoluyla yap." % a, num(g), [num(a // 2), num(g * 2 + 1), num(g + 4)], "%d ÷ 2 = %d, %d ÷ 2 = <b>%d</b>." % (a, a // 2, a // 2, g))

    def eksik():
        b = ch([10, 100, 1000])
        a = ri(3, 99)
        k = ri(0, 1)
        if k == 0:
            return mcq("%d × ? = %s ise ? kaçtır?" % (a, num(a * b)), num(b), [num(b * 10), num(b // 10) if b > 10 else "1", num(a * b - a)], "%s ÷ %d = <b>%s</b>." % (num(a * b), a, num(b)))
        return mcq("? ÷ %s = %d ise ? kaçtır?" % (num(b), a), num(a * b), [num(a * b * 10), num(a * b // 10), num(a + b)], "Bölünen = bölüm × bölen: %d × %s = <b>%s</b>." % (a, num(b), num(a * b)))

    def problem():
        nm = G.K.next()
        k = ri(0, 2)
        if k == 0:
            a, b = ri(2, 9) * 10, ch([10, 100])
            q = "Bir kutuda %d kalem var. %s kutuda kaç kalem vardır?" % (a, num(b))
            return mcq(q, num(a * b), [num(a * b * 10), num(a + b), num(a * b // 10)], "%d × %s = <b>%s</b>." % (a, num(b), num(a * b)))
        if k == 1:
            a = ri(12, 60) * 4
            q = "%s %d TL’yi 4 eşit parçaya bölüp her hafta bir parçasını harcayacak. Haftada kaç lira harcar?" % (nm, a)
            return mcq(q, num(a // 4), [num(a // 2), num(a - 4), num(a // 4 + 4)], "%d ÷ 2 = %d, %d ÷ 2 = <b>%d</b>." % (a, a // 2, a // 2, a // 4))
        a = ri(11, 49)
        q = "Bir biletin fiyatı 25 TL. %d bilet kaç liradır?" % a
        return mcq(q, num(a * 25), [num(a * 20), num(a * 25 + 25), num(a * 100)], "× 25 = × 100 ÷ 4: %s ÷ 4 = <b>%s</b>." % (num(a * 100), num(a * 25)) if a % 4 == 0 else "%d × 25 = %d × 100 ÷ 4 = <b>%s</b>." % (a, a, num(a * 25)))

    sets = [("10, 100 ve 1.000 ile çarpma ve bölme", [(on_yuz, 20)]),
            ("Sonu sıfırlı sayılarla çarpma", [(sifirli, 20)]),
            ("Kısa yoldan çarpma", [(kisayol, 20)]),
            ("Kısa yoldan bölme ve eksik sayı", [(bol_kisayol, 10), (eksik, 10)]),
            ("Problemler", [(problem, 20)])]
    return unit("zihinden-carpma-ve-bolme", "I", "MAT.4.2.4", 15, "Zihinden Çarpma ve Bölme ve Kısa Yollar", "Zihinden Çarpma ve Bölme",
                "Zihinden çarpma ve bölme işlemlerini ve bu işlemlerde kullanılan kısa yolları yapılandırır.",
                "4. sınıf zihinden çarpma ve bölme çalışma kâğıdı: 10, 100 ve 1.000 ile çarpma ve bölme, sonu sıfırlı sayılarla çarpma, 5, 25, 9 ve 11 ile kısa yoldan çarpma, kısa yoldan bölme ve problemler. 100 soru ve cevap anahtarı.",
                "× 10: sona bir sıfır ekle", "÷ 10: sondaki bir sıfırı sil.", sets,
                ["Bir sayıyı 10, 100, 1.000 ile çarparken sayının sağına 1, 2, 3 sıfır yazarız. Böylerken sondaki sıfırları sileriz.",
                 "Sonu sıfırlı sayıları çarparken sıfırsız kısımları çarpar, sonra bütün sıfırları sona ekleriz: 30 × 400 = 12.000.",
                 "Kısa yollar: × 5 = × 10 ÷ 2, × 25 = × 100 ÷ 4, × 9 = × 10 − 1 kez, × 11 = × 10 + 1 kez."],
                [("60 × 300", ["6 × 3 = 18", "Üç sıfır ekle"], "18.000"), ("48 × 25", ["48 × 100 = 4.800", "4.800 ÷ 4"], "1.200")],
                [["60 × 300 = 1.800", "Bütün sıfırları say: 18 ve üç sıfır, 18.000"], ["4.500 ÷ 100 = 450", "İki sıfır silinir: 45"],
                 ["× 9 için × 10 yapıp 1 çıkarmak", "Sayının kendisi çıkarılır: 23 × 9 = 230 − 23"]],
                [("Neden 10 ile çarpınca sona sıfır eklenir?", "Her basamak bir üst basamağa kayar; birler onlar, onlar yüzler olur. Boşalan birler basamağına 0 yazılır."),
                 ("Kısa yollar her sayıda işe yarar mı?", "Evet, ama bazen normal işlem daha kolaydır. Sayılara bakıp en kolay yolu seç."),
                 ("1.000 ile bölünemeyen sayılar ne olur?", "4. sınıfta sonu yeterince sıfırlı sayıları böleriz; diğerleri kalanlı bölme olur.")])


# ============================================================ 16. çarpma ve bölme
def u16():
    def carp3x2():
        a, b = ri(102, 899), ri(12, 89)
        if b % 10 == 0:
            return None
        g = a * b
        bad = a * (b // 10) + a * (b % 10)
        return mcq("%s × %d işleminin sonucu kaçtır?" % (num(a), b), num(g), [num(bad), num(g + a), num(g - 10 * a), num(a * (b % 10) * 10 + a * (b // 10))],
                   "%s × %d = %s, %s × %d = %s. Toplam: <b>%s</b>." % (num(a), b % 10, num(a * (b % 10)), num(a), b // 10 * 10, num(a * (b // 10 * 10)), num(g)))

    def bol4x1():
        b = ri(2, 9)
        q = ri(120, 1999)
        a = q * b
        if a > 9999:
            return None
        return mcq("%s ÷ %d işleminin sonucu kaçtır?" % (num(a), b), num(q), [num(q + 1), num(q * 10) if q < 1000 else num(q - 100), num(q - 10), num(a - b)],
                   "Bölme işlemini soldan başlayarak yaparız. Sağlama: %s × %d = %s. Bölüm <b>%s</b>." % (num(q), b, num(a), num(q)))

    def kalanli():
        b = ri(3, 9)
        q = ri(100, 999)
        r = ri(1, b - 1)
        a = q * b + r
        return mcq("%s ÷ %d işleminde bölüm ve kalan nedir?" % (num(a), b), "bölüm %s, kalan %d" % (num(q), r),
                   ["bölüm %s, kalan %d" % (num(q + 1), r), "bölüm %s, kalan %d" % (num(q), (r + 1) % b or b - 1), "bölüm %s, kalan %d" % (num(q - 1), r + b)],
                   "%s × %d = %s, %s − %s = %d. Bölüm <b>%s</b>, kalan <b>%d</b>." % (num(q), b, num(q * b), num(a), num(q * b), r, num(q), r))

    def bol3x2():
        b = ri(12, 48)
        q = ri(3, 30)
        r = ri(0, b - 1) if G.R.random() < 0.5 else 0
        a = q * b + r
        if a > 999:
            return None
        if r == 0:
            return mcq("%s ÷ %d işleminin sonucu kaçtır?" % (num(a), b), str(q), [str(q + 1), str(q - 1), str(q * 10)], "Sağlama: %d × %d = %s. Bölüm <b>%d</b>." % (q, b, num(a), q))
        return mcq("%s ÷ %d işleminde bölüm ve kalan nedir?" % (num(a), b), "bölüm %d, kalan %d" % (q, r),
                   ["bölüm %d, kalan %d" % (q + 1, r), "bölüm %d, kalan %d" % (q - 1, r + b), "bölüm %d, kalan %d" % (q, r + 1 if r + 1 < b else r - 1)],
                   "%d × %d = %s, kalan %s − %s = %d. Bölüm <b>%d</b>, kalan <b>%d</b>." % (q, b, num(q * b), num(a), num(q * b), r, q, r))

    def iliski():
        b = ri(3, 12)
        q = ri(12, 99)
        r = ri(0, b - 1)
        a = q * b + r
        k = ri(0, 1)
        if k == 0:
            return mcq("Bir bölme işleminde bölen %d, bölüm %d ve kalan %d ise bölünen kaçtır?" % (b, q, r), num(a), [num(q * b), num(q * b - r) if r else num(a + b), num(q + b + r)],
                       "Bölünen = bölen × bölüm + kalan: %d × %d + %d = <b>%s</b>." % (b, q, r, num(a)))
        return mcq("%d × %d = %s ise %s ÷ %d kaçtır?" % (q, b, num(q * b), num(q * b), q), str(b), [str(q), str(b + 1), num(q * b - q)],
                   "Çarpma ve bölme ters işlemlerdir: <b>%d</b>." % b)

    def problem():
        nm = G.K.next()
        k = ri(0, 3)
        if k == 0:
            a, b = ri(15, 48), ri(12, 36)
            q = "Bir sinema salonunda %d sıra, her sırada %d koltuk var. Salonda kaç koltuk vardır?" % (b, a)
            return mcq(q, num(a * b), [num(a + b), num(a * b + a), num(a * b - b)], "%d × %d = <b>%s</b>." % (b, a, num(a * b)))
        if k == 1:
            b = ri(12, 30)
            qq = ri(8, 30)
            r = ri(1, b - 1)
            n = qq * b + r
            if n > 999:
                return None
            q = "%d öğrenci %d kişilik servislere biniyor. Hepsinin binmesi için en az kaç servis gerekir?" % (n, b)
            return mcq(q, str(qq + 1), [str(qq), str(qq + 2), str(r)], "%d ÷ %d = %d, kalan %d. Kalan öğrenciler için bir servis daha: <b>%d</b>." % (n, b, qq, r, qq + 1))
        if k == 2:
            b = ri(3, 9)
            qq = ri(110, 999)
            q = "Bir fabrikada %s oyuncak %d kutuya eşit olarak yerleştirildi. Her kutuda kaç oyuncak vardır?" % (num(qq * b), b)
            return mcq(q, num(qq), [num(qq + 1), num(qq * b - b), num(qq - 10)], "%s ÷ %d = <b>%s</b>." % (num(qq * b), b, num(qq)))
        a, b = ri(125, 450), ri(12, 24)
        q = "%s her ay %d TL biriktiriyor. %d ayda kaç lira biriktirir?" % (nm, a, b)
        return mcq(q, num(a * b), [num(a + b), num(a * b + a), num(a * (b - 1))], "%d × %d = <b>%s</b>." % (a, b, num(a * b)))

    sets = [("Üç basamaklıyı iki basamaklıyla çarpma", [(carp3x2, 20)]),
            ("Dört basamaklıyı bir basamaklıya bölme", [(bol4x1, 20)]),
            ("Kalanlı bölme", [(kalanli, 20)]),
            ("İki basamaklı bölenle bölme", [(bol3x2, 12), (iliski, 8)]),
            ("Problemler", [(problem, 20)])]
    return unit("carpma-ve-bolme", "I", "MAT.4.2.5", 16, "Çarpma ve Bölme İşlemleri ve Aralarındaki İlişki", "Çarpma ve Bölme",
                "Çarpma ve bölme işlemlerini tanır ve bu işlemleri birbiriyle ilişkilendirir.",
                "4. sınıf çarpma ve bölme çalışma kâğıdı: üç basamaklı sayıyı iki basamaklı sayıyla çarpma, dört basamaklı sayıyı bir basamaklı sayıya bölme, kalanlı bölme, iki basamaklı bölen, bölünen-bölen-bölüm-kalan ilişkisi ve problemler. 100 soru ve cevap anahtarı.",
                "Bölünen = bölen × bölüm + kalan", "Kalan her zaman bölenden küçüktür.", sets,
                ["İki basamaklı sayıyla çarparken önce birler basamağıyla, sonra onlar basamağıyla çarparız; ikinci çarpımı bir basamak sola kaydırarak yazar ve toplarız.",
                 "Bölmeye bölünenin en solundaki basamaklardan başlarız. Her adımda “kaç kez sığar?” diye sorarız.",
                 "Bölmenin sağlaması: bölen × bölüm + kalan = bölünen."],
                [("243 × 32", ["243 × 2 = 486", "243 × 30 = 7.290", "486 + 7.290"], "7.776"), ("1.957 ÷ 6", ["19 ÷ 6 = 3, kalan 1", "15 ÷ 6 = 2, kalan 3", "37 ÷ 6 = 6, kalan 1"], "bölüm 326, kalan 1")],
                [["243 × 32 işleminde ikinci satırı kaydırmamak", "Onlar basamağıyla çarpım bir basamak sola kayar (× 30)"], ["Kalanı bölenden büyük bırakmak", "Kalan bölenden büyükse bölüm 1 artmalıdır"],
                 ["Bölümün ortasındaki 0’ı unutmak", "Sığmayan adımda bölüme 0 yazılır: 1.224 ÷ 6 = 204"]],
                [("Bölmenin sağlaması nasıl yapılır?", "Bölen ile bölüm çarpılır, kalan eklenir. Sonuç bölüneni vermelidir."),
                 ("Kalan 0 ise ne demektir?", "Bölünen bölene tam bölünür."),
                 ("Problemde kalan ne anlama gelir?", "Duruma göre değişir: servis sorusunda kalan öğrenciler için bir araç daha gerekir; paylaştırmada kalan artar.")])


# ============================================================ 17. dört işlem problemleri
def u17():
    def iki_adim():
        nm = G.K.next()
        k = ri(0, 4)
        if k == 0:
            a, b, c = ri(12, 40), ri(3, 9), ri(20, 150)
            q = "%s tanesi %d TL olan %d defter ve %d TL’lik bir çanta aldı. Toplam kaç lira ödedi?" % (nm, a, b, c)
            g = a * b + c
            e = "%d × %d = %d, %d + %d = <b>%s</b>." % (a, b, a * b, a * b, c, num(g))
            w = [a * b, a + b + c, a * (b + c)]
        elif k == 1:
            p, n, m = ri(200, 900), ri(3, 9), ri(25, 90)
            if n * m >= p:
                return None
            q = "%s %d TL ile alışverişe çıktı. Tanesi %d TL olan %d oyuncak aldı. Kaç lirası kaldı?" % (nm, p, m, n)
            g = p - n * m
            e = "%d × %d = %d, %d − %d = <b>%s</b>." % (n, m, n * m, p, n * m, num(g))
            w = [n * m, p - m, p - n - m]
        elif k == 2:
            b, n = ri(3, 8), ri(12, 30)
            extra = ri(5, 30)
            q = "Bir sınıfta %d öğrenci var. Her öğrenciye %d kalem verildi ve %d kalem arttı. Başlangıçta kaç kalem vardı?" % (n, b, extra)
            g = n * b + extra
            e = "%d × %d = %d, %d + %d = <b>%s</b>." % (n, b, n * b, n * b, extra, num(g))
            w = [n * b, n * b - extra, n + b + extra]
        elif k == 3:
            t, b = ri(120, 480), ri(2, 6)
            t = t - t % b
            used = ri(10, 50)
            if used >= t // b:
                return None
            q = "%d ceviz %d kardeşe eşit paylaştırıldı. %s kendi payından %d ceviz yedi. %s kaç cevizi kaldı?" % (t, b, nm, used, "Elinde")
            g = t // b - used
            e = "%d ÷ %d = %d, %d − %d = <b>%s</b>." % (t, b, t // b, t // b, used, num(g))
            w = [t // b, t - used, t // b + used]
        else:
            a, b, c = ri(150, 500), ri(150, 500), ri(2, 5)
            q = "Bir fırın sabah %d, öğleden sonra %d ekmek yaptı. Ekmeklerin hepsi %d markete eşit olarak dağıtıldı. Her markete kaç ekmek gitti?" % (a, b, c)
            s = a + b
            if s % c:
                return None
            g = s // c
            e = "%d + %d = %d, %d ÷ %d = <b>%s</b>." % (a, b, s, s, c, num(g))
            w = [s, a // c + b, s - c]
        return mcq(q, num(g), [num(x) for x in w] + [num(g + 10)], e)

    def islem_sec():
        a, b = ri(12, 30), ri(3, 9)
        k = ri(0, 3)
        Q = [("Bir kutuda %d yumurta var. %d kutuda kaç yumurta olur? Bu problem hangi işlemle çözülür?" % (a, b), "%d × %d" % (a, b)),
             ("%d yumurta %d kutuya eşit dağıtılırsa her kutuya kaç yumurta düşer? Bu problem hangi işlemle çözülür?" % (a * b, b), "%d ÷ %d" % (a * b, b)),
             ("Bir kutuda %d yumurta vardı, %d tanesi kırıldı. Kaç yumurta kaldı? Bu problem hangi işlemle çözülür?" % (a, b), "%d − %d" % (a, b)),
             ("Bir kutuda %d, diğerinde %d yumurta var. Toplam kaç yumurta var? Bu problem hangi işlemle çözülür?" % (a, b), "%d + %d" % (a, b))]
        q, g = Q[k]
        x, y = (a * b, b) if k == 1 else (a, b)
        alts = ["%d %s %d" % (x, o, y) for o in "+−×÷" if "%d %s %d" % (x, o, y) != g]
        return mcq(q, g, alts, "Anahtar sözcüklere bak: <b>%s</b>." % g)

    def tablo():
        urun = sh([("kalem", ri(8, 25)), ("defter", ri(15, 45)), ("silgi", ri(5, 15)), ("kitap", ri(60, 150))])[:3]
        adet = [ri(2, 6) for _ in urun]
        tab = "<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr><th>Ürün</th><th>Fiyatı</th></tr></thead><tbody>%s</tbody></table>" % "".join(
            "<tr><td>%s</td><td>%d TL</td></tr>" % (u, p) for u, p in urun)
        g = sum(p * n for (u, p), n in zip(urun, adet))
        what = ", ".join("%d %s" % (n, u) for (u, p), n in zip(urun, adet))
        return mcq("Tabloya göre %s almak için kaç lira ödenir?%s" % (what, tab), "%s TL" % num(g), ["%s TL" % num(g + urun[0][1]), "%s TL" % num(sum(p for u, p in urun)), "%s TL" % num(g - urun[1][1])],
                   " + ".join("%d × %d" % (n, p) for (u, p), n in zip(urun, adet)) + " = <b>%s TL</b>." % num(g))

    def yonerge():
        a = ri(2, 20)
        ops = sh([("2 ile çarp", lambda x: x * 2), ("5 ekle", lambda x: x + 5), ("3 çıkar", lambda x: x - 3), ("10 ile çarp", lambda x: x * 10)])[:3]
        v = a
        for _, f in ops:
            v = f(v)
        if v <= 0:
            return None
        txt = " → ".join(t for t, _ in ops)
        return mcq("%d sayısına sırayla şu yönergeleri uygula: %s. Sonuç kaçtır?" % (a, txt), num(v), near(v, (1, -1, 5, 10, 2)),
                   "Yönergeleri sırayla uygularız: <b>%s</b>." % num(v))

    def olustur():
        a, b = ri(3, 9), ri(12, 40)
        g = "Bir pakette %d kurabiye var. %d pakette kaç kurabiye vardır?" % (b, a)
        return mcq("Sonucu %d × %d işlemiyle bulunan problem hangisidir?" % (a, b), g,
                   ["%d kurabiye %d kişiye paylaştırılırsa her birine kaç kurabiye düşer?" % (b, a), "%d kurabiyeden %d tanesi yendi. Kaç kurabiye kaldı?" % (b, a),
                    "Bir tabakta %d, diğerinde %d kurabiye var. Toplam kaç kurabiye var?" % (b, a)], "Eşit grupların toplamı çarpmayla bulunur: <b>%s</b>" % g)

    sets = [("İki aşamalı problemler", [(iki_adim, 20)]),
            ("İşlem seçme", [(islem_sec, 20)]),
            ("Tablo ile problemler", [(tablo, 20)]),
            ("Yönerge ile işlem", [(yonerge, 20)]),
            ("Problem kurma", [(olustur, 10), (iki_adim, 10)])]
    return unit("dort-islem-problemleri", "I", "MAT.4.2.6, MAT.4.2.7, MAT.4.2.8", 17, "Dört İşlem Gerektiren Problemler", "Dört İşlem Problemleri",
                "Dört işleme yönelik yönergeler oluşturur; dört işlem gerektiren problemleri çözer ve dört işlem gerektiren problem durumlarını yapılandırır.",
                "4. sınıf dört işlem problemleri çalışma kâğıdı: iki aşamalı problemler, işlem seçme, tablo ile alışveriş problemleri, yönergeye göre işlem ve problem kurma. 100 soru ve cevap anahtarı.",
                "Verilenleri ve isteneni ayır", "Problemi adım adım çöz, sonucu tahminle kontrol et.", sets,
                ["Önce problemi oku: Ne verilmiş? Ne isteniyor? Sonra hangi işlemlerin gerektiğine karar ver.",
                 "İki aşamalı problemlerde önce ara sonucu bul (ör. defterlerin fiyatı), sonra onu kullanarak asıl soruyu çöz.",
                 "Sonucu tahminle kontrol et: Bulduğun sayı mantıklı mı?"],
                [("Tanesi 15 TL olan 4 defter ve 60 TL’lik bir çanta", ["4 × 15 = 60", "60 + 60 = 120"], "120 TL"),
                 ("250 TL ile tanesi 35 TL olan 6 oyuncak alındı. Kalan para", ["6 × 35 = 210", "250 − 210 = 40"], "40 TL")],
                [["Ara sonucu bulup durmak", "Soru ne istiyorsa onu bul: kalan parayı soruyorsa çıkarmayı yap"], ["İşlem sırasını karıştırmak", "Önce gerekli ara bilgiyi bul"],
                 ["Birimi yazmamak", "Cevabı TL, kalem, sayfa gibi birimiyle yaz"]],
                [("Problem çözerken hangi adımları izlerim?", "Anla, plan yap, çöz, kontrol et. Verilenleri ve isteneni ayırmak ilk adımdır."),
                 ("Bir problemi farklı yollarla çözebilir miyim?", "Evet. Örneğin önce toplayıp sonra bölebilir ya da ayrı ayrı bölüp toplayabilirsin."),
                 ("Problem kurmak neden önemlidir?", "Bir işlemin günlük hayatta ne anlama geldiğini anlamamızı sağlar.")])


# ============================================================ 18. eşitlik
def u18():
    def bos():
        k = ri(0, 3)
        if k == 0:
            a, b, c = ri(20, 90), ri(20, 90), ri(10, 50)
            if a + b - c <= 0:
                return None
            return mcq("%d + %d = %d + ? eşitliğinde ? yerine hangi sayı gelir?" % (a, b, c), str(a + b - c), [str(a + b), str(a + b + c), str(c)],
                       "Sol taraf %d. %d − %d = <b>%d</b>." % (a + b, a + b, c, a + b - c))
        if k == 1:
            a, b = ri(2, 9), ri(2, 9)
            c = ch([x for x in (2, 3, 4, 6, 8, 12) if (a * b) % x == 0 and x not in (a, b)] or [1])
            if c == 1:
                return None
            return mcq("%d × %d = %d × ? eşitliğinde ? yerine hangi sayı gelir?" % (a, b, c), str(a * b // c), [str(a * b), str(a + b - c), str(a * b - c)],
                       "Sol taraf %d. %d ÷ %d = <b>%d</b>." % (a * b, a * b, c, a * b // c))
        if k == 2:
            a, b = ri(40, 99), ri(10, 39)
            c = ri(5, b - 1)
            return mcq("%d − %d = ? − %d eşitliğinde ? yerine hangi sayı gelir?" % (a, b, c), str(a - b + c), [str(a - b), str(a - b - c), str(a + c)],
                       "Sol taraf %d. ? − %d = %d ise ? = <b>%d</b>." % (a - b, c, a - b, a - b + c))
        a, b = ri(2, 9), ri(3, 9)
        p = a * b * ch([2, 3])
        return mcq("%d ÷ %d = ? × %d eşitliğinde ? yerine hangi sayı gelir?" % (p, a, b), str(p // a // b), [str(p // a), str(p // b), str(p // a - b)],
                   "Sol taraf %d. %d ÷ %d = <b>%d</b>." % (p // a, p // a, b, p // a // b))

    def dogru_mu():
        a, b = ri(2, 9), ri(10, 50)
        k = ri(0, 3)
        S = [("%d × %d = %d × %d" % (a, b, b, a), True), ("%d + %d = %d + %d" % (b, a, a, b), True),
             ("%d − %d = %d − %d" % (b, a, a, b), False), ("%d ÷ %d = %d ÷ %d" % (a * b, a, a, a * b), False)]
        x, ok = S[k]
        g = "=" if ok else "≠"
        return mcq("%s ifadesinde iki taraf arasına hangi sembol gelir? (□ yerine)" % x.replace(" = ", " □ "), g, ["≠" if ok else "=", "&lt;", "+"],
                   ("Toplama ve çarpmada sayıların yeri değişince sonuç değişmez: <b>=</b>." if ok else "Çıkarma ve bölmede sayıların yeri değişince sonuç değişir: <b>≠</b>."))

    def esit_degil():
        a, b, c = ri(10, 60), ri(10, 60), ri(2, 9)
        L = a + b
        k = ri(0, 1)
        if k == 0:
            R_ = L
            right = "%d + %d" % (L - c, c)
        else:
            R_ = L + ch([1, -1, 10])
            right = "%d + %d" % (R_ - c, c)
        g = "=" if R_ == L else "≠"
        return mcq("%d + %d □ %s ifadesinde □ yerine hangi sembol gelir?" % (a, b, right), g, ["≠" if g == "=" else "=", "×", "÷"],
                   "Sol taraf %d, sağ taraf %d: <b>%s</b>." % (L, R_, g))

    def terazi_q():
        a, b = ri(3, 9), ri(3, 9)
        c = ri(2, 6)
        if (a * b) % c:
            return None
        return mcq("Terazi dengede. Sağ kefedeki kutuda kaç olmalıdır?" + terazi("%d × %d" % (a, b), "%d × ?" % c), str(a * b // c), [str(a * b), str(a * b - c), str(a + b)],
                   "Sol kefe %d. %d × ? = %d → ? = <b>%d</b>." % (a * b, c, a * b, a * b // c))

    def hayat():
        n1, n2 = G.K.two()
        a, b = ri(3, 8), ri(10, 25)
        c = ch([x for x in (2, 3, 4, 5, 6) if (a * b) % x == 0] or [1])
        if c in (1, a):
            return None
        g = a * b // c
        return mcq("%s tanesi %d TL olan %d kalem aldı. %s ise tanesi %d TL olan defterlerden aldı ve aynı parayı ödedi. %s kaç defter aldı?" % (n1, b, a, n2, g, n2),
                   str(c), [str(a), str(g), str(c + 1)], "%d × %d = %d. %d × ? = %d → ? = <b>%d</b>." % (a, b, a * b, g, a * b, c))

    sets = [("Eşitliği sağlayan sayı", [(bos, 20)]),
            ("= mi, ≠ mi?", [(dogru_mu, 10), (esit_degil, 10)]),
            ("Terazi modeli", [(terazi_q, 20)]),
            ("Eşitlik ve işlemler", [(bos, 10), (esit_degil, 10)]),
            ("Günlük hayatta eşitlik", [(hayat, 14), (terazi_q, 6)])]
    return unit("esitlik-ve-esit-degildir", "I", "MAT.4.2.9", 18, "Dört İşlemde Eşitlik ve Eşit Değildir", "Eşitlik",
                "Dört işlem bağlamında eşitliğin farklı anlamlarını yorumlar; eşitlik ve eşit değildir (≠) sembollerini kullanır.",
                "4. sınıf eşitlik çalışma kâğıdı: dört işlemde eşitliği sağlayan sayı, eşittir ve eşit değildir sembolleri, terazi modeli ve günlük hayatta eşitlik. 100 soru ve cevap anahtarı.",
                "= iki tarafın değeri aynı demektir", "İki taraf farklıysa ≠ (eşit değildir) kullanılır.", sets,
                ["Eşittir (=) sembolü “sonuç” demek değildir; iki tarafın aynı değerde olduğunu gösterir: 6 × 4 = 3 × 8.",
                 "Eşitlikte boşluğu bulmak için önce bilinen tarafı hesaplarız, sonra diğer tarafı ona eşitleriz.",
                 "İki taraf farklıysa eşit değildir (≠) sembolünü kullanırız: 12 − 5 ≠ 5 − 12."],
                [("6 × 4 = 3 × ?", ["Sol taraf 24", "3 × 8 = 24"], "8"), ("45 + 18 □ 50 + 13", ["63 ve 63"], "=")],
                [["6 × 4 = 3 × ? için 24 yazmak", "? sağ tarafı 24 yapan sayıdır: 8"], ["Çıkarmada sayıların yerini değiştirmek", "12 − 5 ≠ 5 − 12"],
                 ["= sembolünden sonra hep cevap gelir sanmak", "= iki tarafın dengede olduğunu söyler"]],
                [("≠ sembolü ne anlama gelir?", "“Eşit değildir” demektir. İki tarafın değeri farklıdır."),
                 ("Terazi eşitliği nasıl gösterir?", "İki kefe aynı ağırlıktaysa terazi dengede kalır; bu, iki tarafın eşit olduğunu gösterir."),
                 ("Hangi işlemlerde sayıların yeri değişebilir?", "Toplama ve çarpmada yer değiştirmek sonucu değiştirmez; çıkarma ve bölmede değiştirir.")])


UNITS = [u12, u13, u14, u15, u16, u17, u18]
