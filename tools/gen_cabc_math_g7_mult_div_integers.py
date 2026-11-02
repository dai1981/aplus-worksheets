# -*- coding: utf-8 -*-
"""
BC Grade 7 Math: Multiplying and dividing integers (BC Mathematics Curriculum, Grade 7: Computational fluency)
  python3 tools/gen_cabc_math_g7_mult_div_integers.py
Multiplication as repeated addition of negatives (3 × (−4) on a number line), the pattern that shows why
(−1) × (−4) = 4, the sign rules for × and ÷, division as the inverse of multiplication, mixed practice with all
four operations and the order of operations, and word problems in BC contexts (temperatures falling each hour,
sharing a debt, divers, hockey plus-minus, contest scores, mean winter temperatures).
Wrong answers come from real student mistakes: (−3) × (−4) = −12, (−12) ÷ 3 = 4, adding instead of multiplying,
one group too many on the number line, times-table slips, working left to right instead of × and ÷ first,
ignoring brackets, treating a negative divisor as positive, and forgetting the starting value in a word problem.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English. Real minus sign −.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-7")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
M = "−"
NBSP = " "
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Ji-woo", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]


# ------------------------------------------------------------ numbers
def n(v):
    """Integer with the real minus sign. BC style: 4 digits with no separator, 5+ with a no-break space."""
    v = F(v)
    assert v.denominator == 1, v
    a = abs(v.numerator)
    s = str(a) if a < 10000 else "{:,}".format(a).replace(",", NBSP)
    return (M if v < 0 else "") + s


def p(v):
    """Integer in an expression: negatives in brackets."""
    return "(" + n(v) + ")" if v < 0 else n(v)


def deg(v):
    return n(v) + NBSP + "°C"


def money(v):
    v = F(v)
    return (M if v < 0 else "") + "$" + n(abs(v))


def metres(v):
    return n(v) + NBSP + "m"


def cm(v):
    return n(v) + NBSP + "cm"


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def mcq(q, correct, cands, e, rnd):
    """correct and cands: strings, or (string, value) pairs. A candidate equal in value (or text) to the
    correct answer or to an earlier candidate is skipped."""
    cs, cv = correct if isinstance(correct, tuple) else (correct, None)
    seen, vals, pick = {plain(cs)}, ({cv} if cv is not None else set()), []
    for c in cands:
        if c is None:
            continue
        s, v = c if isinstance(c, tuple) else (c, None)
        if not s or plain(s) in seen:
            continue
        if v is not None:
            if v in vals:
                continue
            vals.add(v)
        seen.add(plain(s))
        pick.append(s)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, cs, cands)
    ch = pick + [cs]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(cs), "e": e}


def mcq_v(q, v, cands, e, rnd, fmt=n):
    ok = []
    for c in cands:
        if c is None:
            continue
        c = F(c)
        if c.denominator != 1:
            continue
        ok.append((fmt(c), c))
    return mcq(q, (fmt(v), F(v)), ok, e, rnd)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs, bold=False):
    return len(str(t)) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


class People:
    def __init__(self, rnd):
        self.pool = [(x, "she", "her") for x in GIRLS] + [(x, "he", "his") for x in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p_ = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p_


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions (5 each per set)."""
    for s in sets:
        items = s["items"]
        targets = [i for i in range(4) for _ in range(5)]
        rnd.shuffle(targets)
        for it, t in zip(items, targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t
        final = [sum(1 for it in items if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


# ------------------------------------------------------------ picture: jumps on a number line
def jumps_svg(k, d, label, gap=None):
    """Number line with k jumps of −d starting at 0. Tick every 1, number under 0 and every multiple of d."""
    end = -k * d
    lo, hi = end - 1, 2
    span = hi - lo
    g = gap or max(13, min(26, int(400 / span)))
    labels = [v for v in range(lo, hi + 1) if v % d == 0]
    lw = max(tw(n(v), 14) for v in labels)
    assert d * g >= lw + 6, ("labels overlap", k, d, g)
    pad = int(max(26, lw / 2 + 10))
    W = int(2 * pad + span * g)
    Y = 66
    H = Y + 34

    def X(v):
        return pad + (v - lo) * g

    s = []
    x0, x1 = pad - 16, W - pad + 16
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x0, Y, x1, Y, INK))
    s.append("<path d='M%d %d l9 -5 v10 z M%d %d l-9 -5 v10 z' fill='%s'/>" % (x0 - 2, Y, x1 + 2, Y, INK))
    for v in range(lo, hi + 1):
        x = X(v)
        big = v in labels
        h = 9 if big else 5
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x, Y - h, x, Y + h, INK, "1.8" if big else "1.2"))
        if big:
            s.append(text(x, Y + 26, n(v), 14, bold=(v == 0)))
    for i in range(k):
        a, b = -i * d, -(i + 1) * d
        xa, xb = X(a), X(b)
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                 % (xa, Y - 7, (xa + xb) / 2, Y - 44, xb, Y - 7, RED))
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d z' fill='%s'/>"
                 % (xb, Y - 7, xb + 8, Y - 13, xb + 2, Y - 17, RED))
        s.append(text((xa + xb) / 2, Y - 30, n(-d), 14, bold=True, col=RED))
    s.append("<circle cx='%.1f' cy='%d' r='5.5' fill='%s'/>" % (X(end), Y, GREEN))
    return svg_wrap(W, H, "".join(s), label)


