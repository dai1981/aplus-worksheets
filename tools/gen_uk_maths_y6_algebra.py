# -*- coding: utf-8 -*-
"""
UK Year 6 Maths: Algebra (National Curriculum in England)
  python3 tools/gen_uk_maths_y6_algebra.py
Every answer is checked in code. HTML attributes use single quotes (no backslashes in the JSON).
Wrong answers come from real mistakes: reading 3n as 34 when n = 4, working in the wrong order
(3m − 5 = 25 gives 6 2/3 or 20), using the first term or the difference the wrong way round in a
sequence, swapping the two unknowns, and missing a combination.
"""
import json, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
BLUE = "#2f6fb0"
FILL = "#cfe6d6"
GREY = "#8a8a8a"
RED = "#c0392b"
INK = "#2b2b2b"
ORANGE = "#d9822b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
MINUS = "−"


# ------------------------------------------------------------ text helpers
def n(x):
    """1,000 and above get a comma; negatives use the real minus sign."""
    return (MINUS if x < 0 else "") + "{:,}".format(abs(x))


def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def show(v):
    """Exact text for a Fraction: whole, terminating decimal (1 dp or 2 dp) or mixed number."""
    v = Fr(v)
    if v.denominator == 1:
        return n(v.numerator)
    for dp in (1, 2):
        if (v * 10 ** dp).denominator == 1:
            return ("%." + str(dp) + "f") % float(v)
    w, r = divmod(v.numerator, v.denominator)
    return (n(w) + " " if w else "") + fr(r, v.denominator)


def gbp(p):
    """Money in pence -> 45p, £3, £3.50."""
    if p < 100:
        return "%dp" % p
    if p % 100 == 0:
        return "£%d" % (p // 100)
    return "£%d.%02d" % divmod(p, 100)


def E(s):
    """Plain maths text -> HTML with the letters in italics: '3n + 1' -> 3<i>n</i> + 1."""
    s = s.replace("-", MINUS)
    return re.sub(r"(?<![A-Za-z])([A-Za-z])(?![A-Za-z])", r"<i>\1</i>", s)


def B(s):
    return "<b>%s</b>" % s


# ------------------------------------------------------------ choices
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {re.sub(r"<[^>]+>", "", correct)}
    pick = []
    for c in cands:
        c = str(c)
        k = re.sub(r"<[^>]+>", "", c)
        if k in seen or not c:
            continue
        seen.add(k)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


class People:
    def __init__(self, rnd):
        self.pool = [(x, "she", "her") for x in GIRLS] + [(x, "he", "his") for x in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def pair(xn, x, yn, y):
    return "%s, %s" % (E("%s = %s" % (xn, n(x))), E("%s = %s" % (yn, n(y))))


# ------------------------------------------------------------ pictures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=18, col=INK, anchor="middle", weight="700", italic=False):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, weight, col, anchor, " font-style='italic'" if italic else "", t))


def tw(t, fs):
    return len(str(t)) * fs * 0.6


ARROW = ("<defs><marker id='ah' viewBox='0 0 10 10' refX='8' refY='5' markerWidth='6' markerHeight='6' orient='auto'>"
         "<path d='M0 0 L10 5 L0 10 z' fill='%s'/></marker></defs>" % INK)


def machine_svg(inp, ops, out):
    """Function machine: input -> [op] -> [op] -> output. inp/out may be '?'."""
    bh, gap, y = 40, 30, 8
    parts = [("v", inp)] + [("o", o) for o in ops] + [("v", out)]
    ws = [max(46, int(tw(t, 18)) + 22) if k == "v" else max(64, int(tw(t, 18)) + 24) for k, t in parts]
    x = 4
    s = [ARROW]
    for i, ((k, t), w) in enumerate(zip(parts, ws)):
        if k == "o":
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='4' fill='%s' stroke='%s' stroke-width='2'/>" % (x, y, w, bh, FILL, GREEN))
            s.append(text(x + w / 2, y + 27, t, 18, GREEN))
        else:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='20' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (x, y, w, bh, INK))
            s.append(text(x + w / 2, y + 27, t, 20, RED if t == "?" else INK, italic=t.isalpha()))
        x += w
        if i < len(parts) - 1:
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2' marker-end='url(#ah)'/>"
                     % (x + 3, y + bh / 2, x + gap - 4, y + bh / 2, INK))
            x += gap
    return svg_wrap(x + 4, y + bh + 8, "".join(s),
                    "function machine: %s, %s, %s" % (inp, ", then ".join(ops), out))


def seq_svg(terms, steps=None):
    """Terms in boxes; '?' in red. steps: labels drawn over the jumps (e.g. '+7')."""
    bw = max(50, max(int(tw(t, 20)) + 18 for t in terms))
    gap = 18
    top = 40 if steps else 6
    s = []
    for i, t in enumerate(terms):
        x = 4 + i * (bw + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='40' rx='4' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, top, bw, "#ffffff" if t == "?" else FILL, GREEN))
        s.append(text(x + bw / 2, top + 27, t, 20, RED if t == "?" else INK))
        if steps and i < len(terms) - 1:
            x0, x1 = x + bw / 2 + 6, x + bw + gap + bw / 2 - 6
            s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                     % (x0, top - 2, (x0 + x1) / 2, top - 22, x1, top - 2, BLUE))
            s.append(text((x0 + x1) / 2, top - 20, steps[i], 15, BLUE))
    W = 8 + len(terms) * bw + (len(terms) - 1) * gap
    return svg_wrap(W, top + 46, "".join(s), "number sequence: " + ", ".join(terms))


def sticks_svg(k_max=3):
    """Matchstick squares in a row: pattern 1, 2, 3."""
    u, gap = 30, 34
    s = []
    x = 6
    for k in range(1, k_max + 1):
        y = 8
        slot = max(k * u, 70)
        x0 = x
        x = x0 + (slot - k * u) / 2
        for j in range(k + 1):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='4' stroke-linecap='round'/>"
                     % (x + j * u, y, x + j * u, y + u, ORANGE))
        for j in range(k):
            for yy in (y, y + u):
                s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='4' stroke-linecap='round'/>"
                         % (x + j * u, yy, x + (j + 1) * u, yy, ORANGE))
        s.append(text(x0 + slot / 2, y + u + 24, "Pattern %d" % k, 14, INK, weight="400"))
        x = x0 + slot + gap
    return svg_wrap(int(x - gap + 6), 70, "".join(s), "matchstick patterns 1 to %d: rows of squares" % k_max)


def tables_svg(k_max=3):
    """Tables pushed together in a row: 2 seats on each long side of a table, 1 at each end (4n + 2)."""
    u, TH, gap, r = 44, 30, 26, 7
    s = []
    x = 6 + 2 * r + 2
    y = 8 + 2 * r + 2
    for k in range(1, k_max + 1):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (x, y, k * u, TH, FILL, GREEN))
        for j in range(1, k):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>" % (x + j * u, y, x + j * u, y + TH, GREEN))
        seats = 0
        for j in range(k):
            for yy in (y - r - 3, y + TH + r + 3):
                for xx in (x + j * u + u / 4, x + j * u + 3 * u / 4):
                    s.append("<circle cx='%.1f' cy='%d' r='%d' fill='%s'/>" % (xx, yy, r, BLUE))
                    seats += 1
        for xx in (x - r - 3, x + k * u + r + 3):
            s.append("<circle cx='%d' cy='%d' r='%d' fill='%s'/>" % (xx, y + TH / 2, r, BLUE))
            seats += 1
        assert seats == 4 * k + 2
        s.append(text(x + k * u / 2, y + TH + 2 * r + 24, "%d table%s" % (k, "" if k == 1 else "s"), 14, INK, weight="400"))
        x += k * u + (r + 3 + r) * 2 + gap
    W = x - gap - (r + 3 + r) + 6
    return svg_wrap(W, y + TH + 2 * r + 30, "".join(s), "tables in a row with chairs: 1, 2 and 3 tables")


def shape(kind, cx, cy, s=15):
    if kind == "tri":
        return "<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2'/>" % (
            cx, cy - s, cx + s, cy + s * 0.8, cx - s, cy + s * 0.8, "#f4c7a1", ORANGE)
    if kind == "cir":
        return "<circle cx='%.1f' cy='%.1f' r='%d' fill='#c9dcf2' stroke='%s' stroke-width='2'/>" % (cx, cy, s, BLUE)
    return "<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (
        cx - s, cy - s, 2 * s, 2 * s, FILL, GREEN)


