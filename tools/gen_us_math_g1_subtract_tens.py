# -*- coding: utf-8 -*-
"""
US Grade 1 Math: Subtract Multiples of 10 (1.NBT.C.6)
  python tools/gen_us_math_g1_subtract_tens.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 1: only 10, 20, ... 90 minus 10, 20, ... 90. Numbers up to 120, no commas.
Very short sentences for 6-7 year olds.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
TOP = 120                      # Grade 1 numbers stay at 120 or less


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or not c or c.startswith("-") or re.match(r"^0\b", c) or c.startswith("0¢"):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def mcq_n(q, correct, cands, e, fmt="%d"):
    """Number choices. Wrong numbers that are 0 or less, or over 120, are dropped."""
    ok = [fmt % v for v in cands if v is not None and 0 < v <= TOP and v != correct]
    return mcq(q, fmt % correct, ok, e)


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


def cap(s):
    return s[0].upper() + s[1:]


def tens(n):
    return "1 ten" if n == 1 else "%d tens" % n


def sub(a, b):
    return "%d %s %d" % (a, MINUS, b)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
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
    """Tag pictures that must print larger (rods, number lines) so every piece is easy to count."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
SQ, RGAP, M = 11, 9, 8          # one small square of a rod, gap between rods, margin


def rods_svg(n, crossed=0):
    """n ten rods (each 10 small squares). The last `crossed` rods are crossed out with a red line."""
    W = 2 * M + n * SQ + (n - 1) * RGAP
    H = 2 * M + 10 * SQ
    s = []
    for k in range(n):
        x, y = M + k * (SQ + RGAP), M
        out = k >= n - crossed
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x, y, SQ, 10 * SQ, "#eef5f0" if out else FILL, GREEN))
        for i in range(1, 10):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.8'/>"
                     % (x, y + i * SQ, x + SQ, y + i * SQ, GREEN))
        if out:
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3.5' stroke-linecap='round'/>"
                     % (x - 4, y + 10 * SQ - 14, x + SQ + 4, y + 14, RED))
    label = "base-ten rods: %s" % tens(n) + (", %d crossed out" % crossed if crossed else "")
    return svg_wrap(W, H, "".join(s), label)


DR = 19


def dimes_svg(n):
    """n dimes, rows of at most 5."""
    m, gap = 4, 6
    per = 5 if n > 5 else n
    rows = [per] * (n // per) + ([n % per] if n % per else [])
    d = 2 * DR + gap
    W = 2 * m + max(rows) * d - gap
    H = 2 * m + len(rows) * d - gap
    s = []
    for r, k in enumerate(rows):
        for i in range(k):
            cx, cy = m + DR + i * d, m + DR + r * d
            s.append("<circle cx='%d' cy='%d' r='%d' fill='#dfe3e7' stroke='#7a828a' stroke-width='2'/>" % (cx, cy, DR))
            s.append("<circle cx='%d' cy='%d' r='%d' fill='none' stroke='#9aa2aa' stroke-width='1'/>" % (cx, cy, DR - 4))
            s.append(text(cx, cy + 5, "10¢", 14))
    assert sum(rows) == n
    return svg_wrap(W, H, "".join(s), "%d dimes" % n)


JW = 64                          # one jump of 10 on an open number line


def open_line_svg(start, jumps, end_label="?"):
    """Open number line: start on the right, `jumps` jumps back. jumps = list of sizes (10 or bigger)."""
    m, ry, ly = 30, 22, 52
    widths = [JW if j == 10 else JW + 26 for j in jumps]
    W = 2 * m + sum(widths)
    H = ly + 32
    xs = [W - m]
    for w in widths:
        xs.append(xs[-1] - w)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (m - 18, ly, W - m + 18, ly, INK)]
    for k, j in enumerate(jumps):
        x1, x2 = xs[k], xs[k + 1]
        rx = abs(x2 - x1) / 2
        s.append("<path d='M %d %d A %.1f %d 0 0 0 %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1, ly, rx, ry, x2, ly, GREEN))
        s.append("<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2.5' "
                 "stroke-linejoin='round'/>" % (x2 - 5, ly - 10, x2, ly - 2, x2 + 5, ly - 10, GREEN))
        s.append(text((x1 + x2) / 2, ly - ry - 7, MINUS + str(j), 15, col=GREEN))
    ticks = [str(start)] + [None] * (len(jumps) - 1) + [end_label]
    for x, t in zip(xs, ticks):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, ly - 6, x, ly + 6, INK))
        if t is not None:
            s.append(text(x, ly + 24, t, 16, col=RED if t == "?" else INK))
    return svg_wrap(W, H, "".join(s), "open number line from %d, jumping back %s" % (
        start, ", ".join("minus %d" % j for j in jumps)))


