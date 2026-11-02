# -*- coding: utf-8 -*-
"""
British Columbia Grade 5 Math: Benchmarks and estimation
(BC Mathematics Curriculum, Grade 5: Number - "Whole-number, fraction, and decimal benchmarks")
  python3 tools/gen_cabc_math_g5_benchmarks.py
Whole numbers to 1 000 000 (no-break spaces from 5 digits) and decimals to thousandths.
Round whole numbers to benchmarks, use the fraction benchmarks 0, 1/2 and 1 and the decimal
benchmarks 0, 0.5 and 1, estimate sums and products, and decide if an answer is reasonable.
Round half up (45 000 -> 50 000). Every number choice carries its exact value (Fraction), and a wrong
choice never equals the right value or another wrong one. Wrong answers come from real mistakes:
3/8 is closer to 1, 0.09 is close to 1 (9 is a big digit), rounding the wrong place, rounding in steps,
rounding the wrong way, extra or missing zeros in products, adding tops and bottoms of fractions.
Canadian English. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from decimal import Decimal
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-5")
SLUG = "benchmarks-and-estimation"
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
BLUE = "#2f6db5"
INK = "#2b2b2b"
GREY = "#6b6259"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
CANT = "You can’t tell"


# ------------------------------------------------------------ numbers
def nf(n):
    """4536 -> '4536', 10000 -> '10 000' (no-break space from 5 digits)."""
    assert n >= 0 and n == int(n), n
    s = str(int(n))
    if len(s) < 5:
        return s
    out = []
    while s:
        out.insert(0, s[-3:])
        s = s[:-3]
    return NB.join(out)


def dd(x):
    """Fraction or str -> decimal text: '0.48', '6.5', '12'."""
    x = F(x)
    d = Decimal(x.numerator) / Decimal(x.denominator)
    assert F(str(d)) == x, x
    s = format(d.normalize(), "f")
    if "." in s:
        w, f = s.split(".")
        return nf(int(w)) + "." + f
    return nf(int(s))


def money(x):
    x = F(x)
    assert (x * 100).denominator == 1
    c = int(x * 100)
    return "$" + nf(c // 100) + ("" if c % 100 == 0 else ".%02d" % (c % 100))


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def fx(x):
    """Fraction -> html: 3, 3/8, 1 1/2."""
    x = F(x)
    assert x >= 0
    if x.denominator == 1:
        return nf(x.numerator)
    w = x.numerator // x.denominator
    r = x - w
    return (nf(w) if w else "") + fr(r.numerator, r.denominator)


def N(n):
    return (nf(n), F(n))


def D(s):
    return (dd(s), F(s))


def rnd_to(n, p):
    """round half up to the nearest p (works for Fractions too)"""
    return math.floor(F(n) / p + F(1, 2)) * p


def front(n):
    """round to the greatest place (front-end rounding): 48 -> 50, 396 -> 400, 7 -> 7"""
    if n < 10:
        return n
    p = 10 ** (len(str(n)) - 1)
    return rnd_to(n, p)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """correct and cands are html strings or (html, value) pairs. Right answer first; balance() places it."""
    if not isinstance(correct, tuple):
        correct = (correct, None)
    cs, cv = correct
    seen, vals, pick = {cs}, set(), []
    if cv is not None:
        vals.add(cv)
    for c in cands:
        if c is None:
            continue
        if not isinstance(c, tuple):
            c = (c, None)
        s, v = c
        if not s or s in seen:
            continue
        if v is not None and (v < 0 or v in vals):
            continue
        seen.add(s)
        if v is not None:
            vals.add(v)
        pick.append(s)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, cs, cands)
    return {"q": q, "c": [cs] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Each answer position (A to D) is correct 5 times in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def txt(x, y, s, size=16, color=INK, wt=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='middle'>%s</text>"
            % (x, y, size, wt, color, s))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def sfr(x, cy, a, b, size=15, color=INK):
    """Stacked fraction in SVG, centred at x, fraction bar at cy."""
    w = max(len(str(a)), len(str(b))) * size * 0.62 + 6
    return (txt(x, cy - 4, a, size, color) +
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.8'/>"
            % (x - w / 2, cy, x + w / 2, cy, color) + txt(x, cy + size + 1, b, size, color))


def line_svg(lo, hi, minor, labels, dot, fmt, W=460):
    """Number line lo..hi, a tick every `minor`, labelled ticks at `labels`, red dot (with its value) at `dot`."""
    lo, hi, minor, dot = F(lo), F(hi), F(minor), F(dot)
    labels = [F(v) for v in labels]
    L, R, Y, H = 52, W - 52, 52, 96

    def X(v):
        return L + float((v - lo) / (hi - lo)) * (R - L)

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 12, Y, R + 12, Y, INK)]
    v = lo
    while v <= hi:
        big = v in labels
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%d'/>"
                 % (X(v), Y - (11 if big else 6), X(v), Y + (11 if big else 6), INK, 2 if big else 1))
        if big:
            s.append(txt(X(v), Y + 32, fmt(v), 15, GREEN))
        v += minor
    s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X(dot), Y, RED))
    tx = min(max(X(dot), 44), W - 44)
    s.append(txt(tx, Y - 18, fmt(dot), 16, RED, 800))
    return svg_wrap(W, H, "".join(s), "number line from %s to %s" % (fmt(lo), fmt(hi)))


def round_line(n, p):
    lo = n // p * p
    return line_svg(lo, lo + p, p // 10, [lo, lo + p // 2, lo + p], n, nf)


def big_line(n):
    return line_svg(0, 1000000, 50000, [0, 250000, 500000, 750000, 1000000], n, nf, W=480)


def dec_line(x):
    return line_svg(0, 1, F(1, 10), [0, F(1, 2), 1], x, dd)


def frac_line(a, b, W=400):
    """Number line 0..1 in b equal parts, labels 0, 1/2, 1 and a dot at a/b."""
    x0, x1, Y = 30, W - 30, 26
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x0, Y, x1, Y, INK)]
    for i in range(b + 1):
        X = x0 + (x1 - x0) * i / b
        end = i in (0, b)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X, Y - (11 if end else 8), X, Y + (11 if end else 8), INK, "2.5" if end else "1.8"))
        if end:
            s.append(txt(X, Y + 30, str(i // b), 15, GREEN))
    Xh = (x0 + x1) / 2
    if b % 2:
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2' stroke-dasharray='4 3'/>"
                 % (Xh, Y - 11, Xh, Y + 11, GREEN))
    s.append(sfr(Xh, Y + 30, 1, 2, 15, GREEN))
    s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (x0 + (x1 - x0) * a / b, Y, RED))
    return svg_wrap(W, Y + 56, "".join(s), "number line from 0 to 1 in %d equal parts with a dot at %d/%d" % (b, a, b))


# ============================================================ set 1: round whole numbers to benchmarks
WORD = {10: "ten", 100: "hundred", 1000: "thousand", 10000: "ten thousand", 100000: "hundred thousand"}
LOOK = {10: "ones", 100: "tens", 1000: "hundreds", 10000: "thousands", 100000: "ten thousands"}


def digit(n, i):
    return (n // 10 ** i) % 10


def lg(p):
    return len(str(p)) - 1


def steps(n, p):
    v, q = n, 10
    chain = [n]
    while q <= p:
        v = rnd_to(v, q)
        if v != chain[-1]:
            chain.append(v)
        q *= 10
    return chain


def round_expl(n, p):
    lo = n // p * p
    r = rnd_to(n, p)
    d = digit(n, lg(p) - 1)
    if n - lo == p // 2:
        s = ("%s is exactly halfway between %s and %s. The %s digit is 5, and 5 rounds up."
             % (nf(n), nf(lo), nf(lo + p), LOOK[p]))
    else:
        s = ("%s is between %s and %s. Look at the %s digit: %d. %s, so round %s."
             % (nf(n), nf(lo), nf(lo + p), LOOK[p], d,
                "%d is 5 or more" % d if d >= 5 else "%d is 4 or less" % d, "up" if r > lo else "down"))
    ch = steps(n, p)
    if p >= 1000 and ch[-1] != r:
        s += " Do not round in steps (%s). Look only at the %s digit." % (" → ".join(nf(x) for x in ch), LOOK[p])
    return s + " Answer: <b>%s</b>." % nf(r)


def round_cands(n, p):
    """Wrong answers from real mistakes, most likely first."""
    r = rnd_to(n, p)
    lo = n // p * p
    out = [steps(n, p)[-1],                      # rounded in steps
           rnd_to(rnd_to(n, p // 10), p),        # rounded in two steps
           lo + p if r == lo else lo,            # rounded the wrong way
           rnd_to(n, p // 10)]                   # rounded the wrong place
    if r > lo:
        out.append(r + n % p)                    # kept the digits after the place
    out += [n // (p // 10) * (p // 10), r + p, r - p, n]
    return [N(x) for x in out if x != r and 0 < x <= 1000000]


def q_round(n, p, line=True):
    q = "Round %s to the nearest %s." % (nf(n), WORD[p])
    if line:
        q = fig(round_line(n, p)) + q
    return mcq(q, N(rnd_to(n, p)), round_cands(n, p), round_expl(n, p))


def set_whole():
    its = []
    for n, p, line in [(23486, 1000, True), (58702, 1000, True), (129650, 1000, False),
                       (46820, 10000, True), (73150, 10000, True), (85000, 10000, True),
                       (196400, 10000, False), (284615, 10000, False),
                       (651200, 100000, True), (348500, 100000, True), (450000, 100000, False),
                       (962400, 100000, True), (37951, 100, False), (507380, 100000, False)]:
        its.append(q_round(n, p, line))

    # benchmarks on a line from 0 to 1 000 000
    for n, right, wrong in [(742000, 750000, [700000, 500000, 1000000]), (281000, 250000, [300000, 500000, 0])]:
        bm = [0, 250000, 500000, 750000, 1000000]
        assert all(abs(n - right) < abs(n - b) for b in bm if b != right)
        others = sorted((b for b in bm if b != right), key=lambda b: abs(n - b))[:2]
        q = (fig(big_line(n)) + "The dot shows %s. Which benchmark is it closest to: %s?"
             % (nf(n), ", ".join(nf(b) for b in bm[:-1]) + " or " + nf(bm[-1])))
        e = ("%s is only %s from %s. It is %s from %s and %s from %s. Closest benchmark: <b>%s</b>."
             % (nf(n), nf(abs(n - right)), nf(right), nf(abs(n - others[0])), nf(others[0]),
                nf(abs(n - others[1])), nf(others[1]), nf(right)))
        its.append(mcq(q, N(right), [N(x) for x in wrong], e))

    assert rnd_to(55300, 10000) == 60000 and all(rnd_to(x, 10000) != 60000 for x in (54990, 65000, 66100))
    its.append(mcq("Which number rounds to %s when you round to the nearest ten thousand?" % nf(60000),
                   N(55300), [N(54990), N(65000), N(66100)],
                   "Round each one: 55 300 → 60 000; 54 990 → 50 000 (the thousands digit is 4); "
                   "65 000 → 70 000 (exactly halfway rounds up); 66 100 → 70 000. Only <b>55 300</b> rounds to 60 000."
                   .replace(" 000", NB + "000").replace(" 990", NB + "990").replace(" 300", NB + "300")
                   .replace(" 100", NB + "100")))

    for x in range(350000, 450000, 997):
        assert rnd_to(x, 100000) == 400000
    assert rnd_to(349999, 100000) == 300000 and rnd_to(350000, 100000) == 400000
    its.append(mcq("What is the smallest whole number that rounds to %s when you round to the nearest "
                   "hundred thousand?" % nf(400000),
                   N(350000), [N(349999), N(300000), N(351000)],
                   "The numbers from %s to %s round to %s. %s has a 4 in the ten thousands place, so it rounds "
                   "down to %s. The smallest is <b>%s</b>." % (nf(350000), nf(449999), nf(400000), nf(349999),
                                                              nf(300000), nf(350000))))

    its.append(mcq("Which digit do you look at to round %s to the nearest ten thousand?" % nf(463815),
                   "the thousands digit, 3",
                   ["the ten thousands digit, 6", "the hundreds digit, 8", "the hundred thousands digit, 4"],
                   "To round to the nearest ten thousand, look one place to the right of the ten thousands: the "
                   "<b>thousands digit, 3</b>. 3 is 4 or less, so %s rounds down to %s."
                   % (nf(463815), nf(460000))))

    assert rnd_to(63820, 10000) == 60000 and rnd_to(63820, 1000) == 64000
    its.append(mcq("Owen rounds %s to the nearest ten thousand and gets %s. What should he get?"
                   % (nf(63820), nf(64000)),
                   N(60000), [N(64000), N(70000), N(63800)],
                   "Owen rounded to the nearest thousand. For the nearest ten thousand, look at the thousands digit: 3. "
                   "3 is 4 or less, so round down. %s rounds to <b>%s</b>." % (nf(63820), nf(60000))))
    assert len(its) == 20, len(its)
    return {"title": "Round whole numbers to benchmarks", "items": its}


# ============================================================ set 2: fraction benchmarks 0, 1/2, 1
H = F(1, 2)
FLAB = {"0": "Closest to 0", "h": "Closest to " + fr(1, 2), "1": "Closest to 1", "eq": "Exactly " + fr(1, 2)}


def nearest(x, marks):
    ds = sorted((abs(x - v), k) for k, v in marks)
    assert ds[0][0] != ds[1][0], x
    return ds[0][1]


FMARKS = (("0", F(0)), ("h", H), ("1", F(1)))


def frac_dist(a, b):
    x = F(a, b)
    return ("%s is %s from 0, %s from %s and %s from 1."
            % (fr(a, b), fx(x), fx(abs(x - H)), fr(1, 2), fx(1 - x)))


def set_fractions():
    its = []
    for i, (a, b) in enumerate([(1, 8), (7, 8), (5, 8), (1, 10), (9, 10), (4, 10), (5, 6), (1, 6), (7, 12)]):
        k = nearest(F(a, b), FMARKS)
        q = ((fig(frac_line(a, b)) + "The dot shows %s. " % fr(a, b)) if i < 3 else "") + \
            "Which benchmark is %s closest to: 0, %s or 1?" % (fr(a, b), fr(1, 2))
        e = frac_dist(a, b) + " It is <b>%s</b>." % FLAB[k].lower()
        if k == "h" and b % 2 == 0:
            e += " Tip: half of %d is %d, and %d is close to %d." % (b, b // 2, a, b // 2)
        its.append(mcq(q, FLAB[k], [FLAB[x] for x in ("0", "h", "1", "eq") if x != k], e))

    assert nearest(F(3, 8), FMARKS) == "h"
    its.append(mcq("Ava says %s is closest to 1 because 8 is a big number. Is she right?" % fr(3, 8),
                   "No, it is closest to " + fr(1, 2),
                   ["Yes, it is closest to 1", "No, it is closest to 0", "No, it is exactly " + fr(1, 2)],
                   "Ava is not right. A big bottom number means small parts. %s Half of 8 is 4, and 3 is close to 4, "
                   "so %s is <b>closest to %s</b>." % (frac_dist(3, 8), fr(3, 8), fr(1, 2))))

    def pick(q, right, wrong, target, tname):
        fs = [right] + wrong
        dist = [abs(F(*f) - target) for f in fs]
        assert dist[0] < min(dist[1:]), fs
        e = "Find how far each one is from %s: %s. <b>%s</b> is the closest." % (
            tname, "; ".join("%s is %s away" % (fr(*f), fx(dv)) for f, dv in zip(fs, dist)), fr(*right))
        return mcq(q, (fr(*right), F(*right)), [(fr(*f), F(*f)) for f in wrong], e)

    its.append(pick("Which fraction is closest to 1?", (11, 12), [(3, 4), (5, 12), (1, 12)], F(1), "1"))
    its.append(pick("Which fraction is closest to 0?", (2, 9), [(1, 3), (5, 9), (8, 9)], F(0), "0"))

    for a, b, c, d in [(3, 7, 5, 9), (7, 8, 4, 9)]:
        x, y = F(a, b), F(c, d)
        assert (x < H < y) or (y < H < x)
        s = "&lt;" if x < y else "&gt;"
        o = "&gt;" if x < y else "&lt;"

        def hr(n, m):
            return "Double the top: 2 × %d = %d, which is %s %d, so %s is %s %s." % (
                n, 2 * n, "less than" if 2 * n < m else "more than", m, fr(n, m),
                "less than" if 2 * n < m else "more than", fr(1, 2))
        e = "Use %s as a benchmark. %s %s So <b>%s %s %s</b>." % (fr(1, 2), hr(a, b), hr(c, d), fr(a, b), s, fr(c, d))
        its.append(mcq("Compare %s and %s. Which statement is true?" % (fr(a, b), fr(c, d)),
                       "%s %s %s" % (fr(a, b), s, fr(c, d)),
                       ["%s %s %s" % (fr(a, b), o, fr(c, d)), "%s = %s" % (fr(a, b), fr(c, d)), CANT], e))

    ABOUT = lambda x: ("about " + fx(x), x)
    for (a, b), (c, d) in [((4, 9), (1, 10)), ((7, 8), (1, 10)), ((5, 6), (4, 9)), ((9, 10), (11, 12))]:
        ka, kc = [dict(FMARKS)[nearest(F(n, m), FMARKS)] for n, m in ((a, b), (c, d))]
        est = ka + kc
        exact = F(a, b) + F(c, d)
        assert abs(exact - est) < F(1, 4), (a, b, c, d)
        wrong = [est + H, est - H, est + 1, est + F(3, 2)]
        e = ("%s is close to %s and %s is close to %s. %s + %s = <b>%s</b>. Do not add the tops and the bottoms: "
             "the answer is not %s." % (fr(a, b), fx(ka), fr(c, d), fx(kc), fx(ka), fx(kc), fx(est),
                                       fr(a + c, b + d)))
        its.append(mcq("Use the benchmarks 0, %s and 1 to estimate %s + %s." % (fr(1, 2), fr(a, b), fr(c, d)),
                       ABOUT(est), [ABOUT(w) for w in wrong if w >= 0], e))

    WH = ["Less than 1", "Exactly 1", "Between 1 and 2", "More than 2"]
    for (a, b), (c, d) in [((3, 8), (2, 5)), ((5, 6), (4, 7))]:
        x, y = F(a, b), F(c, d)
        t = x + y
        k = 0 if t < 1 else 1 if t == 1 else 2 if t < 2 else 3
        both = "less" if x < H and y < H else "more"
        assert (x < H and y < H) or (x > H and y > H and x < 1 and y < 1)
        e = ("Both fractions are %s than %s, so the sum is %s than %s + %s = 1.%s So the answer is <b>%s</b>."
             % (both, fr(1, 2), both, fr(1, 2), fr(1, 2),
                "" if both == "less" else " Each one is less than 1, so the sum is less than 2.", WH[k].lower()))
        its.append(mcq("Is %s + %s less than 1, exactly 1, between 1 and 2, or more than 2?" % (fr(a, b), fr(c, d)),
                       WH[k], [w for w in WH if w != WH[k]], e))
    assert len(its) == 20, len(its)
    return {"title": "Fraction benchmarks 0, 1/2 and 1", "items": its}


# ============================================================ set 3: decimal benchmarks 0, 0.5, 1
DLAB = {"0": "Closest to 0", "h": "Closest to 0.5", "1": "Closest to 1", "eq": "Exactly 0.5"}


def dec_dist(x):
    x = F(x)
    return "%s is %s from 0, %s from 0.5 and %s from 1." % (dd(x), dd(x), dd(abs(x - H)), dd(1 - x))


def set_decimals():
    its = []
    for i, s in enumerate(["0.2", "0.9", "0.48", "0.82", "0.125", "0.61", "0.875", "0.37", "0.705", "0.16",
                           "0.064"]):
        x = F(s)
        k = nearest(x, FMARKS)
        q = ((fig(dec_line(x)) + "The dot shows %s. " % dd(x)) if i < 4 else "") + \
            "Which benchmark is %s closest to: 0, 0.5 or 1?" % dd(x)
        e = dec_dist(x) + " It is <b>%s</b>." % DLAB[k].lower()
        if len(s) > 3:
            e += " Tip: think of 0.5 as %s." % ("0.50" if len(s) == 4 else "0.500")
        its.append(mcq(q, DLAB[k], [DLAB[z] for z in ("0", "h", "1", "eq") if z != k], e))

    assert nearest(F("0.09"), FMARKS) == "0"
    its.append(mcq("Leah says 0.09 is closest to 1 because 9 is a big digit. Is she right?",
                   "No, it is closest to 0",
                   ["Yes, it is closest to 1", "No, it is closest to 0.5", "Yes, 9 is more than 5"],
                   "Leah is not right. The 9 is in the hundredths place, so 0.09 is only 9 hundredths. "
                   + dec_dist("0.09") + " It is <b>closest to 0</b>."))

    # round to the nearest whole number with the benchmark 0.5
    for s, wrong in [("3.48", ["4", "3.5", "2"]), ("6.52", ["6", "6.5", "8"]), ("12.095", ["13", "12.1", "11"])]:
        x = F(s)
        w = x.numerator // x.denominator
        part = x - w
        r = rnd_to(x, 1)
        e = ("%s is between %d and %d. The decimal part is %s, which is %s 0.5, so round %s. Answer: <b>%d</b>."
             % (dd(x), w, w + 1, dd(part), "less than" if part < H else "more than", "down" if r == w else "up", r))
        if s == "3.48":
            e += " Do not look at the last digit (8). Compare 0.48 with 0.50."
        if s == "12.095":
            e += " Compare 0.095 with 0.500: it is less, even though 9 is a big digit."
        its.append(mcq("Round %s to the nearest whole number." % dd(x), D(r), [D(z) for z in wrong], e))

    # round to the nearest half
    for s, wrong in [("4.38", ["4", "4.4", "5"]), ("7.84", ["7.5", "7.8", "7"])]:
        x = F(s)
        r = rnd_to(x, H)
        lo = math.floor(x / H) * H
        e = ("%s is between %s and %s. It is %s from %s and %s from %s, so it is closest to <b>%s</b>."
             % (dd(x), dd(lo), dd(lo + H), dd(x - lo), dd(lo), dd(lo + H - x), dd(lo + H), dd(r)))
        its.append(mcq("Round %s to the nearest half (a whole number or a number ending in .5)." % dd(x),
                       D(r), [D(z) for z in wrong], e))

    fs = ["0.47", "0.57", "0.405", "0.05"]
    dist = [abs(F(z) - H) for z in fs]
    assert dist[0] < min(dist[1:])
    its.append(mcq("Which decimal is closest to 0.5?", D(fs[0]), [D(z) for z in fs[1:]],
                   "Write them all with three decimal places and compare with 0.500: "
                   + "; ".join("%s is %s away" % (dd(z), dd(dv)) for z, dv in zip(fs, dist))
                   + ". <b>0.47</b> is the closest. 0.05 is 5 hundredths, not 5 tenths."))

    # estimate sums with decimal benchmarks
    for terms, wrong in [(["2.48", "3.9"], ["6", "5", "7"]), (["0.92", "0.49", "0.06"], ["2", "1", "0.5"])]:
        xs = [F(t) for t in terms]
        rs = [rnd_to(x, H) for x in xs]
        est = sum(rs)
        exact = sum(xs)
        assert abs(est - exact) < F(1, 4)
        e = ("Round each decimal to the nearest half: %s = <b>%s</b>. (The exact answer is %s.)"
             % (" + ".join(dd(r) for r in rs), dd(est), dd(exact)))
        its.append(mcq("Estimate %s. Round each decimal to the nearest half (a whole number or a number ending in .5)."
                       % " + ".join(dd(x) for x in xs), ("about " + dd(est), est),
                       [("about " + w, F(w)) for w in wrong], e))
    assert len(its) == 20, len(its)
    return {"title": "Decimal benchmarks 0, 0.5 and 1", "items": its}


# ============================================================ set 4: estimate sums and products
def sum_item(terms, p):
    rs = [rnd_to(n, p) for n in terms]
    est, exact = sum(rs), sum(terms)
    assert est != exact
    down = sum(n // p * p for n in terms)
    cands = [sum(steps(n, p)[-1] for n in terms), down, sum(rnd_to(n, p // 10) for n in terms), exact,
             est + p, est - p]
    e = ("Round each number to the nearest %s: %s = <b>%s</b>. (The exact answer is %s.)"
         % (WORD[p], " + ".join(nf(r) for r in rs), nf(est), nf(exact)))
    q = "Estimate %s by rounding each number to the nearest %s." % (" + ".join(nf(n) for n in terms), WORD[p])
    return mcq(q, N(est), [N(x) for x in cands if 0 < x <= 2000000], e)


def zeros_note(a, b):
    ra, rb = front(a), front(b)
    da, db = str(ra).rstrip("0") or "0", str(rb).rstrip("0") or "0"
    za, zb = len(str(ra)) - len(da), len(str(rb)) - len(db)
    if za + zb == 0:
        return ""
    return " (%s × %s = %s, then write %d zero%s.)" % (da, db, nf(int(da) * int(db)), za + zb, "" if za + zb == 1 else "s")


def prod_item(a, b):
    ra, rb = front(a), front(b)
    est, exact = ra * rb, a * b
    assert est != exact
    cands = [est // 10, est * 10,                                      # lost or added a zero
             (a // 10 ** (len(str(a)) - 1) * 10 ** (len(str(a)) - 1)) * (b // 10 ** (len(str(b)) - 1) * 10 ** (len(str(b)) - 1)) if b >= 10 else (a // 10 ** (len(str(a)) - 1) * 10 ** (len(str(a)) - 1)) * b,  # rounded down
             ra * b if b >= 10 else None,                              # rounded only one factor
             exact, ra + rb]                                           # exact / added
    e = ("Round %s: %s × %s = <b>%s</b>.%s (The exact answer is %s.)"
         % ("both numbers to their greatest place" if b >= 10 else "%s to its greatest place" % nf(a),
            nf(ra), nf(rb), nf(est), zeros_note(a, b), nf(exact)))
    q = "Estimate %s × %s by rounding %s." % (nf(a), nf(b), "each number to its greatest place" if b >= 10
                                               else "%s to its greatest place" % nf(a))
    return mcq(q, N(est), [N(x) for x in cands if x is not None and 0 < x <= 2000000], e)


def set_estimate():
    its = []
    for terms, p in [([24680, 13240], 1000), ([36450, 21830], 1000), ([18450, 32900, 9720], 1000),
                     ([48315, 29780], 10000), ([71400, 15600], 10000), ([245800, 312400], 10000),
                     ([126400, 381950], 100000), ([452300, 218700], 100000)]:
        its.append(sum_item(terms, p))
    for a, b in [(48, 7), (83, 6), (396, 6), (612, 8), (2875, 4), (48, 31), (67, 22), (89, 53), (315, 19),
                 (724, 48)]:
        its.append(prod_item(a, b))
    # more or less than the estimate
    ML = lambda v: ["More than %s" % nf(v), "Less than %s" % nf(v), "Exactly %s" % nf(v), CANT]
    a, b = 18600, 24700
    est = rnd_to(a, 1000) + rnd_to(b, 1000)
    assert est == 44000 and a + b < est
    its.append(mcq("Noah estimates %s + %s as %s + %s = %s. Is the exact sum more or less than %s?"
                   % (nf(a), nf(b), nf(19000), nf(25000), nf(est), nf(est)),
                   ML(est)[1], [ML(est)[0], ML(est)[2], ML(est)[3]],
                   "Both numbers were rounded <b>up</b> (%s → %s and %s → %s), so the estimate is too big. "
                   "The exact sum, %s, is <b>less than %s</b>." % (nf(a), nf(19000), nf(b), nf(25000), nf(a + b), nf(est))))
    a, b = 412, 6
    est = front(a) * b
    assert est == 2400 and a * b > est
    its.append(mcq("Mei estimates 412 × 6 as 400 × 6 = 2400. Is the exact product more or less than 2400?",
                   ML(est)[0], [ML(est)[1], ML(est)[2], ML(est)[3]],
                   "412 was rounded <b>down</b> to 400, so the estimate is too small. "
                   "The exact product, %s, is <b>more than 2400</b>." % nf(a * b)))
    assert len(its) == 20, len(its)
    return {"title": "Estimate sums and products", "items": its}


# ============================================================ set 5: is the answer reasonable? (word problems)
def yn(q, said, exact, est, est_txt, trap, fmt, extra=""):
    ok = said == exact
    if ok:
        assert abs(said - est) / est < F(1, 10), (said, est)
    else:
        assert abs(said - est) / est > F(1, 2), (said, est)
    right = ("Yes, it is close to %s" if ok else "No, it should be about %s") % fmt(est)
    other = ("No, it should be about %s" if ok else "Yes, it is close to %s") % fmt(est)
    traps = ["Yes, it is close to %s" % fmt(trap), "No, it should be about %s" % fmt(trap)]
    e = "Estimate: %s. %s is %s %s, so the answer is %s.%s" % (
        est_txt, fmt(said), "close to" if ok else "far from", fmt(est),
        "<b>reasonable</b>" if ok else "<b>not reasonable</b>",
        "" if ok else " The exact answer is %s.%s" % (fmt(exact), extra))
    return mcq(q, right, [other] + traps, e)


def word_sum(q, terms, p, fmt=nf):
    rs = [rnd_to(n, p) for n in terms]
    est, exact = sum(rs), sum(terms)
    down = sum(n // p * p for n in terms)
    cands = [down, sum(steps(n, p)[-1] for n in terms), sum(rnd_to(n, p // 10) for n in terms), exact,
             est + p, est - p]
    e = ("Round to the nearest %s: %s = <b>%s</b>. (The exact answer is %s.)"
         % (WORD[p], " + ".join(fmt(r) for r in rs), fmt(est), fmt(exact)))
    return mcq(q, (fmt(est), F(est)), [(fmt(x), F(x)) for x in cands if x > 0], e)


def word_prod(q, a, b, unit):
    ra, rb = front(a), front(b)
    est, exact = ra * rb, a * b
    cands = [est // 10, est * 10, (a // 10 ** (len(str(a)) - 1) * 10 ** (len(str(a)) - 1)) *
             (b // 10 ** (len(str(b)) - 1) * 10 ** (len(str(b)) - 1) if b >= 10 else b), exact, ra + rb]
    u = lambda v: "%s %s" % (nf(v), unit)
    e = ("Round to the greatest place: %s × %s = <b>%s</b>.%s (The exact answer is %s.)"
         % (nf(ra), nf(rb), u(est), zeros_note(a, b), u(exact)))
    return mcq(q, (u(est), F(est)), [(u(x), F(x)) for x in cands if x > 0], e)


def set_words():
    its = []
    its.append(word_sum("A school’s Terry Fox Run raises %s in the morning and %s in the afternoon. "
                        "About how much money is that? Round to the nearest hundred."
                        % (money(2480), money(1365)), [2480, 1365], 100, money))
    its.append(word_sum("A park counts %s visitors on Saturday and %s visitors on Sunday. About how many "
                        "visitors is that? Round to the nearest thousand." % (nf(14865), nf(12390)),
                        [14865, 12390], 1000))
    its.append(word_prod("A BC Ferries boat carries 372 vehicles on each trip. It makes 8 trips in one day. "
                         "About how many vehicles is that? Round 372 to its greatest place.", 372, 8, "vehicles"))
    its.append(word_prod("Grouse Mountain’s gondola carries 98 people on each trip. It makes 42 trips one morning. "
                         "About how many people ride it? Round each number to its greatest place.", 98, 42, "people"))
    its.append(word_prod("Ryan’s school orders 23 boxes of granola bars for a field trip. Each box holds 48 bars. "
                         "About how many bars is that? Round each number to its greatest place.", 23, 48, "bars"))

    assert 12865 + 12390 == 25255
    its.append(yn("The nature house in Stanley Park counts %s visitors in July and %s visitors in August. "
                  "Simran adds them and gets %s. Is her answer reasonable? Round to the nearest thousand to check."
                  % (nf(12865), nf(12390), nf(25255)),
                  25255, 12865 + 12390, 25000, "%s + %s = %s" % (nf(13000), nf(12000), nf(25000)), 2500, nf))
    assert 3125 * 6 == 18750
    its.append(yn("A Kamloops arena sells %s tickets each night for 6 nights. Nadia says that is %s tickets. "
                  "Is her answer reasonable?" % (nf(3125), nf(18750)),
                  18750, 18750, 18000, "%s × 6 = %s" % (nf(3000), nf(18000)), 1800, nf))
    assert 28 * 375 == 10500
    its.append(yn("A ferry carries 375 cars on each trip and makes 28 trips in a week. Liam says that is 1050 cars. "
                  "Is his answer reasonable?",
                  1050, 10500, 12000, "400 × 30 = %s" % nf(12000), 1200, nf,
                  " Liam lost a zero."))
    assert F("2.48") + F("3.9") == F("6.38") and F("2.48") + F("0.39") == F("2.87")
    its.append(yn("Chloe hikes 2.48 km to a lookout and then 3.9 km to a lake in Whistler. She says she hiked "
                  "2.87 km in all. Is her answer reasonable?",
                  F("2.87"), F("6.38"), F("6.5"), "2.5 + 4 = 6.5", 5, lambda v: dd(v) + " km",
                  " Chloe lined up 3.9 as 0.39. Line up the decimal points."))
    its.append(yn("Kai runs %s km on Monday and %s km on Tuesday. He adds the tops and the bottoms and says he ran "
                  "%s km in all. Is his answer reasonable?" % (fr(7, 8), fr(5, 6), fr(12, 14)),
                  F(12, 14), F(7, 8) + F(5, 6), F(2), "%s is close to 1 and %s is close to 1, so 1 + 1 = 2"
                  % (fr(7, 8), fr(5, 6)), 1, lambda v: (fr(12, 14) if v == F(12, 14) else fx(v)) + " km",
                  " Do not add the tops and the bottoms."))

    assert 64 * 38 == 2432 and 64 * 8 + 64 * 3 == 704
    its.append(mcq("A whale-watching boat in Victoria takes 64 people on each trip. It makes 38 trips in May. "
                   "Use an estimate to choose the reasonable number of people.",
                   N(2432), [N(24320), N(704), N(102)],
                   "Estimate: 60 × 40 = 2400. Only <b>2432</b> is close to 2400. 24 320 has an extra zero, 704 forgets "
                   "that the 3 in 38 means 30, and 102 adds instead of multiplying."
                   .replace("24 320", nf(24320))))
    assert 386 * 6 == 2316
    its.append(mcq("A SkyTrain carries 386 people. 6 full trains arrive at a station. "
                   "Use an estimate to choose the reasonable number of people.",
                   N(2316), [N(23160), N(392), N(231)],
                   "Estimate: 400 × 6 = 2400. Only <b>2316</b> is close to 2400. %s has an extra zero, 392 adds "
                   "instead of multiplying, and 231 is missing a digit." % nf(23160)))

    # enough?
    items = [F("12.85"), F("18.40"), F("16.95")]
    rs = [rnd_to(x, 1) for x in items]
    est, exact, down = sum(rs), sum(items), sum(math.floor(x) for x in items)
    assert est == 48 and exact <= 50 and down == 46
    its.append(mcq("Harjot has %s for lunch at Grouse Mountain. He wants a burger for %s, a salad for %s and a "
                   "smoothie for %s. Is %s enough? Round to the nearest dollar."
                   % (money(50), money("12.85"), money("18.40"), money("16.95"), money(50)),
                   "Yes, about $48", ["No, about $48", "Yes, about $46", "No, about $50"],
                   "Round to the nearest dollar: $13 + $18 + $17 = $48. $48 is less than $50, so <b>yes</b>. "
                   "(The exact cost is %s.)" % money(exact)))
    ch = [168, 145, 172]
    est = sum(rnd_to(x, 100) for x in ch)
    assert est == 500 and sum(ch) > 450
    its.append(mcq("The school gym has 450 chairs for the spring concert. 168 students, 145 parents and 172 "
                   "grandparents are coming. Are there enough chairs? Round to the nearest hundred.",
                   "No, about 500 people", ["Yes, about 500 people", "Yes, about 300 people", "No, about 400 people"],
                   "Round to the nearest hundred: 200 + 100 + 200 = 500. 500 is more than 450, so <b>no</b>. "
                   "(Exactly %d people are coming.)" % sum(ch)))

    a, b = 285, 6
    assert front(a) * b == 1800 and a * b < 1800
    its.append(mcq("A bakery in Nanaimo makes 285 buns each day for 6 days. Olivia estimates 300 × 6 = 1800 buns. "
                   "Is the exact number more or less than 1800?",
                   "Less than 1800", ["More than 1800", "Exactly 1800", CANT],
                   "285 was rounded <b>up</b> to 300, so the estimate is too big. The exact number, %s, is "
                   "<b>less than 1800</b>." % nf(a * b)))

    t = [F("48.6"), F("12.7")]
    est = sum(rnd_to(x, 1) for x in t)
    assert est == 62 and sum(t) == F("61.3")
    its.append(mcq("Mateo’s family drives 48.6 km on the Sea-to-Sky Highway, then 12.7 km more to a campsite. "
                   "About how far do they drive? Round each to the nearest whole number.",
                   ("about 62 km", F(62)), [("about 60 km", F(60)), ("about 61.3 km", F("61.3")),
                                            ("about 50 km", F(50))],
                   "Round each one: 48.6 → 49 and 12.7 → 13. 49 + 13 = <b>62</b>. (The exact distance is 61.3 km. "
                   "60 drops the decimal parts.)"))
    assert nearest(F(5, 8), FMARKS) == "h" and nearest(F(1, 12), FMARKS) == "0"
    its.append(mcq("Mei uses %s cup of flour and %s cup of sugar for pancakes. About how much is that in all? "
                   "Use the benchmarks 0, %s and 1." % (fr(5, 8), fr(1, 12), fr(1, 2)),
                   ("about %s cup" % fr(1, 2), H), [("about 1 cup", F(1)), ("about 0 cups", F(0)),
                                                   ("about 1%s cups" % fr(1, 2), F(3, 2))],
                   "%s is close to %s and %s is close to 0. %s + 0 = <b>%s</b>. (Do not add the tops and the "
                   "bottoms: %s is not the sum.)" % (fr(5, 8), fr(1, 2), fr(1, 12), fr(1, 2), fr(1, 2), fr(6, 20))))
    assert nearest(F(11, 12), FMARKS) == "1" and nearest(F(4, 9), FMARKS) == "h"
    its.append(mcq("Jasleen walks %s km to school and %s km to the library. About how far does she walk? "
                   "Use the benchmarks 0, %s and 1." % (fr(11, 12), fr(4, 9), fr(1, 2)),
                   ("about 1%s km" % fr(1, 2), F(3, 2)), [("about 1 km", F(1)), ("about 2 km", F(2)),
                                                         ("about %s km" % fr(1, 2), H)],
                   "%s is close to 1 and %s is close to %s. 1 + %s = <b>1%s</b>." % (
                       fr(11, 12), fr(4, 9), fr(1, 2), fr(1, 2), fr(1, 2))))
    assert F("0.92") + F("0.47") == F("1.39")
    its.append(yn("Wei buys 0.92 kg of salmon and 0.47 kg of rice. He says the total is 0.139 kg. "
                  "Is his answer reasonable?",
                  F("0.139"), F("1.39"), F("1.5"), "0.92 is close to 1 and 0.47 is close to 0.5, so 1 + 0.5 = 1.5",
                  F("0.5"), lambda v: dd(v) + " kg",
                  " 9 tenths + 4 tenths = 13 tenths, which is 1 whole and 3 tenths."))
    assert 245 * 4 == 980
    its.append(yn("A canoe club paddles 245 km each summer for 4 summers. Zara says that is 980 km. "
                  "Is her answer reasonable?",
                  980, 980, 1000, "245 is close to 250, and 250 × 4 = 1000", 100, lambda v: nf(v) + " km"))
    assert len(its) == 20, len(its)
    return {"title": "Is the answer reasonable? Word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>What is a benchmark?</h2>"
        "<p>A benchmark is a friendly number you can compare with, like 0, 1, " + fr(1, 2) + ", 0.5 or "
        + nf(500000) + ". Benchmarks help you estimate: find a quick answer that is close to the exact answer.</p>"
        "<h2>Whole numbers: round to a benchmark</h2>"
        "<p>Look at the digit <b>one place to the right</b> of the place you are rounding to. "
        "<b>5 or more</b>: round up. <b>4 or less</b>: round down. Exactly halfway rounds up.</p>"
        "<figure class='sn-fig'>" + round_line(46820, 10000) +
        "<figcaption>46 820 is past the halfway point, 45 000, so to the nearest ten thousand it rounds up to 50 000."
        .replace(" 820", NB + "820").replace(" 000", NB + "000") + "</figcaption></figure>"
        + table(["Round to the nearest", "Look at the", "Example"], [
            ["thousand", "hundreds digit", "%s → %s" % (nf(58702), nf(59000))],
            ["ten thousand", "thousands digit", "%s → %s" % (nf(73150), nf(70000))],
            ["hundred thousand", "ten thousands digit", "%s → %s" % (nf(651200), nf(700000))],
        ])
        + ex("Do not round in steps", "Round %s to the nearest hundred thousand." % nf(348500),
             "Look only at the ten thousands digit: 4. 4 is 4 or less, so round down. (Rounding in steps, "
             "%s → %s → %s, gives the wrong answer.)" % (nf(348500), nf(350000), nf(400000)), nf(300000))
        + "<h2>Fractions: 0, " + fr(1, 2) + " or 1?</h2>"
        "<p>Compare the top number with the bottom number. If the top is <b>about half</b> of the bottom, the "
        "fraction is close to " + fr(1, 2) + ". If the top is <b>small</b>, it is close to 0. If the top is "
        "<b>almost the same</b> as the bottom, it is close to 1.</p>"
        "<figure class='sn-fig'>" + frac_line(3, 8) +
        "<figcaption>" + fr(3, 8) + " is only " + fr(1, 8) + " away from " + fr(1, 2) + " (" + fr(4, 8) +
        "), so it is closest to " + fr(1, 2) + ", not to 1.</figcaption></figure>"
        + ex("Estimate a fraction sum", "Estimate %s + %s." % (fr(7, 8), fr(4, 9)),
             "%s is close to 1. %s is close to %s. 1 + %s = 1%s." % (fr(7, 8), fr(4, 9), fr(1, 2), fr(1, 2), fr(1, 2)),
             "about 1" + fr(1, 2))
        + "<h2>Decimals: 0, 0.5 or 1?</h2>"
        "<p>0.5 is the same as 0.50 and 0.500. Write the decimals with the same number of places, then compare.</p>"
        "<figure class='sn-fig'>" + dec_line(F("0.82")) +
        "<figcaption>0.82 is 0.18 from 1 and 0.32 from 0.5, so it is closest to 1.</figcaption></figure>"
        + ex("Round with 0.5", "Round 3.48 to the nearest whole number.",
             "The decimal part is 0.48. 0.48 is less than 0.50, so round down. (Do not look only at the 8.)", "3")
        + "<h2>Estimate sums and products</h2>"
        "<p>Round each number, then add or multiply in your head. For products, round each number to its "
        "greatest place, multiply the front digits and then write the zeros.</p>"
        + ex("Estimate a product", "Estimate 48 × 31.",
             "Round: 50 × 30. 5 × 3 = 15, then write 2 zeros: 1500. (The exact answer is 1488.)", "about 1500")
        + ex("Is the answer reasonable?", "Liam says 375 × 28 = 1050.",
             "Estimate: 400 × 30 = %s. 1050 is far from %s, so it is not reasonable. The exact answer is %s."
             % (nf(12000), nf(12000), nf(10500)), "not reasonable")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["“" + fr(3, 8) + " is closest to 1 because 8 is big.”",
             "Compare 3 with half of 8 (4): " + fr(3, 8) + " is closest to " + fr(1, 2)],
            ["“0.09 is close to 1 because 9 is big.”", "0.09 is 9 hundredths: it is closest to 0"],
            ["Rounding the wrong place: %s to the nearest ten thousand → %s" % (nf(63820), nf(64000)),
             "Look at the thousands digit: 3, so %s" % nf(60000)],
            ["Rounding in steps: %s → %s → %s" % (nf(348500), nf(350000), nf(400000)),
             "Look only at the ten thousands digit: 4, so %s" % nf(300000)],
            ["Losing a zero: 50 × 30 = 150", "5 × 3 = 15, then write both zeros: 1500"],
        ])
    )


FAQ = [
    {"q": "What are benchmarks in Grade 5 math in BC?",
     "a": "Benchmarks are friendly numbers used to compare and estimate. In the BC Grade 5 curriculum, students use "
          "whole-number benchmarks like 500 000, the fraction benchmarks 0, 1/2 and 1, and the decimal benchmarks "
          "0, 0.5 and 1.".replace("500 000", nf(500000))},
    {"q": "How do you tell if a fraction is closer to 0, 1/2 or 1?",
     "a": "Compare the top number with half of the bottom number. 3/8 is close to 1/2 because 3 is close to 4 "
          "(half of 8), while 1/8 is close to 0 and 7/8 is close to 1."},
    {"q": "How do you estimate a product like 48 × 31?",
     "a": "Round each number to its greatest place: 50 × 30. Multiply 5 × 3 = 15 and write the two zeros, "
          "so the estimate is 1500 (the exact answer is 1488)."},
    {"q": "How can my child check if an answer is reasonable?",
     "a": "Estimate first, then compare. If 375 × 28 gives 1050 but 400 × 30 = 12 000, the answer is far too small "
          "and should be checked.".replace("12 000", nf(12000))},
]


def gen():
    rnd = random.Random(55804)
    sets = [set_whole(), set_fractions(), set_decimals(), set_estimate(), set_words()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            assert it["q"].count("<svg") <= 1
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
                assert not re.search(r"\d \d{3}\b", re.sub(r"<[^>]+>", "", x)), x   # typed space in a number
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-5", "slug": SLUG, "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 5 Benchmarks and Estimation",
        "seo_title": "Grade 5 Benchmarks and Estimation Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "Benchmarks and Estimation",
        "domain": "Number",
        "standard_code": "Grade 5: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/5/core",
        "standard_text": "Whole-number, fraction, and decimal benchmarks",
        "meta_desc": "Free Grade 5 math worksheets on benchmarks and estimation for the BC curriculum: round whole "
                     "numbers to 1 000 000, use the fraction benchmarks 0, 1/2 and 1 and the decimal benchmarks "
                     "0, 0.5 and 1, estimate sums and products, and check if answers are reasonable. "
                     "100 questions with an answer key.".replace("1 000 000", nf(1000000)),
        "key_big": "Compare with a friendly number: 0, 1/2 or 1 for fractions, 0, 0.5 or 1 for decimals.",
        "key_sub": "3/8 is closest to 1/2 (3 is close to half of 8), and 0.09 is closest to 0. To estimate, round "
                   "first: 48 × 31 is about 50 × 30 = 1500. If an answer is far from the estimate, check it.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "number line")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
