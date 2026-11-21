# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 2: Zahlen vergleichen und ordnen bis 100（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k2_zahlen_vergleichen_und_ordnen.py
Größer, kleiner, gleich; ordnen; Zahlenstrahl; Zählen in Schritten, gerade und ungerade; Sachaufgaben.
Fehler: nur die Einer vergleichen (39 > 41), Zeichen verdreht, am Zahlenstrahl falsch gezählt.
"""
import random
from de_common import mcq, lesson, example, make_unit, mix, Kids, table
from de_k2 import zahlenstrahl100

R = random.Random(49202)
KIDS = Kids(R)
LT, GT = "&lt;", "&gt;"


def stimmt(a, b, pre=None):
    """Vier Sätze, einer stimmt. pre: linke Seite als Term"""
    L = pre or str(a)
    sym = "=" if a == b else LT if a < b else GT
    opts = ["%s %s %d" % (L, x, b) for x in (LT, GT, "=")]
    ans = "%s %s %d" % (L, sym, b)
    flip = "%d %s %s" % (b, sym, L) if sym != "=" else "%d %s %s" % (b, LT, L)
    return ans, [o for o in opts if o != ans] + [flip]


def zeichen():
    kind = R.choice(["zahl", "zahl", "term"])
    if kind == "zahl":
        a = R.randint(10, 99)
        b = R.choice([a + R.randint(1, 9), a - R.randint(1, 9), (a % 10) * 10 + a // 10, a + 10, a - 10])
        if not 10 <= b <= 100 or b == a:
            return None
        ans, w = stimmt(a, b)
        return mcq("Welcher Satz stimmt?" + " (%d und %d)" % (a, b), ans, w,
                   "Vergleiche zuerst die Zehner. %d %s %d: <b>%s</b>." % (a, "ist kleiner als" if a < b else "ist größer als", b, ans))
    z, e = R.randint(2, 9), R.randint(1, 9)
    b = R.choice([10 * z + e, 10 * e + z, 10 * z + e + 1, 10 * z + e - 1])
    v = 10 * z + e
    ans, w = stimmt(v, b, "%d + %d" % (10 * z, e))
    return mcq("Welcher Satz stimmt? (%d + %d und %d)" % (10 * z, e, b), ans, w,
               "%d + %d = %d. %d %s %d: <b>%s</b>." % (10 * z, e, v, v, "ist gleich" if v == b else "ist kleiner als" if v < b else "ist größer als", b, ans))


def ordnen():
    kind = R.choice(["klein", "gross", "folge"])
    base = R.randint(1, 8)
    nums = set()
    while len(nums) < 4:
        x = R.choice([base * 10 + R.randint(0, 9), R.randint(10, 99)])
        nums.add(x)
    nums = list(nums)
    if kind == "klein":
        m = min(nums)
        return mcq("Welche Zahl ist am kleinsten? %s" % ", ".join(map(str, nums)), str(m), [str(x) for x in nums if x != m],
                   "Vergleiche zuerst die Zehner, dann die Einer: <b>%d</b>." % m)
    if kind == "gross":
        m = max(nums)
        return mcq("Welche Zahl ist am größten? %s" % ", ".join(map(str, nums)), str(m), [str(x) for x in nums if x != m],
                   "Vergleiche zuerst die Zehner, dann die Einer: <b>%d</b>." % m)
    s = sorted(nums)
    ans = " &lt; ".join(map(str, s))
    w1 = " &lt; ".join(map(str, sorted(nums, key=lambda x: (x % 10, x))))
    w2 = " &lt; ".join(map(str, s[::-1]))
    w3 = " &lt; ".join(map(str, [s[1], s[0], s[2], s[3]]))
    return mcq("Ordne die Zahlen %s. Beginne mit der kleinsten." % ", ".join(map(str, nums)), ans, [w1, w2, w3],
               "Richtig geordnet: <b>%s</b>." % ans)


def strahl():
    kind = R.choice(["einer", "zehner", "fuenfer"])
    if kind == "einer":
        lo = R.randint(0, 8) * 10
        v = lo + R.randint(1, 19)
        if v % 10 == 0:
            return None
        pic = zahlenstrahl100(lo, lo + 20, [(v, "A")], step=1, every=10)
        return mcq(pic + "Welche Zahl zeigt der Pfeil A?", str(v), [str(v + 1), str(v - 1), str(lo + (v - lo) * 10 if lo + (v - lo) * 10 <= 100 else v + 2)],
                   "Zähle von %d aus die Striche: <b>%d</b>." % (lo if v - lo < 10 else lo + 10, v))
    if kind == "zehner":
        v = R.randint(1, 9) * 10
        pic = zahlenstrahl100(0, 100, [(v, "A")], step=10, every=50)
        return mcq(pic + "Welche Zahl zeigt der Pfeil A?", str(v), [str(v // 10), str(v + 10) if v < 100 else "80", str(v - 10)],
                   "Jeder Strich ist ein Zehner weiter: <b>%d</b>." % v)
    v = R.randint(1, 19) * 5
    if v % 10 == 0:
        return None
    pic = zahlenstrahl100(0, 100, [(v, "A")], step=5, every=10, width=460)
    return mcq(pic + "Welche Zahl zeigt der Pfeil A?", str(v), [str(v + 5), str(v - 5), str(v // 5)],
               "Jeder Strich sind 5. Der Pfeil steht genau zwischen %d und %d: <b>%d</b>." % (v - 5, v + 5, v))


def schritte():
    kind = R.choice(["2", "5", "10", "gerade", "rueck"])
    if kind in ("2", "5", "10"):
        s = int(kind)
        st = R.randint(0, 100 // s - 5) * s + (R.choice([0, 1]) if s == 2 else 0)
        seq = [st + s * i for i in range(5)]
        if seq[-1] > 100:
            return None
        nxt = seq[-1] + s if seq[-1] + s <= 100 else None
        if not nxt:
            return None
        return mcq("Wie geht die Zahlenfolge weiter? %s, ?" % ", ".join(map(str, seq[:4])), str(seq[4]),
                   [str(seq[4] + 1), str(seq[4] + s), str(seq[3] + 1)],
                   "Es geht immer %d weiter: %d + %d = <b>%d</b>." % (s, seq[3], s, seq[4]))
    if kind == "rueck":
        s = R.choice([2, 5, 10])
        st = R.randint(20, 100)
        seq = [st - s * i for i in range(5)]
        if seq[-1] < 0:
            return None
        return mcq("Wie geht die Zahlenfolge weiter? %s, ?" % ", ".join(map(str, seq[:4])), str(seq[4]),
                   [str(seq[3] + s), str(seq[4] - 1) if seq[4] else str(seq[4] + 1), str(seq[4] - s) if seq[4] >= s else str(seq[4] + 2)],
                   "Es geht immer %d zurück: %d − %d = <b>%d</b>." % (s, seq[3], s, seq[4]))
    g = R.choice([True, False])
    nums = R.sample(range(11, 99), 12)
    good = [x for x in nums if (x % 2 == 0) == g]
    bad = [x for x in nums if (x % 2 == 0) != g]
    if not good or len(bad) < 3:
        return None
    return mcq("Welche Zahl ist %s?" % ("gerade" if g else "ungerade"), str(good[0]), [str(x) for x in bad[:3]],
               "%s Zahlen enden auf %s. <b>%d</b> ist %s." % ("Gerade" if g else "Ungerade", "0, 2, 4, 6 oder 8" if g else "1, 3, 5, 7 oder 9", good[0], "gerade" if g else "ungerade"))


def sache():
    kind = R.choice(["sammeln", "haus", "rang", "zwischen"])
    if kind == "sammeln":
        (a, pa), (b, pb) = KIDS.two()
        x, y = R.randint(20, 99), R.randint(20, 99)
        if abs(x - y) < 1 or x // 10 == y // 10 and R.random() < 0.3:
            return None
        if x == y:
            return None
        win = a if x > y else b
        return mcq("%s hat %d Sticker. %s hat %d Sticker. Wer hat mehr?" % (a, x, b, y), win, [b if win == a else a, "Beide gleich viele", "Das kann man nicht sagen"],
                   "%d %s %d: <b>%s</b> hat mehr." % (x, GT if x > y else LT, y, win))
    if kind == "haus":
        n = R.randint(12, 96)
        if n % 2:
            n += 1
        return mcq("In einer Straße stehen auf einer Seite die geraden Hausnummern: %d, %d, %d, … Welche Nummer hat das nächste Haus?" % (n - 4, n - 2, n),
                   str(n + 2), [str(n + 1), str(n + 10), str(n - 2)],
                   "Immer 2 weiter: <b>%d</b>." % (n + 2))
    if kind == "rang":
        ps = [KIDS.next() for _ in range(3)]
        if len({p[0] for p in ps}) < 3:
            return None
        pts = R.sample(range(25, 99), 3)
        o = sorted(range(3), key=lambda i: -pts[i])
        return mcq("Beim Weitwurf erreichen %s %d Punkte, %s %d Punkte und %s %d Punkte. Wer kommt auf Platz 2?" % (ps[0][0], pts[0], ps[1][0], pts[1], ps[2][0], pts[2]),
                   ps[o[1]][0], [ps[o[0]][0], ps[o[2]][0], "Alle sind gleich gut"],
                   "Ordne von groß nach klein: %s. Platz 2: <b>%s</b>." % (", ".join(str(pts[i]) for i in o), ps[o[1]][0]))
    p = KIDS.next()
    a = R.randint(20, 90)
    return mcq("%s denkt sich eine Zahl. Sie ist größer als %d und kleiner als %d. Welche Zahl ist es?" % (p[0], a, a + 2), str(a + 1), [str(a), str(a + 2), str(a + 10)],
               "Zwischen %d und %d liegt nur <b>%d</b>." % (a, a + 2, a + 1))


def main():
    seen = set()
    sets = [
        ("Größer, kleiner oder gleich?", mix(R, seen, [(zeichen, 20)])),
        ("Zahlen ordnen", mix(R, seen, [(ordnen, 20)])),
        ("Am Zahlenstrahl", mix(R, seen, [(strahl, 20)])),
        ("Zählen in Schritten", mix(R, seen, [(schritte, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Vergleiche zuerst die <b>Zehner</b>. Sind sie gleich, vergleiche die Einer.",
         "&lt; heißt „ist kleiner als“, &gt; heißt „ist größer als“. Die Spitze zeigt immer auf die kleinere Zahl.",
         "Am Zahlenstrahl stehen die kleinen Zahlen links und die großen Zahlen rechts.",
         "Gerade Zahlen enden auf 0, 2, 4, 6 oder 8."],
        [example("39 ○ 41", ["3 Zehner und 4 Zehner", "3 Zehner sind weniger"], "39 &lt; 41"),
         example("Ordne 58, 85, 53", ["5 Zehner: 53 und 58", "8 Zehner: 85"], "53 &lt; 58 &lt; 85")],
        [["39 &gt; 41, weil 9 größer als 1 ist", "Zuerst die Zehner vergleichen: 39 &lt; 41"],
         ["Das Zeichen umdrehen", "Die Spitze zeigt zur kleineren Zahl"],
         ["Am Zahlenstrahl jeden Strich als 10 zählen", "Erst schauen, wie viel ein Strich ist"]])
    faq = [
        {"q": "Wie merken sich Kinder die Zeichen < und >?", "a": "Die offene Seite zeigt zur größeren Zahl, die Spitze zur kleineren. Manche stellen sich ein Krokodil vor, das die größere Zahl fressen will."},
        {"q": "Warum ist 39 kleiner als 41?", "a": "Weil 39 nur 3 Zehner hat und 41 schon 4 Zehner. Die Einer zählen erst, wenn die Zehner gleich sind."},
        {"q": "Was sind gerade Zahlen?", "a": "Zahlen, die man ohne Rest in zwei gleiche Teile teilen kann. Sie enden auf 0, 2, 4, 6 oder 8."},
        {"q": "Wie liest man einen Zahlenstrahl?", "a": "Zuerst schaut man, wie groß ein Schritt zwischen zwei Strichen ist. Dann zählt man von einer bekannten Zahl aus weiter."},
    ]
    make_unit(R, "zahlen-vergleichen-und-ordnen", "Z",
              "Die Schülerinnen und Schüler vergleichen und ordnen Zahlen bis 100 mit den Zeichen <, > und =, orientieren sich am Zahlenstrahl, zählen in Schritten und unterscheiden gerade und ungerade Zahlen (Zusammenfassung).",
              "Zahlen vergleichen und ordnen bis 100",
              "Zahlen vergleichen und ordnen bis 100 Klasse 2 – Arbeitsblätter mit Lösungen",
              "Zahlen vergleichen",
              "Zahlen vergleichen und ordnen für Klasse 2: größer, kleiner, gleich, Zahlenstrahl, Zählen in Schritten, gerade und ungerade Zahlen. 100 Übungsaufgaben mit Lösungen, kostenlos.",
              "Zuerst die Zehner vergleichen, dann die Einer.",
              "Die Spitze von < und > zeigt auf die kleinere Zahl.",
              body, faq, sets, 2, grade="klasse-2")


if __name__ == "__main__":
    main()
