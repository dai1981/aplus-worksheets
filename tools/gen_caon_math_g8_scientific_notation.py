# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 8 Math: Scientific Notation
(Ontario Curriculum, Grades 1-8: Mathematics, 2020 - Grade 8, Number B1.1, with Spatial Sense E2.1 prefixes)
  python3 tools/gen_caon_math_g8_scientific_notation.py
Powers of ten with positive and negative exponents, large and small numbers in scientific notation,
comparing and ordering, and metric prefixes (mega, giga, tera, micro, nano, pico) in real contexts.
Numbers: 4-digit numbers have no separator; 5 or more digits use a no-break space (150 000 000). Never commas.
Negative exponents use the real minus sign (U+2212).
Every value is checked with decimal.Decimal (never float).
Wrong answers come from real mistakes: counting digits instead of places (10 000 = 10^5), a positive exponent
for a small number, counting only the zeros after the point (0.0045 = 4.5 x 10^-2), 10^4 = 40, 10^-2 = -100,
leaving 32 x 10^5 unchanged or adjusting the exponent the wrong way, comparing only the first factor
(9.8 x 10^4 > 3.1 x 10^5), and mixing up the prefixes (micro / milli / nano).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal as Dm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-8")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
BLUE = "#1f5fa8"
INK = "#2b2b2b"
GREY = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
MINUS = "−"


# ------------------------------------------------------------ number helpers
def E(e):
    """Exponent text with the real minus sign."""
    return str(e).replace("-", MINUS)


def p10(e):
    return "10<sup>%s</sup>" % E(e)


def sci(m, e):
    return "%s × %s" % (m, p10(e))


def V(m, e=0):
    return Dm(str(m)).scaleb(e)


def std(d):
    """Standard form: 150 000 000, 0.0045, 4700 (no-break spaces in 5+ digit whole parts)."""
    d = Dm(d)
    s = format(d, "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    neg = s.startswith("-")
    s = s.lstrip("-")
    ip, _, fp = s.partition(".")
    if len(ip) > 4:
        g = []
        while ip:
            g.insert(0, ip[-3:])
            ip = ip[:-3]
        ip = NB.join(g)
    return (MINUS if neg else "") + ip + ("." + fp if fp else "")


def is_sci(m):
    return Dm(1) <= Dm(str(m)) < Dm(10)


def places(k):
    return "%d place%s" % (k, "" if k == 1 else "s")


def strip(x):
    return re.sub(r"<[^>]+>", "", x)


def mcq(q, choices, e):
    """choices: list of (html, value or None); the first one is correct. No two choices equal in value."""
    assert len(choices) == 4, (q, choices)
    ch = [str(c) for c, _ in choices]
    assert len(set(strip(x) for x in ch)) == 4, (q, ch)
    vs = [v for _, v in choices if v is not None]
    assert len(set(vs)) == len(vs), (q, ch)
    return {"q": q, "c": ch, "a": 0, "e": e}


def sc(m, e):
    return (sci(m, e), V(m, e))


def sd(d):
    return (std(d), Dm(d))


def pw(e):
    return (p10(e), V(1, e))


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)


# ------------------------------------------------------------ figures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def pow_text(x, y, e, col=INK, bold=True):
    """10 with a raised exponent, centred near x (base 17px, exponent 14px)."""
    ee = E(e)
    w = 19 + 8 * len(ee)
    x0 = x - w / 2.0
    return ("<text x='%.1f' y='%.1f' font-size='17'%s fill='%s'>10<tspan dy='-7' font-size='14'>%s</tspan></text>"
            % (x0, y, " font-weight='700'" if bold else "", col, ee))


def ladder_svg(lo, hi, labels, dot=None, names=None, step=1, gap=60):
    """Powers-of-ten scale: a tick for every exponent lo..hi (by step), 10^e written at `labels`,
    prefix names under the ticks (names: {e: name}), red dot at exponent `dot`."""
    es = list(range(lo, hi + 1, step))
    L = 34
    W = 2 * L + (len(es) - 1) * gap
    Y = 50 if dot is not None else 42
    H = Y + (52 if names else 16)
    if labels is None:
        labels = es

    def X(e):
        return L + (e - lo) / step * gap

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 22, Y, W - L + 22, Y, INK),
         "<path d='M%d %d l-9 -5 v10 Z' fill='%s'/>" % (W - L + 26, Y, INK),
         "<path d='M%d %d l9 -5 v10 Z' fill='%s'/>" % (L - 26, Y, INK)]
    for e in es:
        big = e in labels
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(e), Y - 8, X(e), Y + 8, INK, "1.8" if big else "1.2"))
        if big:
            s.append(pow_text(X(e), Y - 16, e, col=GREEN))
        if names and e in names:
            s.append(text(X(e), Y + 28, names[e], 14, col=BLUE, bold=True))
    if dot is not None:
        s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X(dot), Y, RED))
    return svg_wrap(W, H, "".join(s), "powers of ten scale from 10 to the %s to 10 to the %s" % (E(lo), E(hi)))


