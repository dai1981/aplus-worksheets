# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 8: Lineare Gleichungssysteme grafisch lösen（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k8_lineare_gleichungssysteme_grafisch_loesen.py
Lösung eines Gleichungssystems prüfen, Gleichungen nach y umstellen, Schnittpunkt zweier Geraden ablesen,
Anzahl der Lösungen (ein Schnittpunkt, parallel, identisch), Sachaufgaben mit zwei Graphen.
Fehler: nur eine Gleichung geprüft, beim Umstellen das Vorzeichen nicht gewechselt, x und y beim Ablesen vertauscht, parallele Geraden mit „unendlich viele Lösungen“ verwechselt.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, BLUE, RED, GREEN
from de_k6 import bh, dz
from de_k8 import mcq, expr, gl, par, kosy

R = random.Random(49807)
G = ":"


def zahl(v):
    v = Fr(v)
    return bh(v) if v.denominator != 1 else dz(v)


def lgs(e1, e2, end="<br>"):
    return "I: %s<br>II: %s%s" % (e1, e2, end)


def eq(a, b, c):
    """ax + by = c"""
    return "%s = %s" % (expr([(a, "x"), (b, "y")]), zahl(c))


def pruefen():
    x, y = R.randint(-4, 6), R.randint(-4, 6)
    a1, b1, a2, b2 = [R.choice([-3, -2, -1, 1, 2, 3, 4]) for _ in range(4)]
    if a1 * b2 == a2 * b1:
        return None
    c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
    kind = R.choice(["ja", "nein1", "nein2"])
    px, py = x, y
    if kind == "nein1":
        px, py = y, x
        if (px, py) == (x, y):
            return None
    if kind == "nein2":
        # erfüllt I, aber nicht II
        if b1 == 0:
            return None
        px = x + b1
        py = y - a1
    ok1 = a1 * px + b1 * py == c1
    ok2 = a2 * px + b2 * py == c2
    if kind != "ja" and ok1 and ok2:
        return None
    ans = "Ja, beide Gleichungen sind erfüllt." if ok1 and ok2 else ("Nein, nur Gleichung I ist erfüllt." if ok1 else ("Nein, nur Gleichung II ist erfüllt." if ok2 else "Nein, keine Gleichung ist erfüllt."))
    opts = ["Ja, beide Gleichungen sind erfüllt.", "Nein, nur Gleichung I ist erfüllt.", "Nein, nur Gleichung II ist erfüllt.", "Nein, keine Gleichung ist erfüllt."]
    return mcq(lgs(eq(a1, b1, c1), eq(a2, b2, c2)) + "Ist (%s | %s) eine Lösung des Gleichungssystems?" % (dz(px), dz(py)), ans, [o for o in opts if o != ans],
               "I: %s = %s%s. II: %s = %s%s. <b>%s</b>" % ("%s %s %s + %s %s %s" % (zahl(a1), MAL, par(px), par(b1), MAL, par(py)), zahl(a1 * px + b1 * py), "" if ok1 else " ≠ %s" % zahl(c1),
                                                       "%s %s %s + %s %s %s" % (zahl(a2), MAL, par(px), par(b2), MAL, par(py)), zahl(a2 * px + b2 * py), "" if ok2 else " ≠ %s" % zahl(c2), ans))


def umstellen():
    a = R.choice([-4, -3, -2, -1, 1, 2, 3, 4, 5])
    b = R.choice([1, 1, 2, 3, -1, 4])
    c = R.randint(-12, 12)
    m, n = Fr(-a, b), Fr(c, b)
    return mcq("Stelle nach y um: %s" % eq(a, b, c), gl(m, n), [gl(-m, n), gl(m, -n) if n else gl(m, 1), gl(Fr(-a), c) if b != 1 else gl(Fr(a), -c) if c else gl(-m, 1)],
               "%s auf beiden Seiten%s: <b>%s</b>." % (("− %s" % expr([(a, "x")])) if a > 0 else ("+ %s" % expr([(-a, "x")])), (", dann durch %s teilen" % zahl(b)) if b != 1 else "", gl(m, n)))


