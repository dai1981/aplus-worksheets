# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 8: Mehrstufige Zufallsexperimente（Leitidee Daten und Zufall, Sek I）
  python3 tools/gen_de_mathe_k8_mehrstufige_zufallsexperimente.py
Baumdiagramme mit drei Stufen, Anzahl der Pfade, Pfadregel und Summenregel, Ziehen mit und ohne Zurücklegen (auch dreimal),
„mindestens einmal“ über das Gegenereignis, Erwartungswert und faire Spiele.
Fehler: entlang des Pfades addiert, nur einen von mehreren Pfaden gezählt, „mindestens einmal“ als einfache Wahrscheinlichkeit, Nenner ohne Zurücklegen nicht verkleinert.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, Kids, wrap, line, text, INK
from de_k6 import bh, dz, endlich
from de_k8 import mcq, eur

R = random.Random(49814)
KIDS = Kids(R)
P = " %"


def pz(v):
    return dz(Fr(v) * 100) + P


def pr(v):
    return "%d/%d" % (v.numerator, v.denominator) if v.denominator != 1 else str(v.numerator)


def tree3(p, a="K", b="Z"):
    """dreistufiger Baum mit gleichen Wahrscheinlichkeiten p (für a) je Stufe"""
    W, H = 300, 170
    xs = [6, 92, 182, 274]
    s = []
    def rec(x_i, y, lo, hi, depth):
        if depth == 3:
            return
        ys = [(lo + (lo + hi) / 2) / 2, ((lo + hi) / 2 + hi) / 2]
        for k, (lab, pp) in enumerate([(a, p), (b, 1 - p)]):
            yy = ys[k]
            s.append(line(xs[depth] + (12 if depth else 0), y, xs[depth + 1] - 7, yy, INK, 1.6))
            s.append(text(xs[depth + 1] + 3, yy + 6, lab, 17, weight=700))
            if depth == 0:
                s.append(text((xs[0] + xs[1]) / 2 - 6, (y + yy) / 2 + (-7 if k == 0 else 18), pr(pp), 16, weight=600))
            rec(None, yy, lo if k == 0 else (lo + hi) / 2, (lo + hi) / 2 if k == 0 else hi, depth + 1)
    rec(None, H / 2, 0, H, 0)
    return wrap(W, H, "".join(s), "dreistufiges Baumdiagramm", lg=True)


def baum():
    kind = R.choice(["pfade", "pfade", "muenze3", "bild"])
    if kind == "pfade":
        a, n = R.choice([(2, 3), (2, 4), (3, 2), (6, 2), (3, 3), (4, 2), (2, 5)])
        what = {2: "wirft eine Münze", 3: "dreht ein Glücksrad mit drei gleich großen Farbfeldern", 4: "wirft einen Tetraeder-Würfel", 6: "wirft einen Würfel"}[a]
        verb, obj = what.split(" ", 1)
        return mcq("Man %s %s %d-mal. Wie viele Pfade hat das vollständige Baumdiagramm?" % (verb, obj, n), str(a ** n), [str(a * n), str(a + n), str(a ** (n - 1)), str(n ** a), str(n)],
                   "Jede Stufe hat %d Äste: %s = <b>%d</b>." % (a, (" %s " % MAL).join([str(a)] * n), a ** n))
    if kind == "muenze3":
        ev, g = R.choice([("dreimal Kopf", 1), ("genau zweimal Kopf", 3), ("genau einmal Kopf", 3), ("mindestens zweimal Kopf", 4), ("höchstens einmal Kopf", 4), ("keinmal Kopf", 1)])
        v = Fr(g, 8)
        return mcq("Eine Münze wird dreimal geworfen. Wie groß ist P(%s)?" % ev, bh(v), [bh(Fr(1, 3)) if v != Fr(1, 3) else bh(Fr(1, 2)), bh(Fr(g, 6)), bh(Fr(1, 8)) if v != Fr(1, 8) else bh(Fr(1, 4))],
                   "8 gleich wahrscheinliche Pfade, %d davon günstig: <b>%s</b>." % (g, bh(v)))
    p = Fr(R.choice([1, 1, 2, 3]), R.choice([2, 3, 4, 5]))
    if p >= 1 or p == Fr(1, 2) and R.random() < 0.5:
        return None
    pic = tree3(p, "r", "b")
    ev = R.choice(["rrr", "bbb", "rbr"])
    v = 1
    for c in ev:
        v *= p if c == "r" else 1 - p
    return mcq(pic + "Ein Glücksrad zeigt Rot (r) mit der Wahrscheinlichkeit %s. Es wird dreimal gedreht. Wie groß ist P(%s)?" % (bh(p), ", ".join(ev)), bh(v),
               [bh(sum(p if c == "r" else 1 - p for c in ev)) if sum(p if c == "r" else 1 - p for c in ev) <= 1 else bh(v * 3) if v * 3 <= 1 else bh(v / 2), bh(Fr(1, 8)) if v != Fr(1, 8) else bh(Fr(1, 6)), bh(p if ev[0] == "r" else 1 - p)],
               "Pfadregel: %s = <b>%s</b>." % ((" %s " % MAL).join(bh(p if c == "r" else 1 - p) for c in ev), bh(v)))


