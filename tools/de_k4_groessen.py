# -*- coding: utf-8 -*-
"""
Gemeinsame Aufgaben für Größen mit Kommaschreibweise (Klasse 4): Längen, Gewichte, Rauminhalte.
Ein Einheitenpaar: (groß, klein, Faktor). Kommastellen = Anzahl der Nullen im Faktor.
"""
from de_common import mcq, num, NB


def stellen(f):
    return len(str(f)) - 1


def komma(v_small, f, big):
    """v_small in kleiner Einheit → Kommaschreibweise in großer Einheit: 1250, 1000, km → 1,250 km"""
    p = stellen(f)
    g, r = divmod(v_small, f)
    if r == 0:
        return "%s%s%s" % (num(g), NB, big)
    return "%s,%s%s%s" % (num(g), str(r).rjust(p, "0"), NB, big)


def zwei(v_small, f, big, small):
    g, r = divmod(v_small, f)
    if g and r:
        return "%s%s%s %s%s%s" % (num(g), NB, big, num(r), NB, small)
    return "%s%s%s" % (num(g), NB, big) if g else "%s%s%s" % (num(r), NB, small)


def st(f):
    n = stellen(f)
    return "1 Stelle" if n == 1 else "%d Stellen" % n


def u(v, e):
    return "%s%s%s" % (num(v), NB, e)


def falsche_komma(v_small, f, big):
    """typischer Fehler: führende Null nach dem Komma weggelassen (3 m 7 cm → 3,7 m)"""
    p = stellen(f)
    g, r = divmod(v_small, f)
    if r == 0 or len(str(r)) == p:
        return None
    return "%s,%d%s%s" % (num(g), r, NB, big)


def lesen(R, f, big, small):
    """Kommaschreibweise ↔ zwei Einheiten"""
    def mk():
        g = R.randint(1, 9)
        r = R.choice([R.randint(1, 9), R.randint(10, f - 1) if f > 10 else R.randint(1, 9)])
        if f >= 1000 and R.random() < 0.4:
            r = R.randint(10, 99)
        v = g * f + r
        if R.random() < 0.5:
            ans = komma(v, f, big)
            w = [falsche_komma(v, f, big), komma(v * 10, f, big) if v * 10 % f else None, komma(r * f + g, f, big) if r < 10 else None,
                 "%s,%s%s%s" % (g, str(r).rjust(stellen(f), "0")[::-1], NB, big)]
            q = "Schreibe mit Komma: %s = ? %s" % (zwei(v, f, big, small), big)
            e = "1 %s = %s %s. Hinter dem Komma %s %s: %s = <b>%s</b>." % (big, num(f), small, "steht" if stellen(f) == 1 else "stehen", st(f), zwei(v, f, big, small), ans)
        else:
            ans = zwei(v, f, big, small)
            fk = falsche_komma(v, f, big)
            w = [zwei(g * f + r * 10, f, big, small) if r * 10 < f else None, "%d%s%s %d%s%s" % (g, NB, big, r * (10 ** (stellen(f) - len(str(r)))), NB, small),
                 zwei((g + 1) * f + r, f, big, small)]
            q = "%s = ?" % komma(v, f, big)
            e = "Vor dem Komma stehen die %s, dahinter die %s (%s): <b>%s</b>." % (big, small, st(f), ans)
        return mcq(q, ans, [x for x in w if x and x != ans], e)
    return mk


def kleiner(R, f, big, small):
    def mk():
        g = R.randint(1, 9)
        r = R.randint(1, f - 1)
        if f >= 100 and R.random() < 0.5:
            r = r // (f // 10) * (f // 10) or f // 10
        v = g * f + r
        txt = komma(v, f, big)
        w = [v // 10 if v % 10 == 0 else v + f, int(txt.split(",")[0].replace(NB, "")) * f + int(txt.split(",")[1].split(NB)[0].rstrip("0") or 0) if "," in txt else v + 1,
             v * 10, v + f]
        return mcq("%s = ? %s" % (txt, small), u(v, small), [u(x, small) for x in w if x != v and x > 0],
                   "1 %s = %s %s. %s = %s + %s = <b>%s</b>." % (big, num(f), small, txt, u(g * f, small), u(r, small), u(v, small)))
    return mk


