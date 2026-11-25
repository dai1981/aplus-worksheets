# -*- coding: utf-8 -*-
"""Sverige gymnasiet: Matematik nivå 4（Gy25）"""
import math
from fractions import Fraction as F
from se_g import nz, xp, pol, deriv, ev, integ, U, graf, ri, ch, sh, fq, d, par, sg, M, MN, rd, sup, num, MIN, coin, expr
from se_g3 import P_, fl, ps, frac_html, rpol, ekx

I_ = "<i>i</i>"


def cx(a, b):
    """a + bi"""
    a, b = F(a), F(b)
    if b == 0:
        return sg(a)
    bb = "" if abs(b) == 1 else (fq(abs(b)) if b.denominator != 1 else d(abs(b)))
    if a == 0:
        return (MIN if b < 0 else "") + bb + I_
    return "%s %s %s%s" % (sg(a), "−" if b < 0 else "+", bb, I_)


def pis(k):
    """k · π som text（k Fraction）"""
    k = F(k)
    if k == 0:
        return "0"
    s = MIN if k < 0 else ""
    k = abs(k)
    n, dd = k.numerator, k.denominator
    top = "π" if n == 1 else "%dπ" % n
    return s + (top if dd == 1 else "%s/%d" % (top, dd))


SPEC = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]
SQ = {0: "0", 30: "1/2", 45: "1/√2", 60: "√3/2", 90: "1"}


def sinv(v):
    r = v % 360
    s = 1
    if r > 180:
        r, s = r - 180, -1
    if r > 90:
        r = 180 - r
    t = SQ[r]
    return t if s > 0 or t == "0" else MIN + t


def cosv(v):
    return sinv(v + 90)


