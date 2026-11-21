# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 3: Dividieren mit Rest（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k3_dividieren_mit_rest.py
Teilen mit Rest im Einmaleins, den Rest bestimmen, geht es auf?, Probe, Sachaufgaben (aufrunden oder abrunden?).
Fehler: Rest größer als der Teiler (17 : 5 = 2 Rest 7), Ergebnis um 1 daneben, bei Sachaufgaben den Rest vergessen.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids, MAL, GETEILT, wrap
from ws_common import GREEN, FILL, INK

R = random.Random(49009)
KIDS = Kids(R)


def bleib(r):
    return "Es bleibt 1 übrig" if r == 1 else "Es bleiben %d übrig" % r


def ub(n):
    return "1 bleibt übrig" if n == 1 else "%d bleiben übrig" % n


def rr(q, r):
    return "%d Rest %d" % (q, r) if r else "%d" % q


def gruppen(t, d):
    """Punkte in Gruppen zu d, Rest rot umrandet"""
    q, r = divmod(t, d)
    s, x = [], 8
    for g in range(q):
        s.append("<rect x='%d' y='6' width='%d' height='30' rx='8' fill='none' stroke='%s' stroke-width='1.5'/>" % (x, d * 14 + 6, GREEN))
        for k in range(d):
            s.append("<circle cx='%d' cy='21' r='5' fill='%s' stroke='%s'/>" % (x + 10 + k * 14, FILL, GREEN))
        x += d * 14 + 14
    for k in range(r):
        s.append("<circle cx='%d' cy='21' r='5' fill='#f6c6c0' stroke='#c0392b'/>" % (x + 6 + k * 14))
    x += r * 14 + 8
    return wrap(x, 42, "".join(s), "Punkte in Gruppen")


def task():
    d = R.randint(2, 9)
    q = R.randint(2, 9)
    r = R.randint(1, d - 1)
    t = d * q + r
    pic = gruppen(t, d) if t <= 30 and R.random() < 0.4 else ""
    w = [rr(q - 1, r + d), rr(q + 1, r), rr(q, r + 1) if r + 1 < d else rr(q, r - 1) if r > 1 else rr(q + 1, 0), rr(q, 0), rr(q - 1, r)]
    return mcq(pic + "%d %s %d = ?" % (t, GETEILT, d), rr(q, r), [x for x in w if x != rr(q, r)],
               "Die größte Zahl der %der-Reihe bis %d ist %d (%d %s %d). %s: <b>%s</b>."
               % (d, t, d * q, q, MAL, d, bleib(r), rr(q, r)))


def rest():
    d = R.randint(3, 9)
    q = R.randint(2, 10)
    r = R.randint(0, d - 1)
    t = d * q + r
    if t > 100:
        return None
    w = [r + 1 if r + 1 < d + 1 else r - 1, r + d, q, d - r if d - r != r else r + 2, 0 if r else 1]
    return mcq("Welchen Rest hat %d %s %d?" % (t, GETEILT, d), str(r), [str(x) for x in w if x != r],
               "%d %s %d = %d, %d − %d = %d. Der Rest ist <b>%d</b>." % (q, MAL, d, d * q, t, d * q, r, r))


def aufgehen():
    d = R.randint(3, 9)
    q = R.randint(3, 9)
    ok = d * q
    bad = []
    for _ in range(20):
        x = d * R.randint(3, 9) + R.randint(1, d - 1)
        if x not in bad and x != ok:
            bad.append(x)
        if len(bad) == 3:
            break
    if len(bad) < 3:
        return None
    alle = bad + [ok]
    R.shuffle(alle)
    return mcq("Welche Zahl kann man ohne Rest durch %d teilen? %s" % (d, ", ".join(str(x) for x in alle)), str(ok), [str(x) for x in bad],
               "%d gehört zur %der-Reihe: %d %s %d = %d. Richtig: <b>%d</b>." % (ok, d, q, MAL, d, ok, ok))


def probe():
    d = R.randint(3, 9)
    q = R.randint(3, 9)
    r = R.randint(1, d - 1)
    t = d * q + r
    ans = "%d %s %d + %d = %d" % (q, MAL, d, r, t)
    w = ["%d %s %d − %d = %d" % (q, MAL, d, r, q * d - r), "%d %s %d + %d = %d" % (q, MAL, r, d, q * r + d),
         "%d %s %d = %d" % (q, MAL, d, q * d), "%d + %d + %d = %d" % (q, d, r, q + d + r)]
    return mcq("Welche Probe passt zu %d %s %d = %d Rest %d?" % (t, GETEILT, d, q, r), ans, w,
               "Ergebnis mal Teiler, dann den Rest dazu: <b>%s</b>." % ans)


SACHE_UP = [
    ("%d Kinder fahren mit Autos zum Ausflug. In jedes Auto passen %d Kinder. Wie viele Autos braucht man?", "Autos"),
    ("%d Bücher sollen in Kisten gepackt werden. In eine Kiste passen %d Bücher. Wie viele Kisten braucht man?", "Kisten"),
    ("%d Kinder wollen Boot fahren. In ein Boot passen %d Kinder. Wie viele Boote braucht man mindestens?", "Boote"),
]
SACHE_DOWN = [
    ("%d Eier werden in Schachteln zu %d verpackt. Wie viele volle Schachteln gibt es?", "Schachteln"),
    ("Aus %d Blumen bindet der Gärtner Sträuße mit je %d Blumen. Wie viele Sträuße kann er binden?", "Sträuße"),
]


