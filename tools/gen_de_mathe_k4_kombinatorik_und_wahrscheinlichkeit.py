# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 4: Kombinatorik und Wahrscheinlichkeit（Leitidee Daten und Zufall）
  python3 tools/gen_de_mathe_k4_kombinatorik_und_wahrscheinlichkeit.py
Kombinieren (Kleidung, Eis), Reihenfolgen und Zahlen bilden, Gewinnchancen vergleichen, Chancen „1 von 6“, jeder gegen jeden.
Fehler: addieren statt multiplizieren, Reihenfolgen doppelt oder zu wenig zählen, nur auf die Anzahl der Gewinnkugeln statt auf das Verhältnis achten.
"""
import math
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids, MAL, wrap, table
from ws_common import line, text, INK, GREEN, BLUE, RED

R = random.Random(49119)
KIDS = Kids(R)


def kombinieren():
    kind = R.choice(["kleid", "eis", "menue", "pizza", "kleid3"])
    p = KIDS.next()
    if kind == "kleid":
        a, b = R.randint(2, 6), R.randint(2, 5)
        r = a * b
        return mcq("%s hat %d T-Shirts und %d Hosen. Wie viele verschiedene Kombinationen aus einem T-Shirt und einer Hose kann %s anziehen?" % (p[0], a, b, p[1]),
                   str(r), [str(x) for x in (a + b, r + a, r - 1, 2 * r) if x != r][:3],
                   "Zu jedem T-Shirt passen %d Hosen: %d %s %d = <b>%d</b>." % (b, a, MAL, b, r))
    if kind == "eis":
        a, b = R.randint(3, 8), R.randint(2, 4)
        r = a * b
        return mcq("In der Eisdiele gibt es %d Sorten und %d Becher-Arten. %s wählt eine Sorte und einen Becher. Wie viele Möglichkeiten gibt es?" % (a, b, p[0]),
                   str(r), [str(x) for x in (a + b, r + b, r - b) if x != r],
                   "%d %s %d = <b>%d</b> Möglichkeiten." % (a, MAL, b, r))
    if kind == "menue":
        a, b, c = R.randint(2, 4), R.randint(2, 4), R.randint(2, 3)
        r = a * b * c
        return mcq("In der Mensa gibt es %d Vorspeisen, %d Hauptgerichte und %d Nachspeisen. Wie viele verschiedene Menüs mit je einem Gericht von jeder Art gibt es?" % (a, b, c),
                   str(r), [str(x) for x in (a + b + c, a * b + c, a * b, r + 1) if x != r][:3],
                   "%d %s %d %s %d = <b>%d</b>." % (a, MAL, b, MAL, c, r))
    if kind == "pizza":
        a, b = R.randint(2, 4), R.randint(3, 7)
        r = a * b
        return mcq("Beim Pizzaservice gibt es %d Größen und %d Beläge. Jede Pizza hat genau einen Belag. Wie viele verschiedene Pizzen kann man bestellen?" % (a, b),
                   str(r), [str(x) for x in (a + b, r + a, r - a) if x != r],
                   "%d Größen %s %d Beläge = <b>%d</b>." % (a, MAL, b, r))
    a, b, c = R.randint(2, 4), R.randint(2, 3), R.randint(2, 3)
    r = a * b * c
    return mcq("%s hat %d Mützen, %d Schals und %d Paar Handschuhe. Wie viele verschiedene Kombinationen aus Mütze, Schal und Handschuhen gibt es?" % (p[0], a, b, c),
               str(r), [str(x) for x in (a + b + c, a * b + c, r * 2) if x != r],
               "%d %s %d %s %d = <b>%d</b>." % (a, MAL, b, MAL, c, r))


def reihenfolgen():
    kind = R.choice(["drei", "vier", "ziffern", "ziffern_w", "podest", "flagge"])
    if kind == "drei":
        names = R.sample(["Emma", "Ben", "Mia", "Paul", "Lena", "Finn", "Ida", "Jonas", "Anton", "Clara"], 3)
        return mcq("%s, %s und %s stellen sich in einer Reihe für ein Foto auf. Wie viele verschiedene Reihenfolgen gibt es?" % tuple(names), "6", ["3", "9", "4"],
                   "Für den ersten Platz gibt es 3 Kinder, dann 2, dann 1: 3 %s 2 %s 1 = <b>6</b>." % (MAL, MAL))
    if kind == "vier":
        what = R.choice(["Bücher in ein Regal", "Stofftiere auf ein Brett", "Bilder nebeneinander an die Wand", "Blumentöpfe auf die Fensterbank"])
        return mcq("Du stellst 4 verschiedene %s. Wie viele verschiedene Reihenfolgen gibt es?" % what, "24", ["16", "12", "10"],
                   "4 %s 3 %s 2 %s 1 = <b>24</b>." % (MAL, MAL, MAL))
    if kind == "ziffern":
        ds = sorted(R.sample(range(1, 10), 3))
        return mcq("Bilde mit den Ziffernkarten %d, %d und %d dreistellige Zahlen. Jede Karte wird genau einmal benutzt. Wie viele Zahlen gibt es?" % tuple(ds), "6", ["3", "9", "27"],
                   "Zum Beispiel %d%d%d, %d%d%d, … Für die erste Stelle 3 Karten, dann 2, dann 1: <b>6</b>." % (ds[0], ds[1], ds[2], ds[0], ds[2], ds[1]))
    if kind == "ziffern_w":
        ds = sorted(R.sample(range(1, 10), R.choice([2, 3])))
        n = len(ds)
        r = n * n
        return mcq("Bilde zweistellige Zahlen nur aus den Ziffern %s. Eine Ziffer darf auch doppelt vorkommen (wie %d%d). Wie viele Zahlen gibt es?" % (" und ".join(map(str, ds)) if n == 2 else "%d, %d und %d" % tuple(ds), ds[0], ds[0]),
                   str(r), [str(x) for x in (n * (n - 1), 2 * n, r + 1) if x != r],
                   "Für die Zehnerstelle %d Möglichkeiten, für die Einerstelle auch %d: %d %s %d = <b>%d</b>." % (n, n, n, MAL, n, r))
    if kind == "podest":
        n = R.randint(4, 6)
        r = n * (n - 1) * (n - 2)
        return mcq("Bei einem Wettlauf starten %d Kinder. Wie viele verschiedene Möglichkeiten gibt es für Platz 1, 2 und 3?" % n, str(r),
                   [str(x) for x in (3 * n, n * (n - 1), n * n * n) if x != r],
                   "Platz 1: %d, Platz 2: %d, Platz 3: %d Möglichkeiten. %d %s %d %s %d = <b>%d</b>." % (n, n - 1, n - 2, n, MAL, n - 1, MAL, n - 2, r))
    c = R.randint(3, 5)
    r = c * (c - 1)
    return mcq("Eine Fahne hat zwei Streifen. Es gibt %d Farben. Die beiden Streifen sollen verschiedene Farben haben. Wie viele Fahnen sind möglich?" % c, str(r),
               [str(x) for x in (c * c, 2 * c, r // 2) if x != r],
               "Oben %d Farben, unten noch %d: %d %s %d = <b>%d</b>." % (c, c - 1, c, MAL, c - 1, r))


def kg(n, c):
    return "%d %se Kugel%s" % (n, c, "n" if n != 1 else "")


def C(c):
    return c[0].upper() + c[1:]


COL = {"rot": RED, "blau": BLUE, "grün": GREEN, "gelb": "#e0b000"}


def beutel_svg(counts, label):
    s = []
    balls = [c for c, n in counts for _ in range(n)]
    R2 = random.Random(len(balls) * 31 + sum(n for _, n in counts))
    R2.shuffle(balls)
    per = 6
    for i, c in enumerate(balls):
        x, y = 22 + (i % per) * 24, 22 + (i // per) * 24
        s.append("<circle cx='%d' cy='%d' r='9' fill='%s' stroke='%s' stroke-width='1'/>" % (x, y, COL[c], INK))
    rows = (len(balls) + per - 1) // per
    s.insert(0, "<rect x='6' y='6' width='%d' height='%d' rx='14' fill='#f4f4f4' stroke='%s' stroke-width='1.5'/>" % (per * 24 + 8, rows * 24 + 8, INK))
    return wrap(per * 24 + 22, rows * 24 + 22, "".join(s), label)


def ziehen():
    cs = R.sample(list(COL), R.choice([2, 3]))
    ns = R.sample(range(1, 9), len(cs))
    counts = list(zip(cs, ns))
    kind = R.choice(["meist", "wenig", "unmoeglich"])
    pic = beutel_svg(counts, "Säckchen mit Kugeln")
    if kind == "meist":
        k = ns.index(max(ns))
        return mcq(pic + "Du ziehst ohne hinzusehen eine Kugel. Welche Farbe ziehst du am wahrscheinlichsten?", C(cs[k]),
                   [C(c) for c in cs if c != cs[k]] + [C(c) for c in COL if c not in cs][:3 - (len(cs) - 1)],
                   "Es gibt die meisten %sen Kugeln (%d): <b>%s</b>." % (cs[k], ns[k], C(cs[k])))
    if kind == "wenig":
        if len(cs) < 3:
            return None
        k = ns.index(min(ns))
        return mcq(pic + "Du ziehst ohne hinzusehen eine Kugel. Welche Farbe ist am <b>wenigsten</b> wahrscheinlich?", C(cs[k]),
                   [C(c) for c in cs if c != cs[k]] + ["Alle Farben sind gleich wahrscheinlich."],
                   "Es gibt die wenigsten %sen Kugeln (%d): <b>%s</b>." % (cs[k], ns[k], C(cs[k])))
    miss = [c for c in COL if c not in cs]
    m = R.choice(miss)
    c0 = R.choice(cs)
    tot = sum(ns)
    opts = ["Eine %se Kugel ziehen ist unmöglich." % m, "Eine %se Kugel ziehen ist sicher." % c0, "Eine Kugel ziehen ist unmöglich.",
            "Eine %se Kugel ziehen ist sicher." % m]
    return mcq(pic + "Im Säckchen sind %d Kugeln. Welche Aussage stimmt?" % tot, opts[0], opts[1:],
               "Im Säckchen gibt es keine %se Kugel: Sie zu ziehen ist <b>unmöglich</b>." % m)


def chance():
    kind = R.choice(["wuerfel", "rad", "beutel"])
    if kind == "wuerfel":
        sub = R.choice(["zahl", "gerade", "groesser", "kleiner"])
        if sub == "zahl":
            z = R.randint(1, 6)
            return mcq("Du würfelst mit einem Spielwürfel. Wie groß ist die Chance, eine %d zu würfeln?" % z, "1 von 6", ["%d von 6" % z if z != 1 else "2 von 6", "1 von 2", "6 von 6"],
                       "Der Würfel hat 6 Seiten, eine davon zeigt die %d: <b>1 von 6</b>." % z)
        if sub == "gerade":
            return mcq("Du würfelst. Wie groß ist die Chance auf eine gerade Zahl?", "3 von 6", ["2 von 6", "1 von 6", "4 von 6"],
                       "Gerade sind 2, 4 und 6: <b>3 von 6</b>, also die Hälfte.")
        if sub == "groesser":
            g = R.randint(1, 4)
            r = 6 - g
            return mcq("Du würfelst. Wie groß ist die Chance, eine Zahl größer als %d zu würfeln?" % g, "%d von 6" % r,
                       ["%d von 6" % x for x in (r + 1, g, r - 1 if r > 1 else 6) if x != r][:3],
                       "Größer als %d sind %s: <b>%d von 6</b>." % (g, ", ".join(str(z) for z in range(g + 1, 7)), r))
        g = R.randint(3, 6)
        r = g - 1
        return mcq("Du würfelst. Wie groß ist die Chance, eine Zahl kleiner als %d zu würfeln?" % g, "%d von 6" % r,
                   ["%d von 6" % x for x in (g, r - 1 if r > 1 else 6, 6 - r) if x != r][:3],
                   "Kleiner als %d sind %s: <b>%d von 6</b>." % (g, ", ".join(str(z) for z in range(1, g)), r))
    if kind == "rad":
        n = R.choice([4, 6, 8, 10])
        k = R.randint(1, n - 1)
        col = R.choice(["rot", "blau", "grün", "gelb"])
        other = R.choice([c for c in ["rot", "blau", "grün", "gelb"] if c != col])
        s = []
        cx, cy, rr = 80, 80, 66
        for i in range(n):
            a0, a1 = 2 * math.pi * i / n - math.pi / 2, 2 * math.pi * (i + 1) / n - math.pi / 2
            fill = COL[col] if i < k else COL[other]
            s.append("<path d='M%d,%d L%.1f,%.1f A%d,%d 0 0,1 %.1f,%.1f Z' fill='%s' stroke='white' stroke-width='2'/>" %
                     (cx, cy, cx + rr * math.cos(a0), cy + rr * math.sin(a0), rr, rr, cx + rr * math.cos(a1), cy + rr * math.sin(a1), fill))
        s.append("<polygon points='%d,6 %d,6 %d,22' fill='%s'/>" % (cx - 7, cx + 7, cx, INK))
        pic = wrap(160, 160, "".join(s), "Glücksrad mit %d gleich großen Feldern" % n)
        return mcq(pic + "Das Glücksrad hat %d gleich große Felder. Wie groß ist die Chance, dass es auf %s stehen bleibt?" % (n, C(col)), "%d von %d" % (k, n),
                   ["%d von %d" % (x, y) for x, y in ((n - k, n), (k, n - k) if n - k != k else (k + 1, n), (1, n) if k != 1 else (2, n)) if (x, y) != (k, n)][:3],
                   "%d von %d Feldern %s %s: <b>%d von %d</b>." % (k, n, "ist" if k == 1 else "sind", col, k, n))
    a, b = R.sample(range(1, 8), 2)
    c1, c2 = R.sample(list(COL), 2)
    pic = beutel_svg([(c1, a), (c2, b)], "Säckchen mit Kugeln")
    return mcq(pic + "Im Säckchen sind %s und %s. Wie groß ist die Chance, eine %se Kugel zu ziehen?" % (kg(a, c1), kg(b, c2), c1), "%d von %d" % (a, a + b),
               ["%d von %d" % x for x in ((a, b), (b, a + b), (1, a + b)) if x != (a, a + b)][:3] + (["1 von 2"] if (1, a + b) == (a, a + b) else []),
               "%d Kugeln insgesamt, %d davon %s: <b>%d von %d</b>." % (a + b, a, c1, a, a + b))


def vergleichen():
    while True:
        a1, b1, a2, b2 = R.randint(1, 6), R.randint(1, 8), R.randint(1, 6), R.randint(1, 8)
        if a1 * (a2 + b2) != a2 * (a1 + b1):
            break
    better = "Säckchen A" if a1 * (a2 + b2) > a2 * (a1 + b1) else "Säckchen B"
    trap = (a1 > a2) != (better == "Säckchen A")
    if not trap and R.random() < 0.5:
        return None
    s = "Säckchen A: %s und %s. Säckchen B: %s und %s. " % (kg(a1, "rot"), kg(b1, "blau"), kg(a2, "rot"), kg(b2, "blau"))
    t1, t2 = a1 + b1, a2 + b2
    return mcq(s + "Du gewinnst, wenn du eine rote Kugel ziehst. Aus welchem Säckchen ziehst du besser?", better,
               [v for v in ("Säckchen A", "Säckchen B") if v != better] + ["Bei beiden ist die Chance gleich.", "Das kann man nicht sagen."],
               "A: %d von %d sind rot. B: %d von %d sind rot. %s" % (a1, t1, a2, t2,
               "Bei A ist mehr als die Hälfte rot." if 2 * a1 > t1 and 2 * a2 <= t2 else "Bei B ist mehr als die Hälfte rot." if 2 * a2 > t2 and 2 * a1 <= t1 else
               "Vergleiche gleichnamig: %d von %d und %d von %d." % (a1 * t2, t1 * t2, a2 * t1, t1 * t2)) + " Besser ist <b>%s</b>." % better)


def sache():
    kind = R.choice(["haende", "turnier", "augensumme", "telefon", "wege"])
    if kind == "haende":
        n = R.randint(3, 8)
        r = n * (n - 1) // 2
        return mcq("%d Kinder begrüßen sich. Jedes Kind gibt jedem anderen Kind genau einmal die Hand. Wie oft werden Hände geschüttelt?" % n, str(r),
                   [str(x) for x in (n * (n - 1), n * n, r + 1) if x != r],
                   "Das erste Kind gibt %d Kindern die Hand, das nächste noch %d, … %s = <b>%d</b>." % (n - 1, n - 2, " + ".join(str(k) for k in range(n - 1, 0, -1)), r))
    if kind == "turnier":
        n = R.randint(3, 8)
        r = n * (n - 1) // 2
        return mcq("Bei einem Turnier spielt jede Mannschaft genau einmal gegen jede andere. Es sind %d Mannschaften. Wie viele Spiele gibt es?" % n, str(r),
                   [str(x) for x in (n * (n - 1), n * 2, r - 1) if x != r and x > 0],
                   "Jedes Spiel nur einmal zählen: %s = <b>%d</b>." % (" + ".join(str(k) for k in range(n - 1, 0, -1)), r))
    if kind == "augensumme":
        s = R.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        ways = [(a, b) for a in range(1, 7) for b in range(1, 7) if a + b == s]
        r = len(ways)
        return mcq("Du würfelst mit einem roten und einem blauen Würfel. Auf wie viele Arten kann die Augensumme %d entstehen?" % s, str(r),
                   [str(x) for x in (r + 1, (r + 1) // 2 if r > 1 else 2, 6) if x != r][:3],
                   "Rot und Blau: %s. Das sind <b>%d</b>." % (", ".join("%d+%d" % w for w in ways), r))
    if kind == "telefon":
        n = R.randint(3, 6)
        r = n * (n - 1) // 2
        return mcq("%d Freundinnen schicken sich Fotos. Jede Freundin tauscht mit jeder anderen genau einmal ein Foto (ein Tausch zählt einmal). Wie viele Tauschaktionen gibt es?" % n,
                   str(r), [str(x) for x in (n * (n - 1), n, r + 2) if x != r],
                   "%s = <b>%d</b>." % (" + ".join(str(k) for k in range(n - 1, 0, -1)), r))
    a, b = R.randint(2, 4), R.randint(2, 4)
    r = a * b
    return mcq("Von der Schule zum Park gibt es %d Wege. Vom Park zum Schwimmbad gibt es %d Wege. Wie viele verschiedene Wege führen von der Schule über den Park zum Schwimmbad?" % (a, b),
               str(r), [str(x) for x in (a + b, r + 1, 2 * r) if x != r],
               "Zu jedem der %d Wege passen %d Wege: %d %s %d = <b>%d</b>." % (a, b, a, MAL, b, r))


def main():
    seen = set()
    sets = [
        ("Kombinieren", mix(R, seen, [(kombinieren, 20)])),
        ("Reihenfolgen und Zahlen bilden", mix(R, seen, [(reihenfolgen, 20)])),
        ("Was ist wahrscheinlich?", mix(R, seen, [(ziehen, 14), (vergleichen, 6)])),
        ("Chancen angeben", mix(R, seen, [(chance, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Beim <b>Kombinieren</b> passt zu jeder Möglichkeit der ersten Sache jede Möglichkeit der zweiten Sache. Darum rechnest du <b>mal</b>.",
         "Bei <b>Reihenfolgen</b> wird jeder Platz nacheinander besetzt: 3 Kinder → 3 %s 2 %s 1 = 6 Reihenfolgen." % (MAL, MAL),
         "Die <b>Chance</b> gibst du so an: günstige Möglichkeiten von allen Möglichkeiten, zum Beispiel „1 von 6“ beim Würfel.",
         "Je mehr Gewinnkugeln im Verhältnis zu allen Kugeln, desto größer ist die Chance."],
        [example("3 Hosen und 4 Pullis", ["Zu jeder Hose 4 Pullis", "3 %s 4" % MAL], "12 Kombinationen"),
         example("Säckchen mit 2 roten und 6 blauen Kugeln", ["8 Kugeln, 2 davon rot"], "2 von 8")],
        [["3 Hosen und 4 Pullis: 3 + 4 = 7", "Kombinationen: 3 %s 4 = 12" % MAL],
         ["Jeder gegen jeden: 5 %s 4 = 20 Spiele" % MAL, "Jedes Spiel nur einmal zählen: 10 Spiele"],
         ["Mehr rote Kugeln = immer bessere Chance", "Auch auf die Gesamtzahl der Kugeln achten"]],
        extra=table(["Ereignis", "Beispiel"], [["sicher", "Beim Würfeln kommt eine Zahl von 1 bis 6."], ["möglich", "Beim Würfeln kommt eine 6."], ["unmöglich", "Beim Würfeln kommt eine 7."]]))
    faq = [
        {"q": "Wie findet man alle Kombinationen?", "a": "Mit einem Baumdiagramm oder einer Tabelle. Man geht systematisch vor und schreibt zu jeder ersten Möglichkeit alle zweiten auf. Am Ende rechnet man mal."},
        {"q": "Warum ist die Augensumme 7 bei zwei Würfeln am häufigsten?", "a": "Weil sie auf 6 Arten entstehen kann (1+6, 2+5, 3+4, 4+3, 5+2, 6+1). Die 2 und die 12 gibt es nur auf eine Art."},
        {"q": "Was bedeutet „1 von 6“?", "a": "Von 6 gleich wahrscheinlichen Möglichkeiten ist eine günstig. Auf lange Sicht kommt das Ereignis etwa bei jedem sechsten Versuch vor."},
        {"q": "Wie vergleicht man zwei Säckchen mit Kugeln?", "a": "Man schaut, welcher Anteil der Kugeln gewinnt. 3 von 4 ist besser als 4 von 8, obwohl es weniger Gewinnkugeln sind."},
    ]
    make_unit(R, "kombinatorik-und-wahrscheinlichkeit", "D",
              "Die Schülerinnen und Schüler lösen einfache kombinatorische Aufgaben systematisch, beschreiben und vergleichen Gewinnchancen bei Zufallsexperimenten und geben Wahrscheinlichkeiten als Anteile an (Zusammenfassung).",
              "Kombinatorik und Wahrscheinlichkeit",
              "Kombinatorik und Wahrscheinlichkeit Klasse 4 – Arbeitsblätter mit Lösungen",
              "Kombinatorik und Zufall",
              "Kombinatorik und Wahrscheinlichkeit für Klasse 4: Kombinationen, Reihenfolgen, Zahlen bilden, Gewinnchancen vergleichen und „1 von 6“. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Kombinieren heißt malnehmen.",
              "Chance = günstige von allen Möglichkeiten.",
              body, faq, sets, 19, grade="klasse-4")


if __name__ == "__main__":
    main()
