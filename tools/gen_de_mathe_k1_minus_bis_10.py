# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 1: Minus bis 10（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k1_minus_bis_10.py
Minusaufgaben zu Bildern, Minusaufgaben rechnen, Zahlenstrahl rückwärts und Umkehraufgaben, Platzhalter, Rechengeschichten.
Fehler: plus statt minus, beim Rückwärtszählen die Startzahl mitgezählt, die abgezogene Zahl als Ergebnis genannt.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids
from de_k2 import de, KINDS, DING, ding
from k_pics import crossed_row_svg, hop_line_svg

R = random.Random(49406)
KIDS = Kids(R)


def w(x):
    return [str(v) for v in (x - 1, x + 1, x + 2, x - 2) if 0 <= v <= 10 and v != x]


def bild():
    n = R.randint(3, 10)
    k = R.randint(1, n - 1)
    kind = R.choice(KINDS)
    pic = de(crossed_row_svg(n, kind, k), "%s, %d davon durchgestrichen" % (ding(kind, n), k))
    if R.random() < 0.5:
        ans = "%d − %d = %d" % (n, k, n - k)
        return mcq(pic + "Welche Aufgabe passt zum Bild?", ans, ["%d + %d = %d" % (n, k, n + k), "%d − %d = %d" % (n, n - k, k) if n - k != k else "%d − %d = %d" % (n, k + 1, n - k - 1), "%d − %d = %d" % (n, k, n - k + 1)],
                   "%d %s, %d weg: <b>%s</b>." % (n, DING[kind][1], k, ans))
    return mcq(pic + "Wie viele %s bleiben übrig?" % DING[kind][1], str(n - k), [str(k)] + w(n - k) if k != n - k else w(n - k), "%d − %d = <b>%d</b>." % (n, k, n - k))


def rechnen():
    a = R.randint(1, 10)
    b = R.randint(0, a)
    if a == b and R.random() < 0.7:
        return None
    return mcq("%d − %d = ?" % (a, b), str(a - b), w(a - b) + ([str(a + b)] if a + b <= 10 and b else []), "%d − %d = <b>%d</b>." % (a, b, a - b))


def strahl():
    if R.random() < 0.5:
        s = R.randint(4, 10)
        h = R.randint(1, min(4, s))
        pic = de(hop_line_svg(s, -h, 0, 10, sp=38), "Zahlenstrahl: Start bei %d, %d Sprünge nach links" % (s, h))
        return mcq(pic + "Wo landet der Frosch?", str(s - h), [str(s - h + 1), str(s + h) if s + h <= 10 else str(s - h - 1), str(s)],
                   "Von %d aus %d Sprünge zurück: %d − %d = <b>%d</b>." % (s, h, s, h, s - h))
    a, b = R.randint(1, 7), R.randint(1, 7)
    c = a + b
    if c > 10:
        return None
    ans = "%d − %d = %d" % (c, b, a)
    return mcq("Welche Minusaufgabe gehört zu %d + %d = %d?" % (a, b, c), ans, ["%d − %d = %d" % (a, b, a - b) if a > b else "%d − %d = %d" % (b, a, b - a) if b > a else "%d − %d = %d" % (c, a, b + 1),
                                                                          "%d + %d = %d" % (b, a, c), "%d − %d = %d" % (c, b, a + 1)],
               "Umkehraufgabe: Von %d nimmst du %d weg und erhältst %d: <b>%s</b>." % (c, b, a, ans))


def platz():
    a = R.randint(3, 10)
    b = R.randint(1, a - 1)
    c = a - b
    if R.random() < 0.5:
        return mcq("%d − ? = %d" % (a, c), str(b), [str(a + c) if a + c <= 10 else str(b + 2)] + w(b), "%d − <b>%d</b> = %d." % (a, b, c))
    return mcq("? − %d = %d" % (b, c), str(a), [str(c - b) if c > b else str(a + 2)] + w(a), "<b>%d</b> − %d = %d, denn %d + %d = %d." % (a, b, c, c, b, a))


