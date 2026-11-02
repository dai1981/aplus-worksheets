# -*- coding: utf-8 -*-
"""
US Grade 5 Math: Numerical Expressions and Order of Operations (5.OA.A.1–2)
  python tools/gen_us_math_g5_expressions.py
HTML attributes use single quotes (no backslashes in the JSON).
Every value is computed by a small expression engine and cross-checked with Python eval.
Wrong answers come from real mistakes: working strictly left to right, + before − or × before ÷,
ignoring the parentheses, ignoring the inner parentheses, stopping one step early.
"""
import json, os, random, re, string
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
BLUE = "#2f6fb0"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]

OPEN, CLOSE = ("(", "[", "{"), (")", "]", "}")
MATCH = {")": "(", "]": "[", "}": "{"}
STD = [("×", "÷"), ("+", "−")]                 # the real order
LTR = [("×", "÷", "+", "−")]                   # mistake: strictly left to right
ADD_FIRST = [("×", "÷"), ("+",), ("−",)]       # mistake: + before −
MUL_FIRST = [("×",), ("÷",), ("+", "−")]       # mistake: × before ÷
REV = [("+", "−"), ("×", "÷")]                 # mistake: + and − before × and ÷


# ------------------------------------------------------------ expression engine
def f(n):
    """Grade 5 style: 4536 -> 4,536."""
    return "{:,}".format(int(n))


def tokens(s):
    out = []
    for t in re.findall(r"\d[\d,]*|[×÷+−()\[\]{}]", s):
        out.append(int(t.replace(",", "")) if t[0].isdigit() else t)
    assert render(out) == s, (s, render(out))      # the expression is written in the house style
    return out


def render(ts):
    s = " ".join(f(t) if isinstance(t, int) else t for t in ts)
    for o in OPEN:
        s = s.replace(o + " ", o)
    for c in CLOSE:
        s = s.replace(" " + c, c)
    return s


class Calc(int):
    """A number made by an earlier step (not written in the expression)."""


def apply(a, op, b):
    if op == "×":
        return a * b
    if op == "÷":
        if b == 0 or a % b:
            return None
        return a // b
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
        assert ts[i] == MATCH[ts[j]]
        v = flat_eval(ts[i + 1:j], prec, rtl)
        if v is None:
            return None
        ts[i:j + 1] = [v]


def strip(ts, min_depth=1):
    """Remove grouping symbols at depth >= min_depth (1 = all, 2 = the inner ones)."""
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
    if mode == "addfirst":
        return ev_tokens(ts, ADD_FIRST)
    if mode == "mulfirst":
        return ev_tokens(ts, MUL_FIRST)
    if mode == "rev":
        return ev_tokens(ts, REV)
    if mode == "rtl":
        return ev_tokens(ts, STD, rtl=True)
    if mode == "noparen":
        return ev_tokens(strip(ts))
    if mode == "noparen_ltr":
        return ev_tokens(strip(ts), LTR)
    if mode == "noinner":
        return ev_tokens(strip(ts, 2))
    raise ValueError(mode)


def py_check(s, v):
    """Cross-check with Python eval of the same expression."""
    p = s.replace(",", "").replace("×", "*").replace("÷", "/").replace("−", "-")
    for o in "[{":
        p = p.replace(o, "(")
    for c in "]}":
        p = p.replace(c, ")")
    p = re.sub(r"(\d+)", r"Fraction(\1)", p)
    assert eval(p, {"Fraction": Fraction}) == v, (s, v)


def steps(s, values=False):
    """One operation per step, innermost group first. Returns the expression after each step
    (or, with values=True, the earlier results each step uses)."""
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
            ts[lo - 1:hi + 1] = seg            # drop brackets around a single number
        else:
            ts[lo:hi] = seg
        r = render(ts)
        if not out or out[-1] != r:
            out.append(r)
    return made if values else out


def chain(s):
    v = ev(s)
    assert v is not None and v > 0, s
    py_check(s, v)
    st = steps(s)
    assert int(st[-1].replace(",", "")) == v, (s, st)
    return " = ".join([s] + st)


def val(s):
    v = ev(s)
    assert v is not None and v > 0, s
    py_check(s, v)
    return v


def before_last(s):
    """The answer if you stop one step early: the bigger earlier result that the last step uses."""
    m = steps(s, values=True)
    return int(max(m[-1])) if m and m[-1] else None


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + 3 unique distractors (no zero, negative or missing values)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or not c or c.startswith("-") or c == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    return {"q": q, "c": ch, "a": 3, "e": e}


def nums(vals):
    return [f(v) if isinstance(v, int) and v > 0 else None for v in vals]


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


ASK = ["What is the value of %s?", "Evaluate %s.", "Find the value of %s.", "What is %s?"]

WHY = {
    "noparen": "comes from skipping the parentheses",
    "noparen_ltr": "comes from skipping the grouping symbols and working left to right",
    "noinner": "comes from skipping the inner grouping symbols",
    "ltr": "comes from working strictly left to right",
    "addfirst": "comes from adding before subtracting",
    "mulfirst": "comes from multiplying before dividing",
    "rtl": "comes from working right to left",
    "rev": "comes from adding and subtracting before multiplying and dividing",
}


def mistakes(s, modes, extra=()):
    """Wrong values in order of priority: (value, reason). Only positive whole numbers that differ."""
    v = ev(s)
    out, seen = [], {v}
    for m in modes:
        w = ev(s, m)
        if w is not None and w > 0 and w not in seen:
            seen.add(w)
            out.append((w, WHY[m]))
    for x in extra:
        w = ev(x)
        if w is not None and w > 0 and w not in seen:
            seen.add(w)
            out.append((w, "is the value of " + x))
    w = before_last(s)
    if w is not None and w > 0 and w not in seen:
        out.append((w, "stops one step early"))
    return out


def enough(s, v, modes, extra, n_modes=1):
    """The first n_modes mistakes really change the value, and there are 3 different wrong answers."""
    ws = [ev(s, m) for m in modes[:n_modes]]
    if not all(w is not None and w > 0 and w != v for w in ws) or len(set(ws)) < n_modes:
        return False
    return len(mistakes(s, modes, extra)) >= 3


