# -*- coding: utf-8 -*-
"""Türkiye 9. sınıf (2026 DÖP)：işlem özellikleri, fonksiyonlar, üçgenler, dönüşüm, eşlik-benzerlik, algoritma, mantık, veri, olasılık。"""
import math
from fractions import Fraction as F
import tr_g as G
from tr_g import unit, num, M
from tr_g7 import sn, par, dq, lin, MINUS, gen
from tr_s9a import ri, ch, sh, nz, named, kosy, kurve, reuse, cap, iv, _figure


def setup(rnd):
    pass


def figure(pts, segs, sides=(), right=(), label="geometrik şekil", ticks=()):
    return _figure(pts, segs, sides=sides, right=right, label=label, ticks=ticks)


# ============================================================ 5. işlem özellikleri
def u5():
    OZ = [("a + b = b + a", "Toplamada değişme özelliği"), ("a · b = b · a", "Çarpmada değişme özelliği"),
          ("(a + b) + c = a + (b + c)", "Toplamada birleşme özelliği"), ("(a · b) · c = a · (b · c)", "Çarpmada birleşme özelliği"),
          ("a · (b + c) = a · b + a · c", "Çarpmanın toplama üzerine dağılma özelliği"), ("a + 0 = a", "Toplamada etkisiz eleman"),
          ("a · 1 = a", "Çarpmada etkisiz eleman"), ("a + (−a) = 0", "Toplamada ters eleman"), ("a · (1/a) = 1 (a ≠ 0)", "Çarpmada ters eleman")]

    def ad():
        e, g = ch(OZ)
        return M("“%s” eşitliği hangi özelliği gösterir?" % e, g, sh([x for _, x in OZ if x != g])[:3], "Cevap: <b>%s</b>." % g)

    def sayisal():
        a, b, c = ri(2, 30), ri(2, 30), ri(2, 30)
        k = ri(0, 3)
        if k == 0:
            e, g = "%d · (%d + %d) = %d · %d + %d · %d" % (a, b, c, a, b, a, c), "Çarpmanın toplama üzerine dağılma özelliği"
        elif k == 1:
            e, g = "(%d + %d) + %d = %d + (%d + %d)" % (a, b, c, a, b, c), "Toplamada birleşme özelliği"
        elif k == 2:
            e, g = "%d · %d = %d · %d" % (a, b, b, a), "Çarpmada değişme özelliği"
            if a == b:
                return None
        else:
            e, g = "%d + (%s%d) = 0" % (a, MINUS, a), "Toplamada ters eleman"
        return M("%s eşitliğinde hangi özellik kullanılmıştır?" % e, g, sh([x for _, x in OZ if x != g])[:3], "Cevap: <b>%s</b>." % g)

    def kolay():
        a = ch([25, 50, 125, 20, 4, 8])
        p = {25: 4, 50: 2, 125: 8, 20: 5, 4: 25, 8: 125}[a]
        b = ri(3, 37)
        v = a * p * b
        return M("%d · %d · %d işlemi hangi özellik kullanılarak kolayca yapılır ve sonuç kaçtır?" % (a, b, p), "Değişme ve birleşme; %s" % num(v),
                 ["Dağılma; %s" % num(v + a), "Değişme ve birleşme; %s" % num(v + p), "Etkisiz eleman; %s" % num(a * b)],
                 "(%d · %d) · %d = %d · %d = <b>%s</b>." % (a, p, b, a * p, b, num(v)))

    def dagilma():
        a = ri(2, 9)
        b, c = ri(-9, 9), ri(-9, 9)
        if 0 in (b, c):
            return None
        k = ch([0, 1])
        if k == 0:
            g = lin(a * b, "x", a * c)
            return M("%d(%s) ifadesinin dağılma özelliğiyle yazılışı hangisidir?" % (a, lin(b, "x", c)), g, [lin(a * b, "x", c), lin(b, "x", a * c), lin(a + b, "x", a + c)],
                     "%d · %s ve %d · %s: <b>%s</b>." % (a, lin(b, "x"), a, par(c), g))
        g = "%d(%s)" % (a, lin(b, "x", c))
        return M("%s ifadesinin ortak çarpan parantezine alınmış hâli hangisidir?" % lin(a * b, "x", a * c), g, ["%d(%s)" % (a, lin(b, "x", a * c)), "%s(%s)" % (sn(a * b), lin(1, "x", F(c, b)) if c % b == 0 else lin(1, "x", c)), "%d(%s)" % (a, lin(b, "x", c + 1))],
                 "Her terimde %d çarpanı var: <b>%s</b>." % (a, g))

    sets = [("Özelliğin adı", [(ad, 9), (sayisal, 11)]),
            ("Sayılarla özellikler", [(sayisal, 20)]),
            ("Kolay hesaplama", [(kolay, 20)]),
            ("Dağılma özelliği", [(dagilma, 20)]),
            ("Karışık", [(sayisal, 7), (kolay, 7), (dagilma, 6)])]
    return unit("gercek-sayilarin-islem-ozellikleri", "SY", "MAT.9.1.4", 5, "Gerçek Sayıların İşlem Özellikleri", "İşlem Özellikleri",
                "Gerçek sayıların işlem özelliklerini (değişme, birleşme, dağılma, etkisiz ve ters eleman) cebirsel olarak ifade etmede analojik akıl yürütür.",
                "9. sınıf işlem özellikleri çalışma kâğıdı: değişme, birleşme ve dağılma özellikleri, etkisiz ve ters eleman, özelliklerle kolay hesaplama, ortak çarpan parantezine alma. 100 soru ve cevap anahtarı.",
                "a(b + c) = ab + ac", "Değişme, birleşme ve dağılma hesapları kolaylaştırır.", sets,
                ["Toplama ve çarpmada değişme (a + b = b + a) ve birleşme ((a + b) + c = a + (b + c)) özellikleri vardır.",
                 "Çarpmanın toplama üzerine dağılma özelliği: a(b + c) = ab + ac. Tersine ortak çarpan parantezine alma denir.",
                 "Toplamada etkisiz eleman 0, çarpmada 1’dir. a’nın toplamaya göre tersi −a, çarpmaya göre tersi 1/a’dır (a ≠ 0)."],
                [("25 · 17 · 4", ["(25 · 4) · 17", "100 · 17"], "1.700"), ("6x − 9", ["3 · 2x − 3 · 3"], "3(2x − 3)")],
                [["Çıkarmada değişme özelliğini kullanmak", "5 − 3 ≠ 3 − 5"], ["Dağılmada yalnızca ilk terimi çarpmak", "Her terim çarpılır"],
                 ["0’ın çarpmaya göre tersini aramak", "0’ın çarpmaya göre tersi yoktur"]],
                [("Bölmede değişme özelliği var mı?", "Hayır, 8 ÷ 2 ≠ 2 ÷ 8."),
                 ("Bu özellikler neden önemli?", "Cebirsel ifadeleri düzenlemek ve hızlı hesap yapmak için."),
                 ("Etkisiz eleman ne demek?", "İşleme girince sayıyı değiştirmeyen elemandır.")])


