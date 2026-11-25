# -*- coding: utf-8 -*-
"""Türkiye 8. sınıf (Maarif Modeli, Ortaokul Matematik 2026): Sayılar ve Nicelikler (1〜6)、Cebirsel Düşünme ve Değişimler (7〜12)。"""
import math
from fractions import Fraction as F
import tr_g as G
from tr_g import unit, num, fr, M, NB
from tr_g7 import sn, par, dq, ondalik, lin, MINUS, gen
from id_smp import kosy as _kosy


def setup(rnd):
    pass


def ri(a, b):
    return G.R.randint(a, b)


def ch(xs):
    return G.R.choice(list(xs))


def sh(xs):
    return G.sh(xs)


def nz(a, b):
    while True:
        x = ri(a, b)
        if x:
            return x


def kosy(lines=(), pts=(), lo=-6, hi=6, label="koordinat düzlemi"):
    return _kosy(lines=lines, pts=pts, lo=lo, hi=hi, label=label)


def pw(a, n):
    """a üssü n gösterimi; negatif ve kesirli taban parantezli"""
    a = F(a)
    base = par(a) if (a < 0 or a.denominator > 1) else sn(a)
    if a.denominator > 1 and a > 0:
        base = "(" + sn(a) + ")"
    return "%s<sup>%s</sup>" % (base, sn(n))


# ============================================================ 1. üslü ifadeler
def u1():
    def deger():
        a = nz(-9, 9)
        n = ri(2, 3) if abs(a) > 5 else ri(2, 4) if abs(a) > 2 else ri(2, 6)
        v = F(a) ** n
        return M("%s ifadesinin değeri kaçtır?" % pw(a, n), sn(v), [sn(-v), sn(a * n), sn(abs(a) ** (n - 1) * (1 if a > 0 else -1))],
                 "%s, %s sayısının %d kez kendisiyle çarpımıdır: <b>%s</b>." % (pw(a, n), sn(a), n, sn(v)))

    def isaret():
        a = ri(2, 6)
        n = ri(2, 5)
        e = "%s%s<sup>%d</sup>" % (MINUS, num(a), n)
        v = -(a ** n)
        return M("%s ifadesinin değeri kaçtır? (Parantez yok.)" % e, sn(v), [sn(a ** n), sn(-a * n), sn(-(a ** (n - 1)))],
                 "Üs yalnızca tabandaki sayıya aittir; eksi işareti dışarıda kalır: %s = %s(%s) = <b>%s</b>." % (e, MINUS, num(a ** n), sn(v)))

    def negatif_us():
        a = nz(-5, 6)
        if abs(a) == 1:
            return None
        n = ri(1, 3)
        v = F(1, a ** n) if a > 0 else F(1, a) ** n
        return M("%s ifadesinin değeri kaçtır?" % pw(a, -n), sn(v), [sn(-v), sn(F(a) ** n), sn(F(-a * n))],
                 "Negatif üs, tabanın çarpmaya göre tersini alır: %s = 1 ÷ %s = <b>%s</b>." % (pw(a, -n), pw(a, n), sn(v)))

    def sifir():
        a = ch([nz(-50, 50), rq()])
        k = ch(["0", "1"])
        if k == "0":
            return M("%s ifadesinin değeri kaçtır?" % pw(a, 0), "1", ["0", sn(a), sn(-1)], "Sıfırdan farklı her sayının 0. kuvveti 1’dir: <b>1</b>.")
        return M("%s ifadesinin değeri kaçtır?" % pw(a, 1), sn(a), ["1", sn(-a), "0"], "Bir sayının 1. kuvveti kendisidir: <b>%s</b>." % sn(a))

    def kesirli():
        a = rq()
        n = ri(2, 3)
        v = a ** n
        return M("%s ifadesinin değeri kaçtır?" % pw(a, n), sn(v), [sn(F(a.numerator ** n, a.denominator)), sn(F(a.numerator * n, a.denominator * n)), sn(-v)],
                 "Pay ve payda ayrı ayrı %d. kuvvete alınır: <b>%s</b>." % (n, sn(v)))

    def kiyas():
        a, b = ri(2, 5), ri(2, 5)
        m, n = ri(2, 5), ri(2, 5)
        x, y = a ** m, b ** n
        if x == y or a == b:
            return None
        s = "&lt;" if x < y else "&gt;"
        return M("%s ☐ %s &nbsp; Kutuya hangi sembol gelir?" % (pw(a, m), pw(b, n)), s, ["&gt;" if s == "&lt;" else "&lt;", "=", "≥"],
                 "%s = %d ve %s = %d: <b>%s %s %s</b>." % (pw(a, m), x, pw(b, n), y, pw(a, m), s, pw(b, n)))

    sets = [("Üslü ifadenin değeri", [(deger, 20)]),
            ("Parantez ve işaret", [(isaret, 10), (deger, 10)]),
            ("Negatif üs", [(negatif_us, 20)]),
            ("Sıfırıncı kuvvet ve kesirler", [(sifir, 6), (kesirli, 14)]),
            ("Karşılaştırma ve karışık", [(kiyas, 10), (negatif_us, 5), (kesirli, 5)])]
    return unit("uslu-ifadeler", "S", "MAT.8.1.1", 1, "Üslü İfadeler: Negatif Taban, Sıfırıncı ve Negatif Kuvvet", "Üslü İfadeler",
                "Üslü ifadelere, özelliklerine ve üslü ifadelerle işlemlere ilişkin çıkarım yapar; varsayımlarını örnek ve temsillerle sınar, önermelerini sözel ve cebirsel olarak ifade eder.",
                "8. sınıf üslü ifadeler çalışma kâğıdı: üslü ifadenin değeri, negatif tabanın kuvveti ve parantez, sıfırıncı kuvvet, negatif üs, kesirlerin kuvveti, karşılaştırma. 100 soru ve cevap anahtarı.",
                "aⁿ: a’nın n kez çarpımı", "a⁰ = 1,  a⁻ⁿ = 1/aⁿ  (a ≠ 0)", sets,
                ["aⁿ ifadesi, a sayısının n kez kendisiyle çarpımıdır: 2⁴ = 2 · 2 · 2 · 2 = 16.",
                 "Negatif tabanın çift kuvveti pozitif, tek kuvveti negatiftir: (−3)² = 9, (−3)³ = −27. Parantez yoksa üs yalnızca sayıya aittir: −3² = −9.",
                 "Sıfırdan farklı her sayının 0. kuvveti 1’dir. Negatif üs çarpmaya göre tersini alır: 2⁻³ = 1/2³ = 1/8."],
                [("(−2)⁵", ["5 tane −2’nin çarpımı", "Tek kuvvet: negatif"], "−32"), ("(2/3)⁻²", ["(3/2)²"], "9/4")],
                [["2⁴’ü 2 · 4 = 8 sanmak", "2⁴ = 2 · 2 · 2 · 2 = 16"],
                 ["−3² ile (−3)²’yi aynı sanmak", "−3² = −9, (−3)² = 9"],
                 ["Negatif üssü negatif sayı yapmak", "2⁻³ = 1/8, −8 değil"]],
                [("0⁰ nedir?", "Tanımsızdır; bu yüzden ‘sıfırdan farklı her sayının 0. kuvveti 1’ deriz."),
                 ("Negatif üs neden ters alır?", "2³, 2², 2¹, 2⁰ dizisinde her adımda 2’ye bölünür: 8, 4, 2, 1; devam edince 1/2, 1/4… olur."),
                 ("Üslü ifadeler nerede kullanılır?", "Çok büyük ve çok küçük sayıları (gezegen uzaklıkları, hücre boyutları) yazmada ve hesaplamada.")])


def rq():
    while True:
        d = ch([2, 3, 4, 5])
        n = nz(-4, 4)
        x = F(n, d)
        if x.denominator > 1:
            return x


