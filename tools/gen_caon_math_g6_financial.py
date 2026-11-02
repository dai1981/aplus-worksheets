# -*- coding: utf-8 -*-
"""
CA Grade 6 Math: Financial Literacy (Ontario Curriculum 2020, Financial Literacy F1)
  python3 tools/gen_ca_math_g6_financial.py
Ways to pay (cash, debit, credit, e-transfer), unit price and the best buy, 13% HST, budgets and word problems.
All money is worked with decimal.Decimal; HST is rounded to the cent (half up, and no price is used whose
tax ends in exactly half a cent). Canada has no pennies: cash totals round to the nearest 5 cents, card and
e-transfer payments are exact. Ontario style: 4-digit numbers without a separator, $ and the cent sign.
Helpers are copied from gen_ca_math_g6_add_sub_decimals.py. HTML attributes use single quotes.
"""
import json, os, random, re
from decimal import Decimal as D, ROUND_HALF_UP
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
GREY = "#6b6259"
PAPER = "#fffdf5"
EDGE = "#b8b0a0"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
CENT = D("0.01")


# ------------------------------------------------------------ money
def money(d):
    d = D(d)
    assert 0 <= d < 10000, d
    return "$" + format(d.quantize(CENT), "f")


def cents_ok(x):
    """True when a Decimal or Fraction is a whole number of cents."""
    return (F(str(x)) * 100).denominator == 1


def tax(p):
    """13% HST rounded to the cent. Prices whose tax ends in exactly half a cent are not used."""
    p = D(p)
    raw = p * D("0.13")
    assert (p * 100 * 13) % 100 != 50, p
    return raw.quantize(CENT, rounding=ROUND_HALF_UP)


def with_tax(p):
    return D(p) + tax(p)