def mit():
    r, b = R.randint(1, 6), R.randint(1, 6)
    t = r + b
    pr_, pb = Fr(r, t), Fr(b, t)
    kind = R.choice(["drei_r", "drei_gemischt", "zwei_genau"])
    intro = "In einer Urne liegen %d rote und %d blaue Kugeln. " % (r, b)
    if kind == "drei_r":
        v = pr_ ** 3
        return mcq(intro + "Es wird dreimal <b>mit Zurücklegen</b> gezogen. Wie groß ist die Wahrscheinlichkeit, dreimal Rot zu ziehen?", bh(v), [bh(3 * pr_) if 3 * pr_ <= 1 else bh(pr_ ** 2), bh(pr_), bh(Fr(r ** 3, t * 3))],
                   "%s %s %s %s %s = <b>%s</b>." % (bh(pr_), MAL, bh(pr_), MAL, bh(pr_), bh(v)))
    if kind == "drei_gemischt":
        v = 3 * pr_ * pr_ * pb
        if v > 1:
            return None
        return mcq(intro + "Es wird dreimal <b>mit Zurücklegen</b> gezogen. Wie groß ist die Wahrscheinlichkeit für genau zwei rote Kugeln?", bh(v), [bh(pr_ * pr_ * pb), bh(pr_ * pr_), bh(2 * pr_ * pb) if 2 * pr_ * pb != v else bh(pr_)],
                   "Drei Pfade: rrb, rbr, brr. Jeder hat %s. Summenregel: 3 %s %s = <b>%s</b>." % (bh(pr_ * pr_ * pb), MAL, bh(pr_ * pr_ * pb), bh(v)))
    v = 2 * pr_ * pb
    return mcq(intro + "Es wird zweimal <b>mit Zurücklegen</b> gezogen. Wie groß ist die Wahrscheinlichkeit für zwei verschiedene Farben?", bh(v), [bh(pr_ * pb), bh(pr_ + pb) if pr_ + pb != v else bh(Fr(1, 2)), bh(pr_ * pr_ + pb * pb)],
               "(r, b) + (b, r) = 2 %s %s %s %s = <b>%s</b>." % (MAL, bh(pr_), MAL, bh(pb), bh(v)))


def ohne():
    r, b = R.randint(2, 7), R.randint(2, 7)
    t = r + b
    kind = R.choice(["drei_r", "zwei_b", "erst_r_dann_b", "drei_r"])
    name, _ = KIDS.next()
    intro = "In einem Beutel sind %d rote und %d blaue Murmeln. %s nimmt nacheinander Murmeln heraus, <b>ohne sie zurückzulegen</b>. " % (r, b, name)
    if kind == "drei_r":
        if r < 3:
            return None
        v = Fr(r, t) * Fr(r - 1, t - 1) * Fr(r - 2, t - 2)
        return mcq(intro + "Es wird dreimal <b>mit Zurücklegen</b> gezogen. Wie groß ist die Wahrscheinlichkeit, dreimal Rot zu ziehen?", bh(v), [bh(Fr(r, t) ** 3), bh(Fr(r * (r - 1) * (r - 2), t ** 3)), bh(Fr(r - 2, t - 2))],
                   "%s %s %s %s %s = <b>%s</b>." % (bh(Fr(r, t)), MAL, bh(Fr(r - 1, t - 1)), MAL, bh(Fr(r - 2, t - 2)), bh(v)))
    if kind == "zwei_b":
        v = Fr(b, t) * Fr(b - 1, t - 1)
        return mcq(intro + "Wie groß ist die Wahrscheinlichkeit, zweimal Blau zu ziehen?", bh(v), [bh(Fr(b, t) ** 2), bh(Fr(b, t)), bh(Fr(b * (b - 1), t * t))],
                   "%s %s %s = <b>%s</b>." % (bh(Fr(b, t)), MAL, bh(Fr(b - 1, t - 1)), bh(v)))
    v = Fr(r, t) * Fr(b, t - 1)
    return mcq(intro + "Wie groß ist die Wahrscheinlichkeit, zuerst Rot und dann Blau zu ziehen?", bh(v), [bh(Fr(r, t) * Fr(b, t)), bh(2 * v) if 2 * v <= 1 else bh(v / 2), bh(Fr(r, t) + Fr(b, t - 1)) if Fr(r, t) + Fr(b, t - 1) <= 1 else bh(Fr(b, t - 1))],
               "%s %s %s = <b>%s</b>." % (bh(Fr(r, t)), MAL, bh(Fr(b, t - 1)), bh(v)))


