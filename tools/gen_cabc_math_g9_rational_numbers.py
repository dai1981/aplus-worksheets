# -*- coding: utf-8 -*-
"""
BC Grade 9 Math: Operations with Rational Numbers
(BC Mathematics Curriculum, Mathematics 9: Computational fluency — operations with rational numbers:
addition, subtraction, multiplication, division and order of operations)
  python3 tools/gen_cabc_math_g9_rational_numbers.py
Sets: compare and order rational numbers; add and subtract negative fractions and decimals;
multiply and divide; order of operations (BEDMAS); BC word problems with temperatures and money.

Expressions are written in a small source syntax ("~8 + 3 × 4" is −8 + 3 × 4, "~2^3" is (−2)³,
"3/4" is a fraction) and evaluated exactly with fractions.Fraction, cross-checked with Python eval.
Wrong answers come from real mistakes: sign errors (two negatives multiplied give a negative,
subtracting a negative as if it were positive, the wrong sign on a sum), adding the sizes when the
signs differ, adding numerators and denominators, lining up the last digits instead of the decimal
points, flipping the first fraction instead of the divisor, not flipping at all, working strictly
left to right, ignoring brackets. No wrong choice is equal in value to the answer or to another choice.
The expression engine is adapted from gen_caon_math_g8_order_of_operations.py, rewritten for BC Grade 9.
Canadian English. 4-digit numbers have no separator; 5+ digits use a no-break space.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re, string
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-9")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
BLUE = "#2f6fb0"
FILL = "#cfe6d6"
FONT = "Arial, Helvetica, sans-serif"
NB = "\u00a0"
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
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


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



def sfr(n, d):
    """A signed fraction n/d exactly as written (not simplified)."""
    return (MINUS if n < 0 else "") + fr(abs(n), d)


def P(x):
    """A value written in brackets when it is negative (for the middle of a sum)."""
    s = fmt(x)
    return "(" + s + ")" if x < 0 else s


def mark_large(svg):
    return svg.replace("<svg ", "<svg data-pf='lg' ", 1)


def pick3(v, cands, ok=lambda w: True):
    """The first 3 distinct wrong values (with reasons) that are nice, non-zero and not v."""
    out, seen = [], {v}
    for w, why in cands:
        if w is None:
            continue
        w = Fraction(w)
        if w in seen or w == 0 or not nice(w) or not ok(w):
            continue
        if ALLOW["frac"] and w.denominator > 24:
            continue
        seen.add(w)
        out.append((w, why))
        if len(out) == 3:
            break
    assert len(out) == 3, (v, cands, out)
    return out


def nots(ms, show=fmt):
    return " ".join("Not %s: that %s." % (show(w), why) for w, why in ms)


# ------------------------------------------------------------ set 1: compare and order
def Q(s):
    """'~1 1/4' or '~3/4' or '~0.65' → (html, value), written exactly as given."""
    neg = s.startswith("~")
    t = s.lstrip("~")
    if " " in t:
        w, f = t.split(" ")
        n, d = map(int, f.split("/"))
        v = int(w) + Fraction(n, d)
        h = w + " " + fr(n, d)
    elif "/" in t:
        n, d = map(int, t.split("/"))
        v = Fraction(n, d)
        h = fr(n, d)
    else:
        v = Fraction(t)
        h = t
    return ((MINUS if neg else "") + h, -v if neg else v)


def dec_of(v):
    """A short decimal for an explanation: exact if it ends within 3 places, else about 2 places."""
    if (1000 % v.denominator) == 0:
        s = ("%.3f" % abs(v)).rstrip("0").rstrip(".")
        return "= " + (MINUS if v < 0 else "") + s
    s = "%.2f" % abs(float(v))
    return "≈ " + (MINUS if v < 0 else "") + s


def set_compare(rnd, used):
    mode(neg=True, frac=True)
    its = []
    groups = [
        (["~3/4", "~2/3", "~5/6", "~1/2"], "greatest"),
        (["~0.7", "~0.65", "~0.71", "~0.6"], "least"),
        (["~1 1/4", "~1.3", "~1 1/5", "~1.15"], "greatest"),
        (["2/5", "~0.5", "~3/8", "0.35"], "least"),
        (["~7/4", "~1.8", "~1 2/3", "~1.7"], "least"),
        (["~0.09", "~0.1", "~0.089", "~0.11"], "greatest"),
    ]
    for nums, which in groups:
        q = [Q(s) for s in nums]
        assert len({v for _, v in q}) == 4
        order = sorted(q, key=lambda t: t[1])
        good = order[-1] if which == "greatest" else order[0]
        listing = ", ".join("%s (%s)" % (h, dec_of(v)) if "fr" in h else h for h, v in order)
        tip = ("On a number line, the greatest number is farthest to the right. For negative numbers, the one closer to 0 is greater."
               if which == "greatest" else
               "On a number line, the least number is farthest to the left. For negative numbers, the one farther from 0 is less.")
        e = "From least to greatest: %s. %s" % (listing, tip)
        its.append(mcq("Which number is the <b>%s</b>?" % which, good[0], [h for h, _ in q if h != good[0]], e))

    # which statement is true
    stmts = [
        [("~2/3", "~3/4"), ("~0.4", "~0.35"), ("~5/8", "~0.6"), ("1/3", "~1/2")],
        [("~1.25", "~1 1/3"), ("~0.8", "~0.85"), ("~2/5", "~0.45"), ("~0.3", "~1/3")],
        [("~4/3", "~1.3"), ("~0.25", "~1/5"), ("~0.06", "~0.6"), ("~3/10", "~0.33")],
    ]
    for pairs in stmts:
        rows = []
        for a, b in pairs:
            (ha, va), (hb, vb) = Q(a), Q(b)
            assert va != vb
            rows.append((ha, va, hb, vb))
        # the first statement is written true, the others false
        out = []
        for i, (ha, va, hb, vb) in enumerate(rows):
            true_sign = "&lt;" if va < vb else "&gt;"
            false_sign = "&gt;" if va < vb else "&lt;"
            out.append("%s %s %s" % (ha, true_sign if i == 0 else false_sign, hb))
        ha, va, hb, vb = rows[0]
        dd = lambda h, v: "%s %s" % (h, dec_of(v)) if "fr" in h else h
        e = "%s and %s, so %s. " % (dd(ha, va), dd(hb, vb), out[0]) if ("fr" in ha or "fr" in hb) else "%s. " % out[0]
        e += "Each of the other statements has the sign the wrong way round. For negative numbers, the number closer to 0 is greater."
        its.append(mcq("Which statement is true?", out[0], out[1:], e))

    # order from least to greatest
    orders = [["~0.6", "~2/3", "~0.65"], ["~1 1/2", "~1.45", "~1 3/5"], ["~3/8", "0.3", "~1/4"]]
    for nums in orders:
        q = [Q(s) for s in nums]
        good = sorted(q, key=lambda t: t[1])
        by_size = sorted(q, key=lambda t: abs(t[1]))
        bad = [list(reversed(good)), by_size, [good[1], good[0], good[2]], [good[0], good[2], good[1]]]
        sh = lambda L: ", ".join(h for h, _ in L)
        listing = ", ".join("%s (%s)" % (h, dec_of(v)) if "fr" in h else h for h, v in good)
        e = ("Least to greatest: %s. The number farthest from 0 on the negative side is the least. "
             "Ordering by size and ignoring the minus signs puts the negative numbers backwards." % listing)
        its.append(mcq("Order from <b>least</b> to <b>greatest</b>.", sh(good), [sh(b) for b in bad if sh(b) != sh(good)], e))

    # number lines
    lines = [
        (Fraction(-2), Fraction(1), Fraction(1, 4), Fraction(-5, 4),
         [("~3/4", "counts 1 tick to the right of −1 instead of to the left"),
          ("1 1/4", "drops the minus sign"),
          ("~1.1", "reads each tick as one tenth, but there are 4 ticks in each whole")]),
        (Fraction(-1), Fraction(1), Fraction(1, 10), Fraction(-7, 10),
         [("~0.3", "counts the 3 ticks from −1, but P is 7 tenths to the left of 0"),
          ("0.7", "drops the minus sign"),
          ("~1.3", "counts 3 tenths to the left of −1 instead of to the right")]),
        (Fraction(-2), Fraction(1), Fraction(1, 3), Fraction(-4, 3),
         [("~2/3", "counts 1 tick to the right of −1 instead of to the left"),
          ("1 1/3", "drops the minus sign"),
          ("~1 2/3", "counts 1 tick to the right of −2 instead of 2 ticks")]),
    ]
    for lo, hi, step, p, wrong in lines:
        good = fmt(p) if step.denominator != 10 else Q("~0.7")[0]
        svg = mark_large(numline_svg(lo, hi, step, [(p, "P", RED)], "number line with point P"))
        n_ticks = int(abs(p - round_toward(p)) / step)
        e = ("Each whole is split into %d equal parts, so each tick is %s. P is %d tick%s to the left of %s, so P = %s. "
             % (step.denominator, fmt(step) if step.denominator != 10 else "0.1", n_ticks, "" if n_ticks == 1 else "s",
                fmt(round_toward(p)), good))
        e += " ".join("Not %s: that %s." % (Q(w)[0], why) for w, why in wrong[:2])
        its.append(mcq("Which number is at point P?" + svg, good, [Q(w)[0] for w, _ in wrong], e))

    # between
    q = [Q(s) for s in ["~0.4", "~0.3", "~0.6", "~1/4"]]
    a, b = Fraction(-1, 2), Fraction(-1, 3)
    assert a < q[0][1] < b and all(not (a < v < b) for _, v in q[1:])
    its.append(mcq("Which number is between %s and %s?" % (fmt(a), fmt(b)), q[0][0], [h for h, _ in q[1:]],
                   "%s = " % fmt(a) + MINUS + "0.5 and %s ≈ " % fmt(b) + MINUS + "0.33, and " + MINUS + "0.5 &lt; " + MINUS + "0.4 &lt; " + MINUS
                   + "0.33. " + MINUS + "0.3 and " + MINUS + fr(1, 4) + " are closer to 0 than " + MINUS + fr(1, 3) + ", and " + MINUS + "0.6 is less than " + MINUS + "0.5."))
    q = [Q(s) for s in ["~1 3/8", "~1 1/2", "~1 1/8", "~1 5/8"]]
    a, b = Fraction(-3, 2), Fraction(-5, 4)
    assert a < q[0][1] < b and all(not (a < v < b) for _, v in q[1:])
    its.append(mcq("Which number is between %s and %s?" % (MINUS + "1.5", MINUS + "1.25"), q[0][0], [h for h, _ in q[1:]],
                   "Write them in eighths: " + MINUS + "1.5 = " + MINUS + "1 " + fr(4, 8) + " and " + MINUS + "1.25 = " + MINUS + "1 " + fr(2, 8)
                   + ". " + MINUS + "1 " + fr(3, 8) + " is between them. " + MINUS + "1 " + fr(1, 2) + " is equal to " + MINUS
                   + "1.5, so it is not between."))

    # equivalent forms
    its.append(mcq("Which number is equal to %s?" % fmt(Fraction(-5, 4)), MINUS + "1.25", [MINUS + "1.4", "1.25", MINUS + "0.8"],
                   MINUS + fr(5, 4) + " = " + MINUS + "(5 ÷ 4) = " + MINUS + "1.25. Not " + MINUS + "1.4: that writes the 4 as the decimal digit. "
                   "Not 1.25: that drops the minus sign. Not " + MINUS + "0.8: that divides 4 by 5."))
    its.append(mcq("Which fraction is <b>not</b> equal to " + MINUS + fr(2, 3) + "?", fr(MINUS + "2", MINUS + "3"),
                   [fr(MINUS + "2", 3), fr(2, MINUS + "3"), MINUS + "(" + fr(2, 3) + ")"],
                   "A negative divided by a negative is positive, so " + fr(MINUS + "2", MINUS + "3") + " = " + fr(2, 3)
                   + ". The other three each have one minus sign, so they all equal " + MINUS + fr(2, 3) + "."))
    # opposite vs reciprocal
    its.append(mcq("What is the <b>opposite</b> of " + MINUS + "2 " + fr(3, 5) + "?", "2 " + fr(3, 5),
                   [MINUS + fr(5, 13), fr(5, 13), MINUS + "2.6"],
                   "The opposite is the same distance from 0 on the other side, so change only the sign: 2 " + fr(3, 5) + ". Not "
                   + MINUS + fr(5, 13) + ": that is the reciprocal (" + MINUS + "2 " + fr(3, 5) + " = " + MINUS + fr(13, 5)
                   + ", flipped). Not " + MINUS + "2.6: that is the same number written as a decimal. Opposites add to 0; reciprocals multiply to 1."))
    assert len(its) == 20, len(its)
    return {"title": "Compare and order rational numbers", "items": its}


def round_toward(p):
    """The whole number just to the right of a negative p (toward 0), or just to the left of a positive p."""
    import math
    return Fraction(math.ceil(p)) if p < 0 else Fraction(math.floor(p))


def numline_svg(lo, hi, step, points, label, sp=None):
    n = int((hi - lo) / step)
    if sp is None:
        sp = max(16, min(40, 380 // n))
    x0 = 24
    W = x0 * 2 + n * sp
    y = 46
    out = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x0 - 12, y, x0 + n * sp + 12, y, INK)]
    out.append("<path d='M%d %d l8 -5 v10 z' fill='%s'/>" % (x0 - 16, y, INK))
    out.append("<path d='M%d %d l-8 -5 v10 z' fill='%s'/>" % (x0 + n * sp + 16, y, INK))
    for i in range(n + 1):
        v = lo + i * step
        x = x0 + i * sp
        whole = v.denominator == 1
        out.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>" % (x, y - (10 if whole else 6), x, y + (10 if whole else 6), INK, 2 if whole else 1.5))
        if whole:
            out.append("<text x='%d' y='%d' font-size='16' text-anchor='middle' fill='%s'>%s</text>" % (x, y + 30, INK, fmt(v)))
    for v, name, col in points:
        x = x0 + (v - lo) / step * sp
        out.append("<circle cx='%.1f' cy='%d' r='6' fill='%s'/>" % (x, y, col))
        out.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' text-anchor='middle' fill='%s'>%s</text>" % (x, y - 14, col, name))
    return svg_wrap(W, y + 40, "".join(out), label)


# ------------------------------------------------------------ set 2: add and subtract
def lcmi(a, b):
    import math
    return a * b // math.gcd(a, b)


def misalign(a, b):
    """Adds (signed) decimals with the last digits lined up instead of the decimal points."""
    def parts(x):
        s = ("%.4f" % abs(x)).rstrip("0").rstrip(".")
        dp = len(s.split(".")[1]) if "." in s else 0
        return int(s.replace(".", "")) * (1 if x >= 0 else -1), dp
    (na, da), (nb, db) = parts(a), parts(b)
    if da == db:
        return None
    return Fraction(na + nb, 10 ** max(da, db))


def addsub_item(s, k, frac):
    ts = tokens(s)
    assert len(ts) == 3
    a, op, b = ts
    bb = b if op == "+" else -b          # what is really added
    v = a + bb
    assert v != 0 and nice(v), s
    py_check(s, v)
    sa, sb = abs(a), abs(bb)
    same = (a < 0) == (bb < 0)
    cands = []
    if same:
        cands.append(((1 if v > 0 else -1) * abs(sa - sb), "subtracts the sizes, but the signs are the same, so add the sizes"))
    else:
        cands.append(((1 if v > 0 else -1) * (sa + sb), "adds the sizes, but the signs are different, so subtract the sizes"))
    if frac:
        fa, fb = Fraction(a), Fraction(bb)
        if fa.denominator != 1 and fb.denominator != 1:
            cands.append((Fraction(fa.numerator + fb.numerator, fa.denominator + fb.denominator), "adds the numerators and adds the denominators"))
    else:
        m = misalign(a, bb)
        cands.append((m, "lines up the last digits instead of the decimal points"))
    cands.append((-v, "has the wrong sign: two negatives add to a negative" if same else "has the wrong sign: the number with the greater size decides the sign"))
    if op == "−" and b < 0:
        cands.insert(1, (a + b, "subtracts %s instead of adding it" % fmt(-b)))
    elif op == "−":
        cands.insert(1, (a + b, "adds %s instead of subtracting it" % fmt(b)))
    elif b < 0:
        cands.append((a - b, "drops the minus sign on %s" % fmt(b)))
    if a < 0:
        cands.append((-a + bb, "drops the minus sign on %s" % fmt(a)))
    ms = pick3(v, cands)

    e = ""
    if op == "−":
        e += "Subtracting %s is the same as adding its opposite: %s = %s + %s. " % (P(b), H(s), fmt(a), P(bb))
    if frac:
        fa, fb = Fraction(a), Fraction(bb)
        L = lcmi(fa.denominator, fb.denominator)
        na, nb = fa.numerator * L // fa.denominator, fb.numerator * L // fb.denominator
        imp = ""
        if abs(fa) > 1 and fa.denominator != 1 or abs(fb) > 1 and fb.denominator != 1:
            imp = "Write mixed numbers as improper fractions. "
        e += imp + "Use the common denominator %d: %s + %s = %s" % (L, sfr(na, L), "(" + sfr(nb, L) + ")" if nb < 0 else sfr(nb, L),
                                                                     sfr(na + nb, L))
        vv = Fraction(na + nb, L)
        if vv.denominator != L:
            e += " = " + sfr(vv.numerator, vv.denominator)
        if abs(vv) > 1 and vv.denominator != 1:
            e += " = " + fmt(vv)
        e += ". "
    else:
        if same:
            e += "The signs are the same, so add the sizes: %s + %s = %s, and keep the sign. " % (fmt(sa), fmt(sb), fmt(sa + sb))
        else:
            big, small = (sa, sb) if sa > sb else (sb, sa)
            e += ("The signs are different, so subtract the sizes: %s − %s = %s. The number with the greater size is %s, so the answer is %s. "
                  % (fmt(big), fmt(small), fmt(big - small), "negative" if v < 0 else "positive", fmt(v)))
    e += nots(ms[:2])
    return mcq(ASK[k % len(ASK)] % B(H(s)), fmt(v), [fmt(w) for w, _ in ms], e)


def set_addsub(rnd, used):
    its = []
    mode(neg=True, dec=True, dp=3)
    R = rnd.randint
    d1 = lambda lo, hi: Fraction(R(lo, hi), 10)
    d2 = lambda lo, hi: Fraction(R(lo, hi), 100)
    dec_t = [
        ("~{a} + {b}", lambda: (d1(21, 59), d2(105, 195))),
        ("{a} + ~{b}", lambda: (d2(105, 295), d1(31, 69))),
        ("~{a} + ~{b}", lambda: (d1(11, 49), d2(105, 295))),
        ("{a} − {b}", lambda: (d1(11, 39), d2(405, 795))),
        ("~{a} − {b}", lambda: (d2(105, 395), d1(11, 49))),
        ("{a} − ~{b}", lambda: (d1(11, 49), d2(105, 395))),
        ("~{a} − ~{b}", lambda: (d1(11, 39), d2(405, 795))),
        ("~{a} − ~{b}", lambda: (d2(405, 795), d1(11, 39))),
        ("~{a} + {b}", lambda: (d2(1005, 1895), d1(41, 89))),
    ]
    for k, (t, mk) in enumerate(dec_t):
        for _ in range(1000):
            x, y = mk()
            if x.denominator == 1 or y.denominator == 1 or (x * 10).denominator == 1 and (y * 10).denominator == 1:
                continue
            s = t.format(a=src(x), b=src(y))
            if s in used:
                continue
            try:
                it = addsub_item(s, k, False)
            except AssertionError:
                continue
            break
        used.add(s)
        its.append(it)
    mode(neg=True, frac=True)
    small = [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5), (1, 6), (5, 6), (3, 8), (5, 8), (7, 10), (5, 12)]
    fp = lambda: Fraction(*rnd.choice(small))
    frac_t = [
        ("~{a} + {b}", lambda: (fp(), fp())),
        ("{a} + ~{b}", lambda: (fp(), fp())),
        ("~{a} + ~{b}", lambda: (fp(), fp())),
        ("~{a} − {b}", lambda: (fp(), fp())),
        ("{a} − ~{b}", lambda: (fp(), fp())),
        ("~{a} − ~{b}", lambda: (fp(), fp())),
        ("~{a} + {b}", lambda: (R(1, 3) + fp(), fp())),
        ("~{a} − {b}", lambda: (R(1, 2) + fp(), R(1, 2) + fp())),
        ("{a} − ~{b}", lambda: (R(1, 3) + fp(), fp())),
    ]
    for k, (t, mk) in enumerate(frac_t):
        for _ in range(2000):
            x, y = mk()
            if x == y or x.denominator == y.denominator:
                continue
            s = t.format(a=src(x), b=src(y))
            if s in used:
                continue
            try:
                it = addsub_item(s, k + 1, True)
            except AssertionError:
                continue
            break
        used.add(s)
        its.append(it)
    # missing number and concepts
    mode(neg=True, dec=True)
    assert Fraction("0.5") - Fraction("-1.2") == Fraction("1.7")
    its.append(mcq("What number goes in the box?<br>" + B(MINUS + "1.2 + □ = 0.5"), "1.7", [MINUS + "0.7", "0.7", MINUS + "1.7"],
                   "□ = 0.5 " + MINUS + " (" + MINUS + "1.2) = 0.5 + 1.2 = 1.7. Check: " + MINUS + "1.2 + 1.7 = 0.5. "
                   "Not 0.7: that subtracts 1.2 instead of adding it. Not " + MINUS + "0.7: " + MINUS + "1.2 + (" + MINUS + "0.7) = " + MINUS + "1.9."))
    mode(neg=True, frac=True)
    v = ev("~3/4 − ~1/2")
    assert v == Fraction(-1, 4)
    its.append(mcq("Which expression has the same value as " + B(H("~3/4 − ~1/2")) + "?", H("~3/4 + 1/2"),
                   [H("~3/4 − 1/2"), H("3/4 + 1/2"), H("~3/4 + ~1/2")],
                   "Subtracting a negative is the same as adding its opposite: " + H("~3/4 − ~1/2") + " = " + H("~3/4 + 1/2") + " = "
                   + MINUS + fr(1, 4) + ". The other expressions equal " + MINUS + "1 " + fr(1, 4) + ", 1 " + fr(1, 4) + " and " + MINUS + "1 " + fr(1, 4) + "."))
    assert ev("~3/4 − 1/2") == Fraction(-5, 4) and ev("3/4 + 1/2") == Fraction(5, 4) and ev("~3/4 + ~1/2") == Fraction(-5, 4)
    assert len(its) == 20, len(its)
    return {"title": "Add and subtract rational numbers", "items": its}


# ------------------------------------------------------------ set 3: multiply and divide
def sign_why(a, b):
    if (a < 0) == (b < 0):
        return "has the wrong sign: two negatives give a positive" if a < 0 else "has the wrong sign: two positives give a positive"
    return "has the wrong sign: a negative and a positive give a negative"


def muldiv_item(s, k, frac):
    ts = tokens(s)
    a, op, b = ts
    v = a * b if op == "×" else a / b
    assert v != 0 and nice(v), s
    py_check(s, v)
    sgn = 1 if v > 0 else -1
    A, Bv = abs(a), abs(b)
    cands = []
    if frac:
        if op == "×":
            fa, fb = Fraction(a), Fraction(b)
            if (A > 1 and A.denominator != 1) or (Bv > 1 and Bv.denominator != 1):
                wa, wb = int(A), int(Bv)
                cands.append((sgn * (wa * wb + (A - wa) * (Bv - wb)), "multiplies the whole numbers and the fractions separately"))
            elif fa.denominator != 1 and fb.denominator != 1:
                L = lcmi(fa.denominator, fb.denominator)
                cands.append((sgn * Fraction(A.numerator * L // A.denominator * Bv.numerator * L // Bv.denominator, L),
                              "keeps the common denominator; when you multiply, multiply the denominators too"))
            cands.append((sgn * A / Bv, "divides instead of multiplying"))
        else:
            cands.append((sgn * (1 / A) * Bv, "flips the first fraction instead of the divisor"))
            cands.append((sgn * A * Bv, "multiplies without flipping the divisor"))
            cands.append((sgn * Bv / A, "divides the second number by the first"))
    else:
        if op == "×":
            cands.append((v * 10, "puts the decimal point in the wrong place (count the decimal places in both numbers)"))
            cands.append((v / 10, "puts too many decimal places in the answer"))
        else:
            cands.append((v / 10, "puts the decimal point in the wrong place"))
            cands.append((sgn * A * Bv, "multiplies instead of dividing"))
            cands.append((v * 10, "puts the decimal point in the wrong place"))
    cands.insert(1, (-v, sign_why(a, b)))
    ms = pick3(v, cands)
    rule = "Both numbers are negative, so the answer is positive." if (a < 0 and b < 0) else \
        ("One number is negative, so the answer is negative." if (a < 0) != (b < 0) else "Both numbers are positive, so the answer is positive.")
    if frac:
        fa, fb = Fraction(a), Fraction(b)
        mixed = (A > 1 and A.denominator != 1) or (Bv > 1 and Bv.denominator != 1)
        e = rule + " "
        if mixed:
            e += "Write the mixed numbers as improper fractions: %s. " % ", ".join(
                "%s = %s" % (fmt(x), fr(x.numerator, x.denominator)) for x in (A, Bv) if x > 1 and x.denominator != 1)
        fA = fr(A.numerator, A.denominator) if A.denominator != 1 else fmt(A)
        fB = fr(Bv.numerator, Bv.denominator) if Bv.denominator != 1 else fmt(Bv)
        if op == "×":
            raw = (A.numerator * Bv.numerator, A.denominator * Bv.denominator)
            e += "Multiply the numerators and the denominators: %s × %s = %s" % (fA, fB, fr(*raw))
        else:
            rb = 1 / Bv
            fR = fr(rb.numerator, rb.denominator) if rb.denominator != 1 else fmt(rb)
            raw = (A.numerator * rb.numerator, A.denominator * rb.denominator)
            e += "Multiply by the reciprocal of the divisor: %s ÷ %s = %s × %s = %s" % (fA, fB, fA, fR, fr(*raw))
        rawh = fr(*raw) if raw[1] != 1 else str(raw[0])
        e = e.replace(fr(raw[0], 1), str(raw[0]))
        if fmt(abs(v)) != rawh:
            e += " = " + fmt(abs(v))
        e += ", so the answer is %s. " % fmt(v)
    else:
        if op == "×":
            e = "%s %s × %s = %s. %s " % ("Multiply the sizes:", fmt(A), fmt(Bv), fmt(A * Bv), rule)
        else:
            e = "Divide the sizes: %s ÷ %s = %s. %s " % (fmt(A), fmt(Bv), fmt(A / Bv), rule)
    e += nots(ms[:2])
    return mcq(ASK[k % len(ASK)] % B(H(s)), fmt(v), [fmt(w) for w, _ in ms], e)


def set_muldiv(rnd, used):
    its = []
    R = rnd.randint
    mode(neg=True, dec=True, dp=4)
    d1 = lambda lo, hi: Fraction(R(lo, hi), 10)
    dec_t = [
        ("~{a} × {b}", lambda: (d1(2, 9), d1(2, 9))),
        ("{a} × ~{b}", lambda: (d1(11, 39), R(3, 9))),
        ("~{a} × ~{b}", lambda: (d1(11, 29), d1(2, 9))),
        ("~{a} × {b}", lambda: (Fraction(R(11, 49), 100), R(2, 8))),
        ("~{a} ÷ {b}", lambda: (lambda b, q: (b * q, b))(d1(2, 9), R(2, 9))),
        ("{a} ÷ ~{b}", lambda: (lambda b, q: (b * q, b))(R(2, 9), d1(11, 39))),
        ("~{a} ÷ ~{b}", lambda: (lambda b, q: (b * q, b))(d1(2, 9), d1(11, 49))),
        ("~{a} ÷ {b}", lambda: (lambda b, q: (b * q, b))(Fraction(R(2, 9), 100), R(2, 9))),
    ]
    for k, (t, mk) in enumerate(dec_t):
        for _ in range(2000):
            x, y = mk()
            if x == y or x == 1 or y == 1 or (x.denominator == 1 and y.denominator == 1):
                continue
            s = t.format(a=src(x), b=src(y))
            if s in used:
                continue
            try:
                it = muldiv_item(s, k, False)
            except AssertionError:
                continue
            break
        used.add(s)
        its.append(it)
    mode(neg=True, frac=True)
    small = [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5), (4, 5), (1, 6), (5, 6), (3, 8), (5, 8), (7, 8), (2, 9), (4, 9), (3, 10)]
    fp = lambda: Fraction(*rnd.choice(small))
    frac_t = [
        ("~{a} × {b}", lambda: (fp(), fp())),
        ("{a} × ~{b}", lambda: (fp(), fp())),
        ("~{a} × ~{b}", lambda: (fp(), fp())),
        ("~{a} × {b}", lambda: (R(1, 2) + fp(), R(1, 2) + fp())),
        ("~{a} ÷ {b}", lambda: (fp(), fp())),
        ("{a} ÷ ~{b}", lambda: (fp(), fp())),
        ("~{a} ÷ ~{b}", lambda: (fp(), fp())),
        ("~{a} ÷ {b}", lambda: (R(1, 2) + fp(), fp())),
        ("{a} ÷ ~{b}", lambda: (R(2, 6), fp())),
        ("~{a} ÷ {b}", lambda: (fp(), R(2, 6))),
    ]
    for k, (t, mk) in enumerate(frac_t):
        for _ in range(4000):
            x, y = mk()
            if x == y or x.denominator == y.denominator:
                continue
            s = t.format(a=src(x), b=src(y))
            if s in used:
                continue
            try:
                it = muldiv_item(s, k + 2, True)
            except AssertionError:
                continue
            if Fraction(ev(s)).denominator > 24:
                continue
            break
        used.add(s)
        its.append(it)
    # concepts
    its.append(mcq("Dividing by " + MINUS + fr(2, 3) + " is the same as multiplying by …", MINUS + fr(3, 2),
                   [fr(3, 2), MINUS + fr(2, 3), fr(2, 3)],
                   "To divide, multiply by the reciprocal of the divisor. The reciprocal of " + MINUS + fr(2, 3) + " is " + MINUS + fr(3, 2)
                   + ": flip the fraction and keep the sign, because " + MINUS + fr(2, 3) + " × (" + MINUS + fr(3, 2) + ") = 1. Not " + fr(3, 2)
                   + ": a reciprocal has the same sign."))
    vals = {"a": Fraction(-1, 2) * Fraction(-3, 4) * Fraction(-2), "b": Fraction(-1, 2) * Fraction(-3, 4) * 2,
            "c": Fraction(-1, 2) * Fraction(3, 4) * 2, "d": Fraction(1, 2) * Fraction(-3, 4) * 2}
    assert vals["b"] > 0 and all(vals[k] < 0 for k in "acd")
    its.append(mcq("Which product is <b>positive</b>?", "(" + MINUS + fr(1, 2) + ") × (" + MINUS + fr(3, 4) + ") × 2",
                   ["(" + MINUS + fr(1, 2) + ") × (" + MINUS + fr(3, 4) + ") × (" + MINUS + "2)",
                    "(" + MINUS + fr(1, 2) + ") × " + fr(3, 4) + " × 2",
                    fr(1, 2) + " × (" + MINUS + fr(3, 4) + ") × 2"],
                   "Count the negative factors. An even number of negatives gives a positive; an odd number gives a negative. "
                   "Only (" + MINUS + fr(1, 2) + ") × (" + MINUS + fr(3, 4) + ") × 2 has 2 negative factors: it equals " + fr(3, 4) + "."))
    assert len(its) == 20, len(its)
    return {"title": "Multiply and divide rational numbers", "items": its}


# ------------------------------------------------------------ set 4: order of operations
def set_order(rnd, used):
    R = rnd.randint
    mode(neg=True, dec=True)
    TD = [
        ("~{a} + {b} × {c}", ["ltr"], [("{a} + {b} × {c}", "drops the minus sign on −{a}")], lambda r: (dec1(R(11, 99)), dec1(R(11, 49)), R(2, 9))),
        ("{a} × ~{b} + {c}", ["drop"], [("{a} × ~{b} − {c}", "subtracts {c} instead of adding it")], lambda r: (R(2, 9), dec1(R(11, 49)), dec1(R(11, 99)))),
        ("~{a} × ~{b} − {c}", ["negneg"], [("~{a} × ~{b} + {c}", "adds {c} instead of subtracting it")], lambda r: (dec1(R(11, 49)), R(2, 9), dec1(R(11, 99)))),
        ("{a} − ~{b} × {c}", ["subneg", "ltr"], [], lambda r: (dec1(R(11, 99)), dec1(R(11, 49)), R(2, 6))),
        ("~{a} + {b} ÷ ~{c}", ["drop", "ltr"], [], lambda r: (lambda c, q: (dec1(R(11, 99)), c * q, c))(R(2, 8), dec1(R(11, 39)))),
        ("({a} − {b}) × ~{c}", ["negneg", "noparen"], [], lambda r: (dec1(R(11, 39)), dec1(R(41, 89)), R(2, 6))),
        ("~{a}^2 − {b}", ["negpow", "sq2"], [], lambda r: (dec1(R(2, 9)), dec1(R(11, 49)))),
    ]
    its = templated(rnd, TD, used, vmax=200)
    mode(neg=True, frac=True)
    F = Fraction
    small = [F(1, 2), F(1, 3), F(2, 3), F(1, 4), F(3, 4), F(1, 5), F(2, 5), F(3, 5), F(1, 6), F(5, 6), F(3, 8), F(5, 8)]
    pick = lambda: rnd.choice(small)
    TF = [
        ("{a} + ~{b} × {c}", ["ltr", "drop"], [], lambda r: (pick(), pick(), R(2, 6))),
        ("~{a} × ~{b} − {c}", ["negneg"], [("~{a} × ~{b} + {c}", "adds {c} instead of subtracting it")], lambda r: (pick(), R(2, 4) * 6, pick())),
        ("{a} − {b} ÷ ~{c}", ["subneg", "drop", "ltr"], [], lambda r: (pick(), pick(), pick())),
        ("~{a} ÷ {b} + {c}", ["drop", "rev"], [], lambda r: (pick(), pick(), pick())),
        ("~{a} − {b} × ~{c}", ["subneg", "ltr"], [], lambda r: (pick(), pick(), R(2, 6) * 2)),
        ("({a} − {b}) ÷ ~{c}", ["negneg", "noparen"], [], lambda r: (pick(), R(1, 2), pick())),
        ("{a} × ~{b} + {c} ÷ ~{d}", ["drop", "ltr"], [], lambda r: (R(2, 4) * 4, pick(), pick(), pick())),
        ("~{a}^2 + {b}", ["negpow", "sq2"], [("(~{a} + {b})^2", "adds before squaring")], lambda r: (pick(), pick())),
        ("{a} − ~{b} + {c} × ~{d}", ["subneg", "drop", "ltr"], [], lambda r: (pick(), pick(), pick(), R(2, 4) * 2)),
        ("~{a}^3 × {b}", ["negpow", "sq2"], [], lambda r: rnd.choice([(F(1, 2), R(2, 5) * 8), (F(1, 3), 27), (F(1, 3), 54), (F(3, 2), 8 * R(1, 3))])),
    ]
    its += templated(rnd, TF, used, vmax=50, k0=1)
    s = "~2/3 + 1/3 × 4"
    assert val(s) == Fraction(2, 3) and ev(s, "ltr") == Fraction(-4, 3)
    its.append(true_item(s, ["ltr"], [("2/3 + 1/3 × 4", "drops the minus sign on −" + fr(2, 3)),
                                      ("~2/3 + 1/3 + 4", "adds instead of multiplying")]))
    mode(neg=True, dec=True)
    assert val("~1.5 × 4 − 2.5") == Fraction(-17, 2)
    its.append(first_item("~1.5 × (4 − 2.5)", "4 − 2.5", [MINUS + "1.5 × 4", MINUS + "1.5 − 2.5", "Either part"],
                          "Brackets first, then multiply. Without brackets the answer would be " + fmt(Fraction(-17, 2)) + "."))
    mode(neg=True, frac=True)
    s = "~3/4 ÷ ~1/2 × 2/3"
    assert val(s) == 1 and ev(s, "mulfirst") == Fraction(9, 4)
    assert Fraction(-4, 3) * Fraction(-1, 2) * Fraction(2, 3) == Fraction(4, 9)
    its.append(mcq("What is the value of %s?" % B(H(s)), "1", [MINUS + "1", "2 " + fr(1, 4), fr(4, 9)],
                   chain(s) + ". ÷ and × have the same rank, so work from left to right. Two negatives divided give a positive. "
                   "Not 2 " + fr(1, 4) + ": that multiplies first. Not " + fr(4, 9) + ": that flips the first fraction instead of the divisor."))
    assert len(its) == 20, len(its)
    return {"title": "Order of operations with rational numbers", "items": its}


# ------------------------------------------------------------ set 5: word problems
def money_signed(v):
    v = Fraction(v)
    if (v * 100).denominator != 1 or v == 0:
        return None
    m = money(abs(v))
    if m and m.endswith(".00"):
        m = m[:-3]
    return (MINUS if v < 0 else "") + m if m else None


def money2(v):
    """$ with two decimals when there are cents."""
    v = Fraction(v)
    if v <= 0 or (v * 100).denominator != 1:
        return None
    c = int(v * 100)
    return "$%s.%02d" % (group(c // 100), c % 100) if c % 100 else "$" + group(c // 100)


UNITS = {
    "$": money2,
    "$±": money_signed,
    "°C": lambda v: fmt(v) + "°C",
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
        e = "One expression: %s, so the answer is %s. %s%s" % (chain(s), ans, (note + " " if note else ""), why_text(ms, u, 3))
        its.append(mcq(text, ans, [u(w) for w, _ in ms[:3]], e))

    def which(text, good, bads, tail):
        val(good)
        for b in bads:
            assert ev(b) != ev(good), b
        its.append(mcq(text, H(good), [H(b) for b in bads], "%s. %s" % (chain(good), tail)))

    mode(neg=True, dec=True)
    # temperatures
    wp("At 6:00 a.m. the temperature in Prince George is −14.5°C. By 2:00 p.m. it has risen 9.8°C. What is the temperature at 2:00 p.m.?",
       "~14.5 + 9.8", "°C", [], [("14.5 + 9.8", "drops the minus sign on −14.5"), ("~14.5 − 9.8", "subtracts the rise instead of adding it"),
                                 ("14.5 − 9.8", "gets the sign wrong")])
    wp("It is −6.5°C at the top of Whistler Mountain and 3.8°C in Whistler Village. How many degrees warmer is the village?",
       "3.8 − ~6.5", "°C", [], [("3.8 − 6.5", "subtracts 6.5 instead of adding it"), ("~6.5 − 3.8", "subtracts in the wrong order"),
                                ("6.5 − 3.8", "ignores the minus sign on −6.5°C")])
    wp("The low temperatures in Fort Nelson on four nights are −18.5°C, −22°C, −15.5°C and −20°C. What is the mean low temperature?",
       "(~18.5 + ~22 + ~15.5 + ~20) ÷ 4", "°C", ["noparen"], [("(18.5 + 22 + 15.5 + 20) ÷ 4", "drops the minus signs")])
    wp("At 8:00 p.m. it is 1.5°C in Kamloops. The temperature falls 0.8°C every hour for 5 hours. What is the temperature at 1:00 a.m.?",
       "1.5 − 5 × 0.8", "°C", ["ltr"], [("1.5 − 0.8", "counts only one hour"), ("5 × 0.8 − 1.5", "subtracts in the wrong order")])
    wp("A freezer is at −18°C. During a power outage its temperature rises 1.25°C each hour. What is the temperature after 6 hours?",
       "~18 + 6 × 1.25", "°C", ["ltr"], [("18 + 6 × 1.25", "drops the minus sign on −18"), ("~18 − 6 × 1.25", "subtracts the rise instead of adding it")])
    wp("At 7:00 a.m. it is −3.2°C in Kelowna. During the day the temperature changes by +2.4°C, −1.5°C and then +4.1°C. What is the temperature at the end?",
       "~3.2 + 2.4 + ~1.5 + 4.1", "°C", [], [("~3.2 + 2.4 + 1.5 + 4.1", "adds the drop of 1.5°C"),
                                            ("3.2 + 2.4 + ~1.5 + 4.1", "drops the minus sign on −3.2"),
                                            ("2.4 + ~1.5 + 4.1", "forgets the starting temperature")])
    wp("The temperature in Smithers changes by −2.4°C, +1.2°C and −3.6°C on three days in a row. What is the mean change per day?",
       "(~2.4 + 1.2 + ~3.6) ÷ 3", "°C", ["noparen"], [("(2.4 + 1.2 + 3.6) ÷ 3", "ignores the signs")])
    wp("In 6 hours the temperature in Vernon falls from 5.4°C to −3°C. What is the mean change per hour?",
       "(~3 − 5.4) ÷ 6", "°C", [], [("(5.4 − ~3) ÷ 6", "subtracts in the wrong order: change = final − start"),
                                    ("(~3 + 5.4) ÷ 6", "adds the temperatures instead of subtracting")])
    which("At midnight it is −2.5°C in Prince George. The temperature drops 1.5°C every hour for 4 hours. Which expression gives the temperature at 4:00 a.m.?",
          "~2.5 − 4 × 1.5", ["(~2.5 − 4) × 1.5", "~2.5 + 4 × 1.5", "2.5 − 4 × 1.5"],
          "So it is " + MINUS + "8.5°C at 4:00 a.m. (" + MINUS + "2.5 " + MINUS + " 4) × 1.5 subtracts before multiplying, and " + MINUS
          + "2.5 + 4 × 1.5 treats the drop as a rise.")
    which("At 6:00 a.m. it is −7.5°C on Grouse Mountain. The temperature rises 2.5°C every hour. Which expression gives the number of hours until it reaches 0°C?",
          "(0 − ~7.5) ÷ 2.5", ["~7.5 ÷ 2.5", "7.5 × 2.5", "2.5 − ~7.5"],
          "It takes 3 hours. The temperature must change by 0 " + MINUS + " (" + MINUS + "7.5) = 7.5°C, and it rises 2.5°C each hour. ("
          + MINUS + "7.5) ÷ 2.5 = " + MINUS + "3 cannot be a number of hours.")
    # money
    wp("The school ski club's account has $125.40. The club pays $210.65 for a bus to Grouse Mountain. What is the account balance now?",
       "125.4 − 210.65", "$±", [], [("210.65 − 125.4", "subtracts in the wrong order"), ("125.4 + 210.65", "adds the cost instead of subtracting it"),
                                   ("~125.4 − 210.65", "makes the starting balance negative")],
       "The balance is negative: the club owes $85.25.")
    wp("Mei has $20 on her transit card. She takes 4 bus rides that cost $3.15 each. How much is left on the card?",
       "20 − 4 × 3.15", "$", ["ltr"], [("20 − 3.15", "counts only one ride"), ("4 × 3.15", "finds the cost of the rides, not what is left")])
    wp("A share of a company is worth $24.80. Its value changes by −$1.35 each day for 4 days. What is the share worth then?",
       "24.8 + 4 × ~1.35", "$", ["drop"], [("24.8 + ~1.35", "counts only one day"), ("24.8 − 4 − 1.35", "subtracts 4 instead of multiplying by 4")])
    wp("After buying jerseys, a lacrosse team's fundraising account is at −$36.50. The team then sells 45 chocolate bars at $2.50 each. What is the balance now?",
       "~36.5 + 45 × 2.5", "$±", ["ltr"], [("36.5 + 45 × 2.5", "drops the minus sign on −$36.50"),
                                          ("45 × 2.5", "forgets the starting balance")])
    wp("Ava earns $18.25 an hour at a part-time job in Nanaimo. She works 6 hours and spends $23.40 on lunch and bus fare. How much of the day's pay does she have left?",
       "6 × 18.25 − 23.4", "$", [], [("6 × 18.25", "forgets the lunch and bus fare"), ("6 + 18.25 − 23.4", "adds the hours instead of multiplying"),
                                     ("6 × 18.25 + 23.4", "adds the spending instead of subtracting it")])
    wp("Over three months, Ji-woo's family savings change by +$120.50, −$45.75 and −$210.25. What is the total change?",
       "120.5 + ~45.75 + ~210.25", "$±", [], [("120.5 + 45.75 + 210.25", "ignores the minus signs"),
                                              ("120.5 − 45.75 + 210.25", "drops one minus sign"),
                                              ("~120.5 + ~45.75 + ~210.25", "makes the gain negative")])
    wp("Four friends rent a canoe on Okanagan Lake for $68.40 and buy snacks for $19.20. They split the total cost equally. How much does each friend pay?",
       "(68.4 + 19.2) ÷ 4", "$", ["noparen"], [("68.4 ÷ 4", "forgets the snacks"), ("68.4 + 19.2", "forgets to split the cost")])
    wp("Olivia buys 3 T-shirts at $12.99 each and pays part of the cost with a $15 gift card. How much more does she pay?",
       "3 × 12.99 − 15", "$", [], [("3 × 12.99 + 15", "adds the gift card instead of subtracting it"), ("3 × 12.99", "forgets the gift card"),
                                   ("3 × 13 − 15", "rounds $12.99 up to $13")])
    mode(neg=True, frac=True)
    wp("Kai has $48. He spends " + fr(3, 8) + " of it on a lacrosse stick and " + fr(1, 4) + " of it on a ball and tape. How much money does he have left?",
       "48 − (3/8 + 1/4) × 48", "$", ["noparen"], [("(3/8 + 1/4) × 48", "finds the money spent, not the money left"),
                                                  ("48 − 1/4 × 48", "forgets the " + fr(3, 8)),
                                                  ("48 − 3/8 × 48 + 1/4 × 48", "adds the " + fr(1, 4) + " instead of subtracting it")])
    mode(neg=True, dec=True)
    which("Ski rental costs $38.50 a day plus a one-time $12 fee. Which expression gives the cost of renting skis for 3 days?",
          "12 + 3 × 38.5", ["(12 + 38.5) × 3", "12 × 3 + 38.5", "3 × 38.5 − 12"],
          "So the rental costs $127.50. (12 + 38.5) × 3 would charge the one-time fee 3 times.")
    assert len(its) == 20, len(its)
    return {"title": "Word problems: temperatures and money", "items": its}


# ------------------------------------------------------------ lesson
def steps_svg(rows, label, W=380):
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


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    M = MINUS
    mode(neg=True, frac=True)
    nl = numline_svg(Fraction(-1), Fraction(0), Fraction(1, 4), [(Fraction(-3, 4), M + "3/4", RED), (Fraction(-1, 2), M + "1/2", BLUE)],
                     "number line from negative 1 to 0 in fourths: negative three fourths is to the left of negative one half", sp=80)
    assert ev("~2/3 − ~1/4") == Fraction(-5, 12)
    assert Fraction(-3, 4) / Fraction(1, 2) == Fraction(-3, 2)
    assert val("~1/2 + 3/4 × ~2") == -2
    fig2 = steps_svg([([M + "1/2 + ", ("3/4 × (" + M + "2)", RED)], "multiply first"),
                      ([(M + "1/2 + (" + M + "3/2)", RED)], "then add"),
                      ([(M + "2", GREEN)], "")], "working out negative one half plus three fourths times negative 2 step by step: the answer is negative 2")
    ex_oo = chain("~1/2 + 3/4 × ~2")
    mode(neg=True, dec=True)
    assert Fraction("-3.6") + Fraction("1.25") == Fraction("-2.35")
    assert Fraction("-0.4") * Fraction("-0.3") == Fraction("0.12")
    return (
        "<h2>What is a rational number?</h2>"
        "<p>A <b>rational number</b> is any number you can write as a fraction of two integers, like " + M + fr(3, 4) + ", 2.5 or " + M + "6. "
        "Positive and negative fractions and decimals are all rational numbers. They follow the same sign rules as integers.</p>"
        "<h2>Compare and order</h2>"
        "<p>On a number line, numbers get greater to the right. For two negative numbers, the one <b>closer to 0</b> is greater.</p>"
        "<figure class='sn-fig'>" + nl + "<figcaption>" + M + fr(3, 4) + " is to the left of " + M + fr(1, 2) + ", so " + M + fr(3, 4)
        + " &lt; " + M + fr(1, 2) + ", even though " + fr(3, 4) + " &gt; " + fr(1, 2) + ".</figcaption></figure>"
        "<p>To compare a fraction and a decimal, write both as decimals: " + M + fr(5, 8) + " = " + M + "0.625, so " + M + fr(5, 8) + " &lt; " + M + "0.6.</p>"
        "<h2>Add and subtract</h2>"
        "<p>To subtract, <b>add the opposite</b>. Then use the signs: same signs, add the sizes and keep the sign; different signs, "
        "subtract the sizes and take the sign of the number with the greater size.</p>" +
        ex("Decimals with different signs", "Evaluate " + M + "3.6 + 1.25.",
           "The signs are different, so subtract the sizes: 3.6 " + M + " 1.25 = 2.35. " + M + "3.6 has the greater size, so the answer is negative.",
           M + "2.35") +
        ex("Subtracting a negative fraction", "Evaluate " + M + fr(2, 3) + " " + M + " (" + M + fr(1, 4) + ").",
           "Add the opposite: " + M + fr(2, 3) + " + " + fr(1, 4) + " = " + M + fr(8, 12) + " + " + fr(3, 12) + " = " + M + fr(5, 12) + ".",
           M + fr(5, 12)) +
        "<h2>Multiply and divide</h2>" +
        table(["Signs", "Result", "Example"], [
            ["same signs", "positive", "(" + M + "0.4) × (" + M + "0.3) = 0.12"],
            ["different signs", "negative", "(" + M + fr(3, 4) + ") × " + fr(2, 5) + " = " + M + fr(3, 10)],
        ]) +
        "<p>To divide by a fraction, <b>multiply by the reciprocal of the divisor</b> (the second number). Flip only the divisor, and keep its sign.</p>" +
        ex("Dividing fractions", "Evaluate (" + M + fr(3, 4) + ") ÷ " + fr(1, 2) + ".",
           "(" + M + fr(3, 4) + ") × " + fr(2, 1) + " = " + M + fr(6, 4) + " = " + M + "1 " + fr(1, 2) + ". Different signs give a negative.",
           M + "1 " + fr(1, 2)) +
        "<h2>Order of operations</h2>"
        "<p>Use <b>BEDMAS</b> for every kind of number: brackets, exponents, ÷ and × from left to right, then + and − from left to right. "
        "Apply the sign rules at each step.</p>"
        "<figure class='sn-fig'>" + fig2 + "<figcaption>Multiply before you add: " + M + fr(1, 2) + " + " + fr(3, 4) + " × (" + M + "2) = " + M + "2.</figcaption></figure>" +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            [M + fr(3, 4) + " &gt; " + M + fr(1, 2) + " because 3/4 is bigger", "For negatives, the number closer to 0 is greater: " + M + fr(3, 4) + " &lt; " + M + fr(1, 2)],
            [M + "3.6 + 1.25 = " + M + "4.85", "Different signs: subtract the sizes, " + M + "2.35"],
            ["2 " + M + " (" + M + "1.5) = 0.5", "Subtracting a negative means adding: 2 + 1.5 = 3.5"],
            ["(" + M + "0.4) × (" + M + "0.3) = " + M + "0.12", "Two negatives give a positive: 0.12"],
            [fr(3, 4) + " ÷ " + fr(1, 2) + " = " + fr(4, 3) + " × " + fr(1, 2), "Flip the divisor, not the first number: " + fr(3, 4) + " × 2 = 1 " + fr(1, 2)],
            [M + fr(2, 3) + " + " + fr(1, 4) + " = " + M + fr(1, 7), "Use a common denominator: " + M + fr(8, 12) + " + " + fr(3, 12) + " = " + M + fr(5, 12)],
        ])
    ), ex_oo


FAQ = [
    {"q": "What is a rational number in Grade 9 math?",
     "a": "A rational number is any number that can be written as a fraction of two integers, such as −3/4, 0.6 or −5. "
          "In Mathematics 9, students add, subtract, multiply and divide positive and negative fractions and decimals."},
    {"q": "How do you compare negative fractions?",
     "a": "For negative numbers, the one closer to 0 is greater. So −1/2 > −3/4, even though 3/4 is greater than 1/2. Writing both as decimals (−0.5 and −0.75) makes it easy to check."},
    {"q": "How do you divide negative fractions?",
     "a": "Multiply by the reciprocal of the divisor, then use the sign rules. For example, (−3/4) ÷ (−1/2) = (−3/4) × (−2) = 3/2, because two negatives give a positive."},
    {"q": "Where are rational numbers in the BC Mathematics 9 curriculum?",
     "a": "They are under Computational fluency: operations with rational numbers, including addition, subtraction, multiplication, division and order of operations. "
          "Grade 9 students in BC do not write the FSA, which is written in Grades 4 and 7."},
]


def gen():
    rnd = random.Random(59802)
    used = set()
    sets = [set_compare(rnd, used), set_addsub(rnd, used), set_muldiv(rnd, used), set_order(rnd, used), set_words(rnd, used)]
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
    body, _ = body_html()
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-9", "slug": "operations-with-rational-numbers", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 9 Operations with Rational Numbers",
        "seo_title": "Grade 9 Rational Numbers Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Rational Numbers",
        "domain": "Computational fluency",
        "standard_code": "Grade 9: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/9/core",
        "standard_text": "Operations with rational numbers (addition, subtraction, multiplication, division, and order of operations)",
        "meta_desc": "Free Grade 9 math worksheets on rational numbers for the BC curriculum: compare and order, add and subtract, multiply and divide "
                     "negative fractions and decimals, order of operations and temperature and money problems. 100 questions with an answer key.",
        "key_big": "Rational numbers follow the integer sign rules. To divide, multiply by the reciprocal of the divisor.",
        "key_sub": "Subtracting a negative means adding: −2/3 − (−1/4) = −2/3 + 1/4 = −5/12. (−3/4) ÷ 1/2 = (−3/4) × 2 = −1 1/2. For negatives, the number closer to 0 is greater.",
        "body_html": body, "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
