# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 1 Math: Equal and Not Equal (= and ≠)
(Ontario Curriculum, Grades 1–8: Mathematics, 2020 — Algebra C2.1, C2.2, C2.3)
  python3 tools/gen_caon_math_g1_equality.py
Pan balances (balanced or not), the = and ≠ signs with cube trains and ten frames,
“is 3 + 4 the same as 5 + 2?”, missing numbers that balance (6 + 2 = □ + 3, 20 + 5 = 10 + □),
things that change and stay the same, and word problems. Numbers to 50.
Wrong choices come from real mistakes: reading = as “the answer comes next” (6 + 2 = □ + 3 -> 8),
adding every number (6 + 2 = □ + 3 -> 11), counting the start number (off by one),
judging by the look of the numbers (“the numbers are different, so not equal”),
adding the digits of tens and ones (30 + 5 -> 8) and writing digits side by side (30 + 5 -> 305).
Every answer is checked in code. HTML attributes use single quotes. Canadian English.
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-1")
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
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


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


class People:
    def __init__(self, rnd):
        self.pool = [(x, "she", "her") for x in GIRLS] + [(x, "he", "his") for x in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p

    def girl(self):
        while True:
            p = self.next()
            if p[1] == "she":
                return p

    def boy(self):
        while True:
            p = self.next()
            if p[1] == "he":
                return p


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
    lw = max(len(l) for l, _ in rows) * 9.6 + 14
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


def cake_svg(n):
    W, H = 200, 100
    s = ["<rect x='30' y='58' width='140' height='34' rx='5' fill='#f3d9e4' stroke='%s' stroke-width='2'/>" % INK,
         "<rect x='22' y='90' width='156' height='6' rx='2' fill='%s'/>" % INK]
    step = 120 / (n + 1)
    for i in range(n):
        cx = 40 + step * (i + 1)
        s.append("<rect x='%.1f' y='34' width='7' height='24' fill='%s' stroke='%s' stroke-width='1'/>" % (cx - 3.5, BLUE, INK))
        s.append("<path d='M %.1f 22 Q %.1f 28 %.1f 33 Q %.1f 28 %.1f 22 Z' fill='%s'/>"
                 % (cx, cx + 4, cx, cx - 4, cx, GOLD))
    return svg_wrap(W, H, "".join(s), "birthday cake with %d candles" % n)


def week_svg():
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    bw = 46
    s = []
    for i, d in enumerate(days):
        s.append("<rect x='%d' y='6' width='%d' height='36' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (6 + i * bw, bw, "#fff" if 0 < i < 6 else GREY, INK))
        s.append(text(6 + i * bw + bw / 2, 30, d, 15))
    return svg_wrap(7 * bw + 12, 48, "".join(s), "one week: Sunday to Saturday, 7 days")


def plants_svg():
    s = []
    for i, (h, lab) in enumerate([(18, "May"), (40, "June"), (64, "July")]):
        cx = 46 + i * 84
        base = 92
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='4'/>" % (cx, base, cx, base - h, GREEN))
        s.append("<ellipse cx='%d' cy='%d' rx='11' ry='6' fill='%s' transform='rotate(-30 %d %d)'/>"
                 % (cx - 10, base - h + 6, GREEN, cx - 10, base - h + 6))
        s.append("<ellipse cx='%d' cy='%d' rx='11' ry='6' fill='%s' transform='rotate(30 %d %d)'/>"
                 % (cx + 10, base - h + 6, GREEN, cx + 10, base - h + 6))
        s.append("<path d='M %d %d L %d %d L %d %d L %d %d Z' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (cx - 22, base, cx + 22, base, cx + 16, base + 24, cx - 16, base + 24, "#c8794a", INK))
        s.append(text(cx, base + 44, lab, 16))
    return svg_wrap(260, 142, "".join(s), "the same plant in May, June and July, taller each month")


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


def set_balances(P):
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


# ============================================================ set 2: = and ≠ with pictures
def eq_ne_choices(l, r):
    """One true and three false number sentences about l and r."""
    lv, rv = ev(l), ev(r)
    lt, rt = l.split(), r.split()
    if lv == rv:
        right = "%s = %s" % (l, r)
        if len(rt) == 1:
            alt = str(rv + 1)
        else:
            alt = " ".join(rt[:-1] + [str(int(rt[-1]) + 1)])
        wrong = ["%s %s %s" % (l, NE, r), "%s = %s" % (l, alt), "%s = %s" % (lt[0], r)]
    else:
        right = "%s %s %s" % (l, NE, r)
        wrong = ["%s = %s" % (l, r), "%s %s %d" % (l, NE, lv), "%d = %d" % (lv, rv)]
    return right, wrong


def set_eq_ne(P):
    its = []
    its.append(mcq("What does the " + NE + " sign mean?", "is not equal to",
                   ["is equal to", "add", "take away"],
                   "The " + NE + " sign means <b>is not equal to</b>. 5 " + NE + " 6 means 5 is not the same as 6."))
    its.append(mcq("What does the = sign mean?", "is the same as",
                   ["the answer comes next", "add the numbers", "is more than"],
                   "The = sign means <b>is the same as</b>. Both sides must be the same. "
                   "It does not mean “the answer comes next.”"))
    # cube trains
    pairs = [("4 + 3", "7"), ("5 + 2", "6"), ("3 + 5", "6 + 2"), ("2 + 6", "5 + 4"), ("6 + 3", "9"),
             ("7 + 1", "7"), ("4 + 4", "3 + 5"), ("9 + 2", "10 + 1"), ("8 + 5", "10 + 2"), ("6 + 6", "10 + 2")]
    for l, r in pairs:
        def cubes(x):
            t = x.split()
            if len(t) == 1:
                return [BLUE] * int(t[0])
            return [RED] * int(t[0]) + [GREEN] * int(t[2])
        pic = trains_svg([(l, cubes(l)), (r, cubes(r))])
        right, wrong = eq_ne_choices(l, r)
        lv, rv = ev(l), ev(r)
        other = ("The other train has %d." % rv) if len(r.split()) == 1 else ("%s = %d." % (r, rv))
        if lv == rv:
            e = "%s = %d. %s Both are %d, so use =: <b>%s</b>." % (l, lv, other, lv, right)
        else:
            e = "%s = %d. %s %d is not %d, so use %s: <b>%s</b>." % (l, lv, other, lv, rv, NE, right)
        its.append(stmt_mcq(fig(pic) + "Look at the cubes. Which is true?", right, wrong, e))
    # ten frames: which is true?
    TF = [("8 − 2", "8 − 2 " + NE + " 5", ["8 − 2 = 5", "8 − 2 " + NE + " 6", "8 − 2 = 10"]),
          ("3 + 4", "3 + 4 = 7", ["3 + 4 " + NE + " 7", "3 + 4 = 8", "3 + 4 = 6"]),
          ("9 − 4", "9 − 4 = 5", ["9 − 4 " + NE + " 5", "9 − 4 = 13", "9 − 4 = 6"]),
          ("6 + 3", "6 + 3 " + NE + " 8", ["6 + 3 = 8", "6 + 3 " + NE + " 9", "6 + 3 = 3"]),
          ("10 − 3", "10 − 3 " + NE + " 6", ["10 − 3 = 6", "10 − 3 " + NE + " 7", "10 − 3 = 13"]),
          ("5 + 5", "5 + 5 = 10", ["5 + 5 " + NE + " 10", "5 + 5 = 9", "5 + 5 = 11"])]
    for expr, right, wrong in TF:
        v = ev(expr)
        if "−" in expr:
            how = "Start with %s. Cross out %s. %d are left. %s = %d." % (expr.split()[0], expr.split()[2], v, expr, v)
        else:
            how = "Count the counters: %s = %d." % (expr, v)
        e = how + " So <b>%s</b> is true." % right
        its.append(stmt_mcq(fig(ten_frame_svg(expr)) + "Look at the ten frame. Which is true?", right, wrong, e))
    # which is false? (no picture)
    its.append(_not_true("4 + 2 = 7", ["4 + 2 = 6", "4 + 2 " + NE + " 7", "6 = 4 + 2"],
                         "4 + 2 = 6, not 7. So <b>4 + 2 = 7</b> is not true. "
                         "6 = 4 + 2 is true: the = sign can come first."))
    its.append(_not_true("7 = 7 + 1", ["7 = 8 − 1", "7 " + NE + " 7 + 1", "8 = 7 + 1"],
                         "7 + 1 = 8, not 7. So <b>7 = 7 + 1</b> is not true. 7 = 8 − 1 is true: both sides are 7."))
    assert len(its) == 20, len(its)
    return {"title": "Equal (=) or not equal (" + NE + ")?", "items": its}


def _not_true(right, wrong, e):
    """'Which one is NOT true?': the answer is false, the others are true."""
    assert not true_stmt(right), right
    for w in wrong:
        assert true_stmt(w), w
    return mcq("Which one is NOT true?", right, wrong, e)


# ============================================================ set 3: is 3 + 4 the same as 5 + 2?
def set_same_as(P):
    its = []
    pairs = [("3 + 4", "5 + 2"), ("4 + 4", "5 + 2"), ("6 + 3", "4 + 5"), ("2 + 7", "3 + 5"),
             ("9 − 2", "4 + 3"), ("10 − 4", "3 + 2"), ("5 + 1", "8 − 2"), ("7 + 3", "10 − 1")]
    for a, b in pairs:
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
    # which is the same as ...?
    W = [("4 + 4", "5 + 3", ["4 + 5", "5 + 2", "3 + 3"]),
         ("6 + 3", "7 + 2", ["6 + 4", "7 + 1", "3 + 3"]),
         ("9 − 3", "4 + 2", ["9 + 3", "4 + 3", "9 − 4"]),
         ("5 + 2", "8 − 1", ["5 − 2", "8 + 1", "8 − 2"]),
         ("10 + 6", "8 + 8", ["10 + 7", "8 + 6", "6 + 6"]),
         ("7 + 5", "10 + 2", ["10 + 5", "7 + 7", "10 + 3"])]
    for x, right, wrong in W:
        v = ev(x)
        assert ev(right) == v
        vals = [ev(w) for w in wrong]
        assert v not in vals and len(set(vals)) == 3, (x, vals)
        e = "%s = %d. <b>%s</b> = %d too. The others are %s." % (
            x, v, right, v, ", ".join("%s = %d" % (w, ev(w)) for w in wrong))
        its.append(mcq(fig(ten_frame_svg(x)) + "Which is the same as %s?" % x, right, wrong, e))
    # tens and ones to 50
    its.append(mcq(fig(rods_svg([35], ["30 + 5"])) + "Which number is the same as 30 + 5?", 35, [8, 53, 305],
                   "30 is 3 tens. 5 is 5 ones. 3 tens and 5 ones make <b>35</b>. Not 8: 30 is 3 tens, not 3."))
    its.append(mcq(fig(rods_svg([42], ["40 + 2"])) + "Which number is the same as 40 + 2?", 42, [6, 24, 402],
                   "40 is 4 tens. 2 is 2 ones. 4 tens and 2 ones make <b>42</b>. Not 24: the tens digit comes first."))
    its.append(mcq(fig(rods_svg([25, 25], ["20 + 5", "10 + 15"])) + "Is 20 + 5 the same as 10 + 15?",
                   "Yes. Both are 25.", ["No. 20 is not 10.", "Yes. Both are 35.", "No. 25 is not 35."],
                   "20 + 5 = 25. 10 + 15 = 25. Both are 25, so <b>yes</b>. Do not just look at the first numbers."))
    its.append(mcq(fig(rods_svg([40, 50], ["30 + 10", "20 + 30"])) + "Is 30 + 10 the same as 20 + 30?",
                   "No. 40 is not 50.", ["Yes. Both are 40.", "Yes. Both have a 30.", "Yes. Both are 50."],
                   "30 + 10 = 40. 20 + 30 = 50. 40 is not 50, so <b>no</b>: 30 + 10 " + NE + " 20 + 30."))
    its.append(mcq(fig(rods_svg([30], ["10 + 10 + 10"])) + "Which number is the same as 10 + 10 + 10?", 30, [3, 13, 40],
                   "Count by 10s: 10, 20, 30. So 10 + 10 + 10 = <b>30</b>. Not 3: each rod is 10, not 1."))
    its.append(mcq(fig(rods_svg([25], ["25"])) + "Which is the same as 25?", "20 + 5", ["2 + 5", "20 + 50", "10 + 5"],
                   "25 is 2 tens and 5 ones. That is <b>20 + 5</b>. 2 + 5 = 7, 20 + 50 = 70 and 10 + 5 = 15."))
    assert len(its) == 20, len(its)
    return {"title": "Is 3 + 4 the same as 5 + 2?", "items": its}


# ============================================================ set 4: missing numbers that balance
def missing_item(eq, pic, extra_wrong=None):
    """eq like '6 + 2 = □ + 3'. Wrong: the known side (answer next), adding all numbers, off by one."""
    k = solve(eq)
    l, r = eq.split(" = ")
    known, unk = (l, r) if BOX not in l else (r, l)
    v = ev(known)
    nums = [int(t) for t in unk.split() if t.isdigit()]
    other = nums[0]
    op = "+" if "+" in unk else MINUS
    if op == "+":
        how = "%s + %d = %d. %s So %s = <b>%d</b>." % (BOX, other, v, count_up(other, v), BOX, k) if unk.startswith(BOX) \
            else "%d + %s = %d. %s So %s = <b>%d</b>." % (other, BOX, v, count_up(other, v), BOX, k)
        add_all = v + other
    else:
        how = "%d − %s = %d. Think: %d + %d = %d. So %s = <b>%d</b>." % (other, BOX, v, v, k, other, BOX, k)
        add_all = v + other
    first = "The side you know is %s = %d. " % (known, v) if len(known.split()) > 1 else "The side you know is %d. " % v
    e = first + "The other side must be %d too. " % v + how
    if v != k and len(known.split()) > 1:
        e += " Not %d: the answer does not come right after =." % v
    cands = [v, add_all] + (extra_wrong or []) + [k + 1, k - 1]
    return mcq(pic + "What number makes it balance?<br>%s" % show(eq), k, cands, e)


def set_missing(P):
    its = []
    # A. dot balances with the unknown on the right
    for eq, L, R in [("6 + 2 = □ + 3", (6, 2), 3), ("4 + 3 = □ + 5", (4, 3), 5),
                     ("5 + 5 = □ + 6", (5, 5), 6), ("3 + 6 = 2 + □", (3, 6), 2)]:
        pic = fig(balance_svg([(L[0], RED), (L[1], GREEN)], [(R, BLUE)], unknown=True))
        its.append(missing_item(eq, pic))
    # B-E. pan balances with numbers
    for eq in ["□ + 4 = 9", "7 = □ + 3", "10 = 6 + □", "8 + 2 = 4 + □",
               "9 − 3 = □ + 2", "8 − □ = 5", "10 − 4 = 3 + □", "7 + 1 = 10 − □",
               "8 + 5 = 10 + □", "9 + 6 = 10 + □", "10 + 7 = □ + 8", "6 + 6 = 10 + □"]:
        l, r = eq.split(" = ")
        its.append(missing_item(eq, fig(pan_svg(l, r))))
    # F. tens to 50
    for eq, extra in [("20 + 5 = 10 + □", [5]), ("30 + 4 = □ + 20", [10]),
                      ("10 + 16 = □ + 6", [16]), ("25 + 10 = 30 + □", [15])]:
        l, r = eq.split(" = ")
        its.append(missing_item(eq, fig(pan_svg(l, r)), extra))
    assert len(its) == 20, len(its)
    return {"title": "Find the missing number to balance", "items": its}


# ============================================================ set 5: change, stay the same, word problems
def set_words(P):
    its = []
    # things that change and stay the same
    nm, he, his = P.girl()
    its.append(mcq(fig(cake_svg(6)) + "%s is 6 today. What will change next year?" % nm, "%s age" % his,
                   ["%s birthday" % his, "the days in a week", "the months in a year"],
                   "Next year %s will be 7. %s <b>age</b> changes every year. %s birthday is the same date every year."
                   % (nm, cap(his), cap(his))))
    nm, he, his = P.boy()
    its.append(mcq(fig(cake_svg(7)) + "%s turns 7 on May 12. What stays the same every year?" % nm,
                   "%s birthday" % his, ["%s age" % his, "how tall %s is" % he, "%s shoe size" % his],
                   "%s birthday is <b>May 12</b> every year. %s age, height and shoe size change as %s grows."
                   % (cap(his), cap(his), he)))
    its.append(mcq(fig(week_svg()) + "A week has 7 days. Does that change?", "No. It is always 7.",
                   ["Yes. It changes each week.", "Yes. Winter weeks are longer.", "Yes. Some weeks have 8."],
                   "Every week has 7 days, from Sunday to Saturday. That <b>always stays the same</b>."))
    its.append(mcq(fig(plants_svg()) + "Look at the plant. What changes?", "how tall it is",
                   ["the pot it is in", "the kind of plant", "the colour of the pot"],
                   "The plant gets taller in May, June and July. <b>How tall it is</b> changes. The pot stays the same."))
    nm, he, his = P.girl()
    before = [RED] * 5 + [BLUE] * 3
    after = [RED, BLUE, RED, RED, BLUE, RED, BLUE, RED]
    assert sorted(before) == sorted(after)
    its.append(mcq(fig(trains_svg([("Before", before), ("After", after)]))
                   + "%s has 5 red beads and 3 blue beads. %s moves them around. How many beads now?" % (nm, cap(he)),
                   "8 beads", ["5 beads", "3 beads", "9 beads"],
                   "5 + 3 = 8. Moving the beads does not change how many there are. "
                   "%s still has <b>8 beads</b>." % nm))
    nm, he, his = P.boy()
    its.append(mcq(fig(cake_svg(6)) + "%s is 6 years old. How old will %s be next year?" % (nm, he), "7 years old",
                   ["6 years old", "8 years old", "5 years old"],
                   "Your age goes up by 1 each year. 6 + 1 = <b>7</b>. Not 6: age changes."))

    # word problems
    def yn(lv, rv, unit):
        if lv == rv:
            return "Yes. Both have %d." % lv, ["No. %d is not %d." % (lv, lv + 1), "Yes. Both have %d." % (lv + 1),
                                                "No. The numbers are different."]
        return "No. %d is not %d." % (lv, rv), ["Yes. Both have %d." % lv, "Yes. Both have %d." % rv,
                                                 "Yes. They have the same %s." % unit]

    # 1
    a, ah, _ = P.boy()
    b, bh, _ = P.girl()
    right, wrong = yn(7, 7, "mitts")
    its.append(mcq(fig(trains_svg([(a, [RED] * 4 + [BLUE] * 3), (b, [GREEN] * 7)]))
                   + "%s has 4 red mitts and 3 blue mitts. %s has 7 mitts. Do they have the same number?" % (a, b),
                   right, wrong, "%s: 4 + 3 = 7. %s: 7. 4 + 3 = 7, so <b>yes</b>." % (a, b)))
    # 2
    a, ah, _ = P.girl()
    b, bh, _ = P.boy()
    right, wrong = yn(8, 9, "cards")
    its.append(mcq(fig(trains_svg([(a, [RED] * 5 + [GREEN] * 3), (b, [BLUE] * 9)]))
                   + "%s has 5 hockey cards. %s gets 3 more. %s has 9. Do they have the same number?" % (a, cap(ah), b),
                   right, wrong, "%s: 5 + 3 = 8. %s: 9. 8 is not 9, so <b>no</b>: 5 + 3 %s 9." % (a, b, NE)))
    # 3 skaters and sledders
    right, wrong = yn(8, 8, "kids")
    its.append(mcq(fig(trains_svg([("Rink", [RED] * 5 + [GREEN] * 3), ("Hill", [BLUE] * 4 + [GOLD] * 4)]))
                   + "5 kids skate at the rink. 3 more come. 4 kids sled on the hill. 4 more come. "
                   "Same number at the rink and the hill?", right, wrong,
                   "Rink: 5 + 3 = 8. Hill: 4 + 4 = 8. Both are 8, so <b>yes</b>: 5 + 3 = 4 + 4."))
    # 4 maple leaves
    a, ah, ahis = P.boy()
    b, bh, _ = P.girl()
    right, wrong = yn(7, 7, "leaves")
    its.append(mcq("%s has 10 maple leaves. %s gives 3 away. %s has 9 leaves. %s gives 2 away. "
                   "Do they have the same number now?" % (a, cap(ah), b, cap(bh)), right, wrong,
                   "%s: 10 − 3 = 7. %s: 9 − 2 = 7. Both have 7, so <b>yes</b>: 10 − 3 = 9 − 2." % (a, b)))
    # 5 missing: fruit
    a, ah, _ = P.girl()
    b, bh, bhis = P.boy()
    assert solve("6 + 2 = 3 + □") == 5
    its.append(mcq(fig(trains_svg([(a, [RED] * 6 + [GREEN] * 2), (b, [RED] * 3 + ["?"])]))
                   + "%s has 6 apples and 2 pears. %s has 3 apples. How many pears must %s get to have the same?"
                   % (a, b, bh), "5 pears", ["8 pears", "11 pears", "4 pears"],
                   "%s has 6 + 2 = 8. %s needs 8 too. 3 + %s = 8. %s So %s needs <b>5 pears</b>. "
                   "Not 8: that is %s total." % (a, b, BOX, count_up(3, 8), bh, a + "’s")))
    # 6 which number sentence fits
    a, ah, _ = P.girl()
    b, bh, _ = P.boy()
    its.append(stmt_mcq(fig(trains_svg([(a, [RED] * 4 + [BLUE] * 5), (b, [GREEN] * 9)]))
                        + "%s has 4 red crayons and 5 blue crayons. %s has 9 crayons. Which number sentence fits?" % (a, b),
                        "4 + 5 = 9", ["4 + 5 " + NE + " 9", "4 + 5 = 10", "9 + 5 = 4"],
                        "%s has 4 + 5. %s has 9. 4 + 5 = 9, so they are the same: <b>4 + 5 = 9</b>." % (a, b)))
    # 7 tens: crayons
    a, ah, _ = P.girl()
    b, bh, _ = P.boy()
    its.append(mcq(fig(rods_svg([25, 25], [a, b]))
                   + "%s has 2 boxes of 10 crayons and 5 more. %s has 25 crayons. Do they have the same number?" % (a, b),
                   "Yes. Both have 25.", ["No. %s has more." % a, "Yes. Both have 7.", "No. 25 is not 20."],
                   "%s: 10 + 10 + 5 = 25. %s: 25. Both have 25, so <b>yes</b>. Not 7: each box is 10, not 1." % (a, b)))
    # 8 tens: stickers
    a, ah, _ = P.girl()
    b, bh, bhis = P.boy()
    assert solve("30 = 10 + 10 + 5 + □") == 5
    its.append(mcq(fig(rods_svg([30, 25], [a, b]))
                   + "%s has 30 stickers. %s has 10 + 10 + 5. How many more does %s need to have the same?" % (a, b, bh),
                   "5 stickers", ["25 stickers", "55 stickers", "10 stickers"],
                   "%s has 10 + 10 + 5 = 25. %s has 30. 25 + 5 = 30, so <b>5</b> more. "
                   "Not 25: that is how many %s has now." % (b, a, bh)))
    # 9 Terry Fox Run
    assert solve("6 + 4 = 3 + □") == 7
    its.append(mcq(fig(trains_svg([("Room 1", [RED] * 6 + [GREEN] * 4), ("Room 2", [RED] * 3 + ["?"])]))
                   + "In the Terry Fox Run, Room 1 has 6 girls and 4 boys. Room 2 has 3 girls and some boys. "
                   "Both rooms have the same number. How many boys are in Room 2?",
                   "7 boys", ["10 boys", "13 boys", "6 boys"],
                   "Room 1: 6 + 4 = 10. Room 2 must have 10 too. 3 + %s = 10. 3 + 7 = 10, so <b>7 boys</b>. "
                   "Not 10: that is all of Room 1." % BOX))
    # 10 field trip apples
    a, ah, _ = P.girl()
    b, bh, _ = P.boy()
    its.append(mcq(fig(rods_svg([12, 6], [a, b]))
                   + "The class needs 20 apples for a field trip. %s brings 12. %s brings 6. Is that 20 apples?" % (a, b),
                   "No. 18 is not 20.", ["Yes. 12 + 6 = 20.", "Yes. Both are 20.", "No. They have 19."],
                   "12 + 6 = 18. 18 is not 20, so <b>no</b>: 12 + 6 %s 20. They need 2 more." % NE))
    # 11 towers
    assert solve("7 + 5 = 10 + □") == 2
    its.append(mcq(fig(pan_svg("7 + 5", "10 + " + BOX))
                   + "A tower has 7 blue blocks and 5 red blocks. Another has 10 green blocks. "
                   "How many green blocks must you add to make them the same?", "2 blocks", ["12 blocks", "22 blocks", "3 blocks"],
                   "7 + 5 = 12. 10 + %s = 12. 10 + 2 = 12, so add <b>2 blocks</b>. Not 12: that is the first tower." % BOX))
    # 12 Thanksgiving tarts
    a, ah, _ = P.boy()
    assert solve("9 + 6 = 10 + □") == 5
    its.append(mcq(fig(pan_svg("9 + 6", "10 + " + BOX))
                   + "For Thanksgiving, Grandma makes 9 pumpkin tarts and 6 apple tarts. %s makes 10 tarts. "
                   "How many more tarts must %s make to have the same?" % (a, ah),
                   "5 tarts", ["15 tarts", "25 tarts", "6 tarts"],
                   "Grandma: 9 + 6 = 15. %s: 10 + %s = 15. 10 + 5 = 15, so <b>5 tarts</b>. Not 15: that is Grandma’s total."
                   % (a, BOX)))
    # 13 which number sentence fits (subtraction and addition)
    a, ah, _ = P.boy()
    b, bh, _ = P.girl()
    its.append(stmt_mcq("%s has 8 cards. %s gives 3 away. %s has 2 cards. %s gets 3 more. They have the same. "
                        "Which number sentence fits?" % (a, cap(ah), b, cap(bh)),
                        "8 − 3 = 2 + 3", ["8 + 3 = 2 + 3", "8 − 3 " + NE + " 2 + 3", "8 − 3 = 2 + 5"],
                        "%s: 8 − 3 = 5. %s: 2 + 3 = 5. Both are 5: <b>8 − 3 = 2 + 3</b>." % (a, b)))
    # 14 canoes
    assert solve("4 + 4 = 6 + □") == 2
    its.append(mcq(fig(trains_svg([("Canoe A", [RED] * 4 + [GREEN] * 4), ("Canoe B", [BLUE] * 6 + ["?"])]))
                   + "At the cottage, Canoe A has 4 kids and 4 adults. Canoe B has 6 kids and some adults. "
                   "Both canoes have the same number of people. How many adults are in Canoe B?",
                   "2 adults", ["8 adults", "14 adults", "3 adults"],
                   "Canoe A: 4 + 4 = 8. Canoe B: 6 + %s = 8. 6 + 2 = 8, so <b>2 adults</b>. "
                   "Not 8: that is everyone in Canoe A." % BOX))
    assert len(its) == 20, len(its)
    return {"title": "Same or not the same? Word problems", "items": its}


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
        "<p>When the two sides are not the same, use <b>≠</b>. The heavier side of the balance goes down.</p>"
        "<figure class='sn-fig'>" + balance_svg([(5, RED), (3, GREEN)], [(7, BLUE)]) +
        "<figcaption>5 + 3 is 8. 8 is not 7. The left side goes down, so 5 + 3 ≠ 7.</figcaption></figure>"
        + table(["Two sides", "Left", "Right", "Sign"], [
            ["3 + 4 and 5 + 2", "7", "7", "="],
            ["4 + 4 and 5 + 2", "8", "7", "≠"],
            ["9 − 2 and 4 + 3", "7", "7", "="],
            ["20 + 5 and 10 + 15", "25", "25", "="],
        ]) +
        "<h2>Find the missing number</h2>"
        "<p>A box <b>□</b> is a number you do not know. Find the side you know first. "
        "Then make the other side the same.</p>"
        "<figure class='sn-fig'>" + pan_svg("6 + 2", "□ + 3") +
        "<figcaption>6 + 2 is 8. So □ + 3 must be 8 too. 5 + 3 = 8, so □ = 5.</figcaption></figure>"
        + ex("Example", "6 + 2 = □ + 3", "The left side is 6 + 2 = 8. Now □ + 3 = 8. Count up from 3: 4, 5, 6, 7, 8. That is 5.", "5")
        + ex("Example", "20 + 5 = 10 + □", "The left side is 25. 10 + 15 = 25.", "15")
        + "<h2>What changes and what stays the same?</h2>"
        "<p>Some things change. Your age goes up every year. A plant gets taller. "
        "Some things stay the same. Your birthday is the same date every year. A week always has 7 days. "
        "If you move 8 beads around, you still have 8.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["6 + 2 = □ + 3, so □ = 8", "8 is the left side. □ + 3 = 8, so □ = 5"],
            ["6 + 2 = □ + 3, so □ = 11 (adding all)", "Make both sides the same, do not add everything"],
            ["3 + 4 and 5 + 2 are not equal because the numbers are different", "Find each side: both are 7, so they are equal"],
            ["7 = 8 − 1 is wrong because the answer is first", "The = sign can come first. Both sides are 7"],
            ["30 + 5 = 8", "30 is 3 tens, not 3. 30 + 5 = 35"],
        ])
    )