NAMES = {"tri": "triangle", "cir": "circle", "sq": "square"}


def shapes_svg(rows):
    """rows: lists of tokens: 'tri', 'cir', 'sq' or text ('+', '=', '20')."""
    rh = 44
    s = []
    W = 0
    for r, row in enumerate(rows):
        x = 6
        cy = 6 + r * rh + rh / 2
        for t in row:
            if t in NAMES:
                s.append(shape(t, x + 16, cy))
                x += 32
            else:
                w = max(22, tw(t, 20) + 8)
                s.append(text(x + w / 2, cy + 7, t, 20))
                x += w
            x += 6
        W = max(W, x)
    lab = "; ".join(" ".join(NAMES.get(t, t) for t in row) for row in rows)
    return svg_wrap(int(W) + 6, len(rows) * rh + 12, "".join(s), "shape puzzle: " + lab)


def rect_svg(lt, wt, square=False):
    L, H = (70, 70) if square else (120, 64)
    x0, y0 = 10, 10
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x0, y0, L, H, FILL, GREEN),
         text(x0 + L / 2, y0 + H + 22, lt, 16),
         text(x0 + L + 8, y0 + H / 2 + 6, wt, 16, anchor="start")]
    W = int(x0 + L + 8 + tw(wt, 16) + 8)
    return svg_wrap(W, y0 + H + 30, "".join(s), ("square" if square else "rectangle") + " %s by %s" % (lt, wt))


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and every number can be read."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ set 1: use simple formulae
def set_formulae(P):
    its = []

    def ev(expr, env):
        return Fr(eval(expr, {}, {k: Fr(v) for k, v in env.items()}))

    # 1 3n, n = 4
    assert ev("3*n", {"n": 4}) == 12
    its.append(mcq("If %s, what is the value of %s?" % (E("n = 4"), B(E("3n"))), 12, [34, 7, 1],
                   "%s means 3 × %s. So 3 × 4 = <b>12</b>. It does not mean 34: the 3 and the %s are multiplied, not written side by side."
                   % (E("3n"), E("n"), E("n"))))
    # 2 y - 4
    its.append(mcq("If %s, what is %s?" % (E("y = 9"), B(E("y - 4"))), 5, [13, 36, 94],
                   "Replace %s with 9: 9 %s 4 = <b>5</b>. (13 adds instead of subtracting.)" % (E("y"), MINUS)))
    # 3 xy
    assert ev("x*y", {"x": 4, "y": 7}) == 28
    its.append(mcq("If %s and %s, what is %s?" % (E("x = 4"), E("y = 7"), B(E("xy"))), 28, [47, 11, 3],
                   "%s means %s × %s. So 4 × 7 = <b>28</b>. Not 47 (side by side) and not 11 (adding)." % (E("xy"), E("x"), E("y"))))
    # 4 2a + 5
    assert ev("2*a+5", {"a": 6}) == 17
    its.append(mcq("If %s, what is %s?" % (E("a = 6"), B(E("2a + 5"))), 17, [31, 22, 13],
                   "Multiply first: 2 × 6 = 12. Then add 5: 12 + 5 = <b>17</b>. Not 31: 2%s is not 26. Not 22: that adds 6 + 5 first."
                   % E("a")))
    # 5 4m - 3
    assert ev("4*m-3", {"m": 5}) == 17
    its.append(mcq("If %s, what is %s?" % (E("m = 5"), B(E("4m - 3"))), 17, [42, 8, 6],
                   "4 × 5 = 20, then 20 %s 3 = <b>17</b>. Not 42: 4%s is not 45. Not 8: that subtracts first, 4 × 2." % (MINUS, E("m"))))
    # 6 k / 2 + 3
    assert ev("k/2+3", {"k": 8}) == 7
    its.append(mcq("If %s, what is %s?" % (E("k = 8"), B(E("k ÷ 2 + 3"))), 7, ["1.6", 4, 13],
                   "Divide first: 8 ÷ 2 = 4. Then add 3: 4 + 3 = <b>7</b>. Not 1.6: that adds 2 + 3 first. Not 4: it forgets to add 3."))
    # 7 20 - 2p
    assert ev("20-2*p", {"p": 7}) == 6
    its.append(mcq("If %s, what is %s?" % (E("p = 7"), B(E("20 - 2p"))), 6, [126, 13, 11],
                   "Multiply first: 2 × 7 = 14. Then 20 %s 14 = <b>6</b>. Not 126: that does 20 %s 2 = 18 first, then 18 × 7."
                   % (MINUS, MINUS)))
    # 8 square perimeter
    its.append(mcq(fig(rect_svg("9 cm", "9 cm", True)) + "The perimeter of a square is %s, where %s is the length of a side. "
                   "What is the perimeter of this square?" % (B(E("P = 4s")), E("s")),
                   "36 cm", ["81 cm", "13 cm", "49 cm"],
                   "Replace %s with 9: 4 × 9 = <b>36 cm</b>. 81 cm multiplies 9 × 9, which is how you find the area. "
                   "13 cm adds 4 + 9. 49 cm reads 4%s as 49." % (E("s"), E("s"))))
    # 9 rectangle area
    its.append(mcq(fig(rect_svg("8 cm", "6 cm")) + "The area of a rectangle is %s. What is the area of this rectangle?" % B(E("A = lw")),
                   "48 cm²", ["28 cm²", "14 cm²", "86 cm²"],
                   "%s means %s × %s: 8 × 6 = <b>48 cm²</b>. 28 is the perimeter (8 + 6 + 8 + 6) and 14 only adds 8 + 6."
                   % (E("lw"), E("l"), E("w"))))
    # 10 rectangle perimeter
    assert 2 * (7 + 3) == 20
    its.append(mcq("The perimeter of a rectangle is %s. Find %s when %s cm and %s cm." % (B(E("P = 2(l + w)")), E("P"), E("l = 7"), E("w = 3")),
                   "20 cm", ["17 cm", "10 cm", "21 cm"],
                   "Work out the brackets first: 7 + 3 = 10. Then 2 × 10 = <b>20 cm</b>. 17 cm doubles only the 7. 21 cm is 7 × 3."))
    # 11 metres to centimetres
    its.append(mcq("To change metres to centimetres, use %s, where %s is centimetres and %s is metres. How many centimetres are in 7 metres?"
                   % (B(E("c = 100m")), E("c"), E("m")), 700, [107, 70, n(7000)],
                   "100 × 7 = <b>700</b>. There are 100 cm in 1 m. 107 adds, 70 multiplies by 10 and 7,000 multiplies by 1,000."))
    # 12 legs
    its.append(mcq("A farmer uses %s to count the legs %s on %s cows. How many legs do 12 cows have?" % (B(E("L = 4c")), E("L"), E("c")),
                   48, [412, 16, 3],
                   "4%s means 4 × %s. 4 × 12 = <b>48</b>. Not 412: do not write the numbers side by side. Not 16: that adds 4 + 12."
                   % (E("c"), E("c"))))
    # 13 bike hire
    assert 5 * 4 + 3 == 23
    its.append(mcq("Bike hire costs %s pounds, where %s is the number of hours. How much does it cost to hire a bike for 4 hours?"
                   % (B(E("C = 5h + 3")), E("h")), "£23", ["£35", "£12", "£20"],
                   "5 × 4 = 20, then 20 + 3 = <b>£23</b>. £35 adds 4 + 3 first. £20 forgets the £3."))
    # 14 chicken
    assert 40 * 2 + 20 == 100
    its.append(mcq("The time to roast a chicken is %s minutes, where %s is its mass in kg. How long does a 2 kg chicken take?"
                   % (B(E("t = 40w + 20")), E("w")), "100 minutes", ["80 minutes", "62 minutes", "880 minutes"],
                   "40 × 2 = 80, then 80 + 20 = <b>100 minutes</b>. 80 minutes forgets the extra 20. 880 adds 2 + 20 first."))
    # 15 chairs
    assert 2 * 10 + 2 == 22
    its.append(mcq("For a row of %s tables, the number of chairs is %s. How many chairs are needed for 10 tables?"
                   % (E("t"), B(E("c = 2t + 2"))), 22, [24, 14, 20],
                   "2 × 10 = 20, then 20 + 2 = <b>22</b> chairs. 24 adds first: 2 × 12. 20 forgets the 2 chairs at the ends."))
    # 16 which formula
    its.append(mcq("An equilateral triangle has 3 equal sides of length %s. Which formula gives its perimeter %s?" % (E("s"), E("P")),
                   E("P = 3s"), [E("P = s + 3"), E("P = 4s"), E("P = s × s")],
                   "Add the 3 equal sides: %s + %s + %s = 3%s. So <b>%s</b>. %s adds 3 instead of multiplying by 3."
                   % (E("s"), E("s"), E("s"), E("s"), E("P = 3s"), E("s + 3"))))
    # 17 greatest value
    vals = {"50 - 6a": 50 - 24, "a + 21": 25, "6a": 24, "5a": 20}
    assert max(vals, key=vals.get) == "50 - 6a"
    its.append(mcq("When %s, which expression has the <b>greatest</b> value?" % E("a = 4"), E("50 - 6a"),
                   [E("a + 21"), E("6a"), E("5a")],
                   "Work out each one: 50 %s 24 = <b>26</b>, 4 + 21 = 25, 6 × 4 = 24, 5 × 4 = 20. Multiplying does not always give the biggest answer."
                   % MINUS))
    # 18 work backwards: y = 2x + 1, y = 15
    assert (15 - 1) / 2 == 7
    its.append(mcq("%s. What is %s when %s?" % (B(E("y = 2x + 1")), E("x"), E("y = 15")), 7, [31, 8, "6.5"],
                   "2%s + 1 = 15, so 2%s = 14 and %s = <b>7</b>. Check: 2 × 7 + 1 = 15. 31 puts 15 in place of %s. 8 adds 1 instead of subtracting."
                   % (E("x"), E("x"), E("x"), E("x"))))
    # 19 d = 3t, d = 24
    its.append(mcq("%s. What is %s when %s?" % (B(E("d = 3t")), E("t"), E("d = 24")), 8, [72, 21, 27],
                   "3 × %s = 24, so %s = 24 ÷ 3 = <b>8</b>. Not 72: that is 24 × 3. Use the inverse: divide." % (E("t"), E("t"))))
    # 20 two letters
    assert 3 * 5 - 2 * 4 == 7
    its.append(mcq("If %s and %s, what is %s?" % (E("a = 5"), E("b = 4"), B(E("3a - 2b"))), 7, [27, 1, 14],
                   "3 × 5 = 15 and 2 × 4 = 8. Then 15 %s 8 = <b>7</b>. Not 27: 3%s is 15, not 35, so 35 %s 8 is wrong."
                   % (MINUS, E("a"), MINUS)))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 11, 10, 8, 9, 12, 13, 14, 15, 19, 16, 18, 17]
    its = [its[i] for i in order]
    assert len(its) == 20
    return {"title": "Use simple formulae", "items": its}


