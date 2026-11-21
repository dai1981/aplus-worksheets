# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 1: Rechengeschichten und Sachaufgaben（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k1_rechengeschichten_und_sachaufgaben.py
Welche Aufgabe passt?, Geschichten mit plus, Geschichten mit minus, Frage und Antwort, gemischte Sachaufgaben (ergänzen, vergleichen).
Fehler: plus und minus verwechselt, die Zahl aus dem Text statt des Ergebnisses genannt, unnötige Zahlen mitgerechnet.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids
from de_k2 import de, KINDS, DING, ding
from k_pics import two_groups_svg, crossed_row_svg

R = random.Random(49410)
KIDS = Kids(R)


def passt():
    k = R.choice(KINDS)
    if R.random() < 0.5:
        a, b = R.randint(2, 7), R.randint(2, 6)
        if a + b > 12:
            return None
        pic = de(two_groups_svg(a, k, b, k, word="+"), "%s und noch %s" % (ding(k, a), ding(k, b)))
        ans = "%d + %d" % (a, b)
        return mcq(pic + "Es waren %s. Dann kommen %d dazu. Welche Aufgabe passt?" % (ding(k, a), b), ans,
                   ["%d − %d" % (max(a, b), min(a, b)) if a != b else "%d − %d" % (a, 1), "%d + %d" % (a, a), "%d + %d" % (b, b + 1)],
                   "Es kommen welche dazu, also plus: <b>%s</b> = %d." % (ans, a + b))
    n = R.randint(4, 10)
    t = R.randint(1, n - 2)
    pic = de(crossed_row_svg(n, k, t), "%s, %d davon durchgestrichen" % (ding(k, n), t))
    ans = "%d − %d" % (n, t)
    return mcq(pic + "Welche Aufgabe passt zum Bild?", ans, ["%d + %d" % (n, t), "%d − %d" % (n, n - t) if n - t != t else "%d − %d" % (n, t + 1), "%d − %d" % (t, 1) if t > 1 else "%d − %d" % (n, 1)],
               "%d %s, %d sind weg: <b>%s</b> = %d." % (n, DING[k][1], t, ans, n - t))


PLUS = [("%s hat %d Murmeln. %s bekommt %d Murmeln geschenkt. Wie viele Murmeln hat %s jetzt?", "p"),
        ("Am Morgen kommen %d Kinder in die Klasse. Später kommen noch %d Kinder. Wie viele Kinder sind jetzt in der Klasse?", None),
        ("Auf dem Baum sitzen %d Vögel. %d Vögel fliegen dazu. Wie viele Vögel sitzen jetzt auf dem Baum?", None),
        ("Im Stall stehen %d Pferde. Der Bauer bringt %d Pferde dazu. Wie viele Pferde stehen jetzt im Stall?", None),
        ("%s pflückt %d rote und %d gelbe Blumen. Wie viele Blumen hat %s?", "p2"),
        ("Im Aquarium schwimmen %d Fische. Papa setzt %d Fische dazu. Wie viele Fische sind es jetzt?", None)]
MINUS = [("%s hat %d Bonbons. %s verschenkt %d Bonbons. Wie viele Bonbons hat %s noch?", "p"),
         ("Im Zug sitzen %d Kinder. %d Kinder steigen aus. Wie viele Kinder sind noch im Zug?", None),
         ("Auf dem Teller liegen %d Kekse. Die Kinder essen %d Kekse. Wie viele Kekse liegen noch auf dem Teller?", None),
         ("An der Leine hängen %d Wäschestücke. Mama nimmt %d ab. Wie viele hängen noch an der Leine?", None),
         ("%s hat %d Luftballons. %d Luftballons fliegen weg. Wie viele Luftballons hat %s noch?", "p2"),
         ("Auf der Wiese grasen %d Schafe. %d Schafe laufen in den Stall. Wie viele Schafe sind noch auf der Wiese?", None)]


def fill(t, kind, a, b):
    p = KIDS.next()
    if kind == "p":
        return t % (p[0], a, p[1].capitalize(), b, p[1])
    if kind == "p2":
        return t % (p[0], a, b, p[1])
    return t % (a, b)


