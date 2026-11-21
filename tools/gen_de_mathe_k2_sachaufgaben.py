# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 2: Sachaufgaben（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k2_sachaufgaben.py
Welche Rechnung passt?, Sachaufgaben mit plus und minus, mit mal und geteilt, zwei Rechenschritte, Frage und Antwort.
Fehler: Signalwörter falsch gedeutet („mehr“ heißt nicht immer plus), nur einen Schritt gerechnet, unnötige Zahlen mitgerechnet.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids, MAL, GETEILT

R = random.Random(49211)
KIDS = Kids(R)


def rechnung():
    p = KIDS.next()
    kind = R.choice(["dazu", "weg", "mal", "teilen", "vergleich"])
    a, b = R.randint(20, 60), R.randint(5, 30)
    if kind == "dazu":
        q = "%s hat %d Murmeln. %s gewinnt %d dazu. Wie viele hat %s jetzt?" % (p[0], a, p[1].capitalize(), b, p[1])
        ans = "%d + %d" % (a, b)
    elif kind == "weg":
        q = "Im Korb sind %d Äpfel. %d Äpfel werden gegessen. Wie viele sind noch im Korb?" % (a, b)
        ans = "%d − %d" % (a, b)
    elif kind == "mal":
        g, k = R.randint(3, 9), R.randint(3, 9)
        q = "%d Kinder haben je %d Bonbons. Wie viele Bonbons sind es zusammen?" % (g, k)
        ans = "%d %s %d" % (g, MAL, k)
        return mcq(q + " Welche Rechnung passt?", ans, ["%d + %d" % (g, k), "%d − %d" % (max(g, k), min(g, k)) if g != k else "%d − 1" % g, "%d + %d + %d" % (g, k, k)],
                   "%d-mal %d: <b>%s</b> = %d." % (g, k, ans, g * k))
    elif kind == "teilen":
        g, k = R.randint(2, 6), R.randint(3, 9)
        n = g * k
        q = "%d Stifte werden an %d Kinder verteilt. Wie viele bekommt jedes Kind?" % (n, g)
        ans = "%d %s %d" % (n, GETEILT, g)
        return mcq(q + " Welche Rechnung passt?", ans, ["%d − %d" % (n, g), "%d %s %d" % (n, MAL, g), "%d + %d" % (n, g)],
                   "Gerecht verteilen heißt teilen: <b>%s</b> = %d." % (ans, k))
    else:
        (n1, _), (n2, _) = KIDS.two()
        q = "%s ist %d cm groß. %s ist %d cm groß. Wie viel größer ist %s?" % (n1, a + 100, n2, a + 100 - b, n1)
        ans = "%d − %d" % (a + 100, a + 100 - b)
        return mcq(q + " Welche Rechnung passt?", ans, ["%d + %d" % (a + 100, a + 100 - b), "%d %s %d" % (a + 100, MAL, 2), "%d − %d" % (a + 100, b + 10)],
                   "„Wie viel größer“ fragt nach dem Unterschied: <b>%s</b> = %d cm." % (ans, b))
    w = ["%d − %d" % (a, b) if kind == "dazu" else "%d + %d" % (a, b), "%d %s %d" % (a, MAL, b), "%d − %d" % (b, a) if kind == "dazu" else "%d + %d" % (b, a + 10)]
    return mcq(q + " Welche Rechnung passt?", ans, w, "<b>%s</b> = %d." % (ans, a + b if kind == "dazu" else a - b))


