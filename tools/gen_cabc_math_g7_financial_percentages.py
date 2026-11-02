# -*- coding: utf-8 -*-
"""
BC Grade 7 Math: Financial Percentages (BC Mathematics Curriculum, Financial literacy: financial percentage)
  python3 tools/gen_cabc_math_g7_financial_percentages.py
Percent of an amount, discounts and sale prices, BC sales tax (GST 5% + PST 7%), tips, simple interest (I = Prt),
best buys and budgets. All money is worked with decimal.Decimal; each tax is rounded to the cent (half up, and no
price is used whose GST or PST ends in exactly half a cent). Canada has no pennies: cash totals round to the nearest
5 cents, card payments are exact. BC style: 4-digit numbers without a separator, $ and the cent sign.
Helpers are copied from gen_caon_math_g6_financial.py. HTML attributes use single quotes.
"""
import json, os, random, re
from decimal import Decimal as D, ROUND_HALF_UP
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-7")
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


def rtax(p, rate):
    """A tax (rate in percent) rounded to the cent. Prices whose tax ends in exactly half a cent are not used."""
    p = D(p)
    assert (p * 100 * rate) % 100 != 50, (p, rate)
    return (p * D(rate) / 100).quantize(CENT, rounding=ROUND_HALF_UP)


def gst(p):
    return rtax(p, 5)


def pst(p):
    return rtax(p, 7)


def both(p):
    """GST + PST, each rounded; the same as 12% rounded for every price used here."""
    t = gst(p) + pst(p)
    assert t == rtax(p, 12), p
    return t


def pct(p, r):
    """Exact r% of p (must be whole cents)."""
    x = D(p) * D(r) / 100
    assert x == x.quantize(CENT), (p, r)
    return x


