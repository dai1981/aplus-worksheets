# -*- coding: utf-8 -*-
"""
BC Grade 6 Math: Budgeting and Consumer Math (BC Mathematics Curriculum, Financial literacy:
simple budgeting and consumer math)
  python3 tools/gen_cabc_math_g6_budgeting.py
Simple budgets (income and expenses), needs and wants, unit prices and best buys, discounts, saving goals and
word problems. No sales tax at this grade (BC adds GST and PST in the Grade 7 unit). All money is worked with
decimal.Decimal. Canada has no pennies: cash totals round to the nearest 5 cents, card payments are exact.
BC style: 4-digit numbers without a separator, $ and the cent sign.
Helpers are copied from gen_cabc_math_g7_financial_percentages.py and gen_caon_math_g6_financial.py.
HTML attributes use single quotes.
"""
import json, os, random, re
from decimal import Decimal as D
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
GREY = "#6b6259"
PAPER = "#fffdf5"
EDGE = "#b8b0a0"
LIGHT = "#d9eadf"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Ji-woo", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]
CENT = D("0.01")


# ------------------------------------------------------------ money
def money(d):
    d = D(d)
    assert 0 <= d < 10000, d
    return "$" + format(d.quantize(CENT), "f")


def cents_ok(x):
    return (F(str(x)) * 100).denominator == 1


def pct(p, r):
    """Exact r% of p (must be whole cents)."""
    x = D(p) * D(r) / 100
    assert x == x.quantize(CENT), (p, r)
    return x


def sale(p, r):
    return D(p) - pct(p, r)