def cash(d):
    """No pennies: a cash total is rounded to the nearest 5 cents (1, 2, 6, 7 down; 3, 4, 8, 9 up)."""
    c = int(D(d) * 100)
    assert D(c) / 100 == D(d)
    return D((c + 2) // 5 * 5) / 100


def cap(s):
    return s[0].upper() + s[1:]


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
        if c in seen or not c:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def mq(q, correct, wrongs, e):
    """Money question: correct and wrong values are Decimals; wrong values equal to the answer or below 1 cent are skipped."""
    correct = D(correct)
    w = [money(x) for x in wrongs if x is not None and D(x) > 0 and cents_ok(x) and D(x) != correct]
    return mcq(q, money(correct), w, e)


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) over the 4 positions in every set."""
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


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag wide pictures (3 shelf tags, budget tables) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def tags_svg(tags):
    """Shelf tags side by side: tags = [(name, size, price)]."""
    tw, th, gap = 150, 110, 14
    s = []
    for i, (name, size, price) in enumerate(tags):
        x = 2 + i * (tw + gap)
        s.append("<rect x='%d' y='2' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>" % (x, tw, th, PAPER, EDGE))
        s.append("<path d='M%d 32 V10 a8 8 0 0 1 8 -8 H%d a8 8 0 0 1 8 8 V32 Z' fill='%s'/>" % (x, x + tw - 8, GREEN))
        s.append("<text x='%d' y='24' font-size='17' font-weight='700' fill='#ffffff' text-anchor='middle'>%s</text>" % (x + tw // 2, name))
        s.append("<text x='%d' y='60' font-size='18' fill='%s' text-anchor='middle'>%s</text>" % (x + tw // 2, INK, size))
        s.append("<text x='%d' y='98' font-size='28' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (x + tw // 2, INK, money(price)))
    W = 4 + len(tags) * tw + (len(tags) - 1) * gap
    label = "Shelf tags: " + "; ".join("%s, %s, %s" % (n, sz, money(p)) for n, sz, p in tags)
    return svg_wrap(W, th + 4, "".join(s), label)


def budget_svg(title, money_in, money_out):
    """A small budget table: rows of (label, amount) under Money in and Money out."""
    W, rh, fs = 300, 25, 16
    s = []
    y = 26
    s.append("<text x='%d' y='%d' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>%s</text>" % (W // 2, y - 6, INK, title))
    rows = [("Money in", None, "h")] + [(a, b, "r") for a, b in money_in] + [("Money out", None, "h")] + [(a, b, "r") for a, b in money_out]
    top = y
    for label, amt, kind in rows:
        if kind == "h":
            s.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s'/>" % (y, W - 4, rh, GREEN))
            s.append("<text x='12' y='%d' font-size='%d' font-weight='700' fill='#ffffff'>%s</text>" % (y + 18, fs, label))
        else:
            s.append("<line x1='2' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (y + rh, W - 2, y + rh, EDGE))
            s.append("<text x='12' y='%d' font-size='%d' fill='%s'>%s</text>" % (y + 18, fs, INK, label))
            s.append("<text x='%d' y='%d' font-size='%d' fill='%s' text-anchor='end'>%s</text>" % (W - 12, y + 18, fs, INK, money(amt)))
        y += rh
    s.append("<rect x='2' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>" % (top, W - 4, y - top, EDGE))
    label = "Budget %s. Money in: %s. Money out: %s" % (
        title, ", ".join("%s %s" % (a, money(b)) for a, b in money_in), ", ".join("%s %s" % (a, money(b)) for a, b in money_out))
    return svg_wrap(W, y + 4, "".join(s), label)


# ============================================================ set 1: ways to pay
CASH, DEBIT, CREDIT, ET = "Cash", "Debit card", "Credit card", "E-transfer"
METHODS = [CASH, DEBIT, CREDIT, ET]


def which(q, ans, e):
    return mcq(q, ans, [m for m in METHODS if m != ans], e)


def set_pay(P):
    its = []
    its.append(mcq("When you pay with a debit card, where does the money come from?",
                   "Your own bank account", ["Money borrowed from the card company", "Money saved on the card itself",
                                             "The store’s bank account"],
                   "A debit card takes the money <b>straight out of your own bank account</b> when you pay. "
                   "You can only spend money that is already in the account."))
    its.append(mcq("When you pay with a credit card, what are you doing?",
                   "Borrowing money to pay back later", ["Taking money out of your bank account",
                                                          "Using money saved on the card", "Getting the item for free"],
                   "A credit card company pays the store for you, so you are <b>borrowing</b>. "
                   "You get a bill later and must pay it back."))
    its.append(which("Which way of paying sends money from your bank account to another person using their email address or mobile phone number?",
                     ET, "An <b>e-transfer</b> moves money from one bank account to another. You send it using the other person’s "
                         "email address or mobile phone number, so you do not need to meet."))
    its.append(which("Which way of paying cannot be used to buy something from an online store?",
                     CASH, "Online stores need a card or another electronic payment. You cannot hand coins and bills "
                           "over the internet, so <b>cash</b> cannot be used."))
    its.append(which("Which way of paying is the only one where the total is rounded to the nearest 5¢?",
                     CASH, "Canada has no pennies, so only a <b>cash</b> total is rounded to the nearest 5¢. "
                           "Debit, credit and e-transfer payments are for the exact amount."))
    its.append(which("Which way of paying can cost you interest if you do not pay the full bill by the due date?",
                     CREDIT, "A <b>credit card</b> is borrowed money. If the full bill is not paid by the due date, "
                             "the card company adds interest, so the things you bought cost more."))
    its.append(mcq("What is one advantage of paying with cash?",
                   "You can only spend what you have", ["It works for online shopping", "The bank replaces lost cash",
                                                        "The total is never rounded"],
                   "With cash you can see your money go down, and <b>you cannot spend more than you have</b> with you. "
                   "Cash cannot be used online, lost cash is gone, and cash totals are rounded to 5¢."))
    its.append(mcq("What is one disadvantage of paying with cash?",
                   "It can be lost or stolen", ["You pay interest on it", "You need an email address",
                                                "Stores never take it"],
                   "If cash is <b>lost or stolen</b>, it is usually gone for good. A lost bank card can be cancelled, "
                   "but coins and bills cannot."))
    its.append(mcq("What is one advantage of paying with a debit card?",
                   "You pay with money you already have", ["You can pay the bill next month",
                                                           "It never needs a bank account", "Totals round down to 5¢"],
                   "Debit takes the exact amount from your bank account right away, so <b>you pay with money you already have</b> "
                   "and do not get a bill later. You need a bank account to have a debit card."))
    its.append(mcq("What is one disadvantage of a debit card?",
                   "You need a bank account to use it", ["It charges interest every month",
                                                          "It cannot be used in stores", "It only works for whole dollars"],
                   "A debit card is linked to a bank account, so <b>you need a bank account</b>. "
                   "Debit does not charge interest, because you are not borrowing."))
    its.append(mcq("What is one advantage of a credit card?",
                   "You can buy now and pay later", ["You never have to pay it back",
                                                     "It uses only money in your account", "It never charges interest"],
                   "With a credit card <b>you can buy something now and pay the bill later</b>. "
                   "If you pay the full bill by the due date, you usually pay no interest."))
    its.append(mcq("What is one disadvantage of a credit card?",
                   "It is easy to spend more than you have", ["It cannot be used online",
                                                              "The total is rounded to 5¢", "You must carry coins"],
                   "Because you are borrowing, <b>it is easy to spend more than you have</b>. "
                   "Any part of the bill not paid on time has interest added."))
    its.append(mcq("What is one advantage of an e-transfer?",
                   "You can pay without meeting in person", ["It does not need a bank account",
                                                             "It gives you coins as change", "It is rounded to 5¢"],
                   "An e-transfer goes by email or phone number, so <b>you can pay someone without meeting in person</b>, "
                   "even in another city. Both people need bank accounts."))
    its.append(mcq("What is one disadvantage of an e-transfer?",
                   "A wrong email can send money astray", ["It can only be used in stores",
                                                           "It is rounded to the nearest 5¢", "You must hand it over"],
                   "If you type the wrong email address or phone number, <b>the money can go to the wrong person</b>, "
                   "and it can be hard to get back. Always check before you send."))
    n, he, his = P.next()
    its.append(which("%s’s grandmother in Winnipeg wants to send %s $25 for %s birthday. %s lives in Halifax. "
                     "Which way of paying lets her send it straight to %s’s bank account?" % (n, "her" if he == "she" else "him", his, n, n),
                     ET, "An <b>e-transfer</b> sends money from one bank account to another using an email address or phone number. "
                         "Cash would have to be mailed or handed over."))
    # numbers: exact or rounded
    n, he, his = P.next()
    assert cash("4.17") == D("4.15")
    its.append(mq("%s buys a snack for $4.17 and pays with a debit card. How much is taken from %s bank account?" % (n, his),
                  D("4.17"), [D("4.15"), D("4.20"), D("4.10")],
                  "Debit is charged the <b>exact</b> amount: <b>$4.17</b>. Only cash totals are rounded to 5¢."))
    n, he, his = P.next()
    its.append(mq("%s buys the same $4.17 snack and pays with cash. How much does %s pay?" % (n, he),
                  D("4.15"), [D("4.17"), D("4.20"), D("4.10")],
                  "Cash is rounded to the nearest 5¢. $4.17 is 2¢ from $4.15 and 3¢ from $4.20, so %s pays <b>$4.15</b>. "
                  "(Totals ending in 1, 2, 6 or 7 cents round down; 3, 4, 8 or 9 round up.)" % he))
    its.append(mcq("Which cash total does NOT change when it is rounded to the nearest 5¢?",
                   "$12.35", ["$12.36", "$12.38", "$12.32"],
                   "$12.35 already ends in 5¢, so it stays <b>$12.35</b>. $12.36 → $12.35, $12.38 → $12.40, $12.32 → $12.30."))
    n, he, his = P.next()
    assert cash("9.48") == D("9.50")
    its.append(mq("%s’s total at the corner store is $9.48. %s pays with cash. How much does %s pay?" % (n, cap(he), he),
                  D("9.50"), [D("9.45"), D("9.48"), D("9.40")],
                  "$9.48 is 2¢ from $9.50 and 3¢ from $9.45, so it rounds up to <b>$9.50</b>."))
    n, he, his = P.next()
    t = D("8.63")
    assert cash(t) == D("8.65") and 10 - cash(t) == D("1.35")
    its.append(mq("%s’s total is $8.63. %s pays cash with a $10 bill. How much change does %s get?" % (n, cap(he), he),
                  D("1.35"), [10 - t, 10 - D("8.60"), 10 - D("8.70")],
                  "Step 1, round the cash total: $8.63 is 2¢ from $8.65 and 3¢ from $8.60, so it is $8.65. "
                  "Step 2, change: $10.00 − $8.65 = <b>$1.35</b>. ($1.37 forgets the cash rounding.)"))
    assert len(its) == 20
    return {"title": "Ways to pay: cash, debit, credit and e-transfer", "items": its}


# ============================================================ set 2: unit price and best buy
def unit_item(q, price, amount, base, per, figure=None, note=""):
    """Unit price for `base` when `amount` costs `price` (amount and base in the same unit).
    k = amount / base; unit price = price / k (cent-exact)."""
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
    wr = []
    for w in [F(str(price)) * k, F(str(price)) / (k * 10), F(str(price)) * 10 / k, F(str(price)) / (k / 10) if k >= 10 else None,
              F(str(price)) - k if k.denominator == 1 else None, F(str(price))]:
        if w is not None and w > 0 and (w * 100).denominator == 1:
            wr.append(D(w.numerator) / D(w.denominator))
    if figure:
        q = fig(figure) + q
    return mq(q, ans, wr, e)


def best_item(q, opts, unit_txt, base, figure=False, both=None, cant=None, note=""):
    """opts = [(label, amount, amount_text, price)]; amounts in the base unit's smallest unit; lowest price per base wins."""
    us = []
    for lab, amt, at, pr in opts:
        u = F(str(D(pr))) * base / amt
        assert (u * 100).denominator == 1, (lab, amt, pr)
        us.append((u, lab, at, pr))
    srt = sorted(us)
    tie = len(us) == 2 and us[0][0] == us[1][0]
    parts = []
    for u, lab, at, pr in us:
        k = F(amt_of(opts, lab)) / base
        kt = str(k.numerator) if k.denominator == 1 else format(D(k.numerator) / D(k.denominator), "f")
        parts.append("%s: %s ÷ %s = %s %s" % (lab, money(pr), kt, money(D(u.numerator) / D(u.denominator)), unit_txt))
    e = "Compare the price " + unit_txt + ", not the total price. " + "; ".join(parts) + ". "
    same = both or "Both cost the same " + unit_txt
    if tie:
        ans = same
        e += "The unit prices are equal, so <b>neither is a better buy</b>."
    else:
        assert srt[0][0] < srt[1][0]
        ans = srt[0][1]
        e += ("<b>%s</b> has the lower price %s, so it is the better buy." if len(us) == 2 else
              "<b>%s</b> has the lowest price %s, so it is the best buy.") % (ans, unit_txt)
        cheapest_total = min(us, key=lambda t: D(t[3]))[1]
        if cheapest_total != ans:
            e += " (%s: lower total price, but you get less.)" % cheapest_total
    if note:
        e += " " + note
    choices = [lab for lab, a, at, p in opts]
    if len(opts) == 2:
        choices += [same, cant or "You cannot compare different sizes"]
    else:
        choices += ["They all cost the same " + unit_txt]
    if figure:
        q = fig(tags_svg([(lab, at, pr) for lab, a, at, pr in opts])) + q
    return mcq(q, ans, [c for c in choices if c != ans], e)