def hop_svg(chars, start, end, caption):
    """Digits in a row; the decimal point moves from boundary `start` to boundary `end` (arcs = places)."""
    CW = 30
    L = 16
    n_ = len(chars)
    W = 2 * L + n_ * CW
    Y = 78
    H = Y + 34

    def bx(k):
        return L + k * CW

    s = []
    for i, ch in enumerate(chars):
        s.append(text(L + i * CW + CW / 2.0, Y, ch, 26, bold=True))
    # old point (grey) and new point (red)
    s.append("<circle cx='%.1f' cy='%d' r='3.6' fill='%s'/>" % (bx(start), Y + 1, GREY))
    s.append("<circle cx='%.1f' cy='%d' r='4.6' fill='%s'/>" % (bx(end), Y + 1, RED))
    step = -1 if end < start else 1
    k = start
    while k != end:
        a, b = bx(k), bx(k + step)
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                 % (a, Y - 26, (a + b) / 2.0, Y - 52, b, Y - 28, RED))
        s.append("<path d='M%.1f %d l-5 -8 h10 Z' fill='%s'/>" % (b, Y - 22, RED))
        k += step
    s.append(text(W / 2.0, Y + 28, caption, 15, col=BLUE, bold=True))
    return svg_wrap(W, H, "".join(s), "decimal point moving %d places" % abs(end - start))


def hop_big_lesson():
    return hop_svg(list("3200000"), 7, 1, "6 places left: 3.2 × 10⁶")


def hop_small_lesson():
    return hop_svg(list("00045"), 1, 4, "3 places right: 4.5 × 10⁻³")


# ------------------------------------------------------------ set 1: powers of ten
def set_powers():
    its = []
    # 10^e as a standard number
    for e, w in [(4, [40, 1000, 100000]), (6, [60, 100000, 10000000]),
                 (-2, ["-20", "-100", "0.001"]), (-5, ["-50", "-100000", "0.000001"])]:
        mul = ("10 × " * abs(e))[:-3]
        if e > 0:
            ex_ = "%s = %s. That is 1 followed by %d zeros (not 10 × %d)." % (p10(e), mul, e, e)
        else:
            ex_ = ("A negative exponent means divide: %s = 1 ÷ %s = %s. It is a small positive number, "
                   "not a negative number." % (p10(e), std(V(1, -e)), std(V(1, e))))
        its.append(mcq("Write %s as a standard number." % p10(e),
                       [sd(V(1, e))] + [sd(Dm(str(x))) for x in w], ex_))
    # standard number as a power of ten
    for d, e, w in [("10000", 4, [5, -4, 3]), ("100000000", 8, [9, 7, -8]),
                    ("0.001", -3, [3, -2, -4]), ("0.000001", -6, [6, -5, -7])]:
        if e > 0:
            ex_ = "%s is 1 followed by %d zeros, so it is %s. Count the zeros, not all the digits." % (std(Dm(d)), e, p10(e))
        else:
            ex_ = ("Move the decimal point %s right to reach 1. So %s = %s. "
                   "Small numbers have negative exponents." % (places(-e), std(Dm(d)), p10(e)))
        its.append(mcq("Write %s as a power of ten." % std(Dm(d)), [pw(e)] + [pw(x) for x in w], ex_))
    its.append(mcq("What is the value of %s?" % p10(0), [sd(1), sd(0), sd(10), sd("0.1")],
                   "Any non-zero number to the power 0 is 1. Pattern: 10<sup>2</sup> = 100, 10<sup>1</sup> = 10, 10<sup>0</sup> = 1."))
    its.append(mcq("Write 10 × 10 × 10 × 10 × 10 × 10 × 10 as a power of ten.",
                   [pw(7), pw(6), pw(8), sd(70)],
                   "There are seven 10s multiplied together, so the exponent is 7: 10<sup>7</sup>."))
    its.append(mcq("Write <span class='fr'><span class='fn'>1</span><span class='fd'>1000</span></span> as a power of ten.",
                   [pw(-3), pw(3), pw(-4), sd("-1000")],
                   "1000 = 10<sup>3</sup>, so 1 ÷ 1000 = 10<sup>" + E(-3) + "</sup>."))
    its.append(mcq("Which number is the same as 10<sup>%s</sup>?" % E(-1),
                   [sd("0.1"), sd("-10"), sd("0.01"), sd("-1")],
                   "10<sup>" + E(-1) + "</sup> = 1 ÷ 10 = 0.1. The minus sign in the exponent does not make the number negative."))
    # multiply by a power of ten
    for m, e, w in [("4.7", 3, ["470", "47000", "14.1"]), ("8", 5, ["80000", "8000000", "40"]),
                    ("6.2", -2, ["0.62", "0.0062", "620"]), ("3.9", -4, ["0.0039", "0.000039", "39000"])]:
        if e > 0:
            ex_ = "Multiplying by %s moves the decimal point %s right: %s." % (p10(e), places(e), std(V(m, e)))
        else:
            ex_ = "Multiplying by %s moves the decimal point %s left: %s." % (p10(e), places(-e), std(V(m, e)))
        its.append(mcq("%s = ?" % sci(m, e), [sd(V(m, e))] + [sd(Dm(x)) for x in w], ex_))
    # powers-of-ten scale
    for dot, w in [(-2, ["0.1", "0.001", "100"]), (2, ["1000", "10", "0.01"])]:
        q = ("Each tick on this scale is 10 times the tick to its left. "
             "Which number is at the red dot?" + fig(ladder_svg(-3, 3, [-3, 0, 3], dot=dot)))
        ex_ = ("The dot is %s %s of 10<sup>0</sup> = 1, so it is at %s = %s."
               % (places(abs(dot)).replace("place", "tick"), "right" if dot > 0 else "left", p10(dot), std(V(1, dot))))
        its.append(mcq(q, [sd(V(1, dot))] + [sd(Dm(x)) for x in w], ex_))
    fr4 = lambda d: "<span class='fr'><span class='fn'>1</span><span class='fd'>%s</span></span>" % std(Dm(d))
    its.append(mcq("Which number is the same as 10<sup>%s</sup>?" % E(-4),
                   [(fr4(10000), V(1, -4)), (std(Dm(-10000)), Dm(-10000)), (std(Dm(-40)), Dm(-40)), (fr4(1000), V(1, -3))],
                   "10<sup>" + E(-4) + "</sup> = 1 ÷ 10<sup>4</sup> = <span class='fr'><span class='fn'>1</span><span class='fd'>10 000</span></span> = 0.0001."))
    its.append(mcq("Which number is the greatest?", [pw(-1), pw(-7), pw(-4), pw(-9)],
                   "10<sup>" + E(-1) + "</sup> = 0.1 is the greatest. With negative exponents, the exponent closer to 0 "
                   "gives the bigger number: 0.1 &gt; 0.0001 &gt; 0.0000001."))
    order = [0, 1, 9, 4, 5, 8, 2, 3, 11, 16, 17, 6, 7, 10, 18, 19, 12, 13, 14, 15]
    its = [its[i] for i in order]
    return {"title": "Powers of ten: positive and negative exponents", "items": its}


