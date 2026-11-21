# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 3: Diagramme und Tabellen（Leitidee Daten und Zufall）
  python3 tools/gen_de_mathe_k3_diagramme_und_tabellen.py
Strichlisten, Säulendiagramme ablesen, Tabellen lesen, Daten vergleichen, Umfragen auswerten.
Fehler: Fünferbündel als 4 gezählt, Skala mit Schritten von 2 oder 5 als 1er gelesen, „wie viele mehr“ mit plus gerechnet.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, saeulen, strichliste, table, wrap, fig

R = random.Random(49018)

TOPICS = [
    ("Lieblingstiere der Klasse 3a", ["Hund", "Katze", "Pferd", "Hase", "Vogel"], "Kinder"),
    ("Lieblingsobst", ["Apfel", "Banane", "Erdbeere", "Kirsche", "Traube"], "Kinder"),
    ("Wie kommen die Kinder zur Schule?", ["zu Fuß", "Fahrrad", "Bus", "Auto", "Roller"], "Kinder"),
    ("Lieblingssport", ["Fußball", "Schwimmen", "Turnen", "Tanzen", "Reiten"], "Kinder"),
    ("Ausgeliehene Bücher in der Schulbücherei", ["Mo", "Di", "Mi", "Do", "Fr"], "Bücher"),
    ("Besucher im Schwimmbad", ["Mo", "Di", "Mi", "Do", "Fr"], "Besucher"),
]


TAG = {"Mo": "Montag", "Di": "Dienstag", "Mi": "Mittwoch", "Do": "Donnerstag", "Fr": "Freitag"}


def tt(t):
    return t if t.endswith("?") else t + ":"


def frage(unit, c):
    if unit == "Kinder":
        return "Wie viele Kinder haben „%s“ gewählt?" % c
    return "Wie viele %s waren es am %s?" % (unit, TAG.get(c, c))


def bei(c):
    return "am %s" % TAG[c] if c in TAG else "bei „%s“" % c


