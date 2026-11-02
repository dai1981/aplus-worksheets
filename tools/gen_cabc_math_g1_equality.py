# -*- coding: utf-8 -*-
"""
British Columbia Grade 1 Math: Equal and Not Equal (= and ≠)
(BC Mathematics Curriculum, Grade 1 — Patterning: meaning of equality and inequality)
  python3 tools/gen_cabc_math_g1_equality.py
Pan balances (balanced or not), equal groups (rows spread out differently), the = and ≠ signs
with cube trains and ten frames, “is 4 + 3 the same as 5 + 2?”, more, fewer or the same,
and word problems that make both sides equal. Numbers to 20.
Wrong choices come from real mistakes: reading = as “the answer comes next” (6 + 2 = □ + 3 -> 8),
adding every number (6 + 2 = □ + 3 -> 11), off by one, thinking a longer row has more,
judging by the look of the numbers, and adding the digits of a teen number (10 + 5 -> 6).
Every answer is checked in code. HTML attributes use single quotes. Canadian English.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
BLUE = "#2e6da4"
GOLD = "#e0a100"
GREY = "#e9eef2"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
NE = "≠"
BOX = "□"


# ------------------------------------------------------------ number sentences
def ev(expr):
    """Value of '8 − 1', '4 + 1', '6', '20 + 5'."""
    toks = expr.split()
    v = int(toks[0])
    for op, n in zip(toks[1::2], toks[2::2]):
        assert op in ("+", MINUS), expr
        v = v + int(n) if op == "+" else v - int(n)
    return v


def true_stmt(s):
    """'4 + 3 = 7' or '5 + 2 ≠ 6' is true?"""
    if " = " in s:
        l, r = s.split(" = ")
        return ev(l) == ev(r)
    l, r = s.split(" " + NE + " ")
    return ev(l) != ev(r)


def solve(eq):
    """The one whole number 0-60 that makes eq (with □) true."""
    ok = [n for n in range(0, 61) if true_stmt(eq.replace(BOX, str(n)))]
    assert len(ok) == 1, (eq, ok)
    return ok[0]


def show(eq):
    return eq.replace(BOX, "<b>" + BOX + "</b>")


def count_list(a, b):
    return ", ".join(str(x) for x in range(a + 1, b + 1))


def count_up(a, b):
    """Short way to find b − a for Grade 1."""
    k = b - a
    if k <= 5:
        return "Count up from %d to %d: %s. That is %d." % (a, b, count_list(a, b), k)
    return "Think: %d + %d = %d." % (a, k, b)


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


def stmt_mcq(q, right, wrong, e):
    """Choices are number sentences: exactly one is true."""
    assert true_stmt(right), right
    for w in wrong:
        assert not true_stmt(w), (q, w)
    return mcq(q, right, wrong, e)


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


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag wide pictures so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ figures
def dots_label(groups):
    return " and ".join("%d dot%s" % (n, "" if n == 1 else "s") for n, _ in groups)


def balance_svg(left, right, unknown=False):
    """Pan balance with dots. left/right: lists of (count, colour). unknown: a ? in the right pan.
    The beam is level when both sides are equal (or the right side is unknown); the heavier side goes down."""
    L = sum(n for n, _ in left)
    R = sum(n for n, _ in right)
    assert L <= 15 and R <= 15
    t = 0 if (unknown or L == R) else (10 if L > R else -10)   # + : left side down
    rows = lambda groups, q: max(1, sum(math.ceil(n / 5) for n, _ in groups)) + (1 if q else 0)
    RM = max(rows(left, False), rows(right, unknown))
    by = 43 + 18 * (RM - 1) + 10
    W, H = 300, by + 46
    s = []
    s.append("<polygon points='150,%d 128,%d 172,%d' fill='%s'/>" % (by, by + 34, by + 34, INK))
    s.append("<rect x='105' y='%d' width='90' height='7' rx='2' fill='%s'/>" % (by + 34, INK))
    s.append("<line x1='66' y1='%.1f' x2='234' y2='%.1f' stroke='%s' stroke-width='5' stroke-linecap='round'/>"
             % (by + t * 0.8 * 84 / 78, by - t * 0.8 * 84 / 78, INK))
    for cx, ey, groups, q in [(72, by + t * 0.8, left, False), (228, by - t * 0.8, right, unknown)]:
        py = ey - 10
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='3'/>" % (cx, ey, cx, py, INK))
        s.append("<path d='M %d %.1f L %d %.1f L %d %.1f L %d %.1f Z' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (cx - 52, py - 3, cx + 52, py - 3, cx + 44, py + 3, cx - 44, py + 3, GREY, INK))
        r0 = 0
        for n, col in groups:
            for k in range(n):
                r, c = divmod(k, 5)
                s.append("<circle cx='%d' cy='%.1f' r='7' fill='%s'/>" % (cx - 36 + c * 18, py - 13 - 18 * (r0 + r), col))
            r0 += math.ceil(n / 5)
        if q:
            s.append(text(cx, py - 13 - 18 * r0 + 9, "?", 26))
    rl = dots_label(right)
    if unknown:
        rl = (rl + " and a question mark") if right else "a question mark"
    label = "balance scale with %s on the left and %s on the right" % (dots_label(left), rl)
    return svg_wrap(W, H, "".join(s), label)


FS = 20
GAP = 7
BOXW = 22


def tok_w(t):
    return BOXW if t == BOX else len(t) * FS * 0.6


def expr_w(s):
    ts = s.split(" ")
    return sum(tok_w(t) for t in ts) + GAP * (len(ts) - 1)


def draw_expr(cx, base, s):
    ts = s.split(" ")
    x = cx - expr_w(s) / 2
    out = []
    for t in ts:
        w = tok_w(t)
        if t == BOX:
            out.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2.5'/>"
                       % (x, base - 17, BOXW, BOXW, RED))
        else:
            out.append(text(x + w / 2, base, t, FS))
        x += w + GAP
    return "".join(out)


def pan_svg(left, right):
    """Pan balance with an expression in each pan. Level when equal or when a □ is in it;
    otherwise the side with more goes down."""
    if BOX in left or BOX in right:
        t = 0
    else:
        a, b = ev(left), ev(right)
        t = 0 if a == b else (10 if a > b else -10)
    w = max(96, int(max(expr_w(left), expr_w(right)) + 26))
    cl = 8 + w / 2
    cr = cl + w + 36
    mid = (cl + cr) / 2
    ih = 34
    by = 18 + ih + 5 + 16
    s = []
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='5' stroke-linecap='round'/>"
             % (cl, by + t, cr, by - t, INK))
    for txt, c, dy in ((left, cl, t), (right, cr, -t)):
        top = 18 + dy
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
                 % (c, top + ih + 5, c, by + dy, INK))
        s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (c - w / 2, top, w, ih, GREY, INK))
        s.append("<rect x='%.1f' y='%.1f' width='%d' height='5' fill='%s'/>" % (c - w / 2 - 4, top + ih, w + 8, INK))
        s.append(draw_expr(c, top + 25, txt))
    s.append("<polygon points='%.1f,%d %.1f,%d %.1f,%d' fill='%s'/>" % (mid, by, mid - 22, by + 34, mid + 22, by + 34, GREEN))
    s.append("<rect x='%.1f' y='%d' width='90' height='7' rx='2' fill='%s'/>" % (mid - 45, by + 34, INK))
    return svg_wrap(cr + w / 2 + 12, by + 45, "".join(s),
                    "pan balance with %s on the left and %s on the right" % (left.replace(BOX, "a box"), right.replace(BOX, "a box")))


def trains_svg(rows):
    """Rows of cubes. rows: list of (label, [colour, ...]); a '?' item draws an empty box with ?."""
    C, P, RH = 22, 25, 34
    lw = max(len(l) for l, _ in rows) * 11 + 14
    n = max(len(c) for _, c in rows)
    W = lw + n * P + 8
    H = len(rows) * RH + 8
    s = []
    parts = []
    for i, (lab, cols) in enumerate(rows):
        y = 6 + i * RH
        s.append(text(lw - 10, y + 17, lab, 16, "end"))
        for k, col in enumerate(cols):
            x = lw + k * P
            if col == "?":
                s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2' "
                         "stroke-dasharray='4 3'/>" % (x, y, C, C, INK))
                s.append(text(x + C / 2, y + 18, "?", 17))
            else:
                s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                         % (x, y, C, C, col, INK))
        nn = sum(1 for c in cols if c != "?")
        parts.append("%s has %d cube%s%s" % (lab, nn, "" if nn == 1 else "s", " and a question mark" if "?" in cols else ""))
    return svg_wrap(W, H, "".join(s), "cube trains: " + ", ".join(parts))


CELL = 28
FW, FH = 5 * CELL, 2 * CELL


def frame(x0, y0, colors, crossed=0):
    assert len(colors) <= 10
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='3'/>"
         % (x0, y0, FW, FH, INK)]
    for i in range(1, 5):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
                 % (x0 + i * CELL, y0, x0 + i * CELL, y0 + FH, INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + CELL, x0 + FW, y0 + CELL, INK))
    for k, col in enumerate(colors):
        r, c = divmod(k, 5)
        cx, cy = x0 + c * CELL + CELL // 2, y0 + r * CELL + CELL // 2
        s.append("<circle cx='%d' cy='%d' r='9' fill='%s'/>" % (cx, cy, col))
        if k >= len(colors) - crossed:
            s.append("<path d='M %d %d L %d %d M %d %d L %d %d' stroke='%s' stroke-width='3'/>"
                     % (cx - 10, cy - 10, cx + 10, cy + 10, cx - 10, cy + 10, cx + 10, cy - 10, INK))
    return "".join(s)


def expr_colors(expr):
    """Counters for '4 + 3' (red then green) or '9 − 2' (9 red, last 2 crossed out)."""
    t = expr.split()
    if len(t) == 1:
        return [RED] * int(t[0]), 0
    a, op, b = int(t[0]), t[1], int(t[2])
    if op == "+":
        return [RED] * a + [GREEN] * b, 0
    return [RED] * a, b


def frame_label(expr):
    t = expr.split()
    if len(t) == 1:
        return "%s counters" % t[0]
    if t[1] == "+":
        return "%s red and %s green counters" % (t[0], t[2])
    return "%s counters with %s crossed out" % (t[0], t[2])


def ten_frame_svg(expr):
    cols, x = expr_colors(expr)
    o = 6
    if len(cols) <= 10:
        return svg_wrap(FW + 2 * o, FH + 2 * o, frame(o, o, cols, x), "ten frame with " + frame_label(expr))
    assert x == 0
    return svg_wrap(FW + 2 * o, 2 * FH + 10 + 2 * o, frame(o, o, cols[:10]) + frame(o, o + FH + 10, cols[10:]),
                    "two ten frames with " + frame_label(expr))


def frame_pair_svg(a, b):
    """Two ten frames side by side, with each expression written under its frame."""
    o, gap = 6, 30
    ca, xa = expr_colors(a)
    cb, xb = expr_colors(b)
    s = frame(o, o, ca, xa) + frame(o + FW + gap, o, cb, xb)
    s += text(o + FW / 2, o + FH + 24, a, 18) + text(o + FW + gap + FW / 2, o + FH + 24, b, 18)
    return svg_wrap(2 * FW + gap + 2 * o, FH + 34 + o, s,
                    "two ten frames: %s and %s" % (frame_label(a), frame_label(b)))


def rods_svg(nums, labels):
    """Base ten blocks: each number as tens rods and ones cubes, with a label under it."""
    U, RP = 10, 16                       # cube size, rod pitch
    slots = []
    for n, lab in zip(nums, labels):
        t, o = divmod(n, 10)
        gw = t * RP + math.ceil(o / 5) * (U + 4) + (4 if o else 0)
        slots.append((n, lab, gw, max(gw, len(lab) * 9.6 + 6)))
    W = sum(sl[3] for sl in slots) + 36 * (len(slots) - 1) + 16
    H = 8 + 10 * U + 8 + 22
    s, x = [], 8
    for n, lab, gw, sw in slots:
        t, o = divmod(n, 10)
        gx = x + (sw - gw) / 2
        for i in range(t):
            rx = gx + i * RP
            s.append("<rect x='%.1f' y='8' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (rx, 12, 10 * U, BLUE, INK))
            for j in range(1, 10):
                s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1'/>"
                         % (rx, 8 + j * U, rx + 12, 8 + j * U, INK))
        ox = gx + t * RP + 4
        for k in range(o):
            c, r = divmod(k, 5)
            s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (ox + c * (U + 4), 8 + 10 * U - (r + 1) * (U + 2) + 2, U, U, GOLD, INK))
        s.append(text(x + sw / 2, 8 + 10 * U + 24, lab, 16))
        x += sw + 36
    desc = ", ".join("%s: %d ten%s and %d one%s" % (lab, n // 10, "" if n // 10 == 1 else "s", n % 10,
                                                      "" if n % 10 == 1 else "s") for n, lab in zip(nums, labels))
    return svg_wrap(W, H, "".join(s), "base ten blocks: " + desc)

# ============================================================ set 1: balanced or not?
def yn_choices(lv, rv, yes="Both sides are", why_no=None):
    """Yes/no choices for comparing two values lv and rv."""
    if lv == rv:
        right = "Yes. %s %d." % (yes, lv)
        wrong = ["No. %d is not %d." % (lv, lv + 1), "Yes. %s %d." % (yes, lv + 1),
                 why_no or "No. The sides look different."]
    else:
        right = "No. %d is not %d." % (lv, rv)
        wrong = ["Yes. %s %d." % (yes, lv), "Yes. %s %d." % (yes, rv),
                 why_no or "Yes. The beam is level."]
    return right, wrong


def ex_str(groups):
    return " + ".join(str(n) for n, _ in groups)


def set_balances():
    its = []
    LC = [RED, GREEN]
    RC = [BLUE, GOLD]
    # A. is the scale balanced?
    for l, r in [((4, 3), (7,)), ((5, 2), (6,)), ((3, 3), (2, 4)), ((6, 1), (4, 4)), ((5, 4), (9,)), ((2, 6), (3, 4))]:
        L = [(n, c) for n, c in zip(l, LC)]
        R = [(n, c) for n, c in zip(r, RC)]
        lv, rv = sum(l), sum(r)
        if lv == rv:
            right, wrong = yn_choices(lv, rv, why_no="No. The colours are not the same.")
            e = ("Left: %s = %d. Right: %s%s. Both sides are %d. The scale is level, so it is <b>balanced</b>."
                 % (ex_str(L), lv, ex_str(R), "" if len(r) == 1 else " = %d" % rv, lv))
        else:
            right, wrong = yn_choices(lv, rv)
            e =("Left: %s = %d. Right: %s%s. %d is not %d. The %s side goes down, so it is <b>not balanced</b>."
                 % (ex_str(L), lv, ex_str(R), "" if len(r) == 1 else " = %d" % rv, lv, rv,
                    "left" if lv > rv else "right"))
        its.append(mcq(fig(balance_svg(L, R)) + "Is the scale balanced?", right, wrong, e))
    # B. which number sentence matches the scale?
    B = [((4, 2), (6,), "4 + 2 = 6", ["4 + 2 " + NE + " 6", "4 + 2 = 7", "4 = 6"]),
         ((5, 3), (7,), "5 + 3 " + NE + " 7", ["5 + 3 = 7", "5 + 3 " + NE + " 8", "8 = 7"]),
         ((6,), (3, 3), "6 = 3 + 3", ["6 " + NE + " 3 + 3", "6 = 3 + 4", "6 + 3 = 3"]),
         ((2, 7), (4, 4), "2 + 7 " + NE + " 4 + 4", ["2 + 7 = 4 + 4", "2 + 7 " + NE + " 4 + 5", "9 = 8"])]
    for l, r, right, wrong in B:
        L = [(n, c) for n, c in zip(l, LC)]
        R = [(n, c) for n, c in zip(r, RC)]
        lv, rv = sum(l), sum(r)
        if lv == rv:
            e = "Both sides are %d. The scale is balanced, so use =: <b>%s</b>." % (lv, right)
        else:
            e = "The left side is %d. The right side is %d. Not the same, so use " % (lv, rv) + NE + ": <b>%s</b>." % right
        its.append(stmt_mcq(fig(balance_svg(L, R)) + "Which number sentence matches the scale?", right, wrong, e))
    # C. balanced scale with an unknown side
    for a, b in [(5, 4), (6, 6), (3, 8), (7, 2)]:
        s = a + b
        q = fig(balance_svg([(a, RED), (b, GREEN)], [], unknown=True)) + "The scale is balanced. How many dots are on the right?"
        e = "Balanced means both sides are the same. Left: %d + %d = %d. So the right side has <b>%d</b>." % (a, b, s, s)
        its.append(mcq(q, s, [s + 1, s - 1, max(a, b)], e))
    # D. not balanced: how many more?
    for a, b, k in [(4, 3, 5), (6, 2, 3), (5, 5, 6), (7, 4, 8)]:
        s = a + b
        need = s - k
        q = (fig(balance_svg([(a, RED), (b, GREEN)], [(k, BLUE)]))
             + "How many more dots must go on the right to balance it?")
        e = "Left: %d + %d = %d. Right: %d. %s So add <b>%d</b>. %d + %d = %d." % (a, b, s, k, count_up(k, s), need, k, need, s)
        its.append(mcq(q, need, [s, need + 1, need - 1], e))
    # E. ideas
    its.append(mcq("When is a scale balanced?", "Both sides are the same.",
                   ["One side has more.", "The left side is bigger.", "Both sides have 2 colours."],
                   "A scale is <b>balanced</b> when both sides are the same. Then it is level."))
    its.append(mcq("One side has 8. The other side has 3 + 4. Which side goes down?", "The side with 8",
                   ["The side with 3 + 4", "Neither. 8 = 3 + 4.", "The side with 2 numbers"],
                   "3 + 4 = 7. 8 is more than 7. So <b>the side with 8</b> goes down. 8 " + NE + " 3 + 4."))
    assert len(its) == 20, len(its)
    return {"title": "Balanced or not balanced?", "items": its}


def rows_svg(rows):
    """Rows of dots, each with its own spacing. rows: list of (label, n, pitch, colour).
    Used to show that a longer row does not always have more."""
    R = 8
    lw = max(len(l) for l, _, _, _ in rows) * 11 + 14
    W = lw + max(n * p for _, n, p, _ in rows) + 8
    RH = 30
    H = len(rows) * RH + 8
    s = []
    parts = []
    for i, (lab, n, p, col) in enumerate(rows):
        cy = 6 + i * RH + 13
        s.append(text(lw - 10, cy + 6, lab, 16, "end"))
        for k in range(n):
            s.append("<circle cx='%.1f' cy='%d' r='%d' fill='%s'/>" % (lw + p / 2 + k * p, cy, R, col))
        parts.append("%s has %d dot%s" % (lab, n, "" if n == 1 else "s"))
    return svg_wrap(W, H, "".join(s), "rows of dots: " + ", ".join(parts))


def cubes(x):
    t = x.split()
    if len(t) == 1:
        return [BLUE] * int(t[0])
    return [RED] * int(t[0]) + [GREEN] * int(t[2])


# ============================================================ set 2: equal groups or not?
def set_groups():
    its = []
    its.append(mcq("What does the = sign mean?", "is the same as",
                   ["the answer comes next", "add the numbers", "is more than"],
                   "The = sign means <b>is the same as</b>. Both sides must be the same. "
                   "It does not mean “the answer comes next.”"))
    its.append(mcq("What does the " + NE + " sign mean?", "is not equal to",
                   ["is equal to", "add", "take away"],
                   "The " + NE + " sign means <b>is not equal to</b>. 5 " + NE + " 6 means 5 is not the same as 6."))
    # rows spread out differently
    for a, pa, b, pb in [(6, 36, 6, 22), (7, 22, 5, 40), (8, 24, 8, 34), (9, 34, 10, 24), (5, 22, 5, 42), (12, 30, 11, 22)]:
        pic = rows_svg([("Red", a, pa, RED), ("Blue", b, pb, BLUE)])
        longer = "red" if a * pa > b * pb else "blue"
        if a == b:
            right = "Yes. Both have %d." % a
            wrong = ["No. The %s row is longer." % longer, "No. %d is not %d." % (a, a + 1), "Yes. Both have %d." % (a + 1)]
            e = ("Count each row. Red: %d. Blue: %d. Both have %d, so the groups are <b>equal</b>. "
                 "Do not look at how long the row is." % (a, b, a))
        else:
            right = "No. %d is not %d." % (a, b)
            wrong = ["Yes. Both have %d." % a, "Yes. Both have %d." % b, "Yes. They look the same."]
            e = "Count each row. Red: %d. Blue: %d. %d is not %d, so the groups are <b>not equal</b>." % (a, b, a, b)
            if (a > b) != (longer == "red"):
                e += " The %s row is longer, but it has fewer." % longer
        its.append(mcq(fig(pic) + "Are the two groups equal?", right, wrong, e))
    # cube trains
    for l, r in [("4 + 3", "7"), ("5 + 2", "6"), ("3 + 5", "6 + 2"), ("2 + 6", "5 + 4"), ("9 + 2", "10 + 1"), ("8 + 5", "10 + 2")]:
        pic = trains_svg([(l, cubes(l)), (r, cubes(r))])
        right, wrong = eq_ne_choices(l, r)
        lv, rv = ev(l), ev(r)
        other = ("The other train has %d." % rv) if len(r.split()) == 1 else ("%s = %d." % (r, rv))
        if lv == rv:
            e = "%s = %d. %s Both are %d, so use =: <b>%s</b>." % (l, lv, other, lv, right)
        else:
            e = "%s = %d. %s %d is not %d, so use %s: <b>%s</b>." % (l, lv, other, lv, rv, NE, right)
        its.append(stmt_mcq(fig(pic) + "Look at the cubes. Which is true?", right, wrong, e))
    # ten frames
    TF = [("8 − 2", "8 − 2 " + NE + " 5", ["8 − 2 = 5", "8 − 2 " + NE + " 6", "8 − 2 = 10"]),
          ("3 + 4", "3 + 4 = 7", ["3 + 4 " + NE + " 7", "3 + 4 = 8", "3 + 4 = 6"]),
          ("9 − 4", "9 − 4 = 5", ["9 − 4 " + NE + " 5", "9 − 4 = 13", "9 − 4 = 6"]),
          ("6 + 3", "6 + 3 " + NE + " 8", ["6 + 3 = 8", "6 + 3 " + NE + " 9", "6 + 3 = 3"])]
    for expr, right, wrong in TF:
        v = ev(expr)
        if MINUS in expr:
            how = "Start with %s. Cross out %s. %d are left. %s = %d." % (expr.split()[0], expr.split()[2], v, expr, v)
        else:
            how = "Count the counters: %s = %d." % (expr, v)
        e = how + " So <b>%s</b> is true." % right
        its.append(stmt_mcq(fig(ten_frame_svg(expr)) + "Look at the ten frame. Which is true?", right, wrong, e))
    its.append(_not_true("4 + 2 = 7", ["4 + 2 = 6", "4 + 2 " + NE + " 7", "6 = 4 + 2"],
                         "4 + 2 = 6, not 7. So <b>4 + 2 = 7</b> is not true. "
                         "6 = 4 + 2 is true: the = sign can come first."))
    its.append(_not_true("7 = 7 + 1", ["7 = 8 − 1", "7 " + NE + " 7 + 1", "8 = 7 + 1"],
                         "7 + 1 = 8, not 7. So <b>7 = 7 + 1</b> is not true. 7 = 8 − 1 is true: both sides are 7."))
    assert len(its) == 20, len(its)
    return {"title": "Equal groups or not equal?", "items": its}


def eq_ne_choices(l, r):
    """One true and three false number sentences about l and r."""
    lv, rv = ev(l), ev(r)
    lt, rt = l.split(), r.split()
    if lv == rv:
        right = "%s = %s" % (l, r)
        alt = str(rv + 1) if len(rt) == 1 else " ".join(rt[:-1] + [str(int(rt[-1]) + 1)])
        wrong = ["%s %s %s" % (l, NE, r), "%s = %s" % (l, alt), "%s = %s" % (lt[0], r)]
    else:
        right = "%s %s %s" % (l, NE, r)
        wrong = ["%s = %s" % (l, r), "%s %s %d" % (l, NE, lv), "%d = %d" % (lv, rv)]
    return right, wrong


def _not_true(right, wrong, e):
    """'Which one is NOT true?': the answer is false, the others are true."""
    assert not true_stmt(right), right
    for w in wrong:
        assert true_stmt(w), w
    return mcq("Which one is NOT true?", right, wrong, e)


# ============================================================ set 3: is 4 + 3 the same as 5 + 2?
def missing_item(eq, pic):
    """eq like '4 + 3 = 5 + □'. Wrong: the known side (answer next), adding all numbers, off by one."""
    k = solve(eq)
    l, r = eq.split(" = ")
    known, unk = (l, r) if BOX not in l else (r, l)
    v = ev(known)
    other = [int(t) for t in unk.split() if t.isdigit()][0]
    assert "+" in unk
    if unk.startswith(BOX):
        how = "%s + %d = %d. %s So %s = <b>%d</b>." % (BOX, other, v, count_up(other, v), BOX, k)
    else:
        how = "%d + %s = %d. %s So %s = <b>%d</b>." % (other, BOX, v, count_up(other, v), BOX, k)
    first = ("The side you know is %s = %d. " % (known, v)) if len(known.split()) > 1 else "The side you know is %d. " % v
    e = first + "The other side must be %d too. " % v + how
    if len(known.split()) > 1:
        e += " Not %d: the answer does not come right after =." % v
    return mcq(pic + "What number makes it balance?<br>%s" % show(eq), k, [v, v + other, k + 1, k - 1], e)


def set_same_as():
    its = []
    for a, b in [("4 + 3", "5 + 2"), ("4 + 4", "5 + 2"), ("6 + 3", "4 + 5"), ("2 + 7", "3 + 5"),
                 ("9 − 2", "4 + 3"), ("10 − 4", "3 + 2"), ("5 + 1", "8 − 2"), ("7 + 3", "10 − 1")]:
        va, vb = ev(a), ev(b)
        if va == vb:
            right = "Yes. Both are %d." % va
            wrong = ["No. The numbers are different.", "Yes. Both are %d." % (va + 1), "No. %d is not %d." % (va, va + 1)]
            e = "%s = %d and %s = %d. Both are %d, so <b>yes</b>: %s = %s." % (a, va, b, vb, va, a, b)
        else:
            right = "No. %d is not %d." % (va, vb)
            wrong = ["Yes. Both are %d." % va, "Yes. Both are %d." % vb, "Yes. Both have 2 numbers."]
            e = "%s = %d and %s = %d. %d is not %d, so <b>no</b>: %s %s %s." % (a, va, b, vb, va, vb, a, NE, b)
        its.append(mcq(fig(frame_pair_svg(a, b)) + "Is %s the same as %s?" % (a, b), right, wrong, e))
    for x, right, wrong in [("4 + 4", "5 + 3", ["4 + 5", "5 + 2", "3 + 3"]),
                            ("6 + 3", "7 + 2", ["6 + 4", "7 + 1", "3 + 3"]),
                            ("9 − 3", "4 + 2", ["9 + 3", "4 + 3", "9 − 4"]),
                            ("7 + 5", "10 + 2", ["10 + 5", "7 + 7", "10 + 3"])]:
        v = ev(x)
        assert ev(right) == v
        vals = [ev(w) for w in wrong]
        assert v not in vals and len(set(vals)) == 3, (x, vals)
        e = "%s = %d. <b>%s</b> = %d too. The others are %s." % (
            x, v, right, v, ", ".join("%s = %d" % (w, ev(w)) for w in wrong))
        its.append(mcq(fig(ten_frame_svg(x)) + "Which is the same as %s?" % x, right, wrong, e))
    # teen numbers with base ten blocks
    its.append(mcq(fig(rods_svg([14], ["10 + 4"])) + "Which number is the same as 10 + 4?", 14, [5, 41, 104],
                   "10 is 1 ten. 4 is 4 ones. 1 ten and 4 ones make <b>14</b>. Not 5: 10 is a ten, not 1."))
    its.append(mcq(fig(rods_svg([16, 16], ["10 + 6", "8 + 8"])) + "Is 10 + 6 the same as 8 + 8?",
                   "Yes. Both are 16.", ["No. 10 is not 8.", "Yes. Both are 18.", "No. 16 is not 18."],
                   "10 + 6 = 16. 8 + 8 = 16. Both are 16, so <b>yes</b>: 10 + 6 = 8 + 8."))
    its.append(mcq(fig(rods_svg([13, 14], ["10 + 3", "9 + 5"])) + "Is 10 + 3 the same as 9 + 5?",
                   "No. 13 is not 14.", ["Yes. Both are 13.", "Yes. Both are 14.", "Yes. Both have 2 numbers."],
                   "10 + 3 = 13. 9 + 5 = 14. 13 is not 14, so <b>no</b>: 10 + 3 " + NE + " 9 + 5."))
    v = [ev(w) for w in ["1 + 7", "10 + 8", "7 + 7"]]
    assert 17 not in v and len(set(v)) == 3
    its.append(mcq(fig(rods_svg([17], ["17"])) + "Which is the same as 17?", "10 + 7", ["1 + 7", "10 + 8", "7 + 7"],
                   "17 is 1 ten and 7 ones. That is <b>10 + 7</b>. 1 + 7 = 8, 10 + 8 = 18 and 7 + 7 = 14."))
    for eq in ["4 + 3 = 5 + □", "□ + 4 = 9", "7 = □ + 3", "8 + 2 = 4 + □"]:
        l, r = eq.split(" = ")
        its.append(missing_item(eq, fig(pan_svg(l, r))))
    assert len(its) == 20, len(its)
    return {"title": "Is 4 + 3 the same as 5 + 2?", "items": its}


# ============================================================ set 4: more, fewer, the same
def set_more_fewer():
    its = []
    for na, a, pa, nb, b, pb in [("Liam", 7, 34, "Ava", 9, 22), ("Mei", 8, 24, "Owen", 8, 34),
                                 ("Arjun", 12, 22, "Chloe", 10, 30), ("Simran", 6, 38, "Kai", 6, 22),
                                 ("Ryan", 11, 22, "Leah", 9, 32), ("Hana", 14, 20, "Lucas", 15, 20)]:
        pic = rows_svg([(na, a, pa, RED), (nb, b, pb, BLUE)])
        longer = na if a * pa > b * pb else nb
        if a == b:
            right = "They have the same."
            e = "%s has %d. %s has %d. They have <b>the same</b>. %s’s row is longer, but it does not have more." % (
                na, a, nb, b, longer)
        else:
            win = na if a > b else nb
            right = "%s has more." % win
            e = "%s has %d. %s has %d. %d is more than %d, so <b>%s has more</b>." % (na, a, nb, b, max(a, b), min(a, b), win)
            if win != longer and a * pa != b * pb:
                e += " Count. Do not just look at how long the row is."
        wrong = ["%s has more." % na, "%s has more." % nb, "They have the same.", "You cannot tell."]
        wrong.remove(right)
        its.append(mcq(fig(pic) + "Who has more beads?", right, wrong, e))
    for na, a, nb, b in [("Noah", 9, "Sofia", 6), ("Emma", 12, "Wei", 8), ("Harjot", 15, "Nadia", 10), ("Zara", 13, "Ethan", 7)]:
        d = a - b
        pic = trains_svg([(na, [RED] * a), (nb, [BLUE] * b)])
        e = "Line them up. %s has %d. %s has %d. %s So %s has <b>%d more</b>." % (na, a, nb, b, count_up(b, a), na, d)
        its.append(mcq(fig(pic) + "How many more cubes does %s have than %s?" % (na, nb), d, [a, d + 1, a + b], e))
    for na, a, nb, b in [("Olivia", 5, "Mateo", 8), ("Owen", 7, "Jasleen", 11), ("Chloe", 10, "Arjun", 16), ("Kai", 9, "Emma", 14)]:
        d = b - a
        pic = trains_svg([(na, [RED] * a), (nb, [BLUE] * b)])
        e = "Line them up. %s has %d. %s has %d. %s So %s has <b>%d fewer</b>." % (na, a, nb, b, count_up(a, b), na, d)
        its.append(mcq(fig(pic) + "How many fewer cubes does %s have than %s?" % (na, nb), d, [b, d + 1, d - 1], e))
    for l, r in [("8 + 4", "10 + 1"), ("6 + 6", "9 + 3"), ("7 + 7", "10 + 5")]:
        lv, rv = ev(l), ev(r)
        pic = trains_svg([(l, cubes(l)), (r, cubes(r))])
        opts = ["%s is more." % l, "%s is more." % r, "They are the same.", "You cannot tell."]
        if lv == rv:
            right = opts[2]
            e = "%s = %d. %s = %d. They are <b>the same</b>: %s = %s." % (l, lv, r, rv, l, r)
        else:
            right = opts[0] if lv > rv else opts[1]
            big = l if lv > rv else r
            e = "%s = %d. %s = %d. %d is more than %d, so <b>%s is more</b>. %s %s %s." % (
                l, lv, r, rv, max(lv, rv), min(lv, rv), big, l, NE, r)
        opts.remove(right)
        its.append(mcq(fig(pic) + "Which is more: %s or %s?" % (l, r), right, opts, e))
    for na, a, nb, b in [("Mei", 9, "Kai", 6), ("Noah", 12, "Zara", 7), ("Ethan", 15, "Sofia", 10)]:
        d = a - b
        pic = trains_svg([(na, [RED] * a), (nb, [BLUE] * b)])
        right = "Give %s %d more." % (nb, d)
        wrong = ["Give %s %d more." % (nb, a), "Give %s %d more." % (na, d), "Give %s %d more." % (nb, d + 1)]
        e = "%s has %d. %s has %d. %s needs %d more to have %d too. %d + %d = %d. So <b>give %s %d more</b>." % (
            na, a, nb, b, nb, d, a, b, d, a, nb, d)
        its.append(mcq(fig(pic) + "How can you make them the same?", right, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "More, fewer or the same?", "items": its}


# ============================================================ set 5: make both sides equal (word problems)
def yn(lv, rv):
    if lv == rv:
        return "Yes. Both have %d." % lv, ["No. %d is not %d." % (lv, lv + 1), "Yes. Both have %d." % (lv + 1),
                                            "No. The numbers are different."]
    return "No. %d is not %d." % (lv, rv), ["Yes. Both have %d." % lv, "Yes. Both have %d." % rv,
                                             "Yes. They look the same."]


def need(eq, right_unit, wrong_vals):
    k = solve(eq)
    vals = [k] + wrong_vals
    assert len(set(vals)) == 4 and min(vals) > 0, (eq, vals)
    return "%d %s" % (k, right_unit), ["%d %s" % (w, right_unit) for w in wrong_vals], k


def set_words():
    its = []
    # 1 orcas
    r, w = yn(7, 7)
    its.append(mcq(fig(trains_svg([("Kai", [RED] * 5 + [GREEN] * 2), ("Mei", [BLUE] * 7)]))
                   + "Kai sees 5 orcas. Then 2 more swim by. Mei sees 7 orcas. Do they see the same number?",
                   r, w, "Kai: 5 + 2 = 7. Mei: 7. Both are 7, so <b>yes</b>: 5 + 2 = 7."))
    # 2 stickers
    r, w = yn(11, 10)
    its.append(mcq(fig(trains_svg([("Simran", [RED] * 8 + [GREEN] * 3), ("Owen", [BLUE] * 10)]))
                   + "Simran has 8 stickers. She gets 3 more. Owen has 10. Do they have the same number?",
                   r, w, "Simran: 8 + 3 = 11. Owen: 10. 11 is not 10, so <b>no</b>: 8 + 3 %s 10." % NE))
    # 3 hike and bike
    r, w = yn(10, 10)
    its.append(mcq(fig(trains_svg([("Hike", [RED] * 6 + [GREEN] * 4), ("Bike", [BLUE] * 5 + [GOLD] * 5)]))
                   + "In Stanley Park, 6 kids hike. 4 more join. 5 kids bike. 5 more join. "
                   "Are the same number of kids hiking and biking?", r, w,
                   "Hike: 6 + 4 = 10. Bike: 5 + 5 = 10. Both are 10, so <b>yes</b>: 6 + 4 = 5 + 5."))
    # 4 cedar cones
    r, w = yn(8, 8)
    its.append(mcq(fig(pan_svg("12 − 4", "10 − 2"))
                   + "Noah has 12 cedar cones. He gives 4 away. Chloe has 10. She gives 2 away. "
                   "Do they have the same number now?", r, w,
                   "Noah: 12 − 4 = 8. Chloe: 10 − 2 = 8. Both have 8, so <b>yes</b>: 12 − 4 = 10 − 2."))
    # 5 apples and pears
    right, wrong, k = need("6 + 2 = 3 + □", "pears", [8, 11, 4])
    its.append(mcq(fig(trains_svg([("Ava", [RED] * 6 + [GREEN] * 2), ("Lucas", [RED] * 3 + ["?"])]))
                   + "Ava has 6 apples and 2 pears. Lucas has 3 apples. How many pears must he get to have the same?",
                   right, wrong,
                   "Ava has 6 + 2 = 8. Lucas needs 8 too. 3 + %s = 8. %s So he needs <b>%s</b>. "
                   "Not 8: that is Ava’s total." % (BOX, count_up(3, 8), right)))
    # 6 crayons
    its.append(stmt_mcq(fig(trains_svg([("Jasleen", [RED] * 4 + [BLUE] * 5), ("Ryan", [GREEN] * 9)]))
                        + "Jasleen has 4 red crayons and 5 blue crayons. Ryan has 9 crayons. Which number sentence fits?",
                        "4 + 5 = 9", ["4 + 5 " + NE + " 9", "4 + 5 = 10", "9 + 5 = 4"],
                        "Jasleen has 4 + 5. Ryan has 9. 4 + 5 = 9, so they are the same: <b>4 + 5 = 9</b>."))
    # 7 teen stickers
    its.append(mcq(fig(rods_svg([15, 15], ["Zara", "Harjot"]))
                   + "Zara has a pack of 10 stickers and 5 more. Harjot has 15. Do they have the same number?",
                   "Yes. Both have 15.", ["No. Zara has more.", "Yes. Both have 6.", "No. 15 is not 10."],
                   "Zara: 10 + 5 = 15. Harjot: 15. Both have 15, so <b>yes</b>. Not 6: the pack is 10, not 1."))
    # 8 cards
    right, wrong, k = need("14 = 10 + □", "cards", [14, 24, 5])
    its.append(mcq(fig(rods_svg([14, 10], ["Leah", "Wei"]))
                   + "Leah has 14 hockey cards. Wei has 10. How many more does Wei need to have the same?",
                   right, wrong,
                   "Leah has 14. Wei has 10. 10 + 4 = 14, so Wei needs <b>%s</b>. Not 14: that is how many Leah has." % right))
    # 9 Terry Fox Run
    right, wrong, k = need("6 + 4 = 3 + □", "boys", [10, 13, 6])
    its.append(mcq(fig(trains_svg([("Room 1", [RED] * 6 + [GREEN] * 4), ("Room 2", [RED] * 3 + ["?"])]))
                   + "At the Terry Fox Run, Room 1 has 6 girls and 4 boys. Room 2 has 3 girls and some boys. "
                   "Both rooms have the same number. How many boys are in Room 2?", right, wrong,
                   "Room 1: 6 + 4 = 10. Room 2 must have 10 too. 3 + %s = 10. 3 + 7 = 10, so <b>%s</b>. "
                   "Not 10: that is all of Room 1." % (BOX, right)))
    # 10 field trip apples
    its.append(mcq(fig(rods_svg([12, 6], ["Olivia", "Arjun"]))
                   + "The class needs 20 apples for a field trip. Olivia brings 12. Arjun brings 6. Is that 20 apples?",
                   "No. 18 is not 20.", ["Yes. 12 + 6 = 20.", "Yes. Both are 20.", "No. They have 19."],
                   "12 + 6 = 18. 18 is not 20, so <b>no</b>: 12 + 6 %s 20. They need 2 more." % NE))
    # 11 towers
    right, wrong, k = need("7 + 5 = 10 + □", "blocks", [12, 22, 3])
    its.append(mcq(fig(pan_svg("7 + 5", "10 + " + BOX))
                   + "A tower has 7 blue blocks and 5 red blocks. Another has 10 green blocks. "
                   "How many green blocks must you add to make them the same?", right, wrong,
                   "7 + 5 = 12. 10 + %s = 12. 10 + 2 = 12, so add <b>%s</b>. Not 12: that is the first tower." % (BOX, right)))
    # 12 soccer
    right, wrong, k = need("9 + 6 = 10 + □", "kids", [15, 25, 6])
    its.append(mcq(fig(pan_svg("9 + 6", "10 + " + BOX))
                   + "Team A has 9 kids. 6 more come. Team B has 10 kids. "
                   "How many more kids must come to Team B to make it the same?", right, wrong,
                   "Team A: 9 + 6 = 15. Team B: 10 + %s = 15. 10 + 5 = 15, so <b>%s</b>. "
                   "Not 15: that is all of Team A." % (BOX, right)))
    # 13 cards: subtraction and addition
    its.append(stmt_mcq("Ethan has 8 cards. He gives 3 away. Sofia has 2 cards. She gets 3 more. "
                        "They have the same. Which number sentence fits?",
                        "8 − 3 = 2 + 3", ["8 + 3 = 2 + 3", "8 − 3 " + NE + " 2 + 3", "8 − 3 = 2 + 5"],
                        "Ethan: 8 − 3 = 5. Sofia: 2 + 3 = 5. Both are 5: <b>8 − 3 = 2 + 3</b>."))
    # 14 canoes
    right, wrong, k = need("5 + 4 = 6 + □", "adults", [9, 15, 4])
    its.append(mcq(fig(trains_svg([("Canoe A", [RED] * 5 + [GREEN] * 4), ("Canoe B", [RED] * 6 + ["?"])]))
                   + "At the lake, Canoe A has 5 kids and 4 adults. Canoe B has 6 kids and some adults. "
                   "Both canoes have the same number of people. How many adults are in Canoe B?", right, wrong,
                   "Canoe A: 5 + 4 = 9. Canoe B: 6 + %s = 9. 6 + 3 = 9, so <b>%s</b>. "
                   "Not 9: that is everyone in Canoe A." % (BOX, right)))
    # 15 ferry
    its.append(stmt_mcq(fig(trains_svg([("Liam", [RED] * 7 + [BLUE] * 5), ("Hana", [GREEN] * 12)]))
                        + "On BC Ferries, Liam counts 7 red cars and 5 blue cars. Hana counts 12 cars. "
                        "Which number sentence fits?",
                        "7 + 5 = 12", ["7 + 5 " + NE + " 12", "7 + 5 = 13", "12 + 5 = 7"],
                        "Liam counts 7 + 5 = 12. Hana counts 12. They are the same: <b>7 + 5 = 12</b>."))
    # 16 SkyTrain
    r, w = yn(14, 14)
    its.append(mcq(fig(trains_svg([("Car 1", [RED] * 8 + [GREEN] * 6), ("Car 2", [BLUE] * 14)]))
                   + "8 people get on a SkyTrain car. Then 6 more get on. Car 2 has 14 people. "
                   "Do the cars have the same number?", r, w,
                   "Car 1: 8 + 6 = 14. Car 2: 14. Both have 14, so <b>yes</b>: 8 + 6 = 14."))
    # 17 take some off
    right, wrong, k = need("13 − □ = 9", "blocks", [13, 22, 5])
    its.append(mcq(fig(trains_svg([("Mateo", [RED] * 13), ("Sofia", [BLUE] * 9)]))
                   + "Mateo has 13 blocks in a tower. Sofia has 9. How many must Mateo take off to make them the same?",
                   right, wrong,
                   "Mateo has 13. Sofia has 9. 9 + 4 = 13, so Mateo takes off <b>%s</b>. 13 − 4 = 9. "
                   "Not 13: then he has 0 left." % right))
    # 18 share to make the same
    its.append(mcq(fig(trains_svg([("Kai", [RED] * 9), ("Emma", [BLUE] * 5)]))
                   + "Kai has 9 shells. Emma has 5. Kai gives Emma some. Now they have the same. How many did Kai give?",
                   "2 shells", ["4 shells", "7 shells", "3 shells"],
                   "Together they have 9 + 5 = 14. The same is 7 each. Kai gives 2: 9 − 2 = 7 and 5 + 2 = 7. "
                   "So <b>2 shells</b>. Not 4: then Kai has 5 and Emma has 9."))
    assert 9 - 2 == 5 + 2
    # 19 marbles
    its.append(stmt_mcq(fig(trains_svg([("Lucas", [RED] * 6 + [GREEN] * 6), ("Ava", [BLUE] * 10 + [GOLD] * 2)]))
                        + "Lucas has 6 red and 6 green marbles. Ava has 10 blue and 2 yellow marbles. Which number sentence fits?",
                        "6 + 6 = 10 + 2", ["6 + 6 " + NE + " 10 + 2", "6 + 6 = 12 + 2", "6 + 6 = 10 + 3"],
                        "Lucas: 6 + 6 = 12. Ava: 10 + 2 = 12. Both are 12: <b>6 + 6 = 10 + 2</b>."))
    # 20 Whistler
    right, wrong, k = need("8 + 3 = 5 + □", "kids", [11, 16, 7])
    its.append(mcq(fig(pan_svg("8 + 3", "5 + " + BOX))
                   + "At Whistler, 8 kids ski and 3 kids snowboard. In a second group, 5 kids ski. "
                   "How many must snowboard to make the groups the same?", right, wrong,
                   "Group 1: 8 + 3 = 11. Group 2: 5 + %s = 11. 5 + 6 = 11, so <b>%s</b>. "
                   "Not 11: that is all of Group 1." % (BOX, right)))
    assert len(its) == 20, len(its)
    return {"title": "Make both sides equal: word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>= means “the same as”</h2>"
        "<p>The <b>=</b> sign means <b>is the same as</b>. Both sides must have the same amount. "
        "It does not mean “the answer comes next.” Think of a balance. "
        "When both sides are the same, it is level.</p>"
        "<figure class='sn-fig'>" + balance_svg([(4, RED), (3, GREEN)], [(5, BLUE), (2, GOLD)]) +
        "<figcaption>4 + 3 is 7. 5 + 2 is 7. The scale is balanced, so 4 + 3 = 5 + 2.</figcaption></figure>"
        "<h2>≠ means “is not equal to”</h2>"
        "<p>When the two sides are not the same, use <b>≠</b>. The side with more goes down.</p>"
        "<figure class='sn-fig'>" + balance_svg([(5, RED), (3, GREEN)], [(7, BLUE)]) +
        "<figcaption>5 + 3 is 8. 8 is not 7. The left side goes down, so 5 + 3 ≠ 7.</figcaption></figure>"
        + table(["Two sides", "Left", "Right", "Sign"], [
            ["4 + 3 and 5 + 2", "7", "7", "="],
            ["4 + 4 and 5 + 2", "8", "7", "≠"],
            ["9 − 2 and 4 + 3", "7", "7", "="],
            ["10 + 6 and 8 + 8", "16", "16", "="],
        ]) +
        "<h2>Count. Do not just look.</h2>"
        "<p>A longer row does not always have more. Count each group. "
        "If the numbers are the same, the groups are equal.</p>"
        "<figure class='sn-fig'>" + rows_svg([("Red", 6, 36, RED), ("Blue", 6, 22, BLUE)]) +
        "<figcaption>The red row is longer. But both rows have 6. They are equal.</figcaption></figure>"
        "<h2>More, fewer or the same</h2>"
        "<p>Line the groups up. The extra ones show how many more.</p>"
        + ex("Example", "Noah has 9 cubes. Sofia has 6. How many more does Noah have?",
             "Count up from 6 to 9: 7, 8, 9. That is 3.", "3 more")
        + "<h2>Make both sides equal</h2>"
        "<p>A box <b>□</b> is a number you do not know. Find the side you know first. "
        "Then make the other side the same.</p>"
        "<figure class='sn-fig'>" + pan_svg("6 + 2", "□ + 3") +
        "<figcaption>6 + 2 is 8. So □ + 3 must be 8 too. 5 + 3 = 8, so □ = 5.</figcaption></figure>"
        + ex("Example", "6 + 2 = □ + 3", "The left side is 6 + 2 = 8. Now □ + 3 = 8. Count up from 3: 4, 5, 6, 7, 8. That is 5.", "5")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["6 + 2 = □ + 3, so □ = 8", "8 is the left side. □ + 3 = 8, so □ = 5"],
            ["6 + 2 = □ + 3, so □ = 11 (adding all)", "Make both sides the same. Do not add everything"],
            ["The longer row has more", "Count each row. Spread-out dots are not more"],
            ["4 + 3 and 5 + 2 are not equal because the numbers are different", "Find each side: both are 7, so they are equal"],
            ["7 = 8 − 1 is wrong because the answer is first", "The = sign can come first. Both sides are 7"],
        ])
    )


FAQ = [
    {"q": "What does equality and inequality mean in Grade 1 math in BC?",
     "a": "It means knowing when two amounts are the same (equal) and when they are not (not equal). In the BC Grade 1 Patterning standard, students use balances and objects to show that 4 + 3 = 5 + 2 and that 4 + 4 ≠ 5 + 2."},
    {"q": "How do you teach the equal sign in Grade 1?",
     "a": "Use a pan balance: when both sides have the same amount, it is level. This shows that = means “is the same as,” not “the answer comes next,” so 3 + 4 = 5 + 2 is true."},
    {"q": "What does the not equal sign (≠) mean?",
     "a": "The ≠ sign means “is not equal to.” For example, 8 ≠ 7 and 5 + 3 ≠ 7, because 8 is not the same as 7."},
    {"q": "How do Grade 1 students solve 6 + 2 = □ + 3?",
     "a": "Find the side you know first: 6 + 2 = 8. Then ask what number plus 3 makes 8. Count up from 3 to 8, so the box is 5, not 8."},
]


def gen_unit():
    rnd = random.Random(51805)
    sets = [set_balances(), set_groups(), set_same_as(), set_more_fewer(), set_words()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
            nums = [c for c in it["c"] if re.fullmatch(r"\d+", c)]
            assert len(set(map(int, nums))) == len(nums)
            lead = [re.match(r"(\d+) [a-z]+$", c) for c in it["c"]]
            if all(lead):
                assert len({int(m.group(1)) for m in lead}) == 4, it["c"]
            # numbers to 20 (wrong answers from mistakes may go higher)
            for n in re.findall(r"\d+", re.sub(r"<svg.*?</svg>", "", it["q"])):
                assert int(n) <= 20, (n, it["q"])
    for s in sets:
        for it in s["items"]:
            m = re.search(r"aria-label='balance scale with ([^']*)'", it["q"])
            if m:
                want = sum(int(n) for n in re.findall(r"(\d+) dots?", m.group(1)))
                assert it["q"].count("<circle") == want, it["q"]
            m = re.search(r"aria-label='ten frame with (\d+) (?:red and (\d+) green )?counters", it["q"])
            if m:
                assert it["q"].count("<circle") == int(m.group(1)) + int(m.group(2) or 0), it["q"]
            m = re.search(r"aria-label='rows of dots: ([^']*)'", it["q"])
            if m:
                want = sum(int(n) for n in re.findall(r"(\d+) dots?", m.group(1)))
                assert it["q"].count("<circle") == want, it["q"]
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-1", "slug": "equal-and-not-equal", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 1 Equal and Not Equal",
        "seo_title": "Grade 1 Equal and Not Equal Worksheets (= and ≠): Free Math with Answer Key (BC Curriculum)",
        "short_title": "Equal and Not Equal",
        "domain": "Patterning",
        "standard_code": "Grade 1: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/1/core",
        "standard_text": "Meaning of equality and inequality",
        "meta_desc": "Free Grade 1 math worksheets on equal and not equal for the BC curriculum: balances, equal groups, the = and ≠ signs, is 4 + 3 the same as 5 + 2, more, fewer or the same, and making both sides equal. 100 questions with an answer key.",
        "key_big": "The = sign means “is the same as.” The ≠ sign means “is not equal to.”",
        "key_sub": "4 + 3 = 5 + 2 because both sides are 7. 4 + 4 ≠ 5 + 2 because 8 is not 7. In 6 + 2 = □ + 3, the box is 5, not 8.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "cube trains|base ten blocks|rows of dots")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
