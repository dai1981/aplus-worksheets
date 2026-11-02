# -*- coding: utf-8 -*-
"""
UK Year 6 Maths: Order of operations (BODMAS / BIDMAS), National Curriculum in England
  python3 tools/gen_uk_maths_y6_order_of_operations.py
HTML attributes use single quotes (no backslashes in the JSON).
Squares and cubes are written with <sup> in HTML fields and with ² ³ in plain-text fields.

Expressions are written in a small source syntax ("5 + 3 × 4", "(25 + 15) × 3", "3^2 + 4"),
evaluated exactly with fractions.Fraction and cross-checked with Python eval.
Wrong answers come from real mistakes: working strictly left to right, + and − before × and ÷,
ignoring the brackets, multiplying before dividing (48 ÷ 6 × 2 = 4), adding before subtracting
(20 − 8 + 3 = 9), working right to left (20 − 8 − 3 = 15), 3² = 6, stopping one step early.
"""
import json, os, random, re, string
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
BLUE = "#2f6fb0"
FILL = "#cfe6d6"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]

OPEN, CLOSE = ("(",), (")",)
STD = [("^",), ("×", "÷"), ("+", "−")]               # BIDMAS
LTR = [("^", "×", "÷", "+", "−")]                    # mistake: strictly left to right
REV = [("^",), ("+", "−"), ("×", "÷")]               # mistake: + and − before × and ÷
MULFIRST = [("^",), ("×",), ("÷",), ("+", "−")]      # mistake: × before ÷
ADDFIRST = [("^",), ("×", "÷"), ("+",), ("−",)]      # mistake: + before −


# ------------------------------------------------------------ numbers
def f(n):
    """4536 -> 4,536."""
    return "{:,}".format(int(n))