def eval_item(s, k, modes, extra=(), note=""):
    """'What is the value of s?' Distractors: the listed mistake modes, then extra wrong expressions,
    then stopping one step early."""
    v = val(s)
    ms = mistakes(s, modes, extra)
    assert len(ms) >= 3, (s, ms)
    w, why = ms[0]
    e = chain(s) + ". " + (note + " " if note else "") + "Not %s: that %s." % (f(w), why)
    return mcq(ASK[k % len(ASK)] % B(s), f(v), [f(x) for x, _ in ms], e)


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


def fields(t):
    return [x[1] for x in string.Formatter().parse(t) if x[1]]


def gen_nums(rnd, maker, ok, used):
    for _ in range(5000):
        d = maker(rnd)
        if ok(d) and d not in used:
            used.add(d)
            return d
    raise RuntimeError("no numbers for line %d" % maker.__code__.co_firstlineno)


# ------------------------------------------------------------ set 1: parentheses first
def set_parentheses(rnd, P):
    its = []
    used = set()
    R = rnd.randint
    # (template, distractor modes, extra wrong expressions as templates, number maker)

    def div_nums(r):
        c, d = R(2, 5), R(1, 4)
        b = c * R(2, 6)
        return (b + (c + d) * R(3, 9), b, c, d)

    T = [
        ("{a} × ({b} + {c})", ["noparen"], ["({a} + {b}) × {c}"], lambda r: (R(3, 9), R(4, 12), R(3, 9))),
        ("({a} + {b}) × {c}", ["noparen"], ["{a} × ({b} + {c})"], lambda r: (R(4, 12), R(3, 9), R(3, 9))),
        ("({a} − {b}) × {c}", ["noparen"], ["{a} × {c} − {b}"], lambda r: (R(12, 20), R(3, 9), R(3, 8))),
        ("{a} × ({b} − {c})", ["noparen"], ["{a} × {b}"], lambda r: (R(3, 9), R(10, 18), R(2, 7))),
        ("({a} + {b}) ÷ {c}", ["noparen"], ["{a} ÷ {c} + {b}"], lambda r: (R(2, 9) * 6, R(1, 4) * 6, 6)),
        ("{a} ÷ ({b} − {c})", ["noparen"], ["{a} ÷ {b}"], lambda r: (72, R(10, 14), R(4, 9))),
        ("{a} − ({b} + {c})", ["noparen"], ["{a} − {b}"], lambda r: (R(40, 90), R(11, 19), R(4, 9))),
        ("{a} − ({b} − {c})", ["noparen"], ["{a} − {b}"], lambda r: (R(40, 90), R(12, 25), R(3, 9))),
        ("({a} + {b}) × ({c} − {d})", ["noparen"], ["({a} + {b}) × {c} − {d}"], lambda r: (R(3, 8), R(2, 6), R(9, 14), R(3, 7))),
        ("({a} − {b}) ÷ ({c} + {d})", ["noparen"], ["{a} − {b} ÷ ({c} + {d})"], div_nums),
        ("{a} × ({b} + {c})", ["noparen"], ["{a} × {b}"], lambda r: (R(3, 6), R(11, 18) * 100, R(2, 9) * 50)),
        ("({a} − {b}) ÷ {c}", ["noparen"], ["{a} ÷ {c}"], lambda r: (R(10, 20) * 100, R(1, 9) * 40, 8)),
        ("{a} + {b} × ({c} − {d})", ["noparen", "ltr"], [], lambda r: (R(5, 20), R(3, 9), R(10, 15), R(2, 8))),
        ("({a} + {b}) × {c} − {d}", ["noparen", "ltr"], ["({a} + {b}) × ({c} − {d})"], lambda r: (R(4, 9), R(2, 8), R(3, 6), R(5, 15))),
    ]
    for k, (t, modes, extra, mk) in enumerate(T):
        names = fields(t)

        def ok(d, t=t, names=names, modes=modes, extra=extra):
            m = dict(zip(names, map(f, d)))
            s = t.format(**m)
            v = ev(s)
            if v is None or v <= 1:
                return False
            return enough(s, v, modes, [x.format(**m) for x in extra]) and len(set(d)) == len(d)

        d = gen_nums(rnd, mk, ok, used)
        m = dict(zip(names, map(f, d)))
        s = t.format(**m)
        its.append(eval_item(s, k, modes, [x.format(**m) for x in extra]))
    # which expression has the value?  (all four use the same numbers)
    for a, b, c in [(2, 8, 7), (4, 9, 3), (6, 10, 4)]:
        good = "%d × (%d + %d)" % (a, b, c)
        bad = ["%d × %d + %d" % (a, b, c), "%d + %d × %d" % (b, c, a), "(%d + %d) × %d" % (a, b, c)]
        v = val(good)
        assert all(val(x) != v for x in bad)
        its.append(mcq("Which expression has a value of %s?" % B(f(v)), good, bad,
                       "%s. Without the parentheses, %s = %s, because you multiply before you add."
                       % (chain(good), bad[0], f(val(bad[0])))))
    # which equation is true?
    for a, b, c in [(3, 12, 5), (5, 4, 6)]:
        e1 = "(%d + %d) × %d" % (b, c, a) if a == 3 else "%d × (%d − %d)" % (a + 4, b + 6, c)
        v = val(e1)
        np = ev(e1, "noparen")
        e2 = render(strip(tokens(e1)))
        good = "%s = %s" % (e1, f(v))
        bad = ["%s = %s" % (e1, f(np)), "%s = %s" % (e2, f(v)), "%s = %s" % (e1, f(v + 10))]
        assert np != v and ev(e2) != v
        its.append(mcq("Which equation is true?", good, bad,
                       "%s. Without the parentheses the value changes: %s = %s." % (chain(e1), e2, f(np))))
    # do the parentheses change anything?
    good = "6 + 4 × 5"
    its.append(mcq("Which expression has the same value as %s?" % B("6 + (4 × 5)"), good,
                   ["(6 + 4) × 5", "6 × 4 + 5", "6 + 4 + 5"],
                   "6 + (4 × 5) = 6 + 20 = 26. 6 + 4 × 5 is also 26, because you multiply first anyway. "
                   "(6 + 4) × 5 = 50 is different."))
    assert val("6 + (4 × 5)") == val(good) and all(val(x) != 26 for x in ["(6 + 4) × 5", "6 × 4 + 5", "6 + 4 + 5"])
    assert len(its) == 20, len(its)
    return {"title": "Parentheses first", "items": its}


