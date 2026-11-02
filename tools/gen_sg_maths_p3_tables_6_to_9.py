# -*- coding: utf-8 -*-
"""
Singapore Primary 3 Maths: Multiplication tables of 6, 7, 8 and 9 (MOE 2021 Primary Mathematics
Syllabus, Standard, Number and Algebra, Whole Numbers: "Multiplication tables of 6, 7, 8 and 9;
multiplying and dividing within the multiplication tables; mental calculation")
  python3 tools/gen_sg_maths_p3_tables_6_to_9.py
Arrays, skip counting on number lines, strategies (6 = 5 + 1, 7 = 5 + 2, 8 = double 4, 9 = 10 − 1),
related division facts, missing numbers, fact families and word problems with bar models.
Every product, quotient and missing number is checked in code. Wrong answers are real mistakes:
a neighbouring fact, one group too many or too few, adding instead of multiplying, swapped digits,
7 × 8 = 54, 6 × 9 = 56, and dividing the wrong way.
Singapore English, $ and ¢. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-3")
SLUG = "multiplication-tables-6-7-8-and-9"
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
INK = "#2b2b2b"
NOTE = "#5a5a5a"
FONT = "Arial, Helvetica, sans-serif"
NB = "\u00a0"
X = "×"
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]


# ------------------------------------------------------------ helpers
def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors (no zero or negative numbers).
    Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.lstrip("$").split(" ")[0]
        if c in seen or not c or lead.startswith(("-", "−")) or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set.
    Picture-label choices (A, B, C, D) keep their order."""
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
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    """Approximate text width in px (Arial bold)."""
    t = plain(str(t))
    return sum(0.36 if ch in " .,()" + NB else 0.62 for ch in t) * fs


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


def calc(expr):
    """Evaluate a short expression written with × and ÷ (only digits, spaces and + − × ÷)."""
    assert re.fullmatch(r"[0-9 +×÷−]+", expr), expr
    return F(eval(expr.replace(X, "*").replace("÷", "/").replace("−", "-")))


def true_fact(s):
    """'56 ÷ 7 = 8' -> True / False."""
    left, right = s.split(" = ")
    return calc(left) == calc(right)


# ------------------------------------------------------------ figures
def dots(x0, y0, rows, cols, cell, col=GREEN):
    return "".join("<circle cx='%d' cy='%d' r='%d' fill='%s'/>"
                   % (x0 + c * cell + cell // 2, y0 + r * cell + cell // 2, cell // 3, col)
                   for r in range(rows) for c in range(cols))


def array_svg(rows, cols, cell=22, split=None):
    """rows × cols array of dots. split = k draws a dashed line after k rows and labels both parts."""
    o = 6
    W = cols * cell + 2 * o
    H = rows * cell + 2 * o
    s = [dots(o, o, rows, cols, cell)]
    label = "array of %d rows with %d dots in each row" % (rows, cols)
    if split:
        y = o + split * cell
        s.append("<line x1='2' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>"
                 % (y, W - 2, y, RED))
        lx = W + 6
        s.append(text(lx, o + split * cell / 2 + 6, "%d %s %d" % (split, X, cols), 15, "start"))
        s.append(text(lx, y + (rows - split) * cell / 2 + 6, "%d %s %d" % (rows - split, X, cols), 15, "start", RED))
        W = lx + tw("%d %s %d" % (split, X, cols), 15) + 6
        label += ", split after %d rows" % split
    return svg_wrap(W, H, "".join(s), label)


GROUP_SHAPE = {6: (2, 3), 8: (2, 4), 9: (3, 3), 7: (2, 4)}


def groups_svg(g, n, cell=20, label_sizes=False):
    """g equal groups of n counters, each in a rounded box. Up to 4 boxes per row."""
    gr, gc = GROUP_SHAPE[n]
    pad, gap = 5, 10
    bw, bh = gc * cell + 2 * pad, gr * cell + 2 * pad
    per_row = min(4 if n != 8 else 3, g)
    nrows = (g + per_row - 1) // per_row
    lab = 22 if label_sizes else 0
    W = per_row * bw + (per_row - 1) * gap + 4
    H = nrows * (bh + lab) + (nrows - 1) * gap + 4
    s = []
    for i in range(g):
        r, c = divmod(i, per_row)
        x = 2 + c * (bw + gap)
        y = 2 + r * (bh + lab + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, y, bw, bh, FILL2, GREEN))
        k = 0
        for rr in range(gr):
            for cc in range(gc):
                if k < n:
                    s.append("<circle cx='%d' cy='%d' r='%d' fill='%s'/>"
                             % (x + pad + cc * cell + cell // 2, y + pad + rr * cell + cell // 2, cell // 3, GREEN))
                k += 1
        if label_sizes:
            s.append(text(x + bw / 2, y + bh + 17, str(n), 15))
    return svg_wrap(W, H, "".join(s), "%d equal groups with %d counters in each group" % (g, n))


def jumps_svg(step, n, back=False):
    """Number line from 0 to step × n with n equal jumps (forwards from 0, or backwards to 0)."""
    end = step * n
    L, R = 16, 444
    sc = (R - L) / float(end)
    yl = 64
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 8, yl, R + 8, yl, INK)]
    for v in range(0, end + 1):
        x = L + v * sc
        big = v % step == 0
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%d'/>"
                 % (x, yl - (8 if big else 4), x, yl + (8 if big else 4), INK, 2 if big else 1))
        if big:
            s.append(text(x, yl + 26, str(v), 15))
    for k in range(n):
        a, b = L + k * step * sc, L + (k + 1) * step * sc
        mid = (a + b) / 2
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                 % (a, yl - 4, mid, yl - 46, b, yl - 4, GREEN))
        tip = a if back else b
        d = 1 if back else -1
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>"
                 % (tip, yl - 3, tip + d * 9, yl - 12, tip + d * 2, yl - 14, GREEN))
    lab = "number line with %d jumps of %d %s" % (n, step, "back from %d to 0" % end if back else "from 0 to %d" % end)
    return svg_wrap(R + 16, yl + 34, "".join(s), lab)