def plus():
    t, kind = R.choice(PLUS)
    a, b = R.randint(2, 12), R.randint(2, 8)
    if a + b > 20:
        return None
    return mcq(fill(t, kind, a, b), str(a + b), [str(abs(a - b)) if a != b else str(a + b + 2), str(a + b + 1), str(a + b - 1)],
               "Es kommen welche dazu: %d + %d = <b>%d</b>." % (a, b, a + b))


def minus():
    t, kind = R.choice(MINUS)
    a = R.randint(5, 20)
    b = R.randint(2, min(a - 1, 9))
    return mcq(fill(t, kind, a, b), str(a - b), [str(a + b) if a + b <= 25 else str(a - b + 2), str(a - b + 1), str(b) if b != a - b else str(a)],
               "Es geht etwas weg: %d − %d = <b>%d</b>." % (a, b, a - b))


def frage():
    p = KIDS.next()
    kind = R.choice(["antwort", "unnoetig", "frage"])
    if kind == "antwort":
        a, b = R.randint(3, 10), R.randint(2, 8)
        if a + b > 20:
            return None
        ans = "%s hat jetzt %d Karten." % (p[0], a + b)
        return mcq("%s hat %d Karten und bekommt %d dazu. Welcher Antwortsatz passt?" % (p[0], a, b), ans,
                   ["%s hat jetzt %d Karten." % (p[0], a), "%s bekommt %d Karten." % (p[0], b), "%s hat jetzt %d Karten." % (p[0], abs(a - b))] if abs(a - b) > 1 else
                   ["%s hat jetzt %d Karten." % (p[0], a), "%s bekommt %d Karten." % (p[0], b), "%s hat jetzt %d Karten." % (p[0], a + b + 1)],
                   "%d + %d = %d: <b>%s</b>" % (a, b, a + b, ans))
    if kind == "unnoetig":
        age, a, b = R.randint(6, 7), R.randint(3, 10), R.randint(2, 6)
        return mcq("%s ist %d Jahre alt. %s hat %d Stifte und kauft %d dazu. Wie viele Stifte hat %s jetzt?" % (p[0], age, p[1].capitalize(), a, b, p[1]),
                   str(a + b), [str(age + a + b), str(a + age), str(a - b) if a > b else str(a + b + 1)],
                   "Das Alter brauchst du nicht: %d + %d = <b>%d</b>." % (a, b, a + b))
    a, b = R.randint(5, 12), R.randint(2, 4)
    ans = "Wie viele Äpfel sind noch im Korb?"
    return mcq("Im Korb sind %d Äpfel. %s nimmt %d Äpfel heraus. Welche Frage passt zur Rechnung %d − %d?" % (a, p[0], b, a, b), ans,
               ["Wie viele Äpfel sind es zusammen?", "Wie alt ist %s?" % p[0], "Wie viele Körbe gibt es?"],
               "Es geht etwas weg, gefragt ist der Rest: <b>%s</b>" % ans)


def gemischt():
    kind = R.choice(["fehlt", "mehr", "zwei"])
    p = KIDS.next()
    if kind == "fehlt":
        a = R.randint(3, 15)
        z = R.choice([10, 15, 20])
        if a >= z - 1:
            return None
        return mcq("%s möchte %d Bilder malen. %d Bilder sind schon fertig. Wie viele Bilder fehlen noch?" % (p[0], z, a), str(z - a),
                   [str(z + a) if z + a <= 30 else str(z - a + 2), str(z - a + 1), str(a)],
                   "%d + ? = %d. Es fehlen <b>%d</b> Bilder." % (a, z, z - a))
    if kind == "mehr":
        (n1, _), (n2, _) = KIDS.two()
        a, b = R.randint(8, 20), R.randint(2, 9)
        if b >= a:
            return None
        return mcq("%s hat %d Murmeln. %s hat %d Murmeln. Wie viele Murmeln hat %s mehr?" % (n1, a, n2, b, n1), str(a - b),
                   [str(a + b) if a + b <= 30 else str(a - b + 2), str(a), str(a - b + 1)],
                   "Unterschied: %d − %d = <b>%d</b>." % (a, b, a - b))
    a, b, c = R.randint(4, 9), R.randint(2, 6), R.randint(1, 5)
    if a + b > 20 or c >= a + b:
        return None
    return mcq("Im Bus sitzen %d Kinder. %d Kinder steigen ein und 1 Kind steigt aus. Wie viele Kinder sitzen jetzt im Bus?" % (a, b) if c == 1 else
               "Im Bus sitzen %d Kinder. %d Kinder steigen ein und %d Kinder steigen aus. Wie viele Kinder sitzen jetzt im Bus?" % (a, b, c), str(a + b - c),
               [str(a + b), str(a + b + c), str(a - b + c) if a - b + c > 0 else str(a + b - c + 1)],
               "%d + %d = %d. %d − %d = <b>%d</b>." % (a, b, a + b, a + b, c, a + b - c))


