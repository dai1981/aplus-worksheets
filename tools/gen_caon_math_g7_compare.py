# -*- coding: utf-8 -*-
"""
CA Grade 7 Math: Comparing Fractions and Decimals (Ontario Mathematics Curriculum 2020, Grade 7: B1.3, B1.4, B1.5, B1.6)
  python3 tools/gen_caon_math_g7_compare.py
Positive and negative fractions and decimals to thousandths on horizontal and vertical number lines, comparing and
ordering them, simplifying fractions, finding a number between any two quantities, and rounding decimals to the
nearest tenth, hundredth or whole number, with word problems about temperatures, elevations, lake levels and money.
Wrong answers come from real student mistakes: −0.5 > −0.25 because 5 > 25 is ignored for the sign, 0.45 > 0.5
because it has more digits, dropping the minus sign, counting tick marks instead of spaces, counting from the wrong
label, dividing only the numerator, flipping a fraction, rounding twice, cutting off digits instead of rounding.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English. Real minus sign −.
"""
import json, os, random, re
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-7")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
BLUE = "#1f5fa8"
INK = "#2b2b2b"
GRAY = "#8a8f8c"
FONT = "Arial, Helvetica, sans-serif"
M = "−"
NB = " "


# ------------------------------------------------------------ numbers
# A number is written in the source as an ASCII token: "-0.25", "3/4", "-1 2/3", "10.0".
def V(s):
    """Value of a token."""
    s = s.strip()
    neg = s.startswith("-")
    t = s.lstrip("-")
    if " " in t:
        w, fr_ = t.split(" ")
        a, b = fr_.split("/")
        v = int(w) + F(int(a), int(b))
    elif "/" in t:
        a, b = t.split("/")
        v = F(int(a), int(b))
    else:
        v = F(t)
    return -v if neg else v


def frh(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def H(s):
    """HTML for a token: real minus sign, stacked fractions."""
    s = s.strip()
    neg = s.startswith("-")
    t = s.lstrip("-")
    if " " in t:
        w, fr_ = t.split(" ")
        a, b = fr_.split("/")
        body = w + NB + frh(a, b)
    elif "/" in t:
        a, b = t.split("/")
        body = frh(a, b)
    else:
        body = t
    return (M if neg else "") + body


def P(s):
    """Plain text for a token (aria labels, FAQ)."""
    return s.strip().replace("-", M)


def dtok(v):
    """Fraction with a terminating decimal -> token without trailing zeros."""
    v = F(v)
    d = Decimal(v.numerator) / Decimal(v.denominator)
    t = format(d.normalize(), "f")
    assert F(t) == v, v
    return t


def lbl(v):
    """Label on a number line: integer or decimal, real minus sign."""
    return P(dtok(v))


def ftok(v):
    """Fraction -> token (mixed number when larger than 1)."""
    v = F(v)
    s = "-" if v < 0 else ""
    a = abs(v)
    w, r = divmod(a.numerator, a.denominator)
    if r == 0:
        return s + str(w)
    if w == 0:
        return "%s%d/%d" % (s, r, a.denominator)
    return "%s%d %d/%d" % (s, w, r, a.denominator)


def deg(s):
    return H(s) + NB + "°C"


def m_(s):
    return H(s) + NB + "m"


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ question helpers
def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def mcq_num(q, c, wrongs, e, unit=""):
    """c and wrongs: tokens. Takes the first 3 wrong tokens whose values differ from the answer and each other."""
    vals, pick = {V(c)}, []
    for w in wrongs:
        if V(w) in vals:
            continue
        vals.add(V(w))
        pick.append(w)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, c, wrongs)
    ch = [H(c) + unit] + [H(w) + unit for w in pick]
    assert len({plain(x) for x in ch}) == 4, ch
    return {"q": q, "c": ch, "a": 0, "e": e}


def mcq_txt(q, c, wrongs, e):
    assert len(wrongs) == 3, (q, wrongs)
    ch = [c] + list(wrongs)
    assert len({plain(x) for x in ch}) == 4, ch
    return {"q": q, "c": ch, "a": 0, "e": e}


def mcq_fixed(q, choices, correct, e):
    """Choices keep their order (A B C D)."""
    assert len(set(choices)) == 4 and correct in choices, (q, choices)
    return {"q": q, "c": list(choices), "a": choices.index(correct), "e": e, "fixed": True}


OPS = {"<": (lambda a, b: a < b, "&lt;"), ">": (lambda a, b: a > b, "&gt;"), "=": (lambda a, b: a == b, "=")}


def st(a, op, b):
    """(statement HTML, is it true)."""
    f, sym = OPS[op]
    return "%s %s %s" % (H(a), sym, H(b)), f(V(a), V(b))


def mcq_stmt(q, true_st, false_sts, e):
    assert true_st[1], true_st
    for s in false_sts:
        assert not s[1], s
    return mcq_txt(q, true_st[0], [s[0] for s in false_sts], e)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs, bold=False):
    return len(str(t)) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