def model_svg(rows, label, W=440):
    """Bar model drawn to scale. rows: dicts with
         name:  text at the left of the bar ('' for none)
         segs:  [(length, text inside, shaded)] drawn left to right
         over:  [(start, end, text)] brackets above the bar
         under: [(start, end, text)] brackets below the bar
       Text containing '?' is drawn red."""
    names = [r.get("name", "") for r in rows]
    nw = (max(tw(n, 15) for n in names) + 12) if any(names) else 0
    L = 8 + nw
    R = W - 10
    tot = max(sum(F(a) for a, _, _ in r["segs"]) for r in rows)
    sc = (R - L) / float(tot)
    s = []
    y = 4
    for r in rows:
        over, under = r.get("over", []), r.get("under", [])
        if over:
            y += 24
            for a, b, t in over:
                x1, x2 = L + float(a) * sc, L + float(b) * sc
                col = RED if "?" in t else INK
                s.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                         % (x1, y + 6, x1, y, x2, y, x2, y + 6, col))
                half = tw(t, 15) / 2 + 2
                cx = min(max((x1 + x2) / 2, half + 2), W - half - 2)
                s.append(text(cx, y - 6, t, 15, col=col))
            y += 8
        y0 = y
        bh = 34
        x = L
        for a, t, sh in r["segs"]:
            w = float(a) * sc
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x, y0, w, bh, FILL if sh else "#ffffff", INK))
            if t:
                assert tw(t, 14) + 4 <= w, ("text too wide for segment", t, w)
                s.append(text(x + w / 2, y0 + bh / 2 + 5, t, 14, col=RED if "?" in t else INK))
            x += w
        if r.get("name"):
            s.append(text(8, y0 + bh / 2 + 5, r["name"], 15, "start"))
        y = y0 + bh
        if under:
            for a, b, t in under:
                x1, x2 = L + float(a) * sc, L + float(b) * sc
                col = RED if "?" in t else INK
                s.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                         % (x1, y + 4, x1, y + 10, x2, y + 10, x2, y + 4, col))
                half = tw(t, 15) / 2 + 2
                cx = min(max((x1 + x2) / 2, half + 2), W - half - 2)
                s.append(text(cx, y + 28, t, 15, col=col))
            y += 32
        y += 10
    return svg_wrap(W, y - 4, "".join(s), label)


def units(n, each=""):
    return [(1, each, True) for _ in range(n)]


# ------------------------------------------------------------ strategies
def tip(a, b):
    """Strategy for a × b, where b is the multiplication table being practised."""
    p = a * b
    if b == 6:
        return "6 %s %d is 5 %s %d and one more %d: %d + %d = <b>%d</b>." % (X, a, X, a, a, 5 * a, a, p)
    if b == 7:
        return "7 %s %d is 5 %s %d and 2 %s %d: %d + %d = <b>%d</b>." % (X, a, X, a, X, a, 5 * a, 2 * a, p)
    if b == 8:
        return "8 %s %d is double 4 %s %d: %d + %d = <b>%d</b>." % (X, a, X, a, 4 * a, 4 * a, p)
    if b == 9:
        return "9 %s %d is 10 %s %d take away one %d: %d − %d = <b>%d</b>." % (X, a, X, a, a, 10 * a, a, p)
    raise ValueError(b)


# Products students often mix up (7 × 8 = 54, 6 × 9 = 56, 6 × 8 = 46, ...)
CONFUSE = {56: [54, 64, 58], 54: [56, 45, 64], 48: [46, 42, 56], 42: [48, 36, 49], 63: [36, 64, 72],
           72: [27, 81, 64], 49: [47, 42, 56], 36: [63, 32, 42], 64: [46, 56, 72], 81: [18, 72, 80]}


def rev(n):
    s = str(n)
    if len(s) == 2 and s[0] != s[1] and s[1] != "0":
        return int(s[::-1])
    return None


def fact_cands(a, b, rnd):
    """Real mistakes: a famous mix-up, a neighbouring fact, adding, swapped digits."""
    p = a * b
    first = [v for v in CONFUSE.get(p, []) if v != p][:1]
    pool = [a * (b + 1), a * (b - 1), (a + 1) * b, (a - 1) * b, a + b]
    r = rev(p)
    if r:
        pool.append(r)
    pool = [v for v in pool if v > 0 and v != p and v not in first]
    rnd.shuffle(pool)
    return first + pool + [p + 10, p - 10, p + 2, p - 2]


def fact_q(a, b, rnd):
    """Question shows a × b or b × a; b is the table being practised."""
    x, y = (a, b) if rnd.random() < 0.5 else (b, a)
    return mcq("%d %s %d = ?" % (x, X, y), a * b, fact_cands(a, b, rnd), tip(a, b))


def facts(b, mults, rnd):
    mults = list(mults)
    rnd.shuffle(mults)
    return [fact_q(a, b, rnd) for a in mults]