# ------------------------------------------------------------ set 2: linear number sequences
def seq_terms(a, d, k):
    return [a + d * i for i in range(k)]


def set_sequences(P):
    its = []

    def nt(expr, i):
        return eval(expr, {}, {"n": i})

    # 1 next term
    t = seq_terms(4, 7, 4)
    assert t[-1] + 7 == 32
    its.append(mcq(fig(seq_svg([n(x) for x in t] + ["?"])) + "What is the next term in this sequence?", 32, [31, 33, 39],
                   "The terms go up by 7 each time (11 %s 4 = 7). 25 + 7 = <b>32</b>. 31 and 33 use the wrong step. 39 jumps two steps." % MINUS))
    # 2 decreasing
    t = seq_terms(50, -6, 4)
    assert t == [50, 44, 38, 32]
    its.append(mcq("What is the next term? %s, …" % ", ".join(map(n, t)), 26, [38, 27, 25],
                   "The terms go down by 6 each time. 32 %s 6 = <b>26</b>. 38 adds 6 instead of subtracting." % MINUS))
    # 3 crossing zero
    t = seq_terms(9, -4, 4)
    assert t[-1] - 4 == -7
    its.append(mcq("What is the next term? %s, …" % ", ".join(map(n, t)), n(-7), [n(-1), "7", n(-8)],
                   "Subtract 4 each time. From %s, count back 4 more: <b>%s</b>. %s moves the wrong way past zero."
                   % (n(-3), n(-7), n(-1))))
    # 4 decimals down
    t = [Fr(2), Fr(7, 4), Fr(3, 2), Fr(5, 4)]
    its.append(mcq("What is the next term? %s, …" % ", ".join(show(x) for x in t), "1", ["0.75", "1.05", "1.5"],
                   "The terms go down by 0.25 each time. 1.25 %s 0.25 = <b>1</b>. 1.05 subtracts 0.2 instead of 0.25." % MINUS))
    # 5 rule -> terms
    t = seq_terms(3, 7, 4)
    its.append(mcq("A sequence starts at 3. The rule is <b>add 7</b>. Which shows the first four terms?", ", ".join(map(n, t)),
                   ["7, 10, 13, 16", "10, 17, 24, 31", "7, 14, 21, 28"],
                   "The first term is 3. Then add 7 each time: 3, 10, 17, 24. 7, 10, 13, 16 mixes up the start and the step."))
    # 6 the rule
    its.append(mcq("What is the rule for this sequence? 2.5, 4, 5.5, 7, …", "add 1.5", ["add 2.5", "add 1", "multiply by 2"],
                   "4 %s 2.5 = 1.5, and 5.5 %s 4 = 1.5. The rule is <b>add 1.5</b>. Add 2.5 uses the first term as the step." % (MINUS, MINUS)))
    # 7 4th term from rule
    t = seq_terms(8, 6, 4)
    assert t[3] == 26
    its.append(mcq("The first term of a sequence is 8. The rule is <b>add 6</b>. What is the 4th term?", 26, [32, 24, 14],
                   "8, 14, 20, <b>26</b>. From the 1st term to the 4th term there are only 3 steps: 8 + 3 × 6 = 26. 32 adds 4 steps."))
    # 8 5th term going down
    t = seq_terms(30, -4, 5)
    assert t[4] == 14
    its.append(mcq("The first term of a sequence is 30. The rule is <b>subtract 4</b>. What is the 5th term?", 14, [10, 18, 46],
                   "30, 26, 22, 18, <b>14</b>. There are 4 steps from the 1st to the 5th term: 30 %s 16 = 14. 10 takes 5 steps." % MINUS))
    # 9 missing term
    t = seq_terms(6, 9, 5)
    assert t[2] == 24
    its.append(mcq(fig(seq_svg(["6", "15", "?", "33", "42"])) + "What is the missing term?", 24, [21, 27, 30],
                   "The step is 15 %s 6 = 9. 15 + 9 = <b>24</b>, and 24 + 9 = 33. 21 adds 6 (the first term) instead of the step." % MINUS))
    # 10 which number is in the sequence
    t = seq_terms(3, 4, 12)
    assert 43 in t and 41 not in t and 45 not in t and 40 not in t
    its.append(mcq("The sequence 3, 7, 11, 15, … continues. Which number is in the sequence?", 43, [41, 45, 40],
                   "Every term is 3 more than a multiple of 4 (3, 4 + 3, 8 + 3, …). 40 + 3 = <b>43</b>. 41 and 45 are 1 more than a multiple of 4."))
    # 11 which number down
    t = seq_terms(100, -15, 7)
    assert 55 in t and 60 not in t and 45 not in t and 15 not in t
    its.append(mcq("A sequence starts at 100 and the rule is <b>subtract 15</b>. Which number is in the sequence?", 55, [60, 45, 15],
                   "100, 85, 70, <b>55</b>, 40, 25, 10. The others are not in the list."))
    # 12 matchsticks
    assert [3 * k + 1 for k in (1, 2, 3)] == [4, 7, 10] and 3 * 6 + 1 == 19
    its.append(mcq(fig(sticks_svg()) + "Pattern 1 uses 4 sticks, pattern 2 uses 7 and pattern 3 uses 10. How many sticks are in pattern 6?",
                   19, [22, 16, 24],
                   "Each new square adds 3 sticks: 4, 7, 10, 13, 16, <b>19</b>. 24 is 6 × 4, but squares next to each other share a stick."))
    # 13 nth term: first term
    assert nt("2*n+5", 1) == 7
    its.append(mcq("The %s term of a sequence is %s. What is the first term?" % (E("n") + "th", B(E("2n + 5"))), 7, [5, 2, 25],
                   "Put %s: 2 × 1 + 5 = <b>7</b>. 5 is just the number added; it is not the first term." % E("n = 1")))
    # 14 nth term 10th
    assert nt("3*n+1", 10) == 31
    its.append(mcq("The %s term of a sequence is %s. What is the 10th term?" % (E("n") + "th", B(E("3n + 1"))), 31, [311, 33, 14],
                   "Put %s: 3 × 10 = 30, then 30 + 1 = <b>31</b>. Not 311: 3%s means 3 × %s, not 3 and 10 side by side."
                   % (E("n = 10"), E("n"), E("n"))))
    # 15 nth term 4th
    assert nt("5*n-2", 4) == 18
    its.append(mcq("The %s term of a sequence is %s. What is the 4th term?" % (E("n") + "th", B(E("5n - 2"))), 18, [52, 10, 7],
                   "5 × 4 = 20, then 20 %s 2 = <b>18</b>. Not 52: 5%s is not 54. Not 10: that subtracts first, 5 × 2." % (MINUS, E("n"))))
    # 16 50 - 3n
    assert nt("50-3*n", 5) == 35
    its.append(mcq("The %s term of a sequence is %s. What is the 5th term?" % (E("n") + "th", B(E("50 - 3n"))), 35, [15, 235, 42],
                   "3 × 5 = 15, then 50 %s 15 = <b>35</b>. 15 reads 3%s as 35. 235 does 50 %s 3 first."
                   % (MINUS, E("n"), MINUS)))
    # 17 which sequence 4n
    its.append(mcq("Which sequence has the %s term %s?" % (E("n") + "th", B(E("4n"))), "4, 8, 12, 16",
                   ["4, 5, 6, 7", "0, 4, 8, 12", "5, 9, 13, 17"],
                   "Put %s = 1, 2, 3, 4: 4 × 1 = 4, 4 × 2 = 8, 4 × 3 = 12, 4 × 4 = 16. So <b>4, 8, 12, 16</b>." % E("n")))
    # 18 which nth term 5, 8, 11, 14
    assert [nt("3*n+2", i) for i in range(1, 5)] == [5, 8, 11, 14]
    its.append(mcq("Which %s term gives the sequence 5, 8, 11, 14, …?" % (E("n") + "th"), E("3n + 2"),
                   [E("n + 3"), E("5n + 3"), E("3n + 5")],
                   "The step is 3, so start with 3%s (3, 6, 9, 12). Each term is 2 more, so it is <b>%s</b>. Check: 3 × 1 + 2 = 5. "
                   "%s gives 8 for the first term, not 5." % (E("n"), E("3n + 2"), E("3n + 5"))))
    # 19 which nth term 6, 10, 14, 18
    assert [nt("4*n+2", i) for i in range(1, 5)] == [6, 10, 14, 18]
    its.append(mcq("Which %s term gives the sequence 6, 10, 14, 18, …?" % (E("n") + "th"), E("4n + 2"),
                   [E("n + 4"), E("6n + 4"), E("4n + 6")],
                   "The step is 4, so start with 4%s (4, 8, 12, 16). Each term is 2 more: <b>%s</b>. Check: 4 × 1 + 2 = 6."
                   % (E("n"), E("4n + 2"))))
    # 20 20th term
    t = seq_terms(5, 7, 20)
    assert t[19] == 138
    its.append(mcq("The first term of a sequence is 5. The rule is <b>add 7</b>. What is the 20th term?", 138, [145, 140, 25],
                   "From the 1st term to the 20th term there are 19 steps. 19 × 7 = 133, and 5 + 133 = <b>138</b>. "
                   "145 counts 20 steps. 140 forgets the first term is 5."))
    order = [0, 1, 4, 5, 6, 7, 2, 3, 8, 10, 9, 11, 12, 13, 14, 16, 15, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "Linear number sequences", "items": its}


