# -*- coding: utf-8 -*-
"""Türkiye 5. sınıf (Maarif Modeli, Ortaokul Matematik 2026): Sayılar ve Nicelikler (2), İstatistiksel Araştırma Süreci,
İşlemlerle Cebirsel Düşünme, Veriden Olasılığa — 11〜20 単元。"""
import math
from fractions import Fraction as F
import tr_g as G
from tr_g import unit, cap, fr, ff, mf, num, dec, oku, mcq, M, wrap, text, line, grid_shape, pie_chart, freq_table, dot_plot, sutun_grafigi, sayi_dogrusu, NB, INK, GREEN, FILL, RED, BLUE
from tr_common import low
import tr_s3a as A


def setup(rnd):
    pass


def ri(a, b):
    return G.R.randint(a, b)


def ch(xs):
    return G.R.choice(list(xs))


def sh(xs):
    return G.sh(xs)


def dz(x, k=None):
    return dec(float(x), k)


def pc(x):
    """F → %25"""
    v = F(x) * 100
    return "%%%s" % (num(v.numerator) if v.denominator == 1 else dec(float(v)))


def yuzluk(k, col="#7fb3d5"):
    """10 × 10 kare, k tanesi boyalı"""
    c = 16
    s = []
    for i in range(100):
        x, y = i % 10, i // 10
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='0.8'/>" % (6 + x * c, 6 + y * c, c, c, col if i < k else "#ffffff", INK))
    return G.wrap(172, 172, "".join(s), "100 eş kareden %d tanesi boyalı" % k)