def count_q(svg_html, g, n, kind):
    p = g * n
    wrong = [g + n, (g - 1) * n, (g + 1) * n, g * (n - 1)]
    if kind == "groups":
        e = "There are %d groups of %d. %d %s %d = <b>%d</b>." % (g, n, g, X, n, p)
        ask = "How many counters are there altogether?"
    else:
        e = "There are %d rows with %d dots in each row. %d %s %d = <b>%d</b>." % (g, n, g, X, n, p)
        ask = "How many dots are in this array?"
    e += " Count in %ds: %s." % (n, ", ".join(str(n * k) for k in range(1, g + 1)))
    return mcq(fig(svg_html) + ask, p, wrong, e)


def seq_q(seq, step, wrong, extra=""):
    gaps = [seq[i + 1] - seq[i] for i in range(len(seq) - 1) if seq[i] is not None and seq[i + 1] is not None]
    assert all(g == step for g in gaps), seq
    if None in seq:
        i = seq.index(None)
        ans = seq[i - 1] + step
        assert i + 1 >= len(seq) or seq[i + 1] == ans + step
        show = ", ".join("?" if v is None else str(v) for v in seq)
        e = "Each number is %d more than the one before: %d + %d = <b>%d</b>. %s" % (step, seq[i - 1], step, ans, extra)
        return mcq("Count in %ds. What is the missing number?<br>%s" % (step, show), ans, wrong, e.strip())
    ans = seq[-1] + step
    assert ans % step == 0 and ans not in wrong
    e = "Each number is %d more than the one before: %d + %d = <b>%d</b>. %s" % (step, seq[-1], step, ans, extra)
    return mcq("Count in %ds. What comes next?<br>%s, ?" % (step, ", ".join(map(str, seq))), ans, wrong, e.strip())