def main():
    seen = set()
    sets = [
        ("Welche Aufgabe passt?", mix(R, seen, [(passt, 20)])),
        ("Geschichten mit plus", mix(R, seen, [(plus, 20)])),
        ("Geschichten mit minus", mix(R, seen, [(minus, 20)])),
        ("Frage und Antwort", mix(R, seen, [(frage, 20)])),
        ("Gemischte Sachaufgaben", mix(R, seen, [(gemischt, 20)])),
    ]
    body = lesson(
        ["Stell dir die Geschichte wie einen kleinen Film vor.",
         "Kommt etwas dazu? Dann rechnest du <b>plus</b>.",
         "Geht etwas weg? Dann rechnest du <b>minus</b>.",
         "Schreibe am Ende einen Antwortsatz. Er passt genau zur Frage."],
        [example("6 Kinder spielen. 3 Kinder kommen dazu.", ["dazu: plus", "6 + 3"], "9 Kinder spielen."),
         example("8 Kekse. 5 werden gegessen.", ["weg: minus", "8 − 5"], "3 Kekse bleiben.")],
        [["Bei „aussteigen“ plus rechnen", "Aussteigen heißt weg: minus"],
         ["Eine Zahl aus dem Text als Antwort nehmen", "Erst rechnen, dann antworten"],
         ["Alle Zahlen zusammenrechnen", "Nur die Zahlen nehmen, die zur Frage passen"]])
    faq = [
        {"q": "Was ist eine Rechengeschichte?", "a": "Eine kurze Geschichte aus dem Alltag, zu der eine Rechenaufgabe passt. Kinder lernen so, Mathe in der Welt zu sehen."},
        {"q": "Wie helfe ich meinem Kind bei Sachaufgaben?", "a": "Die Geschichte gemeinsam nachspielen oder malen. Dann fragen: Kommt etwas dazu oder geht etwas weg?"},
        {"q": "Warum ist der Antwortsatz wichtig?", "a": "Er zeigt, ob das Ergebnis zur Frage passt, und übt das genaue Lesen."},
        {"q": "Was tun bei unnötigen Angaben?", "a": "Jede Zahl prüfen: Brauche ich sie für die Frage? Das Alter eines Kindes hat oft nichts mit der Rechnung zu tun."},
    ]
    make_unit(R, "rechengeschichten-und-sachaufgaben", "Z",
              "Die Schülerinnen und Schüler finden zu Bildern und Rechengeschichten passende Plus- und Minusaufgaben bis 20, lösen einfache Sachaufgaben und formulieren Fragen und Antworten (Zusammenfassung).",
              "Rechengeschichten und Sachaufgaben",
              "Rechengeschichten Klasse 1 – Arbeitsblätter mit Lösungen",
              "Rechengeschichten",
              "Rechengeschichten und Sachaufgaben für Klasse 1: Welche Aufgabe passt?, Geschichten mit plus und minus, Frage und Antwort und gemischte Sachaufgaben. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Dazu: plus. Weg: minus.",
              "Am Ende einen Antwortsatz schreiben.",
              body, faq, sets, 10, grade="klasse-1")


if __name__ == "__main__":
    main()