# ------------------------------------------------------------ set 3: missing numbers with letters
def set_equations(P):
    its = []

    def solve(lhs, rhs, var):
        """Find the whole number or fraction solution by brute force over Fractions (to 1 dp / thirds)."""
        cands = {Fr(k, d) for k in range(-200, 2000) for d in (1, 2, 3, 10)}
        sol = [c for c in cands if eval(lhs, {}, {var: c}) == rhs]
        assert len(sol) == 1, (lhs, rhs, sol)
        return sol[0]

    def eq(q_html, lhs, rhs, var, ans, wrong, e):
        assert solve(lhs, rhs, var) == Fr(ans), (lhs, ans)
        its.append(mcq("Solve: " + B(q_html) + ". What is %s?" % E(var), show(ans), [show(Fr(w)) for w in wrong], e))

    eq(E("n + 17 = 45"), "n+17", 45, "n", 28, [62, 32, 17],
       "Use the inverse: %s = 45 %s 17 = <b>28</b>. Check: 28 + 17 = 45. 62 adds instead. 32 takes 5 from 7 in the ones column instead of exchanging." % (E("n"), MINUS))
    eq(E("4y = 36"), "4*y", 36, "y", 9, [32, 144, 40],
       "4%s means 4 × %s. 4 × 9 = 36, so %s = 36 ÷ 4 = <b>9</b>. 32 subtracts 4 instead of dividing." % (E("y"), E("y"), E("y")))
    eq(E("m ÷ 6 = 7"), "m/6", 7, "m", 42, [13, 1, 36],
       "Use the inverse: %s = 7 × 6 = <b>42</b>. Check: 42 ÷ 6 = 7." % E("m"))
    eq(E("a - 23 = 58"), "a-23", 58, "a", 81, [35, 71, 23],
       "Add 23 to both sides: %s = 58 + 23 = <b>81</b>. 35 subtracts instead. 71 forgets to exchange 10 ones for 1 ten." % E("a"))
    eq(E("70 - t = 26"), "70-t", 26, "t", 44, [96, 56, 26],
       "70 take away something leaves 26, so %s = 70 %s 26 = <b>44</b>. Check: 70 %s 44 = 26. 96 adds the numbers." % (E("t"), MINUS, MINUS))
    eq(E("48 = 6p"), "6*p", 48, "p", 8, [42, 288, 54],
       "6 × %s = 48, so %s = 48 ÷ 6 = <b>8</b>. 42 subtracts 6 instead of dividing." % (E("p"), E("p")))
    # word -> equation
    its.append(mcq("Which equation matches this? <b>A number take away 9 is 15.</b>", E("n - 9 = 15"),
                   [E("9 - n = 15"), E("n + 9 = 15"), E("9n = 15")],
                   "Start with the number %s, then take away 9: <b>%s</b>. %s starts with 9, which is the wrong order."
                   % (E("n"), E("n - 9 = 15"), E("9 - n"))))
    eq(E("a + a + a = 27"), "a+a+a", 27, "a", 9, [24, 81, 30],
       "%s + %s + %s = 3%s. 3%s = 27, so %s = <b>9</b>. 24 subtracts 3 instead of dividing by 3." % ((E("a"),) * 6))
    eq(E("n + n + 8 = 30"), "n+n+8", 30, "n", 11, [22, 19, 38],
       "2%s + 8 = 30, so 2%s = 22 and %s = <b>11</b>. 22 forgets there are two %s's." % (E("n"), E("n"), E("n"), E("n")))
    its.append(mcq("I think of a number %s, multiply it by 4 and add 3. The answer is 31. Which equation shows this?" % E("n"),
                   E("4n + 3 = 31"), [E("4 + 3n = 31"), E("n + 4 + 3 = 31"), E("4n = 31 + 3")],
                   "Multiply %s by 4 to get 4%s, then add 3: <b>%s</b>. %s adds 4 instead of multiplying." % (E("n"), E("n"), E("4n + 3 = 31"), E("n + 4"))))
    eq(E("3m - 5 = 25"), "3*m-5", 25, "m", 10, [30, 20, Fr(20, 3)],
       "Undo the steps in reverse order. Add 5 first: 3%s = 30. Then divide by 3: %s = <b>10</b>. Check: 3 × 10 %s 5 = 25. "
       "%s subtracts 5 instead of adding (25 %s 5 = 20, then 20 ÷ 3). 30 forgets to divide by 3. 20 makes both mistakes."
       % (E("m"), E("m"), MINUS, show(Fr(20, 3)), MINUS))
    eq(E("2x + 7 = 31"), "2*x+7", 31, "x", 12, [24, 19, Fr(17, 2)],
       "Subtract 7: 2%s = 24. Divide by 2: %s = <b>12</b>. 24 forgets to divide. 8.5 divides first and then subtracts."
       % (E("x"), E("x")))
    eq(E("5k + 4 = 39"), "5*k+4", 39, "k", 7, [35, Fr(43, 5), 43],
       "Subtract 4: 5%s = 35. Divide by 5: %s = <b>7</b>. 8.6 adds 4 instead of subtracting it." % (E("k"), E("k")))
    eq(E("4a - 6 = 30"), "4*a-6", 30, "a", 9, [6, 36, 24],
       "Add 6: 4%s = 36. Divide by 4: %s = <b>9</b>. 6 subtracts 6 instead of adding. 36 forgets to divide." % (E("a"), E("a")))
    eq(E("7 + 3b = 40"), "7+3*b", 40, "b", 11, [33, 3, 47],
       "Subtract 7: 3%s = 33. Divide by 3: %s = <b>11</b>. 3 reads 3%s as 30 + %s." % (E("b"), E("b"), E("b"), E("b")))
    eq(E("n ÷ 4 + 3 = 10"), "n/4+3", 10, "n", 28, [52, 7, 40],
       "Subtract 3: %s ÷ 4 = 7. Multiply by 4: %s = <b>28</b>. 52 adds 3 instead of subtracting. 7 forgets to multiply."
       % (E("n"), E("n")))
    eq(E("y ÷ 5 - 2 = 6"), "y/5-2", 6, "y", 40, [20, 8, 28],
       "Add 2: %s ÷ 5 = 8. Multiply by 5: %s = <b>40</b>. 20 subtracts 2 instead of adding. 8 forgets to multiply." % (E("y"), E("y")))
    # check a solution
    assert 8 * 7 + 5 == 61
    its.append(mcq("Which value of %s makes %s true?" % (E("p"), B(E("8p + 5 = 61"))), 7, ["8.25", 56, 6],
                   "Try it: 8 × 7 + 5 = 56 + 5 = 61. So %s = <b>7</b>. 8.25 adds 5 to 61 instead of subtracting. 56 forgets to divide by 8." % E("p")))
    assert 3 * 10 - 5 == 25
    its.append(mcq("If %s, what is the value of %s?" % (B(E("3m - 5 = 25")), B(E("m + 4"))), 14, [10, 24, 34],
                   "First find %s: 3%s = 30, so %s = 10. Then %s + 4 = 10 + 4 = <b>14</b>. 10 stops too early."
                   % (E("m"), E("m"), E("m"), E("m"))))
    # function machine backwards
    assert (29 + 7) / 4 == 9
    its.append(mcq(fig(machine_svg("?", ["× 4", "%s 7" % MINUS], "29")) + "What number went into the machine?", 9,
                   ["5.5", 109, 36],
                   "Work backwards with the inverses, from the end: 29 + 7 = 36, then 36 ÷ 4 = <b>9</b>. "
                   "Check: 9 × 4 = 36, 36 %s 7 = 29. 5.5 subtracts 7 instead of adding." % MINUS))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    assert len(its) == 20
    return {"title": "Missing numbers with letters", "items": its}