# ============================================================ 2. üslü ifadelerle işlemler
def u2():
    def carp():
        a = ch([2, 3, 5, 7, 10])
        m, n = nz(-5, 7), nz(-5, 7)
        g = pw(a, m + n)
        return M("%s · %s işleminin sonucu hangisidir?" % (pw(a, m), pw(a, n)), g, [pw(a, m * n), pw(a * a, m + n), pw(a, m - n) if m != 2 * n else pw(a, m + n + 1)],
                 "Tabanlar aynıysa üsler toplanır: %s + %s = %s → <b>%s</b>." % (sn(m), par(n), sn(m + n), g))

    def bol():
        a = ch([2, 3, 5, 7, 10])
        m, n = nz(-5, 8), nz(-5, 8)
        if m == n:
            return None
        g = pw(a, m - n)
        return M("%s ÷ %s işleminin sonucu hangisidir?" % (pw(a, m), pw(a, n)), g, [pw(a, m + n), pw(a, n - m), pw(a, m * n) if m * n != m - n else pw(a, m - n + 1)],
                 "Tabanlar aynıysa bölmede üsler çıkarılır: %s %s %s = %s → <b>%s</b>." % (sn(m), MINUS, par(n), sn(m - n), g))

    def kuvvet():
        a = ch([2, 3, 5, 10])
        m, n = nz(-4, 5), nz(-3, 4)
        g = pw(a, m * n)
        return M("(%s)<sup>%s</sup> ifadesinin eşiti hangisidir?" % (pw(a, m), sn(n)), g, [pw(a, m + n), pw(a, m - n) if m - n != m * n else pw(a, m * n + 1), pw(a * n, m)],
                 "Kuvvetin kuvvetinde üsler çarpılır: %s · %s = %s → <b>%s</b>." % (sn(m), par(n), sn(m * n), g))

    def ayni_us():
        a, b = ch([(2, 5), (4, 25), (2, 3), (3, 5), (5, 4)])
        n = ri(2, 6)
        g = pw(a * b, n)
        return M("%s · %s ifadesinin eşiti hangisidir?" % (pw(a, n), pw(b, n)), g, [pw(a * b, 2 * n), pw(a + b, n), pw(a * b, n + 1)],
                 "Üsler aynıysa tabanlar çarpılır: (%d · %d)<sup>%d</sup> = <b>%s</b>." % (a, b, n, g))

    def bilinmeyen():
        a = ch([2, 3, 5])
        x = nz(-4, 7)
        k = ri(1, 4)
        rhs = F(a) ** (x + k)
        return M("%s · %s = %s ise x kaçtır?" % ("%d<sup>x</sup>" % a, pw(a, k), sn(rhs)), sn(x), [sn(x + k), sn(-x), sn(x + 1)],
                 "%s = %s yazılır; x + %d = %s → x = <b>%s</b>." % (sn(rhs), pw(a, x + k), k, sn(x + k), sn(x)))

    def sadelestir():
        a = ch([2, 3])
        p, q, r = nz(-4, 6), nz(-4, 6), nz(-3, 5)
        e = p + q - r
        g = pw(a, e)
        return M("%s · %s ÷ %s işleminin sonucu hangisidir?" % (pw(a, p), pw(a, q), pw(a, r)), g, [pw(a, p + q + r), pw(a, p * q - r), pw(a, e + 1)],
                 "%s + %s %s %s = %s → <b>%s</b>." % (sn(p), par(q), MINUS, par(r), sn(e), g))

    sets = [("Çarpma", [(carp, 20)]),
            ("Bölme", [(bol, 20)]),
            ("Kuvvetin kuvveti", [(kuvvet, 20)]),
            ("Aynı üslü çarpım", [(ayni_us, 8), (sadelestir, 12)]),
            ("Bilinmeyen üs ve karışık", [(bilinmeyen, 10), (carp, 5), (bol, 5)])]
    return unit("uslu-ifadelerle-islemler", "S", "MAT.8.1.1", 2, "Üslü İfadelerle Çarpma, Bölme ve Kuvvet Alma", "Üslü İfadelerle İşlemler",
                "Üslü ifadelerin özelliklerine ve üslü ifadelerle işlemlere ilişkin genellemeler yapar; aynı tabanlı ve aynı üslü ifadelerle çarpma, bölme ve kuvvet alma kurallarını kullanır.",
                "8. sınıf üslü ifadelerle işlemler çalışma kâğıdı: aynı tabanlı üslü ifadelerle çarpma ve bölme, kuvvetin kuvveti, aynı üslü ifadelerin çarpımı, bilinmeyen üssü bulma. 100 soru ve cevap anahtarı.",
                "Aynı taban: çarpmada üsler toplanır", "aᵐ · aⁿ = aᵐ⁺ⁿ,  aᵐ ÷ aⁿ = aᵐ⁻ⁿ,  (aᵐ)ⁿ = aᵐⁿ", sets,
                ["Tabanları aynı olan üslü ifadeler çarpılırken üsler toplanır: 2³ · 2⁴ = 2⁷. Bölünürken üsler çıkarılır: 5⁶ ÷ 5² = 5⁴.",
                 "Bir üslü ifadenin kuvveti alınırken üsler çarpılır: (3²)⁴ = 3⁸.",
                 "Üsleri aynı olan ifadeler çarpılırken tabanlar çarpılır: 2⁵ · 5⁵ = 10⁵."],
                [("2⁻³ · 2⁷", ["−3 + 7 = 4"], "2⁴"), ("(5²)⁻³", ["2 · (−3) = −6"], "5⁻⁶")],
                [["Çarpmada üsleri çarpmak", "2³ · 2⁴ = 2⁷, 2¹² değil"],
                 ["Tabanları da toplamak", "Taban aynı kalır"],
                 ["Farklı tabanlarda kuralı kullanmak", "2³ · 3² tek bir üslü ifadeye çevrilemez"]],
                [("Tabanlar farklıysa ne yapılır?", "Önce aynı tabana çevrilebiliyor mu bakılır: 4 = 2², 8 = 2³, 27 = 3³."),
                 ("aᵐ ÷ aⁿ’de m < n ise?", "Üs negatif çıkar: 2³ ÷ 2⁵ = 2⁻² = 1/4."),
                 ("Bu kurallar nereden gelir?", "Üslü ifadeyi çarpım olarak açıp çarpanları sayınca görülür: 2³ · 2² = (2·2·2)(2·2) = 2⁵.")])


# ============================================================ 3. bilimsel gösterim
def u3():
    def yaz():
        a = F(ri(10, 99), 10) if ri(0, 1) else F(ri(100, 999), 100)
        n = ri(3, 12)
        v = a * 10 ** n
        if v.denominator != 1:
            return None
        g = "%s × 10<sup>%d</sup>" % (dq(a), n)
        w = ["%s × 10<sup>%d</sup>" % (dq(a * 10), n - 1), "%s × 10<sup>%d</sup>" % (dq(a), n + 1), "%s × 10<sup>%d</sup>" % (dq(a / 10), n + 1)]
        return M("%s sayısının bilimsel gösterimi hangisidir?" % num(int(v)), g, w,
                 "1 ≤ a &lt; 10 olacak biçimde virgül %d basamak sola kayar: <b>%s</b>." % (n, g))

    def kucuk():
        a = F(ri(10, 99), 10)
        n = ri(2, 8)
        v = a / 10 ** n
        g = "%s × 10<sup>%s</sup>" % (dq(a), sn(-n))
        w = ["%s × 10<sup>%s</sup>" % (dq(a), sn(n)), "%s × 10<sup>%s</sup>" % (dq(a), sn(-n + 1)), "%s × 10<sup>%s</sup>" % (dq(a * 10), sn(-n))]
        return M("%s sayısının bilimsel gösterimi hangisidir?" % ondalik(v), g, w,
                 "Virgül %d basamak sağa kayar; küçük sayılarda üs negatiftir: <b>%s</b>." % (n, g))

    def coz():
        a = F(ri(10, 99), 10)
        n = nz(-6, 7)
        v = a * F(10) ** n
        g = ondalik(v) if n < 0 else num(int(v)) if v.denominator == 1 else ondalik(v)
        w = [ondalik(v * 10) if n < 0 else num(int(v * 10)) if (v * 10).denominator == 1 else ondalik(v * 10), ondalik(v / 10), ondalik(a * F(10) ** -n)]
        return M("%s × 10<sup>%s</sup> sayısının ondalık gösterimi hangisidir?" % (dq(a), sn(n)), g, w, "Virgül %d basamak %s kayar: <b>%s</b>." % (abs(n), "sağa" if n > 0 else "sola", g))

    def kiyas():
        a, b = F(ri(11, 99), 10), F(ri(11, 99), 10)
        m, n = nz(-6, 8), nz(-6, 8)
        x, y = a * F(10) ** m, b * F(10) ** n
        if x == y:
            return None
        s = "&lt;" if x < y else "&gt;"
        return M("%s × 10<sup>%s</sup> ☐ %s × 10<sup>%s</sup> &nbsp; Kutuya hangi sembol gelir?" % (dq(a), sn(m), dq(b), sn(n)), s, ["&gt;" if s == "&lt;" else "&lt;", "=", "≥"],
                 "Önce üslere bakılır; üsler eşitse katsayılar karşılaştırılır: <b>%s</b>." % s)

    def carpim():
        a, b = ri(2, 9), ri(2, 9)
        m, n = nz(-6, 9), nz(-6, 9)
        p = a * b
        e = m + n
        if p >= 10:
            c = F(p, 10)
            e += 1
        else:
            c = F(p)
        g = "%s × 10<sup>%s</sup>" % (dq(c), sn(e))
        w = ["%s × 10<sup>%s</sup>" % (dq(c), sn(m * n)), "%s × 10<sup>%s</sup>" % (num(p), sn(m + n + 1)) if p >= 10 else "%s × 10<sup>%s</sup>" % (dq(c), sn(e + 1)), "%s × 10<sup>%s</sup>" % (dq(c), sn(e - 1))]
        return M("(%d × 10<sup>%s</sup>) · (%d × 10<sup>%s</sup>) işleminin bilimsel gösterimi hangisidir?" % (a, sn(m), b, sn(n)), g, w,
                 "Katsayılar çarpılır (%d), üsler toplanır (%s)%s: <b>%s</b>." % (p, sn(m + n), "; 1 ≤ a &lt; 10 için düzenlenir" if p >= 10 else "", g))

    CT = [("Dünya ile Güneş arasındaki uzaklık yaklaşık %s km’dir.", 150000000), ("Bir insan vücudunda yaklaşık %s hücre bulunur.", 37000000000000),
          ("Işık bir yılda yaklaşık %s km yol alır.", 9460000000000), ("Türkiye’nin yüzölçümü yaklaşık %s km²’dir.", 783000),
          ("Bir kum tanesinin kütlesi yaklaşık %s g’dır.", F(4, 10000)), ("Bir bakterinin boyu yaklaşık %s m’dir.", F(2, 1000000)), ("Bir saç telinin kalınlığı yaklaşık %s m’dir.", F(7, 100000))]

    def hayat():
        t, v = ch(CT)
        v = F(v)
        e = len(str(int(v))) - 1 if v >= 1 else -len(str(v.denominator)) + (len(str(v.numerator)))
        if v >= 1:
            a = v / F(10) ** e
        else:
            e = 0
            a = v
            while a < 1:
                a *= 10
                e -= 1
        g = "%s × 10<sup>%s</sup>" % (dq(a), sn(e))
        shown = num(int(v)) if v >= 1 else ondalik(v)
        w = ["%s × 10<sup>%s</sup>" % (dq(a), sn(e + 1)), "%s × 10<sup>%s</sup>" % (dq(a), sn(-e)), "%s × 10<sup>%s</sup>" % (dq(a * 10), sn(e))]
        return M((t % shown) + " Bu sayının bilimsel gösterimi hangisidir?", g, w, "1 ≤ a &lt; 10 olacak biçimde yazarız: <b>%s</b>." % g)

    sets = [("Büyük sayılar", [(yaz, 20)]),
            ("Küçük sayılar", [(kucuk, 20)]),
            ("Bilimsel gösterimden sayıya", [(coz, 20)]),
            ("Karşılaştırma ve çarpma", [(kiyas, 10), (carpim, 10)]),
            ("Günlük hayattan", [(hayat, 7), (carpim, 7), (kucuk, 6)])]
    return unit("bilimsel-gosterim", "S", "MAT.8.1.1", 3, "Çok Büyük ve Çok Küçük Sayılar: Bilimsel Gösterim", "Bilimsel Gösterim",
                "Üslü ifadelerin özelliklerini 10’un kuvvetleriyle kullanarak çok büyük ve çok küçük sayıları bilimsel gösterimle ifade eder, karşılaştırır ve bu gösterimle işlem yapar.",
                "8. sınıf bilimsel gösterim çalışma kâğıdı: büyük ve küçük sayıları a × 10ⁿ biçiminde yazma, bilimsel gösterimden sayıya geçme, karşılaştırma, çarpma ve günlük hayattan örnekler. 100 soru ve cevap anahtarı.",
                "a × 10ⁿ,  1 ≤ a < 10", "Büyük sayılarda n pozitif, küçük sayılarda n negatiftir.", sets,
                ["Bir sayının a × 10ⁿ (1 ≤ a &lt; 10, n tam sayı) biçiminde yazılmasına bilimsel gösterim denir.",
                 "Büyük sayılarda virgül sola kayar ve üs pozitif olur: 34 000 000 = 3,4 × 10⁷. Küçük sayılarda virgül sağa kayar ve üs negatif olur: 0,0005 = 5 × 10⁻⁴.",
                 "Çarparken katsayılar çarpılır, üsler toplanır; sonuçta katsayı 10 veya daha büyükse yeniden düzenlenir."],
                [("520 000 000", ["Virgül 8 basamak sola"], "5,2 × 10⁸"), ("(4 × 10³) · (5 × 10⁻⁷)", ["20 × 10⁻⁴"], "2 × 10⁻³")],
                [["Katsayıyı 10 veya daha büyük bırakmak", "34 × 10⁶ değil, 3,4 × 10⁷"],
                 ["Küçük sayılarda üssü pozitif yazmak", "0,0005 = 5 × 10⁻⁴"],
                 ["Basamakları yanlış saymak", "Virgülün kaç basamak kaydığını tek tek say"]],
                [("Bilimsel gösterim neden kullanılır?", "Çok büyük ve çok küçük sayılar kısa, okunaklı ve karşılaştırılabilir olur."),
                 ("Hesap makinesi bunu nasıl gösterir?", "Çoğu hesap makinesi 3,4E7 gibi yazar; E, ‘× 10 üssü’ demektir."),
                 ("10’un kuvvetleri ile birim dönüşümleri ilişkili mi?", "Evet. 1 km = 10³ m, 1 mm = 10⁻³ m gibi.")])


