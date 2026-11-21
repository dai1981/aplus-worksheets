# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 1: Uhrzeit und Tagesablauf（Leitidee Größen und Messen）
  python3 tools/gen_de_mathe_k1_uhrzeit_und_tagesablauf.py
Volle Stunden, halbe Stunden, Tageszeiten und Tagesablauf, Wochentage, eine Stunde früher und später.
Fehler: großen und kleinen Zeiger vertauscht, „halb drei“ als 3:30 Uhr gelesen, morgens und abends verwechselt.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids, clock, table

R = random.Random(49413)
KIDS = Kids(R)
ZAHL = ["zwölf", "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", "zehn", "elf", "zwölf"]


def hm(h, m):
    return "%d:%02d Uhr" % (h, m)


def nx(h):
    return h % 12 + 1


def pv(h):
    return h - 1 if h > 1 else 12


def voll():
    h = R.randint(1, 12)
    if R.random() < 0.7:
        return mcq(clock(h, 0) + "Wie spät ist es?", hm(h, 0), [hm(nx(h), 0), hm(pv(h), 0), hm(12, h * 5 % 60) if h != 12 else hm(6, 0)],
                   "Der große Zeiger zeigt auf die 12, der kleine auf die %d: <b>%s</b>." % (h, hm(h, 0)))
    return mcq("Wohin zeigt der kleine Zeiger um %d Uhr?" % h, "auf die %d" % h, ["auf die 12", "auf die %d" % nx(h), "auf die %d" % pv(h)] if h != 12 else ["auf die 6", "auf die 1", "auf die 11"],
               "Der kleine Zeiger zeigt die Stunde: <b>auf die %d</b>. Der große Zeiger steht auf der 12." % h)


def halb():
    h = R.randint(1, 12)
    kind = R.choice(["bild", "bild", "wort"])
    if kind == "bild":
        return mcq(clock(h, 30) + "Wie spät ist es?", hm(h, 30), [hm(nx(h), 30), hm(h, 0), hm(6, h * 5 % 60) if h != 6 else hm(nx(h), 0)],
                   "Der große Zeiger zeigt auf die 6, der kleine steht zwischen %d und %d: <b>%s</b>, halb %s." % (h, nx(h), hm(h, 30), ZAHL[nx(h)]))
    return mcq("Welche Uhrzeit ist „halb %s“?" % ZAHL[nx(h)], hm(h, 30), [hm(nx(h), 30), hm(nx(h), 0), hm(h, 0)],
               "„Halb %s“ ist eine halbe Stunde vor %s Uhr: <b>%s</b>." % (ZAHL[nx(h)], ZAHL[nx(h)], hm(h, 30)))


ABLAUF = [("Wann frühstückst du meistens?", "am Morgen", ["in der Nacht", "am Abend", "am Nachmittag"]),
          ("Wann schläfst du?", "in der Nacht", ["am Mittag", "am Vormittag", "am Nachmittag"]),
          ("Wann isst du zu Mittag?", "am Mittag", ["in der Nacht", "am frühen Morgen", "am späten Abend"]),
          ("Wann gehst du ins Bett?", "am Abend", ["am Morgen", "am Mittag", "am Vormittag"]),
          ("Wann bist du meistens in der Schule?", "am Vormittag", ["in der Nacht", "am späten Abend", "um Mitternacht"]),
          ("Was machst du zuerst am Morgen?", "aufstehen", ["zur Schule gehen", "frühstücken", "Zähne putzen nach dem Frühstück"]),
          ("Was kommt nach dem Abendessen?", "schlafen gehen", ["aufstehen", "frühstücken", "zur Schule gehen"]),
          ("Was kommt nach dem Morgen?", "der Vormittag", ["die Nacht", "der Abend", "der Nachmittag"]),
          ("Was kommt nach dem Mittag?", "der Nachmittag", ["der Morgen", "der Vormittag", "die Nacht"]),
          ("Was kommt nach dem Abend?", "die Nacht", ["der Morgen", "der Mittag", "der Nachmittag"]),
          ("Um 7 Uhr morgens ist es …", "Zeit zum Aufstehen", ["Zeit zum Schlafen", "Zeit für das Abendessen", "Mitternacht"]),
          ("Um 8 Uhr abends ist es …", "bald Zeit zum Schlafen", ["Zeit für die Schule", "Zeit zum Frühstücken", "Mittag"]),
          ("Wie viele Stunden hat ein Tag?", "24", ["12", "60", "7"]),
          ("Womit misst man die Zeit?", "mit einer Uhr", ["mit einem Lineal", "mit einer Waage", "mit einem Thermometer"]),
          ("Was dauert länger?", "ein Schultag", ["einmal Zähneputzen", "einmal Händewaschen", "einmal Klatschen"]),
          ("Was dauert am kürzesten?", "einmal blinzeln", ["ein Film", "ein Schultag", "eine Nacht"]),
          ("Was dauert ungefähr eine Stunde?", "ein langer Spaziergang", ["einmal niesen", "eine Woche Urlaub", "ein ganzes Jahr"]),
          ("Was dauert ungefähr eine Minute?", "Hände waschen", ["eine Nacht schlafen", "ein Schultag", "Sommerferien"]),
          ("Wann ist es meistens dunkel?", "in der Nacht", ["am Mittag", "am Vormittag", "am Nachmittag"]),
          ("Wann isst man Abendbrot?", "am Abend", ["am Morgen", "am Vormittag", "in der Nacht um drei"]),
          ("Was kommt vor dem Mittag?", "der Vormittag", ["der Nachmittag", "der Abend", "die Nacht"]),
          ("Was kommt vor dem Abend?", "der Nachmittag", ["der Morgen", "die Nacht", "der Vormittag"])]