TSP = 36                         # space between tens on the 0-100 line


def tens_line_svg(dot=None, back=0, end_label=None):
    """Number line 0 to 100, every ten labeled. A dot at `dot`. back > 0 draws jumps of 10 back from dot."""
    m, ly = 22, 32 if back else 26
    W = 2 * m + 10 * TSP
    H = ly + 32
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (6, ly, W - 6, ly, INK),
         "<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2.5'/>"
         % (14, ly - 6, 6, ly, 14, ly + 6, INK),
         "<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2.5'/>"
         % (W - 14, ly - 6, W - 6, ly, W - 14, ly + 6, INK)]
    X = lambda v: m + v // 10 * TSP
    for k in range(back):
        x1, x2 = X(dot - 10 * k), X(dot - 10 * (k + 1))
        s.append("<path d='M %d %d A %.1f %d 0 0 0 %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1, ly - 2, TSP / 2, 18, x2, ly - 2, GREEN))
        s.append("<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2.5' "
                 "stroke-linejoin='round'/>" % (x2 - 5, ly - 11, x2, ly - 3, x2 + 5, ly - 11, GREEN))
    for v in range(0, 101, 10):
        x = X(v)
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, ly - 7, x, ly + 7, INK))
        s.append(text(x, ly + 26, str(v), 15))
    if dot is not None:
        s.append("<circle cx='%d' cy='%d' r='6' fill='%s'/>" % (X(dot), ly, RED))
    return svg_wrap(W, H, "".join(s), "number line from 0 to 100 by tens" + (" with a dot at %d" % dot if dot else ""))


