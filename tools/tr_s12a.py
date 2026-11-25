# -*- coding: utf-8 -*-
"""Türkiye 12. sınıf (2026 DÖP)：MAT.12.1 diziler ve polinomlar、MAT.12.2 çember ve daire。"""
import math
from fractions import Fraction as F
from tr_lise import M, num, sn, par, lin, dq, MINUS, ri, ch, sh, nz, kurve, figure, frs, U, W3, rts, rt, poly, peval

SUBN = str.maketrans("0123456789n", "₀₁₂₃₄₅₆₇₈₉ₙ")


def setup(rnd):
    pass


def a_(i):
    return "a" + str(i).translate(SUBN)


def pis(fr):
    fr = F(fr)
    if fr == 0:
        return "0"
    s = MINUS if fr < 0 else ""
    a = abs(fr)
    top = ("" if a.numerator == 1 else num(a.numerator)) + "π"
    return s + (top if a.denominator == 1 else frs(top, a.denominator))


def fct(r):
    return "x" if r == 0 else "(%s)" % lin(1, "x", -r)


def pmul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            r[i + j] += x * y
    return r


def pdiv(p, d):
    """p ÷ d (d monik ya da değil) → (bölüm, kalan)"""
    p = [F(x) for x in p]
    q = []
    while len(p) >= len(d):
        c = p[0] / d[0]
        q.append(c)
        for i in range(len(d)):
            p[i] -= c * d[i]
        p.pop(0)
    return q, p