def strich():
    n = R.randint(6, 24)
    s = strichliste(n)
    w = [n - n // 5, n + 1, n - 1, n // 5 * 4 + n % 5 if n >= 5 else n + 2, n + 5]
    return mcq(fig(s) + "Wie viele Striche zeigt die Strichliste?", str(n), [str(x) for x in w if x != n and x > 0],
               "Jedes Bündel mit Querstrich sind 5 Striche: %d %s 5 + %d = <b>%d</b>." % (n // 5, "·", n % 5, n))


def strich_tab():
    t, cats, unit = R.choice(TOPICS[:4])
    cs = R.sample(cats, 3)
    vals = R.sample(range(4, 19), 3)
    rows = [[c, strichliste(v), ""] for c, v in zip(cs, vals)]
    html = table(["", "Strichliste"], [[r[0], r[1]] for r in rows])
    k = R.randint(0, 2)
    v = vals[k]
    return mcq("%s %s Wie viele Kinder haben „%s“ gewählt?" % (tt(t), html, cs[k]), str(v),
               [str(x) for x in (v - v // 5, v + 1, v - 1, vals[(k + 1) % 3]) if x != v and x > 0],
               "Zähle die Fünferbündel und die einzelnen Striche: <b>%d</b>." % v)


def data(step):
    t, cats, unit = R.choice(TOPICS)
    n = R.randint(4, 5)
    cs = cats[:n] if cats[0] == "Mo" else R.sample(cats, n)
    hi = {1: 10, 2: 20, 5: 50, 10: 100}[step]
    vals = [R.randint(1, hi // step) * step for _ in range(n)]
    if len(set(vals)) < n:
        return None
    return t, cs, vals, unit


def ablesen():
    step = R.choice([1, 2, 2, 5, 10])
    d = data(step)
    if not d:
        return None
    t, cs, vals, unit = d
    pic = saeulen(list(zip(cs, vals)), unit, label="Säulendiagramm: " + t, step=step if step > 1 else None)
    kind = R.choice(["wert", "wert", "max", "min"])
    if kind == "wert":
        k = R.randrange(len(cs))
        v = vals[k]
        w = [v // step if step > 1 else v + 1, v + step, v - step if v > step else v + 2 * step, v + 1]
        q = "%s %s" % (tt(t), frage(unit, cs[k]))
        return mcq(pic + q, str(v), [str(x) for x in w if x != v and x > 0],
                   "Lies an der Achse ab. Ein Kästchen bedeutet %d. Die Säule „%s“ reicht bis <b>%d</b>." % (step, cs[k], v))
    k = vals.index(max(vals)) if kind == "max" else vals.index(min(vals))
    others = [c for c in cs if c != cs[k]]
    return mcq(pic + "%s Welche Säule ist am %s?" % (tt(t), "höchsten" if kind == "max" else "niedrigsten"), cs[k], R.sample(others, 3),
               "Am %s ist die Säule „<b>%s</b>“ (%d)." % ("höchsten" if kind == "max" else "niedrigsten", cs[k], vals[k]))


def tabelle():
    t, cats, unit = R.choice(TOPICS[4:] + TOPICS[:2])
    cs = cats[:5] if cats[0] == "Mo" else R.sample(cats, 4)
    vals = [R.randint(12, 95) for _ in cs]
    html = table(["", ] + cs, [[unit] + [str(v) for v in vals]])
    kind = R.choice(["summe", "diff", "doppelt"])
    if kind == "summe":
        a, b = R.sample(range(len(cs)), 2)
        r = vals[a] + vals[b]
        q = "%s %s Wie viele %s sind es %s und %s zusammen?" % (tt(t), html, unit, bei(cs[a]), bei(cs[b]))
        w = [abs(vals[a] - vals[b]), r + 10, r - 1, r + 1]
        e = "%d + %d = <b>%d</b>." % (vals[a], vals[b], r)
    elif kind == "diff":
        a, b = R.sample(range(len(cs)), 2)
        if vals[a] == vals[b]:
            return None
        if vals[a] < vals[b]:
            a, b = b, a
        r = vals[a] - vals[b]
        q = "%s %s Wie viele %s sind es %s mehr als %s?" % (tt(t), html, unit, bei(cs[a]), bei(cs[b]))
        w = [vals[a] + vals[b], r + 10, r - 1 if r > 1 else r + 2, vals[a]]
        e = "Wie viele mehr: größere Zahl minus kleinere Zahl. %d − %d = <b>%d</b>." % (vals[a], vals[b], r)
    else:
        r = sum(vals)
        q = "%s %s Wie viele %s sind es insgesamt?" % (tt(t), html, unit)
        w = [r + 10, r - 10, r - vals[-1], r + 1]
        e = "Alle Zahlen addieren: %s = <b>%d</b>." % (" + ".join(str(v) for v in vals), r)
    return mcq(q, str(r), [str(x) for x in w if x != r and x > 0], e)


def vergleichen():
    step = R.choice([2, 5, 10])
    d = data(step)
    if not d:
        return None
    t, cs, vals, unit = d
    pic = saeulen(list(zip(cs, vals)), unit, label="Säulendiagramm: " + t, step=step)
    a, b = R.sample(range(len(cs)), 2)
    if vals[a] < vals[b]:
        a, b = b, a
    kind = R.choice(["mehr", "zusammen", "halb"])
    if kind == "mehr":
        r = vals[a] - vals[b]
        q = "Wie viele %s sind es %s mehr als %s?" % (unit, bei(cs[a]), bei(cs[b]))
        w = [vals[a] + vals[b], r // step if step > 1 and r // step != r else r + step, r + step, vals[a]]
        e = "%d − %d = <b>%d</b>." % (vals[a], vals[b], r)
    elif kind == "zusammen":
        r = vals[a] + vals[b]
        q = "Wie viele %s sind es %s und %s zusammen?" % (unit, bei(cs[a]), bei(cs[b]))
        w = [vals[a] - vals[b], r + step, r - step, (vals[a] + vals[b]) // step]
        e = "%d + %d = <b>%d</b>." % (vals[a], vals[b], r)
    else:
        r = sum(vals)
        q = "Wie viele %s sind es insgesamt?" % unit
        w = [r + step, r - step, len(cs) * max(vals), r - vals[0]]
        e = "%s = <b>%d</b>." % (" + ".join(str(v) for v in vals), r)
    return mcq(pic + tt(t) + " " + q, str(r), [str(x) for x in w if x != r and x > 0], e)


def umfrage():
    t, cats, unit = R.choice(TOPICS[:4])
    cs = R.sample(cats, 4)
    vals = R.sample(range(2, 12), 4)
    html = table(["Antwort", "Anzahl"], [[c, str(v)] for c, v in zip(cs, vals)])
    kind = R.choice(["klasse", "zweit", "doppelt", "weniger"])
    if kind == "klasse":
        r = sum(vals)
        q = "Umfrage „%s“: %s Jedes Kind hat einmal geantwortet. Wie viele Kinder sind in der Klasse?" % (t, html)
        return mcq(q, str(r), [str(x) for x in (r + 1, r - max(vals), max(vals), r + 10) if x != r and x > 0], "Alle Antworten zusammen: <b>%d Kinder</b>." % r)
    order = sorted(range(4), key=lambda i: -vals[i])
    if kind == "zweit":
        k = order[1]
        q = "Umfrage „%s“: %s Welche Antwort ist auf Platz 2?" % (t, html)
        return mcq(q, cs[k], [cs[i] for i in order if i != k], "Ordne nach der Anzahl: %s. Platz 2: <b>%s</b>." % (", ".join("%s (%d)" % (cs[i], vals[i]) for i in order), cs[k]))
    if kind == "doppelt":
        a = order[0]
        half = [i for i in range(4) if vals[i] * 2 == vals[a]]
        if not half:
            return None
        k = half[0]
        q = "Umfrage „%s“: %s Welche Antwort wurde halb so oft gewählt wie „%s“?" % (t, html, cs[a])
        return mcq(q, cs[k], [cs[i] for i in range(4) if i != k], "%d : 2 = %d. Das ist „<b>%s</b>“." % (vals[a], vals[k], cs[k]))
    a, b = order[0], order[-1]
    r = vals[a] - vals[b]
    q = "Umfrage „%s“: %s Wie viele Kinder mehr haben „%s“ gewählt als „%s“?" % (t, html, cs[a], cs[b])
    return mcq(q, str(r), [str(x) for x in (vals[a] + vals[b], r + 1, r - 1 if r > 1 else r + 2, vals[a]) if x != r], "%d − %d = <b>%d</b>." % (vals[a], vals[b], r))


def main():
    seen = set()
    sets = [
        ("Strichlisten", mix(R, seen, [(strich, 12), (strich_tab, 8)])),
        ("Säulendiagramme ablesen", mix(R, seen, [(ablesen, 20)])),
        ("Tabellen lesen", mix(R, seen, [(tabelle, 20)])),
        ("Daten vergleichen", mix(R, seen, [(vergleichen, 20)])),
        ("Umfragen auswerten", mix(R, seen, [(umfrage, 20)])),
    ]
    body = lesson(
        ["Mit einer <b>Strichliste</b> zählst du schnell: Jeder fünfte Strich wird quer gezogen. So entstehen Fünferbündel.",
         "In einem <b>Säulendiagramm</b> zeigt die Höhe jeder Säule die Anzahl. Schau zuerst, welche Schritte die Achse hat (1, 2, 5 oder 10).",
         "In einer <b>Tabelle</b> findest du die Zahl in der passenden Zeile und Spalte.",
         "„Wie viele mehr?“ rechnest du mit minus: größere Zahl − kleinere Zahl."],
        [example("Strichliste: zwei Fünferbündel und drei Striche", ["5 + 5 + 3"], "13"),
         example("Säule Hund: 14, Säule Katze: 8. Wie viele mehr wählen Hund?", ["14 − 8 = 6"], "6 Kinder mehr")],
        [["Ein Fünferbündel als 4 zählen", "Der Querstrich zählt mit: ein Bündel = 5"],
         ["Skala in 2er-Schritten wie 1er lesen", "Erst die Achse ansehen: ein Kästchen = 2"],
         ["„Wie viele mehr?“ mit plus rechnen", "Den Unterschied mit minus berechnen"]])
    faq = [
        {"q": "Welche Diagramme lernt man in Klasse 3?", "a": "Vor allem Strichlisten, Tabellen und Säulendiagramme (auch Balkendiagramme). Kinder lesen sie ab und erstellen sie aus eigenen Umfragen."},
        {"q": "Warum macht man bei Strichlisten Fünferbündel?", "a": "Bündel aus fünf Strichen lassen sich schnell zählen: zwei Bündel sind 10."},
        {"q": "Worauf muss man beim Ablesen achten?", "a": "Auf die Beschriftung der Achse. Ein Kästchen kann 1, 2, 5 oder 10 bedeuten."},
        {"q": "Wie kann man Daten im Alltag sammeln?", "a": "Mit Umfragen in der Klasse, Zählungen (zum Beispiel Autos vor der Schule) oder Messungen."},
    ]
    make_unit(R, "diagramme-und-tabellen", "D",
              "Die Schülerinnen und Schüler sammeln und strukturieren Daten in Strichlisten und Tabellen, stellen sie in Diagrammen dar und entnehmen Informationen aus Tabellen und Diagrammen (Zusammenfassung).",
              "Diagramme und Tabellen: Strichliste und Säulendiagramm",
              "Diagramme und Tabellen Klasse 3 – Strichliste, Säulendiagramm, Arbeitsblätter mit Lösungen",
              "Diagramme und Tabellen",
              "Daten für Klasse 3: Strichlisten zählen, Säulendiagramme ablesen, Tabellen lesen, Daten vergleichen und Umfragen auswerten. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Erst die Achse lesen, dann die Säule.",
              "„Wie viele mehr?“ heißt minus.",
              body, faq, sets, 18)


if __name__ == "__main__":
    main()
