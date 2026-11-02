# -*- coding: utf-8 -*-
"""
US Grade 6 Math: Exponents and the Order of Operations (6.EE.A.1)
  python tools/gen_us_math_g6_exponents.py
HTML attributes use single quotes (no backslashes in the JSON).
Exponents are written with <sup> in questions, choices, explanations and the lesson.
title / key_big / key_sub / FAQ / set titles are printed as plain text (escaped), so they use
Unicode superscripts (2³) instead.

Expressions are written in a small source syntax ("3 + 2^3 × 2", "(1/2)^2", "0.3^2"), evaluated
exactly with fractions.Fraction by a step engine and cross-checked with Python eval.
Wrong answers come from real mistakes: base × exponent (2⁵ = 10), working strictly left to right
(adding before the power), multiplying before the power, skipping parentheses, squaring each part
of a sum, wrong number of zeros in powers of 10, misplacing the decimal point, stopping one step early.
Grade 6: whole numbers, fractions and decimals; no negative numbers; no zero exponents.
"""
import json, math, os, random, re
from decimal import Decimal
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
BLUE = "#2f6fb0"
FILL, TOP, SIDE = "#cfe6d6", "#e6f2e9", "#a9d3b6"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
DZX, DZY = 0.55, 0.40

OPEN, CLOSE = ("(", "[", "{"), (")", "]", "}")
MATCH = {")": "(", "]": "[", "}": "{"}
STD = [("^",), ("×", "÷"), ("+", "−")]         # the real order
LTR = [("^", "×", "÷", "+", "−")]              # mistake: strictly left to right
POWLAST = [("×", "÷"), ("^",), ("+", "−")]     # mistake: multiply or divide before the power
REV = [("^",), ("+", "−"), ("×", "÷")]         # mistake: + and − before × and ÷


# ------------------------------------------------------------ numbers
def f(n):
    """4536 -> 4,536."""
    return "{:,}".format(int(n))