def ablesen():
    x, y = R.randint(-3, 3), R.randint(-3, 3)
    m1, m2 = R.sample([-2, -1, Fr(-1, 2), Fr(1, 2), 1, 2, 3], 2)
    m1, m2 = Fr(m1), Fr(m2)
    b1, b2 = y - m1 * x, y - m2 * x
    if m1 * m2 > 0 and abs(m1 - m2) < Fr(3, 2):
        return None
    if abs(b1) > 5 or abs(b2) > 5 or b1.denominator != 1 or b2.denominator != 1:
        return None
    pic = kosy([(m1, b1, BLUE, "g"), (m2, b2, RED, "h")], label="Zwei Geraden g und h")
    kind = R.choice(["s", "s", "gl"])
    if kind == "s":
        return mcq(pic + "Lies die Lösung des Gleichungssystems aus dem Schnittpunkt von g und h ab.", "x = %s, y = %s" % (dz(x), dz(y)),
                   ["x = %s, y = %s" % (dz(y), dz(x)) if x != y else "x = %s, y = %s" % (dz(x + 1), dz(y)), "x = 0, y = %s" % zahl(b1) if (0, b1) != (x, y) else "x = %s, y = %s" % (dz(x), dz(y - 1)), "x = %s, y = %s" % (dz(-x), dz(y)) if x else "x = 1, y = %s" % dz(y)],
                   "Die Geraden schneiden sich in S(%s | %s): <b>x = %s, y = %s</b>." % (dz(x), dz(y), dz(x), dz(y)))
    return mcq(pic + "Zu welchem Gleichungssystem gehört die Zeichnung?", lgs(gl(m1, b1), gl(m2, b2), ""),
               [lgs(gl(m1, -b1) if b1 else gl(m1, 1), gl(m2, b2), ""), lgs(gl(-m1, b1), gl(-m2, b2), ""), lgs(gl(m1, b2), gl(m2, b1), "") if b1 != b2 else lgs(gl(m1, b1 + 1), gl(m2, b2 - 1), "")],
               "g: y-Achsenabschnitt %s, Steigung %s. h: y-Achsenabschnitt %s, Steigung %s. <b>%s und %s</b>" % (zahl(b1), zahl(m1), zahl(b2), zahl(m2), gl(m1, b1), gl(m2, b2)))


def anzahl():
    m = Fr(R.choice([-3, -2, -1, Fr(1, 2), 1, 2, 3]))
    b = Fr(R.randint(-5, 5))
    kind = R.choice(["eine", "keine", "unendlich", "keine", "unendlich"])
    if kind == "eine":
        m2 = m + R.choice([-2, -1, 1, 2])
        e2 = gl(m2, R.randint(-5, 5))
        ans = "genau eine Lösung"
        why = "Verschiedene Steigungen: Die Geraden schneiden sich in genau einem Punkt."
    elif kind == "keine":
        e2 = gl(m, b + R.choice([-3, -2, -1, 1, 2, 3]))
        ans = "keine Lösung"
        why = "Gleiche Steigung, verschiedener y-Achsenabschnitt: Die Geraden sind parallel und schneiden sich nie."
    else:
        k = R.choice([2, 3, -1, -2])
        if m.denominator != 1:
            return None
        e2 = "%s = %s" % (expr([(-k * m, "x"), (k, "y")]), zahl(k * b))
        ans = "unendlich viele Lösungen"
        why = "Nach y umgestellt ergibt II dieselbe Gerade %s. Alle Punkte der Geraden sind Lösungen." % gl(m, b)
    opts = ["genau eine Lösung", "keine Lösung", "unendlich viele Lösungen", "genau zwei Lösungen"]
    return mcq(lgs(gl(m, b), e2) + "Wie viele Lösungen hat das Gleichungssystem?", ans, [o for o in opts if o != ans], "%s <b>%s</b>" % (why, ans.capitalize()))


