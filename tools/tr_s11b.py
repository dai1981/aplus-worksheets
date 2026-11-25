# -*- coding: utf-8 -*-
"""Türkiye 11. sınıf (2026 DÖP)：MAT.11.3.2 trigonometrik denklemler、11.3.3–11.3.6 üstel ve logaritmik fonksiyonlar、11.3.7 bileşke、11.3.8 fonksiyonlarda dört işlem。"""
import math
from fractions import Fraction as F
from tr_lise import M, num, sn, par, lin, dq, MINUS, ri, ch, sh, nz, kurve, frs, TRIG, U, W3, poly, peval
from tr_s11a import pis, tval

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def setup(rnd):
    pass


def lg(b, x):
    """log₂ 8"""
    if str(b) == "10":
        return "log %s" % x
    return "log%s %s" % (str(b).translate(SUB), x)


def arg(a, sign=1):
    """x − a（a = 0 ise x）"""
    return "x" if a == 0 else "(%s)" % lin(1, "x", -a)


def pw(b, e):
    """2<sup>x+1</sup>"""
    return "%s<sup>%s</sup>" % (b, e)


# ============================================================ 8. trigonometrik denklemler
SOL = {}
for _d in [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]:
    for _f in ("sin", "cos", "tan"):
        _v = tval(_f, _d)
        SOL.setdefault((_f, _v), []).append(_d)
SOL = {k: v for k, v in SOL.items() if k[1] != "Tanımsız" and ("√" in k[1] or "fr" in k[1] or k[1] in ("0", "1", MINUS + "1"))}


def u8():
    def temel():
        (f, v), ds = ch(sorted(SOL.items()))
        g = ", ".join("%d°" % d for d in ds)
        alld = [d for (ff, vv), dd in SOL.items() for d in dd if ff == f]
        w = [", ".join("%d°" % d for d in sorted(sh(sorted(set(alld) - set(ds)))[:len(ds)])), ", ".join("%d°" % d for d in ds[:1]),
             ", ".join("%d°" % d for d in sorted((d + 180) % 360 for d in ds)), ", ".join("%d°" % d for d in sorted((360 - d) % 360 for d in ds))]
        return M("%s x = %s denkleminin [0°, 360°) aralığındaki çözümleri nelerdir?" % (f, v), g, W3(w, g),
                 "Referans açıyı bul, sonra %s işaretine göre bölgeleri seç: <b>%s</b>." % ({"sin": "sinüsün", "cos": "kosinüsün", "tan": "tanjantın"}[f], g))

    def katsayi():
        (f, v), ds = ch([kv for kv in sorted(SOL.items()) if kv[0][0] != "tan" and kv[0][1] in (frs(1, 2), MINUS + frs(1, 2), "0", "1", MINUS + "1")])
        val = {frs(1, 2): F(1, 2), MINUS + frs(1, 2): F(-1, 2), "0": F(0), "1": F(1), MINUS + "1": F(-1)}[v]
        a = ri(2, 9) * 2
        b = ri(-9, 9)
        c = a * val + b
        eq = "%s %s x %s = %s" % (sn(a), f, "+ %s" % sn(b) if b > 0 else "− %s" % sn(-b), sn(c)) if b else "%s %s x = %s" % (sn(a), f, sn(c))
        g = ", ".join("%d°" % d for d in ds)
        w = [", ".join("%d°" % d for d in sorted((d + 180) % 360 for d in ds)), ", ".join("%d°" % d for d in sorted((d + 90) % 360 for d in ds)), ", ".join("%d°" % d for d in ds[:1]), "Çözüm yoktur"]
        return M("%s denkleminin [0°, 360°) aralığındaki çözümleri nelerdir?" % eq, g, W3(w, g),
                 "%s x = %s bulunur; çözümler <b>%s</b>." % (f, v, g))

    def yok():
        f = ch(["sin", "cos"])
        a = ri(2, 9)
        k = ri(1, 9)
        c = a + k if ri(0, 1) else -a - k
        return M("%d %s x = %s denkleminin gerçek sayılarda kaç çözümü vardır?" % (a, f, sn(c)), "Çözümü yoktur", ["Bir çözümü vardır", "İki çözümü vardır", "Sonsuz çözümü vardır"],
                 "%s x = %s olur; ancak −1 ≤ %s x ≤ 1 olduğundan <b>çözümü yoktur</b>." % (f, sn(F(c, a)), f))

    def sayi():
        (f, v), ds = ch(sorted(SOL.items()))
        k = ri(1, 4)
        n = len(ds) * k
        return M("%s x = %s denkleminin [0°, %s°) aralığında kaç çözümü vardır?" % (f, v, num(360 * k)), num(n), W3([num(len(ds)), num(n + 1), num(n * 2), num(max(n - 1, 0))], num(n)),
                 "Her 360°’lik turda %d çözüm vardır; %d tur → <b>%d</b>." % (len(ds), k, n))

    def genel():
        f = ch(["sin", "cos", "tan"])
        a = ch([30, 45, 60])
        if f == "sin":
            g = "x = %d° + k · 360° veya x = %d° + k · 360°" % (a, 180 - a)
            w = ["x = %d° + k · 180°" % a, "x = %d° + k · 360° veya x = %d° + k · 360°" % (a, 360 - a), "x = %d° + k · 360°" % a]
        elif f == "cos":
            g = "x = %d° + k · 360° veya x = %d° + k · 360°" % (a, 360 - a)
            w = ["x = %d° + k · 180°" % a, "x = %d° + k · 360° veya x = %d° + k · 360°" % (a, 180 - a), "x = %d° + k · 360°" % a]
        else:
            g = "x = %d° + k · 180°" % a
            w = ["x = %d° + k · 360°" % a, "x = %d° + k · 360° veya x = %d° + k · 360°" % (a, 180 - a), "x = %d° + k · 90°" % a]
        return M("%s x = %s denkleminin genel çözümü hangisidir? (k ∈ ℤ)" % (f, TRIG[(f, a)]), g, W3(w, g),
                 "%s fonksiyonunun periyodu %s olduğundan <b>%s</b>." % (f, "180°" if f == "tan" else "360°", g))

    sets = [("Temel denklemler", [(temel, 15), (sayi, 5)]), ("Katsayılı denklemler", [(katsayi, 20)]), ("Çözüm sayısı", [(sayi, 16), (yok, 4)]),
            ("Genel çözüm", [(genel, 9), (yok, 11)]), ("Karışık", [(sayi, 10), (katsayi, 10)])]
    return U(11, "trigonometrik-denklemler", "N", "MAT.11.3.2", 8, "Trigonometrik Denklemler", "Trigonometrik Denklemler",
             "Trigonometrik denklemleri birim çember ve grafikler yardımıyla çözer; belirli bir aralıktaki çözümleri ve genel çözümü bulur.",
             "sin x = a, cos x = a, tan x = a biçimindeki denklemler, katsayılı denklemler, çözüm sayısı, çözümü olmayan denklemler, genel çözüm",
             "Önce referans açı, sonra bölge", "sin ve cos için −1 ≤ a ≤ 1 olmalı.", sets,
             ["sin x = a denkleminde önce referans açı bulunur; sinüs I. ve II. bölgede pozitif, III. ve IV. bölgede negatiftir.",
              "cos x = a için kosinüs I. ve IV. bölgede pozitiftir; tan x = a denkleminin çözümleri 180°’de bir tekrarlanır.",
              "|a| &gt; 1 ise sin x = a ve cos x = a denklemlerinin çözümü yoktur."],
             [("sin x = 1/2", ["Referans 30°", "I. ve II. bölge"], "30°, 150°"), ("2 cos x + 1 = 0", ["cos x = −1/2"], "120°, 240°")],
             [["Yalnızca bir çözüm yazmak", "Bir turda genelde iki çözüm var"], ["Bölge işaretini karıştırmak", "Kosinüs II. bölgede negatif"], ["sin x = 2 için çözüm aramak", "−1 ≤ sin x ≤ 1"]],
             [("tan x = a her zaman çözülür mü?", "Evet, tanjant bütün gerçek değerleri alır."), ("Radyanla nasıl yazılır?", "30° = π/6 gibi dönüştürülür; genel çözümde 2kπ kullanılır."),
              ("Grafikle nasıl görülür?", "y = sin x eğrisi ile y = a doğrusunun kesişim noktaları çözümlerdir.")])