def jl_label(k, d):
    return "number line with %d jumps of %s from 0 to %s" % (k, n(-d), n(-k * d))


# ============================================================ set 1: repeated addition
def set_repeated(rnd, P):
    its = []
    # A1: compute k × (−d) or (−d) × k (5)
    for k, d, rev in [(3, 4, False), (5, 2, False), (4, 6, True), (6, 3, False), (2, 9, True)]:
        v = -k * d
        expr = (p(-d) + " × " + n(k)) if rev else (n(k) + " × " + p(-d))
        sumx = " + ".join([p(-d)] * k)
        q = "What is %s?" % expr
        e = ("%s means %d groups of %s: %s = <b>%s</b>." % (expr, k, n(-d), sumx, n(v)) if not rev else
             "%s = %d × %s, which means %d groups of %s: %s = <b>%s</b>." % (expr, k, p(-d), k, n(-d), sumx, n(v)))
        its.append(mcq_v(q, v, [-v, k - d, v - d, -(k + d), v + d], e, rnd))
    # A2: which multiplication matches the repeated sum (4)
    for k, d in [(4, 5), (3, 7), (5, 3), (6, 2)]:
        v = -k * d
        sumx = " + ".join([p(-d)] * k)
        q = "Which multiplication has the same value as %s?" % sumx
        e = "There are %d groups of %s, so the sum is %d × %s = <b>%s</b>." % (k, n(-d), k, p(-d), n(v))
        cands = [(n(k) + " × " + n(d), k * d), (n(d) + " × " + p(-d), -d * d), (n(k) + " + " + p(-d), k - d),
                 (n(k - 1) + " × " + p(-d), -(k - 1) * d)]
        its.append(mcq(q, (n(k) + " × " + p(-d), v), cands, e, rnd))
    # B: number line with jumps (6)
    for k, d in [(3, 4), (2, 6), (4, 3), (5, 2), (3, 5), (4, 4)]:
        v = -k * d
        q = ("Each red jump is %s. Which multiplication does the number line show?" % n(-d) +
             fig(jumps_svg(k, d, jl_label(k, d))))
        e = "There are %d jumps of %s, ending at %s. So <b>%d × %s = %s</b>." % (k, n(-d), n(v), k, p(-d), n(v))
        cands = [(n(k) + " × " + n(d) + " = " + n(k * d), "pos"), (n(k + 1) + " × " + p(-d) + " = " + n(v - d), "extra"),
                 (n(k) + " + " + p(-d) + " = " + n(k - d), "add"), (n(d) + " × " + p(-d) + " = " + n(-d * d), "dd")]
        its.append(mcq(q, (n(k) + " × " + p(-d) + " = " + n(v), "ok"), cands, e, rnd))
    # C: pattern to negative × negative (5)
    for d, last in [(3, -1), (4, -1), (2, -2), (5, -2), (6, -1)]:
        rows = list(range(2, last - 1, -1))
        shown = rows[:-1]
        v = last * -d
        lines = "<br>".join("%s × %s = %s" % (p(a), p(-d), n(a * -d)) for a in shown)
        q = "Look at the pattern.<br>%s<br>%s × %s = ?" % (lines, p(last), p(-d))
        e = ("Each time the first factor goes down by 1, the product goes <b>up</b> by %d. "
             "So %s × %s = <b>%s</b>. A negative times a negative is positive." % (d, p(last), p(-d), n(v)))
        its.append(mcq_v(q, v, [-v, last - d, 0, v + d, v - d], e, rnd))
    return {"title": "Multiplication as repeated addition", "items": its}


# ============================================================ set 2: sign rules
def sign_word(v):
    return "positive" if v > 0 else "negative"


