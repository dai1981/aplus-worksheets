# -*- coding: utf-8 -*-
"""Türkiye 6. sınıf (Maarif Modeli, Ortaokul Matematik 2026): İşlemlerle Cebirsel Düşünme ve Değişimler, Geometrik Şekiller, Geometrik Nicelikler,
İstatistiksel Araştırma Süreci, Veriden Olasılığa — 11〜22 単元。"""
import math
import random as _r
from fractions import Fraction as F
import tr_g as G
from tr_g import unit, cap, fr, ff, num, dec, mcq, M, wrap, text, line, poly, circle_fig, stem_leaf, dot_plot, freq_table, NB, INK, GREEN, FILL, RED, BLUE
from tr_common import low
import gen_au_maths_y5_angles as AU
from gen_au_maths_y5_angles import Pic, pol

AU.random = _r
O = (0.0, 0.0)


def setup(rnd):
    pass


def ri(a, b):
    return G.R.randint(a, b)


def ch(xs):
    return G.R.choice(list(xs))


def sh(xs):
    return G.sh(xs)


def fig(svg, lab="geometrik şekil"):
    return "<div class='qfig'>" + G.lg(svg.replace("aria-label='marked angle'", "aria-label='%s'" % lab)) + "</div>"


VARS = ["x", "a", "b", "n", "y", "m", "k", "t"]


def ex(a, v, b):
    """a·v + b → '3x + 5', 'x − 2', '4n'"""
    t = ("%s" % v) if a == 1 else ("%d%s" % (a, v))
    if b > 0:
        t += " + %d" % b
    elif b < 0:
        t += " − %d" % -b
    return t


# ============================================================ 11. cebirsel ifadeler
SOZ = [("%s sayısının %d katının %d fazlası", lambda a, b: (a, b)), ("%s sayısının %d katının %d eksiği", lambda a, b: (a, -b)),
       ("%s sayısının %d fazlasının iki katı", None)]


def u11():
    def yaz():
        v = ch(VARS)
        a, b = ri(2, 9), ri(1, 15)
        k = ri(0, 3)
        if k == 0:
            q, g = "Bir %s sayısının %d katının %d fazlası" % (v, a, b), ex(a, v, b)
            w = [ex(a, v, -b), "%d(%s + %d)" % (a, v, b), "%s + %d" % (ex(a, v, 0), a * b) if a * b != b else ex(b, v, a)]
        elif k == 1:
            q, g = "Bir %s sayısının %d katının %d eksiği" % (v, a, b), ex(a, v, -b)
            w = [ex(a, v, b), "%d(%s − %d)" % (a, v, b), "%d − %s" % (b, ex(a, v, 0))]
        elif k == 2:
            q, g = "Bir %s sayısının %d fazlasının %d katı" % (v, b, a), "%d(%s + %d)" % (a, v, b)
            w = [ex(a, v, b), "%s + %d" % (v, a * b), "%d(%s − %d)" % (a, v, b)]
        else:
            q, g = "Bir %s sayısının yarısının %d fazlası" % (v, b), "%s ÷ 2 + %d" % (v, b)
            w = ["(%s + %d) ÷ 2" % (v, b), "2%s + %d" % (v, b), "%s ÷ 2 − %d" % (v, b)]
        return mcq("“%s” ifadesinin cebirsel gösterimi hangisidir?" % q, g, w, "<b>%s</b>." % g)

    def degeri():
        v = ch(VARS)
        a, b = ri(2, 9), ri(-12, 15)
        x = ri(2, 12)
        e = ex(a, v, b)
        g = a * x + b
        return mcq("%s = %d için %s ifadesinin değeri kaçtır?" % (v, x, e), str(g), [str(a + x + b), str(int(str(a) + str(x)) + b), str(a * x - b) if b else str(g + a)],
                   "%s yerine %d yazılır: %d × %d %s %d = <b>%d</b>." % (v, x, a, x, "+" if b >= 0 else "−", abs(b), g))

    def terim():
        v = ch(VARS)
        a, b = ri(2, 12), ri(1, 20)
        e = ex(a, v, b)
        k = ri(0, 2)
        if k == 0:
            return mcq("%s cebirsel ifadesinde %s teriminin katsayısı kaçtır?" % (e, ex(a, v, 0)), str(a), [str(b), v, str(a + b)], "Değişkenin önündeki sayı katsayıdır: <b>%d</b>." % a)
        if k == 1:
            return mcq("%s cebirsel ifadesinde sabit terim hangisidir?" % e, str(b), [str(a), ex(a, v, 0), v], "Değişken içermeyen terim sabit terimdir: <b>%d</b>." % b)
        c = ri(2, 9)
        e3 = "%s + %s + %d" % (ex(a, v, 0), ex(c, ch([x for x in VARS if x != v]), 0), b)
        return mcq("%s cebirsel ifadesi kaç terimden oluşur?" % e3, "3", ["2", "4", "1"], "Terimler “+” ve “−” ile ayrılır: <b>3</b> terim.")

    def sozel():
        v = ch(VARS)
        a, b = ri(2, 9), ri(1, 15)
        e = ex(a, v, b)
        g = "%s sayısının %d katının %d fazlası" % (v, a, b)
        return mcq("%s ifadesinin sözel karşılığı hangisidir?" % e, g, ["%s sayısının %d fazlasının %d katı" % (v, b, a), "%s sayısının %d katının %d eksiği" % (v, a, b), "%s sayısının %d katı" % (v, a + b)],
                   "%s → <b>%s</b>." % (e, g))

    def hayat():
        nm = G.K.next()
        a, b = ri(5, 40), ri(10, 90)
        k = ri(0, 2)
        if k == 0:
            q, g = "Tanesi %d TL olan defterlerden x tane ve %d TL’lik bir çanta alan %s kaç lira öder?" % (a, b, nm), ex(a, "x", b)
            w = [ex(b, "x", a), "%d(x + %d)" % (a, b), "x + %d" % (a + b)]
        elif k == 1:
            q, g = "x TL parası olan %s %d TL harcadı. Kalan parasını gösteren ifade hangisidir?" % (nm, b), "x − %d" % b
            w = ["%d − x" % b, "x + %d" % b, "%dx" % b]
        else:
            q, g = "Bir kenarı x cm olan karenin çevresini gösteren ifade hangisidir?", "4x"
            w = ["x + 4", "x × x", "2x"]
            q = "Bir kenarı %s cm olan eşkenar üçgenin çevresini gösteren ifade hangisidir?" % ch(VARS) if ri(0, 1) else q
            if "üçgen" in q:
                v = q.split("Bir kenarı ")[1].split(" cm")[0]
                g, w = "3%s" % v, ["%s + 3" % v, "%s × %s × %s" % (v, v, v), "2%s" % v]
            else:
                g, w = "4x", ["x + 4", "x × x", "2x"]
        return mcq(q, g, w, "<b>%s</b>." % g)

    sets = [("Cebirsel ifade yazma", [(yaz, 20)]),
            ("İfadenin değeri", [(degeri, 20)]),
            ("Terim, katsayı, sabit terim", [(terim, 20)]),
            ("Sözel ifade", [(sozel, 20)]),
            ("Günlük hayatta cebirsel ifadeler", [(hayat, 12), (degeri, 8)])]
    return unit("cebirsel-ifadeler", "C6", "MAT.6.2.1", 11, "Cebirsel İfadeler: Değişken, Terim, Katsayı ve İfadenin Değeri", "Cebirsel İfadeler",
                "Bilinen niceliklerden bilinmeyen niceliklere ilişkin akıl yürütür; ilişkileri cebirsel ifadelerle gösterir ve açıklar.",
                "6. sınıf cebirsel ifadeler çalışma kâğıdı: sözel ifadeyi cebirsel ifadeye çevirme, değişken, terim, katsayı ve sabit terim, bir cebirsel ifadenin değeri ve günlük hayat problemleri. 100 soru ve cevap anahtarı.",
                "Bilinmeyeni bir harfle göster", "3x + 5: katsayı 3, sabit terim 5.", sets,
                ["Bilinmeyen bir niceliği x, a, n gibi bir harfle gösteririz; bu harfe değişken denir.",
                 "Bir sayının 3 katı 3x, 5 fazlası x + 5, 2 eksiği x − 2 diye yazılır. “3 katının 5 fazlası” 3x + 5 olur.",
                 "3x + 5 ifadesinde 3x ve 5 terimdir; 3 katsayı, 5 sabit terimdir. İfadenin değerini bulmak için değişkenin yerine sayıyı yazarız."],
                [("Bir sayının 4 katının 7 eksiği", ["4 katı: 4x", "7 eksiği: − 7"], "4x − 7"), ("a = 6 için 5a + 2", ["5 × 6 + 2"], "32")],
                [["“3 katının 5 fazlası” → 3(x + 5)", "Önce 3 katı, sonra 5 fazlası: 3x + 5"], ["3x’i 3 + x sanmak", "3x = 3 × x"],
                 ["Değer bulurken 5a’yı 56 diye yazmak (a = 6)", "5a = 5 × 6 = 30"]],
                [("Değişken neden harfle gösterilir?", "Değeri bilinmeyen ya da değişebilen nicelikleri kısa ve genel biçimde yazmak için."),
                 ("Katsayı 1 ise yazılır mı?", "Genellikle yazılmaz: 1x yerine x yazılır."),
                 ("Cebirsel ifade ile denklem arasındaki fark nedir?", "Cebirsel ifadede eşittir yoktur (3x + 5); denklemde vardır (3x + 5 = 20).")])