GESCH = [("%s hat %d Bonbons. %s isst %d davon. Wie viele Bonbons hat %s noch?", "p"),
         ("Auf der Wiese sind %d Hasen. %d Hasen hoppeln weg. Wie viele Hasen sind noch auf der Wiese?", None),
         ("Im Bus sitzen %d Kinder. %d Kinder steigen aus. Wie viele Kinder sitzen noch im Bus?", None),
         ("Auf dem Teller liegen %d Kekse. Papa isst %d Kekse. Wie viele Kekse liegen noch auf dem Teller?", None),
         ("%s hat %d Luftballons. %d Luftballons platzen. Wie viele Luftballons hat %s noch?", "p2"),
         ("An der Leine hängen %d Socken. %d Socken fallen herunter. Wie viele Socken hängen noch an der Leine?", None)]


def geschichte():
    t, kind = R.choice(GESCH)
    a = R.randint(4, 10)
    b = R.randint(2, a - 1)
    p = KIDS.next()
    if kind == "p":
        q = t % (p[0], a, p[1].capitalize(), b, p[1])
    elif kind == "p2":
        q = t % (p[0], a, b, p[1])
    else:
        q = t % (a, b)
    return mcq(q, str(a - b), [str(a + b) if a + b <= 20 else str(a - b + 2), str(b) if b != a - b else str(a)] + w(a - b), "Es geht etwas weg: %d − %d = <b>%d</b>." % (a, b, a - b))


def main():
    seen = set()
    sets = [
        ("Minus mit Bildern", mix(R, seen, [(bild, 20)])),
        ("Minusaufgaben rechnen", mix(R, seen, [(rechnen, 20)])),
        ("Zahlenstrahl und Umkehraufgaben", mix(R, seen, [(strahl, 20)])),
        ("Welche Zahl fehlt?", mix(R, seen, [(platz, 20)])),
        ("Rechengeschichten", mix(R, seen, [(geschichte, 20)])),
    ]
    body = lesson(
        ["Bei <b>minus</b> geht etwas weg. Das Zeichen ist −.",
         "Du kannst rückwärts zählen: 8 − 3, denke 7, 6, 5.",
         "Am Zahlenstrahl springst du nach links.",
         "Zu jeder Minusaufgabe gibt es eine Plusaufgabe: 8 − 3 = 5, also 5 + 3 = 8."],
        [example("7 Äpfel, 2 werden gegessen", ["7 − 2"], "5 Äpfel"),
         example("9 − ? = 6", ["von 9 rückwärts bis 6: 8, 7, 6"], "3")],
        [["Beim Rückwärtszählen die Startzahl mitzählen", "Erst bei der nächsten Zahl anfangen"],
         ["Bei „weg“ plus rechnen", "Weg heißt minus"],
         ["7 − 2 = 2", "Gefragt ist, was übrig bleibt: 5"]])
    faq = [
        {"q": "Warum fällt Minus schwerer als Plus?", "a": "Rückwärtszählen ist ungewohnt. Hilfreich sind Bilder mit durchgestrichenen Dingen und der Zahlenstrahl."},
        {"q": "Was ist eine Umkehraufgabe?", "a": "Die Plusaufgabe, die zur Minusaufgabe gehört: zu 9 − 4 = 5 gehört 5 + 4 = 9. Damit kann man prüfen."},
        {"q": "Kann man Minus auch durch Ergänzen rechnen?", "a": "Ja. 9 − 7: Von 7 bis 9 sind es 2. Das ist besonders bei kleinen Unterschieden schnell."},
        {"q": "Was ist eine Rechengeschichte?", "a": "Eine kleine Geschichte, in der etwas weggeht, zum Beispiel Kinder, die aus dem Bus aussteigen."},
    ]
    make_unit(R, "minus-bis-10", "Z",
              "Die Schülerinnen und Schüler verstehen die Subtraktion als Wegnehmen, lösen Minusaufgaben bis 10 an Bildern, im Kopf und am Zahlenstrahl, nutzen Umkehraufgaben und lösen Rechengeschichten (Zusammenfassung).",
              "Minus bis 10",
              "Minus bis 10 Klasse 1 – Arbeitsblätter mit Lösungen",
              "Minus bis 10",
              "Minus bis 10 für Klasse 1: Minusaufgaben mit Bildern, rechnen, Zahlenstrahl, Umkehraufgaben, fehlende Zahlen und Rechengeschichten. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Minus: Es geht etwas weg.",
              "8 − 3 = 5, denn 5 + 3 = 8.",
              body, faq, sets, 6, grade="klasse-1")


if __name__ == "__main__":
    main()
