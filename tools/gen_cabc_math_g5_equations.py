# -*- coding: utf-8 -*-
"""
British Columbia Grade 5 Math: One-Step Equations with Variables
(BC Mathematics Curriculum, Grade 5 — Patterning: one-step equations with variables)
  python3 tools/gen_cabc_math_g5_equations.py
Letters as unknowns (6n means 6 × n), solving one-step equations with + and − (whole numbers to 1 000 000
and decimals), solving with × and ÷ (6n = 42, n ÷ 4 = 9), checking a solution by putting it back into the
equation, and writing and solving equations for stories in BC contexts.
Wrong choices come from real mistakes: reading 6n as 6 + n (or as the number 6_), using the same operation
instead of the inverse (n + 18 = 45 -> 63, 6n = 42 -> 252, n ÷ 4 = 9 -> 2), smaller-digit-from-larger,
forgetting to carry, lining up the last digits of decimals instead of the decimal points, checking with the
inverse instead of the original equation, and reading letters as alphabet positions.
Every answer is checked in code. HTML attributes use single quotes. Canadian English, BC numbers (10 000).
"""
import json, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
GREY = "#e4e4e4"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]
NB = " "
LETTERS = "abcdefghijklmnopqrstuvwxyz"
COEF = re.compile(r"^(\d+)([a-z])$")


# ------------------------------------------------------------ numbers and equations
def n(x):
    """BC style: 4 digits no separator, 5 or more digits grouped with a no-break space."""
    if isinstance(x, str):
        return x
    s = str(x)
    if abs(x) < 10000:
        return s
    out = ""
    while len(s) > 3:
        out = NB + s[-3:] + out
        s = s[:-3]
    return s + out


def tok(p):
    return n(p) if isinstance(p, int) else p


def plain(*parts):
    """Plain text equation (choices, SVG)."""
    return " ".join(tok(p) for p in parts)


def html(*parts):
    """Equation for question text: a letter in italics, 6n as 6<i>n</i>."""
    out = []
    for p in parts:
        t = tok(p)
        m = COEF.match(t)
        if len(t) == 1 and t in LETTERS:
            t = "<i>" + t + "</i>"
        elif m:
            t = m.group(1) + "<i>" + m.group(2) + "</i>"
        out.append(t)
    return " ".join(out)


def I(t):
    """Italic letter / coefficient for explanations."""
    return html(t)


def val(expr):
    s = expr.replace("−", "-").replace("×", "*").replace(NB, "").replace("$", "")
    s = re.sub(r"(\d+(?:\.\d+)?)", r"F('\1')", s).replace("÷", "/")
    return eval(s, {"__builtins__": {}, "F": Fraction})


def holds(eq, ans=None):
    """'n + 25 = 60' or '6n = 42' is true with the letter = ans."""
    s = re.sub(r"<[^>]+>", "", eq)
    s = re.sub(r"(\d)([a-z])\b", r"\1 × \2", s)
    if ans is not None:
        s = re.sub(r"\b[a-z]\b", str(ans), s)
    vals = [val(p.strip()) for p in s.split("=")]
    return all(v == vals[0] for v in vals)


def sfl(a, b):
    """Smaller digit from larger digit in each column: 400 − 150 -> 350 (a typical mistake)."""
    da, db = str(a), str(b).rjust(len(str(a)), "0")
    return int("".join(str(abs(int(x) - int(y))) for x, y in zip(da, db)))


def nocarry(a, b):
    """Add column by column and drop every carried ten: 48 + 35 -> 73."""
    out, p = 0, 1
    while a or b:
        out += ((a % 10 + b % 10) % 10) * p
        a, b, p = a // 10, b // 10, p * 10
    return out


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = n(correct) if isinstance(correct, int) else str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if isinstance(c, int):
            if c <= 0:
                continue
            c = n(c)
        c = str(c)
        if c in seen or not c or c.startswith("-") or c.startswith("−"):
            continue
        seen.add(c)
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
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
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


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ pictures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(round(w)), int(round(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


FS = 18
GAP = 7


def tok_w(t):
    return len(t) * FS * 0.6


def expr_w(s):
    ts = s.split(" ")
    return sum(tok_w(t) for t in ts) + GAP * (len(ts) - 1)


def draw_expr(cx, base, s):
    """Draw 'n + 20' centred at cx: a letter in red italics, 3n as black 3 and red italic n."""
    ts = s.split(" ")
    x = cx - expr_w(s) / 2
    out = []
    for t in ts:
        w = tok_w(t)
        m = COEF.match(t)
        if len(t) == 1 and t in LETTERS:
            out.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' font-style='italic' fill='%s' "
                       "text-anchor='middle'>%s</text>" % (x + w / 2, base, FS, RED, t))
        elif m:
            out.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s"
                       "<tspan font-style='italic' fill='%s'>%s</tspan></text>"
                       % (x + w / 2, base, FS, INK, m.group(1), RED, m.group(2)))
        else:
            out.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                       % (x + w / 2, base, FS, INK, t))
        x += w + GAP
    return "".join(out)


def pan_svg(left, right):
    """A level pan balance with an expression on each pan."""
    def box_w(t):
        return max(90, int(expr_w(t) + 24))
    wl, wr = box_w(left), box_w(right)
    cl = 8 + wl / 2
    cr = cl + wl / 2 + 40 + wr / 2
    mid = (cl + cr) / 2
    top, ih = 8, 36
    py = top + ih
    s = []
    for t, c, w in ((left, cl, wl), (right, cr, wr)):
        s.append("<rect x='%.1f' y='%d' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (c - w / 2, top, w, ih, GREY, INK))
        s.append(draw_expr(c, top + 25, t))
        s.append("<rect x='%.1f' y='%d' width='%d' height='6' fill='%s'/>" % (c - w / 2, py, w, INK))
        s.append("<rect x='%.1f' y='%d' width='4' height='18' fill='%s'/>" % (c - 2, py + 6, INK))
    by = py + 24
    s.append("<rect x='%.1f' y='%d' width='%.1f' height='6' fill='%s'/>" % (cl - 2, by, cr - cl + 4, INK))
    s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (mid, by + 6, mid - 22, by + 40, mid + 22, by + 40, GREEN))
    s.append("<rect x='%.1f' y='%d' width='80' height='5' fill='%s'/>" % (mid - 40, by + 40, INK))
    return svg_wrap(cr + wr / 2 + 8, by + 47, "".join(s),
                    "pan balance: %s on the left and %s on the right" % (left, right))


def bar_svg(whole, p1, p2):
    """Part-part-whole bar model, drawn to scale. Values are numbers or one letter."""
    vals = [whole, p1, p2]
    nums = [v if isinstance(v, int) else None for v in vals]
    miss = [i for i, v in enumerate(nums) if v is None]
    assert len(miss) == 1
    full = list(nums)
    m = miss[0]
    full[m] = (nums[1] + nums[2]) if m == 0 else (nums[0] - (nums[2] if m == 1 else nums[1]))
    assert full[1] + full[2] == full[0] and min(full) > 0
    W, x0, h = 280, 8, 36
    w1 = round(W * full[1] / full[0])
    w1 = min(max(w1, 80), W - 80)
    s = []
    rows = [(8, [(x0, W, whole, FILL)]), (8 + h + 10, [(x0, w1, p1, "#fff"), (x0 + w1, W - w1, p2, "#fff")])]
    for y, cells in rows:
        for x, w, v, f in cells:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                     % (x, y, w, h, f, GREEN))
            s.append(draw_expr(x + w / 2, y + 25, tok(v)))
    lb = "bar model: whole %s, parts %s and %s" % tuple(tok(v) for v in vals)
    return svg_wrap(W + 16, 8 + 2 * h + 10 + 8, "".join(s), lb)