def amt_of(opts, lab):
    return [a for l, a, at, p in opts if l == lab][0]


def set_unit(P):
    its = []
    G100 = ("100 g", "the mass", "per 100 g")
    its.append(mcq("A shelf tag shows “$0.70 per 100 g”. What does this unit price tell you?",
                   "The cost of 100 g of the food", ["The cost of the whole package", "The tax on the food",
                                                     "How many grams $1 buys"],
                   "A unit price is the price for one unit of the item, here <b>100 g</b>. It lets you compare packages of "
                   "different sizes fairly."))
    its.append(unit_item("A 500 g bag of rice costs $3.50. What is the price per 100 g?", "3.50", 500, 100,
                         ("100 g", "500 g", "per 100 g")))
    its.append(unit_item("A 4 L bag of milk costs $6.20. What is the price per litre?", "6.20", 4, 1,
                         ("1 L", "4 L", "per litre")))
    its.append(unit_item("A 2 L bottle of apple juice costs $3.40. What is the price per litre?", "3.40", 2, 1,
                         ("1 L", "2 L", "per litre")))
    its.append(unit_item("A 300 g block of cheese costs $5.40. What is the price per 100 g?", "5.40", 300, 100,
                         ("100 g", "300 g", "per 100 g")))
    its.append(unit_item("A 1 kg bag of apples costs $4.00. What is the price per 100 g?", "4.00", 1000, 100,
                         ("100 g", "1 kg (1000 g)", "per 100 g"), note="Remember 1 kg = 1000 g, not 100 g."))
    its.append(mcq("Two boxes of crackers are different sizes. What should you compare to find the better buy?",
                   "The price per 100 g", ["The total prices", "The sizes of the boxes", "The pictures on the boxes"],
                   "A bigger box usually costs more in total, so totals do not tell you which is cheaper. Compare "
                   "<b>the price for the same amount</b>, such as per 100 g."))
    its.append(best_item("Which box of cereal is the better buy?",
                         [("Box A", 500, "500 g", "6.00"), ("Box B", 750, "750 g", "8.25")], "per 100 g", 100, figure=True))
    its.append(best_item("Which box of crackers is the better buy?",
                         [("Box A", 200, "200 g", "2.50"), ("Box B", 300, "300 g", "3.90")], "per 100 g", 100, figure=True,
                         note="A bigger box is not always the better buy."))
    its.append(best_item("Which bottle of juice is the better buy?",
                         [("Bottle A", 1, "1 L", "2.40"), ("Bottle B", 2, "2 L", "4.80")], "per litre", 1, figure=True))
    its.append(best_item("Which bag of milk is the better buy?",
                         [("Bag A", 1, "1 L", "2.60"), ("Bag B", 4, "4 L", "6.40")], "per litre", 1, figure=True))
    its.append(best_item("A 650 g tub of yogurt costs $3.90. A pack of 4 yogurt cups, 100 g each, costs $2.80. Which is the better buy?",
                         [("The tub", 650, "650 g", "3.90"), ("The 4 cups", 400, "400 g", "2.80")], "per 100 g", 100))
    its.append(best_item("A box of 8 granola bars costs $3.20. A box of 12 granola bars costs $5.40. Which is the better buy?",
                         [("The box of 8", 8, "8 bars", "3.20"), ("The box of 12", 12, "12 bars", "5.40")], "per bar", 1,
                         cant="You cannot compare different boxes"))
    n, he, his = P.next()
    assert F(350) / 5 == 70 and F(600) / 10 == 60
    its.append(mcq("A 500 g jar of peanut butter costs $3.50. A 1 kg jar costs $6.00. %s says the 500 g jar is the better buy "
                   "because it costs less. Is %s right?" % (n, he),
                   "No, the 1 kg jar costs less per 100 g", ["Yes, it costs less in total", "Yes, smaller jars always cost less per 100 g",
                                                            "No, the two jars cost the same per 100 g"],
                   "Compare unit prices, not totals. 500 g jar: $3.50 ÷ 5 = $0.70 per 100 g. 1 kg jar: $6.00 ÷ 10 = $0.60 per 100 g. "
                   "<b>The 1 kg jar costs less per 100 g</b>, so it is the better buy (if you will use it all)."))
    its.append(unit_item("A 750 g bag of oats costs $6.00. What is the price per 100 g?", "6.00", 750, 100,
                         ("100 g", "750 g", "per 100 g")))
    its.append(unit_item("A 500 mL bottle of maple syrup costs $9.80. What is the price per litre?", "9.80", 500, 1000,
                         ("1 L", "500 mL", "per litre"),
                         note="500 mL is half a litre, so 1 L costs twice as much."))
    its.append(unit_item("A 1.5 kg bag of carrots costs $3.45. What is the price per kilogram?", "3.45", F(3, 2), 1,
                         ("1 kg", "1.5 kg", "per kilogram")))
    its.append(best_item("A 250 mL can of maple syrup costs $8.50. A 1 L jug costs $28.00. Which is the better buy?",
                         [("The can", 250, "250 mL", "8.50"), ("The jug", 1000, "1 L", "28.00")], "per litre", 1000,
                         cant="You cannot compare mL and L"))
    its.append(best_item("Which jug of orange juice is the best buy?",
                         [("Jug A", 1, "1 L", "2.80"), ("Jug B", 2, "2 L", "5.00"), ("Jug C", 4, "4 L", "10.40")],
                         "per litre", 1, figure=True))
    its.append(best_item("Which bag of rice is the best buy?",
                         [("Bag A", 500, "500 g", "2.25"), ("Bag B", 1000, "1 kg", "4.00"), ("Bag C", 2000, "2 kg", "8.40")],
                         "per 100 g", 100, figure=True))
    assert len(its) == 20
    return {"title": "Unit price and the best buy", "items": its}