# ============================================================ 12. örüntüler ve cebirsel ifadeler
def u12():
    def kural():
        a, b = ri(2, 9), ri(-5, 8)
        xs = [a * n + b for n in range(1, 6)]
        if xs[0] <= 0:
            return None
        g = ex(a, "n", b)
        return mcq("%s, … örüntüsünün n. terimini veren cebirsel ifade hangisidir?" % ", ".join(map(str, xs)), g, [ex(a, "n", b + 1), ex(a + 1, "n", b - 1), "n + %d" % a, ex(xs[0], "n", 0)],
                   "Her adımda %d artıyor: %dn. 1. terim için %d × 1 = %d, terim %d → <b>%s</b>." % (a, a, a, a, xs[0], g))

    def terim():
        a, b = ri(2, 12), ri(-6, 10)
        n = ch([10, 15, 20, 25, 40, 50, 100])
        g = a * n + b
        if g <= 0:
            return None
        e = ex(a, "n", b)
        return mcq("n. terimi %s olan örüntünün %d. terimi kaçtır?" % (e, n), num(g), [num(a * n), num(g + a), num(a + n + b)], "n = %d: %d × %d %s %d = <b>%s</b>." % (n, a, n, "+" if b >= 0 else "−", abs(b), num(g)))

    def tablo():
        a, b = ri(2, 9), ri(-4, 9)
        rows = "".join("<tr><td style='text-align:center'>%d</td><td style='text-align:center'>%d</td></tr>" % (n, a * n + b) for n in range(1, 5))
        if a + b <= 0:
            return None
        tab = "<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr><th>Adım (n)</th><th>Terim</th></tr></thead><tbody>%s</tbody></table>" % rows
        g = ex(a, "n", b)
        return mcq("Tablodaki ilişkiyi gösteren cebirsel ifade hangisidir?%s" % tab, g, [ex(a, "n", b + a), ex(a + b, "n", 0) if a + b != a else ex(a + 1, "n", b), "n + %d" % (a + b)],
                   "Terimler her adımda %d artıyor: %dn. n = 1 için %d → <b>%s</b>." % (a, a, a + b, g))

    def sekil():
        a, b = ri(2, 6), ri(0, 4)
        counts = [a * n + b for n in range(1, 4)]
        from tr_s5b import sq_pat
        pic = sq_pat(counts)
        g = ex(a, "n", b)
        return mcq("Şekil örüntüsünde n. adımdaki kare sayısını veren ifade hangisidir?%s" % pic, g, [ex(a, "n", b + 1), ex(a + 1, "n", b - 1 if b > 0 else 0) if ex(a + 1, "n", b - 1 if b > 0 else 0) != g else ex(a + 2, "n", b), "n + %d" % a],
                   "Kareler %d, %d, %d: her adımda %d artıyor. n = 1 için %d → <b>%s</b>." % (counts[0], counts[1], counts[2], a, counts[0], g))

    def kacinci():
        a, b = ri(2, 9), ri(-5, 9)
        n = ri(8, 40)
        v = a * n + b
        if v <= 0:
            return None
        e = ex(a, "n", b)
        return mcq("n. terimi %s olan örüntüde %s kaçıncı terimdir?" % (e, num(v)), "%d. terim" % n, ["%d. terim" % x for x in (n + 1, n - 1, v // a if v // a != n else n + 2)],
                   "%s = %s → n = <b>%d</b>." % (e, num(v), n))

    sets = [("n. terimi bulma", [(kural, 20)]),
            ("İstenen terim", [(terim, 20)]),
            ("Tablodan ifade", [(tablo, 20)]),
            ("Şekil örüntüleri", [(sekil, 20)]),
            ("Kaçıncı terim?", [(kacinci, 20)])]
    return unit("oruntuler-ve-cebirsel-ifadeler", "C6", "MAT.6.2.2", 12, "Sayı ve Şekil Örüntülerini Cebirsel İfadeyle Gösterme", "Örüntüler ve Cebir",
                "Sayı ve şekil örüntülerindeki ilişkileri tablo, grafik ve sözel olarak ifade eder; örüntünün yapısını cebirsel ifadeyle gösterir.",
                "6. sınıf örüntüler ve cebirsel ifadeler çalışma kâğıdı: örüntünün n. terimini bulma, istenen terimi hesaplama, tablodan ve şekilden cebirsel ifade, kaçıncı terim. 100 soru ve cevap anahtarı.",
                "Artış miktarı n’nin katsayısıdır", "1. terimle kontrol edip sabit terimi bul.", sets,
                ["Her adımda aynı miktar artan bir örüntüde artış miktarı n’nin katsayısıdır: 3, 7, 11, 15 → 4n ile başlar.",
                 "Sabit terimi bulmak için 1. terime bakarız: 4 × 1 = 4, terim 3 → 4n − 1.",
                 "n yerine adım sayısını yazarak istediğimiz terimi buluruz."],
                [("5, 8, 11, 14", ["Artış 3: 3n", "3 × 1 = 3, 5 − 3 = 2"], "3n + 2"), ("n. terim 6n − 1 ise 20. terim", ["6 × 20 − 1"], "119")],
                [["3, 7, 11 için 3n yazmak (ilk terime bakmak)", "Katsayı artış miktarıdır: 4n − 1"], ["Sabit terimi kontrol etmemek", "n = 1, 2 için ifadeyi dene"],
                 ["20. terim için 20 × 3 yazıp sabit terimi unutmak", "3 × 20 + 2 = 62"]],
                [("Örüntüyü neden cebirle yazarız?", "Bütün terimleri yazmadan istediğimiz terimi tek işlemle bulmak için."),
                 ("Azalan örüntüler cebirle yazılır mı?", "Evet, ama 6. sınıfta artan örüntülerle çalışırız."),
                 ("Bir sayı örüntüde var mı nasıl anlarım?", "İfadeyi o sayıya eşitleyip n’yi buluruz; n doğal sayıysa sayı örüntüdedir.")])


# ============================================================ 13. algoritmalar ve cebirsel ifadeler
def code(lines):
    return "<div class='qfig'><span class='code'>%s</span></div>" % "<br>".join(lines)


def u13():
    def ifade():
        v = ch(VARS)
        a, b = ri(2, 9), ri(1, 20)
        k = ri(0, 1)
        if k == 0:
            lines = ["1. Bir %s sayısı al." % v, "2. Sayıyı %d ile çarp." % a, "3. Sonuca %d ekle." % b, "4. Sonucu yaz."]
            g = ex(a, v, b)
            w = ["%d(%s + %d)" % (a, v, b), ex(b, v, a), "%s + %d" % (v, a + b)]
        else:
            lines = ["1. Bir %s sayısı al." % v, "2. Sayıya %d ekle." % b, "3. Sonucu %d ile çarp." % a, "4. Sonucu yaz."]
            g = "%d(%s + %d)" % (a, v, b)
            w = [ex(a, v, b), "%s + %d" % (v, a * b) if a * b != b else ex(a, v, b + 1), ex(a, v, -b)]
        return mcq("Algoritmanın çıktısını gösteren cebirsel ifade hangisidir?" + code(lines), g, w, "Adımları sırayla yazarız: <b>%s</b>." % g)

    def hesap():
        v = ch(VARS)
        a, b, c = ri(2, 6), ri(1, 12), ri(2, 4)
        x = ri(2, 15)
        lines = ["1. %s = %d" % (v, x), "2. %s sayısını %d ile çarp." % (v, a), "3. Sonuca %d ekle." % b, "4. Sonucu %d ile çarp." % c, "5. Sonucu yaz."]
        g = (a * x + b) * c
        return mcq("Algoritmanın çıktısı kaçtır?" + code(lines), num(g), [num(a * x + b * c), num((a * x + b)), num(a * (x + b) * c)],
                   "(%d × %d + %d) × %d = <b>%s</b>." % (a, x, b, c, num(g)))

    def tablo():
        a, b = ri(2, 9), ri(1, 15)
        xs = sorted(sh(range(1, 13))[:4])
        rows = "".join("<tr><td style='text-align:center'>%d</td><td style='text-align:center'>%d</td></tr>" % (x, a * x + b) for x in xs)
        tab = "<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr><th>Girdi (x)</th><th>Çıktı</th></tr></thead><tbody>%s</tbody></table>" % rows
        g = ex(a, "x", b)
        return mcq("Bir algoritmanın girdi ve çıktıları tabloda verilmiştir. Çıktıyı veren ifade hangisidir?%s" % tab, g, [ex(a, "x", b + 1), ex(a + 1, "x", b - xs[0] if b - xs[0] else 1), "x + %d" % (a + b)],
                   "Girdi 1 artınca çıktı %d artıyor: %dx. Sabit terim %d → <b>%s</b>." % (a, a, b, g))

    def ters():
        a, b = ri(2, 9), ri(1, 25)
        x = ri(2, 30)
        out = a * x + b
        lines = ["1. Bir sayı al.", "2. Sayıyı %d ile çarp." % a, "3. Sonuca %d ekle." % b, "4. Sonucu yaz."]
        return mcq("Algoritmanın çıktısı %s ise alınan sayı kaçtır?%s" % (num(out), code(lines)), str(x), [str(out - b), str((out + b) // a), str(x + 1)],
                   "%dx + %d = %s → %dx = %s → x = <b>%d</b>." % (a, b, num(out), a, num(out - b), x))

    def fiyat():
        g = ch([200, 250, 400, 500])
        p = ri(5, 60) * (1000 // g) // (1000 // g) * 2
        lines = ["1. x gramlık ürünün fiyatı p TL olsun.", "2. 1.000 ÷ x işlemini yap.", "3. Sonucu p ile çarp.", "4. Sonucu yaz."]
        unit_p = p * 1000 // g if (p * 1000) % g == 0 else None
        if unit_p is None:
            return None
        return mcq("Algoritma bir ürünün 1 kg fiyatını hesaplıyor.%s%d g’lık ürünün fiyatı %d TL ise çıktı kaçtır?" % (code(lines), g, p), "%s TL" % num(unit_p),
                   ["%s TL" % num(x) for x in (p * g // 100, p + 1000 // g, unit_p // 10)], "1.000 ÷ %d = %s; %s × %d = <b>%s TL</b>." % (g, dec(1000.0 / g), dec(1000.0 / g), p, num(unit_p)))

    sets = [("Algoritmadan ifadeye", [(ifade, 20)]),
            ("Çıktıyı hesaplama", [(hesap, 20)]),
            ("Girdi-çıktı tabloları", [(tablo, 20)]),
            ("Girdiyi bulma", [(ters, 20)]),
            ("Günlük hayatta algoritma", [(fiyat, 10), (ifade, 10)])]
    return unit("algoritmalar-ve-cebirsel-ifadeler", "C6", "MAT.6.2.3", 13, "Cebirsel İfadelerle Algoritmalar", "Algoritmalar",
                "Cebirsel ifadeler içeren algoritmaları yorumlar; algoritmanın yapısını tablo veya cebirsel ifadeye dönüştürür ve matematiksel ilişkileri açıklar.",
                "6. sınıf algoritmalar çalışma kâğıdı: algoritmayı cebirsel ifadeye dönüştürme, çıktıyı hesaplama, girdi-çıktı tabloları, girdiyi bulma ve birim fiyat algoritması. 100 soru ve cevap anahtarı.",
                "Her adım ifadeye bir işlem ekler", "Çarp, ekle: 3x + 2. Ekle, çarp: 3(x + 2).", sets,
                ["Bir algoritmanın adımlarını sırayla yazarak cebirsel ifadeye dönüştürürüz: “x al, 3 ile çarp, 2 ekle” → 3x + 2.",
                 "Adımların sırası önemlidir: “2 ekle, sonra 3 ile çarp” → 3(x + 2).",
                 "Girdi-çıktı tablosunda girdi 1 artınca çıktının ne kadar arttığına bakarak katsayıyı buluruz."],
                [("x al, 4 ile çarp, 7 çıkar", ["4x", "4x − 7"], "4x − 7"), ("Çıktı 29, algoritma 3x + 5", ["3x = 24"], "x = 8")],
                [["“5 ekle, 2 ile çarp” → 2x + 5", "Önce ekleme yapıldığı için 2(x + 5)"], ["Tabloda yalnızca bir satıra bakmak", "Bütün satırlarla kontrol et"],
                 ["Girdiyi bulurken işlemleri aynı sırayla yapmak", "Tersine çalış: önce çıkar, sonra böl"]],
                [("Algoritma ile cebirsel ifade arasındaki ilişki nedir?", "Algoritmanın adımları bir cebirsel ifadeyle kısaca yazılabilir."),
                 ("Algoritmalar nerede kullanılır?", "Bilgisayar programlarında, tariflerde ve hesap makinesi işlemlerinde."),
                 ("Parantez neden gereklidir?", "Hangi işlemin önce yapılacağını gösterir; 3(x + 2) ile 3x + 2 farklıdır.")])


# ============================================================ 14. paralel doğrular ve kesen
VAL = lambda th: {1: th, 2: 180 - th, 3: th, 4: 180 - th, 5: th, 6: 180 - th, 7: th, 8: 180 - th}
CIFT = [("yöndeş", (1, 5)), ("yöndeş", (2, 6)), ("yöndeş", (3, 7)), ("yöndeş", (4, 8)), ("iç ters", (3, 5)), ("iç ters", (4, 6)),
        ("dış ters", (1, 7)), ("dış ters", (2, 8)), ("karşı durumlu iç", (4, 5)), ("karşı durumlu iç", (3, 6)), ("karşı durumlu dış", (1, 8)), ("karşı durumlu dış", (2, 7))]


def u14():
    def bul():
        th = ri(35, 145)
        if th == 90:
            return None
        ad, (i, j) = ch(CIFT)
        if ri(0, 1):
            i, j = j, i
        v = VAL(th)
        pic = G.parallel_fig(th, {i: "%d°" % v[i], j: "x"})
        g = v[j]
        e = ("%s açılar eşittir" % ad) if "karşı" not in ad else ("%s açıların toplamı 180°’dir" % ad)
        return mcq("d<sub>1</sub> // d<sub>2</sub> ise x kaç derecedir?" + pic, "%d°" % g, ["%d°" % x for x in (180 - g, 90, g + 10, abs(90 - g) + 90)],
                   "x ile %d° %s açılardır; %s: <b>x = %d°</b>." % (v[i], ad, e, g))

    def ad():
        th = ri(40, 140)
        if th == 90:
            return None
        nm, (i, j) = ch(CIFT)
        pic = G.parallel_fig(th, {i: "a", j: "b"})
        return mcq("d<sub>1</sub> // d<sub>2</sub>. a ve b açıları hangi açı çiftidir?" + pic, cap(nm) + " açılar",
                   [cap(x) + " açılar" for x in ["yöndeş", "iç ters", "dış ters", "karşı durumlu iç", "karşı durumlu dış"] if x != nm], "<b>%s açılar</b>." % cap(nm))

    def esit_mi():
        nm, _ = ch(CIFT)
        g = "Bütünlerdir (toplamları 180°)" if "karşı" in nm else "Eşittir"
        return mcq("Paralel iki doğru bir kesenle kesildiğinde %s açılar için hangisi doğrudur?" % nm, g, ["Eşittir", "Bütünlerdir (toplamları 180°)", "Tümlerdir (toplamları 90°)", "Hiçbir ilişki yoktur"],
                   "Yöndeş, iç ters ve dış ters açılar eşittir; karşı durumlu açılar bütünlerdir: <b>%s</b>." % low(g))

    def iki_bilinmeyen():
        th = ri(35, 145)
        if th == 90:
            return None
        v = VAL(th)
        i = ch([1, 2, 3, 4])
        j, k = sh([x for x in range(5, 9)])[:2]
        pic = G.parallel_fig(th, {i: "%d°" % v[i], j: "x", k: "y"})
        g = v[j] + v[k]
        return mcq("d<sub>1</sub> // d<sub>2</sub> ise x + y kaç derecedir?" + pic, "%d°" % g, ["%d°" % x for x in (g + 10, 360 - g if 360 - g != g else g + 20, 2 * v[i] if 2 * v[i] != g else 180)],
                   "x = %d°, y = %d°. x + y = <b>%d°</b>." % (v[j], v[k], g))

    sets = [("Açıyı bulma", [(bul, 20)]),
            ("Açı çiftlerinin adları", [(ad, 20)]),
            ("Açı çiftlerinin özellikleri", [(esit_mi, 5), (bul, 15)]),
            ("İki bilinmeyen", [(iki_bilinmeyen, 20)]),
            ("Karışık sorular", [(bul, 10), (ad, 10)])]
    return unit("paralel-dogrular-ve-kesen", "GS", "MAT.6.3.1", 14, "Paralel İki Doğrunun Bir Kesenle Oluşturduğu Açılar", "Paralel Doğrular ve Kesen",
                "İki paralel doğrunun bir kesenle oluşturduğu açıları belirler, ayırt eder, sınıflandırır ve adlandırır.",
                "6. sınıf paralel doğrular ve kesen çalışma kâğıdı: yöndeş, iç ters, dış ters, karşı durumlu iç ve dış açılar, açı ölçülerini bulma. 100 soru ve cevap anahtarı.",
                "Yöndeş, iç ters, dış ters açılar eşit", "Karşı durumlu açıların toplamı 180°.", sets,
                ["Paralel iki doğruyu bir kesen kestiğinde 8 açı oluşur. Bunların yalnızca iki farklı ölçüsü vardır ve bu iki ölçü bütünlerdir.",
                 "Yöndeş açılar (aynı konumdaki), iç ters açılar (paraleller arasında, kesenin farklı tarafında) ve dış ters açılar eşittir.",
                 "Karşı durumlu açılar kesenin aynı tarafındadır; toplamları 180°’dir."],
                [("Bir açı 65°, yöndeşi", ["Yöndeş açılar eşit"], "65°"), ("Bir açı 65°, karşı durumlu iç açısı", ["180 − 65"], "115°")],
                [["Karşı durumlu açıları eşit sanmak", "Karşı durumlu açılar bütünlerdir"], ["Paralel olmayan doğrularda bu kuralları kullanmak", "Kurallar yalnızca paralel doğrularda geçerlidir"],
                 ["İç ters ile dış ters açıları karıştırmak", "İç açılar paralellerin arasında, dış açılar dışındadır"]],
                [("Paralel doğrular nasıl gösterilir?", "d<sub>1</sub> // d<sub>2</sub> biçiminde."),
                 ("Kesen dik ise açılar nasıl olur?", "Bütün açılar 90° olur."),
                 ("Bu açılar günlük hayatta nerede görülür?", "Tren rayları ve onları kesen yollar, merdiven korkulukları ve çizgili defterlerde.")])


# ============================================================ 15. dörtgenler
DORTGEN = {
    "kare": dict(paralel="2 çift", kenar="dört kenarı eşit", aci="dört açısı 90°", kosegen="eşit, birbirini dik ortalar"),
    "dikdörtgen": dict(paralel="2 çift", kenar="karşılıklı kenarları eşit", aci="dört açısı 90°", kosegen="eşit, birbirini ortalar"),
    "eşkenar dörtgen": dict(paralel="2 çift", kenar="dört kenarı eşit", aci="karşılıklı açıları eşit", kosegen="birbirini dik ortalar"),
    "paralelkenar": dict(paralel="2 çift", kenar="karşılıklı kenarları eşit", aci="karşılıklı açıları eşit", kosegen="birbirini ortalar"),
    "yamuk": dict(paralel="1 çift", kenar="en az bir çift karşılıklı kenarı paralel", aci="paralel kenarlar arasındaki açılar bütünler", kosegen="genellikle birbirini ortalamaz"),
}


def dortgen_pts(kind):
    if kind == "kare":
        return [(0, 0), (110, 0), (110, -110), (0, -110)], (0, 1, 2, 3)
    if kind == "dikdörtgen":
        return [(0, 0), (170, 0), (170, -90), (0, -90)], (0, 1, 2, 3)
    if kind == "eşkenar dörtgen":
        return [(0, 0), (100, 0), (160, -80), (60, -80)], ()
    if kind == "paralelkenar":
        return [(0, 0), (150, 0), (200, -85), (50, -85)], ()
    return [(0, 0), (190, 0), (140, -85), (40, -85)], ()


def u15():
    def ad():
        kind = ch(list(DORTGEN))
        pts, r = dortgen_pts(kind)
        sx, sy = G.R.uniform(0.75, 1.15), G.R.uniform(0.8, 1.2)
        if kind in ("kare", "eşkenar dörtgen"):
            sy = sx
        t = math.radians(ri(-25, 25))
        pts = [(x * sx * math.cos(t) - y * sy * math.sin(t), x * sx * math.sin(t) + y * sy * math.cos(t)) for x, y in pts]
        ticks = {"kare": [(i, 1) for i in range(4)], "eşkenar dörtgen": [(i, 1) for i in range(4)], "dikdörtgen": [(0, 1), (2, 1), (1, 2), (3, 2)],
                 "paralelkenar": [(0, 1), (2, 1), (1, 2), (3, 2)], "yamuk": []}[kind]
        pic = poly(pts, label="dörtgen", rights=r, ticks=ticks)
        return mcq("Şekildeki dörtgen hangisidir? (Aynı işaretli kenarlar eşittir.)" + pic, cap(kind), [cap(x) for x in DORTGEN if x != kind],
                   "%s: %s, %s. <b>%s</b>." % (cap(kind), DORTGEN[kind]["kenar"], DORTGEN[kind]["aci"], cap(kind)))

    def ozellik():
        kind = ch(list(DORTGEN))
        p = ch(["kenar", "aci", "kosegen"])
        g = DORTGEN[kind][p]
        w = [DORTGEN[x][p] for x in DORTGEN if DORTGEN[x][p] != g] + {"kenar": ["hiçbir kenarı paralel değil", "yalnızca iki kenarı var"],
                                                                     "aci": ["dört açısı 60°", "açıları toplamı 180°"],
                                                                     "kosegen": ["köşegeni yoktur", "köşegenleri her zaman kenarlarına eşittir"]}[p]
        what = {"kenar": "kenarları", "aci": "açıları", "kosegen": "köşegenleri"}[p]
        return mcq("%s için %s hakkında hangisi doğrudur?" % (cap(kind), what), cap(g), sh([cap(x) for x in sorted(set(w))]), "%s: <b>%s</b>." % (cap(kind), g))

    def dogru_mu():
        S = [("Her kare bir eşkenar dörtgendir.", "Doğru"), ("Her eşkenar dörtgen bir karedir.", "Yanlış"), ("Her dikdörtgen bir paralelkenardır.", "Doğru"),
             ("Her paralelkenar bir dikdörtgendir.", "Yanlış"), ("Her kare bir paralelkenardır.", "Doğru"), ("Her yamuk bir paralelkenardır.", "Yanlış"),
             ("Paralelkenarın köşegenleri birbirini ortalar.", "Doğru"), ("Dikdörtgenin köşegenleri her zaman birbirine diktir.", "Yanlış"),
             ("Eşkenar dörtgenin köşegenleri birbirine diktir.", "Doğru"), ("Bir dörtgenin iç açıları toplamı 360°’dir.", "Doğru"),
             ("Yamuğun iki çift karşılıklı kenarı paraleldir.", "Yanlış"), ("Karenin köşegenleri eşit uzunluktadır.", "Doğru")]
        st, g = ch(S)
        return mcq("“%s” ifadesi doğru mu, yanlış mı?" % st, g, ["Yanlış" if g == "Doğru" else "Doğru", "Bazen doğru", "Bilinemez"],
                   "<b>%s</b>. Kare hem dikdörtgen hem eşkenar dörtgendir; dikdörtgen ve eşkenar dörtgen birer paralelkenardır." % g)

    def aci():
        k = ri(0, 2)
        if k == 0:
            a, b, c = ri(60, 120), ri(60, 120), ri(60, 120)
            d = 360 - a - b - c
            if not 30 < d < 160:
                return None
            pts = [(0, 0)]
            return mcq("Bir dörtgenin üç iç açısı %d°, %d° ve %d° ise dördüncü açısı kaç derecedir?" % (a, b, c), "%d°" % d, ["%d°" % x for x in (180 - d if 180 - d > 0 else d + 20, d + 10, 360 - d)],
                       "Dörtgenin iç açıları toplamı 360°: 360 − %d − %d − %d = <b>%d°</b>." % (a, b, c, d))
        if k == 1:
            a = ri(40, 140)
            if a == 90:
                return None
            return mcq("Bir paralelkenarın bir açısı %d° ise ona komşu açı kaç derecedir?" % a, "%d°" % (180 - a), ["%d°" % x for x in (a, 360 - a, 90 - a if a < 90 else a - 90)],
                       "Paralelkenarda komşu açılar bütünlerdir: 180 − %d = <b>%d°</b>." % (a, 180 - a))
        a = ri(40, 140)
        if a == 90:
            return None
        return mcq("Bir eşkenar dörtgenin bir açısı %d° ise karşısındaki açı kaç derecedir?" % a, "%d°" % a, ["%d°" % x for x in (180 - a, 360 - a, a + 10)],
                   "Karşılıklı açılar eşittir: <b>%d°</b>." % a)

    def kosegen():
        k = ri(0, 1)
        n = ri(3, 15)
        if k == 0:
            return mcq("Bir dikdörtgenin bir köşegeni %d cm ise diğer köşegeni kaç santimetredir?" % (2 * n), "%d cm" % (2 * n), ["%d cm" % x for x in (n, 4 * n, 2 * n + 2)],
                       "Dikdörtgenin köşegenleri eşittir: <b>%d cm</b>." % (2 * n))
        return mcq("Bir paralelkenarın köşegenleri O noktasında kesişiyor. Bir köşegenin uzunluğu %d cm ise O noktası bu köşegeni hangi uzunlukta iki parçaya ayırır?" % (2 * n), "%d cm ve %d cm" % (n, n),
                   ["%d cm ve %d cm" % (n - 1, n + 1), "%d cm ve %d cm" % (2 * n, 2 * n), "%d cm ve %d cm" % (n // 2 or 1, 2 * n - (n // 2 or 1))], "Paralelkenarın köşegenleri birbirini ortalar: <b>%d cm ve %d cm</b>." % (n, n))

    sets = [("Dörtgenleri tanıma", [(ad, 20)]),
            ("Özellikler", [(ozellik, 15), (aci, 5)]),
            ("Doğru mu, yanlış mı?", [(dogru_mu, 12), (kosegen, 8)]),
            ("Dörtgende açılar", [(aci, 20)]),
            ("Karışık sorular", [(ad, 8), (aci, 6), (kosegen, 6)])]
    return unit("dortgenler", "GS", "MAT.6.3.2, MAT.6.3.3", 15, "Yamuk, Paralelkenar, Eşkenar Dörtgen, Dikdörtgen ve Kare", "Dörtgenler",
                "İki paralel doğru ve iki kesenle oluşan şekillerin özelliklerine ilişkin akıl yürütür; köşegenleri birbirini ortalayan dörtgenleri oluşturur ve köşegen özelliklerini açıklar.",
                "6. sınıf dörtgenler çalışma kâğıdı: yamuk, paralelkenar, eşkenar dörtgen, dikdörtgen ve kare, kenar, açı ve köşegen özellikleri, dörtgenin iç açıları toplamı. 100 soru ve cevap anahtarı.",
                "Dörtgenin iç açıları toplamı 360°", "Paralelkenarın köşegenleri birbirini ortalar.", sets,
                ["Yamukta en az bir çift karşılıklı kenar paraleldir. Paralelkenarda iki çift karşılıklı kenar paraleldir; karşılıklı kenarlar ve açılar eşittir.",
                 "Dikdörtgen açıları 90° olan paralelkenardır; eşkenar dörtgen kenarları eşit olan paralelkenardır; kare hem dikdörtgen hem eşkenar dörtgendir.",
                 "Paralelkenarın köşegenleri birbirini ortalar. Dikdörtgende köşegenler eşittir, eşkenar dörtgende birbirine diktir. Bir dörtgenin iç açıları toplamı 360°’dir."],
                [("Açıları 80°, 95°, 110° olan dörtgenin dördüncü açısı", ["360 − 80 − 95 − 110"], "75°"), ("Paralelkenarın bir açısı 70°", ["Komşusu 110°, karşısı 70°"], "70°, 110°, 70°, 110°")],
                [["Her eşkenar dörtgeni kare sanmak", "Açıları 90° değilse kare değildir"], ["Dörtgenin açılarını 180°’ye tamamlamak", "Dörtgenin iç açıları toplamı 360°"],
                 ["Dikdörtgenin köşegenlerini dik sanmak", "Köşegenler yalnızca karede ve eşkenar dörtgende diktir"]],
                [("Kare neden bir dikdörtgendir?", "Dört açısı 90° ve karşılıklı kenarları eşit olduğu için dikdörtgenin bütün özelliklerini taşır."),
                 ("Dörtgenin iç açıları neden 360°’dir?", "Bir köşegen dörtgeni iki üçgene ayırır; 2 × 180° = 360°."),
                 ("Köşegenleri birbirini ortalayan dörtgenler hangileridir?", "Paralelkenar, dikdörtgen, eşkenar dörtgen ve kare.")])


# ============================================================ 16. üçgen ve dörtgende açı problemleri
def u16():
    def ucgen():
        a, b = ri(25, 100), ri(25, 100)
        c = 180 - a - b
        if c < 15 or 90 in (a, b, c):
            return None
        pts = AU.tri_pts(a, b, 160)
        pic = fig(AU.shape_svg(pts, {0: "%d°" % a, 1: "%d°" % b, 2: "x"}, "üçgen"), "üçgen")
        return mcq("Üçgende x kaç derecedir?" + pic, "%d°" % c, ["%d°" % x for x in (180 - a, 180 - b, 360 - a - b, c + 10)],
                   "180 − %d − %d = <b>%d°</b>." % (a, b, c))

    def dis():
        a, b = ri(25, 90), ri(25, 90)
        if a + b >= 170 or 90 in (a, b):
            return None
        return mcq("Bir üçgenin iç açılarından ikisi %d° ve %d° ölçülüdür. Üçüncü köşedeki dış açı kaç derecedir?" % (a, b), "%d°" % (a + b),
                   ["%d°" % x for x in (180 - a - b, 360 - a - b, 180 - a)], "Dış açı, kendisine komşu olmayan iki iç açının toplamıdır: %d + %d = <b>%d°</b>." % (a, b, a + b))

    def dis_toplam():
        k = ri(0, 1)
        if k == 0:
            a, b = ri(100, 150), ri(100, 150)
            c = 360 - a - b
            if not 60 < c < 175:
                return None
            return mcq("Bir üçgenin iki dış açısı %d° ve %d° ise üçüncü dış açısı kaç derecedir?" % (a, b), "%d°" % c, ["%d°" % x for x in (180 - c, 540 - a - b - 180 if 0 < 540 - a - b - 180 != c else c + 20, c + 10)],
                       "Üçgenin dış açıları toplamı 360°: 360 − %d − %d = <b>%d°</b>." % (a, b, c))
        a = ri(30, 80)
        return mcq("Bir ikizkenar üçgenin taban açılarından biri %d° ise tepe açısı kaç derecedir?" % a, "%d°" % (180 - 2 * a), ["%d°" % x for x in (180 - a, 2 * a, 90 - a if a < 90 else a)],
                   "180 − %d − %d = <b>%d°</b>." % (a, a, 180 - 2 * a))

    def dortgen():
        k = ri(0, 1)
        if k == 0:
            a, b, c = ri(60, 130), ri(60, 130), ri(60, 130)
            d = 360 - a - b - c
            if not 40 < d < 170:
                return None
            return mcq("Bir dörtgenin açıları %d°, %d°, %d° ve x ise x kaç derecedir?" % (a, b, c), "%d°" % d, ["%d°" % x for x in (180 - a - b if 180 - a - b > 0 else d + 20, d + 10, 360 - d)],
                       "360 − %d − %d − %d = <b>%d°</b>." % (a, b, c, d))
        a = ri(50, 130)
        if a == 90:
            return None
        return mcq("Bir paralelkenarda bir açı %d° ise diğer üç açı hangileridir?" % a, "%d°, %d°, %d°" % (180 - a, a, 180 - a),
                   ["%d°, %d°, %d°" % (a, a, a), "%d°, %d°, %d°" % (90, 90, 360 - a - 180), "%d°, %d°, %d°" % (180 - a, 180 - a, a)],
                   "Komşu açılar bütünler, karşılıklı açılar eşit: <b>%d°, %d°, %d°</b>." % (180 - a, a, 180 - a))

    def oranli():
        k = ri(2, 4)
        a = ri(15, 40)
        b = a * k
        c = 180 - a - b
        if c <= 10 or c >= 150:
            return None
        return mcq("Bir üçgenin bir açısı %d°, ikinci açısı birincinin %d katıdır. Üçüncü açı kaç derecedir?" % (a, k), "%d°" % c, ["%d°" % x for x in (180 - a, c + a, b, 180 - b)],
                   "İkinci açı %d × %d = %d°. 180 − %d − %d = <b>%d°</b>." % (a, k, b, a, b, c))

    sets = [("Üçgenin iç açıları", [(ucgen, 20)]),
            ("Üçgenin dış açısı", [(dis, 20)]),
            ("Dış açılar ve ikizkenar üçgen", [(dis_toplam, 20)]),
            ("Dörtgende açılar", [(dortgen, 20)]),
            ("Problemler", [(oranli, 20)])]
    return unit("ucgen-ve-dortgende-acilar", "GS", "MAT.6.3.4", 16, "Üçgen ve Dörtgenlerde Açı Problemleri", "Üçgen ve Dörtgende Açılar",
                "Üçgen ve dörtgenlerin açılarıyla ilgili problemleri çözer.",
                "6. sınıf üçgen ve dörtgende açılar çalışma kâğıdı: üçgenin iç açıları toplamı, dış açı, dış açılar toplamı, ikizkenar üçgen, dörtgen ve paralelkenarda açılar. 100 soru ve cevap anahtarı.",
                "Üçgen iç açıları 180°, dörtgen 360°", "Dış açı = komşu olmayan iki iç açının toplamı.", sets,
                ["Üçgenin iç açıları toplamı 180°, dörtgenin iç açıları toplamı 360°’dir.",
                 "Üçgenin bir dış açısı, kendisine komşu olmayan iki iç açının toplamına eşittir. Üçgenin dış açıları toplamı 360°’dir.",
                 "İkizkenar üçgende taban açıları eşittir; paralelkenarda karşılıklı açılar eşit, komşu açılar bütünlerdir."],
                [("İç açıları 50° ve 60° olan üçgende üçüncü köşedeki dış açı", ["50 + 60"], "110°"), ("Taban açısı 70° olan ikizkenar üçgenin tepe açısı", ["180 − 70 − 70"], "40°")],
                [["Dış açıyı 180 − (a + b) bulmak", "Dış açı = a + b"], ["Dörtgende 180°’ye tamamlamak", "Dörtgenin iç açıları 360°"],
                 ["İkizkenar üçgende tepe açısını taban açısına eşit sanmak", "Eşit olanlar taban açılarıdır"]],
                [("Dış açı neden iki iç açının toplamıdır?", "Dış açı ve komşu iç açı 180° eder; üçgenin üç iç açısı da 180° eder; bu yüzden dış açı diğer iki iç açıya eşittir."),
                 ("Bir üçgenin dış açıları toplamı neden 360°?", "Her köşede iç + dış = 180°; üç köşede 540°; bundan iç açılar toplamı 180° çıkınca 360° kalır."),
                 ("Açı problemlerini çözerken ilk adım nedir?", "Şekli dikkatle incele ve bilinen kuralları (180°, 360°, eşit açılar) yaz.")])


# ============================================================ 17. alan ölçü birimleri
ALAN = [("km²", 10 ** 6), ("hm²", 10 ** 4), ("dam²", 100), ("m²", 1), ("dm²", F(1, 100)), ("cm²", F(1, 10 ** 4)), ("mm²", F(1, 10 ** 6))]


def u17():
    def cevir():
        i, j = sh(range(7))[:2]
        if abs(i - j) > 2:
            return None
        a, va = ALAN[i]
        b, vb = ALAN[j]
        n = ri(2, 95)
        g = F(n) * F(va) / F(vb)
        gs = num(g) if g.denominator == 1 else G.dz(float(g))
        if g.denominator != 1 and len(gs) > 8:
            return None
        alts = [g * 10, g / 10, g * 100 if g * 100 != g else g * 1000, g / 100]
        return mcq("%d %s kaç %s eder?" % (n, a, b), "%s %s" % (gs, b), ["%s %s" % (num(x) if F(x).denominator == 1 else G.dz(float(x)), b) for x in alts if F(x) != g and (F(x).denominator == 1 or len(G.dz(float(x))) < 10)],
                   "Alan birimleri 100’er 100’er büyür. %s ile %s arasında %d basamak: <b>%s %s</b>." % (a, b, abs(i - j), gs, b))

    def hektar():
        k = ri(0, 2)
        n = ri(2, 40)
        if k == 0:
            return mcq("%d hektar kaç metrekaredir?" % n, "%s m²" % num(n * 10000), ["%s m²" % num(x) for x in (n * 1000, n * 100, n * 100000)], "1 ha = 1 hm² = 10.000 m². %d × 10.000 = <b>%s m²</b>." % (n, num(n * 10000)))
        if k == 1:
            return mcq("%s m² kaç hektardır?" % num(n * 10000), "%d ha" % n, ["%d ha" % x for x in (n * 10, n * 100)] + ["%s ha" % dec(n / 10.0)], "%s ÷ 10.000 = <b>%d ha</b>." % (num(n * 10000), n))
        return mcq("%d km² kaç hektardır?" % n, "%s ha" % num(n * 100), ["%s ha" % num(x) for x in (n * 10, n * 1000, n * 10000)], "1 km² = 100 ha. %d × 100 = <b>%s ha</b>." % (n, num(n * 100)))

    def uzunluk_iliski():
        a = ri(2, 9)
        k = ri(0, 1)
        if k == 0:
            return mcq("Bir kenarı %d m olan kare kaç santimetrekaredir?" % a, "%s cm²" % num(a * a * 10000), ["%s cm²" % num(x) for x in (a * a * 100, a * 100 * 4, a * a * 1000)],
                       "%d m = %d cm. %d × %d = <b>%s cm²</b>." % (a, a * 100, a * 100, a * 100, num(a * a * 10000)))
        return mcq("1 m = 10 dm olduğuna göre 1 m² kaç dm²’dir?", "100 dm²", ["10 dm²", "1.000 dm²", "20 dm²"], "Kenarı 1 m = 10 dm olan karenin alanı 10 × 10 = <b>100 dm²</b>.") if a < 4 else \
            mcq("1 cm = 10 mm olduğuna göre %d cm² kaç mm²’dir?" % a, "%d mm²" % (a * 100), ["%d mm²" % x for x in (a * 10, a * 1000, a * 20)], "1 cm² = 10 × 10 = 100 mm². %d × 100 = <b>%d mm²</b>." % (a, a * 100))

    def karsilastir():
        vals = [(ri(1, 9), "m²"), (ri(10, 990), "dm²"), (ri(1000, 99000), "cm²")]
        cm = {"m²": 10000, "dm²": 100, "cm²": 1}
        cs = [v * cm[u] for v, u in vals]
        if len(set(cs)) < 3:
            return None
        k = ri(0, 1)
        i = cs.index(max(cs)) if k == 0 else cs.index(min(cs))
        opts = ["%s %s" % (num(v), u) for v, u in vals]
        return mcq("%s alanlarından en %s hangisidir?" % (", ".join(opts), "büyüğü" if k == 0 else "küçüğü"), opts[i], [o for j, o in enumerate(opts) if j != i] + ["Hepsi eşit"],
                   "Hepsini cm²’ye çeviririz: %s. <b>%s</b>." % (", ".join("%s cm²" % num(x) for x in cs), opts[i]))

    def problem():
        a, b = ri(20, 400), ri(20, 300)
        p = ri(5, 40) * 100
        k = ri(0, 1)
        if k == 0:
            g = a * b
            return mcq("Kenarları %s m ve %s m olan dikdörtgen bir tarlanın alanı kaç hektardır?" % (num(a * 10), num(b * 10)), "%s ha" % G.dz(a * b / 100.0),
                       ["%s ha" % G.dz(x) for x in (a * b / 10.0, a * b / 1000.0, a * b * 1.0)], "Alan %s m². %s ÷ 10.000 = <b>%s ha</b>." % (num(a * b * 100), num(a * b * 100), G.dz(a * b / 100.0)))
        n = ri(2, 9)
        return mcq("Bir kenarı 50 cm olan kare fayanslarla %d m² alan kaplanacak. Kaç fayans gerekir?" % n, str(n * 4), [str(n * 2), str(n * 50), str(n * 25)],
                   "Bir fayans 50 × 50 = 2.500 cm² = 0,25 m². %d ÷ 0,25 = <b>%d</b>." % (n, n * 4))

    sets = [("Alan birimlerini dönüştürme", [(cevir, 20)]),
            ("Hektar ve dekar", [(hektar, 20)]),
            ("Uzunluk ve alan birimleri ilişkisi", [(uzunluk_iliski, 12), (cevir, 8)]),
            ("Karşılaştırma", [(karsilastir, 20)]),
            ("Problemler", [(problem, 20)])]
    return unit("alan-olcu-birimleri", "GN", "MAT.6.4.1", 17, "Alan Ölçü Birimleri: km², m², dm², cm², mm² ve Hektar", "Alan Ölçü Birimleri",
                "Uzunluk ve alan ölçme birimleri arasındaki ilişkiye yönelik analojik akıl yürütür; alan ölçme birimleri arasındaki ilişkiyi çıkarır.",
                "6. sınıf alan ölçü birimleri çalışma kâğıdı: km², hm², dam², m², dm², cm², mm² arasında dönüştürme, hektar, uzunluk ve alan birimleri ilişkisi, karşılaştırma ve problemler. 100 soru ve cevap anahtarı.",
                "Alan birimleri 100’er 100’er değişir", "1 m² = 100 dm² = 10.000 cm²", sets,
                ["Uzunluk birimleri 10’ar 10’ar, alan birimleri 100’er 100’er değişir: 1 m = 10 dm, 1 m² = 10 dm × 10 dm = 100 dm².",
                 "Büyük alan biriminden küçüğe çevirirken 100, 10.000 ile çarparız; küçükten büyüğe çevirirken böleriz.",
                 "1 hektar (ha) = 1 hm² = 10.000 m². Tarla ve orman alanları hektarla ölçülür."],
                [("3 m² kaç cm²?", ["1 m² = 10.000 cm²", "3 × 10.000"], "30.000 cm²"), ("50.000 m² kaç ha?", ["50.000 ÷ 10.000"], "5 ha")],
                [["1 m² = 100 cm²", "1 m² = 100 cm × 100 cm = 10.000 cm²"], ["Alan birimlerinde 10 ile çarpmak", "Her basamakta 100 kat değişir"],
                 ["Hektarı 1.000 m² sanmak", "1 ha = 10.000 m²"]],
                [("Alan birimleri neden 100 kat değişir?", "Bir alan iki uzunluğun çarpımıdır; uzunluk 10 kat değişince alan 10 × 10 = 100 kat değişir."),
                 ("Hektar nerede kullanılır?", "Tarla, orman, park gibi geniş alanları ölçerken."),
                 ("mm² nerede kullanılır?", "Çok küçük yüzeylerde: bir düğmenin ya da bir mikroçipin yüzeyi gibi.")])


# ============================================================ 18. paralelkenar ve üçgenin alanı
def u18():
    def paralelkenar():
        a, h = ri(4, 16), ri(3, 10)
        sh_ = ri(2, 5)
        pts = [(0, 0), (a * 14, 0), (a * 14 + sh_ * 14, -h * 14), (sh_ * 14, -h * 14)]
        pic = poly(pts + [], [str(a), None, None, None], label="paralelkenar")
        hh = "<div class='qfig'>Taban %d cm, yükseklik %d cm</div>" % (a, h)
        return mcq("Tabanı %d cm, bu tabana ait yüksekliği %d cm olan paralelkenarın alanı kaç santimetrekaredir?" % (a, h) + pic, "%d cm²" % (a * h),
                   ["%d cm²" % x for x in (a * h // 2 if a * h % 2 == 0 else a * h + 1, 2 * (a + h), a + h)], "Paralelkenarın alanı = taban × yükseklik = %d × %d = <b>%d cm²</b>." % (a, h, a * h))

    def ucgen():
        a, h = ri(4, 20), ri(3, 14)
        if (a * h) % 2:
            return None
        g = a * h // 2
        return mcq("Tabanı %d cm, bu tabana ait yüksekliği %d cm olan üçgenin alanı kaç santimetrekaredir?" % (a, h), "%d cm²" % g, ["%d cm²" % x for x in (a * h, a + h, 2 * g + a)],
                   "Üçgenin alanı = taban × yükseklik ÷ 2 = %d × %d ÷ 2 = <b>%d cm²</b>." % (a, h, g))

    def ucgen_fig():
        a, h = ri(4, 14), ri(3, 10)
        if (a * h) % 2:
            return None
        s = 14
        top = ri(0, a) * s
        pts = [(0, 0), (a * s, 0), (top, -h * s)]
        P = poly(pts, [str(a), None, None], label="üçgen", dashed=[])
        hline = "<div class='qfig'>Yükseklik: %d cm</div>" % h
        g = a * h // 2
        return mcq("Şekildeki üçgenin tabanı %d cm, yüksekliği %d cm’dir. Üçgenin alanı kaç santimetrekaredir?%s" % (a, h, P), "%d cm²" % g, ["%d cm²" % x for x in (a * h, a + h, g + a)],
                   "%d × %d ÷ 2 = <b>%d cm²</b>." % (a, h, g))

    def eksik():
        k = ri(0, 1)
        a, h = ri(4, 16), ri(3, 12)
        if k == 0:
            return mcq("Alanı %d cm² olan paralelkenarın tabanı %d cm ise yüksekliği kaç santimetredir?" % (a * h, a), "%d cm" % h, ["%d cm" % x for x in (a * h - a, 2 * h, h + 1)],
                       "%d ÷ %d = <b>%d cm</b>." % (a * h, a, h))
        if (a * h) % 2:
            return None
        return mcq("Alanı %d cm² olan üçgenin tabanı %d cm ise yüksekliği kaç santimetredir?" % (a * h // 2, a), "%d cm" % h, ["%d cm" % x for x in (h // 2 or 1, a * h // 2 - a, h + 2)],
                   "Alan × 2 ÷ taban: %d × 2 ÷ %d = <b>%d cm</b>." % (a * h // 2, a, h))

    def problem():
        k = ri(0, 1)
        if k == 0:
            a, h = ri(10, 40), ri(5, 30)
            p = ri(2, 9) * 10
            return mcq("Tabanı %d m, yüksekliği %d m olan paralelkenar şeklindeki bir bahçeye çim ekilecek. Metrekaresi %d TL ise toplam maliyet kaç TL olur?" % (a, h, p), "%s TL" % num(a * h * p),
                       ["%s TL" % num(x) for x in (a * h * p // 2, 2 * (a + h) * p, a * h)], "Alan %d × %d = %d m². %d × %d = <b>%s TL</b>." % (a, h, a * h, a * h, p, num(a * h * p)))
        a, h = ri(4, 20), ri(4, 20)
        if (a * h) % 2:
            return None
        return mcq("Bir yelken üçgen şeklindedir. Tabanı %d m, yüksekliği %d m ise yelkenin alanı kaç metrekaredir?" % (a, h), "%d m²" % (a * h // 2), ["%d m²" % x for x in (a * h, a + h, a * h // 4 or 1)],
                   "%d × %d ÷ 2 = <b>%d m²</b>." % (a, h, a * h // 2))

    sets = [("Paralelkenarın alanı", [(paralelkenar, 20)]),
            ("Üçgenin alanı", [(ucgen, 14), (ucgen_fig, 6)]),
            ("Eksik uzunluğu bulma", [(eksik, 20)]),
            ("Alan problemleri", [(problem, 20)]),
            ("Karışık sorular", [(paralelkenar, 7), (ucgen_fig, 7), (eksik, 6)])]
    return unit("paralelkenar-ve-ucgenin-alani", "GN", "MAT.6.4.2, MAT.6.4.3", 18, "Paralelkenarın ve Üçgenin Alanı", "Paralelkenar ve Üçgenin Alanı",
                "Dikdörtgenin alan bağıntısından paralelkenar ve üçgenin alan bağıntılarına ulaşır; alan ile ilgili gerçek yaşam problemlerini çözer.",
                "6. sınıf paralelkenar ve üçgenin alanı çalışma kâğıdı: paralelkenarın alanı (taban × yükseklik), üçgenin alanı (taban × yükseklik ÷ 2), eksik uzunluk ve alan problemleri. 100 soru ve cevap anahtarı.",
                "Üçgen = taban × yükseklik ÷ 2", "Paralelkenar = taban × yükseklik", sets,
                ["Bir paralelkenarın bir ucundan üçgen kesip öbür ucuna eklersek aynı taban ve yükseklikte bir dikdörtgen elde ederiz: alan = taban × yükseklik.",
                 "Bir paralelkenarı köşegeniyle iki eş üçgene ayırırız: üçgenin alanı = taban × yükseklik ÷ 2.",
                 "Yükseklik, tabana dik olan uzunluktur; eğik kenarın uzunluğu yükseklik değildir."],
                [("Taban 12 cm, yükseklik 5 cm olan paralelkenar", ["12 × 5"], "60 cm²"), ("Taban 10 cm, yükseklik 7 cm olan üçgen", ["10 × 7 ÷ 2"], "35 cm²")],
                [["Üçgende 2’ye bölmeyi unutmak", "Üçgen, paralelkenarın yarısıdır"], ["Eğik kenarı yükseklik sanmak", "Yükseklik tabana diktir"],
                 ["Alanı cm ile yazmak", "Alan birimi cm²’dir"]],
                [("Aynı taban ve yükseklikteki üçgen ile paralelkenarın alanları nasıl ilişkilidir?", "Üçgenin alanı paralelkenarın alanının yarısıdır."),
                 ("Yükseklik şeklin dışında olabilir mi?", "Evet, geniş açılı üçgenlerde yükseklik şeklin dışına düşebilir."),
                 ("Alan günlük hayatta nerede kullanılır?", "Bahçe, duvar, kumaş, arsa gibi yüzeylerin büyüklüğünü ve maliyetini hesaplarken.")])


# ============================================================ 19. çember uzunluğu
def u19():
    def cevre_r():
        r = ri(2, 20)
        pi_ = ch([3, 3.14])
        g = 2 * pi_ * r
        gs = dec(g) if isinstance(pi_, float) else num(int(g))
        return mcq("Yarıçapı %d cm olan çemberin uzunluğu kaç santimetredir? (π = %s)" % (r, dec(pi_) if isinstance(pi_, float) else "3"), "%s cm" % gs,
                   ["%s cm" % (dec(x) if isinstance(pi_, float) else num(int(x))) for x in (pi_ * r, pi_ * r * r, 2 * pi_ * r + 2 * r)],
                   "Çember uzunluğu = 2 × π × r = 2 × %s × %d = <b>%s cm</b>." % (dec(pi_) if isinstance(pi_, float) else "3", r, gs))

    def cevre_d():
        d = ri(4, 40)
        pi_ = 3
        g = pi_ * d
        pic = circle_fig("%d cm" % d, "d", label="çapı verilen çember")
        return mcq("Çapı %d cm olan çemberin uzunluğu kaç santimetredir? (π = 3)" % d + pic, "%d cm" % g, ["%d cm" % x for x in (2 * g, d + 3, g // 2 if g % 2 == 0 else g + 3)],
                   "Çember uzunluğu = π × çap = 3 × %d = <b>%d cm</b>." % (d, g))

    def ters():
        r = ri(2, 20)
        g = 6 * r
        return mcq("Uzunluğu %d cm olan çemberin yarıçapı kaç santimetredir? (π = 3)" % g, "%d cm" % r, ["%d cm" % x for x in (2 * r, g // 3, r + 3)],
                   "2 × 3 × r = %d → r = %d ÷ 6 = <b>%d cm</b>." % (g, g, r))

    def pi_ne():
        S = [("Bir çemberin uzunluğunun çapına oranı neye eşittir?", "π sayısına", ["2 sayısına", "Yarıçapa", "Alana"]),
             ("π sayısının yaklaşık değeri hangisidir?", "3,14", ["2,14", "4,13", "3,41"]),
             ("Çember uzunluğu çapın yaklaşık kaç katıdır?", "3 katı", ["2 katı", "4 katı", "Yarısı"]),
             ("Çapı iki katına çıkan bir çemberin uzunluğu nasıl değişir?", "İki katına çıkar", ["Dört katına çıkar", "Değişmez", "Yarıya iner"])]
        q, g, w = ch(S)
        return mcq(q, g, w, "Bir çemberin uzunluğu çapının yaklaşık 3,14 katıdır; bu oran π ile gösterilir: <b>%s</b>." % g)

    def problem():
        k = ri(0, 2)
        if k == 0:
            r = ri(20, 50)
            n = ri(2, 10)
            g = 2 * 3 * r * n
            return mcq("Yarıçapı %d cm olan bir bisiklet tekerleği %d tam tur dönüyor. Bisiklet kaç santimetre yol alır? (π = 3)" % (r, n), "%s cm" % num(g), ["%s cm" % num(x) for x in (3 * r * n, 2 * 3 * r, g * 2)],
                       "Bir tur 2 × 3 × %d = %d cm. %d × %d = <b>%s cm</b>." % (r, 6 * r, n, 6 * r, num(g)))
        if k == 1:
            r = ri(5, 30)
            return mcq("Yarıçapı %d m olan dairesel bir havuzun etrafına kaç metre çit gerekir? (π = 3)" % r, "%d m" % (6 * r), ["%s m" % num(x) for x in (3 * r, 3 * r * r, 12 * r)],
                       "2 × 3 × %d = <b>%d m</b>." % (r, 6 * r))
        d = ri(10, 60)
        L = 3 * d * ri(2, 8)
        return mcq("Çapı %d cm olan bir tekerlek %s cm yol alıyor. Tekerlek kaç tur dönmüştür? (π = 3)" % (d, num(L)), str(L // (3 * d)), [str(L // d), str(L // (6 * d) or 1), str(L // (3 * d) + 1)],
                   "Bir tur 3 × %d = %d cm. %s ÷ %d = <b>%d</b> tur." % (d, 3 * d, num(L), 3 * d, L // (3 * d)))

    sets = [("Yarıçapı verilen çember", [(cevre_r, 20)]),
            ("Çapı verilen çember", [(cevre_d, 20)]),
            ("Uzunluktan yarıçapa", [(ters, 16), (pi_ne, 4)]),
            ("Tekerlek ve havuz problemleri", [(problem, 20)]),
            ("Karışık sorular", [(cevre_r, 10), (cevre_d, 10)])]
    return unit("cember-uzunlugu-ve-pi", "GN", "MAT.6.4.4, MAT.6.4.5", 19, "Çember Uzunluğu ve π Sayısı", "Çember Uzunluğu",
                "Çemberin uzunluğu ile çapı arasındaki ilişkiye yönelik akıl yürütür; yarıçapı veya çapı verilen çemberin uzunluğunu hesaplamayı gerektiren problemleri çözer.",
                "6. sınıf çember uzunluğu çalışma kâğıdı: π sayısı, çember uzunluğu = 2πr = π × çap, uzunluktan yarıçapı bulma, tekerlek ve havuz problemleri. 100 soru ve cevap anahtarı.",
                "Çember uzunluğu = 2 × π × r", "π ≈ 3,14: uzunluk çapın yaklaşık 3 katı.", sets,
                ["Her çemberin uzunluğunun çapına oranı aynıdır. Bu sabit sayıya π (pi) denir; π ≈ 3,14.",
                 "Çember uzunluğu = π × çap = 2 × π × yarıçap.",
                 "Bir tekerlek bir tam tur döndüğünde çevresi kadar yol alır."],
                [("r = 5 cm, π = 3", ["2 × 3 × 5"], "30 cm"), ("Çevre 42 cm, π = 3", ["2 × 3 × r = 42", "r = 7"], "7 cm")],
                [["2 ile çarpmayı unutmak (π × r)", "Yarıçap verildiyse 2 × π × r"], ["Çap verildiğinde 2 ile çarpmak", "Çap verildiyse π × çap"],
                 ["Çember uzunluğunu alan sanmak", "Uzunluk cm ile, alan cm² ile ölçülür"]],
                [("π sayısı tam olarak kaçtır?", "π’nin ondalık basamakları sonsuza kadar sürer: 3,14159… Hesaplarda 3 ya da 3,14 kullanırız."),
                 ("Çember uzunluğunu nasıl ölçebilirim?", "Bir ipi çemberin etrafına sarıp düzleştirerek ve cetvelle ölçerek."),
                 ("Tekerlek problemlerinde neden çember uzunluğu kullanılır?", "Tekerlek bir turda kendi çevresi kadar ilerler.")])


# ============================================================ 20. merkez açı ve yay
def sector_fig(angle, r_lab=None):
    W = H = 200
    cx, cy, r = 100, 100, 80
    a0 = 0
    a1 = math.radians(angle)
    x1, y1 = cx + r, cy
    x2, y2 = cx + r * math.cos(a1), cy - r * math.sin(a1)
    big = 1 if angle > 180 else 0
    s = ["<circle cx='%d' cy='%d' r='%d' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (cx, cy, r, GREEN),
         "<path d='M%d %d L%.1f %.1f A%d %d 0 %d 0 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, x1, y1, r, r, big, x2, y2, FILL, GREEN),
         "<path d='M%.1f %.1f A%d %d 0 %d 0 %.1f %.1f' fill='none' stroke='%s' stroke-width='4'/>" % (x1, y1, r, r, big, x2, y2, RED),
         "<circle cx='%d' cy='%d' r='3.5' fill='%s'/>" % (cx, cy, INK)]
    m = math.radians(angle / 2.0)
    s.append(text(cx + 30 * math.cos(m), cy - 30 * math.sin(m) + 5, "%d°" % angle, 13))
    return G.wrap(W, H, "".join(s), "merkez açısı %d° olan yay" % angle)


def u20():
    def oran():
        a = ch([30, 45, 60, 90, 120, 180, 240, 270, 300])
        g = F(a, 360)
        return mcq("Merkez açısı %d° olan yay, çemberin ne kadarıdır?" % a + sector_fig(a), ff(g), [ff(F(a, 180)) if a < 180 else fr(1, 3), fr(a, 100), ff(1 - g)],
                   "%d ÷ 360 = <b>%s</b>." % (a, ff(g)))

    def yay():
        a = ch([30, 45, 60, 90, 120, 180, 240, 270])
        C = ch([36, 48, 72, 120, 144, 180, 240])
        if (C * a) % 360:
            return None
        g = C * a // 360
        return mcq("Uzunluğu %d cm olan bir çemberde merkez açısı %d° olan yayın uzunluğu kaç santimetredir?" % (C, a), "%d cm" % g, ["%d cm" % x for x in (C - g, C * a // 180 if (C * a) % 180 == 0 else g + 5, a, g + C // 12)],
                   "Yay, çemberin %s kadarıdır: %d × %s = <b>%d cm</b>." % (ff(F(a, 360)), C, ff(F(a, 360)), g))

    def yay_r():
        a = ch([60, 90, 120, 180])
        r = ri(2, 12)
        C = 6 * r
        if (C * a) % 360:
            return None
        g = C * a // 360
        return mcq("Yarıçapı %d cm olan çemberde merkez açısı %d° olan yayın uzunluğu kaç santimetredir? (π = 3)" % (r, a), "%d cm" % g, ["%d cm" % x for x in (C, C - g, 3 * r * a // 360 if (3 * r * a) % 360 == 0 else g + 1)],
                   "Çember uzunluğu 2 × 3 × %d = %d cm. %d × %s = <b>%d cm</b>." % (r, C, C, ff(F(a, 360)), g))

    def aci():
        C = ch([36, 60, 72, 90, 120, 180])
        a = ch([30, 45, 60, 90, 120, 150, 180, 240])
        if (C * a) % 360:
            return None
        L = C * a // 360
        return mcq("Uzunluğu %d cm olan bir çemberde %d cm’lik yayı gören merkez açısı kaç derecedir?" % (C, L), "%d°" % a, ["%d°" % x for x in (L, 360 - a, a // 2 if a % 2 == 0 else a + 30, 2 * a if 2 * a < 360 else a - 15)],
                   "%d ÷ %d = %s. 360 × %s = <b>%d°</b>." % (L, C, ff(F(L, C)), ff(F(L, C)), a))

    def iki_kat():
        a = ch([30, 40, 45, 60, 90])
        L = ri(2, 15)
        k = ch([2, 3])
        return mcq("Bir çemberde %d° merkez açılı yayın uzunluğu %d cm ise %d° merkez açılı yayın uzunluğu kaç santimetredir?" % (a, L, a * k), "%d cm" % (L * k), ["%d cm" % x for x in (L, L + k, L * k * 2)],
                   "Merkez açısı %d katına çıkınca yay da %d katına çıkar: <b>%d cm</b>." % (k, k, L * k))

    sets = [("Yay çemberin ne kadarı?", [(oran, 9), (iki_kat, 11)]),
            ("Yay uzunluğu", [(yay, 20)]),
            ("Yarıçapla yay uzunluğu", [(yay_r, 20)]),
            ("Merkez açıyı bulma", [(aci, 20)]),
            ("Merkez açı ve yay ilişkisi", [(iki_kat, 20)])]
    return unit("merkez-acisi-ve-yay", "GN", "MAT.6.4.6", 20, "Merkez Açı ve Yay Uzunluğu", "Merkez Açı ve Yay",
                "Bir çemberde merkez açının ölçüsü ile gördüğü yayın uzunluğu arasındaki ilişkiye yönelik tümevarımsal akıl yürütür.",
                "6. sınıf merkez açı ve yay çalışma kâğıdı: merkez açı ile yayın çemberdeki payı, yay uzunluğunu hesaplama, yarıçapla yay uzunluğu, merkez açıyı bulma. 100 soru ve cevap anahtarı.",
                "Yay = çember × merkez açı ÷ 360", "Merkez açı iki katına çıkarsa yay da iki katına çıkar.", sets,
                ["Bir çemberin tamamı 360°’lik merkez açıya karşılık gelir. 90°’lik merkez açı çemberin 1/4’ünü, 180° yarısını görür.",
                 "Yay uzunluğu = çember uzunluğu × merkez açı ÷ 360.",
                 "Merkez açı büyüdükçe yay da aynı oranda büyür."],
                [("Çember 72 cm, merkez açı 90°", ["90/360 = 1/4", "72 × 1/4"], "18 cm"), ("Çember 60 cm, yay 20 cm", ["20/60 = 1/3", "360 × 1/3"], "120°")],
                [["Merkez açıyı 180’e bölmek", "Tam çember 360°’dir"], ["Yay uzunluğunu derece ile yazmak", "Yay bir uzunluktur: cm, m"],
                 ["Yarıçap verildiğinde çember uzunluğunu bulmadan işlem yapmak", "Önce 2 × π × r ile çember uzunluğunu bul"]],
                [("Merkez açı nedir?", "Köşesi çemberin merkezinde, kolları yarıçap olan açıdır."),
                 ("Yay nedir?", "Çemberin iki noktası arasındaki parçasıdır."),
                 ("Saat kadranında merkez açılar kaç derecedir?", "12 eş parça olduğu için her saat aralığı 360 ÷ 12 = 30°’dir.")])


# ============================================================ 21. veri analizi
def u21():
    def ortalama():
        n = ri(4, 7)
        m = ri(5, 40)
        xs = [m + ri(-6, 6) for _ in range(n - 1)]
        last = m * n - sum(xs)
        if last <= 0:
            return None
        xs.append(last)
        xs = sh(xs)
        return mcq("%s verilerinin aritmetik ortalaması kaçtır?" % ", ".join(map(str, xs)), str(m), [str(m + 1), str(sum(xs)), str(sorted(xs)[n // 2])] if sorted(xs)[n // 2] != m else [str(m + 1), str(sum(xs)), str(m - 2)],
                   "Toplam %d, veri sayısı %d: %d ÷ %d = <b>%d</b>." % (sum(xs), n, sum(xs), n, m))

    def medyan():
        n = ch([5, 7, 9, 6, 8])
        xs = [ri(1, 50) for _ in range(n)]
        s = sorted(xs)
        if n % 2:
            g = s[n // 2]
            gs = str(g)
        else:
            v = F(s[n // 2 - 1] + s[n // 2], 2)
            gs = num(v) if v.denominator == 1 else dec(float(v))
        return mcq("%s verilerinin medyanı (ortanca değeri) kaçtır?" % ", ".join(map(str, xs)), gs, [str(xs[n // 2]), str(round(sum(xs) / float(n))), str(s[n // 2 + 1] if n // 2 + 1 < n else s[0])],
                   "Sıralarız: %s. Ortadaki %s: <b>%s</b>." % (", ".join(map(str, s)), "değer" if n % 2 else "iki değerin ortalaması", gs))

    def mod():
        base = [ri(1, 20) for _ in range(ri(5, 8))]
        m = ch(base)
        xs = sh(base + [m, m])
        c = {x: xs.count(x) for x in xs}
        top = max(c.values())
        if list(c.values()).count(top) > 1:
            return None
        return mcq("%s verilerinin tepe değeri (modu) kaçtır?" % ", ".join(map(str, xs)), str(m), [str(x) for x in sh(set(xs) - {m})[:3]] + [str(max(xs))],
                   "En çok tekrar eden değer %d (%d kez): <b>%d</b>." % (m, c[m], m))

    def dal():
        xs = [ri(10, 59) for _ in range(ri(8, 12))]
        tab = stem_leaf(xs)
        k = ri(0, 2)
        s = sorted(xs)
        if k == 0:
            return mcq("Dal-yaprak gösteriminde verilen verilerin en büyüğü ile en küçüğü arasındaki fark kaçtır?" + tab, str(s[-1] - s[0]), [str(s[-1]), str(s[-1] + s[0]), str(s[-1] - s[0] + 10)],
                       "En büyük %d, en küçük %d: <b>%d</b>." % (s[-1], s[0], s[-1] - s[0]))
        if k == 1:
            return mcq("Dal-yaprak gösteriminde kaç veri vardır?" + tab, str(len(xs)), [str(len(xs) + 1), str(len(set(x // 10 for x in xs))), str(len(xs) - 1)],
                       "Her yaprak bir veridir: <b>%d</b>." % len(xs))
        n = len(s)
        if n % 2 == 0:
            v = F(s[n // 2 - 1] + s[n // 2], 2)
        else:
            v = F(s[n // 2])
        gs = num(v) if v.denominator == 1 else dec(float(v))
        return mcq("Dal-yaprak gösteriminde verilen verilerin medyanı kaçtır?" + tab, gs, [str(s[0]), str(s[-1]), str(s[n // 2 - 2])], "Veriler sıralı; ortadaki değer: <b>%s</b>." % gs)

    def problem():
        nm = G.K.next()
        n = ri(3, 5)
        m = ri(60, 90)
        xs = [m + ri(-12, 12) for _ in range(n)]
        target = m + ri(1, 5)
        need = target * (n + 1) - sum(xs)
        if not 0 < need <= 100:
            return None
        return mcq("%s ilk %d sınavından %s puan aldı. Ortalamasının %d olması için bir sonraki sınavdan kaç puan almalıdır?" % (nm, n, ", ".join(map(str, xs)), target), str(need),
                   [str(target), str(need + n), str(target * n - sum(xs)) if target * n - sum(xs) > 0 else str(need - 5)], "%d sınavın toplamı %d × %d = %d olmalı. %d − %d = <b>%d</b>." % (n + 1, target, n + 1, target * (n + 1), target * (n + 1), sum(xs), need))

    sets = [("Aritmetik ortalama", [(ortalama, 20)]),
            ("Medyan", [(medyan, 20)]),
            ("Tepe değer (mod)", [(mod, 20)]),
            ("Dal-yaprak gösterimi", [(dal, 20)]),
            ("Ortalama problemleri", [(problem, 20)])]
    return unit("veri-analizi", "IA", "MAT.6.5.1, MAT.6.5.2", 21, "Veri Analizi: Aritmetik Ortalama, Medyan, Tepe Değer ve Dal-Yaprak", "Veri Analizi",
                "Kategorik veya nicel kesikli veriyle çalışır ve veriye dayalı karar verir; başkaları tarafından oluşturulan istatistiksel sonuçları tartışır.",
                "6. sınıf veri analizi çalışma kâğıdı: aritmetik ortalama, medyan (ortanca), tepe değer (mod), dal-yaprak gösterimi ve ortalama problemleri. 100 soru ve cevap anahtarı.",
                "Ortalama = toplam ÷ veri sayısı", "Medyan sıralı verinin ortasındaki değerdir.", sets,
                ["Aritmetik ortalama, veriler toplamının veri sayısına bölümüdür.",
                 "Medyan (ortanca), veriler küçükten büyüğe sıralandığında ortadaki değerdir; veri sayısı çiftse ortadaki iki değerin ortalamasıdır.",
                 "Tepe değer (mod), en çok tekrar eden değerdir. Dal-yaprak gösteriminde onlar basamağı dal, birler basamağı yapraktır."],
                [("4, 7, 9, 12 ortalaması", ["4 + 7 + 9 + 12 = 32", "32 ÷ 4"], "8"), ("3, 9, 5, 7, 2 medyanı", ["2, 3, 5, 7, 9"], "5")],
                [["Medyanı sıralamadan bulmak", "Önce küçükten büyüğe sırala"], ["Ortalamayı bulurken yanlış sayıya bölmek", "Toplam, veri sayısına bölünür"],
                 ["Dal-yaprakta dalı veri saymak", "Her yaprak bir veridir"]],
                [("Ortalama ile medyan farklı olabilir mi?", "Evet. Çok büyük ya da çok küçük bir değer ortalamayı etkiler ama medyanı az etkiler."),
                 ("Mod birden fazla olabilir mi?", "Evet, en çok tekrar eden birden fazla değer varsa hepsi moddur."),
                 ("Dal-yaprak gösterimi ne işe yarar?", "Verileri sıralı ve bütün değerleri görünür biçimde gösterir.")])


# ============================================================ 22. deneysel olasılık
def u22():
    def hesap():
        n = ch([20, 25, 40, 50, 100])
        k = ri(1, n - 1)
        ev, it = ch([("zar atıldığında 6 gelme", "atış"), ("yazı tura atıldığında yazı gelme", "atış"), ("çark çevrildiğinde kırmızı gelme", "çevirme"), ("torbadan mavi top çekme", "çekiliş")])
        g = F(k, n)
        return mcq("Bir deneyde %d %s yapılıyor ve %s olayı %d kez gerçekleşiyor. Bu olayın deneysel olasılığı kaçtır?" % (n, it, ev, k), ff(g),
                   [fr(n - k, n), fr(k, n - k) if n - k != k else fr(1, 3), ff(F(k, 100)) if n != 100 else fr(k, 10) if k < 10 else fr(1, k)], "Olayın gerçekleşme sayısı ÷ deneme sayısı = %s." % (("%s = <b>%s</b>" % (fr(k, n), ff(g))) if g.denominator != n else "<b>%s</b>" % ff(g)))

    def tablo():
        cats = sh(["Kırmızı", "Mavi", "Yeşil", "Sarı"])[:3]
        vals = [ri(3, 25) for _ in cats]
        n = sum(vals)
        i = ri(0, 2)
        tab = freq_table("Renk", cats, vals)
        g = F(vals[i], n)
        return mcq("Bir çark %d kez çevrildi. Sonuçlar tabloda verilmiştir.%s%s gelme olayının deneysel olasılığı kaçtır?" % (n, tab, cats[i]), ff(g),
                   [fr(vals[i], n - vals[i]), fr(1, 3), ff(F(vals[(i + 1) % 3], n))], "%d ÷ %d = %s." % (vals[i], n, ("%s = <b>%s</b>" % (fr(vals[i], n), ff(g))) if g.denominator != n else "<b>%s</b>" % ff(g)))

    def tahmin():
        n = ch([50, 100, 200])
        k = ri(5, n // 2)
        N = ch([500, 1000, 2000])
        g = k * N // n if (k * N) % n == 0 else None
        if g is None:
            return None
        return mcq("Bir fabrikada %d ürünün %d tanesinin kusurlu olduğu görüldü. Aynı olasılıkla %s ürünün yaklaşık kaç tanesi kusurlu olur?" % (n, k, num(N)), num(g), [num(k), num(g * 2), num(N - g)],
                   "Deneysel olasılık %s. %s × %s = <b>%s</b>." % (fr(k, n), num(N), fr(k, n), num(g)))

    def cok_deneme():
        S = [("Deneme sayısı arttıkça deneysel olasılık nasıl değişir?", "Teorik olasılığa yaklaşır", ["Hep 1 olur", "Hep 0 olur", "Değişmez"]),
             ("Bir zar 10 kez atıldığında hiç 6 gelmedi. 6 gelme olasılığı 0 mıdır?", "Hayır, deneme sayısı az; olasılık 0 değildir", ["Evet, 6 hiç gelmez", "Evet, zar bozuktur", "Bilinemez"]),
             ("Deneysel olasılık neye dayanır?", "Deneyde elde edilen verilere", ["Tahmine", "Yalnızca hesaplamaya", "Şansa"]),
             ("Yazı tura 1.000 kez atılırsa yazı gelme sayısı yaklaşık kaç olur?", "500", ["1.000", "100", "250"])]
        q, g, w = ch(S)
        return mcq(q, g, w, "Deneme sayısı arttıkça göreli sıklık teorik olasılığa yaklaşır: <b>%s</b>." % g)

    def karsilastir():
        n1, n2 = G.K.two()
        a, b = ch([20, 40, 50]), ch([20, 40, 50])
        x, y = ri(2, a - 2), ri(2, b - 2)
        if F(x, a) == F(y, b):
            return None
        g = n1 if F(x, a) > F(y, b) else n2
        return mcq("%s %d atışta %d kez, %s %d atışta %d kez basket attı. Deneysel olasılığa göre kimin basket atma olasılığı daha yüksektir?" % (n1, a, x, n2, b, y), g,
                   [n2 if g == n1 else n1, "Eşit", "Bilinemez"], "%s ve %s: <b>%s</b>." % (ff(F(x, a)), ff(F(y, b)), g))

    sets = [("Deneysel olasılık", [(hesap, 20)]),
            ("Tablodan olasılık", [(tablo, 20)]),
            ("Tahmin", [(tahmin, 20)]),
            ("Karşılaştırma", [(karsilastir, 20)]),
            ("Deneme sayısı", [(cok_deneme, 4), (hesap, 8), (tablo, 8)])]
    return unit("deneysel-olasilik", "VO", "MAT.6.6.1", 22, "Deneysel Olasılık ve Göreli Sıklık", "Deneysel Olasılık",
                "Bir olayın olasılığını gözleme dayalı tahmin eder; deneme sayısı ile göreli sıklık arasındaki ilişki üzerine çıkarım yapar.",
                "6. sınıf deneysel olasılık çalışma kâğıdı: deneysel olasılığı hesaplama, tablodan olasılık, olasılıkla tahmin, karşılaştırma ve deneme sayısının etkisi. 100 soru ve cevap anahtarı.",
                "Olay sayısı ÷ deneme sayısı", "Deneme arttıkça sonuç teorik olasılığa yaklaşır.", sets,
                ["Deneysel olasılık bir deneyin sonuçlarına dayanır: olayın gerçekleşme sayısı ÷ toplam deneme sayısı.",
                 "Bu orana göreli sıklık da denir. Deneme sayısı arttıkça göreli sıklık teorik olasılığa yaklaşır.",
                 "Deneysel olasılığı kullanarak büyük gruplar için tahmin yapabiliriz."],
                [("50 atışta 12 kez 6", ["12 ÷ 50"], "12/50 = 6/25"), ("100 üründe 4 kusurlu, 1.000 ürün", ["1.000 × 4/100"], "yaklaşık 40")],
                [["Deneme sayısını olay sayısına bölmek", "Olay sayısı ÷ deneme sayısı"], ["Az denemeyle kesin sonuç çıkarmak", "Deneme sayısı arttıkça sonuç güvenilir olur"],
                 ["Deneysel ve teorik olasılığı her zaman eşit sanmak", "Az denemede farklı olabilir"]],
                [("Teorik olasılık ile deneysel olasılık farkı nedir?", "Teorik olasılık hesaplamayla, deneysel olasılık deney sonuçlarıyla bulunur."),
                 ("Deneysel olasılık 0 çıkarsa olay imkânsız mıdır?", "Hayır, yalnızca o deneyde gerçekleşmemiştir."),
                 ("Deneysel olasılık nerede kullanılır?", "Hava tahminlerinde, sporda, üretimde kusur oranı hesaplarken.")])


UNITS = [u11, u12, u13, u14, u15, u16, u17, u18, u19, u20, u21, u22]
