# -*- coding: utf-8 -*-
"""
Singapore Primary 5 Maths: Order of operations (MOE 2021 Primary Mathematics Syllabus, Whole Numbers)
  python3 tools/gen_sg_maths_p5_order_of_operations.py
Order of operations with whole numbers, without a calculator: × and ÷ before + and −,
left to right for operations of the same rank (24 ÷ 4 × 2 = 12, not 3), brackets first,
mixed expressions with brackets, and word problems written as one expression (with bar models).

Expressions are written in a small source syntax and evaluated exactly with fractions.Fraction,
cross-checked with Python eval. Wrong answers come from real mistakes, computed by evaluating the
expression the wrong way: strictly left to right, + and − before × and ÷, × before ÷, + before −,
right to left, ignoring brackets, plus stopping one step early.
Engine adapted from gen_cabc_math_g6_order_of_operations.py.
Singapore English. 4-digit numbers have no separator; 5+ digits use a no-break space.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re, string
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-5")
UPDATED = "2026-11-03"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
BLUE = "#2f6fb0"
FILL = "#cfe6d6"
FONT = "Arial, Helvetica, sans-serif"
NB = "\u00a0"
MINUS = "−"

OPS = ("×", "÷", "+", "−")
STD = [("^",), ("×", "÷"), ("+", "−")]
LEVELS = {
    "ltr": [("^",), ("×", "÷", "+", "−")],          # strictly left to right
    "rev": [("^",), ("+", "−"), ("×", "÷")],        # + and − before × and ÷
    "mulfirst": [("^",), ("×",), ("÷",), ("+", "−")],  # × before ÷
    "addfirst": [("^",), ("×", "÷"), ("+",), ("−",)],  # + before −
}
# switched per set: whole-number sets do not allow negatives or decimals
ALLOW = {"neg": False, "dec": False}


# ------------------------------------------------------------ numbers
def group(n):
    s = str(n)
    if n < 10000:
        return s
    return "{:,}".format(n).replace(",", NB)


def nice(x):
    """A terminating decimal with at most 3 decimal places."""
    return x is not None and 1000 % Fraction(x).denominator == 0


def fmt(x):
    x = Fraction(x)
    assert nice(x), x
    neg, x = x < 0, abs(x)
    w = int(x)
    s = group(w)
    if x.denominator != 1:
        s += "." + str(int((x - w) * 1000)).zfill(3).rstrip("0")
    return (MINUS if neg else "") + s


def src(x):
    """Plain source text for a positive number (no grouping)."""
    return fmt(x).replace(NB, "")


def money(v):
    v = Fraction(v)
    if v <= 0 or (v * 100).denominator != 1:
        return None
    c = int(v * 100)
    if c % 100 == 0:
        return "$" + group(c // 100)
    return "$%s.%02d" % (group(c // 100), c % 100)


# ------------------------------------------------------------ expression engine
TOK = re.compile(r"~?\d+(?:\.\d+)?|[×÷+−()^]")


class Calc(Fraction):
    """A number made by an earlier step."""


def tokens(s):
    raw = TOK.findall(s)
    assert "".join(raw) == s.replace(" ", ""), s
    out = []
    for t in raw:
        if t[0].isdigit() or t[0] == "~":
            out.append(Fraction(t.replace("~", "-")))
        else:
            out.append(t)
    return out


def render(ts):
    out = ""
    i = 0
    while i < len(ts):
        t = ts[i]
        if t == "^":
            assert ts[i + 1] == 2
            out += "²"
            i += 2
            continue
        if isinstance(t, Fraction):
            s = fmt(t)
            prev = ts[i - 1] if i else None
            if t < 0 and len(ts) > 1 and prev != "(":
                s = "(" + s + ")"
        else:
            s = t
        if out and not out.endswith("(") and s != ")":
            out += " "
        out += s
        i += 1
    return out


def H(s):
    return render(tokens(s))


def apply(a, op, b, mode="std"):
    if op == "^":
        assert b == 2
        if mode == "sq2":
            r = a * 2
        else:
            return apply(a, "×", a, mode)
    elif op == "×":
        r = a * b
    elif op == "÷":
        if not b:
            return None
        r = a / b
        if not nice(r) or (not ALLOW["dec"] and r.denominator != 1):
            return None
    elif op == "+":
        r = a + b
    else:
        r = a - b
        if mode == "subneg" and b < 0:
            r = a + b
    if op in ("×", "÷"):
        if mode == "negneg" and a < 0 and b < 0:
            r = -r
        if mode == "drop" and (a < 0) != (b < 0):
            r = -r
    if not ALLOW["neg"] and r < 0:
        return None
    return r


def flat_eval(seq, prec, mode, rtl=False):
    seq = list(seq)
    for level in prec:
        if rtl:
            i = len(seq) - 2
            while i >= 1:
                if seq[i] in level:
                    v = apply(seq[i - 1], seq[i], seq[i + 1], mode)
                    if v is None:
                        return None
                    seq[i - 1:i + 2] = [v]
                i -= 2
        else:
            i = 1
            while i < len(seq):
                if seq[i] in level:
                    v = apply(seq[i - 1], seq[i], seq[i + 1], mode)
                    if v is None:
                        return None
                    seq[i - 1:i + 2] = [v]
                else:
                    i += 2
    assert len(seq) == 1, seq
    return seq[0]


def ev_tokens(ts, prec=STD, mode="std", rtl=False):
    ts = list(ts)
    while True:
        j = next((k for k, t in enumerate(ts) if t == ")"), None)
        if j is None:
            return flat_eval(ts, prec, mode, rtl)
        i = max(k for k in range(j) if ts[k] == "(")
        v = flat_eval(ts[i + 1:j], prec, mode, rtl)
        if v is None:
            return None
        ts[i:j + 1] = [v]


def ev(s, mode="std"):
    ts = tokens(s)
    if mode in LEVELS:
        return ev_tokens(ts, LEVELS[mode])
    if mode == "rtl":
        return ev_tokens(ts, rtl=True)
    if mode == "noparen":
        return ev_tokens([t for t in ts if t not in ("(", ")")])
    if mode in ("std", "sq2", "negneg", "drop", "subneg"):
        return ev_tokens(ts, mode=mode)
    raise ValueError(mode)


def py_check(s, v):
    p = []
    for t in tokens(s):
        if isinstance(t, Fraction):
            p.append("Fraction(%d, %d)" % (t.numerator, t.denominator))
        else:
            p.append({"×": "*", "÷": "/", "−": "-", "^": "**"}.get(t, t))
    assert eval(" ".join(p), {"Fraction": Fraction}) == v, (s, v)


def steps(s, values=False):
    """One operation per step, innermost brackets first."""
    ts = tokens(s)
    out, made = [], []
    while len(ts) > 1:
        j = next((k for k, t in enumerate(ts) if t == ")"), None)
        if j is None:
            lo, hi = 0, len(ts)
        else:
            i = max(k for k in range(j) if ts[k] == "(")
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
        r = render(ts)
        if not out or out[-1] != r:
            out.append(r)
    return made if values else out


def val(s):
    v = ev(s)
    assert v is not None and v != 0 and nice(v), s
    py_check(s, v)
    return v


def chain(s):
    v = val(s)
    st = steps(s)
    assert st[-1] == fmt(v), (s, st)
    return " = ".join([H(s)] + st)


def before_last(s):
    m = steps(s, values=True)
    return max(m[-1]) if m and m[-1] else None


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e):
    """correct + the first 3 unique distractors."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or not c:
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