def money(p):
    """Pence below £1, pounds and pence from £1 (whole pounds without .00 from £10)."""
    p = int(p)
    if p < 100:
        return "%dp" % p
    if p % 100 == 0 and p >= 1000:
        return "£" + f(p // 100)
    return "£%s.%02d" % (f(p // 100), p % 100)


# ------------------------------------------------------------ expression engine
TOK = re.compile(r"\d[\d,]*|[×÷+−()^]")


class Calc(Fraction):
    """A number made by an earlier step (not written in the expression)."""


def tokens(s):
    out = [Fraction(t.replace(",", "")) if t[0].isdigit() else t for t in TOK.findall(s)]
    assert "".join(TOK.findall(s)) == s.replace(" ", ""), s
    return out


def render(ts):
    out = ""
    for i, t in enumerate(ts):
        if t == "^":
            continue
        if i > 0 and ts[i - 1] == "^":
            out += "<sup>%d</sup>" % t
            continue
        s = f(t) if isinstance(t, Fraction) else t
        if out and not out.endswith(OPEN) and s not in CLOSE:
            out += " "
        out += s
    return out


def H(s):
    """Source syntax -> HTML."""
    return render(tokens(s))


def P(s):
    """Source syntax -> plain text (² ³)."""
    return re.sub(r"<sup>(\d)</sup>", lambda m: "⁰¹²³⁴⁵⁶⁷⁸⁹"[int(m.group(1))], H(s))


def apply(a, op, b, bxe=False):
    if op == "^":
        if bxe:
            return a * b
        r = a ** int(b)
        return r
    if op == "×":
        return a * b
    if op == "÷":
        if not b:
            return None
        r = a / b
        return r if r.denominator == 1 else None
    if op == "+":
        return a + b
    r = a - b
    return r if r >= 0 else None


def flat_eval(seq, prec, bxe=False, rtl=False):
    seq = list(seq)
    for level in prec:
        if rtl:
            i = len(seq) - 2
            while i >= 1:
                if seq[i] in level:
                    v = apply(seq[i - 1], seq[i], seq[i + 1], bxe)
                    if v is None:
                        return None
                    seq[i - 1:i + 2] = [v]
                i -= 2
        else:
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


def ev_tokens(ts, prec=STD, bxe=False, rtl=False):
    ts = list(ts)
    while True:
        j = next((k for k, t in enumerate(ts) if t in CLOSE), None)
        if j is None:
            return flat_eval(ts, prec, bxe, rtl)
        i = max(k for k in range(j) if ts[k] in OPEN)
        v = flat_eval(ts[i + 1:j], prec, bxe, rtl)
        if v is None:
            return None
        ts[i:j + 1] = [v]


def ev(s, mode="std"):
    ts = tokens(s)
    if mode == "std":
        return ev_tokens(ts)
    if mode == "ltr":
        return ev_tokens(ts, LTR)
    if mode == "rev":
        return ev_tokens(ts, REV)
    if mode == "mulfirst":
        return ev_tokens(ts, MULFIRST)
    if mode == "addfirst":
        return ev_tokens(ts, ADDFIRST)
    if mode == "rtl":
        return ev_tokens(ts, rtl=True)
    if mode == "bxe":
        return ev_tokens(ts, STD, bxe=True)
    if mode == "noparen":
        return ev_tokens([t for t in ts if t not in OPEN + CLOSE])
    raise ValueError(mode)


def py_check(s, v):
    p = []
    for t in tokens(s):
        if isinstance(t, Fraction):
            p.append(str(int(t)))
        else:
            p.append({"^": "**", "×": "*", "÷": "/", "−": "-"}.get(t, t))
    assert Fraction(eval(" ".join(p).replace("/", "*Fraction(1)/"), {"Fraction": Fraction})) == v, (s, v)


def steps(s, values=False):
    """One operation per step, innermost brackets first."""
    ts = tokens(s)
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
        r = render(ts)
        if not out or out[-1] != r:
            out.append(r)
    return made if values else out


def val(s):
    v = ev(s)
    assert v is not None and v > 0 and v.denominator == 1, s
    py_check(s, v)
    return v


def chain(s):
    v = val(s)
    st = steps(s)
    assert st[-1] == f(v), (s, st)
    return " = ".join([H(s)] + st)


def before_last(s):
    m = steps(s, values=True)
    return max(m[-1]) if m and m[-1] else None


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e):
    """correct + the first 3 unique distractors. Positions are set by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or not c or c.startswith("-"):
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
        self.pool = [(x, "she", "her") for x in GIRLS] + [(x, "he", "his") for x in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def B(s):
    return "<b>%s</b>" % s


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


ASK = ["Calculate %s", "What is %s?", "Work out %s", "Find the value of %s"]

WP = "multiplies the wrong pair of numbers"
SIGN = "uses the wrong sign"
PART = "uses only the first number in the brackets"

WHY = {
    "ltr": "comes from working from left to right without using BIDMAS",
    "rev": "comes from adding or subtracting before multiplying or dividing",
    "mulfirst": "comes from multiplying before dividing, but × and ÷ are equals, so work from left to right",
    "addfirst": "comes from adding before subtracting, but + and − are equals, so work from left to right",
    "rtl": "comes from working from right to left",
    "bxe": "comes from multiplying by the small raised number (like 3<sup>2</sup> = 3 × 2) instead of multiplying the number by itself",
    "noparen": "comes from ignoring the brackets",
}


def mistakes(s, modes, extra=()):
    """Wrong values in order of priority: (value, reason). extra = [(expression, reason)]."""
    v = ev(s)
    out, seen = [], {v}

    def add(w, why):
        if w is None or w <= 0 or w in seen or w.denominator != 1:
            return
        seen.add(w)
        out.append((w, why))

    for m in modes:
        add(ev(s, m), WHY[m])
    for x, why in extra:
        add(ev(x), why)
    add(before_last(s), "stops one step too early")
    return out


def eval_item(s, k, modes, extra=(), note=""):
    v = val(s)
    ms = mistakes(s, modes, extra)
    assert len(ms) >= 3, (s, ms)
    w, why = ms[0]
    e = chain(s) + ". " + (note + " " if note else "") + "Not %s: that %s." % (f(w), why)
    return mcq(ASK[k % len(ASK)] % B(H(s)), f(v), [f(x) for x, _ in ms], e)


def fields(t):
    return [x[1] for x in string.Formatter().parse(t) if x[1]]


def templated(rnd, T, used, vmax=200, k0=0, note=""):
    its = []
    for k, (t, modes, extra, mk) in enumerate(T):
        names = fields(t)

        def build(d, t=t, names=names, extra=extra):
            m = dict(zip(names, map(f, d)))
            return t.format(**m), [(x.format(**m), why) for x, why in extra]

        def ok(d, t=t, modes=modes, build=build):
            if len(set(d)) != len(d):
                return False
            s, ex_ = build(d)
            v = ev(s)
            if v is None or v <= 1 or v > vmax or v.denominator != 1:
                return False
            if any(x is not None and x <= 0 for x in [ev(s, "std")]):
                return False
            w0 = ev(s, modes[0])
            if w0 is None or w0 <= 0 or w0 == v or w0.denominator != 1:
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
        its.append(eval_item(s, k + k0, modes, ex_, note))
    return its


def first_item(s, good, bad, why):
    """Which part of s is worked out first?"""
    return mcq("Which part of %s do you work out first?" % B(H(s)), H(good), [H(x) if x[0].isdigit() else x for x in bad],
               "%s. %s" % (chain(s), why))


def who_item(s, a, wa, b, wb):
    """Two pupils give answers; which of them is right?"""
    v = val(s)
    ra, rb = (wa == v), (wb == v)
    good = "Both" if ra and rb else ("Only " + a if ra else ("Only " + b if rb else "Neither"))
    assert not (ra and rb)
    e = chain(s) + "."
    for n, w in ((a, wa), (b, wb)):
        if w != v:
            why = next(why for m, why in WHY.items() if ev(s, m) == w) if any(ev(s, m) == w for m in WHY) else None
            assert why, (s, w)
            e += " %s’s answer of %s %s." % (n, f(w), why)
    if not ra and not rb:
        e += " So neither of them is right."
    return mcq("%s says %s = %s. %s says it is %s. Who is right?" % (a, B(H(s)), f(wa), b, f(wb)),
               good, ["Only " + a, "Only " + b, "Both", "Neither"], e)


# ------------------------------------------------------------ set 1: × and ÷ before + and −
def set_precedence(rnd, Pp):
    R = rnd.randint
    used = set()
    T = [
        ("{a} + {b} × {c}", ["ltr"], [("{a} × {b} + {c}", WP)], lambda r: (R(2, 9), R(2, 9), R(2, 9))),
        ("{a} + {b} × {c}", ["ltr"], [("{a} × {b} + {c}", WP)], lambda r: (R(11, 40), R(3, 12), R(3, 12))),
        ("{a} − {b} × {c}", ["ltr"], [("{a} × {b} − {c}", WP), ("{a} + {b} × {c}", SIGN)], lambda r: (R(40, 90), R(2, 9), R(2, 6))),
        ("{a} × {b} + {c}", ["rev"], [("{a} + {b} × {c}", WP), ("{a} × {b} − {c}", SIGN)], lambda r: (R(2, 9), R(3, 9), R(2, 9))),
        ("{a} × {b} − {c}", ["rev"], [("{a} − {b} × {c}", WP), ("{a} × {b} + {c}", SIGN)], lambda r: (R(4, 12), R(5, 12), R(2, 4))),
        ("{a} + {b} ÷ {c}", ["ltr"], [("{a} − {b} ÷ {c}", SIGN), ("{a} + {b} × {c}", "multiplies instead of dividing")], lambda r: (lambda c, q: (R(4, 30), c * q, c))(R(2, 9), R(2, 9))),
        ("{a} − {b} ÷ {c}", ["ltr"], [("{a} + {b} ÷ {c}", SIGN), ("{a} − {b} × {c}", "multiplies instead of dividing")], lambda r: (lambda c, q: (R(20, 60), c * q, c))(R(2, 9), R(2, 9))),
        ("{a} ÷ {b} + {c}", ["rev"], [("{a} ÷ {b} − {c}", SIGN), ("{a} × {b} + {c}", "multiplies instead of dividing")], lambda r: (lambda b, q: (b * q, b, R(2, 9)))(R(2, 6), R(4, 12))),
        ("{a} ÷ {b} − {c}", ["rev"], [("{a} ÷ {b} + {c}", SIGN)], lambda r: (lambda b, q: (b * q, b, R(2, 8)))(R(2, 6), R(10, 20))),
        ("{a} + {b} × {c} − {d}", ["ltr", "rev"], [], lambda r: (R(2, 20), R(3, 9), R(3, 9), R(2, 9))),
        ("{a} × {b} + {c} × {d}", ["ltr", "rev"], [], lambda r: (R(2, 9), R(2, 9), R(2, 9), R(2, 9))),
        ("{a} × {b} − {c} × {d}", ["ltr", "rev"], [], lambda r: (R(6, 12), R(6, 12), R(2, 6), R(2, 6))),
        ("{a} − {b} ÷ {c} + {d}", ["ltr", "rev"], [], lambda r: (lambda c, q: (R(20, 50), c * q, c, R(2, 9)))(R(2, 9), R(2, 9))),
        ("{a} + {b} × {c}", ["ltr"], [("{a} × {c} + {b}", WP)], lambda r: (R(1, 9) * 100, R(2, 9) * 10, R(2, 9))),
        ("{a} ÷ {b} + {c} × {d}", ["ltr", "rev"], [], lambda r: (lambda b, q: (b * q, b, R(2, 9), R(2, 9)))(R(2, 9), R(2, 9))),
        ("{a} − {b} × {c} + {d}", ["ltr", "rev"], [], lambda r: (R(50, 99), R(3, 9), R(3, 9), R(2, 20))),
    ]
    its = templated(rnd, T, used, vmax=1000)
    its.append(first_item("4 + 6 × 3", "6 × 3", ["4 + 6", "Either part", "Neither"], "Multiply before you add."))
    its.append(first_item("40 − 30 ÷ 5", "30 ÷ 5", ["40 − 30", "Either part", "Neither"], "Divide before you subtract."))
    assert val("7 + 2 × 5") == 17
    its.append(mcq("Which calculation is correct?", "7 + 2 × 5 = 17", ["7 + 2 × 5 = 45", "7 + 2 × 5 = 10", "7 + 2 × 5 = 19"],
                   "7 + 2 × 5 = 7 + 10 = 17. 45 comes from adding first. 10 stops after 2 × 5. 19 is 7 × 2 + 5, the wrong pair."))
    assert val("7 × 2 + 5") == 19 and val("(7 + 2) × 5") == 45
    assert val("18 − 12 ÷ 3") == 14 and val("(18 − 12) ÷ 3") == 2
    its.append(mcq("Which calculation is correct?", "18 − 12 ÷ 3 = 14", ["18 − 12 ÷ 3 = 2", "18 − 12 ÷ 3 = 22", "18 − 12 ÷ 3 = 6"],
                   "18 − 12 ÷ 3 = 18 − 4 = 14. 2 comes from subtracting first. 22 adds the 4 instead of subtracting it. 6 is just 18 − 12."))
    assert val("18 ÷ 3 − 1") == 5
    assert len(its) == 20, len(its)
    return {"title": "Multiply and divide before you add and subtract", "items": its}


# ------------------------------------------------------------ set 2: brackets first
def set_brackets(rnd, Pp):
    R = rnd.randint
    used = set()
    T = [
        ("({a} + {b}) × {c}", ["noparen"], [("{a} × {c} + {b}", PART)], lambda r: (R(1, 9) * 5, R(1, 9) * 5, R(2, 5))),
        ("({a} + {b}) × {c}", ["noparen"], [("{a} × {c} + {b}", PART)], lambda r: (R(2, 9), R(2, 9), R(2, 9))),
        ("{a} × ({b} − {c})", ["noparen"], [("{a} × ({b} + {c})", SIGN)], lambda r: (R(3, 9), R(10, 20), R(2, 8))),
        ("{a} × ({b} + {c})", ["noparen"], [("{a} × ({b} − {c})", SIGN)], lambda r: (R(3, 9), R(2, 9), R(2, 9))),
        ("({a} − {b}) × {c}", ["noparen"], [("{a} × {c} − {b}", PART)], lambda r: (R(30, 60), R(2, 9), R(2, 5))),
        ("({a} + {b}) ÷ {c}", ["noparen"], [("({a} + {b}) × {c}", "multiplies instead of dividing")], lambda r: (lambda c, t: (lambda a: (a, c * t - a, c))(R(2, c * t - 2)))(R(3, 9), R(3, 9))),
        ("({a} − {b}) ÷ {c}", ["noparen"], [("({a} + {b}) ÷ {c}", SIGN)], lambda r: (lambda c, t, b: (c * t + b, b, c))(R(3, 9), R(3, 9), R(2, 9))),
        ("{a} − ({b} + {c})", ["noparen"], [("{a} + {b} + {c}", "adds all three numbers")], lambda r: (R(40, 90), R(5, 20), R(5, 20))),
        ("{a} ÷ ({b} − {c})", ["noparen"], [("{a} ÷ ({b} + {c})", SIGN)], lambda r: (lambda c, d, q: (d * q, c + d, c))(R(2, 9), R(2, 9), R(2, 9))),
        ("{a} ÷ ({b} × {c})", ["noparen"], [("{a} ÷ ({b} + {c})", "adds instead of multiplying in the brackets")], lambda r: (lambda b, c, q: (b * c * q, b, c))(R(2, 5), R(2, 5), R(2, 9))),
        ("{a} + ({b} − {c}) × {d}", ["noparen", "ltr"], [], lambda r: (R(2, 20), R(8, 15), R(2, 6), R(2, 6))),
        ("({a} + {b}) × ({c} − {d})", ["noparen"], [("{a} + {b} × ({c} − {d})", "ignores the first pair of brackets"), ("({a} + {b}) × {c} − {d}", "ignores the second pair of brackets")], lambda r: (R(2, 9), R(2, 9), R(8, 15), R(2, 6))),
        ("{a} × ({b} + {c}) − {d}", ["noparen"], [("{a} × ({b} + {c} − {d})", "puts the − {d} inside the brackets"), ("{a} × {c} + {b} − {d}", PART)], lambda r: (R(2, 6), R(2, 9), R(2, 9), R(2, 9))),
        ("{a} − {b} × ({c} − {d})", ["noparen", "ltr"], [], lambda r: (R(50, 99), R(2, 6), R(6, 12), R(2, 5))),
        ("({a} − {b}) ÷ ({c} + {d})", ["noparen"], [("({a} − {b}) ÷ {c} + {d}", "ignores the second pair of brackets"), ("{a} − {b} ÷ ({c} + {d})", "ignores the first pair of brackets")], lambda r: (lambda c, d, q, b: ((c + d) * q + b, b, c, d))(R(2, 5), R(2, 5), R(2, 9), R(2, 20))),
        ("{a} × ({b} + {c} × {d})", ["noparen", "ltr"], [], lambda r: (R(2, 5), R(2, 9), R(2, 6), R(2, 6))),
    ]
    its = templated(rnd, T, used, vmax=1000, k0=1)
    its.append(first_item("(9 − 4) × 6", "9 − 4", ["4 × 6", "Either part", "Neither"],
                          "Brackets come first, even though × usually comes before −."))
    its.append(first_item("50 − (12 + 8) × 2", "12 + 8", ["50 − 12", "8 × 2", "Either part"],
                          "Brackets first, then ×, then −."))
    v = val("6 + 4 × 5")
    alts = {"6 + (4 × 5)": v, "(6 + 4) × 5": val("(6 + 4) × 5"), "6 × (4 + 5)": val("6 × (4 + 5)"), "6 × 4 + 5": val("6 × 4 + 5")}
    assert len(set(alts.values())) == 4
    its.append(mcq("Which calculation has the same value as %s?" % B(H("6 + 4 × 5")), H("6 + (4 × 5)"),
                   [H("(6 + 4) × 5"), H("6 × (4 + 5)"), H("6 × 4 + 5")],
                   "6 + 4 × 5 = 6 + 20 = 26. The brackets in 6 + (4 × 5) show what you do first anyway, so the value stays 26. "
                   "(6 + 4) × 5 = 50, 6 × (4 + 5) = 54 and 6 × 4 + 5 = 29."))
    vs = {x: val(x) for x in ["(7 × 4) + 2", "7 × 4 + 2", "2 + 7 × 4", "7 × (4 + 2)"]}
    assert vs["7 × (4 + 2)"] == 42 and len({vs[k] for k in vs if k != "7 × (4 + 2)"}) == 1 and vs["7 × 4 + 2"] == 30
    its.append(mcq("Which calculation has a <b>different</b> value from the others?", H("7 × (4 + 2)"),
                   [H("(7 × 4) + 2"), H("7 × 4 + 2"), H("2 + 7 × 4")],
                   "7 × (4 + 2) = 7 × 6 = 42. The other three all equal 7 × 4 + 2 = 28 + 2 = 30, because × is done before + anyway."))
    assert len(its) == 20, len(its)
    return {"title": "Brackets first", "items": its}


# ------------------------------------------------------------ set 3: left to right, and squares
def set_ltr(rnd, Pp):
    R = rnd.randint
    used = set()
    T = [
        ("{a} ÷ {b} × {c}", ["mulfirst"], [("{a} ÷ {b} + {c}", "adds the last number instead of multiplying")],
         lambda r: (lambda b, c, q: (b * c * q, b, c))(R(2, 6), R(2, 5), R(2, 5))),
        ("{a} − {b} + {c}", ["addfirst"], [("{a} + {b} + {c}", "adds all three numbers")],
         lambda r: (R(15, 40), R(5, 12), R(2, 6))),
        ("{a} − {b} − {c}", ["rtl"], [("{a} + {b} + {c}", "adds all three numbers")],
         lambda r: (R(20, 50), R(6, 15), R(2, 5))),
        ("{a} ÷ {b} ÷ {c}", ["rtl"], [("{a} ÷ ({b} + {c})", "comes from adding {b} and {c}; dividing by {b} then by {c} is the same as dividing by {b} × {c}")],
         lambda r: (lambda b, c, q: (b * c * q, b, c))(R(2, 5), R(2, 5), R(2, 6))),
        ("{a} ÷ {b} × {c}", ["mulfirst"], [("{a} ÷ {b} + {c}", "adds the last number instead of multiplying")],
         lambda r: (lambda b, c, q: (b * c * q * 10, b, c))(R(2, 5), R(2, 5), R(1, 3))),
        ("{a} − {b} + {c}", ["addfirst"], [("{a} + {b} + {c}", "adds all three numbers")],
         lambda r: (R(10, 30) * 10, R(5, 15) * 10, R(2, 9) * 10)),
        ("{a} + {b} ÷ {c} × {d}", ["mulfirst", "ltr", "rev"], [], lambda r: (lambda c, d, q: (R(2, 20), c * d * q, c, d))(R(2, 5), R(2, 5), R(1, 4))),
        ("{a} − {b} + {c} × {d}", ["addfirst", "ltr"], [], lambda r: (R(20, 50), R(5, 15), R(2, 6), R(2, 6))),
        ("{a} × {b} ÷ {c} − {d}", ["rev", "mulfirst"], [("{a} × {b} − {d}", "forgets to divide")],
         lambda r: (lambda c, q: (c * q, R(2, 6), c, R(2, 9)))(R(2, 6), R(2, 6))),
        ("{a} − {b} − {c} + {d}", ["rtl", "addfirst"], [], lambda r: (R(40, 80), R(10, 20), R(5, 12), R(2, 9))),
        ("{a} + {b}^2", ["bxe"], [("({a} + {b})^2", "comes from adding before squaring")], lambda r: (R(2, 20), R(3, 9))),
        ("{a} × {b}^2", ["ltr", "bxe"], [], lambda r: (R(2, 5), R(3, 6))),
        ("{a}^2 − {b} × {c}", ["ltr", "bxe"], [], lambda r: (R(6, 10), R(2, 5), R(2, 6))),
        ("({a} + {b})^2", ["noparen", "bxe"], [], lambda r: (R(2, 6), R(2, 6))),
        ("{a}^3 + {b}", ["bxe"], [("{a}^2 + {b}", "squares instead of cubing")], lambda r: (R(2, 5), R(2, 20))),
        ("{a}^2 + {b}^2", ["bxe"], [("({a} + {b})^2", "comes from adding before squaring")], lambda r: (R(2, 9), R(2, 9))),
    ]
    its = templated(rnd, T, used, vmax=500, k0=2)
    its.append(first_item("48 ÷ 6 × 2", "48 ÷ 6", ["6 × 2", "Either part", "Neither"],
                          "÷ and × are equals, so work from left to right. Doing 6 × 2 first gives 48 ÷ 12 = 4, which is wrong."))
    its.append(first_item("20 − 8 + 3", "20 − 8", ["8 + 3", "Either part", "Neither"],
                          "+ and − are equals, so work from left to right. Doing 8 + 3 first gives 20 − 11 = 9, which is wrong."))
    assert val("3^2") == 9
    its.append(mcq("What is %s (3 squared)?" % B(H("3^2")), "9", ["6", "5", "27"],
                   "3<sup>2</sup> = 3 × 3 = 9. Not 6: that is 3 × 2. Not 5: that is 3 + 2. 27 is 3 cubed, 3<sup>3</sup>."))
    its.append(mcq("Which means the same as %s?" % B(H("6^2")), "6 × 6", ["6 × 2", "6 + 6", "2 × 2 × 2 × 2 × 2 × 2"],
                   "6 squared means 6 × 6 = 36. It is not 6 × 2 = 12 or 6 + 6 = 12."))
    assert len(its) == 20, len(its)
    return {"title": "Left to right, and squares", "items": its}


# ------------------------------------------------------------ set 4: place the brackets; large numbers
def brackets_item(plain, target_expr, others):
    v = val(target_expr)
    assert tokens(plain) == [t for t in tokens(target_expr) if t not in OPEN + CLOSE]
    vals = [val(x) for x in others]
    assert len(set(vals + [v])) == 4, (plain, vals, v)
    pv = val(plain)
    assert pv != v
    return mcq("Where do the brackets go to make this true?<br>%s" % B("%s = %s" % (H(plain), f(v))),
               H(target_expr), [H(x) for x in others],
               "%s. Without brackets, %s = %s." % (chain(target_expr), H(plain), f(pv)))


def which_item(good, bad):
    v = val(good)
    vals = [val(x) for x in bad]
    assert len(set(vals + [v])) == 4, (good, vals)
    e = "%s. The others: %s." % (chain(good), "; ".join("%s = %s" % (H(x), f(val(x))) for x in bad))
    return mcq("Which calculation has a value of %s?" % B(f(v)), H(good), [H(x) for x in bad], e)


def set_brackets_large(rnd, Pp):
    its = []
    its.append(brackets_item("6 + 4 × 5 − 2", "(6 + 4) × 5 − 2", ["6 + 4 × (5 − 2)", "(6 + 4) × (5 − 2)", "6 + (4 × 5 − 2)"]))
    its.append(brackets_item("40 − 10 ÷ 2 + 3", "(40 − 10) ÷ 2 + 3", ["40 − 10 ÷ (2 + 3)", "(40 − 10) ÷ (2 + 3)", "40 − (10 ÷ 2 + 3)"]))
    its.append(brackets_item("7 × 8 − 3 + 2", "7 × (8 − 3 + 2)", ["7 × (8 − 3) + 2", "7 × 8 − (3 + 2)", "(7 × 8 − 3) + 2"]))
    its.append(brackets_item("8 × 7 − 2 × 3", "8 × (7 − 2) × 3", ["8 × (7 − 2 × 3)", "(8 × 7 − 2) × 3", "(8 × 7) − (2 × 3)"]))
    its.append(brackets_item("72 ÷ 6 + 2 × 3", "72 ÷ (6 + 2) × 3", ["72 ÷ (6 + 2 × 3)", "(72 ÷ 6 + 2) × 3", "72 ÷ 6 + (2 × 3)"]))
    its.append(brackets_item("100 − 30 − 20 + 10", "100 − 30 − (20 + 10)", ["100 − (30 − 20) + 10", "(100 − 30) − 20 + 10", "100 − (30 − 20 + 10)"]))
    its.append(which_item("(4 + 6) × 5", ["4 + 6 × 5", "4 × 6 + 5", "4 × (6 + 5)"]))
    its.append(which_item("60 ÷ 5 × 2", ["60 ÷ (5 × 2)", "60 ÷ 5 + 2", "60 − 5 × 2"]))
    its.append(which_item("20 − 8 − 3", ["20 − (8 − 3)", "(20 − 8) ÷ 3", "20 ÷ 2 − 3"]))
    its.append(which_item("6^2 + 8^2", ["(6 + 8)^2", "6 × 2 + 8 × 2", "6^2 + 8 × 2"]))
    its.append(which_item("4,000 ÷ 8 × 2", ["4,000 ÷ (8 × 2)", "4,000 ÷ 8 + 2", "4,000 − 8 × 200"]))
    note = "Use known facts: think in thousands."
    its.append(eval_item("25,000 − 4 × 3,000", 0, ["ltr"], [("25,000 − 3,000", "leaves out the × 4")], note))
    its.append(eval_item("2,400 + 6,000 ÷ 3", 1, ["ltr"], [("2,400 + 6,000", "forgets to divide by 3")]))
    its.append(eval_item("(4,500 + 3,500) × 7", 2, ["noparen"], [("4,500 + 3,500", "forgets to multiply by 7"), ("4,500 × 7 + 3,500", "multiplies only the first number in the brackets")]))
    its.append(eval_item("8,000 + 120,000 ÷ 4", 3, ["ltr"], [("8,000 + 120,000 ÷ 40", "divides by 40, not 4: check the zeros")]))
    its.append(eval_item("900 × 30 + 1,500", 0, ["rev"], [("900 × 3 + 1,500", "forgets the zero in 30")]))
    names = [Pp.next()[0] for _ in range(8)]
    its.append(who_item("48 ÷ 6 × 2", names[0], ev("48 ÷ 6 × 2", "mulfirst"), names[1], val("48 ÷ 6 × 2")))
    its.append(who_item("20 − 8 + 3", names[2], val("20 − 8 + 3"), names[3], ev("20 − 8 + 3", "addfirst")))
    its.append(who_item("(25 + 15) × 3", names[4], val("(25 + 15) × 3"), names[5], ev("(25 + 15) × 3", "noparen")))
    its.append(who_item("5 + 3 × 4 − 2", names[6], ev("5 + 3 × 4 − 2", "ltr"), names[7], ev("5 + 3 × 4 − 2", "rev")))
    assert len(its) == 20, len(its)
    return {"title": "Place the brackets, and mental calculation with large numbers", "items": its}


# ------------------------------------------------------------ set 5: estimation and word problems
def set_words(rnd, Pp):
    its = []

    def add(q, good, bad, e):
        its.append(mcq(q, good, bad, e))

    # estimation
    assert 4987 * 21 == 104727
    add("Which is the best estimate for %s?" % B("4,987 × 21"), "100,000", ["10,000", "1,000,000", "150,000"],
        "Round each number: 4,987 ≈ 5,000 and 21 ≈ 20. 5,000 × 20 = 100,000. (The exact answer is 104,727.) "
        "10,000 and 1,000,000 have the wrong number of zeros. 150,000 rounds 21 to 30.")
    assert 6213 - 2890 == 3323
    add("Which is the best estimate for %s?" % B("6,213 − 2,890"), "3,000", ["9,000", "4,000", "300"],
        "6,213 ≈ 6,000 and 2,890 ≈ 3,000. 6,000 − 3,000 = 3,000. (The exact answer is 3,323.) "
        "9,000 adds instead of subtracting. 4,000 rounds 2,890 down to 2,000.")
    assert round(7820 / 39) == 201
    add("Which is the best estimate for %s?" % B("7,820 ÷ 39"), "200", ["2,000", "20", "160"],
        "7,820 ≈ 8,000 and 39 ≈ 40. 8,000 ÷ 40 = 800 ÷ 4 = 200. (The exact answer is about 200.5.) "
        "2,000 and 20 have the wrong number of zeros. 160 rounds 39 to 50.")
    n1, he, his = Pp.next()
    assert 398 * 52 == 20696
    add("%s works out 398 × 52 and gets 2,696. Use an estimate to check. What do you find?" % n1,
        "It is wrong: the answer should be about 20,000",
        ["It is right: the answer should be about 2,000", "It is wrong: the answer should be about 200,000",
         "It is right: the answer should be about 2,500"],
        "398 ≈ 400 and 52 ≈ 50. 400 × 50 = 20,000, so 2,696 is far too small. (The exact answer is 20,696; "
        "%s has missed a zero when multiplying by the 5 tens.)" % n1)
    assert 21 * 49 == 1029 and 22 * 49 >= 1030
    add("1,030 people are going to a concert by coach. Each coach has 49 seats. How many coaches are needed?",
        "22 coaches", ["21 coaches", "21 r 1 coaches", "20 coaches"],
        "1,030 ÷ 49 = 21 remainder 1. 21 coaches carry 1,029 people, so 1 person still needs a seat. "
        "Round up: 22 coaches. 20 comes from the estimate 1,000 ÷ 50, which is not accurate enough here.")
    assert 495 + 210 + 699 == 1404
    n2, he2, his2 = Pp.next()
    add("%s buys a book for £4.95, a pen for £2.10 and a game for £6.99. About how much does %s spend?" % (n2, he2),
        "About £14", ["About £12", "About £15", "About £140"],
        "Round to the nearest pound: £5 + £2 + £7 = £14. (The exact total is £14.04.) "
        "£12 just drops the pence. £15 rounds every price up. £140 is ten times too big.")
    assert 200 // 6 == 33 and 200 % 6 == 2
    add("A café needs 200 eggs. Eggs come in boxes of 6. How many boxes must the café buy?",
        "34 boxes", ["33 boxes", "33 r 2 boxes", "33.3 boxes"],
        "200 ÷ 6 = 33 remainder 2. 33 boxes hold only 198 eggs, so the café needs one more box: 34 boxes. "
        "You cannot buy part of a box, so 33 r 2 and 33.3 do not make sense here.")
    # word problems written as one calculation
    s = "3 × 85 + 240"
    assert val(s) == 495 and ev("3 × (85 + 240)") == 975
    n, he, his = Pp.next()
    add("%s buys 3 drinks at 85p each and a sandwich at £2.40. How much does %s spend?" % (n, he),
        money(495), [money(975), money(325), money(255)],
        "Write it as one calculation in pence: %s, so 495p = £4.95. Multiply first. "
        "£9.75 is 3 × (85 + 240), which buys 3 sandwiches. £3.25 buys only one drink. £2.55 forgets the sandwich." % chain(s))
    n, he, his = Pp.next()
    v = val("4 × 6 + 3")
    assert v == 27 and len({v, val("4 × (6 + 3)"), val("(4 + 3) × 6"), val("4 + 6 × 3")}) == 4
    add("%s buys 4 packs of 6 pens and 3 single pens. Which calculation gives the number of pens?" % n,
        H("4 × 6 + 3"), [H("4 × (6 + 3)"), H("(4 + 3) × 6"), H("4 + 6 × 3")],
        "4 packs of 6 is 4 × 6, then add the 3 single pens: 4 × 6 + 3 = 24 + 3 = 27. "
        "4 × (6 + 3) = 36 would mean 4 packs of 9.")
    s = "2 × 9 + 3 × 6"
    assert val(s) == 36 and ev(s, "ltr") == 126 and val("(2 + 3) × (9 + 6)") == 75
    add("Cinema tickets cost £9 for an adult and £6 for a child. How much do 2 adults and 3 children pay?",
        "£36", ["£126", "£75", "£18"],
        "%s, so £36. Do both multiplications before adding. £126 comes from working left to right. "
        "£75 is 5 × £15. £18 is only the adults." % chain(s))
    s = "30 × 4 + 85"
    assert val(s) == 205 and val("30 × (4 + 85)") == 2670
    add("30 pupils each pay £4 for a museum trip. The school adds £85. How much money is there altogether?",
        "£205", ["£2,670", "£119", "£120"],
        "%s, so £205. £2,670 is 30 × (4 + 85): the £85 is added once, not for every pupil. "
        "£119 adds all three numbers. £120 forgets the school’s £85." % chain(s))
    s = "500 − 8 × 25"
    assert val(s) == 300 and ev(s, "ltr") == 12300
    n, he, his = Pp.next()
    add("%s has 500 stickers. %s gives 25 stickers to each of 8 friends. How many stickers does %s have left?" % (n, he.capitalize(), he),
        "300", ["12,300", "475", "200"],
        "%s. Multiply first. 12,300 comes from working left to right. 475 gives stickers to only one friend. "
        "200 is the number given away." % chain(s))
    vals = {x: ev(x) for x in ["(18 + 14) ÷ 4", "18 + 14 ÷ 4", "18 ÷ 4 + 14", "4 × (18 + 14)"]}
    assert vals["(18 + 14) ÷ 4"] == 8
    add("A class has 18 boys and 14 girls. They sit in groups of 4. Which calculation gives the number of groups?",
        H("(18 + 14) ÷ 4"), [H("18 + 14 ÷ 4"), H("18 ÷ 4 + 14"), H("4 × (18 + 14)")],
        "Find the whole class first, then divide by 4: (18 + 14) ÷ 4 = 32 ÷ 4 = 8 groups. "
        "Without brackets, 18 + 14 ÷ 4 would divide only the girls.")
    s = "2,000 − 2 × 650"
    assert val(s) == 700 and ev(s, "ltr") == 1998 * 650
    n, he, his = Pp.next()
    add("%s has £20. %s buys 2 books at £6.50 each. How much change does %s get?" % (n, he.capitalize(), he),
        money(700), ["£117.00", "£13.50", "£11.50"],
        "In pence: %s, so £7.00. Multiply before subtracting. £117.00 comes from working left to right: (20 − 2) × 6.50. £13.50 pays for only one book. "
        "£11.50 comes from 20 − 2 − 6.50." % chain(s))
    assert ev("2,000 − 2 − 650") == 1348 and (20 - 2) * 650 == 11700
    s = "45,000 − 8 × 3,500"
    assert val(s) == 17000
    add("A stadium has 45,000 seats. 8 stands of 3,500 seats are full and every other seat is empty. How many seats are empty?",
        "17,000", ["41,500", "28,000", "73,000"],
        "%s. 8 × 3,500 = 8 × 35 hundreds = 280 hundreds = 28,000. 41,500 counts only one stand. "
        "28,000 is the number of full seats. 73,000 adds instead of subtracting." % chain(s))
    s = "1,250 × 20 + 5,000"
    assert val(s) == 30000 and ev(s, "rev") == 1250 * 5020
    add("1,250 runners each raise £20 for charity. A local business gives another £5,000. How much is raised altogether?",
        "£30,000", ["£25,000", "£6,270", "£3,000"],
        "%s, so £30,000. £25,000 forgets the £5,000 gift. £6,270 adds all three numbers. "
        "£3,000 has a zero missing." % chain(s))
    s = "12 × 8 − 4^2"
    assert val(s) == 80 and ev(s, "bxe") == 88
    add("A rectangular garden is 12 m by 8 m. A square patio with 4 m sides is laid in it. What area of the garden is left?",
        "80 m²", ["88 m²", "92 m²", "96 m²"],
        "Area of garden − area of patio: %s m². 88 m² uses 4<sup>2</sup> = 8 instead of 16. "
        "92 m² takes away only 4. 96 m² forgets the patio." % chain(s))
    s = "6^2 − 5"
    assert val(s) == 31 and ev(s, "bxe") == 7
    add("A square patio is 6 slabs long and 6 slabs wide. 5 of the slabs are cracked. How many slabs are not cracked?",
        "31", ["7", "36", "41"],
        "%s. 7 uses 6<sup>2</sup> = 12 instead of 36. 36 forgets the cracked slabs. 41 adds instead of subtracting." % chain(s))
    s = "96 ÷ 4 ÷ 2"
    assert val(s) == 12 and ev(s, "rtl") == 48 and val("96 ÷ (4 + 2)") == 16
    add("96 pencils are shared equally between 4 tables. Each table shares its pencils equally between 2 pupils. "
        "How many pencils does each pupil get?",
        "12", ["48", "24", "16"],
        "%s. 48 comes from working out 4 ÷ 2 first. 24 is the number for each table. 16 divides by 4 + 2 = 6." % chain(s))
    s = "2,400 + 30 × 20"
    assert val(s) == 3000 and ev(s, "ltr") == 48600
    add("At a cake sale, the cupcakes raise £24. Then 30 cookies are sold at 20p each. How much is raised altogether?",
        "£30", ["£486", "£3", "£24"],
        "In pence: £24 = 2,400p, and %s, so 3,000p = £30. Multiply before adding. £486 comes from working left to right. "
        "£3 has the place value wrong. £24 forgets the cookies." % chain(s))
    assert len(its) == 20, len(its)
    return {"title": "Estimate, then solve word problems", "items": its}


# ------------------------------------------------------------ lesson
def steps_svg(rows, label, W=330):
    """rows: (list of parts, note). A part is text or (text, colour)."""
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


def bidmas_svg():
    """Four boxes in order: B, I, DM, AS."""
    boxes = [("B", "Brackets"), ("I", "Indices"), ("D M", "÷ × left to right"), ("A S", "+ − left to right")]
    bw, bh, gap = 150, 64, 26
    W = 4 * bw + 3 * gap + 8
    out = ["<defs><marker id='ar' viewBox='0 0 10 10' refX='8' refY='5' markerWidth='6' markerHeight='6' orient='auto'>"
           "<path d='M0 0 L10 5 L0 10 z' fill='%s'/></marker></defs>" % GREEN]
    for i, (big, small) in enumerate(boxes):
        x = 4 + i * (bw + gap)
        out.append("<rect x='%d' y='4' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>" % (x, bw, bh, FILL, GREEN))
        out.append("<text x='%d' y='32' font-size='22' font-weight='700' fill='%s' text-anchor='middle'>%s</text>" % (x + bw // 2, GREEN, big))
        out.append("<text x='%d' y='56' font-size='15' fill='%s' text-anchor='middle'>%s</text>" % (x + bw // 2, INK, small))
        if i < 3:
            out.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2' marker-end='url(#ar)'/>"
                       % (x + bw + 3, 4 + bh // 2, x + bw + gap - 3, 4 + bh // 2, GREEN))
    return svg_wrap(W, bh + 8, "".join(out), "BIDMAS: brackets, then indices, then division and multiplication, then addition and subtraction")


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    assert val("5 + 3 × 4") == 17 and val("(25 + 15) × 3") == 120 and val("48 ÷ 6 × 2") == 16
    assert val("20 − 8 + 3") == 15 and val("3^2 + 4") == 13 and val("3 × 85 + 240") == 495
    fig1 = steps_svg([(["5 + ", ("3 × 4", RED)], "multiply first"),
                      ([("5 + 12", RED)], "then add"),
                      ([("17", GREEN)], "")], "working out 5 plus 3 times 4 step by step")
    fig2 = steps_svg([([("48 ÷ 6", RED), " × 2"], "left to right"),
                      ([("8 × 2", RED)], ""),
                      ([("16", GREEN)], "")], "working out 48 divided by 6 times 2 from left to right")
    return (
        "<h2>Why the order matters</h2>"
        "<p>A calculation with more than one operation can give different answers if people work in a different order. "
        "So everyone uses the same order. In England it is often called <b>BODMAS</b> or <b>BIDMAS</b>.</p>"
        "<figure class='sn-fig'>" + bidmas_svg() +
        "<figcaption>Brackets, then Indices (or Orders: squares and cubes), then Division and Multiplication, "
        "then Addition and Subtraction.</figcaption></figure>" +
        table(["Step", "Do this", "Example"], [
            ["1", "<b>B</b>rackets", "(25 + 15) × 3 = 40 × 3 = 120"],
            ["2", "<b>I</b>ndices: squares and cubes", "3<sup>2</sup> + 4 = 9 + 4 = 13"],
            ["3", "<b>D</b>ivision and <b>M</b>ultiplication, as equals, from left to right", "48 ÷ 6 × 2 = 8 × 2 = 16"],
            ["4", "<b>A</b>ddition and <b>S</b>ubtraction, as equals, from left to right", "20 − 8 + 3 = 12 + 3 = 15"],
        ]) +
        "<p>D comes before M in the word, but they are <b>equals</b>. Do whichever comes first from the left. "
        "A and S work the same way.</p>"
        "<h2>Worked examples</h2>"
        "<figure class='sn-fig'>" + fig1 +
        "<figcaption>5 + 3 × 4: multiply before you add, so the answer is 17, not 32.</figcaption></figure>" +
        ex("Brackets first", "Calculate (25 + 15) × 3.", chain("(25 + 15) × 3") + ". Without the brackets, 25 + 15 × 3 = 25 + 45 = 70.", "120") +
        "<figure class='sn-fig'>" + fig2 +
        "<figcaption>48 ÷ 6 × 2: ÷ and × are equals, so go from left to right.</figcaption></figure>" +
        ex("Squares", "Calculate 3<sup>2</sup> + 4.", "3<sup>2</sup> means 3 × 3 = 9 (not 3 × 2). So 3<sup>2</sup> + 4 = 9 + 4 = 13.", "13") +
        ex("One calculation for a word problem", "3 drinks cost 85p each and a sandwich costs £2.40. What is the total?",
           "Write it in pence: 3 × 85 + 240 = 255 + 240 = 495p.", "£4.95") +
        "<h2>Estimate to check</h2>"
        "<p>Round each number to make an easy calculation. 4,987 × 21 is about 5,000 × 20 = 100,000. "
        "If your answer is near 10,000 or 1,000,000, check it again. In a problem, think about what the answer means: "
        "if 1,030 people travel on coaches with 49 seats, 1,030 ÷ 49 = 21 r 1, so 22 coaches are needed.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["5 + 3 × 4 = 8 × 4 = 32", "Multiply first: 5 + 12 = 17"],
            ["48 ÷ 6 × 2 = 48 ÷ 12 = 4", "÷ and × are equals: left to right, 8 × 2 = 16"],
            ["20 − 8 + 3 = 20 − 11 = 9", "+ and − are equals: left to right, 12 + 3 = 15"],
            ["3<sup>2</sup> = 3 × 2 = 6", "3<sup>2</sup> = 3 × 3 = 9"],
            ["(25 + 15) × 3 = 25 + 45 = 70", "Work out the brackets first: 40 × 3 = 120"],
        ])
    )


FAQ = [
    {"q": "What is BODMAS or BIDMAS?",
     "a": "It is a way to remember the order of operations: Brackets, Orders or Indices (squares and cubes), Division and Multiplication, then Addition and Subtraction. For example, 5 + 3 × 4 = 5 + 12 = 17."},
    {"q": "Do you always divide before you multiply in BIDMAS?",
     "a": "No. Division and multiplication are equals, so you work from left to right. 48 ÷ 6 × 2 = 8 × 2 = 16. Addition and subtraction work the same way: 20 − 8 + 3 = 15."},
    {"q": "Is the order of operations in the Year 6 SATs?",
     "a": "Yes. It is part of the Year 6 National Curriculum, so calculations such as (25 + 15) × 3 or 500 + 7 × 20 can appear in the arithmetic paper (Paper 1) and in reasoning questions."},
    {"q": "How do you use estimation to check an answer?",
     "a": "Round each number so the calculation is easy, then compare. 4,987 × 21 is about 5,000 × 20 = 100,000, so an answer like 10,473 must be wrong."},
]


def gen():
    rnd = random.Random(6604)
    Pp = People(rnd)
    sets = [set_precedence(rnd, Pp), set_brackets(rnd, Pp), set_ltr(rnd, Pp), set_brackets_large(rnd, Pp), set_words(rnd, Pp)]
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
    for st in sets:
        for it in st["items"]:
            it["c"] = ["<span>%s</span>" % c if "<sup>" in c else c for c in it["c"]]
    return {
        "country": "uk", "subject": "maths", "grade": "year-6", "slug": "order-of-operations", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Order of Operations (BODMAS / BIDMAS)",
        "seo_title": "Year 6 Order of Operations Worksheets: BODMAS, BIDMAS and Brackets",
        "short_title": "Order of operations",
        "domain": "Addition, subtraction, multiplication and division",
        "standard_code": "Year 6: Addition, subtraction, multiplication and division",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Use their knowledge of the order of operations to carry out calculations involving the four operations; perform mental calculations, including with mixed operations and large numbers; use estimation to check answers to calculations and determine, in the context of a problem, an appropriate degree of accuracy.",
        "meta_desc": "Free Year 6 maths worksheets on the order of operations: BODMAS and BIDMAS, brackets, squares, working left to right, mental calculation with large numbers and estimating to check. 100 SATs-style questions with an answer key, matched to the National Curriculum.",
        "key_big": "Brackets first, then squares and cubes, then × and ÷, then + and −: 5 + 3 × 4 = 5 + 12 = 17.",
        "key_sub": "× and ÷ are equals, so work from left to right: 48 ÷ 6 × 2 = 8 × 2 = 16. + and − work the same way: 20 − 8 + 3 = 15.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
