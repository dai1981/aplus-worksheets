# -*- coding: utf-8 -*-
"""
US Grade 6 Math: Writing, Reading and Evaluating Expressions with Variables (6.EE.A.2a–c)
  python tools/gen_us_math_g6_expressions.py
HTML attributes use single quotes (no backslashes in the JSON).
Expressions are written in a small plain notation ("3n + 4", "s^2", "[3/4]x") and turned into HTML.
Every value is found step by step by a small engine and cross-checked with Python eval on Fractions.
Wrong answers come from real mistakes: "3 less than y" as 3 − y, reading 3n as 35 when n = 5,
mixing up the coefficient and the constant, s² as 2s, adding before multiplying.
"""
import json, os, random, re
from decimal import Decimal
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
BLUE = "#2f6fb0"
FILL = "#e8f3ec"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
LETTERS = ["n", "x", "y", "k", "m", "p", "t", "w", "c", "d", "z", "h", "r", "b", "g", "q"]


# ------------------------------------------------------------ numbers
def f(n):
    return "{:,}".format(int(n))


def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def dec(v):
    """Exact decimal text of a Fraction (terminating only): 9/4 -> 2.25."""
    v = Fr(v)
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


def mixed(v):
    v = Fr(v)
    if v.denominator == 1:
        return f(v)
    w, r = divmod(v.numerator, v.denominator)
    return (f(w) + " " if w else "") + fr(r, v.denominator)


def show(v, mode="f"):
    v = Fr(v)
    if v.denominator == 1:
        return f(v)
    return dec(v) if mode == "d" else mixed(v)


def money(v, cents=False):
    v = Fr(v)
    if v.denominator == 1 and not cents:
        return "$" + f(v)
    s = dec(v)
    if "." not in s:
        s += ".00"
    elif len(s.split(".")[1]) == 1:
        s += "0"
    return "$" + s


# ------------------------------------------------------------ plain notation -> HTML
TOK = re.compile(r"\[\d+(?: \d+)?/\d+\]|\d+(?:\.\d+)?|[a-z]|[()+×÷−^]")


class Num:
    def __init__(self, v, html=None):
        self.v = Fr(v)
        self.html = html


def lit(t):
    """A literal number token: '7', '2.5', '[3/4]', '[3 1/2]'."""
    if t[0] == "[":
        body = t[1:-1]
        w = 0
        if " " in body:
            w, body = body.split(" ")
            w = int(w)
        a, b = map(int, body.split("/"))
        h = (f(w) + " " if w else "") + fr(a, b)
        return Num(w + Fr(a, b), h)
    if "." in t:
        return Num(Fr(t), dec(Fr(t)))
    return Num(int(t), f(int(t)))


def tokenize(s):
    out = []
    for t in TOK.findall(s):
        if t[0].isdigit() or t[0] == "[":
            t = lit(t)
        if out:
            p = out[-1]
            left = isinstance(p, Num) or p == ")" or (isinstance(p, str) and p.isalpha())
            right = (isinstance(t, str) and (t.isalpha() or t == "(")) or (isinstance(t, Num) and isinstance(p, str) and p.isalpha())
            if left and right:
                out.append("·")          # implicit multiplication (3n, 2(x + 1), xy)
        out.append(t)
    return out


def render(ts, mode="f"):
    """Token list -> HTML. '·' is implicit (nothing shown); letters in italics; ^ as <sup>."""
    out = ""
    i = 0
    while i < len(ts):
        t = ts[i]
        if t == "^":
            e = ts[i + 1]
            out += "<sup>%s</sup>" % (e.html or show(e.v, mode))
            i += 2
            continue
        if isinstance(t, Num):
            piece = t.html or show(t.v, mode)
        elif t == "·":
            piece = ""
        elif t.isalpha():
            piece = "<i>%s</i>" % t
        else:
            piece = t
        if t in ("+", "−", "×", "÷", "="):
            out += " " + piece + " "
        else:
            out += piece
        i += 1
    return out


def E(s):
    """Plain expression -> HTML."""
    return render(tokenize(s))


# ------------------------------------------------------------ evaluation
def subst(s, env):
    """Replace each letter with its value; implicit multiplication becomes ×.
    A fraction, mixed number or decimal raised to a power gets parentheses."""
    ts = tokenize(s)
    out = []
    for i, t in enumerate(ts):
        if t == "·":
            out.append("×")
        elif isinstance(t, str) and t.isalpha():
            v = Fr(env[t]) if not isinstance(env[t], str) else Fr(env[t])
            html = None
            if isinstance(env[t], str) and "." in env[t]:
                html = dec(Fr(env[t]))
            n = Num(v, html)
            nxt = ts[i + 1] if i + 1 < len(ts) else None
            if nxt == "^" and v.denominator != 1 and not html:
                out += ["(", n, ")"]
            else:
                out.append(n)
        else:
            out.append(t)
    return out


def apply(a, op, b):
    if op == "^":
        return a ** int(b)
    if op == "×":
        return a * b
    if op == "÷":
        return a / b
    if op == "+":
        return a + b
    return a - b


def step(ts):
    """One operation: innermost group first; ^, then × ÷, then + − (left to right)."""
    ts = list(ts)
    j = next((k for k, t in enumerate(ts) if t == ")"), None)
    if j is None:
        lo, hi = 0, len(ts)
    else:
        lo = max(k for k in range(j) if ts[k] == "(")
        lo, hi = lo + 1, j
    seg = ts[lo:hi]
    if len(seg) == 1:
        if hi + 1 < len(ts) and ts[hi + 1] == "^":       # (3/4)^2
            ts[lo - 1:hi + 3] = [Num(seg[0].v ** int(ts[hi + 2].v))]
        else:
            ts[lo - 1:hi + 1] = seg
        return ts
    for level in (("^",), ("×", "÷"), ("+", "−")):
        k = next((k for k in range(1, len(seg), 2) if seg[k] in level), None)
        if k is not None:
            seg[k - 1:k + 2] = [Num(apply(seg[k - 1].v, seg[k], seg[k + 1].v))]
            break
    if j is not None and len(seg) == 1 and not (hi + 1 < len(ts) and ts[hi + 1] == "^" and seg[0].v.denominator != 1):
        ts[lo - 1:hi + 1] = seg
    else:
        ts[lo:hi] = seg
    return ts


def py_val(s, env):
    """Independent check: Python eval on Fractions (no use of the step engine)."""
    vals = []

    def hold(v):
        vals.append(Fr(v))
        return " _%d_ " % (len(vals) - 1)
    p = re.sub(r"\[(\d+) (\d+)/(\d+)\]", lambda m: hold(int(m.group(1)) + Fr(int(m.group(2)), int(m.group(3)))), s)
    p = re.sub(r"\[(\d+)/(\d+)\]", lambda m: hold(Fr(int(m.group(1)), int(m.group(2)))), p)
    p = re.sub(r"(?<![_\d])\d+(?:\.\d+)?(?![_\d.])", lambda m: hold(Fr(m.group(0))), p)
    p = re.sub(r"[a-z]", lambda m: hold(Fr(env[m.group(0)])), p)
    p = re.sub(r"(_\d+_|\))\s*(?=_\d+_|\()", r"\1*", p)
    p = re.sub(r"(_\d+_|\))\s*(?=_\d+_|\()", r"\1*", p)
    p = re.sub(r"_(\d+)_", r"V[\1]", p)
    p = p.replace("×", "*").replace("÷", "/").replace("−", "-").replace("^", "**")
    return eval(p, {"V": vals})


def evaluate(s, env, mode="f"):
    """Returns (value, HTML chain 'substituted = step = ... = value')."""
    ts = subst(s, env)
    parts = [render(ts, mode)]
    while len(ts) > 1:
        ts = step(ts)
        r = render(ts, mode)
        if r != parts[-1]:
            parts.append(r)
    v = ts[0].v
    assert py_val(s, env) == v, (s, env, v, py_val(s, env))
    return v, " = ".join(parts)


def val(s, env):
    return evaluate(s, env)[0]


def same(a, b, letters):
    """Do two plain expressions always have the same value? (checked at three test points)"""
    for seed in (1, 2, 3):
        rr = random.Random(seed)
        env = {k: str(Fr(rr.randint(11, 97), rr.choice([7, 13, 3]))) for k in letters}
        env = {k: Fr(v) for k, v in env.items()}
        if py_val(a, env) != py_val(b, env):
            return False
    return True


