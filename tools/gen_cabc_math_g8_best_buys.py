# -*- coding: utf-8 -*-
"""
BC Grade 8 Math: Best Buys (BC Mathematics Curriculum, Financial literacy: best buys)
  python3 tools/gen_cabc_math_g8_best_buys.py
Unit prices, comparing sizes, discounts and coupons, BC sales tax (GST 5% + PST 7%) on purchases, and best-buy
decisions. All money is worked with decimal.Decimal; each tax is rounded to the cent (half up, and no price is used
whose GST or PST ends in exactly half a cent). Canada has no pennies: cash totals round to the nearest 5 cents,
card payments are exact. BC style: 4-digit numbers without a separator, $ and the cent sign.
Helpers are copied from gen_cabc_math_g7_financial_percentages.py. HTML attributes use single quotes.
"""
import json, math, os, random, re
from decimal import Decimal as D, ROUND_HALF_UP
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-8")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
GREY = "#6b6259"
PAPER = "#fffdf5"
EDGE = "#b8b0a0"
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


def taxed(p):
    return D(p) + both(p)


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


def r2(x):
    return D(x).quantize(CENT, rounding=ROUND_HALF_UP)


def cap(s):
    return s[0].upper() + s[1:]


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
    assert len(w) == 3, (q, wrongs)
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