# ============================================================ komplexa tal, rektangulär form
def rekt():
    def add():
        a, b, c, e = nz(-9, 9), nz(-9, 9), nz(-9, 9), nz(-9, 9)
        k = coin()
        r = cx(a + c, b + e) if k else cx(a - c, b - e)
        return M("Beräkna (%s) %s (%s)." % (cx(a, b), "+" if k else "−", cx(c, e)), r, [cx(a + c, b - e) if k else cx(a - c, b + e), cx(a + e, b + c) if k else cx(a + c, b + e), cx(a * c, b * e)], "Räkna real- och imaginärdel var för sig: <b>%s</b>." % r)

    def mul():
        a, b, c, e = nz(-6, 6), nz(-6, 6), nz(-6, 6), nz(-6, 6)
        r = cx(a * c - b * e, a * e + b * c)
        return M("Beräkna (%s)(%s)." % (cx(a, b), cx(c, e)), r, [cx(a * c + b * e, a * e + b * c), cx(a * c, b * e), cx(a * c - b * e, a * e - b * c)], "Multiplicera ut och använd i² = −1: <b>%s</b>." % r)

    def div():
        c, e = nz(-5, 5), nz(-5, 5)
        x, y = nz(-5, 5), nz(-5, 5)
        # (a + bi) = (x + yi)(c + ei)
        a, b = x * c - y * e, x * e + y * c
        return M("Beräkna %s." % frac_html(cx(a, b), cx(c, e)), cx(x, y), [cx(y, x), cx(x, -y), cx(F(a, c), F(b, e))], "Förläng med konjugatet %s: <b>%s</b>." % (cx(c, -e), cx(x, y)))

    def abs_():
        a, b, r = ch([(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (1, 1, None), (2, 2, None), (1, 2, None), (2, 3, None)])
        sa, sb = ch([1, -1]), ch([1, -1])
        a, b = a * sa, b * sb
        k = ri(0, 2)
        if k == 0:
            if r is None:
                return M("Beräkna |%s|." % cx(a, b), "√%d" % (a * a + b * b), ["%d" % (a * a + b * b), "%d" % (abs(a) + abs(b)), "√%d" % abs(a * a - b * b) if a * a != b * b else "0"], "|z| = √(a² + b²) = <b>√%d</b>." % (a * a + b * b))
            return MN("Beräkna |%s|." % cx(a, b), r, [abs(a) + abs(b), r * r, abs(abs(a) - abs(b)) + r], "|z| = √(%d² + %d²) = <b>%d</b>." % (abs(a), abs(b), r))
        if k == 1:
            return M("Vilket är konjugatet till z = %s?" % cx(a, b), cx(a, -b), [cx(-a, b), cx(-a, -b), cx(b, a)], "Byt tecken på imaginärdelen: <b>%s</b>." % cx(a, -b))
        return M("Beräkna z · z̄ om z = %s." % cx(a, b), sg(a * a + b * b), [sg(a * a - b * b) if a * a != b * b else "1", cx(a * a - b * b, 2 * a * b), sg(2 * a * b) if 2 * a * b != a * a + b * b else "0"], "z · z̄ = a² + b² = <b>%s</b>." % sg(a * a + b * b))

    def potens():
        n = ri(2, 40)
        r = ["1", I_, MIN + "1", MIN + I_][n % 4]
        return M("Beräkna %s%s." % (I_, sup(n)), r, [x for x in ("1", I_, MIN + "1", MIN + I_) if x != r], "i⁴ = 1, och %d = 4 · %d + %d: i%s = <b>%s</b>." % (n, n // 4, n % 4, sup(n % 4), r))

    def ekv():
        p = nz(-8, 8) * 2
        q = ri(1, 12) ** 2 + (p // 2) ** 2
        a, b = -p // 2, math.isqrt(q - (p // 2) ** 2)
        return M("Lös ekvationen %s = 0." % pol({2: 1, 1: p, 0: q}), "x = %s" % cx(a, b).replace(" + ", " ± ").replace(" − ", " ± ") if a else "x = ±%s%s" % ("" if b == 1 else b, I_),
                 ["x = %s ± %d" % (sg(a), b) if a else "x = ±%d" % b, "x = %s" % cx(-a, b).replace(" + ", " ± ").replace(" − ", " ± ") if a else "x = ±%d%s" % (b * b, I_), "x = %s ± %d%s" % (sg(a), b * b, I_) if a else "x = %d%s" % (b, I_)],
                 "pq-formeln: x = %s ± √(%d − %d) = %s ± √(−%d) = %s ± %s%s." % (sg(a), (p // 2) ** 2, q, sg(a), b * b, sg(a), "" if b == 1 else b, I_))

    sets = [("Addition och subtraktion", [(add, 20)]), ("Multiplikation", [(mul, 14), (potens, 6)]), ("Division", [(div, 20)]), ("Belopp och konjugat", [(abs_, 20)]), ("Andragradsekvationer", [(ekv, 20)])]
    return U("komplexa-tal-i-rektangular-form", "KT", "Komplexa tal i rektangulär form", "Komplexa tal",
             "Komplexa tal i rektangulär form: räknesätten, belopp och konjugat samt lösning av andragradsekvationer.",
             "Uppgifter om komplexa tal i rektangulär form för Matematik 4: addition, multiplikation, division, belopp och konjugat samt andragradsekvationer. 100 uppgifter med facit.",
             "i² = −1", "z = a + bi har realdel a och imaginärdel b.", sets,
             ["Den imaginära enheten i uppfyller i² = −1. Ett komplext tal skrivs z = a + bi.",
              "Addera och multiplicera som med vanliga uttryck och ersätt i² med −1. Vid division förlänger du med nämnarens konjugat.",
              "Konjugatet till a + bi är a − bi. Beloppet är |z| = √(a² + b²)."],
             [("(2 + 3i)(1 − i)", ["2 − 2i + 3i − 3i²", "2 + i + 3"], "5 + i"), ("x² + 4 = 0", ["x² = −4"], "x = ±2i")],
             [["i² = 1", "i² = −1"], ["Konjugatet byter tecken på realdelen", "Det byter tecken på imaginärdelen"], ["|3 + 4i| = 7", "|3 + 4i| = 5"]],
             [("Varför behövs komplexa tal?", "För att alla andragradsekvationer ska ha lösningar."), ("Vad är det komplexa talplanet?", "Ett plan där realdelen är x och imaginärdelen y."), ("Är reella tal komplexa?", "Ja, med imaginärdelen 0.")])


# ============================================================ komplexa tal, polär form
def polar():
    VV = [(1, 1, "√2", 45), (1, -1, "√2", 315), (-1, 1, "√2", 135), (-1, -1, "√2", 225), (0, 1, "1", 90), (0, -1, "1", 270), (1, 0, "1", 0), (-1, 0, "1", 180)]

    def arg():
        a, b, r, v = ch(VV)
        k = ri(1, 6)
        return M("Bestäm argumentet för z = %s (0° ≤ arg z &lt; 360°)." % cx(a * k, b * k), "%d°" % v, ["%d°" % ((v + 90) % 360), "%d°" % ((v + 180) % 360), "%d°" % ((360 - v) % 360 if v not in (0, 180) else (v + 270) % 360)], "Punkten (%s, %s) ligger %s: <b>%d°</b>." % (sg(a * k), sg(b * k), "på en axel" if a * b == 0 else "i %s kvadranten" % ["första", "andra", "tredje", "fjärde"][v // 90], v))

    def tilpolar():
        a, b, r, v = ch(VV)
        k = ri(1, 9)
        R = ("%d√2" % k if k > 1 else "√2") if r == "√2" else str(k)
        res = "%s(cos %d° + %s sin %d°)" % (R, v, I_, v)
        return M("Skriv z = %s i polär form." % cx(a * k, b * k), res, ["%s(cos %d° + %s sin %d°)" % (R, (v + 90) % 360, I_, (v + 90) % 360), "%s(cos %d° + %s sin %d°)" % (str(2 * k) if r == "√2" else "%d√2" % k, v, I_, v), "%s(sin %d° + %s cos %d°)" % (R, v, I_, v)],
                   "|z| = %s och arg z = %d°: <b>%s</b>." % (R, v, res))

    def tillrekt():
        r = 2 * ri(1, 4)
        v = ch([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330])
        c = {0: (1, 0), 30: ("√3/2", "1/2"), 60: ("1/2", "√3/2"), 90: (0, 1)}
        cs, sn = cosv(v), sinv(v)
        def mul_(t):
            if t == "0":
                return "0"
            neg = t.startswith(MIN)
            t = t.lstrip(MIN)
            if t == "1":
                v_ = str(r)
            elif t == "1/2":
                v_ = d(F(r, 2))
            elif t == "√3/2":
                v_ = ("%s√3" % d(F(r, 2))) if r != 2 else "√3"
            else:
                v_ = t
            return (MIN if neg else "") + v_
        re_, im_ = mul_(cs), mul_(sn)
        def comb(x, y):
            if y == "0":
                return x
            yy = y.lstrip(MIN)
            if x == "0":
                return (MIN if y.startswith(MIN) else "") + ("" if yy == "1" else yy) + I_
            return "%s %s %s%s" % (x, "−" if y.startswith(MIN) else "+", "" if yy == "1" else yy, I_)
        res = comb(re_, im_)
        return M("Skriv z = %d(cos %d° + %s sin %d°) i formen a + bi." % (r, v, I_, v), res, [comb(im_, re_), comb(re_, (im_[1:] if im_.startswith(MIN) else MIN + im_) if im_ != "0" else str(r)), comb(str(r), str(r)) if res != comb(str(r), str(r)) else comb(re_, "1")],
                 "a = %d cos %d° = %s och b = %d sin %d° = %s: <b>%s</b>." % (r, v, re_, r, v, im_, res))

    def mulp():
        r1, r2 = ri(1, 9), ri(1, 9)
        v1, v2 = ri(1, 17) * 10, ri(1, 17) * 10
        res = "%d(cos %d° + %s sin %d°)" % (r1 * r2, (v1 + v2) % 360, I_, (v1 + v2) % 360)
        k = coin()
        if k:
            return M("Beräkna z₁z₂ om z₁ = %d(cos %d° + %s sin %d°) och z₂ = %d(cos %d° + %s sin %d°)." % (r1, v1, I_, v1, r2, v2, I_, v2), res,
                     ["%d(cos %d° + %s sin %d°)" % (r1 + r2, (v1 + v2) % 360, I_, (v1 + v2) % 360), "%d(cos %d° + %s sin %d°)" % (r1 * r2, v1 * v2 % 360, I_, v1 * v2 % 360), "%d(cos %d° + %s sin %d°)" % (r1 * r2, abs(v1 - v2), I_, abs(v1 - v2)) if v1 != v2 else "%d(cos 0° + %s sin 0°)" % (r1 * r2, I_)],
                     "Multiplicera beloppen och addera argumenten: <b>%s</b>." % res)
        n = ri(2, 6)
        v = ri(1, 9) * 10
        res = "%s(cos %d° + %s sin %d°)" % (num(r1 ** n), n * v % 360, I_, n * v % 360)
        return M("Beräkna z%s om z = %d(cos %d° + %s sin %d°)." % (sup(n), r1, v, I_, v), res, ["%s(cos %d° + %s sin %d°)" % (num(r1 * n), n * v % 360, I_, n * v % 360), "%s(cos %d° + %s sin %d°)" % (num(r1 ** n), v, I_, v), "%s(cos %d° + %s sin %d°)" % (num(r1 ** n), (v + n) % 360, I_, (v + n) % 360)],
                 "de Moivres formel: beloppet upphöjs till %d och argumentet multipliceras med %d: <b>%s</b>." % (n, n, res))

    def divp():
        r2 = ri(1, 6)
        r1 = r2 * ri(1, 6)
        v1, v2 = ri(10, 35) * 10, ri(1, 9) * 10
        res = "%d(cos %d° + %s sin %d°)" % (r1 // r2, (v1 - v2) % 360, I_, (v1 - v2) % 360)
        return M("Beräkna z₁/z₂ om z₁ = %d(cos %d° + %s sin %d°) och z₂ = %d(cos %d° + %s sin %d°)." % (r1, v1, I_, v1, r2, v2, I_, v2), res,
                 ["%d(cos %d° + %s sin %d°)" % (r1 * r2, (v1 - v2) % 360, I_, (v1 - v2) % 360), "%d(cos %d° + %s sin %d°)" % (r1 // r2, (v1 + v2) % 360, I_, (v1 + v2) % 360), "%d(cos %d° + %s sin %d°)" % (r1 - r2 if r1 != 2 * r2 else r1 + r2, (v1 - v2) % 360, I_, (v1 - v2) % 360)],
                 "Dividera beloppen och subtrahera argumenten: <b>%s</b>." % res)

    sets = [("Argument", [(arg, 20)]), ("Till polär form", [(tilpolar, 20)]), ("Till rektangulär form", [(tillrekt, 20)]), ("Multiplikation och de Moivre", [(mulp, 20)]), ("Division i polär form", [(divp, 20)])]
    return U("komplexa-tal-i-polar-form", "KT", "Komplexa tal i polär form och de Moivres formel", "Komplexa tal i polär form",
             "Komplexa tal i polär form, det komplexa talplanet och räkneregler för multiplikation och division i polär form.",
             "Uppgifter om komplexa tal i polär form för Matematik 4: argument, polär och rektangulär form, multiplikation, de Moivres formel och division. 100 uppgifter med facit.",
             "z = r(cos v + i sin v)", "Vid multiplikation adderas argumenten.", sets,
             ["I det komplexa talplanet motsvaras z = a + bi av punkten (a, b). Beloppet r = |z| är avståndet till origo och argumentet v är vinkeln mot positiva realaxeln.",
              "Polär form: z = r(cos v + i sin v), där a = r cos v och b = r sin v.",
              "Vid multiplikation multipliceras beloppen och argumenten adderas. de Moivres formel: zⁿ = rⁿ(cos nv + i sin nv)."],
             [("z = 1 + i", ["r = √2", "v = 45°"], "√2(cos 45° + i sin 45°)")],
             [["Fel kvadrant för argumentet", "Rita punkten först"], ["Multiplicerar argumenten", "Argumenten adderas"], ["Adderar beloppen", "Beloppen multipliceras"]],
             [("Varför polär form?", "Multiplikation och potenser blir mycket enklare."), ("Kan argumentet anges i radianer?", "Ja, 45° = π/4."), ("Vad är argumentet till ett negativt reellt tal?", "180°.")])


# ============================================================ polynomekvationer
def faktor():
    def rest():
        cs = rpol(3, -5, 5)
        a = nz(-3, 3)
        r = ev(cs, a)
        return MN("Bestäm resten när p(x) = %s divideras med (x %s %d)." % (ps(cs), "−" if a > 0 else "+", abs(a)), r, [ev(cs, -a), r + 1, cs.get(0, 0) if cs.get(0, 0) != r else r - 1], "Restsatsen: resten är p(%s) = <b>%s</b>." % (sg(a), sg(r)))

    def faktorn():
        rs = sorted(set(nz(-5, 5) for _ in range(3)))
        if len(rs) < 3:
            return None
        cs = {3: 1, 2: -sum(rs), 1: rs[0] * rs[1] + rs[0] * rs[2] + rs[1] * rs[2], 0: -rs[0] * rs[1] * rs[2]}
        a = ch(rs)
        wr = [x for x in range(-6, 7) if x not in rs and x]
        b = ch(wr)
        return M("Vilken av faktorerna är en faktor i p(x) = %s?" % ps(cs), "(x %s %d)" % ("−" if a > 0 else "+", abs(a)), ["(x %s %d)" % ("+" if a > 0 else "−", abs(a)) if -a not in rs else "(x %s %d)" % ("−" if b > 0 else "+", abs(b)), "(x %s %d)" % ("−" if b > 0 else "+", abs(b)), "(x %s %d)" % ("−" if a * 2 > 0 else "+", abs(2 * a)) if 2 * a not in rs else "(x %s %d)" % ("+" if b > 0 else "−", abs(b))],
                 "Faktorsatsen: (x − a) är en faktor om p(a) = 0. p(%s) = 0: <b>(x %s %d)</b>." % (sg(a), "−" if a > 0 else "+", abs(a)))

    def los():
        r1 = nz(-4, 4)
        r2, r3 = nz(-5, 5), nz(-5, 5)
        if len({r1, r2, r3}) < 3:
            return None
        rs = sorted([r1, r2, r3])
        cs = {3: 1, 2: -sum(rs), 1: rs[0] * rs[1] + rs[0] * rs[2] + rs[1] * rs[2], 0: -rs[0] * rs[1] * rs[2]}
        res = "x = " + ", ".join(sg(x) for x in rs)
        return M("Ekvationen %s = 0 har roten x = %s. Lös ekvationen." % (ps(cs), sg(r1)), res, ["x = " + ", ".join(sg(-x) for x in reversed(rs)), "x = %s" % sg(r1), "x = " + ", ".join(sg(x) for x in sorted([r1, -r2, -r3]))],
                 "Dividera med (x %s %d) och lös andragradsekvationen: <b>%s</b>." % ("−" if r1 > 0 else "+", abs(r1), res))

    def komplex():
        a = nz(-4, 4)
        b = ri(1, 5)
        r = nz(-4, 4)
        # (x − r)(x² − 2a x + a² + b²)
        q2 = {2: 1, 1: -2 * a, 0: a * a + b * b}
        cs = {3: 1, 2: q2[1] - r, 1: q2[0] - r * q2[1], 0: -r * q2[0]}
        res = "x = %s, x = %s" % (sg(r), cx(a, b).replace(" + ", " ± "))
        return M("Lös ekvationen %s = 0 om x = %s är en rot." % (ps(cs), sg(r)), res, ["x = %s, x = %s" % (sg(-r), cx(a, b).replace(" + ", " ± ")), "x = %s, x = %s" % (sg(r), cx(-a, b).replace(" + ", " ± ").replace(" − ", " ± ")), "x = %s, x = %s ± %d" % (sg(r), sg(a), b)],
                 "Dividera med (x %s %d): %s = 0 ger <b>%s</b>." % ("−" if r > 0 else "+", abs(r), ps(q2), res))

    def konj():
        a, b = nz(-6, 6), nz(-6, 6)
        return M("Ett polynom med reella koefficienter har roten %s. Vilken är då också en rot?" % cx(a, b), cx(a, -b), [cx(-a, b), cx(-a, -b), cx(b, a)], "Icke-reella rötter kommer i konjugerade par: <b>%s</b>." % cx(a, -b))

    sets = [("Restsatsen", [(rest, 20)]), ("Faktorsatsen", [(faktorn, 20)]), ("Lös med en känd rot", [(los, 20)]), ("Komplexa rötter", [(komplex, 20)]), ("Konjugerade rötter", [(konj, 8), (rest, 6), (faktorn, 6)])]
    return U("polynomekvationer-och-faktorsatsen", "KT", "Polynomekvationer: faktorsatsen och komplexa rötter", "Polynomekvationer",
             "Algebraiska metoder för att lösa polynomekvationer: faktorsatsen, polynomdivision och komplexa rötter.",
             "Uppgifter om polynomekvationer för Matematik 4: restsatsen, faktorsatsen, lösning med en känd rot, komplexa rötter och konjugerade rötter. 100 uppgifter med facit.",
             "p(a) = 0 ⇔ (x − a) är en faktor", "Icke-reella rötter kommer parvis.", sets,
             ["Restsatsen: när p(x) divideras med (x − a) är resten p(a).",
              "Faktorsatsen: (x − a) är en faktor i p(x) om och endast om p(a) = 0.",
              "Känner du en rot kan du dividera bort faktorn och lösa den andragradsekvation som blir kvar. Har polynomet reella koefficienter kommer icke-reella rötter i konjugerade par."],
             [("x³ − 6x² + 11x − 6 = 0, x = 1", ["(x − 1)(x² − 5x + 6)"], "x = 1, 2, 3")],
             [["Rot 2 ger faktorn (x + 2)", "Faktorn är (x − 2)"], ["Glömmer den kända roten i svaret", "Ta med alla rötter"], ["Glömmer konjugatroten", "a + bi ger också a − bi"]],
             [("Hur många rötter har en tredjegradsekvation?", "Tre, räknade med multiplicitet, varav minst en reell."), ("Hur hittar jag en rot?", "Pröva delare till konstanttermen eller använd grafen."), ("Vad är polynomdivision?", "Division av polynom på samma sätt som liggande stolen.")])


# ============================================================ enhetscirkeln och radianer
def radianer():
    def tillrad():
        v = ch([30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360, 15, 720, 540, 36, 18, 20, 40, 72])
        r = F(v, 180)
        return M("Skriv %d° i radianer." % v, pis(r), [pis(F(180, v)) if v != 180 else "2π", pis(r * 2), pis(r / 2)], "Multiplicera med π/180: %d · π/180 = <b>%s</b>." % (v, pis(r)))

    def tillgrad():
        r = ch([F(1, 6), F(1, 4), F(1, 3), F(1, 2), F(2, 3), F(3, 4), F(5, 6), F(1), F(7, 6), F(5, 4), F(4, 3), F(3, 2), F(5, 3), F(7, 4), F(11, 6), F(2), F(1, 12), F(1, 5), F(1, 9), F(5, 12), F(7, 12), F(2, 5), F(3, 5), F(1, 10), F(1, 18), F(5, 2), F(3)])
        v = r * 180
        return MN("Skriv %s i grader." % pis(r), v, [r * 360, r * 90, v + 180 if v < 180 else v - 90], "Multiplicera med 180/π: <b>%s°</b>." % d(v), "°")

    def varde():
        v = ch(SPEC)
        f = ch(["sin", "cos"])
        res = sinv(v) if f == "sin" else cosv(v)
        allv = sorted(set([sinv(x) for x in SPEC] + [cosv(x) for x in SPEC]))
        w = sh([x for x in allv if x != res])
        oth = cosv(v) if f == "sin" else sinv(v)
        ws = [oth] if oth != res else []
        neg = (res[1:] if res.startswith(MIN) else MIN + res) if res != "0" else "1"
        ws += [neg] + w
        return M("Bestäm det exakta värdet av %s %s." % (f, pis(F(v, 180))), res, ws, "Vinkeln %s = %d°. Läs av i enhetscirkeln: <b>%s</b>." % (pis(F(v, 180)), v, res))

    def bage():
        r = ri(2, 20)
        v = ch([F(1, 6), F(1, 4), F(1, 3), F(1, 2), F(2, 3), F(1), F(3, 2), F(1, 5), F(5, 6), F(3, 4)])
        k = coin()
        if k:
            return M("En cirkel har radien %d cm. Hur lång är cirkelbågen till medelpunktsvinkeln %s?" % (r, pis(v)), "%s cm" % pis(v * r), ["%s cm" % pis(v * r * r), "%s cm" % pis(v * r / 2), "%s cm" % pis(v * 2 * r)], "Bågen b = rv = %d · %s = <b>%s cm</b>." % (r, pis(v), pis(v * r)))
        return M("En cirkelsektor har radien %d cm och vinkeln %s. Vilken är arean?" % (r, pis(v)), "%s cm²" % pis(v * r * r / 2), ["%s cm²" % pis(v * r * r), "%s cm²" % pis(v * r / 2), "%s cm²" % pis(v * r)], "A = r²v/2 = %d² · %s / 2 = <b>%s cm²</b>." % (r, pis(v), pis(v * r * r / 2)))

    def kvadrant():
        v = ri(1, 35) * 10 + 5
        q = v // 90 + 1
        sgn_s = "positivt" if q in (1, 2) else "negativt"
        sgn_c = "positivt" if q in (1, 4) else "negativt"
        f = ch(["sin", "cos"])
        r = sgn_s if f == "sin" else sgn_c
        return M("Är %s %d° positivt eller negativt?" % (f, v), cap_(r), ["Negativt" if r == "positivt" else "Positivt", "Noll", "Det beror på radien"], "%d° ligger i kvadrant %d. %s är %s där: <b>%s</b>." % (v, q, f, r, r))

    sets = [("Grader till radianer", [(tillrad, 20)]), ("Radianer till grader", [(tillgrad, 20)]), ("Exakta värden", [(varde, 20)]), ("Båge och sektor", [(bage, 20)]), ("Tecken i kvadranterna", [(kvadrant, 20)])]
    return U("enhetscirkeln-och-radianer", "TR", "Enhetscirkeln och radianer: exakta värden och bågar", "Enhetscirkeln och radianer",
             "Begreppet radian och trigonometriska värden i enhetscirkeln. Exakta värden för standardvinklar.",
             "Uppgifter om enhetscirkeln och radianer för Matematik 4: grader och radianer, exakta värden, båglängd och sektorarea samt tecken i kvadranterna. 100 uppgifter med facit.",
             "180° = π radianer", "Punkten på enhetscirkeln är (cos v, sin v).", sets,
             ["En radian är den vinkel som ger en båge lika lång som radien. Ett halvt varv är π radianer.",
              "I enhetscirkeln är punkten för vinkeln v (cos v, sin v). Exakta värden: sin 30° = 1/2, sin 45° = 1/√2, sin 60° = √3/2.",
              "Med radianer blir båglängden b = rv och sektorns area A = r²v/2."],
             [("sin(5π/6)", ["5π/6 = 150°", "sin 150° = sin 30°"], "1/2")],
             [["Räknaren i fel läge", "Kontrollera grader/radianer"], ["cos 60° = √3/2", "cos 60° = 1/2"], ["Fel tecken i andra kvadranten", "cos är negativ där"]],
             [("Varför radianer?", "De ger enklare formler för bågar och för derivator av trigonometriska funktioner."), ("Hur många radianer är ett varv?", "2π ≈ 6,28."), ("Vad betyder 1 radian i grader?", "Ungefär 57,3°.")])


def MF(q, a, w, e):
    return M(q, fq(a), [fq(x) for x in w], e)


def cap_(s):
    return s[0].upper() + s[1:]


# ============================================================ trigonometriska formler
def formler():
    def ettan():
        P = [(F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)), (F(8, 17), F(15, 17)), (F(7, 25), F(24, 25)), (F(4, 5), F(3, 5)), (F(12, 13), F(5, 13)), (F(20, 29), F(21, 29)), (F(9, 41), F(40, 41)), (F(11, 61), F(60, 61)), (F(60, 61), F(11, 61)), (F(28, 53), F(45, 53)), (F(45, 53), F(28, 53)), (F(33, 65), F(56, 65)), (F(16, 65), F(63, 65)), (F(21, 29), F(20, 29))]
        s, c = ch(P)
        k = ri(0, 3)
        if k == 3:
            return MF("v är en spetsig vinkel och cos v = %s. Bestäm sin v." % fq(c), s, [1 - c, c, 1 / c], "sin v = √(1 − cos²v) = <b>%s</b>." % fq(s))
        if k == 0:
            return MF("v är en spetsig vinkel och sin v = %s. Bestäm cos v." % fq(s), c, [1 - s, s, 1 / s], "Trigonometriska ettan: cos v = √(1 − sin²v) = <b>%s</b>." % fq(c))
        if k == 1:
            return MF("v är en trubbig vinkel och sin v = %s. Bestäm cos v." % fq(s), -c, [c, 1 - s, -s], "cos v är negativ för trubbiga vinklar: <b>%s</b>." % fq(-c))
        return MF("v är en spetsig vinkel och sin v = %s. Bestäm tan v." % fq(s), s / c, [c / s, s, c], "cos v = %s. tan v = sin v / cos v = <b>%s</b>." % (fq(c), fq(s / c)))

    def dubbel():
        P = [(F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)), (F(8, 17), F(15, 17)), (F(4, 5), F(3, 5)), (F(12, 13), F(5, 13)), (F(7, 25), F(24, 25)), (F(15, 17), F(8, 17)), (F(24, 25), F(7, 25)), (F(11, 61), F(60, 61)), (F(60, 61), F(11, 61)), (F(28, 53), F(45, 53)), (F(45, 53), F(28, 53)), (F(33, 65), F(56, 65)), (F(16, 65), F(63, 65)), (F(21, 29), F(20, 29))]
        s, c = ch(P)
        k = ri(0, 2)
        if k == 0:
            return MF("sin v = %s och cos v = %s. Beräkna sin 2v." % (fq(s), fq(c)), 2 * s * c, [2 * s, s * c, c * c - s * s], "sin 2v = 2 sin v cos v = <b>%s</b>." % fq(2 * s * c))
        if k == 1:
            return MF("sin v = %s och cos v = %s. Beräkna cos 2v." % (fq(s), fq(c)), c * c - s * s, [2 * c, 2 * s * c, c * c + s * s], "cos 2v = cos²v − sin²v = <b>%s</b>." % fq(c * c - s * s))
        return MF("cos v = %s. Beräkna cos 2v." % fq(c), 2 * c * c - 1, [2 * c, c * c, 1 - 2 * c * c], "cos 2v = 2cos²v − 1 = <b>%s</b>." % fq(2 * c * c - 1))

    def addit():
        P = [(45, 30), (60, 45), (90, 30), (180, 60), (90, 45), (30, 45), (30, 60), (60, 30), (120, 45), (135, 30), (150, 45), (210, 45), (90, 60), (180, 45), (270, 30), (240, 45), (2 * ri(10, 40), ri(10, 40))]
        a, b = ch(P)
        f = ch(["sin", "cos"])
        op = ch(["+", "−"])
        if op == "+":
            res = "sin %d° cos %d° + cos %d° sin %d°" % (a, b, a, b) if f == "sin" else "cos %d° cos %d° − sin %d° sin %d°" % (a, b, a, b)
            w = ["sin %d° cos %d° − cos %d° sin %d°" % (a, b, a, b) if f == "sin" else "cos %d° cos %d° + sin %d° sin %d°" % (a, b, a, b), "%s %d° + %s %d°" % (f, a, f, b), "sin %d° sin %d° + cos %d° cos %d°" % (a, b, a, b) if f == "sin" else "sin %d° cos %d° + cos %d° sin %d°" % (a, b, a, b)]
        else:
            res = "sin %d° cos %d° − cos %d° sin %d°" % (a, b, a, b) if f == "sin" else "cos %d° cos %d° + sin %d° sin %d°" % (a, b, a, b)
            w = ["sin %d° cos %d° + cos %d° sin %d°" % (a, b, a, b) if f == "sin" else "cos %d° cos %d° − sin %d° sin %d°" % (a, b, a, b), "%s %d° − %s %d°" % (f, a, f, b), "cos %d° sin %d° − sin %d° cos %d°" % (a, b, a, b)]
        return M("Skriv %s(%d° %s %d°) med additionsformeln." % (f, a, op, b), res, w, "<b>%s</b>." % res)

    def forenkla():
        P = [("sin²x + cos²x", "1", ["0", "2", "sin 2x"]), ("2 sin x cos x", "sin 2x", ["sin x²", "2 sin 2x", "cos 2x"]), ("cos²x − sin²x", "cos 2x", ["1", "sin 2x", "−1"]),
             ("1 − sin²x", "cos²x", ["cos x", "sin²x", "1 − sin x"]), ("1 − 2sin²x", "cos 2x", ["sin 2x", "cos²x", "1"]), ("sin x / cos x", "tan x", ["1", "cot x", "sin²x"]),
             ("2cos²x − 1", "cos 2x", ["cos²x", "1", "sin 2x"]), ("(sin x + cos x)²", "1 + sin 2x", ["1", "1 + cos 2x", "sin²x + cos²x"]), ("sin(180° − x)", "sin x", ["−sin x", "cos x", "−cos x"]),
             ("cos(180° − x)", "−cos x", ["cos x", "sin x", "−sin x"]), ("sin(90° − x)", "cos x", ["sin x", "−cos x", "tan x"]), ("cos(−x)", "cos x", ["−cos x", "sin x", "−sin x"]), ("sin(−x)", "−sin x", ["sin x", "cos x", "−cos x"])]
        q, r, w = ch(P)
        return M("Förenkla %s." % q, r, w, "<b>%s</b>." % r)

    sets = [("Trigonometriska ettan", [(ettan, 20)]), ("Formler för dubbla vinkeln", [(dubbel, 20)]), ("Additionsformlerna", [(addit, 20)]), ("Förenkla", [(forenkla, 12), (ettan, 8)]), ("Blandat", [(dubbel, 10), (forenkla, 1), (addit, 9)])]
    return U("trigonometriska-formler", "TR", "Trigonometriska formler: ettan, additions- och dubbla vinkeln", "Trigonometriska formler",
             "Härledning och användning av trigonometriska formler: trigonometriska ettan, additions- och subtraktionsformler och formler för dubbla vinkeln.",
             "Uppgifter om trigonometriska formler för Matematik 4: trigonometriska ettan, dubbla vinkeln, additionsformlerna och förenkling. 100 uppgifter med facit.",
             "sin²v + cos²v = 1", "sin 2v = 2 sin v cos v", sets,
             ["Trigonometriska ettan: sin²v + cos²v = 1. Den ger cos v om du känner sin v (tänk på tecknet).",
              "Additionsformlerna: sin(u + v) = sin u cos v + cos u sin v och cos(u + v) = cos u cos v − sin u sin v.",
              "Dubbla vinkeln: sin 2v = 2 sin v cos v och cos 2v = cos²v − sin²v = 2cos²v − 1 = 1 − 2sin²v."],
             [("sin v = 3/5, v spetsig", ["cos v = 4/5", "sin 2v = 2 · 3/5 · 4/5"], "24/25")],
             [["sin(u + v) = sin u + sin v", "Använd additionsformeln"], ["Glömmer tecknet för trubbig vinkel", "cos är negativ i andra kvadranten"], ["sin 2v = 2 sin v", "sin 2v = 2 sin v cos v"]],
             [("Varför kallas den ettan?", "För att sin²v + cos²v alltid blir 1."), ("Måste jag kunna formlerna utantill?", "De finns i formelbladet, men du ska kunna använda dem."), ("Var används formlerna?", "Vid förenkling, ekvationslösning och derivering.")])


# ============================================================ trigonometriska ekvationer

def eqtext(f, key, neg, var="v"):
    """likvärdig ekvation f(var) = ±key skriven på flera sätt"""
    m = ri(1, 5)
    c = ri(1, 9)
    sgn = MIN if neg else ""
    rhs = {"1/2": (2 * m, "%d" % m), "√3/2": (2 * m, "%s√3" % ("" if m == 1 else m)), "1/√2": (2 * m, "%s√2" % ("" if m == 1 else m))}[key]
    k = ri(0, 2)
    lhs = "%s %s" % (f, var)
    if k == 0 or m == 1 and k == 1:
        return "%s %s = %s%s" % ("" if rhs[0] == 1 else rhs[0], lhs, sgn, rhs[1]) if not (m == 1 and k == 0 and coin()) else "%s = %s%s" % (lhs, sgn, key)
    if k == 1:
        return "%d %s %s %s = 0" % (rhs[0], lhs, "+" if neg else "−", rhs[1])
    if key == "1/2":
        return "%d %s + %d = %s" % (rhs[0], lhs, c, sg(c - m if neg else c + m))
    return "%d %s + %d = %d %s %s" % (rhs[0], lhs, c, c, "−" if neg else "+", rhs[1])

def ekvationer():
    BASE = {"1/2": (30, 150), "1/√2": (45, 135), "√3/2": (60, 120), "1": (90, 90), "0": (0, 180)}

    def sinekv():
        t, (a, b) = ch([(k, v) for k, v in BASE.items() if k not in ("1", "0")])
        neg = coin()
        if neg:
            a, b = 180 + a, 360 - a
            t = MIN + t
        res = "v = %d° + n · 360° eller v = %d° + n · 360°" % (a, b)
        return M("Lös ekvationen %s." % eqtext("sin", t.lstrip(MIN), neg), res, ["v = %d° + n · 360°" % a, "v = %d° + n · 360° eller v = %d° + n · 360°" % (a, (180 + a) % 360), "v = ±%d° + n · 360°" % a], "Två lösningar per varv: v och 180° − v. <b>%s</b>." % res)

    def cosekv():
        t, (a, _) = ch([(k, v) for k, v in BASE.items() if k not in ("1", "0")])
        neg = coin()
        if neg:
            a = 180 - a
            t = MIN + t
        res = "v = ±%d° + n · 360°" % a
        return M("Lös ekvationen %s." % eqtext("cos", t.lstrip(MIN), neg), res, ["v = %d° + n · 360°" % a, "v = %d° + n · 360° eller v = %d° + n · 360°" % (a, 180 - a), "v = ±%d° + n · 180°" % a], "cos är symmetrisk kring x-axeln: <b>%s</b>." % res)

    def intervall():
        t, (a, b) = ch([(k, v) for k, v in BASE.items() if k not in ("1", "0")])
        f = ch(["sin", "cos"])
        if f == "sin":
            sol = [a, b]
        else:
            sol = [a, 360 - a]
        res = "v = %d° och v = %d°" % tuple(sorted(sol))
        return M("Lös %s för 0° ≤ v &lt; 360°." % eqtext(f, t, False), res, ["v = %d°" % a, "v = %d° och v = %d°" % tuple(sorted([a, 180 + a])), "v = %d° och v = %d°" % tuple(sorted([a, b if f == "cos" else 360 - a]))], "<b>%s</b>." % res)

    def kx():
        k = ri(2, 4)
        a = ch([30, 45, 60])
        t = {30: "1/2", 45: "1/√2", 60: "√3/2"}[a]
        res = "x = %s° + n · %s° eller x = %s° + n · %s°" % (d(F(a, k)), d(F(360, k)), d(F(180 - a, k)), d(F(360, k)))
        return M("Lös ekvationen %s." % eqtext("sin", t, False, "%dx" % k), res, ["x = %s° + n · 360° eller x = %s° + n · 360°" % (d(F(a, k)), d(F(180 - a, k))), "x = %d° + n · %s° eller x = %d° + n · %s°" % (a * k, d(F(360, k)), (180 - a) * k, d(F(360, k))), "x = %s° + n · %s°" % (d(F(a, k)), d(F(360, k)))],
                 "%dx = %d° + n · 360° eller %dx = %d° + n · 360°. Dela med %d: <b>%s</b>." % (k, a, k, 180 - a, k, res))

    def rak():
        s = F(ri(1, 99), 100) * ch([1, -1])
        v = math.degrees(math.asin(float(s)))
        a = fl(v, 1)
        b = fl(180 - v, 1)
        res = "v ≈ %s° + n · 360° eller v ≈ %s° + n · 360°" % (a, b)
        return M("Lös ekvationen sin v = %s. Avrunda till en decimal." % d(s), res, ["v ≈ %s° + n · 360°" % a, "v ≈ ±%s° + n · 360°" % fl(abs(v), 1), "v ≈ %s° + n · 360° eller v ≈ %s° + n · 360°" % (a, fl(180 + v, 1))], "sin⁻¹(%s) ≈ %s°. Den andra lösningen är 180° − v: <b>%s</b>." % (d(s), a, res))

    sets = [("sin v = a", [(sinekv, 20)]), ("cos v = a", [(cosekv, 20)]), ("Lösningar i ett intervall", [(intervall, 20)]), ("sin kx = a", [(kx, 20)]), ("Med räknare", [(rak, 20)])]
    return U("trigonometriska-ekvationer", "TR", "Trigonometriska ekvationer: alla lösningar", "Trigonometriska ekvationer",
             "Lösning av trigonometriska ekvationer, både exakt och med digitala verktyg, och tolkning av lösningarna.",
             "Uppgifter om trigonometriska ekvationer för Matematik 4: sin v = a, cos v = a, lösningar i ett intervall, sin kx = a och lösningar med räknare. 100 uppgifter med facit.",
             "sin v = a: v och 180° − v", "cos v = a: ±v. Lägg till n · 360°.", sets,
             ["sin v = a har lösningarna v₁ och 180° − v₁, plus hela varv: v = v₁ + n · 360°.",
              "cos v = a har lösningarna v = ±v₁ + n · 360°.",
              "För sin kx = a: lös först för kx och dela sedan alla termer med k, även perioden."],
             [("sin v = 1/2", ["v₁ = 30°", "180° − 30° = 150°"], "v = 30° + n · 360° eller 150° + n · 360°")],
             [["Glömmer den andra lösningen", "Rita enhetscirkeln"], ["Glömmer att dela perioden med k", "sin 2x ger perioden 180°"], ["Glömmer n · 360°", "Ange alla lösningar"]],
             [("Vad betyder n?", "Ett godtyckligt heltal."), ("Hur många lösningar har sin v = 2?", "Inga, sin v ligger mellan −1 och 1."), ("Kan jag lösa i radianer?", "Ja, då lägger du till n · 2π.")])


# ============================================================ trigonometriska grafer
def grafer():
    def amp():
        A, k, c = ri(1, 6), ri(1, 4), ri(-4, 4)
        f = ch(["sin", "cos"])
        q = "y = %s%s %s%s" % ("" if A == 1 else "%d " % A, f, "" if k == 1 else "%d" % k, "x") + ("" if c == 0 else " %s %d" % ("+" if c > 0 else "−", abs(c)))
        t = ri(0, 2)
        if t == 0:
            return MN("Bestäm amplituden för %s." % q, A, [A * 2, k, A + abs(c) if c else A + 1], "Amplituden är koefficienten framför %s: <b>%d</b>." % (f, A))
        if t == 1:
            return MN("Bestäm perioden i grader för %s." % q, F(360, k), [360 * k, F(180, k), 360], "Perioden är 360°/%d = <b>%s°</b>." % (k, d(F(360, k))), "°")
        return MN("Bestäm det största värdet för %s." % q, A + c, [A, c, A * k + c], "Största värdet är %d + %s = <b>%s</b>." % (A, par(c), sg(A + c)))

    def las():
        A, k = ri(1, 3), ch([1, 2, 3, F(1, 2)])
        f = ch(["sin", "cos"])
        fn = (lambda x: A * math.sin(float(k) * math.radians(x))) if f == "sin" else (lambda x: A * math.cos(float(k) * math.radians(x)))
        pic = graf(fn, (0, 720, 90), (-4, 4, 1), [], "trigonometrisk graf")
        kk = "" if k == 1 else d(k)
        res = "y = %s%s %sx" % ("" if A == 1 else "%d " % A, f, kk)
        oth = "cos" if f == "sin" else "sin"
        return M("Vilken funktion visas i grafen? (x i grader)" + pic, res, ["y = %s%s %sx" % ("" if A == 1 else "%d " % A, oth, kk), "y = %d %s %sx" % (A + 1, f, kk), "y = %s%s %sx" % ("" if A == 1 else "%d " % A, f, d(k * 2))], "Amplitud %d och period %s°: <b>%s</b>." % (A, d(F(360) / k), res))

    def period_rad():
        k = ri(1, 6)
        f = ch(["sin", "cos"])
        return M("Bestäm perioden för y = %s %sx i radianer." % (f, "" if k == 1 else k), pis(F(2, k)), [pis(F(1, k)), pis(F(2 * k)), pis(F(4, k))], "Perioden är 2π/%d = <b>%s</b>." % (k, pis(F(2, k))))

    def till():
        T = ri(8, 24)
        A = ri(2, 15)
        c = ri(5, 25)
        return M("Temperaturen varierar som T(t) = %d + %d sin(%s) °C, där t är tiden i timmar. Vilken är den lägsta temperaturen och perioden?" % (c, A, ("πt/%d" if F(2, T).numerator == 1 else "2πt/%d") % F(2, T).denominator), "%d °C, %d timmar" % (c - A, T), ["%d °C, %d timmar" % (c + A, T), "%d °C, %d timmar" % (c - A, 2 * T), "%s °C, %d timmar" % (sg(-A), T)],
                 "Lägsta värdet: %d − %d = %d. Perioden: 2π/(2π/%d) = %d. <b>%d °C, %d timmar</b>." % (c, A, c - A, T, T, c - A, T))

    sets = [("Amplitud, period och största värde", [(amp, 20)]), ("Läs av grafen", [(las, 20)]), ("Period i radianer", [(period_rad, 6), (amp, 14)]), ("Tillämpningar", [(till, 20)]), ("Blandat", [(amp, 16), (period_rad, 4)])]
    return U("trigonometriska-grafer", "TR", "Trigonometriska grafer: amplitud, period och förskjutning", "Trigonometriska grafer",
             "Egenskaper hos trigonometriska funktioner och deras grafer: amplitud, period och förskjutning, och modellering av periodiska förlopp.",
             "Uppgifter om trigonometriska grafer för Matematik 4: amplitud, period, största värde, läsa av grafer och tillämpningar. 100 uppgifter med facit.",
             "y = A sin kx + c", "Perioden är 360°/k eller 2π/k.", sets,
             ["För y = A sin kx + c är amplituden |A| och perioden 360°/k (eller 2π/k i radianer).",
              "c förskjuter grafen uppåt eller nedåt. Största värdet är c + A och minsta c − A.",
              "Periodiska förlopp som temperatur, tidvatten och ljud kan modelleras med sinus- och cosinusfunktioner."],
             [("y = 3 sin 2x + 1", ["A = 3", "period 180°", "max 4, min −2"], "")],
             [["Perioden är 360° · k", "Den är 360°/k"], ["Amplituden är största värdet", "Den är avståndet från mittlinjen"], ["Blandar ihop sin och cos", "cos börjar i sitt största värde"]],
             [("Vad är amplitud?", "Halva skillnaden mellan största och minsta värdet."), ("Vad är en period?", "Hur lång tid eller hur stor vinkel det tar innan grafen upprepar sig."), ("Var finns periodiska förlopp?", "I tidvatten, dagsljus, ljud och växelström.")])


# ============================================================ kedjeregeln
def kedje():
    def potens():
        a, b = nz(-5, 5), nz(-9, 9)
        n = ri(2, 6)
        inner = ps({1: a, 0: b})
        res = "f%s(x) = %s(%s)%s" % (P_, sg(n * a), inner, sup(n - 1) if n > 2 else "")
        return M("Derivera f(x) = (%s)%s." % (inner, sup(n)), res, ["f%s(x) = %d(%s)%s" % (P_, n, inner, sup(n - 1) if n > 2 else ""), "f%s(x) = %s(%s)%s" % (P_, sg(n * a), inner, sup(n)), "f%s(x) = %s" % (P_, sg(n * a))], "Yttre derivata %d(%s)%s gånger inre derivata %s: <b>%s</b>." % (n, inner, sup(n - 1) if n > 2 else "", sg(a), res))

    def exp_():
        a, b = nz(-5, 5), ri(-9, 9)
        c = nz(-4, 4)
        inner = ps({2: a, 0: b}) if coin() else ps({1: a, 0: b})
        dinner = ps({1: 2 * a}) if "x²" in inner else sg(a)
        res = "f%s(x) = %s · %se<sup>%s</sup>" % (P_, "(%s)" % dinner if "x" in dinner else dinner, "" if c == 1 else "%d" % c if c != -1 else MIN, inner)
        res = res.replace("· −e", "· (−1)e")
        return M("Derivera f(x) = %se<sup>%s</sup>." % ("" if c == 1 else (MIN if c == -1 else "%d" % c), inner), res, ["f%s(x) = %se<sup>%s</sup>" % (P_, "" if c == 1 else (MIN if c == -1 else "%d" % c), inner), "f%s(x) = %s · e<sup>%s</sup>" % (P_, "(%s)" % dinner if "x" in dinner else dinner, inner), "f%s(x) = %s · %se<sup>%s</sup>" % (P_, "(%s)" % dinner if "x" in dinner else dinner, "" if c == 1 else "%d" % c if c != -1 else MIN, dinner)],
                 "(e<sup>g(x)</sup>)′ = g′(x)e<sup>g(x)</sup>: <b>%s</b>." % res)

    def ln_():
        a, b = nz(-6, 6), nz(-9, 9)
        k = ri(0, 1)
        if k == 0:
            inner = ps({1: a, 0: b})
            return M("Derivera f(x) = ln(%s)." % inner, "f%s(x) = %s" % (P_, frac_html(sg(a), inner)), ["f%s(x) = %s" % (P_, frac_html("1", inner)), "f%s(x) = %s" % (P_, frac_html(sg(a), "x")), "f%s(x) = %s" % (P_, frac_html(inner, sg(a)))], "(ln g)′ = g′/g: <b>%s</b>." % frac_html(sg(a), inner))
        inner = ps({2: a, 0: b})
        return M("Derivera f(x) = ln(%s)." % inner, "f%s(x) = %s" % (P_, frac_html(ps({1: 2 * a}), inner)), ["f%s(x) = %s" % (P_, frac_html("1", inner)), "f%s(x) = %s" % (P_, frac_html(ps({1: 2 * a}), "x")), "f%s(x) = %s" % (P_, frac_html("2", "x"))], "(ln g)′ = g′/g: <b>%s</b>." % frac_html(ps({1: 2 * a}), inner))

    def trig():
        k = nz(-6, 6)
        A = nz(-5, 5)
        f = ch(["sin", "cos"])
        kk = "" if k == 1 else (MIN if k == -1 else str(k))
        if f == "sin":
            res = "f%s(x) = %scos %sx" % (P_, (lambda v: "" if v == 1 else (MIN if v == -1 else str(v)))(A * k), kk)
            w = ["f%s(x) = %scos %sx" % (P_, (lambda v: "" if v == 1 else (MIN if v == -1 else str(v)))(A), kk), "f%s(x) = %scos %sx" % (P_, (lambda v: "" if v == 1 else (MIN if v == -1 else str(v)))(-A * k), kk), "f%s(x) = %ssin %sx" % (P_, (lambda v: "" if v == 1 else (MIN if v == -1 else str(v)))(A * k), kk)]
        else:
            res = "f%s(x) = %ssin %sx" % (P_, (lambda v: "" if v == 1 else (MIN if v == -1 else str(v)))(-A * k), kk)
            w = ["f%s(x) = %ssin %sx" % (P_, (lambda v: "" if v == 1 else (MIN if v == -1 else str(v)))(-A), kk), "f%s(x) = %ssin %sx" % (P_, (lambda v: "" if v == 1 else (MIN if v == -1 else str(v)))(A * k), kk), "f%s(x) = %scos %sx" % (P_, (lambda v: "" if v == 1 else (MIN if v == -1 else str(v)))(-A * k), kk)]
        Aa = "" if A == 1 else (MIN if A == -1 else str(A))
        return M("Derivera f(x) = %s%s %sx." % (Aa, f, kk), res, w, "Inre derivata %s: <b>%s</b>." % (sg(k), res))

    def varde():
        a, b = nz(-3, 3), nz(-5, 5)
        n = ri(2, 4)
        x = ri(-2, 2)
        v = n * a * (a * x + b) ** (n - 1)
        return MN("f(x) = (%s)%s. Beräkna f%s(%d)." % (ps({1: a, 0: b}), sup(n), P_, x), v, [n * (a * x + b) ** (n - 1), (a * x + b) ** n, v + a], "f%s(x) = %s(%s)%s. f%s(%d) = <b>%s</b>." % (P_, sg(n * a), ps({1: a, 0: b}), sup(n - 1) if n > 2 else "", P_, x, num(v)))

    sets = [("Potenser av uttryck", [(potens, 20)]), ("Exponentialfunktioner", [(exp_, 20)]), ("Logaritmfunktioner", [(ln_, 20)]), ("Trigonometriska funktioner", [(trig, 20)]), ("Derivatans värde", [(varde, 20)])]
    return U("kedjeregeln", "DI", "Kedjeregeln: derivera sammansatta funktioner", "Kedjeregeln",
             "Härledning och användning av kedjeregeln för derivering av sammansatta funktioner.",
             "Uppgifter om kedjeregeln för Matematik 4: potenser av uttryck, exponentialfunktioner, logaritmfunktioner, trigonometriska funktioner och derivatans värde. 100 uppgifter med facit.",
             "Yttre derivata gånger inre derivata", "f(g(x))′ = f′(g(x)) · g′(x)", sets,
             ["En sammansatt funktion f(g(x)) har en yttre funktion f och en inre funktion g.",
              "Kedjeregeln: derivatan är den yttre derivatan (med den inre funktionen kvar) gånger den inre derivatan.",
              "Exempel: (e<sup>3x</sup>)′ = 3e<sup>3x</sup>, (ln(2x + 1))′ = 2/(2x + 1) och (sin 4x)′ = 4 cos 4x."],
             [("(3x − 1)⁴", ["4(3x − 1)³ · 3"], "12(3x − 1)³")],
             [["Glömmer inre derivatan", "Multiplicera med g′(x)"], ["Deriverar den inre funktionen i yttre derivatan", "Behåll g(x) i yttre derivatan"], ["(cos x)′ = sin x", "(cos x)′ = −sin x"]],
             [("Hur ser jag att kedjeregeln behövs?", "När något annat än x står inuti en funktion."), ("Kan kedjeregeln användas flera gånger?", "Ja, för funktioner i flera lager."), ("Varför fungerar den?", "Förändringshastigheterna multipliceras.")])


# ============================================================ produkt- och kvotregeln
def produkt():
    def prod():
        a = nz(-5, 5)
        n = ri(1, 3)
        k = nz(-3, 3)
        f = pol({n: a})
        res = "f%s(x) = %s" % (P_, "%se<sup>%sx</sup>(%s)" % ("", "" if k == 1 else (MIN if k == -1 else k), ps({n: a * k, n - 1: a * n})))
        return M("Derivera f(x) = %se<sup>%sx</sup>." % (f, "" if k == 1 else (MIN if k == -1 else k)), res,
                 ["f%s(x) = %se<sup>%sx</sup>" % (P_, pol({n - 1: a * n * k}) if n > 1 else sg(a * k), "" if k == 1 else (MIN if k == -1 else k)), "f%s(x) = e<sup>%sx</sup>(%s)" % (P_, "" if k == 1 else (MIN if k == -1 else k), ps({n: a, n - 1: a * n})), "f%s(x) = e<sup>%sx</sup>(%s)" % (P_, "" if k == 1 else (MIN if k == -1 else k), ps({n: a * k, n - 1: -a * n}))],
                 "Produktregeln: f′ = u′v + uv′ = <b>%s</b>." % res[len("f′(x) = "):])

    def prod_trig():
        n = ri(1, 3)
        f = ch(["sin", "cos"])
        if f == "sin":
            res = "f%s(x) = %s sin x + %s cos x" % (P_, pol({n - 1: n}) if n > 1 else "", xp(n)) if n > 1 else "f%s(x) = sin x + x cos x" % P_
            w = ["f%s(x) = %s cos x" % (P_, pol({n - 1: n}) if n > 1 else "1"), "f%s(x) = %s sin x − %s cos x" % (P_, pol({n - 1: n}) if n > 1 else "1", xp(n)), "f%s(x) = %s cos x" % (P_, xp(n))]
        else:
            res = "f%s(x) = %s cos x − %s sin x" % (P_, pol({n - 1: n}), xp(n)) if n > 1 else "f%s(x) = cos x − x sin x" % P_
            w = ["f%s(x) = %s sin x" % (P_, MIN + (pol({n - 1: n}) if n > 1 else "1")), "f%s(x) = %s cos x + %s sin x" % (P_, pol({n - 1: n}) if n > 1 else "1", xp(n)), "f%s(x) = %s sin x" % (P_, MIN + xp(n))]
        return M("Derivera f(x) = %s %s x." % (xp(n), f), res, w, "u = %s, v = %s x. f′ = u′v + uv′: <b>%s</b>." % (xp(n), f, res[len("f′(x) = "):]))

    def kvot():
        a, b = nz(-6, 6), nz(-6, 6)
        c, e = nz(-6, 6), nz(-6, 6)
        if a * e - b * c == 0:
            return None
        num_ = a * e - b * c
        den = "(%s)²" % ps({1: c, 0: e})
        res = "f%s(x) = %s" % (P_, frac_html(sg(num_), den))
        return M("Derivera f(x) = %s." % frac_html(ps({1: a, 0: b}), ps({1: c, 0: e})), res, ["f%s(x) = %s" % (P_, frac_html(sg(-num_), den)), "f%s(x) = %s" % (P_, sg(F(a, c))), "f%s(x) = %s" % (P_, frac_html(sg(a * e + b * c), den)) if a * e + b * c != num_ else "f%s(x) = %s" % (P_, frac_html(sg(num_), ps({1: c, 0: e})))],
                 "Kvotregeln: (u′v − uv′)/v² = (%s · (%s) − (%s) · %s)/v² = <b>%s</b>." % (sg(a), ps({1: c, 0: e}), ps({1: a, 0: b}), par(c), frac_html(sg(num_), den)))

    def varde():
        a = nz(-4, 4)
        x = ri(-2, 2)
        n = ri(1, 3)
        # f = a x^n e^x → f' = a e^x (n x^(n-1) + x^n)
        v = a * (n * F(x) ** (n - 1) + F(x) ** n) if not (n == 1 and False) else 0
        if x == 0 and n > 1:
            v = 0
        r_txt = ("%se<sup>%d</sup>" % ("" if v == 1 else (MIN if v == -1 else sg(v)), x)) if v and x not in (0,) else (sg(v) if v and x == 0 else "0")
        if x == 1:
            r_txt = "%se" % ("" if v == 1 else (MIN if v == -1 else sg(v))) if v else "0"
        w0 = a * n * F(x) ** (n - 1) if not (x == 0 and n == 1) else a
        def t(vv):
            if vv == 0:
                return "0"
            if x == 0:
                return sg(vv)
            if x == 1:
                return "%se" % ("" if vv == 1 else (MIN if vv == -1 else sg(vv)))
            return "%se<sup>%s</sup>" % ("" if vv == 1 else (MIN if vv == -1 else sg(vv)), sg(x))
        return M("f(x) = %se<sup>x</sup>. Beräkna f%s(%d) exakt." % (pol({n: a}), P_, x), t(v), [t(w0), t(a * F(x) ** n) if a * F(x) ** n != v else t(v + 1), t(v * 2) if v else t(a)],
                 "f%s(x) = e<sup>x</sup>(%s). f%s(%d) = <b>%s</b>." % (P_, ps({n: a, n - 1: a * n}), P_, x, t(v)))

    sets = [("Produktregeln med eˣ", [(prod, 20)]), ("Produktregeln med sin och cos", [(prod_trig, 6), (prod, 14)]), ("Kvotregeln", [(kvot, 20)]), ("Derivatans värde", [(varde, 20)]), ("Blandat", [(kvot, 10), (prod, 10)])]
    return U("produkt-och-kvotregeln", "DI", "Produktregeln och kvotregeln", "Produkt- och kvotregeln",
             "Härledning och användning av deriveringsregler för produkt och kvot av funktioner.",
             "Uppgifter om produkt- och kvotregeln för Matematik 4: produktregeln med eˣ, sin och cos, kvotregeln och derivatans värde. 100 uppgifter med facit.",
             "(uv)′ = u′v + uv′", "(u/v)′ = (u′v − uv′)/v²", sets,
             ["Produktregeln: om f = u · v är f′ = u′v + uv′. Derivatan av en produkt är inte produkten av derivatorna.",
              "Kvotregeln: om f = u/v är f′ = (u′v − uv′)/v². Ordningen i täljaren är viktig.",
              "Bryt gärna ut gemensamma faktorer i svaret, till exempel eˣ."],
             [("x²eˣ", ["2x · eˣ + x² · eˣ"], "eˣ(x² + 2x)"), ("x/(x + 1)", ["(1 · (x + 1) − x · 1)/(x + 1)²"], "1/(x + 1)²")],
             [["(uv)′ = u′v′", "Använd produktregeln"], ["Byter ordning i kvotregeln", "u′v − uv′, i den ordningen"], ["Glömmer kvadraten i nämnaren", "Nämnaren är v²"]],
             [("Kan jag använda produktregeln i stället för kvotregeln?", "Ja, skriv u/v = u · v⁻¹ och använd kedjeregeln."), ("Behöver jag förenkla?", "Det gör svaret tydligare, särskilt om du ska lösa f′ = 0."), ("Var används reglerna?", "När du undersöker grafer och löser optimeringsproblem.")])


# ============================================================ grafer och asymptoter
def asymptoter():
    def lodr():
        a = nz(-6, 6)
        c, b = nz(-5, 5), ri(-5, 5)
        q = frac_html(ps({1: c, 0: b}) if b or c else "1", "x %s %d" % ("−" if a > 0 else "+", abs(a)))
        if c * a + b == 0:
            return None
        return M("Bestäm den lodräta asymptoten till y = %s." % q, "x = %s" % sg(a), ["x = %s" % sg(-a), "y = %s" % sg(c), "x = %s" % sg(c)], "Nämnaren är 0 när x = %s (täljaren är inte 0 där): <b>x = %s</b>." % (sg(a), sg(a)))

    def vagr():
        a = nz(-6, 6)
        c, b = nz(-5, 5), nz(-5, 5)
        if c * a + b == 0:
            return None
        q = frac_html(ps({1: c, 0: b}), "x %s %d" % ("−" if a > 0 else "+", abs(a)))
        return M("Bestäm den vågräta asymptoten till y = %s." % q, "y = %s" % sg(c), ["y = %s" % sg(b), "x = %s" % sg(a), "y = 0" if c else "y = 1"], "När x → ±∞ går y mot kvoten av koefficienterna: <b>y = %s</b>." % sg(c))

    def sned():
        k, m = nz(-4, 4), ri(-5, 5)
        a = ri(1, 9)
        p = nz(-4, 4)
        q = "%s + %s" % (ps({1: k, 0: m}), frac_html(str(a), "x %s %d" % ("−" if p > 0 else "+", abs(p))))
        return M("Bestäm den sneda asymptoten till y = %s." % q, "y = %s" % ps({1: k, 0: m}), ["y = %s" % ps({1: k}) if m else "y = %s" % ps({1: k, 0: 1}), "x = %s" % sg(p), "y = %d" % a], "Bråket går mot 0 när x → ±∞: <b>y = %s</b>." % ps({1: k, 0: m}))

    def deriv_graf():
        P = [("f′(x) &gt; 0 för alla x", "f är växande överallt", ["f är avtagande", "f har ett maximum", "f är konstant"]),
             ("f′(a) = 0 och f′ byter tecken från + till −", "f har en maximipunkt i x = a", ["f har en minimipunkt i x = a", "f har en terrasspunkt i x = a", "f(a) = 0"]),
             ("f″(x) &gt; 0 i ett intervall", "Grafen är konvex (böjer uppåt)", ["Grafen är konkav", "f är avtagande", "f har ett maximum"]),
             ("f″(a) = 0 och f″ byter tecken", "Grafen har en inflexionspunkt i x = a", ["f har ett maximum i x = a", "f′(a) = 0", "f har en asymptot i x = a"]),
             ("f′(a) = 0 och f′ byter inte tecken", "f har en terrasspunkt i x = a", ["f har en maximipunkt", "f har en minimipunkt", "f är växande överallt"])]
        q, r, w = ch(P)
        a = ri(-5, 5)
        return M("Vad kan du säga om grafen om %s? (a = %s)" % (q.replace("a", "a"), sg(a)), r, w, "<b>%s</b>." % r)

    def infl():
        a = nz(-3, 3)
        b = ri(-6, 6) * 3
        c = ri(-9, 9)
        x0 = F(-2 * b, 6 * a)
        cs = {3: a, 2: b, 1: c, 0: ri(-5, 5)}
        if x0.denominator != 1:
            return None
        return MN("Bestäm x-koordinaten för inflexionspunkten till f(x) = %s." % ps(cs), x0, [-x0 if x0 else 1, F(-b, a) if F(-b, a) != x0 else x0 + 1, F(-c, 2 * b) if b and F(-c, 2 * b) != x0 else x0 + 2], "f%s%s(x) = %s = 0 ger <b>x = %s</b>." % (P_, P_, ps({1: 6 * a, 0: 2 * b}), sg(x0)))

    sets = [("Lodräta asymptoter", [(lodr, 20)]), ("Vågräta asymptoter", [(vagr, 20)]), ("Sneda asymptoter", [(sned, 20)]), ("Derivata och grafens form", [(deriv_graf, 5), (infl, 15)]), ("Blandat", [(lodr, 7), (vagr, 7), (sned, 6)])]
    return U("grafer-och-asymptoter", "DI", "Grafer: asymptoter, inflexionspunkter och derivata", "Grafer och asymptoter",
             "Egenskaper hos funktioner och deras grafer, bland annat asymptoter och inflexionspunkter, undersökta med derivata.",
             "Uppgifter om grafer och asymptoter för Matematik 4: lodräta, vågräta och sneda asymptoter, inflexionspunkter och derivatans koppling till grafens form. 100 uppgifter med facit.",
             "Lodrät asymptot där nämnaren är 0", "Inflexionspunkt där f″ byter tecken.", sets,
             ["En lodrät asymptot x = a finns där nämnaren är 0 men inte täljaren.",
              "En vågrät eller sned asymptot beskriver hur grafen beter sig när x → ±∞.",
              "f′ visar var grafen växer och avtar. f″ visar om grafen är konvex eller konkav. Där f″ byter tecken finns en inflexionspunkt."],
             [("y = (2x + 1)/(x − 3)", ["Lodrät: x = 3", "Vågrät: y = 2"], "")],
             [["Asymptoten är y = a", "Lodrät asymptot skrivs x = a"], ["f″ = 0 ger alltid inflexionspunkt", "f″ måste byta tecken"], ["Glömmer sneda asymptoter", "Skriv om som kx + m + bråk"]],
             [("Kan grafen korsa en vågrät asymptot?", "Ja, men den närmar sig asymptoten när x → ±∞."), ("Vad är en inflexionspunkt?", "En punkt där grafen byter från konvex till konkav."), ("Hur ritar jag grafen?", "Bestäm nollställen, asymptoter, extrempunkter och inflexionspunkter.")])


# ============================================================ integraler och volymer
def volymer():
    def trig_int():
        k = ri(1, 4)
        f = ch(["sin", "cos"])
        A = nz(-6, 6)
        kk = "" if k == 1 else str(k)
        Aa = "" if A == 1 else (MIN if A == -1 else str(A))
        if f == "cos":
            res = "F(x) = %s sin %sx + C" % ((lambda v: "" if v == 1 else (MIN if v == -1 else sg(v)))(F(A, k)), kk)
            w = ["F(x) = %s sin %sx + C" % ((lambda v: "" if v == 1 else (MIN if v == -1 else sg(v)))(A * k), kk), "F(x) = %s sin %sx + C" % ((lambda v: "" if v == 1 else (MIN if v == -1 else sg(v)))(F(-A, k)), kk), "F(x) = %s cos %sx + C" % ((lambda v: "" if v == 1 else (MIN if v == -1 else sg(v)))(F(A, k)), kk)]
        else:
            res = "F(x) = %s cos %sx + C" % ((lambda v: "" if v == 1 else (MIN if v == -1 else sg(v)))(F(-A, k)), kk)
            w = ["F(x) = %s cos %sx + C" % ((lambda v: "" if v == 1 else (MIN if v == -1 else sg(v)))(F(A, k)), kk), "F(x) = %s cos %sx + C" % ((lambda v: "" if v == 1 else (MIN if v == -1 else sg(v)))(-A * k), kk), "F(x) = %s sin %sx + C" % ((lambda v: "" if v == 1 else (MIN if v == -1 else sg(v)))(F(-A, k)), kk)]
        return M("Bestäm en primitiv funktion till f(x) = %s%s %sx." % (Aa, f, kk), res, w, "Primitiv till %s kx är %s: <b>%s</b>." % (f, "sin kx / k" if f == "cos" else "−cos kx / k", res))

    def ln_int():
        a = ri(1, 9)
        b = ri(2, 9)
        v = math.log(b) * a
        return M("Beräkna ∫<sub>1</sub><sup>%d</sup> %s dx exakt." % (b, frac_html(str(a), "x")), "%sln %d" % ("" if a == 1 else a, b), ["%s" % d(F(a, b)) if F(a, b).denominator in (1, 2, 4, 5, 8) else "%s/%d" % (a, b), "%sln %d" % ("" if a == 1 else a, b - 1), "%sln %d" % ("" if a * b == 1 else a * b, b) if a > 1 else "ln %d" % (b * b)], "Primitiv till 1/x är ln x: %d(ln %d − ln 1) = <b>%sln %d</b>." % (a, b, "" if a == 1 else a, b))

    def mellan():
        a = ri(1, 4)
        b = ri(1, 8)
        # y = b x and y = a x² intersect x = 0 and x = b/a
        x1 = F(b, a)
        A = F(b, 2) * x1 * x1 - F(a, 3) * x1 ** 3
        return MN("Beräkna arean mellan kurvorna y = %s och y = %s." % (pol({1: b}), pol({2: a})), A, [F(b, 2) * x1 * x1, F(a, 3) * x1 ** 3, A * 6], "Skärning i x = 0 och x = %s. ∫(%s − %s) dx = <b>%s a.e.</b>" % (sg(x1), pol({1: b}), pol({2: a}), sg(A)), "a.e.")

    def rot():
        k = ri(0, 2)
        b = ri(1, 4)
        if k == 0:
            c = ri(1, 5)
            V = F(c * c * b ** 3, 3)
            return M("Området mellan y = %s, x-axeln och x = %d roterar kring x-axeln. Bestäm volymen exakt." % (pol({1: c}), b), "%sπ v.e." % (fq(V) if V != 1 else ""), ["%sπ v.e." % fq(F(c * b * b, 2)), "%sπ v.e." % fq(V * 3), "%s v.e." % fq(V)], "V = π∫<sub>0</sub><sup>%d</sup> (%s)² dx = π · %s = <b>%sπ v.e.</b>" % (b, pol({1: c}), fq(V), fq(V)))
        if k == 1:
            V = F(b * b, 2)
            return M("Området under y = √x mellan x = 0 och x = %d roterar kring x-axeln. Bestäm volymen exakt." % b, "%sπ v.e." % (fq(V) if V != 1 else ""), ["%sπ v.e." % fq(F(2, 3) * b ** F(3, 2) if False else F(b, 1)), "%s v.e." % fq(V), "%sπ v.e." % fq(V * 2)], "V = π∫x dx = π · %d²/2 = <b>%sπ v.e.</b>" % (b, fq(V)))
        a = ri(1, 3)
        V = F(a * a * b ** 5, 5)
        return M("Området mellan y = %s, x-axeln och x = %d roterar kring x-axeln. Bestäm volymen exakt." % (pol({2: a}), b), "%sπ v.e." % fq(V), ["%sπ v.e." % fq(F(a * b ** 3, 3)), "%sπ v.e." % fq(F(a * a * b ** 4, 4)), "%s v.e." % fq(V)], "V = π∫(%s)² dx = π∫%s dx = <b>%sπ v.e.</b>" % (pol({2: a}), pol({4: a * a}), fq(V)))

    def medel():
        a = ri(1, 6)
        b = ri(1, 6)
        v = F(a * b * b, 3)
        return MN("Bestäm medelvärdet av f(x) = %s på intervallet 0 ≤ x ≤ %d." % (pol({2: a}), b), v, [F(a * b * b, 2), a * b * b, F(a * b ** 3, 3)], "Medelvärdet = (1/%d)∫<sub>0</sub><sup>%d</sup> %s dx = <b>%s</b>." % (b, b, pol({2: a}), sg(v)))

    sets = [("Trigonometriska primitiver", [(trig_int, 20)]), ("Integraler med 1/x", [(ln_int, 20)]), ("Area mellan kurvor", [(mellan, 20)]), ("Rotationsvolymer", [(rot, 20)]), ("Medelvärde av en funktion", [(medel, 20)])]
    return U("integraler-och-volymer", "DI", "Integraler: area mellan kurvor och rotationsvolymer", "Integraler och volymer",
             "Primitiva funktioner till trigonometriska funktioner och 1/x. Integraler för area mellan kurvor, rotationsvolymer och medelvärde.",
             "Uppgifter om integraler och volymer för Matematik 4: trigonometriska primitiver, integraler med 1/x, area mellan kurvor, rotationsvolymer och medelvärde. 100 uppgifter med facit.",
             "Rotationsvolym V = π∫ f(x)² dx", "Area = ∫ (övre − undre) dx", sets,
             ["Primitiv till cos kx är sin kx / k, till sin kx är −cos kx / k och till 1/x är ln |x|.",
              "Arean mellan två kurvor är ∫ (övre − undre) dx mellan skärningspunkterna.",
              "När området under y = f(x) roterar kring x-axeln blir volymen V = π∫<sub>a</sub><sup>b</sup> f(x)² dx."],
             [("y = x, 0 ≤ x ≤ 3, kring x-axeln", ["V = π∫x² dx = π · 27/3"], "9π v.e.")],
             [["Glömmer π i rotationsvolymen", "V = π∫f(x)² dx"], ["Kvadrerar inte f(x)", "Det är f(x)²"], ["Undre minus övre", "Övre minus undre"]],
             [("Vad är v.e.?", "Volymenheter."), ("Kan man rotera kring y-axeln?", "Ja, med en liknande metod."), ("Vad är medelvärdet av en funktion?", "Den konstanta höjd som ger samma area på intervallet.")])


UNITS = {"komplexa-tal-i-rektangular-form": rekt, "komplexa-tal-i-polar-form": polar, "polynomekvationer-och-faktorsatsen": faktor, "enhetscirkeln-och-radianer": radianer,
         "trigonometriska-formler": formler, "trigonometriska-ekvationer": ekvationer, "trigonometriska-grafer": grafer, "kedjeregeln": kedje, "produkt-och-kvotregeln": produkt,
         "grafer-och-asymptoter": asymptoter, "integraler-och-volymer": volymer}
