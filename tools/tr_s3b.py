# -*- coding: utf-8 -*-
"""Türkiye 3. sınıf: İşlemlerden Cebirsel Düşünmeye, Nesnelerin Geometrisi, Veriye Dayalı Araştırma — 11〜22 単元。"""
import math
import tr_s3a as A
from tr_s3a import unit, cap, mi, named, dagit
from tr_common import (num, tl, oku, mcq, M, NB, Kids, wrap, text, line, alt_alta, cetele, sutun_grafigi, INK, GREEN, FILL, RED, BLUE)

R = None
K = None


def setup(rnd):
    global R, K
    R = rnd
    K = Kids(rnd)


def ri(a, b):
    return R.randint(a, b)


def ch(xs):
    return R.choice(list(xs))


def sh(xs):
    xs = list(xs)
    R.shuffle(xs)
    return xs


def near(v, ds=(10, -10, 1, -1, 100, -100)):
    return [num(v + d) for d in ds if v + d >= 0]


# ============================================================ 11. toplama
def u11():
    def eldesiz():
        a, b = ri(100, 699), ri(100, 299)
        if any(int(x) + int(y) > 9 for x, y in zip(str(a), str(b))):
            return None
        return mcq("%s + %s = ?" % (num(a), num(b)), num(a + b), near(a + b), "Birler, onlar ve yüzler ayrı ayrı toplanır: <b>%s</b>." % num(a + b))

    def eldeli():
        a, b = ri(105, 799), ri(15, 499)
        s = a + b
        if s >= 1000 or (a % 10 + b % 10 < 10 and a // 10 % 10 + b // 10 % 10 < 10):
            return None
        noc = int("".join(str((int(x) + int(y)) % 10) for x, y in zip(str(a).rjust(3, "0"), str(b).rjust(3, "0"))))
        return mcq("Alt alta toplama yap." + alt_alta([str(a), str(b)], "+"), num(s), [num(noc), num(s + 10), num(s - 10), num(s + 100)],
                   "Birlerden başla; 10 ve fazlası olunca eldeyi bir sonraki basamağa ekle: <b>%s</b>." % num(s))

    def zihinden():
        k = ri(0, 2)
        if k == 0:
            a, b = ri(1, 8) * 100 + ri(0, 9) * 10, ri(1, 9) * 10
            if a + b >= 1000:
                return None
            return mcq("Zihinden topla: %s + %s" % (num(a), num(b)), num(a + b), near(a + b, (10, -10, 100, 1)),
                       "Onluklar toplanır: <b>%s</b>." % num(a + b))
        if k == 1:
            a = ri(101, 899)
            b = ch([99, 199, 98, 101, 201, 9, 19])
            if a + b >= 1000:
                return None
            r = (b + 1) if b % 10 == 9 else (b + 2) if b % 10 == 8 else b
            return mcq("Zihinden topla: %s + %s" % (num(a), num(b)), num(a + b), near(a + b, (1, -1, 10, 100)),
                       "%d yerine %d ekle, sonra fazlasını çıkar: <b>%s</b>." % (b, r, num(a + b)) if r != b else "Yüzlükleri ekle, sonra birliği ekle: <b>%s</b>." % num(a + b))
        a, b, c = ri(10, 99), ri(10, 99), ri(10, 99)
        return mcq("%d + %d + %d = ?" % (a, b, c), num(a + b + c), near(a + b + c), "Önce kolay olan ikisini topla, sonra üçüncüsünü ekle: <b>%s</b>." % num(a + b + c))

    def tahmin():
        a, b = ri(110, 690), ri(110, 290)
        ra, rb = int(math.floor(a / 100.0 + 0.5)) * 100, int(math.floor(b / 100.0 + 0.5)) * 100
        if ra + rb >= 1000 or a % 100 in (50,) or b % 100 == 50:
            return None
        return mcq("%s + %s toplamını en yakın yüzlüklere yuvarlayarak tahmin et." % (num(a), num(b)), num(ra + rb),
                   [num(ra + rb + 100), num(ra + rb - 100), num(a + b)], "%s ≈ %s, %s ≈ %s. Tahmin: <b>%s</b>." % (num(a), num(ra), num(b), num(rb), num(ra + rb)))

    def eksik():
        a, b = ri(100, 599), ri(10, 399)
        s = a + b
        if s >= 1000:
            return None
        if R.random() < 0.5:
            return mcq("%s + … = %s. Noktalı yere hangi sayı gelir?" % (num(a), num(s)), num(b), [num(s + a), num(b + 10), num(b - 1)],
                       "Eksik toplananı bulmak için toplamdan bilinen toplananı çıkar: %s − %s = <b>%s</b>." % (num(s), num(a), num(b)))
        return mcq("… + %s = %s. Noktalı yere hangi sayı gelir?" % (num(b), num(s)), num(a), [num(s + b), num(a + 10), num(a - 10)],
                   "%s − %s = <b>%s</b>." % (num(s), num(b), num(a)))

    def problem():
        name = K.next()
        P = [("Okul kütüphanesinde %d hikâye kitabı ve %d bilim kitabı var. Kütüphanede toplam kaç kitap var?", "kitap"),
             ("%s ilk gün %d, ikinci gün %d sayfa kitap okudu. Toplam kaç sayfa okudu?", "sayfa"),
             ("Bir fırında sabah %d, öğlen %d simit satıldı. Toplam kaç simit satıldı?", "simit"),
             ("Bir otobüs ilk seferde %d, ikinci seferde %d yolcu taşıdı. Toplam kaç yolcu taşıdı?", "yolcu"),
             ("Bir bahçede %d lale ve %d gül var. Bahçede toplam kaç çiçek var?", "çiçek"),
             ("%s kumbarasına geçen ay %d TL, bu ay %d TL attı. Toplam kaç lira biriktirdi?", "TL")]
        t, u = ch(P)
        a, b = ri(120, 560), ri(110, 430)
        if a + b >= 1000:
            return None
        q = t % ((name, a, b) if t.startswith("%s") else (a, b))
        return mcq(q, "%s %s" % (num(a + b), u), ["%s %s" % (x, u) for x in near(a + b, (10, -10, 100))] + ["%s %s" % (num(abs(a - b)), u)],
                   "%s + %s = <b>%s</b>." % (num(a), num(b), num(a + b)))

    sets = [("Eldesiz toplama", [(eldesiz, 20)]),
            ("Eldeli toplama", [(eldeli, 20)]),
            ("Zihinden toplama", [(zihinden, 20)]),
            ("Tahmin ve eksik toplanan", [(tahmin, 10), (eksik, 10)]),
            ("Problemler", [(problem, 20)])]
    return unit("toplama-islemi", "I", "MAT.3.2.1, MAT.3.2.2", 11, "Toplama İşlemi: Eldeli Toplama, Zihinden Toplama ve Tahmin", "Toplama İşlemi",
                "Toplama işleminin sonuçlarını tahminde bulunarak ve zihinden işlem yaparak muhakeme eder; toplama işlemini adımlarına göre çözümler (toplamları 1000'den küçük).",
                "3. sınıf toplama işlemi çalışma kâğıdı: eldesiz ve eldeli toplama, alt alta toplama, zihinden toplama, toplamı tahmin etme, eksik toplanan ve problemler. 100 soru ve cevap anahtarı.",
                "Birlerden başla, eldeyi unutma", "Tahmin için sayıları en yakın yüzlüğe yuvarla.", sets,
                ["Alt alta toplarken basamaklar hizalanır ve birlerden başlanır. Toplam 10 veya fazlaysa 1 onluk elde olarak bir sonraki basamağa eklenir.",
                 "Zihinden toplarken sayıyı parçalara ayır: 456 + 30 = 486, 345 + 99 = 345 + 100 − 1.",
                 "Sonucu kontrol etmek için tahmin yap: 398 + 205 yaklaşık 400 + 200 = 600."],
                [("367 + 248", ["7 + 8 = 15 → 5, elde 1", "6 + 4 + 1 = 11 → 1, elde 1", "3 + 2 + 1 = 6"], "615"), ("… + 230 = 580", ["580 − 230"], "350")],
                [["Eldeyi eklemeyi unutmak", "Elde, bir sonraki basamağa eklenir"], ["Basamakları kaydırarak yazmak", "Birler birlerin, onlar onların altına"],
                 ["Tahmini cevap sanmak", "Tahmin yaklaşık sonuçtur; işlemi yine yap"]],
                [("Elde nedir?", "Bir basamakta toplam 10 veya fazla olunca 10 birlik 1 onluk olur ve bir sonraki basamağa eklenir. Buna elde denir."),
                 ("Toplama işleminin ögeleri nelerdir?", "Toplanan, toplanan ve toplam. 245 + 130 = 375 işleminde 375 toplamdır."),
                 ("Toplananların yeri değişirse toplam değişir mi?", "Hayır. 245 + 130 ile 130 + 245 aynı sonucu verir.")])


# ============================================================ 12. çıkarma
def u12():
    def onluk_bozmadan():
        a = ri(300, 999)
        b = int("".join(str(ri(0, int(d))) for d in str(a)))
        if b < 100 or b == a:
            return None
        return mcq("%s − %s = ?" % (num(a), num(b)), num(a - b), near(a - b), "Her basamak ayrı ayrı çıkarılır: <b>%s</b>." % num(a - b))

    def bozarak():
        a, b = ri(300, 999), ri(105, 299)
        d = a - b
        if d <= 0 or (a % 10 >= b % 10 and a // 10 % 10 >= b // 10 % 10):
            return None
        wrong = int("".join(str(abs(int(x) - int(y))) for x, y in zip(str(a), str(b).rjust(3, "0"))))
        return mcq("Alt alta çıkarma yap." + alt_alta([str(a), str(b)], "−"), num(d), [num(wrong), num(d + 10), num(d - 10), num(d + 100)],
                   "Üstteki rakam küçükse bir üst basamaktan 1 onluk (ya da yüzlük) bozulur: <b>%s</b>." % num(d))

    def zihinden():
        k = ri(0, 2)
        if k == 0:
            a, b = ri(2, 9) * 100 + ri(0, 9) * 10 + ri(0, 9), ri(1, 9) * 10
            if b > a:
                return None
            return mcq("Zihinden çıkar: %s − %s" % (num(a), num(b)), num(a - b), near(a - b, (10, -10, 100, 1)), "Onluklardan çıkar: <b>%s</b>." % num(a - b))
        if k == 1:
            a = ri(150, 999)
            b = ch([99, 98, 199, 9, 19, 29])
            return mcq("Zihinden çıkar: %s − %s" % (num(a), num(b)), num(a - b), near(a - b, (1, -1, 2, 10)),
                       "%d yerine bir fazlasını çıkar, sonra fazla çıkardığını geri ekle: <b>%s</b>." % (b, num(a - b)))
        a = ri(1, 9) * 100
        b = ri(1, a // 10 - 1) * 10
        return mcq("Zihinden çıkar: %s − %s" % (num(a), num(b)), num(a - b), near(a - b, (10, -10, 100)), "<b>%s</b>." % num(a - b))

    def tahmin():
        a, b = ri(410, 990), ri(110, 390)
        ra, rb = int(math.floor(a / 100.0 + 0.5)) * 100, int(math.floor(b / 100.0 + 0.5)) * 100
        if a % 100 == 50 or b % 100 == 50 or ra <= rb:
            return None
        return mcq("%s − %s farkını en yakın yüzlüklere yuvarlayarak tahmin et." % (num(a), num(b)), num(ra - rb),
                   [num(ra - rb + 100), num(ra - rb - 100) if ra - rb > 100 else num(ra + rb), num(a - b)],
                   "%s ≈ %s, %s ≈ %s. Tahmin: <b>%s</b>." % (num(a), num(ra), num(b), num(rb), num(ra - rb)))

    def eksik():
        a, b = ri(200, 999), ri(10, 199)
        d = a - b
        k = ri(0, 1)
        if k == 0:
            return mcq("%s − … = %s. Noktalı yere hangi sayı gelir?" % (num(a), num(d)), num(b), [num(a + d), num(b + 10), num(b - 1)],
                       "Çıkanı bulmak için eksilenden farkı çıkar: %s − %s = <b>%s</b>." % (num(a), num(d), num(b)))
        if a >= 1000:
            return None
        return mcq("… − %s = %s. Noktalı yere hangi sayı gelir?" % (num(b), num(d)), num(a), [num(d - b) if d > b else num(a + 100), num(a + 10), num(a - 10)],
                   "Eksileni bulmak için fark ile çıkanı topla: %s + %s = <b>%s</b>." % (num(d), num(b), num(a)))

    def problem():
        name = K.next()
        P = [("%s, %d sayfalık bir kitabın %d sayfasını okudu. Okuması gereken kaç sayfa kaldı?", "sayfa"),
             ("Bir manavda %d kg elma vardı. Gün içinde %d kg elma satıldı. Kaç kg elma kaldı?", "kg"),
             ("Bir okulda %d öğrenci var. Öğrencilerden %d tanesi kız. Okulda kaç erkek öğrenci var?", "öğrenci"),
             ("%s, %d TL biriktirdi. Bir bisiklet için %d TL harcadı. Kaç lirası kaldı?", "TL"),
             ("Bir tiyatro salonunda %d koltuk var. Gösteriye %d kişi geldi. Kaç koltuk boş kaldı?", "koltuk")]
        t, u = ch(P)
        a, b = ri(250, 980), ri(110, 240)
        q = t % ((name, a, b) if t.startswith("%s") else (a, b))
        return mcq(q, "%s %s" % (num(a - b), u), ["%s %s" % (x, u) for x in near(a - b, (10, -10, 100))] + ["%s %s" % (num(a + b), u)],
                   "%s − %s = <b>%s</b>." % (num(a), num(b), num(a - b)))

    sets = [("Onluk bozmadan çıkarma", [(onluk_bozmadan, 20)]),
            ("Onluk ve yüzlük bozarak çıkarma", [(bozarak, 20)]),
            ("Zihinden çıkarma", [(zihinden, 20)]),
            ("Tahmin ve eksik terim", [(tahmin, 10), (eksik, 10)]),
            ("Problemler", [(problem, 20)])]
    return unit("cikarma-islemi", "I", "MAT.3.2.1, MAT.3.2.2", 12, "Çıkarma İşlemi: Bozarak Çıkarma, Zihinden Çıkarma ve Tahmin", "Çıkarma İşlemi",
                "Çıkarma işleminin sonuçlarını tahminde bulunarak ve zihinden işlem yaparak muhakeme eder; çıkarma işlemini adımlarına göre çözümler (1000'e kadar).",
                "3. sınıf çıkarma işlemi çalışma kâğıdı: onluk bozmadan ve bozarak çıkarma, alt alta çıkarma, zihinden çıkarma, farkı tahmin etme, eksik terim ve problemler. 100 soru ve cevap anahtarı.",
                "Üstteki küçükse bir üst basamaktan boz", "Kontrol: fark + çıkan = eksilen.", sets,
                ["Alt alta çıkarırken birlerden başlanır. Üstteki rakam alttakinden küçükse bir üst basamaktan 1 onluk bozulur (10 birlik olur).",
                 "Çıkarmanın sağlaması toplamayla yapılır: fark ile çıkanın toplamı eksileni verir.",
                 "Zihinden çıkarırken kolay sayılar kullan: 532 − 99 = 532 − 100 + 1."],
                [("524 − 176", ["4 − 6 olmaz: 1 onluk boz, 14 − 6 = 8", "1 − 7 olmaz: 1 yüzlük boz, 11 − 7 = 4", "4 − 1 = 3"], "348"),
                 ("Sağlama: 348 + 176", ["= 524"], "doğru")],
                [["Büyükten küçüğü çıkarmak (6 − 4)", "Üstteki küçükse onluk boz: 14 − 6"], ["Bozduğun basamağı 1 azaltmayı unutmak", "Bozulan basamaktan 1 eksilir"],
                 ["Sıfırdan bozmayı atlamak (500 − 123)", "Önce yüzlükten onluk, sonra onluktan birlik boz"]],
                [("Çıkarma işleminin ögeleri nelerdir?", "Eksilen, çıkan ve fark. 524 − 176 = 348 işleminde 348 farktır."),
                 ("Onluk bozmak ne demektir?", "1 onluğu 10 birliğe çevirmektir. Bu sayede küçük rakamdan büyük rakam çıkarılabilir."),
                 ("Çıkarma işlemini nasıl kontrol ederim?", "Farkı çıkanla topla. Sonuç eksileni veriyorsa işlem doğrudur.")])


# ============================================================ 13. çarpma
def dizi(r, c, col="#e07a5f"):
    s = []
    for i in range(r):
        for j in range(c):
            s.append("<circle cx='%d' cy='%d' r='8' fill='%s' stroke='%s' stroke-width='1.2'/>" % (16 + j * 22, 16 + i * 22, col, INK))
    return wrap(c * 22 + 10, r * 22 + 10, "".join(s), "%d sıra, her sırada %d nesne" % (r, c))


def u13():
    def tablo():
        a, b = ri(2, 10), ri(2, 9)
        p = a * b
        return mcq("%d × %d = ?" % (a, b), str(p), [str(p + a), str(p - b), str(a + b), str(p + 1), str(p - a)],
                   "%s %d kez sayılır: <b>%d</b>." % (cap(dagit(a)), b, p) if a <= 10 else "<b>%d</b>." % p)

    def model():
        r, c = ri(2, 6), ri(2, 9)
        k = ri(0, 1)
        if k == 0:
            return mcq("Dizideki nesne sayısını veren çarpma işlemi hangisidir?" + dizi(r, c), "%d × %d = %d" % (r, c, r * c),
                       ["%d + %d = %d" % (r, c, r + c), "%d × %d = %d" % (r, c, r * c + c), "%d × %d = %d" % (r + 1, c, (r + 1) * c)],
                       "%d sıra, her sırada %d nesne: %d × %d = <b>%d</b>." % (r, c, r, c, r * c))
        return mcq("%s işleminin çarpma ile gösterimi hangisidir?" % " + ".join([str(c)] * r), "%d × %d" % (r, c),
                   ["%d + %d" % (r, c), "%d × %d" % (c, c), "%d × %d" % (r + 1, c)] if r != c else ["%d + %d" % (r, c), "%d × %d" % (r + 1, c), "%d × %d" % (r, c + 1)],
                   "%d tane %d toplanıyor: <b>%d × %d = %d</b>." % (r, c, r, c, r * c))

    def onluk():
        k = ri(0, 1)
        a = ri(2, 99) if k == 0 else ri(2, 9)
        m = 10 if k == 0 else 100
        return mcq("%d × %d = ?" % (a, m), num(a * m), [num(a * m * 10) if a * m * 10 < 10000 else num(a + m), num(a + m), num(a * m // 10) if a * m // 10 != a else num(a * m + 10)],
                   "%d ile çarparken sayının sağına %s sıfır yazılır: <b>%s</b>." % (m, "bir" if m == 10 else "iki", num(a * m)))

    def iki_bir():
        a, b = ri(11, 49), ri(2, 9)
        p = a * b
        if p >= 1000:
            return None
        t, o = divmod(a, 10)
        noc = t * b * 10 + (o * b) % 10
        return mcq("%d × %d = ?" % (a, b), num(p), [num(noc) if noc != p else num(p + 10), num(t * 10 * b + o), num(p + b), num(p - 10)],
                   "%d = %d + %d. %d × %d = %d, %d × %d = %d. %d + %d = <b>%s</b>." % (a, t * 10, o, t * 10, b, t * 10 * b, o, b, o * b, t * 10 * b, o * b, num(p)))

    def ozellik():
        a, b = ri(2, 9), ri(2, 9)
        k = ri(0, 2)
        if k == 0 and a != b:
            return mcq("%d × %d = %d × … Noktalı yere hangi sayı gelir?" % (a, b, b), str(a), [str(b), str(a * b), str(a + b)],
                       "Çarpanların yeri değişince çarpım değişmez: <b>%d</b>." % a)
        if k == 1:
            return mcq("%d × 1 = ?" % (a * 10 + b), str(a * 10 + b), ["1", str(a * 10 + b + 1), "0"], "Bir sayının 1 ile çarpımı kendisidir: <b>%d</b>." % (a * 10 + b))
        return mcq("%d × 0 = ?" % (a * 10 + b), "0", [str(a * 10 + b), "1", str(a * 10 + b - 1)], "Bir sayının 0 ile çarpımı <b>0</b>'dır.")

    def problem():
        name = K.next()
        P = [("Bir kutuda %d kalem var. %d kutuda kaç kalem vardır?", "kalem"), ("Bir sırada %d öğrenci oturuyor. %d sırada kaç öğrenci vardır?", "öğrenci"),
             ("%s her gün %d sayfa kitap okuyor. %d günde kaç sayfa okur?", "sayfa"), ("Bir minibüste %d yolcu var. %d minibüste kaç yolcu vardır?", "yolcu"),
             ("Bir kolide %d portakal var. %d kolide kaç portakal vardır?", "portakal"), ("Bir paket çikolatanın fiyatı %d TL. %d paket kaç lira eder?", "TL")]
        t, u = ch(P)
        a, b = ri(11, 45), ri(3, 9)
        if a * b >= 1000:
            return None
        q = t % ((name, a, b) if t.startswith("%s") else (a, b))
        return mcq(q, "%s %s" % (num(a * b), u), ["%s %s" % (num(x), u) for x in (a + b, a * b + a, a * b - b, a * (b - 1))],
                   "%d × %d = <b>%s</b>." % (a, b, num(a * b)))

    sets = [("Çarpım tablosu", [(tablo, 20)]),
            ("Çarpmanın anlamı ve modeller", [(model, 14), (ozellik, 6)]),
            ("10 ve 100 ile çarpma", [(onluk, 20)]),
            ("İki basamaklı sayıyı bir basamaklı sayıyla çarpma", [(iki_bir, 20)]),
            ("Problemler", [(problem, 20)])]
    return unit("carpma-islemi", "I", "MAT.3.2.3, MAT.3.2.4", 13, "Çarpma İşlemi: Çarpım Tablosu ve İki Basamaklı Sayılarla Çarpma", "Çarpma İşlemi",
                "Çarpma işleminin sonuçlarını muhakeme eder; çarpma işlemini adımlarına göre çözümler: 10'a kadar sayılarla çarpım tablosu, iki basamaklı sayıyı bir basamaklı sayıyla çarpma, 10 ve 100 ile kısa yoldan çarpma.",
                "3. sınıf çarpma işlemi çalışma kâğıdı: çarpım tablosu, tekrarlı toplama ve dizi modeli, 10 ve 100 ile kısa yoldan çarpma, iki basamaklı sayıyı bir basamaklı sayıyla çarpma ve problemler. 100 soru ve cevap anahtarı.",
                "Çarpma tekrarlı toplamadır", "10 ile çarparken sağa bir sıfır, 100 ile iki sıfır yaz.", sets,
                ["Çarpma, aynı sayının tekrar tekrar toplanmasıdır: 4 + 4 + 4 = 3 × 4 = 12.",
                 "Çarpanların yeri değişince çarpım değişmez: 3 × 7 = 7 × 3. Bir sayının 1 ile çarpımı kendisi, 0 ile çarpımı 0'dır.",
                 "İki basamaklı sayıyı çarparken onlukları ve birlikleri ayrı ayrı çarpıp topla: 23 × 4 = 80 + 12 = 92."],
                [("6 × 7", ["altışar yedi kez: 6, 12, …, 42"], "42"), ("34 × 3", ["30 × 3 = 90", "4 × 3 = 12", "90 + 12"], "102")],
                [["Çarpma yerine toplama yapmak (3 × 4 = 7)", "3 × 4, üç tane dört demektir: 12"], ["İki basamaklı çarpmada eldeyi unutmak", "Birlerden gelen onluğu onlara ekle"],
                 ["25 × 10 = 2500 yazmak", "10 ile çarparken bir sıfır eklenir: 250"]],
                [("Çarpma işleminin ögeleri nelerdir?", "Çarpan, çarpan ve çarpım. 6 × 7 = 42 işleminde 42 çarpımdır."),
                 ("Çarpım tablosunu nasıl ezberlerim?", "Ritmik saymayla başla ve çarpanların yerini değiştirmenin çarpımı değiştirmediğini kullan; böylece ezberleyeceğin sayı yarıya iner."),
                 ("Neden 10 ile çarparken sıfır ekleriz?", "Her birlik onluk olur; rakamlar bir basamak sola kayar ve birler basamağına 0 gelir.")])


# ============================================================ 14. bölme
def gruplar(g, k, col="#f2c94c"):
    s, x = [], 6
    per = min(k, 5)
    rws = (k + per - 1) // per
    w, h = per * 18 + 14, rws * 18 + 14
    for i in range(g):
        s.append("<rect x='%d' y='6' width='%d' height='%d' rx='12' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x, w, h, FILL, GREEN))
        for t in range(k):
            s.append("<circle cx='%d' cy='%d' r='6.5' fill='%s' stroke='%s'/>" % (x + 14 + (t % per) * 18, 20 + (t // per) * 18, col, INK))
        x += w + 10
    return wrap(x, h + 12, "".join(s), "%d grup, her grupta %d nesne" % (g, k))


def u14():
    def tablo():
        b, q = ri(2, 9), ri(2, 10)
        a = b * q
        return mcq("%d ÷ %d = ?" % (a, b), str(q), [str(q + 1), str(q - 1), str(a - b), str(b)] if b != q else [str(q + 1), str(q - 1), str(a - b), str(a)],
                   "%d × %d = %d olduğu için %d ÷ %d = <b>%d</b>." % (b, q, a, a, b, q))

    def model():
        g, k = ri(2, 6), ri(2, 7)
        n = g * k
        return mcq("%d nesne %d gruba eşit olarak paylaştırıldı. Her grupta kaç nesne vardır?" % (n, g) + gruplar(g, k), str(k),
                   [str(g), str(n - g), str(k + 1)] if g != k else [str(n - g), str(k + 1), str(k - 1)], "%d ÷ %d = <b>%d</b>." % (n, g, k))

    def kalanli():
        b = ri(2, 9)
        a = ri(b + 1, 99)
        q, r = divmod(a, b)
        if r == 0:
            return None
        g = "bölüm %d, kalan %d" % (q, r)
        return mcq("%d ÷ %d işleminde bölüm ve kalan kaçtır?" % (a, b), cap(g),
                   [cap("bölüm %d, kalan %d" % (q - 1, r + b)), cap("bölüm %d, kalan %d" % (q + 1, r)), cap("bölüm %d, kalan %d" % (q, r + 1)) if r + 1 < b else cap("bölüm %d, kalan %d" % (r, q))],
                   "%d × %d = %d, %d − %d = %d. Kalan bölenden küçüktür: <b>%s</b>." % (b, q, b * q, a, b * q, r, g))

    def ogeler():
        b = ri(2, 9)
        q = ri(2, 11)
        r = ri(0, b - 1)
        a = b * q + r
        if a > 99:
            return None
        k = ri(0, 2)
        if k == 0:
            return mcq("%d ÷ %d işleminde bölünen hangisidir?" % (a, b), str(a), [str(b), str(q), str(r) if r not in (a, b, q) else str(a + 1)],
                       "Bölünen, bölünmek istenen sayıdır: <b>%d</b>." % a)
        if k == 1:
            return mcq("Bir bölme işleminde bölen %d, bölüm %d, kalan %d. Bölünen kaçtır?" % (b, q, r), str(a), [str(b * q), str(b * q - r) if r else str(a + b), str(b + q + r)],
                       "Bölünen = bölen × bölüm + kalan = %d × %d + %d = <b>%d</b>." % (b, q, r, a))
        return mcq("%d ÷ %d işleminde kalan en çok kaç olabilir?" % (ri(30, 99), b), str(b - 1), [str(b), str(b + 1), "0" if b - 1 != 0 else "2"],
                   "Kalan bölenden küçük olmalıdır. Bölen %d ise kalan en çok <b>%d</b>." % (b, b - 1))

    def onla():
        a = ri(2, 9) * 10 * ch([1, 1, 10]) if R.random() < 0.3 else ri(1, 99) * 10
        if a > 990:
            return None
        return mcq("%s ÷ 10 = ?" % num(a), num(a // 10), [num(a * 10), num(a // 100) if a >= 100 else num(a - 10), num(a // 10 + 1)],
                   "Birler basamağı 0 olan sayıyı 10'a bölerken sağdaki sıfır silinir: <b>%s</b>." % num(a // 10))

    def problem():
        name = K.next()
        P = [("%d kalem %d öğrenciye eşit olarak dağıtılıyor. Her öğrenci kaç kalem alır?", "kalem"),
             ("%d yumurta, her birine %d yumurta konan kutulara yerleştiriliyor. Kaç kutu gerekir?", "kutu"),
             ("%s, %d cevizi %d arkadaşıyla eşit olarak paylaştı. Her arkadaşı kaç ceviz aldı?", "ceviz"),
             ("Bir sınıfta %d öğrenci var. Öğrenciler %d kişilik gruplara ayrılıyor. Kaç grup oluşur?", "grup")]
        t, u = ch(P)
        b, q = ri(2, 9), ri(3, 12)
        a = b * q
        if a > 99:
            return None
        q_ = t % ((name, a, b) if t.startswith("%s") else (a, b))
        return mcq(q_, "%d %s" % (q, u), ["%d %s" % (x, u) for x in (a - b, a + b, q + 1, b) if x != q],
                   "%d ÷ %d = <b>%d</b>." % (a, b, q))

    sets = [("Çarpım tablosuyla bölme", [(tablo, 20)]),
            ("Eşit paylaştırma", [(model, 20)]),
            ("Kalanlı bölme", [(kalanli, 20)]),
            ("Bölmenin ögeleri ve 10 ile bölme", [(ogeler, 12), (onla, 8)]),
            ("Problemler", [(problem, 20)])]
    return unit("bolme-islemi", "I", "MAT.3.2.3, MAT.3.2.4", 14, "Bölme İşlemi: Kalansız ve Kalanlı Bölme", "Bölme İşlemi",
                "Bölme işleminin sonuçlarını muhakeme eder; bölme işlemini adımlarına göre çözümler: 100'e kadar sayılarla kalanlı ve kalansız bölme, 10 ile kısa yoldan bölme.",
                "3. sınıf bölme işlemi çalışma kâğıdı: çarpım tablosuyla bölme, eşit paylaştırma, kalanlı bölme, bölünen, bölen, bölüm ve kalan, 10 ile bölme ve problemler. 100 soru ve cevap anahtarı.",
                "Bölme, eşit paylaştırmadır", "Kalan her zaman bölenden küçüktür.", sets,
                ["Bölme, bir çokluğu eşit gruplara ayırmaktır. 12 ÷ 3 = 4: 12 nesne 3 gruba ayrılınca her grupta 4 nesne olur.",
                 "Bölme, çarpmanın tersidir: 4 × 3 = 12 olduğu için 12 ÷ 3 = 4.",
                 "Eşit paylaştırmada artan nesneler kalandır. Kalan bölenden küçük olmalıdır: 23 ÷ 4 → bölüm 5, kalan 3."],
                [("42 ÷ 6", ["6 × 7 = 42"], "7"), ("29 ÷ 4", ["4 × 7 = 28", "29 − 28 = 1"], "bölüm 7, kalan 1")],
                [["Kalanın bölenden büyük olması", "Kalan bölenden küçükse doğrudur"], ["Bölünen ile böleni karıştırmak", "Bölünen ÷ bölen = bölüm"],
                 ["Bölmede sağlama yapmamak", "Bölen × bölüm + kalan = bölünen"]],
                [("Bölme işleminin ögeleri nelerdir?", "Bölünen, bölen, bölüm ve kalan. 29 ÷ 4 işleminde 29 bölünen, 4 bölen, 7 bölüm, 1 kalandır."),
                 ("Kalansız bölme ne demektir?", "Hiç nesne artmayan bölmedir; kalan 0'dır."),
                 ("Bölme işlemini nasıl kontrol ederim?", "Bölen ile bölümü çarp, kalanı ekle. Bölüneni buluyorsan işlem doğrudur.")])


# ============================================================ 15. problemler
def u15():
    def iki_adim():
        name = K.next()
        k = ri(0, 5)
        if k == 0:
            a, b, c = ri(120, 400), ri(50, 300), ri(30, 200)
            if a + b - c <= 0 or a + b >= 1000:
                return None
            return mcq("%s kumbarasında %s vardı. Annesi %s verdi. %s harcadı. Kaç lirası kaldı?" % (name, tl(a), tl(b), tl(c)), tl(a + b - c),
                       [tl(a + b + c), tl(a - b - c) if a - b - c > 0 else tl(a + b - c + 10), tl(a + b - c - 10)], "%d + %d − %d = <b>%s</b>." % (a, b, c, tl(a + b - c)))
        if k == 1:
            p, n, m = ri(5, 15), ri(3, 9), ri(2, 9)
            return mcq("Bir defter %s, bir kalem %s. %s %d defter ve 1 kalem aldı. Kaç lira ödedi?" % (tl(p), tl(m), name, n), tl(p * n + m),
                       [tl(p * n), tl((p + m) * n), tl(p + n + m)], "%d × %d + %d = <b>%s</b>." % (n, p, m, tl(p * n + m)))
        if k == 2:
            g, s, e = ri(3, 8), ri(4, 9), ri(2, 9)
            t = g * s + e
            return mcq("Bir sınıfta %d sıra var, her sırada %d öğrenci oturuyor. Sınıfa %d öğrenci daha geldi. Sınıfta kaç öğrenci oldu?" % (g, s, e), str(t),
                       [str(g * s), str(g + s + e), str(g * (s + e))], "%d × %d + %d = <b>%d</b>." % (g, s, e, t))
        if k == 3:
            b, q = ri(3, 9), ri(3, 9)
            a = b * q
            x = ri(2, 9)
            return mcq("%d kurabiye %d tabağa eşit olarak konuldu. Sonra her tabağa %d kurabiye daha eklendi. Bir tabakta kaç kurabiye oldu?" % (a, b, x), str(q + x),
                       [str(q), str(a + x), str(q * x)], "%d ÷ %d = %d. %d + %d = <b>%d</b>." % (a, b, q, q, x, q + x))
        if k == 4:
            a, b = ri(200, 500), ri(100, 400)
            if a + b >= 1000:
                return None
            c = ri(100, 999 - a - b) if a + b < 899 else None
            if not c:
                return None
            return mcq("Bir çiftlikte %d tavuk, %d ördek ve %d kaz var. Çiftlikte kaç kanatlı hayvan var?" % (a, b, c), num(a + b + c),
                       [num(a + b + c + 100), num(a + b), num(a + b + c - 10)], "%s + %s + %s = <b>%s</b>." % (num(a), num(b), num(c), num(a + b + c)))
        a, b = ri(5, 9), ri(10, 25)
        t = a * b
        c = ri(10, t - 10)
        return mcq("Bir kolide %d paket var, her pakette %d bisküvi var. Bisküvilerden %d tanesi yendi. Kaç bisküvi kaldı?" % (a, b, c), str(t - c),
                   [str(t + c), str(t), str(a + b - c) if a + b > c else str(t - c + 10)], "%d × %d = %d. %d − %d = <b>%d</b>." % (a, b, t, t, c, t - c))

    def islem_sec():
        name = K.next()
        F = [("%s, 48 cevizi 6 arkadaşına eşit dağıttı. Her arkadaşın kaç cevizi olduğunu bulmak için hangi işlem yapılır?", "48 ÷ 6", ["48 × 6", "48 − 6", "48 + 6"]),
             ("Bir kutuda 8 kalem var. 7 kutudaki kalem sayısını bulmak için hangi işlem yapılır?", "7 × 8", ["7 + 8", "8 − 7", "56 ÷ 8"]),
             ("%s 125 TL biriktirdi, 38 TL harcadı. Kalan parasını bulmak için hangi işlem yapılır?", "125 − 38", ["125 + 38", "125 × 38", "125 ÷ 38"]),
             ("Bir otobüste 34 yolcu vardı, durakta 15 yolcu bindi. Otobüsteki yolcu sayısını bulmak için hangi işlem yapılır?", "34 + 15", ["34 − 15", "34 × 15", "34 ÷ 15"]),
             ("Her gün 9 sayfa okuyan %s, 6 günde kaç sayfa okur? Hangi işlem yapılır?", "6 × 9", ["6 + 9", "9 − 6", "9 ÷ 6"]),
             ("72 öğrenci 8 eşit takıma ayrılıyor. Bir takımdaki öğrenci sayısını bulmak için hangi işlem yapılır?", "72 ÷ 8", ["72 × 8", "72 − 8", "72 + 8"]),
             ("Bir manavda 350 kg domates vardı, 120 kg satıldı. Kalan domatesi bulmak için hangi işlem yapılır?", "350 − 120", ["350 + 120", "350 ÷ 120", "350 × 120"]),
             ("Bir kitap 96 sayfa, diğeri 128 sayfa. İki kitabın toplam sayfa sayısını bulmak için hangi işlem yapılır?", "96 + 128", ["128 − 96", "128 × 96", "128 ÷ 96"]),
             ("4 sıra sandalyenin her sırasında 9 sandalye var. Toplam sandalye sayısını bulmak için hangi işlem yapılır?", "4 × 9", ["4 + 9", "9 − 4", "36 ÷ 4"]),
             ("%s 63 boncuğu 7 eşit ipe dizdi. Bir ipte kaç boncuk olduğunu bulmak için hangi işlem yapılır?", "63 ÷ 7", ["63 × 7", "63 − 7", "63 + 7"])]
        t, g, w = ch(F)
        q = t % name if "%s" in t else t
        return mcq(q, g, w, "Problemde istenen şeye göre işlem seçilir: <b>%s</b>." % g)

    def tahmin_kontrol():
        a, b = ri(210, 480), ri(110, 480)
        if a + b >= 1000:
            return None
        s = a + b
        cands = [s, s + 100, s - 100, s + 10]
        name = K.next()
        return mcq("%s, %d + %d işlemini yaptı. Sonucun yaklaşık kaç olması gerektiğini tahmin ederek doğru cevabı seç." % (name, a, b), num(s),
                   [num(x) for x in cands[1:]], "%d ≈ %d, %d ≈ %d, tahmin %d. Tahmine en yakın ve doğru sonuç <b>%s</b>." % (a, round(a, -2), b, round(b, -2), round(a, -2) + round(b, -2), num(s)))

    def eksik_bilgi():
        F = [("Ayşe Hanım pazardan 3 kg elma aldı. Elmalara kaç lira ödedi?", "1 kg elmanın fiyatı", ["Ayşe Hanım’ın yaşı", "Pazarın adı", "Elmaların rengi"]),
             ("Bir otobüs saat 08.00 olunca yola çıktı. Saat kaçta varır?", "Yolculuğun ne kadar sürdüğü", ["Otobüsün rengi", "Şoförün adı", "Yolcuların yaşı"]),
             ("Sınıftaki öğrenciler eşit gruplara ayrılacak. Her grupta kaç öğrenci olur?", "Öğrenci sayısı ve grup sayısı", ["Sınıfın kaçıncı katta olduğu", "Öğretmenin adı", "Tahtanın boyu"]),
             ("Ali kalem kutusuna kalem ekledi. Kutuda kaç kalem oldu?", "Kutudaki ve eklenen kalem sayısı", ["Kalemlerin rengi", "Kutunun fiyatı", "Ali’nin boyu"]),
             ("Bir kitapçıda bugün kitap satıldı. Kaç kitap kaldı?", "İlk baştaki ve satılan kitap sayısı", ["Kitapçının adresi", "Kitapların sayfa sayısı", "Kasiyerin adı"]),
             ("Mert her gün bir miktar su içiyor. Bir haftada kaç bardak su içer?", "Mert’in bir günde içtiği bardak sayısı", ["Bardakların rengi", "Haftanın ilk günü", "Mert’in sınıfı"])]
        q, g, w = ch(F)
        return mcq("“%s” Bu problemi çözmek için hangi bilgi gerekir?" % q, g, w, "Soruyu cevaplamak için <b>%s</b> bilinmelidir." % g.lower())

    sets = [("İki işlemli problemler", [(iki_adim, 20)]),
            ("Hangi işlem yapılır?", [(islem_sec, 10), (iki_adim, 10)]),
            ("Tahmin ve kontrol", [(tahmin_kontrol, 20)]),
            ("Eksik bilgi ve problem kurma", [(eksik_bilgi, 6), (iki_adim, 14)]),
            ("Karışık problemler", [(iki_adim, 20)])]
    return unit("dort-islem-problemleri", "I", "MAT.3.2.5, MAT.3.2.6, MAT.3.2.7", 15, "Dört İşlem Gerektiren Günlük Yaşam Problemleri", "Dört İşlem Problemleri",
                "Dört işlem gerektiren durumlarda verilen yönergeleri izleyerek yorumlar; dört işlem gerektiren günlük yaşam problemlerini çözer ve problem durumlarını yapılandırır.",
                "3. sınıf dört işlem problemleri çalışma kâğıdı: toplama, çıkarma, çarpma ve bölme gerektiren iki işlemli problemler, uygun işlemi seçme, tahmin ve kontrol, eksik bilgi. 100 soru ve cevap anahtarı.",
                "Verilenler, istenen, işlem, kontrol", "Önce ne istendiğini bul, sonra işlemi seç.", sets,
                ["Problemi dikkatlice oku. Verilenleri ve isteneni belirle.",
                 "Hangi işlemin gerektiğine karar ver: birleştirme toplama, kalanı bulma çıkarma, eşit grupları sayma çarpma, eşit paylaştırma bölmedir.",
                 "Sonucu tahminle karşılaştır ve problemin sorusuna uygun olup olmadığını kontrol et."],
                [("4 kutuda 12'şer kalem var, 9 kalem verildi.", ["4 × 12 = 48", "48 − 9 = 39"], "39 kalem"),
                 ("85 TL vardı, 3 tane 15 TL'lik kitap aldı.", ["3 × 15 = 45", "85 − 45 = 40"], "40 TL")],
                [["Sayıların hepsini toplamak", "Her sayının ne anlama geldiğini düşün"], ["Yalnızca ilk işlemi yapıp bırakmak", "İstenen bulunana kadar devam et"],
                 ["Birimi yazmamak", "Cevabın yanına birimi yaz: 39 kalem"]],
                [("Problemi nasıl anlarım?", "Kendi cümlelerinle yeniden anlat ve resmini çiz. Verilenleri ve isteneni ayrı ayrı yaz."),
                 ("İki işlemli problem nedir?", "Sonuca ulaşmak için iki işlem gereken problemdir. Önce bir ara sonuç bulunur, sonra bu sonuçla ikinci işlem yapılır."),
                 ("Problem kurmak nasıl yapılır?", "Bir işlem seç (örneğin 6 × 8) ve bu işlemle çözülen bir günlük yaşam durumu anlat.")])


# ============================================================ 16. eşitlik
def terazi(left, right):
    s = [line(150, 30, 150, 112, INK, 3), "<polygon points='130,120 170,120 150,104' fill='%s'/>" % INK, line(40, 34, 260, 34, INK, 3)]
    for x, t in ((70, left), (230, right)):
        s.append(line(x - 40, 34, x - 40, 50, INK, 1.5) + line(x + 40, 34, x + 40, 50, INK, 1.5))
        s.append("<rect x='%d' y='50' width='80' height='30' rx='6' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x - 40, FILL, GREEN))
        s.append(text(x, 71, t, 15))
    return wrap(300, 126, "".join(s), "dengedeki terazi: sol %s, sağ %s" % (left, right))


def u16():
    def bos():
        op = ch(["+", "−", "×"])
        if op == "+":
            a, b = ri(5, 60), ri(5, 60)
            v = a + b
            c = ri(1, v - 1)
            if c in (a, b):
                return None
            return mcq("%d + %d = %d + …" % (a, b, c), str(v - c), [str(v), str(v + c), str(v - c + 1)],
                       "Sol taraf %d. %d + %d = %d olduğu için <b>%d</b>." % (v, c, v - c, v, v - c))
        if op == "−":
            a, b = ri(30, 99), ri(5, 29)
            v = a - b
            c = ri(v + 1, 99)
            return mcq("%d − %d = %d − …" % (a, b, c), str(c - v), [str(v), str(c + v), str(c - v + 1)],
                       "Sol taraf %d. %d − %d = %d olduğu için <b>%d</b>." % (v, c, c - v, v, c - v))
        a, b = ri(2, 9), ri(2, 9)
        v = a * b
        divs = [d for d in range(2, 10) if v % d == 0 and d not in (a, b) and v // d <= 10]
        if not divs:
            return None
        c = ch(divs)
        return mcq("%d × %d = %d × …" % (a, b, c), str(v // c), [str(v), str(v // c + 1), str(v - c)], "Sol taraf %d. %d × %d = %d olduğu için <b>%d</b>." % (v, c, v // c, v, v // c))

    def dogru_yanlis():
        a, b = ri(10, 80), ri(10, 80)
        v = a + b
        good = R.random() < 0.5
        c = ri(5, v - 5)
        d = v - c if good else v - c + ch([1, -1, 10, -10])
        g = "Doğru" if good else "Yanlış"
        return mcq("“%d + %d = %d + %d” eşitliği doğru mu?" % (a, b, c, d), g, ["Yanlış" if good else "Doğru", "Yalnızca sol taraf doğru", "Eşittir işareti sonuç gösterir"],
                   "Sol taraf %d, sağ taraf %d. Eşitlik <b>%s</b>." % (v, c + d, g.lower()))

    def ayni_sonuc():
        v = ri(12, 48)
        a = ri(2, v - 2)
        opts = []
        good = "%d + %d" % (a, v - a)
        bads = ["%d + %d" % (a, v - a + 1), "%d − %d" % (v, a), "%d + %d" % (a + 1, v - a + 1)]
        return mcq("Hangi işlemin sonucu %d sayısına eşittir?" % v, good, bads, "%s = %d. Eşittir işareti iki tarafın aynı değerde olduğunu gösterir." % (good, v))

    def terazi_q():
        a, b = ri(5, 40), ri(5, 40)
        c = ri(2, a + b - 2)
        v = a + b - c
        return mcq("Terazi dengede. Sağ kefedeki kutuda kaç olmalıdır?" + terazi("%d + %d" % (a, b), "%d + ?" % c), str(v),
                   [str(a + b), str(v + 1), str(a + b + c)], "Sol %d. %d + %d = %d: <b>%d</b>." % (a + b, c, v, a + b, v))

    def esittir_anlam():
        F = [("“7 + 5 = …” işleminde eşittir işareti neyi gösterir?", "İki tarafın aynı değerde olduğunu", ["Cevabın hemen yazılacağını", "Toplama yapılacağını", "Sağdaki sayının büyük olduğunu"]),
             ("“12 = 4 + …” ifadesinde noktalı yere hangi sayı gelir?", "8", ["16", "12", "4"]),
             ("“3 × 4 = 6 + …” ifadesinde noktalı yere hangi sayı gelir?", "6", ["12", "18", "7"]),
             ("“20 − 5 = 10 + …” ifadesinde noktalı yere hangi sayı gelir?", "5", ["15", "25", "10"]),
             ("“18 ÷ 3 = 2 × …” ifadesinde noktalı yere hangi sayı gelir?", "3", ["6", "9", "12"]),
             ("“5 + 5 + 5 = … × 5” ifadesinde noktalı yere hangi sayı gelir?", "3", ["15", "5", "10"]),
             ("Hangisi “8 + 6” ile aynı değerdedir?", "7 + 7", ["8 + 7", "6 + 6", "14 + 6"]),
             ("Hangisi “4 × 6” ile aynı değerdedir?", "3 × 8", ["4 + 6", "5 × 6", "2 × 10"]),
             ("“… = 9 + 9” ifadesinde noktalı yere hangi sayı gelir?", "18", ["9", "81", "0"]),
             ("“30 = 6 × …” ifadesinde noktalı yere hangi sayı gelir?", "5", ["24", "36", "6"])]
        q, g, w = ch(F)
        return mcq(q, g, w, "Eşittir işaretinin iki tarafı aynı değerdedir: <b>%s</b>." % g)

    sets = [("Eşitliği tamamlama", [(bos, 20)]),
            ("Doğru mu yanlış mı?", [(dogru_yanlis, 20)]),
            ("Dengedeki terazi", [(terazi_q, 20)]),
            ("Aynı sonucu veren işlemler", [(ayni_sonuc, 14), (esittir_anlam, 6)]),
            ("Karışık", [(bos, 12), (esittir_anlam, 4), (terazi_q, 4)])]
    return unit("esitlik", "I", "MAT.3.2.8", 16, "Dört İşlem Bağlamında Eşitlik", "Eşitlik",
                "Dört işlem bağlamında eşitliğin farklı anlamlarını yorumlar: eşitliğin kullanımını inceler ve aynı sonucu veren dört işlemleri farklı sayılarla ifade eder.",
                "3. sınıf eşitlik çalışma kâğıdı: eşitliği tamamlama, eşitliğin doğru mu yanlış mı olduğu, dengedeki terazi, aynı sonucu veren işlemler. 100 soru ve cevap anahtarı.",
                "= işaretinin iki tarafı eşittir", "Önce bilinen tarafın değerini bul.", sets,
                ["Eşittir işareti (=) “sonuç şudur” demek değildir; iki tarafın aynı değerde olduğunu gösterir.",
                 "Eşitliği tamamlamak için önce bilinen tarafın değerini hesapla, sonra diğer tarafı bu değere eşitle.",
                 "Dengedeki terazide iki kefe eşittir: 7 + 5 = 9 + 3."],
                [("8 + 7 = 10 + …", ["sol taraf 15", "10 + 5 = 15"], "5"), ("4 × 6 = 3 × …", ["sol taraf 24", "3 × 8 = 24"], "8")],
                [["8 + 7 = 10 + 15 yazmak", "Sağ taraf da 15 etmeli: 10 + 5"], ["Eşittir işaretinin sağına hep sonucu yazmak", "Eşittir, iki tarafın dengesidir"],
                 ["Yalnızca sol tarafı kontrol etmek", "Her iki tarafın değerini hesapla"]],
                [("Eşitlik nedir?", "İki ifadenin aynı değerde olmasıdır: 6 + 4 = 5 + 5."),
                 ("Terazi örneği neden kullanılır?", "Dengede duran terazinin iki kefesi eşit ağırlıktadır. Eşitliğin iki tarafı da böyledir."),
                 ("Bir sayı birden çok şekilde yazılabilir mi?", "Evet: 12 = 6 + 6 = 3 × 4 = 20 − 8 = 24 ÷ 2.")])


# ============================================================ 17. geometrik cisimler
CISIM = {"küp": (8, 6, 12), "dikdörtgenler prizması": (8, 6, 12), "kare prizma": (8, 6, 12), "üçgen prizma": (6, 5, 9),
         "kare piramit": (5, 5, 8), "üçgen piramit": (4, 4, 6), "silindir": (0, 3, 2), "koni": (1, 2, 1), "küre": (0, 1, 0)}
NESNE = [("zar", "küp"), ("kibrit kutusu", "dikdörtgenler prizması"), ("ayakkabı kutusu", "dikdörtgenler prizması"), ("tuğla", "dikdörtgenler prizması"),
         ("futbol topu", "küre"), ("portakal", "küre"), ("misket", "küre"), ("konserve kutusu", "silindir"), ("bardak", "silindir"), ("davul", "silindir"),
         ("dondurma külahı", "koni"), ("trafik konisi", "koni"), ("doğum günü şapkası", "koni"), ("Mısır piramitleri", "kare piramit"), ("buz küpü", "küp"),
         ("çadır (Toblerone kutusu gibi)", "üçgen prizma")]


def cisim_svg(kind):
    from de_common import solid_svg
    m = {"küp": "wuerfel", "dikdörtgenler prizması": "quader", "küre": "kugel", "silindir": "zylinder", "koni": "kegel", "kare piramit": "pyramide"}
    s = solid_svg(m[kind])
    import re
    return re.sub(r"aria-label='[^']*'", "aria-label='bir geometrik cisim'", s, count=1)


def u17():
    def ad():
        k = ch(["küp", "dikdörtgenler prizması", "küre", "silindir", "koni", "kare piramit"])
        return mcq("Resimdeki geometrik cismin adı nedir?" + cisim_svg(k), cap(k),
                   [cap(x) for x in sh(["küp", "dikdörtgenler prizması", "küre", "silindir", "koni", "kare piramit"]) if x != k],
                   "Bu cisim <b>%s</b>." % k)

    def sayi():
        k = ch(["küp", "dikdörtgenler prizması", "kare prizma", "üçgen prizma", "kare piramit", "üçgen piramit"])
        w = ch(["köşe", "yüz", "ayrıt"])
        v = CISIM[k][["köşe", "yüz", "ayrıt"].index(w)]
        others = [x for x in CISIM[k] if x != v]
        GEN = {"küp": "küpün", "dikdörtgenler prizması": "dikdörtgenler prizmasının", "kare prizma": "kare prizmanın", "üçgen prizma": "üçgen prizmanın",
               "kare piramit": "kare piramidin", "üçgen piramit": "üçgen piramidin"}
        POS = {"köşe": "köşesi", "yüz": "yüzü", "ayrıt": "ayrıtı"}
        return mcq("Bir %s kaç %s vardır?" % (GEN[k], POS[w]), str(v), [str(x) for x in others] + [str(v + 2), str(v - 2)],
                   "%s: %d köşe, %d yüz, %d ayrıt." % (cap(k), CISIM[k][0], CISIM[k][1], CISIM[k][2]))

    def nesne2():
        g = ch(["küp", "dikdörtgenler prizması", "küre", "silindir", "koni"])
        good = ch([o for o, k in NESNE if k == g])
        bad = sh([o for o, k in NESNE if k != g])[:3]
        return mcq("Hangisi %s modeline benzer? (%s)" % (g, ", ".join(sorted([good] + bad))), cap(good), [cap(b) for b in bad],
                   "%s, %s modeline benzer." % (cap(good), g))

    def nesne():
        o, g = ch(NESNE)
        return mcq("%s hangi geometrik cisme benzer?" % cap(o), cap(g), [cap(x) for x in sh(["küp", "dikdörtgenler prizması", "küre", "silindir", "koni", "kare piramit", "üçgen prizma"]) if x != g],
                   "%s <b>%s</b> modeline benzer." % (cap(o), g))

    def ozellik():
        F = [("Hangi cismin hiç köşesi yoktur?", "Küre", ["Küp", "Koni", "Kare piramit"]), ("Hangi cismin bütün yüzleri karedir?", "Küp", ["Dikdörtgenler prizması", "Silindir", "Kare piramit"]),
             ("Hangi cisim kayarak değil, yuvarlanarak hareket eder?", "Küre", ["Küp", "Dikdörtgenler prizması", "Kare piramit"]),
             ("Hangi cismin 1 köşesi vardır?", "Koni", ["Küre", "Silindir", "Küp"]), ("Hangi cismin iki yüzü daire, bir yüzü eğridir?", "Silindir", ["Koni", "Küre", "Küp"]),
             ("Hangi cismin tabanı kare, yan yüzleri üçgendir?", "Kare piramit", ["Küp", "Üçgen prizma", "Silindir"]),
             ("İki yüzün birleştiği çizgiye ne denir?", "Ayrıt", ["Köşe", "Yüz", "Kenar"]), ("Ayrıtların birleştiği noktaya ne denir?", "Köşe", ["Ayrıt", "Yüz", "Taban"]),
             ("Geometrik cismin dış yüzeyindeki düz bölgelere ne denir?", "Yüz", ["Köşe", "Ayrıt", "Kenar"]),
             ("Ayrıt ile kenar arasındaki fark nedir?", "Kenar düzlemsel şekillerde, ayrıt cisimlerde kullanılır", ["İkisi aynı şeydir", "Kenar cisimlerde, ayrıt şekillerde kullanılır", "Ayrıt yalnızca kürede bulunur"]),
             ("Hangi cismin hem düz hem eğri yüzü vardır?", "Silindir", ["Küp", "Küre", "Kare piramit"]), ("Hangi cismin 6 yüzü vardır?", "Dikdörtgenler prizması", ["Kare piramit", "Üçgen prizma", "Silindir"]),
             ("Hangi cisim üst üste kolayca dizilebilir?", "Küp", ["Küre", "Koni", "Kare piramit"]), ("Hangi cismin 4 yüzü vardır?", "Üçgen piramit", ["Kare piramit", "Küp", "Üçgen prizma"])]
        q, g, w = ch(F)
        return mcq(q, g, w, "Doğru cevap: <b>%s</b>." % g)

    def karsilastir():
        a, b = sh(["küp", "üçgen prizma", "kare piramit", "üçgen piramit", "dikdörtgenler prizması"])[:2]
        w = ch(["köşe", "yüz", "ayrıt"])
        i = ["köşe", "yüz", "ayrıt"].index(w)
        va, vb = CISIM[a][i], CISIM[b][i]
        if va == vb:
            g = "İkisinin %s sayısı eşittir" % w
        else:
            g = "%s cisminin %s sayısı %d fazladır" % (cap(a if va > vb else b), w, abs(va - vb))
        bads = ["İkisinin %s sayısı eşittir" % w, "%s cisminin %s sayısı %d fazladır" % (cap(b if va > vb else a), w, abs(va - vb) or 1),
                "%s cisminin %s sayısı %d fazladır" % (cap(a if va > vb else b), w, abs(va - vb) + 1),
                "%s cisminin %s sayısı 2 fazladır" % (cap(a), w), "%s cisminin %s sayısı 2 fazladır" % (cap(b), w)]
        return mcq("%s ile %s cisimlerinin %s sayılarını karşılaştır." % (cap(a), b, w), g, bads,
                   "%s: %d %s, %s: %d %s. %s." % (cap(a), va, w, b, vb, w, g))

    sets = [("Cisimleri tanıma", [(ad, 6), (nesne2, 14)]),
            ("Köşe, yüz ve ayrıt sayısı", [(sayi, 18), (karsilastir, 2)]),
            ("Çevremizdeki cisimler", [(nesne, 16), (nesne2, 4)]),
            ("Cisimlerin özellikleri", [(ozellik, 14), (karsilastir, 6)]),
            ("Karşılaştırma", [(karsilastir, 12), (nesne2, 8)])]
    return unit("geometrik-cisimler", "G", "MAT.3.3.1", 17, "Geometrik Cisimler: Köşe, Yüz ve Ayrıt", "Geometrik Cisimler",
                "Geometrik cisimlerin köşe, yüz ve ayrıt özelliklerini yorumlar; kenar ile ayrıt arasındaki farkı ifade eder.",
                "3. sınıf geometrik cisimler çalışma kâğıdı: küp, dikdörtgenler prizması, üçgen prizma, piramit, silindir, koni ve küre, köşe, yüz ve ayrıt sayıları, çevremizdeki cisimler. 100 soru ve cevap anahtarı.",
                "Köşe, yüz, ayrıt", "Küp: 8 köşe, 6 yüz, 12 ayrıt.", sets,
                ["Geometrik cisimlerin yüzleri, ayrıtları ve köşeleri vardır. İki yüzün birleştiği çizgi ayrıt, ayrıtların birleştiği nokta köşedir.",
                 "Küp ve dikdörtgenler prizmasının 8 köşesi, 6 yüzü ve 12 ayrıtı vardır. Kürenin köşesi ve ayrıtı yoktur.",
                 "Düzlemsel şekillerde “kenar”, cisimlerde “ayrıt” denir."],
                [("Kare piramit", ["tabanda 4 köşe + tepe 1", "taban 1 + yanlar 4"], "5 köşe, 5 yüz, 8 ayrıt"), ("Konserve kutusu", ["iki daire yüz, bir eğri yüz"], "silindir")],
                [["Görünmeyen yüzleri saymamak", "Arkadaki ve alttaki yüzleri de say"], ["Ayrıta kenar demek", "Cisimlerde ayrıt denir"],
                 ["Küpü kare sanmak", "Kare düz bir şekil, küp bir cisimdir"]],
                [("Küp ile dikdörtgenler prizması arasındaki fark nedir?", "Küpün bütün yüzleri eş karelerdir. Dikdörtgenler prizmasının yüzleri dikdörtgendir."),
                 ("Kürenin kaç yüzü vardır?", "Kürenin tek bir eğri yüzü vardır; köşesi ve ayrıtı yoktur."),
                 ("Cisimlerin açınımı bu sınıfta var mı?", "Hayır. Açınımlar sonraki sınıflarda çalışılır; 3. sınıfta köşe, yüz ve ayrıtlar incelenir.")])


# ============================================================ 18. geometrik şekiller
SEKIL = {3: "üçgen", 4: "dörtgen", 5: "beşgen", 6: "altıgen", 8: "sekizgen"}


def poligon(n, irregular=False):
    r = 52
    pts = []
    rot = -math.pi / 2 + (R.uniform(-0.3, 0.3) if irregular else 0)
    for i in range(n):
        a = rot + 2 * math.pi * i / n + (R.uniform(-0.25, 0.25) if irregular else 0)
        rr = r * (R.uniform(0.7, 1.0) if irregular else 1)
        pts.append((64 + rr * math.cos(a), 64 + rr * math.sin(a)))
    s = "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.4' stroke-linejoin='round'/>" % (" ".join("%.1f,%.1f" % p for p in pts), FILL, GREEN)
    return wrap(128, 128, s, "bir çokgen")


def dortgen(kind, diag=False):
    if kind == "kare":
        w = h = 100
    else:
        w, h = 150, 84
    s = "<rect x='8' y='8' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2.4'/>" % (w, h, FILL, GREEN)
    if diag:
        s += line(8, 8, 8 + w, 8 + h, RED, 2, " stroke-dasharray='6 4'") + line(8 + w, 8, 8, 8 + h, RED, 2, " stroke-dasharray='6 4'")
    return wrap(w + 16, h + 16, s, kind)


def u18():
    def ad():
        n = ch([3, 4, 5, 6, 8])
        return mcq("Resimdeki şeklin adı nedir?" + poligon(n, R.random() < 0.4), cap(SEKIL[n]), [cap(SEKIL[x]) for x in sh(SEKIL) if x != n],
                   "%d kenarı ve %d köşesi var: <b>%s</b>." % (n, n, SEKIL[n]))

    def kenar():
        n = ch([3, 4, 5, 6, 8])
        w = ch(["kenarı", "köşesi"])
        w = ch(["kenarı", "köşesi"])
        return mcq("Bir %sin kaç %s vardır?" % (SEKIL[n], w),
                   str(n), [str(x) for x in (3, 4, 5, 6, 8) if x != n], "%s: %d kenar, %d köşe." % (cap(SEKIL[n]), n, n))

    def ad_sayi():
        n = ch([3, 4, 5, 6, 8])
        return mcq("%d kenarlı bir çokgene ne ad verilir?" % n, cap(SEKIL[n]), [cap(SEKIL[x]) for x in sh(SEKIL) if x != n],
                   "%d kenarlı çokgen <b>%s</b>." % (n, SEKIL[n]))

    def kosegen():
        k = ri(0, 2)
        if k == 0:
            kind = ch(["kare", "dikdörtgen"])
            return mcq("%s kaç köşegen çizilebilir?" % ("Bir karede" if kind == "kare" else "Bir dikdörtgende") + dortgen(kind, True),
                       "2", ["1", "4", "0"], "Karşılıklı köşeleri birleştiren 2 doğru parçası çizilir: <b>2</b> köşegen.")
        if k == 1:
            return mcq("Üçgende kaç köşegen çizilebilir?", "0", ["1", "2", "3"], "Üçgenin her köşesi diğer iki köşeye kenarla bağlıdır. Üçgenin köşegeni <b>yoktur</b>.")
        return mcq("Köşegen nedir?", "Komşu olmayan iki köşeyi birleştiren doğru parçası", ["Bir kenarın uzunluğu", "İki komşu köşeyi birleştiren kenar", "Şeklin ortasındaki nokta"],
                   "Köşegen, çokgenin <b>komşu olmayan</b> iki köşesini birleştirir.")

    def hangisi():
        n = ch([3, 4, 5, 6, 8])
        items = sh([n] + sh([x for x in (3, 4, 5, 6, 8) if x != n])[:3])
        pics = "".join(poligon(x, R.random() < 0.4) for x in items)
        k = items.index(n)
        lab = "ABCD"
        s = []
        for i, x in enumerate(items):
            s.append("<b>%s)</b>%s" % (lab[i], poligon(x, R.random() < 0.4)))
        return mcq("Hangisi %s?%s" % (SEKIL[n], "".join(s)), lab[k], [lab[i] for i in range(4) if i != k],
                   "%s şeklinin %d kenarı var: <b>%s</b>." % (lab[k], n, SEKIL[n]))

    def arac():
        F = [("Bir doğru parçası çizmek için hangisi kullanılır?", "Cetvel", ["Pergel", "Gönye", "Silgi"]),
             ("Bir çember çizmek için hangisi kullanılır?", "Pergel", ["Cetvel", "Gönye", "İletki"]),
             ("Kare ya da dikdörtgen çizerken dik köşe oluşturmak için hangisi kullanılır?", "Gönye", ["Pergel", "Silgi", "Kalemtıraş"]),
             ("Kareli kâğıtta 3 kare uzunluğunda kenar çizmek için ne yapılır?", "Kareleri sayarak çizgi çekilir", ["Pergel açılır", "Gözle tahmin edilir", "Kâğıt katlanır"]),
             ("Noktalı kâğıtta bir üçgen çizmek için en az kaç nokta birleştirilir?", "3", ["2", "4", "5"]),
             ("Noktalı kâğıtta bir altıgen çizmek için kaç nokta birleştirilir?", "6", ["5", "8", "4"]),
             ("Ekranda geometrik şekil çizmek için hangi araç kullanılabilir?", "Dinamik geometri yazılımı", ["Hesap makinesi", "Takvim", "Termometre"]),
             ("Kare çizerken kenarların eşit olduğunu nasıl kontrol ederiz?", "Cetvelle her kenarı ölçeriz", ["Rengine bakarız", "Köşelerini sayarız", "Kâğıdı çevireriz"])]
        q, g, w = ch(F)
        return mcq(q, g, w, "Doğru cevap: <b>%s</b>." % g)

    sets = [("Şekilleri tanıma", [(ad, 20)]),
            ("Kenar ve köşe sayısı", [(kenar, 10), (ad_sayi, 5), (hangisi, 5)]),
            ("Hangisi?", [(hangisi, 20)]),
            ("Köşegen", [(kosegen, 4), (ad, 16)]),
            ("Çizim araçları", [(arac, 8), (hangisi, 12)])]
    return unit("geometrik-sekiller", "G", "MAT.3.3.2, MAT.3.3.3", 18, "Geometrik Şekiller: Üçgen, Dörtgen, Beşgen, Altıgen, Sekizgen", "Geometrik Şekiller",
                "Kenar sayılarına göre üçgen, dörtgen, beşgen, altıgen ve sekizgeni sınıflandırır ve adlandırır; kare ve dikdörtgende köşegenleri belirler; matematiksel araç ve teknolojilerle şekil çizer.",
                "3. sınıf geometrik şekiller çalışma kâğıdı: üçgen, dörtgen, beşgen, altıgen ve sekizgen, kenar ve köşe sayısı, kare ve dikdörtgende köşegen, çizim araçları. 100 soru ve cevap anahtarı.",
                "Şeklin adı kenar sayısından gelir", "Üç kenar üçgen, beş kenar beşgen, sekiz kenar sekizgen.", sets,
                ["Çokgenlere kenar sayılarına göre ad verilir: 3 kenar üçgen, 4 kenar dörtgen, 5 kenar beşgen, 6 kenar altıgen, 8 kenar sekizgen.",
                 "Bir çokgenin kenar sayısı köşe sayısına eşittir.",
                 "Köşegen komşu olmayan iki köşeyi birleştirir. Kare ve dikdörtgende 2 köşegen vardır; üçgende köşegen yoktur."],
                [("6 kenarlı şekil", ["altı kenar"], "altıgen"), ("Dikdörtgenin köşegenleri", ["karşılıklı köşeler birleştirilir"], "2")],
                [["Şekil döndürülünce adının değiştiğini sanmak", "Dönen şeklin kenar sayısı aynıdır"], ["Kenarları değil köşeleri yanlış saymak", "Kenar sayısı = köşe sayısı"],
                 ["Kenarı köşegen sanmak", "Köşegen komşu olmayan köşeleri birleştirir"]],
                [("Kare bir dörtgen midir?", "Evet. Kare ve dikdörtgen dört kenarlı oldukları için dörtgendir."),
                 ("Daire bir çokgen midir?", "Hayır. Dairenin kenarı ve köşesi yoktur, çokgen değildir."),
                 ("Sekizgeni nerede görebilirim?", "Trafikteki “DUR” levhası sekizgen biçimindedir.")])


# ============================================================ 19. çevre uzunluğu
def kenarli(pts, labels, unit_="cm"):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    W, H = max(xs) + 40, max(ys) + 34
    cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.4'/>" % (" ".join("%d,%d" % p for p in pts), FILL, GREEN)]
    for i, lab in enumerate(labels):
        if lab is None:
            continue
        a, b = pts[i], pts[(i + 1) % len(pts)]
        mx, my = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0
        dx, dy = mx - cx, my - cy
        d = math.hypot(dx, dy) or 1
        s.append(text(mx + dx / d * 18, my + dy / d * 16 + 5, "%s%s%s" % (lab, NB, unit_), 13, col=BLUE))
    return wrap(W, H, "".join(s), "kenar uzunlukları verilen şekil", lg=True)


def u19():
    def ucgen():
        a, b, c = ri(3, 15), ri(3, 15), ri(3, 15)
        if a + b <= c or a + c <= b or b + c <= a:
            return None
        pts = [(30, 140), (230, 140), (30 + ri(40, 160), 30)]
        return mcq("Şeklin çevre uzunluğu kaç santimetredir?" + kenarli(pts, [a, b, c]), "%d cm" % (a + b + c),
                   ["%d cm" % (a + b), "%d cm" % (a * b), "%d cm" % (a + b + c + a)] if a * b != a + b + c else ["%d cm" % (a + b), "%d cm" % (a + b + c + 1), "%d cm" % (a + b + c + a)],
                   "Çevre = kenarların toplamı: %d + %d + %d = <b>%d cm</b>." % (a, b, c, a + b + c))

    def dikdortgen():
        a, b = ri(3, 20), ri(2, 12)
        if a == b:
            return None
        pts = [(30, 30), (230, 30), (230, 130), (30, 130)]
        return mcq("Dikdörtgenin çevre uzunluğu kaç santimetredir?" + kenarli(pts, [a, b, None, None]), "%d cm" % (2 * (a + b)),
                   ["%d cm" % (a + b), "%d cm" % (a * b), "%d cm" % (2 * a + b)] if a * b != 2 * (a + b) else ["%d cm" % (a + b), "%d cm" % (2 * a + b), "%d cm" % (a + 2 * b)],
                   "Karşılıklı kenarlar eşittir: %d + %d + %d + %d = <b>%d cm</b>." % (a, b, a, b, 2 * (a + b)))

    def kare():
        a = ri(2, 25)
        pts = [(30, 30), (150, 30), (150, 150), (30, 150)]
        return mcq("Karenin bir kenarı %d cm. Çevre uzunluğu kaç santimetredir?" % a + kenarli(pts, [a, None, None, None]), "%d cm" % (4 * a),
                   ["%d cm" % (2 * a), "%d cm" % (a * a) if a * a != 4 * a else "%d cm" % (5 * a), "%d cm" % (a + 4)],
                   "Karenin 4 kenarı eşit: 4 × %d = <b>%d cm</b>." % (a, 4 * a))

    def kareli():
        w, h = ri(2, 7), ri(1, 5)
        if w == h:
            return None
        q = 22
        s = []
        for x in range(10):
            for y in range(7):
                s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='#c9d6df' stroke-width='0.8'/>" % (8 + x * q, 8 + y * q, q, q))
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' fill-opacity='0.6' stroke='%s' stroke-width='2.6'/>" % (8 + q, 8 + q, w * q, h * q, FILL, GREEN))
        pic = wrap(10 * q + 16, 7 * q + 16, "".join(s), "kareli kâğıtta dikdörtgen", lg=True)
        return mcq("Her karenin kenarı 1 birim. Boyalı şeklin çevre uzunluğu kaç birimdir?" + pic, "%d birim" % (2 * (w + h)),
                   ["%d birim" % (w * h) if w * h != 2 * (w + h) else "%d birim" % (2 * (w + h) + 2), "%d birim" % (w + h), "%d birim" % (2 * (w + h) - 2)],
                   "Kenarlar %d ve %d birim: %d + %d + %d + %d = <b>%d birim</b>." % (w, h, w, h, w, h, 2 * (w + h)))

    def eksik():
        k = ri(0, 1)
        if k == 0:
            a, b = ri(4, 15), ri(3, 12)
            P = 2 * (a + b)
            return mcq("Bir dikdörtgenin çevresi %d cm, uzun kenarı %d cm. Kısa kenarı kaç santimetredir?" % (P, a), "%d cm" % b,
                       ["%d cm" % (P - a), "%d cm" % (P - 2 * a), "%d cm" % (b + 1)], "%d − %d − %d = %d, iki kısa kenar %d cm: %d ÷ 2 = <b>%d cm</b>." % (P, a, a, 2 * b, 2 * b, 2 * b, b))
        a = ri(2, 20)
        return mcq("Bir karenin çevresi %d cm. Bir kenarı kaç santimetredir?" % (4 * a), "%d cm" % a, ["%d cm" % (2 * a), "%d cm" % (4 * a - 4), "%d cm" % (a + 1)],
                   "%d ÷ 4 = <b>%d cm</b>." % (4 * a, a))

    def tahmin():
        F = [("Bir defterin çevresi", "yaklaşık 1 m (100 cm)", ["yaklaşık 10 cm", "yaklaşık 10 m", "yaklaşık 1 km"]),
             ("Sınıf tahtasının çevresi", "yaklaşık 8 m", ["yaklaşık 8 cm", "yaklaşık 80 m", "yaklaşık 8 km"]),
             ("Bir futbol sahasının çevresi", "yaklaşık 300 m", ["yaklaşık 300 cm", "yaklaşık 30 cm", "yaklaşık 3 m"]),
             ("Bir posta pulunun çevresi", "yaklaşık 10 cm", ["yaklaşık 10 m", "yaklaşık 100 m", "yaklaşık 1 km"]),
             ("Bir masanın üst yüzünün çevresi", "yaklaşık 4 m", ["yaklaşık 4 cm", "yaklaşık 40 m", "yaklaşık 4 km"]),
             ("Okul bahçesinin çevresi", "yaklaşık 200 m", ["yaklaşık 20 cm", "yaklaşık 2 m", "yaklaşık 20 km"])]
        q, g, w = ch(F)
        return mcq("%s ne kadardır?" % q, g, w, "Gerçek nesneyi düşünerek tahmin et: <b>%s</b>." % g)

    sets = [("Üçgenin çevresi", [(ucgen, 20)]),
            ("Dikdörtgenin ve karenin çevresi", [(dikdortgen, 12), (kare, 8)]),
            ("Kareli kâğıtta çevre", [(kareli, 20)]),
            ("Eksik kenarı bulma", [(eksik, 20)]),
            ("Tahmin ve karışık", [(tahmin, 6), (kare, 7), (ucgen, 7)])]
    return unit("cevre-uzunlugu", "G", "MAT.3.3.4", 19, "Çevre Uzunluğu: Ölçme ve Tahmin", "Çevre Uzunluğu",
                "Standart olmayan ve standart araçlarla çevre uzunluğunu tahmin eder, ölçme sonucuyla karşılaştırarak yargıda bulunur.",
                "3. sınıf çevre uzunluğu çalışma kâğıdı: üçgen, kare ve dikdörtgenin çevresi, kareli kâğıtta çevre, eksik kenarı bulma ve çevreyi tahmin etme. 100 soru ve cevap anahtarı.",
                "Çevre = bütün kenarların toplamı", "Karenin çevresi 4 × kenar.", sets,
                ["Bir şeklin çevre uzunluğu, bütün kenarlarının uzunlukları toplamıdır.",
                 "Karenin 4 kenarı eşittir. Dikdörtgenin karşılıklı kenarları eşittir.",
                 "Ölçmeden önce tahmin et, sonra ölç ve tahminini sonuçla karşılaştır."],
                [("Kenarları 5 cm, 7 cm, 9 cm olan üçgen", ["5 + 7 + 9"], "21 cm"), ("Kenarları 8 cm ve 3 cm olan dikdörtgen", ["8 + 3 + 8 + 3"], "22 cm")],
                [["Dikdörtgenin yalnızca iki kenarını toplamak", "Dört kenarın hepsini topla"], ["Kareli kâğıtta kareleri saymak", "Çevre için kenarları say"],
                 ["Birimi yazmamak", "Cevabın yanına birimi yaz: 22 cm"]],
                [("Çevre uzunluğu nerede kullanılır?", "Bahçeye çit çekerken, bir resmin çerçevesini yaparken ya da pist uzunluğunu hesaplarken."),
                 ("Standart olmayan araçla ölçmek ne demek?", "Karış, adım ya da ataş gibi araçlarla ölçmektir. Kişiden kişiye farklı sonuç verebilir."),
                 ("Alan ile çevre aynı mıdır?", "Hayır. Çevre kenarların toplam uzunluğu, alan ise şeklin kapladığı yerdir.")])


# ============================================================ 20. sıvı ölçme
def kap(level, maxl=4, lab="L"):
    """ölçekli kap: level litre (0.5'lik)"""
    H, W = 150, 80
    s = ["<path d='M30 10 L30 %d L%d %d L%d 10' fill='none' stroke='%s' stroke-width='2.4'/>" % (10 + H, 30 + W, 10 + H, 30 + W, INK)]
    wh = H * level / float(maxl)
    s.append("<rect x='32' y='%.1f' width='%d' height='%.1f' fill='#7fb8e6'/>" % (10 + H - wh, W - 4, wh))
    for i in range(0, maxl * 2 + 1):
        y = 10 + H - H * i / float(maxl * 2)
        long_ = i % 2 == 0
        s.append(line(30 + W - (16 if long_ else 9), y, 30 + W, y, INK, 1.6))
        if long_ and i:
            s.append(text(30 + W + 22, y + 5, "%d%sL" % (i // 2, NB), 13))
    return wrap(30 + W + 50, H + 22, "".join(s), "ölçekli kap", lg=True)


def u20():
    def oku_():
        mx = ch([4, 5, 6])
        lv = ri(1, mx * 2 - 1) / 2.0
        g = "%d litre" % lv if lv == int(lv) else ("yarım litre" if lv == 0.5 else "%d buçuk litre" % int(lv))
        alts = sh(["%d litre" % x for x in range(1, mx + 1) if x != lv]) + ["yarım litre", "%d buçuk litre" % int(lv + 1)]
        return mcq("Bu kap en çok %d litre alır. Kapta kaç litre su vardır?" % mx + kap(lv, mx), cap(g), [cap(a) for a in alts if a != g],
                   "Su %s çizgisine kadar dolu: <b>%s</b>." % (g, g))

    def yarim():
        k = ri(0, 2)
        if k == 0:
            n = ri(2, 10)
            return mcq("%d tane yarım litrelik şişe kaç litre eder?" % (2 * n), "%d litre" % n, ["%d litre" % (2 * n), "%d litre" % (n + 1), "%d litre" % (4 * n)],
                       "İki yarım litre 1 litredir. %d ÷ 2 = <b>%d litre</b>." % (2 * n, n))
        if k == 1:
            n = ri(1, 9)
            return mcq("%d litre su kaç tane yarım litrelik şişeyi doldurur?" % n, str(2 * n), [str(n), str(n + 2), str(4 * n)],
                       "1 litre 2 tane yarım litredir. %d × 2 = <b>%d</b>." % (n, 2 * n))
        n = ri(2, 6)
        return mcq("%d buçuk litre kaç tane yarım litredir?" % n, str(2 * n + 1), [str(n), str(2 * n), str(n + 1)],
                   "%d litre = %d yarım litre, buçuk = 1 yarım litre: <b>%d</b>." % (n, 2 * n, 2 * n + 1))

    def tahmin():
        F = [("Bir çay bardağının alabileceği su", "1 litreden az", ["Yaklaşık 10 litre", "Yaklaşık 100 litre", "Yaklaşık 1000 litre"]),
             ("Bir kovanın alabileceği su", "Yaklaşık 10 litre", ["1 litreden az", "Yaklaşık 1000 litre", "Yaklaşık 100 litre"]),
             ("Bir küvetin alabileceği su", "Yaklaşık 150 litre", ["Yaklaşık 1 litre", "Yaklaşık 15 litre", "1 litreden az"]),
             ("Bir sürahinin alabileceği su", "Yaklaşık 2 litre", ["Yaklaşık 200 litre", "Yaklaşık 20 litre", "1 litreden az"]),
             ("Bir çaydanlığın alabileceği su", "Yaklaşık 2 litre", ["Yaklaşık 50 litre", "Yaklaşık 500 litre", "1 litreden az"]),
             ("Bir su damlasının hacmi", "1 litreden çok az", ["Yaklaşık 1 litre", "Yaklaşık 10 litre", "Yaklaşık 2 litre"]),
             ("Bir otomobilin yakıt deposu", "Yaklaşık 50 litre", ["Yaklaşık 5 litre", "1 litreden az", "Yaklaşık 5000 litre"]),
             ("Bir damacana su", "Yaklaşık 19 litre", ["Yaklaşık 2 litre", "Yaklaşık 190 litre", "1 litreden az"]),
             ("Bir şişe ayran", "Yarım litre ya da daha az", ["Yaklaşık 10 litre", "Yaklaşık 50 litre", "Yaklaşık 100 litre"]),
             ("Bir çiçek saksısını sulamak için gereken su", "Yaklaşık yarım litre", ["Yaklaşık 50 litre", "Yaklaşık 500 litre", "Yaklaşık 20 litre"])]
        q, g, w = ch(F)
        return mcq("%s ne kadardır?" % q, g, w, "Günlük hayattaki kapları düşün: <b>%s</b>." % g.lower())

    def problem():
        k = ri(0, 3)
        name = K.next()
        if k == 0:
            a, b = ri(2, 15), ri(2, 15)
            return mcq("Bir kovada %d litre, diğer kovada %d litre su var. İki kovada toplam kaç litre su vardır?" % (a, b), "%d litre" % (a + b),
                       ["%d litre" % abs(a - b) if a != b else "%d litre" % (a + b + 2), "%d litre" % (a + b + 1), "%d litre" % (a * b)], "%d + %d = <b>%d litre</b>." % (a, b, a + b))
        if k == 1:
            t, u = ri(10, 30), ri(2, 9)
            return mcq("%d litrelik bir bidondan %d litre su kullanıldı. Bidonda kaç litre su kaldı?" % (t, u), "%d litre" % (t - u),
                       ["%d litre" % (t + u), "%d litre" % (t - u + 1), "%d litre" % u], "%d − %d = <b>%d litre</b>." % (t, u, t - u))
        if k == 2:
            n, s = ri(3, 9), ch([2, 3, 4, 5])
            return mcq("%s her gün %d litre süt alıyor. %d günde kaç litre süt alır?" % (name, s, n), "%d litre" % (n * s),
                       ["%d litre" % (n + s), "%d litre" % (n * s + s), "%d litre" % (n * s - 1)], "%d × %d = <b>%d litre</b>." % (n, s, n * s))
        n = ri(3, 9)
        b = ch([2, 3, 4, 5])
        return mcq("%d litre limonata %d litrelik sürahilere eşit olarak dolduruluyor. Kaç sürahi gerekir?" % (n * b, b), str(n), [str(n * b), str(n + 1), str(b)],
                   "%d ÷ %d = <b>%d</b>." % (n * b, b, n))

    def kiyas():
        a, b = sh([0.5, 1, 1.5, 2, 3, 4])[:2]
        f = lambda v: "yarım litre" if v == 0.5 else ("%d litre" % v if v == int(v) else "%d buçuk litre" % int(v))
        x, y = sorted([f(a), f(b)])
        g = f(max(a, b))
        return mcq("Hangisi daha fazladır: %s, %s?" % (mi(x), mi(y)), cap(g), [cap(f(min(a, b))), "İkisi eşit", "Karşılaştırılamaz"],
                   "<b>%s</b> daha fazladır." % g)

    sets = [("Kaptaki suyu okuma", [(oku_, 20)]),
            ("Litre ve yarım litre", [(yarim, 20)]),
            ("Sıvı miktarını tahmin etme", [(tahmin, 10), (kiyas, 10)]),
            ("Problemler", [(problem, 20)]),
            ("Karışık", [(oku_, 6), (problem, 14)])]
    return unit("sivi-olcme", "G", "MAT.3.3.5", 20, "Sıvıları Ölçme: Litre ve Yarım Litre", "Sıvı Ölçme",
                "Standart sıvı ölçü birimi (litre) cinsinden sıvı miktarını tahmin eder ve ölçme sonucuyla karşılaştırarak yargıda bulunur.",
                "3. sınıf sıvı ölçme çalışma kâğıdı: litre ve yarım litre, ölçekli kaptaki suyu okuma, sıvı miktarını tahmin etme ve karşılaştırma, sıvı ölçme problemleri. 100 soru ve cevap anahtarı.",
                "Sıvılar litre (L) ile ölçülür", "2 yarım litre = 1 litre.", sets,
                ["Sıvıların miktarı litre ile ölçülür ve L ile gösterilir.",
                 "İki tane yarım litre bir litre eder. Bir buçuk litre, bir litre ile yarım litredir.",
                 "Ölçmeden önce tahmin yap: çay bardağı 1 litreden az, kova yaklaşık 10 litre su alır."],
                [("6 tane yarım litre", ["2 yarım = 1 litre", "6 ÷ 2"], "3 litre"), ("4 litre su, yarım litrelik şişeler", ["4 × 2"], "8 şişe")],
                [["Yarım litreyi 1 litre saymak", "İki yarım litre 1 litredir"], ["Kap büyükse içindeki su çoktur sanmak", "Kabın içindeki suyun seviyesine bak"],
                 ["Ölçekte çizgileri yanlış okumak", "Kısa çizgiler yarım litreyi gösterir"]],
                [("Litre ne kadardır?", "Büyük bir su şişesi 1 litre ya da 1,5 litredir. 1 litre yaklaşık 5 çay bardağı sudur."),
                 ("Sıvıları neden litre ile ölçeriz?", "Herkesin aynı birimi kullanması için. Böylece alışverişte ve tariflerde ölçüler karışmaz."),
                 ("Mililitreyi bu sınıfta öğreniyor muyuz?", "3. sınıfta litre ve yarım litre kullanılır. Mililitre sonraki sınıflarda öğrenilir.")])


# ============================================================ 21. simetri
import gen_de_mathe_k3_achsensymmetrie as SY


def u21():
    SY.R = R

    def hangisi():
        hs = [SY.half() for _ in range(4)]
        if not all(hs):
            return None
        good = SY.mirror(hs[0])
        bads = [SY.broken(SY.mirror(hs[1])), SY.shifted(hs[2]), SY.broken(SY.mirror(hs[3]))]
        if not all(bads) or any(b == SY.mirror({(x, y) for x, y in b if x < 3}) for b in bads):
            return None
        figs = bads + [good]
        R.shuffle(figs)
        k = figs.index(good)
        pic = SY.four(figs).replace("vier Figuren A bis D", "A, B, C, D şekilleri")
        return mcq(pic + "Hangi şekil kırmızı doğruya göre simetriktir?", "ABCD"[k], ["ABCD"[i] for i in range(4) if i != k],
                   "Yalnızca %s şeklinde sol ve sağdaki kareler simetri doğrusuna eşit uzaklıktadır." % "ABCD"[k])

    def tamamla():
        h = SY.half()
        if not h:
            return None
        good = SY.mirror(h)
        shf = SY.shifted(h)
        nr = SY.broken(good)
        flipped = set(h) | {(SY.COLS - 1 - x, SY.ROWS - 1 - y) for x, y in h}
        opts = [good, shf, nr, flipped]
        if not nr or len({frozenset(o) for o in opts}) < 4:
            return None
        pic_half = wrap(SY.COLS * SY.Q + 20, SY.ROWS * SY.Q + 20, SY.grid(10, 10, h), "simetri doğrusu ile şeklin yarısı")
        R.shuffle(opts)
        k = opts.index(good)
        return mcq(pic_half + "Şeklin sol yarısı verilmiştir. Simetri doğrusuna göre doğru tamamlanmış şekil hangisidir?" + SY.four(opts).replace("vier Figuren A bis D", "A, B, C, D şekilleri"),
                   "ABCD"[k], ["ABCD"[i] for i in range(4) if i != k], "Her kare simetri doğrusuna eşit uzaklıkta, diğer tarafa çizilir: <b>%s</b>." % "ABCD"[k])

    def dogru_sayisi():
        F = [("Kare", "4"), ("Dikdörtgen (kare olmayan)", "2"), ("Daire", "Sonsuz sayıda"), ("Eşkenar üçgen", "3"), ("Kalp", "1"), ("Kelebek", "1"),
             ("Düzgün altıgen", "6"), ("H harfi", "2"), ("A harfi", "1"), ("F harfi", "Hiç yok"), ("8 rakamı", "2"), ("3 rakamı", "1"), ("Ö harfi", "1"),
             ("Ç harfi", "Hiç yok")]
        thing, g = ch(F)
        w = [x for x in ["Hiç yok", "1", "2", "3", "4", "6", "Sonsuz sayıda"] if x != g]
        near_ = {"4": ["2", "8"], "2": ["4", "1"], "3": ["1", "6"], "Sonsuz sayıda": ["1", "4"], "1": ["2", "Hiç yok"], "6": ["3", "12"], "Hiç yok": ["1", "2"]}[g]
        return mcq("%s kaç simetri doğrusuna sahiptir?" % thing, g, near_ + sh(w), "%s: <b>%s</b> simetri doğrusu." % (thing, g.lower() if g[0].isalpha() else g))

    def harf():
        DIK = list("AHİMOTUVWY")
        YATAY = list("BCDEHİKO")
        YOK = list("FGJLNPRSZ")
        kind = ch(["dik", "dik", "yatay", "yok"])
        if kind == "dik":
            a = ch(DIK)
            w = sh(YOK)[:3]
            q = "Hangi harfin <b>dikey</b> simetri doğrusu vardır? %s" % ", ".join(sorted([a] + w))
            e = "%s harfini dikey bir çizgiden katlarsan iki yarısı tam üst üste gelir: <b>%s</b>." % (a, a)
        elif kind == "yatay":
            a = ch([x for x in YATAY if x not in DIK])
            w = sh(YOK)[:3]
            q = "Hangi harfin <b>yatay</b> simetri doğrusu vardır? %s" % ", ".join(sorted([a] + w))
            e = "%s harfinin üst ve alt yarısı tam üst üste gelir: <b>%s</b>." % (a, a)
        else:
            a = ch(YOK)
            w = sh(DIK + [x for x in YATAY if x not in DIK])[:3]
            q = "Hangi harfin simetri doğrusu <b>yoktur</b>? %s" % ", ".join(sorted([a] + w))
            e = "%s harfinin simetri doğrusu yoktur: <b>%s</b>." % (a, a)
        return mcq(q, a, w, e)

    def nokta():
        n = ri(1, 6)
        side = ch(["solunda", "sağında"])
        other = "sağında" if side == "solunda" else "solunda"
        k = ri(0, 1)
        if k == 0:
            g = "Simetri doğrusunun %d kare %s" % (n, other)
            return mcq("Bir kare, dikey simetri doğrusunun %d kare %s. Simetriği nerededir?" % (n, side), g,
                       ["Simetri doğrusunun %d kare %s" % (n, side), "Simetri doğrusunun %d kare %s" % (n + 1, other), "Simetri doğrusunun %d kare %s" % (2 * n, other)],
                       "Simetrik nokta aynı uzaklıkta, diğer taraftadır: <b>%s</b>." % g.lower())
        return mcq("Bir kare simetri doğrusuna %d kare uzaklıkta. Bu kare ile simetriği arasında kaç kare vardır?" % n, "%d kare" % (2 * n),
                   ["%d kare" % n, "%d kare" % (n + 1), "%d kare" % (2 * n + 2)], "Doğruya kadar %d, diğer tarafta yine %d: <b>%d kare</b>." % (n, n, 2 * n))

    sets = [("Simetrik şekli bulma", [(hangisi, 20)]),
            ("Şekli simetrisine göre tamamlama", [(tamamla, 20)]),
            ("Simetri doğrusu sayısı", [(dogru_sayisi, 14), (nokta, 6)]),
            ("Harflerde simetri", [(harf, 20)]),
            ("Karışık", [(hangisi, 7), (tamamla, 7), (nokta, 6)])]
    return unit("simetri", "G", "MAT.3.3.6, MAT.3.3.7, MAT.3.3.8", 21, "Simetri: Simetri Doğrusu ve Simetrik Şekli Tamamlama", "Simetri",
                "Kare, dikdörtgen ve dairenin birden fazla simetri doğrusu olduğunu belirler; bir parçası verilen simetrik şekli yatay ve dikey simetri doğrusuna göre tamamlar; bir şeklin simetrisi hakkında yargıda bulunur.",
                "3. sınıf simetri çalışma kâğıdı: simetrik şekli bulma, yarısı verilen şekli simetri doğrusuna göre tamamlama, simetri doğrusu sayısı, harflerde simetri. 100 soru ve cevap anahtarı.",
                "Simetri doğrusu şekli ikiye böler", "Simetrik nokta doğruya eşit uzaklıkta, diğer taraftadır.", sets,
                ["Bir şekil bir doğru boyunca katlandığında iki parça tam üst üste geliyorsa şekil simetriktir; bu doğruya simetri doğrusu denir.",
                 "Kare 4, kare olmayan dikdörtgen 2 simetri doğrusuna sahiptir. Dairenin sonsuz sayıda simetri doğrusu vardır.",
                 "Simetrik şekli tamamlarken her kareyi simetri doğrusuna olan uzaklığı aynı kalacak şekilde diğer tarafa çiz."],
                [("Doğrunun 3 kare solundaki karenin simetriği", ["aynı uzaklık, diğer taraf"], "3 kare sağında"), ("Dikdörtgen", ["dikey ve yatay"], "2 simetri doğrusu")],
                [["Şekli kaydırarak tamamlamak", "Ayna görüntüsü gibi, ters yöne çiz"], ["Dikdörtgenin köşegenini simetri doğrusu sanmak", "Köşegenden katlanınca parçalar üst üste gelmez"],
                 ["Uzaklığı yanlış saymak", "Kareleri simetri doğrusundan başlayarak say"]],
                [("Simetri nerede görülür?", "Kelebeklerde, yapraklarda, binalarda, halı ve kilim desenlerinde."),
                 ("Bir şeklin simetrik olup olmadığını nasıl anlarım?", "Kâğıda çizip katla. İki yarı tam üst üste geliyorsa şekil simetriktir."),
                 ("Ayna simetriyle nasıl ilişkilidir?", "Aynadaki görüntü, cismin aynaya göre simetriğidir; sağ ve sol yer değiştirir.")])


# ============================================================ 22. veri
KONU = [("en sevilen meyve", ["Elma", "Muz", "Çilek", "Kiraz"]), ("en sevilen renk", ["Kırmızı", "Mavi", "Yeşil", "Sarı"]),
        ("okula geliş şekli", ["Yürüyerek", "Servisle", "Otobüsle", "Arabayla"]), ("en sevilen spor", ["Futbol", "Voleybol", "Basketbol", "Yüzme"]),
        ("evcil hayvan", ["Kedi", "Köpek", "Kuş", "Balık"]), ("en sevilen mevsim", ["İlkbahar", "Yaz", "Sonbahar", "Kış"])]


def sıklık_tablosu(cats, vals, with_cetele=False):
    if with_cetele:
        rows = "".join("<tr><td>%s</td><td>%s</td></tr>" % (c, cetele(v).replace("<svg ", "<svg style='height:26px;width:auto' ", 1)) for c, v in zip(cats, vals))
        return "<table class='sn-table' style='width:auto'><thead><tr><th>Seçenek</th><th>Çetele</th></tr></thead><tbody>%s</tbody></table>" % rows
    rows = "".join("<tr><td>%s</td><td style='text-align:center'>%d</td></tr>" % (c, v) for c, v in zip(cats, vals))
    return "<table class='sn-table' style='width:auto'><thead><tr><th>Seçenek</th><th>Sıklık</th></tr></thead><tbody>%s</tbody></table>" % rows


def nokta_grafigi(cats, vals):
    q = 20
    W = 40 + len(cats) * 90
    top = max(vals)
    H = 30 + top * q + 30
    s = [line(20, H - 30, W - 10, H - 30, INK, 2)]
    for i, (c, v) in enumerate(zip(cats, vals)):
        x = 60 + i * 90
        for k in range(v):
            s.append("<circle cx='%d' cy='%d' r='7.5' fill='%s' stroke='%s' stroke-width='1.2'/>" % (x, H - 30 - 12 - k * q, BLUE, INK))
        s.append(text(x, H - 10, c, 12, weight=600))
    return wrap(W, H, "".join(s), "nokta grafiği", lg=True)


def u22():
    def veri(mx=9):
        t, cats = ch(KONU)
        k = ri(3, 4)
        cats = cats[:k]
        vals = [ri(1, mx) for _ in cats]
        if len(set(vals)) < k:
            return None
        return t, cats, vals

    def soru(t, cats, vals, disp, intro, kinds=(0, 1, 2, 3)):
        k = ch(kinds)
        n = len(cats)
        if k == 0:
            i = ri(0, n - 1)
            return mcq("%s%s“%s” seçeneğini kaç öğrenci seçmiştir?" % (intro, disp, cats[i]), str(vals[i]),
                       [str(vals[i] + 1), str(vals[i] - 1) if vals[i] > 1 else str(vals[i] + 2), str(sum(vals))], "%s: <b>%d</b>." % (cats[i], vals[i]))
        if k == 1:
            big = R.random() < 0.5
            c = max(vals) if big else min(vals)
            i = vals.index(c)
            return mcq("%s%sEn %s seçilen hangisidir?" % (intro, disp, "çok" if big else "az"), cats[i], [x for x in cats if x != cats[i]] + ["Hepsi eşit"],
                       "%s: %d. En %s budur: <b>%s</b>." % (cats[i], c, "çok" if big else "az", cats[i]))
        i, j = sh(range(n))[:2]
        if k == 2:
            a, b = max(vals[i], vals[j]), min(vals[i], vals[j])
            return mcq("%s%s“%s” ile “%s” seçenekleri arasında kaç öğrenci fark vardır?" % (intro, disp, cats[i], cats[j]), str(a - b),
                       [str(a + b), str(a - b + 1), str(a - b - 1) if a - b > 1 else str(a)], "%d − %d = <b>%d</b>." % (a, b, a - b))
        return mcq("%s%sAnkete toplam kaç öğrenci katılmıştır?" % (intro, disp), str(sum(vals)), [str(sum(vals) + 1), str(sum(vals) - 1), str(max(vals))],
                   "%s = <b>%d</b>." % (" + ".join(str(v) for v in vals), sum(vals)))

    def c_oku():
        n = ri(3, 18)
        return mcq("Çetelede kaç çizgi vardır?" + cetele(n), str(n), [str(n + 1), str(n - 1), str(n + 5) if n + 5 != n else str(n + 2), str(n // 5)],
                   "Her demet 5 çizgidir: %d demet ve %d çizgi = <b>%d</b>." % (n // 5, n % 5, n))

    def ctablo():
        d = veri(14)
        if not d:
            return None
        t, cats, vals = d
        return soru(t, cats, vals, sıklık_tablosu(cats, vals, True), "Sınıfta “%s” sorusuyla yapılan araştırmanın çetele tablosu:" % t)

    def stablo():
        d = veri(15)
        if not d:
            return None
        t, cats, vals = d
        return soru(t, cats, vals, sıklık_tablosu(cats, vals), "Sınıfta “%s” sorusuyla yapılan araştırmanın sıklık tablosu:" % t)

    def ngrafik():
        d = veri(8)
        if not d:
            return None
        t, cats, vals = d
        return soru(t, cats, vals, nokta_grafigi(cats, vals), "“%s” araştırmasının nokta grafiği (her nokta 1 öğrenci):" % t)

    def plan():
        F = [("Sınıftaki öğrencilerin en sevdiği meyveyi öğrenmek istiyoruz. İlk adım hangisidir?", "Araştırma sorusunu belirlemek", ["Grafiği çizmek", "Sonucu yorumlamak", "Tabloyu boyamak"]),
             ("Verileri toplarken her cevap için çizgi çizdiğimiz tabloya ne denir?", "Çetele tablosu", ["Nokta grafiği", "Takvim", "Basamak tablosu"]),
             ("Her seçeneği kaç kişinin seçtiğini sayılarla gösteren tabloya ne denir?", "Sıklık tablosu", ["Çetele", "Sayı doğrusu", "Çarpım tablosu"]),
             ("Her veriyi bir noktayla gösteren grafiğe ne denir?", "Nokta grafiği", ["Sıklık tablosu", "Çetele", "Resim"]),
             ("Hangi soru veri toplayarak cevaplanabilir?", "Sınıfımızda en çok hangi spor seviliyor?", ["Bugün günlerden ne?", "3 + 4 kaçtır?", "Okulumuzun adı ne?"]),
             ("Araştırmanın son adımı hangisidir?", "Sonuçları araştırma sorusuna göre değerlendirmek", ["Veri toplamak", "Soru sormak", "Çetele çizmek"]),
             ("Çetelede 5. çizgi nasıl çizilir?", "Önceki dört çizgiyi çaprazlama keser", ["Ayrı bir satıra yazılır", "Daha uzun çizilir", "Çizilmez"]),
             ("Bir araştırmada veriyi toplamak için ne yapılabilir?", "Sınıftaki arkadaşlara soru sormak", ["Tahmin edip yazmak", "Grafiği kopyalamak", "Hiçbir şey yapmamak"])]
        q, g, w = ch(F)
        return mcq(q, g, w, "Doğru cevap: <b>%s</b>." % g)

    sets = [("Çeteleyi okuma", [(c_oku, 12), (plan, 8)]),
            ("Çetele tablosu", [(ctablo, 20)]),
            ("Sıklık tablosu", [(stablo, 20)]),
            ("Nokta grafiği", [(ngrafik, 20)]),
            ("Verileri yorumlama", [(stablo, 10), (ngrafik, 10)])]
    return unit("veri-toplama-ve-nokta-grafigi", "V", "MAT.3.4.1", 22, "Veri Toplama: Çetele, Sıklık Tablosu ve Nokta Grafiği", "Veri ve Grafikler",
                "Kategorik ve sayma ile elde edilen nicel verilerle tek veri grubunda çalışır: araştırma sorusu oluşturur, veri toplar, çetele, sıklık tablosu veya nokta grafiği ile görselleştirir ve sonuçları yorumlar.",
                "3. sınıf veri toplama çalışma kâğıdı: araştırma sorusu, çetele tablosu, sıklık tablosu, nokta grafiği, en çok ve en az seçilen, fark ve toplam. 100 soru ve cevap anahtarı.",
                "Soru → veri → tablo → grafik → yorum", "Çetelede her demet 5 çizgidir.", sets,
                ["Araştırma bir soruyla başlar. Sonra veri toplanır, çetele ya da sıklık tablosuyla düzenlenir.",
                 "Çetelede her veri bir çizgidir; beşinci çizgi önceki dördünü çaprazlama keser. Sıklık tablosu her seçeneğin sayısını gösterir.",
                 "Nokta grafiğinde her nokta bir veridir. Grafikten en çok ve en az seçileni, farkı ve toplamı bulabiliriz."],
                [("Çetele: iki demet ve 3 çizgi", ["5 + 5 + 3"], "13"), ("Elma 7, muz 4", ["7 − 4"], "3 öğrenci fark")],
                [["Çetelede demeti 4 saymak", "Bir demet 5 çizgidir"], ["Farkı bulurken toplamak", "Fark için çıkarma yap"],
                 ["Grafikte satırı karıştırmak", "Seçeneğin adını bulup onun noktalarını say"]],
                [("Kategorik veri nedir?", "Sayı olmayan, gruplara ayrılan veridir: renk, meyve, spor gibi."),
                 ("Çetele neden beşerli demetlenir?", "Çizgileri hızlı ve hatasız saymak için. Demetleri beşer beşer sayarız."),
                 ("Nokta grafiğinin faydası nedir?", "Hangi seçeneğin daha çok seçildiğini bir bakışta gösterir.")])


UNITS = [u11, u12, u13, u14, u15, u16, u17, u18, u19, u20, u21, u22]
