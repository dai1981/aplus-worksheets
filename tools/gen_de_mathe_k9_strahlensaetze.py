# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 9: Strahlensätze（Leitidee Raum und Form, Sek I）
  python3 tools/gen_de_mathe_k9_strahlensaetze.py
1. Strahlensatz (Abschnitte auf den Strahlen), 2. Strahlensatz (Parallelen und Strahlabschnitte), V-Figur (X-Figur),
richtige Verhältnisgleichung erkennen, Sachaufgaben (Baumhöhe mit Schatten, Flussbreite, Försterdreieck, Daumensprung).
Fehler: Teilstrecke statt ganzer Strecke beim 2. Strahlensatz, Verhältnisse über Kreuz vertauscht, Parallelen mit Strahlabschnitten des falschen Strahls.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, wrap, line, text, INK, BLUE, RED, GREEN
from de_k6 import dz, bh, endlich
from de_k9 import mcq, zr

R = random.Random(49910)
G = ":"


def zahl(v):
    v = Fr(v)
    return dz(v) if endlich(v) else zr(v, 1)


def ov(s):
    return "<span class='ov'>%s</span>" % s


def figur(labels, label="Strahlensatzfigur"):
    """Z links, Strahl 1 nach oben rechts (A, A'), Strahl 2 nach unten rechts (B, B'), AB ∥ A'B'.
    labels: dict ZA, AA', ZB, BB', AB, A'B' -> Text"""
    Z = (24, 110)
    A, A2 = (150, 60), (300, 0 + 8)
    B, B2 = (150, 150), (300, 196)
    s = [line(Z[0], Z[1], A2[0] + 14, A2[1] - 5, INK, 2.2), line(Z[0], Z[1], B2[0] + 14, B2[1] + 5, INK, 2.2),
         line(A[0], A[1], B[0], B[1], BLUE, 2.6), line(A2[0], A2[1], B2[0], B2[1], BLUE, 2.6)]
    for p, n, dx, dy in [(Z, "Z", -16, 6), (A, "A", -6, -12), (A2, "A'", 22, 16), (B, "B", -6, 24), (B2, "B'", 22, -4)]:
        s.append("<circle cx='%d' cy='%d' r='3.5' fill='%s'/>" % (p[0], p[1], INK) + text(p[0] + dx, p[1] + dy, n, 18))
    pos = {"ZA": ((Z[0] + A[0]) / 2 - 6, (Z[1] + A[1]) / 2 - 10), "AA'": ((A[0] + A2[0]) / 2 - 6, (A[1] + A2[1]) / 2 - 10),
           "ZB": ((Z[0] + B[0]) / 2 - 4, (Z[1] + B[1]) / 2 + 22), "BB'": ((B[0] + B2[0]) / 2, (B[1] + B2[1]) / 2 + 22),
           "AB": (A[0] + 12, (A[1] + B[1]) / 2 + 5), "A'B'": (A2[0] + 14, (A2[1] + B2[1]) / 2 + 5)}
    for k, v in labels.items():
        x, y = pos[k]
        s.append(text(x, y, v, 19, col=RED if k in ("AB", "A'B'") else GREEN, anchor="start" if k in ("AB", "A'B'") else "middle"))
    return wrap(400, 216, "".join(s), label, lg=True)


def werte():
    za = R.randint(2, 9)
    k = Fr(R.choice([2, 3, Fr(3, 2), Fr(5, 2), Fr(4, 3), Fr(5, 3), Fr(7, 4)]))
    za2 = k * za
    zb = R.randint(2, 9)
    zb2 = k * zb
    ab = R.randint(2, 8)
    ab2 = k * ab
    for v in (za2, zb2, ab2):
        if not endlich(v) or (v * 10).denominator != 1:
            return None
    return za, za2, zb, zb2, ab, ab2