# ============================================================ 9. üstel fonksiyon
def u9():
    def deger():
        b = ch([2, 3, 4, 5, 10, F(1, 2), F(1, 3)])
        k = ri(-6, 6)
        x = ri(-3, 4) if b in (2, 3, F(1, 2), F(1, 3)) else ri(-2, 3)
        v = F(b) ** x + k
        bs = sn(b) if F(b).denominator == 1 else "(%s)" % sn(b)
        return M("f(x) = %s için f(%s) kaçtır?" % (pw(bs, "x") + ((" + %s" % sn(k)) if k > 0 else (" − %s" % sn(-k)) if k < 0 else ""), sn(x)), sn(v),
                 W3([sn(F(b) * x + k), sn(F(b) ** (x + 1) + k), sn(F(b) ** (-x) + k), sn(v + 1)], sn(v)), "%s = %s → <b>%s</b>." % (pw(bs, par(x) if x < 0 else x), sn(F(b) ** x), sn(v)))

    def artan():
        b = ch([2, 3, 5, 7, 10, F(1, 2), F(1, 3), F(2, 3), F(3, 2), F(5, 4), F(4, 5), F(1, 10)])
        k = ri(-5, 5)
        g = "Artandır" if b > 1 else "Azalandır"
        bs = sn(b) if F(b).denominator == 1 else "(%s)" % sn(b)
        return M("f(x) = %s%s fonksiyonu artan mı, azalan mı?" % (pw(bs, "x"), (" + %s" % sn(k)) if k > 0 else (" − %s" % sn(-k)) if k < 0 else ""), g, ["Azalandır" if b > 1 else "Artandır", "Sabittir", "Önce azalan sonra artandır"],
                 "Taban %s olduğundan fonksiyon <b>%s</b>." % ("1’den büyük" if b > 1 else "0 ile 1 arasında", g.lower()))

    def goruntu():
        b = ch([2, 3, 4, 5, 10])
        k = ri(-9, 9)
        a = ch([1, -1])
        f = ("%s" if a == 1 else MINUS + "%s") % pw(b, "x") + ((" + %s" % sn(k)) if k > 0 else (" − %s" % sn(-k)) if k < 0 else "")
        g = "(%s, ∞)" % sn(k) if a == 1 else "(−∞, %s)" % sn(k)
        return M("f(x) = %s fonksiyonunun görüntü kümesi hangisidir?" % f, g, W3(["(%s, ∞)" % sn(k), "(−∞, %s)" % sn(k), "[%s, ∞)" % sn(k), "ℝ", "(0, ∞)"], g),
                 "%s her zaman pozitiftir; %s → <b>%s</b>." % (pw(b, "x"), "üstüne %s eklenir" % sn(k) if a == 1 else "işaret değişir ve %s eklenir" % sn(k), g))

    def kesim():
        b = ch([2, 3, 4, 5, 10])
        k = ri(-9, 9)
        c = ri(1, 5)
        f = "%s · %s" % (c, pw(b, "x")) if c > 1 else pw(b, "x")
        f += (" + %s" % sn(k)) if k > 0 else (" − %s" % sn(-k)) if k < 0 else ""
        g = "(0, %s)" % sn(c + k)
        return M("f(x) = %s fonksiyonunun grafiği y eksenini hangi noktada keser?" % f, g, W3(["(0, %s)" % sn(k), "(0, %s)" % sn(c * b + k), "(%s, 0)" % sn(c + k), "(0, %s)" % sn(c)], g),
                 "x = 0 için %s⁰ = 1 → f(0) = %s → <b>%s</b>." % (b, sn(c + k), g))

    def buyume():
        n0 = ri(1, 9) * 100
        t = ri(1, 6)
        T = ri(2, 12)
        k = ch(["iki katına çıkar", "yarıya iner"])
        v = n0 * 2 ** T // 1 if k == "iki katına çıkar" else F(n0, 2 ** T)
        if k == "yarıya iner" and F(v).denominator != 1:
            T = ri(1, 3)
            v = F(n0 * 8, 2 ** T)
            n0 = n0 * 8
        tt = t * T
        v = n0 * 2 ** T if k == "iki katına çıkar" else F(n0, 2 ** T)
        if F(v).denominator != 1:
            return None
        w = "bakteri" if k == "iki katına çıkar" else "gram radyoaktif madde"
        return M("Başlangıçta %s %s var. Bu miktar her %d saatte bir %s. %d saat sonra kaç %s olur?" % (num(n0), w, t, k, tt, w), num(v),
                 W3([num(n0 * 2 * T) if k == "iki katına çıkar" else num(n0 // (2 * T)) if n0 % (2 * T) == 0 else num(v * 2), num(n0 * 2 ** tt) if k == "iki katına çıkar" and n0 * 2 ** tt < 10 ** 9 else num(v * 4), num(v * 2), num(v // 2) if v % 2 == 0 else num(v + n0)], num(v)),
                 "%d saatte %d kez %s: %s · %s = <b>%s</b>." % (tt, T, k, num(n0), pw(2, T) if k == "iki katına çıkar" else pw(frs(1, 2) if False else "(1/2)", T), num(v)))

    sets = [("Değer bulma", [(deger, 20)]), ("Artan ve azalan", [(artan, 20)]), ("Görüntü kümesi", [(goruntu, 20)]),
            ("Eksenleri kesme", [(kesim, 20)]), ("Büyüme ve azalma problemleri", [(buyume, 20)])]
    return U(11, "ustel-fonksiyon", "N", "MAT.11.3.3", 9, "Üstel Fonksiyonlar", "Üstel Fonksiyon",
             "Üstel fonksiyonların grafiklerini ve nitel özelliklerini (artanlık, azalanlık, görüntü kümesi, eksenleri kesme) inceler; büyüme ve azalma problemlerini modeller.",
             "üstel fonksiyonun değeri, tabana göre artanlık ve azalanlık, görüntü kümesi, y eksenini kesme noktası, büyüme ve azalma problemleri",
             "f(x) = aˣ, a > 0 ve a ≠ 1", "a > 1 ise artan, 0 < a < 1 ise azalan.", sets,
             ["f(x) = aˣ (a &gt; 0, a ≠ 1) üstel fonksiyondur; aˣ her zaman pozitiftir ve f(0) = 1’dir.",
              "a &gt; 1 ise fonksiyon artan, 0 &lt; a &lt; 1 ise azalandır.",
              "Her eşit zaman aralığında aynı oranda değişen nicelikler (bakteri, faiz, radyoaktif madde) üstel fonksiyonla modellenir."],
             [("f(x) = 2ˣ + 3, f(2)", ["4 + 3"], "7"), ("100 bakteri, her saat 2 katı, 5 saat", ["100 · 2⁵"], "3.200")],
             [["aˣ’i a · x sanmak", "Üs tekrar eden çarpmadır"], ["Görüntü kümesine k’yi dâhil etmek", "aˣ hiçbir zaman 0 olmaz"], ["Negatif üssü negatif sayı sanmak", "2⁻¹ = 1/2"]],
             [("e sayısı nedir?", "Yaklaşık 2,718 olan, sürekli büyümede ortaya çıkan özel bir sayıdır."), ("Taban neden 1 olamaz?", "1ˣ her zaman 1 olur; fonksiyon sabit olur."),
              ("Üstel büyüme neden hızlıdır?", "Her adımda bir öncekinin katı kadar artar.")])


# ============================================================ 10. logaritma
def u10():
    def tanim():
        b = ch([2, 3, 4, 5, 6, 7, 10])
        n = ri(-3, 5)
        if b ** abs(n) > 100000:
            return None
        x = F(b) ** n
        xs = sn(x)
        return M("%s kaçtır?" % lg(b, xs), sn(n), W3([sn(n + 1), sn(-n) if n else "1", sn(F(x) / b) if x / b >= 1 else sn(n - 1), sn(n * b) if n * b != n else "2"], sn(n)),
                 "%s<sup>%s</sup> = %s olduğundan <b>%s</b>." % (b, sn(n), xs, sn(n)))

    def ozellik():
        b = ch([2, 3, 5, 10])
        p, q = ri(1, 4), ri(1, 4)
        k = ri(0, 2)
        x, y = b ** p, b ** q
        if k == 0:
            return M("%s + %s kaçtır?" % (lg(b, num(x * ri(1, 1))), lg(b, num(y))), sn(p + q), W3([sn(p * q), sn(p + q + 1), sn(abs(p - q)) if p != q else "1", sn(b ** (p + q))], sn(p + q)),
                     "log(xy) = log x + log y: %s = <b>%d</b>." % (lg(b, num(x * y)), p + q))
        if k == 1:
            z = ri(1, 3)
            return M("%s − %s kaçtır?" % (lg(b, num(x * b ** z)), lg(b, num(b ** z))), sn(p), W3([sn(p + 2 * z), sn(F(p + z, z)), sn(p + 1), sn(z)], sn(p)),
                     "log(x ÷ y) = log x − log y: %s = <b>%d</b>." % (lg(b, num(x)), p))
        m = ri(2, 5)
        return M("%s kaçtır?" % lg(b, pw(num(x), m) if x < 100 else "(%s)<sup>%d</sup>" % (num(x), m)), sn(p * m), W3([sn(p + m), sn(p), sn(m), sn(p * m + 1)], sn(p * m)),
                 "log xⁿ = n · log x: %d · %d = <b>%d</b>." % (m, p, p * m))

    def taban():
        b = ch([2, 3, 4, 8, 9, 16, 27, 25, 32])
        base = {2: 2, 4: 2, 8: 2, 16: 2, 32: 2, 3: 3, 9: 3, 27: 3, 25: 5}[b]
        e1 = round(math.log(b, base))
        e2 = ri(1, 6)
        x = base ** e2
        v = F(e2, e1)
        return M("%s kaçtır?" % lg(b, num(x)), sn(v), W3([sn(F(e1, e2)), sn(e2), sn(v + 1), sn(e2 * e1)], sn(v)),
                 "Taban değiştirme: %s ÷ %s = %d ÷ %d = <b>%s</b>." % (lg(base, num(x)), lg(base, num(b)), e2, e1, sn(v)))

    def onluk():
        n = ri(-4, 7)
        x = F(10) ** n
        xs = num(x) if n >= 0 else dq(x)
        return M("log %s kaçtır?" % xs, sn(n), W3([sn(n + 1), sn(-n) if n else "1", sn(n - 1), sn(10 * n) if n else "10"], sn(n)),
                 "log, 10 tabanında logaritmadır: 10<sup>%s</sup> = %s → <b>%s</b>." % (sn(n), xs, sn(n)))

    def us():
        b = ch([2, 3, 5, 7, 10])
        x = ri(2, 50)
        k = ri(0, 1)
        if k == 0:
            return M("%s<sup>%s</sup> kaçtır?" % (b, lg(b, x)), num(x), W3([num(b * x), num(x + b), num(b), num(x * x)], num(x)), "a<sup>logₐ x</sup> = x: <b>%d</b>." % x)
        m = ri(2, 3)
        return M("%s<sup>%d%s</sup> kaçtır?" % (b, m, " " + lg(b, x) if False else lg(b, x).join(["·", ""]) if False else " · " + lg(b, x)), num(x ** m), W3([num(x * m), num(b * x * m), num(x ** m + 1), num(x)], num(x ** m)),
                 "%d · %s = %s ve a<sup>logₐ y</sup> = y: %d<sup>%d</sup> = <b>%s</b>." % (m, lg(b, x), lg(b, "%d<sup>%d</sup>" % (x, m)), x, m, num(x ** m)))

    sets = [("Logaritmanın tanımı", [(tanim, 20)]), ("10 tabanında logaritma", [(onluk, 10), (tanim, 10)]), ("Logaritma özellikleri", [(ozellik, 20)]),
            ("Taban değiştirme", [(taban, 20)]), ("Üs ve logaritma", [(us, 20)])]
    return U(11, "logaritma", "N", "MAT.11.3.4", 10, "Logaritma ve Özellikleri", "Logaritma",
             "Üstel fonksiyonun tersi olarak logaritmayı tanımlar; logaritmanın özelliklerini kullanarak ifadelerin değerini bulur.",
             "logaritmanın tanımı, 10 tabanında logaritma, çarpım, bölüm ve üs özellikleri, taban değiştirme, a üzeri logₐ x",
             "logₐ x = y ⇔ aʸ = x", "log(xy) = log x + log y.", sets,
             ["logₐ x = y ise aʸ = x’tir (a &gt; 0, a ≠ 1, x &gt; 0). Logaritma, üssü bulma işlemidir.",
              "logₐ(xy) = logₐ x + logₐ y, logₐ(x ÷ y) = logₐ x − logₐ y, logₐ xⁿ = n · logₐ x.",
              "Taban değiştirme: logₐ x = log_b x ÷ log_b a. Ayrıca a<sup>logₐ x</sup> = x’tir."],
             [("log₂ 32", ["2⁵ = 32"], "5"), ("log₃ 54 − log₃ 2", ["log₃ 27"], "3")],
             [["log(x + y) = log x + log y sanmak", "Toplamın logaritması böyle ayrılmaz"], ["Tabanı ve üssü karıştırmak", "logₐ x’te a tabandır"], ["Negatif sayının logaritmasını almak", "x &gt; 0 olmalı"]],
             [("ln nedir?", "e tabanında logaritmadır."), ("Logaritma neden icat edildi?", "Büyük sayılarla çarpmayı toplamaya çevirerek hesabı kolaylaştırmak için."),
              ("Nerede kullanılır?", "Deprem büyüklüğü, ses şiddeti (desibel) ve pH ölçeğinde.")])


# ============================================================ 11. logaritmik fonksiyon
def u11():
    def tanim():
        b = ch([2, 3, 5, 10])
        a = ri(-6, 6)
        k = ri(0, 2)
        if k == 0:
            return M("f(x) = %s fonksiyonunun en geniş tanım kümesi hangisidir?" % lg(b, arg(a)), "(%s, ∞)" % sn(a), W3(["[%s, ∞)" % sn(a), "(%s, ∞)" % sn(-a) if a else "(1, ∞)", "ℝ", "(−∞, %s)" % sn(a)], "(%s, ∞)" % sn(a)),
                     "Logaritmanın içi pozitif olmalı: %s &gt; 0 → <b>(%s, ∞)</b>." % (arg(a).strip("()"), sn(a)))
        if k == 1:
            return M("f(x) = %s fonksiyonunun en geniş tanım kümesi hangisidir?" % lg(b, "(%s − x)" % sn(a)), "(−∞, %s)" % sn(a), W3(["(%s, ∞)" % sn(a), "(−∞, %s]" % sn(a), "ℝ", "(−∞, %s)" % sn(-a) if a else "(−∞, 1)"], "(−∞, %s)" % sn(a)),
                     "%s − x &gt; 0 → x &lt; %s: <b>(−∞, %s)</b>." % (sn(a), sn(a), sn(a)))
        c = ri(1, 7)
        return M("f(x) = %s fonksiyonunun en geniş tanım kümesi hangisidir?" % lg(b, "(x² − %d)" % (c * c)), "(−∞, %s) ∪ (%d, ∞)" % (sn(-c), c),
                 W3(["(%s, %d)" % (sn(-c), c), "(%d, ∞)" % c, "ℝ − {%s, %d}" % (sn(-c), c), "(%d, ∞)" % (c * c)], "(−∞, %s) ∪ (%d, ∞)" % (sn(-c), c)), "x² − %d &gt; 0 → x &lt; %s veya x &gt; %d." % (c * c, sn(-c), c))

    def ters():
        b = ch([2, 3, 4, 5, 10])
        k = ri(-6, 6)
        kk = ri(0, 1)
        if kk == 0:
            f = pw(b, "x") + ((" + %s" % sn(k)) if k > 0 else (" − %s" % sn(-k)) if k < 0 else "")
            g = "f⁻¹(x) = " + lg(b, "(%s)" % lin(1, "x", -k)) if k else "f⁻¹(x) = " + lg(b, "x")
            w = ["f⁻¹(x) = " + lg(b, "x") + ((" − %s" % sn(k)) if k > 0 else (" + %s" % sn(-k))) if k else "f⁻¹(x) = " + lg("x", b),
                 "f⁻¹(x) = " + lg(b, "(%s)" % lin(1, "x", k)) if k else "f⁻¹(x) = %s<sup>x</sup>" % b, "f⁻¹(x) = " + pw("x", b) + ((" − %s" % sn(k)) if k > 0 else (" + %s" % sn(-k)) if k else "")]
            return M("f(x) = %s fonksiyonunun tersi hangisidir?" % f, g, W3(w, g), "y = %s → %s = y %s → x = %s; <b>%s</b>." % (f, pw(b, "x"), ("− %s" % sn(k)) if k >= 0 else "+ %s" % sn(-k), lg(b, "(y %s)" % (("− %s" % sn(k)) if k >= 0 else "+ %s" % sn(-k))), g))
        f = lg(b, "x") + ((" + %s" % sn(k)) if k > 0 else (" − %s" % sn(-k)) if k < 0 else "")
        g = "f⁻¹(x) = " + pw(b, lin(1, "x", -k))
        w = ["f⁻¹(x) = " + pw(b, lin(1, "x", k)), "f⁻¹(x) = " + pw(b, "x") + ((" − %s" % sn(k)) if k > 0 else (" + %s" % sn(-k)) if k else " + 1"), "f⁻¹(x) = " + pw("x", b), "f⁻¹(x) = " + lg("x", b)]
        return M("f(x) = %s fonksiyonunun tersi hangisidir?" % f, g, W3(w, g), "y = %s → %s = y %s → x = %s: <b>%s</b>." % (f, lg(b, "x"), ("− %s" % sn(k)) if k >= 0 else "+ %s" % sn(-k), pw(b, "y " + (("− %s" % sn(k)) if k >= 0 else "+ %s" % sn(-k))), g))

    def deger():
        b = ch([2, 3, 5])
        a = ri(-5, 5)
        k = ri(-6, 6)
        n = ri(0, 5)
        x = b ** n + a
        v = n + k
        f = lg(b, arg(a)) + ((" + %s" % sn(k)) if k > 0 else (" − %s" % sn(-k)) if k < 0 else "")
        return M("f(x) = %s için f(%s) kaçtır?" % (f, sn(x)), sn(v), W3([sn(n), sn(v + 1), sn(v - 1), sn(b ** n + k)], sn(v)),
                 "%s = %d → %d %s %s = <b>%s</b>." % (lg(b, num(b ** n)), n, n, "+" if k >= 0 else "−", sn(abs(k)), sn(v)))

    def artan():
        b = ch([2, 3, 10, 5, 7, F(1, 2), F(1, 3), F(1, 10), F(2, 5), F(3, 4)])
        bs = sn(b) if F(b).denominator == 1 else "%d/%d" % (F(b).numerator, F(b).denominator)
        g = "Artandır" if b > 1 else "Azalandır"
        return M("f(x) = %s fonksiyonu (0, ∞) aralığında artan mı, azalan mı?" % lg(bs, "x") if F(b).denominator == 1 else
                 "f(x) = log<sub>%s</sub> x fonksiyonu (0, ∞) aralığında artan mı, azalan mı?" % bs, g, ["Azalandır" if b > 1 else "Artandır", "Sabittir", "Önce artan sonra azalandır"],
                 "Taban %s: <b>%s</b>." % ("1’den büyük" if b > 1 else "0 ile 1 arasında", g.lower()))

    def kesim():
        b = ch([2, 3, 5, 10])
        k = ri(-4, 4)
        x0 = F(b) ** (-k)
        g = "(%s, 0)" % sn(x0)
        f = lg(b, "x") + ((" + %s" % sn(k)) if k > 0 else (" − %s" % sn(-k)) if k < 0 else "")
        return M("f(x) = %s fonksiyonunun grafiği x eksenini hangi noktada keser?" % f, g, W3(["(%s, 0)" % sn(F(b) ** k), "(1, 0)", "(0, %s)" % sn(k), "(%s, 0)" % sn(-k) if k else "(%s, 0)" % sn(b)], g),
                 "f(x) = 0 → %s = %s → x = %s: <b>%s</b>." % (lg(b, "x"), sn(-k), pw(b, par(-k) if k > 0 else sn(-k)), g))

    sets = [("Tanım kümesi", [(tanim, 20)]), ("Değer bulma", [(deger, 20)]), ("Ters fonksiyon", [(ters, 20)]),
            ("Artan ve azalan", [(artan, 10), (kesim, 10)]), ("Eksenleri kesme", [(kesim, 10), (deger, 10)])]
    return U(11, "logaritmik-fonksiyon", "N", "MAT.11.3.5", 11, "Logaritmik Fonksiyonlar", "Logaritmik Fonksiyon",
             "Logaritmik fonksiyonları üstel fonksiyonların tersi olarak inceler; tanım kümesi, artanlık, eksenleri kesme gibi özelliklerini yorumlar.",
             "en geniş tanım kümesi, değer bulma, üstel ve logaritmik fonksiyonların tersi, tabana göre artanlık, x eksenini kesme noktası",
             "logₐ x, aˣ’in tersidir", "Logaritmanın içi pozitif olmalıdır.", sets,
             ["f(x) = logₐ x, g(x) = aˣ fonksiyonunun tersidir; grafikleri y = x doğrusuna göre simetriktir.",
              "Logaritmanın içi pozitif olmalıdır; bu yüzden tanım kümesi içi pozitif yapan x’lerdir.",
              "a &gt; 1 ise logₐ x artan, 0 &lt; a &lt; 1 ise azalandır. logₐ 1 = 0 olduğundan grafik (1, 0) noktasından geçer."],
             [("log₂(x − 3)", ["x − 3 &gt; 0"], "(3, ∞)"), ("f(x) = 2ˣ − 1", ["y + 1 = 2ˣ"], "f⁻¹(x) = log₂(x + 1)")],
             [["Tanım kümesinde ≥ kullanmak", "İç pozitif: &gt;"], ["Tersi alırken k’nin işaretini korumak", "Ters işlemde işaret değişir"], ["log grafiğinin y eksenini kestiğini sanmak", "x = 0’da tanımsızdır"]],
             [("Logaritmik büyüme nasıldır?", "Çok yavaştır; x 10 katına çıkınca log x yalnızca 1 artar."), ("ln x’in tabanı nedir?", "e sayısıdır."),
              ("Grafik neden y eksenine yaklaşır?", "x 0’a yaklaştıkça logₐ x çok büyük negatif değerler alır.")])


# ============================================================ 12. üstel ve logaritmik denklemler
def u12():
    def ustel():
        b = ch([2, 3, 5])
        a, c = ri(1, 3), ri(-4, 4)
        n = ri(1, 5)
        x = F(n - c, a)
        if x.denominator != 1:
            return None
        return M("%s = %s denkleminin çözümü nedir?" % (pw(b, lin(a, "x", c)), num(b ** n)), "x = %s" % sn(x), W3(["x = %s" % sn(F(n + c, a)), "x = %s" % sn(n), "x = %s" % sn(x + 1), "x = %s" % sn(F(b ** n - c, a)) if F(b ** n - c, a).denominator == 1 else "x = %s" % sn(x - 1)], "x = %s" % sn(x)),
                 "%s = %s → %s = %d → <b>x = %s</b>." % (num(b ** n), pw(b, n), lin(a, "x", c), n, sn(x)))

    def ortak():
        p = ch([(2, 4), (2, 8), (3, 9), (3, 27), (4, 8), (9, 27), (2, 16), (5, 25)])
        b1, b2 = p
        base = {2: 2, 4: 2, 8: 2, 16: 2, 3: 3, 9: 3, 27: 3, 5: 5, 25: 5}
        e1, e2 = round(math.log(b1, base[b1])), round(math.log(b2, base[b2]))
        c = ri(-3, 3)
        # b1^(x) = b2^(x + c) → e1 x = e2 (x + c) → x = e2 c ÷ (e1 − e2)
        if e1 == e2:
            return None
        x = F(e2 * c, e1 - e2)
        if c == 0:
            return None
        return M("%s = %s denkleminin çözümü nedir?" % (pw(b1, "x"), pw(b2, lin(1, "x", c))), "x = %s" % sn(x), W3(["x = %s" % sn(-x), "x = %s" % sn(c), "x = %s" % sn(x + 1), "x = %s" % sn(F(e1 * c, e2 - e1))], "x = %s" % sn(x)),
                 "Tabanları %d yaparız: %d<sup>%s</sup> = %d<sup>%s</sup> → x = <b>%s</b>." % (base[b1], base[b1], lin(e1, "x"), base[b1], lin(e2, "x", e2 * c), sn(x)))

    def loglu():
        b = ch([2, 3, 5, 10])
        a = ri(-6, 6)
        n = ri(0, 4)
        x = b ** n + a
        return M("%s = %d denkleminin çözümü nedir?" % (lg(b, arg(a)), n), "x = %s" % sn(x), W3(["x = %s" % sn(b ** n - a), "x = %s" % sn(b * n + a), "x = %s" % sn(n + a), "x = %s" % sn(x + 1)], "x = %s" % sn(x)),
                 "%s = %s → <b>x = %s</b>." % (arg(a).strip("()"), pw(b, n), sn(x)))

    def toplam():
        b = ch([2, 3, 10])
        d = ri(1, 9)
        r = ri(d + 1, d + 12)
        n_ = r * (r - d)
        n = round(math.log(n_, b))
        if b ** n != n_:
            return None
        return M("%s + %s = %d denkleminin çözümü nedir?" % (lg(b, "x"), lg(b, "(x − %d)" % d), n), "x = %d" % r, W3(["x = %s" % sn(d - r), "x = %d" % (r - d), "x = %d" % (r + 1), "x = %d ve x = %s" % (r, sn(d - r))], "x = %d" % r),
                 "%s = %d → x² − %dx − %d = 0 → x = %d veya x = %s; x − %d &gt; 0 olmalı: <b>x = %d</b>." % (lg(b, "[x(x − %d)]" % d), n, d, n_, r, sn(d - r), d, r))

    def esitsizlik():
        b = ch([2, 3, 5])
        n = ri(1, 5)
        k = ch([">", "<"])
        g = "x %s %d" % ("&gt;" if k == ">" else "&lt;", n)
        return M("%s %s %s eşitsizliğinin çözüm kümesi hangisidir?" % (pw(b, "x"), "&gt;" if k == ">" else "&lt;", num(b ** n)), g, W3(["x %s %d" % ("&lt;" if k == ">" else "&gt;", n), "x %s %s" % ("&gt;" if k == ">" else "&lt;", num(b ** n)), "x %s %d" % ("&gt;" if k == ">" else "&lt;", n + 1)], g),
                 "Taban 1’den büyük olduğundan yön korunur: %s %s %s → <b>%s</b>." % (pw(b, "x"), "&gt;" if k == ">" else "&lt;", pw(b, n), g))

    def problem():
        n0 = ri(1, 9) * 1000
        T = ri(2, 10)
        k = ri(2, 6)
        return M("Bir şehrin nüfusu her %d yılda bir 2 katına çıkıyor ve bugün %s. Nüfus kaç yıl sonra %s olur?" % (T, num(n0), num(n0 * 2 ** k)), "%d yıl" % (k * T),
                 W3(["%d yıl" % k, "%d yıl" % (2 ** k), "%d yıl" % ((k + 1) * T), "%d yıl" % (k * T // 2) if k * T % 2 == 0 else "%d yıl" % (k * T + 1)], "%d yıl" % (k * T)),
                 "%s · 2<sup>t/%d</sup> = %s → 2<sup>t/%d</sup> = %d = 2<sup>%d</sup> → t = <b>%d yıl</b>." % (num(n0), T, num(n0 * 2 ** k), T, 2 ** k, k, k * T))

    sets = [("Üstel denklemler", [(ustel, 20)]), ("Tabanları eşitleme", [(ortak, 12), (ustel, 8)]), ("Logaritmik denklemler", [(loglu, 20)]),
            ("Özelliklerle çözme", [(toplam, 10), (esitsizlik, 10)]), ("Problemler", [(problem, 20)])]
    return U(11, "ustel-ve-logaritmik-denklemler", "N", "MAT.11.3.6", 12, "Üstel ve Logaritmik Denklemler ve Eşitsizlikler", "Üstel ve Logaritmik Denklemler",
             "Üstel ve logaritmik fonksiyonlarla ifade edilen denklem ve eşitsizlikleri çözer; gerçek yaşam problemlerini modeller.",
             "üstel denklemler, tabanları eşitleme, logaritmik denklemler, logaritma özellikleriyle çözme, üstel eşitsizlikler, nüfus problemleri",
             "Tabanları eşitle, üsleri eşitle", "Logaritmik denklemde çözümü tanım kümesiyle kontrol et.", sets,
             ["aᵐ = aⁿ ise m = n’dir; bu yüzden üstel denklemlerde tabanlar eşitlenir.",
              "logₐ f(x) = n denklemi f(x) = aⁿ biçimine çevrilir; bulunan çözümün logaritmanın içini pozitif yapması gerekir.",
              "a &gt; 1 ise aˣ &gt; aⁿ eşitsizliği x &gt; n olur; 0 &lt; a &lt; 1 ise yön değişir."],
             [("2ˣ⁺¹ = 32", ["2⁵", "x + 1 = 5"], "x = 4"), ("log₂(x − 1) = 3", ["x − 1 = 8"], "x = 9")],
             [["Tabanları eşitlemeden üsleri eşitlemek", "Önce aynı taban"], ["Negatif çözümü kontrol etmemek", "Logaritmanın içi pozitif olmalı"], ["Eşitsizlikte tabanı kontrol etmemek", "0 &lt; a &lt; 1 ise yön değişir"]],
             [("Taban eşitlenemezse?", "Her iki tarafın logaritması alınır."), ("Yarı ömür nedir?", "Bir maddenin yarısının bozunması için geçen süredir."),
              ("Neden iki çözümden biri atılır?", "Logaritmanın içini negatif yapan çözüm tanım kümesinde değildir.")])


# ============================================================ 13. bileşke fonksiyon
def u13():
    def deger():
        a, b, c, d = nz(-5, 5), ri(-9, 9), nz(-5, 5), ri(-9, 9)
        x = ri(-5, 5)
        k = ri(0, 1)
        if k == 0:
            v = a * (c * x + d) + b
            return M("f(x) = %s ve g(x) = %s ise (f ∘ g)(%s) kaçtır?" % (lin(a, "x", b), lin(c, "x", d), sn(x)), sn(v), W3([sn(c * (a * x + b) + d), sn((a * x + b) * (c * x + d)), sn(a * x + b + c * x + d), sn(v + 1)], sn(v)),
                     "Önce g(%s) = %s, sonra f(%s) = <b>%s</b>." % (sn(x), sn(c * x + d), sn(c * x + d), sn(v)))
        v = c * (a * x + b) + d
        return M("f(x) = %s ve g(x) = %s ise (g ∘ f)(%s) kaçtır?" % (lin(a, "x", b), lin(c, "x", d), sn(x)), sn(v), W3([sn(a * (c * x + d) + b), sn((a * x + b) * (c * x + d)), sn(v - 1), sn(v + a)], sn(v)),
                 "Önce f(%s) = %s, sonra g(%s) = <b>%s</b>." % (sn(x), sn(a * x + b), sn(a * x + b), sn(v)))

    def kural():
        a, b, c, d = nz(-5, 5), ri(-9, 9), nz(-5, 5), ri(-9, 9)
        g_ = "(f ∘ g)(x) = %s" % lin(a * c, "x", a * d + b)
        w = ["(f ∘ g)(x) = %s" % lin(a * c, "x", c * b + d), "(f ∘ g)(x) = %s" % lin(a + c, "x", b + d), "(f ∘ g)(x) = %s" % lin(a * c, "x", b * d), "(f ∘ g)(x) = %s" % lin(a * c, "x", a * d - b)]
        return M("f(x) = %s ve g(x) = %s ise (f ∘ g)(x) hangisidir?" % (lin(a, "x", b), lin(c, "x", d)), g_, W3(w, g_),
                 "f(g(x)) = %s(%s) %s = <b>%s</b>." % (sn(a) if a not in (1, -1) else ("" if a == 1 else MINUS), lin(c, "x", d), ("+ %s" % sn(b)) if b >= 0 else "− %s" % sn(-b), lin(a * c, "x", a * d + b)))

    def kare():
        a, b = ri(-4, 4), ri(-5, 5)
        c = nz(-3, 3)
        x = ri(-4, 4)
        gx = c * x + a
        v = gx * gx + b
        return M("f(x) = x²%s ve g(x) = %s ise f(g(%s)) kaçtır?" % ((" + %s" % sn(b)) if b > 0 else (" − %s" % sn(-b)) if b < 0 else "", lin(c, "x", a), sn(x)), sn(v),
                 W3([sn(c * (x * x + b) + a), sn(gx * 2 + b), sn(v + 1), sn(gx + b)], sn(v)), "g(%s) = %s; f(%s) = %s² %s = <b>%s</b>." % (sn(x), sn(gx), sn(gx), par(gx), ("+ %s" % sn(b)) if b >= 0 else "− %s" % sn(-b), sn(v)))

    def tablo():
        xs = list(range(1, 6))
        fv = sh(list(range(1, 6)))
        gv = sh(list(range(1, 6)))
        x = ri(1, 5)
        k = ri(0, 1)
        t = "<table class='sn-table' style='width:auto'><tbody><tr><td>x</td>%s</tr><tr><td>f(x)</td>%s</tr><tr><td>g(x)</td>%s</tr></tbody></table>" % ("".join("<td>%d</td>" % i for i in xs), "".join("<td>%d</td>" % i for i in fv), "".join("<td>%d</td>" % i for i in gv))
        if k == 0:
            v = fv[gv[x - 1] - 1]
            return M("Tabloya göre (f ∘ g)(%d) kaçtır?%s" % (x, t), num(v), W3([num(gv[fv[x - 1] - 1]), num(fv[x - 1]), num(gv[x - 1])] + [num(i) for i in xs], num(v)),
                     "g(%d) = %d, f(%d) = <b>%d</b>." % (x, gv[x - 1], gv[x - 1], v))
        v = gv[fv[x - 1] - 1]
        return M("Tabloya göre (g ∘ f)(%d) kaçtır?%s" % (x, t), num(v), W3([num(fv[gv[x - 1] - 1]), num(fv[x - 1]), num(gv[x - 1])] + [num(i) for i in xs], num(v)),
                 "f(%d) = %d, g(%d) = <b>%d</b>." % (x, fv[x - 1], fv[x - 1], v))

    def bilinmeyen():
        a, b, c = nz(-4, 4), ri(-9, 9), ri(-9, 9)
        # f(x) = ax + b, (f∘g)(x) = a(gx) + b = px + q; g(x) = mx + n
        m, n = nz(-4, 4), ri(-6, 6)
        p, q = a * m, a * n + b
        g_ = "g(x) = %s" % lin(m, "x", n)
        return M("f(x) = %s ve (f ∘ g)(x) = %s ise g(x) hangisidir?" % (lin(a, "x", b), lin(p, "x", q)), g_,
                 W3(["g(x) = %s" % lin(p, "x", q - b), "g(x) = %s" % lin(m, "x", q), "g(x) = %s" % lin(-m, "x", n), "g(x) = %s" % lin(m, "x", n + 1)], g_),
                 "%s · g(x)%s = %s → g(x) = <b>%s</b>." % (sn(a), (" + %s" % sn(b)) if b > 0 else (" − %s" % sn(-b)) if b < 0 else "", lin(p, "x", q), lin(m, "x", n)))

    sets = [("Bileşkenin değeri", [(deger, 20)]), ("Tablodan bileşke", [(tablo, 20)]), ("Bileşkenin kuralı", [(kural, 20)]),
            ("Karesel fonksiyonla bileşke", [(kare, 20)]), ("Bilinmeyen fonksiyon", [(bilinmeyen, 20)])]
    return U(11, "bileske-fonksiyon", "N", "MAT.11.3.7", 13, "Bileşke Fonksiyon", "Bileşke Fonksiyon",
             "İki fonksiyonun bileşkesini oluşturur; bileşke fonksiyonun değerini ve kuralını bulur, bileşkenin değişme özelliğinin olmadığını gösterir.",
             "bileşkenin değeri, tablodan bileşke, bileşkenin kuralı, karesel fonksiyonla bileşke, bileşkeden bilinmeyen fonksiyonu bulma",
             "(f ∘ g)(x) = f(g(x))", "Önce sağdaki g, sonra f uygulanır.", sets,
             ["(f ∘ g)(x) = f(g(x)): önce g uygulanır, çıkan sonuç f’ye girdi olur.",
              "Genelde f ∘ g ≠ g ∘ f’dir; bileşke işleminin değişme özelliği yoktur.",
              "Kuralı bulmak için f’nin kuralında x yerine g(x) ifadesinin tamamı yazılır."],
             [("f(x) = 2x + 1, g(x) = x − 3, (f ∘ g)(5)", ["g(5) = 2", "f(2) = 5"], "5"), ("(f ∘ g)(x)", ["2(x − 3) + 1"], "2x − 5")],
             [["Önce f’yi uygulamak", "f ∘ g’de önce g"], ["Bileşkeyi çarpım sanmak", "f ∘ g ≠ f · g"], ["x yerine g(x) yazarken parantezi unutmak", "Bütün ifadeyi parantezle yaz"]],
             [("f ∘ f⁻¹ nedir?", "Birim fonksiyon: (f ∘ f⁻¹)(x) = x."), ("Bileşke nerede kullanılır?", "Bir işlemin sonucunun başka bir işleme girdiği durumlarda, örneğin indirim sonrası vergi."),
              ("Bileşke birleşmeli midir?", "Evet: (f ∘ g) ∘ h = f ∘ (g ∘ h).")])


# ============================================================ 14. fonksiyonlarda dört işlem
def u14():
    def toplam():
        f = [nz(-3, 3), ri(-6, 6), ri(-9, 9)]
        g = [ri(-3, 3), ri(-6, 6), ri(-9, 9)]
        op = ch(["+", "−"])
        h = [x + y if op == "+" else x - y for x, y in zip(f, g)]
        if h[0] == 0:
            return None
        gg = "(f %s g)(x) = %s" % (op, poly(h))
        w = ["(f %s g)(x) = %s" % (op, poly([x - y if op == "+" else x + y for x, y in zip(f, g)])), "(f %s g)(x) = %s" % (op, poly([h[0], h[1], -h[2]]) if h[2] else poly([h[0], -h[1], h[2]])),
             "(f %s g)(x) = %s" % (op, poly([h[0], h[1] + 1, h[2]])), "(f %s g)(x) = %s" % (op, poly([-h[0], h[1], h[2]]))]
        return M("f(x) = %s ve g(x) = %s ise (f %s g)(x) hangisidir?" % (poly(f), poly(g), op), gg, W3(w, gg), "Benzer terimler %s: <b>%s</b>." % ("toplanır" if op == "+" else "çıkarılır", poly(h)))

    def deger():
        a, b, c, d = nz(-5, 5), ri(-9, 9), nz(-5, 5), ri(-9, 9)
        x = ri(-5, 5)
        op = ch(["+", "−", "·"])
        fx, gx = a * x + b, c * x + d
        v = fx + gx if op == "+" else fx - gx if op == "−" else fx * gx
        return M("f(x) = %s ve g(x) = %s ise (f %s g)(%s) kaçtır?" % (lin(a, "x", b), lin(c, "x", d), op, sn(x)), sn(v), W3([sn(fx + gx), sn(fx - gx), sn(fx * gx), sn(a * (c * x + d) + b), sn(v + 1)], sn(v)),
                 "f(%s) = %s, g(%s) = %s → <b>%s</b>." % (sn(x), sn(fx), sn(x), sn(gx), sn(v)))

    def bolum():
        a, b = nz(-5, 5), ri(-9, 9)
        r = ri(-7, 7)
        g_ = "ℝ − {%s}" % sn(r)
        return M("f(x) = %s ve g(x) = %s ise (f ÷ g)(x) fonksiyonunun en geniş tanım kümesi hangisidir?" % (lin(a, "x", b), lin(1, "x", -r)), g_,
                 W3(["ℝ − {%s}" % sn(-r) if r else "ℝ − {1}", "ℝ", "ℝ − {%s}" % sn(F(-b, a)), "ℝ − {%s, %s}" % (sn(r), sn(F(-b, a))) if F(-b, a) != r else "(%s, ∞)" % sn(r)], g_),
                 "Paydadaki g(x) sıfır olamaz: %s = 0 → x = %s: <b>%s</b>." % (lin(1, "x", -r), sn(r), g_))

    def carpim():
        a, b, c, d = nz(-4, 4), ri(-6, 6), nz(-4, 4), ri(-6, 6)
        h = [a * c, a * d + b * c, b * d]
        g_ = "(f · g)(x) = %s" % poly(h)
        w = ["(f · g)(x) = %s" % poly([a * c, a * d + b * c, -b * d]) if b * d else "(f · g)(x) = %s" % poly([a * c, -(a * d + b * c), b * d]),
             "(f · g)(x) = %s" % poly([a * c, b * d]), "(f · g)(x) = %s" % poly([a * c, a * d - b * c, b * d]), "(f · g)(x) = %s" % poly([a + c, b + d])]
        return M("f(x) = %s ve g(x) = %s ise (f · g)(x) hangisidir?" % (lin(a, "x", b), lin(c, "x", d)), g_, W3(w, g_), "(%s)(%s) = <b>%s</b>." % (lin(a, "x", b), lin(c, "x", d), poly(h)))

    def katsayi():
        a, b = nz(-5, 5), ri(-9, 9)
        k = nz(-6, 6)
        x = ri(-5, 5)
        v = k * (a * x + b)
        return M("f(x) = %s ise (%s · f)(%s) kaçtır?" % (lin(a, "x", b), sn(k), sn(x)), sn(v), W3([sn(a * k * x + b), sn(a * x + b + k), sn(a * (k * x) + b), sn(v + k)], sn(v)),
                 "%s · f(%s) = %s · %s = <b>%s</b>." % (sn(k), sn(x), sn(k), par(a * x + b), sn(v)))

    sets = [("İşlem sonucunun değeri", [(deger, 20)]), ("Toplama ve çıkarma", [(toplam, 20)]), ("Çarpma", [(carpim, 20)]),
            ("Bölme ve tanım kümesi", [(bolum, 20)]), ("Sabitle çarpma", [(katsayi, 20)])]
    return U(11, "fonksiyonlarda-dort-islem", "N", "MAT.11.3.8", 14, "Fonksiyonlarda Dört İşlem", "Fonksiyonlarda Dört İşlem",
             "Fonksiyonlarla toplama, çıkarma, çarpma ve bölme işlemlerini yapar; işlem sonucunda oluşan fonksiyonun tanım kümesini belirler.",
             "işlem sonucunun değeri, fonksiyonlarla toplama ve çıkarma, çarpma, bölme ve tanım kümesi, sabitle çarpma",
             "(f + g)(x) = f(x) + g(x)", "f ÷ g’de g(x) = 0 yapan değerler çıkarılır.", sets,
             ["(f + g)(x) = f(x) + g(x), (f − g)(x) = f(x) − g(x), (f · g)(x) = f(x) · g(x).",
              "(f ÷ g)(x) = f(x) ÷ g(x)’tir ve g(x) = 0 yapan x değerleri tanım kümesinden çıkarılır.",
              "İşlemin tanım kümesi f ve g’nin tanım kümelerinin kesişimidir."],
             [("f(x) = 2x + 1, g(x) = x − 3, (f + g)(x)", ["2x + 1 + x − 3"], "3x − 2"), ("(f · g)(2)", ["f(2) = 5, g(2) = −1"], "−5")],
             [["Çıkarmada g’nin bütün terimlerinin işaretini değiştirmemek", "f − g = f + (−g)"], ["f · g’yi bileşkeyle karıştırmak", "Çarpım: f(x) · g(x)"], ["Bölmede tanım kümesini kontrol etmemek", "g(x) ≠ 0"]],
             [("Gelir ve gider nasıl birleşir?", "Kâr fonksiyonu K(x) = G(x) − C(x) olarak yazılır."), ("(f + g) grafiği nasıl çizilir?", "Her x için iki fonksiyonun y değerleri toplanır."),
              ("f ÷ g ne zaman tanımsız?", "g(x) = 0 olduğunda.")])


UNITS = [u8, u9, u10, u11, u12, u13, u14]
