# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 3: Gewichte – Gramm und Kilogramm（Leitidee Größen und Messen）
  python3 tools/gen_de_mathe_k3_gewichte.py
Umwandeln (1 kg = 1000 g), Balkenwaage ablesen, vergleichen und ordnen, rechnen, schätzen und Sachaufgaben.
Fehler: 1 kg = 100 g, 2 kg 50 g = 2500 g, verschiedene Einheiten direkt vergleichen (900 g > 1 kg), unpassende Einheit beim Schätzen.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, wrap, NB, table, MAL
from ws_common import line, text, INK, GREEN, FILL

R = random.Random(49013)
KIDS = Kids(R)


def u(v, e):
    return "%s%s%s" % (num(v), NB, e)


def kg_g(g):
    a, b = divmod(g, 1000)
    if a and b:
        return "%d%skg %d%sg" % (a, NB, b, NB)
    return u(a, "kg") if a else u(b, "g")


def waage(left_label, weights):
    """Balkenwaage im Gleichgewicht: links ein Gegenstand, rechts Gewichtsstücke"""
    s = ["<path d='M150 150 L135 168 H165 Z' fill='%s'/>" % INK, line(150, 40, 150, 150, INK, 4), line(40, 40, 260, 40, INK, 4),
         line(55, 40, 55, 70, INK, 1.5), line(245, 40, 245, 70, INK, 1.5),
         "<path d='M20 70 H90 L80 82 H30 Z' fill='%s' stroke='%s'/>" % (FILL, GREEN),
         "<path d='M210 70 H280 L270 82 H220 Z' fill='%s' stroke='%s'/>" % (FILL, GREEN),
         "<rect x='31' y='42' width='48' height='27' rx='3' fill='#e9c27f' stroke='%s'/>" % INK, text(55, 61, left_label, 12)]
    x = 213
    for wv in weights:
        lab = "%d kg" % (wv // 1000) if wv >= 1000 else "%d g" % wv
        wd = 26 if wv >= 500 else 22 if wv >= 100 else 18
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='2' fill='#9aa5ad' stroke='%s'/>" % (x, 70 - wd, wd, wd, INK))
        s.append(text(x + wd / 2.0, 70 - wd - 3, lab.replace(" ", NB), 9))
        x += wd + 2
    return wrap(max(300, x + 10), 172, "".join(s), "Balkenwaage im Gleichgewicht", lg=True)


def umwandeln():
    kind = R.choice(["kg-g", "g-kg", "gemischt", "teile", "rueck"])
    if kind == "kg-g":
        v = R.randint(2, 9)
        return mcq("%s = ? g" % u(v, "kg"), u(v * 1000, "g"), [u(x, "g") for x in (v * 100, v * 10, v * 10000)],
                   "1 kg = 1000 g. %d kg = <b>%s g</b>." % (v, num(v * 1000)))
    if kind == "g-kg":
        v = R.randint(2, 9)
        return mcq("%s = ? kg" % u(v * 1000, "g"), u(v, "kg"), [u(x, "kg") for x in (v * 10, v * 100, v * 1000)],
                   "1000 g = 1 kg. %s g = <b>%d kg</b>." % (num(v * 1000), v))
    if kind == "gemischt":
        a = R.randint(1, 5)
        b = R.choice([R.randint(1, 9) * 100, R.randint(1, 9) * 50, R.randint(1, 99)])
        tot = a * 1000 + b
        w = [a * 1000 + b * 10 if b < 100 else a * 100 + b, int("%d%d" % (a, b)), tot + 100]
        return mcq("%d%skg %d%sg = ? g" % (a, NB, b, NB), u(tot, "g"), [u(x, "g") for x in w if x != tot],
                   "%d kg = %s g, dazu %d g: <b>%s g</b>." % (a, num(a * 1000), b, num(tot)))
    if kind == "teile":
        f, g = R.choice([("ein halbes Kilogramm", 500), ("ein viertel Kilogramm", 250), ("ein dreiviertel Kilogramm", 750)])
        return mcq("Wie viel Gramm sind %s?" % f, u(g, "g"), [u(x, "g") for x in (50, 5000, 200, 25, 75) if x != g][:3],
                   "1 kg = 1000 g. %s sind <b>%d g</b>." % (f[0].upper() + f[1:], g))
    tot = R.randint(11, 59) * 100 + R.choice([0, 0, 50])
    if tot % 1000 == 0:
        return None
    a, b = divmod(tot, 1000)
    w = ["%d%skg %d%sg" % (a, NB, b // 10, NB), "%d%skg %d%sg" % (tot // 100, NB, tot % 100, NB), "%d%skg %d%sg" % (a + 1, NB, b, NB)]
    return mcq("%s = ? kg ? g" % u(tot, "g"), kg_g(tot), [x for x in w if x != kg_g(tot)],
               "1000 g = 1 kg. %s g = <b>%s</b>." % (num(tot), kg_g(tot)))


THINGS = [("Paket", "das Paket"), ("Mehl", "das Mehl"), ("Käse", "der Käse"), ("Kürbis", "der Kürbis"), ("Brot", "das Brot"), ("Zucker", "der Zucker")]


def ablesen():
    pool = [1000, 500, 200, 100, 50, 20, 10]
    n = R.randint(2, 4)
    ws = sorted([R.choice(pool) for _ in range(n)], reverse=True)
    if ws.count(1000) > 1:
        return None
    tot = sum(ws)
    thing, best = R.choice(THINGS)
    w = [tot + 100, tot - 50 if tot > 50 else tot + 50, tot + max(ws), sum(ws[:-1])]
    return mcq(waage(thing, ws) + "Die Waage ist im Gleichgewicht. Wie schwer ist %s?" % best, kg_g(tot),
               [kg_g(x) for x in w if x > 0 and x != tot],
               "Rechts liegen %s. Zusammen <b>%s</b>." % (" + ".join(("%d kg" % (x // 1000)) if x >= 1000 else "%d g" % x for x in ws), kg_g(tot)))


def vergleichen():
    kind = R.choice(["zwei", "zwei", "ordnen"])
    if kind == "zwei":
        a = R.randint(1, 4)
        b = a * 1000 + R.choice([-300, -100, -50, 200, 500])
        ka = u(a, "kg")
        kb = u(b, "g")
        heavier = ka if a * 1000 > b else kb
        return mcq("Was ist schwerer: %s oder %s?" % (ka, kb), heavier, [kb if heavier == ka else ka, "Beide sind gleich schwer", "Das kann man nicht vergleichen"],
                   "Gleiche Einheit: %d kg = %s g. Also ist <b>%s</b> schwerer." % (a, num(a * 1000), heavier))
    vals = R.sample([250, 500, 750, 900, 800, 600], 2) + [R.choice([1000, 2000, 1200, 1500])]
    R.shuffle(vals)
    txt = [kg_g(v) if v >= 1000 else u(v, "g") for v in vals]
    order = sorted(range(3), key=lambda i: vals[i])
    ans = " &lt; ".join(txt[i] for i in order)
    w = [" &lt; ".join(txt[i] for i in order[::-1]), " &lt; ".join(txt[i] for i in sorted(range(3), key=lambda i: int(txt[i].split(NB)[0].replace(NB, "")))),
         " &lt; ".join(txt[i] for i in [order[1], order[0], order[2]])]
    return mcq("Ordne vom leichtesten zum schwersten: %s" % ", ".join(txt), ans, [x for x in w if x != ans],
               "Rechne alles in Gramm um: %s. Richtig: <b>%s</b>." % (", ".join(u(v, "g") for v in vals), ans))


def rechnen():
    kind = R.choice(["minus1kg", "plus", "mal"])
    if kind == "minus1kg":
        c = R.randint(1, 19) * 50
        r = 1000 - c
        return mcq("1%skg − %s = ?" % (NB, u(c, "g")), u(r, "g"), [u(x, "g") for x in (100 - c // 10 if c < 1000 else 0, 1000 + c, r + 100, c) if x > 0 and x != r],
                   "1 kg = 1000 g. 1000 g − %d g = <b>%d g</b>." % (c, r))
    if kind == "plus":
        a, b = R.randint(2, 9) * 50, R.randint(2, 9) * 50
        r = a + b
        return mcq("%s + %s = ?" % (u(a, "g"), u(b, "g")), kg_g(r), [kg_g(x) for x in (r + 100, r - 50, abs(a - b) or r + 50) if x != r],
                   "%d g + %d g = %s g = <b>%s</b>." % (a, b, num(r), kg_g(r)) if r >= 1000 else "%d g + %d g = <b>%d g</b>." % (a, b, r))
    n = R.randint(2, 6)
    g = R.choice([125, 150, 200, 250])
    r = n * g
    return mcq("%d Packungen zu je %s. Wie schwer sind sie zusammen?" % (n, u(g, "g")), kg_g(r),
               [kg_g(x) for x in (n + g, r + g, r - g) if x != r and x > 0], "%d %s %d g = %d g = <b>%s</b>." % (n, MAL, g, r, kg_g(r)))


SCHAETZ = [
    ("Wie schwer ist eine Tafel Schokolade ungefähr?", 100, "g", "kg"),
    ("Wie schwer ist ein Apfel ungefähr?", 150, "g", "kg"),
    ("Wie schwer ist ein Kind in der 3. Klasse ungefähr?", 30, "kg", "g"),
    ("Wie schwer ist eine Packung Mehl ungefähr?", 1, "kg", "g"),
    ("Wie schwer ist ein Fahrrad ungefähr?", 15, "kg", "g"),
    ("Wie schwer ist ein Blatt Papier ungefähr?", 5, "g", "kg"),
    ("Wie schwer ist ein voller Schulranzen ungefähr?", 5, "kg", "g"),
    ("Wie schwer ist ein Ei ungefähr?", 60, "g", "kg"),
]


def sache():
    kind = R.choice(["schaetz", "kuchen", "einkauf", "ranzen"])
    p = KIDS.next()
    if kind == "schaetz":
        qq, v, e, o = R.choice(SCHAETZ)
        w = [u(v, o), u(v * 10, e), u(v * 100 if e == "g" else max(v // 10, 1) if v >= 10 else v * 100, e)]
        return mcq(qq, u(v, e), [x for x in w if x != u(v, e)],
                   "Vergleiche mit Bekanntem: Eine Tafel Schokolade wiegt 100 g, eine Packung Mehl 1 kg. Passend ist etwa <b>%s</b>." % u(v, e))
    if kind == "kuchen":
        mehl = R.choice([250, 300, 350, 400])
        zucker = R.choice([100, 150, 200])
        butter = R.choice([125, 150, 200, 250])
        r = mehl + zucker + butter
        q = "Für einen Kuchen braucht man %s Mehl, %s Zucker und %s Butter. Wie viel ist das zusammen?" % (u(mehl, "g"), u(zucker, "g"), u(butter, "g"))
        return mcq(q, u(r, "g"), [u(x, "g") for x in (r + 100, r - 50, mehl + zucker) if x != r], "%d g + %d g + %d g = <b>%d g</b>." % (mehl, zucker, butter, r))
    if kind == "einkauf":
        a = R.choice([500, 750, 1000, 1500, 2000])
        b = R.choice([250, 500, 400])
        c = R.choice([1000, 2000])
        r = a + b + c
        q = "%s kauft %s Kartoffeln, %s Tomaten und %s Äpfel. Wie schwer ist der Einkauf?" % (p[0], kg_g(a), u(b, "g"), kg_g(c))
        return mcq(q, kg_g(r), [kg_g(x) for x in (r + 500, r - 250, a + b) if x != r and x > 0],
                   "Alles in Gramm: %d g + %d g + %d g = %s g = <b>%s</b>." % (a, b, c, num(r), kg_g(r)))
    full = R.randint(4, 7) * 1000 + R.choice([0, 200, 500])
    book = R.choice([300, 400, 500, 600])
    n = R.randint(2, 4)
    r = full - n * book
    q = "Der Schulranzen von %s wiegt %s. %s nimmt %d Bücher zu je %s heraus. Wie schwer ist der Ranzen jetzt?" % (p[0], kg_g(full), p[1].capitalize(), n, u(book, "g"))
    return mcq(q, kg_g(r), [kg_g(x) for x in (full - book, full + n * book, r - 100) if x != r and x > 0],
               "%d %s %d g = %d g. %s g − %d g = %s g = <b>%s</b>." % (n, MAL, book, n * book, num(full), n * book, num(r), kg_g(r)))


def main():
    seen = set()
    sets = [
        ("Gramm und Kilogramm", mix(R, seen, [(umwandeln, 20)])),
        ("Die Waage ablesen", mix(R, seen, [(ablesen, 20)])),
        ("Vergleichen und ordnen", mix(R, seen, [(vergleichen, 20)])),
        ("Mit Gewichten rechnen", mix(R, seen, [(rechnen, 20)])),
        ("Schätzen und Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Gewichte misst du in Gramm (g) und Kilogramm (kg).",
         "1 kg = 1000 g. Ein halbes Kilogramm sind 500 g, ein viertel Kilogramm 250 g.",
         "Bei einer <b>Balkenwaage im Gleichgewicht</b> sind beide Seiten gleich schwer.",
         "Zum Vergleichen und Rechnen bringst du alles in <b>dieselbe Einheit</b>."],
        [example("2 kg 50 g = ? g", ["2 kg = 2000 g", "2000 g + 50 g = 2050 g"], "2050 g"),
         example("1 kg − 350 g", ["1 kg = 1000 g", "1000 g − 350 g = 650 g"], "650 g")],
        [["1 kg = 100 g", "1 kg = 1000 g"],
         ["2 kg 50 g = 2500 g", "2000 g + 50 g = 2050 g"],
         ["900 g ist mehr als 1 kg, weil 900 größer als 1 ist", "Erst umrechnen: 1 kg = 1000 g &gt; 900 g"]],
        extra=table(["Gegenstand", "ungefähr"], [["Blatt Papier", "5 g"], ["Tafel Schokolade", "100 g"], ["Packung Mehl", "1 kg"], ["Kind in Klasse 3", "30 kg"]]))
    faq = [
        {"q": "Sagt man Gewicht oder Masse?", "a": "In der Grundschule sagt man meistens Gewicht. In der Physik heißt die Größe Masse, die Einheiten g und kg sind dieselben."},
        {"q": "Welche Gewichtseinheiten lernt man in Klasse 3?", "a": "Gramm und Kilogramm mit 1 kg = 1000 g. Die Tonne (1 t = 1000 kg) kommt meist in Klasse 4."},
        {"q": "Wie üben Kinder das Schätzen von Gewichten?", "a": "Mit Vergleichsgegenständen: Eine Tafel Schokolade wiegt 100 g, eine Packung Mehl oder Zucker 1 kg."},
        {"q": "Wie liest man eine Balkenwaage ab?", "a": "Ist die Waage im Gleichgewicht, wiegt der Gegenstand so viel wie alle Gewichtsstücke auf der anderen Seite zusammen."},
    ]
    make_unit(R, "gewichte", "G",
              "Die Schülerinnen und Schüler wiegen und vergleichen Gewichte, rechnen mit Gramm und Kilogramm, wandeln Einheiten um und schätzen mit Stützpunktvorstellungen (Zusammenfassung).",
              "Gewichte: Gramm und Kilogramm",
              "Gewichte Klasse 3 – Gramm und Kilogramm Arbeitsblätter mit Lösungen",
              "Gewichte",
              "Gewichte für Klasse 3: Gramm und Kilogramm umrechnen, Waage ablesen, vergleichen, rechnen, schätzen und Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "1 kg = 1000 g",
              "Ein halbes Kilogramm sind 500 g, ein viertel Kilogramm 250 g.",
              body, faq, sets, 13)


if __name__ == "__main__":
    main()
