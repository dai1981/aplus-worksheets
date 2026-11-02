# -*- coding: utf-8 -*-
"""
CA-BC Grade 7 Math: Order of operations (BC Mathematics Curriculum, Computational fluency)
  python3 tools/gen_cabc_math_g7_order_of_operations.py
BEDMAS with whole numbers, integers and decimals: × and ÷ before + and −, left to right for
operations of the same rank (12 ÷ 2 × 3 = 18, not 2), brackets and simple squares, integers in
expressions, decimals, and BC word problems written as one expression.

Expressions are written in a small source syntax ("~8 + 3 × 4" is −8 + 3 × 4, "(5 + 2)^2" is
(5 + 2)²) and evaluated exactly with fractions.Fraction, cross-checked with Python eval.
Wrong answers come from real mistakes, computed by evaluating the expression the wrong way:
strictly left to right, + and − before × and ÷, × before ÷, + before −, right to left,
ignoring brackets, doubling instead of squaring, and sign errors with integers
((−4) × (−5) = −20, 6 − (−2) = 4, (−3)² = −9), plus stopping one step early.
Helpers are adapted from gen_au_maths_y6_order_of_operations.py, rewritten for BC.
Canadian English. 4-digit numbers have no separator; 5+ digits use a no-break space.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re, string
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-7")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
BLUE = "#2f6fb0"
FILL = "#cfe6d6"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
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
        ("{a} × {b} − {c}", ["rev"], [("{a} − {b} × {c}", WP), ("{a} × {b} + {c}", SIGN)], lambda r: (R(4, 12), R(5, 12), R(2, 4))),
        ("{a} + {b} ÷ {c}", ["ltr"], [("{a} − {b} ÷ {c}", SIGN), ("{a} + {b} × {c}", "multiplies instead of dividing")],
         lambda r: (lambda c, q: (R(4, 30), c * q, c))(R(2, 9), R(2, 9))),
        ("{a} − {b} ÷ {c}", ["ltr"], [("{a} + {b} ÷ {c}", SIGN), ("{a} − {b} × {c}", "multiplies instead of dividing")],
         lambda r: (lambda c, q: (R(20, 60), c * q, c))(R(2, 9), R(2, 9))),
        ("{a} ÷ {b} + {c}", ["rev"], [("{a} ÷ {b} − {c}", SIGN), ("{a} × {b} + {c}", "multiplies instead of dividing")],
         lambda r: (lambda b, q: (b * q, b, R(2, 9)))(R(2, 6), R(4, 12))),
        ("{a} ÷ {b} − {c}", ["rev"], [("{a} ÷ {b} + {c}", SIGN), ("{a} − {c}", "leaves out the ÷ {b}")],
         lambda r: (lambda b, q: (b * q, b, R(2, q - 1)))(R(2, 9), R(5, 12))),
        ("{a} + {b} × {c}", ["ltr"], [("{a} × {c} + {b}", WP)], lambda r: (R(11, 60), R(3, 12), R(3, 12))),
        ("{a} + {b} × {c} − {d}", ["ltr", "rev"], [], lambda r: (R(2, 20), R(3, 9), R(3, 9), R(2, 9))),
        ("{a} × {b} + {c} × {d}", ["ltr", "rev"], [], lambda r: (R(2, 9), R(2, 9), R(2, 9), R(2, 9))),
        ("{a} × {b} − {c} × {d}", ["ltr", "rev"], [], lambda r: (R(6, 12), R(6, 12), R(2, 6), R(2, 6))),
        ("{a} ÷ {b} + {c} × {d}", ["ltr", "rev"], [], lambda r: (lambda b, q: (b * q, b, R(2, 9), R(2, 9)))(R(2, 9), R(2, 9))),
        ("{a} × {b} + {c} ÷ {d}", ["ltr", "rev"], [], lambda r: (lambda d, q: (R(2, 9), R(3, 9), d * q, d))(R(2, 9), R(2, 9))),
        ("{a} − {b} × {c} + {d}", ["ltr", "rev"], [], lambda r: (R(50, 99), R(2, 9), R(2, 6), R(2, 15))),
        ("{a} + {b} × {c} × {d}", ["ltr"], [("{a} + {b} × {c} + {d}", "adds {d} instead of multiplying by it")], lambda r: (R(5, 40), R(2, 6), R(2, 5), R(2, 5))),
        ("{a} × {b} − {c} ÷ {d}", ["ltr", "rev"], [], lambda r: (lambda d, q: (R(5, 12), R(5, 12), d * q, d))(R(2, 9), R(2, 9))),
    ]
    its = templated(rnd, T, used)
    its.append(true_item("5 + 4 × 3", ["ltr"], [("5 × 4 + 3", WP)]))
    its.append(first_item("40 − 30 ÷ 5", "30 ÷ 5", ["40 − 30", "Either part", "Neither part"], "Divide before you subtract."))
    assert val("6 × 4 + 18 ÷ 3") == 30
    its.append(mcq("In %s, which operation do you do last?" % B(H("6 × 4 + 18 ÷ 3")), "The addition", ["The multiplication", "The division", "It does not matter"],
                   "%s. Do × and ÷ first (6 × 4 = 24 and 18 ÷ 3 = 6), then add. "
                   "The order does matter: adding first gives 6 × 22 ÷ 3 = 44, a different answer." % chain("6 × 4 + 18 ÷ 3")))
    assert ev("6 × 4 + 18 ÷ 3", "rev") == 44
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
         lambda r: (lambda c, k, q: (c * k * c * q, c * k, c, R(2, 12)))(R(2, 4), R(2, 4), R(1, 5))),
        ("{a} + {b} − {c} + {d}", ["addfirst"], [("{a} + {b} + {c} + {d}", "adds all four numbers"), ("{a} + {b} − {c} − {d}", SIGN)], lambda r: (R(10, 40), R(10, 40), R(5, 20), R(2, 9))),
        ("{a} − {b} + {c} − {d}", ["addfirst", "rtl"], [], lambda r: (R(40, 90), R(10, 30), R(5, 20), R(2, 9))),
        ("{a} ÷ {b} × {c} + {d}", ["mulfirst", "rev"], [], lambda r: (lambda b, c, q: (b * c * q, b, c, R(2, 9)))(R(2, 6), R(2, 5), R(1, 4))),
        ("{a} − {b} ÷ {c} × {d}", ["mulfirst", "ltr"], [], lambda r: (lambda c, d, q: (R(40, 90), c * d * q, c, d))(R(2, 5), R(2, 5), R(1, 3))),
        ("{a} + {b} ÷ {c} × {d}", ["mulfirst", "ltr", "rev"], [], lambda r: (lambda c, d, q: (R(2, 20), c * d * q, c, d))(R(2, 5), R(2, 5), R(1, 4))),
        ("{a} − {b} × {c} ÷ {d}", ["ltr"], [("{a} − {b} × {c}", "leaves out the ÷ {d}"), ("{a} + {b} × {c} ÷ {d}", SIGN)], lambda r: (lambda d, q: (R(40, 99), d * q, R(2, 6), d))(R(2, 6), R(2, 5))),
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


# ------------------------------------------------------------ set 3: brackets and squares
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
        ("{a} + {b}^2", ["sq2"], [("({a} + {b})^2", "adds before squaring")], lambda r: (R(3, 20), R(3, 9))),
        ("({a} − {b}) × {c}", ["noparen"], [("{a} × {c} − {b}", PART)], lambda r: (R(30, 60), R(2, 9), R(2, 5))),
        ("({a} + {b})^2", ["noparen", "sq2"], [("{a}^2 + {b}^2", "squares each number separately")], lambda r: (R(2, 7), R(2, 6))),
        ("{a} − ({b} + {c})", ["noparen"], [("{a} + {b} + {c}", "adds all three numbers")], lambda r: (R(40, 90), R(5, 20), R(5, 20))),
        ("{a} × {b}^2", ["sq2"], [("({a} × {b})^2", "squares the product, but only {b} is squared")], lambda r: (R(2, 6), R(3, 9))),
        ("{a} ÷ ({b} − {c})", ["noparen"], [("{a} ÷ ({b} + {c})", SIGN)], lambda r: (lambda c, d, q: (d * q, c + d, c))(R(2, 9), R(2, 9), R(2, 9))),
        ("{a}^2 − {b}^2", ["sq2"], [("({a} − {b})^2", "subtracts before squaring")], lambda r: (R(6, 12), R(2, 5))),
        ("{a} + ({b} − {c}) × {d}", ["noparen", "ltr"], [], lambda r: (R(2, 20), R(8, 15), R(2, 6), R(2, 6))),
        ("({a} − {b})^2 ÷ {c}", ["noparen", "sq2"], [], lambda r: (lambda c, b: (lambda d: (b + d, b, c))(c * R(1, 3)))(R(2, 4), R(2, 9))),
        ("({a} + {b}) × ({c} − {d})", ["noparen"], [("{a} + {b} × ({c} − {d})", "ignores the first pair of brackets"),
                                                   ("({a} + {b}) × {c} − {d}", "ignores the second pair of brackets")],
         lambda r: (R(2, 9), R(2, 9), R(8, 15), R(2, 6))),
        ("{a} − {b} × ({c} − {d})", ["noparen", "ltr"], [], lambda r: (R(50, 99), R(2, 6), R(6, 12), R(2, 5))),
        ("{a} × ({b} + {c} × {d})", ["noparen", "ltr"], [], lambda r: (R(2, 5), R(2, 9), R(2, 6), R(2, 6))),
    ]
    its = templated(rnd, T, used, k0=2)
    its.append(brackets_item("5 + 3 × 6 − 2", "(5 + 3) × 6 − 2", ["5 + 3 × (6 − 2)", "(5 + 3) × (6 − 2)", "5 + (3 × 6 − 2)"]))
    its.append(brackets_item("48 − 12 ÷ 4 + 2", "(48 − 12) ÷ 4 + 2", ["48 − 12 ÷ (4 + 2)", "(48 − 12) ÷ (4 + 2)", "48 − (12 ÷ 4 + 2)"]))
    its.append(brackets_item("8 × 9 − 4 + 3", "8 × (9 − 4 + 3)", ["8 × (9 − 4) + 3", "8 × 9 − (4 + 3)", "(8 × 9 − 4) + 3"]))
    its.append(brackets_item("3 + 5 × 4 + 2", "(3 + 5) × (4 + 2)", ["(3 + 5) × 4 + 2", "3 + 5 × (4 + 2)", "(3 + 5 × 4) + 2"]))
    its.append(first_item("60 − (14 + 6) × 2", "14 + 6", ["60 − 14", "6 × 2", "Either part"], "Brackets first, then ×, then −."))
    assert val("3 + 4^2") == 19
    its.append(mcq("In BEDMAS, what does the E stand for?", "Exponents, like 4²", ["Equals signs", "Estimating", "Even numbers"],
                   "BEDMAS: Brackets, Exponents, Division and Multiplication, Addition and Subtraction. "
                   "In Grade 7 the exponents are squares: 4² = 4 × 4 = 16, so 3 + 4² = 3 + 16 = 19."))
    assert len(its) == 20, len(its)
    return {"title": "Brackets and squares (BEDMAS)", "items": its}


# ------------------------------------------------------------ set 4: integers
def set_integers(rnd, used):
    ALLOW.update(neg=True, dec=False)
    R = rnd.randint
    T = [
        ("~{a} + {b} × {c}", ["ltr"], [("{a} + {b} × {c}", "drops the minus sign on −{a}")], lambda r: (R(6, 20), R(2, 9), R(2, 9))),
        ("{a} − {b} × {c}", ["ltr"], [("{b} × {c} − {a}", "subtracts in the wrong order")], lambda r: (R(2, 15), R(3, 9), R(3, 9))),
        ("{a} × ~{b} + {c}", ["drop"], [("{a} × ~{b} − {c}", "subtracts {c} instead of adding it")], lambda r: (R(2, 9), R(2, 9), R(2, 20))),
        ("~{a} × ~{b} − {c}", ["negneg"], [("~{a} × ~{b} + {c}", "adds {c} instead of subtracting it")], lambda r: (R(2, 9), R(2, 9), R(2, 20))),
        ("~{a} ÷ {b} + {c}", ["drop"], [("~{a} ÷ {b} − {c}", SIGN)], lambda r: (lambda b, q: (b * q, b, R(2, 12)))(R(2, 9), R(2, 9))),
        ("{a} − ~{b} × {c}", ["subneg", "ltr"], [], lambda r: (R(2, 15), R(2, 9), R(2, 6))),
        ("{a} + ~{b} × ~{c}", ["negneg", "ltr"], [], lambda r: (R(2, 20), R(2, 9), R(2, 9))),
        ("~{a}^2 + {b}", ["negneg", "sq2"], [], lambda r: (R(2, 9), R(2, 20))),
        ("{a} − {b} × ({c} − {d})", ["subneg", "noparen", "ltr"], [], lambda r: (R(2, 15), R(2, 6), R(1, 5), R(6, 12))),
        ("({a} − {b}) × ~{c}", ["negneg", "noparen"], [], lambda r: (R(2, 8), R(9, 15), R(2, 9))),
        ("~{a} ÷ ({b} − {c})", ["negneg", "noparen"], [], lambda r: (lambda b, d, q: (d * q, b, b + d))(R(2, 9), R(2, 6), R(2, 9))),
        ("~{a} − {b} × ~{c}", ["subneg", "ltr"], [], lambda r: (R(2, 15), R(2, 9), R(2, 9))),
        ("~{a} × {b} − ~{c} × {d}", ["subneg", "ltr"], [], lambda r: (R(2, 9), R(2, 9), R(2, 9), R(2, 9))),
        ("(~{a} + {b})^2", ["negneg", "noparen"], [("~{a}^2 + {b}^2", "squares each number separately")], lambda r: (R(5, 12), R(1, 4))),
        ("{a} ÷ ~{b} − {c} × ~{d}", ["drop", "subneg", "ltr"], [], lambda r: (lambda b, q: (b * q, b, R(2, 9), R(2, 9)))(R(2, 9), R(2, 9))),
        ("{a} − ({b} − {c})^2", ["negneg", "noparen", "sq2"], [], lambda r: (R(2, 20), R(1, 5), R(6, 11))),
        ("~{a} + {b} ÷ ~{c}", ["drop", "ltr"], [], lambda r: (lambda c, q: (R(2, 20), c * q, c))(R(2, 9), R(2, 9))),
    ]
    its = templated(rnd, T, used, vmax=200, k0=3)
    its.append(true_item("~2 × ~3 + 4", ["negneg"], [("~2 × ~3 − 4", "subtracts 4 instead of adding it")]))
    assert val("7 − ~3 × 2") == 13
    its.append(mcq("Which part of %s do you work out first?" % B(H("7 − ~3 × 2")), "(−3) × 2",
                   ["7 − (−3)", "7 − 3", "Either part"],
                   "%s. Multiply first: (−3) × 2 = −6. Then subtracting −6 is the same as adding 6." % chain("7 − ~3 × 2")))
    vals = {x: val(x) for x in ["6 − 2 × 5", "~4 × ~5", "~3^2", "~12 ÷ ~4"]}
    assert vals["6 − 2 × 5"] == -4 and all(v > 0 for k, v in vals.items() if k != "6 − 2 × 5")
    its.append(mcq("Which expression has a <b>negative</b> value?", H("6 − 2 × 5"), [H("~4 × ~5"), H("~3^2"), H("~12 ÷ ~4")],
                   "6 − 2 × 5 = 6 − 10 = −4. The others are positive: (−4) × (−5) = 20, (−3)² = (−3) × (−3) = 9 and (−12) ÷ (−4) = 3."))
    assert len(its) == 20, len(its)
    return {"title": "Integers in expressions", "items": its}


# ------------------------------------------------------------ set 5: decimals and word problems
UNITS = {
    "$": money,
    "°C": lambda v: fmt(v) + "°C",
    "m": lambda v: fmt(v) + " m",
    "km": lambda v: (fmt(v) + " km") if v > 0 else None,
    "mm": lambda v: (fmt(v) + " mm") if v > 0 else None,
    "": lambda v: fmt(v) if v > 0 and v.denominator == 1 else None,
    "points": lambda v: fmt(v) + " points",
    "slices": lambda v: (fmt(v) + " slices") if v > 1 and v.denominator == 1 else None,
    "bottles": lambda v: (fmt(v) + " bottles") if v > 1 and v.denominator == 1 else None,
}


def set_words(rnd, used):
    ALLOW.update(neg=False, dec=True)
    R = rnd.randint
    T = [
        ("{a} + {b} × {c}", ["ltr"], [("{a} × {b} + {c}", WP)], lambda r: (dec1(R(11, 99)), dec1(R(11, 49)), R(2, 9))),
        ("{a} × {b} − {c}", ["rev"], [("{a} × {b} + {c}", SIGN)], lambda r: (R(3, 9), dec2(R(1, 3) * 100 + R(1, 3) * 25), dec2(R(1, 9) * 25))),
        ("({a} + {b}) × {c}", ["noparen"], [("{a} + {b} + {c}", "adds instead of multiplying")], lambda r: (dec1(R(11, 49)), dec1(R(11, 49)), dec1(R(0, 2) * 10 + 5))),
        ("{a} − {b} ÷ {c}", ["ltr"], [("{a} − {b} × {c}", "multiplies instead of dividing")], lambda r: (lambda c, q: (R(10, 20), c * q, c))(R(2, 8), dec1(R(11, 39)))),
        ("{a} ÷ {b} × {c}", ["mulfirst"], [("{a} ÷ {b} + {c}", "adds the last number instead of multiplying")],
         lambda r: (lambda b, q: (b * q, b, R(2, 6)))(R(2, 6), dec1(R(11, 29)))),
        ("{a} × ({b} − {c})", ["noparen"], [("{a} × ({b} + {c})", SIGN)], lambda r: (R(2, 9), dec1(R(50, 99)), dec1(R(11, 45)))),
    ]
    its = templated(rnd, T, used, vmax=1000, k0=0)
    ALLOW.update(neg=True, dec=True)

    def wp(text, s, unit, modes, extra=(), note=""):
        v = val(s)
        u = UNITS[unit]
        ans = u(v)
        assert ans, (s, v)
        ms = [(w, why) for w, why in mistakes(s, modes, extra) if u(w)]
        assert len(ms) >= 3, (s, ms)
        e = "One expression: %s. %s, so %s. %s%s" % (B(H(s)), chain(s), ans, (note + " " if note else ""), why_text(ms, u, 3))
        its.append(mcq(text, ans, [u(w) for w, _ in ms], e))

    def which(text, good, bads, tail):
        val(good)
        its.append(mcq(text, H(good), [H(b) for b in bads], "%s. %s" % (chain(good), tail)))

    wp("A Grade 7 class of 28 students goes to Grouse Mountain. Each student pays $15, and the class pays $45 for the bus. What is the total cost?",
       "28 × 15 + 45", "$", ["rev"], [("28 + 15 + 45", "adds all the numbers")])
    wp("At 6:00 a.m. the temperature in Prince George is −8°C. It rises 3°C every hour for 4 hours. What is the temperature at 10:00 a.m.?",
       "~8 + 3 × 4", "°C", ["ltr"], [("3 × 4", "forgets the starting temperature"), ("8 + 3 × 4", "drops the minus sign on −8")])
    wp("Mei buys 3 bubble teas at $6.25 each. She pays with a $20 bill. How much change does she get?",
       "20 − 3 × 6.25", "$", ["ltr"], [("20 − 6.25", "pays for only one tea")])
    wp("A family takes BC Ferries to Vancouver Island. The fare is $62.50 for the car and $19.25 for each of the 4 people. What is the total fare?",
       "62.5 + 4 × 19.25", "$", ["ltr"], [("(62.5 + 19.25) × 4", "charges the car fare 4 times"), ("62.5 + 19.25", "counts only one person")])
    wp("Owen hikes 4.5 km to a lake in the Okanagan and 4.5 km back, plus a 2.4 km loop around the lake. How far does he hike in all?",
       "2 × 4.5 + 2.4", "km", ["rev"], [("4.5 + 2.4", "forgets the walk back")])
    wp("A school raises $1250 at its Terry Fox Run. Then 6 classes each raise another $85 at a bake sale. How much does the school raise in all?",
       "1250 + 6 × 85", "$", ["ltr"], [("1250 + 85", "counts only one class")])
    wp("Two soccer teams, with 18 and 14 players, share 96 orange slices equally. How many slices does each player get?",
       "96 ÷ (18 + 14)", "slices", ["noparen"], [("96 − 18 − 14", "subtracts instead of dividing"), ("18 + 14", "is the number of players, not slices"),
                                            ("96 ÷ 2", "shares between the 2 teams, not between the players")])
    wp("A scuba diver near Nanaimo is at −18 m (18 m below the surface). She rises 4 m three times, then sinks 5 m. Where is she now?",
       "~18 + 3 × 4 − 5", "m", ["ltr"], [("18 + 3 × 4 − 5", "forgets that −18 m is below the surface"),
                                         ("~18 − 3 × 4 − 5", "subtracts the rises instead of adding them")])
    wp("In a class quiz game, a correct answer scores 5 points and a wrong answer scores −3 points. Ji-woo gets 7 correct and 9 wrong. What is her score?",
       "7 × 5 + 9 × ~3", "points", ["ltr", "drop"], [], note="")
    which("Ava buys 2 notebooks at $3.75 each and a binder for $6.25. Which expression gives the total cost?",
          "2 × 3.75 + 6.25", ["2 × (3.75 + 6.25)", "(2 + 3.75) × 6.25", "2 + 3.75 × 6.25"],
          "So the total is $13.75. 2 × (3.75 + 6.25) would mean 2 binders. The other two multiply the wrong numbers.")
    which("Liam has $50. He buys 4 movie tickets at $8.75 each. Which expression gives the money he has left?",
          "50 − 4 × 8.75", ["(50 − 4) × 8.75", "50 − 4 + 8.75", "4 × 8.75 − 50"],
          "So he has $15 left. (50 − 4) × 8.75 subtracts before multiplying. 4 × 8.75 − 50 subtracts in the wrong order and gives −15.")
    wp("It rains 12.4 mm in Vancouver on Monday, 8.6 mm on Tuesday and 6.3 mm on Wednesday. What is the mean daily rainfall?",
       "(12.4 + 8.6 + 6.3) ÷ 3", "mm", ["noparen"], [("(12.4 + 8.6 + 6.3) × 3", "multiplies instead of dividing")])
    which("At noon the temperature in Kamloops is 4°C. It drops 2°C every hour for 5 hours. Which expression gives the new temperature?",
          "4 − 5 × 2", ["(4 − 5) × 2", "4 − 5 − 2", "5 × 2 − 4"],
          "So the new temperature is −6°C. (4 − 5) × 2 subtracts before multiplying. 5 × 2 − 4 subtracts in the wrong order and gives 6°C.")
    wp("A box lacrosse team of 12 players has 4 cases of 24 water bottles. They give 12 bottles to the coaches and share the rest equally among the players. How many bottles does each player get?",
       "(4 × 24 − 12) ÷ 12", "bottles", ["noparen"], [("4 × 24 − 12", "forgets to share among the players"),
                                               ("(4 × 24 + 12) ÷ 12", "adds the coaches’ bottles instead of taking them away")])
    assert ev("(4 × 24 − 12) ÷ 12") == 7 and ev("4 × 24 − 12 ÷ 12") == 95
    assert len(its) == 20, len(its)
    return {"title": "Decimals and word problems in one expression", "items": its}


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


def bedmas_svg():
    boxes = [("B", "( )", "Brackets"), ("E", "x²", "Exponents"), ("D M", "÷ ×", "left to right"), ("A S", "+ −", "left to right")]
    bw, bh, gap = 112, 84, 24
    W = 4 * bw + 3 * gap + 8
    out = ["<defs><marker id='ar' viewBox='0 0 10 10' refX='8' refY='5' markerWidth='6' markerHeight='6' orient='auto'>"
           "<path d='M0 0 L10 5 L0 10 z' fill='%s'/></marker></defs>" % GREEN]
    for i, (letter, big, small) in enumerate(boxes):
        x = 4 + i * (bw + gap)
        cx = x + bw // 2
        out.append("<rect x='%d' y='4' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>" % (x, bw, bh, FILL, GREEN))
        out.append("<text x='%d' y='28' font-size='20' font-weight='700' fill='%s' text-anchor='middle'>%s</text>" % (cx, GREEN, letter))
        out.append("<text x='%d' y='54' font-size='20' font-weight='700' fill='%s' text-anchor='middle'>%s</text>" % (cx, INK, big))
        out.append("<text x='%d' y='77' font-size='14' fill='%s' text-anchor='middle'>%s</text>" % (cx, INK, small))
        if i < 3:
            out.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2' marker-end='url(#ar)'/>"
                       % (x + bw + 3, 4 + bh // 2, x + bw + gap - 3, 4 + bh // 2, GREEN))
    return svg_wrap(W, bh + 8, "".join(out),
                    "BEDMAS: brackets, then exponents, then division and multiplication from left to right, then addition and subtraction from left to right")


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    ALLOW.update(neg=True, dec=True)
    assert val("2 + 3 × 4") == 14 and ev("2 + 3 × 4", "ltr") == 20
    assert val("12 ÷ 2 × 3") == 18 and ev("12 ÷ 2 × 3", "mulfirst") == 2
    assert val("20 − 8 + 3") == 15 and ev("20 − 8 + 3", "addfirst") == 9
    assert val("(5 + 3)^2 − 10") == 54 and val("~4 + 6 × ~2") == -16 and val("2.5 + 1.5 × 4") == 8.5
    assert val("8 − ~2 × 3") == 14 and ev("8 − ~2 × 3", "subneg") == 2 and val("~3^2") == 9 and ev("~3^2", "negneg") == -9
    assert val("20 − 3 × 6.25") == Fraction(5, 4)
    fig1 = steps_svg([([("12 ÷ 2", RED), " × 3"], "left to right"),
                      ([("6 × 3", RED)], ""),
                      ([("18", GREEN)], "")], "working out 12 divided by 2 times 3 step by step: 6 times 3 is 18")
    fig2 = steps_svg([(["(−4) + ", ("6 × (−2)", RED)], "multiply first"),
                      ([("(−4) + (−12)", RED)], "then add"),
                      ([("−16", GREEN)], "")], "working out negative 4 plus 6 times negative 2 step by step")
    return (
        "<h2>Why the order matters</h2>"
        "<p>An expression with more than one operation could give different answers if people worked in a different order. "
        "So everyone uses the same <b>order of operations</b>. In BC classrooms it is remembered as <b>BEDMAS</b>.</p>"
        "<figure class='sn-fig'>" + bedmas_svg() +
        "<figcaption>Brackets, then exponents, then ÷ and × from left to right, then + and − from left to right.</figcaption></figure>" +
        table(["Step", "Do this", "Example"], [
            ["1", "Brackets", "(25 + 15) × 3 = 40 × 3 = 120"],
            ["2", "Exponents (squares)", "3 + 4² = 3 + 16 = 19"],
            ["3", "÷ and ×, as equals, from left to right", "12 ÷ 2 × 3 = 6 × 3 = 18"],
            ["4", "+ and −, as equals, from left to right", "20 − 8 + 3 = 12 + 3 = 15"],
        ]) +
        "<h2>D and M are a team, and so are A and S</h2>"
        "<p>BEDMAS lists D before M, but division does <b>not</b> always come first. "
        "÷ and × have the same rank, so do whichever comes first from the left. The same is true for + and −.</p>"
        "<figure class='sn-fig'>" + fig1 +
        "<figcaption>12 ÷ 2 × 3 = 18, not 2. Do not multiply 2 × 3 first.</figcaption></figure>" +
        ex("Brackets and a square", "Evaluate (5 + 3)² − 10.", chain("(5 + 3)^2 − 10") + ".", "54") +
        "<h2>Integers and decimals</h2>"
        "<p>The order is the same with negative numbers and decimals. Use the integer sign rules at each step: "
        "two negatives multiplied or divided give a positive, and subtracting a negative is the same as adding.</p>"
        "<figure class='sn-fig'>" + fig2 +
        "<figcaption>Multiply first: 6 × (−2) = −12. Then (−4) + (−12) = −16.</figcaption></figure>" +
        ex("Subtracting a negative", "Evaluate 8 − (−2) × 3.",
           chain("8 − ~2 × 3") + ". Subtracting −6 is the same as adding 6.", "14") +
        ex("Decimals", "Evaluate 2.5 + 1.5 × 4.", chain("2.5 + 1.5 × 4") + ". Not 16: that adds first.", "8.5") +
        "<h2>Word problems as one expression</h2>"
        "<p>Write the whole problem as one expression, then use BEDMAS. Use brackets when a sum must be found before you multiply or divide.</p>" +
        ex("Change from $20", "Mei buys 3 bubble teas at $6.25 each and pays with a $20 bill. How much change does she get?",
           "One expression: 20 − 3 × 6.25 = 20 − 18.75 = 1.25.", "$1.25") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["2 + 3 × 4 = 5 × 4 = 20", "Multiply first: 2 + 12 = 14"],
            ["12 ÷ 2 × 3 = 12 ÷ 6 = 2", "÷ and × are equals: left to right, 6 × 3 = 18"],
            ["20 − 8 + 3 = 20 − 11 = 9", "+ and − are equals: left to right, 12 + 3 = 15"],
            ["4² = 8", "A square is the number times itself: 4 × 4 = 16"],
            ["(−3)² = −9", "(−3) × (−3) = 9. Two negatives give a positive"],
            ["8 − (−6) = 2", "Subtracting a negative means adding: 8 + 6 = 14"],
        ])
    )


FAQ = [
    {"q": "What is BEDMAS in Grade 7 math?",
     "a": "BEDMAS is the order of operations used in Canada: Brackets, Exponents, Division and Multiplication (left to right), then Addition and Subtraction (left to right). For example, 2 + 3 × 4 = 2 + 12 = 14, not 20."},
    {"q": "Is BEDMAS the same as PEMDAS and BODMAS?",
     "a": "Yes. PEMDAS (used in the US) and BODMAS (used in the UK) give the same order with different words. In all of them, × and ÷ have the same rank and so do + and −, so 12 ÷ 2 × 3 = 18."},
    {"q": "Where is order of operations in the BC Grade 7 math curriculum?",
     "a": "It is in the Grade 7 Computational fluency standard: operations with integers, including the order of operations. Students also use it with decimals and fractions and when they write expressions for word problems."},
    {"q": "Does order of operations help with the Grade 7 FSA?",
     "a": "Yes. The Grade 7 FSA numeracy section asks students to solve number problems, and many need more than one step. Writing a problem as one expression and using BEDMAS helps students get the steps in the right order."},
]


def gen():
    rnd = random.Random(37803)
    used = set()
    sets = [set_order(rnd, used), set_ltr(rnd, used), set_brackets(rnd, used), set_integers(rnd, used), set_words(rnd, used)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-7", "slug": "order-of-operations", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 7 Order of Operations (BEDMAS)",
        "seo_title": "Grade 7 Order of Operations Worksheets: Free BEDMAS Math with Answer Key (BC Curriculum)",
        "short_title": "Order of Operations",
        "domain": "Computational fluency",
        "standard_code": "Grade 7: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/7/core",
        "standard_text": "Operations with integers (addition, subtraction, multiplication, division, and order of operations)",
        "meta_desc": "Free Grade 7 math worksheets on the order of operations (BEDMAS), matched to the BC curriculum: × and ÷ before + and −, "
                     "left to right, brackets and squares, integers, decimals and word problems. 100 questions with an answer key, good FSA practice.",
        "key_big": "BEDMAS: brackets, exponents, then ÷ and × left to right, then + and − left to right.",
        "key_sub": "2 + 3 × 4 = 14, not 20. 12 ÷ 2 × 3 = 18, not 2. With integers, use the sign rules at each step: (−3)² = 9 and 8 − (−6) = 14.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