def sache():
    kind = R.choice(["tarif", "tarif", "wandern", "begriff"])
    if kind == "tarif":
        x = R.choice([2, 4, 6, 8])
        mA, mB = sorted(R.sample([Fr(1, 2), 1, 2, Fr(3, 2), 3], 2), reverse=True)
        mA, mB = Fr(mA), Fr(mB)
        bA = Fr(R.choice([0, 1, 2]))
        bB = bA + (mA - mB) * x
        if bB.denominator != 1 or bB > 8 or bA + mA * x > 8 or mA - mB < 1:
            return None
        pic = kosy([(mA, bA, BLUE, "A"), (mB, bB, RED, "B")], lo=0, hi=10, u=22, label="Kosten der Tarife A und B (x: Stunden, y: Euro)")
        kind2 = R.choice(["gleich", "guenstig"])
        if kind2 == "gleich":
            return mcq(pic + "Die Grafik zeigt die Kosten y (in €) zweier Tarife A und B nach x Stunden. Nach wie vielen Stunden kosten beide gleich viel?", "nach %d Stunden" % x,
                       ["nach %s Stunden" % zahl(bA + mA * x), "nach %s Stunden" % zahl(bB), "nach %d Stunden" % (x + 2)],
                       "Die Geraden schneiden sich bei x = %d (y = %s €). <b>nach %d Stunden</b>" % (x, zahl(bA + mA * x), x))
        return mcq(pic + "Die Grafik zeigt die Kosten y (in €) zweier Tarife A und B nach x Stunden. Welcher Tarif ist für %d Stunden günstiger?" % (x + 2), "Tarif B",
                   ["Tarif A", "Beide kosten gleich viel.", "Das kann man nicht ablesen."],
                   "Rechts vom Schnittpunkt (x = %d) liegt B unter A: <b>Tarif B</b>." % x)
    if kind == "wandern":
        v1, v2 = R.choice([(4, 6), (3, 5), (4, 5), (5, 7)])
        d = R.choice([2, 4, 6])
        t = Fr(d, v2 - v1)
        return mcq("Anna startet %d km vor Ben und geht %d km/h. Ben läuft %d km/h hinterher. Die Wege werden durch y = %s und y = %s beschrieben (x in h, y in km). Wann holt Ben Anna ein?" % (d, v1, v2, expr([(v1, "x"), (d, "")]), expr([(v2, "x")])),
                   "nach %s h" % zahl(t), ["nach %s h" % zahl(Fr(d, v1)), "nach %s h" % zahl(Fr(d, v2)) if Fr(d, v2) != t else "nach %s h" % zahl(t + 1), "nach %s h" % zahl(Fr(d, v1 + v2))],
                   "Gleichsetzen: %dx = %s, also %s = %d und <b>x = %s h</b>." % (v2, expr([(v1, "x"), (d, "")]), expr([(v2 - v1, "x")]), d, zahl(t)))
    q, a, w = R.choice([
        ("Was bedeutet der Schnittpunkt zweier Geraden für das Gleichungssystem?", "Seine Koordinaten erfüllen beide Gleichungen.", ["Er erfüllt nur die erste Gleichung.", "Er ist immer der Ursprung.", "Er zeigt die Steigung an."]),
        ("Warum ist die grafische Lösung manchmal ungenau?", "Man kann Schnittpunkte mit Brüchen nur schätzen.", ["Weil Geraden gebogen sind.", "Weil es immer zwei Schnittpunkte gibt.", "Weil man die y-Achse nicht ablesen kann."]),
        ("Zwei Geraden sind parallel und verschieden. Was gilt?", "Das Gleichungssystem hat keine Lösung.", ["Das Gleichungssystem hat genau eine Lösung.", "Das Gleichungssystem hat unendlich viele Lösungen.", "Die Lösung ist x = 0."]),
        ("Zwei Gleichungen beschreiben dieselbe Gerade. Was gilt?", "Es gibt unendlich viele Lösungen.", ["Es gibt keine Lösung.", "Es gibt genau eine Lösung.", "Es gibt genau zwei Lösungen."]),
    ])
    return mcq(q, a, w, "<b>%s</b>" % a)


