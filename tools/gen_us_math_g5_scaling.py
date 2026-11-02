# -*- coding: utf-8 -*-
"""
US Grade 5 Math: Multiplication as Scaling (5.NF.B.5)
  python tools/gen_us_math_g5_scaling.py
Most questions ask about the SIZE of a product without multiplying:
× more than 1 -> bigger, × less than 1 -> smaller, × 1 (such as 4/4) -> the same.
HTML attributes use single quotes (no backslashes in the JSON).
Grade 5 style: numbers 1,000 and above are written with commas.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-5")
UPDATED = "2026-11-02"
DARK = "#4fae74"      # scaled bar
LIGHT = "#d7ecdf"     # original bar
EDGE = "#1f6b3e"
LINE = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def f(n):
    """Grade 5 style: 1500 -> 1,500."""
    return "{:,}".format(n)


def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def mixed(w, r, b):
    if r == 0:
        return f(w)
    if w == 0:
        return fr(r, b)
    return "%s %s" % (f(w), fr(r, b))


def show(v):
    """A Fraction in simplest form: whole number, proper fraction or mixed number."""
    v = F(v)
    q, r = divmod(v.numerator, v.denominator)
    return mixed(q, r, v.denominator)


def plain(s):
    return re.sub(r"<[^>]+>", " ", s)


def mcq(q, right, wrongs, e):
    """right first; balance() moves it. All 4 choices must differ."""
    ch = [right] + list(wrongs)
    assert len(ch) == 4, (q, ch)
    assert len({re.sub(r"\s+", " ", plain(c)).strip() for c in ch}) == 4, ch
    return {"q": q, "c": ch, "a": 0, "e": e}


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


def cap(s):
    return s[0].upper() + s[1:]


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
    """Tag pictures that must print larger so their bars and labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# a factor is (w, n, d): 12 = (12, 0, 1); 3/4 = (0, 3, 4); 1 1/2 = (1, 1, 2)
def val(t):
    return F(t[0]) + F(t[1], t[2])


def fx(t):
    """Write the factor as given (4/4 stays 4/4)."""
    w, n, d = t
    if n == 0:
        return f(w)
    if w == 0:
        return fr(n, d)
    return "%s %s" % (f(w), fr(n, d))


def W(n):
    return (n, 0, 1)


def P(n, d):
    return (0, n, d)


def M(w, n, d):
    return (w, n, d)


def size_word(t):
    v = val(t)
    return "greater than 1" if v > 1 else "less than 1" if v < 1 else "equal to 1"


def one_e(t):
    """Why a factor is more than, less than or equal to 1."""
    w, n, d = t
    v = val(t)
    if n == 0:
        return "%s is %s" % (f(w), size_word(t))
    if w:
        return "%s is %s" % (fx(t), size_word(t))
    if n > d:
        return "%s is greater than 1 (the top is greater than the bottom)" % fx(t)
    if n < d:
        return "%s is less than 1 (the top is less than the bottom)" % fx(t)
    return "%s is equal to 1 (the top and the bottom are the same)" % fx(t)


# ------------------------------------------------------------ SVG pieces
def tw(t, fs):
    return len(str(t)) * fs * 0.6


def text(x, y, t, fs=16, col=LINE, anchor="middle", weight="700"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


FW, FF, GAP = 17, 15, 5


def tok_w(t):
    if isinstance(t, str):
        return tw(t, FW)
    w, n, d = t
    fw = max(tw(n, FF), tw(d, FF)) + 4
    return fw + (tw(w, FW) + GAP if w else 0)


def expr_w(toks):
    return sum(tok_w(t) for t in toks) + GAP * (len(toks) - 1)


def expr_svg(xr, cy, toks):
    """Tokens (strings or factors (w, n, d)) written right-aligned to xr, centered on cy."""
    x = xr - expr_w(toks)
    s = []
    for t in toks:
        wd = tok_w(t)
        if isinstance(t, str):
            s.append(text(x + wd / 2, cy + 6, t, FW))
        else:
            w, n, d = t
            xx = x
            if w:
                s.append(text(xx + tw(w, FW) / 2, cy + 6, w, FW))
                xx += tw(w, FW) + GAP
            fw = max(tw(n, FF), tw(d, FF)) + 4
            m = xx + fw / 2
            s.append(text(m, cy - 4, n, FF))
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.6'/>"
                     % (xx + 1, cy + 0.5, xx + fw - 1, cy + 0.5, LINE))
            s.append(text(m, cy + 16, d, FF))
        x += wd + GAP
    return "".join(s)


def ftok(t):
    """A factor as an SVG token: whole numbers become plain text."""
    return f(t[0]) if t[1] == 0 else t


def bars_svg(rows, label, mark=True, maxw=284):
    """rows: (tokens, parts, shaded, length, fill). length is a Fraction of the first bar.
    A dashed line marks the end of the first bar so the other bars can be compared with it."""
    lw = max(expr_w(r[0]) for r in rows)
    x0 = 6 + lw + 10
    maxlen = max(r[3] for r in rows)
    L = min(180.0, (maxw - x0 - 8) / float(maxlen))
    BH, PITCH, y = 30, 44, 22
    s = []
    for row in rows:
        toks, parts, shaded, length, fill = row[:5]
        grp = row[5] if len(row) > 5 else 0
        cy = y
        s.append(expr_svg(x0 - 10, cy, toks))
        pw = L * float(length) / parts
        for i in range(parts):
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x0 + i * pw, cy - BH / 2, pw, BH, fill if i < shaded else "#fff", EDGE))
        if grp:                                     # thick lines where the original parts end
            for i in range(grp, parts, grp):
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='4'/>"
                         % (x0 + i * pw, cy - BH / 2, x0 + i * pw, cy + BH / 2, EDGE))
        y += PITCH
    ybot = y - PITCH + BH / 2 + 6
    if mark:
        s.append("<line x1='%.1f' y1='4' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>"
                 % (x0 + L, x0 + L, ybot, RED))
    Wd = x0 + L * float(maxlen) + 8
    return svg_wrap(int(Wd + 0.99), int(ybot + 4 + 0.99), "".join(s), label)