# ------------------------------------------------------------ set 2: order of operations without parentheses
def set_order(rnd, P):
    its = []
    used = set()
    R = rnd.randint
    T = [
        ("{a} + {b} × {c}", ["ltr"], ["{a} + {b} + {c}"], lambda r: (R(2, 9), R(3, 9), R(3, 9))),
        ("{a} − {b} × {c}", ["ltr"], ["{a} − {b} − {c}"], lambda r: (R(30, 60), R(3, 6), R(3, 6))),
        ("{a} × {b} + {c} × {d}", ["ltr"], ["{a} × ({b} + {c}) × {d}"], lambda r: (R(3, 8), R(3, 8), R(2, 6), R(3, 7))),
        ("{a} + {b} ÷ {c}", ["ltr"], ["{a} + {b} + {c}"], lambda r: (R(6, 20), R(3, 9) * 4, 4)),
        ("{a} ÷ {b} × {c}", ["mulfirst"], ["{b} × {c}"], lambda r: (R(4, 9) * 12, R(2, 3) * 2, 2)),
        ("{a} ÷ {b} × {c}", ["mulfirst"], ["{b} × {c}"], lambda r: (R(3, 9) * 18, 3, 2)),
        ("{a} − {b} + {c}", ["addfirst"], ["{b} + {c}"], lambda r: (R(20, 40), R(6, 15), R(3, 9))),
        ("{a} − {b} + {c}", ["addfirst"], ["{a} + {b} + {c}"], lambda r: (R(50, 90), R(20, 30), R(5, 15))),
        ("{a} × {b} − {c} ÷ {d}", ["ltr"], ["{a} × ({b} − {c}) ÷ {d}"], lambda r: (R(4, 9), R(5, 9), R(2, 6) * 3, 3)),
        ("{a} − {b} ÷ {c} + {d}", ["ltr", "addfirst"], [], lambda r: (R(15, 30), R(2, 6) * 4, 4, R(2, 8))),
        ("{a} − {b} + {c} − {d}", ["addfirst", "rtl"], [], lambda r: (R(30, 60), R(8, 15), R(10, 20), R(2, 9))),
        ("{a} − {b} ÷ {c} × {d}", ["mulfirst", "ltr"], [], lambda r: (R(40, 90), R(2, 5) * 12, R(2, 3) * 2, 2)),
        ("{a} + {b} × {c} − {d}", ["ltr", "rev"], [], lambda r: (R(5, 20), R(3, 9), R(3, 9), R(2, 8))),
        ("{a} × {b} − {c} + {d}", ["addfirst", "rev"], [], lambda r: (R(3, 9), R(12, 45) * 10, R(30, 90), R(10, 60))),
    ]
    for k, (t, modes, extra, mk) in enumerate(T):
        names = fields(t)

        def ok(d, t=t, names=names, modes=modes, extra=extra):
            m = dict(zip(names, map(f, d)))
            s = t.format(**m)
            v = ev(s)
            if v is None or v <= 1:
                return False
            return enough(s, v, modes, [x.format(**m) for x in extra]) and len(set(d)) == len(d)

        d = gen_nums(rnd, mk, ok, used)
        m = dict(zip(names, map(f, d)))
        s = t.format(**m)
        its.append(eval_item(s, k, modes, [x.format(**m) for x in extra]))
    # which part first?
    FIRST = [("18 − 6 ÷ 3 + 2", "6 ÷ 3", ["18 − 6", "3 + 2"],
              "Divide first because ÷ comes before + and −: 18 − 2 + 2. Then go left to right: 16 + 2 = 18."),
             ("40 − 8 + 2 × 5", "2 × 5", ["40 − 8", "8 + 2"],
              "Multiply first: 40 − 8 + 10. Then go left to right: 32 + 10 = 42."),
             ("30 ÷ 5 × 2 + 4", "30 ÷ 5", ["5 × 2", "2 + 4"],
              "× and ÷ are on the same level, so go left to right: 30 ÷ 5 = 6 first. Then 6 × 2 = 12, and 12 + 4 = 16.")]
    for s, good, bad, e in FIRST:
        v = val(s)
        assert str(v) in e.split()[-1].rstrip(".")
        its.append(mcq("Which part of %s do you work out first?" % B(s), good, bad + ["Any part first"], e))
    # check a claim: (expression, the mistake, other wrong values, what went wrong)
    CLAIM = [("24 ÷ 4 × 2", "mulfirst", ["24 ÷ 4", "4 × 2"], "multiplied before dividing, but × and ÷ go from left to right"),
             ("6 + 4 × 5", "ltr", ["4 × 5", "6 + 4 + 5"], "added first, but you multiply before you add"),
             ("20 − 6 + 4", "addfirst", ["20 − 6", "20 + 6 + 4"], "added before subtracting, but + and − go from left to right")]
    for s, mode, other, what in CLAIM:
        n, he, his = P.next()
        v, w = val(s), ev(s, mode)
        ws = [val(x) for x in other]
        assert len({v, w} | set(ws)) == 4
        its.append(mcq("%s says %s = %s. Is %s right?" % (n, B(s), f(w), he), "No, it is %s" % f(v),
                       ["Yes, it is %s" % f(w)] + ["No, it is %s" % f(x) for x in ws],
                       "%s. %s %s." % (chain(s), n, what)))
    assert len(its) == 20, len(its)
    return {"title": "Order of operations: × and ÷ before + and −", "items": its}