# ------------------------------------------------------------ set 4: two unknowns and combinations
def set_two_unknowns(P):
    its = []

    def sols(f, rng=range(0, 41)):
        return [(a, b) for a in rng for b in rng if f(a, b)]

    # 1 2a + b = 15, a = 4
    assert 15 - 2 * 4 == 7
    its.append(mcq("%s. If %s, what is %s?" % (B(E("2a + b = 15")), E("a = 4"), E("b")), 7, [11, 23, 19],
                   "2 × 4 = 8, so 8 + %s = 15 and %s = <b>7</b>. 11 forgets that 2%s means 2 × 4." % (E("b"), E("b"), E("a"))))
    # 2 2a + 3b = 19, b = 3
    assert (19 - 9) / 2 == 5
    its.append(mcq("%s. If %s, what is %s?" % (B(E("2a + 3b = 19")), E("b = 3"), E("a")), 5, [8, 10, 14],
                   "3 × 3 = 9, so 2%s + 9 = 19. 2%s = 10, so %s = <b>5</b>. 10 forgets to divide by 2. 8 subtracts 3 instead of 9."
                   % (E("a"), E("a"), E("a"))))
    # 3 which pair fits 2x + y = 11
    f = lambda x, y: 2 * x + y == 11
    assert f(3, 5) and not f(5, 3) and not f(4, 7) and not f(2, 9)
    its.append(mcq("Which pair of values fits %s?" % B(E("2x + y = 11")), pair("x", 3, "y", 5),
                   [pair("x", 5, "y", 3), pair("x", 4, "y", 7), pair("x", 2, "y", 9)],
                   "2 × 3 + 5 = 6 + 5 = 11. So <b>%s</b>. %s gives 2 × 5 + 3 = 13. 4 + 7 = 11 forgets to double %s."
                   % (pair("x", 3, "y", 5), pair("x", 5, "y", 3), E("x"))))
    # 4 y = 3x - 2
    f = lambda x, y: y == 3 * x - 2
    assert f(4, 10) and not f(10, 4) and not f(4, 12) and not f(2, 6)
    its.append(mcq("Which pair of values fits %s?" % B(E("y = 3x - 2")), pair("x", 4, "y", 10),
                   [pair("x", 10, "y", 4), pair("x", 4, "y", 12), pair("x", 2, "y", 6)],
                   "3 × 4 %s 2 = 12 %s 2 = 10. So <b>%s</b>. %s forgets to subtract 2." % (MINUS, MINUS, pair("x", 4, "y", 10), pair("x", 4, "y", 12))))
    # 5 a + b = 12, a double b
    s = sols(lambda a, b: a + b == 12 and a == 2 * b)
    assert s == [(8, 4)]
    its.append(mcq("%s and %s is double %s. What are %s and %s?" % (B(E("a + b = 12")), E("a"), E("b"), E("a"), E("b")),
                   pair("a", 8, "b", 4), [pair("a", 4, "b", 8), pair("a", 6, "b", 6), pair("a", 10, "b", 2)],
                   "Try pairs that add to 12. 8 + 4 = 12 and 8 is double 4. So <b>%s</b>. %s has them the wrong way round: 4 is not double 8."
                   % (pair("a", 8, "b", 4), pair("a", 4, "b", 8))))
    # 6 a + b = 9, a is 3 more than b
    s = sols(lambda a, b: a + b == 9 and a == b + 3)
    assert s == [(6, 3)]
    its.append(mcq("%s and %s is 3 more than %s. What is %s?" % (B(E("a + b = 9")), E("a"), E("b"), E("b")), 3, [6, "4.5", 12],
                   "Take away the extra 3: 9 %s 3 = 6. Share 6 equally: %s = <b>3</b> and %s = 6. 6 is the value of %s, not %s."
                   % (MINUS, E("b"), E("a"), E("a"), E("b"))))
    # 7 a + b = 15, b = 4a
    s = sols(lambda a, b: a + b == 15 and b == 4 * a)
    assert s == [(3, 12)]
    its.append(mcq("%s and %s. What are %s and %s?" % (B(E("a + b = 15")), B(E("b = 4a")), E("a"), E("b")),
                   pair("a", 3, "b", 12), [pair("a", 12, "b", 3), pair("a", 4, "b", 11), pair("a", 5, "b", 10)],
                   "%s + 4%s = 5%s = 15, so %s = 3 and %s = 4 × 3 = 12. So <b>%s</b>. 5 and 10 add to 15, but 10 is only double 5."
                   % (E("a"), E("a"), E("a"), E("a"), E("b"), pair("a", 3, "b", 12))))
    # 8 m + n = 20, m = n + 4
    s = sols(lambda m, k: m + k == 20 and m == k + 4)
    assert s == [(12, 8)]
    its.append(mcq("%s and %s. What are %s and %s?" % (B(E("m + n = 20")), B(E("m = n + 4")), E("m"), E("n")),
                   pair("m", 12, "n", 8), [pair("m", 8, "n", 12), pair("m", 10, "n", 10), pair("m", 14, "n", 6)],
                   "Take away the extra 4: 20 %s 4 = 16, and 16 ÷ 2 = 8. So %s = 8 and %s = 12. 14 and 6 differ by 8, not 4."
                   % (MINUS, E("n"), E("m"))))
    # 9 x - y = 5, x + y = 13
    s = sols(lambda x, y: x - y == 5 and x + y == 13)
    assert s == [(9, 4)]
    its.append(mcq("%s and %s. What are %s and %s?" % (B(E("x + y = 13")), B(E("x - y = 5")), E("x"), E("y")),
                   pair("x", 9, "y", 4), [pair("x", 4, "y", 9), pair("x", 8, "y", 5), pair("x", 10, "y", 5)],
                   "Find two numbers that add to 13 and have a difference of 5: 9 + 4 = 13 and 9 %s 4 = 5. "
                   "%s gives 4 %s 9, which is not 5." % (MINUS, pair("x", 4, "y", 9), MINUS)))
    # 10 shapes 1
    tri = 7
    cir = 20 - 2 * tri
    assert cir == 6
    its.append(mcq(fig(shapes_svg([["tri", "+", "tri", "+", "cir", "=", "20"], ["tri", "=", "7"]])) +
                   "Each shape stands for a number. What is the circle worth?", 6, [13, 27, 3],
                   "Two triangles are 7 + 7 = 14. 20 %s 14 = <b>6</b>. 13 takes away only one triangle." % MINUS))
    # 11 shapes 2
    sq = 18 // 2
    tr2 = 15 - sq
    assert (sq, tr2) == (9, 6)
    its.append(mcq(fig(shapes_svg([["sq", "+", "sq", "=", "18"], ["sq", "+", "tri", "=", "15"]])) +
                   "Each shape stands for a number. What is the triangle worth?", 6, [9, 3, "7.5"],
                   "Two squares make 18, so one square is 9. Then 9 + triangle = 15, so the triangle is <b>6</b>. 9 is the square."))
    # 12 a x b = 18, a + b = 9
    s = sols(lambda a, b: a * b == 18 and a + b == 9 and a < b)
    assert s == [(3, 6)]
    its.append(mcq("%s and %s are whole numbers and %s is smaller than %s. %s and %s. What are they?"
                   % (E("a"), E("b"), E("a"), E("b"), B(E("a × b = 18")), B(E("a + b = 9"))),
                   pair("a", 3, "b", 6), [pair("a", 2, "b", 9), pair("a", 4, "b", 5), pair("a", 1, "b", 18)],
                   "List the factor pairs of 18: 1 and 18, 2 and 9, 3 and 6. Only 3 + 6 = 9. 2 and 9 multiply to 18, but add to 11."))
    # 13 p x q = 36, p + q = 15
    s = sols(lambda a, b: a * b == 36 and a + b == 15 and a < b)
    assert s == [(3, 12)]
    its.append(mcq("%s and %s are whole numbers and %s is smaller than %s. %s and %s. What are they?"
                   % (E("p"), E("q"), E("p"), E("q"), B(E("p × q = 36")), B(E("p + q = 15"))),
                   pair("p", 3, "q", 12), [pair("p", 6, "q", 6), pair("p", 4, "q", 9), pair("p", 5, "q", 10)],
                   "Factor pairs of 36: 1 and 36, 2 and 18, 3 and 12, 4 and 9, 6 and 6. Only 3 + 12 = 15. 4 and 9 add to 13."))
    # 14 which does NOT fit 3x + 2y = 20
    f = lambda x, y: 3 * x + 2 * y == 20
    assert sols(lambda x, y: f(x, y) and x > 0 and y > 0) == [(2, 7), (4, 4), (6, 1)] and not f(3, 5)
    its.append(mcq("Which pair does <b>not</b> fit %s?" % B(E("3x + 2y = 20")), pair("x", 3, "y", 5),
                   [pair("x", 2, "y", 7), pair("x", 4, "y", 4), pair("x", 6, "y", 1)],
                   "Test each pair. 3 × 3 + 2 × 5 = 9 + 10 = 19, not 20. The others make 6 + 14, 12 + 8 and 18 + 2, all 20."))
    # 15 a + b = 7, positive
    s = sols(lambda a, b: a + b == 7 and a > 0 and b > 0)
    assert len(s) == 6 and len(sols(lambda a, b: a + b == 7)) == 8
    its.append(mcq("%s and %s are whole numbers bigger than 0, and %s. How many different pairs are there? "
                   "(%s, %s and %s, %s count as different pairs.)"
                   % (E("a"), E("b"), B(E("a + b = 7")), E("a = 1"), E("b = 6"), E("a = 6"), E("b = 1")), 6, [3, 7, 8],
                   "List them in order of %s: %s = 1, 2, 3, 4, 5, 6 and %s = 6, 5, 4, 3, 2, 1. That is <b>6</b> pairs. "
                   "8 would include 0 + 7 and 7 + 0, but 0 is not bigger than 0." % (E("a"), E("a"), E("b"))))
    # 16 x + y = 11, x even, y odd
    s = sols(lambda x, y: x + y == 11 and x > 0 and y > 0 and x % 2 == 0)
    assert len(s) == 5
    its.append(mcq("%s and %s are whole numbers bigger than 0. %s, %s is even and %s is odd. How many pairs are possible?"
                   % (E("x"), E("y"), B(E("x + y = 11")), E("x"), E("y")), 5, [10, 6, 4],
                   "%s can be 2, 4, 6, 8 or 10, and then %s is 9, 7, 5, 3 or 1. That is <b>5</b> pairs. 10 counts every pair, even and odd."
                   % (E("x"), E("y"))))
    # 17 c x d = 12, single digits
    s = sols(lambda c, d: c * d == 12 and 0 < c < 10 and 0 < d < 10)
    assert len(s) == 4
    its.append(mcq("%s and %s are whole numbers from 1 to 9. %s. How many different pairs are there?"
                   % (E("c"), E("d"), B(E("c × d = 12"))), 4, [6, 2, 3],
                   "2 × 6, 3 × 4, 4 × 3 and 6 × 2: <b>4</b> pairs. 1 × 12 does not count because 12 is more than 9. "
                   "2 forgets that 2 × 6 and 6 × 2 are different pairs."))
    # 18 p x q = 24
    s = sols(lambda p, q: p * q == 24 and p > 0)
    assert len(s) == 8
    its.append(mcq("%s and %s are whole numbers. %s. How many different pairs are there? (%s, %s and %s, %s are different.)"
                   % (E("p"), E("q"), B(E("p × q = 24")), E("p = 3"), E("q = 8"), E("p = 8"), E("q = 3")), 8, [4, 7, 6],
                   "Factor pairs of 24: 1 × 24, 2 × 12, 3 × 8, 4 × 6. Each one works both ways round, so 4 × 2 = <b>8</b> pairs. "
                   "4 only counts each pair one way."))
    # 19 meal deal
    assert 3 * 4 == 12
    its.append(mcq("A café sells 3 kinds of sandwich and 4 kinds of drink. A meal deal is 1 sandwich and 1 drink. "
                   "How many different meal deals are there?", 12, [7, 9, 6],
                   "Each of the 3 sandwiches can go with each of the 4 drinks: 3 × 4 = <b>12</b>. 7 adds instead of multiplying."))
    # 20 two-digit numbers with digit sum 5
    s = [k for k in range(10, 100) if k // 10 + k % 10 == 5]
    assert s == [14, 23, 32, 41, 50]
    its.append(mcq("How many two-digit numbers have digits that add up to 5?", 5, [4, 6, 3],
                   "14, 23, 32, 41 and 50: <b>5</b> numbers. 4 forgets 50. 05 is not a two-digit number."))
    assert len(its) == 20
    return {"title": "Two unknowns and combinations", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_words(P):
    its = []

    def add(q, correct, cands, e):
        its.append(mcq(q, correct, cands, e))

    # 1 taxi
    assert 2 * 8 + 3 == 19
    add("A taxi fare is %s pounds, where %s is the number of miles. How much is the fare for 8 miles?"
        % (B(E("C = 2m + 3")), E("m")), "£19", ["£22", "£13", "£16"],
        "2 × 8 = 16, then 16 + 3 = <b>£19</b>. £22 adds 8 + 3 first. £16 forgets the £3 starting charge.")
    # 2 square garden
    add("A square garden has a perimeter of 36 m. Use %s to find the length of one side." % B(E("P = 4s")),
        "9 m", ["144 m", "32 m", "6 m"],
        "4%s = 36, so %s = 36 ÷ 4 = <b>9 m</b>. 144 m multiplies instead of dividing. 32 m subtracts 4." % (E("s"), E("s")))
    # 3 temperature rule
    assert 15 * 2 + 30 == 60
    add("A rough rule to change °C to °F is <b>double it, then add 30</b>. What is 15 °C in °F using this rule?",
        "60 °F", ["90 °F", "30 °F", "45 °F"],
        "Double first: 15 × 2 = 30. Then add 30: <b>60 °F</b>. 90 °F adds 30 first and then doubles. 30 °F forgets to add 30.")
    # 4 plant
    assert Fr(3, 2) * 6 + 4 == 13
    nm, he, his = P.next()
    add("%s’s sunflower is 4 cm tall. It grows 1.5 cm every week. How tall is it after 6 weeks?" % nm,
        "13 cm", ["9 cm", "11.5 cm", "33 cm"],
        "6 × 1.5 = 9 cm of growth. 4 + 9 = <b>13 cm</b>. 9 cm forgets the 4 cm it started at. 11.5 cm counts only 5 weeks.")
    # 5 plumber formula
    add("A plumber charges £40 to come out plus £30 for each hour. Which formula gives the total cost %s pounds for %s hours?"
        % (E("C"), E("h")), E("C = 30h + 40"), [E("C = 40h + 30"), E("C = 70h"), E("C = 30 + 40 + h")],
        "Each hour costs £30, so %s hours cost 30%s. Add the £40 once: <b>%s</b>. %s swaps the two charges."
        % (E("h"), E("h"), E("C = 30h + 40"), E("C = 40h + 30")))
    # 6 think of a number
    assert (25 + 8) / 3 == 11
    add(fig(machine_svg("?", ["× 3", "%s 8" % MINUS], "25")) + "I think of a number. I multiply it by 3, then subtract 8. "
        "The answer is 25. What was my number?", 11, [show(Fr(25 - 8, 3)), 67, 33],
        "Work backwards: 25 + 8 = 33, then 33 ÷ 3 = <b>11</b>. Check: 11 × 3 = 33, 33 %s 8 = 25. "
        "%s subtracts 8 instead of adding. 33 forgets to divide. 67 works forwards: 25 × 3 %s 8." % (MINUS, show(Fr(17, 3)), MINUS))
    assert show(Fr(17, 3)) == "5 " + fr(2, 3)
    # 7 doubling money
    nm, he, his = P.next()
    assert (10 + 4) / 2 == 7
    add("%s doubles %s money, then spends £4. %s has £10 left. How much did %s start with?" % (nm, his, he.capitalize(), he),
        "£7", ["£3", "£16", "£14"],
        "Work backwards: £10 + £4 = £14, then £14 ÷ 2 = <b>£7</b>. Check: £7 × 2 = £14, £14 %s £4 = £10. £3 subtracts the £4." % MINUS)
    # 8 bike hire backwards
    assert (32 - 8) / 4 == 6
    add("Hiring a canoe costs £8 plus £4 for each hour. The bill is £32. For how many hours was the canoe hired?",
        6, [8, 10, 24],
        "Take off the £8 first: £32 %s £8 = £24. Then £24 ÷ £4 = <b>6</b> hours. 8 forgets the £8. 10 adds the £8." % MINUS)
    # 9 tables
    assert 4 * 8 + 2 == 34
    add(fig(tables_svg()) + "Tables are pushed together in a row. 1 table seats 6, 2 tables seat 10, 3 tables seat 14. "
        "How many people can sit at 8 tables in a row?", 34, [48, 38, 30],
        "Each extra table adds 4 seats. The rule is 4%s + 2: 4 × 8 + 2 = <b>34</b>. 48 is 8 × 6, but tables pushed together lose the seats at the joins."
        % E("n"))
    # 10 tables needed
    assert 4 * 12 + 2 == 50 and 4 * 11 + 2 < 50
    add("Using the same rule (4%s + 2 seats for %s tables), how many tables are needed to seat exactly 50 people?" % (E("n"), E("n")),
        12, [13, 9, 8],
        "4%s + 2 = 50, so 4%s = 48 and %s = <b>12</b>. 9 divides 50 by 6, as if the tables were apart." % (E("n"), E("n"), E("n")))
    # 11 tiles
    assert 5 * 9 + 1 == 46
    add("Pattern %s of a tile design uses %s tiles. Which pattern uses 46 tiles?" % (E("n"), B(E("5n + 1"))),
        9, [231, "9.4", 10],
        "5%s + 1 = 46, so 5%s = 45 and %s = <b>9</b>. Check: 5 × 9 + 1 = 46. 231 puts 46 in place of %s. 9.4 adds 1 instead of subtracting."
        % (E("n"), E("n"), E("n"), E("n")))
    # 12 ages
    s = [a for a in range(1, 30) if a + (a - 3) == 21]
    assert s == [12]
    nm, he, his = P.next()
    add("%s is %s years old. %s sister is 3 years younger. Their ages add up to 21. How old is %s?" % (nm, E("a"), his.capitalize(), nm),
        12, [9, "10.5", 18],
        "%s + (%s %s 3) = 21, so 2%s %s 3 = 21. 2%s = 24 and %s = <b>12</b>. 9 is the sister’s age. Check: 12 + 9 = 21."
        % (E("a"), E("a"), MINUS, E("a"), MINUS, E("a"), E("a")))
    # 13 pen and ruler
    s = [r for r in range(0, 121) if r + (r + 40) == 120]
    assert s == [40]
    add("A pen and a ruler cost £1.20 altogether. The pen costs 40p more than the ruler. How much does the ruler cost?",
        "40p", ["80p", "60p", "20p"],
        "Take away the extra 40p: 120p %s 40p = 80p. Share it equally: the ruler costs <b>40p</b> and the pen 80p. "
        "80p is the price of the pen." % MINUS)
    # 14 apples and bananas
    assert (130 - 3 * 30) / 2 == 20
    add("3 apples and 2 bananas cost £1.30. One apple costs 30p. How much does one banana cost?",
        "20p", ["40p", "50p", "65p"],
        "3 apples cost 3 × 30p = 90p. 130p %s 90p = 40p for 2 bananas, so one banana is <b>20p</b>. 40p is two bananas." % MINUS)
    # 15 pencils and rubbers
    s = [(p, r) for p in range(1, 70) for r in range(1, 70) if 2 * p + r == 70 and p + r == 45]
    assert s == [(25, 20)]
    add("2 pencils and 1 rubber cost 70p. 1 pencil and 1 rubber cost 45p. How much does 1 pencil cost?",
        "25p", ["20p", "35p", "45p"],
        "The first group has one more pencil than the second. 70p %s 45p = <b>25p</b> for that pencil. 20p is the rubber." % MINUS)
    # 16 cone flavours
    fl = ["a", "b", "c", "d"]
    pairs_ = [(x, y) for i, x in enumerate(fl) for y in fl[i + 1:]]
    assert len(pairs_) == 6
    nm, he, his = P.next()
    add("An ice cream van has 4 flavours. %s chooses 2 <b>different</b> flavours for a cone. The order does not matter. "
        "How many different choices are there?" % nm, 6, [12, 8, 16],
        "Call them A, B, C, D. AB, AC, AD, BC, BD, CD: <b>6</b> choices. 12 counts AB and BA as different, but the order does not matter.")
    # 17 coins which
    f = lambda a, b: 20 * a + 50 * b == 160
    assert f(3, 2) and not f(2, 3) and not f(4, 1) and not f(5, 1)
    nm, he, his = P.next()
    add("%s has only 20p and 50p coins. %s has £1.60 exactly. Which could %s have?" % (nm, he.capitalize(), he),
        "3 × 20p and 2 × 50p", ["2 × 20p and 3 × 50p", "4 × 20p and 1 × 50p", "5 × 20p and 1 × 50p"],
        "60p + 100p = 160p = £1.60. The others make £1.90, £1.30 and £1.50.")
    # 18 coins how many ways
    s = sols = [(a, b) for a in range(0, 9) for b in range(0, 4) if 20 * a + 50 * b == 160]
    assert sols == [(3, 2), (8, 0)]
    add("In how many different ways can you make exactly £1.60 using only 20p and 50p coins? (You do not have to use both kinds.)",
        2, [1, 3, 4],
        "Try 0, 1, 2, 3 fifty-pence coins: 8 × 20p works, and 2 × 50p + 3 × 20p works. 1 or 3 fifty-pence coins leave 110p or 10p, "
        "which 20p coins cannot make. So there are <b>2</b> ways.")
    # 19 tickets
    s = [(a, c) for a in range(1, 6) for c in range(1, 8) if 5 * a + 3 * c == 21]
    assert s == [(3, 2)]
    add("At the museum an adult ticket costs £5 and a child ticket costs £3. A group of adults and children pays £21. "
        "There is at least one adult and one child. Who is in the group?",
        "3 adults, 2 children", ["2 adults, 3 children", "4 adults, 1 child", "1 adult, 5 children"],
        "3 × £5 + 2 × £3 = £15 + £6 = <b>£21</b>. 2 adults and 3 children cost £19, 4 adults and 1 child cost £23, 1 adult and 5 children cost £20.")
    # 20 cards
    f = lambda x, y: 6 * x + 4 * y == 26
    assert f(3, 2) and not f(2, 3) and not f(4, 1) and not f(1, 4)
    nm, he, his = P.next()
    add("%s buys %s packs of 6 football cards and %s packs of 4 cards. %s gets exactly 26 cards. Which could be true?"
        % (nm, E("x"), E("y"), he.capitalize()), pair("x", 3, "y", 2), [pair("x", 2, "y", 3), pair("x", 4, "y", 1), pair("x", 1, "y", 4)],
        "6 × 3 + 4 × 2 = 18 + 8 = 26. The others make 12 + 12 = 24, 24 + 4 = 28 and 6 + 16 = 22.")
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    assert len(its) == 20
    return {"title": "Word problems: algebra", "items": its}


# ------------------------------------------------------------ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    return (
        "<h2>A letter stands for a number</h2>"
        "<p>In algebra, a letter such as %s stands for a number. %s means 3 × %s. We leave out the × sign "
        "and write the number first. If %s = 4, then 3%s = 12 (not 34).</p>" % (E("n"), E("3n"), E("n"), E("n"), E("n")) +
        "<h2>Use a formula</h2>"
        "<p>A <b>formula</b> is a rule for working something out. Replace each letter with its number. "
        "Then multiply or divide <b>before</b> you add or subtract.</p>" +
        ex("Example", "Bike hire costs %s pounds for %s hours. Find the cost for 4 hours." % (E("C = 5h + 3"), E("h")),
           "Replace %s with 4: 5 × 4 + 3 = 20 + 3 = 23." % E("h"), "£23") +
        "<h2>Linear sequences</h2>"
        "<p>In a <b>linear</b> sequence the terms go up or down by the same amount each time.</p>"
        "<figure class='sn-fig'>" + seq_svg(["3", "10", "17", "24"], ["+7", "+7", "+7"]) +
        "<figcaption>Start at 3 and add 7. The %sth term is 7%s %s 4: the step is 7, and 7 × 1 %s 4 = 3.</figcaption></figure>"
        % (E("n"), E("n"), MINUS, MINUS) +
        ex("Example", "The %sth term is %s. What is the 10th term?" % (E("n"), E("3n + 1")),
           "Put %s: 3 × 10 + 1 = 31." % E("n = 10"), "31") +
        "<h2>Missing number problems</h2>"
        "<p>Write the missing number as a letter. Undo the steps with inverse operations, <b>last step first</b>.</p>"
        "<figure class='sn-fig'>" + machine_svg("m", ["× 3", "%s 5" % MINUS], "25") +
        "<figcaption>%s. To find %s, add 5 (30), then divide by 3.</figcaption></figure>" % (E("3m - 5 = 25"), E("m")) +
        ex("Example", "Solve %s." % E("3m - 5 = 25"),
           "Add 5 to both sides: 3%s = 30. Divide by 3: %s = 10. Check: 3 × 10 %s 5 = 25." % (E("m"), E("m"), MINUS), E("m = 10")) +
        "<h2>Two unknowns</h2>"
        "<p>An equation like %s has many answers. List them in order so you do not miss any.</p>" % E("a + b = 6") +
        table([E("a"), "0", "1", "2", "3", "4", "5", "6"], [[E("b"), "6", "5", "4", "3", "2", "1", "0"]]) +
        "<figure class='sn-fig'>" + shapes_svg([["tri", "+", "tri", "+", "cir", "=", "20"], ["tri", "=", "7"]]) +
        "<figcaption>Two triangles are 14, so the circle is 20 %s 14 = 6.</figcaption></figure>" % MINUS +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["3%s = 34 when %s = 4" % (E("n"), E("n")), "3%s means 3 × %s = 12" % (E("n"), E("n"))],
            ["%s when %s = 6 gives 22" % (E("2a + 5"), E("a")), "Multiply first: 12 + 5 = 17"],
            ["%s gives %s = 20" % (E("3m - 5 = 25"), E("m")), "Add 5, then divide by 3: %s = 10" % E("m")],
            ["%s term of 5, 8, 11 is %s" % (E("n") + "th", E("5n + 3")), "Use the step: 3%s + 2" % E("n")],
            ["10th term of 3, 7, 11 is 3 + 10 × 4", "There are 9 steps: 3 + 9 × 4 = 39"],
            ["Missing a pair of numbers", "List the values of one letter in order: 0, 1, 2, …"],
        ])
    )