def scale_svg(t, n, label_n=None):
    """Original bar n (cut into d parts) and the bar t × n (cut into parts of the same size)."""
    v = val(t)
    d = t[2]
    k = v.numerator * (d // v.denominator)          # number of 1/d parts in the scaled bar
    rows = [([label_n or f(n)], d, d, F(1), LIGHT),
            ([ftok(t), "×", f(n)], k, k, F(k, d), DARK)]
    name = "%d %d/%d" % t if t[0] else "%d/%d" % (t[1], t[2])
    return bars_svg(rows, "scaling bar model: %s and %s times %s" % (n, name, n))


def equiv_svg(a, b, k):
    rows = [([(0, a, b)], b, a, F(1), DARK),
            ([(0, a, b), "×", (0, k, k)], b * k, a * k, F(1), DARK, k)]
    return bars_svg(rows, "scaling bar model: %d/%d and %d/%d times %d/%d" % (a, b, a, b, k, k), mark=False)


# ============================================================ set 1: greater than, less than or equal to?
def cmp_choices(nh):
    return ["Greater than %s" % nh, "Less than %s" % nh, "Equal to %s" % nh, "Cannot tell yet"]


def cmp_item(q, t, nh, e):
    v = val(t)
    ch = cmp_choices(nh)
    idx = 0 if v > 1 else 1 if v < 1 else 2
    return mcq(q, ch[idx], [c for i, c in enumerate(ch) if i != idx], e)


def rule_e(t, nh):
    v = val(t)
    if v > 1:
        tail = "so %s × %s is <b>greater than %s</b>. It is more than 1 group of %s." % (fx(t), nh, nh, nh)
    elif v < 1:
        tail = "so %s × %s is <b>less than %s</b>. It is only part of %s." % (fx(t), nh, nh, nh)
    else:
        tail = "so %s × %s is <b>equal to %s</b>. Multiplying by 1 does not change a number." % (fx(t), nh, nh)
    return one_e(t) + ", " + tail + " You do not need to multiply."


def set_compare_one(rnd):
    its = []
    # A) bar models
    for t, n in [(P(3, 4), 12), (P(5, 4), 8), (P(2, 3), 9), (M(1, 1, 2), 6), (P(4, 4), 10), (P(7, 5), 10)]:
        v = val(t)
        q = (fig(scale_svg(t, n)) + "The top bar is %d. The bottom bar shows %s × %d. Without multiplying, "
             "how does %s × %d compare with %d?" % (n, fx(t), n, fx(t), n, n))
        d = t[2]
        k = v.numerator * (d // v.denominator)
        e = rule_e(t, f(n)) + " In the picture, the bottom bar has %d equal parts and the top bar has %d." % (k, d)
        its.append(cmp_item(q, t, f(n), e))
    # B) without a picture
    for t, nh in [(P(5, 8), "20"), (P(7, 6), "18"), (P(6, 6), "15"), (M(2, 1, 3), "7"), (P(99, 100), "50"),
                  (P(9, 8), "40")]:
        q = "Without multiplying, is %s × %s greater than, less than or equal to %s?" % (fx(t), nh, nh)
        its.append(cmp_item(q, t, nh, rule_e(t, nh)))
    # the other factor decides
    for first, other, ask in [(W(4), P(2, 5), "other"), (P(3, 4), P(5, 6), "other"), (P(3, 4), P(5, 6), "first"),
                              (M(1, 1, 5), P(3, 7), "other")]:
        prod = "%s × %s" % (fx(first), fx(other))
        if ask == "other":
            nh, by = fx(other), first
        else:
            nh, by = fx(first), other
        q = "Without multiplying, is %s greater than, less than or equal to %s?" % (prod, nh)
        e = ("Compare the product with %s by looking at the <b>other</b> factor, %s. " % (nh, fx(by))
             + one_e(by) + ", so the product is <b>%s %s</b>." % ("greater than" if val(by) > 1 else "less than", nh))
        if ask == "first":
            e += " (It does not matter that %s is also less than 1.)" % nh
        its.append(cmp_item(q, by, nh, e))
    # C) pick the product
    picks = [
        ("Which product is <b>less than</b> 15?", "less",
         [P(7, 8), P(9, 8), P(15, 15), M(1, 1, 4)], "15"),
        ("Which product is <b>greater than</b> 24?", "greater",
         [P(5, 3), P(3, 5), P(8, 8), P(99, 100)], "24"),
        ("Which product is <b>equal to</b> 9?", "equal",
         [P(7, 7), P(9, 7), P(7, 9), M(1, 1, 7)], "9"),
        ("Which product is <b>greater than</b> " + fr(2, 3) + "?", "greater",
         [P(5, 4), P(4, 5), P(3, 3), P(1, 2)], fr(2, 3)),
    ]
    for q, kind, ts, nh in picks:
        right = ts[0]
        v = val(right)
        assert (kind == "less" and v < 1) or (kind == "greater" and v > 1) or (kind == "equal" and v == 1)
        for w in ts[1:]:
            vw = val(w)
            assert not ((kind == "less" and vw < 1) or (kind == "greater" and vw > 1) or (kind == "equal" and vw == 1))
        ch = ["%s × %s" % (fx(t), nh) for t in ts]
        e = (one_e(right) + ", so %s × %s is %s %s. " % (fx(right), nh,
                                                          {"less": "less than", "greater": "greater than", "equal": "equal to"}[kind], nh)
             + "Check the others: " + "; ".join(one_e(t) for t in ts[1:]) + ".")
        its.append(mcq(q, ch[0], ch[1:], e))
    assert len(its) == 20, len(its)
    return {"title": "Greater than, less than or equal to the number?", "items": its}


# ============================================================ set 2: compare products without multiplying
def set_compare_two(rnd):
    its = []
    # A) which product is greater
    pairs = [(P(5, 6), P(7, 6), "9"), (P(3, 4), P(3, 5), "10"), (P(4, 5), P(5, 4), "16"), (P(8, 7), P(7, 8), "14"),
             (M(1, 1, 2), M(1, 1, 3), "6"), (P(9, 10), M(1, 1, 10), "30")]
    for a, b, nh in pairs:
        ea, eb = "%s × %s" % (fx(a), nh), "%s × %s" % (fx(b), nh)
        q = "Without multiplying, which is greater: %s or %s?" % (ea, eb)
        big, small = (a, b) if val(a) > val(b) else (b, a)
        right = "%s × %s" % (fx(big), nh)
        wrong = "%s × %s" % (fx(small), nh)
        if (val(a) - 1) * (val(b) - 1) < 0:
            e = ("%s, so %s × %s is more than %s. %s, so %s × %s is less than %s. The greater one is <b>%s</b>."
                 % (cap(one_e(big)), fx(big), nh, nh, cap(one_e(small)), fx(small), nh, nh, right))
        elif big[1] == small[1] and big[0] == small[0]:
            e = ("Both products multiply %s. %s is greater than %s because %s are larger parts than %s. "
                 "A greater factor makes a greater product, so <b>%s</b> is greater."
                 % (nh, fx(big), fx(small), {4: "fourths", 6: "sixths", 3: "thirds", 2: "halves"}.get(big[2], "parts"),
                    {5: "fifths", 7: "sevenths", 8: "eighths", 3: "thirds"}.get(small[2], "parts"), right))
        else:
            e = ("Both products multiply %s, so compare the other factors. %s is greater than %s, so <b>%s</b> is greater."
                 % (nh, fx(big), fx(small), right))
        its.append(mcq(q, right, [wrong, "They are equal", "Cannot tell yet"], e))
    # equal
    q = "Without multiplying, which is greater: %s × 11 or 11?" % fr(6, 6)
    its.append(mcq(q, "They are equal", ["%s × 11" % fr(6, 6), "11", "Cannot tell yet"],
                   "%s, so %s × 11 = 11. <b>They are equal.</b>" % (cap(one_e(P(6, 6))), fr(6, 6))))
    q = "Without multiplying, which is greater: %s × 21 or %s × 15?" % (fr(2, 3), fr(2, 3))
    its.append(mcq(q, "%s × 21" % fr(2, 3), ["%s × 15" % fr(2, 3), "They are equal", "Cannot tell yet"],
                   "Both are %s of a number. %s of a greater number is greater, so <b>%s × 21</b> is greater."
                   % (fr(2, 3), fr(2, 3), fr(2, 3))))
    # B) fill in the sign
    for a, b, side in [(P(2, 3), P(5, 7), "b"), (P(4, 3), P(5, 8), "b"), (P(4, 3), P(5, 8), "a"), (P(9, 9), P(3, 10), "b")]:
        keep, other = (b, a) if side == "b" else (a, b)
        q = "Which sign makes this true?<br>%s × %s <b>?</b> %s" % (fx(a), fx(b), fx(keep))
        vo = val(other)
        right = ">" if vo > 1 else "<" if vo < 1 else "="
        wr = [x for x in [">", "<", "="] if x != right] + ["Cannot tell"]
        e = ("Look at the <b>other</b> factor, %s. %s, so the product is %s %s. The sign is <b>%s</b>."
             % (fx(other), cap(one_e(other)), "greater than" if vo > 1 else "less than" if vo < 1 else "equal to",
                fx(keep), right.replace("<", "&lt;").replace(">", "&gt;")))
        its.append(mcq(q, right.replace("<", "&lt;").replace(">", "&gt;"),
                       [w.replace("<", "&lt;").replace(">", "&gt;") for w in wr], e))
    # C) order three products
    orders = [
        ((P(2, 3), P(7, 6), P(2, 5)), "30", ["A, C, B", "B, A, C", "A, B, C"],
         "A bigger bottom number does not make a bigger fraction: fifths are smaller than thirds."),
        ((P(5, 4), P(5, 8), P(8, 8)), "16", ["A, C, B", "C, B, A", "B, A, C"],
         "Eighths are smaller than fourths, so %s is less than %s." % (fr(5, 8), fr(5, 4))),
        ((P(3, 10), P(9, 10), M(1, 1, 10)), "50", ["C, B, A", "A, C, B", "B, A, C"],
         "%s is the only factor greater than 1." % mixed(1, 1, 10)),
    ]
    for ts, nh, wr, tip in orders:
        names = "ABC"
        q = ("A = %s × %s, B = %s × %s, C = %s × %s<br>Without multiplying, order the products from least to greatest."
             % (fx(ts[0]), nh, fx(ts[1]), nh, fx(ts[2]), nh))
        idx = sorted(range(3), key=lambda i: val(ts[i]))
        right = ", ".join(names[i] for i in idx)
        e = ("All three products multiply %s, so order the factors: %s &lt; %s &lt; %s. So the order is <b>%s</b>. %s"
             % (nh, fx(ts[idx[0]]), fx(ts[idx[1]]), fx(ts[idx[2]]), right, tip))
        its.append(mcq(q, right, wr, e))
    # different numbers too
    q = ("A = %s × 12, B = %s × 8, C = %s × 12<br>Without multiplying, order the products from least to greatest."
         % (fr(3, 4), fr(3, 4), fr(5, 4)))
    assert F(3, 4) * 8 < F(3, 4) * 12 < F(5, 4) * 12
    its.append(mcq(q, "B, A, C", ["B, C, A", "A, B, C", "C, B, A"],
                   "A and B are both %s of a number, and 8 &lt; 12, so B &lt; A. A is less than 12 (%s &lt; 1) and C is "
                   "more than 12 (%s &gt; 1), so A &lt; C. The order is <b>B, A, C</b>." % (fr(3, 4), fr(3, 4), fr(5, 4))))
    # D) what could go in the box
    boxes = [
        ("<b>?</b> × 25 is greater than 25.", P(9, 8), [P(8, 9), P(6, 6), P(1, 2)], "greater than 1"),
        ("<b>?</b> × 18 is less than 18.", P(5, 6), [P(6, 5), P(4, 4), W(2)], "less than 1"),
        ("<b>?</b> × 7 is equal to 7.", P(3, 3), [P(1, 7), P(3, 4), P(4, 3)], "equal to 1"),
        ("<b>?</b> × 8 is between 4 and 8.", P(3, 4), [P(1, 4), P(5, 4), P(1, 2)], None),
    ]
    for q0, right, wr, need in boxes:
        q = q0 + " Which number could be in the box?"
        if need:
            for w in wr:
                assert size_word(w) != need
            assert size_word(right) == need
            e = ("The product is %s, so the box must be <b>%s</b>. %s. Check the others: %s."
                 % (q0.split(" is ")[1].rstrip("."), need, cap(one_e(right)), "; ".join(one_e(w) for w in wr)))
        else:
            for w in wr:
                assert not (4 < val(w) * 8 < 8)
            assert 4 < val(right) * 8 < 8
            e = ("To be less than 8, the box must be less than 1. To be more than 4 (half of 8), it must be more than "
                 "%s. <b>%s</b> is between %s and 1. (%s × 8 = 2, %s × 8 = 4 and %s × 8 = 10 are not between 4 and 8.)"
                 % (fr(1, 2), fr(3, 4), fr(1, 2), fr(1, 4), fr(1, 2), fr(5, 4)))
        its.append(mcq(q, fx(right), [fx(w) for w in wr], e))
    assert len(its) == 20, len(its)
    return {"title": "Compare products without multiplying", "items": its}


# ============================================================ set 3: multiplying by 1 in disguise
def set_times_one(rnd, Pp):
    its = []
    q = "Which fraction is equal to 1?"
    its.append(mcq(q, fr(6, 6), [fr(6, 1), fr(1, 6), fr(6, 7)],
                   "A fraction is equal to 1 when the top and the bottom are the same: <b>%s</b> = 1. "
                   "(%s = 6 and %s is less than 1.)" % (fr(6, 6), fr(6, 1), fr(1, 6))))
    # A) multiply by n/n
    for a, b, k, pic in [(2, 3, 4, True), (3, 5, 2, True), (3, 4, 3, False), (1, 4, 5, False), (4, 7, 3, False)]:
        q = "%s × %s = <b>?</b>" % (fr(a, b), fr(k, k))
        if pic:
            q = fig(equiv_svg(a, b, k)) + q
        e = ("Multiply the tops and the bottoms: %d × %d = %d and %d × %d = %d, so the answer is <b>%s</b>. "
             "%s is 1, so %s is equal to %s."
             % (a, k, a * k, b, k, b * k, fr(a * k, b * k), fr(k, k), fr(a * k, b * k), fr(a, b)))
        if pic:
            e += " The bars are the same length: each part was cut into %d smaller parts." % k
        wr = [fr(a + k, b + k), fr(a * k, b), fr(a, b * k)]
        assert len({F(a * k, b * k), F(a + k, b + k), F(a * k, b), F(a, b * k)}) == 4
        its.append(mcq(q, fr(a * k, b * k), wr, e))
    # B) missing factor
    for a, b, k in [(3, 4, 3), (2, 5, 4), (4, 5, 3), (1, 3, 5)]:
        q = "%s × <b>?</b> = %s<br>What is the missing fraction?" % (fr(a, b), fr(a * k, b * k))
        add = fr(a * k - a, b * k - b)
        e = ("%d × %d = %d and %d × %d = %d, so the missing fraction is <b>%s</b>, which is equal to 1. "
             "%s and %s are equal fractions. (%s would be adding, not multiplying.)"
             % (a, k, a * k, b, k, b * k, fr(k, k), fr(a, b), fr(a * k, b * k), add))
        wr = [add, fr(k, 1), fr(1, k)]
        its.append(mcq(q, fr(k, k), wr, e))
    # C) which product is equal
    for a, b, k in [(4, 7, 2), (3, 8, 5), (5, 9, 3), (7, 10, 4)]:
        q = "Which product is equal to %s?" % fr(a, b)
        right = "%s × %s" % (fr(a, b), fr(k, k))
        wr = ["%s × %s" % (fr(a, b), fr(k, 1)), "%s × %s" % (fr(a, b), fr(1, k)), "%s × %s" % (fr(a, b), fr(k + 1, k))]
        e = ("Only multiplying by 1 keeps the value the same. %s = 1, so <b>%s</b> = %s = %s. "
             "%s and %s are greater than 1, and %s is less than 1."
             % (fr(k, k), right, fr(a * k, b * k), fr(a, b), fr(k, 1), fr(k + 1, k), fr(1, k)))
        its.append(mcq(q, right, wr, e))
    # D) reasons and mistakes
    q = "Which reason shows that %s is equal to %s?" % (fr(3, 5), fr(6, 10))
    its.append(mcq(q, "%s × %s = %s, and %s = 1" % (fr(3, 5), fr(2, 2), fr(6, 10), fr(2, 2)),
                   ["%s × 2 = %s" % (fr(3, 5), fr(6, 10)), "%s + %s = %s" % (fr(3, 5), fr(3, 5), fr(6, 10)),
                    "%s has greater numbers" % fr(6, 10)],
                   "%s = 1, and multiplying by 1 does not change a number. So <b>%s × %s = %s</b> is equal to %s. "
                   "(%s × 2 and %s + %s are both %s, not %s.)"
                   % (fr(2, 2), fr(3, 5), fr(2, 2), fr(6, 10), fr(3, 5), fr(3, 5), fr(3, 5), fr(3, 5), fr(6, 5), fr(6, 10))))
    nm, he, his = Pp.next()
    q = ("%s says %s × %s = %s, so the product is greater than %s because 6 and 15 are greater numbers. What is true?"
         % (nm, fr(2, 5), fr(3, 3), fr(6, 15), fr(2, 5)))
    its.append(mcq(q, "%s is equal to %s" % (fr(6, 15), fr(2, 5)),
                   ["%s is greater than %s" % (fr(6, 15), fr(2, 5)), "%s is less than %s" % (fr(6, 15), fr(2, 5)),
                    "%s is 3 times %s" % (fr(6, 15), fr(2, 5))],
                   "%s = 1, so %s × %s is <b>equal to %s</b>. The numbers are greater, but the parts are smaller: "
                   "%s is the same amount as %s." % (fr(3, 3), fr(2, 5), fr(3, 3), fr(2, 5), fr(6, 15), fr(2, 5))))
    q = "Without multiplying, is %s × %s greater than, less than or equal to %s?" % (fr(5, 6), fr(3, 3), fr(5, 6))
    its.append(cmp_item(q, P(3, 3), fr(5, 6),
                        "%s = 1, so %s × %s is <b>equal to %s</b>. The answer, %s, has greater numbers, but it is "
                        "the same amount." % (fr(3, 3), fr(5, 6), fr(3, 3), fr(5, 6), fr(15, 18))))
    # E) rename with a new denominator
    for a, b, nd in [(5, 8, 24), (2, 3, 15), (3, 4, 20)]:
        k = nd // b
        q = "Multiply %s by a fraction equal to 1 to write it with a denominator of %d. What do you get?" % (fr(a, b), nd)
        e = ("%d × %d = %d, so multiply by %s, which is 1: %s × %s = <b>%s</b>. "
             "(Do not add %d to the top: that changes the value.)"
             % (b, k, nd, fr(k, k), fr(a, b), fr(k, k), fr(a * k, nd), nd - b))
        wr = [fr(a, nd), fr(a + nd - b, nd), fr(a * k, b)]
        its.append(mcq(q, fr(a * k, nd), wr, e))
    assert len(its) == 20, len(its)
    return {"title": "Multiplying by 1 and equivalent fractions", "items": its}


# ============================================================ set 4: explain why and find the mistake
def set_explain(rnd, Pp):
    its = []

    def add(q, right, wr, e):
        its.append(mcq(q, right, wr, e))

    add("Why is %s × 9 greater than 9?" % fr(7, 4),
        "%s is greater than 1" % fr(7, 4),
        ["Multiplying always makes things bigger", "Fourths are big parts", "Fractions always make numbers bigger"],
        "%s is greater than 1, so %s × 9 is more than 1 group of 9. So the reason is: <b>%s is greater than 1</b>. "
        "(Multiplying does not always make things bigger: %s × 9 is less than 9.)" % (fr(7, 4), fr(7, 4), fr(7, 4), fr(1, 2)))
    add("Why is %s × 50 less than 50?" % fr(3, 8),
        "%s is less than 1" % fr(3, 8),
        ["All fractions make numbers smaller", "50 is a large number", "%s × 50 means 50 − %s" % (fr(3, 8), fr(3, 8))],
        "%s is less than 1, so %s × 50 is only part of 50. Not all fractions make numbers smaller: %s × 50 is more than 50."
        % (fr(3, 8), fr(3, 8), fr(9, 8)))
    nm, he, his = Pp.next()
    add("%s says, “Multiplying always makes a number bigger.” Which example shows that %s is wrong?" % (nm, he),
        "%s × 10 = 5" % fr(1, 2),
        ["2 × 10 = 20", "%s × 10 = 15" % fr(3, 2), "%s × 8 = 10" % fr(5, 4)],
        "In <b>%s × 10 = 5</b>, the product 5 is less than 10. When you multiply by a number less than 1, the product "
        "is smaller. The other examples all get bigger." % fr(1, 2))
    add("Which statement is always true?",
        "A number times a fraction less than 1 is less than the number",
        ["A product is always greater than both factors", "A number times a fraction is always smaller",
         "A bigger denominator makes a bigger product"],
        "Multiplying by a fraction less than 1 takes only part of the number, so the product is smaller. "
        "Fractions greater than 1, such as %s, make it bigger, and a bigger denominator means smaller parts." % fr(5, 4))
    nm, he, his = Pp.next()
    add("%s says %s × 18 = 27. Without multiplying, how do you know %s answer is wrong?" % (nm, fr(2, 3), his),
        "The product must be less than 18",
        ["The product must be more than 27", "The product must equal 18", "%s answer is right" % cap(his)],
        "%s is less than 1, so %s × 18 must be <b>less than 18</b>. 27 is more than 18, so it cannot be right. "
        "(27 is 18 ÷ %s. The product is 12.)" % (fr(2, 3), fr(2, 3), fr(2, 3)))
    nm, he, his = Pp.next()
    add("%s says %s × 20 is greater than %s × 20 because 9 is greater than 6. What is %s mistake?"
        % (nm, fr(5, 9), fr(5, 6), his),
        "Ninths are smaller than sixths",
        ["Both products are equal", "%s should compare 20 and 20" % cap(he), "There is no mistake"],
        "A bigger bottom number means <b>smaller parts</b>. %s is less than %s, so %s × 20 is less than %s × 20."
        % (fr(5, 9), fr(5, 6), fr(5, 9), fr(5, 6)))
    nm, he, his = Pp.next()
    add("%s says %s × %s = %s, so the product is greater than %s. What is true?" % (nm, fr(3, 4), fr(4, 4), fr(12, 16), fr(3, 4)),
        "%s = 1, so %s = %s" % (fr(4, 4), fr(12, 16), fr(3, 4)),
        ["%s is greater: 12 &gt; 3" % fr(12, 16), "%s is less than %s" % (fr(12, 16), fr(3, 4)),
         "%s should add %s + %s" % (cap(he), fr(3, 4), fr(4, 4))],
        "%s is 1, and multiplying by 1 does not change a number. <b>%s is equal to %s</b>: it has more parts, "
        "but each part is smaller." % (fr(4, 4), fr(12, 16), fr(3, 4)))
    nm, he, his = Pp.next()
    add("%s multiplied a number by %s and got 30. Was the number %s started with more or less than 30?"
        % (nm, fr(5, 6), he),
        "More than 30", ["Less than 30", "Equal to 30", "Cannot tell yet"],
        "Multiplying by %s (less than 1) makes a number smaller. The product 30 is smaller than the start, so the "
        "start was <b>more than 30</b>. (It was 36: %s × 36 = 30.)" % (fr(5, 6), fr(5, 6)))
    nm, he, his = Pp.next()
    add("%s multiplied a number by %s and got 20. Was the number %s started with more or less than 20?"
        % (nm, fr(4, 3), he),
        "Less than 20", ["More than 20", "Equal to 20", "Cannot tell yet"],
        "Multiplying by %s (greater than 1) makes a number bigger. The product 20 is bigger than the start, so the "
        "start was <b>less than 20</b>. (It was 15: %s × 15 = 20.)" % (fr(4, 3), fr(4, 3)))
    nm, he, his = Pp.next()
    add("%s says %s × 8 = %s. What is %s mistake?" % (nm, mixed(1, 1, 2), mixed(8, 1, 2), his),
        "%s added %s instead of taking %s of 8" % (cap(he), fr(1, 2), fr(1, 2)),
        ["There is no mistake", "The product should be less than 8", "%s × 8 is just 8" % mixed(1, 1, 2)],
        "%s × 8 is 1 group of 8 and %s of 8 more: 8 + 4 = 12. %s added %s instead of taking <b>%s of 8</b>."
        % (mixed(1, 1, 2), fr(1, 2), cap(he), fr(1, 2), fr(1, 2)))
    add("Is %s × %s greater or less than %s? Which reason is right?" % (fr(3, 4), fr(2, 3), fr(2, 3)),
        "Less, because %s is less than 1" % fr(3, 4),
        ["Less, because %s is less than 1" % fr(2, 3), "Greater, because you multiply",
         "Equal, because both are fractions"],
        "To compare the product with %s, look at the <b>other</b> factor, %s. %s is less than 1, so the product is "
        "less than %s. (%s being less than 1 tells you about comparing with %s, not with %s.)"
        % (fr(2, 3), fr(3, 4), fr(3, 4), fr(2, 3), fr(2, 3), fr(3, 4), fr(2, 3)))
    add("Without multiplying, how do you know that 6 × %s is greater than %s?" % (fr(4, 5), fr(4, 5)),
        "6 is greater than 1",
        ["%s is less than 1" % fr(4, 5), "5 is greater than 4", "6 is greater than 5"],
        "6 × %s is 6 groups of %s. The other factor, <b>6, is greater than 1</b>, so the product is greater than %s."
        % (fr(4, 5), fr(4, 5), fr(4, 5)))
    add("Any number is multiplied by %s. Which is true about the product?" % fr(7, 7),
        "It equals the number", ["It is greater than the number", "It is 7 times the number", "It is less than the number"],
        "%s = 1, and a number times 1 is the same number. So the product <b>equals the number</b>." % fr(7, 7))
    add("Which product is <b>less than both</b> of its factors?",
        "%s × %s" % (fr(2, 3), fr(3, 4)), ["4 × %s" % fr(1, 2), "%s × 4" % fr(3, 2), "1 × %s" % fr(5, 6)],
        "Both %s and %s are less than 1, so each one makes the other smaller. <b>%s × %s</b> = %s is less than both. "
        "4 × %s = 2 is less than 4 but greater than %s." % (fr(2, 3), fr(3, 4), fr(2, 3), fr(3, 4), fr(1, 2), fr(1, 2), fr(1, 2)))
    add("Which product is <b>greater than both</b> of its factors?",
        "%s × 4" % fr(3, 2), ["%s × 6" % fr(2, 3), "%s × %s" % (fr(1, 2), fr(3, 2)), "1 × 5"],
        "Both %s and 4 are greater than 1, so each one makes the other bigger: <b>%s × 4</b> = 6. "
        "%s × 6 = 4 is less than 6, and 1 × 5 = 5 is not greater than 5." % (fr(3, 2), fr(3, 2), fr(2, 3)))
    nm, he, his = Pp.next()
    add("%s says %s × 40 is close to 40, but a little less. Is %s right?" % (nm, fr(9, 10), he),
        "Yes: %s is a little less than 1" % fr(9, 10),
        ["No: it is a lot less than 40", "No: it is more than 40", "No: it is exactly 40"],
        "%s is just a little less than 1, so %s × 40 is a little less than 40. (It is 36.)" % (fr(9, 10), fr(9, 10)))
    nm, he, his = Pp.next()
    add("%s says %s × 35 is greater than %s × 35. Is %s right?" % (nm, fr(2, 5), fr(1, 2), he),
        "No: %s is less than %s" % (fr(2, 5), fr(1, 2)),
        ["Yes: fifths are greater than halves", "Yes: 2 and 5 are greater numbers", "No: they are equal"],
        "%s is less than %s (2 out of 5 is less than half of 5), so %s × 35 is <b>less</b> than %s × 35."
        % (fr(2, 5), fr(1, 2), fr(2, 5), fr(1, 2)))
    add("<i>a</i> × 12 = 12. What do you know about <i>a</i>?",
        "It is equal to 1", ["It is greater than 1", "It is less than 1", "It is equal to 12"],
        "The product is the same as 12, so <i>a</i> did not change it: <b><i>a</i> = 1</b> (for example, %s)." % fr(5, 5))
    add("<i>b</i> × 15 is less than 15. What do you know about <i>b</i>?",
        "It is less than 1", ["It is less than 15", "It is greater than 1", "It is equal to 1"],
        "Only a factor <b>less than 1</b> makes 15 smaller. (A number less than 15, such as 2, makes 2 × 15 = 30.)")
    add("<i>c</i> × %s is greater than %s. What do you know about <i>c</i>?" % (fr(3, 5), fr(3, 5)),
        "It is greater than 1", ["It is greater than %s" % fr(3, 5), "It is less than 1", "It is equal to 1"],
        "Only a factor <b>greater than 1</b> makes %s bigger. Greater than %s is not enough: %s × %s is less than %s."
        % (fr(3, 5), fr(3, 5), fr(4, 5), fr(3, 5), fr(3, 5)))
    assert len(its) == 20, len(its)
    return {"title": "Explain why and find the mistake", "items": its}


# ============================================================ set 5: scaling stories
def qty(v, one, many):
    v = F(v)
    return "%s %s" % (show(v), one if v <= 1 else many)


def set_stories(rnd, Pp):
    its = []

    def num(story, t, n, one, many, wr, e0, extra=""):
        """Find the new amount t × n. wr = list of Fractions from real mistakes."""
        v = val(t) * n
        vals = [v] + [F(w) for w in wr]
        assert len(set(vals)) == 4 and all(x > 0 for x in vals), (story, vals)
        bigger = "greater" if val(t) > 1 else "less"
        e = (e0 + " %s, so the answer must be %s than %s. %s × %s = <b>%s</b>.%s"
             % (cap(one_e(t)), bigger, qty(n, one, many), fx(t), show(n), qty(v, one, many), extra))
        its.append(mcq(story, qty(v, one, many), [qty(w, one, many) for w in wr], e))

    nm, he, his = Pp.next()
    num("%s has a photo that is 6 inches wide. %s prints a copy %s times as wide. How wide is the copy?"
        % (nm, cap(he), mixed(1, 1, 2)), M(1, 1, 2), 6, "inch", "inches",
        [F(15, 2), F(13, 2), F(4)], "The copy is %s times 6 inches." % mixed(1, 1, 2),
        " (1 × 6 = 6, and %s of 6 is 3 more.)" % fr(1, 2))
    nm, he, his = Pp.next()
    num("A poster is 8 feet tall. %s makes a small copy that is %s as tall. How tall is the small copy?"
        % (nm, fr(3, 4)), P(3, 4), 8, "foot", "feet",
        [F(35, 4), F(32, 3), F(2)], "The copy is %s of 8 feet." % fr(3, 4))
    nm, he, his = Pp.next()
    num("A muffin recipe uses 3 cups of flour. %s makes %s of the recipe. How much flour does %s use?"
        % (nm, fr(2, 3), he), P(2, 3), 3, "cup", "cups",
        [F(9, 2), F(11, 3), F(1)], "%s uses %s of 3 cups." % (nm, fr(2, 3)))
    nm, he, his = Pp.next()
    num("A pancake recipe uses 2 cups of milk. %s makes %s batches. How much milk does %s need?"
        % (nm, mixed(1, 1, 2), he), M(1, 1, 2), 2, "cup", "cups",
        [F(7, 2), F(5, 2), F(4, 3)], "%s batches use %s times 2 cups." % (mixed(1, 1, 2), mixed(1, 1, 2)))
    num("A real whale is 72 feet long. A model of the whale is %s as long. How long is the model?" % fr(1, 24),
        P(1, 24), 72, "foot", "feet", [F(1728), F(72) + F(1, 24), F(69)],
        "The model is %s of 72 feet." % fr(1, 24), " (72 ÷ 24 = 3.)")
    nm, he, his = Pp.next()
    num("On a map, 1 inch stands for 8 miles. Two towns are %s inches apart on the map. How far apart are the real towns?"
        % mixed(2, 1, 2), M(2, 1, 2), 8, "mile", "miles", [F(21, 2), F(33, 2), F(16, 5)],
        "The real distance is %s times 8 miles." % mixed(2, 1, 2), " (2 × 8 = 16, and %s of 8 is 4 more.)" % fr(1, 2))
    nm, he, his = Pp.next()
    num("%s ran 3 miles on Monday. On Tuesday, %s ran %s as far. How far did %s run on Tuesday?"
        % (nm, he, fr(2, 3), he), P(2, 3), 3, "mile", "miles", [F(9, 2), F(11, 3), F(1)],
        "Tuesday is %s of 3 miles." % fr(2, 3))
    nm, he, his = Pp.next()
    num("A soup recipe uses 4 cups of broth. %s makes %s times the recipe for a party. How much broth does %s need?"
        % (nm, mixed(1, 1, 2), he), M(1, 1, 2), 4, "cup", "cups", [F(11, 2), F(9, 2), F(8, 3)],
        "%s needs %s times 4 cups." % (nm, mixed(1, 1, 2)))
    num("Painting a big wall takes 3 gallons of paint. A smaller wall is %s the size. How much paint does the smaller wall take?"
        % fr(5, 6), P(5, 6), 3, "gallon", "gallons", [F(23, 6), F(18, 5), F(1, 2)],
        "The smaller wall needs %s of 3 gallons." % fr(5, 6), " (3 ÷ 6 = %s, and 5 × %s = %s.)" % (fr(1, 2), fr(1, 2), mixed(2, 1, 2)))
    nm, he, his = Pp.next()
    num("%s's walk to school takes 12 minutes. Riding a bike takes %s as long. How long does the bike ride take?"
        % (nm, fr(3, 4)), P(3, 4), 12, "minute", "minutes", [F(16), F(51, 4), F(3)],
        "The bike ride takes %s of 12 minutes." % fr(3, 4), " (12 ÷ 4 = 3, and 3 × 3 = 9.)")

    # how much more or less
    nm, he, his = Pp.next()
    q = ("%s's puppy weighs 12 pounds. In a few months, it will weigh %s times as much. How much <b>more</b> will it weigh then?"
         % (nm, mixed(2, 1, 2)))
    its.append(mcq(q, "18 pounds more", ["30 pounds more", "%s pounds more" % mixed(2, 1, 2), "6 pounds more"],
                   "%s is greater than 1, so the puppy will get heavier: %s × 12 = 24 + 6 = 30 pounds (2 × 12 = 24, and %s of 12 is 6). "
                   "That is 30 − 12 = <b>18 pounds more</b>. (30 pounds is the new weight, not how much more.)"
                   % (mixed(2, 1, 2), mixed(2, 1, 2), fr(1, 2))))
    nm, he, his = Pp.next()
    q = "%s has a banner that is 24 inches wide. %s shrinks it to %s of its width. How much narrower is the new banner?" % (
        nm, cap(he), fr(5, 6))
    its.append(mcq(q, "4 inches narrower", ["20 inches narrower", "4 inches wider", "%s inch narrower" % fr(1, 6)],
                   "%s is less than 1, so the banner gets narrower: %s × 24 = 20 inches. That is 24 − 20 = "
                   "<b>4 inches narrower</b>. (%s of 24 is 4.)" % (fr(5, 6), fr(5, 6), fr(1, 6))))
    q = "A garden bed is 12 feet long. A new bed will be %s as long. How much longer is the new bed?" % fr(7, 6)
    its.append(mcq(q, "2 feet longer", ["14 feet longer", "2 feet shorter", "%s foot longer" % fr(1, 6)],
                   "%s is greater than 1, so the new bed is longer: %s × 12 = 14 feet. That is 14 − 12 = "
                   "<b>2 feet longer</b>. (The extra %s of 12 is 2.)" % (fr(7, 6), fr(7, 6), fr(1, 6))))
    # bigger or smaller, no calculation
    q = "A sunflower is 10 cm tall. Next week it will be %s times as tall. Which is true?" % mixed(1, 1, 4)
    its.append(mcq(q, "It will be taller than 10 cm",
                   ["It will be shorter than 10 cm", "It will be exactly 10 cm", "It will be %s cm taller" % mixed(1, 1, 4)],
                   "%s is greater than 1, so the sunflower will be <b>taller than 10 cm</b>. It grows by %s of 10 cm "
                   "(%s cm), not by %s cm." % (mixed(1, 1, 4), fr(1, 4), mixed(2, 1, 2), mixed(1, 1, 4))))
    a, ah, _ = Pp.next()
    b, bh, _ = Pp.next()
    q = ("%s makes %s of a cookie recipe. %s makes %s of the same recipe. Who uses more sugar?"
         % (a, fr(3, 4), b, fr(5, 4)))
    its.append(mcq(q, b, [a, "They use the same", "Cannot tell yet"],
                   "%s is less than 1 and %s is greater than 1, so <b>%s</b> uses more. You do not need to know "
                   "how much sugar the recipe uses." % (fr(3, 4), fr(5, 4), b)))
    nm, he, his = Pp.next()
    q = "A bottle holds %s liter of water. %s drinks %s of it. Without multiplying, how much does %s drink?" % (
        fr(3, 4), nm, fr(2, 3), he)
    its.append(mcq(q, "Less than %s liter" % fr(3, 4),
                   ["More than %s liter" % fr(3, 4), "Exactly %s liter" % fr(3, 4), "Cannot tell yet"],
                   "%s is less than 1, so %s of %s liter is <b>less than %s liter</b>. (It is %s liter.)"
                   % (fr(2, 3), fr(2, 3), fr(3, 4), fr(3, 4), fr(1, 2))))
    nm, he, his = Pp.next()
    q = "%s wants to make a photo smaller. Which could %s multiply its width by?" % (nm, he)
    its.append(mcq(q, "× %s" % fr(4, 5), ["× %s" % fr(5, 4), "× %s" % mixed(1, 1, 2), "× %s" % fr(6, 6)],
                   "To make it smaller, multiply by a number less than 1: <b>%s</b>. %s and %s make it bigger, and %s keeps "
                   "it the same." % (fr(4, 5), fr(5, 4), mixed(1, 1, 2), fr(6, 6))))
    q = ("A giraffe is 18 feet tall. A tree is %s times as tall as the giraffe. A bush is %s as tall as the giraffe. "
         "Which list goes from shortest to tallest?" % (mixed(1, 1, 3), fr(1, 3)))
    its.append(mcq(q, "bush, giraffe, tree", ["giraffe, bush, tree", "tree, giraffe, bush", "bush, tree, giraffe"],
                   "The bush is %s of 18 (less than 18), the tree is %s times 18 (more than 18). So the order is "
                   "<b>bush, giraffe, tree</b>: 6 ft, 18 ft, 24 ft." % (fr(1, 3), mixed(1, 1, 3))))
    nm, he, his = Pp.next()
    q = ("%s draws a rectangle 6 cm long and 4 cm wide. Then %s draws a copy that is %s times as long on each side. "
         "What are the sides of the copy?" % (nm, he, mixed(1, 1, 2)))
    its.append(mcq(q, "9 cm and 6 cm", ["%s cm and %s cm" % (mixed(7, 1, 2), mixed(5, 1, 2)),
                                         "4 cm and %s cm" % mixed(2, 2, 3),
                                         "%s cm and %s cm" % (mixed(6, 1, 2), mixed(4, 1, 2))],
                   "%s is greater than 1, so both sides get longer. %s × 6 = 6 + 3 = 9 and %s × 4 = 4 + 2 = 6. "
                   "The copy is <b>9 cm and 6 cm</b>. (Do not add %s or %s to each side.)"
                   % (mixed(1, 1, 2), mixed(1, 1, 2), mixed(1, 1, 2), mixed(1, 1, 2), fr(1, 2))))
    nm, he, his = Pp.next()
    q = ("%s copies a drawing at %s size. Then %s copies the copy at %s size. How does the last copy compare with the "
         "first drawing?" % (nm, fr(2, 3), he, fr(3, 2)))
    its.append(mcq(q, "It is the same size", ["It is bigger", "It is smaller", "Cannot tell yet"],
                   "%s × %s = %s, and %s = 1. Multiplying by 1 does not change the size, so the last copy is "
                   "<b>the same size</b> as the first drawing." % (fr(2, 3), fr(3, 2), fr(6, 6), fr(6, 6))))
    assert len(its) == 20, len(its)
    return {"title": "Scaling stories", "items": its}


# ============================================================ lesson
def body_html():
    three = bars_svg([(["12"], 4, 4, F(1), LIGHT),
                      ([(0, 3, 4), "×", "12"], 3, 3, F(3, 4), DARK),
                      ([(0, 5, 4), "×", "12"], 5, 5, F(5, 4), DARK)],
                     "scaling bar model: 12, 3/4 times 12 and 5/4 times 12")
    fig1 = ("<figure class='sn-fig'>" + three + "<figcaption>The dashed line marks 12. " + fr(3, 4) + " × 12 stops before it "
            "(3 of the 4 parts). " + fr(5, 4) + " × 12 goes past it (5 parts).</figcaption></figure>")
    fig2 = ("<figure class='sn-fig'>" + equiv_svg(2, 3, 4) + "<figcaption>" + fr(2, 3) + " × " + fr(4, 4) + " = "
            + fr(8, 12) + ". The bars are the same length: each third is cut into 4 smaller parts.</figcaption></figure>")
    return (
        "<h2>The big idea</h2>"
        "<p>Multiplying can <b>resize</b> a number. The other factor tells you how:</p>"
        + table(["Multiply by", "The product is", "Example with 12"], [
            ["a number greater than 1", "greater than 12", fr(5, 4) + " × 12 = 15"],
            ["a number less than 1", "less than 12", fr(3, 4) + " × 12 = 9"],
            ["a number equal to 1", "equal to 12", fr(4, 4) + " × 12 = 12"],
        ])
        + "<p>A fraction is greater than 1 when the top is greater than the bottom (" + fr(5, 4) + "), "
        "less than 1 when the top is less (" + fr(3, 4) + "), and equal to 1 when they are the same (" + fr(4, 4) + ").</p>"
        "<h2>See it with bars</h2>" + fig1 +
        "<h2>Compare without multiplying</h2>"
        "<p>To compare a product with one factor, look at the <b>other</b> factor.</p>"
        + ex("Example", "Which is greater: " + fr(5, 6) + " × 9 or " + fr(7, 6) + " × 9?",
             fr(5, 6) + " is less than 1, so " + fr(5, 6) + " × 9 is less than 9. " + fr(7, 6)
             + " is greater than 1, so " + fr(7, 6) + " × 9 is greater than 9.", fr(7, 6) + " × 9")
        + ex("Example", "Is " + fr(3, 4) + " × " + fr(2, 3) + " greater or less than " + fr(2, 3) + "?",
             "Look at the other factor, " + fr(3, 4) + ". It is less than 1, so the product is less than " + fr(2, 3) + ".",
             "less than " + fr(2, 3))
        + "<h2>Multiplying by 1 in disguise</h2>"
        "<p>" + fr(2, 2) + ", " + fr(3, 3) + ", " + fr(4, 4) + " and " + fr(5, 5) + " are all equal to 1. "
        "Multiplying by them does not change the value. It only cuts the parts smaller. That is why "
        "equivalent fractions are equal.</p>" + fig2 +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["“Multiplying always makes a number bigger.”", fr(1, 2) + " × 10 = 5. Times less than 1 makes it smaller."],
            ["“" + fr(3, 5) + " × 10 is greater than " + fr(3, 4) + " × 10 because 5 &gt; 4.”",
             "A bigger bottom number means smaller parts: " + fr(3, 5) + " &lt; " + fr(3, 4)],
            ["“" + fr(8, 12) + " is greater than " + fr(2, 3) + " because 8 &gt; 2.”",
             fr(2, 3) + " × " + fr(4, 4) + " = " + fr(8, 12) + ", and " + fr(4, 4) + " = 1, so they are equal"],
            [mixed(1, 1, 2) + " × 8 = " + mixed(8, 1, 2), "Take 8, then add " + fr(1, 2) + " of 8: 8 + 4 = 12"],
        ])
    )


