# -*- coding: utf-8 -*-
"""
Australia Year 6 Maths: Order of Operations and Equations
(Australian Curriculum v9.0, AC9M6A02)
  python3 tools/gen_au_maths_y6_order_of_operations.py
Order of operations with brackets (× and ÷ before + and −, then left to right), placing brackets,
unknown values in equations with brackets (3 × (? + 4) = 27), the equals sign as a balance
(4 × 6 = 30 − ?) and word problems written as one number sentence.

Expressions are written in a small source syntax ("5 + 3 × 4", "(25 + 15) × 3") and evaluated
exactly with fractions.Fraction, cross-checked with Python eval. Every unknown is checked by putting
it back into the equation, and every wrong choice is checked to make the equation false.
Wrong answers come from real mistakes: working strictly left to right (2 + 3 × 4 = 20), + and −
before × and ÷, ignoring the brackets, × before ÷ (48 ÷ 6 × 2 = 4), + before − (20 − 8 + 3 = 9),
stopping one step early, undoing with the same operation instead of the inverse, undoing in the
wrong order, and reading = as “the answer is” (4 × 6 = 30 − ? gives 24).
HTML attributes use single quotes. Australian English, numbers of 5+ digits grouped with a no-break space.
"""
import json, os, random, re, string
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
BLUE = "#2f6fb0"
FILL = "#cfe6d6"
GREY = "#e4e4e4"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
NB = " "
Q = "<b>?</b>"

OPEN, CLOSE = ("(",), (")",)
STD = [("×", "÷"), ("+", "−")]
LTR = [("×", "÷", "+", "−")]                 # mistake: strictly left to right
REV = [("+", "−"), ("×", "÷")]               # mistake: + and − before × and ÷
MULFIRST = [("×",), ("÷",), ("+", "−")]      # mistake: × before ÷
ADDFIRST = [("×", "÷"), ("+",), ("−",)]      # mistake: + before −


# ------------------------------------------------------------ numbers
def f(x):
    """Australian style: 4 digits no separator, 5 or more digits grouped with a no-break space."""
    s = str(int(x))
    if abs(int(x)) < 10000:
        return s
    out = ""
    while len(s) > 3:
        out = NB + s[-3:] + out
        s = s[:-3]
    return s + out


