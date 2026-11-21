# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 3: Runden und Überschlagen（Leitidee Zahl und Operation）
  python3 tools/gen_de_mathe_k3_runden_und_ueberschlagen.py
Runden auf Zehner und Hunderter, welche Zahl wird so gerundet, Überschlag bei Plus und Minus, Sachaufgaben.
Fehler: immer abrunden (347 → 340), bei 5 abrunden, auf die falsche Stelle runden, exakt statt überschlagen.
"""
import random
from de_common import mcq, num, lesson, example, make_unit, mix, zahlenstrahl, Kids

R = random.Random(49003)
KIDS = Kids(R)


def rz(n):
    return (n + 5) // 10 * 10


def rh(n):
    return (n + 50) // 100 * 100


def s1_zehner():
    n = R.randint(12, 995)
    if n % 10 == 0:
        return None
    if R.random() < 0.3:
        n = n // 10 * 10 + 5
    a = rz(n)
    down, up = n // 10 * 10, n // 10 * 10 + 10
    w = [down if a == up else up, rh(n) if rh(n) != a else None, n, a + 10, a - 20]
    return mcq("Runde %s auf Zehner." % num(n), num(a), [num(x) for x in w if x is not None and x != a],
               "Schau auf die Einer: %d. %s Also %s ≈ <b>%s</b>."
               % (n % 10, "Bei 5, 6, 7, 8, 9 rundest du auf." if n % 10 >= 5 else "Bei 1, 2, 3, 4 rundest du ab.", num(n), num(a)))


def s1_strahl():
    n = R.randint(101, 989)
    if n % 10 in (0, 5):
        return None
    lo = n // 10 * 10
    a = rz(n)
    pic = zahlenstrahl(lo, lo + 10, 1, marks=[(n, "?")], labels=[lo, lo + 10], every=5)
    return mcq(pic + "Am Pfeil steht %s. Zu welchem Zehner liegt die Zahl näher?" % num(n), num(a),
               [num(x) for x in (lo + 10 if a == lo else lo, rh(n) if rh(n) not in (lo, lo + 10) else lo + 20, lo + 5)],
               "%s ist näher an <b>%s</b>. Gerundet: %s ≈ %s." % (num(n), num(a), num(n), num(a)))


def s2_hunderter():
    n = R.randint(105, 994)
    if n % 100 == 0:
        return None
    if R.random() < 0.25:
        n = n // 100 * 100 + 50 + R.choice([0, 0, R.randint(1, 9)])
    a = rh(n)
    down, up = n // 100 * 100, n // 100 * 100 + 100
    w = [down if a == up else up, rz(n), n, a + 100 if a < 1000 else a - 200, a - 100]
    return mcq("Runde %s auf Hunderter." % num(n), num(a), [num(x) for x in w if x != a],
               "Schau auf die Zehner: %d. %s Also %s ≈ <b>%s</b>."
               % (n // 10 % 10, "Bei 5 bis 9 Zehnern rundest du auf." if n // 10 % 10 >= 5 else "Bei 0 bis 4 Zehnern rundest du ab.", num(n), num(a)))


def s2_beide():
    n = R.randint(111, 989)
    if n % 10 == 0 or rz(n) == rh(n):
        return None
    which = R.choice(["Zehner", "Hunderter"])
    a = rz(n) if which == "Zehner" else rh(n)
    o = rh(n) if which == "Zehner" else rz(n)
    w = [o, n // 10 * 10 if which == "Zehner" else n // 100 * 100, a + (10 if which == "Zehner" else 100)]
    return mcq("Runde %s auf %s." % (num(n), which), num(a), [num(x) for x in w if x != a],
               "Auf %s runden: Schau auf die Stelle rechts davon. %s ≈ <b>%s</b>." % (which, num(n), num(a)))


def s3_welche():
    kind = R.choice(["Z", "H"])
    if kind == "H":
        t = R.randint(2, 9) * 100
        ok = t - 50 + R.randint(0, 99)
        bad = [t - 50 - R.randint(1, 9), t + 50 + R.randint(0, 9), t + 100 + R.randint(-40, 40)]
        f = rh
        q = "Welche Zahl ergibt auf Hunderter gerundet %s?" % num(t)
    else:
        t = R.randint(11, 98) * 10
        ok = t - 5 + R.randint(0, 9)
        bad = [t - 5 - R.randint(1, 4), t + 5 + R.randint(0, 4), t + 10 + R.randint(-4, 4)]
        f = rz
        q = "Welche Zahl ergibt auf Zehner gerundet %s?" % num(t)
    bad = [b for b in bad if f(b) != t and 0 < b < 1000]
    if f(ok) != t or ok == t or len(set(bad)) < 3:
        return None
    return mcq(q, num(ok), [num(b) for b in bad],
               "%s ≈ %s. Die anderen Zahlen werden zu %s gerundet." % (num(ok), num(t), ", ".join(num(f(b)) for b in bad)))


def s4_plus():
    op = R.choice(["+", "−"])
    a = R.randint(110, 690)
    b = R.randint(110, 980 - a) if op == "+" else R.randint(105, a - 50)
    if rh(a) == a or rh(b) == b or b < 100:
        return None
    ra, rb = rh(a), rh(b)
    est = ra + rb if op == "+" else ra - rb
    exact = a + b if op == "+" else a - b
    if est <= 0 or est == exact:
        return None
    w = [exact, est + 100, est - 100 if est > 100 else est + 200, rz(a) + rz(b) if op == "+" else rz(a) - rz(b)]
    return mcq("Überschlage: %s %s %s ≈ ?" % (num(a), op, num(b)), num(est), [num(x) for x in w if x != est and x > 0],
               "Runde beide Zahlen auf Hunderter: %s %s %s = <b>%s</b>. (Genau wären es %s.)"
               % (num(ra), op, num(rb), num(est), num(exact)))


def s4_pruefen():
    a = R.randint(110, 590)
    b = R.randint(110, 400)
    exact = a + b
    claims = [exact + R.choice([100, -100, 200]), exact]
    c = R.choice(claims)
    ok = c == exact
    est = rh(a) + rh(b)
    q = "Ben rechnet: %s + %s = %s. Überschlage: Kann das stimmen?" % (num(a), num(b), num(c))
    ans = "Ja, der Überschlag ist etwa %s." % num(est) if ok else "Nein, der Überschlag ist etwa %s." % num(est)
    w = ["Nein, der Überschlag ist etwa %s." % num(est) if ok else "Ja, der Überschlag ist etwa %s." % num(est),
         "Ja, der Überschlag ist etwa %s." % num(c if not ok else est + 200),
         "Nein, der Überschlag ist etwa %s." % num(est + 100 if ok else c)]
    if abs(c - est) < 100 and not ok:
        return None
    return mcq(q, ans, w, "%s + %s ≈ %s + %s = %s. %s" % (num(a), num(b), num(rh(a)), num(rh(b)), num(est),
                                                           "Das Ergebnis passt." if ok else "%s liegt zu weit weg, also hat Ben sich verrechnet." % num(c)))


THINGS = [("Besucher", "Im Zoo waren am Samstag %s Besucher."), ("Kinder", "Auf dem Schulfest waren %s Kinder."),
          ("Bücher", "In der Klassenbücherei stehen %s Bücher."), ("Kilometer", "Familie Weber fährt %s Kilometer in den Urlaub."),
          ("Zuschauer", "Beim Fußballspiel der Jugend waren %s Zuschauer."), ("Äpfel", "Bauer Lang hat %s Äpfel geerntet.")]


def s5_sache():
    kind = R.choice(["etwa", "etwa", "summe", "geld"])
    if kind == "etwa":
        word, t = R.choice(THINGS)
        n = R.randint(105, 994)
        if n % 100 == 0:
            return None
        which = R.choice(["Zehner", "Hunderter"])
        a = rz(n) if which == "Zehner" else rh(n)
        q = t % num(n) + " Runde auf %s: Etwa wie viele %s waren es?" % (which, word) if word not in ("Bücher", "Äpfel", "Kilometer") else \
            t % num(n) + " Runde auf %s: Etwa wie viele %s sind es?" % (which, word)
        o = rh(n) if which == "Zehner" else rz(n)
        w = [o, n // 10 * 10 if which == "Zehner" else n // 100 * 100, a + (10 if which == "Zehner" else 100)]
        return mcq(q, "etwa %s" % num(a), ["etwa %s" % num(x) for x in w if x != a],
                   "%s ≈ <b>%s</b> (auf %s gerundet)." % (num(n), num(a), which))
    if kind == "summe":
        a, b = R.randint(120, 480), R.randint(120, 480)
        if rh(a) == a or rh(b) == b:
            return None
        q = "Am Montag kamen %s Besucher ins Schwimmbad, am Dienstag %s. Etwa wie viele waren es zusammen? Runde auf Hunderter." % (num(a), num(b))
        est = rh(a) + rh(b)
        if est == a + b:
            return None
        return mcq(q, "etwa %s" % num(est), ["etwa %s" % num(x) for x in (a + b, est + 100, est - 100, rz(a) + rz(b)) if x != est],
                   "%s + %s ≈ %s + %s = <b>%s</b>." % (num(a), num(b), num(rh(a)), num(rh(b)), num(est)))
    p = KIDS.next()
    have = R.choice([500, 600, 700, 800, 900])
    a = R.randint(have // 2 - 120, have // 2 + 40)
    b = R.randint(90, have - a + 150)
    est = rh(a) + rh(b)
    real = a + b
    if est == have or abs(real - have) < 30:
        return None
    ok = real <= have
    q = "%s möchte ein Fahrrad für %s € und einen Helm für %s € kaufen. %s hat %s €. Reicht das Geld?" % (p[0], num(a), num(b), p[1].capitalize(), num(have))
    ans = "Ja" if ok else "Nein"
    return mcq(q, ans + ", es kostet zusammen %s €." % num(real),
               ["Nein, es kostet zusammen %s €." % num(real) if ok else "Ja, es kostet zusammen %s €." % num(real),
                ans + ", es kostet zusammen %s €." % num(real + 100), ("Nein" if ok else "Ja") + ", es kostet zusammen %s €." % num(real - 100)],
               "Überschlag: %s + %s ≈ %s. Genau: %s + %s = %s €. %s"
               % (num(rh(a)), num(rh(b)), num(est), num(a), num(b), num(real), "Das ist nicht mehr als %s €." % num(have) if ok else "Das ist mehr als %s €." % num(have)))


def main():
    seen = set()
    sets = [
        ("Runden auf Zehner", mix(R, seen, [(s1_zehner, 14), (s1_strahl, 6)])),
        ("Runden auf Hunderter", mix(R, seen, [(s2_hunderter, 14), (s2_beide, 6)])),
        ("Welche Zahl wird so gerundet?", mix(R, seen, [(s3_welche, 20)])),
        ("Überschlagen", mix(R, seen, [(s4_plus, 14), (s4_pruefen, 6)])),
        ("Sachaufgaben zum Runden", mix(R, seen, [(s5_sache, 20)])),
    ]
    body = lesson(
        ["Beim <b>Runden</b> suchst du die nächste Zehner- oder Hunderterzahl.",
         "Schau auf die Stelle <b>rechts</b> von der Stelle, auf die du rundest.",
         "Bei 0, 1, 2, 3, 4 rundest du <b>ab</b>. Bei 5, 6, 7, 8, 9 rundest du <b>auf</b>.",
         "Beim <b>Überschlagen</b> rundest du zuerst und rechnest dann mit den gerundeten Zahlen. So siehst du schnell, ob ein Ergebnis stimmen kann."],
        [example("Runde 467 auf Zehner und auf Hunderter.", ["auf Zehner: Einer 7 → aufrunden → 470", "auf Hunderter: Zehner 6 → aufrunden → 500"], "470 und 500"),
         example("Überschlage: 312 + 489", ["312 ≈ 300, 489 ≈ 500", "300 + 500 = 800"], "etwa 800")],
        [["347 auf Zehner → 340", "Einer 7: aufrunden → 350"],
         ["450 auf Hunderter → 400", "Bei 5 wird aufgerundet → 500"],
         ["Beim Überschlag genau rechnen", "Erst runden, dann im Kopf rechnen"]])
    faq = [
        {"q": "Wann rundet man auf und wann ab?", "a": "Bei 0 bis 4 an der Stelle rechts davon wird abgerundet, bei 5 bis 9 aufgerundet."},
        {"q": "Wofür braucht man den Überschlag?", "a": "Um schnell zu prüfen, ob ein Ergebnis ungefähr stimmt, zum Beispiel beim Einkaufen oder bei der schriftlichen Addition."},
        {"q": "Was bedeutet das Zeichen ≈?", "a": "Es bedeutet „ungefähr gleich“. 347 ≈ 350 heißt: 347 ist ungefähr 350."},
        {"q": "Ist Runden in Klasse 3 oder Klasse 4?", "a": "Runden auf Zehner und Hunderter kommt in vielen Lehrplänen schon in Klasse 3 vor und wird in Klasse 4 bis zur Million erweitert."},
    ]
    make_unit(R, "runden-und-ueberschlagen", "Z",
              "Die Schülerinnen und Schüler runden Zahlen auf Zehner und Hunderter, überschlagen Ergebnisse und nutzen den Überschlag zur Kontrolle (Zusammenfassung).",
              "Runden und Überschlagen bis 1000",
              "Runden auf Zehner und Hunderter – Mathe Klasse 3 Arbeitsblätter",
              "Runden und Überschlagen",
              "Mathe Klasse 3: Runden auf Zehner und Hunderter, Überschlag bei Plus und Minus, Sachaufgaben. 100 Übungsaufgaben mit Lösungen und Arbeitsblatt zum Ausdrucken, kostenlos.",
              "0 bis 4 abrunden, 5 bis 9 aufrunden.",
              "Beim Überschlagen erst runden, dann rechnen.",
              body, faq, sets, 3)


if __name__ == "__main__":
    main()