# ------------------------------------------------------------ set 2: large numbers
def to_sci_item(d, m, e, small=False):
    d = Dm(d)
    assert V(m, e) == d and is_sci(m)
    if not small:
        q = "Write %s in scientific notation." % std(d)
        w = [sc(m, e + 1), sc(m, e - 1), sc(m, -e)]
        ex_ = ("Move the decimal point %s left to get %s, a number at least 1 and less than 10. "
               "So %s = %s." % (places(e), m, std(d), sci(m, e)))
    else:
        q = "Write %s in scientific notation." % std(d)
        w = [sc(m, -e), sc(m, e + 1), sc(m, e - 1)]
        ex_ = ("Move the decimal point %s right to get %s. A small number has a negative exponent: "
               "%s = %s." % (places(-e), m, std(d), sci(m, e)))
    return mcq(q, [sc(m, e)] + w, ex_)


def to_std_item(m, e):
    d = V(m, e)
    q = "Write %s in standard form." % sci(m, e)
    if e > 0:
        w = [sd(V(m, e - 1)), sd(V(m, e + 1)), sd(V(m, -e))]
        ex_ = "Move the decimal point %s right: %s = %s." % (places(e), sci(m, e), std(d))
    else:
        w = [sd(V(m, e + 1)), sd(V(m, e - 1)), sd(V(m, -e))]
        ex_ = ("Move the decimal point %s left, writing zeros as you go: %s = %s."
               % (places(-e), sci(m, e), std(d)))
    return mcq(q, [sd(d)] + w, ex_)


def which_sci_item(cands, small=False):
    ok = [c for c in cands if is_sci(c[0])]
    assert len(ok) == 1 and ok[0] == cands[0], cands
    bad = cands[1:]
    ex_ = ("In scientific notation the first factor is at least 1 and less than 10. "
           "Only %s fits. %s is not: %s is %s." % (sci(*cands[0]), sci(*bad[0]), bad[0][0],
                                                 "10 or more" if Dm(bad[0][0]) >= 10 else "less than 1"))
    return mcq("Which number is written in scientific notation?", [sc(m, e) for m, e in cands], ex_)


def fix_item(m, e):
    d = V(m, e)
    mm = Dm(m)
    k = 0
    while not (1 <= mm < 10):
        if mm >= 10:
            mm /= 10
            k += 1
        else:
            mm *= 10
            k -= 1
    m2 = format(mm.normalize(), "f")
    e2 = e + k
    assert V(m2, e2) == d
    w = [sc(m2, e), sc(m2, e - k), sc(m2, -e2)]
    if k > 0:
        why = "%s is 10 or more. %s = %s × %s, so add %d to the exponent: %s + %d = %s." % (
            m, m, m2, p10(k), k, E(e), k, E(e2))
    else:
        why = "%s is less than 1. %s = %s × %s, so subtract %d from the exponent: %s − %d = %s." % (
            m, m, m2, p10(k), -k, E(e), -k, E(e2))
    ex_ = why + " Answer: %s." % sci(m2, e2)
    q = "%s is not in scientific notation. Which number is equal to it and written in scientific notation?" % sci(m, e)
    return mcq(q, [sc(m2, e2)] + w, ex_)


