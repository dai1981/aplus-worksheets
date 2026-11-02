# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 2 Math: Equality and Missing Numbers
(Ontario Curriculum, Grades 1–8: Mathematics, 2020 — Algebra C2.1, C2.2, C2.3)
  python3 tools/gen_caon_math_g2_equality.py
Pan balances and the = sign as “the same as”, true or false equations, missing numbers
(□ + 7 = 15, 30 = 18 + □), making both sides equal (20 + 5 = 15 + □) and word problems with a box.
Adding and subtracting to 100. Short sentences for 7- and 8-year-olds.
Wrong choices come from real mistakes: reading = as “the answer is” (20 + 5 = 15 + □ -> 25),
adding when the inverse is needed (□ + 7 = 15 -> 22), taking the smaller digit from the larger in
each column (30 − 18 -> 28), forgetting to regroup, changing the other number the wrong way and
counting on one too many or one too few.
Every answer is checked in code. HTML attributes use single quotes. Canadian English.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
GREY = "#e4e4e4"
INK = "#2b2b2b"
RED = "#c0392b"
BLUE = "#2e6da4"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
BOX = "□"
SYMS = "★▲"
WHAT = "<br>What number goes in the box?"


# ------------------------------------------------------------ equations
def tok(p):
    if isinstance(p, int):
        return str(p)
    if p == "?":
        return BOX
    return p


def plain(*parts):
    """Plain text equation: '?' becomes □."""
    return " ".join(tok(p) for p in parts)


def html(*parts):
    """Equation for question text: □ (or ★, ▲) in bold."""
    out = []
    for p in parts:
        t = tok(p)
        if t == BOX or t in SYMS:
            t = "<b>" + t + "</b>"
        out.append(t)
    return " ".join(out)


def val(expr):
    return eval(expr.replace("−", "-"), {"__builtins__": {}})


def holds(eq, ans=None):
    """'□ + 7 = 15' is true with the box = ans (a ★ or ▲ also counts as the unknown)."""
    s = re.sub(r"<[^>]+>", "", eq)
    if ans is not None:
        for u in BOX + SYMS:
            s = s.replace(u, str(ans))
    vals = [val(p.strip()) for p in s.split("=")]
    return all(v == vals[0] for v in vals)


def only(eq):
    """The one whole number 0-200 that makes eq true."""
    ok = [k for k in range(0, 201) if holds(eq, k)]
    assert len(ok) == 1, (eq, ok)
    return ok[0]


def sfl(a, b):
    """Smaller digit from larger digit in each column: 30 − 18 -> 28 (a typical mistake)."""
    da, db = str(a), str(b).rjust(len(str(a)), "0")
    return int("".join(str(abs(int(x) - int(y))) for x, y in zip(da, db)))


def nocarry(a, b):
    """Add column by column and drop the carried ten: 48 + 25 -> 63."""
    out, p = 0, 1
    while a or b:
        out += ((a % 10 + b % 10) % 10) * p
        a, b, p = a // 10, b // 10, p * 10
    return out


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if isinstance(c, int) and c <= 0:
            continue
        c = str(c)
        if c in seen or not c or c.startswith("-") or c.startswith("−") or c.startswith("0"):
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
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


class People:
    def __init__(self, rnd):
        self.pool = [(x, "she", "her") for x in GIRLS] + [(x, "he", "his") for x in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ pictures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


FS = 18
GAP = 7
BOXW = 22


def tok_w(t):
    return BOXW if t == BOX else len(t) * FS * 0.6


def expr_w(s):
    ts = s.split(" ")
    return sum(tok_w(t) for t in ts) + GAP * (len(ts) - 1)


def draw_expr(cx, base, s):
    """Draw 'a + □' centred at cx; □ is drawn as a red box."""
    ts = s.split(" ")
    x = cx - expr_w(s) / 2
    out = []
    for t in ts:
        w = tok_w(t)
        if t == BOX:
            out.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2.5'/>"
                       % (x, base - 16, BOXW, BOXW, RED))
        else:
            out.append(text(x + w / 2, base, t, FS))
        x += w + GAP
    return "".join(out)


def pan_svg(left, right):
    """A level pan balance with an expression on each pan."""
    def box_w(t):
        return max(90, int(expr_w(t) + 24))
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
        s.append(draw_expr(c, top + 25, t))
        s.append("<rect x='%.1f' y='%d' width='%d' height='6' fill='%s'/>" % (c - w / 2, py, w, INK))
        s.append("<rect x='%.1f' y='%d' width='4' height='18' fill='%s'/>" % (c - 2, py + 6, INK))
    by = py + 24
    s.append("<rect x='%.1f' y='%d' width='%.1f' height='6' fill='%s'/>" % (cl - 2, by, cr - cl + 4, INK))
    s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (mid, by + 6, mid - 22, by + 40, mid + 22, by + 40, GREEN))
    s.append("<rect x='%.1f' y='%d' width='80' height='5' fill='%s'/>" % (mid - 40, by + 40, INK))
    return svg_wrap(cr + wr / 2 + 8, by + 47, "".join(s),
                    "pan balance: %s on the left and %s on the right" % (left.replace(BOX, "box"), right.replace(BOX, "box")))