def sache():
    kind = R.choice(["up", "down", "rest", "rest"])
    d = R.randint(3, 9)
    q = R.randint(3, 9)
    r = R.randint(1, d - 1)
    t = d * q + r
    if kind == "up":
        tmp, u = R.choice(SACHE_UP)
        ans = q + 1
        w = [q, rr(q, r), q + 2, r]
        return mcq(tmp % (t, d), "%d %s" % (ans, u), ["%s %s" % (x, u) for x in w if x != ans and x != 0],
                   "%d %s %d = %d Rest %d. Die restlichen %d brauchen auch noch Platz, also <b>%d %s</b>." % (t, GETEILT, d, q, r, r, ans, u))
    if kind == "down":
        tmp, u = R.choice(SACHE_DOWN[:2])
        w = [q + 1, rr(q, r), r, q - 1]
        return mcq(tmp % (t, d), "%d %s" % (q, u), ["%s %s" % (x, u) for x in w if x != q and x != 0],
                   "%d %s %d = %d Rest %d. Nur volle zählen, also <b>%d %s</b>. %s." % (t, GETEILT, d, q, r, q, u, bleib(r)))
    p = KIDS.next()
    thing = R.choice([("Murmeln", "Murmeln"), ("Sammelkarten", "Karten"), ("Gummibärchen", "Gummibärchen")])
    q2 = "%s verteilt %d %s gerecht an %d Kinder. Wie viele bekommt jedes Kind und wie viele bleiben übrig?" % (p[0], t, thing[0], d)
    ans = "%d %s, %s" % (q, thing[1], ub(r))
    w = ["%d %s, %s" % (q + 1, thing[1], ub(r)), "%d %s, %s" % (q, thing[1], ub(r + 1 if r + 1 < d else r - 1 if r > 1 else d)),
         "%d %s, %s" % (q - 1, thing[1], ub(r + d)), "%d %s, keine bleiben übrig" % (q, thing[1])]
    return mcq(q2, ans, w, "%d %s %d = %d Rest %d: <b>%s</b>." % (t, GETEILT, d, q, r, ans))


def main():
    seen = set()
    sets = [
        ("Teilen mit Rest", mix(R, seen, [(task, 20)])),
        ("Den Rest bestimmen", mix(R, seen, [(rest, 20)])),
        ("Geht es auf?", mix(R, seen, [(aufgehen, 12), (task, 8)])),
        ("Die Probe", mix(R, seen, [(probe, 14), (rest, 6)])),
        ("Sachaufgaben mit Rest", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Nicht jede Zahl lässt sich ohne Rest teilen. Bei 17 %s 5 passen drei Fünfer hinein (15). 2 bleiben übrig: 17 %s 5 = 3 Rest 2." % (GETEILT, GETEILT),
         "Suche die größte Zahl der Reihe, die noch hineinpasst. Der <b>Rest</b> ist immer <b>kleiner als die Zahl, durch die du teilst</b>.",
         "Probe: Ergebnis mal Teiler plus Rest: 3 %s 5 + 2 = 17." % MAL,
         "Bei Sachaufgaben überlegst du: Braucht der Rest noch ein Auto (aufrunden) oder zählen nur volle Packungen (abrunden)?"],
        [example("38 %s 6" % GETEILT, ["6er-Reihe: 36 ist die größte Zahl bis 38 (6 %s 6)" % MAL, "38 − 36 = 2"], "6 Rest 2"),
         example("26 Kinder, in ein Auto passen 4. Wie viele Autos?", ["26 %s 4 = 6 Rest 2" % GETEILT, "Die 2 Kinder brauchen auch ein Auto"], "7 Autos")],
        [["17 %s 5 = 2 Rest 7" % GETEILT, "Der Rest muss kleiner als 5 sein: 3 Rest 2"],
         ["26 Kinder, 4 pro Auto → 6 Autos", "Die 2 übrigen Kinder brauchen noch ein Auto: 7"],
         ["Probe: 3 %s 5 − 2" % MAL, "Den Rest addieren: 3 %s 5 + 2 = 17" % MAL]],
        extra=gruppen(17, 5))
    faq = [
        {"q": "Wann lernt man Division mit Rest?", "a": "Meist am Ende von Klasse 2 oder in Klasse 3, sobald das Einmaleins sicher ist."},
        {"q": "Wie schreibt man den Rest?", "a": "In der Grundschule schreibt man 17 : 5 = 3 Rest 2 (manchmal abgekürzt 3 R 2)."},
        {"q": "Warum muss der Rest kleiner sein als der Teiler?", "a": "Wäre der Rest gleich groß oder größer, passte noch eine Gruppe hinein."},
        {"q": "Was ist bei Sachaufgaben mit Rest wichtig?", "a": "Man muss überlegen, was der Rest bedeutet: Manchmal braucht man noch ein Auto mehr, manchmal zählen nur volle Packungen."},
    ]
    make_unit(R, "dividieren-mit-rest", "Z",
              "Die Schülerinnen und Schüler dividieren mit Rest im Bereich des Einmaleins, deuten den Rest im Sachzusammenhang und kontrollieren mit der Umkehraufgabe (Zusammenfassung).",
              "Dividieren mit Rest",
              "Division mit Rest Klasse 3 – Arbeitsblätter mit Lösungen",
              "Teilen mit Rest",
              "Division mit Rest für Klasse 3: Teilen mit Rest im Einmaleins, Rest bestimmen, Probe und Sachaufgaben (aufrunden oder abrunden). 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Der Rest ist immer kleiner als der Teiler.",
              "17 : 5 = 3 Rest 2, Probe: 3 · 5 + 2 = 17.",
              body, faq, sets, 9)


if __name__ == "__main__":
    main()
