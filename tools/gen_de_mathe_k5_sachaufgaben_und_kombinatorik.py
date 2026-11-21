# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 5: Sachaufgaben und Kombinatorik（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k5_sachaufgaben_und_kombinatorik.py
Sachaufgaben lösen (Frage – Rechnung – Antwort), Überschlag, Zählprinzip, Baumdiagramm, Anordnungen, Mehrschritt-Sachaufgaben.
Fehler: addiert statt multipliziert (3 Hosen und 4 Shirts = 7), Anordnungen nur als n + n gezählt, einen Rechenschritt vergessen.
"""
import random
from de_common import mcq, num, eur, lesson, example, make_unit, mix, Kids, MAL, table

R = random.Random(49511)
KIDS = Kids(R)
DING = [("Hosen", "T-Shirts", "Outfits"), ("Vorspeisen", "Hauptgerichte", "Menüs"), ("Eissorten", "Waffeln", "Eisbecher"), ("Brotsorten", "Beläge", "Brötchen"),
        ("Farben", "Muster", "Fahnen"), ("Pizzasorten", "Getränke", "Angebote (Pizza und Getränk)"), ("Mützen", "Schals", "Kombinationen")]


def kombi():
    a, b, wort = R.choice(DING)
    x, y = R.randint(2, 6), R.randint(2, 6)
    if x * y == x + y:
        return None
    q = "Es gibt %d %s und %d %s. Wie viele verschiedene %s kann man bilden (je eins von beiden)?" % (x, a, y, b, wort)
    return mcq(q, str(x * y), [str(x + y), str(x * y + x), str(x * y - 1)], "Zu jeder der %d %s passen %d %s: %d %s %d = <b>%d</b>." % (x, a, y, b, x, MAL, y, x * y))


def drei():
    x, y, z = R.randint(2, 4), R.randint(2, 4), R.randint(2, 4)
    kind = R.choice(["menu", "code", "reise"])
    if kind == "menu":
        q = "Ein Menü besteht aus %d Vorspeisen, %d Hauptgerichten und %d Nachspeisen. Wie viele verschiedene Menüs gibt es?" % (x, y, z)
    elif kind == "reise":
        q = "Für eine Reise gibt es %d Ziele, %d Hotels pro Ziel und %d Termine. Wie viele Möglichkeiten gibt es?" % (x, y, z)
    else:
        q = "Ein Schloss hat drei Räder. Am ersten Rad gibt es %d, am zweiten %d und am dritten %d Ziffern. Wie viele Codes sind möglich?" % (x, y, z)
    return mcq(q, str(x * y * z), [str(x + y + z), str(x * y + z), str(x * y * z + x)], "Zählprinzip: %d %s %d %s %d = <b>%d</b>." % (x, MAL, y, MAL, z, x * y * z))


def anordnung():
    kind = R.choice(["n", "ziffern", "podest", "fahne"])
    if kind == "n":
        n = R.randint(3, 5)
        f = 1
        for i in range(2, n + 1):
            f *= i
        what = R.choice(["Kinder in einer Reihe aufstellen", "Bücher nebeneinander ins Regal stellen", "Bilder nebeneinander aufhängen"])
        return mcq("Auf wie viele Arten kann man %d %s?" % (n, what), str(f), [str(n * n), str(n + n), str(f // n if n > 3 else f + 2)],
                   "Für den 1. Platz gibt es %d Möglichkeiten, für den 2. noch %d … %s = <b>%d</b>." % (n, n - 1, (" %s " % MAL).join(str(i) for i in range(n, 0, -1)), f))
    if kind == "ziffern":
        ds = sorted(R.sample(range(1, 10), 3))
        return mcq("Wie viele verschiedene dreistellige Zahlen kann man aus den Ziffern %d, %d und %d bilden, wenn jede Ziffer genau einmal vorkommt?" % tuple(ds), "6", ["3", "9", "27"],
                   "1. Stelle: 3, 2. Stelle: 2, 3. Stelle: 1 Möglichkeit. 3 %s 2 %s 1 = <b>6</b>." % (MAL, MAL))
    if kind == "podest":
        n = R.randint(4, 8)
        return mcq("%d Kinder laufen um die Wette. Wie viele Möglichkeiten gibt es für die Plätze 1, 2 und 3?" % n, str(n * (n - 1) * (n - 2)), [str(3 * n), str(n * n * n), str(n * (n - 1))],
                   "%d %s %d %s %d = <b>%d</b>." % (n, MAL, n - 1, MAL, n - 2, n * (n - 1) * (n - 2)))
    n = R.randint(3, 6)
    return mcq("Eine Fahne hat zwei Streifen in verschiedenen Farben. Es gibt %d Farben. Wie viele Fahnen sind möglich?" % n, str(n * (n - 1)), [str(n * n), str(2 * n), str(n + n - 1)],
               "Oben %d Farben, unten noch %d: %d %s %d = <b>%d</b>." % (n, n - 1, n, MAL, n - 1, n * (n - 1)))


def baum():
    kind = R.choice(["muenze", "spiel", "weg", "rad", "rad"])
    if kind == "rad":
        k = R.randint(3, 8)
        return mcq("Ein Glücksrad hat %d gleich große Felder mit verschiedenen Farben. Es wird zweimal gedreht. Wie viele Enden hat das Baumdiagramm?" % k, str(k * k), [str(2 * k), str(k + k - 1), str(k * (k - 1))],
                   "Beim ersten Drehen %d Äste, an jedem wieder %d: %d %s %d = <b>%d</b>." % (k, k, k, MAL, k, k * k))
    if kind == "muenze":
        k = R.randint(2, 4)
        return mcq("Eine Münze wird %d-mal geworfen (Kopf oder Zahl). Wie viele Enden hat das Baumdiagramm?" % k, str(2 ** k), [str(2 * k), str(k * k), str(2 ** k + 2)],
                   "Bei jedem Wurf verzweigt sich jeder Ast in 2: %s = <b>%d</b>." % ((" %s " % MAL).join(["2"] * k), 2 ** k))
    if kind == "spiel":
        n = R.randint(4, 8)
        return mcq("In einer Gruppe spielen %d Kinder Tischtennis. Jedes Kind spielt einmal gegen jedes andere. Wie viele Spiele gibt es?" % n, str(n * (n - 1) // 2), [str(n * (n - 1)), str(n * n), str(2 * n)],
                   "Jedes Kind hat %d Gegner: %d %s %d = %d. Jedes Spiel ist doppelt gezählt: %d : 2 = <b>%d</b>." % (n - 1, n, MAL, n - 1, n * (n - 1), n * (n - 1), n * (n - 1) // 2))
    n = R.randint(4, 9)
    return mcq("Bei einer Feier stoßen %d Personen an. Jede Person stößt mit jeder anderen genau einmal an. Wie oft klingen die Gläser?" % n, str(n * (n - 1) // 2), [str(n * (n - 1)), str(n * 2), str(n * (n - 1) // 2 + n)],
               "%d %s %d : 2 = <b>%d</b>." % (n, MAL, n - 1, n * (n - 1) // 2))


def schritt():
    p, er = KIDS.next()
    kind = R.choice(["kauf", "kauf2", "sparen", "klasse", "fahrt", "tickets", "fehlt", "rest"])
    if kind == "kauf":
        a, pa = R.randint(2, 6), R.choice([120, 150, 180, 250, 320, 450])
        b, pb = R.randint(2, 5), R.choice([90, 110, 140, 199, 230])
        bez = R.choice([10, 20, 50])
        tot = a * pa + b * pb
        if tot > bez * 100:
            return None
        return mcq("%s kauft %d Hefte zu %s und %d Stifte zu %s. %s bezahlt mit %d €. Wie viel Rückgeld bekommt %s?" % (p, a, eur(pa), b, eur(pb), er.capitalize(), bez, er),
                   eur(bez * 100 - tot), [eur(tot), eur(bez * 100 - a * pa), eur(bez * 100 - pa - pb)],
                   "%d %s %s + %d %s %s = %s. %d € − %s = <b>%s</b>." % (a, MAL, eur(pa), b, MAL, eur(pb), eur(tot), bez, eur(tot), eur(bez * 100 - tot)))
    if kind == "kauf2":
        n, pr = R.randint(3, 9), R.choice([2, 3, 4, 5, 6, 8])
        k = R.randint(2, 4)
        return mcq("Ein Kinoticket kostet %d €. %d Kinder gehen %d-mal ins Kino. Wie viel kostet das zusammen?" % (pr, n, k), "%d €" % (pr * n * k), ["%d €" % x for x in (pr * n + k, pr * (n + k), pr * n * k + pr)],
                   "%d %s %d %s %d = <b>%d €</b>." % (pr, MAL, n, MAL, k, pr * n * k))
    if kind == "sparen":
        z = R.choice([120, 150, 180, 240, 300, 360])
        h = R.choice([30, 40, 50, 60])
        w = R.choice([10, 12, 15, 20])
        if (z - h) % w:
            return None
        return mcq("%s möchte ein Fahrrad für %d € kaufen. %s hat schon %d € und spart jede Woche %d €. Wie viele Wochen muss %s noch sparen?" % (p, z, er.capitalize(), h, w, er), str((z - h) // w),
                   [str(z // w), str((z - h) // w + 1), str((z + h) // w)], "(%d − %d) : %d = %d : %d = <b>%d</b> Wochen." % (z, h, w, z - h, w, (z - h) // w))
    if kind == "klasse":
        k, s = R.randint(3, 5), R.randint(24, 30)
        bus = R.choice([50, 60])
        n = k * s
        b = -(-n // bus)
        return mcq("%d Klassen mit je %d Kindern fahren ins Museum. In einen Bus passen %d Personen. Wie viele Busse braucht man mindestens?" % (k, s, bus), str(b),
                   [str(n // bus) if n % bus else str(b + 1), str(b + 1) if n % bus else str(b - 1), str(k)],
                   "%d %s %d = %d Kinder. %d : %d = %d Rest %d. Es werden <b>%d</b> Busse gebraucht." % (k, MAL, s, n, n, bus, n // bus, n % bus, b) if n % bus else "%d %s %d = %d. %d : %d = <b>%d</b>." % (k, MAL, s, n, n, bus, b))
    if kind == "fahrt":
        km = R.choice([12, 15, 18, 24])
        d = R.choice([5, 20, 22])
        return mcq("Der Schulweg von %s ist %d km lang. %s fährt ihn jeden Schultag hin und zurück. Wie viele Kilometer sind das an %d Schultagen?" % (p, km, er.capitalize(), d), "%d km" % (2 * km * d), ["%d km" % x for x in (km * d, 2 * km + d, 2 * km * d + km)],
                   "Hin und zurück: 2 %s %d = %d km. %d %s %d = <b>%d km</b>." % (MAL, km, 2 * km, 2 * km, MAL, d, 2 * km * d))
    if kind == "tickets":
        e, k = R.choice([8, 9, 12, 14]), R.choice([4, 5, 6, 7])
        ne, nk = R.randint(1, 3), R.randint(2, 5)
        tot = ne * e + nk * k
        return mcq("Im Zoo kostet der Eintritt für Erwachsene %d € und für Kinder %d €. Familie Weber hat %d Erwachsene und %d Kinder. Was zahlt sie?" % (e, k, ne, nk), "%d €" % tot,
                   ["%d €" % x for x in ((ne + nk) * e, (ne + nk) * k, e + k)], "%d %s %d + %d %s %d = %d + %d = <b>%d €</b>." % (ne, MAL, e, nk, MAL, k, ne * e, nk * k, tot))
    if kind == "fehlt":
        s = R.randint(200, 900)
        a, b = R.randint(50, s // 3), R.randint(50, s // 3)
        return mcq("Ein Buch hat %d Seiten. %s hat am Montag %d und am Dienstag %d Seiten gelesen. Wie viele Seiten fehlen noch?" % (s, p, a, b), str(s - a - b), [str(s - a), str(a + b), str(s - a - b + 10)],
                   "%d − %d − %d = <b>%d</b> Seiten." % (s, a, b, s - a - b))
    n, g = R.randint(80, 200), R.choice([6, 8, 12])
    if n % g == 0:
        return None
    return mcq("%d Eier sollen in Schachteln zu je %d Eiern verpackt werden. Wie viele Schachteln werden voll und wie viele Eier bleiben übrig?" % (n, g), "%d Schachteln, %d Eier übrig" % (n // g, n % g),
               ["%d Schachteln, %d Eier übrig" % (n // g + 1, n % g), "%d Schachteln, %d Eier übrig" % (n // g, g - n % g), "%d Schachteln, 0 Eier übrig" % (n // g + 1)],
               "%d : %d = %d Rest %d: <b>%d Schachteln, %d Eier übrig</b>." % (n, g, n // g, n % g, n // g, n % g))


def main():
    seen = set()
    sets = [
        ("Zählprinzip: zwei Stufen", mix(R, seen, [(kombi, 20)])),
        ("Zählprinzip: drei Stufen und Baumdiagramme", mix(R, seen, [(drei, 14), (baum, 6)])),
        ("Anordnungen", mix(R, seen, [(anordnung, 16), (baum, 4)])),
        ("Gemischte Kombinatorik", mix(R, seen, [(kombi, 6), (drei, 5), (anordnung, 5), (baum, 4)])),
        ("Sachaufgaben in mehreren Schritten", mix(R, seen, [(schritt, 20)])),
    ]
    body = lesson(
        ["Bei einer <b>Sachaufgabe</b> gehst du in Schritten vor: Frage verstehen – Rechnung aufschreiben – rechnen – Antwortsatz.",
         "Mache vorher einen <b>Überschlag</b>, dann merkst du grobe Fehler.",
         "<b>Zählprinzip</b>: Wählt man nacheinander aus mehreren Stufen, multipliziert man die Anzahlen: 3 Hosen und 4 T-Shirts ergeben 3 %s 4 = 12 Outfits." % MAL,
         "Beim <b>Anordnen</b> wird es immer eine Möglichkeit weniger: 4 Kinder in einer Reihe: 4 %s 3 %s 2 %s 1 = 24." % (MAL, MAL, MAL),
         "Ein <b>Baumdiagramm</b> zeigt alle Möglichkeiten. Jedes Ende ist eine Möglichkeit."],
        [example("2 Eissorten, 3 Waffeln: wie viele Eisbecher?", ["Zu jeder Sorte passen 3 Waffeln", "2 %s 3" % MAL], "6 Eisbecher"),
         example("5 Kinder, Plätze 1 bis 3", ["1. Platz: 5", "2. Platz: 4", "3. Platz: 3", "5 %s 4 %s 3" % (MAL, MAL)], "60 Möglichkeiten")],
        [["3 Hosen, 4 Shirts: 3 + 4 = 7", "Jede Hose mit jedem Shirt: 3 %s 4 = 12" % MAL],
         ["6 Kinder spielen jeder gegen jeden: 6 %s 5 = 30 Spiele" % MAL, "Jedes Spiel doppelt gezählt: 30 : 2 = 15"],
         ["Busse: 130 Kinder, 50 pro Bus: 2 Busse", "2 Rest 30: Die 30 Kinder brauchen auch einen Bus: 3 Busse"]])
    faq = [
        {"q": "Was ist das Zählprinzip?", "a": "Wenn man nacheinander auswählt, multipliziert man die Anzahl der Möglichkeiten jeder Stufe: 3 · 4 · 2 = 24."},
        {"q": "Wofür braucht man ein Baumdiagramm?", "a": "Es zeigt übersichtlich alle Möglichkeiten. Jeder Weg vom Anfang bis zu einem Ende ist eine Möglichkeit."},
        {"q": "Wie löse ich eine Sachaufgabe?", "a": "Lies genau, schreibe die Frage auf, suche die wichtigen Zahlen, rechne in Schritten und schreibe einen Antwortsatz. Prüfe mit einem Überschlag."},
        {"q": "Warum muss man bei „jeder gegen jeden“ durch 2 teilen?", "a": "Das Spiel A gegen B ist dasselbe wie B gegen A. Ohne das Teilen wäre jedes Spiel doppelt gezählt."},
    ]
    make_unit(R, "sachaufgaben-und-kombinatorik", "Z",
              "Die Schülerinnen und Schüler lösen Sachaufgaben in mehreren Schritten, prüfen Ergebnisse durch Überschlag und bestimmen Anzahlen mit dem Zählprinzip und Baumdiagrammen (Zusammenfassung).",
              "Sachaufgaben und Kombinatorik",
              "Sachaufgaben und Kombinatorik Klasse 5 – Arbeitsblätter mit Lösungen",
              "Sachaufgaben & Kombinatorik",
              "Sachaufgaben und Kombinatorik für Klasse 5: Zählprinzip, Baumdiagramm, Anordnungen und Sachaufgaben in mehreren Schritten. 100 Aufgaben mit Lösungen, kostenlos.",
              "Mehrere Stufen: Anzahlen multiplizieren.",
              "3 Hosen und 4 T-Shirts ergeben 3 · 4 = 12 Outfits.",
              body, faq, sets, 11, grade="klasse-5")


if __name__ == "__main__":
    main()
