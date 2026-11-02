# -*- coding: utf-8 -*-
"""
UK Year 4 Maths (National Curriculum in England): Times tables up to 12 × 12
and the Multiplication Tables Check (MTC).
  python3 tools/gen_uk_maths_y4_times_tables.py
Every product, quotient and missing number is checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
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


def split_svg(rows, cols, cut, cell=24):
    """Array of rows x cols split after `cut` columns, with the column counts above and products below."""
    o, top, bot = 6, 26, 28
    W = cols * cell + 2 * o + 10
    H = top + rows * cell + bot
    xr = o + cut * cell + 10
    s = [dots(o, top, rows, cut, cell), dots(xr, top, rows, cols - cut, cell, RED),
         "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>"
         % (xr - 5, top - 4, xr - 5, top + rows * cell + 4, INK),
         text(o + cut * cell / 2, 18, str(cut)), text(xr + (cols - cut) * cell / 2, 18, str(cols - cut), col=RED),
         text(o + cut * cell / 2, top + rows * cell + 21, "%d %s %d = %d" % (cut, X, rows, cut * rows)),
         text(xr + (cols - cut) * cell / 2, top + rows * cell + 21, str((cols - cut) * rows), col=RED)]
    return svg_wrap(W, H, "".join(s), "%d rows of %d dots split into %d and %d columns" % (rows, cols, cut, cols - cut))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def digsum(n):
    return sum(int(d) for d in str(n))


# ------------------------------------------------------------ strategies
def tip(a, b):
    """Strategy for a × b, where b is the times table being practised."""
    p = a * b
    if b == 2:
        return "%d %s 2 is double %d: %d + %d = <b>%d</b>." % (a, X, a, a, a, p)
    if b == 3:
        return "Double %d is %d. Add one more %d: %d + %d = <b>%d</b>." % (a, 2 * a, a, 2 * a, a, p)
    if b == 4:
        return "Double, then double again: %d → %d → <b>%d</b>." % (a, 2 * a, p)
    if b == 5:
        return "%d %s 10 = %d. Half of %d is <b>%d</b>." % (a, X, 10 * a, 10 * a, p)
    if b == 10:
        return "Multiplying by 10 moves each digit one place to the left: %d %s 10 = <b>%d</b>." % (a, X, p)
    if b == 6:
        return "5 %s %d = %d. Add one more %d: %d + %d = <b>%d</b>." % (X, a, 5 * a, a, 5 * a, a, p)
    if b == 7:
        return "5 %s %d = %d and 2 %s %d = %d. %d + %d = <b>%d</b>." % (X, a, 5 * a, X, a, 2 * a, 5 * a, 2 * a, p)
    if b == 8:
        return "Double three times: %d → %d → %d → <b>%d</b>." % (a, 2 * a, 4 * a, p)
    if b == 9:
        s = "10 %s %d = %d. Take away one %d: %d − %d = <b>%d</b>." % (X, a, 10 * a, a, 10 * a, a, p)
        if digsum(p) == 9:
            s += " Check: the digits add up to 9."
        return s
    if b == 11:
        if a <= 9:
            return "For 11 %s %d, write the digit %d twice: <b>%d</b>." % (X, a, a, p)
        return "10 %s %d = %d. Add one more %d: %d + %d = <b>%d</b>." % (X, a, 10 * a, a, 10 * a, a, p)
    if b == 12:
        return "10 %s %d = %d and 2 %s %d = %d. %d + %d = <b>%d</b>." % (X, a, 10 * a, X, a, 2 * a, 10 * a, 2 * a, p)
    raise ValueError(b)


def rev(n):
    s = str(n)
    if len(s) == 2 and s[0] != s[1] and s[1] != "0":
        return int(s[::-1])
    return None


def fact_cands(a, b, rnd):
    """Real mistakes: neighbouring fact, one group too many/few, adding, swapped digits."""
    p = a * b
    pool = [a * (b + 1), a * (b - 1), (a + 1) * b, (a - 1) * b, a + b]
    r = rev(p)
    if r:
        pool.append(r)
    pool = [v for v in pool if v > 0 and v != p]
    rnd.shuffle(pool)
    return pool + [p + 10, p - 10, p + 2, p - 2]


def fact_q(a, b, rnd):
    """Question shows a × b or b × a; b is the table being practised."""
    x, y = (a, b) if rnd.random() < 0.5 else (b, a)
    return mcq("%d %s %d = ?" % (x, X, y), a * b, fact_cands(a, b, rnd), tip(a, b))


USED = set()


def pick_facts(tables, n, rnd, mults=range(2, 13)):
    combos = [(a, b) for b in tables for a in mults]
    rnd.shuffle(combos)
    out = []
    for a, b in combos:
        k = frozenset((a, b))
        if k in USED:
            continue
        USED.add(k)
        out.append((a, b))
        if len(out) == n:
            break
    assert len(out) == n
    return out


def check_seq(start, step, n=3):
    return [start + step * i for i in range(n)]


# ============================================================ set 1: arrays and the easier tables
def set_easy(rnd):
    its = []
    for r, c in [(6, 4), (3, 7), (2, 9), (4, 8)]:
        p = r * c
        e = "%d rows with %d dots in each row: %d %s %d = <b>%d</b>." % (r, c, r, X, c, p)
        its.append(mcq(fig(array_svg(r, c)) + "How many dots are in this array?", p,
                       [r + c, (r - 1) * c, r * (c + 1), r * (c - 1)], e))
    for r, c in [(5, 3), (3, 6), (4, 7), (2, 8)]:
        p = r * c
        right = "%d %s %d" % (r, X, c)
        wrong = [("%d + %d" % (r, c), r + c), ("%d %s %d" % (r, X, c + 1), r * (c + 1)),
                 ("%d %s %d" % (r + 1, X, c), (r + 1) * c), ("%d %s %d" % (r - 1, X, c), (r - 1) * c)]
        assert all(v != p for _, v in wrong)
        e = ("There are %d rows with %d dots in each row, so it shows %d %s %d = %d. "
             "%d %s %d gives the same answer: it is the array turned on its side." % (r, c, r, X, c, p, c, X, r))
        its.append(mcq(fig(array_svg(r, c)) + "Which multiplication matches this array?", right,
                       [w for w, _ in wrong], e))
    for a, b in pick_facts([2, 3, 4, 5, 10], 12, rnd, range(3, 13)):
        its.append(fact_q(a, b, rnd))
    return {"title": "Arrays and the 2, 3, 4, 5 and 10 times tables", "items": its}


# ============================================================ set 2: 6, 7 and 9
def seq_q(seq, step, wrong, extra):
    nxt = seq[-1] + step
    assert all(seq[i + 1] - seq[i] == step for i in range(len(seq) - 1)) and seq[0] % step == 0
    assert nxt not in wrong
    e = "Each number is %d more than the one before: %d + %d = <b>%d</b>. %s" % (step, seq[-1], step, nxt, extra)
    return mcq("Count in %ds. What comes next?<br>%s, ?" % (step, ", ".join(map(str, seq))), nxt, wrong, e)


def set_679(rnd):
    its = [fact_q(a, b, rnd) for a, b in pick_facts([6, 7, 9], 14, rnd)]
    its.append(seq_q([35, 42, 49], 7, [54, 55, 63], "So 7 %s 8 = 56. Don’t mix it up with 54 (6 %s 9)." % (X, X)))
    its.append(seq_q([36, 42, 48], 6, [52, 58, 60], "So 6 %s 9 = 54." % X))
    its.append(seq_q([54, 63, 72], 9, [82, 80, 90], "So 9 %s 9 = 81. The tens go up by 1 and the ones go down by 1." % X))
    for right, wrong, ask in [(63, [64, 69, 53], "Which number is in the 9 times table?"),
                              (54, [56, 59, 44], "Which of these is a multiple of 9?")]:
        assert right % 9 == 0 and all(w % 9 for w in wrong)
        e = ("%d %s 9 = <b>%d</b>. In the 9 times table up to 9 %s 10, the digits add up to 9: %d + %d = 9. "
             "The digits of the others add up to %s and %d."
             % (right // 9, X, right, X, right // 10, right % 10,
                ", ".join(str(digsum(w)) for w in wrong[:2]), digsum(wrong[2])))
        its.append(mcq(ask, right, wrong, e))
    its.append(mcq("Which calculation gives the answer to 9 %s 8?" % X, "10 %s 8 − 8" % X,
                   ["10 %s 8 − 9" % X, "10 %s 8 − 1" % X, "10 %s 9 − 9" % X],
                   "9 lots of 8 is one 8 less than 10 lots of 8: 80 − 8 = <b>72</b>. "
                   "10 %s 8 − 9 = 71 and 10 %s 8 − 1 = 79 take away the wrong amount." % (X, X)))
    assert 10 * 8 - 8 == 72 and 10 * 9 - 9 != 72
    return {"title": "The 6, 7 and 9 times tables", "items": its}


# ============================================================ set 3: 8, 11 and 12
def set_81112(rnd):
    its = [fact_q(a, b, rnd) for a, b in pick_facts([8, 11, 12], 14, rnd)]
    its.append(seq_q([40, 48, 56], 8, [62, 66, 72], "So 8 %s 8 = 64." % X))
    its.append(seq_q([24, 36, 48], 12, [56, 58, 72], "So 12 %s 5 = 60." % X))
    its.append(mcq("Which number is <b>not</b> in the 11 times table?", 101, [88, 110, 132],
                   "11 %s 9 = 99 and 11 %s 10 = 110, so <b>101</b> is not in the 11 times table. "
                   "88 = 11 %s 8, 110 = 11 %s 10 and 132 = 11 %s 12." % (X, X, X, X, X)))
    assert 101 % 11 and all(v % 11 == 0 for v in (88, 110, 132))
    for n in (6, 9):
        e = ("Split 12 into 10 and 2: 10 %s %d = %d and 2 %s %d = %d. %d + %d = <b>%d</b>."
             % (X, n, 10 * n, X, n, 2 * n, 10 * n, 2 * n, 12 * n))
        its.append(mcq("Which calculation gives the answer to 12 %s %d?" % (X, n),
                       "10 %s %d + 2 %s %d" % (X, n, X, n),
                       ["10 %s %d + 2" % (X, n), "10 %s %d + %d" % (X, n, n), "10 %s %d − 2 %s %d" % (X, n, X, n)], e))
        assert 10 * n + 2 != 12 * n and 11 * n != 12 * n and 8 * n != 12 * n
    its.append(mcq("4 %s 7 = 28. Use it to work out 8 %s 7." % (X, X), 56, [30, 35, 54],
                   "8 is double 4, so 8 %s 7 is double 4 %s 7: 28 + 28 = <b>56</b>. "
                   "Adding 2 or 7 to 28 does not double it." % (X, X)))
    return {"title": "The 8, 11 and 12 times tables", "items": its}


# ============================================================ set 4: division, missing numbers, mixed
def set_division(rnd):
    its = []
    for d, q in [(7, 8), (6, 9), (8, 12), (9, 7), (12, 11), (11, 6), (8, 4), (12, 9)]:
        p = d * q
        e = "Think: %d %s ? = %d. %d %s %d = %d, so %d ÷ %d = <b>%d</b>." % (d, X, p, d, X, q, p, p, d, q)
        its.append(mcq("%d ÷ %d = ?" % (p, d), q, [q + 1, q - 1, p - d, d, q + 2], e))
    for a, b in [(7, 9), (8, 7), (12, 8), (6, 8), (9, 12), (11, 7)]:
        p = a * b
        e = ("Ask: %d times what makes %d? Use the inverse: %d ÷ %d = %d. Check: %d %s %d = %d, so ? = <b>%d</b>."
             % (a, p, p, a, b, a, X, b, p, b))
        its.append(mcq("%d %s ? = %d" % (a, X, p), b, [b + 1, b - 1, p - a, a], e))
    for a, b in pick_facts([6, 7, 8, 9, 11, 12], 6, rnd, range(3, 13)):
        its.append(fact_q(a, b, rnd))
    return {"title": "Division facts, missing numbers and mixed facts", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def w(q, ans, unit, wrong, e, check):
        assert check == ans, (q, check, ans)
        u = (lambda v: "%d%s" % (v, unit)) if unit in ("p",) else (lambda v: "%d %s" % (v, unit) if unit else str(v))
        its.append(mcq(q, u(ans), [u(v) for v in wrong], e))

    nm, he, his = P.next()
    w("Eggs come in boxes of 12. %s buys 7 boxes for the school cake sale. How many eggs is that?" % nm, 84, "eggs",
      [74, 72, 19], "7 boxes of 12: 12 %s 7 = 70 + 14 = <b>84</b>. 72 is only 6 boxes." % X, 12 * 7)
    w("There are 11 players in a football team. How many players are in 6 teams?", 66, "players",
      [17, 55, 60], "6 teams of 11: 11 %s 6 = <b>66</b>. Write the 6 twice." % X, 11 * 6)
    w("How many days are there in 9 weeks?", 63, "days", [56, 16, 72],
      "There are 7 days in a week. 9 %s 7 = <b>63</b>. 56 is only 8 weeks." % X, 9 * 7)
    nm, he, his = P.next()
    w("Crisps come in multipacks of 6. %s buys 9 multipacks for a class party. How many bags of crisps does %s get?" % (nm, he),
      54, "bags", [45, 48, 15], "9 packs of 6: 9 %s 6 = <b>54</b>. 45 has the digits the wrong way round." % X, 9 * 6)
    nm, he, his = P.next()
    w("A spider has 8 legs. %s finds 7 spiders in the garden. How many legs is that altogether?" % nm, 56, "legs",
      [54, 15, 48], "7 %s 8 = <b>56</b>. Double 7 three times: 14, 28, 56." % X, 7 * 8)
    nm, he, his = P.next()
    w("A pencil costs 9p. %s buys 8 pencils. How much does %s spend?" % (nm, he), 72, "p", [81, 17, 64],
      "8 %s 9p = 80p − 8p = <b>72p</b>." % X, 8 * 9)
    w("48 pupils get into teams of 6 for PE. How many teams are there?", 8, "teams", [7, 42, 9],
      "48 ÷ 6 = ? Think 6 %s ? = 48. 6 %s 8 = 48, so there are <b>8 teams</b>." % (X, X), 48 // 6)
    w("A minibus holds 12 children. How many minibuses are needed for 96 children on a school trip?", 8, "minibuses",
      [7, 84, 9], "96 ÷ 12 = ? 12 %s 8 = 96, so <b>8 minibuses</b> are full with no one left behind." % X, 96 // 12)
    nm, he, his = P.next()
    w("Stickers cost 7p each. %s has 63p. How many stickers can %s buy?" % (nm, he), 9, "stickers", [8, 56, 10],
      "63 ÷ 7 = ? 7 %s 9 = 63, so %s can buy <b>9 stickers</b>." % (X, he), 63 // 7)
    w("In the school hall, there are 11 rows of chairs with 9 chairs in each row. How many chairs are there?", 99, "chairs",
      [20, 90, 88], "11 %s 9 = <b>99</b>. Write the 9 twice." % X, 11 * 9)
    w("How many weeks are there in 84 days?", 12, "weeks", [11, 77, 13],
      "There are 7 days in a week. 84 ÷ 7 = ? 7 %s 12 = 84, so <b>12 weeks</b>." % X, 84 // 7)
    w("There are 12 months in a year. How many months are there in 5 years?", 60, "months", [17, 48, 50],
      "12 %s 5 = 10 %s 5 + 2 %s 5 = 50 + 10 = <b>60</b>." % (X, X, X), 12 * 5)
    w("A baker puts 8 cupcakes on each tray. She fills 12 trays. How many cupcakes is that?", 96, "cupcakes",
      [88, 20, 69], "12 %s 8: double 12 three times: 24, 48, <b>96</b>. 88 is only 11 trays." % X, 12 * 8)
    nm, he, his = P.next()
    w("Felt tips come in packs of 12. %s has 132 felt tips. How many packs is that?" % nm, 11, "packs", [12, 120, 10],
      "132 ÷ 12 = ? 12 %s 11 = 120 + 12 = 132, so <b>11 packs</b>." % X, 132 // 12)
    nm, he, his = P.next()
    w("%s reads 6 pages of %s book every day for one week. How many pages does %s read?" % (nm, his, he), 42, "pages",
      [13, 36, 48], "There are 7 days in a week. 6 %s 7 = <b>42</b>." % X, 6 * 7)
    nm, he, his = P.next()
    nm2, he2, his2 = P.next()
    w("%s has 8 marbles. %s has 6 times as many marbles. How many marbles does %s have?" % (nm, nm2, nm2), 48, "marbles",
      [14, 40, 56], "6 times as many as 8 means 6 %s 8 = <b>48</b>. 14 is 6 + 8, which adds instead of multiplies." % X, 6 * 8)
    nm, he, his = P.next()
    w("%s buys 4 packs of 6 pens and 3 packs of 8 pens. How many pens does %s have altogether?" % (nm, he), 48, "pens",
      [21, 24, 46], "4 %s 6 = 24 and 3 %s 8 = 24. 24 + 24 = <b>48</b> pens." % (X, X), 4 * 6 + 3 * 8)
    nm, he, his = P.next()
    w("%s has 3 packs of 12 biscuits. %s gives 6 biscuits away. How many biscuits are left?" % (nm, he.capitalize()), 30, "biscuits",
      [36, 42, 9], "3 %s 12 = 36. Then 36 − 6 = <b>30</b>. 36 forgets the 6 given away." % X, 3 * 12 - 6)
    w("72 children sit at 9 tables at lunchtime. Each table has the same number of children. How many children sit at each table?",
      8, "children", [7, 63, 9], "72 ÷ 9 = ? 9 %s 8 = 72, so <b>8 children</b> sit at each table." % X, 72 // 9)
    nm, he, his = P.next()
    w("A packet of football stickers costs 7p. %s buys 11 packets. How much does %s spend?" % (nm, he), 77, "p",
      [18, 70, 84], "11 %s 7p = <b>77p</b>. Write the 7 twice." % X, 11 * 7)
    assert len(its) == 20
    return {"title": "Times tables word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Multiplication is equal groups</h2>"
        "<p><b>6 %s 4</b> means 6 lots of 4. In an array, that is 6 rows with 4 dots in each row. "
        "Turn the array on its side and you get 4 %s 6. The answer is the same: 24. "
        "So when you learn one fact, you know two.</p>" % (X, X)
        + "<figure class='sn-fig'>" + array_svg(6, 4, 30)
        + "<figcaption>6 rows of 4: 6 %s 4 = 24. The same array shows 4 %s 6 = 24, 24 ÷ 6 = 4 and 24 ÷ 4 = 6.</figcaption></figure>"
        % (X, X)
        + "<h2>The Multiplication Tables Check</h2>"
        "<p>By the end of Year 4, the National Curriculum says pupils should know all the times tables up to <b>12 %s 12</b>. "
        "In June of Year 4, children in England take the <b>Multiplication Tables Check (MTC)</b>. "
        "It is an online check of <b>25 questions</b> from the 2 to 12 times tables. "
        "Each question has <b>6 seconds</b> to type the answer. There is no pass mark: it shows which facts a child knows quickly.</p>" % X
        + "<h2>Tricks for the hardest tables</h2>"
        + table(["Table", "Trick", "Example"], [
            ["%s 6" % X, "%s 5, then add one more group" % X, "7 %s 6 = 35 + 7 = 42" % X],
            ["%s 7" % X, "%s 5 plus %s 2" % (X, X), "8 %s 7 = 40 + 16 = 56" % X],
            ["%s 8" % X, "Double, double, double", "6 %s 8: 12, 24, 48" % X],
            ["%s 9" % X, "%s 10, then take one group away" % X, "7 %s 9 = 70 − 7 = 63" % X],
            ["%s 11" % X, "Up to 11 %s 9, write the digit twice" % X, "11 %s 4 = 44" % X],
            ["%s 12" % X, "%s 10 plus %s 2" % (X, X), "12 %s 7 = 70 + 14 = 84" % X],
        ])
        + "<figure class='sn-fig'>" + split_svg(7, 12, 10)
        + "<figcaption>12 %s 7: split 12 into 10 and 2. 10 %s 7 = 70 and 2 %s 7 = 14. 70 + 14 = 84.</figcaption></figure>"
        % (X, X, X)
        + "<p>In the 9 times table, the digits add up to 9: 18, 27, 36, 45, 54, 63, 72, 81, 90. "
        "This is a quick way to check an answer.</p>"
        + ex("Example", "8 %s 7 = ?" % X, "5 %s 7 = 35 and 3 %s 7 = 21. 35 + 21 = 56. Or double 7 three times: 14, 28, 56." % (X, X), "56")
        + ex("Division", "63 ÷ 9 = ?", "Division is the inverse of multiplication. Think: 9 %s ? = 63. 9 %s 7 = 63." % (X, X), "7")
        + ex("Word problem", "Eggs come in boxes of 12. How many eggs are in 6 boxes?",
             "6 lots of 12: 10 %s 6 = 60 and 2 %s 6 = 12. 60 + 12 = 72." % (X, X), "72 eggs")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Mixing up a neighbouring fact: 7 %s 8 = 54 or 48" % X, "Use a trick: 7 %s 8 = 35 + 21 = 56" % X],
            ["Adding instead: 7 %s 8 = 15" % X, "%s means lots of: 7 lots of 8" % X],
            ["Swapping the digits: 12 %s 7 = 48" % X, "Split it: 70 + 14 = 84. Say the answer out loud"],
            ["One group too few: 8 %s 6 = 40" % X, "Count on from a fact you know: 5 %s 8 = 40, then 40 + 8 = 48" % X],
        ])
    )


FAQ = [
    {"q": "What is the Multiplication Tables Check?",
     "a": "It is a statutory online check that Year 4 pupils in England take in June. There are 25 multiplication questions from the 2 to 12 times tables, with 6 seconds to answer each one."},
    {"q": "Is there a pass mark for the Multiplication Tables Check?",
     "a": "No. It is a check, not a test you pass or fail. Each child gets a score out of 25, and schools use it to see which pupils need more help with their times tables."},
    {"q": "What times tables should a Year 4 child know?",
     "a": "All of them up to 12 × 12. The National Curriculum expects pupils to recall multiplication and division facts for every table from 2 to 12 by the end of Year 4."},
    {"q": "Which times tables are the hardest to learn?",
     "a": "Most children find the 6, 7, 8, 9, 11 and 12 times tables hardest. Learn a trick for each, such as × 9 = × 10 take away one group, then practise a few facts every day."},
]


def gen():
    USED.clear()
    rnd = random.Random(4401)
    P = People(rnd)
    sets = [set_easy(rnd), set_679(rnd), set_81112(rnd), set_division(rnd), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"]
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "uk", "subject": "maths", "grade": "year-4", "slug": "times-tables", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Times Tables up to 12 × 12 and the Multiplication Tables Check",
        "seo_title": "Year 4 Times Tables Worksheets: 12 × 12 Practice for the Multiplication Tables Check",
        "short_title": "Times tables",
        "domain": "Multiplication and division",
        "standard_code": "Year 4: Multiplication and division",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Recall multiplication and division facts for multiplication tables up to 12 × 12.",
        "meta_desc": "Free Year 4 times tables worksheets for the Multiplication Tables Check: arrays, tricks for the 6, 7, 8, 9, 11 and 12 times tables, division facts and word problems. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Learn a trick for every hard table: × 9 is × 10 take away one group, and × 12 is × 10 plus × 2.",
        "key_sub": "Every fact gives you two more: 7 × 8 = 56 means 8 × 7 = 56, 56 ÷ 7 = 8 and 56 ÷ 8 = 7. Know them all up to 12 × 12 by the end of Year 4.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
