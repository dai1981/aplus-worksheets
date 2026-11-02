# -*- coding: utf-8 -*-
"""
CA-ON Grade 8 Math: Order of operations with rational numbers (Ontario Curriculum 2020, Number B2.1, B2.3)
  python3 tools/gen_caon_math_g8_order_of_operations.py
BEDMAS with integers, fractions and decimals (positive and negative): the sign rules for × and ÷
at each step, subtracting a negative, brackets and exponents with negative and fractional bases
((−2)³ = −8, (−3)² = 9, (1/2)² = 1/4), mental math with 0.1, 0.01 and 0.001 (B2.3), and Ontario
multi-step problems with rational numbers, ratios, rates and percents written as one expression.

Expressions are written in a small source syntax ("~8 + 3 × 4" is −8 + 3 × 4, "~2^3" is (−2)³,
"3/4" is a fraction) and evaluated exactly with fractions.Fraction, cross-checked with Python
eval. Wrong answers come from real mistakes, computed by evaluating the expression the wrong way:
strictly left to right, + and − before × and ÷, × before ÷, ignoring brackets, multiplying the
base by the exponent, and sign errors ((−4) × (−5) = −20, 6 × (−2) = 12, 6 − (−2) = 4,
(−3)² = −9, (−2)³ = 8), plus stopping one step early. Powers-of-ten distractors move the decimal
point the wrong way or by the wrong number of places.
Helpers are adapted from gen_caon_math_g7_order_of_operations.py and
gen_cabc_math_g7_order_of_operations.py, rewritten for Ontario Grade 8.
Canadian English. 4-digit numbers have no separator; 5+ digits use a no-break space.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re, string
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-8")
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
    "ltr": [("^",), ("×", "÷", "+", "−")],             # strictly left to right
    "rev": [("^",), ("+", "−"), ("×", "÷")],           # + and − before × and ÷
    "mulfirst": [("^",), ("×",), ("÷",), ("+", "−")],  # × before ÷
}
# switched per set
ALLOW = {"neg": False, "dec": False, "frac": False, "dp": 3}


def mode(neg=False, dec=False, frac=False, dp=3):
    ALLOW.update(neg=neg, dec=dec, frac=frac, dp=dp)


# ------------------------------------------------------------ numbers
def group(n):
    s = str(n)
    if n < 10000:
        return s
    return "{:,}".format(n).replace(",", NB)


def nice(x):
    """Fraction mode: a small denominator. Otherwise a terminating decimal with at most dp places."""
    if x is None:
        return False
    x = Fraction(x)
    if ALLOW["frac"]:
        return x.denominator <= 27
    return (10 ** ALLOW["dp"]) % x.denominator == 0


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
            dp = ALLOW["dp"]
            s += "." + str(int((x - w) * 10 ** dp)).zfill(dp).rstrip("0")
    return (MINUS if neg else "") + s


def src(x):
    """Plain source text for a number (no grouping)."""
    x = Fraction(x)
    neg = "~" if x < 0 else ""
    x = abs(x)
    if x.denominator != 1 and ALLOW["frac"]:
        return neg + "%d/%d" % (x.numerator, x.denominator)
    return neg + fmt(x).replace(NB, "")


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
            nxt = ts[i + 1] if i + 1 < len(ts) else None
            wrap = False
            if t < 0 and len(ts) > 1 and prev not in (None, "("):
                wrap = True
            if nxt == "^" and (t < 0 or (ALLOW["frac"] and t.denominator != 1)):
                wrap = True
            if ALLOW["frac"] and t.denominator != 1 and abs(t) > 1 and (prev in ("×", "÷") or nxt in ("×", "÷")):
                wrap = True
            if wrap:
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
        n = int(b)
        if mode == "sq2":
            r = a * b
        elif mode == "negpow" and a < 0:
            r = -(a ** n)
        else:
            r = a ** n
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
    if op in ("×", "÷"):
        if mode == "negneg" and a < 0 and b < 0:
            r = -r
        if mode == "drop" and (a < 0) != (b < 0):
            r = -r
    if not ALLOW["neg"] and r < 0:
        return None
    return r


def flat_eval(seq, prec, mode):
    seq = list(seq)
    for level in prec:
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


def ev_tokens(ts, prec=STD, mode="std"):
    ts = list(ts)
    while True:
        j = next((k for k, t in enumerate(ts) if t == ")"), None)
        if j is None:
            return flat_eval(ts, prec, mode)
        i = max(k for k in range(j) if ts[k] == "(")
        v = flat_eval(ts[i + 1:j], prec, mode)
        if v is None:
            return None
        ts[i:j + 1] = [v]


def ev(s, mode="std"):
    ts = tokens(s)
    if mode in LEVELS:
        return ev_tokens(ts, LEVELS[mode])
    if mode == "noparen":
        return ev_tokens([t for t in ts if t not in ("(", ")")])
    if mode in ("std", "sq2", "negneg", "drop", "subneg", "negpow"):
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
    "noparen": "comes from ignoring the brackets",
    "sq2": "comes from multiplying the base by the exponent (an exponent means repeated multiplication)",
    "negneg": "comes from a sign error: two negatives multiplied or divided give a positive",
    "drop": "comes from a sign error: a negative and a positive multiplied or divided give a negative",
    "subneg": "comes from a sign error: subtracting a negative is the same as adding",
    "negpow": "comes from a sign error with the power: a negative base gives a positive result with an even exponent and a negative result with an odd exponent",
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
        if ALLOW["frac"] and w.denominator > 24:
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
            shown = dict(zip(names, map(fmt, d)))
            return t.format(**m), [(x.format(**m), why.format(**shown)) for x, why in extra]

        def ok(d, modes=modes, build=build):
            if len(set(d)) != len(d):
                return False
            s, ex_ = build(d)
            v = ev(s)
            if v is None or v == 0 or abs(v) > vmax or not nice(v):
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


# ------------------------------------------------------------ set 1: integers
def set_integers(rnd, used):
    mode(neg=True)
    R = rnd.randint
    T = [
        ("~{a} + {b} × {c}", ["ltr"], [("{a} + {b} × {c}", "drops the minus sign on −{a}")], lambda r: (R(6, 20), R(2, 9), R(2, 9))),
        ("{a} × ~{b} + {c}", ["drop"], [("{a} × ~{b} − {c}", "subtracts {c} instead of adding it")], lambda r: (R(2, 9), R(2, 9), R(2, 20))),
        ("~{a} × ~{b} − {c}", ["negneg"], [("~{a} × ~{b} + {c}", "adds {c} instead of subtracting it")], lambda r: (R(2, 9), R(2, 9), R(2, 20))),
        ("~{a} ÷ {b} + {c}", ["drop"], [("~{a} ÷ {b} − {c}", "subtracts {c} instead of adding it")], lambda r: (lambda b, q: (b * q, b, R(2, 12)))(R(2, 9), R(2, 9))),
        ("{a} − ~{b} × {c}", ["subneg", "ltr"], [], lambda r: (R(2, 15), R(2, 9), R(2, 6))),
        ("{a} + ~{b} × ~{c}", ["negneg", "ltr"], [], lambda r: (R(2, 20), R(2, 9), R(2, 9))),
        ("~{a} − {b} ÷ ~{c}", ["subneg", "drop", "ltr"], [], lambda r: (lambda c, q: (R(2, 20), c * q, c))(R(2, 9), R(2, 9))),
        ("~{a} × {b} − ~{c} × {d}", ["subneg", "ltr"], [], lambda r: (R(2, 9), R(2, 9), R(2, 9), R(2, 9))),
        ("{a} ÷ ~{b} × {c}", ["mulfirst", "drop"], [], lambda r: (lambda b, c, q: (b * c * q, b, c))(R(2, 6), R(2, 5), R(2, 5))),
        ("~{a} ÷ ~{b} − {c} × {d}", ["negneg", "ltr"], [], lambda r: (lambda b, q: (b * q, b, R(2, 9), R(2, 9)))(R(2, 9), R(2, 9))),
        ("{a} − {b} × ~{c} + {d}", ["subneg", "ltr"], [], lambda r: (R(2, 15), R(2, 9), R(2, 9), R(2, 15))),
        ("~{a} + {b} × ~{c} − {d}", ["drop", "ltr"], [], lambda r: (R(2, 20), R(2, 9), R(2, 9), R(2, 15))),
        ("~{a} ÷ {b} × ~{c}", ["mulfirst", "negneg"], [], lambda r: (lambda b, c, q: (b * c * q, b, c))(R(2, 5), R(2, 6), R(2, 4))),
        ("{a} ÷ ~{b} − {c} × ~{d}", ["drop", "subneg", "ltr"], [], lambda r: (lambda b, q: (b * q, b, R(2, 9), R(2, 9)))(R(2, 9), R(2, 9))),
        ("~{a} − ~{b} × ~{c}", ["negneg", "subneg", "ltr"], [], lambda r: (R(2, 20), R(2, 9), R(2, 9))),
        ("~{a} ÷ {b} × {c} + {d}", ["mulfirst", "drop", "rev"], [], lambda r: (lambda b, c, q: (b * c * q, b, c, R(2, 15)))(R(2, 5), R(2, 5), R(2, 4))),
        ("{a} + ~{b} ÷ {c} × ~{d}", ["mulfirst", "negneg", "rev"], [], lambda r: (lambda c, d, q: (R(2, 20), c * d * q, c, d))(R(2, 4), R(2, 4), R(1, 3))),
    ]
    its = templated(rnd, T, used, vmax=200)
    its.append(true_item("~2 × ~3 + 4", ["negneg"], [("~2 × ~3 − 4", "subtracts 4 instead of adding it"), ("2 × ~3 + 4", "drops the minus sign on −2")]))
    assert val("7 − ~3 × 2") == 13
    its.append(mcq("Which part of %s do you work out first?" % B(H("7 − ~3 × 2")), "(" + MINUS + "3) × 2",
                   ["7 " + MINUS + " (" + MINUS + "3)", "7 " + MINUS + " 3", "Either part"],
                   "%s. Multiply first: (" % chain("7 − ~3 × 2") + MINUS + "3) × 2 = " + MINUS + "6. Then subtracting "
                   + MINUS + "6 is the same as adding 6."))
    vals = {x: val(x) for x in ["6 − 2 × 5", "~4 × ~5", "~18 ÷ ~3", "~2 × ~3 × 2"]}
    assert vals["6 − 2 × 5"] == -4 and all(v > 0 for k, v in vals.items() if k != "6 − 2 × 5")
    its.append(mcq("Which expression has a <b>negative</b> value?", H("6 − 2 × 5"), [H("~4 × ~5"), H("~18 ÷ ~3"), H("~2 × ~3 × 2")],
                   "6 " + MINUS + " 2 × 5 = 6 " + MINUS + " 10 = " + MINUS + "4. The others are positive: (" + MINUS + "4) × (" + MINUS
                   + "5) = 20, (" + MINUS + "18) ÷ (" + MINUS + "3) = 6 and (" + MINUS + "2) × (" + MINUS + "3) × 2 = 6 × 2 = 12."))
    assert len(its) == 20, len(its)
    return {"title": "Integers: sign rules at each step", "items": its}


# ------------------------------------------------------------ set 2: fractions and decimals
def set_rational(rnd, used):
    R = rnd.randint
    mode(neg=True, dec=True)
    TD = [
        ("~{a} + {b} × {c}", ["ltr"], [("{a} + {b} × {c}", "drops the minus sign on −{a}")], lambda r: (dec1(R(11, 99)), dec1(R(11, 49)), R(2, 9))),
        ("{a} × ~{b} + {c}", ["drop"], [("{a} × ~{b} − {c}", "subtracts {c} instead of adding it")], lambda r: (R(2, 9), dec1(R(11, 49)), dec1(R(11, 99)))),
        ("~{a} × ~{b} − {c}", ["negneg"], [("~{a} × ~{b} + {c}", "adds {c} instead of subtracting it")], lambda r: (dec1(R(11, 49)), R(2, 9), dec1(R(11, 99)))),
        ("~{a} ÷ {b} − {c}", ["drop"], [("~{a} ÷ {b} + {c}", "adds {c} instead of subtracting it")], lambda r: (lambda b, q: (b * q, b, dec1(R(11, 49))))(R(2, 9), dec1(R(11, 39)))),
        ("{a} − ~{b} × {c}", ["subneg", "ltr"], [], lambda r: (dec1(R(11, 99)), dec1(R(11, 49)), R(2, 6))),
        ("~{a} + {b} ÷ ~{c}", ["drop", "ltr"], [], lambda r: (lambda c, q: (dec1(R(11, 99)), c * q, c))(R(2, 8), dec1(R(11, 39)))),
        ("{a} ÷ ~{b} × {c}", ["mulfirst", "drop"], [], lambda r: (lambda b, c, q: (b * c * q, b, c))(R(2, 5), R(2, 4), dec1(R(11, 29)))),
        ("~{a} × {b} + ~{c} × {d}", ["drop", "ltr"], [], lambda r: (dec1(R(11, 49)), R(2, 6), dec2(R(1, 3) * 100 + 25 * R(1, 3)), 4)),
    ]
    its = templated(rnd, TD, used, vmax=200)
    mode(neg=True, frac=True)
    F = Fraction
    small = [F(1, 2), F(1, 3), F(2, 3), F(1, 4), F(3, 4), F(1, 5), F(2, 5), F(3, 5), F(1, 6), F(5, 6), F(1, 8), F(3, 8)]
    pick = lambda: rnd.choice(small)
    TF = [
        ("{a} + ~{b} × {c}", ["ltr", "drop"], [], lambda r: (pick(), pick(), R(2, 6))),
        ("~{a} × ~{b} − {c}", ["negneg"], [("~{a} × ~{b} + {c}", "adds {c} instead of subtracting it")], lambda r: (pick(), R(2, 4) * 6, pick())),
        ("{a} − {b} ÷ ~{c}", ["subneg", "drop", "ltr"], [], lambda r: (pick(), pick(), pick())),
        ("~{a} ÷ {b} + {c}", ["drop", "rev"], [], lambda r: (pick(), pick(), pick())),
        ("~{a} − {b} × ~{c}", ["subneg", "ltr"], [], lambda r: (pick(), pick(), R(2, 6) * 2)),
        ("({a} − {b}) × ~{c}", ["negneg", "noparen"], [], lambda r: (pick(), R(1, 2), R(2, 4) * 6)),
        ("{a} × ~{b} + {c} ÷ ~{d}", ["drop", "ltr"], [], lambda r: (R(2, 4) * 4, pick(), pick(), pick())),
        ("~{a} ÷ ~{b} − {c}", ["negneg", "rev"], [], lambda r: (pick(), pick(), R(1, 3))),
        ("{a} − ~{b} + {c} × ~{d}", ["subneg", "drop", "ltr"], [], lambda r: (pick(), pick(), pick(), R(2, 4) * 2)),
    ]
    its += templated(rnd, TF, used, vmax=50, k0=1)
    s = "~3/4 + 1/4 × 6"
    assert val(s) == F(3, 4) and ev(s, "ltr") == -3
    its.append(true_item(s, ["ltr"], [("3/4 + 1/4 × 6", "drops the minus sign on −" + fr(3, 4)),
                                      ("~3/4 + 1/4 + 6", "adds instead of multiplying")]))
    mode(neg=True, dec=True)
    assert val("~2.5 × 4 + 1.5") == F(-17, 2)
    its.append(first_item("~2.5 × (4 + 1.5)", "4 + 1.5", [MINUS + "2.5 × 4", MINUS + "2.5 + 1.5", "Either part"],
                          "Brackets first, then multiply. Without brackets the answer would be " + fmt(F(-17, 2)) + "."))
    mode(neg=True, frac=True)
    s = "~1/2 × ~2/3 ÷ 1/3"
    assert val(s) == 1
    its.append(mcq("What is the value of %s?" % B(H(s)), "1", [MINUS + "1", fr(1, 9), MINUS + fr(1, 9)],
                   chain(s) + ". Two negatives multiplied give a positive. Dividing by " + fr(1, 3) + " is the same as multiplying by 3. "
                   "Not " + fr(1, 9) + ": that multiplies by " + fr(1, 3) + " instead of dividing."))
    assert ev("~1/2 × ~2/3 × 1/3") == F(1, 9)
    assert len(its) == 20, len(its)
    return {"title": "Fractions and decimals, positive and negative", "items": its}


# ------------------------------------------------------------ set 3: exponents and brackets
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


def set_powers(rnd, used):
    R = rnd.randint
    mode(neg=True)
    T = [
        ("~{a}^2 + {b}", ["negpow", "sq2"], [], lambda r: (R(3, 9), R(2, 20))),
        ("~{a}^3 + {b}", ["negpow", "sq2"], [], lambda r: (R(2, 4), R(2, 30))),
        ("{a} − ~{b}^2", ["negpow", "sq2"], [], lambda r: (R(2, 30), R(3, 9))),
        ("({a} − {b})^2", ["noparen", "negpow"], [("{a}^2 − {b}^2", "squares each number separately")], lambda r: (R(2, 6), R(8, 12))),
        ("~{a} × ({b} − {c})", ["negneg", "noparen"], [], lambda r: (R(2, 9), R(2, 6), R(8, 15))),
        ("({a} + ~{b}) × ~{c}", ["negneg", "noparen"], [], lambda r: (R(2, 6), R(8, 15), R(2, 9))),
        ("({a} − {b})^3 ÷ {c}", ["negpow", "noparen", "sq2"], [], lambda r: (lambda b, d: (b, b + d, d))(R(2, 9), R(2, 4))),
        ("{a} × ~{b}^2 − {c}", ["negpow", "sq2"], [], lambda r: (R(2, 5), R(2, 6), R(2, 20))),
        ("~{a} ÷ ({b} − {c}) + {d}", ["negneg", "noparen"], [],
         lambda r: (lambda d, q, b: (d * q, b, b + d, R(2, 15)))(R(2, 6), R(2, 6), R(1, 6))),
        ("{a} − {b} × ({c} − {d})^2", ["noparen", "ltr", "negpow"], [], lambda r: (R(2, 20), R(2, 5), R(1, 4), R(6, 9))),
        ("~{a}^2 − ~{b}^3", ["negpow", "sq2"], [], lambda r: (R(2, 6), R(2, 3))),
    ]
    its = templated(rnd, T, used, vmax=300)
    mode(neg=True, frac=True)
    F = Fraction
    small = [F(1, 2), F(1, 3), F(2, 3), F(1, 4), F(3, 4), F(2, 5), F(3, 5)]
    TF = [
        ("{a}^2 + {b}", ["sq2"], [("({a} + {b})^2", "adds before squaring")], lambda r: (rnd.choice(small), rnd.choice(small))),
        ("~{a}^3 × {b}", ["negpow", "sq2"], [], lambda r: rnd.choice([(F(1, 2), R(2, 5) * 8), (F(1, 3), 27), (F(1, 3), 54), (F(3, 2), 8 * R(1, 3))])),
        ("{a} − ~{b}^2", ["negpow", "sq2", "subneg"], [], lambda r: (R(1, 3), rnd.choice(small))),
    ]
    its += templated(rnd, TF, used, vmax=50, k0=1)
    mode(neg=True, dec=True)
    TD = [
        ("~{a}^2 × {b}", ["negpow", "sq2"], [], lambda r: (dec1(R(2, 9)), R(2, 9) * 10)),
        ("{a} − {b}^2", ["sq2"], [("({a} − {b})^2", "subtracts before squaring")], lambda r: (R(2, 9), dec1(R(2, 9)))),
    ]
    its += templated(rnd, TD, used, vmax=300, k0=2)
    mode(neg=True)
    its.append(brackets_item("~6 + 4 × 3 − 5", "(~6 + 4) × (3 − 5)", ["(~6 + 4) × 3 − 5", "~6 + 4 × (3 − 5)", "~6 + (4 × 3 − 5)"]))
    its.append(brackets_item("~2 × 3 + 5^2", "~2 × (3 + 5)^2", ["(~2 × 3 + 5)^2", "~2 × (3 + 5^2)", "(~2 × 3) + 5^2"]))
    assert len(its) == 18, len(its)
    s1 = ["~2^4", "~2^3", "~3^2", "~1^6"]
    v1 = [val(x) for x in s1]
    assert v1 == [16, -8, 9, 1]
    its.append(mcq("Which power has a <b>negative</b> value?", H("~2^3"), [H("~2^4"), H("~3^2"), H("~1^6")],
                   "(" + MINUS + "2)³ = (" + MINUS + "2) × (" + MINUS + "2) × (" + MINUS + "2) = " + MINUS + "8. An odd number of negative factors gives a negative. "
                   "The others have an even exponent, so they are positive: (" + MINUS + "2)⁴ = 16, (" + MINUS + "3)² = 9 and (" + MINUS + "1)⁶ = 1."))
    mode(dec=True, dp=4)
    assert Fraction("0.4") ** 2 == Fraction("0.16")
    its.append(mcq("What is the value of %s?" % B("0.4²"), "0.16", ["0.8", "1.6", "0.016"],
                   "0.4² = 0.4 × 0.4 = 0.16. Tenths × tenths gives hundredths, so the answer has 2 decimal places. "
                   "Not 0.8: that multiplies 0.4 by the exponent 2. Not 1.6 or 0.016: they put the decimal point in the wrong place."))
    assert len(its) == 20, len(its)
    return {"title": "Exponents and brackets", "items": its}


# ------------------------------------------------------------ set 4: mental math with 0.1, 0.01, 0.001
PT = {1: "0.1", 2: "0.01", 3: "0.001"}
TEN = {1: "10", 2: "100", 3: "1000"}
PLACES = {k: "%d place%s" % (k, "" if k == 1 else "s") for k in range(6)}


def shift(n, op, k):
    """n × 10^-k or n ÷ 10^-k."""
    m = Fraction(1, 10 ** k)
    return n * m if op == "×" else n / m


def ok_num(x):
    return x is not None and x > 0 and nice(x) and x < 10 ** 6


def shift_item(n, op, k):
    v = shift(n, op, k)
    other = "÷" if op == "×" else "×"
    left = op == "×"
    cands = [(shift(n, other, k), "moves the decimal point the wrong way"),
             (shift(n, op, k + 1), "moves the decimal point %s, one too many" % PLACES[k + 1]),
             (shift(n, op, k - 1) if k > 1 else None, "moves the decimal point %s, one too few" % PLACES[k - 1]),
             (shift(n, other, k + 1), "moves the decimal point the wrong way and %s" % PLACES[k + 1]),
             (shift(n, op, k + 2), "moves the decimal point %s" % PLACES[k + 2])]
    cands = [(w, why) for w, why in cands if ok_num(w) and w != v]
    assert ok_num(v) and len(cands) >= 3, (n, op, k)
    same = "÷ " + TEN[k] if op == "×" else "× " + TEN[k]
    e = "%s %s is the same as %s, so move the decimal point %s to the %s: %s %s %s = %s. " % (
        op, PT[k], same, PLACES[k], "left" if left else "right", fmt(n), op, PT[k], fmt(v))
    e += " ".join("Not %s: that %s." % (fmt(w), why) for w, why in cands[:2])
    return mcq("Use mental math to find %s." % B("%s %s %s" % (fmt(n), op, PT[k])), fmt(v), [fmt(w) for w, _ in cands], e)


def set_powers_of_ten(rnd, used):
    mode(dec=True, dp=4)
    its = []
    F = Fraction
    combos = [("×", 1), ("×", 2), ("×", 3), ("÷", 1), ("÷", 2), ("÷", 3)] * 2
    whole = [45, 38, 72, 260, 507, 6, 93, 125, 840, 19, 64, 350]
    decs = [F("3.6"), F("8.2"), F("0.7"), F("12.5"), F("4.25"), F("0.9"), F("26.4"), F("1.8"), F("7.05"), F("0.35")]
    rnd.shuffle(whole)
    rnd.shuffle(decs)
    for i, (op, k) in enumerate(combos):
        pool = whole if i % 2 == 0 else decs
        for _ in range(len(pool)):
            n = pool.pop()
            try:
                it = shift_item(n, op, k)
            except AssertionError:
                pool.insert(0, n)
                continue
            break
        its.append(it)
    # what is it the same as
    its.append(mcq("Multiplying by 0.01 is the same as …", "dividing by 100", ["multiplying by 100", "dividing by 10", "dividing by 1000"],
                   "0.01 = " + fr(1, 100) + ", so × 0.01 means finding one hundredth: the same as ÷ 100. For example, 45 × 0.01 = 45 ÷ 100 = 0.45."))
    its.append(mcq("Dividing by 0.001 is the same as …", "multiplying by 1000", ["dividing by 1000", "multiplying by 100", "dividing by 100"],
                   "There are 1000 thousandths in 1, so ÷ 0.001 is the same as × 1000. For example, 0.6 ÷ 0.001 = 600. "
                   "Dividing by a number less than 1 makes the answer greater."))
    # missing numbers
    its.append(mcq("What number goes in the box?<br>%s" % B("52 × □ = 0.52"), "0.01", ["0.1", "0.001", "100"],
                   "The decimal point moved 2 places left, so 52 was divided by 100. That is the same as × 0.01. "
                   "Check: 52 × 0.1 = 5.2 and 52 × 0.001 = 0.052."))
    its.append(mcq("What number goes in the box?<br>%s" % B("7.4 ÷ □ = 740"), "0.01", ["0.1", "100", "0.001"],
                   "The decimal point moved 2 places right, so 7.4 was multiplied by 100. That is the same as ÷ 0.01. "
                   "Not 100: 7.4 ÷ 100 = 0.074."))
    vals = {"30 × 0.1": F(3), "30 ÷ 0.1": F(300), "30 × 0.01": F("0.3"), "30 ÷ 0.01": F(3000)}
    assert vals["30 ÷ 0.01"] == max(vals.values())
    its.append(mcq("Which expression has the <b>greatest</b> value?", "30 ÷ 0.01", ["30 × 0.1", "30 ÷ 0.1", "30 × 0.01"],
                   "30 ÷ 0.01 = 30 × 100 = 3000. The others: 30 × 0.1 = 3, 30 ÷ 0.1 = 300 and 30 × 0.01 = 0.3. "
                   "Dividing by a small decimal gives a large answer."))
    # order of operations with powers of ten
    R = rnd.randint
    T = [
        ("{a} + {b} × 0.1", ["ltr"], [("{a} + {b} ÷ 0.1", "divides by 0.1 instead of multiplying")], lambda r: (R(3, 20), R(21, 99) * 10 + R(1, 9))),
        ("{b} + {a} ÷ 0.01", ["ltr"], [("{b} + {a} × 0.01", "multiplies by 0.01 instead of dividing"), ("{b} + {a} ÷ 0.1", "moves the decimal point only 1 place")],
         lambda r: (dec1(R(21, 89)), R(20, 150))),
        ("{a} × 0.001 + {b} × 0.01", ["ltr"], [("{a} × 0.01 + {b} × 0.001", "swaps 0.001 and 0.01"), ("{a} ÷ 0.001 + {b} ÷ 0.01", "divides instead of multiplying")],
         lambda r: (R(1, 9) * 1000 + R(1, 9) * 100, R(11, 99))),
    ]
    its += templated(rnd, T, used, vmax=10000)
    assert len(its) == 20, len(its)
    return {"title": "Mental math with 0.1, 0.01 and 0.001", "items": its}


# ------------------------------------------------------------ set 5: word problems
def unit(sfx, pos=False, whole=False):
    def f(v):
        if pos and v <= 0:
            return None
        if whole and (v.denominator != 1 or v <= 1):
            return None
        return fmt(v) + sfx
    return f


UNITS = {
    "$": money,
    "°C": unit("°C"),
    "m": unit(" m"),
    "km": unit(" km", pos=True),
    "L": unit(" L", pos=True),
    "cups": unit(" cups", pos=True),
    "points": unit(" points"),
    "students": unit(" students", whole=True),
}


def set_words(rnd, used):
    its = []

    def wp(text, s, u_, modes, extra=(), note=""):
        v = val(s)
        u = UNITS[u_]
        ans = u(v)
        assert ans, (s, v)
        ms = [(w, why) for w, why in mistakes(s, modes, extra) if u(w)]
        assert len(ms) >= 3, (s, ms)
        e = "One expression: %s, so %s. %s%s" % (chain(s), ans, (note + " " if note else ""), why_text(ms, u, 3))
        its.append(mcq(text, ans, [u(w) for w, _ in ms[:3]], e))

    def which(text, good, bads, tail):
        val(good)
        for b in bads:
            assert ev(b) != ev(good), b
        its.append(mcq(text, H(good), [H(b) for b in bads], "%s. %s" % (chain(good), tail)))

    mode(neg=True, dec=True)
    wp("At 6:00 a.m. the temperature in Iqaluit is −18°C. It rises 2.5°C every hour for 4 hours. What is the temperature at 10:00 a.m.?",
       "~18 + 4 × 2.5", "°C", ["ltr"], [("18 + 4 × 2.5", "drops the minus sign on −18"), ("4 × 2.5", "forgets the starting temperature")])
    wp("Liam has $35 on his transit card. Each school day he takes 2 bus rides at $3.30 each. How much is left on the card after 5 school days?",
       "35 − 5 × 2 × 3.3", "$", [], [("35 − 5 × 3.3", "counts only one ride a day"), ("35 − 2 × 3.3", "counts only one day")])
    wp("A pair of skates costs $180. They are on sale for 30% off. Ava also buys skate guards for $14. How much does she pay before tax?",
       "180 − 0.3 × 180 + 14", "$", [], [("0.3 × 180 + 14", "pays only the $54 discount plus the guards"),
                                          ("180 − 30 + 14", "takes off $30 instead of 30%")])
    wp("A family drives about 200 km from Ottawa to Montréal. Their car uses 6.8 L of gas for every 100 km. How much gas do they use?",
       "200 ÷ 100 × 6.8", "L", ["mulfirst"], [("200 ÷ 100 + 6.8", "adds the rate instead of multiplying"),
                                             ("200 × 6.8", "forgets that the rate is for every 100 km")])
    wp("A diver in Lake Superior is at −24 m (24 m below the surface). She rises 1.5 m every minute for 6 minutes, then sinks 4 m. Where is she now?",
       "~24 + 6 × 1.5 − 4", "m", ["ltr"], [("24 + 6 × 1.5 − 4", "forgets that −24 m is below the surface"),
                                         ("~24 − 6 × 1.5 − 4", "subtracts the rises instead of adding them")])
    wp("A math contest gives 4 points for a correct answer and −1 point for a wrong answer. Kai gets 18 correct and 5 wrong. What is his score?",
       "18 × 4 + 5 × ~1", "points", ["drop", "ltr"], [("18 × 4", "leaves out the wrong answers")])
    wp("Sofia buys 4 movie tickets at $13.50 each and 2 popcorns at $8.25 each. She pays part of it with a $25 gift card. How much more does she pay?",
       "4 × 13.5 + 2 × 8.25 − 25", "$", [], [("4 × 13.5 + 2 × 8.25", "forgets the gift card"), ("4 × 13.5 + 2 × 8.25 + 25", "adds the gift card instead of taking it away"),
                                                 ("4 × 13.5 + 8.25 − 25", "pays for only one popcorn")])
    wp("In Ontario, milk is sold in jugs and bags. A 2 L jug costs $4.80 and a 4 L bag costs $6.20. How much more does the jug cost per litre?",
       "4.8 ÷ 2 − 6.2 ÷ 4", "$", ["ltr"], [("6.2 − 4.8", "compares the prices, not the prices per litre"),
                                         ("4.8 − 6.2 ÷ 4", "forgets to divide the jug price by 2")])
    wp("A school has 640 students. Next year the number grows by 5%, then 12 students move away. How many students are there then?",
       "640 + 0.05 × 640 − 12", "students", [], [("640 + 5 − 12", "adds 5 instead of 5%"),
                                                 ("0.05 × 640 − 12", "finds only the change, not the new total")])
    wp("Amira has $45 in her bank account. She takes out $12 three times, then puts in $20. How much is in the account now?",
       "45 − 3 × 12 + 20", "$", ["ltr"], [("45 − 12 + 20", "takes out $12 only once")])
    mode(neg=True, dec=True)
    wp("A punch recipe mixes juice and sparkling water in the ratio 3 : 2. Chloe makes 4 L of punch for the class party. How much juice does she need?",
       "4 ÷ (3 + 2) × 3", "L", [], [("4 ÷ (3 + 2) × 2", "finds the sparkling water"),
                                     ("4 ÷ 2 × 3", "divides by 2 instead of by the 5 parts")])
    wp("Ethan cycles 18.6 km in 1.5 hours. At the same speed, how far does he cycle in 2.5 hours?",
       "18.6 ÷ 1.5 × 2.5", "km", ["mulfirst"], [("18.6 ÷ 2.5 × 1.5", "swaps the two times")])
    mode(neg=True, frac=True)
    wp("Hana has 5 cups of flour. She makes 3 batches of bannock, and each batch uses 1 " + fr(1, 4) + " cups. How much flour is left?",
       "5 − 3 × 5/4", "cups", ["ltr"], [("5 − 5/4", "uses flour for only one batch"),
                                       ("5 − 3 × 1/4", "uses only the " + fr(1, 4) + " cup of each batch, not 1 " + fr(1, 4) + " cups")])
    wp("A canoe route in Algonquin Park is 24 km long. A group paddles " + fr(3, 8) + " of the route on Day 1 and " + fr(1, 3) + " of it on Day 2. How many kilometres are left?",
       "24 − (3/8 + 1/3) × 24", "km", ["noparen"], [("(3/8 + 1/3) × 24", "finds the distance paddled, not the distance left"),
                                                    ("24 − 3/8 × 24", "forgets Day 2")])
    mode(neg=True)
    wp("The low temperatures in Winnipeg for five days are −12°C, −8°C, −15°C, −5°C and −10°C. What is the mean low temperature?",
       "(~12 + ~8 + ~15 + ~5 + ~10) ÷ 5", "°C", ["noparen"], [("(12 + 8 + 15 + 5 + 10) ÷ 5", "drops the minus signs")])
    mode(neg=True, dec=True)
    wp("A campsite at an Ontario provincial park costs $48.50 a night, plus a one-time $12 booking fee. Two families share the site for 3 nights and split the total cost equally. How much does each family pay?",
       "(3 × 48.5 + 12) ÷ 2", "$", ["noparen"], [("3 × 48.5 + 12", "forgets to split between the 2 families"),
                                                ("(3 × 48.5 + 3 × 12) ÷ 2", "pays the booking fee every night")])
    which("A taxi charges $4.25 plus $1.95 for each kilometre. Which expression gives the cost of a 6 km ride?",
          "4.25 + 6 × 1.95", ["(4.25 + 1.95) × 6", "4.25 × 6 + 1.95", "6 + 4.25 × 1.95"],
          "So the ride costs $15.95. (4.25 + 1.95) × 6 would charge the $4.25 start fee 6 times.")
    which("At 5:00 p.m. the temperature in Sudbury is 2°C. It drops 1.5°C every hour for 4 hours. Which expression gives the new temperature?",
          "2 − 4 × 1.5", ["(2 − 4) × 1.5", "4 × 1.5 − 2", "2 − 4 − 1.5"],
          "So the new temperature is " + MINUS + "4°C. (2 " + MINUS + " 4) × 1.5 subtracts before multiplying. 4 × 1.5 " + MINUS + " 2 subtracts in the wrong order and gives 4°C.")
    which("Maya mixes blue and white paint in the ratio 2 : 5. She needs 21 L of paint in all. Which expression gives the litres of white paint?",
          "21 ÷ (2 + 5) × 5", ["21 ÷ (2 + 5) × 2", "21 ÷ 2 × 5", "21 × 5 ÷ 2"],
          "So she needs 15 L of white paint. 21 ÷ (2 + 5) × 2 gives the blue paint (6 L). Divide by all 7 parts, not by 2.")
    which("A $60 hoodie is on sale for 25% off. Which expression gives the sale price before tax?",
          "60 − 0.25 × 60", ["(60 − 0.25) × 60", "60 − 25", "0.25 × 60"],
          "So the sale price is $45. 0.25 × 60 = 15 is only the discount, and 60 " + MINUS + " 25 takes off $25 instead of 25%.")
    assert len(its) == 20, len(its)
    return {"title": "Multi-step problems with rational numbers", "items": its}


# ------------------------------------------------------------ lesson
def steps_svg(rows, label, W=360):
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


def shift_svg():
    """Place-value chart: 45 × 0.01 = 0.45, digits move 2 places to the right (the point moves 2 places left)."""
    heads = ["tens", "ones", "tenths", "hundredths"]
    cw, ch = 96, 44
    x0, y0 = 20, 30
    rows = [["4", "5", "", ""], ["", "0", "4", "5"]]
    out = []
    for i, h in enumerate(heads):
        out.append("<text x='%d' y='%d' font-size='14' fill='%s' text-anchor='middle'>%s</text>" % (x0 + i * cw + cw // 2, y0 - 10, INK, h))
    for r, row in enumerate(rows):
        y = y0 + r * (ch + 40)
        for i, d in enumerate(row):
            out.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                       % (x0 + i * cw, y, cw, ch, FILL if i < 2 else "#e8f1fa", GREEN))
            if d:
                out.append("<text x='%d' y='%d' font-size='24' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                           % (x0 + i * cw + cw // 2, y + 31, GREEN if r else INK, d))
        # decimal point between ones and tenths
        out.append("<circle cx='%d' cy='%d' r='4' fill='%s'/>" % (x0 + 2 * cw, y + ch - 6, RED))
        out.append("<text x='%d' y='%d' font-size='16' font-weight='700' fill='%s'>%s</text>"
                   % (x0 + 4 * cw + 12, y + 28, INK, "45" if r == 0 else "0.45"))
    out.append("<defs><marker id='sa' viewBox='0 0 10 10' refX='8' refY='5' markerWidth='6' markerHeight='6' orient='auto'>"
               "<path d='M0 0 L10 5 L0 10 z' fill='%s'/></marker></defs>" % BLUE)
    for i in (0, 1):
        xa = x0 + i * cw + cw // 2
        out.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2' marker-end='url(#sa)'/>"
                   % (xa + 6, y0 + ch + 6, xa + 2 * cw - 10, y0 + ch + 34, BLUE))
    out.append("<text x='%d' y='%d' font-size='15' font-weight='700' fill='%s'>× 0.01</text>" % (x0 + 4 * cw + 12, y0 + ch + 26, BLUE))
    W = x0 + 4 * cw + 80
    Hh = y0 + 2 * ch + 40 + 8
    return svg_wrap(W, Hh, "".join(out), "place value chart: 45 times 0.01 is 0.45, each digit moves 2 places to the right")


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    M = MINUS
    mode(neg=True, dec=True)
    assert val("~4 + 6 × ~2") == -16 and ev("~4 + 6 × ~2", "ltr") == -4
    assert val("8 − ~1.5 × 4") == 14 and ev("8 − ~1.5 × 4", "subneg") == 2
    assert val("(3 − 5)^3 + 10") == 2 and ev("(3 − 5)^3 + 10", "negpow") == 18
    assert val("4.8 ÷ 2 − 6.2 ÷ 4") == Fraction("0.85")
    fig1 = steps_svg([([M + "4 + ", ("6 × (" + M + "2)", RED)], "multiply first"),
                      ([(M + "4 + (" + M + "12)", RED)], "then add"),
                      ([(M + "16", GREEN)], "")], "working out negative 4 plus 6 times negative 2 step by step: the answer is negative 16")
    ex_dec = chain("8 − ~1.5 × 4")
    ex_pow = chain("(3 − 5)^3 + 10")
    ex_word = chain("4.8 ÷ 2 − 6.2 ÷ 4")
    mode(neg=True, frac=True)
    ex_frac = chain("~3/4 + 1/4 × 6")
    assert ev("~3/4 + 1/4 × 6", "ltr") == -3
    mode(neg=True, dec=True)
    return (
        "<h2>The same order for every kind of number</h2>"
        "<p>In Grade 8 the numbers can be integers, fractions or decimals, positive or negative. "
        "These are all <b>rational numbers</b>. The <b>order of operations</b> does not change: it is still <b>BEDMAS</b>.</p>"
        "<figure class='sn-fig'>" + bedmas_svg() +
        "<figcaption>Brackets, then exponents, then ÷ and × from left to right, then + and − from left to right.</figcaption></figure>"
        "<p>÷ and × have the same rank, so do whichever comes first from the left. The same is true for + and −.</p>"
        "<h2>Use the sign rules at each step</h2>"
        "<p>Follow BEDMAS, and use the integer sign rules every time you multiply or divide.</p>" +
        table(["Signs", "Result", "Example"], [
            ["positive and positive", "positive", "3 × 4 = 12"],
            ["negative and negative", "positive", "(" + M + "3) × (" + M + "4) = 12"],
            ["positive and negative", "negative", "3 × (" + M + "4) = " + M + "12"],
            ["subtract a negative", "add", "8 " + M + " (" + M + "6) = 8 + 6 = 14"],
        ]) +
        "<figure class='sn-fig'>" + fig1 +
        "<figcaption>" + M + "4 + 6 × (" + M + "2) = " + M + "16, not " + M + "4. Multiply before you add.</figcaption></figure>" +
        ex("A decimal and subtracting a negative", "Evaluate 8 " + M + " (" + M + "1.5) × 4.",
           ex_dec + ". Subtracting " + M + "6 is the same as adding 6.", "14") +
        ex("Fractions", "Evaluate " + M + fr(3, 4) + " + " + fr(1, 4) + " × 6.",
           ex_frac + ". Not " + M + "3: that adds first.", fr(3, 4)) +
        "<h2>Exponents with negative bases</h2>"
        "<p>An exponent means repeated multiplication of the base. A negative base in brackets gives a positive result "
        "with an even exponent and a negative result with an odd exponent: (" + M + "3)² = 9, but (" + M + "2)³ = " + M + "8.</p>" +
        ex("Brackets, then the exponent", "Evaluate (3 " + M + " 5)³ + 10.", ex_pow + ". Not 18: (" + M + "2)³ is negative.", "2") +
        "<h2>Mental math with 0.1, 0.01 and 0.001</h2>"
        "<p>Multiplying by 0.1, 0.01 or 0.001 is the same as dividing by 10, 100 or 1000. "
        "Dividing by 0.1, 0.01 or 0.001 is the same as multiplying by 10, 100 or 1000. "
        "The number of zeros tells you how many places the digits move.</p>"
        "<figure class='sn-fig'>" + shift_svg() +
        "<figcaption>45 × 0.01 = 45 ÷ 100 = 0.45. Each digit moves 2 places to the right.</figcaption></figure>" +
        table(["Operation", "Same as", "Example"], [
            ["× 0.1", "÷ 10", "38 × 0.1 = 3.8"],
            ["× 0.01", "÷ 100", "38 × 0.01 = 0.38"],
            ["× 0.001", "÷ 1000", "38 × 0.001 = 0.038"],
            ["÷ 0.1", "× 10", "3.8 ÷ 0.1 = 38"],
            ["÷ 0.01", "× 100", "3.8 ÷ 0.01 = 380"],
            ["÷ 0.001", "× 1000", "3.8 ÷ 0.001 = 3800"],
        ]) +
        "<h2>Multi-step problems as one expression</h2>"
        "<p>Write the whole problem as one expression, then use BEDMAS. Use brackets when a sum must be found before you multiply or divide.</p>" +
        ex("Price per litre", "A 2 L jug of milk costs $4.80 and a 4 L bag costs $6.20. How much more does the jug cost per litre?",
           "One expression: " + ex_word + ".", "$0.85, or 85¢") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            [M + "4 + 6 × (" + M + "2) = 2 × (" + M + "2) = " + M + "4", "Multiply first: " + M + "4 + (" + M + "12) = " + M + "16"],
            ["(" + M + "4) × (" + M + "5) = " + M + "20", "Two negatives give a positive: 20"],
            ["8 " + M + " (" + M + "6) = 2", "Subtracting a negative means adding: 8 + 6 = 14"],
            ["(" + M + "3)² = " + M + "6", "(" + M + "3) × (" + M + "3) = 9"],
            ["(" + M + "2)³ = 8", "Three negative factors give a negative: " + M + "8"],
            ["45 × 0.01 = 4500", "× 0.01 makes the number smaller: 0.45"],
        ])
    )


FAQ = [
    {"q": "How do you use BEDMAS with negative numbers?",
     "a": "Use the same order (brackets, exponents, ÷ and × left to right, then + and − left to right) and apply the sign rules at each step. "
          "For example, −4 + 6 × (−2) = −4 + (−12) = −16."},
    {"q": "Is (−3)² the same as −3²?",
     "a": "No. (−3)² = (−3) × (−3) = 9, but −3² means −(3 × 3) = −9 because the exponent is done before the minus sign. Write the brackets when you mean a negative base."},
    {"q": "How do you multiply and divide by 0.1, 0.01 and 0.001 in your head?",
     "a": "Multiplying by 0.1, 0.01 or 0.001 is the same as dividing by 10, 100 or 1000, so the number gets smaller. "
          "Dividing by them is the same as multiplying by 10, 100 or 1000, so 2.5 ÷ 0.01 = 250."},
    {"q": "Where is order of operations in the Ontario Grade 8 math curriculum?",
     "a": "It is in the Number strand. Expectation B2.1 uses the properties and order of operations to solve problems with rational numbers, ratios, rates and percents, "
          "and B2.3 covers mental math with 0.1, 0.01 and 0.001."},
]


def gen():
    rnd = random.Random(48807)
    used = set()
    sets = [set_integers(rnd, used), set_rational(rnd, used), set_powers(rnd, used),
            set_powers_of_ten(rnd, used), set_words(rnd, used)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-8", "slug": "order-of-operations-with-rational-numbers", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Order of Operations with Rational Numbers",
        "seo_title": "Grade 8 Order of Operations Worksheets: Free BEDMAS with Integers, Fractions and Decimals, Answer Key (Ontario Curriculum)",
        "short_title": "Order of Operations",
        "domain": "Number",
        "standard_code": "Grade 8: B2.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use the properties and order of operations, and the relationships between operations, to solve problems involving rational numbers, ratios, rates, and percents, including those requiring multiple steps or multiple operations",
        "meta_desc": "Free Grade 8 math worksheets on the order of operations (BEDMAS) with rational numbers, matched to the Ontario curriculum: "
                     "integer sign rules, fractions and decimals, exponents and brackets, mental math with 0.1, 0.01 and 0.001, and multi-step problems. 100 questions with an answer key.",
        "key_big": "BEDMAS works the same for integers, fractions and decimals. Use the sign rules at each step.",
        "key_sub": "−4 + 6 × (−2) = −4 + (−12) = −16. (−2)³ = −8 but (−3)² = 9. × 0.01 is the same as ÷ 100, and ÷ 0.01 is the same as × 100.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
