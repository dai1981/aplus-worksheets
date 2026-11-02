# -*- coding: utf-8 -*-
"""
AU Year 4 Maths (Australian Curriculum v9.0, AC9M4N02): odd and even numbers.
  python3 tools/gen_au_maths_y4_odd_even.py
Every count, sum, product and odd/even label is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#e8f3ec"
RED = "#c0392b"
GOLD = "#e3a81b"
INK = "#2b2b2b"
GREY = "#9a948c"
FONT = "Arial, Helvetica, sans-serif"
X = "×"
M = "−"
NB = " "
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]


# ------------------------------------------------------------ helpers
def f(n):
    """Australian style: 4 digits plain, 5+ digits grouped with a no-break space."""
    s = str(n)
    if len(s) <= 4:
        return s
    out = ""
    while len(s) > 3:
        out = NB + s[-3:] + out
        s = s[:-3]
    return s + out


def par(n):
    return "even" if n % 2 == 0 else "odd"


def cap(s):
    return s[0].upper() + s[1:]


def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
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
    """Spread the correct answers evenly over the 4 positions in every set."""
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


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK, bold=True):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def calc(expr):
    assert re.fullmatch(r"[0-9 +×−]+", expr), expr
    return eval(expr.replace(X, "*").replace(M, "-"))


# ------------------------------------------------------------ figures
PITCH = 28


def counter(cx, cy, col):
    return "<circle cx='%.1f' cy='%.1f' r='10' fill='%s' stroke='%s' stroke-width='1.5'/>" % (cx, cy, col, INK)


def pairs_body(x0, y0, n, col, outline=False, gx=0):
    """n counters in columns of 2 (pairs); a left-over counter sits alone at the top of the last column."""
    s = []
    cols = (n + 1) // 2
    CP = PITCH + gx
    if outline:
        for c in range(n // 2):
            s.append("<rect x='%.1f' y='%d' width='%d' height='%d' rx='8' fill='none' stroke='%s' "
                     "stroke-width='1.5' stroke-dasharray='4 3'/>"
                     % (x0 + c * CP + gx / 2 - 1, y0 - 2, PITCH + 2, 2 * PITCH + 4, GREEN))
        if n % 2:
            s.append("<circle cx='%.1f' cy='%d' r='13' fill='none' stroke='%s' stroke-width='2'/>"
                     % (x0 + (cols - 1) * CP + gx / 2 + PITCH / 2, y0 + PITCH // 2, RED))
    for i in range(n):
        c, r = divmod(i, 2)
        s.append(counter(x0 + c * CP + gx / 2 + PITCH / 2, y0 + r * PITCH + PITCH / 2, col))
    return "".join(s), cols * CP, 2 * PITCH


def pairs_svg(n):
    o = 6
    body, w, h = pairs_body(o, o, n, GREEN)
    return svg_wrap(w + 2 * o, h + 2 * o, body, "%d counters in pairs" % n)


def two_groups_svg(a, b):
    o, gap = 6, 40
    ba, wa, h = pairs_body(o, o, a, RED)
    bb, wb, _ = pairs_body(o + wa + gap, o, b, GREEN)
    plus = text(o + wa + gap / 2, o + h / 2 + 9, "+", 26)
    return svg_wrap(wa + wb + gap + 2 * o, h + 2 * o, ba + plus + bb, "%d red counters and %d green counters" % (a, b))


def lesson_pairs_svg(a, b):
    o, gap, lab = 10, 60, 26
    ba, wa, h = pairs_body(o, o, a, GREEN, outline=True, gx=10)
    bb, wb, _ = pairs_body(o + wa + gap, o, b, GREEN, outline=True, gx=10)
    W = wa + wb + gap + 2 * o
    t1 = text(o + wa / 2, o + h + 22, "%d: %s" % (a, par(a)), 16, col=GREEN if a % 2 == 0 else RED)
    t2 = text(o + wa + gap + wb / 2, o + h + 22, "%d: %s" % (b, par(b)), 16, col=GREEN if b % 2 == 0 else RED)
    return svg_wrap(W, h + 2 * o + lab, ba + bb + t1 + t2,
                    "%d counters in pairs, none left over, and %d counters in pairs with 1 left over" % (a, b))


def lesson_sum_svg(a, b):
    """odd + odd: the two left-over counters join to make a new pair (lesson only)."""
    o, gap = 10, 44
    ba, wa, h = pairs_body(o, o + 4, a, RED, outline=True, gx=6)
    bb, wb, _ = pairs_body(o + wa + gap, o + 4, b, GREEN, outline=True, gx=6)
    plus = text(o + wa + gap / 2, o + 4 + h / 2 + 9, "+", 26)
    cap_t = text((o + wa + gap + wb + o) / 2, o + h + 34, "%d + %d = %d: even" % (a, b, a + b), 16, col=GREEN)
    return svg_wrap(wa + wb + gap + 2 * o, h + 2 * o + 32, ba + plus + bb + cap_t,
                    "%d counters and %d counters; each has 1 left over" % (a, b))


def numline_svg(lo, hi, label_every=1, dots=(), jumps=(), arrow=None, unit=34):
    """Number line from lo to hi. dots: green dots on numbers; jumps: list of (a, b) arcs; arrow: number marked with an arrow."""
    pad = 22
    W = (hi - lo) * unit + 2 * pad
    top = 34 if jumps or arrow is not None else 14
    yl = top + 10
    H = yl + 34
    X0 = lambda v: pad + (v - lo) * unit
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (pad - 12, yl, W - pad + 12, yl, INK)]
    for v in range(lo, hi + 1):
        big = (v - lo) % label_every == 0
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
                 % (X0(v), yl - (8 if big else 5), X0(v), yl + (8 if big else 5), INK))
        if big:
            s.append(text(X0(v), yl + 26, str(v), 14, bold=False))
    for a, b in jumps:
        xa, xb = X0(a), X0(b)
        s.append("<path d='M %d %d Q %.1f %d %d %d' fill='none' stroke='%s' stroke-width='2'/>"
                 % (xa, yl - 4, (xa + xb) / 2, yl - 40, xb, yl - 4, RED))
        s.append("<polygon points='%d,%d %d,%d %d,%d' fill='%s'/>" % (xb, yl - 3, xb - 7, yl - 10, xb + 1, yl - 12, RED))
    for v in dots:
        s.append("<circle cx='%d' cy='%d' r='7' fill='%s'/>" % (X0(v), yl, GREEN))
    if arrow is not None:
        xa = X0(arrow)
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (xa, 4, xa, yl - 12, RED))
        s.append("<polygon points='%d,%d %d,%d %d,%d' fill='%s'/>" % (xa, yl - 4, xa - 7, yl - 15, xa + 7, yl - 15, RED))
    lab = "number line from %d to %d" % (lo, hi)
    return svg_wrap(W, H, "".join(s), lab)


# ------------------------------------------------------------ shared text
RULE_CHOICES = ["Always even", "Always odd", "Sometimes odd, sometimes even", "It depends on the size"]


def parity_of(op, a, b):
    return {"+": a + b, M: a - b, X: a * b}[op] % 2


def first_digit_guess(op, a, b):
    """What a student gets by using the first digits instead of the ones digits."""
    fa, fb = int(str(a)[0]), int(str(b)[0])
    return {"+": fa + fb, M: fa - fb, X: fa * fb}[op] % 2


def reason(op, pa, pb):
    """The parity rule in words, e.g. 'odd + odd = even'."""
    a, b = (1 if pa == "odd" else 2), (1 if pb == "odd" else 2)
    if op == M:
        a, b = a + 4, b
    return "%s %s %s = %s" % (pa, op, pb, par({"+": a + b, M: a - b, X: a * b}[op]))


# ============================================================ set 1: odd or even?
def set_odd_even(rnd):
    its = []
    for n in (13, 16, 19, 22):
        h = n // 2
        if n % 2:
            e = "Make pairs: %d pairs and 1 counter left over. One left over means <b>odd</b>." % h
        else:
            e = "Make pairs: %d pairs and none left over. Every counter has a partner, so %d is <b>even</b>." % (h, n)
        alt = "even" if n % 2 else "odd"
        its.append(mcq(fig(pairs_svg(n)) + "How many counters are there? Is the number odd or even?",
                       "%d: %s" % (n, par(n)),
                       ["%d: %s" % (n, alt), "%d: %s" % (n + 1, par(n + 1)), "%d: %s" % (n - 1, par(n - 1))], e))

    # reasons: right digit vs first digit
    for n in (4537, 3718, 6290, 8005):
        o, fd, nd = n % 10, int(str(n)[0]), len(str(n))
        assert fd % 2 != o % 2 or o == 0
        right = "%s: ends in %d" % (cap(par(n)), o)
        wrong = ["%s: starts with %d" % (cap(par(fd)), fd),
                 "%s: ends in %d" % (cap("odd" if n % 2 == 0 else "even"), o)]
        if o == 0:
            wrong.append("Neither: ends in 0")
        else:
            wrong.append("%s: has %d digits" % (cap(par(nd)), nd))
        e = ("Only the ones digit matters. %s ends in %d, and %d is %s, so %s is <b>%s</b>. "
             "The first digit, %d, does not tell you." % (f(n), o, o, par(o), f(n), par(n), fd))
        its.append(mcq("Is %s odd or even?" % f(n), right, wrong, e))

    its.append(mcq("Is 0 odd or even?", "Even", ["Odd", "Neither odd nor even", "Both odd and even"],
                   "0 is <b>even</b>. Counting by 2s starts at 0: 0, 2, 4, 6. With 0 objects nothing is left over, "
                   "and 10, 20 and 300 are even because they end in 0."))

    for want, right, wrong in [("even", 3576, [4567, 2681, 8423]),
                               ("even", 1390, [6205, 4871, 2013]),
                               ("even", 5034, [8045, 6123, 4509]),
                               ("odd", 2469, [1358, 3570, 5792]),
                               ("odd", 6801, [7310, 9554, 5236]),
                               ("odd", 4085, [3104, 5216, 1478])]:
        assert par(right) == want and all(par(w) != want for w in wrong)
        assert any(par(int(str(w)[0])) == want for w in wrong)
        e = ("Look at the ones digits only: %s. <b>%s</b> ends in %d, so it is %s. "
             "The first digit does not matter." % (", ".join(str(v % 10) for v in [right] + wrong),
                                                   f(right), right % 10, want))
        its.append(mcq("Which number is <b>%s</b>?" % want, f(right), [f(w) for w in wrong], e))

    for nums in ([34, 107, 250, 999, 1468], [86, 405, 1230, 777, 52]):
        k = sum(1 for v in nums if v % 2 == 0)
        ev = [str(v) for v in nums if v % 2 == 0]
        e = ("The even numbers end in 0, 2, 4, 6 or 8: %s. That is <b>%d</b>. "
             "Remember that a number ending in 0 is even." % (", ".join(ev), k))
        zero_miss = k - sum(1 for v in nums if v % 10 == 0)
        its.append(mcq("How many of these numbers are even?<br>%s" % ", ".join(f(v) for v in nums), k,
                       [zero_miss, k + 1, len(nums) - k, k - 1, k + 2], e))

    lists = [("odd", "13, 35, 57, 79", ["31, 52, 73, 94", "15, 25, 30, 45", "11, 22, 33, 44"]),
             ("even", "12, 30, 54, 76", ["21, 43, 65, 87", "40, 51, 60, 70", "20, 42, 63, 84"])]
    for want, right, wrong in lists:
        assert all(par(int(v)) == want for v in right.split(", "))
        assert all(any(par(int(v)) != want for v in w.split(", ")) for w in wrong)
        e = ("Check the ones digit of every number. In <b>%s</b> they are all %s. "
             "%s looks right if you read the first digits, but the ones digits are %s."
             % (right, want, wrong[0], ", ".join(v[-1] for v in wrong[0].split(", "))))
        its.append(mcq("Which list has <b>only %s</b> numbers?" % want, right, wrong, e))

    its.append(mcq("Which digit tells you if 5274 is odd or even?", "4 (the ones)",
                   ["5 (the thousands)", "2 (the hundreds)", "7 (the tens)"],
                   "Only the <b>ones digit</b> decides. 5274 ends in 4, so it is even. "
                   "Every ten, hundred and thousand can be split into pairs, so those digits never leave one over."))
    assert len(its) == 20, len(its)
    return {"title": "Odd or even? Look at the ones digit", "items": its}


# ============================================================ set 2: rules for + − ×
def set_rules(rnd):
    its = []
    why = {
        ("odd", "+", "odd"): "Each odd number has 1 left over. The two left-overs make a new pair, so nothing is left: "
                             "always <b>even</b>. Example: 3 + 5 = 8.",
        ("even", "+", "even"): "Both numbers are all pairs, so the total is all pairs: always <b>even</b>. Example: 4 + 6 = 10.",
        ("odd", "+", "even"): "The even number is all pairs. The odd number still has 1 left over, "
                              "so the total is always <b>odd</b>. Example: 7 + 4 = 11.",
        ("odd", X, "odd"): "3 %s 5 is 3 groups of 5. Two of the groups make 10, which is even. One group of 5 is left, "
                           "and even + odd = odd. So the answer is always <b>odd</b>: 3 %s 5 = 15." % (X, X),
        ("even", X, "odd"): "An even number of equal groups can be paired group with group, "
                            "so the answer is always <b>even</b>. Example: 4 %s 3 = 12." % X,
        ("even", X, "even"): "Groups of an even number are all pairs, so the answer is always <b>even</b>. "
                             "Example: 4 %s 6 = 24." % X,
        ("odd", M, "odd"): "Taking away an odd number takes away the 1 left over too, "
                           "so only pairs are left: always <b>even</b>. Example: 9 %s 3 = 6." % M,
        ("even", M, "odd"): "Taking an odd number from all pairs breaks one pair and leaves 1 over: "
                            "always <b>odd</b>. Example: 10 %s 3 = 7." % M,
    }
    for (pa, op, pb), e in why.items():
        ans = reason(op, pa, pb).split(" = ")[1]
        right = "Always " + ans
        wrong = [c for c in RULE_CHOICES if c != right]
        # check the rule on many real pairs
        A = [n for n in range(1, 60) if par(n) == pa]
        B = [n for n in range(1, 60) if par(n) == pb]
        assert all(par({"+": a + b, M: a - b, X: a * b}[op]) == ans for a in A for b in B if a - b >= 0 or op != M)
        its.append(mcq("An %s number %s an %s number. The answer is …" % (pa, op, pb), right, wrong, e))

    for a, b in [(7, 5), (6, 9), (9, 9)]:
        t = a + b
        e = ("Red: %d is %s. Green: %d is %s. %s, so %d + %d = %d is <b>%s</b>."
             % (a, par(a), b, par(b), cap(reason("+", par(a), par(b))), a, b, t, par(t)))
        if a % 2 and b % 2:
            e += " The two left-over counters make a new pair."
        alt = "odd" if t % 2 == 0 else "even"
        its.append(mcq(fig(two_groups_svg(a, b)) + "How many counters altogether? Is the total odd or even?",
                       "%d: %s" % (t, par(t)),
                       ["%d: %s" % (t, alt), "%d: %s" % (t - 1, par(t - 1)), "%d: %s" % (t + 1, par(t + 1))], e))

    def sentence_q(ask, right, wrong, e):
        def ok(s):
            lhs, p = s.rsplit(" is ", 1)
            return par(calc(lhs)) == p
        assert ok(right) and not any(ok(w) for w in wrong), (right, wrong)
        its.append(mcq(ask, right, wrong, e))

    sentence_q("Which is true?", "7 + 9 is even", ["3 %s 5 is even" % X, "8 + 5 is even", "9 %s 3 is odd" % M],
               "<b>7 + 9 = 16</b>, and odd + odd is even. 3 %s 5 = 15 is odd, 8 + 5 = 13 is odd "
               "and 9 %s 3 = 6 is even." % (X, M))
    sentence_q("Which is true?", "6 %s 7 is even" % X, ["5 + 6 is even", "9 %s 7 is even" % X, "8 %s 4 is odd" % M],
               "<b>6 %s 7 = 42</b>, and even %s odd is even. 5 + 6 = 11 is odd, 9 %s 7 = 63 is odd "
               "and 8 %s 4 = 4 is even." % (X, X, X, M))

    e = ("Leo needs two odd numbers whose total is even. <b>5 + 7 = 12</b> does it. "
         "4 + 6 uses two even numbers, and 3 + 4 and 2 + 5 use one odd and one even.")
    its.append(mcq("Leo says odd + odd is always odd. Which sum shows he is wrong?", "5 + 7 = 12",
                   ["4 + 6 = 10", "3 + 4 = 7", "2 + 5 = 7"], e))
    assert 5 + 7 == 12 and 4 + 6 == 10 and 3 + 4 == 7 and 2 + 5 == 7

    its.append(mcq("7 + ? is even. Which number could go in the box?", 9, [4, 6, 10],
                   "7 is odd. Odd + odd is even, so the missing number must be odd. Only <b>9</b> is odd: 7 + 9 = 16."))
    assert (7 + 9) % 2 == 0 and all((7 + v) % 2 for v in (4, 6, 10))
    its.append(mcq("3 %s ? is odd. Which number could go in the box?" % X, 5, [2, 4, 6],
                   "Odd %s odd is odd, but odd %s even is even. So the missing number must be odd: "
                   "3 %s <b>5</b> = 15." % (X, X, X)))
    assert (3 * 5) % 2 == 1 and all((3 * v) % 2 == 0 for v in (2, 4, 6))

    def pick_q(ask, want, right, wrong, rule):
        assert par(calc(right)) == want and all(par(calc(w)) != want for w in wrong), (right, wrong)
        e = "%s, so <b>%s = %d</b> is %s. The others are %s." % (
            cap(rule), right, calc(right), want, ", ".join("%s = %d" % (w, calc(w)) for w in wrong))
        its.append(mcq(ask, right, wrong, e))

    pick_q("Which product is <b>even</b>?", "even", "4 %s 7" % X, ["3 %s 5" % X, "7 %s 9" % X, "5 %s 1" % X],
           "even %s odd = even" % X)
    pick_q("Which sum is <b>odd</b>?", "odd", "8 + 7", ["5 + 9", "6 + 4", "3 + 3"], "even + odd = odd")
    pick_q("Which sum is <b>even</b>?", "even", "9 + 13", ["8 + 13", "6 + 11", "10 + 7"], "odd + odd = even")
    pick_q("Which difference is <b>even</b>?", "even", "15 %s 7" % M, ["12 %s 5" % M, "9 %s 4" % M, "10 %s 3" % M],
           "odd %s odd = even" % M)
    assert len(its) == 20, len(its)
    return {"title": "Odd and even rules for +, − and ×", "items": its}


# ============================================================ set 3: predict without calculating
def set_predict(rnd):
    its = []
    for op, a, b in [("+", 347, 289), ("+", 562, 175), ("+", 2148, 3576), (M, 835, 418),
                     (X, 23, 45), (X, 37, 16), (X, 125, 32)]:
        val = calc("%d %s %d" % (a, op, b))
        p = par(val)
        pa, pb = par(a), par(b)
        g = par(first_digit_guess(op, a, b))
        assert g != p, (a, op, b)
        fa, fb = str(a)[0], str(b)[0]
        alt = "odd" if p == "even" else "even"
        right = "%s: %s" % (cap(p), reason(op, pa, pb))
        wrong = ["%s: %s %s %s is %s" % (cap(g), fa, op, fb, g),
                 "%s: %s %s %s = %s" % (cap(alt), pa, op, pb, alt),
                 "%s: %d is %s" % (cap(pa), a, pa) if pa != p else
                 ("%s: %d is %s" % (cap(pb), b, pb) if pb != p else "Can’t tell without working it out")]
        e = ("Look at the ones digits: %d is %s and %d is %s. %s, so the answer is <b>%s</b>. "
             "(Check: %s %s %s = %s.) The first digits do not decide." %
             (a % 10, pa, b % 10, pb, cap(reason(op, pa, pb)), p, f(a), op, f(b), f(val)))
        its.append(mcq("Without working it out, is %s %s %s odd or even?" % (f(a), op, f(b)), right, wrong, e))

    for op, a, b in [("+", 458, 263), (X, 6, 47), (M, 503, 168), (X, 5, 63)]:
        val = calc("%d %s %d" % (a, op, b))
        wrong = [val - 1, val + 1, val + 3]
        assert all(par(w) != par(val) for w in wrong)
        e = ("%s, so the answer must be %s. Only <b>%d</b> is %s. (%d %s %d = %d.)"
             % (cap(reason(op, par(a), par(b))), par(val), val, par(val), a, op, b, val))
        its.append(mcq("Which of these could be the answer to %d %s %d?" % (a, op, b), val, wrong, e))

    its.append(mcq("Ruby worked out 458 + 263 = 720. How can you tell at once that it is wrong?",
                   "Even + odd is odd, but 720 is even",
                   ["Odd + odd is odd, but 720 is even", "4 + 2 is even, so it must be odd", "720 ends in 0, so it is odd"],
                   "458 ends in 8 (even) and 263 ends in 3 (odd). <b>Even + odd is odd</b>, but 720 ends in 0, so it is even. "
                   "The right answer is 721."))
    assert 458 + 263 == 721
    its.append(mcq("Kai worked out 4 %s 237 = 949. How can you tell at once that it is wrong?" % X,
                   "4 %s any number is even, but 949 is odd" % X,
                   ["237 is odd, so the answer must be even too", "949 is even because 4 is even",
                    "Odd %s odd is even, but 949 is odd" % X],
                   "4 is even, and even %s anything is even. <b>949 ends in 9, so it is odd</b>. "
                   "The right answer is 948." % X))
    assert 4 * 237 == 948

    def pick(ask, want, right, wrong):
        assert par(calc(right)) == want and all(par(calc(w)) != want for w in wrong), (right, wrong)
        ones = []
        for w in [right] + wrong:
            ones.append("%s ends in %s" % (w, "…"))
        e = ("Use only the ones digits. In <b>%s</b> they are %s, which gives an %s answer (%s). "
             "Check: %s = %s." % (right, " and ".join(str(int(t) % 10) for t in re.findall(r"\d+", right)), want,
                                  reason(re.search(r"[+×−]", right).group(),
                                         *[par(int(t)) for t in re.findall(r"\d+", right)]),
                                  right, f(calc(right))))
        its.append(mcq(ask, right, wrong, e))

    pick("Which sum is <b>even</b>? Do not work them out.", "even", "235 + 417", ["236 + 417", "235 + 418", "130 + 407"])
    pick("Which sum is <b>odd</b>? Do not work them out.", "odd", "624 + 381", ["623 + 381", "624 + 380", "511 + 703"])
    pick("Which product is <b>odd</b>? Do not work them out.", "odd", "23 %s 45" % X,
         ["24 %s 35" % X, "36 %s 17" % X, "47 %s 12" % X])
    pick("Which difference is <b>odd</b>? Do not work them out.", "odd", "652 %s 317" % M,
         ["651 %s 317" % M, "652 %s 318" % M, "543 %s 321" % M])

    its.append(mcq("Without working it out, is 2 %s 4651 odd or even?" % X, "Even: 2 %s any number" % X,
                   ["Odd: 4651 is odd", "Odd: 2 %s 4 is even" % X, "Odd: odd %s even = odd" % X],
                   "Doubling a number always gives pairs. 2 %s anything is <b>even</b>. Check: 2 %s 4651 = 9302."
                   % (X, X)))
    assert 2 * 4651 == 9302
    its.append(mcq("Is 13 + 25 + 37 odd or even?", "Odd", ["Even", "Neither", "It depends on the order"],
                   "13 + 25 is odd + odd = even. Then even + 37 is even + odd = <b>odd</b>. "
                   "Three odd numbers always add to an odd number. Check: 13 + 25 + 37 = 75."))
    assert 13 + 25 + 37 == 75
    its.append(mcq("Is 5 + 5 + 5 + 5 + 5 + 5 odd or even?", "Even", ["Odd", "Neither", "It depends on the order"],
                   "There are six 5s. The odd numbers pair up: 5 + 5 is even, three times. "
                   "Even + even + even is <b>even</b>. Check: 6 %s 5 = 30." % X))
    assert 6 * 5 == 30
    assert len(its) == 20, len(its)
    return {"title": "Predict odd or even without calculating", "items": its}


# ============================================================ set 4: patterns and number lines
def set_patterns(rnd):
    its = []
    # number lines
    its.append(mcq(fig(numline_svg(14, 26, dots=(16, 18, 20, 22))) +
                   "The dots are on every second number. Which number gets the next dot?", 24, [23, 26, 25],
                   "The dots are on 16, 18, 20, 22: even numbers, going up by 2. 22 + 2 = <b>24</b>. "
                   "23 is the next number, but it is odd."))
    jm = [(37, 39), (39, 41), (41, 43)]
    its.append(mcq(fig(numline_svg(36, 48, jumps=jm)) +
                   "A frog starts at 37 and jumps 2 each time. Keep jumping. Which number will it land on?",
                   47, [44, 46, 48],
                   "37 is odd. Adding 2 keeps an odd number odd, so the frog lands only on odd numbers: "
                   "37, 39, 41, 43, 45, <b>47</b>. 44, 46 and 48 are even."))
    its.append(mcq(fig(numline_svg(120, 132, label_every=5, arrow=127)) +
                   "What number is the arrow pointing to? Is it odd or even?", "127: odd",
                   ["127: even", "126: even", "128: even"],
                   "Count on from 125: 126, 127. The arrow is at 127. It ends in 7, so it is <b>odd</b>."))
    its.append(mcq(fig(numline_svg(240, 252, label_every=2, dots=(243, 245, 247, 249))) +
                   "The dots show a pattern. What kind of numbers are they, and which comes next?",
                   "Odd: 251", ["Even: 250", "Odd: 250", "Even: 251"],
                   "243, 245, 247, 249 end in 3, 5, 7, 9: they are odd and go up by 2. 249 + 2 = <b>251</b>, "
                   "which is odd too."))

    for q, ans, wrong, e in [
        ("Count by 2s. What is missing?<br>4996, 4998, ?, 5002", 5000, [4999, 5001, 4900],
         "4998 + 2 = <b>5000</b>. Then 5000 + 2 = 5002. 4999 counts by 1s."),
        ("Count back by 2s. What comes next?<br>103, 101, 99, ?", 97, [98, 100, 95],
         "Each number is 2 less: 99 %s 2 = <b>97</b>. Counting back by 2s from an odd number gives only odd numbers." % M),
        ("What is missing?<br>85, 87, ?, 91, 93", 89, [88, 90, 86],
         "The numbers go up by 2: 87 + 2 = <b>89</b>, then 89 + 2 = 91. They are all odd."),
        ("What is the next odd number after 1399?", 1401, [1400, 1402, 1501],
         "1399 + 1 = 1400, which is even. The next odd number is 1399 + 2 = <b>1401</b>."),
        ("What is the even number just before 10%s000?" % NB, 9998, [9999, f(10002), 9990],
         "10%s000 %s 1 = 9999, which is odd. The even number before it is 10%s000 %s 2 = <b>9998</b>."
         % (NB, M, NB, M)),
    ]:
        its.append(mcq(q, f(ans), [str(w) for w in wrong], e))
    assert 10000 - 2 == 9998 and 1399 + 2 == 1401

    ev = [n for n in range(31, 42) if n % 2 == 0]
    its.append(mcq("How many even numbers are there from 31 to 41?", len(ev), [6, 10, 11],
                   "The even numbers are %s. That is <b>%d</b>. 31 and 41 are odd, so they do not count."
                   % (", ".join(map(str, ev)), len(ev))))
    od = [n for n in range(1, 21) if n % 2]
    its.append(mcq("How many odd numbers are there from 1 to 20?", len(od), [9, 11, 20],
                   "Half of the numbers 1 to 20 are odd: 1, 3, 5, … 19. That is <b>%d</b>." % len(od)))
    assert len(ev) == 5 and len(od) == 10
    row = [n for n in range(51, 61) if n % 2 == 0]
    its.append(mcq("On a hundreds chart, how many even numbers are in the row 51 to 60?", len(row), [4, 6, 10],
                   "The even numbers are %s. That is <b>%d</b>. Do not forget 60: it ends in 0, so it is even."
                   % (", ".join(map(str, row)), len(row))))

    its.append(mcq("Which pattern has <b>only odd</b> numbers?", "135, 137, 139, 141",
                   ["135, 136, 137, 138", "130, 132, 134, 136", "311, 412, 513, 614"],
                   "Look at the ones digits: 5, 7, 9, 1. They are all odd, so <b>135, 137, 139, 141</b> is the answer. "
                   "In 311, 412, 513, 614 the ones digits are 1, 2, 3, 4."))
    its.append(mcq("The odd numbers start 1, 3, 5, 7, … What is the 10th odd number?", 19, [20, 21, 17],
                   "The odd numbers are 1, 3, 5, 7, 9, 11, 13, 15, 17, <b>19</b>. "
                   "A quick way: double 10 is 20, then take away 1."))
    assert [2 * k - 1 for k in range(1, 11)][-1] == 19
    its.append(mcq("The even numbers go 2, 4, 6, 8, … What is the 15th even number?", 30, [28, 32, 15],
                   "Each even number is double its place: the 15th even number is 2 %s 15 = <b>30</b>." % X))
    its.append(mcq("6 + 7 = 13, 21 + 22 = 43, 58 + 59 = 117. Add two numbers that are next to each other. "
                   "What is always true?", "The answer is odd",
                   ["The answer is even", "The answer ends in 3", "The answer is odd, then even"],
                   "Two numbers next to each other are one odd and one even. Odd + even is always "
                   "<b>odd</b>."))
    its.append(mcq("1 + 3 = 4, 1 + 3 + 5 = 9, 1 + 3 + 5 + 7 = 16. What is 1 + 3 + 5 + 7 + 9?", 25, [24, 26, 36],
                   "The answers are 2 %s 2, 3 %s 3, 4 %s 4. The next is 5 %s 5 = <b>25</b>. Check: 16 + 9 = 25."
                   % (X, X, X, X)))
    assert 1 + 3 + 5 + 7 + 9 == 25
    its.append(mcq("A pattern starts at 46 and goes up by 2: 46, 48, 50, … Will 75 be in the pattern?",
                   "No: 75 is odd", ["Yes: it keeps going up", "Yes: 75 ends in 5", "No: 75 is too big"],
                   "46 is even, and adding 2 always gives another even number. 75 ends in 5, so it is odd. "
                   "<b>No</b>, it is never in the pattern: the pattern goes 74, 76."))
    its.append(mcq("I am an odd number between 70 and 80. My ones digit is more than 7. What number am I?",
                   79, [78, 77, 89],
                   "The odd numbers between 70 and 80 are 71, 73, 75, 77, 79. Only <b>79</b> has a ones digit "
                   "more than 7. 78 is even, and 77 has a ones digit of 7, not more than 7."))
    its.append(mcq("Mia counts by 2s from 0: 0, 2, 4, 6, … Which number will she say?", 136, [135, 137, 141],
                   "Counting by 2s from 0 gives only even numbers. <b>136</b> ends in 6, so it is even. "
                   "135, 137 and 141 are odd."))
    assert len(its) == 20, len(its)
    return {"title": "Patterns and number lines", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def add(q, right, wrong, e):
        its.append(mcq(q, right, wrong, e))

    add("27 students are pairing up for a buddy reading activity. Can every student have a partner?",
        "No: 1 is left over", ["Yes: 27 is even", "No: 2 are left over", "Yes: 2 + 7 = 9"],
        "27 ends in 7, so it is odd. 27 students make 13 pairs with <b>1 student left over</b>. "
        "(2 left over could still make a pair.)")
    assert 27 == 13 * 2 + 1
    add("Two Year 4 classes of 23 and 27 students join for a buddy activity. Can everyone have a partner?",
        "Yes: odd + odd is even", ["No: odd + odd is odd", "No: 23 is odd", "Yes: 2 + 2 is even"],
        "23 and 27 are both odd. Odd + odd is even: 23 + 27 = 50. 50 students make 25 pairs, so <b>yes</b>.")
    assert (23 + 27) % 2 == 0
    add("24 Year 4 students and 25 Year 1 students pair up. How many pairs are there? How many students are left?",
        "24 pairs, 1 left", ["25 pairs, 0 left", "24 pairs, 0 left", "49 pairs, 1 left"],
        "24 + 25 = 49, which is odd. 49 = 24 pairs + 1, so there are <b>24 pairs and 1 student left</b>.")
    assert 24 + 25 == 49 == 24 * 2 + 1
    add("On Wattle Street, the houses on one side have odd numbers. Which house is on that side?",
        57, [48, 62, 70],
        "57 ends in 7, so it is odd: it is on the odd side. 48, 62 and 70 end in 8, 2 and 0, so they are even.")
    nm, he, his = P.next()
    add("%s lives at number 35 on the odd side of the street. What is the number of the next house on %s side, "
        "going up?" % (nm, his), 37, [36, 34, 45],
        "The odd side goes up by 2: 33, 35, <b>37</b>. 36 is across the street, on the even side.")
    add("The houses on the odd side of a street are numbered 1 to 25. How many houses are on that side?",
        13, [12, 25, 24],
        "1, 3, 5, … 25. There are 12 even numbers from 1 to 25, so 25 %s 12 = <b>13</b> odd numbers. "
        "12 forgets house number 1." % M)
    assert len(range(1, 26, 2)) == 13
    add("The houses on the even side of a street are numbered 2 to 40. How many houses are on that side?",
        20, [19, 21, 40], "2, 4, 6, … 40 is counting by 2s to 40. 40 ÷ 2 = <b>20</b> houses.")
    assert len(range(2, 41, 2)) == 20
    nm, he, his = P.next()
    add("%s lives at number 11 on the odd side of the street. %s friend lives 6 houses further along on the "
        "same side. What is the friend’s house number?" % (nm, cap(his)), 23, [17, 22, 24],
        "On the odd side the numbers go up by 2: 13, 15, 17, 19, 21, <b>23</b>. 6 %s 2 = 12 and 11 + 12 = 23. "
        "17 adds 1 for each house instead of 2." % X)
    assert 11 + 6 * 2 == 23
    add("A kookaburra has 2 legs. Which could be the number of legs on some kookaburras?", 34, [35, 37, 41],
        "Every kookaburra adds 2 legs, so the total is always even. Only <b>34</b> is even: 17 kookaburras.")
    add("A netball team has 7 players on the court. 3 teams practise at once. How many players are there? "
        "Is it odd or even?", "21: odd", ["21: even", "10: even", "24: even"],
        "3 %s 7 = 21. Odd %s odd is odd, so 21 is <b>odd</b>. 10 adds 3 + 7 instead of multiplying." % (X, X))
    assert 3 * 7 == 21
    add("In AFL footy, each team has 18 players on the field. How many players are on the field for 2 teams? "
        "Is it odd or even?", "36: even", ["36: odd", "20: even", "38: even"],
        "18 + 18 = 36. Even + even is even, so 36 is <b>even</b>.")
    assert 18 * 2 == 36
    nm, he, his = P.next()
    add("%s has 15 socks. How many pairs can %s make? How many socks are left over?" % (nm, he),
        "7 pairs, 1 left", ["8 pairs, 0 left", "7 pairs, 0 left", "6 pairs, 3 left"],
        "15 is odd. 7 pairs use 14 socks, and 15 %s 14 = 1. So <b>7 pairs and 1 sock left over</b>." % M)
    add("March has 31 days. How many dates in March are odd numbers?", 16, [15, 31, 14],
        "The odd dates are 1, 3, 5, … 31. 31 is odd, so it counts. From 1 to 30 there are 15 odd dates, "
        "plus 31 makes <b>16</b>.")
    assert len(range(1, 32, 2)) == 16
    add("June has 30 days. How many dates in June are even numbers?", 15, [14, 16, 30],
        "The even dates are 2, 4, 6, … 30. That is 30 ÷ 2 = <b>15</b> dates.")
    assert len(range(2, 31, 2)) == 15
    add("Students sit 2 to a seat on the excursion bus. 43 students get on. How many seats do they need?",
        22, [21, 43, 20],
        "43 is odd: 21 pairs and 1 left over. The extra student needs a seat too, so 21 + 1 = <b>22</b> seats.")
    assert -(-43 // 2) == 22
    nm, he, his = P.next()
    add("%s thinks of an odd number and adds 6. Is the answer odd or even?" % nm,
        "Odd: odd + even = odd", ["Even: odd + even = even", "Even: 6 is even", "It depends on the number"],
        "6 is even. Odd + even is always <b>odd</b>. For example, 9 + 6 = 15 and 21 + 6 = 27.")
    nm, he, his = P.next()
    add("%s thinks of an even number. Its tens digit is 7. Its ones digit is the biggest even digit. "
        "What is the number?" % nm, 78, [79, 87, 70],
        "The even digits are 0, 2, 4, 6, 8. The biggest is 8, so the number is <b>78</b>. "
        "87 has the digits the wrong way round.")
    nm, he, his = P.next()
    add("%s had 12 marbles and lost all of them. %s says the number left, 0, is not odd or even. Is %s right?"
        % (nm, cap(he), he), "No: 0 is even",
        ["Yes: 0 is not a number", "No: 0 is odd", "Yes: 0 is neither"],
        "<b>0 is even.</b> 0 objects means none are left over when you make pairs, and counting by 2s starts at 0.")
    nm, he, his = P.next()
    add("%s has only $2 coins in %s money box. Which amount could %s have?" % (nm, his, he),
        "$14", ["$13", "$15", "$9"],
        "Each $2 coin adds 2 dollars, so the total is always an even number of dollars. Only <b>$14</b> is even: "
        "seven $2 coins.")
    nm, he, his = P.next()
    add("%s shares 35 strawberries equally between 2 friends. Will any strawberries be left over?" % nm,
        "Yes: 1 is left over", ["No: 35 shares equally", "Yes: 3 are left over", "No: 3 + 5 is even"],
        "35 ends in 5, so it is odd. Each friend gets 17 and <b>1 strawberry is left over</b>.")
    assert 35 == 17 * 2 + 1
    assert len(its) == 20, len(its)
    return {"title": "Odd and even word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Odd or even? Make pairs</h2>"
        "<p>A number is <b>even</b> if you can put that many objects into pairs with none left over. "
        "It is <b>odd</b> if 1 is left over.</p>"
        "<figure class='sn-fig'>" + lesson_pairs_svg(8, 9)
        + "<figcaption>8 makes 4 pairs: even. 9 makes 4 pairs and 1 left over: odd.</figcaption></figure>"
        "<h2>Big numbers: look at the ones digit</h2>"
        "<p>Every ten, hundred and thousand splits into pairs. So only the <b>ones digit</b> decides.</p>"
        + table(["Ones digit", "The number is", "Examples"], [
            ["0, 2, 4, 6, 8", "Even", "30, 512, 4796"],
            ["1, 3, 5, 7, 9", "Odd", "41, 963, 7205"],
        ])
        + ex("Example", "Is 7354 odd or even?", "The ones digit is 4, which is even. The 7 at the front does not matter.",
             "even")
        + "<h2>Rules for adding, subtracting and multiplying</h2>"
        "<figure class='sn-fig'>" + lesson_sum_svg(5, 3)
        + "<figcaption>5 and 3 each have 1 left over. The two left-overs make a pair, so odd + odd is even.</figcaption></figure>"
        + table(["Adding or subtracting", "Answer", "Multiplying", "Answer"], [
            ["even + even", "even", "even %s even" % X, "even"],
            ["odd + odd", "even", "odd %s odd" % X, "odd"],
            ["even + odd", "odd", "even %s odd" % X, "even"],
        ])
        + "<p>Subtracting follows the same rules as adding: odd %s odd is even, even %s odd is odd.</p>" % (M, M)
        + ex("Predict", "Is 347 + 289 odd or even? Do not work it out.",
             "The ones digits are 7 and 9: odd + odd = even.", "even (347 + 289 = 636)")
        + ex("Check an answer", "Is 4 %s 237 = 949 right?" % X,
             "4 is even, so 4 %s any number is even. 949 is odd, so it must be wrong." % X, "no (it is 948)")
        + "<h2>Patterns on a number line</h2>"
        "<p>Odd and even numbers take turns. Jumping by 2 from an odd number lands only on odd numbers.</p>"
        "<figure class='sn-fig'>" + numline_svg(20, 30, label_every=1, dots=(21, 23, 25, 27, 29))
        + "<figcaption>The odd numbers 21, 23, 25, 27, 29 are every second number.</figcaption></figure>"
        + ex("Word problem", "27 students pair up for buddy reading. Is anyone left out?",
             "27 is odd: 13 pairs and 1 left over.", "yes, 1 student")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Looking at the first digit: 4537 is even", "Look at the ones digit: 7 is odd, so 4537 is odd"],
            ["Thinking odd + odd is odd: 3 + 5 is odd", "The two left-overs make a pair: 3 + 5 = 8, even"],
            ["Thinking 0 is not odd or even", "0 is even: counting by 2s starts 0, 2, 4"],
            ["Forgetting numbers that end in 0: 250 is odd", "A ones digit of 0 means even"],
        ])
    )


FAQ = [
    {"q": "Is 0 an odd or even number?",
     "a": "0 is even. It leaves nothing over when you make pairs, and counting by 2s starts at 0: 0, 2, 4, 6. That is why 10, 20 and 100 are even too."},
    {"q": "How can my child tell if a big number is odd or even?",
     "a": "Look only at the ones digit. If it is 0, 2, 4, 6 or 8 the number is even; if it is 1, 3, 5, 7 or 9 the number is odd. So 4537 is odd and 3718 is even."},
    {"q": "What are the odd and even rules for adding and multiplying?",
     "a": "Even + even and odd + odd are even, and even + odd is odd. When multiplying, the answer is odd only when both numbers are odd, like 3 × 5 = 15."},
    {"q": "What do Year 4 students learn about odd and even numbers in the Australian Curriculum?",
     "a": "In Year 4 (AC9M4N02) students Explain and use the properties of odd and even numbers. They predict whether a sum, difference or product is odd or even and use this to check their working."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(4810)
    P = People(rnd)
    sets = [set_odd_even(rnd), set_rules(rnd), set_predict(rnd), set_patterns(rnd), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "au", "subject": "maths", "grade": "year-4", "slug": "odd-and-even-numbers", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Odd and Even Numbers",
        "seo_title": "Year 4 Odd and Even Numbers Worksheets: Rules, Patterns and Word Problems (Free, with Answers)",
        "short_title": "Odd and even numbers",
        "domain": "Number",
        "standard_code": "AC9M4N02",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Explain and use the properties of odd and even numbers",
        "meta_desc": "Free Year 4 maths worksheets on odd and even numbers: use the ones digit, learn the rules for adding, "
                     "subtracting and multiplying, predict answers without calculating, find patterns on number lines "
                     "and solve word problems. 100 questions with an answer key, aligned to the Australian Curriculum (AC9M4N02).",
        "key_big": "Only the ones digit decides: 0, 2, 4, 6, 8 is even.",
        "key_sub": "Odd + odd is even, even + odd is odd, and a product is odd only when both numbers are odd. "
                   "0 is even.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(number line|\\d+ red counters|(1[6-9]|2\\d) counters in pairs)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
