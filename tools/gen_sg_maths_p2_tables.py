# -*- coding: utf-8 -*-
"""
Singapore Primary 2 Maths: Multiplication tables of 2, 3, 4, 5 and 10 (MOE 2021 Primary Mathematics
Syllabus, Standard, Number and Algebra, Whole Numbers: "Multiplication tables of 2, 3, 4, 5 and 10")
  python3 tools/gen_sg_maths_p2_tables.py
Equal groups and arrays, skip counting on number lines, the tables of 2, 5 and 10, the tables of 3 and 4
(4 is double 2), missing factors and one-step word problems with bar models.
Every product and missing number is checked in code. Wrong answers are real mistakes:
adding instead of multiplying, giving the number of groups (or the number in each group) instead of the total,
skip counting one too many or one too few, and subtracting instead of dividing.
Singapore English, $ and ¢. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-2")
SLUG = "multiplication-tables-2-3-4-5-and-10"
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
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
        lead = c.lstrip("$").split(" ")[0].rstrip("¢")
        if c in seen or not c or lead.startswith(("-", "−")) or lead == "0":
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
    """Evaluate a short expression written with × and + (only digits, spaces and + − × ÷)."""
    assert re.fullmatch(r"[0-9 +×÷−]+", expr), expr
    return F(eval(expr.replace(X, "*").replace("÷", "/").replace("−", "-")))


def true_fact(s):
    left, right = s.split(" = ")
    return calc(left) == calc(right)


# ------------------------------------------------------------ figures
def dots(x0, y0, rows, cols, cell, col=GREEN):
    return "".join("<circle cx='%d' cy='%d' r='%d' fill='%s'/>"
                   % (x0 + c * cell + cell // 2, y0 + r * cell + cell // 2, cell // 3, col)
                   for r in range(rows) for c in range(cols))


def array_svg(rows, cols, cell=24):
    o = 6
    W = cols * cell + 2 * o
    H = rows * cell + 2 * o
    return svg_wrap(W, H, dots(o, o, rows, cols, cell),
                    "array of %d rows with %d dots in each row" % (rows, cols))


GROUP_SHAPE = {2: (1, 2), 3: (1, 3), 4: (2, 2), 5: (2, 3), 10: (2, 5)}


def groups_svg(g, n, cell=20):
    """g equal groups of n counters, each in a rounded box."""
    gr, gc = GROUP_SHAPE[n]
    pad, gap = 5, 10
    bw, bh = gc * cell + 2 * pad, gr * cell + 2 * pad
    per_row = min(3 if n == 10 else (6 if n <= 4 else 4), g)
    nrows = (g + per_row - 1) // per_row
    W = per_row * bw + (per_row - 1) * gap + 4
    H = nrows * bh + (nrows - 1) * gap + 4
    s = []
    for i in range(g):
        r, c = divmod(i, per_row)
        x = 2 + c * (bw + gap)
        y = 2 + r * (bh + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, y, bw, bh, FILL2, GREEN))
        k = 0
        for rr in range(gr):
            for cc in range(gc):
                if k < n:
                    s.append("<circle cx='%d' cy='%d' r='%d' fill='%s'/>"
                             % (x + pad + cc * cell + cell // 2, y + pad + rr * cell + cell // 2, cell // 3, GREEN))
                k += 1
    return svg_wrap(W, H, "".join(s), "%d equal groups with %d counters in each group" % (g, n))


def jumps_svg(step, n):
    """Number line from 0 to step × n with n equal jumps from 0."""
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
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>"
                 % (b, yl - 3, b - 9, yl - 12, b - 2, yl - 14, GREEN))
    return svg_wrap(R + 16, yl + 34, "".join(s), "number line with %d jumps of %d from 0 to %d" % (n, step, end))


def model_svg(rows, label, W=440):
    """Bar model drawn to scale. rows: dicts with name, segs [(length, text, shaded)],
    over / under [(start, end, text)] brackets. Text containing '?' is drawn red."""
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
def skip(step, n):
    return ", ".join(str(step * k) for k in range(1, n + 1))


def tip(a, b):
    """How to find a × b, where b is the multiplication table being practised."""
    p = a * b
    if b == 2:
        return "%d %s 2 is double %d: %d + %d = <b>%d</b>." % (a, X, a, a, a, p)
    if b == 4:
        return "4 is double 2. %d %s 2 = %d. Double it: %d + %d = <b>%d</b>." % (a, X, 2 * a, 2 * a, 2 * a, p)
    if b == 10:
        return "%d tens make %d. %d %s 10 = <b>%d</b>." % (a, p, a, X, p)
    if b in (3, 5):
        return "Count in %ds %d times: %s. So %d %s %d = <b>%d</b>." % (b, a, skip(b, a), a, X, b, p)
    raise ValueError(b)


def fact_cands(a, b, rnd):
    """Real mistakes: adding instead of multiplying, one group too many or too few, a neighbouring table."""
    p = a * b
    first = [a + b] if a + b != p else []
    pool = [(a + 1) * b, (a - 1) * b, a * (b + 1)] + ([a * (b - 1)] if b > 2 else [])
    pool = [v for v in pool if v > 0 and v != p and v not in first]
    rnd.shuffle(pool)
    return first + pool + [p + 10, p + 2, p - 2]


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
    wrong = [g + n, (g + 1) * n, (g - 1) * n, g, n]
    if kind == "groups":
        e = "There are %d groups of %d. %d %s %d = <b>%d</b>." % (g, n, g, X, n, p)
        ask = "How many counters are there altogether?"
    else:
        e = "There are %d rows of %d. %d %s %d = <b>%d</b>." % (g, n, g, X, n, p)
        ask = "How many dots are there?"
    e += " " + tip(g, n)
    return mcq(fig(svg_html) + ask, p, wrong, e)


def seq_q(seq, step, wrong):
    gaps = [seq[i + 1] - seq[i] for i in range(len(seq) - 1) if seq[i] is not None and seq[i + 1] is not None]
    assert all(g == step for g in gaps), seq
    if None in seq:
        i = seq.index(None)
        ans = seq[i - 1] + step
        assert i + 1 >= len(seq) or seq[i + 1] == ans + step
        show = ", ".join("?" if v is None else str(v) for v in seq)
        e = "Add %d each time: %d + %d = <b>%d</b>." % (step, seq[i - 1], step, ans)
        return mcq("Count in %ds. What is the missing number?<br>%s" % (step, show), ans, wrong, e)
    ans = seq[-1] + step
    assert ans % step == 0 and ans not in wrong
    e = "Add %d each time: %d + %d = <b>%d</b>." % (step, seq[-1], step, ans)
    return mcq("Count in %ds. What comes next?<br>%s, ?" % (step, ", ".join(map(str, seq))), ans, wrong, e)


def multiple_q(ask, right, wrong, n, inside):
    assert (right % n == 0) == inside and all((w % n == 0) != inside for w in wrong)
    lst = ", ".join(str(n * k) for k in range(1, 11))
    e = "The table of %d goes %s. <b>%d</b> %s." % (
        n, lst, right, "is in the list (%d %s %d)" % (right // n, X, n) if inside else "is not in the list")
    return mcq(ask, right, wrong, e)


def jumps_q(step, n):
    p = step * n
    right = "%d %s %d = %d" % (n, X, step, p)
    wrong = ["%d %s %d = %d" % (n + 1, X, step, (n + 1) * step), "%d + %d = %d" % (n, step, n + step),
             "%d %s %d = %d" % (n - 1, X, step, (n - 1) * step)]
    assert true_fact(right) and all(true_fact(w) for w in wrong)
    e = ("Count the jumps, not the numbers. There are %d jumps of %d from 0 to %d. So <b>%d %s %d = %d</b>."
         % (n, step, p, n, X, step, p))
    return mcq(fig(jumps_svg(step, n)) + "Which multiplication does this number line show?", right, wrong, e)


def match_q(svg_html, g, n, kind):
    right = "%d %s %d" % (g, X, n)
    wrong = ["%d + %d" % (g, n), "%d %s %d" % (g, X, g), "%d %s %d" % (n, X, n), "%d %s %d" % (g + 1, X, n)]
    wrong = [w for w in wrong if calc(w) != g * n]
    what = "groups of %d" % n if kind == "groups" else "rows of %d" % n
    return mcq(fig(svg_html) + "Which multiplication matches the picture?", right, wrong,
               "There are %d %s: <b>%d %s %d</b> = %d. %d + %d only adds the two numbers."
               % (g, what, g, X, n, g * n, g, n))


# ============================================================ set 1: equal groups and arrays
def set_groups(rnd, P):
    its = [
        count_q(groups_svg(3, 4), 3, 4, "groups"),
        count_q(groups_svg(5, 2), 5, 2, "groups"),
        count_q(groups_svg(4, 5), 4, 5, "groups"),
        count_q(groups_svg(2, 10), 2, 10, "groups"),
        count_q(array_svg(3, 5), 3, 5, "array"),
        count_q(array_svg(4, 3), 4, 3, "array"),
        count_q(array_svg(5, 4), 5, 4, "array"),
        match_q(groups_svg(4, 3), 4, 3, "groups"),
        match_q(array_svg(2, 5), 2, 5, "array"),
    ]
    its.append(mcq(fig(groups_svg(5, 3)) + "How many groups are there?", 5, [3, 15, 8, 6],
                   "Count the boxes. There are <b>5</b> groups. 3 is the number in each group. 15 is the total."))
    its.append(mcq(fig(groups_svg(3, 5)) + "How many counters are in each group?", 5, [3, 15, 8],
                   "Each box has <b>5</b> counters. 3 is the number of groups. 15 is the total."))
    its.append(mcq(fig(groups_svg(4, 2)) + "8 counters are put in groups of 2. How many groups are there?", 4,
                   [2, 8, 6, 5], "Count the boxes: <b>4</b> groups of 2. Check: 4 %s 2 = 8." % X))
    its.append(mcq("Which multiplication is the same as 4 + 4 + 4?", "3 %s 4" % X,
                   ["4 %s 4" % X, "3 + 4", "4 %s 12" % X],
                   "There are three 4s. 3 groups of 4 is <b>3 %s 4</b> = 12." % X))
    its.append(mcq("Which multiplication is the same as 5 + 5 + 5 + 5 + 5 + 5?", "6 %s 5" % X,
                   ["5 %s 5" % X, "6 + 5", "7 %s 5" % X],
                   "Count the 5s. There are six 5s, so it is <b>6 %s 5</b> = 30." % X))
    its.append(mcq("Which addition is the same as 5 groups of 2?", "2 + 2 + 2 + 2 + 2",
                   ["5 + 2", "5 + 5 + 5 + 5 + 5", "2 + 2 + 2 + 2"],
                   "5 groups of 2 means five 2s: <b>2 + 2 + 2 + 2 + 2</b> = 10."))
    its.append(mcq("What is 3 groups of 10?", 30, [13, 40, 20, 3],
                   "3 groups of 10 is 3 tens: 3 %s 10 = <b>30</b>. 13 adds 3 and 10." % X))
    its.append(mcq(fig(array_svg(2, 5)) + "2 %s 5 = 5 %s ?" % (X, X), 2, [5, 10, 3],
                   "You can turn the array round. 2 rows of 5 is the same as 5 rows of 2. So ? = <b>2</b>."))
    nm, he, his = P.next()
    its.append(mcq("%s says 3 groups of 5 is 8. What did %s do wrong?" % (nm, he),
                   "%s added 3 and 5" % cap(he),
                   ["%s counted one group too many" % cap(he), "%s counted only the groups" % cap(he),
                    "%s did nothing wrong" % cap(he)],
                   "3 + 5 = 8, so %s added. 3 groups of 5 is 3 %s 5 = 15." % (he, X)))
    its.append(mcq("There are 4 bags. Each bag has 2 apples. Which multiplication shows this?", "4 %s 2" % X,
                   ["4 + 2", "2 %s 2" % X, "4 %s 4" % X],
                   "4 bags is 4 groups. Each group has 2. So it is <b>4 %s 2</b> = 8." % X))
    nm, he, his = P.next()
    its.append(mcq("An array has 3 rows. There are 18 dots. How many dots are in each row?", 6,
                   [7, 15, 21, 5],
                   "3 %s ? = 18. Count in 3s: 3, 6, 9, 12, 15, 18. That is 6 threes, so there are <b>6</b> dots in each row."
                   % X))
    assert len(its) == 20, len(its)
    return {"title": "Equal groups and arrays", "items": its}


# ============================================================ set 2: tables of 2, 5 and 10
def set_two_five_ten(rnd, P):
    its = [jumps_q(2, 6), jumps_q(5, 4), jumps_q(10, 5)]
    its.append(seq_q([2, 4, 6, 8], 2, [12, 9, 11]))
    its.append(seq_q([5, 10, 15, 20], 5, [30, 21, 26]))
    its.append(seq_q([10, 20, None, 40], 10, [25, 31, 50]))
    its.append(seq_q([35, 40, 45], 5, [55, 46, 60]))
    nm, he, his = P.next()
    its.append(mcq("%s counts in 5s to find 4 %s 5. %s says: 5, 10, 15, 20, 25. What is 4 %s 5?"
                   % (nm, X, cap(he), X), 20, [25, 9, 15],
                   "4 %s 5 needs only 4 fives: 5, 10, 15, 20. %s counted one 5 too many. 4 %s 5 = <b>20</b>."
                   % (X, cap(he), X)))
    its += facts(2, [3, 7, 9, 6], rnd)
    its += facts(5, [3, 6, 7, 9], rnd)
    its += facts(10, [4, 8], rnd)
    its.append(multiple_q("Which number is in the multiplication table of 5?", 35, [32, 52, 38], 5, True))
    its.append(multiple_q("Which number is <b>not</b> in the multiplication table of 2?", 15, [14, 18, 20], 2, False))
    assert len(its) == 20, len(its)
    return {"title": "Tables of 2, 5 and 10", "items": its}


# ============================================================ set 3: tables of 3 and 4
def double_q(a, wrong):
    k, ans = 2 * a, 4 * a
    e = "4 is double 2, so 4 %s %d is double 2 %s %d: %d + %d = <b>%d</b>." % (X, a, X, a, k, k, ans)
    return mcq("2 %s %d = %d. Double it to find 4 %s %d." % (X, a, k, X, a), ans, wrong, e)


def set_three_four(rnd, P):
    its = [count_q(groups_svg(6, 3), 6, 3, "groups"), count_q(groups_svg(5, 4), 5, 4, "groups")]
    its += [jumps_q(3, 5), jumps_q(4, 6)]
    its.append(seq_q([3, 6, 9, 12], 3, [18, 13, 16]))
    its.append(seq_q([16, 20, 24], 4, [32, 25, 30]))
    its.append(seq_q([9, 12, None, 18], 3, [14, 16, 21]))
    its.append(double_q(6, [14, 18, 48]))
    its.append(double_q(8, [18, 24, 64]))
    its += facts(3, [4, 6, 7, 9], rnd)
    its += facts(4, [5, 7, 8, 9], rnd)
    its.append(multiple_q("Which number is in the multiplication table of 3?", 27, [26, 28, 25], 3, True))
    its.append(multiple_q("Which number is <b>not</b> in the multiplication table of 4?", 30, [28, 32, 36], 4, False))
    its.append(mcq("3 %s 8 = 24. What is 8 %s 3?" % (X, X), 24, [11, 21, 27],
                   "You can multiply in any order. 8 %s 3 = 3 %s 8 = <b>24</b>. 11 adds the numbers." % (X, X)))
    assert len(its) == 20, len(its)
    return {"title": "Tables of 3 and 4", "items": its}


# ============================================================ set 4: missing factors
WORD = {2: "twos", 3: "threes", 4: "fours", 5: "fives", 10: "tens"}


def miss_right(a, b):
    """a × ? = a × b"""
    p = a * b
    e = "Count in %ds to %d: %s. That is %d %s. So ? = <b>%d</b>. Check: %d %s %d = %d." % (
        a, p, skip(a, b), b, WORD[a], b, a, X, b, p)
    return mcq("%d %s ? = %d" % (a, X, p), b, [b + 1, b - 1, p - a, p + a], e)


def miss_left(a, b):
    """? × b = a × b"""
    p = a * b
    e = "Count in %ds to %d: %s. That is %d %s. So ? = <b>%d</b>. Check: %d %s %d = %d." % (
        b, p, skip(b, a), a, WORD[b], a, a, X, b, p)
    return mcq("? %s %d = %d" % (X, b, p), a, [a + 1, a - 1, p - b, p + b], e)


def set_missing(rnd, P):
    its = [miss_right(a, b) for a, b in [(2, 7), (5, 8), (10, 6), (3, 9), (4, 7), (3, 6), (5, 10), (4, 8)]]
    its += [miss_left(a, b) for a, b in [(6, 2), (9, 5), (4, 10), (8, 3), (9, 4), (8, 2)]]
    its.append(mcq(fig(jumps_svg(4, 7)) + "4 %s ? = 28. How many jumps of 4 make 28?" % X, 7, [8, 4, 24],
                   "Count the jumps: 4, 8, 12, 16, 20, 24, 28. There are <b>7</b> jumps. "
                   "8 counts the 0 as well."))
    its.append(mcq(fig(groups_svg(3, 10)) + "? %s 10 = 30. How many groups of 10 are there?" % X, 3,
                   [10, 30, 20, 4], "Count the boxes: <b>3</b> groups of 10. 3 %s 10 = 30." % X))
    nm, he, his = P.next()
    its.append(mcq("%s says the missing number in 5 %s ? = 35 is 30. What is the correct number?" % (nm, X),
                   7, [30, 40, 6],
                   "35 − 5 = 30 takes away instead of counting groups. Count in 5s: 5, 10, 15, 20, 25, 30, 35. "
                   "That is <b>7</b> fives."))
    its.append(mcq("3 %s ? = 3 + 3 + 3 + 3" % X, 4, [3, 12, 5],
                   "Count the 3s. There are four 3s, so ? = <b>4</b>."))
    its.append(mcq("? %s 10 = 10 %s 7" % (X, X), 7, [10, 70, 17],
                   "You can multiply in any order. 7 %s 10 = 10 %s 7, so ? = <b>7</b>." % (X, X)))
    its.append(mcq("4 %s ? = 2 %s 6" % (X, X), 3, [6, 12, 4],
                   "2 %s 6 = 12. 4 %s 3 = 12, so ? = <b>3</b>. 12 is the product, not the missing number." % (X, X)))
    assert 4 * 3 == 2 * 6 and 5 * 7 == 35
    assert len(its) == 20, len(its)
    return {"title": "Missing factors", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def w(q, ans, unit, wrong, e, check, svg=None):
        assert check == ans, (q, check, ans)
        assert ans not in wrong
        if unit == "$":
            u = lambda v: "$%d" % v
        elif unit == "¢":
            u = lambda v: "%d¢" % v
        else:
            u = lambda v: "%d %s" % (v, unit)
        its.append(mcq((fig(svg) if svg else "") + q, u(ans), [u(v) for v in wrong], e))

    w("Mdm Wong puts 4 curry puffs on each plate. There are 5 plates. How many curry puffs are there?",
      20, "curry puffs", [9, 16, 24], "5 plates of 4: 5 %s 4 = <b>20</b>. 9 is 5 + 4. It adds instead of multiplies." % X,
      5 * 4)
    w("A bicycle has 2 wheels. There are 8 bicycles at the void deck. How many wheels are there?",
      16, "wheels", [10, 14, 18], "8 bicycles of 2 wheels: 8 %s 2 = <b>16</b>. 10 is 8 + 2." % X, 8 * 2)
    w("A tricycle has 3 wheels. How many wheels do 6 tricycles have?",
      18, "wheels", [9, 15, 21], "6 %s 3 = <b>18</b>. Count in 3s: 3, 6, 9, 12, 15, 18." % X, 6 * 3)
    svg = model_svg([{"segs": units(7, "4"), "over": [(0, 7, "?")]}], "bar model: 7 units of 4")
    w("A car has 4 wheels. There are 7 cars in the car park. How many wheels are there?",
      28, "wheels", [11, 24, 32], "7 units of 4: 7 %s 4 = <b>28</b>. 24 is only 6 cars." % X, 7 * 4, svg)
    w("There are 10 sweets in each packet. How many sweets are there in 9 packets?",
      90, "sweets", [19, 80, 100], "9 packets of 10: 9 %s 10 = <b>90</b>. 19 is 9 + 10." % X, 9 * 10)
    nm, he, his = P.next()
    svg = model_svg([{"segs": units(4, "$5"), "over": [(0, 4, "?")]}], "bar model: 4 units of $5")
    w("A bowl of laksa costs $5. %s buys 4 bowls for %s family. How much does %s pay?" % (nm, his, he),
      20, "$", [9, 15, 25], "4 units of $5: 4 %s $5 = <b>$20</b>. $9 is $5 + $4." % X, 4 * 5, svg)
    nm, he, his = P.next()
    w("%s saves $2 every day. How much does %s save in 9 days?" % (nm, he),
      18, "$", [11, 16, 20], "9 %s $2 = <b>$18</b>. Double 9 is 18. $11 is 9 + 2." % X, 9 * 2)
    nm, he, his = P.next()
    w("A sweet costs 10¢. %s buys 6 sweets. How much does %s pay?" % (nm, he),
      60, "¢", [16, 50, 70], "6 %s 10¢ = <b>60¢</b>. 16¢ adds 6 and 10." % X, 6 * 10)
    w("There are 3 plates. Each plate has 4 slices of kaya toast. How many slices are there altogether?",
      12, "slices", [3, 4, 7], "3 groups of 4: 3 %s 4 = <b>12</b>. 3 is the number of plates, "
      "and 4 is the number on one plate." % X, 3 * 4)
    nm, he, his = P.next()
    w("A packet of stickers costs 5¢. %s buys 8 packets. How much does %s pay?" % (nm, he),
      40, "¢", [13, 35, 45], "8 %s 5¢ = <b>40¢</b>. Count in 5s: 5, 10, 15, 20, 25, 30, 35, 40." % X, 8 * 5)
    svg = model_svg([{"segs": units(6, "5"), "over": [(0, 6, "?")]}], "bar model: 6 units of 5")
    w("For National Day, the class makes 6 rows of flags. There are 5 flags in each row. How many flags are there?",
      30, "flags", [11, 25, 35], "6 units of 5: 6 %s 5 = <b>30</b>. 25 is only 5 rows." % X, 6 * 5, svg)

    # division: sharing and grouping
    svg = model_svg([{"segs": units(5), "over": [(0, 5, "20 stickers")], "under": [(0, 1, "?")]}],
                    "bar model: 20 stickers in 5 equal units")
    w("Mrs Lim shares 20 stickers equally among 5 pupils. How many stickers does each pupil get?",
      4, "stickers", [5, 15, 25], "5 units = 20. 1 unit = 20 ÷ 5 = <b>4</b>. Check: 5 %s 4 = 20. "
      "15 is 20 − 5." % X, 20 // 5, svg)
    w("Mr Tan puts 24 mandarin oranges into bags. He puts 4 oranges in each bag. How many bags does he use?",
      6, "bags", [7, 20, 28], "Count in 4s to 24: 4, 8, 12, 16, 20, 24. That is <b>6</b> fours. "
      "Check: 6 %s 4 = 24." % X, 24 // 4)
    w("30 pupils stand in rows of 10 at assembly. How many rows are there?",
      3, "rows", [4, 20, 40], "30 is 3 tens. 3 %s 10 = 30, so there are <b>3 rows</b>." % X, 30 // 10)
    nm, he, his = P.next()
    w("%s has $16. %s spends $2 each day at recess. How many days will the money last?" % (nm, cap(he)),
      8, "days", [9, 14, 18], "Count in 2s to 16: that is 8 twos. 8 %s $2 = $16, so it lasts <b>8 days</b>." % X,
      16 // 2)
    svg = model_svg([{"segs": units(5), "over": [(0, 5, "35 m")], "under": [(0, 1, "?")]}],
                    "bar model: 35 m in 5 equal units")
    w("Mr Rahman cuts a rope 35 m long into 5 equal pieces. How long is each piece?",
      7, "m", [6, 30, 40], "5 units = 35 m. 1 unit = 35 ÷ 5 = <b>7 m</b>. Check: 5 %s 7 = 35." % X, 35 // 5, svg)
    w("27 pupils visit the Singapore Zoo. They walk in groups of 3. How many groups are there?",
      9, "groups", [8, 24, 30], "Count in 3s to 27: 3, 6, 9, 12, 15, 18, 21, 24, 27. That is <b>9</b> threes. "
      "Check: 9 %s 3 = 27." % X, 27 // 3)
    svg = model_svg([{"segs": units(4), "over": [(0, 4, "32 pencils")], "under": [(0, 1, "?")]}],
                    "bar model: 32 pencils in 4 equal units")
    w("A teacher puts 32 pencils equally into 4 cups. How many pencils are in each cup?",
      8, "pencils", [9, 28, 36], "4 units = 32. 1 unit = 32 ÷ 4 = <b>8</b>. Check: 4 %s 8 = 32. "
      "28 is 32 − 4." % X, 32 // 4, svg)

    # two steps
    nm, he, his = P.next()
    w("%s buys 3 packets of stickers. There are 5 stickers in each packet. %s gives away 4 stickers. "
      "How many stickers does %s have left?" % (nm, cap(he), he), 11, "stickers", [15, 19, 4],
      "3 %s 5 = 15. Then 15 − 4 = <b>11</b>. 15 forgets the 4 stickers given away." % X, 3 * 5 - 4)
    nm, he, his = P.next()
    w("%s has 4 boxes of crayons with 10 crayons in each box. %s also has 3 loose crayons. "
      "How many crayons does %s have altogether?" % (nm, cap(he), he), 43, "crayons", [40, 17, 37],
      "4 %s 10 = 40. Then 40 + 3 = <b>43</b>. 40 forgets the 3 loose crayons." % X, 4 * 10 + 3)
    assert len(its) == 20, len(its)
    return {"title": "Word problems with bar models", "items": its}


# ============================================================ lesson
def body_html():
    rows = [[str(k)] + ["%d %s %d = %d" % (k, X, t, k * t) for t in (2, 3, 4, 5, 10)] for k in range(1, 11)]
    model = model_svg([{"segs": units(5), "over": [(0, 5, "20 stickers")], "under": [(0, 1, "?")]}],
                      "bar model: 20 stickers in 5 equal units")
    assert 4 * 3 == 12 and 20 // 5 == 4 and 2 * 7 * 2 == 28
    return (
        "<h2>Multiplication is equal groups</h2>"
        "<p><b>4 %s 3</b> means 4 groups of 3. Add 3 four times: 3 + 3 + 3 + 3 = 12.</p>" % X
        + "<figure class='sn-fig'>" + groups_svg(4, 3)
        + "<figcaption>4 groups of 3 = 4 %s 3 = 12.</figcaption></figure>" % X
        + "<p>An <b>array</b> has rows that are all the same. 3 rows of 5 dots is 3 %s 5 = 15. "
        "Turn it round and it is 5 %s 3. The answer is still 15.</p>" % (X, X)
        + "<figure class='sn-fig'>" + array_svg(3, 5)
        + "<figcaption>3 rows of 5 = 3 %s 5 = 15.</figcaption></figure>" % X
        + "<h2>Skip count to find a fact</h2>"
        "<p>Count in jumps of the same size. Count the jumps, not the numbers.</p>"
        + "<figure class='sn-fig'>" + jumps_svg(5, 4)
        + "<figcaption>4 jumps of 5: 5, 10, 15, 20. So 4 %s 5 = 20.</figcaption></figure>" % X
        + table(["Table", "Tip", "Example"], [
            ["%s 2" % X, "Double the number", "7 %s 2: 7 + 7 = 14" % X],
            ["%s 4" % X, "Double, then double again", "7 %s 4: 14 + 14 = 28" % X],
            ["%s 5" % X, "Ends in 0 or 5", "7 %s 5 = 35" % X],
            ["%s 10" % X, "Put a 0 at the end", "7 %s 10 = 70" % X],
            ["%s 3" % X, "Count in 3s", "7 %s 3: 3, 6, 9, 12, 15, 18, 21" % X],
        ])
        + table(["", "Table of 2", "Table of 3", "Table of 4", "Table of 5", "Table of 10"], rows)
        + "<h2>Missing factors</h2>"
        "<p>In 5 %s ? = 30, count in 5s until you reach 30. Count how many fives you said.</p>" % X
        + ex("Example", "5 %s ? = 30" % X, "5, 10, 15, 20, 25, 30. That is 6 fives.", "6")
        + "<h2>Word problems: draw a model</h2>"
        "<p>Draw equal units. Many units: multiply. One unit: share or divide.</p>"
        + "<figure class='sn-fig'>" + model
        + "<figcaption>20 stickers shared equally among 5 pupils: 5 units = 20, 1 unit = 4.</figcaption></figure>"
        + ex("Equal groups", "A car has 4 wheels. How many wheels do 7 cars have?",
             "7 groups of 4: 7 %s 4 = 28." % X, "28 wheels")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding: 3 groups of 5 = 8", "%s means groups of. 3 %s 5 = 5 + 5 + 5 = 15" % (X, X)],
            ["Giving the number of groups (3) or the number in one group (5)", "Find the total: 3 %s 5 = 15" % X],
            ["Counting one too many: 5, 10, 15, 20, 25 for 4 %s 5" % X, "Say only 4 fives: 5, 10, 15, 20"],
            ["5 %s ? = 35, so ? = 30" % X, "Count the fives: 7 fives make 35"],
        ])
    )


FAQ = [
    {"q": "Which multiplication tables are taught in Primary 2 in Singapore?",
     "a": "Primary 2 students learn the multiplication tables of 2, 3, 4, 5 and 10. The tables of 6, 7, 8 and 9 come in Primary 3."},
    {"q": "How can I help my child learn the tables of 2, 3, 4, 5 and 10?",
     "a": "Start with equal groups of real objects, then skip count: 2, 4, 6 or 5, 10, 15. Use tips such as “4 is double 2” and “× 10 puts a 0 at the end”."},
    {"q": "What is the most common mistake in P2 multiplication?",
     "a": "Adding instead of multiplying, for example 3 groups of 5 = 8. Another is counting one jump too many when skip counting."},
    {"q": "Are the tables of 2, 3, 4, 5 and 10 in the MOE syllabus?",
     "a": "Yes. The MOE 2021 Primary Mathematics syllabus has the multiplication tables of 2, 3, 4, 5 and 10 in Primary 2, with multiplying and dividing within these tables and simple word problems."},
]


def mark_large(u, pattern):
    """Tag wide pictures (number lines, bar models, many groups) so they print large enough to read."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(62804)
    P = People(rnd)
    sets = [set_groups(rnd, P), set_two_five_ten(rnd, P), set_three_four(rnd, P), set_missing(rnd, P), set_words(P)]
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
        "country": "sg", "subject": "maths", "grade": "primary-2", "slug": SLUG, "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 2 Multiplication Tables of 2, 3, 4, 5 and 10",
        "seo_title": "P2 Multiplication Tables of 2, 3, 4, 5 and 10 Worksheets: Free Primary 2 Maths with Answers (MOE Syllabus)",
        "short_title": "Tables of 2, 3, 4, 5 and 10",
        "domain": "Number and Algebra",
        "standard_code": "Primary 2: Whole Numbers",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Multiplication tables of 2, 3, 4, 5 and 10",
        "meta_desc": "Free P2 maths worksheets on the multiplication tables of 2, 3, 4, 5 and 10: equal groups, arrays, skip counting and bar models. 100 questions with answers.",
        "key_big": "Multiplication means equal groups: 4 × 3 is 4 groups of 3.",
        "key_sub": "4 × 3 = 3 + 3 + 3 + 3 = 12, and 3 × 4 is also 12.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "(number line|bar model|[5-9] equal groups|[0-9]+ equal groups with 10)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
