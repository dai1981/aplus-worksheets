# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 4: Zeit – Sekunden bis Jahre, Zeitspannen und Kalender（Leitidee Größen und Messen）
  python3 tools/gen_de_mathe_k4_zeit.py
Zeiteinheiten umrechnen, Zeitspannen, Anfang und Ende berechnen, Kalender und Wochentage, Sachaufgaben.
Fehler: 1 min = 100 s, 3 h 20 min = 320 min, Zeitspanne über die volle Stunde oder Mitternacht falsch, Monatslängen verwechselt.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, MAL, table

R = random.Random(49113)
KIDS = Kids(R)
TAGE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
MONATE = [("Januar", 31), ("Februar", 28), ("März", 31), ("April", 30), ("Mai", 31), ("Juni", 30), ("Juli", 31), ("August", 31),
          ("September", 30), ("Oktober", 31), ("November", 30), ("Dezember", 31)]


def hm(t):
    t %= 24 * 60
    return "%d:%02d Uhr" % (t // 60, t % 60)


def dauer(m):
    h, mm = divmod(m, 60)
    if h and mm:
        return "%d h %d min" % (h, mm)
    return "%d h" % h if h else "%d min" % mm


def einheiten():
    kind = R.choice(["min-s", "h-min", "tag-h", "woche-tag", "jahr-monat", "s-min"])
    if kind == "min-s":
        a, b = R.randint(1, 9), R.randint(5, 55)
        r = 60 * a + b
        return mcq("%d min %d s = ? s" % (a, b), "%d s" % r, ["%d s" % x for x in (100 * a + b, 10 * a + b, r + 60)], "1 min = 60 s. %d %s 60 s + %d s = <b>%d s</b>." % (a, MAL, b, r))
    if kind == "h-min":
        a, b = R.randint(1, 9), R.choice([5, 10, 15, 20, 25, 30, 40, 45, 50])
        r = 60 * a + b
        return mcq("%d h %d min = ? min" % (a, b), "%d min" % r, ["%d min" % x for x in (100 * a + b, 10 * a + b, r + 60)], "1 h = 60 min. %d %s 60 min + %d min = <b>%d min</b>." % (a, MAL, b, r))
    if kind == "tag-h":
        a, b = R.randint(1, 4), R.randint(1, 23)
        r = 24 * a + b
        return mcq("%d %s %d h = ? h" % (a, "Tag" if a == 1 else "Tage", b), "%d h" % r, ["%d h" % x for x in (12 * a + b, 10 * a + b, r + 24)], "1 Tag = 24 h. %d %s 24 h + %d h = <b>%d h</b>." % (a, MAL, b, r))
    if kind == "woche-tag":
        a, b = R.randint(2, 9), R.randint(1, 6)
        r = 7 * a + b
        return mcq("%d Wochen %d %s = ? Tage" % (a, b, "Tag" if b == 1 else "Tage"), "%d Tage" % r, ["%d Tage" % x for x in (5 * a + b, 10 * a + b, r + 7)], "1 Woche = 7 Tage. %d %s 7 + %d = <b>%d Tage</b>." % (a, MAL, b, r))
    if kind == "jahr-monat":
        a, b = R.randint(1, 5), R.randint(1, 11)
        r = 12 * a + b
        return mcq("%d %s %d %s = ? Monate" % (a, "Jahr" if a == 1 else "Jahre", b, "Monat" if b == 1 else "Monate"), "%d Monate" % r,
                   ["%d Monate" % x for x in (10 * a + b, 52 * a + b, r + 12)], "1 Jahr = 12 Monate. %d %s 12 + %d = <b>%d Monate</b>." % (a, MAL, b, r))
    s = R.randint(61, 599)
    if s % 60 == 0:
        return None
    m, ss = divmod(s, 60)
    ans = "%d min %d s" % (m, ss)
    return mcq("%d s = ? min ? s" % s, ans, ["%d min %d s" % (s // 100, s % 100) if s % 100 < 60 else "%d min %d s" % (m + 1, ss), "%d min %d s" % (m, ss + 10 if ss + 10 < 60 else ss - 10), "%d min %d s" % (m - 1 if m > 1 else m + 2, ss)],
               "60 s = 1 min. %d s = %d %s 60 s + %d s = <b>%s</b>." % (s, m, MAL, ss, ans))


def spanne():
    a = R.randint(6 * 60, 22 * 60) // 5 * 5
    d = R.choice([35, 50, 75, 95, 110, 135, 165, 190, 225, 250, 310]) + R.choice([0, 5])
    b = a + d
    over = b >= 24 * 60
    w = [d + 60, d - 20 if d > 25 else d + 20, ((b // 60 - a // 60) * 100 + (b % 60 - a % 60)) if b % 60 >= a % 60 else d + 40]
    return mcq("Von %s bis %s%s. Wie lange ist das?" % (hm(a), hm(b), " (am nächsten Tag)" if over else ""), dauer(d), [dauer(x) for x in w if x > 0 and dauer(x) != dauer(d)],
               "Rechne in Schritten über die volle Stunde: von %s bis %s sind es <b>%s</b>." % (hm(a), hm(b), dauer(d)))


def zeitpunkt():
    a = R.randint(7 * 60, 21 * 60) // 5 * 5
    d = R.choice([25, 45, 70, 85, 105, 125, 150, 175, 200]) 
    if R.random() < 0.5:
        b = a + d
        q = "Ein Film beginnt um %s und dauert %s. Wann ist er zu Ende?" % (hm(a), dauer(d))
        ans = hm(b)
        w = [hm(a + d + 60), hm(a + d - 60), hm(a + (d // 60) * 100 + d % 60) if (a % 60 + d % 60) >= 60 else hm(b + 10)]
        e = "%s + %s = <b>%s</b>." % (hm(a), dauer(d), ans)
    else:
        b = a
        a = b - d
        q = "Ein Zug kommt um %s an. Die Fahrt hat %s gedauert. Wann ist er abgefahren?" % (hm(b), dauer(d))
        ans = hm(a)
        w = [hm(b + d), hm(a + 60), hm(a - 10)]
        e = "Rückwärts: %s − %s = <b>%s</b>." % (hm(b), dauer(d), ans)
    return mcq(q, ans, [x for x in w if x != ans], e)


def kalender():
    kind = R.choice(["wochentag", "tage", "monat", "dauer"])
    if kind == "wochentag":
        m, ln = R.choice(MONATE)
        d1 = R.randint(1, 10)
        t1 = R.randint(0, 6)
        add = R.choice([7, 14, 21, 3, 10, 17, 5, 12])
        d2 = d1 + add
        if d2 > ln:
            return None
        ans = TAGE[(t1 + add) % 7]
        w = [TAGE[(t1 + add + 1) % 7], TAGE[(t1 + add - 1) % 7], TAGE[(t1 + add + 2) % 7]]
        return mcq("Der %d. %s ist ein %s. Welcher Wochentag ist der %d. %s?" % (d1, m, TAGE[t1], d2, m), ans, w,
                   "%d Tage später. %d Tage sind %d volle Wochen%s: <b>%s</b>." % (add, add, add // 7, " und %d Tage" % (add % 7) if add % 7 else "", ans))
    if kind == "tage":
        m, ln = R.choice(MONATE)
        if m == "Februar":
            return mcq("Wie viele Tage hat der Februar (kein Schaltjahr)?", "28 Tage", ["30 Tage", "31 Tage", "29 Tage"], "Der Februar hat <b>28 Tage</b>, im Schaltjahr 29.")
        return mcq("Wie viele Tage hat der %s?" % m, "%d Tage" % ln, ["%d Tage" % x for x in (61 - ln, 28, 29)], "Der %s hat <b>%d Tage</b>." % (m, ln))
    if kind == "monat":
        i = R.randint(0, 11)
        k = R.randint(2, 9)
        ans = MONATE[(i + k) % 12][0]
        return mcq("Welcher Monat kommt %d Monate nach dem %s?" % (k, MONATE[i][0]), ans, [MONATE[(i + k + 1) % 12][0], MONATE[(i + k - 1) % 12][0], MONATE[(i - k) % 12][0]],
                   "Zähle %d Monate weiter: <b>%s</b>." % (k, ans))
    i = R.randint(0, 10)
    m, ln = MONATE[i]
    d1 = R.randint(ln - 10, ln)
    d2 = R.randint(1, 15)
    days = ln - d1 + d2
    nm = MONATE[i + 1][0]
    return mcq("Die Ferien gehen vom %d. %s bis zum %d. %s (der erste Tag zählt nicht mit). Wie viele Tage sind das?" % (d1, m, d2, nm), "%d Tage" % days,
               ["%d Tage" % x for x in (days + 1, 30 - d1 + d2 if ln != 30 else days - 1, days + 2) if x != days and x > 0],
               "Bis zum Monatsende: %d − %d = %d Tage, dann noch %d Tage: <b>%d Tage</b>." % (ln, d1, ln - d1, d2, days))


def sache():
    p = KIDS.next()
    kind = R.choice(["lauf", "nacht", "training", "alter"])
    if kind == "lauf":
        a, b = R.randint(55, 95), R.randint(55, 95)
        if a == b:
            return None
        p2 = KIDS.next()
        q = "Beim 400-m-Lauf braucht %s %s, %s braucht %s. Wie viele Sekunden ist der Schnellere schneller?" % (p[0], "%d min %d s" % divmod(a, 60) if a >= 60 else "%d s" % a,
                                                                                                                 p2[0], "%d min %d s" % divmod(b, 60) if b >= 60 else "%d s" % b)
        q = q.replace("min 0 s", "min")
        r = abs(a - b)
        return mcq(q, "%d s" % r, ["%d s" % x for x in (r + 40, r + 10, abs((a // 60 * 100 + a % 60) - (b // 60 * 100 + b % 60))) if x != r and x > 0],
                   "In Sekunden: %d s und %d s. %d − %d = <b>%d s</b>." % (a, b, max(a, b), min(a, b), r))
    if kind == "nacht":
        a = R.randint(20 * 60, 23 * 60 + 30) // 5 * 5
        d = R.randint(5 * 60, 10 * 60) // 5 * 5
        b = a + d
        q = "Ein Nachtzug fährt um %s ab und kommt am nächsten Morgen um %s an. Wie lange dauert die Fahrt?" % (hm(a), hm(b))
        return mcq(q, dauer(d), [dauer(x) for x in (d + 60, d - 60, 24 * 60 - d) if dauer(x) != dauer(d)],
                   "Bis Mitternacht: %s, dann bis %s: %s. Zusammen <b>%s</b>." % (dauer(24 * 60 - a), hm(b), dauer(b - 24 * 60), dauer(d)))
    if kind == "training":
        n, m = R.randint(2, 5), R.choice([45, 60, 75, 90])
        w = R.randint(4, 12)
        tot = n * m * w
        q = "%s trainiert %d-mal pro Woche je %d Minuten. Wie viele Stunden sind das in %d Wochen?" % (p[0], n, m, w)
        if tot % 60:
            return None
        r = tot // 60
        return mcq(q, "%d h" % r, ["%d h" % x for x in (tot // 100, r + n, n * m * w // 10) if x != r and x > 0],
                   "%d %s %d %s %d = %d min = <b>%d h</b>." % (n, MAL, m, MAL, w, tot, r))
    y = R.randint(2010, 2018)
    q = "%s ist im Jahr %d geboren. Wie alt wird %s im Jahr 2026?" % (p[0], y, p[1])
    r = 2026 - y
    return mcq(q, "%d Jahre" % r, ["%d Jahre" % x for x in (r + 1, r - 1, r + 10) if x > 0], "2026 − %d = <b>%d Jahre</b>." % (y, r))


def main():
    seen = set()
    sets = [
        ("Zeiteinheiten umrechnen", mix(R, seen, [(einheiten, 20)])),
        ("Zeitspannen", mix(R, seen, [(spanne, 20)])),
        ("Anfang und Ende berechnen", mix(R, seen, [(zeitpunkt, 20)])),
        ("Kalender", mix(R, seen, [(kalender, 20)])),
        ("Sachaufgaben zur Zeit", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["1 min = 60 s, 1 h = 60 min, 1 Tag = 24 h, 1 Woche = 7 Tage, 1 Jahr = 12 Monate (365 oder 366 Tage).",
         "Zeit wird <b>nicht</b> mit 100 gebündelt: 3 h 20 min = 180 min + 20 min = 200 min.",
         "Zeitspannen rechnest du in Schritten: bis zur vollen Stunde, dann die Stunden, dann die restlichen Minuten. Über Mitternacht rechnest du erst bis 24 Uhr.",
         "Wochentage wiederholen sich alle 7 Tage."],
        [example("Von 21:40 Uhr bis 6:15 Uhr", ["bis 22:00 Uhr: 20 min", "bis 6:00 Uhr: 8 h", "bis 6:15 Uhr: 15 min"], "8 h 35 min"),
         example("2 min 15 s in Sekunden", ["2 %s 60 s = 120 s" % MAL, "120 s + 15 s"], "135 s")],
        [["3 h 20 min = 320 min", "3 %s 60 + 20 = 200 min" % MAL],
         ["1 min = 100 s", "1 min = 60 s"],
         ["Über Mitternacht einfach abziehen", "Erst bis 24 Uhr, dann weiter"]],
        extra=table(["Monat", "Tage"], [[m, str(d) if m != "Februar" else "28 (29)"] for m, d in MONATE]))
    faq = [
        {"q": "Welche Zeiteinheiten lernt man in Klasse 4?", "a": "Sekunde, Minute, Stunde, Tag, Woche, Monat und Jahr mit ihren Umrechnungen."},
        {"q": "Wie merkt man sich die Tage der Monate?", "a": "Mit der Knöchelregel: Monate auf den Knöcheln haben 31 Tage, die in den Tälern 30 Tage (Februar 28 oder 29)."},
        {"q": "Wie rechnet man Zeitspannen über Mitternacht?", "a": "Erst die Zeit bis 24:00 Uhr, dann die Zeit ab 0:00 Uhr bis zur Ankunft, und beides addieren."},
        {"q": "Warum rechnet man bei der Zeit nicht mit 100?", "a": "Weil eine Stunde 60 Minuten und eine Minute 60 Sekunden hat. Darum gilt 1 h 30 min nicht als 130 min, sondern als 90 min."},
    ]
    make_unit(R, "zeit-und-kalender", "G",
              "Die Schülerinnen und Schüler rechnen mit Zeiteinheiten von Sekunden bis Jahren, bestimmen Zeitpunkte und Zeitspannen und nutzen den Kalender (Zusammenfassung).",
              "Zeit: Sekunden, Zeitspannen und Kalender",
              "Zeit Klasse 4 – Zeitspannen, Sekunden und Kalender, Arbeitsblätter mit Lösungen",
              "Zeit und Kalender",
              "Klasse 4: Zeiteinheiten umrechnen (s, min, h, Tage, Wochen, Monate), Zeitspannen auch über Mitternacht, Kalender und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "1 h = 60 min, 1 min = 60 s – nicht 100!",
              "Zeitspannen in Schritten über die volle Stunde rechnen.",
              body, faq, sets, 13, grade="klasse-4")


if __name__ == "__main__":
    main()