# ============================================================ 1. aritmetik diziler
def u1():
    def terim():
        a1, d = ri(-20, 20), nz(-9, 9)
        n = ri(5, 40)
        v = a1 + (n - 1) * d
        return M("İlk terimi %s ve ortak farkı %s olan aritmetik dizinin %d. terimi kaçtır?" % (sn(a1), sn(d), n), sn(v), W3([sn(a1 + n * d), sn(a1 + (n - 2) * d), sn(n * d), sn(a1 * n)], sn(v)),
                 "%s = %s + (n − 1)d = %s + %d · %s = <b>%s</b>." % (a_("n"), a_(1), sn(a1), n - 1, par(d), sn(v)))

    def iki():
        a1, d = ri(-15, 15), nz(-8, 8)
        p, q = sorted(sh(list(range(2, 15)))[:2])
        r = ri(q + 1, 30)
        ap, aq, ar = a1 + (p - 1) * d, a1 + (q - 1) * d, a1 + (r - 1) * d
        return M("Bir aritmetik dizide %s = %s ve %s = %s ise %s kaçtır?" % (a_(p), sn(ap), a_(q), sn(aq), a_(r)), sn(ar), W3([sn(ar + d), sn(ar - d), sn(a1 + r * d + 1), sn(aq + (r - q))], sn(ar)),
                 "d = (%s − %s) ÷ %d = %s; %s = %s + %d · %s = <b>%s</b>." % (sn(aq), par(ap), q - p, sn(d), a_(r), sn(aq), r - q, par(d), sn(ar)))

    def toplam():
        a1, d = ri(-10, 20), nz(-5, 6)
        n = ri(5, 30)
        S = n * (2 * a1 + (n - 1) * d) // 2
        return M("İlk terimi %s ve ortak farkı %s olan aritmetik dizinin ilk %d teriminin toplamı kaçtır?" % (sn(a1), sn(d), n), sn(S), W3([sn(n * (a1 + (n - 1) * d)), sn(S + d * n), sn(a1 + (n - 1) * d), sn(n * (2 * a1 + n * d) // 2)], sn(S)),
                 "Sₙ = n(a₁ + aₙ) ÷ 2 = %d · (%s + %s) ÷ 2 = <b>%s</b>." % (n, sn(a1), par(a1 + (n - 1) * d), sn(S)))

    def ardisik():
        n = ri(10, 100)
        k = ch(["tek", "çift", "doğal"])
        if k == "doğal":
            v = n * (n + 1) // 2
            q = "1 + 2 + 3 + … + %d toplamı kaçtır?" % n
        elif k == "çift":
            v = n * (n + 1)
            q = "2 + 4 + 6 + … + %d toplamı kaçtır?" % (2 * n)
        else:
            v = n * n
            q = "1 + 3 + 5 + … + %d toplamı kaçtır?" % (2 * n - 1)
        return M(q, num(v), W3([num(v + n), num(v - n), num(n * n + n) if k != "çift" else num(n * n), num(v * 2)], num(v)), "Terim sayısı %d; toplam (ilk + son) · n ÷ 2 = <b>%s</b>." % (n, num(v)))

    def problem():
        a1, d = ri(5, 50) * 10, ri(1, 20) * 10
        n = ri(4, 12)
        k = ri(0, 1)
        if k == 0:
            v = a1 + (n - 1) * d
            return M("Bir öğrenci ilk hafta %s sayfa kitap okuyor ve her hafta bir önceki haftadan %d sayfa fazla okuyor. %d. hafta kaç sayfa okur?" % (num(a1), d, n), num(v), W3([num(a1 + n * d), num(a1 + (n - 2) * d), num(n * d), num(v * 2)], num(v)),
                     "Aritmetik dizi: %s + %d · %d = <b>%s</b>." % (num(a1), n - 1, d, num(v)))
        S = n * (2 * a1 + (n - 1) * d) // 2
        return M("Bir koşucu ilk gün %s m koşuyor ve her gün bir önceki günden %d m fazla koşuyor. İlk %d günde toplam kaç m koşar?" % (num(a1), d, n), num(S), W3([num(a1 + (n - 1) * d), num(n * a1), num(S + a1), num(n * (a1 + n * d))], num(S)),
                 "Sₙ = %d · (%s + %s) ÷ 2 = <b>%s</b>." % (n, num(a1), num(a1 + (n - 1) * d), num(S)))

    sets = [("Genel terim", [(terim, 20)]), ("İki terimden dizi", [(iki, 20)]), ("İlk n terimin toplamı", [(toplam, 20)]),
            ("Ardışık sayıların toplamı", [(ardisik, 20)]), ("Problemler", [(problem, 20)])]
    return U(12, "aritmetik-diziler", "N", "MAT.12.1.1", 1, "Aritmetik Diziler ve Toplamları", "Aritmetik Diziler",
             "Aritmetik dizilerin genel terimini ve ilk n teriminin toplamını bulur; gerçek yaşam durumlarını aritmetik dizilerle modeller.",
             "genel terim, iki terimi verilen dizi, ilk n terimin toplamı, ardışık sayıların toplamı, aritmetik dizi problemleri",
             "aₙ = a₁ + (n − 1)d", "Sₙ = n(a₁ + aₙ) ÷ 2.", sets,
             ["Ardışık terimleri arasındaki fark sabit olan diziye aritmetik dizi, bu farka ortak fark (d) denir.",
              "Genel terim aₙ = a₁ + (n − 1)d’dir; iki terim biliniyorsa d = (aₚ − a_q) ÷ (p − q) bulunur.",
              "İlk n terimin toplamı Sₙ = n(a₁ + aₙ) ÷ 2’dir."],
             [("a₁ = 3, d = 4, a₁₀", ["3 + 9 · 4"], "39"), ("1 + 2 + … + 100", ["100 · 101 ÷ 2"], "5.050")],
             [["aₙ = a₁ + nd yazmak", "(n − 1) kez d eklenir"], ["Toplamda 2’ye bölmeyi unutmak", "Ortalama × terim sayısı"], ["Terim sayısını yanlış saymak", "Son − ilk ÷ d + 1"]],
             [("Gauss hikâyesi nedir?", "1’den 100’e kadar toplamı uçları eşleştirerek 5.050 bulduğu anlatılır."), ("Aritmetik dizi doğrusal fonksiyon mudur?", "Evet; aₙ, n’nin doğrusal bir fonksiyonudur."),
              ("Nerede görülür?", "Düzenli artan maaş, taksit ve tasarruf planlarında.")])


# ============================================================ 2. geometrik diziler
def u2():
    def terim():
        a1, r = nz(-6, 6), ch([2, 3, -2, -3, F(1, 2), 4, 5])
        n = ri(3, 8)
        v = a1 * F(r) ** (n - 1)
        if abs(v) > 10 ** 6:
            return None
        return M("İlk terimi %s ve ortak çarpanı %s olan geometrik dizinin %d. terimi kaçtır?" % (sn(a1), sn(r), n), sn(v), W3([sn(a1 * F(r) ** n), sn(a1 * F(r) ** (n - 2)), sn(a1 * F(r) * (n - 1)), sn(-v)], sn(v)),
                 "aₙ = a₁ · rⁿ⁻¹ = %s · %s<sup>%d</sup> = <b>%s</b>." % (sn(a1), par(r) if F(r) < 0 or F(r).denominator > 1 else sn(r), n - 1, sn(v)))

    def r_bul():
        a1, r = nz(-5, 5), ch([2, 3, 4, -2, -3, 5])
        p = ri(1, 4)
        k = ch([1, 2])
        ap, aq = a1 * r ** (p - 1), a1 * r ** (p - 1 + k)
        if k == 2 and r < 0:
            return None
        return M("Bir geometrik dizide %s = %s ve %s = %s ise ortak çarpan%s kaçtır?" % (a_(p), sn(ap), a_(p + k), sn(aq), "" if k == 1 else " (pozitif)"), sn(r if k == 1 else abs(r)),
                 W3([sn(aq - ap), sn(F(aq, ap) if k == 2 else -r), sn(r * 2), sn(-r)], sn(r if k == 1 else abs(r))), "r<sup>%d</sup> = %s ÷ %s = %s → r = <b>%s</b>." % (k, sn(aq), par(ap), sn(F(aq, ap)), sn(r if k == 1 else abs(r))))

    def toplam():
        a1, r = ri(1, 5), ch([2, 3])
        n = ri(3, 8)
        S = a1 * (r ** n - 1) // (r - 1)
        return M("İlk terimi %d ve ortak çarpanı %d olan geometrik dizinin ilk %d teriminin toplamı kaçtır?" % (a1, r, n), num(S), W3([num(a1 * r ** (n - 1)), num(a1 * r ** n), num(S + a1 * r ** n), num(S - a1)], num(S)),
                 "Sₙ = a₁(rⁿ − 1) ÷ (r − 1) = %d(%d<sup>%d</sup> − 1) ÷ %d = <b>%s</b>." % (a1, r, n, r - 1, num(S)))

    def orta():
        a, r = ri(1, 9), ri(2, 6)
        c = a * r * r
        b = a * r
        return M("%d, x, %d sayıları pozitif terimli bir geometrik dizinin ardışık üç terimi ise x kaçtır?" % (a, c), num(b), W3([num((a + c) // 2) if (a + c) % 2 == 0 else num(b + 1), num(b * 2), num(a * r * r // 2) if (a * c) % 2 == 0 else num(b - 1), num(c - a)], num(b)),
                 "Geometrik ortalama: x² = %d · %d = %d → x = <b>%d</b>." % (a, c, a * c, b))

    def problem():
        k = ri(0, 2)
        if k == 0:
            a1 = ri(1, 9) * 1000
            p = ch([10, 20, 50])
            n = ri(2, 4)
            v = F(a1) * F(100 + p, 100) ** n
            if v.denominator != 1:
                return None
            return M("Bir firmanın satışları her yıl bir önceki yıla göre %%%d artıyor. Bu yıl %s ürün satıldıysa %d yıl sonra kaç ürün satılır?" % (p, num(a1), n), num(v),
                     W3([num(a1 + a1 * p * n // 100), num(v + a1 * p // 100), num(a1 * (100 + p) // 100), num(a1 * (100 + p * n) // 100 + 100)], num(v)),
                     "Her yıl %s ile çarpılır: %s · %s<sup>%d</sup> = <b>%s</b>." % (dq(F(100 + p, 100)), num(a1), dq(F(100 + p, 100)), n, num(v)))
        if k == 1:
            h = ri(2, 8) * 32
            n = ri(1, 5)
            v = F(h, 2 ** n)
            return M("Bir top %d cm yükseklikten bırakılıyor; her yere çarpışında bir önceki yüksekliğin yarısı kadar yükseliyor. %d. çarpışmadan sonra kaç cm yükselir?" % (h, n), sn(v),
                     W3([sn(F(h, 2 ** (n + 1))), sn(F(h, 2 ** (n - 1))), sn(F(h, 2 * n)), sn(h - 10 * n)], sn(v)), "%d · (1/2)<sup>%d</sup> = <b>%s cm</b>." % (h, n, sn(v)))
        r = ch([2, 3])
        n = ri(3, 8)
        return M("Bir haber ilk saatte %d kişiye ulaşıyor ve her saat ulaştığı kişi sayısı %d katına çıkıyor. %d. saatte kaç kişiye ulaşır?" % (r, r, n), num(r ** n), W3([num(r * n), num(r ** (n - 1)), num(r ** (n + 1)), num(sum(r ** i for i in range(1, n + 1)))], num(r ** n)),
                 "aₙ = %d · %d<sup>%d</sup> = <b>%s</b>." % (r, r, n - 1, num(r ** n)))

    sets = [("Genel terim", [(terim, 20)]), ("Ortak çarpan", [(r_bul, 20)]), ("İlk n terimin toplamı", [(toplam, 20)]),
            ("Geometrik ortalama", [(orta, 20)]), ("Problemler", [(problem, 20)])]
    return U(12, "geometrik-diziler", "N", "MAT.12.1.1", 2, "Geometrik Diziler ve Toplamları", "Geometrik Diziler",
             "Geometrik dizilerin genel terimini ve ilk n teriminin toplamını bulur; büyüme ve azalma durumlarını geometrik dizilerle modeller.",
             "genel terim, ortak çarpanı bulma, ilk n terimin toplamı, geometrik ortalama, yüzde artış ve yarılanma problemleri",
             "aₙ = a₁ · rⁿ⁻¹", "Sₙ = a₁(rⁿ − 1) ÷ (r − 1).", sets,
             ["Ardışık terimlerin oranı sabit olan diziye geometrik dizi, bu orana ortak çarpan (r) denir.",
              "Genel terim aₙ = a₁ · rⁿ⁻¹’dir; ardışık üç terimde ortadaki terimin karesi diğer ikisinin çarpımına eşittir.",
              "İlk n terimin toplamı Sₙ = a₁(rⁿ − 1) ÷ (r − 1)’dir (r ≠ 1)."],
             [("a₁ = 3, r = 2, a₅", ["3 · 2⁴"], "48"), ("4, x, 9", ["x² = 36"], "6")],
             [["aₙ = a₁ · rⁿ yazmak", "Üs n − 1"], ["Ortak çarpanı fark sanmak", "Oran alınır"], ["Yüzde artışı her yıl eklemek", "Her yıl çarpılır"]],
             [("Aritmetik ve geometrik dizi farkı?", "Aritmetikte sabit fark, geometrikte sabit oran vardır."), ("Geometrik dizi üstel fonksiyon mudur?", "Evet; aₙ, n’nin üstel bir fonksiyonudur."),
              ("Nerede kullanılır?", "Bileşik faiz, nüfus artışı ve radyoaktif bozunmada.")])


# ============================================================ 3. diziler ve fonksiyonlar
def u3():
    def genel():
        a, b, c = ri(-3, 3), ri(-6, 6), ri(-9, 9)
        if a == 0 and b == 0:
            return None
        n = ri(1, 12)
        v = a * n * n + b * n + c
        f = poly([a, b, c], "n")
        return M("Genel terimi aₙ = %s olan dizinin %d. terimi kaçtır?" % (f, n), sn(v), W3([sn(a * (n + 1) ** 2 + b * (n + 1) + c), sn(a * (n - 1) ** 2 + b * (n - 1) + c), sn(v + 1), sn(a * n + b * n + c)], sn(v)),
                 "n = %d yazılır: <b>%s</b>." % (n, sn(v)))

    def indirgemeli():
        a1 = ri(-5, 9)
        p, q = ch([1, 2, -1, 3]), ri(-5, 5)
        n = ri(3, 5)
        x = a1
        for _ in range(n - 1):
            x = p * x + q
        rec = lin(p, a_("n"), q).replace("aₙ", "aₙ")
        return M("%s = %s ve %s = %s ise %s kaçtır?" % (a_(1), sn(a1), "aₙ₊₁", rec, a_(n)), sn(x), W3([sn(p * x + q), sn(x - q) if p == 1 else sn((x - q) // p) if (x - q) % p == 0 else sn(x + 1), sn(a1 + (n - 1) * q), sn(x + 2)], sn(x)),
                 "Terimleri sırayla buluruz: <b>%s</b>." % sn(x))

    def kural():
        k = ri(0, 2)
        a1, d = ri(-5, 10), nz(-5, 6)
        if k == 0:
            terms = [a1 + i * d for i in range(4)]
            g = "aₙ = %s" % lin(d, "n", a1 - d)
            w = ["aₙ = %s" % lin(d, "n", a1), "aₙ = %s" % lin(a1, "n", d), "aₙ = %s" % lin(d, "n", a1 + d), "aₙ = %s" % lin(-d, "n", a1 - d)]
        elif k == 1:
            r = ch([2, 3, -2])
            a1 = nz(-4, 4)
            terms = [a1 * r ** i for i in range(4)]
            g = "aₙ = %s · %s<sup>n − 1</sup>" % (sn(a1), par(r))
            w = ["aₙ = %s · %s<sup>n</sup>" % (sn(a1), par(r)), "aₙ = %s · %s<sup>n − 1</sup>" % (sn(r), par(a1)), "aₙ = %s" % lin(r, "n", a1 - r), "aₙ = %s · %s<sup>n + 1</sup>" % (sn(a1), par(r))]
        else:
            c = ri(-5, 5)
            terms = [i * i + c for i in range(1, 5)]
            g = "aₙ = n²" + ((" + %s" % sn(c)) if c > 0 else (" − %s" % sn(-c)) if c < 0 else "")
            w = ["aₙ = %s" % lin(2, "n", c), "aₙ = (n + 1)²" + ((" + %s" % sn(c)) if c > 0 else (" − %s" % sn(-c)) if c < 0 else ""), "aₙ = 2n²" + ((" + %s" % sn(c)) if c > 0 else (" − %s" % sn(-c)) if c < 0 else ""), "aₙ = %s" % lin(3, "n", c - 2)]
        return M("İlk dört terimi %s olan dizinin genel terimi hangisidir?" % ", ".join(sn(t) for t in terms), g, W3(w, g), "n = 1, 2, 3, 4 yazarak kontrol ederiz: <b>%s</b>." % g)

    def monoton():
        a, b = nz(-6, 6), ri(-9, 9)
        k = ri(0, 1)
        if k == 0:
            f = lin(a, "n", b)
            g = "Artandır" if a > 0 else "Azalandır"
        else:
            c, d = ri(1, 5), ri(1, 9)
            # (cn + d) ÷ (n + 1) → aₙ₊₁ − aₙ = (c − d) ÷ ...
            if c == d:
                return None
            f = "(%s) ÷ (n + 1)" % lin(c, "n", d)
            g = "Artandır" if c > d else "Azalandır"
        return M("Genel terimi aₙ = %s olan dizi artan mı, azalan mı?" % f, g, ["Azalandır" if g == "Artandır" else "Artandır", "Sabittir", "Ne artan ne azalandır"],
                 "aₙ₊₁ − aₙ farkının işaretine bakılır: <b>%s</b>." % g.lower())

    def kacinci():
        a1, d = ri(-10, 20), nz(-6, 6)
        n = ri(5, 60)
        v = a1 + (n - 1) * d
        return M("Genel terimi aₙ = %s olan dizinin kaçıncı terimi %s’e eşittir?" % (lin(d, "n", a1 - d), sn(v)) if False else "Genel terimi aₙ = %s olan dizide aₙ = %s ise n kaçtır?" % (lin(d, "n", a1 - d), sn(v)),
                 num(n), W3([num(n + 1), num(n - 1), num(abs(v)) if abs(v) != n else num(n + 2), num(n * 2)], num(n)), "%s = %s → n = <b>%d</b>." % (lin(d, "n", a1 - d), sn(v), n))

    sets = [("Genel terimden terim", [(genel, 20)]), ("İndirgemeli diziler", [(indirgemeli, 20)]), ("Genel terimi bulma", [(kural, 20)]),
            ("Artan ve azalan diziler", [(monoton, 20)]), ("Kaçıncı terim", [(kacinci, 20)])]
    return U(12, "diziler-ve-fonksiyonlar", "N", "MAT.12.1.2", 3, "Diziler ve Fonksiyonlar: Genel Terim ve İndirgeme", "Diziler ve Fonksiyonlar",
             "Dizileri tanım kümesi pozitif tam sayılar olan fonksiyonlar olarak inceler; genel terim, indirgeme bağıntısı ve artanlık-azalanlığı yorumlar.",
             "genel terimden terim bulma, indirgeme bağıntısı, ilk terimlerden genel terimi bulma, artan ve azalan diziler, kaçıncı terim",
             "Dizi, f: ℤ⁺ → ℝ fonksiyonudur", "aₙ = f(n); indirgemede aₙ₊₁, aₙ’den bulunur.", sets,
             ["Dizi, tanım kümesi pozitif tam sayılar olan bir fonksiyondur: aₙ = f(n).",
              "İndirgeme bağıntısında her terim bir önceki terimden bulunur, örneğin aₙ₊₁ = 2aₙ + 1.",
              "aₙ₊₁ − aₙ &gt; 0 ise dizi artan, &lt; 0 ise azalandır."],
             [("aₙ = n² − 1, a₅", ["25 − 1"], "24"), ("3, 7, 11, 15", ["Fark 4"], "aₙ = 4n − 1")],
             [["n yerine 0 yazmak", "Diziler n = 1’den başlar"], ["İndirgemede bir adım atlamak", "Her terimi tek tek bul"], ["Genel terimi yalnızca ilk terimle kontrol etmek", "Birkaç terimle dene"]],
             [("Fibonacci dizisi nedir?", "aₙ₊₂ = aₙ₊₁ + aₙ bağıntısıyla tanımlanan dizidir: 1, 1, 2, 3, 5, 8, …"), ("Dizinin grafiği nasıldır?", "Ayrık noktalardan oluşur."),
              ("Her dizinin genel terimi var mı?", "Hayır; bazı diziler yalnızca indirgemeyle tanımlanır.")])


# ============================================================ 4. polinomlar
def u4():
    def derece():
        n = ri(2, 6)
        cs = [nz(-9, 9)] + [ri(-9, 9) for _ in range(n)]
        k = ri(0, 2)
        f = poly(cs)
        if k == 0:
            return M("P(x) = %s polinomunun derecesi kaçtır?" % f, num(n), W3([num(n + 1), num(n - 1), num(len([c for c in cs if c])), num(cs[0]) if cs[0] > 0 and cs[0] != n else num(n + 2)], num(n)), "En büyük üs <b>%d</b>." % n)
        if k == 1:
            return M("P(x) = %s polinomunun başkatsayısı kaçtır?" % f, sn(cs[0]), W3([sn(cs[-1]), sn(n), sn(cs[1]) if cs[1] else "0", sn(-cs[0])], sn(cs[0])), "En büyük dereceli terimin katsayısı: <b>%s</b>." % sn(cs[0]))
        s = sum(cs)
        return M("P(x) = %s polinomunun katsayılar toplamı kaçtır?" % f, sn(s), W3([sn(cs[-1]), sn(s - cs[-1]), sn(peval(cs, -1)), sn(s + 1)], sn(s)), "Katsayılar toplamı P(1) = <b>%s</b>." % sn(s))

    def deger():
        n = ri(2, 3)
        cs = [nz(-4, 4)] + [ri(-6, 6) for _ in range(n)]
        x = ri(-3, 3)
        v = peval(cs, x)
        return M("P(x) = %s ise P(%s) kaçtır?" % (poly(cs), sn(x)), sn(v), W3([sn(peval(cs, -x)), sn(v + 1), sn(sum(cs)), sn(cs[-1])], sn(v)), "x = %s yazılır: <b>%s</b>." % (sn(x), sn(v)))

    def islem():
        p = [nz(-4, 4), ri(-6, 6), ri(-9, 9)]
        q = [ri(-4, 4), ri(-6, 6), ri(-9, 9)]
        k = ri(0, 1)
        if k == 0:
            h = [a + b for a, b in zip(p, q)]
            if h[0] == 0:
                return None
            g = poly(h)
            return M("P(x) = %s ve Q(x) = %s ise P(x) + Q(x) hangisidir?" % (poly(p), poly(q)), g, W3([poly([a - b for a, b in zip(p, q)]), poly([h[0], h[1], h[2] + 1]), poly([h[0], -h[1], h[2]]), poly([a * b for a, b in zip(p, q)])], g),
                     "Benzer terimler toplanır: <b>%s</b>." % g)
        a, b = nz(-4, 4), ri(-6, 6)
        p2 = [nz(-3, 3), ri(-5, 5)]
        h = pmul([a, b], p2)
        g = poly(h)
        return M("(%s)(%s) çarpımı hangisidir?" % (poly([a, b]), poly(p2)), g, W3([poly([h[0], -h[1], h[2]]), poly([h[0], h[2]]), poly([h[0], h[1], -h[2]]) if h[2] else poly([h[0], h[1] + 1, 0]), poly([a + p2[0], b + p2[1]])], g),
                 "Dağılma özelliğiyle çarpılır: <b>%s</b>." % g)

    def esit():
        a, b = nz(-6, 6), ri(-9, 9)
        m, n = nz(-5, 5), ri(-9, 9)
        # (a − 2)x + b = ... form: P(x) = (k + m)x + (t − n) ≡ ax + b
        k = a - m
        t = b + n
        return M("(%s)x + (%s) = %s olduğuna göre k + t kaçtır?" % (lin(1, "k", m), lin(1, "t", -n), lin(a, "x", b)), sn(k + t), W3([sn(a + b), sn(k - t), sn(k + t + 2 * m), sn(a - m + b - n)], sn(k + t)),
                 "Polinom eşitliğinde aynı dereceli terimlerin katsayıları eşittir: k = %s, t = %s → <b>%s</b>." % (sn(k), sn(t), sn(k + t)))

    sets = [("Derece ve katsayılar", [(derece, 20)]), ("Polinomun değeri", [(deger, 20)]), ("Toplama ve çarpma", [(islem, 20)]),
            ("Polinom eşitliği", [(esit, 20)]), ("Karışık", [(derece, 7), (deger, 7), (islem, 6)])]
    return U(12, "polinomlar", "N", "MAT.12.1.3", 4, "Polinomlar: Derece, Katsayılar ve İşlemler", "Polinomlar",
             "Polinomları doğrusal ve karesel fonksiyonlarla ilişkilendirerek tanımlar; derece, katsayılar, değer ve polinomlarla işlemleri kullanır.",
             "derece, başkatsayı, katsayılar toplamı, polinomun değeri, toplama ve çarpma, polinom eşitliği",
             "Katsayılar toplamı P(1)", "Sabit terim P(0)’dır.", sets,
             ["P(x) = aₙxⁿ + … + a₁x + a₀ biçimindeki ifadeye polinom denir; n derece, aₙ başkatsayıdır.",
              "P(1) katsayılar toplamını, P(0) sabit terimi verir.",
              "İki polinom eşitse aynı dereceli terimlerinin katsayıları eşittir. Doğrusal fonksiyon 1., karesel fonksiyon 2. dereceden polinomdur."],
             [("P(x) = 2x³ − x + 4", ["Derece 3", "P(1) = 5"], "Başkatsayı 2"), ("(x + 2)(x − 3)", ["x² − 3x + 2x − 6"], "x² − x − 6")],
             [["Dereceyi terim sayısı sanmak", "En büyük üs"], ["Katsayılar toplamını P(0) sanmak", "P(1)"], ["Çarpmada bir terimi unutmak", "Her terimi her terimle çarp"]],
             [("Sabit polinomun derecesi?", "Sıfırdan farklı sabit polinomun derecesi 0’dır."), ("√x polinom mu?", "Hayır; üsler doğal sayı olmalıdır."),
              ("Polinomlar nerede kullanılır?", "Eğri çizimi, mühendislik hesapları ve bilgisayar grafiklerinde.")])


# ============================================================ 5. polinom bölme ve kalan
def u5():
    def kalan():
        n = ri(2, 4)
        cs = [nz(-3, 3)] + [ri(-6, 6) for _ in range(n)]
        a = nz(-3, 3)
        r = peval(cs, a)
        return M("P(x) = %s polinomunun %s ile bölümünden kalan kaçtır?" % (poly(cs), lin(1, "x", -a)), sn(r), W3([sn(peval(cs, -a)), sn(r + 1), sn(cs[-1]), sn(sum(cs))], sn(r)),
                 "Kalan teoremi: kalan P(%s) = <b>%s</b>." % (sn(a), sn(r)))

    def carpan():
        p, q = ri(-6, 6), ri(-6, 6)
        a = nz(-3, 3)
        # P(x) = (x − p)(x − q)(x − a) ... find k: x³ + bx² + cx + k with factor (x − a)
        cs = pmul(pmul([1, -p], [1, -q]), [1, -a])
        k = cs[-1]
        cs2 = cs[:-1] + [0]
        g = sn(k)
        return M("P(x) = %s + k polinomu %s ile tam bölünebiliyorsa k kaçtır?" % (poly(cs2) if any(cs2[1:]) else "x³", lin(1, "x", -a)), g, W3([sn(-k), sn(k + a), sn(peval(cs2, -a)), sn(k * 2) if k else "1"], g),
                 "P(%s) = 0 olmalı: %s + k = 0 → k = <b>%s</b>." % (sn(a), sn(peval(cs2, a)), g))

    def bolum():
        a = nz(-4, 4)
        qq = [nz(-3, 3), ri(-6, 6)]
        r = ri(-9, 9)
        cs = pmul(qq, [1, -a])
        cs[-1] += r
        g = poly(qq)
        return M("P(x) = %s polinomunun %s ile bölümünden elde edilen bölüm hangisidir?" % (poly(cs), lin(1, "x", -a)), g, W3([poly([qq[0], -qq[1]]) if qq[1] else poly([qq[0], 1]), poly([qq[0], qq[1] + 1]), poly([-qq[0], qq[1]]), poly([qq[0], qq[1], r]) if r else poly([qq[0], qq[1] - 1])], g),
                 "Bölme ya da Horner yöntemiyle bölüm <b>%s</b>, kalan %s bulunur." % (g, sn(r)))

    def kok():
        r1, r2, r3 = sorted(sh(list(range(-5, 6)))[:3])
        cs = pmul(pmul([1, -r1], [1, -r2]), [1, -r3])
        k = ri(0, 1)
        if k == 0:
            s = r1 + r2 + r3
            return M("P(x) = %s polinomunun köklerinin toplamı kaçtır?" % poly(cs), sn(s), W3([sn(-s) if s else "1", sn(r1 * r2 * r3), sn(cs[2]), sn(s + 1)], sn(s)),
                     "Kökler toplamı −b ÷ a = <b>%s</b> (kökler %s, %s, %s)." % (sn(s), sn(r1), sn(r2), sn(r3)))
        g = "%s, %s ve %s" % (sn(r1), sn(r2), sn(r3))
        return M("P(x) = %s polinomunun kökleri nelerdir?" % poly(cs), g, W3(["%s, %s ve %s" % (sn(-r3), sn(-r2), sn(-r1)), "%s, %s ve %s" % (sn(r1), sn(r2), sn(r3 + 1)), "%s, %s ve %s" % (sn(r1 - 1), sn(r2), sn(r3))], g),
                 "Sabit terimin bölenleri denenir; P(x) = %s%s%s: <b>%s</b>." % (fct(r1), fct(r2), fct(r3), g))

    def ikinci():
        n = ri(2, 3)
        cs = [nz(-3, 3)] + [ri(-6, 6) for _ in range(n)]
        a, b = ri(-4, 4), ri(1, 5)
        r = peval(cs, F(-b, a)) if a else None
        if a == 0 or F(-b, a).denominator != 1:
            return None
        x0 = -b // a
        return M("P(x) = %s polinomunun %s ile bölümünden kalan kaçtır?" % (poly(cs), lin(a, "x", b)), sn(r), W3([sn(peval(cs, -x0)), sn(r + 1), sn(peval(cs, b)), sn(cs[-1])], sn(r)),
                 "%s = 0 → x = %s; kalan P(%s) = <b>%s</b>." % (lin(a, "x", b), sn(x0), sn(x0), sn(r)))

    sets = [("Kalan teoremi", [(kalan, 20)]), ("Bölüm", [(bolum, 20)]), ("Çarpan ve bilinmeyen katsayı", [(carpan, 20)]),
            ("Kökler", [(kok, 20)]), ("Karışık", [(ikinci, 10), (kalan, 10)])]
    return U(12, "polinom-bolme-ve-kalan", "N", "MAT.12.1.4", 5, "Polinomlarda Bölme, Kalan Teoremi ve Kökler", "Polinomlarda Bölme",
             "Polinomların nitel özelliklerini inceler; polinom bölmesi, kalan teoremi ve çarpanlara ayırmayla kökleri bulur.",
             "kalan teoremi, bölüm bulma, çarpan olma şartı ve bilinmeyen katsayı, kökler ve kökler toplamı, ax + b ile bölme",
             "P(x) ÷ (x − a) kalanı P(a)", "P(a) = 0 ise (x − a) bir çarpandır.", sets,
             ["P(x) = (x − a) · Q(x) + K biçiminde yazılır; kalan teoremi: K = P(a).",
              "P(a) = 0 ise x − a, P(x)’in bir çarpanıdır ve a bir köktür.",
              "Tam sayı kökler sabit terimin bölenleri arasındadır; ax³ + bx² + cx + d için kökler toplamı −b ÷ a’dır."],
             [("P(x) = x³ − 2x + 5, (x − 2)", ["P(2) = 8 − 4 + 5"], "9"), ("x³ − 6x² + 11x − 6", ["x = 1, 2, 3 denenir"], "1, 2, 3")],
             [["x − a için P(−a) almak", "x − a = 0 → x = a"], ["Kalanı bölümle karıştırmak", "Kalanın derecesi bölenden küçüktür"], ["Köklerin işaretini ters almak", "(x − 2) → kök 2"]],
             [("Horner yöntemi nedir?", "Katsayılarla hızlı bölme yöntemidir."), ("Kalanın derecesi?", "Bölenin derecesinden küçüktür."),
              ("Kök ile çarpan ilişkisi?", "a kök ise (x − a) çarpandır ve tersi de doğrudur.")])


# ============================================================ 6. polinom ve rasyonel denklemler, eşitsizlikler
def u6():
    def carpim_denk():
        r1, r2, r3 = sorted(sh(list(range(-6, 7)))[:3])
        g = "{%s, %s, %s}" % (sn(r1), sn(r2), sn(r3))
        f = "%s%s%s = 0" % tuple(fct(r) for r in (r1, r2, r3))
        return M("%s denkleminin çözüm kümesi nedir?" % f, g, W3(["{%s, %s, %s}" % (sn(-r3), sn(-r2), sn(-r1)), "{%s, %s}" % (sn(r1), sn(r3)), "{%s, %s, %s}" % (sn(r1), sn(r2), sn(r3 + 1))], g),
                 "Çarpım sıfırsa çarpanlardan biri sıfırdır: <b>%s</b>." % g)

    def esitsizlik():
        r1, r2 = sorted(sh(list(range(-6, 7)))[:2])
        k = ch(["&gt; 0", "&lt; 0", "≥ 0", "≤ 0"])
        f = "%s%s" % tuple(fct(r) for r in (r1, r2))
        ins = {"&lt; 0": "(%s, %s)", "≤ 0": "[%s, %s]"}
        out = {"&gt; 0": "(−∞, %s) ∪ (%s, ∞)", "≥ 0": "(−∞, %s] ∪ [%s, ∞)"}
        g = (ins.get(k) or out.get(k)) % (sn(r1), sn(r2))
        w = [x % (sn(r1), sn(r2)) for x in ("(%s, %s)", "[%s, %s]", "(−∞, %s) ∪ (%s, ∞)", "(−∞, %s] ∪ [%s, ∞)")] + ["(%s, %s)" % (sn(-r2), sn(-r1))]
        return M("%s %s eşitsizliğinin çözüm kümesi nedir?" % (f, k), g, W3(w, g), "Kökler %s ve %s; işaret tablosunda dışarıda pozitif, kökler arasında negatif: <b>%s</b>." % (sn(r1), sn(r2), g))

    def rasyonel():
        a, b = ri(-6, 6), ri(-6, 6)
        if a == b:
            return None
        k = ch(["&gt; 0", "&lt; 0"])
        lo, hi = sorted([a, b])
        if k == "&lt; 0":
            g = "(%s, %s)" % (sn(lo), sn(hi))
        else:
            g = "(−∞, %s) ∪ (%s, ∞)" % (sn(lo), sn(hi))
        f = "%s ÷ %s" % tuple(fct(r) for r in (a, b))
        w = ["(%s, %s)" % (sn(lo), sn(hi)), "(−∞, %s) ∪ (%s, ∞)" % (sn(lo), sn(hi)), "[%s, %s)" % (sn(lo), sn(hi)), "(−∞, %s] ∪ (%s, ∞)" % (sn(lo), sn(hi))]
        return M("%s %s eşitsizliğinin çözüm kümesi nedir?" % (f, k), g, W3(w, g), "Pay ve paydanın kökleri %s ve %s; payda sıfır olamaz: <b>%s</b>." % (sn(a), sn(b), g))

    def ras_denk():
        a, b, c = nz(-5, 5), ri(-9, 9), nz(-4, 4)
        x = ri(-6, 6)
        d = ri(-9, 9)
        if c * x + d == 0:
            return None
        v = F(a * x + b, c * x + d)
        if v.denominator != 1 or a == v * c:
            return None
        return M("(%s) ÷ (%s) = %s denkleminin çözümü nedir?" % (lin(a, "x", b), lin(c, "x", d), sn(v)), "x = %s" % sn(x), W3(["x = %s" % sn(-x) if x else "x = 1", "x = %s" % sn(x + 1), "x = %s" % sn(F(-d, c)), "Çözüm yoktur"], "x = %s" % sn(x)),
                 "%s = %s · (%s) → x = <b>%s</b>; payda sıfır olmuyor." % (lin(a, "x", b), sn(v), lin(c, "x", d), sn(x)))

    def problem():
        x = ri(3, 20)
        y = x + ri(1, 8)
        k = ri(0, 1)
        if k == 0:
            return M("Ardışık olmayan iki pozitif tam sayıdan büyüğü küçüğünden %d fazladır ve çarpımları %d’dir. Küçük sayı kaçtır?" % (y - x, x * y) if False else
                     "İki pozitif tam sayıdan büyüğü küçüğünden %d fazla ve çarpımları %s ise küçük sayı kaçtır?" % (y - x, num(x * y)), num(x), W3([num(y), num(x + 1), num(x - 1), num((x * y) // (y - x)) if (x * y) % (y - x) == 0 else num(x + 2)], num(x)),
                     "x(x + %d) = %s → x² + %dx − %s = 0 → x = <b>%d</b>." % (y - x, num(x * y), y - x, num(x * y), x))
        h = ri(2, 6)
        V = x * y * h
        return M("Bir kutunun yüksekliği %d cm, tabanının uzun kenarı kısa kenarından %d cm fazla ve hacmi %s cm³ ise kısa kenar kaç cm’dir?" % (h, y - x, num(V)), "%d cm" % x, W3(["%d cm" % y, "%d cm" % (x + 1), "%d cm" % (x - 1), "%d cm" % h], "%d cm" % x),
                 "%d · x(x + %d) = %s → x(x + %d) = %d → x = <b>%d cm</b>." % (h, y - x, num(V), y - x, x * y, x))

    sets = [("Çarpım biçimindeki denklemler", [(carpim_denk, 20)]), ("Polinom eşitsizlikleri", [(esitsizlik, 20)]), ("Rasyonel denklemler", [(ras_denk, 20)]),
            ("Rasyonel eşitsizlikler", [(rasyonel, 20)]), ("Problemler", [(problem, 20)])]
    return U(12, "polinom-ve-rasyonel-denklemler", "N", "MAT.12.1.5", 6, "Polinom ve Rasyonel Denklem ve Eşitsizlikler", "Polinom ve Rasyonel Denklemler",
             "Polinom ve rasyonel fonksiyonlarla ifade edilen denklem ve eşitsizlik problemlerini çözer; işaret tablosu kullanır.",
             "çarpım biçimindeki denklemler, işaret tablosuyla polinom eşitsizlikleri, rasyonel denklemler, rasyonel eşitsizlikler, gerçek yaşam problemleri",
             "Kökleri bul, işaret tablosu yap", "Payda sıfır olamaz; payda kökü aralığa dâhil edilmez.", sets,
             ["Çarpım sıfırsa çarpanlardan en az biri sıfırdır.",
              "Eşitsizliklerde kökler sayı doğrusuna yerleştirilir ve işaret tablosu yapılır; en büyük dereceli terimin katsayısı pozitifse en sağdaki aralık pozitiftir.",
              "Rasyonel ifadelerde paydanın kökü tanım kümesinde değildir; eşitsizlikte açık uçla gösterilir."],
             [("(x − 1)(x + 3) &lt; 0", ["Kökler −3 ve 1"], "(−3, 1)"), ("(x − 2) ÷ (x + 1) ≥ 0", ["x ≠ −1"], "(−∞, −1) ∪ [2, ∞)")],
             [["Paydanın kökünü dâhil etmek", "Payda kökü her zaman açık uç"], ["İşaret tablosunda yönü ters almak", "En sağ aralıktan başla"], ["Her iki tarafı x’li ifadeyle bölmek", "Kök kaybolabilir"]],
             [("Çift katlı kökte ne olur?", "İşaret değişmez."), ("Rasyonel denklemde neden kontrol gerekir?", "Paydayı sıfır yapan değer çözüm olamaz."),
              ("İşaret tablosu nedir?", "İfadenin işaretini aralıklara göre gösteren tablodur.")])


# ============================================================ 7–9. çember ve daire
def u7():
    def kiris():
        a, b, c = ch([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (4, 3, 5), (12, 5, 13), (15, 8, 17)])
        m = ri(1, 3)
        a, b, c = a * m, b * m, c * m
        k = ri(0, 2)
        if k == 0:
            return M("Yarıçapı %d cm olan bir çemberde merkezden %d cm uzaklıktaki kirişin uzunluğu kaç cm’dir?" % (c, a), "%d cm" % (2 * b), W3(["%d cm" % b, "%d cm" % (2 * a), "%d cm" % (a + c), "%d cm" % (2 * c)], "%d cm" % (2 * b)),
                     "Merkezden kirişe çizilen dikme kirişi ortalar: yarı kiriş √(%d − %d) = %d → <b>%d cm</b>." % (c * c, a * a, b, 2 * b))
        if k == 1:
            return M("Yarıçapı %d cm olan bir çemberde %d cm uzunluğundaki kirişin merkeze uzaklığı kaç cm’dir?" % (c, 2 * b), "%d cm" % a, W3(["%d cm" % b, "%d cm" % (c - b), "%d cm" % (2 * a), "%d cm" % (c - a)], "%d cm" % a),
                     "Yarı kiriş %d; √(%d − %d) = <b>%d cm</b>." % (b, c * c, b * b, a))
        return M("Bir çemberde %d cm uzunluğundaki kiriş merkezden %d cm uzaklıktadır. Çemberin yarıçapı kaç cm’dir?" % (2 * b, a), "%d cm" % c, W3(["%d cm" % (a + b), "%d cm" % (2 * c), "%d cm" % b, "%d cm" % (c + 1)], "%d cm" % c),
                 "r = √(%d² + %d²) = <b>%d cm</b>." % (b, a, c))

    def teget():
        a, b, c = ch([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (4, 3, 5), (12, 5, 13), (15, 8, 17)])
        m = ri(1, 3)
        a, b, c = a * m, b * m, c * m
        k = ri(0, 1)
        if k == 0:
            return M("Yarıçapı %d cm olan çembere, merkezden %d cm uzaklıktaki P noktasından çizilen teğet parçasının uzunluğu kaç cm’dir?" % (a, c), "%d cm" % b, W3(["%d cm" % (c - a), "%d cm" % (a + c), "%d cm" % (2 * b), "%d cm" % a], "%d cm" % b),
                     "Teğet yarıçapa diktir: √(%d − %d) = <b>%d cm</b>." % (c * c, a * a, b))
        return M("Bir çembere dışındaki bir P noktasından çizilen teğet parçasının uzunluğu %d cm, çemberin yarıçapı %d cm ise P’nin merkeze uzaklığı kaç cm’dir?" % (b, a), "%d cm" % c, W3(["%d cm" % (a + b), "%d cm" % (b - a) if b > a else "%d cm" % (c + 2), "%d cm" % (2 * c), "%d cm" % (c + 1)], "%d cm" % c),
                 "√(%d² + %d²) = <b>%d cm</b>." % (a, b, c))

    def iki_teget():
        t = ri(3, 20)
        r = ri(2, 15)
        return M("Bir çembere dışındaki bir P noktasından iki teğet çiziliyor ve değme noktaları A ile B oluyor. |PA| = %d cm ise |PB| kaç cm’dir?" % t, "%d cm" % t, W3(["%d cm" % (2 * t), "%d cm" % (t + r), "%d cm" % (t // 2) if t % 2 == 0 else "%d cm" % (t + 1), "%d cm" % r], "%d cm" % t),
                 "Bir noktadan çembere çizilen teğet parçaları eşittir: <b>%d cm</b>." % t) if t != r else None

    def tanim():
        S = [("Çemberin iki noktasını birleştiren doğru parçası", "Kiriş"), ("Merkezden geçen kiriş", "Çap"), ("Çemberle yalnızca bir noktada kesişen doğru", "Teğet"),
             ("Çemberi iki noktada kesen doğru", "Kesen"), ("Çember üzerindeki iki nokta arasında kalan parça", "Yay"), ("Merkez ile çember üzerindeki bir noktayı birleştiren doğru parçası", "Yarıçap")]
        t, g = ch(S)
        return M("%s neye denir?" % t, g, W3(sh([x for _, x in S]), g), "Cevap: <b>%s</b>." % g)

    def konum():
        r = ri(3, 15)
        d = ri(1, 25)
        g = "Kesen (iki noktada keser)" if d < r else "Teğet (bir noktada değer)" if d == r else "Kesişmez"
        return M("Yarıçapı %d cm olan çemberin merkezinin bir doğruya uzaklığı %d cm ise doğru ile çemberin durumu nedir?" % (r, d), g,
                 W3(["Kesen (iki noktada keser)", "Teğet (bir noktada değer)", "Kesişmez", "Doğru merkezden geçer"], g), "d %s r olduğundan <b>%s</b>." % ("&lt;" if d < r else "=" if d == r else "&gt;", g.lower()))

    sets = [("Çemberin elemanları", [(tanim, 6), (konum, 14)]), ("Kirişin merkeze uzaklığı", [(kiris, 20)]), ("Teğet", [(teget, 20)]),
            ("Bir noktadan çizilen teğetler", [(iki_teget, 10), (konum, 10)]), ("Karışık", [(kiris, 10), (teget, 10)])]
    return U(12, "cemberin-elemanlari", "GS", "MAT.12.2.1", 7, "Çemberin Elemanları: Kiriş, Teğet ve Kesen", "Çemberin Elemanları",
             "Çemberin elemanlarını (merkez, yarıçap, çap, kiriş, yay, teğet, kesen) tanır; kiriş ve teğet özelliklerini kullanır.",
             "çemberin elemanları, doğru ile çemberin durumu, kirişin merkeze uzaklığı, teğet parçasının uzunluğu, bir noktadan çizilen teğetler",
             "Merkezden kirişe dikme kirişi ortalar", "Teğet, değme noktasındaki yarıçapa diktir.", sets,
             ["Merkezden bir kirişe indirilen dikme kirişi iki eş parçaya ayırır; yarıçap, yarı kiriş ve uzaklık bir dik üçgen oluşturur.",
              "Teğet, değme noktasında yarıçapa diktir. Dışarıdaki bir noktadan çizilen iki teğet parçası eşittir.",
              "Merkezin doğruya uzaklığı d olmak üzere d &lt; r ise doğru keser, d = r ise teğettir, d &gt; r ise kesişmez."],
             [("r = 5, uzaklık 3", ["√(25 − 9) = 4"], "Kiriş 8"), ("r = 6, |PO| = 10", ["√(100 − 36)"], "Teğet 8")],
             [["Kirişin tamamını dik kenar almak", "Yarısı dik kenardır"], ["Teğetin yarıçapa dik olduğunu unutmak", "Dik üçgen kur"], ["Kesen ile teğeti karıştırmak", "Teğet tek noktada değer"]],
             [("En uzun kiriş hangisi?", "Çaptır."), ("Eş kirişlerin özelliği?", "Merkeze eşit uzaklıktadırlar."), ("Teğet neden yarıçapa dik?", "Değme noktası çembere en yakın noktadır.")])


def u8():
    def cevre():
        m = ri(20, 170)
        k = ri(0, 1)
        if k == 0:
            if m % 2:
                return None
            return M("Bir çemberde %d°’lik yayı gören çevre açı kaç derecedir?" % m if False else "Bir çemberde ölçüsü %d° olan yayı gören çevre açı kaç derecedir?" % m, "%d°" % (m // 2), W3(["%d°" % m, "%d°" % (2 * m) if 2 * m < 360 else "%d°" % (180 - m // 2), "%d°" % (180 - m), "%d°" % (90 - m // 2)], "%d°" % (m // 2)),
                     "Çevre açı gördüğü yayın yarısıdır: <b>%d°</b>." % (m // 2))
        return M("Bir çemberde ölçüsü %d° olan çevre açının gördüğü yayı gören merkez açı kaç derecedir?" % (m // 2 if m % 2 == 0 else m), "%d°" % (2 * (m // 2 if m % 2 == 0 else m)),
                 W3(["%d°" % (m // 2 if m % 2 == 0 else m), "%d°" % (180 - (m // 2 if m % 2 == 0 else m)), "%d°" % (4 * (m // 2 if m % 2 == 0 else m) % 360 or 90), "%d°" % (90 + (m // 2 if m % 2 == 0 else m))], "%d°" % (2 * (m // 2 if m % 2 == 0 else m))),
                 "Merkez açı, aynı yayı gören çevre açının iki katıdır: <b>%d°</b>." % (2 * (m // 2 if m % 2 == 0 else m))) if 2 * (m // 2 if m % 2 == 0 else m) < 360 else None

    def cap():
        a = ri(15, 75)
        return M("[AB] çemberin çapı ve C çember üzerinde bir noktadır. m(CAB) = %d° ise m(CBA) kaç derecedir?" % a, "%d°" % (90 - a), W3(["%d°" % (180 - a), "%d°" % a, "%d°" % (90 + a), "%d°" % (2 * a) if 2 * a != 90 - a else "%d°" % (a + 10)], "%d°" % (90 - a)),
                 "Çapı gören çevre açı 90°’dir: m(ACB) = 90° → 180 − 90 − %d = <b>%d°</b>." % (a, 90 - a))

    def ic():
        x, y = ri(20, 160), ri(20, 160)
        if (x + y) % 2 or x + y >= 360:
            return None
        return M("İki kiriş çemberin içinde kesişiyor. Oluşan açının gördüğü yaylar %d° ve %d° ise bu açı kaç derecedir?" % (x, y), "%d°" % ((x + y) // 2), W3(["%d°" % (abs(x - y) // 2) if abs(x - y) % 2 == 0 and x != y else "%d°" % ((x + y) // 2 + 10), "%d°" % (x + y) if x + y < 180 else "%d°" % (360 - x - y), "%d°" % (180 - (x + y) // 2), "%d°" % ((x + y) // 4) if (x + y) % 4 == 0 else "%d°" % ((x + y) // 2 - 5)], "%d°" % ((x + y) // 2)),
                 "İç açı, gördüğü yayların toplamının yarısıdır: (%d + %d) ÷ 2 = <b>%d°</b>." % (x, y, (x + y) // 2))

    def dis():
        x, y = ri(80, 220), ri(10, 90)
        if (x - y) % 2 or x <= y or x + y > 340:
            return None
        return M("Çemberin dışındaki bir noktadan çizilen iki kesen arasındaki açının gördüğü yaylar %d° ve %d° ise bu açı kaç derecedir?" % (x, y), "%d°" % ((x - y) // 2), W3(["%d°" % ((x + y) // 2), "%d°" % (x - y), "%d°" % (180 - (x - y) // 2), "%d°" % ((x - y) // 2 + 10)], "%d°" % ((x - y) // 2)),
                 "Dış açı, yayların farkının yarısıdır: (%d − %d) ÷ 2 = <b>%d°</b>." % (x, y, (x - y) // 2))

    def teget_kiris():
        m = ri(20, 170) * 2
        if m >= 360:
            return None
        return M("Teğet ile kiriş arasındaki açının gördüğü yay %d° ise bu açı kaç derecedir?" % m, "%d°" % (m // 2), W3(["%d°" % m if m < 360 else "100°", "%d°" % (180 - m // 2), "%d°" % (90 - m // 2) if m < 180 else "%d°" % (m // 2 - 30), "%d°" % (m // 4) if m % 4 == 0 else "%d°" % (m // 2 + 15)], "%d°" % (m // 2)),
                 "Teğet-kiriş açısı gördüğü yayın yarısıdır: <b>%d°</b>." % (m // 2))

    def kirisler_dortgen():
        a = ri(50, 130)
        return M("Köşeleri bir çember üzerinde olan ABCD dörtgeninde (kirişler dörtgeni) m(A) = %d° ise m(C) kaç derecedir?" % a, "%d°" % (180 - a), W3(["%d°" % a, "%d°" % (360 - a), "%d°" % (90 - a) if a < 90 else "%d°" % (a - 90), "%d°" % (2 * a) if 2 * a < 360 else "%d°" % (a + 20)], "%d°" % (180 - a)),
                 "Kirişler dörtgeninde karşılıklı açılar bütünlerdir: 180 − %d = <b>%d°</b>." % (a, 180 - a))

    sets = [("Merkez ve çevre açı", [(cevre, 20)]), ("Çapı gören açı", [(cap, 10), (kirisler_dortgen, 10)]), ("İç açı", [(ic, 20)]),
            ("Dış açı", [(dis, 20)]), ("Teğet-kiriş açısı", [(teget_kiris, 20)])]
    return U(12, "cemberde-acilar", "GS", "MAT.12.2.2", 8, "Çemberde Açılar", "Çemberde Açılar",
             "Çemberde merkez, çevre, iç, dış ve teğet-kiriş açıların ölçüleri ile gördükleri yaylar arasındaki ilişkileri kullanır.",
             "merkez ve çevre açı, çapı gören açı, kirişler dörtgeni, iç açı, dış açı, teğet-kiriş açısı",
             "Çevre açı = yay ÷ 2", "Merkez açı gördüğü yaya eşittir.", sets,
             ["Merkez açı gördüğü yayın ölçüsüne eşittir; çevre açı ve teğet-kiriş açısı gördüğü yayın yarısıdır.",
              "Çapı gören çevre açı 90°’dir; kirişler dörtgeninde karşılıklı açılar toplamı 180°’dir.",
              "İç açı gördüğü iki yayın toplamının yarısı, dış açı ise yayların farkının yarısıdır."],
             [("Yay 100°", ["Çevre açı 50°"], "Merkez açı 100°"), ("Yaylar 140° ve 40°, dış açı", ["(140 − 40) ÷ 2"], "50°")],
             [["Çevre açıyı yaya eşit almak", "Yarısıdır"], ["İç açıda farkı almak", "İç açıda toplam"], ["Dış açıda toplamı almak", "Dış açıda fark"]],
             [("Aynı yayı gören çevre açılar?", "Birbirine eşittir."), ("Teğet-kiriş açısı neden çevre açı gibi?", "Çevre açının bir kenarının teğete dönüşmüş hâlidir."),
              ("Kirişler dörtgeni nedir?", "Bütün köşeleri bir çember üzerinde olan dörtgendir.")])


def u9():
    def yay():
        r = ri(2, 24)
        a = ch([30, 45, 60, 72, 90, 120, 135, 150, 180, 240, 270, 300])
        v = F(2 * r * a, 360)
        return M("Yarıçapı %d cm olan bir çemberde %d°’lik merkez açının gördüğü yayın uzunluğu kaç cm’dir?" % (r, a) if False else "Yarıçapı %d cm olan bir çemberde ölçüsü %d° olan merkez açının gördüğü yayın uzunluğu kaç cm’dir?" % (r, a),
                 pis(v), W3([pis(v * 2), pis(F(r * r * a, 360)), pis(v / 2), pis(v + 1)], pis(v)), "Yay = 2πr · %d ÷ 360 = <b>%s</b>." % (a, pis(v)))

    def dilim():
        r = ri(2, 20)
        a = ch([30, 45, 60, 72, 90, 120, 135, 150, 180, 240, 270, 300])
        v = F(r * r * a, 360)
        return M("Yarıçapı %d cm ve merkez açısının ölçüsü %d° olan daire diliminin alanı kaç cm²’dir?" % (r, a), pis(v), W3([pis(F(2 * r * a, 360)), pis(v * 2), pis(F(r * r)), pis(v + F(1, 2))], pis(v)),
                 "Alan = πr² · %d ÷ 360 = <b>%s</b>." % (a, pis(v)))

    def daire():
        r = ri(1, 30)
        k = ri(0, 2)
        if k == 0:
            return M("Yarıçapı %d cm olan dairenin alanı kaç cm²’dir?" % r, pis(r * r), W3([pis(2 * r), pis(r * r * 2), pis(F(r * r, 2)), pis(r)], pis(r * r)), "πr² = <b>%s</b>." % pis(r * r))
        if k == 1:
            return M("Çevresi %s cm olan çemberin yarıçapı kaç cm’dir?" % pis(2 * r), "%d cm" % r, W3(["%d cm" % (2 * r), "%d cm" % (r * r) if r > 1 else "4 cm", "%s cm" % sn(F(r, 2)), "%d cm" % (r + 1)], "%d cm" % r), "2πr = %s → r = <b>%d cm</b>." % (pis(2 * r), r))
        return M("Alanı %s cm² olan dairenin çevresi kaç cm’dir?" % pis(r * r), pis(2 * r), W3([pis(r), pis(r * r), pis(4 * r), pis(F(r, 2))], pis(2 * r)), "πr² = %s → r = %d; çevre 2πr = <b>%s</b>." % (pis(r * r), r, pis(2 * r)))

    def halka():
        r, R = sorted(sh(list(range(1, 16)))[:2])
        v = R * R - r * r
        return M("Yarıçapları %d cm ve %d cm olan iç içe (aynı merkezli) iki çember arasında kalan halkanın alanı kaç cm²’dir?" % (r, R), pis(v), W3([pis((R - r) ** 2), pis(R * R + r * r), pis(2 * (R - r)), pis(R * R)], pis(v)),
                 "π(%d² − %d²) = <b>%s</b>." % (R, r, pis(v)))

    def tekerlek():
        r = ri(10, 50)
        n = ri(5, 100)
        v = F(2 * r * n)
        return M("Yarıçapı %d cm olan bir tekerlek %d tam tur dönüyor. Tekerlek kaç cm yol alır?" % (r, n), pis(v), W3([pis(r * n), pis(r * r * n), pis(v * 2), pis(v + 2 * r)], pis(v)),
                 "Bir turda çevre kadar: 2π · %d · %d = <b>%s cm</b>." % (r, n, pis(v)))

    sets = [("Dairenin alanı ve çevresi", [(daire, 20)]), ("Yay uzunluğu", [(yay, 20)]), ("Daire diliminin alanı", [(dilim, 20)]),
            ("Halka", [(halka, 20)]), ("Problemler", [(tekerlek, 20)])]
    return U(12, "cember-ve-daire-problemleri", "GS", "MAT.12.2.3", 9, "Çember ve Daire Problemleri: Yay Uzunluğu ve Daire Dilimi", "Çember ve Daire Problemleri",
             "Çember ve daire ile ilgili problemlerde çevre, alan, yay uzunluğu ve daire diliminin alanını hesaplar.",
             "dairenin alanı ve çemberin çevresi, yay uzunluğu, daire diliminin alanı, halkanın alanı, tekerlek problemleri",
             "Yay = 2πr · α ÷ 360", "Daire dilimi = πr² · α ÷ 360.", sets,
             ["Çemberin çevresi 2πr, dairenin alanı πr²’dir.",
              "α merkez açılı yayın uzunluğu 2πr · α ÷ 360, daire diliminin alanı πr² · α ÷ 360’tır.",
              "Aynı merkezli iki çember arasındaki halkanın alanı π(R² − r²)’dir."],
             [("r = 6, α = 60°", ["2π · 6 ÷ 6"], "Yay 2π"), ("r = 6, α = 60°", ["36π ÷ 6"], "Dilim 6π")],
             [["Yayda r² kullanmak", "Yay 2πr ile, alan πr² ile"], ["Halkada (R − r)² almak", "R² − r²"], ["Çapı yarıçap sanmak", "r = çap ÷ 2"]],
             [("π neden yaklaşık 3,14?", "Her çemberde çevrenin çapa oranı sabittir ve bu oran π’dir."), ("Radyanla yay?", "α radyan ise yay = r · α."),
              ("Nerede kullanılır?", "Tekerlek, dişli, pasta dilimi ve saat problemlerinde.")])


UNITS = [u1, u2, u3, u4, u5, u6, u7, u8, u9]
