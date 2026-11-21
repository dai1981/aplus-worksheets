# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 9: Ähnlichkeit und zentrische Streckung（Leitidee Raum und Form, Sek I）
  python3 tools/gen_de_mathe_k9_aehnlichkeit_und_zentrische_streckung.py
Zentrische Streckung mit Zentrum Z und Faktor k (Vergrößerung, Verkleinerung), Bildstrecken, Streckfaktor bestimmen,
ähnliche Figuren und Dreiecke, Flächen (k²) und Volumen (k³), Maßstab.
Fehler: Bildlänge = Original + k, Fläche nur mit k statt k² vergrößert, k &lt; 1 für Vergrößerung gehalten, ähnliche Dreiecke nur an einem Winkel erkannt.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, num
from de_k6 import dz
from de_k9 import mcq
from de_k6 import bh, endlich


def zahl(v):
    v = Fr(v)
    return dz(v) if endlich(v) else bh(v)

R = random.Random(49909)
G = ":"


def strecke():
    k = Fr(R.choice([2, 3, 4, Fr(1, 2), Fr(3, 2), Fr(5, 2), Fr(1, 3), Fr(2, 3), Fr(1, 4)]))
    l = Fr(R.randint(2, 24))
    v = k * l
    if v.denominator != 1 and (v * 10).denominator != 1:
        return None
    kind = R.choice(["bild", "bild", "zentrum", "art"])
    if kind == "bild":
        return mcq("Eine Strecke ist %s cm lang. Sie wird mit dem Faktor k = %s zentrisch gestreckt. Wie lang ist die Bildstrecke?" % (dz(l), zahl(k)), "%s cm" % zahl(v),
                   ["%s cm" % zahl(l + k), "%s cm" % zahl(l / k), "%s cm" % zahl(k * k * l)],
                   "Bildlänge = k %s Originallänge = %s %s %s = <b>%s cm</b>." % (MAL, zahl(k), MAL, dz(l), zahl(v)))
    if kind == "zentrum":
        return mcq("Bei einer zentrischen Streckung mit Zentrum Z und k = %s ist ZA = %s cm. Wie lang ist ZA'?" % (zahl(k), dz(l)), "%s cm" % zahl(v),
                   ["%s cm" % zahl(v - l) if v != 2 * l else "%s cm" % zahl(v + l), "%s cm" % zahl(l / k), "%s cm" % zahl(l + k)],
                   "ZA' = k %s ZA = <b>%s cm</b>. A' liegt auf dem Strahl von Z durch A." % (MAL, zahl(v)))
    ans = "eine Vergrößerung" if k > 1 else "eine Verkleinerung"
    return mcq("Ist eine zentrische Streckung mit k = %s eine Vergrößerung oder eine Verkleinerung?" % zahl(k), ans, ["eine Verkleinerung" if k > 1 else "eine Vergrößerung", "eine Kongruenzabbildung", "eine Spiegelung"],
               "k %s 1: <b>%s</b>." % ("&gt;" if k > 1 else "&lt;", ans))


def faktor():
    kind = R.choice(["k", "k", "orig"])
    k = Fr(R.choice([2, 3, 4, 5, Fr(1, 2), Fr(3, 2), Fr(5, 2), Fr(1, 4), Fr(3, 4), Fr(2, 3)]))
    l = Fr(R.randint(2, 20))
    v = k * l
    if v.denominator != 1 and (v * 10).denominator != 1:
        return None
    if kind == "k":
        return mcq("Eine Strecke von %s cm wird auf %s cm gestreckt. Wie groß ist der Streckfaktor k?" % (dz(l), zahl(v)), "k = %s" % zahl(k),
                   ["k = %s" % zahl(1 / k), "k = %s" % zahl(v - l), "k = %s" % zahl(v * l) if (v * l) != k else "k = %s" % zahl(k + 1)],
                   "k = Bild %s Original = %s %s %s = <b>%s</b>." % (G, zahl(v), G, dz(l), zahl(k)))
    return mcq("Nach einer Streckung mit k = %s ist eine Strecke %s cm lang. Wie lang war sie vorher?" % (zahl(k), zahl(v)), "%s cm" % dz(l),
               ["%s cm" % zahl(v * k), "%s cm" % zahl(v - k), "%s cm" % zahl(v + k)],
               "Original = Bild %s k = %s %s %s = <b>%s cm</b>." % (G, zahl(v), G, zahl(k), dz(l)))