def mindestens():
    kind = R.choice(["wuerfel", "muenze", "treffer", "urne"])
    if kind == "wuerfel":
        n = R.choice([2, 3])
        v = 1 - Fr(5, 6) ** n
        return mcq("Ein Würfel wird %d-mal geworfen. Wie groß ist die Wahrscheinlichkeit, mindestens eine Sechs zu werfen?" % n, bh(v), [bh(Fr(n, 6)), bh(Fr(1, 6) ** n), bh(Fr(5, 6) ** n)],
                   "Gegenereignis „keine Sechs“: (%s)<sup>%d</sup> = %s. 1 − %s = <b>%s</b>." % (bh(Fr(5, 6)), n, bh(Fr(5, 6) ** n), bh(Fr(5, 6) ** n), bh(v)))
    if kind == "muenze":
        n = R.choice([2, 3, 4])
        v = 1 - Fr(1, 2) ** n
        return mcq("Eine Münze wird %d-mal geworfen. Wie groß ist die Wahrscheinlichkeit für mindestens einmal Zahl?" % n, bh(v), [bh(Fr(1, 2) ** n), bh(Fr(1, 2)), bh(Fr(n, 2 ** n))],
                   "Gegenereignis „nur Kopf“: (1/2)<sup>%d</sup> = %s. 1 − %s = <b>%s</b>." % (n, bh(Fr(1, 2) ** n), bh(Fr(1, 2) ** n), bh(v)))
    if kind == "treffer":
        p = Fr(R.choice([6, 7, 8, 9]), 10)
        n = R.choice([2, 3])
        v = 1 - (1 - p) ** n
        name, er = KIDS.next()
        return mcq("%s trifft beim Basketball mit einer Wahrscheinlichkeit von %s. %s wirft %d-mal. Wie groß ist die Wahrscheinlichkeit, mindestens einmal zu treffen?" % (name, pz(p), er.capitalize(), n), pz(v),
                   [pz(p ** n), pz(p), pz(min(Fr(1), p * n)) if p * n < 1 else pz((1 - p) ** n)],
                   "Kein Treffer: %s<sup>%d</sup> = %s. 1 − %s = <b>%s</b>." % (dz(1 - p), n, dz((1 - p) ** n), dz((1 - p) ** n), pz(v)))
    r, b = R.randint(1, 4), R.randint(2, 6)
    t = r + b
    v = 1 - Fr(b, t) * Fr(b - 1, t - 1)
    return mcq("In einer Kiste liegen %d rote und %d blaue Bälle. Man zieht zwei Bälle ohne Zurücklegen. Wie groß ist die Wahrscheinlichkeit, mindestens einen roten Ball zu ziehen?" % (r, b), bh(v),
               [bh(Fr(b, t) * Fr(b - 1, t - 1)), bh(Fr(r, t)), bh(1 - Fr(b, t) ** 2) if 1 - Fr(b, t) ** 2 != v else bh(Fr(r, t) * 2) if Fr(r, t) * 2 <= 1 else bh(Fr(r, t - 1))],
               "Gegenereignis „zwei blaue“: %s %s %s = %s. 1 − %s = <b>%s</b>." % (bh(Fr(b, t)), MAL, bh(Fr(b - 1, t - 1)), bh(Fr(b, t) * Fr(b - 1, t - 1)), bh(Fr(b, t) * Fr(b - 1, t - 1)), bh(v)))