def kesir_dogrusu(den, lo, hi, mark, lab="A"):
    """0..hi arası, her birim den parçaya bölünmüş sayı doğrusu; mark: Fraction"""
    W = 470
    L, R_ = 30, W - 30
    n = (hi - lo) * den
    s = [line(L - 10, 40, R_ + 12, 40, INK, 2), "<path d='M%d 40 l-9 -5 v10 Z' fill='%s'/>" % (R_ + 16, INK)]
    for i in range(n + 1):
        x = L + (R_ - L) * i / float(n)
        big = i % den == 0
        s.append(line(x, 40 - (9 if big else 5), x, 40 + (9 if big else 5), INK, 2 if big else 1.2))
        if big:
            s.append(text(x, 64, str(lo + i // den), 14))
    x = L + (R_ - L) * float(mark - lo) / (hi - lo)
    s.append("<path d='M%.1f 30 l-6 -10 h12 Z' fill='%s'/>" % (x, RED) + text(x, 14, lab, 14, col=RED))
    return G.wrap(W, 76, "".join(s), "kesirlerle sayı doğrusu", lg=True)


# ============================================================ 11. kesirler
def u11():
    def model():
        b = ch([2, 3, 4, 5, 6, 8, 10])
        a = ri(1, b - 1)
        t = ri(0, 1)
        pic = A.pie(b, a) if t == 0 else A.bar_frac(b, a)
        return mcq("Boyalı kısım bütünün kaçta kaçıdır?" + pic, fr(a, b), [fr(b - a, b), fr(a, b - a) if b - a != a else fr(a, b + 1), fr(b, a), fr(a, b + 1)],
                   "Bütün %d eş parça, %d parça boyalı: <b>%s</b>." % (b, a, fr(a, b)))

    def dogru():
        b = ch([2, 3, 4, 5, 6])
        hi = ch([1, 2, 3])
        k = ri(1, hi * b - 1)
        if k % b == 0:
            return None
        v = F(k, b)
        pic = kesir_dogrusu(b, 0, hi, v)
        g = ff(v, mixed=True)
        return mcq("Sayı doğrusunda A noktasının gösterdiği sayı hangisidir?" + pic, g, [ff(F(k + 1, b), True), ff(F(k, b + 1), True), ff(F(k - 1, b), True) if k > 1 else fr(1, b + 1), fr(b, k) if k < b else ff(F(k + b, b), True)],
                   "Her birim %d eş parçaya bölünmüş. A noktası 0’dan sonraki %d. çizgide: %s." % (b, k, ("%s = <b>%s</b>" % (fr(k, b), g)) if k > b else "<b>%s</b>" % g))

    def donustur():
        b = ri(2, 9)
        w, a = ri(1, 6), ri(1, b - 1)
        k = w * b + a
        if ri(0, 1):
            alts = [mf(w + 1, a, b), mf(w - 1, a, b) if w > 1 else mf(w + 2, a, b)]
            if b - a != a:
                alts.append(mf(w, b - a, b))
            if w < b and w != a and a > 0:
                alts.append(mf(a, w, b))
            alts.append(fr(k, b * w) if b * w != k else fr(k + 1, b))
            return mcq("%s kesrinin tam sayılı kesir gösterimi hangisidir?" % fr(k, b), mf(w, a, b), alts,
                       "%d ÷ %d = %d, kalan %d: <b>%s</b>." % (k, b, w, a, mf(w, a, b)))
        return mcq("%s kesrinin bileşik kesir gösterimi hangisidir?" % mf(w, a, b), fr(k, b), [fr(w + a, b), fr(w * a + b, b), fr(k + 1, b), fr(k, w * b)],
                   "%d × %d + %d = %d: <b>%s</b>." % (w, b, a, k, fr(k, b)))

    def denk():
        b = ri(2, 9)
        a = ri(1, b - 1)
        m = ri(2, 6)
        k = ri(0, 2)
        if k == 0:
            return mcq("%s kesrini %d ile genişletirsek hangi kesir elde edilir?" % (fr(a, b), m), fr(a * m, b * m), [fr(a * m, b), fr(a, b * m), fr(a + m, b + m)],
                       "Pay ve payda %d ile çarpılır: <b>%s</b>." % (m, fr(a * m, b * m)))
        if k == 1:
            g = F(a * m, b * m)
            return mcq("%s kesrinin en sade hâli hangisidir?" % fr(a * m, b * m), ff(g), [fr(a * m // 1, b), fr(a, b * m), fr(a + 1, b + 1) if F(a + 1, b + 1) != g else fr(a + 2, b + 1)],
                       "Pay ve payda ortak bölenlerine bölünür: <b>%s</b>." % ff(g))
        return mcq("%s = <span class='fr'><span class='fn'>?</span><span class='fd'>%d</span></span> eşitliğinde ? kaçtır?" % (fr(a, b), b * m), str(a * m),
                   [str(a + b * m - b), str(a * m + 1), str(b * m - a)], "Payda %d ile çarpıldı, pay da: %d × %d = <b>%d</b>." % (m, a, m, a * m))

    def hayat():
        nm = G.K.next()
        b = ch([4, 6, 8, 10, 12])
        a = ri(b + 1, 3 * b - 1)
        if a % b == 0:
            return None
        w, r = divmod(a, b)
        what, piece = ch([("pizza", "dilim"), ("pasta", "dilim"), ("çikolata", "kare"), ("ekmek", "parça")])
        return mcq("Her biri %d eş %s olan aynı büyüklükte %s var. %s %d %s yedi. Yediği miktarı tam sayılı kesirle nasıl gösteririz?" % (b, piece, "pizzalar" if what == "pizza" else what + "lar" if what[-1] in "aıou" else what + "ler", nm, a, piece),
                   mf(w, r, b), [fr(a, b * (w + 1)), mf(w + 1, r, b), mf(r, w, b) if r != w and w < b else mf(w, r + 1, b)], "%s = <b>%s</b>." % (fr(a, b), mf(w, r, b)))

    sets = [("Modelle kesir", [(model, 20)]),
            ("Sayı doğrusunda kesirler", [(dogru, 20)]),
            ("Bileşik ve tam sayılı kesir", [(donustur, 20)]),
            ("Genişletme ve sadeleştirme", [(denk, 20)]),
            ("Günlük hayatta kesirler", [(hayat, 10), (dogru, 5), (donustur, 5)])]
    return unit("kesirler", "S", "MAT.5.1.3", 11, "Kesirler: Model, Sayı Doğrusu, Genişletme ve Sadeleştirme", "Kesirler",
                "Kesirleri gerçek yaşam durumlarında farklı biçimlerde (kesir, tam sayılı kesir, ondalık gösterim, yüzde) gösterir.",
                "5. sınıf kesirler çalışma kâğıdı: modelle kesir, sayı doğrusunda kesirler, bileşik ve tam sayılı kesir, genişletme, sadeleştirme ve denk kesirler. 100 soru ve cevap anahtarı.",
                "Payda: bütünün kaç eş parçası?", "Genişletme ve sadeleştirme kesrin değerini değiştirmez.", sets,
                ["Kesir, bir bütünün eş parçalarını gösterir. Payda bütünün kaç eş parçaya bölündüğünü, pay kaç parça alındığını gösterir.",
                 "Sayı doğrusunda her birimi paydadaki sayı kadar eş parçaya böleriz; pay kadar parça ilerleriz.",
                 "Pay ve paydayı aynı sayıyla çarpmaya genişletme, aynı sayıya bölmeye sadeleştirme denir. Değer değişmez: 2/3 = 4/6."],
                [("11/4 kesrini tam sayılı yaz", ["11 ÷ 4 = 2, kalan 3"], "2 3/4"), ("12/18 kesrini sadeleştir", ["12 ve 18 ortak bölen 6", "2/3"], "2/3")],
                [["Sadeleştirirken yalnızca payı bölmek", "Pay ve payda aynı sayıya bölünür"], ["Sayı doğrusunda çizgileri değil aralıkları saymamak", "Her aralık bir parçadır"],
                 ["Tam sayılı kesirde kalanı tam kısma yazmak", "Bölüm tam kısım, kalan pay olur"]],
                [("Bir kesrin en sade hâli nedir?", "Pay ve paydanın 1’den başka ortak böleni kalmamış hâlidir."),
                 ("Bileşik kesir sayı doğrusunda nerededir?", "1’e eşit ya da 1’in sağındadır."),
                 ("Denk kesirleri nasıl bulurum?", "Pay ve paydayı aynı sayıyla çarparak ya da bölerek.")])


# ============================================================ 12. ondalık gösterim
BASAMAK = {10: "onda bir", 100: "yüzde bir", 1000: "binde bir"}


def ondalik_oku(x, den):
    """2,13 → iki tam yüzde on üç"""
    w, r = divmod(int(round(x * den)), den)
    d = {10: "onda", 100: "yüzde", 1000: "binde"}[den]
    return "%s tam %s %s" % (oku(w), d, oku(r)) if r else oku(w)


def u12():
    def kesirden():
        den = ch([10, 100, 1000])
        a = ri(1, den * 3 - 1)
        if a % 10 == 0 and den > 10:
            return None
        v = F(a, den)
        g = dz(v)
        k = len(str(den)) - 1
        alts = [dec(a / (den * 10.0)), dec(a / (den / 10.0)) if den > 10 else dec(a * 10.0 / den), "%d,%d" % (a, den)]
        return mcq("%s kesrinin ondalık gösterimi hangisidir?" % fr(a, den), g, alts, "Paydada %d sıfır var; virgülden sonra %d basamak olur: <b>%s</b>." % (k, k, g))

    def ondalikten():
        den = ch([10, 100, 1000])
        a = ri(1, den - 1)
        if a % 10 == 0 and den > 10:
            return None
        v = F(a, den)
        return mcq("%s ondalık gösteriminin kesir gösterimi hangisidir?" % dz(v), fr(a, den), [fr(a, den * 10), fr(a, den // 10) if den > 10 else fr(a, 1000), fr(den, a) if a != den else fr(1, 2)],
                   "Virgülden sonra %d basamak var; payda %s olur: <b>%s</b>." % (len(str(den)) - 1, num(den), fr(a, den)))

    def okunus():
        den = ch([10, 100])
        a = ri(11, den * 9)
        if a % den == 0 or (den == 100 and a % 10 == 0):
            return None
        x = a / float(den)
        g = ondalik_oku(x, den)
        w = [ondalik_oku(x, 10 if den == 100 else 100) if den == 10 else "%s tam onda %s" % (oku(a // den), oku(a % den)),
             "%s tam %s %s" % (oku(a % den), {10: "onda", 100: "yüzde"}[den], oku(a // den)), "%s %s" % ({10: "onda", 100: "yüzde"}[den], oku(a))]
        return mcq("%s sayısının okunuşu hangisidir?" % dec(x), g, w, "Önce tam kısım, sonra “%s” ve virgülden sonraki sayı okunur: <b>%s</b>." % ({10: "onda", 100: "yüzde"}[den], g))

    def basamak():
        v = ri(1001, 99999) / 1000.0
        s = "%.3f" % v
        ip, fp = s.split(".")
        j = ri(0, 2)
        d = fp[j]
        if d == "0" or fp.count(d) > 1 or d in ip:
            return None
        ad = ["onda birler", "yüzde birler", "binde birler"][j]
        return mcq("%s sayısında %s rakamı hangi basamaktadır?" % (dec(v, 3), d), cap(ad) + " basamağı", [cap(x) + " basamağı" for x in ["onda birler", "yüzde birler", "binde birler", "birler"] if x != ad],
                   "Virgülden sonra sırayla onda birler, yüzde birler, binde birler basamağı gelir: <b>%s</b>." % ad)

    def dogru():
        lo = ri(0, 8)
        k = ri(1, 9)
        v = lo + k / 10.0
        pic = sayi_dogrusu(lo * 10, lo * 10 + 10, 1, marks=[(lo * 10 + k, "A")], labels=[lo * 10, lo * 10 + 10])
        pic = pic.replace(">%d<" % (lo * 10), ">%d<" % lo).replace(">%d<" % (lo * 10 + 10), ">%d<" % (lo + 1))
        return mcq("0,1’lik aralıklarla bölünmüş sayı doğrusunda A noktası hangi sayıyı gösterir?" + pic, dec(v), [dec(lo + k / 100.0), dec(lo + (k + 1) / 10.0), dec(lo + 1 + k / 10.0)],
                   "%d ile %d arası 10 eş parçaya bölünmüş; A, %d. çizgide: <b>%s</b>." % (lo, lo + 1, k, dec(v)))

    def para():
        tl_, kr = ri(1, 99), ri(1, 99)
        if kr % 10 == 0:
            return None
        v = tl_ + kr / 100.0
        return mcq("%d lira %d kuruş, lira cinsinden ondalık gösterimle nasıl yazılır?" % (tl_, kr), "%s TL" % dec(v, 2), ["%s TL" % x for x in ("%d,%d" % (tl_, kr * 10), dec(tl_ + kr / 1000.0, 3), dec(tl_ + kr / 10.0, 1) if kr < 10 else "%d,%02d" % (kr, tl_))],
                   "1 lira = 100 kuruş. %d kuruş = %s lira: <b>%s TL</b>." % (kr, fr(kr, 100), dec(v, 2)))

    sets = [("Kesirden ondalık gösterime", [(kesirden, 20)]),
            ("Ondalık gösterimden kesre", [(ondalikten, 20)]),
            ("Okunuş ve basamaklar", [(okunus, 10), (basamak, 10)]),
            ("Sayı doğrusu", [(dogru, 20)]),
            ("Para ve ölçülerde ondalık gösterim", [(para, 14), (kesirden, 6)])]
    return unit("ondalik-gosterim", "S", "MAT.5.1.3", 12, "Ondalık Gösterim: Onda Birler, Yüzde Birler, Binde Birler", "Ondalık Gösterim",
                "Kesirleri gerçek yaşam durumlarında farklı biçimlerde (kesir, tam sayılı kesir, ondalık gösterim, yüzde) gösterir.",
                "5. sınıf ondalık gösterim çalışma kâğıdı: paydası 10, 100, 1000 olan kesirlerin ondalık gösterimi, okunuş, onda birler, yüzde birler ve binde birler basamağı, sayı doğrusu ve para. 100 soru ve cevap anahtarı.",
                "Payda 100 ise virgülden sonra 2 basamak", "0,25 = 25/100: “sıfır tam yüzde yirmi beş”.", sets,
                ["Paydası 10, 100, 1000 olan kesirleri virgül kullanarak yazabiliriz: 3/10 = 0,3; 47/100 = 0,47; 5/1000 = 0,005.",
                 "Virgülden sonraki basamaklar onda birler, yüzde birler, binde birler basamağıdır.",
                 "Okurken önce tam kısım, sonra “tam”, sonra virgülden sonraki sayı paydasıyla okunur: 2,13 → iki tam yüzde on üç."],
                [("7/100", ["Payda 100: iki basamak"], "0,07"), ("3,4", ["Tam kısım 3, onda 4"], "üç tam onda dört")],
                [["7/100 = 0,7", "Payda 100 ise virgülden sonra iki basamak: 0,07"], ["0,25’i “sıfır virgül yirmi beş” diye okumak", "“Sıfır tam yüzde yirmi beş” diye okunur"],
                 ["5 lira 5 kuruşu 5,5 TL yazmak", "5 kuruş = 0,05 TL: 5,05 TL"]],
                [("Ondalık gösterim nerede kullanılır?", "Fiyatlarda (12,50 TL), uzunlukta (1,75 m) ve kütlede (2,5 kg)."),
                 ("0,5 ile 0,50 eşit midir?", "Evet. Sondaki sıfır değeri değiştirmez: 5/10 = 50/100."),
                 ("Virgül hangi basamaklar arasındadır?", "Birler basamağı ile onda birler basamağı arasında.")])


# ============================================================ 13. yüzdeler
def u13():
    def model():
        k = ri(1, 99)
        return mcq("100 eş kareden boyalı olanlar yüzde kaçtır?" + yuzluk(k), "%%%d" % k, ["%%%d" % x for x in (100 - k, k + 10 if k < 90 else k - 10, k + 1)],
                   "100 kareden %d tanesi boyalı: %s = <b>%%%d</b>." % (k, fr(k, 100), k))

    def kesir_yuzde():
        b, a = ch([(2, 1), (4, 1), (4, 3), (5, 1), (5, 2), (5, 3), (5, 4), (10, 1), (10, 3), (10, 7), (10, 9), (20, 1), (20, 3), (20, 7), (25, 1), (25, 4), (50, 1), (50, 7)])
        v = F(a, b)
        if ri(0, 1):
            return mcq("%s kesri yüzde kaçtır?" % fr(a, b), pc(v), ["%%%d" % a, "%%%d" % b, pc(1 - v) if v != F(1, 2) else "%25", "%%%d" % (a * 10)],
                       "Paydayı 100 yaparız: %s = %s = <b>%s</b>." % (fr(a, b), fr(a * 100 // b, 100), pc(v)))
        return mcq("%s hangi kesre eşittir?" % pc(v), ff(v), [fr(int(v * 100), 10) if int(v * 100) < 100 else fr(1, 3), fr(b, a * 10) if b != a * 10 else fr(1, 4), ff(1 - v) if v != F(1, 2) else fr(1, 4), fr(a, b * 10)],
                   "%s = %s = <b>%s</b>." % (pc(v), fr(int(v * 100), 100), ff(v)))

    def ondalik_yuzde():
        k = ri(1, 99)
        if ri(0, 1):
            return mcq("%s ondalık gösterimi yüzde kaçtır?" % dec(k / 100.0, 2), "%%%d" % k, ["%%%s" % dec(k / 100.0, 2), "%%%d" % (k * 10) if k < 10 else "%%%d" % (k // 10 or 1), "%%%d" % (100 - k)],
                       "%s = %s = <b>%%%d</b>." % (dec(k / 100.0, 2), fr(k, 100), k))
        return mcq("%%%d ondalık gösterimle nasıl yazılır?" % k, dec(k / 100.0, 2), [dec(k / 10.0, 1) if k < 100 else "1", dec(k / 1000.0, 3), str(k)],
                   "%%%d = %s = <b>%s</b>." % (k, fr(k, 100), dec(k / 100.0, 2)))

    def kalan():
        k = ri(1, 99)
        what = ch(["Bir sınıftaki öğrencilerin", "Bir bahçedeki ağaçların", "Bir kitabın sayfalarının", "Bir okuldaki öğrencilerin"])
        rest = {"Bir sınıftaki öğrencilerin": "kız", "Bir bahçedeki ağaçların": "meyve ağacı", "Bir kitabın sayfalarının": "okunmuş", "Bir okuldaki öğrencilerin": "gözlüklü"}[what]
        return mcq("%s %%%d kadarı %s. Geriye kalanlar yüzde kaçtır?" % (what, k, rest), "%%%d" % (100 - k), ["%%%d" % x for x in (k, 100 - k + 10 if k > 10 else 100 - k - 1, 100 + k)] if True else [],
                   "Bütün %%100’dür: 100 − %d = <b>%%%d</b>." % (k, 100 - k))

    def ayni():
        trip = [(F(1, 2), "yarım"), (F(1, 4), "çeyrek"), (F(3, 4), "dörtte üç"), (F(1, 5), "beşte bir"), (F(1, 10), "onda bir"), (F(2, 5), "beşte iki")]
        v, ad = ch(trip)
        reps = [ff(v), dz(v), pc(v)]
        g = "%s = %s = %s" % tuple(reps)
        bad1 = "%s = %s = %s" % (ff(v), dz(v * F(1, 10)), pc(v))
        bad2 = "%s = %s = %s" % (ff(v), dz(v), "%%%d" % (v.denominator))
        bad3 = "%s = %s = %s" % (ff(v), "%d,%d" % (v.numerator, v.denominator), pc(v))
        return mcq("“%s” için hangi gösterimler doğrudur?" % ad, g, [bad1, bad2, bad3], "<b>%s</b>." % g)

    sets = [("Yüzlük modelle yüzde", [(model, 20)]),
            ("Kesir ve yüzde", [(kesir_yuzde, 20)]),
            ("Ondalık gösterim ve yüzde", [(ondalik_yuzde, 20)]),
            ("Bütünün yüzdesi", [(kalan, 20)]),
            ("Aynı sayının farklı gösterimleri", [(ayni, 6), (kesir_yuzde, 7), (ondalik_yuzde, 7)])]
    return unit("yuzdeler", "S", "MAT.5.1.3", 13, "Yüzdeler: Kesir, Ondalık Gösterim ve Yüzde", "Yüzdeler",
                "Kesirleri gerçek yaşam durumlarında farklı biçimlerde (kesir, tam sayılı kesir, ondalık gösterim, yüzde) gösterir.",
                "5. sınıf yüzdeler çalışma kâğıdı: yüzlük modelle yüzde, kesri yüzdeye ve yüzdeyi kesre çevirme, ondalık gösterim ve yüzde, bütünün yüzdesi. 100 soru ve cevap anahtarı.",
                "Yüzde, paydası 100 olan kesirdir", "%25 = 25/100 = 1/4 = 0,25", sets,
                ["Yüzde sembolü (%) “yüzde” demektir: %35 = 35/100. Bütün %100’dür.",
                 "Bir kesri yüzdeye çevirmek için paydasını 100 yaparız: 3/4 = 75/100 = %75.",
                 "Ondalık gösterimden yüzdeye: virgülden sonraki iki basamak yüzdeyi verir: 0,07 = %7, 0,4 = 0,40 = %40."],
                [("2/5", ["2/5 = 40/100"], "%40"), ("%8", ["8/100"], "0,08")],
                [["0,4 = %4", "0,4 = 0,40 = %40"], ["%8 = 0,8", "%8 = 8/100 = 0,08"], ["Yüzde sembolünü sayının arkasına yazmak", "Türkçede % sayının önüne yazılır: %25"]],
                [("%100 ne demektir?", "Bütünün tamamı demektir."),
                 ("Yüzdeyi günlük hayatta nerede görürüz?", "İndirimlerde (%20 indirim), pil göstergesinde (%60) ve hava durumunda (yağış olasılığı %30)."),
                 ("%50 neden yarıma eşittir?", "%50 = 50/100 = 1/2.")])


# ============================================================ 14. farklı gösterimleri karşılaştırma
REPS = [F(1, 2), F(1, 4), F(3, 4), F(1, 5), F(2, 5), F(3, 5), F(4, 5), F(1, 10), F(3, 10), F(7, 10), F(9, 10), F(3, 20), F(7, 20), F(1, 20), F(6, 25), F(13, 50)]


def show(v, kind):
    if kind == 0:
        return ff(v)
    if kind == 1:
        return dz(v)
    return pc(v)


def u14():
    def karsilastir():
        a, b = sh(REPS)[:2]
        ka, kb = sh([0, 1, 2])[:2]
        s = "&gt;" if a > b else "&lt;"
        return mcq("%s ○ %s karşılaştırmasında ○ yerine hangi sembol gelir?" % (show(a, ka), show(b, kb)), s, ["&gt;" if s == "&lt;" else "&lt;", "=", "+"],
                   "İkisini aynı gösterime çeviririz: %s ve %s. Cevap <b>%s</b>." % (pc(a), pc(b), s))

    def esit_mi():
        v = ch(REPS)
        ka, kb = sh([0, 1, 2])[:2]
        if ri(0, 1):
            x, y, g = show(v, ka), show(v, kb), "="
        else:
            w = ch([r for r in REPS if r != v])
            x, y = show(v, ka), show(w, kb)
            g = "&gt;" if v > w else "&lt;"
        return mcq("%s ○ %s karşılaştırmasında ○ yerine hangi sembol gelir?" % (x, y), g, [o for o in ["=", "&gt;", "&lt;", "+"] if o != g],
                   "Aynı gösterime çeviririz. Cevap <b>%s</b>." % g)

    def en_buyuk():
        vs = sh(REPS)[:4]
        ks = [ri(0, 2) for _ in vs]
        k = ri(0, 1)
        g = max(vs) if k == 0 else min(vs)
        opts = [show(v, kk) for v, kk in zip(vs, ks)]
        gi = vs.index(g)
        return mcq("%s sayılarından en %s hangisidir?" % (", ".join(opts), "büyüğü" if k == 0 else "küçüğü"), opts[gi], [o for i, o in enumerate(opts) if i != gi],
                   "Yüzdeye çeviririz: %s. En %s <b>%s</b>." % (", ".join(pc(v) for v in vs), "büyük" if k == 0 else "küçük", opts[gi]))

    def sirala():
        vs = sorted(sh(REPS)[:3])
        ks = sh([0, 1, 2])
        opts = {v: show(v, kk) for v, kk in zip(vs, ks)}
        g = " &lt; ".join(opts[v] for v in vs)
        w = [" &lt; ".join(opts[v] for v in p) for p in ([vs[1], vs[0], vs[2]], [vs[2], vs[1], vs[0]], [vs[0], vs[2], vs[1]])]
        return M("%s sayılarının küçükten büyüğe sıralanışı hangisidir?" % ", ".join(opts[v] for v in sh(vs)), g, w,
                 "Yüzdeye çeviririz: %s. Sıralama <b>%s</b>." % (", ".join(pc(v) for v in vs), g))

    def problem():
        n1, n2 = G.K.two()
        a, b = sh(REPS)[:2]
        what = ch(["kitabın", "yapbozun", "ödevinin", "boyama kitabının"])
        q = "%s %s %s kadarını, %s %s %s kadarını bitirdi. Kim daha çok bitirmiştir?" % (n1, what, show(a, 0), n2, what, show(b, ch([1, 2])))
        g = n1 if a > b else n2
        return mcq(q, g, [n2 if g == n1 else n1, "İkisi eşit", "Bilinemez"], "%s ve %s: <b>%s</b>." % (pc(a), pc(b), g))

    def indirim():
        p1, p2 = sh([10, 15, 20, 25, 30, 40, 50])[:2]
        f2 = ch([F(1, 4), F(1, 5), F(1, 2), F(1, 10), F(3, 10)])
        if F(p1, 100) == f2:
            return None
        g = "Birinci mağaza" if F(p1, 100) > f2 else "İkinci mağaza"
        return mcq("Aynı ayakkabıya birinci mağaza %%%d, ikinci mağaza fiyatın %s kadarı indirim yapıyor. Hangi mağazanın indirimi daha fazladır?" % (p1, ff(f2)), g,
                   ["İkinci mağaza" if g == "Birinci mağaza" else "Birinci mağaza", "İkisi eşit", "Bilinemez"], "%s = %s. %%%d ile karşılaştırırız: <b>%s</b>." % (ff(f2), pc(f2), p1, low(g)))

    sets = [("Farklı gösterimleri karşılaştırma", [(karsilastir, 20)]),
            ("Eşit mi?", [(esit_mi, 20)]),
            ("En büyük ve en küçük", [(en_buyuk, 20)]),
            ("Sıralama", [(sirala, 20)]),
            ("Problemler", [(problem, 12), (indirim, 8)])]
    return unit("farkli-gosterimleri-karsilastirma", "S", "MAT.5.1.4", 14, "Kesir, Ondalık Gösterim ve Yüzdeyi Karşılaştırma", "Gösterimleri Karşılaştırma",
                "Farklı biçimlerde gösterilen kesirlerin karşılaştırılmasına yönelik akıl yürütür.",
                "5. sınıf kesir, ondalık gösterim ve yüzde karşılaştırma çalışma kâğıdı: farklı gösterimleri aynı biçime çevirme, büyük, küçük, eşit sembolleri, sıralama ve indirim problemleri. 100 soru ve cevap anahtarı.",
                "Önce aynı gösterime çevir", "Yüzdeye çevirmek karşılaştırmayı kolaylaştırır.", sets,
                ["Kesir, ondalık gösterim ve yüzde aynı sayıyı farklı biçimlerde gösterebilir: 1/4 = 0,25 = %25.",
                 "Karşılaştırmak için sayıları aynı gösterime çeviririz; çoğu zaman yüzde ya da ondalık gösterim en kolayıdır.",
                 "Ondalık gösterimleri karşılaştırırken basamak sayısını eşitleriz: 0,4 = 0,40 &gt; 0,35."],
                [("3/5 ile 0,55", ["3/5 = 0,60", "0,60 &gt; 0,55"], "3/5 &gt; 0,55"), ("%30, 1/4, 0,28", ["%30, %25, %28"], "1/4 &lt; 0,28 &lt; %30")],
                [["0,4 &lt; 0,35 (35 &gt; 4 diye)", "Basamakları eşitle: 0,40 &gt; 0,35"], ["Farklı gösterimleri çevirmeden karşılaştırmak", "Önce aynı gösterime çevir"],
                 ["%5 ile 0,5’i eşit sanmak", "%5 = 0,05; 0,5 = %50"]],
                [("Hangi gösterime çevirmek en kolaydır?", "Paydası 100’e tamamlanabilen kesirlerde yüzde; diğerlerinde ondalık gösterim."),
                 ("0,5 ile 1/2 neden eşittir?", "1/2 = 5/10 = 0,5."),
                 ("Karşılaştırmayı günlük hayatta nerede kullanırız?", "İndirimleri, sınav başarılarını ve oranları karşılaştırırken.")])


# ============================================================ 15. veri ve grafikler
KONU = [("En sevilen meyve", ["Elma", "Muz", "Çilek", "Kiraz", "Portakal"]), ("En sevilen spor", ["Futbol", "Voleybol", "Basketbol", "Yüzme", "Tenis"]),
        ("Okula geliş şekli", ["Yürüyerek", "Servisle", "Otobüsle", "Arabayla", "Bisikletle"]), ("En sevilen renk", ["Mavi", "Kırmızı", "Yeşil", "Mor", "Sarı"]),
        ("En sevilen ders", ["Matematik", "Türkçe", "Fen", "Müzik", "Beden eğitimi"]), ("Tatil tercihi", ["Deniz", "Dağ", "Köy", "Şehir", "Kamp"])]


def u15():
    def veri(n=None, mx=15):
        t, cats = ch(KONU)
        n = n or ri(3, 5)
        cats = sh(cats)[:n]
        vals = [ri(2, mx) for _ in cats]
        if len(set(vals)) < n:
            return None
        return t, cats, vals

    def tablo_q():
        d = veri()
        if not d:
            return None
        t, cats, vals = d
        k = ri(0, 2)
        tab = freq_table(t, cats, vals)
        if k == 0:
            s = sum(vals)
            return mcq("“%s” araştırmasının sıklık tablosu:%sAraştırmaya kaç öğrenci katılmıştır?" % (t, tab), str(s), [str(s + 1), str(max(vals) * len(vals)), str(s - min(vals))],
                       "Sıklıklar toplanır: <b>%d</b>." % s)
        if k == 1:
            g = cats[vals.index(max(vals))]
            return mcq("“%s” araştırmasının sıklık tablosu:%sEn çok tercih edilen hangisidir?" % (t, tab), g, [c for c in cats if c != g] + ["Hepsi eşit"], "En büyük sıklık %d: <b>%s</b>." % (max(vals), g))
        i, j = sh(range(len(cats)))[:2]
        return mcq("“%s” araştırmasının sıklık tablosu:%s%s ve %s seçenlerin toplamı kaçtır?" % (t, tab, cats[i], cats[j]), str(vals[i] + vals[j]),
                   [str(abs(vals[i] - vals[j])), str(vals[i] + vals[j] + 1), str(sum(vals))], "%d + %d = <b>%d</b>." % (vals[i], vals[j], vals[i] + vals[j]))

    def sutun_q():
        d = veri(mx=12)
        if not d:
            return None
        t, cats, vals = d
        pic = sutun_grafigi(list(zip(cats, vals)), "öğrenci")
        i = ri(0, len(cats) - 1)
        k = ri(0, 1)
        if k == 0:
            return mcq("“%s” araştırmasının sütun grafiği:%s%s seçen kaç öğrenci vardır?" % (t, pic, cats[i]), str(vals[i]), [str(vals[i] + 1), str(vals[i] - 1), str(vals[(i + 1) % len(vals)])],
                       "%s sütununun yüksekliği <b>%d</b>." % (cats[i], vals[i]))
        a, b = vals.index(max(vals)), vals.index(min(vals))
        return mcq("“%s” araştırmasının sütun grafiği:%sEn çok ve en az tercih edilen seçenekler arasında kaç öğrenci fark vardır?" % (t, pic), str(vals[a] - vals[b]),
                   [str(vals[a] + vals[b]), str(vals[a] - vals[b] + 1), str(vals[a])], "%d − %d = <b>%d</b>." % (vals[a], vals[b], vals[a] - vals[b]))

    def daire_q():
        t, cats = ch(KONU)
        parts = ch([(2, [1, 1]), (4, [2, 1, 1]), (4, [1, 1, 1, 1]), (4, [3, 1]), (8, [4, 2, 1, 1]), (8, [4, 3, 1]), (10, [5, 3, 2])])
        den, ps = parts
        cats = sh(cats)[:len(ps)]
        n = den * ri(3, 12)
        pic = pie_chart(cats, ps, label="daire grafiği")
        i = ri(0, len(ps) - 1)
        k = ri(0, 1)
        v = F(ps[i], den)
        if k == 0:
            return mcq("“%s” araştırmasına katılanların dağılımı daire grafiğinde gösterilmiştir.%s%s seçenler bütünün ne kadarıdır?" % (t, pic, cats[i]), ff(v),
                       [ff(F(ps[i], den + 1)), ff(1 - v) if v != F(1, 2) else fr(1, 3), fr(ps[i], 10) if den != 10 else fr(1, 4), fr(1, 3)], "Daire %d eş dilime bölünürse %s %d dilim: <b>%s</b>." % (den, cats[i], ps[i], ff(v)))
        return mcq("“%s” araştırmasına %d öğrenci katılmış ve sonuçlar daire grafiğinde gösterilmiştir.%s%s seçen kaç öğrenci vardır?" % (t, n, pic, cats[i]), str(n * ps[i] // den),
                   [str(n // den), str(n - n * ps[i] // den) if n - n * ps[i] // den != n * ps[i] // den else str(n), str(ps[i]), str(n * ps[i] // den + 1)],
                   "%s seçenler bütünün %s kadarı: %d × %s = <b>%d</b>." % (cats[i], ff(v), n, ff(v), n * ps[i] // den))

    def nokta_q():
        n = ri(12, 20)
        lo, hi = 0, ch([5, 6])
        data = [ri(lo, hi) for _ in range(n)]
        pic = dot_plot(lo, hi, data, "nokta grafiği")
        k = ri(0, 2)
        intro = "Bir sınıftaki öğrencilerin bir haftada okudukları kitap sayısı nokta grafiğinde gösterilmiştir."
        if k == 0:
            cnt = {v: data.count(v) for v in range(lo, hi + 1)}
            m = max(cnt.values())
            if list(cnt.values()).count(m) > 1:
                return None
            g = [v for v in cnt if cnt[v] == m][0]
            return mcq(intro + pic + "Veriler en çok hangi değerde toplanmıştır?", str(g), [str(v) for v in range(lo, hi + 1) if v != g], "En uzun nokta sütunu %d: <b>%d</b>." % (g, g))
        if k == 1:
            return mcq(intro + pic + "En az ve en çok kitap okuyan öğrencilerin okudukları kitap sayıları arasındaki fark kaçtır?", str(max(data) - min(data)),
                       [str(max(data)), str(max(data) + min(data)), str(n)], "En büyük %d, en küçük %d: %d − %d = <b>%d</b>." % (max(data), min(data), max(data), min(data), max(data) - min(data)))
        v = ri(lo + 1, hi)
        g = len([x for x in data if x >= v])
        return mcq(intro + pic + "En az %d kitap okuyan kaç öğrenci vardır?" % v, str(g), [str(data.count(v)), str(n - g), str(g + 1)],
                   "%d ve üstündeki noktalar sayılır: <b>%d</b>." % (v, g))

    def yorum():
        d = veri(4)
        if not d:
            return None
        t, cats, vals = d
        tab = freq_table(t, cats, vals)
        nm = G.K.next()
        k = ri(0, 2)
        i = vals.index(max(vals))
        j = vals.index(min(vals))
        if k == 0:
            claim = "“En çok tercih edilen %s.”" % cats[i]
            g = "Doğru"
        elif k == 1:
            claim = "“En çok tercih edilen %s.”" % cats[j]
            g = "Yanlış, en çok tercih edilen %s" % cats[i]
        else:
            s = sum(vals)
            claim = "“Araştırmaya %d öğrenci katıldı.”" % (s + ch([2, -2, 5]))
            g = "Yanlış, %d öğrenci katıldı" % s
        w = ["Doğru", "Yanlış, en çok tercih edilen %s" % cats[i], "Yanlış, %d öğrenci katıldı" % sum(vals), "Yanlış, en az tercih edilen %s" % cats[i]]
        return mcq("“%s” araştırmasının sonuçları:%s%s şu yorumu yaptı: %s Bu yorum hakkında ne söylenebilir?" % (t, tab, nm, claim), g, [x for x in w if x != g], "Tabloya bakarak kontrol ederiz: <b>%s</b>." % g)

    sets = [("Sıklık tablosu", [(tablo_q, 20)]),
            ("Sütun grafiği", [(sutun_q, 20)]),
            ("Daire grafiği", [(daire_q, 20)]),
            ("Nokta grafiği ve dağılım", [(nokta_q, 20)]),
            ("Yorumları değerlendirme", [(yorum, 20)])]
    return unit("veri-ve-grafikler", "IA", "MAT.5.5.1, MAT.5.5.2", 15, "Kategorik Veri: Sıklık Tablosu, Sütun, Daire ve Nokta Grafiği", "Veri ve Grafikler",
                "Kategorik veriyle çalışır ve veriye dayalı karar verir; başkaları tarafından oluşturulan istatistiksel sonuçları ve yorumları tartışır.",
                "5. sınıf veri ve grafikler çalışma kâğıdı: sıklık tablosu, sütun grafiği, daire grafiğinde parça-bütün ilişkisi, nokta grafiği ve verinin dağılımı, yorumları değerlendirme. 100 soru ve cevap anahtarı.",
                "Grafik, verinin dağılımını gösterir", "Bir yorumu verilerle kontrol et.", sets,
                ["İstatistiksel araştırma bir soruyla başlar. Veri toplanır, sıklık tablosuyla düzenlenir ve uygun bir grafikle gösterilir.",
                 "Sütun grafiği kategorileri karşılaştırmayı, daire grafiği her kategorinin bütüne göre payını, nokta grafiği verilerin nerede toplandığını gösterir.",
                 "Başkasının yorumunu değerlendirirken tabloya ve grafiğe bakarak sayılarla kontrol ederiz."],
                [("Daire grafiğinde yarım daire", ["Bütünün 1/2’si"], "%50"), ("Nokta grafiğinde en uzun sütun 3", ["Veriler 3 etrafında toplanmış"], "3")],
                [["Daire grafiğinde dilim sayısını kişi sayısı sanmak", "Dilim, bütünün kesrini gösterir"], ["Grafiğin ölçeğine bakmadan okumak", "Eksendeki sayılarla oku"],
                 ["Bir yorumu kontrol etmeden kabul etmek", "Verilerle karşılaştır"]],
                [("Kategorik veri nedir?", "Renk, spor, meyve gibi sayı olmayan, gruplara ayrılan veridir."),
                 ("Daire grafiği ne zaman kullanılır?", "Her kategorinin bütüne göre ne kadar yer tuttuğunu göstermek için."),
                 ("Veri toplarken nelere dikkat ederim?", "Soru açık olmalı, herkese aynı soru sorulmalı ve her yanıt bir kez sayılmalı.")])


# ============================================================ 16. eşitliğin korunumu ve işlem özellikleri
def u16():
    def korunum():
        a, b = ri(12, 60), ri(12, 60)
        c = ri(2, 15)
        k = ri(0, 2)
        if k == 0:
            return mcq("%d + %d = %d eşitliğinin her iki tarafına %d eklenirse sağ taraf kaç olur?" % (a, b, a + b, c), str(a + b + c), [str(a + b), str(a + b + 2 * c), str(a + c)],
                       "Eşitliğin iki tarafına aynı sayı eklenirse eşitlik korunur: %d + %d = <b>%d</b>." % (a + b, c, a + b + c))
        if k == 1:
            return mcq("%d + %d = %d eşitliğinin her iki tarafından %d çıkarılırsa sağ taraf kaç olur?" % (a, b, a + b, c), str(a + b - c), [str(a + b), str(a + b + c), str(b - c if b > c else b)],
                       "İki taraftan aynı sayı çıkarılırsa eşitlik korunur: %d − %d = <b>%d</b>." % (a + b, c, a + b - c))
        x = ri(2, 9)
        return mcq("%d × %d = %d eşitliğinin her iki tarafı %d ile çarpılırsa sağ taraf kaç olur?" % (a, x, a * x, c), num(a * x * c), [num(a * x + c), num(a * x), num(a * c)],
                   "Her iki taraf aynı sayıyla çarpılırsa eşitlik korunur: %d × %d = <b>%s</b>." % (a * x, c, num(a * x * c)))

    def denge():
        a, b = ri(10, 40), ri(10, 40)
        c = ri(2, 9)
        k = ri(0, 1)
        if k == 0:
            return mcq("%d + %d = ? + %d eşitliğinde ? kaçtır?" % (a, b, b - c), str(a + c), [str(a - c), str(a), str(a + b)],
                       "Sağdaki %d, %d sayısından %d az; bu yüzden ? de %d sayısından %d fazla olmalı: <b>%d</b>." % (b - c, b, c, a, c, a + c))
        if a - c <= 0:
            return None
        return mcq("%d − %d = ? − %d eşitliğinde ? kaçtır?" % (a + 20, a, a - c), str(20 + a - c), [str(20 + a + c), str(20), str(a)],
                   "Çıkan %d azaldı; farkın korunması için eksilen de %d azalmalı: %d − %d = <b>%d</b>." % (c, c, a + 20, c, 20 + a - c))

    def ozellik():
        a, b, c = ri(2, 30), ri(2, 30), ri(2, 30)
        S = [("%d + %d = %d + %d" % (a, b, b, a), "Toplamada değişme özelliği"), ("%d × %d = %d × %d" % (a, b, b, a), "Çarpmada değişme özelliği"),
             ("(%d + %d) + %d = %d + (%d + %d)" % (a, b, c, a, b, c), "Toplamada birleşme özelliği"), ("(%d × %d) × %d = %d × (%d × %d)" % (a, b, c, a, b, c), "Çarpmada birleşme özelliği"),
             ("%d × (%d + %d) = %d × %d + %d × %d" % (a, b, c, a, b, a, c), "Çarpmanın toplama üzerine dağılma özelliği"),
             ("%d × (%d − %d) = %d × %d − %d × %d" % (a, max(b, c), min(b, c), a, max(b, c), a, min(b, c)), "Çarpmanın çıkarma üzerine dağılma özelliği")]
        x, g = ch(S)
        if b == c or a == b:
            return None
        return mcq("%s eşitliğinde hangi özellik kullanılmıştır?" % x, g, [y for _, y in S if y != g], "<b>%s</b>." % g)

    def kolay():
        k = ri(0, 3)
        if k == 0:
            a = ch([25, 50, 20, 5])
            b = {25: 4, 50: 2, 20: 5, 5: 2}[a]
            c = ri(11, 99)
            g = a * b * c
            return mcq("%d × %d × %d işlemini birleşme özelliğiyle kolayca hesaplayınız." % (a, c, b), num(g), [num(a * c + b), num(g + c), num(a * b + c)],
                       "(%d × %d) × %d = %d × %d = <b>%s</b>." % (a, b, c, a * b, c, num(g)))
        if k == 1:
            a = ri(3, 9)
            b = ri(11, 99)
            t = ch([100, 1000])
            c = t - b
            if c <= 0:
                return None
            return mcq("%d × %d + %d × %d işlemini dağılma özelliğiyle kolayca hesaplayınız." % (a, b, a, c), num(a * t), [num(a * b + c), num(a + t), num(a * t + a)],
                       "%d × (%d + %d) = %d × %s = <b>%s</b>." % (a, b, c, a, num(t), num(a * t)))
        if k == 2:
            a = ri(12, 49)
            b = ch([99, 101, 999, 1001, 98, 102])
            near_ = (b + 50) // 100 * 100
            return mcq("%d × %d işlemini dağılma özelliğiyle hesaplayınız." % (a, b), num(a * b), [num(a * near_), num(a * b + a), num(a * b - a)],
                       "%d × (%s %s %d) = %s %s %d = <b>%s</b>." % (a, num(near_), "+" if b > near_ else "−", abs(b - near_), num(a * near_), "+" if b > near_ else "−", a * abs(b - near_), num(a * b)))
        a, b, c = ri(11, 99), ri(11, 99), ri(11, 99)
        t = (a + c)
        if t % 10:
            return None
        return mcq("%d + %d + %d işlemini değişme ve birleşme özellikleriyle kolayca hesaplayınız." % (a, b, c), str(a + b + c), [str(a + b + c + 10), str(t), str(a + b)],
                   "(%d + %d) + %d = %d + %d = <b>%d</b>." % (a, c, b, t, b, a + b + c))

    def esitmi():
        a, b, c = ri(2, 20), ri(2, 20), ri(2, 20)
        S = [("%d − %d" % (a + b, b), "%d − %d" % (b, a + b), "≠"), ("%d ÷ %d" % (a * b, a), "%d ÷ %d" % (a, a * b), "≠"),
             ("%d + %d" % (a, b), "%d + %d" % (b, a), "="), ("%d × (%d + %d)" % (a, b, c), "%d × %d + %d × %d" % (a, b, a, c), "="),
             ("%d × (%d + %d)" % (a, b, c), "%d × %d + %d" % (a, b, c), "≠")]
        x, y, g = ch(S)
        return mcq("%s □ %s ifadesinde □ yerine hangi sembol gelir?" % (x, y), g, ["≠" if g == "=" else "=", "&lt;", "×"],
                   "İki tarafı hesaplayıp karşılaştırırız: <b>%s</b>. Çıkarma ve bölmede değişme özelliği yoktur." % g)

    sets = [("Eşitliğin korunumu", [(korunum, 20)]),
            ("Eşitliği dengeleme", [(denge, 20)]),
            ("İşlem özellikleri", [(ozellik, 20)]),
            ("Özelliklerle kolay hesaplama", [(kolay, 20)]),
            ("= mi, ≠ mi?", [(esitmi, 12), (ozellik, 8)])]
    return unit("esitlik-ve-islem-ozellikleri", "C5", "MAT.5.2.1", 16, "Eşitliğin Korunumu ve İşlem Özellikleri", "Eşitlik ve İşlem Özellikleri",
                "Doğal sayılarla eşitliğin korunumu ile değişme, birleşme ve dağılma özelliklerine ilişkin akıl yürütür.",
                "5. sınıf eşitlik ve işlem özellikleri çalışma kâğıdı: eşitliğin korunumu, eşitliği dengeleme, değişme, birleşme ve dağılma özellikleri, özelliklerle kolay hesaplama. 100 soru ve cevap anahtarı.",
                "İki tarafa aynı işlem: eşitlik korunur", "Dağılma: a × (b + c) = a × b + a × c", sets,
                ["Bir eşitliğin her iki tarafına aynı sayıyı ekler, çıkarır, iki tarafı aynı sayıyla çarparsak ya da sıfırdan farklı aynı sayıya bölersek eşitlik korunur.",
                 "Toplama ve çarpmada değişme ve birleşme özellikleri vardır: sayıların yeri ve gruplanışı sonucu değiştirmez.",
                 "Çarpmanın toplama ve çıkarma üzerine dağılma özelliği: 6 × (10 + 3) = 6 × 10 + 6 × 3. Hesabı kolaylaştırmak için kullanılır."],
                [("25 × 37 × 4", ["(25 × 4) × 37", "100 × 37"], "3.700"), ("34 × 99", ["34 × (100 − 1)", "3.400 − 34"], "3.366")],
                [["Çıkarmada değişme özelliği var sanmak", "15 − 8 ≠ 8 − 15"], ["Dağılmada yalnızca bir terimi çarpmak", "6 × (10 + 3) = 60 + 18, 60 + 3 değil"],
                 ["Eşitliğin bir tarafını değiştirip diğerini unutmak", "İki tarafa aynı işlem yapılmalı"]],
                [("Hangi işlemlerde değişme özelliği vardır?", "Toplama ve çarpmada. Çıkarma ve bölmede yoktur."),
                 ("Dağılma özelliği neden işe yarar?", "Zor bir çarpmayı kolay parçalara ayırır: 7 × 98 = 7 × 100 − 7 × 2."),
                 ("Eşitliğin korunumu ne demektir?", "İki tarafa aynı işlem yapıldığında eşitliğin bozulmamasıdır; terazi dengede kalır.")])


# ============================================================ 17. işlem önceliği
def u17():
    def iki_islem():
        a, b, c = ri(2, 30), ri(2, 9), ri(2, 9)
        k = ri(0, 3)
        if k == 0:
            e, v, w = "%d + %d × %d" % (a, b, c), a + b * c, (a + b) * c
        elif k == 1:
            if a <= b * c:
                return None
            e, v, w = "%d − %d × %d" % (a, b, c), a - b * c, (a - b) * c
        elif k == 2:
            e, v, w = "%d + %d ÷ %d" % (a, b * c, c), a + b, (a + b * c) // c if (a + b * c) % c == 0 else a + b + c
        else:
            e, v, w = "%d × %d − %d" % (b, c, a) if b * c > a else "%d × %d + %d" % (b, c, a), b * c - a if b * c > a else b * c + a, b * (c - a) if c > a else b * c + a + 1
        return mcq("%s işleminin sonucu kaçtır?" % e, num(v), [num(w), num(v + 1), num(v + 10)], "Önce çarpma ve bölme, sonra toplama ve çıkarma yapılır: <b>%s</b>." % num(v))

    def parantez():
        a, b, c = ri(2, 20), ri(2, 20), ri(2, 9)
        k = ri(0, 1)
        if k == 0:
            e, v, w = "(%d + %d) × %d" % (a, b, c), (a + b) * c, a + b * c
        else:
            if a <= b:
                return None
            e, v, w = "%d × (%d − %d)" % (c, a, b), c * (a - b), c * a - b
        return mcq("%s işleminin sonucu kaçtır?" % e, num(v), [num(w), num(v + c), num(v - 1)], "Önce parantez içi yapılır: <b>%s</b>." % num(v))

    def us():
        a = ri(2, 12)
        k = ri(0, 2)
        if k == 0:
            return mcq("%d<sup>2</sup> ifadesinin değeri kaçtır?" % a, num(a * a), [num(2 * a), num(a + 2), num(a * a * a)], "%d<sup>2</sup> = %d × %d = <b>%s</b>." % (a, a, a, num(a * a)))
        if k == 1:
            a = ri(2, 6)
            return mcq("%d<sup>3</sup> ifadesinin değeri kaçtır?" % a, num(a ** 3), [num(3 * a), num(a * a), num(a + 3)], "%d<sup>3</sup> = %d × %d × %d = <b>%s</b>." % (a, a, a, a, num(a ** 3)))
        return mcq("%d × %d ifadesinin üslü gösterimi hangisidir?" % (a, a), "%d<sup>2</sup>" % a, ["2<sup>%d</sup>" % a, "%d<sup>3</sup>" % a, "%d × 2" % a],
                   "Aynı sayı 2 kez çarpılıyor: <b>%d<sup>2</sup></b>." % a)

    def us_oncelik():
        a, b = ri(2, 9), ri(2, 5)
        c = ri(2, 20)
        k = ri(0, 2)
        if k == 0:
            e, v, w = "%d + %d<sup>2</sup>" % (c, a), c + a * a, (c + a) ** 2
        elif k == 1:
            e, v, w = "%d × %d<sup>2</sup>" % (b, a), b * a * a, (b * a) ** 2
        else:
            e, v, w = "%d<sup>2</sup> − %d × %d" % (a + 5, b, a), (a + 5) ** 2 - b * a, ((a + 5) ** 2 - b) * a
        if v < 0 or w < 0:
            return None
        return mcq("%s işleminin sonucu kaçtır?" % e, num(v), [num(w), num(v + a), num(v - 1)], "Önce üslü ifade, sonra çarpma, en son toplama ve çıkarma: <b>%s</b>." % num(v))

    def problem():
        nm = G.K.next()
        a, b, c = ri(3, 9), ri(15, 60), ri(20, 150)
        g = a * b + c
        q = "%s tanesi %d TL olan %d defter ve %d TL’lik bir kalem kutusu aldı. Ödediği parayı gösteren işlem hangisidir?" % (nm, b, a, c)
        return mcq(q, "%d × %d + %d" % (a, b, c), ["%d × (%d + %d)" % (a, b, c), "(%d + %d) × %d" % (a, b, c), "%d + %d + %d" % (a, b, c)],
                   "Önce defterlerin fiyatı (%d × %d), sonra kalem kutusu eklenir: <b>%d × %d + %d = %s</b>." % (a, b, a, b, c, num(g)))

    sets = [("İşlem önceliği", [(iki_islem, 20)]),
            ("Parantezli işlemler", [(parantez, 20)]),
            ("Kare ve küp", [(us, 20)]),
            ("Üslü ifadelerle işlem önceliği", [(us_oncelik, 20)]),
            ("İşlemi yazma", [(problem, 12), (iki_islem, 8)])]
    return unit("islem-onceligi", "C5", "MAT.5.2.2", 17, "İşlem Önceliği, Kare ve Küp", "İşlem Önceliği",
                "Günlük hayat veya matematiksel durumlarda işlem önceliğini yorumlar.",
                "5. sınıf işlem önceliği çalışma kâğıdı: dört işlemde işlem önceliği, parantezli işlemler, bir sayının karesi ve küpü, üslü ifadelerle işlem önceliği ve problemi işlemle yazma. 100 soru ve cevap anahtarı.",
                "Parantez, üs, çarpma-bölme, toplama", "Önce parantez ve üs; aynı öncelikte soldan sağa.", sets,
                ["İşlem sırası: önce parantez içi, sonra üslü ifadeler, sonra çarpma ve bölme, en son toplama ve çıkarma.",
                 "Aynı öncelikteki işlemler soldan sağa doğru yapılır: 20 − 8 + 3 = 15.",
                 "Bir sayının karesi kendisiyle çarpımıdır: 5<sup>2</sup> = 5 × 5 = 25. Küpü üç kez çarpımıdır: 2<sup>3</sup> = 2 × 2 × 2 = 8."],
                [("4 + 3 × 5", ["3 × 5 = 15", "4 + 15"], "19"), ("2 × 3²", ["3² = 9", "2 × 9"], "18")],
                [["4 + 3 × 5 = 35", "Önce çarpma: 4 + 15 = 19"], ["3² = 6", "3² = 3 × 3 = 9"], ["2 × 3² = 36", "Önce üs: 2 × 9 = 18"]],
                [("Neden işlem önceliği vardır?", "Herkesin aynı ifadeden aynı sonucu bulması için."),
                 ("Parantez işlem sırasını nasıl değiştirir?", "Parantez içindeki işlem her zaman önce yapılır: (4 + 3) × 5 = 35."),
                 ("“Üslü ifade” ne demektir?", "Bir sayının kendisiyle tekrar tekrar çarpımının kısa yazılışıdır: 5<sup>2</sup>, 2<sup>3</sup>.")])


# ============================================================ 18. örüntüler
def u18():
    def kural_bul():
        a, b = ri(2, 9), ri(-3, 5)
        xs = [a * n + b for n in range(1, 6)]
        if xs[0] <= 0:
            return None
        def rl(x, y):
            return ("%d × adım sayısı" % x) + ((" + %d" % y) if y > 0 else (" − %d" % -y) if y < 0 else "")
        g = rl(a, b)
        alts = [rl(a + 1, b - 1), "%d + adım sayısı" % xs[0], rl(a, b + 1), rl(a - 1, b + 1) if a > 2 else rl(a + 2, b)]
        return mcq("%s, … örüntüsünün kuralı hangisidir?" % ", ".join(num(x) for x in xs), g, alts,
                   "Her adımda %d artıyor: %d × adım sayısı. 1. adımda %d × 1 = %d, terim %d; fark %s. Kural: <b>%s</b>." % (a, a, a, a, xs[0], ("+%d" % b) if b >= 0 else "−%d" % -b, g))

    def n_terim():
        a, b = ri(2, 9), ri(0, 6)
        n = ch([10, 15, 20, 25, 30, 50, 100])
        g = a * n + b
        rule = "%d × adım sayısı%s" % (a, (" + %d" % b) if b else "")
        return mcq("Kuralı “%s” olan örüntünün %d. adımı kaçtır?" % (rule, n), num(g), [num(a * n), num(a + n + b), num(g + a)], "%d × %d%s = <b>%s</b>." % (a, n, (" + %d" % b) if b else "", num(g)))

    def tablo():
        a, b = ri(2, 7), ri(0, 5)
        n = ri(6, 12)
        rows = "".join("<tr><td style='text-align:center'>%d</td><td style='text-align:center'>%d</td></tr>" % (i, a * i + b) for i in range(1, 5))
        tab = "<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr><th>Adım</th><th>Terim</th></tr></thead><tbody>%s</tbody></table>" % rows
        g = a * n + b
        return mcq("Tablodaki örüntünün %d. adımı kaçtır?%s" % (n, tab), str(g), [str(g + a), str(a * n), str(g - a)], "Kural %d × adım%s. %d. adım: <b>%d</b>." % (a, (" + %d" % b) if b else "", n, g))

    def sekil():
        a, b = ri(2, 4), ri(0, 3)
        counts = [a * n + b for n in range(1, 4)]
        n = ri(8, 20)
        pic = sq_pat(counts)
        g = a * n + b
        return mcq("Şekil örüntüsünde %d. adımda kaç kare olur?%s" % (n, pic), str(g), [str(g + a), str(a * n), str(n + b)],
                   "Kareler %d, %d, %d: her adımda %d artıyor. Kural %d × adım%s. %d. adım: <b>%d</b>." % (counts[0], counts[1], counts[2], a, a, (" + %d" % b) if b else "", n, g))

    def hangi_adim():
        a, b = ri(2, 9), ri(0, 6)
        n = ri(8, 40)
        v = a * n + b
        rule = "%d × adım sayısı%s" % (a, (" + %d" % b) if b else "")
        return mcq("Kuralı “%s” olan örüntüde %s kaçıncı adımdadır?" % (rule, num(v)), "%d. adım" % n, ["%d. adım" % x for x in (n + 1, n - 1, v // a + 1 if v // a != n else n + 2)],
                   "(%s%s) ÷ %d = <b>%d</b>." % (num(v), (" − %d" % b) if b else "", a, n))

    sets = [("Örüntünün kuralı", [(kural_bul, 20)]),
            ("İstenen adım", [(n_terim, 20)]),
            ("Tablo ile örüntü", [(tablo, 20)]),
            ("Şekil örüntüleri", [(sekil, 20)]),
            ("Terimin adımını bulma", [(hangi_adim, 20)])]
    return unit("oruntuler", "C5", "MAT.5.2.3", 18, "Sayı ve Şekil Örüntülerinin Kuralı", "Örüntüler",
                "Sayı ve şekil örüntülerinin kuralına ilişkin akıl yürütür; kuralı sözel ve sembolik olarak ifade eder.",
                "5. sınıf örüntüler çalışma kâğıdı: örüntünün kuralını bulma, 50. ve 100. adımı hesaplama, tablo ile örüntü, şekil örüntüleri ve terimin adımını bulma. 100 soru ve cevap anahtarı.",
                "Kural: artış × adım sayısı ± sabit", "Kuralı bulunca istediğin adımı hesaplarsın.", sets,
                ["Bir örüntüde her adımda aynı miktar artış varsa kural “artış × adım sayısı” ile başlar.",
                 "Sonra 1. adımı kontrol ederiz: 5, 8, 11… örüntüsünde artış 3; 3 × 1 = 3, terim 5 → kural 3 × adım sayısı + 2.",
                 "Kuralı bulunca 50. ya da 100. adımı tek işlemle hesaplarız: 3 × 50 + 2 = 152."],
                [("4, 7, 10, 13 örüntüsünün kuralı", ["Artış 3", "3 × 1 = 3, 4 − 3 = 1"], "3 × adım sayısı + 1"), ("Kural 5 × adım − 2, 20. adım", ["5 × 20 − 2"], "98")],
                [["Kuralı yalnızca “3 artıyor” diye bırakmak", "Uzak adımlar için “3 × adım sayısı + 1” biçiminde yaz"], ["Kuralı tek terimle kontrol etmek", "Birkaç terimde dene"],
                 ["50. adımı 50 × 3 bulmak", "Sabit terimi ekle: 50 × 3 + 1"]],
                [("Örüntünün kuralı neden önemlidir?", "Bütün terimleri yazmadan istediğimiz adımı bulmamızı sağlar."),
                 ("Kural sembolle nasıl yazılır?", "Adım sayısı yerine harf kullanılabilir; bunu 6. sınıfta cebirsel ifadelerle göreceksin."),
                 ("Şekil örüntüsünde kural nasıl bulunur?", "Her adımdaki şekil sayısını tabloya yazıp artışa bakarız.")])


def sq_pat(counts, c=11):
    s = []
    x = 24
    for k, n in enumerate(counts):
        cols = (n + 3) // 4
        for i in range(n):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#a8d5ba' stroke='%s' stroke-width='1.1'/>" % (x + (i // 4) * c, 8 + (i % 4) * c, c, c, GREEN))
        s.append(text(x + cols * c / 2.0, 8 + 4 * c + 18, "%d. adım" % (k + 1), 12))
        x += max(cols * c, 30) + 34
    return G.wrap(x, 8 + 4 * c + 26, "".join(s), "şekil örüntüsü")


# ============================================================ 19. algoritmalar
def code(lines):
    return "<div class='qfig'><span class='code'>%s</span></div>" % "<br>".join(lines)


def u19():
    def adimlar():
        a = ri(2, 30)
        p, q, r = ri(2, 9), ri(2, 20), ri(2, 5)
        v = (a * p + q) * r
        lines = ["1. Bir sayı seç: %d" % a, "2. Sayıyı %d ile çarp." % p, "3. Sonuca %d ekle." % q, "4. Sonucu %d ile çarp." % r, "5. Sonucu yaz."]
        return mcq("Algoritmaya göre yazılan sonuç kaçtır?" + code(lines), num(v), [num(a * p + q * r), num((a + q) * p * r), num(v + r)],
                   "%d × %d = %d → %d + %d = %d → %d × %d = <b>%s</b>." % (a, p, a * p, a * p, q, a * p + q, a * p + q, r, num(v)))

    def ters():
        p, q = ri(2, 9), ri(2, 30)
        a = ri(2, 40)
        v = a * p + q
        lines = ["1. Bir sayı seç.", "2. Sayıyı %d ile çarp." % p, "3. Sonuca %d ekle." % q, "4. Sonucu yaz."]
        return mcq("Algoritma uygulandığında %s yazılıyor. Başlangıçta seçilen sayı kaçtır?%s" % (num(v), code(lines)), str(a), [str(v - q), str((v + q) // p), str(a + 1)],
                   "Geriye doğru: %s − %d = %d, %d ÷ %d = <b>%d</b>." % (num(v), q, v - q, v - q, p, a))

    def birim_fiyat():
        g = ch([100, 200, 250, 500])
        price = ri(4, 40) * (1000 // g)
        unit_p = price * 1000 // g
        lines = ["1. Ürünün gramını ve fiyatını oku: %d g, %s TL" % (g, num(price)), "2. 1.000 ÷ %d işlemini yap." % g, "3. Bulduğun sayıyı fiyatla çarp.", "4. Sonucu 1 kg fiyatı olarak yaz."]
        return mcq("Bir peynirin 1 kg fiyatını bulan algoritma:%sSonuç kaç TL’dir?" % code(lines), "%s TL" % num(unit_p), ["%s TL" % num(x) for x in (price * g // 100, price + 1000 // g, unit_p // 10)],
                   "1.000 ÷ %d = %d, %d × %s = <b>%s TL</b>." % (g, 1000 // g, 1000 // g, num(price), num(unit_p)))

    def dongu():
        a = ri(1, 20)
        p = ri(2, 9)
        n = ri(3, 6)
        v = a + p * n
        lines = ["1. Sayı = %d" % a, "2. %d kez tekrarla:" % n, "&nbsp;&nbsp;&nbsp;Sayıya %d ekle." % p, "3. Sayıyı yaz."]
        return mcq("Algoritmaya göre yazılan sayı kaçtır?" + code(lines), str(v), [str(a + p), str(a * p * n), str(v + p)], "%d kez %d eklenir: %d + %d × %d = <b>%d</b>." % (n, p, a, n, p, v))

    def tablo():
        p, q = ri(2, 9), ri(1, 15)
        xs = sorted(sh(range(1, 12))[:4])
        rows = "".join("<tr><td style='text-align:center'>%d</td><td style='text-align:center'>%s</td></tr>" % (x, num(x * p + q) if i < 3 else "?") for i, x in enumerate(xs))
        tab = "<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr><th>Giriş</th><th>Çıkış</th></tr></thead><tbody>%s</tbody></table>" % rows
        g = xs[3] * p + q
        return mcq("Bir makine her giriş sayısına aynı iki işlemi uyguluyor.%s? yerine hangi sayı gelir?" % tab, str(g), [str(g + p), str(xs[3] * p), str(xs[3] + q)],
                   "Kural: giriş × %d + %d. %d × %d + %d = <b>%d</b>." % (p, q, xs[3], p, q, g))

    def karar():
        n = ri(2, 200)
        lines = ["1. Sayıyı oku: %d" % n, "2. Sayı çift ise sayıyı 2’ye böl.", "3. Sayı tek ise sayıya 1 ekle.", "4. Sonucu yaz."]
        g = n // 2 if n % 2 == 0 else n + 1
        return mcq("Algoritmaya göre yazılan sonuç kaçtır?" + code(lines), str(g), [str(n + 1) if n % 2 == 0 else str(n // 2), str(n * 2), str(n - 1)],
                   "%d %s: <b>%d</b>." % (n, "çift, 2’ye bölünür" if n % 2 == 0 else "tek, 1 eklenir", g))

    sets = [("Adım adım algoritma", [(adimlar, 20)]),
            ("Algoritmayı tersine çalıştırma", [(ters, 20)]),
            ("Günlük hayatta algoritma", [(birim_fiyat, 20)]),
            ("Tekrar ve karar", [(dongu, 10), (karar, 10)]),
            ("Giriş-çıkış tabloları", [(tablo, 20)])]
    return unit("algoritmalar", "C5", "MAT.5.2.4", 19, "Temel Aritmetik İşlemlerde Algoritmalar", "Algoritmalar",
                "Temel aritmetik işlem durumlarındaki algoritmaları yorumlar; algoritmayı tablo gösterimine veya aritmetik işlemlere dönüştürür.",
                "5. sınıf algoritmalar çalışma kâğıdı: adım adım algoritma, algoritmayı tersine çalıştırma, 1 kg fiyatı bulma, tekrar ve karar adımları, giriş-çıkış tabloları. 100 soru ve cevap anahtarı.",
                "Algoritma: sıralı ve açık adımlar", "Adımları sırayla uygula; sırayı değiştirme.", sets,
                ["Algoritma, bir problemi çözmek için sırayla uygulanan açık adımlardır. Her adım bir öncekinin sonucunu kullanır.",
                 "Algoritmayı tersine çalıştırırken son adımdan başlar, her işlemin tersini yaparız: ekleme yerine çıkarma, çarpma yerine bölme.",
                 "Giriş-çıkış tablolarında her girişe aynı kural uygulanır. Kuralı birkaç satırda kontrol ederiz."],
                [("5 → × 3 → + 4", ["5 × 3 = 15", "15 + 4"], "19"), ("Çıkış 31, kural × 4 + 3", ["31 − 3 = 28", "28 ÷ 4"], "7")],
                [["Adımların sırasını değiştirmek", "(5 + 4) × 3 ile 5 × 3 + 4 farklıdır"], ["Tersine çalışırken işlemleri ters çevirmemek", "Ekleme ↔ çıkarma, çarpma ↔ bölme"],
                 ["Kuralı yalnızca bir satırda denemek", "Tablodaki bütün satırlarda kontrol et"]],
                [("Algoritma yalnızca bilgisayarda mı kullanılır?", "Hayır. Yemek tarifi ve bölme işleminin adımları da birer algoritmadır."),
                 ("Tekrar adımı ne işe yarar?", "Aynı işlemi birçok kez yazmadan “… kez tekrarla” diyerek kısaltır."),
                 ("Karar adımı nedir?", "“Sayı çift ise …, tek ise …” gibi duruma göre farklı yol seçen adımdır.")])


# ============================================================ 20. olasılık
def olc(v, kind):
    v = F(v)
    if kind == 0:
        return ff(v) if v not in (0, 1) else str(v)
    if kind == 1:
        return dz(v) if v not in (0, 1) else str(int(v))
    return pc(v)


def u20():
    def deger():
        S = [("imkânsız", F(0)), ("kesin", F(1)), ("eşit şanslı (yarı yarıya)", F(1, 2))]
        ad, v = ch(S)
        k = ri(0, 2)
        g = olc(v, k)
        w = [olc(x, k) for _, x in S if x != v] + [olc(F(1, 4), k), "2" if k < 2 else "%200"]
        return mcq("%s bir olayın olasılığı %s gösterimle hangisidir?" % (cap(ad), ["kesir", "ondalık", "yüzde"][k]), g, w,
                   "İmkânsız olay 0 (%%0), kesin olay 1 (%%100), eşit şanslı olay 1/2 (0,5 ya da %%50): <b>%s</b>." % g)

    def olay():
        S = [("Bir zar atıldığında 7 gelmesi", F(0)), ("Bir zar atıldığında 1’den 6’ya kadar bir sayı gelmesi", F(1)), ("Yazı tura atıldığında tura gelmesi", F(1, 2)),
             ("Bir zar atıldığında çift sayı gelmesi", F(1, 2)), ("Yalnızca kırmızı topların olduğu torbadan kırmızı top çekilmesi", F(1)),
             ("Yalnızca mavi topların olduğu torbadan sarı top çekilmesi", F(0)), ("Pazartesiden sonraki günün salı olması", F(1)), ("Bir haftanın 8 gün olması", F(0)),
             ("Bir zar atıldığında tek sayı gelmesi", F(1, 2)), ("Eşit iki parçalı çarkta kırmızı bölüme gelmesi", F(1, 2))]
        t, v = ch(S)
        k = ri(0, 2)
        return mcq("“%s” olayının olasılığı %s olarak hangisidir?" % (t, ["kesir", "ondalık gösterim", "yüzde"][k]), olc(v, k), [olc(x, k) for x in (F(0), F(1), F(1, 2), F(1, 4)) if x != v],
                   "<b>%s</b>." % olc(v, k))

    def daha():
        a, b = sh(range(1, 9))[:2]
        c1, c2 = sh(["kırmızı", "mavi", "yeşil", "sarı"])[:2]
        g = c1 if a > b else c2
        return mcq("Bir torbada %d %s ve %d %s top var. Bakmadan çekilen topun hangi renkte olma olasılığı daha fazladır?" % (a, c1, b, c2), cap(g), [cap(c2 if g == c1 else c1), "Eşit", "Bilinemez"],
                   "Hangi renkten daha çok top varsa onun olasılığı daha fazladır: <b>%s</b>." % g)

    def az_cok():
        S = [("Yarın güneşin doğuda doğması", "Kesin"), ("Ocak ayında İstanbul’da kar yağması", "Olası"), ("Temmuz ayında Antalya’da kar yağması", "Olasılığı düşük"),
             ("Bir zar atıldığında 6 gelmesi", "Olasılığı düşük"), ("Bir zar atıldığında 6 gelmemesi", "Olasılığı yüksek"), ("Bir zar atıldığında 0 gelmesi", "İmkânsız"),
             ("9 kırmızı, 1 mavi top bulunan torbadan kırmızı top çekilmesi", "Olasılığı yüksek"), ("9 kırmızı, 1 mavi top bulunan torbadan mavi top çekilmesi", "Olasılığı düşük"),
             ("Yazı tura atıldığında yazı gelmesi", "Eşit şanslı"), ("Bir yılın 365 ya da 366 gün olması", "Kesin")]
        t, g = ch(S)
        return mcq("“%s” olayı olasılık ölçeğinde nereye yerleştirilir?" % t, g, [x for x in ["İmkânsız", "Olasılığı düşük", "Eşit şanslı", "Olasılığı yüksek", "Kesin", "Olası"] if x != g],
                   "0 (imkânsız) ile 1 (kesin) arasında düşünürüz: <b>%s</b>." % low(g))

    def cark():
        n = ch([4, 5, 8, 10])
        k = ri(1, n - 1)
        col, other = sh(["kırmızı", "mavi", "yeşil"])[:2]
        v = F(k, n)
        kind = ri(0, 2)
        return mcq("Eş %d bölmeli bir çarkın %d bölmesi %s, diğerleri %s. Çark çevrildiğinde %s gelme olasılığı hangisidir?" % (n, k, col, other, col), olc(v, kind),
                   [olc(1 - v, kind) if v != F(1, 2) else olc(F(1, 4), kind), olc(F(1, n), kind) if k != 1 else olc(F(2, n), kind), olc(F(k, n + 1), 0) if kind == 0 else "1"],
                   "%d bölmeden %d tanesi %s: %s = <b>%s</b>." % (n, k, col, fr(k, n), olc(v, kind)))

    sets = [("0 ile 1 arasında olasılık", [(deger, 9), (cark, 11)]),
            ("Olayların olasılığı", [(olay, 20)]),
            ("Hangisi daha olası?", [(daha, 20)]),
            ("Olasılık ölçeği", [(az_cok, 10), (cark, 10)]),
            ("Çark ve torba", [(cark, 10), (daha, 10)])]
    return unit("olasilik", "VO", "MAT.5.6.1, MAT.5.6.2", 20, "Olasılık: 0 ile 1 Arasında, Daha Az ve Daha Çok Olası", "Olasılık",
                "Olasılığı 0 (imkânsız) ile 1 (kesin) arasında (0 ve 1 dâhil) bir değer olarak yorumlar; olayları daha az olası ve daha çok olası olarak sınıflandırır.",
                "5. sınıf olasılık çalışma kâğıdı: olasılığın 0 ile 1 arasında olması, kesir, ondalık ve yüzde gösterim, olasılık ölçeği, daha az ve daha çok olası olaylar, çark ve torba. 100 soru ve cevap anahtarı.",
                "Olasılık 0 ile 1 arasındadır", "İmkânsız 0, eşit şanslı 1/2, kesin 1.", sets,
                ["Bir olayın olasılığı 0 ile 1 arasında (0 ve 1 dâhil) bir sayıdır. İmkânsız olay 0, kesin olay 1’dir.",
                 "Olasılığı kesir (1/2), ondalık gösterim (0,5) ya da yüzde (%50) olarak yazabiliriz.",
                 "Bir olayın gerçekleşebileceği durumlar ne kadar çoksa olasılığı o kadar yüksektir."],
                [("Yazı tura atılınca yazı", ["2 sonuçtan 1’i"], "1/2 = 0,5 = %50"), ("Zar atılınca 7", ["Zarda 7 yok"], "0")],
                [["Olasılığı 1’den büyük yazmak", "Olasılık en fazla 1 (%100) olur"], ["Az olası olayı imkânsız sanmak", "Olasılığı düşük de olsa olabilir"],
                 ["%50’yi 0,05 yazmak", "%50 = 0,50 = 0,5"]],
                [("Olasılık neden 1’den büyük olamaz?", "Kesin olay 1’dir; hiçbir olay kesinden daha olası olamaz."),
                 ("Eşit şanslı ne demektir?", "İki sonucun gelme olasılığının aynı olmasıdır; yazı ve tura gibi."),
                 ("Olasılığı günlük hayatta nerede kullanırız?", "Hava durumunda (yağış olasılığı %70), oyunlarda ve kararlarımızda.")])


UNITS = [u11, u12, u13, u14, u15, u16, u17, u18, u19, u20]
