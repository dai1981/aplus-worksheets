# -*- coding: utf-8 -*-
"""Schweiz 3. Klasse: Geld – Franken und Rappen（Münzen 5, 10, 20 Rp., ½, 1, 2, 5 Fr.; Noten 10, 20, 50, 100, 200 Fr.）。Beträge immer auf 5 Rappen."""
import random
import de_common as D
import ch_common as C
from ch_common import chf, geld_svg

COINS = [500, 200, 100, 50, 20, 10, 5]
NOTES = [20000, 10000, 5000, 2000, 1000]


def build(seed, slug, grade, sort, codes, dom):
    R = random.Random(seed)
    K = D.Kids(R)

    def M(q, g, ws, e):
        ws = [w for w in dict.fromkeys(ws) if w != g][:3]
        if len(ws) < 3:
            return None
        return C.mcq(q, g, ws, e)

    def r5(lo, hi):
        return R.randint(lo // 5, hi // 5) * 5

    def zaehlen():
        n = R.randint(3, 6)
        pool = COINS if R.random() < 0.6 else NOTES[2:] + COINS
        items = [R.choice(pool) for _ in range(n)]
        t = sum(items)
        ws = [chf(x) for x in (t + 10, t - 10, t + 100, t - min(items), t + 50) if x > 0]
        return M(geld_svg(items) + "Wie viel Geld ist das?", chf(t), ws,
                 "Zähle vom grössten Wert aus: %s = <b>%s</b>." % (" + ".join(chf(x) for x in sorted(items, reverse=True)), chf(t)))

    def umwandeln():
        k = R.randint(0, 2)
        f = R.randint(1, 9)
        r = R.choice([5, 10, 20, 25, 30, 40, 45, 50, 60, 75, 80, 95])
        t = f * 100 + r
        if k == 0:
            g = "%d Rp." % t
            return M("Wie viele Rappen sind %s?" % chf(t), g, ["%d Rp." % x for x in (f * 10 + r, f * 1000 + r, t + 100, t - 10)],
                     "1 Fr. = 100 Rp. %d Fr. = %d Rp., dazu %d Rp.: <b>%d Rp.</b>" % (f, f * 100, r, t))
        if k == 1:
            return M("Schreibe als Franken: %d Rp. = ?" % t, chf(t), ["%d.%d Fr." % (f, r) if r < 10 else "%d.%d Fr." % (f, r // 10), "%d.%02d Fr." % (t // 10, t % 10), chf(t + 100), "%d Fr." % t],
                     "100 Rp. = 1 Fr. %d Rp. = %d Fr. %d Rp. = <b>%s</b>. Nach dem Punkt stehen immer zwei Stellen." % (t, f, r, chf(t)))
        r = R.choice([5, 10, 20, 30, 40, 50, 60, 70, 80, 90])
        t = f * 100 + r
        return M("Wie schreibt man %d Franken und %d Rappen mit Punkt?" % (f, r), chf(t), ["%d.%d Fr." % (f, r) if r < 10 else "%d.%d Fr." % (f, r // 10) if r % 10 == 0 else chf(t + 1000),
                                                                                     "%d.%02d Fr." % (r, f) if r < 100 else chf(t + 1), chf(t + 1000), chf(t - 5)],
                 "Rappen stehen mit zwei Stellen nach dem Punkt: %d Rp. → %02d. Also <b>%s</b>." % (r, r, chf(t)))

    def preise():
        n = R.choice([2, 2, 3])
        ps = [R.randint(1, 15) * 100 + R.choice([0, 20, 40, 50, 75, 80, 90, 95]) for _ in range(n)]
        t = sum(ps)
        return M("Rechne zusammen: %s" % " + ".join(chf(p) for p in ps), chf(t), [chf(t + 100), chf(t - 100) if t > 100 else chf(t + 200), chf(t + 10), chf(t - 5)],
                 "Franken und Rappen getrennt rechnen. Werden es mehr als 100 Rp., ist das 1 Fr. mehr. Ergebnis: <b>%s</b>." % chf(t))

    def rueckgeld():
        pay = R.choice([1000, 2000, 5000, 10000])
        price = r5(105, pay - 5)
        if price % 100 == 0:
            return None
        back = pay - price
        return M("Ein Spiel kostet %s. Du bezahlst mit %s. Wie viel Rückgeld bekommst du?" % (chf(price), chf(pay)), chf(back),
                 [chf(back + 100), chf(back - 100) if back > 100 else chf(back + 200), chf(back + 10), chf(back - 5) if back > 5 else chf(back + 15)],
                 "Ergänze von %s bis %s: <b>%s</b>." % (chf(price), chf(pay), chf(back)))

    WAREN = [("ein Gipfeli", 120, 160), ("ein Heft", 150, 350), ("einen Farbstift", 80, 250), ("ein Glace", 200, 450), ("einen Apfel", 50, 120),
             ("ein Buch", 900, 2500), ("eine Zeitschrift", 450, 800), ("einen Radiergummi", 90, 200), ("ein Sandwich", 450, 750), ("eine Flasche Wasser", 120, 250)]

    def sache():
        k = R.randint(0, 2)
        p = K.next()
        x = p[0]
        if k == 0:
            (a, a1, a2), (b, b1, b2) = R.sample(WAREN, 2)
            pa, pb = r5(a1, a2), r5(b1, b2)
            have = R.choice([1000, 2000, 5000])
            if pa + pb >= have:
                return None
            r = have - pa - pb
            q = "%s hat %s. %s kauft %s für %s und %s für %s. Wie viel Geld hat %s noch?" % (x, chf(have), p[1].capitalize(), a, chf(pa), b, chf(pb), p[1])
            return M(q, chf(r), [chf(r + 100), chf(r - 100) if r > 100 else chf(r + 200), chf(have - pa), chf(pa + pb)],
                     "Zusammen: %s + %s = %s. %s − %s = <b>%s</b>." % (chf(pa), chf(pb), chf(pa + pb), chf(have), chf(pa + pb), chf(r)))
        if k == 1:
            w = r5(50, 500)
            n = R.randint(3, 9)
            r = w * n
            return M("%s spart jede Woche %s. Wie viel Geld hat %s nach %d Wochen gespart?" % (x, chf(w), p[1], n), chf(r), [chf(r + w), chf(r - w), chf(w + n * 100), chf(r * 10)],
                     "%d × %s = <b>%s</b>." % (n, chf(w), chf(r)))
        (a, a1, a2) = R.choice(WAREN)
        pa = r5(a1, min(a2, 400))
        n = R.randint(2, 6)
        r = pa * n
        return M("%s kauft %d-mal %s für je %s. Wie viel muss %s bezahlen?" % (x, n, a, chf(pa), p[1]), chf(r), [chf(r + pa), chf(r - pa), chf(pa + n), chf(r + 100)],
                 "%d × %s = <b>%s</b>." % (n, chf(pa), chf(r)))

    seen = set()
    sets = [("Geld zählen", D.mix(R, seen, [(zaehlen, 20)])), ("Franken und Rappen", D.mix(R, seen, [(umwandeln, 20)])),
            ("Preise zusammenrechnen", D.mix(R, seen, [(preise, 20)])), ("Rückgeld", D.mix(R, seen, [(rueckgeld, 20)])),
            ("Sachaufgaben mit Geld", D.mix(R, seen, [(sache, 20)]))]
    body = D.lesson(
        ["In der Schweiz bezahlen wir mit Franken (Fr.) und Rappen (Rp.). <b>1 Fr. = 100 Rp.</b>",
         "Münzen: 5 Rp., 10 Rp., 20 Rp., ½ Fr., 1 Fr., 2 Fr., 5 Fr. Noten: 10, 20, 50, 100, 200 und 1000 Fr.",
         "Wir schreiben Geldbeträge mit Punkt: 3 Fr. 50 Rp. = <b>3.50 Fr.</b> Nach dem Punkt stehen immer zwei Stellen.",
         "Beim Rückgeld ergänzen wir vom Preis bis zum bezahlten Betrag."],
        [D.example("Wie viel sind 2 Fr. + 1 Fr. + 50 Rp. + 20 Rp.?", ["Franken: 3 Fr.", "Rappen: 70 Rp."], "3.70 Fr."),
         D.example("Ein Heft kostet 2.40 Fr. Du bezahlst mit 5 Fr.", ["2.40 → 3 Fr.: 60 Rp.", "3 Fr. → 5 Fr.: 2 Fr."], "2.60 Fr. Rückgeld")],
        [["3.05 Fr. als 3 Fr. 50 Rp. lesen", "Die 0 nach dem Punkt zeigt: nur 5 Rappen"], ["1 Fr. = 10 Rp.", "1 Fr. = 100 Rp."],
         ["Beim Zählen eine Münze doppelt zählen", "Vom grössten Wert aus zählen und abhaken"]])
    faq = [{"q": "Welche Münzen gibt es in der Schweiz?", "a": "5 Rappen, 10 Rappen, 20 Rappen, ½ Franken, 1 Franken, 2 Franken und 5 Franken. Die kleinste Münze ist 5 Rappen; Preise werden auf 5 Rappen gerundet."},
           {"q": "Wie schreibt man Geldbeträge?", "a": "Mit Punkt und zwei Stellen für die Rappen: 4 Fr. 5 Rp. = 4.05 Fr."},
           {"q": "Wie übt man Rückgeld?", "a": "Vom Preis aus bis zum nächsten ganzen Franken ergänzen, dann bis zum bezahlten Betrag."},
           {"q": "Was steht im Lehrplan 21 dazu?", "a": "Geld gehört zu den Grössen: Die Kinder können Grössen schätzen, messen, umwandeln und mit ihnen rechnen (MA.3.A.2)."}]
    C.write(slug, grade, sort, codes, dom, "Geld: Franken und Rappen", "Geld",
            "Mathematik 3. Klasse: Franken und Rappen – Geld zählen, umwandeln, Preise zusammenrechnen, Rückgeld und Sachaufgaben. 100 Übungsaufgaben online und Arbeitsblatt mit Lösungen.",
            "1 Fr. = 100 Rp.", "3 Fr. 50 Rp. schreibt man 3.50 Fr.", body, faq, sets, R)
