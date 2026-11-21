# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 5: Längen, Massen und Zeit – Größen umrechnen（Leitidee Größen und Messen, Sek I）
  python3 tools/gen_de_mathe_k5_laengen_massen_und_zeit.py
Längen (mm, cm, dm, m, km), Massen (mg, g, kg, t), Zeit (s, min, h, d), Kommaschreibweise, Sachaufgaben mit Größen.
Gemeinsame Aufgaben aus tools/de_k4_groessen.py (lesen, kleiner, groesser, rechnen).
Fehler: falsche Umrechnungszahl (1 m = 10 cm), bei der Zeit mit 100 statt 60 gerechnet, Komma an der falschen Stelle.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, Kids, MAL, table, NB
import de_k4_groessen as g

R = random.Random(49510)
KIDS = Kids(R)
LAENGE = [(10, "cm", "mm"), (10, "dm", "cm"), (100, "m", "cm"), (1000, "km", "m"), (1000, "m", "mm"), (10, "m", "dm")]
MASSE = [(1000, "kg", "g"), (1000, "t", "kg"), (1000, "g", "mg")]


def paar(lst):
    def mk():
        f, big, small = R.choice(lst)
        fun = R.choice([g.lesen, g.kleiner, g.groesser, g.rechnen])
        return fun(R, f, big, small)()
    return mk


