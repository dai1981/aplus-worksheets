# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 1: Plus bis 10（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k1_plus_bis_10.py
Plusaufgaben zu Bildern, Plusaufgaben rechnen, Tauschaufgaben und Zahlenstrahl, Platzhalter, Rechengeschichten.
Fehler: beim Weiterzählen die Startzahl mitgezählt (um 1 zu wenig), minus statt plus, das Ergebnis statt der fehlenden Zahl angegeben.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids
from de_k2 import de, KINDS, DING, ding
from k_pics import two_groups_svg, hop_line_svg

R = random.Random(49405)
KIDS = Kids(R)


def w(x, hi=10):
    return [str(v) for v in (x - 1, x + 1, x - 2, x + 2) if 0 <= v <= hi + 1 and v != x]


def bild():
    a, b = R.randint(1, 6), R.randint(1, 5)
    if a + b > 10:
        return None
    k = R.choice(KINDS)
    pic = de(two_groups_svg(a, k, b, k, word="+"), "%s und noch %s" % (ding(k, a), ding(k, b)))
    if R.random() < 0.5:
        ans = "%d + %d = %d" % (a, b, a + b)
        return mcq(pic + "Welche Aufgabe passt zum Bild?", ans, ["%d + %d = %d" % (a, b + 1, a + b + 1), "%d − %d = %d" % (max(a, b), min(a, b), abs(a - b)), "%d + %d = %d" % (a, b, a + b - 1)],
                   "%d und %d: <b>%s</b>." % (a, b, ans))
    return mcq(pic + "Wie viele %s sind es zusammen?" % DING[k][1], str(a + b), w(a + b), "%d + %d = <b>%d</b>." % (a, b, a + b))


def rechnen():
    a, b = R.randint(0, 9), R.randint(0, 9)
    if a + b > 10 or (a == 0 and b == 0):
        return None
    return mcq("%d + %d = ?" % (a, b), str(a + b), w(a + b) + ([str(abs(a - b))] if a != b else []), "%d + %d = <b>%d</b>." % (a, b, a + b))


def tausch():
    if R.random() < 0.5:
        a, b = R.randint(1, 8), R.randint(1, 8)
        if a + b > 10 or a == b:
            return None
        return mcq("%d + %d = %d + ?" % (a, b, b), str(a), [str(b), str(a + b), str(a + 1)],
                   "Tauschaufgabe: %d + %d = %d + <b>%d</b>. Beide sind %d." % (a, b, b, a, a + b))
    s, h = R.randint(0, 6), R.randint(1, 4)
    if s + h > 10:
        return None
    pic = de(hop_line_svg(s, h, 0, 10, sp=38), "Zahlenstrahl: Start bei %d, %d Sprünge nach rechts" % (s, h))
    return mcq(pic + "Wo landet der Frosch?", str(s + h), [str(s + h - 1), str(s + h + 1), str(s)] if s else [str(s + h - 1), str(s + h + 1), str(h + 2)],
               "Von %d aus %d Sprünge weiter: %d + %d = <b>%d</b>." % (s, h, s, h, s + h))


def platz():
    a, c = R.randint(1, 8), R.randint(2, 10)
    if c <= a:
        return None
    b = c - a
    if R.random() < 0.5:
        return mcq("%d + ? = %d" % (a, c), str(b), [str(c)] + w(b), "%d + <b>%d</b> = %d." % (a, b, c))
    return mcq("? + %d = %d" % (a, c), str(b), [str(c)] + w(b), "<b>%d</b> + %d = %d." % (b, a, c))


GESCH = [("%s hat %d Äpfel. %s bekommt %d Äpfel dazu. Wie viele Äpfel hat %s jetzt?", "p"),
         ("Auf der Bank sitzen %d Kinder. %d Kinder setzen sich dazu. Wie viele Kinder sitzen jetzt auf der Bank?", None),
         ("Im Teich schwimmen %d Enten. %d Enten kommen dazu. Wie viele Enten schwimmen jetzt im Teich?", None),
         ("%s malt %d Sterne rot und %d Sterne gelb. Wie viele Sterne malt %s?", "p2"),
         ("In der Vase sind %d Blumen. Mama stellt %d Blumen dazu. Wie viele Blumen sind jetzt in der Vase?", None),
         ("Auf dem Baum sitzen %d Vögel. %d Vögel fliegen dazu. Wie viele Vögel sitzen jetzt auf dem Baum?", None)]