# ------------------------------------------------------------ set 3: brackets and braces
def set_nested(rnd, P):
    its = []
    used = set()
    R = rnd.randint
    M = ["noinner", "noparen", "noparen_ltr"]
    T = [
        ("[{a} + ({b} × {c})] × {d}", M, ["[{a} + {b}] × {c} × {d}"], lambda r: (R(2, 9), R(3, 6), R(2, 5), R(3, 6))),
        ("{{{a} − [{b} × ({c} + {d})]}}", M, ["{a} − {b} × {c}"], lambda r: (R(40, 90), R(2, 5), R(2, 6), R(1, 4))),
        ("{a} × [{b} − ({c} − {d})]", M, [], lambda r: (R(3, 7), R(15, 25), R(8, 14), R(2, 7))),
        ("[({a} + {b}) ÷ {c}] × {d}", M, ["({a} + {b}) ÷ ({c} × {d})"], lambda r: (R(3, 7) * 4, R(1, 3) * 4, 4, R(2, 5))),
        ("{a} + [{b} × ({c} − {d})]", M, [], lambda r: (R(5, 20), R(3, 7), R(9, 14), R(2, 7))),
        ("{{[{a} × ({b} − {c})] + {d}}} ÷ {e}", M, ["[{a} × ({b} − {c})] + {d}"], lambda r: (R(3, 8), R(8, 12), R(2, 5), R(2, 9), R(2, 5))),
        ("[{a} − ({b} + {c})] × {d}", M, [], lambda r: (R(25, 40), R(5, 10), R(2, 8), R(3, 5))),
        ("{a} − [({b} + {c}) × {d}]", M, [], lambda r: (R(60, 99), R(3, 7), R(2, 6), R(3, 5))),
        ("{a} × {{{b} + [{c} − ({d} × {e})]}}", M, [], lambda r: (R(2, 4), R(5, 15), R(20, 40), R(2, 5), R(2, 5))),
        ("[{a} − ({b} × {c})] ÷ {d}", M, ["{a} ÷ {d}"], lambda r: (R(10, 16) * 100, 25, 8, 4)),
        ("{{{a} ÷ [{b} × ({c} − {d})]}} + {e}", M, ["{a} ÷ {b}"], lambda r: (R(4, 9) * 24, 2, R(6, 9), R(2, 5), R(2, 9))),
        ("[{a} × ({b} + {c})] − [{d} × ({e} − {g})]", M, [], lambda r: (R(4, 8), R(5, 9), R(2, 6), R(2, 5), R(6, 10), R(1, 5))),
        ("{a} × [{b} − ({c} + {d})]", M, [], lambda r: (R(2, 5) * 25, R(60, 90), R(10, 25), R(5, 15))),
        ("{{[({a} + {b}) × {c}] − {d}}} ÷ {e}", M, [], lambda r: (R(2, 6), R(2, 6), R(3, 6), R(2, 9), R(2, 5))),
    ]
    for k, (t, modes, extra, mk) in enumerate(T):
        names = fields(t)

        def ok(d, t=t, names=names, modes=modes, extra=extra):
            m = dict(zip(names, map(f, d)))
            s = t.format(**m)
            v = ev(s)
            if v is None or v <= 1 or v > 2000:
                return False
            ms = mistakes(s, modes, [x.format(**m) for x in extra])
            return len(ms) >= 3 and ms[0][1] in WHY.values() and len(set(d)) == len(d)

        d = gen_nums(rnd, mk, ok, used)
        m = dict(zip(names, map(f, d)))
        s = t.format(**m)
        its.append(eval_item(s, k, modes, [x.format(**m) for x in extra],
                             note="Work from the inside out."))
    # which part first?
    FIRST = [("{20 − [2 × (3 + 1)]}", "3 + 1", ["20 − 2", "2 × 3"]),
             ("[30 − (4 × 5)] ÷ 2", "4 × 5", ["30 − 4", "5 ÷ 2"]),
             ("6 × [10 − (2 + 5)]", "2 + 5", ["6 × 10", "10 − 2"])]
    for s, good, bad in FIRST:
        its.append(mcq("Which part of %s do you work out first?" % B(s), good, bad + ["Any part first"],
                       "Start with the innermost grouping symbols, the parentheses: %s. Then work outward: %s." % (good, chain(s))))
    # check a claim
    # check a claim: (expression, what the student did, the claimed value as an expression, other wrong values)
    CLAIM = [("[3 + (4 × 2)] × 5", "skipped the grouping symbols and multiplied first", "3 + 4 × 2 × 5",
              ["3 + (4 × 2)", "(3 + 4) × 2 × 5"]),
             ("{30 − [3 × (2 + 4)]}", "skipped the parentheses inside the brackets", "{30 − [3 × 2 + 4]}",
              ["3 × (2 + 4)", "30 − 3 × 2 + 4"]),
             ("[(12 + 6) ÷ 3] × 2", "skipped the parentheses and divided 6 ÷ 3 first", "12 + 6 ÷ 3 × 2",
              ["(12 + 6) ÷ 3", "(12 + 6) ÷ (3 × 2)"])]
    for s, said, claim, other in CLAIM:
        n, he, his = P.next()
        v, w = val(s), val(claim)
        ws = [val(x) for x in other]
        assert len({v, w} | set(ws)) == 4, s
        its.append(mcq("%s says %s = %s. Is %s right?" % (n, B(s), f(w), he), "No, it is %s" % f(v),
                       ["Yes, it is %s" % f(w)] + ["No, it is %s" % f(x) for x in ws],
                       "%s. %s %s." % (chain(s), n, said)))
    assert len(its) == 20, len(its)
    return {"title": "Brackets and braces: work from the inside out", "items": its}