FAQ = [
    {"q": "What does multiplication as scaling mean?",
     "a": "It means thinking of multiplication as resizing a number. Multiplying by a number greater than 1 makes it bigger, by a number less than 1 makes it smaller, and by 1 keeps it the same."},
    {"q": "Does multiplying by a fraction always make a number smaller?",
     "a": "No. Only fractions less than 1 make it smaller: 3/4 × 12 = 9. A fraction greater than 1 makes it bigger: 5/4 × 12 = 15."},
    {"q": "How can you compare products without multiplying?",
     "a": "Look at the other factor. 5/6 × 9 is less than 9 because 5/6 is less than 1, and 7/6 × 9 is greater than 9 because 7/6 is greater than 1."},
    {"q": "Why does multiplying by 4/4 give an equivalent fraction?",
     "a": "4/4 is equal to 1, and multiplying by 1 does not change a number. So 2/3 × 4/4 = 8/12 is the same amount as 2/3, cut into smaller parts."},
]


def gen():
    rnd = random.Random(513)
    Pp = People(rnd)
    sets = [set_compare_one(rnd), set_compare_two(rnd), set_times_one(rnd, Pp), set_explain(rnd, Pp), set_stories(rnd, Pp)]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    return {
        "country": "us", "subject": "math", "grade": "grade-5", "slug": "multiplication-as-scaling", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiplication as Scaling",
        "seo_title": "Grade 5 Multiplication as Scaling Worksheets: Compare Products Without Multiplying, Fractions Greater or Less Than 1",
        "short_title": "Multiplication as scaling",
        "domain": "Number and Operations—Fractions",
        "standard_code": "5.NF.B.5",
        "standard_url": "https://www.thecorestandards.org/Math/Content/5/NF/B/5/",
        "standard_text": "Interpret multiplication as scaling (resizing), by: Comparing the size of a product to the size of one factor on the basis of the size of the other factor, without performing the indicated multiplication. Explaining why multiplying a given number by a fraction greater than 1 results in a product greater than the given number; explaining why multiplying a given number by a fraction less than 1 results in a product smaller than the given number; and relating the principle of fraction equivalence a/b = (n×a)/(n×b) to the effect of multiplying a/b by 1.",
        "meta_desc": "Free Grade 5 worksheets on multiplication as scaling: decide if a product is greater than, less than or equal to a number without multiplying, compare and order products, see equivalent fractions as multiplying by 1, explain mistakes and solve resizing word problems. 100 practice questions with answers.",
        "key_big": "Times more than 1 → bigger. Times less than 1 → smaller. Times 1 → the same.",
        "key_sub": "5/4 × 12 = 15 is greater than 12; 3/4 × 12 = 9 is less than 12; 4/4 × 12 = 12. To compare a product with one factor, look at the other factor.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "scaling bar model")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