def plus_minus():
    p = KIDS.next()
    kind = R.choice(["mehr", "weniger", "zusammen", "unterschied", "vorher"])
    a, b = R.randint(25, 70), R.randint(12, 29)
    if kind == "mehr":
        q = "%s hat %d Sticker. %s hat %d Sticker mehr als %s. Wie viele Sticker hat %s?" % (p[0], a, "Ihr Bruder" if p[1] == "sie" else "Seine Schwester", b, p[0], "ihr Bruder" if p[1] == "sie" else "seine Schwester")
        r = a + b
        w = [a - b, r + 10, r - 1]
    elif kind == "weniger":
        q = "Die Klasse 2a sammelt %d Kastanien. Die Klasse 2b sammelt %d Kastanien weniger. Wie viele sammelt die Klasse 2b?" % (a, b)
        r = a - b
        w = [a + b, r + 10, r - 10]
    elif kind == "zusammen":
        q = "Am Montag kommen %d Besucher in den Streichelzoo, am Dienstag %d. Wie viele Besucher sind das zusammen?" % (a, b)
        r = a + b
        w = [a - b, r + 10, r - 1]
    elif kind == "unterschied":
        q = "Im Bus sitzen %d Kinder und %d Erwachsene. Wie viele Kinder mehr als Erwachsene sind es?" % (a, b)
        r = a - b
        w = [a + b, r + 10, r + 1]
    else:
        q = "%s gibt %d € für ein Buch aus. Danach hat %s noch %d €. Wie viel Geld hatte %s vorher?" % (p[0], b, p[1], a, p[1])
        r = a + b
        return mcq(q, "%d €" % r, ["%d €" % x for x in (a - b, r + 10, a)], "Rückwärts rechnen: %d € + %d € = <b>%d €</b>." % (a, b, r))
    if r > 100:
        return None
    return mcq(q, str(r), [str(x) for x in w if 0 < x <= 100 and x != r], ("%d + %d = <b>%d</b>." % (a, b, r) if r == a + b else "%d − %d = <b>%d</b>." % (a, b, r)))


def mal_geteilt():
    p = KIDS.next()
    kind = R.choice(["reihen", "packungen", "verteilen", "gruppen", "preis"])
    g, k = R.randint(2, 9), R.randint(2, 9)
    n = g * k
    if kind == "reihen":
        q, r, e = "Im Theater stehen %d Reihen mit je %d Stühlen. Wie viele Stühle sind es?" % (g, k), n, "%d %s %d = <b>%d</b>." % (g, MAL, k, n)
        w = [g + k, n + k, n - g]
    elif kind == "packungen":
        q, r, e = "%s kauft %d Packungen Saft. In jeder Packung sind %d Flaschen. Wie viele Flaschen sind es?" % (p[0], g, k), n, "%d %s %d = <b>%d</b>." % (g, MAL, k, n)
        w = [g + k, n + g, n - k]
    elif kind == "verteilen":
        q, r, e = "%d Bonbons werden gerecht an %d Kinder verteilt. Wie viele bekommt jedes Kind?" % (n, g), k, "%d %s %d = <b>%d</b>." % (n, GETEILT, g, k)
        w = [n - g, k + 1, g if g != k else k + 2]
    elif kind == "gruppen":
        q, r, e = "%d Kinder fahren in Autos zum Ausflug. In jedes Auto passen %d Kinder. Wie viele Autos brauchen sie?" % (n, k), g, "%d %s %d = <b>%d</b>." % (n, GETEILT, k, g)
        w = [n - k, g + 1, k if g != k else g + 2]
        if k > 4:
            return None
    else:
        q = "Ein Heft kostet %d €. %s kauft %d Hefte. Wie viel muss %s bezahlen?" % (k, p[0], g, p[1])
        return mcq(q, "%d €" % n, ["%d €" % x for x in (g + k, n + k, n - g)], "%d %s %d € = <b>%d €</b>." % (g, MAL, k, n))
    return mcq(q, str(r), [str(x) for x in w if x > 0 and x != r], e)