def zeit():
    kind = R.choice(["h_min", "min_s", "tag_h", "min_h", "woche", "gemischt"])
    if kind == "h_min":
        h, m = R.randint(1, 5), R.randint(5, 55)
        t = 60 * h + m
        return mcq("%d h %d min = ? min" % (h, m), "%d min" % t, ["%d min" % x for x in (100 * h + m, h * 10 + m, t + 60)], "1 h = 60 min. %d %s 60 + %d = <b>%d min</b>." % (h, MAL, m, t))
    if kind == "min_s":
        m, s = R.randint(1, 9), R.randint(5, 55)
        t = 60 * m + s
        return mcq("%d min %d s = ? s" % (m, s), "%d s" % t, ["%d s" % x for x in (100 * m + s, m * 10 + s, t + 60)], "1 min = 60 s. %d %s 60 + %d = <b>%d s</b>." % (m, MAL, s, t))
    if kind == "tag_h":
        d = R.randint(2, 7)
        return mcq("%d Tage = ? h" % d, "%d h" % (24 * d), ["%d h" % x for x in (12 * d, 60 * d, 10 * d)], "1 Tag = 24 h. %d %s 24 = <b>%d h</b>." % (d, MAL, 24 * d))
    if kind == "min_h":
        t = R.randint(65, 299)
        if t % 60 == 0:
            return None
        h, m = divmod(t, 60)
        return mcq("%d min = ? h ? min" % t, "%d h %d min" % (h, m), ["%d h %d min" % (t // 100, t % 100), "%d h %d min" % (h + 1, m), "%d h %d min" % (h, m + 10) if m + 10 < 60 else "%d h %d min" % (h - 1 if h > 1 else h + 2, m)],
                   "%d min = %d %s 60 min + %d min = <b>%d h %d min</b>." % (t, h, MAL, m, h, m))
    if kind == "woche":
        w = R.randint(2, 9)
        return mcq("%d Wochen = ? Tage" % w, "%d Tage" % (7 * w), ["%d Tage" % x for x in (5 * w, 10 * w, 7 * w + 7)], "1 Woche = 7 Tage. %d %s 7 = <b>%d Tage</b>." % (w, MAL, 7 * w))
    a, b = R.randint(15, 59), R.randint(15, 59)
    s = a + b
    h, m = divmod(s, 60)
    ans = ("%d h %d min" % (h, m)) if h and m else ("1 h" if h else "%d min" % m)
    return mcq("%d min + %d min = ?" % (a, b), ans, ["%d min" % s if h else "%d min" % (s + 10), "%d h %d min" % (s // 100, s % 100) if s >= 100 else "%d h %d min" % (1, s - 50 if s > 50 else s), "%d h %d min" % (h + 1, m)],
               ("%d + %d = %d min = <b>%s</b> (60 min = 1 h)." % (a, b, s, ans)) if h else "%d + %d = <b>%d min</b>." % (a, b, s))


def sache():
    kind = R.choice(["lkw", "staffel", "film", "rezept", "bruecke", "zug"])
    p = KIDS.next()
    if kind == "lkw":
        t = R.randint(5, 18)
        k, kg = R.randint(20, 80), R.randint(50, 200)
        tot = k * kg
        if tot >= t * 1000:
            return None
        return mcq("Ein Lastwagen darf %d t laden. Er transportiert %d Kisten zu je %d kg. Wie viel Kilogramm kann er noch laden?" % (t, k, kg),
                   "%s kg" % num(t * 1000 - tot), ["%s kg" % num(x) for x in (t * 100 - tot if t * 100 > tot else t * 1000 - tot + 100, tot, t * 1000 - tot + 1000)],
                   "%d t = %s kg. %d %s %d kg = %s kg. %s − %s = <b>%s kg</b>." % (t, num(t * 1000), k, MAL, kg, num(tot), num(t * 1000), num(tot), num(t * 1000 - tot)))
    if kind == "staffel":
        n, m = R.randint(4, 8), R.choice([50, 75, 100, 200, 400])
        return mcq("Bei einer Staffel laufen %d Kinder je %d m. Wie lang ist die Staffel insgesamt?" % (n, m), g.zwei(n * m, 1000, "km", "m") if n * m >= 1000 else "%d m" % (n * m),
                   [("%d m" % (n * m * 10)), "%d m" % (n + m), "%d km" % (n * m // 100) if n * m >= 100 else "%d m" % (n * m + m)],
                   "%d %s %d m = <b>%s</b>." % (n, MAL, m, g.zwei(n * m, 1000, "km", "m") if n * m >= 1000 else "%d m" % (n * m)))
    if kind == "film":
        h, m = R.randint(14, 19), R.choice([0, 15, 30, 45])
        d = R.choice([95, 105, 112, 128, 135, 150])
        e = h * 60 + m + d
        return mcq("Ein Film beginnt um %d:%02d Uhr und dauert %d min. Wann ist er zu Ende?" % (h, m, d), "%d:%02d Uhr" % divmod(e, 60),
                   ["%d:%02d Uhr" % ((h + d // 100), (m + d % 100) % 60), "%d:%02d Uhr" % divmod(e + 60, 60), "%d:%02d Uhr" % divmod(e - 10, 60)],
                   "%d min = %d h %d min. %d:%02d Uhr + %d h %d min = <b>%d:%02d Uhr</b>." % ((d, d // 60, d % 60, h, m, d // 60, d % 60) + divmod(e, 60)))
    if kind == "rezept":
        a, b, c = R.choice([250, 300, 400, 500]), R.choice([125, 150, 200, 250]), R.choice([50, 75, 100])
        s = a + b + c
        return mcq("Für einen Kuchen braucht man %d g Mehl, %d g Zucker und %d g Butter. Wie schwer ist das zusammen?" % (a, b, c), g.komma(s, 1000, "kg") if s >= 1000 else "%d g" % s,
                   ["%d kg" % s, g.komma(s, 100, "kg"), "%d g" % (s + 100)],
                   ("%d + %d + %d = %s g = <b>%s</b>." % (a, b, c, num(s), g.komma(s, 1000, "kg"))) if s >= 1000 else "%d + %d + %d = <b>%d g</b>." % (a, b, c, s))
    if kind == "bruecke":
        t = R.choice([3, 5, 7, 12])
        w = R.randint(2000, 9000) // 100 * 100
        ok = w <= t * 1000
        ans = "Ja, %s kg sind weniger als %d t." % (num(w), t) if ok else "Nein, %s kg sind mehr als %d t." % (num(w), t)
        return mcq("Eine Brücke darf mit höchstens %d t befahren werden. Ein Lieferwagen wiegt %s kg. Darf er über die Brücke fahren?" % (t, num(w)), ans,
                   ["Nein, %s kg sind mehr als %d t." % (num(w), t) if ok else "Ja, %s kg sind weniger als %d t." % (num(w), t), "Ja, weil %s größer als %d ist." % (num(w), t), "Das kann man nicht vergleichen."],
                   "%d t = %s kg. <b>%s</b>" % (t, num(t * 1000), ans))
    km = R.randint(120, 600)
    h = R.choice([2, 3, 4, 5])
    if km % h:
        return None
    return mcq("Ein Zug fährt in %d Stunden %d km. Wie viele Kilometer fährt er durchschnittlich in einer Stunde?" % (h, km), "%d km" % (km // h), ["%d km" % x for x in (km * h, km - h, km // h + 10)],
               "%d km : %d = <b>%d km</b>." % (km, h, km // h))


def main():
    seen = set()
    sets = [
        ("Längen umrechnen", mix(R, seen, [(paar(LAENGE), 20)])),
        ("Massen umrechnen", mix(R, seen, [(paar(MASSE), 20)])),
        ("Zeit umrechnen", mix(R, seen, [(zeit, 20)])),
        ("Gemischte Übungen", mix(R, seen, [(paar(LAENGE + MASSE), 14), (zeit, 6)])),
        ("Sachaufgaben mit Größen", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Eine <b>Größe</b> besteht aus Maßzahl und Einheit: 3 m, 250 g, 15 min.",
         "Längen: 1 km = 1000 m, 1 m = 10 dm = 100 cm, 1 cm = 10 mm. Massen: 1 t = 1000 kg, 1 kg = 1000 g, 1 g = 1000 mg.",
         "Zeit: 1 d = 24 h, 1 h = 60 min, 1 min = 60 s. Hier ist die Umrechnungszahl <b>nicht</b> 10, 100 oder 1000!",
         "Vor dem Rechnen oder Vergleichen bringst du alle Größen in <b>dieselbe Einheit</b>."],
        [example("3,25 kg in g", ["1 kg = 1000 g", "3 kg = 3000 g, 0,25 kg = 250 g"], "3250 g"),
         example("2 h 15 min in min", ["2 %s 60 = 120" % MAL, "120 + 15"], "135 min")],
        [["1 m = 10 cm", "1 m = 100 cm"],
         ["2 h 15 min = 215 min", "1 h = 60 min: 135 min"],
         ["3 m 5 cm = 3,5 m", "Zwei Stellen nach dem Komma: 3,05 m"]],
        extra=table(["Größe", "Umrechnung"], [["Länge", "km —1000→ m —10→ dm —10→ cm —10→ mm"], ["Masse", "t —1000→ kg —1000→ g —1000→ mg"], ["Zeit", "d —24→ h —60→ min —60→ s"]]))
    faq = [
        {"q": "Warum muss man beim Rechnen mit Größen umrechnen?", "a": "Man kann nur gleiche Einheiten addieren oder vergleichen. 2 m + 30 cm rechnet man als 200 cm + 30 cm = 230 cm."},
        {"q": "Warum ist das Umrechnen bei der Zeit schwieriger?", "a": "Weil die Zeit nicht im Zehnersystem gemessen wird: 1 h hat 60 min, ein Tag 24 h."},
        {"q": "Was bedeutet die Kommaschreibweise bei Größen?", "a": "3,25 kg heißt 3 kg und 250 g. Die Stellen nach dem Komma gehören zur kleineren Einheit."},
        {"q": "Welche Einheiten lernt man in Klasse 5 neu?", "a": "Oft den Dezimeter, das Milligramm und die Sekunde. Außerdem wird das Umrechnen mit Komma geübt."},
    ]
    make_unit(R, "laengen-massen-und-zeit", "G",
              "Die Schülerinnen und Schüler rechnen Längen, Massen und Zeitspannen in benachbarte Einheiten um, nutzen die Kommaschreibweise und lösen Sachaufgaben mit Größen (Zusammenfassung).",
              "Längen, Massen und Zeit umrechnen",
              "Größen umrechnen Klasse 5 – Arbeitsblätter mit Lösungen",
              "Größen umrechnen",
              "Größen für Klasse 5: Längen, Massen und Zeit umrechnen, Kommaschreibweise und Sachaufgaben mit Größen. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Erst in dieselbe Einheit umrechnen, dann rechnen.",
              "Bei der Zeit: 1 h = 60 min, nicht 100.",
              body, faq, sets, 10, grade="klasse-5")


if __name__ == "__main__":
    main()