# ------------------------------------------------------------ set 4: words <-> expressions, placing parentheses
WORDS = [
    ("Add 8 and 7, then multiply by 2.", "2 × (8 + 7)", ["2 × 8 + 7", "8 + 7 × 2", "2 + 8 × 7"],
     "Add first, so 8 + 7 goes in parentheses. Then multiply by 2: 2 × (8 + 7) = 30. 2 × 8 + 7 would multiply first."),
    ("Subtract 5 from the product of 6 and 9.", "6 × 9 − 5", ["5 − 6 × 9", "6 × (9 − 5)", "6 + 9 − 5"],
     "“The product of 6 and 9” is 6 × 9. “Subtract 5 from” it means take 5 away from it: 6 × 9 − 5 = 49. 5 − 6 × 9 has the order backward."),
    ("Multiply 4 by the sum of 12 and 3.", "4 × (12 + 3)", ["4 × 12 + 3", "4 + 12 × 3", "4 × 12 × 3"],
     "“The sum of 12 and 3” is 12 + 3, and it must be found first, so it goes in parentheses: 4 × (12 + 3) = 60."),
    ("Divide the difference of 30 and 6 by 4.", "(30 − 6) ÷ 4", ["30 − 6 ÷ 4", "4 ÷ (30 − 6)", "30 ÷ 4 − 6"],
     "“The difference of 30 and 6” is 30 − 6. Put it in parentheses so you subtract first, then divide by 4: (30 − 6) ÷ 4 = 6."),
    ("Add 9 to the quotient of 40 and 5.", "40 ÷ 5 + 9", ["40 ÷ (5 + 9)", "9 + 5 ÷ 40", "40 + 5 + 9"],
     "“The quotient of 40 and 5” is 40 ÷ 5. Add 9 to it: 40 ÷ 5 + 9 = 8 + 9 = 17. No parentheses are needed, because ÷ comes first anyway."),
    ("Three times the sum of 15 and 6", "3 × (15 + 6)", ["3 × 15 + 6", "15 + 6 × 3", "3 + 15 + 6"],
     "“Three times” something means 3 × that amount. The amount is the sum 15 + 6, so it goes in parentheses: 3 × (15 + 6) = 63."),
    ("Subtract 8 from 50, then divide by 6.", "(50 − 8) ÷ 6", ["50 − 8 ÷ 6", "(8 − 50) ÷ 6", "50 ÷ 6 − 8"],
     "“Subtract 8 from 50” is 50 − 8, not 8 − 50. It comes first, so it goes in parentheses: (50 − 8) ÷ 6 = 42 ÷ 6 = 7."),
    ("The product of 7 and the difference of 20 and 4", "7 × (20 − 4)", ["7 × 20 − 4", "7 × (4 − 20)", "7 × 4 − 20"],
     "“The difference of 20 and 4” is 20 − 4. Multiply it by 7, so it needs parentheses: 7 × (20 − 4) = 7 × 16 = 112."),
    ("Add the product of 3 and 8 to the product of 5 and 2.", "3 × 8 + 5 × 2", ["3 × (8 + 5) × 2", "(3 + 8) × (5 + 2)", "3 + 8 × 5 + 2"],
     "Each product is a multiplication: 3 × 8 and 5 × 2. Then add them: 3 × 8 + 5 × 2 = 24 + 10 = 34."),
    ("Divide 36 by 4, then subtract the result from 20.", "20 − 36 ÷ 4", ["36 ÷ 4 − 20", "(20 − 36) ÷ 4", "20 − 36 − 4"],
     "36 ÷ 4 is the result. “Subtract the result from 20” means 20 − (36 ÷ 4). Division comes first anyway: 20 − 36 ÷ 4 = 20 − 9 = 11."),
]
TO_WORDS = [
    ("4 × (9 − 2)", "Subtract 2 from 9, then multiply by 4",
     ["Multiply 4 by 9, then subtract 2", "Subtract 9 from 2, then multiply by 4", "Add 9 and 2, then multiply by 4"],
     "The parentheses are worked first: 9 − 2, which is “subtract 2 from 9.” Then the result is multiplied by 4."),
    ("(18 + 6) ÷ 3", "Add 18 and 6, then divide by 3",
     ["Divide 6 by 3, then add 18", "Add 18 and 6, then multiply by 3", "Divide 3 by the sum of 18 and 6"],
     "The parentheses come first: add 18 and 6. Then divide that sum by 3. (18 + 6) ÷ 3 = 24 ÷ 3 = 8."),
    ("20 − 3 × 4", "Subtract the product of 3 and 4 from 20",
     ["Subtract 3 from 20, then multiply by 4", "Subtract 20 from the product of 3 and 4", "Multiply 20 by 3, then subtract 4"],
     "Multiplication comes first, so 3 × 4 is found first. Then it is taken away from 20: 20 − 12 = 8."),
]
PLACE_PATTERNS = [("+", "×", "−"), ("−", "×", "+"), ("×", "+", "×"), ("+", "÷", "×"), ("−", "+", "×"), ("×", "−", "÷"), ("+", "×", "+")]


def placements(n, ops):
    out = []
    for i, j in [(0, 1), (1, 2), (2, 3), (0, 2), (1, 3)]:
        ts = []
        for k in range(4):
            if k == i:
                ts.append("(")
            ts.append(n[k])
            if k == j:
                ts.append(")")
            if k < 3:
                ts.append(ops[k])
        out.append(render(ts))
    return out


def set_words(rnd, P):
    its = []
    for w, good, bad, e in WORDS:
        v = val(good)
        for b in bad:
            assert ev(b) != v, (w, b)
        its.append(mcq("Which expression matches the words?<br>%s" % B(w), good, bad, e))
    for s, good, bad, e in TO_WORDS:
        val(s)
        its.append(mcq("Which words match %s?" % B(s), good, bad, e))
    used = set()
    for ops in PLACE_PATTERNS:
        for _ in range(5000):
            n = [rnd.randint(2, 12) for _ in range(4)]
            if len(set(n)) < 4 or tuple(n) in used:
                continue
            pl = placements(n, ops)
            vs = [ev(p) for p in pl]
            plain = ev(render([n[0], ops[0], n[1], ops[1], n[2], ops[2], n[3]]))
            idx = [i for i, v in enumerate(vs) if v is not None and v > 1 and v != plain and vs.count(v) == 1]
            others = [i for i, v in enumerate(vs) if v is not None and i not in idx[:1] and v not in (plain,)]
            if not idx:
                continue
            t = idx[0]
            others = [i for i in range(5) if i != t and vs[i] is not None and vs[i] != vs[t]]
            if len(others) < 3 or vs[t] > 200:
                continue
            used.add(tuple(n))
            break
        plain_s = render([n[0], ops[0], n[1], ops[1], n[2], ops[2], n[3]])
        rnd.shuffle(others)
        good = pl[t]
        bad = [pl[i] for i in others[:3]]
        its.append(mcq("Where do the parentheses go to make the equation true?<br>%s" % B("%s = %s" % (plain_s, f(vs[t]))),
                       good, bad,
                       "%s. Without parentheses, %s = %s." % (chain(good), plain_s, f(plain))))
    assert len(its) == 20, len(its)
    return {"title": "Write expressions from words and place parentheses", "items": its}


