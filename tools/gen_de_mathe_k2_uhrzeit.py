# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 2: Uhrzeit und Zeitspannen（Leitidee Größen und Messen）
  python3 tools/gen_de_mathe_k2_uhrzeit.py
Volle und halbe Stunden, Viertelstunden, Minuten in 5er-Schritten, Zeitspannen, Kalender und Sachaufgaben.
Fehler: „halb vier“ als 4:30, Stunden- und Minutenzeiger vertauscht, Viertel vor und Viertel nach verwechselt, 1 h = 100 min.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids, clock, table

R = random.Random(49214)
KIDS = Kids(R)
ZAHL = ["zwölf", "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", "zehn", "elf", "zwölf"]


def hm(h, m):
    return "%d:%02d Uhr" % (h, m)


def nx(h):
    return h % 12 + 1


def pv(h):
    return h - 1 if h > 1 else 12


def voll_halb():
    h = R.randint(1, 12)
    m = R.choice([0, 30])
    kind = R.choice(["bild", "bild", "wort"])
    if kind == "bild":
        w = [hm(nx(h), 30) if m == 30 else hm(h, 30), hm(6, h * 5 % 60) if m == 30 and h != 6 else hm(12, h * 5 % 60) if h != 12 else hm(h, 15), hm(pv(h), m), hm(nx(h), m)]
        return mcq(clock(h, m) + "Wie spät ist es?", hm(h, m), [x for x in w if x != hm(h, m)],
                   ("Der lange Zeiger steht auf der 12, der kurze auf der %d: <b>%s</b>." % (h, hm(h, m))) if m == 0 else
                   "Der lange Zeiger steht auf der 6, der kurze zwischen %d und %d: <b>%s</b> (halb %s)." % (h, nx(h), hm(h, m), ZAHL[nx(h)]))
    if m == 0:
        return mcq("Welche Uhrzeit ist „%s Uhr“?" % ZAHL[h], hm(h, 0), [hm(h, 30), hm(pv(h), 30), hm(nx(h), 0)],
                   "„%s Uhr“ ist eine volle Stunde: <b>%s</b>." % (ZAHL[h].capitalize(), hm(h, 0)))
    return mcq("Welche Uhrzeit ist „halb %s“?" % ZAHL[nx(h)], hm(h, 30), [hm(nx(h), 30), hm(nx(h), 0), hm(h, 0)],
               "„Halb %s“ heißt eine halbe Stunde <b>vor</b> %s Uhr: <b>%s</b>." % (ZAHL[nx(h)], ZAHL[nx(h)], hm(h, 30)))


def viertel():
    h = R.randint(1, 12)
    m = R.choice([15, 45])
    kind = R.choice(["bild", "wort", "wort_rueck"])
    if kind == "bild":
        w = [hm(h, 45 if m == 15 else 15), hm(nx(h), m), hm(3 if m == 15 else 9, h * 5 % 60) if h not in (3, 9) else hm(pv(h), m)]
        return mcq(clock(h, m) + "Wie spät ist es?", hm(h, m), w,
                   "Der lange Zeiger steht auf der %d: <b>%s</b> (%s)." % (3 if m == 15 else 9, hm(h, m), "Viertel nach %s" % ZAHL[h] if m == 15 else "Viertel vor %s" % ZAHL[nx(h)]))
    if kind == "wort":
        if m == 15:
            return mcq("Welche Uhrzeit ist „Viertel nach %s“?" % ZAHL[h], hm(h, 15), [hm(h, 45), hm(pv(h), 45), hm(nx(h), 15)],
                       "15 Minuten nach %d Uhr: <b>%s</b>." % (h, hm(h, 15)))
        return mcq("Welche Uhrzeit ist „Viertel vor %s“?" % ZAHL[nx(h)], hm(h, 45), [hm(nx(h), 15), hm(nx(h), 45), hm(h, 15)],
                   "15 Minuten vor %d Uhr: <b>%s</b>." % (nx(h), hm(h, 45)))
    ans = "Viertel nach %s" % ZAHL[h] if m == 15 else "Viertel vor %s" % ZAHL[nx(h)]
    w = ["Viertel vor %s" % ZAHL[h], "Viertel nach %s" % ZAHL[nx(h)], "halb %s" % ZAHL[nx(h)]] if m == 15 else \
        ["Viertel nach %s" % ZAHL[nx(h)], "Viertel vor %s" % ZAHL[h], "halb %s" % ZAHL[nx(h)]]
    return mcq("Wie sagt man zu %s?" % hm(h, m), ans, w, "Man sagt: <b>%s</b>." % ans)