# ============================================================ 6. doğrusal fonksiyonlar
def u6():
    def deger():
        a, b = nz(-5, 5), ri(-9, 9)
        x = ri(-5, 5)
        v = a * x + b
        return M("f(x) = %s fonksiyonu için f(%s) kaçtır?" % (lin(a, "x", b), sn(x)), sn(v), [sn(a * x - b), sn(a + x + b), sn(-v) if v else "1"],
                 "f(%s) = %d · %s %s %d = <b>%s</b>." % (sn(x), a, par(x), "+" if b >= 0 else "−", abs(b), sn(v)))

    def iki_nokta():
        a, b = nz(-4, 4), ri(-6, 6)
        x1, x2 = ri(-4, 1), ri(2, 5)
        y1, y2 = a * x1 + b, a * x2 + b
        g = "f(x) = " + lin(a, "x", b)
        return M("Grafiği (%s, %s) ve (%s, %s) noktalarından geçen doğrusal fonksiyon hangisidir?" % (sn(x1), sn(y1), sn(x2), sn(y2)), g,
                 ["f(x) = " + lin(-a, "x", b), "f(x) = " + lin(a, "x", -b) if b else "f(x) = " + lin(a, "x", 1), "f(x) = " + lin(b if b else 1, "x", a)],
                 "Eğim (%s − %s)/(%s − %s) = %s; f(0) = %s → <b>%s</b>." % (sn(y2), par(y1), sn(x2), par(x1), sn(a), sn(b), g))

    def artan():
        a, b = nz(-5, 5), ri(-8, 8)
        g = "Artandır" if a > 0 else "Azalandır"
        return M("f(x) = %s fonksiyonu artan mı, azalan mı?" % lin(a, "x", b), g, ["Azalandır" if a > 0 else "Artandır", "Sabittir", "Hem artan hem azalandır"],
                 "Eğim %s %s 0 → <b>%s</b>." % (sn(a), "&gt;" if a > 0 else "&lt;", g.lower()))

    def kesen():
        a, b = nz(-4, 4), nz(-8, 8)
        if b % a:
            return None
        x0 = F(-b, a)
        k = ch(["x", "y"])
        if k == "y":
            return M("f(x) = %s fonksiyonunun grafiği y eksenini hangi noktada keser?" % lin(a, "x", b), "(0, %s)" % sn(b), ["(%s, 0)" % sn(x0), "(0, %s)" % sn(-b), "(0, %s)" % sn(a)],
                     "x = 0 için f(0) = %s → <b>(0, %s)</b>." % (sn(b), sn(b)))
        return M("f(x) = %s fonksiyonunun grafiği x eksenini hangi noktada keser?" % lin(a, "x", b), "(%s, 0)" % sn(x0), ["(0, %s)" % sn(b), "(%s, 0)" % sn(-x0) if x0 else "(1, 0)", "(%s, 0)" % sn(b)],
                 "f(x) = 0 → %s = 0 → x = <b>%s</b>." % (lin(a, "x", b), sn(x0)))

    def grafik():
        a, b = nz(-3, 3), ri(-4, 4)
        p = kurve([(lambda x: a * x + b, "#c0392b", "")], (-6, 6, 1), (-6, 6, 1), label="bir doğrunun grafiği")
        g = "f(x) = " + lin(a, "x", b)
        w = ["f(x) = " + lin(-a, "x", b), "f(x) = " + lin(a, "x", -b) if b else "f(x) = " + lin(a, "x", 2), "f(x) = " + lin(b if b not in (0, a) else a + 1, "x", a)]
        return M("Grafiği verilen doğrusal fonksiyon hangisidir?%s" % p, g, w,
                 "Doğru y eksenini %s noktasında kesiyor ve x 1 artınca y %s %s: <b>%s</b>." % (sn(b), sn(abs(a)), "artıyor" if a > 0 else "azalıyor", g))

    sets = [("Fonksiyon değeri", [(deger, 20)]),
            ("Artan, azalan, sabit", [(artan, 10), (kesen, 10)]),
            ("Eksenleri kesme", [(kesen, 20)]),
            ("İki noktadan fonksiyon", [(iki_nokta, 20)]),
            ("Grafik", [(grafik, 20)])]
    return unit("dogrusal-fonksiyonlar", "N", "MAT.9.2.1", 6, "Doğrusal Fonksiyonlar ve Nitel Özellikleri", "Doğrusal Fonksiyonlar",
                "Doğrusal referans fonksiyon f(x) = x ve ondan türetilen doğrusal fonksiyonların nitel özelliklerine (artanlık-azalanlık, eksenleri kesme, eğim) ilişkin matematiksel muhakeme yapar.",
                "9. sınıf doğrusal fonksiyonlar çalışma kâğıdı: f(x) = ax + b, fonksiyon değeri, artan ve azalan fonksiyon, eksenleri kesen noktalar, iki noktası verilen fonksiyon, grafik eşleştirme. 100 soru ve cevap anahtarı.",
                "f(x) = ax + b", "a &gt; 0 artan, a &lt; 0 azalan, a = 0 sabit.", sets,
                ["f(x) = ax + b doğrusal fonksiyonunun grafiği bir doğrudur; a eğimi, b y eksenini kestiği noktayı verir.",
                 "a &gt; 0 ise fonksiyon artan, a &lt; 0 ise azalan, a = 0 ise sabittir.",
                 "Grafiğin x eksenini kestiği noktayı f(x) = 0 denklemiyle, y eksenini kestiği noktayı f(0) ile buluruz."],
                [("f(x) = 2x − 6", ["f(0) = −6", "2x − 6 = 0 → x = 3"], "(0, −6) ve (3, 0)"), ("(1, 5) ve (3, 9)", ["Eğim 4/2 = 2", "b = 3"], "f(x) = 2x + 3")],
                [["Eğimi y farkı yerine x farkı bölü y farkı almak", "Eğim = Δy / Δx"], ["b’yi x eksenini kesen nokta sanmak", "b, y eksenini keser"],
                 ["Negatif eğimi artan sanmak", "a &lt; 0 ise azalan"]],
                [("Referans fonksiyon nedir?", "f(x) = x; diğer doğrusal fonksiyonlar ondan öteleme ve genişleme ile elde edilir."),
                 ("Sabit fonksiyonun grafiği nasıldır?", "x eksenine paralel bir doğrudur."),
                 ("Eğim günlük hayatta neyi gösterir?", "Birim zamandaki değişimi: hız, saatlik ücret gibi.")])


# ============================================================ 7. mutlak değer fonksiyonu
def u7():
    def deger():
        a, h, k = nz(-3, 3), ri(-4, 4), ri(-5, 5)
        x = ri(-6, 6)
        v = a * abs(x - h) + k
        inner = lin(1, "x", -h)
        f = "%s|%s|%s" % ("" if a == 1 else MINUS if a == -1 else sn(a), inner, "" if k == 0 else (" + %d" % k if k > 0 else " − %d" % -k))
        return M("f(x) = %s için f(%s) kaçtır?" % (f, sn(x)), sn(v), [sn(a * (x - h) + k), sn(-v) if v else "1", sn(a * abs(x + h) + k)],
                 "|%s − %s| = %d, %s → <b>%s</b>." % (sn(x), par(h), abs(x - h), "sonuç %s" % sn(v), sn(v)))

    def tepe():
        a, h, k = nz(-3, 3), ri(-5, 5), ri(-5, 5)
        inner = lin(1, "x", -h)
        f = "%s|%s|%s" % ("" if a == 1 else MINUS if a == -1 else sn(a), inner, "" if k == 0 else (" + %d" % k if k > 0 else " − %d" % -k))
        g = "(%s, %s)" % (sn(h), sn(k))
        return M("f(x) = %s fonksiyonunun grafiğinin köşe (tepe) noktası hangisidir?" % f, g, ["(%s, %s)" % (sn(-h), sn(k)), "(%s, %s)" % (sn(k), sn(h)), "(%s, %s)" % (sn(h), sn(-k))],
                 "|x − h| ifadesi x = h iken 0 olur; f(h) = k → <b>%s</b>." % g)

    def parcali():
        h = ri(-5, 5)
        g = "x ≥ %s için %s; x &lt; %s için %s" % (sn(h), lin(1, "x", -h), sn(h), lin(-1, "x", h))
        return M("f(x) = |%s| fonksiyonunun parçalı gösterimi hangisidir?" % lin(1, "x", -h), g,
                 ["x ≥ %s için %s; x &lt; %s için %s" % (sn(h), lin(-1, "x", h), sn(h), lin(1, "x", -h)), "x ≥ %s için %s; x &lt; %s için %s" % (sn(-h), lin(1, "x", h), sn(-h), lin(-1, "x", -h)),
                  "x ≥ 0 için %s; x &lt; 0 için %s" % (lin(1, "x", -h), lin(-1, "x", h))] if h else ["x ≥ 0 için −x; x &lt; 0 için x", "Her x için x", "Her x için −x"],
                 "İçi sıfır yapan değer x = %s; sağında ifade olduğu gibi, solunda işaret değiştirir: <b>%s</b>." % (sn(h), g))

    def denklem():
        h, r = ri(-5, 5), ri(0, 6)
        inner = lin(1, "x", -h)
        if r == 0:
            g = "{%s}" % sn(h)
        else:
            g = "{%s; %s}" % (sn(h - r), sn(h + r))
        return M("|%s| = %d denkleminin çözüm kümesi hangisidir?" % (inner, r), g, ["{%s}" % sn(h + r), "{%s; %s}" % (sn(-h - r), sn(-h + r)) if h else "{%s}" % sn(r + 1), "∅"],
                 "x’in %s sayısına uzaklığı %d: <b>%s</b>." % (sn(h), r, g))

    def grafik():
        h, k = ri(-3, 3), ri(-3, 3)
        a = ch([1, -1])
        p = kurve([(lambda x: a * abs(x - h) + k, "#c0392b", "")], (-6, 6, 1), (-6, 6, 1), label="bir mutlak değer fonksiyonunun grafiği")
        fm = lambda aa, hh, kk: "f(x) = %s|%s|%s" % ("" if aa == 1 else MINUS, lin(1, "x", -hh), "" if kk == 0 else (" + %d" % kk if kk > 0 else " − %d" % -kk))
        g = fm(a, h, k)
        w = [fm(a, -h, k) if h else fm(a, 1, k), fm(a, h, -k) if k else fm(a, h, 1), fm(-a, h, k)]
        return M("Grafiği verilen fonksiyon hangisidir?%s" % p, g, w, "Köşe (%s, %s), kollar %s: <b>%s</b>." % (sn(h), sn(k), "yukarı" if a > 0 else "aşağı", g))

    sets = [("Fonksiyon değeri", [(deger, 20)]),
            ("Köşe noktası", [(tepe, 20)]),
            ("Parçalı gösterim", [(parcali, 11), (denklem, 9)]),
            ("Mutlak değerli denklem", [(denklem, 20)]),
            ("Grafik", [(grafik, 20)])]
    return unit("mutlak-deger-fonksiyonu", "N", "MAT.9.2.2", 7, "Mutlak Değer Fonksiyonu ve Grafiği", "Mutlak Değer Fonksiyonu",
                "Mutlak değer fonksiyonlarının nitel özelliklerini doğrusal fonksiyonlarla analoji kurarak inceler; parçalı gösterim, köşe noktası ve grafiği yorumlar.",
                "9. sınıf mutlak değer fonksiyonu çalışma kâğıdı: f(x) = a|x − h| + k, fonksiyon değeri, köşe noktası, parçalı gösterim, |x − h| = r denklemi, grafik eşleştirme. 100 soru ve cevap anahtarı.",
                "f(x) = a|x − h| + k", "Köşe (h, k); a &gt; 0 ise kollar yukarı.", sets,
                ["|x| fonksiyonu x ≥ 0 için x, x &lt; 0 için −x’tir; grafiği V biçimindedir.",
                 "f(x) = a|x − h| + k grafiğinin köşe noktası (h, k)’dir. a &gt; 0 ise kollar yukarı, a &lt; 0 ise aşağı açılır.",
                 "|x − h| = r denkleminde x’in h’ye uzaklığı r’dir: x = h − r ya da x = h + r."],
                [("f(x) = |x − 2| + 1", ["Köşe x = 2", "f(2) = 1"], "(2, 1)"), ("|x + 3| = 4", ["−3 − 4 ve −3 + 4"], "{−7; 1}")],
                [["|x − 2| köşesini x = −2 sanmak", "İçi sıfır yapan x = 2"], ["Mutlak değerin negatif çıkabileceğini düşünmek", "|a| ≥ 0"],
                 ["Denklemde tek çözüm yazmak", "İki yönde uzaklık vardır"]],
                [("Mutlak değer neyi ölçer?", "Sayı doğrusunda sıfıra (ya da başka bir sayıya) uzaklığı."),
                 ("|x| = −3 denkleminin çözümü var mı?", "Yoktur; mutlak değer negatif olamaz."),
                 ("Grafik neden V biçiminde?", "Köşenin iki yanında iki farklı doğrusal parça vardır.")])


