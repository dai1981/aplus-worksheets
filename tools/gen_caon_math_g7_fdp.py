# -*- coding: utf-8 -*-
"""
Canada (Ontario) Grade 7 Math: Fractions, decimals and percents
(Ontario Curriculum, Grades 1-8: Mathematics, 2020 — Grade 7, Number, B1.7, with B2.2 and B2.3)
  python3 tools/gen_caon_math_g7_fdp.py
Fraction <-> decimal (positive and negative, terminating and repeating: 1/3 = 0.333…), decimal <-> percent
(including 12.5%, 0.5% and percents over 100%), fraction <-> percent, common equivalents
(1/8 = 0.125 = 12.5%), and mental math: increase or decrease a whole number by 1%, 5%, 10%, 25%, 50% and 100%,
with word problems.
Every answer is checked with fractions.Fraction / decimal.Decimal (never float); repeating decimals are built
from real long division.
Canadian English, dollars and cents, metric units, SI number spacing (no-break spaces), real minus sign.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal as Dm
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-7")
UPDATED = "2026-11-02"
FILL = "#4fae74"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
RED = "#d6453b"
BLUE = "#2f6fc0"
GREY = "#d9d9d9"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
NBSP = " "
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def nfr(a, b):
    """Negative fraction: −a/b."""
    return MINUS + fr(a, b)


def mixed(w, a, b):
    return "%d %s" % (w, fr(a, b))


def bar(s):
    """Digits under a repeat bar."""
    return "<span style='text-decoration:overline;text-decoration-thickness:0.09em'>%s</span>" % s


def period(v):
    """(whole, non-repeating digits, repeating digits) of a positive Fraction, from long division."""
    v = F(v)
    whole, r = divmod(v.numerator, v.denominator)
    d = v.denominator
    digits, seen = [], {}
    while r and r not in seen:
        seen[r] = len(digits)
        r *= 10
        digits.append(str(r // d))
        r %= d
    if not r:
        return whole, "".join(digits), ""
    k = seen[r]
    return whole, "".join(digits[:k]), "".join(digits[k:])


def check_period(v, whole, a, b):
    x = F(whole) + (F(int(a), 10 ** len(a)) if a else 0)
    if b:
        x += F(int(b), (10 ** len(b) - 1) * 10 ** len(a))
    assert x == F(v), (v, whole, a, b)


def dots(v, times=3):
    """Repeating decimal written with dots: 1/6 -> 0.1666…"""
    w, a, b = period(v)
    check_period(v, w, a, b)
    assert b, v
    return "%d.%s%s…" % (w, a, b * times)


def bart(v):
    """Repeating decimal written with a bar over the repeating digits."""
    w, a, b = period(v)
    check_period(v, w, a, b)
    assert b, v
    return "%d.%s%s" % (w, a, bar(b))


def dec(v):
    """Exact decimal text of a Fraction with a terminating decimal (real minus sign)."""
    v = F(v)
    d = Dm(abs(v.numerator)) / Dm(v.denominator)
    assert F(d) == abs(v), v
    s = format(d.normalize(), "f")
    return (MINUS + s) if v < 0 else s


def pct(v):
    return dec(F(v) * 100) + "%"


def D(s):
    return F(Dm(s.replace(MINUS, "-")))


def num(n):
    """Whole number in SI style: 4 digits plain, 5+ digits grouped with no-break spaces."""
    s = str(n)
    if len(s) <= 4:
        return s
    out = ""
    while len(s) > 3:
        out = NBSP + s[-3:] + out
        s = s[:-3]
    return s + out


def money(v):
    v = F(v)
    if v.denominator == 1:
        return "$" + num(v.numerator)
    assert (v * 100).denominator == 1, v
    return "$%d.%02d" % (int(v), int(v * 100) % 100)


FRX = re.compile(r"^(?:(\d+) )?<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>( .+)?$")
NUM = re.compile(r"^(\$)?(\d*\.?\d+)(¢|%)?( .+)?$")


def val(c):
    """Value of a choice (Fraction) with its unit; 20% counts as 0.2. None for choices that are not a single
    terminating number (repeating decimals are checked where they are built)."""
    if c.startswith(MINUS):
        v = val(c[1:])
        return None if v is None else (-v[0], v[1])
    c = c.replace(NBSP, "")
    m = FRX.match(c)
    if m:
        return (int(m.group(1) or 0) + F(int(m.group(2)), int(m.group(3))), (m.group(4) or "").strip())
    m = NUM.match(c)
    if not m:
        return None
    v = F(Dm(m.group(2)))
    if m.group(1):
        return (v, "$")
    if m.group(3) == "¢":
        return (v / 100, "$")
    if m.group(3) == "%":
        v = v / 100
    return (v, (m.group(4) or "").strip())


def mcq(q, correct, wrong, e, same_ok=False, value=None):
    """4 choices: correct first + 3 wrong. No two choices may have the same value
    (same_ok=True only for 'which is NOT equal' and list/statement choices). value: the exact answer to check."""
    correct = str(correct)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [correct] + wrong
    assert len(set(re.sub(r"<[^>]+>", "", x) for x in ch)) == 4, (q, ch)
    if value is not None:
        assert val(correct)[0] == F(value), (q, correct, value)
    if not same_ok:
        vs = [val(x) for x in ch]
        known = [v for v in vs if v is not None]
        assert len(set(known)) == len(known), (q, ch)
    return {"q": q, "c": ch, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
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


def text(x, y, t, fs=16, anchor="middle", col=LINE, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


# ------------------------------------------------------------ pictures
def sfr(x, y, a, b, size=15, color=LINE):
    """Stacked fraction drawn in SVG, centred at x. y is the numerator baseline."""
    w = size * 0.62 * max(len(str(a)), len(str(b))) + 4
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5'/>"
            "<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
            % (x, y, size, color, a, x - w / 2, y + 4, x + w / 2, y + 4, color, x, y + size + 4, size, color, b))


def bar_svg(n, k, W=264, H=38):
    """One fraction bar of n equal parts, first k shaded."""
    s = []
    for i in range(n):
        s.append("<rect x='%.1f' y='4' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (4 + i * W / float(n), W / float(n), H, FILL if i < k else "#fff", LINE))
    return svg_wrap(W + 8, H + 8, "".join(s), "fraction bar of %d equal parts with %d shaded" % (n, k))


def grids_svg(ks, cell=15):
    """Hundred grids side by side (each grid is one whole); ks[i] squares shaded in grid i,
    full columns first, then from the top of the next column."""
    pad, gap = 4, 18
    side = 10 * cell
    s = []
    for g, k in enumerate(ks):
        ox = pad + g * (side + gap)
        for c in range(10):
            for r in range(10):
                if c * 10 + r < k:
                    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>"
                             % (ox + c * cell, pad + r * cell, cell, cell, FILL))
        for i in range(1, 10):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.1'/>"
                     % (ox + i * cell, pad, ox + i * cell, pad + side, THIN))
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.1'/>"
                     % (ox, pad + i * cell, ox + side, pad + i * cell, THIN))
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (ox, pad, side, side, LINE))
    w = 2 * pad + len(ks) * side + (len(ks) - 1) * gap
    lab = ("hundred grid with %d of 100 squares shaded" % ks[0] if len(ks) == 1 else
           "%d hundred grids, each one whole, with %s squares shaded" % (len(ks), " and ".join(str(k) for k in ks)))
    return svg_wrap(w, side + 2 * pad, "".join(s), lab)


def sdiv(a, b, places, hide=False, repeat=False):
    """Short division of a ÷ b to `places` decimal places, drawn from the real working. Remainders are carried
    as small red digits. repeat=True: the remainder never reaches 0, so '…' is drawn after the digits.
    hide=True draws the answer digits after the point as empty boxes."""
    w = str(a)
    cells = list(w) + ["."] + ["0"] * places
    q, carry, rem = [], {}, 0
    for i, ch in enumerate(cells):
        if ch == ".":
            q.append(".")
            continue
        cur = rem * 10 + int(ch)
        q.append(str(cur // b))
        rem = cur % b
        nxt = i + 1 if i + 1 < len(cells) and cells[i + 1] != "." else i + 2
        if rem and nxt < len(cells):
            carry[nxt] = str(rem)
    if repeat:
        assert rem != 0, (a, b)
        assert F(Dm("".join(q))) == F(int(F(a, b) * 10 ** places), 10 ** places), (q, a, b)
    else:
        assert rem == 0, (a, b)
        assert F(Dm("".join(q))) == F(a, b), (q, a, b)
    lead = 0
    while lead < len(w) - 1 and q[lead] == "0":
        lead += 1
    CW, DW = 30, 14
    xs, x = [], 62
    for ch in cells:
        xs.append(x)
        x += DW if ch == "." else CW
    W = x + (34 if repeat else 10)
    ytop, ybar, ydig = 34, 46, 78
    o = []
    for i, ch in enumerate(cells):
        cx = xs[i] + (DW if ch == "." else CW) / 2.0
        if ch == ".":
            o.append("<circle cx='%.1f' cy='%d' r='3.5' fill='%s'/>" % (cx, ydig - 2, LINE))
            o.append("<circle cx='%.1f' cy='%d' r='3.5' fill='%s'/>" % (cx, ytop - 2, LINE))
            continue
        o.append(text(cx + 3, ydig, ch, 26))
        if i in carry:
            o.append(text(xs[i] + 5, ydig - 14, carry[i], 15, col=RED))
        if i < lead:
            continue
        if hide and i > len(w):
            o.append("<rect x='%.1f' y='%d' width='20' height='24' fill='#fff' stroke='%s' stroke-width='1.8' rx='3'/>"
                     % (cx - 10, ytop - 22, LINE))
        else:
            o.append(text(cx + 3, ytop, q[i], 26))
    if repeat:
        o.append(text(x + 14, ytop, "…", 26))
        o.append(text(x + 14, ydig, "…", 26))
    o.append("<line x1='54' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (ybar, W - 6, ybar, LINE))
    o.append("<path d='M 54 %d Q 62 %d 54 %d' fill='none' stroke='%s' stroke-width='2.5'/>" % (ybar, ybar + 22, ybar + 44, LINE))
    o.append(text(30, ydig, str(b), 26))
    return svg_wrap(W, ybar + 50, "".join(o), "short division of %s by %d%s"
                    % ("".join(cells), b, " that keeps going" if repeat else ""))


def dline_svg(parts, dot=None, top=None, bottom=None, W=400):
    """Double number line: fractions above (top = {tick: (a, b) or text}), percents below (bottom = {tick: text}).
    Red dot at tick `dot`."""
    L, R, Y = 34, W - 34, 46
    top = top or {}
    bottom = bottom or {}

    def X(i):
        return L + (R - L) * i / float(parts)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for i in range(parts + 1):
        big = i in (0, parts)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(i), Y - (12 if big else 9), X(i), Y + (12 if big else 9), LINE, "2.5" if big else "1.8"))
    for i, t in top.items():
        if isinstance(t, tuple):
            s.append(sfr(X(i), 4 + 14, t[0], t[1], 14))
        else:
            s.append(text(X(i), 28, t, 16))
    for i, t in bottom.items():
        s.append(text(X(i), Y + 32, t, 15 if len(t) > 4 else 16))
    if dot is not None:
        s.append("<circle cx='%.1f' cy='%d' r='8' fill='%s'/>" % (X(dot), Y, RED))
    return svg_wrap(W, Y + 42, "".join(s),
                    "double number line split into %d equal parts, fractions above and percents below" % parts)


def pbar_svg(total, n, k, mode, W=320, H=40, fmt=money):
    """Percent bar model: a bar for `total` (100%) split into n equal parts (each total/n).
    mode 'off': the last k parts are taken away (grey, crossed). mode 'more': k extra parts are added on the right."""
    part = F(total, n)
    extra = k if mode == "more" else 0
    pw = W / float(n + (k if mode == "more" else 0))
    x0, y0 = 6, 30
    s = []
    for i in range(n + extra):
        x = x0 + i * pw
        added = i >= n
        gone = mode == "off" and i >= n - k
        s.append("<rect x='%.1f' y='%d' width='%.2f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'%s/>"
                 % (x, y0, pw, H, GREY if gone else (BLUE if added else FILL), LINE,
                    " stroke-dasharray='6 4'" if added else ""))
        s.append(text(x + pw / 2, y0 + H / 2 + 6, fmt(part), 15, col="#fff" if added else LINE))
        if gone:
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>"
                     % (x + 4, y0 + H - 4, x + pw - 4, y0 + 4, RED))
    # bracket over the original 100%
    xe = x0 + n * pw
    s.append("<path d='M %.1f %d L %.1f %d L %.1f %d L %.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
             % (x0, y0 - 4, x0, y0 - 12, xe, y0 - 12, xe, y0 - 4, LINE))
    lab = "%s = 100%%" % fmt(total)
    lw = 9 * len(lab) + 16
    s.append("<rect x='%.1f' y='3' width='%d' height='20' fill='#fff'/>" % ((x0 + xe) / 2 - lw / 2.0, lw))
    s.append(text((x0 + xe) / 2, 19, lab, 15))
    p = F(100 * k, n)
    if mode == "off":
        xa = x0 + (n - k) * pw
        s.append(text((xa + xe) / 2, y0 + H + 22, "%s%% off" % dec(p), 15, col=RED))
    else:
        s.append(text((xe + xe + k * pw) / 2, y0 + H + 22, "+%s%%" % dec(p), 15, col=BLUE))
    Wt = int(x0 + (n + extra) * pw + 6)
    return svg_wrap(Wt, y0 + H + 30, "".join(s),
                    "bar model of %s split into %d equal parts with %d parts %s"
                    % (fmt(total), n, k, "taken off" if mode == "off" else "added"))


# ============================================================ set 1: fractions and decimals
def set_fraction_decimal():
    its = []

    def f2d(v, right, wrong, e, q=None, fg=""):
        if "…" in right:
            assert right == dots(v), (v, right)
        else:
            assert D(right) == F(v), (v, right)
        its.append(mcq(fg + (q or "Write %s as a decimal." % fr(v.numerator, v.denominator)), right, wrong, e))

    f2d(F(7, 20), "0.35", ["0.72", "0.7", "0.035"],                                     # 0
        "20 × 5 = 100, so multiply the top by 5 too: %s = %s = <b>0.35</b>. 0.72 just writes the digits 7 and 20, "
        "and 0.7 would be %s." % (fr(7, 20), fr(35, 100), fr(7, 10)))
    f2d(F(1, 8), "0.125", ["0.8", "0.18", "0.12"],                                       # 1
        "Divide 1 by 8: 10 ÷ 8 = 1 R 2, 20 ÷ 8 = 2 R 4, 40 ÷ 8 = 5. So %s = <b>0.125</b>. "
        "0.8 uses the denominator as the decimal, and 0.12 stops before the remainder is 0." % fr(1, 8))
    f2d(F(3, 8), "0.375", ["0.38", "0.83", "0.3"],                                       # 2
        "30 ÷ 8 = 3 R 6, 60 ÷ 8 = 7 R 4, 40 ÷ 8 = 5. So 3 ÷ 8 = <b>0.375</b>. "
        "0.38 and 0.83 only use the digits of the fraction.",
        q="The division shows 3 ÷ 8. What is %s as a decimal?" % fr(3, 8), fg=fig(sdiv(3, 8, 3, hide=True)))
    f2d(F(11, 4), "2.75", ["11.4", "2.3", "0.275"],                                      # 3
        "11 ÷ 4 = 2 R 3, so %s = %s. %s = 0.75, so the answer is <b>2.75</b>. "
        "2.3 writes the remainder 3 as a decimal digit." % (fr(11, 4), mixed(2, 3, 4), fr(3, 4)))
    f2d(F(19, 8), "2.375", ["2.38", "23.8", "2.83"],                                     # 4
        "The 2 wholes stay the same. %s = 3 ÷ 8 = 0.375. So %s = <b>2.375</b>." % (fr(3, 8), mixed(2, 3, 8)),
        q="Write %s as a decimal." % mixed(2, 3, 8))
    f2d(F(7, 25), "0.28", ["0.725", "0.07", "0.32"],                                     # 5
        "25 × 4 = 100, so %s = %s = <b>0.28</b>. 0.07 forgets to multiply the top by 4, and 0.32 adds 7 + 25."
        % (fr(7, 25), fr(28, 100)))

    def d2f(s, right, wrong, e, v):
        assert D(s) == v
        its.append(mcq("Write <b>%s</b> as a fraction in simplest form." % s, right, wrong, e, value=v))

    d2f("0.45", fr(9, 20), [fr(45, 10), fr(4, 5), fr(1, 45)],                           # 6
        "0.45 = 45 hundredths = %s. Divide the top and bottom by 5: <b>%s</b>. %s would be 4.5."
        % (fr(45, 100), fr(9, 20), fr(45, 10)), F(9, 20))
    d2f("0.125", fr(1, 8), [fr(125, 100), fr(1, 125), fr(1, 12)],                      # 7
        "0.125 has three decimal places, so it is %s. Divide the top and bottom by 125: <b>%s</b>. "
        "%s would be 1.25." % (fr(125, 1000), fr(1, 8), fr(125, 100)), F(1, 8))
    d2f("0.06", fr(3, 50), [fr(6, 10), fr(6, 1000), fr(1, 6)],                          # 8
        "0.06 = 6 hundredths = %s. Divide the top and bottom by 2: <b>%s</b>. %s would be 0.6, and %s would be 0.006."
        % (fr(6, 100), fr(3, 50), fr(6, 10), fr(6, 1000)), F(3, 50))

    # negative numbers
    its.append(mcq("Write %s as a decimal." % nfr(3, 4), MINUS + "0.75", ["0.75", MINUS + "0.34", MINUS + "7.5"],   # 9
                   "%s = 0.75, and the sign stays the same: %s = <b>%s0.75</b>. 0.75 is positive, so it is on the "
                   "other side of 0." % (fr(3, 4), nfr(3, 4), MINUS), value=F(-3, 4)))
    its.append(mcq("Write %s as a decimal." % nfr(2, 5), MINUS + "0.4", [MINUS + "0.25", "0.4", MINUS + "2.5"],     # 10
                   "%s = %s = 0.4, so %s = <b>%s0.4</b>. %s2.5 is 5 ÷ 2, the wrong way round."
                   % (fr(2, 5), fr(4, 10), nfr(2, 5), MINUS, MINUS), value=F(-2, 5)))
    its.append(mcq("Write <b>%s0.8</b> as a fraction in simplest form." % MINUS, nfr(4, 5),                       # 11
                   [fr(4, 5), nfr(1, 8), nfr(8, 100)],
                   "0.8 = %s = %s. Keep the negative sign: %s0.8 = <b>%s</b>. %s would be %s0.08."
                   % (fr(8, 10), fr(4, 5), MINUS, nfr(4, 5), nfr(8, 100), MINUS), value=F(-4, 5)))
    its.append(mcq("Write <b>1.6</b> as a mixed number in simplest form.", mixed(1, 3, 5),                        # 12
                   [mixed(1, 1, 6), fr(16, 100), mixed(1, 3, 50)],
                   "1.6 = 1 and 6 tenths = %s. Simplify %s: <b>%s</b>. %s would be 0.16."
                   % (mixed(1, 6, 10), fr(6, 10), mixed(1, 3, 5), fr(16, 100)), value=F(8, 5)))

    # repeating decimals
    f2d(F(1, 3), dots(F(1, 3)), ["0.3", "0.13", "3.0"],                                  # 13
        "1 ÷ 3: 10 ÷ 3 = 3 R 1, and the remainder 1 keeps coming back, so the 3s never stop. "
        "%s = <b>0.333…</b>, also written %s with a bar over the digit that repeats. 0.3 is only %s."
        % (fr(1, 3), bart(F(1, 3)), fr(3, 10)),
        q="The division shows 1 ÷ 3. What is %s as a decimal?" % fr(1, 3), fg=fig(sdiv(1, 3, 4, repeat=True)))
    f2d(F(2, 3), dots(F(2, 3)), ["0.23", "0.6", "1.5"],                                  # 14
        "2 ÷ 3: 20 ÷ 3 = 6 R 2, and the remainder 2 keeps coming back. %s = <b>0.666…</b> = %s. "
        "1.5 is 3 ÷ 2, the wrong way round." % (fr(2, 3), bart(F(2, 3))))
    f2d(F(5, 6), dots(F(5, 6)), ["0.56", "0.83", "1.2"],                                 # 15
        "5 ÷ 6: 50 ÷ 6 = 8 R 2, then 20 ÷ 6 = 3 R 2 again and again. Only the 3 repeats: "
        "%s = <b>0.8333…</b> = %s. 0.83 stops too early, and 1.2 is 6 ÷ 5." % (fr(5, 6), bart(F(5, 6))))
    f2d(F(4, 9), dots(F(4, 9)), ["0.49", "0.4", "2.25"],                                 # 16
        "4 ÷ 9: 40 ÷ 9 = 4 R 4, and the remainder 4 keeps coming back. %s = <b>0.444…</b> = %s. "
        "2.25 is 9 ÷ 4, the wrong way round." % (fr(4, 9), bart(F(4, 9))))
    w, a, b = period(F(1, 6))
    assert (a, b) == ("1", "6")
    its.append(mcq("The repeating decimal 0.1%s means 0.1666… What digit is in the <b>thousandths</b> place?"     # 17
                   % bar("6"), "6", ["1", "0", "7"],
                   "The bar is over the 6 only, so 0.1%s = 0.1666…: tenths 1, hundredths 6, thousandths <b>6</b>, "
                   "and the 6s keep going. 7 would come from rounding, but the number is not rounded." % bar("6"),
                   same_ok=True))
    assert bart(F(1, 3)) == "0." + bar("3")
    its.append(mcq("Which fraction is equal to 0.%s?" % bar("3"), fr(1, 3), [fr(33, 100), fr(3, 10), fr(1, 33)],   # 18
                   "1 ÷ 3 = 0.333…, so 0.%s = <b>%s</b>. %s = 0.33 and %s = 0.3 both stop, so they are a little less."
                   % (bar("3"), fr(1, 3), fr(33, 100), fr(3, 10)), value=F(1, 3)))
    assert bart(F(1, 6)) == "0.1" + bar("6")
    its.append(mcq("Which fraction is equal to 0.1%s? Divide to check." % bar("6"), fr(1, 6),                     # 19
                   [fr(1, 16), fr(16, 100), fr(1, 7)],
                   "1 ÷ 6: 10 ÷ 6 = 1 R 4, then 40 ÷ 6 = 6 R 4 again and again, so %s = 0.1666… = 0.1%s. "
                   "The answer is <b>%s</b>. %s = 0.0625 and %s = 0.16 stops."
                   % (fr(1, 6), bar("6"), fr(1, 6), fr(1, 16), fr(16, 100)), value=F(1, 6)))
    assert len(its) == 20, len(its)
    return {"title": "Fractions and decimals, including negative and repeating decimals", "items": its}


# ============================================================ set 2: decimals and percents
def set_decimal_percent():
    its = []
    its.append(mcq(fig(grids_svg([40])) + "What percent of the hundred grid is shaded?", "40%", ["4%", "0.4%", "60%"],
                   "40 of the 100 squares are shaded. Percent means <b>out of 100</b>, so it is <b>40%</b> = 0.4. "
                   "60% is the white part."))
    for d_, right, wrong, e in [
        ("0.4", "40%", ["4%", "0.4%", "400%"],
         "Multiply by 100: 0.4 × 100 = 40, so 0.4 = <b>40%</b>. 0.4 is 4 <b>tenths</b>, not 4 hundredths, so it is not 4%."),
        ("0.08", "8%", ["80%", "0.08%", "0.8%"],
         "0.08 = 8 hundredths = <b>8%</b>. 80% would be 0.8."),
        ("0.65", "65%", ["6.5%", "650%", "0.65%"],
         "0.65 × 100 = 65, so 0.65 = <b>65%</b>. Multiplying by 100 moves the digits 2 places to the left."),
        ("0.125", "12.5%", ["125%", "1.25%", "0.125%"],
         "0.125 × 100 = 12.5, so 0.125 = <b>12.5%</b>. 125% would be 1.25."),
        ("1.5", "150%", ["15%", "1.5%", "50%"],
         "1.5 × 100 = 150, so 1.5 = <b>150%</b>. A number greater than 1 is more than 100%."),
        ("2", "200%", ["2%", "20%", "0.2%"],
         "2 wholes = 2 × 100% = <b>200%</b>. 2% would be 0.02."),
        ("0.005", "0.5%", ["5%", "50%", "0.05%"],
         "0.005 × 100 = 0.5, so 0.005 = <b>0.5%</b>, less than 1%. 5% would be 0.05."),
        ("0.025", "2.5%", ["25%", "0.25%", "0.025%"],
         "0.025 × 100 = 2.5, so 0.025 = <b>2.5%</b>. 25% would be 0.25."),
    ]:
        assert D(d_) * 100 == D(right.rstrip("%"))
        its.append(mcq("Write <b>%s</b> as a percent." % d_, right, wrong, e))
    its.append(mcq("Write <b>0.%s</b> (0.333…) as a percent." % bar("3"), "33.3…%", ["3.3%", "0.33%", "333%"],
                   "Multiply by 100: 0.333… × 100 = 33.333… So 0.%s = <b>33.3…%%</b>, which is %s%%. "
                   "The 3s after the point keep going." % (bar("3"), mixed(33, 1, 3))))
    for p_, right, wrong, e in [
        ("35%", "0.35", ["3.5", "0.035", "35"],
         "Divide by 100: 35 ÷ 100 = <b>0.35</b>. The digits move 2 places to the right."),
        ("4%", "0.04", ["0.4", "4", "0.004"],
         "4% = 4 hundredths. Hundredths are the second place after the point: <b>0.04</b>. 0.4 is 40%."),
        ("70%", "0.7", ["0.07", "7", "0.007"],
         "70% = 70 hundredths = 7 tenths = <b>0.7</b>. 0.07 is only 7%."),
        ("120%", "1.2", ["0.12", "12", "0.012"],
         "120 ÷ 100 = <b>1.2</b>. More than 100% is more than 1 whole. 0.12 would be 12%."),
        ("7.5%", "0.075", ["0.75", "7.5", "0.0075"],
         "7.5 ÷ 100 = <b>0.075</b>. 0.75 would be 75%."),
        ("0.2%", "0.002", ["0.2", "0.02", "2"],
         "0.2 ÷ 100 = <b>0.002</b>. 0.2% is less than 1%, so the decimal is less than 0.01. 0.2 would be 20%."),
        ("250%", "2.5", ["0.25", "25", "0.025"],
         "250 ÷ 100 = <b>2.5</b>. 250% means 2 and a half wholes. 0.25 would be 25%."),
    ]:
        assert D(p_.rstrip("%")) / 100 == D(right)
        its.append(mcq("Write <b>%s</b> as a decimal." % p_, right, wrong, e))
    its.append(mcq(fig(grids_svg([100, 45])) + "Each hundred grid is one whole. What percent is shaded?",
                   "145%", ["45%", "14.5%", "1.45%"],
                   "One full grid is 100%, and the second grid has 45%. 100% + 45% = <b>145%</b> = 1.45. "
                   "45% forgets the full grid."))
    its.append(mcq("Which of these is <b>not</b> equal to 0.6?", "6%", ["60%", "0.60", fr(3, 5)],
                   "0.6 = 0.60 = %s = 60%%. <b>6%%</b> is 0.06, only one tenth as much." % fr(3, 5), same_ok=True))
    its.append(mcq("Which is the <b>greatest</b>?", "0.5", ["45%", "0.05", "5.5%"],
                   "As decimals: 0.5 = 0.500, 45% = 0.450, 0.050 and 5.5% = 0.055. The greatest is <b>0.5</b>."))
    # easy -> hard
    order = [0, 1, 2, 10, 11, 12, 3, 18, 4, 14, 5, 6, 13, 16, 17, 7, 8, 15, 19, 9]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    return {"title": "Decimals and percents, including 12.5%, 0.5% and over 100%", "items": its}


# ============================================================ set 3: fractions and percents
def set_fraction_percent():
    its = []

    def f2p(v, right, wrong, e, q=None, fg=""):
        assert D(right.rstrip("%")) / 100 == F(v), (v, right)
        its.append(mcq(fg + (q or "Write %s as a percent." % fr(F(v).numerator, F(v).denominator)), right, wrong, e))

    f2p(F(3, 4), "75%", ["34%", "43%", "25%"],                                           # 0
        "%s = %s (multiply the top and bottom by 25) = <b>75%%</b>. 34%% just writes the digits, "
        "and 25%% is the part that is left." % (fr(3, 4), fr(75, 100)))
    f2p(F(7, 10), "70%", ["7%", "0.7%", "30%"],                                          # 1
        "%s = %s = <b>70%%</b>. 7%% would be %s." % (fr(7, 10), fr(70, 100), fr(7, 100)))
    f2p(F(2, 5), "40%", ["20%", "2.5%", "60%"],                                          # 2
        "The bar has 5 equal parts, so each part is 100% ÷ 5 = 20%. 2 parts are shaded: 2 × 20% = <b>40%</b>. "
        "20% counts only one part, and 60% is the white part.",
        q="What percent of the bar is shaded?", fg=fig(bar_svg(5, 2)))
    f2p(F(9, 20), "45%", ["9%", "20%", "55%"],                                           # 3
        "20 × 5 = 100, so %s = %s = <b>45%%</b>. 55%% is the part that is left." % (fr(9, 20), fr(45, 100)))
    f2p(F(13, 25), "52%", ["13%", "38%", "48%"],                                         # 4
        "25 × 4 = 100, so %s = %s = <b>52%%</b>. 38%% adds 13 + 25, and 48%% is the part that is left."
        % (fr(13, 25), fr(52, 100)))

    def p2f(p_, right, wrong, e, v):
        assert D(p_.rstrip("%")) / 100 == v
        its.append(mcq("Write <b>%s</b> as a fraction in simplest form." % p_, right, wrong, e, value=v))

    p2f("60%", fr(3, 5), [fr(1, 6), fr(6, 100), fr(2, 5)],                              # 5
        "60%% = %s. Divide the top and bottom by 20: <b>%s</b>. %s would be 6%%, and %s is 40%%."
        % (fr(60, 100), fr(3, 5), fr(6, 100), fr(2, 5)), F(3, 5))
    p2f("85%", fr(17, 20), [fr(85, 10), fr(8, 5), fr(3, 20)],                           # 6
        "85%% = %s. Divide the top and bottom by 5: <b>%s</b>. %s is the 15%% that is left."
        % (fr(85, 100), fr(17, 20), fr(3, 20)), F(17, 20))
    p2f("35%", fr(7, 20), [fr(35, 10), fr(3, 5), fr(13, 20)],                           # 7
        "35%% = %s. Divide the top and bottom by 5: <b>%s</b>. %s just uses the digits 3 and 5."
        % (fr(35, 100), fr(7, 20), fr(3, 5)), F(7, 20))
    p2f("2%", fr(1, 50), [fr(1, 2), fr(1, 5), fr(1, 20)],                               # 8
        "2%% = %s. Divide the top and bottom by 2: <b>%s</b>. %s is 50%%, %s is 20%% and %s is 5%%."
        % (fr(2, 100), fr(1, 50), fr(1, 2), fr(1, 5), fr(1, 20)), F(1, 50))
    p2f("4%", fr(1, 25), [fr(1, 4), fr(2, 5), fr(1, 40)],                               # 9
        "4%% = %s. Divide the top and bottom by 4: <b>%s</b>. %s is 25%%, not 4%%." % (fr(4, 100), fr(1, 25), fr(1, 4)),
        F(1, 25))
    f2p(F(27, 50), "54%", ["27%", "23%", "46%"],                                         # 10
        "50 × 2 = 100, so %s = %s = <b>54%%</b>. 27%% forgets to multiply the top by 2, and 23%% is 50 − 27."
        % (fr(27, 50), fr(54, 100)))
    its.append(mcq("Which of these is <b>not</b> equal to %s?" % fr(3, 4), "34%", ["75%", "0.75", fr(9, 12)],    # 11
                   "%s = %s = 0.75 = 75%%. <b>34%%</b> only writes the digits of the fraction." % (fr(3, 4), fr(9, 12)),
                   same_ok=True))
    f2p(F(5, 2), "250%", ["52%", "25%", "2.5%"],                                         # 12
        "%s = 5 ÷ 2 = 2.5 wholes. 2.5 × 100 = <b>250%%</b>. A fraction greater than 1 is more than 100%%." % fr(5, 2))
    p2f("150%", mixed(1, 1, 2), [mixed(1, 1, 5), fr(3, 20), fr(1, 150)],               # 13
        "150%% = %s = %s. Simplify %s = %s: <b>%s</b>. %s would be 15%%."
        % (fr(150, 100), mixed(1, 50, 100), fr(50, 100), fr(1, 2), mixed(1, 1, 2), fr(3, 20)), F(3, 2))
    f2p(F(5, 4), "125%", ["114%", "25%", "12.5%"],                                       # 14
        "%s = 1 + %s = 100%% + 25%% = <b>125%%</b>. 114%% writes the digits 1, 1 and 4."
        % (mixed(1, 1, 4), fr(1, 4)), q="Write %s as a percent." % mixed(1, 1, 4))
    f2p(F(3, 8), "37.5%", ["3.8%", "30%", "62.5%"],                                      # 15
        "Each eighth is 100% ÷ 8 = 12.5%. 3 eighths: 3 × 12.5% = <b>37.5%</b> (3 ÷ 8 = 0.375). "
        "30% counts each part as 10%, but there are 8 parts, not 10. 62.5% is the white part.",
        q="What percent of the bar is shaded?", fg=fig(bar_svg(8, 3)))
    f2p(F(7, 8), "87.5%", ["78%", "8.75%", "12.5%"],                                     # 16
        "7 ÷ 8 = 0.875 = <b>87.5%%</b>. Or 7 × 12.5%% = 87.5%%. 12.5%% is the one eighth that is left." % ())
    p2f("12.5%", fr(1, 8), [fr(125, 100), fr(1, 12), fr(1, 80)],                       # 17
        "12.5%% = 0.125 = %s. Divide the top and bottom by 125: <b>%s</b>. %s would be 125%%."
        % (fr(125, 1000), fr(1, 8), fr(125, 100)), F(1, 8))
    f2p(F(1, 200), "0.5%", ["2%", "5%", "50%"],                                          # 18
        "200 ÷ 2 = 100, so %s = %s = <b>0.5%%</b>, half of 1%%. 5%% would be %s." % (fr(1, 200), fr("0.5", 100), fr(1, 20)))
    its.append(mcq("Write %s as a percent." % fr(1, 3), "33.3…%", ["3%", "13%", "30%"],                         # 19
                   "1 ÷ 3 = 0.333…, and 0.333… × 100 = 33.333… So %s = <b>33.3…%%</b> = %s%%. "
                   "30%% would be %s, and 13%% just writes the digits." % (fr(1, 3), mixed(33, 1, 3), fr(3, 10))))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 13, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    return {"title": "Fractions and percents", "items": its}


# ============================================================ set 4: common equivalents
def set_benchmarks():
    its = []
    its.append(mcq("Complete: %s = 0.5 = ?" % fr(1, 2), "50%", ["5%", "0.5%", "12%"],
                   "0.5 × 100 = 50, so %s = 0.5 = <b>50%%</b>. 12%% just writes the digits of the fraction." % fr(1, 2)))
    its.append(mcq("Complete: %s = 0.25 = ?" % fr(1, 4), "25%", ["2.5%", "14%", "40%"],
                   "0.25 = 25 hundredths = <b>25%%</b>. 40%% uses the 4 in %s as tenths." % fr(1, 4)))
    its.append(mcq("Complete: %s = ? = 20%%" % fr(1, 5), "0.2", ["0.5", "0.15", "0.02"],
                   "20%% = 20 hundredths = <b>0.2</b>, and %s = %s = 0.2. 0.02 is only 2%%." % (fr(1, 5), fr(2, 10))))
    its.append(mcq("Complete: %s = 0.1 = ?" % fr(1, 10), "10%", ["1%", "0.1%", "100%"],
                   "0.1 = 10 hundredths = <b>10%%</b>. 1%% would be %s." % fr(1, 100)))
    its.append(mcq("%s = 0.125. Use this to write %s as a decimal." % (fr(1, 8), fr(3, 8)), "0.375",
                   ["0.38", "0.0375", "3.125"],
                   "%s is 3 eighths: 3 × 0.125 = <b>0.375</b>. 3.125 adds 3 + 0.125 instead of multiplying."
                   % fr(3, 8), value=F(3, 8)))
    its.append(mcq("%s = 12.5%%. Use this to write %s as a percent." % (fr(1, 8), fr(5, 8)), "62.5%",
                   ["58%", "17.5%", "37.5%"],
                   "%s is 5 eighths: 5 × 12.5%% = <b>62.5%%</b>. 17.5%% adds 12.5 + 5, and 37.5%% is the 3 eighths that are left."
                   % fr(5, 8), value=F(5, 8)))
    its.append(mcq("%s = 0.05. Use this to write %s as a decimal." % (fr(1, 20), fr(3, 20)), "0.15",
                   ["0.32", "0.015", "0.6"],
                   "3 × 0.05 = <b>0.15</b>. 0.6 uses 3 × 0.2, which is %s, not %s." % (fr(3, 5), fr(3, 20)), value=F(3, 20)))
    its.append(mcq("%s = 4%%. Use this to write %s as a percent." % (fr(1, 25), fr(7, 25)), "28%",
                   ["7%", "32%", "18%"],
                   "7 × 4%% = <b>28%%</b>. 32%% adds 7 + 25, and 18%% is 25 − 7." % (), value=F(7, 25)))
    its.append(mcq("%s = 33.3…%%. What is %s as a percent?" % (fr(1, 3), fr(2, 3)), "66.6…%",
                   ["23%", "33.3…%", "60%"],
                   "%s is twice %s: 2 × 33.3…%% = <b>66.6…%%</b> = %s%%. 60%% would be %s."
                   % (fr(2, 3), fr(1, 3), mixed(66, 2, 3), fr(3, 5)), same_ok=True))
    k = 5
    its.append(mcq(fig(dline_svg(8, k, {0: "0", 8: "1"}, {0: "0%", 8: "100%"})) +
                   "The double number line is split into 8 equal parts. What percent is at the red dot?",
                   "62.5%", ["50%", "58%", "80%"],
                   "Each part is %s = 12.5%%. The dot is 5 parts along: 5 × 12.5%% = <b>62.5%%</b>. "
                   "50%% counts each part as 10%%, and 80%% is 8 tenths." % fr(1, 8), value=F(k, 8)))
    its.append(mcq(fig(dline_svg(5, 3, {0: "0", 5: "1"}, {0: "0%", 5: "100%"})) +
                   "The double number line is split into 5 equal parts. What fraction and percent are at the red dot?",
                   "%s and 60%%" % fr(3, 5), ["%s and 30%%" % fr(3, 5), "%s and 35%%" % fr(3, 5), "%s and 3%%" % fr(3, 5)],
                   "Each part is %s = 20%%. The dot is 3 parts along: <b>%s and 60%%</b>. "
                   "30%% counts each part as 10%%, and 35%% just writes the digits." % (fr(1, 5), fr(3, 5)), same_ok=True))
    its.append(mcq("Which of these is <b>not</b> equal to %s?" % fr(1, 8), "0.8", ["0.125", "12.5%", fr(2, 16)],
                   "%s = 1 ÷ 8 = 0.125 = 12.5%% = %s. <b>0.8</b> uses the denominator as the decimal; 0.8 is %s."
                   % (fr(1, 8), fr(2, 16), fr(4, 5)), same_ok=True))
    its.append(mcq("Which row shows the <b>same</b> number three ways?",
                   "%s, 0.75, 75%%" % fr(3, 4),
                   ["%s, 0.34, 34%%" % fr(3, 4), "%s, 0.4, 40%%" % fr(1, 4), "%s, 0.35, 35%%" % fr(3, 5)],
                   "%s = 0.75 = 75%%. The other rows write the digits of the fraction, or use the denominator as tenths. "
                   "<b>%s, 0.75, 75%%</b> is right." % (fr(3, 4), fr(3, 4)), same_ok=True))
    its.append(mcq("Which is closest to %s?" % fr(1, 3), "33%", ["0.3", "3%", "0.13"],
                   "%s = 0.333… 33%% = 0.33 is only 0.003… away. 0.3 is 0.033… away, so <b>33%%</b> is closest." % fr(1, 3)))
    assert F(5, 6) * 100 == F(250, 3) and abs(F(5, 6) * 100 - D("83.3")) < F(1, 20)
    its.append(mcq("%s = 16.7%% to the nearest tenth of a percent. What is %s to the nearest tenth of a percent?"
                   % (fr(1, 6), fr(5, 6)), "83.3%", ["56%", "16.7%", "85%"],
                   "%s = 5 ÷ 6 = 0.8333… = 83.333…%% ≈ <b>83.3%%</b>. Or 100%% − 16.7%% = 83.3%%. "
                   "16.7%% is the sixth that is left." % fr(5, 6)))
    its.append(mcq("Order from <b>least to greatest</b>:<br><b>%s, 0.2, 15%%</b>" % fr(1, 8),
                   "%s, 15%%, 0.2" % fr(1, 8), ["0.2, %s, 15%%" % fr(1, 8), "15%%, 0.2, %s" % fr(1, 8),
                                               "0.2, 15%%, %s" % fr(1, 8)],
                   "Use decimals: %s = 0.125, 15%% = 0.150, 0.2 = 0.200. So <b>%s, 15%%, 0.2</b>. "
                   "%s is not 0.8." % (fr(1, 8), fr(1, 8), fr(1, 8)), same_ok=True))
    its.append(mcq("Which is the <b>greatest</b>?", "0.4", [fr(3, 8), "35%", "0.385"],
                   "As decimals: 0.400, %s = 0.375, 35%% = 0.350 and 0.385. The greatest is <b>0.4</b>." % fr(3, 8)))
    its.append(mcq("Which fraction is equal to 0.%s (0.666…)?" % bar("6"), fr(2, 3), [fr(6, 10), fr(66, 100), fr(3, 2)],
                   "2 ÷ 3 = 0.666…, so 0.%s = <b>%s</b>. %s and %s stop, so they are a little less."
                   % (bar("6"), fr(2, 3), fr(6, 10), fr(66, 100)), value=F(2, 3)))
    its.append(mcq("Write <b>%s0.125</b> as a fraction in simplest form." % MINUS, nfr(1, 8),
                   [fr(1, 8), nfr(1, 12), nfr(1, 80)],
                   "0.125 = %s, a common equivalent. Keep the sign: <b>%s</b>. %s is positive, and %s would be %s0.0125."
                   % (fr(1, 8), nfr(1, 8), fr(1, 8), nfr(1, 80), MINUS), value=F(-1, 8)))
    its.append(mcq("Which shows 2.5 as a mixed number and as a percent?", "%s and 250%%" % mixed(2, 1, 2),
                   ["%s and 25%%" % mixed(2, 1, 5), "%s and 25%%" % mixed(2, 1, 2), "%s and 2.5%%" % fr(5, 2)],
                   "2.5 = 2 and 5 tenths = %s. 2.5 × 100 = 250%%. So <b>%s and 250%%</b>. 25%% would be 0.25."
                   % (mixed(2, 1, 2), mixed(2, 1, 2)), same_ok=True))
    order = [0, 1, 2, 3, 12, 4, 5, 6, 7, 10, 11, 9, 13, 8, 17, 14, 15, 16, 18, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    return {"title": "Common equivalents: 1/8 = 0.125 = 12.5%", "items": its}


# ============================================================ set 5: increase and decrease, word problems
def set_problems(P):
    its = []

    def pc(n, p):
        return F(n) * F(p, 100)

    assert pc(340, 10) == 34
    its.append(mcq("Find <b>10%%</b> of %s mentally." % num(340), "34", ["3.4", "30", "330"],
                   "10%% is %s. Divide by 10: 340 ÷ 10 = <b>34</b>. 330 subtracts 10 instead of finding 10%%." % fr(1, 10)))
    assert pc(4500, 1) == 45
    its.append(mcq("Find <b>1%%</b> of %s mentally." % num(4500), "45", ["450", "4.5", "4499"],
                   "1%% is %s. Divide by 100: 4500 ÷ 100 = <b>45</b>. 450 is 10%%." % fr(1, 100)))
    assert pc(260, 5) == 13
    its.append(mcq("Find <b>5%</b> of 260 mentally.", "13", ["26", "52", "130"],
                   "10% of 260 is 26. 5% is half of 10%: 26 ÷ 2 = <b>13</b>. 52 is 260 ÷ 5, which is 20%, and 130 is 50%."))
    assert pc(84, 25) == 21
    its.append(mcq("Find <b>25%</b> of 84 mentally.", "21", ["42", "59", "8.4"],
                   "25%% = %s. Divide by 4: 84 ÷ 4 = <b>21</b>. 42 is 50%%, and 59 is 84 − 25." % fr(1, 4)))
    assert 60 + pc(60, 50) == 90
    its.append(mcq("Increase 60 by <b>50%</b>.", "90", ["30", "110", "120"],
                   "50% of 60 is half of 60 = 30. Add it on: 60 + 30 = <b>90</b>. 110 adds 50, and 120 is an increase of 100%."))
    assert 45 + pc(45, 100) == 90
    its.append(mcq("Increase 45 by <b>100%</b>.", "90", ["145", "45", "55"],
                   "100% of 45 is all of 45. 45 + 45 = <b>90</b>, so a 100% increase doubles the number. 145 adds 100."))
    assert 80 - pc(80, 25) == 60
    its.append(mcq("Decrease 80 by <b>25%</b>.", "60", ["55", "20", "100"],
                   "25%% of 80 = 80 ÷ 4 = 20. Take it away: 80 − 20 = <b>60</b>. 55 subtracts 25, "
                   "and 20 is only the amount taken off." % ()))
    assert 400 - pc(400, 1) == 396
    its.append(mcq("Decrease 400 by <b>1%</b>.", "396", ["399", "300", "4"],
                   "1% of 400 = 400 ÷ 100 = 4. Take it away: 400 − 4 = <b>396</b>. 399 subtracts 1, not 1%."))
    assert 120 + pc(120, 5) == 126
    its.append(mcq("Increase 120 by <b>5%</b>.", "126", ["125", "132", "6"],
                   "10% of 120 is 12, so 5% is 6. 120 + 6 = <b>126</b>. 125 adds 5, and 132 is an increase of 10%."))
    assert 24000 + pc(24000, 10) == 26400
    its.append(mcq("Increase %s by <b>10%%</b>." % num(24000), num(26400), [num(24010), num(2400), num(21600)],
                   "10%% of %s = %s. %s + %s = <b>%s</b>. %s is a decrease of 10%%."
                   % (num(24000), num(2400), num(24000), num(2400), num(26400), num(21600))))
    # word problems
    n, he, his = P.next()
    assert 80 - pc(80, 25) == 60
    its.append(mcq(fig(pbar_svg(80, 4, 1, "off")) +
                   "A hockey stick costs $80. It is on sale for <b>25% off</b>. What is the sale price?",
                   "$60", ["$55", "$20", "$100"],
                   "25%% = %s, so split $80 into 4 equal parts of $20. Take 1 part off: $80 − $20 = <b>$60</b>. "
                   "$20 is the discount, not the price, and $55 subtracts 25." % fr(1, 4), value=60))
    assert 120 - pc(120, 15) == 102
    its.append(mcq("A winter jacket costs $120. It is <b>15% off</b>. Find 10% and 5% to work out the sale price.",
                   "$102", ["$105", "$18", "$138"],
                   "10% of $120 = $12, and 5% = $6. 15% = $12 + $6 = $18. $120 − $18 = <b>$102</b>. "
                   "$105 subtracts 15, and $138 adds the discount.", value=102))
    assert 18000 + pc(18000, 5) == 18900
    its.append(mcq("A town in Ontario has %s people. The population grows by <b>5%%</b>. What is the new population?"
                   % num(18000), num(18900), [num(18005), num(900), num(19800)],
                   "10%% of %s = %s, so 5%% = 900. %s + 900 = <b>%s</b>. %s is an increase of 10%%."
                   % (num(18000), num(1800), num(18000), num(18900), num(19800))))
    assert 500 + pc(500, 50) == 750
    its.append(mcq(fig(pbar_svg(500, 2, 1, "more", fmt=lambda v: "%d g" % v)) +
                   "A 500 g bag of trail mix now has <b>50% more</b> for free. How much is in the new bag?",
                   "750 g", ["550 g", "250 g", "1000 g"],
                   "50%% of 500 g is half of 500 g = 250 g. 500 + 250 = <b>750 g</b>. 550 g adds 50, and 1000 g "
                   "would be 100%% more." % ()))
    n, he, his = P.next()
    assert pc(640, 25) == 160
    its.append(mcq("A school has 640 students. <b>25%</b> of them take the bus. How many students take the bus?",
                   "160", ["25", "615", "480"],
                   "25%% = %s. 640 ÷ 4 = <b>160</b> students. 480 is the 75%% who do not take the bus." % fr(1, 4)))
    assert pc(64, 15) == F("9.6")
    n, he, his = P.next()
    its.append(mcq("%s’s family has dinner at a restaurant. The bill is $64. They leave a <b>15%%</b> tip. How much is the tip?"
                   % n, "$9.60", ["$6.40", "$3.20", "$73.60"],
                   "10%% of $64 = $6.40, and 5%% is half of that = $3.20. 15%% = $6.40 + $3.20 = <b>$9.60</b>. "
                   "$73.60 is the bill plus the tip, not the tip." % (), value=F("9.6")))
    assert 45 + pc(45, 10) == F("49.5")
    its.append(mcq("A canoe rental costs $45 a day. Next summer the price goes up by <b>10%</b>. What will the new price be?",
                   "$49.50", ["$55", "$4.50", "$45.10"],
                   "10% of $45 = $4.50. $45 + $4.50 = <b>$49.50</b>. $55 adds $10, and $4.50 is only the increase.",
                   value=F("99/2")))
    n, he, his = P.next()
    assert F(21, 25) == F(84, 100)
    its.append(mcq("%s answers 21 of 25 questions correctly on a math test. What is %s score as a percent?" % (n, his),
                   "84%", ["21%", "4%", "16%"],
                   "%s = %s (multiply the top and bottom by 4) = <b>84%%</b>. 16%% is the part %s got wrong."
                   % (fr(21, 25), fr(84, 100), he)))
    assert 160 - pc(160, 25) == 120
    its.append(mcq("Last winter, 160 cm of snow fell in Ottawa. This winter there was <b>25% less</b> snow. "
                   "How much snow fell this winter?", "120 cm", ["135 cm", "40 cm", "200 cm"],
                   "25% of 160 cm = 160 ÷ 4 = 40 cm. 160 − 40 = <b>120 cm</b>. 135 cm subtracts 25, "
                   "and 200 cm is 25% <b>more</b>."))
    up = 40 + pc(40, 50)
    down = up - pc(up, 50)
    assert (up, down) == (60, 30)
    its.append(mcq("A store raises the price of a $40 sweater by <b>50%</b>. Later it puts the sweater on sale for "
                   "<b>50% off</b> the new price. What is the sale price?", "$30", ["$40", "$20", "$60"],
                   "50% of $40 = $20, so the new price is $60. 50% of $60 = $30, so the sale price is $60 − $30 = <b>$30</b>. "
                   "It is not $40: the 50% off is taken from $60, a bigger number.", value=30))
    assert len(its) == 20, len(its)
    return {"title": "Increase and decrease by a percent: mental math and word problems", "items": its}


# ============================================================ lesson
def body_html():
    f_div = sdiv(1, 3, 4, repeat=True)
    f_line = dline_svg(8, None, {i: (i, 8) if 0 < i < 8 else str(i // 8) for i in range(9)},
                       {i: pct(F(i, 8)) for i in range(9)}, W=560)
    f_bar = pbar_svg(80, 4, 1, "off")
    return (
        "<h2>Fractions and decimals</h2>"
        "<p>A fraction is a division: " + fr(3, 8) + " means 3 ÷ 8 = 0.375. If the denominator goes into 10, 100 "
        "or 1000, you can make an equivalent fraction instead: " + fr(7, 20) + " = " + fr(35, 100) + " = 0.35.</p>"
        "<p>Some divisions never end. The remainder keeps coming back, so the digits repeat. "
        "Write the repeating digits with a bar: 0.333… = 0." + bar("3") + ".</p>"
        "<figure class='sn-fig'>" + f_div +
        "<figcaption>1 ÷ 3: the remainder is always 1, so " + fr(1, 3) + " = 0.333… = 0." + bar("3") + "</figcaption></figure>"
        + ex("Decimal to fraction", "Write 0.45 as a fraction in simplest form.",
             "0.45 = 45 hundredths = " + fr(45, 100) + ". Divide the top and bottom by 5.", fr(9, 20))
        + ex("Negative numbers", "Write " + nfr(3, 4) + " as a decimal.",
             fr(3, 4) + " = 0.75. Keep the negative sign.", MINUS + "0.75")
        + "<h2>Decimals and percents</h2>"
        "<p>Percent means <b>out of 100</b>. Decimal to percent: multiply by 100. Percent to decimal: divide by 100. "
        "0.4 = 40%, 0.125 = 12.5%, 1.5 = 150%, 0.005 = 0.5%.</p>"
        + ex("Fraction to percent", "Write " + fr(13, 25) + " as a percent.",
             "25 × 4 = 100, so " + fr(13, 25) + " = " + fr(52, 100) + ".", "52%")
        + "<h2>Common equivalents</h2>"
        "<p>Know these by heart. They make many questions quick: " + fr(3, 8) + " is 3 × 12.5% = 37.5%.</p>"
        "<figure class='sn-fig'>" + f_line +
        "<figcaption>Each eighth is 0.125 = 12.5%.</figcaption></figure>"
        + table(["Fraction", "Decimal", "Percent"], [
            [fr(1, 2), "0.5", "50%"],
            [fr(1, 4), "0.25", "25%"],
            [fr(3, 4), "0.75", "75%"],
            [fr(1, 5), "0.2", "20%"],
            [fr(1, 10), "0.1", "10%"],
            [fr(1, 20), "0.05", "5%"],
            [fr(1, 8), "0.125", "12.5%"],
            [fr(1, 3), "0.333…", "33.3…%"],
            [fr(2, 3), "0.666…", "66.6…%"],
        ])
        + "<h2>Increase or decrease by a percent in your head</h2>"
        "<p>Find the percent of the number, then add it (increase) or subtract it (decrease).</p>"
        + table(["Percent", "Mental math", "Example with 240"], [
            ["100%", "the whole number", "240"],
            ["50%", "÷ 2", "120"],
            ["25%", "÷ 4", "60"],
            ["10%", "÷ 10", "24"],
            ["5%", "half of 10%", "12"],
            ["1%", "÷ 100", "2.4"],
        ])
        + "<figure class='sn-fig'>" + f_bar +
        "<figcaption>25% off $80: 4 equal parts of $20. Take 1 part off: $60.</figcaption></figure>"
        + ex("Increase", "Increase 120 by 5%.", "10% of 120 = 12, so 5% = 6. 120 + 6 = 126.", "126")
        + ex("Decrease", "A $120 jacket is 15% off.", "10% = $12 and 5% = $6, so 15% = $18. $120 − $18 = $102.", "$102")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["0.4 = 4%", "0.4 = 0.40 = 40 hundredths = 40%"],
            [fr(1, 8) + " = 0.8", "Divide: 1 ÷ 8 = 0.125 = 12.5%"],
            [fr(1, 3) + " = 0.3", "1 ÷ 3 = 0.333…; 0.3 is only " + fr(3, 10)],
            ["150% = 0.15", "150 ÷ 100 = 1.5. More than 100% is more than 1."],
            ["Decrease 80 by 25%: 80 − 25 = 55", "Find 25% first: 80 ÷ 4 = 20. 80 − 20 = 60"],
            ["+50% then −50% gets back to the start", "The second 50% is of a different number: $40 → $60 → $30"],
        ])
    )


FAQ = [
    {"q": "What do Grade 7 students learn about fractions, decimals and percents in Ontario?",
     "a": "In the Ontario Grade 7 math curriculum, students convert between fractions, decimals and percents in different contexts, use common equivalents such as 1/8 = 0.125 = 12.5%, and use mental math to increase or decrease a number by 1%, 5%, 10%, 25%, 50% and 100%."},
    {"q": "How do you change a fraction to a percent?",
     "a": "Divide the numerator by the denominator, then multiply by 100: 3/8 = 3 ÷ 8 = 0.375 = 37.5%. If the denominator goes into 100, make an equivalent fraction instead: 13/25 = 52/100 = 52%."},
    {"q": "What is a repeating decimal?",
     "a": "It is a decimal whose digits repeat forever because the division never ends, such as 1/3 = 0.333…. It is written with a bar over the digits that repeat."},
    {"q": "How do you increase or decrease a number by a percent in your head?",
     "a": "Find the percent first (10% is ÷ 10, 5% is half of 10%, 25% is ÷ 4, 1% is ÷ 100), then add it or subtract it. For example, $80 decreased by 25% is $80 − $20 = $60."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (hundred grids, number lines, bars, short division)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(47804)
    P = People(rnd)
    sets = [set_fraction_decimal(), set_decimal_percent(), set_fraction_percent(), set_benchmarks(), set_problems(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-7", "slug": "fractions-decimals-and-percents", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Fractions, Decimals and Percents",
        "seo_title": "Grade 7 Fractions, Decimals and Percents Worksheets (Ontario Math): Free with Answer Key",
        "short_title": "Fractions, decimals and percents",
        "domain": "Number",
        "standard_code": "Grade 7: B1.7",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Convert between fractions, decimal numbers, and percents, in various contexts",
        "meta_desc": "Free Grade 7 fractions, decimals and percents worksheets for the Ontario curriculum: repeating decimals like 1/3 = 0.333…, negative fractions, percents over 100%, common equivalents such as 1/8 = 0.125 = 12.5%, and mental math to increase or decrease by a percent. 100 math questions with an answer key.",
        "key_big": "Fraction to decimal: divide (3/8 = 3 ÷ 8 = 0.375). Decimal to percent: multiply by 100 (0.375 = 37.5%).",
        "key_sub": "Know the common equivalents: 1/2 = 50%, 1/4 = 25%, 1/5 = 20%, 1/8 = 12.5%, 1/3 = 33.3…%. To change a number by a percent, find the percent first, then add or subtract it.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(hundred grid|[0-9]+ hundred grids|double number line|fraction bar|short division|bar model)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