def e_mul(a, b):
    v = a * b
    same = (a < 0) == (b < 0)
    return ("%d × %d = %d. The signs are %s, so the product is %s: %s × %s = <b>%s</b>."
            % (abs(a), abs(b), abs(v), "the same" if same else "different", sign_word(v), p(a), p(b), n(v)))


def e_div(a, b):
    v = a // b
    same = (a < 0) == (b < 0)
    return ("%d ÷ %d = %d. The signs are %s, so the quotient is %s: %s ÷ %s = <b>%s</b>."
            % (abs(a), abs(b), abs(v), "the same" if same else "different", sign_word(v), p(a), p(b), n(v)))


def set_signs(rnd, P):
    its = []
    for a, b in [(-6, -7), (-8, 5), (9, -4), (-12, -3), (-25, 4), (-11, -6)]:
        v = a * b
        its.append(mcq_v("%s × %s = ?" % (p(a), p(b)), v, [-v, a + b, -(a + b), a - b], e_mul(a, b), rnd))
    for a, b in [(-56, 7), (-48, -6), (63, -9), (-72, -8), (-90, 15), (84, -12)]:
        v = a // b
        assert a == v * b
        sg = 1 if v > 0 else -1
        its.append(mcq_v("%s ÷ %s = ?" % (p(a), p(b)), v, [-v, v + sg, -(v + sg), v - sg], e_div(a, b), rnd))
    # three factors (4)
    for a, b, c in [(-2, 3, -5), (-1, -4, -6), (4, -2, 5), (-3, -2, -5)]:
        v = a * b * c
        neg = sum(1 for x in (a, b, c) if x < 0)
        e = ("%d × %d × %d = %d. There %s %d negative factor%s (%s), so the product is %s: <b>%s</b>."
             % (abs(a), abs(b), abs(c), abs(v), "is" if neg == 1 else "are", neg, "" if neg == 1 else "s",
                "odd" if neg % 2 else "even", sign_word(v), n(v)))
        its.append(mcq_v("%s × %s × %s = ?" % (p(a), p(b), p(c)), v, [-v, a + b + c, a * b + c, -(a + b + c)], e, rnd))
    # which statement is true (2)
    q = "Which statement is true?"
    its.append(mcq(q, "(" + M + "6) × (" + M + "4) = 24",
                   ["(" + M + "6) × (" + M + "4) = " + M + "24", "(" + M + "24) ÷ 6 = 4", "24 ÷ (" + M + "6) = 4"],
                   "Same signs give a positive product: (" + M + "6) × (" + M + "4) = <b>24</b>. "
                   "The two divisions have different signs, so their quotients are " + M + "4, not 4.", rnd))
    its.append(mcq(q, "(" + M + "45) ÷ (" + M + "9) = 5",
                   ["(" + M + "45) ÷ (" + M + "9) = " + M + "5", "(" + M + "5) × 9 = 45", "5 × (" + M + "9) = 45"],
                   "Same signs give a positive quotient: (" + M + "45) ÷ (" + M + "9) = <b>5</b>. "
                   "The two products have different signs, so they are " + M + "45, not 45.", rnd))
    # which is negative / positive (2)
    its.append(mcq("Which product is negative?", "(" + M + "7) × 3",
                   ["(" + M + "7) × (" + M + "3)", "7 × 3 × 0", "(" + M + "1) × (" + M + "7) × 3"],
                   "Different signs give a negative product: (" + M + "7) × 3 = <b>" + M + "21</b>. "
                   "(" + M + "7) × (" + M + "3) = 21 and (" + M + "1) × (" + M + "7) × 3 = 21 are positive, and 7 × 3 × 0 = 0.", rnd))
    its.append(mcq("Which quotient is positive?", "(" + M + "36) ÷ (" + M + "4)",
                   ["(" + M + "36) ÷ 4", "36 ÷ (" + M + "4)", "0 ÷ (" + M + "4)"],
                   "Same signs give a positive quotient: (" + M + "36) ÷ (" + M + "4) = <b>9</b>. "
                   "The other two divisions with different signs give " + M + "9, and 0 ÷ (" + M + "4) = 0.", rnd))
    return {"title": "Sign rules for × and ÷", "items": its}


