# -*- coding: utf-8 -*-
"""Schweiz Gymnasium: Gleichungssysteme mit drei Unbekannten, Folgen, Reihen und Grenzwerte, gebrochenrationale Funktionen"""
from fractions import Fraction as Fr
import de_common as D
import ch_common as C
from ch_gym import mcq, z, fz, par, poly, lin, ri, build, MI, NB

SUB = lambda s: "<sub>%s</sub>" % s


def A(n):
    return "a" + SUB(n)


def names(R, k):
    return R.sample(D.GIRLS + D.BOYS, k)


# ============================================================ Gleichungssysteme mit drei Unbekannten
def _eq(c, s=None, rhs=None):
    if rhs is None:
        rhs = sum(a * b for a, b in zip(c, s))
    return "%s = %s" % (poly({"x": c[0], "y": c[1], "z": c[2]}), z(rhs))


def _sys(rows):
    lab = ["I", "II", "III"]
    return "<span class='sys'>%s</span>" % "<br>".join("%s: %s" % (lab[i], r) for i, r in enumerate(rows))


def _det(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def _sol(x, y, w):
    return "x = %s, y = %s, z = %s" % (z(x), z(y), z(w))


def lgs3(R):
    def coefs():
        while True:
            c = [R.randint(-3, 3) for _ in range(3)]
            if sum(1 for a in c if a) >= 2:
                return c

    def check():
        s = [ri(R, -4, 4) for _ in range(3)]
        good = _eq(coefs(), s)
        bad = []
        for _ in range(3):
            c = coefs()
            r = sum(a * b for a, b in zip(c, s)) + R.choice([-2, -1, 1, 2, 3])
            bad.append(_eq(c, rhs=r))
        return mcq("Welche Gleichung wird von x = %s, y = %s, z = %s erfüllt?" % tuple(z(v) for v in s), good, bad,
                   "Setze die drei Zahlen ein und rechne die linke Seite aus. Nur bei <b>%s</b> stimmt die Gleichung." % good)

    def stair():
        x, y, w = [ri(R, -5, 5) for _ in range(3)]
        a, b, c = ri(R, -3, 3, (0,)), ri(R, -3, 3, (0,)), ri(R, -3, 3, (0,))
        k = R.choice([1, 2, 3])
        rows = [_eq([1, a, b], [x, y, w]), _eq([0, 1, c], [x, y, w]), _eq([0, 0, k], [x, y, w])]
        ask = R.choice(["x", "y"])
        if ask == "x":
            ans = x
            wrong = [x - 2 * b * w, y, x + 2 * a * y, -x]
            e = "Aus III: z = %s. In II einsetzen: y = %s. In I einsetzen: x = <b>%s</b>." % (z(w), z(y), z(x))
        else:
            ans = y
            wrong = [y - 2 * c * w, w, -y, x]
            e = "Aus III: z = %s. In II einsetzen: y + %s = %s, also y = <b>%s</b>." % (z(w), par(c * w), z(y + c * w), z(y))
        return mcq("Löse das gestaffelte System. Wie gross ist %s?<br>%s" % (ask, _sys(rows)), z(ans), [z(v) for v in wrong], e)

    def elim():
        while True:
            a1, b1, c1 = ri(R, 1, 4), ri(R, -4, 4, (0,)), ri(R, -4, 4, (0,))
            b2, c2 = ri(R, -4, 4, (0,)), ri(R, -4, 4, (0,))
            d1, d2 = ri(R, -12, 12), ri(R, -12, 12)
            if b1 + b2 or c1 + c2:
                break
        op = R.choice(["+", "−"])
        a2 = -a1 if op == "+" else a1
        I, II = [a1, b1, c1], [a2, b2, c2]
        sg = 1 if op == "+" else -1
        res = lambda s, dd: "%s = %s" % (poly({"y": b1 + s * b2, "z": c1 + s * c2}), z(dd))
        good = res(sg, d1 + sg * d2)
        bad = [res(-sg, d1 - sg * d2), res(sg, d1 - sg * d2), "%s = %s" % (poly({"y": b1 + sg * b2, "z": c1 - sg * c2}), z(d1 + sg * d2))]
        rows = [_eq(I, rhs=d1), _eq(II, rhs=d2)]
        return mcq("Welche Gleichung entsteht aus I %s II? Dabei fällt x weg.<br>%s" % (op, _sys(rows)), good, bad,
                   "Rechne jede Seite für sich: die y-Glieder, die z-Glieder und die rechten Seiten. Ergebnis: <b>%s</b>." % good)

    def full():
        while True:
            m = [[R.randint(-2, 3) for _ in range(3)] for _ in range(3)]
            if _det(m) and all(sum(1 for a in r if a) >= 2 for r in m):
                break
        s = [ri(R, -4, 4) for _ in range(3)]
        rows = [_eq(r, s) for r in m]
        x, y, w = s
        wrong = [(x, w, y), (y, x, w), (-x, y, w), (x, -y, w), (w, y, x)]
        cands = [_sol(*t) for t in wrong if list(t) != s]
        return mcq("Welche Lösung hat das Gleichungssystem?<br>%s" % _sys(rows), _sol(x, y, w), cands,
                   "Eliminiere zuerst eine Unbekannte, löse das System mit zwei Unbekannten und setze ein. Probe in allen drei Gleichungen: <b>%s</b>." % _sol(x, y, w))

    GOODS = [("Gipfeli", "Gipfeli"), ("Brötli", "Brötli"), ("Milchbrötli", "Milchbrötli"), ("Schoggistängel", "Schoggistängel"),
             ("Nussgipfel", "Nussgipfel"), ("Apfelsaft", "Apfelsäfte")]

    def sach():
        t = R.choice(["zahl", "preis", "alter"])
        if t == "zahl":
            x, d, k = R.randint(3, 30), R.randint(2, 15), R.choice([2, 3])
            S = x + x + d + k * x
            return mcq("Drei Zahlen haben die Summe %s. Die zweite Zahl ist um %d grösser als die erste. Die dritte Zahl ist %s so gross wie die erste. Wie heisst die erste Zahl?"
                       % (z(S), d, "doppelt" if k == 2 else "dreimal"), z(x), [z(x + d), z(k * x), z((S - d) // 2)],
                       "x + (x + %d) + %dx = %s ⇒ %dx = %s ⇒ x = <b>%s</b>." % (d, k, z(S), k + 2, z(S - d), z(x)))
        if t == "alter":
            n = names(R, 3)
            a, d1, d2 = R.randint(8, 40), R.randint(1, 9), R.randint(1, 9)
            T = a + (a + d1) + (a + d1 + d2)
            return mcq("%s, %s und %s sind zusammen %d Jahre alt. %s ist %d Jahre älter als %s, %s ist %d Jahre älter als %s. Wie alt ist %s?"
                       % (n[0], n[1], n[2], T, n[1], d1, n[0], n[2], d2, n[1], n[0]),
                       "%d Jahre" % a, ["%d Jahre" % (a + d1), "%d Jahre" % (T // 3), "%d Jahre" % (a - d1)],
                       "a + (a + %d) + (a + %d) = %d ⇒ 3a = %d ⇒ a = <b>%d</b>." % (d1, d1 + d2, T, T - 2 * d1 - d2, a))
        g = R.sample(GOODS, 3)
        p = [5 * R.randint(12, 60) for _ in range(3)]
        combos = R.sample([(1, 1, 1), (2, 1, 0), (0, 1, 2), (1, 0, 3), (3, 1, 1), (1, 2, 1), (2, 0, 1)], 3)
        while _det([list(c) for c in combos]) == 0:
            combos = R.sample([(1, 1, 1), (2, 1, 0), (0, 1, 2), (1, 0, 3), (3, 1, 1), (1, 2, 1), (2, 0, 1)], 3)

        def desc(c):
            parts = []
            for k, (sg, pl) in zip(c, g):
                if k:
                    parts.append("%d %s" % (k, sg if k == 1 else pl))
            return (", ".join(parts[:-1]) + " und " + parts[-1]) if len(parts) > 1 else parts[0]
        lines = ["%s kosten zusammen %s." % (desc(c), C.chf(sum(k * q for k, q in zip(c, p)))) for c in combos]
        lines = [l.replace(" kosten ", " kostet ") if l.startswith("1 ") and " und " not in l and "," not in l else l for l in lines]
        i = R.randrange(3)
        return mcq("%s Was kostet ein %s?" % (" ".join(lines), g[i][0]), C.chf(p[i]), [C.chf(p[(i + 1) % 3]), C.chf(p[(i + 2) % 3]), C.chf(p[i] + 10)],
                   "Stelle mit den Preisen x, y, z drei Gleichungen auf und löse das System. Ein %s kostet <b>%s</b>." % (g[i][0], C.chf(p[i])))

    return dict(
        title="Gleichungssysteme mit drei Unbekannten",
        short="Gleichungssysteme mit 3 Unbekannten",
        meta="Lineare Gleichungssysteme mit drei Unbekannten: Lösungen prüfen, gestaffelte Systeme, Additionsverfahren, Systeme lösen und Sachaufgaben. 100 Aufgaben mit Lösungen.",
        kb="Eine Unbekannte nach der anderen eliminieren.",
        ks="Am Ende in allen drei Gleichungen die Probe machen.",
        think=["Ein lineares Gleichungssystem mit drei Unbekannten hat drei Gleichungen. Die Lösung ist ein Zahlentripel (x | y | z), das <b>alle</b> Gleichungen erfüllt.",
               "Mit dem <b>Additionsverfahren</b> fällt eine Unbekannte weg: zwei Gleichungen so addieren oder subtrahieren, dass sich zum Beispiel die x-Glieder aufheben.",
               "So entsteht ein <b>gestaffeltes System</b>: Die letzte Gleichung hat nur noch eine Unbekannte. Von unten nach oben einsetzen.",
               "Bei Sachaufgaben zuerst festlegen, wofür x, y und z stehen."],
        ex=[("I: x + y + z = 6, II: y + z = 5, III: z = 3", ["Aus III: z = 3", "II: y + 3 = 5, also y = 2", "I: x + 2 + 3 = 6, also x = 1"], "x = 1, y = 2, z = 3"),
            ("I: 2x + y − z = 3, II: −2x + 3y + z = 5. Was ergibt I + II?", ["2x − 2x = 0", "y + 3y = 4y, −z + z = 0", "3 + 5 = 8"], "4y = 8, also y = 2")],
        mist=[["Nur die linken Seiten addieren", "Auch die rechten Seiten addieren"],
              ["Bei I − II nur das erste Glied subtrahieren", "Jedes Glied von II subtrahieren: Vorzeichen umdrehen"],
              ["Die Lösung nur in einer Gleichung prüfen", "Die Probe in allen drei Gleichungen machen"]],
        faq=[{"q": "Wie löst man ein Gleichungssystem mit drei Unbekannten?", "a": "Mit dem Additions- oder Einsetzungsverfahren eine Unbekannte eliminieren, bis ein gestaffeltes System entsteht. Dann von unten nach oben einsetzen."},
             {"q": "Was ist ein gestaffeltes System?", "a": "Ein System in Dreiecksform: Die letzte Gleichung hat nur eine Unbekannte, die mittlere zwei, die erste drei."},
             {"q": "Hat jedes System genau eine Lösung?", "a": "Nein. Ein System kann auch keine oder unendlich viele Lösungen haben, zum Beispiel wenn zwei Gleichungen Vielfache voneinander sind."},
             {"q": "Wie prüfe ich meine Lösung?", "a": "Die drei Zahlen in jede Gleichung einsetzen. Alle drei Gleichungen müssen stimmen."}],
        sets=[("Lösung einsetzen", [(check, 20)]), ("Gestaffelte Systeme", [(stair, 20)]), ("Eine Unbekannte eliminieren", [(elim, 20)]),
              ("Systeme lösen", [(full, 20)]), ("Sachaufgaben", [(sach, 20)])])


# ============================================================ Folgen
def folgen(R):
    def arith():
        a1, d = ri(R, -10, 20), ri(R, -6, 9, (0,))
        return a1, d, [a1 + i * d for i in range(5)]

    def geo():
        a1, q = R.choice([1, 2, 3, 4, 5, -2, -3]), R.choice([2, 3, -2, 4, 5, -3])
        return a1, q, [a1 * q ** i for i in range(5)]

    def nxt():
        if R.random() < 0.5:
            a1, d, t = arith()
            ans, wr = t[4], [t[3] + d + 1, t[3] + 2 * d, t[3] * 2]
        else:
            a1, q, t = geo()
            ans, wr = t[4], [t[3] + (t[3] - t[2]), t[3] * q * q, t[3] + q]
        return mcq("Wie heisst das nächste Glied der Folge %s, …?" % ", ".join(z(v) for v in t[:4]), z(ans), [z(v) for v in wr],
                   "Finde die Regel: immer gleich viel dazu (arithmetisch) oder immer mit derselben Zahl mal (geometrisch). Das nächste Glied ist <b>%s</b>." % z(ans))

    def typ():
        if R.random() < 0.5:
            a1, d, t = arith()
            good = "arithmetisch, d = %s" % z(d)
            bad = ["geometrisch, q = %s" % z(d), "arithmetisch, d = %s" % z(-d), "geometrisch, q = %s" % z(abs(d) + 1)]
        else:
            a1, q, t = geo()
            good = "geometrisch, q = %s" % z(q)
            bad = ["arithmetisch, d = %s" % z(t[1] - t[0]), "geometrisch, q = %s" % z(-q), "arithmetisch, d = %s" % z(q)]
        return mcq("Welche Art von Folge ist %s, …?" % ", ".join(z(v) for v in t[:4]), good, bad,
                   "Differenzen gleich ⇒ arithmetisch (d = Differenz). Quotienten gleich ⇒ geometrisch (q = Quotient). Hier: <b>%s</b>." % good)

    def an_arith():
        a1, d, n = ri(R, -20, 30), ri(R, -8, 12, (0,)), R.randint(10, 60)
        ans = a1 + (n - 1) * d
        return mcq("Eine arithmetische Folge hat %s = %s und d = %s. Berechne %s." % (A(1), z(a1), z(d), A(n)), z(ans),
                   [z(a1 + n * d), z(n * d), z(ans + d)],
                   "%s = %s + (n − 1) · d = %s + %d · %s = <b>%s</b>." % (A("n"), A(1), z(a1), n - 1, par(d), z(ans)))

    def formel():
        d, c = ri(R, -5, 9, (0,)), ri(R, -9, 12)
        t = [d * n + c for n in range(1, 5)]
        good = "%s = %s" % (A("n"), poly({"n": d, 0: c}))
        bad = ["%s = %s" % (A("n"), poly({"n": d, 0: t[0]})), "%s = %s" % (A("n"), poly({"n": t[0], 0: d})),
               "%s = %s" % (A("n"), poly({"n": d + 1, 0: c - 1}))]
        return mcq("Welche Formel beschreibt die Folge %s, …?" % ", ".join(z(v) for v in t), good, bad,
                   "Die Differenz ist d = %s, also %s = %s · n + c. Mit %s = %s folgt c = %s: <b>%s</b>." % (z(d), A("n"), z(d), A(1), z(t[0]), z(c), good))

    def an_geo():
        a1, q, n = R.choice([1, 2, 3, 5, -2, 4]), R.choice([2, 3, -2, 5, 10]), R.randint(4, 8)
        ans = a1 * q ** (n - 1)
        return mcq("Eine geometrische Folge hat %s = %s und q = %s. Berechne %s." % (A(1), z(a1), z(q), A(n)), z(ans),
                   [z(a1 * q ** n), z(a1 * q * (n - 1)), z(-ans)],
                   "%s = %s · q<sup>n − 1</sup> = %s · %s<sup>%d</sup> = <b>%s</b>." % (A("n"), A(1), z(a1), par(q), n - 1, z(ans)))

    def qsuch():
        a1, q, k = R.choice([1, 2, 3, 4, 5, 6]), R.choice([2, 3, 4, 5]), R.choice([2, 3])
        i = R.randint(1, 3)
        ai, aj = a1 * q ** (i - 1), a1 * q ** (i - 1 + k)
        return mcq("In einer geometrischen Folge ist %s = %s und %s = %s. Wie gross ist q (q &gt; 0)?" % (A(i), z(ai), A(i + k), z(aj)), z(q),
                   [z(q ** k), z(Fr(aj - ai, k)), z(q + 1)],
                   "%s = %s · q<sup>%d</sup>, also q<sup>%d</sup> = %s. Daraus q = <b>%s</b>." % (A(i + k), A(i), k, k, z(q ** k), z(q)))

    def rek():
        a1, m, c, n = ri(R, -3, 5), R.choice([2, 3, -1, -2]), ri(R, -4, 5), R.randint(3, 5)
        v = a1
        for _ in range(n - 1):
            v = m * v + c
        w = a1
        for _ in range(n - 2):
            w = m * w + c
        return mcq("Eine Folge ist rekursiv gegeben: %s = %s und %s = %s. Berechne %s." % (A(1), z(a1), A("n+1"), poly({A("n"): m, 0: c}), A(n)), z(v),
                   [z(w), z(m * v + c), z(a1 + (n - 1) * (m + c))],
                   "Glied für Glied rechnen: … %s = %s, %s = <b>%s</b>." % (A(n - 1), z(w), A(n), z(v)))

    def welches():
        a1, d = R.randint(-10, 20), R.randint(2, 9)
        n = R.randint(12, 60)
        v = a1 + (n - 1) * d
        t = [a1 + i * d for i in range(3)]
        return mcq("Das wievielte Glied der Folge %s, … ist %s?" % (", ".join(z(x) for x in t), z(v)), "das %d. Glied" % n,
                   ["das %d. Glied" % (n - 1), "das %d. Glied" % (n + 1), "das %d. Glied" % (v // d)],
                   "%s + (n − 1) · %d = %s ⇒ n − 1 = %d ⇒ n = <b>%d</b>." % (z(a1), d, z(v), n - 1, n))

    return dict(
        title="Arithmetische und geometrische Folgen",
        short="Arithmetische und geometrische Folgen",
        meta="Folgen am Gymnasium: nächstes Glied, arithmetisch oder geometrisch, explizite und rekursive Formeln, aₙ berechnen, q bestimmen. 100 Aufgaben mit Lösungen.",
        kb="Arithmetisch: immer + d. Geometrisch: immer · q.",
        ks="an = a1 + (n − 1) · d und an = a1 · q^(n − 1)",
        think=["Eine <b>Folge</b> ist eine Liste von Zahlen a<sub>1</sub>, a<sub>2</sub>, a<sub>3</sub>, …",
               "<b>Arithmetische Folge</b>: Die Differenz d zwischen zwei Gliedern ist immer gleich. a<sub>n</sub> = a<sub>1</sub> + (n − 1) · d.",
               "<b>Geometrische Folge</b>: Der Quotient q zweier Glieder ist immer gleich. a<sub>n</sub> = a<sub>1</sub> · q<sup>n − 1</sup>.",
               "Eine <b>rekursive</b> Formel sagt, wie man aus einem Glied das nächste berechnet."],
        ex=[("a₁ = 7, d = 4. Berechne a₁₀.", ["a₁₀ = 7 + 9 · 4"], "43"),
            ("Folge 3, 6, 12, 24, … Berechne a₇.", ["q = 2", "a₇ = 3 · 2⁶"], "192")],
        mist=[["a₁₀ = a₁ + 10 · d", "Bis zum 10. Glied sind es nur 9 Schritte: a₁₀ = a₁ + 9 · d"],
              ["Bei 2, 6, 18 die Differenz 4 als Regel nehmen", "Differenzen prüfen: 4, 12 – nicht gleich. Quotient 3 ist gleich."],
              ["a₁ · q · n statt a₁ · qⁿ⁻¹", "q wird (n − 1)-mal multipliziert, nicht mit n"]],
        faq=[{"q": "Woran erkenne ich eine arithmetische Folge?", "a": "Die Differenz zwischen aufeinanderfolgenden Gliedern ist immer gleich, zum Beispiel 3, 7, 11, 15 mit d = 4."},
             {"q": "Woran erkenne ich eine geometrische Folge?", "a": "Der Quotient aufeinanderfolgender Glieder ist immer gleich, zum Beispiel 2, 6, 18, 54 mit q = 3."},
             {"q": "Was ist der Unterschied zwischen expliziter und rekursiver Formel?", "a": "Mit der expliziten Formel berechnet man jedes Glied direkt aus n. Die rekursive Formel braucht das vorherige Glied."},
             {"q": "Kann q negativ sein?", "a": "Ja. Dann wechseln die Vorzeichen der Glieder ab, zum Beispiel 1, −2, 4, −8."}],
        sets=[("Das nächste Glied", [(nxt, 20)]), ("Arithmetisch oder geometrisch?", [(typ, 12), (formel, 8)]),
              ("Arithmetische Folgen", [(an_arith, 12), (welches, 8)]), ("Geometrische Folgen", [(an_geo, 12), (qsuch, 8)]),
              ("Rekursive Folgen und Formeln", [(rek, 12), (formel, 8)])])


# ============================================================ Reihen und Grenzwerte
def reihen(R):
    def s_arith():
        a1, d, n = R.randint(1, 20), R.randint(1, 9), R.randint(10, 50)
        an = a1 + (n - 1) * d
        s = n * (a1 + an) // 2 if n * (a1 + an) % 2 == 0 else None
        if s is None:
            return None
        return mcq("Berechne die Summe der ersten %d Glieder der arithmetischen Folge %s, %s, %s, …" % (n, z(a1), z(a1 + d), z(a1 + 2 * d)), z(s),
                   [z(n * an), z(n * (a1 + an)), z((n - 1) * (a1 + an) // 2)],
                   "%s = %s, s<sub>n</sub> = n · (a<sub>1</sub> + a<sub>n</sub>) : 2 = %d · %s : 2 = <b>%s</b>." % (A(n), z(an), n, z(a1 + an), z(s)))

    def gauss():
        n = R.choice([20, 30, 40, 50, 60, 80, 100, 120, 150, 200, 250, 300])
        a = R.choice([1, 1, 2, 3])
        if a == 1:
            s = n * (n + 1) // 2
            q = "1 + 2 + 3 + … + %s" % z(n)
            wr = [n * n, n * (n - 1) // 2, n * (n + 1)]
        else:
            last = a * n
            s = a * n * (n + 1) // 2
            q = "%d + %d + %d + … + %s" % (a, 2 * a, 3 * a, z(last))
            wr = [n * (a + last), n * last // 2, n * (n + 1) // 2]
        return mcq("Berechne %s." % q, z(s), [z(v) for v in wr], "Paare bilden: erstes + letztes Glied, %d Glieder. Summe = <b>%s</b>." % (n, z(s)))

    def s_geo():
        a1, q, n = R.choice([1, 2, 3, 5]), R.choice([2, 3, 4]), R.randint(4, 8)
        s = a1 * (q ** n - 1) // (q - 1)
        return mcq("Berechne %s + %s + %s + … (%d Glieder, geometrisch)." % (z(a1), z(a1 * q), z(a1 * q * q), n), z(s),
                   [z(a1 * q ** n), z(a1 * (q ** n - 1)), z(a1 * q ** (n - 1))],
                   "s<sub>n</sub> = a<sub>1</sub> · (q<sup>n</sup> − 1) : (q − 1) = %s · (%s − 1) : %d = <b>%s</b>." % (z(a1), z(q ** n), q - 1, z(s)))

    def unendl():
        a1 = R.choice([1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24])
        q = R.choice([Fr(1, 2), Fr(1, 3), Fr(2, 3), Fr(1, 4), Fr(3, 4), Fr(-1, 2), Fr(1, 5), Fr(2, 5)])
        s = a1 / (1 - q)
        ser = z(a1) + ("".join((" − " if t < 0 else " + ") + fz(abs(t)) for t in (a1 * q, a1 * q * q)))
        return mcq("Berechne den Wert der unendlichen geometrischen Reihe %s + …" % ser, fz(s),
                   [fz(a1 / (1 + q)), fz(a1 * q / (1 - q)), "Die Reihe hat keinen Wert."],
                   "q = %s, |q| &lt; 1. s = a<sub>1</sub> : (1 − q) = %s : %s = <b>%s</b>." % (fz(q), z(a1), fz(1 - q), fz(s)))

    def konv():
        a1 = R.choice([1, 2, 3, 4, 5, 6, 8, 10])
        q = R.choice([Fr(1, 2), Fr(2, 3), Fr(3, 2), Fr(2), Fr(-1, 3), Fr(5, 4), Fr(1, 3), Fr(-2)])
        ok = abs(q) < 1
        good = "Ja, denn |q| &lt; 1." if ok else "Nein, denn |q| ≥ 1."
        bad = ["Nein, denn |q| ≥ 1." if ok else "Ja, denn |q| &lt; 1.", "Ja, jede Reihe hat einen Wert.", "Nein, unendlich viele Zahlen haben nie eine endliche Summe."]
        ser = fz(a1) + ("".join((" − " if t < 0 else " + ") + fz(abs(t)) for t in (a1 * q, a1 * q * q)))
        return mcq("Hat die unendliche Reihe %s + … einen endlichen Wert?" % ser, good, bad,
                   "Der Quotient ist q = %s. Eine geometrische Reihe hat nur für |q| &lt; 1 einen Wert. %s" % (fz(q), good))

    def lim():
        k = R.choice(["gleich", "unten", "oben"])
        a, b, c, d = ri(R, 1, 9), ri(R, -9, 9), ri(R, 1, 9), ri(R, -9, 9, (0,))
        if k == "gleich":
            t = "(%s) : (%s)" % (lin(a, b, "n"), lin(c, d, "n"))
            ans, bad = fz(Fr(a, c)), [fz(Fr(b, d)), fz(Fr(a + b, c + d)) if c + d else "1", "Der Grenzwert existiert nicht."]
            sg = lambda v: ("− %d" % -v) if v < 0 else ("+ %d" % v)
            e = "Durch n teilen: (%s %s/n) : (%s %s/n) → %s : %s = <b>%s</b>." % (a, sg(b), c, sg(d), a, c, ans)
        elif k == "unten":
            t = "(%s) : (%s)" % (lin(a, b, "n"), poly({2: c, 0: d}, "n"))
            ans, bad = "0", [fz(Fr(a, c)), fz(Fr(b, d)), "Der Grenzwert existiert nicht."]
            e = "Der Nenner wächst schneller (n² gegen n). Der Bruch geht gegen <b>0</b>."
        else:
            t = "(%s) : (%s)" % (poly({2: a, 0: b}, "n"), lin(c, d, "n"))
            ans, bad = "Die Folge wächst über alle Grenzen.", [fz(Fr(a, c)), "0", fz(Fr(b, d))]
            e = "Der Zähler wächst schneller (n² gegen n). <b>Kein Grenzwert</b>: Die Folge wächst über alle Grenzen."
        return mcq("Gegen welchen Wert strebt %s = %s für n → ∞?" % (A("n"), t), ans, bad, e)

    def sigma():
        a, b, n = R.choice([1, 2, 3, 4, 5]), ri(R, -3, 6), R.randint(4, 12)
        s = sum(a * k + b for k in range(1, n + 1))
        return mcq("Berechne ∑<sub>k = 1</sub><sup>%d</sup> (%s)." % (n, lin(a, b, "k")), z(s),
                   [z(s - (a * n + b)), z(n * (a * n + b)), z(s + b)],
                   "Die Glieder sind %s, %s, …, %s. Ihre Summe ist <b>%s</b>." % (z(a + b), z(2 * a + b), z(a * n + b), z(s)))

    def sach():
        t = R.choice(["lauf", "sitz", "ball", "bakt"])
        if t == "lauf":
            nm = names(R, 1)[0]
            a1, d, n = R.choice([2, 3, 4, 5]), 1, R.choice([5, 6, 7, 8, 9, 10, 12, 14])
            s = n * (2 * a1 + (n - 1) * d)
            if s % 2:
                return None
            s //= 2
            return mcq("%s läuft am ersten Tag %d km und danach jeden Tag %d km mehr. Wie viele Kilometer sind es in %d Tagen zusammen?" % (nm, a1, d, n),
                       "%s km" % z(s), ["%s km" % z(a1 + (n - 1) * d), "%s km" % z(n * (a1 + (n - 1) * d)), "%s km" % z(s - a1)],
                       "Arithmetische Reihe: a<sub>1</sub> = %d, a<sub>%d</sub> = %d. s = %d · (%d + %d) : 2 = <b>%s km</b>." % (a1, n, a1 + (n - 1) * d, n, a1, a1 + (n - 1) * d, z(s)))
        if t == "sitz":
            a1, d, n = R.randint(15, 30), R.choice([1, 2, 3]), R.randint(10, 25)
            s = n * (2 * a1 + (n - 1) * d) // 2 if (n * (2 * a1 + (n - 1) * d)) % 2 == 0 else None
            if s is None:
                return None
            return mcq("In einem Saal hat die erste Reihe %d Sitze, jede weitere Reihe %d Sitze mehr. Es gibt %d Reihen. Wie viele Sitze sind es insgesamt?" % (a1, d, n),
                       z(s), [z(a1 + (n - 1) * d), z(n * a1), z(s + a1)],
                       "Letzte Reihe: %d Sitze. Summe = %d · (%d + %d) : 2 = <b>%s</b>." % (a1 + (n - 1) * d, n, a1, a1 + (n - 1) * d, z(s)))
        if t == "ball":
            h, q = R.choice([(2, Fr(1, 2)), (3, Fr(2, 3)), (4, Fr(1, 2)), (5, Fr(3, 5)), (6, Fr(1, 3)), (8, Fr(3, 4)), (9, Fr(2, 3)), (10, Fr(1, 2))])
            total = h + 2 * h * q / (1 - q)
            return mcq("Ein Ball fällt aus %d m Höhe und springt jedes Mal auf %s der vorherigen Höhe zurück. Welchen Weg legt er insgesamt zurück (beliebig viele Sprünge)?" % (h, fz(q)),
                       "%s m" % fz(total), ["%s m" % fz(h / (1 - q)), "%s m" % fz(h * q / (1 - q)), "%s m" % fz(2 * h / (1 - q))],
                       "Fallen %d m, dann je zweimal (hinauf und hinunter) %s, %s, … Weg = %d + 2 · %s : (1 − %s) = <b>%s m</b>." % (h, fz(h * q), fz(h * q * q), h, fz(h * q), fz(q), fz(total)))
        a, n = R.choice([10, 20, 50, 100, 200, 500]), R.randint(5, 10)
        s = a * 2 ** n
        return mcq("Eine Bakterienkultur hat %s Bakterien und verdoppelt sich jede Stunde. Wie viele sind es nach %d Stunden?" % (z(a), n), z(s),
                   [z(a * 2 * n), z(a * 2 ** (n - 1)), z(a + 2 ** n)],
                   "Geometrische Folge mit q = 2: %s · 2<sup>%d</sup> = <b>%s</b>." % (z(a), n, z(s)))

    return dict(
        title="Reihen und Grenzwerte von Folgen",
        short="Reihen und Grenzwerte",
        meta="Reihen am Gymnasium: arithmetische und geometrische Summen, Summenzeichen, unendliche geometrische Reihen, Grenzwerte von Folgen und Sachaufgaben. 100 Aufgaben mit Lösungen.",
        kb="Arithmetisch: s = n · (a1 + an) : 2",
        ks="Unendliche geometrische Reihe: s = a1 : (1 − q) für |q| kleiner als 1",
        think=["Eine <b>Reihe</b> ist die Summe der Glieder einer Folge.",
               "Arithmetische Reihe: s<sub>n</sub> = n · (a<sub>1</sub> + a<sub>n</sub>) : 2 (erstes plus letztes Glied, mal Anzahl, durch 2).",
               "Geometrische Reihe: s<sub>n</sub> = a<sub>1</sub> · (q<sup>n</sup> − 1) : (q − 1).",
               "Für |q| &lt; 1 hat die <b>unendliche</b> geometrische Reihe den Wert a<sub>1</sub> : (1 − q).",
               "Grenzwert eines Bruchs für n → ∞: Zähler und Nenner durch die höchste Potenz von n teilen."],
        ex=[("1 + 2 + 3 + … + 100", ["100 Glieder", "(1 + 100) · 100 : 2"], "5050"),
            ("8 + 4 + 2 + 1 + …", ["q = ½", "8 : (1 − ½) = 8 : ½"], "16")],
        mist=[["s = n · aₙ", "Mittelwert von erstem und letztem Glied nehmen: n · (a₁ + aₙ) : 2"],
              ["Auch für q = 2 eine unendliche Summe angeben", "Nur für |q| kleiner als 1 gibt es einen Wert"],
              ["(2n + 1) : (n + 3) → 1 : 3", "Durch n teilen: Der Grenzwert ist 2 : 1 = 2"]],
        faq=[{"q": "Was ist der Unterschied zwischen Folge und Reihe?", "a": "Eine Folge ist eine Liste von Zahlen. Eine Reihe ist die Summe dieser Zahlen."},
             {"q": "Wann hat eine unendliche geometrische Reihe einen Wert?", "a": "Genau dann, wenn |q| < 1 ist. Dann ist s = a1 : (1 − q)."},
             {"q": "Wie berechne ich 1 + 2 + … + n schnell?", "a": "Mit der Formel von Gauss: n · (n + 1) : 2."},
             {"q": "Wie finde ich den Grenzwert von (2n + 1) : (n + 3)?", "a": "Zähler und Nenner durch n teilen. Die Glieder 1/n und 3/n gehen gegen 0, es bleibt 2 : 1 = 2."}],
        sets=[("Arithmetische Reihen", [(gauss, 8), (s_arith, 12)]), ("Summenzeichen und geometrische Reihen", [(sigma, 10), (s_geo, 10)]),
              ("Unendliche geometrische Reihen", [(unendl, 12), (konv, 8)]), ("Grenzwerte von Folgen", [(lim, 20)]), ("Sachaufgaben", [(sach, 20)])])


# ============================================================ gebrochenrationale Funktionen
def gebrochen(R):
    def f_lin():
        while True:
            a, b, c, d = ri(R, -6, 6, (0,)), ri(R, -9, 9), ri(R, 1, 4), ri(R, -9, 9, (0,))
            if a * d - b * c:
                return a, b, c, d

    def F(a, b, c, d):
        return "f(x) = (%s) : (%s)" % (lin(a, b), lin(c, d))

    def defm():
        a, b, c, d = f_lin()
        p = Fr(-d, c)
        good = "D = ℝ ∖ {%s}" % fz(p)
        bad = ["D = ℝ ∖ {%s}" % fz(-p), "D = ℝ ∖ {%s}" % fz(Fr(-b, a)), "D = ℝ"]
        return mcq("Welche Definitionsmenge hat %s?" % F(a, b, c, d), good, bad,
                   "Der Nenner darf nicht 0 sein: %s = 0 für x = %s. Also <b>%s</b>." % (lin(c, d), fz(p), good))

    def senk():
        a, b, c, d = f_lin()
        p = Fr(-d, c)
        good = "x = %s" % fz(p)
        return mcq("Wo hat der Graph von %s eine senkrechte Asymptote?" % F(a, b, c, d), good,
                   ["x = %s" % fz(-p), "x = %s" % fz(Fr(-b, a)), "y = %s" % fz(Fr(a, c))],
                   "Polstelle: Nenner gleich 0, Zähler nicht 0. Bei <b>%s</b>." % good)

    def waag():
        k = R.choice(["gleich", "unten", "oben"])
        a, b, c, d = ri(R, -6, 6, (0,)), ri(R, -9, 9), ri(R, 1, 4), ri(R, -9, 9, (0,))
        if k == "gleich":
            ff = F(a, b, c, d)
            good = "y = %s" % fz(Fr(a, c))
            bad = ["y = %s" % fz(Fr(b, d)), "y = 0", "Es gibt keine waagrechte Asymptote."]
            e = "Zählergrad = Nennergrad: y = Quotient der Leitkoeffizienten = <b>%s</b>." % fz(Fr(a, c))
        elif k == "unten":
            ff = "f(x) = (%s) : (%s)" % (lin(a, b), poly({2: c, 0: abs(d)}))
            good = "y = 0"
            bad = ["y = %s" % fz(Fr(a, c)), "y = %s" % fz(Fr(b, abs(d))), "Es gibt keine waagrechte Asymptote."]
            e = "Zählergrad kleiner als Nennergrad: Die x-Achse <b>y = 0</b> ist Asymptote."
        else:
            ff = "f(x) = (%s) : (%s)" % (poly({2: a, 0: b}), lin(c, d))
            good = "Es gibt keine waagrechte Asymptote."
            bad = ["y = %s" % fz(Fr(a, c)), "y = 0", "y = %s" % fz(Fr(b, d))]
            e = "Zählergrad grösser als Nennergrad: <b>keine waagrechte Asymptote</b> (der Graph hat eine schiefe Asymptote)."
        return mcq("Welche waagrechte Asymptote hat der Graph von %s?" % ff, good, bad, e)

    def null():
        a, b, c, d = f_lin()
        x0 = Fr(-b, a)
        good = "x = %s" % fz(x0)
        return mcq("Wo hat %s eine Nullstelle?" % F(a, b, c, d), good, ["x = %s" % fz(Fr(-d, c)), "x = %s" % fz(-x0), "x = %s" % fz(Fr(b, d))],
                   "Der Zähler ist 0: %s = 0 ⇒ x = <b>%s</b> (der Nenner ist dort nicht 0)." % (lin(a, b), fz(x0)))

    def luecke():
        p, q = ri(R, -6, 6, (0,)), ri(R, -6, 6, (0,))
        if p == q or p == -q:
            return None
        k = R.choice(["luecke", "pol"])
        if k == "luecke":
            ff = "f(x) = (%s) : (%s)" % (poly({2: 1, 1: -(p + q), 0: p * q}), lin(1, -p))
            good = "eine hebbare Definitionslücke"
            e = "Zähler = (%s)(%s). Der Faktor (%s) kürzt sich weg: bei x = %s liegt <b>%s</b> vor." % (lin(1, -p), lin(1, -q), lin(1, -p), z(p), good)
        else:
            ff = "f(x) = (%s) : (%s)" % (lin(1, -q), lin(1, -p))
            good = "eine Polstelle"
            e = "Bei x = %s ist der Nenner 0, der Zähler aber %s ≠ 0: <b>%s</b>." % (z(p), z(p - q), good)
        others = ["eine Polstelle", "eine hebbare Definitionslücke", "eine Nullstelle", "kein besonderer Punkt"]
        return mcq("Was hat der Graph von %s bei x = %s?" % (ff, z(p)), good, [o for o in others if o != good], e)

    def versch():
        a, p, q = R.choice([1, 2, 3, -1, -2, 4]), ri(R, -6, 6, (0,)), ri(R, -6, 6, (0,))
        ff = "f(x) = %s : (%s) %s %s" % (z(a), lin(1, -p), "+" if q > 0 else "−", z(abs(q)))
        good = "x = %s und y = %s" % (z(p), z(q))
        return mcq("Welche Asymptoten hat der Graph von %s?" % ff, good,
                   ["x = %s und y = %s" % (z(-p), z(q)), "x = %s und y = %s" % (z(q), z(p)), "x = %s und y = %s" % (z(p), z(a))],
                   "Der Graph von %s : x ist um %s nach rechts/links und %s nach oben/unten verschoben: <b>%s</b>." % (z(a), z(p), z(q), good))

    def wert():
        a, b, c, d = f_lin()
        x = ri(R, -5, 6)
        if c * x + d == 0:
            return None
        v = Fr(a * x + b, c * x + d)
        return mcq("Berechne f(%s) für %s." % (z(x), F(a, b, c, d)), fz(v), [fz(Fr(a * x - b, c * x + d)), fz(Fr(c * x + d, a * x + b)) if a * x + b else "0", fz(Fr(a, c))],
                   "f(%s) = (%s) : (%s) = <b>%s</b>." % (z(x), z(a * x + b), z(c * x + d), fz(v)))

    return dict(
        title="Gebrochenrationale Funktionen und Asymptoten",
        short="Gebrochenrationale Funktionen",
        meta="Gebrochenrationale Funktionen: Definitionsmenge, Nullstellen, Polstellen und hebbare Lücken, senkrechte und waagrechte Asymptoten. 100 Aufgaben mit Lösungen.",
        kb="Nenner = 0: Polstelle oder Lücke.",
        ks="Grade von Zähler und Nenner vergleichen: so findet man die waagrechte Asymptote.",
        think=["Eine <b>gebrochenrationale Funktion</b> ist ein Bruch aus zwei Polynomen: f(x) = Zähler : Nenner.",
               "Wo der Nenner 0 ist, ist f nicht definiert. Ist der Zähler dort nicht 0, hat der Graph eine <b>Polstelle</b> mit senkrechter Asymptote.",
               "Kürzt sich der Faktor weg, ist es eine <b>hebbare Definitionslücke</b>.",
               "Waagrechte Asymptote: Zählergrad &lt; Nennergrad ⇒ y = 0. Gleiche Grade ⇒ y = Quotient der Leitkoeffizienten. Zählergrad &gt; Nennergrad ⇒ keine."],
        ex=[("f(x) = (2x − 4) : (x + 1)", ["Nenner 0 bei x = −1", "Grade gleich: 2 : 1"], "senkrechte Asymptote x = −1, waagrechte y = 2"),
            ("f(x) = (x² − 9) : (x − 3)", ["x² − 9 = (x − 3)(x + 3)", "Kürzen: f(x) = x + 3 für x ≠ 3"], "hebbare Lücke bei x = 3")],
        mist=[["Nullstelle des Nenners als Nullstelle von f", "Nullstellen von f kommen vom Zähler, der Nenner liefert Pole"],
              ["Bei (2x + 1) : (x − 3) die Asymptote y = 1 : (−3)", "Leitkoeffizienten nehmen: y = 2 : 1 = 2"],
              ["Jede Nennernullstelle ist eine Polstelle", "Erst kürzen: Kürzt sich der Faktor, ist es eine Lücke"]],
        faq=[{"q": "Was ist eine Asymptote?", "a": "Eine Gerade, der sich der Graph immer mehr nähert, ohne sie zu erreichen, wenn x gegen eine Polstelle oder gegen ±∞ geht."},
             {"q": "Wie finde ich die senkrechte Asymptote?", "a": "Nullstellen des Nenners bestimmen, die nach dem Kürzen übrig bleiben."},
             {"q": "Wie finde ich die waagrechte Asymptote?", "a": "Grade vergleichen: Zählergrad < Nennergrad gibt y = 0, gleiche Grade geben y = Quotient der Leitkoeffizienten."},
             {"q": "Was ist der Unterschied zwischen Polstelle und Lücke?", "a": "Bei einer Polstelle geht der Graph gegen ±∞. Bei einer hebbaren Lücke fehlt nur ein einzelner Punkt."}],
        sets=[("Definitionsmenge und Funktionswerte", [(defm, 10), (wert, 10)]), ("Nullstellen und Polstellen", [(null, 10), (senk, 10)]),
              ("Polstelle oder Lücke?", [(luecke, 20)]), ("Waagrechte Asymptoten", [(waag, 20)]), ("Verschobene Hyperbeln", [(versch, 20)])])