class Pos:
    """Correct letters (A-D) for picture questions, spread over the set."""

    def __init__(self, rnd):
        self.rnd, self.q = rnd, []

    def next(self):
        if not self.q:
            self.q = [0, 1, 2, 3]
            self.rnd.shuffle(self.q)
        return self.q.pop()


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag wide pictures so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions (5 each). Fixed A-D questions keep their order."""
    for s in sets:
        cnt = [0] * 4
        free = []
        for it in s["items"]:
            if it.pop("fixed", False):
                cnt[it["a"]] += 1
            else:
                free.append(it)
        need = [max(0, 5 - c) for c in cnt]
        assert sum(need) == len(free), (s["title"], cnt)
        targets = [i for i in range(4) for _ in range(need[i])]
        rnd.shuffle(targets)
        for it in free:
            rnd.shuffle(it["c"])
        for it, t in zip(free, targets):
            c = it["c"]
            i = c.index(it.pop("_c"))
            c[i], c[t] = c[t], c[i]
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


# ------------------------------------------------------------ pictures
class NL:
    """Horizontal number line from lo to hi with a tick every `step` and a label under every multiple of `lab`."""

    def __init__(self, lo, hi, step, lab, gap=None):
        lo, hi, step, lab = F(lo), F(hi), F(step), F(lab)
        k = (hi - lo) / step
        assert k.denominator == 1 and (lab / step).denominator == 1
        self.lo, self.hi, self.step, self.lab = lo, hi, step, lab
        self.n = int(k)
        self.labels = [lo + i * step for i in range(self.n + 1) if ((lo + i * step) / lab).denominator == 1]
        lw = max(tw(lbl(v), 14) for v in self.labels)
        self.g = gap or max(12, min(30, int(360 / self.n)))
        assert (lab / step) * self.g >= lw + 6, ("labels overlap", lo, hi, step, lab, self.g)
        self.pad = int(max(26, lw / 2 + 8))
        self.W = int(2 * self.pad + self.n * self.g)
        self.Y = 40
        self.H = 72
        self.pts = []

    def X(self, v):
        return self.pad + float((F(v) - self.lo) / self.step) * self.g

    def point(self, v, name=None, col=GREEN):
        v = F(v)
        assert self.lo <= v <= self.hi and ((v - self.lo) / self.step).denominator == 1, v
        self.pts.append((v, name, col))
        return self

    def svg(self, label):
        Y, s = self.Y, []
        x0, x1 = self.pad - 18, self.W - self.pad + 18
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x0, Y, x1, Y, INK))
        s.append("<path d='M%d %d l9 -5 v10 z M%d %d l-9 -5 v10 z' fill='%s'/>" % (x0 - 2, Y, x1 + 2, Y, INK))
        for i in range(self.n + 1):
            v = self.lo + i * self.step
            x = self.X(v)
            big = v in self.labels
            h = 9 if big else 5
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                     % (x, Y - h, x, Y + h, INK, "1.8" if big else "1.2"))
            if big:
                s.append(text(x, Y + 26, lbl(v), 14, bold=(v == 0)))
        xs = sorted(self.X(v) for v, nm, c in self.pts if nm)
        assert all(b - a >= 16 for a, b in zip(xs, xs[1:])), ("letters overlap", label)
        for v, nm, col in self.pts:
            x = self.X(v)
            s.append("<circle cx='%.1f' cy='%d' r='5.5' fill='%s'/>" % (x, Y, col))
            if nm:
                s.append(text(x, Y - 13, nm, 16, bold=True, col=col))
        return svg_wrap(self.W, self.H, "".join(s), label)


def vline_svg(lo, hi, step, lab, pts, label, zero_note=None):
    """Vertical number line; pts = [(value, name)] drawn as dots with the name to the right."""
    lo, hi, step, lab = F(lo), F(hi), F(step), F(lab)
    k = int((hi - lo) / step)
    g = 20
    top = 18
    x = 64
    Yv = lambda v: top + float((hi - F(v)) / step) * g
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%.1f' stroke='%s' stroke-width='2'/>" % (x, top - 12, x, Yv(lo) + 12, INK)]
    s.append("<path d='M%d %d l-5 9 h10 z M%d %.1f l-5 -9 h10 z' fill='%s'/>" % (x, top - 14, x, Yv(lo) + 14, INK))
    for i in range(k + 1):
        v = lo + i * step
        y = Yv(v)
        big = (v / lab).denominator == 1
        h = 9 if big else 5
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='%s'/>"
                 % (x - h, y, x + h, y, INK, "1.8" if big else "1.2"))
        if big:
            s.append(text(x - 15, y + 5, lbl(v), 14, anchor="end", bold=(v == 0)))
            assert x - 15 - tw(lbl(v), 14) >= 2
    W = 120
    if zero_note:
        assert all(F(v) != 0 for v, nm in pts)
        s.append(text(x + 16, Yv(0) + 5, zero_note, 14, anchor="start", col=GRAY))
        W = int(x + 16 + tw(zero_note, 14) + 8)
    ys = sorted(Yv(v) for v, nm in pts)
    assert all(b - a >= 18 for a, b in zip(ys, ys[1:])), ("letters overlap", label)
    for v, nm in pts:
        v = F(v)
        assert lo <= v <= hi and ((v - lo) / step).denominator == 1
        assert not zero_note or abs(Yv(v) - Yv(0)) >= 18
        s.append("<circle cx='%d' cy='%.1f' r='5.5' fill='%s'/>" % (x, Yv(v), GREEN))
        s.append(text(x + 16, Yv(v) + 6, nm, 16, anchor="start", bold=True, col=GREEN))
    return svg_wrap(W, int(Yv(lo) + 22), "".join(s), label)


def thermo_svg(lo, hi, step, lab, val, label):
    """Thermometer (°C) with a scale on the left; the red column ends at val."""
    lo, hi, step, lab, val = F(lo), F(hi), F(step), F(lab), F(val)
    k = int((hi - lo) / step)
    g = 16
    top = 16
    x = 74
    Yv = lambda v: top + float((hi - v) / step) * g
    bot = Yv(lo)
    s = ["<rect x='%d' y='%d' width='14' height='%.1f' rx='7' fill='#ffffff' stroke='%s' stroke-width='1.6'/>"
         % (x - 7, top - 8, bot - top + 16, INK)]
    s.append("<circle cx='%d' cy='%.1f' r='12' fill='%s' stroke='%s' stroke-width='1.6'/>" % (x, bot + 18, RED, INK))
    s.append("<rect x='%d' y='%.1f' width='6' height='%.1f' fill='%s'/>" % (x - 3, Yv(val), bot + 14 - Yv(val), RED))
    for i in range(k + 1):
        v = lo + i * step
        y = Yv(v)
        big = (v / lab).denominator == 1
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='%s'/>"
                 % (x - 9 - (8 if big else 4), y, x - 9, y, INK, "1.6" if big else "1.1"))
        if big:
            s.append(text(x - 22, y + 5, lbl(v), 14, anchor="end", bold=(v == 0)))
    s.append(text(x + 14, top + 4, "°C", 14, anchor="start"))
    return svg_wrap(110, int(bot + 34), "".join(s), label)


def nl_label(nl, what):
    return "number line from %s to %s %s" % (lbl(nl.lo), lbl(nl.hi), what)


# ============================================================ set 1: number lines
def set_numberline(rnd):
    its = []
    pos = Pos(rnd)
    # A: words to numbers (4)
    words = [
        ("negative two and three tenths", "-2.3", ["-2.03", "2.3", "-0.23"],
         "“Two and” is the whole number 2. “Three tenths” is 3 in the tenths place: 2.3. “Negative” adds the minus sign: "
         "<b>" + M + "2.3</b>."),
        ("negative four hundredths", "-0.04", ["-0.4", "-0.004", "0.04"],
         "Hundredths take two places after the decimal point, so 4 hundredths is 0.04. With the sign: <b>" + M + "0.04</b>. "
         + M + "0.4 is four tenths."),
        ("negative five and twelve thousandths", "-5.012", ["-5.12", "-5.0012", "5.012"],
         "Thousandths take three places, so twelve thousandths is 0.012. Add the 5 ones and the sign: <b>" + M + "5.012</b>. "
         + M + "5.12 is five and twelve hundredths."),
        ("negative three fifths", "-3/5", ["-5/3", "3/5", "-3.5"],
         "Three fifths is " + H("3/5") + ": 3 is the numerator and 5 is the denominator. With the sign: <b>" + H("-3/5") +
         "</b>. " + M + "3.5 is three and five tenths."),
    ]
    for w, c, wr, e in words:
        its.append(mcq_num("Which number is “%s”?" % w, c, wr, e))
    # B: the same number as a fraction or a decimal (3)
    eq = [
        ("Point A is at " + M + "0.75. Which fraction names the same point?", "-3/4", ["-7/5", "3/4", "-1/4"],
         "0.75 = 75 hundredths = " + H("75/100") + " = " + H("3/4") + ". The point is negative, so A = <b>" + H("-3/4") + "</b>. "
         "Do not drop the minus sign."),
        ("Which decimal names the same number as " + H("-2/5") + "?", "-0.4", ["-2.5", "-0.2", "0.4"],
         H("2/5") + " = " + H("4/10") + " = 0.4. So " + H("-2/5") + " = <b>" + M + "0.4</b>. "
         + M + "2.5 just puts the 2 and the 5 on each side of a decimal point."),
        ("Which decimal names the same number as " + H("-1 1/2") + "?", "-1.5", ["-1.2", "1.5", "-1.12"],
         H("1/2") + " = " + H("5/10") + " = 0.5, so " + H("-1 1/2") + " = <b>" + M + "1.5</b>. "
         "The denominator 2 does not become the digit 2."),
    ]
    for q, c, wr, e in eq:
        its.append(mcq_num(q, c, wr, e))
    # C: read a decimal on a number line (3)
    reads = [
        (NL(-1, 1, F(1, 10), F(1, 2)), "-0.7", ["0.7", "-0.3", "-0.8", "-0.6"],
         "There are 5 spaces between " + M + "0.5 and 0, so each tick mark is 0.1. A is 2 tick marks left of " + M +
         "0.5: " + M + "0.6, " + M + "0.7. A = <b>" + M + "0.7</b>. Going left makes a number less, so it is not " + M + "0.3."),
        (NL(-2, 1, F(1, 10), 1), "-1.4", ["1.4", "-1.6", "-0.6", "-1.3"],
         "There are 10 spaces between " + M + "2 and " + M + "1, so each tick mark is 0.1. A is 4 tick marks left of " + M +
         "1: " + M + "1.1, " + M + "1.2, " + M + "1.3, " + M + "1.4. A = <b>" + M + "1.4</b>. It is 6 tick marks right of " +
         M + "2, so it is not " + M + "1.6."),
        (NL(F(-1, 2), F(-2, 5), F(1, 100), F(1, 10), gap=30), "-0.43", ["-0.47", "0.43", "-0.403", "-0.44"],
         "There are 10 spaces between " + M + "0.5 and " + M + "0.4, so each tick mark is 0.01. A is 3 tick marks left of " +
         M + "0.4: " + M + "0.41, " + M + "0.42, " + M + "0.43. A = <b>" + M + "0.43</b>. " + M +
         "0.47 is 3 tick marks from " + M + "0.5, the wrong end."),
    ]
    for nl, c, wr, e in reads:
        nl.point(V(c), "A")
        q = fig(nl.svg(nl_label(nl, "with point A"))) + "What number is at point A?"
        its.append(mcq_num(q, c, wr, e))
    # D: read a fraction on a number line (3)
    freads = [
        (NL(-1, 0, F(1, 4), 1, gap=60), "-1/4", ["-3/4", "1/4", "-1/3"],
         "There are 4 equal spaces between " + M + "1 and 0, so each space is " + H("1/4") + ". A is 1 space left of 0: "
         "A = <b>" + H("-1/4") + "</b>. Count the spaces, not the 3 tick marks in between (that gives thirds)."),
        (NL(-2, 0, F(1, 3), 1, gap=45), "-1 2/3", ["-1 1/3", "1 2/3", "-2/3"],
         "There are 3 equal spaces between whole numbers, so each space is " + H("1/3") + ". A is 2 spaces left of " + M +
         "1: " + H("-1 1/3") + ", " + H("-1 2/3") + ". A = <b>" + H("-1 2/3") + "</b>. Do not forget the whole number: " +
         H("-2/3") + " is between " + M + "1 and 0."),
        (NL(-1, 1, F(1, 5), 1, gap=34), "-3/5", ["-2/5", "3/5", "-3/4"],
         "There are 5 equal spaces between " + M + "1 and 0, so each space is " + H("1/5") + ". A is 3 spaces left of 0: "
         "A = <b>" + H("-3/5") + "</b>. It is 2 spaces right of " + M + "1, so it is not " + H("-2/5") + "."),
    ]
    for nl, c, wr, e in freads:
        nl.point(V(c), "A")
        q = fig(nl.svg(nl_label(nl, "with point A"))) + "What number is at point A?"
        its.append(mcq_num(q, c, wr, e))
    # E: which point is at ... (4)
    lets = [
        (NL(-2, 2, F(1, 4), 1, gap=22), "-1.25", ["-0.75", "1.25", "-1.75"],
         "Each whole is split into 4 spaces, so each tick mark is 0.25. " + M + "1.25 is 1 tick mark left of " + M + "1. "
         "The point 1 tick mark right of " + M + "1 is " + M + "0.75."),
        (NL(-1, 1, F(1, 4), 1, gap=40), "-3/4", ["-1/4", "3/4", "1/4"],
         "Each space is " + H("1/4") + ". " + H("-3/4") + " is 3 spaces left of 0, which is 1 space right of " + M + "1."),
        (NL(-1, 1, F(1, 10), 1, gap=18), "-0.6", ["-0.4", "0.6", "0.4"],
         "There are 10 spaces between " + M + "1 and 0, so each tick mark is 0.1. " + M + "0.6 is 6 tick marks left of 0. "
         + M + "0.4 is only 4 tick marks left of 0."),
        (NL(-3, 3, F(1, 3), 1, gap=24), "-2 1/3", ["-2 2/3", "-1 2/3", "2 1/3"],
         "Each space is " + H("1/3") + ". " + H("-2 1/3") + " is 1 space left of " + M + "2. " + H("-2 2/3") +
         " is 2 spaces left of " + M + "2, and " + H("-1 2/3") + " is 2 spaces left of " + M + "1."),
    ]
    for nl, c, wr, e in lets:
        lp = pos.next()
        letters = [l for l in range(4) if l != lp]
        nl.point(V(c), "ABCD"[lp])
        for w, l in zip(wr, letters):
            nl.point(V(w), "ABCD"[l])
        q = fig(nl.svg(nl_label(nl, "with points A, B, C and D"))) + "Which point is at %s?" % H(c)
        e2 = e.replace("<b>", "").replace("</b>", "") + " The answer is point <b>%s</b>." % "ABCD"[lp]
        its.append(mcq_fixed(q, ["A", "B", "C", "D"], "ABCD"[lp], e2))
    # F: vertical number lines (2)
    q = (fig(vline_svg(F(-1, 2), F(1, 2), F(1, 10), F(1, 2), [(F(-3, 10), "A")],
                       "vertical number line from " + M + "0.5 to 0.5 counting by 0.1 with point A", "usual level")) +
         "This vertical number line shows the water level of Lake Ontario compared with its usual level, in metres. "
         "What number is at point A?")
    e = ("There are 5 spaces between 0 and 0.5, so each tick mark is 0.1. A is 2 tick marks above " + M + "0.5: " + M +
         "0.4, " + M + "0.3. A = <b>" + M + "0.3</b>, so the lake is 0.3" + NB + "m below its usual level. "
         "Going up makes a number greater, so it is not " + M + "0.7.")
    its.append(mcq_num(q, "-0.3", ["0.3", "-0.7", "-0.4"], e))
    q = (fig(thermo_svg(-3, 2, F(1, 2), 1, F(-3, 2), "thermometer from " + M + "3 to 2 °C counting by 0.5")) +
         "This thermometer shows the temperature at a ski hill near Collingwood. What is the temperature?")
    e = ("The labels count by 1, and there are 2 spaces between labels, so each tick mark is 0.5 degrees. The top of the red "
         "column is 1 tick mark below " + M + "1: <b>" + deg("-1.5") + "</b>. (Counting each tick mark as 0.1 gives " +
         M + "1.1.)")
    its.append(mcq_num(q, "-1.5", ["-0.5", "1.5", "-1.1"], e, NB + "°C"))
    # G: where is it (1)
    its.append(mcq_txt("Which describes where " + M + "2.7 is on a number line?",
                       "between " + M + "3 and " + M + "2, closer to " + M + "3",
                       ["between " + M + "3 and " + M + "2, closer to " + M + "2", "between 2 and 3, closer to 3",
                        "between " + M + "2 and " + M + "1, closer to " + M + "2"],
                       M + "2.7 is 2.7 units left of 0, past " + M + "2 but not as far as " + M + "3. It is 0.3 from " + M +
                       "3 and 0.7 from " + M + "2, so it is <b>between " + M + "3 and " + M + "2, closer to " + M + "3</b>."))
    assert len(its) == 20
    return {"title": "Fractions and decimals on a number line", "items": its}


# ============================================================ set 2: compare and order
def approx(t):
    """Decimal form of a token for explanations (3 places for fractions that do not end)."""
    v = V(t)
    d = v.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    if d == 1:
        return P(dtok(v))
    q = Decimal(v.numerator) / Decimal(v.denominator)
    return "about " + P(str(q.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)))


def show(t):
    """Token and, for fractions, its decimal."""
    if "/" in t:
        return "%s = %s" % (H(t), approx(t))
    return H(t)


def lst(toks):
    return ", ".join(H(t) for t in toks)


def set_compare(rnd):
    its = []
    # A: which statement is true (5); each false statement is a real mistake
    tf = [
        (st("-0.25", ">", "-0.5"), [st("0.45", ">", "0.5"), st("-0.8", ">", "-0.75"), st("-1.2", ">", "-1.15")],
         M + "0.25 is closer to 0 than " + M + "0.5, so <b>" + M + "0.25 &gt; " + M + "0.5</b>. The others are false: "
         "0.45 &lt; 0.50, " + M + "0.8 &lt; " + M + "0.75 and " + M + "1.2 &lt; " + M + "1.15."),
        (st("0.45", "<", "0.5"), [st("-0.5", ">", "-0.25"), st("-0.06", "<", "-0.6"), st("0.305", ">", "0.35")],
         "0.5 = 0.50, and 45 hundredths &lt; 50 hundredths, so <b>0.45 &lt; 0.5</b>. A longer decimal is not always greater. "
         "The others are false: " + M + "0.5 is farther left than " + M + "0.25, " + M + "0.06 is closer to 0 than " + M +
         "0.6, and 0.305 &lt; 0.350."),
        (st("-0.8", "<", "-0.75"), [st("0.09", ">", "0.1"), st("-2.4", ">", "-2.375"), st("-0.5", ">", "-0.25")],
         M + "0.8 = " + M + "0.80 is farther from 0 than " + M + "0.75, so <b>" + M + "0.8 &lt; " + M + "0.75</b>. "
         "The others are false: 0.09 &lt; 0.10, " + M + "2.4 = " + M + "2.400 &lt; " + M + "2.375, and " + M + "0.5 &lt; " +
         M + "0.25."),
        (st("-0.06", ">", "-0.6"), [st("-1.2", ">", "-1.15"), st("0.305", ">", "0.35"), st("0.45", ">", "0.5")],
         M + "0.06 is 6 hundredths from 0. " + M + "0.6 = " + M + "0.60 is 60 hundredths from 0, farther left. So <b>" + M +
         "0.06 &gt; " + M + "0.6</b>. The others are false: " + M + "1.2 = " + M + "1.20 &lt; " + M +
         "1.15, 0.305 &lt; 0.350, and 0.45 &lt; 0.50."),
        (st("-2.375", ">", "-2.4"), [st("0.09", ">", "0.1"), st("-0.8", ">", "-0.75"), st("-0.5", ">", "-0.25")],
         "Write " + M + "2.4 as " + M + "2.400. " + M + "2.375 is closer to 0, so <b>" + M + "2.375 &gt; " + M +
         "2.4</b>. The others are false: 0.09 &lt; 0.10, " + M + "0.8 &lt; " + M + "0.75 and " + M + "0.5 &lt; " + M + "0.25."),
    ]
    for t, fs, e in tf:
        its.append(mcq_stmt("Which statement is true?", t, fs, e))
    # B: the greatest / the least of four (5)
    gl = [("least", ["-0.6", "-0.65", "-0.065", "0.6"]),
          ("greatest", ["-3/4", "-2/3", "-0.7", "-0.72"]),
          ("greatest", ["-1.09", "-1.9", "-1.1", "-1.009"]),
          ("least", ["-2 1/2", "-2.45", "-2 3/8", "-2.4"]),
          ("greatest", ["0.408", "0.48", "0.4", "0.084"])]
    for kind, toks in gl:
        best = (max if kind == "greatest" else min)(toks, key=V)
        q = "Which number is the %s? %s" % (kind, lst(toks))
        conv = [t for t in toks if "/" in t]
        e = ""
        if conv:
            e += "Write the fractions as decimals: " + "; ".join(show(t) for t in conv) + ". "
        if kind == "greatest":
            if all(V(t) < 0 for t in toks):
                e += "All four are negative, so the greatest is the one closest to 0: <b>%s</b>." % H(best)
            else:
                e += "Compare place by place: 0.480 is the most thousandths. The greatest is <b>%s</b>." % H(best)
        else:
            e += "The least number is the one farthest left on a number line: <b>%s</b>." % H(best)
        if best == "-1.009":
            e += " " + M + "1.9 has the biggest digits, so it is the least."
        if best == "0.48":
            e += " 0.408 has more digits, but 0.408 &lt; 0.480."
        if best == "-0.65":
            e += " " + M + "0.65 = " + M + "0.650 is farther from 0 than " + M + "0.6 = " + M + "0.600 and " + M + "0.065."
        if best == "-2 1/2":
            e += " " + M + "2.5 = " + M + "2.50 is farther from 0 than " + M + "2.45."
        its.append(mcq_num(q, best, sorted([t for t in toks if t != best], key=lambda t: -abs(V(t)))[::-1], e))
    # C: order (5)
    orders = [(True, ["-0.5", "-0.25", "0.4", "-0.75"]), (True, ["-1/2", "-1/3", "-3/4", "2/3"]),
              (True, ["-1.2", "0.8", "-1.25", "-0.08"]), (False, ["-2/5", "0.3", "-0.45", "-1/4"]),
              (False, ["-3.6", "-3 3/4", "-3.06", "3.5"])]
    for asc, toks in orders:
        right = sorted(toks, key=V, reverse=not asc)
        by_abs = sorted(toks, key=lambda t: abs(V(t)), reverse=not asc)
        rev = sorted(toks, key=V, reverse=asc)
        negs = [t for t in toks if V(t) < 0]
        poss = [t for t in toks if V(t) >= 0]
        if asc:     # negatives ordered by their digits: closest to 0 first
            negw = sorted(negs, key=V, reverse=True) + sorted(poss, key=V)
        else:
            negw = sorted(poss, key=V, reverse=True) + sorted(negs, key=V)
        conv = [t for t in toks if "/" in t]
        e = ""
        if conv:
            e += "Write the fractions as decimals: " + "; ".join(show(t) for t in conv) + ". "
        if asc:
            e += "Start with the number farthest left. Among negative numbers, the one farthest from 0 is the least: "
        else:
            e += "Start with the number farthest right. Among negative numbers, the one closest to 0 comes first: "
        e += "<b>%s</b>." % lst(right)
        q = "Which list is in order from %s? %s" % ("least to greatest" if asc else "greatest to least", lst(toks))
        its.append(mcq_txt(q, lst(right), [lst(negw), lst(by_abs), lst(rev)], e))
    # D: fractions (3)
    its.append(mcq_stmt("Which statement is true?", st("-2/3", ">", "-3/4"),
                        [st("-2/3", "<", "-3/4"), st("-2/3", "=", "-3/4"), st("2/3", ">", "3/4")],
                        "Use a common denominator: " + H("-2/3") + " = " + H("-8/12") + " and " + H("-3/4") + " = " +
                        H("-9/12") + ". " + H("-8/12") + " is closer to 0, so <b>" + H("-2/3") + " &gt; " + H("-3/4") +
                        "</b>. Without the signs it is the other way: " + H("2/3") + " &lt; " + H("3/4") + "."))
    its.append(mcq_stmt("Which statement is true?", st("-5/8", "<", "-0.6"),
                        [st("-5/8", ">", "-0.6"), st("-5/8", "=", "-0.6"), st("5/8", "<", "0.6")],
                        H("5/8") + " = 5 ÷ 8 = 0.625, so " + H("-5/8") + " = " + M + "0.625. It is farther from 0 than " + M +
                        "0.600, so <b>" + H("-5/8") + " &lt; " + M + "0.6</b>."))
    its.append(mcq_stmt("Which statement is true?", st("3/8", "=", "0.375"),
                        [st("3/8", "<", "0.375"), st("3/8", ">", "0.375"), st("3/8", "=", "0.38")],
                        H("3/8") + " = 3 ÷ 8 = 0.375, so <b>" + H("3/8") + " = 0.375</b>. 0.38 is close, but it is not equal: "
                        "0.375 rounds to 0.38."))
    # E: temperatures (2)
    toks = ["-2.5", "-2.05", "-2.45", "-0.25"]
    its.append(mcq_num("Which temperature is the coldest? " + ", ".join(deg(t) for t in toks), "-2.5",
                       ["-2.05", "-2.45", "-0.25"],
                       "The coldest temperature is the least number, the one farthest below 0. " + M + "2.5 = " + M +
                       "2.50 is farther below 0 than " + M + "2.45 and " + M + "2.05: <b>" + deg("-2.5") + "</b>.", NB + "°C"))
    its.append(mcq_num("Which temperature is warmer than " + deg("-4.3") + "?", "-4.25", ["-4.35", "-4.5", "-4.31"],
                       "Warmer means greater: closer to 0 or above it. " + M + "4.25 is closer to 0 than " + M + "4.3 = " +
                       M + "4.30, so <b>" + deg("-4.25") + "</b> is warmer. " + M + "4.35, " + M + "4.5 and " + M +
                       "4.31 are all colder.", NB + "°C"))
    assert len(its) == 20
    return {"title": "Compare and order fractions and decimals", "items": its}


# ============================================================ set 3: simplify fractions
def fstr(a, b, neg=False):
    return ("-" if neg else "") + "%d/%d" % (a, b)


def simp_item(a, b, neg=False, extra=None):
    g = gcd(a, b)
    c = fstr(a // g, b // g, neg)
    wr = list(extra or []) + [fstr(a // g, b, neg), fstr(b // g, a // g, neg), fstr(a, b // g, neg)]
    if neg:
        wr = [fstr(a // g, b // g)] + wr
    q = "Write %s in simplest form." % H(fstr(a, b, neg))
    small = [d for d in range(2, g) if g % d == 0]
    e = ("The greatest common factor (GCF) of %d and %d is %d. %d ÷ %d = %d and %d ÷ %d = %d, so %s = <b>%s</b>."
         % (a, b, g, a, g, a // g, b, g, b // g, H(fstr(a, b, neg)), H(c)))
    if small:
        d = small[0]
        e += " (Dividing by %d gives %s: equal, but not yet in simplest form.)" % (d, H(fstr(a // d, b // d, neg)))
    else:
        e += " Divide the numerator and the denominator by the same number."
    if neg:
        e += " Keep the minus sign."
    return mcq_num(q, c, wr, e)


def set_simplify(rnd):
    its = []
    # A: positive fractions (8)
    for a, b, extra in [(6, 8, None), (9, 12, None), (12, 18, ["2/9"]), (15, 25, ["3/25"]), (16, 24, None),
                        (14, 35, None), (20, 32, ["5/16"]), (18, 45, None)]:
        its.append(simp_item(a, b, extra=extra))
    # B: negative fractions (4)
    for a, b in [(10, 15), (8, 12), (21, 28), (24, 40)]:
        its.append(simp_item(a, b, neg=True))
    # C: GCF and simplest form (4)
    its.append(mcq_num("What is the greatest common factor of 24 and 36?", "12", ["6", "4", "72"],
                       "Factors of 24: 1, 2, 3, 4, 6, 8, 12, 24. Factors of 36: 1, 2, 3, 4, 6, 9, 12, 18, 36. "
                       "The greatest one in both lists is <b>12</b>. 6 and 4 are common factors, but not the greatest. "
                       "72 is a common multiple."))
    its.append(mcq_num("What is the greatest common factor of 18 and 30?", "6", ["3", "2", "90"],
                       "Factors of 18: 1, 2, 3, 6, 9, 18. Factors of 30: 1, 2, 3, 5, 6, 10, 15, 30. The greatest one in "
                       "both lists is <b>6</b>. 90 is a common multiple, not a factor."))
    its.append(mcq_txt("Which fraction is in simplest form?", H("9/16"), [H("6/15"), H("14/21"), H("10/12")],
                       "A fraction is in simplest form when the only common factor of the numerator and the denominator is 1. "
                       "9 = 3 × 3 and 16 = 2 × 2 × 2 × 2 share no factor, so <b>" + H("9/16") + "</b> is in simplest form. "
                       + H("6/15") + " (÷ 3), " + H("14/21") + " (÷ 7) and " + H("10/12") + " (÷ 2) can be simplified."))
    its.append(mcq_txt("Which fraction is in simplest form?", H("-5/9"), [H("-4/10"), H("-9/15"), H("-12/16")],
                       "5 and 9 have no common factor except 1, so <b>" + H("-5/9") + "</b> is in simplest form. "
                       + H("-4/10") + " (÷ 2), " + H("-9/15") + " (÷ 3) and " + H("-12/16") + " (÷ 4) can be simplified."))
    # D: decimal to fraction in simplest form (4)
    dec = [("0.75", "3/4", ["7/5", "75/10", "1/4"], "75 hundredths", "75/100", 25),
           ("-0.4", "-2/5", ["-1/4", "-4/100", "2/5"], "4 tenths", "4/10", 2),
           ("-0.6", "-3/5", ["-1/6", "-6/100", "3/5"], "6 tenths", "6/10", 2),
           ("0.35", "7/20", ["7/2", "3/5", "7/10"], "35 hundredths", "35/100", 5)]
    for d, c, wr, words, f0, g in dec:
        neg = d.startswith("-")
        q = "Write %s as a fraction in simplest form." % H(d)
        e = ("%s is %s%s = %s. Divide both parts by %d: <b>%s</b>." % (
            H(d.lstrip("-")), words, "", H(f0), g, H(c.lstrip("-"))))
        if neg:
            e = e.replace("<b>%s</b>." % H(c.lstrip("-")), "%s. With the sign: <b>%s</b>." % (H(c.lstrip("-")), H(c)))
        assert V(c) == V(d) and V(f0) == abs(V(d))
        its.append(mcq_num(q, c, wr, e))
    assert len(its) == 20
    return {"title": "Simplify fractions", "items": its}


# ============================================================ set 4: between and rounding
def rnd_tok(t, places):
    d = Decimal(t)
    q = Decimal(1).scaleb(-places)
    # never a tie for a negative number (the rule for those is not taught)
    if d < 0:
        assert (abs(d) * 10 ** places) % 1 != Decimal("0.5"), t
    return str(d.quantize(q, rounding=ROUND_HALF_UP))


PLACE = {0: "whole number", 1: "tenth", 2: "hundredth"}
NEXT = {0: "tenths", 1: "hundredths", 2: "thousandths"}


def set_between_round(rnd):
    its = []

    def btw(x, a, b):
        lo, hi = sorted([V(a), V(b)])
        return lo < V(x) < hi

    # A: a number between two numbers (10)
    bt = [
        ("0.3", "0.4", "0.37", ["0.43", "0.035", "3.5"],
         "0.3 = 0.30 and 0.4 = 0.40. Any number of hundredths from 31 to 39 is between them: <b>0.37</b>."),
        ("-0.5", "-0.4", "-0.45", ["-0.55", "-0.35", "0.45"],
         "Write them as " + M + "0.50 and " + M + "0.40. " + M + "0.45 is halfway between them: <b>" + M + "0.45</b>. " +
         M + "0.55 is farther left than " + M + "0.5."),
        ("-2", "-2.1", "-2.05", ["-2.15", "-1.95", "-2.5"],
         "Write them as " + M + "2.00 and " + M + "2.10. " + M + "2.05 is between them: <b>" + M + "2.05</b>. " + M +
         "2.5 is farther left than " + M + "2.1."),
        ("1/4", "1/3", "0.3", ["0.2", "0.35", "0.25"],
         H("1/4") + " = 0.25 and " + H("1/3") + " = 0.333… So <b>0.3</b> is between them. 0.25 is equal to " + H("1/4") +
         ", so it is not between."),
        ("-3/4", "-1/2", "-5/8", ["-7/8", "-3/8", "5/8"],
         "Use eighths: " + H("-3/4") + " = " + H("-6/8") + " and " + H("-1/2") + " = " + H("-4/8") + ". " + H("-5/8") +
         " is between them: <b>" + H("-5/8") + "</b>."),
        ("-1/2", "-1/3", "-5/12", ["-3/5", "-1/4", "5/12"],
         "Use twelfths: " + H("-1/2") + " = " + H("-6/12") + " and " + H("-1/3") + " = " + H("-4/12") + ". " + H("-5/12") +
         " is between them: <b>" + H("-5/12") + "</b>."),
        ("-0.1", "-0.09", "-0.095", ["-0.11", "-0.085", "0.095"],
         "Write them as " + M + "0.100 and " + M + "0.090. " + M + "0.095 is between them: <b>" + M + "0.095</b>. "
         "Adding a thousandths digit gives room for more numbers."),
    ]
    for a, b, c, wr, e in bt:
        assert btw(c, a, b) and not any(btw(w, a, b) for w in wr), (a, b)
        its.append(mcq_num("Which number is between %s and %s?" % (H(a), H(b)), c, wr, e))
    its.append(mcq_num("Which number is <b>not</b> between " + M + "3 and " + M + "2?", "-3.2", ["-2.9", "-2.15", "-2 1/2"],
                       M + "3.2 is farther left than " + M + "3, so <b>" + M + "3.2</b> is not between " + M + "3 and " +
                       M + "2. The other three are all more than " + M + "3 and less than " + M + "2."))
    assert not btw("-3.2", "-3", "-2") and all(btw(w, "-3", "-2") for w in ["-2.9", "-2.15", "-2 1/2"])
    its.append(mcq_num("Which number is exactly halfway between " + M + "0.6 and " + M + "0.5?", "-0.55",
                       ["-0.65", "-0.505", "-0.45"],
                       "Write them as " + M + "0.60 and " + M + "0.50. Halfway between 60 and 50 hundredths is 55 hundredths: "
                       "<b>" + M + "0.55</b>."))
    assert (V("-0.6") + V("-0.5")) / 2 == V("-0.55")
    its.append(mcq_txt("Which statement about 0.12 and 0.13 is true?",
                       "There are many numbers between them, such as 0.125.",
                       ["There are no numbers between them.", "Only 0.125 is between them.",
                        "Only 0.121 to 0.129 are between them."],
                       "Between any two different numbers there is always another number. 0.12 = 0.120 and 0.13 = 0.130, "
                       "so 0.121, 0.125 and 0.1255 are all between them. <b>There are many numbers between them.</b>"))
    # B: rounding (10)
    rq = [
        ("3.648", 2, ["3.64", "3.6", "3.7"]),
        ("5.555", 1, ["5.5", "5.56", "6"]),
        ("0.047", 2, ["0.04", "0.5", "0.1"]),
        ("0.666", 2, ["0.66", "0.7", "0.667"]),
        ("-2.46", 1, ["-2.4", "2.5", "-3"]),
        ("-0.38", 1, ["-0.3", "0.4", "0"]),
        ("-14.7", 0, ["-14", "15", "-10"]),
        ("12.49", 0, ["13", "12.5", "12.4"]),
        ("-6.97", 1, ["-6.10", "-6.9", "7.0"]),
    ]
    for t, p, wr in rq:
        c = rnd_tok(t, p)
        d = Decimal(t)
        digits = t.lstrip("-").split(".")
        nxt = int(digits[1][p])
        up = nxt >= 5
        if d < 0:
            e = ("Round %s as if it were positive. To the nearest %s, look at the %s digit: %d. It is %s, so %s rounds "
                 "to %s. Keep the minus sign: <b>%s</b>." % (H(t[1:]), PLACE[p], NEXT[p], nxt,
                                                            "5 or more" if up else "4 or less", H(t[1:]), H(c[1:]), H(c)))
        else:
            e = ("To the nearest %s, look at the %s digit: %d. It is %s, so round %s: <b>%s</b>."
                 % (PLACE[p], NEXT[p], nxt, "5 or more" if up else "4 or less", "up" if up else "down", H(c)))
        if t == "12.49":
            e += " Do not round twice (12.49 → 12.5 → 13). Use the digit right after the ones place."
        if t == "-6.97":
            e += " 9 tenths + 1 tenth = 10 tenths = 1 one, so 6.9 becomes 7.0. Keep the 0 to show tenths."
        if t == "-0.38":
            e += " " + M + "0.38 is closer to " + M + "0.4 than to " + M + "0.3."
        if t == "0.666":
            e += " 0.667 is rounded to the nearest thousandth, not hundredth."
        q = "Round %s to the nearest %s." % (H(t), PLACE[p])
        its.append(mcq_num(q, c, wr, e))
    c = "-3.18"
    wr = ["-3.12", "-3.26", "3.18"]
    assert rnd_tok(c, 1) == "-3.2" and all(rnd_tok(w, 1) != "-3.2" for w in wr)
    its.append(mcq_num("Which number rounds to " + M + "3.2 when it is rounded to the nearest tenth?", c, wr,
                       M + "3.18 is 2 hundredths from " + M + "3.2, so it rounds to " + M + "3.2: <b>" + M + "3.18</b>. "
                       + M + "3.12 rounds to " + M + "3.1, " + M + "3.26 rounds to " + M + "3.3, and 3.18 is positive."))
    assert len(its) == 20
    return {"title": "Numbers in between and rounding", "items": its}


# ============================================================ set 5: word problems
def set_words(rnd):
    its = []
    # 1
    its.append(mcq_num("The water level of a lake dropped to 0.75" + NB + "m below its normal level. Which number shows the "
                       "water level compared with normal?", "-0.75", ["0.75", "-7.5", "-0.075"],
                       "Below the normal level is the negative direction, and 0 is the normal level. The level is <b>" + M +
                       "0.75</b> (in metres)."))
    # 2
    its.append(mcq_txt("At the Terry Fox Run, Maya ran 2.75" + NB + "km and Arjun ran 2" + NB + frh(3, 4) + NB + "km. "
                       "Which statement is true?", "They ran the same distance.",
                       ["Maya ran farther.", "Arjun ran farther.", "A fraction and a decimal cannot be compared."],
                       H("3/4") + " = 0.75, so 2" + NB + H("3/4") + NB + "km = 2.75" + NB + "km. <b>They ran the same distance.</b>"))
    # 3
    its.append(mcq_txt("In Owen’s class, " + H("3/8") + " of the students walk to school and 0.4 of the students take the bus. "
                       "Which statement is true?", "More students take the bus than walk.",
                       ["More students walk than take the bus.", "The same number of students walk and take the bus.",
                        "A fraction and a decimal cannot be compared."],
                       H("3/8") + " = 3 ÷ 8 = 0.375, and 0.375 &lt; 0.400. <b>More students take the bus than walk.</b>"))
    assert V("3/8") < V("0.4")
    # 4
    its.append(mcq_txt("Ethan’s bank balance is " + M + "$12.50. Chloe’s bank balance is " + M + "$12.05. Who owes more money?",
                       "Ethan", ["Chloe", "They owe the same amount.", "Neither of them owes money."],
                       "A negative balance is money owed. $12.50 is more than $12.05, so " + M + "$12.50 is farther below "
                       "$0. <b>Ethan</b> owes more."))
    # 5
    towns = [("Kenora", "-8.45"), ("Timmins", "-8.5"), ("Sudbury", "-8.05"), ("Thunder Bay", "-8.4")]
    its.append(mcq_txt("One night in January, the lows were: " + ", ".join("%s %s" % (a, deg(b)) for a, b in towns) +
                       ". Which town was the coldest?", "Timmins", ["Kenora", "Sudbury", "Thunder Bay"],
                       "The coldest is the least number. Write them with two decimal places: " + M + "8.45, " + M + "8.50, " +
                       M + "8.05, " + M + "8.40. " + M + "8.50 is farthest below 0, so <b>Timmins</b> was the coldest."))
    # 6
    its.append(mcq_txt("Near a wharf in Nova Scotia, a scuba diver is at " + m_("-4.25") + ", a crab is at " + m_("-4.5") +
                       " and a lobster trap is at " + m_("-4.05") + ". The dock is at " + m_("1.5") +
                       ". (0" + NB + "m is sea level.) Which is the lowest?", "the crab",
                       ["the scuba diver", "the lobster trap", "the dock"],
                       "The lowest is the least number. " + M + "4.5 = " + M + "4.50 is farther below 0 than " + M + "4.25 and "
                       + M + "4.05, so <b>the crab</b> is the lowest."))
    # 7
    sw = [("Mei", "48.37"), ("Kai", "48.4"), ("Zoe", "48.307"), ("Mateo", "48.73")]
    its.append(mcq_txt("Luge races are timed to the thousandth of a second. At a youth race in Calgary, the times were: " +
                       ", ".join("%s %s" % (a, b) + NB + "s" for a, b in sw) + ". Who was the fastest?", "Zoe",
                       ["Mei", "Kai", "Mateo"],
                       "The fastest slider has the least time. Write them with three decimal places: 48.370, 48.400, 48.307, "
                       "48.730. 48.307 is the least, so <b>Zoe</b> was the fastest."))
    # 8
    its.append(mcq_num("The overnight low in Barrie was between " + deg("-6.3") + " and " + deg("-6.2") +
                       ". Which temperature could it have been?", "-6.25", ["-6.35", "-6.15", "-6.5"],
                       "Write them as " + M + "6.30 and " + M + "6.20. " + M + "6.25 is between them: <b>" + deg("-6.25") +
                       "</b>.", NB + "°C"))
    # 9
    its.append(mcq_txt("A recipe for maple syrup cookies needs more than " + H("1/3") + " cup of syrup but less than " +
                       H("1/2") + " cup. Which amount works?", "0.4 cup", ["0.3 cup", "0.25 cup", "0.55 cup"],
                       H("1/3") + " = 0.333… and " + H("1/2") + " = 0.5. <b>0.4 cup</b> is between them. 0.3 is less than "
                       "0.333…"))
    for w in ["0.3", "0.25", "0.55"]:
        assert not V("1/3") < V(w) < V("1/2")
    # 10
    its.append(mcq_num("An arena manager wants the ice temperature between " + deg("-5.5") + " and " + deg("-4.5") +
                       ". Which reading is in that range?", "-4.75", ["-5.75", "-4.25", "4.75"],
                       M + "4.75 is more than " + M + "5.5 and less than " + M + "4.5, so <b>" + deg("-4.75") + "</b> is in the "
                       "range. " + M + "5.75 is too cold and " + M + "4.25 is too warm.", NB + "°C"))
    # 11
    its.append(mcq_num("18 of the 24 students in Priya’s class went to the skating rink. What fraction of the class went, "
                       "in simplest form?", "3/4", ["1/4", "4/3", "3/8"],
                       H("18/24") + ": the GCF of 18 and 24 is 6. 18 ÷ 6 = 3 and 24 ÷ 6 = 4, so <b>" + H("3/4") + "</b>. "
                       + H("1/4") + " is the part that did not go."))
    # 12
    its.append(mcq_num("Leah’s ringette team won 12 of its 20 games. What fraction of the games did the team win, in simplest form?",
                       "3/5", ["2/5", "5/3", "3/10"],
                       H("12/20") + ": the GCF of 12 and 20 is 4. 12 ÷ 4 = 3 and 20 ÷ 4 = 5, so <b>" + H("3/5") + "</b>. "
                       + H("2/5") + " is the part of the games they lost."))
    # 13
    its.append(mcq_txt("Gas costs 151.9¢ per litre. What is that price rounded to the nearest cent?", "152¢",
                       ["151¢", "150¢", "160¢"],
                       "Look at the tenths digit: 9. It is 5 or more, so round up: <b>152¢</b>. 151¢ cuts off the 9 instead of "
                       "rounding."))
    # 14
    its.append(mcq_num("A thermometer in Iqaluit reads " + deg("-17.6") + ". What is the temperature to the nearest degree?",
                       "-18", ["-17", "18", "-20"],
                       "Round 17.6 as if it were positive: the tenths digit is 6, so it rounds up to 18. Keep the sign: <b>" +
                       deg("-18") + "</b>. " + M + "17.6 is closer to " + M + "18 than to " + M + "17.", NB + "°C"))
    assert rnd_tok("-17.6", 0) == "-18"
    # 15
    its.append(mcq_num("A research submarine in Lake Superior is at " + m_("-87.46") + " (0" + NB + "m is the surface of the lake). "
                       "What is its position to the nearest tenth of a metre?", "-87.5", ["-87.4", "87.5", "-88"],
                       "Look at the hundredths digit: 6. It is 5 or more, so 87.46 rounds to 87.5. Keep the sign: <b>" +
                       m_("-87.5") + "</b>.", NB + "m"))
    assert rnd_tok("-87.46", 1) == "-87.5"
    # 16
    its.append(mcq_num("The CN Tower in Toronto is about 553.33" + NB + "m tall. What is its height to the nearest tenth of a metre?",
                       "553.3", ["553.4", "553", "550"],
                       "Look at the hundredths digit: 3. It is 4 or less, so round down: <b>" + m_("553.3") + "</b>. "
                       "553 is rounded to the nearest whole metre.", NB + "m"))
    # 17
    its.append(mcq_txt("The water level in a rain barrel changed by " + H("-3/8") + NB + "m in week 1 and by " + H("-2/5") +
                       NB + "m in week 2. Which statement is true?", "The level dropped more in week 2.",
                       ["The level dropped more in week 1.", "The level dropped the same amount both weeks.",
                        "The level rose in week 2."],
                       H("-3/8") + " = " + M + "0.375 and " + H("-2/5") + " = " + M + "0.4. " + M + "0.400 is farther below "
                       "0 than " + M + "0.375, so <b>the level dropped more in week 2</b>."))
    assert V("-2/5") < V("-3/8")
    # 18
    its.append(mcq_txt("In March, Lake Ontario was 0.08" + NB + "m below its average level. In April, it was 0.12" + NB +
                       "m below. Which statement is true?", "April was lower: " + M + "0.12 &lt; " + M + "0.08.",
                       ["March was lower: " + M + "0.08 &lt; " + M + "0.12.",
                        "April was lower: " + M + "0.12 &gt; " + M + "0.08.", "Both months were at the same level."],
                       "Below average is negative: March " + M + "0.08, April " + M + "0.12. " + M + "0.12 is farther below "
                       "0, so <b>April was lower: " + M + "0.12 &lt; " + M + "0.08</b>."))
    # 19
    cities = [("Toronto", "-3.5"), ("Ottawa", "-8.25"), ("Montréal", "-8.5"), ("Halifax", "3.75")]
    right = [c for c, t in sorted(cities, key=lambda x: -V(x[1]))]
    assert right == ["Halifax", "Toronto", "Ottawa", "Montréal"]
    its.append(mcq_txt("One January afternoon the temperatures were: " + ", ".join("%s %s" % (c, deg(t)) for c, t in cities) +
                       ". Which list goes from warmest to coldest?", ", ".join(right),
                       ["Montréal, Ottawa, Toronto, Halifax", "Halifax, Toronto, Montréal, Ottawa",
                        "Toronto, Halifax, Ottawa, Montréal"],
                       "Warmest is the greatest number. 3.75 is the only positive temperature. Then " + M + "3.5, then " + M +
                       "8.25, and " + M + "8.5 = " + M + "8.50 is the coldest: <b>Halifax, Toronto, Ottawa, Montréal</b>."))
    # 20
    its.append(mcq_num("In gym class, Liam ran the 60" + NB + "m dash in 9.4" + NB + "s and Owen ran it in 9.5" + NB +
                       "s. Hana’s time was between their times. Which could be Hana’s time?", "9.45",
                       ["9.39", "9.51", "9.045"],
                       "Write them as 9.40 and 9.50. 9.45 is between them: <b>9.45" + NB + "s</b>. 9.045 is less than 9.4.",
                       NB + "s"))
    for w in ["9.39", "9.51", "9.045"]:
        assert not V("9.4") < V(w) < V("9.5")
    assert len(its) == 20
    return {"title": "Word problems: temperatures, lake levels and more", "items": its}


# ============================================================ lesson
def body_html():
    nl1 = NL(-1, 1, F(1, 4), F(1, 2), gap=40).point(F(-1, 2), "P").point(F(-1, 4), "Q")
    cmp_ = nl1.svg("number line from " + M + "1 to 1 counting by 0.25 with P at " + M + "0.5 and Q at " + M + "0.25")
    nl2 = NL(-2, 0, F(1, 3), 1, gap=45).point(F(-5, 3), "A")
    frac = nl2.svg("number line from " + M + "2 to 0 in thirds with A at " + M + "1 2/3")
    return (
        "<h2>Positive and negative fractions and decimals</h2>"
        "<p>Fractions and decimals can be negative too. On a number line, negative numbers are to the <b>left</b> of 0 "
        "(or <b>below</b> 0 on a vertical line, like a thermometer). " + M + "0.25 is read “negative twenty-five hundredths”.</p>"
        "<p>Before you read a point, find what each <b>space</b> is worth: the difference between two labels ÷ the number of "
        "spaces between them.</p>"
        "<figure class='sn-fig'>" + frac +
        "<figcaption>There are 3 spaces between whole numbers, so each space is " + H("1/3") + ". A is 2 spaces left of " + M +
        "1, so A = " + H("-1 2/3") + ", not " + H("-2/3") + ".</figcaption></figure>"
        "<h2>Compare and order</h2>"
        "<p>The farther <b>left</b> a number is, the <b>less</b> it is. For two negative numbers, the one closer to 0 is greater.</p>"
        "<figure class='sn-fig'>" + cmp_ +
        "<figcaption>P (" + M + "0.5) is to the left of Q (" + M + "0.25), so " + M + "0.5 &lt; " + M + "0.25. "
        "0.5 is more than 0.25, but " + M + "0.5 is less than " + M + "0.25.</figcaption></figure>"
        "<p>To compare decimals, give them the same number of places: 0.5 = 0.50 &gt; 0.45. "
        "To compare fractions, use a common denominator or write them as decimals: " + H("3/8") + " = 3 ÷ 8 = 0.375.</p>" +
        ex("Example 1", "Order from least to greatest: " + M + "0.5, " + H("-3/4") + ", 0.4, " + M + "0.25",
           H("-3/4") + " = " + M + "0.75. Start with the number farthest from 0 on the left: " + M + "0.75, then " + M +
           "0.5, then " + M + "0.25, then 0.4.",
           H("-3/4") + ", " + M + "0.5, " + M + "0.25, 0.4") +
        "<h2>Simplify fractions</h2>"
        "<p>Divide the numerator and the denominator by their <b>greatest common factor</b> (GCF). The fraction keeps its value.</p>" +
        ex("Example 2", "Write " + H("18/24") + " in simplest form.",
           "The GCF of 18 and 24 is 6. 18 ÷ 6 = 3 and 24 ÷ 6 = 4. (Dividing by 2 gives " + H("9/12") +
           ", which is not yet in simplest form.)", H("3/4")) +
        "<h2>Numbers in between</h2>"
        "<p>There is always another number between two different numbers. Add a zero to get more places, then pick a number "
        "in the middle.</p>" +
        ex("Example 3", "Find a number between " + M + "0.5 and " + M + "0.4.",
           "Write " + M + "0.50 and " + M + "0.40. Any number of hundredths from 41 to 49, with the minus sign, is between them.",
           M + "0.45 (or " + M + "0.42, " + M + "0.48, …)") +
        "<h2>Round decimals</h2>"
        "<p>Look at the digit one place to the right of the place you are rounding to. <b>5 or more</b>: round up. "
        "<b>4 or less</b>: round down. For a negative number, round it as if it were positive, then keep the minus sign.</p>" +
        table(["Round", "Look at", "Answer"], [
            ["3.648 to the nearest hundredth", "the thousandths digit: 8", "3.65"],
            [M + "2.46 to the nearest tenth", "the hundredths digit: 6", M + "2.5"],
            ["12.49 to the nearest whole number", "the tenths digit: 4", "12"],
            [M + "17.6" + NB + "°C to the nearest degree", "the tenths digit: 6", M + "18" + NB + "°C"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            [M + "0.5 &gt; " + M + "0.25 because 0.5 &gt; 0.25", "Farther left is less: " + M + "0.5 &lt; " + M + "0.25"],
            ["0.45 &gt; 0.5 because it has more digits", "Use the same number of places: 0.45 &lt; 0.50"],
            ["Counting tick marks instead of spaces", "Count the spaces between labels: 4 spaces means fourths"],
            ["Simplifying only the numerator: " + H("12/18") + " → " + H("2/18"), "Divide both parts by the GCF: " + H("2/3")],
            ["Rounding twice: 12.49 → 12.5 → 13", "Round the number you started with: 12"],
        ])
    )


FAQ = [
    {"q": "What do Grade 7 students learn about fractions and decimals in the Ontario math curriculum?",
     "a": "Grade 7 students read, represent, compare and order positive and negative fractions and decimals to thousandths. They also simplify fractions, find a number between any two numbers, and round decimals to the nearest tenth, hundredth or whole number."},
    {"q": "Is −0.5 greater than −0.25?",
     "a": "No. −0.5 is farther left on the number line, so −0.5 < −0.25, just as −0.5 °C is colder than −0.25 °C."},
    {"q": "How do you simplify a fraction?",
     "a": "Divide the numerator and the denominator by their greatest common factor. For 18/24 the greatest common factor is 6, so 18/24 = 3/4."},
    {"q": "How do you round a negative decimal?",
     "a": "Round it as if it were positive, then keep the minus sign. −2.46 rounded to the nearest tenth is −2.5, because 2.46 rounds to 2.5."},
]


def gen_unit():
    rnd = random.Random(47803)
    sets = [set_numberline(rnd), set_compare(rnd), set_simplify(rnd), set_between_round(rnd), set_words(rnd)]
    for s in sets:
        for it in s["items"]:
            if not it.get("fixed"):
                it["_c"] = it["c"][it["a"]]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len({plain(c) for c in it["c"]}) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1
            k = plain(it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-7", "slug": "comparing-fractions-and-decimals", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Comparing Fractions and Decimals: Positive and Negative Numbers, Simplifying and Rounding",
        "seo_title": "Grade 7 Comparing Fractions and Decimals Worksheets: Negative Numbers, Simplifying, Rounding (Free, Answer Key)",
        "short_title": "Comparing fractions and decimals",
        "domain": "Number",
        "standard_code": "Grade 7: B1.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Read, represent, compare, and order positive and negative fractions and decimal numbers to thousandths, in various contexts",
        "meta_desc": "Free Grade 7 math worksheets for the Ontario curriculum: positive and negative fractions and decimals on a number line, comparing and ordering, simplifying fractions, numbers between two quantities, and rounding. 100 questions with an answer key.",
        "key_big": "The farther left on the number line, the less the number, so −0.5 < −0.25.",
        "key_sub": "Compare decimals place by place, not by length: 0.5 = 0.50 > 0.45. Simplify a fraction by dividing both parts by their greatest common factor.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(number line|vertical|thermometer)")
    os.makedirs(OUT, exist_ok=True)
    path_ = os.path.join(OUT, u["slug"] + ".json")
    with open(path_, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path_)