def multiple_q(ask, right, wrong, n, inside):
    assert (right % n == 0) == inside and all((w % n == 0) != inside for w in wrong)
    lst = ", ".join(str(n * k) for k in range(1, 11))
    e = "The multiplication table of %d goes %s. <b>%d</b> %s." % (
        n, lst, right, "is in the list (%d %s %d)" % (right // n, X, n) if inside else "is not in the list")
    return mcq(ask, right, wrong, e)


def jumps_q(step, n):
    p = step * n
    right = "%d %s %d = %d" % (n, X, step, p)
    wrong = ["%d %s %d = %d" % (n + 1, X, step, (n + 1) * step), "%d + %d = %d" % (n, step, n + step),
             "%d %s %d = %d" % (n, X, step - 1, n * (step - 1))]
    assert true_fact(right) and all(true_fact(w) for w in wrong)
    e = ("Count the jumps, not the marks: there are %d jumps of %d from 0 to %d. So <b>%d %s %d = %d</b>. "
         "%d %s %d counts the 0 as a jump." % (n, step, p, n, X, step, p, n + 1, X, step))
    return mcq(fig(jumps_svg(step, n)) + "Which multiplication does this number line show?", right, wrong, e)


# ============================================================ set 1: tables of 6 and 7
def set_six_seven(rnd):
    its = [
        count_q(array_svg(4, 6), 4, 6, "array"),
        count_q(array_svg(3, 7), 3, 7, "array"),
        jumps_q(6, 5),
        jumps_q(7, 4),
    ]
    r, c = 6, 7
    right = "%d %s %d" % (r, X, c)
    wrong = ["%d + %d" % (r, c), "%d %s %d" % (r, X, c - 1), "%d %s %d" % (r - 1, X, c)]
    assert all(calc(w) != r * c for w in wrong)
    its.append(mcq(fig(array_svg(r, c)) + "Which multiplication matches this array?", right, wrong,
                   "There are %d rows with %d dots in each row: <b>%d %s %d</b> = %d. %d + %d only adds the two numbers."
                   % (r, c, r, X, c, r * c, r, c)))
    # split arrays: 6 = 5 + 1, 7 = 5 + 2
    assert 5 * 8 + 8 == 48 and 5 * 6 + 2 * 6 == 42
    its.append(mcq(fig(array_svg(6, 8, split=5)) + "5 %s 8 = 40. Use the array to find 6 %s 8." % (X, X),
                   48, [46, 41, 56, 40],
                   "6 rows of 8 is 5 rows of 8 and 1 more row of 8: 40 + 8 = <b>48</b>. 41 adds 1, not one more row of 8."))
    its.append(mcq(fig(array_svg(7, 6, split=5)) + "5 %s 6 = 30 and 2 %s 6 = 12. What is 7 %s 6?" % (X, X, X),
                   42, [36, 48, 32, 13],
                   "7 rows of 6 is 5 rows and 2 more rows: 30 + 12 = <b>42</b>. 36 is only 6 rows (6 %s 6)." % X))
    its.append(seq_q([18, 24, 30], 6, [35, 32, 37], "So 6 %s 6 = 36." % X))
    its.append(seq_q([28, 35, 42], 7, [48, 46, 52], "So 7 %s 7 = 49." % X))
    its.append(seq_q([7, 14, None, 28], 7, [20, 24, 18], "So 7 %s 3 = 21." % X))
    its += facts(6, [3, 4, 6, 7], rnd)
    its += facts(7, [3, 5, 7, 8], rnd)
    its.append(multiple_q("Which number is in the multiplication table of 7?", 49, [45, 48, 52], 7, True))
    its.append(multiple_q("Which number is <b>not</b> in the multiplication table of 6?", 26, [24, 36, 42], 6, False))
    assert len(its) == 20, len(its)
    return {"title": "Tables of 6 and 7: arrays and skip counting", "items": its}


# ============================================================ set 2: tables of 8 and 9
def double_q(a):
    k, ans = 4 * a, 8 * a
    e = ("8 is double 4, so 8 %s %d is double 4 %s %d: %d + %d = <b>%d</b>." % (X, a, X, a, k, k, ans))
    return mcq("4 %s %d = %d. Double it to find 8 %s %d." % (X, a, k, X, a), ans, [k + 4, k + a, k + 8, 4 * k], e)


def nine_q(a):
    t, ans = 10 * a, 9 * a
    assert ans == t - a
    e = ("9 groups is 1 group less than 10 groups. %d − %d = <b>%d</b>. %d takes away 1 instead of one %d."
         % (t, a, ans, t - 1, a))
    return mcq("10 %s %d = %d. Take away one %d to find 9 %s %d." % (X, a, t, a, X, a), ans,
               [t - 1, t - 10, t + a], e)


def pattern_q(a, wrong):
    ans = 9 * a
    assert ans // 10 == a - 1 and ans // 10 + ans % 10 == 9 and ans not in wrong
    e = ("The tens digit is one less than %d, so it is %d. The ones digit makes the sum 9: %d + %d = 9. "
         "So 9 %s %d = <b>%d</b>." % (a, a - 1, a - 1, 9 - (a - 1), X, a, ans))
    return mcq("In the table of 9, the tens digit is one less than the number you multiply by, "
               "and the two digits add up to 9. Use this to find 9 %s %d." % (X, a), ans, wrong, e)


def set_eight_nine(rnd):
    its = [double_q(6), double_q(9), nine_q(4), nine_q(8)]
    its.append(pattern_q(7, [62, 56, 72]))
    its.append(pattern_q(6, [53, 56, 45]))
    nines = ", ".join(str(9 * k) for k in range(1, 7))
    its.append(mcq("Look at the table of 9: %s. The tens digit goes up by 1 each time. "
                   "What happens to the ones digit?" % nines,
                   "It goes down by 1", ["It goes up by 1", "It stays the same", "It goes down by 9"],
                   "The ones digits are 9, 8, 7, 6, 5, 4. Each one is <b>1 less</b>. "
                   "Adding 9 is adding 10 and taking away 1."))
    its.append(seq_q([32, 40, 48], 8, [54, 58, 64], "So 8 %s 7 = 56." % X))
    its.append(seq_q([45, 54, 63], 9, [71, 73, 81], "So 9 %s 8 = 72." % X))
    its.append(count_q(groups_svg(4, 9), 4, 9, "groups"))
    its.append(count_q(groups_svg(5, 8), 5, 8, "groups"))
    its += facts(8, [3, 4, 8], rnd)
    its += facts(9, [5, 9], rnd)
    its.append(mcq("10 %s 9 = ?" % X, 90, [19, 99, 81, 80], "10 groups of 9 is 9 tens: 10 %s 9 = <b>90</b>. 19 adds instead of multiplies." % X))
    its.append(mcq("9 %s 3 = ?" % X, 27, [72, 24, 12, 30], tip(3, 9) + " 72 has the digits the wrong way round."))
    its.append(multiple_q("Which number is in the multiplication table of 9?", 81, [80, 79, 91], 9, True))
    its.append(multiple_q("Which number is <b>not</b> in the multiplication table of 8?", 46, [48, 64, 32], 8, False))
    assert len(its) == 20, len(its)
    return {"title": "Tables of 8 and 9: doubling and patterns", "items": its}


# ============================================================ set 3: related division facts
def div_q(p, d):
    q = p // d
    assert q * d == p
    e = "Think: %d %s ? = %d. %d %s %d = %d, so %d ÷ %d = <b>%d</b>." % (d, X, p, d, X, q, p, p, d, q)
    return mcq("%d ÷ %d = ?" % (p, d), q, [q + 1, q - 1, d, p - d, p], e)


def helper_q(p, d, wrong):
    q = p // d
    right = "%d %s %d = %d" % (d, X, q, p)
    assert true_fact(right) and all(true_fact(w) for w in wrong)
    e = "Division is the inverse of multiplication. %d ÷ %d asks: %d times what makes %d? <b>%s</b>, so %d ÷ %d = %d." % (
        p, d, d, p, right, p, d, q)
    return mcq("Which multiplication fact helps you find %d ÷ %d?" % (p, d), right, wrong, e)


def fact_true_q(a, b, wrong):
    p = a * b
    right = "%d ÷ %d = %d" % (p, a, b)
    assert true_fact(right) and not any(true_fact(w) for w in wrong)
    e = ("%d %s %d = %d, so <b>%d ÷ %d = %d</b> and %d ÷ %d = %d. "
         "Division starts with the biggest number, %d." % (a, X, b, p, p, a, b, p, b, a, p))
    return mcq("%d %s %d = %d. Which division fact is also true?" % (a, X, b, p), right, wrong, e)


def fix_q(name, he, p, d, wrong):
    q = p // d
    right = "%d ÷ %d = %d" % (p, d, q)
    assert true_fact(right) and not any(true_fact(w) for w in wrong)
    e = ("%s divided the wrong way. Start with the total, %d, and divide it by %d: <b>%s</b>. "
         "Check: %d %s %d = %d." % (cap(he), p, d, right, d, X, q, p))
    return mcq("%s writes %d ÷ %d = %d. What should %s write?" % (name, d, p, q, he), right, wrong, e)


def set_division(rnd, P):
    its = [div_q(p, d) for p, d in
           [(42, 6), (56, 7), (48, 8), (63, 9), (54, 6), (72, 8), (49, 7), (36, 9), (30, 6), (64, 8), (45, 9)]]
    its.append(helper_q(63, 9, ["9 %s 6 = 54" % X, "7 %s 8 = 56" % X, "9 + 54 = 63"]))
    its.append(helper_q(56, 8, ["8 %s 6 = 48" % X, "6 %s 9 = 54" % X, "8 + 48 = 56"]))
    for g, n in [(6, 9), (5, 8)]:
        p = g * n
        e = "Count the groups: there are %d groups of %d. %d ÷ %d = <b>%d</b>. Check: %d %s %d = %d." % (
            g, n, p, n, g, g, X, n, p)
        its.append(mcq(fig(groups_svg(g, n)) + "%d counters are put into groups of %d. How many groups are there?" % (p, n),
                       g, [g + 1, g - 1, n, p - n], e))
    p, d = 35, 7
    its.append(mcq(fig(jumps_svg(d, p // d, back=True)) + "How many jumps of 7 does it take to go from 35 back to 0?",
                   5, [6, 7, 4, 28],
                   "Count the jumps: 35, 28, 21, 14, 7, 0 is <b>5</b> jumps. So 35 ÷ 7 = 5. 6 counts the marks instead of the jumps."))
    its.append(fact_true_q(7, 8, ["8 ÷ 56 = 7", "56 ÷ 7 = 9", "56 ÷ 8 = 6"]))
    its.append(fact_true_q(9, 6, ["9 ÷ 54 = 6", "54 ÷ 6 = 8", "54 ÷ 9 = 5"]))
    n, he, _ = P.next()
    its.append(fix_q(n, he, 63, 7, ["9 ÷ 63 = 7", "63 ÷ 7 = 8", "63 ÷ 9 = 8"]))
    n, he, _ = P.next()
    its.append(fix_q(n, he, 48, 6, ["8 ÷ 48 = 6", "48 ÷ 6 = 7", "48 ÷ 8 = 7"]))
    assert len(its) == 20, len(its)
    return {"title": "Related division facts", "items": its}


# ============================================================ set 4: missing numbers and fact families
def set_missing(rnd, P):
    its = []
    for a, b in [(6, 7), (7, 9), (8, 7)]:
        p = a * b
        e = "Ask: %d times what makes %d? %d ÷ %d = %d. Check: %d %s %d = %d, so ? = <b>%d</b>." % (
            a, p, p, a, b, a, X, b, p, b)
        its.append(mcq("%d %s ? = %d" % (a, X, p), b, [b + 1, b - 1, p - a, p + a], e))
    for a, b in [(6, 9), (8, 6), (9, 8)]:
        p = a * b
        e = "Ask: what times %d makes %d? %d ÷ %d = %d. Check: %d %s %d = %d, so ? = <b>%d</b>." % (
            b, p, p, b, a, a, X, b, p, a)
        its.append(mcq("? %s %d = %d" % (X, b, p), a, [a + 1, a - 1, p - b, p + b], e))
    for d, q in [(7, 6), (9, 8)]:
        p = d * q
        e = "Use the inverse: ? = %d %s %d = <b>%d</b>. Check: %d ÷ %d = %d. %d only adds the numbers." % (
            q, X, d, p, p, d, q, d + q)
        its.append(mcq("? ÷ %d = %d" % (d, q), p, [d + q, p + d, p - d], e))
    for p, q in [(56, 7), (54, 9)]:
        d = p // q
        e = "Ask: %d ÷ what makes %d? Think %d %s ? = %d. %d %s %d = %d, so ? = <b>%d</b>." % (
            p, q, q, X, p, q, X, d, p, d)
        its.append(mcq("%d ÷ ? = %d" % (p, q), d, [d + 1, d - 1, p - q, q], e))
    its.append(mcq("Which fact is in the fact family of 7, 9 and 63?", "63 ÷ 9 = 7",
                   ["9 ÷ 63 = 7", "63 ÷ 7 = 8", "7 %s 8 = 63" % X],
                   "The fact family is 7 %s 9 = 63, 9 %s 7 = 63, 63 ÷ 7 = 9 and <b>63 ÷ 9 = 7</b>. "
                   "Division starts with the biggest number, 63." % (X, X)))
    assert true_fact("63 ÷ 9 = 7") and not any(true_fact(w) for w in ["9 ÷ 63 = 7", "63 ÷ 7 = 8", "7 × 8 = 63"])
    for a, b, wrong in [(8, 9, [17, 81, 64]), (6, 9, [15, 56, 63])]:
        p = a * b
        its.append(mcq("A fact family uses the numbers %d, %d and ?. What is the missing number?" % (a, b),
                       p, wrong, "The biggest number in a multiplication fact family is the product: "
                       "%d %s %d = <b>%d</b>. %d is %d + %d." % (a, X, b, p, a + b, a, b)))
    its.append(mcq("9 %s 6 = 54, 6 %s 9 = 54 and 54 ÷ 9 = 6. What is the fourth fact in this fact family?" % (X, X),
                   "54 ÷ 6 = 9", ["6 ÷ 54 = 9", "9 ÷ 6 = 54", "54 ÷ 6 = 8"],
                   "The last fact divides 54 by the other number, 6: <b>54 ÷ 6 = 9</b>. Always start with 54."))
    its.append(mcq("7 %s 8 = 8 %s ?" % (X, X), 7, [8, 6, 56],
                   "You can multiply in any order: 7 %s 8 and 8 %s 7 are both 56. So ? = <b>7</b>." % (X, X)))
    n, he, his = P.next()
    its.append(mcq("%s says 7 %s 8 = 54. What is the correct answer?" % (n, X), "56", ["54", "48", "64"],
                   "7 %s 7 = 49, and one more 7 makes 49 + 7 = <b>56</b>. 54 is 6 %s 9. "
                   "Remember 5, 6, 7, 8: 56 = 7 %s 8." % (X, X, X)))
    n, he, his = P.next()
    its.append(mcq("%s says 6 %s 9 = 56. What is the correct answer?" % (n, X), "54", ["56", "45", "63"],
                   "6 %s 10 = 60. Take away one 6: 60 − 6 = <b>54</b>. 56 is 7 %s 8." % (X, X)))
    its.append(mcq("9 %s 6 = 54. So 9 %s 7 = 54 + ?" % (X, X), 9, [7, 1, 6],
                   "9 %s 7 is one more group of 9 than 9 %s 6. So add <b>9</b>: 54 + 9 = 63. "
                   "Adding 7 or 1 does not add a whole group of 9." % (X, X)))
    its.append(mcq("8 %s 6 = 48. Use this to find 8 %s 7." % (X, X), 56, [55, 49, 54],
                   "8 %s 7 is one more 8 than 8 %s 6: 48 + 8 = <b>56</b>. 55 adds 7 instead of 8." % (X, X)))
    its.append(mcq("7 %s 7 = 49. So 7 %s 6 = 49 − ?" % (X, X), 7, [6, 1, 9],
                   "7 %s 6 is one group of 7 less than 7 %s 7. So take away <b>7</b>: 49 − 7 = 42. "
                   "Taking away 6 or 1 does not take away a whole group of 7." % (X, X)))
    assert 8 * 7 == 48 + 8 and 9 * 7 == 54 + 9 and 7 * 6 == 49 - 7
    assert len(its) == 20, len(its)
    return {"title": "Missing numbers and fact families", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def w(q, ans, unit, wrong, e, check, svg=None):
        assert check == ans, (q, check, ans)
        assert ans not in wrong
        if unit == "$":
            u = lambda v: "$%d" % v
        else:
            u = lambda v: "%d %s" % (v, unit)
        its.append(mcq((fig(svg) if svg else "") + q, u(ans), [u(v) for v in wrong], e))

    nm, he, his = P.next()
    w("Mdm Wong bakes curry puffs. She puts 6 curry puffs on each tray. She bakes 8 trays. "
      "How many curry puffs does she bake?", 48, "curry puffs", [14, 42, 46],
      "8 trays of 6: 8 %s 6 = <b>48</b>. 14 is 8 + 6, which adds instead of multiplies." % X, 8 * 6)
    w("There are 7 days in a week. How many days are there in 9 weeks?", 63, "days", [16, 56, 72],
      "9 weeks of 7 days: 9 %s 7 = <b>63</b>. 9 %s 7 = 10 %s 7 − 7 = 70 − 7." % (X, X, X), 9 * 7)
    w("An octopus has 8 arms. There are 6 octopuses in a tank. How many arms are there altogether?", 48, "arms",
      [14, 40, 56], "6 %s 8 = <b>48</b>. 40 is only 5 octopuses." % X, 6 * 8)
    nm, he, his = P.next()
    w("At the hawker centre, each table has 6 stools. %s counts 7 tables. How many stools are there?" % nm,
      42, "stools", [13, 36, 48], "7 tables of 6 stools: 7 %s 6 = <b>42</b>. 5 %s 6 = 30 and 2 %s 6 = 12, 30 + 12 = 42." % (X, X, X),
      7 * 6)
    nm, he, his = P.next()
    w("For Sports Day, there are 8 teams. Each team has 7 students. How many students are there?", 56, "students",
      [54, 15, 49], "8 %s 7 = <b>56</b>. 54 is a common mistake: 54 is 6 %s 9." % (X, X), 8 * 7)
    nm, he, his = P.next()
    w("%s reads 6 pages of %s library book each day. How many pages does %s read in 9 days?" % (nm, his, he),
      54, "pages", [56, 15, 45], "9 days of 6 pages: 9 %s 6 = <b>54</b>. 56 is 7 %s 8, not 6 %s 9." % (X, X, X), 9 * 6)
    nm, he, his = P.next()
    w("%s gets 9 red packets at Chinese New Year. There is $8 in each red packet. "
      "How much money does %s get?" % (nm, he), 72, "$", [17, 64, 81],
      "9 %s $8: 10 %s 8 = 80, take away one 8: 80 − 8 = <b>$72</b>." % (X, X), 9 * 8)
    nm, he, his = P.next()
    w("A bowl of noodles costs $6. %s buys 4 bowls for %s family. How much does %s pay?" % (nm, his, he),
      24, "$", [10, 18, 30], "4 %s $6 = <b>$24</b>. $10 is 4 + 6, which adds instead of multiplies." % X, 4 * 6)

    # bar models: sharing and grouping
    nm, he, his = P.next()
    svg = model_svg([{"segs": units(8), "over": [(0, 8, "56 stickers")], "under": [(0, 1, "?")]}],
                    "bar model: 56 stickers in 8 equal units")
    w("Mrs Lim shares 56 stickers equally among 8 pupils. How many stickers does each pupil get?", 7, "stickers",
      [8, 48, 64], "8 units = 56. 1 unit = 56 ÷ 8 = <b>7</b>. Check: 8 %s 7 = 56. 48 takes away 8 instead of dividing." % X,
      56 // 8, svg)
    svg = model_svg([{"segs": units(7), "over": [(0, 7, "63 m")], "under": [(0, 1, "?")]}],
                    "bar model: 63 m in 7 equal units")
    w("Mr Tan cuts a rope 63 m long into 7 equal pieces. How long is each piece?", 9, "m",
      [8, 56, 70], "7 units = 63 m. 1 unit = 63 ÷ 7 = <b>9 m</b>. Check: 7 %s 9 = 63." % X, 63 // 7, svg)
    w("72 students stand in rows of 9 for assembly. How many rows are there?", 8, "rows",
      [9, 63, 81], "72 ÷ 9 = ? Think 9 %s ? = 72. 9 %s 8 = 72, so there are <b>8 rows</b>." % (X, X), 72 // 9)
    w("54 mandarin oranges are packed in bags of 6. How many bags are there?", 9, "bags",
      [8, 48, 60], "54 ÷ 6 = ? Think 6 %s ? = 54. 6 %s 9 = 54, so there are <b>9 bags</b>." % (X, X), 54 // 6)
    nm, he, his = P.next()
    w("%s saves $9 each week. How many weeks does %s take to save $63?" % (nm, he), 7, "weeks",
      [6, 8, 54], "63 ÷ 9 = ? 9 %s 7 = 63, so it takes <b>7 weeks</b>." % X, 63 // 9)
    w("48 chairs are set out at the void deck in 6 equal rows. How many chairs are in each row?", 8, "chairs",
      [7, 42, 54], "48 ÷ 6 = ? 6 %s 8 = 48, so there are <b>8 chairs</b> in each row." % X, 48 // 6)

    # bar models: times as many
    n1, he1, his1 = P.next()
    n2, he2, his2 = P.next()
    svg = model_svg([{"name": n1, "segs": [(1, "7", True)]},
                     {"name": n2, "segs": units(6), "over": [(0, 6, "?")]}],
                    "bar model: %s 1 unit, %s 6 units" % (n1, n2))
    w("%s has 7 marbles. %s has 6 times as many marbles as %s. How many marbles does %s have?" % (n1, n2, n1, n2),
      42, "marbles", [13, 49, 36], "1 unit = 7. 6 units = 6 %s 7 = <b>42</b>. 13 is 6 + 7, which adds instead of multiplies." % X,
      6 * 7, svg)
    n1, he1, his1 = P.next()
    n2, he2, his2 = P.next()
    svg = model_svg([{"name": n1, "segs": [(1, "8", True)]},
                     {"name": n2, "segs": units(9), "over": [(1, 9, "?")]}],
                    "bar model: %s 1 unit, %s 9 units" % (n1, n2))
    w("%s has 8 stickers. %s has 9 times as many stickers as %s. How many more stickers does %s have than %s?"
      % (n1, n2, n1, n2, n1), 64, "stickers", [72, 17, 56],
      "%s has 9 units and %s has 1 unit. The difference is 8 units: 8 %s 8 = <b>64</b>. "
      "72 is how many %s has, not how many more." % (n2, n1, X, n2), 9 * 8 - 8, svg)
    n1, he1, his1 = P.next()
    n2, he2, his2 = P.next()
    svg = model_svg([{"name": n1, "segs": units(7), "over": [(0, 7, "49 beads")]},
                     {"name": n2, "segs": [(1, "?", True)]}],
                    "bar model: %s 7 units, %s 1 unit" % (n1, n2))
    w("%s has 49 beads. %s has 7 times as many beads as %s. How many beads does %s have?" % (n1, cap(he1), n2, n2),
      7, "beads", [42, 56, 6], "7 units = 49. 1 unit = 49 ÷ 7 = <b>7</b>. %s has 7 beads. "
      "56 multiplies instead of divides." % n2, 49 // 7, svg)

    # two steps
    nm, he, his = P.next()
    w("%s buys 6 packets of stickers. There are 8 stickers in each packet. %s gives away 5 stickers. "
      "How many stickers does %s have left?" % (nm, cap(he), he), 43, "stickers", [48, 53, 9],
      "6 %s 8 = 48. Then 48 − 5 = <b>43</b>. 48 forgets the 5 stickers given away." % X, 6 * 8 - 5)
    nm, he, his = P.next()
    w("%s has 9 boxes of crayons with 7 crayons in each box. %s also has 4 loose crayons. "
      "How many crayons does %s have altogether?" % (nm, cap(he), he), 67, "crayons", [63, 59, 20],
      "9 %s 7 = 63. Then 63 + 4 = <b>67</b>. 63 forgets the 4 loose crayons." % X, 9 * 7 + 4)
    nm, he, his = P.next()
    w("A plate of kaya toast costs $4 and a drink costs $2. %s buys 8 plates of kaya toast and 8 drinks for %s friends. "
      "How much does %s pay?" % (nm, his, he), 48, "$", [32, 16, 14],
      "Each plate and drink costs $4 + $2 = $6. 8 %s $6 = <b>$48</b>. $32 is only the kaya toast." % X, 8 * (4 + 2))
    assert len(its) == 20, len(its)
    return {"title": "Word problems with bar models", "items": its}


# ============================================================ lesson
def body_html():
    rows = [[str(k)] + ["%d %s %d = %d" % (k, X, t, k * t) for t in (6, 7, 8, 9)] for k in range(1, 11)]
    model = model_svg([{"segs": units(8), "over": [(0, 8, "56 stickers")], "under": [(0, 1, "?")]}],
                      "bar model: 56 stickers in 8 equal units")
    assert 5 * 8 + 2 * 8 == 56 and 10 * 9 - 9 == 81 and 56 // 8 == 7
    return (
        "<h2>Multiplication is equal groups</h2>"
        "<p><b>7 %s 6</b> means 7 groups of 6. In an array, it is 7 rows with 6 dots in each row. "
        "You can turn it round: 6 %s 7 is the same, 42.</p>" % (X, X)
        + "<figure class='sn-fig'>" + array_svg(7, 6, split=5)
        + "<figcaption>7 rows of 6 = 5 rows of 6 + 2 rows of 6: 30 + 12 = 42.</figcaption></figure>"
        + "<h2>Build new facts from facts you know</h2>"
        "<p>You already know the tables of 2, 4, 5 and 10. Use them.</p>"
        + table(["Table", "Trick", "Example"], [
            ["%s 6" % X, "5 groups and 1 more group", "6 %s 8: 40 + 8 = 48" % X],
            ["%s 7" % X, "5 groups and 2 more groups", "7 %s 8: 40 + 16 = 56" % X],
            ["%s 8" % X, "Double the table of 4", "8 %s 6: 24 + 24 = 48" % X],
            ["%s 9" % X, "10 groups, take away 1 group", "9 %s 9: 90 − 9 = 81" % X],
        ])
        + "<p>In the table of 9, the two digits always add up to 9: 18, 27, 36, 45, 54, 63, 72, 81.</p>"
        + "<figure class='sn-fig'>" + jumps_svg(9, 4)
        + "<figcaption>Skip count in 9s: 9, 18, 27, 36. 4 jumps of 9 make 4 %s 9 = 36.</figcaption></figure>" % X
        + table(["", "Table of 6", "Table of 7", "Table of 8", "Table of 9"], rows)
        + "<h2>Division facts</h2>"
        "<p>Division is the inverse of multiplication. Three numbers make a <b>fact family</b>: "
        "6 %s 8 = 48, 8 %s 6 = 48, 48 ÷ 6 = 8 and 48 ÷ 8 = 6.</p>" % (X, X)
        + ex("Example", "63 ÷ 9 = ?", "Think: 9 %s ? = 63. 9 %s 7 = 63." % (X, X), "7")
        + "<h2>Word problems: draw a model</h2>"
        "<p>Draw equal units. Find 1 unit by dividing, or many units by multiplying.</p>"
        + "<figure class='sn-fig'>" + model
        + "<figcaption>56 stickers shared equally among 8 pupils: 8 units = 56, 1 unit = 56 ÷ 8 = 7.</figcaption></figure>"
        + ex("Times as many", "Ali has 7 marbles. Siti has 6 times as many. How many marbles does Siti have?",
             "1 unit = 7. 6 units = 6 %s 7 = 42." % X, "42 marbles")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["7 %s 8 = 54" % X, "5 %s 8 + 2 %s 8 = 40 + 16 = 56. Remember 5, 6, 7, 8: 56 = 7 %s 8" % (X, X, X)],
            ["6 %s 9 = 56" % X, "6 %s 10 − 6 = 60 − 6 = 54" % X],
            ["Dividing the wrong way: 7 ÷ 63 = 9", "Start with the total: 63 ÷ 7 = 9"],
            ["Adding instead: 6 %s 7 = 13" % X, "%s means groups of: 6 groups of 7 = 42" % X],
        ])
    )


FAQ = [
    {"q": "When do children learn the multiplication tables of 6, 7, 8 and 9 in Singapore?",
     "a": "In Primary 3. The tables of 2, 3, 4, 5 and 10 come in Primary 2, and the tables of 6, 7, 8 and 9, with their division facts, come in Primary 3."},
    {"q": "How can I help my child remember 7 × 8 and 6 × 9?",
     "a": "Build them from easier facts: 7 × 8 = 5 × 8 + 2 × 8 = 40 + 16 = 56, and 6 × 9 = 6 × 10 − 6 = 54. Children often mix up 56 and 54, so practise these two side by side."},
    {"q": "What is a fact family in P3 maths?",
     "a": "A fact family is the 4 facts made from 3 numbers, such as 6 × 8 = 48, 8 × 6 = 48, 48 ÷ 6 = 8 and 48 ÷ 8 = 6. It shows that division is the inverse of multiplication."},
    {"q": "Are the tables of 6, 7, 8 and 9 in the MOE syllabus?",
     "a": "Yes. The MOE 2021 Primary Mathematics syllabus has the multiplication tables of 6, 7, 8 and 9, multiplying and dividing within the tables and mental calculation in Primary 3. Students use these facts every year up to the PSLE."},
]


def mark_large(u, pattern):
    """Tag wide pictures (number lines, bar models, many groups) so they print large enough to read."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(63803)
    P = People(rnd)
    sets = [set_six_seven(rnd), set_eight_nine(rnd), set_division(rnd, P), set_missing(rnd, P), set_words(P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(plain(x) for x in it["c"])) == 4, it
            assert it["e"], it["q"]
            assert it["q"].count("<svg") <= 1, it["q"]
            k = it["q"]
            assert k not in keys, it["q"]
            keys.add(k)
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-3", "slug": SLUG, "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 3 Multiplication Tables of 6, 7, 8 and 9",
        "seo_title": "P3 Multiplication Tables of 6, 7, 8 and 9 Worksheets: Free Primary 3 Maths with Answers (MOE Syllabus)",
        "short_title": "Tables of 6, 7, 8 and 9",
        "domain": "Number and Algebra",
        "standard_code": "Primary 3: Whole Numbers",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Multiplication tables of 6, 7, 8 and 9; multiplying and dividing within the multiplication tables; mental calculation",
        "meta_desc": "Free P3 maths worksheets on the tables of 6, 7, 8 and 9: arrays, skip counting, division facts, fact families and bar models. 100 questions with answers.",
        "key_big": "Build new facts from ones you know: 6 is 5 + 1, 7 is 5 + 2, 8 is double 4 and 9 is 10 − 1.",
        "key_sub": "7 × 8 = 5 × 8 + 2 × 8 = 40 + 16 = 56, so 56 ÷ 8 = 7 and 56 ÷ 7 = 8.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "(number line|bar model|[5-9] equal groups|array of [0-9] rows with [0-9] dots in each row, split)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