def set_large():
    its = []
    for d, m, e in [("2400", "2.4", 3), ("45000", "4.5", 4), ("3200000", "3.2", 6), ("507000", "5.07", 5),
                    ("12000000", "1.2", 7), ("6050000", "6.05", 6), ("870000000", "8.7", 8),
                    ("91000000000", "9.1", 10)]:
        its.append(to_sci_item(d, m, e))
    for m, e in [("2.5", 5), ("4", 9), ("1.36", 4), ("7.08", 6), ("9.9", 7), ("6.4", 11)]:
        its.append(to_std_item(m, e))
    its.append(which_sci_item([("6.1", 5), ("32", 5), ("0.7", 6), ("15", 2)]))
    its.append(which_sci_item([("1.08", 8), ("10.5", 6), ("0.25", 9), ("45", 5)]))
    its.append(which_sci_item([("9.5", 3), ("72", 4), ("0.31", 7), ("10", 8)]))
    its.append(fix_item("32", 5))
    its.append(fix_item("0.45", 7))
    its.append(fix_item("850", 3))
    order = [0, 1, 8, 9, 2, 14, 10, 3, 11, 4, 15, 12, 5, 6, 13, 17, 16, 7, 18, 19]
    its = [its[i] for i in order]
    return {"title": "Large numbers in scientific notation", "items": its}


# ------------------------------------------------------------ set 3: small numbers
def set_small():
    its = []
    for d, m, e in [("0.06", "6", -2), ("0.305", "3.05", -1), ("0.0045", "4.5", -3), ("0.0101", "1.01", -2),
                    ("0.00072", "7.2", -4), ("0.000089", "8.9", -5), ("0.0000013", "1.3", -6),
                    ("0.0000002", "2", -7)]:
        its.append(to_sci_item(d, m, e, small=True))
    for m, e in [("3", -2), ("6.08", -1), ("7.1", -4), ("5.25", -3), ("1.4", -5), ("9.6", -6)]:
        its.append(to_std_item(m, e))
    its.append(which_sci_item([("4.5", -4), ("45", -3), ("0.8", -2), ("12", -6)]))
    its.append(which_sci_item([("2.06", -7), ("0.5", -3), ("20.6", -6), ("10", -4)]))
    its.append(which_sci_item([("7", -2), ("70", -4), ("0.9", -1), ("11", -3)]))
    its.append(fix_item("0.6", -3))
    its.append(fix_item("45", -5))
    its.append(fix_item("0.25", -6))
    order = [0, 8, 1, 9, 2, 14, 10, 3, 11, 4, 15, 12, 5, 13, 6, 16, 17, 7, 18, 19]
    its = [its[i] for i in order]
    return {"title": "Small numbers in scientific notation", "items": its}