def erster():
    w = werte()
    if not w:
        return None
    za, za2, zb, zb2, ab, ab2 = w
    kind = R.choice(["zb2", "zb2", "teil", "za2"])
    if kind == "zb2":
        pic = figur({"ZA": "%s" % zahl(za), "AA'": "%s" % zahl(za2 - za), "ZB": "%s" % zahl(zb), "BB'": "?"})
        return mcq(pic + "AB ∥ A'B' (Längen in cm). Berechne %s." % ov("BB'"), "%s cm" % zahl(zb2 - zb),
                   ["%s cm" % zahl(zb2), "%s cm" % zahl(za2 - za), "%s cm" % zahl(zb * za / (za2 - za)) if zb * za / (za2 - za) != zb2 - zb else "%s cm" % zahl(zb2 - zb + 1)],
                   "1. Strahlensatz: %s : %s = %s : %s ⇒ %s = %s %s %s : %s = <b>%s cm</b>." % (ov("BB'"), ov("ZB"), ov("AA'"), ov("ZA"), ov("BB'"), zahl(zb), MAL, zahl(za2 - za), zahl(za), zahl(zb2 - zb)))
    if kind == "teil":
        return mcq("AB ∥ A'B'. Es ist %s = %s cm, %s = %s cm und %s = %s cm. Wie lang ist %s?" % (ov("ZA"), zahl(za), ov("ZA'"), zahl(za2), ov("ZB"), zahl(zb), ov("ZB'")), "%s cm" % zahl(zb2),
                   ["%s cm" % zahl(zb2 - zb), "%s cm" % zahl(zb * za / za2), "%s cm" % zahl(zb + za2 - za)],
                   "%s : %s = %s : %s ⇒ %s = %s %s %s : %s = <b>%s cm</b>." % (ov("ZB'"), ov("ZB"), ov("ZA'"), ov("ZA"), ov("ZB'"), zahl(zb), MAL, zahl(za2), zahl(za), zahl(zb2)))
    pic = figur({"ZA": "%s" % zahl(za), "ZB": "%s" % zahl(zb), "BB'": "%s" % zahl(zb2 - zb), "AA'": "?"})
    return mcq(pic + "AB ∥ A'B' (Längen in cm). Berechne %s." % ov("AA'"), "%s cm" % zahl(za2 - za),
               ["%s cm" % zahl(za2), "%s cm" % zahl(zb2 - zb) if zb2 - zb != za2 - za else "%s cm" % zahl(za2 - za + 1), "%s cm" % zahl(za + zb2 - zb - zb) if za + zb2 - 2 * zb > 0 and za + zb2 - 2 * zb != za2 - za else "%s cm" % zahl(za2 + 1)],
               "%s : %s = %s : %s ⇒ %s = %s %s %s : %s = <b>%s cm</b>." % (ov("AA'"), ov("ZA"), ov("BB'"), ov("ZB"), ov("AA'"), zahl(za), MAL, zahl(zb2 - zb), zahl(zb), zahl(za2 - za)))


def zweiter():
    w = werte()
    if not w:
        return None
    za, za2, zb, zb2, ab, ab2 = w
    kind = R.choice(["ab2", "ab2", "ab", "za2"])
    if kind == "ab2":
        pic = figur({"ZA": "%s" % zahl(za), "AA'": "%s" % zahl(za2 - za), "AB": "%s" % zahl(ab), "A'B'": "?"})
        return mcq(pic + "AB ∥ A'B' (Längen in cm). Berechne %s." % ov("A'B'"), "%s cm" % zahl(ab2),
                   ["%s cm" % zahl(ab * (za2 - za) / za), "%s cm" % zahl(ab + za2 - za), "%s cm" % zahl(ab * za / za2)],
                   "2. Strahlensatz mit den <b>ganzen</b> Strecken ab Z: %s : %s = %s : %s ⇒ %s = %s %s %s : %s = <b>%s cm</b>." % (ov("A'B'"), ov("AB"), ov("ZA'"), ov("ZA"), ov("A'B'"), zahl(ab), MAL, zahl(za2), zahl(za), zahl(ab2)))
    if kind == "ab":
        return mcq("AB ∥ A'B'. Es ist %s = %s cm, %s = %s cm und %s = %s cm. Wie lang ist %s?" % (ov("ZA"), zahl(za), ov("ZA'"), zahl(za2), ov("A'B'"), zahl(ab2), ov("AB")), "%s cm" % zahl(ab),
                   ["%s cm" % zahl(ab2 * za2 / za), "%s cm" % zahl(ab2 - (za2 - za)) if ab2 > za2 - za and ab2 - (za2 - za) != ab else "%s cm" % zahl(ab + 1), "%s cm" % zahl(ab2 * (za2 - za) / za2)],
                   "%s : %s = %s : %s ⇒ %s = %s %s %s : %s = <b>%s cm</b>." % (ov("AB"), ov("A'B'"), ov("ZA"), ov("ZA'"), ov("AB"), zahl(ab2), MAL, zahl(za), zahl(za2), zahl(ab)))
    return mcq("AB ∥ A'B'. Es ist %s = %s cm, %s = %s cm und %s = %s cm. Wie lang ist %s?" % (ov("ZA"), zahl(za), ov("AB"), zahl(ab), ov("A'B'"), zahl(ab2), ov("ZA'")), "%s cm" % zahl(za2),
               ["%s cm" % zahl(za2 - za), "%s cm" % zahl(za * ab / ab2), "%s cm" % zahl(za + ab2 - ab)],
               "%s : %s = %s : %s ⇒ %s = %s %s %s : %s = <b>%s cm</b>." % (ov("ZA'"), ov("ZA"), ov("A'B'"), ov("AB"), ov("ZA'"), zahl(za), MAL, zahl(ab2), zahl(ab), zahl(za2)))