def cash(d):
    c = int(D(d) * 100)
    assert D(c) / 100 == D(d)
    return D((c + 2) // 5 * 5) / 100


def cap(s):
    return s[0].upper() + s[1:]


def weeks(goal, per):
    q = F(str(D(goal))) / F(str(D(per)))
    return -(-q.numerator // q.denominator)


def wk(n):
    return "%d week%s" % (n, "" if n == 1 else "s")


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
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


def mq(q, correct, wrongs, e):
    correct = D(correct)
    w = [money(x) for x in wrongs if x is not None and D(x) > 0 and cents_ok(x) and D(x) != correct]
    return mcq(q, money(correct), w, e)


def balance(sets, rnd):
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
        self.pool = [(n, "she", "her", "her") for n in GIRLS] + [(n, "he", "his", "him") for n in BOYS]
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


def txt(x, y, t, fs=16, anchor="middle", bold=False, col=INK):
    return "<text x='%s' y='%s' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>" % (
        x, y, fs, " font-weight='700'" if bold else "", col, anchor, t)


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    u["body_html"] = rx.sub("<svg data-pf='lg' ", u["body_html"])
    return u


# ------------------------------------------------------------ pictures
def amt_txt(a):
    return "?" if a is None else money(a)


def budget_svg(title, sections):
    """A budget table. sections = [(heading, [(label, amount or None)])]; None prints “?”."""
    W, rh, fs = 300, 25, 16
    s = [txt(W // 2, 20, title, 17, bold=True)]
    y = 28
    top = y
    for head, rows in sections:
        s.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s'/>" % (y, W - 4, rh, GREEN))
        s.append(txt(12, y + 18, head, fs, "start", bold=True, col="#ffffff"))
        y += rh
        for label, amt in rows:
            s.append("<line x1='2' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (y + rh, W - 2, y + rh, EDGE))
            s.append(txt(12, y + 18, label, fs, "start"))
            s.append(txt(W - 12, y + 18, amt_txt(amt), fs, "end", bold=amt is None, col=GREEN if amt is None else INK))
            y += rh
    s.append("<rect x='2' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>" % (top, W - 4, y - top, EDGE))
    label = "Budget %s. " % title + ". ".join(
        "%s: %s" % (h, ", ".join("%s %s" % (a, amt_txt(b)) for a, b in rows)) for h, rows in sections)
    return svg_wrap(W, y + 4, "".join(s), label)


def tags_svg(tags):
    """Shelf tags side by side: tags = [(name, size, price)]."""
    tw, th, gap = 150, 110, 14
    s = []
    for i, (name, size, price) in enumerate(tags):
        x = 2 + i * (tw + gap)
        s.append("<rect x='%d' y='2' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>" % (x, tw, th, PAPER, EDGE))
        s.append("<path d='M%d 32 V10 a8 8 0 0 1 8 -8 H%d a8 8 0 0 1 8 8 V32 Z' fill='%s'/>" % (x, x + tw - 8, GREEN))
        s.append(txt(x + tw // 2, 24, name, 17, bold=True, col="#ffffff"))
        s.append(txt(x + tw // 2, 60, size, 18))
        s.append(txt(x + tw // 2, 98, money(price), 28, bold=True))
    W = 4 + len(tags) * tw + (len(tags) - 1) * gap
    label = "Shelf tags: " + "; ".join("%s, %s, %s" % (n, sz, money(p)) for n, sz, p in tags)
    return svg_wrap(W, th + 4, "".join(s), label)


def sale_tag_svg(price, off):
    """A sale tag: the regular price and the percent (or dollars) off."""
    W, H = 200, 110
    offt = ("%d%% OFF" % off) if isinstance(off, int) else (off + " OFF")
    s = [
        "<path d='M30 4 H192 a6 6 0 0 1 6 6 V100 a6 6 0 0 1 -6 6 H30 L4 55 Z' fill='%s' stroke='%s' stroke-width='2'/>" % (PAPER, RED),
        "<circle cx='26' cy='55' r='6' fill='#ffffff' stroke='%s' stroke-width='2'/>" % RED,
        txt(115, 34, "Regular " + money(price), 17),
        txt(115, 80, offt, 30, bold=True, col=RED),
    ]
    return svg_wrap(W + 2, H + 2, "".join(s), "Sale tag: regular price %s, %s" % (money(price), offt.lower()))


def goal_svg(saved, goal):
    """Savings goal bar: $0 to the goal, the saved part shaded."""
    W, L, R = 420, 30, 390
    y0, h = 34, 34
    x = L + (R - L) * float(F(str(D(saved))) / F(str(D(goal))))
    s = [
        "<rect x='%d' y='%d' width='%.1f' height='%d' fill='%s'/>" % (L, y0, x - L, h, LIGHT),
        "<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>" % (L, y0, R - L, h, GREEN),
        "<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y0 - 6, x, y0 + h + 6, GREEN),
        txt(L, y0 + h + 22, "$0", 15),
        txt("%.1f" % x, y0 - 10, "Saved " + money(saved), 15, bold=True, col=GREEN),
        txt(R, y0 + h + 22, "Goal " + money(goal), 15, anchor="end"),
    ]
    return svg_wrap(W, y0 + h + 30, "".join(s), "Savings goal bar: saved %s of a %s goal" % (money(saved), money(goal)))


# ============================================================ set 1: simple budgets
def set_budgets(P):
    its = []
    its.append(mcq("In a budget, what is income?", "Money you earn or are given",
                   ["Money you spend on things", "The price of an item", "Money you owe someone"],
                   "Income is <b>money coming in</b>: an allowance, pay for a job, or a gift of money. Money going out is an expense."))
    its.append(mcq("Which one is an expense?", "Buying a new soccer ball",
                   ["A weekly allowance", "Pay for walking a dog", "Birthday money from a grandparent"],
                   "An expense is <b>money going out</b>. Buying a soccer ball is an expense. The others are income: money coming in."))
    n, he, his, him = P.next()
    its.append(mq("%s gets a $20 allowance and earns $15 walking a neighbour’s dog each week. What is %s total income each week?" % (n, his),
                  D(35), [D(5), D(20), D(15)],
                  "Add all the money coming in: $20 + $15 = <b>$35</b>. ($5 subtracts instead of adding; $20 counts only the allowance.)"))
    n, he, his, him = P.next()
    its.append(mq("This week %s spends $12 on a movie, $6.50 on snacks and $8 on bus fare. What are %s total expenses?" % (n, his),
                  D("26.50"), [D(26), D("20.50"), D("14.50")],
                  "Add the money going out, lining up the decimal points: $12.00 + $6.50 + $8.00 = <b>$26.50</b>. "
                  "($26 drops the 50¢; $20.50 forgets the bus fare; $14.50 forgets the movie.)"))
    its.append(mcq("When is a budget balanced?", "When income equals expenses plus savings",
                   ["When expenses are more than income", "When you spend all your money on wants", "When income is more than $100"],
                   "A budget is balanced when <b>every dollar of income is planned for</b>: expenses + savings = income."))
    n, he, his, him = P.next()
    assert 4 * 15 == 60
    its.append(mq("%s earns $15 a week. How much does %s earn in 4 weeks?" % (n, he), D(60), [D(19), D(45), D(75)],
                  "4 × $15 = <b>$60</b>. ($19 adds 4 instead of multiplying; $45 is 3 weeks and $75 is 5 weeks.)"))
    n, he, his, him = P.next()
    sec = [("Income", [("Allowance", D(40)), ("Babysitting", D(36))]),
           ("Expenses and savings", [("Phone case", D(15)), ("Snacks", D(12)), ("Bus fare", D(10)), ("Savings", D(25))])]
    assert 76 - 62 == 14 and 76 - 37 == 39
    its.append(mq(fig(budget_svg("%s’s budget for October" % n, sec)) +
                  "Savings are part of the plan. How much money is not planned for yet?",
                  D(14), [D(39), D(138), D(62)],
                  "Income: $40 + $36 = $76. Planned: $15 + $12 + $10 + $25 = $62. $76 − $62 = <b>$14</b>. "
                  "($39 forgets to count the savings; $62 is the planned money, not what is left; $138 adds income and planned money.)"))
    n, he, his, him = P.next()
    assert D(14) * D("3.5") == 49
    its.append(mq("%s earns $14 an hour babysitting. On Saturday %s babysits for 3.5 hours. How much does %s earn?" % (n, he, he),
                  D(49), [D(42), D("17.50"), D(56)],
                  "$14 × 3.5: $14 × 3 = $42 and $14 × 0.5 = $7. $42 + $7 = <b>$49</b>. "
                  "($42 leaves out the half hour; $56 uses 4 hours; $17.50 adds instead of multiplying.)"))
    n, he, his, him = P.next()
    its.append(mcq("%s’s income is $60 this month. %s expenses are $72. What does this mean?" % (n, cap(his)),
                   "%s spends $12 more than %s has" % (cap(he), he),
                   ["%s has $12 left over" % cap(he), "%s spends $132 more than %s has" % (cap(he), he), "The budget is balanced"],
                   "Expenses are more than income: $72 − $60 = $12. %s is <b>$12 short</b> and must cut $12 of expenses or earn more." % cap(he)))
    n, he, his, him = P.next()
    sec = [("Income", [("Allowance", D(25)), ("Mowing lawns", D(45))]),
           ("Expenses and savings", [("Soccer cleats", D(32)), ("Snacks", D(9)), ("Savings", None)])]
    assert 70 - 32 - 9 == 29
    its.append(mq(fig(budget_svg("%s’s budget for May" % n, sec)) +
                  "%s wants this budget to be balanced. How much should go to savings?" % n,
                  D(29), [D(38), D(111), D(61)],
                  "Income: $25 + $45 = $70. Expenses: $32 + $9 = $41. Savings: $70 − $41 = <b>$29</b>. "
                  "($38 forgets the snacks; $61 forgets the cleats; $111 adds everything together.)"))
    n, he, his, him = P.next()
    assert 12 * 8 == 96
    its.append(mq("A music app costs $8 a month. How much does it cost for one year?", D(96), [D(80), D(104), D(416)],
                  "A year has 12 months. 12 × $8 = <b>$96</b>. ($80 uses 10 months; $104 uses 13 months; $416 uses 52, the number of weeks.)"))
    n, he, his, him = P.next()
    assert (60 - 45) * 6 == 90
    its.append(mq("%s’s income is $60 a month and %s expenses are $45 a month. %s saves the rest. How much does %s save in 6 months?"
                  % (n, his, cap(he), he),
                  D(90), [D(360), D(270), D(15)],
                  "Savings each month: $60 − $45 = $15. In 6 months: 6 × $15 = <b>$90</b>. "
                  "($360 is all the income; $270 is all the expenses; $15 is only one month.)"))
    n, he, his, him = P.next()
    assert D("2.45") * 8 == D("19.60")
    its.append(mq("A bus ride costs $2.45. %s takes 8 rides. How much does %s spend?" % (n, he),
                  D("19.60"), [D("16.45"), D("196.00"), D("1.96")],
                  "8 × $2.45 = 8 × $2 + 8 × $0.45 = $16 + $3.60 = <b>$19.60</b>. "
                  "($16.45 multiplies only the dollars; $196.00 and $1.96 put the decimal point in the wrong place.)"))
    n, he, his, him = P.next()
    sec = [("Income", [("Allowance", D(50))]),
           ("Expenses and savings", [("Hockey stick", D(30)), ("Snacks", D(15)), ("Savings", D(15))])]
    its.append(mcq(fig(budget_svg("%s’s budget for March" % n, sec)) +
                   "This budget plans $10 more than the income. Which change balances it?",
                   "Spend $10 less on snacks", ["Save $10 more", "Spend $10 more on the stick", "Earn $10 less"],
                   "Planned: $30 + $15 + $15 = $60, but income is $50. To balance, plan $10 less: "
                   "<b>spend $10 less on snacks</b> (now $5). Saving more or earning less makes the gap bigger."))
    n, he, his, him = P.next()
    assert pct(150, 60) == 90
    its.append(mq("%s earns $150 at a summer job and spends 40%% of it. How much is left?" % n,
                  D(90), [D(60), D(110), D(210)],
                  "If 40% is spent, 60% is left. 10% of $150 is $15, so 60% is 6 × $15 = <b>$90</b>. "
                  "($60 is the 40% spent; $110 subtracts 40 dollars, not 40%; $210 adds 40% instead of taking it away.)"))
    n, he, his, him = P.next()
    assert 12 * 5 == 60 and 70 - 60 == 10
    its.append(mcq("Job A pays $12 an hour for 5 hours. Job B pays $70 for the same afternoon. Which pays more?",
                   "Job B, by $10", ["Job A, by $10", "Job B, by $58", "They pay the same"],
                   "Job A: 5 × $12 = $60. Job B: $70. $70 − $60 = $10, so <b>Job B pays $10 more</b>. "
                   "($58 compares $70 with $12, the pay for one hour.)"))
    n, he, his, him = P.next()
    assert pct(120, 20) == 24
    its.append(mq("%s’s monthly income is $120. %s plans to save 20%% of it. How much will %s save each month?" % (n, cap(he), he),
                  D(24), [D(20), D(96), D(6)],
                  "10% of $120 is $12, so 20% is 2 × $12 = <b>$24</b>. ($20 uses the percent as dollars; $6 divides by 20; $96 is the 80% left to spend.)"))
    n, he, his, him = P.next()
    sec = [("Income", [("Allowance", D(45)), ("Bottle returns", D(15))]),
           ("Expenses and savings", [("Snacks", D(18)), ("Swim pass", D(27)), ("Savings", D(15))])]
    assert F(15, 60) == F(1, 4)
    its.append(mcq(fig(budget_svg("%s’s budget for June" % n, sec)) +
                   "What percent of %s’s income goes to savings?" % n,
                   "25%", ["15%", "33%", "75%"],
                   "Income: $45 + $15 = $60. Savings: $15. $15 out of $60 = 1/4 = <b>25%</b>. "
                   "(15% uses the dollars as the percent; 33% compares savings with expenses, $15 out of $45; 75% is the rest.)"))
    n, he, his, him = P.next()
    assert (20 - D("12.50")) * 4 == 30
    its.append(mq("%s earns $20 a week and spends $12.50 a week. %s saves the rest. How much has %s saved after 4 weeks?"
                  % (n, cap(he), he),
                  D(30), [D(80), D(50), D("7.50")],
                  "Saved each week: $20.00 − $12.50 = $7.50. After 4 weeks: 4 × $7.50 = <b>$30</b>. "
                  "($80 is all the income; $50 is what she spends; $7.50 is only one week.)"))
    n, he, his, him = P.next()
    assert 3 * 18 + 2 * 25 == 104 and 104 - 80 == 24
    its.append(mq("In April %s earns $18 for each of 3 car washes and $25 for each of 2 yard clean-ups. %s spends $80 on new runners. "
                  "How much is left?" % (n, cap(he)),
                  D(24), [D(104), D(31), D(184)],
                  "Income: 3 × $18 + 2 × $25 = $54 + $50 = $104. Left: $104 − $80 = <b>$24</b>. "
                  "($104 forgets the runners; $31 mixes up the counts, 3 × $25 + 2 × $18; $184 adds the $80.)"))
    assert 3 * 25 + 2 * 18 - 80 == 31
    assert len(its) == 20
    return {"title": "Simple budgets: income and expenses", "items": its}


# ============================================================ set 2: needs and wants
def set_needs(P):
    its = []
    its.append(mcq("What is a need?", "Something you must have to live safely and be healthy",
                   ["Something nice that you can live without", "Anything that costs more than $50", "Anything your friends have"],
                   "A need is <b>something you must have to be safe and healthy</b>, like food, water, a home and warm clothes. "
                   "A want is nice to have, but you can live without it."))
    its.append(mcq("Which one is a need?", "Healthy food for meals", ["A new video game", "A concert ticket", "A bag of candy"],
                   "You must eat to stay healthy, so <b>healthy food for meals</b> is a need. The others are wants."))
    its.append(mcq("Which one is a want?", "A phone case with a cool design", ["Clean drinking water", "A warm winter coat", "A place to live"],
                   "You can live without a fancy phone case, so <b>it is a want</b>. Water, warm clothes and a home are needs."))
    its.append(mcq("It rains a lot in Vancouver in the fall. A student walks to school every day. Which one is a need?",
                   "A rain jacket that fits", ["A game console", "Movie tickets", "A second backpack"],
                   "Staying dry and warm keeps you healthy, so <b>a rain jacket that fits</b> is a need. The others are wants."))
    its.append(mcq("Which one is a need for a family?", "Heat and electricity for the home",
                   ["A streaming service", "A holiday trip", "A new boat"],
                   "A home must be warm and safe, so <b>heat and electricity</b> are needs. The others are wants."))
    its.append(mcq("Why can shoes be a need or a want?", "One pair that fits is a need; an extra fancy pair is a want",
                   ["Shoes are always a want", "Shoes are a need only if they are expensive", "Shoes are never in a budget"],
                   "You need <b>shoes that fit</b> to walk safely. A second, fancy pair is nice but not needed, so it is a want."))
    its.append(mcq("In a grocery cart there is milk, bread, apples and a chocolate bar. Which one is a want?", "The chocolate bar",
                   ["The milk", "The bread", "The apples"],
                   "Milk, bread and apples are healthy foods for meals: needs. <b>The chocolate bar</b> is a treat: a want."))
    its.append(mcq("Money is tight this month. What is the best order to plan spending?", "Needs first, then wants if money is left",
                   ["Wants first, then needs", "The most expensive thing first", "Whatever you see first in the store"],
                   "Pay for <b>needs first</b> so you are safe and healthy. Use any money left over for savings and wants."))
    lst = [("Groceries", D(85)), ("Winter boots", D(60)), ("Video game", D(70)), ("Movie night", D(25))]
    assert 85 + 60 == 145 and 85 + 60 + 70 + 25 == 240 and 85 + 70 == 155
    its.append(mq("A family’s list: groceries $85, winter boots $60, a video game $70 and a movie night $25. How much is for needs?",
                  D(145), [D(95), D(240), D(215)],
                  "Needs: groceries and winter boots. $85 + $60 = <b>$145</b>. ($95 is the wants; $240 is everything; "
                  "$215 counts the video game as a need.)"))
    assert 85 + 60 + 70 == 215
    n, he, his, him = P.next()
    sec = [("Needs", [("School supplies", D(24)), ("Gym shoes", D(38))]),
           ("Wants", [("Skateboard wheels", D(29)), ("Comic books", D(16))])]
    assert 24 + 38 == 62 and 29 + 16 == 45 and 62 - 45 == 17
    its.append(mq(fig(budget_svg("%s’s spending plan" % n, sec)) +
                  "How much more is planned for needs than for wants?",
                  D(17), [D(107), D(45), D(9)],
                  "Needs: $24 + $38 = $62. Wants: $29 + $16 = $45. $62 − $45 = <b>$17</b>. "
                  "($107 adds the two totals; $45 is only the wants; $9 compares only gym shoes and skateboard wheels.)"))
    assert 38 - 29 == 9
    n, he, his, him = P.next()
    assert 50 - 32 == 18
    its.append(mq("%s has $50. %s needs $32 for a bus pass and lunches this week. How much is left for wants and savings?" % (n, cap(he)),
                  D(18), [D(82), D(22), D(32)],
                  "Pay the needs first: $50 − $32 = <b>$18</b> left. ($32 is the needs; $82 adds instead of subtracting; "
                  "$22 takes 0 − 2 as 2 instead of regrouping.)"))
    n, he, his, him = P.next()
    its.append(mcq("%s has $20. %s can buy a book or go to a movie, but not both. %s buys the book. What does %s give up?"
                   % (n, cap(he), cap(he), he),
                   "The movie", ["The book", "Nothing", "Both the book and the movie"],
                   "When you choose one thing, you give up the other. This is a <b>trade-off</b>. Buying the book means "
                   "%s gives up <b>the movie</b>." % he))
    assert F(240, 400) == F(3, 5)
    its.append(mcq("A family’s weekly budget is $400. They spend $240 on needs. What percent of the budget is needs?",
                   "60%", ["40%", "24%", "167%"],
                   "$240 out of $400 = 240/400 = 60/100 = <b>60%</b>. (40% is the rest; 24% comes from the dollars, 240; "
                   "167% divides the wrong way, 400 ÷ 240.)"))
    n, he, his, him = P.next()
    assert D("14.50") + D("22.75") == D("37.25") and D("14.50") + 28 == D("42.50")
    assert D("22.75") + 28 == D("50.75") and 28 + D("19.99") == D("47.99")
    its.append(mcq("%s has $40 for wants. Which two things can %s buy without going over $40?" % (n, he),
                   "Book $14.50 and puzzle $22.75",
                   ["Book $14.50 and cap $28.00", "Puzzle $22.75 and cap $28.00", "Cap $28.00 and earbuds $19.99"],
                   "Book + puzzle = $14.50 + $22.75 = <b>$37.25</b>, which is under $40. The other pairs cost $42.50, $50.75 and $47.99."))
    n, he, his, him = P.next()
    assert 90 + 70 == 160
    its.append(mcq("After paying for needs, a family has $150 left. They want a $90 bike and a $70 tablet case. Can they buy both?",
                   "No, they are $10 short", ["Yes, with $10 left", "No, they are $160 short", "Yes, with $60 left"],
                   "$90 + $70 = $160, which is more than $150. $160 − $150 = $10, so <b>they are $10 short</b>. "
                   "(“$60 left” counts only the bike.)"))
    n, he, his, him = P.next()
    assert pct(80, 45) == 36
    its.append(mq("%s’s family has $80 for the week. 55%% goes to needs. How much is left for wants and savings?" % n,
                  D(36), [D(44), D(25), D(45)],
                  "If 55% is needs, 100% − 55% = 45% is left. 10% of $80 is $8, so 40% is $32 and 5% is $4. "
                  "45% = <b>$36</b>. ($44 is the needs; $45 uses the percent as dollars; $25 subtracts 55 from 80.)"))
    n, he, his, him = P.next()
    assert 60 - 30 - 18 == 12
    its.append(mq("%s gets $60 for %s birthday. %s puts 50%% into savings and spends $18 on school supplies (a need). "
                  "%s spends the rest on a want. How much is that?" % (n, his, cap(he), cap(he)),
                  D(12), [D(42), D(30), D(48)],
                  "Savings: 50% of $60 = $30. Left: $60 − $30 − $18 = <b>$12</b>. "
                  "($30 is the savings; $42 forgets the savings; $48 forgets the school supplies.)"))
    assert F(2400, 3200) == F(3, 4)
    its.append(mcq("A family earns $3200 a month. They spend $2400 on needs such as rent, food and heat. What percent is that?",
                   "75%", ["25%", "24%", "133%"],
                   "2400/3200 = 24/32 = 3/4 = <b>75%</b>. (25% is the part left; 24% comes from the dollars, 2400; "
                   "133% divides the wrong way: 3200 ÷ 2400.)"))
    n, he, his, him = P.next()
    assert 4 * 12 == 48 and 70 - 48 == 22
    its.append(mq("%s has $70. %s needs 4 lunches at $12 each for a school camp. %s wants a $25 hoodie. "
                  "After the lunches, how much more money does %s need for the hoodie?" % (n, cap(he), cap(he), he),
                  D(3), [D(22), D(45), D(13)],
                  "Lunches (needs): 4 × $12 = $48. Left: $70 − $48 = $22. The hoodie costs $25, so %s needs "
                  "$25 − $22 = <b>$3</b> more. ($22 is the money left; $45 subtracts only the hoodie; "
                  "$13 takes away only one lunch.)" % he))
    n, he, his, him = P.next()
    its.append(mcq("%s is saving for new hockey skates because %s old skates are too small and %s plays on a team. "
                   "%s also wants a new video game. Which should %s buy first?" % (n, his, he, cap(he), he),
                   "The skates", ["The video game", "Both, even if there is not enough money", "Whichever costs less"],
                   "Skates that fit are needed to play safely on the team, so they come first. "
                   "<b>The skates</b> are the need here; the game is a want."))
    assert len(its) == 20
    return {"title": "Needs and wants", "items": its}


# ============================================================ set 3: unit prices and best buys
def unit_item(q, price, amount, base, per, figure=None, note=""):
    """Unit price for `base` when `amount` costs `price` (amount and base in the same unit)."""
    price = D(price)
    k = F(amount) / F(base)
    u = F(str(price)) / k
    assert (u * 100).denominator == 1, (price, amount, base)
    ans = D(u.numerator) / D(u.denominator)
    kt = str(k.numerator) if k.denominator == 1 else format(D(k.numerator) / D(k.denominator), "f")
    if k.denominator == 1:
        e = "There are %s groups of %s in %s, so divide: " % (kt, per[0], per[1])
    else:
        e = "%s = %s × %s, so divide: " % (per[1], kt, per[0])
    e += ("%s ÷ %s = <b>%s %s</b>. Check: %s × %s = %s."
          % (money(price), kt, money(ans), per[2], money(ans), kt, money(price)))
    if note:
        e += " " + note
    e += " (Multiplying instead of dividing gives %s.)" % money(price * D(k.numerator) / D(k.denominator))
    wr = []
    for w in [F(str(price)) * k, F(str(price)) / (k * 10), F(str(price)) * 10 / k,
              F(str(price)) - k if k.denominator == 1 else None, F(str(price))]:
        if w is not None and w > 0 and (w * 100).denominator == 1:
            wr.append(D(w.numerator) / D(w.denominator))
    if figure:
        q = fig(figure) + q
    return mq(q, ans, wr, e)


def best_item(q, opts, unit_txt, base, figure=False, cant=None, note=""):
    """opts = [(label, amount, amount_text, price)]; lowest price per base wins."""
    us = []
    parts = []
    for lab, amt, at, pr in opts:
        u = F(str(D(pr))) * base / F(amt)
        assert (u * 100).denominator == 1, (lab, amt, pr)
        k = F(amt) / base
        kt = str(k.numerator) if k.denominator == 1 else format(D(k.numerator) / D(k.denominator), "f")
        us.append((u, lab, pr))
        parts.append("%s: %s ÷ %s = %s %s" % (lab, money(pr), kt, money(D(u.numerator) / D(u.denominator)), unit_txt))
    srt = sorted(us)
    assert srt[0][0] < srt[1][0]
    ans = srt[0][1]
    e = "Compare the price " + unit_txt + ", not the total price. " + "; ".join(parts) + ". "
    e += ("<b>%s</b> has the lower price %s, so it is the better buy." if len(opts) == 2 else
          "<b>%s</b> has the lowest price %s, so it is the best buy.") % (ans, unit_txt)
    cheapest_total = min(us, key=lambda t: D(t[2]))[1]
    if cheapest_total != ans:
        e += " (%s has the lowest total, but you get less.)" % cheapest_total
    if note:
        e += " " + note
    choices = [lab for lab, a, at, p in opts]
    if len(opts) == 2:
        choices += ["Both cost the same " + unit_txt, cant or "You cannot compare different sizes"]
    else:
        choices += ["They all cost the same " + unit_txt]
    if figure:
        q = fig(tags_svg([(lab, at, pr) for lab, a, at, pr in opts])) + q
    return mcq(q, ans, [c for c in choices if c != ans], e)


def set_unit(P):
    its = []
    its.append(mcq("A shelf tag says “$0.60 per 100 g”. What does this unit price tell you?",
                   "The cost of 100 g of the food", ["The cost of the whole package", "How many grams are in the package",
                                                     "How many grams $1 buys"],
                   "A unit price is the price for one unit of an item, here <b>100 g</b>. It lets you compare packages of "
                   "different sizes fairly."))
    its.append(unit_item("A 500 g bag of pasta costs $2.50. What is the price per 100 g?", "2.50", 500, 100,
                         ("100 g", "500 g", "per 100 g")))
    its.append(unit_item("A 2 L carton of milk costs $4.30. What is the price per litre?", "4.30", 2, 1,
                         ("1 L", "2 L", "per litre")))
    its.append(unit_item("A carton of 12 eggs costs $5.40. What is the price per egg?", "5.40", 12, 1,
                         ("1 egg", "12 eggs", "per egg")))
    its.append(unit_item("A 400 g box of BC blueberries costs $5.20. What is the price per 100 g?", "5.20", 400, 100,
                         ("100 g", "400 g", "per 100 g")))
    its.append(unit_item("A 2 kg bag of Okanagan apples costs $6.40. What is the price per 100 g?", "6.40", 2000, 100,
                         ("100 g", "2 kg (2000 g)", "per 100 g"),
                         note="Remember 1 kg = 1000 g. ($3.20 is the price per kilogram, not per 100 g.)"))
    its.append(mcq("Two boxes of crackers are different sizes. What should you compare to find the better buy?",
                   "The price for the same amount, such as per 100 g", ["The total prices", "The sizes of the boxes",
                                                                       "The pictures on the boxes"],
                   "A bigger box usually costs more in total, so totals do not tell you which is cheaper. Compare "
                   "<b>the price for the same amount</b>: the unit price."))
    its.append(best_item("Which box of cereal is the better buy?",
                         [("Box A", 400, "400 g", "5.20"), ("Box B", 750, "750 g", "8.25")], "per 100 g", 100, figure=True))
    its.append(best_item("Which box of crackers is the better buy?",
                         [("Box A", 200, "200 g", "2.40"), ("Box B", 300, "300 g", "3.90")], "per 100 g", 100, figure=True,
                         note="A bigger box is not always the better buy."))
    its.append(best_item("Which jug of apple juice is the better buy?",
                         [("Jug A", 1, "1 L", "2.60"), ("Jug B", 2, "2 L", "4.80")], "per litre", 1, figure=True))
    n, he, his, him = P.next()
    assert F(350) / 5 == 70 and F(600) / 10 == 60
    its.append(mcq("A 500 g jar of peanut butter costs $3.50. A 1 kg jar costs $6.00. %s says the 500 g jar is the better buy "
                   "because it costs less. Is %s right?" % (n, he),
                   "No, the 1 kg jar costs less per 100 g", ["Yes, it costs less in total", "Yes, small jars always cost less per 100 g",
                                                            "No, the two jars cost the same per 100 g"],
                   "Compare unit prices, not totals. 500 g jar: $3.50 ÷ 5 = $0.70 per 100 g. 1 kg jar: $6.00 ÷ 10 = $0.60 per 100 g. "
                   "<b>The 1 kg jar costs less per 100 g</b>, so it is the better buy (if you will use it all)."))
    its.append(best_item("A box of 6 granola bars costs $3.30. A box of 10 granola bars costs $5.00. Which is the better buy?",
                         [("The box of 6", 6, "6 bars", "3.30"), ("The box of 10", 10, "10 bars", "5.00")], "per bar", 1,
                         cant="You cannot compare different boxes"))
    its.append(unit_item("A 1.5 kg bag of carrots costs $3.45. What is the price per kilogram?", "3.45", F(3, 2), 1,
                         ("1 kg", "1.5 kg", "per kilogram")))
    its.append(unit_item("A 250 g pack of smoked salmon costs $9.50. What is the price per 100 g?", "9.50", 250, 100,
                         ("100 g", "250 g", "per 100 g")))
    its.append(unit_item("An 800 g bag of cherries costs $6.40. What is the price per kilogram?", "6.40", 800, 1000,
                         ("1 kg", "800 g", "per kilogram"), note="800 g is less than 1 kg, so 1 kg costs more than $6.40."))
    its.append(best_item("Which bag of rice is the best buy?",
                         [("Bag A", 1, "1 kg", "3.20"), ("Bag B", 2, "2 kg", "6.00"), ("Bag C", 5, "5 kg", "16.00")],
                         "per kilogram", 1, figure=True))
    its.append(best_item("A 650 g tub of yogurt costs $3.90. A pack of 4 yogurt cups, 100 g each, costs $2.80. Which is the better buy?",
                         [("The tub", 650, "650 g", "3.90"), ("The 4 cups", 400, "400 g", "2.80")], "per 100 g", 100))
    assert D("4.40") * D("2.5") == 11
    its.append(mq("Grapes cost $4.40 per kilogram. How much do 2.5 kg cost?", D(11), [D("8.80"), D("6.90"), D("1.76")],
                  "Multiply the unit price by the amount: $4.40 × 2.5 = $8.80 + $2.20 = <b>$11.00</b>. "
                  "($8.80 is only 2 kg; $6.90 adds 4.40 + 2.5; $1.76 divides.)"))
    assert 5 * D("1.75") == D("8.75") and D("7.50") / 5 == D("1.50")
    its.append(mq("One notebook costs $1.75. A pack of 5 notebooks costs $7.50. How much do you save on each notebook by buying the pack?",
                  D("0.25"), [D("1.25"), D("1.50"), D("5.75")],
                  "Pack price per notebook: $7.50 ÷ 5 = $1.50. Saving on each: $1.75 − $1.50 = <b>$0.25</b> (25¢). "
                  "($1.25 is the saving on all 5; $1.50 is the pack’s unit price.)"))
    its.append(best_item("A 400 mL bottle of shampoo costs $5.60. A 1 L bottle costs $12.00. Which is the better buy?",
                         [("The 400 mL bottle", 400, "400 mL", "5.60"), ("The 1 L bottle", 1000, "1 L", "12.00")], "per 100 mL", 100,
                         cant="You cannot compare mL and L"))
    assert len(its) == 20
    return {"title": "Unit prices and best buys", "items": its}


# ============================================================ set 4: discounts
def set_discount(P):
    its = []
    its.append(mq(fig(sale_tag_svg(40, 10)) + "A $40 hoodie is 10% off. How much is the discount?",
                  D(4), [D(30), D(36), D("0.40")],
                  "10% is one tenth. $40 ÷ 10 = <b>$4</b> off. ($36 is the sale price, not the discount; $30 subtracts 10 dollars; $0.40 is 1%.)"))
    its.append(mq("A $40 hoodie is 10% off. What is the sale price?", sale(40, 10), [D(30), D(4), D(44)],
                  "Discount: 10% of $40 = $4. Sale price: $40 − $4 = <b>$36</b>. ($30 subtracts 10 dollars, not 10%; $44 adds the discount.)"))
    its.append(mq(fig(sale_tag_svg(60, 25)) + "What is the sale price of this rain jacket?", sale(60, 25), [D(35), D(15), D(75)],
                  "Discount: 25% of $60 = $60 ÷ 4 = $15. Sale price: $60 − $15 = <b>$45</b>. "
                  "($35 subtracts 25 dollars instead of 25%; $15 is the discount; $75 adds the discount.)"))
    its.append(mq("A pair of $80 hiking boots is 50% off. What is the sale price?", sale(80, 50), [D(30), D(120), D("79.50")],
                  "50% off is half off. $80 ÷ 2 = <b>$40</b>. ($30 subtracts 50 dollars; $79.50 subtracts 50¢; $120 adds 50%.)"))
    its.append(mq(fig(sale_tag_svg(50, "$15")) + "What is the sale price of this backpack?", D(35), [D("42.50"), D(15), D(65)],
                  "This tag takes off dollars, not a percent. $50 − $15 = <b>$35</b>. "
                  "($42.50 takes off 15%; $65 adds the $15.)"))
    its.append(mq("A $35 board game is 20% off. What is the sale price?", sale(35, 20), [D(15), D(7), D(42)],
                  "Discount: 10% is $3.50, so 20% is $7. Sale price: $35 − $7 = <b>$28</b>. ($15 is 35 − 20; $7 is the discount; $42 adds the discount.)"))
    its.append(mcq("An item is 30% off. Which calculation gives the sale price?", "Find 70% of the price",
                   ["Find 30% of the price", "Subtract $30 from the price", "Find 130% of the price"],
                   "30% off means you pay 100% − 30% = 70% of the price, so <b>find 70% of the price</b>. "
                   "30% of the price is only the discount."))
    its.append(mq(fig(sale_tag_svg(150, 30)) + "What is the sale price of these skis?", sale(150, 30), [D(120), D(45), D(195)],
                  "Discount: 10% of $150 is $15, so 30% is $45. Sale price: $150 − $45 = <b>$105</b>. "
                  "($120 subtracts 30 dollars; $45 is the discount; $195 adds the discount.)"))
    its.append(mq("A $48 soccer ball is 25% off. What is the sale price?", sale(48, 25), [D(23), D(12), D(60)],
                  "Discount: 25% of $48 = $48 ÷ 4 = $12. Sale price: $48 − $12 = <b>$36</b>. ($23 is 48 − 25; $12 is the discount; $60 adds the discount.)"))
    its.append(mq("A $75 tent is 40% off. What is the sale price?", sale(75, 40), [D(35), D(30), D(105)],
                  "You pay 60%. 10% of $75 is $7.50, so 60% is 6 × $7.50 = <b>$45</b>. ($35 is 75 − 40; $30 is the discount; $105 adds the discount.)"))
    its.append(mcq("A pair of $80 skates is on sale for $60. What percent is the discount?", "25%", ["20%", "75%", "33%"],
                   "Discount: $80 − $60 = $20. Compare it with the <b>regular</b> price: $20 out of $80 = 1/4 = <b>25%</b>. "
                   "(20% uses the dollars; 75% is the part you pay; 33% compares $20 with the sale price, $60.)"))
    assert pct(90, 20) == 18
    its.append(mcq("A $90 jacket can be bought at 20% off or with a $20-off coupon. Which deal saves more?",
                   "$20 off, by $2", ["20% off, by $2", "They save the same", "20% off, by $18"],
                   "20% of $90 = $18 off. The coupon is $20 off. $20 − $18 = $2, so <b>the $20-off coupon saves $2 more</b>. "
                   "(“They save the same” mixes up 20% and $20; $18 is the 20% discount, not the difference.)"))
    its.append(mq("A $32 T-shirt is on clearance for 75% off. What is the clearance price?", sale(32, 75), [D(24), D(16), D("31.25")],
                  "25% of $32 is $8, so 75% off is $24 off. You pay 25%: <b>$8</b>. ($24 is the discount; $16 is only 50% off; $31.25 takes off 75¢, not 75%.)"))
    assert 24 + 12 == 36
    its.append(mq("A bookstore deal: buy one book, get the second one 50% off. Two books cost $24 each. How much do the two books cost?",
                  D(36), [D(24), D(48), D(12)],
                  "First book: $24. Second book: 50% of $24 off, so $12. Total: $24 + $12 = <b>$36</b>. "
                  "($48 forgets the discount; $24 makes the second book free.)"))
    assert 2 * D("4.50") == 9 and D(9) / 3 == 3
    n, he, his, him = P.next()
    its.append(mq("A store has “buy 2, get 1 free” on juice packs that cost $4.50 each. %s takes 3 packs. "
                  "What does %s pay for each pack?" % (n, he),
                  D(3), [D("4.50"), D("1.50"), D("13.50")],
                  "%s pays for 2 packs: 2 × $4.50 = $9.00. That buys 3 packs: $9.00 ÷ 3 = <b>$3.00 per pack</b>. "
                  "($4.50 forgets the free pack; $1.50 divides one price by 3; $13.50 is 3 packs with no deal.)" % cap(he)))
    assert sale(60, 15) == 51 and sale(56, 10) == D("50.40")
    its.append(mcq("Store A sells a hockey stick for $60 at 15% off. Store B sells the same stick for $56 at 10% off. Which is cheaper?",
                   "Store B: $50.40", ["Store A: $51.00", "Store A: $45.00", "Store B: $46.00"],
                   "Store A: 15% of $60 is $9, so $60 − $9 = $51.00. Store B: 10% of $56 is $5.60, so $56 − $5.60 = $50.40. "
                   "<b>Store B is cheaper, at $50.40</b>. ($45.00 and $46.00 subtract the percent numbers as dollars.)"))
    n, he, his, him = P.next()
    assert sale(64, 25) == 48
    its.append(mq("%s has $50. A $64 hoodie is 25%% off. How much money does %s have left after buying it?" % (n, he),
                  D(2), [D(11), D(34), D(16)],
                  "Sale price: 25% of $64 is $16, so $64 − $16 = $48. Left: $50 − $48 = <b>$2</b>. "
                  "($16 is the discount; $11 uses $64 − 25 = $39; $34 subtracts only the discount from $50.)"))
    assert sale(50, 20) == 40
    its.append(mq("A bike helmet is 20% off. The sale price is $40. What was the regular price?",
                  D(50), [D(48), D(32), D(60)],
                  "The sale price is 80% of the regular price. 80% is $40, so 10% is $5 and 100% is <b>$50</b>. "
                  "Check: 20% of $50 is $10 and $50 − $10 = $40. ($48 adds 20% of $40 instead; $60 adds 20 dollars; $32 takes 20% off again.)"))
    n, he, his, him = P.next()
    assert 46 + 5 - 10 == 41
    its.append(mcq("A store gives $10 off when you spend $50 or more. %s’s items cost $46. If %s adds a $5 pair of socks, "
                   "what happens?" % (n, he),
                   "%s pays $41, which is $5 less" % cap(he),
                   ["%s pays $51, which is $5 more" % cap(he), "%s pays $36, which is $10 less" % cap(he), "%s pays $46, the same" % cap(he)],
                   "With the socks: $46 + $5 = $51, which is $50 or more, so $10 comes off: $51 − $10 = $41. "
                   "<b>%s pays $41, $5 less than $46</b>, and gets the socks too." % cap(he)))
    assert sale(9, 20) == D("7.20") and D("7.20") / 2 == D("3.60")
    its.append(mcq("A 2 kg bag of oats costs $9.00 and is 20% off. A 1 kg bag costs $3.80 and is not on sale. Which is the better buy?",
                   "The 2 kg bag, by 20¢ per kg", ["The 1 kg bag, by 20¢ per kg", "The 1 kg bag, because it costs less",
                                                   "They cost the same per kg"],
                   "Sale price of the 2 kg bag: 20% of $9.00 is $1.80, so $7.20. Per kg: $7.20 ÷ 2 = $3.60. "
                   "1 kg bag: $3.80 per kg. <b>The 2 kg bag is better by 20¢ per kg</b>. "
                   "(Comparing totals, $3.80 and $7.20, is the mistake.)"))
    assert len(its) == 20
    return {"title": "Discounts and sale prices", "items": its}


# ============================================================ set 5: saving goals and word problems
def set_words(P):
    its = []
    n, he, his, him = P.next()
    assert weeks(84, 12) == 7
    its.append(mcq("%s wants headphones that cost $84. %s saves $12 each week. How many weeks will it take?" % (n, cap(he)),
                   wk(7), [wk(6), wk(72), wk(96)],
                   "Divide the goal by the savings each week: $84 ÷ $12 = <b>7 weeks</b>. Check: 7 × $12 = $84. "
                   "(72 comes from $84 − $12; 96 from $84 + $12.)"))
    n, he, his, him = P.next()
    assert weeks(90, 12) == 8
    its.append(mcq("%s wants a video game that costs $90. %s saves $12 each week. How many weeks until %s has enough?" % (n, cap(he), he),
                   wk(8), [wk(7), "7.5 weeks", wk(78)],
                   "$90 ÷ $12 = 7.5. After 7 weeks %s has 7 × $12 = $84, which is not enough. After 8 weeks %s has $96. "
                   "So it takes <b>8 weeks</b>: round up. (78 comes from $90 − $12.)" % (he, he)))
    n, he, his, him = P.next()
    assert weeks(110 - 35, 15) == 5 and weeks(110, 15) == 8
    its.append(mcq("%s has $35 saved. %s wants a bike helmet that costs $110 and saves $15 each week. How many more weeks until %s can buy it?"
                   % (n, cap(he), he), wk(5), [wk(8), wk(3), wk(10)],
                   "%s still needs $110 − $35 = $75. $75 ÷ $15 = <b>5 weeks</b>. "
                   "(8 weeks forgets the $35 already saved; 10 weeks adds it; 3 weeks divides the $35 saved.)" % cap(he)))
    n, he, his, him = P.next()
    assert D(168) / 12 == 14
    its.append(mq("%s wants to save $168 for a summer camp that starts in 12 weeks. How much must %s save each week?" % (n, he),
                  D(14), [D(156), D("1.40"), D(180)],
                  "Share the goal over the weeks: $168 ÷ 12 = <b>$14</b> a week. Check: 12 × $14 = $168. "
                  "($156 subtracts and $180 adds instead of dividing; $1.40 puts the decimal point in the wrong place.)"))
    n, he, his, him = P.next()
    assert F(72, 96) == F(3, 4)
    its.append(mcq(fig(goal_svg(72, 96)) + "%s is saving for a skateboard. What percent of the goal has %s saved?" % (n, he),
                   "75%", ["72%", "25%", "24%"],
                   "$72 out of $96 = 72/96 = 3/4 = <b>75%</b>. (72% uses the dollars as the percent; 25% is the part still needed.)"))
    n, he, his, him = P.next()
    assert weeks(96 - 72, 8) == 3
    its.append(mcq(fig(goal_svg(72, 96)) + "%s saves $8 a week. How many more weeks until %s reaches the goal?" % (n, he),
                   wk(3), [wk(12), wk(9), wk(24)],
                   "Still needed: $96 − $72 = $24. $24 ÷ $8 = <b>3 weeks</b>. "
                   "(12 weeks divides the whole goal; 9 weeks divides the $72 already saved; 24 is the dollars needed.)"))
    n, he, his, him = P.next()
    assert 13 * 4 == 52 and pct(52, 25) == 13
    its.append(mq("%s earns $13 an hour babysitting and works 4 hours. %s saves 25%% of the money. How much does %s save?" % (n, cap(he), he),
                  D(13), [D(39), D(25), D(52)],
                  "Earned: 4 × $13 = $52. 25% is one quarter: $52 ÷ 4 = <b>$13</b>. ($52 is all the money earned; $39 is the 75% left; $25 uses the percent as dollars.)"))
    assert F(320, 500) == F(16, 25)
    its.append(mcq("A Grade 6 class sets a goal of raising $500 at the Terry Fox Run. So far they have raised $320. What percent of the goal is that?",
                   "64%", ["36%", "32%", "156%"],
                   "320/500 = 64/100 = <b>64%</b>. (36% is the part still to raise; 32% divides by 10 instead of 5; 156% divides 500 by 320.)"))
    assert D(468) / 26 == 18
    its.append(mq("A class of 26 students goes on a field trip to Grouse Mountain. The bus costs $468. How much is the bus for each student?",
                  D(18), [D(442), D(494), D("1.80")],
                  "Share the cost equally: $468 ÷ 26 = <b>$18</b>. Check: 26 × $18 = $468. ($442 subtracts 26; $1.80 misplaces the decimal.)"))
    assert 84 * D("1.25") == 105
    its.append(mq("At a bake sale, the class sells 84 cookies for $1.25 each. How much money do they raise?",
                  D(105), [D("85.25"), D(84), D("10.50")],
                  "84 × $1.25 = 84 × $1 + 84 × $0.25 = $84 + $21 = <b>$105</b>. "
                  "($84 forgets the 25¢; $85.25 adds instead of multiplying; $10.50 puts the decimal point in the wrong place.)"))
    n, he, his, him = P.next()
    assert cash(D("3.67")) == D("3.65") and 5 - D("3.65") == D("1.35")
    its.append(mq("%s buys a snack for $3.67 and pays cash with a $5 bill. Canada has no pennies, so a cash total rounds to the nearest 5¢. "
                  "How much change does %s get?" % (n, he),
                  D("1.35"), [D("1.33"), D("1.30"), D("1.40")],
                  "$3.67 is 2¢ from $3.65 and 3¢ from $3.70, so the cash total is $3.65. Change: $5.00 − $3.65 = <b>$1.35</b>. "
                  "($1.33 forgets the rounding; $1.30 rounds up to $3.70 and $1.40 rounds down to $3.60, but $3.65 is the nearest 5¢.)"))
    n, he, his, him = P.next()
    assert 16 * D("7.5") == 120
    its.append(mq("In the summer, %s picks cherries in the Okanagan for $16 an hour. %s works 7.5 hours. How much does %s earn?" % (n, cap(he), he),
                  D(120), [D(112), D("23.50"), D(128)],
                  "$16 × 7.5 = $16 × 7 + $16 × 0.5 = $112 + $8 = <b>$120</b>. ($112 leaves out the half hour; $128 uses 8 hours; $23.50 adds instead of multiplying.)"))
    n, he, his, him = P.next()
    assert 6 * 52 == 312
    its.append(mq("%s saves $6 every week for a whole year. How much does %s save?" % (n, he),
                  D(312), [D(72), D(58), D(24)],
                  "A year has 52 weeks. 52 × $6 = <b>$312</b>. ($72 uses 12, the number of months; $58 adds 52 + 6; $24 is only about one month.)"))
    assert 48 * 8 - 36 == 348
    its.append(mq("A soccer team holds a car wash in Surrey. They wash 48 cars at $8 each. Soap and sponges cost $36. How much money do they make?",
                  D(348), [D(384), D(420), D(92)],
                  "Money in: 48 × $8 = $384. Take away the cost of supplies: $384 − $36 = <b>$348</b>. "
                  "($384 forgets the supplies; $420 adds them; $92 adds all the numbers.)"))
    n, he, his, him = P.next()
    assert (240 - 64) / 16 == 11 and 240 / 16 == 15
    its.append(mq("%s wants a $240 bike before the summer holidays, which start in 16 weeks. %s already has $64 saved. "
                  "How much must %s save each week?" % (n, cap(he), he),
                  D(11), [D(15), D(4), D(19)],
                  "Still needed: $240 − $64 = $176. $176 ÷ 16 = <b>$11</b> a week. Check: 16 × $11 = $176. "
                  "($15 forgets the $64 saved; $19 adds the $64; $4 divides $64 by 16.)"))
    assert 40 * D("0.75") == 30 and 30 - 12 == 18
    its.append(mq("Two friends run a lemonade stand. Lemons, sugar and cups cost $12. They sell 40 cups for 75¢ each. What is their profit?",
                  D(18), [D(30), D(42), D(288)],
                  "Money in: 40 × $0.75 = $30. Profit = money in − costs: $30 − $12 = <b>$18</b>. "
                  "($30 forgets the costs; $42 adds them; $288 reads 75¢ as $7.50.)"))
    n, he, his, him = P.next()
    assert sale(120, 25) == 90 and weeks(90, 15) == 6 and weeks(120, 15) == 8
    its.append(mcq("New skates cost $120. They go on sale for 25%% off. %s saves $15 a week. How many fewer weeks must %s save because of the sale?"
                   % (n, he),
                   wk(2), [wk(6), wk(8), wk(14)],
                   "Sale price: 25% of $120 is $30, so $90. $90 ÷ $15 = 6 weeks. Without the sale: $120 ÷ $15 = 8 weeks. "
                   "8 − 6 = <b>2 weeks</b> fewer. (6 weeks is the time with the sale and 8 weeks without it; 14 weeks adds them.)"))
    assert 75 - 6 * D("11.50") == 6
    its.append(mq("The class has $75 for a party. They buy 6 pizzas at $11.50 each. How much money is left?",
                  D(6), [D("63.50"), D(9), D(69)],
                  "Pizzas: 6 × $11.50 = $69. Left: $75 − $69 = <b>$6</b>. "
                  "($63.50 subtracts the price of only one pizza; $69 is the cost, not what is left; $9 forgets the 50¢ on each pizza.)"))
    n, he, his, him = P.next()
    assert 20 - D("8.50") == D("11.50") and weeks(92, D("11.50")) == 8
    its.append(mcq("%s earns $20 a week, spends $8.50 a week on snacks and saves the rest. %s goal is $92 for a lacrosse stick. "
                   "How many weeks will it take?" % (n, cap(his)),
                   wk(8), [wk(5), wk(11), wk(4)],
                   "Saved each week: $20.00 − $8.50 = $11.50. $92 ÷ $11.50 = <b>8 weeks</b>. Check: 8 × $11.50 = $92. "
                   "(5 weeks divides by all $20; 11 weeks divides by the $8.50 spent; 4 weeks also forgets to round up.)"))
    n, he, his, him = P.next()
    assert sale(80, 15) == 68 and 68 - 20 == 48 and weeks(48, 12) == 4
    its.append(mcq("%s wants an $80 jacket. Next week it will be 15%% off. %s has $20 and saves $12 a week. "
                   "How many weeks of saving until %s can buy it at the sale price?" % (n, cap(he), he),
                   wk(4), [wk(5), wk(7), wk(6)],
                   "Sale price: 15% of $80 is $12, so $68. Still needed: $68 − $20 = $48. $48 ÷ $12 = <b>4 weeks</b>. "
                   "(5 weeks forgets the sale; 6 weeks forgets the $20; 7 weeks forgets both.)"))
    assert weeks(80 - 20, 12) == 5 and weeks(68, 12) == 6 and weeks(80, 12) == 7
    assert len(its) == 20
    return {"title": "Saving goals and word problems", "items": its}


# ============================================================ lesson
def body_html():
    sec = [("Income", [("Allowance", D(30)), ("Dog walking", D(20))]),
           ("Expenses and savings", [("Bus fare", D(12)), ("Snacks", D(8)), ("Savings", D(15))])]
    assert 50 - 35 == 15
    return (
        "<h2>Budgets: income and expenses</h2>"
        "<p>A budget is a plan for your money. <b>Income</b> is money coming in. <b>Expenses</b> are money going out. "
        "Savings are part of the plan too. A budget is balanced when income = expenses + savings.</p>"
        "<figure class='sn-fig'>" + budget_svg("A budget for one month", sec) +
        "<figcaption>Income: $30 + $20 = $50. Planned: $12 + $8 + $15 = $35. $15 is not planned yet.</figcaption></figure>"
        "<h2>Needs and wants</h2>"
        "<p>A <b>need</b> is something you must have to be safe and healthy: food, water, a home, warm clothes. "
        "A <b>want</b> is nice to have, but you can live without it. Plan for needs first.</p>"
        "<h2>Unit prices and the best buy</h2>"
        "<p>A unit price is the price for one unit, such as per 100 g, per litre or per item. "
        "To find the best buy, compare unit prices, not total prices.</p>"
        "<figure class='sn-fig'>" + tags_svg([("Box A", "400 g", D("5.20")), ("Box B", "750 g", D("8.25"))]) +
        "<figcaption>Box A: $5.20 ÷ 4 = $1.30 per 100 g. Box B: $8.25 ÷ 7.5 = $1.10 per 100 g. Box B is the better buy.</figcaption></figure>"
        "<h2>Discounts</h2>"
        "<p>A discount takes money off the regular price. Find the percent of the regular price and subtract it. "
        "Or find the percent you still pay: 25% off means you pay 75%.</p>" +
        ex("Example", "A $60 rain jacket is 25% off. What is the sale price?",
           "Discount: 25% of $60 = $60 ÷ 4 = $15. Sale price: $60 − $15 = $45. Or: 75% of $60 = $45.", "$45") +
        "<h2>Saving goals</h2>"
        "<p>Subtract what you already have from the goal. Divide what is left by the amount you save each week. "
        "If the answer is not a whole number, round up.</p>" +
        ex("Example", "You want a $90 video game. You have $18 and save $8 a week. How many weeks will it take?",
           "Still needed: $90 − $18 = $72. $72 ÷ $8 = 9. It takes 9 weeks.", "9 weeks") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Picking the package with the lowest total price", "Compare the price per 100 g, per litre or per item"],
            ["Forgetting that savings are part of the plan", "Income = expenses + savings"],
            ["25% off $60 = $60 − 25 = $35", "Find 25% of $60 ($15), then subtract: $45"],
            ["$90 ÷ $12 = 7.5, so 7 weeks", "Round up: after 7 weeks you are still short, so 8 weeks"],
            ["Forgetting money you already saved", "Subtract it from the goal first"],
        ])
    )


FAQ = [
    {"q": "What is budgeting and consumer math in Grade 6 BC math?",
     "a": "It is the Grade 6 financial literacy topic in the BC curriculum. Students plan simple budgets with income and expenses, "
          "sort needs and wants, compare unit prices to find the best buy, and work out discounts and saving goals."},
    {"q": "How do you find the best buy using unit price?",
     "a": "Divide each price by its amount to get the price per 100 g, per litre or per item, then pick the lowest. "
          "For example, $5.20 for 400 g is $1.30 per 100 g and $8.25 for 750 g is $1.10 per 100 g, so the bigger box is the better buy."},
    {"q": "How do I explain needs and wants to my child?",
     "a": "A need is something you must have to be safe and healthy, like food, a home and a warm coat; a want is nice to have, "
          "like a video game. A good budget pays for needs first, then savings and wants."},
    {"q": "How do you make a simple budget for kids?",
     "a": "List the money coming in (allowance, chores, gifts), then the money going out and the amount to save. "
          "If income equals expenses plus savings, the budget is balanced."},
]


def gen():
    rnd = random.Random(56818)
    P = People(rnd)
    sets = [set_budgets(P), set_needs(P), set_unit(P), set_discount(P), set_words(P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            if all(re.fullmatch(r"\$\d+\.\d\d", x) for x in it["c"]):
                assert len({D(x[1:]) for x in it["c"]}) == 4, it
            assert it["q"] not in keys, it["q"]
            keys.add(it["q"])
            assert it["q"].count("<svg") <= 1
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
                assert "HST" not in x and "13%" not in x and "GST" not in x and "PST" not in x, x
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-6", "slug": "budgeting-and-consumer-math", "sort": 18,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 6 Budgeting and Consumer Math: Budgets, Needs and Wants, Unit Prices and Discounts",
        "seo_title": "Grade 6 Budgeting and Consumer Math Worksheets: Unit Price, Discounts and Saving Goals (Free, Answer Key, BC Curriculum)",
        "short_title": "Budgeting and consumer math",
        "domain": "Financial literacy",
        "standard_code": "Grade 6: Financial literacy",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/6/core",
        "standard_text": "Financial literacy – simple budgeting and consumer math",
        "meta_desc": "Free Grade 6 math worksheets on budgeting and consumer math for the BC curriculum: income and expenses, "
                     "needs and wants, unit prices and the best buy, discounts and sale prices, and saving goals. "
                     "100 questions with an answer key.",
        "key_big": "Compare unit prices, not total prices: the lowest price per 100 g, per litre or per item is the best buy.",
        "key_sub": "A budget is balanced when income equals expenses plus savings. Pay for needs first. "
                   "For a discount, find the percent of the regular price and subtract it.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "Shelf tags: [^;']*;[^;']*;")
    mark_large(u, "Budget ")
    mark_large(u, "Savings goal bar")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