# ------------------------------------------------------------ set 5: interpret without calculating, word problems
def set_interpret(rnd, P):
    its = []
    s1, s0 = "3 × (18,932 + 921)", "18,932 + 921"
    assert val(s1) == 3 * val(s0)
    its.append(mcq("Without calculating, how does %s compare with %s?" % (B(s1), B(s0)), "3 times as large",
                   ["3 more", "921 times as large", "the same"],
                   "3 × (18,932 + 921) is 3 groups of the sum 18,932 + 921, so it is 3 times as large. "
                   "Adding 3 would make it only 3 more."))
    s1, s0 = "(4,520 − 386) ÷ 2", "4,520 − 386"
    assert val(s1) * 2 == val(s0)
    its.append(mcq("Without calculating, how does %s compare with %s?" % (B(s1), B(s0)), "half as large",
                   ["2 less", "twice as large", "386 less"],
                   "Dividing by 2 splits the difference 4,520 − 386 into 2 equal parts, so the value is half as large."))
    s1, s0 = "10 × (73 + 1,409)", "73 + 1,409"
    assert val(s1) == 10 * val(s0)
    its.append(mcq("Without calculating, how does %s compare with %s?" % (B(s1), B(s0)), "10 times as large",
                   ["10 more", "73 times as large", "the same"],
                   "10 × (73 + 1,409) is 10 groups of the sum 73 + 1,409, so it is 10 times as large."))
    s0 = "645 + 317"
    good = "2 × (645 + 317)"
    bad = ["2 × 645 + 317", "645 + 317 + 2", "(645 + 317) ÷ 2"]
    assert val(good) == 2 * val(s0) and all(val(b) != 2 * val(s0) for b in bad)
    its.append(mcq("Which expression is twice as large as %s?" % B(s0), good, bad,
                   "Twice as large means 2 groups of the whole sum, so the sum goes in parentheses: 2 × (645 + 317). "
                   "2 × 645 + 317 doubles only 645."))
    s0 = "9 × 1,206"
    good = "4 × 9 × 1,206"
    bad = ["4 + 9 × 1,206", "9 × 1,206 + 4", "9 × (1,206 + 4)"]
    assert val(good) == 4 * val(s0) and all(val(b) != 4 * val(s0) for b in bad)
    its.append(mcq("Which expression is 4 times as large as %s?" % B(s0), good, bad,
                   "Multiplying 9 × 1,206 by 4 makes it 4 times as large: 4 × 9 × 1,206. Adding 4 makes it only 4 more."))
    a, b = "5 × (2,346 + 78)", "4 × (2,346 + 78)"
    assert val(a) > val(b)
    its.append(mcq("Without calculating, which is greater?", a, [b, "They are equal", "You must calculate"],
                   "Both use the same sum, 2,346 + 78. 5 groups of it are more than 4 groups, so %s is greater." % a))
    a, b = "7 × (468 + 52)", "7 × (468 + 25)"
    assert val(a) > val(b)
    its.append(mcq("Without calculating, which is greater?", a, [b, "They are equal", "You must calculate"],
                   "Both are 7 groups of a sum. 468 + 52 is greater than 468 + 25, so %s is greater." % a))
    a, b = "9,000 − 45 + 12", "9,000 − (45 + 12)"
    assert val(a) > val(b)
    its.append(mcq("Without calculating, which is greater?", a, [b, "They are equal", "You must calculate"],
                   "9,000 − (45 + 12) takes away both 45 and 12. 9,000 − 45 + 12 takes away 45 and then adds 12 back, so it is greater."))
    s1, s0 = "8 × 395 + 8", "8 × 395"
    assert val(s1) == val(s0) + 8
    its.append(mcq("Without calculating, how does %s compare with %s?" % (B(s1), B(s0)), "8 more",
                   ["8 times as large", "395 more", "the same"],
                   "8 × 395 + 8 is 8 × 395 with 8 added, so it is 8 more. The + 8 is not multiplied, because there are no parentheses."))
    n, he, his = P.next()
    s1, s0 = "6 × (250 + 39)", "250 + 39"
    assert val(s1) == 6 * val(s0)
    its.append(mcq("%s says %s is 6 more than %s. Is %s right?" % (n, B(s1), B(s0), he), "No, it is 6 times as large",
                   ["Yes, it is 6 more", "No, it is 39 times as large", "No, they are equal"],
                   "6 × (250 + 39) is 6 groups of 250 + 39, so it is 6 times as large. It would be 6 more only if it were 250 + 39 + 6."))
    # word problems: choose the expression
    WP = []
    n, he, his = P.next()
    WP.append(("%s buys 3 packs of 12 pencils and 5 extra pencils. Which expression shows how many pencils %s buys?" % (n, he),
               "3 × 12 + 5", ["3 × (12 + 5)", "3 + 12 × 5", "(3 + 12) × 5"],
               "3 packs of 12 is 3 × 12. The 5 extra pencils are added once, not to every pack: 3 × 12 + 5 = 36 + 5 = 41."))
    n, he, his = P.next()
    WP.append(("%s has $50. %s buys 4 books that cost $9 each. Which expression shows how much money %s has left?" % (n, cap(he), he),
               "50 − 4 × 9", ["(50 − 4) × 9", "4 × 9 − 50", "50 − 4 + 9"],
               "The books cost 4 × 9. Take that away from 50: 50 − 4 × 9 = 50 − 36 = 14. Multiplication comes first, so no parentheses are needed."))
    WP.append(("28 students and 4 teachers split into 2 equal groups for a field trip. Which expression shows how many people are in each group?",
               "(28 + 4) ÷ 2", ["28 + 4 ÷ 2", "28 ÷ 2 + 4", "2 ÷ (28 + 4)"],
               "First find everyone: 28 + 4. Then split into 2 groups. The sum must be found first, so it goes in parentheses: (28 + 4) ÷ 2 = 16."))
    WP.append(("Each of 6 tables has 4 red cups and 5 blue cups. Which expression shows how many cups there are in all?",
               "6 × (4 + 5)", ["6 × 4 + 5", "6 + 4 + 5", "6 + 4 × 5"],
               "Each table has 4 + 5 cups, and there are 6 tables: 6 × (4 + 5) = 6 × 9 = 54. 6 × 4 + 5 forgets the blue cups on 5 of the tables."))
    n, he, his = P.next()
    WP.append(("%s saves $12 a week for 5 weeks. Then %s spends $18. Which expression shows how much money %s has now?" % (n, he, he),
               "12 × 5 − 18", ["12 × 5 + 18", "18 − 12 × 5", "5 × 18 − 12"],
               "%s saves 12 × 5 dollars. Then $18 is taken away: 12 × 5 − 18 = 60 − 18 = 42. 18 − 12 × 5 has the order backward." % n))
    n, he, his = P.next()
    WP.append(("%s had 120 stickers. %s gave 15 stickers to each of 4 friends. Which expression shows how many stickers %s has left?" % (n, cap(he), he),
               "120 − 4 × 15", ["(120 − 4) × 15", "120 − 4 − 15", "4 × 15 − 120"],
               "%s gave away 4 × 15 stickers. Take that from 120: 120 − 4 × 15 = 120 − 60 = 60." % n))
    for q, good, bad, e in WP:
        v = val(good)
        assert all(ev(b) != v for b in bad), q
        assert str(v) in e, (q, v)
        its.append(mcq(q, good, bad, e))
    # word problems: find the value
    VP = [
        ("A movie ticket costs $9 and a bag of popcorn costs $5. A family of 4 gets a ticket and a bag of popcorn for each person. "
         "They pay with a $100 bill. How much change do they get?", "100 − 4 × (9 + 5)", "$",
         ["100 − 4 × 9 + 5", "4 × (9 + 5)", "100 − 4 × 9 − 5"],
         "Not $69: that skips the parentheses. Not $56: that is the cost, not the change."),
        ("A school orders 12 boxes of 24 markers. 30 markers are broken. The rest are shared equally by 6 classes. "
         "How many markers does each class get?", "(12 × 24 − 30) ÷ 6", ("marker", "markers"),
         ["12 × 24 − 30 ÷ 6", "12 × 24 ÷ 6", "12 × 24 − 30"],
         "The subtraction must come before the division, so it goes in parentheses. Not 283: that divides before subtracting."),
        ("A bakery makes 8 trays of 15 muffins and 4 trays of 12 muffins. At the end of the day, 20 muffins are left. "
         "How many muffins did the bakery sell?", "8 × 15 + 4 × 12 − 20", ("muffin", "muffins"),
         ["8 × 15 + 4 × 12", "8 × 15 + 4 × 12 + 20", "(8 × 15 + 4) × 12 − 20"],
         "Find both products first and add them, then subtract the 20 muffins that were left. 168 is all the muffins, not the ones sold."),
        ("A class trip costs $1,250 for each adult and $875 for each child. How much do 3 adults and 2 children pay in all?",
         "3 × 1,250 + 2 × 875", "$",
         ["3 × 1,250 + 875", "(3 + 2) × 1,250", "(1,250 + 875) × 5"],
         "Multiply each price by the number of people first, then add. Not $4,625: that counts only 1 child."),
    ]
    for q, s, u, bad, note in VP:
        v = val(s)
        U = (lambda x: "$" + f(x)) if u == "$" else (lambda x, u=u: "%s %s" % (f(x), u[0] if x == 1 else u[1]))
        cands = [U(ev(b)) for b in bad if ev(b) is not None and ev(b) != v and ev(b) > 0]
        its.append(mcq(q, U(v), cands,
                       "Write one expression and evaluate it: %s. %s Answer: %s." % (chain(s), note, U(v))))
    assert len(its) == 20, len(its)
    return {"title": "Interpret expressions and solve word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def inside_out_svg():
    """{20 − [2 × (3 + 1)]} worked from the inside out; the part worked next is red."""
    rows = [("", ["{20 − [2 × ", ("(3 + 1)", RED), "]}"], "parentheses first"),
            ("= ", ["{20 − ", ("[2 × 4]", RED), "}"], "then brackets"),
            ("= ", [("{20 − 8}", RED)], "then braces"),
            ("= ", [("12", GREEN)], "")]
    fs, lh = 22, 40
    W, H = 420, 16 + lh * len(rows)
    out = []
    for i, (eq, parts, note) in enumerate(rows):
        y = 36 + i * lh
        span = "".join("<tspan fill='%s'>%s</tspan>" % ((p[1], p[0]) if isinstance(p, tuple) else (INK, p)) for p in parts)
        out.append("<text x='34' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='end'>%s</text>" % (y, fs, INK, eq.strip()))
        out.append("<text x='40' y='%d' font-size='%d' font-weight='700'>%s</text>" % (y, fs, span))
        if note:
            out.append("<text x='%d' y='%d' font-size='15' fill='%s'>%s</text>" % (W - 8, y - 2, BLUE, note))
    body = "".join(out).replace("<text x='%d'" % (W - 8), "<text text-anchor='end' x='%d'" % (W - 8))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' role='img' "
            "aria-label='working an expression from the inside out'><g font-family='%s'>%s</g></svg>" % (W, H, W, H, FONT, body))


