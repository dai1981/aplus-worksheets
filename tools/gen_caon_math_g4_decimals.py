# -*- coding: utf-8 -*-
"""
Ontario Grade 4 Math: Decimal tenths (Ontario Curriculum 2020, B1.7, B1.9, B2.3)
  python3 tools/gen_caon_math_g4_decimals.py
Tenth strips, number lines and place value charts are drawn from whole numbers of tenths (24 = 2.4).
Every answer is checked with fractions.Fraction / decimal.Decimal (never float).
Canadian English, metric units. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal as Dm
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-4")
UPDATED = "2026-11-02"
FILL = "#4fae74"
LINE = "#2b2b2b"
RED = "#d6453b"
BLUE = "#2f6fb5"
GREEN = "#006633"
HEADFILL = "#cfe6d6"
FONT = "Arial, Helvetica, sans-serif"


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def mixed(w, a, b):
    return "%d %s" % (w, fr(a, b))


def D(t):
    """Decimal text for t tenths: 3 -> '0.3', 24 -> '2.4', 10 -> '1'."""
    s = format((Dm(t) / 10).normalize(), "f")
    assert F(Dm(s)) == F(t, 10)
    return s


def V(s):
    return F(Dm(s))


FRX = re.compile(r"^<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>( .+)?$")
NUM = re.compile(r"^(\d*\.?\d+)( [a-zA-Z]+)?$")


def val(c):
    """(value, unit) of a choice. None for choices that are not one number."""
    m = FRX.match(c)
    if m:
        return (F(int(m.group(1)), int(m.group(2))), (m.group(3) or "").strip())
    m = NUM.match(c)
    if not m:
        return None
    return (F(Dm(m.group(1))), (m.group(2) or "").strip())


def mcq(q, correct, wrong, e, same_ok=False):
    """4 choices: correct first + 3 wrong. No two choices may have the same value (0.1 vs 0.10)."""
    correct = str(correct)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [correct] + wrong
    assert len(set(re.sub(r"<[^>]+>", "", x) for x in ch)) == 4, (q, ch)
    if not same_ok:
        vs = [val(x) for x in ch]
        known = [v for v in vs if v is not None]
        assert len(set(known)) == len(known), (q, ch)
    return {"q": q, "c": ch, "a": 0, "e": e}


def fixed(q, choices, a, e):
    """Choices are picture labels (A, B, C, D): keep this order; the answer position is fixed."""
    assert len(set(choices)) == 4
    return {"q": q, "c": list(choices), "a": a, "e": e, "fix": True}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        for it in s["items"]:
            if it.get("fix"):
                targets.remove(it["a"])
        rnd.shuffle(targets)
        k = 0
        for it in s["items"]:
            if it.get("fix"):
                continue
            t = targets[k]
            k += 1
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        for it in s["items"]:
            it.pop("fix", None)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    assert "'" not in label
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


def tw(t):
    return "1 tenth" if t == 1 else "%d tenths" % t


# ------------------------------------------------------------ pictures
def strip_body(n, k, ox, oy, W=300, H=40):
    """One strip split into n equal parts, the first k shaded."""
    s = []
    for i in range(n):
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (ox + W * i / float(n), oy, W / float(n), H, FILL if i < k else "#fff", LINE))
    return "".join(s)


def strips_svg(t, W=300, H=40, gap=12):
    """Tenth strips: each strip is 1 whole split into 10 equal parts; t tenths shaded in total (full strips first)."""
    n = max(1, (t + 9) // 10)
    body = "".join(strip_body(10, min(10, t - 10 * i), 6, 6 + i * (H + gap), W, H) for i in range(n))
    return svg_wrap(W + 12, n * H + (n - 1) * gap + 12, body,
                    "tenth strip%s split into 10 equal parts with %d parts shaded" % ("s" if n > 1 else "", t))


def strips_abcd_svg(spec, W=260, H=30, gap=14):
    """Four strips labelled A-D, all the same length. spec: (parts, shaded) for each strip."""
    o = []
    for i, (n, k) in enumerate(spec):
        y = 6 + i * (H + gap)
        o.append(text(14, y + H / 2.0 + 6, "ABCD"[i], 18))
        o.append(strip_body(n, k, 34, y, W, H))
    return svg_wrap(34 + W + 6, 12 + 4 * H + 3 * gap, "".join(o), "four strips labelled A, B, C and D")


def fifths_tenths_svg(k5, W=300, H=36, gap=14):
    """A strip in 5 equal parts (k5 shaded) above an empty strip in 10 equal parts of the same size."""
    o = [strip_body(5, k5, 6, 6, W, H), strip_body(10, 0, 6, 6 + H + gap, W, H)]
    return svg_wrap(W + 12, 12 + 2 * H + gap, "".join(o),
                    "two strips of the same size: one in 5 equal parts with %d shaded, one in 10 equal parts" % k5)


def line_svg(a, b, spaces, labels=None, dots=(), W=420, flabels=None):
    """Number line from a to b tenths with `spaces` equal spaces.
    labels: tenths values written under the line (default both ends). flabels: {value: text} for other label text.
    dots: (value, letter or None)."""
    labels = labels if labels is not None else [a, b]
    flabels = flabels or {}
    lettered = any(l for _, l in dots)
    L, R = 30, W - 30
    Y = 46 if lettered else 30
    assert (b - a) * 10 % spaces == 0 or True
    step = F(b - a, spaces)

    def X(v):
        return L + (R - L) * float(F(v - a) / (b - a))
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for i in range(spaces + 1):
        v = a + i * step
        big = v in labels
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(v), Y - (13 if big else 8), X(v), Y + (13 if big else 8), LINE, "2.5" if big else "1.8"))
    for v in labels:
        assert F(v - a) % step == 0
        s.append(text(X(v), Y + 36, flabels.get(v, D(v)), 17))
    xs = []
    for v, l in dots:
        assert a <= v <= b and F(v - a) % step == 0
        xs.append(X(v))
        s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X(v), Y, BLUE if l else RED))
        if l:
            s.append(text(X(v), Y - 20, l, 18))
    xs.sort()
    assert all(q - p >= 20 for p, q in zip(xs, xs[1:])), (a, b, dots)
    lab = "number line from %s to %s split into %d equal spaces" % (D(a), D(b), spaces)
    if lettered:
        lab += " with points %s" % ", ".join(l for _, l in dots)
    return svg_wrap(W, Y + 46, "".join(s), lab)


PV = [(1, "Tens"), (0, "Ones"), (-1, "Tenths")]


def chart_svg(s, hi=None):
    """Place value chart: (Tens) | Ones | . | Tenths. hi: place drawn in red."""
    w, _, f = s.partition(".")
    tens = len(w) > 1
    cols = PV if tens else PV[1:]
    CW, PW, HEAD, ROW = 100, 16, 30, 44
    x0, y0 = 6, 6
    W = 2 * x0 + len(cols) * CW + PW
    H = 2 * y0 + HEAD + ROW
    xs, x = {}, x0
    for p, _ in cols:
        xs[p] = x
        x += CW + (PW if p == 0 else 0)
    px = xs[0] + CW
    o = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0, y0, W - 2 * x0, HEAD + ROW, GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, W - 2 * x0, HEAD, HEADFILL)]
    for p, name in cols:
        if p != cols[0][0]:
            o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                     % (xs[p], y0, xs[p], y0 + HEAD + ROW, GREEN))
        o.append(text(xs[p] + CW / 2.0, y0 + 20, name, 14))
    o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
             % (px + PW, y0, px + PW, y0 + HEAD + ROW, GREEN))
    o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + HEAD, W - x0, y0 + HEAD, GREEN))
    yb = y0 + HEAD
    assert len(w) <= 2 and len(f) == 1, s
    digits = {}
    for j, ch in enumerate(w):
        digits[len(w) - 1 - j] = ch
    digits[-1] = f
    for p, ch in digits.items():
        o.append(text(xs[p] + CW / 2.0, yb + 32, ch, 28, col=RED if hi == p else LINE, weight=800))
    o.append("<circle cx='%.1f' cy='%d' r='4.5' fill='%s'/>" % (px + PW / 2.0, yb + 31, LINE))
    return svg_wrap(W, H, "".join(o), "place value chart showing %s" % s)


# ============================================================ set 1: tenths with strips and number lines
def set_tenths():
    its = []
    for k, wrong in [(3, ["0.03", "3.10", "0.7"]), (7, ["0.07", "7.10", "0.3"]), (5, ["0.05", "5.10", "5"])]:
        e = ("The strip is 1 whole split into 10 equal parts, so each part is 1 tenth. %d parts are shaded: "
             "%s = <b>%s</b>. Tenths go in the <b>first</b> place after the decimal point." % (k, fr(k, 10), D(k)))
        if k == 3:
            e += " 3.10 mixes up the fraction and the decimal: it means 3 wholes and more."
        if k == 7:
            e += " 0.3 is the part that is <b>not</b> shaded."
        if k == 5:
            e += " 5 would mean 5 whole strips."
        its.append(mcq(fig(strips_svg(k)) + "The strip is 1 whole. What decimal is shaded?", D(k), wrong, e))
    its.append(mcq("1 whole is split into 10 equal parts. What decimal is each part?", "0.1", ["1.10", "10", "1"],
                   "Each part is %s of the whole, one <b>tenth</b>: <b>0.1</b>. "
                   "1.10 is a mistake from writing the 1 and the 10 of %s with a point between them." % (fr(1, 10), fr(1, 10))))
    its.append(mcq("How many tenths make <b>1 whole</b>?", "10", ["100", "1", "5"],
                   "1 whole split into 10 equal parts: %s = 1. So <b>10</b> tenths make 1 whole." % fr(10, 10)))
    its.append(mcq("Which decimal is <b>4 tenths</b>?", "0.4", ["4", "0.04", "4.10"],
                   "4 tenths = %s. Write 0, the decimal point, then 4 in the tenths place: <b>0.4</b>. "
                   "4 would be 4 wholes." % fr(4, 10)))
    its.append(fixed(fig(strips_abcd_svg([(10, 4), (10, 6), (6, 1), (12, 6)])) +
                     "All four strips are the same size. Which strip shows <b>0.6</b>?", ["A", "B", "C", "D"], 1,
                     "0.6 is 6 tenths, so the strip must have <b>10 equal parts</b> with 6 shaded: strip <b>B</b>. "
                     "A shows 0.4. C shows %s. D has 6 shaded, but it has 12 parts, so it shows one half."
                     % fr(1, 6)))
    its.append(mcq(fig(strips_svg(6)) + "The strip is 1 whole. What decimal is <b>not</b> shaded?", "0.4",
                   ["0.6", "0.04", "4"],
                   "6 of the 10 parts are shaded, so 10 − 6 = 4 parts are not shaded: %s = <b>0.4</b>. "
                   "0.6 is the shaded part." % fr(4, 10)))
    its.append(mcq(fig(line_svg(0, 10, 10, dots=[(3, None)])) + "What decimal is at the red dot?", "0.3",
                   ["0.03", "3", "0.7"],
                   "The line from 0 to 1 has <b>10 equal spaces</b>, so each space is 1 tenth (0.1). "
                   "The dot is 3 spaces after 0: <b>0.3</b>."))
    its.append(mcq(fig(line_svg(0, 10, 10, dots=[(8, None)])) + "What decimal is at the red dot?", "0.8",
                   ["0.08", "8", "0.2"],
                   "Each of the 10 spaces is 0.1. The dot is 8 spaces after 0: <b>0.8</b>. "
                   "(0.2 counts the 2 spaces back from 1, the wrong end.)"))
    its.append(mcq(fig(line_svg(0, 10, 10, labels=[0, 5, 10], dots=[(7, None)])) + "What decimal is at the red dot?", "0.7",
                   ["0.07", "0.2", "7"],
                   "Each space is 0.1. The dot is 2 spaces after 0.5: 0.5, 0.6, <b>0.7</b>. "
                   "0.2 counts only the spaces after 0.5."))
    its.append(mcq(fig(line_svg(0, 10, 10, dots=[(1, None)])) + "What decimal is at the red dot?", "0.1",
                   ["0.01", "1", "0.9"],
                   "The dot is 1 space after 0. Each space is 1 tenth: <b>0.1</b>. 1 is the end of the line."))
    its.append(mcq(fig(line_svg(0, 10, 10, dots=[(5, None)])) + "The red dot is halfway between 0 and 1. What decimal is it at?",
                   "0.5", ["0.05", "0.2", "5"],
                   "The dot is 5 spaces after 0, and each space is 0.1: <b>0.5</b>. "
                   "0.2 comes from the 2 in one half (%s), but one half is 5 tenths." % fr(1, 2)))
    its.append(fixed(fig(line_svg(0, 10, 10, dots=[(2, "A"), (4, "B"), (6, "C"), (9, "D")])) +
                     "Which point is at <b>0.4</b>?", ["A", "B", "C", "D"], 1,
                     "Each space is 0.1. Count 4 spaces from 0: point <b>B</b>. A is 0.2, C is 0.6 and D is 0.9."))
    its.append(fixed(fig(line_svg(0, 10, 10, dots=[(1, "A"), (3, "B"), (5, "C"), (8, "D")])) +
                     "Which point is at <b>0.8</b>?", ["A", "B", "C", "D"], 3,
                     "Each space is 0.1. Count 8 spaces from 0 (or 2 back from 1): point <b>D</b>. "
                     "A is 0.1, B is 0.3 and C is 0.5."))
    its.append(mcq("Count on in tenths. What comes next?<br><b>0.4, 0.5, 0.6, ?</b>", "0.7", ["0.61", "7", "0.8"],
                   "Each step adds 1 tenth: 6 tenths + 1 tenth = 7 tenths = <b>0.7</b>. 0.8 skips a number."))
    its.append(mcq("Count on in tenths. What comes next?<br><b>0.7, 0.8, 0.9, ?</b>", "1", ["0.10", "0.91", "10"],
                   "9 tenths and 1 more make 10 tenths, which is <b>1</b> whole (1.0). "
                   "0.10 is <b>not</b> next: 0.10 is the same as 0.1, which is far back near 0."))
    its.append(mcq("Count back in tenths. What comes next?<br><b>1, 0.9, 0.8, ?</b>", "0.7", ["0.07", "1.1", "0.6"],
                   "Each step takes away 1 tenth: 8 tenths − 1 tenth = 7 tenths = <b>0.7</b>. "
                   "1.1 counts up, and 0.6 skips a number."))
    its.append(mcq("Kai’s granola bar has 10 equal pieces. He eats 7 pieces. What decimal of the bar is <b>left</b>?",
                   "0.3", ["0.7", "0.03", "3"],
                   "10 − 7 = 3 pieces are left. Each piece is 1 tenth, so %s of the bar is left: <b>0.3</b>. "
                   "0.7 is the part he ate." % fr(3, 10)))
    its.append(mcq("A garden has 10 equal rows. Maya plants carrots in 2 rows and beans in 5 rows. "
                   "What decimal of the garden is planted?", "0.7", ["0.25", "0.3", "7"],
                   "2 + 5 = 7 of the 10 rows are planted: %s = <b>0.7</b>. 0.3 is the part with no plants." % fr(7, 10)))
    assert len(its) == 20, len(its)
    return {"title": "Tenths with strips and number lines", "items": its}


# ============================================================ set 2: decimals greater than 1
def set_greater():
    its = []
    for t, wrong in [(12, ["0.12", "12", "2.1"]), (23, ["0.23", "23", "3.2"]), (31, ["0.31", "31", "1.3"])]:
        w, d = divmod(t, 10)
        e = ("Each strip is 1 whole. %d whole %s shaded (%d) and %s of the last strip: %d and %s = <b>%s</b>. "
             "%s would be less than 1."
             % (w, "strip is" if w == 1 else "strips are", w, tw(d), w, fr(d, 10), D(t), wrong[0]))
        its.append(mcq(fig(strips_svg(t)) + "Each strip is 1 whole. What decimal is shaded?", D(t), wrong, e))
    its.append(mcq("Write %s as a decimal." % mixed(2, 7, 10), "2.7", ["2.07", "27", "7.2"],
                   "2 wholes, then the decimal point, then 7 tenths in the first place after the point: <b>2.7</b>. "
                   "2.07 puts the 7 one place too far to the right."))
    its.append(mcq("Write %s as a decimal." % mixed(5, 3, 10), "5.3", ["3.5", "53", "5.03"],
                   "The whole number goes before the point and the tenths after it: <b>5.3</b>. 3.5 swaps them."))
    its.append(mcq("Which decimal is <b>4 ones and 6 tenths</b>?", "4.6", ["6.4", "46", "0.46"],
                   "Ones go before the decimal point and tenths go right after it: <b>4.6</b>."))
    its.append(mcq("How many tenths are there in <b>3.2</b>?", "32", ["2", "3", "320"],
                   "1 whole = 10 tenths, so 3 wholes = 30 tenths. 30 + 2 = <b>32</b> tenths. "
                   "(2 is only the digit in the tenths place.)"))
    its.append(mcq("How many tenths are there in <b>1.5</b>?", "15", ["5", "1", "51"],
                   "1 whole = 10 tenths. 10 + 5 = <b>15</b> tenths. (5 is only the digit in the tenths place.)"))
    its.append(mcq("<b>26 tenths</b> is the same as which decimal?", "2.6", ["26", "0.26", "20.6"],
                   "10 tenths make 1 whole, so 20 tenths make 2 wholes. 26 tenths = 2 wholes and 6 tenths = <b>2.6</b>."))
    its.append(mcq(fig(chart_svg("7.3", hi=-1)) + "What is the value of the red digit in 7.3?", "3 tenths",
                   ["3 ones", "3 tens", "3 hundreds"],
                   "The red 3 is in the first place after the decimal point, the tenths column. "
                   "Its value is <b>3 tenths</b> = 0.3.", same_ok=True))
    its.append(mcq(fig(chart_svg("25.8", hi=0)) + "What is the value of the red digit in 25.8?", "5 ones",
                   ["5 tenths", "5 tens", "5 hundreds"],
                   "The red 5 is just before the decimal point, in the ones column. Its value is <b>5 ones</b> = 5.", same_ok=True))
    its.append(mcq("What is the value of the digit <b>6</b> in <b>46.9</b>?", "6", ["0.6", "60", "600"],
                   "In 46.9 the 6 is just before the decimal point, in the ones place. It is worth <b>6</b>."))
    its.append(mcq("What is the value of the digit <b>4</b> in <b>13.4</b>?", "0.4", ["4", "40", "400"],
                   "In 13.4 the 4 is right after the decimal point, in the tenths place. It is worth 4 tenths = <b>0.4</b>."))
    its.append(mcq(fig(line_svg(20, 30, 10, dots=[(26, None)])) + "What decimal is at the red dot?", "2.6",
                   ["0.6", "2.06", "2.4"],
                   "The line goes from 2 to 3 with 10 equal spaces, so each space is 0.1. "
                   "The dot is 6 spaces after 2: <b>2.6</b>. (2.4 counts back from 3, the wrong end.)"))
    its.append(mcq(fig(line_svg(40, 60, 20, labels=[40, 50, 60], dots=[(53, None)])) + "What decimal is at the red dot?",
                   "5.3", ["5.03", "5.7", "4.3"],
                   "Between 4 and 5 there are 10 spaces, so each space is 0.1. The dot is 3 spaces after 5: <b>5.3</b>. "
                   "5.7 counts back from 6."))
    its.append(fixed(fig(line_svg(10, 30, 20, labels=[10, 20, 30], dots=[(14, "A"), (16, "B"), (24, "C"), (28, "D")])) +
                     "Which point is at <b>2.4</b>?", ["A", "B", "C", "D"], 2,
                     "2.4 is 4 tenths after 2. Count 4 spaces to the right of 2: point <b>C</b>. "
                     "A is 1.4 (4 tenths after 1), B is 1.6 and D is 2.8."))
    its.append(mcq("Count on in tenths. What comes next?<br><b>1.7, 1.8, 1.9, ?</b>", "2", ["1.10", "1.91", "1"],
                   "1.9 + 0.1: 9 tenths and 1 more make 10 tenths, which is 1 more whole. So 1 whole becomes 2: "
                   "the next number is <b>2</b> (or 2.0). 1.10 is the same as 1.1."))
    its.append(mcq("Count back in tenths. What comes next?<br><b>3.2, 3.1, 3, ?</b>", "2.9", ["3.9", "2.1", "29"],
                   "3 is the same as 30 tenths. 1 tenth less is 29 tenths: 2 wholes and 9 tenths = <b>2.9</b>. "
                   "3.9 is much bigger than 3."))
    its.append(mcq("Owen’s ribbon is 2 m and 5 tenths of a metre long. How long is it as a decimal?", "2.5 m",
                   ["25 m", "0.25 m", "5.2 m"],
                   "2 whole metres and %s of a metre: <b>2.5 m</b>." % fr(5, 10)))
    its.append(mcq("Each pizza at the class party is cut into 10 equal slices. There are 3 whole pizzas "
                   "and 7 slices left. What decimal shows the pizza left?", "3.7", ["37", "0.37", "7.3"],
                   "3 whole pizzas and 7 tenths of a pizza: %s = <b>3.7</b> pizzas. 7.3 swaps the wholes and the tenths."
                   % mixed(3, 7, 10)))
    assert V("2") - V("0.1") == V("1.9") and V("3") - V("0.1") == V("2.9")
    assert len(its) == 20, len(its)
    return {"title": "Decimals greater than 1", "items": its}


# ============================================================ set 3: compare and order tenths
def cmp_item(x, y, e):
    a, b = V(x), V(y)
    lt, gt, eq = "%s &lt; %s" % (x, y), "%s &gt; %s" % (x, y), "%s = %s" % (x, y)
    right = lt if a < b else gt if a > b else eq
    wrong = [c for c in (lt, gt, eq) if c != right] + ["You can’t tell"]
    return mcq("Compare the decimals.", right, wrong, e, same_ok=True)


def set_compare():
    its = []
    its.append(cmp_item("0.3", "0.7", "Both have 0 ones. Compare the tenths: 3 tenths &lt; 7 tenths. So <b>0.3 &lt; 0.7</b>."))
    its.append(cmp_item("6.5", "6.7", "Both have 6 ones. Compare the tenths: 5 tenths &lt; 7 tenths. So <b>6.5 &lt; 6.7</b>."))
    its.append(cmp_item("1.4", "0.9", "Compare the ones first: 1.4 has 1 one and 0.9 has 0 ones. So <b>1.4 &gt; 0.9</b>, "
                        "even though 9 &gt; 4."))
    its.append(cmp_item("4.1", "3.9", "Compare the ones first: 4 &gt; 3. So <b>4.1 &gt; 3.9</b>. The tenths only matter "
                        "when the ones are the same."))
    its.append(cmp_item("0.9", "0.10", "0.10 is the same as 0.1 (a 0 at the end does not change the value). "
                        "9 tenths &gt; 1 tenth, so <b>0.9 &gt; 0.10</b>. Do not compare 9 with 10."))
    its.append(cmp_item("12.3", "9.8", "12.3 has 12 wholes and 9.8 has only 9 wholes. So <b>12.3 &gt; 9.8</b>."))
    its.append(mcq("Which number is <b>greater than 2.5</b>?", "3.1", ["1.9", "2.4", "0.8"],
                   "3.1 has 3 ones, more than the 2 ones in 2.5. So <b>3.1</b> &gt; 2.5. "
                   "1.9 is smaller even though 9 &gt; 5: it has only 1 one."))
    its.append(mcq("Which decimal is the <b>greatest</b>?", "1.2", ["0.9", "1.1", "0.10"],
                   "0.9 and 0.10 have 0 ones. 1.1 and 1.2 both have 1 one; compare the tenths: 2 &gt; 1. "
                   "So <b>1.2</b> is the greatest. (0.10 = 0.1.)"))
    its.append(mcq("Which decimal is the <b>smallest</b>?", "2.7", ["3.1", "2.9", "7.2"],
                   "2.7 and 2.9 have the fewest ones (2). Compare their tenths: 7 &lt; 9. So <b>2.7</b> is the smallest."))
    its.append(mcq("Which number is <b>between 1.4 and 1.8</b>?", "1.6", ["1.3", "1.9", "4.1"],
                   "Count on in tenths from 1.4: 1.5, <b>1.6</b>, 1.7, then 1.8. 1.3 is less than 1.4 and 1.9 is more than 1.8."))
    its.append(mcq("Which statement is <b>true</b>?", "4.2 &lt; 4.7", ["0.9 &lt; 0.10", "5.3 &gt; 5.8", "2.9 &gt; 3.1"],
                   "4.2 and 4.7 both have 4 ones, and 2 tenths &lt; 7 tenths. So <b>4.2 &lt; 4.7</b> is true. "
                   "0.9 &lt; 0.10 is false because 0.10 = 0.1.", same_ok=True))
    its.append(mcq("Which number is <b>closest to 1</b>?", "0.9", ["0.1", "0.5", "1.9"],
                   "0.9 is just 1 tenth less than 1. 0.5 is 5 tenths away, and 0.1 and 1.9 are 9 tenths away. "
                   "So <b>0.9</b> is the closest."))
    for nums, right, wrong, how, e in [
        (["0.8", "0.3", "0.5"], "0.3, 0.5, 0.8", ["0.8, 0.5, 0.3", "0.3, 0.8, 0.5", "0.5, 0.3, 0.8"], "smallest to greatest",
         "All have 0 ones. Compare the tenths: 3, 5 and 8. Order: <b>0.3, 0.5, 0.8</b>."),
        (["1.2", "0.9", "2.1"], "0.9, 1.2, 2.1", ["1.2, 2.1, 0.9", "2.1, 1.2, 0.9", "0.9, 2.1, 1.2"], "smallest to greatest",
         "Compare the ones first: 0.9 has 0, 1.2 has 1 and 2.1 has 2. Order: <b>0.9, 1.2, 2.1</b>. "
         "0.9 is not the biggest just because 9 is a big digit."),
        (["3.4", "4.3", "3.9"], "4.3, 3.9, 3.4", ["3.4, 3.9, 4.3", "3.9, 4.3, 3.4", "4.3, 3.4, 3.9"], "greatest to smallest",
         "4.3 has the most ones, so it is the greatest. 3.9 &gt; 3.4 (9 tenths &gt; 4 tenths). "
         "Order: <b>4.3, 3.9, 3.4</b>. Careful: the question asks for greatest first."),
        (["0.9", "0.10", "0.5"], "0.10, 0.5, 0.9", ["0.5, 0.9, 0.10", "0.9, 0.5, 0.10", "0.10, 0.9, 0.5"], "smallest to greatest",
         "0.10 is the same as 0.1, just 1 tenth. Compare the tenths: 1, 5 and 9. Order: <b>0.10, 0.5, 0.9</b>. "
         "0.10 is not the biggest just because 10 is a bigger number than 9."),
    ]:
        vs = sorted((V(x) for x in nums), reverse=how.startswith("greatest"))
        assert [V(x) for x in right.split(", ")] == vs, right
        its.append(mcq("Order from <b>%s</b>: <b>%s</b>" % (how, ", ".join(nums)), right, wrong, e, same_ok=True))
    its.append(fixed(fig(line_svg(0, 20, 20, labels=[0, 10, 20], dots=[(3, "A"), (8, "B"), (13, "C"), (17, "D")])) +
                     "Which point is at <b>1.3</b>?", ["A", "B", "C", "D"], 2,
                     "1.3 is 3 tenths after 1. Count 3 spaces to the right of 1: point <b>C</b>. "
                     "A is 0.3, B is 0.8 and D is 1.7."))
    its.append(mcq("In the 60 m dash on track and field day, Chloe runs it in 9.8 seconds and Arjun runs it in "
                   "10.2 seconds. Who is faster?", "Chloe", ["Arjun", "They are equally fast", "You can’t tell"],
                   "In a race, the <b>shorter</b> time is faster. 9.8 has 9 wholes and 10.2 has 10 wholes, so 9.8 &lt; 10.2. "
                   "<b>Chloe</b> is faster.", same_ok=True))
    its.append(mcq("Three bean plants in Ms. Patel’s class are 4.5 cm, 5.4 cm and 4.9 cm tall. "
                   "How tall is the <b>tallest</b> plant?", "5.4 cm", ["4.9 cm", "4.5 cm", "You can’t tell"],
                   "5.4 has 5 whole centimetres; the others have only 4. So <b>5.4 cm</b> is the tallest, "
                   "even though 4.9 has a 9."))
    its.append(mcq("In the long jump, Liam jumps 2.7 m, Noah jumps 2.9 m and Kai jumps 2.3 m. Who jumps the farthest?",
                   "Noah", ["Liam", "Kai", "They jump the same"],
                   "All three jumps are 2 whole metres. Compare the tenths: 9 &gt; 7 &gt; 3. So <b>Noah</b> jumps the farthest.",
                   same_ok=True))
    order = [0, 1, 2, 3, 4, 5, 6, 9, 11, 12, 13, 7, 8, 10, 16, 14, 15, 17, 18, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Compare and order tenths", "items": its}


# ============================================================ set 4: fractions and decimal tenths
def set_fractions():
    its = []
    for n, wrong in [(3, ["0.03", "3.10", "3"]), (9, ["0.09", "9.10", "0.1"]), (6, ["0.06", "6.10", "0.4"])]:
        e = "%s is %s. Tenths go in the <b>first</b> place after the decimal point: <b>%s</b>." % (fr(n, 10), tw(n), D(n))
        e += {3: " 3.10 just writes the 3 and the 10 with a point between them.",
              9: " 0.09 puts the 9 one place too far to the right.",
              6: " 0.4 is the part that is left (4 tenths)."}[n]
        its.append(mcq("Write %s as a decimal." % fr(n, 10), D(n), wrong, e))
    its.append(mcq("Which fraction is equal to <b>0.3</b>?", fr(3, 10), [fr(1, 3), fr(3, 1), fr(7, 10)],
                   "0.3 has one digit after the point, so it means tenths: 3 tenths = <b>%s</b>. "
                   "It is not %s: that would be 1 out of 3 equal parts." % (fr(3, 10), fr(1, 3))))
    its.append(mcq("Which fraction is equal to <b>0.8</b>?", fr(8, 10), [fr(1, 8), fr(8, 1), fr(2, 10)],
                   "One digit after the point means tenths: 0.8 = 8 tenths = <b>%s</b>. %s is 0.2, the part that is left."
                   % (fr(8, 10), fr(2, 10))))
    its.append(mcq("Which fraction is equal to <b>0.5</b>?", fr(5, 10), [fr(1, 5), fr(5, 1), fr(1, 10)],
                   "0.5 = 5 tenths = <b>%s</b> (which is also %s). It is <b>not</b> %s: one fifth is only 0.2."
                   % (fr(5, 10), fr(1, 2), fr(1, 5))))
    assert F(1, 5) == V("0.2") and F(1, 2) == V("0.5")
    its.append(mcq("Which decimal is equal to %s?" % fr(1, 2), "0.5", ["1.2", "0.2", "0.12"],
                   "Cut a whole into 10 equal parts: half of them is 5 parts. %s = %s = <b>0.5</b>. "
                   "1.2 and 0.12 just copy the digits 1 and 2." % (fr(1, 2), fr(5, 10))))
    its.append(mcq("Which decimal is equal to %s?" % fr(1, 5), "0.2", ["0.5", "1.5", "0.15"],
                   "Cut a whole into 10 equal parts. 1 fifth of them is 2 parts: %s = %s = <b>0.2</b>. "
                   "0.5 is a common mistake: 0.5 is one half, not one fifth." % (fr(1, 5), fr(2, 10))))
    its.append(mcq("Which one is <b>not</b> equal to 0.5?", fr(1, 5), [fr(5, 10), fr(1, 2), "five tenths"],
                   "0.5 = five tenths = %s = %s. But %s = %s = 0.2, so <b>%s</b> is not equal to 0.5."
                   % (fr(5, 10), fr(1, 2), fr(1, 5), fr(2, 10), fr(1, 5)), same_ok=True))
    its.append(mcq(fig(fifths_tenths_svg(2)) + "The two strips are the same size. What decimal of the top strip is shaded?",
                   "0.4", ["0.2", "2.5", "0.25"],
                   "The top strip is in 5 equal parts, so each part is %s. Each fifth covers 2 tenths of the bottom strip. "
                   "2 fifths = 4 tenths: %s = %s = <b>0.4</b>. 0.2 counts the parts but forgets they are fifths."
                   % (fr(1, 5), fr(2, 5), fr(4, 10))))
    assert F(2, 5) == V("0.4")
    its.append(mcq("Which mixed number is equal to <b>1.7</b>?", mixed(1, 7, 10), [mixed(7, 1, 10), mixed(1, 1, 7), fr(7, 10)],
                   "1.7 = 1 whole and 7 tenths = <b>%s</b>. %s forgets the whole." % (mixed(1, 7, 10), fr(7, 10)), same_ok=True))
    its.append(mcq("Which mixed number is equal to <b>3.5</b>?", mixed(3, 5, 10), [mixed(3, 1, 5), mixed(5, 3, 10), fr(3, 5)],
                   "3.5 = 3 wholes and 5 tenths = <b>%s</b>. %s is wrong: 0.5 is %s, not %s."
                   % (mixed(3, 5, 10), mixed(3, 1, 5), fr(5, 10), fr(1, 5)), same_ok=True))
    its.append(mcq("Write %s as a decimal." % fr(13, 10), "1.3", ["13.10", "0.13", "3.1"],
                   "10 tenths make 1 whole, so 13 tenths = 1 whole and 3 tenths = <b>1.3</b>."))
    its.append(mcq("How many tenths are equal to %s?" % fr(1, 2), "5", ["2", "1", "10"],
                   "Half of 10 tenths is <b>5</b> tenths: %s = %s = 0.5." % (fr(1, 2), fr(5, 10))))
    its.append(mcq(fig(line_svg(0, 10, 10, dots=[(7, None)])) + "Which fraction names the red dot?", fr(7, 10),
                   [fr(1, 7), fr(3, 10), fr(7, 1)],
                   "The line from 0 to 1 has 10 equal spaces, so each space is %s. The dot is 7 spaces after 0: "
                   "<b>%s</b> = 0.7. %s counts back from 1." % (fr(1, 10), fr(7, 10), fr(3, 10))))
    its.append(mcq("Which is greater: <b>0.4</b> or %s?" % fr(1, 2), fr(1, 2), ["0.4", "They are equal", "You can’t tell"],
                   "%s = %s = 0.5, and 0.5 &gt; 0.4. So <b>%s</b> is greater." % (fr(1, 2), fr(5, 10), fr(1, 2)), same_ok=True))
    rt = "%s, %s, 0.6" % (fr(3, 10), fr(1, 2))
    its.append(mcq("Order from <b>smallest to greatest</b>: 0.6, %s, %s" % (fr(1, 2), fr(3, 10)), rt,
                   ["%s, 0.6, %s" % (fr(1, 2), fr(3, 10)), "%s, %s, 0.6" % (fr(1, 2), fr(3, 10)), "0.6, %s, %s" % (fr(1, 2), fr(3, 10))],
                   "Change them all to tenths: %s = 0.3, %s = 0.5 and 0.6. Order: <b>%s</b>." % (fr(3, 10), fr(1, 2), rt),
                   same_ok=True))
    its.append(mcq("Which pair shows two <b>equal</b> numbers?", "0.7 and " + fr(7, 10),
                   ["0.7 and " + fr(1, 7), "0.2 and " + fr(1, 2), "0.5 and " + fr(1, 5)],
                   "0.7 = 7 tenths = %s, so <b>0.7 and %s</b> are equal. %s = 0.5 (not 0.2) and %s = 0.2 (not 0.5)."
                   % (fr(7, 10), fr(7, 10), fr(1, 2), fr(1, 5)), same_ok=True))
    its.append(mcq("Mei walks %s km to school. Ethan walks 0.4 km. Who walks farther?" % fr(1, 2), "Mei",
                   ["Ethan", "They walk the same", "You can’t tell"],
                   "%s km = %s km = 0.5 km, and 0.5 &gt; 0.4. So <b>Mei</b> walks farther." % (fr(1, 2), fr(5, 10)), same_ok=True))
    its.append(mcq("A pan of brownies is cut into 10 equal pieces. The class eats 6 pieces. "
                   "Which shows the part they eat?", fr(6, 10) + " and 0.6",
                   [fr(6, 10) + " and 0.06", fr(4, 10) + " and 0.4", fr(1, 6) + " and 0.6"],
                   "6 of the 10 equal pieces: <b>%s = 0.6</b>. %s and 0.4 is the part that is left."
                   % (fr(6, 10), fr(4, 10)), same_ok=True))
    assert len(its) == 20, len(its)
    return {"title": "Fractions and decimal tenths", "items": its}


# ============================================================ set 5: add and subtract tenths
def calc(a, op, b, right, wrong, e, unit=""):
    r = V(a) + V(b) if op == "+" else V(a) - V(b)
    assert r == V(right), (a, op, b, right)
    for w in wrong:
        assert V(w) != r
    u = (" " + unit) if unit else ""
    return (right + u, [w + u for w in wrong], e)


def set_add_sub():
    its = []
    for a, op, b, right, wrong, e in [
        ("0.4", "+", "0.3", "0.7", ["0.07", "0.1", "7"],
         "4 tenths + 3 tenths = 7 tenths = <b>0.7</b>. The answer is still in tenths, so it is not 0.07."),
        ("0.8", "+", "0.2", "1", ["0.10", "0.6", "10"],
         "8 tenths + 2 tenths = 10 tenths, and 10 tenths make 1 whole: <b>1</b>. 0.10 is only 1 tenth."),
        ("0.6", "+", "0.7", "1.3", ["0.13", "13", "0.1"],
         "Make 1: 0.6 + 0.4 = 1, then add the other 0.3: <b>1.3</b>. 13 tenths is 1 whole and 3 tenths, not 0.13."),
        ("1", "−", "0.4", "0.6", ["1.4", "0.3", "3"],
         "1 = 10 tenths. 10 tenths − 4 tenths = 6 tenths = <b>0.6</b>. 0.3 comes from 4 − 1, which is the wrong way round."),
        ("2.5", "+", "1.3", "3.8", ["38", "1.2", "3.08"],
         "Add the ones: 2 + 1 = 3. Add the tenths: 5 + 3 = 8 tenths. So 2.5 + 1.3 = <b>3.8</b>."),
        ("3.6", "+", "0.8", "4.4", ["3.14", "44", "2.8"],
         "Make the next whole: 3.6 + 0.4 = 4, then add the other 0.4: <b>4.4</b>. "
         "3.14 writes 14 tenths in the tenths place; 14 tenths = 1 whole and 4 tenths."),
        ("4.7", "−", "1.2", "3.5", ["5.9", "35", "2.5"],
         "Take away the ones: 4 − 1 = 3. Take away the tenths: 7 − 2 = 5. So 4.7 − 1.2 = <b>3.5</b>. 5.9 adds instead."),
        ("3.2", "−", "0.5", "2.7", ["3.3", "3.7", "2.3"],
         "Take away 0.2 to get to 3, then take away 0.3 more: <b>2.7</b>. "
         "3.3 does 5 − 2 because 2 − 5 looks hard; 3.7 adds instead of taking away."),
        ("5", "−", "1.6", "3.4", ["4.6", "6.6", "3.6"],
         "Count up from 1.6: 0.4 makes 2, and 3 more makes 5. 0.4 + 3 = <b>3.4</b>. "
         "4.6 only takes away the 1 and forgets the 0.6."),
    ]:
        right, wrong, e = calc(a, "+" if op == "+" else "-", b, right, wrong, e)
        its.append(mcq("%s %s %s = ?" % (a, op, b), right, wrong, e))
    its.append(mcq("1.5 + ? = 2", "0.5", ["3.5", "5", "0.15"],
                   "Count up from 1.5 to 2: 5 tenths make the next whole. So the missing number is <b>0.5</b>. "
                   "3.5 adds 1.5 + 2."))
    assert V("1.5") + V("0.5") == 2
    words = [
        ("In the 60 m dash, Liam runs it in 10.4 seconds and Priya runs it in 9.8 seconds. "
         "How many seconds faster is Priya?", "10.4", "-", "9.8", "0.6", ["1.4", "0.4", "20.2"], "seconds",
         "Count up from 9.8: 0.2 makes 10, then 0.4 more makes 10.4. 0.2 + 0.4 = <b>0.6 seconds</b>. "
         "1.4 takes 4 from 8 instead of 8 from 4."),
        ("Amira’s bean plant is 4.6 cm tall. It grows 1.5 cm in a week. How tall is it now?",
         "4.6", "+", "1.5", "6.1", ["5.11", "3.1", "61"], "cm",
         "4.6 + 1 = 5.6, then 5.6 + 0.5: 0.4 makes 6 and 0.1 more makes <b>6.1 cm</b>. "
         "5.11 writes 11 tenths in the tenths place; 11 tenths = 1 whole and 1 tenth."),
        ("Lucas has 3 m of rope for a canoe trip. He cuts off 1.4 m. How much rope is left?",
         "3", "-", "1.4", "1.6", ["2.6", "2.4", "4.4"], "m",
         "Count up from 1.4: 0.6 makes 2, and 1 more makes 3. 0.6 + 1 = <b>1.6 m</b>. "
         "2.6 only takes away the 1 whole; 4.4 adds."),
        ("Hana swims 25 m in 21.5 seconds. On her next try she is 0.7 seconds faster. What is her new time?",
         "21.5", "-", "0.7", "20.8", ["22.2", "21.2", "14.5"], "seconds",
         "Faster means a shorter time, so subtract. 21.5 − 0.5 = 21, then take away 0.2 more: <b>20.8 seconds</b>. "
         "22.2 adds; 21.2 does 7 − 5."),
        ("On a snow day, 2.5 cm of snow falls in the morning and 3.8 cm falls in the afternoon. "
         "How much snow falls in all?", "2.5", "+", "3.8", "6.3", ["5.13", "1.3", "63"], "cm",
         "Ones: 2 + 3 = 5. Tenths: 5 + 8 = 13 tenths = 1 whole and 3 tenths. 5 + 1.3 = <b>6.3 cm</b>. "
         "1.3 is the difference, not the total."),
        ("At the Terry Fox Run, Ava walks 2.5 km and then runs 1.5 km. How far does she go in all?",
         "2.5", "+", "1.5", "4", ["3.10", "1", "40"], "km",
         "Tenths: 5 + 5 = 10 tenths = 1 whole. Ones: 2 + 1 = 3, and 3 + 1 = <b>4 km</b>. "
         "3.10 writes 10 tenths in the tenths place."),
        ("Jayden’s pencil is 18.4 cm long. After sharpening, it is 2.6 cm shorter. How long is it now?",
         "18.4", "-", "2.6", "15.8", ["16.2", "21", "16.8"], "cm",
         "18.4 − 2 = 16.4. Then take away 0.6: 16.4 − 0.4 = 16, and 16 − 0.2 = <b>15.8 cm</b>. "
         "16.2 does 6 − 4 in the tenths; 21 adds."),
        ("On a canoe trip, Sofia’s family paddles 3.6 km in the morning and 2.7 km in the afternoon. "
         "How much farther do they paddle in the morning?", "3.6", "-", "2.7", "0.9", ["1.1", "6.3", "1.9"], "km",
         "Count up from 2.7: 0.3 makes 3, then 0.6 more makes 3.6. 0.3 + 0.6 = <b>0.9 km</b>. "
         "1.1 does 7 − 6 in the tenths; 6.3 is the total."),
    ]
    for q, a, op, b, right, wrong, unit, e in words:
        r, w, e = calc(a, op, b, right, wrong, e, unit)
        its.append(mcq(q, r, w, e))
    its.append(mcq("Zoe has a 1 L water bottle. She drinks 0.3 L at recess and 0.4 L at lunch. "
                   "How much water is left?", "0.3 L", ["0.7 L", "0.6 L", "1.7 L"],
                   "She drinks 0.3 + 0.4 = 0.7 L. Then 1 − 0.7 = <b>0.3 L</b> is left. 0.7 L is the amount she drinks."))
    assert 1 - (V("0.3") + V("0.4")) == V("0.3")
    its.append(mcq("Kai’s backpack has a mass of 3.4 kg. He takes out his 0.8 kg lunch bag and puts in a 1.5 kg library book. "
                   "What is the mass of the backpack now?", "4.1 kg", ["2.6 kg", "5.7 kg", "4.9 kg"],
                   "Take away: 3.4 − 0.8 = 2.6. Then add: 2.6 + 1.5 = <b>4.1 kg</b>. "
                   "2.6 kg stops after one step; 5.7 kg adds all three."))
    assert V("3.4") - V("0.8") + V("1.5") == V("4.1") and V("3.4") + V("0.8") + V("1.5") == V("5.7")
    assert len(its) == 20, len(its)
    return {"title": "Add and subtract tenths", "items": its}


# ============================================================ lesson
def body_html():
    f_strip = strips_svg(3)
    f_line = line_svg(0, 10, 10, dots=[(3, None)])
    f_big = strips_svg(24)
    f_chart = chart_svg("2.4")
    f_cmp = line_svg(0, 10, 10, dots=[(1, "0.10"), (9, "0.9")]).replace("with points 0.10, 0.9", "with 0.10 and 0.9 marked")
    return (
        "<h2>Tenths</h2>"
        "<p>Split 1 whole into <b>10 equal parts</b>. Each part is one <b>tenth</b>: " + fr(1, 10) + " = 0.1. "
        "Tenths go in the <b>first place</b> after the decimal point.</p>"
        "<figure class='sn-fig'>" + f_strip +
        "<figcaption>The strip is 1 whole. 3 of the 10 parts are shaded: " + fr(3, 10) + " = 0.3.</figcaption></figure>"
        "<p>On a number line from 0 to 1 with 10 equal spaces, each space is 0.1.</p>"
        "<figure class='sn-fig'>" + f_line +
        "<figcaption>The dot is 3 spaces after 0, so it is at 0.3.</figcaption></figure>"
        "<h2>Decimals greater than 1</h2>"
        "<p>Ten tenths make 1 whole. Write the wholes before the decimal point and the tenths after it.</p>"
        "<figure class='sn-fig'>" + f_big +
        "<figcaption>2 whole strips and 4 tenths: " + mixed(2, 4, 10) + " = 2.4. That is 24 tenths.</figcaption></figure>"
        "<figure class='sn-fig'>" + f_chart +
        "<figcaption>2.4 = 2 ones and 4 tenths.</figcaption></figure>"
        "<h2>Fractions and decimals</h2>"
        "<p>A fraction in tenths is easy to write as a decimal: " + fr(7, 10) + " = 0.7. "
        "Halves and fifths can be changed to tenths first.</p>"
        + table(["Fraction", "Tenths", "Decimal"], [
            [fr(1, 2), fr(5, 10), "0.5"],
            [fr(1, 5), fr(2, 10), "0.2"],
            [fr(2, 5), fr(4, 10), "0.4"],
        ])
        + ex("Example 1", "Write " + mixed(3, 5, 10) + " as a decimal.",
             "3 wholes go before the point. 5 tenths go in the first place after it.", "3.5")
        + "<h2>Comparing decimals</h2>"
        "<p>Compare the ones first. If the ones are the same, compare the tenths.</p>"
        "<figure class='sn-fig'>" + f_cmp +
        "<figcaption>0.10 is the same as 0.1. It is far to the left of 0.9, so 0.9 &gt; 0.10.</figcaption></figure>"
        + ex("Example 2", "Order 1.2, 0.9 and 2.1 from smallest to greatest.",
             "Compare the ones: 0, 1 and 2.", "0.9, 1.2, 2.1")
        + "<h2>Adding and subtracting tenths</h2>"
        "<p>Add or take away the tenths, and remember that 10 tenths make 1 whole. "
        "Making the next whole number helps.</p>"
        + ex("Example 3", "0.6 + 0.7 = ?", "0.6 + 0.4 = 1. Then add the other 0.3.", "1.3")
        + ex("Example 4", "3.2 − 0.5 = ?", "3.2 − 0.2 = 3. Then take away the other 0.3.", "2.7")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["0.5 = " + fr(1, 5), "0.5 = " + fr(5, 10) + " = " + fr(1, 2) + ", and " + fr(1, 5) + " = 0.2"],
            ["0.10 &gt; 0.9 because 10 &gt; 9", "0.10 = 0.1, and 1 tenth &lt; 9 tenths"],
            ["Writing " + fr(3, 10) + " as 3.10 or 0.03", "Tenths use the first place: 0.3"],
            ["0.6 + 0.7 = 0.13", "13 tenths = 1 whole and 3 tenths: 1.3"],
            ["Counting 0.8, 0.9, 0.10", "10 tenths make 1 whole: 0.8, 0.9, 1"],
        ])
    )


FAQ = [
    {"q": "What do Grade 4 students learn about decimals in Ontario?",
     "a": "In the Ontario math curriculum, Grade 4 students read, show, compare and order decimal tenths, connect them to fractions like 3/10 = 0.3 and 1/2 = 0.5, and add and subtract tenths in their heads. Hundredths come in Grade 5."},
    {"q": "How do you explain decimal tenths to a child?",
     "a": "Show a strip or a chocolate bar split into 10 equal parts. Each part is one tenth, 0.1, so 3 parts are 0.3 and 10 parts make 1 whole."},
    {"q": "Is 0.5 the same as 1/5?",
     "a": "No. 0.5 means 5 tenths, which is 5/10 or one half. One fifth is 2/10, so 1/5 = 0.2."},
    {"q": "Is 0.10 bigger than 0.9?",
     "a": "No. 0.10 is the same as 0.1, just 1 tenth, while 0.9 is 9 tenths. Compare the tenths digits, not the number of digits."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (number lines, strips, place value charts)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(44808)
    sets = [set_tenths(), set_greater(), set_compare(), set_fractions(), set_add_sub()]
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
        "country": "ca-on", "subject": "math", "grade": "grade-4", "slug": "decimal-tenths", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 4 Decimal Tenths",
        "seo_title": "Grade 4 Decimal Tenths Worksheets: Free Math Practice with Answer Key (Ontario Curriculum)",
        "short_title": "Decimal tenths",
        "domain": "Number",
        "standard_code": "Grade 4: B1.7",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Read, represent, compare, and order decimal tenths, in various contexts",
        "meta_desc": "Free Grade 4 math worksheets on decimal tenths for the Ontario curriculum: tenths on strips and number lines, decimals greater than 1, comparing and ordering, fractions like 1/2 = 0.5, and adding and subtracting tenths. 100 questions with an answer key.",
        "key_big": "Tenths are the first place after the decimal point: 3/10 = 0.3, and 10 tenths make 1 whole.",
        "key_sub": "0.5 is 5/10 (one half), not 1/5. 0.10 is the same as 0.1, so 0.9 > 0.10. 0.6 + 0.7 = 1.3, not 0.13.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(number line|tenth strip|place value chart|four strips|two strips)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
