# -*- coding: utf-8 -*-
"""
Singapore Primary 5 Maths: Discount, GST and Annual Interest (MOE 2021 Primary Mathematics Syllabus, Percentage)
  python3 tools/gen_sg_maths_p5_discount_gst_interest.py
Discount and sale price, price after 9% GST, discount then GST on a receipt, annual interest for 1 year,
word problems with bar models and comparing deals. All money is worked with decimal.Decimal and every answer is
exact to the cent (GST is only charged on whole-dollar amounts). Singapore style: whole dollars as $45, otherwise
$39.24; 5 or more digits grouped with a no-break space ($10 200); the cent sign for amounts under $1.
Helpers are adapted from gen_cabc_math_g7_financial_percentages.py. HTML attributes use single quotes.
"""
import json, os, random, re
from decimal import Decimal as D

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-5")
UPDATED = "2026-11-03"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
GREY = "#6b6259"
PAPER = "#fffdf5"
EDGE = "#b8b0a0"
LIGHT = "#d9eadf"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]
CENT = D("0.01")


# ------------------------------------------------------------ money
def group(n):
    s = str(n)
    if len(s) <= 4:
        return s
    out = []
    while s:
        out.insert(0, s[-3:])
        s = s[:-3]
    return NB.join(out)


def money(d):
    """$45, $39.24, $10 200, $1471.50 (Singapore: no separator for 4 digits)."""
    d = D(d)
    assert 0 <= d < 100000, d
    assert d == d.quantize(CENT), d
    whole = int(d)
    if d == whole:
        return "$" + group(whole)
    return "$" + group(whole) + "." + format(d.quantize(CENT), "f").split(".")[1]


def money2(d):
    """Always with cents, for receipts: $80.00."""
    d = D(d).quantize(CENT)
    return "$" + group(int(d)) + "." + format(d, "f").split(".")[1]


def pct(p, r):
    """Exact r% of p (must be whole cents)."""
    x = D(p) * D(r) / 100
    assert x == x.quantize(CENT), (p, r)
    return x.quantize(CENT) if x != int(x) else D(int(x))


def gst(p):
    p = D(p)
    assert p == int(p), p  # GST only on whole dollars here, so it is exact
    return pct(p, 9)


def sale(p, r):
    return D(p) - pct(p, r)


def after_gst(p):
    return D(p) + gst(p)


def interest(p, r):
    return pct(p, r)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c:
            continue
        seen.add(c)
        pick.append(c)
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def mq(q, correct, wrongs, e):
    correct = D(correct)
    ws = [D(x) for x in wrongs]
    assert len(ws) == 3 and len(set(ws + [correct])) == 4 and all(w > 0 for w in ws), (q, correct, ws)
    return mcq(q, money(correct), [money(x) for x in ws], e)


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


def cap(s):
    return s[0].upper() + s[1:]


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
def sale_tag_svg(price, off):
    W, H = 210, 110
    s = [
        "<path d='M30 4 H202 a6 6 0 0 1 6 6 V100 a6 6 0 0 1 -6 6 H30 L4 55 Z' fill='%s' stroke='%s' stroke-width='2'/>" % (PAPER, RED),
        "<circle cx='26' cy='55' r='6' fill='#ffffff' stroke='%s' stroke-width='2'/>" % RED,
        txt(120, 34, "Usual price " + money(price), 17),
        txt(120, 80, "%d%% OFF" % off, 30, bold=True, col=RED),
    ]
    return svg_wrap(W + 2, H + 2, "".join(s), "Sale tag: usual price %s, %d%% off" % (money(price), off))


def cell(W, y, val, bold):
    """A value at the right of a receipt row; an empty value is a short line to fill in."""
    if val == "":
        return "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>" % (W - 84, y + 3, W - 14, y + 3, GREY)
    return txt(W - 14, y, val, 16, "end", bold=bold or val == "?", col=GREEN if val == "?" else INK)


