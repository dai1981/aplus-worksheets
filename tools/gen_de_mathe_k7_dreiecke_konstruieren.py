# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 7: Dreiecke konstruieren und Kongruenzsätze（Leitidee Raum und Form, Sek I）
  python3 tools/gen_de_mathe_k7_dreiecke_konstruieren.py
Dreiecksungleichung, Kongruenz, Kongruenzsätze SSS, SWS, WSW (WWS) und SsW, eindeutige Konstruierbarkeit, Konstruktionsschritte, Bezeichnungen im Dreieck.
Fehler: WWW für einen Kongruenzsatz gehalten, SWS mit nicht eingeschlossenem Winkel benutzt, Dreiecksungleichung mit ≥ statt >.
"""
import random
from de_common import lesson, example, make_unit, mix, Kids, MAL, table
from de_k7 import mcq

R = random.Random(49712)
KIDS = Kids(R)
SAETZE = ["SSS", "SWS", "WSW", "SsW"]


def ungleichung():
    kind = R.choice(["ja", "nein", "grenz", "dritte"])
    if kind == "ja":
        a, b = R.randint(3, 12), R.randint(3, 12)
        c = R.randint(abs(a - b) + 1, a + b - 1)
        return mcq("Kann man ein Dreieck mit den Seiten %d cm, %d cm und %d cm zeichnen?" % (a, b, c), "Ja, je zwei Seiten sind zusammen länger als die dritte.",
                   ["Nein, die Seiten sind zu verschieden.", "Nein, zwei Seiten sind zusammen zu kurz.", "Nur, wenn ein Winkel 90° ist."],
                   "Längste Seite %d cm &lt; %d cm (Summe der anderen). <b>Ja</b>." % (max(a, b, c), a + b + c - max(a, b, c)))
    if kind == "nein":
        a, b = R.randint(2, 8), R.randint(2, 8)
        c = a + b + R.randint(1, 5)
        return mcq("Kann man ein Dreieck mit den Seiten %d cm, %d cm und %d cm zeichnen?" % (a, b, c), "Nein, zwei Seiten sind zusammen zu kurz.",
                   ["Ja, je zwei Seiten sind zusammen länger als die dritte.", "Ja, aber nur ein rechtwinkliges.", "Ja, wenn man genau zeichnet."],
                   "%d + %d = %d ist nicht größer als %d. <b>Nein</b>." % (a, b, a + b, c))
    if kind == "grenz":
        a, b = R.randint(2, 8), R.randint(2, 8)
        return mcq("Kann man ein Dreieck mit den Seiten %d cm, %d cm und %d cm zeichnen?" % (a, b, a + b), "Nein, die Punkte liegen auf einer Strecke.",
                   ["Ja, je zwei Seiten sind zusammen länger als die dritte.", "Ja, ein sehr flaches Dreieck.", "Ja, ein gleichschenkliges."],
                   "%d + %d = %d ist genau so lang wie die dritte Seite, nicht länger. <b>Nein</b>." % (a, b, a + b))
    a, b = R.randint(3, 12), R.randint(3, 12)
    if a == b:
        return None
    lo, hi = abs(a - b), a + b
    return mcq("Zwei Seiten eines Dreiecks sind %d cm und %d cm lang. Welche Länge kann die dritte Seite haben?" % (a, b), "%d cm" % R.randint(lo + 1, hi - 1),
               ["%d cm" % hi, "%d cm" % lo if lo else "%d cm" % (hi + 2), "%d cm" % (hi + R.randint(1, 4))],
               "Die dritte Seite muss größer als %d cm und kleiner als %d cm sein." % (lo, hi))


def satz():
    k = R.randrange(10)
    D = [("Von einem Dreieck kennt man alle drei Seitenlängen. Welcher Kongruenzsatz passt?", "SSS", ["SWS", "WSW", "WWW"]),
         ("Gegeben sind zwei Seiten und der Winkel, den sie einschließen. Welcher Kongruenzsatz passt?", "SWS", ["SSS", "SsW", "WSW"]),
         ("Gegeben sind eine Seite und die beiden anliegenden Winkel. Welcher Kongruenzsatz passt?", "WSW", ["SWS", "SSS", "SsW"]),
         ("Gegeben sind zwei Seiten und der Winkel, der der längeren Seite gegenüberliegt. Welcher Kongruenzsatz passt?", "SsW", ["SWS", "WSW", "SSS"]),
         ("Gegeben: a = 5 cm, b = 7 cm, γ = 50°. Welcher Kongruenzsatz passt?", "SWS", ["SsW", "WSW", "SSS"]),
         ("Gegeben: c = 6 cm, α = 40°, β = 75°. Welcher Kongruenzsatz passt?", "WSW", ["SWS", "SsW", "WWW"]),
         ("Gegeben: a = 4 cm, b = 6 cm, c = 7 cm. Welcher Kongruenzsatz passt?", "SSS", ["SWS", "WSW", "SsW"]),
         ("Gegeben: a = 5 cm, c = 8 cm, γ = 70°. Welcher Kongruenzsatz passt?", "SsW", ["SWS", "WSW", "SSS"]),
         ("Gegeben: b = 4 cm, c = 6 cm, α = 65°. Welcher Kongruenzsatz passt?", "SWS", ["SsW", "SSS", "WSW"]),
         ("Gegeben: a = 7 cm, β = 50°, γ = 60°. Welcher Kongruenzsatz passt?", "WSW", ["SWS", "SsW", "SSS"])]
    q, a, w = D[k]
    return mcq(q, a, w, {"SSS": "Drei Seiten: <b>SSS</b>.", "SWS": "Zwei Seiten und der eingeschlossene Winkel: <b>SWS</b>.", "WSW": "Eine Seite und zwei Winkel (der dritte ergibt sich aus 180°): <b>WSW</b>.",
                         "SsW": "Zwei Seiten und der Gegenwinkel der größeren Seite: <b>SsW</b>."}[a])


SEITE = {"a": ("B", "C"), "b": ("A", "C"), "c": ("A", "B")}
WINKEL = {"α": "A", "β": "B", "γ": "C"}
GEGEN = {"a": "α", "b": "β", "c": "γ"}


def satz_r():
    kind = R.choice(SAETZE)
    if kind == "SSS":
        vals = sorted(R.sample(range(3, 12), 3))
        if vals[0] + vals[1] <= vals[2]:
            return None
        q = "a = %d cm, b = %d cm, c = %d cm" % tuple(R.sample(vals, 3))
    elif kind == "SWS":
        s1, s2 = R.sample("abc", 2)
        w = [g for g in "αβγ" if WINKEL[g] in SEITE[s1] and WINKEL[g] in SEITE[s2]][0]
        q = "%s = %d cm, %s = %d cm, %s = %d°" % (s1, R.randint(3, 10), s2, R.randint(3, 10), w, R.randint(30, 120))
    elif kind == "WSW":
        s1 = R.choice("abc")
        ws = [g for g in "αβγ" if g != GEGEN[s1]]
        a1, a2 = R.randint(30, 80), R.randint(30, 80)
        q = "%s = %d cm, %s = %d°, %s = %d°" % (s1, R.randint(3, 10), ws[0], a1, ws[1], a2)
    else:
        s1, s2 = R.sample("abc", 2)
        l1, l2 = sorted(R.sample(range(3, 11), 2))
        q = "%s = %d cm, %s = %d cm, %s = %d°" % (s1, l1, s2, l2, GEGEN[s2], R.randint(30, 110))
    return mcq("Gegeben: %s. Nach welchem Kongruenzsatz ist das Dreieck eindeutig?" % q, kind, [x for x in SAETZE if x != kind] + ["WWW"],
               {"SSS": "Drei Seiten: <b>SSS</b>.", "SWS": "Der Winkel liegt zwischen den beiden Seiten: <b>SWS</b>.", "WSW": "Eine Seite und zwei Winkel: <b>WSW</b>.",
                "SsW": "Der Winkel liegt der größeren der beiden Seiten gegenüber: <b>SsW</b>."}[kind])


def pruefen():
    a, b = R.randint(3, 10), R.randint(3, 10)
    w = R.randint(30, 120)
    kind = R.choice(["gleich", "anders", "nicht_eingeschl"])
    if kind == "gleich":
        return mcq("Dreieck 1: a = %d cm, b = %d cm, γ = %d°. Dreieck 2: a = %d cm, b = %d cm, γ = %d°. Sind die Dreiecke kongruent?" % (a, b, w, a, b, w), "Ja, nach SWS.", ["Nein.", "Nur wenn auch c gleich ist.", "Ja, nach SSS."],
                   "Zwei Seiten und der eingeschlossene Winkel stimmen überein: <b>Ja, nach SWS</b>.")
    if kind == "anders":
        w2 = w + R.choice([-10, 10, 15])
        return mcq("Dreieck 1: a = %d cm, b = %d cm, γ = %d°. Dreieck 2: a = %d cm, b = %d cm, γ = %d°. Sind die Dreiecke kongruent?" % (a, b, w, a, b, w2), "Nein, der eingeschlossene Winkel ist verschieden.", ["Ja, nach SWS.", "Ja, nach SSS.", "Ja, weil zwei Seiten gleich sind."],
                   "Der Winkel zwischen a und b ist verschieden, also ist auch c verschieden: <b>Nein</b>.")
    return mcq("Zwei Dreiecke haben je die Seiten %d cm und %d cm und einen Winkel von %d°, der aber nicht zwischen diesen Seiten liegt. Sind sie sicher kongruent?" % (a, b, w), "Nicht sicher – nur wenn der Winkel der größeren Seite gegenüberliegt (SsW).",
               ["Ja, immer nach SWS.", "Ja, nach SSS.", "Nein, nie."], "SWS gilt nur für den eingeschlossenen Winkel. Sonst braucht man SsW: <b>nicht sicher</b>.") if a != b else None


def eindeutig():
    k = R.randrange(10)
    D = [("Gegeben sind α = 50°, β = 60°, γ = 70°. Ist das Dreieck eindeutig konstruierbar?", "Nein, die Größe ist nicht festgelegt (WWW).", ["Ja, mit WSW.", "Ja, mit SSS.", "Nein, die Winkelsumme stimmt nicht."]),
         ("Gegeben sind α = 80°, β = 70°, γ = 40°. Kann es so ein Dreieck geben?", "Nein, die Winkelsumme ist 190°.", ["Ja, eindeutig.", "Ja, aber nicht eindeutig.", "Ja, mit WSW."]),
         ("Gegeben: a = 6 cm, b = 4 cm, α = 30° (α liegt der längeren Seite gegenüber). Ist das Dreieck eindeutig?", "Ja, nach SsW.", ["Nein, es gibt zwei Dreiecke.", "Nein, SWS passt nicht.", "Ja, nach SWS."]),
         ("Gegeben: a = 4 cm, b = 6 cm, α = 30° (α liegt der kürzeren Seite gegenüber). Ist das Dreieck eindeutig?", "Nein, es kann zwei verschiedene Dreiecke geben.", ["Ja, nach SsW.", "Ja, nach SWS.", "Ja, nach SSS."]),
         ("Gegeben: c = 5 cm, α = 100°, β = 90°. Kann man das Dreieck konstruieren?", "Nein, die beiden Winkel sind zusammen schon über 180°.", ["Ja, nach WSW.", "Ja, ein stumpfwinkliges.", "Nur ungenau."]),
         ("Gegeben: a = 5 cm, b = 5 cm, γ = 60°. Was für ein Dreieck entsteht?", "ein gleichseitiges Dreieck", ["ein rechtwinkliges Dreieck", "ein stumpfwinkliges Dreieck", "gar keins"]),
         ("Zwei Dreiecke stimmen in allen drei Winkeln überein. Sind sie kongruent?", "Nicht unbedingt, sie können verschieden groß sein.", ["Ja, immer.", "Ja, nach WSW.", "Nein, nie."]),
         ("Zwei Dreiecke stimmen in allen drei Seiten überein. Sind sie kongruent?", "Ja, nach SSS.", ["Nicht unbedingt.", "Nur bei rechtwinkligen Dreiecken.", "Nein."]),
         ("Was bedeutet „kongruent“?", "deckungsgleich: gleiche Form und gleiche Größe", ["nur gleiche Form", "nur gleicher Flächeninhalt", "nur gleicher Umfang"]),
         ("Gegeben: a = 3 cm, b = 4 cm, c = 8 cm. Ist das Dreieck konstruierbar?", "Nein, 3 cm + 4 cm ist kürzer als 8 cm.", ["Ja, nach SSS.", "Ja, ein stumpfwinkliges.", "Ja, ein rechtwinkliges."])]
    q, a, w = D[k]
    return mcq(q, a, w, "<b>%s</b>" % a)


def schritte():
    k = R.randrange(8)
    D = [("SSS mit a, b, c: Was zeichnet man zuerst?", "eine Seite, z. B. c = AB", ["einen Winkel", "den Umkreis", "die Höhe"]),
         ("SSS: Wie findet man den Punkt C, wenn AB gezeichnet ist?", "Kreis um A mit Radius b und Kreis um B mit Radius a schneiden", ["Winkel an A antragen", "Mittelsenkrechte von AB zeichnen", "Parallele zu AB zeichnen"]),
         ("SWS mit b, c und α: Was zeichnet man nach der Seite c = AB?", "den Winkel α in A antragen", ["den Winkel β in B antragen", "einen Kreis um B mit Radius b", "die Höhe auf c"]),
         ("WSW mit c, α und β: Wie entsteht der Punkt C?", "als Schnittpunkt der beiden freien Schenkel von α und β", ["als Mittelpunkt von AB", "mit einem Kreis um A", "durch Messen der Höhe"]),
         ("Welches Werkzeug braucht man bei SSS unbedingt?", "einen Zirkel", ["einen Winkelmesser", "einen Taschenrechner", "eine Schere"]),
         ("Wie heißt die Seite, die dem Punkt A gegenüberliegt?", "a", ["b", "c", "α"]),
         ("Welcher Winkel liegt an der Ecke B?", "β", ["α", "γ", "δ"]),
         ("Wie viele Lösungen hat eine Konstruktion nach SSS (bis auf Lage)?", "genau eine", ["keine", "zwei", "unendlich viele"])]
    q, a, w = D[k]
    return mcq(q, a, w, "<b>%s</b>." % a)


def sache():
    k = R.randrange(6)
    if k == 0:
        a, b = R.randint(3, 6), R.randint(3, 6)
        c = R.randint(abs(a - b) + 1, a + b - 1)
        return mcq("Aus drei Holzleisten von %d dm, %d dm und %d dm soll ein Dreieck gelegt werden. Wie viele verschiedene (nicht kongruente) Dreiecke gibt es?" % (a, b, c), "genau eins", ["keins", "zwei", "unendlich viele"],
                   "Drei Seiten legen das Dreieck fest (SSS): <b>genau eins</b>.") if a + b > c else None
    if k == 1:
        a = R.randint(3, 8)
        return mcq("Eine Leiter (%d m) lehnt an einer Wand. Unten steht sie 1 m von der Wand weg. Ist das Dreieck aus Leiter, Wand und Boden festgelegt?" % a, "Ja, nach SsW (rechter Winkel an der Wand).", ["Nein, es fehlt eine Seite.", "Ja, nach WWW.", "Nein, es gibt zwei Möglichkeiten."], "Zwei Seiten und der rechte Winkel gegenüber der längsten Seite: <b>SsW</b>.") if a == 3 else None
    if k == 2:
        return mcq("Ein Vermesser kennt eine Strecke von 50 m und die beiden Winkel an ihren Enden zu einem Baum. Welcher Satz zeigt, dass die Lage des Baums festliegt?", "WSW", ["SSS", "SWS", "WWW"], "Eine Seite und die beiden anliegenden Winkel: <b>WSW</b>.")
    if k == 3:
        return mcq("Wie viele Stäbe braucht man mindestens, damit ein Dreieck aus Stäben stabil ist?", "3", ["2", "4", "6"], "Drei Seiten legen das Dreieck fest (SSS). Deshalb ist ein Dreieck stabil, ein Viereck nicht: <b>3</b>.")
    if k == 4:
        a = R.randint(4, 9)
        return mcq("Zwei Seiten eines Dreiecks sind %d cm lang und schließen einen Winkel von 60° ein. Wie lang ist die dritte Seite?" % a, "%d cm" % a, ["%d cm" % (2 * a), "%d cm" % (a // 2) if a // 2 else "1 cm", "Das kann man nicht sagen."],
                   "Gleichschenklig mit 60° an der Spitze: Basiswinkel (180° − 60°) : 2 = 60°. Also gleichseitig: <b>%d cm</b>." % a)
    a, b = R.randint(3, 9), R.randint(3, 9)
    return mcq("Ein Zaun soll ein dreieckiges Beet einschließen. Zwei Seiten sind %d m und %d m lang. Wie lang darf die dritte Seite höchstens sein (ganze Meter)?" % (a, b), "%d m" % (a + b - 1), ["%d m" % (a + b), "%d m" % (abs(a - b) + 1), "%d m" % (a + b + 1)],
               "Sie muss kürzer als %d + %d = %d m sein: <b>%d m</b>." % (a, b, a + b, a + b - 1))


def main():
    seen = set()
    sets = [
        ("Dreiecksungleichung", mix(R, seen, [(ungleichung, 20)])),
        ("Kongruenzsätze erkennen", mix(R, seen, [(satz, 8), (satz_r, 12)])),
        ("Eindeutig konstruierbar?", mix(R, seen, [(eindeutig, 10), (pruefen, 10)])),
        ("Konstruktionsschritte", mix(R, seen, [(schritte, 8), (satz_r, 12)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 5), (pruefen, 8), (ungleichung, 7)])),
    ]
    body = lesson(
        ["Ein Dreieck gibt es nur, wenn je zwei Seiten zusammen <b>länger</b> sind als die dritte (Dreiecksungleichung).",
         "Zwei Dreiecke sind <b>kongruent</b> (deckungsgleich), wenn sie in Form und Größe übereinstimmen.",
         "Kongruenzsätze: <b>SSS</b> (drei Seiten), <b>SWS</b> (zwei Seiten und der eingeschlossene Winkel), <b>WSW</b> (eine Seite und zwei Winkel), <b>SsW</b> (zwei Seiten und der Gegenwinkel der größeren Seite).",
         "Mit drei Winkeln (WWW) ist nur die Form, nicht die Größe festgelegt."],
        [example("a = 5 cm, b = 4 cm, c = 6 cm", ["c zeichnen", "Kreis um A mit 4 cm, Kreis um B mit 5 cm", "Schnittpunkt C"], "SSS, eindeutig"),
         example("3 cm, 4 cm, 8 cm", ["3 + 4 = 7 &lt; 8"], "kein Dreieck")],
        [["WWW ist ein Kongruenzsatz", "Drei Winkel legen die Größe nicht fest"],
         ["SWS mit einem Winkel, der nicht zwischen den Seiten liegt", "Der Winkel muss eingeschlossen sein"],
         ["3 cm, 4 cm, 7 cm ist ein Dreieck", "3 + 4 = 7 ist nicht größer als 7: kein Dreieck"]],
        extra=table(["Satz", "gegeben"], [["SSS", "drei Seiten"], ["SWS", "zwei Seiten und der eingeschlossene Winkel"], ["WSW", "eine Seite und zwei Winkel"], ["SsW", "zwei Seiten und der Gegenwinkel der größeren Seite"]]))
    faq = [
        {"q": "Was sind Kongruenzsätze?", "a": "Regeln, welche Angaben ein Dreieck eindeutig festlegen: SSS, SWS, WSW und SsW."},
        {"q": "Warum ist WWW kein Kongruenzsatz?", "a": "Drei Winkel legen nur die Form fest. Das Dreieck kann beliebig groß oder klein sein."},
        {"q": "Was sagt die Dreiecksungleichung?", "a": "Je zwei Seiten eines Dreiecks sind zusammen länger als die dritte Seite."},
        {"q": "Wie konstruiert man ein Dreieck aus drei Seiten?", "a": "Eine Seite zeichnen, um ihre Endpunkte Kreise mit den anderen Seitenlängen ziehen. Der Schnittpunkt ist die dritte Ecke."},
    ]
    make_unit(R, "dreiecke-konstruieren", "R",
              "Die Schülerinnen und Schüler prüfen die Dreiecksungleichung, nennen und nutzen die Kongruenzsätze SSS, SWS, WSW und SsW und entscheiden, ob ein Dreieck eindeutig konstruierbar ist (Zusammenfassung).",
              "Dreiecke konstruieren und Kongruenzsätze",
              "Dreiecke konstruieren und Kongruenzsätze Klasse 7 – Arbeitsblätter",
              "Kongruenzsätze",
              "Dreiecke konstruieren für Klasse 7: Dreiecksungleichung, Kongruenzsätze SSS, SWS, WSW, SsW und Konstruktionsschritte. 100 Aufgaben mit Lösungen, kostenlos.",
              "SSS, SWS, WSW, SsW legen ein Dreieck fest.",
              "Je zwei Seiten zusammen länger als die dritte.",
              body, faq, sets, 12, grade="klasse-7")


if __name__ == "__main__":
    main()
