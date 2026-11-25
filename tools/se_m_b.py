# -*- coding: utf-8 -*-
"""Sverige åk 4–6: bråk, decimaltal, procent, algebra, mönster, proportionalitet（lv = 4, 5, 6）"""
import math
from fractions import Fraction as F
import se_m as S
from se_m import num, kr, M, fr, fq, d, ri, ch, sh, cap, unit, tab
from se_common import tallinje, wrap, text, line, INK, GREEN, FILL, RED
from se_m_a import R0


def K():
    return S.K


NAMN = {2: "halv", 3: "tredjedel", 4: "fjärdedel", 5: "femtedel", 6: "sjättedel", 8: "åttondel", 10: "tiondel", 12: "tolftedel", 100: "hundradel"}
PL = {2: "halvor", 3: "tredjedelar", 4: "fjärdedelar", 5: "femtedelar", 6: "sjättedelar", 8: "åttondelar", 10: "tiondelar", 12: "tolftedelar", 100: "hundradelar"}


def bar(n, k, w=300, h=36, col="#7fb3d5"):
    cw = w / float(n)
    s = ["<rect x='%.1f' y='6' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (6 + i * cw, cw, h, col if i < k else "#ffffff", INK) for i in range(n)]
    return wrap(w + 12, h + 12, "".join(s), "remsa i %d lika delar, %d färgade" % (n, k))


def bars(n, k):
    """flera hela: k delar färgade, n delar per hel"""
    w = int(math.ceil(k / float(n)))
    s = []
    cw = 220.0 / n
    for j in range(w):
        for i in range(n):
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='30' fill='%s' stroke='%s' stroke-width='2'/>" % (6 + i * cw, 6 + j * 40, cw, "#f4a261" if j * n + i < k else "#ffffff", INK))
    return wrap(232, w * 40 + 6, "".join(s), "%d remsor i %d delar, %d delar färgade" % (w, n, k))


def grid100(k):
    s = []
    for i in range(100):
        x, y = i % 10, i // 10
        s.append("<rect x='%d' y='%d' width='14' height='14' fill='%s' stroke='%s' stroke-width='0.8'/>" % (6 + x * 14, 6 + y * 14, "#81b29a" if i < k else "#ffffff", INK))
    return wrap(152, 152, "".join(s), "hundraruta med %d färgade rutor" % k)


# ============================================================ bråk
def brak(lv):
    dens = [2, 3, 4, 5, 6, 8, 10] if lv == 4 else [2, 3, 4, 5, 6, 8, 10, 12]

    def bild():
        n = ch(dens)
        k = ri(1, n - 1)
        return M(bar(n, k) + "Hur stor del av remsan är färgad?", fr(k, n), [fr(n - k, n) if n - k != k else fr(k, n + 1), fr(k, n - k) if n - k != k else fr(k + 1, n), fr(n, k)],
                 "Remsan har %d lika delar och %d är färgade: <b>%d/%d</b>." % (n, k, k, n))

    def av_antal():
        n = ch([2, 3, 4, 5, 6, 8, 10])
        k = ri(1, n - 1)
        m = ri(2, 12)
        t = n * m
        thing = ch(["elever", "kulor", "bullar", "kronor", "sidor", "minuter"])
        return M("Hur mycket är %s av %d %s?" % (fr(k, n), t, thing), "%d %s" % (k * m, thing), ["%d %s" % x for x in [(m, thing), (t - k * m, thing), (k * m + k, thing), (t // k if t % k == 0 and t // k != k * m else k * m + m, thing)]],
                 "%s av %d = %d. Då är %s av %d = %d × %d = <b>%d</b>." % (fr(1, n), t, m, fr(k, n), t, k, m, k * m))

    def jamfor():
        if lv == 4:
            a, b = sh(dens)[:2]
            k = 1
            big = fr(1, min(a, b))
            return M("Vilket är störst, %s eller %s?" % (fr(1, a), fr(1, b)), big, [fr(1, max(a, b)), "De är lika stora", "Det går inte att jämföra"],
                     "Ju fler delar det hela delas i, desto mindre är varje del. Störst är <b>%s</b>." % big.replace("<", "<"))
        n = ch(dens)
        x, y = sorted(sh(range(1, n))[:2]) if n > 2 else (None, None)
        if x is None or lv == 5 and R0():
            k = ri(1, 5)
            a, b = sorted(sh([3, 4, 5, 6, 8, 10])[:2])
            if k >= a:
                return None
            return M("Vilket är störst, %s eller %s?" % (fr(k, a), fr(k, b)), fr(k, a), [fr(k, b), "De är lika stora", "Det går inte att jämföra"],
                     "Samma täljare: färre delar ger större delar. <b>%d/%d</b> är störst." % (k, a))
        if lv == 6 and R0():
            a, b = ch([(2, 4), (3, 6), (2, 6), (4, 8), (2, 8), (5, 10), (3, 12), (4, 12), (2, 10)])
            p = ri(1, a - 1)
            q = ri(1, b - 1)
            if F(p, a) == F(q, b):
                return None
            g = fr(p, a) if F(p, a) > F(q, b) else fr(q, b)
            return M("Vilket är störst, %s eller %s?" % (fr(p, a), fr(q, b)), g, [fr(q, b) if g == fr(p, a) else fr(p, a), "De är lika stora", "Det går inte att jämföra"],
                     "Förläng till samma nämnare: %s = %s. Jämför sedan täljarna." % (fr(p, a), fr(p * b // a, b)))
        return M("Vilket är störst, %s eller %s?" % (fr(x, n), fr(y, n)), fr(y, n), [fr(x, n), "De är lika stora", "Det går inte att jämföra"],
                 "Samma nämnare: den med störst täljare är störst, <b>%d/%d</b>." % (y, n))

    def blandad():
        n = ch([2, 3, 4, 5, 6, 8])
        w = ri(1, 4)
        r = ri(1, n - 1)
        t = w * n + r
        if R0():
            return M(bars(n, t) + "Hur många hela och delar är färgade? Skriv i blandad form.", fq(F(t, n), True), [fq(F(t, n + 1), True) if t > n + 1 else fr(t, n + 1), "%d%s" % (w + 1, fr(r, n)), "%d%s" % (w, fr(n - r, n)) if n - r != r else fr(t, n)],
                     "%d hela och %d/%d: <b>%d %d/%d</b>, alltså %d/%d." % (w, r, n, w, r, n, t, n))
        return M("Skriv %s i blandad form." % fr(t, n), fq(F(t, n), True), ["%d%s" % (w, fr(r + 1, n)) if r + 1 < n else "%d%s" % (w + 1, fr(1, n)), "%d%s" % (t // 10 or 1, fr(t % 10 or 1, n)), "%d%s" % (r, fr(w, n)) if r != w else "%d%s" % (w + 1, fr(r, n))],
                 "%d/%d = %d hela (%d/%d) och %d/%d kvar: <b>%d %d/%d</b>." % (t, n, w, w * n, n, r, n, w, r, n))

    def linje():
        n = ch([2, 3, 4, 5, 6, 8, 10]) if lv == 4 else ch([3, 4, 5, 6, 8, 10, 12])
        k = ri(1, n - 1)
        pic = tallinje(0, n, 1, [(k, "A")], labels=[0, n], width=360).replace(">%d<" % n, ">1<")
        return M(pic + "Vilket bråk visar pilen A? Sträckan från 0 till 1 är delad i %d lika delar." % n, fr(k, n), [fr(k, n + 1), fr(n - k, n) if n - k != k else fr(k + 1, n), fr(k, 10) if n != 10 else fr(k, 100)],
                 "Pilen står %d steg från 0, och varje steg är 1/%d: <b>%d/%d</b>." % (k, n, k, n))

    def likvardig():
        n = ch([2, 3, 4, 5, 6])
        k = ri(1, n - 1)
        m = ri(2, 5)
        if F(k, n).denominator != n:
            return None
        return M("Vilket bråk med nämnaren %d är lika mycket som %s?" % (n * m, fr(k, n)), fr(k * m, n * m), [fr(k + m, n + m), fr(k * m, n), fr(k, n * m), fr(k * m + 1, n * m)],
                 "Förläng: multiplicera både täljare och nämnare med %d: <b>%d/%d</b>." % (m, k * m, n * m))

    def forkorta():
        n = ch([2, 3, 4, 5])
        k = ri(1, n - 1)
        m = ri(2, 6)
        if F(k, n).denominator != n:
            return None
        return M("Förkorta %s så mycket som möjligt." % fr(k * m, n * m), fr(k, n), [fr(k * m - m, n * m - m) if k > 1 else fr(1, n * m // 2) if (n * m) % 2 == 0 else fr(2, n * m), fr(k * m, n), fr(k, n * m)] + [fr(k * m // 2, n * m // 2)] if m % 2 == 0 and m > 2 else [fr(k * m, n), fr(k, n * m), fr(k + 1, n)],
                 "Dela både täljare och nämnare med %d: <b>%d/%d</b>." % (m, k, n))

    def plus_samma():
        n = ch([4, 5, 6, 8, 10, 12])
        a, b = ri(1, n - 2), ri(1, n - 2)
        if R0():
            if a + b > n + 3:
                return None
            s = F(a + b, n)
            return M("%s + %s = ?" % (fr(a, n), fr(b, n)), fr(a + b, n), [fr(a + b, 2 * n), fr(a * b, n) if a * b != a + b else fr(a + b + 1, n), fr(a + b, n + n // 2)],
                     "Samma nämnare: lägg ihop täljarna. %d + %d = %d: <b>%d/%d</b>%s." % (a, b, a + b, a + b, n, " = %s" % fq(s, True) if s > 1 else ""))
        if a == b:
            return None
        a, b = max(a, b), min(a, b)
        return M("%s − %s = ?" % (fr(a, n), fr(b, n)), fr(a - b, n), [fr(a - b, 0 if False else n * 2), fr(a + b, n), fr(a - b + 1, n)],
                 "Samma nämnare: dra bort täljarna. %d − %d = %d: <b>%d/%d</b>." % (a, b, a - b, a - b, n))

    def plus_olika():
        a, b = ch([(2, 4), (3, 6), (2, 6), (4, 8), (2, 8), (5, 10), (3, 12), (4, 12), (2, 10), (6, 12)])
        p, q = ri(1, a - 1), ri(1, b - 1)
        sub = R0() and F(p, a) > F(q, b)
        res = F(p, a) - F(q, b) if sub else F(p, a) + F(q, b)
        m = b // a
        num_ = p * m - q if sub else p * m + q
        return M("%s %s %s = ? (Svara i den nämnare som är störst.)" % (fr(p, a), "−" if sub else "+", fr(q, b)), fr(num_, b),
                 [fr(abs(p - q) if sub else p + q, a + b), fr(abs(p - q) if sub else p + q, b), fr(num_ + 1, b), fr(num_, a)],
                 "Förläng %s till %s. %s %s %s = <b>%s</b>." % (fr(p, a), fr(p * m, b), fr(p * m, b), "−" if sub else "+", fr(q, b), fr(num_, b)))

    def ganger():
        n = ch([3, 4, 5, 6, 8])
        k = ri(1, n - 1)
        m = ri(2, 6)
        p = F(k * m, n)
        return M("%d × %s = ?" % (m, fr(k, n)), fq(p, True) if p.denominator != 1 else str(p.numerator) if False else fq(p, True),
                 [fr(k * m, n * m), fr(k + m, n), fq(F(k * m, n) + 1, True), fr(k, n * m)],
                 "Multiplicera täljaren: %d × %d = %d, alltså %s%s." % (m, k, k * m, fr(k * m, n), " = <b>%s</b>" % fq(p, True) if p > 1 else " (<b>%s</b>)" % fq(p)))

    def text_():
        nm, g = K().next()
        k = ri(0, 2)
        if k == 0:
            n = ch([3, 4, 5])
            t = n * ri(4, 15)
            return M("En klass har %d elever. %s av eleverna har cykel. Hur många elever har cykel?" % (t, fr(1, n)), str(t // n), [str(t - t // n), str(n), str(t // n + 1)],
                     "%d : %d = <b>%d</b>." % (t, n, t // n))
        if k == 1:
            n = ch([4, 5, 8, 10])
            a = ri(1, n - 2)
            return M("%s äter %s av en pizza och hennes bror äter %s. Hur stor del av pizzan har de ätit?" % (nm, fr(a, n), fr(1, n)) if g == "f" else
                     "%s äter %s av en pizza och hans syster äter %s. Hur stor del av pizzan har de ätit?" % (nm, fr(a, n), fr(1, n)),
                     fr(a + 1, n), [fr(a + 1, 2 * n), fr(a, n), fr(n - a - 1, n) if n - a - 1 != a + 1 else fr(a + 2, n)], "%s + %s = <b>%s</b>." % (fr(a, n), fr(1, n), fr(a + 1, n)))
        n = ch([3, 4, 5])
        kk = ri(1, n - 1)
        if math.gcd(kk, n) > 1:
            return None
        t = n * ri(10, 40)
        return M("En bok har %d sidor. %s har läst %s av boken. Hur många sidor har %s läst?" % (t, nm, fr(kk, n), "hon" if g == "f" else "han"), str(t * kk // n),
                 [str(t // n), str(t - t * kk // n) if kk * 2 != n else str(t // n + kk), str(t * kk // n + kk)], "%s av %d = %d, så %s av %d = <b>%d</b>." % (fr(1, n), t, t // n, fr(kk, n), t, t * kk // n))

    if lv == 4:
        sets = [("Del av en helhet", [(bild, 20)]), ("Bråk på tallinjen", [(linje, 20)]), ("Del av ett antal", [(av_antal, 20)]),
                ("Jämföra bråk och blandad form", [(jamfor, 10), (blandad, 10)]), ("Textuppgifter", [(text_, 20)])]
    elif lv == 5:
        sets = [("Bråk på tallinjen", [(linje, 12), (bild, 8)]), ("Likvärdiga bråk", [(likvardig, 20)]), ("Jämföra och blandad form", [(jamfor, 10), (blandad, 10)]),
                ("Addition och subtraktion", [(plus_samma, 20)]), ("Del av antal och textuppgifter", [(av_antal, 10), (text_, 10)])]
    else:
        sets = [("Förlänga och förkorta", [(likvardig, 10), (forkorta, 10)]), ("Jämföra bråk", [(jamfor, 12), (blandad, 8)]),
                ("Addition och subtraktion", [(plus_samma, 8), (plus_olika, 12)]), ("Bråk gånger heltal", [(ganger, 20)]),
                ("Del av antal och textuppgifter", [(av_antal, 10), (text_, 10)])]
    return unit("brak", "T", "Bråk: del av helhet, del av antal och blandad form" if lv == 4 else "Bråk: likvärdiga bråk, jämföra och räkna med bråk", "Bråk",
                "Tal i bråkform och deras användning i vardagliga situationer. Del av helhet och del av antal%s." % ("" if lv == 4 else ", likvärdiga bråk och beräkningar med bråk"),
                "Arbetsblad om bråk för årskurs %d: %s. 100 uppgifter med facit." % (lv, "del av helhet, bråk på tallinjen, del av antal, jämföra bråk och blandad form" if lv == 4 else
                                                                                       "likvärdiga bråk, jämföra bråk, blandad form, addition och subtraktion och del av antal" if lv == 5 else
                                                                                       "förlänga och förkorta, jämföra bråk, addition och subtraktion med olika nämnare och bråk gånger heltal"),
                "Nämnaren visar delarna", "Täljaren visar hur många delar du tar.", sets,
                ["Ett bråk beskriver lika stora delar av en helhet. I 3/5 är 5 nämnaren (hur många delar det hela har) och 3 täljaren (hur många delar du tar).",
                 "Del av antal: 3/4 av 20. Räkna först 1/4 av 20 = 5, sedan 3 × 5 = 15.",
                 "Likvärdiga bråk är lika stora fast de skrivs olika: 1/2 = 2/4 = 3/6. Du förlänger genom att multiplicera täljare och nämnare med samma tal."
                 + (" För att addera bråk med olika nämnare förlänger du först till samma nämnare." if lv == 6 else "")],
                [("3/4 av 20", ["1/4 av 20 = 5", "3 × 5"], "15"), ("7/4 i blandad form", ["4/4 = 1 hel", "3/4 kvar"], "1 3/4")] if lv == 4 else
                [("2/5 + 1/5", ["Samma nämnare", "2 + 1 = 3"], "3/5"), ("Vilket bråk är lika mycket som 2/3?", ["Förläng med 4"], "8/12")] if lv == 5 else
                [("1/2 + 3/8", ["1/2 = 4/8", "4/8 + 3/8"], "7/8"), ("Förkorta 12/18", ["Dela med 6"], "2/3")],
                [["1/5 är större än 1/3 eftersom 5 &gt; 3", "Fler delar ger mindre bitar: 1/3 är större"], ["2/5 + 1/5 = 3/10", "Nämnaren ändras inte: 3/5"],
                 ["3/4 av 20 = 5", "Det är 1/4 av 20. 3/4 är tre gånger så mycket: 15"]],
                [("Vad heter delarna i ett bråk?", "Talet ovanför bråkstrecket är täljaren och talet under är nämnaren."),
                 ("Vad är blandad form?", "Ett tal med heltal och bråk, till exempel 2 1/4. Det är samma sak som 9/4."),
                 ("Ändras bråkets värde när jag förlänger?", "Nej. 1/2 och 2/4 är exakt lika mycket.")])


# ============================================================ decimaltal
def decimaltal(lv):
    def bild():
        k = ri(1, 99) if lv >= 5 else ri(1, 9)
        if lv >= 5:
            return M(grid100(k) + "Hur stor del av hundrarutan är färgad? Skriv som decimaltal.", d(F(k, 100)), [d(F(k, 10)) if k < 10 else num(k), d(F(k, 1000)), d(F(100 - k, 100))],
                     "%d av 100 rutor = %d hundradelar = <b>%s</b>." % (k, k, d(F(k, 100))))
        return M(bar(10, k) + "Hur stor del av remsan är färgad? Skriv som decimaltal.", d(F(k, 10)), [d(F(k, 100), 2), str(k), d(F(10 - k, 10))],
                 "%d av 10 delar = %d tiondelar = <b>%s</b>." % (k, k, d(F(k, 10))))

    def bratil():
        den = ch([10, 100] if lv == 4 else [10, 100, 1000])
        k = ri(1, den - 1)
        if k % 10 == 0 and den > 10:
            return None
        x = F(k, den)
        p = len(str(den)) - 1
        return M("Skriv %s som decimaltal." % fr(k, den), d(x, p), [d(F(k, den * 10), p + 1), d(F(k, den // 10), max(p - 1, 0)) if den > 10 else str(k), "%d,%d" % (k, den)],
                 "%s = %d %s = <b>%s</b>." % (fr(k, den), k, {10: "tiondelar", 100: "hundradelar", 1000: "tusendelar"}[den], d(x, p)))

    def jamfor():
        p = 2 if lv == 4 else 3
        a = ri(1, 9) + F(ri(1, 10 ** p - 1), 10 ** p)
        xs = {a}
        while len(xs) < 4:
            b = int(a) + F(ri(1, 10 ** p - 1), 10 ** p) if R0() else int(a) + F(ri(1, 9), 10)
            xs.add(b)
        xs = sh(sorted(xs))
        big = R0()
        g = max(xs) if big else min(xs)
        return M("Vilket tal är <b>%s</b>? %s" % ("störst" if big else "minst", ", ".join(d(x) for x in xs)), d(g), [d(x) for x in xs if x != g],
                 "Jämför tiondelarna först, sedan hundradelarna%s. Svar: <b>%s</b>." % (" och tusendelarna" if p == 3 else "", d(g)))

    def linje():
        lo = ri(0, 8)
        k = ri(1, 9)
        v = lo + F(k, 10)
        pic = tallinje(0, 10, 1, [(k, "A")], labels=[0, 10], width=360).replace(">10<", ">%d<" % (lo + 1)).replace(">0<", ">%d<" % lo, 1)
        if lo + 1 == 10:
            return None
        return M(pic + "Vilket decimaltal visar pilen A?", d(v), [d(lo + F(k, 100)), d(lo + F(10 - k, 10)) if k != 5 else d(lo + F(6, 10)), "%d,%d" % (lo + k, 0) if False else d(lo + k)],
                 "Sträckan från %d till %d är delad i 10 tiondelar. Pilen står på %d tiondelar: <b>%s</b>." % (lo, lo + 1, k, d(v)))

    def tio():
        x = F(ri(11, 9999), ch([10, 100, 1000]))
        t = ch([10, 100, 1000])
        if R0():
            return M("%s × %s = ?" % (d(x), num(t)), d(x * t), [d(x * t * 10), d(x * t / 10), d(x + t)],
                     "Gånger %s: kommat flyttas %d steg åt höger. <b>%s</b>." % (num(t), len(str(t)) - 1, d(x * t)))
        try:
            ans = d(x / t)
        except ValueError:
            return None
        return M("%s : %s = ?" % (d(x), num(t)), ans, [d(x / t * 10), d(x / t / 10) if (x / t / 10 * 10 ** 6).denominator == 1 else d(x * 10), d(x * t)],
                 "Delat med %s: kommat flyttas %d steg åt vänster. <b>%s</b>." % (num(t), len(str(t)) - 1, ans))

    def enheter():
        k = ri(0, 3)
        if k == 0:
            c = ri(105, 995)
            return M("Skriv %d cm i meter." % c, d(F(c, 100)) + " m", [d(F(c, 10)) + " m", d(F(c, 1000)) + " m", num(c) + " m"], "100 cm = 1 m. %d cm = <b>%s m</b>." % (c, d(F(c, 100))))
        if k == 1:
            g = ri(105, 4995)
            return M("Skriv %s g i kilogram." % num(g), d(F(g, 1000)) + " kg", [d(F(g, 100)) + " kg", d(F(g, 10)) + " kg", num(g) + " kg"], "1 000 g = 1 kg. %s g = <b>%s kg</b>." % (num(g), d(F(g, 1000))))
        if k == 2:
            x = F(ri(11, 99), 10)
            return M("Skriv %s m i centimeter." % d(x), num(int(x * 100)) + " cm", [num(int(x * 10)) + " cm", num(int(x * 1000)) + " cm", d(x) + "0 cm"], "1 m = 100 cm. %s m = <b>%s cm</b>." % (d(x), num(int(x * 100))))
        dl = ri(11, 49)
        return M("Skriv %d dl i liter." % dl, d(F(dl, 10)) + " l", [d(F(dl, 100)) + " l", num(dl * 10) + " l", num(dl) + " l"], "10 dl = 1 l. %d dl = <b>%s l</b>." % (dl, d(F(dl, 10))))

    def vardagen():
        n = K().name()
        a, b = F(ri(12, 48), 10), F(ri(12, 48), 10)
        k = ri(0, 2)
        if k == 0:
            return M("%s hoppar %s m och sedan %s m. Hur långt hoppar %s sammanlagt?" % (n, d(a), d(b), n), d(a + b) + " m", [d(a + b + 1) + " m", d(a + b - F(1, 10)) + " m", d(a + b + F(1, 10)) + " m"],
                     "%s + %s = <b>%s m</b>." % (d(a), d(b), d(a + b)))
        if k == 1:
            if a == b:
                return None
            a, b = max(a, b), min(a, b)
            return M("En planka är %s m lång. %s sågar av %s m. Hur lång är biten som är kvar?" % (d(a), n, d(b)), d(a - b) + " m", [d(a + b) + " m", d(a - b + F(1, 10)) + " m", d(abs(a - b - 1)) + " m"],
                     "%s − %s = <b>%s m</b>." % (d(a), d(b), d(a - b)))
        t = [F(ri(95, 130), 10) for _ in range(4)]
        if len(set(t)) < 4:
            return None
        names = ["Alice", "Noah", "Vera", "Hugo"]
        rows = [[nn, d(x) + " s"] for nn, x in zip(names, t)]
        best = names[t.index(min(t))]
        return M(tab(["Löpare", "Tid på 60 m"], rows) + "Vem sprang snabbast?", best, [x for x in names if x != best], "Snabbast är den som har kortast tid: <b>%s</b>, %s s." % (best, d(min(t))))

    if lv == 4:
        sets = [("Tiondelar", [(bild, 8), (linje, 12)]), ("Bråk som decimaltal", [(bratil, 20)]), ("Decimaltal på tallinjen", [(linje, 20)]),
                ("Jämföra decimaltal", [(jamfor, 20)]), ("Decimaltal i vardagen", [(vardagen, 14), (enheter, 6)])]
    elif lv == 5:
        sets = [("Hundradelar", [(bild, 20)]), ("Bråk som decimaltal", [(bratil, 20)]), ("Jämföra decimaltal", [(jamfor, 20)]),
                ("Decimaltal och enheter", [(enheter, 20)]), ("Decimaltal i vardagen", [(vardagen, 20)])]
    else:
        sets = [("Bråk som decimaltal", [(bratil, 20)]), ("Jämföra och ordna", [(jamfor, 20)]), ("Gånger och delat med 10, 100 och 1 000", [(tio, 20)]),
                ("Decimaltal och enheter", [(enheter, 20)]), ("Decimaltal i vardagen", [(vardagen, 20)])]
    return unit("decimaltal", "T", "Decimaltal: tiondelar och hundradelar" if lv == 4 else "Decimaltal: hundradelar och tusendelar" if lv == 5 else "Decimaltal: jämföra, omvandla och gånger 10, 100 och 1 000", "Decimaltal",
                "Tal i decimalform och deras användning i vardagliga situationer. Positionssystemet för tal i decimalform.",
                "Arbetsblad om decimaltal för årskurs %d: %s. 100 uppgifter med facit." % (lv, "tiondelar, bråk som decimaltal, tallinjen och att jämföra decimaltal" if lv == 4 else
                                                                                             "hundradelar, bråk som decimaltal, jämföra decimaltal och enheter" if lv == 5 else
                                                                                             "bråk som decimaltal, jämföra och ordna, gånger och delat med 10, 100 och 1 000 och enheter"),
                "Tiondelar, hundradelar, tusendelar", "Siffran direkt efter kommat är tiondelar.", sets,
                ["Till höger om decimalkommat kommer tiondelar, hundradelar och tusendelar. 3,47 = 3 hela, 4 tiondelar och 7 hundradelar.",
                 "Jämför decimaltal plats för plats från vänster. 0,6 är större än 0,58, eftersom 6 tiondelar är mer än 5 tiondelar.",
                 "Vid gånger 10 flyttas kommat ett steg åt höger och vid delat med 10 ett steg åt vänster: 3,47 × 10 = 34,7."],
                [("Skriv 7/100 som decimaltal", ["7 hundradelar", "0 tiondelar, 7 hundradelar"], "0,07"), ("Vilket är störst, 0,6 eller 0,58?", ["0,6 = 0,60", "60 hundradelar &gt; 58 hundradelar"], "0,6")],
                [["0,58 är större än 0,6 eftersom 58 &gt; 6", "Jämför tiondelarna: 6 &gt; 5"], ["7/100 = 0,7", "7 hundradelar = 0,07"],
                 ["3,47 × 10 = 3,470", "Kommat flyttas: 34,7"]],
                [("Varför använder vi decimaltal?", "För mått och tider som inte är hela tal, till exempel 1,45 m eller 12,3 sekunder."),
                 ("Är 0,5 och 0,50 samma tal?", "Ja. En nolla i slutet efter kommat ändrar inte värdet."),
                 ("Hur läser man 2,35?", "Två hela och trettiofem hundradelar, eller två komma tre fem.")])


# ============================================================ procent
def procent(lv):
    PAIRS = [(50, 1, 2), (25, 1, 4), (75, 3, 4), (10, 1, 10), (20, 1, 5), (40, 2, 5), (60, 3, 5), (30, 3, 10), (70, 7, 10), (90, 9, 10), (80, 4, 5), (100, 1, 1)]

    def ruta():
        k = ri(1, 99)
        return M(grid100(k) + "Hur många procent av hundrarutan är färgad?", "%d %%" % k, ["%d %%" % x for x in (100 - k, k + 10, k // 10 if k >= 10 else k + 1)],
                 "Procent betyder hundradelar. %d av 100 rutor = <b>%d %%</b>." % (k, k))

    def omvandla():
        p, a, b = ch(PAIRS[:-1])
        k = ri(0, 2)
        if k == 0:
            return M("Hur många procent är %s?" % fr(a, b), "%d %%" % p, ["%d %%" % x for x in sorted(set(q for q, _, _ in PAIRS) - {p}, key=lambda x: abs(x - p))[:2]] + ["%d %%" % (a * 10 + b)],
                     "%s = %s = <b>%d %%</b>." % (fr(a, b), fr(p, 100), p))
        if k == 1:
            return M("Skriv %d %% som decimaltal." % p, d(F(p, 100), 2) if p % 10 else d(F(p, 100)), [d(F(p, 1000), 3), num(p), d(F(p, 10))],
                     "%d %% = %d hundradelar = <b>%s</b>." % (p, p, d(F(p, 100))))
        return M("Skriv %d %% som ett bråk i enklaste form." % p, fr(a, b), [fr(p, 10) if p % 10 == 0 and p != 10 else fr(1, 100), fr(a, b + 1), fr(b, a) if a != b else fr(1, 2)],
                 "%d %% = %s = <b>%s</b>." % (p, fr(p, 100), fr(a, b)))

    def av():
        p, a, b = ch(PAIRS[:9] if lv == 5 else PAIRS[:-1])
        t = b * ri(2, 60) * (10 if p % 10 == 0 and b == 10 else 1)
        if lv == 5 and t > 1000:
            return None
        v = t * a // b
        return M("Hur mycket är %d %% av %s?" % (p, num(t)), num(v), [num(x) for x in (t - v, t * p, t // 10 if p != 10 else t // 5, v + 10)],
                 "%d %% = %s. %s av %s = <b>%s</b>." % (p, fr(a, b), fr(a, b), num(t), num(v)))

    def rabatt():
        p = ch([10, 20, 25, 50] if lv == 5 else [10, 20, 25, 30, 40, 50, 15])
        pr = ch([x for x in range(100, 2001, 20) if x * p % 100 == 0])
        r = pr * p // 100
        thing = ch(["en jacka", "ett par skor", "en cykelhjälm", "ett spel", "en ryggsäck", "en lampa"])
        return M("%s kostar %s. På rean är det %d %% rabatt. Vad kostar %s nu?" % (cap(thing), kr(pr), p, "den" if thing.startswith("en ") else "det"), kr(pr - r),
                 [kr(r), kr(pr - p), kr(pr + r), kr(pr - r - 10)], "%d %% av %d = %d. %d − %d = <b>%s</b>." % (p, pr, r, pr, r, kr(pr - r)))

    def hur_manga():
        p, a, b = ch(PAIRS[:-1])
        t = b * ri(2, 20)
        k = t * a // b
        what = ch(["elever har hund", "av eleverna går till skolan", "av bollarna är röda"])
        return M("I en klass med %d elever har %d elever hund. Hur många procent av eleverna har hund?" % (t, k) if what == "elever har hund" else
                 "Det finns %d bollar och %d av dem är röda. Hur många procent av bollarna är röda?" % (t, k),
                 "%d %%" % p, ["%d %%" % x for x in (k, 100 - p, p // 2 if p > 10 else p + 15) if x != p and 0 < x <= 100] + ["%d %%" % min(99, k * 10)],
                 "%d av %d = %s = %s = <b>%d %%</b>." % (k, t, fr(k, t), fr(a, b), p))

    if lv == 5:
        sets = [("Procent är hundradelar", [(ruta, 20)]), ("Bråk, decimaltal och procent", [(omvandla, 20)]), ("Procent av ett tal", [(av, 20)]),
                ("Rabatt", [(rabatt, 20)]), ("Hur många procent?", [(hur_manga, 20)])]
    else:
        sets = [("Bråk, decimaltal och procent", [(omvandla, 20)]), ("Procent av ett tal", [(av, 20)]), ("Rabatt och reapris", [(rabatt, 20)]),
                ("Hur många procent?", [(hur_manga, 20)]), ("Blandat", [(av, 8), (rabatt, 6), (ruta, 6)])]
    return unit("procent", "T", "Procent: hundradelar, procent av ett tal och rabatt", "Procent",
                "Tal i procentform och deras samband med tal i bråk- och decimalform. Proportionalitet och procent och deras samband.",
                "Arbetsblad om procent för årskurs %d: procent som hundradelar, bråk, decimaltal och procent, procent av ett tal, rabatt och hur många procent. 100 uppgifter med facit." % lv,
                "Procent = hundradelar", "50 % = hälften, 25 % = en fjärdedel, 10 % = en tiondel", sets,
                ["Procent betyder hundradelar. 35 % = 35/100 = 0,35.",
                 "Några procent är bra att kunna utantill: 50 % är hälften, 25 % är en fjärdedel, 75 % är tre fjärdedelar och 10 % är en tiondel.",
                 "Procent av ett tal: 20 % av 350. Räkna 10 % = 35 och sedan 20 % = 2 × 35 = 70. Vid rabatt drar du bort det från priset."],
                [("25 % av 240", ["25 % = 1/4", "240 : 4"], "60"), ("En tröja för 400 kr med 30 % rabatt", ["10 % = 40 kr", "30 % = 120 kr", "400 − 120"], "280 kr")],
                [["25 % av 240 = 25", "25 % är en fjärdedel: 240 : 4 = 60"], ["Svarar med rabatten i stället för det nya priset", "Dra bort rabatten från priset"],
                 ["5 % = 0,5", "5 % = 5 hundradelar = 0,05"]],
                [("Kan man ha mer än 100 %?", "Ja, till exempel när något ökar till mer än det dubbla. 100 % är det hela."),
                 ("Hur räknar jag 10 % snabbt?", "Dela med 10: 10 % av 380 är 38."),
                 ("Vad är skillnaden mellan rabatt och pris?", "Rabatten är hur mycket du slipper betala. Priset är det du betalar.")])


# ============================================================ ekvationer och uttryck
def ekvationer(lv):
    def ruta():
        a, b = ri(12, 90), ri(5, 60)
        k = ri(0, 3)
        if k == 0:
            return M("□ + %d = %d. Vilket tal står i rutan?" % (a, a + b), str(b), [str(a + b + a), str(b + 1), str(b - 10) if b > 10 else str(b + 10)], "%d − %d = <b>%d</b>." % (a + b, a, b))
        if k == 1:
            return M("%d − □ = %d. Vilket tal står i rutan?" % (a + b, a), str(b), [str(2 * a + b), str(b + 1), str(a)] if a != b else [str(b + 1), str(b - 1), str(2 * a)], "%d − %d = %d. Svar: <b>%d</b>." % (a + b, b, a, b))
        m, n = ri(3, 9), ri(3, 12)
        if k == 2:
            return M("%d × □ = %d. Vilket tal står i rutan?" % (m, m * n), str(n), [str(m * n - m), str(n + 1), str(m)] if m != n else [str(n + 1), str(n - 1), str(m * n - m)], "%d : %d = <b>%d</b>." % (m * n, m, n))
        return M("□ : %d = %d. Vilket tal står i rutan?" % (m, n), str(m * n), [str(n // m) if n > m else str(m + n), str(m + n), str(m * n + m)], "%d × %d = <b>%d</b>." % (n, m, m * n))

    def x1():
        a, b = ri(5, 80), ri(5, 60)
        k = ri(0, 3)
        if k == 0:
            return M("Lös ekvationen x + %d = %d." % (a, a + b), "x = %d" % b, ["x = %d" % v for v in (2 * a + b, b + 1, a)] if a != b else ["x = %d" % v for v in (3 * a, b + 1, b - 1)], "x = %d − %d = <b>%d</b>." % (a + b, a, b))
        if k == 1:
            return M("Lös ekvationen x − %d = %d." % (a, b), "x = %d" % (a + b), ["x = %d" % v for v in (abs(b - a) if b != a else a + 1, a + b + 1, a + b - 10)], "x = %d + %d = <b>%d</b>." % (b, a, a + b))
        m, n = ri(2, 9), ri(3, 15)
        if k == 2:
            return M("Lös ekvationen %dx = %d." % (m, m * n), "x = %d" % n, ["x = %d" % v for v in (m * n - m, m * n * m, n + 1)], "x = %d : %d = <b>%d</b>." % (m * n, m, n))
        return M("Lös ekvationen x/%d = %d." % (m, n), "x = %d" % (m * n), ["x = %d" % v for v in (n + m, n - m if n > m else m * n + m, m * n + 1)], "x = %d × %d = <b>%d</b>." % (n, m, m * n))

    def x2():
        a, x, b = ri(2, 9), ri(2, 15), ri(1, 30)
        if R0():
            c = a * x + b
            return M("Lös ekvationen %dx + %d = %d." % (a, b, c), "x = %d" % x, ["x = %d" % v for v in (x + 1, (c + b) // a if (c + b) % a == 0 else x + 2, c - b)],
                     "Dra bort %d: %dx = %d. Dela med %d: <b>x = %d</b>." % (b, a, c - b, a, x))
        c = a * x - b
        if c <= 0:
            return None
        return M("Lös ekvationen %dx − %d = %d." % (a, b, c), "x = %d" % x, ["x = %d" % v for v in (x - 1, (c - b) // a if c > b and (c - b) % a == 0 else x + 3, c + b)],
                 "Lägg till %d: %dx = %d. Dela med %d: <b>x = %d</b>." % (b, a, c + b, a, x))

    def varde():
        a = ri(2, 12)
        k = ri(0, 3) if lv == 6 else ri(0, 2)
        b, c = ri(2, 9), ri(1, 20)
        if lv == 4:
            if k == 0:
                return M("Vad är värdet av uttrycket a + %d om a = %d?" % (c, a), str(a + c), [str(a * c), str(a + c + 1), str(c)], "%d + %d = <b>%d</b>." % (a, c, a + c))
            if k == 1:
                if a <= c:
                    a += c
                return M("Vad är värdet av uttrycket a − %d om a = %d?" % (c, a), str(a - c), [str(a + c), str(a - c + 1), str(c - a) if c > a else str(a)], "%d − %d = <b>%d</b>." % (a, c, a - c))
            return M("Vad är värdet av uttrycket %d · a om a = %d?" % (b, a), str(a * b), [str(a + b), "%d%d" % (b, a), str(a * b + b)], "%d · %d = <b>%d</b>." % (b, a, a * b))
        if k == 0:
            return M("Vad är värdet av %dx + %d om x = %d?" % (b, c, a), str(b * a + c), [str(b * (a + c)), "%d%d" % (b, a + c) if int("%d%d" % (b, a)) + c != b * a + c else str(b + a + c), str(b + a + c)],
                     "%d · %d + %d = %d + %d = <b>%d</b>." % (b, a, c, b * a, c, b * a + c))
        if k == 1:
            return M("Vad är värdet av %d(x + %d) om x = %d?" % (b, c, a), str(b * (a + c)), [str(b * a + c), str(b + a + c), str(b * (a + c) + b)],
                     "Parentesen först: %d + %d = %d. Sedan %d · %d = <b>%d</b>." % (a, c, a + c, b, a + c, b * (a + c)))
        if k == 2:
            y = ri(2, 9)
            return M("Vad är värdet av x · y + x om x = %d och y = %d?" % (a, y), str(a * y + a), [str(a * (y + 1) + 1), str(a + y + a), str(a * y)],
                     "%d · %d + %d = <b>%d</b>." % (a, y, a, a * y + a))
        m, n = ri(2, 9), ri(2, 9)
        return M("Förenkla uttrycket %dx + %dx." % (m, n), "%dx" % (m + n), ["%dx" % (m * n), "%dx²" % (m + n), "%d + x" % (m + n)], "%d + %d = %d, alltså <b>%dx</b>." % (m, n, m + n, m + n))

    def uttryck():
        nm, g = K().next()
        k = ri(0, 3)
        n = ri(2, 9)
        sym = "a" if lv == 4 else "x"
        opts = [("%s har %s kulor. %s får %d kulor till. Hur många kulor har %s nu?" % (nm, sym, cap("hon" if g == "f" else "han"), n, "hon" if g == "f" else "han"), "%s + %d" % (sym, n), ["%s − %d" % (sym, n), "%d · %s" % (n, sym) if lv == 4 else "%d%s" % (n, sym), "%d" % n]),
                ("En penna kostar %s kr. Vad kostar %d pennor?" % (sym, n), "%d · %s" % (n, sym) if lv == 4 else "%d%s" % (n, sym), ["%s + %d" % (sym, n), "%s − %d" % (sym, n), "%s : %d" % (sym, n)]),
                ("%s är %s år. Hennes lillebror är %d år yngre. Hur gammal är lillebrodern?" % (nm, sym, n) if g == "f" else "%s är %s år. Hans lillebror är %d år yngre. Hur gammal är lillebrodern?" % (nm, sym, n),
                 "%s − %d" % (sym, n), ["%s + %d" % (sym, n), "%d − %s" % (n, sym), "%d · %s" % (n, sym) if lv == 4 else "%d%s" % (n, sym)]),
                ("%d kompisar delar lika på %s bullar. Hur många bullar får var och en?" % (n, sym), "%s : %d" % (sym, n), ["%d : %s" % (n, sym), "%s − %d" % (sym, n), "%d · %s" % (n, sym) if lv == 4 else "%d%s" % (n, sym)])]
        q, a, w = opts[k]
        return M(q + " Vilket uttryck passar?", a, w, "Uttrycket <b>%s</b> beskriver situationen." % a)

    def stall_upp():
        nm = K().name()
        p, m = ri(12, 60), ri(2, 6)
        c = ri(10, 90)
        tot = p * m + c if lv == 6 else p + c
        if lv == 6:
            return M("%s köper %d böcker som kostar lika mycket och en penna för %d kr. Det kostar %d kr. Vilken ekvation passar om en bok kostar x kr?" % (nm, m, c, tot),
                     "%dx + %d = %d" % (m, c, tot), ["%dx = %d" % (m, tot), "x + %d = %d" % (c, tot), "%d(x + %d) = %d" % (m, c, tot)],
                     "%d böcker kostar %dx och pennan %d kr: <b>%dx + %d = %d</b>. x = %d." % (m, m, c, m, c, tot, p))
        return M("%s hade några kronor. %s fick %d kr i veckopeng och har nu %d kr. Vilken ekvation passar om %s hade x kr?" % (nm, nm, c, tot, nm),
                 "x + %d = %d" % (c, tot), ["x − %d = %d" % (c, tot), "%d − x = %d" % (c, tot), "%dx = %d" % (c, tot)], "Det hon eller han hade (x) plus %d kr blir %d kr: <b>x + %d = %d</b>." % (c, tot, c, tot))

    if lv == 4:
        sets = [("Tal i rutan", [(ruta, 20)]), ("Värdet av ett uttryck", [(varde, 20)]), ("Skriv ett uttryck", [(uttryck, 20)]),
                ("Ekvationer", [(x1, 20)]), ("Ekvationer i vardagen", [(stall_upp, 10), (ruta, 10)])]
    elif lv == 5:
        sets = [("Tal i rutan", [(ruta, 20)]), ("Lös ekvationen", [(x1, 20)]), ("Värdet av ett uttryck", [(varde, 20)]),
                ("Skriv ett uttryck", [(uttryck, 20)]), ("Ekvationer i vardagen", [(stall_upp, 12), (x1, 8)])]
    else:
        sets = [("Lös ekvationen", [(x1, 20)]), ("Ekvationer i två steg", [(x2, 20)]), ("Värdet av ett uttryck", [(varde, 20)]),
                ("Skriv ett uttryck", [(uttryck, 20)]), ("Ekvationer i vardagen", [(stall_upp, 20)])]
    return unit("ekvationer-och-uttryck", "A", "Ekvationer och uttryck: obekanta tal och variabler", "Ekvationer och uttryck",
                "Obekanta tal och deras egenskaper samt situationer där det finns behov av att beteckna ett obekant tal med en symbol. Enkla algebraiska uttryck och ekvationer. Metoder för enkel ekvationslösning.",
                "Arbetsblad om ekvationer och uttryck för årskurs %d: obekanta tal, värdet av ett uttryck, skriv ett uttryck och lös ekvationer%s. 100 uppgifter med facit." % (lv, " i två steg" if lv == 6 else ""),
                "Gör samma sak på båda sidor", "En ekvation är en likhet med ett obekant tal.", sets,
                ["Ett obekant tal kan skrivas med en symbol eller en bokstav, till exempel □ eller x.",
                 "I en ekvation är båda sidor lika mycket. Lös den genom att göra det motsatta: x + 15 = 40 ger x = 40 − 15 = 25.",
                 "I ett uttryck som 3x + 4 betyder 3x att 3 multipliceras med x. Om x = 5 blir uttrycket 3 · 5 + 4 = 19."],
                [("x + 15 = 40", ["Dra bort 15 från båda sidor"], "x = 25"), ("3x + 4 = 19", ["3x = 15", "x = 15 : 3"], "x = 5")] if lv == 6 else
                [("x + 15 = 40", ["Dra bort 15 från båda sidor"], "x = 25"), ("4x = 36", ["Dela med 4"], "x = 9")],
                [["x + 15 = 40 ger x = 55", "Gör det motsatta: 40 − 15 = 25"], ["3x betyder 3 + x", "3x betyder 3 · x"],
                 ["Kontrollerar inte svaret", "Sätt in svaret: 25 + 15 = 40 stämmer"]],
                [("Vad är en variabel?", "En bokstav som står för ett tal som kan variera eller som vi inte vet än."),
                 ("Hur kontrollerar jag en ekvation?", "Sätt in ditt svar i stället för x och se om båda sidor blir lika."),
                 ("Varför skriver man 3x och inte 3 · x?", "Det är kortare. Mellan en siffra och en bokstav betyder det alltid gånger.")])


# ============================================================ mönster och talföljder
def dots_fig(xs, shape="rad"):
    s = []
    x = 8
    for i, v in enumerate(xs):
        for j in range(v):
            s.append("<rect x='%d' y='%d' width='9' height='9' fill='%s' stroke='%s'/>" % (x + (j % 4) * 10, 70 - (j // 4) * 10, FILL, GREEN))
        s.append(text(x + 18, 96, "Figur %d" % (i + 1), 11, weight=400))
        x += 64
    return wrap(x + 4, 102, "".join(s), "växande mönster")


def monster(lv):
    def nasta():
        st = ri(3, 25) if lv == 4 else ri(4, 60)
        a = ri(1, 200)
        up = R0() or lv == 4
        xs = [a + i * st * (1 if up else -1) for i in range(5)]
        if min(xs) < 0:
            return None
        n = xs[-1] + st * (1 if up else -1)
        if n < 0:
            return None
        return M("Hur fortsätter talföljden? %s, …" % ", ".join(num(x) for x in xs), num(n), [num(n + st), num(n - 1), num(xs[-1] + st + 1 if up else xs[-1] - st - 1)],
                 "Talen %s med %d: <b>%s</b>." % ("ökar" if up else "minskar", st, num(n)))

    def gang():
        a, k = ri(1, 5), ch([2, 3, 10])
        xs = [a * k ** i for i in range(4)]
        n = xs[-1] * k
        return M("Hur fortsätter talföljden? %s, …" % ", ".join(num(x) for x in xs), num(n), [num(xs[-1] + (xs[-1] - xs[-2])), num(n + 1), num(n * k)],
                 "Varje tal är %d gånger så stort som talet före: <b>%s</b>." % (k, num(n)))

    def figur():
        a, st = ri(1, 4), ri(2, 4)
        xs = [a + i * st for i in range(4)]
        t = ch([5, 6]) if lv == 4 else ch([10, 15, 20, 25])
        v = a + (t - 1) * st
        return M(dots_fig(xs) + "Mönstret fortsätter likadant. Hur många rutor har figur %d?" % t, str(v), [str(v + st), str(t * st) if t * st != v else str(v + 2 * st), str(v - 1)],
                 "Figur 1 har %d och varje figur får %d till. Figur %d: %d + %d · %d = <b>%d</b>." % (a, st, t, a, t - 1, st, v))

    def tabell():
        a, st = ri(1, 9), ri(2, 7)
        rows = [[str(i), str(a + st * i)] for i in range(1, 5)]
        t = ri(8, 30)
        v = a + st * t
        return M(tab(["Figur nr", "Antal stickor"], rows) + "Hur många stickor behövs till figur %d?" % t, str(v), [str(st * t), str(v + a), str(a + st * (t - 1))],
                 "Antalet ökar med %d. Regeln: %d · figurnumret + %d. %d · %d + %d = <b>%d</b>." % (st, st, a, st, t, a, v))

    def formel():
        a, st = ri(0, 9), ri(2, 6)
        good = "%dn + %d" % (st, a) if a else "%dn" % st
        rows = [[str(i), str(a + st * i)] for i in range(1, 5)]
        bad = ["n + %d" % (st + a), "%dn + %d" % (st + a, 0) if a else "%dn + 1" % st, "%dn + %d" % (a or 1, st) if a != st else "%dn − %d" % (st, a or 1)]
        return M(tab(["n", "Antal"], rows) + "Vilken formel ger antalet för figur n?", good, bad,
                 "Antalet ökar med %d varje gång, alltså %dn. För n = 1 ska det bli %d: <b>%s</b>." % (st, st, a + st, good))

    def lucka():
        st = ri(3, 30)
        a = ri(1, 100)
        xs = [a + i * st for i in range(6)]
        k = ri(1, 4)
        v = xs[k]
        return M("Vilket tal saknas? %s" % ", ".join(num(x) if i != k else "□" for i, x in enumerate(xs)), num(v), [num(v + 1), num(v - st + 1), num(v + st)],
                 "Talen ökar med %d: %s + %d = <b>%s</b>." % (st, num(xs[k - 1]), st, num(v)))

    if lv == 4:
        sets = [("Fortsätt talföljden", [(nasta, 20)]), ("Gånger-mönster", [(gang, 10), (nasta, 10)]), ("Vilket tal saknas?", [(lucka, 20)]),
                ("Växande figurer", [(figur, 20)]), ("Tabeller", [(tabell, 20)])]
    else:
        sets = [("Fortsätt talföljden", [(nasta, 12), (gang, 8)]), ("Vilket tal saknas?", [(lucka, 20)]), ("Växande figurer", [(figur, 20)]),
                ("Tabeller", [(tabell, 20)]), ("Formler", [(formel, 20)])]
    return unit("monster-och-talfoljder", "A", "Mönster och talföljder: regler, figurer och formler" if lv >= 5 else "Mönster och talföljder", "Mönster och talföljder",
                "Hur mönster i talföljder och geometriska mönster kan konstrueras, beskrivas och uttryckas.",
                "Arbetsblad om mönster för årskurs %d: fortsätt talföljder, saknade tal, växande figurer, tabeller%s. 100 uppgifter med facit." % (lv, " och formler" if lv >= 5 else " och gånger-mönster"),
                "Hitta regeln", "Hur ändras talet från en figur till nästa?", sets,
                ["Hitta regeln genom att jämföra talen som står bredvid varandra: ökar de med lika mycket varje gång, eller blir de ett visst antal gånger större?",
                 "I ett växande mönster kan du räkna ut figur nummer 10 utan att rita alla figurer: börja med figur 1 och lägg till ökningen 9 gånger.",
                 "En formel beskriver mönstret: om antalet ökar med 3 varje gång och figur 1 har 5 blir formeln 3n + 2."],
                [("Figur 1: 5, figur 2: 8, figur 3: 11", ["Ökar med 3", "Figur 10: 5 + 9 · 3"], "32"), ("Formel för 5, 8, 11, 14", ["3n", "3 · 1 + 2 = 5"], "3n + 2")],
                [["Figur 10 = 10 · 3 = 30", "Börja med figur 1: 5 + 9 · 3 = 32"], ["Tittar bara på två tal", "Kontrollera regeln på alla tal"],
                 ["Formeln n + 3", "Ökningen 3 ska stå framför n: 3n + 2"]],
                [("Vad är en talföljd?", "Tal som följer en regel, till exempel 4, 8, 12, 16 där talen ökar med 4."),
                 ("Vad betyder n i en formel?", "n är figurens nummer. Sätt in numret för att få antalet."),
                 ("Kan ett mönster minska?", "Ja, till exempel 100, 93, 86, 79 där talen minskar med 7.")])


# ============================================================ proportionalitet
def proportionalitet(lv):
    def jamforpris():
        a, b = ch([(2, 3), (3, 5), (2, 5), (4, 6), (3, 4), (5, 8)])
        p1, p2 = ri(8, 25), ri(8, 25)
        if p1 == p2:
            return None
        thing = ch([("äpplen", "kg"), ("ost", "kg"), ("saft", "liter"), ("godis", "kg")])
        c1, c2 = a * p1, b * p2
        best = "paket A" if p1 < p2 else "paket B"
        return M("Paket A: %d %s %s för %d kr. Paket B: %d %s %s för %d kr. Vilket är billigast per %s?" % (a, thing[1], thing[0], c1, b, thing[1], thing[0], c2, thing[1]),
                 best, ["paket B" if best == "paket A" else "paket A", "de kostar lika mycket per " + thing[1], "det som kostar minst totalt"],
                 "Jämförpris: A %d : %d = %d kr per %s, B %d : %d = %d kr per %s. <b>%s</b> är billigast." % (c1, a, p1, thing[1], c2, b, p2, thing[1], cap(best)))

    def recept():
        p = ch([2, 4, 6])
        q = ch([x for x in (2, 3, 4, 6, 8, 12) if x != p])
        ing = ch([("dl mjöl", ri(2, 9)), ("ägg", ri(1, 4)), ("dl mjölk", ri(3, 9)), ("g smör", ch([50, 60, 100, 120]))])
        v = F(ing[1] * q, p)
        if v.denominator != 1:
            return None
        return M("Ett recept för %d personer behöver %d %s. Hur mycket behövs för %d personer?" % (p, ing[1], ing[0], q), "%d %s" % (v, ing[0]),
                 ["%d %s" % (x, ing[0]) for x in (ing[1] + q - p, ing[1] * q, ing[1] * 2 if ing[1] * 2 != v else ing[1] + 1)],
                 "Per person: %d : %d. För %d personer: %d · %d : %d = <b>%d %s</b>." % (ing[1], p, q, ing[1], q, p, v, ing[0]))

    def tabell():
        k = ri(2, 15)
        xs = sorted(sh(range(1, 11))[:3])
        t = ri(11, 30)
        rows = [[str(x), num(k * x)] for x in xs]
        return M(tab(["Antal biljetter", "Pris (kr)"], rows) + "Priset är proportionellt mot antalet. Vad kostar %d biljetter?" % t, kr(k * t),
                 [kr(k * t + k), kr(k + t), kr(k * (t - 1))], "En biljett kostar %d kr. %d · %d = <b>%s</b>." % (k, t, k, kr(k * t)))

    def hastighet():
        v = ch([4, 5, 12, 15, 18, 20, 40, 50, 60, 70, 80, 90])
        t = ch([2, 3, 4]) if v >= 40 else ch([2, 3])
        k = ri(0, 2)
        mode = {4: "går", 5: "går", 12: "cyklar", 15: "cyklar", 18: "cyklar", 20: "cyklar"}.get(v, "kör")
        if k == 0:
            return M("En bil kör med farten %d km/h. Hur långt kommer den på %d timmar?" % (v, t) if mode == "kör" else "Du %s %d km/h. Hur långt kommer du på %d timmar?" % (mode, v, t),
                     "%d km" % (v * t), ["%d km" % x for x in (v + t, v * t + v, v // t if v % t == 0 else v - t)], "Sträcka = fart · tid = %d · %d = <b>%d km</b>." % (v, t, v * t))
        if k == 1:
            return M("Ett tåg kör %d km på %d timmar. Vilken är medelfarten?" % (v * t, t), "%d km/h" % v, ["%d km/h" % x for x in (v * t * t, v * t - t, v + t)],
                     "Fart = sträcka : tid = %d : %d = <b>%d km/h</b>." % (v * t, t, v))
        m = ch([30, 15, 45])
        dist = v * m // 60
        if v * m % 60:
            return None
        return M("En buss kör med farten %d km/h. Hur långt kommer den på %d minuter?" % (v, m), "%d km" % dist, ["%d km" % x for x in (v * m, v - dist if v != 2 * dist else v + 5, dist + 10)],
                 "%d minuter = %s timme. %d · %s = <b>%d km</b>." % (m, fr(m // 15, 4) if m != 30 else fr(1, 2), v, fr(m // 15, 4) if m != 30 else fr(1, 2), dist))

    if lv == 5:
        sets = [("Proportionella tabeller", [(tabell, 20)]), ("Recept", [(recept, 20)]), ("Jämförpris", [(jamforpris, 20)]),
                ("Fart, tid och sträcka", [(hastighet, 20)]), ("Blandat", [(tabell, 7), (recept, 7), (jamforpris, 6)])]
    else:
        sets = [("Proportionella tabeller", [(tabell, 20)]), ("Recept", [(recept, 20)]), ("Jämförpris", [(jamforpris, 20)]),
                ("Fart, tid och sträcka", [(hastighet, 20)]), ("Blandat", [(hastighet, 7), (recept, 7), (tabell, 6)])]
    return unit("proportionalitet", "F", "Proportionalitet: jämförpris, recept och fart", "Proportionalitet",
                "Proportionalitet och procent och deras samband. Proportionella samband vid enkla undersökningar, till exempel pris per kilo och fart.",
                "Arbetsblad om proportionalitet för årskurs %d: proportionella tabeller, recept, jämförpris och fart, tid och sträcka. 100 uppgifter med facit." % lv,
                "Räkna ut för en först", "Pris för 1 kg, mängd för 1 person, sträcka på 1 timme.", sets,
                ["Två storheter är proportionella när den ena blir dubbelt så stor om den andra blir dubbelt så stor, till exempel antal biljetter och pris.",
                 "Räkna gärna ut hur mycket det blir för en först: 3 kg kostar 54 kr, då kostar 1 kg 54 : 3 = 18 kr.",
                 "Fart, sträcka och tid hör ihop: sträcka = fart · tid. Kör du 60 km/h i 2 timmar kommer du 120 km."],
                [("3 kg kostar 54 kr. Vad kostar 5 kg?", ["1 kg: 54 : 3 = 18 kr", "5 · 18"], "90 kr"), ("Fart 80 km/h i 3 timmar", ["80 · 3"], "240 km")],
                [["Det största paketet är alltid billigast", "Jämför priset per kg"], ["Recept för 4 personer till 6: lägger till 2 dl", "Räkna per person och multiplicera"],
                 ["Fart = sträcka · tid", "Fart = sträcka : tid"]],
                [("Vad är jämförpris?", "Priset per kilo eller per liter. Det gör det lätt att jämföra förpackningar av olika storlek."),
                 ("Vad betyder km/h?", "Kilometer per timme, alltså hur många kilometer man kommer på en timme."),
                 ("Är alla samband proportionella?", "Nej. Din längd är inte proportionell mot din ålder.")])


UNITS = {"brak": brak, "decimaltal": decimaltal, "procent": procent, "ekvationer-och-uttryck": ekvationer,
         "monster-och-talfoljder": monster, "proportionalitet": proportionalitet}