def gleichung():
    opts_ok = [("%s : %s = %s : %s" % (ov("ZA"), ov("ZA'"), ov("ZB"), ov("ZB'")), "1. Strahlensatz"),
               ("%s : %s = %s : %s" % (ov("ZA"), ov("AA'"), ov("ZB"), ov("BB'")), "1. Strahlensatz (Teilstrecken)"),
               ("%s : %s = %s : %s" % (ov("AB"), ov("A'B'"), ov("ZA"), ov("ZA'")), "2. Strahlensatz"),
               ("%s : %s = %s : %s" % (ov("A'B'"), ov("AB"), ov("ZB'"), ov("ZB")), "2. Strahlensatz")]
    wrong = ["%s : %s = %s : %s" % (ov("AB"), ov("A'B'"), ov("ZA"), ov("AA'")),
             "%s : %s = %s : %s" % (ov("ZA"), ov("ZA'"), ov("ZB'"), ov("ZB")),
             "%s : %s = %s : %s" % (ov("AB"), ov("A'B'"), ov("AA'"), ov("BB'")),
             "%s : %s = %s : %s" % (ov("A'B'"), ov("AB"), ov("ZB"), ov("ZB'")),
             "%s : %s = %s : %s" % (ov("ZA"), ov("ZB'"), ov("ZB"), ov("ZA'"))]
    a, why = R.choice(opts_ok)
    kind = R.choice(["richtig", "falsch"])
    if kind == "richtig":
        return mcq("AB ∥ A'B', Z ist der Scheitel der Strahlen. Welche Verhältnisgleichung ist richtig?", a, R.sample(wrong, 3), "<b>%s</b> (%s)." % (a, why))
    wq = R.choice(wrong)
    oks = R.sample([o for o, _ in opts_ok], 3)
    return mcq("AB ∥ A'B', Z ist der Scheitel der Strahlen. Welche Verhältnisgleichung ist <b>falsch</b>?", wq, oks,
               "Beim 2. Strahlensatz müssen die Strahlabschnitte ab Z gemessen werden, und auf beiden Seiten muss die Reihenfolge gleich sein. <b>%s</b> ist falsch." % wq)


def xfigur():
    w = werte()
    if not w:
        return None
    za, za2, zb, zb2, ab, ab2 = w
    kind = R.choice(["par", "strahl"])
    intro = "Die Geraden AA' und BB' schneiden sich in Z (X-Figur, A und A' auf verschiedenen Seiten von Z), und AB ∥ A'B'. "
    if kind == "par":
        return mcq(intro + "Es ist %s = %s cm, %s = %s cm und %s = %s cm. Wie lang ist %s?" % (ov("ZA"), zahl(za), ov("ZA'"), zahl(za2), ov("AB"), zahl(ab), ov("A'B'")), "%s cm" % zahl(ab2),
                   ["%s cm" % zahl(ab * za / za2), "%s cm" % zahl(ab + za2 - za), "%s cm" % zahl(ab * (za + za2) / za)],
                   "Auch in der X-Figur: %s : %s = %s : %s ⇒ <b>%s cm</b>." % (ov("A'B'"), ov("AB"), ov("ZA'"), ov("ZA"), zahl(ab2)))
    return mcq(intro + "Es ist %s = %s cm, %s = %s cm und %s = %s cm. Wie lang ist %s?" % (ov("ZA"), zahl(za), ov("ZA'"), zahl(za2), ov("ZB"), zahl(zb), ov("ZB'")), "%s cm" % zahl(zb2),
               ["%s cm" % zahl(zb * za / za2), "%s cm" % zahl(zb + za2 - za), "%s cm" % zahl(zb2 + zb)],
               "%s : %s = %s : %s ⇒ %s = %s %s %s : %s = <b>%s cm</b>." % (ov("ZB'"), ov("ZB"), ov("ZA'"), ov("ZA"), ov("ZB'"), zahl(zb), MAL, zahl(za2), zahl(za), zahl(zb2)))