def card_svg(title, top, rows):
    """A receipt or savings record. top = [(label, value)] above a dashed line, rows = [(label, value)] below it.
    Values are text; '?' is shown in green. The last row is bold."""
    W, rh = 290, 24
    s = [txt(W // 2, 24, title, 17, bold=True)]
    y = 50
    for lab, val in top:
        s.append(txt(14, y, lab, 16, "start"))
        s.append(cell(W, y, val, False))
        y += rh
    s.append("<line x1='10' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5' stroke-dasharray='4 3'/>" % (
        y - 14, W - 10, y - 14, GREY))
    y += 6
    for i, (lab, val) in enumerate(rows):
        last = i == len(rows) - 1
        s.append(txt(14, y, lab, 16, "start", bold=last))
        s.append(cell(W, y, val, last))
        y += rh
    s.insert(0, "<rect x='2' y='2' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (W - 4, y - 12, PAPER, EDGE))
    label = title + ": " + ", ".join("%s %s" % (a, b or "blank") for a, b in top + rows)
    return svg_wrap(W, y - 8, "".join(s), label)


def bar_model_svg(n, k, total_txt, part_txt, rest_txt, part_name, rest_name):
    """Bar model: n equal units for 100% (total above); the first k units shaded (part), the rest below."""
    L, R = 20, 420
    u = (R - L) / n
    y0, h = 40, 36
    xk = L + k * u
    s = []
    s.append("<rect x='%d' y='%d' width='%s' height='%d' fill='%s'/>" % (L, y0, round(k * u, 2), h, LIGHT))
    for i in range(n):
        s.append("<rect x='%s' y='%d' width='%s' height='%d' fill='none' stroke='%s' stroke-width='2'/>" % (
            round(L + i * u, 2), y0, round(u, 2), h, GREEN))
    # top bracket over the whole bar
    s.append("<path d='M%d %d V%d H%d V%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (L, y0 - 6, y0 - 14, R, y0 - 6, INK))
    s.append("<rect x='%d' y='%d' width='%d' height='20' fill='#ffffff'/>" % ((L + R) / 2 - 48, y0 - 26, 96))
    s.append(txt((L + R) / 2, y0 - 9, total_txt, 16, bold=True))
    # bottom brackets
    yb = y0 + h + 6
    for a, b, t1, t2, col in ((L, xk, part_txt, part_name, RED), (xk, R, rest_txt, rest_name, GREEN)):
        a2, b2 = round(a + 3, 2), round(b - 3, 2)
        s.append("<path d='M%s %d V%d H%s V%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (a2, yb, yb + 8, b2, yb, INK))
        cx = round((a + b) / 2, 2)
        s.append(txt(cx, yb + 26, t1, 16, bold=True, col=col))
        s.append(txt(cx, yb + 45, t2, 14, col=GREY))
    W, H = 440, yb + 52
    label = "Bar model: %d units = %s; %s %s, %s %s" % (n, total_txt, part_name, part_txt, rest_name, rest_txt)
    return svg_wrap(W, H, "".join(s), label)


# ============================================================ set 1: discount and sale price
def set_discount(P):
    its = []
    its.append(mq(fig(sale_tag_svg(45, 20)) + "The usual price of a school bag is $45. It is sold at a 20% discount. How much is the discount?",
                  D(9), [D(20), D(36), D(25)],
                  "10% of $45 = $4.50, so 20% = 2 × $4.50 = <b>$9</b>. ($20 uses the percentage as dollars; $36 is the sale price.)"))
    its.append(mq("The usual price of a school bag is $45. It is sold at a 20% discount. What is the sale price?",
                  sale(45, 20), [D(25), D(54), D(9)],
                  "Discount: 20% of $45 = $9. Sale price: $45 − $9 = <b>$36</b>. "
                  "($25 subtracts 20 dollars, not 20%; $54 adds the discount.)"))
    its.append(mq("A pair of shoes costs $60. There is a 10% discount. How much is the discount?",
                  D(6), [D(10), D(54), D(50)],
                  "10% of $60 = $60 ÷ 10 = <b>$6</b>. ($10 uses the percentage as dollars; $54 is the sale price.)"))
    its.append(mq("A pair of shoes costs $60. There is a 10% discount. What is the sale price?",
                  sale(60, 10), [D(50), D(66), D(6)],
                  "Discount: 10% of $60 = $6. Sale price: $60 − $6 = <b>$54</b>. ($50 subtracts $10; $66 adds the discount.)"))
    its.append(mq("A T-shirt costs $38. It is sold at 50% off. What is the sale price?",
                  sale(38, 50), [D(57), D(76), D("37.50")],
                  "50% is half. $38 ÷ 2 = <b>$19</b>. ($57 adds 50%; $76 doubles instead of halving; $37.50 takes away 50¢, not 50%.)"))
    its.append(mq(fig(sale_tag_svg(64, 25)) + "What is the sale price of this rice cooker?",
                  sale(64, 25), [D(39), D(16), D(80)],
                  "25% is one quarter. Discount: $64 ÷ 4 = $16. Sale price: $64 − $16 = <b>$48</b>. "
                  "($39 subtracts 25 dollars; $16 is the discount.)"))
    its.append(mq("A standing fan costs $120. It is sold at a 5% discount. How much is the discount?",
                  D(6), [D(5), D(12), D(114)],
                  "10% of $120 = $12, so 5% = $12 ÷ 2 = <b>$6</b>. ($5 uses the percentage as dollars; $12 is 10%; $114 is the sale price.)"))
    its.append(mcq("An item is sold at a 20% discount. Which gives the sale price?", "80% of the usual price",
                   ["20% of the usual price", "Usual price − $20", "120% of the usual price"],
                   "The usual price is 100%. Take away 20%: 100% − 20% = 80%. So the sale price is <b>80% of the usual price</b>. "
                   "20% of the usual price is only the discount."))
    its.append(mq("A bicycle helmet costs $90. It is sold at a 30% discount. What is the sale price?",
                  sale(90, 30), [D(60), D(27), D(117)],
                  "10% of $90 = $9, so 30% = $27. Sale price: $90 − $27 = <b>$63</b>. ($60 subtracts 30 dollars; $27 is the discount.)"))
    its.append(mq("A pair of sports shoes costs $80. It is sold at a 15% discount. What is the sale price?",
                  sale(80, 15), [D(65), D(12), D(92)],
                  "10% of $80 = $8 and 5% = $4, so 15% = $12. Sale price: $80 − $12 = <b>$68</b>. "
                  "($65 subtracts 15 dollars; $92 adds the discount.)"))
    its.append(mq("A set of storybooks costs $35. It is sold at a 40% discount. What is the sale price?",
                  sale(35, 40), [D(14), D(49), D("31.50")],
                  "10% of $35 = $3.50, so 40% = 4 × $3.50 = $14. Sale price: $35 − $14 = <b>$21</b>. "
                  "($14 is the discount; $31.50 takes off only 10%.)"))
    its.append(mcq("The usual price of a lamp is $50. Mrs Lim gets a discount of $10. What percentage discount is this?",
                   "20%", ["10%", "80%", "5%"],
                   "Discount as a fraction of the usual price: 10/50 = 20/100 = <b>20%</b>. "
                   "(10% uses the dollars as the percentage; 80% is the part she pays; 5% comes from 50 ÷ 10.)"))
    its.append(mcq("The usual price of a jacket is $80. The sale price is $60. What percentage discount is given?",
                   "25%", ["20%", "75%", "33⅓%"],
                   "Discount: $80 − $60 = $20. Compare with the <b>usual</b> price: 20/80 = 1/4 = <b>25%</b>. "
                   "(20% uses the dollars; 75% is the part paid; 33⅓% divides by the sale price.)"))
    its.append(mcq("The usual price of a water bottle is $40. The sale price is $34. What percentage discount is given?",
                   "15%", ["6%", "85%", "34%"],
                   "Discount: $40 − $34 = $6. 6/40 = 15/100 = <b>15%</b>. "
                   "(6% uses the dollars; 85% is the part paid; 34% uses the sale price.)"))
    its.append(mq("A study desk costs $250. It is sold at a 12% discount. What is the sale price?",
                  sale(250, 12), [D(238), D(30), D(280)],
                  "1% of $250 = $2.50, so 12% = 12 × $2.50 = $30. Sale price: $250 − $30 = <b>$220</b>. "
                  "($238 subtracts 12 dollars; $30 is the discount.)"))
    its.append(mq("A laptop costs $1200. It is sold at a 15% discount. What is the sale price?",
                  sale(1200, 15), [D(1185), D(180), D(1380)],
                  "10% of $1200 = $120 and 5% = $60, so 15% = $180. Sale price: $1200 − $180 = <b>$1020</b>. "
                  "($1185 subtracts 15 dollars; $1380 adds the discount.)"))
    n, he, his, him = P.next()
    its.append(mq("A pair of shoes costs $72. %s buys it at a 25%% discount. How much does %s save?" % (n, he),
                  D(18), [D(25), D(54), D(47)],
                  "The amount saved is the discount. 25%% of $72 = $72 ÷ 4 = <b>$18</b>. "
                  "($54 is what %s pays; $47 is $72 − 25.)" % he))
    its.append(mq("A T-shirt costs $15. A shop gives 10% off the total when you buy 2. How much do 2 T-shirts cost?",
                  D(27), [D(20), D("28.50"), D(3)],
                  "Total: 2 × $15 = $30. Discount: 10% of $30 = $3. Pay: $30 − $3 = <b>$27</b>. "
                  "($20 subtracts $10; $28.50 takes 10% off one T-shirt only; $3 is the discount.)"))
    assert sale(56, 25) == 42
    its.append(mq(fig(bar_model_svg(4, 1, "$56", "25%", "?", "discount", "sale price")) +
                  "The usual price of a toy is $56. It is sold at a 25% discount. Use the model to find the sale price.",
                  D(42), [D(31), D(14), D(70)],
                  "25% = 1/4, so the bar has 4 units. 4 units = $56, 1 unit = $56 ÷ 4 = $14. "
                  "Sale price = 3 units = 3 × $14 = <b>$42</b>. ($31 subtracts 25 dollars; $14 is the discount.)"))
    assert sale(80, 20) - 5 == 59
    its.append(mq("A bag costs $80. The shop gives a 20% discount first. Then Mdm Wong uses a $5 voucher. How much does she pay?",
                  D(59), [D(55), D(60), D(69)],
                  "20% of $80 = $16, so the sale price is $64. Voucher: $64 − $5 = <b>$59</b>. "
                  "($55 subtracts 20 dollars; $60 treats the $5 as 5% more off; $69 adds the voucher.)"))
    assert len(its) == 20
    return {"title": "Discount and sale price", "items": its}


# ============================================================ set 2: GST
def set_gst(P):
    its = []
    its.append(mq("In Singapore, GST is 9%. How much GST is charged on a $100 item?",
                  gst(100), [D("0.90"), D(109), D(91)],
                  "9% of $100 = 9/100 × $100 = <b>$9</b>. ($109 is the price after GST, not the GST.)"))
    its.append(mq("How much is 9% GST on $80?", gst(80), [D(9), D("0.72"), D(72)],
                  "1% of $80 = $0.80, so 9% = 9 × $0.80 = <b>$7.20</b>. "
                  "($9 uses the percentage as dollars; $72 is 90% of $80.)"))
    its.append(mq("An item costs $80 before GST. What is the price after 9% GST?", after_gst(80),
                  [D(89), D("72.80"), D("7.20")],
                  "GST: 9% of $80 = $7.20. Price after GST: $80 + $7.20 = <b>$87.20</b>. "
                  "($89 adds $9; $72.80 subtracts the GST; $7.20 is only the GST.)"))
    its.append(mq("How much is 9% GST on $50?", gst(50), [D(9), D("0.45"), D("54.50")],
                  "1% of $50 = $0.50, so 9% = 9 × $0.50 = <b>$4.50</b>. ($54.50 is the price after GST.)"))
    its.append(mq("A pair of school shoes costs $25 before GST. How much is the 9% GST?", gst(25), [D(9), D("27.25"), D("2.50")],
                  "1% of $25 = $0.25, so 9% = 9 × $0.25 = <b>$2.25</b>. "
                  "($2.50 is 10%; $27.25 is the price after GST; $9 uses the percentage as dollars.)"))
    its.append(mq("A pair of headphones costs $50 before GST. What is the price after 9% GST?", after_gst(50),
                  [D(59), D("45.50"), D("50.09")],
                  "GST: 9% of $50 = $4.50. Price after GST: $50 + $4.50 = <b>$54.50</b>. "
                  "($59 adds $9; $50.09 adds 9¢; $45.50 subtracts the GST.)"))
    its.append(mcq("Which gives the price of an item after 9% GST?", "109% of the price",
                   ["9% of the price", "Price + $9", "91% of the price"],
                   "The price is 100%. GST adds 9% more: 100% + 9% = <b>109% of the price</b>. "
                   "9% of the price is only the GST; 91% takes the GST away."))
    its.append(mq("A microwave oven costs $200 before GST. What is the price after 9% GST?", after_gst(200),
                  [D(209), D(182), D(18)],
                  "GST: 1% of $200 = $2, so 9% = $18. Price after GST: $200 + $18 = <b>$218</b>. "
                  "($209 adds $9; $182 subtracts the GST; $18 is only the GST.)"))
    its.append(mq("A box of art materials costs $30 before GST. What is the price after 9% GST?", after_gst(30),
                  [D(39), D("27.30"), D(33)],
                  "GST: 9% of $30 = 9 × $0.30 = $2.70. Price after GST: $30 + $2.70 = <b>$32.70</b>. "
                  "($39 adds $9; $33 adds 10%; $27.30 subtracts the GST.)"))
    its.append(mq("How much is 9% GST on $120?", gst(120), [D(9), D("1.08"), D(108)],
                  "1% of $120 = $1.20, so 9% = 9 × $1.20 = <b>$10.80</b>. "
                  "($9 uses the percentage as dollars; $108 is 90% of $120; $1.08 is 0.9%.)"))
    its.append(mq("A lunch box costs $15 before GST. What is the price after 9% GST?", after_gst(15),
                  [D(24), D("13.65"), D("16.50")],
                  "GST: 9% of $15 = 9 × $0.15 = $1.35. Price after GST: $15 + $1.35 = <b>$16.35</b>. "
                  "($24 adds $9; $16.50 adds 10%; $13.65 subtracts the GST.)"))
    n, he, his, him = P.next()
    its.append(mq("A table fan costs $45 before GST. How much does %s pay after 9%% GST?" % n, after_gst(45),
                  [D(54), D("40.95"), D("49.50")],
                  "GST: 9% of $45 = 9 × $0.45 = $4.05. Price after GST: $45 + $4.05 = <b>$49.05</b>. "
                  "($49.50 writes $4.05 as $4.50; $54 adds $9; $40.95 subtracts the GST.)"))
    rec = card_svg("Receipt", [("Sports socks", money2(25)), ("Shin guards", money2(13))],
                   [("Subtotal", money2(38)), ("GST 9%", "?"), ("Total", "")])
    assert gst(38) == D("3.42")
    its.append(mq(fig(rec) + "How much is the GST on this receipt?", gst(38), [D(9), D("2.25"), D("3.80")],
                  "GST is 9% of the subtotal. 1% of $38 = $0.38, so 9% = 9 × $0.38 = <b>$3.42</b>. "
                  "($2.25 is GST on the socks only; $3.80 is 10%; $9 uses the percentage as dollars.)"))
    rec = card_svg("Receipt", [("Sports socks", money2(25)), ("Shin guards", money2(13))],
                   [("Subtotal", money2(38)), ("GST 9%", money2(gst(38))), ("Total", "?")])
    its.append(mq(fig(rec) + "What is the total on this receipt?", after_gst(38), [D(47), D("34.58"), D("40.25")],
                  "Total = subtotal + GST = $38.00 + $3.42 = <b>$41.42</b>. "
                  "($47 adds $9; $34.58 subtracts the GST; $40.25 adds GST on the socks only.)"))
    its.append(mq("A television costs $1500 before GST. What is the price after 9% GST?", after_gst(1500),
                  [D(1509), D(1365), D(1650)],
                  "GST: 1% of $1500 = $15, so 9% = $135. Price after GST: $1500 + $135 = <b>$1635</b>. "
                  "($1509 adds $9; $1650 adds 10%; $1365 subtracts the GST.)"))
    assert gst(28) == D("2.52")
    its.append(mq("A pencil case costs $28 and a ruler set costs $12, before GST. What is the total price after 9% GST?",
                  after_gst(40), [D(49), D("36.40"), D("42.52")],
                  "Price before GST: $28 + $12 = $40. GST: 9% of $40 = $3.60. Total: $40 + $3.60 = <b>$43.60</b>. "
                  "($42.52 adds GST on the pencil case only; $49 adds $9.)"))
    its.append(mq("The price of a mattress is $70 before GST. What is the price after 9% GST?", after_gst(70),
                  [D(79), D("63.70"), D(77)],
                  "GST: 9% of $70 = $6.30. Price after GST: $70 + $6.30 = <b>$76.30</b>. "
                  "($79 adds $9; $77 adds 10%; $63.70 subtracts the GST.)"))
    its.append(mq("An item costs $90 before GST. How much more is its price after 9% GST?", gst(90),
                  [D(9), D("98.10"), D("0.81")],
                  "The difference is the GST: 9% of $90 = 9 × $0.90 = <b>$8.10</b>. ($98.10 is the price after GST; $9 uses the percentage as dollars.)"))
    assert after_gst(50) == D("54.50")
    its.append(mcq("Shop A sells a speaker for $50 before GST. Shop B sells the same speaker for $54, GST included. Which shop is cheaper?",
                   "Shop B, by 50¢", ["Shop A, by $4", "Shop A, by 50¢", "They cost the same"],
                   "Shop A: $50 + 9% GST = $50 + $4.50 = $54.50. Shop B: $54. <b>Shop B is cheaper by 50¢</b>. "
                   "(Shop A by $4 forgets to add GST to Shop A’s price.)"))
    n, he, his, him = P.next()
    assert after_gst(48) == D("52.32") and after_gst(12) == D("13.08")
    its.append(mq("%s buys 4 cushions at $12 each, before GST. How much does %s pay after 9%% GST?" % (n, he),
                  D("52.32"), [D(57), D("13.08"), D("43.68")],
                  "Price before GST: 4 × $12 = $48. GST: 9% of $48 = $4.32. Total: $48 + $4.32 = <b>$52.32</b>. "
                  "($13.08 is for 1 cushion only; $57 adds $9; $43.68 subtracts the GST.)"))
    assert len(its) == 20
    return {"title": "Price after GST", "items": its}


# ============================================================ set 3: discount then GST
def dg(p, r):
    return after_gst(sale(p, r))


def set_receipt(P):
    its = []
    its.append(mcq("A $50 bag is sold at a 20% discount. Then 9% GST is added. GST is worked out on which amount?",
                   "$40, the sale price", ["$50, the usual price", "$10, the discount", "$30, the usual price minus 20"],
                   "You pay GST on the price you actually pay. 20% of $50 = $10, so the sale price is $50 − $10 = <b>$40</b>, "
                   "and GST is 9% of $40."))
    rec = card_svg("Receipt", [("Football boots", money2(64)), ("Discount 25%", "?")],
                   [("Sale price", ""), ("GST 9%", ""), ("Total", "")])
    its.append(mq(fig(rec) + "How much is the discount on this receipt?", D(16), [D(25), D(48), D(39)],
                  "25% of $64 = $64 ÷ 4 = <b>$16</b>. ($25 uses the percentage as dollars; $48 is the sale price.)"))
    assert dg(45, 20) == D("39.24") and D(36) + gst(45) == D("40.05")
    its.append(mq("The usual price of a school bag is $45. It is sold at a 20% discount. Then 9% GST is added. How much do you pay?",
                  D("39.24"), [D("40.05"), D("49.05"), D(36)],
                  "Sale price: $45 − $9 = $36. GST: 9% of $36 = $3.24. Pay: $36 + $3.24 = <b>$39.24</b>. "
                  "($40.05 adds GST on the usual price; $49.05 forgets the discount; $36 forgets the GST.)"))
    rec = card_svg("Receipt", [("Rain jacket", money2(80)), ("Discount 25%", "−" + money2(20))],
                   [("Sale price", money2(60)), ("GST 9%", "?"), ("Total", "")])
    its.append(mq(fig(rec) + "How much is the GST on this receipt?", gst(60), [D("7.20"), D(9), D("1.80")],
                  "GST is 9% of the sale price: 9% of $60 = 9 × $0.60 = <b>$5.40</b>. "
                  "($7.20 is GST on the usual price $80; $1.80 is GST on the discount.)"))
    rec = card_svg("Receipt", [("Rain jacket", money2(80)), ("Discount 25%", "−" + money2(20))],
                   [("Sale price", money2(60)), ("GST 9%", money2(D("5.40"))), ("Total", "?")])
    its.append(mq(fig(rec) + "What is the total on this receipt?", dg(80, 25), [D("67.20"), D("87.20"), D(60)],
                  "Total = sale price + GST = $60.00 + $5.40 = <b>$65.40</b>. "
                  "($67.20 adds GST on $80; $87.20 forgets the discount.)"))
    assert dg(100, 10) == D("98.10")
    its.append(mq("A jacket costs $100. It is sold at a 10% discount, and 9% GST is added. What is the price after GST?",
                  D("98.10"), [D(99), D(109), D(90)],
                  "Sale price: $100 − $10 = $90. GST: 9% of $90 = $8.10. Price: $90 + $8.10 = <b>$98.10</b>. "
                  "($99 adds GST on $100; $109 forgets the discount; $90 forgets the GST.)"))
    assert dg(200, 15) == D("185.30") and 170 + 18 == 188
    its.append(mq("A bicycle costs $200. It is sold at a 15% discount, and 9% GST is added. How much does it cost?",
                  D("185.30"), [D(188), D(218), D(194)],
                  "Discount: 15% of $200 = $30, so the sale price is $170. GST: 9% of $170 = $15.30. "
                  "Total: $170 + $15.30 = <b>$185.30</b>. ($188 adds GST on $200; $194 subtracts 15 dollars and adds 9 dollars.)"))
    assert dg(60, 50) == D("32.70")
    its.append(mq("A pair of shoes costs $60. It is sold at 50% off, and 9% GST is added. What is the price after GST?",
                  D("32.70"), [D("35.40"), D(30), D("65.40")],
                  "Sale price: half of $60 = $30. GST: 9% of $30 = $2.70. Total: $30 + $2.70 = <b>$32.70</b>. "
                  "($35.40 adds GST on $60; $30 forgets the GST; $65.40 forgets the discount.)"))
    assert dg(60, 10) == D("58.86")
    rec = card_svg("Receipt", [("Badminton racket", money2(35)), ("Shuttlecocks", money2(25)), ("Discount 10%", "?")],
                   [("Sale price", ""), ("GST 9%", ""), ("Total", "?")])
    its.append(mq(fig(rec) + "The shop takes 10% off the whole bill. Then 9% GST is added. What is the total?",
                  D("58.86"), [D("59.40"), D("65.40"), D(54)],
                  "Bill: $35 + $25 = $60. Discount: 10% of $60 = $6, so the sale price is $54. "
                  "GST: 9% of $54 = $4.86. Total: $54 + $4.86 = <b>$58.86</b>. "
                  "($59.40 adds GST on $60; $65.40 forgets the discount; $54 forgets the GST.)"))
    assert dg(120, 20) == D("104.64")
    its.append(mq("A standing fan costs $120. It is sold at a 20% discount, and 9% GST is added. What is the price after GST?",
                  D("104.64"), [D("106.80"), D("130.80"), D(96)],
                  "Sale price: $120 − $24 = $96. GST: 9% of $96 = $8.64. Total: $96 + $8.64 = <b>$104.64</b>. "
                  "($106.80 adds GST on $120; $130.80 forgets the discount.)"))
    assert gst(sale(75, 40)) == D("4.05")
    its.append(mq("A school bag costs $75. It is sold at a 40% discount. How much GST is paid on the sale price?",
                  D("4.05"), [D("6.75"), D("2.70"), D(9)],
                  "Discount: 40% of $75 = $30, so the sale price is $45. GST: 9% of $45 = <b>$4.05</b>. "
                  "($6.75 is GST on the usual price; $2.70 is GST on the discount.)"))
    assert after_gst(40) == D("43.60") and after_gst(50) - 10 == D("44.50")
    its.append(mq("A $50 board game is bought with a $10 voucher. GST is charged on the price after the voucher. What is the total?",
                  D("43.60"), [D("44.50"), D(49), D(40)],
                  "Voucher first: $50 − $10 = $40. GST: 9% of $40 = $3.60. Total: $40 + $3.60 = <b>$43.60</b>. "
                  "($44.50 adds GST before using the voucher; $49 adds $9.)"))
    assert dg(90, 30) == D("68.67")
    its.append(mq("A pair of goggles and a swim cap cost $90 in all. They are sold at a 30% discount, and 9% GST is added. What is the total?",
                  D("68.67"), [D("71.10"), D("98.10"), D(63)],
                  "Discount: 30% of $90 = $27, so the sale price is $63. GST: 9% of $63 = $5.67. "
                  "Total: $63 + $5.67 = <b>$68.67</b>. ($71.10 adds GST on $90; $98.10 forgets the discount.)"))
    n, he, his, him = P.next()
    assert dg(100, 20) == D("87.20")
    its.append(mcq("A shop gives 20%% off and then adds 9%% GST. %s says, “I pay 11%% less than the usual price.” Is %s right?" % (n, he),
                   "No, %s pays $87.20 for every $100" % he,
                   ["Yes, 20% − 9% = 11%", "No, %s pays $89 for every $100" % he, "No, %s pays $109 for every $100" % he],
                   "Try $100: 20% off gives $80. GST is 9% of $80 = $7.20, not $9. Total: <b>$87.20 for every $100</b>, "
                   "which is 12.8% less. The GST is worked out on the smaller sale price."))
    assert dg(250, 20) == 218
    its.append(mq("A study desk costs $250. It is sold at a 20% discount, and 9% GST is added. What is the price after GST?",
                  D(218), [D("222.50"), D("272.50"), D(200)],
                  "Sale price: $250 − $50 = $200. GST: 9% of $200 = $18. Total: $200 + $18 = <b>$218</b>. "
                  "($222.50 adds GST on $250; $272.50 forgets the discount.)"))
    assert dg(20, 10) == D("19.62")
    its.append(mq("5 notebooks cost $4 each. The shop gives 10% off the total, and then adds 9% GST. How much do the 5 notebooks cost?",
                  D("19.62"), [D("19.80"), D("21.80"), D(18)],
                  "Total: 5 × $4 = $20. Sale price: $20 − $2 = $18. GST: 9% of $18 = $1.62. "
                  "Pay: $18 + $1.62 = <b>$19.62</b>. ($19.80 adds GST on $20; $21.80 forgets the discount.)"))
    assert dg(1500, 10) == D("1471.50") and 1350 + 135 == 1485
    its.append(mq("A laptop costs $1500. It is sold at a 10% discount, and 9% GST is added. What is the price after GST?",
                  D("1471.50"), [D(1485), D(1635), D(1350)],
                  "Sale price: $1500 − $150 = $1350. GST: 9% of $1350 = $121.50. "
                  "Total: $1350 + $121.50 = <b>$1471.50</b>. ($1485 adds GST on $1500; $1635 forgets the discount.)"))
    n, he, his, him = P.next()
    assert dg(30, 10) == D("29.43") and 50 - D("29.43") == D("20.57")
    its.append(mq("%s buys a $30 storybook at a 10%% discount. 9%% GST is added. %s pays with a $50 note. How much change does %s get?" % (n, cap(he), he),
                  D("20.57"), [D("20.30"), D(23), D("17.30")],
                  "Sale price: $30 − $3 = $27. GST: 9% of $27 = $2.43. Total: $29.43. Change: $50 − $29.43 = <b>$20.57</b>. "
                  "($20.30 uses GST on $30; $23 forgets the GST; $17.30 forgets the discount.)"))
    assert dg(60, 20) == D("52.32") and after_gst(50) == D("54.50")
    its.append(mcq("Shop A sells a bag for $60 at a 20% discount. Shop B sells the same bag for $50 with no discount. "
                   "Both shops add 9% GST. Which shop is cheaper?",
                   "Shop A, by $2.18", ["Shop B, by $2.18", "Shop A, by $2", "They cost the same"],
                   "Shop A: $60 − $12 = $48, and $48 + $4.32 GST = $52.32. Shop B: $50 + $4.50 GST = $54.50. "
                   "$54.50 − $52.32 = $2.18, so <b>Shop A is cheaper by $2.18</b>. ($2 forgets the GST.)"))
    n, he, his, him = P.next()
    assert dg(150, 20) == D("130.80") and 150 - D("130.80") == D("19.20")
    its.append(mq("The usual price of a pair of inline skates is $150. %s buys it at a 20%% discount, and 9%% GST is added. "
                  "%s pays with three $50 notes. How much change does %s get?" % (n, cap(he), he),
                  D("19.20"), [D("16.50"), D(30), D("40.80")],
                  "Sale price: $150 − $30 = $120. GST: 9% of $120 = $10.80. Total: $130.80. "
                  "Change: $150 − $130.80 = <b>$19.20</b>. ($16.50 uses GST on $150; $30 forgets the GST; $40.80 subtracts the GST.)"))
    assert len(its) == 20
    return {"title": "Discount, then GST on a receipt", "items": its}


# ============================================================ set 4: annual interest
def set_interest(P):
    its = []
    its.append(mcq("A bank pays interest of 2% per annum. What does “per annum” mean?", "For each year",
                   ["For each month", "For each day", "Once only, when you open the account"],
                   "“Per annum” means <b>for each year</b>. 2% per annum means the bank pays 2% of your savings for each year."))
    its.append(mq("Ali puts $5000 in a bank. The interest rate is 2% per annum. How much interest does he get after 1 year?",
                  interest(5000, 2), [D(10), D(5100), D(1000)],
                  "1% of $5000 = $50, so 2% = <b>$100</b>. ($5100 is the amount in the bank, not the interest; $1000 is 20%.)"))
    its.append(mq("Ali puts $5000 in a bank at 2% interest per annum. How much is in his account after 1 year?",
                  5000 + interest(5000, 2), [D(100), D(5002), D(4900)],
                  "Interest: 2% of $5000 = $100. Amount after 1 year: $5000 + $100 = <b>$5100</b>. "
                  "($100 is only the interest; $5002 adds $2; $4900 subtracts the interest.)"))
    its.append(mq("$1000 is saved in a bank at 3% interest per annum. How much interest is earned in 1 year?",
                  interest(1000, 3), [D(3), D(1030), D(300)],
                  "1% of $1000 = $10, so 3% = <b>$30</b>. ($3 uses the percentage as dollars; $1030 is the amount in the bank.)"))
    its.append(mq("$2000 is saved in a bank at 1% interest per annum. How much interest is earned in 1 year?",
                  interest(2000, 1), [D(1), D(2020), D(200)],
                  "1% of $2000 = $2000 ÷ 100 = <b>$20</b>. ($200 is 10%; $2020 is the amount in the bank.)"))
    its.append(mq("$800 is saved in a bank at 5% interest per annum. How much is in the account after 1 year?",
                  800 + interest(800, 5), [D(40), D(805), D(760)],
                  "Interest: 10% of $800 = $80, so 5% = $40. Amount: $800 + $40 = <b>$840</b>. "
                  "($40 is only the interest; $805 adds $5; $760 subtracts the interest.)"))
    its.append(mq("$3000 is saved in a bank at 2.5% interest per annum. How much interest is earned in 1 year?",
                  interest(3000, D("2.5")), [D(750), D(3075), D("7.50")],
                  "1% of $3000 = $30, so 2.5% = 2.5 × $30 = <b>$75</b>. ($750 is 25%; $3075 is the amount in the bank.)"))
    its.append(mcq("$4000 is saved at 3% interest per annum. Which gives the interest for 1 year?", "3% of $4000",
                   ["$4000 + $3", "103% of $4000", "$4000 ÷ 3"],
                   "The interest for 1 year is <b>3% of $4000</b> = $120. 103% of $4000 = $4120 is the amount in the bank, "
                   "not the interest."))
    its.append(mq("$6000 is saved in a bank at 1.5% interest per annum. How much interest is earned in 1 year?",
                  interest(6000, D("1.5")), [D(9), D(6090), D(900)],
                  "1% of $6000 = $60 and 0.5% = $30, so 1.5% = <b>$90</b>. ($900 is 15%; $6090 is the amount in the bank.)"))
    its.append(mq("Mrs Ng puts $10" + NB + "000 in a bank at 2% interest per annum. How much is in her account after 1 year?",
                  10000 + interest(10000, 2), [D(200), D(10002), D(12000)],
                  "Interest: 1% of $10" + NB + "000 = $100, so 2% = $200. Amount: $10" + NB + "000 + $200 = <b>$10" + NB + "200</b>. "
                  "($200 is only the interest; $12" + NB + "000 adds 20%.)"))
    rec = card_svg("Savings account", [("Saved on 1 Jan", money2(2500)), ("Interest rate", "4% per annum")],
                   [("Interest for 1 year", "?"), ("Amount after 1 year", "")])
    its.append(mq(fig(rec) + "How much interest is earned in 1 year?", interest(2500, 4), [D(4), D(2600), D(1000)],
                  "1% of $2500 = $25, so 4% = 4 × $25 = <b>$100</b>. ($2600 is the amount after 1 year; $1000 is 40%.)"))
    rec = card_svg("Savings account", [("Saved on 1 Jan", money2(1200)), ("Interest rate", "3% per annum")],
                   [("Interest for 1 year", ""), ("Amount after 1 year", "?")])
    its.append(mq(fig(rec) + "How much is in the account after 1 year?", 1200 + interest(1200, 3), [D(36), D(1203), D(1560)],
                  "Interest: 1% of $1200 = $12, so 3% = $36. Amount: $1200 + $36 = <b>$1236</b>. "
                  "($36 is only the interest; $1560 adds 30%.)"))
    its.append(mcq("$4000 earns $80 interest in 1 year. What is the interest rate per annum?", "2%",
                   ["80%", "50%", "0.2%"],
                   "1% of $4000 = $40. $80 is 2 × $40, so the rate is <b>2%</b> per annum. "
                   "(80% uses the dollars; 50% comes from $4000 ÷ $80.)"))
    n, he, his, him = P.next()
    assert interest(3000, 2) - interest(3000, D("1.5")) == 15
    its.append(mq("%s has $3000 to save. Bank A pays 2%% per annum. Bank B pays 1.5%% per annum. How much more interest does Bank A pay in 1 year?" % n,
                  D(15), [D("0.50"), D(60), D(45)],
                  "Bank A: 2% of $3000 = $60. Bank B: 1.5% of $3000 = $45. Difference: $60 − $45 = <b>$15</b>. "
                  "($0.50 subtracts the rates as dollars; $60 is Bank A’s interest.)"))
    its.append(mq("Mr Rahman saves $8000 at 2.5% interest per annum. How much is in his account after 1 year?",
                  8000 + interest(8000, D("2.5")), [D(8025), D(200), D(10000)],
                  "Interest: 1% of $8000 = $80, so 2.5% = 2.5 × $80 = $200. Amount: $8000 + $200 = <b>$8200</b>. "
                  "($200 is only the interest; $8025 adds $25; $10" + NB + "000 adds 25%.)"))
    n, he, his, him = P.next()
    its.append(mcq("%s’s account had $1500 at the start of the year and $1530 at the end. No money was added or taken out. "
                   "What is the interest rate per annum?" % n,
                   "2%", ["30%", "50%", "20%"],
                   "Interest: $1530 − $1500 = $30. 1% of $1500 = $15, and $30 = 2 × $15, so the rate is <b>2%</b>. "
                   "(30% uses the dollars; 50% comes from $1500 ÷ $30; 20% is 10 times too big.)"))
    n, he, his, him = P.next()
    assert interest(2000, 2) + interest(3000, 3) == 130
    its.append(mq("%s puts $2000 in Bank A at 2%% per annum and $3000 in Bank B at 3%% per annum. How much interest does %s get in 1 year altogether?" % (n, he),
                  D(130), [D(125), D(250), D(5130)],
                  "Bank A: 2% of $2000 = $40. Bank B: 3% of $3000 = $90. Total: $40 + $90 = <b>$130</b>. "
                  "($125 uses 2.5% on $5000; $250 uses 5% on $5000; $5130 is the total amount in the banks.)"))
    its.append(mq("$20" + NB + "000 is kept in a fixed deposit at 3% interest per annum. How much interest is earned in 1 year?",
                  interest(20000, 3), [D(60), D(6000), D(20600)],
                  "1% of $20" + NB + "000 = $200, so 3% = <b>$600</b>. ($6000 is 30%; $20" + NB + "600 is the amount, not the interest.)"))
    its.append(mq("Mr Tan borrows $5000 from a bank at 4% interest per annum. How much must he pay back after 1 year?",
                  5000 + interest(5000, 4), [D(200), D(5004), D(4800)],
                  "When you borrow, you pay back the loan plus interest. Interest: 4% of $5000 = $200. "
                  "Pay back: $5000 + $200 = <b>$5200</b>. ($200 is only the interest; $4800 subtracts it.)"))
    n, he, his, him = P.next()
    assert 2400 + interest(2400, D("2.5")) == 2460
    its.append(mq("%s saves $2400 at 2.5%% interest per annum. %s hopes to have $2500 after 1 year. How much less than $2500 will %s have?" % (n, cap(he), he),
                  D(40), [D(100), D(60), D(2460)],
                  "Interest: 1% of $2400 = $24, so 2.5% = $60. Amount: $2400 + $60 = $2460. "
                  "Less than $2500 by $2500 − $2460 = <b>$40</b>. ($100 forgets the interest; $60 is the interest; $2460 is the amount.)"))
    assert len(its) == 20
    return {"title": "Annual interest", "items": its}


# ============================================================ set 5: word problems and comparing deals
def set_words(P):
    its = []
    assert sale(35, 20) == 28
    its.append(mq(fig(bar_model_svg(5, 1, "$35", "20%", "?", "discount", "sale price")) +
                  "A box of mandarin oranges costs $35 before Chinese New Year. During a sale, it is sold at a 20% discount. "
                  "What is the sale price?",
                  D(28), [D(15), D(7), D(42)],
                  "20% = 1/5, so the bar has 5 units. 5 units = $35, 1 unit = $7. Sale price = 4 units = 4 × $7 = <b>$28</b>. "
                  "($15 subtracts 20 dollars; $7 is the discount; $42 adds it.)"))
    n, he, his, him = P.next()
    assert sale(84, 25) == 63
    its.append(mq(fig(bar_model_svg(4, 1, "$84", "25%", "?", "discount", "price paid")) +
                  "%s buys a pair of roller skates. The usual price is $84. %s gets a 25%% discount. How much does %s pay?" % (n, cap(he), he),
                  D(63), [D(59), D(21), D(105)],
                  "25%% = 1/4, so the bar has 4 units. 4 units = $84, 1 unit = $21. %s pays 3 units = 3 × $21 = <b>$63</b>. "
                  "($59 subtracts 25 dollars; $21 is the discount.)" % cap(he)))
    assert sale(60, 25) == 45 and sale(52, 10) == D("46.80")
    its.append(mcq("Shop A sells a bag at $60 with 25% off. Shop B sells the same bag at $52 with 10% off. Which shop is cheaper?",
                   "Shop A, by $1.80", ["Shop B, by $1.80", "Shop A, by $7", "They cost the same"],
                   "Shop A: $60 − $15 = $45. Shop B: $52 − $5.20 = $46.80. <b>Shop A is cheaper by $1.80</b>. "
                   "(Shop A by $7 subtracts the percentages as dollars: $35 and $42.)"))
    n, he, his, him = P.next()
    assert sale(80, 30) == 56
    its.append(mcq("A bag costs $80. %s can use either a 30%% discount or a $25 voucher, not both. Which is the better deal?" % n,
                   "The $25 voucher, by $1", ["30% off, by $5", "30% off, by $1", "They are the same"],
                   "30% of $80 = $24, so 30% off gives $56. The voucher gives $80 − $25 = $55. "
                   "<b>The $25 voucher is better by $1</b>. (30% off by $5 compares 30 with 25.)"))
    n, he, his, him = P.next()
    its.append(mq("During a National Day sale, everything is 15%% off. %s buys a pair of shoes at $40 and a bag at $60. How much does %s pay?" % (n, he),
                  sale(100, 15), [D(70), D(15), D(115)],
                  "Total: $40 + $60 = $100. Discount: 15% of $100 = $15. Pay: $100 − $15 = <b>$85</b>. "
                  "($70 takes $15 off each item; $15 is the discount; $115 adds it.)"))
    n, he, his, him = P.next()
    assert 3000 + interest(3000, 2) + 500 == 3560 and 3500 + interest(3500, 2) == 3570
    its.append(mq("%s puts $3000 in a bank at 2%% interest per annum. After 1 year, the interest is added, and then %s puts in another $500. "
                  "How much is in the account now?" % (n, he),
                  D(3560), [D(3570), D(560), D(3060)],
                  "Interest: 2% of $3000 = $60, so after 1 year there is $3060. Add $500: $3060 + $500 = <b>$3560</b>. "
                  "($3570 gives interest on the $500 too, but it was put in after the year; $3060 forgets the $500.)"))
    n, he, his, him = P.next()
    assert dg(75, 20) == D("65.40") and 100 - D("65.40") == D("34.60") and 100 - after_gst(75) == D("18.25")
    its.append(mq("%s has $100. %s buys a $75 video game at a 20%% discount, and 9%% GST is added. How much money does %s have left?" % (n, cap(he), he),
                  D("34.60"), [D(40), D(25), D("18.25")],
                  "Sale price: $75 − $15 = $60. GST: 9% of $60 = $5.40. Total: $65.40. Left: $100 − $65.40 = <b>$34.60</b>. "
                  "($40 forgets the GST; $25 forgets the discount and the GST; $18.25 forgets the discount.)"))
    assert dg(240, 25) == D("196.20")
    its.append(mq("Mrs Lim buys an air purifier at a year-end sale. The usual price is $240. It is sold at a 25% discount, and 9% GST is added. "
                  "How much does she pay?",
                  D("196.20"), [D("201.60"), D("261.60"), D(180)],
                  "Sale price: $240 − $60 = $180. GST: 9% of $180 = $16.20. Total: $180 + $16.20 = <b>$196.20</b>. "
                  "($201.60 adds GST on $240; $261.60 forgets the discount; $180 forgets the GST.)"))
    n, he, his, him = P.next()
    assert interest(5000, 2) - interest(5000, D("1.8")) == 10
    its.append(mq("%s has $5000. Bank A pays 2%% interest per annum. Bank B pays 1.8%% per annum. How much more interest does Bank A pay in 1 year?" % n,
                  D(10), [D("0.20"), D(90), D(100)],
                  "Bank A: 2% of $5000 = $100. Bank B: 1.8% of $5000 = $90. Difference: <b>$10</b>. "
                  "Or: 0.2% of $5000 = $10. ($0.20 subtracts the rates as dollars; $100 is Bank A’s interest.)"))
    n, he, his, him = P.next()
    assert pct(60, 10) + pct(40, 25) == 16 and pct(60, 25) + pct(40, 10) == 19
    its.append(mq("A pair of shoes costs $60 and a cap costs $40. The shoes are 10%% off and the cap is 25%% off. How much does %s save on both?" % n,
                  D(16), [D(35), D(19), D(84)],
                  "Shoes: 10% of $60 = $6. Cap: 25% of $40 = $10. Saved: $6 + $10 = <b>$16</b>. "
                  "($35 adds the percentages as dollars; $19 swaps the two percentages; $84 is the amount paid.)"))
    assert sale(90, 10) - 5 == 76 and sale(85, 10) == D("76.50")
    its.append(mq(fig(bar_model_svg(10, 1, "$90", "10%", "?", "discount", "sale price")) +
                  "A school bag costs $90. The shop takes 10% off first. Then a $5 voucher is used. How much is paid?",
                  D(76), [D(75), D("76.50"), D(86)],
                  "10 units = $90, 1 unit = $9. Sale price: 9 units = $81. Voucher: $81 − $5 = <b>$76</b>. "
                  "($75 subtracts 10 dollars; $76.50 uses the voucher first; $86 forgets the 10% off.)"))
    n, he, his, him = P.next()
    assert sale(100, 10) == 90 and 100 - D("2.50") == D("97.50")
    its.append(mq("%s’s family buys 4 tickets to a school concert at $25 each. They get a 10%% discount on the total. How much do they pay?" % n,
                  D(90), [D("97.50"), D(60), D(10)],
                  "Total: 4 × $25 = $100. Discount: 10% of $100 = $10. Pay: $100 − $10 = <b>$90</b>. "
                  "($97.50 takes 10% off one ticket only; $60 takes $10 off each ticket; $10 is the discount.)"))
    its.append(mcq("Two shirts cost $30 each. Shop A: buy 1, get the second at 50% off. Shop B: 20% off both shirts. Which shop is cheaper?",
                   "Shop A, by $3", ["Shop B, by $3", "Shop A, by $15", "They cost the same"],
                   "Shop A: $30 + $15 = $45. Shop B: 20% of $60 = $12 off, so $48. <b>Shop A is cheaper by $3</b>. "
                   "($15 is only the discount on the second shirt.)"))
    assert sale(48, 10) - sale(48, 25) == D("7.20")
    its.append(mq("A sports shop sells a jersey for $48. Members get 25% off. Non-members get 10% off. How much more does a non-member pay?",
                  D("7.20"), [D(15), D(36), D("43.20")],
                  "Member: $48 − $12 = $36. Non-member: $48 − $4.80 = $43.20. Difference: $43.20 − $36 = <b>$7.20</b>. "
                  "Or: 15% of $48 = $7.20. ($15 uses the percentages as dollars; $36 and $43.20 are the two prices.)"))
    n, he, his, him = P.next()
    assert sale(25, 20) == 20
    its.append(mcq("At a book fair, a $25 storybook is sold for $20. What percentage discount does %s get?" % n,
                   "20%", ["5%", "25%", "80%"],
                   "Discount: $25 − $20 = $5. Compare with the usual price: 5/25 = 20/100 = <b>20%</b>. "
                   "(5% uses the dollars; 25% divides by the sale price $20; 80% is the part paid.)"))
    assert sale(135, 20) == 108 and after_gst(108) == D("117.72") and 108 + gst(135) == D("120.15")
    its.append(mq("Mr Rahman buys 3 shirts at $45 each for Hari Raya Puasa. He gets 20% off the total, and 9% GST is added. How much does he pay?",
                  D("117.72"), [D("120.15"), D("147.15"), D(108)],
                  "Total: 3 × $45 = $135. Sale price: $135 − $27 = $108. GST: 9% of $108 = $9.72. "
                  "Pay: $108 + $9.72 = <b>$117.72</b>. ($120.15 adds GST on $135; $147.15 forgets the discount.)"))
    n, he, his, him = P.next()
    assert after_gst(120) == D("130.80") and sale(135, 5) == D("128.25")
    its.append(mcq("%s’s mother can buy a vacuum cleaner online for $120 plus 9%% GST, or in a shop for $135 with GST included and 5%% off. "
                   "Which is cheaper?" % n,
                   "The shop, by $2.55", ["Online, by $2.55", "Online, by $8.25", "The shop, by $15"],
                   "Online: $120 + $10.80 GST = $130.80. Shop: 5% of $135 = $6.75 off, so $128.25. "
                   "$130.80 − $128.25 = $2.55, so <b>the shop is cheaper by $2.55</b>. (Online by $8.25 forgets the GST.)"))
    assert gst(21) == D("1.89") and 39 + D("1.89") == D("40.89") and 39 - D("3.51") == D("35.49")
    its.append(mq("Mdm Wong buys 3 bowls of laksa at $6 each and 3 cups of bubble tea at $7 each, before GST. "
                  "How much does she pay after 9% GST?",
                  after_gst(39), [D(48), D("40.89"), D("35.49")],
                  "Food: 3 × $6 = $18. Drinks: 3 × $7 = $21. Total before GST: $39. GST: 9% of $39 = $3.51. "
                  "Pay: $39 + $3.51 = <b>$42.51</b>. ($48 adds $9; $40.89 adds GST on the drinks only; $35.49 subtracts the GST.)"))
    n, he, his, him = P.next()
    assert 1200 + interest(1200, 2) - dg(150, 20) == D("1093.20") and 1200 - dg(150, 20) == D("1069.20")
    assert 1200 + interest(1200, 2) - 150 == 1074
    its.append(mq("%s has $1200 in a bank at 2%% interest per annum. After 1 year, %s takes out money to buy a $150 bicycle "
                  "at a 20%% discount, with 9%% GST added. How much is left in the bank?" % (n, he),
                  D("1093.20"), [D(1080), D("1069.20"), D(1074)],
                  "After 1 year: $1200 + 2% of $1200 = $1200 + $24 = $1224. Bicycle: $150 − $30 = $120, and $120 + $10.80 GST = $130.80. "
                  "Left: $1224 − $130.80 = <b>$1093.20</b>. ($1069.20 forgets the interest; $1074 forgets the discount and the GST; $1080 forgets the interest and the GST.)"))
    n, he, his, him = P.next()
    assert dg(1800, 15) == D("1667.70") and after_gst(1550) == D("1689.50") and D("1689.50") - D("1667.70") == D("21.80")
    its.append(mcq("%s’s father wants a $1800 television. Shop A gives 15%% off. Shop B gives $250 off. Both shops then add 9%% GST. "
                   "Which shop is cheaper?" % n,
                   "Shop A, by $21.80", ["Shop A, by $20", "Shop B, by $21.80", "Shop B, by $20"],
                   "Shop A: 15% of $1800 = $270 off, so $1530, and $1530 + $137.70 GST = $1667.70. "
                   "Shop B: $1550, and $1550 + $139.50 GST = $1689.50. Difference: $1689.50 − $1667.70 = $21.80. "
                   "<b>Shop A is cheaper by $21.80</b>. ($20 is the difference before GST.)"))
    assert len(its) == 20, len(its)
    return {"title": "Word problems and comparing deals", "items": its}


# ============================================================ lesson
def body_html():
    assert sale(45, 20) == 36 and dg(45, 20) == D("39.24") and interest(5000, 2) == 100
    return (
        "<h2>Discount</h2>"
        "<p>A discount is an amount taken off the usual price. It is a percentage of the <b>usual price</b>. "
        "Sale price = usual price − discount.</p>"
        "<figure class='sn-fig'>" + bar_model_svg(5, 1, "$45", "$9", "$36", "20% discount", "sale price") +
        "<figcaption>20% = 1/5. 5 units = $45, so 1 unit = $9. The discount is 1 unit ($9). The sale price is 4 units ($36).</figcaption></figure>" +
        ex("Example 1", "The usual price of a school bag is $45. It is sold at a 20% discount. Find the sale price.",
           "Discount: 20% of $45 = 20/100 × $45 = $9. Sale price: $45 − $9 = $36.", "$36") +
        "<h2>GST</h2>"
        "<p>In Singapore, GST (Goods and Services Tax) is <b>9%</b>. It is added to the price. "
        "Price after GST = price before GST + 9% of the price before GST.</p>" +
        ex("Example 2", "An item costs $80 before GST. Find the price after 9% GST.",
           "GST: 9% of $80 = 9/100 × $80 = $7.20. Price after GST: $80 + $7.20 = $87.20.", "$87.20") +
        "<h2>Discount, then GST</h2>"
        "<p>When an item is on sale, take off the discount first. GST is worked out on the <b>sale price</b>, the price you actually pay.</p>"
        "<figure class='sn-fig'>" + card_svg("Receipt", [("School bag", money2(45)), ("Discount 20%", "−" + money2(9))],
                                             [("Sale price", money2(36)), ("GST 9%", money2(D("3.24"))), ("Total", money2(D("39.24")))]) +
        "<figcaption>GST is 9% of $36, not 9% of $45: $36 + $3.24 = $39.24.</figcaption></figure>"
        "<h2>Annual interest</h2>"
        "<p>A bank pays interest on your savings. “Per annum” means for each year. "
        "The interest for 1 year is a percentage of the money saved. The amount in the bank after 1 year = money saved + interest.</p>" +
        ex("Example 3", "Siti saves $5000 in a bank at 2% interest per annum. How much is in her account after 1 year?",
           "Interest: 2% of $5000 = 2/100 × $5000 = $100. Amount: $5000 + $100 = $5100.", "$5100") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["20% off $45 = $45 − $20 = $25", "Find 20% of $45 ($9), then subtract: $36"],
            ["Adding the discount: $45 + $9 = $54", "A discount is taken away: $45 − $9 = $36"],
            ["GST on the usual price after a discount", "Work out 9% of the sale price"],
            ["Adding $9 for 9% GST", "9% GST on $80 is 9/100 × $80 = $7.20"],
            ["Giving $5100 as the interest", "The interest is $100; $5100 is the amount in the bank"],
        ])
    )


FAQ = [
    {"q": "What is taught in P5 percentage?",
     "a": "Primary 5 students learn to write a part of a whole as a percentage and to find a percentage of an amount. "
          "They use this to find discount, GST and annual interest, as in the MOE syllabus."},
    {"q": "How do I calculate GST in Singapore?",
     "a": "GST in Singapore is 9%, so find 9% of the price and add it: 9% GST on $80 is $7.20, and the price after GST is $87.20. "
          "If there is a discount, take it off first and work out GST on the sale price."},
    {"q": "What is the most common mistake with discount?",
     "a": "The most common mistake is subtracting the percentage as dollars, for example 20% off $45 as $45 − $20 = $25. "
          "Find 20% of $45 first ($9), then subtract to get the sale price of $36."},
    {"q": "How do I explain annual interest to my child?",
     "a": "Tell your child that the bank pays a percentage of the money saved for each year it stays there. "
          "$5000 at 2% per annum earns $100 interest in 1 year, so the account then has $5100."},
]


def gen():
    rnd = random.Random(65809)
    P = People(rnd)
    sets = [set_discount(P), set_gst(P), set_receipt(P), set_interest(P), set_words(P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in keys, it["q"]
            keys.add(it["q"])
            assert it["q"].count("<svg") <= 1
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x and "..." not in x, x
                assert not re.search(r"\d,\d{3}", x), x
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-5", "slug": "discount-gst-and-interest", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 5 Discount, GST and Annual Interest",
        "seo_title": "P5 Discount, GST and Interest Worksheets: Free Primary 5 Maths with Answers (MOE Syllabus)",
        "short_title": "Discount, GST and interest",
        "domain": "Number and Algebra",
        "standard_code": "Primary 5: Percentage",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Finding discount, GST and annual interest",
        "meta_desc": "Free P5 maths practice on percentage: discount and sale price, 9% GST, receipts and annual interest. "
                     "100 questions with answers and bar models.",
        "key_big": "Take the discount off the usual price first, then add 9% GST on the sale price.",
        "key_sub": "20% off $45: discount $9, sale price $36. GST: 9% of $36 = $3.24, so you pay $39.24.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    mark_large(u, "Bar model")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