def aehnlich():
    kind = R.choice(["winkel", "seite", "seite", "pruef", "begriff"])
    if kind == "winkel":
        a, b = R.randint(25, 80), R.randint(25, 80)
        if a + b >= 170:
            return None
        return mcq("Zwei Dreiecke stimmen in den Winkeln %d° und %d° überein. Was gilt?" % (a, b), "Sie sind ähnlich, denn auch der dritte Winkel (%d°) ist gleich." % (180 - a - b),
                   ["Sie sind kongruent.", "Man braucht noch eine gleiche Seite, um Ähnlichkeit zu zeigen.", "Sie sind nur ähnlich, wenn sie gleich groß sind."],
                   "Zwei gleiche Winkel genügen: Der dritte ist dann auch gleich. <b>Ähnlich</b> (aber nicht unbedingt gleich groß).")
    if kind == "seite":
        a, b, c = R.choice([(3, 4, 5), (4, 5, 6), (5, 7, 8), (2, 3, 4), (6, 8, 9), (5, 6, 7)])
        k = Fr(R.choice([2, 3, Fr(3, 2), Fr(5, 2), 4]))
        if (k * a).denominator != 1 and (k * a * 10).denominator != 1:
            return None
        return mcq("Das Dreieck ABC hat die Seiten %d cm, %d cm und %d cm. Ein ähnliches Dreieck hat als kürzeste Seite %s cm. Wie lang ist seine längste Seite?" % (a, b, c, zahl(k * a)), "%s cm" % zahl(k * c),
                   ["%s cm" % zahl(c + k * a - a), "%s cm" % zahl(k * b), "%s cm" % zahl(c * k * k)],
                   "k = %s %s %d = %s. Längste Seite: %s %s %d = <b>%s cm</b>." % (zahl(k * a), G, a, zahl(k), zahl(k), MAL, c, zahl(k * c)))
    if kind == "pruef":
        a, b = R.choice([(4, 6), (3, 5), (6, 9), (8, 12), (5, 8), (10, 15)])
        k = R.choice([Fr(3, 2), 2, 3, Fr(5, 2)])
        ok = R.random() < 0.5
        c, d = (k * a, k * b) if ok else (k * a, k * b + 1)
        ans = "Ja, beide Seiten wurden mit %s multipliziert." % zahl(k) if ok else "Nein, die Seitenverhältnisse sind verschieden."
        return mcq("Ein Rechteck ist %d cm × %d cm groß, ein anderes %s cm × %s cm. Sind die Rechtecke ähnlich?" % (a, b, zahl(c), zahl(d)), ans,
                   ["Nein, die Seitenverhältnisse sind verschieden." if ok else "Ja, beide Seiten wurden mit %s multipliziert." % zahl(k), "Ja, alle Rechtecke sind ähnlich.", "Nein, ähnliche Figuren sind immer gleich groß."],
                   "%s %s %d = %s und %s %s %d = %s. <b>%s</b>" % (zahl(c), G, a, zahl(c / a), zahl(d), G, b, zahl(d / b), "Ja" if ok else "Nein"))
    q, a, w = R.choice([
        ("Welche Figuren sind immer zueinander ähnlich?", "zwei Quadrate", ["zwei Rechtecke", "zwei Dreiecke", "zwei Rauten"]),
        ("Welche Figuren sind immer zueinander ähnlich?", "zwei Kreise", ["zwei Ellipsen", "zwei Parallelogramme", "zwei Trapeze"]),
        ("Was bleibt bei einer zentrischen Streckung gleich?", "die Winkel", ["die Seitenlängen", "der Flächeninhalt", "der Umfang"]),
        ("Was bedeutet „ähnlich“ in der Geometrie?", "gleiche Form, Größe kann verschieden sein", ["gleiche Größe, Form kann verschieden sein", "gleicher Flächeninhalt", "gleicher Umfang"]),
        ("Eine Streckung hat k = 1. Was passiert?", "Die Figur bleibt gleich (Kongruenz).", ["Die Figur wird doppelt so groß.", "Die Figur verschwindet.", "Die Figur wird gespiegelt."]),
        ("Welche Figuren sind immer zueinander ähnlich?", "zwei gleichseitige Dreiecke", ["zwei gleichschenklige Dreiecke", "zwei rechtwinklige Dreiecke", "zwei Rechtecke"]),
    ])
    return mcq(q, a, w, "<b>%s</b>" % a)