def sache():
    kind = R.choice(["baum", "baum", "fluss", "daumen", "foerster", "stab"])
    if kind in ("baum", "stab"):
        h, s = R.choice([(Fr(1), Fr(3, 2)), (Fr(2), Fr(3)), (Fr(3, 2), Fr(2)), (Fr(1), Fr(4, 5)), (Fr(2), Fr(5, 2))])
        S = s * R.choice([6, 8, 10, 12, 15, 20])
        H = h * S / s
        obj = R.choice(["ein Baum", "ein Turm", "ein Fahnenmast"]) if kind == "baum" else "eine Laterne"
        return mcq("Ein %s m langer Stab wirft einen %s m langen Schatten. Zur gleichen Zeit wirft %s einen %s m langen Schatten. Wie hoch ist %s?" % (dz(h), dz(s), obj, dz(S), obj.replace("ein ", "der ").replace("eine ", "die ")),
                   "%s m" % zahl(H), ["%s m" % zahl(S * s / h), "%s m" % zahl(S - s + h), "%s m" % zahl(S)],
                   "H : %s = %s : %s ⇒ H = %s %s %s : %s = <b>%s m</b>." % (dz(S), dz(h), dz(s), dz(h), MAL, dz(S), dz(s), zahl(H)))
    if kind == "fluss":
        a, b, c = R.choice([(Fr(5), Fr(15), Fr(10)), (Fr(4), Fr(20), Fr(6)), (Fr(6), Fr(18), Fr(8)), (Fr(8), Fr(24), Fr(10)), (Fr(5), Fr(30), Fr(12))])
        x = b * c / a
        return mcq("Um die Breite x eines Flusses zu messen, steckt man Stäbe ab. Mit den Strahlensätzen ergibt sich x : %s = %s : %s (in m). Wie breit ist der Fluss?" % (dz(c), dz(b), dz(a)), "%s m" % zahl(x),
                   ["%s m" % zahl(a * c / b), "%s m" % zahl(b + c - a), "%s m" % zahl(b * a / c)], "x = %s %s %s : %s = <b>%s m</b>." % (dz(c), MAL, dz(b), dz(a), zahl(x)))
    if kind == "daumen":
        e = R.choice([60, 65, 70])
        sprung = R.choice([30, 40, 50, 60])
        aug = 6
        d = Fr(sprung * e, aug)
        return mcq("Beim Daumensprung ist der Arm %d cm lang, der Augenabstand 6 cm. Der Daumen springt in der Ferne %d m weit. Wie weit ist das Ziel entfernt?" % (e, sprung), "%s m" % zahl(d),
                   ["%s m" % zahl(Fr(sprung * aug, e)), "%s m" % zahl(Fr(sprung, 6)), "%s m" % zahl(Fr(sprung * e, 100))],
                   "Entfernung : %d m = %d cm : 6 cm ⇒ Entfernung = %d %s %d : 6 = <b>%s m</b>." % (sprung, e, sprung, MAL, e, zahl(d)))
    a = R.choice([20, 25, 30])
    d = R.choice([15, 20, 25, 30])
    return mcq("Ein Förster peilt mit einem Försterdreieck: Bei %d cm waagrechter Länge geht die Peillinie %d cm nach oben. Er steht %d m vom Baum entfernt, seine Augen sind 1,5 m hoch. Wie hoch ist der Baum?" % (a, a, d),
               "%s m" % zahl(Fr(d) + Fr(3, 2)), ["%s m" % zahl(Fr(d)), "%s m" % zahl(Fr(d) - Fr(3, 2)), "%s m" % zahl(Fr(d) * 2)],
               "Die Kathetenlängen sind gleich, also ist die Höhe über den Augen gleich der Entfernung: %d m. Plus 1,5 m: <b>%s m</b>." % (d, zahl(Fr(d) + Fr(3, 2))))