def dec(v):
    """Exact decimal: Fraction(9, 100) -> 0.09."""
    v = Fraction(v)
    d = v.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    assert d == 1, v
    s = format(Decimal(v.numerator) / Decimal(v.denominator), "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    whole, _, frac = s.partition(".")
    return f(int(whole)) + ("." + frac if frac else "")


def fr(n, d):
    """Stacked fraction (not simplified, so a mistake like 4/6 can be shown as written)."""
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (n, d)


def frac(v):
    v = Fraction(v)
    if v.denominator == 1:
        return f(v.numerator)
    w, r = divmod(v.numerator, v.denominator)
    return (f(w) + " " if w else "") + fr(r, v.denominator)


def kind_of(s):
    return "frac" if "/" in s else ("dec" if "." in s else "int")


def num(v, kind):
    v = Fraction(v)
    if v.denominator == 1:
        return f(v.numerator)
    return dec(v) if kind == "dec" else frac(v)


def pw(b, n):
    """Power in HTML: 5<sup>3</sup>."""
    return "%s<sup>%d</sup>" % (b if isinstance(b, str) else f(b), n)


# ------------------------------------------------------------ expression engine
TOK = re.compile(r"\(\d+/\d+\)|\d+/\d+|\d[\d,]*(?:\.\d+)?|[×÷+−()\[\]{}^]")


class Calc(Fraction):
    """A number made by an earlier step (not written in the expression)."""


def tokens(s):
    out = []
    for t in TOK.findall(s):
        if t[0].isdigit() or (t[0] == "(" and "/" in t):
            out.append(Fraction(t.strip("()").replace(",", "")))
        else:
            out.append(t)
    assert "".join(TOK.findall(s)) == s.replace(" ", ""), s
    return out


def render(ts, kind):
    out = ""
    for i, t in enumerate(ts):
        if t == "^":
            continue
        if i > 0 and ts[i - 1] == "^":
            out += "<sup>%d</sup>" % t
            continue
        if isinstance(t, Fraction):
            s = num(t, kind)
            if t.denominator != 1 and kind == "frac" and i + 1 < len(ts) and ts[i + 1] == "^":
                s = "(" + s + ")"
        else:
            s = t
        if out and not out.endswith(OPEN) and s not in CLOSE:
            out += " "
        out += s
    return out


def H(s):
    """Source syntax -> HTML."""
    return render(tokens(s), kind_of(s))


def apply(a, op, b, bxe=False):
    if op == "^":
        if bxe:
            return a * b
        if b.denominator != 1 or b < 1 or b > 12:
            return None
        r = a ** int(b)
        return r if r <= 10 ** 7 else None
    if op == "×":
        return a * b
    if op == "÷":
        return a / b if b else None
    if op == "+":
        return a + b
    r = a - b
    return r if r >= 0 else None


def flat_eval(seq, prec, bxe=False):
    seq = list(seq)
    for level in prec:
        i = 1
        while i < len(seq):
            if seq[i] in level:
                v = apply(seq[i - 1], seq[i], seq[i + 1], bxe)
                if v is None:
                    return None
                seq[i - 1:i + 2] = [v]
            else:
                i += 2
    assert len(seq) == 1
    return seq[0]


def ev_tokens(ts, prec=STD, bxe=False):
    ts = list(ts)
    while True:
        j = next((k for k, t in enumerate(ts) if t in CLOSE), None)
        if j is None:
            return flat_eval(ts, prec, bxe)
        i = max(k for k in range(j) if ts[k] in OPEN)
        assert ts[i] == MATCH[ts[j]]
        v = flat_eval(ts[i + 1:j], prec, bxe)
        if v is None:
            return None
        ts[i:j + 1] = [v]


def strip(ts, min_depth=1):
    out, d = [], 0
    for t in ts:
        if t in OPEN:
            d += 1
            if d < min_depth:
                out.append(t)
        elif t in CLOSE:
            if d < min_depth:
                out.append(t)
            d -= 1
        else:
            out.append(t)
    return out


def ev(s, mode="std"):
    ts = tokens(s)
    if mode == "std":
        return ev_tokens(ts)
    if mode == "ltr":
        return ev_tokens(ts, LTR)
    if mode == "powlast":
        return ev_tokens(ts, POWLAST)
    if mode == "rev":
        return ev_tokens(ts, REV)
    if mode == "bxe":
        return ev_tokens(ts, STD, bxe=True)
    if mode == "noparen":
        return ev_tokens(strip(ts))
    if mode == "noinner":
        return ev_tokens(strip(ts, 2))
    raise ValueError(mode)


def py_check(s, v):
    p = []
    for t in tokens(s):
        if isinstance(t, Fraction):
            p.append("Fraction(%d, %d)" % (t.numerator, t.denominator))
        else:
            p.append({"^": "**", "×": "*", "÷": "/", "−": "-", "[": "(", "{": "(", "]": ")", "}": ")"}.get(t, t))
    assert eval(" ".join(p), {"Fraction": Fraction}) == v, (s, v)


def steps(s, values=False):
    """One operation per step, innermost group first."""
    ts, kind = tokens(s), kind_of(s)
    out, made = [], []
    while len(ts) > 1:
        j = next((k for k, t in enumerate(ts) if t in CLOSE), None)
        if j is None:
            lo, hi = 0, len(ts)
        else:
            i = max(k for k in range(j) if ts[k] in OPEN)
            lo, hi = i + 1, j
        seg = ts[lo:hi]
        if len(seg) > 1:
            for level in STD:
                k = next((k for k in range(1, len(seg), 2) if seg[k] in level), None)
                if k is not None:
                    v = apply(seg[k - 1], seg[k], seg[k + 1])
                    assert v is not None, s
                    made.append([x for x in (seg[k - 1], seg[k + 1]) if isinstance(x, Calc)])
                    seg[k - 1:k + 2] = [Calc(v)]
                    break
        if j is not None and len(seg) == 1:
            ts[lo - 1:hi + 1] = seg
        else:
            ts[lo:hi] = seg
        r = render(ts, kind)
        if not out or out[-1] != r:
            out.append(r)
    return made if values else out


def val(s):
    v = ev(s)
    assert v is not None and v > 0, s
    py_check(s, v)
    return v


def chain(s):
    v = val(s)
    st = steps(s)
    assert st[-1] == num(v, kind_of(s)), (s, st)
    return " = ".join([H(s)] + st)


def before_last(s):
    m = steps(s, values=True)
    return max(m[-1]) if m and m[-1] else None


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e):
    """correct + the first 3 unique distractors (no zero or negative amounts). Positions are set by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        lead = re.sub(r"<[^>]+>", "", c).split(" ")[0].lstrip("$").replace(",", "")
        if c in seen or not c or lead.startswith("-") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Exactly 5 correct answers in each position A-D in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            right = it["c"][it["a"]]
            wrong = [x for i, x in enumerate(it["c"]) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def cap(s):
    return s[0].upper() + s[1:]


def B(s):
    return "<b>%s</b>" % s


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


ASK = ["What is the value of %s?", "Evaluate %s.", "Find the value of %s.", "What is %s?"]

WHY = {
    "ltr": "comes from working strictly left to right",
    "powlast": "comes from multiplying or dividing before finding the power",
    "rev": "comes from adding or subtracting before multiplying or dividing",
    "bxe": "comes from multiplying the base by the exponent",
    "noparen": "comes from skipping the parentheses",
    "noinner": "comes from skipping the inner grouping symbols",
}


def mistakes(s, modes, extra=()):
    """Wrong values in order of priority: (value, reason). extra = [(expression, reason)]."""
    v, kind = ev(s), kind_of(s)
    out, seen = [], {v}

    def add(w, why):
        if w is None or w <= 0 or w in seen:
            return
        if kind == "int" and w.denominator != 1:
            return
        if kind == "dec" and w != w.limit_denominator(1000):
            return
        if kind == "dec":
            try:
                dec(w)
            except AssertionError:
                return
        seen.add(w)
        out.append((w, why))

    for m in modes:
        add(ev(s, m), WHY[m])
    for x, why in extra:
        add(ev(x), why)
    add(before_last(s), "stops one step early")
    return out


def eval_item(s, k, modes, extra=(), note=""):
    v, kind = val(s), kind_of(s)
    ms = mistakes(s, modes, extra)
    assert len(ms) >= 3, (s, ms)
    w, why = ms[0]
    e = chain(s) + ". " + (note + " " if note else "") + "Not %s: that %s." % (num(w, kind), why)
    return mcq(ASK[k % len(ASK)] % B(H(s)), num(v, kind), [num(x, kind) for x, _ in ms], e)


def fields(t):
    import string
    return [x[1] for x in string.Formatter().parse(t) if x[1]]


def gen_nums(rnd, maker, ok, used):
    for _ in range(20000):
        d = maker(rnd)
        if ok(d) and d not in used:
            used.add(d)
            return d
    raise RuntimeError("no numbers for line %d" % maker.__code__.co_firstlineno)


def templated(rnd, T, used, vmax=2000, note=""):
    its = []
    for k, (t, modes, extra, mk) in enumerate(T):
        names = fields(t)

        def build(d, t=t, names=names, extra=extra):
            m = dict(zip(names, map(str, d)))
            if "n" in m:
                m["n1"] = str(int(m["n"]) + 1)
            return t.format(**m), [(x.format(**m), why) for x, why in extra]

        def ok(d, t=t, modes=modes, build=build):
            if len(set(d)) != len(d):
                return False
            s, ex_ = build(d)
            v = ev(s)
            if v is None or v <= 1 or (v > vmax and not t.startswith("10^")) or v.denominator != 1:
                return False
            w0 = ev(s, modes[0])
            if w0 is None or w0 <= 0 or w0 == v or w0.denominator != 1:
                return False
            return len(mistakes(s, modes, ex_)) >= 3

        d = gen_nums(rnd, mk, ok, used)
        s, ex_ = build(d)
        its.append(eval_item(s, k, modes, ex_, note))
    return its


# ------------------------------------------------------------ pictures
def tw(t, fs):
    t = str(t)
    return (len(t) - t.count(",") * 0.6 - t.count(" ") * 0.3) * fs * 0.6


class Canvas:
    """Collects shapes and text, tracks the bounding box, then writes a tight SVG."""
    def __init__(self):
        self.el, self.boxes = [], []
        self.x0 = self.y0 = 1e9
        self.x1 = self.y1 = -1e9

    def grow(self, x0, y0, x1, y1):
        self.x0, self.y0 = min(self.x0, x0), min(self.y0, y0)
        self.x1, self.y1 = max(self.x1, x1), max(self.y1, y1)

    def poly(self, pts, fill, sw=1.6, col=GREEN):
        self.el.append(("p", pts, fill, sw, col))
        for x, y in pts:
            self.grow(x - sw, y - sw, x + sw, y + sw)

    def text(self, x, y, t, fs=16, anchor="middle", col=INK):
        """(x, y) is the middle of the text."""
        w = tw(t, fs)
        x0 = x - w / 2 if anchor == "middle" else (x if anchor == "start" else x - w)
        box = (x0, y - fs * 0.5, x0 + w, y + fs * 0.5)
        for b in self.boxes:
            assert box[2] < b[0] or b[2] < box[0] or box[3] < b[1] or b[3] < box[1], (t, box, b)
        self.boxes.append(box)
        self.el.append(("t", x, y + fs * 0.36, t, fs, anchor, col))
        self.grow(*box)

    def svg(self, label, pad=5, square_ok=False):
        ox, oy = self.x0 - pad, self.y0 - pad
        W, H_ = int(math.ceil(self.x1 - ox + pad)), int(math.ceil(self.y1 - oy + pad))
        if W == H_ and not square_ok:
            W += 1
        s = []
        for e in self.el:
            if e[0] == "p":
                s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='%g' stroke-linejoin='round'/>"
                         % (" ".join("%.1f,%.1f" % (x - ox, y - oy) for x, y in e[1]), e[2], e[4], e[3]))
            else:
                _, x, y, t, fs, anchor, col = e
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
                         % (x - ox, y - oy, fs, col, anchor, t))
        return svg_wrap(W, H_, "".join(s), label)


def proj(X, Y, Z, k):
    return (X * k + Z * k * DZX, -Y * k - Z * k * DZY)


def draw_cube(cv, n, k, dx=0.0):
    """n × n × n unit cubes, back to front; faces hidden by a neighbour are left out."""
    keys = {(x, y, z) for x in range(n) for y in range(n) for z in range(n)}
    drawn = 0
    for x, y, z in sorted(keys, key=lambda c: (-c[2], c[1], c[0])):
        p = lambda a, b, c: (proj(x + a, y + b, z + c, k)[0] + dx, proj(x + a, y + b, z + c, k)[1])
        if (x, y, z - 1) not in keys:
            cv.poly([p(0, 0, 0), p(1, 0, 0), p(1, 1, 0), p(0, 1, 0)], FILL)
        if (x, y + 1, z) not in keys:
            cv.poly([p(0, 1, 0), p(1, 1, 0), p(1, 1, 1), p(0, 1, 1)], TOP)
        if (x + 1, y, z) not in keys:
            cv.poly([p(1, 0, 0), p(1, 0, 1), p(1, 1, 1), p(1, 1, 0)], SIDE)
        drawn += 1
    assert drawn == n ** 3
    return proj(n, 0, 0, k)[0] + dx


def draw_square(cv, n, c, x0=0.0, y0=0.0):
    """n × n grid of unit squares; (x0, y0) is the bottom-left corner."""
    for i in range(n):
        for j in range(n):
            x, y = x0 + i * c, y0 - (j + 1) * c
            cv.poly([(x, y), (x + c, y), (x + c, y + c), (x, y + c)], FILL)


def cube_svg(n, label=None):
    cv = Canvas()
    draw_cube(cv, n, k=min(24, 130 / n))
    return cv.svg(label or "cube made of unit cubes, %d on each edge" % n)


def square_svg(n):
    cv = Canvas()
    draw_square(cv, n, c=min(20, 120 / n))
    return cv.svg("square grid of unit squares, %d on each side" % n, square_ok=True)


def square_and_cube_svg():
    """Lesson: 3 × 3 square (3² = 9) next to a 3 × 3 × 3 cube (3³ = 27)."""
    cv = Canvas()
    c = 24
    draw_square(cv, 3, c)
    cv.text(1.5 * c, 18, "3² = 9", 18)
    x0 = 3 * c + 60
    draw_cube(cv, 3, c, dx=x0)
    cv.text(x0 + 1.5 * c, 18, "3³ = 27", 18)
    return cv.svg("a 3 by 3 square of 9 unit squares and a 3 by 3 by 3 cube of 27 unit cubes")


def order_svg():
    """3 + 2³ × 2 worked step by step; the part worked next is red."""
    rows = [("", ["3 + ", ("2³", RED), " × 2"], "exponent first"),
            ("= ", ["3 + ", ("8 × 2", RED)], "then multiply"),
            ("= ", [("3 + 16", RED)], "then add"),
            ("= ", [("19", GREEN)], "")]
    fs, lh = 22, 40
    W, Hh = 400, 16 + lh * len(rows)
    out = []
    for i, (eq, parts, note) in enumerate(rows):
        y = 36 + i * lh
        span = "".join("<tspan fill='%s'>%s</tspan>" % ((p[1], p[0]) if isinstance(p, tuple) else (INK, p)) for p in parts)
        out.append("<text x='34' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='end'>%s</text>" % (y, fs, INK, eq.strip()))
        out.append("<text x='40' y='%d' font-size='%d' font-weight='700' xml:space='preserve'>%s</text>" % (y, fs, span))
        if note:
            out.append("<text text-anchor='end' x='%d' y='%d' font-size='15' fill='%s'>%s</text>" % (W - 8, y - 2, BLUE, note))
    return svg_wrap(W, Hh, "".join(out), "evaluating 3 + 2 cubed times 2 step by step")


# ------------------------------------------------------------ set 1: read and write exponents
def set_read(rnd, P):
    its = []
    # repeated factors -> power
    for b, n in [(5, 3), (2, 6), (7, 4), (3, 4), (10, 4)]:
        prod = " × ".join([f(b)] * n)
        good, swap, signs = pw(b, n), pw(n, b), pw(b, n - 1)
        times = "%s × %d" % (f(b), n)
        assert len({b ** n, n ** b, b ** (n - 1), b * n}) == 4
        its.append(mcq("Which power means %s?" % B(prod), good, [swap, signs, times],
                       "%s is used as a factor %d times, so the base is %s and the exponent is %d: %s. "
                       "Count the factors, not the × signs (there are only %d × signs)." % (f(b), n, f(b), n, good, n - 1)))
    # power -> repeated factors
    for b, n in [(6, 4), (3, 5), (2, 7), (9, 3)]:
        good = " × ".join([f(b)] * n)
        swap = " × ".join([f(n)] * b)
        short = " × ".join([f(b)] * (n - 1))
        times = "%s × %d" % (f(b), n)
        assert len({b ** n, n ** b, b ** (n - 1), b * n}) == 4
        its.append(mcq("Which expression means the same as %s?" % B(pw(b, n)), good, [times, swap, short],
                       "The exponent %d says to use the base %s as a factor %d times: %s. It does not mean %s."
                       % (n, f(b), n, good, times)))
    # base and exponent
    its.append(mcq("In %s, which number is the base?" % B(pw(8, 3)), "8", ["3", "24", "512"],
                   "The base is the big number that is multiplied: 8. The small raised number 3 is the exponent. "
                   "8<sup>3</sup> = 8 × 8 × 8 = 512 is the value."))
    its.append(mcq("In %s, what does the exponent 6 tell you?" % B(pw(4, 6)), "Use 4 as a factor 6 times",
                   ["Multiply 4 by 6", "Use 6 as a factor 4 times", "Add 4 six times"],
                   "The exponent tells how many times the base is used as a factor: 4<sup>6</sup> = 4 × 4 × 4 × 4 × 4 × 4. "
                   "It is not 4 × 6."))
    # words
    its.append(mcq("How do you read %s?" % B(pw(7, 2)), "7 squared", ["7 cubed", "7 times 2", "2 to the 7th power"],
                   "An exponent of 2 is read “squared,” because 7<sup>2</sup> is the area of a square with sides of 7. "
                   "“Cubed” is for an exponent of 3."))
    its.append(mcq("How do you read %s?" % B(pw(2, 5)), "2 to the 5th power",
                   ["5 to the 2nd power", "2 times 5", "2 cubed"],
                   "Read the base first, then the exponent: 2<sup>5</sup> is “2 to the 5th power.” "
                   "It means 2 × 2 × 2 × 2 × 2 = 32."))
    its.append(mcq("Which power is “6 cubed”?", pw(6, 3), [pw(3, 6), "6 × 3", pw(6, 2)],
                   "“Cubed” means an exponent of 3: 6<sup>3</sup> = 6 × 6 × 6 = 216. It is not 6 × 3 = 18."))
    # squares and cubes
    n = 5
    its.append(mcq(fig(square_svg(n)) + "The square is %d units long on each side. Which power shows how many unit squares cover it?" % n,
                   pw(n, 2), [pw(2, n), "%d × 2" % n, pw(n, 3)],
                   "%d rows of %d squares: %d × %d = %s = %d unit squares. That is why an exponent of 2 is called “squared.”"
                   % (n, n, n, n, pw(n, 2), n * n)))
    n = 6
    its.append(mcq(fig(square_svg(n)) + "The square is %d units long on each side. How many unit squares cover it?" % n,
                   "36", ["12", "24", "20"],
                   "%s = 6 × 6 = 36. Not 12: that is 6 × 2. Not 24: that counts the units around the outside (the perimeter)." % pw(6, 2)))
    n = 4
    vis = n ** 3 - (n - 1) ** 3
    assert vis == 37
    its.append(mcq(fig(cube_svg(n)) + "The cube is made of unit cubes, %d on each edge. How many unit cubes make the cube?" % n,
                   "64", ["16", "12", str(vis)],
                   "%s = 4 × 4 × 4 = 64. Not 16: that is only one face. Not %d: that counts only the cubes you can see." % (pw(4, 3), vis)))
    n = 5
    its.append(mcq(fig(cube_svg(n)) + "The cube is made of unit cubes, %d on each edge. Which power shows how many unit cubes make it?" % n,
                   pw(5, 3), [pw(3, 5), pw(5, 2), "5 × 3"],
                   "Each layer has 5 × 5 cubes and there are 5 layers: 5 × 5 × 5 = %s = 125. "
                   "That is why an exponent of 3 is called “cubed.” %s = 25 counts only one face." % (pw(5, 3), pw(5, 2))))
    # two different bases
    for (a, m), (b, n) in [((2, 3), (3, 2)), ((5, 2), (7, 3))]:
        prod = " × ".join([f(a)] * m + [f(b)] * n)
        good = "%s × %s" % (pw(a, m), pw(b, n))
        bad = ["%s + %s" % (pw(a, m), pw(b, n)), "%s × %s" % (pw(a, n), pw(b, m)), pw(a * b, m + n)]
        vals = [a ** m * b ** n, a ** m + b ** n, a ** n * b ** m, (a * b) ** (m + n)]
        assert len(set(vals)) == 4
        its.append(mcq("Which shows %s using exponents?" % B(prod), good, bad,
                       "There are %d factors of %d and %d factors of %d, so the expression is %s. "
                       "The factors are multiplied, so use ×, not +." % (m, a, n, b, good)))
    assert len(its) == 20, len(its)
    return {"title": "Read and write exponents", "items": its}


# ------------------------------------------------------------ set 2: evaluate powers
def set_powers(rnd, P):
    its = []
    for b, n in [(2, 5), (3, 4), (4, 3), (5, 3), (6, 2), (7, 2), (2, 7), (9, 3)]:
        v = b ** n
        cands = [(b * n, "%d × %d" % (b, n)), (n ** b, pw(n, b)), (b ** (n - 1), "one factor too few"),
                 (b + n, "%d + %d" % (b, n)), (b ** (n + 1), "one factor too many")]
        seen, picks = {v}, []
        for w, why in cands:
            if w not in seen:
                seen.add(w)
                picks.append((w, why))
        w, why = picks[0]
        e = "%s = %s = %s. Not %s: that is %s, the base times the exponent." % (pw(b, n), " × ".join([f(b)] * n), f(v), f(w), why)
        its.append(mcq("What is the value of %s?" % B(pw(b, n)), f(v), [f(x) for x, _ in picks[:3]], e))
    for n in (4, 6):
        v = 10 ** n
        its.append(mcq("What is the value of %s?" % B(pw(10, n)), f(v), [f(10 * n), f(10 ** (n - 1)), f(10 ** (n + 1))],
                       "%s = %s = %s: a 1 followed by %d zeros. Not %s: that is 10 × %d."
                       % (pw(10, n), " × ".join(["10"] * n), f(v), n, f(10 * n), n)))
    its.append(mcq("Which is true?", "%s = 1" % pw(1, 8), ["%s = 8" % pw(1, 8), "%s = 2" % pw(0, 2), "%s = 1" % pw(0, 2)],
                   "1<sup>8</sup> = 1 × 1 × 1 × 1 × 1 × 1 × 1 × 1 = 1. Any power of 1 is 1. "
                   "0<sup>2</sup> = 0 × 0 = 0, so it is not 2 or 1."))
    its.append(mcq("Which is true?", "%s = 0" % pw(0, 4), ["%s = 4" % pw(0, 4), "%s = 4" % pw(1, 4), "%s = 1" % pw(4, 1)],
                   "0<sup>4</sup> = 0 × 0 × 0 × 0 = 0. Not 4: that is 0 + 4. "
                   "1<sup>4</sup> = 1 and 4<sup>1</sup> = 4."))
    # fractions
    F = [((2, 3), 2, [fr(4, 3), fr(2, 9), fr(4, 6)],
          "(2/3)<sup>2</sup> = 2/3 × 2/3. Multiply the numerators and the denominators: 2 × 2 = 4 and 3 × 3 = 9. "
          "Not 4/3: that is 2/3 × 2. Not 2/9: square the numerator, too."),
         ((1, 2), 3, [fr(3, 2), fr(1, 6), fr(1, 4)],
          "(1/2)<sup>3</sup> = 1/2 × 1/2 × 1/2 = 1/8. Not 3/2: that is 1/2 × 3. Not 1/6: the denominator is 2 × 2 × 2 = 8, not 2 × 3."),
         ((3, 4), 2, [fr(6, 8), fr(9, 4), fr(3, 16)],
          "(3/4)<sup>2</sup> = 3/4 × 3/4 = 9/16. Not 6/8: that doubles the numerator and denominator. "
          "Square both the numerator and the denominator.")]
    for (a, d), n, bad, e in F:
        s = "(%d/%d)^%d" % (a, d, n)
        v = val(s)
        bad_vals = [Fraction(*map(int, re.findall(r">(\d+)<", x))) for x in bad]
        assert v not in bad_vals and len(set(bad_vals)) == 3, s
        e = e.replace("2/3", fr(2, 3)).replace("1/2", fr(1, 2)).replace("3/4", fr(3, 4)).replace("4/3", fr(4, 3)) \
             .replace("2/9", fr(2, 9)).replace("3/2", fr(3, 2)).replace("1/6", fr(1, 6)).replace("6/8", fr(6, 8)) \
             .replace("9/16", fr(9, 16)).replace("1/8", fr(1, 8))
        its.append(mcq("What is the value of %s?" % B(H(s)), num(v, "frac"), bad, e))
    # decimals
    D = [("0.3^2", ["0.9", "0.6", "0.009"],
          "0.3<sup>2</sup> = 0.3 × 0.3 = 0.09. 3 × 3 = 9, and there are 2 decimal places in all. Not 0.9: count the decimal places."),
         ("0.2^3", ["0.6", "0.08", "0.8"],
          "0.2<sup>3</sup> = 0.2 × 0.2 × 0.2 = 0.008. 2 × 2 × 2 = 8, with 3 decimal places in all. Not 0.6: that is 0.2 × 3."),
         ("1.5^2", ["3", "1.25", "22.5"],
          "1.5<sup>2</sup> = 1.5 × 1.5 = 2.25. Not 3: that is 1.5 × 2. Not 1.25: you cannot square the 1 and the 0.5 separately.")]
    for s, bad, e in D:
        v = val(s)
        assert all(Fraction(x) != v for x in bad) and len(set(map(Fraction, bad))) == 3
        assert dec(v) in e
        its.append(mcq("What is the value of %s?" % B(H(s)), dec(v), bad, e))
    its.append(mcq("Which is greater, %s or %s?" % (B(pw(2, 5)), B(pw(5, 2))), pw(2, 5),
                   [pw(5, 2), "They are equal", "You cannot tell"],
                   "2<sup>5</sup> = 32 and 5<sup>2</sup> = 25, so 2<sup>5</sup> is greater. Switching the base and the exponent changes the value."))
    its.append(mcq("Which power has a value of %s?" % B("1,000"), pw(10, 3), [pw(3, 10), pw(10, 4), pw(10, 2)],
                   "1,000 = 10 × 10 × 10 = 10<sup>3</sup>. The exponent is the number of zeros. "
                   "3<sup>10</sup> = 59,049 is much bigger."))
    assert 3 ** 10 == 59049
    assert len(its) == 20, len(its)
    return {"title": "Evaluate powers", "items": its}


# ------------------------------------------------------------ set 3: order of operations with exponents
def set_order(rnd, P):
    R = rnd.randint
    used = set()
    T = [
        ("{a} + {b}^{n} × {c}", ["ltr", "bxe"], [], lambda r: (R(2, 9), R(2, 3), 3, R(2, 5))),
        ("{a} × {b}^2", ["ltr", "bxe"], [], lambda r: (R(2, 5), R(3, 9))),
        ("{a}^2 + {b}^2", ["bxe"], [("({a} + {b})^2", "comes from adding first, then squaring")], lambda r: (R(2, 9), R(2, 9))),
        ("{a}^{n} − {b} × {c}", ["ltr", "bxe"], [], lambda r: (R(3, 6), 3, R(2, 6), R(2, 9))),
        ("({a} + {b})^2 ÷ {c}", ["noparen", "bxe"], [], lambda r: (R(2, 8), R(2, 8), R(2, 6))),
        ("({a} − {b})^3", ["noparen", "bxe"], [], lambda r: (R(6, 12), R(2, 6))),
        ("{a} × ({b} + {c})^2", ["noparen", "ltr", "bxe"], [], lambda r: (R(2, 5), R(1, 5), R(2, 5))),
        ("{a}^{n} ÷ {b} + {c}", ["bxe", "rev"], [], lambda r: (R(2, 6) * 2, 2, R(2, 4) * 2, R(2, 9))),
        ("{a} + {b}^{n} − {c}", ["ltr", "bxe"], [], lambda r: (R(2, 9), R(2, 5), 3, R(2, 9))),
        ("{a}^2 × {b}^3", ["bxe"], [("{a}^2 + {b}^3", "comes from adding instead of multiplying")], lambda r: (R(2, 5), 2)),
        ("{c} + ({a} + {b})^2", ["noparen", "ltr", "bxe"], [], lambda r: (R(1, 5), R(2, 6), R(5, 20))),
        ("{a}^2 − {b}^2", ["bxe"], [("({a} − {b})^2", "comes from subtracting first, then squaring")], lambda r: (R(6, 12), R(2, 5))),
        ("10^{n} × {a}", ["bxe"], [("10^{n1} × {a}", "has one zero too many")], lambda r: (R(3, 5), R(2, 9))),
        ("{a} × {b}^2 − {c}", ["ltr", "bxe"], [], lambda r: (R(2, 5), R(3, 6), R(2, 9))),
    ]
    its = templated(rnd, T, used, vmax=3000)
    # which part first?
    FIRST = [("4 + 3 × 2^3", "2^3", ["4 + 3", "3 × 2"], "The exponent comes first, before × and +."),
             ("(5 − 2)^2 × 4", "5 − 2", ["2^2", "2 × 4"], "Grouping symbols come first, even before the exponent."),
             ("20 − 2 × 3^2", "3^2", ["20 − 2", "2 × 3"], "The exponent comes first, before × and −.")]
    for s, good, bad, why in FIRST:
        its.append(mcq("Which part of %s do you work out first?" % B(H(s)), H(good), [H(x) for x in bad] + ["Any part first"],
                       "%s. %s" % (chain(s), why)))
    # check a claim: expression, the claimed (wrong) expression, what went wrong, other wrong expressions
    CLAIM = [("2 × 3^2", "6^2", "multiplied 2 × 3 first, but the exponent comes first", ["2 × 6", "3^2"]),
             ("10 − 2^3", "10 − 6", "multiplied the base by the exponent, but 2<sup>3</sup> = 2 × 2 × 2 = 8", ["2^3", "8^3"]),
             ("(2 + 4)^2", "2^2 + 4^2", "squared each number, but the sum must be found first", ["2 + 4^2", "6 × 2"])]
    for s, claim, what, other in CLAIM:
        n, he, his = P.next()
        v, w = val(s), val(claim)
        ws = [val(x) for x in other]
        assert len({v, w} | set(ws)) == 4, s
        its.append(mcq("%s says %s = %s. Is %s right?" % (n, B(H(s)), f(w), he), "No, it is %s" % f(v),
                       ["Yes, it is %s" % f(w)] + ["No, it is %s" % f(x) for x in ws],
                       "%s. %s %s." % (chain(s), n, what)))
    assert len(its) == 20, len(its)
    return {"title": "Order of operations with exponents", "items": its}


# ------------------------------------------------------------ set 4: grouping symbols, fractions and decimals
def set_harder(rnd, P):
    R = rnd.randint
    used = set()
    M = ["noinner", "noparen", "bxe", "ltr"]
    T = [
        ("[{a} + ({b} − {c})^2] ÷ {d}", M, [], lambda r: (R(2, 20), R(5, 9), R(1, 4), R(2, 5))),
        ("{a} × [{b}^2 − ({c} + {d})]", M, [], lambda r: (R(2, 5), R(5, 9), R(2, 6), R(1, 5))),
        ("{a}^2 − [{b} × ({c} − {d})]", M, [], lambda r: (R(7, 12), R(2, 5), R(5, 9), R(1, 4))),
        ("[({a} + {b})^2 − {c}] ÷ {d}", M, [], lambda r: (R(2, 5), R(2, 5), R(1, 9), R(2, 5))),
        ("{{{a} × [{b}^2 − {c}]}} + {d}", M, [], lambda r: (R(2, 5), R(3, 6), R(2, 8), R(2, 20))),
        ("{a} + [{b}^2 ÷ ({c} − {d})]", M, [], lambda r: (R(2, 20), R(4, 12), R(5, 9), R(1, 4))),
        ("[{a}^2 + {b}^2] × {c}", ["bxe", "ltr"], [("({a} + {b})^2 × {c}", "comes from adding first, then squaring")], lambda r: (R(2, 6), R(2, 6), R(2, 5))),
        ("({a} + {b})^2 − {c}^2", ["noparen", "bxe"], [("{a}^2 + {b}^2 − {c}^2", "comes from squaring each number in the parentheses")], lambda r: (R(2, 6), R(2, 6), R(2, 6))),
    ]
    its = templated(rnd, T, used, vmax=2000, note="Work from the inside out.")
    # fractions and decimals (expression, modes, extra wrong expressions)
    FD = [
        ("(2/3)^2 × 9", ["bxe"], [("2/9 × 9", "comes from squaring only the denominator"), ("2/3 × 9", "forgets the exponent")]),
        ("(1/2)^3 + 3/8", ["bxe"], [("1/6 + 3/8", "comes from multiplying the denominator by 3 instead of 2 × 2 × 2")]),
        ("12 × (1/2)^2", ["ltr", "bxe"], []),
        ("0.5^2 + 0.3", ["bxe"], [("2.5 + 0.3", "comes from writing 0.5<sup>2</sup> as 2.5 instead of 0.25")]),
        ("4 × 0.2^2", ["ltr", "bxe"], []),
        ("10^3 × 0.45", ["bxe"], [("100 × 0.45", "uses 100 for 10<sup>3</sup>"), ("10,000 × 0.45", "uses 10,000 for 10<sup>3</sup>")]),
        ("1.2^2 − 0.44", ["bxe"], [("14.4 − 0.44", "puts the decimal point in the wrong place: 1.2<sup>2</sup> = 1.44")]),
        ("(0.3 + 0.1)^2 × 5", ["noparen", "bxe"], [("(0.3^2 + 0.1^2) × 5", "comes from squaring each number in the parentheses")]),
    ]
    for k, (s, modes, extra) in enumerate(FD):
        assert len(mistakes(s, modes, extra)) >= 3, (s, mistakes(s, modes, extra))
        its.append(eval_item(s, k + 1, modes, extra))
    # which expression has the value?
    for good, bad in [("(2 + 4)^2", ["2 + 4^2", "2^2 + 4^2", "2 × 4^2"]),
                      ("2 × (1 + 2)^3", ["2 × 1 + 2^3", "(2 × 1 + 2)^3", "2 + (1 + 2)^3"])]:
        v = val(good)
        assert all(val(b) != v for b in bad) and len({val(b) for b in bad}) == 3
        its.append(mcq("Which expression has a value of %s?" % B(f(v)), H(good), [H(b) for b in bad],
                       "%s. Without the parentheses, %s = %s." % (chain(good), H(bad[0]), f(val(bad[0])))))
    # where do the parentheses go?
    for plain, good, bad in [("2 × 3 + 1^2", "2 × (3 + 1)^2", ["(2 × 3 + 1)^2", "2 × (3 + 1^2)", "(2 × 3) + 1^2"]),
                             ("1 + 3 × 2^3", "(1 + 3) × 2^3", ["(1 + 3 × 2)^3", "1 + (3 × 2)^3", "1 + 3 × (2^3)"])]:
        v = val(good)
        assert all(val(b) != v for b in bad) and len({val(b) for b in bad}) == 3 and val(plain) != v
        its.append(mcq("Where do the parentheses go to make the equation true?<br>%s" % B("%s = %s" % (H(plain), f(v))),
                       H(good), [H(b) for b in bad],
                       "%s. Without parentheses, %s = %s." % (chain(good), H(plain), f(val(plain)))))
    assert len(its) == 20, len(its)
    return {"title": "Grouping symbols, fractions and decimals", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(rnd, P):
    its = []

    def add(q, good, bad, e):
        its.append(mcq(q, good, bad, e))

    def unit(u):
        return lambda x: "%s %s" % (x, u)

    # doubling
    assert val("2^6") == 64
    add("An amoeba splits into 2 amoebas every hour, and each new amoeba does the same. "
        "You start with 1 amoeba. How many amoebas are there after 6 hours?",
        "64", ["12", "32", "36"],
        "Each hour the number doubles: 2 × 2 × 2 × 2 × 2 × 2 = 2<sup>6</sup> = 64. Not 12: that is 2 × 6. Not 32: that is only 5 hours.")
    assert val("5 × 2^4") == 80 and ev("5 × 2^4", "ltr") == 10000
    add("A lab dish has 5 bacteria. The number of bacteria doubles every day. How many bacteria are there after 4 days?",
        "80", ["10,000", "40", "160"],
        "5 × 2<sup>4</sup> = 5 × 16 = 80. Find the power first. Not 10,000: that is (5 × 2)<sup>4</sup>. Not 160: that is 5 days.")
    n, he, his = P.next()
    assert val("2^9") == 512
    add("%s puts 1 penny in a jar on day 1, 2 pennies on day 2, 4 pennies on day 3, and keeps doubling. "
        "How many pennies does %s put in on day 10?" % (n, he),
        "512", ["1,024", "20", "18"],
        "From day 1 to day 10 the amount doubles 9 times, so day 10 is 2<sup>9</sup> = 512 pennies. "
        "Not 1,024: that is one doubling too many.")
    n, he, his = P.next()
    add("%s folds a sheet of paper in half 5 times. Each fold doubles the number of layers. How many layers are there now?" % n,
        "32", ["10", "25", "16"],
        "2 × 2 × 2 × 2 × 2 = 2<sup>5</sup> = 32 layers. Not 10: that is 2 × 5. Not 25: that is 5<sup>2</sup>.")
    n, he, his = P.next()
    add("%s sends a message to 3 friends. In the next round, each of them sends it to 3 new friends, and so on. "
        "How many people get the message in round 4?" % n,
        "81", ["12", "64", "27"],
        "Round 1: 3. Round 2: 3<sup>2</sup> = 9. Round 3: 3<sup>3</sup> = 27. Round 4: 3<sup>4</sup> = 81. Not 12: that is 3 × 4.")
    add("A school has 5 buildings. Each building has 5 floors, each floor has 5 classrooms, and each classroom has 5 windows. "
        "How many windows are there?",
        "625", ["20", "125", "1,024"],
        "5 × 5 × 5 × 5 = 5<sup>4</sup> = 625 windows. Not 125: that is 5<sup>3</sup>, the number of classrooms.")
    assert val("5^4") == 625 and 4 ** 5 == 1024
    # squares and cubes
    sqft, cuin = unit("sq ft"), unit("cu in")
    add("A square garden is 9 ft long on each side. What is its area?",
        sqft(81), [sqft(18), sqft(36), sqft(729)],
        "Area of a square = side × side = 9<sup>2</sup> = 81 sq ft. Not 18 sq ft: that is 9 × 2. 36 is the perimeter in feet.")
    add("A box is a cube with edges 6 in long. What is its volume?",
        cuin(216), [cuin(18), cuin(36), cuin(729)],
        "Volume of a cube = edge × edge × edge = 6<sup>3</sup> = 216 cu in. Not 18: that is 6 × 3. Not 36: that is 6<sup>2</sup>, only one face.")
    add("A square patio is 12 tiles long and 12 tiles wide. How many tiles cover it?",
        "144", ["24", "48", "1,728"],
        "12<sup>2</sup> = 12 × 12 = 144 tiles. Not 48: that is the perimeter, 4 × 12. 1,728 is 12<sup>3</sup>.")
    n3 = 3
    vis = n3 ** 3 - (n3 - 1) ** 3
    assert vis == 19
    add(fig(cube_svg(3, "cube puzzle made of small cubes, 3 on each edge")) +
        "A puzzle cube is made of small cubes, 3 on each edge. How many small cubes make the puzzle?",
        "27", ["9", "19", "54"],
        "3<sup>3</sup> = 3 × 3 × 3 = 27 small cubes. Not 19: that counts only the cubes you can see. Not 54: that counts the squares on all 6 faces.")
    n, he, his = P.next()
    s = "10 × 12 − 6^2"
    assert val(s) == 84
    add("%s puts a square rug with 6 ft sides on a floor that is 10 ft by 12 ft. How many square feet of the floor are not covered?" % n,
        sqft(84), [sqft(108), sqft(36), sqft(156)],
        "%s sq ft. Not 108 sq ft: that uses 6 × 2 for the rug. Not 156 sq ft: subtract the rug, do not add it." % chain(s))
    s = "8^2 − 3^2"
    assert val(s) == 55 and val("(8 − 3)^2") == 25
    add("A square garden with 8 m sides has a square pond with 3 m sides in it. What is the area of the garden without the pond?",
        "55 sq m", ["25 sq m", "10 sq m", "64 sq m"],
        "%s sq m. Not 25 sq m: that is (8 − 3)<sup>2</sup>. Square each side first, then subtract." % chain(s))
    s = "4^3 + 5^3"
    assert val(s) == 189 and val("(4 + 5)^3") == 729
    add("Two boxes are cubes. One has 4 in edges and the other has 5 in edges. What is their total volume?",
        cuin(189), [cuin(729), cuin(27), cuin(41)],
        "%s cu in. Not 729 cu in: that is (4 + 5)<sup>3</sup>. Find each volume first, then add." % chain(s))
    n, he, his = P.next()
    s = "2 × 3^2"
    assert val(s) == 18
    add("%s has 2 square rugs. Each one has 3 ft sides. What is the total area of the rugs?" % n,
        sqft(18), [sqft(36), sqft(12), sqft(9)],
        "%s sq ft. Not 36 sq ft: that is (2 × 3)<sup>2</sup>. Find the power first, then multiply." % chain(s))
    # powers of 10
    s = "6 × 10^3"
    assert val(s) == 6000 and ev(s, "ltr") == 216000
    add("A box holds 10<sup>3</sup> paper clips. How many paper clips are in 6 boxes?",
        "6,000", ["216,000", "180", "600"],
        "%s paper clips. Not 216,000: that is (6 × 10)<sup>3</sup>. Not 180: 10<sup>3</sup> is 1,000, not 30." % chain(s))
    add("A square field has sides of 100 m. What is its area?",
        "10,000 sq m", ["200 sq m", "1,000 sq m", "400 sq m"],
        "100<sup>2</sup> = 100 × 100 = 10,000 sq m, which is 10<sup>4</sup>. Not 200: that is 100 × 2. Not 400: that is the perimeter.")
    # compare areas
    add("A square photo has 5 in sides. It is enlarged so the sides are 10 in. How many times as large is the area now?",
        "4 times", ["2 times", "10 times", "25 times"],
        "Old area: 5<sup>2</sup> = 25 sq in. New area: 10<sup>2</sup> = 100 sq in. 100 ÷ 25 = 4, so 4 times as large. "
        "The sides double, but the area is 2<sup>2</sup> = 4 times as large.")
    add("A chessboard has 8 rows of 8 squares. Which expression shows the number of squares?",
        pw(8, 2), [pw(2, 8), "8 × 2", pw(8, 3)],
        "8 rows of 8 is 8 × 8 = 8<sup>2</sup> = 64 squares. 2<sup>8</sup> = 256 and 8 × 2 = 16 are different.")
    # decimals and fractions
    add("A square tile has sides of 0.5 m. What is its area?",
        "0.25 sq m", ["1 sq m", "2.5 sq m", "0.125 sq m"],
        "0.5<sup>2</sup> = 0.5 × 0.5 = 0.25 sq m. Not 1 sq m: that is 0.5 × 2. Not 2.5: count the decimal places (2 in all).")
    assert val("0.5^2") == Fraction(1, 4) and val("(1/2)^3") == Fraction(1, 8)
    add("A small box is a cube with edges %s ft long. What is its volume?" % fr(1, 2),
        "%s cu ft" % fr(1, 8), ["%s cu ft" % fr(3, 2), "%s cu ft" % fr(1, 6), "%s cu ft" % fr(1, 4)],
        "(%s)<sup>3</sup> = %s × %s × %s = %s cu ft. Not %s: that is %s × 3. Not %s: that is only (%s)<sup>2</sup>."
        % (fr(1, 2), fr(1, 2), fr(1, 2), fr(1, 2), fr(1, 8), fr(3, 2), fr(1, 2), fr(1, 4), fr(1, 2)))
    assert len(its) == 20, len(its)
    return {"title": "Exponent word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    assert val("3 + 2^3 × 2") == 19 and val("(4 + 2)^2 ÷ 3") == 12 and val("0.3^2") == Fraction(9, 100)
    return (
        "<h2>What an exponent means</h2>"
        "<p>An <b>exponent</b> tells how many times to use a number as a factor. "
        "In 5<sup>3</sup>, 5 is the <b>base</b> and 3 is the <b>exponent</b>. "
        "5<sup>3</sup> = 5 × 5 × 5 = 125. The whole thing is called a <b>power</b>.</p>" +
        table(["Power", "Read it as", "Means", "Value"], [
            ["7<sup>2</sup>", "7 squared", "7 × 7", "49"],
            ["5<sup>3</sup>", "5 cubed", "5 × 5 × 5", "125"],
            ["2<sup>5</sup>", "2 to the 5th power", "2 × 2 × 2 × 2 × 2", "32"],
            ["10<sup>4</sup>", "10 to the 4th power", "10 × 10 × 10 × 10", "10,000"],
        ]) +
        "<figure class='sn-fig'>" + square_and_cube_svg() +
        "<figcaption>“Squared” and “cubed” come from shapes: a 3 by 3 square has 3<sup>2</sup> = 9 unit squares, "
        "and a cube with 3 on each edge has 3<sup>3</sup> = 27 unit cubes.</figcaption></figure>"
        "<h2>Evaluate a power</h2>"
        "<p>Write the base as a factor as many times as the exponent says, then multiply.</p>" +
        ex("Whole numbers", "Evaluate 2<sup>5</sup> and 10<sup>4</sup>.",
           "2<sup>5</sup> = 2 × 2 × 2 × 2 × 2 = 32. For 10<sup>4</sup>, write a 1 and 4 zeros: 10,000.", "32 and 10,000") +
        ex("Fractions and decimals", "Evaluate (%s)<sup>2</sup> and 0.3<sup>2</sup>." % fr(2, 3),
           "(%s)<sup>2</sup> = %s × %s = %s. 0.3<sup>2</sup> = 0.3 × 0.3 = 0.09 (2 decimal places in all)."
           % (fr(2, 3), fr(2, 3), fr(2, 3), fr(4, 9)), "%s and 0.09" % fr(4, 9)) +
        "<p>Any power of 1 is 1: 1<sup>8</sup> = 1. Any power of 0 is 0: 0<sup>2</sup> = 0 × 0 = 0.</p>"
        "<h2>The order of operations</h2>" +
        table(["Step", "Do this", "Example"], [
            ["1", "Grouping symbols ( ), [ ], { }, the innermost first", "(4 + 2)<sup>2</sup> = 6<sup>2</sup>"],
            ["2", "Exponents", "6<sup>2</sup> = 36"],
            ["3", "× and ÷, from left to right", "36 ÷ 3 = 12"],
            ["4", "+ and −, from left to right", "3 + 16 = 19"],
        ]) +
        "<p>Many classes remember this as PEMDAS or GEMDAS (Grouping, Exponents, Multiply and Divide, Add and Subtract).</p>"
        "<figure class='sn-fig'>" + order_svg() +
        "<figcaption>3 + 2<sup>3</sup> × 2: find the power first (8), then multiply (16), then add (19).</figcaption></figure>" +
        ex("Example", "Evaluate (4 + 2)<sup>2</sup> ÷ 3.", chain("(4 + 2)^2 ÷ 3") + ".", "12") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["2<sup>5</sup> = 2 × 5 = 10", "Use 2 as a factor 5 times: 2 × 2 × 2 × 2 × 2 = 32"],
            ["3 + 2<sup>3</sup> × 2 = 5<sup>3</sup> × 2", "Find the power before you add: 3 + 8 × 2 = 19"],
            ["2 × 3<sup>2</sup> = 6<sup>2</sup> = 36", "The exponent is only on the 3: 2 × 9 = 18"],
            ["(2 + 4)<sup>2</sup> = 2<sup>2</sup> + 4<sup>2</sup> = 20", "Add inside the parentheses first: 6<sup>2</sup> = 36"],
            ["0.3<sup>2</sup> = 0.9", "0.3 × 0.3 = 0.09"],
            ["10<sup>4</sup> = 1,000", "The exponent is the number of zeros: 10,000"],
        ])
    )


FAQ = [
    {"q": "What is an exponent in 6th grade math?",
     "a": "An exponent tells how many times to use the base as a factor. In 2⁵, the base is 2 and the exponent is 5, so 2⁵ = 2 × 2 × 2 × 2 × 2 = 32."},
    {"q": "Where do exponents go in the order of operations?",
     "a": "Exponents come right after grouping symbols and before multiplication and division. For example, 3 + 2³ × 2 = 3 + 8 × 2 = 3 + 16 = 19."},
    {"q": "Why is 2⁵ not equal to 10?",
     "a": "2⁵ means 2 used as a factor 5 times, not 2 × 5. 2 × 2 × 2 × 2 × 2 = 32. Multiplying the base by the exponent is the most common exponent mistake."},
    {"q": "How do you square a fraction or a decimal?",
     "a": "Multiply it by itself. (2/3)² = 2/3 × 2/3 = 4/9, and 0.3² = 0.3 × 0.3 = 0.09, not 0.9."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(608)
    P = People(rnd)
    sets = [set_read(rnd, P), set_powers(rnd, P), set_order(rnd, P), set_harder(rnd, P), set_story(rnd, P)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "us", "subject": "math", "grade": "grade-6", "slug": "exponents-order-of-operations", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Exponents and the Order of Operations",
        "seo_title": "Grade 6 Exponents Worksheets: Evaluate Powers and Use the Order of Operations",
        "short_title": "Exponents",
        "domain": "Expressions and Equations",
        "standard_code": "6.EE.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/6/EE/A/1/",
        "standard_text": "Write and evaluate numerical expressions involving whole-number exponents.",
        "meta_desc": "Free Grade 6 exponents worksheets: write repeated multiplication as a power, evaluate powers of whole numbers, fractions and decimals, and use the order of operations with exponents. 100 practice questions with step-by-step answers.",
        "key_big": "An exponent tells how many times to use the base as a factor: 2⁵ = 2 × 2 × 2 × 2 × 2 = 32.",
        "key_sub": "2⁵ is not 2 × 5. In the order of operations, exponents come right after grouping symbols: 3 + 2³ × 2 = 3 + 8 × 2 = 19.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    # The print sheet lays out each choice as an inline-flex box (.pr-ch > span), which would turn a bare
    # <sup> into its own flex item on the baseline. One wrapping span keeps the exponent raised.
    for st in sets:
        for it in st["items"]:
            it["c"] = ["<span>%s</span>" % c if "<sup>" in c else c for c in it["c"]]
    return mark_large(u, "cube")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
