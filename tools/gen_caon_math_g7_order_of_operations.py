# -*- coding: utf-8 -*-
"""
CA-ON Grade 7 Math: Order of operations (Ontario Curriculum 2020, Number B2.1)
  python3 tools/gen_caon_math_g7_order_of_operations.py
BEDMAS with whole numbers, decimals and fractions: × and ÷ before + and −, left to right for
operations of the same rank (12 ÷ 2 × 3 = 18, not 2), brackets and exponents (squares, cubes,
powers of 10), decimals and fractions in expressions, the distributive, commutative and
associative properties for mental math, and Ontario word problems (rates, ratios, percents)
written as one expression.

Expressions are written in a small source syntax ("~8 + 3 × 4" is −8 + 3 × 4, "(5 + 2)^3" is
(5 + 2)³, "3/4" is a fraction) and evaluated exactly with fractions.Fraction, cross-checked with
Python eval. Wrong answers come from real mistakes, computed by evaluating the expression the
wrong way: strictly left to right (3 + 4 × 2 = 14), + and − before × and ÷, × before ÷,
+ before −, right to left, ignoring brackets, multiplying the base by the exponent (2³ = 6),
subtracting a negative as if it were positive, and stopping one step early.
Grade 7 multiplies and divides integers only in Grade 8, so negatives appear only in
addition and subtraction.
Helpers are adapted from gen_cabc_math_g7_order_of_operations.py, rewritten for Ontario.
Canadian English. 4-digit numbers have no separator; 5+ digits use a no-break space.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re, string
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-7")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
BLUE = "#2f6fb0"
FILL = "#cfe6d6"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
MINUS = "−"
SUP = {2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶"}

STD = [("^",), ("×", "÷"), ("+", "−")]
LEVELS = {
    "ltr": [("^",), ("×", "÷", "+", "−")],          # strictly left to right
    "rev": [("^",), ("+", "−"), ("×", "÷")],        # + and − before × and ÷
    "mulfirst": [("^",), ("×",), ("÷",), ("+", "−")],  # × before ÷
    "addfirst": [("^",), ("×", "÷"), ("+",), ("−",)],  # + before −
}
# switched per set: whole-number sets do not allow negatives, decimals or fractions
ALLOW = {"neg": False, "dec": False, "frac": False}


# ------------------------------------------------------------ numbers
def group(n):
    s = str(n)
    if n < 10000:
        return s
    return "{:,}".format(n).replace(",", NB)


def nice(x):
    """Fraction mode: a small denominator. Otherwise a terminating decimal with at most 3 places."""
    if x is None:
        return False
    x = Fraction(x)
    if ALLOW["frac"]:
        return x.denominator <= 24
    return 1000 % x.denominator == 0


def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def fmt(x):
    x = Fraction(x)
    assert nice(x), x
    neg, x = x < 0, abs(x)
    w = int(x)
    if ALLOW["frac"] and x.denominator != 1:
        r = x - w
        s = fr(r.numerator, r.denominator)
        if w:
            s = group(w) + " " + s
    else:
        s = group(w)
        if x.denominator != 1:
            s += "." + str(int((x - w) * 1000)).zfill(3).rstrip("0")
    return (MINUS if neg else "") + s


def src(x):
    """Plain source text for a number (no grouping)."""
    x = Fraction(x)
    if x.denominator != 1 and (ALLOW["frac"] or 1000 % x.denominator):
        return "%d/%d" % (x.numerator, x.denominator)
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
TOK = re.compile(r"~?\d+/\d+|~?\d+(?:\.\d+)?|[×÷+−()^]")


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
            out += SUP[int(ts[i + 1])]
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
        if mode == "sq2":
            r = a * b
        else:
            r = a ** int(b)
    elif op == "×":
        r = a * b
    elif op == "÷":
        if not b:
            return None
        r = a / b
        if not nice(r) or (not ALLOW["dec"] and not ALLOW["frac"] and r.denominator != 1):
            return None
    elif op == "+":
        r = a + b
    else:
        r = a - b
        if mode == "subneg" and b < 0:
            r = a + b
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
    if mode in ("std", "sq2", "subneg"):
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
    "sq2": "comes from multiplying the base by the exponent (an exponent means repeated multiplication: 2³ = 2 × 2 × 2)",
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
        if not ALLOW["dec"] and not ALLOW["frac"] and w.denominator != 1:
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
            if v is None or v == 0 or abs(v) > vmax or not nice(v):
                return False
            if v > 0 and v < 2 and not (ALLOW["neg"] or ALLOW["dec"] or ALLOW["frac"]):
                return False
            if ALLOW["frac"] and v.denominator > 12:
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


def mode(neg=False, dec=False, frac=False):
    ALLOW.update(neg=neg, dec=dec, frac=frac)


# ------------------------------------------------------------ set 1: × and ÷ before + and −, then left to right
def set_order(rnd, used):
    mode()
    R = rnd.randint
    T = [
        ("{a} + {b} × {c}", ["ltr"], [("{a} × {b} + {c}", WP)], lambda r: (R(2, 9), R(2, 9), R(2, 9))),
        ("{a} − {b} × {c}", ["ltr"], [("{a} × {b} − {c}", WP), ("{a} + {b} × {c}", SIGN)], lambda r: (R(40, 99), R(2, 9), R(2, 8))),
        ("{a} × {b} + {c}", ["rev"], [("{a} + {b} × {c}", WP), ("{a} × {b} − {c}", SIGN)], lambda r: (R(6, 15), R(3, 12), R(2, 9))),
        ("{a} × {b} − {c}", ["rev"], [("{a} − {b} × {c}", WP), ("{a} × {b} + {c}", SIGN)], lambda r: (R(4, 12), R(5, 12), R(2, 4))),
        ("{a} + {b} ÷ {c}", ["ltr"], [("{a} − {b} ÷ {c}", SIGN), ("{a} + {b} × {c}", "multiplies instead of dividing")],
         lambda r: (lambda c, q: (R(4, 30), c * q, c))(R(2, 9), R(2, 9))),
        ("{a} − {b} ÷ {c}", ["ltr"], [("{a} + {b} ÷ {c}", SIGN), ("{a} − {b} × {c}", "multiplies instead of dividing")],
         lambda r: (lambda c, q: (R(20, 60), c * q, c))(R(2, 9), R(2, 9))),
        ("{a} ÷ {b} + {c}", ["rev"], [("{a} ÷ {b} − {c}", SIGN), ("{a} × {b} + {c}", "multiplies instead of dividing")],
         lambda r: (lambda b, q: (b * q, b, R(2, 9)))(R(2, 6), R(4, 12))),
        ("{a} + {b} × {c} − {d}", ["ltr", "rev"], [], lambda r: (R(2, 20), R(3, 9), R(3, 9), R(2, 9))),
        ("{a} × {b} + {c} × {d}", ["ltr", "rev"], [], lambda r: (R(2, 9), R(2, 9), R(2, 9), R(2, 9))),
        ("{a} × {b} − {c} × {d}", ["ltr", "rev"], [], lambda r: (R(6, 12), R(6, 12), R(2, 6), R(2, 6))),
        ("{a} ÷ {b} + {c} × {d}", ["ltr", "rev"], [], lambda r: (lambda b, q: (b * q, b, R(2, 9), R(2, 9)))(R(2, 9), R(2, 9))),
        ("{a} − {b} × {c} + {d}", ["ltr", "rev"], [], lambda r: (R(50, 99), R(2, 9), R(2, 6), R(2, 15))),
        ("{a} ÷ {b} × {c}", ["mulfirst"], [("{a} ÷ {b} + {c}", "adds the last number instead of multiplying")],
         lambda r: (lambda b, c, q: (b * c * q, b, c))(R(2, 6), R(2, 5), R(2, 5))),
        ("{a} − {b} + {c}", ["addfirst"], [("{a} + {b} + {c}", "adds all three numbers")], lambda r: (R(30, 90), R(12, 30), R(5, 20))),
        ("{a} ÷ {b} × {c} + {d}", ["mulfirst", "rev"], [], lambda r: (lambda b, c, q: (b * c * q, b, c, R(2, 9)))(R(2, 6), R(2, 5), R(1, 4))),
        ("{a} − {b} ÷ {c} × {d}", ["mulfirst", "ltr"], [], lambda r: (lambda c, d, q: (R(40, 90), c * d * q, c, d))(R(2, 5), R(2, 5), R(1, 3))),
        ("{a} − {b} − {c} + {d}", ["rtl", "addfirst"], [], lambda r: (R(50, 99), R(10, 25), R(5, 15), R(2, 9))),
    ]
    its = templated(rnd, T, used)
    assert val("3 + 4 × 2") == 11 and ev("3 + 4 × 2", "ltr") == 14
    its.append(true_item("3 + 4 × 2", ["ltr"], [("3 × 4 + 2", WP), ("3 + 4 + 2", "adds instead of multiplying")]))
    its.append(first_item("40 − 30 ÷ 5", "30 ÷ 5", ["40 − 30", "Either part", "Neither part"], "Divide before you subtract."))
    its.append(first_item("48 ÷ 6 × 2", "48 ÷ 6", ["6 × 2", "Either part", "Neither part"],
                          "× and ÷ have the same rank, so work from left to right."))
    assert len(its) == 20, len(its)
    return {"title": "× and ÷ before + and −", "items": its}


# ------------------------------------------------------------ set 2: brackets and exponents
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
    mode()
    R = rnd.randint
    PART = "uses only the first number in the brackets"
    T = [
        ("({a} + {b}) × {c}", ["noparen"], [("{a} × {c} + {b}", PART)], lambda r: (R(2, 9), R(2, 9), R(2, 9))),
        ("{a} × ({b} − {c})", ["noparen"], [("{a} × ({b} + {c})", SIGN)], lambda r: (R(3, 9), R(10, 20), R(2, 8))),
        ("{a} + {b}^2", ["sq2"], [("({a} + {b})^2", "adds before squaring")], lambda r: (R(3, 20), R(3, 9))),
        ("{a} − ({b} + {c})", ["noparen"], [("{a} + {b} + {c}", "adds all three numbers")], lambda r: (R(40, 90), R(5, 20), R(5, 20))),
        ("({a} + {b})^2", ["noparen", "sq2"], [("{a}^2 + {b}^2", "squares each number separately")], lambda r: (R(2, 7), R(2, 6))),
        ("{a} × {b}^2", ["sq2"], [("({a} × {b})^2", "squares the product, but only {b} is squared")], lambda r: (R(2, 6), R(3, 9))),
        ("{a}^3 + {b}", ["sq2"], [("({a} + {b})^3", "adds before cubing"), ("{a}^2 + {b}", "squares instead of cubing")], lambda r: (R(2, 5), R(3, 20))),
        ("{a} ÷ ({b} − {c})", ["noparen"], [("{a} ÷ ({b} + {c})", SIGN)], lambda r: (lambda c, d, q: (d * q, c + d, c))(R(2, 9), R(2, 9), R(2, 9))),
        ("{a}^2 − {b}^2", ["sq2"], [("({a} − {b})^2", "subtracts before squaring")], lambda r: (R(6, 12), R(2, 5))),
        ("{a} + ({b} − {c}) × {d}", ["noparen", "ltr"], [], lambda r: (R(2, 20), R(8, 15), R(2, 6), R(2, 6))),
        ("({a} − {b})^3 ÷ {c}", ["noparen", "sq2"], [], lambda r: (lambda b, d: (b + d, b, d))(R(2, 9), R(2, 4))),
        ("({a} + {b}) × ({c} − {d})", ["noparen"], [("{a} + {b} × ({c} − {d})", "ignores the first pair of brackets"),
                                                   ("({a} + {b}) × {c} − {d}", "ignores the second pair of brackets")],
         lambda r: (R(2, 9), R(2, 9), R(8, 15), R(2, 6))),
        ("{a} − {b} × ({c} − {d})", ["noparen", "ltr"], [], lambda r: (R(50, 99), R(2, 6), R(6, 12), R(2, 5))),
        ("{a} × ({b} + {c} × {d})", ["noparen", "ltr"], [], lambda r: (R(2, 5), R(2, 9), R(2, 6), R(2, 6))),
    ]
    its = templated(rnd, T, used, k0=2)
    its.append(brackets_item("5 + 3 × 6 − 2", "(5 + 3) × 6 − 2", ["5 + 3 × (6 − 2)", "(5 + 3) × (6 − 2)", "5 + (3 × 6 − 2)"]))
    its.append(brackets_item("48 − 12 ÷ 4 + 2", "(48 − 12) ÷ 4 + 2", ["48 − 12 ÷ (4 + 2)", "(48 − 12) ÷ (4 + 2)", "48 − (12 ÷ 4 + 2)"]))
    its.append(brackets_item("3 + 5 × 4 + 2", "(3 + 5) × (4 + 2)", ["(3 + 5) × 4 + 2", "3 + 5 × (4 + 2)", "(3 + 5 × 4) + 2"]))
    # powers of 10 (Grade 7 works with numbers to one billion)
    s = "4 × 10^5 + 3 × 10^3"
    v = val(s)
    assert v == 403000
    its.append(mcq("What is the value of %s?" % B(H(s)), fmt(v), [fmt(40300), fmt(4030000), fmt(290)],
                   "%s. 10⁵ is 1 followed by 5 zeros. Not 40%s300: that uses one zero too few in each power. "
                   "Not 290: that multiplies the 10 by the exponent (10⁵ is not 50)." % (chain(s), NB)))
    assert val("2^3") == 8
    its.append(mcq("What is the value of %s?" % B(H("2^3")), "8", ["6", "5", "9"],
                   "2³ = 2 × 2 × 2 = 8. Not 6: that multiplies the base by the exponent (2 × 3). "
                   "Not 5: that adds 2 + 3. Not 9: that is 3², the base and exponent swapped."))
    its.append(first_item("60 − (14 + 6) × 2", "14 + 6", ["60 − 14", "6 × 2", "Either part"], "Brackets first, then ×, then −."))
    assert len(its) == 20, len(its)
    return {"title": "Brackets and exponents (BEDMAS)", "items": its}


# ------------------------------------------------------------ set 3: decimals and fractions
def set_dec_frac(rnd, used):
    R = rnd.randint
    mode(dec=True)
    TD = [
        ("{a} + {b} × {c}", ["ltr"], [("{a} × {b} + {c}", WP)], lambda r: (dec1(R(11, 99)), dec1(R(11, 49)), R(2, 9))),
        ("{a} × {b} − {c}", ["rev"], [("{a} × {b} + {c}", SIGN)], lambda r: (R(3, 9), dec2(R(1, 3) * 100 + R(1, 3) * 25), dec2(R(1, 9) * 25))),
        ("({a} + {b}) × {c}", ["noparen"], [("{a} + {b} + {c}", "adds instead of multiplying")], lambda r: (dec1(R(11, 49)), dec1(R(11, 49)), dec1(R(0, 2) * 10 + 5))),
        ("{a} − {b} ÷ {c}", ["ltr"], [("{a} − {b} × {c}", "multiplies instead of dividing")], lambda r: (lambda c, q: (R(10, 20), c * q, c))(R(2, 8), dec1(R(11, 39)))),
        ("{a} ÷ {b} × {c}", ["mulfirst"], [("{a} ÷ {b} + {c}", "adds the last number instead of multiplying")],
         lambda r: (lambda b, q: (b * q, b, R(2, 6)))(R(2, 6), dec1(R(11, 29)))),
        ("{a} × ({b} − {c})", ["noparen"], [("{a} × ({b} + {c})", SIGN)], lambda r: (R(2, 9), dec1(R(50, 99)), dec1(R(11, 45)))),
        ("{a} × {b} + {c} × {d}", ["ltr", "rev"], [], lambda r: (dec1(5), R(4, 20) * 2, dec1(R(11, 29)), R(2, 6))),
        ("{a} ÷ {b} + {c}", ["rev"], [("{a} × {b} + {c}", "multiplies instead of dividing")],
         lambda r: (lambda b, q: (b * q, b, dec1(R(11, 49))))(dec1(R(2, 9)), R(2, 9))),
        ("{a}^2 + {b}", ["sq2"], [("({a} + {b})^2", "adds before squaring")], lambda r: (dec1(R(2, 9)), dec1(R(11, 39)))),
        ("{a} − {b} × {c}", ["ltr"], [("{a} − {b}", "leaves out the × {c}")], lambda r: (R(10, 30), dec2(R(1, 9) * 25 + R(1, 3) * 100), R(2, 4))),
    ]
    its = templated(rnd, TD, used, vmax=200)
    mode(frac=True)
    F = Fraction
    small = [F(1, 2), F(1, 3), F(2, 3), F(1, 4), F(3, 4), F(1, 5), F(2, 5), F(3, 5), F(1, 6), F(5, 6), F(1, 8), F(3, 8)]
    pick = lambda: rnd.choice(small)
    TF = [
        ("{a} + {b} × {c}", ["ltr"], [("{a} × {b} + {c}", WP)], lambda r: (pick(), pick(), R(2, 6))),
        ("{a} − {b} ÷ {c}", ["ltr"], [("{a} − {b} × {c}", "multiplies instead of dividing")], lambda r: (R(2, 5), pick(), R(2, 4))),
        ("{a} × {b} + {c}", ["rev"], [("{a} × {b} − {c}", SIGN)], lambda r: (pick(), R(2, 4) * 6, pick())),
        ("({a} + {b}) × {c}", ["noparen"], [("{a} + {b} + {c}", "adds instead of multiplying")], lambda r: (pick(), pick(), R(2, 6) * 4)),
        ("{a} ÷ ({b} − {c})", ["noparen"], [("{a} ÷ ({b} + {c})", SIGN)], lambda r: (R(2, 6), pick(), pick())),
        ("{a} × {b} − {c} × {d}", ["ltr", "rev"], [], lambda r: (pick(), R(2, 6) * 4, pick(), R(2, 6) * 3)),
        ("{a} − {b} + {c}", ["addfirst"], [("{a} + {b} + {c}", "adds all three numbers")], lambda r: (pick(), pick(), pick())),
        ("{a} ÷ {b} × {c}", ["mulfirst"], [("{a} ÷ {b} + {c}", "adds the last number instead of multiplying")], lambda r: (pick(), pick(), R(2, 6))),
        ("{a} + {b} × ({c} − {d})", ["noparen", "ltr"], [], lambda r: (pick(), pick(), R(3, 6), pick())),
    ]
    its += templated(rnd, TF, used, vmax=50, k0=1)
    s = "1/2 + 1/2 × 4"
    assert val(s) == F(5, 2) and ev(s, "ltr") == 4
    its.append(true_item(s, ["ltr"], [("1/2 × 4", "leaves out the first ½"), ("1/2 + 1/2 + 4", "adds instead of multiplying")]))
    assert len(its) == 20, len(its)
    return {"title": "Decimals and fractions in expressions", "items": its}


# ------------------------------------------------------------ set 4: properties for mental math
def set_props(rnd, used):
    mode()
    R = rnd.randint
    its = []
    F = Fraction

    def g(n):
        return fmt(F(n))

    # mental math with a number near a round number
    nears = rnd.sample([(98, 100), (99, 100), (49, 50), (199, 200), (102, 100), (101, 100), (52, 50), (298, 300)], 3)
    for (n, rr), a in zip(nears, rnd.sample(range(3, 10), 3)):
        d = abs(n - rr)
        op, nop = ("−", "+") if n < rr else ("+", "−")
        v = a * n
        part = a * rr - d if n < rr else a * rr + d
        sgn = a * rr + a * d if n < rr else a * rr - a * d
        e = "%s × %s = %s × %d %s %s × %d = %s %s %s = %s. Multiply <b>both</b> %d and %d by %d. Not %s: that multiplies only the %d." % (
            a, n, a, rr, op, a, d, g(a * rr), op, g(a * d), g(v), rr, d, a, g(part), rr)
        its.append(mcq("Use the distributive property to find %s mentally." % B("%d × %d" % (a, n)),
                       g(v), [g(part), g(sgn), g(a * rr)], e))
    # which expression is equal
    for n, a in [(59, 8), (103, 6), (48, 7)]:
        rr = (n + 5) // 10 * 10
        d = abs(n - rr)
        tens = n // 10 * 10
        op, nop = ("−", "+") if n < rr else ("+", "−")
        good = "%d × %d %s %d × %d" % (a, rr, op, a, d)
        bads = ["%d × %d %s %d" % (a, rr, op, d), "%d × %d %s %d × %d" % (a, rr, nop, a, d),
                "%d × %d + %d" % (a, tens, n - tens) if n < 100 else "%d × 10 + %d × 3" % (a, a)]
        v = val(good)
        assert v == a * n and all(val(b) != v for b in bads) and len({val(b) for b in bads}) == 3
        its.append(mcq("Which expression is equal to %s?" % B("%d × %d" % (a, n)), H(good), [H(b) for b in bads],
                       "%d is %d %s %d, so %d × %d = %s. Multiply both parts by %d, not just one."
                       % (n, rr, op, d, a, n, chain(good), a)))
    # missing number
    for a, n in [(9, 36), (7, 64)]:
        t, u = n // 10 * 10, n % 10
        its.append(mcq("What number goes in the box?<br>%s" % B("%d × %d = %d × %d + %d × □" % (a, n, a, t, a)),
                       str(u), [str(a * u), str(n), str(t)],
                       "%d = %d + %d, so %d × %d = %d × %d + %d × %d = %s + %d = %s." % (n, t, u, a, n, a, t, a, u, g(a * t), a * u, g(a * n))))
    # compatible numbers (commutative and associative)
    for p, m, q in [(25, 37, 4), (5, 86, 2), (50, 23, 2)]:
        v = p * m * q
        e = "Change the order: %d × %d = %d, so %d × %d × %d = %d × %d = %s. Not %s: that stops after %d × %d." % (
            p, q, p * q, p, m, q, p * q, m, g(v), g(p * m), p, m)
        its.append(mcq("Use the commutative property to find %s mentally." % B("%d × %d × %d" % (p, m, q)),
                       g(v), [g(p * m), g(v * 10), g(v // 10)], e))
    # name the property
    names = ["Distributive property", "Commutative property", "Associative property", "Identity property"]
    shown = [
        ("6 × (20 + 3) = 6 × 20 + 6 × 3", 0, "The 6 is shared out (distributed) over both parts of the sum."),
        ("4 × 17 × 25 = 4 × 25 × 17", 1, "Only the order of the numbers changes. Commutative means you can swap the order."),
        ("(8 × 5) × 3 = 8 × (5 × 3)", 2, "The numbers stay in the same order, but the brackets move. Associative means you can regroup."),
        ("3.75 × 1 = 3.75", 3, "Multiplying by 1 leaves a number the same. The identity for × is 1."),
    ]
    for s, k, why in shown:
        its.append(mcq("Which property does this show?<br>%s" % B(s.replace("−", MINUS)), names[k],
                       [x for i, x in enumerate(names) if i != k], why))
    # factoring out a common factor
    for a, b, c, sg in [(4, 23, 77, "+"), (6, 64, 36, "+"), (15, 37, 17, "−")]:
        s = "%d × %d %s %d × %d" % (a, b, sg, a, c)
        inner = b + c if sg == "+" else b - c
        v = val(s)
        wr = [val("%d × %d %s %d" % (a, b, sg, c)), (a + a) * inner, a + inner]
        assert len(set(wr + [v])) == 4
        its.append(mcq("Find %s mentally." % B(H(s)), g(v), [g(x) for x in wr],
                       "Both parts have the factor %d, so %s = %d × (%d %s %d) = %d × %d = %s. "
                       "Not %s: that forgets to multiply %d by %d." % (a, H(s), a, b, sg.replace("−", MINUS), c, a, inner, g(v), g(wr[0]), c, a)))
    # decimals
    mode(dec=True)
    for a, n in [(4, "2.99"), (6, "3.98")]:
        x = F(n)
        rr = int(x) + 1
        d = rr - x
        v = a * x
        e = "%s = %d %s %s, so %d × %s = %d × %d %s %d × %s = %d %s %s = %s." % (
            n, rr, MINUS, fmt(d), a, n, a, rr, MINUS, a, fmt(d), a * rr, MINUS, fmt(a * d), fmt(v))
        e += " Not %s: that subtracts %s only once." % (fmt(a * rr - d), fmt(d))
        its.append(mcq("Use mental math to find %s." % B("%d × %s" % (a, n)), fmt(v), [fmt(a * rr - d), fmt(a * rr + a * d), fmt(a * rr)], e))
    mode()
    assert len(its) == 20, len(its)
    for it in its:
        assert len(set(it["c"])) == 4, it
    return {"title": "Properties for mental math", "items": its}


# ------------------------------------------------------------ set 5: word problems
UNITS = {
    "$": money,
    "°C": lambda v: fmt(v) + "°C",
    "m": lambda v: fmt(v) + " m",
    "km": lambda v: (fmt(v) + " km") if v > 0 else None,
    "L": lambda v: (fmt(v) + " L") if v > 0 else None,
    "points": lambda v: fmt(v) + " points",
    "goals": lambda v: (fmt(v) + " goals") if v > 0 else None,
    "students": lambda v: (fmt(v) + " students") if v > 1 and v.denominator == 1 else None,
    "bottles": lambda v: (fmt(v) + " bottles") if v > 1 and v.denominator == 1 else None,
}


def set_words(rnd, used):
    its = []

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
        for b in bads:
            assert ev(b) != ev(good), b
        its.append(mcq(text, H(good), [H(b) for b in bads], "%s. %s" % (chain(good), tail)))

    mode(neg=True, dec=True)
    wp("A Grade 7 class of 27 students visits the Royal Ontario Museum. Each ticket costs $14, and the bus costs $325. What is the total cost?",
       "27 × 14 + 325", "$", ["rev"], [("27 + 14 + 325", "adds all the numbers"), ("14 + 325", "pays for only one student")])
    wp("At 7:00 a.m. the temperature in Thunder Bay is −11°C. It rises 2°C every hour for 5 hours. What is the temperature at noon?",
       "~11 + 2 × 5", "°C", ["ltr"], [("2 × 5", "forgets the starting temperature"), ("11 + 2 × 5", "drops the minus sign on −11")])
    wp("At the skating rink, Mei buys 3 hot chocolates at $3.75 each. She pays with a $20 bill. How much change does she get?",
       "20 − 3 × 3.75", "$", ["ltr"], [("20 − 3.75", "pays for only one hot chocolate")])
    wp("A canoe rental at a cottage costs $15 for the first hour and $9 for each extra hour. Liam rents a canoe for 4 hours. How much does he pay?",
       "15 + 3 × 9", "$", ["ltr"], [("15 + 4 × 9", "charges the first hour twice"), ("4 × 9", "uses $9 for every hour")])
    wp("A hockey stick costs $120. It is on sale for 25% off. Ethan also buys a roll of tape for $6. How much does he pay before tax?",
       "120 − 0.25 × 120 + 6", "$", [], [("0.25 × 120 + 6", "pays only the $30 discount plus the tape, not the sale price"),
                                              ("120 − 25 + 6", "takes off $25 instead of 25%")])
    wp("In a class of 30 students, the ratio of students who walk to school to students who take the bus is 2 : 3. How many students take the bus?",
       "30 ÷ (2 + 3) × 3", "students", ["noparen"], [("30 ÷ (2 + 3) × 2", "finds the students who walk"),
                                                     ("30 ÷ 3", "divides by 3 instead of by the 5 parts")])
    wp("Hana’s scores on four math quizzes are 18, 15, 20 and 17. What is her mean score?",
       "(18 + 15 + 20 + 17) ÷ 4", "points", ["noparen"], [("(18 + 15 + 20 + 17) × 4", "multiplies instead of dividing")])
    wp("At the Terry Fox Run, Noah runs 3 laps of a 1.6 km loop and then 0.8 km to the finish line. How far does he run in all?",
       "3 × 1.6 + 0.8", "km", ["rev"], [("1.6 + 0.8", "counts only one lap")])
    wp("A bus fare is $2.75. Olivia takes 2 bus rides a day for 5 school days. She starts with $40 on her transit card. How much is left at the end of the week?",
       "40 − 2 × 5 × 2.75", "$", ["ltr"], [("40 − 5 × 2.75", "counts only one ride a day"), ("40 − 2.75", "counts only one ride")])
    wp("A diver in Georgian Bay is at −12 m (12 m below the surface). She rises 3 m two times, then sinks 7 m. Where is she now?",
       "~12 + 2 × 3 − 7", "m", ["ltr"], [("12 + 2 × 3 − 7", "forgets that −12 m is below the surface"),
                                        ("~12 − 2 × 3 − 7", "subtracts the rises instead of adding them")])
    wp("In a class quiz game, a correct answer earns 4 points and a wrong answer loses 2 points. Arjun gets 8 correct and 5 wrong. What is his score?",
       "8 × 4 − 5 × 2", "points", ["ltr", "rev"], [("8 × 4 + 5 × 2", "adds the points for wrong answers")])
    wp("A ringette team of 15 players has 5 cases of 24 water bottles. They keep 30 bottles for the next game and share the rest equally among the players. How many bottles does each player get?",
       "(5 × 24 − 30) ÷ 15", "bottles", ["noparen"], [("5 × 24 − 30", "forgets to share among the players"),
                                                     ("(5 × 24 + 30) ÷ 15", "adds the 30 bottles instead of taking them away")])
    wp("A car uses 7.5 L of gas for every 100 km. A family drives 450 km from Toronto to Ottawa. How much gas does the car use?",
       "450 ÷ 100 × 7.5", "L", ["mulfirst"], [("450 ÷ 7.5", "divides by the rate")])
    mode(dec=True)
    wp("A school has 640 students. 15% walk to school and 25% take the bus. The rest come by car. How many students come by car?",
       "640 − (0.15 + 0.25) × 640", "students", ["noparen"], [("(0.15 + 0.25) × 640", "finds the students who walk or take the bus"),
                                                              ("640 − 0.15 × 640", "subtracts only the students who walk"),
                                                              ("640 − 40", "subtracts 40 instead of 40%")])
    wp("At a sugar bush, maple syrup costs $12 for a small bottle and $21 for a large jug. Chloe buys 3 bottles and 2 jugs. She pays with a $100 bill. How much change does she get?",
       "100 − (3 × 12 + 2 × 21)", "$", ["noparen"], [("3 × 12 + 2 × 21", "forgets to subtract from $100"),
                                                     ("100 − 3 × 12 − 21", "pays for only one jug")])
    wp("A hockey team plays 6 games. It scores 2 goals in each of 4 games and 5 goals in each of the other 2 games. What is the mean number of goals per game?",
       "(4 × 2 + 2 × 5) ÷ 6", "goals", ["noparen"], [("(4 × 2 + 2 × 5) ÷ 2", "divides by the 2 kinds of game, not the 6 games"),
                                                    ("(2 + 5) ÷ 2", "finds the mean of 2 and 5, not of the 6 games")])
    mode(frac=True)
    wp("Maya has 12 m of ribbon. She uses " + fr(3, 4) + " of it for a project, then buys 5 m more. How much ribbon does she have now?",
       "12 − 3/4 × 12 + 5", "m", ["ltr"], [("3/4 × 12 + 5", "adds to the part she used, not the part left")])
    mode(dec=True)
    which("Jayden buys 3 rolls of hockey tape at $4.25 each and a puck for $2.50. Which expression gives the total cost?",
          "3 × 4.25 + 2.5", ["3 × (4.25 + 2.5)", "(3 + 4.25) × 2.5", "3 + 4.25 × 2.5"],
          "So the total is $15.25. 3 × (4.25 + 2.5) would mean 3 pucks. The other two multiply the wrong numbers.")
    mode(neg=True)
    which("At 4:00 p.m. the temperature in Sudbury is 3°C. It drops 2°C every hour for 4 hours. Which expression gives the new temperature?",
          "3 − 4 × 2", ["(3 − 4) × 2", "3 − 4 − 2", "4 × 2 − 3"],
          "So the new temperature is −5°C. (3 − 4) × 2 subtracts before multiplying. 4 × 2 − 3 subtracts in the wrong order and gives 5°C.")
    mode()
    which("Priya earns $15 an hour babysitting. She works 3 hours on Friday and 4 hours on Saturday. Which expression gives her total pay?",
          "15 × (3 + 4)", ["15 × 3 + 4", "15 + 3 × 4", "(15 + 3) × 4"],
          "So she earns $105. Without the brackets, 15 × 3 + 4 adds only $4 for Saturday.")
    assert len(its) == 20, len(its)
    return {"title": "Multi-step word problems in one expression", "items": its}


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


def area_svg(a, t, u):
    """Area model for a × (t + u): two rectangles side by side, drawn to scale."""
    sc = 6
    w1, w2, h = t * sc, u * sc, a * sc
    x0, y0 = 30, 30
    out = [
        "<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (x0, y0, w1, h, FILL, GREEN),
        "<rect x='%d' y='%d' width='%d' height='%d' fill='#e8f1fa' stroke='%s' stroke-width='2'/>" % (x0 + w1, y0, w2, h, BLUE),
        "<text x='%d' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%d</text>" % (x0 + w1 / 2, y0 - 9, INK, t),
        "<text x='%d' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%d</text>" % (x0 + w1 + w2 / 2, y0 - 9, INK, u),
        "<text x='%d' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='end'>%d</text>" % (x0 - 7, y0 + h / 2 + 6, INK, a),
        "<text x='%d' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%d × %d = %d</text>" % (x0 + w1 / 2, y0 + h / 2 + 6, GREEN, a, t, a * t),
        "<text x='%d' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%d</text>" % (x0 + w1 + w2 / 2, y0 + h / 2 + 6, BLUE, a * u),
    ]
    return svg_wrap(x0 + w1 + w2 + 8, y0 + h + 8, "".join(out),
                    "area model: %d by %d split into %d by %d and %d by %d" % (a, t + u, a, t, a, u))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    mode(neg=True, dec=True)
    assert val("3 + 4 × 2") == 11 and ev("3 + 4 × 2", "ltr") == 14
    assert val("12 ÷ 2 × 3") == 18 and ev("12 ÷ 2 × 3", "mulfirst") == 2
    assert val("20 − 8 + 3") == 15 and ev("20 − 8 + 3", "addfirst") == 9
    assert val("(5 + 3)^2 − 10") == 54 and val("2.5 + 1.5 × 4") == 8.5 and val("2^3") == 8
    assert val("6 × 47") == 282 and val("20 − 3 × 3.75") == Fraction(35, 4)
    fig1 = steps_svg([(["3 + ", ("4 × 2", RED)], "multiply first"),
                      ([("3 + 8", RED)], "then add"),
                      ([("11", GREEN)], "")], "working out 3 plus 4 times 2 step by step: 3 plus 8 is 11")
    fig2 = steps_svg([([("12 ÷ 2", RED), " × 3"], "left to right"),
                      ([("6 × 3", RED)], ""),
                      ([("18", GREEN)], "")], "working out 12 divided by 2 times 3 step by step: 6 times 3 is 18")
    ex_dec = chain("2.5 + 1.5 × 4")
    mode(frac=True)
    ex_frac = chain("3/4 + 1/2 × 3")
    assert val("3/4 + 1/2 × 3") == Fraction(9, 4) and ev("3/4 + 1/2 × 3", "ltr") == Fraction(15, 4)
    wrong_frac = fmt(Fraction(15, 4))
    mode(neg=True, dec=True)
    return (
        "<h2>Why the order matters</h2>"
        "<p>An expression with more than one operation could give different answers if people worked in a different order. "
        "So everyone uses the same <b>order of operations</b>. In Ontario classrooms it is remembered as <b>BEDMAS</b>.</p>"
        "<figure class='sn-fig'>" + bedmas_svg() +
        "<figcaption>Brackets, then exponents, then ÷ and × from left to right, then + and − from left to right.</figcaption></figure>" +
        table(["Step", "Do this", "Example"], [
            ["1", "Brackets", "(25 + 15) × 3 = 40 × 3 = 120"],
            ["2", "Exponents", "3 + 2³ = 3 + 8 = 11"],
            ["3", "÷ and ×, as equals, from left to right", "12 ÷ 2 × 3 = 6 × 3 = 18"],
            ["4", "+ and −, as equals, from left to right", "20 − 8 + 3 = 12 + 3 = 15"],
        ]) +
        "<figure class='sn-fig'>" + fig1 +
        "<figcaption>3 + 4 × 2 = 11, not 14. Do not add 3 + 4 first.</figcaption></figure>" +
        "<h2>D and M are a team, and so are A and S</h2>"
        "<p>BEDMAS lists D before M, but division does <b>not</b> always come first. "
        "÷ and × have the same rank, so do whichever comes first from the left. The same is true for + and −.</p>"
        "<figure class='sn-fig'>" + fig2 +
        "<figcaption>12 ÷ 2 × 3 = 18, not 2. Do not multiply 2 × 3 first.</figcaption></figure>" +
        ex("Brackets and an exponent", "Evaluate (5 + 3)² − 10.", chain("(5 + 3)^2 − 10") + ".", "54") +
        "<p>An exponent means repeated multiplication: 2³ = 2 × 2 × 2 = 8, not 2 × 3 = 6. "
        "Powers of 10 help with large numbers: 4 × 10⁵ = 400" + NB + "000.</p>"
        "<h2>Decimals and fractions</h2>"
        "<p>The order is the same with decimals and fractions. Only the arithmetic at each step changes.</p>" +
        ex("Decimals", "Evaluate 2.5 + 1.5 × 4.", ex_dec + ". Not 16: that adds first.", "8.5") +
        ex("Fractions", "Evaluate " + fr(3, 4) + " + " + fr(1, 2) + " × 3.", ex_frac + ". Not " + wrong_frac + ": that adds first.", "2 " + fr(1, 4)) +
        "<h2>Properties make mental math faster</h2>"
        "<p>The <b>distributive property</b> lets you split a number into friendly parts: a × (b + c) = a × b + a × c. "
        "Multiply <b>both</b> parts.</p>"
        "<figure class='sn-fig'>" + area_svg(6, 40, 7) +
        "<figcaption>6 × 47 = 6 × 40 + 6 × 7 = 240 + 42 = 282.</figcaption></figure>"
        "<p>The <b>commutative</b> and <b>associative</b> properties let you change the order and the grouping of a product: "
        "25 × 37 × 4 = 25 × 4 × 37 = 100 × 37 = 3700.</p>"
        "<h2>Word problems as one expression</h2>"
        "<p>Write the whole problem as one expression, then use BEDMAS. Use brackets when a sum must be found before you multiply or divide.</p>" +
        ex("Change from $20", "Mei buys 3 hot chocolates at $3.75 each and pays with a $20 bill. How much change does she get?",
           "One expression: " + chain("20 − 3 × 3.75") + ".", "$8.75") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["3 + 4 × 2 = 7 × 2 = 14", "Multiply first: 3 + 8 = 11"],
            ["12 ÷ 2 × 3 = 12 ÷ 6 = 2", "÷ and × are equals: left to right, 6 × 3 = 18"],
            ["20 − 8 + 3 = 20 − 11 = 9", "+ and − are equals: left to right, 12 + 3 = 15"],
            ["2³ = 6", "An exponent means repeated multiplication: 2 × 2 × 2 = 8"],
            ["6 × 98 = 600 − 2 = 598", "Multiply both parts: 600 − 12 = 588"],
        ])
    )


FAQ = [
    {"q": "What is BEDMAS in Grade 7 math?",
     "a": "BEDMAS is the order of operations used in Ontario: Brackets, Exponents, Division and Multiplication (left to right), then Addition and Subtraction (left to right). For example, 3 + 4 × 2 = 3 + 8 = 11, not 14."},
    {"q": "Is BEDMAS the same as PEMDAS and BODMAS?",
     "a": "Yes. PEMDAS (used in the US) and BODMAS (used in the UK) give the same order with different words. In all of them, × and ÷ have the same rank and so do + and −, so 12 ÷ 2 × 3 = 18."},
    {"q": "Where is order of operations in the Ontario Grade 7 math curriculum?",
     "a": "It is in the Number strand, expectation B2.1: students use the properties and order of operations to solve problems with whole numbers, decimals, fractions, ratios, rates and percents, including multi-step problems."},
    {"q": "How does the distributive property help with mental math?",
     "a": "It lets you split a number into friendly parts and multiply each part. For example, 7 × 98 = 7 × 100 − 7 × 2 = 700 − 14 = 686."},
]


def gen():
    rnd = random.Random(47811)
    used = set()
    sets = [set_order(rnd, used), set_brackets(rnd, used), set_dec_frac(rnd, used), set_props(rnd, used), set_words(rnd, used)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-7", "slug": "order-of-operations", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 7 Order of Operations (BEDMAS)",
        "seo_title": "Grade 7 Order of Operations Worksheets: Free BEDMAS Math with Answer Key (Ontario Curriculum)",
        "short_title": "Order of Operations",
        "domain": "Number",
        "standard_code": "Grade 7: B2.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use the properties and order of operations, and the relationships between operations, to solve problems involving whole numbers, decimal numbers, fractions, ratios, rates, and percents, including those requiring multiple steps or multiple operations",
        "meta_desc": "Free Grade 7 math worksheets on the order of operations (BEDMAS), matched to the Ontario curriculum: × and ÷ before + and −, "
                     "brackets and exponents, decimals and fractions, the distributive property for mental math and multi-step word problems. 100 questions with an answer key.",
        "key_big": "BEDMAS: brackets, exponents, then ÷ and × left to right, then + and − left to right.",
        "key_sub": "3 + 4 × 2 = 11, not 14. 12 ÷ 2 × 3 = 18, not 2. 2³ = 2 × 2 × 2 = 8. Write a word problem as one expression, then follow BEDMAS.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