FAQ = [
    {"q": "What algebra do children learn in Year 6?",
     "a": "Year 6 is when algebra is first taught as its own topic. Children use simple formulae, describe linear sequences, write missing number problems with letters, find pairs of numbers that fit an equation with two unknowns and list all the possible combinations."},
    {"q": "Is algebra in the Year 6 SATs?",
     "a": "Yes. Algebra questions appear in the KS2 maths reasoning papers, for example finding the value of shapes in a puzzle, using a formula for a cost or solving “I think of a number” problems."},
    {"q": "What does 3n mean?",
     "a": "3n means 3 × n. If n = 4, then 3n = 12. It does not mean the digits 3 and 4 written next to each other."},
    {"q": "How do you find the nth term of a sequence?",
     "a": "Find the step between terms and multiply n by it. Then add or subtract to match the first term. For 5, 8, 11, 14 the step is 3, so the nth term is 3n + 2."},
]


def gen():
    rnd = random.Random(6613)
    P = People(rnd)
    sets = [set_formulae(P), set_sequences(P), set_equations(P), set_two_unknowns(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(re.sub(r"<[^>]+>", "", x) for x in it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = it["q"]
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "uk", "subject": "maths", "grade": "year-6", "slug": "algebra", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Algebra: Formulae, Sequences and Equations",
        "seo_title": "Year 6 Algebra Worksheets: Formulae, nth Term, Missing Numbers and Two Unknowns",
        "short_title": "Algebra",
        "domain": "Algebra",
        "standard_code": "Year 6: Algebra",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Use simple formulae; generate and describe linear number sequences; express missing number problems algebraically; find pairs of numbers that satisfy an equation with two unknowns; enumerate possibilities of combinations of two variables.",
        "meta_desc": "Free Year 6 maths worksheets on algebra: using simple formulae, linear sequences and the nth term, missing number problems with letters, equations with two unknowns and listing combinations. 100 SATs-style questions with an answer key, matched to the National Curriculum.",
        "key_big": "A letter stands for a number: 3n means 3 × n, so if n = 4, then 3n = 12.",
        "key_sub": "In a formula, multiply or divide before you add or subtract. To solve an equation, undo the steps with inverse operations, last step first.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "matchstick|tables in a row|function machine|number sequence")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "algebra.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
