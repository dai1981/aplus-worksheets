# -*- coding: utf-8 -*-
"""
CA-ON Grade 5 Math: Financial Literacy (Ontario Curriculum 2020, F1.2 to F1.6)
  python3 tools/gen_caon_math_g5_financial.py
Total cost of several items and change (cash rounded to 5 cents), adding 13% HST to whole-dollar prices,
simple budgets, unit price and the best buy, credit, debt, interest and taxes.
All money is worked with decimal.Decimal. HST is only taken on whole-dollar prices, so it is always an exact
number of cents. Canada has no pennies: cash totals round to the nearest 5 cents; card payments are exact.
Helpers are copied from gen_caon_math_g6_financial.py. HTML attributes use single quotes.
"""
import json, os, random, re
from decimal import Decimal as D, ROUND_HALF_UP
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-5")
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



def receipt_svg(title, items, total=None):
    """A store receipt: rows of (item, price), optional total line."""
    W, rh, fs = 280, 26, 16
    s = []
    y = 4
    s.append("<rect x='2' y='2' width='%d' height='%%H%%' rx='4' fill='%s' stroke='%s' stroke-width='2'/>" % (W - 4, PAPER, EDGE))
    s.append("<text x='%d' y='%d' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>%s</text>" % (W // 2, y + 20, GREEN, title))
    y += 30
    s.append("<line x1='12' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5' stroke-dasharray='4 3'/>" % (y, W - 12, y, GREY))
    for name, price in items:
        s.append("<text x='14' y='%d' font-size='%d' fill='%s'>%s</text>" % (y + 19, fs, INK, name))
        s.append("<text x='%d' y='%d' font-size='%d' fill='%s' text-anchor='end'>%s</text>" % (W - 14, y + 19, fs, INK, money(price)))
        y += rh
    if total is not None:
        s.append("<line x1='12' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5' stroke-dasharray='4 3'/>" % (y + 3, W - 12, y + 3, GREY))
        y += 4
        s.append("<text x='14' y='%d' font-size='%d' font-weight='700' fill='%s'>%s</text>" % (y + 19, fs, INK, total[0]))
        s.append("<text x='%d' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='end'>%s</text>"
                 % (W - 14, y + 19, fs, INK, total[1]))
        y += rh
    H = y + 8
    body = "".join(s).replace("%H%", str(H - 4))
    label = "Receipt %s: %s" % (title, ", ".join("%s %s" % (n, money(p)) for n, p in items))
    return svg_wrap(W, H, body, label)


def big(n):
    """Whole number with a no-break space between groups of three when it has 5 or more digits."""
    t = str(n)
    if len(t) <= 4:
        return t
    out = ""
    while len(t) > 3:
        out = " " + t[-3:] + out
        t = t[:-3]
    return t + out


# ============================================================ set 1: total cost and change
def set_total(P):
    its = []
    assert D("1.25") + D("2.50") == D("3.75")
    its.append(mq("A juice box costs $1.25 and a muffin costs $2.50. What is the total cost?",
                  D("3.75"), [D("1.50"), D("3.50"), D("4.75")],
                  "Line up the decimal points: $1.25 + $2.50 = <b>$3.75</b>. ($1.50 reads $2.50 as 25¢.)"))
    items = [("Pencil case", D("4.35")), ("Ruler", D("1.20")), ("Eraser", D("0.95"))]
    assert sum(p for n, p in items) == D("6.50")
    its.append(mq(fig(receipt_svg("School Supplies", items)) + "What is the total cost of the three items?",
                  D("6.50"), [D("5.55"), D("5.50"), D("7.50")],
                  "Add the cents: 35¢ + 20¢ + 95¢ = 150¢ = $1.50. Add the dollars: $4 + $1 + $0 = $5. "
                  "$5 + $1.50 = <b>$6.50</b>. ($5.50 forgets to carry the extra dollar; $5.55 leaves out the eraser.)"))
    its.append(mcq("Estimate the total cost of three items priced $3.95, $6.10 and $1.98. Round each price to the nearest dollar.",
                   "About $12", ["About $10", "About $11", "About $13"],
                   "$3.95 → $4, $6.10 → $6, $1.98 → $2. $4 + $6 + $2 = <b>about $12</b>. "
                   "(About $10 just drops the cents: $3 + $6 + $1.)"))
    n, he, his = P.next()
    assert 10 - D("7.40") == D("2.60")
    its.append(mq("%s buys a book for $7.40 and pays with a $10 bill. How much change does %s get?" % (n, he),
                  D("2.60"), [D("3.60"), D("2.40"), D("3.40")],
                  "$10.00 − $7.40 = <b>$2.60</b>. Check: $7.40 + $2.60 = $10.00. "
                  "($3.60 forgets to regroup a dollar.)"))
    assert D("0.10") + D("0.25") + 1 == D("1.35") == 5 - D("3.65")
    its.append(mq("Count up to find the change from $5 for a $3.65 snack: $3.65 → $3.75 → $4.00 → $5.00. How much change is that?",
                  D("1.35"), [D("1.45"), D("2.35"), D("1.25")],
                  "Add the jumps: 10¢ + 25¢ + $1.00 = <b>$1.35</b>. Check: $3.65 + $1.35 = $5.00."))
    assert cash("6.42") == D("6.40")
    its.append(mq("Canada has no pennies, so a cash total is rounded to the nearest 5¢. A cash total is $6.42. How much do you pay?",
                  D("6.40"), [D("6.45"), D("6.42"), D("6.50")],
                  "$6.42 is 2¢ from $6.40 and 3¢ from $6.45. The closer one is <b>$6.40</b>."))
    assert cash("8.73") == D("8.75")
    its.append(mq("A cash total is $8.73. Rounded to the nearest 5¢, how much do you pay?",
                  D("8.75"), [D("8.70"), D("8.73"), D("8.80")],
                  "$8.73 is 2¢ from $8.75 and 3¢ from $8.70, so you pay <b>$8.75</b>."))
    its.append(mcq("Which cash total stays the same when it is rounded to the nearest 5¢?",
                   "$5.65", ["$5.61", "$5.68", "$5.64"],
                   "<b>$5.65</b> already ends in 5¢. $5.61 → $5.60, $5.68 → $5.70, $5.64 → $5.65."))
    n, he, his = P.next()
    its.append(mq("%s’s total at the store is $6.42. %s pays with a debit card. How much is taken from %s bank account?" % (n, cap(he), his),
                  D("6.42"), [D("6.40"), D("6.45"), D("6.50")],
                  "Card payments are for the <b>exact</b> amount: <b>$6.42</b>. Only cash totals are rounded to 5¢."))
    assert 3 * D("2.25") == D("6.75")
    its.append(mq("Hot dogs cost $2.25 each. How much do 3 hot dogs cost?",
                  D("6.75"), [D("6.25"), D("5.25"), D("4.50")],
                  "3 × $2.25: 3 × $2 = $6 and 3 × 25¢ = 75¢. $6 + 75¢ = <b>$6.75</b>. "
                  "($6.25 multiplies only the dollars; $5.25 adds 3 instead of multiplying.)"))
    items = [("Notebook", D("2.49")), ("Glue stick", D("1.79")), ("Markers", D("5.99")), ("Pencils", D("3.25"))]
    assert 2 + 2 + 6 + 3 == 13
    its.append(mcq(fig(receipt_svg("School Supplies", items)) + "Round each price to the nearest dollar. About how much is the total?",
                   "About $13", ["About $11", "About $12", "About $14"],
                   "$2.49 → $2, $1.79 → $2, $5.99 → $6, $3.25 → $3. $2 + $2 + $6 + $3 = <b>about $13</b>. "
                   "(About $11 just drops the cents.) The exact total is $13.52, close to the estimate."))
    n, he, his = P.next()
    assert 20 - D("13.55") == D("6.45")
    its.append(mq("%s’s total is $13.55. %s pays cash with a $20 bill. How much change does %s get?" % (n, cap(he), he),
                  D("6.45"), [D("7.45"), D("6.55"), D("33.55")],
                  "$13.55 already ends in 5¢, so it is not rounded. $20.00 − $13.55 = <b>$6.45</b>. "
                  "Check: $13.55 + $6.45 = $20.00. ($7.45 forgets to regroup.)"))
    n, he, his = P.next()
    assert cash("11.37") == D("11.35") and 20 - D("11.35") == D("8.65")
    its.append(mq("%s’s total is $11.37. %s pays cash with a $20 bill. How much change does %s get?" % (n, cap(he), he),
                  D("8.65"), [D("8.63"), D("8.60"), D("9.65")],
                  "Step 1, round the cash total: $11.37 is 2¢ from $11.35, so it is $11.35. "
                  "Step 2: $20.00 − $11.35 = <b>$8.65</b>. ($8.63 forgets the cash rounding.)"))
    its.append(mcq("A cashier gives 65¢ in change. Which uses the fewest coins?",
                   "2 quarters, 1 dime, 1 nickel", ["6 dimes, 1 nickel", "2 quarters, 3 nickels", "1 quarter, 4 dimes"],
                   "All four make 65¢. Start with the biggest coins: 2 quarters = 50¢, 1 dime = 60¢, 1 nickel = 65¢. "
                   "That is <b>4 coins</b>. The others use 5 or 7 coins."))
    assert 2 + 1 + D("0.25") + D("0.10") == D("3.35")
    its.append(mq("%s has a toonie, a loonie, a quarter and a dime. How much money is that?" % P.next()[0],
                  D("3.35"), [D("2.35"), D("3.30"), D("4.35")],
                  "Toonie $2 + loonie $1 + quarter 25¢ + dime 10¢ = <b>$3.35</b>. "
                  "($2.35 counts the toonie as $1; $3.30 counts the dime as 5¢.)"))
    n, he, his = P.next()
    assert 2 * D("3.50") + D("2.75") == D("9.75")
    its.append(mq("%s buys 2 bags of popcorn at $3.50 each and a drink for $2.75. What is the total cost?" % n,
                  D("9.75"), [D("6.25"), D("7.00"), D("8.75")],
                  "Popcorn: 2 × $3.50 = $7.00. Total: $7.00 + $2.75 = <b>$9.75</b>. ($6.25 counts only one bag of popcorn.)"))
    n, he, his = P.next()
    assert D("8.95") + D("6.89") + D("4.75") == D("20.59") and 9 + 7 + 5 == 21
    its.append(mcq("%s has $20. %s wants a hat for $8.95, a scarf for $6.89 and mitts for $4.75. Estimate: does %s have enough?" % (n, cap(he), he),
                   "No, it is about $21", ["Yes, it is about $18", "Yes, it is about $20", "No, it is about $25"],
                   "Round: $8.95 → $9, $6.89 → $7, $4.75 → $5. $9 + $7 + $5 = $21, which is more than $20. "
                   "<b>No</b>. The exact total, $20.59, agrees. (About $18 drops the cents; about $20 rounds $4.75 down.)"))
    n, he, his = P.next()
    items = [("Skate rental", D("4.50")), ("Admission", D("3.75")), ("Hot chocolate", D("2.15"))]
    assert sum(p for x, p in items) == D("10.40") and 20 - D("10.40") == D("9.60")
    its.append(mq(fig(receipt_svg("Skating Rink", items)) +
                  "%s pays cash with a $20 bill. How much change does %s get?" % (n, he),
                  D("9.60"), [D("10.60"), D("9.40"), D("30.40")],
                  "Total: $4.50 + $3.75 + $2.15 = $10.40 (already a multiple of 5¢). "
                  "Change: $20.00 − $10.40 = <b>$9.60</b>. ($10.60 forgets to regroup; $30.40 adds instead of subtracting.)"))
    n, he, his = P.next()
    t = D("2.29") + D("4.50") + D("1.99")
    assert t == D("8.78") and cash(t) == D("8.80")
    its.append(mq("%s buys bread for $2.29, cheese for $4.50 and apples for $1.99. %s pays with cash. How much does %s pay?" % (n, cap(he), he),
                  D("8.80"), [D("8.78"), D("8.75"), D("7.78")],
                  "Total: $2.29 + $4.50 + $1.99 = $8.78. Cash rounds to the nearest 5¢: $8.78 is 2¢ from $8.80, "
                  "so %s pays <b>$8.80</b>. ($8.78 forgets the cash rounding.)" % he))
    n, he, his = P.next()
    assert 4 * D("2.35") == D("9.40") and 10 - D("9.40") == D("0.60")
    its.append(mq("%s buys 4 packs of hockey cards at $2.35 each. %s pays cash with a $10 bill. How much change does %s get?" % (n, cap(he), he),
                  D("0.60"), [D("1.65"), D("7.65"), D("1.60")],
                  "Cost: 4 × $2.35 = $8 + $1.40 = $9.40. Change: $10.00 − $9.40 = <b>$0.60</b>. "
                  "($1.65 multiplies only the dollars; $7.65 pays for 1 pack.)"))
    assert len(its) == 20
    return {"title": "Total cost and change", "items": its}


# ============================================================ set 2: 13% HST
def hst_q(q, p, e_extra=""):
    p = D(p)
    t = tax(p)
    assert p == int(p)
    e = "13%% = 13¢ for every $1. %d × 13¢ = %s, so the HST is <b>%s</b>." % (p, money(t), money(t))
    if e_extra:
        e += " " + e_extra
    return mq(q, t, [D(13), t / 10, p + t, D("0.13")], e)


def tot_q(q, p, e_extra=""):
    p = D(p)
    t = tax(p)
    e = "HST: %d × 13¢ = %s. Total: %s + %s = <b>%s</b>." % (p, money(t), money(p), money(t), money(p + t))
    if e_extra:
        e += " " + e_extra
    return mq(q, p + t, [p + 13, p + D("0.13"), t, p + t / 10], e)


def set_hst(P):
    its = []
    its.append(mcq("In Ontario, 13% HST is added to most things you buy. What does 13% mean?",
                   "13¢ for every $1", ["$13 on every item", "13¢ on every item", "$1.30 for every $1"],
                   "Percent means “out of 100”. 13% is 13 out of 100, so the tax is <b>13¢ for every $1</b> (100¢) of the price."))
    its.append(mcq("An item costs $1. How much is the 13% HST?",
                   "13¢", ["$13", "$1.13", "1¢"],
                   "13% of $1 is <b>13¢</b>. ($1.13 is the price plus the tax.)"))
    its.append(hst_q("A book costs $10. How much is the 13% HST?", 10, "($13.00 adds $13 instead of 13%.)"))
    its.append(hst_q("A board game costs $20. How much is the 13% HST?", 20))
    its.append(hst_q("A pair of running shoes costs $50. How much is the 13% HST?", 50))
    its.append(hst_q("A phone charger costs $5. How much is the 13% HST?", 5))
    assert tax(40) == D("5.20")
    its.append(mq("Find 13% of $40 in two steps: 10% of $40 is $4.00 and 3% of $40 is $1.20. What is 13% of $40?",
                  D("5.20"), [D("4.03"), D("45.20"), D("1.20")],
                  "13% = 10% + 3%. $4.00 + $1.20 = <b>$5.20</b>. ($4.03 uses 3¢ instead of 3%; $45.20 is the price plus the tax.)"))
    its.append(tot_q("A T-shirt costs $10. 13% HST is added. What is the total price?", 10,
                     "($23.00 adds $13 instead of 13%.)"))
    its.append(tot_q("A puzzle costs $20. 13% HST is added. What is the total price?", 20))
    its.append(tot_q("A soccer ball costs $30. 13% HST is added. What is the total price?", 30))
    its.append(tot_q("A backpack costs $50. 13% HST is added. What is the total price?", 50))
    its.append(tot_q("A bike helmet costs $40. 13% HST is added. What is the total price?", 40))
    its.append(tot_q("A tent costs $100. 13% HST is added. What is the total price?", 100,
                     "On $100, 13% is exactly $13."))
    n, he, his = P.next()
    its.append(mcq("A shirt costs $20. %s says the total with 13%% HST is $33. What mistake did %s make?" % (n, he),
                   "%s added $13 instead of 13%%" % cap(he),
                   ["%s forgot to add the tax" % cap(he), "%s gave only the tax" % cap(he), "%s rounded to the nearest 5¢" % cap(he)],
                   "13%% of $20 is $2.60, so the total is $22.60. $20 + $13 = $33 shows that "
                   "<b>%s added $13 instead of 13%%</b>." % he))
    assert tax(60) == D("7.80")
    its.append(mq("A bike lock costs $60. 13% HST is added. What is the total price?",
                  D("67.80"), [D(73), D("60.13"), D("7.80")],
                  "HST: 10% of $60 is $6.00 and 3% is $1.80, so 13% is $7.80. Total: $60 + $7.80 = <b>$67.80</b>."))
    n, he, his = P.next()
    assert with_tax(20) == D("22.60") and D(15) + tax(15) + 5 == D("21.95")
    its.append(mq("%s buys a $15 puzzle and a $5 card game. 13%% HST is added to both. What is the total?" % n,
                  D("22.60"), [D("21.95"), D("33.00"), D("20.13")],
                  "Price before tax: $15 + $5 = $20. HST: 20 × 13¢ = $2.60. Total: $20 + $2.60 = <b>$22.60</b>. "
                  "($21.95 adds tax to the puzzle only.)"))
    its.append(mcq("A video game costs $49. About how much is the 13% HST?",
                   "About $6.50", ["About $13", "About $4.90", "About $0.65"],
                   "$49 is close to $50. 13% of $50 = 50 × 13¢ = $6.50, so the HST is <b>about $6.50</b>. "
                   "($4.90 is only 10%.)"))
    n, he, his = P.next()
    t = with_tax(9)
    assert t == D("10.17") and cash(t) == D("10.15")
    its.append(mq("%s buys a $9 kite. 13%% HST is added, and %s pays with cash. How much does %s pay?" % (n, he, he),
                  D("10.15"), [D("10.17"), D("10.20"), D(22)],
                  "HST: 9 × 13¢ = $1.17. Total: $10.17. Cash rounds to the nearest 5¢: $10.17 is 2¢ from $10.15, "
                  "so %s pays <b>$10.15</b>. ($10.17 is what a card would pay.)" % he))
    n, he, his = P.next()
    t = with_tax(15)
    assert t == D("16.95") and 20 - t == D("3.05")
    its.append(mq("%s buys a $15 hockey puck set. 13%% HST is added. %s pays cash with a $20 bill. How much change does %s get?" % (n, cap(he), he),
                  D("3.05"), [D(5), D("3.95"), D("4.87")],
                  "HST: 15 × 13¢ = $1.95. Total: $16.95 (already ends in 5¢). Change: $20.00 − $16.95 = <b>$3.05</b>. "
                  "($5.00 forgets the HST; $4.87 subtracts 13¢ instead of 13%.)"))
    n, he, his = P.next()
    t = with_tax(22)
    assert t == D("24.86") and 25 - t == D("0.14")
    its.append(mcq("%s has $25 in %s bank account. %s wants a $22 game, and 13%% HST is added. %s will pay by debit card. Can %s buy it?"
                   % (n, his, cap(he), cap(he), he),
                   "Yes, with 14¢ left", ["No, %s is $10 short" % he, "Yes, with $3 left", "No, %s is 14¢ short" % he],
                   "HST: 22 × 13¢ = $2.86. Total: $22 + $2.86 = $24.86. $25.00 − $24.86 = $0.14, so <b>yes, with 14¢ left</b>. "
                   "($3 left forgets the HST; $10 short adds $13.)"))
    assert len(its) == 20
    return {"title": "Adding 13% HST", "items": its}


# ============================================================ set 3: budgets
def weeks(goal, per):
    q = F(str(D(goal))) / F(str(D(per)))
    return -(-q.numerator // q.denominator)


def wk(n):
    return "%d week%s" % (n, "" if n == 1 else "s")


def set_budget(P):
    its = []
    its.append(mcq("What is a budget?", "A plan for how to earn, spend and save money",
                   ["A list of things you want", "The money in your piggy bank", "A receipt from a store"],
                   "A budget is <b>a plan</b>. It shows the money coming in and how you plan to spend and save it."))
    its.append(mcq("In a budget, which of these is money coming in?",
                   "Pay for walking a dog", ["A movie ticket", "Money put into savings", "A snack at recess"],
                   "Money coming in is money you get or earn, like an allowance or <b>pay for walking a dog</b>. "
                   "The others are money going out."))
    its.append(mcq("A budget lists needs and wants. Which is a need?",
                   "A warm winter coat", ["A new video game", "A concert ticket", "A second pair of sneakers"],
                   "A need is something you must have to stay safe and healthy. In a Canadian winter, "
                   "<b>a warm winter coat</b> is a need. The others are wants."))
    n, he, his = P.next()
    its.append(mq("%s gets a $10 allowance each week. %s puts $4 into savings. How much is left to spend?" % (n, cap(he)),
                  D(6), [D(14), D(4), D(40)],
                  "$10 − $4 = <b>$6</b>. ($14 adds instead of subtracting; $4 is the part saved.)"))
    n, he, his = P.next()
    its.append(mq("%s saves $5 each week. How much has %s saved after 8 weeks?" % (n, he),
                  D(40), [D(13), D(35), D(45)],
                  "8 × $5 = <b>$40</b>. ($13 adds 8 + 5 instead of multiplying.)"))
    n, he, his = P.next()
    assert weeks(60, 6) == 10
    its.append(mcq("%s wants a $60 pair of skates. %s saves $6 each week. How many weeks will it take?" % (n, cap(he)),
                   wk(10), [wk(54), wk(66), wk(9)],
                   "$60 ÷ $6 = <b>10 weeks</b>. Check: 10 × $6 = $60. (54 subtracts $60 − $6.)"))
    n, he, his = P.next()
    assert weeks(45, 10) == 5
    its.append(mcq("%s wants a $45 book set. %s saves $10 each week. How many weeks until %s has enough?" % (n, cap(he), he),
                   wk(5), [wk(4), "4.5 weeks", wk(35)],
                   "After 4 weeks %s has $40, which is not enough. After 5 weeks %s has $50. "
                   "So it takes <b>5 weeks</b>. Always round up the weeks." % (he, he)))
    n, he, his = P.next()
    bi, bo = [("Allowance", D(15)), ("Raking leaves", D(10))], [("Snacks", D(5)), ("Movie", D(8)), ("Savings", D(7))]
    left = sum(b for a, b in bi) - sum(b for a, b in bo)
    assert left == 5
    its.append(mq(fig(budget_svg("%s’s budget for October" % n, bi, bo)) +
                  "How much of %s’s money is not planned for yet?" % n,
                  left, [D(12), D(45), D(20)],
                  "Money in: $15 + $10 = $25. Money out: $5 + $8 + $7 = $20. $25 − $20 = <b>$5</b>. "
                  "($12 forgets that savings is planned money too.)"))
    n, he, his = P.next()
    bi, bo = [("Allowance", D(20)), ("Shovelling snow", D(10))], [("Hockey tape", D(12)), ("Snacks", D(8)), ("Savings", D(10))]
    assert sum(b for a, b in bi) == sum(b for a, b in bo) == 30
    its.append(mcq(fig(budget_svg("%s’s budget for January" % n, bi, bo)) + "Is %s’s budget balanced?" % n,
                   "Yes, money in equals money out", ["No, %s has $10 left over" % he, "No, %s plans $10 too much" % he,
                                                      "No, savings is not money out"],
                   "Money in: $20 + $10 = $30. Money out: $12 + $8 + $10 = $30. They are equal, so <b>the budget is balanced</b>."))
    n, he, his = P.next()
    bi, bo = [("Allowance", D(20))], [("Swim lessons", D(9)), ("Art supplies", D(7)), ("Savings", D(8))]
    assert sum(b for a, b in bo) - 20 == 4
    its.append(mcq(fig(budget_svg("%s’s budget for April" % n, bi, bo)) + "Is %s’s budget balanced?" % n,
                   "No, %s plans $4 more than %s has" % (he, he),
                   ["Yes, it is balanced", "No, %s has $4 left over" % he, "No, %s plans $24 more than %s has" % (he, he)],
                   "Money out: $9 + $7 + $8 = $24. Money in: $20. $24 − $20 = $4, so <b>%s plans $4 more than %s has</b>. "
                   "%s could save $4 instead of $8." % (he, he, cap(he))))
    n, he, his = P.next()
    its.append(mq("%s earns $8 an hour babysitting. How much does %s earn in 3 hours?" % (n, he),
                  D(24), [D(11), D(16), D(32)],
                  "3 × $8 = <b>$24</b>. ($11 adds instead of multiplying.)"))
    n, he, his = P.next()
    assert 30 * D("0.50") == 15 and 15 - 6 == 9
    its.append(mq("%s sells 30 cups of lemonade at $0.50 each. Lemons and cups cost %s $6. How much money does %s make after paying for them?"
                  % (n, "her" if he == "she" else "him", he),
                  D(9), [D(15), D(21), D(24)],
                  "Sales: 30 × 50¢ = $15. After costs: $15 − $6 = <b>$9</b>. ($15 forgets the costs.)"))
    n, he, his = P.next()
    its.append(mq("%s earns $24 and splits it equally into three jars: save, spend and share. How much goes in each jar?" % n,
                  D(8), [D(12), D(21), D(72)],
                  "$24 ÷ 3 = <b>$8</b>. Check: $8 + $8 + $8 = $24. ($12 splits into 2 jars.)"))
    n, he, his = P.next()
    its.append(mq("%s gets a $5 allowance each week. How much does %s get in 4 weeks?" % (n, he),
                  D(20), [D(9), D(25), D(15)],
                  "4 × $5 = <b>$20</b>."))
    n, he, his = P.next()
    assert 50 - 32 - D("9.50") == D("8.50")
    its.append(mq("A class has $50 for a party. Pizza costs $32 and drinks cost $9.50. How much money is left?",
                  D("8.50"), [D(18), D("41.50"), D("9.50")],
                  "Spent: $32.00 + $9.50 = $41.50. Left: $50.00 − $41.50 = <b>$8.50</b>. ($18 forgets the drinks.)"))
    n, he, his = P.next()
    its.append(mcq("%s’s budget plans $3 more than %s has. Which change would balance it?" % (n, he),
                   "Spend $3 less on snacks", ["Spend $3 more on games", "Save $3 more", "Add a $3 movie"],
                   "To balance, money out must go <b>down</b> by $3. Spending $3 less on snacks does that. "
                   "The other choices make money out even bigger."))
    n, he, his = P.next()
    assert weeks(120 - 40, 20) == 4 and weeks(120, 20) == 6
    its.append(mcq("%s needs $120 for a hockey tournament. %s already has $40 and saves $20 each week. How many more weeks until %s has enough?"
                   % (n, cap(he), he), wk(4), [wk(6), wk(8), wk(3)],
                   "Still needed: $120 − $40 = $80. $80 ÷ $20 = <b>4 weeks</b>. (6 weeks forgets the $40 already saved.)"))
    n, he, his = P.next()
    its.append(mcq("%s earns $12 for each lawn %s mows. How many lawns must %s mow to earn $60?" % (n, he, he),
                   "5 lawns", ["48 lawns", "72 lawns", "6 lawns"],
                   "$60 ÷ $12 = <b>5 lawns</b>. Check: 5 × $12 = $60. (48 subtracts $60 − $12.)"))
    n, he, his = P.next()
    assert 4 * 10 == 40 and 15 * 3 == 45
    its.append(mcq("Plan A: save $4 a week for 10 weeks. Plan B: save $15 a month for 3 months. Which plan saves more, and by how much?",
                   "Plan B, by $5", ["Plan A, by $5", "Plan B, by $11", "They save the same"],
                   "Plan A: 10 × $4 = $40. Plan B: 3 × $15 = $45. $45 − $40 = $5, so <b>Plan B saves $5 more</b>."))
    n, he, his = P.next()
    assert D(18) + D("7.50") + 10 == D("35.50") and 40 - D("35.50") == D("4.50")
    its.append(mq("%s has $40 for a March Break week. %s plans $18 for a trip to the science centre, $7.50 for snacks and $10 for savings. "
                  "How much is not planned for yet?" % (n, cap(he)),
                  D("4.50"), [D("14.50"), D("5.50"), D("35.50")],
                  "Planned: $18.00 + $7.50 + $10.00 = $35.50. Left: $40.00 − $35.50 = <b>$4.50</b>. "
                  "($14.50 forgets the savings; $35.50 is the planned money.)"))
    assert len(its) == 20
    return {"title": "Simple budgets", "items": its}


# ============================================================ set 4: unit price and best buy
def set_unit(P):
    its = []
    its.append(mcq("A shelf tag shows “$0.60 per 100 g”. What does this unit price tell you?",
                   "The cost of 100 g of the food", ["The cost of the whole package", "The tax on the food",
                                                     "How many grams are in the package"],
                   "A unit price is the price for one unit, here <b>100 g</b>. It lets you compare packages of different sizes."))
    its.append(mq("A pack of 4 muffins costs $6.00. What is the price for 1 muffin?",
                  D("1.50"), [D(24), D(2), D(10)],
                  "Divide the price by the number of muffins: $6.00 ÷ 4 = <b>$1.50</b>. Check: 4 × $1.50 = $6.00. "
                  "($24 multiplies instead of dividing.)"))
    its.append(mq("A pack of 6 juice boxes costs $4.20. What is the price for 1 juice box?",
                  D("0.70"), [D("25.20"), D(7), D("0.07")],
                  "$4.20 ÷ 6 = <b>$0.70</b> (70¢). Check: 6 × $0.70 = $4.20. ($7.00 and $0.07 put the decimal point in the wrong place.)"))
    its.append(mq("A 3 kg bag of apples costs $6.60. What is the price per kilogram?",
                  D("2.20"), [D("19.80"), D("3.60"), D(22)],
                  "$6.60 ÷ 3 = <b>$2.20</b> per kilogram. Check: 3 × $2.20 = $6.60. ($3.60 subtracts 3 instead of dividing.)"))
    its.append(unit_item("A 2 L bottle of apple juice costs $3.80. What is the price per litre?", "3.80", 2, 1,
                         ("1 L", "2 L", "per litre")))
    its.append(unit_item("A 500 g bag of pasta costs $4.00. What is the price per 100 g?", "4.00", 500, 100,
                         ("100 g", "500 g", "per 100 g")))
    its.append(mcq("Two bags of rice are different sizes. What should you compare to find the better buy?",
                   "The price per 100 g", ["The total prices", "The sizes of the bags", "The colours of the bags"],
                   "A bigger bag usually costs more in total, so totals do not tell you which is cheaper. "
                   "Compare <b>the price for the same amount</b>, such as per 100 g."))
    its.append(best_item("Which pack of granola bars is the better buy?",
                         [("Pack A", 4, "4 bars", "3.00"), ("Pack B", 6, "6 bars", "4.20")], "per bar", 1, figure=True,
                         cant="You cannot compare different packs"))
    its.append(best_item("Which bag of carrots is the better buy?",
                         [("Bag A", 1, "1 kg", "2.40"), ("Bag B", 2, "2 kg", "4.40")], "per kilogram", 1, figure=True))
    its.append(best_item("Which bottle of orange juice is the better buy?",
                         [("Bottle A", 1, "1 L", "2.50"), ("Bottle B", 2, "2 L", "5.00")], "per litre", 1, figure=True))
    its.append(best_item("Which box of crackers is the better buy?",
                         [("Box A", 300, "300 g", "3.60"), ("Box B", 500, "500 g", "6.50")], "per 100 g", 100, figure=True,
                         note="A bigger box is not always the better buy."))
    its.append(best_item("A pack of 10 pencils costs $2.50. A pack of 12 pencils costs $2.88. Which is the better buy?",
                         [("The pack of 10", 10, "10 pencils", "2.50"), ("The pack of 12", 12, "12 pencils", "2.88")], "per pencil", 1,
                         cant="You cannot compare different packs"))
    assert D(6) / 4 * 10 == 15
    its.append(mq("4 muffins cost $6.00. At the same price, how much do 10 muffins cost?",
                  D(15), [D(12), D(60), D(10)],
                  "Unit price: $6.00 ÷ 4 = $1.50 each. 10 muffins: 10 × $1.50 = <b>$15.00</b>. "
                  "($12 adds $6 for 6 more muffins instead of $1.50 each.)"))
    assert D("8.25") / 3 == D("2.75")
    its.append(mq("A pack of 3 rolls of hockey tape costs $8.25. What is the price for 1 roll?",
                  D("2.75"), [D("24.75"), D("5.25"), D("2.25")],
                  "$8.25 ÷ 3 = <b>$2.75</b>. Check: 3 × $2.75 = $8.25. ($5.25 subtracts 3 instead of dividing.)"))
    its.append(best_item("Which milk is the best buy?",
                         [("Milk A", 1, "1 L", "2.30"), ("Milk B", 2, "2 L", "4.40"), ("Milk C", 4, "4 L", "6.40")],
                         "per litre", 1, figure=True))
    n, he, his = P.next()
    assert D(8) / 5 == D("1.60") and D(4) / 2 == 2
    its.append(mcq("A 2 kg bag of potatoes costs $4. A 5 kg bag costs $8. %s says the 2 kg bag is the better buy because it costs less. "
                   "Is %s right?" % (n, he),
                   "No, the 5 kg bag costs less per kilogram", ["Yes, it costs less in total", "Yes, smaller bags always cost less",
                                                               "No, they cost the same per kilogram"],
                   "Compare unit prices, not totals. 2 kg bag: $4 ÷ 2 = $2.00 per kg. 5 kg bag: $8 ÷ 5 = $1.60 per kg. "
                   "<b>The 5 kg bag costs less per kilogram</b>, so it is the better buy if you will use it all."))
    n, he, his = P.next()
    its.append(mq("%s earns $36 for 4 hours of babysitting. What is %s pay for 1 hour?" % (n, his),
                  D(9), [D(144), D(32), D(40)],
                  "This is a unit rate: $36 ÷ 4 = <b>$9 per hour</b>. Check: 4 × $9 = $36."))
    assert 2 * D(6) - 11 == 1
    its.append(mcq("A 250 mL bottle of maple syrup costs $6.00. A 500 mL bottle costs $11.00. Which is the better buy?",
                   "The 500 mL bottle", ["The 250 mL bottle", "They cost the same for 500 mL", "You cannot compare different bottles"],
                   "Compare the same amount. Two 250 mL bottles make 500 mL and cost 2 × $6.00 = $12.00. "
                   "The 500 mL bottle costs $11.00, which is $1.00 less for the same amount, so <b>the 500 mL bottle</b> is the better buy. "
                   "(The 250 mL bottle has the lower total price, but you get less.)"))
    its.append(best_item("Which bag of rice is the best buy?",
                         [("Bag A", 1, "1 kg", "3.20"), ("Bag B", 2, "2 kg", "5.80"), ("Bag C", 5, "5 kg", "15.50")],
                         "per kilogram", 1, figure=True, note="The biggest bag is not always the best buy."))
    n, he, his = P.next()
    assert 12 * D("0.85") - 2 * D("4.20") == D("1.80")
    its.append(mq("%s needs 12 juice boxes. Single juice boxes cost $0.85 each. A pack of 6 costs $4.20. "
                  "How much does %s save by buying 2 packs instead of 12 single boxes?" % (n, he),
                  D("1.80"), [D("0.15"), D("10.20"), D("8.40")],
                  "12 single boxes: 12 × $0.85 = $10.20. 2 packs: 2 × $4.20 = $8.40. Savings: $10.20 − $8.40 = <b>$1.80</b>. "
                  "($0.15 is the saving on only 1 box.)"))
    assert len(its) == 20
    return {"title": "Unit price and the best buy", "items": its}


# ============================================================ set 5: credit, debt and taxes
def set_credit(P):
    its = []
    its.append(mcq("What does it mean to buy something on credit?",
                   "You borrow money now and pay it back later", ["You pay with coins and bills", "You get it for free",
                                                                  "You use money you have already saved"],
                   "Buying on credit means <b>borrowing</b>. The lender pays now, and you must pay the money back later."))
    its.append(mcq("What is debt?",
                   "Money that you owe", ["Money that you saved", "Money that you earned", "Money that you gave away"],
                   "When you borrow money, the amount you still have to pay back is your <b>debt</b>: money that you owe."))
    its.append(mcq("What is interest on a loan?",
                   "Extra money you pay for borrowing", ["Money taken off the price", "The tax added at the store",
                                                         "Money that you earn at a job"],
                   "Lenders charge <b>interest</b>: extra money you pay for using their money. "
                   "The longer you take to pay back, the more interest you usually pay."))
    n, he, his = P.next()
    its.append(mq("%s’s family borrows $100. The interest is 10%% for one year. How much is the interest?" % n,
                  D(10), [D(110), D(1), D(90)],
                  "10% means $10 for every $100. So the interest is <b>$10</b>. ($110 is the total to pay back.)"))
    its.append(mq("A family borrows $200 and pays 10% interest after one year. How much do they pay back in all?",
                  D(220), [D(210), D(200), D(20)],
                  "Interest: 10% of $200 = $20. Pay back: $200 + $20 = <b>$220</b>. ($200 forgets the interest; $210 adds $10 instead of 10%.)"))
    n, he, his = P.next()
    its.append(mq("%s’s mom has a credit card bill of $80. She pays $30. How much debt is left on the card?" % n,
                  D(50), [D(110), D(30), D(80)],
                  "$80 − $30 = <b>$50</b> is still owed. Interest may be added to it next month."))
    its.append(mcq("A credit card bill is $60. It is paid in full by the due date. How much interest is added?",
                   "$0, no interest", ["$6", "$60", "$13"],
                   "When a credit card bill is <b>paid in full by the due date</b>, there is usually no interest. "
                   "Interest is added to money that is not paid back on time."))
    its.append(mcq("Two loans are both $200. Loan A has 5% interest. Loan B has 10% interest. Which costs more, and by how much?",
                   "Loan B, by $10", ["Loan A, by $10", "Loan B, by $5", "They cost the same"],
                   "Loan A: 5% of $200 = $10. Loan B: 10% of $200 = $20. $20 − $10 = $10, so <b>Loan B costs $10 more</b>. "
                   "A higher interest rate means you owe more."))
    n, he, his = P.next()
    its.append(mcq("%s borrows $60 from %s sister to buy a ticket. %s pays her back $5 each week. How many weeks will it take?" % (n, his, cap(he)),
                   wk(12), [wk(55), wk(65), wk(11)],
                   "$60 ÷ $5 = <b>12 weeks</b>. Check: 12 × $5 = $60. (55 subtracts $60 − $5.)"))
    n, he, his = P.next()
    assert 50 + 5 == 55 and 55 // 11 == 5
    its.append(mcq("%s borrows $50 and must pay back 10%% extra. %s pays $11 each week. How many weeks will it take to pay it all back?" % (n, cap(he)),
                   wk(5), [wk(4), wk(6), wk(55)],
                   "Extra: 10%% of $50 = $5, so %s owes $55. $55 ÷ $11 = <b>5 weeks</b>. "
                   "(After 4 weeks %s has paid only $44.)" % (he, he)))
    its.append(mcq("Who collects the 13% HST that is added to prices in Ontario?",
                   "The federal and provincial governments", ["The store keeps it", "Only the city", "The school board"],
                   "The store collects HST and sends it to the government. Part goes to the <b>federal government</b> "
                   "(Government of Canada) and part to the <b>province of Ontario</b>."))
    its.append(mcq("Cities and towns collect a tax from people who own homes and land. What is this tax called?",
                   "Property tax", ["Sales tax", "Income tax", "Interest"],
                   "<b>Property tax</b> is paid on homes and land. It helps pay for city services such as "
                   "garbage pickup, parks, libraries and snow plowing."))
    its.append(mcq("Which service does the Ontario government pay for with tax money?",
                   "Public schools and hospitals", ["Garbage pickup", "Canada’s armed forces", "A family’s groceries"],
                   "Provinces pay for <b>schools and hospitals</b>. Garbage pickup is a city service. "
                   "The armed forces are paid for by the federal government."))
    its.append(mcq("Which service does the federal government (Government of Canada) pay for with tax money?",
                   "Canada’s armed forces", ["The local library", "Public schools", "Garbage pickup"],
                   "The federal government pays for things for the whole country, like <b>Canada’s armed forces</b>. "
                   "Libraries and garbage pickup are city services, and schools are provincial."))
    its.append(mcq("Income tax is a tax on what?",
                   "The money people earn", ["The things people buy", "Homes and land", "Money people borrow"],
                   "<b>Income tax</b> is taken from the money people earn at their jobs. "
                   "Tax on things you buy is sales tax (HST). Tax on homes and land is property tax."))
    assert D(100) * D("0.08") == 8
    its.append(mq("Ontario’s 13% HST has two parts: 5% goes to the federal government and 8% goes to the province. "
                  "On a $100 item, how much HST goes to the province?",
                  D(8), [D(5), D(13), D(108)],
                  "8% of $100 = <b>$8</b>. The other $5 goes to the federal government. $8 + $5 = $13, the full HST."))
    assert 24000 + 18500 == 42500
    its.append(mcq("A town uses property tax to pay $24%s000 for a new playground and $18%s500 for snow plowing. How much is that in all?" % (" ", " "),
                   "$" + big(42500), ["$" + big(32500), "$" + big(5500), "$" + big(42000)],
                   "$%s + $%s = <b>$%s</b>. ($%s forgets to carry the 1 into the ten thousands; $5500 subtracts.)"
                   % (big(24000), big(18500), big(42500), big(32500))))
    n, he, his = P.next()
    assert 300 + 30 == 330
    its.append(mq("%s’s dad buys a $300 bike on credit. He does not pay the bill on time, so 10%% interest is added. How much does he owe now?" % n,
                  D(330), [D(310), D(30), D(270)],
                  "Interest: 10% of $300 = $30. He owes $300 + $30 = <b>$330</b>. ($310 adds $10 instead of 10%; "
                  "$270 subtracts the interest.)"))
    assert 10 * 10 - 90 == 10
    its.append(mcq("A tablet costs $90 if you pay now. Or you can pay $10 a month for 10 months. How much more does paying monthly cost?",
                   "$10 more", ["$0, they are the same", "$100 more", "$80 more"],
                   "Monthly: 10 × $10 = $100. $100 − $90 = <b>$10 more</b>. Paying over time often costs extra, like interest."))
    n, he, his = P.next()
    assert tax(40) == D("5.20") and tax(30) == D("3.90")
    its.append(mq("%s buys a $30 sweater and a $10 hat. 13%% HST is added. How much of %s total is tax?" % (n, his),
                  D("5.20"), [D(13), D("3.90"), D("45.20")],
                  "Price before tax: $30 + $10 = $40. HST: 40 × 13¢ = <b>$5.20</b>. "
                  "($3.90 taxes only the sweater; $45.20 is the whole total.)"))
    assert len(its) == 20
    return {"title": "Credit, debt and taxes word problems", "items": its}


# ============================================================ lesson
def body_html():
    items = [("Sandwich", D("4.75")), ("Apple", D("0.89")), ("Milk", D("1.65"))]
    t = sum(p for n, p in items)
    assert t == D("7.29") and cash(t) == D("7.30") and 10 - D("7.30") == D("2.70")
    assert with_tax(20) == D("22.60") and tax(30) == D("3.90") and D(4) / 5 == D("0.80") and D(6) / 8 == D("0.75")
    return (
        "<h2>Total cost and change</h2>"
        "<p>To find the total, line up the decimal points and add. To estimate first, round each price to the nearest dollar.</p>"
        "<p>Canada has no pennies. When you pay with <b>cash</b>, the total is rounded to the nearest 5¢: "
        "totals ending in 1, 2, 6 or 7 cents round down; 3, 4, 8 or 9 round up. Card payments are exact.</p>"
        "<figure class='sn-fig'>" + receipt_svg("Lunch", items, ("Total", money(t))) +
        "<figcaption>Estimate: $5 + $1 + $2 = about $8. Exact total: $7.29.</figcaption></figure>" +
        ex("Example", "You pay the $7.29 lunch bill with cash and a $10 bill. How much change do you get?",
           "Round the cash total: $7.29 → $7.30. Count up: $7.30 → $7.50 → $8.00 → $10.00 is 20¢ + 50¢ + $2.00.",
           "$2.70") +
        "<h2>Adding 13% HST</h2>"
        "<p>In Ontario, 13% HST (sales tax) is added to most things you buy. 13% means <b>13¢ for every $1</b>. "
        "A quick way: 10% plus 3%.</p>" +
        ex("Example", "A $20 puzzle has 13% HST added. What is the total?",
           "HST: 20 × 13¢ = $2.60. Total: $20.00 + $2.60 = $22.60.", "$22.60") +
        ex("Example", "Find 13% of $30.", "10% of $30 = $3.00. 3% of $30 = $0.90. $3.00 + $0.90 = $3.90.", "$3.90") +
        "<h2>Budgets</h2>"
        "<p>A budget is a plan for money coming in (allowance, jobs) and money going out (spending and saving). "
        "It is <b>balanced</b> when money in equals money out.</p>"
        "<figure class='sn-fig'>" + budget_svg("A budget for May", [("Allowance", D(20)), ("Dog walking", D(10))],
                                               [("Swimming", D(12)), ("Snacks", D(6)), ("Savings", D(12))]) +
        "<figcaption>Money in: $20 + $10 = $30. Money out: $12 + $6 + $12 = $30. The budget is balanced.</figcaption></figure>"
        "<h2>Unit price: find the best buy</h2>"
        "<p>A bigger package usually costs more, so compare the <b>unit price</b>: the cost of 1 item, 1 kg, 1 L or 100 g. "
        "The lower unit price is the better buy.</p>"
        "<figure class='sn-fig'>" + tags_svg([("Box A", "5 bars", D("4.00")), ("Box B", "8 bars", D("6.00"))]) +
        "<figcaption>Box A: $4.00 ÷ 5 = $0.80 per bar. Box B: $6.00 ÷ 8 = $0.75 per bar. Box B is the better buy, "
        "even though it costs more.</figcaption></figure>"
        "<h2>Credit, debt and interest</h2>"
        "<p>Buying on <b>credit</b> means borrowing money and paying it back later. The money you owe is <b>debt</b>. "
        "Lenders add <b>interest</b>, extra money for borrowing. Borrow $100 at 10% interest for a year and you pay back $110. "
        "A higher interest rate means you owe more.</p>"
        "<h2>Taxes pay for services</h2>" +
        table(["Government", "Taxes it collects", "Services it pays for"], [
            ["Federal (Canada)", "Income tax, the 5% part of HST", "Armed forces, passports"],
            ["Provincial (Ontario)", "Income tax, the 8% part of HST", "Schools, hospitals, highways"],
            ["Municipal (city or town)", "Property tax", "Garbage pickup, parks, libraries, snow plowing"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Adding $13 instead of 13% ($20 → $33)", "13% is 13¢ for every $1: $20 → $2.60 tax"],
            ["Giving only the tax as the total", "Add the HST to the price: $20 + $2.60 = $22.60"],
            ["Picking the package with the lower total price", "Compare the price per item, per kg or per 100 g"],
            ["Forgetting to round a cash total", "Cash rounds to the nearest 5¢; cards do not"],
            ["Rounding the weeks down ($45 ÷ $10 = 4.5 → 4)", "Round up: after 4 weeks you are still short"],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn in financial literacy in Ontario?",
     "a": "Grade 5 students find the total cost of several items, including 13% HST, design simple budgets, compare unit prices "
          "to find the best buy, learn about credit, debt and interest, and learn how taxes pay for community services."},
    {"q": "How do you add 13% HST to a price?",
     "a": "HST is 13¢ for every $1, so multiply the dollars by 13¢ and add it to the price. A $20 item has $2.60 HST, for a total of $22.60."},
    {"q": "How do you round a cash total in Canada without pennies?",
     "a": "Round to the nearest 5¢: totals ending in 1, 2, 6 or 7 cents round down, and 3, 4, 8 or 9 round up. "
          "Debit and credit card payments are not rounded."},
    {"q": "How do you explain credit, debt and interest to a Grade 5 student?",
     "a": "Credit means borrowing money now and paying it back later, and debt is the money you still owe. "
          "Interest is the extra money you pay for borrowing, so $100 borrowed at 10% for a year costs $110 to pay back."},
]


def verify(sets):
    for s in sets:
        for it in s["items"]:
            right = it["c"][it["a"]]
            if "with cash" in it["q"] and right.startswith("$") and "change" not in it["q"]:
                assert int(D(right[1:]) * 100) % 5 == 0, it["q"]


def gen():
    rnd = random.Random(45820)
    P = People(rnd)
    sets = [set_total(P), set_hst(P), set_budget(P), set_unit(P), set_credit(P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-5", "slug": "financial-literacy", "sort": 20,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 5 Financial Literacy: Total Cost, 13% HST, Budgets and Best Buys",
        "seo_title": "Grade 5 Financial Literacy Math Worksheets: Total Cost, HST, Budgets and Unit Price (Free, Answer Key)",
        "short_title": "Financial Literacy",
        "domain": "Financial Literacy",
        "standard_code": "Grade 5: F1.2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Estimate and calculate the cost of transactions involving multiple items priced in dollars and cents, "
                         "including sales tax, using various strategies",
        "meta_desc": "Free Grade 5 financial literacy math worksheets for the Ontario curriculum: total cost and change with cash "
                     "rounding, adding 13% HST, simple budgets, unit price and the best buy, and credit, debt, interest and taxes. "
                     "100 questions with an answer key.",
        "key_big": "HST is 13¢ for every $1, and the best buy has the lowest unit price.",
        "key_sub": "Add the tax to the price: a $20 item costs $22.60. Compare the price per item or per kilogram, not the total. "
                   "Cash totals round to the nearest 5¢; card payments are exact.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "Shelf tags: [^;']*;[^;']*;")
    mark_large(u, "Budget ")
    mark_large(u, "Receipt ")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