# ============================================================ set 3: division as the inverse
def set_inverse(rnd, P):
    its = []
    # given a multiplication fact, find a division (7)
    for a, b, which in [(6, -7, "b"), (6, -7, "a"), (-4, -9, "b"), (-5, 8, "a"), (-3, -11, "a"), (7, -8, "a"), (-9, -6, "b")]:
        prod = a * b
        if which == "b":   # prod ÷ a = b
            dv, ans = a, b
        else:              # prod ÷ b = a
            dv, ans = b, a
        q = "%s × %s = %s. Use this fact to find %s ÷ %s." % (p(a), p(b), n(prod), p(prod), p(dv))
        e = ("Division undoes multiplication. %s × %s = %s, so %s ÷ %s = <b>%s</b>."
             % (p(dv), p(ans), n(prod), p(prod), p(dv), n(ans)))
        its.append(mcq_v(q, ans, [-ans, dv, -dv, prod - dv], e, rnd))
    # missing factor (7)
    for known, prod, left in [(-8, 48, True), (5, -45, False), (-7, -63, True), (-6, 54, False), (12, -60, True),
                              (-4, -32, False), (-9, 81, True)]:
        ans = prod // known
        assert ans * known == prod
        q = ("□ × %s = %s. What number goes in the box?" % (p(known), n(prod)) if left else
             "%s × □ = %s. What number goes in the box?" % (p(known), n(prod)))
        e = ("Divide to find the missing factor: %s ÷ %s = %s. Check: %s × %s = %s. The box is <b>%s</b>."
             % (p(prod), p(known), n(ans), p(ans), p(known), n(prod), n(ans)))
        its.append(mcq_v(q, ans, [-ans, prod - known, prod + known, prod * known], e, rnd))
    # which multiplication checks a division (3)
    for a, b in [(-35, 5), (42, -6), (-64, -8)]:
        v = a // b
        q = "Which multiplication checks that %s ÷ %s = %s?" % (p(a), p(b), n(v))
        e = "Multiply the quotient by the divisor to get back the dividend: <b>%s × %s = %s</b>." % (p(v), p(b), n(a))
        cands = ["%s × %s = %s" % (p(-v), p(b), n(-a)), "%s × %s = %s" % (p(v), p(-b), n(-a)),
                 "%s × %s = %s" % (p(a), p(b), n(a * b))]
        its.append(mcq(q, "%s × %s = %s" % (p(v), p(b), n(a)), cands, e, rnd))
    # missing dividend (3)
    for dv, ans in [(-4, 9), (6, -7), (-5, -8)]:
        x = dv * ans
        q = "□ ÷ %s = %s. What number goes in the box?" % (p(dv), n(ans))
        e = ("Multiply to undo the division: %s × %s = %s. Check: %s ÷ %s = %s. The box is <b>%s</b>."
             % (p(ans), p(dv), n(x), p(x), p(dv), n(ans), n(x)))
        its.append(mcq_v(q, x, [-x, ans + dv, ans - dv, -(ans - dv)], e, rnd))
    return {"title": "Division as the inverse of multiplication", "items": its}


# ============================================================ set 4: all four operations
def first(v):
    """First number in an expression: no brackets needed."""
    return n(v)