def geschichte():
    t, kind = R.choice(GESCH)
    a, b = R.randint(2, 7), R.randint(2, 5)
    if a + b > 10:
        return None
    p = KIDS.next()
    if kind == "p":
        q = t % (p[0], a, p[1].capitalize(), b, p[1])
    elif kind == "p2":
        q = t % (p[0], a, b, p[1])
    else:
        q = t % (a, b)
    return mcq(q, str(a + b), w(a + b) + ([str(abs(a - b))] if a != b else []), "Es kommen welche dazu: %d + %d = <b>%d</b>." % (a, b, a + b))


def main():
    seen = set()
    sets = [
        ("Plus mit Bildern", mix(R, seen, [(bild, 20)])),
        ("Plusaufgaben rechnen", mix(R, seen, [(rechnen, 20)])),
        ("Tauschaufgaben und Zahlenstrahl", mix(R, seen, [(tausch, 20)])),
        ("Welche Zahl fehlt?", mix(R, seen, [(platz, 20)])),
        ("Rechengeschichten", mix(R, seen, [(geschichte, 20)])),
    ]
    body = lesson(
        ["Bei <b>plus</b> kommt etwas dazu. Das Zeichen ist +.",
         "Rechne von der größeren Zahl aus weiter: 2 + 6, denke 6, 7, 8.",
         "Tauschaufgabe: 2 + 6 und 6 + 2 haben dasselbe Ergebnis.",
         "Am Zahlenstrahl springst du nach rechts."],
        [example("3 Äpfel und 4 Äpfel", ["3 + 4"], "7 Äpfel"),
         example("5 + ? = 8", ["von 5 bis 8 weiterzählen: 6, 7, 8"], "3")],
        [["Beim Weiterzählen die Startzahl mitzählen (5 + 3: 5, 6, 7)", "Erst nach der Startzahl zählen: 6, 7, 8"],
         ["Bei „dazu“ minus rechnen", "Dazu heißt plus"],
         ["5 + ? = 8 → 8", "Gesucht ist die fehlende Zahl: 3"]])
    faq = [
        {"q": "Wie lernen Kinder das Plusrechnen?", "a": "Zuerst mit Dingen und Bildern (zusammenlegen), dann im Zehnerfeld und am Zahlenstrahl, zuletzt nur mit Zahlen."},
        {"q": "Warum ist die Tauschaufgabe hilfreich?", "a": "2 + 7 rechnet man leichter als 7 + 2, also von der größeren Zahl aus. Das Ergebnis ist gleich."},
        {"q": "Sollen Kinder mit den Fingern rechnen?", "a": "Am Anfang ja. Mit der Zeit sollen sie Aufgaben bis 10 auswendig können und Finger nur noch zum Prüfen nutzen."},
        {"q": "Was ist eine Rechengeschichte?", "a": "Eine kleine Geschichte, in der etwas dazukommt oder weggeht. Die Kinder finden die passende Aufgabe."},
    ]
    make_unit(R, "plus-bis-10", "Z",
              "Die Schülerinnen und Schüler verstehen die Addition als Zusammenfügen und Hinzufügen, lösen Plusaufgaben bis 10 an Bildern, im Kopf und am Zahlenstrahl, nutzen Tauschaufgaben und lösen Rechengeschichten (Zusammenfassung).",
              "Plus bis 10",
              "Plus bis 10 Klasse 1 – Arbeitsblätter mit Lösungen",
              "Plus bis 10",
              "Plus bis 10 für Klasse 1: Plusaufgaben mit Bildern, rechnen, Tauschaufgaben, Zahlenstrahl, fehlende Zahlen und Rechengeschichten. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Plus: Es kommt etwas dazu.",
              "Von der größeren Zahl aus weiterzählen.",
              body, faq, sets, 5, grade="klasse-1")


if __name__ == "__main__":
    main()