def flaeche_volumen():
    k = R.choice([2, 3, 4, 5, 10, Fr(1, 2), Fr(3, 2)])
    k = Fr(k)
    kind = R.choice(["A", "A", "V", "faktor", "umfang"])
    if kind == "A":
        A = Fr(R.randint(2, 30))
        v = A * k * k
        if v.denominator != 1 and (v * 100).denominator != 1:
            return None
        return mcq("Eine Figur mit dem Flächeninhalt %s cm² wird mit k = %s gestreckt. Wie groß ist der neue Flächeninhalt?" % (dz(A), zahl(k)), "%s cm²" % dz(v),
                   ["%s cm²" % dz(A * k) if (A * k * 100).denominator == 1 else "%s cm²" % dz(A + k), "%s cm²" % dz(A * k ** 3) if (A * k ** 3 * 1000).denominator == 1 else "%s cm²" % dz(A + 1), "%s cm²" % dz(A + k * k)],
                   "Flächen wachsen mit k²: %s %s %s = <b>%s cm²</b>." % (dz(A), MAL, zahl(k * k), dz(v)))
    if kind == "V":
        V = Fr(R.randint(2, 20))
        v = V * k ** 3
        if (v * 1000).denominator != 1:
            return None
        return mcq("Ein Körper mit dem Volumen %s cm³ wird mit k = %s gestreckt. Wie groß ist das neue Volumen?" % (dz(V), zahl(k)), "%s cm³" % dz(v),
                   ["%s cm³" % dz(V * k) if (V * k * 100).denominator == 1 else "%s cm³" % dz(V + 1), "%s cm³" % dz(V * k * k) if (V * k * k * 100).denominator == 1 else "%s cm³" % dz(V + 2), "%s cm³" % dz(V + k ** 3) if (V + k ** 3) != v else "%s cm³" % dz(V + 3)],
                   "Volumen wachsen mit k³: %s %s %s = <b>%s cm³</b>." % (dz(V), MAL, zahl(k ** 3), dz(v)))
    if kind == "umfang":
        u = R.randint(5, 40)
        if (k * u * 10).denominator != 1:
            return None
        return mcq("Ein Vieleck hat den Umfang %d cm. Es wird mit k = %s gestreckt. Wie groß ist der neue Umfang?" % (u, zahl(k)), "%s cm" % zahl(k * u), ["%s cm" % zahl(k * k * u), "%s cm" % zahl(u + k), "%d cm" % u],
                   "Längen (auch der Umfang) wachsen mit k: <b>%s cm</b>." % zahl(k * u))
    m = R.choice([2, 3, 4, 5])
    return mcq("Eine Figur wird so gestreckt, dass ihr Flächeninhalt %d-mal so groß ist wie vorher. Wie groß ist der Streckfaktor k?" % (m * m), "k = %d" % m,
               ["k = %d" % (m * m), "k = %d" % (m * m // 2), "k = %d" % (m + 1)], "A wächst mit k². k² = %d ⇒ <b>k = %d</b>." % (m * m, m))


def massstab():
    kind = R.choice(["karte", "karte", "modell", "zurueck"])
    if kind == "karte":
        m = R.choice([10000, 25000, 50000, 100000, 200000])
        c = R.choice([2, 3, 4, 5, 6, 8, Fr(5, 2), Fr(3, 2)])
        km = Fr(c) * m / 100000
        return mcq("Auf einer Karte im Maßstab 1 : %s sind zwei Orte %s cm voneinander entfernt. Wie weit ist das in Wirklichkeit?" % (num(m), dz(c)), "%s km" % dz(km),
                   ["%s km" % dz(km * 10), "%s km" % dz(km / 10), "%s km" % dz(km * 100)],
                   "%s cm %s %s = %s cm = <b>%s km</b>." % (dz(c), MAL, num(m), num(int(Fr(c) * m)), dz(km)))
    if kind == "modell":
        m = R.choice([87, 50, 20, 100, 25])
        l = R.choice([20, 25, 30, 40, 15])
        return mcq("Ein Modellauto im Maßstab 1 : %d ist %d cm lang. Wie lang ist das echte Auto?" % (m, l) if m in (20, 25) else "Ein Modell im Maßstab 1 : %d ist %d cm lang. Wie lang ist das Original?" % (m, l),
                   "%s m" % dz(Fr(l * m, 100)), ["%s m" % dz(Fr(l * m, 1000)), "%s m" % dz(Fr(l + m, 100)), "%s m" % dz(Fr(l * m, 10))],
                   "%d cm %s %d = %s cm = <b>%s m</b>." % (l, MAL, m, num(l * m), dz(Fr(l * m, 100))))
    m = R.choice([25000, 50000, 100000])
    km = R.choice([1, 2, 3, 5, Fr(3, 2), Fr(5, 2)])
    c = Fr(km) * 100000 / m
    return mcq("Eine Strecke ist in Wirklichkeit %s km lang. Wie lang ist sie auf einer Karte im Maßstab 1 : %s?" % (dz(km), num(m)), "%s cm" % dz(c),
               ["%s cm" % dz(c * 10), "%s cm" % dz(c / 10), "%s mm" % dz(c)], "%s km = %s cm, geteilt durch %s: <b>%s cm</b>." % (dz(km), num(int(Fr(km) * 100000)), num(m), dz(c)))


def main():
    seen = set()
    sets = [
        ("Zentrische Streckung", mix(R, seen, [(strecke, 20)])),
        ("Streckfaktor bestimmen", mix(R, seen, [(faktor, 20)])),
        ("Ähnliche Figuren", mix(R, seen, [(aehnlich, 20)])),
        ("Flächen und Volumen", mix(R, seen, [(flaeche_volumen, 20)])),
        ("Maßstab", mix(R, seen, [(massstab, 20)])),
    ]
    body = lesson(
        ["Bei einer <b>zentrischen Streckung</b> mit Zentrum Z und Faktor k liegt der Bildpunkt A' auf dem Strahl ZA, und es gilt ZA' = k %s ZA." % MAL,
         "k &gt; 1: Vergrößerung, 0 &lt; k &lt; 1: Verkleinerung. Alle Längen werden mit k multipliziert, Winkel bleiben gleich.",
         "Figuren, die durch Streckung (und Bewegung) auseinander hervorgehen, sind <b>ähnlich</b>. Dreiecke sind ähnlich, wenn zwei Winkel übereinstimmen.",
         "Flächeninhalte ändern sich mit k², Volumen mit k³."],
        [example("Strecke 6 cm, k = 2,5", ["6 %s 2,5" % MAL], "15 cm"),
         example("Fläche 12 cm², k = 3", ["12 %s 3² = 12 %s 9" % (MAL, MAL)], "108 cm²")],
        [["k = 3: Bildlänge = Länge + 3", "Bildlänge = 3 %s Länge" % MAL],
         ["Fläche mit k multiplizieren", "Fläche mit k² multiplizieren"],
         ["Alle Rechtecke sind ähnlich", "Nur bei gleichem Seitenverhältnis"]])
    faq = [
        {"q": "Was ist eine zentrische Streckung?", "a": "Eine Abbildung mit einem Zentrum Z und einem Faktor k: Jeder Punkt wird auf dem Strahl von Z aus so verschoben, dass sein Abstand von Z k-mal so groß wird."},
        {"q": "Wann sind zwei Figuren ähnlich?", "a": "Wenn sie die gleiche Form haben: gleiche Winkel und gleiche Seitenverhältnisse. Die Größe darf verschieden sein."},
        {"q": "Wie ändert sich der Flächeninhalt bei einer Streckung?", "a": "Er wird mit k² multipliziert. Das Volumen eines Körpers mit k³."},
        {"q": "Was bedeutet der Maßstab 1 : 50 000?", "a": "1 cm auf der Karte entspricht 50 000 cm = 500 m in der Wirklichkeit."},
    ]
    make_unit(R, "aehnlichkeit-und-zentrische-streckung", "R",
              "Die Schülerinnen und Schüler führen zentrische Streckungen durch, bestimmen Streckfaktoren, erkennen und begründen Ähnlichkeit, berechnen Längen, Flächen und Volumen ähnlicher Figuren und nutzen Maßstäbe (Zusammenfassung).",
              "Ähnlichkeit und zentrische Streckung",
              "Zentrische Streckung und Ähnlichkeit Klasse 9 – Streckfaktor, Arbeitsblätter",
              "Zentrische Streckung",
              "Ähnlichkeit für Klasse 9: zentrische Streckung, Streckfaktor, ähnliche Figuren und Dreiecke, Flächen mit k², Volumen mit k³ und Maßstab. 100 Aufgaben mit Lösungen, kostenlos.",
              "Längen · k, Flächen · k², Volumen · k³",
              "Ähnliche Figuren: gleiche Winkel, gleiche Seitenverhältnisse.",
              body, faq, sets, 9, grade="klasse-9")


if __name__ == "__main__":
    main()
