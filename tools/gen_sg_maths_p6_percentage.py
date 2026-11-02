# -*- coding: utf-8 -*-
"""
Singapore Primary 6 Maths: Percentage (MOE 2021 Primary Mathematics Syllabus, Standard)
  python3 tools/gen_sg_maths_p6_percentage.py
Percentage of a quantity (review), finding the whole given a part and the percentage,
percentage increase, percentage decrease and PSLE-style word problems (model method,
before and after, units and parts).
All arithmetic uses fractions.Fraction, so every answer is exact; every right answer is checked in code.
Every bar model is drawn from the numbers in the question.
HTML attributes use single quotes (no backslashes in the JSON).
Singapore style: 4-digit numbers without a separator (1350), 5 or more digits with a no-break space (10 000);
money as $64, $2.70 or 90¢; litres as ℓ.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-6")
UPDATED = "2026-11-03"
FILL = "#9fd3b4"
FILL2 = "#f6d58e"
LINE = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
NBSP = " "


# ------------------------------------------------------------ numbers
def num(x):
    """Exact decimal text; 5 or more digits grouped with a no-break space: 12500 -> '12 500', 1350 -> '1350'."""
    x = F(x)
    assert x >= 0, x
    d, k = x.denominator, 0
    while (10 ** k) % d:
        k += 1
        assert k < 8, x
    v = x.numerator * (10 ** k // d)
    i, r = divmod(v, 10 ** k)
    s = str(i)
    if i >= 10000:
        s = "{:,}".format(i).replace(",", NBSP)
    if r:
        s += "." + str(r).zfill(k).rstrip("0")
    return s


def pct(x):
    return num(x) + "%"


def money(x, cents=False):
    """$64, $2.70 (cents=True: always two decimal places), 90¢ under $1"""
    x = F(x)
    c = x * 100
    assert c.denominator == 1 and c > 0, x
    c = int(c)
    if c < 100:
        return "%d¢" % c
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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, col=LINE, anchor="middle", weight="700"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def tw(t, fs):
    """rough text width for Arial bold"""
    return len(plain(t)) * fs * 0.6


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
def bar_svg(parts, shade, top, inside=(), below=(), W=480, divide=True):
    """Bar model: a bar of `parts` equal parts, the first `shade` parts shaded.
    top: text over the whole bar (None: no label); inside: [(centre in part units, text)];
    below: [(from part, to part, text)] brackets under the bar. Text with '?' is red.
    divide=False draws only the line where the shading ends."""
    L, R = 14, W - 14
    pw = (R - L) / float(parts)
    Y0 = 42 if top else 6
    Y1 = Y0 + 44
    H = Y1 + (42 if below else 6)
    s = []
    if top:
        col = RED if "?" in top else LINE
        s.append("<line x1='%d' y1='30' x2='%d' y2='30' stroke='%s' stroke-width='2'/>" % (L, R, LINE))
        for x in (L, R):
            s.append("<line x1='%d' y1='24' x2='%d' y2='36' stroke='%s' stroke-width='2'/>" % (x, x, LINE))
        w = tw(top, 17) + 14
        s.append("<rect x='%.1f' y='12' width='%.1f' height='24' fill='#ffffff'/>" % ((L + R) / 2.0 - w / 2.0, w))
        s.append(text((L + R) / 2.0, 30, top, 17, col))
    if shade:
        s.append("<rect x='%d' y='%d' width='%.1f' height='%d' fill='%s'/>" % (L, Y0, pw * float(shade), Y1 - Y0, FILL))
    lines = range(1, parts) if divide else ([shade] if 0 < shade < parts else [])
    for i in lines:
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.6'/>" % (L + i * pw, Y0, L + i * pw, Y1, LINE))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (L, Y0, R - L, Y1 - Y0, LINE))
    for c, t in inside:
        s.append(text(L + c * pw, (Y0 + Y1) / 2.0 + 5, t, 14))
    for a, b, t in below:
        col = RED if "?" in t else LINE
        xa, xb = L + pw * a + 2, L + pw * b - 2
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                 % (xa, Y1 + 6, xa, Y1 + 13, xb, Y1 + 13, xb, Y1 + 6, col))
        w = tw(t, 17)
        cx = min(max((xa + xb) / 2.0, L + w / 2.0), R - w / 2.0)
        s.append(text(cx, Y1 + 34, t, 17, col, weight="800"))
    lab = "bar model: %s in %d equal parts, %s parts shaded" % (plain(top) if top else "a bar", parts, num(shade))
    return svg_wrap(W, H, "".join(s), lab)


def compare_svg(rows, uw=56, label="comparison model"):
    """Comparison bar model. rows: [(name, units, right_text, inside)] with inside = [(unit index, text)].
    All units have the same width uw, so the bars are drawn to scale."""
    namew = max(tw(r[0], 16) for r in rows) + 18
    L = 8 + namew
    maxu = max(r[1] for r in rows)
    rightw = max(tw(r[2], 17) for r in rows) + 16
    W = int(L + maxu * uw + rightw + 6)
    rh, gap, top = 40, 18, 6
    H = top + len(rows) * rh + (len(rows) - 1) * gap + 6
    s = []
    for k, (name, units, rt, inside) in enumerate(rows):
        y = top + k * (rh + gap)
        s.append(text(L - 10, y + rh / 2.0 + 6, name, 16, anchor="end"))
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (L, y, units * uw, rh, FILL if k % 2 == 0 else FILL2))
        for i in range(1, units):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.6'/>" % (L + i * uw, y, L + i * uw, y + rh, LINE))
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (L, y, units * uw, rh, LINE))
        for i, t in inside:
            s.append(text(L + (i + 0.5) * uw, y + rh / 2.0 + 5, t, 14))
        if rt:
            s.append(text(L + units * uw + 10, y + rh / 2.0 + 6, rt, 17, RED if "?" in rt else LINE, anchor="start"))
    return svg_wrap(W, H, "".join(s), label + ": " + ", ".join("%s %d units" % (r[0], r[1]) for r in rows))


# ------------------------------------------------------------ helpers for explanations
def of(p, n):
    return F(p) * F(n) / 100


def of_e(p, n, u=""):
    """p% of n = p/100 × n = r"""
    r = of(p, n)
    return "%s of %s = %s × %s = <b>%s</b>." % (pct(p), num(n) + u, fr(num(p), 100), num(n) + u, num(r) + u)


def whole_e(p, part, u="", m=False):
    """p% → part, then a friendly step (1%, 5%, 10% or 25%), then 100%"""
    p, part = F(p), F(part)
    w = part / p * 100
    N = (lambda x: money(x)) if m else (lambda x: num(x) + u)
    head = "%s → %s. " % (pct(p), N(part))
    if p < 100 and 100 % p == 0:
        k = 100 / p
        return head + "100%% = %s × %s, so 100%% → %s × %s = <b>%s</b>." % (num(k), pct(p), num(k), N(part), N(w))
    for g in (25, 20, 10, 5, 1):
        if p % g == 0:
            k = p / g
            st = part / k
            return head + "%d%% → %s ÷ %s = %s. 100%% → %s × %s = <b>%s</b>." % (
                g, N(part), num(k), N(st), N(st), num(F(100, g)), N(w))


# ============================================================ set 1: percentage of a quantity (review)
def set_review():
    its = []
    q = fig(bar_svg(5, 1, "60", [(i + 0.5, "20%") for i in range(5)], [(0, 1, "20% = ?")])) + \
        "The bar shows 60 split into 5 equal parts. What is <b>20%</b> of 60?"
    its.append(nmcq(q, 12, [3, 48, 40], "100%% is 5 parts, so 20%% is 1 part: 60 ÷ 5 = <b>12</b>. "
                    "Not 60 ÷ 20 = 3, and not 60 %s 20 = 40. 48 is the other 80%%." % MINUS))
    q = fig(bar_svg(4, 3, "84", [(i + 0.5, "25%") for i in range(4)], [(0, 3, "75% = ?")])) + \
        "The bar shows 84 split into 4 equal parts. What is <b>75%</b> of 84?"
    its.append(nmcq(q, 63, [21, 9, 112], "1 part is 25%%: 84 ÷ 4 = 21. 75%% is 3 parts: 3 × 21 = <b>63</b>. "
                    "21 is only 25%%. 112 comes from 84 ÷ 0.75, which is wrong here."))
    for p, n, wr, note in [
            (30, 45, [150, 15, F("31.5")], "Multiply, do not divide: 150 would be the whole if 30% were 45. 31.5 is the other 70%."),
            (15, 260, [26, 221, 245], "26 is only 10%. 221 is the other 85%. Do not take away 15."),
            (35, 80, [24, 52, 45], "24 is only 30%. 52 is the other 65%. Do not take away 35."),
            (12, 350, [35, 308, F("4.2")], "35 is only 10%. 308 is the other 88%."),
            (8, 650, [65, F("5.2"), 598], "65 is 10%, not 8%. 598 is the other 92%."),
            (45, 120, [66, 48, 75], "66 is the other 55%. 48 is only 40%."),
            (F("2.5"), 400, [100, 1, F("397.5")], "100 is 25%, not 2.5%. 1 is 0.25%."),
            (125, 48, [12, 73, F("38.4")], "125% is more than the whole, so the answer is more than 48. 12 is only 25%. Do not add 125.")]:
        r = of(p, n)
        its.append(nmcq("What is <b>%s</b> of %s?" % (pct(p), num(n)), r, wr, of_e(p, n) + " " + note))

    its.append(nmcq("What is <b>60%</b> of $75?", 45, [30, F("7.5"), 125],
                    "%s × $75 = <b>$45</b>. $30 is the other 40%%. $7.50 is only 10%%." % fr(60, 100), kind="money"))
    its.append(nmcq("What is <b>15%</b> of $36?", F("5.4"), [F("3.6"), F("30.6"), F("2.4")],
                    "%s × $36 = <b>$5.40</b>. $3.60 is only 10%%. $30.60 is the other 85%%. Not $36 ÷ 15." % fr(15, 100), kind="money"))
    its.append(nmcq("What is <b>40%</b> of 2.5 kg? Give your answer in grams.", 1000, [100, 1500, 400],
                    "2.5 kg = 2500 g. %s × 2500 g = <b>1000 g</b>. 1500 g is the other 60%%. 100 g comes from 2.5 kg = 250 g, but 1 kg = 1000 g." % fr(40, 100),
                    unit=" g"))
    its.append(nmcq("What is <b>65%</b> of 3 ℓ? Give your answer in millilitres.", 1950, [1050, 195, 2935],
                    "3 ℓ = 3000 ml. %s × 3000 ml = <b>1950 ml</b>. 1050 ml is the other 35%%. Do not take away 65." % fr(65, 100),
                    unit=" ml"))
    its.append(nmcq("What is <b>20%</b> of 1 h 30 min? Give your answer in minutes.", 18, [72, 9, 26],
                    "1 h 30 min = 90 min, not 130 min. %s × 90 = <b>18 min</b>. 72 min is the other 80%%. 9 min is only 10%%." % fr(20, 100),
                    unit=" min"))
    its.append(mcq("Which calculation gives <b>35% of 60</b>?", "35 ÷ 100 × 60",
                   ["60 ÷ 35 × 100", "100 ÷ 35 × 60", "60 ÷ 100 ÷ 35"],
                   "35%% means %s. So 35%% of 60 = 35 ÷ 100 × 60 = 21. <b>60 ÷ 35 × 100</b> would find the whole if 35%% were 60." % fr(35, 100)))
    its.append(nmcq("What percentage of 24 is 18?", 75, [18, 25, 6],
                    "%s = %s = <b>75%%</b>. 18%% would be 18 out of 100. 25%% is the other part." % (fr(18, 24), fr(75, 100)), kind="pct"))
    its.append(nmcq("Express 27 out of 60 as a percentage.", 45, [27, 55, 33],
                    "%s × 100%% = <b>45%%</b>. 27%% would be 27 out of 100. 55%% is the other part. Do not take 27 from 60." % fr(27, 60),
                    kind="pct"))
    its.append(nmcq("What percentage of 4 kg is 1.2 kg?", 30, [F("0.3"), 12, 70],
                    "%s = 0.3. 0.3 × 100%% = <b>30%%</b>. 0.3%% forgets to multiply by 100. 70%% is the other part." % fr("1.2", 4),
                    kind="pct"))
    its.append(nmcq("There are 40 students in a class. 35% of them wear glasses. How many students wear glasses?",
                    14, [26, 35, 5],
                    "%s × 40 = <b>14</b> students. 26 students do not wear glasses. 35 would be 35 out of 100, but there are only 40." % fr(35, 100)))
    assert len(its) == 20, len(its)
    return {"title": "Percentage of a quantity (review)", "items": its}


# ============================================================ set 2: find the whole
def wq(p, part, u="", m=False):
    p, part = F(p), F(part)
    return part / p * 100


def set_whole():
    its = []
    tenths = [(i + 0.5, "10%") for i in range(10)]
    fifths = [(i + 0.5, "20%") for i in range(5)]

    def add(q, p, part, wr, note, u="", kind="num", figure=None):
        w = wq(p, part)
        assert w.denominator == 1 or kind != "num" or True
        e = whole_e(p, part, u, kind == "money") + " " + note
        its.append(nmcq((fig(figure) if figure else "") + q, w, wr, e, unit=u, kind=kind))

    add("The bar model shows that 30% of a number is 45. What is the number?", 30, 45, [F("13.5"), 105, 75],
        "13.5 is 30% of 45, which is the wrong question. 105 is the other 70%. Do not add 45 and 30.",
        figure=bar_svg(10, 3, "100% = ?", tenths, [(0, 3, "30% = 45")]))
    add("The bar model shows that 25% of a number is 18. What is the number?", 25, 18, [F("4.5"), 54, 43],
        "54 is only 75%. 4.5 is 25% of 18, which is the wrong question.",
        figure=bar_svg(4, 1, "100% = ?", [(i + 0.5, "25%") for i in range(4)], [(0, 1, "25% = 18")]))
    add("The bar model shows that 40% of a number is 56. What is the number?", 40, 56, [F("22.4"), 84, 96],
        "84 is only the other 60%. 22.4 is 40% of 56. Do not add 40.",
        figure=bar_svg(5, 2, "100% = ?", fifths, [(0, 2, "40% = 56")]))
    add("The bar model shows that 60% of a number is 75. What is the number?", 60, 75, [45, 50, 135],
        "45 is 60% of 75, which is the wrong question. 50 is only 40%.",
        figure=bar_svg(5, 3, "100% = ?", fifths, [(0, 3, "60% = 75")]))
    for p, part, wr, note in [
            (20, 14, [F("2.8"), 56, 34], "2.8 is 20% of 14. 56 is only 80%."),
            (15, 27, [F("4.05"), 153, 42], "4.05 is 15% of 27. 153 is the other 85%. Do not add 15."),
            (75, 96, [72, 32, 171], "72 is 75% of 96. 32 is only 25%. The whole is more than 96."),
            (12, 30, [F("3.6"), 360, 42], "3.6 is 12% of 30. 360 is 30 × 12. Divide by 12, then multiply by 100."),
            (35, 63, [F("22.05"), 117, 98], "22.05 is 35% of 63. 117 is the other 65%."),
            (5, 8, [F("0.4"), 40, 13], "0.4 is 5% of 8. 40 is only 25% (8 × 5)."),
            (1, F("3.5"), [35, F("0.035"), 3500], "35 would be the whole if 3.5 were 10%. 1% is 3.5, so 100% is 100 times as much.")]:
        add("<b>%s</b> of a number is %s. What is the number?" % (pct(p), num(part)), p, part, wr, note)

    add("<b>120%</b> of a number is 54. What is the number?", 120, 54, [F("64.8"), 9, F("43.2")],
        "120% is more than the whole, so the number is less than 54. 64.8 is 120% of 54. 43.2 takes 20% of 54 away, but 20% must be of the number, not of 54.")
    add("<b>40%</b> of the mass of a bag of rice is 2.4 kg. What is the mass of the bag of rice?", 40, F("2.4"),
        [F("0.96"), F("3.6"), 60], "0.96 kg is 40% of 2.4 kg. 3.6 kg is only 60%. 60 kg has the decimal point in the wrong place.", u=" kg")
    add("<b>80%</b> of the cost of a book is $36. What is the cost of the book?", 80, 36, [F("28.8"), 9, F("43.2")],
        "$28.80 is 80% of $36. $43.20 adds 20% of $36, but the missing 20% is of the cost, not of $36.", kind="money")
    add("Ali spent 10% of his savings on a book. The book cost $6.50. How much were his savings?", 10, F("6.5"),
        [F("0.65"), F("58.5"), 650], "65¢ is 10% of $6.50. 10% × 10 = 100%, so multiply by 10, not by 100.", kind="money")
    its.append(mcq("30% of a number is 45. Which calculation gives the number?", "45 ÷ 30 × 100",
                   ["45 × 30 ÷ 100", "45 + 30", "45 ÷ 30"],
                   "30%% → 45, so 1%% → 45 ÷ 30 = 1.5 and 100%% → 1.5 × 100 = 150. That is <b>45 ÷ 30 × 100</b>. "
                   "45 × 30 ÷ 100 finds 30%% of 45 instead."))
    add("25% of the beads in a box are red. There are 36 red beads. How many beads are there in the box?", 25, 36,
        [9, 108, 61], "9 is 25% of 36. 108 is the number of beads that are not red.")
    add("45% of the students in a hall are boys. There are 27 boys. How many students are there in the hall?", 45, 27,
        [F("12.15"), 33, 72], "12.15 is 45% of 27. 33 is the number of girls, not all the students. Do not add 27 and 45.")
    # left over: the part given is the rest
    w = wq(40, 18)
    assert w == 45
    its.append(nmcq(fig(bar_svg(5, 3, "100% = ?", [(1.5, "spent 60%"), (4, "left 40%")], [(3, 5, "$18")], divide=False)) +
                    "Mei Ling spent 60% of her money and had $18 left. How much money did she have at first?",
                    45, [30, F("10.8"), F("28.8")],
                    "She had 100%% %s 60%% = 40%% left. 40%% → $18. 10%% → $18 ÷ 4 = $4.50. 100%% → <b>$45</b>. "
                    "$30 treats $18 as 60%%. $28.80 adds 60%% of $18, but 60%% is of the money at first." % MINUS, kind="money"))
    assert wq(65, F("1.3")) == 2
    its.append(nmcq("Hafiz used 35% of a bag of flour. He had 1.3 kg of flour left. How much flour was in the bag at first?",
                    2, [F("0.845"), F("1.755"), F("0.455")],
                    "He had 100%% %s 35%% = 65%% left. 65%% → 1.3 kg. 1%% → 1.3 ÷ 65 = 0.02 kg. 100%% → <b>2 kg</b>. "
                    "1.755 kg adds 35%% of 1.3 kg, but 35%% is of the flour at first." % MINUS, unit=" kg"))
    assert len(its) == 20, len(its)
    return {"title": "Find the whole from a part (bar models)", "items": its}


# ============================================================ set 3: percentage increase
def inc_e(old, p, u="", m=False):
    N = (lambda x: money(x)) if m else (lambda x: num(x) + u)
    d = of(p, old)
    return "Increase = %s × %s = %s. New value = %s + %s = <b>%s</b>." % (fr(num(p), 100), N(old), N(d), N(old), N(d), N(old + d))


def pinc_e(old, new, m=False, u=""):
    N = (lambda x: money(x)) if m else (lambda x: num(x) + u)
    d = F(new) - F(old)
    p = d / F(old) * 100
    return "Increase = %s %s %s = %s. Percentage increase = %s × 100%% = <b>%s</b>." % (
        N(new), MINUS, N(old), N(d), fr(N(d), N(old)), pct(p))


def set_increase():
    its = []
    q = fig(compare_svg([("Before", 4, "40", [(i, "25%") for i in range(4)]), ("After", 5, "?", [(4, "25%")])],
                        label="comparison model before and after")) + \
        "The model shows 40 <b>increased by 25%</b>. What is the new value?"
    its.append(nmcq(q, 50, [10, 65, 30], "40 is 4 units, so 1 unit (25%) = 10. After the increase there are 5 units: <b>50</b>. "
                    "10 is only the increase. Do not add 25."))
    for old, p, wr, note, u, kind in [
            (80, 15, [12, 95, 68], "12 is the increase, not the new value. Do not add 15.", "", "num"),
            (250, 8, [20, 258, 230], "$20 is the increase. Do not add 8.", "", "money"),
            (360, 5, [365, 18, 342], "18 is the increase. 342 is a decrease, not an increase.", "", "num"),
            (1200, 30, [360, 1230, 840], "360 is the increase. 840 is a decrease of 30%.", "", "num"),
            (45, 20, [9, 65, 36], "9 kg is the increase. 36 kg is a decrease of 20%.", " kg", "num"),
            (F("2.5"), 40, [1, F("2.9"), F("1.5")], "1 ℓ is the increase. 2.9 ℓ adds 0.4, not 40%.", " ℓ", "num")]:
        new = old + of(p, old)
        what = money(old) if kind == "money" else num(old) + u
        its.append(nmcq("Increase %s by <b>%s</b>. What is the new value?" % (what, pct(p)), new, wr,
                        inc_e(old, p, u, kind == "money") + " " + note, unit=u, kind=kind))
    for old, new, wr, note, kind in [
            (40, 50, [20, 10, 125], "20% divides by the new value (50). Always divide by the value before the change.", "pct"),
            (200, 350, [150, 175, F("0.75")], "150 is the increase, not a percentage. 175% is the new value as a percentage of the old.", "pct"),
            (30, 60, [50, 30, 200], "50% divides by the new value. The number doubled, so it went up by 100%.", "pct"),
            (800, 920, [120, 115, F("1.5")], "120 is the increase, not a percentage. 115% is the new value as a percentage of the old.", "pct")]:
        p = (F(new) - old) / old * 100
        its.append(nmcq("A number increased from %s to %s. What is the <b>percentage increase</b>?" % (num(old), num(new)), p, wr,
                        pinc_e(old, new) + " " + note, kind=kind))
    assert (F(300) - 250) / 250 * 100 == 20
    its.append(mcq("The price of a bicycle went up from $250 to $300. What is the <b>percentage increase</b>?",
                   "20%", ["16⅔%", "50%", "120%"],
                   pinc_e(250, 300, m=True) + " 16⅔% divides $50 by the new price ($300). $50 is not 50%."))
    assert (F(3) - F("2.5")) / F("2.5") * 100 == 20
    its.append(mcq("The mass of a puppy increased from 2.5 kg to 3 kg. What is the <b>percentage increase</b> in its mass?",
                   "20%", ["16⅔%", "0.5%", "120%"],
                   pinc_e(F("2.5"), 3, u=" kg") + " 16⅔% divides by the new mass. 0.5 kg is the increase, not 0.5%."))
    # reverse: find the value before the increase
    assert F(60) / F(120) * 100 == 50
    its.append(nmcq("After a <b>20% increase</b>, the price of a school bag is $60. What was the price before the increase?",
                    50, [48, 72, 40],
                    "The price before is 100%%. After the increase it is 120%%. 120%% → $60, 1%% → 50¢, 100%% → <b>$50</b>. "
                    "$48 takes 20%% of $60 away, but the 20%% was of the old price, not of $60.", kind="money"))
    assert F(400) / 125 * 100 == 320
    its.append(nmcq("After a <b>25% increase</b>, a library has 400 members. How many members did it have before the increase?",
                    320, [300, 500, 375],
                    "Before = 100%%, after = 125%%. 125%% → 400, so 25%% → 80 and 100%% → <b>320</b>. "
                    "300 takes 25%% of 400 away, but the 25%% was of the old number."))
    assert F(72, 60) * 100 == 120
    its.append(mcq("The number of visitors rose from 60 to 72. The new number is what percentage of the old number?",
                   "120%", ["20%", "12%", "83⅓%"],
                   "%s × 100%% = <b>120%%</b>. 20%% is the percentage increase. 83⅓%% is the old number as a percentage of the new." % fr(72, 60)))
    its.append(nmcq("What is 35 <b>increased by 100%</b>?", 70, [135, 36, 350],
                    "100%% of 35 is 35. 35 + 35 = <b>70</b>. An increase of 100%% doubles the number. Do not add 100 or 1."))
    its.append(mcq("Which calculation gives 65 <b>increased by 12%</b>?", "65 × 112 ÷ 100",
                   ["65 × 12 ÷ 100", "65 + 12", "65 × 88 ÷ 100"],
                   "The new value is 100%% + 12%% = 112%% of 65, so <b>65 × 112 ÷ 100</b> = 72.8. 65 × 12 ÷ 100 is only the increase. "
                   "65 × 88 ÷ 100 is a decrease."))
    its.append(mcq(fig(compare_svg([("Before", 5, "", []), ("After", 8, "", [])], uw=48, label="comparison model before and after")) +
                   "The model shows the number of visitors to a museum before and after a change. All the units are equal. "
                   "What is the <b>percentage increase</b>?",
                   "60%", ["37.5%", "3%", "160%"],
                   "Before = 5 units, after = 8 units. Increase = 3 units. %s × 100%% = <b>60%%</b>. "
                   "37.5%% divides by the 8 units after. 3 units is not 3%%." % fr(3, 5)))
    assert F(9) / 15 * 100 == 60
    its.append(nmcq("A shop increased the price of a bag by 15%. The increase was $9. What is the new price of the bag?",
                    69, [60, 51, 135],
                    "15%% → $9, so 1%% → 60¢ and 100%% → $60 (the old price). New price = $60 + $9 = <b>$69</b>. "
                    "$60 is the old price. $135 is $9 × 15.", kind="money"))
    assert len(its) == 20, len(its)
    return {"title": "Percentage increase", "items": its}


# ============================================================ set 4: percentage decrease
def dec_e(old, p, u="", m=False):
    N = (lambda x: money(x)) if m else (lambda x: num(x) + u)
    d = of(p, old)
    return "Decrease = %s × %s = %s. New value = %s %s %s = <b>%s</b>." % (fr(num(p), 100), N(old), N(d), N(old), MINUS, N(d), N(old - d))


def pdec_e(old, new, m=False, u=""):
    N = (lambda x: money(x)) if m else (lambda x: num(x) + u)
    d = F(old) - F(new)
    p = d / F(old) * 100
    return "Decrease = %s %s %s = %s. Percentage decrease = %s × 100%% = <b>%s</b>." % (
        N(old), MINUS, N(new), N(d), fr(N(d), N(old)), pct(p))


def set_decrease():
    its = []
    q = fig(compare_svg([("Before", 5, "60", [(i, "20%") for i in range(5)]), ("After", 4, "?", [])],
                        label="comparison model before and after")) + \
        "The model shows 60 <b>decreased by 20%</b>. What is the new value?"
    its.append(nmcq(q, 48, [12, 40, 72], "60 is 5 units, so 1 unit (20%) = 12. After the decrease there are 4 units: <b>48</b>. "
                    "12 is only the decrease. Do not take away 20. 72 is an increase."))
    for old, p, wr, note, u, kind in [
            (90, 30, [27, 60, 117], "27 is the decrease, not the new value. Do not take away 30.", "", "num"),
            (45, 40, [18, 5, 63], "$18 is the decrease. $63 is an increase.", "", "money"),
            (640, 15, [96, 625, 736], "96 is the decrease. 736 is an increase. Do not take away 15.", "", "num"),
            (2, 35, [F("0.7"), F("1.65"), F("2.7")], "0.7 kg is the decrease. 1.65 kg takes away 0.35 kg, which is 35% of 1 kg, not of 2 kg.", " kg", "num"),
            (1500, 8, [120, 1492, 1620], "120 is the decrease. 1620 is an increase.", "", "num"),
            (F("3.6"), 25, [F("0.9"), F("3.35"), F("4.5")], "90¢ is the decrease. $3.35 takes away 25¢, not 25%.", "", "money")]:
        new = old - of(p, old)
        what = money(old) if kind == "money" else num(old) + u
        its.append(nmcq("Decrease %s by <b>%s</b>. What is the new value?" % (what, pct(p)), new, wr,
                        dec_e(old, p, u, kind == "money") + " " + note, unit=u, kind=kind))
    for old, new, wr, note in [
            (50, 40, [25, 10, 80], "25% divides by the new value (40). Always divide by the value before the change."),
            (80, 50, [60, 30, F("62.5")], "60% divides by the new value (50). 30 is the decrease, not a percentage. 62.5% is the new value as a percentage of the old."),
            (60, 30, [100, 30, 200], "100% divides by the new value (30). The number halved, so it went down by 50%.")]:
        p = (F(old) - new) / old * 100
        its.append(nmcq("A number decreased from %s to %s. What is the <b>percentage decrease</b>?" % (num(old), num(new)), p, wr,
                        pdec_e(old, new) + " " + note, kind="pct"))
    assert (F(120) - 90) / 120 * 100 == 25
    its.append(mcq("The price of a fan was reduced from $120 to $90. What is the <b>percentage decrease</b>?",
                   "25%", ["33⅓%", "30%", "75%"],
                   pdec_e(120, 90, m=True) + " 33⅓% divides $30 by the new price ($90). $30 is not 30%. 75% is the new price as a percentage of the old."))
    its.append(nmcq("The number of cars in a car park fell from 400 to 340. What is the <b>percentage decrease</b>?",
                    15, [60, 85, F("0.15")],
                    pdec_e(400, 340) + " 60 is the decrease, not a percentage. 85% is the cars left as a percentage of 400.", kind="pct"))
    its.append(nmcq("The water in a tank fell from 2.5 ℓ to 2 ℓ. What is the <b>percentage decrease</b>?",
                    20, [25, F("0.5"), 80],
                    pdec_e(F("2.5"), 2, u=" ℓ") + " 25% divides by the new volume. 0.5 ℓ is the decrease, not 0.5%.", kind="pct"))
    # reverse
    assert F(60) / 80 * 100 == 75
    its.append(nmcq("After a <b>20% discount</b>, a pair of shoes costs $60. What was the price before the discount?",
                    75, [72, 48, 80],
                    "The price before is 100%%. After 20%% off, it is 80%%. 80%% → $60, 10%% → $7.50, 100%% → <b>$75</b>. "
                    "$72 adds 20%% of $60 back, but the 20%% was of the price before, not of $60.", kind="money"))
    assert F(340) / 85 * 100 == 400
    its.append(nmcq("After a <b>15% decrease</b>, a school has 340 students. How many students did it have before the decrease?",
                    400, [391, 289, 355],
                    "Before = 100%%, after = 85%%. 85%% → 340, so 5%% → 20 and 100%% → <b>400</b>. "
                    "391 adds 15%% of 340, but the 15%% was of the number before."))
    its.append(mcq("Which calculation gives 70 <b>decreased by 15%</b>?", "70 × 85 ÷ 100",
                   ["70 × 15 ÷ 100", "70 %s 15" % MINUS, "70 × 115 ÷ 100"],
                   "The new value is 100%% %s 15%% = 85%% of 70, so <b>70 × 85 ÷ 100</b> = 59.5. 70 × 15 ÷ 100 is only the decrease. "
                   "70 × 115 ÷ 100 is an increase." % MINUS))
    its.append(mcq("A price is reduced by 35%. The new price is what percentage of the old price?",
                   "65%", ["35%", "135%", "0.65%"],
                   "The old price is 100%%. 100%% %s 35%% = <b>65%%</b>. 35%% is the part taken off. 135%% would be an increase." % MINUS))
    its.append(mcq(fig(compare_svg([("Before", 8, "", []), ("After", 6, "", [])], uw=48, label="comparison model before and after")) +
                   "The model shows the number of fish in a pond before and after some were sold. All the units are equal. "
                   "What is the <b>percentage decrease</b>?",
                   "25%", ["33⅓%", "2%", "75%"],
                   "Before = 8 units, after = 6 units. Decrease = 2 units. %s × 100%% = <b>25%%</b>. "
                   "33⅓%% divides by the 6 units after. 75%% is the fish left." % fr(2, 8)))
    assert F(12) / 15 * 100 == 80
    its.append(nmcq("The price of a lamp was reduced by 15%. The discount was $12. What is the new price of the lamp?",
                    68, [80, 92, F("10.2")],
                    "15%% → $12, so 5%% → $4 and 100%% → $80 (the price before). New price = $80 %s $12 = <b>$68</b>. "
                    "$80 is the price before. $92 adds the discount instead of taking it away." % MINUS, kind="money"))
    assert 50 - of(20, 50) == 40 and 40 + of(20, 40) == 48
    its.append(mcq("Which is greater: 50 decreased by 20%, or 40 increased by 20%?", "40 increased by 20%",
                   ["50 decreased by 20%", "They are equal", "You can’t tell"],
                   "50 decreased by 20%: 20% of 50 = 10, so 40. 40 increased by 20%: 20% of 40 = 8, so 48. "
                   "48 &gt; 40, so <b>40 increased by 20%</b> is greater. The same percentage gives different amounts when the starting values differ."))
    assert len(its) == 20, len(its)
    return {"title": "Percentage decrease", "items": its}


# ============================================================ set 5: PSLE-style word problems
def set_psle():
    its = []
    M = "money"

    assert F(64) / 4 * 5 == 80
    its.append(nmcq(fig(bar_svg(5, 4, "usual price = ?", [(2, "paid 80%"), (4.5, "20%")], [(0, 4, "$64")], divide=False)) +
                    "A pair of shoes was sold at a 20% discount. Siti paid $64 for it. What was the usual price of the shoes?",
                    80, [F("76.8"), F("51.2"), 84],
                    "Usual price = 100%% = 5 units. Siti paid 100%% %s 20%% = 80%% = 4 units. 4 units = $64, 1 unit = $16. "
                    "5 units = <b>$80</b>. $76.80 adds 20%% of $64 back, but the discount was 20%% of the usual price." % MINUS, kind=M))

    assert F(105) / 15 * 100 == 700 and 700 - 105 == 595
    its.append(nmcq("Mr Tan bought a television at a 15% discount. He saved $105. How much did he pay for the television?",
                    595, [700, F("120.75"), 805],
                    "15%% → $105, so 5%% → $35 and 100%% → $700 (the usual price). He paid $700 %s $105 = <b>$595</b>. "
                    "$700 is the usual price, not what he paid." % MINUS, kind=M))

    assert F(1350) / 108 * 100 == 1250
    its.append(nmcq("The number of students in a school increased by 8% this year. There are now 1350 students. "
                    "How many students were there last year?",
                    1250, [1242, 1458, 1342],
                    "Last year = 100%%. This year = 108%%. 108%% → 1350, 1%% → 12.5, 100%% → <b>1250</b>. "
                    "1242 takes 8%% of 1350 away, but the 8%% was of last year’s number."))

    assert (F(60) - 48) / 48 * 100 == 25
    its.append(nmcq("The number of students in a CCA increased from 48 to 60. What is the percentage increase?",
                    25, [20, 12, 125],
                    pinc_e(48, 60) + " 20% divides by the new number (60). 12 is the increase, not 12%.", kind="pct"))

    assert F(45) / 30 * 70 == 105
    its.append(nmcq(fig(bar_svg(10, 7, "savings", [(3.5, "spent 70%"), (8.5, "left 30%")], [(0, 7, "?"), (7, 10, "$45")], divide=False)) +
                    "Arjun spent 70% of his savings on a bicycle. He had $45 left. How much did the bicycle cost?",
                    105, [150, F("31.5"), F("13.5")],
                    "He had 30%% left. 30%% → $45, so 10%% → $15. The bicycle cost 70%% → 7 × $15 = <b>$105</b>. "
                    "$150 is all his savings. $31.50 is 70%% of $45, but the 70%% is of his savings.", kind=M))

    assert F(75 - 60, 60) * 100 == 25 and F(75 - 60, 75) * 100 == 20
    its.append(nmcq("Ali has $75. Raju has $60. What percentage more money does Ali have than Raju?",
                    25, [20, 15, 125],
                    "Ali has $15 more. Compare with Raju’s money, because “more than Raju” means Raju is 100%%. "
                    "%s × 100%% = <b>25%%</b>. 20%% divides by Ali’s money." % fr("$15", "$60"), kind="pct"))
    its.append(nmcq("Ali has $75. Raju has $60. What percentage less money does Raju have than Ali?",
                    20, [25, 15, 80],
                    "Raju has $15 less. Compare with Ali’s money, because “less than Ali” means Ali is 100%%. "
                    "%s × 100%% = <b>20%%</b>. 25%% divides by Raju’s money. 80%% is Raju’s money as a percentage of Ali’s." % fr("$15", "$75"),
                    kind="pct"))

    # girls join, boys unchanged
    boys = 600 - of(40, 600)
    assert boys == 360 and 2 * boys - 600 == 120
    its.append(nmcq("There were 600 students in a school. 40% of them were girls. Some more girls joined the school. "
                    "Then 50% of the students were girls. How many girls joined the school?",
                    120, [60, 360, 720],
                    "Boys = 60%% of 600 = 360. The number of boys did not change. After: boys = 50%% = 360, so all the students = 720. "
                    "Girls now = 720 %s 360 = 360. Girls before = 240. Girls who joined = 360 %s 240 = <b>120</b>. "
                    "60 is only 10%% of 600: the total also changed." % (MINUS, MINUS)))

    assert F(160) / 5 * 4 == 128
    its.append(nmcq(fig(compare_svg([("Wei Ming", 4, "?", []), ("Jun Jie", 5, "160", [])], label="comparison model")) +
                    "Jun Jie had 25% more stickers than Wei Ming. Jun Jie had 160 stickers. How many stickers did Wei Ming have?",
                    128, [120, 200, 135],
                    "“25%% more than Wei Ming” means Wei Ming is 100%% = 4 units and Jun Jie is 125%% = 5 units. "
                    "5 units = 160, 1 unit = 32. Wei Ming = 4 units = <b>128</b>. 120 takes 25%% of 160 away, which is wrong."))

    assert (F("1.47") - F("1.4")) / F("1.4") * 100 == 5
    its.append(nmcq("Kavya’s height increased from 1.4 m to 1.47 m. What is the percentage increase in her height?",
                    5, [7, F("0.05"), 105],
                    "Increase = 1.47 m %s 1.4 m = 0.07 m. %s × 100%% = <b>5%%</b>. 7%% uses 7 cm as a percentage. "
                    "105%% is her new height as a percentage of the old." % (MINUS, fr("0.07", "1.4")), kind="pct"))

    assert 150 - of(20, 150) == 120 and 120 - of(10, 120) == 108
    its.append(nmcq("A bag cost $150. A shop gave a 20% discount. During a sale, it took a further 10% off the discounted price. "
                    "What was the final price of the bag?",
                    108, [105, 12, 135],
                    "After 20%% off: 80%% of $150 = $120. After a further 10%% off: 90%% of $120 = <b>$108</b>. "
                    "$105 takes 30%% off $150, but the 10%% is of $120, not of $150.", kind=M))

    assert F(260) / 65 * 35 == 140
    its.append(nmcq(fig(bar_svg(20, 13, "usual price", [(6.5, "paid 65%"), (16.5, "discount 35%")], [(0, 13, "$260"), (13, 20, "?")],
                                divide=False)) +
                    "After a 35% discount, a bicycle cost $260. How much was the discount?",
                    140, [91, 400, 169],
                    "Paid 100%% %s 35%% = 65%%. 65%% → $260, so 5%% → $20. Discount = 35%% → 7 × $20 = <b>$140</b>. "
                    "$91 is 35%% of $260, but the discount is 35%% of the usual price. $400 is the usual price." % MINUS, kind=M))

    left = 800 - of(25, 800)
    assert left == 600 and left - of(40, left) == 360
    its.append(nmcq("Mrs Lim had $800. She spent 25% of it on groceries and 40% of the remainder on clothes. "
                    "How much money did she have left?",
                    360, [280, 240, 440],
                    "Groceries: 25%% of $800 = $200. Remainder: $600. Clothes: 40%% of $600 = $240. Left: $600 %s $240 = <b>$360</b>. "
                    "$280 takes 65%% of $800, but the 40%% is of the remainder, not of $800." % MINUS, kind=M))

    assert 20 + of(20, 20) == 24 and 24 - of(20, 24) == F("19.2")
    its.append(nmcq("The price of durians was $20 per kg. In June the price increased by 20%. In July the new price decreased by 20%. "
                    "What was the price per kg in July?",
                    F("19.2"), [20, 16, 24],
                    "June: 120%% of $20 = $24. July: 80%% of $24 = <b>$19.20</b>. It is not $20: the 20%% decrease is of $24, "
                    "which is more than 20%% of $20.", kind=M))

    assert 5000 + of(2, 5000) == 5100
    its.append(nmcq("Mr Rahman put $5000 in a bank. The bank pays 2% interest per annum. How much money will he have in the bank after 1 year?",
                    5100, [100, 5002, 4900],
                    "Interest = 2%% of $5000 = $100. After 1 year: $5000 + $100 = <b>$5100</b>. $100 is only the interest. Do not add $2.", kind=M))

    sun = 2400 - of(15, 2400)
    assert sun == 2040 and 2400 + sun == 4440
    its.append(nmcq("2400 people visited the Singapore Zoo on Saturday. On Sunday, 15% fewer people visited. "
                    "How many people visited the zoo on the two days altogether?",
                    4440, [2040, 2760, 5160],
                    "Sunday: 85%% of 2400 = 2040. Altogether: 2400 + 2040 = <b>4440</b>. 2040 is only Sunday. "
                    "2760 uses 15%% more instead of fewer."))

    assert F(120) / 15 * 100 == 800 and 800 - 120 == 680
    its.append(nmcq("Ethan made a drink with syrup and water. 15% of the drink was syrup. He used 120 ml of syrup. "
                    "How much water did he use?",
                    680, [800, 18, 102],
                    "15%% → 120 ml, so 5%% → 40 ml and 100%% → 800 ml of drink. Water = 800 ml %s 120 ml = <b>680 ml</b>. "
                    "800 ml is all the drink. 18 ml is 15%% of 120 ml." % MINUS, unit=" ml"))

    # 40% of Siti = 60% of Nurul -> Siti : Nurul = 3 : 2
    s, n = 90, 60
    assert of(40, s) == of(60, n) and s + n == 150
    its.append(nmcq("40% of Siti’s money is equal to 60% of Nurul’s money. They have $150 altogether. How much money does Siti have?",
                    90, [60, 75, 36],
                    "40%% = %s and 60%% = %s. %s of Siti’s money = %s of Nurul’s money, so 2 × Siti’s money = 3 × Nurul’s money. "
                    "Siti has 3 units and Nurul has 2 units (2 × 3 units = 3 × 2 units). 5 units = $150, 1 unit = $30. "
                    "Siti = 3 units = <b>$90</b>. $60 is Nurul’s money." % (fr(2, 5), fr(3, 5), fr(2, 5), fr(3, 5)), kind=M))

    girls = 480 - of(45, 480)
    assert girls == 264 and of(25, girls) == 66
    its.append(nmcq("There are 480 pupils in a school. 45% of them are boys. 25% of the girls are in the choir. "
                    "How many girls are in the choir?",
                    66, [54, 120, 198],
                    "Girls = 55%% of 480 = 264. Choir = 25%% of 264 = <b>66</b>. 54 is 25%% of the boys. "
                    "120 is 25%% of all the pupils. 198 is the girls not in the choir."))

    assert F(36) * 4 == 144 and 144 + 180 == 324
    its.append(nmcq(fig(compare_svg([("Girls", 4, "", []), ("Boys", 5, "", [(4, "36")])], label="comparison model")) +
                    "At a camp, the number of boys is 25% more than the number of girls. There are 36 more boys than girls. "
                    "How many children are there at the camp altogether?",
                    324, [180, 144, 288],
                    "Girls = 100%% = 4 units. Boys = 125%% = 5 units. The difference is 1 unit = 36. "
                    "Altogether = 9 units = 9 × 36 = <b>324</b>. 180 is the number of boys and 144 is the number of girls."))
    assert len(its) == 20, len(its)
    return {"title": "PSLE-style word problems: discounts, before and after, units and parts", "items": its}


# ============================================================ lesson
def body_html():
    f_whole = bar_svg(10, 3, "100% = ?", [(i + 0.5, "10%") for i in range(10)], [(0, 3, "30% = 45")], W=500)
    f_inc = compare_svg([("Before", 4, "$40", [(i, "25%") for i in range(4)]), ("After", 5, "$50", [(4, "25%")])],
                        label="comparison model before and after")
    f_disc = bar_svg(5, 4, "usual price = ?", [(2, "paid 80%"), (4.5, "20%")], [(0, 4, "$64")], W=500, divide=False)
    return (
        "<h2>Percentage of a quantity</h2>"
        "<p>Per cent means “out of 100”. To find a percentage of a quantity, write the percentage as a fraction "
        "over 100 and multiply.</p>"
        + ex("Example", "Find 35% of 80.", fr(35, 100) + " × 80 = 28.", "28")
        + "<h2>Finding the whole from a part</h2>"
        "<p>If you know a part and its percentage, find 1% (or 10%) first. Then find 100%.</p>"
        "<figure class='sn-fig'>" + f_whole +
        "<figcaption>30% is 3 of the 10 parts. 3 parts = 45, so 1 part = 15 and 10 parts = 150.</figcaption></figure>"
        + ex("Example", "30% of a number is 45. What is the number?",
             "30% → 45. 10% → 45 ÷ 3 = 15. 100% → 15 × 10 = 150.", "150")
        + "<h2>Percentage increase and decrease</h2>"
        "<p>The value <b>before</b> the change is always 100%.</p>"
        + table(["To find", "Do this"], [
            ["percentage increase", "increase ÷ value before × 100%"],
            ["percentage decrease", "decrease ÷ value before × 100%"],
            ["new value after a 25% increase", "125% of the value before"],
            ["new value after a 20% decrease", "80% of the value before"],
        ])
        + "<figure class='sn-fig'>" + f_inc +
        "<figcaption>$40 is 4 units of 25%. After a 25% increase there are 5 units: $50.</figcaption></figure>"
        + ex("Example", "A price went up from $40 to $50. What is the percentage increase?",
             "Increase = $10. " + fr("$10", "$40") + " × 100% = 25%. Divide by $40 (before), not $50.", "25%")
        + "<h2>Before and after: price before a discount</h2>"
        "<p>When you know the value <b>after</b> the change, find what percentage it is of the value before.</p>"
        "<figure class='sn-fig'>" + f_disc +
        "<figcaption>20% off: Siti paid 80% = 4 units. 4 units = $64, so 1 unit = $16 and 5 units = $80.</figcaption></figure>"
        + ex("Example", "After a 20% discount, Siti paid $64. What was the usual price?",
             "Usual price = 100% = 5 units. Paid = 80% = 4 units = $64. 1 unit = $16. 5 units = $80.", "$80")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["30% of a number is 45, so the number is 30% of 45 = 13.5", "Find the whole: 10% = 15, so 100% = 150"],
            ["40 to 50: 10 ÷ 50 = 20% increase", "Divide by the value before: 10 ÷ 40 = 25%"],
            ["Paid $64 after 20% off, so usual price = $64 + 20% of $64 = $76.80",
             "$64 is 80% of the usual price: 80% → $64, so 100% → $80"],
            ["Ali has 25% more than Raju, so Raju has 25% less than Ali",
             "Check what is 100%: $75 is 25% more than $60, but $60 is 20% less than $75"],
        ])
    )


FAQ = [
    {"q": "What is taught in P6 percentage?",
     "a": "Primary 6 students find the whole when they know a part and its percentage, and work out percentage increase and decrease. They use these in PSLE word problems about discounts, enrolment, savings and “what percentage more”."},
    {"q": "How do I find the original price after a discount?",
     "a": "Find what percentage you paid, then work back to 100%. After a 20% discount you pay 80%, so if 80% is $64, then 10% is $8 and 100% is $80."},
    {"q": "What is the most common mistake in percentage increase and decrease?",
     "a": "Dividing by the new value instead of the value before the change. From 40 to 50 is an increase of 10 ÷ 40 = 25%, not 10 ÷ 50 = 20%."},
    {"q": "Is percentage tested in the PSLE?",
     "a": "Yes. Percentage is part of the MOE Primary 6 syllabus and appears in both PSLE papers, often in multi-step word problems that use the model method."},
]


def gen():
    rnd = random.Random(66803)
    sets = [set_review(), set_whole(), set_increase(), set_decrease(), set_psle()]
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
        "country": "sg", "subject": "maths", "grade": "primary-6", "slug": "percentage", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 6 Percentage: Finding the Whole, Percentage Increase and Decrease",
        "seo_title": "P6 Percentage Worksheets: Free Primary 6 Maths with Answers, PSLE Practice (MOE Syllabus)",
        "short_title": "Percentage",
        "domain": "Number and Algebra",
        "standard_code": "Primary 6: Percentage",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Finding the whole given a part and the percentage; finding percentage increase/decrease",
        "meta_desc": "Free P6 percentage practice: find the whole from a part, percentage increase and decrease, and PSLE word problems. 100 questions with answers.",
        "key_big": "The value before the change is always 100%.",
        "key_sub": "After a 20% discount you pay 80%: if 80% is $64, then 10% is $8 and 100% is $80.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160
    return mark_large(u, "(bar model|comparison model)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