def ablauf():
    order = list(range(len(ABLAUF)))
    R.shuffle(order)
    st = {"i": 0}

    def mk():
        if st["i"] >= len(order):
            return None
        q, a, w = ABLAUF[order[st["i"]]]
        st["i"] += 1
        return mcq(q, a, w, "<b>%s</b>." % (a[0].upper() + a[1:]))
    return mk


TAGE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]


def woche():
    i = R.randrange(7)
    kind = R.choice(["morgen", "gestern", "nach", "vor", "zahl"])
    if kind == "morgen":
        return mcq("Heute ist %s. Welcher Tag ist morgen?" % TAGE[i], TAGE[(i + 1) % 7], [TAGE[(i - 1) % 7], TAGE[(i + 2) % 7], TAGE[i]],
                   "Morgen ist der nächste Tag: <b>%s</b>." % TAGE[(i + 1) % 7])
    if kind == "gestern":
        return mcq("Heute ist %s. Welcher Tag war gestern?" % TAGE[i], TAGE[(i - 1) % 7], [TAGE[(i + 1) % 7], TAGE[(i - 2) % 7], TAGE[i]],
                   "Gestern war der Tag davor: <b>%s</b>." % TAGE[(i - 1) % 7])
    if kind == "nach":
        return mcq("Welcher Tag kommt nach %s?" % TAGE[i], TAGE[(i + 1) % 7], [TAGE[(i - 1) % 7], TAGE[(i + 2) % 7], TAGE[(i + 3) % 7]],
                   "Nach %s kommt <b>%s</b>." % (TAGE[i], TAGE[(i + 1) % 7]))
    if kind == "vor":
        return mcq("Welcher Tag kommt vor %s?" % TAGE[i], TAGE[(i - 1) % 7], [TAGE[(i + 1) % 7], TAGE[(i - 2) % 7], TAGE[(i + 3) % 7]],
                   "Vor %s kommt <b>%s</b>." % (TAGE[i], TAGE[(i - 1) % 7]))
    q, a, w = R.choice([("Wie viele Tage hat eine Woche?", "7", ["5", "10", "12"]), ("An welchen Tagen ist meistens keine Schule?", "Samstag und Sonntag", ["Montag und Dienstag", "Mittwoch und Donnerstag", "Freitag und Montag"]),
                        ("Welcher Tag ist der erste Tag der Woche?", "Montag", ["Sonntag", "Mittwoch", "Freitag"]), ("Wie viele Monate hat ein Jahr?", "12", ["7", "10", "24"])])
    return mcq(q, a, w, "<b>%s</b>." % a)