def set_mixed(rnd, P):
    its = []
    # plain add / subtract (4)
    for a, b, op in [(-7, 3, "+"), (-5, -8, "-"), (4, -9, "+"), (-6, 11, "-")]:
        v = a + b if op == "+" else a - b
        if op == "+":
            q = "%s + %s = ?" % (first(a), p(b))
            if (a < 0) != (b < 0):
                e = "The signs are different, so subtract: %d − %d = %d. The sign comes from the number farther from 0: <b>%s</b>." % (
                    max(abs(a), abs(b)), min(abs(a), abs(b)), abs(v), n(v))
            else:
                e = "Both numbers are negative, so add the sizes and keep the minus sign: <b>%s</b>." % n(v)
            cands = [-v, a - b, -(a - b), a * b]
        else:
            q = "%s − %s = ?" % (first(a), p(b))
            e = "Subtracting is adding the opposite: %s + %s = <b>%s</b>." % (first(a), p(-b), n(v))
            cands = [a + b, -v, -(a + b), a * b]
        its.append(mcq_v(q, v, cands, e, rnd))
    # a + b × c (3)
    for a, b, c in [(-6, 4, -2), (5, -3, 4), (-10, -2, -3)]:
        v = a + b * c
        q = "%s + %s × %s = ?" % (first(a), p(b), p(c))
        e = "Multiply first: %s × %s = %s. Then %s + %s = <b>%s</b>." % (p(b), p(c), n(b * c), first(a), p(b * c), n(v))
        its.append(mcq_v(q, v, [(a + b) * c, a - b * c, -v, a + abs(b * c)], e, rnd))
    # a − b ÷ c (3)
    for a, b, c in [(8, -12, 4), (-8, 20, -4), (-6, -18, -6)]:
        v = a - F(b, c)
        lr = F(a - b, c)
        q = "%s − %s ÷ %s = ?" % (first(a), p(b), p(c))
        e = "Divide first: %s ÷ %s = %s. Then %s − %s = <b>%s</b>." % (p(b), p(c), n(F(b, c)), first(a), p(F(b, c)), n(v))
        its.append(mcq_v(q, v, [lr, a + F(b, c), -v, F(a + b, c), a - abs(F(b, c))], e, rnd))
    # (a + b) × c (3)
    for a, b, c in [(-9, 4, -3), (2, -7, 6), (-4, -1, -5)]:
        v = (a + b) * c
        q = "(%s + %s) × %s = ?" % (first(a), p(b), p(c))
        e = "Brackets first: %s + %s = %s. Then %s × %s = <b>%s</b>." % (first(a), p(b), n(a + b), p(a + b), p(c), n(v))
        its.append(mcq_v(q, v, [a + b * c, -v, (a - b) * c, a * c + b], e, rnd))
    # a × b + c × d (3)
    for a, b, c, d in [(-3, 5, -2, -4), (4, -6, 3, 2), (-7, -2, 5, -3)]:
        v = a * b + c * d
        q = "%s × %s + %s × %s = ?" % (first(a), p(b), p(c), p(d))
        e = ("Multiply first: %s × %s = %s and %s × %s = %s. Then %s + %s = <b>%s</b>."
             % (first(a), p(b), n(a * b), p(c), p(d), n(c * d), n(a * b), p(c * d), n(v)))
        its.append(mcq_v(q, v, [(a * b + c) * d, a * b - c * d, -v, a * b + abs(c * d)], e, rnd))
    # (a − b) ÷ c (2)
    for a, b, c in [(-10, -2, 4), (6, -9, -3)]:
        v = F(a - b, c)
        assert v.denominator == 1
        q = "(%s − %s) ÷ %s = ?" % (first(a), p(b), p(c))
        e = ("Brackets first: %s − %s = %s + %s = %s. Then %s ÷ %s = <b>%s</b>."
             % (first(a), p(b), first(a), p(-b), n(a - b), p(a - b), p(c), n(v)))
        its.append(mcq_v(q, v, [F(a + b, c), -v, a - F(b, c), F(a + b, -c), a - b + c], e, rnd))
    # a × (b − c) (2)
    for a, b, c in [(-4, 3, 8), (5, -2, -7)]:
        v = a * (b - c)
        q = "%s × (%s − %s) = ?" % (first(a), first(b), p(c))
        e = ("Brackets first: %s − %s = %s. Then %s × %s = <b>%s</b>."
             % (first(b), p(c), n(b - c), first(a), p(b - c), n(v)))
        its.append(mcq_v(q, v, [a * b - c, a * (b + c), -v, a * b + c], e, rnd))
    return {"title": "Mixed practice: all four operations", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd, P):
    its = []
    # 1-2: temperature change only
    for place, rate, hrs in [("on Grouse Mountain", 2, 5), ("in Prince George", 3, 4)]:
        v = -rate * hrs
        q = ("After sunset, the temperature %s falls %d" % (place, rate) + NBSP + "°C each hour. "
             "What is the total change in temperature after %d hours?" % hrs)
        e = "A fall of %s each hour for %d hours: %d × %s = <b>%s</b>." % (deg(rate), hrs, hrs, p(-rate), deg(v))
        its.append(mcq_v(q, v, [-v, -(rate + hrs), v + rate, v - rate], e, rnd, fmt=deg))
    # 3-4: temperature with a start
    for place, start, t0, rate, hrs in [("in Whistler", 4, "6 p.m.", 3, 4), ("in Kamloops", -2, "8 p.m.", 2, 4)]:
        v = start - rate * hrs
        t1 = {"6 p.m.": "10 p.m.", "8 p.m.": "midnight"}[t0]
        q = ("At %s, the temperature %s is %s. It falls %d" % (t0, place, deg(start), rate) + NBSP +
             "°C each hour. What is the temperature at %s?" % t1)
        e = ("From %s to %s is %d hours. The change is %d × %s = %s. Then %s + %s = <b>%s</b>."
             % (t0, t1, hrs, hrs, p(-rate), deg(-rate * hrs), n(start), p(-rate * hrs), deg(v)))
        its.append(mcq_v(q, v, [-rate * hrs, start + rate * hrs, -v, start - rate * (hrs - 1)], e, rnd, fmt=deg))
    # 5-7: sharing a debt
    for who, debt, k in [("Five friends", 40, 5), ("The six players on a volleyball team", 90, 6),
                         ("Four cousins", 72, 4)]:
        v = F(-debt, k)
        q = ("%s owe %s together for a BC Ferries trip, and they share the debt equally. "
             "Which integer shows each person’s share, in dollars?" % (who, money(debt)) if debt == 40 else
             "%s owe %s together for a bus to a tournament in Kelowna, and they share the debt equally. "
             "Which integer shows each person’s share, in dollars?" % (who, money(debt)) if debt == 90 else
             "%s owe %s together for a cabin on Vancouver Island, and they share the debt equally. "
             "Which integer shows each person’s share, in dollars?" % (who, money(debt)))
        e = "A debt is negative: %s ÷ %d = <b>%s</b>. Each person owes $%d." % (p(-debt), k, n(v), debt // k)
        its.append(mcq_v(q, v, [-v, -debt * k, -(debt - k), debt - k], e, rnd))
    # 8-9: scuba diver
    for nm_, rate, mins in [(None, 3, 6), (None, 4, 5)]:
        nm, he, his = P.next()
        v = -rate * mins
        q = ("%s is scuba diving off Vancouver Island. %s starts at the surface (0" % (nm, he.capitalize()) + NBSP +
             "m) and goes down %d" % rate + NBSP + "m each minute for %d minutes. Which integer shows %s position?" % (mins, his))
        e = "Down is negative: %d × %s = <b>%s</b>, so %s is %d" % (mins, p(-rate), metres(v), he, rate * mins) + NBSP + "m below the surface."
        its.append(mcq_v(q, v, [-v, -(rate + mins), v + rate, v - rate], e, rnd, fmt=metres))
    # 10-11: bank account
    for amt, wks in [(6, 8), (15, 4)]:
        nm, he, his = P.next()
        v = -amt * wks
        q = ("%s pays $%d each week for a phone plan from %s savings account. "
             "Which integer shows the change in %s balance after %d weeks, in dollars?" % (nm, amt, his, his, wks)
             if amt == 6 else
             "%s pays $%d each week for swimming lessons from %s savings account. "
             "Which integer shows the change in %s balance after %d weeks, in dollars?" % (nm, amt, his, his, wks))
        e = "Paying out is negative: %d × %s = <b>%s</b>." % (wks, p(-amt), n(v))
        its.append(mcq_v(q, v, [-v, -(amt + wks), v + amt, amt - wks], e, rnd))
    # 12-13: rate from total change
    for total, hrs, ctx in [(-18, 6, "temp"), (-24, 4, "river")]:
        v = F(total, hrs)
        if ctx == "temp":
            q = ("Overnight in Vernon, the temperature changed by %s in %d hours. It fell by the same amount each hour. "
                 "What was the change each hour?" % (deg(total), hrs))
            e = "Divide the total change by the hours: %s ÷ %d = <b>%s</b> each hour." % (p(total), hrs, deg(v))
            fmt = deg
        else:
            q = ("After a dry spell, the level of a creek near Nanaimo changed by %s in %d days. It fell by the same amount each day. "
                 "What was the change each day?" % (cm(total), hrs))
            e = "Divide the total change by the days: %s ÷ %d = <b>%s</b> each day." % (p(total), hrs, cm(v))
            fmt = cm
        its.append(mcq_v(q, v, [-v, total + hrs, total - hrs, total * hrs], e, rnd, fmt=fmt))
    # 14-15: how many hours / days (positive answer)
    for rate, total, ctx in [(4, -28, "reservoir"), (2, -14, "temp")]:
        v = F(total, -rate)
        if ctx == "reservoir":
            q = ("The water level in a reservoir falls 4" + NBSP + "cm each day. After how many days will the change be %s?" % cm(total))
            e = "Each day the change is " + cm(-4) + ". " + p(total) + " ÷ " + p(-4) + " = <b>%s</b> days (same signs, positive)." % n(v)
            its.append(mcq(q, (n(v) + " days", v), [(M + n(v) + " days", -v), ("112 days", F(112)), ("24 days", F(24))], e, rnd))
        else:
            q = ("At midnight in Fort St. John, the temperature is 0" + NBSP + "°C and falls 2" + NBSP +
                 "°C each hour. After how many hours will it be %s?" % deg(total))
            e = "Each hour the change is " + deg(-2) + ". " + p(total) + " ÷ " + p(-2) + " = <b>%s</b> hours (same signs, positive)." % n(v)
            its.append(mcq(q, (n(v) + " hours", v), [(M + n(v) + " hours", -v), ("28 hours", F(28)), ("12 hours", F(12))], e, rnd))
    # 16-17: contest scoring
    for right, wrong, plus, minus in [(6, 4, 5, 2), (9, 6, 4, 3)]:
        nm, he, his = P.next()
        v = right * plus + wrong * -minus
        q = ("In a math contest, each correct answer scores +%d and each wrong answer scores %s. "
             "%s gets %d correct and %d wrong. What is %s score?" % (plus, n(-minus), nm, right, wrong, his))
        e = ("%d × %d + %d × %s = %d + %s = <b>%s</b>."
             % (right, plus, wrong, p(-minus), right * plus, p(-wrong * minus), n(v)))
        its.append(mcq_v(q, v, [right * plus + wrong * minus, (right + wrong) * (plus - minus), -v,
                                right * plus - minus], e, rnd))
    # 18-19: mean of temperatures
    for place, temps in [("Prince George", [-8, -12, -4, -3, -8]), ("Smithers", [-15, -9, -14, -6, -6])]:
        tot = sum(temps)
        v = F(tot, len(temps))
        assert v.denominator == 1
        srt = sorted(temps)
        med = srt[2]
        q = ("The low temperatures in %s on five days in January were " % place +
             ", ".join(deg(t) for t in temps) + ". What was the mean low temperature?")
        e = "Add: %s. Divide by 5: %s ÷ 5 = <b>%s</b>." % (" + ".join(p(t) if i else n(t) for i, t in enumerate(temps)) + " = " + n(tot),
                                                            p(tot), deg(v))
        its.append(mcq_v(q, v, [-v, tot, med, F(tot, 4)], e, rnd, fmt=deg))
    # 20: hockey plus-minus
    nm, he, his = P.next()
    q = ("In hockey, a player’s plus-minus goes up 1 when %s team scores while %s is on the ice and down 1 when the other team scores. "
         "%s has a plus-minus of %s in each of 4 games. What is %s total plus-minus for the 4 games?" % (his, he, nm, n(-2), his))
    e = "Each game adds %s to the total: 4 × %s = <b>%s</b>." % (n(-2), p(-2), n(-8))
    its.append(mcq_v(q, -8, [8, -6, -2], e, rnd))
    return {"title": "Word problems: temperature, debts and more", "items": its}


# ============================================================ lesson
def body_html():
    j = jumps_svg(3, 4, jl_label(3, 4), gap=20)
    pat = table(["Multiplication", "Product"], [
        ["3 × (" + M + "4)", M + "12"], ["2 × (" + M + "4)", M + "8"], ["1 × (" + M + "4)", M + "4"],
        ["0 × (" + M + "4)", "0"], ["(" + M + "1) × (" + M + "4)", "4"], ["(" + M + "2) × (" + M + "4)", "8"]])
    return (
        "<h2>Multiplying is repeated addition</h2>"
        "<p>3 × (" + M + "4) means 3 groups of " + M + "4. Add them: (" + M + "4) + (" + M + "4) + (" + M + "4) = " + M + "12. "
        "On a number line, start at 0 and make 3 jumps of " + M + "4.</p>"
        "<figure class='sn-fig'>" + j +
        "<figcaption>3 jumps of " + M + "4 end at " + M + "12, so 3 × (" + M + "4) = " + M + "12. "
        "The order does not matter: (" + M + "4) × 3 = " + M + "12 too.</figcaption></figure>"
        "<h2>Why a negative times a negative is positive</h2>"
        "<p>Follow the pattern. Each time the first factor goes down by 1, the product goes <b>up</b> by 4. "
        "Keep going past 0 and the products become positive.</p>" + pat +
        "<h2>The sign rules</h2>"
        "<p>Multiply or divide the numbers without their signs. Then choose the sign. "
        "<b>Same signs give a positive answer. Different signs give a negative answer.</b> The rules are the same for × and ÷.</p>" +
        table(["Signs", "Multiply", "Divide"], [
            ["positive and positive", "3 × 4 = 12", "12 ÷ 3 = 4"],
            ["negative and negative", "(" + M + "3) × (" + M + "4) = 12", "(" + M + "12) ÷ (" + M + "3) = 4"],
            ["positive and negative", "3 × (" + M + "4) = " + M + "12", "12 ÷ (" + M + "3) = " + M + "4"],
            ["negative and positive", "(" + M + "3) × 4 = " + M + "12", "(" + M + "12) ÷ 3 = " + M + "4"],
        ]) +
        "<p>With three or more factors, count the negative factors. An even number of them gives a positive product; "
        "an odd number gives a negative product.</p>"
        "<h2>Division undoes multiplication</h2>"
        "<p>Every multiplication fact gives two division facts. Use it to check your sign.</p>" +
        ex("Example 1", "What is (" + M + "42) ÷ 6?",
           "Ask: 6 × ? = " + M + "42. Since 6 × (" + M + "7) = " + M + "42, the quotient is " + M + "7.", M + "7") +
        ex("Example 2", "□ × (" + M + "8) = 48. What number goes in the box?",
           "Divide: 48 ÷ (" + M + "8) = " + M + "6. Check: (" + M + "6) × (" + M + "8) = 48.", M + "6") +
        "<h2>Order of operations</h2>"
        "<p>Do brackets first, then × and ÷ from left to right, then + and − from left to right. "
        "Write negative numbers in brackets so the signs are easy to see.</p>" +
        ex("Example 3", M + "6 + 4 × (" + M + "2)",
           "Multiply first: 4 × (" + M + "2) = " + M + "8. Then " + M + "6 + (" + M + "8) = " + M + "14.", M + "14") +
        ex("Example 4", "The temperature in Whistler is 4" + NBSP + "°C at 6 p.m. and falls 3" + NBSP + "°C each hour. "
           "What is it at 10 p.m.?",
           "4 hours × (" + M + "3) = " + M + "12. Then 4 + (" + M + "12) = " + M + "8.", deg(-8)) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["(" + M + "3) × (" + M + "4) = " + M + "12", "Same signs give a positive answer: 12"],
            ["(" + M + "12) ÷ 3 = 4", "Different signs give a negative answer: " + M + "4"],
            ["Adding instead of multiplying: 3 × (" + M + "4) = " + M + "1", "3 × (" + M + "4) is 3 groups of " + M + "4: " + M + "12"],
            ["Working left to right: " + M + "6 + 4 × (" + M + "2) = 4", "Multiply before you add: " + M + "6 + (" + M + "8) = " + M + "14"],
            ["Forgetting the starting temperature", "Add the change to the start: 4 + (" + M + "12) = " + M + "8"],
        ])
    )