# ============================================================ 4. kareköklü ifadeler
def u4():
    def tam():
        n = ri(1, 25)
        k = ch(["√%d" % (n * n), "kenar"])
        if k == "kenar":
            return M("Alanı %d cm² olan karenin bir kenarı kaç cm’dir?" % (n * n), num(n), [num(n * n // 2) if n > 2 else num(n + 2), num(n * 4), num(n + 1)],
                     "Karenin kenarı alanın kareköküdür: √%d = <b>%d</b> cm." % (n * n, n))
        return M("√%d kaçtır?" % (n * n), num(n), [num(n * n // 2) if n > 2 else num(n + 3), num(n + 1), num(n - 1) if n > 1 else num(n + 2)],
                 "%d · %d = %d olduğundan √%d = <b>%d</b>." % (n, n, n * n, n * n, n))

    def arasi():
        n = ri(2, 150)
        r = int(math.isqrt(n))
        if r * r == n:
            return None
        g = "%d ile %d" % (r, r + 1)
        return M("√%d hangi iki ardışık doğal sayı arasındadır?" % n, g, ["%d ile %d" % (r - 1, r), "%d ile %d" % (r + 1, r + 2), "%d ile %d" % (n // 2, n // 2 + 1)],
                 "%d² = %d &lt; %d &lt; %d = %d²: <b>%s</b> arasındadır." % (r, r * r, n, (r + 1) ** 2, r + 1, g))

    def tahmin():
        n = ri(2, 99)
        r = int(math.isqrt(n))
        if r * r == n:
            return None
        cands = [F(r * 10 + d, 10) for d in range(10)]
        best = min(cands, key=lambda x: abs(x * x - n))
        w = [best + F(1, 10), best - F(1, 10), F(n, 2)]
        return M("√%d sayısının onda birler basamağına kadar yaklaşık değeri hangisidir?" % n, dq(best), [dq(x) for x in w],
                 "%s² = %s ile %s² = %s arasında karşılaştırırız; %d’ye en yakın: <b>%s</b>." % (dq(best), dq(best * best), dq(best + F(1, 10)), dq((best + F(1, 10)) ** 2), n, dq(best)))

    def hangisi():
        sq = [k * k for k in range(4, 21)]
        g = ch(sq)
        bad = [x for x in (g + 1, g - 1, g + 2, g - 3, g * 2) if x not in sq and x > 0]
        return G.withopts(M("Hangisi bir tam kare sayıdır?", num(g), [num(x) for x in sh(bad)[:3]], "%d = %d²: <b>%d</b>." % (g, int(math.isqrt(g)), g)), "%s sayıları veriliyor.")

    def iki():
        a, b = ri(1, 12), ri(1, 12)
        op = ch(["+", MINUS])
        v = a + b if op == "+" else a - b
        return M("√%d %s √%d işleminin sonucu kaçtır?" % (a * a, op, b * b), sn(v), [sn(a * a + b * b if op == "+" else a * a - b * b), sn(v + 1), sn(-v) if v else "1"],
                 "√%d = %d ve √%d = %d: %d %s %d = <b>%s</b>." % (a * a, a, b * b, b, a, op, b, sn(v)))

    sets = [("Tam kare sayıların karekökü", [(tam, 20)]),
            ("Hangi iki sayı arasında?", [(arasi, 20)]),
            ("Yaklaşık değer", [(tahmin, 20)]),
            ("Tam kare sayılar", [(hangisi, 10), (iki, 10)]),
            ("Karışık", [(arasi, 7), (tahmin, 7), (tam, 6)])]
    return unit("karekoklu-ifadeler", "S", "MAT.8.1.2", 4, "Kareköklü İfadeler: Tam Kare Sayılar ve Yaklaşık Değer", "Kareköklü İfadeler",
                "Kareköklü ifadelerle ilgili muhakeme yapar; karenin alanı ile kenar uzunluğu arasındaki ilişkiyi belirler, tam kare olmayan bir sayının karekökünün hangi iki doğal sayı arasında olduğunu ve yaklaşık değerini gösterir.",
                "8. sınıf kareköklü ifadeler çalışma kâğıdı: tam kare sayıların karekökü, karenin alanından kenar bulma, karekökün hangi iki doğal sayı arasında olduğu, onda birlik yaklaşık değer. 100 soru ve cevap anahtarı.",
                "√a: karesi a olan pozitif sayı", "√49 = 7, çünkü 7² = 49. √50, 7 ile 8 arasındadır.", sets,
                ["Alanı a birimkare olan karenin bir kenarı √a birimdir. Karesi a olan pozitif sayıya a’nın karekökü denir.",
                 "1, 4, 9, 16, 25… gibi bir doğal sayının karesi olan sayılara tam kare sayılar denir; bunların karekökü doğal sayıdır.",
                 "Tam kare olmayan bir sayının karekökü, iki ardışık doğal sayı arasındadır: 36 &lt; 40 &lt; 49 olduğundan 6 &lt; √40 &lt; 7."],
                [("√40", ["6² = 36, 7² = 49"], "6 ile 7 arasında, yaklaşık 6,3"), ("Alanı 121 cm² olan kare", ["√121"], "11 cm")],
                [["√16’yı 8 sanmak", "Karekök yarısı değildir: 4 · 4 = 16"],
                 ["√9 + √16’yı √25 sanmak", "3 + 4 = 7; kökler toplanmaz"],
                 ["Yaklaşık değeri kontrol etmemek", "Bulduğun sayının karesini al, verilen sayıya yakın mı bak"]],
                [("Negatif bir sayının karekökü var mı?", "Gerçek sayılarda yoktur; hiçbir sayının karesi negatif olmaz."),
                 ("√2 neden tam bulunamaz?", "√2 irrasyonel bir sayıdır; ondalık gösterimi sonsuza kadar devam eder ve tekrar etmez."),
                 ("Karekök nerede kullanılır?", "Karenin kenarını bulmada ve Pisagor bağıntısında.")])


# ============================================================ 5. rasyonel ve irrasyonel
def u5():
    RAT = ["√%d" % (k * k) for k in range(2, 13)] + ["0,<span class='ov'>%d</span>" % d for d in range(1, 10)] + ["%s" % fr(a, b) for a, b in ((3, 7), (5, 9), (2, 3), (7, 11))] + ["−4,25", "1,5", "0,125"]
    IRR = ["√%d" % n for n in (2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15, 17, 18, 20, 24, 30, 50)] + ["π", "1,010010001…", "0,123456789101112…"]

    def hangisi():
        k = ch(["irrasyonel", "rasyonel"])
        good = ch(IRR if k == "irrasyonel" else RAT)
        bad = sh(RAT if k == "irrasyonel" else IRR)[:3]
        return G.withopts(M("Hangisi bir %s sayıdır?" % k, good, bad,
                            "Rasyonel sayılar a/b biçiminde yazılabilir; ondalık gösterimleri sonlu ya da devirlidir. İrrasyonel sayıların ondalık gösterimi sonsuz ve devirsizdir. Cevap: <b>%s</b>." % good), "%s sayıları veriliyor.")

    def kok():
        n = ri(2, 200)
        r = math.isqrt(n)
        ok = r * r == n
        g = "Rasyonel" if ok else "İrrasyonel"
        return M("√%d sayısı rasyonel midir, irrasyonel midir?" % n, g, ["İrrasyonel" if ok else "Rasyonel", "Tam sayı değildir ama rasyoneldir" if not ok else "Hem rasyonel hem irrasyonel", "Gerçek sayı değildir"],
                 ("%d bir tam kare (%d²): √%d = %d <b>rasyoneldir</b>." % (n, r, n, r)) if ok else "%d tam kare değil; √%d’nin ondalık gösterimi devirsiz ve sonsuzdur: <b>irrasyoneldir</b>." % (n, n))

    def ondalik_tur():
        S = [("0,333…", "Rasyonel (devirli: 1/3)"), ("2,5", "Rasyonel (sonlu: 5/2)"), ("1,414213562…", "İrrasyonel (devirsiz: √2)"), ("0,121212…", "Rasyonel (devirli: 12/99)"),
             ("3,14159265…", "İrrasyonel (devirsiz: π)"), ("0,75", "Rasyonel (sonlu: 3/4)"), ("2,236067977…", "İrrasyonel (devirsiz: √5)"), ("0,1666…", "Rasyonel (devirli: 1/6)"),
             ("1,7320508…", "İrrasyonel (devirsiz: √3)"), ("−0,8", "Rasyonel (sonlu: −4/5)")]
        t, g = ch(S)
        kind = g.split(" ")[0]
        w = ["İrrasyonel" if kind == "Rasyonel" else "Rasyonel", "Tam sayı", "Doğal sayı"]
        return M("Ondalık gösterimi %s olan sayı nasıl bir sayıdır?" % t, kind, w, "%s → <b>%s</b>." % (t, g))

    def kume():
        S = [("Her doğal sayı bir rasyonel sayıdır.", "Doğru"), ("Her rasyonel sayı bir tam sayıdır.", "Yanlış"), ("Her irrasyonel sayı bir gerçek sayıdır.", "Doğru"),
             ("Bir sayı hem rasyonel hem irrasyonel olabilir.", "Yanlış"), ("Her tam sayı bir rasyonel sayıdır.", "Doğru"), ("Her gerçek sayı rasyoneldir.", "Yanlış"),
             ("Devirli ondalık gösterimler rasyonel sayıdır.", "Doğru"), ("√9 irrasyonel bir sayıdır.", "Yanlış"), ("π rasyonel bir sayıdır.", "Yanlış"), ("Rasyonel sayılar ile irrasyonel sayılar birlikte gerçek sayıları oluşturur.", "Doğru")]
        t, g = ch(S)
        return M("“%s” ifadesi doğru mu, yanlış mı?" % t, g, ["Yanlış" if g == "Doğru" else "Doğru", "Bazen doğru", "Karar verilemez"],
                 "Doğal sayılar ⊂ tam sayılar ⊂ rasyonel sayılar; rasyonel ve irrasyonel sayılar ayrıktır ve birlikte gerçek sayıları oluşturur. Cevap: <b>%s</b>." % g)

    sets = [("Hangisi irrasyonel?", [(hangisi, 20)]),
            ("Karekökler", [(kok, 20)]),
            ("Ondalık gösterime bakarak", [(ondalik_tur, 8), (hangisi, 12)]),
            ("Sayı kümeleri", [(kume, 8), (kok, 12)]),
            ("Karışık", [(hangisi, 8), (kok, 8), (ondalik_tur, 2), (kume, 2)])]
    return unit("rasyonel-ve-irrasyonel-sayilar", "S", "MAT.8.1.3", 5, "Rasyonel ve İrrasyonel Sayılar", "İrrasyonel Sayılar",
                "Sayıların rasyonel ya da irrasyonel olduğunu değerlendirir; ondalık gösterimleri ölçüt alarak bölme ya da hesap makinesiyle elde eder, karşılaştırır ve yargıda bulunur.",
                "8. sınıf rasyonel ve irrasyonel sayılar çalışma kâğıdı: hangi sayının irrasyonel olduğu, tam kare olmayan sayıların karekökü, ondalık gösterime bakarak sınıflandırma, sayı kümeleri. 100 soru ve cevap anahtarı.",
                "İrrasyonel: sonsuz ve devirsiz ondalık", "√2, √3, π irrasyoneldir; √4 = 2 rasyoneldir.", sets,
                ["Rasyonel sayılar a/b (b ≠ 0) biçiminde yazılabilir; ondalık gösterimleri ya sonludur ya da devirlidir.",
                 "Ondalık gösterimi sonsuz olan ve tekrar etmeyen sayılara irrasyonel sayılar denir: √2 = 1,41421356…, π = 3,14159…",
                 "Tam kare olmayan doğal sayıların karekökleri irrasyoneldir. Rasyonel ve irrasyonel sayılar birlikte gerçek sayıları oluşturur."],
                [("√16 ve √17", ["16 = 4²", "17 tam kare değil"], "√16 rasyonel, √17 irrasyonel"), ("0,<span class='ov'>27</span>", ["Devirli ondalık"], "Rasyonel (27/99 = 3/11)")],
                [["π’yi 3,14 olduğu için rasyonel sanmak", "3,14 yalnızca yaklaşık değerdir"],
                 ["Her kökü irrasyonel sanmak", "√25 = 5 rasyoneldir"],
                 ["Devirli ondalığı irrasyonel sanmak", "Tekrar eden ondalık rasyoneldir"]],
                [("İrrasyonel sayıların kesir hâli var mı?", "Hayır. İki tam sayının bölümü olarak yazılamazlar."),
                 ("Hesap makinesi irrasyonelliği gösterir mi?", "Hayır, ekrana sığan basamakları gösterir; sayının devam ettiğini bilmemiz gerekir."),
                 ("İrrasyonel sayılar sayı doğrusunda var mı?", "Evet. √2, kenarı 1 olan karenin köşegeni ölçülerek sayı doğrusunda işaretlenebilir.")])


# ============================================================ 6. gerçek sayılar ve aralıklar
def u6():
    def arada():
        n = ri(3, 120)
        r = math.isqrt(n)
        if r * r == n:
            return None
        return M("Sayı doğrusunda √%d hangi iki tam sayı arasında yer alır?" % n, "%d ile %d" % (r, r + 1), ["%d ile %d" % (r - 1, r), "%d ile %d" % (r + 1, r + 2), "%d ile %d" % (n // 3, n // 3 + 1)],
                 "%d &lt; %d &lt; %d → <b>%d ile %d</b> arasında." % (r * r, n, (r + 1) ** 2, r, r + 1))

    def sirala():
        a = [("√%d" % n, math.sqrt(n)) for n in sh([2, 3, 5, 7, 10, 15, 20, 30, 40, 50])[:2]]
        b = [(dq(F(x, 10)), x / 10) for x in sh(range(5, 70))[:1]] + [(sn(F(p, q)), p / q) for p, q in [ch([(3, 2), (5, 3), (7, 4), (9, 2), (-5, 2)])]]
        xs = a + b
        if len({round(v, 3) for _, v in xs}) < 4:
            return None
        up = sorted(xs, key=lambda t: t[1])
        g = " &lt; ".join(t[0] for t in up)
        wr = [" &lt; ".join(t[0] for t in sh(xs)) for _ in range(6)]
        wr = [w for w in wr if w != g]
        return M("%s sayılarının küçükten büyüğe sıralanışı hangisidir?" % ", ".join(t[0] for t in sorted(xs, key=lambda t: t[0])), g, wr, "Yaklaşık değerler: %s. Küçükten büyüğe: <b>%s</b>." % (", ".join("%s ≈ %s" % (t[0], dq(F(round(t[1], 2)).limit_denominator(100), 2)) for t in up), g))

    def say():
        lo, hi = ri(-8, 3), ri(4, 12)
        L = ch(["&lt;", "≤"])
        Rr = ch(["&lt;", "≤"])
        n = (hi - lo + 1) - (1 if L == "&lt;" else 0) - (1 if Rr == "&lt;" else 0)
        return M("%s %s x %s %s eşitsizliğini sağlayan kaç tam sayı vardır?" % (sn(lo), L, Rr, sn(hi)), num(n), [num(n + 1), num(n - 1), num(n + 2)],
                 "Uç noktalar %s dâhil. Tam sayılar %s’den %s’e: toplam <b>%d</b>." % ({("&lt;", "&lt;"): "ikisi de değil", ("≤", "≤"): "ikisi de", ("&lt;", "≤"): "yalnızca sağ uç", ("≤", "&lt;"): "yalnızca sol uç"}[(L, Rr)],
                                                                                 sn(lo + (1 if L == "&lt;" else 0)), sn(hi - (1 if Rr == "&lt;" else 0)), n))

    def kok_araligi():
        a, b = ri(1, 6), ri(7, 13)
        lo, hi = a * a, b * b
        n = len([k for k in range(lo, hi + 1) if math.isqrt(k) ** 2 != k])
        cnt = b - a - 1
        return M("%d &lt; √x &lt; %d eşitsizliğini sağlayan kaç tane tam kare olan x doğal sayısı vardır?" % (a, b), num(cnt), [num(cnt + 1), num(cnt + 2), num(b * b - a * a - 1)],
                 "√x bir doğal sayı olmalı ve %d ile %d arasında olmalı: %s. Toplam <b>%d</b>." % (a, b, ", ".join(str(k) for k in range(a + 1, b)), cnt))

    def aralik():
        a, b = ri(-6, 2), ri(3, 9)
        k = ch(["kapalı", "açık", "soldan kapalı"])
        g = {"kapalı": "%s ≤ x ≤ %s", "açık": "%s &lt; x &lt; %s", "soldan kapalı": "%s ≤ x &lt; %s"}[k] % (sn(a), sn(b))
        dots = {"kapalı": (True, True), "açık": (False, False), "soldan kapalı": (True, False)}[k]
        W, H = 420, 64
        X = lambda v: 210 + (v - (a + b) / 2.0) * 28
        s = "<svg viewBox='0 0 %d %d' role='img' aria-label='sayı doğrusunda aralık'><line x1='10' y1='30' x2='410' y2='30' stroke='#333' stroke-width='2'/>" % (W, H)
        for v in range(a - 3, b + 4):
            if 10 < X(v) < 410:
                s += "<line x1='%.0f' y1='24' x2='%.0f' y2='36' stroke='#333'/><text x='%.0f' y='56' font-size='13' text-anchor='middle'>%s</text>" % (X(v), X(v), X(v), sn(v))
        s += "<line x1='%.0f' y1='30' x2='%.0f' y2='30' stroke='#c0392b' stroke-width='5'/>" % (X(a), X(b))
        for v, full in ((a, dots[0]), (b, dots[1])):
            s += "<circle cx='%.0f' cy='30' r='7' fill='%s' stroke='#c0392b' stroke-width='3'/>" % (X(v), "#c0392b" if full else "#fff")
        others = [x for x in ["%s ≤ x ≤ %s", "%s &lt; x &lt; %s", "%s ≤ x &lt; %s", "%s &lt; x ≤ %s"] if x % (sn(a), sn(b)) != g]
        return M("Sayı doğrusunda gösterilen gerçek sayı aralığı hangisidir?<div class='qfig'>%s</div>" % G.lg(s + "</svg>"), g, [o % (sn(a), sn(b)) for o in others],
                 "Dolu yuvarlak uç noktanın aralığa dâhil olduğunu, boş yuvarlak dâhil olmadığını gösterir: <b>%s</b>." % g)

    sets = [("Sayı doğrusunda karekökler", [(arada, 20)]),
            ("Gerçek sayıları sıralama", [(sirala, 20)]),
            ("Sayı aralıkları", [(aralik, 20)]),
            ("Aralıktaki tam sayılar", [(say, 14), (kok_araligi, 6)]),
            ("Karışık", [(arada, 6), (sirala, 7), (say, 7)])]
    return unit("gercek-sayilar-ve-sayi-araliklari", "S", "MAT.8.1.4", 6, "Gerçek Sayılar ve Sayı Aralıkları", "Gerçek Sayılar",
                "Gerçek sayıları ve gerçek sayı aralıklarını sayı doğrusunda yorumlar; doğal sayılardan başlayarak gerçek sayıları inceler, sayı doğrusuna yerleştirir ve aralıklar arasındaki ilişkiyi açıklar.",
                "8. sınıf gerçek sayılar ve sayı aralıkları çalışma kâğıdı: kareköklü sayıları sayı doğrusuna yerleştirme, rasyonel ve irrasyonel sayıları sıralama, açık ve kapalı aralıklar, aralıktaki tam sayıları sayma. 100 soru ve cevap anahtarı.",
                "Gerçek sayılar sayı doğrusunu doldurur", "Dolu yuvarlak dâhil, boş yuvarlak dâhil değil.", sets,
                ["Gerçek sayılar rasyonel ve irrasyonel sayılardan oluşur ve sayı doğrusunun tamamını doldurur.",
                 "Kareköklü bir sayıyı yerleştirmek için tam karelere bakarız: 9 &lt; 11 &lt; 16 olduğundan √11, 3 ile 4 arasındadır.",
                 "−2 ≤ x &lt; 5 gibi bir aralıkta dolu uç dâhil, boş uç dâhil değildir; aradaki tüm gerçek sayılar aralığa aittir."],
                [("√30", ["25 &lt; 30 &lt; 36"], "5 ile 6 arasında"), ("−3 &lt; x ≤ 4 aralığındaki tam sayılar", ["−2, −1, 0, 1, 2, 3, 4"], "7 tane")],
                [["Açık uç noktayı saymak", "x &lt; 4 ise 4 dâhil değil"],
                 ["√x’i x/2 gibi düşünmek", "√50 ≈ 7,1"],
                 ["Negatif sayıları sıralarken yanılmak", "−5/2 = −2,5 en küçüklerdendir"]],
                [("Bir aralıkta kaç gerçek sayı vardır?", "Sonsuz tane; iki gerçek sayı arasında her zaman başka bir gerçek sayı bulunur."),
                 ("Aralıklar nerede kullanılır?", "Sıcaklık, hız ya da yaş sınırı gibi bir değerin hangi sınırlar içinde olduğunu göstermede."),
                 ("√2 sayı doğrusunda nasıl işaretlenir?", "Kenarı 1 olan karenin köşegeni pergelle sayı doğrusuna taşınır.")])


# ============================================================ 7. dik koordinat sistemi
def u7():
    def oku():
        x, y = nz(-5, 5), nz(-5, 5)
        g = "(%s, %s)" % (sn(x), sn(y))
        return M("Koordinat düzlemindeki A noktasının koordinatları hangisidir?" + kosy(pts=[(x, y, "A")]), g,
                 ["(%s, %s)" % (sn(y), sn(x)), "(%s, %s)" % (sn(-x), sn(y)), "(%s, %s)" % (sn(x), sn(-y))],
                 "Önce x (apsis, yatay), sonra y (ordinat, dikey) yazılır: <b>%s</b>." % g)

    def bolge():
        x, y = nz(-9, 9), nz(-9, 9)
        b = {(True, True): "1. bölge", (False, True): "2. bölge", (False, False): "3. bölge", (True, False): "4. bölge"}[(x > 0, y > 0)]
        return M("A(%s, %s) noktası koordinat düzleminin hangi bölgesindedir?" % (sn(x), sn(y)), b, [v for v in ("1. bölge", "2. bölge", "3. bölge", "4. bölge") if v != b],
                 "x %s, y %s: <b>%s</b>." % ("pozitif" if x > 0 else "negatif", "pozitif" if y > 0 else "negatif", b))

    def eksen():
        k = ch(["x", "y"])
        v = nz(-9, 9)
        g = "(%s, 0)" % sn(v) if k == "x" else "(0, %s)" % sn(v)
        w = ["(0, %s)" % sn(v) if k == "x" else "(%s, 0)" % sn(v), "(%s, %s)" % (sn(v), sn(v)), "(%s, 1)" % sn(v) if k == "x" else "(1, %s)" % sn(v)]
        return G.withopts(M("Hangi nokta %s ekseni üzerindedir?" % k, g, w, "%s ekseni üzerindeki noktaların %s bileşeni 0’dır: <b>%s</b>." % (k, "y" if k == "x" else "x", g)), "%s noktaları veriliyor.")

    def uzak():
        x1, y1 = nz(-6, 6), nz(-6, 6)
        k = ch(["yatay", "dikey"])
        d = ri(2, 9)
        if k == "yatay":
            x2, y2 = x1 + d * ch([1, -1]), y1
        else:
            x2, y2 = x1, y1 + d * ch([1, -1])
        return M("A(%s, %s) ile B(%s, %s) noktaları arasındaki uzaklık kaç birimdir?" % (sn(x1), sn(y1), sn(x2), sn(y2)), num(d),
                 [num(abs(x1 + x2) + abs(y1 + y2)) if abs(x1 + x2) + abs(y1 + y2) != d else num(d + 2), num(d + 1), num(abs(x1) + abs(x2) + abs(y1) + abs(y2))],
                 "Noktalar aynı %s doğru üzerinde; farklı koordinatların farkı: <b>%d</b>." % ("yatay" if k == "yatay" else "dikey", d))

    def dortgen():
        x, y = ri(-5, 0), ri(-5, 0)
        w, h = ri(2, 6), ri(2, 6)
        pts = [(x, y), (x + w, y), (x + w, y + h)]
        g = "(%s, %s)" % (sn(x), sn(y + h))
        return M("Bir dikdörtgenin üç köşesi (%s, %s), (%s, %s) ve (%s, %s) noktalarıdır. Dördüncü köşesi hangisidir?" % (sn(x), sn(y), sn(x + w), sn(y), sn(x + w), sn(y + h)), g,
                 ["(%s, %s)" % (sn(x + w), sn(y - h)), "(%s, %s)" % (sn(y + h), sn(x)), "(%s, %s)" % (sn(x - w), sn(y + h))], "Dikdörtgenin karşılıklı kenarları paraleldir: <b>%s</b>; alan %d · %d = %d." % (g, w, h, w * h))

    sets = [("Noktanın koordinatları", [(oku, 20)]),
            ("Bölgeler", [(bolge, 20)]),
            ("Eksenler üzerindeki noktalar", [(eksen, 10), (uzak, 10)]),
            ("Uzaklık ve şekiller", [(uzak, 10), (dortgen, 10)]),
            ("Karışık", [(oku, 7), (bolge, 7), (dortgen, 6)])]
    return unit("dik-koordinat-sistemi", "C8", "MAT.8.2.1", 7, "Dik Koordinat Sistemi", "Koordinat Sistemi",
                "Gerçek yaşam durumlarında dik koordinat sistemini çözümler; düzlem, eksenler ve sayı ikilileri gibi bileşenleri ve aralarındaki ilişkileri belirler.",
                "8. sınıf dik koordinat sistemi çalışma kâğıdı: noktanın koordinatlarını okuma, bölgeler, eksenler üzerindeki noktalar, yatay ve dikey uzaklık, dikdörtgenin eksik köşesi. 100 soru ve cevap anahtarı.",
                "(x, y): önce yatay, sonra dikey", "x eksenine apsis, y eksenine ordinat denir.", sets,
                ["Dik kesişen iki sayı doğrusu (x ve y eksenleri) dik koordinat sistemini oluşturur. Kesiştikleri nokta başlangıç noktasıdır: (0, 0).",
                 "Her nokta bir sıralı ikiliyle gösterilir: (x, y). x yatay konumu (apsis), y dikey konumu (ordinat) verir.",
                 "Eksenler düzlemi dört bölgeye ayırır: 1. bölge (+, +), 2. bölge (−, +), 3. bölge (−, −), 4. bölge (+, −)."],
                [("A noktası 3 birim sola, 2 birim yukarı", ["x = −3, y = 2"], "A(−3, 2), 2. bölge"), ("A(2, −1) ile B(2, 5)", ["Aynı x, dikey uzaklık 5 − (−1)"], "6 birim")],
                [["x ile y’yi yer değiştirmek", "(2, 5) ile (5, 2) farklı noktalardır"],
                 ["Eksen üzerindeki noktayı bir bölgeye koymak", "Eksenler hiçbir bölgeye ait değildir"],
                 ["Uzaklığı koordinatları toplayarak bulmak", "Farkın mutlak değerini al"]],
                [("Koordinat sistemi nerede kullanılır?", "Haritalarda, GPS’te, oyunlarda ve grafik çiziminde."),
                 ("Başlangıç noktası hangi bölgededir?", "Hiçbir bölgede değildir; iki eksenin kesişimidir."),
                 ("Bölgeler neden saat yönünün tersine numaralanır?", "Bu, matematikte açı ölçmedeki yönle uyumlu bir alışkanlıktır.")])


# ============================================================ 8. doğrusal fonksiyonlar
def u8():
    def kural():
        m, b = nz(-5, 6), ri(-9, 9)
        xs = sorted(sh(range(-3, 6))[:4])
        rows = "<table class='sn-table'><tr><th>x</th>%s</tr><tr><th>y</th>%s</tr></table>" % ("".join("<td>%s</td>" % sn(x) for x in xs), "".join("<td>%s</td>" % sn(m * x + b) for x in xs))
        g = "y = " + lin(m, "x", b)
        w = ["y = " + lin(m, "x", -b) if b else "y = " + lin(m, "x", 1), "y = " + lin(m + 1, "x", b - xs[0]) if m + 1 else "y = " + lin(2, "x", b), "y = " + lin(b if b else 2, "x", m)]
        return M("Tablodaki x ve y arasındaki doğrusal ilişkiyi gösteren denklem hangisidir?<div class='qfig'>%s</div>" % rows, g, w,
                 "x 1 artınca y %s değişiyor: eğim %s. x = 0 için y = %s. Kural: <b>%s</b>." % (sn(m), sn(m), sn(b), g))

    def deger():
        m, b = nz(-6, 6), ri(-12, 12)
        x = nz(-6, 6)
        v = m * x + b
        return M("f(x) = %s doğrusal fonksiyonu için f(%s) kaçtır?" % (lin(m, "x", b), sn(x)), sn(v), [sn(m * -x + b), sn(m + x + b), sn(v - b - b) if b else sn(v + 1)],
                 "x yerine %s yazılır: %s · %s %s %s = <b>%s</b>." % (sn(x), sn(m), par(x), "+" if b >= 0 else MINUS, num(abs(b)), sn(v)))

    def ters():
        m, b = nz(-6, 6), ri(-12, 12)
        x = nz(-8, 8)
        v = m * x + b
        return M("f(x) = %s ve f(a) = %s ise a kaçtır?" % (lin(m, "x", b), sn(v)), sn(x), [sn(-x), sn(F(v, m)), sn(x + 1)],
                 "%s = %s → %s = %s → a = <b>%s</b>." % (lin(m, "a", b), sn(v), lin(m, "a"), sn(v - b), sn(x)))

    def degisken():
        S = [("Bir taksinin ücreti gidilen yola bağlıdır.", "Gidilen yol", "Ücret"), ("Bir mumun boyu yandığı süreye bağlıdır.", "Süre", "Mumun boyu"),
             ("Bir depodaki su miktarı musluğun açık kaldığı süreye bağlıdır.", "Süre", "Su miktarı"), ("Ödenen fatura, kullanılan elektrik miktarına bağlıdır.", "Kullanılan elektrik", "Ödenen fatura"),
             ("Bir bitkinin boyu geçen gün sayısına bağlıdır.", "Gün sayısı", "Bitkinin boyu"), ("Alınan defterlerin tutarı defter sayısına bağlıdır.", "Defter sayısı", "Tutar")]
        t, ind, dep = ch(S)
        k = ch(["bağımsız", "bağımlı"])
        g = ind if k == "bağımsız" else dep
        return M("%s Bu durumda %s değişken hangisidir?" % (t, k), g, [dep if g == ind else ind, "İkisi de bağımsızdır", "Değişken yoktur"],
                 "Değeri diğerine bağlı olan bağımlı değişkendir (%s); onu belirleyen bağımsız değişkendir (%s). Cevap: <b>%s</b>." % (dep.lower(), ind.lower(), g))

    def dogrusal_mi():
        m, b = nz(-4, 5), ri(-6, 6)
        xs = [0, 1, 2, 3]
        good = ri(0, 1)
        ys = [m * x + b for x in xs]
        if not good:
            ys = [x * x + b for x in xs] if ri(0, 1) else ys[:2] + [ys[2] + 1, ys[3]]
        rows = "<table class='sn-table'><tr><th>x</th>%s</tr><tr><th>y</th>%s</tr></table>" % ("".join("<td>%d</td>" % x for x in xs), "".join("<td>%s</td>" % sn(y) for y in ys))
        g = "Evet, doğrusaldır" if good else "Hayır, doğrusal değildir"
        return M("Tablodaki ilişki doğrusal mıdır?<div class='qfig'>%s</div>" % rows, g, ["Hayır, doğrusal değildir" if good else "Evet, doğrusaldır", "Yalnızca x pozitifken", "Tablodan anlaşılmaz"],
                 "x eşit adımlarla artarken y’deki değişim %s. %s" % ("hep aynı" if good else "aynı değil", "<b>Doğrusaldır</b>." if good else "<b>Doğrusal değildir</b>."))

    sets = [("Tablodan kural", [(kural, 20)]),
            ("Fonksiyonun değeri", [(deger, 20)]),
            ("Verilen değer için x", [(ters, 20)]),
            ("Bağımlı ve bağımsız değişken", [(degisken, 10), (dogrusal_mi, 10)]),
            ("Karışık", [(kural, 7), (deger, 7), (dogrusal_mi, 6)])]
    return unit("dogrusal-iliskiler-ve-fonksiyonlar", "C8", "MAT.8.2.2", 8, "Doğrusal İlişkiden Doğrusal Fonksiyonlara", "Doğrusal Fonksiyonlar",
                "Doğrusal ilişkileri doğrusal fonksiyonlarla temsil eder; doğrusal fonksiyonların cebirsel, tablo ve grafik temsillerini tanır, temsiller arasında geçiş yaparak modelleme ve problem çözme yapar.",
                "8. sınıf doğrusal fonksiyonlar çalışma kâğıdı: tablodan doğrusal ilişkinin kuralını bulma, f(x) değerini hesaplama, verilen değer için x’i bulma, bağımlı ve bağımsız değişken. 100 soru ve cevap anahtarı.",
                "y = mx + n: eşit adımda eşit değişim", "x 1 artınca y hep m kadar değişiyorsa ilişki doğrusaldır.", sets,
                ["İki değişken arasında, birindeki eşit artışlar diğerinde hep aynı miktarda değişime yol açıyorsa ilişki doğrusaldır.",
                 "Doğrusal fonksiyon f(x) = mx + n biçimindedir. x bağımsız, y = f(x) bağımlı değişkendir.",
                 "Tablodan kural bulurken x 1 arttığında y’nin ne kadar değiştiğine (m) ve x = 0 iken y’nin değerine (n) bakarız."],
                [("x: 0, 1, 2  y: 5, 8, 11", ["Her adımda +3", "x = 0 iken 5"], "y = 3x + 5"), ("f(x) = −2x + 7, f(4)", ["−8 + 7"], "−1")],
                [["Kuralı yalnızca ilk iki sütuna bakarak yazmak", "Tüm sütunlarda kontrol et"],
                 ["f(−3) hesaplarken parantezi unutmak", "−2 · (−3) = 6"],
                 ["Bağımlı ile bağımsız değişkeni karıştırmak", "Diğerine bağlı olan bağımlıdır"]],
                [("Fonksiyon ne demektir?", "Her x değerine tek bir y değeri karşılık getiren kuraldır."),
                 ("Doğrusal fonksiyonun grafiği nasıldır?", "Bir doğrudur; bu yüzden ‘doğrusal’ denir."),
                 ("Günlük hayatta örnek?", "Sabit hızla gidilen yol, sabit fiyatla alınan ürünlerin tutarı.")])


# ============================================================ 9. grafikler
def u9():
    def denklem():
        m, b = nz(-3, 3), ri(-4, 4)
        g = "y = " + lin(m, "x", b)
        w = ["y = " + lin(-m, "x", b), "y = " + lin(m, "x", -b) if b else "y = " + lin(m, "x", 2), "y = " + lin(b if b else 1, "x", m)]
        return M("Grafikteki doğrunun denklemi hangisidir?" + kosy(lines=[(m, b, "#2f6fc4", "")]), g, w,
                 "Doğru y eksenini %s noktasında kesiyor (n = %s); x 1 artınca y %s değişiyor (m = %s): <b>%s</b>." % (sn(b), sn(b), sn(m), sn(m), g))

    def kesim():
        m = nz(-4, 4)
        x0 = nz(-5, 5)
        b = -m * x0
        k = ch(["x", "y"])
        if abs(b) > 30:
            return None
        g = "(%s, 0)" % sn(x0) if k == "x" else "(0, %s)" % sn(b)
        w = ["(0, %s)" % sn(x0), "(%s, 0)" % sn(b), "(%s, 0)" % sn(-x0) if k == "x" else "(0, %s)" % sn(-b)]
        return M("y = %s doğrusu %s eksenini hangi noktada keser?" % (lin(m, "x", b), k), g, [x for x in w if x != g] + ["(0, 0)"],
                 ("y = 0 yazılır: %s = 0 → x = %s." % (lin(m, "x", b), sn(x0)) if k == "x" else "x = 0 yazılır: y = %s." % sn(b)) + " Cevap <b>%s</b>." % g)

    def uzerinde():
        m, b = nz(-4, 4), ri(-6, 6)
        x = nz(-5, 5)
        good = (x, m * x + b)
        bad = [(x, m * x + b + 1), (x + 1, m * x + b - m + 1) if m != 1 else (x + 2, m * x + b), (-x, m * x + b)]
        bad = [p for p in bad if p[1] != m * p[0] + b]
        if len(set(bad)) < 3:
            return None
        return G.withopts(M("Hangi nokta y = %s doğrusunun üzerindedir?" % lin(m, "x", b), "(%s, %s)" % (sn(good[0]), sn(good[1])), ["(%s, %s)" % (sn(p[0]), sn(p[1])) for p in bad],
                            "x = %s için y = %s · %s %s %d = %s: <b>(%s, %s)</b>." % (sn(x), sn(m), par(x), "+" if b >= 0 else MINUS, abs(b), sn(good[1]), sn(good[0]), sn(good[1]))), "%s noktaları veriliyor.")

    def grafik_sec():
        m, b = nz(-3, 3), ri(-4, 4)
        cols = ["#2f6fc4", "#d35400", "#16a085", "#8e44ad"]
        ls = [(m, b), (-m, b), (m, -b if b else 2), (m + (1 if m < 3 else -1), b)]
        if len(set(ls)) < 4:
            return None
        order = sh(range(4))
        names = ["d₁", "d₂", "d₃", "d₄"]
        lines = [(ls[order[i]][0], ls[order[i]][1], cols[i], names[i]) for i in range(4)]
        j = order.index(0)
        return M("y = %s doğrusunun grafiği hangisidir?" % lin(m, "x", b) + kosy(lines=lines), names[j], [n for i, n in enumerate(names) if i != j],
                 "y eksenini %s’te kesen ve eğimi %s olan doğru: <b>%s</b>." % (sn(b), sn(m), names[j]))

    sets = [("Grafikten denklem", [(denklem, 20)]),
            ("Eksenleri kestiği noktalar", [(kesim, 20)]),
            ("Doğru üzerindeki nokta", [(uzerinde, 20)]),
            ("Doğru grafik hangisi?", [(grafik_sec, 20)]),
            ("Karışık", [(denklem, 7), (kesim, 7), (uzerinde, 6)])]
    return unit("dogrusal-fonksiyonlarin-grafikleri", "C8", "MAT.8.2.2", 9, "Doğrusal Fonksiyonların Grafikleri", "Doğrusal Grafikler",
                "Doğrusal fonksiyonların grafik temsilini cebirsel ve tablo temsilleriyle ilişkilendirir; grafiğin eksenleri kestiği noktaları ve grafik üzerindeki noktaları yorumlar.",
                "8. sınıf doğrusal fonksiyonların grafikleri çalışma kâğıdı: grafikten denklem yazma, doğrunun eksenleri kestiği noktalar, bir noktanın doğru üzerinde olup olmadığı, denkleme uygun grafiği seçme. 100 soru ve cevap anahtarı.",
                "y = mx + n: n, y eksenini kestiği yer", "x eksenini kestiği yer için y = 0 yazılır.", sets,
                ["y = mx + n doğrusu y eksenini (0, n) noktasında keser. x eksenini kestiği noktayı bulmak için y = 0 yazarız.",
                 "Bir nokta doğru üzerindeyse koordinatları denklemi sağlar: x’i yerine koyunca aynı y çıkar.",
                 "Grafikten denklem yazmak için önce y eksenini kestiği yeri (n), sonra x 1 artınca y’nin ne kadar değiştiğini (m) okuruz."],
                [("y = 2x − 6", ["x = 0: y = −6", "y = 0: x = 3"], "(0, −6) ve (3, 0)"), ("(2, 1) noktası y = 3x − 5 üzerinde mi?", ["3 · 2 − 5 = 1"], "Evet")],
                [["x eksenini keserken x = 0 yazmak", "x ekseninde y = 0’dır"],
                 ["Eğimin işaretini ters okumak", "Sağa doğru inen doğrunun eğimi negatiftir"],
                 ["Noktayı denkleme yanlış yerleştirmek", "(x, y): önce x"]],
                [("İki nokta bir doğruyu belirler mi?", "Evet. Grafik çizmek için iki noktayı işaretleyip birleştirmek yeter."),
                 ("y = 3 nasıl bir doğrudur?", "x eksenine paralel (yatay) bir doğrudur; eğimi 0’dır."),
                 ("Grafik neden önemlidir?", "Değişimi bir bakışta gösterir: hangi değerde ne olduğunu ve ne kadar hızlı değiştiğini.")])


# ============================================================ 10. eğim
def u10():
    def iki_nokta():
        x1, y1 = nz(-6, 6), nz(-6, 6)
        dx = nz(-5, 5)
        m = F(nz(-6, 6), ch([1, 1, 2, 3]))
        dy = m * dx
        if dy.denominator != 1:
            return None
        x2, y2 = x1 + dx, y1 + int(dy)
        return M("A(%s, %s) ve B(%s, %s) noktalarından geçen doğrunun eğimi kaçtır?" % (sn(x1), sn(y1), sn(x2), sn(y2)), sn(m),
                 [sn(-m), sn(1 / m) if m else "1", sn(m + 1)], "Eğim = (y₂ − y₁) ÷ (x₂ − x₁) = %s ÷ %s = <b>%s</b>." % (sn(y2 - y1), sn(x2 - x1), sn(m)))

    def denklemden():
        a, b = nz(-6, 6), ri(-9, 9)
        k = ch(["y = ", "2y = ", "3y = "])
        c = {"y = ": 1, "2y = ": 2, "3y = ": 3}[k]
        m = F(a, c)
        return M("%s%s doğrusunun eğimi kaçtır?" % (k, lin(a, "x", b)), sn(m), [sn(a), sn(F(b, c)), sn(-m)] if c > 1 else [sn(-m), sn(b), sn(1 / m) if abs(m) != 1 else sn(m + 1)],
                 ("y yalnız bırakılır: y = %s · x + … → eğim <b>%s</b>." % (sn(m), sn(m))) if c > 1 else "y = mx + n biçiminde x’in katsayısı eğimdir: <b>%s</b>." % sn(m))

    def grafikten():
        m = F(nz(-3, 3), ch([1, 2]))
        b = ri(-3, 3)
        if m.denominator == 2 and b % 1:
            return None
        return M("Grafikteki doğrunun eğimi kaçtır?" + kosy(lines=[(m, b, "#2f6fc4", "")], pts=[(0, b, ""), (m.denominator, b + m.numerator, "")]), sn(m),
                 [sn(-m), sn(1 / m), sn(m * 2) if m * 2 != -m else sn(m + 1)], "İşaretli iki noktada x %d artınca y %s değişiyor: eğim %s/%d = <b>%s</b>." % (m.denominator, sn(m.numerator), sn(m.numerator), m.denominator, sn(m)))

    def anlam():
        S = [("Bir musluktan depoya dakikada %d litre su akıyor. Su miktarı–zaman grafiğinin eğimi kaçtır?", "%d L/dk"), ("Bir araç saatte %d km sabit hızla gidiyor. Yol–zaman grafiğinin eğimi kaçtır?", "%d km/sa"),
             ("Bir kitapçıda her defter %d TL. Tutar–defter sayısı grafiğinin eğimi kaçtır?", "%d TL/defter"), ("Bir mum her saat %d cm kısalıyor. Mumun boyu–zaman grafiğinin eğimi kaçtır?", "−%d cm/sa")]
        t, g = ch(S)
        v = ri(2, 90)
        gg = g % v
        alt = [g.replace("−", "") % v if "−" in g else "−" + g % v, "%d" % (v * 2) + gg.split(str(v))[-1], "1/%d" % v + gg.split(str(v))[-1]]
        return M(t % v, gg.replace("−", MINUS), [x.replace("−", MINUS) for x in alt], "Eğim, bağımsız değişken 1 birim artınca bağımlı değişkendeki değişimdir: <b>%s</b>." % gg.replace("−", MINUS))

    def yatay():
        S = [("y = %d", "0"), ("x eksenine paralel bir doğru", "0"), ("Sağa doğru yükselen bir doğru", "Pozitif"), ("Sağa doğru alçalan bir doğru", "Negatif")]
        t, g = ch(S)
        if "%d" in t:
            t = t % nz(-9, 9)
        w = [x for x in ["0", "Pozitif", "Negatif", "Tanımsız"] if x != g]
        return M("%s için eğim nasıldır?" % cap_(t) if "y =" not in t else "%s doğrusunun eğimi kaçtır?" % t, g, w,
                 "Yatay doğruların eğimi 0; sağa yükselenlerin pozitif, sağa alçalanların negatiftir. Cevap: <b>%s</b>." % g)

    sets = [("İki noktadan eğim", [(iki_nokta, 20)]),
            ("Denklemden eğim", [(denklemden, 20)]),
            ("Grafikten eğim", [(grafikten, 20)]),
            ("Eğimin anlamı", [(anlam, 16), (yatay, 4)]),
            ("Karışık", [(iki_nokta, 7), (denklemden, 7), (anlam, 6)])]
    return unit("egim", "C8", "MAT.8.2.2, MAT.8.2.3", 10, "Doğrunun Eğimi", "Eğim",
                "Doğrusal fonksiyonlarda eğimi grafik, tablo ve cebirsel temsillerle ilişkilendirir; eğimin gerçek yaşamdaki anlamını (değişim oranı) yorumlar.",
                "8. sınıf eğim çalışma kâğıdı: iki noktadan geçen doğrunun eğimi, denklemden ve grafikten eğim, yatay doğrular, eğimin günlük hayattaki anlamı (hız, birim fiyat). 100 soru ve cevap anahtarı.",
                "Eğim = dikey değişim ÷ yatay değişim", "y = mx + n’de m eğimdir; değişim oranını gösterir.", sets,
                ["Eğim, doğru üzerinde x 1 birim artınca y’nin ne kadar değiştiğidir: m = (y₂ − y₁) ÷ (x₂ − x₁).",
                 "y = mx + n denkleminde x’in katsayısı m eğimdir. Eğim pozitifse doğru sağa doğru yükselir, negatifse alçalır, 0 ise yataydır.",
                 "Gerçek yaşamda eğim bir değişim oranıdır: hız (km/sa), birim fiyat (TL/adet), akış hızı (L/dk)."],
                [("A(1, 2), B(4, 11)", ["(11 − 2) ÷ (4 − 1)"], "3"), ("2y = 6x − 4", ["y = 3x − 2"], "Eğim 3")],
                [["Farkları farklı sırayla almak", "İkisinde de aynı noktadan başla: y₂ − y₁ ve x₂ − x₁"],
                 ["2y = 6x − 4’te eğimi 6 sanmak", "Önce y’yi yalnız bırak: y = 3x − 2"],
                 ["Yatay doğrunun eğimini tanımsız sanmak", "Yatay: 0; dikey doğru: tanımsız"]],
                [("Eğim neden önemli?", "Bir niceliğin diğerine göre ne kadar hızlı değiştiğini gösterir."),
                 ("Dikey doğrunun eğimi var mı?", "Yoktur (tanımsızdır), çünkü x değişmez ve sıfıra bölme gerekir."),
                 ("Yolların eğimi ile aynı şey mi?", "Evet. %10 eğim, 100 m yatayda 10 m yükselmek demektir.")])


def cap_(s):
    return G.cap(s)


# ============================================================ 11. iki doğrunun durumu
def u11():
    def durum():
        m1, b1 = nz(-4, 4), ri(-6, 6)
        k = ch(["paralel", "kesişen", "çakışık"])
        if k == "paralel":
            m2, b2 = m1, b1 + nz(-4, 4)
        elif k == "kesişen":
            m2, b2 = m1 + nz(-3, 3), ri(-6, 6)
        else:
            m2, b2 = m1, b1
        c = ch([1, 2])
        e2 = ("%sy = %s" % ("" if c == 1 else "2", lin(m2 * c, "x", b2 * c)))
        g = {"paralel": "Paraleldir", "kesişen": "Bir noktada kesişir", "çakışık": "Çakışıktır (aynı doğru)"}[k]
        return M("y = %s ve %s doğruları için hangisi doğrudur?" % (lin(m1, "x", b1), e2), g, [v for v in ("Paraleldir", "Bir noktada kesişir", "Çakışıktır (aynı doğru)", "Diktir ve kesişmez") if v != g],
                 "Eğimler %s ve %s; y eksenini kesim noktaları %s ve %s. %s" % (sn(m1), sn(m2), sn(b1), sn(b2), {"paralel": "Eğimler eşit, kesim noktaları farklı: <b>paralel</b>.", "kesişen": "Eğimler farklı: <b>bir noktada kesişir</b>.", "çakışık": "Eğimler ve kesim noktaları aynı: <b>çakışık</b>."}[k]))

    def kesisim():
        x, y = nz(-5, 5), nz(-6, 6)
        m1, m2 = nz(-4, 4), nz(-4, 4)
        if m1 == m2:
            return None
        b1, b2 = y - m1 * x, y - m2 * x
        g = "(%s, %s)" % (sn(x), sn(y))
        return M("y = %s ve y = %s doğrularının kesişim noktası hangisidir?" % (lin(m1, "x", b1), lin(m2, "x", b2)), g,
                 ["(%s, %s)" % (sn(y), sn(x)), "(%s, %s)" % (sn(-x), sn(y)), "(%s, %s)" % (sn(x), sn(m1 * x + b2))],
                 "İki ifadeyi eşitleriz: %s = %s → x = %s; y = %s: <b>%s</b>." % (lin(m1, "x", b1), lin(m2, "x", b2), sn(x), sn(y), g))

    def paralel_bul():
        m, b = nz(-5, 5), ri(-8, 8)
        c = ri(-8, 8)
        if c == b:
            return None
        g = "y = " + lin(m, "x", c)
        return G.withopts(M("Hangi doğru y = %s doğrusuna paraleldir?" % lin(m, "x", b), g, ["y = " + lin(-m, "x", c), "y = " + lin(m + 1, "x", b), "y = " + lin(c if c else 2, "x", m)],
                            "Paralel doğruların eğimleri eşittir (%s), y eksenini kesim noktaları farklıdır: <b>%s</b>." % (sn(m), g)), "%s doğruları veriliyor.")

    def grafik():
        x, y = nz(-4, 4), nz(-4, 4)
        m1, m2 = nz(-2, 2), nz(-2, 2)
        if m1 == m2:
            return None
        b1, b2 = y - m1 * x, y - m2 * x
        if abs(b1) > 6 or abs(b2) > 6:
            return None
        g = "(%s, %s)" % (sn(x), sn(y))
        return M("Grafikteki iki doğrunun kesişim noktası hangisidir?" + kosy(lines=[(m1, b1, "#2f6fc4", "d₁"), (m2, b2, "#d35400", "d₂")]), g,
                 ["(%s, %s)" % (sn(y), sn(x)), "(%s, %s)" % (sn(x + 1), sn(y)), "(%s, %s)" % (sn(x), sn(y - 1))], "Doğruların ortak noktası: <b>%s</b>." % g)

    def m_bul():
        m = nz(-5, 5)
        a = nz(-4, 4)
        k = m - a
        if k == 0:
            return None
        return M("y = %s ve y = (%s)x + 3 doğruları paralel ise k kaçtır?" % (lin(m, "x", ri(-5, 5) or 1), lin(1, "k", a)), sn(k), [sn(m), sn(-k), sn(m + a)],
                 "Paralel doğruların eğimleri eşittir: k %s %d = %s → k = <b>%s</b>." % ("+" if a > 0 else MINUS, abs(a), sn(m), sn(k)))

    sets = [("İki doğrunun durumu", [(durum, 20)]),
            ("Kesişim noktası", [(kesisim, 20)]),
            ("Grafikte kesişim", [(grafik, 20)]),
            ("Paralel doğrular", [(paralel_bul, 12), (m_bul, 8)]),
            ("Karışık", [(durum, 7), (kesisim, 7), (m_bul, 6)])]
    return unit("iki-dogrusal-fonksiyonun-durumu", "C8", "MAT.8.2.3", 11, "İki Doğrusal Fonksiyonun Birbirine Göre Durumu", "İki Doğrunun Durumu",
                "İki doğrusal fonksiyonun birbirine göre durumu hakkında çıkarım yapar; farklı doğrusal fonksiyonları inceleyerek eğim ve kesişim noktalarına göre paralel, kesişen ve çakışık doğrular için genelleme yapar.",
                "8. sınıf iki doğrunun birbirine göre durumu çalışma kâğıdı: paralel, kesişen ve çakışık doğrular, iki doğrunun kesişim noktasını cebirle ve grafikte bulma, paralellik koşulu. 100 soru ve cevap anahtarı.",
                "Eğimler eşit → paralel", "Eğimler farklı → kesişir; her şey aynı → çakışık.", sets,
                ["Eğimleri eşit, y eksenini kestiği noktaları farklı olan doğrular paraleldir; hiç kesişmezler.",
                 "Eğimleri farklı olan iki doğru tek bir noktada kesişir. Kesişim noktasını bulmak için iki ifadeyi eşitleriz.",
                 "Eğimleri ve y eksenini kestiği noktaları aynı olan doğrular çakışıktır; aynı doğrudur."],
                [("y = 2x + 1 ve y = 2x − 3", ["Eğimler 2 ve 2", "Kesim noktaları farklı"], "Paralel"), ("y = x + 2 ve y = −x + 6", ["x + 2 = −x + 6", "x = 2, y = 4"], "(2, 4)")],
                [["2y = 4x + 2 ile y = 2x + 1’i farklı sanmak", "Sadeleştirince aynı doğru: çakışık"],
                 ["Kesişim noktasında yalnızca x’i yazmak", "y’yi de bul: (x, y)"],
                 ["Paralel için y kesim noktasının da eşit olması gerektiğini düşünmek", "Eşitse çakışık olur"]],
                [("İki paralel doğru arasında uzaklık değişir mi?", "Hayır, paralel doğrular arasındaki uzaklık her yerde aynıdır."),
                 ("Kesişim noktası ne anlama gelir?", "İki durumun eşit olduğu anı gösterir: örneğin iki tarifenin aynı ücreti verdiği dakika."),
                 ("Doğrular dik olabilir mi?", "Evet, ama diklik koşulu bu sınıfın konusu değildir; kesişen doğruların özel bir durumudur.")])


# ============================================================ 12. doğrusal fonksiyon problemleri ve algoritma
def u12():
    def taksi():
        a, p = ri(3, 8) * 10, ri(15, 40)
        km = ri(3, 25)
        return M("Bir taksinin açılış ücreti %d TL, kilometre başına ücreti %d TL’dir. %d km yol giden bir yolcu kaç TL öder?" % (a, p, km), "%s TL" % num(a + p * km),
                 ["%s TL" % num((a + p) * km), "%s TL" % num(p * km), "%s TL" % num(a * km + p)], "Ücret = %d + %d · x; x = %d için %d + %d = <b>%s TL</b>." % (a, p, km, a, p * km, num(a + p * km)))

    def tarife():
        a1, p1 = ri(0, 5) * 20, ri(3, 8)
        a2, p2 = a1 + ri(2, 8) * 20, p1 - ri(1, 3)
        if p2 <= 0 or (a2 - a1) % (p1 - p2):
            return None
        x = (a2 - a1) // (p1 - p2)
        return M("A tarifesi: %d TL sabit + dakikası %d TL. B tarifesi: %d TL sabit + dakikası %d TL. Kaç dakikalık konuşmada iki tarife aynı ücreti verir?" % (a1, p1, a2, p2), num(x),
                 [num(x + 5), num((a2 - a1) // p1) if (a2 - a1) // p1 != x else num(x + 2), num(x * 2)], "%d + %dx = %d + %dx → %dx = %d → x = <b>%d</b>." % (a1, p1, a2, p2, p1 - p2, a2 - a1, x))

    def depo():
        V, r = ri(20, 80) * 10, ri(5, 20)
        t = ri(2, V // r - 1)
        return M("İçinde %d L su olan bir depodan dakikada %d L su boşaltılıyor. %d dakika sonra depoda kaç litre su kalır?" % (V, r, t), "%s L" % num(V - r * t),
                 ["%s L" % num(V + r * t), "%s L" % num(r * t), "%s L" % num(V - r - t)], "Su = %d − %d · t; t = %d için <b>%s L</b>." % (V, r, t, num(V - r * t)))

    def kural():
        a, p = ri(2, 8) * 10, ri(5, 30)
        nm = ch(["Bir spor salonu", "Bir yüzme havuzu", "Bir kütüphane"])
        g = "y = %dx + %d" % (p, a)
        return M("%s %d TL üyelik ücreti ve her giriş için %d TL alıyor. x giriş sayısı, y toplam ücret ise doğrusal fonksiyon hangisidir?" % (nm, a, p), g,
                 ["y = %dx + %d" % (a, p), "y = %dx" % (a + p), "y = %dx − %d" % (p, a)], "Sabit ücret n = %d, giriş başına artış m = %d: <b>%s</b>." % (a, p, g))

    def algoritma():
        m, b = nz(-5, 6), ri(-9, 9)
        x = nz(-6, 6)
        L = ["1. Başla", "2. x değerini al (x = %s)" % sn(x), "3. x’i %s ile çarp" % sn(m), "4. Sonuca %s ekle" % par(b), "5. Sonucu y olarak yaz", "6. Bitir"]
        v = m * x + b
        return M("Algoritma hangi doğrusal fonksiyonu hesaplar ve çıktısı nedir?<div class='qfig'><span class='code'>%s</span></div>" % "<br>".join(L),
                 "y = %s; y = %s" % (lin(m, "x", b), sn(v)), ["y = %s; y = %s" % (lin(b if b else 1, "x", m), sn((b if b else 1) * x + m)), "y = %s; y = %s" % (lin(m, "x", -b) if b else lin(m, "x", 1), sn(m * x - b) if b else sn(m * x + 1)),
                                                             "y = %s; y = %s" % (lin(m, "x", b), sn(v + m))],
                 "Adımlar y = %s fonksiyonunu verir; x = %s için <b>y = %s</b>." % (lin(m, "x", b), sn(x), sn(v)))

    sets = [("Taksi ve ücret", [(taksi, 20)]),
            ("Tarifeleri karşılaştırma", [(tarife, 20)]),
            ("Azalan nicelikler", [(depo, 20)]),
            ("Fonksiyonu yazma", [(kural, 12), (algoritma, 8)]),
            ("Karışık", [(algoritma, 8), (taksi, 6), (depo, 6)])]
    return unit("dogrusal-fonksiyon-problemleri-ve-algoritma", "C8", "MAT.8.2.2, MAT.8.2.4", 12, "Doğrusal Fonksiyon Problemleri ve Algoritma", "Doğrusal Fonksiyon Problemleri",
                "Doğrusal fonksiyon içeren gerçek yaşam problemlerini modeller ve çözer; çözüm adımlarını ve aralarındaki ilişkileri algoritma ifade yöntemleriyle yapılandırır.",
                "8. sınıf doğrusal fonksiyon problemleri çalışma kâğıdı: taksi ve abonelik ücretleri, iki tarifenin eşit olduğu an, boşalan depo, problem durumundan fonksiyon yazma, algoritma ile fonksiyon. 100 soru ve cevap anahtarı.",
                "Sabit kısım + değişen kısım", "Ücret = açılış + birim ücret · miktar → y = mx + n", sets,
                ["Gerçek yaşamdaki birçok durum y = mx + n ile modellenir: n başlangıçtaki (sabit) değer, m her birim için değişimdir.",
                 "İki tarifenin aynı ücreti verdiği anı bulmak için iki fonksiyonu eşitleriz; bu, grafiklerin kesişim noktasıdır.",
                 "Azalan durumlarda (boşalan depo, yanan mum) eğim negatiftir: y = başlangıç − hız · zaman."],
                [("Açılış 40 TL, km başına 25 TL, 12 km", ["40 + 25 · 12"], "340 TL"), ("A: 20 + 6x, B: 60 + 4x", ["20 + 6x = 60 + 4x", "2x = 40"], "20 dakika")],
                [["Sabit ücreti her birimle çarpmak", "Açılış ücreti bir kez eklenir"],
                 ["Azalan durumda eğimi pozitif almak", "Boşalma: −r · t"],
                 ["Kesişimden sonra hangi tarifenin ucuz olduğunu karıştırmak", "Birim ücreti düşük olan uzun vadede ucuzdur"]],
                [("Hangi tarife daha uygun, nasıl anlarım?", "Kesişim noktasından önce ve sonra birer değer deneyip ücretleri karşılaştır."),
                 ("Modelin her zaman doğru olduğunu söyleyebilir miyiz?", "Hayır; depo boşalınca su eksiye düşmez. Model yalnızca anlamlı aralıkta geçerlidir."),
                 ("Algoritma burada ne işe yarar?", "Aynı hesaplamayı her x için adım adım ve hatasız yapmayı sağlar.")])


UNITS = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12]