def body_html():
    assert val("{20 − [2 × (3 + 1)]}") == 12 and val("5 + 3 × 4") == 17 and val("24 ÷ 4 × 2") == 12
    return (
        "<h2>What is a numerical expression?</h2>"
        "<p>A numerical expression is numbers and operation signs with no equal sign, like 2 × (8 + 7). "
        "To <b>evaluate</b> an expression means to find its value. Everyone must get the same value, so we follow one order.</p>"
        "<h2>The order of operations</h2>" +
        table(["Step", "Do this", "Example"], [
            ["1", "Grouping symbols ( ), [ ], { } first, the innermost first", "2 × (8 + 7) = 2 × 15 = 30"],
            ["2", "× and ÷, from left to right", "24 ÷ 4 × 2 = 6 × 2 = 12"],
            ["3", "+ and −, from left to right", "10 − 4 + 3 = 6 + 3 = 9"],
        ]) +
        ex("Example", "Evaluate 5 + 3 × 4.", "There are no grouping symbols. Multiply first: 3 × 4 = 12. Then add: 5 + 12 = 17.", "17 (not 32)") +
        "<h2>Brackets and braces: work from the inside out</h2>"
        "<p>When one group is inside another, parentheses ( ) go inside, brackets [ ] go around them, "
        "and braces { } go around the brackets. Start with the innermost group.</p>"
        "<figure class='sn-fig'>" + inside_out_svg() +
        "<figcaption>{20 − [2 × (3 + 1)]}: 3 + 1 = 4, then 2 × 4 = 8, then 20 − 8 = 12.</figcaption></figure>"
        "<h2>Write an expression from words</h2>"
        "<p>Find the operation words. If a part must be done first but would not be done first by the order of operations, "
        "put it in parentheses.</p>" +
        table(["Words", "Expression"], [
            ["the sum of 8 and 7", "8 + 7"],
            ["the difference of 20 and 4", "20 − 4"],
            ["the product of 6 and 9", "6 × 9"],
            ["the quotient of 40 and 5", "40 ÷ 5"],
            ["subtract 5 from 12", "12 − 5 (not 5 − 12)"],
            ["add 8 and 7, then multiply by 2", "2 × (8 + 7)"],
            ["subtract 5 from the product of 6 and 9", "6 × 9 − 5"],
        ]) +
        "<h2>Interpret an expression without calculating</h2>"
        "<p>You can compare expressions by looking at their structure. 3 × (18,932 + 921) is <b>3 times as large</b> as "
        "18,932 + 921, because it is 3 groups of that sum. (4,520 − 386) ÷ 2 is <b>half as large</b> as 4,520 − 386.</p>" +
        ex("Example", "Which is greater: 7 × (468 + 52) or 7 × (468 + 25)?",
           "Both are 7 groups of a sum, and 468 + 52 is the greater sum.", "7 × (468 + 52)") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["5 + 3 × 4 = 8 × 4 = 32", "Multiply before you add: 5 + 12 = 17"],
            ["24 ÷ 4 × 2 = 24 ÷ 8 = 3", "× and ÷ are on the same level. Go left to right: 6 × 2 = 12"],
            ["20 − 6 + 4 = 20 − 10 = 10", "+ and − are on the same level. Go left to right: 14 + 4 = 18"],
            ["Starting with the brackets, not the parentheses inside them", "Work from the innermost group outward"],
            ["“Subtract 5 from 12” written as 5 − 12", "The number you subtract from comes first: 12 − 5"],
            ["“Twice the sum of 6 and 4” written as 2 × 6 + 4", "Put the sum in parentheses: 2 × (6 + 4)"],
        ])
    )