# ------------------------------------------------------------ set 4: compare and order
def set_compare():
    its = []
    for kind, ns in [("greatest", [("3.1", 5), ("9.8", 4), ("7.5", 3), ("5.4", 4)]),
                     ("greatest", [("1.2", 7), ("9.9", 6), ("8", 5), ("2.4", 6)]),
                     ("greatest", [("2", -3), ("9", -5), ("5", -4), ("8.5", -6)]),
                     ("greatest", [("6.4", -2), ("6.4", -5), ("9.1", -3), ("1.7", -4)]),
                     ("least", [("1.5", -6), ("9.2", -4), ("3", -5), ("4.8", -2)]),
                     ("least", [("7", -3), ("2", 2), ("9.5", 0), ("3.3", -1)])]:
        vals = [V(*x) for x in ns]
        best = max(vals) if kind == "greatest" else min(vals)
        assert vals[0] == best and vals.count(best) == 1
        if kind == "greatest":
            ex_ = ("Compare the exponents first. The greatest exponent is %s, in %s. "
                   "Only if two exponents are equal do you compare the first factors."
                   % (E(ns[0][1]), sci(*ns[0])))
        else:
            ex_ = ("Compare the exponents first. The least exponent is %s, so %s = %s is the least."
                   % (E(ns[0][1]), sci(*ns[0]), std(vals[0])))
        its.append(mcq("Which number is the %s?" % kind, [sc(*x) for x in ns], ex_))
    # which statement is true
    for st in [[(("4.2", 5), ">", ("9.7", 4)), (("6", -3), ">", ("2", -2)), (("3.5", 6), "<", ("8", 5)),
                (("1", -4), ">", ("1", -3))],
               [(("5", -6), "<", ("5", -5)), (("7.2", 8), "<", ("9.1", 7)), (("4", -2), "<", ("4", -4)),
                (("2.6", 3), ">", ("1.1", 4))],
               [(("8.8", -3), ">", ("9.9", -4)), (("1.9", 10), "<", ("9.2", 9)), (("3", -7), ">", ("3", -6)),
                (("6.5", 4), ">", ("6.6", 4))],
               [(("2.05", 6), "<", ("2.5", 6)), (("7", -1), "<", ("7", -2)), (("5.1", 5), ">", ("4.9", 6)),
                (("9", -8), ">", ("1", -7))]]:
        truth = []
        for a, op, b in st:
            truth.append(V(*a) > V(*b) if op == ">" else V(*a) < V(*b))
        assert truth == [True, False, False, False], st
        ch = [("%s %s %s" % (sci(*a), "&gt;" if op == ">" else "&lt;", sci(*b)), None) for a, op, b in st]
        a, op, b = st[0]
        if a[1] == b[1]:
            ex_ = ("The exponents are equal, so compare the first factors: %s %s %s." % (a[0], "&gt;" if op == ">" else "&lt;", b[0]))
        else:
            ex_ = ("Compare the exponents: %s %s %s, so %s %s %s. Check: %s %s %s."
                   % (E(a[1]), "&gt;" if op == ">" else "&lt;", E(b[1]), sci(*a), "&gt;" if op == ">" else "&lt;",
                      sci(*b), std(V(*a)), "&gt;" if op == ">" else "&lt;", std(V(*b))))
        its.append(mcq("Which statement is true?", ch, ex_))
    # order least to greatest
    for ns in [[("2.5", 4), ("9", 3), ("1.1", 5)],
               [("4", -3), ("7", -5), ("1.2", -2)],
               [("3.6", 6), ("3.6", -6), ("8", 5)],
               [("0.0009", None), ("5.5", -4), ("1", -3)]]:
        def show(x):
            return std(Dm(x[0])) if x[1] is None else sci(*x)

        def val(x):
            return Dm(x[0]) if x[1] is None else V(*x)
        right = sorted(ns, key=val)
        by_first = sorted(ns, key=lambda x: (val(x) / (Dm(10) ** val(x).adjusted())))
        cands = [right[::-1], by_first, [right[1], right[0], right[2]], [right[0], right[2], right[1]],
                 [right[2], right[0], right[1]]]
        wrong = []
        for c in cands:
            if c != right and c not in wrong:
                wrong.append(c)
        wrong = wrong[:3]
        assert len(wrong) == 3
        fmt = lambda o: ", ".join(show(x) for x in o)
        ex_ = ("Write each number in standard form and compare: %s. So the order is %s."
               % (" &lt; ".join(std(val(x)) for x in right), fmt(right)))
        q = "Order from least to greatest: %s" % ", ".join(show(x) for x in ns)
        its.append(mcq(q, [(fmt(right), None)] + [(fmt(w), None) for w in wrong], ex_))
    # how many times as large
    for a, b, w in [(("6", 7), ("6", 4), ["3", "100", "10000"]),
                    (("8", -3), ("8", -5), ["2", "1000", "0.01"]),
                    (("9", 5), ("3", 3), ["3", "30", "3000"])]:
        r = V(*a) / V(*b)
        q = "%s is how many times as large as %s?" % (sci(*a), sci(*b))
        if a[0] == b[0]:
            ex_ = ("Divide the powers of ten: %s ÷ %s = 10<sup>%s</sup> = %s."
                   % (p10(a[1]), p10(b[1]), E(a[1] - b[1]), std(r)))
        else:
            ex_ = ("Divide the first factors and the powers of ten: %s ÷ %s = %s and %s ÷ %s = %s. "
                   "%s × %s = %s." % (a[0], b[0], std(V(a[0]) / V(b[0])), p10(a[1]), p10(b[1]),
                                      std(V(1, a[1] - b[1])), std(V(a[0]) / V(b[0])), std(V(1, a[1] - b[1])), std(r)))
        its.append(mcq(q, [sd(r)] + [sd(Dm(x)) for x in w], ex_))
    # between two powers of ten
    for lo, hi, lab, ns in [(4, 5, None, [("3.7", 4), ("3.7", 5), ("9.9", 3), ("1.2", 6)]),
                            (-3, -2, None, [("4", -3), ("4", -2), ("4", -4), ("4", 3)]),
                            (6, 9, "1 million (10<sup>6</sup>) and 1 billion (10<sup>9</sup>)",
                             [("2.5", 8), ("2.5", 9), ("2.5", 5), ("2.5", -8)])]:
        ok = [x for x in ns if V(1, lo) < V(*x) < V(1, hi)]
        assert ok == [ns[0]], ns
        q = "Which number is between %s?" % (lab or "%s and %s" % (p10(lo), p10(hi)))
        ex_ = "%s = %s, which is between %s and %s." % (sci(*ns[0]), std(V(*ns[0])), std(V(1, lo)), std(V(1, hi)))
        its.append(mcq(q, [sc(*x) for x in ns], ex_))
    order = [0, 1, 17, 2, 6, 18, 3, 7, 14, 4, 10, 15, 5, 8, 11, 19, 16, 9, 12, 13]
    its = [its[i] for i in order]
    return {"title": "Compare and order numbers in scientific notation", "items": its}


