# -*- coding: utf-8 -*-
"""
British Columbia Grade 2 Math: Equality and Inequality (=, ≠, < and >)
(BC Mathematics Curriculum, Grade 2 — Patterning: symbolic representation of equality and inequality)
  python3 tools/gen_cabc_math_g2_equality.py
Balances and the = and ≠ signs, comparing numbers to 100 with < and > (the open side faces the bigger
number), true or false number sentences, missing numbers that make both sides balance (□ + 8 = 14,
6 + 7 = 10 + □) and word problems in BC contexts. Short sentences for 7- and 8-year-olds.
Wrong choices come from real mistakes: mixing up < and >, reading the sentence backwards, comparing the
ones before the tens (42 and 37 -> 37 is bigger), reading = as “the answer is” (6 + 7 = 10 + □ -> 13),
adding when the inverse is needed, taking the smaller digit from the larger (40 − 25 -> 25), forgetting to
regroup and changing the other number the wrong way.
Every answer is checked in code. HTML attributes use single quotes. Canadian English.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
GREY = "#e4e4e4"
INK = "#2b2b2b"
RED = "#c0392b"
BLUE = "#2e6da4"
FONT = "Arial, Helvetica, sans-serif"
BOX = "□"
SYMS = "★▲"
WHAT = "<br>What number goes in the box?"
LT, GT, NE = "&lt;", "&gt;", "≠"


# ------------------------------------------------------------ number sentences
def tok(p):
    if isinstance(p, int):
        return str(p)
    if p == "?":
        return BOX
    return p


def plain(*parts):
    """Plain text sentence: '?' becomes □."""
    return " ".join(tok(p) for p in parts)


def html(*parts):
    """Sentence for question text: □ in bold."""
    out = []
    for p in parts:
        t = tok(p)
        if t == BOX or t in SYMS:
            t = "<b>" + t + "</b>"
        out.append(t)
    return " ".join(out)


def val(expr):
    expr = expr.replace("¢", "").strip()
    assert re.fullmatch(r"[0-9 +−]+", expr), expr
    return eval(expr.replace("−", "-"), {"__builtins__": {}})


OPS = {"=": lambda a, b: a == b, "≠": lambda a, b: a != b, "<": lambda a, b: a < b, ">": lambda a, b: a > b}


def split(s):
    """'9 + 6 &gt; 14' -> ('9 + 6', '>', '14')"""
    s = re.sub(r"<[^>]+>", "", s).replace("&lt;", "<").replace("&gt;", ">")
    found = [op for op in OPS if (" %s " % op) in s]
    assert len(found) == 1, s
    l, r = s.split(" %s " % found[0])
    return l, found[0], r


def holds(s, ans=None):
    """Is the number sentence true (with the box = ans)?"""
    if ans is not None:
        for u in BOX + SYMS:
            s = s.replace(u, str(ans))
    l, op, r = split(s)
    return OPS[op](val(l), val(r))


def only(eq):
    """The one whole number 0-200 that makes eq true."""
    ok = [k for k in range(0, 201) if holds(eq, k)]
    assert len(ok) == 1, (eq, ok)
    return ok[0]


def sfl(a, b):
    """Smaller digit from larger digit in each column: 40 − 25 -> 25 (a typical mistake)."""
    da, db = str(a), str(b).rjust(len(str(a)), "0")
    return int("".join(str(abs(int(x) - int(y))) for x, y in zip(da, db)))


def nocarry(a, b):
    """Add column by column and drop the carried ten: 47 + 15 -> 52."""
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
        if c in seen or not c:
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



def blocks_svg(a, b):
    """Base ten blocks for a (left) and b (right): tens rods and ones cubes, drawn to the numbers."""
    C, G = 8, 4
    top = 8
    rod_h = 10 * C

    def group(x0, v):
        t, o = divmod(v, 10)
        s, x = [], x0
        for _ in range(t):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, top, C, rod_h, FILL, GREEN))
            for k in range(1, 10):
                s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.8'/>"
                         % (x, top + k * C, x + C, top + k * C, GREEN))
            x += C + G
        if o:
            x += 4
            cols = math.ceil(o / 5)
            for j in range(o):
                c, r = divmod(j, 5)
                s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='1.5'/>"
                         % (x + c * (C + 3), top + rod_h - (r + 1) * (C + 3) + 3, C, C, BLUE))
            x += cols * (C + 3) - 3
        else:
            x -= G
        return s, x - x0

    sa, wa = group(0, a)
    sb, wb = group(0, b)
    wa, wb = max(wa, 30), max(wb, 30)
    xa = 10
    xb = xa + wa + 50
    W = xb + wb + 10
    s = ["<g transform='translate(%d 0)'>%s</g>" % (xa, "".join(group(0, a)[0])),
         "<g transform='translate(%d 0)'>%s</g>" % (xb, "".join(group(0, b)[0])),
         text(xa + wa / 2, top + rod_h + 24, str(a), 18), text(xb + wb / 2, top + rod_h + 24, str(b), 18)]
    return svg_wrap(W, top + rod_h + 32, "".join(s), "base ten blocks: %d on the left and %d on the right" % (a, b))


def say(op):
    return {"=": "is equal to", "≠": "is not equal to", "<": "is less than", ">": "is greater than"}[op]


def H(s):
    return s.replace("<", "&lt;").replace(">", "&gt;")


# ============================================================ set 1: = and ≠
def set_eq_ne():
    its = []
    Q1 = "Which number sentence matches the balance?"
    for left, right, sent, wrongs, e in [
        ([(6, RED), (4, GREEN)], [(10, BLUE)], "6 + 4 = 10", ["6 + 4 ≠ 10", "6 + 4 = 11", "10 ≠ 6 + 4"],
         "The left side has 6 + 4 = 10. The right side has 10. The balance is level, so <b>6 + 4 = 10</b>."),
        ([(7, RED), (5, GREEN)], [(9, BLUE)], "7 + 5 ≠ 9", ["7 + 5 = 9", "7 + 5 ≠ 12", "7 + 5 = 10"],
         "The left side has 7 + 5 = 12. The right side has 9. 12 is not 9, and the balance is not level, so <b>7 + 5 ≠ 9</b>."),
        ([(8, BLUE)], [(3, RED), (5, GREEN)], "8 = 3 + 5", ["8 ≠ 3 + 5", "8 = 3 + 6", "3 = 8 + 5"],
         "The left side has 8. The right side has 3 + 5 = 8. The balance is level, so <b>8 = 3 + 5</b>."),
        ([(4, RED), (4, GREEN)], [(6, RED), (3, GREEN)], "4 + 4 ≠ 6 + 3", ["4 + 4 = 6 + 3", "4 + 4 ≠ 6 + 2", "4 + 4 = 6 + 4"],
         "The left side has 4 + 4 = 8. The right side has 6 + 3 = 9. 8 is not 9, and the heavier side goes down, "
         "so <b>4 + 4 ≠ 6 + 3</b>."),
    ]:
        assert holds(sent) and not any(holds(w) for w in wrongs), sent
        l, op, r = split(sent)
        assert val(l) == sum(k for k, _ in left) and val(r) == sum(k for k, _ in right)
        its.append(mcq(Q1 + fig(dots_svg(left, right)), sent, wrongs, e))

    # which sign, and why
    for s, right, wrongs, e in [
        ("9 + 6 ? 15", "=, both are 15", ["≠, 9 + 6 is 14", "≠, the sides look different", "=, both are 16"],
         "9 + 6 = 15. The right side is 15 too. Both sides are the same, so use =: <b>9 + 6 = 15</b>."),
        ("8 + 5 ? 12", "≠, 13 is not 12", ["=, 8 + 5 is 12", "=, both are 13", "≠, 8 + 5 is 14"],
         "8 + 5 = 13. 13 is not 12, so use ≠: <b>8 + 5 ≠ 12</b>."),
        ("10 ? 4 + 6", "=, both are 10", ["≠, the answer goes last", "≠, 4 + 6 is 11", "=, both are 11"],
         "4 + 6 = 10. Both sides are 10, so use =: <b>10 = 4 + 6</b>. The answer does not have to go last."),
        ("7 + 7 ? 10 + 4", "=, both are 14", ["≠, 7 is not 10", "≠, 14 is not 15", "=, both are 15"],
         "7 + 7 = 14 and 10 + 4 = 14. Both sides are 14, so use =: <b>7 + 7 = 10 + 4</b>."),
        ("20 + 30 ? 60", "≠, 50 is not 60", ["=, 20 + 30 is 60", "=, both are 50", "≠, 20 + 30 is 40"],
         "2 tens + 3 tens = 5 tens, so 20 + 30 = 50. 50 is not 60, so use ≠: <b>20 + 30 ≠ 60</b>."),
        ("15 − 5 ? 5 + 5", "=, both are 10", ["≠, one is − and one is +", "≠, 10 is not 11", "=, both are 20"],
         "15 − 5 = 10 and 5 + 5 = 10. Both sides are 10, so use =: <b>15 − 5 = 5 + 5</b>. "
         "The signs + and − can be different."),
    ]:
        sign = right.split(",")[0]
        assert holds(s.replace("?", sign))
        for w in wrongs:
            if w.split(",")[0] != sign:
                assert not holds(s.replace("?", w.split(",")[0])), (s, w)
        its.append(mcq("Which sign goes in the box? Why?<br>" + s.replace("?", "<b>" + BOX + "</b>"), right, wrongs, e))

    # which is true / false
    qt = iter(["Which number sentence is true?", "Work out each side. Which one is true?",
               "Which one is true? Check both sides."])
    for right, wrongs, e in [
        ("5 + 3 ≠ 7", ["5 + 3 ≠ 8", "5 + 3 = 7", "8 ≠ 3 + 5"],
         "5 + 3 = 8. 8 is not 7, so <b>5 + 3 ≠ 7</b> is true. 5 + 3 ≠ 8 is false, because both sides are 8."),
        ("12 = 6 + 6", ["12 ≠ 6 + 6", "12 = 6 + 7", "6 = 12 + 6"],
         "6 + 6 = 12. Both sides are 12, so <b>12 = 6 + 6</b> is true. 6 + 7 is 13, not 12."),
        ("40 + 10 ≠ 40", ["40 + 10 = 40", "40 + 10 ≠ 50", "50 ≠ 10 + 40"],
         "40 + 10 = 50. 50 is not 40, so <b>40 + 10 ≠ 40</b> is true. 40 + 10 ≠ 50 is false, because both sides are 50."),
    ]:
        assert holds(right) and not any(holds(w) for w in wrongs)
        its.append(mcq(next(qt), right, wrongs, e))
    qf = iter(["Which number sentence is false?", "Work out each side. Which one is false?",
               "Which one is false? Check both sides."])
    for right, trues, e in [
        ("9 + 9 = 19", ["9 + 9 = 18", "9 + 9 ≠ 19", "18 = 9 + 9"],
         "9 + 9 = 18, not 19. So <b>9 + 9 = 19</b> is false. It should be 9 + 9 ≠ 19."),
        ("30 ≠ 10 + 20", ["30 = 10 + 20", "30 ≠ 10 + 10", "30 = 20 + 10"],
         "10 + 20 = 30. Both sides are 30, so <b>30 ≠ 10 + 20</b> is false. It should be 30 = 10 + 20."),
        ("16 − 8 = 9", ["16 − 8 ≠ 9", "16 − 8 = 8", "16 − 8 = 4 + 4"],
         "16 − 8 = 8, not 9. So <b>16 − 8 = 9</b> is false."),
    ]:
        assert not holds(right) and all(holds(w) for w in trues)
        its.append(mcq(next(qf), right, trues, e))

    its.append(mcq("What does the ≠ sign mean?", "is not equal to",
                   ["is equal to", "the answer is", "take away"],
                   "≠ means <b>is not equal to</b>. The two sides are not the same. 5 + 2 ≠ 8, because 7 is not 8."))
    its.append(mcq("What does the = sign mean?", "is the same as",
                   ["the answer is next", "is not the same as", "add the numbers"],
                   "= means <b>is the same as</b>. In 6 + 4 = 5 + 5, both sides are 10. "
                   "The answer does not always come next."))
    assert holds("6 + 4 ≠ 10 + 2")
    its.append(mcq("Kai writes 6 + 4 = 10 + 2. Is he right?", "No. 10 is not 12.",
                   ["Yes. 6 + 4 is 10.", "Yes. Both sides are 12.", "No. 6 + 4 is 11."],
                   "6 + 4 = 10, but 10 + 2 = 12. 10 is not 12, so the sentence should be <b>6 + 4 ≠ 10 + 2</b>. "
                   "Kai read = as “the answer is”."))
    assert holds("3 + 5 = 5 + 3")
    its.append(mcq("Zara writes 3 + 5 ≠ 5 + 3. Is she right?", "No. Both sides are 8.",
                   ["Yes. The order is not the same.", "Yes. 3 is not 5.", "No. 3 + 5 is 9."],
                   "3 + 5 = 8 and 5 + 3 = 8. Both sides are the same, so it should be <b>3 + 5 = 5 + 3</b>. "
                   "Changing the order does not change the total."))
    assert len(its) == 20
    return {"title": "Equal (=) and not equal (≠)", "items": its}


# ============================================================ set 2: < and >
def set_lt_gt():
    its = []
    its.append(mcq("The signs &lt; and &gt; have an open side. Which number does the open side face?",
                   "the bigger number", ["the smaller number", "the first number", "the answer"],
                   "The open side always faces <b>the bigger number</b>. In 9 &gt; 4, it faces 9. In 4 &lt; 9, it faces 9 too."))
    its.append(mcq("What does 35 &gt; 28 mean?", "35 is greater than 28",
                   ["35 is less than 28", "35 is equal to 28", "28 is greater than 35"],
                   "Read from left to right. &gt; means “is greater than”. So 35 &gt; 28 means <b>35 is greater than 28</b>. "
                   "The open side faces 35."))
    its.append(mcq("What does 19 &lt; 40 mean?", "19 is less than 40",
                   ["19 is greater than 40", "40 is less than 19", "19 is the same as 40"],
                   "Read from left to right. &lt; means “is less than”. So 19 &lt; 40 means <b>19 is less than 40</b>. "
                   "The open side faces 40."))
    # base ten blocks
    for a, b in [(42, 37), (25, 52), (63, 36), (54, 59), (30, 27)]:
        op = "<" if a < b else ">"
        bad = ">" if op == "<" else "<"
        right = H("%d %s %d" % (a, op, b))
        wrongs = [H("%d %s %d" % (a, bad, b)), H("%d %s %d" % (b, op, a)), "%d = %d" % (a, b)]
        assert holds(right) and not any(holds(w) for w in wrongs)
        ta, tb = a // 10, b // 10
        big, small = max(a, b), min(a, b)
        if ta != tb:
            why = "%d has %d tens. %d has %d tens. %d tens is more, so %d is greater." % (a, ta, b, tb, max(ta, tb), big)
        else:
            why = ("Both have %d tens. Look at the ones: %d has %d and %d has %d. So %d is greater."
                   % (ta, a, a % 10, b, b % 10, big))
        e = why + " The open side faces %d: <b>%s</b>." % (big, right)
        if a % 10 > b % 10 and a < b or a % 10 < b % 10 and a > b:
            e += " Look at the tens first, not the ones."
        its.append(mcq("Which is true?" + fig(blocks_svg(a, b)), right, wrongs, e))
    # which sign and why
    for s, right, wrongs, e in [
        ("8 + 7 ? 14", "&gt;, 15 is more than 14", ["&lt;, 14 is less than 15", "=, 8 + 7 is 14", "&lt;, 8 is less than 14"],
         "8 + 7 = 15. 15 is greater than 14. The open side faces 15: <b>8 + 7 &gt; 14</b>."),
        ("56 ? 65", "&lt;, 56 is less than 65", ["&gt;, 65 is more than 56", "&gt;, 6 ones is more than 5", "=, the digits are the same"],
         "56 has 5 tens. 65 has 6 tens. So 56 is less than 65. The open side faces 65: <b>56 &lt; 65</b>."),
        ("30 + 40 ? 70", "=, both are 70", ["&lt;, 30 is less than 70", "&gt;, 30 + 40 is 80", "&gt;, 40 is more than 30"],
         "3 tens + 4 tens = 7 tens, so 30 + 40 = 70. Both sides are 70: <b>30 + 40 = 70</b>."),
        ("50 − 20 ? 20 + 20", "&lt;, 30 is less than 40", ["&gt;, 40 is more than 30", "&gt;, 50 is more than 20", "&gt;, 50 − 20 is 70"],
         "50 − 20 = 30 and 20 + 20 = 40. 30 is less than 40. The open side faces 40: <b>50 − 20 &lt; 20 + 20</b>."),
        ("9 + 9 ? 20 − 1", "&lt;, 18 is less than 19", ["&gt;, 19 is more than 18", "=, both are 19", "&gt;, 20 is more than 9"],
         "9 + 9 = 18 and 20 − 1 = 19. 18 is less than 19. The open side faces 19: <b>9 + 9 &lt; 20 − 1</b>."),
    ]:
        sign = right.split(",")[0]
        assert holds(s.replace("?", sign)), s
        for w in wrongs:
            if w.split(",")[0] != sign:
                assert not holds(s.replace("?", w.split(",")[0])), (s, w)
        its.append(mcq("Which sign goes in the box? Why?<br>" + s.replace("?", "<b>" + BOX + "</b>"), right, wrongs, e))
    # which is true
    q2 = iter(["Which one is true? Look at the signs.", "Which one is true? Work out the sum first."])
    for right, wrongs, e in [
        ("48 &lt; 84", ["57 &gt; 75", "62 &lt; 26", "39 &gt; 93"],
         "48 has 4 tens and 84 has 8 tens, so <b>48 &lt; 84</b>. The others face the wrong way: 57 &lt; 75, 62 &gt; 26, 39 &lt; 93."),
        ("66 = 60 + 6", ["66 &gt; 60 + 6", "66 &lt; 6 + 6", "66 = 6 + 6"],
         "60 + 6 = 66. Both sides are 66, so <b>66 = 60 + 6</b>. 6 + 6 is only 12."),
    ]:
        assert holds(right) and not any(holds(w) for w in wrongs)
        its.append(mcq(next(q2), right, wrongs, e))
    # which number makes it true
    for s, ans, wr, e in [
        ("? &gt; 58", 61, [58, 49, 55],
         "□ &gt; 58 means the box is greater than 58. 61 has 6 tens, so <b>61</b> &gt; 58. "
         "Not 58: 58 is equal to 58, not greater. Not 49: 4 tens is less than 5 tens."),
        ("27 &lt; ?", 30, [27, 25, 18],
         "27 &lt; □ means the box is greater than 27. <b>30</b> is greater than 27. "
         "Not 18: look at the tens first. 1 ten is less than 2 tens."),
        ("? &lt; 40", 38, [40, 41, 50],
         "□ &lt; 40 means the box is less than 40. <b>38</b> has 3 tens, so it is less than 40. "
         "Not 40: 40 is equal to 40, not less."),
    ]:
        assert holds(s.replace("?", BOX), ans) and not any(holds(s.replace("?", BOX), w) for w in wr), s
        its.append(mcq("Which number makes this true?<br>" + s.replace("?", "<b>" + BOX + "</b>"), ans, wr, e))
    # mistakes
    assert holds("23 > 19")
    its.append(mcq("Ryan writes 23 &lt; 19. Is he right?", "No. 23 &gt; 19.",
                   ["Yes. 3 is less than 9.", "Yes. 23 is less.", "No. 23 = 19."],
                   "Look at the tens first. 23 has 2 tens and 19 has 1 ten, so 23 is greater: <b>23 &gt; 19</b>. "
                   "Ryan looked at the ones."))
    assert holds("15 + 5 = 20")
    its.append(mcq("Leah writes 15 + 5 &gt; 20. Is she right?", "No. 15 + 5 = 20.",
                   ["Yes. 15 + 5 is 21.", "Yes. 20 is greater.", "No. 15 + 5 &lt; 20."],
                   "15 + 5 = 20. Both sides are 20, so the right sign is =: <b>15 + 5 = 20</b>."))
    assert len(its) == 20
    return {"title": "Greater than (>) and less than (<)", "items": its}


# ============================================================ set 3: true or false
def tf_right(sent):
    l, op, r = split(sent)
    a, b = val(l), val(r)
    if OPS[op](a, b):
        word = {"=": "Both sides are %d." % a, "≠": "%d is not %d." % (a, b),
                "<": "%d is less than %d." % (a, b), ">": "%d is greater than %d." % (a, b)}[op]
        return "True. " + word, True
    if a == b:
        return "False. Both sides are %d." % a, False
    word = {"=": "%d is not %d." % (a, b), "<": "%d is not less than %d." % (a, b),
            ">": "%d is not greater than %d." % (a, b)}[op]
    return "False. " + word, False


def tf_item(sent, wrongs):
    right, ok = tf_right(sent)
    for w in wrongs:
        assert w != right
    l, op, r = split(sent)
    a, b = val(l), val(r)
    work = " ".join("%s = %d." % (x, val(x)) for x in (l, r) if x != str(val(x)))
    if a == b:
        rel = "Both sides are %d." % a
    elif op in "=≠":
        rel = "%d is not %d." % (a, b)
    else:
        rel = "%d %s %d." % (a, "is less than" if a < b else "is greater than", b)
    e = (work + " " if work else "") + rel + " So <b>%s</b> is <b>%s</b>." % (H(sent), "true" if ok else "false")
    return mcq("True or false?<br>" + H(sent), H(right), [H(w) for w in wrongs], e)


def set_true_false():
    its = []
    for sent, wrongs in [
        ("9 + 4 = 13", ["True. Both sides are 14.", "False. 9 + 4 is 12.", "False. 9 is not 13."]),
        ("15 = 8 + 7", ["False. The answer goes last.", "False. 8 + 7 is 14.", "True. Both sides are 16."]),
        ("6 + 6 ≠ 12", ["True. 6 + 6 is 13.", "True. The sides look different.", "False. 12 is not 13."]),
        ("7 + 5 ≠ 11", ["False. 7 + 5 is 11.", "False. Both sides are 12.", "True. 13 is not 11."]),
        ("24 > 42", ["True. 4 ones is more than 2 ones.", "True. 24 is less than 42.", "False. 24 is equal to 42."]),
        ("36 < 63", ["False. 6 ones is more than 3 ones.", "False. 36 is greater than 63.", "True. 36 is equal to 63."]),
        ("8 + 8 > 15", ["False. 8 + 8 is 15.", "False. 8 is less than 15.", "False. 16 is less than 15."]),
        ("10 + 3 < 12", ["True. 10 is less than 12.", "True. 3 is less than 12.", "False. Both sides are 12."]),
        ("20 + 20 = 30 + 10", ["False. 20 is not 30.", "False. 40 is not 30.", "True. Both sides are 50."]),
        ("14 − 7 < 8", ["False. 14 is greater than 8.", "False. 14 − 7 is 8.", "False. 7 is greater than 8."]),
        ("50 + 5 ≠ 55", ["True. The sides look different.", "True. 55 is not 50.", "False. 50 + 5 is 60."]),
        ("45 > 40 + 6", ["True. 45 is greater than 40.", "True. 45 is greater than 6.", "False. Both sides are 45."]),
        ("30 − 10 = 10 + 10", ["False. One is − and one is +.", "False. 40 is not 20.", "True. Both sides are 40."]),
        ("17 + 3 < 30", ["False. 17 + 3 is 30.", "False. 20 is greater than 30.", "False. 20 is equal to 30."]),
        ("60 > 59", ["False. 9 ones is more than 0 ones.", "False. 60 is less than 59.", "True. 59 is greater than 60."]),
        ("40 + 30 = 80 − 10", ["False. One is + and one is −.", "False. 70 is not 90.", "True. Both sides are 80."]),
        ("25 + 25 > 50", ["True. 25 + 25 is 60.", "True. 50 is greater than 25.", "False. 50 is less than 50."]),
        ("72 − 2 ≠ 70", ["True. 72 − 2 is 52.", "True. 72 is not 70.", "False. 72 − 2 is 74."]),
    ]:
        its.append(tf_item(sent, wrongs))
    right, wrongs = "35 + 5 > 39", ["35 + 5 < 39", "35 + 5 = 39", "35 + 5 ≠ 40"]
    assert holds(right) and not any(holds(w) for w in wrongs)
    its.append(mcq("Which number sentence is true? Find the sum first.", H(right), [H(w) for w in wrongs],
                   "35 + 5 = 40. 40 is greater than 39, so <b>35 + 5 &gt; 39</b> is true. "
                   "35 + 5 ≠ 40 is false, because both sides are 40."))
    right, trues = "18 < 9 + 9", ["18 = 9 + 9", "18 > 9 + 8", "18 ≠ 9 + 8"]
    assert not holds(right) and all(holds(w) for w in trues)
    its.append(mcq("Which number sentence is false? Find the sums first.", H(right), [H(w) for w in trues],
                   "9 + 9 = 18. Both sides are 18, so <b>18 &lt; 9 + 9</b> is false. 9 + 8 = 17, and 18 is greater than 17, "
                   "so the other three are true."))
    assert len(its) == 20
    return {"title": "True or false number sentences", "items": its}


# ============================================================ set 4: missing numbers to balance
def set_missing():
    its = []

    def add(parts, cands, e, pic=None, level=False):
        eq = plain(*parts)
        ans = only(eq)
        for c in cands:
            assert c != ans and not holds(eq, c), (eq, c)
        if level:
            l, r = eq.split(" = ")
            q = "The balance is level." + WHAT + fig(pan_svg(l, r))
        else:
            q = html(*parts) + WHAT + (fig(pic) if pic else "")
        its.append(mcq(q, ans, cands, e.replace("ANS", "<b>%d</b>" % ans)))

    add([8, "+", 5, "=", "?"], [3, 12, 14],
        "The box is the same as 8 + 5. 8 + 5 = ANS. Not 3: that subtracts.", level=True)
    assert sfl(16, 7) == 11
    add(["?", "=", 16, "−", 7], [23, 11, 8],
        "The box is the same as 16 − 7. 16 − 7 = ANS. Not 23: that adds. "
        "Not 11: you cannot take 7 from 6, so regroup a ten.", level=True)
    add([6, "+", 7, "=", 10, "+", "?"], [13, 23, 4],
        "The left side is 6 + 7 = 13. So 10 + □ must be 13 too. 13 − 10 = ANS. "
        "Not 13: that is the left side, not the box. = does not mean “the answer is”.", level=True)
    add([9, "+", 6, "=", "?", "+", 5], [15, 20, 11],
        "The left side is 9 + 6 = 15. So □ + 5 = 15. 15 − 5 = ANS. Not 15: that is the left side. "
        "Not 20: that adds 15 and 5.", level=True)
    add([20, "+", 30, "=", 40, "+", "?"], [50, 90, 20],
        "The left side is 20 + 30 = 50. So 40 + □ = 50. 50 − 40 = ANS. Not 50: that is the left side. "
        "Not 90: that adds 50 and 40.", level=True)
    add([15, "+", 10, "=", "?", "+", 20], [25, 45, 15],
        "The left side is 15 + 10 = 25. So □ + 20 = 25. 25 − 20 = ANS. Not 25: that is the left side. "
        "Not 15: 20 is more than 10, so the box must be less than 15.", level=True)
    add(["?", "+", 8, "=", 14], [22, 7, 5],
        "What adds to 8 to make 14? 14 − 8 = ANS. Check: 6 + 8 = 14. Not 22: that adds.")
    assert sfl(17, 9) == 12
    add([9, "+", "?", "=", 17], [26, 12, 9],
        "Count on from 9 to 17: 1 to make 10, then 7 more. 1 + 7 = ANS. Check: 9 + 8 = 17. "
        "Not 26: that adds. Not 12: that takes the smaller digit from the larger.")
    assert sfl(40, 25) == 25
    add([40, "=", 25, "+", "?"], [65, 25, 14],
        "The = sign can come first. 25 + □ = 40. Count on: 25 to 30 is 5, 30 to 40 is 10. 5 + 10 = ANS. "
        "Not 65: that adds. Not 25: that takes the smaller digit from the larger.", jump_svg(25, 40))
    add([12, "+", 4, "=", "?", "+", 6], [16, 14, 22],
        "The left side is 12 + 4 = 16. So □ + 6 = 16. 16 − 6 = ANS. Not 16: that is the left side. "
        "Not 14: 6 is 2 more than 4, so the box must be 2 less than 12, not 2 more.")
    add([30, "+", 15, "=", 35, "+", "?"], [45, 80, 20],
        "The left side is 30 + 15 = 45. So 35 + □ = 45. 45 − 35 = ANS. Not 45: that is the left side. "
        "Not 20: 35 is more than 30, so the box must be less than 15.")
    add(["?", "+", 25, "=", 20, "+", 30], [50, 75, 5],
        "The right side is 20 + 30 = 50. So □ + 25 = 50. 50 − 25 = ANS. Not 50: that is the right side. "
        "Not 75: that adds 50 and 25.")
    add([18, "−", 8, "=", 15, "−", "?"], [10, 25, 11],
        "The left side is 18 − 8 = 10. So 15 − □ = 10. 15 − 10 = ANS. Not 10: that is the left side. "
        "Not 11: 15 is less than 18, so take away less than 8.")
    add([50, "−", 20, "=", 40, "−", "?"], [30, 70, 20],
        "The left side is 50 − 20 = 30. So 40 − □ = 30. 40 − 30 = ANS. Not 30: that is the left side. "
        "Not 70: that adds 40 and 30.")
    add([45, "+", 5, "=", 60, "−", "?"], [50, 110, 15],
        "The left side is 45 + 5 = 50. So 60 − □ = 50. 60 − 50 = ANS. Not 50: that is the left side. "
        "Not 110: that adds 60 and 50.")
    assert sfl(70, 36) == 46
    add([70, "=", "?", "+", 36], [106, 46, 33],
        "□ + 36 = 70. Count on: 36 to 40 is 4, 40 to 70 is 30. 4 + 30 = ANS. Not 106: that adds. "
        "Not 46: that takes the smaller digit from the larger.", jump_svg(36, 70))
    add([63, "−", "?", "=", 40], [103, 40, 24],
        "63 take away what leaves 40? 63 − 40 = ANS. Check: 63 − 23 = 40. Not 103: that adds. "
        "Not 40: 40 is what is left, not what was taken away.")
    assert nocarry(47, 15) == 52
    add(["?", "−", 15, "=", 47], [32, 52, 63],
        "The box is the number you start with. Undo − 15 by adding: 47 + 15 = ANS. 7 + 5 = 12, so regroup a ten. "
        "Check: 62 − 15 = 47. Not 32: that subtracts. Not 52: that forgets the regrouped ten.", bar_svg("?", 47, 15))
    add([25, "+", 25, "=", 30, "+", "?"], [50, 80, 30],
        "The left side is 25 + 25 = 50. So 30 + □ = 50. 50 − 30 = ANS. Not 50: that is the left side. "
        "Not 30: 30 is 5 more than 25, so the box must be 5 less than 25.")
    add([100, "=", 58, "+", "?"], [158, 52, 43],
        "58 + □ = 100. Count on: 58 to 60 is 2, 60 to 100 is 40. 2 + 40 = ANS. Not 158: that adds. "
        "Not 52: from 60 to 100 is 4 tens, not 5 tens.", bar_svg(100, 58, "?"))
    assert len(its) == 20
    return {"title": "Missing numbers that balance", "items": its}


# ============================================================ set 5: word problems
def set_words():
    its = []

    def pick(q, right, wrongs, e, check=True):
        if check:
            assert holds(right) and not any(holds(w) for w in wrongs), right
        its.append(mcq(q, H(right), [H(w) for w in wrongs], e))

    def solve(q, parts, cands, e, unit="", pic=None):
        eq = plain(*parts)
        ans = only(eq)
        for c in cands:
            assert not holds(eq, c)
        f = lambda v: "%d%s" % (v, unit)
        its.append(mcq(q + (fig(pic) if pic else ""), f(ans), [f(c) for c in cands],
                       "%s. %s" % (html(*parts), e.replace("ANS", "<b>%s</b>" % f(ans)))))

    # 1
    pick("Liam has 34 hockey cards. Ava has 43 hockey cards. Which is true?" + fig(blocks_svg(34, 43)),
         "34 < 43", ["34 > 43", "43 < 34", "34 = 43"],
         "34 has 3 tens. 43 has 4 tens. So Liam has fewer cards: <b>34 &lt; 43</b>. The open side faces 43.")
    # 2
    pick("At the beach, Mei finds 18 shells. Owen finds 9 shells in the morning and 9 in the afternoon. Which is true?",
         "18 = 9 + 9", ["18 ≠ 9 + 9", "18 > 9 + 9", "18 < 9 + 9"],
         "Owen finds 9 + 9 = 18 shells. Mei finds 18. They are the same: <b>18 = 9 + 9</b>.")
    # 3
    its.append(mcq("A BC Ferries boat has 46 cars on the top deck and 64 cars on the lower deck. "
                   "Which deck has more cars?",
                   "lower deck: 64 &gt; 46", ["top deck: 46 &gt; 64", "top deck: 6 &gt; 4", "same: 46 = 64"],
                   "64 has 6 tens. 46 has 4 tens. So <b>64 &gt; 46</b>. The lower deck has more cars."))
    assert holds("64 > 46") and not holds("46 > 64") and not holds("46 = 64")
    # 4
    pick("On Monday, the class sees 52 salmon in the river. On Tuesday, they see 25 salmon. Which is true?",
         "52 > 25", ["52 < 25", "25 > 52", "52 = 25"],
         "52 has 5 tens. 25 has 2 tens. More salmon on Monday: <b>52 &gt; 25</b>. The open side faces 52.")
    # 5
    assert sfl(24, 15) == 11
    solve("Chloe has 15 stickers. She gets some more. Now she has 24. How many stickers did she get?",
          [15, "+", "?", "=", 24], [39, 11, 8],
          "Count on: 15 to 20 is 5, 20 to 24 is 4. 5 + 4 = ANS. Not 39: that adds. "
          "Not 11: that takes the smaller digit from the larger.", pic=bar_svg(24, 15, "?"))
    # 6
    pick("Arjun reads 8 books in March and 6 books in April. Nadia reads 15 books. Which is true?",
         "8 + 6 ≠ 15", ["8 + 6 = 15", "8 + 6 > 15", "8 + 6 ≠ 14"],
         "Arjun reads 8 + 6 = 14 books. 14 is not 15: <b>8 + 6 ≠ 15</b>.")
    # 7
    assert 12 + 9 == 21
    its.append(mcq("A whale-watching boat sees 12 orcas in the morning and 9 orcas in the afternoon. "
                   "Another boat sees 20 orcas. Which boat sees more orcas?",
                   "the first boat: 21 &gt; 20", ["the other boat: 20 &gt; 12", "the other boat: 20 &gt; 19",
                                                  "the same: both see 20"],
                   "The first boat sees 12 + 9 = 21 orcas. <b>21 &gt; 20</b>, so the first boat sees more. "
                   "Add both times before you compare."))
    # 8
    assert 3 * 10 + 5 == 35 and holds("35 < 40")
    its.append(mcq("Hana has 3 dimes and 1 nickel. A freezie costs 40¢. Does she have enough money?",
                   "No. 35¢ &lt; 40¢", ["Yes. 35¢ &gt; 40¢", "Yes. 4 coins is 40¢", "No. 30¢ &lt; 40¢"],
                   "3 dimes are 30¢. 1 nickel is 5¢. 30¢ + 5¢ = 35¢. <b>35¢ &lt; 40¢</b>, so she does not have enough. "
                   "Count the value, not the number of coins."))
    # 9
    solve("Ethan has 20 red blocks and 6 blue blocks. Sofia has 16 blocks. "
          "How many more blocks does Sofia need to have the same number as Ethan?",
          [20, "+", 6, "=", 16, "+", "?"], [26, 42, 2],
          "Ethan has 20 + 6 = 26. So 16 + □ = 26, and the box is ANS. Not 26: that is Ethan’s total. "
          "Not 42: that adds 26 and 16.")
    # 10
    assert sfl(50, 35) == 25
    solve("A Grade 2 class runs laps for the Terry Fox Run. The goal is 50 laps. They have run 35 laps. "
          "How many more laps do they need?",
          [35, "+", "?", "=", 50], [85, 25, 14],
          "Count on: 35 to 40 is 5, 40 to 50 is 10. 5 + 10 = ANS. Not 85: that adds. "
          "Not 25: that takes the smaller digit from the larger.", pic=jump_svg(35, 50))
    # 11
    solve("A SkyTrain car has 48 people. At a station, some people get off. Now 30 people are on the car. "
          "How many got off?",
          [48, "−", "?", "=", 30], [78, 30, 17],
          "48 − 30 = ANS. Check: 48 − 18 = 30. Not 78: that adds. Not 30: 30 is how many are left.",
          pic=bar_svg(48, 30, "?"))
    # 12
    solve("In one year, Nanaimo has 20 rainy days in November and 5 rainy days in July. "
          "How many more rainy days are in November?",
          [5, "+", "?", "=", 20], [25, 14, 16],
          "Count on from 5 to 20, or 20 − 5 = ANS. Not 25: that adds.", unit=" days")
    # 13
    pick("Simran picks 27 apples at an orchard in Kelowna. She wants 40 apples. "
         "Which number sentence shows how many more she needs?",
         "27 + □ = 40", ["27 + 40 = □", "40 + □ = 27", "□ − 27 = 40"],
         "She starts with 27, picks some more (the box) and ends with 40: <b>27 + □ = 40</b>. The box is 13.",
         check=False)
    assert only("27 + □ = 40") == 13 and not any(holds(w, 13) for w in ["27 + 40 = □", "40 + □ = 27", "□ − 27 = 40"])
    # 14
    assert all(45 < v < 50 for v in [47]) and not any(45 < v < 50 for v in [45, 50, 54])
    its.append(mcq("Jasleen has more than 45 beads and fewer than 50 beads. How many beads could she have?", "47",
                   ["45", "50", "54"],
                   "The number must be &gt; 45 and &lt; 50. <b>47</b> works: 47 &gt; 45 and 47 &lt; 50. "
                   "Not 45 or 50: they are equal, not more or fewer. Not 54: 54 &gt; 50."))
    # 15
    assert 12 + 9 == 21 and holds("22 > 21")
    its.append(mcq("Kai skis down Grouse Mountain 12 times on Saturday and 9 times on Sunday. "
                   "Leah skis down 22 times. Who skis down more times?",
                   "Leah: 22 &gt; 21", ["Kai: 21 &gt; 22", "the same: both are 22", "Kai: 12 &gt; 9"],
                   "Kai skis 12 + 9 = 21 times. <b>22 &gt; 21</b>, so Leah skis more times. "
                   "Not Kai: 21 is less than 22."))
    # 16
    pick("Wei counts 9 bald eagles in a tree and 8 on the riverbank. Lucas counts 18 bald eagles. Which is true?",
         "9 + 8 < 18", ["9 + 8 > 18", "9 + 8 = 18", "18 < 9 + 8"],
         "Wei counts 9 + 8 = 17 eagles. 17 is less than 18. The open side faces 18: <b>9 + 8 &lt; 18</b>.")
    # 17
    solve("The soccer team has 14 players. 9 players are on the field. The rest are on the bench. "
          "How many are on the bench?",
          [9, "+", "?", "=", 14], [23, 6, 4],
          "14 − 9 = ANS. Check: 9 + 5 = 14. Not 23: that adds.")
    # 18
    assert sfl(60, 38) == 38
    solve("A ferry has room for 60 bikes. 38 bikes are on the ferry. How many more bikes can get on?",
          [38, "+", "?", "=", 60], [98, 38, 32],
          "Count on: 38 to 40 is 2, 40 to 60 is 20. 2 + 20 = ANS. Not 98: that adds. "
          "Not 38: that takes the smaller digit from the larger.", pic=jump_svg(38, 60))
    # 19
    solve("Owen has 30 red beads and 15 blue beads. Ji-woo has 40 beads. "
          "How many more beads does Ji-woo need to have the same number as Owen?",
          [30, "+", 15, "=", 40, "+", "?"], [45, 25, 85],
          "Owen has 30 + 15 = 45. So 40 + □ = 45, and the box is ANS. Not 45: that is Owen’s total. "
          "Not 25: 40 is more than 30, so Ji-woo needs fewer than 15.")
    # 20
    assert 50 - 35 == 15 and holds("20 > 15") and sfl(50, 35) == 25
    its.append(mcq("Sofia has 50¢. She buys a pencil for 35¢. Ava has 20¢. Who has more money now?",
                   "Ava: 20¢ &gt; 15¢", ["Sofia: 50¢ &gt; 20¢", "Sofia: 25¢ &gt; 20¢", "Sofia: 15¢ &gt; 20¢"],
                   "Sofia has 50¢ − 35¢ = 15¢ left. <b>20¢ &gt; 15¢</b>, so Ava has more. "
                   "Not 25¢: from 35¢ to 50¢ is 15¢. Not 50¢: Sofia spent some of it. 15¢ &gt; 20¢ faces the wrong way."))
    assert len(its) == 20
    return {"title": "Word problems: equal or not equal", "items": its}


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
        "<h2>= means “is the same as”. ≠ means “is not equal to”</h2>"
        "<p>Think of a balance. When both sides are the same, it is level. Write <b>=</b>. "
        "When they are not the same, the heavier side goes down. Write <b>≠</b>.</p>"
        "<figure class='sn-fig'>" + dots_svg([(4, RED), (4, GREEN)], [(6, RED), (3, GREEN)]) +
        "<figcaption>4 + 4 = 8 and 6 + 3 = 9. 8 is not 9, so 4 + 4 ≠ 6 + 3.</figcaption></figure>" +
        table(["Sentence", "Left side", "Right side", "Sign"], [
            ["9 + 6 and 15", "15", "15", "="],
            ["8 + 5 and 12", "13", "12", "≠"],
            ["7 + 7 and 10 + 4", "14", "14", "="],
        ]) +
        "<h2>&lt; and &gt;: the open side faces the bigger number</h2>"
        "<p><b>&lt;</b> means “is less than”. <b>&gt;</b> means “is greater than”. "
        "Read from left to right. Look at the tens first. If the tens are the same, look at the ones.</p>"
        "<figure class='sn-fig'>" + blocks_svg(42, 37) +
        "<figcaption>42 has 4 tens. 37 has 3 tens. So 42 &gt; 37. You can also write 37 &lt; 42.</figcaption></figure>" +
        ex("Example", "Which sign goes in the box? 8 + 7 <b>□</b> 14",
           "Work out each side first. 8 + 7 = 15. 15 is greater than 14.", "8 + 7 &gt; 14") +
        "<h2>Find the missing number</h2>"
        "<p>A box □ stands for a number we do not know. Work out the side you know. "
        "Then find what makes the other side the same.</p>"
        "<figure class='sn-fig'>" + pan_svg("6 + 7", "10 + " + BOX) +
        "<figcaption>6 + 7 = 13, so 10 + □ must be 13 too. The box is 3, not 13.</figcaption></figure>" +
        ex("Example", html(40, "=", 25, "+", "?"),
           "Count on from 25 to 40: 25 to 30 is 5, 30 to 40 is 10. 5 + 10 = 15. Check: 25 + 15 = 40.", "15") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["42 &lt; 37 (&lt; and &gt; mixed up)", "The open side faces the bigger number: 42 &gt; 37"],
            ["37 is bigger than 42, because 7 &gt; 2", "Look at the tens first: 4 tens &gt; 3 tens"],
            ["6 + 4 = 10 + 2 (= means “the answer is”)", "Both sides must be the same. 10 is not 12, so 6 + 4 ≠ 10 + 2"],
            ["6 + 7 = 10 + □, so □ = 13", "13 is the left side. 10 + □ = 13, so □ = 3"],
            ["40 = 25 + □, so □ = 25 (smaller digit from larger)", "Count on: 25 to 30 is 5, 30 to 40 is 10. □ = 15"],
        ])
    )


FAQ = [
    {"q": "What does equality and inequality mean in Grade 2 math?",
     "a": "Equality means two amounts are the same, written with =. Inequality means they are not the same, written with ≠, or with < and > to show which one is less or greater."},
    {"q": "How can my child remember which way < and > go?",
     "a": "The open side always faces the bigger number. In 42 > 37 it opens toward 42, and in 37 < 42 it still opens toward 42."},
    {"q": "Where is equality in the BC Grade 2 math curriculum?",
     "a": "It is in Patterning: “symbolic representation of equality and inequality.” Students show equal and not equal with balances and pictures and write number sentences with = and ≠, using numbers to 100."},
    {"q": "Why does my child write 6 + 7 = 10 + 13?",
     "a": "Many children read = as “the answer is”. Show a balance: both sides must be the same, so 6 + 7 = 10 + 3."},
]


def gen_unit():
    rnd = random.Random(52806)
    sets = [set_eq_ne(), set_lt_gt(), set_true_false(), set_missing(), set_words()]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-2", "slug": "equality-and-inequality", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 2 Equality and Inequality (=, ≠, <, >)",
        "seo_title": "Grade 2 Equality and Inequality Worksheets (=, ≠, <, >): Free Math with Answer Key (BC Curriculum)",
        "short_title": "Equality and Inequality",
        "domain": "Patterning",
        "standard_code": "Grade 2: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/2/core",
        "standard_text": "Symbolic representation of equality and inequality",
        "meta_desc": "Free Grade 2 math worksheets on equality and inequality for the BC curriculum: balances with = and ≠, comparing numbers to 100 with < and >, true or false number sentences, missing numbers and word problems. 100 questions with an answer key.",
        "key_big": "= means “is the same as”. ≠ means “is not equal to”. The open side of < and > faces the bigger number.",
        "key_sub": "4 + 4 ≠ 6 + 3, because 8 is not 9. 42 > 37, because 4 tens is more than 3 tens. In 6 + 7 = 10 + □, the box is 3, not 13.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "bar model|pan balance|number line|base ten blocks")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