def dots_svg(left, right):
    """Pan balance with counters. left/right: lists of (count, colour). Level when both sides are equal,
    otherwise the heavier side goes down. Each group starts a new row of 5."""
    L = sum(k for k, _ in left)
    R = sum(k for k, _ in right)
    assert L <= 15 and R <= 15
    t = 0 if L == R else (10 if L > R else -10)
    rows = lambda groups: max(1, sum(math.ceil(k / 5) for k, _ in groups))
    RM = max(rows(left), rows(right))
    by = 43 + 18 * (RM - 1) + 10
    W, H = 300, by + 46
    s = ["<polygon points='150,%d 128,%d 172,%d' fill='%s'/>" % (by, by + 34, by + 34, INK),
         "<rect x='105' y='%d' width='90' height='7' rx='2' fill='%s'/>" % (by + 34, INK),
         "<line x1='66' y1='%.1f' x2='234' y2='%.1f' stroke='%s' stroke-width='5' stroke-linecap='round'/>"
         % (by + t * 0.8 * 84 / 78, by - t * 0.8 * 84 / 78, INK)]
    for cx, ey, groups in [(72, by + t * 0.8, left), (228, by - t * 0.8, right)]:
        py = ey - 10
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='3'/>" % (cx, ey, cx, py, INK))
        s.append("<path d='M %d %.1f L %d %.1f L %d %.1f L %d %.1f Z' fill='#e9eef2' stroke='%s' stroke-width='2.5'/>"
                 % (cx - 52, py - 3, cx + 52, py - 3, cx + 44, py + 3, cx - 44, py + 3, INK))
        r0 = 0
        for k, col in groups:
            for j in range(k):
                r, c = divmod(j, 5)
                s.append("<circle cx='%d' cy='%.1f' r='7' fill='%s'/>" % (cx - 36 + c * 18, py - 13 - 18 * (r0 + r), col))
            r0 += math.ceil(k / 5)
    lab = "balance with %s on the left and %s on the right" % (
        " and ".join("%d counters" % k for k, _ in left), " and ".join("%d counters" % k for k, _ in right))
    return svg_wrap(W, H, "".join(s), lab)


def bar_svg(whole, p1, p2):
    """Part-part-whole bar model, drawn to scale. Values are numbers or '?' (box)."""
    vals = [whole, p1, p2]
    nums = [v if isinstance(v, int) else None for v in vals]
    miss = [i for i, v in enumerate(nums) if v is None]
    assert len(miss) == 1
    full = list(nums)
    m = miss[0]
    full[m] = (nums[1] + nums[2]) if m == 0 else (nums[0] - (nums[2] if m == 1 else nums[1]))
    assert full[1] + full[2] == full[0] and min(full) > 0
    W, x0, h = 260, 8, 36
    w1 = round(W * full[1] / full[0])
    w1 = min(max(w1, 66), W - 66)
    s = []
    rows = [(8, [(x0, W, whole, FILL)]), (8 + h + 10, [(x0, w1, p1, "#fff"), (x0 + w1, W - w1, p2, "#fff")])]
    for y, cells in rows:
        for x, w, v, f in cells:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                     % (x, y, w, h, f, GREEN))
            s.append(draw_expr(x + w / 2, y + 25, tok(v)))
    lab = "bar model: whole %s, parts %s and %s" % tuple("box" if v == "?" else tok(v) for v in vals)
    return svg_wrap(W + 16, 8 + 2 * h + 10 + 8, "".join(s), lab)


