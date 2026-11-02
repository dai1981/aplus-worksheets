# -*- coding: utf-8 -*-
"""
CA Grade 3 Math (Ontario Mathematics Curriculum 2020, B2.2): multiplication facts for 2, 5 and 10
and the related division facts.
  python3 tools/gen_ca_math_g3_facts.py
Every product, quotient and missing factor is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#e8f3ec"
INK = "#2b2b2b"
COIN = "#d9dde2"
COIN_EDGE = "#7a828c"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
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


def array_svg(rows, cols, cell=24):
    o = 6
    return svg_wrap(cols * cell + 2 * o, rows * cell + 2 * o, dots(o, o, rows, cols, cell),
                    "array of %d rows with %d dots in each row" % (rows, cols))


GROUP_SHAPE = {2: (1, 2), 5: (1, 5), 10: (2, 5)}


def groups_svg(g, n, cell=20, label_sizes=False):
    """g equal groups of n counters, each group in a rounded box."""
    gr, gc = GROUP_SHAPE[n]
    pad, gap = 5, 10
    bw, bh = gc * cell + 2 * pad, gr * cell + 2 * pad
    per_row = min({2: 6, 5: 3, 10: 3}[n], g)
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


def coins_svg(k, value):
    """k coins of the same value: nickels (5¢) or dimes (10¢)."""
    r = 19 if value == 5 else 17          # a nickel is bigger than a dime
    d = 2 * 19 + 8
    per_row = k if k <= 6 else (k + 1) // 2
    nrows = (k + per_row - 1) // per_row
    W, H = per_row * d + 4, nrows * d + 4
    s = []
    for i in range(k):
        row, col = divmod(i, per_row)
        cx = 2 + col * d + d / 2
        cy = 2 + row * d + d / 2
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (cx, cy, r, COIN, COIN_EDGE))
        s.append(text(cx, cy + 5.5, "%d¢" % value, 15))
    name = "nickels" if value == 5 else "dimes"
    return svg_wrap(W, H, "".join(s), "%d %s worth %d cents each" % (k, name, value))


def jumps_svg(step, n, end):
    """Number line from 0 to end, labelled every step, with n jumps of step from 0."""
    sp = 34 if step == 5 else 30 if step == 2 else 36
    m, ly, ry = 22, 46, 20
    ticks = end // step
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


# ------------------------------------------------------------ strategies
def tip(a, b):
    """Strategy for a × b, where b is the fact family being practised (2, 5 or 10)."""
    p = a * b
    if b == 2:
        return "2 %s %d is double %d: %d + %d = <b>%d</b>." % (X, a, a, a, a, p)
    if b == 5:
        return ("Skip count by 5s, %d jumps: %s. Or halve 10 %s %d = %d to get <b>%d</b>."
                % (a, ", ".join(str(5 * i) for i in range(1, a + 1)), X, a, 10 * a, p))
    if b == 10:
        return "%d tens make %d. So %d %s 10 = <b>%d</b>." % (a, p, a, X, p)
    raise ValueError(b)


def fact_cands(a, b, rnd):
    """Real mistakes: the fact next door (5 × 7 = 30), one group too many, adding instead of multiplying."""
    p = a * b
    pool = [(a - 1) * b, (a + 1) * b, a + b]
    pool = [v for v in pool if v > 0 and v != p]
    rnd.shuffle(pool)
    return pool + [p + 1, p - 1, p + 2]


def fact_q(a, b, rnd):
    """Question shows a × b or b × a; b is the fact family being practised."""
    x, y = (a, b) if rnd.random() < 0.5 else (b, a)
    return mcq("%d %s %d = ?" % (x, X, y), a * b, fact_cands(a, b, rnd), tip(a, b))


def facts(b, mults, rnd):
    mults = list(mults)
    rnd.shuffle(mults)
    return [fact_q(a, b, rnd) for a in mults]


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
    return mcq(fig(svg_html) + ask, p, wrong, e)


def coin_q(k, value, wrong):
    tot = k * value
    name = "nickel" if value == 5 else "dime"
    assert tot < 100 and tot not in wrong
    e = "Each %s is %d¢. Skip count by %ds: %s. %d %s %d¢ = <b>%d¢</b>." % (
        name, value, value, ", ".join(str(value * i) for i in range(1, k + 1)), k, X, value, tot)
    return mcq(fig(coins_svg(k, value)) + "How much money is this?", "%d¢" % tot, ["%d¢" % w for w in wrong], e)


def multiple_q(ask, right, wrong, table_n, inside):
    assert (right % table_n == 0) == inside and all((w % table_n == 0) != inside for w in wrong)
    lst = ", ".join(str(table_n * k) for k in range(1, 11))
    e = "Skip count by %ds: %s. <b>%d</b> %s." % (
        table_n, lst, right, "is in the list" if inside else "is not in the list")
    e += {2: " Numbers in the 2s are even: they end in 0, 2, 4, 6 or 8.",
          5: " Numbers in the 5s always end in 0 or 5.",
          10: " Numbers in the 10s always end in 0."}[table_n]
    return mcq(ask, right, wrong, e)


def choice_calc_q(ask, target, right, wrong, e):
    assert calc(right) == target and all(calc(w) != target for w in wrong), (ask, right, wrong)
    return mcq(ask, right, wrong, e)


def true_sentence_q(right, wrong, e, ask="Which number sentence is true?"):
    assert ok_sentence(right) and not any(ok_sentence(w) for w in wrong), (right, wrong)
    return mcq(ask, right, wrong, e)


# ============================================================ set 1: facts with arrays and skip counting
def set_facts(rnd):
    its = [
        count_q(groups_svg(4, 2), 4, 2, [6, 10, 7], "groups"),
        count_q(groups_svg(3, 5), 3, 5, [8, 20, 10], "groups"),
        count_q(groups_svg(4, 10), 4, 10, [14, 30, 50], "groups"),
        count_q(array_svg(2, 7), 2, 7, [9, 12, 16], "array"),
        count_q(array_svg(5, 6), 5, 6, [11, 25, 35], "array"),
    ]
    for r, c in [(2, 9), (5, 4)]:
        p = r * c
        wrong = ["%d + %d" % (r, c), "%d %s %d" % (r, X, c + 1), "%d %s %d" % (r + 1, X, c)]
        e = ("There are %d rows with %d dots in each row, so it shows %d %s %d = %d. "
             "%d + %d adds the numbers instead of multiplying." % (r, c, r, X, c, p, r, c))
        its.append(choice_calc_q(fig(array_svg(r, c)) + "Which number sentence matches this array?", p,
                                 "%d %s %d" % (r, X, c), wrong, e))
    its.append(coin_q(7, 5, [12, 30, 40]))
    its.append(coin_q(6, 10, [16, 50, 70]))
    its.append(seq_q([8, 10, 12], 2, [13, 16, 24], "So 2 %s 7 = 14." % X))
    its.append(seq_q([25, 30, 35], 5, [36, 45, 50], "So 5 %s 8 = 40." % X))
    its.append(seq_q([50, 60, 70], 10, [71, 90, 75], "So 10 %s 8 = 80." % X))
    its += facts(2, [3, 6, 8], rnd)
    its += facts(5, [2, 9], rnd)
    its += facts(10, [3, 5, 7], rnd)
    assert len(its) == 20, len(its)
    return {"title": "Facts for 2, 5 and 10: arrays and skip counting", "items": its}


# ============================================================ set 2: related division facts and fact families
def set_division(rnd):
    its = []
    for d, q in [(2, 7), (5, 4), (10, 6), (2, 9), (5, 8), (10, 9), (2, 6), (5, 7)]:
        p = d * q
        e = ("Think: %d %s ? = %d. %d %s %d = %d, so %d ÷ %d = <b>%d</b>."
             % (d, X, p, d, X, q, p, p, d, q))
        if d != q:
            e += " The answer is not %d: that is the number you started with." % p
        its.append(mcq("%d ÷ %d = ?" % (p, d), q, [p, q + 1, q - 1, p - d], e))
    for g, n in [(6, 2), (3, 10)]:
        p = g * n
        e = "Count the groups: there are %d groups of %d. %d ÷ %d = <b>%d</b>. Check: %d %s %d = %d." % (
            g, n, p, n, g, g, X, n, p)
        its.append(mcq(fig(groups_svg(g, n)) + "%d counters are put into groups of %d. How many groups are there?" % (p, n),
                       g, [g + 1, g - 1, p - n, p], e))
    for k, n, wrong in [(7, 2, [8, 6, 12]), (6, 10, [5, 7, 50]), (5, 5, [4, 6, 20])]:
        p = k * n
        e = "%d ÷ %d = ? Skip count by %ds to %d: %s. That is <b>%d</b> jumps." % (
            p, n, n, p, ", ".join(str(n * i) for i in range(1, k + 1)), k)
        its.append(mcq("How many %ds make %d?" % (n, p), k, wrong, e))
    for a, b in [(2, 8), (5, 9), (10, 4)]:
        p = a * b
        right = "%d ÷ %d = %d" % (p, a, b)
        wrong = ["%d ÷ %d = %d" % (b, a, p), "%d ÷ %d = %d" % (p, b, a + 1), "%d ÷ %d = %d" % (p, a, b - 1)]
        assert ok_sentence(right) and not any(ok_sentence(w) for w in wrong)
        e = ("%d, %d and %d make a fact family. %d %s %d = %d, so <b>%d ÷ %d = %d</b> and %d ÷ %d = %d. "
             "Division starts with the biggest number, %d." % (a, b, p, a, X, b, p, p, a, b, p, b, a, p))
        its.append(mcq("%d %s %d = %d. Which division fact is also true?" % (a, X, b, p), right, wrong, e))
    for a, b in [(5, 6), (10, 7)]:
        p = a * b
        right = "%d ÷ %d = %d" % (p, b, a)
        wrong = ["%d ÷ %d = %d" % (b, p, a), "%d + %d = %d" % (a, b, a + b), "%d − %d = %d" % (p, b, p - b)]
        assert ok_sentence(right)
        e = ("The fact family for %d, %d and %d is %d %s %d = %d, %d %s %d = %d, %d ÷ %d = %d and <b>%d ÷ %d = %d</b>. "
             "%d ÷ %d is turned around: division starts with the biggest number."
             % (a, b, p, a, X, b, p, b, X, a, p, p, a, b, p, b, a, b, p))
        its.append(mcq("Which fact is in the same fact family as %d %s %d = %d?" % (a, X, b, p), right, wrong, e))
    its.append(mcq("Which fact helps you work out 35 ÷ 5?", "5 %s 7 = 35" % X,
                   ["5 %s 6 = 30" % X, "35 + 5 = 40", "35 − 5 = 30"],
                   "35 ÷ 5 asks: 5 times what makes 35? <b>5 %s 7 = 35</b>, so 35 ÷ 5 = 7." % X))
    its.append(mcq("Which fact helps you work out 18 ÷ 2?", "2 %s 9 = 18" % X,
                   ["2 %s 8 = 16" % X, "18 − 2 = 16", "18 + 2 = 20"],
                   "18 ÷ 2 asks: 2 times what makes 18? <b>2 %s 9 = 18</b>, so 18 ÷ 2 = 9." % X))
    assert 5 * 7 == 35 and 2 * 9 == 18
    assert len(its) == 20, len(its)
    return {"title": "Related division facts and fact families", "items": its}


# ============================================================ set 3: missing factors
def set_missing(rnd):
    its = []
    for a, b in [(2, 8), (5, 9), (10, 4), (5, 3), (2, 10), (10, 7)]:
        p = a * b
        e = "Ask: %d times what makes %d? %d ÷ %d = %d. Check: %d %s %d = %d, so ? = <b>%d</b>." % (
            a, p, p, a, b, a, X, b, p, b)
        its.append(mcq("%d %s ? = %d" % (a, X, p), b, [p - a, b + 1, b - 1, p], e))
    for a, b in [(6, 5), (4, 2), (8, 10), (7, 2), (2, 5), (3, 10)]:
        p = a * b
        e = "Ask: what times %d makes %d? %d ÷ %d = %d. Check: %d %s %d = %d, so ? = <b>%d</b>." % (
            b, p, p, b, a, a, X, b, p, a)
        its.append(mcq("? %s %d = %d" % (X, b, p), a, [p - b, a + 1, a - 1, p], e))
    for d, q in [(5, 6), (2, 8), (10, 5)]:
        p = d * q
        e = "Use the related multiplication fact: ? = %d %s %d = <b>%d</b>. Check: %d ÷ %d = %d." % (q, X, d, p, p, d, q)
        its.append(mcq("? ÷ %d = %d" % (d, q), p, [d + q, p + d, p - d, q], e))
    for p, q in [(20, 4), (60, 6), (14, 2)]:
        d = p // q
        assert d * q == p
        e = "Ask: %d ÷ what = %d? Think %d %s ? = %d. %d %s %d = %d, so %d ÷ %d = %d and ? = <b>%d</b>." % (
            p, q, q, X, p, q, X, d, p, p, d, q, d)
        its.append(mcq("%d ÷ ? = %d" % (p, q), d, [p - q, p + q, d + 1, d - 1], e))
    for step, n, end in [(5, 7, 40), (2, 8, 20)]:
        p = step * n
        e = "Count the jumps: there are %d jumps of %d. %d %s %d = %d, so ? = <b>%d</b>." % (n, step, n, X, step, p, n)
        its.append(mcq(fig(jumps_svg(step, n, end)) + "The jumps go from 0 to %d. Fill in: ? %s %d = %d" % (p, X, step, p),
                       n, [n + 1, n - 1, p], e))
    assert len(its) == 20, len(its)
    return {"title": "Missing factors", "items": its}


# ============================================================ set 4: mixed practice
def set_mixed(rnd):
    its = []
    for a, b in [(2, 9), (5, 8)]:
        p = a * b
        e = ("You can multiply in any order and get the same answer. %d %s %d = %d, so %d %s %d = <b>%d</b> too."
             % (a, X, b, p, b, X, a, p))
        its.append(mcq("%d %s %d = %d. So %d %s %d = ?" % (a, X, b, p, b, X, a), p, [a + b, p - a, p + a], e))
    its.append(choice_calc_q("Which has the same answer as 9 %s 5?" % X, 45, "5 %s 9" % X,
                             ["9 + 5", "9 %s 9" % X, "5 %s 5" % X],
                             "5 %s 9 is 9 %s 5 turned around. Both make <b>45</b>." % (X, X)))
    for a, b in [(7, 2), (4, 2), (7, 5), (3, 5), (4, 5), (6, 10), (9, 10), (2, 10)]:
        its.append(fact_q(a, b, rnd))
    its.append(choice_calc_q("Which fact has the answer 40?", 40, "5 %s 8" % X,
                             ["5 %s 7" % X, "2 %s 10" % X, "5 %s 9" % X],
                             "5 %s 8 = <b>40</b>. 5 %s 7 = 35, 2 %s 10 = 20 and 5 %s 9 = 45." % (X, X, X, X)))
    its.append(choice_calc_q("Which fact has the answer 18?", 18, "2 %s 9" % X,
                             ["2 %s 8" % X, "5 %s 3" % X, "2 %s 10" % X],
                             "2 %s 9 = <b>18</b>. 2 %s 8 = 16, 5 %s 3 = 15 and 2 %s 10 = 20." % (X, X, X, X)))
    its.append(true_sentence_q("5 %s 6 = 30" % X, ["5 %s 7 = 30" % X, "2 %s 8 = 18" % X, "10 %s 4 = 14" % X],
                               "<b>5 %s 6 = 30</b>. 5 %s 7 = 35, 2 %s 8 = 16 and 10 %s 4 = 40." % (X, X, X, X)))
    its.append(true_sentence_q("10 %s 9 = 90" % X, ["2 %s 6 = 8" % X, "5 %s 5 = 20" % X, "10 %s 6 = 16" % X],
                               "<b>10 %s 9 = 90</b>. 2 %s 6 = 12, 5 %s 5 = 25 and 10 %s 6 = 60." % (X, X, X, X),
                               "Only one of these number sentences is correct. Which one?"))
    its.append(mcq("10 %s 6 = 60. Use it to find 5 %s 6." % (X, X), 30, [60, 55, 11],
                   "5 is half of 10, so 5 %s 6 is half of 10 %s 6. Half of 60 is <b>30</b>." % (X, X)))
    its.append(mcq("5 %s 8 = 40. Use it to find 5 %s 9." % (X, X), 45, [41, 40, 50],
                   "5 %s 9 is one more group of 5 than 5 %s 8: 40 + 5 = <b>45</b>. "
                   "41 adds 1 instead of 5." % (X, X)))
    assert 10 * 6 // 2 == 5 * 6 and 5 * 9 == 40 + 5
    its.append(multiple_q("Which number is in the 2s?", 16, [15, 17, 21], 2, True))
    its.append(multiple_q("Which number is in the 5s?", 35, [33, 36, 52], 5, True))
    its.append(multiple_q("Which number is <b>not</b> in the 10s?", 45, [40, 60, 90], 10, False))
    assert len(its) == 20, len(its)
    return {"title": "Mixed practice", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def w(q, ans, unit, wrong, e, check):
        assert check == ans, (q, check, ans)
        assert ans not in wrong
        if unit == "¢":
            u = lambda v: "%d¢" % v
        elif unit == "$":
            u = lambda v: "$%d" % v
        else:
            u = lambda v: "%d %s" % (v, unit)
        its.append(mcq(q, u(ans), [u(v) for v in wrong], e))

    w("Each hockey team brings 10 players to the tournament. There are 6 teams. How many players is that?",
      60, "players", [16, 50, 70], "6 teams of 10: 6 %s 10 = <b>60</b>. 16 is 6 + 10, which adds instead of multiplies." % X,
      6 * 10)
    w("Juice boxes come in packs of 10. The teacher buys 4 packs for the field trip. How many juice boxes is that?",
      40, "juice boxes", [14, 30, 50], "4 packs of 10: 4 %s 10 = <b>40</b>. 4 tens make 40." % X, 4 * 10)
    nm, he, his = P.next()
    w(fig(coins_svg(8, 5)) + "%s has 8 nickels. A nickel is worth 5¢. How much money does %s have?" % (nm, he),
      40, "¢", [13, 35, 45], "8 %s 5¢ = <b>40¢</b>. 5, 10, 15, 20, 25, 30, 35, 40. "
      "35¢ is 7 nickels, one too few." % X, 8 * 5)
    w("Each student has 2 mitts. 9 students hang their mitts to dry after recess. How many mitts is that?",
      18, "mitts", [11, 16, 20], "9 %s 2 = <b>18</b>. Double 9 is 18. 11 is 9 + 2, which adds instead of multiplies." % X,
      9 * 2)
    nm, he, his = P.next()
    w(fig(coins_svg(7, 10)) + "%s has 7 dimes. A dime is worth 10¢. How much money does %s have?" % (nm, he),
      70, "¢", [17, 60, 80], "7 %s 10¢ = <b>70¢</b>. 7 tens make 70." % X, 7 * 10)
    w("Two people sit in each canoe. 8 canoes go out on the lake at the cottage. How many people is that?",
      16, "people", [10, 14, 18], "8 %s 2 = <b>16</b>. Double 8 is 16. 10 is 8 + 2, which adds instead of multiplies." % X, 8 * 2)
    w("30 students make teams of 5 in gym class. How many teams are there?", 6, "teams",
      [5, 7, 25], "30 ÷ 5 = ? Think 5 %s ? = 30. 5 %s 6 = 30, so there are <b>6 teams</b>." % (X, X), 30 // 5)
    w("Juice boxes come in packs of 10. The school needs 70 juice boxes for the Terry Fox Run. How many packs is that?",
      7, "packs", [6, 8, 60], "70 ÷ 10 = ? 10 %s 7 = 70, so they need <b>7 packs</b>." % X, 70 // 10)
    nm, he, his = P.next()
    w("%s has 45¢, all in nickels. How many nickels does %s have?" % (nm, he), 9, "nickels",
      [8, 40, 50], "Each nickel is 5¢. 45 ÷ 5 = ? 5 %s 9 = 45, so %s has <b>9 nickels</b>." % (X, he), 45 // 5)
    w("There are 20 skates in the lost and found. Skates come in pairs. How many pairs is that?", 10, "pairs",
      [18, 22, 40], "A pair is 2. 20 ÷ 2 = ? 2 %s 10 = 20, so there are <b>10 pairs</b>. "
      "40 is 20 %s 2, which multiplies instead of divides." % (X, X), 20 // 2)
    w("A farm puts 50 bottles of maple syrup into boxes of 10. How many boxes does it fill?", 5, "boxes",
      [4, 6, 40], "50 ÷ 10 = ? 10 %s 5 = 50, so it fills <b>5 boxes</b>." % X, 50 // 10)
    w("In a hockey game, each team has 5 skaters on the ice. How many skaters are on the ice for both teams?",
      10, "skaters", [7, 5, 15], "Two teams of 5: 2 %s 5 = <b>10</b>. 7 is 2 + 5, which adds instead of multiplies." % X,
      2 * 5)
    nm, he, his = P.next()
    nm2, he2, his2 = P.next()
    w("%s scores 3 goals this season. %s scores 5 times as many. How many goals does %s score?" % (nm, nm2, nm2),
      15, "goals", [8, 2, 20], "5 times as many as 3 means 5 %s 3 = <b>15</b>. 8 is 5 + 3, which adds instead of multiplies." % X,
      5 * 3)
    nm, he, his = P.next()
    w("%s’s class has 3 packs of 10 juice boxes. 24 students each take one. How many juice boxes are left?" % nm,
      6, "juice boxes", [30, 54, 7], "First 3 %s 10 = 30. Then 30 − 24 = <b>6</b>. 30 forgets the 24 juice boxes that were taken." % X,
      3 * 10 - 24)
    nm, he, his = P.next()
    w("%s shares 18 maple cookies equally with %s brother. How many cookies does each of them get?" % (nm, his),
      9, "cookies", [8, 16, 36], "2 people share 18. 18 ÷ 2 = ? 2 %s 9 = 18, so each gets <b>9 cookies</b>." % X, 18 // 2)
    w("At the skating rink, 5 children sit on each bench. There are 9 benches. How many children is that?",
      45, "children", [14, 40, 50], "9 %s 5 = <b>45</b>. 40 is 8 %s 5, one bench too few." % (X, X), 9 * 5)
    w("The teacher opens 8 boxes of crayons. Each box has 10 crayons. How many crayons is that?",
      80, "crayons", [18, 70, 90], "8 %s 10 = <b>80</b>. 8 tens make 80." % X, 8 * 10)
    w("On the bus for the field trip, 2 students sit in each seat. There are 16 students. How many seats do they fill?",
      8, "seats", [14, 18, 32], "16 ÷ 2 = ? 2 %s 8 = 16, so they fill <b>8 seats</b>. "
      "32 is 16 %s 2, which multiplies instead of divides." % (X, X), 16 // 2)
    nm, he, his = P.next()
    w("On a snow day, %s and 4 friends each make 2 snowballs. How many snowballs do they make?" % nm,
      10, "snowballs", [8, 6, 12], "%s and 4 friends is 5 children. 5 %s 2 = <b>10</b>. "
      "8 forgets to count %s." % (nm, X, nm), 5 * 2)
    w("Pizza lunch costs $5 for each student. 4 friends buy pizza lunch. How much do they pay in all?",
      20, "$", [9, 15, 25], "4 %s $5 = <b>$20</b>. $9 is 4 + 5, which adds instead of multiplies." % X, 4 * 5)
    assert len(its) == 20
    return {"title": "Word problems: hockey, juice boxes and nickels", "items": its}


# ============================================================ lesson
def body_html():
    rows = [[str(k), "%d %s 2 = %d" % (k, X, 2 * k), "%d %s 5 = %d" % (k, X, 5 * k),
             "%d %s 10 = %d" % (k, X, 10 * k)] for k in range(1, 11)]
    return (
        "<h2>Multiplication means equal groups</h2>"
        "<p><b>4 %s 5</b> means 4 groups of 5. Skip count by 5s: 5, 10, 15, 20. So 4 %s 5 = 20. "
        "You can multiply in any order: 5 %s 4 = 20 too.</p>" % (X, X, X)
        + "<figure class='sn-fig'>" + groups_svg(4, 5, 24, True)
        + "<figcaption>4 groups of 5: 5, 10, 15, 20. 4 %s 5 = 20.</figcaption></figure>" % X
        + "<p>An <b>array</b> shows equal rows. 2 rows of 7 dots is 2 %s 7 = 14.</p>" % X
        + "<figure class='sn-fig'>" + array_svg(2, 7)
        + "<figcaption>2 rows of 7: 2 %s 7 = 14.</figcaption></figure>" % X
        + "<h2>A trick for each fact</h2>"
        + table(["Facts", "Trick", "Example"], [
            ["%s 2" % X, "Double the number", "2 %s 8: 8 + 8 = 16" % X],
            ["%s 10" % X, "Count the tens; the answer ends in 0", "10 %s 6 = 60" % X],
            ["%s 5" % X, "Skip count by 5s, or take half of the 10s; the answer ends in 0 or 5",
             "5 %s 6: half of 60 = 30" % X],
        ])
        + "<figure class='sn-fig'>" + coins_svg(6, 5)
        + "<figcaption>Six nickels: 5, 10, 15, 20, 25, 30. 6 %s 5¢ = 30¢.</figcaption></figure>" % X
        + table(["", "2s", "5s", "10s"], rows)
        + ex("Example", "5 %s 7 = ?" % X, "Skip count by 5s, 7 jumps: 5, 10, 15, 20, 25, 30, 35. "
             "Or: 10 %s 7 = 70, and half of 70 is 35." % X, "35")
        + "<h2>Every fact gives division facts</h2>"
        "<p>Division is the opposite of multiplication. 5, 8 and 40 make a <b>fact family</b>: "
        "5 %s 8 = 40, 8 %s 5 = 40, 40 ÷ 5 = 8 and 40 ÷ 8 = 5. "
        "A division fact starts with the biggest number.</p>" % (X, X)
        + ex("Division", "14 ÷ 2 = ?", "Think: 2 %s ? = 14. 2 %s 7 = 14." % (X, X), "7")
        + ex("Missing factor", "? %s 10 = 60" % X, "Think: 60 ÷ 10. 6 tens make 60.", "6")
        + ex("Word problem", "Juice boxes come in packs of 10. How many juice boxes are in 3 packs?",
             "3 groups of 10: 10, 20, 30. So 3 %s 10 = 30." % X, "30 juice boxes")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding instead of multiplying: 5 %s 3 = 8" % X, "%s means groups of: 5 groups of 3 = 15" % X],
            ["Stopping one jump too soon: 5 %s 7 = 30" % X, "Count the jumps on your fingers: 7 jumps of 5 is 35"],
            ["Turning division around: 5 ÷ 35 = 7", "Start with the biggest number: 35 ÷ 5 = 7"],
            ["Giving the big number in division: 14 ÷ 2 = 14", "Ask: 2 times what makes 14? The answer is 7"],
        ])
    )


FAQ = [
    {"q": "What multiplication facts should a Grade 3 student know in Ontario?",
     "a": "The Ontario Mathematics Curriculum (2020) asks Grade 3 students to recall the multiplication facts for 2, 5 and 10 and the related division facts. In Grade 4 this grows to all facts up to 10 × 10."},
    {"q": "Is multiplication on the Grade 3 EQAO math test?",
     "a": "The Grade 3 EQAO math assessment is based on the Ontario curriculum, so it can include multiplication and division, often as short word problems. Knowing the 2, 5 and 10 facts quickly leaves more time to think about the problem."},
    {"q": "How can I help my child learn the 2, 5 and 10 times tables?",
     "a": "Skip count out loud by 2s, 5s and 10s, then practise a few facts each day. Counting nickels and dimes, or pairs of mitts, makes the facts real."},
    {"q": "What is a fact family in Grade 3 math?",
     "a": "A fact family is a set of related facts that use the same three numbers, such as 5 × 8 = 40, 8 × 5 = 40, 40 ÷ 5 = 8 and 40 ÷ 8 = 5. It shows students that every multiplication fact also gives two division facts."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(33801)
    P = People(rnd)
    sets = [set_facts(rnd), set_division(rnd), set_missing(rnd), set_mixed(rnd), set_words(P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-3", "slug": "multiplication-facts-for-2-5-and-10", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiplication Facts for 2, 5 and 10",
        "seo_title": "Grade 3 Multiplication Facts Worksheets: 2, 5 and 10 with Answer Key (Ontario)",
        "short_title": "Multiplication facts: 2, 5 and 10",
        "domain": "Number",
        "standard_code": "Grade 3: B2.2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Recall and demonstrate multiplication facts for 2, 5, and 10, and related division facts",
        "meta_desc": "Free Grade 3 math worksheets on the multiplication facts for 2, 5 and 10: arrays, skip counting, fact families, related division facts, missing factors and word problems. 100 questions with an answer key, following the Ontario curriculum and useful for EQAO.",
        "key_big": "The 2s are doubles. The 10s end in 0. The 5s are half of the 10s.",
        "key_sub": "Skip count to check: 5 × 7 is 7 jumps of 5, which is 35. Every fact gives division facts: 5 × 7 = 35, so 35 ÷ 5 = 7 and 35 ÷ 7 = 5.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(([5-9]|1[0-9]) equal groups|[0-9]+ equal groups with 10|[6-9] (nickels|dimes)|number line)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