# ------------------------------------------------------------ typical mistakes
def wrong_diffs(a, b, rnd):
    """Wrong answers for a − b from real mistakes. First: dropping the zero (70 − 30 = 4)."""
    d = a - b
    rest = [a - b // 10,          # took away ones, not tens: 70 − 3 = 67
            d + 10,               # counted one jump too few
            d - 10,               # counted one jump too many
            a + b]                # added
    rnd.shuffle(rest)
    return [d // 10] + rest + [b, d * 10]


def tens_e(a, b):
    d = a - b
    return "%d is %s. %d is %s. %s %s %s = %s. So %s = <b>%d</b>." % (
        a, tens(a // 10), b, tens(b // 10), tens(a // 10), MINUS, tens(b // 10), tens(d // 10), sub(a, b), d)


ALL = [(a, b) for a in range(20, 100, 10) for b in range(10, a, 10)]   # 36 pairs, no zero answers


def pick_pairs(rnd, k, ok=lambda a, b: True):
    pool = [p for p in ALL if ok(*p)]
    return rnd.sample(pool, k)


# ============================================================ set 1: take away ten rods
def set_rods(rnd):
    pairs = pick_pairs(rnd, 20, lambda a, b: a <= 90)
    pairs.sort(key=lambda p: (p[0] + p[1], p[0]))
    its = []
    kinds = ["x", "x", "x", "t", "x", "x", "w", "x", "x", "t", "x", "x", "w", "x", "x", "t", "x", "x", "w", "x"]
    for (a, b), k in zip(pairs, kinds):
        ta, tb, d = a // 10, b // 10, a - b
        pic = fig(rods_svg(ta, tb))
        if k == "x":
            q = pic + "Each rod is 10. Some rods are crossed out. What is %s?" % sub(a, b)
            e = ("There are %d rods. That is %d. %s %s crossed out. Count the rods left: %s. %s = <b>%d</b>."
                 % (ta, a, cap(tens(tb)).replace(" tens", "").replace(" ten", ""), "rod is" if tb == 1 else "rods are",
                    tens(d // 10), sub(a, b), d))
            its.append(mcq_n(q, d, wrong_diffs(a, b, rnd), e))
        elif k == "t":
            q = pic + "There are %s. %s crossed out. How many tens are left?" % (
                tens(ta), "1 ten is" if tb == 1 else "%d tens are" % tb)
            e = "%s %s %s = %s. That is %d." % (tens(ta), MINUS, tens(tb), tens(d // 10), d)
            wrong = [tens(d), tens(d // 10 + 1), tens(ta + tb), tens(tb)]
            if d // 10 > 1:
                wrong.append(tens(d // 10 - 1))
            its.append(mcq(q, tens(d // 10), wrong, cap(e)))
        else:
            q = pic + "Which subtraction does the picture show?"
            e = ("There are %d rods, so start at %d. %d %s crossed out, so take away %d. The picture shows %s = %d."
                 % (ta, a, tb, "rod is" if tb == 1 else "rods are", b, sub(a, b), d))
            wrong = ["%d + %d" % (a, b) if a + b <= TOP else None, sub(a, tb), sub(a, d) if d != b else None,
                     sub(d, b) if d > b else None, sub(a, b + 10) if b + 10 < a else sub(a, b - 10)]
            its.append(mcq(q, sub(a, b), wrong, e))
    return {"title": "Take away ten rods", "items": its}


# ============================================================ set 2: tens facts
def set_facts(rnd):
    its = []
    # a tens − b tens = ? tens (5)
    for a, b in pick_pairs(rnd, 5, lambda a, b: a <= 70):
        ta, tb, td = a // 10, b // 10, (a - b) // 10
        q = "%s %s %s = ?" % (tens(ta), MINUS, tens(tb))
        e = "Count the tens like ones. %d %s %d = %d. So %s %s %s = <b>%s</b>." % (
            ta, MINUS, tb, td, tens(ta), MINUS, tens(tb), tens(td))
        wrong = [tens(td + 1), "%d ones" % td if td > 1 else "1 one", tens(ta + tb), tens(td * 10)]
        its.append(mcq(q, tens(td), wrong, e))
    # basic fact helps (6)
    for a, b in pick_pairs(rnd, 6):
        ta, tb, d = a // 10, b // 10, a - b
        q = "%d %s %d = %d. So %s = ?" % (ta, MINUS, tb, d // 10, sub(a, b))
        e = "%d %s %d = %d, so %s %s %s = %s. %s = <b>%d</b>." % (
            ta, MINUS, tb, d // 10, tens(ta), MINUS, tens(tb), tens(d // 10), cap(tens(d // 10)), d)
        its.append(mcq_n(q, d, wrong_diffs(a, b, rnd), e))
    # which fact helps (4)
    for a, b in pick_pairs(rnd, 4, lambda a, b: a < 90):
        ta, tb = a // 10, b // 10
        q = "Which fact helps you find %s?" % sub(a, b)
        e = "%d is %s and %d is %s. So use %d %s %d." % (a, tens(ta), b, tens(tb), ta, MINUS, tb)
        wrong = ["%d + %d" % (ta, tb), sub(a, tb), sub(ta + 1, tb), sub(ta, tb + 1) if tb + 1 < ta else None]
        its.append(mcq(q, sub(ta, tb), wrong, e))
    # same as (5)
    for a, b in pick_pairs(rnd, 5, lambda a, b: b >= 20 and a - b >= 20):
        ta, tb = a // 10, b // 10
        q = "Which is the same as %s?" % sub(a, b)
        e = "%d is %s. %d is %s. So %s is %s %s %s." % (a, tens(ta), b, tens(tb), sub(a, b), tens(ta), MINUS, tens(tb))
        right = "%s %s %s" % (tens(ta), MINUS, tens(tb))
        wrong = ["%d ones %s %d ones" % (ta, MINUS, tb), "%s + %s" % (tens(ta), tens(tb)),
                 "%s %s %d ones" % (tens(ta), MINUS, tb)]
        its.append(mcq(q, right, wrong, e))
    t, b, w, s = its[0:5], its[5:11], its[11:15], its[15:20]
    order = t[:2] + b[:2] + t[2:3] + w[:1] + b[2:3] + t[3:4] + s[:2] + w[1:2] + b[3:4] + t[4:] + s[2:3] \
        + w[2:3] + b[4:5] + s[3:4] + w[3:] + b[5:] + s[4:]
    assert len(order) == 20
    return {"title": "Use tens facts", "items": order}


# ============================================================ set 3: count back on a number line
def set_lines(rnd):
    its = []
    # open line with jumps of 10 (6)
    for a, b in pick_pairs(rnd, 6, lambda a, b: b <= 40):
        n, d = b // 10, a - b
        q = fig(open_line_svg(a, [10] * n)) + "Start at %d. Jump back by tens. What is %s?" % (a, sub(a, b))
        steps = ", ".join(str(a - 10 * k) for k in range(1, n + 1))
        e = "Start at %d. Make %d %s back: %s. You land on <b>%d</b>." % (a, n, "jump" if n == 1 else "jumps", steps, d)
        its.append(mcq_n(q, d, wrong_diffs(a, b, rnd), e))
    # open line, one big jump (3)
    for a, b in pick_pairs(rnd, 3, lambda a, b: b >= 30):
        d = a - b
        q = fig(open_line_svg(a, [b])) + "Start at %d. Jump back %d in one jump. Where do you land?" % (a, b)
        e = "%d is %s. Jump back %s from %d. %s = <b>%d</b>." % (b, tens(b // 10), tens(b // 10), a, sub(a, b), d)
        its.append(mcq_n(q, d, wrong_diffs(a, b, rnd), e))
    # 0-100 line with a dot (4)
    for a, b in pick_pairs(rnd, 4, lambda a, b: a >= 50):
        n, d = b // 10, a - b
        q = fig(tens_line_svg(dot=a)) + "Start at the dot. Count back %s. Where do you land?" % tens(n)
        steps = ", ".join(str(a - 10 * k) for k in range(1, n + 1))
        e = "The dot is at %d. Count back %s: %s. You land on <b>%d</b>." % (a, tens(n), steps, d)
        its.append(mcq_n(q, d, wrong_diffs(a, b, rnd), e))
    # what does the line show (4)
    for a, b in pick_pairs(rnd, 4, lambda a, b: 20 <= b <= 40):
        n, d = b // 10, a - b
        q = fig(open_line_svg(a, [10] * n, end_label=str(d))) + "Which subtraction does the number line show?"
        e = "It starts at %d. There %s %d %s of 10. That is %d. %s = %d." % (
            a, "is" if n == 1 else "are", n, "jump" if n == 1 else "jumps", b, sub(a, b), d)
        right = "%s = %d" % (sub(a, b), d)
        wrong = ["%s = %d" % (sub(a, n), a - n), "%d + %d = %d" % (a, b, a + b) if a + b <= TOP else None,
                 "%s = %d" % (sub(a, b + 10), d - 10) if d > 10 else None,
                 "%s = %d" % (sub(a, b - 10), d + 10)]
        its.append(mcq(q, right, wrong, e))
    # count back in words (3)
    for a, b in pick_pairs(rnd, 3, lambda a, b: 20 <= b <= 30):
        n, d = b // 10, a - b
        shown = ", ".join(str(a - 10 * k) for k in range(n))
        q = "Count back by tens: %s, ☐. What number goes in the box?" % shown
        e = "Each step back takes away 10: %s. The box is <b>%d</b>. So %s = %d." % (
            ", ".join(str(a - 10 * k) for k in range(n + 1)), d, sub(a, b), d)
        its.append(mcq_n(q, d, [d + 10, a - b // 10, d // 10, d - 10, a + b], e))
    o, big, dot, show, cnt = its[0:6], its[6:9], its[9:13], its[13:17], its[17:20]
    order = o[:2] + cnt[:1] + o[2:3] + dot[:1] + o[3:4] + show[:1] + dot[1:2] + cnt[1:2] + o[4:5] + big[:1] \
        + show[1:2] + dot[2:3] + o[5:] + big[1:2] + show[2:3] + cnt[2:] + dot[3:] + big[2:] + show[3:]
    assert len(order) == 20
    return {"title": "Count back on a number line", "items": order}


# ============================================================ set 4: think addition
def set_think_add(rnd, P):
    its = []
    # a − b = ? think b + ? = a (6)
    for a, b in pick_pairs(rnd, 6):
        d = a - b
        q = "%s = ?<br>Think: %d + ☐ = %d." % (sub(a, b), b, a)
        e = "Count up from %d to %d by tens. %d + %d = %d. So %s = <b>%d</b>." % (b, a, b, d, a, sub(a, b), d)
        its.append(mcq_n(q, d, wrong_diffs(a, b, rnd), e))
    # a − ? = d (5)
    for a, b in pick_pairs(rnd, 5, lambda a, b: a - b != b):
        d = a - b
        q = "%d %s ☐ = %d. What number goes in the box?" % (a, MINUS, d)
        e = "Think addition: %d + ☐ = %d. %d + %d = %d. So %s = %d. The box is <b>%d</b>." % (d, a, d, b, a, sub(a, b), d, b)
        its.append(mcq_n(q, b, [b // 10, a + d, d, b + 10, b - 10], e))
    # ? − b = d (3)
    for a, b in pick_pairs(rnd, 3, lambda a, b: a - b > b):
        d = a - b
        q = "☐ %s %d = %d. What number goes in the box?" % (MINUS, b, d)
        e = ("Start with the box. Take away %d and %d is left. So add them back: %d + %d = %d. "
             "Check: %s = %d. The box is <b>%d</b>." % (b, d, d, b, a, sub(a, b), d, a))
        its.append(mcq_n(q, a, [d - b, a // 10, a + 10, a - 10], e))
    # which addition checks (3)
    for a, b in pick_pairs(rnd, 3, lambda a, b: a - b != b):
        d = a - b
        q = "Which addition fact checks %s = %d?" % (sub(a, b), d)
        e = "Add the answer and the part you took away. %d + %d = %d. You get back to %d, so %s = %d is right." % (
            d, b, a, a, sub(a, b), d)
        right = "%d + %d = %d" % (d, b, a)
        wrong = ["%d + %d = %d" % (a, b, a + b) if a + b <= TOP else None, "%s = %d" % (sub(d, b), d - b) if d > b else None,
                 "%d + %d = %d" % (a, d, a + d) if a + d <= TOP else None, "%d + %d = %d" % (d, b + 10, a + 10),
                 "%d + %d = %d" % (d // 10, b, d // 10 + b)]
        its.append(mcq(q, right, wrong, e))
    # fix a mistake (3)
    for (a, b), bad in zip([(70, 30), (80, 50), (60, 20)], ["drop", "ones", "add"]):
        d = a - b
        name, she, her = P.next()
        if bad == "drop":
            got, why = d // 10, "%s forgot the 0. %s is %s, not %d." % (cap(she), cap(tens(d // 10)), d, d // 10)
        elif bad == "ones":
            got, why = a - b // 10, "%s took away %d ones. But %d is %s, so take away %s." % (
                cap(she), b // 10, b, tens(b // 10), tens(b // 10))
        else:
            got, why = a + b, "%s added. To take away, count back %s from %d." % (cap(she), tens(b // 10), a)
        q = "%s says %s = %d. That is not right. What is %s?" % (name, sub(a, b), got, sub(a, b))
        e = "%s %s = <b>%d</b>. Check: %d + %d = %d." % (why, sub(a, b), d, d, b, a)
        its.append(mcq_n(q, d, [got] + wrong_diffs(a, b, rnd), e))
    s1, s2, s3, s4, s5 = its[0:6], its[6:11], its[11:14], its[14:17], its[17:20]
    order = s1[:2] + s4[:1] + s1[2:3] + s2[:1] + s5[:1] + s1[3:4] + s2[1:2] + s4[1:2] + s3[:1] + s1[4:5] \
        + s2[2:3] + s5[1:2] + s3[1:2] + s2[3:4] + s1[5:] + s4[2:] + s3[2:] + s5[2:] + s2[4:]
    assert len(order) == 20
    return {"title": "Think addition to subtract", "items": order}


# ============================================================ set 5: word problems
def set_stories(rnd, P):
    its = []

    def story(q, a, b, e, cands=None, money=False, extra=()):
        d = a - b
        c = list(extra) + (cands if cands is not None else wrong_diffs(a, b, rnd))
        its.append(mcq_n(q, d, c, e, fmt="%d¢" if money else "%d"))

    def person():
        n, she, her = P.next()
        return n, she, cap(she), her

    n, she, She, her = person()
    story("%s has 60 beads. %s uses 20 beads. How many beads are left?" % (n, She), 60, 20,
          "Take away: %s = <b>40</b>. %s has 40 beads left." % (sub(60, 20), n))
    story("There are 30 ducks in a pond. 10 ducks fly away. How many ducks are left?", 30, 10,
          "%s = <b>20</b>. 20 ducks are left." % sub(30, 10))
    n, she, She, her = person()
    story("%s has 8 bags of beads. Each bag has 10 beads. %s gives away 3 bags. "
          "How many beads does %s have now?" % (n, She, she), 80, 30,
          "8 bags = 80 beads. 3 bags = 30 beads. %s = <b>50</b>. Watch out: 5 is the number of bags, not beads." % sub(80, 30),
          extra=[5])
    story("A box has 40 crayons. 10 crayons are broken. How many crayons are not broken?", 40, 10,
          "%s = <b>30</b>. 30 crayons are not broken." % sub(40, 10))
    n, she, She, her = person()
    its_before = len(its)
    story(fig(dimes_svg(7)) + "%s has these dimes. A dime is 10¢. %s spends 30¢. How much money is left?" % (n, She),
          70, 30, "Count the dimes by tens: 7 dimes = 70¢. 70¢ − 30¢ = <b>40¢</b>.", money=True)
    n, she, She, her = person()
    story("A book has 90 pages. %s has read 40 pages. How many pages are left to read?" % n, 90, 40,
          "%s = <b>50</b>. %s has 50 pages left to read." % (sub(90, 40), n))
    n, she, She, her = person()
    story("Stickers come in sheets of 10. %s has 6 sheets. %s uses 4 sheets. How many stickers are left?" % (n, She),
          60, 40, "6 sheets = 60 stickers. 4 sheets = 40 stickers. %s = <b>20</b>. 2 is the number of sheets left, "
          "not stickers." % sub(60, 40), extra=[2])
    story("There are 50 kids on the playground. 20 kids go inside. How many kids are still outside?", 50, 20,
          "%s = <b>30</b>. 30 kids are still outside." % sub(50, 20))
    n, she, She, her = person()
    story("%s has 90¢. A toy car costs 60¢. %s buys it. How much money does %s have left?" % (n, She, she), 90, 60,
          "90¢ − 60¢ = <b>30¢</b>. Think: 9 dimes take away 6 dimes is 3 dimes.", money=True)
    story("A farm has 80 chickens. 50 chickens are in the barn. The rest are outside. How many chickens are outside?",
          80, 50, "%s = <b>30</b>. Check: 50 + 30 = 80." % sub(80, 50))
    n, she, She, her = person()
    m, he2, He2, his2 = person()
    story("%s has 80 blocks. %s has 30 blocks. How many more blocks does %s have than %s?" % (n, m, n, m), 80, 30,
          "Find the difference. %s = <b>50</b>. %s has 50 more blocks." % (sub(80, 30), n))
    n, she, She, her = person()
    story(fig(dimes_svg(8)) + "%s has these dimes. %s buys a ball for 50¢. How much money is left?" % (n, She),
          80, 50, "8 dimes = 80¢. 80¢ − 50¢ = <b>30¢</b>.", money=True)
    story("A baker makes 60 muffins. 30 muffins are sold. How many muffins are left?", 60, 30,
          "%s = <b>30</b>. 30 muffins are left." % sub(60, 30))
    n, she, She, her = person()
    story("%s needs 70 points to win. %s has 40 points. How many more points does %s need?" % (n, She, she), 70, 40,
          "Think: 40 + ☐ = 70. Count up by tens: 50, 60, 70. That is 3 tens. %s needs <b>30</b> more points." % n)
    story("There are 90 chairs in the gym. Kids sit in 70 chairs. How many chairs are empty?", 90, 70,
          "%s = <b>20</b>. 20 chairs are empty." % sub(90, 70))
    n, she, She, her = person()
    story("%s picks 50 apples. %s puts 10 apples in each bag. %s gives away 2 bags. How many apples are left?"
          % (n, She, She), 50, 20, "2 bags = 20 apples. %s = <b>30</b>." % sub(50, 20), extra=[3])
    n, she, She, her = person()
    m, he2, He2, his2 = person()
    story("%s has 20 toy cars. %s has 60 toy cars. How many fewer cars does %s have than %s?" % (n, m, n, m), 60, 20,
          "Compare. Take the smaller number from the bigger one: %s = <b>40</b>. %s has 40 fewer cars." % (sub(60, 20), n))
    story("There are 70 books on a shelf. Kids take 60 books. How many books are on the shelf now?", 70, 60,
          "%s = <b>10</b>. 7 tens take away 6 tens is 1 ten. 10 books are left." % sub(70, 60))
    n, she, She, her = person()
    story("%s has 40¢. %s gets 3 more dimes. Then %s spends 50¢. How much money is left?" % (n, She, she), 70, 50,
          "3 dimes = 30¢. 40¢ + 30¢ = 70¢. 70¢ − 50¢ = <b>20¢</b>.", money=True, extra=[10])
    # start unknown: the answer is a sum, so build it by hand
    n, she, She, her = person()
    its.append(mcq_n("%s had some marbles. %s lost 20 marbles. Now %s has 50 marbles. "
                     "How many marbles did %s have at first?" % (n, She, she, she), 70, [30, 60, 80, 7],
                     "Put the lost marbles back. 50 + 20 = <b>70</b>. Check: %s = 50. "
                     "Do not subtract 50 %s 20 here." % (sub(70, 20), MINUS)))
    assert len(its) == 20
    return {"title": "Word problems with tens", "items": its}


# ------------------------------------------------------------ lesson
def body_html():
    return (
        "<h2>Take away tens like ones</h2>"
        "<p>70 is <b>7 tens</b>. 30 is <b>3 tens</b>. To find 70 − 30, take away 3 tens. "
        "You know 7 − 3 = 4. So 7 tens − 3 tens = 4 tens. That is <b>40</b>.</p>"
        "<figure class='sn-fig'>" + rods_svg(7, 3) +
        "<figcaption>7 rods of ten. Cross out 3 rods. 4 rods are left. 70 − 30 = 40.</figcaption></figure>"
        + ex("Use a fact you know", "What is 90 − 50?",
             "9 − 5 = 4. So 9 tens − 5 tens = 4 tens.", "40") +
        "<h2>Count back by tens</h2>"
        "<p>On a number line, jump back 10 at a time. Count the jumps.</p>"
        "<figure class='sn-fig'>" + tens_line_svg(dot=70, back=3) +
        "<figcaption>Start at 70. Jump back 3 tens: 60, 50, 40. You land on 40.</figcaption></figure>"
        "<h2>Think addition</h2>"
        "<p>Subtraction and addition go together. To find 80 − 50, ask: 50 + what makes 80? "
        "Count up by tens: 60, 70, 80. That is 3 tens.</p>"
        + ex("Missing number", "80 − ☐ = 50",
             "Think: 50 + ☐ = 80. 50 + 30 = 80.", "30") +
        ex("Word problem", "Leo has 6 dimes. That is 60¢. He spends 20¢. How much is left?",
           "60¢ − 20¢ = 40¢. 6 dimes take away 2 dimes is 4 dimes.", "40¢") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["70 − 30 = 4 (the 0 is lost)", "4 tens is 40. Write the 0"],
            ["70 − 30 = 67 (took away 3 ones)", "30 is 3 tens. Take away 3 tens"],
            ["70 − 30 = 100 (added)", "Take away means count back"],
            ["80 − ☐ = 50, writing 130", "Think 50 + ☐ = 80. The box is 30"],
        ])
    )


FAQ = [
    {"q": "How do you subtract multiples of 10 in 1st grade?",
     "a": "Think of each number as tens. 70 − 30 is 7 tens − 3 tens = 4 tens, so the answer is 40. Children use the fact 7 − 3 = 4 they already know."},
    {"q": "Why does my child write 70 − 30 = 4?",
     "a": "They did 7 − 3 and forgot that the answer counts tens. Ask “4 what?” 4 tens is 40, so write the 0."},
    {"q": "What does 1.NBT.C.6 mean?",
     "a": "It is the Common Core standard for Grade 1: subtract multiples of 10 from 10 to 90, like 60 − 20, using models, place value and the link between addition and subtraction."},
    {"q": "How can I help my child practice subtracting tens at home?",
     "a": "Use dimes or bundles of 10 straws. Show 8 bundles, take away 3, and count the tens left. Then write it as 80 − 30 = 50."},
]


def gen():
    rnd = random.Random(109)
    P = People(rnd)
    sets = [set_rods(rnd), set_facts(rnd), set_lines(rnd), set_think_add(rnd, P), set_stories(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    u = {
        "country": "us", "subject": "math", "grade": "grade-1", "slug": "subtract-multiples-of-10", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Subtract Multiples of 10 (Grade 1)",
        "seo_title": "Grade 1 Subtracting Tens Worksheets: Subtract Multiples of 10 Like 70 − 30 With Rods and Number Lines",
        "short_title": "Subtract multiples of 10",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "1.NBT.C.6",
        "standard_url": "https://www.thecorestandards.org/Math/Content/1/NBT/C/6/",
        "standard_text": "Subtract multiples of 10 in the range 10-90 from multiples of 10 in the range 10-90 (positive or zero differences), using concrete models or drawings and strategies based on place value, properties of operations, and/or the relationship between addition and subtraction; relate the strategy to a written method and explain the reasoning used.",
        "meta_desc": "Free Grade 1 worksheets for subtracting multiples of 10, like 70 − 30 and 90 − 50: take away ten rods, tens facts, count back on a number line, think addition, missing numbers and word problems with dimes. 100 practice questions with an answer key.",
        "key_big": "Subtract tens like ones: 7 tens − 3 tens = 4 tens, so 70 − 30 = 40.",
        "key_sub": "Use a fact you know (7 − 3 = 4), then write the 0, because the answer counts tens. Check by adding: 40 + 30 = 70.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "base-ten rods|open number line|number line from 0")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
