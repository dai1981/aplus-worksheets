# -*- coding: utf-8 -*-
"""
British Columbia Grade 6 Math: One-Step Equations
(BC Mathematics Curriculum, Grade 6 — Patterning: one-step equations with whole-number coefficients and solutions)
  python3 tools/gen_cabc_math_g6_equations.py
Pan balances and the equal sign, solving x + 12 = 30 and x − 9 = 20 (to the millions), 5x = 35, x ÷ 4 = 8,
and writing and solving equations from stories in BC contexts.
Wrong choices come from real mistakes: using the same operation instead of the inverse (x + 12 = 30 -> 42,
5x = 35 -> 175, x ÷ 4 = 8 -> 2), subtracting the coefficient (5x = 35 -> 30), smaller-digit-from-larger,
forgetting to carry, place-value slips with multiples of 10, and neighbouring facts.
Every answer is checked in code. HTML attributes use single quotes. Canadian English, BC numbers (10 000).
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
GREY = "#e4e4e4"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
M = "−"
NB = " "
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia", "Ji-woo"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]


# ------------------------------------------------------------ numbers
def n(x):
    """BC style: 4 digits no separator, 5 or more digits grouped with a no-break space."""
    x = int(x)
    s = str(abs(x))
    if abs(x) >= 10000:
        out = ""
        while len(s) > 3:
            out = NB + s[-3:] + out
            s = s[:-3]
        s = s + out
    return (M if x < 0 else "") + s


def sfl(a, b):
    """Smaller digit from larger digit in each column: 30 − 12 -> 22 (a typical mistake)."""
    da, db = str(a), str(b).rjust(len(str(a)), "0")
    return int("".join(str(abs(int(x) - int(y))) for x, y in zip(da, db)))


def nocarry(a, b):
    """Add column by column and drop every carried ten: 75 + 48 -> 13."""
    out, p = 0, 1
    while a or b:
        out += ((a % 10 + b % 10) % 10) * p
        a, b, p = a // 10, b // 10, p * 10
    return out


# ------------------------------------------------------------ equations in a mini syntax
# "x + 12 = 30", "5x = 35", "x / 4 = 8" (÷), "x * 6 = 90" (×), "84 = x + 29"; tokens separated by spaces.
def V(v):
    return "<i>%s</i>" % v


def render(s):
    out = []
    for t in s.split(" "):
        if re.match(r"^\d+[a-z]$", t):
            out.append(n(t[:-1]) + V(t[-1]))
        elif re.match(r"^[a-z]$", t):
            out.append(V(t))
        elif re.match(r"^\d+$", t):
            out.append(n(t))
        else:
            out.append({"-": M, "*": "×", "/": "÷"}.get(t, t))
    return " ".join(out)


def ev(side, x):
    s = []
    for t in side.split(" "):
        if re.match(r"^\d+[a-z]$", t):
            s.append("(F(%s)*X)" % t[:-1])
        elif re.match(r"^[a-z]$", t):
            s.append("X")
        elif re.match(r"^\d+$", t):
            s.append("F(%s)" % t)
        else:
            s.append(t)
    return eval(" ".join(s), {"__builtins__": {}, "F": F, "X": F(x)})


def holds(s, x):
    a, b = s.split(" = ")
    return ev(a, x) == ev(b, x)


def var_of(s):
    return re.search(r"[a-z]", s).group(0)


def solve_eq(s):
    """Solve a one-step equation (linear in the unknown, or c ÷ x = q); the solution must be a whole number > 0."""
    if re.search(r"/ [a-z]\b", s):
        a, b = s.split(" = ")
        side, c = (a, b) if re.search(r"[a-z]", a) else (b, a)
        p = int(side.split(" ")[0])
        x = F(p) / ev(c, 0)
    else:
        f0 = ev(s.split(" = ")[0], 0) - ev(s.split(" = ")[1], 0)
        f1 = ev(s.split(" = ")[0], 1) - ev(s.split(" = ")[1], 1)
        x = -f0 / (f1 - f0)
    assert x.denominator == 1 and x > 0, (s, x)
    x = int(x)
    assert holds(s, x), s
    return x


def whole(v):
    v = F(v)
    return int(v) if v.denominator == 1 and v > 0 else None


# ------------------------------------------------------------ question helpers
def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def mcq(q, correct, cands, e):
    """correct + the first 3 unique distractors (strings). Positions are set later by balance()."""
    seen, pick = {plain(correct)}, []
    for c in cands:
        if c is None or plain(c) in seen:
            continue
        seen.add(plain(c))
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def fmt(v, unit=None):
    if unit is None:
        return n(v)
    if unit == "$":
        return "$" + n(v)
    sing, plur = unit
    return "%s %s" % (n(v), sing if v == 1 else plur)


def mcq_n(q, x, cands, e, unit=None, notes=True):
    """cands: (value, why) pairs or plain values. Only whole, positive, new values are used; the reasons
    for the wrong answers used are added to the explanation."""
    used, add = {x}, []
    for c in cands:
        val, why = c if isinstance(c, tuple) else (c, None)
        w = whole(val)
        if w is None or w in used:
            continue
        used.add(w)
        add.append((w, why))
        if len(add) == 3:
            break
    assert len(add) == 3, (q, x, cands)
    it = mcq(q, fmt(x, unit), [fmt(w, unit) for w, _ in add], e)
    why = ["%s comes from %s" % (fmt(w, unit), t) for w, t in add if t]
    if notes and why:
        it["e"] += " Wrong answers: " + "; ".join(why) + "."
    return it


def near(x, k=1):
    return [x + k, x - k, x + 2 * k, x - 2 * k]


def step_of(x):
    return 10 ** max(0, len(str(x)) - 2)


def balance(sets, rnd):
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [y for i, y in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


class People:
    def __init__(self, rnd):
        self.pool = [(x, "she", "her", "her") for x in GIRLS] + [(x, "he", "his", "him") for x in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ solving one-step equations: steps and mistakes
def analyse(s):
    """Return (x, steps text, [(wrong value, why)]) for a one-step equation in the mini syntax."""
    x = solve_eq(s)
    v = var_of(s)
    a, b = s.split(" = ")
    side, c = (a, b) if re.search(r"[a-z]", a) else (b, a)
    c = int(c) if re.match(r"^\d+$", c) else int(ev(c, 0))
    t = side.split(" ")
    X = V(v)
    if len(t) == 1:                                        # 5x = 35
        k = int(t[0][:-1])
        steps = ("%s means %d × %s. Divide both sides by %s: %s = %s ÷ %s = <b>%s</b>. Check: %s × %s = %s."
                 % (render(t[0]), k, X, n(k), X, n(c), n(k), n(x), n(k), n(x), n(c)))
        wr = [(c - k, "subtracting %s instead of dividing" % n(k)),
              (c * k, "multiplying by %s instead of dividing" % n(k))]
        if k % 10 == 0:
            wr += [(x * 10, "a place-value slip with the zeros"), (F(x, 10), "a place-value slip with the zeros")]
        wr += near(x)
    elif t[1] == "*":                                      # x × 6 = 90 or 6 × x = 90
        k = int(t[2]) if t[0] == v else int(t[0])
        steps = ("Divide both sides by %s: %s = %s ÷ %s = <b>%s</b>. Check: %s."
                 % (n(k), X, n(c), n(k), n(x), render(side.replace(v, str(x))) + " = " + n(c)))
        wr = [(c - k, "subtracting %s instead of dividing" % n(k)), (c * k, "multiplying by %s instead of dividing" % n(k))] + near(x)
    elif t[1] == "+":                                      # x + a = c or a + x = c
        k = int(t[2]) if t[0] == v else int(t[0])
        steps = ("Subtract %s from both sides: %s = %s − %s = <b>%s</b>. Check: %s = %s."
                 % (n(k), X, n(c), n(k), n(x), render(side.replace(v, str(x))), n(c)))
        wr = [(c + k, "adding %s instead of subtracting it" % n(k))]
        if sfl(c, k) != x:
            wr.append((sfl(c, k), "taking the smaller digit from the larger in each column"))
        wr += near(x, step_of(x)) + near(x, 1)
    elif t[1] == "-" and t[0] == v:                        # x − a = c
        k = int(t[2])
        steps = ("Add %s to both sides: %s = %s + %s = <b>%s</b>. Check: %s = %s."
                 % (n(k), X, n(c), n(k), n(x), render(side.replace(v, str(x))), n(c)))
        wr = [(c - k, "subtracting %s again instead of adding it" % n(k)) if c > k else
              (k - c, "subtracting instead of adding")]
        if nocarry(c, k) != x:
            wr.append((nocarry(c, k), "forgetting to carry"))
        wr += near(x, step_of(x)) + near(x, 1)
    elif t[1] == "-":                                      # a − x = c
        k = int(t[0])
        steps = ("%s take away what leaves %s? %s = %s − %s = <b>%s</b>. Check: %s = %s."
                 % (n(k), n(c), X, n(k), n(c), n(x), render(side.replace(v, str(x))), n(c)))
        wr = [(k + c, "adding the two numbers")]
        if sfl(k, c) != x:
            wr.append((sfl(k, c), "taking the smaller digit from the larger in each column"))
        wr += near(x, step_of(x)) + near(x, 1)
    elif t[1] == "/" and t[0] == v:                        # x ÷ a = c
        k = int(t[2])
        steps = ("%s is the number you start with. Multiply both sides by %s: %s = %s × %s = <b>%s</b>. Check: %s ÷ %s = %s."
                 % (X, n(k), X, n(c), n(k), n(x), n(x), n(k), n(c)))
        wr = []
        if c % k == 0:
            wr.append((c // k, "dividing by %s again instead of multiplying" % n(k)))
        wr.append((c + k, "adding %s instead of multiplying" % n(k)))
        if k % 10 == 0:
            wr += [(x * 10, "a place-value slip with the zeros"), (F(x, 10), "a place-value slip with the zeros")]
        if c > k:
            wr.append((c - k, "subtracting %s" % n(k)))
        wr += [(k * (c + 1), None), (k * (c - 1), None)]
    else:                                                  # a ÷ x = c
        k = int(t[0])
        steps = ("%s shared into how many groups gives %s in each? %s = %s ÷ %s = <b>%s</b>. Check: %s ÷ %s = %s."
                 % (n(k), n(c), X, n(k), n(c), n(x), n(k), n(x), n(c)))
        wr = [(k * c, "multiplying instead of dividing"), (k - c, "subtracting"), (k + c, "adding")] + near(x)
    return x, steps, wr


def solve_item(s, prompt=None, pic=None):
    x, steps, wr = analyse(s)
    v = var_of(s)
    q = (prompt or "Solve %s. What is %s?") % (render(s), V(v))
    return mcq_n(q + (fig(pic) if pic else ""), x, wr, steps)


# ------------------------------------------------------------ pictures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(round(w)), int(round(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    return len(t) * fs * 0.6


def text(x, y, t, fs=18, col=INK, italic=False, bold=True):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s%s fill='%s' text-anchor='middle'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", " font-style='italic'" if italic else "", col, t))


def scale_svg(left, right):
    """A level pan balance. left / right: lists of a letter (a block of unknown mass) or a number (a weight)."""
    def item_w(t):
        return 34 if t.isalpha() else max(34, int(tw(t, 18) + 14))
    gap = 6

    def pan_w(items):
        return max(80, sum(item_w(t) for t in items) + gap * (len(items) - 1) + 16)
    wl, wr = pan_w(left), pan_w(right)
    cl = 8 + wl / 2
    cr = cl + wl / 2 + 44 + wr / 2
    mid = (cl + cr) / 2
    top, ih = 10, 34
    py = top + ih
    s = []
    for items, c, w in ((left, cl, wl), (right, cr, wr)):
        tot = sum(item_w(t) for t in items) + gap * (len(items) - 1)
        x = c - tot / 2
        for t in items:
            iw = item_w(t)
            if t.isalpha():
                s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (x, top, iw, ih, FILL, GREEN))
                s.append(text(x + iw / 2, top + 24, t, 18, col=RED, italic=True))
            else:
                s.append("<rect x='%.1f' y='%d' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='2'/>" % (x, top, iw, ih, GREY, INK))
                s.append(text(x + iw / 2, top + 24, n(t)))
            x += iw + gap
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='6' fill='%s'/>" % (c - w / 2, py, w, INK))
        s.append("<rect x='%.1f' y='%d' width='4' height='18' fill='%s'/>" % (c - 2, py + 6, INK))
    by = py + 24
    s.append("<rect x='%.1f' y='%d' width='%.1f' height='6' fill='%s'/>" % (cl - 2, by, cr - cl + 4, INK))
    s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (mid, by + 6, mid - 22, by + 40, mid + 22, by + 40, GREEN))
    s.append("<rect x='%.1f' y='%d' width='80' height='5' fill='%s'/>" % (mid - 40, by + 40, INK))

    def say(items):
        return " and ".join(("block " + t) if t.isalpha() else n(t) for t in items)
    return svg_wrap(cr + wr / 2 + 8, by + 47, "".join(s),
                    "pan balance: %s on the left, %s on the right" % (say(left), say(right)))


def lab_t(t, x, y, fs=18):
    """Label in a bar: a letter in red italics, a number in ink."""
    if isinstance(t, str) and t.isalpha():
        return text(x, y, t, fs, col=RED, italic=True)
    return text(x, y, n(t), fs)


def parts_svg(k, part, total):
    """Equal-parts bar: k equal parts, each labelled part, with the total above a bracket.
    part / total are numbers or a letter."""
    cw = 50 if k <= 5 else (42 if k <= 7 else 36)
    x0, y = 8, 40
    s = []
    for i in range(k):
        s.append("<rect x='%d' y='%d' width='%d' height='36' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (x0 + i * cw, y, cw, FILL, GREEN))
        s.append(lab_t(part, x0 + i * cw + cw / 2, y + 25, 18 if len(str(part)) <= 3 else 15))
    x1 = x0 + k * cw
    s.append("<path d='M%d %d v-8 H%d v8' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y - 4, x1, INK))
    s.append(lab_t(total, (x0 + x1) / 2, y - 16))

    def say(t):
        return ("block " + t) if isinstance(t, str) else n(t)
    return svg_wrap(x1 + 8, y + 44, "".join(s), "equal parts bar: %d equal parts of %s make %s" % (k, say(part), say(total)))


def bar_svg(whole_, p1, p2):
    """Part-part-whole bar model drawn to scale. One value is a letter."""
    vals = [whole_, p1, p2]
    nums = [v if isinstance(v, int) else None for v in vals]
    m = [i for i, v in enumerate(nums) if v is None]
    assert len(m) == 1
    full = list(nums)
    m = m[0]
    full[m] = (nums[1] + nums[2]) if m == 0 else (nums[0] - (nums[2] if m == 1 else nums[1]))
    assert full[1] + full[2] == full[0] and min(full) > 0
    W, x0, h = 300, 8, 36
    w1 = round(W * full[1] / full[0])
    w1 = min(max(w1, 80), W - 80)
    s = []
    rows = [(8, [(x0, W, whole_, FILL)]), (8 + h + 10, [(x0, w1, p1, "#fff"), (x0 + w1, W - w1, p2, "#fff")])]
    for y, cells in rows:
        for x, w, v, f in cells:
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                     % (x, y, w, h, f, GREEN))
            s.append(lab_t(v, x + w / 2, y + 25))

    def say(t):
        return ("block " + t) if isinstance(t, str) else n(t)
    return svg_wrap(W + 16, 8 + 2 * h + 10 + 8, "".join(s),
                    "bar model: whole %s, parts %s and %s" % tuple(say(v) for v in vals))


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ============================================================ set 1: balances and the equal sign
def set_balance(P):
    its = []
    LEVEL = "The pan balance is level. Each block has the same mass, %s. "
    # A. which equation matches the balance
    for L, R, right, wr in [
        (["x", "12"], ["30"], "x + 12 = 30", ["x = 12 + 30", "x - 12 = 30", "12x = 30"]),
        (["x", "x", "x", "x"], ["28"], "4x = 28", ["x + 4 = 28", "x / 4 = 28", "28x = 4"]),
        (["45"], ["y", "19"], "45 = y + 19", ["45 + 19 = y", "45 = y - 19", "19y = 45"]),
        (["n", "n", "n", "n", "n"], ["30", "15"], "5n = 30 + 15", ["5 + n = 45", "5n = 30", "n = 30 + 15 + 5"]),
    ]:
        x = solve_eq(right)
        assert not any(holds(w, x) for w in wr)
        v = var_of(right)
        if len(L) >= 4:
            e = ("There are %d blocks %s on one pan. %d equal blocks is %s, which means %d × %s. So <b>%s</b>. "
                 "Then %s = %s." % (len(L), V(v), len(L), render("%d%s" % (len(L), v)), len(L), V(v), render(right), V(v), n(x)))
        else:
            e = ("The pans balance, so both sides are equal. Write what is on each pan with = between them: <b>%s</b>. "
                 "Then %s = %s." % (render(right), V(v), n(x)))
        its.append(mcq("The pans balance. Which equation matches?" + fig(scale_svg(L, R)), render(right),
                       [render(w) for w in wr], e))
    # B. balance: what is the unknown
    for L, R, s in [
        (["x", "25"], ["60"], "x + 25 = 60"),
        (["m", "m", "m"], ["21"], "3m = 21"),
        (["k", "140"], ["500"], "k + 140 = 500"),
        (["a", "a", "a", "a", "a", "a"], ["54"], "6a = 54"),
        (["72"], ["p", "38"], "72 = p + 38"),
        (["y", "9"], ["14", "20"], "y + 9 = 34"),
        (["t", "t"], ["40", "16"], "2t = 56"),
    ]:
        x, steps, wr = analyse(s)
        v = var_of(s)
        pre = ""
        if len(R) == 2 and all(r.isdigit() for r in R):
            pre = "The right pan has %s + %s = %s. So %s. " % (n(R[0]), n(R[1]), n(int(R[0]) + int(R[1])), render(s))
        else:
            pre = "The balance shows %s. " % render(s)
        its.append(mcq_n(LEVEL % V(v) + "What is %s?" % V(v) + fig(scale_svg(L, R)), x, wr, pre + steps))
    # C. keeping the balance level
    its.append(mcq("The balance shows " + render("x + 12 = 30") + ". You take 12 off the left pan. "
                   "What must you do to the right pan to keep it level?",
                   "Take 12 off it too", ["Add 12 to it", "Take 30 off it", "Nothing"],
                   "Whatever you do to one side, do to the other side. <b>Take 12 off the right pan too</b>: "
                   + V("x") + " = 30 − 12 = 18. Adding 12 to the right pan would make it tip."))
    its.append(mcq("The balance shows " + render("4x = 28") + ". To find one block, you split the left pan into "
                   "4 equal groups. What must you do to the right side?",
                   "Divide 28 by 4", ["Subtract 4 from 28", "Multiply 28 by 4", "Leave it as 28"],
                   "Do the same to both sides. Split both sides into 4 equal groups: <b>28 ÷ 4</b> = 7, so "
                   + V("x") + " = 7. Subtracting 4 undoes + 4, not × 4."))
    its.append(mcq("Which step solves " + render("x - 9 = 20") + " and keeps both sides equal?",
                   "Add 9 to both sides",
                   ["Subtract 9 from both sides", "Add 9 to one side only", "Add 20 to both sides"],
                   "Adding undoes subtracting. <b>Add 9 to both sides</b>: " + V("x") + " = 20 + 9 = 29. Check: 29 − 9 = 20. "
                   "Subtracting 9 again is the same operation, not the inverse."))
    its.append(mcq("Which step solves " + render("x / 5 = 6") + " and keeps both sides equal?",
                   "Multiply both sides by 5",
                   ["Divide both sides by 5", "Multiply one side by 5", "Subtract 5 from both sides"],
                   "Multiplying undoes dividing. <b>Multiply both sides by 5</b>: " + V("x") + " = 6 × 5 = 30. "
                   "Check: 30 ÷ 5 = 6. Dividing by 5 again is the same operation."))
    # D. which equation has this solution
    for sol, right, wr in [
        (6, "7x = 42", ["x + 6 = 18", "x - 6 = 12", "6x = 6"]),
        (12, "x - 4 = 8", ["4x = 8", "x + 4 = 8", "x / 4 = 8"]),
        (40, "x / 5 = 8", ["8x = 40", "x - 5 = 8", "x + 5 = 40"]),
    ]:
        assert holds(right, sol) and not any(holds(w, sol) for w in wr)
        chk = {6: "7 × 6 = 42", 12: "12 − 4 = 8", 40: "40 ÷ 5 = 8"}[sol]
        e = "Substitute %s = %s into each equation. %s, so <b>%s</b> is true. " % (V("x"), n(sol), chk, render(right))
        if sol == 40:
            e += "8" + V("x") + " = 40 has the solution 5, not 40: it mixes up the two numbers."
        elif sol == 12:
            e += V("x") + " ÷ 4 = 8 has the solution 32."
        else:
            e += "6" + V("x") + " = 6 has the solution 1."
        its.append(mcq("Which equation has the solution %s = %s?" % (V("x"), n(sol)), render(right),
                       [render(w) for w in wr], e))
    # E. meaning of 5x
    its.append(mcq("What does 5" + V("x") + " mean?", "5 × " + V("x"),
                   ["5 + " + V("x"), V("x") + " ÷ 5", V("x") + " − 5"],
                   "A number written right before a letter means multiply. 5" + V("x") + " means <b>5 × "
                   + V("x") + "</b>, or 5 equal blocks of " + V("x") + ". If " + V("x") + " = 7, then 5" + V("x") + " = 35."))
    # F. checking finds the mistake
    nm, he, his, him = P.next()
    its.append(mcq("%s solves %s and gets %s = 42. Which check shows that %s answer is wrong?"
                   % (nm, render("x + 12 = 30"), V("x"), his),
                   "42 + 12 = 54, not 30",
                   ["42 − 12 = 30", "30 + 12 = 42", "42 ÷ 12 = 30"],
                   "To check, put the answer back into the equation: 42 + 12 = 54, and 54 is not 30. "
                   "%s added 12 instead of subtracting it. The right answer is 30 − 12 = 18." % nm))
    assert not holds("x + 12 = 30", 42) and holds("x + 12 = 30", 18)
    assert len(its) == 20, len(its)
    return {"title": "Pan balances and the equal sign", "items": its}


# ============================================================ set 2: x + 12 = 30 and x − 9 = 20
def set_add_sub(P):
    its = []
    for s, pic in [
        ("x + 12 = 30", None),
        ("x + 27 = 64", None),
        ("45 + n = 91", None),
        ("y + 138 = 405", ("bar", 405, "y", 138)),
        ("x - 15 = 40", None),
        ("m - 48 = 75", None),
        ("a - 250 = 380", ("bar", "a", 380, 250)),
        ("84 = x + 29", None),
        ("120 = p - 65", None),
        ("90 - x = 34", None),
        ("500 - y = 215", None),
        ("1500 + x = 4200", None),
        ("x + 2750 = 6000", None),
        ("k - 1800 = 3600", None),
        ("x + 12500 = 30000", None),
        ("n - 25000 = 48000", None),
        ("x + 45000 = 120000", None),
        ("d + 2500000 = 7000000", None),
    ]:
        p = bar_svg(*pic[1:]) if pic else None
        its.append(solve_item(s, pic=p))
    nm, he, his, him = P.next()
    its.append(mcq("%s solves %s and gets %s = 15. What did %s do wrong?" % (nm, render("x - 25 = 40"), V("x"), he),
                   cap(he) + " subtracted instead of adding",
                   [cap(he) + " added instead of subtracting", cap(he) + " forgot to carry", "Nothing, 15 is right"],
                   "Check: 15 − 25 does not give 40. %s used the same operation, <b>subtraction, instead of the inverse</b>. "
                   "Add 25 to both sides: %s = 40 + 25 = 65. Check: 65 − 25 = 40." % (cap(he), V("x"))))
    its.append(mcq("What is the first step to solve " + render("x + 38 = 95") + "?",
                   "Subtract 38 from both sides",
                   ["Add 38 to both sides", "Subtract 95 from both sides", "Divide both sides by 38"],
                   "Subtraction undoes addition. <b>Subtract 38 from both sides</b>: " + V("x") + " = 95 − 38 = 57. "
                   "Check: 57 + 38 = 95."))
    assert solve_eq("x + 38 = 95") == 57
    assert len(its) == 20, len(its)
    return {"title": "Solve x + 12 = 30 and x − 9 = 20", "items": its}


# ============================================================ set 3: 5x = 35
def set_mul(P):
    its = []
    for s, pic in [
        ("5x = 35", (5, "x", 35)),
        ("3n = 27", (3, "n", 27)),
        ("8y = 56", None),
        ("9m = 72", None),
        ("6x = 54", None),
        ("7k = 84", None),
        ("12x = 96", None),
        ("11p = 132", None),
        ("63 = 7x", None),
        ("120 = 8n", None),
        ("15x = 180", None),
        ("20x = 1800", None),
        ("25t = 1000", None),
        ("100x = 4500", None),
        ("1000x = 36000", None),
        ("40x = 2800", None),
        ("x * 6 = 90", None),
        ("4 * w = 52", None),
    ]:
        p = parts_svg(*pic) if pic else None
        its.append(solve_item(s, pic=p))
    nm, he, his, him = P.next()
    its.append(mcq("%s solves %s and writes %s = 36. What did %s do?" % (nm, render("6x = 42"), V("x"), he),
                   cap(he) + " subtracted 6 instead of dividing by 6",
                   [cap(he) + " multiplied 42 by 6", cap(he) + " added 6 to 42", "Nothing, 36 is right"],
                   "42 − 6 = 36, so %s <b>subtracted 6 instead of dividing</b>. 6%s means 6 × %s, and division undoes "
                   "multiplication: %s = 42 ÷ 6 = 7. Check: 6 × 7 = 42." % (he, V("x"), V("x"), V("x"))))
    its.append(mcq("What is the first step to solve " + render("9x = 63") + "?",
                   "Divide both sides by 9",
                   ["Subtract 9 from both sides", "Multiply both sides by 9", "Add 9 to both sides"],
                   "9" + V("x") + " means 9 × " + V("x") + ". Division undoes multiplication, so <b>divide both sides by 9</b>: "
                   + V("x") + " = 63 ÷ 9 = 7. Subtracting 9 would undo + 9, not × 9."))
    assert solve_eq("6x = 42") == 7 and solve_eq("9x = 63") == 7
    assert len(its) == 20, len(its)
    return {"title": "Solve 5x = 35", "items": its}


# ============================================================ set 4: x ÷ 4 = 8
def set_div(P):
    its = []
    for s, pic in [
        ("x / 4 = 8", (4, 8, "x")),
        ("n / 3 = 9", None),
        ("y / 6 = 7", None),
        ("m / 5 = 12", (5, 12, "m")),
        ("x / 8 = 9", None),
        ("k / 12 = 7", None),
        ("x / 10 = 45", None),
        ("p / 25 = 4", None),
        ("x / 100 = 36", None),
        ("x / 1000 = 250", None),
        ("15 = t / 6", None),
        ("9 = x / 9", None),
        ("48 / x = 6", None),
        ("72 / n = 9", None),
        ("100 / x = 4", None),
        ("x / 20 = 15", None),
        ("x / 50 = 30", None),
        ("360 / a = 12", None),
    ]:
        p = parts_svg(*pic) if pic else None
        its.append(solve_item(s, pic=p))
    nm, he, his, him = P.next()
    its.append(mcq("%s solves %s and gets %s = 2. What did %s do wrong?" % (nm, render("n / 6 = 12"), V("n"), he),
                   cap(he) + " divided instead of multiplying",
                   [cap(he) + " multiplied instead of dividing", cap(he) + " subtracted instead of adding",
                    "Nothing, 2 is right"],
                   "Check: 2 ÷ 6 is not 12. %s used the same operation, <b>division, instead of the inverse</b>. "
                   "Multiply both sides by 6: %s = 12 × 6 = 72. Check: 72 ÷ 6 = 12." % (cap(he), V("n"))))
    its.append(mcq("What is the first step to solve " + render("x / 9 = 4") + "?",
                   "Multiply both sides by 9",
                   ["Divide both sides by 9", "Subtract 9 from both sides", "Add 9 to both sides"],
                   "Multiplication undoes division. <b>Multiply both sides by 9</b>: " + V("x") + " = 4 × 9 = 36. "
                   "Check: 36 ÷ 9 = 4."))
    assert solve_eq("n / 6 = 12") == 72 and solve_eq("x / 9 = 4") == 36
    assert len(its) == 20, len(its)
    return {"title": "Solve x ÷ 4 = 8", "items": its}


# ============================================================ set 5: write and solve from stories
def set_words(P):
    its = []

    def match(q, right, wr, e):
        x = solve_eq(right)
        for w in wr:
            assert not holds(w, x), w
        its.append(mcq(q, render(right), [render(w) for w in wr], e))

    def story(q, s, unit=None, pic=None, wr=None):
        x, steps, auto = analyse(s)
        wr = wr or auto
        its.append(mcq_n(q + (fig(pic) if pic else ""), x, wr, "Equation: %s. %s" % (render(s), steps), unit=unit))

    W = "Which equation matches?"
    # write an equation
    match("A Grade 6 class has raised $385 for the Terry Fox Run. Its goal is $1000. Let %s be the money it still needs. %s"
          % (V("m"), W),
          "385 + m = 1000", ["m = 385 + 1000", "m - 385 = 1000", "385m = 1000"],
          "What they have plus what they still need makes the goal: <b>%s</b>. Then %s = 1000 − 385 = $615."
          % (render("385 + m = 1000"), V("m")))
    match("4 SkyTrain cars carry 520 people. Each car carries the same number of people, %s. %s" % (V("p"), W),
          "4p = 520", ["p + 4 = 520", "p / 4 = 520", "520p = 4"],
          "4 equal groups of %s make 520: <b>%s</b>. Equal groups mean ×, not +. Then %s = 520 ÷ 4 = 130."
          % (V("p"), render("4p = 520"), V("p")))
    match("A BC Ferries boat has %s cars on board. 85 cars drive off and 240 are still on board. %s" % (V("c"), W),
          "c - 85 = 240", ["c + 85 = 240", "85 - c = 240", "240 - c = 85"],
          "Start with %s, take away 85, and 240 are left: <b>%s</b>. Then %s = 240 + 85 = 325."
          % (V("c"), render("c - 85 = 240"), V("c")))
    match("A hiking club in Kamloops splits into 8 equal groups with 12 hikers in each group. Let %s be the number of "
          "hikers. %s" % (V("h"), W),
          "h / 8 = 12", ["8h = 12", "h - 8 = 12", "12 / h = 8"],
          "Start with %s hikers and share them into 8 groups to get 12 in each: <b>%s</b>. Then %s = 12 × 8 = 96."
          % (V("h"), render("h / 8 = 12"), V("h")))
    match("Which equation means “a number divided by 7 is 15”?",
          "n / 7 = 15", ["7 / n = 15", "7n = 15", "n - 7 = 15"],
          "Start with the number %s and divide it by 7: <b>%s</b>. Then %s = 15 × 7 = 105. 7 ÷ %s starts with 7, "
          "not with the number." % (V("n"), render("n / 7 = 15"), V("n"), V("n")))
    match("Which equation means “6 times a number is 84”?",
          "6n = 84", ["6 + n = 84", "n / 6 = 84", "84n = 6"],
          "“6 times a number” is 6%s, and “is 84” is = 84: <b>%s</b>. Then %s = 84 ÷ 6 = 14."
          % (V("n"), render("6n = 84"), V("n")))
    its.append(mcq("Which story matches " + render("3x = 45") + "?",
                   "3 tickets cost the same. They cost $45 in all.",
                   ["A ticket costs $3. Then the price goes up by $45.",
                    "3 friends each have $45.",
                    "$45 is shared and $3 is left over."],
                   "3%s means 3 equal groups of %s. 3 tickets at the same price %s make $45: <b>3%s = 45</b>, "
                   "so each ticket costs 45 ÷ 3 = $15." % (V("x"), V("x"), V("x"), V("x"))))
    its.append(mcq("Which story matches " + render("x - 120 = 380") + "?",
                   "Some salmon swim up a creek. 120 are caught and 380 are left.",
                   ["120 salmon swim up a creek and then 380 more come.",
                    "380 salmon swim up a creek and 120 are caught.",
                    "120 salmon are shared among 380 bears."],
                   "%s is the number at the start. Take away 120 and 380 are left: <b>%s</b>. Then %s = 380 + 120 = 500. "
                   "The story “380 salmon … 120 are caught” starts with 380, so it matches 380 − 120 = %s."
                   % (V("x"), render("x - 120 = 380"), V("x"), V("x"))))
    # solve
    nm, he, his, him = P.next()
    story("%s’s family is driving about 780 km from Vancouver to Prince George. They have driven 495 km. "
          "How many more kilometres do they have to drive?" % nm,
          "495 + d = 780", unit=("km", "km"), pic=bar_svg(780, 495, "d"))
    story("A ski hill sells the same number of lift tickets each hour for 8 hours. It sells 2400 tickets in all. "
          "How many tickets does it sell each hour?",
          "8t = 2400", unit=("ticket", "tickets"))
    nm, he, his, him = P.next()
    story("%s saves the same amount each week for 12 weeks. %s saves $156 in all. How much does %s save each week?"
          % (nm, cap(he), he), "12s = 156", unit="$")
    nm, he, his, him = P.next()
    story("%s shares some Okanagan cherries equally into 6 bags. Each bag has 25 cherries. How many cherries did %s "
          "start with?" % (nm, he), "c / 6 = 25", unit=("cherry", "cherries"))
    story("A stadium has 54000 seats. 38750 people are in their seats. How many seats are empty?".replace(
        "54000", n(54000)).replace("38750", n(38750)), "38750 + e = 54000", unit=("seat", "seats"))
    story("A fish counter on a creek in the Fraser Valley counts some salmon. After 1450 more swim by, the total is 6200. "
          "How many salmon had it counted before?", "s + 1450 = 6200", unit=("salmon", "salmon"))
    story("24 students raise the same amount for the Terry Fox Run. Together they raise $720. How much does each "
          "student raise?", "24r = 720", unit="$")
    story("A school is going on a field trip to the Royal BC Museum in Victoria. Each bus holds 48 students. "
          "336 students are going, and every bus is full. How many buses do they need?",
          "48b = 336", unit=("bus", "buses"))
    nm, he, his, him = P.next()
    story("%s cuts a 200 cm cedar board into 8 equal pieces. How long is each piece?" % nm,
          "8p = 200", unit=("cm", "cm"), pic=parts_svg(8, "p", 200))
    story("The students in a Grade 6 class form 4 equal lacrosse teams with 7 players on each team. "
          "How many students are in the class?", "s / 4 = 7", unit=("student", "students"),
          wr=[(11, "adding 4 instead of multiplying"), (32, "4 × 8, the wrong fact"), (24, "4 × 6, the wrong fact")])
    nm, he, his, him = P.next()
    story("%s spends $46 at the PNE in Vancouver and has $29 left. How much money did %s have at the start?" % (nm, he),
          "m - 46 = 29", unit="$")
    story("A school district plans to plant 10000 tree seedlings. Students have planted 6475 so far. "
          "How many more do they need to plant?".replace("10000", n(10000)),
          "6475 + t = 10000", unit=("seedling", "seedlings"))
    assert len(its) == 20, len(its)
    return {"title": "Write and solve equations from stories", "items": its}


# ============================================================ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    x = V("x")
    return (
        "<h2>An equation is a balance</h2>"
        "<p>An <b>equation</b> says two sides are equal, like a level pan balance. A letter such as " + x +
        " stands for the unknown number. To solve the equation, find the value of " + x + " that makes it true.</p>"
        "<figure class='sn-fig'>" + scale_svg(["x", "12"], ["30"]) +
        "<figcaption>" + render("x + 12 = 30") + ". Take 12 off both pans: " + x + " = 18.</figcaption></figure>"
        "<h2>Use the inverse operation</h2>"
        "<p>Undo what is done to " + x + ". Use the <b>inverse</b> operation, and do it to <b>both sides</b>. "
        "Then put your answer back in to check.</p>" +
        table(["Equation", "Undo it with", "Do this", "Answer"], [
            [render("x + 12 = 30"), M + " 12 on both sides", "30 " + M + " 12", x + " = 18"],
            [render("x - 9 = 20"), "+ 9 on both sides", "20 + 9", x + " = 29"],
            [render("5x = 35"), "÷ 5 on both sides", "35 ÷ 5", x + " = 7"],
            [render("x / 4 = 8"), "× 4 on both sides", "8 × 4", x + " = 32"],
        ]) +
        "<p>5" + x + " means 5 × " + x + ". A number written right before a letter means multiply.</p>"
        "<figure class='sn-fig'>" + parts_svg(5, "x", 35) +
        "<figcaption>5 equal parts make 35: 5" + x + " = 35, so " + x + " = 35 ÷ 5 = 7.</figcaption></figure>" +
        ex("Example", render("x / 4 = 8"),
           x + " is the number you start with. Multiply both sides by 4: " + x + " = 8 × 4 = 32. Check: 32 ÷ 4 = 8.",
           x + " = 32") +
        ex("Example", render("x + 12500 = 30000"),
           "Subtract " + n(12500) + " from both sides: " + x + " = " + n(30000) + " − " + n(12500) + " = " + n(17500)
           + ". Check: " + n(17500) + " + " + n(12500) + " = " + n(30000) + ".", x + " = " + n(17500)) +
        "<h2>Write an equation from a story</h2>"
        "<p>Choose a letter for the number you do not know. Joining is +, taking away is " + M + ", "
        "equal groups are ×, and sharing equally is ÷. Then solve and check.</p>"
        "<figure class='sn-fig'>" + bar_svg(1000, 385, "m") +
        "<figcaption>$385 raised, goal $1000: 385 + " + V("m") + " = 1000, so " + V("m") + " = 615.</figcaption></figure>" +
        ex("Example", "4 SkyTrain cars carry 520 people. Each car carries the same number. How many in each car?",
           "Equation: 4" + V("p") + " = 520. Divide both sides by 4: " + V("p") + " = 130. Check: 4 × 130 = 520.",
           "130 people") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            [render("x + 12 = 30") + ", so " + x + " = 42 (30 + 12)", "Use the inverse: 30 " + M + " 12 = 18"],
            [render("x - 9 = 20") + ", so " + x + " = 11 (20 " + M + " 9)", "Use the inverse: 20 + 9 = 29"],
            [render("5x = 35") + ", so " + x + " = 175 (35 × 5)", "Use the inverse: 35 ÷ 5 = 7"],
            [render("5x = 35") + ", so " + x + " = 30 (35 " + M + " 5)", "5" + x + " means 5 × " + x + ", so divide"],
            [render("x / 4 = 8") + ", so " + x + " = 2 (8 ÷ 4)", "Use the inverse: 8 × 4 = 32"],
            ["Changing only one side", "Do the same to both sides to keep the balance level"],
        ])
    )


FAQ = [
    {"q": "What are one-step equations in Grade 6 math in BC?",
     "a": "They are equations like x + 12 = 30, 5x = 35 or x ÷ 4 = 8 that take one step to solve. The BC Grade 6 Patterning standard uses whole-number coefficients and whole-number solutions."},
    {"q": "How do you solve 5x = 35?",
     "a": "5x means 5 × x, so use the inverse operation and divide both sides by 5: x = 35 ÷ 5 = 7. Check by putting 7 back in: 5 × 7 = 35."},
    {"q": "Why do you do the same thing to both sides of an equation?",
     "a": "An equation is like a level pan balance. If you change only one side it tips, so whatever you do to one side you must do to the other."},
    {"q": "What is the most common mistake with one-step equations?",
     "a": "Using the same operation instead of the inverse, for example adding 12 to solve x + 12 = 30. Checking the answer in the original equation catches this mistake."},
]


def gen_unit():
    rnd = random.Random(56808)
    P = People(rnd)
    sets = [set_balance(P), set_add_sub(P), set_mul(P), set_div(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(plain(c) for c in it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-6", "slug": "one-step-equations", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 6 One-Step Equations",
        "seo_title": "Grade 6 One-Step Equations Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "One-Step Equations",
        "domain": "Patterning",
        "standard_code": "Grade 6: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/6/core",
        "standard_text": "One-step equations with whole-number coefficients and solutions",
        "meta_desc": "Free Grade 6 math worksheets on one-step equations for the BC curriculum: pan balances, solving x + 12 = 30, 5x = 35 and x ÷ 4 = 8 with inverse operations, and writing and solving equations from stories. 100 questions with an answer key.",
        "key_big": "Use the inverse operation on both sides: subtraction undoes addition, and division undoes multiplication.",
        "key_sub": "5x = 35, so x = 35 ÷ 5 = 7. x ÷ 4 = 8, so x = 8 × 4 = 32. Then check by putting the answer back in.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "bar model|pan balance|equal parts bar")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