def sache():
    kind = R.choice(["ampel", "spiel", "erwart", "pin", "test"])
    if kind == "ampel":
        p = Fr(R.choice([4, 5, 6]), 10)
        n = R.choice([2, 3])
        return mcq("Auf dem Schulweg liegen %d Ampeln. Jede zeigt unabhängig mit %s Rot. Wie groß ist die Wahrscheinlichkeit, nur grüne Ampeln zu haben?" % (n, pz(p)), pz((1 - p) ** n),
                   [pz(1 - p), pz(1 - p ** n), pz(p ** n)], "Grün: %s. %s<sup>%d</sup> = <b>%s</b>." % (pz(1 - p), dz(1 - p), n, pz((1 - p) ** n)))
    if kind == "spiel":
        e, g = R.choice([(1, 5), (2, 10), (1, 4), (2, 6), (1, 3)])
        # Einsatz e €, Gewinn g € bei Doppelsechs? Pasch
        pw = Fr(1, 6)
        ew = pw * g - e
        if ew == 0:
            ans = "fair, denn im Mittel gewinnt man %s und zahlt %s" % (eur(pw * g), eur(e))
        else:
            ans = ("nicht fair, der Spieler verliert im Mittel %s pro Spiel" % eur(-ew)) if ew < 0 else ("nicht fair, der Spieler gewinnt im Mittel %s pro Spiel" % eur(ew))
        return mcq("Bei einem Spiel zahlt man %d € Einsatz und wirft zwei Würfel. Bei einem Pasch bekommt man %d € ausgezahlt. Ist das Spiel fair?" % (e, g), ans,
                   [a for a in ["fair, denn im Mittel gewinnt man %s und zahlt %s" % (eur(pw * g), eur(e)), "nicht fair, der Spieler verliert im Mittel %s pro Spiel" % eur(abs(ew) + 1), "nicht fair, der Spieler gewinnt im Mittel %s pro Spiel" % eur(abs(ew) + Fr(1, 2)), "fair, denn ein Pasch ist selten"] if a != ans],
                   "P(Pasch) = %s. Mittlere Auszahlung: %s %s %d € = %s. Einsatz %d €. <b>%s</b>" % (bh(pw), bh(pw), MAL, g, eur(pw * g), e, ans[0].upper() + ans[1:]))
    if kind == "erwart":
        n = R.choice([200, 300, 600, 900])
        p = R.choice([Fr(1, 4), Fr(1, 3), Fr(1, 6), Fr(1, 12)])
        if (n * p).denominator != 1:
            return None
        q = {Fr(1, 4): "Zwei Münzen werden %d-mal geworfen. Wie oft erwartet man etwa zweimal Kopf?", Fr(1, 6): "Zwei Würfel werden %d-mal geworfen. Wie oft erwartet man einen Pasch?",
             Fr(1, 12): "Ein Würfel und eine Münze werden %d-mal zusammen geworfen. Wie oft erwartet man „Sechs und Kopf“?"}.get(p)
        if q is None:
            return None
        return mcq(q % n, "etwa %d-mal" % (n * p), ["etwa %d-mal" % (n // 2), "etwa %d-mal" % (n - n * p), "genau %d-mal" % (n * p)],
                   "P = %s. Erwartete Anzahl: %d %s %s = <b>%d</b>. Genau kann man es nicht vorhersagen." % (bh(p), n, MAL, bh(p), n * p))
    if kind == "pin":
        n = R.choice([3, 4])
        return mcq("Eine PIN hat %d Ziffern von 0 bis 9 (Wiederholung erlaubt). Wie groß ist die Wahrscheinlichkeit, sie beim ersten Raten zu treffen?" % n, "1/%s" % ("1000" if n == 3 else "10 000"),
                   ["1/%d" % (10 * n), "%d/10" % n, "1/%d" % (10 ** (n - 1))], "Es gibt 10<sup>%d</sup> = %s mögliche PINs: <b>1/%s</b>." % (n, "1000" if n == 3 else "10 000", "1000" if n == 3 else "10 000"))
    v = Fr(R.choice([1, 2, 3]), 10)
    w = Fr(R.choice([7, 8, 9]), 10)
    name, er = KIDS.next()
    return mcq("%s beantwortet zwei Quizfragen. Die erste beantwortet %s mit einer Wahrscheinlichkeit von %s richtig, die zweite mit %s. Wie groß ist die Wahrscheinlichkeit, dass beide richtig sind?" % (name, er, pz(v), pz(w)), pz(v * w),
               [pz(v + w) if v + w < 1 else pz(v), pz((v + w) / 2), pz(1 - v * w)], "Pfadregel: %s %s %s = <b>%s</b>." % (dz(v), MAL, dz(w), pz(v * w)))


def main():
    seen = set()
    sets = [
        ("Baumdiagramme", mix(R, seen, [(baum, 20)])),
        ("Mit Zurücklegen", mix(R, seen, [(mit, 20)])),
        ("Ohne Zurücklegen", mix(R, seen, [(ohne, 20)])),
        ("Mindestens einmal", mix(R, seen, [(mindestens, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Ein <b>mehrstufiges Zufallsexperiment</b> besteht aus mehreren Teilexperimenten nacheinander. Man stellt es im <b>Baumdiagramm</b> dar.",
         "<b>Pfadregel</b>: Die Wahrscheinlichkeiten entlang eines Pfades werden multipliziert. <b>Summenregel</b>: Gehören mehrere Pfade zu einem Ereignis, werden ihre Wahrscheinlichkeiten addiert.",
         "<b>Ohne Zurücklegen</b> ändern sich die Wahrscheinlichkeiten von Stufe zu Stufe.",
         "„<b>Mindestens einmal</b>“ berechnet man am schnellsten über das Gegenereignis „keinmal“: P = 1 − P(keinmal)."],
        [example("Münze dreimal: P(KKK)", ["%s %s %s %s %s" % (bh(Fr(1, 2)), MAL, bh(Fr(1, 2)), MAL, bh(Fr(1, 2)))], bh(Fr(1, 8))),
         example("Würfel zweimal: mindestens eine 6", ["keine 6: %s %s %s = %s" % (bh(Fr(5, 6)), MAL, bh(Fr(5, 6)), bh(Fr(25, 36)))], "1 − %s = %s" % (bh(Fr(25, 36)), bh(Fr(11, 36))))],
        [["Pfad: %s + %s" % (bh(Fr(1, 2)), bh(Fr(1, 2))), "Entlang des Pfades multiplizieren"],
         ["Genau zweimal Kopf bei 3 Würfen: %s" % bh(Fr(1, 8)), "Drei Pfade (KKZ, KZK, ZKK): %s" % bh(Fr(3, 8))],
         ["Mindestens eine 6 bei 2 Würfen: %s" % bh(Fr(2, 6)), "1 − (%s)²" % bh(Fr(5, 6))]])
    faq = [
        {"q": "Was ist ein mehrstufiges Zufallsexperiment?", "a": "Mehrere Zufallsexperimente nacheinander, z. B. dreimal eine Münze werfen. Man zeichnet dafür ein Baumdiagramm."},
        {"q": "Wann multipliziere und wann addiere ich?", "a": "Entlang eines Pfades wird multipliziert (Pfadregel). Mehrere passende Pfade werden addiert (Summenregel)."},
        {"q": "Wie rechne ich „mindestens einmal“?", "a": "Mit dem Gegenereignis „keinmal“: P(mindestens einmal) = 1 − P(keinmal)."},
        {"q": "Wann ist ein Spiel fair?", "a": "Wenn der mittlere Gewinn genau dem Einsatz entspricht, also der Erwartungswert für den Spieler 0 € beträgt."},
    ]
    make_unit(R, "mehrstufige-zufallsexperimente", "D",
              "Die Schülerinnen und Schüler beschreiben mehrstufige Zufallsexperimente mit Baumdiagrammen, berechnen Wahrscheinlichkeiten mit Pfad- und Summenregel (mit und ohne Zurücklegen), nutzen Gegenereignisse und beurteilen Spiele (Zusammenfassung).",
              "Mehrstufige Zufallsexperimente",
              "Mehrstufige Zufallsexperimente Klasse 8 – Baumdiagramm, Pfadregel, Arbeitsblätter",
              "Baumdiagramme",
              "Wahrscheinlichkeit für Klasse 8: mehrstufige Baumdiagramme, Pfad- und Summenregel, mit und ohne Zurücklegen, mindestens einmal, faire Spiele. 100 Aufgaben mit Lösungen, kostenlos.",
              "Entlang des Pfades multiplizieren, Pfade addieren.",
              "Mindestens einmal = 1 − keinmal.",
              body, faq, sets, 14, grade="klasse-8")


if __name__ == "__main__":
    main()