def parts_svg(k, part, total):
    """Equal-parts bar: k equal parts, each labelled part, with the total above a bracket."""
    cw = 46 if k <= 6 else 40
    x0, y = 8, 40
    s = []
    for i in range(k):
        s.append("<rect x='%d' y='%d' width='%d' height='36' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (x0 + i * cw, y, cw, FILL, GREEN))
        s.append(draw_expr(x0 + i * cw + cw / 2, y + 25, tok(part)))
    x1 = x0 + k * cw
    s.append("<path d='M%d %d v-8 H%d v8' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y - 4, x1, INK))
    s.append(draw_expr((x0 + x1) / 2, y - 16, tok(total)))
    return svg_wrap(x1 + 8, y + 44, "".join(s),
                    "equal parts bar: %d equal parts of %s make %s" % (k, tok(part), tok(total)))


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ distractor lists
def step_of(ans):
    return max(10, 10 ** (len(str(ans)) - 2))


def sub_cands(big, small, ans):
    """Answer is big − small. Mistakes: adding instead (same operation), smaller-from-larger, regrouping slips."""
    c = [big + small]
    if sfl(big, small) != ans:
        c.append(sfl(big, small))
    st = step_of(ans)
    return c + [ans + st, ans - st, ans + 10, ans - 10, ans + 1, ans - 1]


def add_cands(a, b, ans):
    """Answer is a + b. Mistakes: subtracting instead, forgetting to carry, carry slips."""
    c = [abs(a - b)]
    if nocarry(a, b) != ans:
        c.append(nocarry(a, b))
    st = step_of(ans)
    return c + [ans - st, ans + st, ans - 10, ans + 10, ans + 1, ans - 1]


def letter_in(parts):
    for p in parts:
        if isinstance(p, str):
            m = re.search(r"[a-z]$", p)
            if m and (len(p) == 1 or COEF.match(p)):
                return m.group(0)
    raise AssertionError(parts)


def ask(parts):
    return html(*parts) + ". What is <i>%s</i>?" % letter_in(parts)


def put(parts, ans):
    """The equation with the letter replaced by ans (6n -> 6 × 7)."""
    out = []
    for p in parts:
        if isinstance(p, str) and COEF.match(p):
            out.append(COEF.match(p).group(1) + " × " + n(ans))
        elif isinstance(p, str) and len(p) == 1 and p in LETTERS:
            out.append(n(ans))
        else:
            out.append(tok(p))
    return " ".join(out)


# ============================================================ set 1: letters as unknowns
def set_letters(P):
    its = []
    its.append(mcq("In the equation " + html("n", "+", 7, "=", 15) + ", what does <i>n</i> stand for?",
                   "An unknown number", ["The number 14", "The word “number”", "Any number at all"],
                   "A letter in an equation is a <b>variable</b>. It stands for an <b>unknown number</b>. Here <i>n</i> = 8, "
                   "because 8 + 7 = 15. Not 14: <i>n</i> is not its place in the alphabet. In this equation, "
                   "<i>n</i> has only one value."))
    its.append(mcq("What does 6<i>n</i> mean?", "6 × n", ["6 + n", "60 + n", "n − 6"],
                   "A number written right next to a letter means multiply. <b>6<i>n</i> = 6 × <i>n</i></b>. "
                   "It does not mean 6 + <i>n</i>, and it is not a two-digit number in the sixties."))
    its.append(mcq("Which means the same as <i>n</i> × 9?", "9n", ["9 + n", "n − 9", "n ÷ 9"],
                   "<i>n</i> × 9 is the same as 9 × <i>n</i>, and we write it as <b>9<i>n</i></b>, number first. "
                   "9 + <i>n</i> adds instead of multiplying."))
    its.append(mcq("Which is the same as <i>n</i> + <i>n</i> + <i>n</i> + <i>n</i>?", "4n", ["n + 4", "2n", "n ÷ 4"],
                   "Adding <i>n</i> four times is 4 groups of <i>n</i>: 4 × <i>n</i> = <b>4<i>n</i></b>. "
                   "Not <i>n</i> + 4: that adds 4 once."))
    its.append(mcq("Which means “a number divided by 8”?", "n ÷ 8", ["8 ÷ n", "8n", "n − 8"],
                   "Start with the number <i>n</i>, then divide by 8: <b><i>n</i> ÷ 8</b>. "
                   "8 ÷ <i>n</i> starts with 8, not with the number. 8<i>n</i> means 8 × <i>n</i>."))
    # substitute
    for letter, v, expr, ans, wr, e in [
        ("n", 4, "6n", 24, [10, 64, 2], "6<i>n</i> means 6 × <i>n</i>. Put in 4: 6 × 4 = <b>24</b>. "
         "Not 10: that reads 6<i>n</i> as 6 + <i>n</i>. Not 64: that writes the 6 and the 4 side by side."),
        ("n", 7, "5n", 35, [12, 57, 2], "5<i>n</i> = 5 × 7 = <b>35</b>. Not 12: that adds. "
         "Not 57: that writes the digits side by side."),
        ("y", 12, "3y", 36, [15, 312, 9], "3<i>y</i> = 3 × 12 = <b>36</b>. Not 15: that adds. "
         "Not 312: that writes the numbers side by side."),
        ("m", 8, "m ÷ 2", 4, [16, 10, 6], "Put in 8: 8 ÷ 2 = <b>4</b>. Not 16: that multiplies. "
         "Not 10: that adds. Not 6: that subtracts."),
        ("t", 50, "t × 4", 200, [54, 2000, 46], "Put in 50: 50 × 4 = <b>200</b>. Not 54: that adds. "
         "Not 2000: that writes one zero too many."),
        ("a", 36, "a ÷ 9", 4, [27, 45, 324], "Put in 36: 36 ÷ 9 = <b>4</b>. Not 27: that subtracts. "
         "Not 324: that multiplies."),
    ]:
        assert val(put(expr.split(" "), v)) == ans
        its.append(mcq("If <i>%s</i> = %s, what is %s?" % (letter, n(v), html(*expr.split(" "))), ans, wr, e))
    # which value makes it true
    for parts, ans, wr, e in [
        (["n", "+", 9, "=", 20], 11, [29, 10, 12],
         "Try each value. 11 + 9 = 20, so <b><i>n</i> = 11</b>. Not 29: that adds 20 and 9. "
         "10 + 9 is 19 and 12 + 9 is 21."),
        (["4n", "=", 32], 8, [28, 128, 36],
         "4<i>n</i> means 4 × <i>n</i>. 4 × 8 = 32, so <b><i>n</i> = 8</b>. Not 28: that reads 4<i>n</i> as 4 + <i>n</i>. "
         "Not 128: that multiplies 32 by 4."),
        (["n", "−", 15, "=", 25], 40, [10, 50, 30],
         "40 − 15 = 25, so <b><i>n</i> = 40</b>. Not 10: that subtracts 15 from 25, the same operation. "
         "50 − 15 is 35 and 30 − 15 is 15."),
        (["n", "÷", 3, "=", 6], 18, [2, 9, 3],
         "18 ÷ 3 = 6, so <b><i>n</i> = 18</b>. Not 2: that divides 6 by 3. Not 9: that adds. Not 3: that subtracts."),
    ]:
        assert holds(plain(*parts), ans) and not any(holds(plain(*parts), w) for w in wr)
        its.append(mcq("Which value of <i>n</i> makes " + html(*parts) + " true?", ans, wr, e))
    # balance
    assert holds("n + 20 = 45", 25)
    its.append(mcq("The pans balance. What is <i>n</i>?" + fig(pan_svg("n + 20", "45")), 25, [65, 35, 15],
                   "Both pans have the same value, so <i>n</i> + 20 = 45. Take 20 from both sides: "
                   "<i>n</i> = 45 − 20 = <b>25</b>. Not 65: that adds."))
    # which is true when n = 6
    assert holds("3n = 18", 6) and not any(holds(w, 6) for w in ["3n = 9", "3n = 36", "3n = 63"])
    its.append(mcq("<i>n</i> = 6. Which equation is true?", "3n = 18", ["3n = 9", "3n = 36", "3n = 63"],
                   "3<i>n</i> = 3 × 6 = 18, so <b>3<i>n</i> = 18</b> is true. 9 is 3 + 6. 36 and 63 write the digits side by side."))
    # letters can change
    assert holds("8 + p = 13", 5) and holds("8 + n = 13", 5)
    its.append(mcq("Look at " + html(8, "+", "p", "=", 13) + " and " + html(8, "+", "n", "=", 13) + ". What is true?",
                   "p = 5 and n = 5", ["p = 21 and n = 21", "p = 16 and n = 14", "p and n must be different"],
                   "Any letter can stand for the unknown. Both equations say 8 + something = 13, so "
                   "<b><i>p</i> = 5 and <i>n</i> = 5</b>. Not 16 and 14: those are the places of p and n in the alphabet. "
                   "Not 21: that adds 8 and 13."))
    # mistakes
    nm, he, his = P.next()
    its.append(mcq("%s says: “If <i>n</i> = 5, then 3<i>n</i> = 35.” What is wrong?" % nm,
                   "3n means 3 × n, so it is 15",
                   ["3n means 3 + n, so it is 8", "3n means 5 × 5, so it is 25", "Nothing is wrong"],
                   "3<i>n</i> means 3 × <i>n</i>. With <i>n</i> = 5, 3<i>n</i> = 3 × 5 = <b>15</b>. %s wrote the 3 and the 5 "
                   "side by side. 3 + <i>n</i> would be 8, but 3<i>n</i> is not 3 + <i>n</i>." % nm))
    nm, he, his = P.next()
    assert holds("6n = 42", 7)
    its.append(mcq("%s reads 6<i>n</i> = 42 as 6 + <i>n</i> = 42. What is the correct value of <i>n</i>?" % nm,
                   "n = 7, because 6 × 7 = 42",
                   ["n = 36, because 6 + 36 = 42", "n = 48, because 42 + 6 = 48", "n = 252, because 42 × 6 = 252"],
                   "6<i>n</i> means 6 × <i>n</i>, not 6 + <i>n</i>. 6 × <i>n</i> = 42, so <i>n</i> = 42 ÷ 6 = <b>7</b>. "
                   "36 would only be right for 6 + <i>n</i> = 42."))
    assert len(its) == 20, len(its)
    return {"title": "Letters as unknowns", "items": its}


# ============================================================ set 2: + and −
def set_add_sub(P):
    its = []

    def add(parts, ans, cands, e, bar=None):
        eq = plain(*parts)
        assert holds(eq, ans), eq
        its.append(mcq(ask(parts) + (fig(bar_svg(*bar)) if bar else ""), ans, cands, e))

    def unknown_plus(parts, a, s, u, bar=None):
        ans = s - a
        e = ("Use the inverse. Subtraction undoes addition: <i>%s</i> = %s = <b>%s</b>. Check: %s. "
             "Not %s: that adds, the same operation, instead of subtracting." % (u, plain(s, "−", a), n(ans),
                                                                                  put(parts, ans), n(s + a)))
        if sfl(s, a) not in (ans, s + a):
            e += " Not %s: that takes the smaller digit from the larger in each column." % n(sfl(s, a))
        add(parts, ans, sub_cands(s, a, ans), e, bar)

    def unknown_taken(parts, a, r, u):
        ans = a - r
        e = ("%s take away what leaves %s? <i>%s</i> = %s = <b>%s</b>. Check: %s. Not %s: that adds the two numbers."
             % (n(a), n(r), u, plain(a, "−", r), n(ans), put(parts, ans), n(a + r)))
        if sfl(a, r) != ans:
            e += " Not %s: that takes the smaller digit from the larger in each column." % n(sfl(a, r))
        add(parts, ans, sub_cands(a, r, ans), e)

    def unknown_start(parts, a, r, u, bar=None):
        ans = r + a
        e = ("<i>%s</i> is the number you start with. Undo − %s by adding: <i>%s</i> = %s = <b>%s</b>. Check: %s. "
             "Not %s: that subtracts, the same operation, instead of adding."
             % (u, n(a), u, plain(r, "+", a), n(ans), put(parts, ans), n(abs(r - a))))
        if nocarry(r, a) != ans and nocarry(r, a) > 0:
            e += " Not %s: that forgets to carry." % n(nocarry(r, a))
        add(parts, ans, add_cands(r, a, ans), e, bar)

    unknown_plus(["n", "+", 18, "=", 45], 18, 45, "n")
    unknown_start(["n", "−", 12, "=", 30], 12, 30, "n")
    unknown_plus([36, "+", "k", "=", 91], 36, 91, "k")
    unknown_plus(["x", "+", 245, "=", 700], 245, 700, "x")
    unknown_plus([1250, "+", "n", "=", 4000], 1250, 4000, "n")
    unknown_plus(["n", "+", 12500, "=", 40000], 12500, 40000, "n")
    unknown_taken([85, "−", "y", "=", 37], 85, 37, "y")
    unknown_taken([600, "−", "m", "=", 275], 600, 275, "m")
    unknown_taken([50000, "−", "p", "=", 18000], 50000, 18000, "p")
    unknown_start(["n", "−", 46, "=", 38], 46, 38, "n")
    unknown_start(["a", "−", 350, "=", 480], 350, 480, "a")
    unknown_start(["t", "−", 2750, "=", 6500], 2750, 6500, "t")
    unknown_start(["n", "−", 25000, "=", 75000], 25000, 75000, "n")
    # = sign first
    add([90, "=", "n", "+", 35], 55, sub_cands(90, 35, 55),
        "The = sign can come first. <i>n</i> + 35 = 90, so <i>n</i> = 90 − 35 = <b>55</b>. Check: 55 + 35 = 90. "
        "Not 125: that adds. Not 65: that takes the smaller digit from the larger.")
    assert sfl(90, 35) == 65
    assert sfl(925, 350) == 635
    add([350, "=", 925, "−", "w"], 575, sub_cands(925, 350, 575),
        "The = sign can come first. 925 − <i>w</i> = 350, so <i>w</i> = 925 − 350 = <b>575</b>. "
        "Check: 925 − 575 = 350. Not 1275: that adds the two numbers. "
        "Not 635: that takes the smaller digit from the larger in each column.")
    # decimals
    assert holds("n + 2.5 = 7.25", "4.75")
    its.append(mcq(ask(["n", "+", "2.5", "=", "7.25"]), "4.75", ["9.75", "7.00", "5.35"],
                   "Undo + 2.5 by subtracting: <i>n</i> = 7.25 − 2.50 = <b>4.75</b>. Check: 4.75 + 2.5 = 7.25. "
                   "Write 2.5 as 2.50 and line up the decimal points. Not 7.00: that lines up the last digits "
                   "(7.25 − 0.25). Not 9.75: that adds."))
    assert holds("n − 1.2 = 3.45", "4.65")
    its.append(mcq(ask(["n", "−", "1.2", "=", "3.45"]), "4.65", ["2.25", "3.57", "3.65"],
                   "Undo − 1.2 by adding: <i>n</i> = 3.45 + 1.20 = <b>4.65</b>. Check: 4.65 − 1.2 = 3.45. "
                   "Not 2.25: that subtracts. Not 3.57: that lines up the last digits (3.45 + 0.12). "
                   "Not 3.65: that adds only the 0.2."))
    # bar models
    unknown_plus([275, "+", "n", "=", 650], 275, 650, "n", (650, 275, "n"))
    unknown_start(["n", "−", 1400, "=", 2600], 1400, 2600, "n", ("n", 2600, 1400))
    # mistake
    nm, he, his = P.next()
    its.append(mcq("%s solves <i>n</i> + 27 = 63 and gets <i>n</i> = 90. What did %s do wrong?" % (nm, he),
                   cap(he) + " added instead of subtracting",
                   [cap(he) + " subtracted instead of adding", cap(he) + " forgot to carry", "Nothing, 90 is right"],
                   "90 + 27 is 117, not 63. %s used the same operation, <b>addition, instead of the inverse</b>. "
                   "Undo + 27 by subtracting: <i>n</i> = 63 − 27 = 36. Check: 36 + 27 = 63." % cap(he)))
    assert len(its) == 20, len(its)
    return {"title": "Solve equations with + and −", "items": its}


# ============================================================ set 3: × and ÷
def set_mul_div(P):
    its = []

    def coef(parts, a, p, wr, e3):
        ans = p // a
        assert holds(plain(*parts), ans)
        u = letter_in(parts)
        cf = [t for t in parts if isinstance(t, str) and COEF.match(t)]
        intro = ("%s means %d × <i>%s</i>. " % (I(cf[0]), a, u)) if cf else ""
        e = ("%sDivision undoes multiplication: <i>%s</i> = %s = <b>%s</b>. Check: %s. %s"
             % (intro, u, plain(p, "÷", a), n(ans), put(parts, ans), e3))
        its.append(mcq(ask(parts), ans, wr, e))

    coef(["6n", "=", 42], 6, 42, [36, 252, 48],
         "Not 36: that reads 6<i>n</i> as 6 + <i>n</i>. Not 252: that multiplies instead of dividing.")
    coef(["4n", "=", 28], 4, 28, [24, 112, 32],
         "Not 24: that reads 4<i>n</i> as 4 + <i>n</i>. Not 112: that multiplies instead of dividing.")
    coef(["8k", "=", 96], 8, 96, [88, 768, 104],
         "Not 88: that reads 8<i>k</i> as 8 + <i>k</i>. Not 768: that multiplies instead of dividing.")
    coef(["7y", "=", 56], 7, 56, [49, 392, 63],
         "Not 49: that reads 7<i>y</i> as 7 + <i>y</i>. Not 392: that multiplies instead of dividing.")
    coef(["12n", "=", 108], 12, 108, [96, 1296, 120],
         "Not 96: that reads 12<i>n</i> as 12 + <i>n</i>. Not 1296: that multiplies instead of dividing.")
    coef(["5m", "=", 300], 5, 300, [295, 1500, 6],
         "Think 30 tens ÷ 5 = 6 tens. Not 6: that drops the zero. Not 295: that subtracts. Not 1500: that multiplies.")
    coef(["20t", "=", 160], 20, 160, [140, 3200, 80],
         "Think 16 tens ÷ 2 tens = 8. Not 140: that subtracts. Not 3200: that multiplies. "
         "Not 80: that divides by 2 instead of 20.")
    coef(["n", "×", 4, "=", 44], 4, 44, [40, 176, 48],
         "Not 40: that subtracts. Not 176: that multiplies instead of dividing.")
    # n ÷ a = q
    for parts, a, q, wr, e3 in [
        (["n", "÷", 4, "=", 9], 4, 9, [13, 5, 32], "Not 13: that adds. Not 5: that subtracts. Not 32: that is 8 × 4."),
        (["n", "÷", 6, "=", 8], 6, 8, [14, 2, 42], "Not 14: that adds. Not 2: that subtracts. Not 42: that is 7 × 6."),
        (["a", "÷", 3, "=", 15], 3, 15, [5, 18, 12],
         "Not 5: that divides again, the same operation, instead of multiplying. Not 18: that adds."),
        (["p", "÷", 10, "=", 25], 10, 25, [35, 15, 2500],
         "Not 35: that adds. Not 15: that subtracts. Not 2500: that writes one zero too many."),
    ]:
        ans = a * q
        assert holds(plain(*parts), ans)
        u = letter_in(parts)
        e = ("<i>%s</i> is the number you start with. Multiplication undoes division: <i>%s</i> = %s = <b>%s</b>. "
             "Check: %s. %s" % (u, u, plain(q, "×", a), n(ans), put(parts, ans), e3))
        its.append(mcq(ask(parts), ans, wr, e))
    # p ÷ n = q
    for parts, p, q in [([72, "÷", "n", "=", 8], 72, 8), ([48, "÷", "w", "=", 6], 48, 6)]:
        ans = p // q
        assert holds(plain(*parts), ans)
        u = letter_in(parts)
        e = ("Ask: %d divided by what gives %d? <i>%s</i> = %s = <b>%d</b>. Check: %s. "
             "Not %s: that multiplies. Not %s: that subtracts." % (p, q, u, plain(p, "÷", q), ans, put(parts, ans),
                                                                  n(p * q), n(p - q)))
        its.append(mcq(ask(parts), ans, [p * q, p - q, p + q], e))
    # = first
    its.append(mcq(ask([54, "=", "6n"]), 9, [48, 324, 60],
                   "The = sign can come first. 6<i>n</i> = 54, so <i>n</i> = 54 ÷ 6 = <b>9</b>. Check: 6 × 9 = 54. "
                   "Not 48: that reads 6<i>n</i> as 6 + <i>n</i>. Not 324: that multiplies."))
    assert holds("54 = 6n", 9) and holds("7 = n ÷ 8", 56)
    its.append(mcq(ask([7, "=", "n", "÷", 8]), 56, [15, 1, 48],
                   "The = sign can come first. <i>n</i> ÷ 8 = 7, so <i>n</i> = 7 × 8 = <b>56</b>. Check: 56 ÷ 8 = 7. "
                   "Not 15: that adds. Not 1: that subtracts. Not 48: that is 6 × 8."))
    # pictures
    assert holds("3n = 33", 11)
    its.append(mcq("The pans balance. What is <i>n</i>?" + fig(pan_svg("3n", "33")), 11, [30, 99, 36],
                   "3<i>n</i> = 33, so <i>n</i> = 33 ÷ 3 = <b>11</b>. Check: 3 × 11 = 33. "
                   "Not 30: that reads 3<i>n</i> as 3 + <i>n</i>. Not 99: that multiplies."))
    assert holds("5n = 65", 13)
    its.append(mcq("The bar shows 5 equal parts of <i>n</i> that make 65. " + ask(["5n", "=", 65])
                   + fig(parts_svg(5, "n", 65)), 13, [60, 325, 70],
                   "5 equal parts make 65, so <i>n</i> = 65 ÷ 5 = <b>13</b>. Check: 5 × 13 = 65. "
                   "Not 60: that subtracts. Not 325: that multiplies."))
    assert holds("n ÷ 4 = 13", 52)
    its.append(mcq("The bar shows <i>n</i> cut into 4 equal parts of 13. " + ask(["n", "÷", 4, "=", 13])
                   + fig(parts_svg(4, 13, "n")), 52, [17, 9, 48],
                   "<i>n</i> is the whole. Put the 4 parts together: <i>n</i> = 13 × 4 = <b>52</b>. Check: 52 ÷ 4 = 13. "
                   "Not 17: that adds. Not 9: that subtracts. Not 48: that is 12 × 4."))
    # mistake
    nm, he, his = P.next()
    its.append(mcq("%s solves 6<i>n</i> = 48 and gets <i>n</i> = 42. What did %s do wrong?" % (nm, he),
                   cap(he) + " read 6n as 6 + n",
                   [cap(he) + " multiplied instead of dividing", cap(he) + " divided instead of multiplying",
                    "Nothing, 42 is right"],
                   "48 − 6 = 42, so %s solved 6 + <i>n</i> = 48. But <b>6<i>n</i> means 6 × <i>n</i></b>. "
                   "<i>n</i> = 48 ÷ 6 = 8. Check: 6 × 8 = 48." % nm))
    assert len(its) == 20, len(its)
    return {"title": "Solve equations with × and ÷", "items": its}


# ============================================================ set 4: check solutions
def set_check(P):
    its = []

    def item(q, right, wrongs, e):
        its.append(mcq(q, right, wrongs, e))

    def IS(v, parts):
        return "Is <i>%s</i> = %s the solution of %s?" % (letter_in(parts), n(v), html(*parts))

    assert holds("n + 18 = 45", 27) and nocarry(27, 18) == 35
    item(IS(27, ["n", "+", 18, "=", 45]), "Yes, 27 + 18 = 45",
         ["No, 27 + 18 = 35", "No, it should be 63", "No, 45 + 27 = 72"],
         "To check, put the value back into the equation. 27 + 18 = 45, so <b>yes</b>. "
         "27 + 18 = 35 forgets to carry the ten. 63 is 45 + 18, the same operation.")
    assert not holds("n − 12 = 30", 18)
    item(IS(18, ["n", "−", 12, "=", 30]), "No, 18 − 12 = 6",
         ["Yes, 18 + 12 = 30", "Yes, 30 − 12 = 18", "No, 18 − 12 = 4"],
         "Put 18 into the equation: 18 − 12 = 6, not 30. So <b>no</b>. The solution is 30 + 12 = 42. "
         "18 + 12 = 30 and 30 − 12 = 18 are true facts, but they do not put 18 into <i>n</i> − 12 = 30.")
    assert holds("6k = 42", 7)
    item(IS(7, ["6k", "=", 42]), "Yes, 6 × 7 = 42", ["No, 6 + 7 = 13", "No, 6 × 7 = 48", "No, 67 is not 42"],
         "6<i>k</i> means 6 × <i>k</i>. 6 × 7 = 42, so <b>yes</b>. 6 + 7 reads 6<i>k</i> as 6 + <i>k</i>. "
         "67 writes the digits side by side. 6 × 7 is 42, not 48.")
    assert not holds("n ÷ 4 = 8", 2)
    item(IS(2, ["n", "÷", 4, "=", 8]), "No, 2 ÷ 4 is not 8",
         ["Yes, 8 ÷ 4 = 2", "Yes, 2 × 4 = 8", "No, it should be 12"],
         "Put 2 into the equation: 2 ÷ 4 is less than 1, not 8. So <b>no</b>. The solution is 8 × 4 = 32. "
         "8 ÷ 4 = 2 and 2 × 4 = 8 are true facts, but they do not put 2 into <i>n</i> ÷ 4 = 8. 12 adds 8 and 4.")
    assert holds("y + 2.5 = 7.25", "4.75")
    item(IS("4.75", ["y", "+", "2.5", "=", "7.25"]), "Yes, 4.75 + 2.5 = 7.25",
         ["No, 4.75 + 2.5 = 5.00", "No, it should be 9.75", "No, it should be 5.35"],
         "Line up the decimal points: 4.75 + 2.50 = 7.25, so <b>yes</b>. 5.00 lines up the last digits instead. "
         "9.75 adds. 5.35 takes the smaller digit from the larger.")
    assert not holds("n − 15 = 40", 25)
    nm, he, his = P.next()
    item("%s solves <i>n</i> − 15 = 40 and gets <i>n</i> = 25. Check %s answer. What is true?" % (nm, his),
         "Wrong: 25 − 15 = 10, not 40",
         ["Right: 25 + 15 = 40", "Right: 40 − 15 = 25", "Wrong: n should be 45"],
         "Put 25 back into <i>n</i> − 15 = 40: 25 − 15 = 10, not 40. So the answer is <b>wrong</b>. "
         "Undo − 15 by adding: <i>n</i> = 40 + 15 = 55. 45 − 15 is 30, so 45 is wrong too.")
    assert holds("72 ÷ m = 8", 9)
    item(IS(9, [72, "÷", "m", "=", 8]), "Yes, 72 ÷ 9 = 8",
         ["No, 72 ÷ 9 = 7", "No, it should be 576", "No, it should be 64"],
         "Put 9 into the equation: 72 ÷ 9 = 8, so <b>yes</b>. 576 is 72 × 8. 64 is 72 − 8.")
    assert not holds("p + 18000 = 50000", 30000)
    item(IS(30000, ["p", "+", 18000, "=", 50000]), "No, 30" + NB + "000 + 18" + NB + "000 = 48" + NB + "000",
         ["Yes, 30" + NB + "000 + 18" + NB + "000 = 50" + NB + "000", "No, it should be 68" + NB + "000",
          "Yes, it is close to 50" + NB + "000"],
         "30" + NB + "000 + 18" + NB + "000 = 48" + NB + "000, not 50" + NB + "000, so <b>no</b>. Close is not enough: "
         "both sides must be equal. The solution is 50" + NB + "000 − 18" + NB + "000 = 32" + NB + "000.")
    # which equation has this solution
    for v, right, wrongs, e in [
        (6, "7n = 42", ["n + 9 = 14", "n − 4 = 10", "n ÷ 2 = 4"],
         "Put 6 into each one. 7 × 6 = 42, so <b>7<i>n</i> = 42</b>. The others give 6 + 9 = 15, 6 − 4 = 2 and 6 ÷ 2 = 3."),
        (12, "n ÷ 3 = 4", ["3n = 15", "n − 5 = 8", "20 − n = 6"],
         "Put 12 into each one. 12 ÷ 3 = 4, so <b><i>n</i> ÷ 3 = 4</b>. 3<i>n</i> = 15 reads 3<i>n</i> as 3 + <i>n</i>: "
         "3 × 12 is 36. 12 − 5 = 7 and 20 − 12 = 8."),
        (40, "n − 15 = 25", ["n + 15 = 25", "5n = 45", "n ÷ 4 = 8"],
         "Put 40 into each one. 40 − 15 = 25, so <b><i>n</i> − 15 = 25</b>. 5<i>n</i> = 45 reads 5<i>n</i> as 5 + <i>n</i>: "
         "5 × 40 is 200. 40 + 15 = 55 and 40 ÷ 4 = 10."),
    ]:
        assert holds(right, v) and not any(holds(w, v) for w in wrongs)
        item("Which equation has the solution <i>n</i> = %d?" % v, right, wrongs, e)
    # which check is correct
    for q, right, wrongs, e in [
        ("Which check shows that <i>n</i> = 9 solves 8<i>n</i> = 72?", "8 × 9 = 72",
         ["8 + 9 = 17", "72 × 8 = 576", "72 − 9 = 63"],
         "Put 9 in place of <i>n</i> in the equation. 8<i>n</i> is 8 × <i>n</i>, so the check is <b>8 × 9 = 72</b>."),
        ("Which check shows that <i>y</i> = 56 solves <i>y</i> ÷ 7 = 8?", "56 ÷ 7 = 8",
         ["56 × 7 = 392", "56 − 7 = 49", "56 + 7 = 63"],
         "Put 56 in place of <i>y</i> in the equation: <b>56 ÷ 7 = 8</b>. The other facts are true, "
         "but they do not use the operation in the equation."),
        ("Which check shows that <i>n</i> = 325 solves 600 − <i>n</i> = 275?", "600 − 325 = 275",
         ["600 + 325 = 925", "325 − 275 = 50", "275 + 600 = 875"],
         "Put 325 in place of <i>n</i>: <b>600 − 325 = 275</b>. The left side equals the right side, so 325 is the solution."),
    ]:
        for t in [right] + wrongs:
            assert holds(t), t
        item(q, right, wrongs, e)
    # fix it
    nm, he, his = P.next()
    item("%s solves <i>n</i> + 125 = 400 and gets 375. %s check is 375 + 125 = 500. What should %s do?"
         % (nm, cap(his), he),
         "Solve again: n = 275", ["Keep 375, it is close", "Change it to 525", "Change it to 500"],
         "500 is not 400, so the check shows 375 is wrong. Solve again: <i>n</i> = 400 − 125 = <b>275</b>. "
         "Check: 275 + 125 = 400. 525 adds, the same operation.")
    nm, he, his = P.next()
    assert holds("9n = 63", 7)
    item("%s solves 9<i>n</i> = 63 and gets <i>n</i> = 54. The check gives 9 × 54 = 486. What is the correct answer?" % nm,
         "n = 7, because 9 × 7 = 63",
         ["n = 54, because 54 + 9 = 63", "n = 72, because 63 + 9 = 72", "n = 567, because 63 × 9 = 567"],
         "486 is not 63, so 54 is wrong. 9<i>n</i> means 9 × <i>n</i>. <i>n</i> = 63 ÷ 9 = <b>7</b>. Check: 9 × 7 = 63. "
         "54 comes from reading 9<i>n</i> as 9 + <i>n</i>.")
    nm, he, his = P.next()
    assert holds("n ÷ 5 = 9", 45)
    item("%s solves <i>n</i> ÷ 5 = 9 and gets <i>n</i> = 45. %s check is 45 ÷ 5 = 9. What is true?" % (nm, cap(his)),
         "The answer is right", ["It is wrong, n = 14", "It is wrong, n = 4", "The check should be 45 × 5"],
         "The check puts 45 back into the equation: 45 ÷ 5 = 9. Both sides match, so <b>the answer is right</b>. "
         "14 adds and 4 subtracts.")
    nm, he, his = P.next()
    assert not holds("4n = 45", 5)
    item("%s says <i>n</i> = 5 solves 4<i>n</i> = 45, because 4 and 5 make 45. Is %s right?" % (nm, he),
         "No, 4 × 5 = 20, not 45", ["Yes, 4n means 4 and n side by side", "No, 4 + 5 = 9, not 45", "Yes, 45 ends in 5"],
         "4<i>n</i> means 4 × <i>n</i>, not the digits side by side. 4 × 5 = 20, not 45, so <b>no</b>. "
         "4 + 5 is the wrong check: 4<i>n</i> is not 4 + <i>n</i>.")
    assert holds("n + 15 = 30", 15) and holds("n ÷ 3 = 5", 15) and holds("60 − n = 45", 15) and not holds("3n = 18", 15)
    item("<i>n</i> = 15. Which equation is <b>not</b> true?", "3n = 18", ["n + 15 = 30", "n ÷ 3 = 5", "60 − n = 45"],
         "3<i>n</i> = 3 × 15 = 45, not 18, so <b>3<i>n</i> = 18</b> is not true. 18 is 3 + 15. "
         "15 + 15 = 30, 15 ÷ 3 = 5 and 60 − 15 = 45 are all true.")
    nm, he, his = P.next()
    assert holds("4n = 100", 25)
    item("%s tries values in 4<i>n</i> = 100. 4 × 20 = 80 is too small and 4 × 30 = 120 is too big. What is <i>n</i>?" % nm,
         25, [96, 400, 104],
         "<i>n</i> is between 20 and 30. 100 ÷ 4 = <b>25</b>. Check: 4 × 25 = 100. Not 96: that subtracts. "
         "Not 400: that multiplies. Not 104: that adds.")
    assert len(its) == 20, len(its)
    return {"title": "Check solutions", "items": its}


# ============================================================ set 5: stories
def set_words(P):
    its = []

    def match(q, right, wrongs, ans, e):
        assert holds(right, ans), right
        for w in wrongs:
            assert not holds(w, ans), w
        its.append(mcq(q + " Which equation matches?", right, wrongs, e))

    def solve(q, parts, ans, cands, e, unit="", money=False, pic=None):
        assert holds(plain(*parts), ans), parts
        f = (lambda v: "$" + n(v)) if money else (lambda v: n(v) + unit)
        its.append(mcq(q + (fig(pic) if pic else ""), f(ans), [f(c) for c in cands],
                       "Equation: %s. %s" % (html(*parts), e)))

    nm, he, his = P.next()
    match("%s has some hockey cards, <i>c</i>. %s gets 24 more and now has 61." % (nm, cap(he)),
          "c + 24 = 61", ["24 + 61 = c", "c − 24 = 61", "61 + c = 24"], 37,
          "Some cards plus 24 more make 61: <b><i>c</i> + 24 = 61</b>. 61 is the total, not a part. "
          "Then <i>c</i> = 61 − 24 = 37.")
    match("A school orders 6 boxes of pencils with <i>n</i> pencils in each box. There are 144 pencils in all.",
          "6n = 144", ["6 + n = 144", "n ÷ 6 = 144", "144 × 6 = n"], 24,
          "6 equal groups of <i>n</i> make 144: <b>6<i>n</i> = 144</b>. Equal groups mean ×, not +. "
          "Then <i>n</i> = 144 ÷ 6 = 24.")
    match("A class shares a pack of <i>s</i> stickers equally among 4 groups. Each group gets 18 stickers.",
          "s ÷ 4 = 18", ["4s = 18", "18 ÷ 4 = s", "s − 4 = 18"], 72,
          "Start with <i>s</i>, share into 4 groups and get 18 in each: <b><i>s</i> ÷ 4 = 18</b>. "
          "Then <i>s</i> = 18 × 4 = 72.")
    match("A BC Ferries terminal has <i>c</i> cars waiting. 175 cars drive onto the ferry and 290 cars are still waiting.",
          "c − 175 = 290", ["c + 175 = 290", "175 − c = 290", "290 − c = 175"], 465,
          "Start with <i>c</i>, take away 175 and 290 are left: <b><i>c</i> − 175 = 290</b>. "
          "Then <i>c</i> = 290 + 175 = 465.")
    nm, he, his = P.next()
    match("The drive from Kamloops to Prince George is about 520 km. %s’s family has driven <i>d</i> km. "
          "They have 305 km left." % nm,
          "d + 305 = 520", ["520 + 305 = d", "d − 305 = 520", "305 − d = 520"], 215,
          "The part driven plus the part left makes the whole trip: <b><i>d</i> + 305 = 520</b>. "
          "Then <i>d</i> = 520 − 305 = 215 km.")
    match("A bus ticket costs $3. A class pays $84 for <i>t</i> tickets.",
          "3t = 84", ["3 + t = 84", "t ÷ 3 = 84", "84 × 3 = t"], 28,
          "<i>t</i> tickets at $3 each cost 3 × <i>t</i>: <b>3<i>t</i> = 84</b>. Then <i>t</i> = 84 ÷ 3 = 28 tickets.")
    match("“A number minus 2.5 is 4.75.”",
          "n − 2.5 = 4.75", ["2.5 − n = 4.75", "n + 2.5 = 4.75", "n = 2.5 − 4.75"], "7.25",
          "Start with the number <i>n</i>, then subtract 2.5: <b><i>n</i> − 2.5 = 4.75</b>. "
          "Then <i>n</i> = 4.75 + 2.5 = 7.25.")
    match("“Eight times a number is 96.”",
          "8n = 96", ["8 + n = 96", "n ÷ 8 = 96", "n − 8 = 96"], 12,
          "“Eight times a number” is 8 × <i>n</i>, written 8<i>n</i>: <b>8<i>n</i> = 96</b>. Then <i>n</i> = 96 ÷ 8 = 12.")
    # solve
    assert sfl(1000, 375) == 1375
    solve("A Grade 5 class has raised $375 for the Terry Fox Run. The goal is $1000. "
          "Use 375 + <i>m</i> = 1000. How much more do they need to raise?",
          [375, "+", "m", "=", 1000], 625, [1375, 725, 735],
          "<i>m</i> = 1000 − 375 = <b>$625</b>. Check: $375 + $625 = $1000. Not $1375: that adds. "
          "Not $725 or $735: regrouping across the zeros went wrong. 1000 is 9 hundreds, 9 tens and 10 ones.", money=True, pic=bar_svg(1000, 375, "m"))
    assert sfl(4000, 1450) == 3450
    solve("Volunteers count salmon swimming up a creek. They count 1450 salmon in the first week. "
          "After two weeks the total is 4000. How many did they count in the second week?",
          [1450, "+", "n", "=", 4000], 2550, sub_cands(4000, 1450, 2550),
          "<i>n</i> = 4000 − 1450 = <b>2550</b> salmon. Check: 1450 + 2550 = 4000. Not 5450: that adds. "
          "Not 3450: that takes the smaller digit from the larger in each column.")
    solve("A ski school at Whistler puts 84 students into groups of 6. How many groups are there?",
          ["6g", "=", 84], 14, [78, 504, 90],
          "<i>g</i> = 84 ÷ 6 = <b>14</b> groups. Check: 6 × 14 = 84. Not 78: that reads 6<i>g</i> as 6 + <i>g</i>. "
          "Not 504: that multiplies.")
    nm, he, his = P.next()
    solve("%s plants cedar seedlings in 8 equal rows. There are 15 seedlings in each row. "
          "How many seedlings did %s plant?" % (nm, he),
          ["n", "÷", 8, "=", 15], 120, [23, 7, 135],
          "Undo ÷ 8 by multiplying: <i>n</i> = 15 × 8 = <b>120</b> seedlings. Check: 120 ÷ 8 = 15. "
          "Not 23: that adds. Not 7: that subtracts. Not 135: that is 15 × 9.")
    assert sfl(450, 288) == 238
    solve("A theatre in Nanaimo has 450 seats. 288 seats are full. How many seats are empty?",
          [288, "+", "e", "=", 450], 162, sub_cands(450, 288, 162),
          "<i>e</i> = 450 − 288 = <b>162</b> seats. Check: 288 + 162 = 450. Not 738: that adds. "
          "Not 238: that takes the smaller digit from the larger in each column.", pic=bar_svg(450, 288, "e"))
    nm, he, his = P.next()
    solve("%s spends $4.75 on a smoothie and has $10.50 left. How much money did %s have at the start?" % (nm, he),
          ["m", "−", "4.75", "=", "10.50"], "15.25", ["5.75", "14.25", "16.25"],
          "Undo − 4.75 by adding: <i>m</i> = 10.50 + 4.75 = <b>$15.25</b>. Check: $15.25 − $4.75 = $10.50. "
          "Not $5.75: that subtracts. Not $14.25: that forgets to carry.", money=True)
    solve("Juice boxes come in packs of 12. The school needs 180 juice boxes for Sports Day. How many packs does it need?",
          ["12p", "=", 180], 15, [168, 2160, 192],
          "<i>p</i> = 180 ÷ 12 = <b>15</b> packs. Check: 12 × 15 = 180. Not 168: that subtracts. "
          "Not 2160: that multiplies.")
    solve("9 friends share the cost of renting ice time for hockey equally. The rent is $630. How much does each friend pay?",
          ["9c", "=", 630], 70, [621, 5670, 7],
          "<i>c</i> = 630 ÷ 9 = <b>$70</b>. Check: 9 × $70 = $630. Not $621: that subtracts. Not $5670: that multiplies. "
          "Not $7: that drops the zero (63 tens ÷ 9 = 7 tens).", money=True)
    nm, he, his = P.next()
    solve("The seawall around Stanley Park is about 9 km long. %s has biked 3.5 km of it. How far is left?" % nm,
          ["3.5", "+", "d", "=", 9], "5.5", ["12.5", "6.5", "6"],
          "<i>d</i> = 9 − 3.5 = <b>5.5</b> km. Check: 3.5 + 5.5 = 9. Not 12.5: that adds. "
          "Not 6.5: that takes away 3 and then adds 0.5. Not 6: that forgets the 0.5.", unit=" km")
    assert sfl(15000, 8750) == 13750
    solve("A school wants to collect 15" + NB + "000 cans for the food bank. So far it has 8750 cans. "
          "How many more cans does it need?",
          [8750, "+", "c", "=", 15000], 6250, sub_cands(15000, 8750, 6250),
          "<i>c</i> = 15" + NB + "000 − 8750 = <b>6250</b> cans. Check: 8750 + 6250 = 15" + NB + "000. "
          "Not 23" + NB + "750: that adds. Not 13" + NB + "750: that takes the smaller digit from the larger.")
    assert sfl(400000, 125000) == 325000
    solve("A salmon hatchery releases some young salmon in April and 125" + NB + "000 in May. "
          "It releases 400" + NB + "000 in all. How many did it release in April?",
          ["n", "+", 125000, "=", 400000], 275000, sub_cands(400000, 125000, 275000),
          "<i>n</i> = 400" + NB + "000 − 125" + NB + "000 = <b>275" + NB + "000</b>. Check: 275" + NB + "000 + 125"
          + NB + "000 = 400" + NB + "000. Not 525" + NB + "000: that adds. Not 325" + NB + "000: that takes the "
          "smaller digit from the larger.")
    solve("A school library packs 252 books into 9 boxes with the same number in each box. How many books go in each box?",
          ["9b", "=", 252], 28, [243, 2268, 261],
          "<i>b</i> = 252 ÷ 9 = <b>28</b> books. Check: 9 × 28 = 252. Not 243: that reads 9<i>b</i> as 9 + <i>b</i>. "
          "Not 2268: that multiplies.")
    assert len(its) == 20, len(its)
    return {"title": "Write and solve equations for stories", "items": its}


# ============================================================ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    return (
        "<h2>A letter stands for an unknown number</h2>"
        "<p>In <i>n</i> + 20 = 45, the letter <i>n</i> is a <b>variable</b>. It stands for one number we do not know yet. "
        "Any letter can be used. A number right next to a letter means multiply: <b>6<i>n</i> means 6 × <i>n</i></b>, "
        "not 6 + <i>n</i>.</p>"
        "<figure class='sn-fig'>" + pan_svg("n + 20", "45") +
        "<figcaption>The pans balance, so n + 20 = 45. The = sign means both sides are the same.</figcaption></figure>"
        "<h2>Solve it with the inverse</h2>"
        "<p>To find the variable, use the <b>inverse</b> operation, the one that undoes what is done to it.</p>" +
        table(["Equation", "Undo it with", "Do this", "Solution"], [
            [html("n", "+", 18, "=", 45), "−", "45 − 18", "<i>n</i> = 27"],
            [html("n", "−", 12, "=", 30), "+", "30 + 12", "<i>n</i> = 42"],
            [html("6n", "=", 42), "÷", "42 ÷ 6", "<i>n</i> = 7"],
            [html("n", "÷", 4, "=", 9), "×", "9 × 4", "<i>n</i> = 36"],
        ]) +
        "<figure class='sn-fig'>" + parts_svg(6, "n", 42) +
        "<figcaption>6 equal parts of n make 42: 6n = 42, so n = 42 ÷ 6 = 7.</figcaption></figure>" +
        ex("Example", html("n", "÷", 4, "=", 9),
           "<i>n</i> is the number you start with. Undo ÷ 4 by multiplying: 9 × 4 = 36.", "<i>n</i> = 36") +
        "<h2>Check the solution</h2>"
        "<p>Put your answer back into the <b>original equation</b>. If both sides are equal, it is the solution.</p>" +
        ex("Example", "Is <i>n</i> = 7 the solution of 6<i>n</i> = 42?",
           "6<i>n</i> means 6 × <i>n</i>. 6 × 7 = 42. Both sides are 42.", "Yes") +
        "<h2>Write an equation for a story</h2>"
        "<p>Choose a letter for the number you do not know. Joining is +, taking away is −, "
        "equal groups are ×, and sharing equally is ÷.</p>"
        "<figure class='sn-fig'>" + bar_svg(1000, 375, "m") +
        "<figcaption>$375 raised, goal $1000: 375 + m = 1000, so m = 1000 − 375 = 625.</figcaption></figure>" +
        ex("Example", "A school orders 6 boxes of pencils. There are 144 pencils in all. How many are in each box?",
           "Equation: 6<i>n</i> = 144. <i>n</i> = 144 ÷ 6 = 24. Check: 6 × 24 = 144.", "24 pencils") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["6<i>n</i> = 42, so <i>n</i> = 36 (reads 6<i>n</i> as 6 + <i>n</i>)", "6<i>n</i> means 6 × <i>n</i>: 42 ÷ 6 = 7"],
            ["<i>n</i> + 18 = 45, so <i>n</i> = 63 (45 + 18)", "Use the inverse: 45 − 18 = 27"],
            ["6<i>n</i> = 42, so <i>n</i> = 252 (42 × 6)", "Use the inverse: 42 ÷ 6 = 7"],
            ["<i>n</i> ÷ 4 = 8, so <i>n</i> = 2 (8 ÷ 4)", "Undo ÷ 4 by multiplying: 8 × 4 = 32"],
            ["If <i>n</i> = 5, 3<i>n</i> = 35", "3<i>n</i> = 3 × 5 = 15"],
            ["Checking with a different fact, like 8 ÷ 4 = 2", "Put the answer into the original equation"],
        ])
    )