# ------------------------------------------------------------ set 5: prefixes and real contexts
def set_real():
    its = []
    for name, sym, e, w in [("mega", "M", 6, [3, 9, -6]), ("micro", "μ", -6, [-3, -9, 6]),
                            ("giga", "G", 9, [6, 12, -9]), ("nano", "n", -9, [-6, -12, 9]),
                            ("tera", "T", 12, [9, 6, -12])]:
        q = "The metric prefix <b>%s</b> (symbol %s) means multiply by which power of ten?" % (name, sym)
        ex_ = "%s means %s = %s." % (name.capitalize(), p10(e), std(V(1, e)))
        its.append(mcq(q, [pw(e)] + [pw(x) for x in w], ex_))
    its.append(mcq("The CN Tower in Toronto is 553 m tall. What is its height in scientific notation?",
                   [sc("5.53", 2), sc("5.53", 3), sc("5.53", 1), sc("5.53", -2)],
                   "Move the decimal point 2 places left: 553 = 5.53 × 10<sup>2</sup> m."))
    its.append(mcq("The distance from Earth to the Sun is about 150 000 000 km. Which is this distance in scientific notation?",
                   [sc("1.5", 8), sc("1.5", 9), sc("1.5", 7), sc("1.5", -8)],
                   "Move the decimal point 8 places left: 150 000 000 = 1.5 × 10<sup>8</sup> km. "
                   "(1.5 × 10<sup>9</sup> comes from counting all 9 digits.)"))
    its.append(mcq("The Moon is about 384 000 km from Earth. Which is this distance in scientific notation?",
                   [sc("3.84", 5), sc("3.84", 6), sc("3.84", 4), sc("3.84", -5)],
                   "Move the decimal point 5 places left: 384 000 = 3.84 × 10<sup>5</sup> km."))
    its.append(mcq("Light travels about 3 × 10<sup>5</sup> km in one second. Write this distance in standard form.",
                   [(std(V(3, 5)) + " km", V(3, 5)), ("30" + NB + "000 km", Dm(30000)),
                    ("3" + NB + "000" + NB + "000 km", Dm(3000000)), ("15 km", Dm(15))],
                   "3 × 10<sup>5</sup> = 3 × 100 000 = 300 000 km. (15 comes from 3 × 5, which is not what 10<sup>5</sup> means.)"))
    its.append(mcq("Canada has about 41 million people. Write this number in scientific notation.",
                   [sc("4.1", 7), sc("4.1", 6), sc("4.1", 8), sc("4.1", -7)],
                   "41 million = 41 000 000. Move the decimal point 7 places left: 4.1 × 10<sup>7</sup>."))
    its.append(mcq("A bacterium is about 2 micrometres (2 μm) long. How long is it in metres?",
                   [(sci(2, -6) + " m", V(2, -6)), (sci(2, -3) + " m", V(2, -3)),
                    (sci(2, -9) + " m", V(2, -9)), (sci(2, 6) + " m", V(2, 6))],
                   "Micro means 10<sup>" + E(-6) + "</sup>, so 2 μm = 2 × 10<sup>" + E(-6) + "</sup> m. "
                   "(10<sup>" + E(-3) + "</sup> is milli and 10<sup>" + E(-9) + "</sup> is nano.)"))
    its.append(mcq("A red blood cell is about 8 μm wide. Write this width in metres as a decimal.",
                   [("0.000008 m", Dm("0.000008")), ("0.008 m", Dm("0.008")),
                    ("0.0000008 m", Dm("0.0000008")), ("0.00008 m", Dm("0.00008"))],
                   "8 μm = 8 × 10<sup>" + E(-6) + "</sup> m. Move the decimal point 6 places left: 0.000008 m (5 zeros after the point)."))
    its.append(mcq("Liam’s new hard drive holds 2 terabytes (2 TB). How many bytes is that?",
                   [sc(2, 12), sc(2, 9), sc(2, 6), sc(2, -12)],
                   "Tera means 10<sup>12</sup>, so 2 TB = 2 × 10<sup>12</sup> bytes. (10<sup>9</sup> is giga and 10<sup>6</sup> is mega.)"))
    its.append(mcq("A wind turbine in Ontario is rated at 3 megawatts (3 MW). How many watts is that?",
                   [("3" + NB + "000" + NB + "000 W", Dm(3000000)), ("3000 W", Dm(3000)),
                    ("3" + NB + "000" + NB + "000" + NB + "000 W", Dm(3000000000)), ("0.000003 W", Dm("0.000003"))],
                   "Mega means 10<sup>6</sup> = 1 000 000. 3 × 1 000 000 = 3 000 000 W."))
    its.append(mcq("A flu virus is about 100 nanometres (100 nm) across. Which is this length in metres, in scientific notation?",
                   [(sci(1, -7) + " m", V(1, -7)), (sci(1, -9) + " m", V(1, -9)),
                    (sci(1, -11) + " m", V(1, -11)), (sci(1, -4) + " m", V(1, -4))],
                   "100 nm = 100 × 10<sup>" + E(-9) + "</sup> m = 10<sup>2</sup> × 10<sup>" + E(-9) +
                   "</sup> m = 1 × 10<sup>" + E(-7) + "</sup> m. Add the exponents: 2 + (" + E(-9) + ") = " + E(-7) + "."))
    its.append(mcq("Maya’s phone has 128 gigabytes (128 GB) of storage. Which is this number of bytes in scientific notation?",
                   [sc("1.28", 11), sc("1.28", 9), sc("1.28", 7), sc("1.28", 12)],
                   "128 GB = 128 × 10<sup>9</sup> bytes. 128 = 1.28 × 10<sup>2</sup>, so the total is "
                   "1.28 × 10<sup>2 + 9</sup> = 1.28 × 10<sup>11</sup> bytes."))
    its.append(mcq("A human hair is about 80 μm wide. A bacterium is about 2 μm long. How many bacteria, end to end, "
                   "would fit across the width of the hair?",
                   [sd(40), sd(160), sd(400), sd(4)],
                   "Both lengths are in micrometres, so divide: 80 ÷ 2 = 40 bacteria."))
    its.append(mcq("A bacterium is about 2 × 10<sup>" + E(-6) + "</sup> m long. A virus is about 1 × 10<sup>" + E(-7) +
                   "</sup> m across. The bacterium is how many times as long as the virus?",
                   [sd(20), sd("0.05"), sd(2), sd(200)],
                   "2 ÷ 1 = 2 and 10<sup>" + E(-6) + "</sup> ÷ 10<sup>" + E(-7) + "</sup> = 10<sup>1</sup> = 10. "
                   "2 × 10 = 20 times as long."))
    its.append(mcq("A nanosecond is 10<sup>" + E(-9) + "</sup> s and a picosecond is 10<sup>" + E(-12) +
                   "</sup> s. How many picoseconds are in one nanosecond?",
                   [sd(1000), sd(3), sd("0.001"), sd(1000000)],
                   "10<sup>" + E(-9) + "</sup> ÷ 10<sup>" + E(-12) + "</sup> = 10<sup>" + E(-9) + " − (" + E(-12) +
                   ")</sup> = 10<sup>3</sup> = 1000 picoseconds."))
    its.append(mcq("Canada has about 4 × 10<sup>7</sup> people and the world has about 8 × 10<sup>9</sup> people. "
                   "The world population is about how many times as large as Canada’s?",
                   [sd(200), sd(2), sd(20), sd(2000)],
                   "8 ÷ 4 = 2 and 10<sup>9</sup> ÷ 10<sup>7</sup> = 10<sup>2</sup> = 100. 2 × 100 = 200 times as large."))
    assert V(8, 9) / V(4, 7) == 200 and V(2, -6) / V(1, -7) == 20 and V(1, -9) / V(1, -12) == 1000
    assert Dm(128) * V(1, 9) == V("1.28", 11) and Dm(100) * V(1, -9) == V(1, -7)
    assert len(its) == 20
    return {"title": "Metric prefixes and real-world numbers", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % x for x in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    names = {12: "tera", 9: "giga", 6: "mega", 3: "kilo", 0: "", -3: "milli", -6: "micro", -9: "nano", -12: "pico"}
    names = {k: v for k, v in names.items() if v}
    return (
        "<h2>Powers of ten</h2>"
        "<p>A positive exponent tells how many 10s you multiply: 10<sup>4</sup> = 10 × 10 × 10 × 10 = 10 000. "
        "A <b>negative exponent</b> means you divide by that many 10s. It gives a small positive number, "
        "not a negative number: 10<sup>" + E(-3) + "</sup> = 1 ÷ 1000 = 0.001.</p>"
        + table(["Power", "Standard form", "Power", "Standard form"], [
            [p10(3), "1000", p10(-1), "0.1"],
            [p10(2), "100", p10(-2), "0.01"],
            [p10(1), "10", p10(-3), "0.001"],
            [p10(0), "1", p10(-6), "0.000001"],
        ])
        + "<h2>What scientific notation is</h2>"
        "<p>A number in scientific notation is written as <b>a × 10<sup>n</sup></b>. The first factor <b>a</b> is "
        "at least 1 and less than 10. The exponent <b>n</b> is an integer. It is a short way to write very large "
        "and very small numbers, such as distances in space or the size of a cell.</p>"
        "<h2>Large numbers</h2>"
        "<p>Move the decimal point to the left until one non-zero digit is in front of it. "
        "The number of places you moved is the exponent.</p>"
        "<figure class='sn-fig'>" + hop_big_lesson() +
        "<figcaption>3 200 000: the decimal point moves 6 places left to make 3.2, so 3 200 000 = 3.2 × 10<sup>6</sup>.</figcaption></figure>"
        + ex("Large number", "The distance from Earth to the Sun is about 150 000 000 km. Write it in scientific notation.",
             "Move the decimal point 8 places left: 1.5. The number is large, so the exponent is positive.",
             "1.5 × 10<sup>8</sup> km")
        + "<h2>Small numbers</h2>"
        "<p>For a number less than 1, move the decimal point to the <b>right</b> until one non-zero digit is in front "
        "of it. The exponent is <b>negative</b>.</p>"
        "<figure class='sn-fig'>" + hop_small_lesson() +
        "<figcaption>0.0045: the decimal point moves 3 places right to make 4.5, so 0.0045 = 4.5 × 10<sup>" + E(-3) +
        "</sup>.</figcaption></figure>"
        + ex("Back to standard form", "Write 7.1 × 10<sup>" + E(-4) + "</sup> in standard form.",
             "Move the decimal point 4 places left, writing zeros: 7.1 → 0.00071.", "0.00071")
        + "<h2>Compare and order</h2>"
        "<p>Compare the <b>exponents</b> first: the greater exponent gives the greater number. "
        "Only when the exponents are equal do you compare the first factors.</p>"
        + ex("Compare", "Which is greater: 3.1 × 10<sup>5</sup> or 9.8 × 10<sup>4</sup>?",
             "The exponents are 5 and 4, and 5 &gt; 4. Check: 310 000 &gt; 98 000.",
             "3.1 × 10<sup>5</sup>")
        + "<p>With negative exponents, the exponent closer to zero gives the greater number: "
          "2 × 10<sup>" + E(-3) + "</sup> = 0.002 is greater than 9 × 10<sup>" + E(-5) + "</sup> = 0.00009.</p>"
        "<h2>Metric prefixes</h2>"
        "<p>Each metric prefix stands for a power of ten. One step on this scale is 1000 times as large.</p>"
        "<figure class='sn-fig'>" + ladder_svg(-12, 12, None, names=names, step=3, gap=58) +
        "<figcaption>From pico (10<sup>" + E(-12) + "</sup>) to tera (10<sup>12</sup>). A bacterium is about 2 μm "
        "= 2 × 10<sup>" + E(-6) + "</sup> m long.</figcaption></figure>"
        + table(["Prefix", "Symbol", "Power of ten", "Example"], [
            ["tera", "T", p10(12), "a 2 TB hard drive"],
            ["giga", "G", p10(9), "128 GB of phone storage"],
            ["mega", "M", p10(6), "a 3 MW wind turbine"],
            ["micro", "μ", p10(-6), "a 2 μm bacterium"],
            ["nano", "n", p10(-9), "a 100 nm virus"],
            ["pico", "p", p10(-12), "1 ps = 10<sup>" + E(-12) + "</sup> s"],
        ])
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["32 × 10<sup>5</sup> as scientific notation", "The first factor must be from 1 to less than 10: 3.2 × 10<sup>6</sup>"],
            ["0.0045 = 4.5 × 10<sup>3</sup>", "A number less than 1 has a negative exponent: 4.5 × 10<sup>" + E(-3) + "</sup>"],
            ["3 200 000 = 3.2 × 10<sup>7</sup> (counting all 7 digits)", "Count the places the point moves: 6"],
            ["10<sup>4</sup> = 40", "10<sup>4</sup> = 10 × 10 × 10 × 10 = 10 000"],
            ["10<sup>" + E(-2) + "</sup> = " + MINUS + "100", "10<sup>" + E(-2) + "</sup> = 1 ÷ 100 = 0.01"],
            ["9.8 × 10<sup>4</sup> &gt; 3.1 × 10<sup>5</sup> because 9.8 &gt; 3.1", "Compare the exponents first"],
        ])
    )


