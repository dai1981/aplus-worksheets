# -*- coding: utf-8 -*-
"""
AU Year 6 Maths: Percentages of quantities
(Australian Curriculum v9.0, AC9M6N07)
  python3 tools/gen_au_maths_y6_percentages.py
Fractions of a quantity (3/4 of 60), percentages built from 50%, 25%, 10% and 1% (35% of 80),
decimals of a quantity (0.2 of 45), discounts and sale prices (20% off $45), comparing deals and
real-life problems.
All arithmetic uses fractions.Fraction, so every answer is exact; every right answer is checked in code.
Every bar model is drawn from the numbers in the question.
Australian style: 4-digit numbers without a separator, 5 or more digits with a no-break space (40 000);
money as $45, $40.50 or 45c; metric units with mL and L. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-6")
UPDATED = "2026-11-02"
FILL = "#9fd3b4"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
NBSP = "\u00a0"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]


# ------------------------------------------------------------ numbers
def num(x):
    """Exact decimal text: F(9, 2) -> '4.5', 2500 -> '2500', 40000 -> '40 000' (no-break space)."""
    x = F(x)
    assert x >= 0, x
    d, k = x.denominator, 0
    while (10 ** k) % d:
        k += 1
        assert k < 8, x
    v = x.numerator * (10 ** k // d)
    i, r = divmod(v, 10 ** k)
    s = str(i) if i < 10000 else "{:,}".format(i).replace(",", NBSP)
    if r:
        s += "." + str(r).zfill(k).rstrip("0")
    return s


def pct(x):
    return num(x) + "%"


def money(x, cents=False):
    """$45, $40.50 (cents=True: always two digits), 45c under $1"""
    x = F(x)
    c = x * 100
    assert c.denominator == 1 and c > 0, x
    c = int(c)
    if c < 100:
        return "%dc" % c
    d = num(c // 100)
    if cents or c % 100:
        return "$%s.%02d" % (d, c % 100)
    return "$" + d


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def plain(s):
    return re.sub(r"<[^>]+>", " ", s)


def mcq(q, right, wrongs, e):
    """right first; balance() moves it. All 4 choices must differ."""
    ch = [right] + list(wrongs)
    assert len(ch) == 4, (q, ch)
    assert len({re.sub(r"\s+", " ", plain(c)).strip() for c in ch}) == 4, ch
    return {"q": q, "c": ch, "a": 0, "e": e}


def nmcq(q, right, wrongs, e, unit="", kind="num"):
    """Number choices: all values different and positive. kind: num, pct or money."""
    vals = [F(right)] + [F(w) for w in wrongs]
    assert len(set(vals)) == 4 and all(v > 0 for v in vals), (q, vals)
    if kind == "money":
        cents = any((v * 100) % 100 for v in vals if v >= 1)
        ch = [money(v, cents) for v in vals]
    elif kind == "pct":
        ch = [pct(v) for v in vals]
    else:
        ch = [num(v) + unit for v in vals]
    return mcq(q, ch[0], ch[1:], e)


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


def text(x, y, t, fs=16, col=LINE, anchor="middle", weight="700"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger (bar models) so the parts and labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def bar_svg(parts, shade, whole_txt, labels, ask="?", halves=(), W=460):
    """Bar model: a bar of `parts` equal parts, the first `shade` parts shaded.
    whole_txt is written over the whole bar (None: no label); labels: [(centre in part units, text)] inside the bar;
    halves: part indexes where a dashed line splits the part in two; ask: text under the shaded part (red)."""
    L, R = 14, W - 14
    pw = (R - L) / float(parts)
    top = 42 if whole_txt else 6
    Y0, Y1 = top, top + 44
    H = Y1 + (42 if ask else 6)
    s = []
    if whole_txt:
        s.append("<line x1='%d' y1='30' x2='%d' y2='30' stroke='%s' stroke-width='2'/>" % (L, R, LINE))
        for x in (L, R):
            s.append("<line x1='%d' y1='24' x2='%d' y2='36' stroke='%s' stroke-width='2'/>" % (x, x, LINE))
        tw = len(plain(whole_txt)) * 9 + 14
        s.append("<rect x='%.1f' y='12' width='%d' height='24' fill='#ffffff'/>" % ((L + R) / 2.0 - tw / 2.0, tw))
        s.append(text((L + R) / 2.0, 30, whole_txt, 17))
    if shade:
        s.append("<rect x='%d' y='%d' width='%.1f' height='%d' fill='%s'/>" % (L, Y0, pw * float(shade), Y1 - Y0, FILL))
    for i in range(1, parts):
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.6'/>" % (L + i * pw, Y0, L + i * pw, Y1, LINE))
    for i in halves:
        x = L + (i + 0.5) * pw
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.6' stroke-dasharray='4 3'/>" % (x, Y0, x, Y1, LINE))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (L, Y0, R - L, Y1 - Y0, LINE))
    for c, t in labels:
        s.append(text(L + c * pw, (Y0 + Y1) / 2.0 + 5, t, 14))
    if ask:
        xe = L + pw * float(shade)
        s.append("<path d='M%d %d L%d %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                 % (L, Y1 + 6, L, Y1 + 13, xe, Y1 + 13, xe, Y1 + 6, RED))
        tw = len(plain(ask)) * 11
        cx = max((L + xe) / 2.0, L + tw / 2.0)
        s.append(text(cx, Y1 + 36, ask, 18, RED, weight="800"))
    lab = "bar model: %s in %d equal parts, %s parts shaded" % (plain(whole_txt) if whole_txt else "a bar", parts, num(shade))
    return svg_wrap(W, H, "".join(s), lab)


# ------------------------------------------------------------ explanations
def build_e(p, n, N=None):
    """Steps to find p% of n from 10%, 5% and 1% (or 50% and 25%). N: number formatter."""
    p, n = F(p), F(n)
    N = N or num
    r = p * n / 100
    t = n / 10
    o = n / 100
    if p == 50:
        return "50%% is a half, so divide by 2: %s ÷ 2 = <b>%s</b>." % (N(n), N(r))
    if p == 25:
        return "25%% is a quarter, so divide by 4: %s ÷ 4 = <b>%s</b>." % (N(n), N(r))
    if p == 75:
        h = n / 2
        return ("50%% is %s ÷ 2 = %s. 25%% is half of that: %s. 75%% = 50%% + 25%% = %s + %s = <b>%s</b>."
                % (N(n), N(h), N(h / 2), N(h), N(h / 2), N(r)))
    if p == 10:
        return "10%% is a tenth, so divide by 10: %s ÷ 10 = <b>%s</b>." % (N(n), N(r))
    if p == 1:
        return "1%% is a hundredth, so divide by 100: %s ÷ 100 = <b>%s</b>." % (N(n), N(r))
    if p == 5:
        return "10%% of %s is %s. 5%% is half of 10%%: <b>%s</b>." % (N(n), N(t), N(r))
    if p in (90, 95, 99):
        d = 100 - p
        dd = n * d / 100
        how = {10: "10%% is %s ÷ 10 = %s" % (N(n), N(dd)),
               5: "10%% is %s, so 5%% is %s" % (N(t), N(dd)),
               1: "1%% is %s ÷ 100 = %s" % (N(n), N(dd))}[d]
        return ("%s%% = 100%% %s %d%%. %s. %s %s %s = <b>%s</b>."
                % (num(p), MINUS, d, how, N(n), MINUS, N(dd), N(r)))
    tens, rest = divmod(int(p), 10)
    steps, terms, names = [], [], []
    if tens:
        steps.append("10%% of %s is %s ÷ 10 = %s." % (N(n), N(n), N(t)))
        if tens > 1:
            steps.append("%d0%% = %d × %s = %s." % (tens, tens, N(t), N(tens * t)))
        terms.append(tens * t)
        names.append("%d0%%" % tens)
    if rest == 5:
        steps.append("5%% is half of 10%%: %s." % N(t / 2))
        terms.append(t / 2)
        names.append("5%")
    elif rest:
        steps.append("1%% is %s ÷ 100 = %s%s." % (N(n), N(o), "" if rest == 1 else ", so %d%% = %d × %s = %s" % (rest, rest, N(o), N(rest * o))))
        terms.append(rest * o)
        names.append("%d%%" % rest)
    assert terms and sum(terms) == r, (p, n)
    if len(terms) == 1:
        last = steps[-1]
        k = last.rfind("= " + N(r) + ".")
        assert k >= 0, (p, n, last)
        steps[-1] = last[:k] + "= <b>%s</b>." % N(r)
        return " ".join(steps)
    steps.append("%s%% = %s = %s = <b>%s</b>." % (num(p), " + ".join(names), " + ".join(N(x) for x in terms), N(r)))
    return " ".join(steps)


def frac_e(a, b, n, u=""):
    """a/b of n: divide by b, multiply by a."""
    n = F(n)
    one = n / b
    r = one * a
    N = lambda x: num(x) + u
    if a == 1:
        return "To find %s, divide by %d: %s ÷ %d = <b>%s</b>." % (fr(1, b), b, N(n), b, N(r))
    return ("Divide by the denominator, then multiply by the numerator. %s of %s is %s ÷ %d = %s, "
            "so %s is %d × %s = <b>%s</b>." % (fr(1, b), N(n), N(n), b, N(one), fr(a, b), a, N(one), N(r)))


# ============================================================ set 1: fraction of a quantity
def frac_wrong(kind, a, b, n):
    n = F(n)
    if kind == "unit":
        return n / b, "%s is only %s. Multiply by %d as well." % (num(n / b), fr(1, b), a)
    if kind == "comp":
        return n * (b - a) / b, "%s is the other %s." % (num(n * (b - a) / b), fr(b - a, b))
    if kind == "sub":
        return n - a, "%s takes away %d instead of finding a fraction." % (num(n - a), a)
    if kind == "flip":
        return n / a * b, "%s divides by the numerator (%d) instead of the denominator (%d)." % (num(n / a * b), a, b)
    if kind == "mulb":
        return n * b, "%s multiplies by %d. %s of a number is smaller than the number, so divide." % (num(n * b), b, fr(1, b))
    if kind == "mula":
        return n * a, "%s multiplies by %d but forgets to divide by %d." % (num(n * a), a, b)
    raise ValueError(kind)


def set_fractions(rnd):
    its = []
    rows = [
        (1, 4, 28, ["sub", "mulb", "comp"], True),
        (1, 3, 27, ["sub", "mulb", "comp"], False),
        (1, 10, 90, ["sub", "mulb", "comp"], False),
        (1, 8, 96, ["sub", "mulb", "comp"], False),
        (3, 4, 60, ["unit", "flip", "sub"], True),
        (2, 5, 35, ["unit", "comp", "sub"], True),
        (2, 3, 45, ["unit", "sub", "mula"], False),
        (3, 5, 40, ["unit", "comp", "sub"], False),
        (9, 10, 50, ["unit", "sub", "mula"], False),
        (3, 10, 120, ["unit", "comp", "flip"], False),
        (7, 10, 200, ["unit", "comp", "sub"], False),
        (4, 5, 75, ["unit", "sub", "mula"], False),
        (5, 8, 64, ["unit", "comp", "sub"], False),
        (5, 6, 42, ["unit", "sub", "mula"], False),
        (3, 4, 240, ["unit", "flip", "sub"], False),
        (3, 8, 400, ["unit", "comp", "sub"], False),
    ]
    for a, b, n, kinds, pic in rows:
        r = F(n * a, b)
        ws = [frac_wrong(k, a, b, n) for k in kinds]
        q = "What is %s of %s?" % (fr(a, b), num(n))
        if pic:
            one = F(n, b)
            q = fig(bar_svg(b, a, num(n), [(i + 0.5, num(one)) for i in range(b)])) + \
                "The bar shows %s split into %d equal parts. " % (num(n), b) + q
        e = frac_e(a, b, n) + " " + " ".join(w[1] for w in ws)
        its.append(nmcq(q, r, [w[0] for w in ws], e))

    its.append(mcq("Which calculation finds %s of 60?" % fr(3, 4), "60 ÷ 4 × 3",
                   ["60 ÷ 3 × 4", "60 × 3 × 4", "60 ÷ 4 + 3"],
                   "Divide by the denominator (4) to find one quarter, then multiply by the numerator (3): "
                   "60 ÷ 4 × 3 = 15 × 3 = 45. 60 ÷ 3 × 4 = 80 mixes up the numerator and the denominator."))
    assert F(3, 4) * 60 == 45
    its.append(nmcq("What is %s of 1 hour? Give your answer in minutes." % fr(3, 4), 45, [15, 75, 20],
                    "1 hour = 60 minutes. 60 ÷ 4 = 15, so %s of an hour is 3 × 15 = <b>45 minutes</b>. "
                    "15 minutes is only %s. An hour has 60 minutes, not 100, so it is not 75. "
                    "Divide by 4, not by 3." % (fr(3, 4), fr(1, 4)), unit=" minutes"))
    assert F(2, 5) * 1000 == 400
    its.append(nmcq("What is %s of 1 kg? Give your answer in grams." % fr(2, 5), 400, [200, 40, 600],
                    "1 kg = 1000 g. 1000 ÷ 5 = 200, so %s is 2 × 200 = <b>400 g</b>. "
                    "200 g is only %s. 600 g is the other %s. 40 g has the wrong place value."
                    % (fr(2, 5), fr(1, 5), fr(3, 5)), unit=" g"))
    assert F(2, 3) * 30 == 20 and F(3, 4) * 24 == 18
    its.append(mcq("Which is more: %s of 30 or %s of 24?" % (fr(2, 3), fr(3, 4)),
                   fr(2, 3) + " of 30", [fr(3, 4) + " of 24", "They are equal", "You can’t tell"],
                   "%s of 30: 30 ÷ 3 × 2 = 20. %s of 24: 24 ÷ 4 × 3 = 18. 20 &gt; 18, so <b>%s of 30</b> is more, "
                   "even though %s is the bigger fraction." % (fr(2, 3), fr(3, 4), fr(2, 3), fr(3, 4))))
    assert len(its) == 20, len(its)
    return {"title": "Fraction of a quantity", "items": its}


# ============================================================ set 2: percentage of a quantity
def set_percent(rnd):
    its = []
    f10 = bar_svg(10, 1, "70", [(i + 0.5, "10%") for i in range(10)], ask="10% = ?", W=520)
    its.append(nmcq(fig(f10) + "The bar shows 70 split into ten equal parts. What is <b>10%</b> of 70?", 7, [F("0.7"), 60, 700],
                    build_e(10, 70) + " 0.7 would be 1% (÷ 100). Do not take away 10, and do not multiply by 10."))
    rows = [
        (50, 86, [172, 36, F("8.6")], "Halve, do not double. Do not take away 50. 8.6 is only 10%."),
        (25, 64, [48, 39, F("2.56")], "48 is the other 75%. Do not take away 25, and do not divide by 25."),
        (10, 350, [F("3.5"), 340, 315], "3.5 is only 1%. 315 is the other 90%. Do not take away 10."),
        (1, 600, [60, 599, 594], "1% is a hundredth, not a tenth: 60 would be 10%. Do not take away 1. 594 is the other 99%."),
        (1, 2500, [250, 2499, 2475], "250 would be 10%, because 1% means ÷ 100, not ÷ 10. Do not take away 1."),
    ]
    for p, n, wr, note in rows:
        its.append(nmcq("What is <b>%d%%</b> of %s?" % (p, num(n)), F(p * n, 100), wr, build_e(p, n) + " " + note))
    f25 = bar_svg(4, 1, "120", [(i + 0.5, "25%") for i in range(4)], ask="25% = ?")
    its.append(nmcq(fig(f25) + "The bar shows 120 split into four equal parts. What is <b>25%</b> of 120?", 30, [90, 95, F("4.8")],
                    build_e(25, 120) + " 90 is the other 75%. Do not take away 25, and do not divide by 25."))
    rows = [
        (50, 7, [14, F("0.14"), F("0.7")], "The answer does not have to be a whole number. Not 7 ÷ 50. 0.7 is only 10%."),
        (1, 45, [F("4.5"), 44, F("44.55")], "4.5 would be 10%: 1% means ÷ 100. Do not take away 1. 44.55 is the other 99%."),
        (20, 45, [F("4.5"), 25, F("2.25")], "4.5 is only 10%. Do not take away 20, and do not divide by 20."),
        (30, 250, [25, 220, 175], "25 is only 10%. 175 is the other 70%. Do not take away 30."),
    ]
    for p, n, wr, note in rows:
        its.append(nmcq("What is <b>%d%%</b> of %s?" % (p, num(n)), F(p * n, 100), wr, build_e(p, n) + " " + note))
    f35 = bar_svg(10, F(7, 2), "80", [(0.5, "8"), (1.5, "8"), (2.5, "8"), (3.25, "4"), (3.75, "4")] +
                  [(i + 0.5, "8") for i in range(4, 10)], ask="35% = ?", halves=(3,), W=520)
    its.append(nmcq(fig(f35) + "The bar shows 80 split into ten parts of 10%. What is <b>35%</b> of 80?", 28, [24, 45, 52],
                    build_e(35, 80) + " 24 is only 30%: add the 5% as well. 52 is the other 65%. Do not take away 35."))
    rows = [
        (5, 240, [48, 24, 235], "Not 240 ÷ 5 = 48: that is 20%. 24 is 10%."),
        (75, 36, [9, 18, F("0.48")], "9 is 25% and 18 is 50%. Add them to get 75%. Not 36 ÷ 75."),
        (15, 60, [4, 6, 51], "Not 60 ÷ 15 = 4. 6 is only 10%. 51 is the other 85%."),
        (2, 350, [70, F("3.5"), 348], "70 would be 20%: 1% is ÷ 100, not ÷ 10. 3.5 is only 1%. Do not take away 2."),
        (45, 120, [48, 66, 75], "48 is only 40%. 66 is the other 55%. Do not take away 45."),
        (99, 300, [3, 299, 270], "3 is the 1% you take away. Take away 1%, not 1. 270 is 90%."),
        (12, 300, [25, 30, 360], "Not 300 ÷ 12 = 25. 30 is only 10%: add 2% as well. 360 comes from thinking 1% is 30 (a tenth)."),
    ]
    for p, n, wr, note in rows:
        its.append(nmcq("What is <b>%d%%</b> of %s?" % (p, num(n)), F(p * n, 100), wr, build_e(p, n) + " " + note))
    its.append(mcq("Which calculation finds <b>1% of 700</b>?", "700 ÷ 100", ["700 ÷ 10", "700 × 100", "700 %s 1" % MINUS],
                   "1% is one hundredth, so divide by 100: 700 ÷ 100 = 7. 700 ÷ 10 = 70 is 10%, not 1%."))
    assert len(its) == 20, len(its)
    return {"title": "Percentage of a quantity: 50%, 25%, 10% and 1%", "items": its}


# ============================================================ set 3: decimal of a quantity
def dec_e(d, n, u=""):
    """d of n where d is a decimal: say it as a fraction, then find that fraction."""
    d, n = F(d), F(n)
    r = d * n
    N = lambda x: num(x) + u
    easy = {F(1, 2): (1, 2), F(1, 4): (1, 4), F(3, 4): (3, 4), F(1, 10): (1, 10), F(1, 100): (1, 100), F(1, 5): (1, 5)}
    if d in easy:
        a, b = easy[d]
        if a == 1:
            return "%s = %s, so divide by %d: %s ÷ %d = <b>%s</b>." % (num(d), fr(1, b), b, N(n), b, N(r))
        return ("%s = %s. %s ÷ %d = %s, and %d × %s = <b>%s</b>." % (num(d), fr(a, b), N(n), b, N(n / b), a, N(n / b), N(r)))
    if (d * 10).denominator == 1:
        k = int(d * 10)
        return ("%s = %d tenths. 0.1 of %s is %s ÷ 10 = %s, so %s is %d × %s = <b>%s</b>."
                % (num(d), k, N(n), N(n), N(n / 10), num(d), k, N(n / 10), N(r)))
    if d == F(1, 20):
        return "0.05 is half of 0.1. 0.1 of %s is %s, so 0.05 of %s is <b>%s</b>." % (N(n), N(n / 10), N(n), N(r))
    if d == F(15, 100):
        return ("0.15 = 0.1 + 0.05. 0.1 of %s is %s and 0.05 is half of that, %s. %s + %s = <b>%s</b>."
                % (N(n), N(n / 10), N(n / 20), N(n / 10), N(n / 20), N(r)))
    raise ValueError(d)


def set_decimals(rnd):
    its = []
    rows = [
        ("0.5", 30, [60, 6, 25], "60 doubles instead of halving. 6 is 30 ÷ 5, but 0.5 is a half, not a fifth. 25 takes away 5."),
        ("0.1", 70, [F("0.7"), 700, F("69.9")], "0.7 would be 0.01 of 70. Do not take away 0.1."),
        ("0.2", 45, [F("22.5"), 225, F("4.5")], "0.2 is one fifth, not one half. 225 is 45 ÷ 0.2, not 0.2 of 45. 4.5 is only 0.1."),
        ("0.25", 48, [24, 192, 36], "24 is 0.5 of 48. 192 is 48 × 4. 36 is 0.75 of 48."),
        ("0.75", 40, [10, 20, 300], "10 is only 0.25 and 20 is 0.5. 0.75 is less than 1, so the answer must be less than 40, not 300."),
        ("0.01", 600, [60, F("0.6"), 594], "60 would be 0.1 of 600. 0.6 is 0.001 of 600. 594 is 0.99 of 600."),
        ("0.3", 50, [5, 35, 150], "5 is only 0.1. 35 is 0.7. 0.3 is less than 1, so the answer is less than 50, not 150."),
        ("0.6", 25, [F("2.5"), 10, 150], "2.5 is only 0.1. 10 is 0.4. 150 forgets the decimal point: 0.6 is not 6."),
        ("0.05", 80, [40, 8, F("0.4")], "0.05 is not 0.5: 40 would be 0.5 of 80. 8 is 0.1 of 80."),
        ("0.4", 120, [12, 30, 72], "12 is only 0.1. 0.4 is not a quarter, so it is not 120 ÷ 4 = 30. 72 is 0.6."),
        ("0.9", 60, [6, F("59.1"), 66], "6 is the 0.1 you take away. Do not take away 0.9. 66 is more than 60, but 0.9 is less than 1."),
        ("0.2", F("3.5"), [7, F("1.75"), F("0.07")], "0.2 is not a half, so it is not 1.75. 7 is 3.5 × 2: you still need to ÷ 10."),
        ("0.5", F("7.4"), [F("14.8"), F("1.48"), F("0.37")], "Halve, do not double. 1.48 is 7.4 ÷ 5. 0.37 has the wrong place value."),
    ]
    for d, n, wr, note in rows:
        r = F(d) * F(n)
        its.append(nmcq("What is <b>%s</b> of %s?" % (d, num(n)), r, wr, dec_e(F(d), n) + " " + note))
    assert F("0.3") * 2000 == 600
    its.append(nmcq("What is <b>0.3</b> of 2 kg? Give your answer in grams.", 600, [60, 1400, 300],
                    "2 kg = 2000 g. 0.1 of 2000 g is 200 g, so 0.3 is 3 × 200 = <b>600 g</b>. "
                    "60 g has the wrong place value. 1400 g is 0.7. 300 g is 0.3 of only 1 kg.", unit=" g"))
    assert F("0.25") * 200 == 50
    its.append(nmcq("What is <b>0.25</b> of 2 m? Give your answer in centimetres.", 50, [25, 150, 5],
                    "2 m = 200 cm. 0.25 is a quarter: 200 ÷ 4 = <b>50 cm</b>. 25 cm is 0.25 of only 1 m. "
                    "150 cm is 0.75. 5 cm has the wrong place value.", unit=" cm"))
    assert F("0.75") * 1000 == 750
    its.append(nmcq("What is <b>0.75</b> of 1 L? Give your answer in millilitres.", 750, [250, 75, 7500],
                    "1 L = 1000 mL. 0.75 = %s: 1000 ÷ 4 = 250, and 3 × 250 = <b>750 mL</b>. "
                    "250 mL is only 0.25. 0.75 of 1 L is less than 1 L, so it is not 7500 mL." % fr(3, 4), unit=" mL"))
    rows = [("0.15", 200, [20, 170, 300], "20 is only 0.1. 170 is 0.85. 300 is 1.5 times 200, not 0.15.")]
    for d, n, wr, note in rows:
        r = F(d) * F(n)
        its.append(nmcq("What is <b>%s</b> of %s?" % (d, num(n)), r, wr, dec_e(F(d), n) + " " + note))
    assert F("0.2") * 45 == F(20, 100) * 45 == 9
    its.append(mcq("Which is the same as <b>0.2 of 45</b>?", "20% of 45", ["2% of 45", fr(1, 2) + " of 45", "45 ÷ 0.2"],
                   "0.2 = %s = 20%%, so 0.2 of 45 = <b>20%% of 45</b> = 9. 2%% would be 0.02. 0.2 is not a half. "
                   "45 ÷ 0.2 = 225 is far too big." % fr(20, 100)))
    assert F("0.25") * 80 == F(1, 4) * 80 == 20
    its.append(mcq("Which is the same as <b>0.25 of 80</b>?", fr(1, 4) + " of 80", [fr(1, 25) + " of 80", "2.5% of 80", "80 × 25"],
                   "0.25 = 25%% = %s, so 0.25 of 80 = <b>%s of 80</b> = 20. 2.5%% would be 0.025. "
                   "%s is not the same as 0.25." % (fr(1, 4), fr(1, 4), fr(1, 25))))
    assert F("0.3") * 70 == 21 and F("0.4") * 50 == 20
    its.append(mcq("Which is more: 0.3 of 70 or 0.4 of 50?", "0.3 of 70", ["0.4 of 50", "They are equal", "You can’t tell"],
                   "0.3 of 70: 0.1 is 7, so 0.3 is 21. 0.4 of 50: 0.1 is 5, so 0.4 is 20. 21 &gt; 20, so <b>0.3 of 70</b> is more, "
                   "even though 0.4 is the bigger decimal."))
    assert len(its) == 20, len(its)
    return {"title": "Decimal of a quantity", "items": its}


# ============================================================ set 4: discounts and sale prices
def disc_e(p, price):
    """How much is taken off and the sale price."""
    d = F(p, 100) * price
    return (build_e(p, price, money).replace("<b>", "").replace("</b>", "") +
            " That is the discount. Sale price: %s %s %s = <b>%s</b>." % (money(price), MINUS, money(d), money(price - d)))


def set_discounts(rnd, P):
    its = []
    M = "money"
    f20 = bar_svg(5, 1, "$45", [(i + 0.5, "20%") for i in range(5)], ask="off")
    assert 45 - F(20, 100) * 45 == 36
    its.append(nmcq(fig(f20) + "A pair of runners costs $45. It is <b>20% off</b>. What is the sale price?", 36, [25, 9, F("40.5")],
                    disc_e(20, 45) + " $25 takes off $20, not 20%. $9 is only the discount. $40.50 takes off only 10%.", kind=M))
    f30 = bar_svg(10, 3, "$80", [(i + 0.5, "$8") for i in range(10)], ask="30% off", W=520)
    assert 80 - F(30, 100) * 80 == 56
    its.append(nmcq(fig(f30) + "A school bag costs $80. It is <b>30% off</b>. What is the sale price?", 56, [24, 50, 72],
                    disc_e(30, 80) + " $24 is the discount, not the price. $50 takes off $30, not 30%. $72 takes off only 10%.", kind=M))
    rows = [
        (10, 60, "A cricket bat costs $60. It is 10% off. What is the sale price?", [6, 50, F("59.9")],
         "$6 is the discount. $50 takes off $10, not 10%. $59.90 takes off 10c."),
        (25, 80, "A snorkel set costs $80. It is 25% off. What is the sale price?", [20, 55, 40],
         "$20 is the discount. $55 takes off $25, not 25%. $40 would be 50% off."),
        (20, 65, "A netball costs $65. It is 20% off. What is the sale price?", [13, 45, F("58.5")],
         "$13 is the discount. $45 takes off $20, not 20%. $58.50 takes off only 10%."),
        (40, 120, "A scooter costs $120. It is 40% off. What is the sale price?", [48, 80, 108],
         "$48 is the discount. $80 takes off $40, not 40%. $108 takes off only 10%."),
        (5, 200, "A tablet costs $200. It is 5% off. What is the sale price?", [10, 195, 160],
         "$10 is the discount. $195 takes off $5, not 5%. $160 takes off 200 ÷ 5 = $40, which is 20%."),
        (75, 16, "A beach towel costs $16. In a clearance sale it is 75% off. What is the sale price?", [12, 8, F("15.25")],
         "$12 is the discount. $8 is only 50% off. $15.25 takes off 75c, not 75%."),
        (35, 60, "A footy jumper costs $60. It is 35% off. What is the sale price?", [21, 25, 42],
         "$21 is the discount. $25 takes off $35, not 35%. $42 takes off only 30%."),
        (12, 50, "A board game costs $50. It is 12% off. What is the sale price?", [6, 38, 45],
         "$6 is the discount. $38 takes off $12, not 12%. $45 takes off only 10%."),
        (60, 70, "A bike helmet costs $70. It is 60% off. What is the sale price?", [42, 10, 63],
         "$42 is the discount. $10 takes off $60, not 60%. $63 takes off only 10%."),
    ]
    for p, price, q, wr, note in rows:
        r = price - F(p, 100) * price
        q = q.replace("It is %d%% off" % p, "It is <b>%d%% off</b>" % p).replace(
            "it is %d%% off" % p, "it is <b>%d%% off</b>" % p)
        assert "<b>" in q, q
        its.append(nmcq(q, r, wr, disc_e(p, price) + " " + note, kind=M))
    rows = [
        (30, 90, "A beach umbrella costs $90. It is 30% off. <b>How much money is taken off?</b>",
         [63, 30, 9], "$63 is the sale price, not the money taken off. 30% is not $30. $9 is only 10%."),
        (15, 40, "A pair of swimming goggles costs $40. It is 15% off. <b>How much money is taken off?</b>",
         [34, 15, 4], "$34 is the sale price, not the money taken off. 15% is not $15. $4 is only 10%."),
    ]
    for p, price, q, wr, note in rows:
        its.append(nmcq(q, F(p, 100) * price, wr, build_e(p, price, money) + " " + note, kind=M))
    assert 36 - F(1, 3) * 36 == 24
    its.append(nmcq("A lunch box costs $36. It is <b>%s off</b>. What is the sale price?" % fr(1, 3), 24, [12, 33, 27],
                    "%s of $36 is $36 ÷ 3 = $12 off. Sale price: $36 %s $12 = <b>$24</b>. "
                    "$12 is the discount. $33 takes off $3, not a third. $27 takes off only a quarter." % (fr(1, 3), MINUS), kind=M))
    assert F("4.5") - F(10, 100) * F("4.5") == F("4.05")
    its.append(nmcq("At the school canteen a meat pie costs $4.50. On Fridays it is <b>10% off</b>. What is the Friday price?",
                    F("4.05"), [F("0.45"), F("4.40"), F("4.95")],
                    "10%% of $4.50 is $4.50 ÷ 10 = 45c off. Friday price: $4.50 %s 45c = <b>$4.05</b>. "
                    "45c is the discount. $4.40 takes off 10c, not 10%%. $4.95 adds 10%% instead of taking it off." % MINUS, kind=M))
    assert F(50 - 40, 50) == F(20, 100)
    its.append(nmcq("A rashie cost $50. In the sale it costs $40. What percentage has been taken off?", 20, [10, 80, 25],
                    "$10 has been taken off. %s = %s = <b>20%%</b>. $10 off is not 10%%. 80%% is the part you still pay. "
                    "Compare with the old price ($50), not the new price ($40)." % (fr(10, 50), fr(20, 100)), kind="pct"))
    assert F(10, 25) == F(40, 100)
    its.append(nmcq("A frisbee cost $25. In the sale it costs $15. What percentage has been taken off?", 40, [10, 60, 15],
                    "$10 has been taken off. %s = %s = <b>40%%</b>. $10 off is not 10%%. 60%% is the part you still pay. "
                    "$15 is the new price, not a percentage." % (fr(10, 25), fr(40, 100)), kind="pct"))
    assert (30 + 20) - F(25, 100) * 50 == F("37.5")
    its.append(nmcq("A shirt costs $30 and a cap costs $20. Everything is <b>25% off</b>. How much do you pay for both?",
                    F("37.5"), [F("12.5"), 25, 45],
                    "Total before the sale: $30 + $20 = $50. 25%% of $50 is $50 ÷ 4 = $12.50 off. "
                    "You pay $50 %s $12.50 = <b>$37.50</b>. $12.50 is the discount. $25 takes off $25, not 25%%. "
                    "$45 takes off only 10%%." % MINUS, kind=M))
    n, he, his = P.next()
    assert 50 - (48 - F(25, 100) * 48) == 14
    its.append(nmcq("%s buys a $48 video game that is <b>25%% off</b>. %s pays with a $50 note. How much change does %s get?"
                    % (n, he.capitalize(), he), 14, [2, 12, 36],
                    "25%% of $48 is $48 ÷ 4 = $12 off, so the game costs $48 %s $12 = $36. Change: $50 %s $36 = <b>$14</b>. "
                    "$2 is the change without the discount. $12 is the discount. $36 is the price, not the change." % (MINUS, MINUS), kind=M))
    assert 45 - F(20, 100) * 45 == 36 and 45 - F(10, 100) * 45 == F("40.5") and 40 - F(20, 100) * 40 == 32
    its.append(mcq("Which sale gives a price of <b>$36</b>?", "20% off $45", ["10% off $45", "$20 off $45", "20% off $40"],
                   "20% of $45 is $9, and $45 − $9 = $36, so <b>20% off $45</b>. 10% off $45 is $40.50. "
                   "$20 off $45 is $25. 20% off $40 is $32."))
    for it in its:
        it["e"] = it["e"].replace("%%", "%")
    assert len(its) == 20, len(its)
    return {"title": "Discounts and sale prices", "items": its}


# ============================================================ set 5: compare deals, real-life problems
def set_problems(rnd, P):
    its = []
    M = "money"
    n, he, his = P.next()
    assert F(20, 100) * 45 == 9
    its.append(mcq("%s wants a $45 game. One shop offers 20%% off. Another shop offers $10 off. Which is the better deal?" % n,
                   "$10 off", ["20% off", "They are the same", "You can’t tell"],
                   "20% of $45 is $9 off. $10 off saves more than $9, so <b>$10 off</b> is the better deal. "
                   "20% is not the same as $20 or $10."))
    assert 36 - F(25, 100) * 36 == 27 and 36 - 8 == 28
    its.append(mcq("A pair of jeans costs $36 in two shops. Shop A takes 25% off. Shop B takes $8 off. Which shop is cheaper now?",
                   "Shop A", ["Shop B", "They cost the same", "You can’t tell"],
                   "Shop A: 25%% of $36 = $9 off, so $27. Shop B: $36 %s $8 = $28. $27 &lt; $28, so <b>Shop A</b> is cheaper." % MINUS))
    assert F(1, 3) * 60 == 20 and F(30, 100) * 60 == 18
    its.append(mcq("A pair of shoes costs $60. Which saves more: %s off or 30%% off?" % fr(1, 3),
                   fr(1, 3) + " off", ["30% off", "They save the same", "You can’t tell"],
                   "%s of $60 is $20. 30%% of $60 is $18. $20 &gt; $18, so <b>%s off</b> saves more. "
                   "%s is about 33%%, which is more than 30%%." % (fr(1, 3), fr(1, 3), fr(1, 3))))
    assert 50 - F(20, 100) * 50 == 40 and 44 - F(10, 100) * 44 == F("39.6")
    its.append(mcq("Shop A sells a hat for $50 with 20% off. Shop B sells the same hat for $44 with 10% off. Which shop is cheaper?",
                   "Shop B", ["Shop A", "They cost the same", "You can’t tell"],
                   "Shop A: 20%% of $50 = $10 off, so $40. Shop B: 10%% of $44 = $4.40 off, so $44 %s $4.40 = $39.60. "
                   "$39.60 &lt; $40, so <b>Shop B</b> is cheaper, even though its discount is smaller." % MINUS))
    assert F(1, 2) * 70 == 35 and F(40, 100) * 70 == 28
    its.append(mcq("A skateboard costs $70. Which saves more: half price or 40% off?", "Half price",
                   ["40% off", "They save the same", "You can’t tell"],
                   "Half price is 50%% off: $70 ÷ 2 = $35 off. 40%% of $70 is $28 off. $35 &gt; $28, so <b>half price</b> saves more."))
    assert 80 - F(25, 100) * 80 == 60 and 75 - 15 == 60
    its.append(mcq("Shop A sells a backpack for $80 with 25% off. Shop B sells it for $75 with $15 off. Which shop is cheaper?",
                   "They cost the same", ["Shop A", "Shop B", "You can’t tell"],
                   "Shop A: 25%% of $80 = $20 off, so $60. Shop B: $75 %s $15 = $60. Both cost $60, so they <b>cost the same</b>." % MINUS))
    assert 2 * 3 == 6 and 9 - F(30, 100) * 9 == F("6.3")
    its.append(mcq("Bottles of water cost $3 each. You need 3 bottles. Which deal is cheaper: “buy 2, get 1 free” or “30% off everything”?",
                   "Buy 2, get 1 free", ["30% off everything", "They cost the same", "You can’t tell"],
                   "Buy 2, get 1 free: you pay for 2 bottles, 2 × $3 = $6. 30%% off: 3 bottles cost $9, 30%% of $9 is $2.70, "
                   "so you pay $9 %s $2.70 = $6.30. $6 &lt; $6.30, so <b>buy 2, get 1 free</b> is cheaper." % MINUS))
    assert F(25, 100) * 120 == 30 and F(20, 100) * 120 == 24 and F(1, 10) * 120 == 12
    its.append(mcq("A bike costs $120. Which discount saves the most money?", "25% off", ["$28 off", "20% off", fr(1, 10) + " off"],
                   "25%% of $120 is $30. 20%% of $120 is $24. %s of $120 is $12. $30 is more than $28, so <b>25%% off</b> saves the most."
                   % fr(1, 10)))

    assert F(35, 100) * 240 == 84
    its.append(nmcq("There are 240 students at a school. 35% of them walk to school. How many students walk to school?",
                    84, [35, 156, 72],
                    build_e(35, 240).replace("</b>.", "</b> students.") + " 35 would be 35 out of 100, but there are 240 students. "
                    "156 is the other 65%. 72 is only 30%."))
    assert F(3, 4) * 160 == 120
    its.append(nmcq("160 students go to the swimming carnival. %s of them swim in a race. How many students swim in a race?" % fr(3, 4),
                    120, [40, 157, 80],
                    frac_e(3, 4, 160) + " 40 is only %s. Do not take away 3. 80 is a half." % fr(1, 4)))
    assert 200 - F("0.6") * 200 == 80
    its.append(nmcq("A sausage sizzle has 200 sausages. By lunchtime 0.6 of them are sold. How many sausages are left?",
                    80, [120, 140, 60],
                    "0.1 of 200 is 20, so 0.6 is 6 × 20 = 120 sold. Left: 200 %s 120 = <b>80</b>. "
                    "120 is the number sold, not left. 140 takes away 60, not 0.6. 60 thinks 0.6 means 60." % MINUS))
    assert F(85, 100) * 40000 == 34000
    its.append(nmcq("A footy stadium holds 40%s000 people. It is 85%% full. How many people are in the stadium?" % NBSP,
                    34000, [6000, 39915, 3400],
                    build_e(85, 40000) + " 6000 is the number of empty seats. Do not take away 85. 3400 has the wrong place value."))
    n, he, his = P.next()
    assert 250 - F(40, 100) * 250 == 150
    its.append(nmcq("A cake recipe uses 250 g of sugar. %s uses 40%% less sugar. How much sugar does %s use?" % (n, he),
                    150, [100, 210, 350],
                    "10%% of 250 g is 25 g, so 40%% is 100 g. %s uses 250 g %s 100 g = <b>150 g</b>. "
                    "100 g is the sugar left out, not the sugar used. 210 g takes away 40 g, not 40%%. Less sugar, not more." % (n, MINUS),
                    unit=" g"))
    assert 3000 - F(45, 100) * 3000 == 1650
    its.append(nmcq("A school wants to raise $3000 for new sports equipment. So far it has raised 45% of it. How much more does it need?",
                    1650, [1350, 2955, 1500],
                    "10%% of $3000 is $300, so 40%% is $1200, and 5%% is $150. 45%% = $1200 + $150 = $1350 raised. "
                    "Still needed: $3000 %s $1350 = <b>$1650</b>. $1350 is what has been raised. $2955 takes away $45, not 45%%." % MINUS,
                    kind=M))
    n, he, his = P.next()
    assert F(30, 100) * 1500 == 450
    its.append(nmcq("%s has a 1.5 L bottle of water. %s drinks 30%% of it. How much water does %s drink?" % (n, he.capitalize(), he),
                    450, [45, 1050, 1470],
                    "1.5 L = 1500 mL. 10%% is 150 mL, so 30%% is 3 × 150 = <b>450 mL</b>. 45 mL has the wrong place value. "
                    "1050 mL is what is left. Do not take away 30.", unit=" mL"))
    assert F("0.75") * 20 == 15
    its.append(nmcq("A netball team played 20 games and won 0.75 of them. How many games did the team win?",
                    15, [5, 75, F("19.25")],
                    "0.75 = %s. 20 ÷ 4 = 5, so %s is 3 × 5 = <b>15</b> games. 5 is the number of games lost. "
                    "75 is not possible: the team only played 20 games. Do not take away 0.75." % (fr(3, 4), fr(3, 4))))
    n, he, his = P.next()
    assert F(15, 100) * 20 * 4 == 12
    its.append(nmcq("%s gets $20 pocket money each week and saves 15%% of it. How much does %s save in 4 weeks?" % (n, he),
                    12, [3, 68, 60],
                    "10%% of $20 is $2 and 5%% is $1, so 15%% is $3 each week. In 4 weeks: 4 × $3 = <b>$12</b>. "
                    "$3 is only one week. $68 is what %s spends. $60 uses $15, not 15%%." % he, kind=M))
    assert 120 - F(25, 100) * 120 - F(1, 3) * 120 == 50
    its.append(nmcq("The canteen sold 120 items at lunch. 25%% were fruit cups and %s were sushi rolls. The rest were wraps. How many wraps were sold?"
                    % fr(1, 3), 50, [70, 90, 80],
                    "Fruit cups: 25%% of 120 = 120 ÷ 4 = 30. Sushi: %s of 120 = 120 ÷ 3 = 40. "
                    "Wraps: 120 %s 30 %s 40 = <b>50</b>. 70 is the fruit cups and sushi together. "
                    "90 and 80 only take away one of them." % (fr(1, 3), MINUS, MINUS)))
    assert 90 - F(10, 100) * 90 == 81
    its.append(nmcq("90 Year 6 students are going on an excursion. On the day, 10% are away sick. How many students go on the excursion?",
                    81, [9, 80, 89],
                    "10%% of 90 is 90 ÷ 10 = 9 away. 90 %s 9 = <b>81</b> students go. 9 is the number away. "
                    "Do not take away 10 or 1." % MINUS))
    assert 150 - F(20, 100) * 150 - 10 == 110
    its.append(nmcq("A pair of footy boots costs $150. They are 20% off, and then a $10 voucher is taken off the sale price. How much do they cost?",
                    110, [120, 40, 130],
                    "20%% of $150: 10%% is $15, so 20%% is $30. Sale price: $150 %s $30 = $120. "
                    "Then the voucher: $120 %s $10 = <b>$110</b>. $120 forgets the voucher. $40 is the total saved. "
                    "$130 takes off $20, not 20%%." % (MINUS, MINUS), kind=M))
    for it in its:
        it["e"] = it["e"].replace("%%", "%")
    assert len(its) == 20, len(its)
    return {"title": "Compare deals and solve real-life problems", "items": its}


# ============================================================ lesson
def body_html():
    f34 = bar_svg(4, 3, "60", [(i + 0.5, "15") for i in range(4)], ask="3/4 = 45")
    f35 = bar_svg(10, F(7, 2), "80", [(0.5, "8"), (1.5, "8"), (2.5, "8"), (3.25, "4"), (3.75, "4")] +
                  [(i + 0.5, "8") for i in range(4, 10)], ask="35% = 24 + 4 = 28", halves=(3,), W=520)
    f20 = bar_svg(5, 1, "$45", [(i + 0.5, "$9") for i in range(5)], ask="20% off = $9")
    return (
        "<h2>A fraction of a quantity</h2>"
        "<p>To find a fraction of an amount, <b>divide by the denominator</b>, then <b>multiply by the numerator</b>.</p>"
        + ex("Example", "Find " + fr(3, 4) + " of 60.",
             "60 ÷ 4 = 15, so one quarter is 15. Three quarters is 3 × 15.", "45")
        + "<figure class='sn-fig'>" + f34 +
        "<figcaption>60 in four equal parts. Each part is 15, and three parts are 45.</figcaption></figure>"
        + "<h2>A percentage of a quantity</h2>"
        "<p>Per cent means “out of 100”. Learn these four, then build any percentage from them.</p>"
        + table(["Percentage", "Fraction", "Decimal", "How to find it"], [
            ["50%", fr(1, 2), "0.5", "÷ 2"],
            ["25%", fr(1, 4), "0.25", "÷ 4"],
            ["10%", fr(1, 10), "0.1", "÷ 10"],
            ["1%", fr(1, 100), "0.01", "÷ 100"],
        ])
        + ex("Example", "Find 35% of 80.", "10% of 80 = 8, so 30% = 24. 5% is half of 10% = 4. 35% = 24 + 4.", "28")
        + "<figure class='sn-fig'>" + f35 +
        "<figcaption>80 in ten parts of 10%. 35% is three and a half parts.</figcaption></figure>"
        + ex("Example", "Find 99% of 300.", "1% of 300 = 3. 99% = 100% " + MINUS + " 1% = 300 " + MINUS + " 3.", "297")
        + "<h2>A decimal of a quantity</h2>"
        "<p>A decimal is another way to write a fraction: 0.2 = " + fr(2, 10) + " = 20%. Use whichever is easiest.</p>"
        + ex("Example", "Find 0.2 of 45.", "0.1 of 45 = 45 ÷ 10 = 4.5. 0.2 is 2 × 4.5.", "9")
        + "<h2>Discounts and sale prices</h2>"
        "<p>A discount is the money taken off. Find the discount, then <b>take it away</b> from the price.</p>"
        + ex("Example", "Runners cost $45. They are 20% off. What is the sale price?",
             "10% of $45 = $4.50, so 20% = $9 off. $45 " + MINUS + " $9.", "$36")
        + "<figure class='sn-fig'>" + f20 +
        "<figcaption>$45 in five parts of 20%. Take one part ($9) off: you pay the other four parts, $36.</figcaption></figure>"
        "<p>To compare deals, work out the price you pay for each one. A calculator is useful for awkward amounts, "
        "but familiar percentages are quicker in your head.</p>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["20% off $45 = $45 " + MINUS + " $20 = $25", "20% is not $20. 20% of $45 = $9, so $45 " + MINUS + " $9 = $36"],
            ["20% off $45 costs $9", "$9 is the discount. Take it off: $45 " + MINUS + " $9 = $36"],
            ["1% of 600 = 60", "1% is " + fr(1, 100) + ", so ÷ 100: 6. 60 is 10%"],
            [fr(3, 4) + " of 60 = 60 ÷ 3 × 4 = 80", "Divide by the denominator: 60 ÷ 4 × 3 = 45"],
            ["0.2 of 45 = half of 45", "0.2 is " + fr(1, 5) + ", not " + fr(1, 2) + ": 45 ÷ 5 = 9"],
        ])
    )


FAQ = [
    {"q": "How do you find a percentage of a quantity in Year 6?",
     "a": "Find 10% by dividing by 10 and 1% by dividing by 100, then build the percentage you need. For example, 35% of 80 is 30% (24) plus 5% (4), which makes 28."},
    {"q": "How do you work out 20% off a price?",
     "a": "Find 20% of the price, then take it away. For $45: 10% is $4.50, so 20% is $9, and the sale price is $45 − $9 = $36."},
    {"q": "How do you find a fraction of an amount, like 3/4 of 60?",
     "a": "Divide by the denominator, then multiply by the numerator: 60 ÷ 4 = 15 and 15 × 3 = 45."},
    {"q": "Can Year 6 students use a calculator for percentages?",
     "a": "Yes, the Australian Curriculum (AC9M6N07) says to use digital tools where appropriate, but students should find familiar fractions, decimals and percentages such as 50%, 25%, 10% and 1% mentally."},
]


def gen():
    rnd = random.Random(6807)
    P = People(rnd)
    sets = [set_fractions(rnd), set_percent(rnd), set_decimals(rnd), set_discounts(rnd, P), set_problems(rnd, P)]
    for s in sets:
        for it in s["items"]:
            it["e"] = it["e"].replace("%%", "%")
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            assert "%%" not in it["e"] and "%%" not in it["q"], it
            assert len(re.findall("<svg", it["q"])) <= 1
            seen.add(it["q"])
    u = {
        "country": "au", "subject": "maths", "grade": "year-6", "slug": "percentages-of-quantities", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Percentages of Quantities: Fractions, Decimals and Discounts",
        "seo_title": "Year 6 Percentages of Quantities Worksheets: 35% of 80, 3/4 of 60 and 20% Off Sale Prices",
        "short_title": "Percentages of quantities",
        "domain": "Number",
        "standard_code": "AC9M6N07",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Solve problems that require finding a familiar fraction, decimal or percentage of a quantity, including percentage discounts, choosing efficient calculation strategies and using digital tools where appropriate",
        "meta_desc": "Free Year 6 maths worksheets for the Australian Curriculum: find a fraction, decimal or percentage of a quantity (3/4 of 60, 0.2 of 45, 35% of 80), work out discounts and sale prices, and compare deals. 100 questions with an answer key.",
        "key_big": "Find 10% (÷ 10) and 1% (÷ 100), then build: 35% of 80 = 24 + 4 = 28.",
        "key_sub": "For a fraction, divide by the denominator and multiply by the numerator: 3/4 of 60 = 15 × 3 = 45. For a discount, take it off the price: 20% off $45 = $45 − $9 = $36.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "bar model")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