FAQ = [
    {"q": "What are one-step equations with variables in Grade 5 math in BC?",
     "a": "They are equations like n + 18 = 45, 6n = 42 or n ÷ 4 = 9, where a letter stands for one unknown number. The BC Grade 5 Patterning standard asks students to solve them with one inverse operation."},
    {"q": "What does 6n mean in math?",
     "a": "6n means 6 × n. A number written right next to a letter is multiplied by it, so if n = 7, then 6n = 42, not 13 or 67."},
    {"q": "How do you solve n ÷ 4 = 9?",
     "a": "Use the inverse. Multiplication undoes division, so n = 9 × 4 = 36. Check: 36 ÷ 4 = 9."},
    {"q": "How do you check the solution of an equation?",
     "a": "Put the answer back in place of the letter in the original equation. If both sides are equal, the answer is correct; if not, solve again."},
]


def gen_unit():
    rnd = random.Random(55809)
    P = People(rnd)
    sets = [set_letters(P), set_add_sub(P), set_mul_div(P), set_check(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-5", "slug": "one-step-equations-with-variables",
        "sort": 9, "updated": UPDATED, "pdf_url": "",
        "title": "Grade 5 One-Step Equations with Variables",
        "seo_title": "Grade 5 One-Step Equations with Variables Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "One-Step Equations",
        "domain": "Patterning",
        "standard_code": "Grade 5: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/5/core",
        "standard_text": "One-step equations with variables",
        "meta_desc": "Free Grade 5 math worksheets on one-step equations with variables for the BC curriculum: what 6n means, solving n + 18 = 45, n − 12 = 30, 6n = 42 and n ÷ 4 = 9, checking solutions and writing equations for stories. 100 questions with an answer key.",
        "key_big": "A letter stands for an unknown number. Use the inverse operation to find it, then check.",
        "key_sub": "6n means 6 × n. 6n = 42, so n = 42 ÷ 6 = 7. Check: 6 × 7 = 42.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "bar model|pan balance|equal parts bar")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
