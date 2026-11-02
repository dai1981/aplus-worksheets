# -*- coding: utf-8 -*-
"""
Singapore Primary 5 Maths: Percentage (MOE 2021 Primary Mathematics Syllabus, Standard)
  python3 tools/gen_sg_maths_p5_percentage.py
Percentage as "out of 100" (hundred squares), fractions and decimals as percentages,
a part of a whole as a percentage (18 out of 40), a percentage of a quantity (25% of $60),
and word problems with bar models (test marks, class surveys, savings).
All arithmetic uses fractions.Fraction, so every answer is exact; every right answer is checked in code.
Every bar model and grid is drawn from the numbers in the question.
HTML attributes use single quotes (no backslashes in the JSON).
Singapore style: 4-digit numbers without a separator, 5+ digits with a no-break space; money as $15, $3.60 or 85¢.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-5")
UPDATED = "2026-11-03"
FILL = "#9fd3b4"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
NBSP = " "


# ------------------------------------------------------------ numbers
def num(x):
    """Exact decimal text: F(9, 2) -> '4.5', 2500 -> '2500', 12000 -> '12 000' (no-break space)."""
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
    """$45, $40.50 (cents=True: always two digits), 80¢ under $1"""
    x = F(x)
    c = x * 100
    assert c.denominator == 1 and c > 0, x
    c = int(c)
    if c < 100:
        return "%d¢" % c
    if cents or c % 100:
        return "$%s.%02d" % (num(c // 100), c % 100)
    return "$" + num(c // 100)


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
        ch = [money(v) for v in vals]
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


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger (bar models, grids) so the parts and labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def hundred_svg(k, cell=18):
    """10 x 10 hundred square with k squares shaded: full columns first, then from the top of the next column."""
    assert 0 < k <= 100
    pad = 4
    s = []
    for c in range(10):
        for r in range(10):
            if c * 10 + r < k:
                s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (pad + c * cell, pad + r * cell, cell, cell, FILL))
    for i in range(1, 10):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (pad + i * cell, pad, pad + i * cell, pad + 10 * cell, THIN))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (pad, pad + i * cell, pad + 10 * cell, pad + i * cell, THIN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (pad, pad, 10 * cell, 10 * cell, LINE))
    w = 10 * cell + 2 * pad
    return svg_wrap(w, w, "".join(s), "hundred square with %d of 100 squares shaded" % k)


def rect_grid_svg(rows, cols, k, cell=26):
    """rows x cols grid with the first k squares (row by row) shaded"""
    pad = 4
    W, H = cols * cell + 2 * pad, rows * cell + 2 * pad
    s = []
    for i in range(k):
        r, c = divmod(i, cols)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (pad + c * cell, pad + r * cell, cell, cell, FILL))
    for c in range(1, cols):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.4'/>" % (pad + c * cell, pad, pad + c * cell, pad + rows * cell, THIN))
    for r in range(1, rows):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.4'/>" % (pad, pad + r * cell, pad + cols * cell, pad + r * cell, THIN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (pad, pad, cols * cell, rows * cell, LINE))
    return svg_wrap(W, H, "".join(s), "grid of %d squares with %d shaded" % (rows * cols, k))


def bar_svg(parts, shade, whole_txt, labels, ask="?", span=None, W=460):
    """Bar model: a bar of `parts` equal parts (units), the first `shade` parts shaded.
    whole_txt is written over the whole bar (None: no label); labels: [(centre in part units, text)] inside the bar;
    ask: red text under a bracket over parts span=(a, b) (default: the shaded parts); '' for no bracket."""
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
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (L, Y0, R - L, Y1 - Y0, LINE))
    for c, t in labels:
        s.append(text(L + c * pw, (Y0 + Y1) / 2.0 + 5, t, 14))
    if ask:
        a, b = span if span else (0, shade)
        xa, xb = L + pw * float(a), L + pw * float(b)
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                 % (xa, Y1 + 6, xa, Y1 + 13, xb, Y1 + 13, xb, Y1 + 6, RED))
        tw = len(plain(ask)) * 11
        cx = min(max((xa + xb) / 2.0, L + tw / 2.0), R - tw / 2.0)
        s.append(text(cx, Y1 + 36, ask, 18, RED, weight="800"))
    lab = "bar model: %s in %d equal parts, %s parts shaded" % (plain(whole_txt) if whole_txt else "a bar", parts, num(shade))
    return svg_wrap(W, H, "".join(s), lab)


def unit_bar(parts, shade, whole_txt, ask="?", span=None):
    """bar of equal units, each labelled with its percentage"""
    p = 100 // parts
    assert p * parts == 100
    return bar_svg(parts, shade, whole_txt, [(i + 0.5, "%d%%" % p) for i in range(parts)], ask=ask, span=span)


def of_e(p, n, u="", money_=False):
    """p% of n = p/100 × n = r"""
    r = F(p) * F(n) / 100
    N = (lambda x: money(x)) if money_ else (lambda x: num(x) + u)
    return "%s%% of %s = %s × %s = <b>%s</b>." % (num(p), N(n), fr(num(p), 100), N(n), N(r))


def part_e(part, n):
    """part out of n as a percentage: part/n × 100%"""
    p = F(part * 100, n)
    assert p.denominator == 1, (part, n)
    m = F(100, n)
    if m.denominator == 1:
        return "%s = %s = <b>%s%%</b>." % (fr(part, n), fr(num(p), 100), num(p))
    from math import gcd
    k = gcd(part, n)
    a, b = part // k, n // k
    if b == 100:
        return "%s = %s = <b>%s%%</b>." % (fr(part, n), fr(num(p), 100), num(p))
    if 100 % b == 0:
        return "%s = %s = %s = <b>%s%%</b>." % (fr(part, n), fr(a, b), fr(num(p), 100), num(p))
    return "%s × 100%% = <b>%s%%</b>." % (fr(part, n), num(p))


# ============================================================ set 1: out of 100
def set_hundred():
    its = []
    # hundred squares: (shaded, ask about shaded?, wrongs, note)
    for k, ask_sh, wr, note in [
            (37, True, [63, F("3.7"), F("0.37")], "63% is the part that is not shaded."),
            (8, True, [80, 92, F("0.8")], "8 squares are shaded, not 8 columns. 92% is not shaded."),
            (45, True, [55, F("4.5"), 54], "Count the full columns first: 4 columns = 40 squares, then 5 more."),
            (72, False, [72, 38, F("2.8")], "72% is the shaded part. 100 " + MINUS + " 72 = 28, not 38: rename 1 ten as 10 ones."),
            (16, True, [84, F("1.6"), 61], "1 full column (10 squares) and 6 more. 84% is not shaded."),
            (90, False, [90, 1, 9], "90 squares are shaded, so 10 squares are not shaded. 9 is the number of shaded columns."),
            (100, True, [10, 1, 50], "All 100 squares are shaded. That is the whole: 100%.")]:
        part = k if ask_sh else 100 - k
        word = "shaded" if ask_sh else "<b>not</b> shaded"
        q = fig(hundred_svg(k)) + "The hundred square has 100 equal squares. What percentage of it is %s?" % word
        e = "%d out of 100 squares are %s: %s = <b>%d%%</b>. " % (part, "shaded" if ask_sh else "not shaded", fr(part, 100), part) + note
        its.append(nmcq(q, part, wr, e, kind="pct"))

    its.append(nmcq("What is <b>29 out of 100</b> as a percentage?", 29, [71, F("2.9"), F("0.29")],
                    "Per cent means out of 100, so 29 out of 100 = %s = <b>29%%</b>. 71%% is the rest of the 100." % fr(29, 100), kind="pct"))
    its.append(mcq("Write <b>9%</b> as a fraction.", fr(9, 100), [fr(9, 10), fr(1, 9), fr(9, 1000)],
                   "9%% means 9 out of 100: <b>%s</b>. %s would be 90%%." % (fr(9, 100), fr(9, 10))))
    its.append(nmcq("Write %s as a percentage." % fr(3, 100), 3, [30, F("0.3"), 300],
                    "%s means 3 out of 100, so it is <b>3%%</b>. 30%% would be %s." % (fr(3, 100), fr(3, 10)), kind="pct"))
    its.append(mcq("Which is the same as <b>40%</b>?", "40 out of 100", ["4 out of 100", "40 out of 10", "60 out of 100"],
                   "Per cent means out of 100, so 40%% = <b>40 out of 100</b>. 60 out of 100 is the other part."))
    its.append(mcq("What does <b>per cent</b> mean?", "out of 100", ["out of 10", "out of 1000", "for each one"],
                   "“Per cent” means <b>out of 100</b>. 7% is 7 out of 100. The sign % stands for “per cent”."))
    its.append(nmcq("64 out of every 100 students in a school wear spectacles. What percentage of the students do <b>not</b> wear spectacles?",
                    36, [64, 46, F("3.6")],
                    "The whole is 100%%. 100%% %s 64%% = <b>36%%</b>. 46%% is a renaming mistake: 100 %s 64 = 36." % (MINUS, MINUS), kind="pct"))
    its.append(nmcq("Find the missing percentage: 45% + ? = 100%", 55, [65, 45, 145],
                    "100%% %s 45%% = <b>55%%</b>. Check: 45 + 55 = 100. 65%% is a renaming mistake." % MINUS, kind="pct"))
    its.append(nmcq("In a hundred square, 30 squares are red and 25 squares are blue. The rest are white. What percentage of the squares are white?",
                    45, [55, 70, 75],
                    "Red and blue: 30 + 25 = 55 squares = 55%%. White: 100%% %s 55%% = <b>45%%</b>. "
                    "55%% is red and blue together." % MINUS, kind="pct"))
    its.append(nmcq("A hawker centre has 100 tables. 83 tables are taken. What percentage of the tables are empty?",
                    17, [83, 27, F("1.7")],
                    "100 %s 83 = 17 empty tables out of 100, so <b>17%%</b>. 83%% of the tables are taken." % MINUS, kind="pct"))
    its.append(mcq("Which is the largest part of a whole?", "90%", ["9%", "19%", "89%"],
                   "All of them are out of 100. 90 out of 100 is the most, so <b>90%</b> is the largest."))
    its.append(nmcq("Ali shaded 7 squares of a hundred square. Mei Ling shaded 30% of another hundred square. "
                    "How many more squares did Mei Ling shade than Ali?", 23, [37, 33, 13],
                    "30%% of a hundred square is 30 squares. 30 %s 7 = <b>23</b>. 37 adds instead of subtracts." % MINUS))
    its.append(nmcq("A packet has 100 beads. 4 of the beads are broken. What percentage of the beads are broken?",
                    4, [96, 40, F("0.4")],
                    "4 out of 100 = %s = <b>4%%</b>. 96%% of the beads are not broken. 40%% would be 40 beads." % fr(4, 100), kind="pct"))
    its.append(nmcq("How many squares must you shade to show <b>1%</b> of a hundred square?", 1, [10, 100, 99],
                    "1%% means 1 out of 100, so shade <b>1</b> square. 10 squares would be 10%%."))
    assert len(its) == 20, len(its)
    return {"title": "Percentage means out of 100: hundred squares", "items": its}


# ============================================================ set 2: fractions and decimals to percentages
def set_convert():
    its = []
    for a, b, wr, note in [
            (3, 10, [3, 13, 70], "Do not write the numerator as the percentage."),
            (1, 4, [14, 4, 75], "Do not join the 1 and the 4 together. 75% is the other three quarters."),
            (3, 5, [35, 53, 40], "3/5 is not 35%: do not write the 3 and the 5 together."),
            (7, 20, [7, 27, 65], "Do not add 7 and 20. 65% is the other part."),
            (3, 4, [34, 25, F("7.5")], "Do not join the 3 and the 4. 25% is the part that is left."),
            (9, 25, [9, 34, 64], "9% would be 9 out of 100. 34 is 9 + 25."),
            (4, 5, [45, 20, 8], "4/5 is not 45%. 20% is the other fifth."),
            (1, 5, [15, 5, 80], "Do not join the 1 and the 5. 5% would be 1 out of 20."),
            (13, 50, [13, 63, 74], "13% would be 13 out of 100. 63 is 13 + 50."),
            (11, 20, [11, 31, 45], "11% would be 11 out of 100. 45% is the other part."),
            (2, 25, [2, 27, 92], "2% would be 2 out of 100. 92% is the other part."),
            (19, 20, [19, 5, 39], "19% would be 19 out of 100. 5% is the part that is left.")]:
        p = F(a, b) * 100
        m = 100 // b
        assert m * b == 100
        e = ("Multiply the numerator and the denominator by %d to make the denominator 100: %s = %s = <b>%s%%</b>. "
             "Or: %s × 100%% = %s%%. " % (m, fr(a, b), fr(num(p), 100), num(p), fr(a, b), num(p))) + note.replace(
            "%d/%d" % (a, b), fr(a, b))
        its.append(nmcq("Write %s as a percentage." % fr(a, b), p, wr, e, kind="pct"))

    for d, wr, note in [
            ("0.4", [4, F("0.4"), 400], "0.4 = 4 tenths = 40 hundredths. 4% would be 0.04."),
            ("0.75", [F("7.5"), F("0.75"), 25], "Multiply by 100, not by 10. 25% is the part that is left."),
            ("0.08", [80, F("0.08"), F("0.8")], "0.08 is 8 hundredths, not 8 tenths. 80% would be 0.8."),
            ("0.36", [F("3.6"), 360, 64], "Move the digits two places to the left (× 100), not one."),
            ("0.5", [5, F("0.5"), 500], "0.5 = 5 tenths = 50 hundredths. 5% would be 0.05.")]:
        v = F(d)
        p = v * 100
        e = "%s × 100%% = <b>%s%%</b>. " % (d, num(p)) + note
        its.append(nmcq("Write <b>%s</b> as a percentage." % d, p, wr, e, kind="pct"))

    assert F(35, 100) == F(7, 20)
    its.append(mcq("Write <b>35%</b> as a fraction in its simplest form.", fr(7, 20), [fr(3, 5), fr(7, 10), fr(1, 35)],
                   "35%% = %s. Divide the numerator and the denominator by 5: <b>%s</b>. %s = 70%%." % (fr(35, 100), fr(7, 20), fr(7, 10))))
    assert F(6, 100) == F("0.06")
    its.append(mcq("Write <b>6%</b> as a decimal.", "0.06", ["0.6", "0.006", "6"],
                   "6%% = %s = 6 hundredths = <b>0.06</b>. 0.6 is 6 tenths = 60%%." % fr(6, 100)))
    assert F(13, 20) * 100 == 65
    its.append(mcq("Which is the greatest?", fr(13, 20), ["0.6", "62%", "0.58"],
                   "Write them all as percentages: %s = 65%%, 0.6 = 60%%, 0.58 = 58%%. The greatest is <b>%s</b>."
                   % (fr(13, 20), fr(13, 20))))
    assert len(its) == 20, len(its)
    return {"title": "Fractions and decimals as percentages", "items": its}


# ============================================================ set 3: part of a whole as a percentage
def set_part():
    its = []
    its.append(nmcq(fig(rect_grid_svg(4, 5, 7)) + "What percentage of the grid is shaded?", 35, [7, 65, 13],
                    "7 of the 20 squares are shaded. %s There are 20 squares, not 100, so it is not 7%%." % part_e(7, 20), kind="pct"))
    its.append(nmcq(fig(bar_svg(8, 2, None, [], ask="")) + "The bar has 8 equal parts. What percentage of the bar is shaded?",
                    25, [2, 75, 4],
                    "2 of the 8 parts are shaded. %s 4%% comes from 8 ÷ 2: do not divide the whole by the part." % part_e(2, 8), kind="pct"))
    its.append(nmcq(fig(rect_grid_svg(5, 5, 9)) + "What percentage of the grid is <b>not</b> shaded?", 64, [9, 36, 16],
                    "25 squares, 9 shaded, so 16 are not shaded. %s 36%% is the shaded part." % part_e(16, 25), kind="pct"))

    for part, n, wr, note in [
            (18, 40, [18, 55, 22], "18% would be 18 out of 100. 55% is the other part."),
            (5, 20, [5, 4, 75], "4% comes from 20 ÷ 5: do not divide the whole by the part."),
            (12, 60, [12, 5, 80], "5% comes from 60 ÷ 12: put the part on top, the whole at the bottom."),
            (9, 30, [9, 70, 21], "9% would be 9 out of 100. 21 is 30 − 9, not a percentage."),
            (21, 35, [21, 40, 14], "21% would be 21 out of 100. 40% is the other part."),
            (27, 36, [27, 25, 9], "27% would be 27 out of 100. 25% is the other part."),
            (33, 300, [33, 89, F("1.1")], "The whole is 300, not 100. 89% is the other part."),
            (72, 400, [72, 82, 36], "36% comes from dividing by 2 only: 36/200 is not out of 100. 72% would be 72 out of 100."),
            (120, 500, [12, 76, 120], "12% drops a zero. 120% would be 120 out of 100. 76% is the other part."),
            (15, 75, [15, 5, 80], "5% comes from 75 ÷ 15: do not divide the whole by the part.")]:
        p = F(part * 100, n)
        e = part_e(part, n) + " " + note.replace("%d/%d" % (part, n), fr(part, n)).replace("18/100", fr(18, 100)) \
            .replace("36/200", fr(36, 200)).replace("24/100", fr(24, 100)).replace("30 − 9", "30 " + MINUS + " 9")
        its.append(nmcq("Express <b>%s out of %s</b> as a percentage." % (num(part), num(n)), p, wr, e, kind="pct"))

    its.append(nmcq("What percentage of $50 is $12?", 24, [12, 76, 38],
                    "%s Do not write $12 as 12%%: the whole is $50, not $100." % part_e(12, 50), kind="pct"))
    its.append(nmcq("What percentage of 2 m is 50 cm?", 25, [50, 4, 75],
                    "Use the same unit: 2 m = 200 cm. %s 50%% forgets to change 2 m to 200 cm." % part_e(50, 200), kind="pct"))
    its.append(nmcq("What percentage of 1 kg is 300 g?", 30, [300, 3, 70],
                    "1 kg = 1000 g. %s 300%% forgets to change 1 kg to 1000 g." % part_e(300, 1000), kind="pct"))
    its.append(nmcq("What percentage of 1 h is 15 min?", 25, [15, 4, 75],
                    "1 h = 60 min. %s 1 h has 60 min, not 100 min, so it is not 15%%." % part_e(15, 60), kind="pct"))
    its.append(nmcq("What percentage of 2 ℓ is 400 ml?", 20, [40, 5, 80],
                    "2 ℓ = 2000 ml. %s 40%% uses 1000 ml instead of 2000 ml." % part_e(400, 2000), kind="pct"))
    assert F(6, 8) * 100 == 75 and F(14, 20) * 100 == 70
    its.append(mcq("Which is the greater percentage: 6 out of 8 or 14 out of 20?", "6 out of 8",
                   ["14 out of 20", "They are equal", "You cannot tell"],
                   "%s = 75%%. %s = 70%%. 75%% &gt; 70%%, so <b>6 out of 8</b> is greater, even though 14 is more than 6."
                   % (fr(6, 8), fr(14, 20))))
    assert F(18, 40) * 100 == 45
    its.append(mcq("Which calculation expresses <b>18 out of 40</b> as a percentage?",
                   fr(18, 40) + " × 100%", [fr(40, 18) + " × 100%", fr(18, 40) + " × 10%", fr(18, 100) + " × 40%"],
                   "Put the part (18) over the whole (40), then multiply by 100%%: %s × 100%% = 45%%. "
                   "%s divides the whole by the part." % (fr(18, 40), fr(40, 18))))
    assert len(its) == 20, len(its)
    return {"title": "Express a part of a whole as a percentage", "items": its}


# ============================================================ set 4: percentage of a quantity
def set_of():
    its = []
    its.append(nmcq(fig(unit_bar(4, 1, "$60", ask="25% = ?")) + "The bar model shows $60 in 4 equal units. What is <b>25%</b> of $60?",
                    15, [35, 45, F("2.4")],
                    "4 units = 100%% = $60, so 1 unit = 25%% = $60 ÷ 4 = <b>$15</b>. %s "
                    "$35 is $60 %s 25: 25%% is not 25 dollars. $45 is the other 75%%." % (of_e(25, 60, money_=True), MINUS), kind="money"))
    for p, n, u, wr, note in [
            (10, 80, "", [F("0.8"), 70, 800], "10% means ÷ 10, not ÷ 100. Do not take away 10."),
            (50, 64, "", [128, 14, F("3.2")], "50% is a half, not double. 14 is 64 − 50."),
            (20, 150, "", [130, F("7.5"), 120], "130 is 150 − 20. 7.5 is 150 ÷ 20. 120 is the other 80%."),
            (75, 48, "", [12, 64, 24], "12 is only 25% and 24 is 50%. 64 is 48 ÷ 3/4."),
            (30, 90, "", [60, 3, 9], "60 is 90 − 30. 3 is 90 ÷ 30. 9 is only 10%."),
            (15, 200, "", [185, 20, 15], "185 is 200 − 15. 20 is only 10%. 15 forgets that the whole is 200, not 100."),
            (5, 360, "", [72, 36, 355], "72 is 360 ÷ 5, which is 20%. 36 is 10%."),
            (12, 50, "", [38, 5, 44], "38 is 50 − 12. 5 is only 10%. 44 is the other 88%."),
            (35, 400, " ml", [365, 260, 14], "365 ml is 400 − 35. 260 ml is the other 65%."),
            (90, 70, "", [7, 60, 77], "7 is the 10% that is left out. 60 is 70 − 10."),
            (1, 900, "", [90, 899, F("0.9")], "1% means ÷ 100. 90 would be 10%."),
            (45, 80, "", [44, 35, 32], "44 is the other 55%. 35 is 80 − 45. 32 is only 40%.")]:
        r = F(p) * F(n) / 100
        its.append(nmcq("Find <b>%d%%</b> of %s%s." % (p, num(n), u), r, wr,
                        of_e(p, n, u) + " " + note.replace(" − ", " " + MINUS + " ").replace("3/4", fr(3, 4)), unit=u))
    its.append(nmcq("Find <b>40%</b> of $35.", 14, [21, F("3.5"), F("1.4")],
                    of_e(40, 35, money_=True) + " $21 is the other 60%. $3.50 is only 10%.", kind="money"))
    its.append(nmcq("Find <b>8%</b> of $250.", 20, [200, 242, 25],
                    of_e(8, 250, money_=True) + " $200 is 80%. $242 is $250 " + MINUS + " 8. $25 is only 10%.", kind="money"))
    its.append(nmcq("Find <b>60%</b> of 2 kg. Give your answer in grams.", 1200, [120, 800, 12],
                    "2 kg = 2000 g. " + of_e(60, 2000, " g") + " 800 g is the other 40%.", unit=" g"))
    its.append(nmcq("Find <b>25%</b> of 1 ℓ. Give your answer in millilitres.", 250, [750, 25, 40],
                    "1 ℓ = 1000 ml. " + of_e(25, 1000, " ml") + " 40 ml is 1000 ÷ 25. 750 ml is the other 75%.", unit=" ml"))
    its.append(nmcq("Find <b>70%</b> of 3 m. Give your answer in centimetres.", 210, [90, 21, 230],
                    "3 m = 300 cm. " + of_e(70, 300, " cm") + " 90 cm is the other 30%. 230 cm is 300 " + MINUS + " 70.", unit=" cm"))
    its.append(nmcq(fig(unit_bar(10, 3, "240", ask="30% = ?")) + "The bar model shows 240 in 10 equal units. What is <b>30%</b> of 240?",
                    72, [8, 168, 210],
                    "10 units = 100%% = 240, so 1 unit = 10%% = 24. 3 units = 30%% = 3 × 24 = <b>72</b>. "
                    "8 is 240 ÷ 30. 168 is the other 70%%. 210 is 240 %s 30." % MINUS))
    assert F(25, 100) * 60 == 15
    its.append(mcq("Which calculation finds <b>25% of 60</b>?", fr(25, 100) + " × 60",
                   ["60 ÷ 25", "60 " + MINUS + " 25", fr(100, 25) + " × 60"],
                   "25%% = %s, so 25%% of 60 = %s × 60 = 15. 60 ÷ 25 divides by the percentage instead." % (fr(25, 100), fr(25, 100))))
    assert len(its) == 20, len(its)
    return {"title": "Find a percentage of a quantity", "items": its}


# ============================================================ set 5: word problems
def set_words():
    its = []
    M = "money"

    assert F(36, 40) * 100 == 90
    its.append(nmcq("Mei Ling scored 36 out of 40 marks in a maths test. What percentage of the marks did she score?",
                    90, [36, 10, 9],
                    "%s 9%% comes from %s = %s: that is 9 tenths, not 9 hundredths. 10%% is the part she did not score." % (part_e(36, 40), fr(36, 40), fr(9, 10)), kind="pct"))

    assert F(14, 40) * 100 == 35
    its.append(nmcq("In a class survey, 14 of the 40 students chose chicken rice as their favourite hawker food. "
                    "What percentage of the students chose chicken rice?", 35, [14, 65, 26],
                    "%s 14%% would be 14 out of 100. 65%% chose other food." % part_e(14, 40), kind="pct"))

    assert F(35, 100) * 200 == 70
    its.append(nmcq("200 students were asked how they travel to school. 35% of them take the MRT. How many students take the MRT?",
                    70, [35, 130, 165],
                    of_e(35, 200) + " 35 would be 35 out of 100, but there are 200 students. 130 is the other 65%."))

    assert F(20, 100) * 60 == 12
    its.append(nmcq(fig(unit_bar(5, 1, "$60", ask="saves ?")) +
                    "Hafiz gets $60 of pocket money a month. He saves 20% of it. How much does he save each month?",
                    12, [48, 40, 3],
                    "5 units = 100%% = $60, so 1 unit = 20%% = $60 ÷ 5 = <b>$12</b>. "
                    "$48 is what he spends. $40 is $60 %s 20. $3 is $60 ÷ 20." % MINUS, kind=M))

    assert F(45, 150) * 100 == 30
    its.append(nmcq("Siti had $150. She saved $45 of it. What percentage of her money did she save?",
                    30, [45, 70, F("0.3")],
                    "%s 0.3%% forgets to multiply %s = 0.3 by 100%%. 70%% is the part she did not save." % (part_e(45, 150), fr(45, 150)), kind="pct"))

    assert 40 - F(45, 100) * 40 == 22
    its.append(nmcq("There are 40 students in a class. 45% of them are boys. How many girls are there?",
                    22, [18, 55, 5],
                    "Girls: 100%% %s 45%% = 55%%. 55%% of 40 = %s × 40 = <b>22</b>. 18 is the number of boys. "
                    "55 is the percentage of girls, not the number." % (MINUS, fr(55, 100))))

    assert 80 - F(20, 100) * 80 == 64
    its.append(nmcq(fig(unit_bar(5, 1, "80 oranges", ask="left = ?", span=(1, 5))) +
                    "Mrs Ng bought 80 mandarin oranges for Chinese New Year. She gave 20% of them to her neighbours. "
                    "How many oranges did she have left?", 64, [16, 60, 20],
                    "5 units = 100%% = 80, so 1 unit = 20%% = 80 ÷ 5 = 16. She gave away 1 unit and kept 4 units: 4 × 16 = <b>64</b>. "
                    "16 is the number she gave away. 60 is 80 %s 20. 20 is 80 ÷ 4." % MINUS))

    assert F(25, 100) * 40 == 10
    its.append(nmcq("In a class of 40 students, 30% take the school bus and 45% come by car. The rest walk to school. "
                    "How many students walk?", 10, [25, 12, 18],
                    "Walk: 100%% %s 30%% %s 45%% = 25%%. 25%% of 40 = 40 ÷ 4 = <b>10</b>. "
                    "25 is the percentage, not the number of students. 12 take the bus and 18 come by car." % (MINUS, MINUS)))

    assert 250 - F(92, 100) * 250 == 20
    its.append(nmcq("250 students ran in a race on Sports Day. 92% of them finished the race. How many students did not finish?",
                    20, [230, 8, 25],
                    "Did not finish: 100%% %s 92%% = 8%%. 8%% of 250 = %s × 250 = <b>20</b>. "
                    "230 finished. 8 is the percentage, not the number." % (MINUS, fr(8, 100))))

    assert F(5, 25) * 100 == 20
    its.append(nmcq("Ryan answered 25 questions in a quiz. He got 20 of them correct. What percentage of the questions did he get wrong?",
                    20, [80, 5, 25],
                    "He got 25 %s 20 = 5 wrong. %s 80%% is the percentage he got correct." % (MINUS, part_e(5, 25)), kind="pct"))

    assert F(60, 100) * 500 == 300
    its.append(nmcq(fig(unit_bar(5, 3, "500 ℓ", ask="?")) +
                    "A water tank holds 500 ℓ when it is full. It is 60% full. How much water is in the tank?",
                    300, [200, 440, 30],
                    "5 units = 100%% = 500 ℓ, so 1 unit = 20%% = 100 ℓ. 60%% is 3 units = <b>300 ℓ</b>. "
                    "200 ℓ is the empty part. 440 ℓ is 500 %s 60. 30 ℓ is only 6%%." % MINUS, unit=" ℓ"))

    assert F(15, 100) * 800 == 120
    its.append(nmcq("A school has 800 students. 15% of them are in a uniformed group CCA. How many students is that?",
                    120, [785, 680, 12],
                    of_e(15, 800) + " 785 is 800 " + MINUS + " 15. 680 is the other 85%."))

    assert F(40, 250) * 100 == 16
    its.append(nmcq("A class library has 250 books. 40 of them are borrowed. What percentage of the books are borrowed?",
                    16, [40, 84, F("0.16")],
                    "%s 40%% would be 40 out of 100. 0.16%% forgets to multiply by 100%%." % part_e(40, 250), kind="pct"))

    assert 1000 - F(30, 100) * 1000 == 700
    its.append(nmcq("Priya had 1 ℓ of orange juice. She drank 30% of it. How much juice was left? Give your answer in millilitres.",
                    700, [300, 970, 70],
                    "1 ℓ = 1000 ml. 30%% of 1000 ml = 300 ml. Left: 1000 ml %s 300 ml = <b>700 ml</b>. "
                    "300 ml is what she drank. 970 ml is 1000 %s 30." % (MINUS, MINUS), unit=" ml"))

    assert 20 - F(35, 100) * 20 == 13
    its.append(nmcq("Jun Jie had $20 on his EZ-Link card. He used 35% of it on bus and MRT rides. How much was left on the card?",
                    13, [7, 65, 14],
                    "35%% of $20 = %s × $20 = $7. Left: $20 %s $7 = <b>$13</b>. $7 is the amount used. $14 takes away only 30%%. "
                    "$65 is 100 %s 35: the money is $20, not $100." % (fr(35, 100), MINUS, MINUS), kind=M))

    assert 120 - F(75, 100) * 120 == 30
    its.append(nmcq(fig(unit_bar(4, 3, "120 durians", ask="left = ?", span=(3, 4))) +
                    "A fruit stall had 120 durians. 75% of them were sold. How many durians were left?",
                    30, [90, 45, 25],
                    "4 units = 120, so 1 unit = 120 ÷ 4 = 30. 3 units were sold and 1 unit is left: <b>30</b>. "
                    "90 were sold. 45 is 120 %s 75. 25 is the percentage left, not the number." % MINUS))

    assert F(42, 50) * 100 == 84 and F(17, 20) * 100 == 85
    its.append(mcq("Wei Ming scored 42 out of 50 in English and 17 out of 20 in science. In which test did he score the higher percentage?",
                   "Science", ["English", "They are equal", "You cannot tell"],
                   "English: %s = %s = 84%%. Science: %s = %s = 85%%. 85%% &gt; 84%%, so <b>science</b>, "
                   "even though he scored more marks in English." % (fr(42, 50), fr(84, 100), fr(17, 20), fr(85, 100))))

    assert 50 - F(40, 100) * 50 - F(10, 100) * 50 == 25
    its.append(nmcq("Zhi Hao had $50. He spent 40% of it on a book and 10% of it on bubble tea. How much money did he have left?",
                    25, [20, 30, 5],
                    "He spent 40%% + 10%% = 50%%. He had 50%% left: 50%% of $50 = <b>$25</b>. "
                    "$20 is the cost of the book and $5 is the bubble tea. $30 only takes away the book." , kind=M))

    assert F(65, 100) * 200 == 130
    its.append(nmcq("Xin Yi received $200 in red packets at Chinese New Year. She saved 65% of the money in the bank. "
                    "How much money did she save?", 130, [70, 135, 65],
                    of_e(65, 200, money_=True) + " $70 is what she did not save. $135 is $200 " + MINUS + " 65.", kind=M))

    assert F(5, 25) * 100 == 20 and F(12, 25) * 100 == 48
    its.append(nmcq("25 students voted for a class outing. 8 chose Sentosa, 12 chose Gardens by the Bay and the rest chose the Singapore Zoo. "
                    "What percentage of the students chose the Singapore Zoo?", 20, [5, 48, 80],
                    "Zoo: 25 %s 8 %s 12 = 5 students. %s 5%% would be 5 out of 100. 48%% chose Gardens by the Bay."
                    % (MINUS, MINUS, part_e(5, 25)), kind="pct"))
    assert len(its) == 20, len(its)
    return {"title": "Percentage word problems: test marks, surveys and savings", "items": its}


# ============================================================ lesson
def body_html():
    f_h = hundred_svg(37, cell=16)
    f_bar = unit_bar(4, 1, "$60", ask="25% = $15")
    f_grid = rect_grid_svg(4, 10, 18, cell=24)
    return (
        "<h2>Percentage means “out of 100”</h2>"
        "<p>A <b>percentage</b> is a part of a whole, written out of 100. The sign <b>%</b> means per cent. "
        "100% is the whole. 37% means 37 out of 100.</p>"
        "<figure class='sn-fig'>" + f_h +
        "<figcaption>37 of the 100 squares are shaded: " + fr(37, 100) + " = 37%. 63% is not shaded.</figcaption></figure>"
        "<h2>Fractions and decimals as percentages</h2>"
        "<p>Make the denominator 100, or multiply by 100%.</p>"
        + ex("Example", "Write " + fr(3, 5) + " as a percentage.",
             "Multiply the numerator and the denominator by 20: " + fr(3, 5) + " = " + fr(60, 100) + ".", "60%")
        + ex("Example", "Write 0.08 as a percentage.", "0.08 × 100% = 8%. (0.08 is 8 hundredths.)", "8%")
        + table(["Fraction", "Decimal", "Percentage"], [
            [fr(1, 2), "0.5", "50%"],
            [fr(1, 4), "0.25", "25%"],
            [fr(3, 4), "0.75", "75%"],
            [fr(1, 5), "0.2", "20%"],
            [fr(1, 10), "0.1", "10%"],
        ]) +
        "<h2>A part of a whole as a percentage</h2>"
        "<p>Put the <b>part</b> over the <b>whole</b>, then multiply by 100%.</p>"
        "<figure class='sn-fig'>" + f_grid +
        "<figcaption>18 out of 40 squares are shaded.</figcaption></figure>"
        + ex("Example", "Express 18 out of 40 as a percentage.",
             fr(18, 40) + " × 100% = 45%. Or: " + fr(18, 40) + " = " + fr(9, 20) + " = " + fr(45, 100) + ".", "45%")
        + "<p>Use the same unit for the part and the whole: 50 cm out of 2 m = 50 cm out of 200 cm = 25%.</p>"
        "<h2>A percentage of a quantity</h2>"
        "<p>Write the percentage as a fraction out of 100 and multiply. A bar model helps.</p>"
        "<figure class='sn-fig'>" + f_bar +
        "<figcaption>4 units = 100% = $60, so 1 unit = 25% = $60 ÷ 4 = $15.</figcaption></figure>"
        + ex("Example", "Find 25% of $60.", fr(25, 100) + " × $60 = $15.", "$15")
        + ex("Example", "A class has 40 students. 45% are boys. How many girls are there?",
             "Girls: 100% " + MINUS + " 45% = 55%. " + fr(55, 100) + " × 40 = 22.", "22 girls")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            [fr(3, 5) + " = 35%", "Make the denominator 100: " + fr(3, 5) + " = " + fr(60, 100) + " = 60%"],
            ["18 out of 40: 40 ÷ 18", "Part over whole: " + fr(18, 40) + " × 100% = 45%"],
            ["25% of 60 = 60 " + MINUS + " 25 = 35", fr(25, 100) + " × 60 = 15"],
            ["18 out of 40 = 18%", "18% means 18 out of 100. The whole here is 40"],
            ["0.08 = 80%", "0.08 is 8 hundredths: 0.08 × 100% = 8%"],
        ])
    )


FAQ = [
    {"q": "What is taught in P5 percentage?",
     "a": "Primary 5 students learn that percentage means out of 100, change fractions and decimals to percentages, express a part of a whole as a percentage and find a percentage of a quantity, such as 25% of $60."},
    {"q": "How do I explain percentage to my child?",
     "a": "Start with a hundred square: 37 squares shaded out of 100 is 37%. Then use a bar model: split $60 into 4 equal units, so 25% is 1 unit, $15."},
    {"q": "What is the most common mistake with percentage?",
     "a": "Writing the numbers of a fraction side by side, such as 3/5 = 35%. Make the denominator 100 instead: 3/5 = 60/100 = 60%."},
    {"q": "Is percentage in the MOE syllabus for Primary 5?",
     "a": "Yes. Percentage is a Primary 5 topic in the MOE 2021 Primary Mathematics Syllabus, and it is built on in Primary 6 for the PSLE."},
]


def gen():
    rnd = random.Random(65808)
    sets = [set_hundred(), set_convert(), set_part(), set_of(), set_words()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            for k in ("q", "e"):
                it[k] = it[k].replace("%%", "%")
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            assert "%%" not in it["e"] and "%%" not in it["q"], it
            assert len(re.findall("<svg", it["q"])) <= 1
            seen.add(it["q"])
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-5", "slug": "percentage", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 5 Percentage: Parts of a Whole and Percentage of a Quantity",
        "seo_title": "P5 Percentage Worksheets: Free Primary 5 Maths Practice with Answers (MOE Syllabus)",
        "short_title": "Percentage",
        "domain": "Number and Algebra",
        "standard_code": "Primary 5: Percentage",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Expressing a part of a whole as a percentage; use of %; finding a percentage part of a whole",
        "meta_desc": "Free P5 percentage practice: hundred squares, fractions and decimals as %, 18 out of 40 as a percentage, 25% of $60. 100 questions with answers.",
        "key_big": "Percentage means out of 100: part ÷ whole × 100%.",
        "key_sub": "18 out of 40 = 18/40 × 100% = 45%, and 25% of $60 = 25/100 × $60 = $15.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "(bar model|grid of)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
