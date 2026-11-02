# -*- coding: utf-8 -*-
"""
CA-BC Grade 4 Math (BC Mathematics Curriculum, Computational fluency):
multiplication and division facts to 100 (introductory computational strategies).
  python3 tools/gen_cabc_math_g4_facts.py
Every product, quotient and missing factor is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#e8f3ec"
BROWN = "#b5651d"
INK = "#2b2b2b"
CAR = "#3a6ea5"
CARD = "#fdf3e1"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]
X = "×"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or c.startswith("0"):
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


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def dots(x0, y0, rows, cols, cell, col=GREEN):
    return "".join("<circle cx='%d' cy='%d' r='%d' fill='%s'/>"
                   % (x0 + c * cell + cell // 2, y0 + r * cell + cell // 2, cell // 3, col)
                   for r in range(rows) for c in range(cols))


def array_svg(rows, cols, cell=22):
    o = 6
    return svg_wrap(cols * cell + 2 * o, rows * cell + 2 * o, dots(o, o, rows, cols, cell),
                    "array of %d rows with %d dots in each row" % (rows, cols))


def split_svg(rows, top, cols, cell=22):
    """An array of rows x cols split into top rows and the rest, with a label for each part."""
    o, gap, lab = 6, 10, 70
    bot = rows - top
    W = cols * cell + 2 * o + lab
    H = rows * cell + gap + 2 * o
    s = [dots(o, o, top, cols, cell, GREEN), dots(o, o + top * cell + gap, bot, cols, cell, BROWN)]
    y1 = o + top * cell / 2 + 6
    y2 = o + top * cell + gap + bot * cell / 2 + 6
    s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>"
             % (o, o + top * cell + gap / 2, o + cols * cell, o + top * cell + gap / 2, INK))
    s.append(text(o + cols * cell + 8, y1, "%d %s %d" % (top, X, cols), 15, "start", GREEN))
    s.append(text(o + cols * cell + 8, y2, "%d %s %d" % (bot, X, cols), 15, "start", BROWN))
    return svg_wrap(W, H, "".join(s), "array of %d rows with %d dots split into %d rows and %d rows" % (rows, cols, top, bot))


GROUP_SHAPE = {2: (1, 2), 3: (1, 3), 4: (2, 2), 5: (1, 5), 6: (2, 3)}


def groups_svg(g, n, cell=20, label_sizes=False):
    """g equal groups of n counters, each group in a rounded box."""
    gr, gc = GROUP_SHAPE[n]
    pad, gap = 5, 10
    bw, bh = gc * cell + 2 * pad, gr * cell + 2 * pad
    per_row = min({2: 6, 3: 5, 4: 4, 5: 3, 6: 4}[n], g)
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
                 % (x, y, bw, bh, FILL, GREEN))
        s.append(dots(x + pad, y + pad, gr, gc, cell))
        if label_sizes:
            s.append(text(x + bw / 2, y + bh + 17, str(n), 15))
    return svg_wrap(W, H, "".join(s), "%d equal groups with %d counters in each group" % (g, n))


def jumps_svg(step, n, end):
    """Number line from 0 to end, labelled every step, with n jumps of step from 0."""
    sp = 34
    m, ly, ry = 22, 46, 20
    ticks = end // step
    assert ticks * step == end
    W = 2 * m + ticks * sp
    H = ly + 30
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (m - 12, ly, W - m + 12, ly, INK)]
    for k in range(ticks + 1):
        x = m + k * sp
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, ly - 6, x, ly + 6, INK))
        s.append(text(x, ly + 24, str(k * step), 14))
    for k in range(n):
        x1, x2 = m + k * sp, m + (k + 1) * sp
        s.append("<path d='M %d %d A %.1f %d 0 0 1 %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1, ly, sp / 2, ry, x2, ly, GREEN))
        s.append("<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2.5' "
                 "stroke-linejoin='round'/>" % (x2 - 5, ly - 10, x2, ly - 2, x2 + 5, ly - 10, GREEN))
    return svg_wrap(W, H, "".join(s), "number line from 0 to %d with jumps of %d" % (end, step))


def car_deck_svg(rows, cols, last=None):
    """Top view of a ferry car deck: rows of cars, all full except an optional last row with `last` cars."""
    cw, ch, gx, gy, o = 24, 14, 6, 8, 8
    total_rows = rows + (1 if last else 0)
    W = cols * cw + (cols - 1) * gx + 2 * o
    H = total_rows * ch + (total_rows - 1) * gy + 2 * o
    s = ["<rect x='1' y='1' width='%d' height='%d' rx='10' fill='#eef1f4' stroke='%s' stroke-width='2'/>"
         % (W - 2, H - 2, INK)]
    for r in range(total_rows):
        k = cols if r < rows else last
        for c in range(k):
            x = o + c * (cw + gx)
            y = o + r * (ch + gy)
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='4' fill='%s'/>" % (x, y, cw, ch, CAR))
            s.append("<rect x='%d' y='%d' width='6' height='%d' rx='2' fill='#ffffff' opacity='0.7'/>"
                     % (x + cw - 9, y + 3, ch - 6))
    lab = "car deck with %d full rows of %d cars" % (rows, cols)
    if last:
        lab += " and one row with %d cars" % last
    return svg_wrap(W, H, "".join(s), lab)


def card_packs_svg(k, n):
    """k packs of hockey cards, each marked with n cards."""
    pw, ph, gap = 46, 60, 10
    per_row = min(k, 6)
    nrows = (k + per_row - 1) // per_row
    W = per_row * pw + (per_row - 1) * gap + 4
    H = nrows * ph + (nrows - 1) * gap + 4
    s = []
    for i in range(k):
        r, c = divmod(i, per_row)
        x, y = 2 + c * (pw + gap), 2 + r * (ph + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, y, pw, ph, CARD, BROWN))
        s.append(text(x + pw / 2, y + 30, str(n), 22, col=BROWN))
        s.append(text(x + pw / 2, y + 50, "cards", 14))
    return svg_wrap(W, H, "".join(s), "%d packs of hockey cards with %d cards in each pack" % (k, n))


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
    return eval(expr.replace(X, "*").replace("÷", "/").replace("−", "-"))


def ok_sentence(s):
    lhs, rhs = s.split(" = ")
    return calc(lhs) == int(rhs)


def choice_calc_q(ask, target, right, wrong, e):
    assert calc(right) == target and all(calc(w) != target for w in wrong), (ask, right, wrong)
    return mcq(ask, right, wrong, e)


def true_sentence_q(right, wrong, e, ask="Which number sentence is true?"):
    assert ok_sentence(right) and not any(ok_sentence(w) for w in wrong), (right, wrong)
    return mcq(ask, right, wrong, e)


# ------------------------------------------------------------ strategies
def tip(a, b):
    """Strategy for a × b, where b is the fact family being practised."""
    p = a * b
    if b == 2:
        return "2 %s %d is double %d: %d + %d = <b>%d</b>." % (X, a, a, a, a, p)
    if b == 3:
        return "3 groups of %d: %d + %d + %d = <b>%d</b>. Or 2 %s %d = %d, plus one more %d: <b>%d</b>." % (
            a, a, a, a, p, X, a, 2 * a, a, p)
    if b == 4:
        return "Double, then double again: 2 %s %d = %d, and double %d is <b>%d</b>." % (X, a, 2 * a, 2 * a, p)
    if b == 5:
        return "Half of the 10s: 10 %s %d = %d, and half of %d is <b>%d</b>." % (X, a, 10 * a, 10 * a, p)
    if b == 10:
        return "%d tens make %d. So %d %s 10 = <b>%d</b>." % (a, p, a, X, p)
    raise ValueError(b)


def fact_cands(a, b, rnd):
    """Real mistakes: the fact next door, adding instead of multiplying."""
    p = a * b
    pool = [(a - 1) * b, (a + 1) * b, a + b]
    pool = [v for v in pool if v > 0 and v != p]
    rnd.shuffle(pool)
    return pool + [p + 1, p - 1, p + 2]


def fact_q(a, b, rnd):
    x, y = (a, b) if rnd.random() < 0.5 else (b, a)
    return mcq("%d %s %d = ?" % (x, X, y), a * b, fact_cands(a, b, rnd), tip(a, b))


def seq_q(seq, step, wrong, extra=""):
    nxt = seq[-1] + step
    assert all(seq[i + 1] - seq[i] == step for i in range(len(seq) - 1)) and seq[0] % step == 0
    assert nxt not in wrong
    e = "Each number is %d more than the one before: %d + %d = <b>%d</b>. %s" % (step, seq[-1], step, nxt, extra)
    return mcq("Skip count by %ds. What comes next?<br>%s, ?" % (step, ", ".join(map(str, seq))), nxt, wrong, e.strip())


def count_q(svg_html, g, n, wrong, kind):
    p = g * n
    assert p not in wrong
    if kind == "groups":
        e = "There are %d groups of %d. %d %s %d = <b>%d</b>." % (g, n, g, X, n, p)
        ask = "How many counters are there in all?"
    else:
        e = "There are %d rows with %d dots in each row. %d %s %d = <b>%d</b>." % (g, n, g, X, n, p)
        ask = "How many dots are in this array?"
    if g + n in wrong:
        e += " %d is %d + %d, which adds instead of multiplies." % (g + n, g, n)
    return mcq(fig(svg_html) + ask, p, wrong, e)


# ============================================================ set 1: arrays and skip counting
def set_facts(rnd):
    its = [
        count_q(groups_svg(4, 3), 4, 3, [7, 9, 15], "groups"),
        count_q(groups_svg(6, 4), 6, 4, [10, 20, 28], "groups"),
        count_q(array_svg(2, 9), 2, 9, [11, 16, 20], "array"),
        count_q(array_svg(5, 7), 5, 7, [12, 30, 40], "array"),
        count_q(array_svg(3, 8), 3, 8, [11, 21, 27], "array"),
    ]
    for r, c in [(4, 6), (3, 9)]:
        p = r * c
        wrong = ["%d + %d" % (r, c), "%d %s %d" % (r, X, c + 1), "%d %s %d" % (r + 1, X, c)]
        e = ("There are %d rows with %d dots in each row, so it shows %d %s %d = %d. "
             "%d + %d adds the numbers instead of multiplying." % (r, c, r, X, c, p, r, c))
        its.append(choice_calc_q(fig(array_svg(r, c)) + "Which number sentence matches this array?", p,
                                 "%d %s %d" % (r, X, c), wrong, e))
    its.append(seq_q([12, 14, 16], 2, [17, 20, 32], "So 2 %s 9 = 18." % X))
    its.append(seq_q([30, 35, 40], 5, [41, 50, 55], "So 5 %s 9 = 45." % X))
    its.append(seq_q([60, 70, 80], 10, [81, 100, 85], "So 10 %s 9 = 90." % X))
    its.append(seq_q([12, 15, 18], 3, [19, 20, 24], "So 3 %s 7 = 21." % X))
    its.append(seq_q([20, 24, 28], 4, [29, 30, 36], "So 4 %s 8 = 32." % X))
    n = 7
    its.append(mcq(fig(jumps_svg(3, n, 24)) + "Which fact does this number line show?",
                   "7 %s 3 = 21" % X, ["6 %s 3 = 18" % X, "7 + 3 = 10", "8 %s 3 = 24" % X],
                   "There are 7 jumps of 3 from 0 to 21: 3, 6, 9, 12, 15, 18, 21. So <b>7 %s 3 = 21</b>." % X))
    assert 7 * 3 == 21
    its += [fact_q(a, b, rnd) for a, b in [(8, 2), (7, 5), (6, 10), (6, 3), (9, 4), (7, 4), (9, 3)]]
    assert len(its) == 20, len(its)
    return {"title": "Facts with arrays and skip counting: 2s, 5s, 10s, 3s and 4s", "items": its}


# ============================================================ set 2: strategies
def set_strategies(rnd):
    its = []
    # doubles for the 4s
    for a, wrong in [(7, [14, 21, 11]), (6, [12, 18, 10]), (9, [18, 27, 13]), (8, [16, 24, 12])]:
        k, ans = 2 * a, 4 * a
        assert ans not in wrong and wrong[1] == 3 * a and wrong[2] == 4 + a
        e = ("4 is double 2, so 4 %s %d is double 2 %s %d: %d + %d = <b>%d</b>. "
             "%d is only 3 groups of %d." % (X, a, X, a, k, k, ans, 3 * a, a))
        its.append(mcq("2 %s %d = %d. Double it to find 4 %s %d." % (X, a, k, X, a), ans, wrong, e))
    # 5s are half of the 10s
    for a in (8, 7, 9):
        t, ans = 10 * a, 5 * a
        wrong = [t, t - 5, 5 + a]
        assert ans not in wrong
        e = ("5 is half of 10, so 5 %s %d is half of 10 %s %d. Half of %d is <b>%d</b>. "
             "%d takes away only 5." % (X, a, X, a, t, ans, t - 5))
        its.append(mcq("10 %s %d = %d. Use it to find 5 %s %d." % (X, a, t, X, a), ans, wrong, e))
    # 10s are double the 5s
    its.append(mcq("5 %s 6 = 30. Use it to find 10 %s 6." % (X, X), 60, [35, 36, 16],
                   "10 is double 5, so 10 %s 6 is double 5 %s 6: 30 + 30 = <b>60</b>. "
                   "35 adds 5 instead of doubling." % (X, X)))
    assert 10 * 6 == 2 * 30
    # near facts: one more group
    its.append(mcq(fig(split_svg(7, 6, 6)) + "6 %s 6 = 36. Use the picture to find 7 %s 6." % (X, X), 42,
                   [37, 43, 36],
                   "7 rows of 6 is 6 rows of 6 plus one more row of 6: 36 + 6 = <b>42</b>. "
                   "37 adds 1, not one more group of 6."))
    assert 7 * 6 == 36 + 6
    for a, b, wrong in [(7, 7, [50, 57, 54]), (8, 8, [65, 73, 81]), (9, 5, [46, 51, 45]), (5, 8, [41, 46, 40])]:
        p, ans = a * b, a * (b + 1)
        if a == 5:   # 5 × 8 known, find 6 × 8 (one more group of 8)
            p, ans = 5 * 8, 6 * 8
            e = "6 %s 8 is one more group of 8 than 5 %s 8: 40 + 8 = <b>48</b>. Add a whole group of 8, not 1." % (X, X)
            its.append(mcq("5 %s 8 = 40. Use it to find 6 %s 8." % (X, X), ans, wrong, e))
            continue
        assert ans == p + a and ans not in wrong
        e = ("%d %s %d is one more group of %d than %d %s %d: %d + %d = <b>%d</b>. Add a whole group of %d, not 1."
             % (a, X, b + 1, a, a, X, b, p, a, ans, a))
        its.append(mcq("%d %s %d = %d. Use it to find %d %s %d." % (a, X, b, p, a, X, b + 1), ans, wrong, e))
    # near facts: one group less (the 9s)
    for a, wrong in [(7, [69, 60, 70]), (6, [59, 50, 56])]:
        t, ans = 10 * a, 9 * a
        assert ans not in wrong
        e = ("9 groups is one group less than 10 groups. 10 %s %d = %d, then take away one %d: %d − %d = <b>%d</b>. "
             "Take away %d, not 1." % (X, a, t, a, t, a, ans, a))
        its.append(mcq("10 %s %d = %d. Use it to find 9 %s %d." % (X, a, t, X, a), ans, wrong, e))
    its.append(choice_calc_q("Which is a good way to work out 6 %s 7?" % X, 42, "6 %s 6 + 6" % X,
                             ["6 %s 6 + 7" % X, "6 %s 6 + 1" % X, "6 + 7"],
                             "6 %s 7 is 7 groups of 6. That is 6 groups of 6 plus one more 6: 36 + 6 = <b>42</b>." % X))
    its.append(choice_calc_q("Which is the same as 8 %s 6?" % X, 48, "4 %s 6 + 4 %s 6" % (X, X),
                             ["4 %s 6 + 4" % X, "8 + 6", "4 %s 6 + 6" % X],
                             "8 is double 4, so 8 %s 6 = 4 %s 6 + 4 %s 6 = 24 + 24 = <b>48</b>." % (X, X, X)))
    its.append(choice_calc_q("Which is the same as 4 %s 9?" % X, 36, "2 %s 9 + 2 %s 9" % (X, X),
                             ["2 %s 9 + 2" % X, "2 %s 9 + 9" % X, "4 + 9"],
                             "4 is double 2, so 4 %s 9 = 2 %s 9 + 2 %s 9 = 18 + 18 = <b>36</b>. "
                             "18 + 9 is only 3 nines." % (X, X, X)))
    its.append(true_sentence_q("7 %s 8 = 56" % X, ["7 %s 8 = 54" % X, "6 %s 9 = 56" % X, "8 %s 8 = 56" % X],
                               "<b>7 %s 8 = 56</b>. Say 5, 6, 7, 8: 56 = 7 %s 8. "
                               "54 is 6 %s 9, and 8 %s 8 = 64." % (X, X, X, X)))
    its.append(true_sentence_q("4 %s 7 = 28" % X, ["4 %s 7 = 11" % X, "4 %s 7 = 21" % X, "4 %s 7 = 24" % X],
                               "4 %s 7 is double 2 %s 7: 14 + 14 = <b>28</b>. 11 adds instead of multiplies, "
                               "21 is only 3 sevens, and 24 is 4 %s 6." % (X, X, X),
                               "Only one of these number sentences is correct. Which one?"))
    assert len(its) == 20, len(its)
    return {"title": "Strategies: doubles, halves and near facts", "items": its}


# ============================================================ set 3: division facts and fact families
def set_division(rnd):
    its = []
    for d, q in [(3, 7), (4, 8), (6, 7), (7, 8), (9, 7), (8, 6), (4, 9), (6, 9)]:
        p = d * q
        e = "Think: %d %s ? = %d. %d %s %d = %d, so %d ÷ %d = <b>%d</b>." % (d, X, p, d, X, q, p, p, d, q)
        its.append(mcq("%d ÷ %d = ?" % (p, d), q, [q + 1, q - 1, p - d, d, p], e))
    for g, n in [(5, 3), (7, 4)]:
        p = g * n
        e = "Count the groups: there are %d groups of %d. %d ÷ %d = <b>%d</b>. Check: %d %s %d = %d." % (
            g, n, p, n, g, g, X, n, p)
        its.append(mcq(fig(groups_svg(g, n)) + "%d counters are put into groups of %d. How many groups are there?" % (p, n),
                       g, [g + 1, g - 1, p - n, p], e))
    for a, b in [(6, 8), (7, 9), (4, 7)]:
        p = a * b
        right = "%d ÷ %d = %d" % (p, a, b)
        wrong = ["%d ÷ %d = %d" % (b, a, p), "%d ÷ %d = %d" % (p, b, a + 1), "%d ÷ %d = %d" % (p, a, b - 1)]
        assert ok_sentence(right) and not any(ok_sentence(w) for w in wrong)
        e = ("%d, %d and %d make a fact family. %d %s %d = %d, so <b>%d ÷ %d = %d</b> and %d ÷ %d = %d. "
             "Division starts with the biggest number, %d." % (a, b, p, a, X, b, p, p, a, b, p, b, a, p))
        its.append(mcq("%d %s %d = %d. Which division fact is also true?" % (a, X, b, p), right, wrong, e))
    for a, b in [(3, 9), (8, 7)]:
        p = a * b
        right = "%d ÷ %d = %d" % (p, b, a)
        wrong = ["%d ÷ %d = %d" % (b, p, a), "%d + %d = %d" % (a, b, a + b), "%d − %d = %d" % (p, b, p - b)]
        assert ok_sentence(right)
        e = ("The fact family for %d, %d and %d is %d %s %d = %d, %d %s %d = %d, %d ÷ %d = %d and <b>%d ÷ %d = %d</b>. "
             "%d ÷ %d is turned around: division starts with the biggest number."
             % (a, b, p, a, X, b, p, b, X, a, p, p, a, b, p, b, a, b, p))
        its.append(mcq("Which fact is in the same fact family as %d %s %d = %d?" % (a, X, b, p), right, wrong, e))
    its.append(mcq("Which fact is <b>not</b> in the fact family for 4, 6 and 24?", "6 ÷ 24 = 4",
                   ["4 %s 6 = 24" % X, "24 ÷ 4 = 6", "24 ÷ 6 = 4"],
                   "4 %s 6 = 24, 24 ÷ 4 = 6 and 24 ÷ 6 = 4 are all in the family. "
                   "<b>6 ÷ 24 = 4</b> divides the wrong way: start with the biggest number, 24." % X))
    assert 4 * 6 == 24 and 24 // 4 == 6
    its.append(mcq("Which fact helps you work out 49 ÷ 7?", "7 %s 7 = 49" % X,
                   ["7 %s 6 = 42" % X, "49 − 7 = 42", "49 + 7 = 56"],
                   "49 ÷ 7 asks: 7 times what makes 49? <b>7 %s 7 = 49</b>, so 49 ÷ 7 = 7." % X))
    its.append(mcq("Which fact helps you work out 72 ÷ 8?", "8 %s 9 = 72" % X,
                   ["8 %s 8 = 64" % X, "72 − 8 = 64", "8 + 9 = 17"],
                   "72 ÷ 8 asks: 8 times what makes 72? <b>8 %s 9 = 72</b>, so 72 ÷ 8 = 9." % X))
    its.append(mcq("Which multiplication fact checks 45 ÷ 5 = 9?", "9 %s 5 = 45" % X,
                   ["45 − 5 = 40", "9 + 5 = 14", "9 %s 4 = 36" % X],
                   "Multiply the answer by the number you divided by: <b>9 %s 5 = 45</b>. "
                   "Subtracting 5 once does not undo dividing by 5." % X))
    its.append(mcq("How many 3s make 27?", 9, [8, 24, 30],
                   "27 ÷ 3 = ? Skip count by 3s: 3, 6, 9, 12, 15, 18, 21, 24, 27. That is <b>9</b> jumps. "
                   "24 is 27 − 3, which subtracts only one 3."))
    assert 7 * 7 == 49 and 8 * 9 == 72 and 9 * 5 == 45 and 27 // 3 == 9
    assert len(its) == 20, len(its)
    return {"title": "Related division facts and fact families", "items": its}


# ============================================================ set 4: missing factors
def set_missing(rnd):
    its = []
    for a, b in [(3, 8), (4, 9), (6, 7), (7, 7), (8, 4), (9, 6)]:
        p = a * b
        e = "Ask: %d times what makes %d? %d ÷ %d = %d. Check: %d %s %d = %d, so ? = <b>%d</b>." % (
            a, p, p, a, b, a, X, b, p, b)
        its.append(mcq("%d %s ? = %d" % (a, X, p), b, [p - a, b + 1, b - 1, p], e))
    for a, b in [(6, 3), (8, 7), (9, 8), (5, 6)]:
        p = a * b
        e = "Ask: what times %d makes %d? %d ÷ %d = %d. Check: %d %s %d = %d, so ? = <b>%d</b>." % (
            b, p, p, b, a, a, X, b, p, a)
        its.append(mcq("? %s %d = %d" % (X, b, p), a, [p - b, a + 1, a - 1, p], e))
    for d, q in [(4, 7), (6, 8), (9, 3)]:
        p = d * q
        e = ("Division undoes multiplication, so multiply back: ? = %d %s %d = <b>%d</b>. Check: %d ÷ %d = %d."
             % (q, X, d, p, p, d, q))
        its.append(mcq("? ÷ %d = %d" % (d, q), p, [d + q, p + d, p - d, q], e))
    for p, q in [(56, 7), (36, 9), (30, 6)]:
        d = p // q
        assert d * q == p
        e = "Ask: %d ÷ what = %d? Think %d %s ? = %d. %d %s %d = %d, so ? = <b>%d</b>." % (
            p, q, q, X, p, q, X, d, p, d)
        its.append(mcq("%d ÷ ? = %d" % (p, q), d, [p - q, d + 1, d - 1, p + q], e))
    for step, n, end in [(4, 6, 32), (3, 8, 27)]:
        p = step * n
        e = "Count the jumps: there are %d jumps of %d. %d %s %d = %d, so ? = <b>%d</b>." % (n, step, n, X, step, p, n)
        its.append(mcq(fig(jumps_svg(step, n, end)) + "The jumps go from 0 to %d. Fill in: ? %s %d = %d" % (p, X, step, p),
                       n, [n + 1, n - 1, p], e))
    its.append(mcq("An array has 6 rows and 42 dots. How many dots are in each row?", 7, [36, 8, 48],
                   "6 %s ? = 42. 42 ÷ 6 = 7, so each row has <b>7</b> dots. 36 is 42 − 6, which subtracts "
                   "instead of dividing." % X))
    its.append(mcq("Which number makes both true?<br>4 %s ? = 28 and 28 ÷ ? = 4" % X, 7, [24, 6, 8],
                   "4 %s 7 = 28 and 28 ÷ 7 = 4. They are in the same fact family, so ? = <b>7</b>. "
                   "24 is 28 − 4." % X))
    assert 6 * 7 == 42 and 4 * 7 == 28
    assert len(its) == 20, len(its)
    return {"title": "Missing factors", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def w(q, ans, unit, wrong, e, check):
        assert check == ans, (q, check, ans)
        assert ans not in wrong
        if unit == "$":
            u = lambda v: "$%d" % v
        else:
            u = lambda v: "%d %s" % (v, unit)
        its.append(mcq(q, u(ans), [u(v) for v in wrong], e))

    w(fig(car_deck_svg(6, 9)) + "This is part of a BC Ferries car deck. There are 6 rows with 9 cars in each row. "
      "How many cars is that?", 54, "cars", [15, 45, 63],
      "6 rows of 9: 6 %s 9 = <b>54</b>. 15 is 6 + 9, which adds instead of multiplies." % X, 6 * 9)
    nm, he, his = P.next()
    w(fig(card_packs_svg(6, 8)) + "%s buys 6 packs of hockey cards. Each pack has 8 cards. How many cards does %s get?"
      % (nm, he), 48, "cards", [14, 42, 56],
      "6 packs of 8: 6 %s 8 = <b>48</b>. 5 %s 8 = 40, plus one more 8 is 48. 14 is 6 + 8." % (X, X), 6 * 8)
    w("54 cars wait for the ferry to Nanaimo. Each row on the car deck holds 9 cars. How many rows do the cars fill?",
      6, "rows", [45, 63, 5], "54 ÷ 9 = ? 9 %s 6 = 54, so the cars fill <b>6 rows</b>. "
      "45 is 54 − 9, which takes away only one row." % X, 54 // 9)
    w(fig(car_deck_svg(5, 7, 3)) + "On this car deck, 5 rows have 7 cars each. The last row has only 3 cars. "
      "How many cars are there in all?", 38, "cars", [35, 42, 15],
      "5 full rows: 5 %s 7 = 35. Add the last row: 35 + 3 = <b>38</b>. 42 counts the last row as full." % X,
      5 * 7 + 3)
    nm, he, his = P.next()
    w("Binder pages hold 9 hockey cards each. %s has 63 cards. How many pages can %s fill?" % (nm, he), 7, "pages",
      [54, 8, 72], "63 ÷ 9 = ? 9 %s 7 = 63, so %s fills <b>7 pages</b>. 54 is 63 − 9." % (X, he), 63 // 9)
    nm, he, his = P.next()
    w("%s has 4 Vancouver Canucks cards. %s cousin has 6 times as many. How many Canucks cards does the cousin have?"
      % (nm, his.capitalize()), 24, "cards", [10, 20, 28],
      "6 times as many as 4 means 6 %s 4 = <b>24</b>. 10 is 6 + 4, which adds instead of multiplies." % X, 6 * 4)
    nm, he, his = P.next()
    w("%s puts 32 hockey cards into 4 equal piles. How many cards are in each pile?" % nm, 8, "cards",
      [7, 9, 28], "32 ÷ 4 = ? 4 %s 8 = 32, so each pile has <b>8 cards</b>. 28 is 32 − 4." % X, 32 // 4)
    nm, he, his = P.next()
    w("%s buys 3 packs of hockey cards with 9 cards in each pack. %s gives 5 cards to a friend. "
      "How many cards does %s have left?" % (nm, he.capitalize(), he), 22, "cards", [27, 32, 7],
      "First 3 %s 9 = 27. Then 27 − 5 = <b>22</b>. 27 forgets the 5 cards given away." % X, 3 * 9 - 5)
    nm, he, his = P.next()
    w("Hockey cards cost $3 a pack. %s has $27. How many packs can %s buy?" % (nm, he), 9, "packs",
      [24, 81, 8], "27 ÷ 3 = ? 3 %s 9 = 27, so %s can buy <b>9 packs</b>. 81 is 27 %s 3, which multiplies instead "
      "of divides." % (X, he, X), 27 // 3)
    w("A Grade 4 class goes on a SkyTrain field trip. 9 students sit in each of 4 cars. How many students is that?",
      36, "students", [13, 27, 45], "4 cars of 9: 4 %s 9 = <b>36</b>. Double 2 %s 9 = 18: 18 + 18 = 36." % (X, X),
      4 * 9)
    w("45 students walk in the Terry Fox Run in groups of 5. How many groups are there?", 9, "groups",
      [8, 40, 50], "45 ÷ 5 = ? 5 %s 9 = 45, so there are <b>9 groups</b>." % X, 45 // 5)
    w("A chairlift at Whistler carries 4 skiers on each chair. How many skiers ride on 8 chairs?", 32, "skiers",
      [12, 28, 36], "8 %s 4 = <b>32</b>. Double 8 is 16, double 16 is 32. 12 is 8 + 4." % X, 8 * 4)
    w("24 students go canoeing. 3 students sit in each canoe. How many canoes do they need?", 8, "canoes",
      [21, 72, 7], "24 ÷ 3 = ? 3 %s 8 = 24, so they need <b>8 canoes</b>. "
      "72 is 24 %s 3, which multiplies instead of divides." % (X, X), 24 // 3)
    w("An orchard in the Okanagan packs apples in trays of 6. How many apples fit in 7 trays?", 42, "apples",
      [13, 36, 48], "7 %s 6 = <b>42</b>. 6 %s 6 = 36, plus one more 6 is 42." % (X, X), 7 * 6)
    nm, he, his = P.next()
    w("%s plants cedar seedlings in 8 rows. Each row has 7 seedlings. How many seedlings is that?" % nm, 56,
      "seedlings", [54, 15, 63], "8 %s 7 = <b>56</b>. Say 5, 6, 7, 8: 56 = 7 %s 8. 54 is 6 %s 9, not 7 %s 8."
      % (X, X, X, X), 8 * 7)
    w("A lacrosse tournament in Burnaby has 7 teams. Each team has 10 players. How many players is that?", 70,
      "players", [17, 60, 80], "7 %s 10 = <b>70</b>. 7 tens make 70. 17 is 7 + 10." % X, 7 * 10)
    nm, he, his = P.next()
    w("%s sees 3 bald eagles at each of 6 stops along the Squamish River. How many eagles is that?" % nm, 18,
      "eagles", [9, 15, 21], "6 stops with 3 eagles: 6 %s 3 = <b>18</b>. 9 is 6 + 3." % X, 6 * 3)
    nm, he, his = P.next()
    w("%s and %s 2 friends share 24 crackers equally on a hike. How many crackers does each person get?" % (nm, his),
      8, "crackers", [12, 21, 72], "%s and 2 friends is 3 people. 24 ÷ 3 = <b>8</b>. "
      "12 shares between only 2 people and forgets %s." % (nm, nm), 24 // 3)
    nm, he, his = P.next()
    nm2, he2, his2 = P.next()
    w("%s has 7 packs of 10 hockey cards. %s has 8 packs of 8 cards. How many more cards does %s have?"
      % (nm, nm2, nm), 6, "cards", [2, 134, 64],
      "%s: 7 %s 10 = 70. %s: 8 %s 8 = 64. 70 − 64 = <b>6</b>. 134 adds the two totals instead of finding "
      "the difference." % (nm, X, nm2, X), 7 * 10 - 8 * 8)
    w("A Kamloops school buys 9 boxes of markers. Each box has 8 markers. How many markers is that?", 72, "markers",
      [17, 64, 81], "9 %s 8 = <b>72</b>. 10 %s 8 = 80, take away one 8: 72." % (X, X), 9 * 8)
    assert len(its) == 20
    return {"title": "Word problems: ferries, hockey cards and field trips", "items": its}


# ============================================================ lesson
def body_html():
    rows = [[str(k)] + ["%d" % (k * n) for n in (2, 3, 4, 5, 10)] for k in range(1, 11)]
    return (
        "<h2>Multiplication means equal groups</h2>"
        "<p><b>4 %s 6</b> means 4 groups of 6. Skip count by 6s: 6, 12, 18, 24. So 4 %s 6 = 24. "
        "You can multiply in any order: 6 %s 4 = 24 too. In Grade 4 you work with all facts up to 10 %s 10 = 100.</p>"
        % (X, X, X, X)
        + "<figure class='sn-fig'>" + array_svg(4, 6)
        + "<figcaption>An array of 4 rows of 6: 4 %s 6 = 24.</figcaption></figure>" % X
        + table(["", "2s", "3s", "4s", "5s", "10s"], rows)
        + "<h2>Strategies for harder facts</h2>"
        + table(["Strategy", "How it works", "Example"], [
            ["Doubles", "The 4s are double the 2s", "4 %s 7: 14 + 14 = 28" % X],
            ["Halves", "The 5s are half of the 10s", "5 %s 8: half of 80 = 40" % X],
            ["Near fact: one more group", "Use a fact you know, then add one group", "6 %s 7 = 6 %s 6 + 6 = 42" % (X, X)],
            ["Near fact: one group less", "The 9s are the 10s take away one group", "9 %s 7 = 70 − 7 = 63" % X],
        ])
        + "<figure class='sn-fig'>" + split_svg(7, 6, 6)
        + "<figcaption>7 rows of 6 = 6 rows of 6 + 1 row of 6: 36 + 6 = 42.</figcaption></figure>"
        + ex("Example", "8 %s 6 = ?" % X, "8 is double 4. 4 %s 6 = 24, and 24 + 24 = 48." % X, "48")
        + "<h2>Every fact gives division facts</h2>"
        "<p>Division is the opposite of multiplication. 7, 8 and 56 make a <b>fact family</b>: "
        "7 %s 8 = 56, 8 %s 7 = 56, 56 ÷ 7 = 8 and 56 ÷ 8 = 7. "
        "A division fact starts with the biggest number.</p>" % (X, X)
        + ex("Division", "63 ÷ 9 = ?", "Think: 9 %s ? = 63. 9 %s 7 = 63." % (X, X), "7")
        + ex("Missing factor", "? %s 6 = 54" % X, "Think: 54 ÷ 6. 6 %s 9 = 54." % X, "9")
        + ex("Word problem", "A BC Ferries car deck has 6 rows with 9 cars in each row. How many cars is that?",
             "6 rows of 9: 6 %s 9 = 54." % X, "54 cars")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding instead of multiplying: 6 %s 9 = 15" % X, "%s means groups of: 6 groups of 9 = 54" % X],
            ["Mixing up 7 %s 8 = 54" % X, "Say 5, 6, 7, 8: 56 = 7 %s 8. (54 is 6 %s 9.)" % (X, X)],
            ["Near fact: 6 %s 7 = 36 + 1 = 37" % X, "Add a whole group of 6: 36 + 6 = 42"],
            ["Dividing the wrong way: 8 ÷ 56 = 7", "Start with the biggest number: 56 ÷ 8 = 7"],
        ])
    )


FAQ = [
    {"q": "What multiplication facts should a Grade 4 student know in BC?",
     "a": "The BC Mathematics Curriculum asks Grade 4 students to work with multiplication and division facts to 100, using strategies such as doubling, halving and near facts. Many students know the 2s, 5s and 10s well and are building up the 3s, 4s and harder facts like 7 × 8."},
    {"q": "Is multiplication on the Grade 4 FSA?",
     "a": "The FSA numeracy section is based on the BC curriculum, so it can include multiplication and division, often inside word problems. Knowing the facts quickly leaves more time to think about each problem."},
    {"q": "What is a near fact in Grade 4 math?",
     "a": "A near fact uses a fact you already know to find one next to it. For example, 6 × 6 = 36, so 6 × 7 is one more group of 6: 36 + 6 = 42."},
    {"q": "How can I help my child learn multiplication and division facts at home?",
     "a": "Practise a few facts each day and ask for the matching division fact too, such as 4 × 8 = 32 and 32 ÷ 8 = 4. Everyday things like packs of hockey cards or rows of cars make the facts real."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(34801)
    P = People(rnd)
    sets = [set_facts(rnd), set_strategies(rnd), set_division(rnd), set_missing(rnd), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = it["q"]
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-4",
        "slug": "multiplication-and-division-facts-to-100", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiplication and Division Facts to 100",
        "seo_title": "Grade 4 Multiplication and Division Facts to 100 Worksheets with Answer Key (BC)",
        "short_title": "Multiplication and division facts to 100",
        "domain": "Computational fluency",
        "standard_code": "Grade 4: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/4/core",
        "standard_text": "Multiplication and division facts to 100 (introductory computational strategies)",
        "meta_desc": "Free Grade 4 math worksheets on multiplication and division facts to 100: arrays, skip counting, doubles, near facts, fact families, missing factors and word problems. 100 questions with an answer key, following the BC curriculum and useful for the FSA.",
        "key_big": "Use a fact you know to find one you don’t: 6 × 7 = 6 × 6 + 6 = 42.",
        "key_sub": "The 4s are double the 2s, and the 5s are half of the 10s. Every multiplication fact gives division facts: 7 × 8 = 56, so 56 ÷ 8 = 7 and 56 ÷ 7 = 8.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(car deck|[0-9]+ packs of hockey|number line|[0-9]+ equal groups)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
