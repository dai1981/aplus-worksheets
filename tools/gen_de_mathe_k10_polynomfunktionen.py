# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 10: Polynomfunktionen (ganzrationale Funktionen)（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k10_polynomfunktionen.py
Grad, Leitkoeffizient, y-Achsenabschnitt, Verhalten für x → ±∞, Symmetrie (nur gerade / nur ungerade Exponenten),
Nullstellen aus der Linearfaktorform, durch Ausklammern, mit Substitution (biquadratisch), Vielfachheit, Graphen zuordnen, Sachaufgaben.
Fehler: Nullstellen von (x − 2) als −2, Ausklammern und dabei x = 0 vergessen, Grad = Anzahl der Summanden, Symmetrie wegen des absoluten Glieds übersehen.
"""
import random, math
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, num, BLUE
from de_k6 import bh, dz
from de_k8 import coef
from de_k10 import mcq, zr, kurve

R = random.Random(50005)
M = "−"
NB = " "
SUP = {1: "", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶"}


def zz(v):
    v = Fr(v)
    if v < 0:
        return M + zz(-v)
    return dz(v) if v.denominator == 1 else bh(v)


def poly(cs):
    """cs: {Exponent: Koeffizient}"""
    out = ""
    for e in sorted(cs, reverse=True):
        k = Fr(cs[e])
        if k == 0:
            continue
        out += coef(k, ("x" + SUP[e]) if e else "", out == "")
    return out or "0"


def expand(roots, a=1):
    c = [Fr(a)]
    for r in roots:
        n = [Fr(0)] * (len(c) + 1)
        for i, k in enumerate(c):
            n[i] += k
            n[i + 1] -= k * r
        c = n
    deg = len(c) - 1
    return {deg - i: k for i, k in enumerate(c)}


def lf(r):
    if r == 0:
        return "x"
    return "(x%s%s%s%s)" % (NB, M if r > 0 else "+", NB, zz(abs(r)))


def faktor(roots, a=1, mult=None):
    pre = "" if a == 1 else (M if a == -1 else zz(a))
    s = ""
    for r in sorted(roots, key=lambda r: r != 0):
        f = lf(r)
        if mult and mult.get(r, 1) > 1:
            f = (f if r != 0 else "x") + SUP[mult[r]]
        s += f
    return pre + s


def nst(rs):
    rs = sorted(set(rs))
    return "x = " + "; x = ".join(zz(r) for r in rs) if len(rs) < 4 else "x = " + "; ".join(zz(r) for r in rs)


def grad():
    n = R.randint(2, 5)
    cs = {e: R.choice([0, 0, 1, -1, 2, -3, 4, Fr(1, 2)]) for e in range(n)}
    cs[n] = R.choice([1, -1, 2, -2, 3, Fr(1, 2), -Fr(1, 3)])
    if sum(1 for e in cs if cs[e] != 0) < 3:
        return None
    f = "f(x) = " + poly(cs)
    kind = R.choice(["g", "g", "l", "y"])
    if kind == "g":
        t = sum(1 for e in cs if cs[e] != 0)
        return mcq("Welchen Grad hat %s?" % f, "Grad %d" % n, ["Grad %d" % t if t != n else "Grad %d" % (n + 1), "Grad %d" % (n - 1), "Grad %d" % (n + 2) if t != n + 2 else "Grad 1"],
                   "Der höchste Exponent ist %d: <b>Grad %d</b>." % (n, n))
    if kind == "l":
        return mcq("Wie heißt der Leitkoeffizient von %s?" % f, zz(cs[n]), [zz(cs[0]) if cs[0] != cs[n] else zz(cs[n] + 1), zz(n), zz(-cs[n])],
                   "Der Faktor vor x%s ist der Leitkoeffizient: <b>%s</b>." % (SUP[n], zz(cs[n])))
    return mcq("Wo schneidet der Graph von %s die y-Achse?" % f, "bei y = %s" % zz(cs[0]), ["bei y = %s" % zz(cs[n]) if cs[n] != cs[0] else "bei y = %s" % zz(cs[0] + 1), "bei y = 0" if cs[0] else "bei y = 1", "bei y = %s" % zz(-cs[0]) if cs[0] else "bei y = %s" % zz(cs[n] + 2)],
               "f(0) = absolutes Glied: <b>y = %s</b>." % zz(cs[0]))


VERL = {(1, 1): "von links unten nach rechts oben", (1, -1): "von links oben nach rechts unten",
        (0, 1): "von links oben nach rechts oben", (0, -1): "von links unten nach rechts unten"}


def verhalten():
    n = R.randint(2, 6)
    a = R.choice([1, -1, 2, -2, 3, -4, Fr(1, 2), -Fr(1, 2)])
    cs = {n: a}
    for e in range(n):
        if R.random() < 0.6:
            cs[e] = R.choice([1, -2, 3, -5, 7, 10, -8])
    if len(cs) < 3:
        return None
    s = 1 if a > 0 else -1
    key = (n % 2, s)
    ans = "Er verläuft " + VERL[key] + "."
    w = ["Er verläuft " + VERL[k] + "." for k in VERL if k != key]
    return mcq("Wie verläuft der Graph von f(x) = %s für große |x|?" % poly(cs), ans, w,
               "Nur der Summand %s zählt: Grad %d (%s), Leitkoeffizient %s. <b>%s</b>" % (coef(a, "x" + SUP[n], True), n, "ungerade" if n % 2 else "gerade", "positiv" if a > 0 else "negativ", ans))


def linear():
    k = R.choice([2, 3, 3, 3])
    rs = R.sample([-4, -3, -2, -1, 0, 1, 2, 3, 4, 5, Fr(1, 2), -Fr(3, 2)], k)
    a = R.choice([1, 1, 2, -1, -3, Fr(1, 2)])
    kind = R.choice(["n", "n", "n", "g", "y"])
    f = "f(x) = " + faktor(rs, a)
    if kind == "n":
        return mcq("Bestimme die Nullstellen von %s." % f, nst(rs), [nst([-r for r in rs]), nst([r for r in rs if r != 0] + ([a] if a not in rs else [])) if 0 in rs else nst(rs[:-1]), nst([-r for r in rs[:1]] + rs[1:])],
                   "Ein Produkt ist 0, wenn ein Faktor 0 ist: <b>%s</b>." % nst(rs))
    if kind == "g":
        return mcq("Welchen Grad hat %s?" % f, "Grad %d" % k, ["Grad %d" % (k + 1), "Grad %d" % (k - 1), "Grad %d" % (2 * k)],
                   "Ausmultipliziert ist der höchste Exponent %d: <b>Grad %d</b>." % (k, k))
    y = a
    for r in rs:
        y *= -r
    return mcq("Wo schneidet der Graph von %s die y-Achse?" % f, "bei y = %s" % zz(y), ["bei y = %s" % zz(-y) if y else "bei y = 1", "bei y = %s" % zz(a) if a != y else "bei y = %s" % zz(y + 2), "bei y = %s" % zz(sum(rs)) if sum(rs) not in (y, -y, a) else "bei y = %s" % zz(y + 1)],
               "x = 0 einsetzen: f(0) = <b>%s</b>." % zz(y))


def ausklammern():
    kind = R.choice(["x", "x", "x2", "bi", "bi"])
    if kind == "x":
        p, q = R.sample([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6], 2)
        a = R.choice([1, 1, 2, -1])
        cs = expand([0, p, q], a)
        rs = [0, p, q]
        return mcq("Bestimme alle Nullstellen von f(x) = %s." % poly(cs), nst(rs), [nst([p, q]), nst([0, -p, -q]), nst([0, p * q]) if p * q not in (p, q, 0) else nst([0, -p])],
                   "x ausklammern: f(x) = x %s (%s). Also x = 0 oder %s = 0: <b>%s</b>." % (MAL, poly({e - 1: k for e, k in cs.items() if e > 0}), poly({e - 1: k for e, k in cs.items() if e > 0}), nst(rs)))
    if kind == "x2":
        c = R.choice([1, 4, 9, 16, 25])
        r = int(math.isqrt(c))
        cs = {4: 1, 2: -c}
        return mcq("Bestimme alle Nullstellen von f(x) = %s." % poly(cs), nst([-r, 0, r]), [nst([-r, r]), nst([0, c]), nst([0, r])],
                   "x² ausklammern: x² (x² − %d) = 0 ⇒ x = 0 (doppelt) oder x² = %d: <b>%s</b>." % (c, c, nst([-r, 0, r])))
    u1, u2 = R.sample([1, 4, 9, 16, 25, 36], 2)
    cs = {4: 1, 2: -(u1 + u2), 0: u1 * u2}
    rs = [math.isqrt(u1), -math.isqrt(u1), math.isqrt(u2), -math.isqrt(u2)]
    return mcq("Bestimme alle Nullstellen von f(x) = %s (Substitution z = x²)." % poly(cs), nst(rs),
               [nst([u1, u2]), nst([math.isqrt(u1), math.isqrt(u2)]), nst([-u1, -u2, u1, u2])],
               "z² − %d z + %d = 0 ⇒ z = %d oder z = %d. Dann x² = z: <b>%s</b>." % (u1 + u2, u1 * u2, min(u1, u2), max(u1, u2), nst(rs)))


def symmetrie():
    kind = R.choice(["s", "s", "s", "v"])
    if kind == "s":
        typ = R.choice(["g", "u", "k"])
        if typ == "g":
            es = R.sample([0, 2, 4, 6], 3)
        elif typ == "u":
            es = R.sample([1, 3, 5], 2) + ([] if R.random() < 0.5 else [R.choice([1, 3, 5])])
        else:
            es = [R.choice([3, 5, 4]), R.choice([2, 1]), 0]
            if es[0] % 2 == es[1] % 2 and 0 not in es:
                return None
        es = sorted(set(es), reverse=True)
        if len(es) < 2:
            return None
        cs = {e: R.choice([1, -2, 3, -4, 5, Fr(1, 2)]) for e in es}
        if typ == "k":
            ex = [e for e in cs]
            if all(e % 2 == 0 for e in ex) or all(e % 2 == 1 for e in ex):
                return None
        ans = {"g": "achsensymmetrisch zur y-Achse", "u": "punktsymmetrisch zum Ursprung", "k": "weder zur y-Achse noch zum Ursprung symmetrisch"}[typ]
        w = [v for v in ["achsensymmetrisch zur y-Achse", "punktsymmetrisch zum Ursprung", "weder zur y-Achse noch zum Ursprung symmetrisch", "achsensymmetrisch zur x-Achse"] if v != ans]
        why = {"g": "Nur gerade Exponenten (die Zahl allein zählt als x⁰)", "u": "Nur ungerade Exponenten", "k": "Gerade und ungerade Exponenten gemischt"}[typ]
        return mcq("Welche Symmetrie hat der Graph von f(x) = %s?" % poly(cs), "Er ist %s." % ans, ["Er ist %s." % v for v in w], "%s: <b>%s</b>." % (why, ans))
    r = R.choice([-3, -2, -1, 1, 2, 3])
    s = R.choice([v for v in [-3, -2, -1, 0, 1, 2, 3] if v != r])
    return mcq("Wie verhält sich der Graph von f(x) = %s an der Stelle x = %s?" % (faktor([r, s], 1, {r: 2}), zz(r)),
               "Er berührt die x-Achse (doppelte Nullstelle).", ["Er schneidet die x-Achse (einfache Nullstelle).", "Er hat dort keine Nullstelle.", "Er hat dort eine Polstelle."],
               "Der Faktor %s kommt quadratisch vor: doppelte Nullstelle, kein Vorzeichenwechsel. <b>Er berührt die x-Achse.</b>" % lf(r))


def graph():
    rs = sorted(R.sample([-3, -2, -1, 0, 1, 2, 3], 3))
    a = R.choice([Fr(1, 2), -Fr(1, 2), Fr(1, 3), -Fr(1, 3), Fr(1, 4), -Fr(1, 4)])
    f = lambda x: float(a) * (x - rs[0]) * (x - rs[1]) * (x - rs[2])
    if max(abs(f(x / 10)) for x in range(-35, 36)) < 1.5:
        return None
    pic = kurve([(f, BLUE, "")], (-4, 4, 1), (-6, 6, 2), W=320, H=300, label="Graph einer Polynomfunktion dritten Grades")
    ans = "f(x) = " + faktor(rs, a)
    w = ["f(x) = " + faktor(rs, -a), "f(x) = " + faktor([-r for r in rs], a) if sorted(-r for r in rs) != rs else "f(x) = " + faktor([rs[0], rs[1], rs[2] + 1], a),
         "f(x) = " + faktor(rs[:2], a)]
    return mcq(pic + "Welche Gleichung gehört zum Graphen?", ans, w,
               "Nullstellen bei %s; der Graph verläuft %s, also ist a %s 0: <b>%s</b>." % ("; ".join(zz(r) for r in rs), VERL[(1, 1 if a > 0 else -1)], "&gt;" if a > 0 else "&lt;", ans))


def sach():
    kind = R.choice(["box", "box", "gew", "wert"])
    if kind == "box":
        s = R.choice([20, 24, 30, 16, 40])
        x = R.choice([d for d in range(1, s // 2) if d <= 6])
        v = x * (s - 2 * x) ** 2
        return mcq("Aus einem quadratischen Karton (Seite %d cm) wird eine Schachtel gefaltet: An den Ecken werden Quadrate mit der Seite x cm ausgeschnitten. Dann gilt V(x) = x %s (%d − 2x)². Wie groß ist das Volumen für x = %d?" % (s, MAL, s, x),
                   "%s cm³" % num(v), ["%s cm³" % num((s - 2 * x) ** 2), "%s cm³" % num(x * (s - x) ** 2), "%s cm³" % num(x * (s - 2 * x) * 2)],
                   "V(%d) = %d %s %d² = %d %s %d = <b>%s cm³</b>." % (x, x, MAL, s - 2 * x, x, MAL, (s - 2 * x) ** 2, num(v)))
    if kind == "gew":
        a, b, c = R.choice([(1, 6, 0), (1, 9, 0), (1, 12, 0)])
        x = R.randint(2, b - 1)
        g = -x ** 3 + b * x ** 2
        return mcq("Der Gewinn eines Betriebs ist G(x) = %s (x in Tausend Stück, G in Tausend €). Wie hoch ist der Gewinn bei %d Tausend Stück?" % (poly({3: -1, 2: b}), x),
                   "%s Tausend €" % num(g), ["%s Tausend €" % num(x ** 3 + b * x ** 2), "%s Tausend €" % num(-3 * x + 2 * b), "%s Tausend €" % num(b * x ** 2)],
                   "G(%d) = %s%d + %d %s %d = <b>%s Tausend €</b>. Der Gewinn ist 0 bei x = 0 und x = %d." % (x, M, x ** 3, b, MAL, x ** 2, num(g), b))
    rs = sorted(R.sample([-4, -3, -2, -1, 1, 2, 3, 4], 2))
    t = R.choice([v for v in range(-4, 6) if v not in rs and v != 0])
    cs = expand(rs + [0], 1)
    val = t * (t - rs[0]) * (t - rs[1])
    return mcq("Für die Funktion h(x) = %s soll der Funktionswert an der Stelle x = %s bestimmt werden. Wie groß ist er?" % (poly(cs), zz(t)), zz(val), [zz(-val) if val else "1", zz(t ** 3), zz(val + 2 * t if t else val + 3)],
               "Einsetzen oder Linearfaktorform x(x %s %s)(x %s %s): <b>%s</b>." % (M if rs[0] > 0 else "+", zz(abs(rs[0])), M if rs[1] > 0 else "+", zz(abs(rs[1])), zz(val)))


def main():
    seen = set()
    sets = [
        ("Grad, Leitkoeffizient, y-Achse", mix(R, seen, [(grad, 14), (verhalten, 6)])),
        ("Verhalten im Unendlichen und Symmetrie", mix(R, seen, [(verhalten, 10), (symmetrie, 10)])),
        ("Nullstellen aus Linearfaktoren", mix(R, seen, [(linear, 20)])),
        ("Ausklammern und Substitution", mix(R, seen, [(ausklammern, 20)])),
        ("Graphen und Sachaufgaben", mix(R, seen, [(graph, 10), (sach, 10)])),
    ]
    body = lesson(
        ["Eine <b>Polynomfunktion</b> (ganzrationale Funktion) ist eine Summe von Potenzen mit natürlichen Exponenten, z. B. f(x) = 2x³ − x + 5. Der höchste Exponent ist der <b>Grad</b>, sein Faktor der <b>Leitkoeffizient</b>.",
         "Für große |x| bestimmt nur der Summand mit dem höchsten Exponenten den Verlauf.",
         "Nur gerade Exponenten: achsensymmetrisch zur y-Achse. Nur ungerade: punktsymmetrisch zum Ursprung.",
         "Nullstellen: Linearfaktorform ablesen, x ausklammern oder bei x⁴ und x² mit z = x² substituieren."],
        [example("f(x) = x³ − 4x", ["x(x² − 4) = 0", "x = 0 oder x² = 4"], "x = −2; x = 0; x = 2"),
         example("f(x) = x⁴ − 5x² + 4", ["z² − 5z + 4 = 0 ⇒ z = 1 oder z = 4"], "x = −2; x = −1; x = 1; x = 2")],
        [["f(x) = (x − 3)(x + 1): x = −3", "x − 3 = 0 ⇒ x = 3"],
         ["x³ − 4x = 0 ⇒ x² = 4, nur ±2", "Auch x = 0 ist Nullstelle"],
         ["x⁴ + x² + 1 ist punktsymmetrisch", "Nur gerade Exponenten: Achsensymmetrie"]])
    faq = [
        {"q": "Was ist der Grad einer Polynomfunktion?", "a": "Der höchste Exponent von x, z. B. Grad 3 bei f(x) = 2x³ − x + 5."},
        {"q": "Wie erkenne ich das Verhalten im Unendlichen?", "a": "Am Grad (gerade oder ungerade) und am Vorzeichen des Leitkoeffizienten."},
        {"q": "Wie finde ich die Nullstellen von x³ − 4x?", "a": "x ausklammern: x(x² − 4) = 0, also x = 0, x = 2 und x = −2."},
        {"q": "Was ist eine doppelte Nullstelle?", "a": "Ein Linearfaktor kommt quadratisch vor; der Graph berührt dort die x-Achse, ohne sie zu schneiden."},
    ]
    make_unit(R, "polynomfunktionen", "F",
              "Die Schülerinnen und Schüler untersuchen ganzrationale Funktionen: Grad und Leitkoeffizient, Verhalten im Unendlichen, Symmetrie, Nullstellen (Linearfaktoren, Ausklammern, Substitution) und Graphen (Zusammenfassung).",
              "Polynomfunktionen (ganzrationale Funktionen)",
              "Polynomfunktionen Klasse 10 – Nullstellen, Symmetrie, Verhalten im Unendlichen, Arbeitsblätter mit Lösungen",
              "Polynomfunktionen",
              "Polynomfunktionen für Klasse 10: Grad, Leitkoeffizient, Verhalten im Unendlichen, Symmetrie, Nullstellen mit Linearfaktoren, Ausklammern und Substitution, Graphen. 100 Aufgaben mit Lösungen, kostenlos.",
              "f(x) = aₙxⁿ + … + a₁x + a₀",
              "Der Summand mit dem höchsten Exponenten bestimmt den Verlauf.",
              body, faq, sets, 5, grade="klasse-10")


if __name__ == "__main__":
    main()
