# -*- coding: utf-8 -*-
"""Türkiye 10. sınıf (2026 DÖP)：MAT.10.4 fonksiyonlar（karesel, karekök, rasyonel, ters）、MAT.10.5 sayma ve algoritma、MAT.10.6 analitik inceleme、MAT.10.7 koşullu olasılık ve Bayes。"""
import math
from fractions import Fraction as F
from tr_lise import dq, cap, M, num, sn, par, lin, MINUS, ri, ch, sh, nz, kosy, kurve, figure, U, W3, rts, rt, poly, peval, nCr, nPr, iv


def setup(rnd):
    pass


def code(lines):
    return "<span class='code'>%s</span>" % "<br>".join(l.replace("  ", "&nbsp;&nbsp;") for l in lines)


def pt(x, y):
    return "(%s, %s)" % (sn(x), sn(y))


def vform(a, r, k):
    """a(x − r)² + k"""
    inner = "x" if r == 0 else "(x %s %s)" % ("−" if r > 0 else "+", sn(abs(r)))
    s = ("" if a == 1 else MINUS if a == -1 else sn(a)) + (inner + "²")
    if k:
        s += (" + %s" % sn(k)) if k > 0 else (" − %s" % sn(-k))
    return s


def pct(p):
    return "%" + num(p)


# ============================================================ 11. karesel fonksiyon
def u11():
    def tepe():
        a, r, k = nz(-3, 3), ri(-5, 5), ri(-6, 6)
        cs = [a, -2 * a * r, a * r * r + k]
        g = pt(r, k)
        return M("f(x) = %s fonksiyonunun grafiğinin tepe noktası hangisidir?" % poly(cs), g, W3([pt(-r, k), pt(k, r), pt(r, -k), pt(-r, -k)], g)[:3] if r or k else [pt(1, 0), pt(0, 1), pt(-1, 0)],
                 "r = −b ÷ 2a = %s, k = f(%s) = %s → T<b>%s</b>." % (sn(r), sn(r), sn(k), g))

    def kok():
        p, q = ri(-7, 7), ri(-7, 7)
        if p >= q:
            return None
        a = ch([1, 1, -1, 2])
        cs = [a, -a * (p + q), a * p * q]
        g = "%s ve %s" % (sn(p), sn(q))
        return M("f(x) = %s fonksiyonunun grafiği x eksenini hangi noktalarda keser? (apsisler)" % poly(cs), g, W3(["%s ve %s" % (sn(-q), sn(-p)), "%s ve %s" % (sn(p * q), sn(p + q)) if p * q < p + q else "%s ve %s" % (sn(p + q), sn(p * q)), "%s ve %s" % (sn(p), sn(-q))], g),
                 "f(x) = 0 → %s(x %s)(x %s) = 0 → x = <b>%s</b>." % ("" if a == 1 else sn(a), "−" if p >= 0 else "+", sn(abs(p)), sn(abs(q)) if False else ("− %s" % sn(q) if q >= 0 else "+ %s" % sn(-q)), g) if False else
                 "f(x) = 0 denklemini çarpanlara ayırarak çözeriz: x = <b>%s</b>." % g)

    def grafik():
        a, r, k = ch([1, -1]), ri(-3, 3), ri(-4, 4)
        f = lambda x: a * (x - r) ** 2 + k
        p = kurve([(f, "#c0392b", "")], (-6, 6, 1), (-6, 6, 1), label="bir parabolün grafiği")
        g = vform(a, r, k)
        return M("Grafiği verilen parabol hangi fonksiyona aittir?%s" % p, "f(x) = " + g, ["f(x) = " + vform(a, -r, k) if r else "f(x) = " + vform(a, 1, k), "f(x) = " + vform(-a, r, k), "f(x) = " + vform(a, r, -k) if k else "f(x) = " + vform(a, r, 2)],
                 "Tepe noktası %s ve kollar %s → <b>f(x) = %s</b>." % (pt(r, k), "yukarı" if a > 0 else "aşağı", g))

    def deger():
        a, b, c = nz(-3, 3), ri(-6, 6), ri(-9, 9)
        x = ri(-4, 4)
        v = a * x * x + b * x + c
        return M("f(x) = %s için f(%s) kaçtır?" % (poly([a, b, c]), sn(x)), sn(v), W3([sn(-a * x * x + b * x + c), sn(a * x * x - b * x + c), sn(v + a), sn(2 * a * x + b + c)], sn(v)),
                 "x yerine %s yazılır: <b>%s</b>." % (sn(x), sn(v)))

    def ekstrem():
        a, r, k = nz(-3, 3), ri(-5, 5), ri(-9, 9)
        cs = [a, -2 * a * r, a * r * r + k]
        t = "en küçük" if a > 0 else "en büyük"
        return M("f(x) = %s fonksiyonunun %s değeri kaçtır?" % (poly(cs), t), sn(k), W3([sn(r), sn(-k), sn(a * r * r + k), sn(k + a)], sn(k)),
                 "a %s 0 olduğundan tepe noktasında %s değer: f(%s) = <b>%s</b>." % ("&gt;" if a > 0 else "&lt;", t, sn(r), sn(k)))

    sets = [("Değer bulma", [(deger, 20)]), ("Tepe noktası", [(tepe, 20)]), ("x eksenini kesen noktalar", [(kok, 20)]),
            ("En büyük ve en küçük değer", [(ekstrem, 20)]), ("Grafikten fonksiyon", [(grafik, 20)])]
    return U(10, "karesel-fonksiyon", "N", "MAT.10.4.2", 11, "Karesel Fonksiyonlar ve Parabol", "Karesel Fonksiyon",
             "Karesel fonksiyon ve grafiğinin nitel özelliklerini (tepe noktası, simetri ekseni, kökler, en büyük ve en küçük değer) matematiksel temsillerle inceler.",
             "değer bulma, tepe noktası, x eksenini kesen noktalar, en büyük ve en küçük değer, grafikten fonksiyonu bulma",
             "f(x) = a(x − r)² + k", "T(r, k) tepe noktası; a &gt; 0 ise kollar yukarı.".replace("&gt;", ">"), sets,
             ["f(x) = ax² + bx + c fonksiyonunun grafiği paraboldür; tepe noktasının apsisi r = −b ÷ 2a’dır.",
              "a &gt; 0 ise kollar yukarı, tepe noktası en küçük değeri verir; a &lt; 0 ise kollar aşağı, tepe noktası en büyük değeri verir.",
              "Grafiğin x eksenini kestiği noktalar f(x) = 0 denkleminin kökleridir."],
             [("f(x) = x² − 6x + 5", ["r = 3", "f(3) = −4"], "T(3, −4)"), ("x² − 6x + 5 = 0", ["(x − 1)(x − 5)"], "x = 1 ve 5")],
             [["r = b ÷ 2a almak", "İşaret: r = −b ÷ 2a"], ["Tepe noktasında k yerine r yazmak", "Değer k’dir"], ["a’nın işaretini unutmak", "a &lt; 0 ise en büyük değer"]],
             [("Simetri ekseni nedir?", "x = r doğrusudur; parabol bu doğruya göre simetriktir."), ("Kök yoksa?", "Parabol x eksenini kesmez."),
              ("Günlük hayatta parabol?", "Atılan bir topun yolu, köprü kemerleri ve uydu antenleri.")])


