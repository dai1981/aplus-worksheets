# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 1: Zahlen vergleichen bis 20（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k1_zahlen_vergleichen.py
Mengen vergleichen, wie viele mehr?, größer – kleiner – gleich (<, >, =), Zahlen ordnen, Sachaufgaben.
Fehler: nach der Größe der Bilder statt nach der Anzahl urteilen, Zeichen verdreht, „wie viele mehr“ mit der ganzen Menge beantwortet.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids
from de_k2 import de, KINDS, DING, ding
from k_pics import row_svg, two_groups_svg

R = random.Random(49403)
KIDS = Kids(R)
LT, GT = "&lt;", "&gt;"


def mengen():
    k1, k2 = R.sample(KINDS, 2)
    a, b = R.sample(range(2, 11), 2)
    pic = de(two_groups_svg(a, k1, b, k2, word="|"), "%s und %s" % (ding(k1, a), ding(k2, b)))
    more = DING[k1][1] if a > b else DING[k2][1]
    less = DING[k2][1] if a > b else DING[k1][1]
    return mcq(pic + "Wovon gibt es mehr: %s oder %s?" % (DING[k1][1], DING[k2][1]), more, [less, "Von beiden gleich viele", "Das kann man nicht sagen"],
               "%d %s %d. Es gibt mehr <b>%s</b>." % (max(a, b), "ist mehr als", min(a, b), more))


def mehr():
    k1, k2 = R.sample(KINDS, 2)
    a, b = R.sample(range(2, 11), 2)
    if a < b:
        a, b = b, a
    pic = de(row_svg(a, k1, per_row=10), ding(k1, a)) + de(row_svg(b, k2, per_row=10), ding(k2, b))
    d = a - b
    return mcq(pic + "Wie viele %s sind es mehr als %s?" % (DING[k1][1], DING[k2][1]), str(d), [str(a), str(d + 1), str(d - 1) if d > 1 else str(b)],
               "Lege immer ein Paar. %d %s %s übrig: <b>%d</b>." % (d, DING[k1][0] if d == 1 else DING[k1][1], "bleibt" if d == 1 else "bleiben", d))


def stimmt(a, b):
    sym = "=" if a == b else LT if a < b else GT
    ans = "%d %s %d" % (a, sym, b)
    w = ["%d %s %d" % (a, x, b) for x in (LT, GT, "=") if x != sym]
    w.append("%d %s %d" % (b, sym, a) if sym != "=" else "%d %s %d" % (b, LT, a))
    return ans, w


