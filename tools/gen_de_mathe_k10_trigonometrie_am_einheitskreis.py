# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 10: Trigonometrie am Einheitskreis（Leitidee Raum und Form, Sek I）
  python3 tools/gen_de_mathe_k10_trigonometrie_am_einheitskreis.py
P(cos α | sin α) am Einheitskreis, exakte Werte für 0°, 30°, 45°, 60°, 90° und ihre Vielfachen, Vorzeichen in den Quadranten,
Beziehungen sin(180° − α) = sin α, cos(180° − α) = −cos α, sin² α + cos² α = 1, tan α = sin α : cos α,
Winkel zu gegebenem Sinus- oder Kosinuswert (zwei Lösungen zwischen 0° und 360°), Riesenrad-Aufgaben.
Fehler: sin und cos vertauscht, Vorzeichen im 2. bis 4. Quadranten vergessen, nur eine Lösung angegeben, sin² α + cos² α = 1 nicht genutzt.
"""
import random, math
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, num, wrap, line, text, INK, RED, BLUE, GREEN
from de_k6 import bh, dz
from de_k8 import GRID
from de_k10 import mcq, zr

R = random.Random(50007)
M = "−"
H = "½"
# exakte Werte für Winkel im 1. Quadranten: (sin, cos)
EX = {0: ("0", "1"), 30: (H, H + "√3"), 45: (H + "√2", H + "√2"), 60: (H + "√3", H), 90: ("1", "0")}
ANG = [a for a in range(0, 361, 30)] + [45, 135, 225, 315]
ANG = sorted(set(ANG))


def neg(s):
    return s if s == "0" else (s[1:] if s.startswith(M) else M + s)


def exakt(a):
    """(sin, cos) als Text"""
    a %= 360
    if a <= 90:
        return EX[a]
    if a <= 180:
        s, c = EX[180 - a]
        return s, neg(c)
    if a <= 270:
        s, c = EX[a - 180]
        return neg(s), neg(c)
    s, c = EX[360 - a]
    return neg(s), c


def wert(t):
    return {"0": 0.0, "1": 1.0, H: 0.5, H + "√2": math.sqrt(2) / 2, H + "√3": math.sqrt(3) / 2}[t.lstrip(M)] * (-1 if t.startswith(M) else 1)


def ekreis(a, zeige=True, label="Einheitskreis"):
    W = Hh = 290
    c, r = 145, 105
    s = [line(c - r - 18, c, c + r + 22, c, INK, 2) + line(c, c + r + 18, c, c - r - 22, INK, 2),
         text(c + r + 18, c - 8, "x", 16, italic=True), text(c + 12, c - r - 12, "y", 16, italic=True),
         "<circle cx='%d' cy='%d' r='%d' fill='none' stroke='%s' stroke-width='2.4'/>" % (c, c, r, BLUE),
         text(c + r + 4, c + 20, "1", 15, weight=600), text(c - r - 8, c + 20, M + "1", 15, weight=600),
         text(c - 12, c - r + 4, "1", 15, weight=600, anchor="end"), text(c - 12, c + r + 4, M + "1", 15, weight=600, anchor="end")]
    x = c + r * math.cos(math.radians(a))
    y = c - r * math.sin(math.radians(a))
    rr = 26
    s.append("<path d='M%d %d A%d %d 0 %d 0 %.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>" % (c + rr, c, rr, rr, 1 if a > 180 else 0, c + rr * math.cos(math.radians(a)), c - rr * math.sin(math.radians(a)), RED))
    ta = math.radians(a / 2)
    s.append(text(c + 48 * math.cos(ta), c - 48 * math.sin(ta) + 6, "α", 17, col=RED, italic=True, weight=700))
    s.append(line(c, c, x, y, INK, 2.2))
    if zeige:
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%d' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>" % (x, y, x, c, GREEN))
        s.append("<line x1='%.1f' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>" % (x, y, c, y, GREEN))
    s.append("<circle cx='%.1f' cy='%.1f' r='5.5' fill='%s'/>" % (x, y, RED))
    dx = 12 if math.cos(math.radians(a)) >= -0.1 else -12
    s.append(text(x + dx, y - 10 if math.sin(math.radians(a)) >= 0 else y + 22, "P", 17, col=RED, weight=700, anchor="start" if dx > 0 else "end"))
    return wrap(W, Hh, "".join(s), label, lg=True)


def punkt():
    a = R.choice([v for v in ANG if v % 90 != 0] + [90, 180, 270])
    sn, cs = exakt(a)
    ans = "P(%s | %s)" % (cs, sn)
    w = ["P(%s | %s)" % (sn, cs) if sn != cs else "P(%s | %s)" % (neg(cs), sn), "P(%s | %s)" % (neg(cs), sn) if cs != "0" else "P(%s | %s)" % (cs, neg(sn)), "P(%s | %s)" % (cs, neg(sn)) if sn != "0" else "P(%s | %s)" % (neg(sn), cs)]
    if R.random() < 0.6:
        return mcq(ekreis(a, label="Einheitskreis mit Punkt P zum Winkel %d Grad" % a) + "Der Punkt P gehört zum Winkel α = %d°. Welche Koordinaten hat P?" % a, ans, w,
                   "P = (cos α | sin α) = <b>%s</b>." % ans)
    t = R.choice(["sin", "cos"])
    v = sn if t == "sin" else cs
    o = cs if t == "sin" else sn
    return mcq(ekreis(a, label="Einheitskreis mit Punkt P zum Winkel %d Grad" % a) + "Wie groß ist %s %d°? Lies am Einheitskreis ab." % (t, a), v,
               [o if o != v else neg(v), neg(v) if v != "0" else "1", "1" if v not in ("1", M + "1") and o != "1" else (H if v != H else M + H)],
               "%s α ist die %s-Koordinate von P: <b>%s</b>." % (t, "y" if t == "sin" else "x", v))


def exakte():
    a = R.choice([v for v in ANG if v not in (0, 360)])
    t = R.choice(["sin", "cos", "sin", "cos", "tan"])
    sn, cs = exakt(a)
    if t == "tan":
        if cs == "0":
            return None
        tv = math.tan(math.radians(a))
        tab = {1.0: "1", math.sqrt(3): "√3", 1 / math.sqrt(3): "⅓√3", 0.0: "0"}
        k = [x for x in tab if abs(abs(tv) - x) < 1e-9]
        if not k:
            return None
        ts = tab[k[0]]
        ts = (M + ts) if tv < -1e-9 else ts
        return mcq("Berechne tan %d° exakt." % a, ts, [neg(ts) if ts != "0" else "1", {"1": "√3", "√3": "⅓√3", "⅓√3": "√3", "0": "1"}[ts.lstrip(M)], "nicht definiert" if ts != "nicht definiert" else "0"],
                   "tan α = sin α : cos α = %s : %s = <b>%s</b>." % (sn, cs, ts))
    v = sn if t == "sin" else cs
    o = cs if t == "sin" else sn
    return mcq("Berechne %s %d° exakt." % (t, a), v, [neg(v) if v != "0" else "1", o if o != v and o != neg(v) else ("1" if v.lstrip(M) != "1" else H), (H + "√2") if v.lstrip(M) not in (H + "√2",) and o.lstrip(M) != H + "√2" else (H + "√3" if v.lstrip(M) != H + "√3" else H)],
               "Bezugswinkel im 1. Quadranten bestimmen, dann das Vorzeichen im Quadranten beachten: <b>%s %d° = %s</b>." % (t, a, v))


def vorzeichen():
    kind = R.choice(["q", "w", "w", "zahl"])
    QS = {1: ("+", "+"), 2: ("+", M), 3: (M, M), 4: (M, "+")}
    if kind == "q":
        q = R.randint(1, 4)
        s, c = QS[q]
        txt = "sin α %s 0 und cos α %s 0" % ("&gt;" if s == "+" else "&lt;", "&gt;" if c == "+" else "&lt;")
        return mcq("In welchem Quadranten liegt der Winkel α, wenn %s ist?" % txt, "im %d. Quadranten" % q, ["im %d. Quadranten" % k for k in (1, 2, 3, 4) if k != q],
                   "sin ist die y-, cos die x-Koordinate: <b>%d. Quadrant</b> (%s)." % (q, {1: "0° bis 90°", 2: "90° bis 180°", 3: "180° bis 270°", 4: "270° bis 360°"}[q]))
    a = R.choice([v for v in range(5, 360, 5) if v % 90])
    t = R.choice(["sin", "cos"])
    v = math.sin(math.radians(a)) if t == "sin" else math.cos(math.radians(a))
    if kind == "zahl":
        return mcq("Berechne %s %d° mit dem Taschenrechner (auf vier Nachkommastellen)." % (t, a), zr(v, 4),
                   [zr(-v, 4), zr(math.cos(math.radians(a)) if t == "sin" else math.sin(math.radians(a)), 4), zr(math.sin(a) if t == "sin" else math.cos(a), 4)],
                   "Taschenrechner im Modus DEG: <b>%s %d° ≈ %s</b>." % (t, a, zr(v, 4)))
    ans = "positiv" if v > 0 else "negativ"
    return mcq("Ist %s %d° positiv oder negativ?" % (t, a), ans, ["negativ" if v > 0 else "positiv", "gleich 0", "nicht definiert"],
               "%d° liegt im %d. Quadranten; dort ist %s %s: <b>%s</b>." % (a, a // 90 + 1, t, ans, ans))


def beziehung():
    kind = R.choice(["sup", "sup", "pyth", "pyth", "tan", "neg"])
    if kind == "sup":
        a = R.choice([v for v in range(10, 90, 5) if v not in (30, 45, 60)])
        t = R.choice(["sin", "cos"])
        ans = "%s %d°" % (t, a) if t == "sin" else "%scos %d°" % (M, a)
        return mcq("Welcher Ausdruck ist gleich %s %d°?" % (t, 180 - a), ans,
                   ["%scos %d°" % (M, a) if t == "sin" else "cos %d°" % a, "%s %d°" % ("cos" if t == "sin" else "sin", a), "%ssin %d°" % (M, a) if t == "sin" else "sin %d°" % a],
                   "Spiegelung an der y-Achse: sin(180° − α) = sin α, cos(180° − α) = −cos α. <b>%s</b>" % ans)
    if kind == "pyth":
        tr = R.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (4, 3, 5), (12, 5, 13)])
        s, c = Fr(tr[0], tr[2]), Fr(tr[1], tr[2])
        q = R.choice([1, 2])
        sg = 1 if q == 1 else -1
        cc = sg * c
        st = dz(s) if s.denominator in (5, 25) else bh(s)
        ct = (M if sg < 0 else "") + (dz(c) if c.denominator in (5, 25) else bh(c))
        return mcq("Es ist sin α = %s und α liegt im %d. Quadranten. Wie groß ist cos α?" % (st, q), ct,
                   [((M if sg > 0 else "") + (dz(c) if c.denominator in (5, 25) else bh(c))), (dz(1 - s) if (1 - s).denominator in (5, 25) else bh(1 - s)), (dz(1 - s * s) if (1 - s * s).denominator in (5, 25) else bh(1 - s * s))],
                   "sin² α + cos² α = 1 ⇒ cos² α = 1 − %s² = %s. Im %d. Quadranten ist cos α %s: <b>%s</b>." % ("(%s)" % st, bh(c * c), q, "positiv" if sg > 0 else "negativ", ct))
    if kind == "tan":
        tr = R.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (4, 3, 5)])
        s, c = Fr(tr[0], tr[2]), Fr(tr[1], tr[2])
        t = s / c
        f = lambda v: dz(v) if v.denominator in (1, 2, 4, 5, 8, 10, 20, 25) else bh(v)
        return mcq("Für einen spitzen Winkel α gilt sin α = %s und cos α = %s. Wie groß ist tan α?" % (f(s), f(c)), f(t), [f(c / s), f(s * c), f(s + c) if s + c != t else f(c - s)],
                   "tan α = sin α : cos α = %s : %s = <b>%s</b>." % (f(s), f(c), f(t)))
    a = R.choice([20, 35, 40, 50, 70, 25])
    t = R.choice(["sin", "cos"])
    ans = ("%ssin %d°" % (M, a)) if t == "sin" else "cos %d°" % a
    return mcq("Welcher Ausdruck ist gleich %s %d°?" % (t, 360 - a), ans, [("sin %d°" % a) if t == "sin" else ("%scos %d°" % (M, a)), "%s%s %d°" % (M, "cos" if t == "sin" else "sin", a), "%s %d°" % ("cos" if t == "sin" else "sin", a)],
               "Spiegelung an der x-Achse: sin(360° − α) = −sin α, cos(360° − α) = cos α. <b>%s</b>" % ans)


def winkel():
    kind = R.choice(["ex", "ex", "tr", "tr"])
    if kind == "ex":
        t = R.choice(["sin", "cos"])
        cand = [(a, exakt(a)[0 if t == "sin" else 1]) for a in ANG if a < 360]
        v = R.choice(sorted(set(c for _, c in cand) - {"0", "1", M + "1"}))
        sol = sorted(a for a, c in cand if c == v)
        ans = "α = %d° oder α = %d°" % tuple(sol)
        oth = sorted(a for a, c in cand if c == neg(v))
        b0 = sol[0]
        w = ["nur α = %d°" % b0, "α = %d° oder α = %d°" % tuple(oth), "α = %d° oder α = %d°" % (b0, b0 + 180 if b0 + 180 < 360 else b0 - 180) if (b0 + 180) % 360 not in sol else "α = %d° oder α = %d°" % (b0, 360 - b0)]
        return mcq("Für welche Winkel zwischen 0° und 360° gilt %s α = %s?" % (t, v), ans, w,
                   "Am Einheitskreis gibt es zwei Punkte mit %s-Koordinate %s: <b>%s</b>." % ("y" if t == "sin" else "x", v, ans))
    t = R.choice(["sin", "cos"])
    v = Fr(R.choice([1, 2, 3, 4, 6, 7, 8, 9]), 10) * R.choice([1, -1])
    if t == "sin":
        b = math.degrees(math.asin(float(v)))
        sol = sorted([(180 - b) % 360, b % 360])
    else:
        b = math.degrees(math.acos(float(v)))
        sol = sorted([b, 360 - b])
    ans = "α ≈ %s° oder α ≈ %s°" % (zr(sol[0], 1), zr(sol[1], 1))
    w = ["nur α ≈ %s°" % zr(sol[0], 1), "α ≈ %s° oder α ≈ %s°" % (zr(sol[0], 1), zr((sol[0] + 180) % 360, 1)) if abs((sol[0] + 180) % 360 - sol[1]) > 0.5 else "α ≈ %s° oder α ≈ %s°" % (zr(sol[0], 1), zr(360 - sol[0], 1)),
         "α ≈ %s° oder α ≈ %s°" % (zr(sol[0] + 90, 1), zr(sol[1] + 90 if sol[1] + 90 < 360 else sol[1] - 90, 1))]
    return mcq("Löse %s α = %s für 0° ≤ α &lt; 360° (auf eine Nachkommastelle)." % (t, dz(v) if v > 0 else M + dz(-v)), ans, w,
               "Taschenrechner: %s<sup>−1</sup>(%s) ≈ %s°. %s <b>%s</b>" % (t, dz(v) if v > 0 else M + dz(-v), zr(b, 1), "Zweite Lösung 180° − α." if t == "sin" else "Zweite Lösung 360° − α.", ans))


def riesenrad():
    r = R.choice([10, 12, 15, 20, 25, 30])
    h0 = r + R.choice([2, 3, 5])
    a = R.choice([v for v in range(10, 360, 10) if v % 90])
    hv = h0 + r * math.sin(math.radians(a))
    kind = R.choice(["h", "h", "x"])
    if kind == "h":
        return mcq("Ein Riesenrad hat den Radius %d m; seine Achse ist %d m über dem Boden. Eine Gondel hat sich von der rechten waagerechten Position aus um %d° gegen den Uhrzeigersinn gedreht. Wie hoch ist sie über dem Boden (auf eine Nachkommastelle)?" % (r, h0, a),
                   "≈ %s m" % zr(hv, 1), ["≈ %s m" % zr(h0 + r * math.cos(math.radians(a)), 1), "≈ %s m" % zr(r * math.sin(math.radians(a)), 1), "≈ %s m" % zr(h0 - r * math.sin(math.radians(a)), 1)],
                   "h = %d + %d %s sin %d° ≈ <b>%s m</b>." % (h0, r, MAL, a, zr(hv, 1)))
    xv = r * math.cos(math.radians(a))
    return mcq("Ein Riesenrad hat den Radius %d m. Wie weit ist eine Gondel nach einer Drehung um %d° (von der rechten waagerechten Position, gegen den Uhrzeigersinn) waagerecht von der Achse entfernt (auf eine Nachkommastelle)?" % (r, a),
               "≈ %s m" % zr(abs(xv), 1), ["≈ %s m" % zr(abs(r * math.sin(math.radians(a))), 1), "≈ %s m" % zr(r - abs(xv), 1), "≈ %s m" % zr(r * abs(math.cos(a)), 1)],
               "Waagerechter Abstand |%d %s cos %d°| ≈ <b>%s m</b>." % (r, MAL, a, zr(abs(xv), 1)))


def main():
    seen = set()
    sets = [
        ("Punkte am Einheitskreis", mix(R, seen, [(punkt, 20)])),
        ("Exakte Werte", mix(R, seen, [(exakte, 20)])),
        ("Vorzeichen und Taschenrechner", mix(R, seen, [(vorzeichen, 20)])),
        ("Beziehungen", mix(R, seen, [(beziehung, 20)])),
        ("Winkel bestimmen und Riesenrad", mix(R, seen, [(winkel, 10), (riesenrad, 10)])),
    ]
    body = lesson(
        ["Am <b>Einheitskreis</b> (Radius 1) gehört zu jedem Winkel α ein Punkt P(cos α | sin α). cos α ist die x-Koordinate, sin α die y-Koordinate.",
         "So sind sin und cos für alle Winkel von 0° bis 360° erklärt. Die Vorzeichen hängen vom Quadranten ab.",
         "Es gilt sin² α + cos² α = 1, tan α = sin α : cos α, sin(180° − α) = sin α und cos(180° − α) = −cos α.",
         "Zu einem Sinuswert gibt es zwischen 0° und 360° meist zwei Winkel: α und 180° − α. Beim Kosinus: α und 360° − α."],
        [example("sin 150°", ["Bezugswinkel 30°", "2. Quadrant: sin positiv"], "½"),
         example("sin α = 0,5", ["α = 30°", "180° − 30° = 150°"], "α = 30° oder α = 150°")],
        [["cos 120° = ½", "2. Quadrant: cos 120° = −½"],
         ["P(sin α | cos α)", "P(cos α | sin α)"],
         ["sin α = 0,5 ⇒ nur α = 30°", "auch α = 150°"]])
    faq = [
        {"q": "Was zeigt der Einheitskreis?", "a": "Ein Kreis mit Radius 1. Der Punkt zum Winkel α hat die Koordinaten (cos α | sin α)."},
        {"q": "Wann ist der Kosinus negativ?", "a": "Im 2. und 3. Quadranten, also für Winkel zwischen 90° und 270°."},
        {"q": "Wie viele Winkel haben den Sinus 0,5?", "a": "Zwischen 0° und 360° zwei: 30° und 150°."},
        {"q": "Wie hängen sin und cos zusammen?", "a": "sin² α + cos² α = 1 – das ist der Satz des Pythagoras am Einheitskreis."},
    ]
    make_unit(R, "trigonometrie-am-einheitskreis", "R",
              "Die Schülerinnen und Schüler erweitern Sinus und Kosinus am Einheitskreis auf Winkel bis 360°, nutzen exakte Werte, Vorzeichen und Beziehungen und bestimmen Winkel zu gegebenen Werten (Zusammenfassung).",
              "Trigonometrie am Einheitskreis",
              "Einheitskreis Klasse 10 – Sinus und Kosinus bis 360°, exakte Werte, Arbeitsblätter mit Lösungen",
              "Einheitskreis",
              "Trigonometrie am Einheitskreis für Klasse 10: Punkte P(cos α | sin α), exakte Werte, Vorzeichen in den Quadranten, Beziehungen und Winkel bestimmen. 100 Aufgaben mit Lösungen, kostenlos.",
              "P(cos α | sin α)",
              "sin² α + cos² α = 1",
              body, faq, sets, 7, grade="klasse-10")


if __name__ == "__main__":
    main()