def zwei():
    p = KIDS.next()
    kind = R.choice(["kauf", "bus", "mal_plus", "geteilt_minus", "sammeln"])
    if kind == "kauf":
        a, b = R.randint(12, 35), R.randint(5, 25)
        g = R.choice([50, 60, 80, 100])
        if a + b >= g:
            return None
        q = "%s hat %d €. %s kauft ein Spiel für %d € und ein Buch für %d €. Wie viel Geld bleibt übrig?" % (p[0], g, p[1].capitalize(), a, b)
        r = g - a - b
        return mcq(q, "%d €" % r, ["%d €" % x for x in (g - a, g - b, a + b, r + 10) if x != r],
                   "Erst: %d + %d = %d €. Dann: %d − %d = <b>%d €</b>." % (a, b, a + b, g, a + b, r))
    if kind == "bus":
        a, b, c = R.randint(20, 40), R.randint(5, 15), R.randint(5, 20)
        q = "Im Bus sitzen %d Menschen. An der Haltestelle steigen %d aus und %d ein. Wie viele sitzen jetzt im Bus?" % (a, b, c)
        r = a - b + c
        return mcq(q, str(r), [str(x) for x in (a - b, a + c, a + b + c, a - b - c) if x != r and x > 0],
                   "%d − %d = %d. %d + %d = <b>%d</b>." % (a, b, a - b, a - b, c, r))
    if kind == "mal_plus":
        g, k, e = R.randint(2, 5), R.choice([6, 8, 10, 12]), R.randint(2, 9)
        q = "%s hat %d volle Schachteln mit je %d Buntstiften und noch %d einzelne Buntstifte. Wie viele Buntstifte sind es?" % (p[0], g, k, e)
        r = g * k + e
        return mcq(q, str(r), [str(x) for x in (g * k, g + k + e, g * (k + e), r + 1) if x != r],
                   "%d %s %d = %d. %d + %d = <b>%d</b>." % (g, MAL, k, g * k, g * k, e, r))
    if kind == "geteilt_minus":
        g, k = R.randint(2, 5), R.randint(4, 9)
        n = g * k
        m = R.randint(1, k - 1)
        q = "%d Erdbeeren werden gerecht an %d Kinder verteilt. Jedes Kind isst %d davon sofort. Wie viele Erdbeeren hat jedes Kind noch?" % (n, g, m)
        r = k - m
        return mcq(q, str(r), [str(x) for x in (k, n - m, r + 1, n - g - m) if x != r and x > 0],
                   "%d %s %d = %d. %d − %d = <b>%d</b>." % (n, GETEILT, g, k, k, m, r))
    a, b = R.randint(10, 30), R.randint(10, 30)
    q = "%s sammelt am Montag %d Kastanien und am Dienstag %d. %s verschenkt 10 Kastanien. Wie viele bleiben?" % (p[0], a, b, p[1].capitalize())
    r = a + b - 10
    return mcq(q, str(r), [str(x) for x in (a + b, a + b - 20, a - 10 + b - 10, r + 1) if x != r],
               "%d + %d = %d. %d − 10 = <b>%d</b>." % (a, b, a + b, a + b, r))


def frage_antwort():
    p = KIDS.next()
    kind = R.choice(["antwort", "frage", "unnoetig"])
    if kind == "antwort":
        g, k = R.randint(3, 8), R.randint(3, 8)
        q = "%s kauft %d Tüten mit je %d Äpfeln. Wie viele Äpfel hat %s? Welcher Antwortsatz passt?" % (p[0], g, k, p[1])
        ans = "%s hat %d Äpfel." % (p[0], g * k)
        return mcq(q, ans, ["%s hat %d Tüten." % (p[0], g), "%s hat %d Äpfel." % (p[0], g + k), "In einer Tüte sind %d Äpfel." % k],
                   "Der Antwortsatz beantwortet genau die Frage: <b>%s</b>" % ans)
    if kind == "frage":
        a, b = R.randint(20, 50), R.randint(10, 40)
        q = "%s hat %d Murmeln. %s Freundin hat %d Murmeln. Welche Frage kann man mit %d + %d beantworten?" % (p[0], a, "Ihre" if p[1] == "sie" else "Seine", b, a, b)
        ans = "Wie viele Murmeln haben beide zusammen?"
        return mcq(q, ans, ["Wie viele Murmeln hat %s mehr?" % p[0], "Wie alt ist %s?" % p[0], "Wie viele Murmeln fehlen noch?"],
                   "Plus rechnet man, wenn man zusammenzählt: <b>%s</b>" % ans)
    a, b, c = R.randint(3, 9), R.randint(10, 40), R.randint(2, 5)
    q = "%s ist %d Jahre alt. %s hat %d Bücher und kauft %d neue. Wie viele Bücher hat %s jetzt?" % (p[0], a, p[1].capitalize(), b, c, p[1])
    return mcq(q, str(b + c), [str(a + b + c), str(b - c), str(a + b)],
               "Das Alter brauchst du nicht. %d + %d = <b>%d</b>." % (b, c, b + c))