FAQ = [
    {"q": "When do Ontario students learn scientific notation?",
     "a": "In Grade 8. The Ontario math curriculum (Number, B1.1) has students represent and compare very large and "
          "very small numbers, including with scientific notation, and describe how they are used in everyday life."},
    {"q": "How do you write a small number like 0.0045 in scientific notation?",
     "a": "Move the decimal point right until one non-zero digit is in front of it: 4.5. You moved 3 places, "
          "and the number is less than 1, so the exponent is negative: 4.5 × 10⁻³."},
    {"q": "Why is 32 × 10⁵ not in scientific notation?",
     "a": "The first factor must be at least 1 and less than 10. 32 is too big, so write 32 as 3.2 × 10 "
          "and add 1 to the exponent: 3.2 × 10⁶."},
    {"q": "What do the prefixes mega, giga, micro and nano mean?",
     "a": "Mega means 10⁶ (a million), giga 10⁹ (a billion), micro 10⁻⁶ (a millionth) and nano 10⁻⁹ (a billionth). "
          "Tera is 10¹² and pico is 10⁻¹²."},
]


SVG = re.compile(r"(<svg.*?</svg>)", re.S)
GAP = re.compile(r"(?<=\d) (?=\d{3}(?!\d))")


def nbsp(s):
    """Use a no-break space between digit groups (150 000 000) everywhere outside SVG markup."""
    return "".join(p if p.startswith("<svg") else GAP.sub(NB, p) for p in SVG.split(s))