def B(s):
    return "<b>%s</b>" % s


def cap(s):
    return s[0].upper() + s[1:]


def svg_wrap(w, h, body, label):
    w, h = int(round(w)), int(round(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


ASK = ["Find the value of %s.", "What is the value of %s?", "Calculate %s.", "Work out %s."]

WP = "uses the wrong pair of numbers"
SIGN = "uses the wrong sign"

WHY = {
    "ltr": "comes from working left to right without doing × and ÷ first",
    "rev": "comes from adding or subtracting before multiplying or dividing",
    "mulfirst": "comes from multiplying before dividing, but × and ÷ have the same rank, so work left to right",
    "addfirst": "comes from adding before subtracting, but + and − have the same rank, so work left to right",
    "rtl": "comes from working from right to left",
    "noparen": "comes from ignoring the brackets",
    "sq2": "comes from doubling instead of squaring (a number squared is the number times itself)",
    "negneg": "comes from a sign error: two negatives multiplied or divided give a positive",
    "drop": "comes from a sign error: a negative and a positive multiplied or divided give a negative",
    "subneg": "comes from a sign error: subtracting a negative is the same as adding",
}


def mistakes(s, modes, extra=()):
    v = ev(s)
    out, seen = [], {v}

    def add(w, why):
        if w is None or w == 0 or w in seen or not nice(w):
            return
        if not ALLOW["neg"] and w < 0:
            return
        if not ALLOW["dec"] and w.denominator != 1:
            return
        seen.add(w)
        out.append((w, why))

    for m in modes:
        add(ev(s, m), WHY[m])
    for x, why in extra:
        add(ev(x), why)
    add(before_last(s), "stops one step too early")
    return out


def why_text(ms, unit=fmt, n=2):
    return " ".join("Not %s: that %s." % (unit(w), why) for w, why in ms[:n])


def eval_item(s, k, modes, extra=()):
    v = val(s)
    ms = mistakes(s, modes, extra)
    assert len(ms) >= 3, (s, ms)
    e = chain(s) + ". " + why_text(ms)
    return mcq(ASK[k % len(ASK)] % B(H(s)), fmt(v), [fmt(x) for x, _ in ms], e)


def fields(t):
    return [x[1] for x in string.Formatter().parse(t) if x[1]]


def templated(rnd, T, used, vmax=1000, k0=0):
    its = []
    for k, (t, modes, extra, mk) in enumerate(T):
        names = fields(t)

        def build(d, t=t, names=names, extra=extra):
            m = dict(zip(names, map(src, d)))
            return t.format(**m), [(x.format(**m), why.format(**m)) for x, why in extra]

        def ok(d, modes=modes, build=build):
            if len(set(d)) != len(d):
                return False
            s, ex_ = build(d)
            v = ev(s)
            if v is None or v == 0 or abs(v) > vmax or not nice(v) or (v > 0 and v < 2 and not ALLOW["neg"]):
                return False
            w0 = ev(s, modes[0])
            if w0 is None or w0 == v or not nice(w0):
                return False
            return len(mistakes(s, modes, ex_)) >= 3

        for _ in range(20000):
            d = mk(rnd)
            if ok(d) and build(d)[0] not in used:
                break
        else:
            raise RuntimeError("no numbers for %s" % t)
        s, ex_ = build(d)
        used.add(s)
        its.append(eval_item(s, k + k0, modes, ex_))
    return its


def first_item(s, good, bad, why):
    return mcq("Which part of %s do you work out first?" % B(H(s)), good, bad, "%s. %s" % (chain(s), why))


def true_item(s, modes, extra=()):
    v = val(s)
    ms = mistakes(s, modes, extra)
    assert len(ms) >= 3, (s, ms)
    e = "%s, so %s = %s is correct. %s" % (chain(s), H(s), fmt(v), why_text(ms, n=3))
    return mcq("Which number sentence is correct?", "%s = %s" % (H(s), fmt(v)),
               ["%s = %s" % (H(s), fmt(w)) for w, _ in ms], e)


def dec1(n):
    return Fraction(n, 10)


def dec2(n):
    return Fraction(n, 100)




def T(x, y, s, size=15, fill=INK, anchor="middle", weight="700"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, size, weight, fill, anchor, s))


def tw(s, size=15):
    return len(s) * size * 0.58


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


# ------------------------------------------------------------ bar models
SEGFILL = {"u": FILL, "o": "#e3e3e3", "w": "#ffffff"}


def model_svg(rows, top=None, under=(), right=None, BW=360, label="bar model"):
    """Bar model drawn to scale.
    rows: [(name, [(value, text, style)])], style u (unit, green), o (other, grey), w (white).
    top: (v0, v1, text) bracket over row 0; under: [(row, v0, v1, text)] brackets under a row;
    right: text for a bracket on the right joining all rows. Text '?' is drawn in red."""
    names = [n for n, _ in rows]
    nw = max([tw(n, 15) for n in names] + [0])
    x0 = 8 + (nw + 10 if nw else 0)
    maxv = max(sum(v for v, _, _ in segs) for _, segs in rows)
    sc = BW / float(maxv)
    bh = 36
    out = []
    y = 38 if top else 8
    ys = []
    for i, (n, segs) in enumerate(rows):
        ys.append(y)
        y += bh + (38 if any(u[0] == i for u in under) else 16)
    Hh = y - 16 + 8 if not any(u[0] == len(rows) - 1 for u in under) else y - 38 + 44

    def col(t):
        return RED if t == "?" else INK

    for i, (n, segs) in enumerate(rows):
        ry = ys[i]
        if n:
            out.append(T(8, ry + 24, n, 15, INK, "start"))
        x = x0
        for v, t, st in segs:
            w = v * sc
            out.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                       % (x, ry, w, bh, SEGFILL[st], GREEN))
            if t:
                fs = 15 if tw(t, 15) + 6 <= w else 14
                assert tw(t, fs) + 4 <= w, (t, w)
                out.append(T(x + w / 2, ry + 24, t, fs, col(t)))
            x += w
    if top:
        v0, v1, t = top
        a, b = x0 + v0 * sc, x0 + v1 * sc
        ry = ys[0]
        out.append("<path d='M%.1f %d V%d H%.1f V%d' fill='none' stroke='%s' stroke-width='2'/>" % (a, ry - 4, ry - 11, b, ry - 4, INK))
        out.append(T((a + b) / 2, ry - 16, t, 16, col(t)))
    for r, v0, v1, t in under:
        a, b = x0 + v0 * sc, x0 + v1 * sc
        yb = ys[r] + bh
        out.append("<path d='M%.1f %d V%d H%.1f V%d' fill='none' stroke='%s' stroke-width='2'/>" % (a, yb + 4, yb + 11, b, yb + 4, RED if t == "?" else INK))
        out.append(T((a + b) / 2, yb + 30, t, 16, col(t)))
    W = x0 + BW + 8
    if right:
        xr = x0 + BW + 8
        y0, y1 = ys[0], ys[-1] + bh
        out.append("<path d='M%.1f %d H%.1f V%d H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (xr, y0, xr + 8, y1, xr, INK))
        out.append(T(xr + 14, (y0 + y1) / 2 + 6, right, 16, col(right), "start"))
        W = xr + 14 + tw(right, 16) + 8
    return svg_wrap(W, Hh, "".join(out), label)


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ set 1: × and ÷ before + and −
def set_order(rnd, used):
    ALLOW.update(neg=False, dec=False)
    R = rnd.randint
    T_ = [
        ("{a} + {b} × {c}", ["ltr"], [("{a} × {b} + {c}", WP)], lambda r: (R(2, 9), R(2, 9), R(2, 9))),
        ("{a} − {b} × {c}", ["ltr"], [("{a} × {b} − {c}", WP), ("{a} + {b} × {c}", SIGN)], lambda r: (R(40, 99), R(2, 9), R(2, 8))),
        ("{a} × {b} + {c}", ["rev"], [("{a} + {b} × {c}", WP), ("{a} × {b} − {c}", SIGN)], lambda r: (R(2, 9), R(3, 9), R(2, 9))),
        ("{a} × {b} − {c}", ["rev"], [("{a} − {b} × {c}", WP), ("{a} × {b} + {c}", SIGN)], lambda r: (R(4, 10), R(5, 10), R(2, 4))),
        ("{a} + {b} ÷ {c}", ["ltr"], [("{a} − {b} ÷ {c}", SIGN), ("{a} + {b} × {c}", "multiplies instead of dividing")],
         lambda r: (lambda c, q: (R(4, 30), c * q, c))(R(2, 9), R(2, 9))),
        ("{a} − {b} ÷ {c}", ["ltr"], [("{a} + {b} ÷ {c}", SIGN), ("{a} − {b} × {c}", "multiplies instead of dividing")],
         lambda r: (lambda c, q: (R(20, 60), c * q, c))(R(2, 9), R(2, 9))),
        ("{a} ÷ {b} + {c}", ["rev"], [("{a} ÷ {b} − {c}", SIGN), ("{a} × {b} + {c}", "multiplies instead of dividing")],
         lambda r: (lambda b, q: (b * q, b, R(2, 9)))(R(2, 6), R(4, 10))),
        ("{a} ÷ {b} − {c}", ["rev"], [("{a} ÷ {b} + {c}", SIGN), ("{a} − {c}", "leaves out the ÷ {b}")],
         lambda r: (lambda b, q: (b * q, b, R(2, q - 1)))(R(2, 9), R(5, 10))),
        ("{a} + {b} × {c}", ["ltr"], [("{a} × {c} + {b}", WP)], lambda r: (R(11, 60), R(3, 12), R(3, 10))),
        ("{a} + {b} × {c} − {d}", ["ltr", "rev"], [], lambda r: (R(2, 20), R(3, 9), R(3, 9), R(2, 9))),
        ("{a} × {b} + {c} × {d}", ["ltr", "rev"], [], lambda r: (R(2, 9), R(2, 12), R(2, 9), R(2, 9))),
        ("{a} × {b} − {c} × {d}", ["ltr", "rev"], [], lambda r: (R(6, 12), R(6, 10), R(2, 6), R(2, 6))),
        ("{a} ÷ {b} + {c} × {d}", ["ltr", "rev"], [], lambda r: (lambda b, q: (b * q, b, R(2, 9), R(2, 9)))(R(2, 9), R(2, 9))),
        ("{a} × {b} + {c} ÷ {d}", ["ltr", "rev"], [], lambda r: (lambda d, q: (R(2, 9), R(3, 9), d * q, d))(R(2, 9), R(2, 9))),
        ("{a} − {b} × {c} + {d}", ["ltr", "rev"], [], lambda r: (R(50, 99), R(2, 9), R(2, 6), R(2, 15))),
        ("{a} + {b} × {c} × {d}", ["ltr"], [("{a} + {b} × {c} + {d}", "adds {d} instead of multiplying by it")], lambda r: (R(5, 40), R(2, 6), R(2, 5), R(2, 5))),
        ("{a} × {b} − {c} ÷ {d}", ["ltr", "rev"], [], lambda r: (lambda d, q: (R(5, 10), R(5, 10), d * q, d))(R(2, 9), R(2, 9))),
    ]
    its = templated(rnd, T_, used)
    its.append(true_item("5 + 4 × 3", ["ltr"], [("5 × 4 + 3", WP)]))
    its.append(first_item("40 − 30 ÷ 5", "30 ÷ 5", ["40 − 30", "Either part", "Neither part"], "Divide before you subtract."))
    assert val("6 × 4 + 18 ÷ 3") == 30 and ev("6 × 4 + 18 ÷ 3", "rev") == 44
    its.append(mcq("In %s, which operation do you do last?" % B(H("6 × 4 + 18 ÷ 3")), "The addition",
                   ["The multiplication", "The division", "It does not matter"],
                   "%s. Do × and ÷ first (6 × 4 = 24 and 18 ÷ 3 = 6), then add. "
                   "The order does matter: adding first gives 6 × 22 ÷ 3 = 44, a different answer." % chain("6 × 4 + 18 ÷ 3")))
    assert len(its) == 20, len(its)
    return {"title": "× and ÷ before + and −", "items": its}


# ------------------------------------------------------------ set 2: same rank, left to right
def set_ltr(rnd, used):
    ALLOW.update(neg=False, dec=False)
    R = rnd.randint
    ADD3 = ("{a} + {b} + {c}", "adds all three numbers")
    T_ = [
        ("{a} ÷ {b} × {c}", ["mulfirst"], [("{a} ÷ {b} + {c}", "adds the last number instead of multiplying")],
         lambda r: (lambda b, c, q: (b * c * q, b, c))(R(2, 6), R(2, 5), R(2, 5))),
        ("{a} − {b} + {c}", ["addfirst"], [ADD3], lambda r: (R(15, 40), R(5, 12), R(2, 6))),
        ("{a} − {b} − {c}", ["rtl"], [ADD3], lambda r: (R(20, 50), R(6, 15), R(2, 5))),
        ("{a} ÷ {b} × {c}", ["mulfirst"], [("{a} ÷ {b} + {c}", "adds the last number instead of multiplying")],
         lambda r: (lambda b, c, q: (b * c * q, b, c))(R(3, 9), R(2, 6), R(2, 4))),
        ("{a} − {b} + {c}", ["addfirst"], [ADD3], lambda r: (R(60, 150), R(15, 40), R(5, 25))),
        ("{a} ÷ {b} ÷ {c} + {d}", ["rtl", "rev"], [],
         lambda r: (lambda c, k, q: (c * k * c * q, c * k, c, R(2, 12)))(R(2, 4), R(2, 3), R(1, 5))),
        ("{a} + {b} − {c} + {d}", ["addfirst"], [("{a} + {b} + {c} + {d}", "adds all four numbers"), ("{a} + {b} − {c} − {d}", SIGN)],
         lambda r: (R(10, 40), R(10, 40), R(5, 20), R(2, 9))),
        ("{a} − {b} + {c} − {d}", ["addfirst", "rtl"], [], lambda r: (R(40, 90), R(10, 30), R(5, 20), R(2, 9))),
        ("{a} ÷ {b} × {c} + {d}", ["mulfirst", "rev"], [], lambda r: (lambda b, c, q: (b * c * q, b, c, R(2, 9)))(R(2, 6), R(2, 5), R(1, 4))),
        ("{a} − {b} ÷ {c} × {d}", ["mulfirst", "ltr"], [], lambda r: (lambda c, d, q: (R(40, 90), c * d * q, c, d))(R(2, 5), R(2, 5), R(1, 3))),
        ("{a} + {b} ÷ {c} × {d}", ["mulfirst", "ltr", "rev"], [], lambda r: (lambda c, d, q: (R(2, 20), c * d * q, c, d))(R(2, 5), R(2, 5), R(1, 4))),
        ("{a} − {b} × {c} ÷ {d}", ["ltr"], [("{a} − {b} × {c}", "leaves out the ÷ {d}"), ("{a} + {b} × {c} ÷ {d}", SIGN)],
         lambda r: (lambda d, q: (R(40, 99), d * q, R(2, 6), d))(R(2, 6), R(2, 5))),
        ("{a} ÷ {b} × {c} − {d}", ["mulfirst", "rev"], [], lambda r: (lambda b, c, q: (b * c * q, b, c, R(2, 9)))(R(2, 6), R(2, 5), R(2, 4))),
        ("{a} − {b} − {c} + {d}", ["rtl", "addfirst"], [], lambda r: (R(50, 99), R(10, 25), R(5, 15), R(2, 9))),
        ("{a} ÷ {b} ÷ {c} × {d}", ["rtl", "mulfirst"], [], lambda r: (lambda c, k, d: (c * k * c * d * 2, c * k, c, d))(R(2, 3), R(2, 3), R(2, 5))),
        ("{a} − {b} + {c} × {d}", ["addfirst", "ltr"], [], lambda r: (R(30, 60), R(10, 25), R(2, 9), R(2, 6))),
        ("{a} − {b} + {c} ÷ {d}", ["addfirst", "ltr"], [("{a} − {b} + {c} × {d}", "multiplies instead of dividing")],
         lambda r: (lambda d, q: (R(30, 70), R(10, 25), d * q, d))(R(2, 9), R(2, 9))),
    ]
    its = templated(rnd, T_, used, k0=1)
    its.append(true_item("24 ÷ 4 × 2", ["mulfirst"], [("24 × 4 ÷ 2", "swaps the order of the numbers")]))
    its.append(first_item("48 ÷ 6 × 2", "48 ÷ 6", ["6 × 2", "Either part", "Neither part"],
                          "× and ÷ have the same rank, so work from left to right."))
    its.append(true_item("20 − 8 + 3", ["addfirst"], [("20 + 8 + 3", "adds all three numbers"), ("20 + 8 − 3", "swaps the signs")]))
    assert len(its) == 20, len(its)
    return {"title": "Same rank: work from left to right", "items": its}


# ------------------------------------------------------------ set 3: brackets
def brackets_item(plain, target_expr, others):
    v = val(target_expr)
    assert tokens(plain) == [t for t in tokens(target_expr) if t not in ("(", ")")]
    vals = [val(x) for x in others]
    assert len(set(vals + [v])) == 4, (plain, vals, v)
    pv = val(plain)
    assert pv != v
    return mcq("Where do the brackets go to make this true?<br>%s" % B("%s = %s" % (H(plain), fmt(v))),
               H(target_expr), [H(x) for x in others],
               "%s. Without brackets, %s = %s." % (chain(target_expr), H(plain), fmt(pv)))


def set_brackets(rnd, used):
    ALLOW.update(neg=False, dec=False)
    R = rnd.randint
    PART = "uses only the first number in the brackets"
    T_ = [
        ("({a} + {b}) × {c}", ["noparen"], [("{a} × {c} + {b}", PART)], lambda r: (R(2, 9), R(2, 9), R(2, 9))),
        ("{a} × ({b} − {c})", ["noparen"], [("{a} × ({b} + {c})", SIGN)], lambda r: (R(3, 9), R(10, 20), R(2, 8))),
        ("({a} − {b}) × {c}", ["noparen"], [("{a} × {c} − {b}", PART)], lambda r: (R(30, 60), R(2, 9), R(2, 5))),
        ("{a} − ({b} + {c})", ["noparen"], [("{a} + {b} + {c}", "adds all three numbers")], lambda r: (R(40, 90), R(5, 20), R(5, 20))),
        ("({a} + {b}) ÷ {c}", ["noparen"], [("({a} + {b}) × {c}", "multiplies instead of dividing")],
         lambda r: (lambda c: (c * R(2, 6), c * R(2, 6), c))(R(2, 9))),
        ("{a} − ({b} − {c})", ["noparen"], [("{a} + ({b} − {c})", "adds the brackets instead of subtracting them")],
         lambda r: (R(30, 80), R(12, 25), R(3, 9))),
        ("{a} ÷ ({b} − {c})", ["noparen"], [("{a} ÷ ({b} + {c})", SIGN)], lambda r: (lambda c, d, q: (d * q, c + d, c))(R(2, 9), R(2, 9), R(2, 9))),
        ("({a} − {b}) ÷ {c}", ["noparen"], [("({a} − {b}) × {c}", "multiplies instead of dividing")],
         lambda r: (lambda b, c, q: (b + c * q, b, c))(R(2, 20), R(2, 9), R(2, 9))),
        ("{a} × ({b} + {c}) − {d}", ["noparen"], [("{a} × ({b} + {c} − {d})", "puts {d} inside the brackets")],
         lambda r: (R(2, 6), R(2, 9), R(2, 9), R(2, 15))),
        ("{a} ÷ ({b} × {c})", ["noparen"], [("{a} − {b} × {c}", "subtracts instead of dividing")],
         lambda r: (lambda b, c: (b * c * R(2, 5), b, c))(R(2, 4), R(2, 5))),
        ("{a} + ({b} − {c}) × {d}", ["noparen", "ltr"], [], lambda r: (R(2, 20), R(8, 15), R(2, 6), R(2, 6))),
        ("({a} + {b}) × ({c} − {d})", ["noparen"], [("{a} + {b} × ({c} − {d})", "ignores the first pair of brackets"),
                                                   ("({a} + {b}) × {c} − {d}", "ignores the second pair of brackets")],
         lambda r: (R(2, 9), R(2, 9), R(8, 15), R(2, 6))),
        ("{a} − {b} × ({c} − {d})", ["noparen", "ltr"], [], lambda r: (R(50, 99), R(2, 6), R(6, 12), R(2, 5))),
        ("{a} × ({b} + {c} × {d})", ["noparen", "ltr"], [], lambda r: (R(2, 5), R(2, 9), R(2, 6), R(2, 6))),
    ]
    its = templated(rnd, T_, used, k0=2)
    its.append(brackets_item("4 + 2 × 7 − 3", "(4 + 2) × 7 − 3", ["4 + 2 × (7 − 3)", "(4 + 2) × (7 − 3)", "4 + (2 × 7 − 3)"]))
    its.append(brackets_item("54 − 18 ÷ 6 + 3", "(54 − 18) ÷ 6 + 3", ["54 − 18 ÷ (6 + 3)", "(54 − 18) ÷ (6 + 3)", "54 − (18 ÷ 6 + 3)"]))
    its.append(brackets_item("7 × 8 − 3 + 2", "7 × (8 − 3 + 2)", ["7 × (8 − 3) + 2", "7 × 8 − (3 + 2)", "(7 × 8 − 3) + 2"]))
    its.append(brackets_item("2 + 6 × 3 + 4", "(2 + 6) × (3 + 4)", ["(2 + 6) × 3 + 4", "2 + 6 × (3 + 4)", "(2 + 6 × 3) + 4"]))
    its.append(first_item("60 − (14 + 6) × 2", "14 + 6", ["60 − 14", "6 × 2", "Either part"], "Brackets first, then ×, then −."))
    its.append(first_item("9 × (12 − 4) ÷ 6", "12 − 4", ["9 × 12", "4 ÷ 6", "Either part"],
                          "Work out the brackets first, then × and ÷ from left to right."))
    assert len(its) == 20, len(its)
    return {"title": "Brackets first", "items": its}


# ------------------------------------------------------------ set 4: mixed expressions
def set_mixed(rnd, used):
    ALLOW.update(neg=False, dec=False)
    R = rnd.randint

    def split(s):
        b = R(2, s - 2)
        return b, s - b

    T_ = [
        ("{a} × ({b} + {c}) ÷ {d}", ["noparen"], [("{a} × ({b} + {c}) × {d}", "multiplies by {d} instead of dividing"),
                                                 ("{a} × {b} + {c}", "ignores the brackets and leaves out the ÷ {d}")],
         lambda r: (lambda d: (R(2, 12), d * R(1, 5), d * R(1, 5), d))(R(3, 9))),
        ("({a} − {b}) ÷ {c} + {d} × {e}", ["noparen", "ltr"], [],
         lambda r: (lambda b, c: (b + c * R(3, 12), b, c, R(5, 30), R(2, 9)))(R(5, 40), R(3, 9))),
        ("{a} − ({b} + {c}) ÷ {d}", ["noparen", "ltr"], [],
         lambda r: (lambda d: (lambda b, c: (R(60, 200), b, c, d))(*split(d * R(3, 12))))(R(3, 9))),
        ("{a} × {b} − ({c} + {d}) × {e}", ["noparen", "ltr"], [],
         lambda r: (R(12, 40), R(5, 9), R(2, 9), R(2, 9), R(2, 6))),
        ("{a} + {b} × ({c} − {d}) ÷ {e}", ["noparen", "ltr"], [],
         lambda r: (lambda e: (R(10, 90), e * R(2, 6), R(12, 30), R(2, 9), e))(R(2, 6))),
        ("({a} + {b}) × {c} − {d} ÷ {e}", ["noparen", "rev"], [],
         lambda r: (lambda e: (R(10, 40), R(5, 30), R(3, 9), e * R(2, 9), e))(R(2, 9))),
        ("{a} ÷ ({b} − {c}) × {d}", ["noparen", "mulfirst"], [],
         lambda r: (lambda k, c: (k * R(3, 12), k + c, c, R(2, 9)))(R(3, 9), R(2, 20))),
        ("{a} − {b} ÷ {c} × {d} + {e}", ["mulfirst", "ltr"], [],
         lambda r: (lambda c: (R(100, 300), c * R(2, 9), c, R(2, 9), R(5, 40)))(R(2, 9))),
        ("{a} × {b} + {c} ÷ {d}", ["ltr", "rev"], [],
         lambda r: (lambda d: (25 * R(2, 9), R(2, 8), d * 10 * R(2, 9), d))(R(2, 5))),
        ("{a} − ({b} − {c}) × {d}", ["noparen", "ltr"], [],
         lambda r: (R(200, 900), R(30, 90), R(5, 25), R(2, 9))),
        ("({a} + {b}) ÷ ({c} − {d})", ["noparen"], [("({a} + {b}) ÷ {c} − {d}", "ignores the second pair of brackets"),
                                                   ("{a} + {b} ÷ ({c} − {d})", "ignores the first pair of brackets")],
         lambda r: (lambda k, d: (lambda a, b: (a, b, k + d, d))(*split(k * R(5, 15))))(R(3, 9), R(2, 9))),
        ("{a} × ({b} − {c} ÷ {d})", ["noparen", "ltr"], [],
         lambda r: (lambda d: (R(3, 12), R(20, 60), d * R(2, 9), d))(R(2, 9))),
        ("{a} ÷ {b} × ({c} + {d})", ["noparen", "mulfirst"], [],
         lambda r: (lambda b: (b * R(3, 15), b, R(2, 9), R(2, 9)))(R(2, 9))),
        ("{a} − {b} × {c} ÷ {d} + {e}", ["addfirst", "ltr"], [("{a} − {b} × {c} + {e}", "leaves out the ÷ {d}"),
                                                          ("{a} − {b} × {c} ÷ {d} − {e}", SIGN)],
         lambda r: (lambda d: (R(150, 500), d * R(2, 9), R(2, 9), d, R(10, 60)))(R(2, 9))),
    ]
    its = templated(rnd, T_, used, vmax=20000, k0=3)
    its.append(true_item("200 − (16 + 24) ÷ 8 × 5", ["ltr", "mulfirst", "noparen"]))
    its.append(first_item("3 × (45 − 15 ÷ 5)", "15 ÷ 5", ["45 − 15", "3 × 45", "Either part"],
                          "Work inside the brackets first. Inside the brackets, divide before you subtract."))
    assert val("(10 + 15) × 4") == 100
    its.append(mcq("What number goes in the box?<br><b>(☐ + 15) × 4 = 100</b>", "10", ["25", "40", "85"],
                   "The brackets are multiplied by 4, so first divide: 100 ÷ 4 = 25. Then ☐ + 15 = 25, so ☐ = 10. "
                   "Check: (10 + 15) × 4 = 25 × 4 = 100. Not 25: that is the value of the brackets. "
                   "Not 40: that adds 15 instead of taking it away. Not 85: that takes away 15 before dividing by 4."))
    exprs = ["48 − 6 × 2", "48 ÷ (6 − 2)", "48 ÷ 6 − 2", "48 ÷ 6 × 2"]
    vs = [val(x) for x in exprs]
    assert vs == [36, 12, 6, 16]
    its.append(mcq("Which expression has the greatest value?", H(exprs[0]), [H(x) for x in exprs[1:]],
                   "; ".join(chain(x) for x in exprs) + ". The greatest value is 36."))
    its.append(true_item("1000 − 25 × 8 + 600 ÷ 4", ["ltr"], [("1000 − 25 × 8 − 600 ÷ 4", SIGN)]))
    s = "36 + 4 × (18 − 9) ÷ 6"
    assert val(s) == 42
    its.append(mcq("In %s, which operation do you do last?" % B(H(s)), "The addition",
                   ["The subtraction", "The multiplication", "The division"],
                   "%s. Brackets first (18 − 9 = 9), then × and ÷ from left to right (4 × 9 = 36, 36 ÷ 6 = 6), and the addition last." % chain(s)))
    assert len(its) == 20, len(its)
    return {"title": "Mixed expressions with brackets", "items": its}


# ------------------------------------------------------------ set 5: word problems
def count(word):
    return lambda v: ("%s %s" % (fmt(v), word)) if v > 1 and v.denominator == 1 else None


UNITS = {
    "$": lambda v: money(v) if v.denominator == 1 else None,
    "cm": lambda v: (fmt(v) + " cm") if v > 0 and v.denominator == 1 else None,
    "points": count("points"), "flats": count("flats"), "stickers": count("stickers"), "seats": count("seats"),
    "rambutans": count("rambutans"), "oranges": count("oranges"),
}


def set_words(rnd, used):
    ALLOW.update(neg=False, dec=False)
    its = []

    def wp(text, s, unit, modes, extra=(), svg=None, units=""):
        v = val(s)
        u = UNITS[unit]
        ans = u(v)
        assert ans, (s, v)
        ms = [(w, why) for w, why in mistakes(s, modes, extra) if u(w)]
        assert len(ms) >= 3, (s, ms)
        e = "One expression: %s. %s, so the answer is %s. %s%s" % (B(H(s)), chain(s), ans, units, why_text(ms, u, 3))
        its.append(mcq((fig(svg) if svg else "") + text, ans, [u(w) for w, _ in ms], e))

    def which(text, good, bads, tail):
        val(good)
        its.append(mcq(text, H(good), [H(b) for b in bads], "%s. %s" % (chain(good), tail)))

    lab = "bar model"
    wp("A class of 38 P5 students goes on a learning journey. Each ticket costs $12 and the bus costs $180. What is the total cost?",
       "38 × 12 + 180", "$", ["rev"], [("38 + 12 + 180", "adds all the numbers")],
       model_svg([("", [(456, "38 × $12", "u"), (180, "$180", "o")])], top=(0, 636, "?"), label=lab + ": 38 tickets at 12 dollars and a 180 dollar bus, total unknown"))
    wp("Hui Min buys 3 bowls of laksa at $5 each. She pays with a $50 note. How much change does she get?",
       "50 − 3 × 5", "$", ["ltr"], [("50 − 5", "pays for only one bowl")],
       model_svg([("", [(5, "$5", "u"), (5, "$5", "u"), (5, "$5", "u"), (35, "", "w")])], top=(0, 50, "$50"),
                 under=[(0, 15, 50, "?")], label=lab + ": 50 dollars with 3 parts of 5 dollars spent, change unknown"))
    wp("Mdm Wong buys 6 plates of chicken rice at $4 each and 6 cups of sugarcane juice at $2 each. How much does she pay?",
       "6 × 4 + 6 × 2", "$", ["ltr", "rev"])
    wp("An HDB block has 12 floors with 8 flats on each floor. 9 of the flats are empty. How many flats have people living in them?",
       "12 × 8 − 9", "flats", ["rev"], [("12 × 8 + 9", SIGN), ("12 + 8 − 9", "adds instead of multiplying")])
    wp("Siti and Ali have 96 stickers altogether. Siti has 3 times as many stickers as Ali. How many stickers does Siti have?",
       "96 ÷ (3 + 1) × 3", "stickers", ["noparen", "mulfirst"],
       [("96 ÷ (3 + 1)", "is Ali’s stickers (1 unit), not Siti’s"), ("96 ÷ 3", "forgets that Ali is 1 unit too")],
       model_svg([("Ali", [(24, "", "u")]), ("Siti", [(24, "", "u"), (24, "", "u"), (24, "", "u")])],
                 under=[(1, 0, 72, "?")], right="96", label=lab + ": Ali 1 unit, Siti 3 units, 96 altogether"),
       "4 units = 96, 1 unit = 24, 3 units = 72. ")
    wp("Kumar has $500. He buys 4 bags at $45 each and a pair of shoes for $89. How much money does he have left?",
       "500 − 4 × 45 − 89", "$", ["rtl"], [("500 − 4 × 45", "forgets the shoes"), ("500 − 45 − 89", "pays for only one bag")],
       model_svg([("", [(45, "$45", "u"), (45, "$45", "u"), (45, "$45", "u"), (45, "$45", "u"), (89, "$89", "o"), (231, "", "w")])],
                 top=(0, 500, "$500"), under=[(0, 269, 500, "?")], BW=400,
                 label=lab + ": 500 dollars with 4 bags of 45 dollars and shoes of 89 dollars, money left unknown"))
    wp("At recess, a canteen stall sells 48 plates of fried noodles at $3 each and 36 cups of drinks at $2 each. How much money does the stall collect?",
       "48 × 3 + 36 × 2", "$", ["ltr", "rev"])
    wp("An MRT train has 6 cars. Each car has 48 seats. There are 40 people sitting down. How many seats are empty?",
       "6 × 48 − 40", "seats", ["rev"], [("6 × 48 + 40", SIGN), ("6 + 48 − 40", "adds instead of multiplying")])
    wp("Priya buys 4 files that cost the same and a pen for $6. She pays $38 in all. How much does each file cost?",
       "(38 − 6) ÷ 4", "$", ["noparen"], [("(38 + 6) ÷ 4", "adds the pen instead of taking it away"),
                                       ("(38 − 6) × 4", "multiplies instead of dividing")],
       model_svg([("", [(8, "?", "u"), (8, "", "u"), (8, "", "u"), (8, "", "u"), (6, "$6", "o")])], top=(0, 38, "$38"),
                 label=lab + ": 4 equal units for the files and 6 dollars for the pen make 38 dollars"),
       "4 units + $6 = $38, 4 units = $32, 1 unit = $8. ")
    which("Ali buys 3 plates of chicken rice at $4 each and a drink for $2. Which expression gives the total cost?",
          "3 × 4 + 2", ["3 × (4 + 2)", "(3 + 4) × 2", "3 + 4 × 2"],
          "So the total is $14. 3 × (4 + 2) would mean 3 drinks. The other two multiply the wrong numbers.")
    which("Mei Ling has $20. She buys 3 kaya toast sets at $5 each. Which expression gives the money she has left?",
          "20 − 3 × 5", ["(20 − 3) × 5", "20 − 3 + 5", "3 × 5 − 20"],
          "So she has $5 left. (20 − 3) × 5 subtracts before multiplying. 3 × 5 − 20 subtracts in the wrong order.")
    which("Two P5 classes, with 37 and 35 students, make groups of 6 for Sports Day. Which expression gives the number of groups?",
          "(37 + 35) ÷ 6", ["37 + 35 ÷ 6", "37 + 35 × 6", "6 ÷ (37 + 35)"],
          "So there are 12 groups. Brackets are needed: without them you would divide only the 35 by 6.")
    wp("A tray holds 24 rambutans. Mrs Ng buys 5 trays and shares the rambutans equally among 8 families. How many rambutans does each family get?",
       "5 × 24 ÷ 8", "rambutans", ["mulfirst"], [("5 × 24 × 8", "multiplies by 8 instead of dividing"),
                                              ("5 × 24 − 8", "takes away 8 instead of dividing"), ("5 × 24", "forgets to share")])
    wp("Jun Jie has $36 more than Wei Ming. Together they have $150. How much money does Wei Ming have?",
       "(150 − 36) ÷ 2", "$", ["noparen"], [("(150 + 36) ÷ 2", "adds the difference instead of taking it away"),
                                         ("150 ÷ 2", "shares equally, but Jun Jie has more")],
       model_svg([("Wei Ming", [(57, "?", "u")]), ("Jun Jie", [(57, "", "u"), (36, "$36", "o")])],
                 right="$150", label=lab + ": Wei Ming 1 unit, Jun Jie 1 unit and 36 dollars, 150 dollars altogether"),
       "2 units + $36 = $150, 2 units = $114, 1 unit = $57. ")
    wp("In a class quiz, each correct answer scores 4 points and each bonus question scores 10 points. Farah gets 17 correct answers and 2 bonus questions right. What is her score?",
       "17 × 4 + 2 × 10", "points", ["ltr", "rev"])
    which("A hawker sells 25 bowls of laksa in the morning and 30 bowls in the afternoon. Each bowl costs $5. Which expression gives the money she collects?",
          "(25 + 30) × 5", ["25 + 30 × 5", "25 × 30 + 5", "(25 + 5) × 30"],
          "So she collects $275. Without the brackets, only the 30 afternoon bowls would be multiplied by $5.")
    wp("A rope is 450 cm long. Raju cuts off 3 pieces of 85 cm each. How long is the rope that is left?",
       "450 − 3 × 85", "cm", ["ltr"], [("450 − 85", "cuts off only one piece"), ("450 + 3 × 85", SIGN)],
       model_svg([("", [(85, "85 cm", "u"), (85, "85 cm", "u"), (85, "85 cm", "u"), (195, "", "w")])], top=(0, 450, "450 cm"),
                 under=[(0, 255, 450, "?")], label=lab + ": 450 centimetres with 3 pieces of 85 centimetres cut off, rest unknown"))
    wp("Chloe buys 4 packs of 6 mandarin oranges for Chinese New Year. She gives 2 oranges to each of 9 relatives. How many oranges are left?",
       "4 × 6 − 2 × 9", "oranges", ["ltr"], [("4 × 6 − 9", "gives each relative only 1 orange"), ("4 × 6 + 2 × 9", SIGN)])
    which("Ahmad has 84 marbles. He keeps 12 and shares the rest equally among 6 friends. Which expression gives each friend’s share?",
          "(84 − 12) ÷ 6", ["84 − 12 ÷ 6", "84 ÷ 6 − 12", "(84 + 12) ÷ 6"],
          "So each friend gets 12 marbles. Brackets are needed so you subtract before you divide.")
    wp("Mrs Lim bakes 360 curry puffs. She packs them in boxes of 6 and sells each box for $4. How much money does she collect if she sells all the boxes?",
       "360 ÷ 6 × 4", "$", ["mulfirst"], [("360 × 4", "sells each curry puff for $4"), ("360 ÷ 6", "counts the boxes, not the money")])
    assert len(its) == 20, len(its)
    return {"title": "Word problems in one expression", "items": its}


# ------------------------------------------------------------ lesson
def steps_svg(rows, label, W=340):
    fs, lh = 22, 40
    Hh = 16 + lh * len(rows)
    out = []
    for i, (parts, note) in enumerate(rows):
        y = 36 + i * lh
        span = "".join("<tspan fill='%s'>%s</tspan>" % ((p[1], p[0]) if isinstance(p, tuple) else (INK, p)) for p in parts)
        if i:
            out.append("<text x='34' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='end'>=</text>" % (y, fs, INK))
        out.append("<text x='40' y='%d' font-size='%d' font-weight='700' xml:space='preserve'>%s</text>" % (y, fs, span))
        if note:
            out.append("<text text-anchor='end' x='%d' y='%d' font-size='16' fill='%s'>%s</text>" % (W - 8, y - 2, BLUE, note))
    return svg_wrap(W, Hh, "".join(out), label)


def order_svg():
    boxes = [("1", "( )", "Brackets"), ("2", "× ÷", "left to right"), ("3", "+ −", "left to right")]
    bw, bh, gap = 120, 84, 28
    W = 3 * bw + 2 * gap + 8
    out = ["<defs><marker id='ar' viewBox='0 0 10 10' refX='8' refY='5' markerWidth='6' markerHeight='6' orient='auto'>"
           "<path d='M0 0 L10 5 L0 10 z' fill='%s'/></marker></defs>" % GREEN]
    for i, (num, big, small) in enumerate(boxes):
        x = 4 + i * (bw + gap)
        cx = x + bw // 2
        out.append("<rect x='%d' y='4' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>" % (x, bw, bh, FILL, GREEN))
        out.append("<text x='%d' y='28' font-size='18' font-weight='700' fill='%s' text-anchor='middle'>Step %s</text>" % (cx, GREEN, num))
        out.append("<text x='%d' y='54' font-size='20' font-weight='700' fill='%s' text-anchor='middle'>%s</text>" % (cx, INK, big))
        out.append("<text x='%d' y='77' font-size='14' fill='%s' text-anchor='middle'>%s</text>" % (cx, INK, small))
        if i < 2:
            out.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2' marker-end='url(#ar)'/>"
                       % (x + bw + 3, 4 + bh // 2, x + bw + gap - 3, 4 + bh // 2, GREEN))
    return svg_wrap(W, bh + 8, "".join(out),
                    "Order of operations: brackets, then multiplication and division from left to right, then addition and subtraction from left to right")


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    ALLOW.update(neg=False, dec=False)
    assert val("2 + 3 × 4") == 14 and ev("2 + 3 × 4", "ltr") == 20
    assert val("24 ÷ 4 × 2") == 12 and ev("24 ÷ 4 × 2", "mulfirst") == 3
    assert val("20 − 8 + 3") == 15 and ev("20 − 8 + 3", "addfirst") == 9
    assert val("(8 + 4) × 3 − 6") == 30 and ev("(8 + 4) × 3 − 6", "noparen") == 14
    assert val("7 + 6 × 8") == 55 and ev("7 + 6 × 8", "ltr") == 104
    assert val("(15 + 25) ÷ 5 + 3 × 6") == 26 and val("50 − 3 × 5") == 35 and ev("50 − 3 × 5", "ltr") == 235
    fig1 = steps_svg([([("24 ÷ 4", RED), " × 2"], "left to right"),
                      ([("6 × 2", RED)], ""),
                      ([("12", GREEN)], "")], "working out 24 divided by 4 times 2 step by step: 6 times 2 is 12")
    fig2 = steps_svg([([("(8 + 4)", RED), " × 3 − 6"], "brackets first"),
                      ([("12 × 3", RED), " − 6"], "then ×"),
                      ([("36 − 6", RED)], "then −"),
                      ([("30", GREEN)], "")], "working out 8 plus 4 in brackets, times 3, minus 6 step by step")
    fig3 = model_svg([("", [(5, "$5", "u"), (5, "$5", "u"), (5, "$5", "u"), (35, "", "w")])], top=(0, 50, "$50"),
                     under=[(0, 15, 50, "?")], label="bar model: 50 dollars with 3 parts of 5 dollars spent, change unknown")
    return (
        "<h2>Why the order matters</h2>"
        "<p>An expression with more than one operation can give different answers if people work in a different order. "
        "So everyone uses the same <b>order of operations</b>.</p>"
        "<figure class='sn-fig'>" + order_svg() +
        "<figcaption>Brackets first, then × and ÷ from left to right, then + and − from left to right.</figcaption></figure>" +
        table(["Step", "Do this", "Example"], [
            ["1", "Brackets", "(25 + 15) × 3 = 40 × 3 = 120"],
            ["2", "× and ÷, as equals, from left to right", "24 ÷ 4 × 2 = 6 × 2 = 12"],
            ["3", "+ and −, as equals, from left to right", "20 − 8 + 3 = 12 + 3 = 15"],
        ]) +
        ex("Multiply before you add", "Find the value of 7 + 6 × 8.", chain("7 + 6 × 8") + ". Not 104: that adds first.", "55") +
        "<h2>Same rank: work from left to right</h2>"
        "<p>× and ÷ have the same rank, so do whichever comes first from the left. The same is true for + and −. "
        "Division does <b>not</b> always come before multiplication, and addition does <b>not</b> always come before subtraction.</p>"
        "<figure class='sn-fig'>" + fig1 +
        "<figcaption>24 ÷ 4 × 2 = 12, not 3. Do not multiply 4 × 2 first.</figcaption></figure>" +
        "<h2>Brackets first</h2>"
        "<p>Brackets change the order. Work out what is inside the brackets before anything else.</p>"
        "<figure class='sn-fig'>" + fig2 +
        "<figcaption>(8 + 4) × 3 − 6 = 30. Without the brackets, 8 + 4 × 3 − 6 = 14.</figcaption></figure>" +
        ex("Brackets and all four operations", "Find the value of (15 + 25) ÷ 5 + 3 × 6.",
           chain("(15 + 25) ÷ 5 + 3 × 6") + ". Brackets first, then ÷ and ×, then +.", "26") +
        "<h2>Word problems as one expression</h2>"
        "<p>Draw a bar model, then write the whole problem as one expression. "
        "Use brackets when a sum or difference must be found before you multiply or divide.</p>"
        "<figure class='sn-fig'>" + fig3 +
        "<figcaption>3 bowls at $5 each are taken away from $50. The rest is the change.</figcaption></figure>" +
        ex("Change from $50", "Hui Min buys 3 bowls of laksa at $5 each. She pays with a $50 note. How much change does she get?",
           "One expression: " + chain("50 − 3 × 5") + ".", "$35") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["2 + 3 × 4 = 5 × 4 = 20", "Multiply first: 2 + 12 = 14"],
            ["24 ÷ 4 × 2 = 24 ÷ 8 = 3", "× and ÷ are equals: left to right, 6 × 2 = 12"],
            ["20 − 8 + 3 = 20 − 11 = 9", "+ and − are equals: left to right, 12 + 3 = 15"],
            ["(8 + 4) × 3 = 8 + 12 = 20", "Brackets first: 12 × 3 = 36"],
            ["50 − 3 × 5 = 47 × 5 = 235", "Multiply first: 50 − 15 = 35"],
        ])
    )


FAQ = [
    {"q": "What is the order of operations in P5 maths?",
     "a": "Work out the brackets first, then multiplication and division from left to right, then addition and subtraction from left to right. For example, 2 + 3 × 4 = 2 + 12 = 14, not 20."},
    {"q": "Do you always divide before you multiply?",
     "a": "No. Multiplication and division have the same rank, so you work from left to right. 24 ÷ 4 × 2 = 6 × 2 = 12, not 24 ÷ 8 = 3."},
    {"q": "What is the most common mistake with order of operations?",
     "a": "The most common mistake is working strictly from left to right, such as 50 − 3 × 5 = 47 × 5. Multiply first: 50 − 15 = 35."},
    {"q": "Is order of operations in the MOE Primary 5 syllabus?",
     "a": "Yes. The 2021 MOE Primary Mathematics syllabus covers order of operations and the use of brackets in Primary 5 Whole Numbers, without a calculator. Students use it again in P6 and in PSLE Paper 1."},
]


def gen():
    rnd = random.Random(65803)
    used = set()
    sets = [set_order(rnd, used), set_ltr(rnd, used), set_brackets(rnd, used), set_mixed(rnd, used), set_words(rnd, used)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            key = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert key not in seen, it["q"]
            seen.add(key)
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-5", "slug": "order-of-operations", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 5 Order of Operations",
        "seo_title": "P5 Order of Operations Worksheets: Free Primary 5 Maths with Answers (MOE Syllabus)",
        "short_title": "Order of Operations",
        "domain": "Number and Algebra",
        "standard_code": "Primary 5: Whole Numbers",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Order of operations without calculator; use of brackets without calculator",
        "meta_desc": "Free P5 maths practice on the order of operations: × and ÷ before + and −, left to right, brackets and word problems. 100 questions with answers.",
        "key_big": "Brackets first, then × and ÷ from left to right, then + and − from left to right.",
        "key_sub": "24 ÷ 4 × 2 = 6 × 2 = 12, not 3, and 2 + 3 × 4 = 2 + 12 = 14, not 20.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "bar model")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