# ============================================================ 12. karekök ve rasyonel fonksiyonlar
def u12():
    def kok_tanim():
        a, b = ri(-6, 6), ri(-6, 6)
        k = ri(0, 1)
        inner = lin(1, "x", -a)
        f = "√(%s)%s" % (inner, (" + %s" % sn(b)) if b > 0 else (" − %s" % sn(-b)) if b < 0 else "")
        if k == 0:
            return M("f(x) = %s fonksiyonunun en geniş tanım kümesi hangisidir?" % f, "[%s, ∞)" % sn(a), ["(%s, ∞)" % sn(a), "[%s, ∞)" % sn(b) if b != a else "[%s, ∞)" % sn(a + 1), "(−∞, %s]" % sn(a)],
                     "x − (%s) ≥ 0 → <b>[%s, ∞)</b>." % (sn(a), sn(a)))
        return M("f(x) = %s fonksiyonunun görüntü kümesi hangisidir?" % f, "[%s, ∞)" % sn(b), ["[%s, ∞)" % sn(a) if a != b else "[%s, ∞)" % sn(b + 1), "(%s, ∞)" % sn(b), "ℝ"],
                 "Karekök en az 0 olduğundan f(x) ≥ %s: <b>[%s, ∞)</b>." % (sn(b), sn(b)))

    def kok_deger():
        a, b = ri(-5, 5), ri(-5, 5)
        t = ri(0, 8)
        x = t * t + a
        v = t + b
        f = "√(%s)%s" % (lin(1, "x", -a), (" + %s" % sn(b)) if b > 0 else (" − %s" % sn(-b)) if b < 0 else "")
        return M("f(x) = %s için f(%s) kaçtır?" % (f, sn(x)), sn(v), W3([sn(t * t + b), sn(t - b), sn(v + 1), sn(-v)], sn(v)), "√(%s) = %d → %d %s = <b>%s</b>." % (sn(x - a), t, t, ("+ %s" % sn(b)) if b >= 0 else "− %s" % sn(-b), sn(v)))

    def asimptot():
        a, b, c, d = nz(-5, 5), ri(-9, 9), nz(-3, 3), ri(-9, 9)
        if a * d == b * c:
            return None
        k = ri(0, 1)
        f = "(%s) ÷ (%s)" % (lin(a, "x", b), lin(c, "x", d))
        if k == 0:
            g = "x = %s" % sn(F(-d, c))
            return M("f(x) = %s fonksiyonunun düşey asimptotu hangisidir?" % f, g, W3(["x = %s" % sn(F(d, c)), "x = %s" % sn(F(a, c)), "x = %s" % sn(F(-b, a)), "x = %s" % sn(F(-d, c) + 1)], g),
                     "Paydayı sıfır yapan değer: %s = 0 → <b>%s</b>." % (lin(c, "x", d), g))
        g = "y = %s" % sn(F(a, c))
        return M("f(x) = %s fonksiyonunun yatay asimptotu hangisidir?" % f, g, W3(["y = %s" % sn(F(c, a)), "y = %s" % sn(F(b, d)) if d else "y = %s" % sn(F(a, c) + 1), "y = %s" % sn(F(-d, c)), "y = %s" % sn(F(a, c) + 1)], g),
                 "x büyüdükçe f(x) başkatsayıların oranına yaklaşır: %s ÷ %s → <b>%s</b>." % (sn(a), sn(c), g))

    def ras_deger():
        a, b, c, d = nz(-5, 5), ri(-9, 9), nz(-3, 3), ri(-9, 9)
        x = ri(-5, 5)
        if c * x + d == 0 or a * d == b * c:
            return None
        v = F(a * x + b, c * x + d)
        return M("f(x) = (%s) ÷ (%s) için f(%s) kaçtır?" % (lin(a, "x", b), lin(c, "x", d), sn(x)), sn(v), W3([sn(F(c * x + d, a * x + b)) if a * x + b else "0" if v else "1", sn(v + 1), sn(-v) if v else "1", sn(F(a, c))], sn(v)),
                 "Pay %s, payda %s → <b>%s</b>." % (sn(a * x + b), sn(c * x + d), sn(v)))

    def ters_oran():
        k = ri(2, 12) * 6
        x1, x2 = ch([(2, 3), (3, 4), (2, 6), (3, 6), (4, 6), (2, 4)])
        v = F(k, x2)
        return M("Bir işi %d işçi %s günde bitiriyor. Aynı hızla çalışan %d işçi bu işi kaç günde bitirir? (f(x) = k ÷ x)" % (x1, sn(F(k, x1)), x2), "%s gün" % sn(v), W3(["%s gün" % sn(F(k, x1) * x2 // x1) if (F(k, x1) * x2 / x1).denominator == 1 else None, "%s gün" % sn(F(k, x1) + x2 - x1), "%s gün" % sn(v + 2), "%s gün" % sn(v * 2)], "%s gün" % sn(v)),
                 "İşçi sayısı ile gün sayısı ters orantılıdır: k = %d · %s = %d, %d ÷ %d = <b>%s</b>." % (x1, sn(F(k, x1)), k, k, x2, sn(v)))

    sets = [("Karekök fonksiyonunun değeri", [(kok_deger, 20)]), ("Tanım ve görüntü kümesi", [(kok_tanim, 20)]), ("Rasyonel fonksiyonun değeri", [(ras_deger, 20)]),
            ("Asimptotlar", [(asimptot, 20)]), ("Ters orantı problemleri", [(ters_oran, 12), (asimptot, 8)])]
    return U(10, "karekok-ve-rasyonel-fonksiyonlar", "N", "MAT.10.4.3, MAT.10.4.4", 12, "Karekök ve Rasyonel Fonksiyonlar", "Karekök ve Rasyonel Fonksiyonlar",
             "Karekök fonksiyonları ve f(x) = (ax + b) ÷ (cx + d) biçimindeki rasyonel fonksiyonların grafik ve nitel özelliklerini (tanım ve görüntü kümesi, asimptotlar) inceler.",
             "karekök fonksiyonunun değeri, tanım ve görüntü kümesi, rasyonel fonksiyonun değeri, düşey ve yatay asimptot, ters orantı",
             "Kök içi ≥ 0, payda ≠ 0", "Yatay asimptot y = a ÷ c, düşey asimptot cx + d = 0.", sets,
             ["f(x) = √(x − a) + b fonksiyonunda kök içi negatif olamaz: tanım kümesi [a, ∞), görüntü kümesi [b, ∞).",
              "f(x) = (ax + b) ÷ (cx + d) fonksiyonunda paydayı sıfır yapan x değeri düşey asimptottur.",
              "x çok büyüdükçe f(x), a ÷ c değerine yaklaşır; y = a ÷ c yatay asimptottur."],
             [("√(x − 2) + 1", ["x ≥ 2", "f(x) ≥ 1"], "[2, ∞) ve [1, ∞)"), ("(2x + 1) ÷ (x − 3)", ["x = 3", "y = 2"], "Asimptotlar")],
             [["Görüntü kümesini tanım kümesiyle karıştırmak", "Tanım x’e, görüntü y’ye aittir"], ["Düşey asimptotta işareti ters almak", "cx + d = 0 çöz"],
              ["Yatay asimptotu b ÷ d sanmak", "Başkatsayılar: a ÷ c"]],
             [("Asimptot nedir?", "Grafiğin giderek yaklaştığı ama değmediği doğrudur."), ("Ters orantı rasyonel midir?", "Evet, f(x) = k ÷ x en basit rasyonel fonksiyondur."),
              ("Karekök grafiği nasıldır?", "Bir başlangıç noktasından sağa doğru yavaşlayarak yükselir.")])


# ============================================================ 13. ters fonksiyonlar
def u13():
    def dogrusal():
        a, b = nz(-6, 6), ri(-9, 9)
        if a in (1,) and b == 0:
            return None
        g = "f⁻¹(x) = (%s) ÷ %s" % (lin(1, "x", -b), par(a)) if a != 1 else "f⁻¹(x) = %s" % lin(1, "x", -b)
        if a == -1:
            g = "f⁻¹(x) = %s" % lin(-1, "x", b)
        w = ["f⁻¹(x) = (%s) ÷ %s" % (lin(1, "x", b), par(a)), "f⁻¹(x) = %s" % lin(a, "x", -b), "f⁻¹(x) = (%s) ÷ %s" % (lin(1, "x", -b), par(-a))]
        return M("f(x) = %s fonksiyonunun tersi hangisidir?" % lin(a, "x", b), g, W3(w, g), "y = %s → x = (y %s) ÷ %s → <b>%s</b>." % (lin(a, "x", b), ("− %s" % sn(b)) if b >= 0 else "+ %s" % sn(-b), par(a), g))

    def deger():
        a, b = nz(-6, 6), ri(-9, 9)
        x = ri(-6, 6)
        y = a * x + b
        return M("f(x) = %s ise f⁻¹(%s) kaçtır?" % (lin(a, "x", b), sn(y)), sn(x), W3([sn(a * y + b), sn(y), sn(x + 1), sn(-x) if x else "1"], sn(x)),
                 "f(x) = %s denklemini çözeriz: %s = %s → x = <b>%s</b>." % (sn(y), lin(a, "x", b), sn(y), sn(x)))

    def rasyonel():
        a, b, c, d = nz(-4, 4), ri(-6, 6), ri(1, 3), ri(-6, 6)
        if a * d == b * c:
            return None
        g = "f⁻¹(x) = (%s) ÷ (%s)" % (lin(-d, "x", b), lin(c, "x", -a))
        w = ["f⁻¹(x) = (%s) ÷ (%s)" % (lin(d, "x", -b), lin(c, "x", -a)), "f⁻¹(x) = (%s) ÷ (%s)" % (lin(c, "x", d), lin(a, "x", b)), "f⁻¹(x) = (%s) ÷ (%s)" % (lin(-d, "x", b), lin(-c, "x", a)) if False else "f⁻¹(x) = (%s) ÷ (%s)" % (lin(a, "x", -b), lin(c, "x", d))]
        return M("f(x) = (%s) ÷ (%s) fonksiyonunun tersi hangisidir?" % (lin(a, "x", b), lin(c, "x", d)), g, W3(w, g),
                 "(ax + b) ÷ (cx + d) fonksiyonunun tersi (−dx + b) ÷ (cx − a)’dır: <b>%s</b>." % g)

    def tablo():
        xs = sh(list(range(-3, 6)))[:4]
        ys = sh(list(range(-5, 10)))[:4]
        i = ri(0, 3)
        t = "<table class='sn-table' style='width:auto'><tbody><tr><td>x</td>%s</tr><tr><td>f(x)</td>%s</tr></tbody></table>" % ("".join("<td>%s</td>" % sn(x) for x in xs), "".join("<td>%s</td>" % sn(y) for y in ys))
        return M("Bire bir f fonksiyonunun bazı değerleri tabloda verilmiştir.%sf⁻¹(%s) kaçtır?" % (t, sn(ys[i])), sn(xs[i]), W3([sn(ys[(i + 1) % 4]), sn(xs[(i + 1) % 4]), sn(ys[i])] + [sn(x) for x in xs], sn(xs[i])),
                 "f(%s) = %s olduğundan f⁻¹(%s) = <b>%s</b>." % (sn(xs[i]), sn(ys[i]), sn(ys[i]), sn(xs[i])))

    def bire_bir():
        S = [("f(x) = x² (ℝ’den ℝ’ye)", "Tersi yoktur; bire bir değildir"), ("f(x) = 3x − 2 (ℝ’den ℝ’ye)", "Tersi vardır"), ("f(x) = |x| (ℝ’den ℝ’ye)", "Tersi yoktur; bire bir değildir"),
             ("f(x) = x³ (ℝ’den ℝ’ye)", "Tersi vardır"), ("f(x) = x² ([0, ∞)’dan [0, ∞)’a)", "Tersi vardır"), ("f(x) = 7 (ℝ’den ℝ’ye)", "Tersi yoktur; bire bir değildir")]
        t, g = ch(S)
        return M("%s fonksiyonunun tersi var mıdır?" % t, g, W3(["Tersi vardır", "Tersi yoktur; bire bir değildir", "Tersi yoktur; tanım kümesi boştur", "Her fonksiyonun tersi vardır"], g),
                 "Bir fonksiyonun tersinin olması için bire bir ve örten olması gerekir. Cevap: <b>%s</b>." % g)

    sets = [("Ters fonksiyonun değeri", [(deger, 20)]), ("Tablodan ters değer", [(tablo, 14), (bire_bir, 6)]), ("Doğrusal fonksiyonun tersi", [(dogrusal, 20)]),
            ("Rasyonel fonksiyonun tersi", [(rasyonel, 20)]), ("Karışık", [(deger, 10), (dogrusal, 10)])]
    return U(10, "ters-fonksiyonlar", "N", "MAT.10.4.5", 13, "Ters Fonksiyonlar", "Ters Fonksiyonlar",
             "Bir fonksiyonun grafiği ile tersinin grafiği arasındaki ilişkiyi inceler; doğrusal ve rasyonel fonksiyonların tersini bulur.",
             "ters fonksiyonun değeri, tablodan f⁻¹ bulma, tersi olan fonksiyonlar, doğrusal ve rasyonel fonksiyonların tersi",
             "f(a) = b ⇔ f⁻¹(b) = a", "Tersini bulmak için y = f(x)’te x’i yalnız bırak.", sets,
             ["f(a) = b ise f⁻¹(b) = a’dır; ters fonksiyon girdi ile çıktının yerini değiştirir.",
              "Tersini bulmak için y = f(x) yazılır, x yalnız bırakılır, sonra x ile y yer değiştirir.",
              "Bir fonksiyonun tersinin olması için bire bir ve örten olması gerekir. f ve f⁻¹ grafikleri y = x doğrusuna göre simetriktir."],
             [("f(x) = 2x + 3", ["y = 2x + 3", "x = (y − 3) ÷ 2"], "f⁻¹(x) = (x − 3) ÷ 2"), ("f(4) = 11", ["Yer değiştir"], "f⁻¹(11) = 4")],
             [["f⁻¹(x)’i 1 ÷ f(x) sanmak", "Ters fonksiyon çarpmaya göre ters değildir"], ["İşlemleri aynı sırayla geri almak", "Ters sırayla geri al"],
              ["Bire bir olmayan fonksiyona ters yazmak", "Önce bire birliği kontrol et"]],
             [("f(f⁻¹(x)) nedir?", "x’tir."), ("Grafikler nasıl ilişkilidir?", "y = x doğrusuna göre birbirinin yansımasıdır."),
              ("x² neden tersinir değil?", "f(2) = f(−2) olduğu için bire bir değildir; tanım kümesi [0, ∞) yapılırsa tersi √x olur.")])


# ============================================================ 14. fonksiyon problemleri
def u14():
    def kesisim():
        a, b, c, d = nz(-4, 4), ri(-9, 9), nz(-4, 4), ri(-9, 9)
        if a == c:
            return None
        x = F(d - b, a - c)
        if x.denominator != 1:
            return None
        return M("f(x) = %s ve g(x) = %s ise f(x) = g(x) eşitliğini sağlayan x kaçtır?" % (lin(a, "x", b), lin(c, "x", d)), sn(x), W3([sn(-x) if x else "1", sn(F(b - d, a + c)) if a + c else "2", sn(x + 1), sn(a * x + b)], sn(x)),
                 "%s = %s → x = <b>%s</b>." % (lin(a, "x", b), lin(c, "x", d), sn(x)))

    def maliyet():
        sabit, birim, fiyat = ri(2, 20) * 100, ri(5, 40), 0
        fiyat = birim + ri(5, 30)
        n = F(sabit, fiyat - birim)
        if n.denominator != 1:
            return None
        return M("Bir atölyenin aylık sabit gideri %s TL, ürün başına maliyeti %d TL’dir. Ürün %d TL’ye satılıyor. Zarar etmemek için en az kaç ürün satılmalıdır?" % (num(sabit), birim, fiyat), num(n),
                 W3([num(sabit // birim) if sabit % birim == 0 else num(n + 3), num(sabit // fiyat) if sabit % fiyat == 0 else num(n - 2), num(n + 1), num(n * 2)], num(n)),
                 "Gelir %dx, gider %s + %dx; %dx ≥ %s + %dx → x ≥ <b>%s</b>." % (fiyat, num(sabit), birim, fiyat, num(sabit), birim, num(n)))

    def alan():
        P = ri(4, 30) * 4
        x = P // 4
        A = x * x
        k = ri(0, 1)
        if k == 0:
            return M("Çevresi %d m olan dikdörtgen biçimindeki bir bahçenin alanı en çok kaç m² olabilir?" % P, num(A), W3([num(A - 1), num(P * P // 8), num(P), num(A // 2)], num(A)),
                     "Kenarlar x ve %d − x: A(x) = x(%d − x), en büyük değer x = %d iken → <b>%s m²</b>." % (P // 2, P // 2, x, num(A)))
        L = P // 2
        A2 = L * L // 2 if L % 2 == 0 else None
        if A2 is None:
            return None
        return M("Bir kenarı duvar olan dikdörtgen bir alan, diğer üç kenarına toplam %d m tel çekilerek çevriliyor. Alan en çok kaç m² olur?" % L, num(L * L // 8) if L % 4 == 0 else None,
                 [num(L * L // 4), num(L * L // 16) if L % 4 == 0 else "1", num(L * L // 8 + L)], "A(x) = x(%d − 2x), tepe x = %d ÷ 4 → <b>%s m²</b>." % (L, L, num(L * L // 8) if L % 4 == 0 else "")) if L % 4 == 0 else None

    def atis():
        v, h0 = ch([10, 20, 30, 40]), ri(0, 30)
        # h(t) = −5t² + vt + h0
        tmax = F(v, 10)
        hmax = h0 + F(v * v, 20)
        k = ri(0, 1)
        if k == 0:
            return M("Yerden %d m yükseklikten atılan bir topun t saniye sonraki yüksekliği h(t) = −5t² + %dt + %d metredir. Top en fazla kaç m yükselir?" % (h0, v, h0) if h0 else "Yerden atılan bir topun t saniye sonraki yüksekliği h(t) = −5t² + %dt metredir. Top en fazla kaç m yükselir?" % v,
                     sn(hmax), W3([sn(hmax - h0) if h0 else sn(hmax / 2), sn(tmax), sn(hmax + 5), sn(v)], sn(hmax)), "Tepe noktası t = %d ÷ 10 = %s; h(%s) = <b>%s m</b>." % (v, sn(tmax), sn(tmax), sn(hmax)))
        return M("Bir topun t saniye sonraki yüksekliği h(t) = −5t² + %dt + %d metredir. Top kaçıncı saniyede en yüksek noktadadır?" % (v, h0), sn(tmax), W3([sn(tmax * 2), sn(hmax), sn(tmax + 1)], sn(tmax)),
                 "t = −b ÷ 2a = %d ÷ 10 = <b>%s</b>." % (v, sn(tmax)))

    def esitsizlik():
        p, q = ri(-6, 6), ri(-6, 6)
        if p >= q:
            return None
        cs = [1, -(p + q), p * q]
        k = ch(["&lt; 0", "≥ 0"])
        g = "(%s, %s)" % (sn(p), sn(q)) if k == "&lt; 0" else "(−∞, %s] ∪ [%s, ∞)" % (sn(p), sn(q))
        w = ["(−∞, %s) ∪ (%s, ∞)" % (sn(p), sn(q)), "[%s, %s]" % (sn(p), sn(q)), "(%s, %s)" % (sn(-q), sn(-p)), "(%s, %s)" % (sn(p), sn(q)), "(−∞, %s] ∪ [%s, ∞)" % (sn(p), sn(q))]
        return M("f(x) = %s olmak üzere f(x) %s eşitsizliğinin çözüm kümesi hangisidir?" % (poly(cs), k), g, W3(w, g),
                 "Kökler %s ve %s; parabol kökler arasında negatiftir. Cevap: <b>%s</b>." % (sn(p), sn(q), g))

    sets = [("Kesişim noktası", [(kesisim, 20)]), ("Gelir ve gider", [(maliyet, 20)]), ("En büyük alan", [(alan, 20)]),
            ("Atış problemleri", [(atis, 20)]), ("Eşitsizlikler", [(esitsizlik, 20)])]
    return U(10, "fonksiyonlarla-denklem-ve-esitsizlik-problemleri", "N", "MAT.10.4.6", 14, "Fonksiyonlarla Denklem ve Eşitsizlik Problemleri", "Fonksiyon Problemleri",
             "Doğrusal ve karesel fonksiyonlarla ifade edilen gerçek yaşam durumlarını modelleyerek denklem ve eşitsizlik problemlerini çözer.",
             "iki fonksiyonun kesişimi, gelir-gider ve kâr, çevresi verilen en büyük alan, atış problemleri, karesel eşitsizlikler",
             "Durumu fonksiyonla modelle", "En büyük ya da en küçük değer tepe noktasındadır.", sets,
             ["Problemi bir fonksiyonla yazarız: bilinmeyeni x seç, istenen niceliği x türünden yaz.",
              "Doğrusal modellerde f(x) = g(x) ya da f(x) ≥ g(x) çözülür; karesel modellerde en büyük ve en küçük değer tepe noktasındadır.",
              "Karesel eşitsizliklerde önce kökler bulunur, sonra parabolün kökler arasında ve dışında aldığı işarete bakılır."],
             [("Çevre 40 m", ["A(x) = x(20 − x)", "x = 10"], "100 m²"), ("x² − x − 6 &lt; 0", ["Kökler −2 ve 3"], "(−2, 3)")],
             [["Sabit gideri unutmak", "Gider = sabit + birim · x"], ["Tepe noktasının apsisini değer sanmak", "Değer f(r)’dir"], ["Eşitsizlikte aralığı ters almak", "a &gt; 0 ise kökler arası negatiftir"]],
             [("Model neden önemli?", "Gerçek durumu matematiksel olarak inceleyip tahmin yapmamızı sağlar."), ("Kâr nasıl hesaplanır?", "Kâr = gelir − gider."),
              ("Atışta neden −5?", "Yer çekimi ivmesi yaklaşık 10 m/s² olduğundan −½ · 10 · t².")])


# ============================================================ 15. sayma stratejileri
def u15():
    def carpma():
        S = [("%d farklı tişört ve %d farklı pantolonu olan biri kaç farklı biçimde giyinebilir?", 2),
             ("Bir lokantada %d çeşit çorba ve %d çeşit ana yemek var. Bir çorba ve bir ana yemek kaç farklı biçimde seçilir?", 2),
             ("A şehrinden B şehrine %d, B’den C’ye %d farklı yol var. A’dan B’ye uğrayarak C’ye kaç farklı yoldan gidilir?", 2),
             ("%d farklı kalem, %d farklı defter ve %d farklı silgiden birer tane kaç farklı biçimde seçilir?", 3)]
        t, n = ch(S)
        xs = [ri(2, 9) for _ in range(n)]
        v = 1
        for x in xs:
            v *= x
        return M(t % tuple(xs), num(v), W3([num(sum(xs)), num(v + 1), num(v * 2), num(v - xs[0])], num(v)), "Çarpma yoluyla sayma: %s = <b>%s</b>." % (" · ".join(map(str, xs)), num(v)))

    def toplama():
        a, b = ri(3, 15), ri(3, 15)
        return M("Bir kütüphanede %d farklı roman ve %d farklı hikâye kitabı vardır. Bu kitaplardan bir tane kaç farklı biçimde seçilir?" % (a, b), num(a + b), W3([num(a * b), num(a + b - 1), num(a + b + 1)], num(a + b)),
                 "Ya roman ya hikâye: toplama yoluyla sayma, %d + %d = <b>%d</b>." % (a, b, a + b))

    def sayi():
        digs = sorted(sh(list(range(0, 10)))[:ri(4, 6)])
        n = ri(2, 3)
        tekrar = ch([True, False])
        has0 = 0 in digs
        k = len(digs)
        if tekrar:
            v = (k - 1 if has0 else k) * k ** (n - 1)
        else:
            v = (k - 1 if has0 else k) * nPr(k - 1, n - 1)
        return M("{%s} kümesinin elemanlarıyla rakamları %s %d basamaklı kaç doğal sayı yazılabilir?" % (", ".join(map(str, digs)), "tekrar edebilen" if tekrar else "farklı", n), num(v),
                 W3([num(k ** n), num(nPr(k, n)), num(v + k), num(v - 1)], num(v)), "Birinci basamağa %s, diğerlerine %s: <b>%s</b>." % ("0 gelemez" if has0 else "%d seçenek" % k, "%d seçenek" % k if tekrar else "kalan rakamlar", num(v)))

    def perm():
        n = ri(3, 8)
        r = ri(2, min(n, 4))
        k = ri(0, 1)
        if k == 0:
            v = math.factorial(n)
            return M("%d kişi bir sıraya kaç farklı biçimde dizilir?" % n, num(v), W3([num(n * n), num(v // n), num(nCr(n, 2)), num(v + n)], num(v)), "%d! = <b>%s</b>." % (n, num(v)))
        v = nPr(n, r)
        return M("%d kişilik bir sınıftan %d kişi başkan, yardımcı%s olarak kaç farklı biçimde seçilir?" % (n, r, {2: "", 3: " ve sekreter", 4: ", sekreter ve sayman"}[r]), num(v),
                 W3([num(nCr(n, r)), num(n ** r), num(v // 2), num(math.factorial(n))], num(v)), "Sıra önemli: P(%d, %d) = <b>%s</b>." % (n, r, num(v)))

    def komb():
        n = ri(4, 12)
        r = ri(2, min(n - 1, 4))
        S = ["%d kişiden %d kişilik bir ekip kaç farklı biçimde seçilir?", "%d farklı meyveden %d tanesi kaç farklı biçimde seçilir?",
             "Düzlemde herhangi üçü doğrusal olmayan %d noktadan %d tanesi kaç farklı biçimde seçilir?"]
        t = ch(S)
        v = nCr(n, r)
        return M(t % (n, r), num(v), W3([num(nPr(n, r)), num(n * r), num(v + n), num(v - 1)], num(v)), "Sıra önemsiz: C(%d, %d) = %d! ÷ (%d! · %d!) = <b>%s</b>." % (n, r, n, r, n - r, num(v)))

    def faktoriyel():
        a = ri(3, 9)
        b = ri(1, a - 1)
        v = math.factorial(a) // math.factorial(b)
        return M("%d! ÷ %d! kaçtır?" % (a, b), num(v), W3([num(math.factorial(a - b)), num(a - b), num(v // a) if v // a else "2", num(v * b)], num(v)), "%s = <b>%s</b>." % (" · ".join(str(i) for i in range(a, b, -1)), num(v)))

    sets = [("Toplama ve çarpma yoluyla sayma", [(toplama, 6), (carpma, 14)]), ("Rakamlarla sayı yazma", [(sayi, 20)]), ("Faktöriyel ve sıralama", [(faktoriyel, 10), (perm, 10)]),
            ("Seçim: sıra önemli mi?", [(perm, 10), (komb, 10)]), ("Kombinasyon", [(komb, 20)])]
    return U(10, "sayma-stratejileri", "SAB", "MAT.10.5.1", 15, "Sayma Stratejileri: Permütasyon ve Kombinasyon", "Sayma Stratejileri",
             "Sayma stratejilerini (toplama ve çarpma yoluyla sayma, sıralama ve seçme) kullanarak olası durumların sayısını belirler.",
             "toplama ve çarpma yoluyla sayma, rakamlarla sayı yazma, faktöriyel, sıralama (permütasyon), seçme (kombinasyon)",
             "Sıra önemliyse sırala, değilse seç", "P(n, r) = n! ÷ (n − r)!, C(n, r) = P(n, r) ÷ r!.", sets,
             ["Birbirini dışlayan seçenekler toplanır (ya o ya bu); art arda yapılan seçimler çarpılır (hem o hem bu).",
              "n farklı nesne n! biçimde sıralanır. n nesneden r tanesinin sıralanması P(n, r) = n! ÷ (n − r)!’dir.",
              "Sıra önemli değilse seçim yapılır: C(n, r) = n! ÷ (r! · (n − r)!)."],
             [("3 tişört, 4 pantolon", ["3 · 4"], "12"), ("6 kişiden 2 kişilik ekip", ["6 · 5 ÷ 2"], "15")],
             [["Sıra önemsizken permütasyon kullanmak", "Ekip, grup → kombinasyon"], ["İlk basamağa 0 koymak", "Sayılar 0 ile başlamaz"], ["Toplama ile çarpmayı karıştırmak", "“ya” toplanır, “ve” çarpılır"]],
             [("0! kaçtır?", "1’dir."), ("C(n, r) ile C(n, n − r) neden eşit?", "r tanesini seçmek, kalan n − r tanesini dışarıda bırakmakla aynıdır."),
              ("Sayma neden önemli?", "Olasılık hesaplarının temelidir.")])


# ============================================================ 16. algoritmik işlemler
def u16():
    def dongu():
        a, b, n = ri(1, 5), ri(2, 4), ri(3, 6)
        x = a
        for _ in range(n):
            x = x * b
        return M("Algoritmanın çıktısı nedir?%s" % code(["1. x ← %d" % a, "2. %d kez tekrarla: x ← x · %d" % (n, b), "3. x değerini yaz"]), num(x), W3([num(a * b * n), num(x // b), num(x * b), num(a + b * n)], num(x)),
                 "%d · %d<sup>%d</sup> = <b>%s</b>." % (a, b, n, num(x)))

    def fakt():
        n = ri(3, 7)
        v = math.factorial(n)
        return M("Algoritmanın çıktısı nedir?%s" % code(["1. s ← 1", "2. i = 1, 2, …, %d için: s ← s · i" % n, "3. s değerini yaz"]), num(v), W3([num(n * (n + 1) // 2), num(v // n), num(v * (n + 1)), num(n ** 2)], num(v)),
                 "Bu algoritma %d! değerini hesaplar: <b>%s</b>." % (n, num(v)))

    def kosul():
        n = ri(10, 40)
        d = ch([3, 4, 5, 6, 7])
        v = len([i for i in range(1, n + 1) if i % d == 0])
        return M("Algoritmanın çıktısı nedir?%s" % code(["1. say ← 0", "2. i = 1, 2, …, %d için: eğer i, %d ile tam bölünüyorsa say ← say + 1" % (n, d), "3. say değerini yaz"]), num(v), W3([num(v + 1), num(v - 1), num(n - v), num(n // d + 2)], num(v)),
                 "1, 2, …, %d arasında %d ile bölünen sayıların sayısı: <b>%d</b>." % (n, d, v))

    def collatz():
        n = ri(3, 30)
        x, s = n, 0
        while x != 1:
            x = x // 2 if x % 2 == 0 else 3 * x + 1
            s += 1
        if s > 25:
            return None
        return M("x = %d ile başlayan algoritma kaç adımda durur?%s" % (n, code(["x ≠ 1 oldukça tekrarla:", "  eğer x çift ise x ← x ÷ 2", "  değilse x ← 3x + 1", "  adım ← adım + 1"])), num(s), W3([num(s + 1), num(s - 1), num(s + 2), num(n // 2)], num(s)),
                 "Değerleri tek tek yazarak sayarız: <b>%d</b> adım." % s)

    def kombi():
        n = ri(4, 9)
        r = ri(2, 3)
        v = nCr(n, r)
        if r == 2:
            c = ["1. say ← 0", "2. i = 1, …, %d ve j = i + 1, …, %d için: say ← say + 1" % (n, n), "3. say değerini yaz"]
        else:
            c = ["1. say ← 0", "2. i &lt; j &lt; k olacak biçimde 1, …, %d arasından her (i, j, k) için: say ← say + 1" % n, "3. say değerini yaz"]
        return M("Algoritmanın çıktısı nedir?%s" % code(c), num(v), W3([num(nPr(n, r)), num(n ** r), num(v + n), num(v - 1)], num(v)), "Bu algoritma C(%d, %d) seçimlerini sayar: <b>%s</b>." % (n, r, num(v)))

    sets = [("Tekrar eden çarpma", [(dongu, 20)]), ("Faktöriyel algoritması", [(fakt, 5), (dongu, 15)]), ("Koşullu sayma", [(kosul, 20)]),
            ("Seçimleri sayan algoritmalar", [(kombi, 10), (kosul, 10)]), ("Adım sayma", [(collatz, 20)])]
    return U(10, "algoritmik-islemler", "SAB", "MAT.10.5.2", 16, "Sayma Problemlerinde Algoritmik İşlemler", "Algoritmik İşlemler",
             "Sayma problemlerinin çözümünde algoritma temelli yaklaşımlar kullanır; tekrar ve koşul yapıları içeren algoritmaların çıktısını bulur.",
             "tekrar eden çarpma, faktöriyel algoritması, koşullu sayma, seçimleri sayan iç içe döngüler, adım sayma",
             "Değişkenleri adım adım izle", "İç içe döngüler seçimleri sayar.", sets,
             ["Algoritmayı izlerken her adımda değişkenlerin değerini bir tabloya yazarız.",
              "Bir döngüde s ← s · i yapılırsa sonuç faktöriyel olur.",
              "i &lt; j olacak biçimde iç içe döngüler, sıranın önemsiz olduğu seçimleri (kombinasyon) sayar."],
             [("s ← 1; i = 1…4: s ← s · i", ["1, 2, 6, 24"], "24"), ("i &lt; j, 1…5", ["C(5, 2)"], "10")],
             [["Döngüyü bir eksik saymak", "İlk ve son değeri kontrol et"], ["Koşulu tersine uygulamak", "Koşul doğruysa adım yapılır"], ["i ve j sırasını iki kez saymak", "i &lt; j olduğundan her çift bir kez"]],
             [("Algoritma neden sayma problemine yardımcı olur?", "Büyük sayıları sistemli olarak saymayı ve bilgisayarla hesaplamayı sağlar."),
              ("Collatz sanısı nedir?", "Her pozitif tam sayıyla başlanınca sonunda 1’e ulaşıldığı düşünülür; henüz ispatlanmamıştır."),
              ("Faktöriyel neden çabuk büyür?", "Her adımda daha büyük bir sayıyla çarpılır.")])


# ============================================================ 17. iki nokta arası uzaklık
def u17():
    def uzak():
        x1, y1 = ri(-6, 6), ri(-6, 6)
        a, b, c = ch([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 6, 10), (4, 3, 5), (12, 5, 13), (0, 7, 7), (9, 12, 15)])
        sx, sy = ch([1, -1]), ch([1, -1])
        x2, y2 = x1 + sx * a, y1 + sy * b
        return M("A%s ve B%s noktaları arasındaki uzaklık kaç birimdir?" % (pt(x1, y1), pt(x2, y2)), num(c), W3([num(a + b), num(c + 1), num(abs(a - b)) if a != b else "1", num(c * c)], num(c)),
                 "|AB| = √(%s² + %s²) = √%d = <b>%d</b>." % (par(x2 - x1), par(y2 - y1), c * c, c))

    def uzak_kok():
        x1, y1, x2, y2 = [ri(-6, 6) for _ in range(4)]
        d2 = (x2 - x1) ** 2 + (y2 - y1) ** 2
        o, i = rt(d2)
        if i == 1 or d2 == 0:
            return None
        g = rts(o, i)
        return M("A%s ve B%s noktaları arasındaki uzaklık kaç birimdir?" % (pt(x1, y1), pt(x2, y2)), g, W3([num(abs(x2 - x1) + abs(y2 - y1)), "√%d" % (d2 + 1), rts(o + 1, i), "√%d" % (abs(x2 - x1) + abs(y2 - y1))], g),
                 "√(%d + %d) = √%d = <b>%s</b>." % ((x2 - x1) ** 2, (y2 - y1) ** 2, d2, g) if o > 1 else "√(%d + %d) = <b>%s</b>." % ((x2 - x1) ** 2, (y2 - y1) ** 2, g))

    def orta():
        x1, y1 = ri(-8, 8), ri(-8, 8)
        x2, y2 = ri(-8, 8), ri(-8, 8)
        k = ri(0, 1)
        if k == 0:
            g = pt(F(x1 + x2, 2), F(y1 + y2, 2))
            return M("A%s ve B%s noktalarını birleştiren doğru parçasının orta noktası hangisidir?" % (pt(x1, y1), pt(x2, y2)), g, W3([pt(F(x2 - x1, 2), F(y2 - y1, 2)), pt(x1 + x2, y1 + y2), pt(F(y1 + y2, 2), F(x1 + x2, 2))], g),
                     "Orta nokta koordinatların ortalamasıdır: <b>%s</b>." % g)
        g = pt(2 * x2 - x1, 2 * y2 - y1)
        return M("[AB] doğru parçasının orta noktası M%s ve A%s ise B noktası hangisidir?" % (pt(x2, y2), pt(x1, y1)), g, W3([pt(F(x1 + x2, 2), F(y1 + y2, 2)), pt(x2 - x1, y2 - y1), pt(2 * x1 - x2, 2 * y1 - y2)], g),
                 "B = 2M − A = <b>%s</b>." % g)

    def bolen():
        x1, y1 = ri(-6, 6), ri(-6, 6)
        m, n = ch([(1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2)])
        dx, dy = (m + n) * ri(-3, 3), (m + n) * ri(-3, 3)
        if dx == 0 and dy == 0:
            return None
        x2, y2 = x1 + dx, y1 + dy
        px, py = x1 + dx * m // (m + n), y1 + dy * m // (m + n)
        g = pt(px, py)
        return M("A%s ve B%s olmak üzere [AB] üzerindeki P noktası için |AP| : |PB| = %d : %d olsun. P noktası hangisidir?" % (pt(x1, y1), pt(x2, y2), m, n), g,
                 W3([pt(x1 + dx * n // (m + n), y1 + dy * n // (m + n)), pt(F(x1 + x2, 2), F(y1 + y2, 2)), pt(px + 1, py)], g), "A’dan B’ye yolun %d/%d kadarı gidilir: <b>%s</b>." % (m, m + n, g))

    def ucgen():
        x1, y1 = ri(-4, 4), ri(-4, 4)
        a, b, c = ch([(3, 4, 5), (6, 8, 10), (5, 12, 13)])
        A, B, C = (x1, y1), (x1 + a, y1), (x1, y1 + b)
        P = a + b + c
        return M("Köşeleri A%s, B%s ve C%s olan üçgenin çevresi kaç birimdir?" % (pt(*A), pt(*B), pt(*C)), num(P), W3([num(a + b), num(a * b // 2), num(P + 1), num(2 * c)], num(P)),
                 "|AB| = %d, |AC| = %d, |BC| = √(%d + %d) = %d → <b>%d</b>." % (a, b, a * a, b * b, c, P))

    sets = [("İki nokta arası uzaklık", [(uzak, 20)]), ("Köklü uzaklıklar", [(uzak_kok, 20)]), ("Orta nokta", [(orta, 20)]),
            ("Doğru parçasını bölen nokta", [(bolen, 20)]), ("Problemler", [(ucgen, 10), (uzak, 10)])]
    return U(10, "iki-nokta-arasi-uzaklik", "AN", "MAT.10.6.1", 17, "Analitik Düzlemde İki Nokta Arasındaki Uzaklık", "İki Nokta Arası Uzaklık",
             "Analitik düzlemde iki nokta arasındaki uzaklığı, bir doğru parçasının orta noktasını ve doğru parçasını belli bir oranda bölen noktayı bulur.",
             "iki nokta arası uzaklık formülü, köklü uzaklıklar, orta nokta, doğru parçasını bölen nokta, koordinatlarla çevre",
             "|AB| = √(Δx² + Δy²)", "Orta nokta koordinatların ortalamasıdır.", sets,
             ["İki nokta arasındaki uzaklık Pisagor teoreminden gelir: |AB| = √((x₂ − x₁)² + (y₂ − y₁)²).",
              "[AB]’nin orta noktası ((x₁ + x₂) ÷ 2, (y₁ + y₂) ÷ 2)’dir.",
              "|AP| : |PB| = m : n ise P, A’dan B’ye giden yolun m ÷ (m + n)’i kadar ilerisindedir."],
             [("A(1, 2), B(4, 6)", ["Δx = 3, Δy = 4"], "5"), ("A(2, 4), B(6, 0)", ["Ortalama"], "M(4, 2)")],
             [["Farkların karesini almadan toplamak", "Önce kare al"], ["Orta noktada farkı ikiye bölmek", "Toplamı ikiye böl"], ["Bölme oranını ters uygulamak", "m, A tarafına aittir"]],
             [("Formül neden Pisagor’dan gelir?", "Δx ve Δy dik kenarlar, uzaklık hipotenüstür."), ("Uzaklık negatif olur mu?", "Hayır, karekök her zaman 0 ya da pozitiftir."),
              ("Orta nokta nerede kullanılır?", "Kenarortay ve simetri problemlerinde.")])


# ============================================================ 18. doğrunun analitik incelenmesi
def u18():
    def egim():
        x1, y1, x2, y2 = [ri(-8, 8) for _ in range(4)]
        if x1 == x2:
            return None
        m = F(y2 - y1, x2 - x1)
        return M("A%s ve B%s noktalarından geçen doğrunun eğimi kaçtır?" % (pt(x1, y1), pt(x2, y2)), sn(m), W3([sn(F(x2 - x1, y2 - y1)) if y2 != y1 else "1", sn(-m) if m else "1", sn(m + 1), sn(F(y2 + y1, x2 + x1)) if x2 + x1 else "2"], sn(m)),
                 "m = (y₂ − y₁) ÷ (x₂ − x₁) = %s ÷ %s = <b>%s</b>." % (sn(y2 - y1), par(x2 - x1), sn(m)))

    def denklem():
        m, b = nz(-4, 4), ri(-8, 8)
        x1 = ri(-4, 4)
        y1 = m * x1 + b
        g = "y = %s" % lin(m, "x", b)
        return M("Eğimi %s olan ve %s noktasından geçen doğrunun denklemi hangisidir?" % (sn(m), pt(x1, y1)), g, W3(["y = %s" % lin(m, "x", -b), "y = %s" % lin(-m, "x", b), "y = %s" % lin(m, "x", y1), "y = %s" % lin(m, "x", b + 1)], g),
                 "y − %s = %s(x − %s) → <b>%s</b>." % (par(y1), sn(m), par(x1), g))

    def paralel():
        m, b = nz(-4, 4), ri(-8, 8)
        x1, y1 = ri(-4, 4), ri(-6, 6)
        k = ch(["paralel", "dik"])
        if k == "paralel":
            mm = F(m)
        else:
            mm = F(-1, m)
        c = y1 - mm * x1
        if c.denominator != 1:
            return None
        g = "y = %s" % lin(mm, "x", c)
        o = F(-1, m) if k == "paralel" else F(m)
        return M("%s noktasından geçen ve y = %s doğrusuna %s olan doğrunun denklemi hangisidir?" % (pt(x1, y1), lin(m, "x", b), k), g,
                 W3(["y = %s" % lin(o, "x", y1 - o * x1) if (y1 - o * x1).denominator == 1 else "y = %s" % lin(o, "x", y1), "y = %s" % lin(mm, "x", b) if b != c else "y = %s" % lin(mm, "x", c + 1), "y = %s" % lin(-mm, "x", c)], g),
                 "%s doğruların eğimi %s; y − %s = %s(x − %s) → <b>%s</b>." % ("Paralel" if k == "paralel" else "Dik", "eşittir" if k == "paralel" else "çarpımı −1’dir", par(y1), sn(mm), par(x1), g))

    def kesim():
        a, b = nz(-6, 6), nz(-6, 6)
        g = pt(a, 0) + " ve " + pt(0, b)
        c = a * b
        # x ÷ a + y ÷ b = 1 → bx + ay = ab
        eq = "%s = %s" % (lin(b, "x", 0) + (" + " if a > 0 else " − ") + ("" if abs(a) == 1 else sn(abs(a))) + "y", sn(c))
        return M("%s doğrusunun eksenleri kestiği noktalar hangileridir?" % eq, g, W3([pt(b, 0) + " ve " + pt(0, a), pt(-a, 0) + " ve " + pt(0, -b), pt(a, 0) + " ve " + pt(0, -b)], g),
                 "y = 0 → x = %s; x = 0 → y = %s: <b>%s</b>." % (sn(a), sn(b), g))

    def nokta_dogru():
        a, b = ch([(3, 4), (4, 3), (5, 12), (12, 5), (6, 8), (8, 6), (1, 0), (0, 1)])
        s1, s2 = ch([1, -1]), ch([1, -1])
        A, B = a * s1, b * s2
        n = math.isqrt(A * A + B * B)
        x0, y0 = ri(-5, 5), ri(-5, 5)
        d = ri(1, 6)
        C = -(A * x0 + B * y0) + ch([1, -1]) * d * n
        eq = "%s = 0" % poly_line(A, B, C)
        return M("%s noktasının %s doğrusuna uzaklığı kaç birimdir?" % (pt(x0, y0), eq), num(d), W3([num(d + 1), num(abs(A * x0 + B * y0 + C)), num(d * 2), num(abs(d - 1)) if d > 1 else "2"], num(d)),
                 "|%s · %s + %s · %s + %s| ÷ √(%d + %d) = %d ÷ %d = <b>%d</b>." % (sn(A), par(x0), sn(B), par(y0), par(C), A * A, B * B, d * n, n, d))

    sets = [("Eğim", [(egim, 20)]), ("Doğru denklemi", [(denklem, 20)]), ("Paralel ve dik doğrular", [(paralel, 20)]),
            ("Eksenleri kestiği noktalar", [(kesim, 20)]), ("Noktanın doğruya uzaklığı", [(nokta_dogru, 20)])]
    return U(10, "dogrunun-analitik-incelenmesi", "AN", "MAT.10.6.2", 18, "Doğrunun Analitik İncelenmesi", "Doğrunun Analitik İncelenmesi",
             "Analitik düzlemde doğrunun eğimini ve denklemini inceler; paralel ve dik doğruların eğimleri arasındaki ilişkiyi ve bir noktanın doğruya uzaklığını kullanır.",
             "iki noktadan eğim, eğimi ve bir noktası verilen doğru, paralel ve dik doğrular, eksenleri kestiği noktalar, noktanın doğruya uzaklığı",
             "m = Δy ÷ Δx", "Paralelde m₁ = m₂, dikte m₁ · m₂ = −1.", sets,
             ["Eğim, doğru üzerinde x 1 birim artınca y’nin ne kadar değiştiğidir: m = (y₂ − y₁) ÷ (x₂ − x₁).",
              "Eğimi m olan ve (x₁, y₁) noktasından geçen doğru: y − y₁ = m(x − x₁).",
              "Paralel doğruların eğimleri eşittir; dik doğruların eğimleri çarpımı −1’dir. (x₀, y₀) noktasının ax + by + c = 0 doğrusuna uzaklığı |ax₀ + by₀ + c| ÷ √(a² + b²)’dir."],
             [("A(1, 2), B(3, 8)", ["6 ÷ 2"], "m = 3"), ("m = 2, (1, 5)", ["y − 5 = 2(x − 1)"], "y = 2x + 3")],
             [["Eğimde Δx ÷ Δy almak", "Δy üstte"], ["Dik doğruda yalnızca işaret değiştirmek", "Ters ve işaret değiştir: −1/m"], ["Uzaklıkta mutlak değeri unutmak", "Uzaklık pozitiftir"]],
             [("Eğim 0 ise?", "Doğru yataydır."), ("Düşey doğrunun eğimi?", "Tanımsızdır; denklemi x = a biçimindedir."),
              ("Eğim günlük hayatta?", "Yolların, rampaların ve çatıların dikliğidir.")])


def poly_line(A, B, C):
    s = lin(A, "x", 0) if A else ""
    if B:
        t = ("" if abs(B) == 1 else sn(abs(B))) + "y"
        s = (s + (" + " if B > 0 else " − ") + t) if s else ((MINUS if B < 0 else "") + t)
    if C:
        s += (" + %s" % sn(C)) if C > 0 else (" − %s" % sn(-C))
    return s


# ============================================================ 19. koşullu olasılık
def u19():
    def zar():
        S = [("çift", {2, 4, 6}), ("tek", {1, 3, 5}), ("asal", {2, 3, 5}), ("3’ten büyük", {4, 5, 6}), ("4’ten küçük", {1, 2, 3}), ("5’ten küçük", {1, 2, 3, 4})]
        (an, A), (bn, B) = sh(S)[:2]
        if not (A & B):
            return None
        v = F(len(A & B), len(B))
        return M("Bir zar atılıyor. Gelen sayının %s olduğu bilindiğine göre %s olma olasılığı kaçtır?" % (bn, an), sn(v), W3([sn(F(len(A & B), 6)), sn(F(len(A), 6)), sn(F(len(A & B), len(A))), sn(1 - v) if v != 1 else "0"], sn(v)),
                 "Örnek uzay {%s} kümesine daralır; bunlardan %s olanlar {%s}: <b>%s</b>." % (", ".join(map(str, sorted(B))), an, ", ".join(map(str, sorted(A & B))), sn(v)))

    def kart():
        n = ri(10, 30)
        S = [("çift", lambda i: i % 2 == 0), ("tek", lambda i: i % 2 == 1), ("3’ün katı", lambda i: i % 3 == 0), ("5’in katı", lambda i: i % 5 == 0), ("4’ün katı", lambda i: i % 4 == 0)]
        (an, fa), (bn, fb) = sh(S)[:2]
        B = [i for i in range(1, n + 1) if fb(i)]
        AB = [i for i in B if fa(i)]
        if not AB or len(AB) == len(B):
            return None
        v = F(len(AB), len(B))
        return M("1’den %d sayısına kadar numaralanmış kartlardan biri çekiliyor. Kart numarasının %s olduğu bilindiğine göre %s olma olasılığı kaçtır?" % (n, bn, an), sn(v),
                 W3([sn(F(len(AB), n)), sn(F(len([i for i in range(1, n + 1) if fa(i)]), n)), sn(1 - v), sn(F(len(AB), len(B) + 1))], sn(v)),
                 "%s olan kartlar %d tane; bunların %d tanesi %s: <b>%s</b>." % (cap(bn), len(B), len(AB), an, sn(v)))

    def tablo():
        r1, r2, c1, c2 = ch([("Kız", "Erkek", "Gözlüklü", "Gözlüksüz"), ("10-A", "10-B", "Satranç kulübünde", "Kulüpte değil"), ("Sabah", "Akşam", "Otobüsle", "Yürüyerek")])
        a, b, c, d = [ri(3, 25) for _ in range(4)]
        t = "<table class='sn-table' style='width:auto'><thead><tr><th></th><th>%s</th><th>%s</th></tr></thead><tbody><tr><td>%s</td><td>%d</td><td>%d</td></tr><tr><td>%s</td><td>%d</td><td>%d</td></tr></tbody></table>" % (c1, c2, r1, a, b, r2, c, d)
        k = ri(0, 1)
        if k == 0:
            v = F(a, a + c)
            return M("Tablodan rastgele bir kişi seçiliyor:%sSeçilenin “%s” olduğu bilindiğine göre %s olma olasılığı kaçtır?" % (t, c1, r1), sn(v), W3([sn(F(a, a + b)), sn(F(a, a + b + c + d)), sn(F(c, a + c))], sn(v)),
                     "P(%s | %s) = %d ÷ %d = <b>%s</b>." % (r1, c1, a, a + c, sn(v)))
        v = F(d, c + d)
        return M("Tablodan rastgele bir kişi seçiliyor:%sSeçilenin %s olduğu bilindiğine göre “%s” olma olasılığı kaçtır?" % (t, r2, c2), sn(v), W3([sn(F(d, b + d)), sn(F(d, a + b + c + d)), sn(F(c, c + d))], sn(v)),
                 "P(%s | %s) = %d ÷ %d = <b>%s</b>." % (c2, r2, d, c + d, sn(v)))

    def formul():
        pb = F(ri(2, 9), 10)
        pab = F(ri(1, int(pb * 10) - 1), 10) if pb > F(1, 10) else None
        if pab is None:
            return None
        v = pab / pb
        return M("P(A ∩ B) = %s ve P(B) = %s ise P(A | B) kaçtır?" % (dq(pab, 1), dq(pb, 1)), sn(v), W3([sn(pab * pb), sn(pb / pab), sn(pb - pab), sn(1 - v) if v != 1 else "0"], sn(v)),
                 "P(A | B) = P(A ∩ B) ÷ P(B) = %s ÷ %s = <b>%s</b>." % (dq(pab, 1), dq(pb, 1), sn(v)))

    def torba():
        k, m = ri(2, 8), ri(2, 8)
        renk = ch([("kırmızı", "mavi"), ("beyaz", "siyah"), ("sarı", "yeşil")])
        v = F(k - 1, k + m - 1)
        return M("Bir torbada %d %s ve %d %s top vardır. Geri koymadan art arda iki top çekiliyor. Birinci topun %s olduğu bilindiğine göre ikincinin de %s olma olasılığı kaçtır?" % (k, renk[0], m, renk[1], renk[0], renk[0]),
                 sn(v), W3([sn(F(k, k + m)), sn(F(k - 1, k + m)), sn(F(m, k + m - 1)), sn(F(k * (k - 1), (k + m) * (k + m - 1)))], sn(v)),
                 "Birinci çekilişten sonra %d top kalır, bunların %d tanesi %s: <b>%s</b>." % (k + m - 1, k - 1, renk[0], sn(v)))

    def bagimsiz():
        pa, pb = F(ri(1, 9), 10), F(ri(1, 9), 10)
        k = ri(0, 1)
        if k == 0:
            v = pa * pb
            return M("A ve B bağımsız olaylar, P(A) = %s ve P(B) = %s ise P(A ∩ B) kaçtır?" % (dq(pa, 1), dq(pb, 1)), dq(v, 2), W3([dq(pa + pb, 1) if pa + pb < 1 else dq(pa, 1), dq(abs(pa - pb), 1) if pa != pb else "0", dq(v + F(1, 10), 2)], dq(v, 2)),
                     "Bağımsız olaylarda P(A ∩ B) = P(A) · P(B) = <b>%s</b>." % dq(v, 2))
        return M("A ve B bağımsız olaylar ve P(A) = %s ise P(A | B) kaçtır?" % dq(pa, 1), dq(pa, 1), W3([dq(pb, 1), dq(pa * pb, 2), dq(1 - pa, 1)], dq(pa, 1)),
                 "Bağımsız olaylarda B’nin gerçekleşmesi A’yı etkilemez: P(A | B) = P(A) = <b>%s</b>." % dq(pa, 1)) if pa != pb and pa * pb != pa and 1 - pa != pb else None

    sets = [("Zar ve kartlar", [(zar, 10), (kart, 10)]), ("İki yönlü tablolar", [(tablo, 20)]), ("Formülle hesaplama", [(formul, 20)]),
            ("Geri koymadan çekiliş", [(torba, 20)]), ("Bağımsız olaylar", [(bagimsiz, 14), (kart, 6)])]
    return U(10, "kosullu-olasilik", "VO", "MAT.10.7.1", 19, "Koşullu Olasılık", "Koşullu Olasılık",
             "Koşullu olasılığı hesaplar; bir olayın gerçekleştiği bilindiğinde örnek uzayın daraldığını ve bağımsız olaylarda koşullu olasılığın değişmediğini yorumlar.",
             "zar ile koşullu olasılık, iki yönlü tablolarda koşullu olasılık, P(A | B) formülü, geri koymadan çekiliş, bağımsız olaylar",
             "P(A | B) = P(A ∩ B) ÷ P(B)", "B bilindiğinde örnek uzay B’ye daralır.", sets,
             ["P(A | B), B olayının gerçekleştiği bilindiğinde A’nın gerçekleşme olasılığıdır.",
              "B bilindiğinde örnek uzay B’ye daralır: P(A | B) = P(A ∩ B) ÷ P(B).",
              "A ve B bağımsız ise P(A | B) = P(A) ve P(A ∩ B) = P(A) · P(B)’dir."],
             [("Zar çift geldi; asal mı?", ["{2, 4, 6}", "Asal: {2}"], "1/3"), ("P(A ∩ B) = 0,2; P(B) = 0,5", ["0,2 ÷ 0,5"], "2/5")],
             [["P(A | B) ile P(B | A)’yı karıştırmak", "Koşul çizginin sağındadır"], ["Bütün örnek uzaya bölmek", "Daralmış uzaya böl"], ["Geri koymadan çekilişte toplamı azaltmamak", "Bir top eksilir"]],
             [("P(A | B) = P(B | A) olur mu?", "Genelde hayır; yalnızca P(A) = P(B) iken."), ("Bağımsızlık ne demek?", "Bir olayın gerçekleşmesi diğerinin olasılığını değiştirmez."),
              ("Nerede kullanılır?", "Tıbbi testlerde, hava tahmininde ve sigortacılıkta.")])


# ============================================================ 20. Bayes teoremi
def u20():
    def toplam():
        pa = ri(2, 8) * 10
        p1, p2 = ri(1, 9) * 5, ri(1, 9) * 5
        pb = F(pa * p1 + (100 - pa) * p2, 10000)
        return M("Bir fabrikada ürünlerin %s kadarı A makinesinde, kalanı B makinesinde üretilir. A’nın ürünlerinin %s kadarı, B’ninkilerin %s kadarı kusurludur. Rastgele seçilen bir ürünün kusurlu olma olasılığı kaçtır?" % (pct(pa), pct(p1), pct(p2)),
                 sn(pb), W3([sn(F(p1 + p2, 200)), sn(F(pa * p1, 10000)), sn(F(p1, 100)), sn(pb + F(1, 100))], sn(pb)),
                 "Toplam olasılık: %s · %s + %s · %s = <b>%s</b>." % (sn(F(pa, 100)), sn(F(p1, 100)), sn(F(100 - pa, 100)), sn(F(p2, 100)), sn(pb)))

    def bayes():
        pa = ri(2, 8) * 10
        p1, p2 = ri(1, 9) * 5, ri(1, 9) * 5
        num_ = pa * p1
        den = pa * p1 + (100 - pa) * p2
        v = F(num_, den)
        return M("Bir fabrikada ürünlerin %s kadarı A makinesinde, kalanı B makinesinde üretilir. A’nın ürünlerinin %s kadarı, B’ninkilerin %s kadarı kusurludur. Seçilen ürün kusurlu ise A’da üretilmiş olma olasılığı kaçtır?" % (pct(pa), pct(p1), pct(p2)),
                 sn(v), W3([sn(F(pa, 100)), sn(F(p1, 100)), sn(1 - v), sn(F(num_, 10000))], sn(v)),
                 "P(A | K) = P(A) · P(K | A) ÷ P(K) = %d ÷ %d = <b>%s</b>." % (num_, den, sn(v)))

    def test():
        p = ch([1, 2, 5, 10])
        s, f = ch([90, 95, 80]), ch([5, 10, 2])
        num_ = p * s
        den = p * s + (100 - p) * f
        v = F(num_, den)
        return M("Bir toplulukta kişilerin %s kadarı hastadır. Bir test hastaların %s kadarında pozitif, sağlıklıların %s kadarında da yanlışlıkla pozitif çıkıyor. Testi pozitif çıkan birinin hasta olma olasılığı kaçtır?" % (pct(p), pct(s), pct(f)),
                 sn(v), W3([sn(F(s, 100)), sn(F(p, 100)), sn(1 - v), sn(F(100 - f, 100))], sn(v)),
                 "P(H | +) = %s · %s ÷ (%s · %s + %s · %s) = %d ÷ %d = <b>%s</b>." % (sn(F(p, 100)), sn(F(s, 100)), sn(F(p, 100)), sn(F(s, 100)), sn(F(100 - p, 100)), sn(F(f, 100)), num_, den, sn(v)))

    def torba():
        a1, b1, a2, b2 = [ri(1, 8) for _ in range(4)]
        # torba seçimi eşit olasılıklı, kırmızı çekildi
        num_ = F(a1, a1 + b1)
        den = num_ + F(a2, a2 + b2)
        v = num_ / den
        return M("I. torbada %d kırmızı %d mavi, II. torbada %d kırmızı %d mavi top vardır. Rastgele bir torba seçilip bir top çekiliyor. Top kırmızı ise I. torbadan çekilmiş olma olasılığı kaçtır?" % (a1, b1, a2, b2),
                 sn(v), W3([sn(F(1, 2)), sn(num_), sn(1 - v), sn(F(a1, a1 + a2))], sn(v)),
                 "P(I | K) = ½ · %s ÷ (½ · %s + ½ · %s) = <b>%s</b>." % (sn(num_), sn(num_), sn(F(a2, a2 + b2)), sn(v))) if v != F(1, 2) and v != F(a1, a1 + a2) else None

    def agac():
        p = ri(1, 9) * 10
        q1, q2 = ri(1, 9) * 10, ri(1, 9) * 10
        v = F(p * q1, 10000)
        return M("Bir öğrenci servise %s olasılıkla yetişir. Yetişirse derse %s olasılıkla, yetişemezse %s olasılıkla zamanında girer. Öğrencinin servise yetişip derse zamanında girme olasılığı kaçtır?" % (pct(p), pct(q1), pct(q2)),
                 sn(v), W3([sn(F(q1, 100)), sn(F(p * q1 + (100 - p) * q2, 10000)), sn(F(p + q1, 200)), sn(F(p, 100))], sn(v)),
                 "Ağaç diyagramında dal boyunca çarparız: %s · %s = <b>%s</b>." % (sn(F(p, 100)), sn(F(q1, 100)), sn(v)))

    sets = [("Ağaç diyagramı", [(agac, 20)]), ("Toplam olasılık", [(toplam, 20)]), ("Bayes teoremi", [(bayes, 20)]),
            ("Torbalar", [(torba, 20)]), ("Tıbbi testler", [(test, 20)])]
    return U(10, "bayes-teoremi", "VO", "MAT.10.7.2", 20, "Toplam Olasılık ve Bayes Teoremi", "Bayes Teoremi",
             "Bayes teoremini kullanarak yeni bir bilgi elde edildiğinde olasılıkların nasıl güncellendiğini inceler; toplam olasılık kuralını uygular.",
             "ağaç diyagramında olasılık, toplam olasılık kuralı, Bayes teoremi, torba problemleri, tıbbi test sonuçlarını yorumlama",
             "P(A | K) = P(A ∩ K) ÷ P(K)", "P(K) tüm dallardan toplanır (toplam olasılık).", sets,
             ["Ağaç diyagramında bir dal boyunca olasılıklar çarpılır; aynı sonuca giden dallar toplanır.",
              "Toplam olasılık: P(K) = P(A) · P(K | A) + P(B) · P(K | B).",
              "Bayes teoremi: P(A | K) = P(A) · P(K | A) ÷ P(K). Yeni bilgi (K) ile olasılık güncellenir."],
             [("%60 A, %40 B; kusur %5 ve %10", ["0,03 + 0,04 = 0,07"], "P(K) = 7/100"), ("Kusurlu ise A?", ["0,03 ÷ 0,07"], "3/7")],
             [["Payda yalnızca bir dalı almak", "Bütün dalları topla"], ["P(K | A) ile P(A | K)’yı karıştırmak", "Bayes yer değiştirir"], ["Nadir hastalıkta pozitif testi kesin sanmak", "Yanlış pozitifler çok olabilir"]],
             [("Bayes kimdir?", "18. yüzyılda yaşamış İngiliz matematikçi Thomas Bayes’tir."), ("Neden şaşırtıcı sonuçlar çıkar?", "Nadir olaylarda yanlış pozitifler gerçek pozitiflerden çok olabilir."),
              ("Nerede kullanılır?", "Tıp, istenmeyen e-posta filtreleri ve yapay zekâda.")])


UNITS = [u11, u12, u13, u14, u15, u16, u17, u18, u19, u20]