FAQ = [
    {"q": "What does the not equal sign (≠) mean in Grade 1 math?",
     "a": "The ≠ sign means “is not equal to.” For example, 4 + 4 ≠ 5 + 2 because 8 is not the same as 7."},
    {"q": "How do you teach the equal sign in Grade 1?",
     "a": "Use a pan balance: when both sides have the same amount, it is level. This shows that = means “is the same as,” not “the answer comes next,” so 3 + 4 = 5 + 2 is true."},
    {"q": "How do Grade 1 students solve 6 + 2 = □ + 3?",
     "a": "Find the side you know first: 6 + 2 = 8. Then ask what number plus 3 makes 8. Count up from 3 to 8, so the box is 5, not 8."},
    {"q": "What does “quantities that change and stay the same” mean in the Ontario Grade 1 curriculum?",
     "a": "In the Algebra strand (C2.1), students notice that some amounts change, like your age or a plant’s height, while others stay the same, like your birthday or the 7 days in a week."},
]


def gen_unit():
    rnd = random.Random(41808)
    P = People(rnd)
    sets = [set_balances(P), set_eq_ne(P), set_same_as(P), set_missing(P), set_words(P)]
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
            # numbers in number-only choices or "N unit" choices: never equal in value
            lead = [re.match(r"(\d+) [a-z]+$", c) for c in it["c"]]
            if all(lead):
                assert len({int(m.group(1)) for m in lead}) == 4, it["c"]
    # dots drawn on each balance scale match its label
    for s in sets:
        for it in s["items"]:
            m = re.search(r"aria-label='balance scale with ([^']*)'", it["q"])
            if m:
                want = sum(int(n) for n in re.findall(r"(\d+) dots?", m.group(1)))
                assert it["q"].count("<circle") == want, it["q"]
            m = re.search(r"aria-label='ten frame with (\d+) (?:red and (\d+) green )?counters", it["q"])
            if m:
                assert it["q"].count("<circle") == int(m.group(1)) + int(m.group(2) or 0), it["q"]
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-1", "slug": "equal-and-not-equal", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 1 Equal and Not Equal",
        "seo_title": "Grade 1 Equal and Not Equal Worksheets (= and ≠): Free Math with Answer Key (Ontario Curriculum)",
        "short_title": "Equal and Not Equal",
        "domain": "Algebra",
        "standard_code": "Grade 1: C2.2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Determine whether given pairs of addition and subtraction expressions are equivalent or not",
        "meta_desc": "Free Grade 1 math worksheets on equal and not equal for the Ontario curriculum: balances, the = and ≠ signs, is 3 + 4 the same as 5 + 2, missing numbers like 6 + 2 = □ + 3, and things that change or stay the same. 100 questions with an answer key.",
        "key_big": "The = sign means “is the same as.” The ≠ sign means “is not equal to.”",
        "key_sub": "3 + 4 = 5 + 2 because both sides are 7. 4 + 4 ≠ 5 + 2 because 8 is not 7. In 6 + 2 = □ + 3, the box is 5, not 8.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "cube trains|base ten blocks|two ten frames|one week")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
