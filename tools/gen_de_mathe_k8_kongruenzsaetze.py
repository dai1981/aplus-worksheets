# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 8: Kongruente Dreiecke und Kongruenzsätze（Leitidee Raum und Form, Sek I）
  python3 tools/gen_de_mathe_k8_kongruenzsaetze.py
Kongruenz (deckungsgleich), Kongruenzsätze SSS, SWS, WSW und SsW, eindeutige Konstruierbarkeit, Dreiecksungleichung,
einander entsprechende Seiten und Winkel, Begründen mit Kongruenz.
Fehler: WWW für ausreichend gehalten, SsW mit dem Winkel an der kürzeren Seite, beim Zuordnen die Reihenfolge der Ecken nicht beachtet.
"""
import random
from de_common import lesson, example, make_unit, mix, wrap, line, text, INK, BLUE, RED, GREEN, FILL
from de_k8 import mcq

R = random.Random(49810)
CM = " cm"
SAETZE = ["SSS", "SWS", "WSW", "SsW"]
GEG = {"a": "b", "b": "a"}


def tri_svg(given):
    """Dreieck ABC, given: Liste der markierten Stücke (a, b, c, α, β, γ) mit Text"""
    A, B, C = (40, 170), (300, 170), (190, 40)
    s = ["<polygon points='%d,%d %d,%d %d,%d' fill='%s' stroke='%s' stroke-width='2.5'/>" % (A + B + C + (FILL, GREEN))]
    s.append(text(A[0] - 12, A[1] + 16, "A", 15) + text(B[0] + 12, B[1] + 16, "B", 15) + text(C[0], C[1] - 10, "C", 15))
    pos = {"c": ((A[0] + B[0]) / 2, A[1] + 22), "a": ((B[0] + C[0]) / 2 + 20, (B[1] + C[1]) / 2), "b": ((A[0] + C[0]) / 2 - 22, (A[1] + C[1]) / 2),
           "α": (A[0] + 40, A[1] - 10), "β": (B[0] - 38, B[1] - 10), "γ": (C[0], C[1] + 32)}
    for k, v in given:
        x, y = pos[k]
        col = RED if k in "αβγ" else BLUE
        s.append(text(x, y, v, 13, col=col, anchor="middle"))
    return wrap(340, 200, "".join(s), "Dreieck ABC mit gegebenen Stücken", lg=True)


def wl():
    return R.randint(25, 95)


def sl():
    return R.randint(3, 12)


def gegeben(satz):
    if satz == "SSS":
        while True:
            a, b, c = sl(), sl(), sl()
            if a + b > c and a + c > b and b + c > a:
                return [("a", "a = %d%s" % (a, CM)), ("b", "b = %d%s" % (b, CM)), ("c", "c = %d%s" % (c, CM))]
    if satz == "SWS":
        x, y, w = R.choice([("a", "b", "γ"), ("b", "c", "α"), ("a", "c", "β")])
        return [(x, "%s = %d%s" % (x, sl(), CM)), (y, "%s = %d%s" % (y, sl(), CM)), (w, "%s = %d°" % (w, wl()))]
    if satz == "WSW":
        sd, w1, w2 = R.choice([("c", "α", "β"), ("a", "β", "γ"), ("b", "α", "γ")])
        v1, v2 = wl(), wl()
        if v1 + v2 >= 170:
            v2 = 170 - v1 - 10
        return [(sd, "%s = %d%s" % (sd, sl(), CM)), (w1, "%s = %d°" % (w1, v1)), (w2, "%s = %d°" % (w2, v2))]
    # SsW: zwei Seiten, Winkel gegenüber der längeren
    x, y, w = R.choice([("a", "b", "α"), ("b", "a", "β"), ("c", "a", "γ"), ("a", "c", "α"), ("b", "c", "β"), ("c", "b", "γ")])
    lx = R.randint(6, 12)
    ly = R.randint(3, lx - 1)
    return [(x, "%s = %d%s" % (x, lx, CM)), (y, "%s = %d%s" % (y, ly, CM)), (w, "%s = %d°" % (w, R.randint(30, 110)))]


WHY = {"SSS": "Alle drei Seiten sind gegeben.", "SWS": "Zwei Seiten und der Winkel dazwischen sind gegeben.",
       "WSW": "Eine Seite und die beiden anliegenden Winkel sind gegeben.", "SsW": "Zwei Seiten und der Winkel gegenüber der längeren Seite sind gegeben."}


def welcher():
    satz = R.choice(SAETZE)
    g = gegeben(satz)
    R.shuffle(g)
    txt = ", ".join(v for _, v in g)
    pic = tri_svg(g) if R.random() < 0.5 else ""
    return mcq(pic + "Von einem Dreieck ABC sind gegeben: %s. Nach welchem Kongruenzsatz ist es eindeutig konstruierbar?" % txt, satz, [v for v in SAETZE if v != satz],
               "%s <b>%s</b>" % (WHY[satz], satz))


def reicht():
    kind = R.choice(["www", "ssw_kurz", "ssw_lang", "sws", "sww", "ungl", "ungl_ok", "zwei"])
    if kind == "www":
        a, b = wl(), wl()
        if a + b >= 170:
            return None
        return mcq("Von einem Dreieck sind nur die drei Winkel bekannt: α = %d°, β = %d°, γ = %d°. Ist das Dreieck eindeutig bestimmt?" % (a, b, 180 - a - b),
                   "Nein, die Form steht fest, aber nicht die Größe.", ["Ja, nach WSW.", "Ja, nach SSS.", "Nein, die Winkelsumme stimmt nicht."],
                   "Mit drei Winkeln gibt es viele ähnliche Dreiecke verschiedener Größe. <b>Nein</b> – es fehlt eine Seite.")
    if kind == "ssw_kurz":
        lx = R.randint(6, 12)
        ly = R.randint(3, lx - 2)
        w = R.randint(25, 50)
        return mcq("Gegeben: a = %d cm, b = %d cm und β = %d°. Ist das Dreieck eindeutig bestimmt?" % (lx, ly, w), "Nein, β liegt der kürzeren Seite gegenüber.",
                   ["Ja, nach SsW.", "Ja, nach SWS.", "Nein, weil zwei Seiten nie reichen."],
                   "β liegt b gegenüber, und b = %d cm ist die kürzere Seite. Dann kann es zwei Dreiecke geben. <b>Nein</b>" % ly)
    if kind == "ssw_lang":
        lx = R.randint(6, 12)
        ly = R.randint(3, lx - 1)
        w = R.randint(30, 110)
        return mcq("Gegeben: a = %d cm, b = %d cm und α = %d°. Ist das Dreieck eindeutig bestimmt?" % (lx, ly, w), "Ja, nach SsW.",
                   ["Nein, α liegt der kürzeren Seite gegenüber.", "Ja, nach SWS.", "Nein, es fehlt eine dritte Seite."],
                   "α liegt a gegenüber, und a = %d cm ist die längere Seite: <b>SsW</b>." % lx)
    if kind == "sws":
        return mcq("Gegeben: b = %d cm, c = %d cm und α = %d°. Ist das Dreieck eindeutig bestimmt?" % (sl(), sl(), wl()), "Ja, nach SWS.",
                   ["Ja, nach SsW.", "Nein, α liegt keiner Seite gegenüber.", "Nein, es fehlt eine Seite."],
                   "α liegt zwischen b und c (an der Ecke A): <b>SWS</b>.")
    if kind == "sww":
        a, b = wl(), wl()
        if a + b >= 170:
            return None
        return mcq("Gegeben: a = %d cm, α = %d° und β = %d°. Ist das Dreieck eindeutig bestimmt?" % (sl(), a, b), "Ja, denn γ = %d° lässt sich berechnen (WSW)." % (180 - a - b),
                   ["Nein, α liegt nicht an a.", "Ja, nach SSS.", "Nein, man braucht zwei Seiten."],
                   "γ = 180° − %d° − %d° = %d°. Dann sind a und die anliegenden Winkel β und γ bekannt: <b>WSW</b>." % (a, b, 180 - a - b))
    if kind in ("ungl", "ungl_ok"):
        a, b = sl(), sl()
        c = a + b + R.randint(0, 3) if kind == "ungl" else R.randint(abs(a - b) + 1, a + b - 1)
        ok = c < a + b and a < b + c and b < a + c
        ans = "Ja, jede Seite ist kürzer als die Summe der beiden anderen." if ok else "Nein, %d + %d ist nicht größer als %d." % (a, b, c)
        return mcq("Gibt es ein Dreieck mit den Seiten %d cm, %d cm und %d cm?" % (a, b, c), ans,
                   ["Nein, %d + %d ist nicht größer als %d." % (a, b, c) if ok else "Ja, jede Seite ist kürzer als die Summe der beiden anderen.", "Ja, drei Seiten ergeben immer ein Dreieck.", "Nein, die Seiten müssen gleich lang sein."],
                   "Dreiecksungleichung: Die Summe zweier Seiten muss größer sein als die dritte. %d + %d = %d %s %d. <b>%s</b>" % (a, b, a + b, "&gt;" if a + b > c else "≤", c, "Ja" if ok else "Nein"))
    return mcq("Zwei Dreiecke stimmen in zwei Seiten überein. Was muss noch übereinstimmen, damit sie sicher kongruent sind?", "der Winkel zwischen diesen Seiten",
               ["irgendein Winkel", "der Flächeninhalt", "nichts, zwei Seiten reichen"],
               "Nach SWS: <b>der eingeschlossene Winkel</b> (oder die dritte Seite nach SSS).")


def entspricht():
    P = ["ABC", "DEF", "PQR", "KLM", "RST", "XYZ"]
    t1, t2 = R.sample(P, 2)
    kind = R.choice(["seite", "winkel", "laenge"])
    i, j = R.sample(range(3), 2)
    if kind == "seite":
        s1 = t1[i] + t1[j]
        s2 = t2[i] + t2[j]
        return mcq("Es gilt △%s ≅ △%s. Welche Strecke entspricht der Strecke %s?" % (t1, t2, s1), s2,
                   [w for w in [t2[j] + t2[3 - i - j], t2[i] + t2[3 - i - j], t2[3 - i - j] + t2[i]] if set(w) != set(s2)],
                   "Die Ecken entsprechen sich in der Reihenfolge: %s ↔ %s, %s ↔ %s, %s ↔ %s. <b>%s</b>" % (t1[0], t2[0], t1[1], t2[1], t1[2], t2[2], s2))
    if kind == "winkel":
        w = R.randint(25, 110)
        return mcq("Es gilt △%s ≅ △%s. Der Winkel bei %s ist %d°. Welcher Winkel ist auch %d° groß?" % (t1, t2, t1[i], w, w), "der Winkel bei %s" % t2[i],
                   ["der Winkel bei %s" % t2[k] for k in range(3) if k != i] + ["der Winkel bei %s" % t1[(i + 1) % 3]],
                   "%s entspricht %s: <b>der Winkel bei %s</b>." % (t1[i], t2[i], t2[i]))
    L = sl()
    return mcq("Es gilt △%s ≅ △%s und %s = %d cm. Wie lang ist %s?" % (t1, t2, t1[i] + t1[j], L, t2[i] + t2[j]), "%d cm" % L, ["%d cm" % (L * 2), "%d cm" % (L + 1), "Das kann man nicht wissen."],
               "Kongruente Dreiecke haben gleich lange entsprechende Seiten: <b>%d cm</b>." % L)


def begriff():
    q, a, w = R.choice([
        ("Was bedeutet „kongruent“?", "deckungsgleich: gleiche Form und gleiche Größe", ["gleiche Form, aber andere Größe", "gleicher Umfang", "gleicher Flächeninhalt"]),
        ("Welche Abbildung erzeugt keine kongruente Figur?", "eine Vergrößerung", ["eine Verschiebung", "eine Drehung", "eine Spiegelung"]),
        ("Zwei Dreiecke haben den gleichen Flächeninhalt. Sind sie kongruent?", "Nicht unbedingt.", ["Ja, immer.", "Nein, nie.", "Ja, wenn sie spitzwinklig sind."]),
        ("Was gilt für kongruente Figuren?", "Entsprechende Seiten und Winkel sind gleich groß.", ["Nur die Winkel sind gleich groß.", "Nur der Umfang ist gleich.", "Sie liegen immer an derselben Stelle."]),
        ("Wofür steht „WSW“?", "eine Seite und die beiden anliegenden Winkel", ["zwei Winkel und eine beliebige Seite", "Winkel, Seite, Winkel in beliebiger Lage", "drei Winkel"]),
        ("Wofür steht „SWS“?", "zwei Seiten und der eingeschlossene Winkel", ["zwei Seiten und ein beliebiger Winkel", "drei Seiten", "ein Winkel und zwei Höhen"]),
        ("Ein Dreieck wird an einer Geraden gespiegelt. Ist das Bild kongruent?", "Ja, Spiegeln ändert weder Längen noch Winkel.", ["Nein, die Seiten werden vertauscht.", "Nur wenn das Dreieck gleichschenklig ist.", "Nein, die Größe ändert sich."]),
        ("Warum reicht SsW nur mit dem Winkel gegenüber der längeren Seite?", "Sonst kann es zwei verschiedene Dreiecke geben.", ["Sonst ist die Winkelsumme falsch.", "Sonst wird das Dreieck zu groß.", "Es reicht immer."]),
        ("Ein Viereck wird an einer Diagonale in zwei kongruente Dreiecke geteilt. Welche Aussage folgt?", "Die beiden Dreiecke haben den gleichen Flächeninhalt.", ["Das Viereck ist ein Quadrat.", "Alle Winkel sind 90°.", "Die Diagonalen sind gleich lang."]),
        ("Mit welchem Satz zeigt man: Die Diagonale teilt ein Parallelogramm in kongruente Dreiecke?", "WSW oder SSS (gleiche Gegenseiten, gemeinsame Diagonale)", ["WWW", "nur SsW", "Das kann man nicht zeigen."]),
    ])
    return mcq(q, a, w, "<b>%s</b>" % a)


def anwenden():
    kind = R.choice(["drachen", "gleichschenklig", "winkel", "spiegel"])
    if kind == "drachen":
        w = R.randint(30, 80)
        return mcq("Ein Drachenviereck ABCD hat AB = AD und CB = CD. Die Diagonale AC teilt es in zwei Dreiecke. Der Winkel bei B ist %d°. Wie groß ist der Winkel bei D?" % (w + 40), "%d°" % (w + 40),
                   ["%d°" % (180 - w - 40), "%d°" % (90), "%d°" % (360 - 2 * (w + 40))],
                   "△ABC ≅ △ADC nach SSS (AB = AD, CB = CD, AC gemeinsam). Entsprechende Winkel: <b>%d°</b>." % (w + 40))
    if kind == "gleichschenklig":
        g = R.randint(30, 100)
        return mcq("Ein gleichschenkliges Dreieck hat den Winkel %d° an der Spitze. Die Höhe teilt es in zwei kongruente Dreiecke. Wie groß ist jeder Basiswinkel?" % (2 * (g // 2)), "%d°" % ((180 - 2 * (g // 2)) // 2),
                   ["%d°" % (g // 2), "%d°" % (180 - 2 * (g // 2)), "%d°" % (90 - (g // 2) + 10)],
                   "Basiswinkel: (180° − %d°) : 2 = <b>%d°</b>." % (2 * (g // 2), (180 - 2 * (g // 2)) // 2))
    if kind == "winkel":
        a, b = wl(), wl()
        if a + b >= 170:
            return None
        return mcq("△ABC ≅ △DEF mit α = %d° und β = %d°. Wie groß ist der Winkel bei F?" % (a, b), "%d°" % (180 - a - b), ["%d°" % a, "%d°" % b, "%d°" % (a + b)],
                   "Bei F liegt der Winkel, der γ entspricht: 180° − %d° − %d° = <b>%d°</b>." % (a, b, 180 - a - b))
    L = sl()
    return mcq("Ein Dreieck mit dem Umfang %d cm wird verschoben und gedreht. Welchen Umfang hat das Bilddreieck?" % (3 * L + 2), "%d cm" % (3 * L + 2),
               ["%d cm" % (2 * (3 * L + 2)), "%d cm" % (3 * L), "Das hängt von der Drehung ab."],
               "Verschieben und Drehen ändern keine Längen. Das Bild ist kongruent: <b>%d cm</b>." % (3 * L + 2))


def main():
    seen = set()
    sets = [
        ("Kongruenz verstehen", mix(R, seen, [(begriff, 10), (entspricht, 10)])),
        ("Welcher Kongruenzsatz?", mix(R, seen, [(welcher, 20)])),
        ("Reichen die Angaben?", mix(R, seen, [(reicht, 20)])),
        ("Entsprechende Stücke", mix(R, seen, [(entspricht, 20)])),
        ("Anwenden und begründen", mix(R, seen, [(anwenden, 12), (welcher, 8)])),
    ]
    body = lesson(
        ["Zwei Figuren sind <b>kongruent</b> (deckungsgleich), wenn sie in Form und Größe übereinstimmen. Verschieben, Drehen und Spiegeln erzeugen kongruente Figuren.",
         "Dreiecke sind kongruent, wenn sie übereinstimmen in",
         "<b>SSS</b>: drei Seiten – <b>SWS</b>: zwei Seiten und dem eingeschlossenen Winkel – <b>WSW</b>: einer Seite und den beiden anliegenden Winkeln – <b>SsW</b>: zwei Seiten und dem Winkel gegenüber der längeren Seite.",
         "Drei Winkel (WWW) reichen nicht: Die Größe ist dann offen. Bei △ABC ≅ △DEF entsprechen sich A und D, B und E, C und F."],
        [example("a = 5 cm, b = 7 cm, γ = 50°", ["γ liegt zwischen a und b"], "SWS"),
         example("a = 4 cm, b = 6 cm, β = 40°", ["β liegt b gegenüber, b ist die längere Seite"], "SsW")],
        [["Drei Winkel bestimmen das Dreieck", "Die Größe fehlt, es gibt viele ähnliche Dreiecke"],
         ["SsW mit dem Winkel gegenüber der kürzeren Seite", "Nur gegenüber der längeren Seite eindeutig"],
         ["△ABC ≅ △DEF: AB entspricht EF", "Reihenfolge der Ecken: AB entspricht DE"]])
    faq = [
        {"q": "Welche Kongruenzsätze gibt es?", "a": "SSS, SWS, WSW und SsW. Jeder beschreibt drei Angaben, mit denen ein Dreieck eindeutig festgelegt ist."},
        {"q": "Warum reicht WWW nicht?", "a": "Drei Winkel legen nur die Form fest. Es gibt große und kleine Dreiecke mit denselben Winkeln."},
        {"q": "Was ist bei SsW wichtig?", "a": "Der Winkel muss der längeren der beiden Seiten gegenüberliegen. Sonst kann es zwei verschiedene Dreiecke geben."},
        {"q": "Wozu braucht man Kongruenzsätze?", "a": "Um eindeutige Konstruktionen zu erkennen und um geometrische Aussagen zu begründen, z. B. dass zwei Strecken gleich lang sind."},
    ]
    make_unit(R, "kongruenzsaetze", "R",
              "Die Schülerinnen und Schüler erkennen kongruente Figuren, wenden die Kongruenzsätze SSS, SWS, WSW und SsW an, entscheiden über die eindeutige Konstruierbarkeit von Dreiecken und begründen Eigenschaften mit Kongruenz (Zusammenfassung).",
              "Kongruente Dreiecke und Kongruenzsätze",
              "Kongruenzsätze Klasse 8 – SSS, SWS, WSW, SsW, Arbeitsblätter mit Lösungen",
              "Kongruenzsätze",
              "Kongruenzsätze für Klasse 8: SSS, SWS, WSW und SsW erkennen, eindeutige Konstruierbarkeit, entsprechende Seiten und Winkel, Begründungen. 100 Aufgaben mit Lösungen, kostenlos.",
              "SSS, SWS, WSW, SsW",
              "Drei Winkel reichen nicht.",
              body, faq, sets, 10, grade="klasse-8")


if __name__ == "__main__":
    main()