FAQ = [
    {"q": "What do Grade 7 students learn about integers in BC?",
     "a": "The BC Grade 7 math curriculum includes operations with integers: adding, subtracting, multiplying and dividing them, and using the order of operations. Students use number lines, patterns and contexts like temperature and money."},
    {"q": "Why is a negative times a negative a positive?",
     "a": "Look at the pattern 2 × (−4) = −8, 1 × (−4) = −4, 0 × (−4) = 0. Each step the product goes up by 4, so (−1) × (−4) = 4 and (−2) × (−4) = 8."},
    {"q": "What are the rules for dividing integers?",
     "a": "Divide the numbers without their signs, then choose the sign: same signs give a positive quotient and different signs give a negative quotient. So (−12) ÷ 3 = −4 and (−12) ÷ (−3) = 4."},
    {"q": "Do these integer worksheets help with the Grade 7 FSA?",
     "a": "Yes. The Grade 7 FSA includes numeracy, where students use number sense to solve problems. Working with integers in contexts like falling temperatures and shared debts, as in these worksheets, is good practice for it."},
]


def gen_unit():
    rnd = random.Random(37802)
    P = People(rnd)
    sets = [set_repeated(rnd, P), set_signs(rnd, P), set_inverse(rnd, P), set_mixed(rnd, P), set_words(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len({plain(c) for c in it["c"]}) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1
            k = plain(it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-7", "slug": "multiplying-and-dividing-integers", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 7 Multiplying and Dividing Integers",
        "seo_title": "Grade 7 Multiplying and Dividing Integers Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Multiplying and dividing integers",
        "domain": "Computational fluency",
        "standard_code": "Grade 7: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/7/core",
        "standard_text": "Operations with integers (addition, subtraction, multiplication, division, and order of operations)",
        "meta_desc": "Free Grade 7 math worksheets on multiplying and dividing integers for the BC curriculum: repeated addition like 3 × (−4), the sign rules, division as the inverse of multiplication, order of operations, and word problems with falling temperatures and shared debts. 100 questions with an answer key, good FSA numeracy practice.",
        "key_big": "Same signs give a positive answer; different signs give a negative answer. (−3) × (−4) = 12 and (−12) ÷ 3 = −4.",
        "key_sub": "3 × (−4) means three groups of −4: (−4) + (−4) + (−4) = −12. Check a division with multiplication: (−12) ÷ 3 = −4 because 3 × (−4) = −12.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "number line")
    os.makedirs(OUT, exist_ok=True)
    path_ = os.path.join(OUT, u["slug"] + ".json")
    with open(path_, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path_)