# ============================================================ set 3: 13% HST
def hst_wrongs(p):
    p = D(p)
    return [p + 13, p + D("0.13"), p + tax(p), tax(p), p * D("0.1") + p, (p * D("0.013")).quantize(CENT), p * 13]


def rawtxt(x):
    """Exact product as money text: 1.3 -> $1.30, 3.2487 -> $3.2487."""
    x = D(x)
    return money(x) if x == x.quantize(CENT) else "$" + format(x.normalize(), "f")


def tax_item(q, p, extra_e=""):
    p = D(p)
    t = tax(p)
    raw = p * D("0.13")
    if raw == t:
        e = "13%% = 0.13. %s × 0.13 = <b>%s</b>." % (money(p), money(t))
    else:
        e = "13%% = 0.13. %s × 0.13 = %s, which rounds to <b>%s</b> (to the nearest cent)." % (money(p), rawtxt(raw), money(t))
    if extra_e:
        e += " " + extra_e
    down = raw.quantize(CENT, rounding="ROUND_DOWN")
    wr = [(p * D("0.013")).quantize(CENT) if (p * D("0.013")) == (p * D("0.013")).quantize(CENT) else None,
          down if down != t else None, p * 13 if p * 13 < 1000 else None, p + t, D("13"), D("0.13"), p * D("0.1")]
    return mq(q, t, wr, e)


def total_item(q, p, extra_e=""):
    p = D(p)
    t = tax(p)
    raw = p * D("0.13")
    tot = p + t
    e = "HST: %s × 0.13 = %s%s. Total: %s + %s = <b>%s</b>." % (
        money(p), rawtxt(raw), "" if raw == t else " → " + money(t), money(p), money(t), money(tot))
    if extra_e:
        e += " " + extra_e
    return mq(q, tot, [p + 13, p + D("0.13"), t, p + p * D("0.1")], e)


def set_hst(P):
    its = []
    its.append(mcq("Most things you buy in Ontario have 13% HST added. What does 13% mean?",
                   "13¢ for every $1", ["$13 on every purchase", "13¢ on every purchase", "$1.30 for every $1"],
                   "Percent means “out of 100”. 13% = 13 out of 100, so the tax is <b>13¢ for every $1</b> of the price. "
                   "On $10 the HST is $1.30."))
    its.append(tax_item("What is 13% of $10.00?", "10"))
    its.append(tax_item("A board game costs $20.00. How much is the 13% HST?", "20"))
    its.append(tax_item("A pair of headphones costs $50.00. How much is the 13% HST?", "50"))
    its.append(tax_item("A phone case costs $8.00. How much is the 13% HST?", "8"))
    assert D(3) + D("0.90") == tax(30)
    its.append(mq("Find 13% of $30 in your head: 10% of $30 is $3.00 and 3% of $30 is $0.90. What is 13% of $30?",
                  D("3.90"), [D("3.03"), D("33.90"), D("3.30"), D("0.39")],
                  "13% = 10% + 3%. $3.00 + $0.90 = <b>$3.90</b>. (3% of $30 is 3 × $0.30 = $0.90, not $0.03.)"))
    its.append(mcq("Which calculation gives the total price with 13% HST in one step?",
                   "price × 1.13", ["price × 0.13", "price + 13", "price × 13"],
                   "The total is 100% of the price plus 13% more = 113% = 1.13. So <b>price × 1.13</b> gives the total. "
                   "price × 0.13 gives only the tax."))
    its.append(total_item("A backpack costs $40.00. 13% HST is added. What is the total price?", "40"))
    its.append(total_item("A puzzle costs $25.00. 13% HST is added. What is the total price?", "25"))
    its.append(total_item("A skateboard costs $60.00. 13% HST is added. What is the total price?", "60"))
    its.append(total_item("A set of markers costs $12.40. 13% HST is added. What is the total price?", "12.40"))
    its.append(tax_item("A video game costs $24.99. How much is the 13% HST, rounded to the nearest cent?", "24.99"))
    its.append(total_item("A video game costs $24.99. 13% HST is added. What is the total price?", "24.99"))
    its.append(tax_item("A water bottle costs $7.49. How much is the 13% HST, rounded to the nearest cent?", "7.49"))
    assert tax("80") == D("10.40") and abs(D("79.99") * D("0.13") - D("10.40")) < D("0.01")
    its.append(mcq("About how much HST is added to an item that costs $79.99? Round the price first.",
                   "about $10.40", ["about $13", "about $8", "about $1.04"],
                   "$79.99 is about $80. 10% of $80 is $8 and 3% is $2.40, so 13% is about $8 + $2.40 = <b>$10.40</b>. "
                   "($8 is only 10%; $13 adds $13 instead of 13%.)"))
    tot = with_tax("7")
    assert tot == D("7.91") and cash(tot) == D("7.90")
    n, he, his = P.next()
    its.append(mq("A $7.00 key chain has 13%% HST added. %s pays with cash. How much does %s pay?" % (n, he),
                  D("7.90"), [tot, D("7.95"), D("20.00"), D("7.13")],
                  "HST: $7.00 × 0.13 = $0.91. Total: $7.91. Cash is rounded to the nearest 5¢: $7.91 → <b>$7.90</b>. "
                  "($7.91 is what a card pays.)"))
    tot = with_tax("3.60")
    assert tot == D("4.07") and cash(tot) == D("4.05")
    n, he, his = P.next()
    its.append(mq("A $3.60 pack of trading cards has 13%% HST added. %s pays with cash. How much does %s pay?" % (n, he),
                  D("4.05"), [tot, D("4.10"), D("16.60"), D("3.75")],
                  "HST: $3.60 × 0.13 = $0.468 → $0.47. Total: $3.60 + $0.47 = $4.07. Cash rounds $4.07 down to <b>$4.05</b>."))
    p = D("14.99") + D("5.00")
    assert p == D("19.99") and tax(p) == D("2.60") and p + tax(p) == D("22.59")
    its.append(mq("A soccer ball costs $14.99 and a pump costs $5.00. 13% HST is added to the total. What is the total price?",
                  D("22.59"), [p + 13, D("14.99") + tax("14.99") + 5, p + D("0.13"), tax(p) * 2],
                  "Price before tax: $14.99 + $5.00 = $19.99. HST: $19.99 × 0.13 = $2.5987 → $2.60. "
                  "Total: $19.99 + $2.60 = <b>$22.59</b>. (Tax is added to both items.)"))
    assert tax("15.75") == D("2.05")
    its.append(tax_item("A pack of art paper costs $15.75. How much is the 13% HST, rounded to the nearest cent?", "15.75",
                        "Do not just cut off the extra digits ($2.04): 0.75¢ rounds up."))
    assert with_tax("11.30") == D("12.77") and with_tax(10) == D("11.30") and (D("11.30") - D("11.30") * D("0.13")).quantize(CENT) == D("9.83")
    its.append(mq("A total of $11.30 includes 13% HST. What was the price before HST?",
                  D("10.00"), [D("9.83"), D("11.17"), D("12.77")],
                  "The total is 113% of the price, so price × 1.13 = $11.30. Price = $11.30 ÷ 1.13 = <b>$10.00</b>. "
                  "Check: $10.00 + $1.30 = $11.30. ($9.83 takes 13% of the total, but the tax was 13% of the price. $12.77 adds the tax a second time.)"))
    assert len(its) == 20
    return {"title": "Adding 13% HST", "items": its}