def main():
    seen = set()
    sets = [
        ("Welche Rechnung passt?", mix(R, seen, [(rechnung, 20)])),
        ("Mit plus und minus", mix(R, seen, [(plus_minus, 20)])),
        ("Mit mal und geteilt", mix(R, seen, [(mal_geteilt, 20)])),
        ("Zwei Rechenschritte", mix(R, seen, [(zwei, 20)])),
        ("Frage, Rechnung, Antwort", mix(R, seen, [(frage_antwort, 20)])),
    ]
    body = lesson(
        ["Lies die Aufgabe zweimal. Was weißt du? Was wird gefragt?",
         "Überlege dann: Kommt etwas dazu (plus)? Geht etwas weg (minus)? Sind es gleiche Gruppen (mal)? Wird gerecht verteilt (geteilt)?",
         "Manche Aufgaben haben zwei Schritte. Rechne erst den ersten Schritt, dann den zweiten.",
         "Schreibe am Ende einen Antwortsatz."],
        [example("Leni hat 34 €. Sie kauft ein Buch für 12 € und Stifte für 5 €. Wie viel bleibt?", ["12 + 5 = 17", "34 − 17 = 17"], "Leni bleiben 17 €."),
         example("4 Tüten mit je 6 Äpfeln", ["4 %s 6 = 24" % MAL], "Es sind 24 Äpfel.")],
        [["„mehr“ heißt immer plus", "„Wie viel mehr?“ fragt nach dem Unterschied: minus"],
         ["Nur den ersten Schritt rechnen", "Prüfen: Ist die Frage schon beantwortet?"],
         ["Alle Zahlen mitrechnen", "Nur die Zahlen nehmen, die zur Frage gehören"]])
    faq = [
        {"q": "Warum fallen Kindern Sachaufgaben schwer?", "a": "Sie müssen den Text verstehen, die wichtigen Zahlen finden und die passende Rechnung wählen. Hilfreich ist ein fester Ablauf: Frage – Rechnung – Antwort."},
        {"q": "Sind Signalwörter hilfreich?", "a": "Nur bedingt. „Mehr“ kann plus bedeuten („3 mehr bekommen“), aber auch minus („Wie viel mehr hat Tim?“). Besser ist es, sich die Situation vorzustellen."},
        {"q": "Wie hilft eine Skizze?", "a": "Eine kleine Zeichnung oder ein Rechenstrich zeigt, was dazukommt oder weggeht. So findet man die Rechnung leichter."},
        {"q": "Muss man immer einen Antwortsatz schreiben?", "a": "In der Grundschule ja. Der Antwortsatz zeigt, dass das Ergebnis zur Frage passt."},
    ]
    make_unit(R, "sachaufgaben", "Z",
              "Die Schülerinnen und Schüler lösen Sachaufgaben im Zahlenraum bis 100 mit allen vier Rechenarten, auch mit zwei Rechenschritten, wählen die passende Rechnung und formulieren Antworten (Zusammenfassung).",
              "Sachaufgaben bis 100",
              "Sachaufgaben Klasse 2 – Arbeitsblätter mit Lösungen",
              "Sachaufgaben",
              "Sachaufgaben für Klasse 2: Welche Rechnung passt?, plus und minus, mal und geteilt, zwei Rechenschritte, Frage und Antwort. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Frage – Rechnung – Antwort",
              "Stell dir die Situation vor: dazu, weg, Gruppen oder verteilen?",
              body, faq, sets, 11, grade="klasse-2")


if __name__ == "__main__":
    main()