def spaeter():
    h = R.randint(1, 11)
    kind = R.choice(["spaeter", "frueher", "dauer", "halb_spaeter"])
    if kind == "spaeter":
        k = R.choice([1, 2, 3])
        return mcq("Es ist %d Uhr. Wie spät ist es %s?" % (h, "in 1 Stunde" if k == 1 else "in %d Stunden" % k), hm((h + k - 1) % 12 + 1, 0),
                   [hm(pv(h) if k == 1 else (h - k - 1) % 12 + 1, 0), hm(h, 30), hm((h + k) % 12 + 1, 0)],
                   "%d Uhr und %d Stunde%s weiter: <b>%s</b>." % (h, k, "" if k == 1 else "n", hm((h + k - 1) % 12 + 1, 0)))
    if kind == "frueher":
        h = R.randint(2, 12)
        return mcq("Es ist %d Uhr. Wie spät war es vor 1 Stunde?" % h, hm(h - 1, 0), [hm(nx(h), 0), hm(h - 1, 30), hm(h, 30)],
                   "Eine Stunde zurück: <b>%s</b>." % hm(h - 1, 0))
    if kind == "dauer":
        k = R.randint(1, 4)
        return mcq("Der Ausflug beginnt um %d Uhr und endet um %d Uhr. Wie lange dauert er?" % (h, h + k) if h + k <= 12 else
                   "Der Ausflug beginnt um 8 Uhr und endet um %d Uhr. Wie lange dauert er?" % (8 + k), "%d Stunde%s" % (k, "" if k == 1 else "n"),
                   ["%d Stunden" % (k + 1), "%d Stunde%s" % (k - 1, "" if k - 1 == 1 else "n") if k > 1 else "eine halbe Stunde", "%d Stunden" % (h + k) if h + k > 1 and h + k <= 12 else "10 Stunden"],
                   "Zähle die Stunden: <b>%d Stunde%s</b>." % (k, "" if k == 1 else "n"))
    return mcq("Es ist %d Uhr. Wie spät ist es eine halbe Stunde später?" % h, hm(h, 30), [hm(nx(h), 30), hm(nx(h), 0), hm(pv(h), 30)],
               "Eine halbe Stunde nach %d Uhr: <b>%s</b>." % (h, hm(h, 30)))


def main():
    seen = set()
    sets = [
        ("Volle Stunden", mix(R, seen, [(voll, 20)])),
        ("Halbe Stunden", mix(R, seen, [(halb, 20)])),
        ("Tageszeiten und Tagesablauf", mix(R, seen, [(ablauf(), 20)])),
        ("Die Wochentage", mix(R, seen, [(woche, 20)])),
        ("Früher und später", mix(R, seen, [(spaeter, 20)])),
    ]
    body = lesson(
        ["Die Uhr hat einen <b>kleinen Zeiger</b> für die Stunden und einen <b>großen Zeiger</b> für die Minuten.",
         "Zeigt der große Zeiger auf die 12, ist es eine volle Stunde: 3 Uhr.",
         "Zeigt der große Zeiger auf die 6, ist es halb: Der kleine Zeiger steht zwischen zwei Zahlen. Bei „halb drei“ ist es 2:30 Uhr.",
         "Der Tag hat Morgen, Vormittag, Mittag, Nachmittag, Abend und Nacht."],
        [example("Großer Zeiger auf 12, kleiner Zeiger auf 7", ["volle Stunde"], "7 Uhr"),
         example("Großer Zeiger auf 6, kleiner zwischen 4 und 5", ["halb fünf"], "4:30 Uhr")],
        [["Kleinen und großen Zeiger vertauschen", "Kleiner Zeiger = Stunde"],
         ["halb drei = 3:30 Uhr", "halb drei = 2:30 Uhr (eine halbe Stunde vor drei)"],
         ["Vor- und Nachmittag verwechseln", "Vormittag ist vor dem Mittag"]],
        extra=table(["Uhrzeit", "So sagt man"], [["3:00 Uhr", "drei Uhr"], ["2:30 Uhr", "halb drei"], ["7:00 Uhr", "sieben Uhr"]]))
    faq = [
        {"q": "Was lernen Kinder in Klasse 1 zur Uhr?", "a": "Volle und halbe Stunden, die Tageszeiten, die Wochentage und einfache Zeitspannen in Stunden. Viertelstunden kommen meist in Klasse 2."},
        {"q": "Warum ist „halb drei“ so schwer?", "a": "Weil man an die kommende Stunde denkt: Es ist halb auf dem Weg zu drei Uhr, also 2:30 Uhr."},
        {"q": "Wie übt man das Uhrlesen?", "a": "Mit einer Lernuhr: Zeiten stellen und lesen. Im Alltag fragen: Um wie viel Uhr gibt es Mittagessen?"},
        {"q": "Wie lernt man die Wochentage?", "a": "Mit einem Wochenplan, auf dem jeden Tag ein Haken gemacht wird, und mit Liedern oder Reimen."},
    ]
    make_unit(R, "uhrzeit-und-tagesablauf", "G",
              "Die Schülerinnen und Schüler lesen volle und halbe Stunden ab, ordnen Tageszeiten und Tätigkeiten im Tagesablauf, kennen die Wochentage und bestimmen einfache Zeitpunkte und Zeitspannen (Zusammenfassung).",
              "Uhrzeit und Tagesablauf",
              "Uhrzeit Klasse 1 – Arbeitsblätter mit Lösungen",
              "Uhrzeit",
              "Uhrzeit für Klasse 1: volle und halbe Stunden, Tageszeiten, Tagesablauf, Wochentage, früher und später. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Kleiner Zeiger: Stunde. Großer Zeiger: Minuten.",
              "Halb drei = 2:30 Uhr",
              body, faq, sets, 13, grade="klasse-1")


if __name__ == "__main__":
    main()