FAQ = [
    {"q": "What is the order of operations in 5th grade?",
     "a": "Work inside parentheses, brackets and braces first, starting with the innermost group. Then multiply and divide from left to right, and then add and subtract from left to right. (Some classes call this PEMDAS; exponents come in Grade 6.)"},
    {"q": "What is the difference between parentheses, brackets and braces?",
     "a": "They all mean “do this part first.” Parentheses ( ) go inside, brackets [ ] go around them, and braces { } go around brackets, so you can see which group to start with: {20 − [2 × (3 + 1)]} = 12."},
    {"q": "Does multiplication always come before division?",
     "a": "No. Multiplication and division are on the same level, so you do them in order from left to right: 24 ÷ 4 × 2 = 6 × 2 = 12. Addition and subtraction work the same way: 20 − 6 + 4 = 18."},
    {"q": "What does it mean to interpret an expression without evaluating it?",
     "a": "It means telling what an expression shows without finding its value. For example, 3 × (18,932 + 921) is 3 times as large as 18,932 + 921, because it is 3 groups of that sum."},
]


def gen():
    rnd = random.Random(507)
    P = People(rnd)
    sets = [set_parentheses(rnd, P), set_order(rnd, P), set_nested(rnd, P), set_words(rnd, P), set_interpret(rnd, P)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "us", "subject": "math", "grade": "grade-5", "slug": "numerical-expressions", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Numerical Expressions and the Order of Operations",
        "seo_title": "Grade 5 Numerical Expressions Worksheets: Order of Operations with Parentheses, Brackets and Braces",
        "short_title": "Numerical expressions",
        "domain": "Operations and Algebraic Thinking",
        "standard_code": "5.OA.A.1–2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/5/OA/A/",
        "standard_text": "Use parentheses, brackets, or braces in numerical expressions, and evaluate expressions with these symbols. Write simple expressions that record calculations with numbers, and interpret numerical expressions without evaluating them. For example, express the calculation “add 8 and 7, then multiply by 2” as 2 × (8 + 7). Recognize that 3 × (18,932 + 921) is three times as large as 18,932 + 921, without having to calculate the indicated sum or product.",
        "meta_desc": "Free Grade 5 numerical expressions worksheets: evaluate expressions with parentheses, brackets and braces, use the order of operations, write expressions from words, and compare expressions without calculating. 100 practice questions with step-by-step answers.",
        "key_big": "Grouping symbols first, from the inside out. Then × and ÷, then + and −, each from left to right.",
        "key_sub": "5 + 3 × 4 = 5 + 12 = 17, not 32. 24 ÷ 4 × 2 = 6 × 2 = 12. 3 × (18,932 + 921) is 3 times as large as 18,932 + 921, with no calculating needed.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
