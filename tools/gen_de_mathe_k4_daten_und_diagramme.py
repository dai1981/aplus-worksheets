# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 4: Daten und Diagramme（Leitidee Daten und Zufall）
  python3 tools/gen_de_mathe_k4_daten_und_diagramme.py
Säulendiagramme mit großen Zahlen (Skala 50, 100, 500), Werte zwischen den Linien, Vergleichen, Tabellen, Liniendiagramme (Temperatur), Umfragen.
Fehler: Skala nicht beachtet (1 Kästchen = 1), Wert der nächsten Linie abgelesen, Unterschied und Summe verwechselt.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, MAL, NB, wrap, table, saeulen
from ws_common import line, text, INK, GREEN, BLUE

R = random.Random(49118)
KIDS = Kids(R)

TOPICS = [
    ("Besucher im Zoo", ["Mo", "Di", "Mi", "Do", "Fr"], "Besucher", (500, 5000)),
    ("Ausgeliehene Bücher in der Bücherei", ["Mo", "Di", "Mi", "Do", "Fr"], "Bücher", (50, 500)),
    ("Verkaufte Brötchen in der Bäckerei", ["Mo", "Di", "Mi", "Do", "Fr", "Sa"], "Brötchen", (100, 900)),
    ("Besucher im Museum", ["Di", "Mi", "Do", "Fr"], "Besucher", (50, 400)),
    ("Gesammelte Pfandflaschen der Klassen", ["4a", "4b", "4c", "4d"], "Flaschen", (50, 300)),
    ("Zuschauer beim Fußballturnier", ["Fr", "Sa", "So"], "Zuschauer", (200, 1000)),
    ("Gelaufene Runden beim Sponsorenlauf", ["3a", "3b", "4a", "4b"], "Runden", (50, 400)),
]
LONG = {"Mo": "Montag", "Di": "Dienstag", "Mi": "Mittwoch", "Do": "Donnerstag", "Fr": "Freitag", "Sa": "Samstag", "So": "Sonntag",
        "Aug.": "August", "Sept.": "September", "Jan.": "Januar", "Feb.": "Februar"}


def wann(c):
    if c in ("Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"):
        return "am %s" % LONG[c]
    if c.endswith("Uhr"):
        return "um %s" % c
    if c[0].isdigit():
        return "bei der Klasse %s" % c
    return "im %s" % LONG.get(c, c)