def groesser(R, f, big, small):
    def mk():
        v = R.randint(f + 1, 9 * f + f - 1)
        if v % f == 0:
            return None
        ans = komma(v, f, big)
        w = [falsche_komma(v, f, big), komma(v * 10, f, big) if (v * 10) % f else u(v * 10 // f, big), komma(v // 10, f, big) if v // 10 > 0 else None,
             "%s,%s%s%s" % (num(v // f + 1), str(v % f).rjust(stellen(f), "0"), NB, big)]
        return mcq("%s = ? %s" % (u(v, small), big), ans, [x for x in w if x and x != ans],
                   "%s %s = 1 %s. %s = %s = <b>%s</b>." % (num(f), small, big, u(v, small), zwei(v, f, big, small), ans))
    return mk


def rechnen(R, f, big, small):
    def mk():
        kind = R.choice(["plus", "minus", "vergleich", "rest1"])
        if kind == "plus":
            a, b = R.randint(f // 2, 5 * f), R.randint(f // 10, 3 * f)
            a, b = a // (f // 10 or 1) * (f // 10 or 1), b // (f // 10 or 1) * (f // 10 or 1)
            if not a or not b:
                return None
            r = a + b
            q = "%s + %s = ?" % (komma(a, f, big), u(b, small))
            w = [r + f, a + b // f if b >= f else r - f // 10 if r > f // 10 else r + f // 10, r + f // 10, a + b * 10]
            return mcq(q, komma(r, f, big), [komma(x, f, big) for x in w if x > 0 and x != r],
                       "In %s umrechnen: %s + %s = %s = <b>%s</b>." % (small, u(a, small), u(b, small), u(r, small), komma(r, f, big)))
        if kind == "minus":
            a = R.randint(2, 9) * f
            b = R.randint(f // 10 or 1, a - 1)
            b = b // (f // 10 or 1) * (f // 10 or 1) or f // 10 or 1
            r = a - b
            q = "%s − %s = ?" % (u(a // f, big), u(b, small))
            w = [a // f * f - b // 10 if b // 10 else r + 1, r + f, r - f // 10 if r > f // 10 else r + 2 * (f // 10 or 1), a // f - b if a // f > b else r + f // 10]
            return mcq(q, komma(r, f, big), [komma(x, f, big) for x in w if x > 0 and x != r],
                       "%s = %s. %s − %s = %s = <b>%s</b>." % (u(a // f, big), u(a, small), u(a, small), u(b, small), u(r, small), komma(r, f, big)))
        if kind == "vergleich":
            a = R.randint(f + 1, 5 * f)
            b = a + R.choice([-1, 1]) * R.randint(1, f // 2 if f > 2 else 1)
            if a == b or b <= 0:
                return None
            big_one = komma(a, f, big) if a > b else u(b, small)
            q = "Was ist mehr: %s oder %s?" % (komma(a, f, big), u(b, small))
            other = u(b, small) if a > b else komma(a, f, big)
            return mcq(q, big_one, [other, "Beides ist gleich viel", "Das kann man nicht vergleichen"],
                       "In %s: %s = %s. Mehr ist <b>%s</b>." % (small, komma(a, f, big), u(a, small), big_one))
        g = R.randint(1, 4)
        x = R.randint(1, f - 1)
        x = x // (f // 10 or 1) * (f // 10 or 1) or (f // 10 or 1)
        r = f - x
        q = "Wie viel fehlt von %s bis %s?" % (komma(g * f + x, f, big), u(g + 1, big))
        w = [x, r + (f // 10 or 1), f - r // 10 if r // 10 else r + 2, r * 10 if r * 10 < f else r + 2 * (f // 10 or 1)]
        return mcq(q, u(r, small), [u(v, small) for v in w if v > 0 and v != r],
                   "%s = %s. Bis %s = %s fehlen <b>%s</b>." % (komma(g * f + x, f, big), u(g * f + x, small), u(g + 1, big), u((g + 1) * f, small), u(r, small)))
    return mk