def zeichen():
    a = R.randint(0, 20)
    b = R.choice([a, a + R.randint(1, 5), a - R.randint(1, 5), (a % 10) * 10 + a // 10 if 10 <= a <= 20 else a + 2])
    if not 0 <= b <= 20 or (a == b and R.random() < 0.6):
        return None
    ans, w = stimmt(a, b)
    return mcq("Welcher Satz stimmt? (%d und %d)" % (a, b), ans, w,
               "Die Spitze zeigt zur kleineren Zahl: <b>%s</b>." % ans if a != b else "Beide Zahlen sind gleich: <b>%s</b>." % ans)


def ordnen():
    nums = R.sample(range(0, 21), 4)
    kind = R.choice(["klein", "gross", "folge"])
    if kind == "klein":
        m = min(nums)
        return mcq("Welche Zahl ist am kleinsten? %s" % ", ".join(map(str, nums)), str(m), [str(x) for x in nums if x != m], "Am kleinsten ist <b>%d</b>." % m)
    if kind == "gross":
        m = max(nums)
        return mcq("Welche Zahl ist am größten? %s" % ", ".join(map(str, nums)), str(m), [str(x) for x in nums if x != m], "Am größten ist <b>%d</b>." % m)
    s = sorted(nums)
    ans = ", ".join(map(str, s))
    return mcq("Ordne von klein nach groß: %s" % ", ".join(map(str, nums)), ans,
               [", ".join(map(str, s[::-1])), ", ".join(map(str, [s[1], s[0], s[2], s[3]])), ", ".join(map(str, [s[0], s[2], s[1], s[3]]))],
               "Von klein nach groß: <b>%s</b>." % ans)


def sache():
    kind = R.choice(["karten", "alter", "tore", "mehr"])
    (n1, _), (n2, _) = KIDS.two()
    a, b = R.sample(range(3, 21), 2)
    if kind == "karten":
        win = n1 if a > b else n2
        return mcq("%s hat %d Murmeln. %s hat %d Murmeln. Wer hat mehr?" % (n1, a, n2, b), win, [n2 if win == n1 else n1, "Beide gleich viele", "Keiner"],
                   "%d ist mehr als %d: <b>%s</b>." % (max(a, b), min(a, b), win))
    if kind == "alter":
        a, b = R.sample(range(5, 12), 2)
        old = n1 if a > b else n2
        return mcq("%s ist %d Jahre alt. %s ist %d Jahre alt. Wer ist älter?" % (n1, a, n2, b), old, [n2 if old == n1 else n1, "Beide sind gleich alt", "Keiner"],
                   "%d ist mehr als %d: <b>%s</b> ist älter." % (max(a, b), min(a, b), old))
    if kind == "tore":
        a, b = R.sample(range(0, 8), 2)
        win = "Team Rot" if a > b else "Team Blau"
        return mcq("Team Rot schießt %d Tore. Team Blau schießt %d Tore. Wer gewinnt?" % (a, b), win, ["Team Blau" if win == "Team Rot" else "Team Rot", "Unentschieden", "Keiner"],
                   "%d ist mehr als %d: <b>%s</b> gewinnt." % (max(a, b), min(a, b), win))
    if a < b:
        a, b = b, a
    return mcq("%s hat %d Sticker, %s hat %d Sticker. Wie viele Sticker hat %s mehr?" % (n1, a, n2, b, n1), str(a - b), [str(a), str(a + b) if a + b <= 20 else str(a - b + 2), str(a - b + 1)],
               "%d − %d = <b>%d</b>." % (a, b, a - b))


def main():
    seen = set()
    sets = [
        ("Wo sind mehr?", mix(R, seen, [(mengen, 20)])),
        ("Wie viele mehr?", mix(R, seen, [(mehr, 20)])),
        ("Größer, kleiner, gleich", mix(R, seen, [(zeichen, 20)])),
        ("Zahlen ordnen", mix(R, seen, [(ordnen, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Zum Vergleichen legst du Paare: Ein Ding von hier, ein Ding von dort. Was übrig bleibt, ist mehr.",
         "Achte auf die <b>Anzahl</b>, nicht auf die Größe der Bilder.",
         "&lt; heißt „kleiner als“, &gt; heißt „größer als“, = heißt „gleich“. Die Spitze zeigt zur kleineren Zahl.",
         "In der Zahlenreihe steht die größere Zahl weiter hinten."],
        [example("7 Äpfel und 4 Birnen", ["4 Paare", "3 Äpfel bleiben übrig"], "3 Äpfel mehr"),
         example("12 ○ 9", ["12 ist größer"], "12 &gt; 9")],
        [["Große Bilder sind mehr", "Zählen, nicht schätzen"],
         ["12 &lt; 9", "Die Spitze zeigt zur 9: 12 &gt; 9"],
         ["„Wie viele mehr?“ – mit 7 antworten", "Gefragt ist der Unterschied: 3"]])
    faq = [
        {"q": "Wie lernen Kinder < und > zu unterscheiden?", "a": "Die offene Seite zeigt zur größeren Zahl, die Spitze zur kleineren. Viele Kinder denken an ein Krokodil, das die größere Zahl fressen will."},
        {"q": "Warum Paare bilden?", "a": "So sieht man ohne Zählen, wo mehr ist, und kann den Unterschied direkt ablesen."},
        {"q": "Was bedeutet „gleich viele“?", "a": "Jedes Ding hat einen Partner und nichts bleibt übrig. Dann schreibt man das Gleichheitszeichen."},
        {"q": "Bis zu welcher Zahl vergleicht man in Klasse 1?", "a": "Bis 20. Im zweiten Schuljahr geht es weiter bis 100."},
    ]
    make_unit(R, "zahlen-vergleichen", "Z",
              "Die Schülerinnen und Schüler vergleichen Mengen und Zahlen bis 20 durch Paarbildung und mit den Zeichen <, > und =, bestimmen Unterschiede und ordnen Zahlen (Zusammenfassung).",
              "Zahlen vergleichen: mehr, weniger, gleich",
              "Zahlen vergleichen Klasse 1 – Arbeitsblätter mit Lösungen",
              "Zahlen vergleichen",
              "Zahlen vergleichen für Klasse 1: Mengen vergleichen, wie viele mehr, größer, kleiner und gleich, Zahlen ordnen. 100 Übungsaufgaben mit Bildern und Lösungen, kostenlos.",
              "Die Spitze zeigt zur kleineren Zahl.",
              "Paare legen: Was übrig bleibt, ist mehr.",
              body, faq, sets, 3, grade="klasse-1")


if __name__ == "__main__":
    main()