def money(c):
    """Cents below $1 as 75c; dollars as $4.95, whole dollars as $12."""
    c = int(c)
    assert c % 5 == 0, c
    if c < 100:
        return "%dc" % c
    if c % 100 == 0:
        return "$" + f(c // 100)
    return "$%s.%02d" % (f(c // 100), c % 100)


# ------------------------------------------------------------ expression engine
TOK = re.compile(r"\d[\d" + NB + r"]*|[×÷+−()?=]")


class Calc(Fraction):
    """A number made by an earlier step."""


def tokens(s):
    out = [Fraction(t.replace(NB, "")) if t[0].isdigit() else t for t in TOK.findall(s)]
    assert "".join(TOK.findall(s)) == s.replace(" ", ""), s
    return out


def render(ts):
    out = ""
    for t in ts:
        s = f(t) if isinstance(t, Fraction) else (Q if t == "?" else t)
        if out and not out.endswith(OPEN) and s not in CLOSE:
            out += " "
        out += s
    return out


def H(s):
    return render(tokens(s))


def apply(a, op, b):
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


def flat_eval(seq, prec, rtl=False):
    seq = list(seq)
    for level in prec:
        if rtl:
            i = len(seq) - 2
            while i >= 1:
                if seq[i] in level:
                    v = apply(seq[i - 1], seq[i], seq[i + 1])
                    if v is None:
                        return None
                    seq[i - 1:i + 2] = [v]
                i -= 2
        else:
            i = 1
            while i < len(seq):
                if seq[i] in level:
                    v = apply(seq[i - 1], seq[i], seq[i + 1])
                    if v is None:
                        return None
                    seq[i - 1:i + 2] = [v]
                else:
                    i += 2
    assert len(seq) == 1
    return seq[0]


def ev_tokens(ts, prec=STD, rtl=False):
    ts = list(ts)
    while True:
        j = next((k for k, t in enumerate(ts) if t in CLOSE), None)
        if j is None:
            return flat_eval(ts, prec, rtl)
        i = max(k for k in range(j) if ts[k] in OPEN)
        v = flat_eval(ts[i + 1:j], prec, rtl)
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
    if mode == "noparen":
        return ev_tokens([t for t in ts if t not in OPEN + CLOSE])
    raise ValueError(mode)


def py_check(s, v):
    p = []
    for t in tokens(s):
        if isinstance(t, Fraction):
            p.append(str(int(t)))
        else:
            p.append({"×": "*", "÷": "/", "−": "-"}.get(t, t))
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
    """correct + the first 3 unique distractors."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
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
    w, h = int(round(w)), int(round(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


ASK = ["Work out %s", "What is %s?", "Calculate %s", "Find the value of %s"]

WP = "uses the wrong pair of numbers"
SIGN = "uses the wrong sign"
PART = "uses only the first number in the brackets"

WHY = {
    "ltr": "comes from working from left to right without doing × and ÷ first",
    "rev": "comes from adding or subtracting before multiplying or dividing",
    "mulfirst": "comes from multiplying before dividing, but × and ÷ are equals, so work from left to right",
    "addfirst": "comes from adding before subtracting, but + and − are equals, so work from left to right",
    "rtl": "comes from working from right to left",
    "noparen": "comes from ignoring the brackets",
}


def mistakes(s, modes, extra=()):
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


def templated(rnd, T, used, vmax=200, k0=0):
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
        its.append(eval_item(s, k + k0, modes, ex_))
    return its


def first_item(s, good, bad, why):
    return mcq("Which part of %s do you work out first?" % B(H(s)), H(good), [H(x) if x[0].isdigit() else x for x in bad],
               "%s. %s" % (chain(s), why))


# ------------------------------------------------------------ set 1: × and ÷ first, then left to right
def set_order(rnd, Pp):
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
        ("{a} + {b} × {c} − {d}", ["ltr", "rev"], [], lambda r: (R(2, 20), R(3, 9), R(3, 9), R(2, 9))),
        ("{a} × {b} + {c} × {d}", ["ltr", "rev"], [], lambda r: (R(2, 9), R(2, 9), R(2, 9), R(2, 9))),
        ("{a} × {b} − {c} × {d}", ["ltr", "rev"], [], lambda r: (R(6, 12), R(6, 12), R(2, 6), R(2, 6))),
        ("{a} − {b} ÷ {c} + {d}", ["ltr", "rev"], [], lambda r: (lambda c, q: (R(20, 50), c * q, c, R(2, 9)))(R(2, 9), R(2, 9))),
        ("{a} ÷ {b} + {c} × {d}", ["ltr", "rev"], [], lambda r: (lambda b, q: (b * q, b, R(2, 9), R(2, 9)))(R(2, 9), R(2, 9))),
        ("{a} + {b} × {c}", ["ltr"], [("{a} × {c} + {b}", WP)], lambda r: (R(1, 9) * 100, R(2, 9) * 10, R(2, 9))),
        ("{a} ÷ {b} × {c}", ["mulfirst"], [("{a} ÷ {b} + {c}", "adds the last number instead of multiplying")],
         lambda r: (lambda b, c, q: (b * c * q, b, c))(R(2, 6), R(2, 5), R(2, 5))),
        ("{a} − {b} + {c}", ["addfirst"], [("{a} + {b} + {c}", "adds all three numbers")],
         lambda r: (R(15, 40), R(5, 12), R(2, 6))),
        ("{a} − {b} − {c}", ["rtl"], [("{a} + {b} + {c}", "adds all three numbers")],
         lambda r: (R(20, 50), R(6, 15), R(2, 5))),
        ("{a} + {b} ÷ {c} × {d}", ["mulfirst", "ltr", "rev"], [], lambda r: (lambda c, d, q: (R(2, 20), c * d * q, c, d))(R(2, 5), R(2, 5), R(1, 4))),
    ]
    its = templated(rnd, T, used, vmax=1000)
    assert val("2 + 3 × 4") == 14 and ev("2 + 3 × 4", "ltr") == 20
    its.append(mcq("Which number sentence is correct?", "2 + 3 × 4 = 14", ["2 + 3 × 4 = 20", "2 + 3 × 4 = 12", "2 + 3 × 4 = 10"],
                   "2 + 3 × 4 = 2 + 12 = 14. 20 comes from adding first: 2 + 3 = 5, then 5 × 4. 12 stops after 3 × 4. 10 is 2 × 3 + 4, the wrong pair."))
    assert val("2 × 3 + 4") == 10
    its.append(first_item("40 − 30 ÷ 5", "30 ÷ 5", ["40 − 30", "Either part", "Neither"], "Divide before you subtract."))
    assert len(its) == 20, len(its)
    return {"title": "× and ÷ first, then left to right", "items": its}


# ------------------------------------------------------------ set 2: brackets; where do the brackets go?
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


def set_brackets(rnd, Pp):
    R = rnd.randint
    used = set()
    T = [
        ("({a} + {b}) × {c}", ["noparen"], [("{a} × {c} + {b}", PART)], lambda r: (R(2, 9), R(2, 9), R(2, 9))),
        ("{a} × ({b} − {c})", ["noparen"], [("{a} × ({b} + {c})", SIGN)], lambda r: (R(3, 9), R(10, 20), R(2, 8))),
        ("({a} − {b}) × {c}", ["noparen"], [("{a} × {c} − {b}", PART)], lambda r: (R(30, 60), R(2, 9), R(2, 5))),
        ("({a} + {b}) ÷ {c}", ["noparen"], [("({a} + {b}) × {c}", "multiplies instead of dividing")], lambda r: (lambda c, t: (lambda a: (a, c * t - a, c))(R(2, c * t - 2)))(R(3, 9), R(3, 9))),
        ("{a} − ({b} + {c})", ["noparen"], [("{a} + {b} + {c}", "adds all three numbers")], lambda r: (R(40, 90), R(5, 20), R(5, 20))),
        ("{a} ÷ ({b} − {c})", ["noparen"], [("{a} ÷ ({b} + {c})", SIGN)], lambda r: (lambda c, d, q: (d * q, c + d, c))(R(2, 9), R(2, 9), R(2, 9))),
        ("{a} + ({b} − {c}) × {d}", ["noparen", "ltr"], [], lambda r: (R(2, 20), R(8, 15), R(2, 6), R(2, 6))),
        ("({a} + {b}) × ({c} − {d})", ["noparen"], [("{a} + {b} × ({c} − {d})", "ignores the first pair of brackets"), ("({a} + {b}) × {c} − {d}", "ignores the second pair of brackets")], lambda r: (R(2, 9), R(2, 9), R(8, 15), R(2, 6))),
        ("{a} − {b} × ({c} − {d})", ["noparen", "ltr"], [], lambda r: (R(50, 99), R(2, 6), R(6, 12), R(2, 5))),
        ("{a} × ({b} + {c} × {d})", ["noparen", "ltr"], [], lambda r: (R(2, 5), R(2, 9), R(2, 6), R(2, 6))),
    ]
    its = templated(rnd, T, used, vmax=1000, k0=1)
    its.append(brackets_item("6 + 4 × 5 − 2", "(6 + 4) × 5 − 2", ["6 + 4 × (5 − 2)", "(6 + 4) × (5 − 2)", "6 + (4 × 5 − 2)"]))
    its.append(brackets_item("40 − 10 ÷ 2 + 3", "(40 − 10) ÷ 2 + 3", ["40 − 10 ÷ (2 + 3)", "(40 − 10) ÷ (2 + 3)", "40 − (10 ÷ 2 + 3)"]))
    its.append(brackets_item("7 × 8 − 3 + 2", "7 × (8 − 3 + 2)", ["7 × (8 − 3) + 2", "7 × 8 − (3 + 2)", "(7 × 8 − 3) + 2"]))
    its.append(brackets_item("2 + 6 × 3 + 1", "(2 + 6) × (3 + 1)", ["(2 + 6) × 3 + 1", "2 + 6 × (3 + 1)", "(2 + 6 × 3) + 1"]))
    its.append(brackets_item("72 ÷ 6 + 2 × 3", "72 ÷ (6 + 2) × 3", ["72 ÷ (6 + 2 × 3)", "(72 ÷ 6 + 2) × 3", "72 ÷ 6 + (2 × 3)"]))
    its.append(brackets_item("50 − 20 − 10 + 5", "50 − 20 − (10 + 5)", ["50 − (20 − 10) + 5", "(50 − 20) − 10 + 5", "50 − (20 − 10 + 5)"]))
    its.append(brackets_item("9 + 3 × 5 − 2", "9 + 3 × (5 − 2)", ["(9 + 3) × 5 − 2", "(9 + 3) × (5 − 2)", "(9 + 3 × 5) − 2"]))
    its.append(brackets_item("90 ÷ 3 + 6 × 2", "90 ÷ (3 + 6) × 2", ["(90 ÷ 3 + 6) × 2", "90 ÷ 3 + (6 × 2)", "90 ÷ (3 + 6 × 2)"]))
    its.append(first_item("50 − (12 + 8) × 2", "12 + 8", ["50 − 12", "8 × 2", "Either part"],
                          "Brackets first, then ×, then −."))
    vs = {x: val(x) for x in ["(7 × 4) + 2", "7 × 4 + 2", "2 + 7 × 4", "7 × (4 + 2)"]}
    assert vs["7 × (4 + 2)"] == 42 and len({vs[k] for k in vs if k != "7 × (4 + 2)"}) == 1 and vs["7 × 4 + 2"] == 30
    its.append(mcq("Which calculation has a <b>different</b> value from the others?", H("7 × (4 + 2)"),
                   [H("(7 × 4) + 2"), H("7 × 4 + 2"), H("2 + 7 × 4")],
                   "7 × (4 + 2) = 7 × 6 = 42. The other three all equal 7 × 4 + 2 = 28 + 2 = 30, because × is done before + anyway."))
    assert len(its) == 20, len(its)
    return {"title": "Brackets first, and where the brackets go", "items": its}


# ------------------------------------------------------------ unknown values
def sub(s, x):
    return s.replace("?", str(int(x)))


def eq_true(L, Rr, x):
    a, b = ev(sub(L, x)), ev(sub(Rr, x))
    return a is not None and a == b


def unk_item(L, Rr, x, cands, how, k, ask=None):
    """Find ? in L = Rr. cands = [(value, why)]. Checks the answer and that every choice used is wrong."""
    assert x > 0 and int(x) == x
    assert eq_true(L, Rr, x), (L, Rr, x)
    for y in range(0, 3000):
        if y != x:
            assert not eq_true(L, Rr, y), (L, Rr, y)
    picked, seen = [], {x}
    for w, why in cands:
        if w is None or w <= 0 or int(w) != w or w in seen:
            continue
        assert not eq_true(L, Rr, w)
        seen.add(w)
        picked.append((int(w), why))
        if len(picked) == 3:
            break
    assert len(picked) == 3, (L, Rr, x, cands)
    side = L if "?" in L else Rr
    chk = chain(sub(side, x))
    e = "%s Check: %s. Not %s: that %s." % (how, chk, f(picked[0][0]), picked[0][1])
    asks = ask or ["Find the value of %s." % Q, "What number does %s stand for?" % Q,
                   "Which number makes this true?", "Find the missing number."]
    q = "%s<br>%s" % (asks[k % len(asks)], B("%s = %s" % (H(L), H(Rr))))
    return mcq(q, f(x), [f(w) for w, _ in picked], e)


def set_unknowns(rnd, Pp):
    R = rnd.randint
    its, used = [], set()

    def ok_add(it):
        if it["q"] in used:
            return False
        used.add(it["q"])
        its.append(it)
        return True

    def T_mul_add(k, big=False, swap=False, inner_first=True):
        # a × (? + b) = c
        while True:
            a, b, x = (R(2, 9), R(2, 9), R(2, 12)) if not big else (R(3, 8), R(5, 30) * 5, R(2, 9) * 5)
            if len({a, b, x}) < 3:
                continue
            c, q = a * (x + b), x + b
            inner = "(? + %d)" % b if inner_first else "(%d + ?)" % b
            L = "%d × %s" % (a, inner)
            how = ("Undo the × %d first: the brackets must equal %s ÷ %d = %d. Then undo the + %d: %s = %d − %d = %d."
                   % (a, f(c), a, q, b, Q, q, b, x))
            cands = [(q, "stops after dividing and forgets to take away %d" % b),
                     (q + b, "adds %d instead of taking it away" % b),
                     (Fraction(c - b, a), "takes away %d before dividing by %d; undo the × outside the brackets first" % (b, a)),
                     (c - b, "takes away %d but forgets to divide by %d" % (b, a))]
            Ls, Rs = (L, f(c)) if not swap else (f(c), L)
            try:
                it = unk_item(Ls, Rs, x, cands, how, k)
            except AssertionError:
                continue
            if ok_add(it):
                return

    def T_mul_sub(k):
        # a × (? − b) = c
        while True:
            a, b, q = R(2, 9), R(2, 9), R(3, 12)
            x, c = q + b, a * q
            if len({a, b, x}) < 3 or q - b <= 0:
                continue
            how = ("Undo the × %d first: ? − %d = %d ÷ %d = %d. Then undo the − %d by adding: %s = %d + %d = %d."
                   % (a, b, c, a, q, b, Q, q, b, x)).replace("? −", Q + " −", 1)
            cands = [(q, "stops after dividing and forgets to add %d" % b),
                     (q - b, "takes away %d instead of adding it" % b),
                     (Fraction(c + b, a), "adds %d before dividing by %d; undo the × outside the brackets first" % (b, a)),
                     (c + b, "adds %d but forgets to divide by %d" % (b, a))]
            try:
                it = unk_item("%d × (? − %d)" % (a, b), f(c), x, cands, how, k)
            except AssertionError:
                continue
            if ok_add(it):
                return

    def T_div(k, minus=False):
        # (? + b) ÷ a = c  or  (? − b) ÷ a = c
        while True:
            a, b, c = R(2, 9), R(2, 12), R(3, 12)
            x = c * a - b if not minus else c * a + b
            if x <= 1 or len({a, b, c, x}) < 4:
                continue
            op, inv = ("+", "take away") if not minus else ("−", "add")
            how = ("Undo the ÷ %d by multiplying: the brackets must equal %d × %d = %d. Then %s %d: %s = %d."
                   % (a, c, a, c * a, inv, b, Q, x))
            cands = [(c * a, "forgets to %s %d" % (inv, b)),
                     (c * a + b if not minus else c * a - b, "%s %d instead" % ("adds" if not minus else "takes away", b)),
                     (Fraction(c, a) - b if not minus else Fraction(c, a) + b, "divides by %d instead of multiplying" % a),
                     (c - b if not minus else c + b, "forgets to multiply by %d" % a)]
            try:
                it = unk_item("(? %s %d) ÷ %d" % (op, b, a), f(c), x, cands, how, k)
            except AssertionError:
                continue
            if ok_add(it):
                return

    def T_lin(k, minus=False):
        # ? × a + b = c  /  a × ? − b = c (no brackets)
        while True:
            a, x = R(3, 9), R(3, 12)
            b = a * R(1, 4)
            c = a * x + b if not minus else a * x - b
            if c <= 0 or len({a, b, x}) < 3:
                continue
            if not minus:
                L = "? × %d + %d" % (a, b)
                how = ("× comes before +, so undo the + %d first: %s − %d = %d. Then undo the × %d: %s = %d ÷ %d = %d."
                       % (b, f(c), b, c - b, a, Q, c - b, a, x))
                cands = [(Fraction(c + b, a), "adds %d instead of taking it away" % b),
                         (Fraction(c, a) - b, "undoes the × before the +; undo the last step first"),
                         (c - b, "forgets to divide by %d" % a), (Fraction(c, a), "forgets the + %d" % b)]
            else:
                L = "%d × ? − %d" % (a, b)
                how = ("Undo the − %d first by adding: %s + %d = %d. Then undo the × %d: %s = %d ÷ %d = %d."
                       % (b, f(c), b, c + b, a, Q, c + b, a, x))
                cands = [(Fraction(c - b, a), "takes away %d instead of adding it" % b),
                         (Fraction(c, a) + b, "undoes the × before the −; undo the last step first"),
                         (c + b, "forgets to divide by %d" % a), (Fraction(c, a), "forgets the − %d" % b)]
            try:
                it = unk_item(L, f(c), x, cands, how, k)
            except AssertionError:
                continue
            if ok_add(it):
                return

    def T_sum_times(k):
        # (a + b) × ? = c
        while True:
            a, b, x = R(2, 9), R(2, 9), R(3, 12)
            if len({a, b, x}) < 3:
                continue
            c = (a + b) * x
            how = "Work out the brackets first: %d + %d = %d. So %d × %s = %s, and %s = %s ÷ %d = %d." % (a, b, a + b, a + b, Q, f(c), Q, f(c), a + b, x)
            cands = [(Fraction(c - a, b), "ignores the brackets and reads it as %d + %d × ?" % (a, b)),
                     (Fraction(c, a), "divides by %d only, not by %d + %d" % (a, a, b)),
                     (c - a - b, "takes away %d and %d instead of dividing" % (a, b)),
                     (Fraction(c, a) + b, "divides by %d and adds %d" % (a, b))]
            try:
                it = unk_item("(%d + %d) × ?" % (a, b), f(c), x, cands, how, k)
            except AssertionError:
                continue
            if ok_add(it):
                return

    def T_div_into(k):
        # c ÷ (? + b) = a
        while True:
            a, b, x = R(2, 9), R(2, 9), R(2, 9)
            if len({a, b, x}) < 3:
                continue
            c = a * (x + b)
            how = ("%s ÷ (? + %d) = %d, so the brackets must equal %s ÷ %d = %d. Then %s = %d − %d = %d."
                   % (f(c), b, a, f(c), a, x + b, Q, x + b, b, x)).replace("(? +", "(" + Q + " +", 1)
            cands = [(x + b, "forgets to take away %d" % b), (x + 2 * b, "adds %d instead of taking it away" % b),
                     (c - a - b, "takes away %d and %d instead of dividing" % (a, b)),
                     (Fraction(c - b, a), "takes away %d before dividing; find the value of the brackets first" % b)]
            try:
                it = unk_item("%s ÷ (? + %d)" % (f(c), b), f(a), x, cands, how, k)
            except AssertionError:
                continue
            if ok_add(it):
                return

    def T_three(k):
        # a × (? + b) − d = c
        while True:
            a, b, x, d = R(2, 6), R(2, 9), R(2, 9), R(2, 9)
            if len({a, b, x, d}) < 4:
                continue
            c = a * (x + b) - d
            if c <= 0:
                continue
            how = ("Undo the steps in reverse order. Undo − %d: %d + %d = %d. Undo × %d: %d ÷ %d = %d. Undo + %d: %s = %d − %d = %d."
                   % (d, c, d, c + d, a, c + d, a, x + b, b, Q, x + b, b, x))
            cands = [(Fraction(c - d, a) - b, "takes away %d instead of adding it back" % d),
                     (x + b, "forgets to take away %d at the end" % b),
                     (x + 2 * b, "adds %d instead of taking it away" % b),
                     (c + d - b, "forgets to divide by %d" % a)]
            try:
                it = unk_item("%d × (? + %d) − %d" % (a, b, d), f(c), x, cands, how, k)
            except AssertionError:
                continue
            if ok_add(it):
                return

    def T_add_mul(k):
        # a + b × (? − d) = c
        while True:
            a, b, x, d = R(5, 20), R(2, 6), R(5, 12), R(2, 4)
            if len({a, b, x, d}) < 4 or x - d < 2:
                continue
            c = a + b * (x - d)
            how = ("Undo the + %d first: %d − %d = %d. So %d × (? − %d) = %d. Undo × %d: %d ÷ %d = %d. Undo − %d: %s = %d + %d = %d."
                   % (a, c, a, c - a, b, d, c - a, b, c - a, b, x - d, d, Q, x - d, d, x)).replace("(? −", "(" + Q + " −", 1)
            cands = [(x - d, "forgets to add %d at the end" % d),
                     (Fraction(c, a + b) + d, "adds %d and %d first, but × comes before +" % (a, b)),
                     (x - 2 * d, "takes away %d instead of adding it" % d),
                     (Fraction(c + a, b) + d, "adds %d instead of taking it away" % a)]
            try:
                it = unk_item("%d + %d × (? − %d)" % (a, b, d), f(c), x, cands, how, k)
            except AssertionError:
                continue
            if ok_add(it):
                return

    k = 0
    for fn in [lambda k: T_mul_add(k), lambda k: T_mul_add(k), lambda k: T_mul_add(k, inner_first=False),
               lambda k: T_mul_add(k, swap=True), lambda k: T_mul_add(k, big=True),
               T_mul_sub, T_mul_sub, lambda k: T_div(k), lambda k: T_div(k, minus=True), lambda k: T_div(k),
               lambda k: T_lin(k), lambda k: T_lin(k, minus=True), T_sum_times, T_sum_times, T_div_into, T_div_into,
               T_three, T_three, T_add_mul, T_add_mul]:
        fn(k)
        k += 1
    assert len(its) == 20, len(its)
    return {"title": "Find the unknown in equations with brackets", "items": its}


# ------------------------------------------------------------ set 4: the equals sign as a balance
def tw(t, fs):
    return len(str(t)) * fs * 0.6


def pan_svg(left, right):
    """A level pan balance with an expression on each pan (plain text, '?' allowed)."""
    def box_w(t):
        return max(90, int(tw(t, 18) + 24))
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
        if "?" in t:
            a, b = t.split("?")
            x = c - tw(t, 18) / 2
            s.append("<text x='%.1f' y='%d' font-size='18' font-weight='700' fill='%s' xml:space='preserve'>%s<tspan fill='%s'>?</tspan>%s</text>"
                     % (x, top + 25, INK, a, RED, b))
        else:
            s.append("<text x='%.1f' y='%d' font-size='18' font-weight='700' fill='%s' text-anchor='middle'>%s</text>" % (c, top + 25, INK, t))
        s.append("<rect x='%.1f' y='%d' width='%d' height='6' fill='%s'/>" % (c - w / 2, py, w, INK))
        s.append("<rect x='%.1f' y='%d' width='4' height='18' fill='%s'/>" % (c - 2, py + 6, INK))
    by = py + 24
    s.append("<rect x='%.1f' y='%d' width='%.1f' height='6' fill='%s'/>" % (cl - 2, by, cr - cl + 4, INK))
    s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (mid, by + 6, mid - 22, by + 40, mid + 22, by + 40, GREEN))
    s.append("<rect x='%.1f' y='%d' width='80' height='5' fill='%s'/>" % (mid - 40, by + 40, INK))
    return svg_wrap(cr + wr / 2 + 8, by + 47, "".join(s), "pan balance: %s on the left and %s on the right" % (left, right))


def plain_src(s):
    """Source -> plain text for the pan picture."""
    return re.sub(r"<[^>]+>", "", H(s))


def bal_item(L, Rr, x, cands, how, k, pan=False):
    it = unk_item(L, Rr, x, cands, how, k,
                  ask=["Find the value of %s." % Q, "What number does %s stand for?" % Q,
                       "Which number makes this true?", "Find the missing number."])
    if pan:
        it["q"] = ("The pan balance is level. What number does %s stand for?<br>%s<br>%s"
                   % (Q, pan_svg(plain_src(L), plain_src(Rr)), B("%s = %s" % (H(L), H(Rr)))))
    return it


def true_item(good, bads, k):
    """Which number sentence is true? good/bads are 'L = R' source strings."""
    def sides(s):
        return [x.strip() for x in s.split("=")]
    for s in [good] + bads:
        assert len(sides(s)) >= 2
    gl, gr = sides(good)
    assert val(gl) == val(gr)
    parts = []
    for b in bads:
        ss = sides(b)
        assert len(ss) == 2, b
        assert val(ss[0]) != val(ss[1]), b
        parts.append("%s: %s = %s but %s = %s" % (" = ".join(H(x) for x in ss), H(ss[0]), f(val(ss[0])), H(ss[1]), f(val(ss[1]))))
    rend = lambda s: " = ".join(H(x) for x in sides(s))
    e = "%s is true: both sides equal %s. The others are false. %s." % (rend(good), f(val(gl)), ". ".join(cap(p) for p in parts[:1]) + ("" if len(parts) < 2 else ". " + ". ".join(parts[1:])))
    return mcq("Which number sentence is true?", rend(good), [rend(b) for b in bads], e)


def cap(s):
    return s[0].upper() + s[1:]


def set_balance(rnd, Pp):
    R = rnd.randint
    its, used = [], set()

    def add(it):
        if it["q"] in used:
            return False
        used.add(it["q"])
        its.append(it)
        return True

    def run(make, k, pan=False):
        for _ in range(5000):
            try:
                L, Rr, x, cands, how = make()
                it = bal_item(L, Rr, x, cands, how, k, pan)
            except AssertionError:
                continue
            if add(it):
                return
        raise RuntimeError("no item")

    def A():  # a × b = c − ?
        a, b = R(3, 9), R(3, 9)
        c = (a * b // 10 + R(1, 3)) * 10
        p, x = a * b, c - a * b
        assert a != b and x > 1
        how = "The left side is %d × %d = %d. So %d − %s = %d, and %s = %d − %d = %d." % (a, b, p, c, Q, p, Q, c, p, x)
        return ("%d × %d" % (a, b), "%d − ?" % c, x,
                [(p, "is the value of the left side, not the missing number: = means “the same as”, not “the answer is”"),
                 (c + p, "adds instead of subtracting"), (c - a - b, "adds %d and %d instead of multiplying" % (a, b))], how)

    def Bb():  # a × b = c + ?
        a, b = R(3, 9), R(4, 9)
        p = a * b
        c = R(5, p - 3)
        x = p - c
        assert a != b and x > 1 and c != x
        how = "The left side is %d × %d = %d. So %d + %s = %d, and %s = %d − %d = %d." % (a, b, p, c, Q, p, Q, p, c, x)
        return ("%d × %d" % (a, b), "%d + ?" % c, x,
                [(p, "is the value of the left side, not the missing number"), (p + c, "adds instead of subtracting"),
                 (a + b - c, "adds %d and %d instead of multiplying" % (a, b)), (c, "copies a number from the sentence")], how)

    def C():  # a + b = ? × c
        c, x = R(2, 9), R(3, 12)
        s = c * x
        a = R(2, s - 2)
        b = s - a
        assert len({a, b, c, x}) == 4
        how = "The left side is %d + %d = %d. So %s × %d = %d, and %s = %d ÷ %d = %d." % (a, b, s, Q, c, s, Q, s, c, x)
        return ("%d + %d" % (a, b), "? × %d" % c, x,
                [(s, "is the value of the left side, not the missing number"), (s * c, "multiplies instead of dividing"),
                 (s - c, "takes away %d instead of dividing" % c)], how)

    def D():  # a × b = c × ?
        while True:
            a, b, c = R(2, 9), R(2, 12), R(2, 9)
            if (a * b) % c == 0 and len({a, b, c, a * b // c}) == 4:
                break
        p, x = a * b, a * b // c
        how = "The left side is %d × %d = %d. So %d × %s = %d, and %s = %d ÷ %d = %d." % (a, b, p, c, Q, p, Q, p, c, x)
        return ("%d × %d" % (a, b), "%d × ?" % c, x,
                [(p, "is the value of the left side, not the missing number"),
                 (a + b - c, "treats both sides as adding (%d + %d = %d + %d)" % (a, b, c, a + b - c)),
                 (p - c, "takes away %d instead of dividing" % c)], how)

    def E():  # ? − a = b × c
        a, b, c = R(3, 20), R(3, 9), R(3, 9)
        assert len({a, b, c}) == 3
        p, x = b * c, b * c + a
        how = "The right side is %d × %d = %d. So %s − %d = %d, and %s = %d + %d = %d." % (b, c, p, Q, a, p, Q, p, a, x)
        return ("? − %d" % a, "%d × %d" % (b, c), x,
                [(p - a, "takes away %d instead of adding it" % a), (p, "is the value of the right side, not the missing number"),
                 (b + c + a, "adds %d and %d instead of multiplying" % (b, c))], how)

    def F():  # c ÷ d = e − ?
        d, q = R(2, 9), R(3, 9)
        c = d * q
        e_ = q + R(2, 15)
        x = e_ - q
        assert len({c, d, e_, x}) == 4 and x != q
        how = "The left side is %d ÷ %d = %d. So %d − %s = %d, and %s = %d − %d = %d." % (c, d, q, e_, Q, q, Q, e_, q, x)
        return ("%d ÷ %d" % (c, d), "%d − ?" % e_, x,
                [(q, "is the value of the left side, not the missing number"), (e_ + q, "adds instead of subtracting"),
                 (c - d, "subtracts instead of dividing" ) if c - d != x else (e_, "copies a number")], how)

    def G():  # a × b + c = ? × d
        while True:
            a, b, c, d = R(2, 9), R(2, 9), R(2, 20), R(2, 9)
            s = a * b + c
            if s % d == 0 and len({a, b, c, d}) == 4 and s // d > 1:
                break
        x = s // d
        how = "The left side is %d × %d + %d = %d + %d = %d. So %s × %d = %d, and %s = %d ÷ %d = %d." % (a, b, c, a * b, c, s, Q, d, s, Q, s, d, x)
        cands = [(s, "is the value of the left side, not the missing number"),
                 (Fraction(a * (b + c), d), "adds %d + %d first, but × comes before +" % (b, c)),
                 (s - d, "takes away %d instead of dividing" % d), (s * d, "multiplies instead of dividing")]
        return ("%d × %d + %d" % (a, b, c), "? × %d" % d, x, cands, how)

    def Hh():  # a × b = (? + c) × d
        while True:
            a, b, d, c = R(2, 9), R(3, 12), R(2, 9), R(2, 9)
            p = a * b
            if p % d == 0 and p // d - c > 1 and len({a, b, c, d}) == 4:
                break
        x = p // d - c
        how = ("The left side is %d × %d = %d. So (? + %d) × %d = %d. The brackets must equal %d ÷ %d = %d, so %s = %d − %d = %d."
               % (a, b, p, c, d, p, p, d, p // d, Q, p // d, c, x)).replace("(? +", "(" + Q + " +", 1)
        return ("%d × %d" % (a, b), "(? + %d) × %d" % (c, d), x,
                [(p // d, "forgets to take away %d" % c), (p // d + c, "adds %d instead of taking it away" % c),
                 (Fraction(p - c, d), "takes away %d before dividing" % c), (p - c, "forgets to divide by %d" % d)], how)

    def K():  # a × b − c = d + ?
        while True:
            a, b, c, d = R(3, 9), R(3, 9), R(2, 9), R(5, 20)
            x = a * b - c - d
            if x > 1 and len({a, b, c, d, x}) == 5:
                break
        lv = a * b - c
        how = "The left side is %d × %d − %d = %d − %d = %d. So %d + %s = %d, and %s = %d − %d = %d." % (a, b, c, a * b, c, lv, d, Q, lv, Q, lv, d, x)
        return ("%d × %d − %d" % (a, b, c), "%d + ?" % d, x,
                [(lv, "is the value of the left side, not the missing number"), (lv + d, "adds %d instead of subtracting" % d),
                 (a * (b - c) - d, "works out %d − %d first, but × comes before −" % (b, c)), (a * b - d, "forgets the − %d" % c)], how)

    def M():  # (a + b) × c = d × ?
        while True:
            a, b, c, d = R(2, 9), R(2, 9), R(2, 6), R(2, 9)
            p = (a + b) * c
            if p % d == 0 and len({a, b, c, d}) == 4 and p // d > 1:
                break
        x = p // d
        how = "The left side is (%d + %d) × %d = %d × %d = %d. So %d × %s = %d, and %s = %d ÷ %d = %d." % (a, b, c, a + b, c, p, d, Q, p, Q, p, d, x)
        return ("(%d + %d) × %d" % (a, b, c), "%d × ?" % d, x,
                [(p, "is the value of the left side, not the missing number"),
                 (Fraction(a + b * c, d), "ignores the brackets on the left"), (p - d, "takes away %d instead of dividing" % d),
                 (p * d, "multiplies instead of dividing")], how)

    k = 0
    for mk, pan in [(A, True), (A, False), (Bb, True), (Bb, False), (C, False), (C, False), (D, True), (D, False),
                    (E, False), (F, False), (G, False), (G, False), (Hh, False), (K, False), (M, False)]:
        run(mk, k, pan)
        k += 1
    assert val("4 × 6") == 24
    its.append(mcq("Which number makes this true?<br>%s" % B("4 × 6 = 30 − %s" % Q), "6", ["24", "54", "20"],
                   "4 × 6 = 24, so 30 − %s must also be 24. 30 − 6 = 24, so %s = 6. Not 24: that is the value of 4 × 6. "
                   "The = sign means “is the same as”, not “the answer is”. 54 adds 30 + 24. 20 adds 4 + 6 instead of multiplying." % (Q, Q)))
    its.append(true_item("3 × 8 = 30 − 6", ["3 × 8 = 30 − 8", "3 × 8 = 4 + 20 + 2", "5 × 4 = 30 − 8"], 0))
    its.append(true_item("36 ÷ 4 = 3 × 3", ["36 ÷ 4 = 3 × 4", "36 ÷ 4 = 12 − 4", "36 ÷ 6 = 3 × 3"], 1))
    its.append(true_item("(5 + 3) × 4 = 40 − 8", ["5 + 3 × 4 = 40 − 8", "(5 + 3) × 4 = 40 − 6", "(5 + 3) × 4 = 30 + 4"], 2))
    assert val("6 × 7") == 42 and val("42 + 5") == 47
    its.append(mcq("Ethan writes: %s. Why is this wrong?" % B("6 × 7 = 42 + 5 = 47"),
                   "It says 6 × 7 = 47, which is false",
                   ["6 × 7 is 48, not 42", "42 + 5 is 46, not 47", "Nothing: the working is correct"],
                   "The = sign means both sides are the same. 6 × 7 = 42, but 42 + 5 = 47, so “6 × 7 = 47” is not true. "
                   "Write two number sentences instead: 6 × 7 = 42, then 42 + 5 = 47."))
    assert len(its) == 20, len(its)
    return {"title": "The equals sign: balance both sides", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_words(rnd, Pp):
    its = []

    def add(q, good, bad, e):
        its.append(mcq(q, good, bad, e))

    # 1 sausage sizzle
    s = "4 × 3 + 3 × 2"
    assert val(s) == 18 and ev(s, "ltr") == 30 and val("(4 + 3) × (3 + 2)") == 35 and val("4 × 3 + 3") == 15
    n, he, his = Pp.next()
    add("At the school sausage sizzle, a sausage costs $3 and a drink costs $2. %s buys 4 sausages and 3 drinks. How much does %s spend?" % (n, he),
        "$18", ["$30", "$35", "$15"],
        "One number sentence: %s, so $18. Do both multiplications before adding. $30 comes from working left to right. "
        "$35 is (4 + 3) × (3 + 2). $15 forgets to multiply the drinks by $2." % chain(s))
    # 2 which number sentence: buses
    assert val("(48 + 52) ÷ 25") == 4
    add("48 Year 5 students and 52 Year 6 students go on a school excursion. Each bus takes 25 students. Which number sentence gives the number of buses?",
        H("(48 + 52) ÷ 25"), [H("48 + 52 ÷ 25"), H("48 ÷ 25 + 52"), H("25 × (48 + 52)")],
        "Add the two year levels first, then divide: (48 + 52) ÷ 25 = 100 ÷ 25 = 4 buses. "
        "Without brackets, 48 + 52 ÷ 25 would divide only the Year 6 students.")
    # 3 stickers
    s = "500 − 8 × 25"
    assert val(s) == 300 and ev(s, "ltr") == 12300
    n, he, his = Pp.next()
    add("%s has 500 footy cards. %s gives 25 cards to each of 8 friends. How many cards does %s have left?" % (n, cap(he), he),
        "300", [f(12300), "475", "200"],
        "%s. Multiply first. %s comes from working left to right. 475 gives cards to only one friend. 200 is the number given away." % (chain(s), f(12300)))
    # 4 canteen in cents
    s = "3 × 120 + 250"
    assert val(s) == 610 and val("3 × (120 + 250)") == 1110
    n, he, his = Pp.next()
    add("At the school canteen, %s buys 3 fruit cups at $1.20 each and a wrap for $2.50. How much does %s spend?" % (n, he),
        money(610), [money(1110), money(370), money(360)],
        "In cents: %s, so 610c = $6.10. Multiply first. $11.10 is 3 × (120 + 250), which buys 3 wraps. "
        "$3.70 buys only one fruit cup. $3.60 forgets the wrap." % chain(s))
    # 5 which sentence: pens
    assert len({val("4 × 6 + 3"), val("4 × (6 + 3)"), val("(4 + 3) × 6"), val("4 + 6 × 3")}) == 4
    n, he, his = Pp.next()
    add("%s buys 4 packs of 6 pencils and 3 single pencils. Which number sentence gives the number of pencils?" % n,
        H("4 × 6 + 3"), [H("4 × (6 + 3)"), H("(4 + 3) × 6"), H("4 + 6 × 3")],
        "4 packs of 6 is 4 × 6, then add the 3 single pencils: 4 × 6 + 3 = 24 + 3 = 27. 4 × (6 + 3) = 36 would mean 4 packs of 9.")
    # 6 think of a number
    assert 3 * (5 + 4) == 27
    n, he, his = Pp.next()
    add("%s thinks of a number. %s adds 4, then multiplies by 3. The answer is 27. What is the number?" % (n, cap(he)),
        "5", ["9", "13", "23"],
        "Number sentence: 3 × (%s + 4) = 27. Undo in reverse order: 27 ÷ 3 = 9, then 9 − 4 = 5. Check: 3 × (5 + 4) = 3 × 9 = 27. "
        "Not 9: that forgets to take away 4. 13 adds 4 instead. 23 takes away 4 but forgets to divide." % Q)
    # 7 think of a number 2
    assert (11 * 4 - 6) == 38
    n, he, his = Pp.next()
    add("%s thinks of a number, multiplies it by 4 and then takes away 6. The answer is 38. Which number sentence shows this?" % n,
        H("? × 4 − 6 = 38"), [H("(? − 6) × 4 = 38"), H("? × 6 − 4 = 38"), H("? − 6 × 4 = 38")],
        "Multiply first, then take away 6: %s × 4 − 6 = 38. Undo: 38 + 6 = 44, 44 ÷ 4 = 11, so the number is 11. "
        "(%s − 6) × 4 would take away 6 before multiplying." % (Q, Q))
    # 8 swimming carnival
    s = "6 × 25 + 4 × 50"
    assert val(s) == 350 and ev(s, "ltr") == 7700 and val("(6 + 4) × (25 + 50)") == 750
    n, he, his = Pp.next()
    add("At the swimming carnival, %s swims 6 laps of a 25 m pool and then 4 laps of a 50 m pool. How far does %s swim altogether?" % (n, he),
        "350 m", [f(7700) + " m", "750 m", "200 m"],
        "%s, so 350 m. %s m comes from working left to right. 750 m is (6 + 4) × (25 + 50). 200 m counts only the 50 m pool." % (chain(s), f(7700)))
    # 9 unknown: packets of stickers
    assert 3 * 12 + 5 == 41
    n, he, his = Pp.next()
    add("%s buys 3 packets of stickers and gets 5 free stickers. %s has 41 stickers altogether. How many stickers are in each packet?" % (n, cap(he)),
        "12", ["15", "36", "46"],
        "Number sentence: 3 × %s + 5 = 41. Undo the + 5: 41 − 5 = 36. Undo the × 3: 36 ÷ 3 = 12. Check: 3 × 12 + 5 = 41. "
        "15 is 46 ÷ 3, which adds the 5 instead of taking it away. 36 forgets to divide by 3. 46 adds the 5." % Q)
    # 10 cricket
    assert (20 + 15) * 2 == 70 and 20 + 15 * 2 == 50
    add("A cricket team has 20 players in the seniors and 15 in the juniors. Each player needs 2 caps. Which number sentence gives the number of caps?",
        H("(20 + 15) × 2"), [H("20 + 15 × 2"), H("20 × 15 + 2"), H("(20 + 2) × 15")],
        "Add the players first, then multiply: (20 + 15) × 2 = 35 × 2 = 70 caps. Without brackets, 20 + 15 × 2 = 50 gives caps only to the juniors.")
    # 11 equal sharing, fundraising
    s = "(350 + 250) ÷ 4"
    assert val(s) == 150 and 350 + Fraction(250, 4) == Fraction(825, 2) and 600 * 4 == 2400
    add("A school raises $350 at a fete and $250 at a trivia night. The money is shared equally between 4 charities. How much does each charity get?",
        "$150", ["$600", "$412.50", "$2400"],
        "%s, so $150. Add first, then divide. $600 is the total before sharing. $412.50 ignores the brackets (350 + 250 ÷ 4). "
        "$2400 multiplies instead of dividing." % chain(s))
    # 12 balance word problem
    assert 6 * 4 == 30 - 6
    n1 = Pp.next()[0]
    n2, he2, his2 = Pp.next()
    add("%s has 6 bags of 4 marbles. %s has 30 marbles but loses some. Now they have the same number of marbles. How many did %s lose?" % (n1, n2, n2),
        "6", ["24", "54", "20"],
        "Number sentence: 6 × 4 = 30 − %s. 6 × 4 = 24, so 30 − %s = 24 and %s = 6. "
        "Not 24: that is how many marbles each has now. 54 adds instead of subtracting. 20 adds 6 + 4 instead of multiplying." % (Q, Q, Q))
    # 13 netball
    s = "120 − 7 × 12"
    assert val(s) == 36 and ev(s, "ltr") == 1356
    add("A netball club has 120 bibs. 7 teams each take 12 bibs. How many bibs are left?",
        "36", ["1356", "108", "84"],
        "%s. Multiply first. 1356 comes from working left to right. 108 takes bibs for only one team. 84 is the number of bibs taken." % chain(s))
    # 14 kangaroo fact? unknown with brackets: tickets
    assert 2 * (15 + 10) == 50
    n, he, his = Pp.next()
    add("At the zoo, %s pays $50 for 2 adult tickets and 2 guidebooks. A guidebook costs $10. How much is one adult ticket?" % n,
        "$15", ["$25", "$20", "$30"],
        "Number sentence: 2 × (%s + 10) = 50. Undo the × 2: 50 ÷ 2 = 25. Undo the + 10: 25 − 10 = 15. Check: 2 × (15 + 10) = 50. "
        "$25 forgets to take away the guidebook. $20 is (50 − 10) ÷ 2, which takes away only one guidebook. $30 is 50 − 2 × 10, which forgets to share between 2." % Q)
    # 15 kilometres
    s = "3 × 12 + 2 × 8"
    assert val(s) == 52 and ev(s, "ltr") == 304
    n, he, his = Pp.next()
    add("%s rides 12 km on each of 3 days and 8 km on each of 2 days. How far does %s ride altogether?" % (n, he),
        "52 km", ["304 km", "100 km", "20 km"],
        "%s, so 52 km. 304 km comes from working left to right. 100 km is (3 + 2) × (12 + 8). 20 km adds 12 + 8 only." % chain(s))
    assert val("(3 + 2) × (12 + 8)") == 100
    # 16 which sentence: change
    assert 50 - 3 * 12 == 14
    n, he, his = Pp.next()
    add("%s pays for 3 T-shirts at $12 each with a $50 note. Which number sentence gives %s change?" % (n, his),
        H("50 − 3 × 12"), [H("(50 − 3) × 12"), H("50 − 3 + 12"), H("50 ÷ 3 × 12")],
        "Find the cost first, 3 × 12 = 36, then subtract from $50. 50 − 3 × 12 = 50 − 36 = 14, so the change is $14. "
        "(50 − 3) × 12 subtracts before multiplying.")
    # 17 Perth to... realistic sharing
    s = "(18 + 14) ÷ 4"
    assert val(s) == 8
    add("A class has 18 girls and 14 boys. They work in groups of 4. How many groups are there?",
        "8", ["21.5", "128", "32"],
        "%s groups. Add first, then divide. 21.5 comes from 18 + 14 ÷ 4 with no brackets, which divides only the boys. 128 multiplies by 4. 32 is the whole class." % chain(s))
    # 18 unknown: equal teams
    assert 6 * 6 + 3 == 39 and (39 + 3) // 6 == 7 and 39 // 3 == 13
    add("39 students come to footy training. 3 of them are goal umpires. The rest make teams of 6. How many teams are there?",
        "6", ["7", "36", "13"],
        "Number sentence: %s × 6 + 3 = 39. Undo the + 3: 39 − 3 = 36. Undo the × 6: 36 ÷ 6 = 6 teams. "
        "7 is 42 ÷ 6, which adds the 3 umpires instead of taking them away. 36 forgets to divide by 6. 13 is 39 ÷ 3, which divides by the number of umpires." % Q)
    # 19 large numbers
    s = "45000 − 8 × 3500"
    assert val(s) == 17000
    add("A stadium in Melbourne has %s seats. 8 stands of %s seats are full and every other seat is empty. How many seats are empty?" % (f(45000), f(3500)),
        f(17000), [f(41500), f(28000), f(73000)],
        "%s. 8 × 3500 = 8 × 35 hundreds = 280 hundreds. %s counts only one stand. %s is the number of full seats. %s adds instead of subtracting."
        % (chain(s), f(41500), f(28000), f(73000)))
    # 20 balance: two people same total
    assert 4 * 9 + 6 == 6 * 7
    n1 = Pp.next()[0]
    n2, he2, his2 = Pp.next()
    add("%s buys 4 books at $9 each and a $6 bookmark. %s buys 6 books that all cost the same. They spend the same amount. How much is each of %s books?"
        % (n1, n2, his2), "$7", ["$42", "$6", "$10"],
        "Number sentence: 4 × 9 + 6 = 6 × %s. The left side is 36 + 6 = 42. So 6 × %s = 42, and %s = 42 ÷ 6 = 7. "
        "$42 is the total, not one book. $6 is (4 × 9) ÷ 6, which forgets the bookmark. $10 is 4 × (9 + 6) ÷ 6, which adds before multiplying." % (Q, Q, Q))
    assert 4 * (9 + 6) / 6 == 10 and 36 / 6 == 6
    assert len(its) == 20, len(its)
    return {"title": "Write a number sentence and solve", "items": its}


# ------------------------------------------------------------ lesson
def steps_svg(rows, label, W=330):
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
    boxes = [("( )", "Brackets"), ("× ÷", "left to right"), ("+ −", "left to right")]
    bw, bh, gap = 150, 64, 30
    W = 3 * bw + 2 * gap + 8
    out = ["<defs><marker id='ar' viewBox='0 0 10 10' refX='8' refY='5' markerWidth='6' markerHeight='6' orient='auto'>"
           "<path d='M0 0 L10 5 L0 10 z' fill='%s'/></marker></defs>" % GREEN]
    for i, (big, small) in enumerate(boxes):
        x = 4 + i * (bw + gap)
        out.append("<rect x='%d' y='4' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>" % (x, bw, bh, FILL, GREEN))
        out.append("<text x='%d' y='32' font-size='22' font-weight='700' fill='%s' text-anchor='middle'>%s</text>" % (x + bw // 2, GREEN, big))
        out.append("<text x='%d' y='56' font-size='15' fill='%s' text-anchor='middle'>%s</text>" % (x + bw // 2, INK, small))
        if i < 2:
            out.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2' marker-end='url(#ar)'/>"
                       % (x + bw + 3, 4 + bh // 2, x + bw + gap - 3, 4 + bh // 2, GREEN))
    return svg_wrap(W, bh + 8, "".join(out), "order of operations: brackets, then multiplication and division, then addition and subtraction")


def undo_svg():
    """? -> +4 -> ×3 -> 27 on top; 5 <- −4 <- ÷3 <- 27 underneath."""
    W, bw, aw = 420, 64, 76
    xs = [10 + i * (bw + aw) for i in range(3)]
    out = ["<defs><marker id='au' viewBox='0 0 10 10' refX='8' refY='5' markerWidth='6' markerHeight='6' orient='auto'>"
           "<path d='M0 0 L10 5 L0 10 z' fill='%s'/></marker>"
           "<marker id='ad' viewBox='0 0 10 10' refX='8' refY='5' markerWidth='6' markerHeight='6' orient='auto'>"
           "<path d='M0 0 L10 5 L0 10 z' fill='%s'/></marker></defs>" % (GREEN, RED)]
    top = [("?", RED), ("9", INK), ("27", INK)]
    bot = [("5", GREEN), ("9", INK), ("27", INK)]
    for row, (y, vals) in enumerate(((8, top), (88, bot))):
        for x, (t, col) in zip(xs, vals):
            out.append("<rect x='%d' y='%d' width='%d' height='40' rx='6' fill='#fff' stroke='%s' stroke-width='2'/>" % (x, y, bw, INK))
            out.append("<text x='%d' y='%d' font-size='20' font-weight='700' fill='%s' text-anchor='middle'>%s</text>" % (x + bw // 2, y + 27, col, t))
    ops_top, ops_bot = ["+ 4", "× 3"], ["− 4", "÷ 3"]
    for i in range(2):
        x1, x2 = xs[i] + bw + 4, xs[i + 1] - 4
        out.append("<line x1='%d' y1='28' x2='%d' y2='28' stroke='%s' stroke-width='2.5' marker-end='url(#au)'/>" % (x1, x2, GREEN))
        out.append("<text x='%d' y='20' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>" % ((x1 + x2) // 2, GREEN, ops_top[i]))
        out.append("<line x1='%d' y1='108' x2='%d' y2='108' stroke='%s' stroke-width='2.5' marker-end='url(#ad)'/>" % (x2, x1, RED))
        out.append("<text x='%d' y='132' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s</text>" % ((x1 + x2) // 2, RED, ops_bot[i]))
    out.append("<text x='%d' y='72' font-size='14' fill='%s' text-anchor='middle'>undo in reverse order</text>" % (W // 2 - 10, BLUE))
    w = xs[2] + bw + 10
    return svg_wrap(w, 140, "".join(out), "function machine: question mark plus 4 times 3 makes 27; undo: 27 divided by 3 is 9, 9 minus 4 is 5")


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    assert val("2 + 3 × 4") == 14 and val("(25 + 15) × 3") == 120 and val("48 ÷ 6 × 2") == 16
    assert val("20 − 8 + 3") == 15 and 3 * (5 + 4) == 27 and 4 * 6 == 30 - 6
    fig1 = steps_svg([(["2 + ", ("3 × 4", RED)], "multiply first"),
                      ([("2 + 12", RED)], "then add"),
                      ([("14", GREEN)], "")], "working out 2 plus 3 times 4 step by step")
    return (
        "<h2>Why the order matters</h2>"
        "<p>A calculation with more than one operation could give different answers if people worked in a different order. "
        "So everyone uses the same <b>order of operations</b>. Many Australian classrooms remember it as <b>BODMAS</b>.</p>"
        "<figure class='sn-fig'>" + order_svg() +
        "<figcaption>Brackets first, then × and ÷ from left to right, then + and − from left to right.</figcaption></figure>" +
        table(["Step", "Do this", "Example"], [
            ["1", "Brackets", "(25 + 15) × 3 = 40 × 3 = 120"],
            ["2", "× and ÷, as equals, from left to right", "48 ÷ 6 × 2 = 8 × 2 = 16"],
            ["3", "+ and −, as equals, from left to right", "20 − 8 + 3 = 12 + 3 = 15"],
        ]) +
        "<figure class='sn-fig'>" + fig1 +
        "<figcaption>2 + 3 × 4: multiply before you add, so the answer is 14, not 20.</figcaption></figure>" +
        ex("Brackets change the answer", "Work out (25 + 15) × 3.",
           chain("(25 + 15) × 3") + ". Without the brackets, 25 + 15 × 3 = 25 + 45 = 70.", "120") +
        "<h2>Find the unknown: undo in reverse order</h2>"
        "<p>In 3 × (%s + 4) = 27, the unknown had 4 added, then was multiplied by 3. "
        "To find it, undo the last step first, using the inverse operation.</p>" % Q +
        "<figure class='sn-fig'>" + undo_svg() +
        "<figcaption>Forwards: add 4, then multiply by 3. Backwards: divide by 3, then take away 4.</figcaption></figure>" +
        ex("Unknown inside brackets", "3 × (%s + 4) = 27" % Q,
           "Undo × 3: the brackets must equal 27 ÷ 3 = 9. Undo + 4: %s = 9 − 4 = 5. Check: 3 × (5 + 4) = 3 × 9 = 27." % Q, "5") +
        ex("No brackets", "%s × 4 + 8 = 36" % Q,
           "× comes before +, so the + 8 was the last step. Undo it first: 36 − 8 = 28. Then 28 ÷ 4 = 7. Check: 7 × 4 + 8 = 28 + 8 = 36.", "7") +
        "<h2>The equals sign means “the same as”</h2>"
        "<p>= does not mean “the answer is”. It means both sides have the same value, like a level balance.</p>"
        "<figure class='sn-fig'>" + pan_svg("4 × 6", "30 − ?") +
        "<figcaption>The left side is 24, so 30 − ? must also be 24. ? = 6.</figcaption></figure>" +
        ex("Balance", "4 × 6 = 30 − %s" % Q,
           "Work out the side you know: 4 × 6 = 24. So 30 − %s = 24, and %s = 30 − 24 = 6." % (Q, Q), "6") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["2 + 3 × 4 = 5 × 4 = 20", "Multiply first: 2 + 12 = 14"],
            ["48 ÷ 6 × 2 = 48 ÷ 12 = 4", "× and ÷ are equals: left to right, 8 × 2 = 16"],
            ["20 − 8 + 3 = 20 − 11 = 9", "+ and − are equals: left to right, 12 + 3 = 15"],
            ["3 × (? + 4) = 27, so ? = 9", "9 is the value of the brackets. Take away 4: ? = 5"],
            ["4 × 6 = 30 − ?, so ? = 24", "24 is the left side. 30 − ? = 24, so ? = 6"],
            ["6 × 7 = 42 + 5 = 47", "Write two number sentences: 6 × 7 = 42, then 42 + 5 = 47"],
        ])
    )


FAQ = [
    {"q": "What is the order of operations in Year 6 maths?",
     "a": "Work out brackets first, then multiplication and division from left to right, then addition and subtraction from left to right. For example, 2 + 3 × 4 = 2 + 12 = 14, not 20."},
    {"q": "Is BODMAS taught in Australian schools?",
     "a": "Yes. Many Australian teachers use BODMAS (or BIDMAS) to help students remember the order of operations. The key point is that × and ÷ are equals, and so are + and −, so you work from left to right: 48 ÷ 6 × 2 = 16."},
    {"q": "How do you find an unknown inside brackets, like 3 × (? + 4) = 27?",
     "a": "Undo the steps in reverse order. Divide by 3 to get 9, the value of the brackets, then take away 4 to get 5. Check: 3 × (5 + 4) = 27."},
    {"q": "Which Australian Curriculum content description covers this?",
     "a": "AC9M6A02 in Year 6: find unknown values in numerical equations involving brackets and combinations of operations. It builds the skills students need for algebra in Year 7, where NAPLAN numeracy is next sat."},
]


def gen():
    rnd = random.Random(6811)
    Pp = People(rnd)
    sets = [set_order(rnd, Pp), set_brackets(rnd, Pp), set_unknowns(rnd, Pp), set_balance(rnd, Pp), set_words(rnd, Pp)]
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
        "country": "au", "subject": "maths", "grade": "year-6", "slug": "order-of-operations-and-equations", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 6 Order of Operations and Equations",
        "seo_title": "Year 6 Order of Operations and Equations Worksheets: Free Maths with Answer Key (Australian Curriculum)",
        "short_title": "Order of Operations and Equations",
        "domain": "Algebra",
        "standard_code": "AC9M6A02",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Find unknown values in numerical equations involving brackets and combinations of arithmetic operations, using the properties of numbers and operations",
        "meta_desc": "Free Year 6 maths worksheets on the order of operations and equations, aligned to the Australian Curriculum (AC9M6A02): brackets, × and ÷ before + and −, placing brackets, unknowns like 3 × (? + 4) = 27, balancing 4 × 6 = 30 − ? and word problems. 100 questions with an answer key.",
        "key_big": "Brackets first, then × and ÷, then + and −, each from left to right: 2 + 3 × 4 = 2 + 12 = 14.",
        "key_sub": "To find an unknown, undo the steps in reverse order: 3 × (? + 4) = 27, so ? + 4 = 9 and ? = 5. The = sign means “the same as”: 4 × 6 = 30 − 6.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    # pan balances print at normal size so page 3 is not shrunk
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
