# -*- coding: utf-8 -*-
"""
US Grade 3 Math: Two-Step Word Problems (3.OA.D.8)
  python tools/gen_us_math_g3_two_step.py
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-3")
UPDATED = "2026-11-01"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd):
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


class People:
    def __init__(self, rnd):
        self.rnd = rnd
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ problem templates
# Each template returns a dict:
#   q     the story,  ans  the answer (number),  unit  word after the number ("" for money, which uses $)
#   s1/s2 the two steps as text,  wrong  answers from typical mistakes,  eq / eq_wrong  equations with a letter
def money(v):
    return "$%d" % v


def t_get_give(r, P):
    n, he, his = P.next()
    a, b, c = r.randint(24, 68), r.randint(12, 35), r.randint(8, 30)
    t = a + b
    return dict(q="%s had %d stickers. %s got %d more from a friend and then gave %d to %s brother. "
                  "How many stickers does %s have now?" % (n, a, cap(he), b, c, his, n),
                ans=t - c, unit="stickers", s1="Got more: %d + %d = %d." % (a, b, t), s2="Gave away: %d − %d = %d." % (t, c, t - c),
                wrong=[t, a + b + c, a - b + c if a - b + c > 0 else t + 10, t - c + 10],
                L="s", eq="%d + %d − %d = s" % (a, b, c), eq_wrong=["%d + %d + %d = s" % (a, b, c), "%d − %d + %d = s" % (a, b, c), "%d + %d = s" % (a, b)])


def t_bus(r, P):
    a, b, c = r.randint(30, 58), r.randint(8, 25), r.randint(6, 22)
    t = a - b
    return dict(q="A bus had %d people on it. At the first stop, %d people got off and %d people got on. "
                  "How many people are on the bus now?" % (a, b, c),
                ans=t + c, unit="people", s1="Got off: %d − %d = %d." % (a, b, t), s2="Got on: %d + %d = %d." % (t, c, t + c),
                wrong=[t, a - b - c, a + b + c, t + c - 10],
                L="p", eq="%d − %d + %d = p" % (a, b, c), eq_wrong=["%d + %d + %d = p" % (a, b, c), "%d − %d − %d = p" % (a, b, c), "%d − %d = p" % (a, b)])


def t_bake(r, P):
    a, b = r.randint(36, 85), r.randint(28, 70)
    c = r.randint(25, a + b - 15)
    t = a + b
    return dict(q="A bakery made %d muffins in the morning and %d muffins in the afternoon. It sold %d muffins. "
                  "How many muffins are left?" % (a, b, c),
                ans=t - c, unit="muffins", s1="Muffins made: %d + %d = %d." % (a, b, t), s2="Left after selling: %d − %d = %d." % (t, c, t - c),
                wrong=[t, a + b + c, abs(a - c) + b + 10, t - c + 10],
                L="m", eq="%d + %d − %d = m" % (a, b, c), eq_wrong=["%d + %d + %d = m" % (a, b, c), "%d − %d − %d = m" % (a, b, c), "%d + %d = m" % (a, b)])


def t_more_than(r, P):
    n, he, his = P.next()
    a, b = r.randint(18, 45), r.randint(6, 19)
    t = a + b
    return dict(q="%s read %d pages on Monday. On Tuesday, %s read %d more pages than on Monday. "
                  "How many pages did %s read on both days?" % (n, a, he, b, n),
                ans=a + t, unit="pages", s1="Tuesday: %d + %d = %d pages." % (a, b, t), s2="Both days: %d + %d = %d." % (a, t, a + t),
                wrong=[t, a + b + b, 2 * a, a + t + 10],
                L="p", eq="%d + (%d + %d) = p" % (a, a, b), eq_wrong=["%d + %d = p" % (a, b), "%d + %d + %d = p" % (a, b, b), "%d − %d + %d = p" % (a, b, a)])


def t_money_left(r, P):
    n, he, his = P.next()
    a = r.randint(30, 60)
    b, c = r.randint(8, 18), r.randint(3, 9)
    return dict(q="%s has $%d. %s buys a book for $%d and a pen for $%d. How much money does %s have left?" % (n, a, cap(he), b, c, n),
                ans=a - b - c, unit="$", s1="Spent: $%d + $%d = $%d." % (b, c, b + c), s2="Left: $%d − $%d = $%d." % (a, b + c, a - b - c),
                wrong=[a - b, b + c, a - b + c, a - c],
                L="m", eq="%d − %d − %d = m" % (a, b, c), eq_wrong=["%d − %d + %d = m" % (a, b, c), "%d + %d + %d = m" % (a, b, c), "%d − %d = m" % (a, b)])


def t_class(r, P):
    a = r.randint(24, 32)
    g = r.randint(a // 2 + 2, a - 6)
    boys = a - g
    return dict(q="There are %d students in a class. %d of them are girls. How many more girls than boys are there?" % (a, g),
                ans=g - boys, unit="more girls", s1="Boys: %d − %d = %d." % (a, g, boys), s2="How many more girls: %d − %d = %d." % (g, boys, g - boys),
                wrong=[boys, a - g - boys if a - g - boys > 0 else a + g, a + g, g],
                L="d", eq="%d − (%d − %d) = d" % (g, a, g), eq_wrong=["%d − %d = d" % (a, g), "%d + %d = d" % (a, g), "%d − %d − %d = d" % (a, g, g)])


def t_packs_give(r, P):
    n, he, his = P.next()
    k, m = r.randint(3, 9), r.randint(4, 10)
    c = r.randint(3, k * m - 5)
    t = k * m
    return dict(q="%s buys %d packs of pencils. Each pack has %d pencils. %s gives %d pencils to friends. "
                  "How many pencils does %s have left?" % (n, k, m, cap(he), c, n),
                ans=t - c, unit="pencils", s1="Pencils in all: %d × %d = %d." % (k, m, t), s2="Left: %d − %d = %d." % (t, c, t - c),
                wrong=[t, k + m - c if k + m - c > 0 else t + c, t + c, k * (m - 1)],
                L="p", eq="%d × %d − %d = p" % (k, m, c), eq_wrong=["%d + %d − %d = p" % (k, m, c), "%d × %d + %d = p" % (k, m, c), "%d × %d = p" % (k, m)])


def t_rows_add(r, P):
    k, m = r.randint(4, 9), r.randint(5, 10)
    c = r.randint(4, 15)
    t = k * m
    return dict(q="A hall has %d rows of chairs with %d chairs in each row. %d more chairs are added at the back. "
                  "How many chairs are there now?" % (k, m, c),
                ans=t + c, unit="chairs", s1="Chairs in rows: %d × %d = %d." % (k, m, t), s2="Add the new chairs: %d + %d = %d." % (t, c, t + c),
                wrong=[t, k + m + c, k * (m + c), t - c],
                L="c", eq="%d × %d + %d = c" % (k, m, c), eq_wrong=["%d + %d + %d = c" % (k, m, c), "%d × %d − %d = c" % (k, m, c), "%d × (%d + %d) = c" % (k, m, c)])


def t_boxes_loose(r, P):
    n, he, his = P.next()
    k, m = r.randint(3, 8), r.choice([6, 8, 10, 12])
    c = r.randint(3, m - 1)
    t = k * m
    return dict(q="A box holds %d crayons. %s has %d full boxes and %d extra crayons. How many crayons does %s have?" % (m, n, k, c, n),
                ans=t + c, unit="crayons", s1="Crayons in boxes: %d × %d = %d." % (k, m, t), s2="Add the extra crayons: %d + %d = %d." % (t, c, t + c),
                wrong=[t, k + m + c, (k + 1) * m, t + c + 10],
                L="c", eq="%d × %d + %d = c" % (k, m, c), eq_wrong=["%d + %d + %d = c" % (k, m, c), "%d × %d − %d = c" % (k, m, c), "%d × %d = c" % (k, m)])


def t_change(r, P):
    n, he, his = P.next()
    k, m = r.randint(2, 5), r.randint(3, 9)
    t = k * m
    pay = [v for v in (10, 20, 50) if v > t + 2][0]
    return dict(q="Movie tickets cost $%d each. %s buys %d tickets and pays with a $%d bill. How much change does %s get?" % (m, n, k, pay, he),
                ans=pay - t, unit="$", s1="Cost of the tickets: %d × $%d = $%d." % (k, m, t), s2="Change: $%d − $%d = $%d." % (pay, t, pay - t),
                wrong=[t, pay - m, pay - k - m, pay - t + 10],
                L="c", eq="%d − %d × %d = c" % (pay, k, m), eq_wrong=["%d − %d − %d = c" % (pay, k, m), "%d × %d = c" % (k, m), "%d + %d × %d = c" % (pay, k, m)])


def t_save_spend(r, P):
    n, he, his = P.next()
    k, m = r.randint(4, 9), r.randint(4, 10)
    t = k * m
    c = r.randint(6, t - 8)
    return dict(q="%s saves $%d each week for %d weeks. Then %s spends $%d on a game. How much money does %s have left?" % (n, m, k, he, c, n),
                ans=t - c, unit="$", s1="Saved: %d × $%d = $%d." % (k, m, t), s2="Left: $%d − $%d = $%d." % (t, c, t - c),
                wrong=[t, k + m + c, t + c, m * (k - 1)],
                L="m", eq="%d × %d − %d = m" % (k, m, c), eq_wrong=["%d + %d − %d = m" % (k, m, c), "%d × %d + %d = m" % (k, m, c), "%d × %d = m" % (k, m)])


def t_times_longer(r, P):
    m, k = r.randint(4, 12), r.randint(3, 6)
    t = k * m
    return dict(q="A red ribbon is %d cm long. A blue ribbon is %d times as long as the red ribbon. "
                  "How much longer is the blue ribbon than the red ribbon?" % (m, k),
                ans=t - m, unit="cm", s1="Blue ribbon: %d × %d = %d cm." % (k, m, t), s2="How much longer: %d − %d = %d cm." % (t, m, t - m),
                wrong=[t, t + m, k + m, m * (k + 1)],
                L="n", eq="%d × %d − %d = n" % (k, m, m), eq_wrong=["%d × %d = n" % (k, m), "%d × %d + %d = n" % (k, m, m), "%d + %d = n" % (k, m)])


def t_share_eat(r, P):
    k, each = r.randint(3, 8), r.randint(5, 9)
    a = k * each
    c = r.randint(2, each - 2)
    return dict(q="%d cookies are shared equally among %d friends. Each friend eats %d cookies. "
                  "How many cookies does each friend have left?" % (a, k, c),
                ans=each - c, unit="cookies", s1="Each friend gets %d ÷ %d = %d." % (a, k, each), s2="After eating: %d − %d = %d." % (each, c, each - c),
                wrong=[each, a - c, a - k * c, each + c],
                L="c", eq="%d ÷ %d − %d = c" % (a, k, c), eq_wrong=["%d − %d − %d = c" % (a, k, c), "%d ÷ %d + %d = c" % (a, k, c), "%d ÷ %d = c" % (a, k)])


def t_pages_add(r, P):
    n, he, his = P.next()
    k, each = r.randint(3, 7), r.randint(4, 9)
    a = k * each
    c = r.randint(2, 6)
    return dict(q="%s has %d stamps. %s puts the same number on each of %d pages. Then %s adds %d more stamps to every page. "
                  "How many stamps are on each page now?" % (n, a, cap(he), k, he, c),
                ans=each + c, unit="stamps", s1="Each page at first: %d ÷ %d = %d." % (a, k, each), s2="After adding: %d + %d = %d." % (each, c, each + c),
                wrong=[each, a + c, each + c * k, a // k * c],
                L="s", eq="%d ÷ %d + %d = s" % (a, k, c), eq_wrong=["%d + %d ÷ %d = s" % (a, c, k), "%d ÷ %d − %d = s" % (a, k, c), "%d × %d + %d = s" % (a, k, c)])


def t_teams(r, P):
    k = r.randint(3, 6)
    teams = r.randint(5, 9)
    a = k * teams
    c = r.randint(2, teams - 2)
    return dict(q="%d students are split into teams of %d. %d teams play soccer and the rest play basketball. "
                  "How many teams play basketball?" % (a, k, c),
                ans=teams - c, unit="teams", s1="Number of teams: %d ÷ %d = %d." % (a, k, teams), s2="Basketball teams: %d − %d = %d." % (teams, c, teams - c),
                wrong=[teams, a - c, a - k * c, teams + c],
                L="t", eq="%d ÷ %d − %d = t" % (a, k, c), eq_wrong=["%d − %d − %d = t" % (a, k, c), "%d ÷ %d = t" % (a, k), "%d ÷ %d + %d = t" % (a, k, c)])


def t_get_bag(r, P):
    n, he, his = P.next()
    k = r.randint(3, 8)
    total = k * r.randint(6, 9)
    b = r.randint(6, total - 10)
    a = total - b
    if a == b:
        a, b = a + 2, b - 2
    return dict(q="%s had %d marbles and got %d more. %s puts all the marbles into bags of %d. How many bags does %s fill?" % (n, a, b, cap(he), k, he),
                ans=total // k, unit="bags", s1="Marbles in all: %d + %d = %d." % (a, b, total), s2="Bags: %d ÷ %d = %d." % (total, k, total // k),
                wrong=[total, total // k + 1, total - k, total // k + 2],
                L="b", eq="(%d + %d) ÷ %d = b" % (a, b, k), eq_wrong=["%d + %d ÷ %d = b" % (a, b, k), "(%d + %d) × %d = b" % (a, b, k), "%d + %d − %d = b" % (a, b, k)])


def t_rotten(r, P):
    k = r.randint(3, 6)
    good = k * r.randint(4, 9)
    b = r.randint(3, 9)
    a = good + b
    return dict(q="A farmer picks %d apples. %d apples are bad and are thrown away. The rest are packed equally into %d baskets. "
                  "How many apples go in each basket?" % (a, b, k),
                ans=good // k, unit="apples", s1="Good apples: %d − %d = %d." % (a, b, good), s2="Each basket: %d ÷ %d = %d." % (good, k, good // k),
                wrong=[good, good // k + 1, good - k, good // k + b],
                L="a", eq="(%d − %d) ÷ %d = a" % (a, b, k), eq_wrong=["%d − %d ÷ %d = a" % (a, b, k), "(%d + %d) ÷ %d = a" % (a, b, k), "%d − %d = a" % (a, b)])


def t_rope(r, P):
    n, he, his = P.next()
    k, piece = r.randint(4, 8), r.randint(3, 9)
    a = k * piece
    c = r.randint(2, k - 1)
    return dict(q="A rope %d meters long is cut into %d equal pieces. %s uses %d of the pieces. How many meters of rope does %s use?" % (a, k, n, c, he),
                ans=piece * c, unit="m", s1="Each piece: %d ÷ %d = %d m." % (a, k, piece), s2="%d pieces: %d × %d = %d m." % (c, c, piece, piece * c),
                wrong=[piece, a - c, piece + c, a - piece],
                L="r", eq="%d ÷ %d × %d = r" % (a, k, c), eq_wrong=["%d ÷ %d + %d = r" % (a, k, c), "%d − %d = r" % (a, c), "%d ÷ %d = r" % (a, k)])


def t_fewer_both(r, P):
    a, b = r.randint(35, 80), r.randint(8, 25)
    t = a - b
    return dict(q="A red box has %d beads. A blue box has %d fewer beads than the red box. How many beads are in both boxes?" % (a, b),
                ans=a + t, unit="beads", s1="Blue box: %d − %d = %d." % (a, b, t), s2="Both boxes: %d + %d = %d." % (a, t, a + t),
                wrong=[t, a + b, a + a, a + t + 10],
                L="b", eq="%d + (%d − %d) = b" % (a, a, b), eq_wrong=["%d + %d = b" % (a, b), "%d − %d = b" % (a, b), "%d + %d + %d = b" % (a, a, b)])


def t_need_more(r, P):
    n, he, his = P.next()
    goal = r.choice([100, 150, 200])
    a, b = r.randint(25, 60), r.randint(15, 35)
    return dict(q="%s wants to collect %d trading cards. %s has %d cards and buys %d more. How many more cards does %s need?" % (n, goal, cap(he), a, b, he),
                ans=goal - a - b, unit="cards", s1="Cards now: %d + %d = %d." % (a, b, a + b), s2="Still needed: %d − %d = %d." % (goal, a + b, goal - a - b),
                wrong=[a + b, goal - a, goal - a + b, goal - b],
                L="c", eq="%d − (%d + %d) = c" % (goal, a, b), eq_wrong=["%d − %d + %d = c" % (goal, a, b), "%d + %d = c" % (a, b), "%d + %d + %d = c" % (goal, a, b)])


def t_parking(r, P):
    a, b, c = r.randint(60, 95), r.randint(12, 28), r.randint(9, 24)
    return dict(q="A parking lot had %d cars. In the morning, %d cars drove away. At lunch, %d more cars drove away. How many cars are in the lot now?" % (a, b, c),
                ans=a - b - c, unit="cars", s1="After the morning: %d − %d = %d." % (a, b, a - b), s2="After lunch: %d − %d = %d." % (a - b, c, a - b - c),
                wrong=[a - b, a - b + c, b + c, a - c],
                L="c", eq="%d − %d − %d = c" % (a, b, c), eq_wrong=["%d − %d + %d = c" % (a, b, c), "%d + %d + %d = c" % (a, b, c), "%d − %d = c" % (a, b)])


def t_tree(r, P):
    a, b, c = r.randint(40, 75), r.randint(6, 14), r.randint(5, 13)
    return dict(q="A young tree was %d inches tall. It grew %d inches in the spring and %d inches in the summer. How tall is the tree now?" % (a, b, c),
                ans=a + b + c, unit="inches", s1="After spring: %d + %d = %d." % (a, b, a + b), s2="After summer: %d + %d = %d." % (a + b, c, a + b + c),
                wrong=[a + b, b + c, a + b - c, a + c],
                L="h", eq="%d + %d + %d = h" % (a, b, c), eq_wrong=["%d + %d − %d = h" % (a, b, c), "%d + %d = h" % (a, b), "%d − %d − %d = h" % (a, b, c)])


def t_pay_two(r, P):
    n, he, his = P.next()
    k, m, c = r.randint(3, 8), r.randint(2, 6), r.randint(3, 9)
    t = k * m
    return dict(q="A notebook costs $%d. %s buys %d notebooks and one pen for $%d. How much does %s spend in all?" % (m, n, k, c, he),
                ans=t + c, unit="$", s1="Notebooks: %d × $%d = $%d." % (k, m, t), s2="Add the pen: $%d + $%d = $%d." % (t, c, t + c),
                wrong=[t, k + m + c, k * (m + c), t - c],
                L="s", eq="%d × %d + %d = s" % (k, m, c), eq_wrong=["%d + %d + %d = s" % (k, m, c), "%d × (%d + %d) = s" % (k, m, c), "%d × %d = s" % (k, m)])


def t_together_times(r, P):
    n, he, his = P.next()
    n2, he2, his2 = P.next()
    m, k = r.randint(4, 12), r.randint(2, 5)
    t = k * m
    return dict(q="%s has %d toy cars. %s has %d times as many toy cars as %s. How many toy cars do they have together?" % (n, m, n2, k, n),
                ans=m + t, unit="toy cars", s1="%s's cars: %d × %d = %d." % (n2, k, m, t), s2="Together: %d + %d = %d." % (m, t, m + t),
                wrong=[t, m + k, t - m, m * (k + 2)],
                L="t", eq="%d + %d × %d = t" % (m, k, m), eq_wrong=["%d + %d = t" % (m, k), "%d × %d = t" % (k, m), "%d × %d − %d = t" % (k, m, m)])


def t_pages_left(r, P):
    n, he, his = P.next()
    m, k = r.randint(5, 12), r.randint(3, 7)
    t = k * m
    total = t + r.randint(15, 60)
    return dict(q="%s's book has %d pages. %s reads %d pages every day for %d days. How many pages are left to read?" % (n, total, cap(he), m, k),
                ans=total - t, unit="pages", s1="Pages read: %d × %d = %d." % (k, m, t), s2="Pages left: %d − %d = %d." % (total, t, total - t),
                wrong=[t, total - m, total - k - m, total - t + 10],
                L="p", eq="%d − %d × %d = p" % (total, k, m), eq_wrong=["%d − %d − %d = p" % (total, k, m), "%d × %d = p" % (k, m), "%d + %d × %d = p" % (total, k, m)])


def t_empty_seats(r, P):
    k, m = r.randint(5, 10), r.choice([4, 6, 8])
    t = k * m
    c = r.randint(t // 3, t - 5)
    return dict(q="A restaurant has %d tables with %d seats at each table. %d people are eating there. How many seats are empty?" % (k, m, c),
                ans=t - c, unit="seats", s1="Seats in all: %d × %d = %d." % (k, m, t), s2="Empty seats: %d − %d = %d." % (t, c, t - c),
                wrong=[t, k + m + c if k + m + c != t - c else t + c, t + c, c - k if c - k > 1 else t + 10],
                L="e", eq="%d × %d − %d = e" % (k, m, c), eq_wrong=["%d + %d − %d = e" % (k, m, c), "%d × %d + %d = e" % (k, m, c), "%d × %d = e" % (k, m)])


def t_cost_each(r, P):
    k, each = r.randint(3, 6), r.randint(3, 9)
    a = k * each
    c = r.randint(k + 1, 9)
    return dict(q="%d toy trucks cost $%d. Each truck costs the same amount. How much do %d trucks cost?" % (k, a, c),
                ans=each * c, unit="$", s1="One truck: $%d ÷ %d = $%d." % (a, k, each), s2="%d trucks: %d × $%d = $%d." % (c, c, each, each * c),
                wrong=[each, a + c, a * c, each + c],
                L="t", eq="%d ÷ %d × %d = t" % (a, k, c), eq_wrong=["%d × %d = t" % (a, c), "%d ÷ %d + %d = t" % (a, k, c), "%d ÷ %d = t" % (a, k)])


def t_split_money(r, P):
    n, he, his = P.next()
    k, each = r.randint(3, 5), r.randint(6, 12)
    a = k * each
    c = r.randint(2, each - 2)
    return dict(q="%s and %d friends share $%d equally. Then %s spends $%d on a snack. How much money does %s have left?" % (n, k - 1, a, he, c, he),
                ans=each - c, unit="$", s1="%d people share the money: $%d ÷ %d = $%d each." % (k, a, k, each),
                s2="After the snack: $%d − $%d = $%d." % (each, c, each - c),
                wrong=[each, a - c, a // (k - 1) - c, each + c],
                L="m", eq="%d ÷ %d − %d = m" % (a, k, c), eq_wrong=["%d ÷ %d − %d = m" % (a, k - 1, c), "%d − %d = m" % (a, c), "%d ÷ %d = m" % (a, k)])


def t_walk(r, P):
    n, he, his = P.next()
    k, each = r.randint(3, 6), r.randint(2, 5)
    a = k * each
    c = r.randint(k + 1, 9)
    return dict(q="%s walks the same distance every day. In %d days, %s walks %d miles. How many miles does %s walk in %d days?" % (n, k, he, a, he, c),
                ans=each * c, unit="miles", s1="One day: %d ÷ %d = %d miles." % (a, k, each), s2="%d days: %d × %d = %d miles." % (c, c, each, each * c),
                wrong=[each, a + c, a + (c - k), each * (c - 1)],
                L="m", eq="%d ÷ %d × %d = m" % (a, k, c), eq_wrong=["%d + %d = m" % (a, c), "%d ÷ %d + %d = m" % (a, k, c), "%d × %d = m" % (a, c)])


def t_pizza(r, P):
    k = r.randint(2, 5)
    kids = r.choice([d for d in (2, 3, 4, 5, 6, 8) if (k * 8) % d == 0 and (k * 8) // d >= 2 and d != k])
    t = k * 8
    return dict(q="Each pizza is cut into 8 slices. %d pizzas are shared equally among %d children. How many slices does each child get?" % (k, kids),
                ans=t // kids, unit="slices", s1="Slices in all: %d × 8 = %d." % (k, t), s2="Each child: %d ÷ %d = %d." % (t, kids, t // kids),
                wrong=[t, 8 // kids if 8 // kids > 1 else t // kids + 2, k + 8, t // kids + 1],
                L="s", eq="%d × 8 ÷ %d = s" % (k, kids), eq_wrong=["%d × 8 = s" % k, "%d + 8 ÷ %d = s" % (k, kids), "8 ÷ %d = s" % kids])


ADD_SUB = [t_get_give, t_bus, t_bake, t_more_than, t_money_left, t_class, t_fewer_both, t_need_more, t_parking, t_tree]
MULT = [t_packs_give, t_rows_add, t_boxes_loose, t_change, t_save_spend, t_times_longer, t_pay_two, t_together_times, t_pages_left, t_empty_seats]
DIV = [t_share_eat, t_pages_add, t_teams, t_get_bag, t_rotten, t_rope, t_cost_each, t_split_money, t_walk, t_pizza]


def fmt(v, unit):
    return money(v) if unit == "$" else ("%d %s" % (v, unit) if unit else str(v))


def explain(d):
    return "Step 1: %s Step 2: %s So the answer is %s." % (d["s1"], d["s2"], fmt(d["ans"], d["unit"]))


def solve_item(d, rnd):
    cands = [fmt(v, d["unit"]) for v in d["wrong"] + [d["ans"] + 2, d["ans"] + 5, d["ans"] - 3] if v > 1]
    return mcq(d["q"], fmt(d["ans"], d["unit"]), cands, explain(d), rnd)


def make(templates, n, rnd, P):
    out = []
    order = (templates * ((n // len(templates)) + 1))[:n]
    rnd.shuffle(order)
    for t in order:
        out.append(t(rnd, P))
    return out


# ------------------------------------------------------------ sets
def set_solve(title, templates, rnd, P):
    return {"title": title, "items": [solve_item(d, rnd) for d in make(templates, 20, rnd, P)]}


def set_equation(rnd, P):
    its = []
    for d in make(rnd.sample(ADD_SUB + MULT + DIV, 20), 20, rnd, P):
        L = d["L"]
        stem = d["q"] + " Which equation can you use to find <b>%s</b>?" % L
        e = ("Step 1: %s Step 2: %s Put both steps together: %s, so %s = %s."
             % (d["s1"], d["s2"], d["eq"].split(" = ")[0], L, fmt(d["ans"], d["unit"])))
        its.append(mcq(stem, d["eq"], d["eq_wrong"], e, rnd))
    return {"title": "Write an equation with a letter", "items": its}


def round100(v):
    return int((v + 50) // 100 * 100)


def set_estimate(rnd, P):
    its = []
    # 5: estimate a 3-number problem
    for _ in range(5):
        a, b = rnd.randint(180, 480), rnd.randint(160, 450)
        c = rnd.randint(110, 290)
        while abs(a - round100(a)) < 15 or abs(b - round100(b)) < 15 or abs(c - round100(c)) < 15 or round100(a) + round100(b) - round100(c) <= 100 or abs(a + b - c - (round100(a) + round100(b) - round100(c))) > 50:
            a, b, c = rnd.randint(180, 480), rnd.randint(160, 450), rnd.randint(110, 290)
        ra, rb, rc = round100(a), round100(b), round100(c)
        est = ra + rb - rc
        story = ["A school collected %d cans of food in week 1 and %d cans in week 2. It gave %d cans to a food bank. "
                 "Round each number to the nearest hundred. About how many cans does the school have left?",
                 "A farm stand had %d apples. The farmer picked %d more. Then %d apples were sold. "
                 "Round each number to the nearest hundred. About how many apples are at the stand now?",
                 "A theater sold %d tickets on Friday and %d tickets on Saturday. %d people asked for their money back. "
                 "Round each number to the nearest hundred. About how many tickets were kept?"][_ % 3]
        its.append(mcq(story % (a, b, c),
                       "about %d" % est, ["about %d" % v for v in [ra + rb, ra + rb + rc, est + 100, est - 100]],
                       "%d → %d, %d → %d, %d → %d. Step 1: %d + %d = %d. Step 2: %d − %d = %d. The exact answer is %d, which is close to %d."
                       % (a, ra, b, rb, c, rc, ra, rb, ra + rb, ra + rb, rc, est, a + b - c, est), rnd))
    # 5: is this answer reasonable?
    for i in range(5):
        n, he, his = P.next()
        a, b = rnd.randint(210, 460), rnd.randint(150, 380)
        c = rnd.randint(120, 260)
        while abs(a - round100(a)) < 15 or abs(b - round100(b)) < 15 or abs(c - round100(c)) < 15 or round100(a) + round100(b) - round100(c) <= 100 or abs(a + b - c - (round100(a) + round100(b) - round100(c))) > 50:
            a, b, c = rnd.randint(210, 460), rnd.randint(150, 380), rnd.randint(120, 260)
        ra, rb, rc = round100(a), round100(b), round100(c)
        est, exact = ra + rb - rc, a + b - c
        claim = [exact, a + b + c, a + b, exact, a + b + c][i]
        ok = claim == exact
        good = "Yes, it is close to %d" % est if ok else "No, it should be close to %d" % est
        cands = ["No, it should be close to %d" % est, "Yes, it is close to %d" % est,
                 "No, it should be close to %d" % (ra + rb + rc), "Yes, it is close to %d" % round100(claim),
                 "No, it should be close to %d" % (ra + rb)]
        story = ["A library had %d books. It bought %d new books and gave away %d old books. %s says the library has %d books now. ",
                 "A zoo had %d visitors in the morning and %d in the afternoon. %d visitors left before the show. %s says %d visitors stayed for the show. ",
                 "A store had %d bottles of water. It got %d more bottles and sold %d bottles. %s says the store has %d bottles left. "][i % 3]
        its.append(mcq((story % (a, b, c, n, claim)) + "Use rounding to check. Is %s answer reasonable?" % his,
                       good, [x for x in cands if x != good],
                       "Estimate: %d + %d − %d = %d. %s answer, %d, %s. The exact answer is %d + %d − %d = %d."
                       % (ra, rb, rc, est, cap(his), claim, "is close to %d, so it is reasonable" % est if ok else
                          "is far from %d, so it is not reasonable" % est, a, b, c, exact), rnd))
    # 10: harder two-step problems with bigger numbers
    for d in make([t_need_more, t_tree, t_pages_left, t_empty_seats, t_together_times, t_split_money, t_pizza, t_walk, t_fewer_both, t_cost_each], 10, rnd, P):
        its.append(solve_item(d, rnd))
    rnd.shuffle(its)
    return {"title": "Estimate and check", "items": its}


# ------------------------------------------------------------ lesson
def tape_svg():
    """Bar model: 3 boxes of 8 crayons. The last box is split into 3 kept and 5 given away (8 = 3 + 5)."""
    cell, x0, y0 = 70, 20, 40
    give = cell * 5 // 8                              # 5 out of 8 of the last box
    gx = x0 + 3 * cell - give
    s = []
    for i in range(3):
        s.append("<rect x='%d' y='%d' width='%d' height='38' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x0 + i * cell, y0, cell, FILL, GREEN))
    s.append("<rect x='%d' y='%d' width='%d' height='38' fill='#f6d5d1' stroke='%s' stroke-width='2.5' stroke-dasharray='5 3'/>" % (gx, y0, give, RED))
    for x, t, col in [(x0 + cell // 2, "8", INK), (x0 + cell + cell // 2, "8", INK),
                      (x0 + 2 * cell + (cell - give) // 2, "3", INK), (gx + give // 2, "5", RED)]:
        s.append("<text x='%d' y='%d' font-size='18' font-weight='700' fill='%s' text-anchor='middle'>%s</text>" % (x, y0 + 26, col, t))
    s.append("<path d='M%d %d v-10 h%d v10' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 - 6, 3 * cell, INK))
    s.append("<text x='%d' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>3 × 8 = 24 crayons</text>" % (x0 + 1.5 * cell, y0 - 22, INK))
    s.append("<path d='M%d %d v10 h%d v-10' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y0 + 44, gx - x0, INK))
    s.append("<text x='%d' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>? left</text>" % (x0 + (gx - x0) // 2, y0 + 74, INK))
    s.append("<path d='M%d %d v10 h%d v-10' fill='none' stroke='%s' stroke-width='2'/>" % (gx, y0 + 44, give, RED))
    s.append("<text x='%d' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>5 given</text>" % (gx + give // 2, y0 + 74, RED))
    W, H = x0 * 2 + 3 * cell + 14, y0 + 86
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' role='img' "
            "aria-label='bar model: 3 groups of 8 with 5 taken away'>%s</svg>" % (W, H, W, H, "".join(s)))


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    return (
        "<h2>Find the hidden question</h2>"
        "<p>A two-step problem needs <b>two calculations</b>. The answer to the first step is not written in the story. "
        "You have to find it before you can answer the real question.</p>" +
        ex("Example", "Maya has 3 boxes of crayons with 8 crayons in each box. She gives 5 crayons to a friend. How many crayons does she have left?",
           "Hidden question: how many crayons does she have at first? 3 × 8 = 24. Real question: 24 − 5 = 19.", "19 crayons") +
        "<figure class='sn-fig'>" + tape_svg() +
        "<figcaption>A bar model shows both steps: first the whole (3 × 8 = 24), then the part taken away. 8 + 8 + 3 = 19 are left.</figcaption></figure>"
        "<h2>Choose the operation</h2>" +
        table(["The story says", "Usually means"], [
            ["in all, total, altogether, more join", "add"],
            ["left, fewer, how many more, gave away", "subtract"],
            ["each, rows of, packs of, times as many", "multiply"],
            ["shared equally, split into, groups of", "divide"],
        ]) +
        "<p>Key words help, but always picture what is happening. “How many more” compares two amounts, so you subtract.</p>"
        "<h2>Write an equation with a letter</h2>"
        "<p>Use a letter for the number you do not know. For Maya's crayons: <b>3 × 8 − 5 = c</b>. "
        "Do the multiplication first, then subtract: c = 19.</p>" +
        ex("Example", "Tickets cost $4 each. Leo buys 3 tickets and pays with a $20 bill. Which equation finds his change, c?",
           "Step 1: the tickets cost 3 × 4 = $12. Step 2: the change is 20 − 12 = $8.", "20 − 3 × 4 = c, so c = $8") +
        "<h2>Check that the answer makes sense</h2>"
        "<p>Round to the nearest ten or hundred and do the steps in your head. If your exact answer is far from the "
        "estimate, look for a mistake.</p>" +
        ex("Example", "A library has 412 books, buys 289 more and gives away 196. Is 505 a reasonable answer?",
           "Estimate: 400 + 300 − 200 = 500. 505 is close to 500.", "Yes, it is reasonable") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Stopping after the first step", "Read the question again: what does it ask for?"],
            ["Adding every number in the story", "Picture the story. Is something taken away or shared?"],
            ["Doing the steps in the wrong order", "Find the hidden number first, then use it"],
            ["Not checking the answer", "Estimate with rounded numbers"],
        ])
    )


FAQ = [
    {"q": "What is a two-step word problem?",
     "a": "It is a story problem that needs two calculations. First you find a number that is not given, then you use it to answer the question. For example: 3 boxes of 8 crayons, 5 given away. First 3 × 8 = 24, then 24 − 5 = 19."},
    {"q": "Why do Grade 3 students write equations with a letter?",
     "a": "The letter stands for the unknown answer. Writing 3 × 8 − 5 = c shows both steps in one line, which helps students plan before they calculate. This is part of standard 3.OA.D.8."},
    {"q": "How can my child check a two-step word problem?",
     "a": "Round the numbers, solve the problem in your head with the rounded numbers, and compare. If the exact answer is far from the estimate, something went wrong."},
    {"q": "What is the most common mistake in two-step problems?",
     "a": "Stopping after the first step. Children find the hidden number, such as 24 crayons, and give it as the answer. Always reread the question at the end."},
]


def gen_two_step():
    rnd = random.Random(39)
    P = People(rnd)
    sets = [set_solve("Add and subtract in two steps", ADD_SUB, rnd, P),
            set_solve("Multiply, then add or subtract", MULT, rnd, P),
            set_solve("Divide, then add, subtract or multiply", DIV, rnd, P),
            set_equation(rnd, P),
            set_estimate(rnd, P)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    return {
        "country": "us", "subject": "math", "grade": "grade-3", "slug": "two-step-word-problems", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Two-Step Word Problems",
        "seo_title": "Grade 3 Two-Step Word Problems Worksheets: All Four Operations, Equations with a Letter and Estimation",
        "short_title": "Two-step word problems",
        "domain": "Operations and Algebraic Thinking",
        "standard_code": "3.OA.D.8",
        "standard_url": "https://www.thecorestandards.org/Math/Content/3/OA/D/8/",
        "standard_text": "Solve two-step word problems using the four operations. Represent these problems using equations with a letter standing for the unknown quantity. Assess the reasonableness of answers using mental computation and estimation strategies including rounding.",
        "meta_desc": "Free Grade 3 two-step word problem worksheets: add, subtract, multiply and divide in two steps, write equations with a letter for the unknown, and check answers by estimating. 100 practice questions with step-by-step answers.",
        "key_big": "Find the hidden number first. Then answer the real question.",
        "key_sub": "Step 1 finds a number the story does not tell you. Step 2 uses it. Write both steps as one equation with a letter, and check with an estimate.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_two_step()
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
