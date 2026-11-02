# -*- coding: utf-8 -*-
"""
CA-BC Grade 6 Math: Order of operations (BC Mathematics Curriculum, Computational fluency)
  python3 tools/gen_cabc_math_g6_order_of_operations.py
Order of operations with whole numbers (no exponents, no negatives, no decimals):
× and ÷ before + and −, left to right for operations of the same rank (12 ÷ 2 × 3 = 18, not 2),
brackets first, multiplication and division facts to 100 inside expressions, and BC word problems
written as one expression.

Expressions are written in a small source syntax and evaluated exactly with fractions.Fraction,
cross-checked with Python eval. Wrong answers come from real mistakes, computed by evaluating the
expression the wrong way: strictly left to right, + and − before × and ÷, × before ÷, + before −,
right to left, ignoring brackets, plus stopping one step early.
Engine adapted from gen_cabc_math_g7_order_of_operations.py.
Canadian English. 4-digit numbers have no separator; 5+ digits use a no-break space.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re, string
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-6")
UPDATED = "2026-11-02"
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


ASK = ["Evaluate %s.", "What is the value of %s?", "Calculate %s.", "Find the value of %s."]

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



# ------------------------------------------------------------ set 1: × and ÷ before + and −
def set_order(rnd, used):
    ALLOW.update(neg=False, dec=False)
    R = rnd.randint
    T = [
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
        ("{a} + {b} × {c}", ["ltr"], [("{a} × {c} + {b}", WP)], lambda r: (R(11, 60), R(3, 10), R(3, 10))),
        ("{a} + {b} × {c} − {d}", ["ltr", "rev"], [], lambda r: (R(2, 20), R(3, 9), R(3, 9), R(2, 9))),
        ("{a} × {b} + {c} × {d}", ["ltr", "rev"], [], lambda r: (R(2, 9), R(2, 9), R(2, 9), R(2, 9))),
        ("{a} × {b} − {c} × {d}", ["ltr", "rev"], [], lambda r: (R(6, 10), R(6, 10), R(2, 6), R(2, 6))),
        ("{a} ÷ {b} + {c} × {d}", ["ltr", "rev"], [], lambda r: (lambda b, q: (b * q, b, R(2, 9), R(2, 9)))(R(2, 9), R(2, 9))),
        ("{a} × {b} + {c} ÷ {d}", ["ltr", "rev"], [], lambda r: (lambda d, q: (R(2, 9), R(3, 9), d * q, d))(R(2, 9), R(2, 9))),
        ("{a} − {b} × {c} + {d}", ["ltr", "rev"], [], lambda r: (R(50, 99), R(2, 9), R(2, 6), R(2, 15))),
        ("{a} + {b} × {c} × {d}", ["ltr"], [("{a} + {b} × {c} + {d}", "adds {d} instead of multiplying by it")], lambda r: (R(5, 40), R(2, 6), R(2, 5), R(2, 5))),
        ("{a} × {b} − {c} ÷ {d}", ["ltr", "rev"], [], lambda r: (lambda d, q: (R(5, 10), R(5, 10), d * q, d))(R(2, 9), R(2, 9))),
    ]
    its = templated(rnd, T, used)
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
    T = [
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
    its = templated(rnd, T, used, k0=1)
    its.append(true_item("12 ÷ 2 × 3", ["mulfirst"], [("12 × 2 ÷ 3", "swaps the order of the numbers")]))
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
    T = [
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
    its = templated(rnd, T, used, k0=2)
    its.append(brackets_item("4 + 2 × 7 − 3", "(4 + 2) × 7 − 3", ["4 + 2 × (7 − 3)", "(4 + 2) × (7 − 3)", "4 + (2 × 7 − 3)"]))
    its.append(brackets_item("54 − 18 ÷ 6 + 3", "(54 − 18) ÷ 6 + 3", ["54 − 18 ÷ (6 + 3)", "(54 − 18) ÷ (6 + 3)", "54 − (18 ÷ 6 + 3)"]))
    its.append(brackets_item("7 × 8 − 3 + 2", "7 × (8 − 3 + 2)", ["7 × (8 − 3) + 2", "7 × 8 − (3 + 2)", "(7 × 8 − 3) + 2"]))
    its.append(brackets_item("2 + 6 × 3 + 4", "(2 + 6) × (3 + 4)", ["(2 + 6) × 3 + 4", "2 + 6 × (3 + 4)", "(2 + 6 × 3) + 4"]))
    its.append(first_item("60 − (14 + 6) × 2", "14 + 6", ["60 − 14", "6 × 2", "Either part"], "Brackets first, then ×, then −."))
    its.append(first_item("9 × (12 − 4) ÷ 6", "12 − 4", ["9 × 12", "4 ÷ 6", "Either part"],
                          "Work out the brackets first, then × and ÷ from left to right."))
    assert len(its) == 20, len(its)
    return {"title": "Brackets first", "items": its}


# ------------------------------------------------------------ set 4: facts to 100 in expressions
def set_facts(rnd, used):
    ALLOW.update(neg=False, dec=False)
    R = rnd.randint

    def F():
        return R(6, 9)

    T = [
        ("{a} × {b} + {c} × {d}", ["ltr", "rev"], [], lambda r: (F(), F(), F(), F())),
        ("{a} × {b} − {c} × {d}", ["ltr", "rev"], [], lambda r: (R(7, 10), R(7, 9), R(3, 6), R(3, 6))),
        ("{a} ÷ {b} + {c} ÷ {d}", ["ltr"], [("{a} ÷ {b} + {c} × {d}", "multiplies by {d} instead of dividing"),
                                             ("{a} ÷ {b} − {c} ÷ {d}", SIGN)],
         lambda r: (lambda b, d: (b * F(), b, d * F(), d))(F(), F())),
        ("{a} × {b} − {c} ÷ {d}", ["ltr"], [("{a} × {b} + {c} ÷ {d}", SIGN), ("{a} × {b} − {c} × {d}", "multiplies by {d} instead of dividing")],
         lambda r: (lambda d: (F(), F(), d * F(), d))(F())),
        ("{a} ÷ {b} + {c} × {d}", ["ltr"], [("{a} × {b} + {c} × {d}", "multiplies by {b} instead of dividing")],
         lambda r: (lambda b: (b * F(), b, F(), F()))(F())),
        ("{a} − {b} ÷ {c}", ["ltr"], [("{a} + {b} ÷ {c}", SIGN)], lambda r: (lambda c: (R(20, 99), c * F(), c))(F())),
        ("{a} ÷ {b} ÷ {c}", ["rtl"], [("{a} ÷ {c}", "leaves out the ÷ {b}")],
         lambda r: (lambda c, k: (lambda b: (b * R(2, 100 // b), b, c))(c * k))(R(2, 3), R(2, 4))),
        ("{a} + {b} × {c}", ["ltr"], [("{a} × {b} + {c}", WP)], lambda r: (R(10, 50), F(), F())),
        ("{a} × {b} + {c}", ["rev"], [("{a} + {b} × {c}", WP), ("{a} × {b} − {c}", SIGN)], lambda r: (F(), F(), R(10, 30))),
        ("{a} − {b} × {c}", ["ltr"], [("{a} × {b} − {c}", WP), ("{a} + {b} × {c}", SIGN)], lambda r: (R(60, 99), F(), F())),
        ("{a} ÷ {b} − {c}", ["rev"], [("{a} ÷ {b} + {c}", SIGN), ("{a} − {c}", "leaves out the ÷ {b}")],
         lambda r: (lambda b, q: (b * q, b, R(2, q - 2)))(F(), R(6, 10))),
        ("{a} ÷ {b} × {c} + {d}", ["mulfirst", "rev"], [], lambda r: (lambda b: (b * F(), b, R(2, 5), R(2, 9)))(F())),
        ("{a} − {b} × {c} − {d}", ["ltr", "rtl"], [], lambda r: (R(70, 99), F(), F(), R(2, 9))),
        ("{a} × {b} + {c} ÷ {d} − {e}", ["ltr", "rev"], [], lambda r: (lambda d: (F(), F(), d * F(), d, R(2, 9)))(F())),
    ]
    its = templated(rnd, T, used, vmax=200, k0=3)
    for it in its:
        nums = [int(x) for x in re.findall(r"\d+", re.sub(r"<[^>]+>", "", it["q"]))]
        assert max(nums) <= 100, it["q"]

    # which fact first
    s = "9 + 6 × 7"
    assert val(s) == 51
    its.append(mcq("Which fact do you use first to evaluate %s?" % B(H(s)), "6 × 7 = 42", ["9 + 6 = 15", "9 × 7 = 63", "6 + 7 = 13"],
                   "%s. Multiply before you add, so the first fact is 6 × 7 = 42." % chain(s)))
    # missing number
    assert 7 * 9 + 6 == 69 and 7 * 10 == 70
    its.append(mcq("What number goes in the box?<br><b>7 × ☐ + 6 = 69</b>", "9", ["63", "10", "75"],
                   "Take away the 6 first: 69 − 6 = 63. Then 7 × 9 = 63, so the number is 9. "
                   "Not 63: that stops before dividing by 7. Not 10: 7 × 10 + 6 = 76. "
                   "Not 75: that adds the 6 instead of taking it away."))
    its.append(true_item("8 × 7 − 4 × 9", ["ltr", "rev"]))
    good, bads = "6 × 9 − 6", ["6 × (9 − 6)", "6 + 9 × 6", "54 ÷ 6 + 6"]
    assert val(good) == 48 and all(val(b) != 48 for b in bads)
    its.append(mcq("Which expression has a value of <b>48</b>?", H(good), [H(b) for b in bads],
                   "%s. The others: %s; %s; %s." % (chain(good), chain(bads[0]), chain(bads[1]), chain(bads[2]))))
    its.append(true_item("100 − 9 × 8 + 6", ["ltr"], [("100 − 9 × 8 − 6", SIGN)]))
    assert val("81 ÷ 9 + 9 × 9") == 90
    its.append(mcq("In %s, which operation do you do last?" % B(H("81 ÷ 9 + 9 × 9")), "The addition",
                   ["The division", "The multiplication", "It does not matter"],
                   "%s. Use the facts 81 ÷ 9 = 9 and 9 × 9 = 81 first, then add." % chain("81 ÷ 9 + 9 × 9")))
    assert len(its) == 20, len(its)
    return {"title": "Multiplication and division facts in expressions", "items": its}


# ------------------------------------------------------------ set 5: word problems
def count(word):
    return lambda v: ("%s %s" % (fmt(v), word)) if v > 1 and v.denominator == 1 else None


UNITS = {
    "$": lambda v: money(v) if v.denominator == 1 else None,
    "km": lambda v: (fmt(v) + " km") if v > 0 and v.denominator == 1 else None,
    "points": count("points"), "slices": count("slices"), "bottles": count("bottles"),
    "seedlings": count("seedlings"), "seats": count("seats"), "bags": count("bags"), "people": count("people"),
}


def set_words(rnd, used):
    ALLOW.update(neg=False, dec=False)
    its = []

    def wp(text, s, unit, modes, extra=()):
        v = val(s)
        u = UNITS[unit]
        ans = u(v)
        assert ans, (s, v)
        ms = [(w, why) for w, why in mistakes(s, modes, extra) if u(w)]
        assert len(ms) >= 3, (s, ms)
        e = "One expression: %s. %s, so %s. %s" % (B(H(s)), chain(s), ans, why_text(ms, u, 3))
        its.append(mcq(text, ans, [u(w) for w, _ in ms], e))

    def which(text, good, bads, tail):
        val(good)
        its.append(mcq(text, H(good), [H(b) for b in bads], "%s. %s" % (chain(good), tail)))

    wp("A Grade 6 class of 27 students visits the Vancouver Aquarium. Each ticket costs $14, and the bus costs $250. What is the total cost?",
       "27 × 14 + 250", "$", ["rev"], [("27 + 14 + 250", "adds all the numbers")])
    wp("Arjun buys 4 packs of hockey cards at $6 each. He pays with a $50 bill. How much change does he get?",
       "50 − 4 × 6", "$", ["ltr"], [("50 − 6", "pays for only one pack")])
    wp("A family of 5 takes BC Ferries to Vancouver Island. The fare is $68 for the car and $19 for each person. What is the total fare?",
       "68 + 5 × 19", "$", ["ltr"], [("(68 + 19) × 5", "charges the car fare 5 times"), ("68 + 19", "counts only one person")])
    wp("Owen bikes 8 km to Stanley Park and 8 km back home. In the park he rides a 9 km loop on the seawall. How far does he bike in all?",
       "2 × 8 + 9", "km", ["rev"], [("8 + 9", "forgets the ride back home")])
    wp("A school raises $1240 at its Terry Fox Run. Then 6 classes each raise another $45 at a bake sale. How much does the school raise in all?",
       "1240 + 6 × 45", "$", ["ltr"], [("1240 + 45", "counts only one class")])
    wp("Two soccer teams, with 11 and 13 players, share 72 orange slices equally. How many slices does each player get?",
       "72 ÷ (11 + 13)", "slices", ["noparen"], [("72 − 11 − 13", "subtracts instead of dividing"),
                                             ("72 ÷ 2", "shares between the 2 teams, not between the players"),
                                             ("11 + 13", "is the number of players, not slices")])
    assert val("(3 × 24 + 8) ÷ 16") == 5
    wp("A lacrosse team has 3 cases of 24 water bottles. The coaches keep 8 bottles. The 16 players share the rest equally. How many bottles does each player get?",
       "(3 × 24 − 8) ÷ 16", "bottles", ["noparen"], [("3 × 24 − 8", "forgets to share among the players"),
                                                 ("(3 × 24 + 8) ÷ 16", "adds the coaches’ bottles instead of taking them away"),
                                                 ("3 × 24", "forgets the coaches and the sharing")])
    wp("In a class math game, a correct answer scores 5 points and a bonus question scores 10 points. Nadia gets 9 correct answers and 3 bonus questions. What is her score?",
       "9 × 5 + 3 × 10", "points", ["ltr", "rev"])
    wp("A class plants 6 rows of 9 cedar seedlings near the Fraser River. Later, 7 seedlings do not survive. How many seedlings are left?",
       "6 × 9 − 7", "seedlings", ["rev"], [("6 + 9 − 7", "adds instead of multiplying"), ("6 × 9 + 7", SIGN)])
    wp("A SkyTrain has 4 cars with 30 seats in each car. There are 25 people sitting down. How many seats are empty?",
       "4 × 30 − 25", "seats", ["rev"], [("4 × 30 + 25", SIGN), ("4 + 30 − 25", "adds instead of multiplying")])
    wp("A class orders 8 pizzas. Each pizza is cut into 8 slices. Each of the 30 students eats 2 slices. How many slices are left?",
       "8 × 8 − 30 × 2", "slices", ["ltr"], [("8 × 8 − 30", "gives each student only 1 slice")])
    wp("A day pass at a small ski hill near Kelowna costs $65 for an adult and $38 for a youth. How much do 2 adults and 3 youths pay?",
       "2 × 65 + 3 × 38", "$", ["ltr"], [("65 + 38", "pays for only one adult and one youth"),
                                       ("(2 + 3) × (65 + 38)", "pays both prices for every person")])
    wp("Liam picks 6 baskets of 12 peaches in the Okanagan. He packs them in bags of 8. How many bags does he fill?",
       "6 × 12 ÷ 8", "bags", ["mulfirst"], [("6 × 12", "forgets to put the peaches in bags"),
                                          ("6 × 12 × 8", "multiplies by 8 instead of dividing"),
                                          ("6 × 12 − 8", "subtracts 8 instead of dividing")])
    which("Ava buys 3 notebooks at $4 each and a binder for $7. Which expression gives the total cost?",
          "3 × 4 + 7", ["3 × (4 + 7)", "(3 + 4) × 7", "3 + 4 × 7"],
          "So the total is $19. 3 × (4 + 7) would mean 3 binders. The other two multiply the wrong numbers.")
    which("Hana has $40. She buys 3 movie tickets at $11 each. Which expression gives the money she has left?",
          "40 − 3 × 11", ["(40 − 3) × 11", "40 − 3 + 11", "3 × 11 − 40"],
          "So she has $7 left. (40 − 3) × 11 subtracts before multiplying. 3 × 11 − 40 subtracts in the wrong order.")
    which("Two classes, with 26 and 28 students, make teams of 6 for a field day. Which expression gives the number of teams?",
          "(26 + 28) ÷ 6", ["26 + 28 ÷ 6", "26 + 28 × 6", "6 ÷ (26 + 28)"],
          "So there are 9 teams. Brackets are needed: without them you would divide only the 28 by 6.")
    which("Zara earns $8 an hour for 5 hours of babysitting. She also gets a $10 tip. Which expression gives the money she earns?",
          "8 × 5 + 10", ["8 × (5 + 10)", "8 + 5 × 10", "(8 + 5) × 10"],
          "So she earns $50. 8 × (5 + 10) would pay her for 15 hours. The other two multiply the wrong numbers.")
    wp("Mateo saves $15 a week for 8 weeks. Then he spends $48 on soccer cleats and $12 on socks. How much money does he have left?",
       "15 × 8 − 48 − 12", "$", ["rtl"], [("15 × 8 + 48 + 12", "adds the costs instead of subtracting them")])
    wp("A whale-watching boat in Victoria takes 4 groups of 9 students and 6 teachers. How many people from the school are on the boat?",
       "4 × 9 + 6", "people", ["rev"], [("4 + 9 + 6", "adds all the numbers")])
    which("Ethan has 56 hockey cards. He keeps 8 and shares the rest equally among 6 friends. Which expression gives each friend’s share?",
          "(56 − 8) ÷ 6", ["56 − 8 ÷ 6", "56 ÷ 6 − 8", "(56 + 8) ÷ 6"],
          "So each friend gets 8 cards. Brackets are needed so you subtract before you divide.")
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
    boxes = [("1", "( )", "Brackets"), ("2", "÷ ×", "left to right"), ("3", "+ −", "left to right")]
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
                    "Order of operations: brackets, then division and multiplication from left to right, then addition and subtraction from left to right")


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
    assert val("12 ÷ 2 × 3") == 18 and ev("12 ÷ 2 × 3", "mulfirst") == 2
    assert val("20 − 8 + 3") == 15 and ev("20 − 8 + 3", "addfirst") == 9
    assert val("(8 + 4) × 3 − 6") == 30 and ev("(8 + 4) × 3 − 6", "noparen") == 14
    assert val("7 + 6 × 8") == 55 and ev("7 + 6 × 8", "ltr") == 104
    assert val("56 ÷ 8 + 9 × 6") == 61 and val("50 − 4 × 6") == 26 and ev("50 − 4 × 6", "ltr") == 276
    fig1 = steps_svg([([("12 ÷ 2", RED), " × 3"], "left to right"),
                      ([("6 × 3", RED)], ""),
                      ([("18", GREEN)], "")], "working out 12 divided by 2 times 3 step by step: 6 times 3 is 18")
    fig2 = steps_svg([([("(8 + 4)", RED), " × 3 − 6"], "brackets first"),
                      ([("12 × 3", RED), " − 6"], "then ×"),
                      ([("36 − 6", RED)], "then −"),
                      ([("30", GREEN)], "")], "working out 8 plus 4 in brackets, times 3, minus 6 step by step")
    return (
        "<h2>Why the order matters</h2>"
        "<p>An expression with more than one operation can give different answers if people work in a different order. "
        "So everyone uses the same <b>order of operations</b>.</p>"
        "<figure class='sn-fig'>" + order_svg() +
        "<figcaption>Brackets first, then ÷ and × from left to right, then + and − from left to right.</figcaption></figure>" +
        table(["Step", "Do this", "Example"], [
            ["1", "Brackets", "(25 + 15) × 3 = 40 × 3 = 120"],
            ["2", "÷ and ×, as equals, from left to right", "12 ÷ 2 × 3 = 6 × 3 = 18"],
            ["3", "+ and −, as equals, from left to right", "20 − 8 + 3 = 12 + 3 = 15"],
        ]) +
        "<p>Many Canadian classrooms remember the order as <b>BEDMAS</b>: Brackets, Exponents, Division and Multiplication, "
        "Addition and Subtraction. Grade 6 expressions have no exponents, so you can skip the E for now.</p>" +
        ex("Multiply before you add", "Evaluate 7 + 6 × 8.", chain("7 + 6 × 8") + ". Not 104: that adds first.", "55") +
        "<h2>Same rank: work from left to right</h2>"
        "<p>÷ and × have the same rank, so do whichever comes first from the left. The same is true for + and −. "
        "Division does <b>not</b> always come before multiplication.</p>"
        "<figure class='sn-fig'>" + fig1 +
        "<figcaption>12 ÷ 2 × 3 = 18, not 2. Do not multiply 2 × 3 first.</figcaption></figure>" +
        "<h2>Brackets first</h2>"
        "<p>Brackets change the order. Work out what is inside the brackets before anything else.</p>"
        "<figure class='sn-fig'>" + fig2 +
        "<figcaption>(8 + 4) × 3 − 6 = 30. Without the brackets, 8 + 4 × 3 − 6 = 14.</figcaption></figure>" +
        "<h2>Facts make it quick</h2>"
        "<p>Most steps use multiplication and division facts to 100. Know them well and each step takes a moment.</p>" +
        ex("Two facts, then add", "Evaluate 56 ÷ 8 + 9 × 6.", chain("56 ÷ 8 + 9 × 6") + ". The facts are 56 ÷ 8 = 7 and 9 × 6 = 54.", "61") +
        "<h2>Word problems as one expression</h2>"
        "<p>Write the whole problem as one expression, then use the order of operations. "
        "Use brackets when a sum or difference must be found before you multiply or divide.</p>" +
        ex("Change from $50", "Arjun buys 4 packs of hockey cards at $6 each and pays with a $50 bill. How much change does he get?",
           "One expression: " + chain("50 − 4 × 6") + ".", "$26") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["2 + 3 × 4 = 5 × 4 = 20", "Multiply first: 2 + 12 = 14"],
            ["12 ÷ 2 × 3 = 12 ÷ 6 = 2", "÷ and × are equals: left to right, 6 × 3 = 18"],
            ["20 − 8 + 3 = 20 − 11 = 9", "+ and − are equals: left to right, 12 + 3 = 15"],
            ["(8 + 4) × 3 = 8 + 12 = 20", "Brackets first: 12 × 3 = 36"],
            ["50 − 4 × 6 = 46 × 6 = 276", "Multiply first: 50 − 24 = 26"],
        ])
    )


FAQ = [
    {"q": "What is the order of operations in Grade 6 math?",
     "a": "Work out brackets first, then multiplication and division from left to right, then addition and subtraction from left to right. For example, 2 + 3 × 4 = 2 + 12 = 14, not 20."},
    {"q": "What does BEDMAS mean?",
     "a": "BEDMAS stands for Brackets, Exponents, Division and Multiplication, Addition and Subtraction. Division and multiplication are equals, and so are addition and subtraction, so 12 ÷ 2 × 3 = 18. Grade 6 work has no exponents yet."},
    {"q": "Is BEDMAS the same as PEMDAS and BODMAS?",
     "a": "Yes. PEMDAS (used in the US) and BODMAS (used in the UK) give the same order with different words. In all of them, × and ÷ have the same rank and so do + and −."},
    {"q": "Where is order of operations in the BC Grade 6 math curriculum?",
     "a": "It is in the Grade 6 Computational fluency content: order of operations with whole numbers. Students also build fluency with multiplication and division facts to 100, which they use at every step."},
]


def gen():
    rnd = random.Random(56806)
    used = set()
    sets = [set_order(rnd, used), set_ltr(rnd, used), set_brackets(rnd, used), set_facts(rnd, used), set_words(rnd, used)]
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
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-6", "slug": "order-of-operations", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 6 Order of Operations",
        "seo_title": "Grade 6 Order of Operations Worksheets: Free BEDMAS Math with Answer Key (BC Curriculum)",
        "short_title": "Order of Operations",
        "domain": "Computational fluency",
        "standard_code": "Grade 6: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/6/core",
        "standard_text": "Order of operations with whole numbers",
        "meta_desc": "Free Grade 6 math worksheets on the order of operations, matched to the BC curriculum: × and ÷ before + and −, "
                     "left to right, brackets, multiplication and division facts, and word problems. 100 questions with an answer key.",
        "key_big": "Brackets first, then ÷ and × from left to right, then + and − from left to right.",
        "key_sub": "2 + 3 × 4 = 14, not 20. 12 ÷ 2 × 3 = 18, not 2. 20 − 8 + 3 = 15, not 9.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