# ============================================================ set 4: budgets, earning and saving
def weeks(goal, per):
    q = F(str(D(goal))) / F(str(D(per)))
    return -(-q.numerator // q.denominator)


def wk(n):
    return "%d week%s" % (n, "" if n == 1 else "s")


def set_budget(P):
    its = []
    its.append(mcq("What is a budget?", "A plan for earning, spending and saving",
                   ["A list of things you want to buy", "The money in your bank account", "A bill from a store"],
                   "A budget is <b>a plan</b> for your money: the money coming in (earning) and how it will be spent and saved."))
    its.append(mcq("When is a budget balanced?", "Money in = money spent + money saved",
                   ["Money spent is more than money in", "You spend nothing at all", "You save all your money"],
                   "A budget is balanced when <b>every dollar coming in is planned for</b>: spending plus saving equals money in."))
    n, he, his = P.next()
    assert 6 * 5 == 30
    its.append(mq("%s gets a $15 allowance each week and saves $5 of it. How much has %s saved after 6 weeks?" % (n, he),
                  D(30), [D(90), D(60), D(11)],
                  "%s saves $5 each week. 6 × $5 = <b>$30</b>. ($90 is all of the allowance, and $60 is the part spent.)" % cap(he)))
    n, he, his = P.next()
    assert D(12) * D("3.5") == 42
    its.append(mq("%s earns $12 an hour babysitting. On Saturday %s babysits for 3.5 hours. How much does %s earn?" % (n, he, he),
                  D(42), [D(36), D("15.50"), D(48)],
                  "Earnings = rate × hours = $12 × 3.5. $12 × 3 = $36 and $12 × 0.5 = $6. $36 + $6 = <b>$42</b>. "
                  "($36 leaves out the half hour.)"))
    n, he, his = P.next()
    assert weeks(84, 12) == 7
    its.append(mcq("%s wants headphones that cost $84. %s saves $12 each week. How many weeks will it take?" % (n, cap(he)),
                   wk(7), [wk(6), wk(72), wk(8)],
                   "Divide the goal by the savings each week: $84 ÷ $12 = <b>7 weeks</b>. Check: 7 × $12 = $84. "
                   "(72 comes from subtracting $84 − $12.)"))
    n, he, his = P.next()
    assert weeks(90, 12) == 8
    its.append(mcq("%s wants a video game that costs $90. %s saves $12 each week. How many weeks until %s has enough?" % (n, cap(he), he),
                   wk(8), [wk(7), "7.5 weeks", wk(78)],
                   "$90 ÷ $12 = 7.5. After 7 weeks %s has only 7 × $12 = $84, which is not enough. "
                   "After 8 weeks %s has $96. So it takes <b>8 weeks</b>: round up." % (he, he)))
    n, he, his = P.next()
    assert D(20) * D("0.25") == 5
    its.append(mq("%s plans to save 25%% of a $20 allowance. How much does %s save?" % (n, he),
                  D(5), [D(15), D("0.25"), D(4)],
                  "25%% is one quarter. $20 ÷ 4 = <b>$5</b>. ($15 is the 75%% %s keeps to spend.)" % he))
    n, he, his = P.next()
    assert D(40) * D("0.3") == 12
    its.append(mq("%s earns $40. %s plans to save 50%%, spend 30%% and give 20%% to charity. How much will %s spend?" % (n, cap(he), he),
                  D(12), [D(20), D(8), D(30)],
                  "Spend 30% of $40: 10% is $4, so 30% is 3 × $4 = <b>$12</b>. Check: save $20 + spend $12 + give $8 = $40."))
    n, he, his = P.next()
    bi, bo = [("Allowance", D(20)), ("Dog walking", D(15))], [("Movie", D(12)), ("Snacks", D(6)), ("Savings", D(10))]
    left = sum(b for a, b in bi) - sum(b for a, b in bo)
    assert left == 7
    its.append(mq(fig(budget_svg("%s’s budget for May" % n, bi, bo)) +
                  "Look at %s’s budget. How much money is not planned for yet?" % n,
                  left, [D(17), D(63), D(25)],
                  "Money in: $20 + $15 = $35. Money out: $12 + $6 + $10 = $28 (savings is planned money too). "
                  "$35 − $28 = <b>$7</b>. ($17 forgets to count the savings.)"))
    n, he, his = P.next()
    bi, bo = [("Allowance", D(50))], [("Hockey tape", D(18)), ("Pizza night", D(15)), ("Savings", D(22))]
    tin, tout = sum(b for a, b in bi), sum(b for a, b in bo)
    assert tout - tin == 5
    its.append(mcq(fig(budget_svg("%s’s budget for March" % n, bi, bo)) +
                   "Is %s’s budget balanced?" % n,
                   "No, %s plans $5 more than %s has" % (he, he),
                   ["Yes, it is balanced", "No, %s has $5 left over" % he, "No, %s plans $55 more than %s has" % (he, he)],
                   "Money out: $18 + $15 + $22 = $55. Money in: $50. $55 − $50 = $5, so <b>%s plans to spend and save $5 more than %s has</b>. "
                   "%s could save $17 instead of $22." % (he, he, cap(he))))
    assert D(420) / 28 == 15
    its.append(mq("A Grade 6 class of 28 students is going on a field trip. The bus costs $420. How much is the bus for each student?",
                  D(15), [D(448), D(392), D("1.50")],
                  "Share the cost equally: $420 ÷ 28 = <b>$15</b>. Check: 28 × $15 = $420."))
    assert 28 * D("12.50") == 350
    its.append(mq("Admission to the science centre is $12.50 per student. How much is admission for all 28 students?",
                  D(350), [D(336), D("40.50"), D(35)],
                  "28 × $12.50 = 28 × $12 + 28 × $0.50 = $336 + $14 = <b>$350</b>. ($336 forgets the 50¢.)"))
    assert D(15) + D("12.50") == D("27.50")
    its.append(mq("For the field trip, each student pays $15 for the bus and $12.50 for admission. What is the total for each student?",
                  D("27.50"), [D("16.25"), D("2.50"), D("28.50")],
                  "Add the two costs: $15.00 + $12.50 = <b>$27.50</b>."))
    assert D(252) / 28 == 9 and D("27.50") - 9 == D("18.50")
    its.append(mq("The class raises $252 at a bake sale to help pay for the $27.50-per-student trip. The money is shared equally by the "
                  "28 students. How much does each student pay now?",
                  D("18.50"), [D("9.00"), D("36.50"), D("224.50")],
                  "Step 1: $252 ÷ 28 = $9 for each student. Step 2: $27.50 − $9.00 = <b>$18.50</b>."))
    n, he, his = P.next()
    assert 3 * 6 == 18
    its.append(mcq("%s can earn $3 for each day of chores (6 days a week), or get $20 each week. Which choice gives more money in a week?" % n,
                   "$20 each week", ["$3 a day for 6 days", "Both give the same", "You cannot tell"],
                   "$3 × 6 days = $18 a week. $20 > $18, so <b>$20 each week</b> gives $2 more."))
    n, he, his = P.next()
    assert weeks(110 - 35, 15) == 5 and weeks(110, 15) == 8
    its.append(mcq("%s has $35 saved. %s wants a bike helmet that costs $110 and saves $15 each week. How many more weeks until %s can buy it?"
                   % (n, cap(he), he), wk(5), [wk(8), wk(3), wk(7)],
                   "%s still needs $110 − $35 = $75. $75 ÷ $15 = <b>5 weeks</b>. "
                   "(8 weeks forgets the $35 already saved.)" % cap(he)))
    n, he, his = P.next()
    assert 7 * 20 - 45 == 95
    its.append(mq("After a big snowfall, %s shovels 7 driveways at $20 each. %s spends $45 on new winter mitts and a hat. "
                  "How much does %s have left to save?" % (n, cap(he), he),
                  D(95), [D(140), D(185), D(25)],
                  "Earned: 7 × $20 = $140. Left: $140 − $45 = <b>$95</b>."))
    its.append(mcq("A budget lists needs and wants. In a Canadian winter, which is a need for a student?",
                   "Winter boots that fit", ["A new video game", "A concert ticket", "A second hockey jersey"],
                   "A need is something you must have to be safe and healthy. <b>Winter boots that fit</b> keep your feet warm and dry. "
                   "The others are wants: nice to have, but not needed."))
    n, he, his = P.next()
    assert F(12, 48) == F(1, 4)
    its.append(mcq("%s’s budget is $48 for the month. %s plans to spend $12 on snacks. What percent of the budget is that?" % (n, cap(he)),
                   "25%", ["12%", "36%", "4%"],
                   "$12 out of $48 = 12/48 = 1/4 = <b>25%</b>. (12% uses the dollars as the percent; 4% comes from 48 ÷ 12.)"))
    n, he, his = P.next()
    assert D(150) / 10 == 15
    its.append(mq("%s wants to save $150 for summer camp by Canada Day, which is 10 weeks away. How much must %s save each week?" % (n, he),
                  D(15), [D(140), D("1.50"), D(160)],
                  "Share the goal over the weeks: $150 ÷ 10 = <b>$15</b> a week. Check: 10 × $15 = $150."))
    assert len(its) == 20
    return {"title": "Budgets, earning and saving", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []
    n, he, his = P.next()
    p = D("59.99")
    t = tax(p)
    assert t == D("7.80") and p + t == D("67.79")
    its.append(mq("%s buys a hockey stick for $59.99. 13%% HST is added, and %s pays with a debit card. How much is %s charged?" % (n, he, he),
                  p + t, [p + 13, cash(p + t), p + D("0.13")],
                  "HST: $59.99 × 0.13 = $7.7987 → $7.80. Total: $59.99 + $7.80 = <b>$67.79</b>. "
                  "Debit is charged the exact amount, so it is not rounded to 5¢."))
    n, he, his = P.next()
    p = D(21)
    assert with_tax(p) == D("23.73") and cash(with_tax(p)) == D("23.75")
    its.append(mq("%s buys a $21.00 board game. 13%% HST is added, and %s pays with cash. How much does %s pay?" % (n, he, he),
                  D("23.75"), [D("23.73"), D(34), D("23.70")],
                  "HST: $21.00 × 0.13 = $2.73. Total: $23.73. Cash: $23.73 is 2¢ from $23.75, so %s pays <b>$23.75</b>. "
                  "($23.73 forgets the cash rounding.)" % he))
    n, he, his = P.next()
    p = D(16)
    assert with_tax(p) == D("18.08") and cash(D("18.08")) == D("18.10") and 20 - D("18.10") == D("1.90")
    its.append(mq("%s buys a $16.00 art kit. 13%% HST is added. %s pays cash with a $20 bill. How much change does %s get?" % (n, cap(he), he),
                  D("1.90"), [D("1.92"), D(4), D("1.95")],
                  "HST: $16.00 × 0.13 = $2.08, so the total is $18.08. Cash rounds $18.08 up to $18.10. "
                  "Change: $20.00 − $18.10 = <b>$1.90</b>. ($1.92 forgets the cash rounding; $4.00 forgets the HST.)"))
    n, he, his = P.next()
    p = D(80)
    need = with_tax(p) - 15
    assert with_tax(p) == D("90.40") and need == D("75.40") and weeks(need, 10) == 8 and weeks(80 - 15, 10) == 7 and weeks(with_tax(p), 10) == 10
    its.append(mcq("%s wants a skateboard that costs $80 plus 13%% HST. %s has $15 saved and saves $10 each week. "
                   "How many more weeks until %s can buy it?" % (n, cap(he), he),
                   wk(8), [wk(7), wk(10), wk(6)],
                   "Total with HST: $80 × 1.13 = $90.40. Still needed: $90.40 − $15 = $75.40. $75.40 ÷ $10 = 7.54, "
                   "so round up to <b>8 weeks</b>. (7 weeks forgets the HST; 10 weeks forgets the $15 saved.)"))
    n, he, his = P.next()
    assert D("4.50") / 3 == D("1.50") and D(7) / 5 == D("1.40") and 15 * D("1.50") - 15 * D("1.40") == D("1.50")
    its.append(mq("%s needs 15 notebooks for school. Store A sells 3 notebooks for $4.50. Store B sells 5 notebooks for $7.00. "
                  "How much does %s save by buying them all at the store with the lower unit price?" % (n, he),
                  D("1.50"), [D("2.50"), D("0.10"), D(21)],
                  "Unit prices: Store A $4.50 ÷ 3 = $1.50 each; Store B $7.00 ÷ 5 = $1.40 each. "
                  "15 notebooks: Store A 15 × $1.50 = $22.50; Store B 15 × $1.40 = $21.00. Savings: $22.50 − $21.00 = <b>$1.50</b>."))
    n, he, his = P.next()
    assert D(48) * D("0.75") == 36
    its.append(mq("A $48 hoodie is on sale for 25% off. What is the sale price before tax?",
                  D(36), [D(12), D(23), D(60)],
                  "25% of $48 = $48 ÷ 4 = $12 off. Sale price: $48 − $12 = <b>$36</b>. ($12 is the discount, not the price.)"))
    assert with_tax(36) == D("40.68")
    its.append(mq("%s buys the hoodie at the sale price of $36. 13%% HST is added. What is the total?" % n,
                  D("40.68"), [D(49), D("36.13"), D("4.68"), D("39.60")],
                  "HST: $36 × 0.13 = $4.68. Total: $36.00 + $4.68 = <b>$40.68</b>."))
    n, he, his = P.next()
    assert 4 * D("2.50") * 5 == 50
    its.append(mq("For the Terry Fox Run, 4 neighbours each pledge $2.50 for every kilometre %s runs. %s runs 5 km. "
                  "How much does %s raise?" % (n, cap(he), he),
                  D(50), [D("12.50"), D(10), D("11.50")],
                  "One neighbour gives 5 × $2.50 = $12.50. Four neighbours give 4 × $12.50 = <b>$50</b>."))
    n, he, his = P.next()
    assert D("54.24") / 4 == D("13.56") and D("54.24") / 3 == D("18.08")
    its.append(mq("%s and 3 friends order pizza for $54.24, tax included. %s pays, and %s friends send their shares by e-transfer. "
                  "What is each person’s equal share?" % (n, n, his),
                  D("13.56"), [D("18.08"), D("50.24"), D("216.96")],
                  "%s and 3 friends make 4 people. $54.24 ÷ 4 = <b>$13.56</b>. (Dividing by 3 forgets to count %s.) "
                  "Check: 4 × $13.56 = $54.24." % (n, n)))
    n, he, his = P.next()
    t = with_tax(32)
    assert t == D("36.16") and 50 - t == D("13.84")
    its.append(mq("%s has $50 in %s bank account. %s buys $32.00 earbuds with a debit card, and 13%% HST is added. How much is left in the account?"
                  % (n, his, cap(he)),
                  D("13.84"), [D(18), D(5), D("13.85")],
                  "HST: $32 × 0.13 = $4.16. Total: $36.16. Left: $50.00 − $36.16 = <b>$13.84</b>. "
                  "Debit is exact, so there is no rounding. ($18 forgets the HST.)"))
    n, he, his = P.next()
    assert 4 * 13 == 52 and 156 / 52 == 3
    its.append(mcq("Each Saturday %s babysits for 4 hours at $13 an hour. %s wants to earn $156 for a new bike. How many Saturdays will it take?"
                   % (n, cap(he)), "3 Saturdays", ["12 Saturdays", "39 Saturdays", "4 Saturdays"],
                   "Each Saturday: 4 × $13 = $52. $156 ÷ $52 = <b>3 Saturdays</b>. (12 divides by $13, the pay for only one hour.)"))
    its.append(best_item("Apples are sold in three bags. Which bag is the best buy?",
                         [("Bag A", 2, "2 kg", "5.20"), ("Bag B", 3, "3 kg", "7.50"), ("Bag C", 5, "5 kg", "13.00")],
                         "per kilogram", 1, figure=True))
    assert 6 * 15 == 90 and with_tax(90) == D("101.70")
    its.append(mq("A class orders 6 pizzas at $15 each for a pizza lunch. 13% HST is added. What is the total cost?",
                  D("101.70"), [D(103), D("11.70"), D("90.13"), D("99.00")],
                  "Before tax: 6 × $15 = $90. HST: $90 × 0.13 = $11.70. Total: $90 + $11.70 = <b>$101.70</b>."))
    n, he, his = P.next()
    p = D("27.99")
    t = with_tax(p)
    assert t == D("31.63") and cash(t) == D("31.65") and 50 - cash(t) == D("18.35")
    its.append(mq("%s buys a basketball for $27.99. 13%% HST is added. %s pays cash with a $50 bill. How much change does %s get?" % (n, cap(he), he),
                  D("18.35"), [D("18.37"), D("22.01"), D("18.40")],
                  "HST: $27.99 × 0.13 = $3.6387 → $3.64. Total: $31.63. Cash rounds $31.63 up to $31.65. "
                  "Change: $50.00 − $31.65 = <b>$18.35</b>. ($22.01 forgets the HST; $18.37 forgets the cash rounding.)"))
    assert D(62) / 40 == D("1.55") and D("1.55") * 50 == D("77.50")
    its.append(mq("A family pays $62.00 for 40 L of gas on the drive to the cottage. At the same price per litre, how much would 50 L cost?",
                  D("77.50"), [D(72), D("1.55"), D("49.60")],
                  "Unit price: $62.00 ÷ 40 = $1.55 per litre. 50 L: 50 × $1.55 = <b>$77.50</b>. "
                  "($72 adds $10 for 10 more litres instead of 10 × $1.55.)"))
    n, he, his = P.next()
    assert D(15) * D("0.4") == 6 and weeks(54, 6) == 9 and weeks(54, 15) == 4
    its.append(mcq("%s earns $15 a week and saves 40%% of it. How many weeks will it take %s to save $54?" % (n, "her" if he == "she" else "him"),
                   wk(9), [wk(4), wk(6), wk(36)],
                   "40% of $15: 10% is $1.50, so 40% is 4 × $1.50 = $6 a week. $54 ÷ $6 = <b>9 weeks</b>. "
                   "(4 weeks uses all $15; 6 is the dollars saved each week, not the weeks.)"))
    n1, _, _ = P.next()
    n2, _, _ = P.next()
    assert cash("2.98") == D("3.00")
    its.append(mcq("%s buys a $2.98 granola bar with cash. %s buys the same bar with a debit card. Who pays more, and by how much?" % (n1, n2),
                   "%s, by 2¢" % n1, ["%s, by 2¢" % n2, "%s, by 3¢" % n1, "They pay the same"],
                   "Cash: $2.98 rounds up to $3.00. Debit: exactly $2.98. <b>%s pays 2¢ more</b>. "
                   "On another day a cash total might round down instead, so cash can also cost a little less." % n1))
    assert (D(650) / 26 + 14) == 39 and D(260) / 26 == 10 and D(39) - 10 == 29
    its.append(mq("A class of 26 students goes on a field trip. The bus costs $650 and admission is $14 per student. "
                  "The school council gives $260. The rest is shared equally. How much does each student pay?",
                  D(29), [D(39), D(15), D(25)],
                  "Bus per student: $650 ÷ 26 = $25. Cost per student: $25 + $14 = $39. Council money per student: $260 ÷ 26 = $10. "
                  "Each pays $39 − $10 = <b>$29</b>."))
    n, he, his = P.next()
    assert 15 * 6 == 90 and 90 - 75 == 15
    its.append(mcq("Public skating costs $6 a visit, or $75 for a winter pass. %s plans to skate 15 times this winter. Which is cheaper, and by how much?" % n,
                   "The pass, by $15", ["Paying each visit, by $15", "The pass, by $69", "They cost the same"],
                   "Paying each visit: 15 × $6 = $90. The pass: $75. $90 − $75 = $15, so <b>the pass is cheaper by $15</b>. "
                   "($69 is $75 − $6.)"))
    n, he, his = P.next()
    sv = 13 * 8
    t = with_tax(85)
    assert sv == 104 and t == D("96.05") and sv - t == D("7.95")
    its.append(mq("%s saves $8 a week for 13 weeks. Then %s buys a pair of skates for $85 plus 13%% HST, paying by debit. How much of %s savings is left?"
                  % (n, he, his),
                  D("7.95"), [D(19), D("7.92"), D("6.00")],
                  "Savings: 13 × $8 = $104. Skates: $85 × 0.13 = $11.05 HST, so $96.05. Left: $104.00 − $96.05 = <b>$7.95</b>. "
                  "($19 forgets the HST.)"))
    assert len(its) == 20
    return {"title": "Money word problems", "items": its}


# ============================================================ lesson
def body_html():
    assert tax(40) == D("5.20") and with_tax(40) == D("45.20")
    assert with_tax("24.99") == D("28.24") and cash(D("28.24")) == D("28.25")
    return (
        "<h2>Four ways to pay</h2>"
        "<p>Each way to pay has advantages and disadvantages. Choose the one that fits what you are buying.</p>" +
        table(["Way to pay", "How it works", "Advantages", "Disadvantages"], [
            ["Cash", "Coins and bills", "You can only spend what you have. No bank account needed", "Can be lost or stolen. Not for online stores. Total rounded to 5¢"],
            ["Debit card", "Takes money straight from your bank account", "Exact amount. No bill later. Works in stores and online", "Needs a bank account. You can only spend what is in it"],
            ["Credit card", "Borrows money you pay back when the bill comes", "Buy now, pay later. Works in stores and online", "Easy to overspend. Interest is added if the bill is not paid in full on time"],
            ["E-transfer", "Sends money between bank accounts by email or phone number", "Pay someone without meeting", "Needs a bank account. A typing mistake can send money to the wrong person"],
        ]) +
        "<p>Canada has no pennies. Only <b>cash</b> totals are rounded to the nearest 5¢ (1, 2, 6, 7 cents round down; 3, 4, 8, 9 round up). "
        "Card and e-transfer payments are exact.</p>"
        "<h2>Unit price: find the best buy</h2>"
        "<p>A bigger package usually costs more, so you cannot compare total prices. Find the <b>unit price</b>: the cost of the same "
        "amount, such as 100 g, 1 L or 1 item. The lower unit price is the better buy.</p>"
        "<figure class='sn-fig'>" + tags_svg([("Box A", "400 g", D("4.80")), ("Box B", "650 g", D("7.15"))]) +
        "<figcaption>Box A: $4.80 ÷ 4 = $1.20 per 100 g. Box B: $7.15 ÷ 6.5 = $1.10 per 100 g. Box B is the better buy, even though it costs more.</figcaption></figure>"
        "<h2>Adding 13% HST</h2>"
        "<p>In Ontario, 13% HST is added to most things you buy (some, like basic groceries, have none). 13% means 13¢ for every $1. "
        "Multiply the price by 0.13, round to the nearest cent, then add. Or multiply by 1.13 in one step.</p>" +
        ex("Example", "A $40.00 backpack has 13% HST added. What is the total?",
           "HST: $40.00 × 0.13 = $5.20. Total: $40.00 + $5.20 = $45.20. One step: $40.00 × 1.13 = $45.20.", "$45.20") +
        ex("Example", "A $24.99 game has 13% HST added. How much do you pay with cash?",
           "HST: $24.99 × 0.13 = $3.2487 → $3.25. Total: $28.24. Cash rounds to the nearest 5¢: $28.25. A card pays $28.24.",
           "$28.25 with cash") +
        "<h2>Budgets: plan your money</h2>"
        "<p>A budget lists the money coming in (allowance, jobs) and the money going out (spending and saving). "
        "It is <b>balanced</b> when money in equals money out.</p>"
        "<figure class='sn-fig'>" + budget_svg("A budget for May", [("Allowance", D(20)), ("Dog walking", D(15))],
                                               [("Movie", D(12)), ("Snacks", D(6)), ("Savings", D(17))]) +
        "<figcaption>Money in: $20 + $15 = $35. Money out: $12 + $6 + $17 = $35. The budget is balanced.</figcaption></figure>" +
        ex("Example", "You want a $90 game and save $12 a week. How many weeks will it take?",
           "$90 ÷ $12 = 7.5. After 7 weeks you have $84, not enough. Round up.", "8 weeks") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Picking the package with the lower total price", "Compare the price per 100 g, per litre or per item"],
            ["Adding $13 (or 13¢) instead of 13%", "Find 13% of the price: price × 0.13"],
            ["Giving only the tax as the total", "Add the HST to the price: price × 1.13"],
            ["Forgetting to round a cash total", "Cash rounds to the nearest 5¢; cards do not"],
            ["Rounding the weeks down ($90 ÷ $12 = 7.5 → 7)", "Round up: after 7 weeks you are still short"],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn in financial literacy in Ontario?",
     "a": "Grade 6 students compare ways to pay (cash, debit, credit and e-transfer), find unit prices to choose the best value, "
          "and design simple budgets. Money questions also use decimals and percents, such as adding 13% HST."},
    {"q": "How do you calculate 13% HST on a price?",
     "a": "Multiply the price by 0.13 and round to the nearest cent, then add it to the price. For $40, the HST is $5.20 and the total is $45.20, the same as $40 × 1.13."},
    {"q": "How do you find the best buy using unit price?",
     "a": "Divide each price by the amount to get the cost for the same unit, such as 100 g or 1 L. The lower unit price is the better buy, even if the package costs more in total."},
    {"q": "What is the difference between a debit card and a credit card?",
     "a": "A debit card takes money straight from your own bank account. A credit card borrows money that you pay back later, and interest is added if the bill is not paid in full by the due date."},
]


def verify(sets):
    for s in sets:
        for it in s["items"]:
            right = it["c"][it["a"]]
            if "with cash" in it["q"] and right.startswith("$") and "change" not in it["q"]:
                assert int(D(right[1:]) * 100) % 5 == 0, it["q"]


def gen():
    rnd = random.Random(36819)
    P = People(rnd)
    sets = [set_pay(P), set_unit(P), set_hst(P), set_budget(P), set_words(P)]
    balance(sets, rnd)
    verify(sets)
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
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-6", "slug": "financial-literacy", "sort": 19,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 6 Financial Literacy: Ways to Pay, Unit Price, HST and Budgets",
        "seo_title": "Grade 6 Financial Literacy Worksheets: Unit Price, 13% HST and Budgets (Free, Answer Key)",
        "short_title": "Financial Literacy",
        "domain": "Financial Literacy",
        "standard_code": "Grade 6: Financial Literacy, F1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Describe the advantages and disadvantages of various methods of payment that can be used when purchasing goods "
                         "and services; determine the unit rates of goods and services, and identify which is the best value; design basic budgets",
        "meta_desc": "Free Grade 6 financial literacy math worksheets for the Ontario curriculum: cash, debit, credit and e-transfer, "
                     "unit price and the best buy, adding 13% HST, cash rounding without pennies, and simple budgets for saving goals "
                     "and a class trip. 100 questions with an answer key, good EQAO practice.",
        "key_big": "Compare unit prices, not totals, and add 13% HST as price × 1.13.",
        "key_sub": "The lower price per 100 g or per litre is the better buy. HST is 13¢ for every $1, rounded to the cent; "
                   "only cash totals round to the nearest 5¢. A budget is balanced when money in equals money spent plus saved.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "Shelf tags: [^;']*;[^;']*;")
    mark_large(u, "Budget ")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
