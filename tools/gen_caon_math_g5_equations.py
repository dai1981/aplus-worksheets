# -*- coding: utf-8 -*-
"""
CA Grade 5 Math: Expressions, Equations and Inequalities (Ontario Mathematics Curriculum 2020, Grade 5: Algebra, C2.1-C2.4)
  python3 tools/gen_caon_math_g5_equations.py
Words to algebraic expressions and back (C2.1), evaluating expressions such as 3n + 4 when n = 6 (C2.2),
solving equations with whole numbers up to 100 and checking the solutions (C2.3), and inequalities with one
operation and whole numbers up to 50, graphed on a number line (C2.4), with word problems in Canadian contexts.
Wrong answers come from real student mistakes: reading 3n as 3 + n or as the number 36, writing 7 − n for
"7 less than n", using the wrong inverse operation, stopping after the first step, regrouping slips,
checking with the inverse operation instead of the original equation, and the wrong circle or arrow on a graph.
Every answer is checked in code. HTML attributes use single quotes (no backslashes in the JSON).
Canadian English. Real minus sign −.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
GREY = "#e4e4e4"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
M = "−"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]

SYM = {">": "&gt;", "<": "&lt;", ">=": "≥", "<=": "≤"}
PSYM = {">": ">", "<": "<", ">=": "≥", "<=": "≤"}
OPP = {">": "<", "<": ">", ">=": "<=", "<=": ">="}          # arrow the other way
SWAP = {">": ">=", ">=": ">", "<": "<=", "<=": "<"}          # open <-> closed circle
RIGHT = {">": True, ">=": True, "<": False, "<=": False}
CLOSED = {">": False, "<": False, ">=": True, "<=": True}
WORDS = {">": "greater than", "<": "less than", ">=": "greater than or equal to", "<=": "less than or equal to"}


# ------------------------------------------------------------ text helpers
def V(v):
    return "<i>%s</i>" % v


def term(a, v):
    return V(v) if a == 1 else "%d%s" % (a, V(v))


def osym(op):
    return "+" if op == "+" else M


def lhs(a, op, b, v="x"):
    return "%s %s %d" % (term(a, v), osym(op), b)


def eq(a, op, b, c, v="x"):
    return "%s = %d" % (lhs(a, op, b, v), c)


def ineq_s(a, op, b, rel, c, v="x"):
    return "%s %s %d" % (lhs(a, op, b, v), SYM[rel], c)


def sol(v, rel, k):
    return "%s %s %d" % (V(v), SYM[rel], k)


def val(a, op, b, x):
    return a * x + b if op == "+" else a * x - b


def solve2(a, op, b, c):
    r = F(c - b if op == "+" else c + b, a)
    assert r.denominator == 1 and r > 0, (a, op, b, c)
    return int(r)


def holds(x, rel, c):
    return {">": x > c, "<": x < c, ">=": x >= c, "<=": x <= c}[rel]


def calc(a, op, b, x):
    """'3 × 7 + 5 = 26'"""
    return "%d × %d %s %d = %d" % (a, x, osym(op), b, val(a, op, b, x))


def whole(v):
    v = F(v)
    return int(v) if v.denominator == 1 and v > 0 else None


def cap(s):
    return s[0].upper() + s[1:]


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


# ------------------------------------------------------------ question helpers
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


def mcq_n(q, v, cands, e, rnd, unit="", notes=None):
    """notes (optional, parallel to cands): why a wrong answer happens; added to e for the choices used."""
    notes = notes or [None] * len(cands)
    good = [(c, t) for c, t in zip(cands, notes) if c is not None and F(c).denominator == 1 and c > 0]
    it = mcq(q, (str(v) + unit, F(v)), [(str(c) + unit, F(c)) for c, t in good], e, rnd)
    used, add = set(), []
    for c, t in good:
        if t and str(c) + unit in it["c"] and F(c) not in used:
            used.add(F(c))
            add.append("%s comes from %s" % (c, t))
    if add:
        it["e"] += " Wrong answers: " + "; ".join(add) + "."
    return it


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    return len(str(t)) * fs * 0.58


def text(x, y, t, fs=16, anchor="middle", col=INK, italic=False, bold=False):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-style='italic'" if italic else "", " font-weight='700'" if bold else "",
               col, anchor, t))


class People:
    def __init__(self, rnd):
        self.pool = [(x, "she", "her") for x in GIRLS] + [(x, "he", "his") for x in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions (5 each per set)."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]


# ------------------------------------------------------------ pictures
def scale_svg(left, right, label):
    """A level pan balance. left / right: lists of 'x' (a block) or a number (a weight)."""
    def item_w(t):
        return 34 if t == "x" else max(34, int(tw(t, 16) + 14))
    gap = 6

    def pan_w(items):
        return max(80, sum(item_w(t) for t in items) + gap * (len(items) - 1) + 16)
    wl, wr = pan_w(left), pan_w(right)
    cl = 8 + wl / 2
    cr = cl + wl / 2 + 44 + wr / 2
    mid = (cl + cr) / 2
    top, ih = 10, 34
    py = top + ih
    s = []
    for items, c, w in ((left, cl, wl), (right, cr, wr)):
        tot = sum(item_w(t) for t in items) + gap * (len(items) - 1)
        x = c - tot / 2
        for t in items:
            iw = item_w(t)
            if t == "x":
                s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (x, top, iw, ih, FILL, GREEN))
                s.append(text(x + iw / 2, top + 24, "n", 18, col=RED, italic=True))
            else:
                s.append("<rect x='%.1f' y='%d' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='2'/>" % (x, top, iw, ih, GREY, INK))
                s.append(text(x + iw / 2, top + 23, t))
            x += iw + gap
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='6' fill='%s'/>" % (c - w / 2, py, w, INK))
        s.append("<rect x='%.1f' y='%d' width='4' height='18' fill='%s'/>" % (c - 2, py + 6, INK))
    by = py + 24
    s.append("<rect x='%.1f' y='%d' width='%.1f' height='6' fill='%s'/>" % (cl - 2, by, cr - cl + 4, INK))
    s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (mid, by + 6, mid - 22, by + 40, mid + 22, by + 40, GREEN))
    s.append("<rect x='%.1f' y='%d' width='80' height='5' fill='%s'/>" % (mid - 40, by + 40, INK))
    W = int(cr + wr / 2 + 8)
    return svg_wrap(W, by + 47, "".join(s), "pan balance: " + label)


GAP, PAD, FS = 30, 30, 15


def nline(lo, rel, k, label=None):
    """Number line from lo to lo + 10. Circle at k: open for > <, closed for >= <=.
    A thick green arrow shows the solutions."""
    hi = lo + 10
    assert lo <= k <= hi
    W = 2 * PAD + GAP * 10
    Y, H = 24, 56
    X = lambda v: PAD + GAP * (v - lo)
    L, R = PAD - 22, W - PAD + 22
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.8'/>" % (L + 2, Y, R - 2, Y, INK),
         "<path d='M%d %d L%d %d L%d %d Z' fill='%s'/>" % (L, Y, L + 9, Y - 5, L + 9, Y + 5, INK),
         "<path d='M%d %d L%d %d L%d %d Z' fill='%s'/>" % (R, Y, R - 9, Y - 5, R - 9, Y + 5, INK)]
    for v in range(lo, hi + 1):
        x = X(v)
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.6'/>" % (x, Y - 6, x, Y + 6, INK))
        s.append(text(x, Y + 26, str(v), FS))
    xc = X(k)
    end = R - 1 if RIGHT[rel] else L + 1
    tip = 12 if RIGHT[rel] else -12
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='5'/>" % (xc, Y, end - tip, Y, GREEN))
    s.append("<path d='M%d %d L%d %d L%d %d Z' fill='%s'/>" % (end, Y, end - tip, Y - 8, end - tip, Y + 8, GREEN))
    s.append("<circle cx='%d' cy='%d' r='7' fill='%s' stroke='%s' stroke-width='2.5'/>"
             % (xc, Y, GREEN if CLOSED[rel] else "#ffffff", GREEN))
    return svg_wrap(W, H, "".join(s), label or "number line graph")


def window(rnd, k):
    return max(0, k - rnd.choice([3, 4, 5, 6, 7]))


def describe(rel, k):
    return "%s circle at %d, arrow to the %s" % ("Closed" if CLOSED[rel] else "Open", k, "right" if RIGHT[rel] else "left")


def why_graph(rel, k, v="x"):
    circ = ("a closed (filled-in) circle, because %d is a solution" if CLOSED[rel]
            else "an open circle, because %d is not a solution") % k
    side = "right, toward greater numbers" if RIGHT[rel] else "left, toward lesser numbers"
    return "%s has %s, and the arrow points %s." % (sol(v, rel, k), circ, side)



def steps2(a, op, b, c, v="x"):
    """Undo + or − first, then undo ×."""
    x = solve2(a, op, b, c)
    mid = c - b if op == "+" else c + b
    undo = ("Subtract %d from both sides" % b) if op == "+" else ("Add %d to both sides" % b)
    return ("%s: %s = %d. Then divide both sides by %d: %s = %d ÷ %d = %d. Check: %s."
            % (undo, term(a, v), mid, a, V(v), mid, a, x, calc(a, op, b, x)))


# ------------------------------------------------------------ grade 5 helpers
N = V("n")


def mcq_e(q, right, wrong, e, rnd):
    return mcq(q, right, wrong, e, rnd)


def ev(expr, n):
    """expr: python expression in n (whole-number result checked)."""
    v = F(eval(expr, {"F": F}, {"n": F(n)}))
    assert v.denominator == 1 and v >= 0, (expr, n, v)
    return int(v)


# ------------------------------------------------------------ set 1: words to expressions
def set_words_expr(rnd, P):
    its = []
    n, n2, n3, n4 = N, "2" + N, "3" + N, "4" + N

    def w2e(words, right, wrong, e):
        its.append(mcq("Which expression means “%s”?" % words, right, wrong, e, rnd))

    w2e("5 more than a number <i>n</i>", "%s + 5" % n, ["5%s" % n, "%s %s 5" % (n, M), "5 %s %s" % (M, n)],
        "“5 more than” means add 5 to the number: %s + 5. 5%s means 5 × %s, which is different." % (n, n, n))
    w2e("7 less than a number <i>n</i>", "%s %s 7" % (n, M), ["7 %s %s" % (M, n), "%s + 7" % n, "7%s" % n],
        "“7 less than %s” means start with %s and take away 7: %s %s 7. Watch the order: 7 %s %s means 7 take away %s."
        % (n, n, n, M, M, n, n))
    w2e("3 times a number <i>n</i>", n3, ["%s + 3" % n, "%s ÷ 3" % n, "%s %s 3" % (n, M)],
        "“3 times %s” is 3 × %s. In algebra we write it as 3%s, with no × sign. 3%s does not mean 3 + %s." % (n, n, n, n, n))
    w2e("a number <i>n</i> divided by 4", "%s ÷ 4" % n, ["4 ÷ %s" % n, n4, "%s %s 4" % (n, M)],
        "Start with %s and divide by 4: %s ÷ 4. The order matters: 4 ÷ %s means 4 divided by %s." % (n, n, n, n))
    w2e("the sum of a number <i>n</i> and 12", "%s + 12" % n, ["12%s" % n, "%s %s 12" % (n, M), "12 %s %s" % (M, n)],
        "A <b>sum</b> is the answer to an addition: %s + 12." % n)
    w2e("the product of 6 and a number <i>n</i>", "6" + n, ["6 + %s" % n, "%s ÷ 6" % n, "%s %s 6" % (n, M)],
        "A <b>product</b> is the answer to a multiplication: 6 × %s, written 6%s. 6 + %s would be a sum." % (n, n, n))
    w2e("a number <i>n</i> decreased by 9", "%s %s 9" % (n, M), ["9 %s %s" % (M, n), "%s + 9" % n, "9" + n],
        "“Decreased by 9” means take 9 away from %s: %s %s 9." % (n, n, M))
    w2e("twice a number <i>n</i>", n2, ["%s + 2" % n, "%s ÷ 2" % n, "2 %s %s" % (M, n)],
        "“Twice” means 2 times: 2 × %s = 2%s. It is the same as %s + %s, not %s + 2." % (n, n, n, n, n))
    w2e("half of a number <i>n</i>", "%s ÷ 2" % n, [n2, "%s %s 2" % (n, M), "2 ÷ %s" % n],
        "Half of a number means divide it into 2 equal parts: %s ÷ 2. 2%s would be double, not half." % (n, n))
    w2e("4 more than 3 times a number <i>n</i>", "%s + 4" % n3, ["%s + 3" % n4, "3 + %s + 4" % n, "%s %s 4" % (n3, M)],
        "First “3 times %s”: 3%s. Then “4 more than” that: 3%s + 4. 3 + %s + 4 reads 3%s as 3 + %s." % (n, n, n, n, n, n))
    w2e("5 less than twice a number <i>n</i>", "%s %s 5" % (n2, M), ["5 %s %s" % (M, n2), "5%s %s 2" % (n, M), "2 + %s %s 5" % (n, M)],
        "“Twice %s” is 2%s. “5 less than” that means take away 5: 2%s %s 5. Watch the order: 5 %s 2%s is different."
        % (n, n, n, M, M, n))
    w2e("a number <i>n</i> divided by 3, plus 10", "%s ÷ 3 + 10" % n, ["3 ÷ %s + 10" % n, "%s + 10" % n3, "%s ÷ 10 + 3" % n],
        "Divide %s by 3 first: %s ÷ 3. Then add 10: %s ÷ 3 + 10." % (n, n, n))

    def e2w(expr, right, wrong, e):
        its.append(mcq("Which words match the expression %s?" % expr, right, wrong, e, rnd))

    e2w(n4, "4 times a number <i>n</i>", ["4 more than a number <i>n</i>", "a number <i>n</i> divided by 4", "4 less than a number <i>n</i>"],
        "4%s means 4 × %s, so it is “4 times a number %s.” It does not mean 4 + %s." % (n, n, n, n))
    e2w("%s %s 6" % (n, M), "6 less than a number <i>n</i>", ["6 minus a number <i>n</i>", "6 more than a number <i>n</i>", "6 times a number <i>n</i>"],
        "%s %s 6 starts with %s and takes away 6: “6 less than a number %s.” “6 minus a number %s” is 6 %s %s, the other order."
        % (n, M, n, n, n, M, n))
    e2w("%s + 1" % n2, "1 more than twice a number <i>n</i>",
        ["2 more than a number <i>n</i>", "twice a number <i>n</i>, minus 1", "the sum of 2, a number <i>n</i> and 1"],
        "2%s means twice %s (2 × %s). Then + 1 means 1 more. “The sum of 2, %s and 1” would be 2 + %s + 1, which reads 2%s as 2 + %s."
        % (n, n, n, n, n, n, n))
    e2w("%s ÷ 5" % n, "a number <i>n</i> divided by 5", ["5 divided by a number <i>n</i>", "5 times a number <i>n</i>", "5 less than a number <i>n</i>"],
        "%s ÷ 5 starts with %s and divides it by 5." % (n, n))
    e2w("%s + 8" % n, "8 more than a number <i>n</i>", ["the product of 8 and a number <i>n</i>", "a number <i>n</i> decreased by 8", "a number <i>n</i> divided by 8"],
        "+ 8 means 8 more. The product of 8 and %s would be 8%s." % (n, n))

    nm, he, his = P.next()
    s = V("s")
    its.append(mcq("%s has some stickers, %s. %s gets 9 more stickers. Which expression shows how many stickers %s has now?"
                   % (nm, s, cap(he), he), "%s + 9" % s, ["9%s" % s, "%s %s 9" % (s, M), "9 %s %s" % (M, s)],
                   "%s gets more, so add: %s + 9." % (cap(he), s), rnd))
    p = V("p")
    its.append(mcq("Freezies cost $2 each at the school fun fair. Which expression shows the cost in dollars of %s freezies?" % p,
                   "2" + p, ["%s + 2" % p, "%s ÷ 2" % p, "%s %s 2" % (p, M)],
                   "Each freezie costs $2, so %s freezies cost 2 × %s = 2%s dollars." % (p, p, p), rnd))
    nm, he, his = P.next()
    b = V("b")
    its.append(mcq("A box holds %s crayons. %s has 3 full boxes and 5 loose crayons. Which expression shows how many crayons %s has?"
                   % (b, nm, he), "3%s + 5" % b, ["5%s + 3" % b, "3 + %s + 5" % b, "8" + b],
                   "3 boxes of %s crayons is 3%s. Add the 5 loose crayons: 3%s + 5. 3 + %s + 5 counts only one box."
                   % (b, b, b, b), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Words to expressions", "items": its}


# ------------------------------------------------------------ set 2: evaluate expressions
def set_evaluate(rnd, P):
    its = []

    def item(expr_html, expr_py, n, cands, work, notes=None, q=None, unit=""):
        v = ev(expr_py, n)
        e = "Put %d in place of %s: %s = %d." % (n, N, work, v)
        qq = q or "What is the value of %s when %s = %d?" % (expr_html, N, n)
        its.append(mcq_n(qq, v, cands, e, rnd, unit, notes))

    item("%s + 9" % N, "n + 9", 6, [54, 3, 14], "6 + 9",
         ["multiplying 6 × 9", "subtracting 9 − 6", "counting on and saying 6 as the first count"])
    item("%s %s 7" % (N, M), "n - 7", 15, [22, 12, 9], "15 %s 7" % M,
         ["adding instead of subtracting", "taking the smaller digit from the larger (7 − 5 = 2)", "counting back and saying 15 as the first count"])
    item("4" + N, "4*n", 7, [11, 47, 32], "4 × 7",
         ["reading 4%s as 4 + %s" % (N, N), "reading 4%s as the number 47" % N, "using 4 × 8 instead of 4 × 7"])
    item("5" + N, "5*n", 9, [14, 59, 40], "5 × 9",
         ["reading 5%s as 5 + %s" % (N, N), "reading 5%s as the number 59" % N, "using 5 × 8"])
    item("3%s + 4" % N, "3*n+4", 6, [13, 40, 30], "3 × 6 + 4 = 18 + 4",
         ["reading 3%s as 3 + %s (3 + 6 + 4)" % (N, N), "reading 3%s as the number 36 (36 + 4)" % N, "adding before multiplying (3 × 10)"])
    item("2%s + 5" % N, "2*n+5", 8, [15, 33, 26], "2 × 8 + 5 = 16 + 5",
         ["reading 2%s as 2 + %s" % (N, N), "reading 2%s as the number 28" % N, "adding before multiplying (2 × 13)"])
    item("6%s %s 4" % (N, M), "6*n-4", 5, [7, 61, 34], "6 × 5 %s 4 = 30 %s 4" % (M, M),
         ["reading 6%s as 6 + %s" % (N, N), "reading 6%s as the number 65" % N, "adding 4 instead of subtracting it"])
    item("4%s + 9" % N, "4*n+9", 3, [16, 43, 48], "4 × 3 + 9 = 12 + 9",
         ["reading 4%s as 4 + %s" % (N, N), "reading 4%s as the number 34" % N, "adding before multiplying (4 × 12)"])
    item("7%s %s 10" % (N, M), "7*n-10", 6, [3, 42, 52], "7 × 6 %s 10 = 42 %s 10" % (M, M),
         ["reading 7%s as 7 + %s" % (N, N), "forgetting to subtract 10", "adding 10 instead of subtracting it"])
    item("%s ÷ 4" % N, "n/4", 32, [128, 28, 36], "32 ÷ 4",
         ["multiplying instead of dividing", "subtracting 4", "adding 4"])
    item("%s ÷ 3 + 5" % N, "n/3+5", 27, [86, 29, 9], "27 ÷ 3 + 5 = 9 + 5",
         ["multiplying by 3 instead of dividing", "subtracting 3 instead of dividing", "forgetting the + 5"])
    item("10 + 2%s" % N, "10+2*n", 9, [21, 39, 108], "10 + 2 × 9 = 10 + 18",
         ["reading 2%s as 2 + %s" % (N, N), "reading 2%s as the number 29" % N, "working left to right: (10 + 2) × 9"])
    item("50 %s 3%s" % (M, N), "50-3*n", 8, [39, 12, 74], "50 %s 3 × 8 = 50 %s 24" % (M, M),
         ["reading 3%s as 3 + %s (50 %s 3 %s 8)" % (N, N, M, M), "reading 3%s as the number 38" % N, "adding 24 instead of subtracting it"])
    item("8%s + 3" % N, "8*n+3", 0, [11, 83, 24], "8 × 0 + 3 = 0 + 3",
         ["reading 8%s as 8 + %s" % (N, N), "reading 8%s as the number 80" % N, "adding before multiplying (8 × 3)"])
    item("%s + %s + %s" % (N, N, N), "n+n+n", 7, [10, 14, 28], "7 + 7 + 7",
         ["reading it as %s + 3" % N, "adding only two 7s", "adding four 7s"])
    # which expression
    exprs = [("5" + N, "5*n"), ("%s + 20" % N, "n+20"), ("4%s + 5" % N, "4*n+5"), ("2%s + 10" % N, "2*n+10")]
    vals = [ev(p, 4) for _, p in exprs]
    assert vals.count(20) == 1 and vals[0] == 20
    its.append(mcq("Which expression has the value 20 when %s = 4?" % N, exprs[0][0], [x for x, _ in exprs[1:]],
                   "Put 4 in for %s: 5 × 4 = 20 ✓; 4 + 20 = 24; 4 × 4 + 5 = 21; 2 × 4 + 10 = 18." % N, rnd))
    exprs = [("30 %s %s" % (M, N), "30-n"), ("4" + N, "4*n"), ("%s + 12" % N, "n+12"), ("2%s + 8" % N, "2*n+8")]
    vals = [ev(p, 5) for _, p in exprs]
    assert max(vals) == vals[0] and vals.count(vals[0]) == 1 and len(set(vals)) == 4
    its.append(mcq("Which expression has the greatest value when %s = 5?" % N, exprs[0][0], [x for x, _ in exprs[1:]],
                   "Put 5 in for %s: 30 %s 5 = 25; 4 × 5 = 20; 5 + 12 = 17; 2 × 5 + 8 = 18. The greatest is 25." % (N, M), rnd))
    h = V("h")
    v = 4 * 2 + 3
    its.append(mcq_n("Renting skates costs 4%s + 3 dollars for %s hours. What does it cost to rent skates for 2 hours?" % (h, h),
                     v, [9, 45, 20],
                     "Put 2 in for %s: 4 × 2 + 3 = 8 + 3 = 11. It costs $11. Wrong answers: 9 reads 4%s as 4 + %s; 45 reads 4%s as 42; 20 adds before multiplying (4 × 5)."
                     % (h, h, h, h), rnd))
    its[-1]["c"] = ["$" + c for c in its[-1]["c"]]
    s = V("s")
    its.append(mcq_n("The perimeter of a square with sides %s cm long is 4%s cm. What is the perimeter when %s = 9?" % (s, s, s),
                     36, [13, 81, 18],
                     "Put 9 in for %s: 4 × 9 = 36 cm. 13 reads 4%s as 4 + %s, 81 is 9 × 9 (that is the area), and 18 counts only 2 sides."
                     % (s, s, s), rnd, " cm"))
    c = V("c")
    its.append(mcq_n("A chair has 4 legs. The expression 4%s gives the number of legs on %s chairs. How many legs are on 12 chairs?" % (c, c),
                     48, [16, 44, 52],
                     "Put 12 in for %s: 4 × 12 = 48 legs. 16 reads 4%s as 4 + 12. 44 and 52 use 11 or 13 chairs instead of 12." % (c, c),
                     rnd, " legs"))
    assert len(its) == 20, len(its)
    return {"title": "Evaluate expressions", "items": its}


# ------------------------------------------------------------ set 3: solve equations
def set_solve(rnd, P):
    its = []

    def item(q_eq, x, cands, e, notes=None):
        its.append(mcq_n("Solve: %s" % q_eq, x, cands, e, rnd, notes=notes))

    item("%s + 17 = 45" % N, 28, [62, 32, 38],
         "Undo + 17 by subtracting 17 from both sides: %s = 45 %s 17 = 28. Check: 28 + 17 = 45." % (N, M),
         ["adding 17 instead of subtracting it", "taking 5 %s 7 as 7 %s 5" % (M, M), "regrouping but not taking 1 away from the tens"])
    item("%s %s 23 = 58" % (N, M), 81, [35, 71, 711],
         "Undo %s 23 by adding 23 to both sides: %s = 58 + 23 = 81. Check: 81 %s 23 = 58." % (M, N, M),
         ["subtracting instead of adding", "forgetting to carry the 1 ten", "writing 8 + 3 = 11 in the ones place without regrouping"])
    item("6%s = 54" % N, 9, [48, 324, 60],
         "6%s means 6 × %s. Undo × 6 by dividing both sides by 6: %s = 54 ÷ 6 = 9. Check: 6 × 9 = 54." % (N, N, N),
         ["subtracting 6 instead of dividing", "multiplying by 6 instead of dividing", "adding 6"])
    item("%s ÷ 4 = 9" % N, 36, [13, 5, 32],
         "Undo ÷ 4 by multiplying both sides by 4: %s = 9 × 4 = 36. Check: 36 ÷ 4 = 9." % N,
         ["adding 4 instead of multiplying", "subtracting 4", "using 4 × 8 instead of 4 × 9"])
    item("7%s = 63" % N, 9, [56, 70, 8],
         "Divide both sides by 7: %s = 63 ÷ 7 = 9. Check: 7 × 9 = 63." % N,
         ["subtracting 7 instead of dividing", "adding 7", "a fact slip (7 × 8 = 56, not 63)"])
    item("%s ÷ 5 = 8" % N, 40, [13, 3, 45],
         "Multiply both sides by 5: %s = 8 × 5 = 40. Check: 40 ÷ 5 = 8." % N,
         ["adding 5 instead of multiplying", "subtracting 5", "using 5 × 9"])
    item("45 = %s + 19" % N, 26, [64, 34, 36],
         "The letter can be on the right side. Subtract 19 from both sides: 45 %s 19 = 26, so %s = 26. Check: 26 + 19 = 45." % (M, N),
         ["adding 19 instead of subtracting it", "taking 5 %s 9 as 9 %s 5" % (M, M), "regrouping but not taking 1 away from the tens"])
    item("30 %s %s = 12" % (M, N), 18, [42, 22, 8],
         "30 take away some number is 12. The number taken away is 30 %s 12 = 18. Check: 30 %s 18 = 12." % (M, M),
         ["adding 30 + 12", "taking 2 %s 0 instead of regrouping" % M, "subtracting 12 from 20 instead of 30"])
    item("48 ÷ %s = 6" % N, 8, [288, 42, 54],
         "48 divided by some number is 6. Since 6 × 8 = 48, %s = 48 ÷ 6 = 8. Check: 48 ÷ 8 = 6." % N,
         ["multiplying 48 × 6", "subtracting 6", "adding 6"])
    item("9%s = 72" % N, 8, [63, 81, 648],
         "Divide both sides by 9: %s = 72 ÷ 9 = 8. Check: 9 × 8 = 72." % N,
         ["subtracting 9 instead of dividing", "adding 9", "multiplying by 9 instead of dividing"])
    # pan balances
    for k, b, c, cands, notes in [(2, 8, 20, [12, 14, 2], ["stopping at 2%s = 12" % N, "adding 8 instead of subtracting it", "dividing first: 20 ÷ 2 %s 8" % M]),
                                  (3, 4, 19, [15, 12, 45], ["stopping at 3%s = 15" % N, "subtracting 3 instead of dividing by 3", "multiplying 15 by 3 instead of dividing"])]:
        x = solve2(k, "+", b, c)
        svg = scale_svg(["x"] * k + [str(b)], [str(c)], "%d blocks n and %d balance %d" % (k, b, c))
        e = ("The balance shows %s. Take %d off both pans: %s = %d. %d equal blocks make %d, so each block is %d ÷ %d = %d. Check: %s."
             % (eq(k, "+", b, c, "n"), b, term(k, "n"), c - b, k, c - b, c - b, k, x, calc(k, "+", b, x)))
        its.append(mcq_n(fig(svg) + "The pan balance is level. Each block has the same mass, %s. What is %s?" % (N, N),
                         x, cands, e, rnd, notes=notes))
    # two-step
    for a, op, b, c, cands, notes in [
            (2, "+", 3, 15, [12, 9, 10], ["stopping at 2%s = 12" % N, "adding 3 instead of subtracting it", "subtracting 2 instead of dividing by 2"]),
            (3, "-", 2, 25, [27, 24, 81], ["stopping at 3%s = 27" % N, "subtracting 3 instead of dividing by 3", "multiplying 27 by 3"]),
            (4, "+", 5, 41, [36, 32, 144], ["stopping at 4%s = 36" % N, "subtracting 4 instead of dividing by 4", "multiplying 36 by 4"]),
            (5, "+", 10, 60, [50, 14, 2], ["stopping at 5%s = 50" % N, "adding 10 instead of subtracting it", "dividing first: 60 ÷ 5 %s 10" % M]),
            (6, "-", 6, 30, [36, 4, 24], ["stopping at 6%s = 36" % N, "subtracting 6 instead of adding it", "subtracting 6 from 30 and stopping"])]:
        x = solve2(a, op, b, c)
        item(eq(a, op, b, c, "n"), x, cands, steps2(a, op, b, c, "n"), notes)
    its.append(mcq("What is the best first step to solve %s?" % eq(3, "+", 5, 26, "n"),
                   "Subtract 5 from both sides",
                   ["Divide 26 by 3", "Add 5 to both sides", "Subtract 3 from both sides"],
                   "3%s + 5 means “multiply by 3, then add 5.” Undo in reverse order: first subtract 5 from both sides to get 3%s = 21, "
                   "then divide by 3 to get %s = 7." % (N, N, N), rnd))
    its.append(mcq("What should you do to solve %s ÷ 6 = 7?" % N,
                   "Multiply both sides by 6",
                   ["Divide 7 by 6", "Subtract 6 from both sides", "Add 6 to both sides"],
                   "The opposite of dividing by 6 is multiplying by 6: %s = 7 × 6 = 42. Check: 42 ÷ 6 = 7." % N, rnd))
    item("%s + %s + 9 = 25" % (N, N), 8, [16, 17, 14],
         "%s + %s is 2%s, so 2%s + 9 = 25. Subtract 9: 2%s = 16. Divide by 2: %s = 8. Check: 8 + 8 + 9 = 25." % ((N,) * 6),
         ["stopping at %s + %s = 16" % (N, N), "adding 9 instead of subtracting it", "reading %s + %s as %s + 2" % (N, N, N)])
    assert len(its) == 20, len(its)
    return {"title": "Solve equations", "items": its}


# ------------------------------------------------------------ set 4: check solutions
def set_check(rnd, P):
    its = []
    v = "n"
    for x, a, op, b in [(6, 3, "+", 4), (8, 2, "+", 9), (5, 6, "-", 7), (9, 4, "+", 5), (7, 5, "-", 8), (4, 9, "+", 6)]:
        c = val(a, op, b, x)
        other = "-" if op == "+" else "+"
        wr = [(b, op, a), (a, other, b)]
        for ca, cop, cb in wr:
            assert val(ca, cop, cb, x) != c and val(ca, cop, cb, x) > 0
        add_all = x + a + b if op == "+" else x + a - b
        assert add_all != c and add_all > 0
        right = eq(a, op, b, c, v)
        wrong = [eq(ca, cop, cb, c, v) for ca, cop, cb in wr] + ["%s + %d %s %d = %d" % (N, a, osym(op), b, c)]
        e = ("Put %d in for %s in each one. %s ✓. The others are false: %s; %s; %d + %d %s %d = %d."
             % (x, N, calc(a, op, b, x), calc(b, op, a, x), calc(a, other, b, x), x, a, osym(op), b, add_all))
        its.append(mcq("Which equation has %s = %d as its solution?" % (N, x), right, wrong, e, rnd))
    for a, op, b, x0, d in [(3, "+", 5, 7, 0), (4, "+", 6, 5, 1), (5, "-", 8, 9, 0),
                            (6, "+", 4, 7, -1), (2, "+", 13, 9, 0), (7, "-", 4, 6, 1)]:
        c = val(a, op, b, x0)
        x = x0 + d
        digits = "%d%d %s %d = %d" % (a, x, osym(op), b, val(1, op, b, int("%d%d" % (a, x))))
        q = "Is %s = %d a solution of %s? Which check is correct?" % (N, x, eq(a, op, b, c, v))
        if d == 0:
            right = "Yes, because %s" % calc(a, op, b, x)
            wrong = ["No, because %s" % digits,
                     "No, because %d + %d %s %d = %d" % (a, x, osym(op), b, val(1, op, b, a + x)),
                     "No, because %d %s %d = %d, not %d" % (c, osym("-" if op == "+" else "+"), b,
                                                           c - b if op == "+" else c + b, x)]
            e = ("Put %d in for %s: %s. Both sides are equal, so %d is a solution. %s means %d × %s, not the number %d%d or %d + %d."
                 % (x, N, calc(a, op, b, x), x, term(a, v), a, N, a, x, a, x))
        else:
            mid = c - b if op == "+" else c + b
            assert mid != a * x and mid % a == 0
            right = "No, because %s, not %d" % (calc(a, op, b, x), c)
            wrong = ["Yes, because %d %s %d = %d and %d ÷ %d = %d" % (c, osym("-" if op == "+" else "+"), b, mid, mid, a, x),
                     "No, because %s" % digits,
                     "No, because %d × %d = %d, not %d" % (a, x, a * x, c)]
            e = ("Put %d in for %s: %s. That is not %d, so %d is not a solution. (The solution is %d.) "
                 "%d ÷ %d is %d, not %d, and you must check the whole left side, %s."
                 % (x, N, calc(a, op, b, x), c, x, x0, mid, a, x0, x, lhs(a, op, b, v)))
        its.append(mcq(q, right, wrong, e, rnd))
    # the right way to check
    for nm_eq, got, right, wrong, e in [
        ("%s + 18 = 50" % N, 68, "68 + 18 = 86, not 50, so 68 is wrong",
         ["68 %s 18 = 50, so 68 is right" % M, "50 + 18 = 68, so 68 is right", "68 + 50 = 118, so 68 is wrong"],
         "To check, put the answer back into the <b>original</b> equation: 68 + 18 = 86, not 50. So 68 is wrong. "
         "The right answer is 50 %s 18 = 32 (check: 32 + 18 = 50). Doing the same work again, or using the opposite operation, does not test the answer." % M),
        ("%s %s 16 = 25" % (N, M), 31, "31 %s 16 = 15, not 25, so 31 is wrong" % M,
         ["25 + 16 = 31, so 31 is right", "31 + 16 = 47, so 31 is wrong", "31 is greater than 25, so 31 is right"],
         "Put 31 back into the original equation: 31 %s 16 = 15, not 25. So 31 is wrong. "
         "The right answer is 25 + 16 = 41 (the 1 ten was not carried). Check: 41 %s 16 = 25." % (M, M)),
        ("4%s = 36" % N, 32, "4 × 32 = 128, not 36, so 32 is wrong",
         ["32 + 4 = 36, so 32 is right", "36 %s 4 = 32, so 32 is right" % M, "32 ÷ 4 = 8, so 32 is wrong"],
         "4%s means 4 × %s. Put 32 back in: 4 × 32 = 128, not 36. So 32 is wrong. The right answer is 36 ÷ 4 = 9 (check: 4 × 9 = 36)." % (N, N))]:
        nm, he, his = P.next()
        its.append(mcq("%s solved %s and got %s = %d. Which is the correct way to check %s answer?" % (nm, nm_eq, N, got, his),
                       right, wrong, e, rnd))
    # test each choice
    for qe, fn, x, ws in [("2%s + 7 = 25" % N, lambda t: 2 * t + 7, 9, [18, 16, 8]),
                          ("5%s %s 3 = 32" % (N, M), lambda t: 5 * t - 3, 7, [35, 29, 6]),
                          ("%s ÷ 4 + 2 = 9" % N, lambda t: F(t, 4) + 2, 28, [7, 44, 34]),
                          ("%s + %s + %s = 27" % (N, N, N), lambda t: 3 * t, 9, [24, 30, 81])]:
        target = fn(x)
        for w in ws:
            assert fn(w) != target
        parts = []
        for t in [x] + ws:
            r = fn(t)
            rs = str(r) if F(r).denominator == 1 else "not a whole number"
            if qe.startswith("2"):
                parts.append("2 × %d + 7 = %s" % (t, rs))
            elif qe.startswith("5"):
                parts.append("5 × %d %s 3 = %s" % (t, M, rs))
            elif "÷" in qe:
                parts.append("%d ÷ 4 + 2 = %s" % (t, rs) if F(r).denominator == 1 else "%d ÷ 4 is not a whole number" % t)
            else:
                parts.append("%d + %d + %d = %s" % (t, t, t, rs))
        e = "Test each choice in the equation. %s ✓; %s." % (parts[0], "; ".join(parts[1:]))
        its.append(mcq_n("Which number is the solution of %s? Test each choice." % qe, x, ws, e, rnd))
    nm, he, his = P.next()
    its.append(mcq("%s checks %s = 9 in 7%s %s 13 = 50. %s writes: 7 × 9 %s 13 = 63 %s 13 = 50. What does this show?"
                   % (nm, N, N, M, cap(he), M, M),
                   "9 is the solution", ["9 is not the solution", "The solution is 50", "The solution is 63"],
                   "When %s = 9, the left side equals 50, the same as the right side. So 9 is the solution. "
                   "63 is only 7 × 9, and 50 is the value of the right side." % N, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Check solutions", "items": its}


# ------------------------------------------------------------ set 5: inequalities, graphs and word problems
def set_ineq_words(rnd, P):
    its = []
    for q, k, rel, cands, e in [
        ("%s + 6 &lt; 20" % N, 14, "<", [("<", 26), (">", 14), ("<=", 14)],
         "Undo + 6 by subtracting 6 from both sides: %s &lt; 14. The sign stays &lt;. 14 itself is not a solution, because 14 + 6 = 20 is not less than 20."),
        ("%s %s 8 &gt; 15" % (N, M), 23, ">", [(">", 7), ("<", 23), (">=", 23)],
         "Undo %s 8 by adding 8 to both sides: %s &gt; 23. 23 itself is not a solution, because 23 %s 8 = 15 is not greater than 15."),
        ("4%s ≤ 32" % N, 8, "<=", [("<=", 28), (">=", 8), ("<", 8)],
         "Undo × 4 by dividing both sides by 4: %s ≤ 8. 8 is a solution, because 4 × 8 = 32 and 32 ≤ 32 is true."),
        ("%s ÷ 3 ≥ 9" % N, 27, ">=", [(">=", 3), (">=", 12), (">", 27)],
         "Undo ÷ 3 by multiplying both sides by 3: %s ≥ 27. 27 is a solution, because 27 ÷ 3 = 9 and 9 ≥ 9 is true.")]:
        e = e % ((M, N, M) if e.count("%s") == 3 else (N,))
        its.append(mcq("Solve: %s" % q, (sol("n", rel, k), (rel, k)),
                       [(sol("n", r, kk), (r, kk)) for r, kk in cands], e, rnd))
    # which number is (not) a solution
    for q, fn, rel, c, r, ws, want in [("%s + 9 &gt; 30" % N, lambda t: t + 9, ">", 30, 22, [21, 19, 12], True),
                                       ("5%s &lt; 40" % N, lambda t: 5 * t, "<", 40, 8, [7, 6, 3], False)]:
        assert holds(fn(r), rel, c) == want
        for x in ws:
            assert holds(fn(x), rel, c) != want
        tests = "; ".join("%d → %d %s %d is %s" % (x, fn(x), SYM[rel], c, "true" if holds(fn(x), rel, c) else "false")
                          for x in [r] + ws)
        qq = "Which number is %s a solution of %s?" % ("" if want else "<b>not</b>", q)
        qq = qq.replace("is  a", "is a")
        e = "Test each number in the left side. %s." % tests
        if r == 8:
            e += " 5 × 8 = 40, and 40 is not less than 40."
        else:
            e += " 21 + 9 = 30, and 30 is not greater than 30."
        its.append(mcq_n(qq, r, ws, e, rnd))
    # graph -> which inequality
    for k, rel, right, wrong, e in [
        (9, ">=", "%s + 5 ≥ 14" % N, ["%s + 5 &gt; 14" % N, "%s + 5 ≤ 14" % N, "%s %s 5 ≥ 14" % (N, M)],
         "The graph shows %s ≥ 9: a closed circle at 9, arrow to the right. %s + 5 ≥ 14 gives %s ≥ 9 (subtract 5). "
         "%s %s 5 ≥ 14 gives %s ≥ 19 instead." % (N, N, N, N, M, N)),
        (6, "<", "3%s &lt; 18" % N, ["3%s ≤ 18" % N, "3%s &gt; 18" % N, "%s + 3 &lt; 18" % N],
         "The graph shows %s &lt; 6: an open circle at 6, arrow to the left. 3%s &lt; 18 gives %s &lt; 6 (divide by 3). "
         "%s + 3 &lt; 18 gives %s &lt; 15, because it reads 3%s as 3 + %s." % (N, N, N, N, N, N, N))]:
        svg = nline(window(rnd, k), rel, k, "number line graph of n %s %d" % (PSYM[rel], k))
        its.append(mcq(fig(svg) + "The graph shows the solution of which inequality?", right, wrong, e, rnd))
    # how to graph
    for q, rel, k in [("%s %s 7 &gt; 12" % (N, M), ">", 19), ("2%s ≤ 30" % N, "<=", 15)]:
        right = describe(rel, k)
        wrong = [describe(SWAP[rel], k), describe(OPP[rel], k), describe(OPP[SWAP[rel]], k)]
        e = "First solve: %s gives %s. %s" % (q, sol("n", rel, k), why_graph(rel, k, "n"))
        its.append(mcq("How do you graph the solution of %s on a number line?" % q, right, wrong, e, rnd))
    # word problems
    nm, he, his = P.next()
    its.append(mcq("%s has some hockey cards, %s. %s gets 15 more and now has 42. Which equation fits?" % (nm, N, cap(he)),
                   "%s + 15 = 42" % N, ["15%s = 42" % N, "%s %s 15 = 42" % (N, M), "%s + 42 = 15" % N],
                   "%s starts with %s cards and gets 15 more: %s + 15. That equals 42: %s + 15 = 42. (So %s = 27.)"
                   % (cap(he), N, N, N, N), rnd))
    nm, he, his = P.next()
    its.append(mcq_n("%s buys 6 packs of markers. Each pack has the same number of markers. %s has 48 markers in all. "
                     "How many markers are in each pack?" % (nm, cap(he)), 8, [42, 54, 288],
                     "6%s = 48, so %s = 48 ÷ 6 = 8. Check: 6 × 8 = 48. 42 subtracts 6, 54 adds 6, and 288 multiplies." % (N, N),
                     rnd, " markers"))
    its.append(mcq_n("On a canoe trip, a group paddles some kilometres on Saturday and 18 km on Sunday. They paddle 45 km in all. "
                     "How far did they paddle on Saturday?", 27, [63, 33, 37],
                     "%s + 18 = 45, so %s = 45 %s 18 = 27 km. Check: 27 + 18 = 45. 63 adds instead of subtracting; 33 takes 5 %s 8 as 8 %s 5; "
                     "37 forgets to take 1 away from the tens." % (N, N, M, M, M), rnd, " km"))
    its.append(mcq_n("A class shares some maple taffy equally among 8 groups. Each group gets 6 pieces. "
                     "How many pieces of taffy were there?", 48, [14, 2, 42],
                     "%s ÷ 8 = 6, so %s = 6 × 8 = 48. Check: 48 ÷ 8 = 6. 14 adds and 2 subtracts; 42 uses 6 × 7." % (N, N),
                     rnd, " pieces"))
    nm, he, his = P.next()
    its.append(mcq_n("For the Terry Fox Run, %s has raised $35. %s wants to raise $80 in all. How much more does %s need to raise?"
                     % (nm, cap(he), he), 45, [115, 55, 50],
                     "35 + %s = 80, so %s = 80 %s 35 = 45. Check: 35 + 45 = 80. 115 adds instead of subtracting, "
                     "55 forgets to regroup, and 50 subtracts only the 30." % (N, N, M), rnd))
    its[-1]["c"] = ["$" + c for c in its[-1]["c"]]
    its.append(mcq_n("Science centre tickets cost $7 each. A family also pays $5 for parking. They pay $33 in all. "
                     "How many tickets did they buy? Solve 7%s + 5 = 33." % N, 4, [28, 21, 196],
                     steps2(7, "+", 5, 33, "n") + " 28 forgets to divide by 7, 21 subtracts 7 instead of dividing, and 196 multiplies 28 by 7.",
                     rnd, " tickets"))
    its.append(mcq("A school bus can hold at most 48 students. 29 students are already on the bus. Which inequality shows how many "
                   "more students, %s, can get on?" % V("s"),
                   "%s + 29 ≤ 48" % V("s"), ["%s + 29 ≥ 48" % V("s"), "%s + 29 &lt; 48" % V("s"), "%s %s 29 ≤ 48" % (V("s"), M)],
                   "The students on the bus are %s + 29. “At most 48” means 48 is allowed, so use ≤: %s + 29 ≤ 48."
                   % (V("s"), V("s")), rnd))
    its.append(mcq_n("Solve %s + 29 ≤ 48 for the bus. What is the greatest number of students who can still get on?" % V("s"),
                     19, [77, 18, 21],
                     "Subtract 29: %s ≤ 19. So at most 19 more students. 77 adds instead of subtracting, 18 forgets that ≤ includes 19, "
                     "and 21 takes 8 %s 9 as 9 %s 8." % (V("s"), M, M), rnd, " students"))
    nm, he, his = P.next()
    its.append(mcq_n("%s earns 3 points for each correct answer in a math game. %s needs <b>more than</b> 24 points to win, so "
                     "3%s &gt; 24. What is the least number of correct answers %s needs?" % (nm, cap(he), N, he), 9, [8, 72, 21],
                     "Divide by 3: %s &gt; 8. 8 correct answers give exactly 24 points, which is not more than 24, so the least whole number is 9. "
                     "72 multiplies instead of dividing, and 21 subtracts 3." % N, rnd, " answers"))
    d = V("d")
    its.append(mcq("A class earns 5 points each day. They need at least 30 points for a pizza party, so 5%s ≥ 30. "
                   "How do you graph the number of days, %s?" % (d, d),
                   describe(">=", 6), [describe(">", 6), describe("<=", 6), describe("<", 6)],
                   "Divide by 5: %s ≥ 6. %s" % (d, why_graph(">=", 6, "d")), rnd))
    assert len(its) == 20, len(its)
    return {"title": "Inequalities, graphs and word problems", "items": its}


# ------------------------------------------------------------ lesson
def body_html():
    bal = scale_svg(["x", "x", "6"], ["20"], "2 blocks n and 6 balance 20")
    g1 = nline(8, "<", 14, "number line graph of n < 14")
    g2 = nline(4, ">=", 8, "number line graph of n ≥ 8")
    n = N
    return (
        "<h2>What is an expression?</h2>"
        "<p>A letter such as %s stands for a number we do not know yet. It is called a <b>variable</b>. "
        "An <b>expression</b> uses numbers, letters and operations, like %s + 5 or 3%s.</p>"
        "<p>A number right in front of a letter means <b>multiply</b>: 3%s means 3 × %s. It never means 3 + %s.</p>" % (n, n, n, n, n, n) +
        table(["Words", "Expression"], [
            ["5 more than a number", "%s + 5" % n], ["7 less than a number", "%s %s 7" % (n, M)],
            ["3 times a number", "3" + n], ["a number divided by 4", "%s ÷ 4" % n],
            ["4 more than 3 times a number", "3%s + 4" % n]]) +
        "<h2>Evaluate an expression</h2>"
        "<p>To <b>evaluate</b>, put the number in place of the letter. Then multiply or divide before you add or subtract.</p>" +
        ex("Example 1", "Evaluate 3%s + 4 when %s = 6." % (n, n),
           "3 × 6 + 4 = 18 + 4 = 22.", "22") +
        "<h2>Solve an equation</h2>"
        "<p>An <b>equation</b> says two sides are equal, like a level pan balance. To <b>solve</b> it, find the number that makes both sides equal. "
        "Use the <b>opposite operation</b>, and do the same thing to both sides.</p>" +
        table(["Operation", "Undo it with"], [["+ 5", M + " 5"], [M + " 7", "+ 7"], ["× 3", "÷ 3"], ["÷ 4", "× 4"]]) +
        ex("Example 2", "Solve %s + 17 = 45." % n,
           "Subtract 17 from both sides: %s = 45 %s 17 = 28." % (n, M), "%s = 28" % n) +
        "<figure class='sn-fig'>" + bal +
        "<figcaption>2%s + 6 = 20. Take 6 off both pans: 2%s = 14. Each block is 14 ÷ 2 = 7.</figcaption></figure>" % (n, n) +
        "<h2>Check (verify) a solution</h2>"
        "<p>Put your answer back into the <b>original</b> equation. If both sides are equal, it is correct.</p>" +
        ex("Example 3", "Is %s = 7 a solution of 2%s + 6 = 20?" % (n, n),
           "2 × 7 + 6 = 14 + 6 = 20. Both sides are 20.", "Yes") +
        "<h2>Inequalities</h2>"
        "<p>An <b>inequality</b> uses &lt;, &gt;, ≤ or ≥. Solve it like an equation. The answer is a range of numbers. "
        "Show it on a number line.</p>" +
        ex("Example 4", "Solve %s + 6 &lt; 20 and graph the solution." % n,
           "Subtract 6 from both sides: %s &lt; 14. Check 13: 13 + 6 = 19, and 19 &lt; 20 is true. "
           "Check 14: 14 + 6 = 20, and 20 &lt; 20 is false." % n, "%s &lt; 14" % n) +
        "<figure class='sn-fig'>" + g1 +
        "<figcaption>%s &lt; 14: open circle at 14 (14 is not a solution), arrow to the left.</figcaption></figure>" % n +
        table(["Symbol", "Circle", "Arrow"], [
            ["&lt;", "open", "left"], ["≤", "closed (filled in)", "left"],
            ["&gt;", "open", "right"], ["≥", "closed (filled in)", "right"]]) +
        "<figure class='sn-fig'>" + g2 +
        "<figcaption>4%s ≥ 32 gives %s ≥ 8: closed circle at 8 (8 is a solution), arrow to the right.</figcaption></figure>" % (n, n) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Reading 3%s as 3 + %s" % (n, n), "3%s means 3 × %s" % (n, n)],
            ["With %s = 6, reading 3%s as 36" % (n, n), "3%s = 3 × 6 = 18" % n],
            ["Writing 7 %s %s for “7 less than %s”" % (M, n, n), "Start with the number: %s %s 7" % (n, M)],
            ["Adding 17 in %s + 17 = 45" % n, "Undo + 17 with %s 17" % M],
            ["Stopping at 2%s = 14" % n, "Finish: divide by 2 to get %s = 7" % n],
            ["A closed circle for &lt; or &gt;", "Closed circles are only for ≤ and ≥"],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about equations in the Ontario math curriculum?",
     "a": "In Grade 5 (Algebra, C2), students translate between words and algebraic expressions, evaluate expressions like 3n + 4, solve equations with whole numbers up to 100 and check the solutions. They also solve inequalities with one operation, like n + 6 < 20, and graph them on a number line."},
    {"q": "What does 3n mean in math?",
     "a": "3n means 3 × n. A number written right in front of a letter means multiply, so when n = 6, 3n is 18, not 9 and not 36."},
    {"q": "How do you solve an equation like n + 17 = 45?",
     "a": "Use the opposite operation on both sides. Subtract 17 to get n = 28, then check: 28 + 17 = 45."},
    {"q": "What is the difference between an equation and an inequality?",
     "a": "An equation has one answer that makes both sides equal, like n + 6 = 20 (n = 14). An inequality like n + 6 < 20 has many answers, so we graph them on a number line."},
]


def gen_unit():
    rnd = random.Random(45812)
    P = People(rnd)
    sets = [set_words_expr(rnd, P), set_evaluate(rnd, P), set_solve(rnd, P), set_check(rnd, P), set_ineq_words(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len({plain(c) for c in it["c"]}) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1
            assert "\\" not in it["q"] + "".join(it["c"]) + it["e"]
            k = plain(it["q"])
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-5", "slug": "expressions-equations-and-inequalities", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Expressions, Equations and Inequalities: Evaluate, Solve and Check",
        "seo_title": "Grade 5 Expressions, Equations and Inequalities Worksheets: Free Math with Answer Key (Ontario Curriculum)",
        "short_title": "Expressions, Equations and Inequalities",
        "domain": "Algebra",
        "standard_code": "Grade 5: C2.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Solve equations that involve whole numbers up to 100 in various contexts, and verify solutions",
        "meta_desc": "Free Grade 5 math worksheets on expressions, equations and inequalities for the Ontario curriculum: write expressions from words, evaluate 3n + 4 when n = 6, solve equations like n + 17 = 45, check solutions, and graph inequalities like n + 6 < 20. 100 questions with an answer key.",
        "key_big": "3n means 3 × n. To solve an equation, do the opposite operation to both sides.",
        "key_sub": "n + 17 = 45, so n = 45 − 17 = 28. Check by putting 28 back in: 28 + 17 = 45. Inequalities use the same steps: n + 6 < 20 gives n < 14.",
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
