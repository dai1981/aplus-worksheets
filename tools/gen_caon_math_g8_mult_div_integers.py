# -*- coding: utf-8 -*-
"""
Ontario Grade 8 Math: Multiplying and Dividing Integers (Ontario Mathematics Curriculum 2020, Grade 8: B2.7)
  python3 tools/gen_caon_math_g8_mult_div_integers.py
Patterns that lead to the sign rules (jumps on a number line, product and quotient patterns that continue past 0),
multiplying two, three and four integers, dividing integers and checking with multiplication, mixed practice with
the order of operations (brackets, squares, fraction-style quotients), and word problems in Ontario contexts
(temperatures falling each hour, sharing a debt, divers in Georgian Bay, account payments, contest scores, means).
Wrong answers come from real student mistakes: (−3) × (−4) = −12, (−12) ÷ 3 = 4, adding instead of multiplying,
one jump too many, working left to right instead of × and ÷ first, ignoring brackets, (−3)² = −9,
counting the sign of only the first two factors, and forgetting the starting value in a word problem.
Helpers are adapted from gen_cabc_math_g7_mult_div_integers.py; wording is rewritten for Ontario Grade 8.
Canadian English, real minus sign −. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-8")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
M = "−"
NBSP = "\u00a0"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


# ------------------------------------------------------------ numbers
def n(v):
    """Integer with the real minus sign. Ontario style: 4 digits with no separator, 5+ with a no-break space."""
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


def sign_word(v):
    return "positive" if v > 0 else "negative"


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


# ============================================================ set 1: patterns
def set_patterns(rnd, P):
    its = []
    # A: number line jumps (5)
    for k, d in [(3, 4), (2, 7), (4, 3), (5, 2), (3, 5)]:
        v = -k * d
        q = ("Each red jump is %s. Which multiplication does the number line show?" % n(-d) +
             fig(jumps_svg(k, d, jl_label(k, d))))
        e = ("There are %d jumps of %s, starting at 0 and ending at %s. So <b>%d × %s = %s</b>."
             % (k, n(-d), n(v), k, p(-d), n(v)))
        cands = [(n(k) + " × " + n(d) + " = " + n(k * d), "pos"), (n(k + 1) + " × " + p(-d) + " = " + n(v - d), "extra"),
                 (n(k) + " + " + p(-d) + " = " + n(k - d), "add"), (n(d) + " × " + p(-d) + " = " + n(-d * d), "dd")]
        its.append(mcq(q, (n(k) + " × " + p(-d) + " = " + n(v), "ok"), cands, e, rnd))
    # B: positive × positive continued past 0 -> negative × positive (4)
    for d, last in [(4, -1), (6, -2), (3, -3), (9, -1)]:
        rows = list(range(3, last - 1, -1))
        shown = rows[:-1]
        v = last * d
        lines = "<br>".join("%s × %s = %s" % (p(a), n(d), n(a * d)) for a in shown)
        q = "Continue the pattern.<br>%s<br>%s × %s = ?" % (lines, p(last), n(d))
        e = ("Each time the first factor goes down by 1, the product goes <b>down</b> by %d. "
             "So %s × %s = <b>%s</b>. A negative times a positive is negative." % (d, p(last), n(d), n(v)))
        its.append(mcq_v(q, v, [-v, last + d, v + d, v - d, 0], e, rnd))
    # C: negative × negative patterns (5)
    for d, last in [(3, -1), (5, -1), (2, -3), (7, -2), (8, -1)]:
        rows = list(range(2, last - 1, -1))
        shown = rows[:-1]
        v = last * -d
        lines = "<br>".join("%s × %s = %s" % (p(a), p(-d), n(a * -d)) for a in shown)
        q = "Continue the pattern.<br>%s<br>%s × %s = ?" % (lines, p(last), p(-d))
        e = ("Each time the first factor goes down by 1, the product goes <b>up</b> by %d. "
             "So %s × %s = <b>%s</b>. A negative times a negative is positive." % (d, p(last), p(-d), n(v)))
        its.append(mcq_v(q, v, [-v, last - d, 0, v + d, v - d], e, rnd))
    # D: division patterns (4)
    for dv, last in [(4, -1), (5, -2), (-3, -1), (-6, -2)]:
        # dividends go down by |dv| each row; quotient = dividend / dv
        a_ = abs(dv)
        divs = [m * a_ for m in range(2, last - 1, -1)]
        shown = divs[:-1]
        x = divs[-1]
        v = x // dv
        lines = "<br>".join("%s ÷ %s = %s" % (p(t), p(dv), n(t // dv)) for t in shown)
        q = "Continue the pattern.<br>%s<br>%s ÷ %s = ?" % (lines, p(x), p(dv))
        step = "down" if dv > 0 else "up"
        e = ("Each time the dividend goes down by %d, the quotient goes <b>%s</b> by 1. So %s ÷ %s = <b>%s</b>. "
             "Check: %s × %s = %s." % (a_, step, p(x), p(dv), n(v), p(v), p(dv), n(x)))
        its.append(mcq_v(q, v, [-v, x - dv, x + dv, v + (1 if v > 0 else -1), 0], e, rnd))
    # E: which rule does the pattern show (2)
    q = ("Which rule does this pattern show?<br>2 × (" + M + "5) = " + M + "10<br>1 × (" + M + "5) = " + M + "5<br>"
         "0 × (" + M + "5) = 0<br>(" + M + "1) × (" + M + "5) = 5<br>(" + M + "2) × (" + M + "5) = 10")
    its.append(mcq(q, "A negative times a negative is positive.",
                   ["A negative times a negative is negative.", "A positive times a negative is positive.",
                    "Zero times a negative is negative."],
                   "The last two rows multiply two negatives and the products, 5 and 10, are positive. "
                   "So <b>a negative times a negative is positive</b>.", rnd))
    q = ("Which rule does this pattern show?<br>12 ÷ 3 = 4<br>6 ÷ 3 = 2<br>0 ÷ 3 = 0<br>"
         "(" + M + "6) ÷ 3 = " + M + "2<br>(" + M + "12) ÷ 3 = " + M + "4")
    its.append(mcq(q, "A negative divided by a positive is negative.",
                   ["A negative divided by a positive is positive.", "A positive divided by a positive is negative.",
                    "Zero divided by a positive is positive."],
                   "The last two rows divide a negative by a positive and the quotients, " + M + "2 and " + M + "4, "
                   "are negative. So <b>a negative divided by a positive is negative</b>.", rnd))
    return {"title": "Patterns that lead to the sign rules", "items": its}


# ============================================================ set 2: multiplying
def e_mul(a, b):
    v = a * b
    same = (a < 0) == (b < 0)
    return ("%d × %d = %d. The signs are %s, so the product is %s: %s × %s = <b>%s</b>."
            % (abs(a), abs(b), abs(v), "the same" if same else "different", sign_word(v), p(a), p(b), n(v)))


def e_many(fs):
    v = 1
    for x in fs:
        v *= x
    neg = sum(1 for x in fs if x < 0)
    return ("%s = %d. There %s %d negative factor%s (an %s number), so the product is %s: <b>%s</b>."
            % (" × ".join(str(abs(x)) for x in fs), abs(v), "is" if neg == 1 else "are", neg, "" if neg == 1 else "s",
               "odd" if neg % 2 else "even", sign_word(v), n(v)))


def set_multiply(rnd, P):
    its = []
    # two factors (6)
    for a, b in [(-6, -8), (-9, 7), (8, -7), (-12, -5), (-11, 9), (-4, -13)]:
        v = a * b
        its.append(mcq_v("%s × %s = ?" % (p(a), p(b)), v, [-v, a + b, -(a + b), a - b], e_mul(a, b), rnd))
    # larger numbers (4)
    for a, b in [(-15, -6), (25, -8), (-14, -12), (-32, 5)]:
        v = a * b
        its.append(mcq_v("%s × %s = ?" % (p(a), p(b)), v, [-v, a + b, -(a + b), v + (10 if v > 0 else -10)],
                         e_mul(a, b), rnd))
    # three and four factors (6)
    for fs in [(-2, -3, -4), (-5, 4, -3), (6, -1, -7), (-3, -3, -3), (-1, -2, -3, -4), (-2, 3, -2, -5)]:
        v = 1
        for x in fs:
            v *= x
        first2 = fs[0] * fs[1]
        cands = [-v, sum(fs), -sum(fs), first2 + sum(fs[2:])]
        its.append(mcq_v(" × ".join(p(x) if i else p(x) for i, x in enumerate(fs)) + " = ?", v, cands, e_many(fs), rnd))
    # clever grouping (2)
    for a, b, c in [(-25, 7, -4), (-5, -13, -2)]:
        v = a * b * c
        e = ("Group the friendly pair first: %s × %s = %s. Then %s × %s = <b>%s</b>."
             % (p(a), p(c), n(a * c), p(a * c), p(b), n(v)))
        its.append(mcq_v("%s × %s × %s = ?" % (p(a), p(b), p(c)), v, [-v, a * c + b, -(a * c + b), a + b + c], e, rnd))
    # which product is negative / positive (2)
    its.append(mcq("Which product is negative?", "(" + M + "2) × (" + M + "3) × (" + M + "5)",
                   ["(" + M + "2) × (" + M + "3) × 5", "(" + M + "2) × (" + M + "3) × (" + M + "5) × 0",
                    "(" + M + "2) × (" + M + "3) × (" + M + "5) × (" + M + "1)"],
                   "Three negative factors is an odd number, so (" + M + "2) × (" + M + "3) × (" + M + "5) = <b>" + M + "30</b>. "
                   "Two or four negative factors give 30, and any product with 0 is 0.", rnd))
    its.append(mcq("Which product is positive?", "(" + M + "1) × (" + M + "4) × (" + M + "6) × (" + M + "2)",
                   ["(" + M + "1) × 4 × 6 × 2", "(" + M + "1) × (" + M + "4) × (" + M + "6) × 2",
                    "1 × 4 × 6 × 0"],
                   "Four negative factors is an even number, so the product is positive: <b>48</b>. "
                   "One or three negative factors give " + M + "48, and a product with 0 is 0.", rnd))
    return {"title": "Multiplying integers", "items": its}


# ============================================================ set 3: dividing
def e_div(a, b):
    v = a // b
    same = (a < 0) == (b < 0)
    return ("%d ÷ %d = %d. The signs are %s, so the quotient is %s: %s ÷ %s = <b>%s</b>."
            % (abs(a), abs(b), abs(v), "the same" if same else "different", sign_word(v), p(a), p(b), n(v)))


def set_divide(rnd, P):
    its = []
    # basic (6)
    for a, b in [(-56, 7), (-48, -6), (63, -9), (-72, -8), (-81, 9), (54, -6)]:
        v = a // b
        assert a == v * b
        sg = 1 if v > 0 else -1
        its.append(mcq_v("%s ÷ %s = ?" % (p(a), p(b)), v, [-v, v + sg, -(v + sg), a + b], e_div(a, b), rnd))
    # larger (4)
    for a, b in [(-96, 8), (-144, -12), (150, -25), (-210, -15)]:
        v = a // b
        assert a == v * b
        sg = 1 if v > 0 else -1
        its.append(mcq_v("%s ÷ %s = ?" % (p(a), p(b)), v, [-v, v + sg, -(v + sg), a + b], e_div(a, b), rnd))
    # check with multiplication (3)
    for a, b in [(-36, 4), (45, -9), (-88, -11)]:
        v = a // b
        q = "Which multiplication checks that %s ÷ %s = %s?" % (p(a), p(b), n(v))
        e = "Multiply the quotient by the divisor to get back the dividend: <b>%s × %s = %s</b>." % (p(v), p(b), n(a))
        cands = ["%s × %s = %s" % (p(-v), p(b), n(-a)), "%s × %s = %s" % (p(v), p(-b), n(-a)),
                 "%s × %s = %s" % (p(a), p(b), n(a * b))]
        its.append(mcq(q, "%s × %s = %s" % (p(v), p(b), n(a)), cands, e, rnd))
    # missing factor or dividend (4)
    for kind, known, res in [("lf", -7, -56), ("rf", -9, 72), ("dvd", -6, 9), ("dvd", 4, -13)]:
        if kind == "lf":
            ans = res // known
            q = "□ × %s = %s. What number goes in the box?" % (p(known), n(res))
            e = ("Divide to find the missing factor: %s ÷ %s = %s. Check: %s × %s = %s. The box is <b>%s</b>."
                 % (p(res), p(known), n(ans), p(ans), p(known), n(res), n(ans)))
            cands = [-ans, res - known, res + known, res * known]
        elif kind == "rf":
            ans = res // known
            q = "%s × □ = %s. What number goes in the box?" % (p(known), n(res))
            e = ("Divide to find the missing factor: %s ÷ %s = %s. Check: %s × %s = %s. The box is <b>%s</b>."
                 % (p(res), p(known), n(ans), p(known), p(ans), n(res), n(ans)))
            cands = [-ans, res - known, res + known, res * known]
        else:
            ans = known * res
            q = "□ ÷ %s = %s. What number goes in the box?" % (p(known), n(res))
            e = ("Multiply to undo the division: %s × %s = %s. Check: %s ÷ %s = %s. The box is <b>%s</b>."
                 % (p(res), p(known), n(ans), p(ans), p(known), n(res), n(ans)))
            cands = [-ans, res + known, res - known, -(res - known)]
        its.append(mcq_v(q, ans, cands, e, rnd))
    # zero (1)
    its.append(mcq("0 ÷ (" + M + "8) = ?", ("0", F(0)), [(M + "8", F(-8)), ("8", F(8)), (M + "1", F(-1))],
                   "Zero divided by any non-zero number is 0, because (" + M + "8) × 0 = 0. So 0 ÷ (" + M + "8) = <b>0</b>.",
                   rnd))
    # two divisions left to right (2)
    for a, b, c in [(-120, -4, -5), (360, -6, -10)]:
        v = F(a, b) / c
        assert v.denominator == 1
        e = ("Work from left to right: %s ÷ %s = %s. Then %s ÷ %s = <b>%s</b>."
             % (p(a), p(b), n(F(a, b)), p(F(a, b)), p(c), n(v)))
        wrong_rl = F(a) / (F(b) / c) if F(b) / c != 0 and (F(a) / (F(b) / c)).denominator == 1 else None
        its.append(mcq_v("%s ÷ %s ÷ %s = ?" % (p(a), p(b), p(c)), v, [-v, F(a, b), -F(a, b), wrong_rl],
                         e, rnd))
    return {"title": "Dividing integers", "items": its}


# ============================================================ set 4: order of operations
def set_mixed(rnd, P):
    its = []
    # a + b × c (3)
    for a, b, c in [(-8, 3, -4), (7, -2, 6), (-9, -5, -3)]:
        v = a + b * c
        q = "%s + %s × %s = ?" % (n(a), p(b), p(c))
        e = "Multiply first: %s × %s = %s. Then %s + %s = <b>%s</b>." % (p(b), p(c), n(b * c), n(a), p(b * c), n(v))
        its.append(mcq_v(q, v, [(a + b) * c, a - b * c, -v, a + abs(b * c), b * c], e, rnd))
    # a − b ÷ c (3)
    for a, b, c in [(10, -16, 4), (-5, 24, -6), (-3, -27, -9)]:
        v = a - F(b, c)
        q = "%s − %s ÷ %s = ?" % (n(a), p(b), p(c))
        e = "Divide first: %s ÷ %s = %s. Then %s − %s = <b>%s</b>." % (p(b), p(c), n(F(b, c)), n(a), p(F(b, c)), n(v))
        its.append(mcq_v(q, v, [F(a - b, c), a + F(b, c), -v, a - abs(F(b, c)), F(b, c)], e, rnd))
    # (a + b) × c (3)
    for a, b, c in [(-11, 5, -3), (3, -8, 7), (-6, -2, -4)]:
        v = (a + b) * c
        q = "(%s + %s) × %s = ?" % (n(a), p(b), p(c))
        e = "Brackets first: %s + %s = %s. Then %s × %s = <b>%s</b>." % (n(a), p(b), n(a + b), p(a + b), p(c), n(v))
        its.append(mcq_v(q, v, [a + b * c, -v, (a - b) * c, a * c + b, a * c], e, rnd))
    # a × b + c × d (3)
    for a, b, c, d in [(-4, 6, -3, -5), (5, -7, 2, 4), (-8, -3, 6, -2)]:
        v = a * b + c * d
        q = "%s × %s + %s × %s = ?" % (n(a), p(b), p(c), p(d))
        e = ("Multiply first: %s × %s = %s and %s × %s = %s. Then %s + %s = <b>%s</b>."
             % (n(a), p(b), n(a * b), p(c), p(d), n(c * d), n(a * b), p(c * d), n(v)))
        its.append(mcq_v(q, v, [(a * b + c) * d, a * b - c * d, -v, a * b + abs(c * d), -(a * b) + c * d], e, rnd))
    # (a − b) ÷ c (2)
    for a, b, c in [(-14, -2, 2), (9, -15, -6)]:
        v = F(a - b, c)
        assert v.denominator == 1
        q = "(%s − %s) ÷ %s = ?" % (n(a), p(b), p(c))
        e = ("Brackets first: %s − %s = %s + %s = %s. Then %s ÷ %s = <b>%s</b>."
             % (n(a), p(b), n(a), p(-b), n(a - b), p(a - b), p(c), n(v)))
        its.append(mcq_v(q, v, [F(a + b, c), -v, a - F(b, c), F(a + b, -c), a - b + c, F(a, c) - b], e, rnd))
    # a × (b − c) (2)
    for a, b, c in [(-6, 2, 9), (3, -4, -10)]:
        v = a * (b - c)
        q = "%s × (%s − %s) = ?" % (n(a), n(b), p(c))
        e = ("Brackets first: %s − %s = %s. Then %s × %s = <b>%s</b>."
             % (n(b), p(c), n(b - c), n(a), p(b - c), n(v)))
        its.append(mcq_v(q, v, [a * b - c, a * (b + c), -v, a * b + c, a * b], e, rnd))
    # squares and cubes of negatives (2)
    q = "(" + M + "3)² − 4 × (" + M + "2) = ?"
    e = ("Square first: (" + M + "3)² = (" + M + "3) × (" + M + "3) = 9. Multiply: 4 × (" + M + "2) = " + M + "8. "
         "Then 9 − (" + M + "8) = 9 + 8 = <b>17</b>.")
    its.append(mcq_v(q, 17, [-1, 1, -10, -17], e, rnd))
    q = "(" + M + "2)³ + 5 × 3 = ?"
    e = ("(" + M + "2)³ = (" + M + "2) × (" + M + "2) × (" + M + "2) = " + M + "8 (three negative factors). "
         "Multiply: 5 × 3 = 15. Then " + M + "8 + 15 = <b>7</b>.")
    its.append(mcq_v(q, 7, [23, 9, -9, -23], e, rnd))
    # quotient of two expressions (2)
    for top, bot in [((-20, 4, "-"), (2, 8, "-")), ((5, -6, "x"), (-3, 2, "-"))]:
        ta, tb, to = top
        ba, bb, bo = bot
        tv = ta - tb if to == "-" else ta * tb
        bv = ba - bb
        v = F(tv, bv)
        assert v.denominator == 1
        ts = "%s − %s" % (n(ta), p(tb)) if to == "-" else "%s × %s" % (n(ta), p(tb))
        bs = "%s − %s" % (n(ba), p(bb))
        q = "(%s) ÷ (%s) = ?" % (ts, bs)
        e = ("Work out each bracket first: %s = %s and %s = %s. Then %s ÷ %s = <b>%s</b>."
             % (ts, n(tv), bs, n(bv), p(tv), p(bv), n(v)))
        alt_bot = ba + bb
        alt = F(tv, alt_bot) if alt_bot else None
        its.append(mcq_v(q, v, [-v, alt, -alt if alt is not None else None, tv + bv, tv - bv], e, rnd))
    return {"title": "Order of operations with integers", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd, P):
    its = []
    # 1-2: temperature change only
    for place, rate, hrs in [("in Thunder Bay", 2, 6), ("in Timmins", 3, 5)]:
        v = -rate * hrs
        q = ("After sunset, the temperature %s falls %s each hour. "
             "What is the total change in temperature after %d hours?" % (place, deg(rate), hrs))
        e = "A fall of %s each hour for %d hours: %d × %s = <b>%s</b>." % (deg(rate), hrs, hrs, p(-rate), deg(v))
        its.append(mcq_v(q, v, [-v, -(rate + hrs), v + rate, v - rate], e, rnd, fmt=deg))
    # 3-4: temperature with a start
    for place, start, t0, t1, rate, hrs in [("in Sudbury", 5, "6 p.m.", "11 p.m.", 2, 5),
                                            ("in Ottawa", -3, "9 p.m.", "1 a.m.", 3, 4)]:
        v = start - rate * hrs
        q = ("At %s, the temperature %s is %s. It falls %s each hour. What is the temperature at %s?"
             % (t0, place, deg(start), deg(rate), t1))
        e = ("From %s to %s is %d hours. The change is %d × %s = %s. Then %s + %s = <b>%s</b>."
             % (t0, t1, hrs, hrs, p(-rate), deg(-rate * hrs), n(start), p(-rate * hrs), deg(v)))
        its.append(mcq_v(q, v, [-rate * hrs, start + rate * hrs, -v, start - rate * (hrs - 1)], e, rnd, fmt=deg))
    # 5-7: sharing a debt
    for who, debt, k, what in [("Five friends", 750, 5, "a weekend cottage rental on Lake Muskoka"),
                               ("The six players on a basketball team", 270, 6, "a bus to a tournament in Kingston"),
                               ("Four cousins", 132, 4, "canoe rentals in Algonquin Park")]:
        v = F(-debt, k)
        q = ("%s owe %s together for %s, and they share the debt equally. "
             "Which integer shows each person’s share, in dollars?" % (who, "$" + n(debt), what))
        e = "A debt is negative: %s ÷ %d = <b>%s</b>. Each person owes $%d." % (p(-debt), k, n(v), debt // k)
        its.append(mcq_v(q, v, [-v, -debt * k, -(debt - k), debt - k], e, rnd))
    # 8-9: diver
    for rate, mins in [(3, 7), (4, 6)]:
        nm, he, his = P.next()
        v = -rate * mins
        q = ("%s is scuba diving near Tobermory in Georgian Bay. %s starts at the surface (0" % (nm, he.capitalize()) +
             NBSP + "m) and goes down %s each minute for %d minutes. Which integer shows %s position?"
             % (metres(rate), mins, his))
        e = ("Down is negative: %d × %s = <b>%s</b>, so %s is %s below the surface."
             % (mins, p(-rate), metres(v), he, metres(rate * mins)))
        its.append(mcq_v(q, v, [-v, -(rate + mins), v + rate, v - rate], e, rnd, fmt=metres))
    # 10-11: account payments
    for amt, wks, what in [(12, 9, "a music app"), (25, 6, "skating lessons")]:
        nm, he, his = P.next()
        v = -amt * wks
        q = ("%s pays $%d each month for %s from %s bank account. "
             "Which integer shows the change in %s balance after %d months, in dollars?" % (nm, amt, what, his, his, wks))
        e = "Paying out is negative: %d × %s = <b>%s</b>." % (wks, p(-amt), n(v))
        its.append(mcq_v(q, v, [-v, -(amt + wks), v + amt, amt - wks], e, rnd))
    # 12-13: rate from total change
    q = ("Overnight in North Bay, the temperature changed by %s in 7 hours. It fell by the same amount each hour. "
         "What was the change each hour?" % deg(-21))
    e = "Divide the total change by the hours: %s ÷ 7 = <b>%s</b> each hour." % (p(-21), deg(-3))
    its.append(mcq_v(q, -3, [3, -21 + 7, -21 - 7, -147], e, rnd, fmt=deg))
    q = ("During a dry August, the water level of a small lake near Kenora changed by %s in 8 weeks. "
         "It fell by the same amount each week. What was the change each week?" % cm(-32))
    e = "Divide the total change by the weeks: %s ÷ 8 = <b>%s</b> each week." % (p(-32), cm(-4))
    its.append(mcq_v(q, -4, [4, -32 + 8, -32 - 8, -256], e, rnd, fmt=cm))
    # 14-15: how many hours / days (positive answer)
    q = ("The water level in a reservoir falls 3" + NBSP + "cm each day. After how many days will the change be %s?" % cm(-27))
    e = "Each day the change is " + cm(-3) + ". " + p(-27) + " ÷ " + p(-3) + " = <b>9</b> days (same signs, so positive)."
    its.append(mcq(q, ("9 days", F(9)), [(M + "9 days", F(-9)), ("81 days", F(81)), ("24 days", F(24))], e, rnd))
    q = ("At midnight in Kapuskasing, the temperature is 0" + NBSP + "°C and falls 2" + NBSP +
         "°C each hour. After how many hours will it be %s?" % deg(-16))
    e = "Each hour the change is " + deg(-2) + ". " + p(-16) + " ÷ " + p(-2) + " = <b>8</b> hours (same signs, so positive)."
    its.append(mcq(q, ("8 hours", F(8)), [(M + "8 hours", F(-8)), ("32 hours", F(32)), ("14 hours", F(14))], e, rnd))
    # 16-17: contest scoring
    for right, wrong, plus, minus in [(7, 5, 4, 2), (11, 8, 3, 2)]:
        nm, he, his = P.next()
        v = right * plus + wrong * -minus
        q = ("In a math contest, each correct answer scores +%d and each wrong answer scores %s. "
             "%s gets %d correct and %d wrong. What is %s score?" % (plus, n(-minus), nm, right, wrong, his))
        e = ("%d × %d + %d × %s = %d + %s = <b>%s</b>."
             % (right, plus, wrong, p(-minus), right * plus, p(-wrong * minus), n(v)))
        its.append(mcq_v(q, v, [right * plus + wrong * minus, (right + wrong) * (plus - minus), -v,
                                right * plus - minus], e, rnd))
    # 18-19: mean of temperatures
    for place, temps in [("Kenora", [-12, -18, -7, -9, -14]), ("Kapuskasing", [-21, -16, -9, -15, -19])]:
        tot = sum(temps)
        v = F(tot, len(temps))
        assert v.denominator == 1
        med = sorted(temps)[2]
        q = ("The low temperatures in %s on five days in January were " % place +
             ", ".join(deg(t) for t in temps) + ". What was the mean low temperature?")
        e = "Add: %s. Divide by 5: %s ÷ 5 = <b>%s</b>." % (
            " + ".join(p(t) if i else n(t) for i, t in enumerate(temps)) + " = " + n(tot), p(tot), deg(v))
        its.append(mcq_v(q, v, [-v, tot, med, F(tot, 4)], e, rnd, fmt=deg))
    # 20: hockey plus-minus, two steps
    nm, he, his = P.next()
    q = ("In hockey, a player’s plus-minus goes up 1 when %s team scores while %s is on the ice and down 1 when the other "
         "team scores. %s has a plus-minus of %s in each of 3 games and +5 in the next game. "
         "What is %s total plus-minus for the 4 games?" % (his, he, nm, n(-2), his))
    e = "3 × %s + 5 = %s + 5 = <b>%s</b>." % (p(-2), n(-6), n(-1))
    its.append(mcq_v(q, -1, [-11, 1, -6, -3], e, rnd))
    return {"title": "Word problems: temperature, debts and more", "items": its}


# ============================================================ lesson
def body_html():
    j = jumps_svg(3, 4, jl_label(3, 4), gap=20)
    pat = table(["Multiplication", "Product"], [
        ["2 × (" + M + "4)", M + "8"], ["1 × (" + M + "4)", M + "4"],
        ["0 × (" + M + "4)", "0"], ["(" + M + "1) × (" + M + "4)", "4"], ["(" + M + "2) × (" + M + "4)", "8"]])
    return (
        "<h2>Multiplying is repeated addition</h2>"
        "<p>3 × (" + M + "4) means 3 groups of " + M + "4: (" + M + "4) + (" + M + "4) + (" + M + "4) = " + M + "12. "
        "On a number line, start at 0 and make 3 jumps of " + M + "4.</p>"
        "<figure class='sn-fig'>" + j +
        "<figcaption>3 jumps of " + M + "4 end at " + M + "12, so 3 × (" + M + "4) = " + M + "12. "
        "Order does not matter: (" + M + "4) × 3 = " + M + "12 too.</figcaption></figure>"
        "<h2>A pattern shows why (" + M + ") × (" + M + ") is positive</h2>"
        "<p>Each time the first factor goes down by 1, the product goes <b>up</b> by 4. "
        "Continue past 0 and the products become positive.</p>" + pat +
        "<h2>The sign rules</h2>"
        "<p>Multiply or divide the numbers without their signs, then choose the sign. "
        "<b>Same signs give a positive answer. Different signs give a negative answer.</b> "
        "The same rules work for × and ÷.</p>" +
        table(["Signs", "Multiply", "Divide"], [
            ["positive and positive", "3 × 4 = 12", "12 ÷ 3 = 4"],
            ["negative and negative", "(" + M + "3) × (" + M + "4) = 12", "(" + M + "12) ÷ (" + M + "3) = 4"],
            ["positive and negative", "3 × (" + M + "4) = " + M + "12", "12 ÷ (" + M + "3) = " + M + "4"],
            ["negative and positive", "(" + M + "3) × 4 = " + M + "12", "(" + M + "12) ÷ 3 = " + M + "4"],
        ]) +
        "<p>With three or more factors, count the negative factors. An even count gives a positive product; "
        "an odd count gives a negative product.</p>" +
        ex("Example 1", "(" + M + "2) × 5 × (" + M + "3) × (" + M + "1)",
           "2 × 5 × 3 × 1 = 30. There are 3 negative factors (odd), so the product is negative.", M + "30") +
        ex("Example 2", "(" + M + "72) ÷ 8",
           "72 ÷ 8 = 9. The signs are different, so the quotient is negative. Check: 8 × (" + M + "9) = " + M + "72.",
           M + "9") +
        "<h2>Order of operations</h2>"
        "<p>Brackets first, then exponents, then × and ÷ from left to right, then + and − from left to right. "
        "Write negative numbers in brackets so each sign is easy to see.</p>" +
        ex("Example 3", "(" + M + "4)² − 3 × (" + M + "2)",
           "(" + M + "4)² = (" + M + "4) × (" + M + "4) = 16. Then 3 × (" + M + "2) = " + M + "6. "
           "Last, 16 − (" + M + "6) = 16 + 6 = 22.", "22") +
        ex("Example 4", "In Barrie, the temperature is 4" + NBSP + "°C at 7 p.m. and falls 3" + NBSP + "°C each hour. "
           "What is it at 11 p.m.?",
           "That is 4 hours. The change is 4 × (" + M + "3) = " + M + "12. Then 4 + (" + M + "12) = " + M + "8.", deg(-8)) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["(" + M + "3) × (" + M + "4) = " + M + "12", "Same signs give a positive answer: 12"],
            ["(" + M + "12) ÷ 3 = 4", "Different signs give a negative answer: " + M + "4"],
            ["Adding instead of multiplying: 3 × (" + M + "4) = " + M + "1", "3 × (" + M + "4) is 3 groups of " + M + "4: " + M + "12"],
            ["(" + M + "3)² = " + M + "9", "(" + M + "3)² = (" + M + "3) × (" + M + "3) = 9"],
            ["Working left to right: " + M + "8 + 3 × (" + M + "4) = 20", "Multiply before you add: " + M + "8 + (" + M + "12) = " + M + "20"],
            ["Forgetting the starting temperature", "Add the change to the start: 4 + (" + M + "12) = " + M + "8"],
        ])
    )


FAQ = [
    {"q": "How do you multiply and divide integers in Grade 8?",
     "a": "Multiply or divide the numbers without their signs, then choose the sign: same signs give a positive answer and different signs give a negative answer. So (−3) × (−4) = 12 and (−12) ÷ 3 = −4."},
    {"q": "Why is a negative times a negative a positive?",
     "a": "Look at the pattern 2 × (−4) = −8, 1 × (−4) = −4, 0 × (−4) = 0. Each step the product goes up by 4, so (−1) × (−4) = 4 and (−2) × (−4) = 8."},
    {"q": "Which Ontario Grade 8 expectation covers multiplying and dividing integers?",
     "a": "Expectation B2.7 in the Number strand of the 2020 Ontario math curriculum: multiply and divide integers, using appropriate strategies, in various contexts."},
    {"q": "Do Grade 8 students in Ontario write EQAO?",
     "a": "No. Ontario students write EQAO assessments in Grades 3 and 6, and the next math assessment is in Grade 9. Integer skills from Grade 8 are used all through Grade 9 math."},
]


def gen_unit():
    rnd = random.Random(48805)
    P = People(rnd)
    sets = [set_patterns(rnd, P), set_multiply(rnd, P), set_divide(rnd, P), set_mixed(rnd, P), set_words(rnd, P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-8", "slug": "multiplying-and-dividing-integers", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Multiplying and Dividing Integers",
        "seo_title": "Grade 8 Multiplying and Dividing Integers Worksheets: Free Math Practice with Answer Key (Ontario Curriculum)",
        "short_title": "Multiplying and dividing integers",
        "domain": "Number",
        "standard_code": "Grade 8: B2.7",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Multiply and divide integers, using appropriate strategies, in various contexts",
        "meta_desc": "Free Grade 8 math worksheets on multiplying and dividing integers for the Ontario curriculum: patterns that explain the sign rules, products of several integers, division checked by multiplication, order of operations, and word problems with falling temperatures and shared debts. 100 questions with an answer key.",
        "key_big": "Same signs give a positive answer; different signs give a negative answer. (−3) × (−4) = 12 and (−12) ÷ 3 = −4.",
        "key_sub": "With three or more factors, count the negatives: an even count gives a positive product, an odd count a negative one. Check a division with multiplication: (−12) ÷ 3 = −4 because 3 × (−4) = −12.",
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
