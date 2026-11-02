# -*- coding: utf-8 -*-
"""
US Grade 5 Math: Fractions as Division (5.NF.B.3)
  python tools/gen_us_math_g5_fractions_division.py
a/b = a ÷ b. 3 pizzas shared by 4 friends: each gets 3/4 of a pizza.
17 ÷ 5 = 17/5 = 3 2/5 (the remainder 2 is shared by 5, so it becomes 2/5).
Answers are in simplest form (mixed numbers when more than 1). Every value is checked with Fraction.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-5")
UPDATED = "2026-11-02"
DARK = "#4fae74"      # one friend's share
LIGHT = "#e3f2e8"     # the other pieces
LINE = "#2b2b2b"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def f(n):
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


def dv(a, b):
    return "%d ÷ %d" % (a, b)


def mcq(q, correct, cands, e):
    """correct and cands are (html, value) pairs (value may be None). A candidate with the same text
    or the same value as an earlier choice is skipped, so no two choices are worth the same."""
    ch, vals = [correct[0]], [correct[1]]
    for h, v in cands:
        if not h or h in ch or (v is not None and v in vals):
            continue
        ch.append(h)
        vals.append(v)
        if len(ch) == 4:
            break
    assert len(ch) == 4, (q, correct, cands)
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
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag sharing pictures (many small pieces) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ figures
def circles_svg(a, b, R=30, colors=None):
    """a circles (pizzas), each cut into b equal slices. Slice 0 of every circle is dark (one friend's share).
    colors: optional list of b fills, slice k of every circle gets colors[k]."""
    G, PAD = 12, 4
    s = []
    for i in range(a):
        cx = PAD + R + i * (2 * R + G)
        cy = PAD + R
        for k in range(b):
            t0 = -math.pi / 2 + 2 * math.pi * k / b
            t1 = -math.pi / 2 + 2 * math.pi * (k + 1) / b
            x0, y0 = cx + R * math.cos(t0), cy + R * math.sin(t0)
            x1, y1 = cx + R * math.cos(t1), cy + R * math.sin(t1)
            fill = colors[k] if colors else (DARK if k == 0 else LIGHT)
            s.append("<path d='M%.1f %.1f L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1.6' "
                     "stroke-linejoin='round'/>" % (cx, cy, x0, y0, R, R, x1, y1, fill, LINE))
        s.append("<circle cx='%d' cy='%d' r='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (cx, cy, R, LINE))
    W = 2 * PAD + a * 2 * R + (a - 1) * G
    return svg_wrap(W, 2 * PAD + 2 * R, "".join(s),
                    "%d circles, each cut into %d equal slices, one slice of each circle dark" % (a, b))


def bars_svg(a, b, BW=80, BH=26, per=None):
    """a bars, each cut into b equal parts; part 0 of every bar is dark. Up to 5 bars in one row, else two rows."""
    G, PAD = 12, 4
    if per is None:
        per = a if a <= 5 else (a + 1) // 2
    rows = (a + per - 1) // per
    cols = min(a, per)
    s = []
    pw = BW / float(b)
    for i in range(a):
        x0 = PAD + (i % per) * (BW + G)
        y0 = PAD + (i // per) * (BH + G)
        for k in range(b):
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
                     % (x0 + k * pw, y0, pw, BH, DARK if k == 0 else LIGHT, LINE))
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (x0, y0, BW, BH, LINE))
    W = 2 * PAD + cols * BW + (cols - 1) * G
    H = 2 * PAD + rows * BH + (rows - 1) * G
    return svg_wrap(W, H, "".join(s), "%d bars, each cut into %d equal parts, one part of each bar dark" % (a, b))


def model(kind, a, b):
    return circles_svg(a, b) if kind == "c" else bars_svg(a, b)


# ------------------------------------------------------------ typical wrong answers for a ÷ b
def wrongs(a, b, order, unit=None, flip_frac=False):
    """(html, value) pairs from real mistakes, in the order given."""
    q, r = divmod(a, b)
    out = []
    for k in order:
        v = h = None
        if k == "flip":                       # b ÷ a: divided the other way
            v = F(b, a)
            if flip_frac:
                h = fr(b, a)
        elif k == "oneb":                     # one piece only: 1/b
            v = F(1, b)
        elif k == "remq":                     # remainder over the quotient: 17 ÷ 5 = 3 2/3
            if q > 1 and 0 < r < q:
                v, h = q + F(r, q), mixed(q, r, q)
        elif k == "rema":                     # remainder over the number divided: 17 ÷ 5 = 3 2/17
            if q > 0 and r:
                v, h = q + F(r, a), mixed(q, r, a)
        elif k == "quot":                     # dropped the remainder: 17 ÷ 5 = 3
            if q > 0 and r:
                v = F(q)
        elif k == "dec":                      # wrote 3 R 2 as 3.2
            if q > 0 and 0 < r < 10:
                v, h = F(10 * q + r, 10), "%d.%d" % (q, r)
        elif k == "zero":                     # "you can't share 3 by 4"
            if a < b:
                v, h = F(0), "0"
        elif k == "whole_a":                  # counted pieces: a
            v = F(a)
        elif k == "onea":
            v = F(1, a)
        else:
            raise ValueError(k)
        if v is None:
            continue
        if h is None:
            h = show(v)
        out.append((qty(h, v, unit) if unit else h, v))
    return out


UNITS = {"foot": ("foot", "feet"), "liter": ("liter", "liters"), "mile": ("mile", "miles"),
         "dollar": ("dollar", "dollars"), "cup": ("cup", "cups"), "gallon": ("gallon", "gallons"),
         "pound": ("pound", "pounds"), "hour": ("hour", "hours"), "quart": ("quart", "quarts"),
         "meter": ("meter", "meters"), "lap": ("lap", "laps"),
         "pizza": ("of a pizza", "pizzas", "pizza"), "loaf": ("of a loaf", "loaves", "loaf"),
         "bar": ("of a bar", "bars", "bar"), "pie": ("of a pie", "pies", "pie"),
         "sandwich": ("of a sandwich", "sandwiches", "sandwich")}


def qty(h, v, unit):
    """3/4 cup, 1 1/2 cups, 3/4 of a pizza, 1 1/2 pizzas."""
    u = UNITS[unit]
    if v == 1:
        return "1 %s" % (u[2] if len(u) == 3 else u[0])
    return "%s %s" % (h, u[0] if v < 1 else u[1])


def share_e(a, b, unit=None, what="the answer is"):
    """a ÷ b = a/b, then the mixed number from the remainder. what: 'each piece is', 'each friend gets', ..."""
    v = F(a, b)
    ans = show(v)
    if unit:
        ans = qty(ans, v, unit)
    s = "%s = %s. " % (dv(a, b), fr(a, b))
    q, r = divmod(a, b)
    if q == 0:
        s += "%d is less than %d, so the answer is less than 1. " % (a, b)
    else:
        rb = fr(r, b) if math.gcd(r, b) == 1 else "%s = %s" % (fr(r, b), show(F(r, b)))
        s += ("%s = %d R %d: %d %s, and the %d left over %s shared by %d, which is %s. "
              % (dv(a, b), q, r, q, "whole" if q == 1 else "wholes", r, "is" if r == 1 else "are", b, rb))
    return s + ("So %s <b>%s</b>." % (what, ans) if q else "%s <b>%s</b>." % (cap(what), ans))


def short_e(a, b):
    q, r = divmod(a, b)
    if q == 0:
        return "%s = <b>%s</b>." % (dv(a, b), fr(a, b))
    return ("%s = %d R %d, and the %d left over %s shared by %d: %s. So %s = <b>%s</b>."
            % (dv(a, b), q, r, r, "is" if r == 1 else "are", b, fr(r, b), dv(a, b), show(F(a, b))))


# ============================================================ set 1: a/b = a ÷ b
def set_meaning():
    its = []
    for a, b in [(3, 4), (5, 8), (2, 3), (9, 10), (7, 3)]:
        q = "Which division means the same as %s?" % fr(a, b)
        e = ("The fraction bar means divide: the top number ÷ the bottom number. So %s = <b>%s</b>. "
             "(%s is %s, the other way around.)" % (fr(a, b), dv(a, b), dv(b, a), show(F(b, a))))
        its.append(mcq(q, (dv(a, b), F(a, b)),
                       [(dv(b, a), F(b, a)), ("%d × %d" % (a, b), F(a * b)), (dv(1, b), F(1, b))], e))
    for a, b in [(2, 5), (4, 7), (5, 6), (8, 3), (11, 4)]:
        q = "%s = <b>?</b>" % dv(a, b)
        if a < b:
            order = ["flip", "zero", "oneb"]
            e = ("Write the number you divide on top and the number you divide by on the bottom: %s = <b>%s</b>. "
                 "You can divide a smaller number by a bigger one; the answer is less than 1." % (dv(a, b), fr(a, b)))
        else:
            order = ["flip", "dec", "quot", "oneb"]
            e = ("Write the number you divide on top: %s = <b>%s</b>. As a mixed number, %s = %s." % (
                dv(a, b), fr(a, b), fr(a, b), show(F(a, b))))
        its.append(mcq(q, (fr(a, b), F(a, b)), wrongs(a, b, order, flip_frac=True), e))
    for a, b in [(12, 4), (18, 6), (20, 5), (14, 7)]:
        q = "%s = <b>?</b>" % fr(a, b)
        e = "The fraction bar means divide: %s = %s = <b>%d</b>. Check: %d × %d = %d." % (fr(a, b), dv(a, b), a // b, a // b, b, a)
        its.append(mcq(q, (str(a // b), F(a // b)),
                       [(str(a - b), F(a - b)), (str(a * b), F(a * b)), (fr(1, a // b), F(1, a // b))], e))
    for a, b in [(3, 5), (7, 2), (4, 9)]:
        q = "Which equation is true?"
        right = "%s = %s" % (dv(a, b), fr(a, b))
        wrong = ["%s = %s" % (dv(a, b), fr(b, a)), "%s = %s" % (dv(b, a), fr(a, b)), "%s = %s" % (dv(a, b), fr(1, b))]
        e = ("A fraction is the top number divided by the bottom number, in the same order: %s = %s. "
             "%s would be %s." % (dv(a, b), fr(a, b), dv(b, a), fr(b, a)))
        its.append(mcq(q, (right, None), [(w, None) for w in wrong], e))
    its.append(mcq("<b>?</b> ÷ 6 = %s" % fr(5, 6), ("5", F(5)), [("6", F(6)), ("30", F(30)), ("11", F(11))],
                   "%s means 5 ÷ 6, so the missing number is <b>5</b>." % fr(5, 6)))
    its.append(mcq("9 ÷ <b>?</b> = %s" % fr(9, 10), ("10", F(10)), [("9", F(9)), ("90", F(90)), ("19", F(19))],
                   "%s means 9 ÷ 10, so the missing number is <b>10</b>." % fr(9, 10)))
    its.append(mcq("<b>?</b> ÷ 3 = %s" % fr(4, 3), ("4", F(4)), [("3", F(3)), ("12", F(12)), ("7", F(7))],
                   "%s means 4 ÷ 3, so the missing number is <b>4</b>. (As a mixed number, %s = %s.)"
                   % (fr(4, 3), fr(4, 3), mixed(1, 1, 3))))
    assert len(its) == 20, len(its)
    return {"title": "A fraction means division", "items": its}


# ============================================================ set 2: sharing models
def set_models():
    its = []
    stories = {
        "pizza": ("pizzas", "pizza", "friends"), "pie": ("pies", "pie", "people"),
        "bar": ("granola bars", "bar", "children"), "sandwich": ("sandwiches", "sandwich", "friends"),
        "loaf": ("loaves of bread", "loaf", "families"),
    }
    SING = {"friends": "friend", "people": "person", "children": "child", "families": "family"}
    items = [("c", "pizza", 3, 4), ("c", "pie", 2, 3), ("c", "pizza", 2, 5), ("c", "pie", 3, 8),
             ("c", "pizza", 4, 5), ("c", "pie", 5, 6),
             ("b", "bar", 5, 3), ("b", "sandwich", 7, 4), ("b", "loaf", 4, 3), ("b", "bar", 5, 2), ("b", "sandwich", 3, 2)]
    for kind, thing, a, b in items:
        many, one, who = stories[thing]
        each = SING[who]
        cut = "slices" if kind == "c" else "parts"
        q = (fig(model(kind, a, b)) + "%d %s are shared equally by %d %s. Each %s is cut into %d equal %s, and the dark "
             "%s go to one %s. How much does each %s get?" % (a, many, b, who, one, b, cut, cut, each, each))
        v = F(a, b)
        if a < b:
            order = ["oneb", "flip", "whole_a", "onea"]
        else:
            order = ["flip", "rema", "remq", "quot", "oneb"]
        e = ("Each %s gets 1 %s from each of the %d %s: %d %s, each %s of a %s. That is %s, so %s = %s."
             % (each, cut[:-1], a, many, a, cut, fr(1, b), one, fr(a, b), dv(a, b), fr(a, b)))
        if a > b:
            e += " %s = %d R %d, so %s = <b>%s</b>." % (dv(a, b), a // b, a % b, fr(a, b), qty(show(v), v, thing))
        else:
            e += " Each %s gets <b>%s</b>." % (each, qty(show(v), v, thing))
        its.append(mcq(q, (qty(show(v), v, thing), v), wrongs(a, b, order, thing), e))
    for kind, thing, a, b in [("c", "pizza", 3, 7), ("c", "pie", 5, 8), ("b", "sandwich", 6, 5), ("b", "bar", 5, 4)]:
        many, one, who = stories[thing]
        q = (fig(model(kind, a, b)) + "The picture shows %d %s shared equally by %d %s. Which division gives one share?"
             % (a, many, b, who))
        e = ("Divide the %s by the number of %s: %s = %s %s for each. The dark pieces show one share."
             % (many, who, dv(a, b), show(F(a, b)), UNITS[thing][0] if a <= b else UNITS[thing][1]))
        its.append(mcq(q, (dv(a, b), F(a, b)),
                       [(dv(b, a), F(b, a)), ("%d × %d" % (a, b), F(a * b)), (dv(1, b), F(1, b))], e))
    # work backward
    rev = [
        ("Some pizzas are shared equally by 8 friends. Each friend gets %s of a pizza. How many pizzas are shared?" % fr(3, 8),
         3, [8, 24, 5], "Each friend gets %s = 3 ÷ 8, so <b>3</b> pizzas are shared by 8 friends." % fr(3, 8)),
        ("3 pies are shared equally. Each person gets %s of a pie. How many people share the pies?" % fr(3, 5),
         5, [3, 15, 2], "%s = 3 ÷ 5, so 3 pies are shared by <b>5</b> people." % fr(3, 5)),
        ("Some loaves of bread are shared equally by 4 families. Each family gets %s loaves. How many loaves are shared?" % mixed(1, 3, 4),
         7, [4, 3, 28], "%s = %s = 7 ÷ 4, so <b>7</b> loaves are shared by 4 families." % (mixed(1, 3, 4), fr(7, 4))),
        ("5 sandwiches are shared equally. Each friend gets %s of a sandwich. How many friends share the sandwiches?" % fr(5, 6),
         6, [5, 30, 11], "%s = 5 ÷ 6, so 5 sandwiches are shared by <b>6</b> friends." % fr(5, 6)),
        ("Some cakes are shared equally by 3 teams. Each team gets %s of a cake. How many cakes are shared?" % fr(2, 3),
         2, [3, 6, 1], "%s = 2 ÷ 3, so <b>2</b> cakes are shared by 3 teams." % fr(2, 3)),
    ]
    for q, ans, wr, e in rev:
        its.append(mcq(q, (str(ans), F(ans)), [(str(w), F(w)) for w in wr], e))
    assert len(its) == 20, len(its)
    return {"title": "Share wholes equally", "items": its}


# ============================================================ set 3: mixed numbers from division
def set_mixed():
    its = []
    orders = [["remq", "rema", "quot", "dec", "flip"], ["dec", "remq", "quot", "rema", "flip"],
              ["rema", "quot", "remq", "flip", "dec"], ["quot", "dec", "rema", "remq", "flip"]]
    for i, (a, b) in enumerate([(17, 5), (23, 4), (11, 3), (19, 6), (29, 8), (13, 2), (31, 7), (26, 9)]):
        v = F(a, b)
        q = "Write the answer as a mixed number.<br>%s = <b>?</b>" % dv(a, b)
        its.append(mcq(q, (show(v), v), wrongs(a, b, orders[i % 4]), share_e(a, b)))
    for i, (a, b) in enumerate([(22, 5), (14, 3), (25, 6), (39, 8)]):
        v = F(a, b)
        qq, r = divmod(a, b)
        q = "Write %s as a mixed number." % fr(a, b)
        e = ("%s means %s. %s = %d R %d: %d wholes, and the %d left over %s %s. So %s = <b>%s</b>."
             % (fr(a, b), dv(a, b), dv(a, b), qq, r, qq, r, "is" if r == 1 else "are", fr(r, b), fr(a, b), show(v)))
        its.append(mcq(q, (show(v), v), wrongs(a, b, orders[(i + 1) % 4]), e))
    for w, r, b in [(4, 1, 3), (2, 3, 7), (5, 1, 4), (3, 3, 4)]:
        a = w * b + r
        q = "Which division has the answer %s?" % mixed(w, r, b)
        e = ("Multiply the whole number by the divisor and add the remainder: %d × %d + %d = %d. "
             "So <b>%s</b> = %d R %d = %s." % (w, b, r, a, dv(a, b), w, r, mixed(w, r, b)))
        its.append(mcq(q, (dv(a, b), F(a, b)),
                       [(dv(w * b, b), F(w)), (dv(w * b - r, b), F(w * b - r, b)), (dv(b, a), F(b, a))], e))
    for a, b in [(26, 4), (33, 6), (38, 8), (22, 6)]:
        qq, r = divmod(a, b)
        v = F(a, b)
        q = "%s = %d R %d. Write %s as a mixed number in simplest form." % (dv(a, b), qq, r, dv(a, b))
        e = ("The %d left over %s shared by %d: %s = %s. So %s = %s = <b>%s</b>."
             % (r, "is" if r == 1 else "are", b, fr(r, b), show(F(r, b)), dv(a, b), mixed(qq, r, b), show(v)))
        cands = []
        if r < qq:
            cands.append((mixed(qq, r, qq), qq + F(r, qq)))
        cands += [("%d.%d" % (qq, r), F(10 * qq + r, 10)), (mixed(qq, r, a), qq + F(r, a)), (str(qq), F(qq)),
                  (mixed(qq, 1, r), qq + F(1, r))]
        its.append(mcq(q, (show(v), v), cands, e))
    assert len(its) == 20, len(its)
    return {"title": "Mixed numbers from division", "items": its}


# ============================================================ set 4: estimate, compare, find mistakes
def set_reason(P):
    its = []
    for a, b in [(23, 4), (22, 7), (38, 5), (3, 8), (19, 2), (41, 6), (13, 5)]:
        qq, r = divmod(a, b)

        def btw(n):
            return "%d and %d" % (n, n + 1)
        q = "%s is between which two whole numbers?" % dv(a, b)
        cands = []
        fq = b // a
        if qq >= 1:
            cands += [btw(qq - 1), btw(qq + 1), btw(fq)]
        else:
            cands += [btw(fq), btw(1), btw(a)]
        cands.append(btw(r))
        if qq == 0:
            e = "%s = %s. The top number is less than the bottom number, so it is less than 1: between <b>0 and 1</b>." % (dv(a, b), fr(a, b))
        else:
            e = ("%s = %d R %d, so %s = %s. That is more than %d but less than %d: between <b>%s</b>."
                 % (dv(a, b), qq, r, dv(a, b), show(F(a, b)), qq, qq + 1, btw(qq)))
        its.append(mcq(q, (btw(qq), None), [(c, None) for c in cands], e))

    pairs = [((5, 6), (6, 5)), ((3, 8), (3, 4)), ((8, 3), (7, 3)), ((9, 4), (18, 8)), ((5, 2), (11, 4))]
    notes = ["%s is less than 1 and %s is more than 1." % (fr(5, 6), fr(6, 5)),
             "Sharing 3 among 8 gives smaller shares than sharing 3 among 4.",
             "Both are thirds, and 8 thirds is more than 7 thirds.",
             "",
             "%s = %s and %s = %s." % (mixed(2, 1, 2), mixed(2, 2, 4), fr(11, 4), mixed(2, 3, 4))]
    for ((x1, x2), (y1, y2)), note in zip(pairs, notes):
        xv, yv = F(x1, x2), F(y1, y2)
        x, y = dv(x1, x2), dv(y1, y2)
        q = "Which is greater: %s or %s?" % (x, y)
        e = "%s = %s and %s = %s. " % (x, show(xv), y, show(yv))
        if xv == yv:
            right = "They are equal."
            e += "%s = %s, so <b>they are equal</b>." % (fr(y1, y2), fr(x1, x2))
        else:
            right = x if xv > yv else y
            e += "<b>%s</b> is greater. %s" % (right, note)
        its.append(mcq(q, (right, None), [(c, None) for c in [x, y, "They are equal.", "You can’t tell."]], e.strip()))

    nots = [
        ((7, 2), [fr(7, 2), mixed(3, 1, 2), "3.5"], fr(2, 7),
         "%s = %s = %s = 3.5. <b>%s</b> is 2 ÷ 7, which is less than 1." % (dv(7, 2), fr(7, 2), mixed(3, 1, 2), fr(2, 7))),
        ((9, 4), [fr(9, 4), mixed(2, 1, 4), fr(18, 8)], mixed(2, 1, 2),
         "%s = %s = %s = %s. <b>%s</b> puts the remainder 1 over 2 instead of over 4." % (dv(9, 4), fr(9, 4), mixed(2, 1, 4), fr(18, 8), mixed(2, 1, 2))),
        ((11, 3), [fr(11, 3), mixed(3, 2, 3), fr(22, 6)], mixed(3, 2, 11),
         "%s = %s = %s = %s. <b>%s</b> puts the remainder over 11 instead of over 3." % (dv(11, 3), fr(11, 3), mixed(3, 2, 3), fr(22, 6), mixed(3, 2, 11))),
        ((5, 8), [fr(5, 8), fr(10, 16), fr(15, 24)], fr(8, 5),
         "%s = %s = %s = %s. <b>%s</b> is 8 ÷ 5, which is more than 1." % (dv(5, 8), fr(5, 8), fr(10, 16), fr(15, 24), fr(8, 5))),
    ]
    for (a, b), eq, odd, e in nots:
        q = "Which is <b>not</b> equal to %s?" % dv(a, b)
        its.append({"q": q, "c": [odd] + eq, "a": 0, "e": e})

    M = {"remq": "put the remainder over the quotient", "dec": "wrote the remainder after a decimal point",
         "flip": "divided the other way", "ok": "nothing; the answer is correct"}
    for kind, a, b, wrote in [("remq", 13, 4, mixed(3, 1, 3)), ("dec", 17, 5, "3.2"), ("flip", 3, 7, fr(7, 3)),
                              ("ok", 22, 5, mixed(4, 2, 5))]:
        nm, he, his = P.next()
        q = "%s says %s = %s. What did %s do?" % (nm, dv(a, b), wrote, he)

        def say(k):
            return cap(M[k]) + "." if k == "ok" else "%s %s." % (cap(he), M[k])
        right = say(kind)
        wrong = [say(k) for k in ["ok", "remq", "dec", "flip"] if k != kind]
        good = short_e(a, b)
        if kind == "remq":
            e = "The remainder is shared by the divisor 4, not by the quotient 3. 13 ÷ 4 = 3 R 1, so 13 ÷ 4 = <b>%s</b>." % mixed(3, 1, 4)
        elif kind == "dec":
            e = "3 R 2 is not 3.2. %s (As a decimal, that is 3.4.)" % good
        elif kind == "flip":
            e = "%s found 7 ÷ 3. The first number goes on top. %s" % (nm, good)
        else:
            e = "%s is right. %s" % (nm, good)
        its.append(mcq(q, (right, None), [(w, None) for w in wrong], e))
    assert len(its) == 20, len(its)
    return {"title": "Estimate, compare and find mistakes", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []
    o1 = ["flip", "remq", "quot", "rema", "dec", "oneb"]
    o2 = ["rema", "flip", "dec", "quot", "remq", "oneb"]
    o3 = ["quot", "dec", "flip", "remq", "rema", "oneb"]
    op = ["oneb", "flip", "whole_a", "onea"]

    def add(q, a, b, unit, order, what, extra=""):
        v = F(a, b)
        its.append(mcq(q, (qty(show(v), v, unit), v), wrongs(a, b, order, unit), share_e(a, b, unit, what) + extra))

    nm, he, his = P.next()
    add("%s has 7 feet of ribbon. %s cuts it into 4 equal pieces. How long is each piece?" % (nm, cap(he)),
        7, 4, "foot", o1, "each piece is")
    add("3 liters of juice are poured equally into 4 bottles. How much juice is in each bottle?",
        3, 4, "liter", op, "each bottle gets")
    add("A relay team of 3 runners runs 5 miles. Each runner runs the same distance. How far does each runner run?",
        5, 3, "mile", o2, "each runner runs")
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    add("%s, %s and two friends share $9 equally. How many dollars does each person get?" % (n1, n2),
        9, 4, "dollar", ["rema", "quot", "remq", "flip", "oneb"], "each person gets", " (That is $2.25.)")
    add("2 cups of rice are split equally into 3 bowls. How much rice is in each bowl?",
        2, 3, "cup", op, "each bowl gets")
    add("6 friends share 5 pizzas equally. How much pizza does each friend get?",
        5, 6, "pizza", op, "each friend gets")
    nm, he, his = P.next()
    add("%s has 10 gallons of paint for 3 fences. %s uses the same amount on each fence. How much paint goes on each fence?"
        % (nm, cap(he)), 10, 3, "gallon", o1, "each fence gets")
    add("A family hikes a 9-mile trail over 2 days. They hike the same distance each day. How far do they hike each day?",
        9, 2, "mile", o3, "they hike")
    add("A teacher shares 6 pounds of clay equally among 5 students. How much clay does each student get?",
        6, 5, "pound", o2, "each student gets")
    nm, he, his = P.next()
    add("%s practices guitar for 3 hours in all over 4 days. %s practices the same amount each day. How long does %s practice each day?"
        % (nm, cap(he), he), 3, 4, "hour", op, "%s practices" % he, " (That is 45 minutes.)")
    add("15 quarts of lemonade are shared equally among 4 tables at a picnic. How much lemonade does each table get?",
        15, 4, "quart", o1, "each table gets")
    nm, he, his = P.next()
    add("%s cuts an 11-meter rope into 3 equal pieces. How long is each piece?" % nm,
        11, 3, "meter", o2, "each piece is")
    add("7 people share 4 loaves of bread equally. How much bread does each person get?",
        4, 7, "loaf", op, "each person gets")
    add("A track team runs 10 laps as a relay. Each of the 4 runners runs the same distance. How far does each runner run?",
        10, 4, "lap", o3, "each runner runs")

    nm, he, his = P.next()
    q = "%s shares 5 feet of ribbon equally among 8 friends. Which expression shows how much ribbon each friend gets?" % nm
    e = "Divide the ribbon by the number of friends: <b>5 ÷ 8</b> = %s foot each." % fr(5, 8)
    its.append(mcq(q, (dv(5, 8), F(5, 8)), [(dv(8, 5), F(8, 5)), ("5 × 8", F(40)), (dv(1, 8), F(1, 8))], e))
    q = "A farmer puts 7 pounds of beans into 3 bags with the same amount in each bag. Which expression shows the pounds in each bag?"
    e = "Divide the beans by the number of bags: <b>7 ÷ 3</b> = %s = %s pounds in each bag." % (fr(7, 3), mixed(2, 1, 3))
    its.append(mcq(q, (dv(7, 3), F(7, 3)), [(dv(3, 7), F(3, 7)), ("7 × 3", F(21)), (dv(1, 3), F(1, 3))], e))

    q = "6 friends share 4 pizzas equally. Does each friend get more or less than half a pizza?"
    e = ("4 ÷ 6 = %s = %s. Half a pizza is %s, and %s is more than %s, so each friend gets <b>more than half a pizza</b>."
         % (fr(4, 6), fr(2, 3), fr(3, 6), fr(4, 6), fr(3, 6)))
    its.append(mcq(q, ("More than half", None), [(c, None) for c in ["Less than half", "Exactly half", "A whole pizza"]], e))
    q = "4 people share 13 cups of soup equally. Each person’s soup is between which two amounts?"
    e = ("13 ÷ 4 = 3 R 1, so each person gets %s cups. That is between <b>3 and 4 cups</b>." % mixed(3, 1, 4))
    its.append(mcq(q, ("3 and 4 cups", None), [(c, None) for c in ["2 and 3 cups", "4 and 5 cups", "0 and 1 cup"]], e))

    q = ("At a party, 4 friends at the red table share 3 pizzas equally. 5 friends at the blue table share 4 pizzas equally. "
         "At which table does each friend get more pizza?")
    e = ("Red: 3 ÷ 4 = %s = %s. Blue: 4 ÷ 5 = %s = %s. %s is more than %s, so each friend at the <b>blue table</b> gets more."
         % (fr(3, 4), fr(15, 20), fr(4, 5), fr(16, 20), fr(16, 20), fr(15, 20)))
    its.append(mcq(q, ("The blue table", None), [(c, None) for c in ["The red table", "They get the same.", "You can’t tell."]], e))
    (n1, _, _), (n2, _, _) = P.next(), P.next()
    q = ("%s’s team of 3 shares 7 sandwiches equally. %s’s team of 4 shares 9 sandwiches equally. "
         "On which team does each person get more?" % (n1, n2))
    e = ("%s’s team: 7 ÷ 3 = %s. %s’s team: 9 ÷ 4 = %s. Both get 2 whole sandwiches, and %s is more than %s, "
         "so each person on <b>%s’s team</b> gets more." % (n1, mixed(2, 1, 3), n2, mixed(2, 1, 4), fr(1, 3), fr(1, 4), n1))
    its.append(mcq(q, ("%s’s team" % n1, None), [(c, None) for c in ["%s’s team" % n2, "They get the same.", "You can’t tell."]], e))
    assert len(its) == 20, len(its)
    return {"title": "Word problems", "items": its}


# ============================================================ lesson
def body_html():
    cols = ["#4fae74", "#f2b84b", "#6aa6e0", "#e57f6e"]
    pz = ("<figure class='sn-fig'>" + circles_svg(3, 4, R=44, colors=cols) +
          "<figcaption>3 pizzas for 4 friends. Cut each pizza into 4 slices; each friend gets one slice of each pizza "
          "(one color). That is 3 fourths: 3 ÷ 4 = " + fr(3, 4) + ".</figcaption></figure>")
    bars = ("<figure class='sn-fig'>" + bars_svg(5, 3, BW=96, BH=30, per=5) +
            "<figcaption>5 bars for 3 children. Each child gets one dark third from each bar: 5 thirds = "
            + fr(5, 3) + " = " + mixed(1, 2, 3) + " bars.</figcaption></figure>")
    return (
        "<h2>The big idea: the fraction bar means divide</h2>"
        "<p>A fraction is a division problem. The top number is divided by the bottom number.</p>"
        + table(["Fraction", "Division", "Read it as"], [
            [fr(3, 4), dv(3, 4), "3 shared equally by 4"],
            [fr(17, 5), dv(17, 5), "17 shared equally by 5"],
        ]) +
        "<h2>Sharing: 3 pizzas for 4 friends</h2>"
        "<p>You can share a smaller number by a bigger one. The answer is a fraction less than 1.</p>"
        + pz
        + bars
        + ex("Example", "4 friends share 3 pizzas equally. How much pizza does each friend get?",
             "Divide the pizzas by the friends: 3 ÷ 4 = " + fr(3, 4) + ".", fr(3, 4) + " of a pizza")
        + "<h2>Mixed numbers from division</h2>"
        "<p>Divide to get the whole number. The <b>remainder</b> is still shared, so it goes <b>over the divisor</b>.</p>"
        + table(["Division", "With a remainder", "As a mixed number"], [
            [dv(17, 5) + " = " + fr(17, 5), "3 R 2", mixed(3, 2, 5)],
            [dv(23, 4) + " = " + fr(23, 4), "5 R 3", mixed(5, 3, 4)],
        ])
        + ex("Example", "A 7-foot ribbon is cut into 4 equal pieces. How long is each piece?",
             "7 ÷ 4 = 1 R 3. Each piece gets 1 foot, and the 3 feet left over are split into 4 parts: " + fr(3, 4) + " foot each.",
             mixed(1, 3, 4) + " feet")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["3 ÷ 4 = " + fr(4, 3) + " (dividing the other way)", "The first number goes on top: 3 ÷ 4 = " + fr(3, 4) + "."],
            ["3 ÷ 4 = 0 (“you can’t share 3 by 4”)", "You can: each share is " + fr(3, 4) + "."],
            ["17 ÷ 5 = " + mixed(3, 2, 3) + " (remainder over the quotient)", "The remainder is shared by 5: " + mixed(3, 2, 5) + "."],
            ["17 ÷ 5 = 3.2 (3 R 2 written as a decimal)", "3 R 2 means 3 and " + fr(2, 5) + ", which is 3.4."],
            ["17 ÷ 5 = 3 (leaving out the remainder)", "Share the remainder too: " + mixed(3, 2, 5) + "."],
        ])
    )


FAQ = [
    {"q": "What does it mean to interpret a fraction as division?",
     "a": "It means a/b is the same as a ÷ b. For example, 3/4 = 3 ÷ 4: if 3 pizzas are shared equally by 4 people, each gets 3/4 of a pizza."},
    {"q": "How do you write a division answer as a mixed number?",
     "a": "Divide to get the whole number, then put the remainder over the divisor. 17 ÷ 5 = 3 R 2, so 17 ÷ 5 = 3 2/5."},
    {"q": "Can you divide a smaller number by a larger number?",
     "a": "Yes. The answer is a fraction less than 1. 2 ÷ 5 = 2/5, so 2 cookies shared by 5 children gives each child 2/5 of a cookie."},
    {"q": "Is 3 ÷ 4 the same as 4 ÷ 3?",
     "a": "No. 3 ÷ 4 = 3/4, which is less than 1, but 4 ÷ 3 = 4/3 = 1 1/3. The number you divide always goes on top."},
]


def gen():
    rnd = random.Random(512)
    P = People(rnd)
    sets = [set_meaning(), set_models(), set_mixed(), set_reason(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "us", "subject": "math", "grade": "grade-5", "slug": "fractions-as-division", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Fractions as Division",
        "seo_title": "Grade 5 Fractions as Division Worksheets: a/b = a ÷ b, Sharing Models, Mixed Numbers and Word Problems",
        "short_title": "Fractions as division",
        "domain": "Number and Operations—Fractions",
        "standard_code": "5.NF.B.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/5/NF/B/3/",
        "standard_text": "Interpret a fraction as division of the numerator by the denominator (a/b = a ÷ b). Solve word problems involving division of whole numbers leading to answers in the form of fractions or mixed numbers, e.g., by using visual fraction models or equations to represent the problem.",
        "meta_desc": "Free Grade 5 worksheets on fractions as division: see that 3/4 = 3 ÷ 4, share pizzas and bars with fraction models, turn 17 ÷ 5 into 3 2/5, compare quotients, and solve sharing word problems. 100 practice questions with answers.",
        "key_big": "A fraction is a division: 3/4 = 3 ÷ 4.",
        "key_sub": "3 pizzas shared by 4 friends gives each friend 3/4 of a pizza. With a remainder, put it over the divisor: 17 ÷ 5 = 3 R 2 = 3 2/5.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "[0-9]+ (circles|bars)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