def minuten():
    h = R.randint(1, 12)
    m = R.choice([5, 10, 20, 25, 35, 40, 50, 55])
    w = [hm(h, (m + 5) % 60), hm(m // 5, h * 5 % 60) if m // 5 != h else hm(h, m - 5), hm(nx(h), m), hm(h, m // 5)]
    return mcq(clock(h, m) + "Wie spät ist es?", hm(h, m), [x for x in w if x != hm(h, m)],
               "Der lange Zeiger steht auf der %d. Das sind %d %s 5 = %d Minuten. Es ist <b>%s</b>." % (m // 5, m // 5, "·", m, hm(h, m)))


def dauer(mins):
    h, m = divmod(mins, 60)
    if h and m:
        return "%d h %d min" % (h, m)
    return "%d h" % h if h else "%d min" % m


def spanne():
    kind = R.choice(["von_bis", "spaeter", "einheit"])
    if kind == "von_bis":
        h = R.randint(7, 17)
        m1 = R.choice([0, 15, 30])
        d = R.choice([15, 30, 45, 60, 90, 20, 40])
        t2 = h * 60 + m1 + d
        return mcq("Von %s bis %s. Wie lange dauert das?" % (hm(h, m1), hm(t2 // 60, t2 % 60)), dauer(d),
                   [dauer(x) for x in (d + 15, abs(d - 15) or 5, d + 60)], "Zähle von %s bis %s: <b>%s</b>." % (hm(h, m1), hm(t2 // 60, t2 % 60), dauer(d)))
    if kind == "spaeter":
        h = R.randint(7, 16)
        m1 = R.choice([0, 15, 30, 45])
        d = R.choice([15, 30, 45, 60])
        t2 = h * 60 + m1 + d
        return mcq("Es ist %s. Wie spät ist es in %s?" % (hm(h, m1), dauer(d)), hm(t2 // 60, t2 % 60),
                   [hm((t2 - 15) // 60, (t2 - 15) % 60), hm((t2 + 15) // 60, (t2 + 15) % 60), hm(h, (m1 + d) % 100) if (m1 + d) < 60 else hm(h + 2, m1)],
                   "%s + %s = <b>%s</b>." % (hm(h, m1), dauer(d), hm(t2 // 60, t2 % 60)))
    q, a, w = R.choice([("Wie viele Minuten hat eine Stunde?", "60 min", ["100 min", "30 min", "24 min"]),
                        ("Wie viele Minuten sind eine halbe Stunde?", "30 min", ["50 min", "15 min", "60 min"]),
                        ("Wie viele Minuten sind eine Viertelstunde?", "15 min", ["25 min", "30 min", "45 min"]),
                        ("Wie viele Stunden hat ein Tag?", "24 h", ["12 h", "60 h", "100 h"]),
                        ("Wie viele Minuten sind eine Dreiviertelstunde?", "45 min", ["75 min", "30 min", "34 min"]),
                        ("Wie viele Minuten sind 2 Stunden?", "120 min", ["200 min", "60 min", "100 min"])])
    return mcq(q, a, w, "1 h = 60 min. <b>%s</b>." % a)


TAGE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]


def kalender():
    kind = R.choice(["morgen", "gestern", "monat", "monat_vor", "zahl", "sache", "sache"])
    if kind == "morgen":
        i = R.randrange(7)
        k = R.choice([1, 2, 3])
        word = {1: "morgen", 2: "übermorgen", 3: "in drei Tagen"}[k]
        return mcq("Heute ist %s. Welcher Tag ist %s?" % (TAGE[i], word), TAGE[(i + k) % 7], [TAGE[(i - k) % 7], TAGE[(i + k + 1) % 7], TAGE[(i + k - 1) % 7]],
                   "Zähle %d Tag%s weiter: <b>%s</b>." % (k, "" if k == 1 else "e", TAGE[(i + k) % 7]))
    if kind == "gestern":
        i = R.randrange(7)
        return mcq("Heute ist %s. Welcher Tag war gestern?" % TAGE[i], TAGE[(i - 1) % 7], [TAGE[(i + 1) % 7], TAGE[(i - 2) % 7], TAGE[(i + 2) % 7]],
                   "Einen Tag zurück: <b>%s</b>." % TAGE[(i - 1) % 7])
    if kind == "monat":
        i = R.randrange(12)
        return mcq("Welcher Monat kommt nach dem %s?" % MONATE[i], MONATE[(i + 1) % 12], [MONATE[(i - 1) % 12], MONATE[(i + 2) % 12], MONATE[(i + 6) % 12]],
                   "Nach dem %s kommt der <b>%s</b>." % (MONATE[i], MONATE[(i + 1) % 12]))
    if kind == "monat_vor":
        i = R.randrange(12)
        return mcq("Welcher Monat kommt vor dem %s?" % MONATE[i], MONATE[(i - 1) % 12], [MONATE[(i + 1) % 12], MONATE[(i - 2) % 12], MONATE[(i + 6) % 12]],
                   "Vor dem %s kommt der <b>%s</b>." % (MONATE[i], MONATE[(i - 1) % 12]))
    if kind == "zahl":
        q, a, w = R.choice([("Wie viele Tage hat eine Woche?", "7", ["5", "10", "12"]), ("Wie viele Monate hat ein Jahr?", "12", ["10", "7", "24"]),
                            ("Wie viele Tage hat der Januar?", "31", ["30", "28", "12"]), ("Wie viele Wochen sind 14 Tage?", "2", ["14", "7", "4"]),
                            ("Wie viele Tage sind 3 Wochen?", "21", ["10", "3", "30"])])
        return mcq(q, a, w, "<b>%s</b>." % a)
    p = KIDS.next()
    kind = R.choice(["schule", "film", "zug", "training"])
    if kind == "schule":
        h, m = 7, R.choice([30, 35, 40, 45])
        d = R.choice([10, 15, 20])
        t = h * 60 + m + d
        return mcq("%s geht um %s los. Der Schulweg dauert %d Minuten. Wann ist %s in der Schule?" % (p[0], hm(h, m), d, p[1]), hm(t // 60, t % 60),
                   [hm(h, m + d - 10), hm(t // 60, (t + 10) % 60) if t % 60 + 10 < 60 else hm(t // 60 + 1, t % 60 + 10 - 60), hm(h, m - d)],
                   "%s + %d min = <b>%s</b>." % (hm(h, m), d, hm(t // 60, t % 60)))
    if kind == "film":
        h = R.choice([15, 16, 17])
        d = R.choice([60, 75, 90, 105])
        t = h * 60 + d
        return mcq("Ein Kinderfilm beginnt um %s und dauert %s. Wann ist er zu Ende?" % (hm(h, 0), dauer(d)), hm(t // 60, t % 60),
                   [hm(h + 1, 0), hm(t // 60 + 1, t % 60), hm(h + d // 60, d % 60 + 15) if d % 60 + 15 < 60 else hm(h + 2, 0)],
                   "%s + %s = <b>%s</b>." % (hm(h, 0), dauer(d), hm(t // 60, t % 60)))
    if kind == "zug":
        h, m = R.choice([8, 9, 10, 14]), R.choice([10, 20, 40])
        d = R.choice([30, 45, 50])
        t = h * 60 + m + d
        return mcq("Der Zug fährt um %s ab und kommt um %s an. Wie lange dauert die Fahrt?" % (hm(h, m), hm(t // 60, t % 60)), dauer(d),
                   [dauer(x) for x in (d + 10, d - 10, 100 - d if 100 - d != d else d + 20)], "Von %s bis %s: <b>%s</b>." % (hm(h, m), hm(t // 60, t % 60), dauer(d)))
    h = R.choice([15, 16, 17])
    return mcq("%s hat Fußballtraining von %s bis %s. Wie lange dauert das Training?" % (p[0], hm(h, 0), hm(h + 1, 30)), "1 h 30 min",
               ["30 min", "2 h 30 min", "1 h 50 min"], "Von %s bis %s ist 1 Stunde, dann noch 30 Minuten: <b>1 h 30 min</b>." % (hm(h, 0), hm(h + 1, 0)))


def main():
    seen = set()
    sets = [
        ("Volle und halbe Stunden", mix(R, seen, [(voll_halb, 20)])),
        ("Viertelstunden", mix(R, seen, [(viertel, 20)])),
        ("Minuten ablesen", mix(R, seen, [(minuten, 20)])),
        ("Zeitspannen", mix(R, seen, [(spanne, 20)])),
        ("Kalender und Sachaufgaben", mix(R, seen, [(kalender, 20)])),
    ]
    body = lesson(
        ["Der <b>kurze Zeiger</b> zeigt die Stunden, der <b>lange Zeiger</b> die Minuten.",
         "Steht der lange Zeiger auf der 12, ist es eine volle Stunde. Steht er auf der 6, ist es halb.",
         "„Halb vier“ heißt eine halbe Stunde <b>vor</b> vier Uhr: 3:30 Uhr.",
         "Viertel nach drei = 3:15 Uhr. Viertel vor vier = 3:45 Uhr. 1 h = 60 min."],
        [example("Der lange Zeiger steht auf der 4, der kurze kurz nach der 8", ["4 %s 5 = 20 Minuten" % "·"], "8:20 Uhr"),
         example("Von 9:15 Uhr bis 10:00 Uhr", ["bis 9:30 sind 15 min", "bis 10:00 noch 30 min"], "45 min")],
        [["halb vier = 4:30 Uhr", "halb vier = 3:30 Uhr"],
         ["Den kurzen Zeiger als Minuten lesen", "Kurz = Stunde, lang = Minuten"],
         ["1 h = 100 min", "1 h = 60 min"]],
        extra=table(["Uhrzeit", "So sagt man"], [["3:00 Uhr", "drei Uhr"], ["3:15 Uhr", "Viertel nach drei"], ["3:30 Uhr", "halb vier"], ["3:45 Uhr", "Viertel vor vier"]]))
    faq = [
        {"q": "Warum ist „halb vier“ 3:30 Uhr?", "a": "„Halb“ bezieht sich auf die kommende Stunde: Man ist auf halbem Weg zu vier Uhr. In manchen Regionen sagt man auch „drei Uhr dreißig“."},
        {"q": "Was lernen Kinder in Klasse 2 zur Uhr?", "a": "Volle, halbe und Viertelstunden, Minuten in Fünferschritten und einfache Zeitspannen. Die 24-Stunden-Zählung wird in Klasse 3 vertieft."},
        {"q": "Wie übt man das Uhrlesen?", "a": "Mit einer Lernuhr mit beweglichen Zeigern und im Alltag: Wann beginnt die Schule? Wann gibt es Abendessen?"},
        {"q": "Was ist eine Zeitspanne?", "a": "Die Zeit, die zwischen zwei Uhrzeiten vergeht, zum Beispiel von 8:00 Uhr bis 8:45 Uhr sind 45 Minuten."},
    ]
    make_unit(R, "uhrzeit", "G",
              "Die Schülerinnen und Schüler lesen Uhrzeiten auf der analogen Uhr ab (volle, halbe und Viertelstunden, Minuten), benennen Uhrzeiten, bestimmen einfache Zeitspannen und orientieren sich im Kalender (Zusammenfassung).",
              "Uhrzeit: Uhr lesen und Zeitspannen",
              "Uhrzeit lernen Klasse 2 – Arbeitsblätter mit Lösungen",
              "Uhrzeit",
              "Uhrzeit für Klasse 2: volle und halbe Stunden, Viertelstunden, Minuten ablesen, Zeitspannen, Wochentage und Monate. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Kurzer Zeiger: Stunde. Langer Zeiger: Minuten.",
              "Halb vier = 3:30 Uhr",
              body, faq, sets, 14, grade="klasse-2")


if __name__ == "__main__":
    main()
