# -*- coding: utf-8 -*-
"""
CA Grade 4 Math (Ontario Mathematics Curriculum 2020, B2.2): multiplication facts for 1 x 1 to 10 x 10
and the related division facts.
  python3 tools/gen_caon_math_g4_facts.py
Every product, quotient and missing factor is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#e8f3ec"
BROWN = "#b5651d"
INK = "#2b2b2b"
GREY = "#9aa1a9"
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


def split_svg(rows, top, cols, cell=22):
    """An array of rows x cols split into top rows and the rest, with a label for each part."""
    o, gap, lab = 6, 10, 62
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
    return svg_wrap(W, H, "".join(s),
                    "array of %d rows with %d dots split into %d rows and %d rows" % (rows, cols, top, bot))


def hands_svg(k):
    """Ten fingers numbered 1 to 10, finger k folded down (the 9s finger trick for 9 x k)."""
    fw, gap, hgap, m = 18, 6, 22, 8
    tall, short, top = 70, 26, 8
    xs = []
    x = m
    for i in range(10):
        xs.append(x)
        x += fw + (hgap if i == 4 else gap)
    W = int(xs[-1] + fw + m)
    base = top + tall
    H = base + 26
    s = []
    for i, x0 in enumerate(xs):
        n = i + 1
        h = short if n == k else tall
        col, edge = (GREY, "#6b7178") if n == k else (FILL, GREEN)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x0, base - h, fw, h, col, edge))
        s.append(text(x0 + fw / 2, base + 20, str(n), 14))
    return svg_wrap(W, H, "".join(s), "ten fingers numbered 1 to 10 with finger %d folded down" % k)


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


def check_wrong(ans, wrong):
    assert ans not in wrong, (ans, wrong)


# ------------------------------------------------------------ strategies
def tip(a, b):
    """Strategy for a × b, where b is the fact family being practised."""
    p = a * b
    if b == 2:
        return "Double %d: %d + %d = <b>%d</b>." % (a, a, a, p)
    if b == 3:
        return "Double %d, then add one more %d: %d + %d = <b>%d</b>." % (a, a, 2 * a, a, p)
    if b == 4:
        return "Double, then double again: %d → %d → <b>%d</b>." % (a, 2 * a, p)
    if b == 5:
        return "Half of the 10s: 10 %s %d = %d, and half of %d is <b>%d</b>." % (X, a, 10 * a, 10 * a, p)
    if b == 10:
        return "%d tens make %d. So %d %s 10 = <b>%d</b>." % (a, p, a, X, p)
    raise ValueError(b)


def fact_cands(a, b, rnd):
    """Real mistakes: the fact next door (one group too many or too few) and adding instead of multiplying."""
    p = a * b
    pool = [(a - 1) * b, (a + 1) * b, a + b]
    pool = [v for v in pool if v > 0 and v != p]
    rnd.shuffle(pool)
    return pool + [a * (b + 1), a * (b - 1), p + 1, p - 1]


def fact_q(a, b, rnd):
    x, y = (a, b) if rnd.random() < 0.5 else (b, a)
    return mcq("%d %s %d = ?" % (x, X, y), a * b, fact_cands(a, b, rnd), tip(a, b))


def seq_q(seq, step, wrong, extra=""):
    nxt = seq[-1] + step
    assert all(seq[i + 1] - seq[i] == step for i in range(len(seq) - 1)) and seq[0] % step == 0
    check_wrong(nxt, wrong)
    e = "Each number is %d more than the one before: %d + %d = <b>%d</b>. %s" % (step, seq[-1], step, nxt, extra)
    return mcq("Skip count by %ds. What comes next?<br>%s, ?" % (step, ", ".join(map(str, seq))), nxt, wrong, e.strip())


# ============================================================ set 1: facts for 2, 3, 4, 5 and 10
def set_facts(rnd):
    its = []
    for r, c, wrong in [(3, 4, [7, 15, 16]), (3, 7, [10, 18, 24]), (4, 6, [10, 20, 28]), (4, 9, [13, 32, 40])]:
        p = r * c
        check_wrong(p, wrong)
        e = "There are %d rows with %d dots in each row. %d %s %d = <b>%d</b>." % (r, c, r, X, c, p)
        if r + c in wrong:
            e += " %d is %d + %d: that adds instead of multiplying." % (r + c, r, c)
        its.append(mcq(fig(array_svg(r, c)) + "How many dots are in this array?", p, wrong, e))
    for r, c in [(4, 7), (3, 8)]:
        p = r * c
        wrong = ["%d + %d" % (r, c), "%d %s %d" % (r, X, c + 1), "%d %s %d" % (r - 1, X, c)]
        e = ("There are %d rows with %d dots in each row, so it shows <b>%d %s %d</b> = %d. "
             "%d + %d adds the numbers instead of multiplying." % (r, c, r, X, c, p, r, c))
        its.append(choice_calc_q(fig(array_svg(r, c)) + "Which number sentence matches this array?", p,
                                 "%d %s %d" % (r, X, c), wrong, e))
    its.append(seq_q([12, 15, 18], 3, [20, 22, 24], "So 3 %s 7 = 21." % X))
    its.append(seq_q([20, 24, 28], 4, [30, 36, 31], "So 4 %s 8 = 32." % X))
    for b, mults in [(2, [7, 9]), (5, [6, 8]), (10, [4, 9]), (3, [6, 8, 9]), (4, [6, 7, 8])]:
        for a in mults:
            its.append(fact_q(a, b, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Facts for 2, 3, 4, 5 and 10 with arrays", "items": its}


# ============================================================ set 2: strategies for 6, 7, 8 and 9
def set_strategies(rnd):
    its = []
    for a in (7, 8, 9, 6):
        k, ans = 3 * a, 6 * a
        wrong = [k, k + 3, k + 6, 7 * a]
        check_wrong(ans, wrong)
        e = "6 is double 3, so 6 %s %d is double 3 %s %d: %d + %d = <b>%d</b>." % (X, a, X, a, k, k, ans)
        its.append(mcq("3 %s %d = %d. Double it to find 6 %s %d." % (X, a, k, X, a), ans, wrong, e))
    for k, wrong in [(4, [63, 45, 27]), (7, [36, 72, 54]), (6, [45, 63, 56])]:
        ans = 9 * k
        left, right = k - 1, 10 - k
        assert 10 * left + right == ans
        check_wrong(ans, wrong)
        e = ("Finger %d is down. There are %d fingers to the left (tens) and %d to the right (ones), "
             "so 9 %s %d = <b>%d</b>. Read the left side first." % (k, left, right, X, k, ans))
        its.append(mcq(fig(hands_svg(k)) + "The 9s finger trick: to find 9 %s %d, fold down finger %d. "
                       "What is 9 %s %d?" % (X, k, k, X, k), ans, wrong, e))
    for a in (8, 5):
        t, ans = 10 * a, 9 * a
        wrong = [t - 1, t, t + a, t - 10]
        e = ("9 groups is one group less than 10 groups. 10 %s %d = %d, then take away one %d: "
             "%d − %d = <b>%d</b>. Take away %d, not 1." % (X, a, t, a, t, a, ans, a))
        its.append(mcq("10 %s %d = %d. Use it to find 9 %s %d." % (X, a, t, X, a), ans, wrong, e))
    its.append(choice_calc_q("Which is a good way to work out 9 %s 7?" % X, 63, "10 %s 7 − 7" % X,
                             ["10 %s 7 − 1" % X, "10 %s 7 + 7" % X, "9 + 7"],
                             "9 sevens is one seven less than 10 sevens: 70 − 7 = <b>63</b>. "
                             "Taking away 1 gives 69, which is wrong."))
    nines = [9 * k for k in range(1, 11)]
    assert 72 in nines and not any(v in nines for v in (74, 65, 82))
    its.append(mcq("Which number is in the 9s?", 72, [74, 65, 82],
                   "The 9s are 9, 18, 27, 36, 45, 54, 63, <b>72</b>, 81, 90. "
                   "Up to 90, the two digits of a 9s fact add to 9: 7 + 2 = 9. "
                   "7 + 4 = 11, 6 + 5 = 11 and 8 + 2 = 10."))
    for a, wrong in [(7, [28, 32, 54]), (9, [36, 63, 81])]:
        k, ans = 4 * a, 8 * a
        check_wrong(ans, wrong)
        e = "8 is double 4, so 8 %s %d is double 4 %s %d: %d + %d = <b>%d</b>." % (X, a, X, a, k, k, ans)
        its.append(mcq("4 %s %d = %d. Double it to find 8 %s %d." % (X, a, k, X, a), ans, wrong, e))
    its.append(mcq("5 %s 8 = 40 and 2 %s 8 = 16. So 7 %s 8 = ?" % (X, X, X), 56, [54, 48, 15],
                   "7 eights = 5 eights + 2 eights. 40 + 16 = <b>56</b>. 54 is a common mix-up: 54 is 6 %s 9." % X))
    assert 5 * 8 + 2 * 8 == 56
    its.append(mcq(fig(split_svg(7, 5, 6)) + "Use the picture. What is 7 %s 6?" % X, 42, [36, 40, 13],
                   "The array is split into 5 %s 6 = 30 and 2 %s 6 = 12. 30 + 12 = <b>42</b>." % (X, X)))
    assert 5 * 6 + 2 * 6 == 42
    for known, kp, a, b, wrong in [((7, 7), 49, 7, 8, [50, 54, 57]), ((6, 6), 36, 6, 7, [37, 43, 48]),
                                   ((8, 8), 64, 8, 7, [63, 72, 54])]:
        assert known[0] * known[1] == kp
        ans = a * b
        check_wrong(ans, wrong)
        if b > known[1]:
            e = ("%d %s %d is one more group of %d than %d %s %d: %d + %d = <b>%d</b>. Add a whole %d, not 1."
                 % (a, X, b, a, known[0], X, known[1], kp, a, ans, a))
        else:
            e = ("%d %s %d is one group of %d less than %d %s %d: %d − %d = <b>%d</b>. Take away a whole %d, not 1."
                 % (a, X, b, a, known[0], X, known[1], kp, a, ans, a))
        its.append(mcq("Near fact: %d %s %d = %d. Use it to find %d %s %d." % (known[0], X, known[1], kp, a, X, b),
                       ans, wrong, e))
    its.append(true_sentence_q("7 %s 8 = 56" % X, ["7 %s 8 = 54" % X, "6 %s 9 = 56" % X, "8 %s 8 = 56" % X],
                               "<b>7 %s 8 = 56</b>. Say 5, 6, 7, 8: 56 = 7 %s 8. "
                               "6 %s 9 = 54 and 8 %s 8 = 64." % (X, X, X, X)))
    its.append(choice_calc_q("Which is the same as 6 %s 8?" % X, 48, "3 %s 8 + 3 %s 8" % (X, X),
                             ["3 %s 8 + 3" % X, "6 + 8", "5 %s 8 + 1" % X],
                             "6 groups of 8 = 3 groups of 8 + 3 groups of 8: 24 + 24 = <b>48</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Strategies for 6, 7, 8 and 9: doubles, the 9s trick and near facts", "items": its}


# ============================================================ set 3: division facts and fact families
def set_division(rnd):
    its = []
    for d, q in [(3, 8), (4, 7), (6, 7), (7, 8), (8, 6), (9, 7), (6, 9), (4, 9)]:
        p = d * q
        e = "Think: %d %s ? = %d. %d %s %d = %d, so %d ÷ %d = <b>%d</b>." % (d, X, p, d, X, q, p, p, d, q)
        its.append(mcq("%d ÷ %d = ?" % (p, d), q, [q + 1, q - 1, p - d, p], e))
    for r, c, wrong in [(4, 8, [7, 9, 28]), (3, 6, [5, 7, 15])]:
        p = r * c
        check_wrong(c, wrong)
        e = ("%d dots in %d equal rows: %d ÷ %d = <b>%d</b>. Check: %d %s %d = %d."
             % (p, r, p, r, c, r, X, c, p))
        its.append(mcq(fig(array_svg(r, c)) + "These %d dots are in %d equal rows. How many dots are in each row?"
                       % (p, r), c, wrong, e))
    for a, b in [(7, 9), (6, 8), (4, 6)]:
        p = a * b
        right = "%d ÷ %d = %d" % (p, a, b)
        wrong = ["%d ÷ %d = %d" % (b, a, p), "%d ÷ %d = %d" % (p, b, a + 1), "%d ÷ %d = %d" % (p, a, b - 1)]
        assert ok_sentence(right) and not any(ok_sentence(w) for w in wrong)
        e = ("%d, %d and %d make a fact family. %d %s %d = %d, so <b>%d ÷ %d = %d</b> and %d ÷ %d = %d. "
             "Division starts with the biggest number, %d." % (a, b, p, a, X, b, p, p, a, b, p, b, a, p))
        its.append(mcq("%d %s %d = %d. Which division fact is also true?" % (a, X, b, p), right, wrong, e))
    its.append(mcq("Which fact is in the same fact family as 8 %s 9 = 72?" % X, "72 ÷ 9 = 8",
                   ["9 ÷ 72 = 8", "8 + 9 = 17", "72 − 9 = 63"],
                   "The fact family for 8, 9 and 72 is 8 %s 9 = 72, 9 %s 8 = 72, 72 ÷ 8 = 9 and <b>72 ÷ 9 = 8</b>. "
                   "9 ÷ 72 is turned around: division starts with the biggest number." % (X, X)))
    its.append(mcq("Which is <b>not</b> in the same fact family as 4 %s 8 = 32?" % X, "32 ÷ 2 = 16",
                   ["8 %s 4 = 32" % X, "32 ÷ 4 = 8", "32 ÷ 8 = 4"],
                   "The fact family for 4, 8 and 32 is 4 %s 8, 8 %s 4, 32 ÷ 4 and 32 ÷ 8. "
                   "<b>32 ÷ 2 = 16</b> is true, but it uses 2 and 16, so it is not in this family." % (X, X)))
    its.append(mcq("Which three numbers make a multiplication fact family?", "4, 9, 36",
                   ["4, 9, 13", "4, 8, 36", "5, 7, 12"],
                   "4 %s 9 = 36, so <b>4, 9 and 36</b> make a fact family. 4 + 9 = 13 and 5 + 7 = 12 are adding, "
                   "and 4 %s 8 = 32, not 36." % (X, X)))
    its.append(mcq("Which fact helps you work out 54 ÷ 9?", "9 %s 6 = 54" % X,
                   ["9 %s 5 = 45" % X, "54 − 9 = 45", "54 + 9 = 63"],
                   "54 ÷ 9 asks: 9 times what makes 54? <b>9 %s 6 = 54</b>, so 54 ÷ 9 = 6." % X))
    its.append(mcq("Which multiplication fact checks 56 ÷ 8 = 7?", "7 %s 8 = 56" % X,
                   ["56 − 8 = 48", "8 %s 8 = 64" % X, "56 + 8 = 64"],
                   "Multiply the answer by the number you divided by: <b>7 %s 8 = 56</b>. "
                   "Subtracting 8 once does not undo dividing by 8." % X))
    for n, k, wrong in [(7, 9, [8, 10, 56]), (6, 6, [5, 7, 30])]:
        p = n * k
        check_wrong(k, wrong)
        e = "%d ÷ %d = ? Skip count by %ds to %d: %s. That is <b>%d</b> jumps." % (
            p, n, n, p, ", ".join(str(n * i) for i in range(1, k + 1)), k)
        its.append(mcq("How many %ds make %d?" % (n, p), k, wrong, e))
    assert 9 * 6 == 54 and 7 * 8 == 56 and 4 * 9 == 36 and 8 * 9 == 72
    assert len(its) == 20, len(its)
    return {"title": "Related division facts and fact families", "items": its}


# ============================================================ set 4: missing factors
def set_missing(rnd):
    its = []
    for a, b in [(3, 7), (4, 8), (6, 8), (7, 9), (8, 4), (9, 6)]:
        p = a * b
        e = "Ask: %d times what makes %d? %d ÷ %d = %d. Check: %d %s %d = %d, so ? = <b>%d</b>." % (
            a, p, p, a, b, a, X, b, p, b)
        its.append(mcq("%d %s ? = %d" % (a, X, p), b, [b + 1, b - 1, p - a, p + a], e))
    for a, b in [(8, 7), (9, 9), (4, 6), (6, 7), (3, 9), (10, 8)]:
        p = a * b
        e = "Ask: what times %d makes %d? %d ÷ %d = %d. Check: %d %s %d = %d, so ? = <b>%d</b>." % (
            b, p, p, b, a, a, X, b, p, a)
        its.append(mcq("? %s %d = %d" % (X, b, p), a, [a + 1, a - 1, p - b, p + b], e))
    for d, q in [(6, 7), (8, 9), (4, 6)]:
        p = d * q
        e = ("Division undoes multiplication, so multiply back: ? = %d %s %d = <b>%d</b>. Check: %d ÷ %d = %d."
             % (q, X, d, p, p, d, q))
        its.append(mcq("? ÷ %d = %d" % (d, q), p, [d + q, p + d, p - d, q - d], e))
    for p, q in [(63, 7), (32, 8), (54, 9)]:
        d = p // q
        assert d * q == p
        e = "Ask: %d ÷ what = %d? Think %d %s ? = %d. %d %s %d = %d, so ? = <b>%d</b>." % (
            p, q, q, X, p, q, X, d, p, d)
        its.append(mcq("%d ÷ ? = %d" % (p, q), d, [p - q, d + 1, d - 1, p + q], e))
    for r, c, wrong in [(3, 9, [8, 10, 24]), (5, 7, [6, 8, 30])]:
        p = r * c
        check_wrong(c, wrong)
        e = "There are %d rows. Count the dots in one row, or think %d ÷ %d = %d. So ? = <b>%d</b>." % (r, p, r, c, c)
        its.append(mcq(fig(array_svg(r, c)) + "This array has %d dots in %d rows. Fill in: %d %s ? = %d"
                       % (p, r, r, X, p), c, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Missing factors", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def w(q, ans, unit, wrong, e, check):
        assert check == ans, (q, check, ans)
        check_wrong(ans, wrong)
        if unit == "$":
            u = lambda v: "$%d" % v
        else:
            u = lambda v: "%d %s" % (v, unit)
        its.append(mcq(q, u(ans), [u(v) for v in wrong], e))

    w("Each canoe holds 3 campers. 7 canoes go out on the lake. How many campers is that?",
      21, "campers", [10, 18, 24], "7 canoes of 3: 7 %s 3 = <b>21</b>. 10 is 7 + 3, which adds instead of multiplies." % X,
      7 * 3)
    w("Muffins for the bake sale come in trays of 6. The class bakes 9 trays. How many muffins is that?",
      54, "muffins", [15, 48, 56], "9 trays of 6: 9 %s 6 = <b>54</b>. Use 10 %s 6 = 60, then take away one 6. "
      "15 is 9 + 6, which adds instead of multiplies." % (X, X), 9 * 6)
    nm, he, his = P.next()
    w("%s has 7 toonies. A toonie is worth $2. How much money does %s have?" % (nm, he),
      14, "$", [9, 12, 16], "7 %s $2 = <b>$14</b>. Double 7 is 14. $9 is 7 + 2, which adds instead of multiplies." % X,
      7 * 2)
    w("For the Terry Fox Run, 8 students each raise $6. How much do they raise in all?",
      48, "$", [14, 42, 54], "8 %s $6 = <b>$48</b>. 3 %s 8 = 24, and double 24 is 48. "
      "$14 is 8 + 6, which adds instead of multiplies." % (X, X), 8 * 6)
    w("For the school concert, the gym has 9 rows of chairs with 8 chairs in each row. How many chairs is that?",
      72, "chairs", [17, 63, 81], "9 %s 8 = <b>72</b>. 10 %s 8 = 80, then take away one 8: 80 − 8 = 72." % (X, X), 9 * 8)
    w("28 students go on a field trip. Parents drive them, with 4 students in each car. How many cars do they need?",
      7, "cars", [6, 8, 24], "28 ÷ 4 = ? Think 4 %s ? = 28. 4 %s 7 = 28, so they need <b>7 cars</b>." % (X, X), 28 // 4)
    w("The hockey coach puts 42 pucks into buckets, 6 pucks in each bucket. How many buckets does the coach fill?",
      7, "buckets", [6, 8, 36], "42 ÷ 6 = ? 6 %s 7 = 42, so the coach fills <b>7 buckets</b>." % X, 42 // 6)
    w("A sugar shack packs 48 bottles of maple syrup into boxes of 8. How many boxes does it fill?",
      6, "boxes", [5, 7, 40], "48 ÷ 8 = ? 8 %s 6 = 48, so it fills <b>6 boxes</b>." % X, 48 // 8)
    nm, he, his = P.next()
    nm2, he2, his2 = P.next()
    w("%s reads 6 books this fall. %s reads 4 times as many. How many books does %s read?" % (nm, nm2, nm2),
      24, "books", [10, 18, 30], "4 times as many as 6 means 4 %s 6 = <b>24</b>. "
      "10 is 4 + 6, which adds instead of multiplies." % X, 4 * 6)
    w("There are 7 pairs of winter boots in the hallway. How many boots is that?",
      14, "boots", [9, 12, 16], "A pair is 2. 7 %s 2 = <b>14</b>. 9 is 7 + 2, which adds instead of multiplies." % X,
      7 * 2)
    nm, he, his = P.next()
    w("%s puts 36 cookies onto 4 plates, with the same number on each plate. How many cookies go on each plate?" % nm,
      9, "cookies", [8, 32, 40], "36 ÷ 4 = ? 4 %s 9 = 36, so <b>9 cookies</b> go on each plate. "
      "32 is 36 − 4, which subtracts instead of divides." % X, 36 // 4)
    nm, he, his = P.next()
    w("%s buys 3 packs of hockey cards. Each pack has 8 cards. Then %s gives 5 cards to a friend. "
      "How many cards does %s have now?" % (nm, he, he),
      19, "cards", [24, 29, 6], "First 3 %s 8 = 24. Then 24 − 5 = <b>19</b>. "
      "24 forgets the 5 cards %s gave away." % (X, he), 3 * 8 - 5)
    w("Juice boxes come in packs of 6. The teacher buys 5 packs. 27 students each take one. How many juice boxes are left?",
      3, "juice boxes", [30, 4, 57], "First 5 %s 6 = 30. Then 30 − 27 = <b>3</b>. "
      "30 forgets the juice boxes that were taken." % X, 5 * 6 - 27)
    w("7 flocks of Canada geese fly over the school. Each flock has 9 geese. How many geese is that?",
      63, "geese", [16, 56, 72], "7 %s 9 = <b>63</b>. 10 %s 7 = 70, then take away one 7: 70 − 7 = 63. "
      "16 is 7 + 9, which adds instead of multiplies." % (X, X), 7 * 9)
    w("Skates cost $4 to rent at the skating rink. 9 friends rent skates. How much do they pay in all?",
      36, "$", [13, 32, 40], "9 %s $4 = <b>$36</b>. Double 9 is 18, and double 18 is 36. "
      "$13 is 9 + 4, which adds instead of multiplies." % X, 9 * 4)
    w("There are 63 chairs set up in 9 equal rows for the Remembrance Day assembly. How many chairs are in each row?",
      7, "chairs", [6, 8, 54], "63 ÷ 9 = ? 9 %s 7 = 63, so there are <b>7 chairs</b> in each row." % X, 63 // 9)
    nm, he, his = P.next()
    nm2, he2, his2 = P.next()
    w("%s has 8 hockey cards. %s has 7 times as many. How many hockey cards does %s have?" % (nm, nm2, nm2),
      56, "cards", [15, 54, 48], "7 times as many as 8 means 7 %s 8 = <b>56</b>. Say 5, 6, 7, 8: 56 = 7 %s 8. "
      "54 is a common mix-up, and 15 is 7 + 8." % (X, X), 7 * 8)
    w("Each pizza for the pizza lunch is cut into 8 slices. The class needs 40 slices. How many pizzas should they order?",
      5, "pizzas", [4, 6, 32], "40 ÷ 8 = ? 8 %s 5 = 40, so they should order <b>5 pizzas</b>." % X, 40 // 8)
    w("Each ringette team brings 10 players to the tournament. There are 4 teams. How many players is that?",
      40, "players", [14, 30, 50], "4 teams of 10: 4 %s 10 = <b>40</b>. 14 is 4 + 10, which adds instead of multiplies." % X,
      4 * 10)
    nm, he, his = P.next()
    w("%s plants a garden with 6 rows of tomato plants. There are 7 plants in each row. How many tomato plants is that?" % nm,
      42, "plants", [13, 36, 48], "6 %s 7 = <b>42</b>. 3 %s 7 = 21, and double 21 is 42. "
      "13 is 6 + 7, which adds instead of multiplies." % (X, X), 6 * 7)
    assert len(its) == 20
    return {"title": "Word problems: canoes, hockey cards and the bake sale", "items": its}


# ============================================================ lesson
def body_html():
    head = [X] + [str(n) for n in range(1, 11)]
    rows = [["<b>%d</b>" % r] + [str(r * c) for c in range(1, 11)] for r in range(1, 11)]
    return (
        "<h2>Know every fact to 10 %s 10</h2>"
        "<p>In Grade 4 you learn all the multiplication facts from 1 %s 1 to 10 %s 10. "
        "<b>7 %s 6</b> means 7 groups of 6. You can multiply in any order: 6 %s 7 is the same as 7 %s 6. "
        "So if you know the 2s, 3s, 4s, 5s and 10s, only a few facts are left to learn.</p>" % (X, X, X, X, X, X)
        + "<figure class='sn-fig'>" + array_svg(4, 9, 22)
        + "<figcaption>4 rows of 9: 9, 18, 27, 36. 4 %s 9 = 36.</figcaption></figure>" % X
        + "<h2>A strategy for each fact</h2>"
        + table(["Facts", "Strategy", "Example"], [
            ["%s 2" % X, "Double the number", "2 %s 8: 8 + 8 = 16" % X],
            ["%s 3" % X, "Double, then add one more group", "3 %s 7: 14 + 7 = 21" % X],
            ["%s 4" % X, "Double, then double again", "4 %s 6: 12, 24" % X],
            ["%s 5" % X, "Half of the 10s", "5 %s 8: half of 80 = 40" % X],
            ["%s 6" % X, "Double the 3s", "6 %s 7: 21 + 21 = 42" % X],
            ["%s 7" % X, "5s + 2s", "7 %s 8: 40 + 16 = 56" % X],
            ["%s 8" % X, "Double the 4s", "8 %s 6: 24 + 24 = 48" % X],
            ["%s 9" % X, "10s take away one group", "9 %s 7: 70 − 7 = 63" % X],
            ["%s 10" % X, "Count the tens", "10 %s 6 = 60" % X],
        ])
        + "<figure class='sn-fig'>" + split_svg(7, 5, 8)
        + "<figcaption>7 %s 8 = 5 %s 8 + 2 %s 8 = 40 + 16 = 56.</figcaption></figure>" % (X, X, X)
        + "<p><b>The 9s finger trick.</b> Hold up 10 fingers. For 9 %s 4, fold down finger 4. "
        "The 3 fingers to the left are tens and the 6 to the right are ones: 36.</p>" % X
        + "<figure class='sn-fig'>" + hands_svg(4)
        + "<figcaption>9 %s 4: 3 tens and 6 ones = 36.</figcaption></figure>" % X
        + ex("Near fact", "7 %s 7 = 49. What is 7 %s 8?" % (X, X),
             "7 %s 8 is one more group of 7: 49 + 7 = 56." % X, "56")
        + table(head, rows)
        + "<h2>Every fact gives division facts</h2>"
        "<p>Division undoes multiplication. 6, 9 and 54 make a <b>fact family</b>: "
        "6 %s 9 = 54, 9 %s 6 = 54, 54 ÷ 6 = 9 and 54 ÷ 9 = 6. "
        "A division fact starts with the biggest number.</p>" % (X, X)
        + ex("Division", "63 ÷ 9 = ?", "Think: 9 %s ? = 63. 9 %s 7 = 63." % (X, X), "7")
        + ex("Missing factor", "? %s 8 = 48" % X, "Think: 48 ÷ 8. 6 %s 8 = 48." % X, "6")
        + ex("Word problem", "Muffins come in trays of 6. How many muffins are in 8 trays?",
             "8 groups of 6: 3 %s 8 = 24, double 24 = 48. So 8 %s 6 = 48." % (X, X), "48 muffins")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Mixing up 7 %s 8 = 54 and 6 %s 9 = 54" % (X, X), "Say 5, 6, 7, 8: 56 = 7 %s 8" % X],
            ["Adding instead of multiplying: 6 %s 9 = 15" % X, "%s means groups of: 6 groups of 9 = 54" % X],
            ["9s from 10s: 10 %s 7 − 1 = 69" % X, "Take away a whole group: 70 − 7 = 63"],
            ["Turning division around: 8 ÷ 56 = 7", "Start with the biggest number: 56 ÷ 8 = 7"],
        ])
    )


FAQ = [
    {"q": "What multiplication facts should a Grade 4 student know in Ontario?",
     "a": "The Ontario Mathematics Curriculum (2020) asks Grade 4 students to recall the multiplication facts from 1 × 1 to 10 × 10 and the related division facts, such as 7 × 8 = 56 and 56 ÷ 8 = 7. In Grade 3 they learned the facts for 2, 5 and 10."},
    {"q": "Do Grade 4 students write EQAO in Ontario?",
     "a": "No. Ontario students write the EQAO assessments in Grades 3 and 6. Knowing every fact to 10 × 10 in Grade 4 builds a strong base for Grade 5 and Grade 6 math."},
    {"q": "What is the easiest way to remember 7 × 8?",
     "a": "Say “5, 6, 7, 8”: 56 = 7 × 8. You can also split it: 5 × 8 = 40 and 2 × 8 = 16, so 7 × 8 = 40 + 16 = 56."},
    {"q": "How can I help my child learn the 6, 7, 8 and 9 times tables?",
     "a": "Teach one strategy for each: double the 3s for the 6s, double the 4s for the 8s, and use the 10s and take away one group for the 9s. Practise a few facts each day and ask for the related division fact too."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(44801)
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
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-4", "slug": "multiplication-facts-to-10-x-10", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiplication Facts to 10 × 10",
        "seo_title": "Grade 4 Multiplication Facts Worksheets: Times Tables to 10 × 10 with Answer Key (Ontario)",
        "short_title": "Multiplication facts to 10 × 10",
        "domain": "Number",
        "standard_code": "Grade 4: B2.2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Recall and demonstrate multiplication facts for 1 × 1 to 10 × 10, and related division facts",
        "meta_desc": "Free Grade 4 math worksheets on the multiplication facts to 10 × 10: arrays, strategies for the 6s, 7s, 8s and 9s, fact families, related division facts, missing factors and word problems. 100 questions with an answer key, following the Ontario curriculum.",
        "key_big": "Learn a strategy for each fact: double the 3s for the 6s, double the 4s for the 8s, and use the 10s for the 9s.",
        "key_sub": "Every fact gives division facts: 7 × 8 = 56, so 56 ÷ 8 = 7 and 56 ÷ 7 = 8. Remember 5, 6, 7, 8: 56 = 7 × 8.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(ten fingers|array of [0-9]+ rows with [7-9] dots)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