def pick_topic(halb=False):
    t, cats, unit, (lo, hi) = R.choice(TOPICS)
    step = {50: 50, 100: 100, 200: 100, 500: 500}.get(lo, 50)
    if hi <= 500:
        step = 50
    elif hi <= 1000:
        step = 100
    else:
        step = 500
    unitstep = step // 2 if halb else step
    vals = [R.randint(max(1, lo // unitstep), hi // unitstep) * unitstep for _ in cats]
    if len(set(vals)) < len(vals):
        return None
    return t, cats, unit, vals, step


def ablesen(halb=False):
    def mk():
        d = pick_topic(halb)
        if not d:
            return None
        t, cs, unit, vals, step = d
        k = R.randrange(len(cs))
        v = vals[k]
        if halb and v % step == 0:
            return None
        pic = saeulen(list(zip(cs, vals)), unit, label="Säulendiagramm: " + t, step=step)
        w = [v // step, v + step // 2 if halb else v + step, v - step // 2 if halb else v - step, (v // step + 1) * step if halb else v * 10]
        unitw = "km" if unit == "km" else unit
        q = "%s: Wie viele %s waren es %s?" % (t, unitw if unit != "km" else "Kilometer", wann(cs[k]))
        return mcq(pic + q, num(v), [num(x) for x in w if x != v and x > 0],
                   ("Eine Linie bedeutet %s. Die Säule endet genau in der Mitte zwischen zwei Linien: <b>%s</b>." if halb else
                    "Eine Linie bedeutet %s. Die Säule reicht bis <b>%s</b>.") % (num(step), num(v)))
    return mk


def vergleichen():
    d = pick_topic()
    if not d:
        return None
    t, cs, unit, vals, step = d
    pic = saeulen(list(zip(cs, vals)), unit, label="Säulendiagramm: " + t, step=step)
    kind = R.choice(["diff", "sum", "max", "doppelt"])
    i, j = R.sample(range(len(cs)), 2)
    if kind == "diff":
        a, b = max(vals[i], vals[j]), min(vals[i], vals[j])
        ci, cj = (cs[i], cs[j]) if vals[i] > vals[j] else (cs[j], cs[i])
        r = a - b
        return mcq(pic + "%s: Wie viel mehr waren es %s als %s?" % (t, wann(ci), wann(cj)), num(r), [num(x) for x in (a + b, r + step, a, r // step if r // step > 1 else r * 2) if x != r],
                   "%s − %s = <b>%s</b>." % (num(a), num(b), num(r)))
    if kind == "sum":
        r = sum(vals)
        return mcq(pic + "%s: Wie viele %s waren es insgesamt?" % (t, unit if unit != "km" else "Kilometer"), num(r),
                   [num(x) for x in (r - vals[0], r + step, max(vals) * len(vals), r - step) if x != r],
                   "Addiere alle Säulen: %s = <b>%s</b>." % (" + ".join(num(v) for v in vals), num(r)))
    if kind == "max":
        k = vals.index(max(vals))
        m = vals.index(min(vals))
        r = vals[k] - vals[m]
        return mcq(pic + "%s: Wie groß ist der Unterschied zwischen dem höchsten und dem niedrigsten Wert?" % t, num(r),
                   [num(x) for x in (vals[k], vals[k] + vals[m], r + step, r - step) if x != r and x > 0],
                   "Höchster Wert %s, niedrigster Wert %s: %s − %s = <b>%s</b>." % (num(vals[k]), num(vals[m]), num(vals[k]), num(vals[m]), num(r)))
    pairs = [(a, b) for a in range(len(cs)) for b in range(len(cs)) if a != b and vals[a] == 2 * vals[b]]
    if not pairs:
        return None
    a, b = R.choice(pairs)
    return mcq(pic + "%s: Wann waren es doppelt so viele wie %s?" % (t, wann(cs[b])), cs[a], [c for c in cs if c != cs[a]][:3],
               "%s ist das Doppelte von %s: <b>%s</b>." % (num(vals[a]), num(vals[b]), cs[a]))


STAEDTE = [("Hamburg", 1892000), ("München", 1512000), ("Köln", 1084000), ("Frankfurt", 773000), ("Stuttgart", 633000),
           ("Düsseldorf", 629000), ("Leipzig", 616000), ("Dortmund", 595000), ("Essen", 584000), ("Bremen", 569000),
           ("Dresden", 563000), ("Hannover", 548000), ("Nürnberg", 526000)]
ENTF = {("Berlin", "Hamburg"): 289, ("Berlin", "München"): 585, ("Berlin", "Köln"): 574, ("Hamburg", "München"): 791, ("Hamburg", "Köln"): 426,
        ("München", "Köln"): 575, ("Berlin", "Leipzig"): 190, ("Hamburg", "Leipzig"): 395, ("München", "Leipzig"): 430, ("Köln", "Leipzig"): 498}


def tabelle():
    kind = R.choice(["entf", "entf", "lauf", "lauf"])
    if kind == "entf":
        cities = ["Berlin", "Hamburg", "München", "Köln", "Leipzig"]
        cs = R.sample(cities, 4)

        def d(a, b):
            return ENTF.get((a, b)) or ENTF.get((b, a))
        rows = [[a] + [("–" if a == b else "%d km" % d(a, b)) for b in cs] for a in cs]
        html = table([""] + cs, rows)
        a, b, c = R.sample(cs, 3)
        sub = R.choice(["hin", "rund"])
        if sub == "hin":
            r = d(a, b)
            return mcq("Entfernungstabelle (Straßenkilometer, gerundet): Wie weit ist es von %s nach %s?" % (a, b) + html, "%d%skm" % (r, NB),
                       ["%d%skm" % (x, NB) for x in (d(a, c), d(b, c), r * 2) if x != r],
                       "Suche die Zeile %s und die Spalte %s: <b>%d km</b>." % (a, b, r))
        r = d(a, b) + d(b, c)
        return mcq("Entfernungstabelle (Straßenkilometer, gerundet): Familie %s fährt von %s über %s nach %s. Wie weit ist die Fahrt?" % (R.choice(["Becker", "Wagner", "Schulz", "Yilmaz", "Fischer"]), a, b, c) + html,
                   "%d%skm" % (r, NB), ["%d%skm" % (x, NB) for x in (d(a, c), d(a, b) + d(a, c), r + 100) if x != r],
                   "%d km + %d km = <b>%d km</b>." % (d(a, b), d(b, c), r))
    names = R.sample(["Emma", "Ben", "Mia", "Paul", "Lena", "Finn", "Ida", "Jonas"], 4)
    times = R.sample(range(118, 196), 4)

    def mmss(s):
        return "%d min %02d s" % divmod(s, 60) if s >= 60 else "%d s" % s
    rows = [[n, mmss(t)] for n, t in zip(names, times)]
    html = table(["Kind", "Zeit für 800 m"], rows)
    sub = R.choice(["schnell", "diff"])
    if sub == "schnell":
        k = times.index(min(times))
        return mcq("Beim Sportfest laufen vier Kinder 800 m. Wer war am schnellsten?" + html, names[k],
                   [names[times.index(max(times))]] + [n for i, n in enumerate(names) if i not in (k, times.index(max(times)))],
                   "Am schnellsten ist, wer die <b>kürzeste</b> Zeit braucht: <b>%s</b> (%s)." % (names[k], mmss(times[k])))
    i, j = R.sample(range(4), 2)
    if times[i] > times[j]:
        i, j = j, i
    r = times[j] - times[i]
    return mcq("Beim Sportfest laufen vier Kinder 800 m. Wie viele Sekunden war %s schneller als %s?" % (names[i], names[j]) + html, "%d%ss" % (r, NB),
               ["%d%ss" % (x, NB) for x in (r + 40, abs(r - 40) or r + 20, times[j] + times[i] - 120) if x != r and x > 0],
               "%s = %d s, %s = %d s. %d − %d = <b>%d s</b>." % (mmss(times[j]), times[j], mmss(times[i]), times[i], times[j], times[i], r))


def linien_svg(xs, ys, step, unit_label, label):
    lo = min(0, (min(ys) // step) * step)
    hi = ((max(ys) + step - 1) // step) * step
    H, x0, y0 = 160, 46, 20
    dx = 52
    W = x0 + dx * (len(xs) - 1) + 40
    Y = lambda v: y0 + H - (v - lo) / float(hi - lo) * H
    s = []
    for v in range(lo, hi + 1, step):
        s.append(line(x0, Y(v), W - 10, Y(v), "#cccccc", 1))
        s.append(text(x0 - 8, Y(v) + 5, ("−%d" % -v) if v < 0 else str(v), 12, anchor="end", weight=400))
    s.append(line(x0, y0, x0, y0 + H, INK, 2))
    s.append(line(x0, y0 + H, W - 10, y0 + H, INK, 2))
    pts = []
    for i, (x, v) in enumerate(zip(xs, ys)):
        X = x0 + 20 + i * dx
        pts.append("%.0f,%.1f" % (X, Y(v)))
        s.append(text(X, y0 + H + 18, x, 12, weight=600))
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.5'/>" % (" ".join(pts), BLUE))
    for p in pts:
        a, b = p.split(",")
        s.append("<circle cx='%s' cy='%s' r='4' fill='%s'/>" % (a, b, BLUE))
    s.append(text(8, y0 - 6, unit_label, 12, anchor="start", weight=600))
    return wrap(W, y0 + H + 28, "".join(s), label, lg=True)


def linien():
    hours = ["6 Uhr", "8 Uhr", "10 Uhr", "12 Uhr", "14 Uhr", "16 Uhr", "18 Uhr"]
    season = R.choice(["Sommer", "Frühling"])
    base = R.randint(10, 16) if season == "Sommer" else R.randint(4, 9)
    rise = [0, 3, 6, 9, 10, 8, 5]
    ys = [base + r + R.choice([-1, 0, 1]) for r in rise]
    if len(set(ys)) < 6:
        return None
    pic = linien_svg(hours, ys, 2, "°C", "Liniendiagramm: Temperatur an einem Tag im %s" % season)
    kind = R.choice(["wert", "max", "diff", "steigt"])
    pre = pic + "Das Liniendiagramm zeigt die Temperatur an einem Tag im %s. " % season
    if kind == "wert":
        k = R.randrange(7)
        v = ys[k]
        return mcq(pre + "Wie warm war es um %s?" % hours[k], "%d%s°C" % (v, NB), ["%d%s°C" % (x, NB) for x in (v + 1, v - 1, v + 2, ys[(k + 1) % 7]) if x != v][:3],
                   "Gehe von %s nach oben bis zum Punkt und lies links ab: <b>%d °C</b>." % (hours[k], v))
    if kind == "max":
        k = ys.index(max(ys))
        if ys.count(max(ys)) > 1:
            return None
        return mcq(pre + "Um wie viel Uhr war es am wärmsten?", hours[k], [h for i, h in enumerate(hours) if i != k and abs(i - k) <= 3][:3],
                   "Der höchste Punkt liegt bei <b>%s</b> (%d °C)." % (hours[k], ys[k]))
    if kind == "diff":
        i, j = sorted(R.sample(range(7), 2))
        r = abs(ys[j] - ys[i])
        if r == 0:
            return None
        return mcq(pre + "Wie groß ist der Temperaturunterschied zwischen %s und %s?" % (hours[i], hours[j]), "%d%s°C" % (r, NB),
                   ["%d%s°C" % (x, NB) for x in (ys[i] + ys[j], r + 2, r + 1 if r > 1 else r + 3, max(ys[i], ys[j])) if x != r][:3],
                   "%d °C und %d °C: Unterschied <b>%d °C</b>." % (ys[i], ys[j], r))
    i = R.randrange(6)
    up = ys[i + 1] > ys[i]
    ans = "Die Temperatur steigt." if up else "Die Temperatur sinkt." if ys[i + 1] < ys[i] else None
    if not ans:
        return None
    return mcq(pre + "Was passiert zwischen %s und %s?" % (hours[i], hours[i + 1]), ans,
               [v for v in ("Die Temperatur steigt.", "Die Temperatur sinkt.") if v != ans] + ["Die Temperatur bleibt gleich.", "Das kann man nicht ablesen."],
               "Die Linie geht %s: <b>%s</b>" % ("nach oben" if up else "nach unten", ans))


UMFR = [("Lieblingssport", ["Fußball", "Schwimmen", "Turnen", "Reiten", "Basketball"]),
        ("Schulweg", ["zu Fuß", "Fahrrad", "Bus", "Auto", "Roller"]),
        ("Lieblingsobst", ["Äpfel", "Bananen", "Erdbeeren", "Trauben", "Kirschen"]),
        ("Lieblings-AG", ["Chor", "Schach", "Theater", "Garten", "Computer"])]


def umfrage():
    t, cats = R.choice(UMFR)
    vals = R.sample(range(8, 60), 4)
    cs = R.sample(cats, 4)
    tot = sum(vals)
    schulen = R.choice(["Die Grundschule am See", "Die Lindenschule", "Die Grundschule Nord", "Die Schillerschule"])
    html = table([t, "Anzahl der Kinder"], [[c, str(v)] for c, v in zip(cs, vals)])
    kind = R.choice(["tot", "mehr", "rang", "rest"])
    pre = "%s hat alle Kinder der 3. und 4. Klassen nach dem Thema „%s“ gefragt." % (schulen, t) + html
    if kind == "tot":
        return mcq(pre + "Wie viele Kinder wurden befragt?", str(tot), [str(x) for x in (tot - vals[0], tot + 10, max(vals) * 4) if x != tot],
                   "%s = <b>%d</b>." % (" + ".join(map(str, vals)), tot))
    if kind == "mehr":
        i, j = R.sample(range(4), 2)
        if vals[i] < vals[j]:
            i, j = j, i
        r = vals[i] - vals[j]
        return mcq(pre + "Wie viele Kinder mehr haben „%s“ gewählt als „%s“?" % (cs[i], cs[j]), str(r), [str(x) for x in (vals[i] + vals[j], r + 10, r - 1 if r > 1 else r + 2) if x != r],
                   "%d − %d = <b>%d</b>." % (vals[i], vals[j], r))
    if kind == "rang":
        o = sorted(range(4), key=lambda k: -vals[k])
        return mcq(pre + "Was liegt auf Platz 2?", cs[o[1]], [cs[o[0]], cs[o[2]], cs[o[3]]],
                   "Ordne der Größe nach: %s. Platz 2: <b>%s</b>." % (", ".join("%s (%d)" % (cs[k], vals[k]) for k in o), cs[o[1]]))
    k = R.randrange(4)
    r = tot - vals[k]
    return mcq(pre + "Wie viele Kinder haben <b>nicht</b> „%s“ gewählt?" % cs[k], str(r), [str(x) for x in (vals[k], tot, r + 10) if x != r],
               "Alle Kinder: %d. %d − %d = <b>%d</b>." % (tot, tot, vals[k], r))


def main():
    seen = set()
    sets = [
        ("Säulendiagramme ablesen", mix(R, seen, [(ablesen(False), 20)])),
        ("Werte zwischen den Linien", mix(R, seen, [(ablesen(True), 20)])),
        ("Vergleichen und rechnen", mix(R, seen, [(vergleichen, 20)])),
        ("Tabellen und Liniendiagramme", mix(R, seen, [(tabelle, 10), (linien, 10)])),
        ("Umfragen auswerten", mix(R, seen, [(umfrage, 20)])),
    ]
    body = lesson(
        ["Schau zuerst auf die <b>Skala</b>: Wie viel bedeutet ein Abstand zwischen zwei Linien? Oft sind es 50, 100 oder 500.",
         "Endet eine Säule zwischen zwei Linien, liegt der Wert dazwischen. In der Mitte ist es die Hälfte des Abstands.",
         "Ein <b>Liniendiagramm</b> zeigt, wie sich etwas verändert, zum Beispiel die Temperatur im Laufe eines Tages.",
         "In einer Tabelle findest du einen Wert, wo sich Zeile und Spalte treffen."],
        [example("Skala in 100er-Schritten, Säule endet in der Mitte zwischen 300 und 400", ["Hälfte von 100 = 50", "300 + 50"], "350"),
         example("Montag 450 Bücher, Dienstag 300 Bücher", ["Unterschied: 450 − 300"], "150 Bücher mehr")],
        [["Jede Linie als 1 zählen", "Erst die Skala lesen: 1 Linie = 50, 100, …"],
         ["Den Wert der nächsten Linie nehmen", "Bei Säulen zwischen den Linien die Mitte beachten"],
         ["„Wie viel mehr?“ mit plus rechnen", "Unterschied = größerer Wert − kleinerer Wert"]])
    faq = [
        {"q": "Welche Diagramme lernt man in Klasse 4?", "a": "Vor allem Säulen- und Balkendiagramme, Tabellen und Strichlisten. Viele Schulen zeigen auch einfache Liniendiagramme, etwa für die Temperatur."},
        {"q": "Was ist eine Skala?", "a": "Die Zahlen an der senkrechten Achse. Sie zeigen, wie viel ein Abstand zwischen zwei Linien bedeutet."},
        {"q": "Wann nimmt man ein Liniendiagramm?", "a": "Wenn man zeigen will, wie sich ein Wert über die Zeit verändert, zum Beispiel die Temperatur oder die Größe einer Pflanze."},
        {"q": "Wie liest man eine Entfernungstabelle?", "a": "Man sucht die Zeile mit dem einen Ort und die Spalte mit dem anderen Ort. Wo sie sich treffen, steht die Entfernung."},
    ]
    make_unit(R, "daten-und-diagramme", "D",
              "Die Schülerinnen und Schüler entnehmen Säulendiagrammen mit verschiedenen Skalen, Tabellen und Liniendiagrammen Daten, vergleichen und berechnen damit und werten Umfragen aus (Zusammenfassung).",
              "Daten und Diagramme: Säulen, Tabellen und Liniendiagramme",
              "Daten und Diagramme Klasse 4 – Arbeitsblätter mit Lösungen",
              "Daten und Diagramme",
              "Daten und Diagramme für Klasse 4: Säulendiagramme mit großen Zahlen ablesen, Werte zwischen den Linien, Tabellen, Liniendiagramme und Umfragen. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Erst die Skala lesen, dann den Wert.",
              "1 Linie kann 50, 100 oder 500 bedeuten.",
              body, faq, sets, 18, grade="klasse-4")


if __name__ == "__main__":
    main()
