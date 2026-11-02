# -*- coding: utf-8 -*-
"""
US Grade 2 Math: Measuring Length (2.MD.A.1-4)
  python tools/gen_us_math_g2_measuring.py
Whole units only. Every object in a picture is drawn exactly from its start mark to its end mark,
and every length, difference and choice is computed in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#8a8a8a"
RULER = "#f6e7a8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]

UNITS = {"in": ("inch", "inches"), "cm": ("centimeter", "centimeters"), "ft": ("foot", "feet"),
         "yd": ("yard", "yards"), "m": ("meter", "meters")}
RULER_LABEL = {"in": "inches", "cm": "cm"}
# pixels per unit and length of the ruler, chosen so both rulers are the same width (360)
PU = {"in": 45, "cm": 24}
RLEN = {"in": 8, "cm": 15}


def u(n, unit):
    one, many = UNITS[unit]
    return "%d %s" % (n, one if n == 1 else many)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors (no 0 or negatives). Positions are set by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or re.match(r"^0\b", c):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def mcq_len(q, L, unit, cands, e):
    return mcq(q, u(L, unit), [u(c, unit) if isinstance(c, int) else c for c in cands
                               if not isinstance(c, int) or c > 0], e)


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
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


def count_list(n):
    return ", ".join(str(i) for i in range(1, n + 1))


# ------------------------------------------------------------ objects (drawn from x0 to x1 in the band yt..yb)
def draw_object(kind, x0, x1, yt, yb):
    ym = (yt + yb) / 2.0
    L = x1 - x0
    s = []
    if kind == "pencil":
        s.append("<rect x='%.1f' y='%.1f' width='9' height='%.1f' fill='#f2a7b5' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 2, yb - yt - 4, INK))
        s.append("<rect x='%.1f' y='%.1f' width='6' height='%.1f' fill='#b8b8b8' stroke='%s' stroke-width='1.2'/>" % (x0 + 9, yt + 1, yb - yt - 2, INK))
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#f4c430' stroke='%s' stroke-width='1.2'/>" % (x0 + 15, yt + 1, L - 33, yb - yt - 2, INK))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#e8c79a' stroke='%s' stroke-width='1.2' stroke-linejoin='round'/>"
                 % (x1 - 18, yt + 1, x1 - 18, yb - 1, x1, ym, INK))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (x1 - 6, ym - 3.6, x1 - 6, ym + 3.6, x1, ym, INK))
    elif kind == "crayon":
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='3' fill='#3d7cc9' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 2, L - 12, yb - yt - 4, INK))
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#9cc3ee'/>" % (x0 + 6, yt + 8, max(L - 26, 4), yb - yt - 16))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#3d7cc9' stroke='%s' stroke-width='1.2' stroke-linejoin='round'/>"
                 % (x1 - 12, yt + 4, x1 - 12, yb - 4, x1, ym + 2.5, x1, ym - 2.5, INK))
    elif kind == "leaf":
        xm = (x0 + x1) / 2
        s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z' fill='#7cc47f' stroke='%s' stroke-width='1.4'/>"
                 % (x0, ym, xm, yt - 9, x1, ym, xm, yb + 9, x0, ym, GREEN))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.2'/>" % (x0 + 2, ym, x1 - 3, ym, GREEN))
    elif kind == "nail":
        s.append("<rect x='%.1f' y='%.1f' width='4' height='%.1f' fill='#9aa0a6' stroke='%s' stroke-width='1.1'/>" % (x0, yt + 3, yb - yt - 6, INK))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#c3c7cb' stroke='%s' "
                 "stroke-width='1.1' stroke-linejoin='round'/>"
                 % (x0 + 4, ym - 3, x1 - 10, ym - 3, x1, ym, x1 - 10, ym + 3, x0 + 4, ym + 3, INK))
    elif kind == "ribbon":
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#e05a6a' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 6, L, yb - yt - 12, INK))
    elif kind == "paper strip":
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#cfe3f7' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 4, L, yb - yt - 8, INK))
    elif kind == "craft stick":
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='8' fill='#e6c88f' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 4, L, yb - yt - 8, INK))
    elif kind == "eraser":
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='3' fill='#f2a7b5' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 2, L, yb - yt - 4, INK))
    elif kind == "caterpillar":
        k = max(3, int(round(L / 15.0)))
        d = L / k
        for i in range(k):
            col = "#4e9a3f" if i == k - 1 else "#8cc63f"
            s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='1.1'/>"
                     % (x0 + d * (i + 0.5), ym + 2, min(d / 2 - 0.4, 10), col, GREEN))
        s.append("<circle cx='%.1f' cy='%.1f' r='1.6' fill='%s'/>" % (x1 - d * 0.35, ym, INK))
    elif kind == "marker":
        cw = min(0.3 * L, 45)
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='3' fill='#f4f4f4' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 3, L - cw, yb - yt - 6, INK))
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='4' fill='#2e8b57' stroke='%s' stroke-width='1.2'/>" % (x1 - cw, yt + 1, cw, yb - yt - 2, INK))
    elif kind == "straw":
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='#ffffff' stroke='%s' stroke-width='1.2'/>" % (x0, yt + 7, L, yb - yt - 14, INK))
        x = x0 + 6
        while x + 6 < x1:
            s.append("<rect x='%.1f' y='%.1f' width='6' height='%.1f' fill='#e05a6a'/>" % (x, yt + 7.6, yb - yt - 15.2))
            x += 14
    elif kind == "paper clip":
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='%.1f' fill='none' stroke='#6d7a86' stroke-width='2.4'/>"
                 % (x0 + 1.2, yt + 4, L - 2.4, yb - yt - 8, (yb - yt - 8) / 2.0))
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='%.1f' fill='none' stroke='#6d7a86' stroke-width='2.4'/>"
                 % (x0 + 7, yt + 8.5, L - 18, yb - yt - 17, (yb - yt - 17) / 2.0))
    elif kind == "key":
        r = (yb - yt) / 2.0 - 1
        s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='6' fill='#e3b94a' stroke='%s' stroke-width='1.2'/>" % (x0 + 2 * r - 2, ym - 3, L - 2 * r + 2, INK))
        for t in range(3):
            s.append("<rect x='%.1f' y='%.1f' width='5' height='%d' fill='#e3b94a' stroke='%s' stroke-width='1.1'/>"
                     % (x1 - 6 - t * 9, ym + 3, 6 - 2 * (t % 2), INK))
        s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#e3b94a' stroke='%s' stroke-width='1.2'/>" % (x0 + r, ym, r, INK))
        s.append("<circle cx='%.1f' cy='%.1f' r='3' fill='#fff' stroke='%s' stroke-width='1'/>" % (x0 + r * 0.7, ym, INK))
    else:
        raise ValueError(kind)
    return "".join(s)


# ------------------------------------------------------------ rulers
PADL = 16


def ruler_body(unit, y, flip=False, n=None, pu=None, right=None):
    """Ruler 0..RLEN[unit] with only whole-unit marks. Top edge at y (height 42).
    flip=True puts the marks on the bottom edge and the numbers on top."""
    n = n or RLEN[unit]
    pu = pu or PU[unit]
    X = lambda k: PADL + pu * k
    lab = RULER_LABEL[unit]
    lw = 44 if unit == "in" else 20
    right = right or X(n) + 16 + lw + 8
    s = ["<rect x='%.1f' y='%.1f' width='%.1f' height='42' rx='3' fill='%s' stroke='%s' stroke-width='1.5'/>"
         % (PADL - 10, y, right - (PADL - 10), RULER, INK)]
    for k in range(n + 1):
        if flip:
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (X(k), y + 42, X(k), y + 24, INK))
            ty = y + 18
        else:
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (X(k), y, X(k), y + 18, INK))
            ty = y + 36
        s.append("<text x='%.1f' y='%.1f' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%d</text>" % (X(k), ty, INK, k))
    s.append("<text x='%.1f' y='%.1f' font-size='14' fill='%s'>%s</text>" % (X(n) + 16, ty, INK, lab))
    return "".join(s), right + 6


def guide(x, y0, y1):
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1' stroke-dasharray='3 2'/>"
            % (x, y0, x, y1, GREY))


def ruler_svg(unit, objs):
    """objs: list of (kind, start, end). Each object gets its own band above the ruler."""
    pu = PU[unit]
    X = lambda k: PADL + pu * k
    band, gap = 24, 8
    top = 6
    rtop = top + len(objs) * (band + gap)
    s = []
    for i, (kind, a, b) in enumerate(objs):
        assert 0 <= a < b <= RLEN[unit], (kind, a, b)
        yt = top + i * (band + gap)
        s.append(guide(X(a), yt - 3, rtop))
        s.append(guide(X(b), yt - 3, rtop))
        s.append(draw_object(kind, X(a), X(b), yt, yt + band))
    body, W = ruler_body(unit, rtop)
    desc = " and ".join("%s from %d to %d" % (k, a, b) for k, a, b in objs)
    return svg_wrap(int(W), int(rtop + 48), "".join(s) + body,
                    "%s above a ruler in %s" % (desc, UNITS[unit][1]))


def two_ruler_svg(kind, cm, inch):
    """Centimeter ruler on top (marks pointing down), object in the middle, inch ruler below.
    Drawn so that 15 cm and 6 inches line up (2.5 cm per inch: close enough to the real 2.54)."""
    assert abs(cm - 2.5 * inch) < 1e-9
    pc, pi = 24.0, 60.0
    right = PADL + 6 * pi + 16 + 44 + 8
    top, W = ruler_body("cm", 4, flip=True, n=15, pu=pc, right=right)
    bot, _ = ruler_body("in", 82, n=6, pu=pi, right=right)
    x0, x1 = PADL, PADL + pc * cm
    assert abs(x1 - (PADL + pi * inch)) < 1e-9
    body = top + bot + guide(x0, 46, 82) + guide(x1, 46, 82) + draw_object(kind, x0, x1, 52, 76)
    return svg_wrap(int(W), 128, body, "%s measured with a centimeter ruler and an inch ruler" % kind)


# ============================================================ set 1: measure from 0
S1 = [("in", "eraser", 2), ("cm", "paper clip", 3), ("in", "crayon", 3), ("cm", "eraser", 5),
      ("in", "leaf", 4), ("cm", "caterpillar", 4), ("in", "paper clip", 1), ("cm", "key", 6),
      ("in", "marker", 5), ("cm", "crayon", 9), ("in", "pencil", 6), ("cm", "nail", 7),
      ("in", "key", 3), ("cm", "craft stick", 11), ("in", "ribbon", 7), ("cm", "marker", 13),
      ("in", "straw", 8), ("cm", "pencil", 15)]


def set_from_zero(P):
    its = []
    asks = ["How long is the %s?", "How many %s long is the %s?", "Measure the %s. How long is it?"]
    its.append(mcq("When you measure with a ruler, where do you put one end of the object?", "at the 0 mark",
                   ["at the 1 mark", "at the edge of the ruler", "anywhere"],
                   "Put the end at <b>0</b>. Some rulers have a little space before the 0, so do not use the edge. "
                   "If you start at 1, the number at the end is 1 too big."))
    for i, (unit, obj, L) in enumerate(S1):
        if i % 3 == 1:
            q = asks[1] % (UNITS[unit][1], obj)
        else:
            q = asks[i % 3] % obj
        q = fig(ruler_svg(unit, [(obj, 0, L)])) + q
        other = "cm" if unit == "in" else "in"
        e = ("The %s starts at 0 and ends at %d. Count the spaces: %s. It is <b>%s</b> long."
             % (obj, L, count_list(L), u(L, unit)))
        if L >= 2:
            e += " Do not count the marks: there are %d marks, because the 0 mark is not a space." % (L + 1)
        else:
            e += " There are 2 marks but only 1 space."
        e += " This ruler shows %s." % UNITS[unit][1]
        its.append(mcq_len(q, L, unit, [L + 1, u(L, other), L - 1, L + 2], e))
        if i == 8:
            its.append(mcq("What do you count to find a length on a ruler?", "the spaces between marks",
                           ["the tick marks", "all the numbers on the ruler", "the last number on the ruler"],
                           "Each space from one mark to the next is 1 unit. Count the <b>spaces</b>, not the marks. "
                           "A 3-inch crayon covers 3 spaces but touches 4 marks."))
    assert len(its) == 20, len(its)
    return {"title": "Measure with a ruler", "items": its}


# ============================================================ set 2: not starting at 0
S2 = [("in", "crayon", 2, 6), ("cm", "paper clip", 5, 9), ("in", "key", 3, 6), ("cm", "crayon", 3, 11),
      ("in", "eraser", 1, 3), ("cm", "key", 2, 8), ("in", "caterpillar", 5, 7), ("cm", "caterpillar", 8, 11),
      ("in", "marker", 2, 7), ("cm", "leaf", 4, 14), ("in", "paper clip", 6, 7), ("cm", "eraser", 9, 14)]


def not_zero_e(obj, a, b, unit):
    L = b - a
    e = "The %s starts at %d, not at 0. " % (obj, a)
    if L <= 6:
        e += "Count the spaces from %d to %d: %s. Or subtract: " % (a, b, count_list(L))
    else:
        e += "Subtract: "
    e += "%d − %d = %d. So it is <b>%s</b> long. %d is where it ends, not how long it is." % (b, a, L, u(L, unit), b)
    return e


def set_not_zero(P):
    its = []
    for i, (unit, obj, a, b) in enumerate(S2):
        L = b - a
        q = fig(ruler_svg(unit, [(obj, a, b)])) + ("How long is the %s?" if i % 2 == 0 else
                                                     "The %%s does not start at 0. How many %s long is it?" % UNITS[unit][1]) % obj
        its.append(mcq_len(q, L, unit, [b, L + 1, a, L - 1, a + b], not_zero_e(obj, a, b, unit)))

    for unit, obj, a, b in [("cm", "crayon", 4, 13), ("in", "spoon", 1, 7), ("cm", "ribbon", 3, 15), ("in", "toy car", 2, 5)]:
        L = b - a
        if unit == "cm":
            q = "A %s is on a centimeter ruler. One end is at %d. The other end is at %d. How long is the %s?" % (obj, a, b, obj)
        else:
            q = "A %s starts at the %d-inch mark and ends at the %d-inch mark. How long is the %s?" % (obj, a, b, obj)
        its.append(mcq_len(q, L, unit, [b, L + 1, a + b, L - 1], not_zero_e(obj, a, b, unit)))

    nm, he, his = P.next()
    q = ("The end of %s's ruler broke off, so it starts at 4. %s puts a paper clip at the 4. "
         "The paper clip ends at 7. How many centimeters long is it?" % (nm, cap(he)))
    e = "Count from 4, not from 0: 5, 6, 7 is 3 spaces. 7 − 4 = 3, so the paper clip is <b>3 centimeters</b> long."
    its.append(mcq_len(q, 3, "cm", [7, 4, 11], e))

    nm, he, his = P.next()
    q = ("%s's ruler starts at 3 because the end is broken. %s lines up a marker at 3. "
         "The marker ends at 8. How long is the marker?" % (nm, cap(he)))
    e = "Count the spaces from 3 to 8: 1, 2, 3, 4, 5. 8 − 3 = 5, so the marker is <b>5 inches</b> long."
    its.append(mcq_len(q.replace("ends at 8", "ends at the 8-inch mark"), 5, "in", [8, 6, 11], e))

    nm, he, his = P.next()
    q = ("%s measured a leaf on a centimeter ruler. It starts at 2 and ends at 9. "
         "%s says the leaf is 9 centimeters long. What did %s do wrong?" % (nm, cap(he), he))
    e = ("%s read the number at the end. The leaf starts at 2, so count from 2 to 9: 9 − 2 = 7. "
         "The leaf is 7 centimeters long." % nm)
    its.append(mcq(q, "%s read the end number." % cap(he),
                   ["%s counted the spaces." % cap(he), "%s added 2 and 9." % cap(he), "%s used an inch ruler." % cap(he)], e))

    nm, he, his = P.next()
    q = ("A crayon starts at 3 and ends at 12 on a centimeter ruler. %s counts the marks from 3 to 12 and gets 10. "
         "How long is the crayon?" % nm)
    e = ("Count spaces, not marks. From 3 to 12 there are 10 marks but only 9 spaces. 12 − 3 = 9, "
         "so the crayon is <b>9 centimeters</b> long.")
    its.append(mcq_len(q, 9, "cm", [10, 12, 15], e))
    assert len(its) == 20, len(its)
    return {"title": "When the object does not start at 0", "items": its}


# ============================================================ set 3: tools, units and estimates
def set_estimate(P):
    its = []
    T = [("Which tool is best for measuring the length of a crayon?", "a ruler",
          ["a yardstick", "a meter stick", "a measuring tape"],
          "A crayon is short, so a <b>ruler</b> is best. A yardstick or a meter stick is much longer than you need."),
         ("Which tool is best for measuring around a tree trunk?", "a measuring tape",
          ["a ruler", "a yardstick", "a meter stick"],
          "A <b>measuring tape</b> can bend around the tree. Rulers and sticks are stiff and stay straight."),
         ("Ava wants to measure a rug in meters. Which tool should she use?", "a meter stick",
          ["a yardstick", "a 12-inch ruler", "a scale"],
          "A <b>meter stick</b> is 1 meter long. A yardstick shows yards and feet, and a scale tells how heavy something is."),
         ("Leo wants to measure his bed in yards. Which tool should he use?", "a yardstick",
          ["a meter stick", "a centimeter ruler", "a scale"],
          "A <b>yardstick</b> is 1 yard long. A meter stick shows meters, not yards.")]
    for q, a, w, e in T:
        its.append(mcq(q, a, w, e))

    U = [("Which unit is best for measuring a paper clip?", "centimeters", ["meters", "feet", "yards"],
          "A paper clip is small. Use a small unit: <b>centimeters</b>. Meters, feet and yards are for big things."),
         ("Which unit is best for measuring a pencil?", "inches", ["feet", "yards", "meters"],
          "A pencil is shorter than a 12-inch ruler. Use a small unit: <b>inches</b>."),
         ("Which unit is the longest?", "1 meter", ["1 yard", "1 foot", "1 inch"],
          "A <b>meter</b> is a little longer than a yard. A yard is 3 feet, and a foot is 12 inches."),
         ("Which unit is the shortest?", "1 centimeter", ["1 inch", "1 foot", "1 meter"],
          "A <b>centimeter</b> is about the width of your little finger. An inch is longer than that.")]
    for q, a, w, e in U:
        its.append(mcq(q, a, w, e))

    E = [("About how long is a new pencil?", "7 inches", ["7 feet", "1 inch", "70 inches"],
          "A new pencil is a little shorter than a 12-inch ruler, so it is about <b>7 inches</b>. 7 feet is as tall as a door."),
         ("About how long is a crayon?", "9 centimeters", ["9 meters", "1 centimeter", "90 centimeters"],
          "A crayon fits in your hand. That is about <b>9 centimeters</b>. 9 meters is longer than a classroom wall."),
         ("About how wide is your little finger?", "1 centimeter", ["1 meter", "1 foot", "10 centimeters"],
          "Your little finger is about <b>1 centimeter</b> wide. It is a good way to picture 1 centimeter."),
         ("About how long is a house key?", "5 centimeters", ["5 meters", "50 centimeters", "5 feet"],
          "A key fits in your hand, so it is about <b>5 centimeters</b>. 5 feet is about as tall as a grown-up."),
         ("About how long is a sheet of paper?", "11 inches", ["11 feet", "11 yards", "1 inch"],
          "A sheet of school paper is about <b>11 inches</b> long. That is a little shorter than a 12-inch ruler."),
         ("About how tall is a door?", "7 feet", ["7 inches", "7 yards", "70 feet"],
          "A door is taller than a grown-up, who is about 5 or 6 feet. A door is about <b>7 feet</b> tall."),
         ("About how tall is a door in meters?", "2 meters", ["2 centimeters", "20 meters", "20 centimeters"],
          "A meter stick is about as high as a doorknob. A door is about 2 meter sticks tall: <b>2 meters</b>."),
         ("About how wide is a classroom door?", "1 meter", ["1 centimeter", "10 meters", "1 inch"],
          "A meter stick fits across a door, so a door is about <b>1 meter</b> wide."),
         ("About how tall is a second grader?", "4 feet", ["4 inches", "4 yards", "40 feet"],
          "Stack four 12-inch rulers. That is about as tall as a second grader: about <b>4 feet</b>."),
         ("About how high is a basketball hoop?", "10 feet", ["10 inches", "10 yards", "100 feet"],
          "A basketball hoop is <b>10 feet</b> high, higher than a grown-up can reach. 10 inches is shorter than a sheet of paper."),
         ("About how long is a classroom?", "30 feet", ["30 inches", "3 feet", "300 feet"],
          "A classroom is about <b>30 feet</b> long, about 10 yardsticks. 3 feet is only 1 yardstick, and 30 inches is shorter than 1 yardstick."),
         ("About how long is a school bus?", "12 meters", ["12 centimeters", "1 meter", "120 meters"],
          "A school bus is as long as about 12 meter sticks in a row: <b>12 meters</b>. 1 meter is only about the width of a door.")]
    for q, a, w, e in E:
        its.append(mcq(q, a, w, e))
    assert len(its) == 20, len(its)
    return {"title": "Choose the tool and estimate", "items": its}


# ============================================================ set 4: two units for the same object
def set_two_units(P):
    its = []
    its.append(mcq("Which is longer, 1 inch or 1 centimeter?", "1 inch",
                   ["1 centimeter", "They are the same.", "You cannot tell."],
                   "<b>1 inch</b> is longer. About 2 and a half centimeters fit in 1 inch."))
    its.append(mcq("Which is longer, 1 foot or 1 meter?", "1 meter",
                   ["1 foot", "They are the same.", "You cannot tell."],
                   "<b>1 meter</b> is longer. A meter stick is longer than a yardstick, and a yardstick is 3 feet."))
    for kind, cm, inch, ask in [("key", 5, 2, "cm"), ("crayon", 10, 4, "in"), ("paper strip", 15, 6, "cm"), ("eraser", 5, 2, "in")]:
        q = fig(two_ruler_svg(kind, cm, inch))
        if ask == "cm":
            q += "Look at the top ruler. How many centimeters long is the %s?" % kind
            e = ("Read the centimeter ruler on top. The %s ends at %d, so it is <b>%d centimeters</b>. "
                 "On the inch ruler it is only %d, because an inch is longer." % (kind, cm, cm, inch))
            its.append(mcq_len(q, cm, "cm", [inch, cm + 1, u(cm, "in"), cm - 1], e))
        else:
            q += "Look at the bottom ruler. How many inches long is the %s?" % kind
            e = ("Read the inch ruler on the bottom. The %s ends at %d, so it is <b>%s</b>. "
                 "%d is the number of centimeters." % (kind, inch, u(inch, "in"), cm))
            its.append(mcq_len(q, inch, "in", [cm, inch + 1, u(inch, "cm"), inch - 1], e))
    q = fig(two_ruler_svg("craft stick", 10, 4)) + "Which is true about the craft stick?"
    e = ("The craft stick is 10 on the centimeter ruler and 4 on the inch ruler: <b>4 inches and 10 centimeters</b>. "
         "Same stick, two units.")
    its.append(mcq(q, "4 in and 10 cm", ["10 in and 4 cm", "4 in and 4 cm", "10 in and 10 cm"], e))

    nm, he, his = P.next()
    its.append(mcq("%s measured a book. It is 9 inches long. Now %s measures it in centimeters. What will %s find?" % (nm, he, he),
                   "more than 9 centimeters", ["less than 9 centimeters", "exactly 9 centimeters", "9 inches again"],
                   "A centimeter is shorter than an inch. It takes <b>more</b> short units to cover the same book, so the number is more than 9."))
    nm, he, his = P.next()
    m = P.next()
    its.append(mcq("%s and %s measured the same desk. %s got 24. %s got 60. Who used centimeters?" % (nm, m[0], nm, m[0]),
                   m[0], [nm, "both of them", "neither of them"],
                   "Centimeters are short, so you need more of them. The bigger number, 60, is in centimeters. "
                   "<b>%s</b> used centimeters, and %s used inches." % (m[0], nm)))
    its.append(mcq("Why is a pencil 18 centimeters long but only 7 inches long?", "A centimeter is shorter.",
                   ["A centimeter is longer.", "The pencil grew.", "Someone made a mistake."],
                   "<b>A centimeter is shorter than an inch.</b> The shorter the unit, the more of them you need. "
                   "So the centimeter number, 18, is bigger."))
    nm, he, his = P.next()
    its.append(mcq("A rope is 4 meters long. %s measures it again in centimeters. Will %s number be bigger or smaller than 4?" % (nm, his),
                   "bigger", ["smaller", "the same", "You cannot tell."],
                   "A centimeter is much shorter than a meter. %s needs many centimeters to cover the rope, so the number is <b>bigger</b>: 400." % nm))
    nm, he, his = P.next()
    its.append(mcq("%s measured the hall in feet and got 30. Then %s used a yardstick. What will %s new number be?" % (nm, he, his),
                   "less than 30", ["more than 30", "exactly 30", "30 feet again"],
                   "A yard is longer than a foot (1 yard = 3 feet). Longer units mean fewer of them, so the number is <b>less than 30</b>. It is 10 yards."))
    nm, he, his = P.next()
    m = P.next()
    its.append(mcq("%s's rope is 5 feet long. %s's rope is 5 yards long. Which rope is longer?" % (nm, m[0]),
                   "%s's rope" % m[0], ["%s's rope" % nm, "They are the same.", "You cannot tell."],
                   "The numbers are the same, but the units are not. A yard is longer than a foot, so 5 yards is longer. "
                   "<b>%s's rope</b> is longer." % m[0]))
    its.append(mcq("Which length is the longest?", "10 meters", ["10 feet", "10 inches", "10 centimeters"],
                   "All the numbers are 10, so look at the units. A meter is the longest unit here, so <b>10 meters</b> is the longest."))
    its.append(mcq("Which length is the shortest?", "8 centimeters", ["8 inches", "8 feet", "8 yards"],
                   "All the numbers are 8. A centimeter is the shortest unit, so <b>8 centimeters</b> is the shortest."))
    nm, he, his = P.next()
    its.append(mcq("%s measured a rug. It is 6 feet long. Then %s measured it in yards. Which number could %s get?" % (nm, he, he),
                   "2 yards", ["6 yards", "12 yards", "18 yards"],
                   "A yard is longer than a foot, so the number of yards is smaller than 6. 3 feet make 1 yard, so 6 feet is <b>2 yards</b>."))
    its.append(mcq("A table is 2 meters long. How many centimeters long is it?", "200 centimeters",
                   ["2 centimeters", "20 centimeters", "102 centimeters"],
                   "A meter stick has 100 centimeters. 2 meters is 100 + 100 = <b>200 centimeters</b>. "
                   "The centimeter number is bigger because a centimeter is shorter."))
    nm, he, his = P.next()
    its.append(mcq("%s's ruler is 30 centimeters long. The other side shows inches. About how many inches long is it?" % nm,
                   "12 inches", ["30 inches", "60 inches", "90 inches"],
                   "An inch is longer than a centimeter, so the inch number must be smaller than 30. "
                   "This is a 1-foot ruler: <b>12 inches</b> on one side and about 30 centimeters on the other."))
    its.append(mcq("Which list goes from the shortest unit to the longest?",
                   "centimeter, inch, foot, yard",
                   ["inch, centimeter, foot, yard", "centimeter, inch, yard, foot", "yard, foot, inch, centimeter"],
                   "A <b>centimeter</b> is the width of a finger. An <b>inch</b> is a bit longer. "
                   "A <b>foot</b> is 12 inches, and a <b>yard</b> is 3 feet."))
    nm, he, his = P.next()
    its.append(mcq("%s measured %s desk with a 12-inch ruler and got 2 rulers. Then %s used inches. "
                   "Which is true?" % (nm, his, he),
                   "The inch number is bigger.", ["The inch number is smaller.", "Both numbers are 2.", "The desk got longer."],
                   "Each 12-inch ruler is 1 foot. An inch is shorter than a foot, so there are more of them. "
                   "The desk is 2 feet, or 24 inches, so <b>the inch number is bigger</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Inches or centimeters: one object, two units", "items": its}


# ============================================================ set 5: how much longer
S5 = [("in", "pencil", 7, "crayon", 3, "longer"), ("cm", "pencil", 14, "crayon", 9, "longer"),
      ("in", "straw", 8, "eraser", 2, "longer"), ("cm", "craft stick", 11, "caterpillar", 4, "longer"),
      ("in", "ribbon", 6, "key", 3, "shorter"), ("cm", "leaf", 12, "paper clip", 3, "longer"),
      ("in", "marker", 5, "paper clip", 1, "longer"), ("cm", "ribbon", 15, "nail", 7, "shorter")]


def digit_slip(a, b):
    """Common mistake: subtract the smaller digit from the bigger one in each place (85 − 47 → 42)."""
    if a < 10 or b < 10:
        return None
    t = abs(a // 10 - b // 10)
    o = abs(a % 10 - b % 10)
    r = t * 10 + o
    return r if r != a - b else None


def set_longer(P):
    its = []
    for unit, A, a, B, b, ask in S5:
        d = a - b
        q = fig(ruler_svg(unit, [(A, 0, a), (B, 0, b)]))
        if ask == "longer":
            q += "How much longer is the %s than the %s?" % (A, B)
        else:
            q += "How much shorter is the %s than the %s?" % (B, A)
        e = ("Both start at 0. The %s ends at %d and the %s ends at %d. Count the spaces from %d to %d, or subtract: "
             "%d − %d = %d. The %s is <b>%s</b> %s." % (A, a, B, b, b, a, a, b, d,
                                                      A if ask == "longer" else B, u(d, unit),
                                                      "longer" if ask == "longer" else "shorter"))
        its.append(mcq_len(q, d, unit, [a, a + b, d + 1, d - 1], e))

    W = [("{N}'s ribbon is 14 inches long. {M}'s ribbon is 9 inches long. How much longer is {N}'s ribbon?", 14, 9, "in", "longer"),
         ("{N} jumped 5 feet. {M} jumped 4 feet. How much farther did {N} jump?", 5, 4, "ft", "farther"),
         ("A pencil is 18 centimeters long. A crayon is 9 centimeters long. How much longer is the pencil?", 18, 9, "cm", "longer"),
         ("{N} found two worms. One is 12 centimeters long. The other is 7 centimeters long. How much longer is the long worm?", 12, 7, "cm", "longer"),
         ("A bed is 6 feet long. {N} is 4 feet tall. How much longer is the bed than {N}?", 6, 4, "ft", "longer"),
         ("A table is 36 inches wide. A desk is 24 inches wide. How much wider is the table?", 36, 24, "in", "wider"),
         ("A green snake is 32 inches long. A brown snake is 50 inches long. How much shorter is the green snake?", 50, 32, "in", "shorter"),
         ("A school bus is 40 feet long. A car is 15 feet long. How much longer is the bus?", 40, 15, "ft", "longer"),
         ("A pool is 25 meters long. {N} swims 18 meters and stops. How many more meters must {he} swim to reach the end?", 25, 18, "m", "more"),
         ("{N}'s block tower is 54 centimeters tall. {M}'s tower is 29 centimeters tall. How much taller is {N}'s tower?", 54, 29, "cm", "taller"),
         ("The hallway is 65 feet long. The classroom is 38 feet long. How much longer is the hallway?", 65, 38, "ft", "longer"),
         ("A sunflower is 85 centimeters tall. A tomato plant is 47 centimeters tall. How much taller is the sunflower?", 85, 47, "cm", "taller")]
    for tpl, a, b, unit, word in W:
        nm, he, his = P.next()
        m = P.next()[0] if "{M}" in tpl else ""
        q = tpl.format(N=nm, M=m, he=he)
        d = a - b
        e = "Subtract the shorter length from the longer one: %d − %d = <b>%d</b>. " % (a, b, d)
        if a >= 20 and b >= 10:
            e += "Check by adding: %d + %d = %d. " % (b, d, a)
        elif 2 <= d <= 6:
            e += "Or count up from %d to %d: %s. " % (b, a, count_list(d))
        e += "Do not add the lengths: %d + %d = %d is the total, not the difference." % (a, b, a + b)
        e = e.replace("  ", " ")
        cands = [digit_slip(a, b), a + b, a, d + 1, d - 1]
        its.append(mcq_len(q, d, unit, [c for c in cands if c is not None], e))
    assert len(its) == 20, len(its)
    return {"title": "How much longer?", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Line up at 0 and count the spaces</h2>"
        "<p>Put one end of the object at the <b>0</b> mark. Look at where the other end stops. "
        "Each space between two marks is <b>1 unit</b>. Count the spaces, not the marks.</p>"
        "<figure class='sn-fig'>" + ruler_svg("in", [("pencil", 0, 6)]) +
        "<figcaption>The pencil starts at 0 and ends at 6. It covers 6 spaces, so it is 6 inches long.</figcaption></figure>"
        "<h2>When the object does not start at 0</h2>"
        "<p>Count the spaces from where the object starts to where it ends. Or subtract: end − start.</p>"
        "<figure class='sn-fig'>" + ruler_svg("cm", [("leaf", 3, 10)]) +
        "<figcaption>The leaf starts at 3 and ends at 10. 10 − 3 = 7, so the leaf is 7 centimeters long, not 10.</figcaption></figure>"
        + ex("Example", "A crayon starts at 2 and ends at 6 on an inch ruler. How long is it?",
             "Count from 2: 3, 4, 5, 6 is 4 spaces. 6 − 2 = 4.", "4 inches")
        + "<h2>Units of length</h2>"
        "<p>Pick a tool and a unit that fit the object. Use a ruler for small things, a yardstick or meter stick for bigger things, "
        "and a measuring tape for very long or curved things. To estimate, picture a benchmark.</p>"
        + table(["Unit", "About as long as", "Good for"], [
            ["1 inch", "the width of a quarter coin", "pencils, crayons, books"],
            ["1 foot = 12 inches", "a 12-inch ruler", "desks, beds, rooms"],
            ["1 yard = 3 feet", "a yardstick", "rugs, hallways, fields"],
            ["1 centimeter", "the width of your little finger", "paper clips, keys, crayons"],
            ["1 meter = 100 centimeters", "a meter stick, about the width of a door", "rooms, pools, buses"],
        ]) +
        table(["Object", "About how long"], [
            ["new pencil", "7 inches or 18 centimeters"],
            ["door (tall)", "7 feet or 2 meters"],
            ["classroom", "30 feet or 9 meters"],
        ]) +
        "<h2>Same object, two units</h2>"
        "<p>A centimeter is shorter than an inch. So the same object is <b>more</b> centimeters than inches. "
        "The shorter the unit, the bigger the number.</p>"
        "<figure class='sn-fig'>" + two_ruler_svg("crayon", 10, 4) +
        "<figcaption>The same crayon is 10 centimeters (top ruler) and 4 inches (bottom ruler).</figcaption></figure>"
        "<h2>How much longer?</h2>"
        "<p>Measure both objects in the same unit. Then subtract the shorter length from the longer length.</p>"
        "<figure class='sn-fig'>" + ruler_svg("cm", [("marker", 0, 13), ("crayon", 0, 8)]) +
        "<figcaption>The marker is 13 centimeters. The crayon is 8 centimeters. 13 − 8 = 5, so the marker is 5 centimeters longer.</figcaption></figure>"
        + ex("Example", "A ribbon is 45 inches long. A rope is 28 inches long. How much longer is the ribbon?",
             "Subtract: 45 − 28 = 17. Check: 28 + 17 = 45.", "17 inches")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Reading the end number when the object starts at 3", "Subtract the start: 10 − 3 = 7"],
            ["Counting the marks (7 marks for 6 inches)", "Count the spaces between marks"],
            ["Starting at the edge of the ruler or at 1", "Line up the end of the object with 0"],
            ["Thinking more centimeters means a longer object than inches", "A centimeter is shorter, so you need more of them"],
            ["Using a small unit for a big thing (a door is 7 inches)", "Picture a benchmark: a door is about 7 feet"],
            ["Adding to find how much longer", "Subtract the shorter length from the longer one"],
        ])
    )


FAQ = [
    {"q": "What do 2nd graders learn about measuring length?",
     "a": "In Grade 2, children measure length with rulers, yardsticks, meter sticks and measuring tapes in inches, feet, centimeters and meters. "
          "They also estimate lengths and find how much longer one object is than another (Common Core 2.MD.A.1–4)."},
    {"q": "Why is the number of centimeters bigger than the number of inches?",
     "a": "A centimeter is shorter than an inch, so it takes more centimeters to cover the same object. A 4-inch crayon is about 10 centimeters long."},
    {"q": "How do you measure when the object does not start at 0?",
     "a": "Count the spaces from where the object starts to where it ends, or subtract the start from the end. An object from 2 to 7 is 7 − 2 = 5 units long."},
    {"q": "What are good benchmarks for inches, feet, centimeters and meters?",
     "a": "1 centimeter is about the width of a little finger, and 1 inch is about the width of a quarter coin. "
          "1 foot is a 12-inch ruler, and 1 meter is about the width of a door."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (rulers) so their numbers stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(212)
    P = People(rnd)
    sets = [set_from_zero(P), set_not_zero(P), set_estimate(P), set_two_units(P), set_longer(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"]
            assert k not in seen, it["q"]
            seen.add(k)
            for c in it["c"]:      # singular/plural units
                assert not re.search(r"\b1 (inches|feet|centimeters|meters|yards)\b", c), c
                assert not re.search(r"\b([02-9]|\d\d+) (inch|foot|centimeter|meter|yard)\b", c), c
    # every one-object ruler question: the answer is end − start
    n = 0
    for s in sets:
        for it in s["items"]:
            m = re.search(r"aria-label='([a-z ]+) from (\d+) to (\d+) above a ruler in (inches|centimeters)", it["q"])
            if m and " and " not in m.group(1):
                a, b = int(m.group(2)), int(m.group(3))
                unit = "in" if m.group(4) == "inches" else "cm"
                assert it["c"][it["a"]] == u(b - a, unit), it["q"][-80:]
                n += 1
    assert n == 30, n
    u_ = {
        "country": "us", "subject": "math", "grade": "grade-2", "slug": "measuring-length", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Measuring Length: Inches, Feet, Centimeters and Meters",
        "seo_title": "Grade 2 Measuring Length Worksheets: Use a Ruler, Inches and Centimeters, Estimate, How Much Longer",
        "short_title": "Measuring length",
        "domain": "Measurement and Data",
        "standard_code": "2.MD.A.1–4",
        "standard_url": "https://www.thecorestandards.org/Math/Content/2/MD/A/",
        "standard_text": "Measure the length of an object by selecting and using appropriate tools such as rulers, yardsticks, meter sticks, "
                         "and measuring tapes. Measure the length of an object twice, using length units of different lengths for the two "
                         "measurements; describe how the two measurements relate to the size of the unit chosen. Estimate lengths using units "
                         "of inches, feet, centimeters, and meters. Measure to determine how much longer one object is than another, "
                         "expressing the length difference in terms of a standard length unit.",
        "meta_desc": "Free Grade 2 measuring length worksheets with ruler pictures: measure in inches and centimeters, objects that do not "
                     "start at 0, choose the right tool and unit, estimate with benchmarks, and find how much longer. 100 practice questions with answers.",
        "key_big": "Line up at 0 and count the spaces, not the marks.",
        "key_sub": "If the object starts at 3 and ends at 10, it is 10 − 3 = 7 units long. A centimeter is shorter than an inch, "
                   "so the same object is more centimeters than inches. To find how much longer, subtract.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u_, "[^']*ruler")


if __name__ == "__main__":
    out = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, out["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