def main():
    seen = set()
    sets = [
        ("1. Strahlensatz", mix(R, seen, [(erster, 20)])),
        ("2. Strahlensatz", mix(R, seen, [(zweiter, 20)])),
        ("X-Figur und Verhältnisgleichungen", mix(R, seen, [(gleichung, 2), (xfigur, 18)])),
        ("Gemischte Aufgaben", mix(R, seen, [(erster, 10), (zweiter, 10)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Zwei Strahlen mit gemeinsamem Anfangspunkt Z werden von zwei <b>Parallelen</b> AB und A'B' geschnitten.",
         "<b>1. Strahlensatz</b>: Die Abschnitte auf den Strahlen stehen im gleichen Verhältnis: %s : %s = %s : %s." % (ov("ZA"), ov("ZA'"), ov("ZB"), ov("ZB'")),
         "<b>2. Strahlensatz</b>: Die Parallelen stehen im gleichen Verhältnis wie die Strahlabschnitte <b>ab Z</b>: %s : %s = %s : %s." % (ov("AB"), ov("A'B'"), ov("ZA"), ov("ZA'")),
         "Das gilt auch, wenn sich die Geraden in Z kreuzen (X-Figur)."],
        [example("ZA = 4, ZA' = 10, AB = 3", ["A'B' : 3 = 10 : 4"], "A'B' = 7,5"),
         example("ZA = 4, AA' = 6, ZB = 5", ["BB' : 5 = 6 : 4"], "BB' = 7,5")],
        [["A'B' : AB = AA' : ZA", "Beim 2. Strahlensatz ganze Strecken ab Z: ZA' : ZA"],
         ["ZA : ZA' = ZB' : ZB", "Gleiche Reihenfolge auf beiden Seiten"],
         ["Strahlensatz ohne Parallelen", "Die Parallelität ist Voraussetzung"]])
    faq = [
        {"q": "Was sagt der 1. Strahlensatz?", "a": "Werden zwei Strahlen von Parallelen geschnitten, verhalten sich die Abschnitte auf dem einen Strahl wie die entsprechenden Abschnitte auf dem anderen."},
        {"q": "Was sagt der 2. Strahlensatz?", "a": "Die Abschnitte auf den Parallelen verhalten sich wie die zugehörigen Strahlabschnitte, gemessen vom Scheitel Z."},
        {"q": "Was ist der häufigste Fehler?", "a": "Beim 2. Strahlensatz eine Teilstrecke wie AA' statt der ganzen Strecke ZA' zu verwenden."},
        {"q": "Wofür braucht man die Strahlensätze?", "a": "Um unzugängliche Längen zu messen: Höhe eines Baumes mit dem Schatten, Breite eines Flusses, Entfernungen mit dem Daumensprung."},
    ]
    make_unit(R, "strahlensaetze", "R",
              "Die Schülerinnen und Schüler wenden den 1. und 2. Strahlensatz in V- und X-Figuren an, stellen passende Verhältnisgleichungen auf und berechnen unzugängliche Längen in Sachsituationen (Zusammenfassung).",
              "Strahlensätze",
              "Strahlensätze Klasse 9 – 1. und 2. Strahlensatz, Arbeitsblätter mit Lösungen",
              "Strahlensätze",
              "Strahlensätze für Klasse 9: 1. und 2. Strahlensatz, Verhältnisgleichungen aufstellen und Sachaufgaben wie Baumhöhe, Flussbreite und Daumensprung. 100 Aufgaben mit Lösungen, kostenlos.",
              "ZA : ZA' = ZB : ZB' = AB : A'B'",
              "Beim 2. Strahlensatz immer ab Z messen.",
              body, faq, sets, 10, grade="klasse-9")


if __name__ == "__main__":
    main()