def jump_svg(a, b):
    """Number line from a to b with one jump (an arc) from a to b marked with a box: a + □ = b."""
    assert b > a
    L, R, Y = 26, 286, 76
    X = lambda v: L + (v - a) * (R - L) / (b - a)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 16, Y, R + 16, Y, INK)]
    ticks = [a, b] + [v for v in range((a // 10 + 1) * 10, b, 10) if min(X(v) - X(a), X(b) - X(v)) >= 28]
    for v in sorted(set(ticks)):
        big = v in (a, b)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%d'/>"
                 % (X(v), Y - 8, X(v), Y + 8, INK, 3 if big else 2))
        s.append(text(X(v), Y + 28, str(v), 16 if big else 14, col=INK if big else "#555"))
    s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (X(a), Y - 6, (X(a) + X(b)) / 2, 6, X(b), Y - 6, GREEN))
    s.append("<path d='M%.1f %d l-9 -8 l2 10 Z' fill='%s'/>" % (X(b), Y - 6, GREEN))
    cx = (X(a) + X(b)) / 2
    s.append("<rect x='%.1f' y='%d' width='26' height='26' fill='#fff' stroke='%s' stroke-width='2.5'/>" % (cx - 13, 18, RED))
    return svg_wrap(R + 26, Y + 36, "".join(s), "number line: a jump from %d to %d" % (a, b))


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ============================================================ set 1: balances and = means "the same as"
def set_same_as(P):
    its = []
    Q1 = "The balance is level. Which equation matches?"
    # A. counters on a level balance
    for left, right, eq, wrongs in [
        ([(6, RED), (3, GREEN)], [(9, BLUE)], "6 + 3 = 9", ["6 + 3 = 10", "6 = 3 + 9", "9 + 3 = 6"]),
        ([(12, BLUE)], [(7, RED), (5, GREEN)], "12 = 7 + 5", ["12 = 7 + 6", "12 + 7 = 5", "7 = 12 + 5"]),
        ([(8, RED), (4, GREEN)], [(6, RED), (6, GREEN)], "8 + 4 = 6 + 6", ["8 + 4 = 6 + 7", "8 + 4 = 12 + 6", "8 + 6 = 4 + 6"]),
    ]:
        assert holds(eq) and not any(holds(w) for w in wrongs)
        assert val(eq.split(" = ")[0]) == sum(k for k, _ in left)
        l, r = eq.split(" = ")
        e = ("Count each side. The left side has %s. The right side has %s. Both sides are %d, so <b>%s</b>."
             % ("%s = %d" % (l, val(l)) if " " in l else l, "%s = %d" % (r, val(r)) if " " in r else r, val(l), eq))
        its.append(mcq(Q1 + fig(dots_svg(left, right)), eq, wrongs, e))
    # B. expressions on a level balance
    for l, r, wrongs in [("10 + 5", "8 + 7", ["10 + 5 = 8 + 8", "10 + 5 = 15 + 7", "10 + 7 = 8 + 5"]),
                         ("20", "12 + 8", ["20 = 12 + 9", "20 + 12 = 8", "12 = 20 + 8"])]:
        eq = l + " = " + r
        assert holds(eq) and not any(holds(w) for w in wrongs)
        e = ("The balance is level, so both sides are the same. %s = %d, so <b>%s</b>."
             % (r if " " in r else l, val(r), eq))
        if " " in l and " " in r:
            e = "%s = %d and %s = %d. Both sides are the same, so <b>%s</b>." % (l, val(l), r, val(r), eq)
        its.append(mcq(Q1 + fig(pan_svg(l, r)), eq, wrongs, e))
    # C. level balance with a box
    for l, r, ans, wr, e in [
        ("9 + 7", BOX, 16, [2, 15, 17], "The box is the same as 9 + 7. 9 + 7 = <b>16</b>. Not 2: that subtracts."),
        (BOX, "15 − 6", 9, [21, 8, 11], "The box is the same as 15 − 6. 15 − 6 = <b>9</b>. Not 21: that adds."),
        ("30 + 20", BOX, 50, [10, 5, 40], "3 tens + 2 tens = 5 tens. 30 + 20 = <b>50</b>. Not 5: 5 tens is 50. "
         "Not 10: that subtracts."),
        (BOX, "40 − 10", 30, [50, 3, 20], "4 tens − 1 ten = 3 tens. 40 − 10 = <b>30</b>. Not 50: that adds. "
         "Not 3: 3 tens is 30."),
    ]:
        assert val(l if l != BOX else r) == ans
        its.append(mcq("The balance is level." + WHAT + fig(pan_svg(l, r)), ans, wr, e))
    # D. a balance that is not level
    for a, b, k in [(5, 4, 6), (7, 6, 8), (9, 5, 10)]:
        S = a + b
        need = S - k
        e = ("The left side has %d + %d = %d. The right side has %d. Count on from %d to %d. "
             "You need <b>%d</b> more. Check: %d + %d = %d." % (a, b, S, k, k, S, need, k, need, S))
        its.append(mcq("The balance is not level. How many counters must go on the right to make it level?"
                       + fig(dots_svg([(a, RED), (b, GREEN)], [(k, BLUE)])), need, [S, need + 1, need - 1], e))
    # E. same value
    for ex_, right, wrongs in [
        ("6 + 6", "10 + 2", ["10 + 6", "6 + 7", "12 + 6"]),
        ("9 + 5", "10 + 4", ["10 + 5", "9 + 4", "14 + 5"]),
        ("20 + 30", "40 + 10", ["40 + 30", "20 + 20", "50 + 30"]),
        ("15 − 5", "5 + 5", ["15 + 5", "5 + 4", "10 + 5"]),
    ]:
        v = val(ex_)
        assert val(right) == v and all(val(w) != v for w in wrongs)
        e = "%s = %d and %s = %d. They are the same, so <b>%s = %s</b>." % (ex_, v, right, v, ex_, right)
        its.append(mcq("Which is the same as %s?" % ex_, right, wrongs, e))
    # F. meaning, = first, a mistake
    its.append(mcq("What does the = sign mean?", "is the same as",
                   ["the answer is next", "add the numbers", "is more than"],
                   "The = sign means <b>is the same as</b>. In 5 + 5 = 6 + 4, both sides are 10. "
                   "The answer does not always come next."))
    its.append(mcq(html("?", "=", 6, "+", 9) + WHAT, 15, [3, 14, 16],
                   "The = sign can come first. The box is the same as 6 + 9. 6 + 9 = <b>15</b>. Not 3: that subtracts."))
    assert sfl(18, 9) == 11
    its.append(mcq(html("?", "=", 18, "−", 9) + WHAT, 9, [27, 11, 8],
                   "The box is the same as 18 − 9. 18 − 9 = <b>9</b>. Not 27: that adds. "
                   "Not 11: you cannot take 9 from 8, so regroup."))
    nm, he, his = P.next()
    eq = plain(7, "+", 3, "=", "?", "+", 4)
    assert holds(eq, 6)
    its.append(mcq("%s writes 10 in the box. Is %s right?<br>%s" % (nm, he, html(7, "+", 3, "=", "?", "+", 4)),
                   "No, the box is 6", ["Yes, 7 + 3 is 10", "No, the box is 14", "No, the box is 3"],
                   "7 + 3 = 10, so the right side must be 10 too. □ + 4 = 10, so the box is <b>6</b>. "
                   "%s read = as “the answer is”. 10 + 4 is 14, not 10." % nm))
    assert len(its) == 20
    return {"title": "Balances: = means “the same as”", "items": its}


# ============================================================ set 2: true or false
def tf_item(eq, wrong):
    lhs, rhs = eq.split(" = ")
    a, b = val(lhs), val(rhs)
    parts = " ".join("%s = %d." % (x, val(x)) for x in (lhs, rhs) if x != str(val(x)))
    if a == b:
        right = "True. Both sides are %d." % a
        e = (parts + " " if parts else "") + "Both sides are %d, so it is <b>true</b>." % a
    else:
        right = "False. %d is not %d." % (a, b)
        e = (parts + " " if parts else "") + "%d and %d are not the same, so it is <b>false</b>." % (a, b)
    for w in wrong:
        assert w != right
    return mcq("True or false?<br>%s" % eq, right, wrong, e)


def set_true_false():
    its = []
    its.append(tf_item("15 = 15", ["False. There is no + or −.", "False. The answer goes last.", "True. Both sides are 30."]))
    its.append(tf_item("14 = 9 + 5", ["False. The answer goes last.", "False. 9 + 5 is 13.", "True. Both sides are 13."]))
    its.append(tf_item("8 + 5 = 12", ["True. Both sides are 12.", "True. 8 + 5 is 12.", "False. 13 is not 14."]))
    its.append(tf_item("7 + 6 = 6 + 7", ["False. The order is not the same.", "False. 13 is not 14.", "True. Both sides are 14."]))
    its.append(tf_item("12 − 4 = 7", ["True. Both sides are 7.", "True. 12 − 4 is 7.", "False. 8 is not 6."]))
    its.append(tf_item("9 + 4 = 10 + 3", ["False. 9 is not 10.", "False. 13 is not 14.", "True. Both sides are 14."]))
    its.append(tf_item("30 + 20 = 50 + 10", ["True. 30 + 20 is 50.", "True. Both sides are 60.", "False. 50 is not 70."]))
    its.append(tf_item("16 − 8 = 4 + 4", ["False. One is − and one is +.", "False. 8 is not 9.", "True. Both sides are 12."]))
    its.append(tf_item("40 + 5 = 45 + 5", ["True. 40 + 5 is 45.", "True. Both sides are 50.", "False. 45 is not 55."]))
    its.append(tf_item("25 + 10 = 30 + 5", ["False. 25 is not 30.", "False. 35 is not 40.", "True. Both sides are 40."]))
    its.append(tf_item("50 − 20 = 20 + 10", ["False. One is − and one is +.", "False. 30 is not 40.", "True. Both sides are 70."]))
    its.append(tf_item("18 + 7 = 25 − 5", ["True. 18 + 7 is 25.", "True. Both sides are 25.", "False. 25 is not 30."]))
    its.append(tf_item("60 = 35 + 25", ["False. The answer goes last.", "False. 35 + 25 is 50.", "True. Both sides are 50."]))
    its.append(tf_item("47 + 3 = 40 + 7", ["True. Both have 4 tens.", "True. Both sides are 47.", "False. 50 is not 57."]))
    # which is true?
    pt = iter(["Which equation is true?", "Work out both sides. Which equation is true?",
               "Which one is true? Check both sides."])
    for right, wrong in [("10 = 4 + 6", ["10 = 4 + 5", "4 = 10 + 6", "10 + 4 = 6"]),
                         ("8 + 9 = 9 + 8", ["8 + 9 = 9 + 9", "8 + 9 = 18", "17 = 8 + 8"]),
                         ("20 + 6 = 30 − 4", ["20 + 6 = 30 + 4", "20 + 6 = 30", "20 + 6 = 26 + 4"])]:
        assert holds(right) and not any(holds(w) for w in wrong), right
        l, r = right.split(" = ")
        e = ("Work out both sides. In <b>%s</b>, both sides are %d, so it is true. The other three have sides that "
             "are not the same." % (right, val(l)))
        its.append(mcq(next(pt), right, wrong, e))
    # which is false?
    pf = iter(["Which equation is false?", "Work out both sides. Which equation is false?",
               "Which one is false? Check both sides."])
    for right, wrong in [("6 + 7 = 14", ["6 + 7 = 13", "13 = 7 + 6", "6 + 7 = 10 + 3"]),
                         ("20 + 4 = 24 + 4", ["20 + 4 = 24", "24 = 20 + 4", "20 + 4 = 4 + 20"]),
                         ("35 − 5 = 20 + 5", ["35 − 5 = 30", "30 = 35 − 5", "35 − 5 = 20 + 10"])]:
        assert not holds(right) and all(holds(w) for w in wrong), right
        l, r = right.split(" = ")
        parts = " ".join("%s = %d." % (x, val(x)) for x in (l, r) if x != str(val(x)))
        e = "%s %d is not %d, so <b>%s</b> is false. The other three are true." % (parts, val(l), val(r), right)
        its.append(mcq(next(pf), right, wrong, e))
    assert len(its) == 20
    return {"title": "True or false equations", "items": its}


# ============================================================ set 3: missing numbers
def set_missing():
    its = []

    def add(parts, cands, e, pic=None, q=None):
        eq = plain(*parts)
        ans = only(eq)
        sym = [p for p in parts if isinstance(p, str) and p in SYMS]
        if sym:
            q = (q or html(*parts) + "<br>What number is %s?" % sym[0])
        else:
            q = (q or html(*parts) + WHAT)
        if pic:
            q += fig(pic)
        e = e.replace("ANS", "<b>%d</b>" % ans)
        its.append(mcq(q, ans, cands, e))
        return ans

    def part_add(first, a, s, pic=None):
        """□ + a = s (first=True) or a + □ = s."""
        ans = s - a
        parts = ["?", "+", a, "=", s] if first else [a, "+", "?", "=", s]
        e = ("Think: what adds to %d to make %d? Count on from %d to %d, or subtract: %d − %d = ANS. "
             "Check: %s. Not %d: that adds." % (a, s, a, s, s, a,
                                                plain(*[ans if p == "?" else p for p in parts]), s + a))
        if sfl(s, a) != ans:
            e += " Not %d: regroup a ten, do not take the smaller digit from the larger." % sfl(s, a)
        add(parts, [s + a, sfl(s, a), ans + 1, ans - 1, ans + 10, ans - 10], e,
            pic(a, s) if pic else None)

    part_add(True, 7, 15, lambda a, s: bar_svg(s, "?", a))
    part_add(False, 6, 14)
    add([13, "−", "?", "=", 5], [18, 7, 9],
        "13 take away what leaves 5? 13 − 5 = ANS. Check: 13 − 8 = 5. Not 18: that adds.")
    add(["?", "−", 6, "=", 9], [3, 14, 16],
        "The box is the number you start with. Undo − 6 by adding: 9 + 6 = ANS. Check: 15 − 6 = 9. "
        "Not 3: that subtracts.", bar_svg("?", 9, 6))
    add([30, "=", 18, "+", "?"], [48, 28, 13],
        "The = sign can come first. 18 + □ = 30. Count on: 18 to 20 is 2, 20 to 30 is 10. 2 + 10 = ANS. "
        "Not 48: that adds. Not 28: that takes the smaller digit from the larger.", jump_svg(18, 30))
    assert sfl(30, 18) == 28
    add(["★", "+", 6, "=", 13], [19, 6, 8],
        "The ★ is a symbol for a number we do not know. It works like a box. 13 − 6 = ANS. Check: 7 + 6 = 13. "
        "Not 19: that adds.")
    add([20, "+", "?", "=", 50], [70, 3, 20],
        "Count on by tens from 20: 30, 40, 50. That is 3 tens, or ANS. Not 3: 3 tens is 30. Not 70: that adds.",
        jump_svg(20, 50))
    its.append(mcq("In " + html(9, "+", "?", "=", 15) + ", what does the box stand for?",
                   "a number we do not know", ["the answer, 15", "add the numbers", "zero"],
                   "The box stands for <b>a number we do not know</b> yet. Here it is 6, because 9 + 6 = 15. "
                   "The answer to 9 + □ is 15, but the box itself is not 15."))
    part_add(False, 25, 40, lambda a, s: jump_svg(a, s))
    add([45, "=", "?", "+", 20], [65, 35, 24],
        "□ + 20 = 45. Take away 2 tens: 45 − 20 = ANS. Check: 25 + 20 = 45. Not 65: that adds. "
        "Not 35: that takes away only 1 ten.")
    add([70, "−", "?", "=", 40], [110, 3, 20],
        "70 take away what leaves 40? 7 tens − 4 tens = 3 tens = ANS. Check: 70 − 30 = 40. "
        "Not 110: that adds. Not 3: 3 tens is 30.")
    add(["?", "−", 20, "=", 35], [15, 45, 65],
        "The box is the number you start with. Undo − 20 by adding: 35 + 20 = ANS. Check: 55 − 20 = 35. "
        "Not 15: that subtracts.", bar_svg("?", 35, 20))
    add([20, "−", "▲", "=", 12], [32, 12, 7],
        "The ▲ is a symbol for a number we do not know. 20 take away what leaves 12? 20 − 12 = ANS. "
        "Check: 20 − 8 = 12. Not 32: that adds. Not 12: 12 is what is left, not what was taken away.")
    part_add(False, 36, 50, lambda a, s: jump_svg(a, s))
    part_add(True, 28, 60, lambda a, s: bar_svg(s, "?", a))
    add([80, "=", 52, "+", "?"], [132, 32, 38],
        "52 + □ = 80. Count on: 52 to 60 is 8, 60 to 80 is 20. 8 + 20 = ANS. Not 132: that adds. "
        "Not 32: that takes the smaller digit from the larger.", jump_svg(52, 80))
    assert sfl(80, 52) == 32
    add([64, "−", "?", "=", 30], [94, 35, 44],
        "64 take away what leaves 30? 64 − 30 = ANS. Check: 64 − 34 = 30. Not 94: that adds.")
    add([90, "−", "?", "=", 45], [135, 55, 35],
        "90 take away what leaves 45? 90 − 45 = ANS. Check: 45 + 45 = 90. Not 135: that adds. Not 55: that takes the smaller digit from the larger.",
        bar_svg(90, 45, "?"))
    assert sfl(90, 45) == 55
    assert nocarry(48, 25) == 63
    add(["?", "−", 25, "=", 48], [23, 63, 83],
        "Undo − 25 by adding: 48 + 25 = ANS. 8 + 5 = 13, so regroup a ten. Check: 73 − 25 = 48. "
        "Not 23: that subtracts. Not 63: that forgets the regrouped ten.")
    add([100, "=", "?", "+", 65], [165, 45, 25],
        "□ + 65 = 100. Count on: 65 to 70 is 5, 70 to 100 is 30. 5 + 30 = ANS. Not 165: that adds. "
        "Not 45: that counts 4 tens instead of 3.", bar_svg(100, "?", 65))
    assert len(its) == 20
    return {"title": "Find the missing number", "items": its}


# ============================================================ set 4: make both sides equal
def set_equal_sides():
    its = []

    def add(parts, cands, e, pic=False, q=None):
        eq = plain(*parts)
        ans = only(eq)
        if q is None:
            q = html(*parts) + WHAT
            if pic:
                l, r = eq.split(" = ")
                q = "The balance is level." + WHAT + fig(pan_svg(l, r))
        its.append(mcq(q, ans, cands, e.replace("ANS", "<b>%d</b>" % ans)))

    def ab_c(a, b, c, pic=False):
        """a + b = c + □"""
        S = a + b
        ans = S - c
        d = a - c
        wrong_way = b - d   # changes b the wrong way
        e = "Work out the side you know: %d + %d = %d. So %d + □ = %d, and □ = %d − %d = ANS. " % (a, b, S, c, S, S, c)
        e += "Not %d: that is the left side, not the box. Not %d: that adds %d and %d." % (S, S + c, S, c)
        if wrong_way > 0:
            e += " Not %d: %d is %s than %d, so the box must be %s than %d." % (
                wrong_way, c, "more" if c > a else "less", a, "less" if c > a else "more", b)
        add([a, "+", b, "=", c, "+", "?"], [S, wrong_way, S + c, ans + 1, ans - 1], e, pic)

    ab_c(5, 4, 3, True)
    ab_c(8, 2, 6)
    ab_c(7, 6, 10, True)
    ab_c(9, 5, 10)
    ab_c(20, 5, 15, True)
    ab_c(30, 20, 40)
    ab_c(12, 8, 10, True)
    ab_c(25, 10, 20)
    ab_c(40, 15, 50, True)
    ab_c(35, 20, 30)
    add(["?", "+", 6, "=", 4, "+", 9], [13, 11, 19, 8],
        "The right side is 4 + 9 = 13. So □ + 6 = 13, and □ = 13 − 6 = ANS. Not 13: that is the right side. "
        "Not 19: that adds 13 and 6.")
    add(["?", "+", 10, "=", 30, "+", 15], [45, 55, 25],
        "The right side is 30 + 15 = 45. So □ + 10 = 45, and □ = 45 − 10 = ANS. Not 45: that is the right side. "
        "Not 55: that adds 10 instead of taking it away.", True)
    add([15, "−", 5, "=", 12, "−", "?"], [10, 8, 22],
        "The left side is 15 − 5 = 10. So 12 − □ = 10, and □ = 12 − 10 = ANS. Not 10: that is the left side.")
    add([20, "−", 4, "=", 18, "−", "?"], [16, 6, 4],
        "The left side is 20 − 4 = 16. So 18 − □ = 16, and □ = 18 − 16 = ANS. Not 16: that is the left side. "
        "Not 4: 18 is less than 20, so take away less than 4.")
    add([10, "+", 10, "=", 25, "−", "?"], [20, 45, 15],
        "The left side is 10 + 10 = 20. So 25 − □ = 20, and □ = 25 − 20 = ANS. Not 20: that is the left side. "
        "Not 45: that adds.")
    add([50, "−", 10, "=", 30, "+", "?"], [40, 70, 20],
        "The left side is 50 − 10 = 40. So 30 + □ = 40, and □ = 40 − 30 = ANS. Not 40: that is the left side. "
        "Not 70: that adds 30 and 40.")
    # C2.2: what must be added / subtracted
    for parts, cands, e in [
        ([20, "+", 4, "+", "?", "=", 30], [24, 10, 54],
         "20 + 4 = 24. Count on from 24 to 30: ANS. So add 6. Not 24: that is 20 + 4. Not 10: that forgets the 4."),
        ([15, "+", 10, "+", "?", "=", 20, "+", 20], [40, 25, 5],
         "The right side is 20 + 20 = 40. The left side has 15 + 10 = 25. 40 − 25 = ANS. So add 15. "
         "Not 40: that is the right side. Not 5: that only compares 15 and 20."),
        ([30, "+", 15, "−", "?", "=", 40], [45, 10, 85],
         "30 + 15 = 45. To get from 45 down to 40, take away ANS. Not 45: that is the left side. "
         "Not 10: that only compares 30 and 40."),
        ([50, "−", 10, "−", "?", "=", 30], [40, 20, 70],
         "50 − 10 = 40. To get from 40 down to 30, take away ANS. Not 40: that is 50 − 10. "
         "Not 20: that is 50 − 30 and forgets the − 10."),
    ]:
        eq = plain(*parts)
        what = "added to" if "+ " + BOX in eq else "taken away from"
        left = eq.split(" = ")[0].rsplit(" ", 2)[0]
        q = "What number must be %s %s to make both sides equal?<br>%s" % (what, left, html(*parts))
        add(parts, cands, e, q=q)
    assert len(its) == 20
    return {"title": "Make both sides equal", "items": its}


# ============================================================ set 5: word problems with a box
def set_words(P):
    its = []

    def match(q, right, wrongs, e):
        if BOX not in right:
            assert holds(right) and not any(holds(w) for w in wrongs)
            its.append(mcq(q, right, wrongs, e))
            return
        ans = only(right)
        for w in wrongs:
            assert not holds(w, ans), w
        its.append(mcq(q, right, wrongs, e.replace("ANS", str(ans))))

    def solve(q, parts, cands, e, unit="", bar=None, jump=None):
        eq = plain(*parts)
        ans = only(eq)
        f = lambda v: "%d%s" % (v, unit)
        q = q + (fig(bar_svg(*bar)) if bar else "") + (fig(jump_svg(*jump)) if jump else "")
        its.append(mcq(q, f(ans), [f(c) for c in cands if c > 0],
                       "%s. %s" % (html(*parts), e.replace("ANS", "<b>%s</b>" % f(ans)))))

    # 1, 2
    nm, he, his = P.next()
    match("%s has 8 hockey cards. %s gets some more. Now %s has 15. Which equation matches?" % (nm, cap(he), he),
          plain(8, "+", "?", "=", 15), [plain(8, "+", 15, "=", "?"), plain(15, "+", "?", "=", 8), plain("?", "−", 8, "=", 15)],
          "%s starts with 8, gets some more and ends with 15: <b>8 + □ = 15</b>. The box is ANS." % nm)
    solve("%s has 8 hockey cards. %s gets some more. Now %s has 15. How many cards did %s get?" % (nm, cap(he), he, he),
          [8, "+", "?", "=", 15], [23, 8, 6], "Count on from 8 to 15, or 15 − 8 = ANS. Not 23: that adds.")
    # 3
    nm, he, his = P.next()
    solve("%s picks 27 apples at the orchard. %s wants 40 apples. How many more does %s need to pick?" % (nm, cap(he), he),
          [27, "+", "?", "=", 40], [67, 23, 14],
          "Count on: 27 to 30 is 3, 30 to 40 is 10. 3 + 10 = ANS. Not 67: that adds. Not 23: when you regroup, 4 tens becomes 3 tens.",
          jump=(27, 40))
    # 4
    solve("There are 30 Canada geese on a pond. Some fly away. Now 12 are left. How many flew away?",
          [30, "−", "?", "=", 12], [42, 22, 17],
          "30 − 12 = ANS. Check: 30 − 18 = 12. Not 42: that adds. Not 22: that takes the smaller digit from the larger.",
          bar=(30, 12, "?"))
    assert sfl(30, 12) == 22
    # 5, 6
    match("There are some loons on a lake. 7 more loons land. Now there are 19. Which equation matches?",
          plain("?", "+", 7, "=", 19), [plain(19, "+", 7, "=", "?"), plain(7, "−", "?", "=", 19), plain("?", "−", 7, "=", 19)],
          "Some loons (the box), plus 7 more, make 19: <b>□ + 7 = 19</b>. The box is ANS.")
    solve("There are some loons on a lake. 7 more loons land. Now there are 19. How many loons were there at first?",
          ["?", "+", 7, "=", 19], [26, 13, 11], "19 − 7 = ANS. Check: 12 + 7 = 19. Not 26: that adds.")
    # 7
    solve("There are 26 students in gym class. 14 are on the red team. The rest are on the blue team. "
          "How many are on the blue team?",
          [14, "+", "?", "=", 26], [40, 13, 11], "26 − 14 = ANS. Check: 14 + 12 = 26. Not 40: that adds.",
          bar=(26, 14, "?"))
    # 8
    nm, he, his = P.next()
    solve("The school bus takes students to the skating rink. At one stop, 9 students get off. Now 16 are on the bus. "
          "How many were on the bus before the stop?",
          ["?", "−", 9, "=", 16], [7, 15, 24],
          "Undo − 9 by adding: 16 + 9 = ANS. Check: 25 − 9 = 16. Not 7: that subtracts. Not 15: that forgets the regrouped ten.")
    assert nocarry(16, 9) == 15
    # 9
    nm, he, his = P.next()
    solve("%s has 50¢. %s buys a freezie for 35¢. How much money does %s have left?" % (nm, cap(he), he),
          [35, "+", "?", "=", 50], [85, 25, 20],
          "Count on from 35¢ to 50¢: 5¢ to 40¢, then 10¢ to 50¢. 5¢ + 10¢ = ANS. Not 85¢: that adds. "
          "Not 25¢: that takes the smaller digit from the larger.", unit="¢")
    assert sfl(50, 35) == 25
    # 10
    solve("A Grade 2 class runs laps for the Terry Fox Run. The goal is 60 laps. They run 35 laps. "
          "How many more laps do they need?",
          [35, "+", "?", "=", 60], [95, 35, 24],
          "Count on: 35 to 40 is 5, 40 to 60 is 20. 5 + 20 = ANS. Not 95: that adds. "
          "Not 35: that takes the smaller digit from the larger.", jump=(35, 60))
    # 11
    solve("A sugar shack has 45 bottles of maple syrup. It sells some. Now 20 are left. How many did it sell?",
          [45, "−", "?", "=", 20], [65, 20, 35],
          "45 − 20 = ANS. Check: 45 − 25 = 20. Not 65: that adds. Not 20: 20 is what is left.",
          bar=(45, 20, "?"))
    # 12
    nm1, he1, his1 = P.next()
    nm2, he2, his2 = P.next()
    match("%s has 20 red blocks and 5 blue blocks. %s has 15 blocks. %s wants the same number as %s. "
          "Which equation shows how many more blocks %s needs?" % (nm1, nm2, nm2, nm1, nm2),
          plain(20, "+", 5, "=", 15, "+", "?"),
          [plain(20, "+", 5, "=", "?"), plain(20, "+", 15, "=", 5, "+", "?"), plain(15, "+", 5, "=", 20, "+", "?")],
          "The two totals must be the same: <b>20 + 5 = 15 + □</b>. 20 + 5 = 25, so the box is ANS.")
    # 13
    nm1, he1, his1 = P.next()
    nm2, he2, his2 = P.next()
    solve("%s has 10 stickers and gets 6 more. %s has 12 stickers. How many more does %s need to have the same number as %s?"
          % (nm1, nm2, nm2, nm1),
          [10, "+", 6, "=", 12, "+", "?"], [16, 8, 28],
          "10 + 6 = 16. So 12 + □ = 16, and the box is ANS. Not 16: that is %s’s total. "
          "Not 8: 12 is more than 10, so %s needs fewer than 6." % (nm1, nm2))
    # 14
    solve("The school library has 70 books on a shelf. 38 are in English. The rest are in French. "
          "How many are in French?",
          [38, "+", "?", "=", 70], [108, 48, 42],
          "70 − 38 = ANS. Count on: 38 to 40 is 2, 40 to 70 is 30. Not 108: that adds. "
          "Not 48: that takes the smaller digit from the larger.", bar=(70, 38, "?"))
    assert sfl(70, 38) == 48
    # 15
    nm, he, his = P.next()
    solve("%s’s family needs 36 buns for Thanksgiving dinner. They have 18. How many more do they need?" % nm,
          [18, "+", "?", "=", 36], [54, 22, 17],
          "36 − 18 = ANS. Check: 18 + 18 = 36. Not 54: that adds. Not 22: that takes the smaller digit from the larger.")
    assert sfl(36, 18) == 22
    # 16
    nm, he, his = P.next()
    solve("%s’s family drives 90 km to the cottage. They stop for lunch after 55 km. How far do they still have to drive?" % nm,
          [55, "+", "?", "=", 90], [145, 45, 25],
          "Count on: 55 to 60 is 5, 60 to 90 is 30. 5 + 30 = ANS. Not 145: that adds. "
          "Not 45: that takes the smaller digit from the larger.", unit=" km", jump=(55, 90))
    assert sfl(90, 55) == 45
    # 17
    nm, he, his = P.next()
    match("%s works out 52 − 18 = 34. Which equation can %s use to check %s answer?" % (nm, he, his),
          "34 + 18 = 52", ["52 + 18 = 34", "34 − 18 = 52", "52 + 34 = 18"],
          "Check a subtraction with addition. Add the answer and the number taken away: "
          "<b>34 + 18 = 52</b>. It is true, so 34 is right.")
    # 18
    solve("The school wants to collect 100 cans for the food bank. It has 65 cans. How many more cans does it need?",
          [65, "+", "?", "=", 100], [165, 45, 25],
          "Count on: 65 to 70 is 5, 70 to 100 is 30. 5 + 30 = ANS. Not 165: that adds. "
          "Not 45: that counts 4 tens instead of 3.", bar=(100, 65, "?"))
    # 19
    solve("A Grade 2 class has 23 students. On a snow day, only 15 come to school. How many stay home?",
          [15, "+", "?", "=", 23], [38, 12, 7],
          "Count on: 15 to 20 is 5, 20 to 23 is 3. 5 + 3 = ANS. Not 38: that adds. "
          "Not 12: that takes the smaller digit from the larger.")
    assert sfl(23, 15) == 12
    # 20
    nm1, he1, his1 = P.next()
    nm2, he2, his2 = P.next()
    solve("%s has 30 red beads and 25 blue beads. %s has 40 beads. How many more beads does %s need to have the same number as %s?"
          % (nm1, nm2, nm2, nm1),
          [30, "+", 25, "=", 40, "+", "?"], [55, 35, 95],
          "30 + 25 = 55. So 40 + □ = 55, and the box is ANS. Not 55: that is %s’s total. "
          "Not 35: 40 is more than 30, so %s needs fewer than 25." % (nm1, nm2))
    assert len(its) == 20
    return {"title": "Word problems with a box", "items": its}


# ============================================================ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    return (
        "<h2>The = sign means “the same as”</h2>"
        "<p>An <b>equation</b> has an = sign. The = sign means both sides are the <b>same</b>. "
        "Think of a balance. When both sides are the same, it is level.</p>"
        "<figure class='sn-fig'>" + pan_svg("8 + 6", "10 + 4") +
        "<figcaption>8 + 6 = 14 and 10 + 4 = 14. The balance is level, so 8 + 6 = 10 + 4.</figcaption></figure>"
        "<p>An equation is <b>true</b> when both sides are the same. 9 + 4 = 10 + 3 is true. "
        "9 + 4 = 13 + 3 is false, because 13 + 3 is 16.</p>"
        "<h2>Find the missing number</h2>"
        "<p>A box □ stands for a number we do not know. A symbol like ★ works the same way. "
        "Count on, or use subtraction. Then put your number in the box to check.</p>"
        "<figure class='sn-fig'>" + jump_svg(18, 30) +
        "<figcaption>18 + □ = 30. Count on: 18 to 20 is 2, 20 to 30 is 10. The box is 12.</figcaption></figure>" +
        table(["Equation", "Do this", "Box"], [
            [html("?", "+", 7, "=", 15), "15 − 7", "8"],
            [html(30, "=", 18, "+", "?"), "count on from 18 to 30", "12"],
            [html(13, "−", "?", "=", 5), "13 − 5", "8"],
            [html("?", "−", 6, "=", 9), "9 + 6", "15"],
        ]) +
        ex("Example", html("?", "−", 6, "=", 9),
           "The box is the number you start with. Undo − 6 by adding: 9 + 6 = 15. Check: 15 − 6 = 9.", "15") +
        "<h2>Make both sides equal</h2>"
        "<p>Work out the side you know first. Then find what the other side needs.</p>"
        "<figure class='sn-fig'>" + pan_svg("20 + 5", "15 + " + BOX) +
        "<figcaption>20 + 5 = 25, so 15 + □ must be 25 too. The box is 10.</figcaption></figure>" +
        ex("Example", html(20, "+", 5, "=", 15, "+", "?"),
           "The left side is 20 + 5 = 25. So 15 + □ = 25. 25 − 15 = 10.", "10") +
        ex("Example", "What must be added to 20 + 4 to make 30?",
           "20 + 4 = 24. Count on from 24 to 30: 6.", "6") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["20 + 5 = 15 + □, so □ = 25", "25 is the left side. 15 + □ = 25, so □ = 10"],
            ["7 + 3 = □ + 4, so □ = 10", "The = sign is not “the answer is”. □ + 4 = 10, so □ = 6"],
            ["□ + 7 = 15, so □ = 22 (15 + 7)", "Subtract: 15 − 7 = 8"],
            ["□ − 6 = 9, so □ = 3 (9 − 6)", "Undo − 6 by adding: 9 + 6 = 15"],
            ["30 − 18 = 28 (smaller digit from larger)", "Count on: 18 to 20 is 2, 20 to 30 is 10. 30 − 18 = 12"],
        ])
    )


