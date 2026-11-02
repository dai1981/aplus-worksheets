# -*- coding: utf-8 -*-
"""
AU Year 4 Maths (Australian Curriculum v9.0, AC9M4A02): multiplication facts to 10 x 10
and related division facts, with strategies and facts with zeros.
  python3 tools/gen_au_maths_y4_multiplication_facts.py
Every product, quotient and missing number is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#e8f3ec"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
X = "×"
NB = " "


# ------------------------------------------------------------ helpers
def fmt(n):
    """Australian style: 4 digits plain, 5+ digits grouped with a no-break space."""
    s = str(n)
    if len(s) <= 4:
        return s
    out = ""
    while len(s) > 3:
        out = NB + s[-3:] + out
        s = s[:-3]
    return s + out


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
    o, gap, lab = 6, 10, 70
    bot = rows - top
    W = cols * cell + 2 * o + lab
    H = rows * cell + gap + 2 * o
    s = [dots(o, o, top, cols, cell, GREEN), dots(o, o + top * cell + gap, bot, cols, cell, "#b5651d")]
    y1 = o + top * cell / 2 + 6
    y2 = o + top * cell + gap + bot * cell / 2 + 6
    s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>"
             % (o, o + top * cell + gap / 2, o + cols * cell, o + top * cell + gap / 2, INK))
    s.append(text(o + cols * cell + 8, y1, "%d %s %d" % (top, X, cols), 15, "start", GREEN))
    s.append(text(o + cols * cell + 8, y2, "%d %s %d" % (bot, X, cols), 15, "start", "#b5651d"))
    return svg_wrap(W, H, "".join(s), "array of %d rows with %d dots split into %d rows and %d rows" % (rows, cols, top, bot))


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


def choice_calc_q(ask, target, right, wrong, e):
    assert calc(right) == target and all(calc(w) != target for w in wrong), (ask, right, wrong)
    return mcq(ask, right, wrong, e)


def true_sentence_q(right, wrong, e, ask="Which number sentence is true?"):
    def ok(s):
        lhs, rhs = s.split(" = ")
        return calc(lhs) == int(rhs)
    assert ok(right) and not any(ok(w) for w in wrong), (right, wrong)
    return mcq(ask, right, wrong, e)


# ------------------------------------------------------------ strategies
def tip(a, b):
    """Strategy for a × b, where b is the fact family being practised (6, 7, 8 or 9)."""
    p = a * b
    if b == 6:
        return "Double the 3s: 3 %s %d = %d, and double %d is <b>%d</b>." % (X, a, 3 * a, 3 * a, p)
    if b == 7:
        return "Split 7 into 5 + 2: 5 %s %d = %d and 2 %s %d = %d. %d + %d = <b>%d</b>." % (
            X, a, 5 * a, X, a, 2 * a, 5 * a, 2 * a, p)
    if b == 8:
        return "Double, double, double: %d → %d → %d → <b>%d</b>." % (a, 2 * a, 4 * a, p)
    if b == 9:
        return "Use the 10s: 10 %s %d = %d. Take away one group of %d: %d − %d = <b>%d</b>." % (
            X, a, 10 * a, a, 10 * a, a, p)
    raise ValueError(b)


def fact_cands(a, b, rnd):
    """Real mistakes: the fact next door, adding, and the well-known 7 x 8 / 6 x 8 mix-ups."""
    p = a * b
    pool = [a * (b + 1), a * (b - 1), (a + 1) * b, (a - 1) * b, a + b]
    if {a, b} == {7, 8}:
        pool = [54, 48, 63, 15]
    if {a, b} == {6, 8}:
        pool = [42, 56, 54, 14]
    pool = [v for v in pool if v > 0 and v != p]
    rnd.shuffle(pool)
    return pool + [p + 1, p - 1, p + 10, p - 10]


def fact_q(a, b, rnd):
    x, y = (a, b) if rnd.random() < 0.5 else (b, a)
    return mcq("%d %s %d = ?" % (x, X, y), a * b, fact_cands(a, b, rnd), tip(a, b))


def seq_q(seq, step, wrong, extra=""):
    nxt = seq[-1] + step
    assert all(seq[i + 1] - seq[i] == step for i in range(len(seq) - 1)) and seq[0] % step == 0
    assert nxt not in wrong
    e = "Each number is %d more than the one before: %d + %d = <b>%d</b>. %s" % (step, seq[-1], step, nxt, extra)
    return mcq("Skip count by %ds. What comes next?<br>%s, ?" % (step, ", ".join(map(str, seq))), nxt, wrong, e.strip())


# ============================================================ set 1: facts for 6, 7, 8 and 9
def set_facts(rnd):
    its = []
    for r, c, wrong in [(5, 6, [11, 25, 36]), (3, 8, [11, 21, 32]), (4, 7, [11, 21, 35]), (3, 9, [12, 18, 36])]:
        p = r * c
        assert p not in wrong
        e = "There are %d rows with %d dots in each row. %d %s %d = <b>%d</b>." % (r, c, r, X, c, p)
        its.append(mcq(fig(array_svg(r, c)) + "How many dots are in this array?", p, wrong, e))
    for r, c in [(6, 8), (7, 6)]:
        p = r * c
        wrong = ["%d + %d" % (r, c), "%d %s %d" % (r, X, c + 1), "%d %s %d" % (r - 1, X, c)]
        e = ("There are %d rows with %d dots in each row, so it shows %d %s %d = %d. "
             "%d %s %d gives the same answer: it is the array turned on its side." % (r, c, r, X, c, p, c, X, r))
        its.append(choice_calc_q(fig(array_svg(r, c)) + "Which number sentence matches this array?", p,
                                 "%d %s %d" % (r, X, c), wrong, e))
    its.append(seq_q([18, 24, 30], 6, [32, 31, 40], "So 6 %s 6 = 36." % X))
    its.append(seq_q([21, 28, 35], 7, [40, 36, 45], "So 7 %s 6 = 42." % X))
    its.append(seq_q([32, 40, 48], 8, [54, 49, 58], "So 8 %s 7 = 56." % X))
    its.append(seq_q([45, 54, 63], 9, [71, 64, 73], "So 9 %s 8 = 72." % X))
    for b, mults in [(6, [7, 9]), (7, [4, 7, 8]), (8, [6, 8]), (9, [3, 7, 9])]:
        for a in mults:
            its.append(fact_q(a, b, rnd))
    assert len(its) == 20, len(its)
    return {"title": "Facts for 6, 7, 8 and 9: arrays and skip counting", "items": its}


# ============================================================ set 2: division facts and fact families
def set_division(rnd):
    its = []
    for d, q in [(6, 7), (7, 8), (8, 6), (9, 7), (6, 9), (8, 9), (9, 4), (7, 7)]:
        p = d * q
        e = "Think: %d %s ? = %d. %d %s %d = %d, so %d ÷ %d = <b>%d</b>." % (d, X, p, d, X, q, p, p, d, q)
        its.append(mcq("%d ÷ %d = ?" % (p, d), q, [q + 1, q - 1, p - d, d, p], e))
    for a, b in [(6, 9), (8, 8)]:
        p = a * b
        e = "Ask: %d times what makes %d? %d ÷ %d = %d. Check: %d %s %d = %d, so ? = <b>%d</b>." % (
            a, p, p, a, b, a, X, b, p, b)
        its.append(mcq("%d %s ? = %d" % (a, X, p), b, [b + 1, b - 1, p - a, p + a], e))
    for a, b in [(9, 9), (4, 7)]:
        p = a * b
        e = "Ask: what times %d makes %d? %d ÷ %d = %d. Check: %d %s %d = %d, so ? = <b>%d</b>." % (
            b, p, p, b, a, a, X, b, p, a)
        its.append(mcq("? %s %d = %d" % (X, b, p), a, [a + 1, a - 1, p - b, p + b], e))
    for d, q in [(6, 8), (9, 5)]:
        p = d * q
        e = ("Division undoes multiplication, so multiply back: ? = %d %s %d = <b>%d</b>. Check: %d ÷ %d = %d."
             % (q, X, d, p, p, d, q))
        its.append(mcq("? ÷ %d = %d" % (d, q), p, [d + q, q - d, p + d, p - d], e))
    for a, b in [(7, 9), (6, 8)]:
        p = a * b
        right = "%d ÷ %d = %d" % (p, a, b)
        wrong = ["%d ÷ %d = %d" % (b, a, p), "%d ÷ %d = %d" % (p, b, a + 1), "%d ÷ %d = %d" % (p, a, b - 1)]
        assert p / a == b and all(int(w.split(" = ")[1]) != calc(w.split(" = ")[0]) for w in wrong)
        e = ("%d, %d and %d make a fact family. %d %s %d = %d, so <b>%d ÷ %d = %d</b> and %d ÷ %d = %d. "
             "Division starts with the biggest number, %d." % (a, b, p, a, X, b, p, p, a, b, p, b, a, p))
        its.append(mcq("%d %s %d = %d. Which division fact is also true?" % (a, X, b, p), right, wrong, e))
    its.append(mcq("Which fact helps you work out 72 ÷ 9?", "9 %s 8 = 72" % X,
                   ["9 %s 7 = 63" % X, "72 − 9 = 63", "72 + 9 = 81"],
                   "72 ÷ 9 asks: 9 times what makes 72? <b>9 %s 8 = 72</b>, so 72 ÷ 9 = 8." % X))
    its.append(mcq("Which fact helps you work out 42 ÷ 7?", "7 %s 6 = 42" % X,
                   ["7 %s 5 = 35" % X, "42 − 7 = 35", "6 + 7 = 13"],
                   "42 ÷ 7 asks: 7 times what makes 42? <b>7 %s 6 = 42</b>, so 42 ÷ 7 = 6." % X))
    its.append(mcq("Which multiplication fact checks 56 ÷ 8 = 7?", "7 %s 8 = 56" % X,
                   ["56 − 8 = 48", "8 %s 8 = 64" % X, "56 + 8 = 64"],
                   "Multiplication is the inverse of division, not subtraction or addition. "
                   "Multiply the answer by the number you divided by: <b>7 %s 8 = 56</b>." % X))
    its.append(mcq("Which multiplication fact checks 36 ÷ 9 = 4?", "4 %s 9 = 36" % X,
                   ["36 − 9 = 27", "4 + 9 = 13", "4 %s 8 = 32" % X],
                   "Multiply the answer by the number you divided by: <b>4 %s 9 = 36</b>. "
                   "Subtracting 9 once does not undo dividing by 9." % X))
    assert 9 * 8 == 72 and 7 * 6 == 42 and 7 * 8 == 56 and 4 * 9 == 36
    assert len(its) == 20, len(its)
    return {"title": "Related division facts and fact families", "items": its}


# ============================================================ set 3: strategies
def set_strategies(rnd):
    its = []
    for a in (7, 8, 9, 6):
        k, ans = 3 * a, 6 * a
        wrong = [k, k + 3, k + 6, 7 * a]
        e = "6 is double 3, so 6 %s %d is double 3 %s %d: %d + %d = <b>%d</b>." % (X, a, X, a, k, k, ans)
        its.append(mcq("3 %s %d = %d. Double it to find 6 %s %d." % (X, a, k, X, a), ans, wrong, e))
    for a in (7, 6, 8, 4):
        t, ans = 10 * a, 9 * a
        wrong = [t - 1, t, t + a, t - 10]
        e = ("9 groups is one group less than 10 groups. 10 %s %d = %d, then take away one %d: %d − %d = <b>%d</b>. "
             "Take away %d, not 1." % (X, a, t, a, t, a, ans, a))
        its.append(mcq("10 %s %d = %d. Use it to find 9 %s %d." % (X, a, t, X, a), ans, wrong, e))
    for a, wrong in [(7, [28, 32, 35]), (9, [36, 40, 81])]:
        k, ans = 4 * a, 8 * a
        assert ans not in wrong
        e = "8 is double 4, so 8 %s %d is double 4 %s %d: %d + %d = <b>%d</b>." % (X, a, X, a, k, k, ans)
        its.append(mcq("4 %s %d = %d. Double it to find 8 %s %d." % (X, a, k, X, a), ans, wrong, e))
    for a, wrong in [(8, [54, 48, 63]), (6, [35, 48, 36])]:
        f, t, ans = 5 * a, 2 * a, 7 * a
        assert ans not in wrong
        e = "7 groups = 5 groups + 2 groups. %d + %d = <b>%d</b>." % (f, t, ans)
        its.append(mcq("5 %s %d = %d and 2 %s %d = %d. So 7 %s %d = ?" % (X, a, f, X, a, t, X, a), ans, wrong, e))
    for a, b in [(8, 9), (6, 7)]:
        p = a * b
        e = ("Turnarounds have the same answer. %d %s %d = %d, so %d %s %d = <b>%d</b> too."
             % (a, X, b, p, b, X, a, p))
        its.append(mcq("%d %s %d = %d. So %d %s %d = ?" % (a, X, b, p, b, X, a), p, [a + b, p - a, p + a, p - b], e))
    for a, b in [(9, 7), (8, 6)]:
        p = a * b
        e = "%d %s %d is the turnaround of %d %s %d. Both make <b>%d</b>." % (b, X, a, a, X, b, p)
        its.append(choice_calc_q("Which has the same answer as %d %s %d?" % (a, X, b), p, "%d %s %d" % (b, X, a),
                                 ["%d + %d" % (a, b), "%d %s %d" % (a, X, a), "%d %s %d" % (b, X, b)], e))
    its.append(choice_calc_q("Which is a good way to work out 9 %s 6?" % X, 54, "10 %s 6 − 6" % X,
                             ["10 %s 6 − 1" % X, "10 %s 6 + 6" % X, "9 + 6"],
                             "9 sixes is one six less than 10 sixes: 60 − 6 = <b>54</b>. "
                             "Taking away 1 gives 59, which is wrong."))
    its.append(choice_calc_q("Which is the same as 6 %s 8?" % X, 48, "3 %s 8 + 3 %s 8" % (X, X),
                             ["3 %s 8 + 3" % X, "6 + 8", "5 %s 8 + 1" % X],
                             "6 groups of 8 = 3 groups of 8 + 3 groups of 8: 24 + 24 = <b>48</b>."))
    its.append(true_sentence_q("7 %s 8 = 56" % X, ["7 %s 8 = 54" % X, "6 %s 9 = 56" % X, "8 %s 8 = 56" % X],
                               "<b>7 %s 8 = 56</b>. Remember 5, 6, 7, 8: 56 = 7 %s 8. "
                               "6 %s 9 = 54 and 8 %s 8 = 64." % (X, X, X, X)))
    its.append(true_sentence_q("6 %s 9 = 54" % X, ["7 %s 9 = 56" % X, "6 %s 8 = 42" % X, "9 %s 9 = 72" % X],
                               "<b>6 %s 9 = 54</b>. 7 %s 9 = 63, 6 %s 8 = 48 and 9 %s 9 = 81." % (X, X, X, X),
                               "Only one of these number sentences is correct. Which one?"))
    assert len(its) == 20, len(its)
    return {"title": "Strategies: doubling, the 9s trick and turnarounds", "items": its}


# ============================================================ set 4: facts with zeros
def set_zeros(rnd):
    its = []
    for a, t, nb in [(6, 40, 50), (7, 30, 40), (8, 60, 70), (9, 70, 80), (80, 7, 6), (4, 90, 80), (9, 50, 60), (6, 70, 80)]:
        p = a * t
        small = p // 10
        if t % 10 == 0:
            f, ones = a, t // 10
            nbp = a * nb
            e = "%d %s %d = %d. %d %s %d tens = %d tens = <b>%s</b>." % (f, X, ones, small, f, X, ones, small, fmt(p))
            add = a + t
        else:
            f, ones = t, a // 10
            nbp = nb * a
            e = "%d %s %d = %d. %d tens %s %d = %d tens = <b>%s</b>." % (ones, X, f, small, ones, X, f, small, fmt(p))
            add = a + t
        wrong = [fmt(small), fmt(p * 10), fmt(nbp), fmt(add)]
        e += " Do not forget the zero."
        its.append(mcq("%d %s %d = ?" % (a, X, t), fmt(p), wrong, e))
    for a, h, nb in [(7, 400, 8), (9, 600, 8)]:
        p = a * h
        wrong = [fmt(p // 10), fmt(p * 10), fmt(nb * h), fmt(a + h)]
        e = "%d %s %d = %d. %d %s %d hundreds = %d hundreds = <b>%s</b>." % (
            a, X, h // 100, a * h // 100, a, X, h // 100, a * h // 100, fmt(p))
        its.append(mcq("%d %s %d = ?" % (a, X, h), fmt(p), wrong, e))
    for p, d in [(240, 8), (420, 6), (560, 7), (360, 9), (480, 6), (630, 9), (720, 8), (350, 7)]:
        q = p // d
        assert q * d == p and q % 10 == 0
        e = "%d is %d tens. %d tens ÷ %d = %d tens, so %d ÷ %d = <b>%d</b>. Check: %d %s %d = %d." % (
            p, p // 10, p // 10, d, q // 10, p, d, q, q, X, d, p)
        its.append(mcq("%d ÷ %d = ?" % (p, d), q, [q // 10, q * 10, q + 10, q - 10, p - d], e))
    its.append(mcq("8 %s ? = 320" % X, 40, [4, 400, 30, 312],
                   "32 = 8 %s 4, so 320 = 8 %s 40. ? = <b>40</b>." % (X, X)))
    its.append(mcq("? %s 9 = 540" % X, 60, [6, 600, 50, 531],
                   "54 = 6 %s 9, so 540 = 60 %s 9. ? = <b>60</b>." % (X, X)))
    assert 8 * 40 == 320 and 60 * 9 == 540
    assert len(its) == 20, len(its)
    return {"title": "Facts with zeros: 6 × 40 and 240 ÷ 8", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def w(q, ans, unit, wrong, e, check):
        assert check == ans, (q, check, ans)
        assert ans not in wrong
        if unit == "$":
            u = lambda v: "$" + fmt(v)
        else:
            u = lambda v: "%s %s" % (fmt(v), unit)
        its.append(mcq(q, u(ans), [u(v) for v in wrong], e))

    w("The school hall has 7 rows of chairs with 8 chairs in each row. How many chairs are there?", 56, "chairs",
      [15, 54, 48], "7 rows of 8: 7 %s 8 = <b>56</b>. 15 is 7 + 8, which adds instead of multiplies." % X, 7 * 8)
    w("Sausages come in packets of 8. The canteen buys 9 packets for the sausage sizzle. How many sausages is that?",
      72, "sausages", [17, 64, 81], "9 packets of 8: 9 %s 8 = <b>72</b>. 10 %s 8 = 80, take away one 8: 72." % (X, X), 9 * 8)
    w("A netball team has 7 players on the court. 6 teams play at the gala day. How many players is that?", 42, "players",
      [13, 36, 48], "6 teams of 7: 6 %s 7 = <b>42</b>. 13 is 6 + 7, which adds instead of multiplies." % X, 6 * 7)
    w("A huntsman spider has 8 legs. How many legs do 6 huntsman spiders have?", 48, "legs",
      [14, 42, 56], "6 %s 8 = <b>48</b>. Double 3 %s 8 = 24: 24 + 24 = 48." % (X, X), 6 * 8)
    nm, he, his = P.next()
    w("%s reads 9 pages of %s library book every night. How many pages does %s read in 7 nights?" % (nm, his, he),
      63, "pages", [16, 56, 72], "7 %s 9 = <b>63</b>. 10 %s 7 = 70, take away 7: 63." % (X, X), 7 * 9)
    nm, he, his = P.next()
    w("Muesli bars come in boxes of 6. %s’s mum buys 8 boxes for the school camp. How many bars is that?" % nm, 48,
      "bars", [14, 42, 54], "8 boxes of 6: 8 %s 6 = <b>48</b>. Double 8 %s 3 = 24: 24 + 24 = 48." % (X, X), 8 * 6)
    w("54 students make teams of 9 for tug of war. How many teams are there?", 6, "teams",
      [5, 7, 45], "54 ÷ 9 = ? Think 9 %s ? = 54. 9 %s 6 = 54, so there are <b>6 teams</b>. "
      "45 comes from 54 − 9, which takes away only one team." % (X, X), 54 // 9)
    w("63 students sit in rows of 9 at assembly. How many rows are there?", 7, "rows",
      [6, 8, 54], "63 ÷ 9 = ? 9 %s 7 = 63, so there are <b>7 rows</b>." % X, 63 // 9)
    nm, he, his = P.next()
    w("%s cuts 48 orange slices and shares them equally among 6 netball players. How many slices does each player get?"
      % nm, 8, "slices", [7, 9, 42], "48 ÷ 6 = ? 6 %s 8 = 48, so each player gets <b>8 slices</b>." % X, 48 // 6)
    w("The sausage sizzle needs 56 sausages. Sausages come in packets of 8. How many packets are needed?", 7, "packets",
      [6, 48, 64], "56 ÷ 8 = ? 8 %s 7 = 56, so <b>7 packets</b> are needed." % X, 56 // 8)
    w("Water bottles come in packs of 6. The coach needs 54 bottles for the athletics carnival. How many packs is that?",
      9, "packs", [8, 48, 60], "54 ÷ 6 = ? 6 %s 9 = 54, so the coach needs <b>9 packs</b>." % X, 54 // 6)
    w("81 students make teams of 9 for a maths quiz. How many teams are there?", 9, "teams",
      [8, 72, 90], "81 ÷ 9 = ? 9 %s 9 = 81, so there are <b>9 teams</b>." % X, 81 // 9)
    w("A bus holds 60 students. 7 buses go on the school excursion. How many students can travel?", 420, "students",
      [42, 4200, 67], "7 %s 6 tens = 42 tens = <b>420</b>. 42 forgets the zero." % X, 7 * 60)
    w("Tickets to the school disco cost $6. 80 students buy a ticket. How much money is collected?", 480, "$",
      [48, 4800, 86], "80 %s $6: 8 %s 6 = 48, so 8 tens %s 6 = <b>$480</b>." % (X, X, X), 80 * 6)
    w("Each student pays $8 for an excursion to the zoo. 30 students go. How much do they pay altogether?", 240, "$",
      [38, 24, 2400], "30 %s $8: 3 %s 8 = 24, so 3 tens %s 8 = <b>$240</b>. $38 adds instead of multiplies." % (X, X, X),
      30 * 8)
    w("360 students sit in 9 equal rows at the swimming carnival. How many students are in each row?", 40, "students",
      [4, 400, 351], "360 ÷ 9 = ? 36 ÷ 9 = 4, so 360 ÷ 9 = <b>40</b>. 351 comes from 360 − 9, which subtracts "
      "instead of dividing." , 360 // 9)
    nm, he, his = P.next()
    w("%s has 9 packets of 7 stickers. %s gives 10 stickers to a friend. How many stickers does %s have left?"
      % (nm, he.capitalize(), he), 53, "stickers", [63, 73, 46],
      "9 %s 7 = 63. Then 63 − 10 = <b>53</b>. 63 forgets the 10 given away." % X, 9 * 7 - 10)
    w("The class buys 6 packets of 8 sausages for a sausage sizzle. 5 sausages get burnt. How many are left to eat?", 43,
      "sausages", [48, 53, 37], "6 %s 8 = 48. Then 48 − 5 = <b>43</b>. 37 comes from using 6 %s 7 = 42 by mistake." % (X, X),
      6 * 8 - 5)
    w("The hall has 8 rows of 9 chairs. 65 people sit down. How many chairs are empty?", 7, "chairs",
      [72, 137, 17], "8 %s 9 = 72 chairs. 72 − 65 = <b>7</b> chairs are empty. 137 adds instead of subtracting." % X,
      8 * 9 - 65)
    nm, he, his = P.next()
    nm2, he2, his2 = P.next()
    w("%s saves $9. %s saves 6 times as much. How much does %s save?" % (nm, nm2, nm2), 54, "$",
      [15, 48, 63], "6 times as much as $9 means 6 %s $9 = <b>$54</b>. $15 is 6 + 9, which adds instead of multiplies." % X,
      6 * 9)
    assert len(its) == 20
    return {"title": "Word problems: rows, packets and teams", "items": its}


# ============================================================ lesson
def body_html():
    rows = [[str(k)] + ["%d" % (k * n) for n in (6, 7, 8, 9)] for k in range(1, 11)]
    return (
        "<h2>Know every fact to 10 %s 10</h2>"
        "<p>In Year 4 you learn all the multiplication facts up to 10 %s 10. "
        "You already know the 2s, 3s, 4s, 5s and 10s. Turnarounds mean you know most of the rest too: "
        "6 %s 4 is the same as 4 %s 6. The new facts to learn are the 6s, 7s, 8s and 9s.</p>" % (X, X, X, X)
        + "<figure class='sn-fig'>" + array_svg(6, 7, 22)
        + "<figcaption>6 rows of 7: 7, 14, 21, 28, 35, 42. 6 %s 7 = 42.</figcaption></figure>" % X
        + "<h2>A trick for each fact family</h2>"
        + table(["Facts", "Trick", "Example"], [
            ["%s 6" % X, "Double the 3s", "6 %s 7: 3 %s 7 = 21, double = 42" % (X, X)],
            ["%s 7" % X, "5s + 2s", "7 %s 8: 40 + 16 = 56" % X],
            ["%s 8" % X, "Double, double, double", "8 %s 6: 12, 24, 48" % X],
            ["%s 9" % X, "10s take away one group", "9 %s 7: 70 − 7 = 63" % X],
        ])
        + "<figure class='sn-fig'>" + split_svg(7, 5, 8)
        + "<figcaption>7 %s 8 = 5 %s 8 + 2 %s 8 = 40 + 16 = 56.</figcaption></figure>" % (X, X, X)
        + table(["", "6s", "7s", "8s", "9s"], rows)
        + ex("Example", "9 %s 6 = ?" % X, "10 %s 6 = 60. Take away one 6: 60 − 6 = 54." % X, "54")
        + "<h2>Every fact gives division facts</h2>"
        "<p>Division is the inverse of multiplication. 7, 8 and 56 make a <b>fact family</b>: "
        "7 %s 8 = 56, 8 %s 7 = 56, 56 ÷ 7 = 8 and 56 ÷ 8 = 7.</p>" % (X, X)
        + ex("Division", "63 ÷ 9 = ?", "Think: 9 %s ? = 63. 9 %s 7 = 63." % (X, X), "7")
        + "<h2>Facts with zeros</h2>"
        "<p>Use the fact you know, then think in tens. 6 %s 4 = 24, so 6 %s 40 = 24 tens = 240.</p>" % (X, X)
        + ex("Multiply", "6 %s 40 = ?" % X, "6 %s 4 = 24. 6 %s 4 tens = 24 tens." % (X, X), "240")
        + ex("Divide", "240 ÷ 8 = ?", "240 is 24 tens. 24 ÷ 8 = 3, so 24 tens ÷ 8 = 3 tens.", "30")
        + ex("Word problem", "Sausages come in packets of 8. How many sausages are in 7 packets?",
             "7 packets of 8: 7 %s 8 = 56." % X, "56 sausages")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Mixing up 7 %s 8 = 54 and 6 %s 9 = 54" % (X, X), "Say 5, 6, 7, 8: 56 = 7 %s 8" % X],
            ["Adding instead: 6 %s 9 = 15" % X, "%s means groups of: 6 groups of 9 = 54" % X],
            ["9s trick: 10 %s 7 − 1 = 69" % X, "Take away a whole group: 70 − 7 = 63"],
            ["Dropping the zero: 6 %s 40 = 24" % X, "6 %s 4 tens = 24 tens = 240" % X],
            ["Checking 56 ÷ 8 = 7 with 56 − 8", "Check with multiplication: 7 %s 8 = 56" % X],
        ])
    )


FAQ = [
    {"q": "What multiplication facts should a Year 4 student know in Australia?",
     "a": "The Australian Curriculum (v9.0) asks Year 4 students to recall all multiplication facts up to 10 × 10 and the related division facts, such as 7 × 8 = 56 and 56 ÷ 8 = 7. They also use these facts for larger numbers, like 6 × 40 = 240."},
    {"q": "Do Year 4 students sit NAPLAN?",
     "a": "No. NAPLAN is for Years 3, 5, 7 and 9. Knowing every fact to 10 × 10 by the end of Year 4 gives students a strong start for the Year 5 numeracy test."},
    {"q": "What is the easiest way to remember 7 × 8?",
     "a": "Say “5, 6, 7, 8”: 56 = 7 × 8. You can also split it: 5 × 8 = 40 and 2 × 8 = 16, so 7 × 8 = 40 + 16 = 56."},
    {"q": "How can I help my child learn the 6, 7, 8 and 9 times tables?",
     "a": "Teach one trick for each: double the 3s for the 6s, double three times for the 8s, and use the 10s and take away one group for the 9s. Practise a few facts each day and ask for the related division fact too."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(4801)
    P = People(rnd)
    sets = [set_facts(rnd), set_division(rnd), set_strategies(rnd), set_zeros(rnd), set_words(P)]
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
        "country": "au", "subject": "maths", "grade": "year-4", "slug": "multiplication-facts-to-10-x-10", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiplication Facts to 10 × 10",
        "seo_title": "Year 4 Multiplication Facts Worksheets: Times Tables to 10 × 10 with Answers",
        "short_title": "Multiplication facts to 10 × 10",
        "domain": "Algebra",
        "standard_code": "AC9M4A02",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Recall and demonstrate proficiency with multiplication facts up to 10 x 10 and related division facts; extend and apply facts to develop efficient mental strategies for computation with larger numbers without a calculator",
        "meta_desc": "Free Year 4 maths worksheets on multiplication facts to 10 × 10: the 6, 7, 8 and 9 times tables, related division facts, mental strategies, facts with zeros like 6 × 40, and word problems. 100 questions with an answer key, following the Australian Curriculum.",
        "key_big": "Use a fact you know to find one you don’t.",
        "key_sub": "Double the 3s for the 6s, double three times for the 8s, and for the 9s use the 10s and take away one group: 9 × 7 = 70 − 7 = 63. Every fact gives division facts and facts with zeros: 56 ÷ 8 = 7 and 7 × 80 = 560.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "array of [0-9]+ rows with [7-9] dots")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
