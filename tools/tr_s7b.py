# -*- coding: utf-8 -*-
"""Türkiye 7. sınıf: İşlemlerle Cebirsel Düşünme ve Değişimler (10〜15)、Dönüşüm (16〜17)、Geometrik Şekiller (18)。"""
import math
from fractions import Fraction as F
import tr_g as G
from tr_g import unit, num, fr, M, NB, line, text, INK, GREEN, RED, BLUE, FILL
from tr_g7 import sn, par, dq, lin, terms, MINUS, gen


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


V = ["x", "a", "y", "n", "m", "k"]


def code(lines):
    return "<div class='qfig'><span class='code'>%s</span></div>" % "<br>".join(lines)


# ============================================================ 10. cebirsel ifadeler
def u10():
    def topla():
        v = ch(V)
        a, b, c, d = nz(-9, 9), nz(-12, 12), nz(-9, 9), nz(-12, 12)
        op = ch(["+", MINUS])
        e1, e2 = lin(a, v, b), lin(c, v, d)
        A, B = (a + c, b + d) if op == "+" else (a - c, b - d)
        if A == 0:
            return None
        g = lin(A, v, B)
        w = [lin(a + c, v, b - d) if op != "+" else lin(a - c, v, b + d), lin(A, v, -B) if B else lin(A + 1, v, 1), lin(-A, v, B), lin(A, v, B + 1)]
        return M("(%s) %s (%s) işleminin sonucu hangisidir?" % (e1, op, e2), g, w,
                 "%sBenzer terimleri toplarız: <b>%s</b>." % ("Parantezin önündeki eksi, içindeki her terimin işaretini değiştirir. " if op != "+" else "", g))

    def carp():
        v = ch(V)
        k = rq_or_int()
        a, b = nz(-9, 9), nz(-9, 9)
        if (k * a).denominator != 1 or (k * b).denominator != 1:
            return None
        g = lin(int(k * a), v, int(k * b))
        w = [lin(int(k * a), v, b), lin(a, v, int(k * b)), lin(int(-k * a), v, int(k * b)), lin(int(k * a), v, int(-k * b))]
        return M("%s · (%s) ifadesinin eşiti hangisidir?" % (par(k), lin(a, v, b)), g, w,
                 "Dağılma özelliği: parantezin önündeki sayı içindeki her terimle çarpılır: <b>%s</b>." % g)

    def deger():
        v = ch(V)
        a, b = nz(-9, 9), nz(-15, 15)
        x = nz(-6, 6)
        val = a * x + b
        return M("%s = %s için %s ifadesinin değeri kaçtır?" % (v, sn(x), lin(a, v, b)), sn(val), [sn(a * -x + b), sn(a + x + b), sn(val + a)],
                 "%s yerine %s yazarız: %s · %s %s %s = <b>%s</b>." % (v, sn(x), sn(a), par(x), "+" if b > 0 else MINUS, num(abs(b)), sn(val)))

    def benzer():
        v, u = sh(V)[:2]
        cs = [(nz(-7, 7), v), (nz(-7, 7), u), (nz(-7, 7), v), (nz(-9, 9), "")]
        A = cs[0][0] + cs[2][0]
        if A == 0:
            return None
        g = terms([(A, v), (cs[1][0], u), (cs[3][0], "")])
        w = [terms([(A + cs[1][0], v), (cs[3][0], "")]), terms([(cs[0][0] - cs[2][0], v), (cs[1][0], u), (cs[3][0], "")]), terms([(A, v), (cs[1][0] + cs[3][0], u)]),
             terms([(A, v), (-cs[1][0], u), (cs[3][0], "")])]
        return M("%s ifadesinin en sade biçimi hangisidir?" % terms(cs), g, w, "Yalnızca aynı harfli (benzer) terimler toplanır: <b>%s</b>." % g)

    def cevre():
        v = ch(["x", "a", "n"])
        a, b = ri(1, 5), ri(1, 9)
        c, d = ri(1, 4), ri(0, 6)
        g = lin(2 * (a + c), v, 2 * (b + d))
        w = [lin(a + c, v, b + d), lin(2 * a + c, v, 2 * b + d), lin(4 * (a + c), v, 4 * (b + d)) if a + c < 4 else lin(2 * (a + c) + 1, v, 2 * (b + d))]
        return M("Kenar uzunlukları (%s) cm ve (%s) cm olan dikdörtgenin çevre uzunluğunu gösteren ifade hangisidir?" % (lin(a, v, b), lin(c, v, d) if d else lin(c, v)), g, w,
                 "Çevre = 2 · (kısa kenar + uzun kenar) = 2 · (%s) = <b>%s</b>." % (lin(a + c, v, b + d), g))

    sets = [("Toplama ve çıkarma", [(topla, 20)]),
            ("Benzer terimler", [(benzer, 20)]),
            ("Sayıyla çarpma (dağılma)", [(carp, 20)]),
            ("İfadenin değeri", [(deger, 20)]),
            ("Çevre ve karışık", [(cevre, 8), (topla, 6), (carp, 6)])]
    return unit("cebirsel-ifadelerle-islemler", "C6", "MAT.7.2.1", 10, "Cebirsel İfadelerle Toplama, Çıkarma ve Rasyonel Sayıyla Çarpma", "Cebirsel İfadeler",
                "Cebirsel ifadelerle toplama, çıkarma ve bir rasyonel sayı ile çarpma işlemlerini yorumlar; toplama ve çarpmanın özelliklerini kullanır, işlemlerin denkliğini açıklar.",
                "7. sınıf cebirsel ifadeler çalışma kâğıdı: benzer terimler, cebirsel ifadelerle toplama ve çıkarma, dağılma özelliği ile çarpma, ifadenin değerini bulma, çevre ifadesi. 100 soru ve cevap anahtarı.",
                "Yalnızca benzer terimler toplanır", "3x + 2x = 5x, ama 3x + 2 sadeleşmez.", sets,
                ["Harfleri ve üsleri aynı olan terimlere benzer terim denir. Benzer terimlerin katsayıları toplanır: 4a − 7a = −3a.",
                 "Parantezin önünde eksi varsa parantez kaldırılırken içteki her terimin işareti değişir: −(2x − 5) = −2x + 5.",
                 "Bir sayıyla çarparken dağılma özelliğini kullanırız: −3(2x + 4) = −6x − 12."],
                [("(3x − 4) − (5x + 2)", ["3x − 4 − 5x − 2"], "−2x − 6"), ("x = −2 için 4x + 9", ["4 · (−2) + 9"], "1")],
                [["−(5x + 2) yaparken yalnızca ilk terimin işaretini değiştirmek", "−5x − 2 olmalı"],
                 ["3x + 4’ü 7x yapmak", "Sabit terim ile harfli terim toplanmaz"],
                 ["Dağılmada ikinci terimi çarpmayı unutmak", "−3(2x + 4) = −6x − 12"]],
                [("Katsayı nedir?", "Harfin önündeki sayıdır. −5y teriminde katsayı −5’tir."),
                 ("x ile 1x aynı mı?", "Evet. Katsayı 1 olduğunda yazılmaz."),
                 ("Cebirsel ifadeler nerede kullanılır?", "Bilinmeyen ya da değişen nicelikleri genel olarak göstermek için: çevre, fiyat, örüntüler.")])


def rq_or_int():
    if ri(0, 2):
        return F(nz(-6, 6))
    return F(ch([1, -1, 1, 3, -3]), ch([2, 3]))


