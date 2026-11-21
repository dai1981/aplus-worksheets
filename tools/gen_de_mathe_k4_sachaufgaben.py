# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 4: Sachaufgaben（Sachrechnen, Leitidee Zahl und Operation / Größen und Messen）
  python3 tools/gen_de_mathe_k4_sachaufgaben.py
Überflüssige Angaben, zweischrittige und dreischrittige Aufgaben, Fahrpläne und Tabellen, Rückwärtsrechnen.
Fehler: alle Zahlen verrechnen, nur einen Schritt rechnen, beim Rückwärtsrechnen die Rechenart nicht umkehren.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, MAL, GETEILT, table, eur

R = random.Random(49108)
KIDS = Kids(R)


def ueberfluessig():
    p = KIDS.next()
    kind = R.choice(["kino", "ausflug", "garten", "buch"])
    if kind == "kino":
        n, c, t = R.randint(3, 8), R.randint(6, 12), R.choice([16, 17, 18])
        q = "%d Kinder gehen um %d Uhr ins Kino. Eine Karte kostet %d €. Wie viel kosten alle Karten?" % (n, t, c)
        ans, w = "die Uhrzeit (%d Uhr)" % t, ["die Anzahl der Kinder (%d)" % n, "den Preis (%d €)" % c, "Ich brauche alle Angaben."]
    elif kind == "ausflug":
        km, n, c = R.randint(40, 180), R.randint(20, 30), R.randint(5, 15)
        q = "Die Klasse 4b fährt %d km mit dem Bus in den Zoo. %d Kinder kommen mit. Der Eintritt kostet %d € pro Kind. Wie viel kostet der Eintritt für alle?" % (km, n, c)
        ans, w = "die Entfernung (%d km)" % km, ["die Anzahl der Kinder (%d)" % n, "den Eintritt (%d €)" % c, "Ich brauche alle Angaben."]
    elif kind == "garten":
        r, b, a = R.randint(4, 12), R.randint(6, 15), R.randint(3, 9)
        q = "Im Garten sind %d Beete. In jedem Beet wachsen %d Salatköpfe. Das Gartenhaus ist %d Jahre alt. Wie viele Salatköpfe sind es?" % (r, b, a)
        ans, w = "das Alter des Gartenhauses (%d Jahre)" % a, ["die Anzahl der Beete (%d)" % r, "die Salatköpfe pro Beet (%d)" % b, "Ich brauche alle Angaben."]
    else:
        s, d, pg = R.randint(120, 380), R.randint(12, 30), R.randint(8, 15)
        q = "%s liest ein Buch mit %d Seiten. Das Buch kostet %d €. %s liest jeden Tag %d Seiten. Nach wie vielen Tagen ist %s fertig (ungefähr)?" % (p[0], s, d, p[1].capitalize(), pg, p[1])
        ans, w = "den Preis (%d €)" % d, ["die Seitenzahl (%d)" % s, "die Seiten pro Tag (%d)" % pg, "Ich brauche alle Angaben."]
    return mcq(q + " Welche Angabe brauchst du nicht?", ans, w, "Für die Frage spielt <b>%s</b> keine Rolle." % ans)