def main():
    seen = set()
    sets = [
        ("Lösungen prüfen", mix(R, seen, [(pruefen, 20)])),
        ("Nach y umstellen", mix(R, seen, [(umstellen, 20)])),
        ("Schnittpunkt ablesen", mix(R, seen, [(ablesen, 20)])),
        ("Anzahl der Lösungen", mix(R, seen, [(anzahl, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Ein <b>lineares Gleichungssystem</b> besteht aus zwei Gleichungen mit zwei Variablen x und y. Eine Lösung ist ein Zahlenpaar, das <b>beide</b> Gleichungen erfüllt.",
         "Grafisch: Beide Gleichungen nach y umstellen, die Geraden zeichnen und den <b>Schnittpunkt</b> ablesen.",
         "Verschiedene Steigungen: genau eine Lösung. Gleiche Steigung, anderes b: parallel, keine Lösung. Gleiche Gerade: unendlich viele Lösungen."],
        [example("I: y = 2x − 1, II: y = −x + 5", ["Schnittpunkt S(2 | 3)", "Probe: 2 %s 2 − 1 = 3, −2 + 5 = 3" % MAL], "x = 2, y = 3"),
         example("3x + y = 7 nach y", ["− 3x"], "y = −3x + 7")],
        [["(2 | 3) erfüllt I, also Lösung", "Beide Gleichungen prüfen"],
         ["2x + y = 5 → y = 2x + 5", "Vorzeichen wechselt: y = −2x + 5"],
         ["Parallele Geraden: unendlich viele Lösungen", "Parallel und verschieden: keine Lösung"]])
    faq = [
        {"q": "Wie löse ich ein Gleichungssystem grafisch?", "a": "Stelle beide Gleichungen nach y um, zeichne beide Geraden und lies den Schnittpunkt ab. Seine Koordinaten sind die Lösung."},
        {"q": "Wann hat ein Gleichungssystem keine Lösung?", "a": "Wenn die beiden Geraden parallel sind, also die gleiche Steigung, aber verschiedene y-Achsenabschnitte haben."},
        {"q": "Wann gibt es unendlich viele Lösungen?", "a": "Wenn beide Gleichungen dieselbe Gerade beschreiben. Dann ist jeder Punkt der Geraden eine Lösung."},
        {"q": "Wie prüfe ich eine Lösung?", "a": "Setze x und y in beide Gleichungen ein. Nur wenn beide stimmen, ist das Zahlenpaar eine Lösung."},
    ]
    make_unit(R, "lineare-gleichungssysteme-grafisch-loesen", "F",
              "Die Schülerinnen und Schüler prüfen Lösungen linearer Gleichungssysteme mit zwei Variablen, lösen sie grafisch über den Schnittpunkt zweier Geraden und entscheiden über die Anzahl der Lösungen (Zusammenfassung).",
              "Lineare Gleichungssysteme grafisch lösen",
              "Lineare Gleichungssysteme grafisch lösen Klasse 8 – Schnittpunkt, Arbeitsblätter",
              "LGS grafisch",
              "Lineare Gleichungssysteme für Klasse 8: Lösungen prüfen, nach y umstellen, Schnittpunkt ablesen, Anzahl der Lösungen und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "Lösung = Schnittpunkt der beiden Geraden.",
              "Parallel: keine Lösung. Gleiche Gerade: unendlich viele.",
              body, faq, sets, 7, grade="klasse-8")


if __name__ == "__main__":
    main()