def fix_spaces(u):
    for k in ("title", "seo_title", "short_title", "meta_desc", "key_big", "key_sub", "body_html"):
        u[k] = nbsp(u[k])
    for f in u["faq"]:
        f["q"], f["a"] = nbsp(f["q"]), nbsp(f["a"])
    for s in u["sets"]:
        s["title"] = nbsp(s["title"])
        for it in s["items"]:
            it["q"], it["e"] = nbsp(it["q"]), nbsp(it["e"])
            it["c"] = [nbsp(c) for c in it["c"]]
    return u


def mark_large(u, pattern):
    """Tag wide pictures (powers-of-ten scales) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(48801)
    sets = [set_powers(), set_large(), set_small(), set_compare(), set_real()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-8", "slug": "scientific-notation", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Scientific Notation: Very Large and Very Small Numbers",
        "seo_title": "Grade 8 Scientific Notation Worksheets: Powers of Ten and Metric Prefixes, Free Math with Answer Key (Ontario Curriculum)",
        "short_title": "Scientific notation",
        "domain": "Number",
        "standard_code": "Grade 8: B1.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Represent and compare very large and very small numbers, including through the use of scientific notation, and describe various ways they are used in everyday life",
        "meta_desc": "Free Grade 8 math worksheets on scientific notation for the Ontario curriculum: powers of ten with positive and negative exponents, writing large and small numbers as a × 10ⁿ, comparing and ordering, and metric prefixes from pico to tera with space, cell and computer examples. 100 questions with an answer key.",
        "key_big": "Scientific notation is a × 10ⁿ, where a is at least 1 and less than 10: 3 200 000 = 3.2 × 10⁶ and 0.0045 = 4.5 × 10⁻³.",
        "key_sub": "The exponent is the number of places the decimal point moves, not the number of digits. Large numbers get a positive exponent and small numbers a negative one. 32 × 10⁵ is not scientific notation.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(fix_spaces(u), "powers of ten scale")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