# ------------------------------------------------------------ question helpers
def mcq(q, correct, wrong, e):
    seen = {re.sub(r"<[^>]+>", "", correct)}
    pick = []
    for c in wrong:
        k = re.sub(r"<[^>]+>", "", c)
        if k in seen:
            continue
        seen.add(k)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, wrong)
    return {"q": q, "c": pick + [correct], "a": 3, "e": e}


def mcq_val(q, v, wrong, e, fmt=show):
    """Number answers: 3 wrong values from real mistakes (positive, different from each other and from v)."""
    ws = []
    for w in wrong:
        if w is None:
            continue
        w = Fr(w)
        if w > 0 and w != v and w not in ws:
            ws.append(w)
    assert len(ws) >= 3, (q, v, wrong)
    return mcq(q, fmt(v), [fmt(w) for w in ws[:3]], e)


def mcq_expr(q, good, bad, e, letters):
    """Expression answers: no wrong choice is equivalent to the right one or to another wrong one."""
    allx = [good] + bad
    for i in range(len(allx)):
        for j in range(i + 1, len(allx)):
            assert not same(allx[i], allx[j], letters), (q, allx[i], allx[j])
    return mcq(q, E(good), [E(b) for b in bad], e)


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


def join(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def B(s):
    return "<b>%s</b>" % s


def V(x):
    return "<i>%s</i>" % x


def cat(*xs):
    """Reading digits side by side as one number: 3 and 5 -> 35."""
    return int("".join(str(int(x)) for x in xs))


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            rest = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(rest)
            rest.insert(t, c[it["a"]])
            it["c"] = rest
            it["a"] = t


# ------------------------------------------------------------ figures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label, sq=False):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=15, anchor="middle", bold=False, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def tw(t, fs):
    return len(re.sub(r"<[^>]+>", "", t)) * fs * 0.6


def label(x, y, lab, anchor="middle", col=INK):
    """lab = (value, unit). A fraction or mixed number is drawn stacked, like on paper.
    Returns (svg, width, plain text)."""
    v, unit = lab
    if isinstance(v, str) or Fr(v).denominator == 1:
        t = "%s %s" % (v if isinstance(v, str) else f(v), unit)
        w = tw(t, 15)
        x0 = {"middle": x - w / 2, "start": x, "end": x - w}[anchor]
        return text(x0, y, t, anchor="start", col=col), w, t
    v = Fr(v)
    wh, r = divmod(v.numerator, v.denominator)
    d = v.denominator
    ww = tw(str(wh), 15) + 3 if wh else 0
    fw = max(len(str(r)), len(str(d))) * 8 + 4
    uw = tw(" " + unit, 15)
    w = ww + fw + uw
    x0 = {"middle": x - w / 2, "start": x, "end": x - w}[anchor]
    out = text(x0, y, str(wh), anchor="start", col=col) if wh else ""
    fx = x0 + ww + fw / 2
    out += text(fx, y - 7, str(r), fs=14, col=col) + text(fx, y + 11, str(d), fs=14, col=col)
    out += "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.3'/>" % (fx - fw / 2 + 1, y - 3, fx + fw / 2 - 1, y - 3, col)
    out += text(x0 + ww + fw + 4, y, unit, anchor="start", col=col)
    plain = "%s%d/%d %s" % ("%d " % wh if wh else "", r, d, unit)
    return out, w, plain


def frac_lab(lab):
    v = lab[0]
    return not isinstance(v, str) and Fr(v).denominator != 1


def square_svg(lab):
    sv, w, t = label(0, 0, lab)
    W = int(max(90, w + 12))
    x0 = (W - 60) / 2
    yl = 88 if frac_lab(lab) else 86
    sv, w, t = label(W / 2, yl, lab)
    body = "<rect x='%.1f' y='6' width='60' height='60' fill='%s' stroke='%s' stroke-width='2'/>" % (x0, FILL, GREEN) + sv
    return svg_wrap(W, yl + (16 if frac_lab(lab) else 8), body, "square with side " + t)


def cube_svg(lab):
    s, dx, dy = 54, 20, 16
    x0, y0 = 20, 6 + dy
    p = lambda pts: " ".join("%.1f,%.1f" % q for q in pts)
    front = [(x0, y0), (x0 + s, y0), (x0 + s, y0 + s), (x0, y0 + s)]
    top = [(x0, y0), (x0 + dx, y0 - dy), (x0 + s + dx, y0 - dy), (x0 + s, y0)]
    side = [(x0 + s, y0), (x0 + s + dx, y0 - dy), (x0 + s + dx, y0 + s - dy), (x0 + s, y0 + s)]
    st = "stroke='%s' stroke-width='2' stroke-linejoin='round'" % GREEN
    sv, w, t = label(x0 + s / 2, y0 + s + 20, lab)
    body = ("<polygon points='%s' fill='%s' %s/>" % (p(front), FILL, st) +
            "<polygon points='%s' fill='#d3eadb' %s/>" % (p(top), st) +
            "<polygon points='%s' fill='#c2e0cc' %s/>" % (p(side), st) + sv)
    W = max(x0 + s + dx + 12, int(x0 + s / 2 + w / 2) + 6)
    return svg_wrap(W, y0 + s + 28, body, "cube with edge " + t)


def rect_svg(llab, wlab):
    rw, rh = 112, 58
    x0, y0 = 8, 6
    fr_ = frac_lab(llab) or frac_lab(wlab)
    sl, lw, lt = label(x0 + rw / 2, y0 + rh + (22 if fr_ else 20), llab)
    sw, ww, wt = label(x0 + rw + 8, y0 + rh / 2 + 5, wlab, anchor="start")
    body = ("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (x0, y0, rw, rh, FILL, GREEN) + sl + sw)
    W = int(x0 + rw + 8 + ww + 6)
    return svg_wrap(W, y0 + rh + (36 if fr_ else 28), body, "rectangle with length %s and width %s" % (lt, wt))


def triangle_svg(blab, hlab):
    """Right triangle: the height is the left side, the base is the bottom side."""
    sh, hw, ht = label(0, 0, hlab)
    bw, h = 120, 70
    x0, y0 = int(hw) + 14, 8
    sh, hw, ht = label(x0 - 8, y0 + h / 2 + 5, hlab, anchor="end", col=BLUE)
    sb, bww, bt = label(x0 + bw / 2, y0 + h + 20, blab)
    pts = "%d,%d %d,%d %d,%d" % (x0, y0, x0, y0 + h, x0 + bw, y0 + h)
    body = ("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2' stroke-linejoin='round'/>" % (pts, FILL, GREEN) +
            "<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='1.3'/>" % (x0, y0 + h - 10, x0 + 10, y0 + h - 10, x0 + 10, y0 + h, GREEN) +
            sh + sb)
    return svg_wrap(x0 + bw + 8, y0 + h + 28, body, "right triangle with base %s and height %s" % (bt, ht))


def parts_svg():
    """3n + 4 with its parts labeled."""
    W, H = 400, 150
    xs = {"3": 150, "n": 172, "+": 208, "4": 246}
    body = ""
    body += text(xs["3"], 78, "3", fs=34, bold=True, col=RED)
    body += "<text x='%d' y='78' font-size='34' font-weight='700' font-style='italic' fill='%s' text-anchor='middle'>n</text>" % (xs["n"], INK)
    body += text(xs["+"], 78, "+", fs=34, bold=True)
    body += text(xs["4"], 78, "4", fs=34, bold=True, col=BLUE)
    # braces over the terms
    for x1, x2, lab in ((136, 186, "term"), (232, 260, "term")):
        body += "<path d='M%d 44 L%d 36 L%d 36 L%d 44' fill='none' stroke='%s' stroke-width='1.5'/>" % (x1, x1, x2, x2, GREEN)
        body += text((x1 + x2) / 2, 26, lab, fs=15, col=GREEN)
    # labels below
    body += "<line x1='%d' y1='88' x2='%d' y2='112' stroke='%s' stroke-width='1.5'/>" % (xs["3"], 96, RED)
    body += text(80, 130, "coefficient", fs=15, col=RED)
    body += "<line x1='%d' y1='88' x2='%d' y2='112' stroke='%s' stroke-width='1.5'/>" % (xs["n"], 196, INK)
    body += text(200, 130, "variable", fs=15)
    body += "<line x1='%d' y1='88' x2='%d' y2='112' stroke='%s' stroke-width='1.5'/>" % (xs["4"], 312, BLUE)
    body += text(320, 130, "constant", fs=15, col=BLUE)
    return svg_wrap(W, H, body, "the parts of 3n + 4")


# ------------------------------------------------------------ set 1: words -> expressions
# (phrase, right expression, wrong expressions, explanation); {v} {w} letters, {a} {b} numbers
WORDS = [
    ("{a} more than {v}", "{v} + {a}", ["{a}{v}", "{v} − {a}", "{a} − {v}"],
     "“More than” means add: start with {V} and add {a}, so {R}. {X0} would mean {a} × {V}."),
    ("the product of {a} and {v}", "{a}{v}", ["{a} + {v}", "{v} − {a}", "{v} ÷ {a}"],
     "“Product” means multiply: {a} × {V}. A number next to a letter means multiply, so write {R}."),
    ("{a} less than {v}", "{v} − {a}", ["{a} − {v}", "{v} + {a}", "{a}{v}"],
     "“{a} less than {V}” starts with {V} and takes {a} away: {R}. {X0} has the order backward."),
    ("the sum of {v} and {a}", "{v} + {a}", ["{a}{v}", "{v} − {a}", "{v} ÷ {a}"],
     "“Sum” means add: {R}. {X0} is a product, not a sum."),
    ("{v} divided by {a}", "{v} ÷ {a}", ["{a} ÷ {v}", "{a}{v}", "{v} − {a}"],
     "The number being divided comes first: {R}. {X0} divides {a} by {V}, which is different."),
    ("twice {v}", "2{v}", ["{v} + 2", "{v}^2", "{v} ÷ 2"],
     "“Twice” means 2 times: 2 × {V} = {R}. {X1} means {V} × {V}, not 2 × {V}."),
    ("{v} decreased by {a}", "{v} − {a}", ["{a} − {v}", "{v} + {a}", "{v} ÷ {a}"],
     "“Decreased by {a}” means take {a} away from {V}: {R}. {X0} has the order backward."),
    ("{v} squared", "{v}^2", ["2{v}", "{v} + 2", "{v} ÷ 2"],
     "“Squared” means multiply the number by itself: {V} × {V} = {R}. {X0} means 2 × {V}, which is a different value."),
    ("subtract {v} from {a}", "{a} − {v}", ["{v} − {a}", "{v} + {a}", "{a}{v}"],
     "“Subtract {V} from {a}” means start with {a} and take {V} away: {R}, not {X0}."),
    ("{v} increased by {a}", "{v} + {a}", ["{v} − {a}", "{a}{v}", "{a} − {v}"],
     "“Increased by” means add: {R}. {X1} would mean {a} × {V}."),
    ("half of {v}", "{v} ÷ 2", ["2{v}", "{v} − 2", "2 ÷ {v}"],
     "Half of a number means divide it by 2: {R}. {X0} would be twice the number."),
    ("the quotient of {a} and {v}", "{a} ÷ {v}", ["{v} ÷ {a}", "{a}{v}", "{a} − {v}"],
     "“Quotient” means divide, and the first number named is divided: {R}. {X0} has the order backward."),
    ("{v} cubed", "{v}^3", ["3{v}", "{v} + 3", "{v}^2"],
     "“Cubed” means use the number as a factor 3 times: {V} × {V} × {V} = {R}. {X0} means 3 × {V}."),
    ("{a} times the sum of {v} and {b}", "{a}({v} + {b})", ["{a}{v} + {b}", "{a} + {v} + {b}", "{b}({v} + {a})"],
     "The sum {V} + {b} must be found first, so it goes in parentheses: {R}. {X0} multiplies only {V} by {a}."),
    ("{b} more than {a} times {v}", "{a}{v} + {b}", ["{a}({v} + {b})", "{a}{v} − {b}", "{b}{v} + {a}"],
     "{a} times {V} is {a}{V}. {b} more than that means add {b}: {R}. No parentheses are needed, because you multiply first anyway."),
    ("{a} fewer than the product of {b} and {v}", "{b}{v} − {a}", ["{a} − {b}{v}", "{b}({v} − {a})", "{b}{v} + {a}"],
     "The product of {b} and {V} is {b}{V}. “{a} fewer than” it means take {a} away: {R}, not {X0}."),
    ("triple {v}, then subtract {b}", "3{v} − {b}", ["3({v} − {b})", "{b} − 3{v}", "{v}^3 − {b}"],
     "Triple means 3 times: 3{V}. Then subtract {b}: {R}. {X2} would cube {V}, not triple it."),
    ("the quotient of {v} and {a}, plus {b}", "{v} ÷ {a} + {b}", ["{v} ÷ ({a} + {b})", "{a} ÷ {v} + {b}", "{a}{v} + {b}"],
     "The quotient of {V} and {a} is {V} ÷ {a}. Then add {b}: {R}. {X0} would add {a} + {b} first."),
    ("the sum of {v} and {w}, divided by {a}", "({v} + {w}) ÷ {a}", ["{v} + {w} ÷ {a}", "{a} ÷ ({v} + {w})", "{v} + {w} − {a}"],
     "The whole sum is divided, so it goes in parentheses: {R}. {X0} would divide only {W} by {a}."),
]


def set_words(rnd, P):
    its = []
    letters = list(LETTERS)
    rnd.shuffle(letters)
    used = set()
    # what does 3n mean?
    a = 3
    its.append(mcq_expr("What does %s mean?" % B(E("3n")), "3 × n", ["3 + n", "n − 3", "n ÷ 3"],
                        "A number written right next to a letter means multiply: 3%s = 3 × %s. "
                        "So when %s = 5, 3%s = 3 × 5 = 15, not 35." % (V("n"), V("n"), V("n"), V("n")), ["n"]))
    for k, (ph, good, bad, e) in enumerate(WORDS):
        v = letters[k % len(letters)]
        w = letters[(k + 5) % len(letters)]
        while True:
            a, b = rnd.randint(2, 9), rnd.randint(2, 12)
            if ph.startswith("subtract"):
                a = rnd.randint(15, 30)
            if a != b and (ph, a, b) not in used and a != 2:
                used.add((ph, a, b))
                break
        m = {"a": a, "b": b, "v": v, "w": w}
        g = good.format(**m)
        bs = [x.format(**m) for x in bad]
        hm = {"a": a, "b": b, "V": V(v), "W": V(w), "R": E(g)}
        for i, x in enumerate(bs):
            hm["X%d" % i] = E(x)
        its.append(mcq_expr("Which expression means %s?" % B(ph.format(a=a, b=b, v=V(v), w=V(w))), g, bs,
                            e.format(**hm), [v, w]))
    assert len(its) == 20, len(its)
    return {"title": "Write expressions from words", "items": its}


# ------------------------------------------------------------ set 2: parts of an expression, expressions -> words
def set_parts(rnd, P):
    its = []
    R = rnd.randint
    a, b, c = 4, 7, 2
    s = "%dx + %dy + %d" % (a, b, c)
    its.append(mcq("How many terms are in %s?" % B(E(s)), "3", ["2", "5", "4"],
                   "Terms are the parts joined by + or −: %s, %s and %d. That is 3 terms." % (E("%dx" % a), E("%dy" % b), c)))
    a, b = R(3, 9), R(10, 15)
    s = "%dm + %d" % (a, b)
    its.append(mcq("What is the coefficient of %s in %s?" % (V("m"), B(E(s))), str(a), [str(b), V("m"), str(a + b)],
                   "The coefficient is the number multiplied by the variable: %s means %d × %s, so it is %d. %d is the constant."
                   % (E("%dm" % a), a, V("m"), a, b)))
    a, b = R(3, 9), R(10, 15)
    s = "%dk + %d" % (a, b)
    its.append(mcq("What is the constant in %s?" % B(E(s)), str(b), [str(a), E("%dk" % a), str(a + b)],
                   "The constant is the term with no variable. It always stays %d. %d is the coefficient of %s." % (b, a, V("k"))))
    b = R(4, 15)
    its.append(mcq("What is the coefficient of %s in %s?" % (V("p"), B(E("p + %d" % b))), "1", ["0", str(b), V("p")],
                   "%s means 1 × %s, so its coefficient is 1, even though the 1 is not written." % (V("p"), V("p"))))
    a, b = R(2, 9), R(10, 20)
    s = "%d + %dt" % (b, a)
    its.append(mcq("What are the terms of %s?" % B(E(s)), "%d and %s" % (b, E("%dt" % a)),
                   ["%d and %d" % (b, a), "%d and %s" % (a, V("t")), "%d, %d and %s" % (b, a, V("t"))],
                   "Terms are separated by + or −. %s is one term (%d × %s), so the terms are %d and %s."
                   % (E("%dt" % a), a, V("t"), b, E("%dt" % a))))
    its.append(mcq("Which description fits %s?" % B("2(8 + 7)"), "a product of two factors",
                   ["a sum of two terms", "a sum of three terms", "a quotient of two numbers"],
                   "The last step is to multiply 2 by (8 + 7), so 2(8 + 7) is a product. Its two factors are 2 and (8 + 7)."))
    its.append(mcq("In %s, how can you describe the factor %s?" % (B("2(8 + 7)"), B("(8 + 7)")), "a sum of two terms",
                   ["a product of two factors", "a difference of two terms", "a quotient of two numbers"],
                   "(8 + 7) is one factor of the product, and it is also a sum of the two terms 8 and 7. It equals 15."))
    KIND = [("(x + %d) ÷ %d" % (R(2, 9), R(2, 6)), "a quotient", "The last step is to divide the sum by %s, so the whole expression is a quotient."),
            ("%dy − %d" % (R(3, 9), R(2, 9)), "a difference", "%s is a product, but the last step is to subtract, so the whole expression is a difference."),
            ("%d(w − %d)" % (R(3, 9), R(1, 5)), "a product", "The parentheses are worked first, and the last step is to multiply, so the whole expression is a product."),
            ("%d + %dn" % (R(10, 20), R(2, 9)), "a sum", "%s is a product, but the last step is to add, so the whole expression is a sum.")]
    for s, good, e in KIND:
        toks = tokenize(s)
        if good == "a quotient":
            e = e % toks[-1].v
        elif "%s" in e:
            part = s.split(" ")[0] if good == "a difference" else s.split(" ")[-1]
            e = e % E(part)
        its.append(mcq("Look at the last step. What kind of expression is %s?" % B(E(s)), good,
                       [x for x in ["a sum", "a difference", "a product", "a quotient"] if x != good], e))
    a, b, c = R(5, 9), R(2, 4), R(6, 12)
    s = "%dx + %dy + %d" % (a, b, c)
    its.append(mcq("In %s, what is the coefficient of %s?" % (B(E(s)), V("y")), str(b), [str(a), str(c), "1"],
                   "The coefficient of %s is the number multiplied by %s: %s. %d goes with %s, and %d is the constant."
                   % (V("y"), V("y"), E("%dy" % b), a, V("x"), c)))
    its.append(mcq_expr("Which expression has a coefficient of 4 and a constant of 9?", "4x + 9", ["9x + 4", "4x + 9y", "x + 4 + 9"],
                        "In %s, 4 is multiplied by %s (the coefficient) and 9 stands alone (the constant). In %s, 9 is the coefficient."
                        % (E("4x + 9"), V("x"), E("9x + 4")), ["x", "y"]))
    its.append(mcq("Which expression has 3 terms?", E("x + 2y + 7"), [E("2(x + 7)"), E("8xy"), E("5x + 1")],
                   "%s has the terms %s, %s and 7. %s is one product (2 terms inside the parentheses), %s is 1 term, and %s has 2 terms."
                   % (E("x + 2y + 7"), V("x"), E("2y"), E("2(x + 7)"), E("8xy"), E("5x + 1"))))
    a, b = R(3, 6), R(7, 12)
    its.append(mcq("Which words match %s?" % B(E("%dn + %d" % (a, b))), "%d more than %d times %s" % (b, a, V("n")),
                   ["%d times the sum of %s and %d" % (a, V("n"), b), "%d less than %d times %s" % (b, a, V("n")),
                    "%d more than %d times %s" % (a, b, V("n"))],
                   "%s is %d times %s. Adding %d makes it %d more. “%d times the sum” would need parentheses: %s."
                   % (E("%dn" % a), a, V("n"), b, b, a, E("%d(n + %d)" % (a, b)))))
    b = R(5, 12)
    its.append(mcq("Which words match %s?" % B(E("y − %d" % b)), "%d less than %s" % (b, V("y")),
                   ["%s less than %d" % (V("y"), b), "%d more than %s" % (b, V("y")), "the product of %d and %s" % (b, V("y"))],
                   "%s starts with %s and takes %d away, so it is %d less than %s. “%s less than %d” would be %s."
                   % (E("y − %d" % b), V("y"), b, b, V("y"), V("y"), b, E("%d − y" % b))))
    a, b = R(4, 8), R(2, 3)
    its.append(mcq("Which words match %s?" % B(E("%d(x − %d)" % (a, b))), "%d times the difference of %s and %d" % (a, V("x"), b),
                   ["%d less than %d times %s" % (b, a, V("x")), "%d times the sum of %s and %d" % (a, V("x"), b),
                    "the difference of %d and %d times %s" % (b, a, V("x"))],
                   "The parentheses hold the difference %s, and it is multiplied by %d. “%d less than %d times %s” would be %s, with no parentheses."
                   % (E("x − %d" % b), a, b, a, V("x"), E("%dx − %d" % (a, b)))))
    b = R(3, 9)
    its.append(mcq("Which words match %s?" % B(E("k ÷ %d" % b)), "the quotient of %s and %d" % (V("k"), b),
                   ["the quotient of %d and %s" % (b, V("k")), "the product of %s and %d" % (V("k"), b), "%d less than %s" % (b, V("k"))],
                   "%s divides %s by %d, so it is the quotient of %s and %d. The order matters: %s is different."
                   % (E("k ÷ %d" % b), V("k"), b, V("k"), b, E("%d ÷ k" % b))))
    a, b = R(3, 9), R(10, 15)
    s = "%dx^2 + %d" % (a, b)
    its.append(mcq("What is the coefficient in %s?" % B(E(s)), str(a), ["2", str(b), str(2 * a)],
                   "%s means %d × %s × %s. The coefficient is %d. The small 2 is the exponent, and %d is the constant."
                   % (E("%dx^2" % a), a, V("x"), V("x"), a, b)))
    n, he, his = P.next()
    a, b = R(2, 9), R(10, 15)
    its.append(mcq("%s says the constant in %s is %d. Is %s right?" % (n, B(E("%d + %dn" % (b, a))), a, he),
                   "No, the constant is %d" % b,
                   ["Yes, %d is the constant" % a, "No, the constant is %s" % E("%dn" % a), "No, there is no constant"],
                   "The constant is the term with no variable, which is %d. %d is the coefficient of %s. The order of the terms does not matter."
                   % (b, a, V("n"))))
    assert len(its) == 20, len(its)
    return {"title": "Parts of an expression: terms, coefficients and constants", "items": its}


# ------------------------------------------------------------ set 3: evaluate with whole numbers
# (expression, letters with value ranges, number ranges, mistakes: list of (function(env) -> value, reason))
def T(expr, nums, lets, mist):
    return (expr, nums, lets, mist)


EVAL = [
    T("{a}n", {"a": (3, 9)}, {"n": (4, 9)},
      [(lambda e: cat(e["a"], e["n"]), "reads {an} as the number {cat}"),
       (lambda e: e["a"] + e["n"], "adds instead of multiplying"),
       (lambda e: cat(e["n"], e["a"]), "writes the digits side by side")]),
    T("{a}n + {b}", {"a": (2, 9), "b": (2, 9)}, {"n": (3, 9)},
      [(lambda e: cat(e["a"], e["n"]) + e["b"], "reads {an} as the number {cat}"),
       (lambda e: e["a"] * (e["n"] + e["b"]), "adds before multiplying"),
       (lambda e: e["a"] + e["n"] + e["b"], "adds {a} instead of multiplying")]),
    T("{a}n − {b}", {"a": (3, 9), "b": (2, 9)}, {"n": (4, 9)},
      [(lambda e: cat(e["a"], e["n"]) - e["b"], "reads {an} as the number {cat}"),
       (lambda e: e["a"] * (e["n"] - e["b"]), "subtracts before multiplying"),
       (lambda e: e["a"] * e["n"] + e["b"], "adds {b} instead of subtracting")]),
    T("{b} + {a}n", {"a": (2, 6), "b": (3, 12)}, {"n": (3, 9)},
      [(lambda e: (e["b"] + e["a"]) * e["n"], "adds before multiplying (left to right)"),
       (lambda e: e["b"] + cat(e["a"], e["n"]), "reads {an} as the number {cat}"),
       (lambda e: e["b"] + e["a"] + e["n"], "adds instead of multiplying")]),
    T("{a}(n + {b})", {"a": (2, 9), "b": (2, 9)}, {"n": (3, 9)},
      [(lambda e: e["a"] * e["n"] + e["b"], "multiplies only {n} by {a}"),
       (lambda e: e["a"] + e["n"] + e["b"], "adds instead of multiplying"),
       (lambda e: cat(e["a"], e["n"]) + e["b"], "reads {an} as the number {cat}")]),
    T("n ÷ {a} + {b}", {"a": (2, 6), "b": (2, 9)}, {"n": (12, 60)},
      [(lambda e: e["n"] / (e["a"] + e["b"]), "adds before dividing"),
       (lambda e: e["n"] / e["a"], "stops before adding {b}"),
       (lambda e: (e["n"] + e["b"]) / e["a"], "adds before dividing")]),
    T("(n + {b}) ÷ {a}", {"a": (2, 6), "b": (2, 9)}, {"n": (10, 40)},
      [(lambda e: e["n"] + e["b"] / e["a"], "skips the parentheses"),
       (lambda e: e["n"] / e["a"] + e["b"], "divides only {n}"),
       (lambda e: e["n"] + e["b"], "forgets to divide")]),
    T("n^2 + {b}", {"b": (2, 9)}, {"n": (3, 9)},
      [(lambda e: 2 * e["n"] + e["b"], "reads {n}<sup>2</sup> as 2 × {n}"),
       (lambda e: e["n"] + 2 + e["b"], "adds the exponent"),
       (lambda e: e["n"] ** 2, "forgets to add {b}")]),
    T("{a}n^2", {"a": (2, 5)}, {"n": (3, 6)},
      [(lambda e: (e["a"] * e["n"]) ** 2, "squares {a} too, but only {n} is squared"),
       (lambda e: e["a"] * 2 * e["n"], "reads {n}<sup>2</sup> as 2 × {n}"),
       (lambda e: e["a"] * e["n"], "forgets the exponent")]),
    T("n^3", {}, {"n": (3, 5)},
      [(lambda e: 3 * e["n"], "reads {n}<sup>3</sup> as 3 × {n}"),
       (lambda e: e["n"] ** 2, "uses {n} as a factor only 2 times"),
       (lambda e: e["n"] + 3, "adds the exponent")]),
    T("{c} − {a}n", {"a": (2, 6), "c": (40, 60)}, {"n": (3, 7)},
      [(lambda e: (e["c"] - e["a"]) * e["n"], "subtracts before multiplying"),
       (lambda e: e["c"] - e["a"] - e["n"], "subtracts {n} instead of multiplying"),
       (lambda e: e["a"] * e["n"], "stops before subtracting from {c}")]),
    T("n(n + {b})", {"b": (2, 6)}, {"n": (3, 8)},
      [(lambda e: e["n"] * e["n"] + e["b"], "skips the parentheses"),
       (lambda e: e["n"] + e["n"] + e["b"], "adds instead of multiplying"),
       (lambda e: e["n"] + e["b"], "forgets to multiply by {n}")]),
    T("{c} ÷ n + {b}", {"b": (2, 9), "c": (24, 60)}, {"n": (3, 8)},
      [(lambda e: e["c"] / (e["n"] + e["b"]), "adds before dividing"),
       (lambda e: e["c"] / e["n"], "stops before adding {b}"),
       (lambda e: e["c"] - e["n"] + e["b"], "subtracts instead of dividing")]),
    T("{a}x + {b}y", {"a": (2, 6), "b": (2, 6)}, {"x": (3, 9), "y": (3, 9)},
      [(lambda e: e["a"] * e["y"] + e["b"] * e["x"], "switches the values of {X} and {Y}"),
       (lambda e: e["a"] + e["x"] + e["b"] + e["y"], "adds instead of multiplying"),
       (lambda e: e["a"] * (e["x"] + e["b"]) * e["y"], "works from left to right")]),
    T("xy − {b}", {"b": (2, 9)}, {"x": (3, 9), "y": (3, 9)},
      [(lambda e: e["x"] + e["y"] - e["b"], "adds {X} and {Y} instead of multiplying"),
       (lambda e: cat(e["x"], e["y"]) - e["b"], "reads {xy} as the number {cat}"),
       (lambda e: e["x"] * (e["y"] - e["b"]), "subtracts before multiplying")]),
    T("{a}(x − y)", {"a": (2, 9)}, {"x": (9, 15), "y": (2, 8)},
      [(lambda e: e["a"] * e["x"] - e["y"], "multiplies only {x} by {a}"),
       (lambda e: e["a"] * (e["x"] + e["y"]), "adds instead of subtracting"),
       (lambda e: e["x"] - e["y"], "forgets to multiply by {a}")]),
    T("x^2 + y^2", {}, {"x": (2, 6), "y": (2, 6)},
      [(lambda e: (e["x"] + e["y"]) ** 2, "adds before squaring"),
       (lambda e: 2 * e["x"] + 2 * e["y"], "reads each square as 2 times the number"),
       (lambda e: e["x"] ** 2 + e["y"], "squares only {x}")]),
    T("{a}x + y ÷ {b}", {"a": (2, 6), "b": (2, 5)}, {"x": (3, 9), "y": (10, 40)},
      [(lambda e: (e["a"] * e["x"] + e["y"]) / e["b"], "adds before dividing"),
       (lambda e: e["a"] * e["x"] + e["y"], "forgets to divide"),
       (lambda e: e["a"] + e["x"] + e["y"] / e["b"], "adds {a} instead of multiplying")]),
]

ASK = ["What is the value of %s when %s?", "Evaluate %s when %s.", "Find the value of %s when %s."]


def env_text(env):
    return " and ".join("%s = %s" % (V(k), show(v)) for k, v in env.items())


def set_eval(rnd, P):
    its = []
    for k, (expr, nums, lets, mist) in enumerate(EVAL):
        for _ in range(5000):
            m = {x: rnd.randint(*r) for x, r in nums.items()}
            env = {x: rnd.randint(*r) for x, r in lets.items()}
            if len(set(list(m.values()) + list(env.values()))) < len(m) + len(env):
                continue
            s = expr.format(**m)
            v = val(s, env)
            if v.denominator != 1 or v <= 0:
                continue
            e = {x: Fr(y) for x, y in dict(m, **env).items()}
            ws = [g(e) for g, _ in mist]
            if Fr(ws[0]).denominator != 1 or ws[0] <= 0 or Fr(ws[0]) == v:
                continue
            ok = {Fr(w) for w in ws if Fr(w).denominator == 1 and w > 0 and w != v}
            if len(ok) < 3:
                continue
            break
        else:
            raise RuntimeError(expr)
        v, ch = evaluate(s, env)
        cc = cat(e["x"], e["y"]) if "xy" in expr else (cat(e["a"], e["n"]) if "a" in e and "n" in e else 0)
        hm = {x: show(y) for x, y in e.items()}
        hm.update({"cat": cc, "an": show(e.get("a", 0)) + V("n"), "xy": E("xy"), "X": V("x"), "Y": V("y")})
        why = mist[0][1].format(**hm)
        repl = " and ".join("%s with %s" % (V(x), show(y)) for x, y in env.items())
        expl = "Replace %s: %s. Not %s: that %s." % (repl, ch, show(ws[0]), why)
        q = ASK[k % len(ASK)] % (B(E(s)), env_text(env))
        its.append(mcq_val(q, v, [w for w in ws if Fr(w).denominator == 1], expl))
    # the mistake of reading 3n as 35
    n, he, his = P.next()
    s, env = "3n + 4", {"n": 5}
    v, ch = evaluate(s, env)
    assert v == 19
    its.append(mcq("%s says %s = 39 when %s = 5. What mistake did %s make?" % (n, B(E(s)), V("n"), he),
                   "%s read 3%s as 35" % (cap(he), V("n")),
                   ["%s added before multiplying" % cap(he), "%s forgot to add 4" % cap(he), "No mistake, 39 is right"],
                   "3%s means 3 × %s, not the digits 3 and 5 side by side: %s. %s used 35 + 4 = 39." % (V("n"), V("n"), ch, n)))
    n, he, his = P.next()
    s, env = "2n^2", {"n": 3}
    v, ch = evaluate(s, env)
    assert v == 18
    its.append(mcq("%s says %s = 36 when %s = 3. What mistake did %s make?" % (n, B(E(s)), V("n"), he),
                   "%s squared 2 × 3, not just 3" % cap(he),
                   ["%s read 3<sup>2</sup> as 3 × 2" % cap(he), "%s added 2 and 3" % cap(he), "No mistake, 36 is right"],
                   "The exponent goes with %s only. Square first, then multiply: %s. %s found (2 × 3)<sup>2</sup> = 6<sup>2</sup> = 36."
                   % (V("n"), ch, n)))
    assert len(its) == 20, len(its)
    return {"title": "Evaluate expressions with whole numbers", "items": its}


# ------------------------------------------------------------ set 4: formulas, fractions, decimals, exponents
def unit_fmt(u, mode="f"):
    return lambda v: "%s %s" % (show(v, mode), u)


def set_formulas(rnd, P):
    its = []
    SQ, CU = "<sup>2</sup>", "<sup>3</sup>"

    def item(q, s, env, wrong, note, mode="f", fmt=None, intro=None):
        v, ch = evaluate(s, env, mode)
        fm = fmt or (lambda x: show(x, mode))
        ws = [Fr(w) for w in wrong]
        e = "%s%s. %s" % (intro or ("Replace " + join("%s with %s" % (V(k), (dec(Fr(x)) if mode == "d" else show(Fr(x))))
                                                               for k, x in env.items()) + ": "), ch, note)
        its.append(mcq_val(q, v, ws, e, fm))
        return v

    # 1 square
    s = 7
    v = item(fig(square_svg((s, "cm"))) + "The area of a square is %s. What is the area of this square?" % B("A = " + E("s^2")),
             "s^2", {"s": s}, [2 * s, 4 * s, s + 2], "Not 14 cm%s: %s means %s × %s, not 2 × %s." % (SQ, E("s^2"), V("s"), V("s"), V("s")),
             fmt=unit_fmt("cm" + SQ))
    assert v == 49
    # 2 cube
    s = 4
    v = item(fig(cube_svg((s, "in."))) + "The volume of a cube is %s. What is the volume of this cube?" % B("V = " + E("s^3")),
             "s^3", {"s": s}, [3 * s, s ** 2, 3 * s ** 2], "Not 12 in.%s: %s means %s × %s × %s, not 3 × %s." % (CU, E("s^3"), V("s"), V("s"), V("s"), V("s")),
             fmt=unit_fmt("in." + CU))
    assert v == 64
    # 3 rectangle perimeter
    l, w = 9, 5
    v = item(fig(rect_svg((l, "ft"), (w, "ft"))) + "Use %s to find the perimeter of this rectangle." % B("P = " + E("2l + 2w")),
             "2l + 2w", {"l": l, "w": w}, [l * w, l + w, 2 * l + w],
             "Not 45 ft: that is the area, %s × %s. Not 14 ft: that adds only one length and one width." % (V("l"), V("w")),
             fmt=unit_fmt("ft"))
    assert v == 28
    # 4 distance
    r, t = 48, 3
    v = item("A train goes at a speed of %d miles per hour for %d hours. Use %s to find the distance it travels." % (r, t, B("d = " + E("rt"))),
             "rt", {"r": r, "t": t}, [r + t, r // t, r - t],
             "%s means %s × %s, so multiply the speed by the time. Not 51 miles: that adds." % (E("rt"), V("r"), V("t")), fmt=unit_fmt("miles"))
    assert v == 144
    # 5 triangle
    b, h = 10, 7
    v = item(fig(triangle_svg((b, "cm"), (h, "cm"))) + "The area of a triangle is %s. What is the area of this triangle?" % B("A = " + E("[1/2]bh")),
             "[1/2]bh", {"b": b, "h": h}, [b * h, b + h, Fr(b, 2) + h],
             "Not 70 cm%s: that forgets to multiply by %s." % (SQ, fr(1, 2)), fmt=unit_fmt("cm" + SQ))
    assert v == 35
    # 6 temperature
    C = 20
    v = item("The formula %s changes degrees Celsius to degrees Fahrenheit. What is %s when %s?" % (B("F = " + E("[9/5]c + 32").replace("<i>c</i>", "<i>C</i>")), V("F"), V("C") + " = 20"),
             "[9/5]c + 32", {"c": C}, [Fr(9, 5) * C, C + 32, Fr(9, 5) * (C + 32)],
             "Multiply first, then add 32. Not 36: that forgets to add 32.", mode="d",
             intro="Replace %s with 20: " % V("C"), fmt=lambda x: "%s°F" % dec(x))
    assert v == 68
    # 7 rectangle decimals
    v = item(fig(rect_svg(("4.5", "m"), (2, "m"))) + "Use %s to find the area of this rectangle." % B("A = " + E("lw")),
             "lw", {"l": "4.5", "w": 2}, [Fr("6.5"), 13, 8],
             "Not 13 m%s: that is the perimeter. Not 8 m%s: the 0.5 must be multiplied too." % (SQ, SQ), mode="d", fmt=unit_fmt("m" + SQ, "d"))
    assert v == 9
    # 8 rectangle mixed numbers
    l, w = Fr(7, 2), Fr(5, 4)
    v = item(fig(rect_svg((l, "ft"), (w, "ft"))) + "Use %s to find the perimeter of this rectangle." % B("P = " + E("2l + 2w")),
             "2l + 2w", {"l": l, "w": w}, [l + w, l * w, 2 * l + w],
             "Not %s ft: that adds only one length and one width." % mixed(l + w), fmt=unit_fmt("ft"))
    assert v == Fr(19, 2)
    # 9 4x, x = 3/4
    v = item("Evaluate %s when %s = %s." % (B(E("4x")), V("x"), fr(3, 4)), "4x", {"x": Fr(3, 4)}, [4 + Fr(3, 4), Fr(3, 16), 12],
             "Not 4 %s: 4%s means 4 × %s, not 4 and %s side by side." % (fr(3, 4), V("x"), V("x"), fr(3, 4)))
    assert v == 3
    # 10 6t - 2, t = 2/3
    v = item("Find the value of %s when %s = %s." % (B(E("6t − 2")), V("t"), fr(2, 3)), "6t − 2", {"t": Fr(2, 3)}, [4, 10, 6 + Fr(2, 3) - 2],
             "Not 4: that forgets to subtract 2. Not 10: 6 × 2 = 12 forgets the denominator 3.")
    assert v == 2
    # 11 x^2, x = 1.5
    v = item("What is the value of %s when %s = 1.5?" % (B(E("x^2")), V("x")), "x^2", {"x": "1.5"}, [3, Fr("22.5"), Fr("3.5")],
             "Not 3: %s means 1.5 × 1.5, not 2 × 1.5." % E("x^2"), mode="d")
    assert v == Fr(9, 4)
    # 12 y^3, y = 1/2
    v = item("Evaluate %s when %s = %s." % (B(E("y^3")), V("y"), fr(1, 2)), "y^3", {"y": Fr(1, 2)}, [Fr(3, 2), Fr(1, 6), Fr(1, 4)],
             "%s means %s × %s × %s. Not %s: that multiplies by 3." % (E("y^3"), fr(1, 2), fr(1, 2), fr(1, 2), mixed(Fr(3, 2))))
    assert v == Fr(1, 8)
    # 13 2.5n + 1, n = 4
    v = item("Find the value of %s when %s = 4." % (B(E("2.5n + 1")), V("n")), "2.5n + 1", {"n": 4},
             [Fr("12.5"), Fr("7.5"), 10], "Not 12.5: that adds 4 + 1 before multiplying.", mode="d")
    assert v == 11
    # 14 square with fraction side
    s = Fr(2, 3)
    v = item(fig(square_svg((Fr(2, 3), "ft"))) + "Use %s to find the area of this square." % B("A = " + E("s^2")),
             "s^2", {"s": s}, [2 * s, Fr(2, 9), 4 * s],
             "Square both the numerator and the denominator. Not %s ft%s: that doubles the side." % (mixed(2 * s), SQ),
             fmt=unit_fmt("ft" + SQ))
    assert v == Fr(4, 9)
    # 15 box volume
    v = item("A box is 5 in. long, 3 in. wide and %s in. tall. Use %s to find its volume." % (fr(1, 2), B("V = " + E("lwh"))),
             "lwh", {"l": 5, "w": 3, "h": Fr(1, 2)}, [15, 5 + 3 + Fr(1, 2), 30],
             "Not 15 in.%s: that forgets the height. Not 30 in.%s: that divides by %s." % (CU, CU, fr(1, 2)), fmt=unit_fmt("in." + CU))
    assert v == Fr(15, 2)
    # 16 distance with a decimal time
    v = item("A car goes at a speed of 60 miles per hour for 2.5 hours. Use %s to find the distance." % B("d = " + E("rt")),
             "rt", {"r": 60, "t": "2.5"}, [Fr("62.5"), 120, 24],
             "Not 120 miles: that uses only 2 hours. Not 62.5 miles: that adds.", mode="d", fmt=unit_fmt("miles", "d"))
    assert v == 150
    # 17 2^n + 1
    v = item("Evaluate %s when %s = 5." % (B("2<sup><i>n</i></sup> + 1"), V("n")), "2^n + 1", {"n": 5}, [11, 26, 32],
             "2<sup>5</sup> means 2 × 2 × 2 × 2 × 2 = 32. Not 11: that is 2 × 5 + 1. Not 32: that forgets to add 1.",
             intro="Replace %s with 5: " % V("n"))
    assert v == 33
    # 18 x^3 - 1
    v = item("What is the value of %s when %s = 4?" % (B(E("x^3 − 1")), V("x")), "x^3 − 1", {"x": 4}, [11, 15, 64],
             "Not 11: %s is not 3 × 4. Not 64: that forgets to subtract 1." % E("x^3"))
    assert v == 63
    # 19 s^2, s = 0.3
    v = item(fig(square_svg(("0.3", "m"))) + "Use %s to find the area of this square." % B("A = " + E("s^2")), "s^2", {"s": "0.3"},
             [Fr("0.9"), Fr("0.6"), 9],
             "0.3 has 1 decimal place, so 0.3 × 0.3 has 2 decimal places. Not 0.9 m%s: the decimal point is in the wrong place." % SQ,
             mode="d", fmt=unit_fmt("m" + SQ, "d"))
    assert v == Fr(9, 100)
    # 20 1/2(n + 6)
    v = item("Evaluate %s when %s = 10." % (B(E("[1/2](n + 6)")), V("n")), "[1/2](n + 6)", {"n": 10}, [11, 16, 5],
             "Not 11: that halves only 10. Not 16: that forgets to multiply by %s." % fr(1, 2))
    assert v == 8
    assert len(its) == 20, len(its)
    return {"title": "Formulas, fractions, decimals and exponents", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_problems(rnd, P):
    its = []
    # choose the expression
    n1, he1, his1 = P.next()
    CH = [
        ("Movie tickets cost $12 each. There is a $5 online fee for the whole order. Which expression shows the cost of %s tickets?" % V("t"),
         "12t + 5", ["12(t + 5)", "5t + 12", "12 + 5 + t"], ["t"],
         "Each ticket is $12, so %s tickets cost 12%s. The $5 fee is paid once: 12%s + 5. %s would charge the fee for every ticket."
         % (V("t"), V("t"), V("t"), E("12(t + 5)"))),
        ("%s reads %s pages each day for 6 days. Then %s reads 20 more pages. Which expression shows how many pages %s reads in all?" % (n1, V("p"), he1, he1),
         "6p + 20", ["6(p + 20)", "20p + 6", "p + 6 + 20"], ["p"],
         "6 days of %s pages is 6%s. Then add the 20 pages once: 6%s + 20." % (V("p"), V("p"), V("p"))),
        ("4 friends share the cost of a pizza equally. The pizza costs %s dollars. Which expression shows how much each friend pays?" % V("c"),
         "c ÷ 4", ["4c", "4 ÷ c", "c − 4"], ["c"],
         "Sharing equally means dividing the cost by 4: %s. %s divides 4 by the cost, which is backward." % (E("c ÷ 4"), E("4 ÷ c"))),
    ]
    n2, he2, his2 = P.next()
    CH.append(("%s is 3 years older than %s brother. %s brother is %s years old. Which expression shows %s age?" % (n2, his2, cap(his2), V("b"), n2 + "’s"),
               "b + 3", ["3b", "b − 3", "3 − b"], ["b"],
               "Older means more years, so add 3 to the brother’s age: %s. %s would mean 3 times as old." % (E("b + 3"), E("3b"))))
    n3, he3, his3 = P.next()
    n4, he4, his4 = P.next()
    CH.append(("%s has %s trading cards. %s has 5 fewer than twice as many cards as %s. Which expression shows how many cards %s has?" % (n3, V("c"), n4, n3, n4),
               "2c − 5", ["5 − 2c", "2(c − 5)", "2c + 5"], ["c"],
               "Twice as many as %s is 2%s. 5 fewer than that is 2%s − 5. %s has the order backward." % (n3, V("c"), V("c"), E("5 − 2c"))))
    CH += [
        ("At noon it is 68°F. The temperature drops 2°F each hour. Which expression shows the temperature %s hours after noon?" % V("h"),
         "68 − 2h", ["2h − 68", "(68 − 2)h", "68 + 2h"], ["h"],
         "In %s hours it drops 2%s degrees. Take that away from 68: 68 − 2%s. %s would make it warmer." % (V("h"), V("h"), V("h"), E("68 + 2h"))),
        ("A square garden has sides that are %s feet long. Which expression shows the length of fence needed to go around it?" % V("s"),
         "4s", ["s^2", "s + 4", "2s"], ["s"],
         "Going around means the perimeter. A square has 4 equal sides: %s. %s is the area, not the perimeter." % (E("4s"), E("s^2"))),
        ("A phone plan costs $25 a month plus $3 for each gigabyte (GB) of data used. Which expression shows the cost for a month with %s GB?" % V("g"),
         "25 + 3g", ["3(25 + g)", "25g + 3", "28g"], ["g"],
         "$3 for each of %s GB is 3%s. Add the $25 once: 25 + 3%s. %s puts the numbers on the wrong parts." % (V("g"), V("g"), V("g"), E("25g + 3"))),
        ("4 friends order a pizza that costs %s dollars and pay a $6 delivery fee. They split the total equally. Which expression shows what each friend pays?" % V("p"),
         "(p + 6) ÷ 4", ["p + 6 ÷ 4", "p ÷ 4 + 6", "4(p + 6)"], ["p"],
         "The total is %s, and the whole total is split, so it goes in parentheses: %s. %s would split only the fee." % (E("p + 6"), E("(p + 6) ÷ 4"), E("p + 6 ÷ 4"))),
    ]
    n5, he5, his5 = P.next()
    CH.append(("%s read %s pages on Monday and twice as many pages on Tuesday. Which expression shows how many pages %s read on both days?" % (n5, V("n"), he5),
               "n + 2n", ["2n", "n + 2", "n + n + 2"], ["n"],
               "Monday is %s pages and Tuesday is 2%s pages. Add them: %s, which is 3%s. %s counts only Tuesday." % (V("n"), V("n"), E("n + 2n"), V("n"), E("2n"))))
    for q, good, bad, letters, e in CH:
        its.append(mcq_expr(q, good, bad, e, letters))

    # write an expression and find the value
    def vp(q, s, env, wrong, note, fmt):
        v, ch = evaluate(s, env, "d")
        repl = join("%s with %s" % (V(k), dec(Fr(x))) for k, x in env.items())
        e = "Expression: %s. Replace %s: %s. %s" % (E(s), repl, ch, note)
        its.append(mcq_val(q, v, wrong, e, fmt))
        return v

    cents = lambda v: money(v, cents=True)
    v = vp("Movie tickets cost $12 each, plus a $5 fee for the whole order. Use %s to find the cost of 4 tickets." % B(E("12t + 5")),
           "12t + 5", {"t": 4}, [12 * 9, 5 * 4 + 12, 12 + 5 + 4], "Not $108: the fee is paid once, not for every ticket.", money)
    assert v == 53
    v = vp("A taxi ride costs $3 plus $2.50 for each mile. Write an expression for %s miles and find the cost of an 8-mile ride." % V("m"),
           "3 + 2.5m", {"m": 8}, [Fr("5.5") * 8, 3 * 8 + Fr("2.5"), Fr("2.5") * 8],
           "Not $44.00: that adds 3 + 2.50 before multiplying.", cents)
    assert v == 23
    n, he, his = P.next()
    v = vp("%s has $40 and saves $8 each week. Write an expression for %s weeks and find how much %s has after 6 weeks." % (n, V("w"), he),
           "40 + 8w", {"w": 6}, [48 * 6, 40 + 8 + 6, 8 * 6], "Not $288: that adds 40 + 8 before multiplying.", money)
    assert v == 88
    v = vp("At a bake sale, cookies cost $0.75 each. Write an expression for %s cookies and find how much 24 cookies cost." % V("c"),
           "0.75c", {"c": 24}, [75 * 24, 24 + Fr("0.75"), 32],
           "Not $1,800.00: 0.75 is less than 1, so the cost must be less than 24 dollars.", cents)
    assert v == 18
    v = vp("A car travels at 60 miles per hour. Write an expression for %s hours and find how far it goes in 3.5 hours." % V("h"),
           "60h", {"h": "3.5"}, [Fr("63.5"), 180, 240], "Not 180 miles: that leaves out the half hour.",
           lambda x: "%s miles" % dec(x))
    assert v == 210
    v = vp("4 friends order a pizza for %s dollars and pay a $6 delivery fee. They split the total equally. Use %s to find what each pays when %s = 22."
           % (V("p"), B(E("(p + 6) ÷ 4")), V("p")),
           "(p + 6) ÷ 4", {"p": 22}, [22 + Fr(6, 4), Fr(22, 4) + 6, 28],
           "Not $23.50: that splits only the fee. Not $28.00: that is the total, not each share.", cents)
    assert v == 7
    v = vp("At noon it is 68°F. The temperature drops 2°F each hour. Use %s to find the temperature 5 hours after noon." % B(E("68 − 2h")),
           "68 − 2h", {"h": 5}, [66 * 5, 68 + 10, 68 - 2 - 5], "Not 78°F: the temperature drops, so subtract.",
           lambda x: "%s°F" % f(x))
    assert v == 58
    v = vp("A gym charges a $15 sign-up fee and $20 each month. Write an expression for %s months and find the cost for 9 months." % V("m"),
           "15 + 20m", {"m": 9}, [35 * 9, 15 + 20 + 9, 20 * 9], "Not $180: that forgets the sign-up fee.", money)
    assert v == 195
    n, he, his = P.next()
    v = vp("%s reads %s pages each weekday (5 days) and 40 pages on Saturday. Write an expression and find the pages %s reads in the week when %s = 25."
           % (n, V("p"), he, V("p")),
           "5p + 40", {"p": 25}, [5 * 65, 25 + 5 + 40, 125], "Not 125 pages: that forgets Saturday.",
           lambda x: "%s pages" % f(x))
    assert v == 165
    v = vp("A field trip costs $150 for the bus plus $8 for each student. Write an expression for %s students and find the cost for 32 students." % V("n"),
           "150 + 8n", {"n": 32}, [158 * 32, 150 + 8 + 32, 8 * 32], "Not $5,056: that adds 150 + 8 before multiplying.", money)
    assert v == 406
    assert len(its) == 20, len(its)
    return {"title": "Word problems: write and evaluate expressions", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    v1, ch1 = evaluate("3n + 4", {"n": 5})
    v2, ch2 = evaluate("s^2", {"s": 6})
    v3, ch3 = evaluate("2(x + 3)", {"x": 4})
    assert (v1, v2, v3) == (19, 36, 14)
    return (
        "<h2>Letters stand for numbers</h2>"
        "<p>A <b>variable</b> is a letter that stands for a number, like %s. An <b>expression</b> uses numbers, variables and "
        "operation signs, with no equal sign: %s.</p>"
        "<p>A number written next to a letter means multiply: %s means 3 × %s. %s means %s × %s, and %s means %s × %s.</p>"
        % (V("n"), E("3n + 4"), E("3n"), V("n"), E("xy"), V("x"), V("y"), E("s^2"), V("s"), V("s")) +
        "<h2>Write an expression from words</h2>" +
        table(["Words", "Expression"], [
            ["5 more than %s, %s increased by 5" % (V("n"), V("n")), E("n + 5")],
            ["3 less than %s, %s decreased by 3" % (V("y"), V("y")), E("y − 3") + " (not " + E("3 − y") + ")"],
            ["the product of 4 and %s" % V("a"), E("4a")],
            ["%s divided by 6, the quotient of %s and 6" % (V("k"), V("k")), E("k ÷ 6")],
            ["subtract %s from 20" % V("x"), E("20 − x")],
            ["2 times the sum of %s and 7" % V("x"), E("2(x + 7)")],
        ]) +
        "<h2>Name the parts of an expression</h2>"
        "<p>A <b>term</b> is a part joined to the others by + or −. The <b>coefficient</b> is the number multiplied by a variable. "
        "The <b>constant</b> is a term with no variable.</p>"
        "<figure class='sn-fig'>" + parts_svg() +
        "<figcaption>%s has 2 terms. 3 is the coefficient of %s, and 4 is the constant.</figcaption></figure>" % (E("3n + 4"), V("n")) +
        "<p>Look at the last step to name the whole expression. 2(8 + 7) is a <b>product</b> of two factors, 2 and (8 + 7). "
        "The factor (8 + 7) is also a <b>sum</b> of two terms.</p>"
        "<h2>Evaluate an expression</h2>"
        "<p>Replace each variable with its value. Then use the order of operations: parentheses, exponents, × and ÷, then + and −.</p>" +
        ex("Example", "Evaluate %s when %s = 5." % (E("3n + 4"), V("n")), "Replace %s with 5: %s." % (V("n"), ch1), "%s (not 39)" % show(v1)) +
        ex("Example", "Evaluate %s when %s = 4." % (E("2(x + 3)"), V("x")), "Parentheses first: %s." % ch3, show(v3)) +
        "<h2>Use a formula</h2>"
        "<p>A formula is an expression for a real quantity. The area of a square is %s.</p>" % ("A = " + E("s^2")) +
        "<figure class='sn-fig'>" + square_svg((6, "cm")) +
        "<figcaption>%s = %s, so the area is 36 cm<sup>2</sup>.</figcaption></figure>" % (E("s^2"), ch2) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["“3 less than %s” written as %s" % (V("y"), E("3 − y")), "Start with %s and take 3 away: %s" % (V("y"), E("y − 3"))],
            ["%s = 35 when %s = 5" % (E("3n"), V("n")), "%s means 3 × %s: 3 × 5 = 15" % (E("3n"), V("n"))],
            ["Calling 4 the coefficient in %s" % E("3n + 4"), "The coefficient goes with the variable (3). 4 is the constant"],
            ["%s = 12 when %s = 6" % (E("s^2"), V("s")), "%s means 6 × 6 = 36, not 2 × 6" % E("s^2")],
            ["%s = 39 when %s = 5 (adding first)" % (E("3(n + 8)"), V("n")) if False else "%s = 23 when %s = 5" % (E("3(n + 8)"), V("n")),
             "Multiply the whole sum: 3 × (5 + 8) = 3 × 13 = 39"],
        ])
    )


FAQ = [
    {"q": "What is a variable in 6th grade math?",
     "a": "A variable is a letter, such as n or x, that stands for a number. In 3n + 4, the value of n can change, and the expression changes with it."},
    {"q": "How do you evaluate an expression?",
     "a": "Replace each variable with its value, then follow the order of operations. For 3n + 4 when n = 5: 3 × 5 + 4 = 15 + 4 = 19."},
    {"q": "What is the difference between a coefficient and a constant?",
     "a": "The coefficient is the number multiplied by a variable, and the constant is a number with no variable. In 3n + 4, 3 is the coefficient and 4 is the constant."},
    {"q": "How do you write “3 less than a number” as an expression?",
     "a": "Start with the number and take 3 away: n − 3. Writing 3 − n is a common mistake, because “less than” reverses the order of the words."},
]


def gen():
    rnd = random.Random(610)
    P = People(rnd)
    sets = [set_words(rnd, P), set_parts(rnd, P), set_eval(rnd, P), set_formulas(rnd, P), set_problems(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert "\\" not in it["q"] + it["e"] + "".join(it["c"])
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "us", "subject": "math", "grade": "grade-6", "slug": "writing-evaluating-expressions", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Writing and Evaluating Expressions with Variables",
        "seo_title": "Grade 6 Writing and Evaluating Expressions Worksheets: Variables, Terms, Coefficients and Formulas (6.EE.A.2)",
        "short_title": "Writing and evaluating expressions",
        "domain": "Expressions and Equations",
        "standard_code": "6.EE.A.2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/6/EE/A/2/",
        "standard_text": "Write, read, and evaluate expressions in which letters stand for numbers.",
        "meta_desc": "Free Grade 6 expressions worksheets: write expressions with variables from words, name terms, coefficients and constants, evaluate expressions and formulas like A = s² and d = rt, and solve word problems. 100 practice questions with an answer key.",
        "key_big": "A letter stands for a number. 3n means 3 × n, so when n = 5, 3n + 4 = 15 + 4 = 19.",
        "key_sub": "“3 less than y” is y − 3, not 3 − y. In 3n + 4, 3 is the coefficient and 4 is the constant. To evaluate, replace the letter with its value and use the order of operations.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