def zwei():
    p = KIDS.next()
    kind = R.choice(["einkauf", "lager", "lauf", "sparen", "saal"])
    if kind == "einkauf":
        n, c, pay = R.randint(3, 8), R.randint(150, 990), R.choice([5000, 10000])
        if n * c >= pay:
            return None
        q = "%s kauft %d Bücher zu je %s und bezahlt mit %s. Wie viel Wechselgeld bekommt %s?" % (p[0], n, eur(c), eur(pay), p[1])
        r = pay - n * c
        w = [n * c, pay - c, r + 100]
        return mcq(q, eur(r), [eur(x) for x in w if x > 0 and x != r], "Erst %d %s %s = %s, dann %s − %s = <b>%s</b>." % (n, MAL, eur(c), eur(n * c), eur(pay), eur(n * c), eur(r)))
    if kind == "lager":
        a, k, per = R.randint(800, 2400), R.randint(5, 12), R.randint(24, 60)
        if k * per >= a:
            return None
        q = "Im Lager sind %s Dosen. Es werden %d Kartons mit je %d Dosen verschickt. Wie viele Dosen sind noch im Lager?" % (num(a), k, per)
        r = a - k * per
        w = [a - per, a - k - per, k * per, r + per]
    elif kind == "lauf":
        rd, m = R.randint(8, 25), R.choice([400, 500, 800])
        q = "Beim Sponsorenlauf läuft %s %d Runden zu je %d m. Wie viele Kilometer und Meter sind das?" % (p[0], rd, m)
        tot = rd * m
        km, mm = divmod(tot, 1000)
        ans = ("%d km %d m" % (km, mm)) if mm else "%d km" % km
        w = ["%d km %d m" % (tot // 100, tot % 100) if tot % 100 else "%d km" % (tot // 100), "%d km %d m" % (km + 1, mm), "%d m" % (rd + m)]
        return mcq(q, ans, [x for x in w if x != ans], "%d %s %d m = %s m = <b>%s</b>." % (rd, MAL, m, num(tot), ans))
    elif kind == "sparen":
        wk, s, toy = R.randint(5, 20), R.randint(3, 9), R.randint(30, 150)
        if wk * s < toy:
            return None
        q = "%s spart %d Wochen lang jede Woche %d €. Dann kauft %s ein Spiel für %d €. Wie viel Geld bleibt übrig?" % (p[0], wk, s, p[1], toy)
        r = wk * s - toy
        w = [wk * s, wk + s - toy if wk + s > toy else toy - s, r + s]
        return mcq(q, "%d €" % r, ["%d €" % x for x in w if x >= 0 and x != r], "%d %s %d € = %d €, %d € − %d € = <b>%d €</b>." % (wk, MAL, s, wk * s, wk * s, toy, r))
    else:
        rows, seats, empty = R.randint(15, 40), R.randint(12, 30), R.randint(10, 90)
        q = "Ein Saal hat %d Reihen mit je %d Plätzen. %d Plätze bleiben leer. Wie viele Zuschauer sind da?" % (rows, seats, empty)
        r = rows * seats - empty
        w = [rows * seats, rows + seats - empty if rows + seats > empty else r + 10, r + empty * 2]
    return mcq(q, num(r), [num(x) for x in w if x > 0 and x != r], "Zwei Schritte: erst malnehmen, dann abziehen. Ergebnis: <b>%s</b>." % num(r))


def drei():
    p = KIDS.next()
    kind = R.choice(["fest", "klassenfahrt", "bauer"])
    if kind == "fest":
        a, pa, b, pb, cost = R.randint(40, 120), R.choice([2, 3]), R.randint(30, 90), R.choice([4, 5]), R.randint(50, 150)
        q = "Beim Schulfest werden %d Waffeln zu je %d € und %d Stück Kuchen zu je %d € verkauft. Die Zutaten haben %d € gekostet. Wie viel Gewinn bleibt?" % (a, pa, b, pb, cost)
        r = a * pa + b * pb - cost
        w = [a * pa + b * pb, a * pa - cost, (a + b) * pa - cost]
        e = "Waffeln: %d €, Kuchen: %d €, zusammen %d €. Minus %d € = <b>%d €</b>." % (a * pa, b * pb, a * pa + b * pb, cost, r)
    elif kind == "klassenfahrt":
        n, bus, house = R.randint(20, 28), R.randint(300, 600), R.randint(1500, 3000)
        tot = bus + house
        if tot % n:
            return None
        q = "Eine Klassenfahrt kostet %s € für den Bus und %s € für die Jugendherberge. %d Kinder teilen sich die Kosten. Wie viel zahlt jedes Kind?" % (num(bus), num(house), n)
        r = tot // n
        w = [house // n if house % n == 0 else r + 10, tot, r + 5]
        e = "%s € + %s € = %s €. %s € %s %d = <b>%d €</b>." % (num(bus), num(house), num(tot), num(tot), GETEILT, n, r)
    else:
        rows, per, sold = R.randint(10, 30), R.randint(20, 40), R.randint(50, 200)
        box = R.choice([6, 10, 12])
        rest = rows * per - sold
        if rest <= 0 or rest % box:
            return None
        q = "Ein Bauer hat %d Reihen mit je %d Kohlköpfen. %d verkauft er auf dem Markt. Den Rest packt er in Kisten zu je %d. Wie viele Kisten braucht er?" % (rows, per, sold, box)
        r = rest // box
        w = [rows * per // box, rest, r + 1]
        e = "%d %s %d = %d, %d − %d = %d, %d %s %d = <b>%d</b>." % (rows, MAL, per, rows * per, rows * per, sold, rest, rest, GETEILT, box, r)
    return mcq(q, num(r) if kind != "fest" and kind != "klassenfahrt" else "%s €" % num(r),
               [num(x) if kind not in ("fest", "klassenfahrt") else "%s €" % num(x) for x in w if x > 0 and x != r], e)


def fahrplan():
    start_h = R.randint(6, 16)
    stations = ["Hamburg", "Hannover", "Kassel", "Fulda", "Frankfurt"] if R.random() < 0.5 else ["München", "Augsburg", "Ulm", "Stuttgart", "Mannheim"]
    times = [start_h * 60 + R.randint(0, 50)]
    for _ in range(4):
        times.append(times[-1] + R.randint(25, 80))
    fmt = lambda t: "%d:%02d" % (t // 60, t % 60)
    tab = table(["Bahnhof"] + stations, [["Zug"] + [fmt(t) for t in times]])
    i, j = sorted(R.sample(range(5), 2))
    d = times[j] - times[i]
    h, m = divmod(d, 60)
    ans = ("%d h %d min" % (h, m) if m else "%d h" % h) if h else "%d min" % m
    def du(x):
        hh, mm = divmod(x, 60)
        return ("%d h %d min" % (hh, mm) if mm else "%d h" % hh) if hh else "%d min" % mm
    w = [du(d + 10), du(d - 10) if d > 15 else du(d + 20), du((times[j] // 60 - times[i] // 60) * 100 + times[j] % 60 - times[i] % 60) if times[j] % 60 >= times[i] % 60 else du(d + 60)]
    return mcq("Fahrplan: %s Wie lange fährt der Zug von %s nach %s?" % (tab, stations[i], stations[j]), ans, [x for x in w if x != ans],
               "Abfahrt %s Uhr, Ankunft %s Uhr: <b>%s</b>." % (fmt(times[i]), fmt(times[j]), ans))


def rueckwaerts():
    kind = R.choice(["denke", "denke", "geld"])
    if kind == "denke":
        x = R.randint(3, 60)
        a, b = R.randint(2, 9), R.randint(5, 90)
        op = R.choice(["mal-plus", "plus-mal", "mal-minus"])
        if op == "mal-plus":
            r = x * a + b
            q = "Ich denke mir eine Zahl. Ich nehme sie mal %d und addiere %d. Ich erhalte %d. Welche Zahl habe ich mir gedacht?" % (a, b, r)
            e = "Rückwärts: %d − %d = %d, %d %s %d = <b>%d</b>." % (r, b, r - b, r - b, GETEILT, a, x)
            w = [(r + b) // a if (r + b) % a == 0 else x + 1, r - b, r // a if r % a == 0 and r // a != x else x + 2]
        elif op == "plus-mal":
            r = (x + b) * a
            q = "Ich denke mir eine Zahl. Ich addiere %d und nehme das Ergebnis mal %d. Ich erhalte %s. Welche Zahl habe ich mir gedacht?" % (b, a, num(r))
            e = "Rückwärts: %s %s %d = %d, %d − %d = <b>%d</b>." % (num(r), GETEILT, a, x + b, x + b, b, x)
            w = [r // a + b, (r - b) // a if (r - b) % a == 0 else x + 1, x + b]
        else:
            if x * a <= b:
                return None
            r = x * a - b
            q = "Ich denke mir eine Zahl. Ich nehme sie mal %d und ziehe %d ab. Ich erhalte %d. Welche Zahl habe ich mir gedacht?" % (a, b, r)
            e = "Rückwärts: %d + %d = %d, %d %s %d = <b>%d</b>." % (r, b, r + b, r + b, GETEILT, a, x)
            w = [(r - b) // a if r > b and (r - b) % a == 0 else x - 1, r + b, x + 1]
        return mcq(q, str(x), [str(v) for v in w if v != x and v > 0], e)
    p = KIDS.next()
    end, spent, got = R.randint(5, 40), R.randint(5, 30), R.randint(5, 20)
    start = end + spent - got
    if start <= 0:
        return None
    q = "%s gibt auf dem Jahrmarkt %d € aus und bekommt danach %d € von Oma. Jetzt hat %s %d €. Wie viel Geld hatte %s vorher?" % (p[0], spent, got, p[1], end, p[1])
    return mcq(q, "%d €" % start, ["%d €" % v for v in (end + spent + got, end - spent + got if end - spent + got > 0 else start + 10, end) if v != start],
               "Rückwärts: %d € − %d € = %d €, %d € + %d € = <b>%d €</b>." % (end, got, end - got, end - got, spent, start))


def main():
    seen = set()
    sets = [
        ("Welche Angabe brauchst du nicht?", mix(R, seen, [(ueberfluessig, 20)])),
        ("Aufgaben mit zwei Schritten", mix(R, seen, [(zwei, 20)])),
        ("Aufgaben mit drei Schritten", mix(R, seen, [(drei, 20)])),
        ("Fahrpläne lesen", mix(R, seen, [(fahrplan, 20)])),
        ("Rückwärts rechnen", mix(R, seen, [(rueckwaerts, 20)])),
    ]
    body = lesson(
        ["Lies die Aufgabe zweimal. Markiere die <b>Frage</b> und die Angaben, die du dafür brauchst.",
         "Nicht jede Zahl im Text wird gebraucht. Streiche überflüssige Angaben durch.",
         "Bei mehreren Schritten hilft ein <b>Lösungsplan</b>: Was rechne ich zuerst, was danach?",
         "Beim <b>Rückwärtsrechnen</b> fängst du beim Ergebnis an und nimmst die Umkehraufgaben: aus plus wird minus, aus mal wird geteilt."],
        [example("Ich denke mir eine Zahl, nehme sie mal 4 und addiere 7. Ich erhalte 43.", ["43 − 7 = 36", "36 %s 4 = 9" % GETEILT], "9"),
         example("5 Bücher zu je 8 €, bezahlt mit 50 €. Wechselgeld?", ["5 %s 8 € = 40 €" % MAL, "50 € − 40 € = 10 €"], "10 €")],
        [["Alle Zahlen aus dem Text verrechnen", "Nur die Angaben nutzen, die zur Frage passen"],
         ["Nach dem ersten Schritt aufhören", "Prüfen, ob die Frage schon beantwortet ist"],
         ["Rückwärts: erst teilen, dann minus", "Den letzten Schritt zuerst umkehren"]])
    faq = [
        {"q": "Wie lösen Kinder Sachaufgaben am besten?", "a": "Mit einem festen Ablauf: Frage finden, wichtige Angaben markieren, Lösungsplan, Rechnung, Antwortsatz und Kontrolle."},
        {"q": "Was sind überflüssige Angaben?", "a": "Zahlen im Text, die man für die Frage nicht braucht. Sie stehen dort, damit Kinder genau lesen."},
        {"q": "Wie liest man einen Fahrplan?", "a": "In einer Zeile stehen die Uhrzeiten eines Zuges. Die Fahrzeit ist die Zeitspanne zwischen Abfahrt und Ankunft."},
        {"q": "Was ist Rückwärtsrechnen?", "a": "Man beginnt beim Ergebnis und macht alle Schritte in umgekehrter Reihenfolge mit der Umkehraufgabe rückgängig."},
    ]
    make_unit(R, "sachaufgaben", "Z",
              "Die Schülerinnen und Schüler lösen mehrschrittige Sachaufgaben, entnehmen Informationen aus Texten, Tabellen und Fahrplänen, erkennen überflüssige Angaben und nutzen Strategien wie Rückwärtsrechnen (Zusammenfassung).",
              "Sachaufgaben: mehrere Schritte, Fahrpläne und Rückwärtsrechnen",
              "Sachaufgaben Klasse 4 – Arbeitsblätter mit Lösungen",
              "Sachaufgaben",
              "Sachaufgaben für Klasse 4: überflüssige Angaben, Aufgaben mit zwei und drei Schritten, Fahrpläne und Rückwärtsrechnen. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Frage finden, Plan machen, rechnen, antworten.",
              "Nicht jede Zahl im Text wird gebraucht.",
              body, faq, sets, 8, grade="klasse-4")


if __name__ == "__main__":
    main()
