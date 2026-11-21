# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 10: Sinus- und Kosinusfunktion（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k10_sinus_und_kosinusfunktion.py
f(x) = sin x und cos x im Bogenmaß, Funktionswerte, Nullstellen, Hoch- und Tiefpunkte, Periode 2π,
f(x) = a · sin(b · x) + d: Amplitude |a|, Periode 2π/b, Wertebereich, Verschiebung, Graphen zuordnen, Modelle (Gezeiten, Riesenrad, Tageslänge).
Fehler: Periode b statt 2π/b, Amplitude = a + d, Nullstellen von cos bei kπ, Wertebereich ohne d.
"""
import random, math
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, num, BLUE, RED
from de_k6 import bh, dz
from de_k10 import mcq, zr, kurve, pi_txt

R = random.Random(50008)
M = "−"
PI = math.pi
NB = " "


def zz(v):
    v = Fr(v)
    if v < 0:
        return M + zz(-v)
    return dz(v) if v.denominator in (1, 2, 4, 5) else bh(v)


def fterm(a=1, b=1, d=0, fn="sin", c=0):
    a, b, d = Fr(a), Fr(b), Fr(d)
    pre = "" if a == 1 else (M if a == -1 else zz(a) + NB + MAL + NB)
    if c:
        arg = "x%s%s%s%s" % (NB, M if c > 0 else "+", NB, pi_txt(abs(Fr(c))))
        arg = ("%s%s(%s)" % (zz(b), NB + MAL + NB, arg)) if b != 1 else arg
    else:
        arg = "x" if b == 1 else "%sx" % zz(b) if b.denominator == 1 else "%sx" % bh(b)
    s = "%s%s(%s)" % (pre, fn, arg)
    if d:
        s += " %s %s" % ("+" if d > 0 else M, zz(abs(d)))
    return "f(x) = " + s


def xlab(k):
    return pi_txt(Fr(round(k / (PI / 2)), 2))


def werte():
    fn = R.choice(["sin", "cos"])
    k = R.choice(range(-4, 9))
    x = Fr(k, 2)
    if R.random() < 0.3:
        k6 = R.choice([1, 5, 7, 11, 2, 4])
        x = Fr(k6, 6)
    v = math.sin(float(x) * PI) if fn == "sin" else math.cos(float(x) * PI)
    tab = {0: "0", 1: "1", -1: M + "1", 0.5: "½", -0.5: M + "½", round(math.sqrt(3) / 2, 6): "½√3", -round(math.sqrt(3) / 2, 6): M + "½√3"}
    vs = tab.get(round(v, 6) if abs(round(v, 6)) not in (0.5, 1) else round(v, 1))
    if vs is None:
        vs = tab.get(round(v, 6))
    if vs is None:
        return None
    oth = math.cos(float(x) * PI) if fn == "sin" else math.sin(float(x) * PI)
    os_ = tab.get(round(oth, 6) if abs(round(oth, 6)) not in (0.5, 1) else round(oth, 1))
    w = [os_ if os_ and os_ != vs else ("1" if vs != "1" else "0"), (vs[1:] if vs.startswith(M) else (M + vs if vs != "0" else M + "1")), R.choice([t for t in ["½", M + "½", "½√3", M + "½√3", "0", "1", M + "1"] if t != vs and t != os_ and t != (vs[1:] if vs.startswith(M) else M + vs)])]
    return mcq("Berechne %s(%s) exakt." % (fn, pi_txt(x)), vs, w, "x = %s entspricht %s°: <b>%s(%s) = %s</b>." % (pi_txt(x), zr(float(x) * 180, 0), fn, pi_txt(x), vs))


def eigen():
    fn = R.choice(["sin", "cos"])
    kind = R.choice(["null", "hoch", "tief", "per", "wb", "sym"])
    if kind == "null":
        ans = "x = 0; π; 2π" if fn == "sin" else "x = π/2; 3π/2"
        return mcq("Welche Nullstellen hat f(x) = %s x im Intervall [0; 2π]?" % fn, ans, ["x = π/2; 3π/2" if fn == "sin" else "x = 0; π; 2π", "x = π", "x = 0; 2π"],
                   "%s x = 0 an den Stellen <b>%s</b>." % (fn, ans))
    if kind == "hoch":
        ans = "H(π/2 | 1)" if fn == "sin" else "H(0 | 1) und H(2π | 1)"
        return mcq("Wo hat f(x) = %s x im Intervall [0; 2π] Hochpunkte?" % fn, ans, ["H(π | 1)", "H(3π/2 | 1)" if fn == "sin" else "H(π/2 | 1)", "H(0 | 1) und H(2π | 1)" if fn == "sin" else "H(π/2 | 1) und H(3π/2 | 1)"],
                   "Der größte Wert ist 1: <b>%s</b>." % ans)
    if kind == "tief":
        ans = "T(3π/2 | −1)" if fn == "sin" else "T(π | −1)"
        return mcq("Wo hat f(x) = %s x im Intervall [0; 2π] einen Tiefpunkt?" % fn, ans, ["T(π | −1)" if fn == "sin" else "T(3π/2 | −1)", "T(π/2 | −1)", "T(2π | −1)"],
                   "Der kleinste Wert ist −1: <b>%s</b>." % ans)
    if kind == "per":
        return mcq("Welche Periode hat f(x) = %s x?" % fn, "2π", ["π", "360", "1"], "Nach einer vollen Umdrehung (2π) wiederholen sich die Werte: <b>2π</b>.")
    if kind == "wb":
        return mcq("Welchen Wertebereich hat f(x) = %s x?" % fn, "W = [−1; 1]", ["W = ℝ", "W = [0; 1]", "W = [−2π; 2π]"],
                   "Am Einheitskreis liegen sin und cos zwischen −1 und 1: <b>W = [−1; 1]</b>.")
    ans = "punktsymmetrisch zum Ursprung" if fn == "sin" else "achsensymmetrisch zur y-Achse"
    return mcq("Welche Symmetrie hat der Graph von f(x) = %s x?" % fn, "Er ist %s." % ans, ["Er ist %s." % v for v in ["achsensymmetrisch zur y-Achse" if fn == "sin" else "punktsymmetrisch zum Ursprung", "achsensymmetrisch zur x-Achse", "nicht symmetrisch"]],
               "%s: <b>%s</b>." % ("sin(−x) = −sin x" if fn == "sin" else "cos(−x) = cos x", ans))


def verschieb():
    fn = R.choice(["sin", "cos"])
    c = Fr(R.choice([1, 2, 3, 4, 6]), R.choice([1, 2, 3, 4, 6])) * R.choice([1, -1])
    if abs(c) >= 2 or c.denominator not in (1, 2, 3, 4, 6):
        return None
    kind = R.choice(["r", "r", "n"])
    f = fterm(1, 1, 0, fn, c)
    if kind == "r":
        ans = "um %s nach %s" % (pi_txt(abs(c)), "rechts" if c > 0 else "links")
        return mcq("Wie geht der Graph von %s aus dem Graphen von %s x hervor?" % (f, fn), "Verschiebung " + ans,
                   ["Verschiebung um %s nach %s" % (pi_txt(abs(c)), "links" if c > 0 else "rechts"), "Verschiebung um %s nach oben" % pi_txt(abs(c)), "Streckung mit dem Faktor %s" % pi_txt(abs(c))],
                   "x − c verschiebt um c nach rechts, x + c nach links: <b>Verschiebung %s</b>." % ans)
    k = R.randint(1, 4)
    n = 2 * k + 1
    return mcq("Wie viele Nullstellen hat f(x) = %s x im Intervall [0; %s]?" % (fn, pi_txt(2 * k)), str(2 * k + 1 if fn == "sin" else 2 * k),
               [str(2 * k if fn == "sin" else 2 * k + 1), str(k), str(4 * k)], "Pro Periode 2π gibt es zwei Nullstellen%s: <b>%d</b>." % (", dazu der Rand x = 0" if fn == "sin" else "", 2 * k + 1 if fn == "sin" else 2 * k))


def param():
    fn = R.choice(["sin", "cos"])
    a = Fr(R.choice([1, 2, 3, 4, Fr(1, 2), Fr(3, 2), -2, -3]))
    b = Fr(R.choice([1, 2, 3, 4, Fr(1, 2), Fr(1, 3)]))
    d = Fr(R.choice([0, 0, 1, 2, -1, 3]))
    if a == 1 and b == 1 and d == 0:
        return None
    f = fterm(a, b, d, fn)
    kind = R.choice(["amp", "per", "per", "wb", "max"])
    if kind == "amp":
        return mcq("Wie groß ist die Amplitude von %s?" % f, zz(abs(a)), [zz(abs(a) + d) if d else zz(2 * abs(a)), zz(b) if b != abs(a) else zz(abs(a) + 1), zz(2 * abs(a)) if d else zz(abs(a) + 1)],
                   "Die Amplitude ist |a| = <b>%s</b>." % zz(abs(a)))
    if kind == "per":
        p = 2 / b
        return mcq("Welche Periode hat %s?" % f, pi_txt(p), [pi_txt(b) if b != p else pi_txt(p * 2), pi_txt(2 * b) if 2 * b != p else pi_txt(p / 2), zz(b) if b != 1 else "π"],
                   "p = 2π : b = 2π : %s = <b>%s</b>." % (zz(b), pi_txt(p)))
    if kind == "wb":
        lo, hi = d - abs(a), d + abs(a)
        return mcq("Welchen Wertebereich hat %s?" % f, "W = [%s; %s]" % (zz(lo), zz(hi)), ["W = [%s; %s]" % (zz(-abs(a)), zz(abs(a))) if d else "W = [%s; %s]" % (zz(-1), zz(1)), "W = [%s; %s]" % (zz(d), zz(hi)), "W = [%s; %s]" % (zz(lo - b), zz(hi + b)) if b != 0 else "W = ℝ"],
                   "Mittellinie y = %s, Amplitude %s: <b>W = [%s; %s]</b>." % (zz(d), zz(abs(a)), zz(lo), zz(hi)))
    return mcq("Wie groß ist der größte Funktionswert von %s?" % f, zz(d + abs(a)), [zz(abs(a)) if d else zz(2 * abs(a)), zz(d + 1) if d + 1 != d + abs(a) else zz(d + 2 * abs(a)), zz(d + abs(a) * b) if d + abs(a) * b != d + abs(a) else zz(d + abs(a) + 1), zz(d - abs(a)), zz(d)],
               "Größter Wert = d + |a| = %s + %s = <b>%s</b>." % (zz(d), zz(abs(a)), zz(d + abs(a))))


def graph():
    fn = R.choice(["sin", "cos"])
    a = Fr(R.choice([1, 2, 3, -1, -2, Fr(1, 2)]))
    b = Fr(R.choice([1, 1, 2, Fr(1, 2)]))
    d = Fr(R.choice([0, 0, 1, -1]))
    if abs(a) + abs(d) > 3:
        return None
    F = (lambda x: float(a) * math.sin(float(b) * x) + float(d)) if fn == "sin" else (lambda x: float(a) * math.cos(float(b) * x) + float(d))
    pic = kurve([(F, BLUE, "")], (0, 2 * PI, PI / 2), (-3, 3, 1), W=360, H=270, label="Graph einer trigonometrischen Funktion", xlab=xlab)
    ans = fterm(a, b, d, fn)
    alts = set()
    for aa, bb, dd, ff in [(a, b, d, "cos" if fn == "sin" else "sin"), (-a, b, d, fn), (a, b * 2 if b != 2 else Fr(1, 2), d, fn), (a * 2 if abs(a) < 2 else a / 2, b, d, fn), (a, b, -d if d else 1, fn)]:
        alts.add(fterm(aa, bb, dd, ff))
    alts.discard(ans)
    w = R.sample(sorted(alts), 3)
    return mcq(pic + "Welche Funktionsgleichung gehört zum Graphen?", ans, w,
               "Mittellinie y = %s, Amplitude %s, Periode %s, Start bei x = 0 %s: <b>%s</b>." % (
                   zz(d), zz(abs(a)), pi_txt(2 / b), ("auf der Mittellinie" + (" steigend" if a > 0 else " fallend")) if fn == "sin" else ("im Hochpunkt" if a > 0 else "im Tiefpunkt"), ans))


def modell():
    kind = R.choice(["gez", "gez", "rad", "tag", "aufstellen"])
    if kind == "gez":
        a = R.choice([Fr(3, 2), Fr(2), Fr(5, 2), Fr(3), Fr(4)])
        d = R.choice([4, 5, 6])
        T = R.choice([12, Fr(25, 2)])
        q = R.choice(["max", "min", "per", "wert"])
        b = Fr(2, 1) / T
        f = "h(t) = %s %s sin(%sπ/%s %s t) + %d" % (zz(a), MAL, "2", zz(T) if Fr(T).denominator == 1 else "12,5", MAL, d)
        base = "Der Wasserstand in einem Hafen wird durch %s beschrieben (t in Stunden, h in m). " % f
        if q == "max":
            return mcq(base + "Wie hoch ist das Wasser bei Flut höchstens?", "%s m" % zz(d + a), ["%s m" % zz(a), "%s m" % zz(d), "%s m" % zz(d + 2 * a)], "h<sub>max</sub> = %d + %s = <b>%s m</b>." % (d, zz(a), zz(d + a)))
        if q == "min":
            return mcq(base + "Wie hoch ist das Wasser bei Ebbe?", "%s m" % zz(d - a), ["%s m" % zz(-a), "%s m" % zz(d), "%s m" % zz(a)], "h<sub>min</sub> = %d − %s = <b>%s m</b>." % (d, zz(a), zz(d - a)))
        if q == "per":
            return mcq(base + "Nach wie vielen Stunden wiederholt sich der Wasserstand?", "nach %s h" % zz(T), ["nach %s h" % zz(Fr(T) / 2), "nach %s h" % zz(Fr(T) * 2), "nach %s h" % zr(2 * PI / (2 * PI / float(T)) * PI, 1)],
                       "Periode 2π : (2π/%s) = <b>%s h</b>." % (zz(T), zz(T)))
        tt = R.choice([3, 6, 9]) if T == 12 else R.choice([Fr(25, 8), Fr(25, 4)])
        v = d + float(a) * math.sin(2 * PI / float(T) * float(tt))
        return mcq(base + "Wie hoch ist das Wasser nach %s Stunden (auf eine Nachkommastelle)?" % zz(tt), "≈ %s m" % zr(v, 1),
                   ["≈ %s m" % zr(d + float(a) * math.sin(float(tt)), 1), "≈ %s m" % zr(float(a) * math.sin(2 * PI / float(T) * float(tt)), 1), "≈ %s m" % zr(d + float(a) * math.cos(2 * PI / float(T) * float(tt)), 1)],
                   "h(%s) = %d + %s %s sin(%s) ≈ <b>%s m</b>." % (zz(tt), d, zz(a), MAL, pi_txt(Fr(2) * Fr(tt) / Fr(T)), zr(v, 1)))
    if kind == "rad":
        r = R.choice([10, 15, 20, 25])
        h0 = r + R.choice([2, 3, 5])
        T = R.choice([10, 12, 15, 20])
        q = R.choice(["max", "min", "per"])
        f = "h(t) = %d %s sin(2π/%d %s t) + %d" % (r, MAL, T, MAL, h0)
        base = "Die Höhe einer Gondel im Riesenrad ist %s (t in min, h in m). " % f
        if q == "max":
            return mcq(base + "Welche größte Höhe erreicht die Gondel?", "%d m" % (h0 + r), ["%d m" % r, "%d m" % h0, "%d m" % (h0 + 2 * r)], "%d + %d = <b>%d m</b>." % (h0, r, h0 + r))
        if q == "min":
            return mcq(base + "Wie hoch ist die Gondel an der tiefsten Stelle?", "%d m" % (h0 - r), ["0 m", "%d m" % h0, "%d m" % r], "%d − %d = <b>%d m</b>." % (h0, r, h0 - r))
        return mcq(base + "Wie lange dauert eine Umdrehung?", "%d min" % T, ["%s min" % zr(2 * PI / T, 2), "%d min" % (2 * T), "%d min" % (T // 2) if T % 2 == 0 else "%s min" % zr(T / 2, 1)],
                   "Periode 2π : (2π/%d) = <b>%d min</b>." % (T, T))
    if kind == "tag":
        d = 12
        a = R.choice([3, 4, Fr(9, 2), 5])
        q = R.choice(["max", "min", "diff"])
        base = "Die Tageslänge in einer Stadt wird durch L(t) = %s %s sin(2π/365 %s (t − 80)) + 12 beschrieben (t = Tag des Jahres, L in Stunden). " % (zz(a), MAL, MAL)
        if q == "max":
            return mcq(base + "Wie lang ist der längste Tag?", "%s h" % zz(d + a), ["%s h" % zz(a), "%s h" % zz(d), "%s h" % zz(d + 2 * a)], "12 + %s = <b>%s h</b>." % (zz(a), zz(d + a)))
        if q == "min":
            return mcq(base + "Wie lang ist der kürzeste Tag?", "%s h" % zz(d - a), ["%s h" % zz(d), "%s h" % zz(a), "%s h" % zz(d - 2 * a)], "12 − %s = <b>%s h</b>." % (zz(a), zz(d - a)))
        return mcq(base + "Um wie viele Stunden unterscheiden sich der längste und der kürzeste Tag?", "%s h" % zz(2 * a), ["%s h" % zz(a), "%s h" % zz(d), "%s h" % zz(d + a)],
                   "(12 + %s) − (12 − %s) = 2 %s %s = <b>%s h</b>." % (zz(a), zz(a), MAL, zz(a), zz(2 * a)))
    hi = R.choice([5, 6, 8, 10, 12])
    lo = R.choice([v for v in (0, 1, 2, 4) if v < hi - 1])
    a, d = Fr(hi - lo, 2), Fr(hi + lo, 2)
    T = R.choice([4, 6, 8, 12, 24])
    ans = "f(t) = %s %s sin(%s %s t) + %s" % (zz(a), MAL, pi_txt(Fr(2, T)), MAL, zz(d))
    return mcq("Eine Größe schwankt sinusförmig zwischen %d und %d mit der Periode %d. Sie startet zur Zeit t = 0 auf der Mittellinie und steigt. Welche Gleichung passt?" % (lo, hi, T), ans,
               ["f(t) = %s %s sin(%s %s t) + %s" % (zz(hi - lo), MAL, pi_txt(Fr(2, T)), MAL, zz(d)), "f(t) = %s %s sin(%d %s t) + %s" % (zz(a), MAL, T, MAL, zz(d)), "f(t) = %s %s sin(%s %s t) + %s" % (zz(a), MAL, pi_txt(Fr(2, T)), MAL, zz(lo)) if lo != 0 else "f(t) = %s %s sin(%s %s t)" % (zz(a), MAL, pi_txt(Fr(2, T)), MAL)],
               "a = (%d − %d) : 2 = %s, d = (%d + %d) : 2 = %s, b = 2π : %d = %s: <b>%s</b>." % (hi, lo, zz(a), hi, lo, zz(d), T, pi_txt(Fr(2, T)), ans))


def main():
    seen = set()
    sets = [
        ("Funktionswerte im Bogenmaß", mix(R, seen, [(werte, 20)])),
        ("Eigenschaften und Verschiebung", mix(R, seen, [(eigen, 12), (verschieb, 8)])),
        ("Amplitude, Periode, Wertebereich", mix(R, seen, [(param, 20)])),
        ("Graphen zuordnen", mix(R, seen, [(graph, 20)])),
        ("Periodische Vorgänge", mix(R, seen, [(modell, 20)])),
    ]
    body = lesson(
        ["Die <b>Sinusfunktion</b> f(x) = sin x und die <b>Kosinusfunktion</b> f(x) = cos x ordnen jedem x (im Bogenmaß) den Sinus- bzw. Kosinuswert zu.",
         "Beide haben die Periode 2π, den Wertebereich [−1; 1] und die Amplitude 1. sin x hat Nullstellen bei 0, π, 2π …, cos x bei π/2, 3π/2 …",
         "f(x) = a %s sin(b %s x) + d: Amplitude |a|, Periode 2π/b, Mittellinie y = d, Wertebereich [d − |a|; d + |a|]." % (MAL, MAL)],
        [example("f(x) = 3 %s sin(2x) + 1" % MAL, ["Amplitude 3", "Periode 2π : 2 = π", "W = [1 − 3; 1 + 3]"], "W = [−2; 4]"),
         example("sin(3π/2)", ["3π/2 entspricht 270°"], "−1")],
        [["sin(2x): Periode 2", "Periode 2π : 2 = π"],
         ["3 %s sin x + 1: Amplitude 4" % MAL, "Amplitude 3, nur |a| zählt"],
         ["cos x = 0 bei x = 0", "cos 0 = 1, Nullstellen bei π/2 und 3π/2"]])
    faq = [
        {"q": "Welche Periode hat sin(bx)?", "a": "2π : b. Zum Beispiel hat sin(2x) die Periode π."},
        {"q": "Was ist die Amplitude?", "a": "Der Abstand vom Hoch- oder Tiefpunkt zur Mittellinie; bei a · sin x ist sie |a|."},
        {"q": "Wie hängen sin und cos zusammen?", "a": "Der Graph von cos ist der um π/2 nach links verschobene Graph von sin: cos x = sin(x + π/2)."},
        {"q": "Warum rechnet man im Bogenmaß?", "a": "Damit x eine reelle Zahl ist und man die Funktionen wie andere Funktionen zeichnen und verknüpfen kann."},
    ]
    make_unit(R, "sinus-und-kosinusfunktion", "F",
              "Die Schülerinnen und Schüler untersuchen Sinus- und Kosinusfunktion im Bogenmaß, deuten die Parameter a, b und d (Amplitude, Periode, Verschiebung) und beschreiben periodische Vorgänge (Zusammenfassung).",
              "Sinus- und Kosinusfunktion",
              "Sinusfunktion Klasse 10 – Amplitude, Periode, Graphen, Arbeitsblätter mit Lösungen",
              "Sinus- und Kosinusfunktion",
              "Sinus- und Kosinusfunktion für Klasse 10: Funktionswerte im Bogenmaß, Nullstellen und Extrempunkte, Amplitude, Periode, Wertebereich, Graphen und periodische Vorgänge. 100 Aufgaben mit Lösungen, kostenlos.",
              "f(x) = a · sin(b · x) + d",
              "Amplitude |a|, Periode 2π/b, Mittellinie y = d.",
              body, faq, sets, 8, grade="klasse-10")


if __name__ == "__main__":
    main()