# ============================================================ 8. problemler
def u8():
    yas, ardisik, fiyat = reuse("tr_s7b", "u13", "yas"), reuse("tr_s7b", "u13", "ardisik"), reuse("tr_s7b", "u13", "fiyat")
    taksi, tarife = reuse("tr_s8a", "u12", "taksi"), reuse("tr_s8a", "u12", "tarife")

    def esitsizlik():
        a, b = nz(-6, 6), ri(-10, 10)
        c = ri(-10, 10)
        op = ch(["&lt;", "≤", "&gt;", "≥"])
        x0 = F(c - b, a)
        flip = a < 0
        rev = {"&lt;": "&gt;", "≤": "≥", "&gt;": "&lt;", "≥": "≤"}
        o2 = rev[op] if flip else op
        incl = o2 in ("≤", "≥")
        g = iv(None, x0, False, incl) if o2 in ("&lt;", "≤") else iv(x0, None, incl, False)
        w = [iv(x0, None, incl, False) if o2 in ("&lt;", "≤") else iv(None, x0, False, incl), iv(None, x0, False, not incl) if o2 in ("&lt;", "≤") else iv(x0, None, not incl, False), iv(None, -x0, False, incl) if x0 else iv(None, 1, False, incl)]
        return M("%s %s %s eşitsizliğinin çözüm kümesi hangisidir?" % (lin(a, "x", b), op, sn(c)), g, w,
                 "%s %s %s%s → x %s %s: <b>%s</b>." % (lin(a, "x"), op, sn(c - b), " (negatif sayıya bölünce yön değişir)" if flip else "", o2, sn(x0), g))

    def model():
        p, q = ri(2, 9) * 5, ri(10, 60) * 10
        b = ri(q // p + 1, q // p + 30)
        n = G.K.next()
        return M("Bir spor salonunda aylık sabit ücret %s TL ve her giriş %d TL’dir. %s bir ayda en fazla %s TL harcamak istiyor. En fazla kaç kez girebilir?" % (num(q), p, n, num(q + b * p - ri(1, p - 1))),
                 num(b - 1), [num(b), num(b - 2), num((q + b * p) // p)], "%s + %dx ≤ toplam → x en fazla <b>%d</b>." % (num(q), p, b - 1))

    sets = [("Denklem kurma", [(yas, 10), (ardisik, 10)]),
            ("Eşitsizlikler", [(esitsizlik, 20)]),
            ("Doğrusal modeller", [(taksi, 10), (tarife, 10)]),
            ("Bütçe problemleri", [(model, 20)]),
            ("Karışık", [(fiyat, 7), (esitsizlik, 7), (model, 6)])]
    return unit("dogrusal-denklem-ve-esitsizlik-problemleri", "N", "MAT.9.2.3", 8, "Doğrusal Denklem ve Eşitsizlik Problemleri", "Denklem ve Eşitsizlik Problemleri",
                "Doğrusal fonksiyonlarla ifade edilebilen denklem ve eşitsizlikler içeren problemleri çözer; durumu modelleyip çözüm kümesini yorumlar.",
                "9. sınıf doğrusal denklem ve eşitsizlik problemleri çalışma kâğıdı: yaş ve ardışık sayı problemleri, birinci dereceden eşitsizliklerin çözüm kümesi, taksi ve tarife modelleri, bütçe problemleri. 100 soru ve cevap anahtarı.",
                "Durumu f(x) = ax + b ile modelle", "Negatif sayıyla çarpınca eşitsizliğin yönü değişir.", sets,
                ["Problemdeki sabit miktar b, birim başına değişen miktar a olur: f(x) = ax + b.",
                 "Denklem kurmak için bilinmeyene x der, verilenleri x cinsinden yazarız.",
                 "Eşitsizlikte iki taraf negatif bir sayıyla çarpılır ya da bölünürse eşitsizliğin yönü değişir."],
                [("−3x + 2 &lt; 11", ["−3x &lt; 9", "x &gt; −3"], "(−3, ∞)"), ("Sabit 200 TL, giriş 30 TL, en fazla 500 TL", ["200 + 30x ≤ 500"], "x ≤ 10")],
                [["Negatif bölmede yönü değiştirmemek", "−2x &gt; 6 → x &lt; −3"], ["“En fazla”yı &lt; ile yazmak", "En fazla: ≤"],
                 ["Sabit ücreti her seferde eklemek", "Sabit ücret bir kez eklenir"]],
                [("Eşitsizliğin çözüm kümesi neden aralıktır?", "Koşulu sağlayan sonsuz çok sayı vardır."),
                 ("“En az” nasıl yazılır?", "≥ ile yazılır."),
                 ("Doğrusal model ne zaman kullanılır?", "Her birimde aynı miktarda artan ya da azalan durumlarda.")])


# ============================================================ 9. üçgende açı ve kenar
def u9():
    aci_kenar, esitsizlik = reuse("tr_s8b", "u13", "buyuk_kenar"), reuse("tr_s8b", "u14", "aralik")
    kac = reuse("tr_s8b", "u14", "kac")

    def dis():
        A_, B_ = ri(25, 100), ri(25, 100)
        C_ = 180 - A_ - B_
        if C_ < 15:
            return None
        k = ri(0, 1)
        if k == 0:
            return M("ABC üçgeninde m(A) = %d° ve m(B) = %d°’dir. C köşesindeki dış açı kaç derecedir?" % (A_, B_), "%d°" % (A_ + B_), ["%d°" % C_, "%d°" % (180 - A_), "%d°" % (360 - A_ - B_)],
                     "Bir dış açı, kendisine komşu olmayan iki iç açının toplamına eşittir: %d + %d = <b>%d°</b>." % (A_, B_, A_ + B_))
        return M("Bir üçgenin bir dış açısı %d°, ona komşu olmayan iç açılardan biri %d°’dir. Diğer komşu olmayan iç açı kaç derecedir?" % (A_ + B_, A_), "%d°" % B_,
                 ["%d°" % (180 - A_ - B_), "%d°" % (180 - B_), "%d°" % (A_ + B_ - 90) if A_ + B_ > 90 and A_ + B_ - 90 != B_ else "%d°" % (B_ + 10)],
                 "%d − %d = <b>%d°</b>." % (A_ + B_, A_, B_))

    def dis_toplam():
        a, b = ri(80, 150), ri(80, 150)
        c = 360 - a - b
        if c <= 30 or c >= 180:
            return None
        return M("Bir üçgenin iki dış açısı %d° ve %d°’dir. Üçüncü dış açı kaç derecedir?" % (a, b), "%d°" % c, ["%d°" % (180 - c), "%d°" % (c + 20), "%d°" % (c - 10)],
                 "Üçgenin dış açıları toplamı 360°: 360 − %d − %d = <b>%d°</b>." % (a, b, c))

    def x_bul():
        x = ri(10, 40)
        p, q = ri(1, 3), ri(1, 3)
        r = ri(0, 40)
        if p * x + q * x + r >= 175:
            return None
        third = 180 - (p * x + q * x + r)
        A_ = "%sx" % ("" if p == 1 else p)
        B_ = "%sx + %d" % ("" if q == 1 else q, r) if r else "%sx" % ("" if q == 1 else q)
        return M("Bir üçgenin açıları %s, %s ve %d°’dir. x kaçtır?" % (A_, B_, third), num(x), [num(x + 5), num(180 - third), num(x - 3)],
                 "%s + %s + %d = 180 → %dx = %d → x = <b>%d</b>." % (A_, B_, third, p + q, 180 - third - r, x))

    sets = [("İç ve dış açılar", [(dis, 20)]),
            ("Dış açılar toplamı", [(dis_toplam, 10), (x_bul, 10)]),
            ("Açı-kenar ilişkisi", [(aci_kenar, 20)]),
            ("Üçgen eşitsizliği", [(esitsizlik, 10), (kac, 10)]),
            ("Karışık", [(x_bul, 10), (dis, 10)])]
    return unit("ucgende-aci-ve-kenar-ozellikleri", "GS", "MAT.9.3.1", 9, "Üçgende Açı ve Kenar Özellikleri", "Üçgende Açı ve Kenar",
                "Üçgende açı ve kenarla ilgili özellikleri (iç ve dış açılar, açı-kenar ilişkisi, üçgen eşitsizliği) ve bu özellikler arasındaki ilişkileri doğrular veya ispatlar.",
                "9. sınıf üçgende açı ve kenar özellikleri çalışma kâğıdı: iç açılar toplamı, dış açı özelliği, dış açılar toplamı, açı-kenar ilişkisi, üçgen eşitsizliği. 100 soru ve cevap anahtarı.",
                "Dış açı = uzak iki iç açının toplamı", "İç açılar 180°, dış açılar 360°.", sets,
                ["Bir üçgenin iç açıları toplamı 180°’dir.",
                 "Bir dış açı, kendisine komşu olmayan iki iç açının toplamına eşittir. Dış açılar toplamı 360°’dir.",
                 "Büyük açının karşısında büyük kenar bulunur ve her kenar diğer ikisinin farkından büyük, toplamından küçüktür."],
                [("m(A) = 50°, m(B) = 70°", ["C’deki dış açı 50 + 70"], "120°"), ("Kenarlar 5 ve 9", ["4 &lt; x &lt; 14"], "Üçüncü kenar 4 ile 14 arasında")],
                [["Dış açıyı 180 − komşu olmayan açı sanmak", "Dış açı = komşu olmayan iki iç açının toplamı"], ["Dış açılar toplamını 180° almak", "360°’dir"],
                 ["Eşitlik durumunda üçgen oluştuğunu sanmak", "a + b = c ise üçgen oluşmaz"]],
                [("Dış açı özelliği nasıl ispatlanır?", "Dış açı ile komşu iç açı 180° eder; iç açılar da 180°; ikisi karşılaştırılır."),
                 ("Öklid dışı geometride iç açılar toplamı 180° mi?", "Hayır, küre yüzeyinde 180°’den büyük olabilir."),
                 ("Üçgen eşitsizliği nerede kullanılır?", "Mesafe tahminlerinde ve yapıların sağlamlığında.")])


# ============================================================ 10. geometrik dönüşümler
def u10():
    yansima = reuse("tr_s8b", "u21", "yansima")
    oteleme = reuse("tr_s8b", "u20", "nokta")

    def donme():
        x, y = nz(-6, 6), nz(-6, 6)
        k = ch([90, 180, 270])
        yon = ch(["saat yönünün tersine", "saat yönünde"])
        kk = k if yon == "saat yönünün tersine" else (360 - k) % 360
        img = {90: (-y, x), 180: (-x, -y), 270: (y, -x)}[kk]
        g = "(%s, %s)" % (sn(img[0]), sn(img[1]))
        others = [{90: (-y, x), 180: (-x, -y), 270: (y, -x)}[t] for t in (90, 180, 270) if t != kk] + [(y, x)]
        return M("A(%s, %s) noktası orijin etrafında %s %d° döndürülürse görüntüsü hangisidir?" % (sn(x), sn(y), yon, k), g, ["(%s, %s)" % (sn(p[0]), sn(p[1])) for p in others],
                 "Saat yönünün tersine 90°: (x, y) → (−y, x); 180°: (−x, −y); 270°: (y, −x). Cevap: <b>%s</b>." % g)

    def ozellik():
        S = [("Öteleme, yansıma ve dönme için hangisi her zaman doğrudur?", "Şekil ile görüntüsü eştir", ["Görüntü daha büyüktür", "Şeklin açıları değişir", "Kenar uzunlukları yarıya iner"]),
             ("Hangi dönüşümde şeklin yönü (saat yönü dizilişi) ters döner?", "Yansıma", ["Öteleme", "180° dönme", "90° dönme"]),
             ("Orijin etrafında 180° dönme hangisine eşittir?", "Orijine göre yansıma", ["x eksenine göre yansıma", "y eksenine göre yansıma", "Öteleme"]),
             ("x eksenine göre yansıyan bir noktanın hangi koordinatı değişmez?", "Apsisi (x)", ["Ordinatı (y)", "İkisi de değişir", "İkisi de değişmez"])]
        q, g, w = ch(S)
        return M(q, g, w, "Bu dönüşümler uzunlukları ve açıları korur. Cevap: <b>%s</b>." % g)

    def ardisik():
        x, y = nz(-5, 5), nz(-5, 5)
        dx, dy = nz(-3, 3), nz(-3, 3)
        p = (-y, x)
        q = (p[0] + dx, p[1] + dy)
        g = "(%s, %s)" % (sn(q[0]), sn(q[1]))
        return M("A(%s, %s) noktası önce orijin etrafında saat yönünün tersine 90° döndürülüyor, sonra (%s, %s) kadar ötelenip son görüntü bulunuyor. Son görüntü hangisidir?" % (sn(x), sn(y), sn(dx), sn(dy)),
                 g, ["(%s, %s)" % (sn(y + dx), sn(-x + dy)), "(%s, %s)" % (sn(-x + dx), sn(-y + dy)), "(%s, %s)" % (sn(x + dx), sn(y + dy))],
                 "Dönme: (%s, %s); öteleme: <b>%s</b>." % (sn(p[0]), sn(p[1]), g))

    sets = [("Öteleme", [(oteleme, 20)]),
            ("Yansıma", [(yansima, 20)]),
            ("Dönme", [(donme, 20)]),
            ("Art arda dönüşüm", [(ardisik, 16), (ozellik, 4)]),
            ("Karışık", [(donme, 10), (ardisik, 10)])]
    return unit("geometrik-donusumler", "ES", "MAT.9.4.1", 10, "Geometrik Dönüşümler: Öteleme, Yansıma ve Dönme", "Geometrik Dönüşümler",
                "Geometrik dönüşümlerle (öteleme, yansıma, dönme) ilgili çıkarım yapar; koordinat düzleminde noktaların görüntülerini bulur ve dönüşümlerin eşliği koruduğunu fark eder.",
                "9. sınıf geometrik dönüşümler çalışma kâğıdı: koordinat düzleminde öteleme, eksenlere göre yansıma, orijin etrafında 90°, 180° ve 270° dönme, art arda dönüşümler. 100 soru ve cevap anahtarı.",
                "Dönme 90°: (x, y) → (−y, x)", "Öteleme, yansıma ve dönme şekli eş tutar.", sets,
                ["Öteleme (x, y) → (x + a, y + b); x eksenine göre yansıma (x, −y); y eksenine göre yansıma (−x, y).",
                 "Orijin etrafında saat yönünün tersine 90° dönme (x, y) → (−y, x), 180° dönme (−x, −y), 270° dönme (y, −x).",
                 "Bu dönüşümler uzunlukları ve açıları korur; şekil ile görüntüsü eştir."],
                [("A(3, 2), 90° saat yönünün tersine", ["(−2, 3)"], "A′(−2, 3)"), ("A(−1, 4), 180°", ["(1, −4)"], "A′(1, −4)")],
                [["Saat yönü ile tersini karıştırmak", "Saat yönünde 90° = tersine 270°"], ["Dönmede koordinatları yer değiştirmeyi unutmak", "90°’de x ve y yer değiştirir"],
                 ["Art arda dönüşümde sırayı değiştirmek", "Önce birinci dönüşüm uygulanır"]],
                [("Hangi dönüşüm şeklin yönünü korur?", "Öteleme ve dönme korur; yansıma ters çevirir."),
                 ("Homoteti nedir?", "Şekli büyüten ya da küçülten dönüşümdür; benzerlik oluşturur."),
                 ("Dönüşümler nerede kullanılır?", "Bilgisayar grafiklerinde, desenlerde ve mimaride.")])


# ============================================================ 11–14. eşlik ve benzerlik
def tales_fig(a, b, c, d):
    pts = {"A": (0, 6), "D": (2, 3), "E": (5, 3), "B": (4, 0), "C": (10, 0)}
    return figure(pts, [("A", "B"), ("A", "C"), ("B", "C"), ("D", "E")], sides=[("A", "D", a), ("D", "B", b), ("A", "E", c), ("E", "C", d)], label="paralel doğru parçalı üçgen")


def u11():
    kural, yeterli = reuse("tr_s8b", "u15", "kural"), reuse("tr_s8b", "u15", "yeterli")
    eleman, benzer_mi = reuse("tr_s8b", "u15", "eleman"), reuse("tr_s8b", "u16", "benzer_mi")

    def aa():
        A_, B_ = ri(30, 90), ri(20, 80)
        C_ = 180 - A_ - B_
        if C_ < 10:
            return None
        D_, E_ = ch([(A_, B_), (A_, C_), (B_, C_), (A_ + 5, B_)])
        good = sorted([D_, E_]) in (sorted([A_, B_]), sorted([A_, C_]), sorted([B_, C_]))
        g = "Benzerdir (AA)" if good else "Benzer değildir"
        return M("Bir üçgenin açıları %d°, %d° ve %d°’dir. Diğer üçgenin iki açısı %d° ve %d°’dir. Bu üçgenler benzer midir?" % (A_, B_, C_, D_, E_), g,
                 ["Benzer değildir" if good else "Benzerdir (AA)", "Eştir", "Bilinemez"], "İki açı eşitse üçüncü de eşittir (AA benzerlik). Cevap: <b>%s</b>." % g)

    sets = [("Eşlik koşulları", [(kural, 3), (yeterli, 5), (eleman, 12)]),
            ("Benzerlik koşulları", [(aa, 20)]),
            ("Kenar oranları", [(benzer_mi, 20)]),
            ("Karşılık gelen elemanlar", [(eleman, 20)]),
            ("Karışık", [(aa, 10), (benzer_mi, 10)])]
    return unit("eslik-ve-benzerlik-kosullari", "ES", "MAT.9.4.2", 11, "Eşlik ve Benzerlik Koşulları", "Eşlik ve Benzerlik Koşulları",
                "İki üçgenin eş veya benzer olması için gerekli asgari koşullarla (KKK, KAK, AKA; AA, KKK, KAK benzerlik) ilgili çıkarım yapar.",
                "9. sınıf eşlik ve benzerlik koşulları çalışma kâğıdı: KKK, KAK ve AKA eşlik, AA, KKK ve KAK benzerlik, karşılık gelen elemanlar, kenar oranlarıyla benzerlik. 100 soru ve cevap anahtarı.",
                "Eşlik: KKK, KAK, AKA", "Benzerlik: AA, KKK oranı, KAK oranı.", sets,
                ["Eşlik için üç kenar (KKK), iki kenar ve aradaki açı (KAK) ya da iki açı ve aradaki kenar (AKA) eşit olmalıdır.",
                 "Benzerlik için iki açının eşit olması (AA) yeter; ya da üç kenarın oranları eşit (KKK) ya da iki kenarın oranı ve aradaki açı eşit (KAK) olmalıdır.",
                 "ABC ≅ DEF ya da ABC ∼ DEF yazımında köşeler sırayla eşleşir: A↔D, B↔E, C↔F."],
                [("Açılar 50°, 60° ve 50°, 70°", ["Her ikisi de 50°, 60°, 70°"], "AA ile benzer"), ("Kenarlar 3, 4, 5 ve 6, 8, 10", ["Oranlar 2"], "KKK ile benzer")],
                [["AAA ile eş sanmak", "AAA yalnızca benzerlik verir"], ["Köşe sırasını karıştırmak", "Yazım sırasına göre eşle"],
                 ["Açı iki kenarın arasında değilken KAK demek", "Açı iki kenarın arasında olmalı"]],
                [("Eş üçgenler benzer midir?", "Evet, oranı 1 olan benzer üçgenlerdir."),
                 ("KKA neden eşlik koşulu değildir?", "İki farklı üçgen oluşabilir."),
                 ("Benzerlik oranı neyi gösterir?", "Karşılık gelen kenarların oranını.")])


def u12():
    oran, golge = reuse("tr_s8b", "u16", "oran"), reuse("tr_s8b", "u16", "golge")

    def alan_oran():
        k = ch([F(2), F(3), F(1, 2), F(3, 2), F(4), F(1, 3)])
        A_ = ri(2, 30)
        if (A_ * k * k).denominator != 1:
            return None
        v = A_ * k * k
        return M("Alanı %d cm² olan bir üçgen, kenarları %s katına çıkacak biçimde benzer bir üçgene dönüştürülüyor. Yeni üçgenin alanı kaç cm²’dir?" % (A_, sn(k)), sn(v),
                 [sn(A_ * k), sn(A_ * k * 2), sn(A_ + k)], "Alanlar oranı benzerlik oranının karesidir: %d · %s² = <b>%s cm²</b>." % (A_, par(k), sn(v)))

    def cevre_oran():
        a, b, c = ri(3, 12), ri(3, 12), ri(3, 12)
        if not (a + b > c and a + c > b and b + c > a):
            return None
        k = ri(2, 5)
        return M("Kenarları %d, %d ve %d cm olan üçgene benzer bir üçgenin en kısa kenarı %d cm’dir. Yeni üçgenin çevresi kaç cm’dir?" % (a, b, c, min(a, b, c) * k), num((a + b + c) * k),
                 [num(a + b + c + min(a, b, c) * (k - 1)), num((a + b + c) * k * k), num((a + b + c) * (k + 1))],
                 "Oran %d: çevre %d · %d = <b>%d cm</b>." % (k, a + b + c, k, (a + b + c) * k))

    sets = [("Benzer üçgen oluşturma", [(oran, 20)]),
            ("Çevreler oranı", [(cevre_oran, 20)]),
            ("Alanlar oranı", [(alan_oran, 20)]),
            ("Gölge problemleri", [(golge, 20)]),
            ("Karışık", [(oran, 7), (alan_oran, 7), (cevre_oran, 6)])]
    return unit("benzer-ucgenler-olusturma", "ES", "MAT.9.4.3", 12, "Benzer Üçgenler Oluşturma: Oran, Çevre ve Alan", "Benzer Üçgenler",
                "Bir üçgenden hareketle ona benzer üçgenler oluşturma ile ilgili yansıtma yapar; benzerlik oranının kenarlara, çevreye ve alana etkisini yorumlar.",
                "9. sınıf benzer üçgenler çalışma kâğıdı: benzerlik oranıyla kenar bulma, çevreler oranı, alanlar oranı (oranın karesi), gölge problemleri. 100 soru ve cevap anahtarı.",
                "Alanlar oranı = k²", "Kenarlar ve çevreler oranı k, alanlar oranı k².", sets,
                ["Benzer üçgenlerde karşılık gelen kenarların oranı benzerlik oranıdır: k.",
                 "Çevreler oranı da k’dir. Alanlar oranı ise k²’dir.",
                 "Bir üçgenin kenarlarını k ile çarparak benzer bir üçgen oluştururuz; açılar değişmez."],
                [("Kenarlar 2 katı", ["Çevre 2 katı", "Alan 4 katı"], "k = 2, k² = 4"), ("Alan 9 cm², oran 3", ["9 · 9"], "81 cm²")],
                [["Alanı da k katı almak", "Alan k² katı olur"], ["Oranı ters almak", "Yeni ÷ eski"], ["Açıları da k ile çarpmak", "Açılar değişmez"]],
                [("Benzer üçgen nasıl çizilir?", "Kenarları aynı oranla büyütür ya da küçültürüz; açılar aynı kalır."),
                 ("Hacimler oranı nedir?", "Benzer cisimlerde k³’tür."),
                 ("Fotoğraf büyütmek benzerlik midir?", "Evet, en ve boy aynı oranda büyür.")])


def u13():
    def tales():
        ad, db = ri(2, 9), ri(2, 9)
        ae = ri(2, 12)
        ec = F(ae * db, ad)
        if ec.denominator != 1:
            return None
        return M("Şekilde [DE] ∥ [BC]’dir. |AD| = %d, |DB| = %d, |AE| = %d ise |EC| = x kaçtır?%s" % (ad, db, ae, tales_fig(str(ad), str(db), str(ae), "x")), sn(ec),
                 [sn(F(ad * db, ae)) if (ad * db) % ae == 0 and F(ad * db, ae) != ec else sn(ec + 1), sn(ae + db - ad) if ae + db - ad > 0 and ae + db - ad != ec else sn(ec + 2), sn(db)] if db != ec else [sn(ec + 1), sn(ec + 2), sn(ae)],
                 "Tales: |AD|/|DB| = |AE|/|EC| → %d/%d = %d/x → x = <b>%s</b>." % (ad, db, ae, sn(ec)))

    def oklid():
        m = ch([1, 1, 2, 3])
        s_, t_ = ri(1, 5), ri(1, 5)
        if s_ == t_:
            return None
        p, k = m * s_ * s_, m * t_ * t_
        h = math.isqrt(p * k)
        kk = ri(0, 1)
        if kk == 0:
            return M("ABC dik üçgeninde A açısı 90°, [AH] hipotenüse ait yüksekliktir. |BH| = %d, |HC| = %d ise |AH| kaçtır?" % (p, k), num(h), [num(p + k), num((p + k) // 2), num(h + 1)],
                     "Öklid: |AH|² = |BH| · |HC| = %d → |AH| = <b>%d</b>." % (p * k, h))
        c2 = p * (p + k)
        r = math.isqrt(c2)
        if r * r != c2:
            return None
        return M("ABC dik üçgeninde A açısı 90°, [AH] hipotenüse ait yüksekliktir. |BH| = %d, |HC| = %d ise |AB| kaçtır?" % (p, k), num(r), [num(h), num(p + k), num(r + 1)],
                 "Öklid: |AB|² = |BH| · |BC| = %d · %d = %d → |AB| = <b>%d</b>." % (p, p + k, c2, r))

    hip, dik = reuse("tr_s8b", "u17", "hip"), reuse("tr_s8b", "u17", "dik_kenar")

    sets = [("Tales teoremi", [(tales, 20)]),
            ("Öklid bağıntıları", [(oklid, 20)]),
            ("Pisagor: hipotenüs", [(hip, 20)]),
            ("Pisagor: dik kenar", [(dik, 20)]),
            ("Karışık", [(tales, 7), (oklid, 7), (hip, 6)])]
    return unit("tales-oklid-ve-pisagor-teoremleri", "ES", "MAT.9.4.4", 13, "Tales, Öklid ve Pisagor Teoremleri", "Tales, Öklid, Pisagor",
                "Tales, Öklid ve Pisagor teoremlerini ispatlar ve bu teoremleri uzunluk hesaplarında kullanır.",
                "9. sınıf Tales, Öklid ve Pisagor teoremleri çalışma kâğıdı: paralel doğrular ve orantılı parçalar, dik üçgende hipotenüse ait yükseklik (Öklid bağıntıları), Pisagor teoremi. 100 soru ve cevap anahtarı.",
                "Tales: AD/DB = AE/EC", "Öklid: h² = p · k;  Pisagor: a² + b² = c².", sets,
                ["Tales: Bir üçgende bir kenara paralel çizilen doğru diğer iki kenarı orantılı parçalara ayırır: |AD|/|DB| = |AE|/|EC|.",
                 "Öklid: Dik üçgende hipotenüse ait yükseklik h, hipotenüsü p ve k parçalarına ayırırsa h² = p · k; dik kenar için b² = p · c.",
                 "Pisagor: Dik kenarların kareleri toplamı hipotenüsün karesine eşittir. Bu teoremler benzer üçgenlerle ispatlanır."],
                [("AD = 3, DB = 2, AE = 6", ["3/2 = 6/x"], "EC = 4"), ("BH = 4, HC = 9", ["h² = 36"], "h = 6")],
                [["Tales oranını AD/AB yerine AD/DB ile karıştırmak", "Aynı tür oranları eşle"], ["Öklid’de p + k kullanmak", "h² = p · k"],
                 ["Pisagor’u dik olmayan üçgende kullanmak", "Yalnızca dik üçgenlerde"]],
                [("Tales teoremi nasıl ispatlanır?", "ADE ve ABC üçgenlerinin AA ile benzer olduğu gösterilir."),
                 ("Öklid bağıntısı nereden gelir?", "Yükseklik dik üçgeni iki benzer dik üçgene ayırır."),
                 ("Pisagor teoreminin kaç ispatı var?", "Yüzlerce farklı ispatı vardır; biri benzer üçgenlerle yapılır.")])


def u14():
    tales_m = None

    def merdiven():
        return None
    merd, kos = reuse("tr_s8b", "u17", "merdiven"), reuse("tr_s8b", "u17", "kosegen")
    golge, oran = reuse("tr_s8b", "u16", "golge"), reuse("tr_s8b", "u16", "oran")
    bulmaca = reuse("tr_s8b", "u15", "bulmaca")

    def nehir():
        a, b = ri(2, 9) * 2, ri(2, 9) * 3
        c = ri(2, 6) * 2
        x = F(a * c, b) if False else None
        p, q = ri(3, 12), ri(3, 12)
        r = ri(4, 15)
        w = F(p * r, q)
        if w.denominator != 1:
            return None
        return M("Bir nehrin genişliğini ölçmek için benzer iki dik üçgen oluşturuluyor. Küçük üçgenin kenarları %d m ve %d m, büyük üçgende %d m’ye karşılık gelen kenar %d m’dir. Nehrin genişliği (büyük üçgende %d m’ye karşılık gelen kenar) kaç m’dir?" % (q, p, q, r, p),
                 "%s m" % sn(w), ["%s m" % sn(F(q * r, p)) if F(q * r, p) != w else "%s m" % sn(w + 1), "%s m" % sn(p + r - q) if p + r - q > 0 and p + r - q != w else "%s m" % sn(w + 2), "%s m" % sn(r)] if r != w else ["%s m" % sn(w + 1), "%s m" % sn(w + 2), "%s m" % sn(p)],
                 "Oran %d/%d: %d · %d/%d = <b>%s m</b>." % (r, q, p, r, q, sn(w)))

    sets = [("Gölge ve yükseklik", [(golge, 20)]),
            ("Mesafe ölçme", [(nehir, 20)]),
            ("Merdiven ve köşegen", [(merd, 10), (kos, 10)]),
            ("Eş üçgenlerle denklem", [(bulmaca, 20)]),
            ("Karışık", [(golge, 7), (nehir, 7), (oran, 6)])]
    return unit("eslik-ve-benzerlik-problemleri", "ES", "MAT.9.4.5", 14, "Eşlik ve Benzerlik Problemleri", "Eşlik ve Benzerlik Problemleri",
                "Eşlik ve benzerlikle ilgili çıkarım ve teoremleri (Tales, Öklid, Pisagor) içeren gerçek yaşam problemlerini çözer.",
                "9. sınıf eşlik ve benzerlik problemleri çalışma kâğıdı: gölgeyle yükseklik ölçme, benzer üçgenlerle nehir genişliği, merdiven ve köşegen, eş üçgenlerle denklem kurma. 100 soru ve cevap anahtarı.",
                "Benzer üçgen kur, oranı yaz", "Ulaşılamayan uzunlukları benzerlikle buluruz.", sets,
                ["Doğrudan ölçemediğimiz uzunlukları (ağaç yüksekliği, nehir genişliği) benzer üçgenler kurarak buluruz.",
                 "Güneş ışınları paralel geldiği için aynı anda oluşan gölgeler benzer üçgenler oluşturur.",
                 "Dik üçgen oluşan durumlarda Pisagor teoremini kullanırız."],
                [("2 m direk 3 m gölge, ağacın gölgesi 12 m", ["2/3 = h/12"], "h = 8 m"), ("Merdiven 13 m, alt uç 5 m", ["√(169 − 25)"], "12 m")],
                [["Oranı yanlış eşleştirmek", "Yükseklik/gölge = yükseklik/gölge"], ["Birimleri karıştırmak", "Hepsini aynı birime çevir"],
                 ["Dik üçgen olmayan durumda Pisagor kullanmak", "Dik açıyı kontrol et"]],
                [("Thales piramidin yüksekliğini nasıl ölçtü?", "Kendi gölgesinin boyuna eşit olduğu anda piramidin gölgesini ölçtü."),
                 ("Benzerlik haritalarda nasıl kullanılır?", "Ölçek, gerçek uzunluklarla haritadaki uzunlukların oranıdır."),
                 ("Eşlik problemlerde ne işe yarar?", "Eş üçgenlerin karşılık gelen kenarları eşit olduğu için bilinmeyen uzunlukları bulmayı sağlar.")])


# ============================================================ 15–16. algoritma ve mantık
def code(lines):
    return "<span class='code'>%s</span>" % "<br>".join(l.replace("  ", "&nbsp;&nbsp;") for l in lines)


def u15():
    def dongu():
        a, d, n = ri(0, 9), ri(2, 7), ri(3, 6)
        s = a + d * n
        return M("Aşağıdaki algoritmanın çıktısı nedir?%s" % code(["1. s ← %d" % a, "2. %d kez tekrarla: s ← s + %d" % (n, d), "3. s değerini yaz"]), num(s),
                 [num(a + d * (n - 1)), num(a + d + n), num(a * d * n) if a * d * n != s else num(s + d)], "%d + %d · %d = <b>%d</b>." % (a, n, d, s))

    def toplam():
        n = ri(4, 15)
        k = ch(["tek", "çift", "hepsi"])
        vals = [i for i in range(1, n + 1) if k == "hepsi" or (i % 2 == 1) == (k == "tek")]
        s = sum(vals)
        cond = {"tek": "i tek ise ", "çift": "i çift ise ", "hepsi": ""}[k]
        return M("Algoritma: t ← 0; i = 1, 2, …, %d değerlerinin her biri için %st ← t + i; sonunda t yazılır. Çıktı kaçtır?" % (n, cond), num(s), [num(s + n), num(s - vals[-1]), num(n * (n + 1) // 2) if k != "hepsi" else num(s + 1)],
                 "Toplanan sayılar: %s → <b>%d</b>." % (", ".join(map(str, vals)), s))

    def kosul():
        x = ri(-20, 30)
        a = ri(0, 15)
        out = 2 * x if x > a else x - a
        return M("x = %s için algoritmanın çıktısı nedir?%s" % (sn(x), code(["Eğer x &gt; %d ise y ← 2x" % a, "Değilse y ← x − %d" % a, "y değerini yaz"])), sn(out),
                 [sn(x - a) if x > a else sn(2 * x), sn(out + 1), sn(-out) if out else "1"], "%s %s %d olduğundan %s → <b>%s</b>." % (sn(x), "&gt;" if x > a else "≤", a, "y = 2x" if x > a else "y = x − %d" % a, sn(out)))

    def ebob():
        a, b = ri(12, 99), ri(12, 99)
        x, y = max(a, b), min(a, b)
        steps = 0
        while y:
            x, y = y, x % y
            steps += 1
        g = x
        return M("Algoritma (Öklid): a ← %d, b ← %d; b ≠ 0 oldukça (a, b) ← (b, a’nın b ile bölümünden kalan); sonunda a yazılır. Çıktı kaçtır?" % (max(a, b), min(a, b)), num(g),
                 [num(min(a, b)), num(g * 2) if g * 2 != max(a, b) else num(g + 1), num(max(a, b) - min(a, b)) if max(a, b) - min(a, b) != g else num(g + 3)],
                 "Bu algoritma iki sayının en büyük ortak bölenini bulur: <b>%d</b>." % g)

    sets = [("Tekrar eden adımlar", [(dongu, 20)]),
            ("Koşullu adımlar", [(kosul, 20)]),
            ("Toplam algoritmaları", [(toplam, 20)]),
            ("Öklid algoritması", [(ebob, 20)]),
            ("Karışık", [(dongu, 7), (kosul, 7), (toplam, 6)])]
    return unit("algoritma-temelli-problemler", "AB", "MAT.9.5.1", 15, "Algoritma Temelli Problemler", "Algoritmalar",
                "Algoritma temelli yaklaşımlarla problem çözer; tekrar ve koşul yapıları içeren algoritmaları izleyerek çıktıyı bulur.",
                "9. sınıf algoritma çalışma kâğıdı: tekrar eden adımlar, koşullu yapılar (eğer-değilse), toplam algoritmaları, en büyük ortak böleni bulan Öklid algoritması. 100 soru ve cevap anahtarı.",
                "Adım adım izle", "Değişkenin değerini her adımda bir tabloya yaz.", sets,
                ["Algoritma, bir problemi çözmek için sıralı ve açık adımlardır.",
                 "Tekrar yapısında aynı adımlar belli sayıda ya da bir koşul sağlandıkça yinelenir.",
                 "Koşul yapısında (eğer … ise … değilse …) koşulun doğru ya da yanlış olmasına göre farklı adım uygulanır."],
                [("s ← 3; 4 kez s ← s + 5", ["3 + 4 · 5"], "23"), ("a = 48, b = 18", ["(18, 12) → (12, 6) → (6, 0)"], "6")],
                [["Tekrar sayısını bir eksik saymak", "Her tekrarı tabloya yaz"], ["Koşulda ≤ ile &lt;’yi karıştırmak", "Sınır değeri kontrol et"],
                 ["Değişkenin eski değerini kullanmak", "Her adımda güncel değeri kullan"]],
                [("Algoritma ile program farkı nedir?", "Algoritma adımların planıdır; program bu planın bir dilde yazılmış hâlidir."),
                 ("Öklid algoritması neden önemli?", "Bilinen en eski algoritmalardan biridir ve EBOB’u hızlıca bulur."),
                 ("Akış şeması nedir?", "Algoritmanın şekillerle gösterimidir.")])


def u16():
    def baglac():
        p, q = ch([True, False]), ch([True, False])
        op = ch(["∧", "∨", "⇒", "⇔"])
        v = {"∧": p and q, "∨": p or q, "⇒": (not p) or q, "⇔": p == q}[op]
        T = lambda b: "1" if b else "0"
        return M("p ≡ %s ve q ≡ %s ise p %s q önermesinin doğruluk değeri nedir?" % (T(p), T(q), op), T(v), [T(not v), "Belirlenemez", "Hem 0 hem 1"],
                 "%s: %s. Cevap: <b>%s</b>." % ({"∧": "“ve” yalnızca ikisi 1 iken 1", "∨": "“veya” en az biri 1 iken 1", "⇒": "“ise” yalnızca 1 ⇒ 0 durumunda 0", "⇔": "“ancak ve ancak” değerler aynıysa 1"}[op], "", T(v)))

    def onerme():
        a = ri(2, 20)
        S = [("%d bir asal sayıdır." % a, all(a % d for d in range(2, a))), ("%d bir çift sayıdır." % a, a % 2 == 0),
             ("%d sayısı 3 ile tam bölünür." % a, a % 3 == 0), ("%d &gt; 10" % a, a > 10)]
        t, v = ch(S)
        u = ch(S)
        if u[0] == t:
            return None
        op = ch(["ve", "veya"])
        val = (v and u[1]) if op == "ve" else (v or u[1])
        g = "Doğru" if val else "Yanlış"
        return M("“%s %s %s” bileşik önermesi doğru mu, yanlış mı?" % (t.rstrip("."), op, u[0].rstrip(".").lower() if u[0][0].isalpha() else u[0].rstrip(".")), g,
                 ["Yanlış" if val else "Doğru", "Belirlenemez", "Önerme değildir"], "Birinci %s, ikinci %s; “%s” → <b>%s</b>." % ("doğru" if v else "yanlış", "doğru" if u[1] else "yanlış", op, g.lower()))

    def degil():
        S = [("Her öğrenci okula gelmiştir.", "Okula gelmeyen en az bir öğrenci vardır."), ("Bazı sayılar çifttir.", "Hiçbir sayı çift değildir."),
             ("∀x ∈ ℝ, x² ≥ 0", "∃x ∈ ℝ, x² &lt; 0"), ("∃x ∈ ℕ, x + 3 = 1", "∀x ∈ ℕ, x + 3 ≠ 1"), ("Bütün kareler dikdörtgendir.", "Dikdörtgen olmayan en az bir kare vardır."),
             ("p ∧ q", "p′ ∨ q′"), ("p ∨ q", "p′ ∧ q′"), ("∀x ∈ ℤ, 2x çifttir.", "∃x ∈ ℤ, 2x çift değildir.")]
        t, g = ch(S)
        w = [x for _, x in S if x != g][:6]
        return M("“%s” önermesinin olumsuzu (değili) hangisidir?" % t, g, sh(w)[:3], "Değil alırken ∀ ↔ ∃ değişir, koşul olumsuzlanır; ∧ ↔ ∨ değişir. Cevap: <b>%s</b>." % g)

    def nicel():
        S = [("∀x ∈ ℝ, x² + 1 &gt; 0", "Doğru"), ("∃x ∈ ℤ, 2x = 7", "Yanlış"), ("∃x ∈ ℝ, x² = 2", "Doğru"), ("∀x ∈ ℕ, x ≥ 1", "Yanlış"),
             ("∀x ∈ ℤ, x + 0 = x", "Doğru"), ("∃x ∈ ℚ, x² = 2", "Yanlış"), ("∀x ∈ ℝ, |x| ≥ 0", "Doğru"), ("∃x ∈ ℕ, x &lt; 0", "Yanlış"),
             ("∀x ∈ ℝ, 2x &gt; x", "Yanlış"), ("∃x ∈ ℝ, x + 5 = 2", "Doğru")]
        t, g = ch(S)
        return M("“%s” önermesi doğru mu, yanlış mı?" % t, g, ["Yanlış" if g == "Doğru" else "Doğru", "Önerme değildir", "Belirlenemez"],
                 "∀ (her) için tek bir karşı örnek yanlış yapar; ∃ (en az bir) için tek bir örnek doğru yapar. Cevap: <b>%s</b>." % g)

    def alg():
        x = ri(1, 40)
        a, b = ri(5, 20), ri(2, 5)
        cond = "x &gt; %d ve x, %d ile tam bölünür" % (a, b)
        cond2 = "x &gt; %d veya x, %d ile tam bölünür" % (a, b)
        k = ch([0, 1])
        c = (x > a and x % b == 0) if k == 0 else (x > a or x % b == 0)
        out = "EVET" if c else "HAYIR"
        return M("x = %d için çıktı nedir?%s" % (x, code(["Eğer %s ise “EVET” yaz" % (cond if k == 0 else cond2), "Değilse “HAYIR” yaz"])), out, ["HAYIR" if c else "EVET", "Çıktı yoktur", "EVET ve HAYIR"],
                 "%d &gt; %d: %s; %d, %d ile bölünür: %s; “%s” → <b>%s</b>." % (x, a, "doğru" if x > a else "yanlış", x, b, "doğru" if x % b == 0 else "yanlış", "ve" if k == 0 else "veya", out))

    sets = [("Bağlaçlar ve doğruluk değeri", [(baglac, 16), (alg, 4)]),
            ("Bileşik önermeler", [(onerme, 20)]),
            ("Niceleyiciler", [(nicel, 10), (degil, 8), (onerme, 2)]),
            ("Algoritmalarda bağlaçlar", [(alg, 20)]),
            ("Karışık", [(onerme, 10), (alg, 10)])]
    return unit("mantik-baglaclari-ve-niceleyiciler", "AB", "MAT.9.5.2, MAT.9.5.3", 16, "Mantık Bağlaçları ve Niceleyiciler", "Mantık Bağlaçları",
                "Algoritmik yapılar içerisindeki mantık bağlaçlarını (ve, veya, ise, ancak ve ancak, değil) ve niceleyicileri (her, en az bir) çözümler ve algoritmalarda kullanır.",
                "9. sınıf mantık bağlaçları ve niceleyiciler çalışma kâğıdı: ve, veya, ise, ancak ve ancak bağlaçlarının doğruluk değerleri, bileşik önermeler, her ve en az bir niceleyicileri, olumsuzlama, algoritmalarda koşullar. 100 soru ve cevap anahtarı.",
                "∧ ve, ∨ veya, ⇒ ise, ∀ her, ∃ en az bir", "Değil alırken ∀ ile ∃ yer değiştirir.", sets,
                ["“ve” (∧) bağlacıyla kurulan önerme yalnızca iki önerme de doğruysa doğrudur. “veya” (∨) en az biri doğruysa doğrudur.",
                 "p ⇒ q yalnızca p doğru, q yanlış iken yanlıştır. p ⇔ q, p ve q aynı değerdeyse doğrudur.",
                 "∀ “her”, ∃ “en az bir” demektir. ∀x için önermenin değili ∃x için koşulun değilidir."],
                [("p ≡ 1, q ≡ 0, p ∧ q", ["İkisi de 1 değil"], "0"), ("∀x ∈ ℝ, x² ≥ 0 değili", ["∀ → ∃", "≥ → &lt;"], "∃x ∈ ℝ, x² &lt; 0")],
                [["“veya”yı “ya … ya …” sanmak", "Matematikte veya ikisi birden doğru olunca da doğrudur"], ["p ⇒ q’yu p yanlışken yanlış saymak", "p yanlışsa p ⇒ q doğrudur"],
                 ["Değil alırken niceleyiciyi değiştirmemek", "∀ ↔ ∃"]],
                [("Önerme nedir?", "Doğru ya da yanlış olduğu kesin olarak söylenebilen ifadedir."),
                 ("Algoritmalarda bağlaçlar nerede kullanılır?", "Koşullu yapılarda (eğer x &gt; 0 ve x &lt; 10 ise …)."),
                 ("De Morgan kuralı nedir?", "(p ∧ q)′ ≡ p′ ∨ q′ ve (p ∨ q)′ ≡ p′ ∧ q′.")])


# ============================================================ 17. veri
def u17():
    ozet = reuse("tr_s8b", "u22", "ozet")
    sapma = reuse("tr_s7c", "u25", "sapma")

    def ceyrek():
        n = ch([7, 9, 11])
        xs = sorted(ri(1, 60) for _ in range(n))
        if len(set(xs)) < n - 1:
            return None
        lo, hi = xs[:n // 2], xs[n // 2 + 1:]
        med = lambda a: F(a[len(a) // 2]) if len(a) % 2 else F(a[len(a) // 2 - 1] + a[len(a) // 2], 2)
        q1, q3 = med(lo), med(hi)
        k = ch(["Q1", "Q3", "IQR"])
        v = {"Q1": q1, "Q3": q3, "IQR": q3 - q1}[k]
        name = {"Q1": "alt çeyreği (Q1)", "Q3": "üst çeyreği (Q3)", "IQR": "çeyrekler açıklığı (Q3 − Q1)"}[k]
        shown = sh(xs)
        return M("%s verilerinin %s kaçtır?" % (", ".join(map(str, shown)), name), dq(v, 1) if v.denominator > 1 else sn(v),
                 [dq(x, 1) if F(x).denominator > 1 else sn(x) for x in {q1, q3, q3 - q1, F(xs[n // 2]), F(xs[-1] - xs[0])} if x != v],
                 "Sıralı: %s. Ortanca %d; alt yarı %s, üst yarı %s. Q1 = %s, Q3 = %s → <b>%s</b>." % (", ".join(map(str, xs)), xs[n // 2], ", ".join(map(str, lo)), ", ".join(map(str, hi)), dq(q1, 1) if q1.denominator > 1 else sn(q1), dq(q3, 1) if q3.denominator > 1 else sn(q3), dq(v, 1) if v.denominator > 1 else sn(v)))

    def aykiri():
        base = sorted(ri(20, 40) for _ in range(6))
        out = ri(90, 150)
        xs = base + [out]
        mean = F(sum(xs), 7)
        medn = sorted(xs)[3]
        g = "Ortanca, çünkü uç değerden az etkilenir"
        return M("%s verilerinde %d bir uç (aykırı) değerdir. Verinin merkezini en iyi gösteren ölçü hangisidir?" % (", ".join(map(str, sh(xs))), out), g,
                 ["Aritmetik ortalama, çünkü bütün verileri kullanır", "Açıklık, çünkü en büyük ve en küçüğü gösterir", "En büyük değer"],
                 "Ortalama %s, ortanca %d; ortalama uç değer yüzünden büyümüştür. Cevap: <b>ortanca</b>." % (dq(mean, 1), medn))

    def yorum():
        a1, a2 = ri(55, 80), ri(55, 80)
        s1, s2 = ri(3, 15), ri(3, 15)
        if a1 == a2 or s1 == s2:
            return None
        k = ch(["daha tutarlı", "ortalaması daha yüksek"])
        g = ("A sınıfı" if s1 < s2 else "B sınıfı") if k == "daha tutarlı" else ("A sınıfı" if a1 > a2 else "B sınıfı")
        return M("A sınıfı: ortalama %d, standart sapma %d. B sınıfı: ortalama %d, standart sapma %d. Hangi sınıfın notları %s?" % (a1, s1, a2, s2, k), g,
                 ["B sınıfı" if g == "A sınıfı" else "A sınıfı", "İkisi aynı", "Bilinemez"],
                 "%s. Cevap: <b>%s</b>." % ("Standart sapması küçük olan daha tutarlıdır" if k == "daha tutarlı" else "Ortalamaları karşılaştırırız", g))

    sets = [("Merkez ve yayılım", [(ozet, 20)]),
            ("Çeyrekler", [(ceyrek, 20)]),
            ("Ortalama mutlak sapma", [(sapma, 20)]),
            ("Uç değerler ve yorum", [(aykiri, 10), (yorum, 10)]),
            ("Karışık", [(ceyrek, 7), (yorum, 7), (ozet, 6)])]
    return unit("tek-nicel-degiskenli-veri", "IA", "MAT.9.6.1, MAT.9.6.2", 17, "Tek Nicel Değişkenli Veri: Merkez, Yayılım ve Çeyrekler", "Tek Değişkenli Veri",
                "Tek nicel değişkenli veri dağılımlarıyla çalışır; merkezi eğilim ve yayılım ölçülerini, çeyrekleri ve uç değerleri kullanarak veriye dayalı karar verir ve başkalarının yorumlarını tartışır.",
                "9. sınıf veri analizi çalışma kâğıdı: ortalama, ortanca, tepe değer ve açıklık, alt ve üst çeyrek, çeyrekler açıklığı, ortalama mutlak sapma, uç değerler ve standart sapmayla yorum. 100 soru ve cevap anahtarı.",
                "Merkez + yayılım = dağılımın özeti", "Uç değer varsa ortanca daha iyi bir merkez ölçüsüdür.", sets,
                ["Merkezi eğilim ölçüleri (ortalama, ortanca, tepe değer) verinin nerede toplandığını gösterir.",
                 "Yayılım ölçüleri (açıklık, çeyrekler açıklığı, ortalama mutlak sapma, standart sapma) verinin ne kadar dağıldığını gösterir.",
                 "Çeyrekler sıralı veriyi dört eşit parçaya böler: Q1 alt yarının, Q3 üst yarının ortancasıdır."],
                [("3, 5, 7, 8, 10, 12, 15", ["Ortanca 8", "Q1 = 5, Q3 = 12"], "IQR = 7"), ("Notlar 60, 62, 65, 98", ["98 uç değer"], "Ortanca tercih edilir")],
                [["Çeyrekleri sıralamadan bulmak", "Önce küçükten büyüğe sırala"], ["Uç değerli veride ortalamaya güvenmek", "Ortancaya da bak"],
                 ["Küçük standart sapmayı kötü sanmak", "Küçük sapma tutarlılık demektir"]],
                [("Kutu grafiği nedir?", "En küçük, Q1, ortanca, Q3 ve en büyük değeri gösteren grafiktir."),
                 ("Standart sapma neyi gösterir?", "Verilerin ortalamadan ortalama ne kadar uzaklaştığını."),
                 ("Bir istatistiksel yorumu nasıl değerlendiririm?", "Verinin nasıl toplandığına, örneklemin büyüklüğüne ve hangi ölçünün kullanıldığına bakarım.")])


# ============================================================ 18. olasılık
def u18():
    deneysel, tahmin = reuse("tr_s8b", "u23", "deneysel"), reuse("tr_s8b", "u23", "tahmin")
    torba, tumleyen = reuse("tr_s7c", "u26", "torba"), reuse("tr_s7c", "u26", "tumleyen")

    def iki_zar():
        s = ri(2, 12)
        k = ch(["toplamı %d" % s, "toplamı %d’den büyük" % s if False else "toplamı en az %d" % s])
        if "en az" in k:
            c = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b >= s)
        else:
            c = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == s)
        p = F(c, 36)
        return M("İki zar birlikte atılıyor. Üst yüzlerdeki sayıların %s olma olasılığı kaçtır?" % k, sn(p), [sn(F(c, 12)) if F(c, 12) <= 1 and F(c, 12) != p else sn(F(c + 1, 36)), sn(1 - p) if 1 - p != p else sn(F(1, 2) + F(1, 36)), sn(F(c, 11)) if F(c, 11) <= 1 else sn(F(1, 6))],
                 "36 eşit olası sonuçtan %d tanesi uygun: %d/36 = <b>%s</b>." % (c, c, sn(p)))

    def tumevarim():
        n = ch([10, 50, 100, 1000])
        c = ri(n // 10, n // 2)
        g = "Deney sayısı arttıkça oran teorik olasılığa yaklaşır"
        return M("Bir para %d kez atıldı, %d kez yazı geldi. Bu deneyin %d kez daha tekrarlanması hakkında hangisi en doğrudur?" % (n, c, n * 10), g,
                 ["Bundan sonra daha çok tura gelir", "Yazı gelme oranı tam %s olur" % sn(F(c, n)), "Sonuç önceden kesin bilinir"],
                 "Tümevarımsal akıl yürütme: çok sayıda deneyde oran 1/2’ye yaklaşır. Cevap: <b>bu ifadedir</b>.")

    sets = [("Deneysel olasılık", [(deneysel, 20)]),
            ("Beklenen sonuç", [(tahmin, 16), (tumevarim, 4)]),
            ("Teorik olasılık", [(torba, 20)]),
            ("İki zar", [(iki_zar, 20)]),
            ("Karışık", [(torba, 7), (tahmin, 7), (deneysel, 6)])]
    return unit("deneysel-ve-teorik-olasilik", "VO", "MAT.9.7.1, MAT.9.7.2", 18, "Deneysel ve Teorik Olasılık", "Olasılık",
                "Olayların olasılığını gözleme dayalı tahmin eder; deneysel olasılıktan teorik olasılığa tümevarımsal akıl yürütür.",
                "9. sınıf olasılık çalışma kâğıdı: deneysel olasılık, beklenen sonuç sayısı, büyük sayılar ve tümevarımsal akıl yürütme, teorik olasılık, iki zarın toplamı. 100 soru ve cevap anahtarı.",
                "P(A) = uygun ÷ tüm sonuçlar", "Çok deneyde deneysel olasılık teoriğe yaklaşır.", sets,
                ["Deneysel olasılık = olayın gözlenme sayısı ÷ deney sayısı.",
                 "Çıktılar eşit olasılıklıysa teorik olasılık P(A) = uygun sonuç sayısı ÷ tüm sonuç sayısıdır.",
                 "Deney çok kez tekrarlandıkça deneysel olasılık teorik olasılığa yaklaşır; bu gözlemden genel bir sonuca varmak tümevarımsal akıl yürütmedir."],
                [("İki zar, toplam 7", ["(1,6), (2,5), (3,4), (4,3), (5,2), (6,1)", "6/36"], "1/6"), ("200 atışta 52 kez 6", ["52/200"], "13/50")],
                [["İki zarda 11 sonuç saymak", "36 sıralı sonuç vardır"], ["Az deneyle kesin sonuç çıkarmak", "Çok deney gerekir"],
                 ["Bir önceki sonucun sonrakini etkilediğini sanmak", "Atışlar bağımsızdır"]],
                [("Kumarbaz yanılgısı nedir?", "Art arda yazı geldi diye sıradakinin tura olacağını sanmaktır; atışlar bağımsızdır."),
                 ("Benzetim (simülasyon) neden kullanılır?", "Deneyi bilgisayarla çok kez tekrarlayıp olasılığı tahmin etmek için."),
                 ("Olasılık 0 ve 1 ne demek?", "0 imkânsız, 1 kesin olaydır.")])


UNITS = [u5, u6, u7, u8, u9, u10, u11, u12, u13, u14, u15, u16, u17, u18]