def cash(d):
    c = int(D(d) * 100)
    assert D(c) / 100 == D(d)
    return D((c + 2) // 5 * 5) / 100


def cap(s):
    return s[0].upper() + s[1:]


def rawtxt(x):
    x = D(x)
    return money(x) if x == x.quantize(CENT) else "$" + format(x.normalize(), "f")


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
def bar_svg(total, r, part_label=None):
    """Percent bar: 0% to 100% on top, $0 to the total below, the r% part shaded."""
    W, L, R = 420, 30, 390
    y0, h = 34, 34
    x = L + (R - L) * r / 100
    s = [
        "<rect x='%d' y='%d' width='%s' height='%d' fill='%s'/>" % (L, y0, x - L, h, LIGHT),
        "<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>" % (L, y0, R - L, h, GREEN),
        "<line x1='%s' y1='%d' x2='%s' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y0 - 6, x, y0 + h + 6, GREEN),
        txt(L, y0 - 10, "0%", 15), txt(x, y0 - 10, "%d%%" % r, 15, bold=True), txt(R, y0 - 10, "100%", 15),
        txt(L, y0 + h + 22, "$0", 15), txt(x, y0 + h + 22, part_label or "?", 15, bold=True, col=GREEN),
        txt(R, y0 + h + 22, money(total), 15),
    ]
    label = "Percent bar: %d%% of %s" % (r, money(total))
    return svg_wrap(W, y0 + h + 30, "".join(s), label)


def sale_tag_svg(price, off):
    """A sale tag: the regular price and the percent off."""
    W, H = 200, 110
    s = [
        "<path d='M30 4 H192 a6 6 0 0 1 6 6 V100 a6 6 0 0 1 -6 6 H30 L4 55 Z' fill='%s' stroke='%s' stroke-width='2'/>" % (PAPER, RED),
        "<circle cx='26' cy='55' r='6' fill='#ffffff' stroke='%s' stroke-width='2'/>" % RED,
        txt(115, 34, "Regular " + money(price), 17),
        txt(115, 80, "%d%% OFF" % off, 30, bold=True, col=RED),
    ]
    return svg_wrap(W + 2, H + 2, "".join(s), "Sale tag: regular price %s, %d%% off" % (money(price), off))


def receipt_svg(items, rows, title="Receipt"):
    """items = [(name, price)]; rows = [(label, value_text)] printed under the line."""
    W, rh = 280, 24
    s = [txt(W // 2, 22, title, 17, bold=True)]
    y = 48
    for name, p in items:
        s.append(txt(14, y, name, 16, "start"))
        s.append(txt(W - 14, y, money(p), 16, "end"))
        y += rh
    s.append("<line x1='10' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5' stroke-dasharray='4 3'/>" % (y - 14, W - 10, y - 14, GREY))
    y += 6
    for i, (lab, val) in enumerate(rows):
        last = i == len(rows) - 1
        s.append(txt(14, y, lab, 16, "start", bold=last))
        s.append(txt(W - 14, y, val, 16, "end", bold=last, col=GREEN if val == "?" else INK))
        y += rh
    s.insert(0, "<rect x='2' y='2' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (W - 4, y - 12, PAPER, EDGE))
    label = "Receipt: " + ", ".join("%s %s" % (n, money(p)) for n, p in items) + "; " + ", ".join("%s %s" % r for r in rows)
    return svg_wrap(W, y - 8, "".join(s), label)


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


def budget_svg(title, money_in, money_out):
    W, rh, fs = 300, 25, 16
    s = []
    y = 26
    s.append(txt(W // 2, y - 6, title, 17, bold=True))
    rows = [("Money in", None, "h")] + [(a, b, "r") for a, b in money_in] + [("Money out", None, "h")] + [(a, b, "r") for a, b in money_out]
    top = y
    for label, amt, kind in rows:
        if kind == "h":
            s.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s'/>" % (y, W - 4, rh, GREEN))
            s.append(txt(12, y + 18, label, fs, "start", bold=True, col="#ffffff"))
        else:
            s.append("<line x1='2' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (y + rh, W - 2, y + rh, EDGE))
            s.append(txt(12, y + 18, label, fs, "start"))
            s.append(txt(W - 12, y + 18, money(amt), fs, "end"))
        y += rh
    s.append("<rect x='2' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>" % (top, W - 4, y - top, EDGE))
    label = "Budget %s. Money in: %s. Money out: %s" % (
        title, ", ".join("%s %s" % (a, money(b)) for a, b in money_in), ", ".join("%s %s" % (a, money(b)) for a, b in money_out))
    return svg_wrap(W, y + 4, "".join(s), label)


# ============================================================ set 1: percent of an amount
def pof(q, p, r, wrongs, e, figure=None):
    ans = pct(p, r)
    if figure:
        q = fig(figure) + q
    return mq(q, ans, wrongs, e)


def set_percent(P):
    its = []
    its.append(pof("What is 10% of $60?", 60, 10, [D(50), D(10), D("0.60")],
                   "10% = 10 out of 100 = one tenth. $60 ÷ 10 = <b>$6</b>. ($50 subtracts 10 from 60; 10% is not $10.)"))
    its.append(pof("What is 50% of $37?", 37, 50, [D("7.40"), D(74), D(13)],
                   "50% is one half. $37 ÷ 2 = <b>$18.50</b>. ($7.40 divides by 5; $74 doubles instead of halving.)",
                   figure=bar_svg(37, 50)))
    its.append(pof("What is 25% of $48?", 48, 25, [D(23), D(36), D("1.92")],
                   "25% is one quarter. $48 ÷ 4 = <b>$12</b>. ($23 is 48 − 25; $36 is 75%; $1.92 divides by 25.)",
                   figure=bar_svg(48, 25)))
    its.append(pof("What is 1% of $250?", 250, 1, [D(25), D(249), D("0.25")],
                   "1% is one hundredth. $250 ÷ 100 = <b>$2.50</b>. ($25 is 10%; $0.25 is 0.1%; $249 subtracts 1.)"))
    its.append(pof("What is 5% of $80?", 80, 5, [D(8), D(75), D("0.40")],
                   "10% of $80 is $8, and 5% is half of that: <b>$4</b>. ($8 is 10%; $0.40 is 0.5%; $75 subtracts 5 from 80.)"))
    its.append(pof("What is 12% of $50?", 50, 12, [D(12), D(38), D(60)],
                   "12% = 0.12. $50 × 0.12 = <b>$6</b>. Or: 10% is $5 and 2% is $1, so 12% is $6. "
                   "($12 uses the percent as dollars; $60 multiplies by 1.2 instead of 0.12.)"))
    its.append(pof("What is 15% of $40?", 40, 15, [D(25), D(15), D(4)],
                   "10% of $40 is $4 and 5% is $2. 15% = $4 + $2 = <b>$6</b>. ($4 is only 10%; $25 is 40 − 15.)"))
    its.append(pof("What is 20% of $85?", 85, 20, [D(65), D("8.50"), D("4.25")],
                   "10% of $85 is $8.50, so 20% is 2 × $8.50 = <b>$17</b>. ($8.50 is 10%; $4.25 divides by 20.)"))
    its.append(pof("What is 7% of $30?", 30, 7, [D(21), D("0.21"), D(23)],
                   "7% = 0.07. $30 × 0.07 = <b>$2.10</b>. Or: 1% is $0.30, so 7% is 7 × $0.30 = $2.10. "
                   "($21 multiplies by 0.7, which is 70%.)"))
    its.append(mcq("Which calculation finds 12% of a price?", "price × 0.12",
                   ["price × 12", "price ÷ 12", "price − 12"],
                   "Percent means “out of 100”, so 12% = 12 ÷ 100 = 0.12. Multiply: <b>price × 0.12</b>. "
                   "price × 12 is 1200%, and price − 12 takes away $12, not 12%."))
    its.append(pof("What is 75% of $36?", 36, 75, [D(9), D(39), D("0.48")],
                   "25% of $36 is $36 ÷ 4 = $9, so 75% is 3 × $9 = <b>$27</b>. ($9 is only 25%; $39 is 75 − 36.)",
                   figure=bar_svg(36, 75)))
    its.append(pof("What is 30% of $45?", 45, 30, [D(15), D("4.50"), D("1.35")],
                   "10% of $45 is $4.50, so 30% is 3 × $4.50 = <b>$13.50</b>. ($15 is 45 − 30; $4.50 is only 10%.)"))
    its.append(pof("What is 5% of $64?", 64, 5, [D(32), D("6.40"), D(59)],
                   "10% of $64 is $6.40, so 5% is half: <b>$3.20</b>. ($32 is 50%; $6.40 is 10%; $59 subtracts 5 from 64.)"))
    its.append(pof("10% of $70 is $7. Use this to find 5% of $70.", 70, 5, [D(14), D(65), D("0.70")],
                   "5% is half of 10%. $7 ÷ 2 = <b>$3.50</b>. ($14 doubles, which gives 20%; $0.70 is 1%.)"))
    its.append(pof("What is 12% of $25?", 25, 12, [D(12), D(13), D(30)],
                   "10% of $25 is $2.50 and 2% is $0.50. 12% = $2.50 + $0.50 = <b>$3</b>. "
                   "($12 uses the percent as dollars; $13 is 25 − 12.)"))
    n, he, his, him = P.next()
    its.append(mcq("A $40 game is on sale. %s saves $10. What percent of the price does %s save?" % (n, he),
                   "25%", ["10%", "4%", "75%"],
                   "$10 out of $40 = 10/40 = 1/4 = <b>25%</b>. (10% uses the dollars as the percent; 4% comes from 40 ÷ 10; 75% is the part paid.)"))
    its.append(mcq("$9 is what percent of $60?", "15%", ["9%", "51%", "85%"],
                   "$9 ÷ $60 = 0.15 = <b>15%</b>. Check: 10% of $60 is $6 and 5% is $3, so 15% is $9. "
                   "(9% uses the dollars as the percent; 85% is the rest.)"))
    its.append(pof("What is 12% of $75?", 75, 12, [D(12), D(63), D(90)],
                   "10% of $75 is $7.50 and 2% is $1.50. 12% = $7.50 + $1.50 = <b>$9</b>. "
                   "($12 uses the percent as dollars; $90 is 120%.)"))
    its.append(pof("What is 150% of $24?", 24, 150, [D(12), D("3.60"), D(360)],
                   "150% = 100% + 50%. $24 + $12 = <b>$36</b>. ($12 is only 50%; $3.60 is 15%; $360 multiplies by 15.)"))
    its.append(pof("What is 35% of $120?", 120, 35, [D(85), D(12), D("4.20")],
                   "10% of $120 is $12, so 30% is $36 and 5% is $6. 35% = $36 + $6 = <b>$42</b>. "
                   "($85 is 120 − 35; $4.20 is 3.5%.)"))
    assert len(its) == 20
    return {"title": "Percent of an amount", "items": its}


# ============================================================ set 2: discounts and sale prices
def sale(p, r):
    return D(p) - pct(p, r)


def set_discount(P):
    its = []
    its.append(mq(fig(sale_tag_svg(40, 10)) + "A $40 sweater is 10% off. How much is the discount?",
                  D(4), [D(30), D(36), D("0.40")],
                  "10% of $40 = $40 ÷ 10 = <b>$4</b> off. ($36 is the sale price, not the discount; $30 subtracts 10 from 40.)"))
    its.append(mq("A $40 sweater is 10% off. What is the sale price?", sale(40, 10), [D(30), D(4), D(44)],
                  "Discount: 10% of $40 = $4. Sale price: $40 − $4 = <b>$36</b>. ($30 subtracts the percent number, 10.)"))
    its.append(mq(fig(sale_tag_svg(60, 25)) + "What is the sale price of this rain jacket?", sale(60, 25), [D(35), D(15), D(75)],
                  "Discount: 25% of $60 = $60 ÷ 4 = $15. Sale price: $60 − $15 = <b>$45</b>. "
                  "($35 subtracts 25 dollars instead of 25%; $15 is the discount.)"))
    its.append(mq("An $80 pair of hiking boots is 50% off. What is the sale price?", sale(80, 50), [D(30), D(120), D("79.50")],
                  "50% off is half off. $80 ÷ 2 = <b>$40</b>. ($30 subtracts 50 dollars; $79.50 subtracts 50¢; $120 adds 50%.)"))
    its.append(mq("A $35 board game is 20% off. What is the sale price?", sale(35, 20), [D(15), D(7), D(42)],
                  "Discount: 10% is $3.50, so 20% is $7. Sale price: $35 − $7 = <b>$28</b>. ($15 is 35 − 20; $7 is the discount.)"))
    its.append(mcq("Which calculation gives the sale price when an item is 30% off?", "price × 0.70",
                   ["price × 0.30", "price − 30", "price × 1.30"],
                   "30% off means you pay 100% − 30% = 70% of the price, so <b>price × 0.70</b>. "
                   "price × 0.30 gives only the discount."))
    its.append(mq(fig(sale_tag_svg(120, 30)) + "What is the sale price of this snowboard?", sale(120, 30), [D(90), D(36), D(156)],
                  "You pay 70%: $120 × 0.70 = <b>$84</b>. Or: 30% of $120 is $36, and $120 − $36 = $84. ($90 is 120 − 30.)"))
    its.append(mq("A $48 soccer ball is 15% off. What is the sale price?", sale(48, 15), [D(33), D("7.20"), D("55.20")],
                  "Discount: 10% is $4.80 and 5% is $2.40, so 15% is $7.20. Sale price: $48.00 − $7.20 = <b>$40.80</b>. ($33 is 48 − 15.)"))
    its.append(mq("A $65 tent is 40% off. What is the sale price?", sale(65, 40), [D(25), D(26), D(91)],
                  "You pay 60%: $65 × 0.60 = <b>$39</b>. ($25 is 65 − 40; $26 is the discount; $91 adds 40%.)"))
    its.append(mcq("A $90 pair of skates is on sale for $72. What percent is the discount?", "20%", ["18%", "80%", "25%"],
                   "Discount: $90 − $72 = $18. Compare it with the <b>regular</b> price: $18 ÷ $90 = 0.2 = <b>20%</b>. "
                   "(18% uses the dollars; 80% is the part you pay; 25% divides by the sale price.)"))
    its.append(mcq("A $50 pair of running shoes is on sale for $35. What percent is the discount?", "30%", ["15%", "70%", "35%"],
                   "Discount: $50 − $35 = $15. $15 ÷ $50 = 0.3 = <b>30%</b>. (15% uses the dollars; 70% is the part you pay.)"))
    its.append(mcq("A jacket costs $80. Store A takes 25% off. Store B takes $15 off. Which deal is better?",
                   "25% off, by $5", ["$15 off, by $5", "$15 off, by $10", "They are the same"],
                   "25% of $80 = $20 off, so Store A’s price is $60. Store B’s price is $80 − $15 = $65. "
                   "<b>25% off is better by $5</b>. ($15 off by $10 compares 25 with 15, not dollars.)"))
    its.append(mq("A $28 T-shirt is on clearance for 75% off. What is the clearance price?", sale(28, 75), [D(21), D(14), D(35)],
                  "25% of $28 is $7, so 75% off is $21 off. You pay 25%: <b>$7</b>. ($21 is the discount; $14 is 50% off.)"))
    n, he, his, him = P.next()
    its.append(mq("Two $18 T-shirts are on a deal: buy one, get the second one 50% off. How much do the two T-shirts cost before tax?",
                  D(27), [D(18), D(36), D(9)],
                  "First T-shirt: $18. Second T-shirt: 50% of $18 off, so $9. Total: $18 + $9 = <b>$27</b>. ($36 forgets the discount.)"))
    n, he, his, him = P.next()
    assert sale(64, 25) == 48
    its.append(mq("%s has $50. A $64 hoodie is 25%% off. How much money does %s have left after buying it (before tax)?" % (n, he),
                  D(2), [D(11), D(34), D(16)],
                  "Sale price: 25% of $64 is $16, so $64 − $16 = $48. Left: $50 − $48 = <b>$2</b>. "
                  "($11 uses $64 − 25 = $39; $34 subtracts only the discount.)"))
    its.append(mcq("A tent has a regular price of $120. It is on sale for $30 off. What percent off is that?", "25%",
                   ["30%", "4%", "75%"],
                   "$30 ÷ $120 = 1/4 = <b>25%</b>. (30% uses the dollars; 4% comes from 120 ÷ 30; 75% is the part you pay.)"))
    assert sale(sale(100, 20), 10) == 72
    its.append(mq("A $100 winter coat is 20% off. Then the store takes another 10% off the sale price. What is the final price?",
                  D(72), [D(70), D(80), D(28)],
                  "20% off: $100 − $20 = $80. Another 10% off $80: $80 − $8 = <b>$72</b>. "
                  "($70 adds the percents to 30%, but the second 10% is taken from $80, not $100.)"))
    its.append(mcq("Is 20% off and then another 10% off the same as 30% off?", "No, it is 28% off in total",
                   ["Yes, 20% + 10% = 30%", "No, it is 32% off in total", "No, it is 2% off in total"],
                   "On $100: 20% off gives $80, then 10% of $80 is $8 off, so the price is $72. That is $28 off $100: "
                   "<b>28% off in total</b>. The second discount is taken from a smaller price."))
    assert sale(60, 25) == 45
    its.append(mq("A pair of ski goggles is 25% off. The sale price is $45. What was the regular price?",
                  D(60), [D("56.25"), D("33.75"), D(70)],
                  "The sale price is 75% of the regular price. 75% is $45, so 25% is $45 ÷ 3 = $15, and 100% is 4 × $15 = <b>$60</b>. "
                  "Check: 25% of $60 is $15 and $60 − $15 = $45. ($56.25 adds 25% of $45 instead.)"))
    assert sale(85, 20) == 68 and sale(75, 10) == D("67.50")
    its.append(mcq("Store A sells a jacket for $85 at 20% off. Store B sells the same jacket for $75 at 10% off. Which store has the lower price?",
                   "Store B: $67.50", ["Store A: $68.00", "Store A: $65.00", "They are the same: $65.00"],
                   "Store A: 20% of $85 is $17, so $85 − $17 = $68.00. Store B: 10% of $75 is $7.50, so $75 − $7.50 = $67.50. "
                   "<b>Store B is lower, at $67.50</b>. ($65.00 subtracts the percent numbers as dollars.)"))
    assert len(its) == 20
    return {"title": "Discounts and sale prices", "items": its}


# ============================================================ set 3: sales tax (GST + PST)
def set_tax(P):
    its = []
    its.append(mcq("In BC, most things you buy have 5% GST and 7% PST added. What percent is added in total?",
                   "12%", ["2%", "35%", "5.7%"],
                   "Add the two tax rates: 5% + 7% = <b>12%</b>. So on most items you pay 12¢ more for every $1."))
    its.append(mq("A $40 lamp has 5% GST added. How much is the GST?", gst(40), [D(4), D("0.20"), D(42)],
                  "5% = 0.05. $40 × 0.05 = <b>$2</b>. Or: 10% is $4, so 5% is $2. ($4 is 10%; $0.20 is 0.5%; $42 is the price plus GST.)"))
    its.append(mq("A $40 lamp has 7% PST added. How much is the PST?", pst(40), [D(7), D("0.28"), D(28)],
                  "7% = 0.07. $40 × 0.07 = <b>$2.80</b>. ($7 uses the percent as dollars; $28 multiplies by 0.7.)"))
    its.append(mq("A $50 pair of headphones has 5% GST and 7% PST added. How much tax is that in total?", both(50),
                  [D(12), D("3.50"), D(56)],
                  "GST: $50 × 0.05 = $2.50. PST: $50 × 0.07 = $3.50. Total tax: $2.50 + $3.50 = <b>$6</b> (12% of $50). "
                  "($12 adds 12 dollars instead of 12%; $3.50 is only the PST.)"))
    its.append(mq("A $50 pair of headphones has 12% tax added (5% GST + 7% PST). What is the total price?", 50 + both(50),
                  [D(62), D("50.12"), D(6)],
                  "Tax: 12% of $50 = $6. Total: $50 + $6 = <b>$56</b>. Or in one step: $50 × 1.12 = $56. "
                  "($62 adds $12, not 12%.)"))
    its.append(mcq("Which calculation gives the total price of an item with 5% GST and 7% PST added?", "price × 1.12",
                   ["price × 0.12", "price + 12", "price × 0.05 × 0.07"],
                   "The total is 100% of the price plus 12% tax = 112% = 1.12. So <b>price × 1.12</b>. price × 0.12 gives only the tax."))
    its.append(mcq("In BC, which item has 5% GST but no PST?", "A child’s winter jacket",
                   ["A video game", "A pair of adult headphones", "A skateboard"],
                   "Children’s clothing and footwear have no PST in BC, so <b>a child’s winter jacket</b> has only 5% GST. "
                   "The other items have both GST and PST (12%)."))
    t = 30 + gst(30)
    assert t == D("31.50")
    its.append(mq("A pair of children’s rain boots costs $30. Children’s footwear has 5% GST but no PST. What is the total price?",
                  t, [D("33.60"), D(35), D("1.50")],
                  "Only GST applies: $30 × 0.05 = $1.50. Total: $30 + $1.50 = <b>$31.50</b>. ($33.60 adds 12%, but there is no PST.)"))
    t = 24 + gst(24)
    assert t == D("25.20")
    its.append(mq("A family’s restaurant meal costs $24 before tax. Restaurant meals in BC have 5% GST but no PST. What is the total?",
                  t, [D("26.88"), D(29), D("1.20")],
                  "GST: $24 × 0.05 = $1.20. Total: $24 + $1.20 = <b>$25.20</b>. ($26.88 adds 12%, but restaurant food has no PST.)"))
    t = 70 + both(70)
    assert t == D("78.40")
    its.append(mq("A $70 video game has 5% GST and 7% PST added. What is the total price?", t, [D(82), D("73.50"), D("8.40")],
                  "GST: $3.50. PST: $4.90. Total tax: $8.40 (12% of $70). Total: $70 + $8.40 = <b>$78.40</b>. "
                  "($73.50 adds only the GST.)"))
    t = 85 + both(85)
    assert gst(85) == D("4.25") and pst(85) == D("5.95") and t == D("95.20")
    its.append(mq("An $85 skateboard has 5% GST and 7% PST added. What is the total price?", t, [D(97), D("89.25"), D("10.20")],
                  "GST: $85 × 0.05 = $4.25. PST: $85 × 0.07 = $5.95. Total: $85 + $4.25 + $5.95 = <b>$95.20</b>. "
                  "($97 adds $12; $89.25 adds only the GST.)"))
    items = [("Phone case", D(28)), ("Charger", D(17))]
    sub = sum(p for n_, p in items)
    assert sub == 45 and gst(sub) == D("2.25") and pst(sub) == D("3.15") and sub + both(sub) == D("50.40")
    its.append(mq(fig(receipt_svg(items, [("Subtotal", money(sub)), ("GST 5%", money(gst(sub))), ("PST 7%", money(pst(sub))),
                                          ("Total", "?")])) + "What is the total on this receipt?",
                  D("50.40"), [D(57), D("47.25"), D("45.12")],
                  "Add the subtotal and both taxes: $45.00 + $2.25 + $3.15 = <b>$50.40</b>. ($47.25 forgets the PST; $57 adds $12.)"))
    assert pst("24.99") == D("1.75")
    its.append(mq("A pair of earbuds costs $24.99. How much is the 7% PST, rounded to the nearest cent?", D("1.75"),
                  [D("1.74"), D("17.49"), D("2.99")],
                  "$24.99 × 0.07 = $1.7493, which rounds to <b>$1.75</b>. "
                  "(Do not just cut off the digits; $17.49 multiplies by 0.7; $2.99 is 12%, both taxes.)"))
    t = D("24.99") + both("24.99")
    assert gst("24.99") == D("1.25") and t == D("27.99")
    its.append(mq("The $24.99 earbuds have 5% GST and 7% PST added. What is the total price?", t,
                  [D("36.99"), D("26.24"), D("25.11")],
                  "GST: $24.99 × 0.05 = $1.2495 → $1.25. PST: $1.7493 → $1.75. Total: $24.99 + $1.25 + $1.75 = <b>$27.99</b>. "
                  "($26.24 forgets the PST; $36.99 adds $12.)"))
    n, he, his, him = P.next()
    t = 16 + both(16)
    assert t == D("17.92") and cash(t) == D("17.90")
    its.append(mq("A $16 board game has 5%% GST and 7%% PST added. %s pays with cash. How much does %s pay?" % (n, he),
                  D("17.90"), [t, D("17.95"), D(28)],
                  "Tax: $16 × 0.12 = $1.92. Total: $17.92. Canada has no pennies, so a cash total rounds to the nearest 5¢: "
                  "$17.92 → <b>$17.90</b>. ($17.92 is what a card pays.)"))
    its.append(mcq("About how much GST and PST is added to an adult jacket that costs $39.99? Round the price first.",
                   "about $4.80", ["about $12", "about $2", "about $0.48"],
                   "$39.99 is about $40. 12% of $40: 10% is $4 and 2% is $0.80, so about <b>$4.80</b>. "
                   "($12 adds 12 dollars; $2 is only the 5% GST.)"))
    assert 60 + both(60) == D("67.20") and (D("67.20") * D("0.88")).quantize(CENT) == D("59.14")
    its.append(mq("A total of $67.20 includes 5% GST and 7% PST. What was the price before tax?", D(60),
                  [D("59.14"), D("55.20"), D("75.26")],
                  "The total is 112% of the price, so price × 1.12 = $67.20. Price = $67.20 ÷ 1.12 = <b>$60</b>. "
                  "Check: $60 × 1.12 = $67.20. ($59.14 takes 12% of the total, but the tax was 12% of the price.)"))
    t = sale(80, 25)
    assert t + both(t) == D("67.20") and D(80) * D("0.87") == D("69.60")
    its.append(mq("A pair of $80 headphones is 25% off. Then 5% GST and 7% PST are added. What is the total?", D("67.20"),
                  [D("69.60"), D(72), D(60)],
                  "Sale price: $80 − $20 = $60. Tax: 12% of $60 = $7.20. Total: $60 + $7.20 = <b>$67.20</b>. "
                  "(Do not subtract 25% and add 12% in one step: $80 × 0.87 = $69.60 is wrong, because the tax is on the sale price. $72 adds $12.)"))
    assert 40 + both(40) == D("44.80") and 50 + both(50) - 10 == 46
    its.append(mq("A $50 item has a $10-off coupon. The 12% tax (GST + PST) is charged on the price after the coupon. What is the total?",
                  D("44.80"), [D(46), D(52), D(40)],
                  "Coupon first: $50 − $10 = $40. Tax: 12% of $40 = $4.80. Total: <b>$44.80</b>. "
                  "($46 adds the tax before taking off the coupon: $56 − $10. Tax is charged on the price you actually pay.)"))
    a = 15 + gst(15)
    b = 40 + both(40)
    assert a == D("15.75") and b == D("44.80") and a + b == D("60.55")
    its.append(mq("A child’s T-shirt costs $15 (5% GST only). An adult hoodie costs $40 (5% GST and 7% PST). What is the total for both?",
                  D("60.55"), [D("61.60"), D("57.75"), D(55)],
                  "T-shirt: $15 + $0.75 GST = $15.75. Hoodie: $40 + $4.80 = $44.80. Total: $15.75 + $44.80 = <b>$60.55</b>. "
                  "($61.60 adds 12% to both; $57.75 adds only GST to both.)"))
    assert len(its) == 20
    return {"title": "Sales tax: GST and PST", "items": its}


# ============================================================ set 4: tips and simple interest
def interest(p, r, t):
    i = D(p) * D(r) / 100 * D(t)
    assert i == i.quantize(CENT)
    return i


def set_tips(P):
    its = []
    its.append(mq("A restaurant bill is $40. How much is a 15% tip?", pct(40, 15), [D(25), D(15), D(4)],
                  "10% of $40 is $4 and 5% is $2. 15% = $4 + $2 = <b>$6</b>. ($15 uses the percent as dollars; $4 is only 10%.)"))
    its.append(mq("A pizza delivery costs $35. How much is a 20% tip?", pct(35, 20), [D(15), D(20), D("3.50")],
                  "10% of $35 is $3.50, so 20% is 2 × $3.50 = <b>$7</b>. ($15 is 35 − 20; $3.50 is 10%.)"))
    its.append(mq("A meal costs $50. How much is an 18% tip?", pct(50, 18), [D(32), D(18), D(5)],
                  "$50 × 0.18 = <b>$9</b>. Or: 10% is $5, 8% is $4, and $5 + $4 = $9. ($18 uses the percent as dollars.)"))
    its.append(mq("A $60 meal has a 15% tip added. What is the total with the tip (before tax)?", 60 + pct(60, 15),
                  [D(75), D(9), D(66)],
                  "Tip: 10% is $6 and 5% is $3, so 15% is $9. Total: $60 + $9 = <b>$69</b>. ($75 adds $15; $66 adds only 10%.)"))
    its.append(mq("10% of a $46 bill is $4.60. Use this to find a 15% tip.", pct(46, 15), [D("4.60"), D("9.20"), D("2.30")],
                  "15% = 10% + 5%. 5% is half of $4.60, which is $2.30. $4.60 + $2.30 = <b>$6.90</b>. ($9.20 is 20%.)"))
    n, he, his, him = P.next()
    t = (48 + pct(48, 20)) / 4
    assert t == D("14.40")
    its.append(mq("%s and 3 friends share a $48 pizza order. They add a 20%% tip and split the total equally. How much does each person pay?" % n,
                  t, [D(12), D(17), D("57.60")],
                  "Tip: 20% of $48 = $9.60. Total: $57.60. 4 people: $57.60 ÷ 4 = <b>$14.40</b>. ($12 forgets the tip; $57.60 is the whole bill.)"))
    its.append(mcq("The simple interest formula is I = Prt. What does r stand for?", "The interest rate per year, as a decimal",
                   ["The total amount at the end", "The number of years", "The starting amount (principal)"],
                   "I is the interest, P is the principal (starting amount), <b>r is the yearly interest rate written as a decimal</b> "
                   "(3% = 0.03), and t is the time in years."))
    its.append(mq("What is the simple interest on $200 at 3% per year for 1 year?", interest(200, 3, 1), [D(600), D(206), D("0.60")],
                  "I = Prt = $200 × 0.03 × 1 = <b>$6</b>. ($600 uses 3 instead of 0.03; $206 is the balance, not the interest.)"))
    its.append(mq("What is the simple interest on $500 at 2% per year for 3 years?", interest(500, 2, 3), [D(10), D(3000), D(530)],
                  "I = Prt = $500 × 0.02 × 3 = $10 × 3 = <b>$30</b>. ($10 is only 1 year; $3000 uses 2 instead of 0.02; $530 is the balance.)"))
    i = interest(400, 4, 2)
    its.append(mq("%s puts $400 in a savings account that pays 4%% simple interest per year. How much is in the account after 2 years?" % P.next()[0],
                  400 + i, [i, D(416), D(3600)],
                  "I = $400 × 0.04 × 2 = $32. Balance: $400 + $32 = <b>$432</b>. ($32 is only the interest; $416 is after 1 year.)"))
    its.append(mq("What is the simple interest on $1000 at 1.5% per year for 4 years?", interest(1000, D("1.5"), 4),
                  [D(15), D(6000), D(1060)],
                  "I = $1000 × 0.015 × 4 = $15 × 4 = <b>$60</b>. ($15 is only 1 year; $1060 is the balance.)"))
    assert interest(300, 2, 5) == 30 and interest(500, 1, 3) == 15
    its.append(mcq("Which earns more simple interest: $300 at 2% per year for 5 years, or $500 at 1% per year for 3 years?",
                   "$300 for 5 years, by $15", ["$500 for 3 years, by $15", "$500 for 3 years, by $200", "They earn the same"],
                   "$300 × 0.02 × 5 = $30. $500 × 0.01 × 3 = $15. <b>The $300 for 5 years earns $15 more</b>. "
                   "A bigger principal does not always earn more; the rate and the time matter too."))
    its.append(mcq("$800 earns $24 of simple interest in 1 year. What is the interest rate?", "3%", ["24%", "0.03%", "33%"],
                   "r = I ÷ (P × t) = $24 ÷ $800 = 0.03 = <b>3%</b>. (24% uses the dollars; 33% divides $800 by $24.)"))
    assert interest(600, 2, 3) == 36
    its.append(mcq("$600 earns 2% simple interest per year. How many years until it earns $36 of interest?", "3 years",
                   ["18 years", "12 years", "6 years"],
                   "Interest each year: $600 × 0.02 = $12. $36 ÷ $12 = <b>3 years</b>. "
                   "(18 divides $36 by 2; 12 is the interest for one year, not the time.)"))
    n, he, his, him = P.next()
    i = interest(250, 8, 1)
    its.append(mq("%s borrows $250 for a new phone at 8%% simple interest per year. How much must %s pay back after 1 year?" % (n, he),
                  250 + i, [i, D(2250), D(258)],
                  "I = $250 × 0.08 × 1 = $20. Pay back: $250 + $20 = <b>$270</b>. ($20 is only the interest; $258 adds $8; $2250 uses 8 instead of 0.08.)"))
    i = interest(1200, 3, D("0.5"))
    its.append(mq("What is the simple interest on $1200 at 3% per year for 6 months?", i, [D(36), D(216), D(1218)],
                  "6 months is half a year, so t = 0.5. I = $1200 × 0.03 × 0.5 = $36 × 0.5 = <b>$18</b>. "
                  "($36 is a full year; $216 uses t = 6.)"))
    n, he, his, him = P.next()
    assert 40 + gst(40) + pct(40, 15) == 48 and (42 * D("1.15")) == D("48.30")
    its.append(mq("%s’s family has a $40 restaurant meal. 5%% GST is added (no PST on restaurant food), and they tip 15%% of the price before tax. "
                  "How much do they pay in total?" % n,
                  D(48), [D(42), D("48.30"), D(46)],
                  "GST: $40 × 0.05 = $2. Tip: 15% of $40 = $6. Total: $40 + $2 + $6 = <b>$48</b>. "
                  "($42 forgets the tip; $46 forgets the GST; $48.30 takes the tip on the taxed amount.)"))
    n, he, his, him = P.next()
    i = interest(350, 2, 2)
    its.append(mq("%s puts $350 into a savings account at 2%% simple interest per year for 2 years. What is the balance at the end?" % n,
                  350 + i, [i, D(357), D(1750)],
                  "I = $350 × 0.02 × 2 = $14. Balance: $350 + $14 = <b>$364</b>. ($14 is the interest; $357 is after 1 year; $1750 uses 2 instead of 0.02.)"))
    its.append(mq("How much more is a 20% tip than a 15% tip on a $64 bill?", pct(64, 5), [D(5), D("9.60"), D("12.80")],
                  "The difference is 5% of $64 = $3.20. (Check: 20% is $12.80 and 15% is $9.60; $12.80 − $9.60 = <b>$3.20</b>.) "
                  "($5 uses the percents as dollars.)"))
    assert interest(1500, 3, 1) == 45
    its.append(mq("How much must you put in a savings account at 3% simple interest per year to earn $45 in 1 year?", D(1500),
                  [D(15), D(135), D(150)],
                  "I = Prt, so $45 = P × 0.03 × 1. P = $45 ÷ 0.03 = <b>$1500</b>. Check: 3% of $1500 = $45. "
                  "($135 multiplies by 3; $150 divides by 0.3.)"))
    assert len(its) == 20
    return {"title": "Tips and simple interest", "items": its}


# ============================================================ set 5: best buys and budgeting
def best_item(q, opts, unit_txt, base, figure=False):
    """opts = [(label, amount, amount_text, price)]; lowest price per base wins."""
    us = []
    parts = []
    for lab, amt, at, pr in opts:
        u = F(str(D(pr))) * base / F(amt)
        assert (u * 100).denominator == 1, (lab, amt, pr)
        k = F(amt) / base
        kt = str(k.numerator) if k.denominator == 1 else format(D(k.numerator) / D(k.denominator), "f")
        ut = money(D(u.numerator) / D(u.denominator))
        us.append((u, lab, pr))
        parts.append("%s: %s ÷ %s = %s %s" % (lab, money(pr), kt, ut, unit_txt))
    srt = sorted(us)
    assert srt[0][0] < srt[1][0]
    ans = srt[0][1]
    e = "Compare the price " + unit_txt + ", not the total price. " + "; ".join(parts) + ". "
    e += "<b>%s</b> has the lowest price %s, so it is the best buy." % (ans, unit_txt)
    cheapest_total = min(us, key=lambda t: D(t[2]))[1]
    if cheapest_total != ans:
        e += " (%s has the lowest total, but you get less.)" % cheapest_total
    choices = [lab for lab, a, at, p in opts]
    if len(opts) == 2:
        choices += ["Both cost the same " + unit_txt, "You cannot compare different sizes"]
    else:
        choices += ["They all cost the same " + unit_txt]
    if figure:
        q = fig(tags_svg([(lab, at, pr) for lab, a, at, pr in opts])) + q
    return mcq(q, ans, [c for c in choices if c != ans], e)


def wk(n):
    return "%d week%s" % (n, "" if n == 1 else "s")


def weeks(goal, per):
    q = F(str(D(goal))) / F(str(D(per)))
    return -(-q.numerator // q.denominator)


def set_words(P):
    its = []
    its.append(best_item("Which bag of granola is the better buy?",
                         [("Bag A", 500, "500 g", "4.50"), ("Bag B", 800, "800 g", "6.80")], "per 100 g", 100, figure=True))
    its.append(best_item("Which jug of apple juice is the best buy?",
                         [("Jug A", 1, "1 L", "2.40"), ("Jug B", 2, "2 L", "4.40"), ("Jug C", 4, "4 L", "9.20")],
                         "per litre", 1, figure=True))
    assert D("13.20") / D("0.6") == 22
    its.append(mq("A 600 g piece of wild BC salmon costs $13.20. What is the price per kilogram?", D(22),
                  [D("7.92"), D("2.20"), D("220.00")],
                  "1 kg = 1000 g, and 600 g = 0.6 kg. $13.20 ÷ 0.6 = <b>$22.00 per kilogram</b>. "
                  "Check: 0.6 × $22 = $13.20. ($7.92 multiplies by 0.6; $2.20 is the price per 100 g.)"))
    n, he, his, him = P.next()
    assert 15 * 7 == 105
    its.append(mcq("The community pool charges $7 per swim, or $90 for a 15-swim pass. %s plans to swim 15 times. Which is cheaper, and by how much?" % n,
                   "The pass, by $15", ["Paying each swim, by $15", "The pass, by $83", "They cost the same"],
                   "Paying each swim: 15 × $7 = $105. The pass: $90. $105 − $90 = $15, so <b>the pass is cheaper by $15</b>. ($83 is $90 − $7.)"))
    t = sale(60, 20)
    assert t + both(t) == D("53.76") and D(60) * D("0.92") == D("55.20")
    its.append(mq("A $60 pair of adult running shoes is 20% off. 5% GST and 7% PST are added to the sale price. What is the total?",
                  D("53.76"), [D("55.20"), D(48), D(60)],
                  "Sale price: $60 − $12 = $48. Tax: 12% of $48 = $5.76. Total: $48 + $5.76 = <b>$53.76</b>. "
                  "($55.20 combines 20% off and 12% tax into 8% off; $48 forgets the tax.)"))
    n, he, his, him = P.next()
    assert 15 * 6 == 90 and pct(90, 60) == 54
    its.append(mq("%s earns $15 an hour babysitting and works 6 hours. %s spends 40%% and saves the rest. How much does %s save?" % (n, cap(he), he),
                  D(54), [D(36), D(30), D(90)],
                  "Earned: 6 × $15 = $90. Saves 100% − 40% = 60%: $90 × 0.6 = <b>$54</b>. ($36 is the 40% spent; $30 is 90 − 60.)"))
    n, he, his, him = P.next()
    bi, bo = [("Allowance", D(50)), ("Yard work", D(30))], [("Food", D(20)), ("Games", D(16)), ("Savings", D(24))]
    assert F(24, 80) == F(3, 10)
    its.append(mcq(fig(budget_svg("%s’s budget for June" % n, bi, bo)) + "What percent of %s’s money in goes to savings?" % n,
                   "30%", ["24%", "20%", "40%"],
                   "Money in: $50 + $30 = $80. Savings: $24. $24 ÷ $80 = 0.3 = <b>30%</b>. "
                   "(24% uses the dollars; 40% compares savings with spending, $24 ÷ $60.)"))
    n, he, his, him = P.next()
    tot = 250 + both(250)
    assert tot == 280 and weeks(tot - 40, 25) == 10 and weeks(250 - 40, 25) == 9 and weeks(tot, 25) == 12
    its.append(mcq("%s wants a $250 snowboard for the winter. 5%% GST and 7%% PST are added. %s has $40 saved and saves $25 a week. "
                   "How many more weeks until %s can buy it?" % (n, cap(he), he),
                   wk(10), [wk(9), wk(12), wk(11)],
                   "Total: $250 × 1.12 = $280. Still needed: $280 − $40 = $240. $240 ÷ $25 = 9.6, so round up to <b>10 weeks</b>. "
                   "(9 weeks forgets the tax or rounds down; 12 weeks forgets the $40 saved; 11 weeks also rounds down.)"))
    n, he, his, him = P.next()
    i = interest(600, D("2.5"), 2)
    assert i == 30
    its.append(mq("%s puts $600 from a summer job into a savings account at 2.5%% simple interest per year. How much interest does %s earn in 2 years?" % (n, he),
                  i, [D(15), D(3000), D(630)],
                  "I = Prt = $600 × 0.025 × 2 = $15 × 2 = <b>$30</b>. ($15 is one year; $630 is the balance.)"))
    assert sale(90, 30) == 63 and 90 - 25 == 65
    its.append(mq("Headphones cost $90. One coupon gives 30% off. Another gives $25 off. What is the lower price before tax?", D(63),
                  [D(65), D(60), D("70.56")],
                  "30% off: 30% of $90 = $27, so $63. $25 off: $65. The lower price is <b>$63</b>. "
                  "($60 subtracts 30 dollars; $70.56 adds the tax.)"))
    n, he, his, him = P.next()
    tot = 72 + gst(72) + pct(72, 18)
    assert tot == D("88.56") and tot / 4 == D("22.14") and (72 + gst(72)) / 4 == D("18.90") and (72 + pct(72, 18)) / 4 == D("21.24")
    assert (72 + both(72) + pct(72, 18)) / 4 == D("23.40")
    its.append(mq("%s and 3 friends have dinner in Vancouver. The food costs $72. 5%% GST is added (no PST on restaurant food), "
                  "and they tip 18%% of the price before tax. They split the total equally. How much does each person pay?" % n,
                  D("22.14"), [D("18.90"), D("21.24"), D("23.40")],
                  "GST: $72 × 0.05 = $3.60. Tip: $72 × 0.18 = $12.96. Total: $72 + $3.60 + $12.96 = $88.56. "
                  "Each: $88.56 ÷ 4 = <b>$22.14</b>. ($18.90 forgets the tip; $23.40 adds PST, which restaurant food does not have.)"))
    its.append(best_item("Which bag of rice is the better buy?",
                         [("Bag A", 2, "2 kg", "7.80"), ("Bag B", 5, "5 kg", "18.50")], "per kilogram", 1, figure=True))
    n, he, his, him = P.next()
    assert pct(240, 20) == 48
    its.append(mq("%s earns $240 picking fruit in the Okanagan. %s plans to save 50%%, spend 30%% and give 20%% to charity. How much will %s give?" % (n, cap(he), he),
                  D(48), [D(20), D(24), D(72)],
                  "20% of $240: 10% is $24, so 20% is <b>$48</b>. Check: $120 + $72 + $48 = $240. ($24 is only 10%; $72 is the 30% spent.)"))
    assert 1250 * D("1.2") == 1500
    its.append(mq("Last year a school raised $1250 at its Terry Fox Run. This year it raised 20% more. How much did it raise this year?",
                  D(1500), [D(1270), D(250), D(1000)],
                  "20% of $1250: 10% is $125, so 20% is $250. This year: $1250 + $250 = <b>$1500</b>. "
                  "($1270 adds $20; $250 is only the increase; $1000 is 20% less.)"))
    assert 400 + pct(400, 5) == 420
    its.append(mq("A hockey registration fee of $400 goes up by 5% next season. What is the new fee?", D(420),
                  [D(405), D(20), D(380)],
                  "5% of $400 = $20. New fee: $400 + $20 = <b>$420</b>. ($405 adds $5; $380 subtracts the increase.)"))
    assert 50 + both(50) == 56
    its.append(mcq("Store A sells a speaker for $50 plus 12% tax (GST + PST). Store B sells the same speaker for $55 with tax included. Which is cheaper?",
                   "Store B, by $1", ["Store A, by $5", "Store A, by $1", "They cost the same"],
                   "Store A: $50 × 1.12 = $56. Store B: $55. <b>Store B is cheaper by $1</b>. "
                   "(Store A by $5 forgets to add the tax to Store A’s price.)"))
    n, he, his, him = P.next()
    i = interest(300, 5, 2)
    its.append(mq("%s borrows $300 from %s parents for a bike and agrees to pay 5%% simple interest per year. %s pays it all back after 2 years. "
                  "How much does %s pay back?" % (n, his, cap(he), he),
                  300 + i, [D(315), i, D(3300)],
                  "I = $300 × 0.05 × 2 = $30. Pay back: $300 + $30 = <b>$330</b>. ($315 is only 1 year of interest; $30 is only the interest.)"))
    n, he, his, him = P.next()
    t = D("11.40") + gst("11.40")
    assert t == D("11.97") and cash(t) == D("11.95") and 20 - cash(t) == D("8.05")
    t12 = D("11.40") + both("11.40")
    assert t12 == D("12.77") and 20 - cash(t12) == D("7.25")
    its.append(mq("At a café in Victoria, %s buys lunch for $11.40. 5%% GST is added (no PST on food). %s pays cash with a $20 bill. "
                  "How much change does %s get?" % (n, cap(he), he),
                  D("8.05"), [D("8.03"), D("8.60"), D("7.25")],
                  "GST: $11.40 × 0.05 = $0.57. Total: $11.97. Cash rounds to the nearest 5¢: $11.95. "
                  "Change: $20.00 − $11.95 = <b>$8.05</b>. ($8.03 forgets the cash rounding; $8.60 forgets the GST; $7.25 adds PST too.)"))
    n, he, his, him = P.next()
    t = sale(90, 20)
    assert t == 72 and t + both(t) == D("80.64") and 100 - D("80.64") == D("19.36") and 100 - D(90) * D("0.92") == D("17.20")
    its.append(mq("%s has $100 in %s bank account. %s buys a $90 adult rain jacket at 20%% off, and 5%% GST and 7%% PST are added. "
                  "%s pays by debit. How much is left in the account?" % (n, his, cap(he), cap(he)),
                  D("19.36"), [D(28), D("17.20"), D(10)],
                  "Sale price: $90 − $18 = $72. Tax: 12% of $72 = $8.64. Total: $80.64. Left: $100.00 − $80.64 = <b>$19.36</b>. "
                  "Debit is exact, so there is no rounding. ($28 forgets the tax; $17.20 combines 20% off and 12% tax into 8% off.)"))
    n, he, his, him = P.next()
    assert sale(30, 10) * 4 == 108 and 108 + both(108) == D("120.96")
    its.append(mq("A soccer team buys 4 adult jerseys at $30 each. The store gives 10% off the whole order, then adds 5% GST and 7% PST. "
                  "What is the total?",
                  D("120.96"), [D("134.40"), D(108), D("122.40")],
                  "Before the discount: 4 × $30 = $120. 10% off: $120 − $12 = $108. Tax: 12% of $108 = $12.96. "
                  "Total: $108 + $12.96 = <b>$120.96</b>. ($108 forgets the tax; $134.40 forgets the discount; $122.40 is $120 × 1.02, which combines 10% off and 12% tax.)"))
    assert D(120) * D("1.02") == D("122.40") and 120 + both(120) == D("134.40")
    assert len(its) == 20
    return {"title": "Best buys and budgeting", "items": its}


# ============================================================ lesson
def body_html():
    assert pct(80, 25) == 20 and 60 + both(60) == D("67.20") and interest(500, 3, 2) == 30
    return (
        "<h2>Percent of an amount</h2>"
        "<p>Percent means “out of 100”. To find a percent of an amount, write the percent as a decimal and multiply. "
        "12% = 0.12, 5% = 0.05, 7% = 0.07.</p>"
        "<p>You can also build percents from 10%: 10% is one tenth, 5% is half of 10%, and 1% is one hundredth.</p>"
        "<figure class='sn-fig'>" + bar_svg(80, 25, "$20") +
        "<figcaption>25% of $80 is one quarter of $80: $80 ÷ 4 = $20.</figcaption></figure>"
        "<h2>Discounts and sale prices</h2>"
        "<p>A discount is a percent of the regular price. Subtract it, or multiply by what is left: 25% off means you pay 75%.</p>" +
        ex("Example", "An $80 jacket is 25% off. What is the sale price?",
           "Discount: 25% of $80 = $20. Sale price: $80 − $20 = $60. Or: $80 × 0.75 = $60.", "$60") +
        "<h2>Sales tax in BC: GST and PST</h2>"
        "<p>Most things you buy in BC have <b>5% GST</b> and <b>7% PST</b> added, 12% in total. Some items have only GST: "
        "children’s clothing and footwear, and restaurant meals. Find the sale price first, then add the tax.</p>"
        "<figure class='sn-fig'>" + receipt_svg([("Headphones", D(60))], [("GST 5%", "$3.00"), ("PST 7%", "$4.20"), ("Total", "$67.20")]) +
        "<figcaption>GST: $60 × 0.05 = $3.00. PST: $60 × 0.07 = $4.20. Total: $67.20, the same as $60 × 1.12.</figcaption></figure>"
        "<h2>Tips and simple interest</h2>"
        "<p>A tip is a percent of a restaurant bill, often 15% to 20% of the price before tax. "
        "Simple interest uses <b>I = Prt</b>: principal × yearly rate (as a decimal) × time in years.</p>" +
        ex("Example", "You save $500 at 3% simple interest per year for 2 years. How much is in the account?",
           "I = $500 × 0.03 × 2 = $30. Balance: $500 + $30 = $530.", "$530") +
        "<h2>Best buys and budgets</h2>"
        "<p>To find the best buy, compare the price for the same amount, such as per 100 g or per litre. "
        "When you plan a budget, remember to include the tax.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["12% of $50 = $12", "12% = 0.12, so $50 × 0.12 = $6"],
            ["25% off $60 = $60 − 25 = $35", "Find 25% of $60 ($15), then subtract: $45"],
            ["Taking 25% off and adding 12% tax as one step: price × 0.87", "Take the discount first, then add 12% of the sale price"],
            ["Adding PST to children’s clothing or restaurant meals", "These have 5% GST only"],
            ["Using I = P × 3 × t for 3%", "Write the rate as a decimal: 3% = 0.03"],
            ["Giving the interest as the balance", "Balance = principal + interest"],
        ])
    )


FAQ = [
    {"q": "What are GST and PST in BC?",
     "a": "GST is the 5% federal sales tax and PST is BC’s 7% provincial sales tax, so most items have 12% added. "
          "Some items, like children’s clothing and restaurant meals, have only the 5% GST."},
    {"q": "How do you calculate a sale price with a percent discount?",
     "a": "Find the percent of the regular price and subtract it, or multiply by the percent you still pay. "
          "For 25% off $80, the discount is $20 and the sale price is $60, the same as $80 × 0.75."},
    {"q": "How do Grade 7 students calculate simple interest?",
     "a": "They use I = Prt: the principal times the yearly interest rate as a decimal times the time in years. "
          "$500 at 3% for 2 years earns $500 × 0.03 × 2 = $30."},
    {"q": "Do financial percent worksheets help with the Grade 7 FSA?",
     "a": "Yes. The Grade 7 FSA includes numeracy, where students solve problems in real contexts. "
          "Working out discounts, sales tax, tips and interest is good practice for that kind of question."},
]


def gen():
    rnd = random.Random(37816)
    P = People(rnd)
    sets = [set_percent(P), set_discount(P), set_tax(P), set_tips(P), set_words(P)]
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
                assert "HST" not in x and "13%" not in x, x
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-7", "slug": "financial-percentages", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 7 Financial Percentages: Discounts, GST and PST, Tips and Simple Interest",
        "seo_title": "Grade 7 Financial Percentages Worksheets: Discounts, GST + PST, Tips and Interest (Free, Answer Key, BC Curriculum)",
        "short_title": "Financial percentages",
        "domain": "Financial literacy",
        "standard_code": "Grade 7: Financial literacy",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/7/core",
        "standard_text": "Financial literacy – financial percentage",
        "meta_desc": "Free Grade 7 math worksheets on financial percentages for the BC curriculum: percent of an amount, discounts and sale prices, "
                     "5% GST and 7% PST, tips, simple interest with I = Prt, best buys and budgets. 100 questions with an answer key, "
                     "good FSA numeracy practice.",
        "key_big": "Write the percent as a decimal and multiply: 12% of $50 = $50 × 0.12 = $6.",
        "key_sub": "Take the discount first, then add the tax: 5% GST and 7% PST make 12% on most items in BC. "
                   "Simple interest is I = Prt, with the rate as a decimal and the time in years.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "Shelf tags: [^;']*;[^;']*;")
    mark_large(u, "Percent bar")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
