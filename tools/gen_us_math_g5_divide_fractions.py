# -*- coding: utf-8 -*-
"""
US Grade 5 Math: Divide Unit Fractions and Whole Numbers (5.NF.B.7)
  python tools/gen_us_math_g5_divide_fractions.py
Only two kinds of division (Grade 5):
  whole number ÷ unit fraction   3 ÷ 1/4 = 12   (how many fourths are in 3?)
  unit fraction ÷ whole number   1/2 ÷ 3 = 1/6  (cut 1/2 into 3 equal parts)
No fraction ÷ fraction rule ("keep-change-flip" is Grade 6). Every answer is checked with multiplication.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-5")
UPDATED = "2026-11-02"
FILL = "#4fae74"      # shaded part
LIGHT = "#dff1e5"     # light tint
DARK = "#1f6e45"      # one small piece
LINE = "#2b2b2b"
GRAY = "#8a8178"
RED = "#d6453b"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
PARTS = {2: ("half", "halves"), 3: ("third", "thirds"), 4: ("fourth", "fourths"), 5: ("fifth", "fifths"),
         6: ("sixth", "sixths"), 7: ("seventh", "sevenths"), 8: ("eighth", "eighths"), 9: ("ninth", "ninths"),
         10: ("tenth", "tenths"), 12: ("twelfth", "twelfths")}


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def num(v):
    """A Fraction as a whole number or a fraction span (simplest form)."""
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else fr(v.numerator, v.denominator)


def wu(n, b):
    """whole number ÷ unit fraction"""
    return "%d ÷ %s" % (n, fr(1, b))


def uw(b, n):
    """unit fraction ÷ whole number"""
    return "%s ÷ %d" % (fr(1, b), n)


def parts(b, k=2):
    return PARTS[b][0] if k == 1 else PARTS[b][1]


def pl(k, one, many):
    return one if k == 1 else many


def mcq(q, correct, cands, e):
    """correct / cands: html strings or (html, value) pairs; a candidate equal in value to the answer is skipped.
    Positions are set later by balance()."""
    cv = None
    if isinstance(correct, tuple):
        correct, cv = correct
    seen = {correct}
    pick = []
    for c in cands:
        v = None
        if isinstance(c, tuple):
            c, v = c
        if not c or c in seen or (cv is not None and v is not None and v == cv):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


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
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


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


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger (many small pieces or ticks) so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ figures
def tape_svg(n, b, PW=None):
    """n wholes in a row, each cut into b equal pieces. Thick lines between wholes, labels 0..n below."""
    k = n * b
    if PW is None:
        PW = max(16, min(30, 300 // k))
    L, T, BH = 12, 6, 36
    W = L * 2 + k * PW
    s = []
    for i in range(k):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
                 % (L + i * PW, T, PW, BH, LIGHT if (i // b) % 2 == 0 else "#c4e6cf", LINE))
    for j in range(n + 1):
        x = L + j * b * PW
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3.5'/>" % (x, T - 2, x, T + BH + 8, LINE))
        s.append("<text x='%d' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                 % (x, T + BH + 26, LINE, j))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (L, T, k * PW, BH, LINE))
    return svg_wrap(W, T + BH + 32, "".join(s),
                    "%d %s, each cut into %d equal pieces: %d pieces" % (n, pl(n, "whole", "wholes"), b, k))


def jumps_svg(n, b, W=440):
    """Number line 0..n with ticks every 1/b and n*b jumps of 1/b."""
    total = n * b
    L, R, Y = 18, W - 18, 46
    def X(i):
        return L + (R - L) * i / float(total)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for i in range(total + 1):
        whole = (i % b == 0)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(i), Y - (12 if whole else 7), X(i), Y + (12 if whole else 7), LINE, "2.5" if whole else "1.6"))
        if whole:
            s.append("<text x='%.1f' y='%d' font-size='18' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                     % (X(i), Y + 34, LINE, i // b))
    h = 26 if (R - L) / float(total) > 24 else 18
    for j in range(total):
        x0, x1 = X(j), X(j + 1)
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.2'/>"
                 % (x0 + 1, Y - 3, (x0 + x1) / 2, Y - 3 - h, x1 - 1, Y - 3, RED))
        s.append("<path d='M%.1f %d l-6 -8 l8 1 z' fill='%s'/>" % (x1 - 1, Y - 3, RED))
    return svg_wrap(W, Y + 42, "".join(s),
                    "number line from 0 to %d with jumps of 1/%d" % (n, b))


def area_svg(b, n, W=168, H=112):
    """A rectangle (1 whole) cut into b columns; the first column is shaded and cut into n rows; one piece is dark.
    Dashed lines carry the rows across the whole so all b*n pieces can be counted."""
    L, T = 4, 4
    cw = W / float(b)
    rh = H / float(n)
    s = ["<rect x='%d' y='%d' width='%.1f' height='%d' fill='%s'/>" % (L, T, cw, H, FILL),
         "<rect x='%d' y='%d' width='%.1f' height='%.1f' fill='%s'/>" % (L, T, cw, rh, DARK)]
    for r in range(1, n):
        y = T + r * rh
        s.append("<line x1='%.1f' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='1.5' stroke-dasharray='5 4'/>"
                 % (L + cw, y, L + W, y, GRAY))
        s.append("<line x1='%d' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (L, y, L + cw, y, LINE))
    for c in range(1, b):
        x = L + c * cw
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x, T, x, T + H, LINE))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (L, T, W, H, LINE))
    return svg_wrap(W + 8, H + 8, "".join(s),
                    "rectangle cut into %d columns; one column is shaded and cut into %d equal pieces" % (b, n))


def split_line_svg(b, n, W=420):
    """Number line 0..1, ticks every 1/(b*n); 1/b marked with a bracket; the first small part in red."""
    total = b * n
    L, R, Y = 18, W - 18, 74
    def X(i):
        return L + (R - L) * i / float(total)
    s = []
    # bracket over 0 .. 1/b with a stacked fraction label
    x0, x1 = X(0), X(n)
    s.append("<path d='M%.1f %d V%d H%.1f V%d' fill='none' stroke='%s' stroke-width='2'/>" % (x0, Y - 16, Y - 24, x1, Y - 16, LINE))
    cx = (x0 + x1) / 2
    s.append("<text x='%.1f' y='%d' font-size='18' font-weight='700' fill='%s' text-anchor='middle'>1</text>" % (cx, Y - 52, LINE))
    s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (cx - 11, Y - 47, cx + 11, Y - 47, LINE))
    s.append("<text x='%.1f' y='%d' font-size='18' font-weight='700' fill='%s' text-anchor='middle'>%d</text>" % (cx, Y - 29, LINE, b))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE))
    s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='6' stroke-linecap='butt'/>" % (X(0), Y, X(1), Y, RED))
    for i in range(total + 1):
        if i % total == 0:
            hh, sw = 13, "2.5"
        elif i % n == 0:
            hh, sw = 10, "2.2"
        else:
            hh, sw = 6, "1.4"
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>" % (X(i), Y - hh, X(i), Y + hh, LINE, sw))
    for i, t in ((0, "0"), (total, "1")):
        s.append("<text x='%.1f' y='%d' font-size='18' font-weight='700' fill='%s' text-anchor='middle'>%s</text>" % (X(i), Y + 34, LINE, t))
    return svg_wrap(W, Y + 42, "".join(s), "number line from 0 to 1 with 1/%d split into %d equal parts" % (b, n))


# ------------------------------------------------------------ explanations
def check_wu(n, b):
    return "Check: %d × %s = %s = %d." % (n * b, fr(1, b), fr(n * b, b), n)


def check_uw(b, n):
    return "Check: %s × %d = %s = %s." % (fr(1, b * n), n, fr(n, b * n), fr(1, b))


def e_wu(n, b):
    if n == 1:
        s = "There are %d %s in 1 whole, so %s = <b>%d</b>. " % (b, parts(b), wu(n, b), b)
    else:
        s = ("Each whole has %d %s. %d wholes have %d × %d = %d %s, so %s = <b>%d</b>. "
             % (b, parts(b), n, n, b, n * b, parts(b), wu(n, b), n * b))
    return s + check_wu(n, b)


def e_uw(b, n):
    return ("Cut %s into %d equal parts. Then 1 whole has %d × %d = %d of these parts, so each part is %s. "
            "%s = <b>%s</b>. %s" % (fr(1, b), n, b, n, b * n, fr(1, b * n), uw(b, n), fr(1, b * n), check_uw(b, n)))


# ------------------------------------------------------------ typical wrong answers
def wu_wrongs(n, b):
    """n ÷ 1/b: (html, value) pairs from real mistakes, most common first."""
    return [
        (num(F(n, b)), F(n, b)),                # divided by b (or multiplied by 1/b): answer got smaller
        (str(n + b), F(n + b)),                 # added
        (fr(1, n * b), F(1, n * b)),            # mixed up the two kinds
        (str(b), F(b)),                         # counted the pieces in one whole only
        (str(n * b + 1), F(n * b + 1)),         # counted tick marks, not spaces
        (str(n * b - 1), F(n * b - 1)),
    ]


def uw_wrongs(b, n):
    """1/b ÷ n: (html, value) pairs from real mistakes, most common first."""
    return [
        (fr(1, n), F(1, n)),                    # a part of the shaded piece, not of the whole
        (str(n * b), F(n * b)),                 # mixed up the two kinds
        (fr(n, b), F(n, b)),                    # multiplied instead of dividing
        (fr(1, n + b), F(1, n + b)),            # added the bottom number and the whole number
        (fr(b, n), F(b, n)),                    # flipped
    ]


# ============================================================ set 1: whole number ÷ unit fraction with models
def set_wu_models():
    its = []
    for n, b in [(2, 3), (3, 4), (4, 2), (2, 5), (3, 3), (5, 2), (2, 6)]:
        q = (fig(tape_svg(n, b)) + "Each whole is cut into %s. How many %s are in %d?<br>%s = <b>?</b>"
             % (parts(b), parts(b), n, wu(n, b)))
        its.append(mcq(q, (str(n * b), F(n * b)), wu_wrongs(n, b), e_wu(n, b)))
    for n, b in [(1, 5), (2, 4), (3, 2), (4, 3), (1, 8), (3, 5)]:
        q = (fig(jumps_svg(n, b)) + "Each jump is %s. How many jumps does it take to get from 0 to %d?<br>%s = <b>?</b>"
             % (fr(1, b), n, wu(n, b)))
        e = ("Count the jumps, not the tick marks. Each whole has %d jumps of %s" % (b, fr(1, b)))
        e += (", so there are %d jumps. " % b) if n == 1 else (", so %d wholes have %d × %d = %d jumps. " % (n, n, b, n * b))
        e += "%s = <b>%d</b>. %s" % (wu(n, b), n * b, check_wu(n, b))
        its.append(mcq(q, (str(n * b), F(n * b)), wu_wrongs(n, b), e))
    for n, b in [(1, 6), (4, 5), (5, 3), (6, 2), (2, 8), (3, 10), (7, 4)]:
        q = "How many %s are in %d?<br>%s = <b>?</b>" % (parts(b), n, wu(n, b))
        its.append(mcq(q, (str(n * b), F(n * b)), wu_wrongs(n, b), e_wu(n, b)))
    assert len(its) == 20, len(its)
    return {"title": "How many unit fractions are in a whole number?", "items": its}


# ============================================================ set 2: unit fraction ÷ whole number with models
def set_uw_models():
    its = []
    for b, n in [(2, 3), (3, 2), (4, 2), (2, 4), (3, 3), (5, 2), (2, 5), (4, 3)]:
        q = (fig(area_svg(b, n)) + "The green column is %s of the whole rectangle. It is cut into %d equal pieces. "
             "What fraction of the <b>whole</b> rectangle is the dark piece?<br>%s = <b>?</b>" % (fr(1, b), n, uw(b, n)))
        e = ("Follow the dashed lines: the whole rectangle has %d × %d = %d equal pieces, and the dark piece is 1 of them. "
             "%s = <b>%s</b>. %s" % (b, n, b * n, uw(b, n), fr(1, b * n), check_uw(b, n)))
        its.append(mcq(q, (fr(1, b * n), F(1, b * n)), uw_wrongs(b, n), e))
    for b, n in [(3, 4), (6, 2), (2, 6), (5, 3), (8, 2), (7, 2)]:
        q = (fig(split_line_svg(b, n)) + "The bracket shows %s. It is split into %d equal parts. "
             "What fraction of 1 whole is the red part?<br>%s = <b>?</b>" % (fr(1, b), n, uw(b, n)))
        e = ("Count the small spaces from 0 to 1: there are %d × %d = %d, so the red part is %s. "
             "%s = <b>%s</b>. %s" % (b, n, b * n, fr(1, b * n), uw(b, n), fr(1, b * n), check_uw(b, n)))
        its.append(mcq(q, (fr(1, b * n), F(1, b * n)), uw_wrongs(b, n), e))
    for b, n in [(3, 5), (6, 3), (10, 2), (4, 6), (5, 4), (12, 2)]:
        q = "Cut %s into %d equal parts. What fraction of 1 whole is each part?<br>%s = <b>?</b>" % (fr(1, b), n, uw(b, n))
        its.append(mcq(q, (fr(1, b * n), F(1, b * n)), uw_wrongs(b, n), e_uw(b, n)))
    assert len(its) == 20, len(its)
    return {"title": "Share a unit fraction into equal parts", "items": its}


# ============================================================ set 3: compute, check, match a model
def set_compute():
    its = []
    for n, b in [(5, 6), (6, 4), (7, 3), (10, 2)]:
        its.append(mcq("%s = <b>?</b>" % wu(n, b), (str(n * b), F(n * b)), wu_wrongs(n, b), e_wu(n, b)))
    for b, n in [(7, 2), (4, 5), (9, 2), (6, 4)]:
        its.append(mcq("%s = <b>?</b>" % uw(b, n), (fr(1, b * n), F(1, b * n)), uw_wrongs(b, n), e_uw(b, n)))

    # which multiplication checks the answer
    for n, b in [(4, 3), (2, 8)]:
        q = "To check %s = %d, which multiplication should you do?" % (wu(n, b), n * b)
        right = "%d × %s" % (n * b, fr(1, b))
        wrong = ["%d × %s" % (n, fr(1, b)), "%d × %d" % (n * b, n), "%d × %d" % (n * b, b)]
        e = ("Multiply the answer by the number you divided by. It should give the number you started with: "
             "%d × %s = %s = %d. It matches, so %d is right." % (n * b, fr(1, b), fr(n * b, b), n, n * b))
        its.append(mcq(q, right, wrong, e))
    for b, n in [(3, 4), (5, 2)]:
        q = "To check %s = %s, which multiplication should you do?" % (uw(b, n), fr(1, b * n))
        right = "%s × %d" % (fr(1, b * n), n)
        wrong = ["%s × %d" % (fr(1, b), n), "%s × %s" % (fr(1, b * n), fr(1, b)), "%s × %d" % (fr(1, b * n), b)]
        e = ("Multiply the answer by the number you divided by. It should give the number you started with: "
             "%s × %d = %s = %s. It matches, so %s is right." % (fr(1, b * n), n, fr(n, b * n), fr(1, b), fr(1, b * n)))
        its.append(mcq(q, right, wrong, e))

    # missing numbers
    its.append(mcq("<b>?</b> ÷ %s = 20" % fr(1, 4), ("5", F(5)),
                   [("80", F(80)), ("24", F(24)), ("16", F(16)), (fr(1, 80), F(1, 80))],
                   "There are 20 fourths in the missing number. Each whole has 4 fourths, so 20 ÷ 4 = <b>5</b> wholes. "
                   "Check: 20 × %s = %s = 5." % (fr(1, 4), fr(20, 4))))
    its.append(mcq("%s ÷ <b>?</b> = %s" % (fr(1, 6), fr(1, 18)), ("3", F(3)),
                   [("12", F(12)), (fr(1, 3), F(1, 3)), ("24", F(24)), ("18", F(18))],
                   "%s is cut into equal parts that are each %s. %s × 3 = %s = %s, so the missing number is <b>3</b>."
                   % (fr(1, 6), fr(1, 18), fr(1, 18), fr(3, 18), fr(1, 6))))
    its.append(mcq("6 ÷ <b>?</b> = 18", (fr(1, 3), F(1, 3)),
                   [("3", F(3)), ("12", F(12)), (fr(1, 18), F(1, 18)), (fr(1, 12), F(1, 12))],
                   "The answer 18 is bigger than 6, so you divide by a unit fraction. 6 wholes hold 18 pieces, "
                   "so there are 18 ÷ 6 = 3 pieces in each whole: the pieces are %s. Check: 18 × %s = %s = 6."
                   % (fr(1, 3), fr(1, 3), fr(18, 3))))
    its.append(mcq("<b>?</b> ÷ 3 = %s" % fr(1, 15), (fr(1, 5), F(1, 5)),
                   [("5", F(5)), (fr(1, 45), F(1, 45)), (fr(1, 12), F(1, 12)), (fr(1, 18), F(1, 18))],
                   "Multiply to undo the division: %s × 3 = %s = %s. So %s = %s, and the missing number is <b>%s</b>."
                   % (fr(1, 15), fr(3, 15), fr(1, 5), uw(5, 3), fr(1, 15), fr(1, 5))))

    # which equation matches the model
    for n, b in [(4, 3), (3, 5)]:
        q = (fig(tape_svg(n, b)) + "The picture shows %d wholes cut into %s. Which division equation matches?"
             % (n, parts(b)))
        right = "%s = %d" % (wu(n, b), n * b)
        wrong = ["%s = %s" % (uw(b, n), fr(1, n * b)), "%d ÷ %d = %d" % (n, b, n * b), "%d ÷ %s = %d" % (n * b, fr(1, b), n)]
        e = ("The picture asks how many %s are in %d. There are %d, so %s = %d. %s"
             % (parts(b), n, n * b, wu(n, b), n * b, check_wu(n, b)))
        its.append(mcq(q, right, wrong, e))
    for b, n in [(3, 4), (6, 2)]:
        q = (fig(area_svg(b, n)) + "The picture shows %s of a rectangle cut into %d equal pieces. "
             "Which division equation matches?" % (fr(1, b), n))
        right = "%s = %s" % (uw(b, n), fr(1, b * n))
        wrong = ["%s = %d" % (wu(n, b), n * b), "%s = %s" % (uw(b, n), fr(1, n)), "%s ÷ %d = %s" % (fr(1, b * n), n, fr(1, b))]
        e = ("%s is cut into %d equal pieces. The whole rectangle has %d of those pieces, so each one is %s of the whole: "
             "%s = %s. (%s is only part of the green column, not of the whole.) %s"
             % (fr(1, b), n, b * n, fr(1, b * n), uw(b, n), fr(1, b * n), fr(1, n), check_uw(b, n)))
        its.append(mcq(q, right, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Compute and check with multiplication", "items": its}


# ============================================================ set 4: compare and reason
def set_reason(P):
    its = []
    for n, b in [(6, 2), (5, 3), (8, 4)]:
        q = "Without finding the answer, %s is ___ %d." % (wu(n, b), n)
        e = ("Each whole holds %d %s, so there are more %s than wholes. %s is greater than %d (it is %d)."
             % (b, parts(b), parts(b), wu(n, b), n, n * b))
        its.append(mcq(q, "greater than", ["less than", "equal to", "%s of" % ("half" if b == 2 else "one " + parts(b, 1))], e))
    for b, n in [(4, 3), (2, 5), (6, 2)]:
        q = "Without finding the answer, %s is ___ %s." % (uw(b, n), fr(1, b))
        e = ("Cutting %s into %d equal parts makes each part smaller than %s. %s is less than %s (it is %s)."
             % (fr(1, b), n, fr(1, b), uw(b, n), fr(1, b), fr(1, b * n)))
        its.append(mcq(q, "less than", ["greater than", "equal to", "%d times" % n], e))

    # which is greater
    pairs = [
        ((wu(3, 2), F(6)), (uw(2, 3), F(1, 6))),
        ((wu(4, 6), F(24)), (wu(4, 3), F(12))),
        ((uw(3, 2), F(1, 6)), (uw(3, 4), F(1, 12))),
        ((wu(2, 5), F(10)), (wu(5, 2), F(10))),
        ((uw(2, 4), F(1, 8)), (uw(4, 2), F(1, 8))),
    ]
    for (x, xv), (y, yv) in pairs:
        if xv == yv:
            right = "They are equal."
        else:
            right = x if xv > yv else y
        q = "Which is greater: %s or %s?" % (x, y)
        e = "%s = %s and %s = %s. " % (x, num(xv), y, num(yv))
        if xv == yv:
            e += "Both are %s, so <b>they are equal</b>." % num(xv)
        else:
            e += "%s is greater than %s." % (num(max(xv, yv)), num(min(xv, yv)))
            if "÷ %s" % fr(1, 6) in x:
                e += " Sixths are smaller than thirds, so more of them fit in 4."
            elif x.startswith(fr(1, 3)):
                e += " Cutting into fewer parts makes bigger parts."
        its.append(mcq(q, right, [x, y, "They are equal.", "You can’t tell."], e))

    # find the mistake
    M = {
        "times": "multiplied instead of dividing",
        "kind": "mixed up the two kinds of division",
        "wb": "divided by the bottom number only",
        "part": "found a part of the fraction, not of the whole",
        "ok": "nothing; the answer is correct",
    }
    cases = [
        ("times", "u", 3, 4, fr(4, 3)),
        ("kind", "u", 5, 2, "10"),
        ("wb", "w", 4, 3, fr(4, 3)),
        ("part", "u", 2, 3, fr(1, 3)),
        ("ok", "w", 2, 6, "12"),
    ]
    for kind, typ, x, y, wrote in cases:
        nm, he, his = P.next()
        expr = uw(x, y) if typ == "u" else wu(x, y)
        q = "%s says %s = %s. What did %s do?" % (nm, expr, wrote, he)

        def say(k):
            return cap(M[k]) + "." if k == "ok" else cap("%s %s." % (he, M[k]))
        right = say(kind)
        wrong = [say(k) for k in ["ok", "times", "kind", "wb", "part"] if k != kind]
        if typ == "u":
            b, n = x, y
            good = "%s = %s. %s" % (uw(b, n), fr(1, b * n), check_uw(b, n))
            if kind == "times":
                e = "%s found %s × %d = %s. Dividing %s into %d parts must give a smaller piece: %s" % (nm, fr(1, b), n, fr(n, b), fr(1, b), n, good)
            elif kind == "kind":
                e = "%s found %s, which asks how many %s are in %d. Here %s is cut into %d parts: %s" % (nm, wu(n, b), parts(b), n, fr(1, b), n, good)
            else:
                e = ("%s is the size of one part compared with %s, not with the whole. The whole has %d × %d = %d such parts: %s"
                     % (fr(1, n), fr(1, b), b, n, b * n, good))
        else:
            n, b = x, y
            good = "%s = %d. %s" % (wu(n, b), n * b, check_wu(n, b))
            if kind == "wb":
                e = ("%s found %d ÷ %d = %s. The question asks how many %s are in %d, and that is more than %d: %s"
                     % (nm, n, b, fr(n, b), parts(b), n, n, good))
            else:
                e = "Each whole has %d %s, so %d wholes have %d. %s is right: %s" % (b, parts(b), n, n * b, nm, good)
        its.append(mcq(q, right, wrong, e))

    # what does the division mean
    def means(n, b):
        return {"wu": "the number of %s in %d" % (parts(b), n),
                "uw": "%s cut into %d equal parts" % (fr(1, b), n),
                "whole": "%d cut into %d equal parts" % (n, b),
                "times": "%s of %d" % (fr(1, b), n)}
    for typ, n, b in [("wu", 3, 4), ("uw", 3, 4), ("wu", 2, 5), ("uw", 2, 6)]:
        m = means(n, b)
        expr = wu(n, b) if typ == "wu" else uw(b, n)
        q = "Which describes %s?" % expr
        if typ == "wu":
            e = "%s asks how many %s fit in %d. That is %d, because %s" % (expr, parts(b), n, n * b, check_wu(n, b)[7:])
        else:
            e = "%s means cut %s into %d equal parts. Each part is %s. %s" % (expr, fr(1, b), n, fr(1, b * n), check_uw(b, n))
        other = "uw" if typ == "wu" else "wu"
        its.append(mcq(q, cap(m[typ]), [cap(m[other]), cap(m["whole"]), cap(m["times"])], e))
    assert len(its) == 20, len(its)
    return {"title": "Compare, explain and find mistakes", "items": its}


# ============================================================ set 5: word problems
UNITS = {"pound": ("pound", "pounds"), "gallon": ("gallon", "gallons"), "hour": ("hour", "hours"),
         "mile": ("mile", "miles"), "cup": ("cup", "cups"), "liter": ("liter", "liters")}


def qty(v, unit):
    one, many = UNITS[unit]
    return "%s %s" % (num(v), one if v <= 1 else many)


def set_words(P):
    its = []

    def count(story, n, b, what):
        e = "%s: %s = <b>%d</b> %s. %s" % (cap(what), wu(n, b), n * b, story[1], check_wu(n, b))
        its.append(mcq(story[0], (str(n * b), F(n * b)), wu_wrongs(n, b), e))

    def share(story, b, n, unit=None):
        def show(h, v):
            return "%s %s" % (h, UNITS[unit][0] if v <= 1 else UNITS[unit][1]) if unit else h
        right = show(fr(1, b * n), F(1, b * n))
        cands = [(show(h, v), v) for h, v in uw_wrongs(b, n)]
        e = "%s is cut into %d equal parts: %s = <b>%s</b>. %s" % (story[1], n, uw(b, n), right, check_uw(b, n))
        its.append(mcq(story[0], (right, F(1, b * n)), cands, e))

    nm, he, his = P.next()
    count(("%s has 5 pounds of trail mix. %s puts %s pound in each bag. How many bags can %s fill?"
           % (nm, cap(he), fr(1, 4), he), "bags"), 5, 4, "find how many %s-pound parts are in 5 pounds" % fr(1, 4))
    nm, he, his = P.next()
    count(("%s has a ribbon 3 meters long. %s cuts it into pieces that are each %s meter long. How many pieces does %s get?"
           % (nm, cap(he), fr(1, 5), he), "pieces"), 3, 5, "find how many %s-meter pieces are in 3 meters" % fr(1, 5))
    count(("A pot holds 4 cups of rice. One serving is %s cup. How many servings are in the pot?" % fr(1, 3),
           "servings"), 4, 3, "find how many %s-cup servings are in 4 cups" % fr(1, 3))
    count(("A class has 2 hours for book talks. Each book talk takes %s hour. How many book talks fit?" % fr(1, 4),
           "book talks"), 2, 4, "find how many %s-hour talks fit in 2 hours" % fr(1, 4))
    count(("Each pizza is cut into slices that are %s of a pizza. How many slices are in 3 pizzas?" % fr(1, 8),
           "slices"), 3, 8, "find how many eighths are in 3 wholes")
    nm, he, his = P.next()
    count(("%s has 8 yards of rope. Each jump rope needs %s yard. How many jump ropes can %s make?" % (nm, fr(1, 2), he),
           "jump ropes"), 8, 2, "find how many %s-yard pieces are in 8 yards" % fr(1, 2))
    count(("A jug holds 7 liters of juice. Each cup holds %s liter. How many cups can be filled?" % fr(1, 4),
           "cups"), 7, 4, "find how many %s-liter cups are in 7 liters" % fr(1, 4))
    count(("A trail is 2 miles long. There is a sign every %s mile. How many %s-mile sections does the trail have?"
           % (fr(1, 10), fr(1, 10)), "sections"), 2, 10, "find how many %s-mile sections are in 2 miles" % fr(1, 10))
    nm, he, his = P.next()
    count(("%s has 3 pounds of clay. Each small pot uses %s pound. How many pots can %s make?" % (nm, fr(1, 6), he),
           "pots"), 3, 6, "find how many %s-pound parts are in 3 pounds" % fr(1, 6))

    (n1, h1, _), (n2, h2, _) = P.next(), P.next()
    share(("%s of a pizza is left. %s and %s share it equally. What fraction of the whole pizza does each friend get?"
           % (fr(1, 3), n1, n2), fr(1, 3)), 3, 2)
    share(("%s of a pan of brownies is left. 4 friends share it equally. What fraction of the whole pan does each friend get?"
           % fr(1, 2), fr(1, 2)), 2, 4)
    nm, he, his = P.next()
    share(("%s has %s pound of cheese. %s cuts it into 3 equal pieces. How much does each piece weigh?"
           % (nm, fr(1, 4), cap(he)), fr(1, 4) + " pound"), 4, 3, "pound")
    share(("%s gallon of milk is poured equally into 5 glasses. How much milk is in each glass?" % fr(1, 2),
           fr(1, 2) + " gallon"), 2, 5, "gallon")
    nm, he, his = P.next()
    share(("%s plants %s of %s garden with 2 kinds of flowers. Each kind gets an equal part. What fraction of the whole garden "
           "is each kind?" % (nm, fr(1, 5), his), fr(1, 5)), 5, 2)
    nm, he, his = P.next()
    share(("%s practices piano for %s hour. %s spends equal time on 4 songs. How long does %s spend on each song?"
           % (nm, fr(1, 3), cap(he), he), fr(1, 3) + " hour"), 3, 4, "hour")
    share(("A path in the park is %s mile long. It is split into 3 equal parts for a relay race. How long is each part?"
           % fr(1, 2), fr(1, 2) + " mile"), 2, 3, "mile")
    (n1, h1, _), (n2, h2, _) = P.next(), P.next()
    share(("%s and %s share %s of a cake equally. What fraction of the whole cake does each one get?"
           % (n1, n2, fr(1, 8)), fr(1, 8)), 8, 2)

    # which expression
    nm, he, his = P.next()
    q = "%s has 3 cups of flour. Each batch of pancakes needs %s cup. Which expression shows how many batches %s can make?" % (nm, fr(1, 4), he)
    e = "The question asks how many %s-cup parts are in 3 cups: %s = 12 batches. %s" % (fr(1, 4), wu(3, 4), check_wu(3, 4))
    its.append(mcq(q, wu(3, 4), [uw(4, 3), "3 × %s" % fr(1, 4), "3 ÷ 4"], e))
    q = "%s of a sandwich is shared equally by 3 children. Which expression shows how much of the sandwich each child gets?" % fr(1, 2)
    e = "%s is cut into 3 equal parts: %s = %s of the sandwich. %s" % (fr(1, 2), uw(2, 3), fr(1, 6), check_uw(2, 3))
    its.append(mcq(q, uw(2, 3), [wu(3, 2), "3 × %s" % fr(1, 2), "3 ÷ 2"], e))

    # compare two people
    (n1, h1, _), (n2, h2, _) = P.next(), P.next()
    q = ("%s has 2 pounds of beads and puts %s pound in each bag. %s has 3 pounds of beads and puts %s pound in each bag. "
         "Who fills more bags?" % (n1, fr(1, 4), n2, fr(1, 2)))
    e = ("%s: %s = 8 bags. %s: %s = 6 bags. 8 is more than 6, so <b>%s</b> fills more bags. %s has fewer beads, "
         "but %s bags are smaller." % (n1, wu(2, 4), n2, wu(3, 2), n1, cap(h1), fr(1, 4) + "-pound"))
    its.append(mcq(q, n1, [n2, "They fill the same number.", "You can’t tell."], e))
    assert len(its) == 20, len(its)
    return {"title": "Word problems", "items": its}


# ============================================================ lesson
def body_html():
    tape = ("<figure class='sn-fig'>" + tape_svg(3, 4, PW=26) +
            "<figcaption>3 wholes, each cut into fourths. Count the fourths: 3 × 4 = 12, so 3 ÷ " + fr(1, 4) + " = 12.</figcaption></figure>")
    area = ("<figure class='sn-fig'>" + area_svg(2, 3, W=240, H=144) +
            "<figcaption>The green half is cut into 3 equal pieces. The dashed lines show that the whole has 6 of these pieces, "
            "so the dark piece is " + fr(1, 6) + ": " + fr(1, 2) + " ÷ 3 = " + fr(1, 6) + ".</figcaption></figure>")
    return (
        "<h2>The big idea: two kinds of division</h2>"
        "<p>In Grade 5 you divide with <b>unit fractions</b> (fractions with 1 on top) in two ways.</p>"
        + table(["Problem", "Question it asks", "Answer"], [
            [wu(3, 4), "How many fourths are in 3?", "12 (bigger than 3)"],
            [uw(2, 3), "Cut " + fr(1, 2) + " into 3 equal parts. How big is each part?", fr(1, 6) + " (smaller than " + fr(1, 2) + ")"],
        ]) +
        "<h2>Whole number ÷ unit fraction</h2>"
        "<p>Ask: <b>how many of the unit fraction fit</b> in the whole number? Each whole has 4 fourths, so 3 wholes have 3 × 4 = 12 fourths.</p>"
        + tape
        + ex("Example", "How many " + fr(1, 3) + "-cup scoops are in 5 cups?",
             "Each cup has 3 thirds. 5 × 3 = 15, so 5 ÷ " + fr(1, 3) + " = 15.", "15 scoops")
        + "<h2>Unit fraction ÷ whole number</h2>"
        "<p>Cut the fraction into that many <b>equal parts</b>. Then ask: what fraction of the <b>whole</b> is one part?</p>"
        + area
        + ex("Example", fr(1, 4) + " of a pizza is shared equally by 2 friends. How much of the pizza does each friend get?",
             "Cut " + fr(1, 4) + " into 2 equal parts. The whole pizza has 4 × 2 = 8 of these parts, so " + uw(4, 2) + " = " + fr(1, 8) + ".",
             fr(1, 8) + " of the pizza")
        + "<h2>Check with multiplication</h2>"
        "<p>Multiply the answer by the number you divided by. You should get the number you started with.</p>"
        + table(["Division", "Check"], [
            [uw(3, 4) + " = " + fr(1, 12), fr(1, 12) + " × 4 = " + fr(4, 12) + " = " + fr(1, 3)],
            [wu(4, 3) + " = 12", "12 × " + fr(1, 3) + " = " + fr(12, 3) + " = 4"],
        ])
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            [wu(4, 3) + " = " + fr(4, 3) + " (dividing 4 by 3)", "Count the thirds in 4: 4 × 3 = 12. The answer is bigger than 4."],
            [uw(3, 4) + " = " + fr(4, 3) + " (multiplying)", "Cutting into parts makes them smaller: " + fr(1, 12)],
            [uw(3, 4) + " = 12 (mixing up the two kinds)", "12 is " + wu(4, 3) + ". Here " + fr(1, 3) + " is cut into 4 parts."],
            [uw(2, 3) + " = " + fr(1, 3) + " (a part of the half)", "Compare with the whole: 6 parts make 1, so " + fr(1, 6)],
        ])
    )


FAQ = [
    {"q": "How do you divide a whole number by a unit fraction?",
     "a": "Ask how many of the unit fraction fit in the whole number. 3 ÷ 1/4 = 12, because each whole has 4 fourths and 3 × 4 = 12."},
    {"q": "How do you divide a unit fraction by a whole number?",
     "a": "Cut the fraction into that many equal parts and see what part of the whole each piece is. 1/2 ÷ 3 = 1/6, because 1/6 × 3 = 1/2."},
    {"q": "Why is the answer bigger when you divide by a fraction?",
     "a": "Dividing by 1/2 asks how many halves fit, and every whole holds 2 halves. So 6 ÷ 1/2 = 12, which is greater than 6."},
    {"q": "Do 5th graders learn keep-change-flip?",
     "a": "No. Standard 5.NF.B.7 covers only unit fractions and whole numbers, solved with models and a multiplication check. Dividing any fraction by any fraction comes in Grade 6 (6.NS.A.1)."},
]


def gen():
    rnd = random.Random(503)
    P = People(rnd)
    sets = [set_wu_models(), set_uw_models(), set_compute(), set_reason(P), set_words(P)]
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
        "country": "us", "subject": "math", "grade": "grade-5", "slug": "divide-fractions", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Divide Unit Fractions and Whole Numbers",
        "seo_title": "Grade 5 Dividing Fractions Worksheets: Unit Fractions ÷ Whole Numbers, Whole Numbers ÷ Unit Fractions, Models and Word Problems",
        "short_title": "Divide fractions",
        "domain": "Number and Operations—Fractions",
        "standard_code": "5.NF.B.7",
        "standard_url": "https://www.thecorestandards.org/Math/Content/5/NF/B/7/",
        "standard_text": "Apply and extend previous understandings of division to divide unit fractions by whole numbers and whole numbers by unit fractions. Interpret division of a unit fraction by a non-zero whole number, and compute such quotients. Interpret division of a whole number by a unit fraction, and compute such quotients. Solve real world problems involving division of unit fractions by non-zero whole numbers and division of whole numbers by unit fractions.",
        "meta_desc": "Free Grade 5 worksheets on dividing fractions: find how many 1/4s are in 3, share 1/2 into 3 equal parts, use fraction bars, area models and number lines, check with multiplication, and solve sharing and serving word problems. 100 practice questions with answers.",
        "key_big": "3 ÷ 1/4 asks how many fourths are in 3. 1/2 ÷ 3 cuts 1/2 into 3 equal parts.",
        "key_sub": "3 ÷ 1/4 = 12, because 12 × 1/4 = 3. 1/2 ÷ 3 = 1/6, because 1/6 × 3 = 1/2. Dividing by a unit fraction gives a bigger number; dividing a unit fraction by a whole number gives a smaller piece.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(number line|[^']*: [1-9][0-9] pieces)")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
