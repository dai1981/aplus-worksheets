# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 3: Zahlen bis 1000（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k3_zahlen_bis_1000.py
Hunderter, Zehner, Einer; Zahlwörter; Zerlegen; Zahlenstrahl; Nachbarzahlen; Zahlenrätsel.
Fehler: Zahlendreher (354 → 345), fehlende Null (4 H 7 E → 47), falsch abgelesene Skala.
"""
import random
from de_common import (mcq, num, lesson, example, make_unit, pick_unique, mix, dienes, stellenwerttafel,
                       zahlenstrahl, Kids)

R = random.Random(49001)

ONES = ["", "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun"]
TEENS = ["zehn", "elf", "zwölf", "dreizehn", "vierzehn", "fünfzehn", "sechzehn", "siebzehn", "achtzehn", "neunzehn"]
TENS = ["", "", "zwanzig", "dreißig", "vierzig", "fünfzig", "sechzig", "siebzig", "achtzig", "neunzig"]


def w99(n):
    if n < 10:
        return ONES[n]
    if n < 20:
        return TEENS[n - 10]
    t, o = divmod(n, 10)
    return (("ein" if o == 1 else ONES[o]) + "und" + TENS[t]) if o else TENS[t]


def wort(n):
    if n == 1000:
        return "eintausend"
    h, r = divmod(n, 100)
    s = (("ein" if h == 1 else ONES[h]) + "hundert") if h else ""
    return s + w99(r)


def dreher(n):
    """Zahlendreher: Zehner und Einer vertauscht"""
    h, z, e = n // 100, n // 10 % 10, n % 10
    return h * 100 + e * 10 + z if z != e else None


def three():
    return R.randint(101, 999)


# ---------------------------------------------------------------- Runde 1: H Z E
def s1_bild():
    h, z, e = R.randint(1, 4), R.randint(0, 9), R.randint(0, 9)
    n = 100 * h + 10 * z + e
    w = [dreher(n), 100 * h + z + 10 * e if z != e else None, h * 10 + z if e == 0 else 100 * z + 10 * h + e,
         n + 10, n - 1, n + 100]
    return mcq(dienes(h, z, e, "Hunderterplatten, Zehnerstangen und Einerwürfel") + "Welche Zahl ist dargestellt?", num(n),
               [num(x) for x in w if x and 0 < x < 1000 and x != n],
               "%d Hunderter, %d Zehner und %d Einer: %d + %d + %d = <b>%s</b>." % (h, z, e, 100 * h, 10 * z, e, num(n)))


def s1_tafel():
    h, z, e = R.randint(1, 9), R.randint(0, 9), R.randint(0, 9)
    if z == 0 and e == 0:
        return None
    n = 100 * h + 10 * z + e
    nozero = int("%d%s%s" % (h, z if z else "", e if e else "")) if (z == 0 or e == 0) else None
    w = [nozero, dreher(n), 100 * e + 10 * z + h if e else None, n + 10, n - 10, n + 1]
    return mcq("Welche Zahl steht in der Stellenwerttafel?" + stellenwerttafel(h, z, e), num(n),
               [num(x) for x in w if x and x != n and x < 1000],
               "H = Hunderter, Z = Zehner, E = Einer. %d H, %d Z, %d E ist <b>%s</b>.%s"
               % (h, z, e, num(n), " Die Null hält den Platz frei." if (z == 0 or e == 0) else ""))


def s1_stelle():
    n = three()
    h, z, e = n // 100, n // 10 % 10, n % 10
    if len({h, z, e}) < 3:
        return None
    pos = R.choice(["Hunderter", "Zehner", "Einer"])
    ans = {"Hunderter": h, "Zehner": z, "Einer": e}[pos]
    wert = {"Hunderter": 100 * h, "Zehner": 10 * z, "Einer": e}[pos]
    q = "Wie viele %s hat die Zahl %s?" % (pos, num(n))
    w = [h, z, e, wert, n // 10 if pos == "Zehner" else None]
    return mcq(q, str(ans), [str(x) for x in w if x is not None and x != ans],
               "%s = %d H %d Z %d E. Die Zahl hat <b>%d %s</b>." % (num(n), h, z, e, ans, pos))


# ---------------------------------------------------------------- Runde 2: Zahlwörter
def s2_wort():
    n = three()
    d = dreher(n)
    w = [d, n // 100 * 100 + n % 10 * 10 + n // 10 % 10 if d else None,
         int(str(n)[0] + str(n)[2] + str(n)[1]) if d else None, n + 100, n - 100, n + 10, n + 1]
    return mcq("Schreibe mit Ziffern: <b>%s</b>" % wort(n), num(n), [num(x) for x in w if x and 0 < x < 1000 and x != n],
               ("Erst die Hunderter, dann die Zehner, dann die Einer. Achtung: Wir sprechen die Einer vor den Zehnern. %s = <b>%s</b>."
                if n % 100 > 20 and n % 10 else "Erst die Hunderter, dann der Rest: %s = <b>%s</b>.") % (wort(n), num(n)))


def s2_lesen():
    n = three()
    d = dreher(n)
    if not d:
        return None
    w = [wort(d), wort(n + 100) if n < 900 else wort(n - 100), wort(n + 10) if n % 100 < 90 else wort(n - 10),
         wort(n + 1)]
    return mcq("Wie heißt die Zahl <b>%s</b>?" % num(n), wort(n), w,
               "%s: %d Hunderter, dann %s. Richtig ist <b>%s</b>." % (num(n), n // 100, w99(n % 100) or "keine Zehner und Einer", wort(n)))


def s2_null():
    h = R.randint(1, 9)
    k = R.choice(["0e", "z0", "00"])
    if k == "0e":
        e = R.randint(1, 9)
        n = 100 * h + e
        w = [10 * h + e, 100 * h + 10 * e, n + 10, n + 100 if h < 9 else n - 100]
    elif k == "z0":
        z = R.randint(1, 9)
        n = 100 * h + 10 * z
        w = [10 * h + z, 100 * h + z, 1000 + z if h == 1 else n + 1, n + 100 if h < 9 else n - 100]
    else:
        n = 100 * h
        w = [10 * h, h, 100 * h + 1, n + 10]
    return mcq("Schreibe mit Ziffern: <b>%s</b>" % wort(n), num(n), [num(x) for x in w if x and x < 1000 and x != n],
               "%s hat %d Hunderter, %d Zehner und %d Einer. Fehlende Stellen schreibst du mit 0: <b>%s</b>."
               % (wort(n), n // 100, n // 10 % 10, n % 10, num(n)))


# ---------------------------------------------------------------- Runde 3: Zerlegen
def s3_plus():
    n = three()
    h, z, e = n // 100, n // 10 % 10, n % 10
    parts = [100 * h, 10 * z, e]
    parts = [p for p in parts if p]
    if len(parts) < 2:
        return None
    R.shuffle(parts)
    q = "%s = ?" % " + ".join(num(p) for p in parts)
    w = [int("".join(str(p) for p in parts)) if len("".join(str(p) for p in parts)) <= 3 else None,
         dreher(n), 100 * h + e if z and e else None, 100 * h + 10 * z if e and z else None, n + 10, n - 10, n + 100]
    return mcq(q, num(n), [num(x) for x in w if x and x < 1000 and x != n],
               "%d Hunderter, %d Zehner, %d Einer ergeben <b>%s</b>." % (h, z, e, num(n)))


def s3_gemischt():
    h, e = R.randint(1, 9), R.randint(1, 9)
    z = R.choice([0, 0, R.randint(1, 9)])
    n = 100 * h + 10 * z + e
    bits = ["%d H" % h] + (["%d Z" % z] if z else []) + ["%d E" % e]
    R.shuffle(bits)
    w = [10 * h + e if z == 0 else 100 * e + 10 * z + h, 100 * h + e if z else 10 * h + e, 100 * e + h if z == 0 else dreher(n), n + 100 if h < 9 else n - 100, n + 10]
    return mcq("%s = ?" % " + ".join(bits), num(n), [num(x) for x in w if x and x < 1000 and x != n],
               "Ordne nach Stellen: %d H, %d Z, %d E = <b>%s</b>." % (h, z, e, num(n)))


def s3_zerlegen():
    n = three()
    h, z, e = n // 100, n // 10 % 10, n % 10
    if not z or not e:
        return None
    ans = "%s + %s + %s" % (num(100 * h), num(10 * z), e)
    w = ["%d + %d + %d" % (h, z, e), "%s + %s + %s" % (num(100 * h), num(10 * e), z),
         "%s + %s + %s" % (num(100 * z), num(10 * h), e) if z != h else "%s + %s + %s" % (num(10 * h), num(10 * z), e),
         "%s + %s" % (num(100 * h), num(z + e))]
    return mcq("Wie zerlegst du %s richtig?" % num(n), ans, w,
               "%s = %d H %d Z %d E = <b>%s</b>." % (num(n), h, z, e, ans))


# ---------------------------------------------------------------- Runde 4: Zahlenstrahl und Nachbarzahlen
def s4_strahl():
    kind = R.choice(["z", "h", "e"])
    if kind == "h":
        v = R.randint(1, 9) * 100
        lo, hi, step, every = 0, 1000, 100, 500
        lab = [0, 500, 1000]
        w = [v + 100, v - 100, v // 10, v + 50]
    elif kind == "z":
        lo = R.randint(1, 9) * 100
        hi, step, every = lo + 100, 10, 50
        v = lo + R.randint(1, 9) * 10
        if v == lo + 50:
            return None
        lab = [lo, lo + 50, hi]
        w = [v + 10, v - 10, lo + (v - lo) // 10, v + 1]
    else:
        lo = R.randint(10, 98) * 10
        hi, step, every = lo + 10, 1, 5
        v = lo + R.choice([1, 2, 3, 4, 6, 7, 8, 9])
        lab = [lo, lo + 5, hi]
        w = [v + 1, v - 1, lo + (v - lo) * 10 if lo + (v - lo) * 10 < 1000 else v + 2, v + 10]
    pic = zahlenstrahl(lo, hi, step, marks=[(v, "?")], labels=lab, every=every)
    return mcq(pic + "Welche Zahl gehört an den Pfeil?", num(v), [num(x) for x in w if 0 <= x <= 1000 and x != v],
               "Ein Strich bedeutet hier %d. Zähle von %s aus weiter: <b>%s</b>." % (step, num(lab[0] if v < lab[1] else lab[1]), num(v)))


def s4_nachbar():
    kind = R.choice(["vor", "nach", "zehner", "hunderter"])
    n = R.randint(102, 998)
    if kind == "vor":
        a = n - 1
        q = "Welche Zahl ist der Vorgänger von %s?" % num(n)
        w = [n + 1, n - 10, n - 2]
        e = "Der Vorgänger ist um 1 kleiner: %s − 1 = <b>%s</b>." % (num(n), num(a))
        return mcq(q, num(a), [num(x) for x in w], e)
    if kind == "nach":
        if n % 10 != 9:
            n = n // 10 * 10 + 9
        a = n + 1
        q = "Welche Zahl ist der Nachfolger von %s?" % num(n)
        w = [n - 1, n // 10 * 10, n + 10, n + 2]
        e = "Der Nachfolger ist um 1 größer: %s + 1 = <b>%s</b>." % (num(n), num(a))
        return mcq(q, num(a), [num(x) for x in w if x != a and x <= 1000], e)
    if kind == "zehner":
        if n % 10 == 0:
            return None
        lo = n // 10 * 10
        ans = "%s und %s" % (num(lo), num(lo + 10))
        w = ["%s und %s" % (num(n - 1), num(n + 1)), "%s und %s" % (num(lo - 10), num(lo)),
             "%s und %s" % (num(n // 100 * 100), num(n // 100 * 100 + 100)), "%s und %s" % (num(lo + 10), num(lo + 20))]
        return mcq("Zwischen welchen Nachbarzehnern liegt %s?" % num(n), ans, w,
                   "Die Zehnerzahlen direkt davor und danach: <b>%s</b>." % ans)
    if n % 100 == 0:
        return None
    lo = n // 100 * 100
    ans = "%s und %s" % (num(lo), num(lo + 100))
    w = ["%s und %s" % (num(n // 10 * 10), num(n // 10 * 10 + 10)), "%s und %s" % (num(lo - 100), num(lo)) if lo >= 100 else None,
         "%s und %s" % (num(lo + 100), num(lo + 200)) if lo <= 800 else None, "%s und %s" % (num(n - 1), num(n + 1))]
    return mcq("Zwischen welchen Nachbarhundertern liegt %s?" % num(n), ans, w,
               "Die Hunderterzahlen direkt davor und danach: <b>%s</b>." % ans)


# ---------------------------------------------------------------- Runde 5: Zahlenrätsel und Sachaufgaben
KIDS = Kids(R)


def s5_raetsel():
    h, z, e = R.randint(1, 9), R.randint(0, 9), R.randint(1, 9)
    n = 100 * h + 10 * z + e
    kind = R.choice(["zwischen", "stellen", "mehr"])
    if kind == "zwischen":
        lo = n // 10 * 10
        q = "Meine Zahl liegt zwischen %s und %s. Sie hat %d Einer. Welche Zahl ist es?" % (num(lo), num(lo + 10), e)
        w = [lo + 10 + e if lo + 10 + e < 1000 else lo - 10 + e, 100 * h + 10 * e + z if e != z else n + 1, lo - 10 + e if lo >= 110 else n + 2]
        ex = "Zwischen %s und %s stehen nur Zahlen mit %d Zehnern. Mit %d Einern: <b>%s</b>." % (num(lo), num(lo + 10), z, e, num(n))
    elif kind == "stellen":
        if len({h, z, e}) < 3:
            return None
        q = "Meine Zahl hat %d Hunderter, %d Einer und %d Zehner. Welche Zahl ist es?" % (h, e, z)
        w = [100 * h + 10 * e + z, 100 * e + 10 * z + h, 100 * h + e if z else n + 10]
        ex = "Sortiere nach Stellen: H = %d, Z = %d, E = %d. Die Zahl ist <b>%s</b>." % (h, z, e, num(n))
    else:
        if h == 9:
            return None
        base = n
        n = base + 100
        q = "Meine Zahl ist um 100 größer als %s. Welche Zahl ist es?" % num(base)
        w = [base + 10, base + 1, base - 100 if base > 200 else base + 200]
        ex = "100 mehr: Die Hunderterziffer wird um 1 größer. %s + 100 = <b>%s</b>." % (num(base), num(n))
    return mcq(q, num(n), [num(x) for x in w if x and x != n and x < 1000], ex)


SACHE = [
    ("Im Theater gibt es %d Reihen mit je 10 Plätzen und noch %d Einzelplätze. Wie viele Plätze sind es?", "Plätze"),
    ("Eine Klasse sammelt Kronkorken. Es sind %d volle Zehnerbeutel und %d einzelne Kronkorken. Wie viele Kronkorken sind es?", "Kronkorken"),
    ("Im Lager stehen %d Kisten mit je 10 Äpfeln und %d lose Äpfel. Wie viele Äpfel sind es?", "Äpfel"),
]


def s5_sache():
    kind = R.choice(["hunderter", "zehner", "zehner", "geld"])
    if kind == "zehner":
        t = R.choice(SACHE)
        z, e = R.randint(12, 59), R.randint(1, 9)
        n = 10 * z + e
        q = t[0] % (z, e)
        w = [z + e, 10 * e + z if 10 * e + z != n else n + 10, 100 * z + e if 100 * z + e < 1000 else n + 1, n + 10]
        ex = "%d Zehner sind %s. Dazu %d: <b>%s %s</b>." % (z, num(10 * z), e, num(n), t[1])
        return mcq(q, "%s %s" % (num(n), t[1]), ["%s %s" % (num(x), t[1]) for x in w if x != n], ex)
    if kind == "hunderter":
        h, z = R.randint(2, 9), R.randint(1, 9)
        n = 100 * h + 10 * z
        q = "Ein Bäcker backt %d Bleche mit je 100 Brötchen und %d Bleche mit je 10 Brötchen. Wie viele Brötchen sind das?" % (h, z)
        w = [h + z, 10 * h + z, 100 * z + 10 * h if z != h else n + 100, n + 1]
        ex = "%d · 100 = %s und %d · 10 = %s. Zusammen <b>%s Brötchen</b>." % (h, num(100 * h), z, num(10 * z), num(n))
        return mcq(q, "%s Brötchen" % num(n), ["%s Brötchen" % num(x) for x in w if x != n], ex)
    p = KIDS.next()
    h, z, e = R.randint(1, 9), R.randint(1, 9), R.randint(1, 9)
    n = 100 * h + 10 * z + e
    q = ("%s hat %d Hunderter-Scheine, %d Zehner-Münzen und %d Einer-Münzen aus Spielgeld. Wie viel Spielgeld hat %s?"
         % (p[0], h, z, e, p[1]))
    w = [100 * h + 10 * e + z if e != z else n + 10, h + z + e, 100 * e + 10 * z + h if e != h else n + 1, n + 100 if h < 9 else n - 100]
    ex = "%d H, %d Z, %d E = <b>%s</b>." % (h, z, e, num(n))
    return mcq(q, num(n), [num(x) for x in w if x != n and x < 1000], ex)


def main():
    seen = set()
    sets = [
        ("Hunderter, Zehner und Einer", mix(R, seen, [(s1_bild, 8), (s1_tafel, 7), (s1_stelle, 5)])),
        ("Zahlen lesen und schreiben", mix(R, seen, [(s2_wort, 8), (s2_lesen, 6), (s2_null, 6)])),
        ("Zahlen zerlegen", mix(R, seen, [(s3_plus, 8), (s3_gemischt, 7), (s3_zerlegen, 5)])),
        ("Zahlenstrahl und Nachbarzahlen", mix(R, seen, [(s4_strahl, 12), (s4_nachbar, 8)])),
        ("Zahlenrätsel und Sachaufgaben", mix(R, seen, [(s5_raetsel, 10), (s5_sache, 10)])),
    ]
    body = lesson(
        ["Jede Ziffer hat einen Platz: <b>H</b>underter, <b>Z</b>ehner, <b>E</b>iner.",
         "In 354 stehen 3 Hunderter (300), 5 Zehner (50) und 4 Einer (4).",
         "Beim Sprechen sagen wir die Einer vor den Zehnern: drei-hundert-<b>vier</b>-und-<b>fünfzig</b>. Geschrieben wird trotzdem 3 5 4.",
         "Fehlt eine Stelle, schreibst du eine 0: 4 Hunderter und 7 Einer sind 407."],
        [example("Schreibe mit Ziffern: sechshundertzwölf", ["6 Hunderter = 600", "zwölf = 1 Zehner und 2 Einer"], "612"),
         example("Welche Zahl ist 5 H + 8 E?", ["Hunderter: 5, Zehner: 0, Einer: 8"], "508")],
        [["achthundertdreiundvierzig → 834", "Erst Hunderter, dann Zehner, dann Einer: 843"],
         ["4 H 7 E → 47", "Die leere Zehnerstelle bekommt eine 0: 407"],
         ["Am Zahlenstrahl jeden Strich als 1 zählen", "Erst schauen, wie viel ein Strich bedeutet (1, 10 oder 100)"]],
        extra=stellenwerttafel(3, 5, 4))
    faq = [
        {"q": "Welche Zahlen lernen Kinder in Klasse 3?", "a": "In Klasse 3 wird der Zahlenraum bis 1000 erarbeitet: Hunderter, Zehner und Einer, Zahlen lesen und schreiben, ordnen und am Zahlenstrahl zeigen."},
        {"q": "Warum verdrehen Kinder oft Zehner und Einer?", "a": "Im Deutschen sprechen wir die Einer zuerst (vierundfünfzig), schreiben aber die Zehner zuerst (54). Die Stellenwerttafel hilft, die Ziffern richtig zu setzen."},
        {"q": "Was ist eine Stellenwerttafel?", "a": "Eine Tabelle mit den Spalten H (Hunderter), Z (Zehner) und E (Einer). Jede Ziffer kommt in ihre Spalte."},
        {"q": "Wie übt man den Zahlenstrahl?", "a": "Zuerst klären, wie viel ein Strich bedeutet. Dann von einer beschrifteten Zahl aus in diesen Schritten weiterzählen."},
    ]
    make_unit(R, "zahlen-bis-1000", "Z",
              "Die Schülerinnen und Schüler verstehen den Aufbau des Zehnersystems, stellen Zahlen bis 1000 dar (Stellenwerttafel, Material, Zahlenstrahl) und wechseln zwischen den Darstellungen (Zusammenfassung).",
              "Zahlen bis 1000: Hunderter, Zehner und Einer",
              "Zahlen bis 1000 – Mathe Klasse 3 Arbeitsblätter mit Lösungen",
              "Zahlen bis 1000",
              "Mathe Klasse 3: Zahlen bis 1000 mit Stellenwerttafel, Zahlwörtern, Zahlenstrahl und Nachbarzahlen. 100 Übungsaufgaben online und Arbeitsblatt mit Lösungen zum Ausdrucken (kostenlos).",
              "Hunderter, Zehner, Einer – jede Ziffer hat ihren Platz.",
              "354 = 300 + 50 + 4. Fehlt eine Stelle, schreibst du 0.",
              body, faq, sets, 1)


if __name__ == "__main__":
    main()