# ============================================================ 11. denklemler
def u11():
    def iki_adim():
        v = ch(V)
        x = nz(-12, 12)
        a, b = nz(-9, 9), nz(-20, 20)
        if abs(a) == 1:
            return None
        c = a * x + b
        return M("%s = %s denkleminin çözümü hangisidir?" % (lin(a, v, b), sn(c)), "%s = %s" % (v, sn(x)),
                 ["%s = %s" % (v, sn(-x)), "%s = %s" % (v, sn(x + 1)), "%s = %s" % (v, sn(c - b))],
                 "Önce %s ile, sonra katsayıyla işlem: %s = %s → %s = %s → <b>%s = %s</b>." % (sn(b), lin(a, v), sn(c - b), v, sn(F(c - b, a)), v, sn(x)))

    def parantez():
        v = ch(V)
        x = nz(-9, 9)
        a, b = nz(-6, 6), nz(-9, 9)
        if abs(a) == 1:
            return None
        c = a * (x + b)
        return M("%s(%s) = %s denkleminde %s kaçtır?" % (sn(a), lin(1, v, b), sn(c), v), sn(x), [sn(-x), sn(F(c, a) + b), sn(c - b)],
                 "İki taraf %s ile bölünür: %s = %s, buradan %s = <b>%s</b>." % (sn(a), lin(1, v, b), sn(F(c, a)), v, sn(x)))

    def iki_taraf():
        v = ch(V)
        x = nz(-9, 9)
        a, c = nz(-8, 8), nz(-8, 8)
        if a == c:
            return None
        b = nz(-15, 15)
        d = a * x + b - c * x
        return M("%s = %s denkleminin çözüm kümesindeki %s değeri kaçtır?" % (lin(a, v, b), lin(c, v, d), v), sn(x), [sn(-x), sn(x + 1), sn(F(d - b, a + c)) if a + c else sn(x + 2)],
                 "Harfli terimleri bir tarafa, sayıları diğer tarafa toplarız: %s = %s, %s = <b>%s</b>." % (lin(a - c, v), sn(d - b), v, sn(x)))

    def kesirli():
        v = ch(V)
        k = ch([2, 3, 4, 5])
        x = k * nz(-6, 6)
        b = nz(-9, 9)
        c = x // k + b
        return M("%s/%d %s %d = %s denkleminde %s kaçtır?" % (v, k, "+" if b > 0 else MINUS, abs(b), sn(c), v), sn(x), [sn(x // k), sn(c * k), sn(-x), sn(x + k)],
                 "%s/%d = %s %s %s = %s, %s = %d · %s = <b>%s</b>." % (v, k, sn(c), MINUS if b > 0 else "+", num(abs(b)), sn(c - b), v, k, par(c - b), sn(x)))

    def kok_mu():
        v = ch(V)
        x = nz(-8, 8)
        a, b = nz(-6, 6), nz(-12, 12)
        c = a * x + b
        cands = [x, -x, x + 1, x - 2]
        if len(set(cands)) < 4:
            return None
        return G.withopts(M("Hangisi %s = %s denklemini sağlar?" % (lin(a, v, b), sn(c)), sn(x), [sn(y) for y in cands[1:]],
                            "%s = %s yazınca %s · %s %s %d = %s olur: <b>%s</b>." % (v, sn(x), sn(a), par(x), "+" if b > 0 else MINUS, abs(b), sn(c), sn(x))), "%s sayıları veriliyor.")

    sets = [("İki adımlı denklemler", [(iki_adim, 20)]),
            ("Parantezli denklemler", [(parantez, 20)]),
            ("Bilinmeyen iki tarafta", [(iki_taraf, 20)]),
            ("Kesirli denklemler", [(kesirli, 20)]),
            ("Denklemi sağlayan sayı", [(kok_mu, 10), (iki_taraf, 5), (kesirli, 5)])]
    return unit("birinci-dereceden-bir-bilinmeyenli-denklemler", "C6", "MAT.7.2.2", 11, "Birinci Dereceden Bir Bilinmeyenli Denklemler", "Denklemler",
                "Birinci dereceden bir bilinmeyenli doğrusal denklemleri çözmek için strateji geliştirir ve uygular; çözümü örnekler ve temsillerle kontrol eder.",
                "7. sınıf birinci dereceden bir bilinmeyenli denklemler çalışma kâğıdı: iki adımlı denklemler, parantezli denklemler, bilinmeyenin iki tarafta olduğu denklemler, kesirli denklemler. 100 soru ve cevap anahtarı.",
                "Eşitliğin iki tarafına aynı işlem", "Terazi gibi: iki tarafa aynı işlem yapılır.", sets,
                ["Denklem, içinde bilinmeyen bulunan bir eşitliktir. Eşitliğin iki tarafına aynı işlem yapılırsa eşitlik bozulmaz (terazi gibi).",
                 "Önce sabit terimden kurtuluruz (ekleme ya da çıkarma), sonra katsayıya böleriz.",
                 "Bilinmeyen iki taraftaysa harfli terimleri bir tarafa, sayıları diğer tarafa toplarız. Bulduğumuz değeri denklemde yerine yazıp kontrol ederiz."],
                [("3x − 7 = 11", ["3x = 18"], "x = 6"), ("5a + 4 = 2a − 8", ["5a − 2a = −8 − 4", "3a = −12"], "a = −4")],
                [["Terimi karşıya geçirirken işaretini değiştirmemek", "3x − 7 = 11 → 3x = 11 + 7"],
                 ["Katsayıya bölmeyi unutmak", "3x = 18 ise x = 6, x = 18 değil"],
                 ["Negatif katsayıya bölerken işareti karıştırmak", "−4x = 12 → x = −3"]],
                [("Denklemin kaç çözümü olur?", "Birinci dereceden bir bilinmeyenli denklemin (katsayı 0 değilse) tek çözümü vardır."),
                 ("Çözümü nasıl kontrol ederim?", "Bulduğun sayıyı denklemde yerine yaz; iki taraf eşit çıkmalı."),
                 ("Kesirli denklemde ne yapmalı?", "Paydadan kurtulmak için iki tarafı paydayla çarp.")])


# ============================================================ 12. eşitsizlikler
def ineq_line(k, op):
    W, H = 420, 64
    s = "<svg viewBox='0 0 %d %d' role='img' aria-label='sayı doğrusunda eşitsizlik'>" % (W, H)
    s += "<line x1='14' y1='30' x2='406' y2='30' stroke='#333' stroke-width='2'/>"
    for i in range(-5, 6):
        x = 210 + i * 36
        s += "<line x1='%d' y1='24' x2='%d' y2='36' stroke='#333'/><text x='%d' y='56' font-size='13' text-anchor='middle'>%s</text>" % (x, x, x, (MINUS if k + i < 0 else "") + str(abs(k + i)))
    right = op in (">", "≥")
    s += "<line x1='210' y1='30' x2='%d' y2='30' stroke='#c0392b' stroke-width='5'/>" % (400 if right else 20)
    s += "<circle cx='210' cy='30' r='7' fill='%s' stroke='#c0392b' stroke-width='3'/>" % ("#c0392b" if op in ("≥", "≤") else "#fff")
    return "<div class='qfig'>" + G.lg(s + "</svg>") + "</div>"


def opq(o):
    return {"<": "&lt;", ">": "&gt;", "≤": "≤", "≥": "≥"}[o]


FLIP = {"<": ">", ">": "<", "≤": "≥", "≥": "≤"}


def u12():
    def coz():
        v = ch(["x", "a", "y"])
        x = nz(-8, 8)
        a, b = nz(-6, 6), nz(-12, 12)
        if abs(a) == 1 and ri(0, 1):
            return None
        o = ch(["<", ">", "≤", "≥"])
        c = a * x + b
        oo = FLIP[o] if a < 0 else o
        g = "%s %s %s" % (v, opq(oo), sn(x))
        w = ["%s %s %s" % (v, opq(FLIP[oo]), sn(x)), "%s %s %s" % (v, opq(oo), sn(-x)), "%s %s %s" % (v, opq(o if a < 0 else FLIP[o]), sn(-x))]
        return M("%s %s %s eşitsizliğinin çözümü hangisidir?" % (lin(a, v, b), opq(o), sn(c)), g, w,
                 "%s %s %s; iki taraf %s ile bölünür%s: <b>%s</b>." % (lin(a, v), opq(o), sn(c - b), sn(a), " (negatif sayıyla bölündüğü için yön değişir)" if a < 0 else "", g))

    def dogru():
        k = ri(-5, 5)
        o = ch(["<", ">", "≤", "≥"])
        v = "x"
        g = "%s %s %s" % (v, opq(o), sn(k))
        others = [x for x in ["<", ">", "≤", "≥"] if x != o]
        return M("Sayı doğrusunda gösterilen çözüm kümesi hangi eşitsizliğe aittir?" + ineq_line(k, o), g, ["%s %s %s" % (v, opq(x), sn(k)) for x in others],
                 "İçi dolu yuvarlak sayının dâhil olduğunu (≤, ≥), boş yuvarlak dâhil olmadığını (&lt;, &gt;) gösterir. Ok %s doğru: <b>%s</b>." % ("sağa" if o in (">", "≥") else "sola", g))

    def saglar():
        k = nz(-6, 6)
        o = ch(["<", ">", "≤", "≥"])
        def ok(y):
            return {"<": y < k, ">": y > k, "≤": y <= k, "≥": y >= k}[o]
        cs = [k - 2, k - 1, k, k + 1, k + 2, k + 3, k - 3]
        good = [y for y in cs if ok(y)]
        bad = [y for y in cs if not ok(y)]
        if len(bad) < 3 or not good:
            return None
        g = ch(good)
        return G.withopts(M("Hangisi x %s %s eşitsizliğini sağlar?" % (opq(o), sn(k)), sn(g), [sn(y) for y in sh(bad)],
                            "x %s %s: %s bu koşulu sağlar." % (opq(o), sn(k), sn(g))), "%s sayıları veriliyor.")

    def soz():
        S = [("Bir asansör en fazla %d kg taşıyabilir. Asansördeki yük (y) için hangisi doğrudur?", "y ≤ %d", ["y &lt; %d", "y ≥ %d", "y &gt; %d"]),
             ("Bir sınava girmek için en az %d yaşında olmak gerekir. Yaş (y) için hangisi doğrudur?", "y ≥ %d", ["y &gt; %d", "y ≤ %d", "y &lt; %d"]),
             ("Bir köprüden %d tondan ağır araçlar geçemez. Geçebilen aracın ağırlığı (a) için hangisi doğrudur?", "a ≤ %d", ["a &lt; %d", "a ≥ %d", "a &gt; %d"]),
             ("Hava sıcaklığı %d °C’nin altına düştü. Sıcaklık (s) için hangisi doğrudur?", "s &lt; %d", ["s ≤ %d", "s &gt; %d", "s ≥ %d"])]
        t, g, w = ch(S)
        n = {"asansör": ri(30, 100) * 10, "yaşında": ri(7, 18), "tondan": ri(3, 40)}.get(next((k for k in ("asansör", "yaşında", "tondan") if k in t), ""), None)
        if n is None:
            n = nz(-10, 10)
        return M(t % n, g % n, [x % n for x in w], "‘En fazla’ ≤, ‘en az’ ≥, ‘altına’ &lt;, ‘üstüne’ &gt; ile gösterilir: <b>%s</b>." % (g % n))

    sets = [("Eşitsizlik çözme", [(coz, 20)]),
            ("Sayı doğrusunda çözüm", [(dogru, 20)]),
            ("Eşitsizliği sağlayan sayı", [(saglar, 20)]),
            ("Sözel ifadeler", [(soz, 12), (dogru, 8)]),
            ("Karışık", [(coz, 10), (saglar, 5), (soz, 5)])]
    return unit("birinci-dereceden-bir-bilinmeyenli-esitsizlikler", "C6", "MAT.7.2.2", 12, "Birinci Dereceden Bir Bilinmeyenli Eşitsizlikler", "Eşitsizlikler",
                "Birinci dereceden bir bilinmeyenli doğrusal eşitsizlikleri içeren gerçek yaşam problemlerini çözer; çözüm kümesini sayı doğrusunda gösterir.",
                "7. sınıf eşitsizlikler çalışma kâğıdı: birinci dereceden eşitsizlikleri çözme, negatif sayıyla bölünce yön değiştirme, çözüm kümesini sayı doğrusunda gösterme, ‘en az’ ve ‘en fazla’ ifadeleri. 100 soru ve cevap anahtarı.",
                "Negatifle çarp ya da böl: yön değişir", "−2x &lt; 6 ise x &gt; −3.", sets,
                ["Eşitsizlik, iki ifadenin &lt;, &gt;, ≤, ≥ sembolleriyle karşılaştırılmasıdır. Çözümü denklem gibi yaparız.",
                 "Eşitsizliğin iki tarafı negatif bir sayıyla çarpılır ya da bölünürse eşitsizliğin yönü değişir.",
                 "Sayı doğrusunda ≤ ve ≥ için içi dolu, &lt; ve &gt; için içi boş yuvarlak kullanılır."],
                [("2x − 5 &lt; 7", ["2x &lt; 12"], "x &lt; 6"), ("−3a + 1 ≥ 10", ["−3a ≥ 9", "−3’e bölünce yön değişir"], "a ≤ −3")],
                [["Negatif sayıya bölünce yönü değiştirmemek", "−2x &lt; 6 → x &gt; −3"],
                 ["Dolu ve boş yuvarlağı karıştırmak", "x ≥ 2: 2 dâhil, dolu yuvarlak"],
                 ["‘En az’ ifadesini &lt; ile yazmak", "En az 18: y ≥ 18"]],
                [("Eşitsizliğin kaç çözümü vardır?", "Genellikle sonsuz çözümü vardır; bu yüzden çözüm kümesi sayı doğrusunda bir ışınla gösterilir."),
                 ("Pozitif sayıyla çarpınca yön değişir mi?", "Hayır. Yalnızca negatif sayıyla çarpma ya da bölmede değişir."),
                 ("Çözümü nasıl kontrol ederim?", "Çözüm kümesinden bir sayı seçip eşitsizlikte yerine yaz; doğru çıkmalı.")])


# ============================================================ 13. problemler
def u13():
    def yas():
        n1, n2 = G.K.two()
        x = ri(6, 14)
        k = ri(2, 4)
        d = ri(1, 8)
        tot = x + k * x + d
        return M("%s yaşının %d katının %d fazlası %s yaşına eşittir. İkisinin yaşları toplamı %d ise %s kaç yaşındadır?" % (gen(n1), k, d, gen(n2), tot, n1), num(x),
                 [num(k * x + d), num(tot // 2), num(x + 1)], "%s x olsun: x + %dx + %d = %d → %dx = %d → x = <b>%d</b>." % (n1, k, d, tot, k + 1, tot - d, x))

    def ardisik():
        n = ch([2, 3, 4])
        x = ri(-20, 40)
        s = sum(x + i for i in range(n))
        word = {2: "İki", 3: "Üç", 4: "Dört"}[n]
        return M("Toplamları %s olan %s ardışık tam sayının en küçüğü kaçtır?" % (sn(s), word.lower()), sn(x),
                 [sn(x + 1), sn(x - 1), sn(F(s, n)) if s % n else sn(x + n - 1)],
                 "En küçüğü x olsun: %s = %s → %dx = %s → x = <b>%s</b>." % (" + ".join(["x"] + ["(x + %d)" % i for i in range(1, n)]), sn(s), n, sn(s - n * (n - 1) // 2), sn(x)))

    def fiyat():
        a = ri(2, 6)
        p = ri(5, 40) * 5
        f = ri(10, 60)
        T = a * p + f
        it = ch(["defter", "kitap", "tişört", "kalem kutusu"])
        return M("%d %s ve %d TL’lik bir çanta için toplam %s TL ödendi. Bir %s kaç TL’dir? (Bir %s x TL)" % (a, it, f, num(T), it, it), "%s TL" % num(p),
                 ["%s TL" % num((T + f) // a) if (T + f) % a == 0 else "%s TL" % num(p + 5), "%s TL" % num(T // a), "%s TL" % num(p - 5)],
                 "%dx + %d = %s → %dx = %s → x = <b>%s TL</b>." % (a, f, num(T), a, num(T - f), num(p)))

    def butce():
        b = ri(20, 60) * 10
        p = ch([15, 20, 25, 30, 35, 40])
        g = b // p
        return M("Bir öğrencinin %s TL’si var. Tanesi %d TL olan kitaplardan en fazla kaç tane alabilir? (%d · n ≤ %s)" % (num(b), p, p, num(b)),
              num(g), [num(g + 1), num(b // 10), num(g - 1) if g > 1 else num(g + 2)], "%d · n ≤ %s → n ≤ %s; n doğal sayı olduğundan en fazla <b>%d</b>." % (p, num(b), sn(F(b, p)), g))

    def en_az():
        need = ri(60, 90)
        k = ri(3, 5)
        sc = [ri(50, 100) for _ in range(k - 1)]
        rest = need * k - sum(sc)
        if not 0 < rest <= 100:
            return None
        nm = G.K.next()
        return M("%s ilk %d sınavından %s puan aldı. %d sınavın ortalamasının en az %d olması için son sınavdan en az kaç puan almalıdır?" % (nm, k - 1, ", ".join(map(str, sc)), k, need), num(rest),
                 [num(need), num(rest + 5), num(rest - 3)], "(%s + p) ÷ %d ≥ %d → p ≥ %d · %d − %d = <b>%d</b>." % (" + ".join(map(str, sc)), k, need, need, k, sum(sc), rest))

    sets = [("Yaş problemleri", [(yas, 20)]),
            ("Ardışık sayılar", [(ardisik, 20)]),
            ("Fiyat problemleri", [(fiyat, 20)]),
            ("Eşitsizlik problemleri", [(butce, 10), (en_az, 10)]),
            ("Karışık", [(yas, 5), (ardisik, 5), (fiyat, 5), (en_az, 5)])]
    return unit("denklem-ve-esitsizlik-problemleri", "C6", "MAT.7.2.2", 13, "Denklem ve Eşitsizlik Problemleri", "Denklem Problemleri",
                "Gerçek yaşam problemlerinde nicelikleri ve aralarındaki eşitlik ya da eşitsizlik ilişkilerini belirler; denklem veya eşitsizlik kurup çözer ve sonucu kontrol eder.",
                "7. sınıf denklem ve eşitsizlik problemleri çalışma kâğıdı: yaş problemleri, ardışık sayılar, fiyat problemleri, bütçe ve ‘en az kaç puan’ problemleri. 100 soru ve cevap anahtarı.",
                "Bilinmeyene harf ver, ilişkiyi yaz", "Sonra denklemi çöz ve cevabı soruya göre kontrol et.", sets,
                ["Problemde aranan niceliğe bir harf veririz (örneğin x). Diğer nicelikleri bu harf cinsinden yazarız.",
                 "Metindeki ‘eşittir, toplamı …’ ifadeleri denklem; ‘en az, en fazla, en çok’ ifadeleri eşitsizlik kurmamızı sağlar.",
                 "Çözümden sonra sonucu metinde yerine koyup kontrol ederiz; adet ve yaş gibi nicelikler doğal sayı olmalıdır."],
                [("Ardışık üç tam sayının toplamı 48", ["x + (x + 1) + (x + 2) = 48", "3x + 3 = 48"], "15, 16, 17"),
                 ("150 TL ile 35 TL’lik kitaptan en fazla kaç tane", ["35n ≤ 150", "n ≤ 4,28…"], "4 tane")],
                [["Harf verilen niceliği karıştırmak", "x’in neyi gösterdiğini başta yaz"],
                 ["Eşitsizlikte sonucu yuvarlamak", "n ≤ 4,28 ise en fazla 4 (5 olmaz)"],
                 ["Soruda isteneni değil x’i cevap vermek", "‘En büyüğü’ soruluyorsa x + 2’yi hesapla"]],
                [("Problemde denklem mi, eşitsizlik mi kurmalıyım?", "‘Eşittir, toplamı’ gibi kesin ilişkiler denklem; ‘en az, en fazla, aşmamalı’ gibi sınırlar eşitsizlik gerektirir."),
                 ("Ardışık tam sayılar nasıl yazılır?", "x, x + 1, x + 2 … Ardışık çift sayılar ise x, x + 2, x + 4 …"),
                 ("Cevap kesirli çıkarsa?", "Adet soruluyorsa en yakın uygun doğal sayıyı seç ve koşulu yeniden kontrol et.")])


# ============================================================ 14. sayılarla ispat
def u14():
    def cift_tek():
        S = [("İki tek sayının toplamı", "her zaman çifttir", ["her zaman tektir", "bazen tek bazen çifttir", "her zaman 4’ün katıdır"], "(2m + 1) + (2n + 1) = 2(m + n + 1): 2’nin katı, çift."),
             ("Bir çift ile bir tek sayının toplamı", "her zaman tektir", ["her zaman çifttir", "bazen çifttir", "her zaman 3’ün katıdır"], "2m + (2n + 1) = 2(m + n) + 1: tek."),
             ("İki çift sayının toplamı", "her zaman çifttir", ["her zaman tektir", "bazen tektir", "her zaman 4’ün katıdır"], "2m + 2n = 2(m + n): çift."),
             ("İki tek sayının çarpımı", "her zaman tektir", ["her zaman çifttir", "bazen çifttir", "her zaman 3’ün katıdır"], "(2m + 1)(2n + 1) = 4mn + 2m + 2n + 1 = 2(…) + 1: tek."),
             ("Bir çift sayı ile herhangi bir tam sayının çarpımı", "her zaman çifttir", ["her zaman tektir", "bazen tektir", "her zaman sıfırdır"], "2m · n = 2(mn): çift."),
             ("Ardışık iki tam sayının toplamı", "her zaman tektir", ["her zaman çifttir", "bazen çifttir", "her zaman 4’ün katıdır"], "n + (n + 1) = 2n + 1: tek."),
             ("Ardışık iki tam sayının çarpımı", "her zaman çifttir", ["her zaman tektir", "bazen tektir", "her zaman 3’ün katıdır"], "İki ardışık sayıdan biri mutlaka çifttir; çarpım çifttir."),
             ("Ardışık üç tam sayının toplamı", "her zaman 3’ün katıdır", ["her zaman çifttir", "her zaman tektir", "her zaman 6’nın katıdır"], "n + (n + 1) + (n + 2) = 3n + 3 = 3(n + 1): 3’ün katı.")]
        t, g, w, e = ch(S)
        n = ri(1, 40)
        ex = {"İki tek sayının toplamı": (2 * n + 1, 2 * ri(1, 40) + 1), "Bir çift ile bir tek sayının toplamı": (2 * n, 2 * ri(1, 40) + 1),
              "İki çift sayının toplamı": (2 * n, 2 * ri(1, 40)), "İki tek sayının çarpımı": (2 * n + 1, 2 * ri(1, 9) + 1),
              "Bir çift sayı ile herhangi bir tam sayının çarpımı": (2 * n, ri(1, 30)), "Ardışık iki tam sayının toplamı": (n, n + 1),
              "Ardışık iki tam sayının çarpımı": (n, n + 1), "Ardışık üç tam sayının toplamı": (n, n + 2)}[t]
        tail = "%d ile %d arasındaki sayıları" % ex if t.startswith("Ardışık üç") else "%d ve %d sayılarını" % ex
        return M("Örnekleri inceleyip genelleyiniz: %s için hangisi doğrudur? (Örnek: %s deneyin.)" % (t, tail), g, w, e + " Cevap: <b>%s</b>." % g)

    def cebir():
        S = [("Bir çift sayı", "2n"), ("Bir tek sayı", "2n + 1"), ("Ardışık iki tam sayı", "n ve n + 1"), ("Bir sayının 3 katı", "3n"),
             ("5’in katı olan bir sayı", "5n"), ("Ardışık iki çift sayı", "2n ve 2n + 2"), ("Ardışık iki tek sayı", "2n + 1 ve 2n + 3"), ("4’e bölündüğünde 1 kalanını veren sayı", "4n + 1")]
        t, g = ch(S)
        w = [x for _, x in S if x != g]
        return M("n bir tam sayı olmak üzere, ‘%s’ cebirsel olarak nasıl gösterilir?" % t.lower() if t[0] not in "0123456789" else "n bir tam sayı olmak üzere, ‘%s’ cebirsel olarak nasıl gösterilir?" % t, g, sh(w),
                 "Genel gösterim, n yerine her tam sayı yazıldığında doğru örnek verir: <b>%s</b>." % g)

    def karsi():
        S = [("Her asal sayı tektir.", "2"), ("İki sayının toplamı her zaman ikisinden de büyüktür.", "−3 + 2 = −1"),
             ("Bir sayının karesi her zaman sayının kendisinden büyüktür.", "(1/2)² = 1/4"), ("Çarpım her zaman çarpanlardan büyüktür.", "5 · 0 = 0"),
             ("Negatif iki sayının çarpımı negatiftir.", "(−2) · (−3) = 6"), ("Bir sayıyı bölmek onu her zaman küçültür.", "6 ÷ (1/2) = 12"),
             ("Ardışık iki sayının çarpımı tektir.", "2 · 3 = 6"), ("Her tek sayı asaldır.", "9")]
        t, g = ch(S)
        w = [x for _, x in S if x != g]
        return M("‘%s’ önermesinin yanlış olduğunu gösteren karşıt örnek hangisidir?" % t, g, sh(w)[:3] + ["Karşıt örnek yoktur"],
                 "Tek bir karşıt örnek, genel bir önermenin yanlış olduğunu göstermeye yeter: <b>%s</b>." % g)

    def oruntu():
        a, d = ri(-5, 10), nz(-6, 7)
        seq = [a + d * i for i in range(5)]
        n = ri(10, 40)
        g = a + d * (n - 1)
        return M("%s, … örüntüsünün genel terimi %s ise %d. terimi kaçtır?" % (", ".join(sn(x) for x in seq), lin(d, "n", a - d), n), sn(g),
                 [sn(g + d), sn(d * n), sn(g - d)], "Genel terim %s; n = %d için <b>%s</b>." % (lin(d, "n", a - d), n, sn(g)))

    def genel():
        a, d = ri(-5, 10), nz(-6, 7)
        seq = [a + d * i for i in range(5)]
        g = lin(d, "n", a - d)
        w = [lin(d, "n", a), lin(a, "n", d) if a not in (0,) else lin(d + 1, "n", a), lin(d, "n", a - d + 1), lin(-d, "n", a + d)]
        return M("%s, … örüntüsünün n. terimini veren ifade hangisidir?" % ", ".join(sn(x) for x in seq), g, w,
                 "Ardışık terimlerin farkı %s, kural %s · n ile başlar; n = 1 için %s olmalı: <b>%s</b>." % (sn(d), sn(d), sn(a), g))

    sets = [("Tek ve çift sayılar", [(cift_tek, 20)]),
            ("Cebirsel gösterim", [(cebir, 8), (cift_tek, 12)]),
            ("Karşıt örnek", [(karsi, 8), (oruntu, 12)]),
            ("Örüntünün genel terimi", [(genel, 20)]),
            ("Karışık", [(oruntu, 8), (genel, 6), (cift_tek, 6)])]
    return unit("sayilarla-ispat-ve-oruntuler", "C6", "MAT.7.2.3", 14, "Sayılar ve Özellikleriyle İlgili İspat", "Sayılarla İspat",
                "Sayılar ve özellikleriyle ilgili ispatlara yönelik matematiksel akıl yürütür; örnek ve örüntülerden varsayım oluşturur, sınar ve cebirsel ispat yöntemlerini kullanır.",
                "7. sınıf sayılarla ispat çalışma kâğıdı: tek ve çift sayıların toplamı ve çarpımı, cebirsel gösterim (2n, 2n + 1), karşıt örnek, örüntülerin genel terimi. 100 soru ve cevap anahtarı.",
                "Örnek göstermez, ispat gösterir", "2n, 2n + 1 ile ispat; tek karşıt örnek çürütür.", sets,
                ["Birkaç örnekten bir varsayım çıkarırız. Varsayımın her zaman doğru olduğunu göstermek için cebirsel ispat yaparız.",
                 "Çift sayı 2n, tek sayı 2n + 1 biçiminde yazılır (n tam sayı). Ardışık sayılar n, n + 1, n + 2 …",
                 "Bir genellemenin yanlış olduğunu göstermek için tek bir karşıt örnek yeter."],
                [("Ardışık üç tam sayının toplamı 3’ün katıdır", ["n + (n + 1) + (n + 2) = 3n + 3", "3(n + 1)"], "Her zaman 3’ün katı"),
                 ("‘Her asal sayı tektir’", ["2 asal ve çift"], "Karşıt örnek: 2")],
                [["Birkaç örnekle ispat yapıldığını sanmak", "Örnekler varsayım verir; ispat için cebir gerekir"],
                 ["Tek sayıyı 2n − 1 yazmayı yanlış sanmak", "2n − 1 de tek sayıdır; 2n + 1 ile aynı kümeyi verir"],
                 ["İki tek sayıyı 2n + 1 ve 2n + 1 yazmak", "Farklı sayılar için farklı harf: 2m + 1 ve 2n + 1"]],
                [("İspat ne demektir?", "Bir önermenin her durumda doğru olduğunu mantıklı adımlarla göstermektir."),
                 ("Karşıt örnek ne işe yarar?", "Genel bir önermenin yanlış olduğunu tek bir örnekle gösterir."),
                 ("Örüntüde n neyi gösterir?", "Terimin sıra numarasını gösterir: 1., 2., 3. terim …")])


# ============================================================ 15. algoritmalar
def u15():
    def cikti():
        a, b, c = nz(-6, 6), nz(-9, 9), ri(2, 5)
        x = nz(-8, 8)
        v = (a * x + b) * c
        L = ["1. Başla", "2. Bir x sayısı al (x = %s)" % sn(x), "3. x’i %s ile çarp" % sn(a), "4. Sonuca %s ekle" % sn(b), "5. Sonucu %d ile çarp" % c, "6. Sonucu yaz, bitir"]
        return M("Algoritmanın çıktısı kaçtır?" + code(L), sn(v), [sn(a * x + b * c), sn(a * x + b + c), sn(-v)],
                 "%s · %s = %s; %s + %s = %s; %s · %d = <b>%s</b>." % (sn(a), par(x), sn(a * x), sn(a * x), par(b), sn(a * x + b), par(a * x + b), c, sn(v)))

    def ifade():
        a, b = nz(-6, 6), nz(-9, 9)
        o = ch(["once_carp", "once_topla"])
        if o == "once_carp":
            L = ["1. Başla", "2. Bir x sayısı al", "3. x’i %s ile çarp" % sn(a), "4. Sonuca %s ekle" % sn(b), "5. Sonucu yaz, bitir"]
            g, w = lin(a, "x", b), [lin(a, "x", a * b), "%s(x + %s)" % (sn(a), sn(b)), lin(b, "x", a)]
        else:
            L = ["1. Başla", "2. Bir x sayısı al", "3. x’e %s ekle" % sn(b), "4. Sonucu %s ile çarp" % sn(a), "5. Sonucu yaz, bitir"]
            g, w = lin(a, "x", a * b), [lin(a, "x", b), lin(b, "x", a), lin(a, "x", a + b)]
        return M("Algoritmanın verdiği sonucu gösteren cebirsel ifade hangisidir?" + code(L), g, w,
                 "Adımları sırayla cebirsel ifadeye çeviririz: <b>%s</b>." % g)

    def sira():
        a, b = ri(2, 9), ri(2, 12)
        e = "%dx − %d = %d" % (a, b, a * ri(2, 9) - b)
        x = (int(e.split("= ")[1]) + b) // a
        steps = ["Eşitliğin iki tarafına %d ekle" % b, "İki tarafı %d ile böl" % a, "x’in değerini yaz", "Çözümü denklemde yerine koyup kontrol et"]
        g = " → ".join("%d" % i for i in (1, 2, 3, 4))
        order = sh(range(4))
        shown = ["%s. %s" % ("ABCD"[i], steps[order[i]]) for i in range(4)]
        good = "".join("ABCD"[order.index(k)] for k in range(4))
        cands = set()
        while len(cands) < 3:
            p = "".join(sh(list(good)))
            if p != good:
                cands.add(p)
        return M("%s denklemini çözen algoritmanın adımları karışık verilmiştir. Doğru sıralama hangisidir?%s" % (e, code(shown)), " – ".join(good), [" – ".join(c) for c in cands],
                 "Önce sabit terimden kurtulur, sonra katsayıya böler, sonucu yazar ve kontrol ederiz: <b>%s</b> (x = %d)." % (" – ".join(good), x))

    def dongu():
        s, d, n = ri(-10, 10), nz(-5, 6), ri(3, 6)
        v = s + d * n
        L = ["1. Başla", "2. sayı ← %s" % sn(s), "3. %d kez tekrar et:" % n, NB * 6 + "sayı ← sayı %s %d" % ("+" if d > 0 else MINUS, abs(d)), "4. sayıyı yaz, bitir"]
        return M("Algoritma çalıştırıldığında ekrana hangi sayı yazılır?" + code(L), sn(v), [sn(v - d), sn(s + d), sn(v + d)],
                 "Her tekrarda %s eklenir: %s + %d · %s = <b>%s</b>." % (sn(d), sn(s), n, par(d), sn(v)))

    def kosul():
        x = nz(-12, 12)
        a, b = nz(-5, 5), nz(-9, 9)
        L = ["1. Başla", "2. Bir x sayısı al (x = %s)" % sn(x), "3. Eğer x &lt; 0 ise x ← x · %s" % par(a), NB * 3 + "değilse x ← x + %s" % par(b), "4. x’i yaz, bitir"]
        v = x * a if x < 0 else x + b
        return M("Algoritmanın çıktısı kaçtır?" + code(L), sn(v), [sn(x * a if x >= 0 else x + b), sn(x), sn(-v)],
                 "x = %s, %s; bu yüzden %s: <b>%s</b>." % (sn(x), "x &lt; 0" if x < 0 else "x ≥ 0", "x · %s" % par(a) if x < 0 else "x + %s" % par(b), sn(v)))

    sets = [("Algoritmanın çıktısı", [(cikti, 20)]),
            ("Algoritma ve cebirsel ifade", [(ifade, 20)]),
            ("Tekrar eden adımlar", [(dongu, 20)]),
            ("Koşullu adımlar", [(kosul, 20)]),
            ("Adımları sıralama ve karışık", [(sira, 6), (cikti, 7), (dongu, 7)])]
    return unit("cebirsel-islemler-ve-algoritma", "C6", "MAT.7.2.4", 15, "Aritmetik ve Cebirsel İşlemlerde Algoritma", "Algoritmalar",
                "Aritmetik ve cebirsel işlemlerin sürecini algoritmik ifade yöntemleriyle yapılandırır; adımları ve aralarındaki ilişkileri açıklar ve tutarlı bir bütün oluşturur.",
                "7. sınıf algoritma çalışma kâğıdı: algoritmanın çıktısını bulma, algoritmayı cebirsel ifadeye çevirme, tekrar eden ve koşullu adımlar, denklem çözme adımlarını sıralama. 100 soru ve cevap anahtarı.",
                "Adımlar sırayla, tek tek uygulanır", "Tekrar ve ‘eğer … ise’ adımlarına dikkat.", sets,
                ["Algoritma, bir işi yapmak için sıralı adımlar listesidir. Adımlar doğal dil, sözde kod ya da akış şemasıyla yazılabilir.",
                 "Bir algoritmayı cebirsel ifadeye çevirmek için adımları sırayla uygularız: ‘x’i 3 ile çarp, 5 ekle’ → 3x + 5.",
                 "‘n kez tekrar et’ adımı aynı işlemi n kez yapar; ‘eğer … ise’ adımı koşula göre farklı işlem yaptırır."],
                [("x = −2; x’i 4 ile çarp, 7 ekle", ["4 · (−2) = −8", "−8 + 7"], "−1"), ("x’e 3 ekle, sonucu 2 ile çarp", ["(x + 3) · 2"], "2x + 6")],
                [["Adımların sırasını değiştirmek", "‘Önce ekle sonra çarp’ ile ‘önce çarp sonra ekle’ farklı sonuç verir"],
                 ["Tekrar sayısını eksik saymak", "3 kez tekrar: işlem 3 kez yapılır"],
                 ["Koşulu kontrol etmeden işlem yapmak", "Önce x’in koşulu sağlayıp sağlamadığına bak"]],
                [("Algoritma ile program aynı mı?", "Algoritma çözüm adımlarıdır; program bu adımların bir bilgisayar dilinde yazılmış hâlidir."),
                 ("Akış şemasında hangi şekiller kullanılır?", "Başla/bitir için oval, işlem için dikdörtgen, karar için eşkenar dörtgen."),
                 ("Algoritmanın doğru olduğunu nasıl anlarım?", "Birkaç farklı girdiyle çalıştırıp sonuçları elle hesapladıklarınla karşılaştır.")])


# ============================================================ 16. yansıma
def grid_pts(pts, axis, labels=(), extra=(), n=10, title="koordinat düzleminde şekil ve simetri doğrusu"):
    C = 22
    W = H = n * C + 20
    s = ["<svg viewBox='0 0 %d %d' role='img' aria-label='%s'>" % (W, H, title)]
    for i in range(n + 1):
        s.append("<line x1='%d' y1='10' x2='%d' y2='%d' stroke='#d5dde3'/>" % (10 + i * C, 10 + i * C, 10 + n * C))
        s.append("<line x1='10' y1='%d' x2='%d' y2='%d' stroke='#d5dde3'/>" % (10 + i * C, 10 + n * C, 10 + i * C))
    def P(p):
        return (10 + p[0] * C, 10 + (n - p[1]) * C)
    if pts:
        s.append("<polygon points='%s' fill='#a8d5ba' fill-opacity='.7' stroke='%s' stroke-width='2'/>" % (" ".join("%d,%d" % P(p) for p in pts), GREEN))
    for poly_, col in extra:
        s.append("<polygon points='%s' fill='none' stroke='%s' stroke-width='2' stroke-dasharray='5 3'/>" % (" ".join("%d,%d" % P(p) for p in poly_), col))
    if axis:
        k, kind = axis
        if kind == "v":
            s.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='2.4' stroke-dasharray='6 4'/>" % (10 + k * C, 10 + k * C, H - 4, RED))
        else:
            s.append("<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.4' stroke-dasharray='6 4'/>" % (10 + (n - k) * C, W - 4, 10 + (n - k) * C, RED))
    for p, lab in labels:
        x, y = P(p)
        s.append("<circle cx='%d' cy='%d' r='4' fill='%s'/><text x='%d' y='%d' font-size='13' font-weight='700' fill='%s'>%s</text>" % (x, y, INK, x + 6, y - 6, INK, lab))
    return "<div class='qfig'>" + G.lg("".join(s) + "</svg>") + "</div>"


def refl(p, axis):
    k, kind = axis
    return (2 * k - p[0], p[1]) if kind == "v" else (p[0], 2 * k - p[1])


def u16():
    def nokta():
        axis = (ri(3, 7), ch(["v", "h"]))
        k = axis[0]
        if axis[1] == "v":
            p = (ri(max(0, 2 * k - 10), k - 1), ri(1, 9))
        else:
            p = (ri(1, 9), ri(max(0, 2 * k - 10), k - 1))
        q = refl(p, axis)
        if axis[1] == "v":
            cands = [q, (q[0] + 1, q[1]), (q[0] - 1, q[1]) if q[0] - 1 > k else (q[0] + 2, q[1]), (q[0], q[1] + ch([1, -1]))]
        else:
            cands = [q, (q[0], q[1] + 1), (q[0], q[1] - 1) if q[1] - 1 > k else (q[0], q[1] + 2), (q[0] + ch([1, -1]), q[1])]
        if len(set(cands)) < 4 or any(not (1 <= c[0] <= 9 and 1 <= c[1] <= 9) for c in cands) or p in cands:
            return None
        labs = sh(["A", "B", "C", "D"])
        return M("P noktasının kırmızı doğruya göre yansıma görüntüsü hangi noktadır?" + grid_pts([], axis, [(p, "P")] + [(c, labs[i]) for i, c in enumerate(cands[:4])]),
                 labs[0], labs[1:], "Görüntü, simetri doğrusuna P ile aynı uzaklıkta ve doğruya dik doğrultuda karşı taraftadır: <b>%s</b>." % labs[0])

    def sekil():
        axis = (5, ch(["v", "h"]))
        while True:
            if axis[1] == "v":
                pts = [(ri(1, 4), ri(1, 9)) for _ in range(3)]
            else:
                pts = [(ri(1, 9), ri(1, 4)) for _ in range(3)]
            a, b, c = pts
            if abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])) >= 4:
                break
        good = [refl(p, axis) for p in pts]
        shift = [(p[0] + (5 if axis[1] == "v" else 0), p[1] + (5 if axis[1] == "h" else 0)) for p in pts]
        bad1 = [(10 - p[0], 10 - p[1]) for p in pts]
        bad2 = [(g[0] + (1 if axis[1] == "v" else 0), g[1] + (1 if axis[1] == "h" else 0)) for g in good]
        opts = [good, shift, bad1, bad2]
        if len({tuple(sorted(o)) for o in opts}) < 4 or any(not all(0 <= x <= 10 and 0 <= y <= 10 for x, y in o) for o in opts):
            return None
        order = sh(range(4))
        cols = ["#2f6fc4", "#d35400", "#8e44ad", "#16a085"]
        extra = [(opts[order[i]], cols[i]) for i in range(4)]
        labs = [((sum(x for x, _ in opts[order[i]]) / 3.0, sum(y for _, y in opts[order[i]]) / 3.0), "ABCD"[i]) for i in range(4)]
        j = order.index(0)
        return M("Yeşil üçgenin kırmızı doğruya göre yansıma görüntüsü kesik çizgili üçgenlerden hangisidir? (Harf üçgenin ortasındadır.)" + grid_pts(pts, axis, labs, extra),
                 "ABCD"[j], [x for i, x in enumerate("ABCD") if i != j], "Her köşe, doğruya eşit uzaklıkta karşı tarafa yansır: <b>%s</b>." % "ABCD"[j])

    def ozellik():
        S = [("Yansıma dönüşümünde şekil ile görüntüsü için hangisi doğrudur?", "Eştir (boyut ve şekil aynı)", ["Görüntü daha büyüktür", "Görüntü daha küçüktür", "Yalnızca açıları eşittir"]),
             ("Bir noktanın görüntüsü ile simetri doğrusu arasındaki uzaklık için hangisi doğrudur?", "Noktanın doğruya uzaklığına eşittir", ["İki katıdır", "Yarısıdır", "Her zaman 1 birimdir"]),
             ("Bir nokta ile yansıma görüntüsünü birleştiren doğru parçası simetri doğrusuyla nasıl bir açı yapar?", "Dik açı (90°)", ["45°", "180°", "Açı yapmaz, paraleldir"]),
             ("Simetri doğrusu üzerindeki bir noktanın yansıma görüntüsü nerededir?", "Kendisiyle aynı noktadır", ["Doğrunun sağındadır", "Doğrunun solundadır", "Görüntüsü yoktur"]),
             ("Yansıma dönüşümünde değişen özellik hangisidir?", "Şeklin yönü (sağ-sol)", ["Kenar uzunlukları", "Açı ölçüleri", "Alanı"]),
             ("Bir açının simetri doğrusu aynı zamanda nedir?", "Açıortayı", ["Kenarortayı", "Yüksekliği", "Köşegeni"]),
             ("Bir doğru parçasının (uç noktalarını birbirine yansıtan) simetri doğrusu aynı zamanda nedir?", "Orta dikmesi", ["Açıortayı", "Kenarortayı", "Paraleli"])]
        q, g, w = ch(S)
        return M(q, g, w, "Yansıma dönüşümü uzunlukları ve açıları korur; şekil görüntüsüyle eştir, yalnızca yönü değişir. Cevap: <b>%s</b>." % g)

    def uzaklik():
        k = ri(3, 7)
        x = ri(0, k - 1)
        d = k - x
        return M("Dikey simetri doğrusu x = %d çizgisidir. P noktası bu doğrunun %d birim solundadır. P ile görüntüsü P′ arasındaki uzaklık kaç birimdir?" % (k, d), num(2 * d),
                 [num(d), num(d + 1), num(2 * d + 2)], "P′ doğrunun %d birim sağındadır; aradaki uzaklık %d + %d = <b>%d</b> birim." % (d, d, d, 2 * d))

    def es_mi():
        axis = (5, "v")
        pts = [(ri(1, 4), ri(1, 9)) for _ in range(3)]
        a, b, c = pts
        if abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])) < 4:
            return None
        img = [refl(p, axis) for p in pts]
        mv = ri(0, 1)
        if mv:
            img = [(img[0][0] + 1, img[0][1])] + img[1:]
        ok = "Hayır" if mv else "Evet"
        return M("Kesik çizgili üçgen, yeşil üçgenin kırmızı doğruya göre yansıması mıdır?" + grid_pts(pts, axis, extra=[(img, "#2f6fc4")]), ok,
                 ["Evet" if mv else "Hayır", "Yalnızca iki köşe için", "Karar verilemez"],
                 "Her köşenin doğruya uzaklığını karşılaştırırız. %s" % ("Bir köşe 1 birim kaymış: <b>Hayır</b>." if mv else "Bütün köşeler eşit uzaklıkta yansımış: <b>Evet</b>."))

    sets = [("Noktanın görüntüsü", [(nokta, 20)]),
            ("Şeklin görüntüsü", [(sekil, 20)]),
            ("Yansıma mı?", [(es_mi, 12), (uzaklik, 8)]),
            ("Yansımanın özellikleri", [(ozellik, 7), (uzaklik, 6), (nokta, 7)]),
            ("Karışık", [(sekil, 8), (es_mi, 6), (nokta, 6)])]
    return unit("yansima-donusumu", "D", "MAT.7.3.1", 16, "Yansıma Dönüşümü", "Yansıma Dönüşümü",
                "Şekillerin yansıma dönüşümü altındaki görüntülerini oluşturmaya dair çıkarım yapar; şekil ile görüntüsü arasındaki ilişkiyi ve iki eş şeklin bir doğruya göre simetrik olup olmadığını değerlendirir.",
                "7. sınıf yansıma dönüşümü çalışma kâğıdı: noktanın ve üçgenin bir doğruya göre yansıması, görüntünün doğru olup olmadığı, yansımanın özellikleri (eşlik, uzaklık, diklik). 100 soru ve cevap anahtarı.",
                "Görüntü doğruya aynı uzaklıkta", "Şekil ile görüntüsü eştir; yalnızca yönü değişir.", sets,
                ["Yansıma dönüşümünde her nokta, simetri doğrusuna dik doğrultuda ve aynı uzaklıkta karşı tarafa taşınır.",
                 "Şekil ile görüntüsü eştir: kenar uzunlukları ve açı ölçüleri değişmez; sağ ile sol yer değiştirir.",
                 "Bir nokta ile görüntüsünü birleştiren doğru parçası simetri doğrusuna diktir ve bu doğru tarafından ortadan ikiye bölünür."],
                [("x = 5 doğrusunun 3 birim solundaki P(2, 4)", ["Görüntü 3 birim sağda"], "P′(8, 4)"), ("Bir açının simetri doğrusu", ["Açıyı iki eş parçaya böler"], "Açıortay")],
                [["Görüntüyü aynı tarafa çizmek", "Görüntü doğrunun karşı tarafındadır"],
                 ["Uzaklığı yanlış saymak", "Kareleri doğruya dik doğrultuda say"],
                 ["Yansımayı ötelemeyle karıştırmak", "Ötelemede yön değişmez; yansımada sağ-sol yer değiştirir"]],
                [("Yansıma ile simetri aynı şey mi?", "Bir şekil ile yansıması birlikte simetrik bir şekil oluşturur; simetri doğrusu yansıma doğrusudur."),
                 ("Görüntüye neden P′ denir?", "P′ (P üssü) P noktasının görüntüsü olduğunu gösterir."),
                 ("Ayna yansıma dönüşümüne örnek midir?", "Evet. Aynadaki görüntü aynaya eşit uzaklıkta ve aynı büyüklüktedir.")])


# ============================================================ 17. orta dikme ve açıortay
def u17():
    def aciortay():
        a = ch(range(20, 171, 2))
        return M("Ölçüsü %d° olan bir açının açıortayı, açıyı ölçüleri kaç derece olan iki açıya ayırır?" % a, "%d°" % (a // 2), ["%d°" % a, "%d°" % (180 - a), "%d°" % (90 - a // 2) if a < 180 else "45°"],
                 "Açıortay açıyı iki eş parçaya böler: %d ÷ 2 = <b>%d°</b>." % (a, a // 2))

    def aciortay_ters():
        h = ri(12, 85)
        return M("[OC, AOB açısının açıortayıdır. m(AOC) = %d° ise m(AOB) kaç derecedir?" % h, "%d°" % (2 * h), ["%d°" % h, "%d°" % (180 - h), "%d°" % (90 + h)],
                 "Açıortay açıyı iki eş parçaya böler: m(AOB) = 2 · %d = <b>%d°</b>." % (h, 2 * h))

    def orta():
        L = ri(6, 40)
        return M("d doğrusu [AB]’nin orta dikmesidir ve d ile [AB] M noktasında kesişiyor. |AB| = %d cm ise |AM| kaç cm’dir?" % L, dq(F(L, 2)) + " cm",
                 [num(L) + " cm", dq(F(L, 4)) + " cm", num(L + 2) + " cm"], "Orta dikme doğru parçasını iki eş parçaya böler: %d ÷ 2 = <b>%s cm</b>." % (L, dq(F(L, 2))))

    def esit_uzak():
        x = ri(2, 12)
        a, b = ri(2, 5), ri(1, 15)
        d = a * x + b
        m = ri(1, a - 1) if a > 1 else 1
        e = d - m * x
        return M("P noktası [AB]’nin orta dikmesi üzerindedir. |PA| = (%s) cm ve |PB| = (%s) cm ise x kaçtır?" % (lin(a, "x", b), lin(m, "x", e)), num(x),
                 [num(x + 1), num(x * 2), num(d)], "Orta dikme üzerindeki her nokta uç noktalara eşit uzaklıktadır: %s = %s → %s = %s → x = <b>%d</b>." % (lin(a, "x", b), lin(m, "x", e), lin(a - m, "x"), sn(e - b), x))

    def ozellik():
        S = [("Bir doğru parçasının orta dikmesi üzerindeki her nokta için hangisi doğrudur?", "Doğru parçasının uç noktalarına eşit uzaklıktadır", ["Uç noktalardan birine daha yakındır", "Doğru parçasına paraleldir", "Doğru parçasının üzerindedir"]),
             ("Bir açının açıortayı üzerindeki her nokta için hangisi doğrudur?", "Açının kollarına eşit uzaklıktadır", ["Köşeye eşit uzaklıktadır", "Kollardan birine daha yakındır", "Açının dışındadır"]),
             ("Orta dikme, doğru parçası ile kaç derecelik açı yapar?", "90°", ["45°", "60°", "180°"]),
             ("Pergel ve cetvelle orta dikme çizerken pergel uç noktalara nasıl yerleştirilir?", "Her iki uçtan aynı açıklıkla (yarısından büyük) yaylar çizilir", ["Yalnızca bir uçtan yay çizilir", "Açıklık yarısından küçük seçilir", "Pergel kullanılmaz"]),
             ("Açıortay çizerken ilk adım hangisidir?", "Köşe merkezli bir yayla iki kolu kesmek", ["Kolları uzatmak", "Köşeden dik çizmek", "Kolların orta noktasını bulmak"])]
        q, g, w = ch(S)
        return M(q, g, w, "Orta dikme, doğru parçasının simetri doğrusudur; açıortay, açının simetri doğrusudur. Cevap: <b>%s</b>." % g)

    def kol():
        a = ri(30, 160)
        k = ch([2, 3])
        if a % (4 if k == 2 else 2):
            return None
        return M("Bir AOB açısının ölçüsü %d°’dir. [OC açıortaydır. [OD de AOC açısının açıortayıdır. m(AOD) kaç derecedir?" % a if k == 2 else "m(AOB) = %d°. [OC açıortaydır. m(COB) + m(AOB) kaç derecedir?" % a,
                 ("%s°" % sn(F(a, 4))) if k == 2 else "%d°" % (a + a // 2),
                 (["%d°" % (a // 2), "%s°" % sn(F(a, 8)), "%d°" % a] if k == 2 else ["%d°" % a, "%d°" % (2 * a), "%d°" % (a // 2)]),
                 ("m(AOC) = %d ÷ 2 = %d°; m(AOD) = %d ÷ 2 = <b>%s°</b>." % (a, a // 2, a // 2, sn(F(a, 4)))) if k == 2 else "m(COB) = %d°; toplam %d + %d = <b>%d°</b>." % (a // 2, a // 2, a, a + a // 2))

    sets = [("Açıortay", [(aciortay, 10), (aciortay_ters, 10)]),
            ("Orta dikme", [(orta, 20)]),
            ("Eşit uzaklık", [(esit_uzak, 20)]),
            ("Özellikler ve çizim", [(ozellik, 5), (kol, 15)]),
            ("Karışık", [(aciortay, 5), (orta, 5), (esit_uzak, 5), (kol, 5)])]
    return unit("orta-dikme-ve-aciortay", "D", "MAT.7.3.2", 17, "Orta Dikme ve Açıortay", "Orta Dikme ve Açıortay",
                "Yansıma dönüşümündeki deneyimlerini orta dikme ve açıortay inşasına yansıtır; simetri doğrusunun özelliklerinden orta dikme ve açıortay çizimini çıkarır.",
                "7. sınıf orta dikme ve açıortay çalışma kâğıdı: açıortay açıyı iki eş açıya böler, orta dikme doğru parçasını ortadan dik keser, uç noktalara eşit uzaklık, çizim adımları. 100 soru ve cevap anahtarı.",
                "Açıortay: açının simetri doğrusu", "Orta dikme: doğru parçasının simetri doğrusu (ortadan, dik).", sets,
                ["Bir açının simetri doğrusu açıortaydır; açıyı ölçüleri eşit iki açıya böler.",
                 "Bir doğru parçasının simetri doğrusu orta dikmedir; doğru parçasını orta noktasından keser ve ona diktir.",
                 "Orta dikme üzerindeki her nokta doğru parçasının uç noktalarına eşit uzaklıktadır. Açıortay üzerindeki her nokta açının kollarına eşit uzaklıktadır."],
                [("m(AOB) = 84°, [OC açıortay", ["84 ÷ 2"], "m(AOC) = 42°"), ("P orta dikme üzerinde, |PA| = 2x + 3, |PB| = 15", ["2x + 3 = 15"], "x = 6")],
                [["Açıortayı açıyı 90°’ye bölen doğru sanmak", "Açıortay açıyı iki eş parçaya böler"],
                 ["Orta dikmenin yalnızca ortadan geçtiğini düşünmek", "Hem ortadan geçer hem diktir"],
                 ["Eşit uzaklığı yanlış iki noktaya uygulamak", "Orta dikmede uç noktalara (A ve B) eşit uzaklık"]],
                [("Orta dikme ile kenarortay aynı mı?", "Hayır. Orta dikme bir doğru parçasının ortasından geçen dik doğrudur; kenarortay üçgende köşeyi karşı kenarın ortasına birleştirir."),
                 ("Açıortayı katlayarak bulabilir miyim?", "Evet. Kâğıdı açının iki kolu üst üste gelecek biçimde katlarsan kat yeri açıortaydır."),
                 ("Bunlar neden yansımayla ilgili?", "Çünkü ikisi de simetri doğrusudur: açıortay kolları, orta dikme uç noktaları birbirine yansıtır.")])


# ============================================================ 18. kenarortay, açıortay, yükseklik
def cevian(kind, labels=("A", "B", "C", "D")):
    """ABC üçgeni, A’dan [BC]’ye bir doğru parçası; kind: 'k' kenarortay, 'a' açıortay, 'h' yükseklik"""
    import math as _m
    B, C = (40.0, 190.0), (320.0, 190.0)
    A = (ch([110.0, 130.0, 150.0, 200.0, 220.0]), ch([30.0, 40.0, 55.0]))
    if kind == "k":
        D = ((B[0] + C[0]) / 2, 190.0)
    elif kind == "h":
        D = (A[0], 190.0)
    else:
        ab = _m.hypot(A[0] - B[0], A[1] - B[1])
        ac = _m.hypot(A[0] - C[0], A[1] - C[1])
        t = ab / (ab + ac)
        D = (B[0] + (C[0] - B[0]) * t, 190.0)
    s = ["<svg viewBox='0 0 360 225' role='img' aria-label='üçgen ve bir köşeden çizilen doğru parçası'>",
         "<polygon points='%.0f,%.0f %.0f,%.0f %.0f,%.0f' fill='%s' stroke='%s' stroke-width='2.4'/>" % (A + B + C + (FILL, GREEN)),
         "<line x1='%.0f' y1='%.0f' x2='%.0f' y2='%.0f' stroke='%s' stroke-width='2.4'/>" % (A + D + (RED,))]
    if kind == "k":
        for P, Q in ((B, D), (D, C)):
            mx = (P[0] + Q[0]) / 2
            s.append("<line x1='%.0f' y1='183' x2='%.0f' y2='197' stroke='%s' stroke-width='2'/>" % (mx, mx, INK))
    elif kind == "h":
        s.append("<path d='M%.0f 178 L%.0f 178 L%.0f 190' fill='none' stroke='%s' stroke-width='1.6'/>" % (D[0], D[0] + 12, D[0] + 12, INK))
    else:
        def ang(P):
            return _m.atan2(P[1] - A[1], P[0] - A[0])
        for P, Q in ((B, D), (D, C)):
            a1, a2 = ang(P), ang(Q)
            r = 26
            m = (a1 + a2) / 2
            s.append("<path d='M%.1f %.1f A%d %d 0 0 %d %.1f %.1f' fill='none' stroke='%s' stroke-width='1.6'/>" % (A[0] + r * _m.cos(a1), A[1] + r * _m.sin(a1), r, r, 0 if a1 > a2 else 1, A[0] + r * _m.cos(a2), A[1] + r * _m.sin(a2), INK))
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.6'/>" % (A[0] + (r - 4) * _m.cos(m), A[1] + (r - 4) * _m.sin(m), A[0] + (r + 4) * _m.cos(m), A[1] + (r + 4) * _m.sin(m), INK))
    for P, lab, dx, dy in ((A, labels[0], 0, -8), (B, labels[1], -14, 6), (C, labels[2], 14, 6), (D, labels[3], 0, 22)):
        s.append("<text x='%.0f' y='%.0f' font-size='15' font-weight='700' text-anchor='middle' fill='%s'>%s</text>" % (P[0] + dx, P[1] + dy, INK, lab))
    return "<div class='qfig'>" + G.lg("".join(s) + "</svg>") + "</div>"


NAMES = {"k": "Kenarortay", "a": "Açıortay", "h": "Yükseklik"}


def u18():
    def tani():
        kind = ch("kah")
        g = NAMES[kind]
        w = [v for k, v in NAMES.items() if k != kind] + ["Orta dikme"]
        why = {"k": "[BD] ile [DC] üzerindeki çizgiler eşit uzunluğu gösterir: D, [BC]’nin orta noktası.",
               "a": "A köşesindeki iki açı eşit işaretli: açıyı iki eş parçaya bölüyor.",
               "h": "D’deki işaret dik açıyı gösterir: [AD] ⊥ [BC]."}[kind]
        return M("Şekilde kırmızı [AD] doğru parçası ABC üçgeninin neyidir?" + cevian(kind), g, w, why + " Cevap: <b>%s</b>." % g)

    def kenar():
        L = ri(5, 30) * 2
        return M("[AD], ABC üçgeninde [BC] kenarına ait kenarortaydır. |BC| = %d cm ise |BD| kaç cm’dir?" % L, "%d cm" % (L // 2), ["%d cm" % L, "%d cm" % (L // 4) if L % 4 == 0 else "%d cm" % (L // 2 + 1), "%d cm" % (L * 2)],
                 "Kenarortay karşı kenarı iki eş parçaya böler: %d ÷ 2 = <b>%d cm</b>." % (L, L // 2))

    def aci():
        a = ri(20, 70) * 2
        b = ri(20, 160 - a)
        c = 180 - a - b
        return M("ABC üçgeninde m(A) = %d°, m(B) = %d°. [AD] açıortay ise m(BAD) kaç derecedir?" % (a, b), "%d°" % (a // 2), ["%d°" % a, "%d°" % (c // 2) if c % 2 == 0 else "%d°" % (c), "%d°" % (90 - a // 2)],
                 "Açıortay A açısını iki eş parçaya böler: %d ÷ 2 = <b>%d°</b>." % (a, a // 2))

    def ikiz():
        S = [("İkizkenar bir üçgende tepe açısından tabana çizilen kenarortay için hangisi doğrudur?", "Aynı zamanda açıortay ve yüksekliktir", ["Yalnızca kenarortaydır", "Tabana paraleldir", "Tabanı 1’e 2 oranında böler"]),
             ("Eşkenar üçgende bir kenara ait kenarortay için hangisi doğrudur?", "Aynı zamanda açıortay ve yüksekliktir", ["Yalnızca yüksekliktir", "Açıortay olamaz", "Kenarı ikiye bölmez"]),
             ("Bir üçgenin üç kenarortayının kesiştiği noktaya ne denir?", "Ağırlık merkezi", ["Orta dikme", "Açıortay", "Köşe"]),
             ("Bir üçgende yükseklik ile ait olduğu kenar arasındaki açı kaç derecedir?", "90°", ["45°", "60°", "180°"]),
             ("Bir üçgenin kaç tane kenarortayı vardır?", "3", ["1", "2", "6"]),
             ("Çeşitkenar bir üçgende bir köşeden çizilen kenarortay ile açıortay için hangisi doğrudur?", "Genellikle farklı doğru parçalarıdır", ["Her zaman aynıdır", "Her zaman diktir", "İkisi de yüksekliktir"])]
        q, g, w = ch(S)
        a, b = ri(30, 80), 0
        return M(q, g, w, "Kenarortay karşı kenarın orta noktasına, açıortay açıyı ikiye bölerek, yükseklik dik olarak iner. İkizkenar ve eşkenar üçgende bunlar çakışabilir. Cevap: <b>%s</b>." % g)

    def ikiz_hesap():
        t = ri(10, 40) * 2
        k = ri(25, 75) * 2
        return M("İkizkenar ABC üçgeninde |AB| = |AC| ve |BC| = %d cm’dir. A’dan [BC]’ye çizilen yükseklik [BC]’yi D noktasında kesiyor. m(BAC) = %d° ise |BD| ve m(BAD) nedir?" % (t, k),
                 "%d cm ve %d°" % (t // 2, k // 2), ["%d cm ve %d°" % (t, k // 2), "%d cm ve %d°" % (t // 2, k), "%d cm ve %d°" % (t // 2, 90 - k // 2)],
                 "İkizkenar üçgende tabana inen yükseklik aynı zamanda kenarortay ve açıortaydır: |BD| = %d ÷ 2, m(BAD) = %d ÷ 2 → <b>%d cm ve %d°</b>." % (t, k, t // 2, k // 2))

    sets = [("Hangisi?", [(tani, 20)]),
            ("Kenarortay", [(kenar, 20)]),
            ("Açıortay", [(aci, 20)]),
            ("İkizkenar ve eşkenar üçgen", [(ikiz_hesap, 14), (ikiz, 6)]),
            ("Karışık", [(tani, 8), (kenar, 4), (aci, 4), (ikiz_hesap, 4)])]
    return unit("ucgende-kenarortay-aciortay-ve-yukseklik", "GS", "MAT.7.5.1, MAT.7.5.2", 18, "Üçgende Kenarortay, Açıortay ve Yükseklik", "Kenarortay ve Açıortay",
                "Matematiksel araç ve teknolojiden yararlanarak üçgende kenarortay, açıortay ve yüksekliği çözümler; orta dikme inşası deneyimini kenarortay inşasına yansıtır.",
                "7. sınıf üçgende kenarortay, açıortay ve yükseklik çalışma kâğıdı: şekilde hangisi olduğunu bulma, kenarortayın böldüğü uzunluk, açıortayın böldüğü açı, ikizkenar ve eşkenar üçgende özel durumlar, ağırlık merkezi. 100 soru ve cevap anahtarı.",
                "Kenarortay → orta nokta", "Açıortay → açıyı ikiye böler, yükseklik → dik iner.", sets,
                ["Kenarortay: bir köşeyi karşı kenarın orta noktasına birleştiren doğru parçası. Karşı kenarı iki eş parçaya böler. Üç kenarortay ağırlık merkezinde kesişir.",
                 "Açıortay: bir köşedeki açıyı iki eş açıya bölen doğru parçası. Yükseklik: bir köşeden karşı kenara (ya da uzantısına) dik inen doğru parçası.",
                 "İkizkenar üçgende tabana ait kenarortay aynı zamanda açıortay ve yüksekliktir. Eşkenar üçgende bu her kenar için geçerlidir."],
                [("|BC| = 18 cm, [AD] kenarortay", ["D orta nokta"], "|BD| = 9 cm"), ("m(A) = 70°, [AD] açıortay", ["70 ÷ 2"], "m(BAD) = 35°")],
                [["Kenarortayı açıortay sanmak", "Kenarortay kenarı, açıortay açıyı ikiye böler"],
                 ["Yüksekliğin her zaman üçgenin içinde olduğunu düşünmek", "Geniş açılı üçgende yükseklik dışarıda olabilir"],
                 ["Her üçgende kenarortay ile açıortayın çakıştığını sanmak", "Yalnızca ikizkenar üçgende tabana ait olanlar çakışır"]],
                [("Ağırlık merkezi neden önemlidir?", "Üçgen biçimindeki ince bir levha bu noktadan tutulursa dengede durur."),
                 ("Kenarortay nasıl çizilir?", "Önce karşı kenarın orta dikmesini çizerek orta noktayı bulur, sonra köşeyle birleştiririz."),
                 ("Bir üçgende kaç yükseklik vardır?", "Her kenara bir tane olmak üzere 3 yükseklik vardır.")])


UNITS = [u10, u11, u12, u13, u14, u15, u16, u17, u18]