def coupon_svg(line1, line2):
    """A dashed-edge store coupon."""
    W, H = 220, 96
    s = [
        "<rect x='3' y='3' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='2' stroke-dasharray='7 4'/>" % (W - 6, H - 6, PAPER, GREEN),
        txt(W // 2, 30, "COUPON", 15, bold=True, col=GREEN),
        txt(W // 2, 62, line1, 26, bold=True),
        txt(W // 2, 84, line2, 14, col=GREY),
    ]
    return svg_wrap(W, H, "".join(s), "Coupon: %s, %s" % (line1, line2))


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


# ============================================================ set 1: unit prices
def up(q, price, qty, ans, wrongs, e, figure=None):
    assert D(price) / D(qty) == D(ans) or r2(D(price) / D(qty)) == D(ans), (q, price, qty, ans)
    if figure:
        q = fig(figure) + q
    return mq(q, ans, wrongs, e)


def set_unit(P):
    its = []
    its.append(up("A 4-pack of yogurt cups costs $6.00. What is the price per cup?", 6, 4, D("1.50"),
                  [D(24), D("0.67"), D(2)],
                  "Unit price = price ÷ number of items. $6.00 ÷ 4 = <b>$1.50 per cup</b>. "
                  "($24.00 multiplies; $0.67 divides the wrong way, 4 ÷ 6; $2.00 subtracts.)"))
    its.append(up("A 2 L carton of milk costs $4.80. What is the price per litre?", "4.80", 2, D("2.40"),
                  [D("9.60"), D("0.42"), D("2.80")],
                  "$4.80 ÷ 2 = <b>$2.40 per litre</b>. ($9.60 multiplies; $0.42 is 2 ÷ 4.80, the wrong way round; $2.80 subtracts 2.)"))
    its.append(up("A box of 12 granola bars costs $5.40. What is the price per bar?", "5.40", 12, D("0.45"),
                  [D("0.54"), D("2.22"), D("64.80")],
                  "$5.40 ÷ 12 = <b>$0.45 per bar</b> (45¢). ($0.54 divides by 10; $2.22 is 12 ÷ 5.40; $64.80 multiplies.)"))
    its.append(up("A 3 kg bag of Okanagan apples costs $5.97. What is the price per kilogram?", "5.97", 3, D("1.99"),
                  [D("17.91"), D("0.50"), D("2.97")],
                  "$5.97 ÷ 3 = <b>$1.99 per kilogram</b>. ($17.91 multiplies; $0.50 is 3 ÷ 5.97; $2.97 subtracts 3.)",
                  figure=tags_svg([("Apples", "3 kg", D("5.97"))])))
    its.append(up("A 500 g block of cheese costs $7.50. What is the price per 100 g?", "7.50", 5, D("1.50"),
                  [D(15), D("0.15"), D("37.50")],
                  "500 g is 5 groups of 100 g. $7.50 ÷ 5 = <b>$1.50 per 100 g</b>. "
                  "($15.00 is the price per kilogram; $0.15 divides by 50; $37.50 multiplies by 5.)"))
    its.append(up("A 6-pack of sparkling water costs $4.50. What is the price per can?", "4.50", 6, D("0.75"),
                  [D(27), D("1.33"), D("0.45")],
                  "$4.50 ÷ 6 = <b>$0.75 per can</b> (75¢). ($27.00 multiplies; $1.33 is 6 ÷ 4.50; $0.45 divides by 10.)"))
    its.append(mcq("A 400 g bag of trail mix costs $6.00. Which calculation gives the price per 100 g?", "$6.00 ÷ 4",
                   ["4 ÷ $6.00", "$6.00 × 4", "$6.00 ÷ 400"],
                   "400 g is 4 groups of 100 g, so share the price among 4: <b>$6.00 ÷ 4</b> = $1.50. "
                   "4 ÷ $6.00 is upside down, and $6.00 ÷ 400 gives the price per gram."))
    its.append(up("A 1.5 kg bag of rice costs $4.50. What is the price per kilogram?", "4.50", "1.5", D(3),
                  [D("6.75"), D("0.33"), D("2.25")],
                  "$4.50 ÷ 1.5 = <b>$3.00 per kilogram</b>. Check: 1.5 × $3.00 = $4.50. "
                  "($6.75 multiplies; $0.33 is 1.5 ÷ 4.50; $2.25 divides by 2.)"))
    its.append(up("A 750 mL bottle of olive oil costs $9.00. What is the price per 100 mL?", 9, "7.5", D("1.20"),
                  [D(12), D("0.12"), D("6.75")],
                  "750 mL is 7.5 groups of 100 mL. $9.00 ÷ 7.5 = <b>$1.20 per 100 mL</b>. "
                  "($12.00 is the price per litre; $0.12 divides by 75; $6.75 multiplies by 0.75.)"))
    its.append(up("A pack of 8 AA batteries costs $11.92. What is the price per battery?", "11.92", 8, D("1.49"),
                  [D("95.36"), D("0.67"), D("3.92")],
                  "$11.92 ÷ 8 = <b>$1.49 per battery</b>. ($95.36 multiplies; $0.67 is 8 ÷ 11.92; $3.92 subtracts 8.)"))
    its.append(up("A 250 g box of BC blueberries costs $4.00. What is the price per kilogram?", 4, "0.25", D(16),
                  [D("1.60"), D("62.50"), D("0.16")],
                  "1 kg = 1000 g, which is 4 boxes of 250 g. 4 × $4.00 = <b>$16.00 per kilogram</b>. "
                  "($1.60 is the price per 100 g; $62.50 is 250 ÷ 4; $0.16 divides by 25.)"))
    its.append(up("A driver pays $70.00 for 40 L of gas. What is the price per litre?", 70, 40, D("1.75"),
                  [D("0.57"), D(30), D("17.50")],
                  "$70.00 ÷ 40 = <b>$1.75 per litre</b>. ($0.57 is 40 ÷ 70; $30.00 subtracts; $17.50 divides by 4.)"))
    its.append(up("A 2 kg bag of flour costs $5.20. What is the price per 100 g?", "5.20", 20, D("0.26"),
                  [D("2.60"), D("0.52"), D("0.13")],
                  "2 kg = 2000 g, which is 20 groups of 100 g. $5.20 ÷ 20 = <b>$0.26 per 100 g</b>. "
                  "($2.60 is the price per kilogram; $0.52 divides by 10; $0.13 divides by 40.)"))
    its.append(up("A dozen eggs costs $5.88. What is the price per egg?", "5.88", 12, D("0.49"),
                  [D("0.59"), D("2.04"), D("70.56")],
                  "A dozen is 12. $5.88 ÷ 12 = <b>$0.49 per egg</b> (49¢). ($0.59 divides by 10; $2.04 is 12 ÷ 5.88; $70.56 multiplies.)"))
    its.append(up("A 400 g fillet of wild BC salmon costs $11.60. What is the price per kilogram?", "11.60", "0.4", D(29),
                  [D("2.90"), D("4.64"), D("46.40")],
                  "400 g = 0.4 kg. $11.60 ÷ 0.4 = <b>$29.00 per kilogram</b>. Check: 0.4 × $29 = $11.60. "
                  "($2.90 is the price per 100 g; $4.64 multiplies by 0.4; $46.40 multiplies by 4.)"))
    its.append(up("A 400 mL bottle of shampoo costs $6.80. What is the price per 100 mL?", "6.80", 4, D("1.70"),
                  [D("0.59"), D("27.20"), D("1.36")],
                  "400 mL is 4 groups of 100 mL. $6.80 ÷ 4 = <b>$1.70 per 100 mL</b>. "
                  "($0.59 is 4 ÷ 6.80; $27.20 multiplies; $1.36 divides by 5.)"))
    its.append(up("A 3 L jug of apple juice costs $7.00. What is the price per litre, rounded to the nearest cent?", 7, 3, D("2.33"),
                  [D("0.43"), D(21), D("2.34")],
                  "$7.00 ÷ 3 = 2.333…, which rounds to <b>$2.33 per litre</b>. "
                  "($0.43 is 3 ÷ 7; $21.00 multiplies; $2.34 rounds the wrong way: the next digit is 3, so round down.)"))
    assert D("2.35") * 10 == D("23.50")
    its.append(mq("Cheese at the deli costs $2.35 per 100 g. What is the price per kilogram?", D("23.50"),
                  [D(235), D("2.35"), D("0.24")],
                  "1 kg = 1000 g, which is 10 groups of 100 g. 10 × $2.35 = <b>$23.50 per kilogram</b>. "
                  "($235.00 multiplies by 100; $2.35 is still the price per 100 g; $0.24 divides by 10.)"))
    assert D("2.20") * D("3.5") == D("7.70")
    its.append(mq("Trail mix in the bulk bin costs $2.20 per 100 g. How much do 350 g cost?", D("7.70"),
                  [D("6.60"), D("0.63"), D(22)],
                  "350 g is 3.5 groups of 100 g. 3.5 × $2.20 = <b>$7.70</b>. "
                  "($6.60 uses only 3 groups; $0.63 divides by 3.5; $22.00 is the price per kilogram.)"))
    assert D("7.47") / 3 == D("2.49") and D("2.49") * 5 == D("12.45")
    its.append(mq("A pack of 3 toothbrushes costs $7.47. At the same unit price, how much would 5 toothbrushes cost?", D("12.45"),
                  [D("12.47"), D("37.35"), D("14.94")],
                  "Unit price: $7.47 ÷ 3 = $2.49. Five toothbrushes: 5 × $2.49 = <b>$12.45</b>. "
                  "($12.47 adds 5 to the price; $37.35 is 5 × $7.47, five whole packs; $14.94 is two packs.)"))
    assert len(its) == 20
    return {"title": "Unit prices", "items": its}


# ============================================================ set 2: compare sizes
def best_item(q, opts, unit_txt, base, figure=False):
    """opts = [(label, amount, amount_text, price)]; lowest price per base wins (or a tie)."""
    us = []
    parts = []
    for lab, amt, at, pr in opts:
        u = F(str(D(pr))) * base / F(str(amt))
        assert (u * 100).denominator == 1, (lab, amt, pr)
        k = F(str(amt)) / base
        kt = str(k.numerator) if k.denominator == 1 else format(D(k.numerator) / D(k.denominator), "f")
        ut = money(D(u.numerator) / D(u.denominator))
        us.append((u, lab, pr))
        parts.append("%s: %s ÷ %s = %s %s" % (lab, money(pr), kt, ut, unit_txt))
    srt = sorted(us)
    same = "Both cost the same " + unit_txt if len(opts) == 2 else "They all cost the same " + unit_txt
    e = "Compare the price " + unit_txt + ", not the total price. " + "; ".join(parts) + ". "
    if srt[0][0] == srt[-1][0]:
        ans = same
        e += "<b>The unit prices are equal</b>, so neither is a better buy."
    else:
        assert srt[0][0] < srt[1][0]
        ans = srt[0][1]
        e += "<b>%s</b> has the lowest price %s, so it is the best buy." % (ans, unit_txt)
        cheapest_total = min(us, key=lambda t: D(t[2]))[1]
        if cheapest_total != ans:
            e += " (%s has the lowest total, but you get less.)" % cheapest_total
        biggest = max(opts, key=lambda o: F(str(o[1])))[0]
        if biggest != ans:
            e += " The biggest size is not always the best buy."
    choices = [lab for lab, a, at, p in opts] + [same]
    if len(opts) == 2:
        choices += ["You cannot compare different sizes"]
    if figure:
        q = fig(tags_svg([(lab, at, pr) for lab, a, at, pr in opts])) + q
    return mcq(q, ans, [c for c in choices if c != ans], e)


def set_compare(P):
    its = []
    its.append(best_item("Which box of cereal is the better buy?",
                         [("Box A", 400, "400 g", "4.80"), ("Box B", 750, "750 g", "8.25")], "per 100 g", 100, figure=True))
    its.append(best_item("Which carton of orange juice is the better buy?",
                         [("Carton A", 1, "1 L", "2.60"), ("Carton B", 2, "2 L", "4.80")], "per litre", 1, figure=True))
    its.append(best_item("Which bottle of ketchup is the better buy?",
                         [("Bottle A", 375, "375 mL", "2.25"), ("Bottle B", 1000, "1 L", "6.50")], "per 100 mL", 100, figure=True))
    its.append(best_item("Which carton of eggs is the better buy?",
                         [("Carton A", 12, "12 eggs", "4.80"), ("Carton B", 18, "18 eggs", "6.84")], "per egg", 1, figure=True))
    its.append(best_item("Which bag of pasta is the better buy?",
                         [("Bag A", 500, "500 g", "1.75"), ("Bag B", 900, "900 g", "3.15")], "per 100 g", 100, figure=True))
    its.append(best_item("Which pack of paper towels is the better buy?",
                         [("Pack A", 6, "6 rolls", "8.40"), ("Pack B", 12, "12 rolls", "15.60")], "per roll", 1, figure=True))
    its.append(best_item("Which pack of AA batteries is the better buy?",
                         [("Pack A", 4, "4 batteries", "5.00"), ("Pack B", 10, "10 batteries", "13.00")], "per battery", 1, figure=True))
    its.append(best_item("Which bag of rice is the best buy?",
                         [("Bag A", 1, "1 kg", "3.20"), ("Bag B", 2, "2 kg", "6.00"), ("Bag C", 5, "5 kg", "16.00")],
                         "per kilogram", 1, figure=True))
    its.append(best_item("Which bag of coffee is the better buy? (1 kg = 1000 g)",
                         [("Bag A", 340, "340 g", "10.20"), ("Bag B", 1000, "1 kg", "27.00")], "per 100 g", 100, figure=True))
    its.append(best_item("Which bottle of sparkling juice is the better buy? (1 L = 1000 mL)",
                         [("Bottle A", 750, "750 mL", "3.00"), ("Bottle B", 2000, "2 L", "7.00")], "per 100 mL", 100, figure=True))
    its.append(best_item("Which package of cheddar is the better buy? (1 kg = 1000 g)",
                         [("Pack A", 450, "450 g", "6.30"), ("Pack B", 1200, "1.2 kg", "15.60")], "per 100 g", 100, figure=True))
    its.append(best_item("Which pack of sparkling water is the best buy?",
                         [("Pack A", 6, "6 cans", "4.20"), ("Pack B", 12, "12 cans", "7.80"), ("Pack C", 24, "24 cans", "16.80")],
                         "per can", 1, figure=True))
    its.append(best_item("Which pack of soap bars is the better buy?",
                         [("Pack A", 3, "3 bars", "4.50"), ("Pack B", 8, "8 bars", "11.60")], "per bar", 1, figure=True))
    its.append(best_item("Which jug of laundry soap is the better buy?",
                         [("Jug A", 32, "32 loads", "9.60"), ("Jug B", 64, "64 loads", "17.92")], "per load", 1, figure=True))
    its.append(best_item("Which bottle of olive oil is the best buy? (1 L = 1000 mL)",
                         [("Bottle A", 500, "500 mL", "6.50"), ("Bottle B", 1000, "1 L", "12.00"), ("Bottle C", 3000, "3 L", "37.50")],
                         "per 100 mL", 100, figure=True))
    assert D("6.00") / 4 == D("1.50") and 4 * D("2.10") == D("8.40")
    its.append(mq("A 1 L carton of milk costs $2.10. A 4 L jug costs $6.00. How much do you save by buying the 4 L jug instead of four 1 L cartons?",
                  D("2.40"), [D("3.90"), D("0.60"), D("8.40")],
                  "Four cartons: 4 × $2.10 = $8.40. The jug: $6.00. Saving: $8.40 − $6.00 = <b>$2.40</b>. "
                  "($3.90 compares one carton with the jug, which are different amounts; $0.60 is the saving per litre; $8.40 is the cost of four cartons.)"))
    assert D("3.60") / 2 == D("1.80") and D("8.50") / 5 == D("1.70")
    its.append(mq("A 2 kg bag of carrots costs $3.60. A 5 kg bag costs $8.50. How much less per kilogram is the 5 kg bag?",
                  D("0.10"), [D("4.90"), D("1.70"), D("0.50")],
                  "2 kg bag: $3.60 ÷ 2 = $1.80 per kg. 5 kg bag: $8.50 ÷ 5 = $1.70 per kg. Difference: <b>$0.10</b> (10¢) per kilogram. "
                  "($4.90 compares the totals; $1.70 is the unit price, not the difference; $0.50 is the saving on all 5 kg.)"))
    assert D("8.10") / 6 == D("1.35") and D("5.60") / 4 == D("1.40")
    its.append(mq("Bakery A sells 6 muffins for $8.10. Bakery B sells 4 muffins for $5.60. How much would 12 muffins cost at the bakery with the lower unit price?",
                  D("16.20"), [D("16.80"), D("11.20"), D("13.70")],
                  "Bakery A: $8.10 ÷ 6 = $1.35 per muffin. Bakery B: $5.60 ÷ 4 = $1.40 per muffin. Bakery A is cheaper: "
                  "12 muffins = 2 boxes of 6 = <b>$16.20</b>. ($16.80 uses Bakery B; $11.20 is only 8 muffins; $13.70 adds the two prices.)"))
    assert D("4.35") / D("1.5") == D("2.90") and D("11.20") / 4 == D("2.80")
    its.append(mcq("A 1.5 kg bag of apples costs $4.35. A 4 kg box costs $11.20. Which is the better buy, and by how much per kilogram?",
                   "The 4 kg box, by 10¢ per kg", ["The 1.5 kg bag, by 10¢ per kg", "The 1.5 kg bag, by $6.85 per kg", "They cost the same per kg"],
                   "Bag: $4.35 ÷ 1.5 = $2.90 per kg. Box: $11.20 ÷ 4 = $2.80 per kg. <b>The 4 kg box is cheaper by 10¢ per kilogram</b>. "
                   "($6.85 is the difference between the totals, which are for different amounts.)"))
    its.append(mcq("Which statement about best buys is true?",
                   "Compare prices for the same amount, such as per 100 g",
                   ["The bigger package is always the better buy", "The package with the lower price is always the better buy",
                    "You cannot compare packages of different sizes"],
                   "A best buy has the <b>lowest price for the same amount</b> (the unit price). "
                   "A bigger package is often cheaper per unit, but not always, and a lower total often means you just get less."))
    assert len(its) == 20
    return {"title": "Compare sizes", "items": its}


# ============================================================ set 3: discounts and coupons
def set_discount(P):
    its = []
    its.append(mq(fig(sale_tag_svg(60, 25)) + "How much is the discount on this $60 rain jacket?", D(15),
                  [D(35), D(45), D("2.40")],
                  "25% of $60 = $60 ÷ 4 = <b>$15</b>. ($35 subtracts 25 dollars; $45 is the sale price, not the discount; $2.40 is 60 ÷ 25.)"))
    its.append(mq("A $48 pair of runners is 25% off. What is the sale price?", sale(48, 25), [D(23), D(12), D(60)],
                  "Discount: 25% of $48 = $12. Sale price: $48 − $12 = <b>$36</b>. ($23 subtracts 25 dollars; $12 is the discount; $60 adds 25%.)"))
    its.append(mq(fig(sale_tag_svg(90, 30)) + "What is the sale price of this pair of hiking boots?", sale(90, 30),
                  [D(60), D(27), D(117)],
                  "You pay 70%: $90 × 0.70 = <b>$63</b>. Or: 30% of $90 = $27 and $90 − $27 = $63. "
                  "($60 subtracts 30 dollars; $27 is the discount; $117 adds 30%.)"))
    its.append(mq(fig(coupon_svg("$5 OFF", "any item")) + "This coupon is used on a $32 phone case. What is the price after the coupon?",
                  D(27), [D("30.40"), D(37), D("1.60")],
                  "$5 off means subtract 5 dollars: $32 − $5 = <b>$27</b>. "
                  "($30.40 treats it as 5% off; $37 adds; $1.60 is 5% of $32.)"))
    its.append(mcq("Which calculation gives the sale price when an item is 35% off?", "price × 0.65",
                   ["price × 0.35", "price − 35", "price × 1.35"],
                   "35% off means you pay 100% − 35% = 65%, so <b>price × 0.65</b>. price × 0.35 gives only the discount."))
    its.append(mq("A $75 backpack is 40% off. What is the sale price?", sale(75, 40), [D(35), D(30), D(105)],
                  "You pay 60%: $75 × 0.60 = <b>$45</b>. ($35 subtracts 40 dollars; $30 is the discount; $105 adds 40%.)"))
    its.append(mq("A $200 bike is 15% off. What is the sale price?", sale(200, 15), [D(185), D(30), D(230)],
                  "10% of $200 is $20 and 5% is $10, so 15% is $30. Sale price: $200 − $30 = <b>$170</b>. "
                  "($185 subtracts 15 dollars; $30 is the discount; $230 adds 15%.)"))
    its.append(mcq("A $80 hoodie is on sale for $60. What percent is the discount?", "25%", ["20%", "about 33%", "75%"],
                   "Discount: $80 − $60 = $20. Compare it with the <b>regular</b> price: $20 ÷ $80 = 0.25 = <b>25%</b>. "
                   "(20% uses the dollars as the percent; about 33% divides by the sale price, $20 ÷ $60; 75% is the part you pay.)"))
    its.append(mcq(fig(coupon_svg("$8 OFF", "any item")) + "This coupon is used on a $40 item. What percent of the price does it save?",
                   "20%", ["8%", "5%", "80%"],
                   "$8 ÷ $40 = 0.2 = <b>20%</b>. (8% uses the dollars; 5% is 40 ÷ 8; 80% is the part you still pay.)"))
    assert sale(45, 20) == 36
    its.append(mcq("A $45 game can be bought with 20% off or with a $10-off coupon. Which deal gives the lower price?",
                   "$10 off, by $1", ["20% off, by $1", "20% off, by $10", "They give the same price"],
                   "20% off: 20% of $45 = $9, so $36. $10 off: $35. <b>$10 off is better by $1</b>. "
                   "(20% off by $10 compares the numbers 20 and 10, not dollars.)"))
    assert sale(120, 15) == 102
    its.append(mcq("A $120 pair of skates can be bought with 15% off or with a $20-off coupon. Which deal gives the lower price?",
                   "$20 off, by $2", ["15% off, by $2", "15% off, by $5", "They give the same price"],
                   "15% off: 15% of $120 = $18, so $102. $20 off: $100. <b>$20 off is better by $2</b>. "
                   "(15% off by $5 compares 20 with 15, not dollars.)"))
    assert sale(78, 20) == D("62.40") and 78 - 15 == 63
    its.append(mcq(fig(coupon_svg("$15 OFF", "orders of $75 or more")) +
                   "A $78 order can use this coupon or a 20%-off coupon, but not both. Which coupon saves more?",
                   "20% off, by 60¢", ["$15 off, by 60¢", "20% off, by $5", "They save the same"],
                   "20% of $78 = $15.60 off. The $15 coupon takes $15 off. <b>20% off saves 60¢ more</b>. "
                   "(By $5 compares the numbers 20 and 15, not dollars.)"))
    its.append(mq("A store has a deal: buy one T-shirt, get the second one 50% off. Two $26 T-shirts are bought. What is the total before tax?",
                  D(39), [D(26), D(52), D(13)],
                  "First: $26. Second: 50% off $26 = $13. Total: $26 + $13 = <b>$39</b>. "
                  "($26 treats the second as free; $52 forgets the deal; $13 is only the second shirt.)"))
    assert D(9) / 3 == 3
    its.append(mq("Granola bars are $4.50 a box with a deal: buy 2, get 1 free. What is the price per box when you take 3 boxes?",
                  D(3), [D("1.50"), D("4.50"), D("2.25")],
                  "You pay for 2 boxes: 2 × $4.50 = $9.00 for 3 boxes. Per box: $9.00 ÷ 3 = <b>$3.00</b>. "
                  "($1.50 is the price ÷ 3; $4.50 is the regular price; $2.25 is the price ÷ 2.)"))
    its.append(mq("A $45 hoodie is on clearance for 60% off. What is the clearance price?", sale(45, 60),
                  [D(27), D("44.40"), D(72)],
                  "You pay 40%: $45 × 0.40 = <b>$18</b>. ($27 is the discount; $44.40 subtracts 60¢; $72 adds 60%.)"))
    assert sale(sale(150, 20), 10) == 108
    its.append(mq("A $150 snowboard is 20% off. At the till, the store takes another 10% off the sale price. What is the final price?",
                  D(108), [D(105), D(120), D(42)],
                  "20% off: $150 − $30 = $120. Another 10% off $120: $120 − $12 = <b>$108</b>. "
                  "($105 adds the percents to 30%, but the second 10% is taken from $120; $120 forgets the second discount; $42 is the total discount.)"))
    assert sale(80, 20) - 10 == 54 and sale(70, 20) == 56
    its.append(mq("An $80 jacket is 20% off. Then a $10-off coupon is used on the sale price. What is the final price before tax?",
                  D(54), [D(56), D(50), D(70)],
                  "20% off: $80 − $16 = $64. Coupon: $64 − $10 = <b>$54</b>. "
                  "($56 uses the coupon first and then takes 20% off $70; $50 takes 30 dollars off; $70 forgets the 20% off.)"))
    assert sale(60, 15) == 51 and r2(51 * D("1.15")) == D("58.65") and 51 * D("0.85") == D("43.35")
    its.append(mq("A pair of ski goggles is 15% off. The sale price is $51. What was the regular price?", D(60),
                  [D("58.65"), D(66), D("43.35")],
                  "The sale price is 85% of the regular price. Regular price = $51 ÷ 0.85 = <b>$60</b>. "
                  "Check: 15% of $60 is $9 and $60 − $9 = $51. ($58.65 adds 15% of $51 instead; $66 adds $15; $43.35 takes 15% off again.)"))
    n, he, his, him = P.next()
    assert 50 - (sale(64, 25) - 5) == 7 and (64 - 5) * D("0.75") == D("44.25")
    its.append(mq("%s has $50. A $64 hoodie is 25%% off, and %s uses a $5-off coupon on the sale price. How much money does %s have left (before tax)?"
                  % (n, he, he),
                  D(7), [D(2), D(16), D("5.75")],
                  "Sale price: 25% of $64 is $16, so $48. Coupon: $48 − $5 = $43. Left: $50 − $43 = <b>$7</b>. "
                  "($2 forgets the coupon; $16 subtracts 25 dollars instead of 25%; $5.75 uses the coupon before the 25% off.)"))
    its.append(mcq("Is 20% off and then another 10% off the same as 30% off?", "No, it is 28% off in total",
                   ["Yes, 20% + 10% = 30%", "No, it is 32% off in total", "No, it is 2% off in total"],
                   "On $100: 20% off gives $80, then 10% of $80 is $8, so the price is $72. That is $28 off $100: "
                   "<b>28% off in total</b>. The second discount is taken from a smaller price."))
    assert len(its) == 20
    return {"title": "Discounts and coupons", "items": its}


# ============================================================ set 4: GST + PST on purchases
def set_tax(P):
    its = []
    its.append(mq("A $60 lamp has 5% GST added. How much is the GST?", gst(60), [D(6), D("0.30"), D(63)],
                  "5% = 0.05. $60 × 0.05 = <b>$3</b>. Or: 10% is $6, so 5% is $3. ($6 is 10%; $0.30 is 0.5%; $63 is the price plus GST.)"))
    its.append(mq("A $60 lamp has 7% PST added. How much is the PST?", pst(60), [D(7), D("0.42"), D(42)],
                  "7% = 0.07. $60 × 0.07 = <b>$4.20</b>. ($7 uses the percent as dollars; $0.42 is 0.7%; $42 multiplies by 0.7.)"))
    its.append(mq("An $80 pair of headphones has 5% GST and 7% PST added. How much tax is that in total?", both(80),
                  [D(12), D(4), D("5.60")],
                  "GST: $80 × 0.05 = $4.00. PST: $80 × 0.07 = $5.60. Total tax: <b>$9.60</b> (12% of $80). "
                  "($12 adds 12 dollars instead of 12%; $4 is only the GST; $5.60 is only the PST.)"))
    its.append(mq("An $80 pair of headphones has 12% tax added (5% GST + 7% PST). What is the total price?", taxed(80),
                  [D(92), D(84), D("80.12")],
                  "Tax: 12% of $80 = $9.60. Total: $80 + $9.60 = <b>$89.60</b>. Or in one step: $80 × 1.12 = $89.60. "
                  "($92 adds $12; $84 adds only the GST; $80.12 adds 12¢.)"))
    its.append(mcq("Which calculation gives the total price of an item with 5% GST and 7% PST added?", "price × 1.12",
                   ["price × 0.12", "price + 12", "price × 0.05 × 0.07"],
                   "The total is 100% of the price plus 12% tax = 112% = 1.12. So <b>price × 1.12</b>. price × 0.12 gives only the tax."))
    assert 40 + gst(40) == 42
    its.append(mq("A child’s snowsuit costs $40. Children’s clothing in BC has 5% GST but no PST. What is the total price?",
                  D(42), [D("44.80"), D(47), D(2)],
                  "Only GST applies: $40 × 0.05 = $2. Total: $40 + $2 = <b>$42</b>. ($44.80 adds 12%, but there is no PST; $47 adds $7; $2 is only the tax.)"))
    assert 36 + gst(36) == D("37.80")
    its.append(mq("A family’s restaurant meal costs $36 before tax. Restaurant meals in BC have 5% GST but no PST. What is the total?",
                  D("37.80"), [D("40.32"), D(41), D("1.80")],
                  "GST: $36 × 0.05 = $1.80. Total: $36 + $1.80 = <b>$37.80</b>. ($40.32 adds 12%, but restaurant meals have no PST; $41 adds $5.)"))
    assert 22 + gst(22) == D("23.10")
    its.append(mq("A $22 novel is bought in Victoria. Printed books in BC have 5% GST but no PST. What is the total price?",
                  D("23.10"), [D("24.64"), D(27), D("1.10")],
                  "GST: $22 × 0.05 = $1.10. Total: $22 + $1.10 = <b>$23.10</b>. ($24.64 adds 12%, but books have no PST; $27 adds $5.)"))
    items = [("Phone case", D(34)), ("Charger", D(21))]
    sub = sum(p for n_, p in items)
    assert sub == 55 and gst(sub) == D("2.75") and pst(sub) == D("3.85") and taxed(sub) == D("61.60")
    its.append(mq(fig(receipt_svg(items, [("Subtotal", money(sub)), ("GST 5%", money(gst(sub))), ("PST 7%", money(pst(sub))),
                                          ("Total", "?")])) + "What is the total on this receipt?",
                  D("61.60"), [D(67), D("57.75"), D("55.12")],
                  "Add the subtotal and both taxes: $55.00 + $2.75 + $3.85 = <b>$61.60</b>. "
                  "($57.75 forgets the PST; $67 adds $12; $55.12 adds 12¢.)"))
    assert pst("14.99") == D("1.05") and gst("14.99") == D("0.75")
    its.append(mq("A phone stand costs $14.99. How much is the 7% PST, rounded to the nearest cent?", D("1.05"),
                  [D("1.04"), D("10.49"), D("1.80")],
                  "$14.99 × 0.07 = $1.0493, which rounds to <b>$1.05</b>. "
                  "($1.04 cuts off the digits instead of rounding; $10.49 multiplies by 0.7; $1.80 is 12%, both taxes.)"))
    assert taxed("14.99") == D("16.79")
    its.append(mq("The $14.99 phone stand has 5% GST and 7% PST added. What is the total price?", D("16.79"),
                  [D("26.99"), D("15.74"), D("16.11")],
                  "GST: $14.99 × 0.05 = $0.7495 → $0.75. PST: $1.0493 → $1.05. Total: $14.99 + $0.75 + $1.05 = <b>$16.79</b>. "
                  "($15.74 forgets the PST; $26.99 adds $12; $16.11 adds $1.12.)"))
    n, he, his, him = P.next()
    t = taxed(23)
    assert t == D("25.76") and cash(t) == D("25.75")
    its.append(mq("A $23 board game has 5%% GST and 7%% PST added. %s pays with cash. How much does %s pay?" % (n, he),
                  D("25.75"), [t, D("25.80"), D(35)],
                  "Tax: $23 × 0.12 = $2.76. Total: $25.76. Canada has no pennies, so a cash total rounds to the nearest 5¢: "
                  "$25.76 → <b>$25.75</b>. ($25.76 is what a card pays; $25.80 rounds up instead of to the nearest 5¢; $35 adds $12.)"))
    t = sale(90, 20)
    assert taxed(t) == D("80.64") and D(90) * D("0.92") == D("82.80") and taxed(90) == D("100.80")
    its.append(mq("A $90 adult rain jacket is 20% off. Then 5% GST and 7% PST are added. What is the total?", D("80.64"),
                  [D("82.80"), D(72), D("100.80")],
                  "Sale price: $90 − $18 = $72. Tax: 12% of $72 = $8.64. Total: $72 + $8.64 = <b>$80.64</b>. "
                  "($82.80 combines 20% off and 12% tax into 8% off; $72 forgets the tax; $100.80 forgets the discount.)"))
    its.append(mcq("A store takes 20% off an item and also adds 12% tax (GST + PST). Does the total change if the tax is added before the discount?",
                   "No, both orders give the same total",
                   ["Yes, taking the discount first is cheaper", "Yes, adding the tax first is cheaper", "Yes, the total is 8% off either way"],
                   "Both are multiplications: price × 0.80 × 1.12 = price × 1.12 × 0.80 = price × 0.896. "
                   "<b>The order does not matter for a percent discount</b>. It is never “8% off”: that adds and subtracts the percents."))
    assert taxed(35) == D("39.20") and taxed(45) - 10 == D("40.40")
    its.append(mq(fig(coupon_svg("$10 OFF", "taken off before tax")) +
                  "This coupon is used on a $45 sweater. 5% GST and 7% PST are added to the price after the coupon. What is the total?",
                  D("39.20"), [D("40.40"), D(35), D("50.40")],
                  "Coupon first: $45 − $10 = $35. Tax: 12% of $35 = $4.20. Total: $35 + $4.20 = <b>$39.20</b>. "
                  "($40.40 adds the tax before taking off the $10: $50.40 − $10; $35 forgets the tax; $50.40 forgets the coupon.)"))
    its.append(mcq("A $10-off coupon is used on an item with 12% tax (GST + PST). Which way gives the lower total?",
                   "Coupon before tax, by $1.20",
                   ["Coupon after tax, by $1.20", "Coupon before tax, by $10", "Both ways give the same total"],
                   "Before tax, the $10 is not taxed, so you also save 12% of $10 = $1.20 in tax. "
                   "<b>Taking the coupon off before tax is cheaper by $1.20</b>. (Unlike a percent discount, a dollar coupon changes the total.)"))
    assert taxed(40) == D("44.80") and r2(D("44.80") * D("0.88")) == D("39.42") and r2(D("44.80") * D("1.12")) == D("50.18")
    its.append(mq("A total of $44.80 includes 5% GST and 7% PST. What was the price before tax?", D(40),
                  [D("39.42"), D("32.80"), D("50.18")],
                  "The total is 112% of the price, so price = $44.80 ÷ 1.12 = <b>$40</b>. Check: $40 × 1.12 = $44.80. "
                  "($39.42 takes 12% off the total, but the tax was 12% of the price; $32.80 subtracts $12; $50.18 adds tax again.)"))
    a = 50 + gst(50)
    b = taxed(15)
    assert a == D("52.50") and b == D("16.80") and a + b == D("69.30") and taxed(65) == D("72.80") and 65 + gst(65) == D("68.25")
    its.append(mq("Children’s running shoes cost $50 (5% GST only). Adult socks cost $15 (5% GST and 7% PST). What is the total for both?",
                  D("69.30"), [D("72.80"), D("68.25"), D(65)],
                  "Shoes: $50 + $2.50 GST = $52.50. Socks: $15 + $1.80 = $16.80. Total: $52.50 + $16.80 = <b>$69.30</b>. "
                  "($72.80 adds 12% to both; $68.25 adds only GST to both; $65 forgets the tax.)"))
    n, he, his, him = P.next()
    t = taxed(sale(35, 20))
    assert t == D("31.36") and cash(t) == D("31.35") and taxed(35) == D("39.20")
    its.append(mq("A $35 water bottle is 20%% off, then 5%% GST and 7%% PST are added. %s pays with cash. How much does %s pay?" % (n, he),
                  D("31.35"), [D("31.36"), D("31.40"), D("39.20")],
                  "Sale price: $35 − $7 = $28. Tax: 12% of $28 = $3.36. Total: $31.36. Cash rounds to the nearest 5¢: <b>$31.35</b>. "
                  "($31.36 is the card total; $31.40 rounds up; $39.20 forgets the discount.)"))
    n, he, his, him = P.next()
    assert taxed(53) == D("59.36") and 60 - taxed(45) - 8 == D("1.60")
    its.append(mq("%s has $60 in %s bank account. %s buys an adult hoodie for $45 and a cap for $8. Both have 5%% GST and 7%% PST. "
                  "%s pays by debit. How much is left?" % (n, his, cap(he), cap(he)),
                  D("0.64"), [D(7), D("0.65"), D("1.60")],
                  "Before tax: $45 + $8 = $53. Tax: 12% of $53 = $6.36. Total: $59.36. Left: $60.00 − $59.36 = <b>$0.64</b>. "
                  "Debit is exact, so there is no rounding. ($7 forgets the tax; $0.65 rounds as if paying cash; $1.60 forgets the tax on the cap.)"))
    assert len(its) == 20
    return {"title": "GST and PST on purchases", "items": its}


# ============================================================ set 5: best-buy decisions and word problems
def set_words(P):
    its = []
    n, he, his, him = P.next()
    assert 10 * D("6.50") == 65
    its.append(mcq("The community pool in Nanaimo charges $6.50 per swim, or $55 for a 10-swim pass. %s plans to swim 10 times. "
                   "Which is cheaper, and by how much?" % n,
                   "The pass, by $10", ["Paying each swim, by $10", "The pass, by $48.50", "They cost the same"],
                   "Paying each swim: 10 × $6.50 = $65. The pass: $55. $65 − $55 = $10, so <b>the pass is cheaper by $10</b>. "
                   "($48.50 is $55 − $6.50, which compares the pass with one swim.)"))
    assert 4 * 95 - 340 == 40 and D(340) / 4 == 85
    its.append(mq("A ski hill near Kamloops sells day tickets for $95, or a 4-day pass for $340. How much does the pass save per day?",
                  D(10), [D(40), D(85), D(245)],
                  "Pass per day: $340 ÷ 4 = $85. Saving per day: $95 − $85 = <b>$10</b>. "
                  "($40 is the saving for all 4 days; $85 is the pass price per day; $245 is $340 − $95.)"))
    n, he, his, him = P.next()
    assert D(65) / 18 > 3 and 3 * 18 < 65 < 4 * 18
    its.append(mcq("A climbing gym in Burnaby charges $18 per visit or $65 for a month. %s climbs several times a month. "
                   "What is the smallest number of visits in a month that makes the monthly pass cheaper?" % n,
                   "4 visits", ["3 visits", "47 visits", "83 visits"],
                   "$65 ÷ $18 ≈ 3.6. Three visits cost 3 × $18 = $54, less than $65. Four visits cost $72, more than $65. "
                   "So the pass is cheaper from <b>4 visits</b>. (3 rounds down; 47 is $65 − $18; 83 is $65 + $18.)"))
    n, he, his, him = P.next()
    assert 2 * D("4.50") == 9
    its.append(mcq("Blueberries cost $4.50 for a 500 g box, or $14.00 for a 2 kg flat. %s’s family will eat only 1 kg before the berries spoil. "
                   "Which choice costs less for them?" % n,
                   "Two 500 g boxes, by $5", ["The 2 kg flat, by $4", "The 2 kg flat, by $5", "They cost the same"],
                   "They need 1 kg = two 500 g boxes: 2 × $4.50 = $9.00. The flat costs $14.00. <b>Two boxes cost $5 less</b>. "
                   "The flat has the lower unit price (70¢ vs 90¢ per 100 g), but it is not a best buy if half of it is wasted."))
    assert taxed(sale(80, 25)) == D("67.20") and taxed(sale(70, 10)) == D("70.56")
    its.append(mcq("Store A sells a jacket for $80 at 25% off. Store B sells the same jacket for $70 at 10% off. Both add 5% GST and 7% PST. "
                   "Which store has the lower total?",
                   "Store A, by $3.36", ["Store A, by $3.00", "Store B, by $10.00", "Store B, by $3.36"],
                   "Store A: $80 − $20 = $60, and $60 × 1.12 = $67.20. Store B: $70 − $7 = $63, and $63 × 1.12 = $70.56. "
                   "<b>Store A is lower by $3.36</b>. ($3.00 is the difference before tax; Store B by $10 compares the regular prices.)"))
    assert D("8.97") / 3 == D("2.99") and 2 * D("8.97") == D("17.94") and 6 * D("3.29") == D("19.74")
    its.append(mq("Hockey tape costs $3.29 a roll, or $8.97 for a 3-pack. A team needs 6 rolls. What is the lowest cost?",
                  D("17.94"), [D("19.74"), D("26.91"), D("8.97")],
                  "3-pack: $8.97 ÷ 3 = $2.99 a roll, cheaper than $3.29. Six rolls = two 3-packs: 2 × $8.97 = <b>$17.94</b>. "
                  "($19.74 buys 6 single rolls; $26.91 buys 3 packs, which is 9 rolls; $8.97 is only 3 rolls.)"))
    n, he, his, him = P.next()
    its.append(mcq("%s can buy a speaker online for $54 plus $8 shipping, or at a store in Surrey for $59. Both prices include tax. "
                   "Which is cheaper, and by how much?" % n,
                   "The store, by $3", ["Online, by $5", "Online, by $3", "They cost the same"],
                   "Online: $54 + $8 = $62. Store: $59. <b>The store is cheaper by $3</b>. (Online by $5 forgets the shipping.)"))
    assert D(14) * D("0.75") == D("10.50") and D("10.50") - D("9.75") == D("0.75")
    its.append(mq("Granola in the bulk bin costs $1.40 per 100 g. A 750 g bag of the same granola costs $9.75. How much do you save by buying the bag instead of 750 g from the bin?",
                  D("0.75"), [D("8.35"), D("1.30"), D("0.10")],
                  "Bin: 7.5 × $1.40 = $10.50 for 750 g. Bag: $9.75. Saving: $10.50 − $9.75 = <b>$0.75</b> (75¢). "
                  "($8.35 is $9.75 − $1.40; $1.30 is the bag’s price per 100 g; $0.10 is the saving per 100 g.)"))
    assert D("1.6") * 8 == D("12.8") and D("12.8") * D("1.80") == D("23.04")
    its.append(mq("A car uses 8 L of gas per 100 km. Gas costs $1.80 per litre. How much does the gas cost for a 160 km drive?",
                  D("23.04"), [D("14.40"), D("230.40"), D("12.80")],
                  "160 km is 1.6 groups of 100 km, so the car uses 1.6 × 8 L = 12.8 L. Cost: 12.8 × $1.80 = <b>$23.04</b>. "
                  "($14.40 is 8 L for only 100 km; $230.40 puts the decimal point in the wrong place; $12.80 is the litres, not the cost.)"))
    n, he, his, him = P.next()
    assert D("1.89") * 45 == D("85.05") and D("0.06") * 45 == D("2.70")
    its.append(mq("Gas costs $1.89 per litre at one station and $1.83 per litre at another. %s’s parent fills a 45 L tank. How much is saved at the cheaper station?" % n,
                  D("2.70"), [D("0.06"), D(27), D(6)],
                  "Saving per litre: $1.89 − $1.83 = $0.06. For 45 L: 45 × $0.06 = <b>$2.70</b>. "
                  "($0.06 is only one litre; $27.00 puts the decimal point in the wrong place; $6 reads 6¢ as $6.)"))
    assert D("10.47") - 10 == D("0.47")
    its.append(mq("Juice boxes are $3.49 each, or 3 for $10. How much do you save by buying 3 at the deal price?",
                  D("0.47"), [D("0.16"), D("6.51"), D("3.49")],
                  "Three at $3.49: 3 × $3.49 = $10.47. Deal: $10.00. Saving: <b>$0.47</b> (47¢). "
                  "($0.16 is the saving on one item, rounded; $6.51 is $10 − $3.49; $3.49 is one item.)"))
    assert pct(900, 8) == 72 and 72 - 65 == 7
    its.append(mq("A warehouse store membership costs $65 a year and saves 8% on groceries. A family spends $900 a year there. "
                  "How much does the family save in a year after paying for the membership?",
                  D(7), [D(72), D(137), D(65)],
                  "Saving: 8% of $900 = $72. After the membership: $72 − $65 = <b>$7</b>. "
                  "($72 forgets the membership cost; $137 adds the fee; $65 is only the fee.)"))
    assert 4 * D("5.60") == D("22.40") and 3 * D("8.88") == D("26.64") and 30 * D("0.70") == 21
    assert 2 * D("8.88") + D("5.60") == D("23.36") and D("5.60") / 8 == D("0.70") and D("8.88") / 12 == D("0.74")
    its.append(mq("A class needs 30 juice boxes for a field trip. Packs of 8 cost $5.60 and packs of 12 cost $8.88. "
                  "What is the lowest cost to get at least 30 boxes?",
                  D("22.40"), [D(21), D("26.64"), D("16.80")],
                  "Unit prices: $5.60 ÷ 8 = 70¢ and $8.88 ÷ 12 = 74¢, so packs of 8 are cheaper. "
                  "Four packs of 8 give 32 boxes: 4 × $5.60 = <b>$22.40</b>. Two 12-packs and one 8-pack cost $23.36. "
                  "($21 is 30 × 70¢, but you cannot buy part of a pack; $26.64 is three 12-packs; $16.80 is only 24 boxes.)"))
    assert taxed(75) == 84
    its.append(mcq("Store A sells a pair of headphones for $75 plus 12% tax (GST + PST). Store B sells the same pair for $82 with tax included. Which is cheaper?",
                   "Store B, by $2", ["Store A, by $7", "Store A, by $2", "They cost the same"],
                   "Store A: $75 × 1.12 = $84. Store B: $82. <b>Store B is cheaper by $2</b>. "
                   "(Store A by $7 forgets to add the tax to Store A’s price.)"))
    assert D(480) / 15 == 32
    its.append(mcq("A bike costs $480 to buy, or $15 a day to rent. For how many days of renting does the rent add up to the price of the bike?",
                   "32 days", ["465 days", "3.2 days", "320 days"],
                   "$480 ÷ $15 = <b>32 days</b>. Check: 32 × $15 = $480. Renting for fewer days is cheaper; for more days, buying is. "
                   "(465 is $480 − $15; 3.2 and 320 put the decimal point in the wrong place.)"))
    assert 30 * 12 == 360 and 30 * 9 + 75 == 345
    its.append(mcq("A school orders 30 T-shirts for its Terry Fox Run. Supplier A charges $12 a shirt. Supplier B charges $9 a shirt plus a $75 set-up fee. "
                   "Which supplier is cheaper, and by how much?",
                   "Supplier B, by $15", ["Supplier B, by $90", "Supplier A, by $15", "Supplier A, by $72"],
                   "Supplier A: 30 × $12 = $360. Supplier B: 30 × $9 + $75 = $270 + $75 = $345. "
                   "<b>Supplier B is cheaper by $15</b>. (By $90 forgets the set-up fee; $72 compares $12 with $9 + $75 for one shirt.)"))
    n, he, his, him = P.next()
    assert 4 * D("18.50") == 74 and 74 + gst(74) == D("77.70") and D("77.70") / 6 == D("12.95")
    assert r2(D(74) / 6) == D("12.33") and r2(taxed(74) / 6) == D("13.81") and r2(D("77.70") / 4) == D("19.43")
    its.append(mq("%s and 5 teammates order 4 pizzas for take-out at $18.50 each. Prepared food in BC has 5%% GST but no PST. "
                  "They split the total equally. How much does each person pay?" % n,
                  D("12.95"), [D("12.33"), D("13.81"), D("19.43")],
                  "Pizzas: 4 × $18.50 = $74.00. GST: $74 × 0.05 = $3.70. Total: $77.70. Six people: $77.70 ÷ 6 = <b>$12.95</b>. "
                  "($12.33 forgets the GST; $13.81 adds PST too; $19.43 splits among only 4 people.)"))
    n, he, his, him = P.next()
    t = taxed(320)
    assert t == D("358.40") and math.ceil((t - 110) / 30) == 9 and (320 - 110) / 30 == 7 and math.ceil(t / 30) == 12
    its.append(mcq("%s wants a $320 bike. 5%% GST and 7%% PST are added. %s has $110 saved and saves $30 a week. "
                   "How many more weeks until %s can buy it?" % (n, cap(he), he),
                   "9 weeks", ["8 weeks", "7 weeks", "12 weeks"],
                   "Total: $320 × 1.12 = $358.40. Still needed: $358.40 − $110 = $248.40. $248.40 ÷ $30 = 8.28, so round up to "
                   "<b>9 weeks</b>. (8 weeks rounds down and is $8.40 short; 7 weeks forgets the tax; 12 weeks forgets the $110 saved.)"))
    n, he, his, him = P.next()
    assert taxed(3 * 16 - 8) == D("44.80") and taxed(48) == D("53.76") and taxed(32) == D("35.84")
    its.append(mq("%s buys 3 adult T-shirts at $16 each. The deal is buy 2, get the third one 50%% off. Then 5%% GST and 7%% PST are added. "
                  "What is the total?" % n,
                  D("44.80"), [D("53.76"), D(40), D("35.84")],
                  "Before tax: $16 + $16 + $8 = $40. Tax: 12% of $40 = $4.80. Total: <b>$44.80</b>. "
                  "($53.76 forgets the deal; $40 forgets the tax; $35.84 treats the third shirt as free.)"))
    n, he, his, him = P.next()
    assert D("4.55") / D("6.5") == D("0.70") and D("6.00") / 10 == D("0.60") and D("3.25") / 5 == D("0.65")
    its.append(mcq("A 1 kg tub of yogurt costs $6.00. A 500 g tub costs $3.75, and %s has a 50¢-off coupon for the 500 g tub. "
                   "Which is the better buy for %s?" % (n, him),
                   "The 1 kg tub: 60¢ per 100 g", ["The 500 g tub: 65¢ per 100 g", "The 500 g tub: 75¢ per 100 g", "They cost the same per 100 g"],
                   "1 kg tub: $6.00 ÷ 10 = 60¢ per 100 g. 500 g tub with the coupon: $3.75 − $0.50 = $3.25, and $3.25 ÷ 5 = 65¢ per 100 g. "
                   "<b>The 1 kg tub is still the better buy</b>. (75¢ forgets the coupon.)"))
    assert len(its) == 20
    return {"title": "Best-buy decisions and word problems", "items": its}


# ============================================================ lesson
def body_html():
    assert D("4.50") / 5 == D("0.90") and D("6.80") / 8 == D("0.85")
    t = sale(90, 20)
    assert t == 72 and gst(t) == D("3.60") and pst(t) == D("5.04") and taxed(t) == D("80.64")
    return (
        "<h2>Unit price: the price for one unit</h2>"
        "<p>A unit price is the price for 1 item, 1 kg, 1 L or 100 g. Divide the price by the amount: "
        "<b>unit price = price ÷ amount</b>. Always put the price first.</p>" +
        ex("Example", "A 3 kg bag of apples costs $5.97. What is the price per kilogram?",
           "$5.97 ÷ 3 = $1.99.", "$1.99 per kilogram") +
        "<h2>Compare sizes with the unit price</h2>"
        "<p>To find the best buy, compare the price for the <b>same amount</b>. Change the units first if you need to: "
        "1 kg = 1000 g and 1 L = 1000 mL. The bigger package is often cheaper per unit, but not always.</p>"
        "<figure class='sn-fig'>" + tags_svg([("Bag A", "500 g", D("4.50")), ("Bag B", "800 g", D("6.80"))]) +
        "<figcaption>Bag A: $4.50 ÷ 5 = 90¢ per 100 g. Bag B: $6.80 ÷ 8 = 85¢ per 100 g. Bag B is the better buy, even though its total is higher.</figcaption></figure>"
        "<h2>Discounts and coupons</h2>"
        "<p>A percent discount is a percent of the regular price: 25% off means you pay 75%, so multiply by 0.75. "
        "A coupon for dollars off is subtracted. When there are two percent discounts, take the second one from the new price.</p>"
        "<h2>GST and PST in BC</h2>"
        "<p>Most things you buy in BC have <b>5% GST</b> and <b>7% PST</b> added, 12% in total, so the total is price × 1.12. "
        "Some items have only GST, such as children’s clothing, restaurant meals and printed books. "
        "Take the discount or coupon off first, then add the tax to the price you actually pay.</p>"
        "<figure class='sn-fig'>" + receipt_svg([("Rain jacket", D(90))], [("20% off", "−$18.00"), ("Subtotal", "$72.00"),
                                                                           ("GST 5%", "$3.60"), ("PST 7%", "$5.04"), ("Total", "$80.64")]) +
        "<figcaption>Discount first: $90 − $18 = $72. Then tax: $72 × 1.12 = $80.64.</figcaption></figure>"
        "<h2>Best-buy decisions</h2>"
        "<p>A best buy is not only the lowest unit price. Think about how much you need, how much you will use before it spoils, "
        "shipping, fees and tax. Compare the <b>total you will really pay</b> for what you need.</p>" +
        ex("Example", "A pool charges $6.50 per swim or $55 for a 10-swim pass. You will swim 10 times. Which is cheaper?",
           "Each swim: 10 × $6.50 = $65. Pass: $55. $65 − $55 = $10.", "The pass, by $10") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Comparing the totals of different sizes", "Compare unit prices, such as per 100 g or per litre"],
            ["Dividing the amount by the price (3 ÷ $5.97)", "Divide the price by the amount: $5.97 ÷ 3"],
            ["Comparing 400 g with 1 kg without changing units", "Change to the same unit first: 1 kg = 1000 g"],
            ["25% off $60 = $60 − 25 = $35", "Find 25% of $60 ($15), then subtract: $45"],
            ["Adding tax before taking off a $10 coupon", "Take the coupon off first, then add 12% to what is left"],
            ["Writing 20% off and 12% tax as “8% off”", "Multiply: price × 0.80 × 1.12"],
            ["Adding PST to children’s clothing, restaurant meals or books", "These have 5% GST only"],
        ])
    )


FAQ = [
    {"q": "How do you find the best buy in Grade 8 math?",
     "a": "Find the unit price of each option by dividing the price by the amount, using the same unit for each, such as per 100 g or per litre. "
          "The lowest unit price is the best buy, as long as you need and will use that amount."},
    {"q": "How do you calculate the total with GST and PST in BC?",
     "a": "Multiply the price by 1.12, because 5% GST plus 7% PST is 12%. For example, $80 × 1.12 = $89.60. "
          "Items with GST only, like children’s clothing, are multiplied by 1.05."},
    {"q": "Is the discount taken before or after tax?",
     "a": "Stores take the discount or coupon off first and then add tax to the price you pay. "
          "For a percent discount the total is the same either way, but a dollar-off coupon taken before tax also saves the tax on that amount."},
    {"q": "What is financial literacy in the Grade 8 BC math curriculum?",
     "a": "In Grade 8, the BC curriculum’s financial literacy standard is best buys: comparing unit prices, discounts, coupons and sales tax to make good spending choices. "
          "These worksheets give 100 practice questions with an answer key."},
]


def gen():
    rnd = random.Random(58814)
    P = People(rnd)
    sets = [set_unit(P), set_compare(P), set_discount(P), set_tax(P), set_words(P)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-8", "slug": "best-buys", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Best Buys: Unit Prices, Discounts, Coupons, GST and PST",
        "seo_title": "Grade 8 Best Buys Worksheets: Unit Price, Discounts and GST + PST (Free Math, Answer Key, BC Curriculum)",
        "short_title": "Best buys",
        "domain": "Financial literacy",
        "standard_code": "Grade 8: Financial literacy",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/8/core",
        "standard_text": "Financial literacy – best buys",
        "meta_desc": "Free Grade 8 math worksheets on best buys for the BC curriculum: unit prices, comparing sizes, discounts and coupons, "
                     "5% GST and 7% PST on purchases, and real best-buy decisions. 100 questions with an answer key.",
        "key_big": "Compare unit prices, not totals: price ÷ amount, for the same unit.",
        "key_sub": "Take the discount or coupon off first, then add tax: 5% GST and 7% PST make 12% on most items in BC, so multiply by 1.12.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "Shelf tags: [^;']*;[^;']*;")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