FAQ = [
    {"q": "What does the equal sign mean in Grade 2 math?",
     "a": "The equal sign means “is the same as”, not “the answer is”. In 20 + 5 = 15 + □, both sides must be 25, so the box is 10, not 25."},
    {"q": "How do you find the missing number in □ + 7 = 15?",
     "a": "Count on from 7 to 15, or subtract: 15 − 7 = 8. Then check by putting 8 in the box: 8 + 7 = 15."},
    {"q": "What is equality in the Grade 2 Ontario math curriculum?",
     "a": "In the Algebra strand (C2.1 to C2.3), Grade 2 students use symbols for unknown numbers, find what to add or take away to make two expressions equal, and show equal relationships with numbers up to 100."},
    {"q": "How can I help my child with true or false equations at home?",
     "a": "Write an equation like 9 + 4 = 10 + 3 and ask your child to work out each side. If both sides are the same number, it is true. A kitchen scale or a toy balance shows the idea well."},
]


def gen_unit():
    rnd = random.Random(42809)
    P = People(rnd)
    sets = [set_same_as(P), set_true_false(), set_missing(), set_equal_sides(), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-2", "slug": "equality-and-missing-numbers", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 2 Equality and Missing Numbers",
        "seo_title": "Grade 2 Equality and Missing Numbers Worksheets: Free Math with Answer Key (Ontario Curriculum)",
        "short_title": "Equality and Missing Numbers",
        "domain": "Algebra",
        "standard_code": "Grade 2: C2.2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Determine what needs to be added to or subtracted from addition and subtraction expressions to make them equivalent",
        "meta_desc": "Free Grade 2 math worksheets on equality for the Ontario curriculum: balances and the equal sign, true or false equations, missing numbers like □ + 7 = 15, making both sides equal and word problems. 100 questions with an answer key.",
        "key_big": "The equal sign means “is the same as”. Both sides of an equation must be the same.",
        "key_sub": "□ + 7 = 15, so □ = 15 − 7 = 8. In 20 + 5 = 15 + □, the left side is 25, so □ = 10, not 25.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "bar model|pan balance|number line")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
