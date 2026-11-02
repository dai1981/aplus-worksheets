# -*- coding: utf-8 -*-
"""
British Columbia Grade 7 Math: Two-Step Equations
(BC Mathematics Curriculum, Grade 7 — Patterning: two-step equations with whole-number coefficients,
constants, and solutions)
  python3 tools/gen_cabc_math_g7_two_step_equations.py
Pan balances and undoing in reverse order, equations like 3x + 4 = 19, equations like x/4 + 2 = 7 and
2x − 5 = 11, writing an equation from words or a model (balance, bar, number machine), and word problems
in BC contexts (a phone plan, a bike rental near Stanley Park, a cabin in Whistler, a kayak tour in Victoria).
Wrong choices come from real mistakes: dividing before subtracting (3x + 4 = 19 -> 19 ÷ 3 − 4), using the same
operation instead of the inverse (adding 4, or dividing x/4 by 4 again), forgetting the second step,
multiplying instead of dividing, counting 3x as x + 3, and mixing up the coefficient and the constant.
Every answer is checked in code. HTML attributes use single quotes. Canadian English, real minus sign −.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-7")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
GREY = "#e4e4e4"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
M = "−"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia", "Ji-woo"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]


# ------------------------------------------------------------ equations in a mini syntax
# "3n + 4 = 19", "n/4 + 2 = 7", "4 + 3n = 25", "41 = 5n + 6", "n/2 = 15 + 6"; tokens are separated by spaces.
def frac(top, bot):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (top, bot)


def V(v):
    return "<i>%s</i>" % v


def render(s):
    out = []
    for t in s.split(" "):
        m = re.match(r"^(\d*)([a-z])/(\d+)$", t)
        if m:
            out.append(frac(m.group(1) + V(m.group(2)), m.group(3)))
        elif re.match(r"^\d+[a-z]$", t):
            out.append(t[:-1] + V(t[-1]))
        elif re.match(r"^[a-z]$", t):
            out.append(V(t))
        else:
            out.append({"-": M, "*": "×", "/": "÷"}.get(t, t))
    return " ".join(out)


def ev(side, x):
    s = []
    for t in side.split(" "):
        m = re.match(r"^(\d*)([a-z])/(\d+)$", t)
        if m:
            s.append("(%sX/F(%s))" % ((m.group(1) + "*") if m.group(1) else "", m.group(3)))
        elif re.match(r"^\d+[a-z]$", t):
            s.append("(%s*X)" % t[:-1])
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


def solve_text(s):
    """Whole-number solution of a linear equation in the mini syntax (searched, then checked)."""
    sols = [x for x in range(0, 2000) if holds(s, x)]
    assert len(sols) == 1, (s, sols)
    return sols[0]


def whole(v):
    v = F(v)
    return int(v) if v.denominator == 1 and v > 0 else None


# ------------------------------------------------------------ two-step equations a·x ± b = c and x/a ± b = c
def eqs(form, a, op, b, c, v="x"):
    t = ("%d%s" % (a, v) if a != 1 else v) if form == "m" else "%s/%d" % (v, a)
    return "%s %s %d = %d" % (t, op, b, c)


def solve2(form, a, op, b, c):
    mid = c - b if op == "+" else c + b
    x = F(mid, a) if form == "m" else mid * a
    assert x.denominator == 1 if isinstance(x, F) else True
    x = int(x)
    assert x > 0 and holds(eqs(form, a, op, b, c), x), (form, a, op, b, c)
    return x


def calc(form, a, op, b, x):
    c = (a * x if form == "m" else x // a) + (b if op == "+" else -b)
    head = "%d × %d" % (a, x) if form == "m" else "%d ÷ %d" % (x, a)
    return "%s %s %d = %d" % (head, "+" if op == "+" else M, b, c)


def steps(form, a, op, b, c, v="x"):
    x = solve2(form, a, op, b, c)
    mid = c - b if op == "+" else c + b
    undo = ("Subtract %d from both sides" % b) if op == "+" else ("Add %d to both sides" % b)
    t = render(("%d%s" % (a, v)) if form == "m" else "%s/%d" % (v, a))
    if form == "m":
        last = "Divide both sides by %d: %s = %d ÷ %d = <b>%d</b>" % (a, V(v), mid, a, x)
    else:
        last = "Multiply both sides by %d: %s = %d × %d = <b>%d</b>" % (a, V(v), mid, a, x)
    return "%s: %s = %d. %s. Check: %s." % (undo, t, mid, last, calc(form, a, op, b, x))


def wrongs(form, a, op, b, c):
    """(value, why) from real mistakes, most common first."""
    if form == "m" and op == "+":
        return [(F(c, a) - b, "dividing before subtracting %d" % b), (F(c + b, a), "adding %d instead of subtracting it" % b),
                (c - b, "forgetting to divide by %d" % a), ((c - b) * a, "multiplying by %d instead of dividing" % a)]
    if form == "m":
        return [(F(c, a) + b, "dividing before adding %d" % b), (F(c - b, a), "subtracting %d instead of adding it" % b),
                (c + b, "forgetting to divide by %d" % a), ((c + b) * a, "multiplying by %d instead of dividing" % a)]
    if op == "+":
        return [(a * c - b, "multiplying by %d before subtracting %d" % (a, b)), (F(c - b, a), "dividing by %d instead of multiplying" % a),
                ((c + b) * a, "adding %d instead of subtracting it" % b), (c - b, "forgetting to multiply by %d" % a)]
    return [(a * c + b, "multiplying by %d before adding %d" % (a, b)), (F(c + b, a), "dividing by %d instead of multiplying" % a),
            ((c - b) * a, "subtracting %d instead of adding it" % b), (c + b, "forgetting to multiply by %d" % a)]


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
        return str(v)
    if unit == "$":
        return "$" + str(v)
    sing, plur = unit
    return "%d %s" % (v, sing if v == 1 else plur)


def mcq_n(q, x, cands, e, unit=None, notes=True, limit=None):
    """cands: (value, why) pairs or plain values. Only whole, positive, new values are used; the reasons
    for the wrong answers used are added to the explanation."""
    used, add = {x}, []
    for c in cands:
        val, why = c if isinstance(c, tuple) else (c, None)
        w = whole(val)
        if w is None or w in used or (limit and w > limit):
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


def scale_svg(left, right, label):
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
                s.append(text(x + iw / 2, top + 24, t))
            x += iw + gap
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='6' fill='%s'/>" % (c - w / 2, py, w, INK))
        s.append("<rect x='%.1f' y='%d' width='4' height='18' fill='%s'/>" % (c - 2, py + 6, INK))
    by = py + 24
    s.append("<rect x='%.1f' y='%d' width='%.1f' height='6' fill='%s'/>" % (cl - 2, by, cr - cl + 4, INK))
    s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (mid, by + 6, mid - 22, by + 40, mid + 22, by + 40, GREEN))
    s.append("<rect x='%.1f' y='%d' width='80' height='5' fill='%s'/>" % (mid - 40, by + 40, INK))
    return svg_wrap(cr + wr / 2 + 8, by + 47, "".join(s), "pan balance: " + label)


def bal(k, b, c, v="x"):
    return scale_svg([v] * k + [str(b)], [str(c)], "%d blocks %s and %d balance %d" % (k, v, b, c))


def tape_svg(k, b, total, x, v="x"):
    """Bar model drawn to scale: k parts of v and one part b make total (k·x + b = total)."""
    assert k * x + b == total
    W, x0, y, h = 300, 8, 40, 36
    wx = W * x / total
    wb = W - k * wx
    assert wx >= 30 and wb >= 26, (k, b, total, x)
    s = []
    for i in range(k):
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (x0 + i * wx, y, wx, h, FILL, GREEN))
        s.append(text(x0 + i * wx + wx / 2, y + 25, v, 18, col=RED, italic=True))
    s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
             % (x0 + k * wx, y, wb, h, GREY, GREEN))
    s.append(text(x0 + k * wx + wb / 2, y + 25, str(b)))
    s.append("<path d='M%d %d v-8 H%d v8' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y - 4, x0 + W, INK))
    s.append(text(x0 + W / 2, y - 16, str(total)))
    return svg_wrap(W + 16, y + h + 6, "".join(s), "bar model: %d parts %s and %d make %d" % (k, v, b, total))


def flow_svg(start, ops, end, undo=False):
    """Number machine: start -> op -> op -> end. With undo, a second row shows the inverse operations
    from right to left."""
    bw, ow, aw, h = 50, 62, 34, 38
    xs, x = [], 8
    widths = [bw] + [ow] * len(ops) + [bw]
    for w in widths:
        xs.append(x)
        x += w + aw
    W = x - aw + 8
    s = []

    def row(y, labels, back):
        for i, (bx, w, t) in enumerate(zip(xs, widths, labels)):
            if i == 0:
                fill, col, it = FILL, RED, t.isalpha()
            elif i == len(widths) - 1:
                fill, col, it = FILL, INK, False
            else:
                fill, col, it = "#fff", (RED if back else INK), False
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (bx, y, w, h, 6 if 0 < i < len(widths) - 1 else 2, fill, GREEN if not back else RED, ))
            s.append(text(bx + w / 2, y + 26, t, 18, col=col, italic=it))
        for i in range(len(widths) - 1):
            x1, x2 = xs[i] + widths[i] + 4, xs[i + 1] - 4
            ym = y + h / 2
            if back:
                s.append("<path d='M%d %.1f H%d' stroke='%s' stroke-width='2.5'/>" % (x1 + 8, ym, x2, RED))
                s.append("<path d='M%d %.1f l9 -6 v12 Z' fill='%s'/>" % (x1, ym, RED))
            else:
                s.append("<path d='M%d %.1f H%d' stroke='%s' stroke-width='2.5'/>" % (x1, ym, x2 - 8, INK))
                s.append("<path d='M%d %.1f l-9 -6 v12 Z' fill='%s'/>" % (x2, ym, INK))
    row(8, [start] + ops + [end], False)
    H = 8 + h + 8
    if undo:
        inv = {"×": "÷", "÷": "×", "+": M, M: "+"}
        row(8 + h + 18, [start] + [inv[o[0]] + o[1:] for o in ops] + [end], True)
        H += h + 18
    lab = "number machine: %s, %s, gives %s" % (start, ", then ".join(ops), end)
    if undo:
        lab += ", and the inverse operations back"
    return svg_wrap(W, H, "".join(s), lab)


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ============================================================ set 1: balance models and undoing in reverse order
def set_balance(P):
    its = []
    # A. pan balances: what is x
    for k, b, c in [(2, 3, 11), (3, 4, 25), (4, 6, 30), (5, 2, 37)]:
        x = solve2("m", k, "+", b, c)
        e = ("The balance shows %s. Take %d off both pans: %s = %d. %d equal blocks make %d, so each block is "
             "%d ÷ %d = <b>%d</b>. Check: %s." % (render(eqs("m", k, "+", b, c)), b, render("%dx" % k), c - b, k, c - b,
                                                   c - b, k, x, calc("m", k, "+", b, x)))
        its.append(mcq_n("The pan balance is level. Each block has the same mass, %s. What is %s?" % (V("x"), V("x"))
                         + fig(bal(k, b, c)), x, wrongs("m", k, "+", b, c) + near(x), e))
    # B. which equation matches the balance
    for k, b, c, wr in [(3, 5, 20, ["x + 3 + 5 = 20", "5x + 3 = 20", "3x = 20 + 5"]),
                        (4, 3, 27, ["x + 4 + 3 = 27", "3x + 4 = 27", "4x = 27 + 3"])]:
        right = eqs("m", k, "+", b, c)
        x = solve_text(right)
        assert not any(holds(w, x) for w in wr)
        e = ("The left pan has %d blocks %s and a %d. That is %s + %d, written %s + %d. So <b>%s</b>. "
             "%s + %d + %d would mean only one block." % (k, V("x"), b, " + ".join([V("x")] * k), b, render("%dx" % k), b,
                                                         render(right), V("x"), k, b))
        its.append(mcq("The pans balance. Which equation matches?" + fig(bal(k, b, c)),
                       render(right), [render(w) for w in wr], e))
    # C. first move on a balance
    its.append(mcq("The balance shows " + render("3x + 5 = 20") + ". You take 5 off both pans. Which equation shows "
                   "what is left?" + fig(bal(3, 5, 20)),
                   render("3x = 15"), [render("3x = 20"), render("3x = 25"), render("x = 15")],
                   "Take 5 off the left pan and 5 off the right pan. The pans still balance: 3 blocks on the left, "
                   "20 − 5 = 15 on the right, so <b>" + render("3x = 15") + "</b>. Then " + V("x") + " = 15 ÷ 3 = 5. "
                   "Taking 5 off only one pan makes the balance tip."))
    its.append(mcq("You solve " + render("2x + 7 = 19") + " on a balance. After taking 7 off both pans, it shows "
                   + render("2x = 12") + ". What should you do next?",
                   "Divide both sides by 2",
                   ["Subtract 2 from both sides", "Multiply both sides by 2", "Add 7 to both sides"],
                   "2" + V("x") + " means 2 × " + V("x") + ". Division undoes multiplication, so <b>divide both sides by 2</b>: "
                   + V("x") + " = 12 ÷ 2 = 6. Check: 2 × 6 + 7 = 19. Subtracting 2 would undo + 2, not × 2."))
    # D. best first step
    for s, right, wr, why in [
        ("3x + 4 = 19", "Subtract 4 from both sides", ["Divide both sides by 3", "Add 4 to both sides", "Subtract 3 from both sides"],
         "3%s + 4 means “multiply by 3, then add 4”. Undo the last step first: <b>subtract 4 from both sides</b> to get "
         "3%s = 15, then divide by 3: %s = 5. Dividing 19 by 3 first does not give a whole number." % (V("x"), V("x"), V("x"))),
        ("5n - 6 = 24", "Add 6 to both sides", ["Divide both sides by 5", "Subtract 6 from both sides", "Add 5 to both sides"],
         "5%s − 6 means “multiply by 5, then subtract 6”. Undo the − 6 first: <b>add 6 to both sides</b> to get 5%s = 30, "
         "then divide by 5: %s = 6. Subtracting 6 is the same operation, not the inverse." % (V("n"), V("n"), V("n"))),
        ("y/3 + 2 = 8", "Subtract 2 from both sides", ["Divide both sides by 3", "Add 2 to both sides", "Subtract 3 from both sides"],
         "%s means “divide by 3, then add 2”. Undo the + 2 first: <b>subtract 2 from both sides</b> to get %s = 6, then "
         "multiply by 3: %s = 18." % (render("y/3 + 2"), render("y/3"), V("y"))),
        ("m/4 - 1 = 5", "Add 1 to both sides", ["Subtract 1 from both sides", "Divide both sides by 4", "Add 4 to both sides"],
         "%s means “divide by 4, then subtract 1”. Undo the − 1 first: <b>add 1 to both sides</b> to get %s = 6, then "
         "multiply by 4: %s = 24." % (render("m/4 - 1"), render("m/4"), V("m"))),
    ]:
        x = solve_text(s)
        assert x in (5, 6, 18, 24)
        its.append(mcq("What is the best first step to solve %s?" % render(s), right, wr, why))
    # E. reverse order
    its.append(mcq("To make 4%s + 7, start with %s, multiply by 4, then add 7. Which order undoes it?" % (V("x"), V("x")),
                   "Subtract 7, then divide by 4",
                   ["Divide by 4, then subtract 7", "Add 7, then multiply by 4", "Subtract 4, then divide by 7"],
                   "Undo the steps in <b>reverse order</b>, like taking off shoes before socks. The last step was + 7, so "
                   "subtract 7 first. Then undo × 4 by dividing by 4."))
    its.append(mcq("To make %s − 3, start with %s, divide by 2, then subtract 3. Which order undoes it?" % (render("x/2"), V("x")),
                   "Add 3, then multiply by 2",
                   ["Multiply by 2, then add 3", "Subtract 3, then divide by 2", "Add 2, then multiply by 3"],
                   "Reverse order: the last step was − 3, so <b>add 3 first</b>. Then undo ÷ 2 by <b>multiplying by 2</b>. "
                   "Multiplying first would also double the 3."))
    # F. number machines
    for ops, a, op, b, c in [(["× 3", "+ 4"], 3, "+", 4, 25), (["× 2", M + " 5"], 2, "-", 5, 11),
                             (["÷ 4", "+ 2"], 4, "+", 2, 7), (["× 5", "+ 8"], 5, "+", 8, 43)]:
        form = "d" if ops[0][0] == "÷" else "m"
        x = solve2(form, a, op, b, c)
        nm, he, his, him = P.next()
        undo1 = ("subtract %d" % b) if op == "+" else ("add %d" % b)
        undo2 = ("divide by %d" % a) if form == "m" else ("multiply by %d" % a)
        mid = c - b if op == "+" else c + b
        q = ("%s thinks of a number. %s puts it through this number machine and gets %d. What was %s number?"
             % (nm, cap(he), c, his)) + fig(flow_svg("?", ops, str(c)))
        e = ("Work backwards from %d in reverse order. First %s: %d. Then %s: <b>%d</b>. Check: %s."
             % (c, undo1, mid, undo2, x, calc(form, a, op, b, x)))
        its.append(mcq_n(q, x, wrongs(form, a, op, b, c) + near(x), e))
    # G. dividing first, and checking a solution
    nm, he, his, him = P.next()
    its.append(mcq("%s solves %s. %s divides first: %s, so %s = 4. What should %s do instead?"
                   % (nm, render("2x + 6 = 20"), cap(he), "20 ÷ 2 = 10 and 10 − 6 = 4", V("x"), he),
                   "Subtract 6 first, then divide by 2",
                   ["Add 6 first, then divide by 2", "Divide by 6 first", "Nothing, 4 is right"],
                   "Check 4: 2 × 4 + 6 = 14, not 20, so 4 is wrong. Dividing first only divided the 20, not the 6. "
                   "<b>Subtract 6 first</b>: 2%s = 14. Then divide by 2: %s = 7. Check: 2 × 7 + 6 = 20." % (V("x"), V("x"))))
    assert solve_text("2x + 6 = 20") == 7 and not holds("2x + 6 = 20", 4)
    its.append(mcq_n("Which value of %s makes %s true?" % (V("x"), render("4x - 5 = 19")), 6,
                     [(24, "forgetting to divide by 4"), (96, "multiplying by 4 instead of dividing"),
                      (14, "subtracting 5 instead of adding it")],
                     "Put each value in. 4 × 6 − 5 = 24 − 5 = 19, so <b>6</b> works. Or solve: add 5 to get 4%s = 24, then "
                     "divide by 4." % V("x")))
    assert holds("4x - 5 = 19", 6)
    assert len(its) == 20, len(its)
    return {"title": "Balance models and undoing in reverse order", "items": its}


# ============================================================ set 2: equations like 3x + 4 = 19
def set_plus(P):
    its = []
    T = [(2, 3, 11, "x"), (3, 4, 19, "x"), (2, 6, 20, "n"), (4, 1, 21, "y"), (5, 5, 40, "x"), (3, 9, 30, "k"),
         (6, 4, 46, "m"), (4, 8, 48, "x"), (7, 3, 59, "a"), (8, 6, 70, "n"), (9, 2, 83, "p"), (5, 15, 80, "t"),
         (6, 12, 90, "x"), (12, 5, 89, "y")]
    for a, b, c, v in T:
        s = eqs("m", a, "+", b, c, v)
        x = solve2("m", a, "+", b, c)
        its.append(mcq_n("Solve: %s" % render(s), x, wrongs("m", a, "+", b, c) + near(x), steps("m", a, "+", b, c, v)))
    # constant first, = first, larger numbers
    for s, a, b, c, v in [("4 + 3x = 25", 3, 4, 25, "x"), ("10 + 6n = 70", 6, 10, 70, "n")]:
        x = solve_text(s)
        e = ("%s is the same as %s. %s" % (render(s.split(" = ")[0]), render("%d%s + %d" % (a, v, b)), steps("m", a, "+", b, c, v)))
        its.append(mcq_n("Solve: %s" % render(s), x, wrongs("m", a, "+", b, c) + near(x), e))
    s = "41 = 5x + 6"
    x = solve_text(s)
    its.append(mcq_n("Solve: %s" % render(s), x, wrongs("m", 5, "+", 6, 41) + near(x),
                     "The = sign can come first. %s means %s. " % (render(s), render("5x + 6 = 41")) + steps("m", 5, "+", 6, 41)))
    s = "15x + 20 = 200"
    x = solve_text(s)
    its.append(mcq_n("Solve: %s" % render(s), x, wrongs("m", 15, "+", 20, 200) + near(x), steps("m", 15, "+", 20, 200)))
    # dividing-first mistake
    nm, he, his, him = P.next()
    assert solve_text("5x + 10 = 60") == 10
    its.append(mcq_n("%s solves %s. %s writes 60 ÷ 5 = 12, then 12 − 10 = 2. What is the correct value of %s?"
                     % (nm, render("5x + 10 = 60"), cap(he), V("x")), 10,
                     [(2, "dividing before subtracting 10"), (14, "adding 10 instead of subtracting it"),
                      (50, "forgetting to divide by 5")],
                     "%s divided first, so the 10 was not divided. Check 2: 5 × 2 + 10 = 20, not 60. Subtract 10 first: "
                     "5%s = 50. Then divide by 5: %s = <b>10</b>. Check: 5 × 10 + 10 = 60." % (nm, V("x"), V("x"))))
    # check a solution
    its.append(mcq_n("Which value of %s is a solution of %s?" % (V("n"), render("6n + 7 = 43")), 6,
                     [(36, "forgetting to divide by 6"), (7, "dividing 43 by 6 and rounding (6 × 7 + 7 = 49, not 43)"),
                      (216, "multiplying by 6 instead of dividing")],
                     "Put the value back in. 6 × 6 + 7 = 36 + 7 = 43, so <b>6</b> is a solution. Or solve: subtract 7 to get "
                     "6%s = 36, then divide by 6." % V("n")))
    assert holds("6n + 7 = 43", 6)
    assert len(its) == 20, len(its)
    return {"title": "Solve equations like 3x + 4 = 19", "items": its}


# ============================================================ set 3: x/4 + 2 = 7 and 2x − 5 = 11
def set_minus_div(P):
    its = []
    for a, b, c, v in [(2, 5, 11, "x"), (3, 2, 13, "n"), (4, 7, 21, "y"), (5, 6, 24, "x"), (6, 10, 32, "k"),
                       (3, 12, 15, "m"), (7, 4, 52, "x"), (8, 9, 63, "p")]:
        x = solve2("m", a, "-", b, c)
        its.append(mcq_n("Solve: %s" % render(eqs("m", a, "-", b, c, v)), x, wrongs("m", a, "-", b, c) + near(x),
                         steps("m", a, "-", b, c, v)))
    for a, op, b, c, v in [(4, "+", 2, 7, "x"), (2, "+", 3, 9, "n"), (3, "+", 5, 11, "y"), (5, "+", 4, 10, "x"),
                           (2, "-", 1, 6, "m"), (3, "-", 4, 5, "x"), (6, "-", 2, 4, "k"), (4, "-", 3, 7, "a")]:
        x = solve2("d", a, op, b, c)
        its.append(mcq_n("Solve: %s" % render(eqs("d", a, op, b, c, v)), x, wrongs("d", a, op, b, c) + near(x, a),
                         steps("d", a, op, b, c, v)))
    # = sign first
    s = "9 = 2x - 7"
    x = solve_text(s)
    its.append(mcq_n("Solve: %s" % render(s), x, wrongs("m", 2, "-", 7, 9) + near(x),
                     "The = sign can come first: %s means %s. " % (render(s), render("2x - 7 = 9")) + steps("m", 2, "-", 7, 9)))
    s = "20 = n/3 + 14"
    x = solve_text(s)
    its.append(mcq_n("Solve: %s" % render(s), x, wrongs("d", 3, "+", 14, 20) + near(x, 3),
                     "The = sign can come first: %s means %s. " % (render(s), render("n/3 + 14 = 20"))
                     + steps("d", 3, "+", 14, 20, "n")))
    # mistakes
    nm, he, his, him = P.next()
    assert solve_text("3x - 6 = 18") == 8
    its.append(mcq("%s solves %s. %s subtracts 6 from both sides and ends with %s = 4. What went wrong?"
                   % (nm, render("3x - 6 = 18"), cap(he), V("x")),
                   cap(he) + " should add 6, not subtract it",
                   [cap(he) + " should divide by 6 first", cap(he) + " should multiply by 3", "Nothing, 4 is right"],
                   "To undo − 6, use the inverse: <b>add 6</b>, not the same operation. 3%s = 18 + 6 = 24, so %s = 24 ÷ 3 = 8. "
                   "Check: 3 × 8 − 6 = 18. Check 4: 3 × 4 − 6 = 6, not 18." % (V("x"), V("x"))))
    nm, he, his, him = P.next()
    assert solve_text("x/3 + 5 = 9") == 12
    its.append(mcq("%s solves %s and gets %s = 22. What went wrong?" % (nm, render("x/3 + 5 = 9"), V("x")),
                   cap(he) + " multiplied by 3 before subtracting 5",
                   [cap(he) + " should divide 9 by 3", cap(he) + " should add 5 to both sides", "Nothing, 22 is right"],
                   "%s did 9 × 3 = 27, then 27 − 5 = 22. That multiplies first. Undo in reverse order: <b>subtract 5 first</b>: "
                   "%s = 4. Then multiply by 3: %s = 12. Check: 12 ÷ 3 + 5 = 9." % (nm, render("x/3"), V("x"))))
    assert len(its) == 20, len(its)
    return {"title": "Solve equations like x/4 + 2 = 7 and 2x − 5 = 11", "items": its}


# ============================================================ set 4: write an equation from words or a model
def set_write(P):
    its = []

    def match(q, right, wr, e, x=None):
        x = solve_text(right) if x is None else x
        assert holds(right, x), right
        for w in wr:
            assert not holds(w, x), (w, x)
        assert "</b>." in e, e
        e = e.replace("</b>.", "</b>. Then %s = %d." % (V(var_of(right)), x), 1)
        its.append(mcq(q, render(right), [render(w) for w in wr], e))

    W = "Which equation matches?"
    # words
    match("“Three times a number, plus 4, is 19.” " + W, "3n + 4 = 19", ["3 + 4n = 19", "3n - 4 = 19", "n + 3 + 4 = 19"],
          "Let %s be the number. Three times it is 3%s, plus 4 is + 4, and “is” means =: <b>%s</b>."
          % (V("n"), V("n"), render("3n + 4 = 19")))
    match("“Twice a number, minus 5, is 11.” " + W, "2n - 5 = 11", ["2n + 5 = 11", "5n - 2 = 11", "n/2 - 5 = 11"],
          "Twice a number is 2%s. Minus 5 is − 5: <b>%s</b>. %s would be half the number." % (V("n"), render("2n - 5 = 11"), render("n/2")))
    match("“A number divided by 4, plus 2, is 7.” " + W, "n/4 + 2 = 7", ["4n + 2 = 7", "n/2 + 4 = 7", "n/4 = 7 + 2"],
          "Divide the number by 4: %s. Then add 2: <b>%s</b>. %s multiplies instead of dividing."
          % (render("n/4"), render("n/4 + 2 = 7"), render("4n")))
    match("“Five more than six times a number is 47.” " + W, "6n + 5 = 47", ["5n + 6 = 47", "6n - 5 = 47", "6n = 47 + 5"],
          "Six times a number is 6%s. Five more than that is 6%s + 5: <b>%s</b>. Do not swap the 5 and the 6."
          % (V("n"), V("n"), render("6n + 5 = 47")))
    match("“A number divided by 3, minus 4, is 2.” " + W, "n/3 - 4 = 2", ["3n - 4 = 2", "n/3 + 4 = 2", "n/4 - 3 = 2"],
          "Divide by 3: %s. Then subtract 4: <b>%s</b>." % (render("n/3"), render("n/3 - 4 = 2")))
    match("“Eight less than four times a number is 28.” " + W, "4n - 8 = 28", ["8 - 4n = 28", "4n + 8 = 28", "8n - 4 = 28"],
          "Four times a number is 4%s. “Eight less than” it means take 8 away from it: <b>%s</b>. "
          "%s would take 4%s away from 8." % (V("n"), render("4n - 8 = 28"), render("8 - 4n"), V("n")))
    match("“Half of a number, minus 3, is 9.” " + W, "n/2 - 3 = 9", ["2n - 3 = 9", "n/2 + 3 = 9", "3 - n/2 = 9"],
          "Half of a number is the number divided by 2: %s. Minus 3 takes 3 away: <b>%s</b>. "
          "2%s would be double the number, not half." % (render("n/2"), render("n/2 - 3 = 9"), V("n")))
    # stories
    nm, he, his, him = P.next()
    match("A community centre in Burnaby charges a $20 sign-up fee plus $8 for each swim. %s pays $68 in all for "
          "%s swims. %s" % (nm, V("s"), W), "8s + 20 = 68", ["20s + 8 = 68", "8s - 20 = 68", "s + 8 + 20 = 68"],
          "$8 for each of %s swims is 8%s. Add the $20 fee: <b>%s</b>. The fee is paid once, so it is not multiplied by %s."
          % (V("s"), V("s"), render("8s + 20 = 68"), V("s")))
    nm, he, his, him = P.next()
    match("%s has $90. %s buys 4 concert tickets that cost %s dollars each and has $10 left. %s" % (nm, cap(he), V("t"), W),
          "90 - 4t = 10", ["4t - 90 = 10", "90 + 4t = 10", "4t - 10 = 90"],
          "Start with 90 and take away 4 tickets, 4%s: <b>%s</b>. The money left is 10." % (V("t"), render("90 - 4t = 10")))
    match("4 friends share the cost of a pizza, %s dollars, equally. Each friend also pays $3 for a drink. Each friend "
          "pays $9 in all. %s" % (V("c"), W), "c/4 + 3 = 9", ["4c + 3 = 9", "c/3 + 4 = 9", "c/4 - 3 = 9"],
          "Each share of the pizza is %s. Add the $3 drink: <b>%s</b>. Sharing equally means divide, not multiply."
          % (render("c/4"), render("c/4 + 3 = 9")))
    match("A BC Ferries boat has 15 cars on board. Then 6 lanes of %s cars each drive on. Now there are 75 cars. %s"
          % (V("c"), W), "6c + 15 = 75", ["15c + 6 = 75", "6c - 15 = 75", "c + 6 + 15 = 75"],
          "6 lanes of %s cars is 6%s. Add the 15 already on board: <b>%s</b>." % (V("c"), V("c"), render("6c + 15 = 75")))
    # models
    for k, b, c, wr in [(4, 6, 26, ["x + 4 + 6 = 26", "6x + 4 = 26", "4x = 26 + 6"]),
                        (2, 9, 25, ["x + 2 + 9 = 25", "9x + 2 = 25", "2x = 25 + 9"])]:
        right = eqs("m", k, "+", b, c)
        match("The pans balance. " + W + fig(bal(k, b, c)), right, wr,
              "%d blocks %s is %s. Add the %d: <b>%s</b>. Counting the blocks as %s + %d is a common mistake."
              % (k, V("x"), render("%dx" % k), b, render(right), V("x"), k))
    for k, b, c, wr in [(3, 7, 31, ["x + 3 + 7 = 31", "7x + 3 = 31", "3x - 7 = 31"]),
                        (5, 6, 46, ["x + 5 + 6 = 46", "6x + 5 = 46", "5x - 6 = 46"])]:
        right = eqs("m", k, "+", b, c)
        x = solve_text(right)
        match("The bar model shows %d equal parts %s and a part of %d. They make %d. %s" % (k, V("x"), b, c, W)
              + fig(tape_svg(k, b, c, x)), right, wr,
              "%d parts of %s is %s. Add the %d to make the whole, %d: <b>%s</b>."
              % (k, V("x"), render("%dx" % k), b, c, render(right)))
    match("A number %s goes into this machine. " % V("n") + W + fig(flow_svg("n", ["× 4", M + " 3"], "25")),
          "4n - 3 = 25", ["4n + 3 = 25", "3n - 4 = 25", "4 - 3n = 25"],
          "First multiply by 4: 4%s. Then subtract 3: 4%s − 3. The machine gives 25: <b>%s</b>."
          % (V("n"), V("n"), render("4n - 3 = 25")))
    match("A number %s goes into this machine. " % V("n") + W + fig(flow_svg("n", ["÷ 2", "+ 6"], "15")),
          "n/2 + 6 = 15", ["2n + 6 = 15", "n/6 + 2 = 15", "n/2 = 15 + 6"],
          "First divide by 2: %s. Then add 6. The machine gives 15: <b>%s</b>." % (render("n/2"), render("n/2 + 6 = 15")))
    # equation -> story
    assert solve_text("5x + 15 = 40") == 5
    its.append(mcq("Which story matches %s?" % render("5x + 15 = 40"),
                   "A kayak costs $15 to rent plus $5 per hour. The bill is $40.",
                   ["A kayak costs $5 to rent plus $15 per hour. The bill is $40.",
                    "A kayak costs $15 per hour. 5 people pay $40 in all.",
                    "A kayak costs $40 to rent. You get $15 off for 5 hours."],
                   "5%s is $5 for each of %s hours. + 15 is a one-time $15 fee. The total is $40: <b>$15 to rent plus $5 per hour</b>. "
                   "Then %s = 5 hours. $5 to rent plus $15 per hour would be %s." % (V("x"), V("x"), V("x"), render("15x + 5 = 40"))))
    assert solve_text("x/3 - 2 = 6") == 24
    its.append(mcq("Which story matches %s?" % render("x/3 - 2 = 6"),
                   "3 friends share %s cherries equally. Each eats 2 and has 6 left." % V("x"),
                   ["3 bags have %s cherries each. 2 are eaten and 6 are left." % V("x"),
                    "3 friends share %s cherries equally. Each gets 2 more and has 6." % V("x"),
                    "2 friends share %s cherries equally. Each eats 3 and has 6 left." % V("x")],
                   "%s is one friend’s equal share. − 2 means each eats 2. 6 are left: <b>3 friends share equally, each eats 2</b>. "
                   "Then %s = 24 cherries. 3 bags of %s each would be 3%s." % (render("x/3"), V("x"), V("x"), V("x"))))
    # mistake
    nm, he, his, him = P.next()
    match("“Seven times a number, minus 3, is 25.” %s writes %s. Which equation is right?" % (nm, render("3 - 7n = 25")),
          "7n - 3 = 25", ["3 - 7n = 25", "7n + 3 = 25", "3n - 7 = 25"],
          "Seven times a number is 7%s. Minus 3 takes 3 away from it: <b>%s</b>. %s takes 7%s away from 3."
          % (V("n"), render("7n - 3 = 25"), render("3 - 7n"), V("n")))
    assert len(its) == 20, len(its)
    return {"title": "Write an equation from words or a model", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def solve(q, s, cands, why, unit, form, a, op, b, c, v):
        x = solve_text(s)
        assert x == solve2(form, a, op, b, c), s
        e = "Equation: %s. %s %s" % (render(s), steps(form, a, op, b, c, v), why)
        its.append(mcq_n(q, x, cands if cands is not None else wrongs(form, a, op, b, c) + near(x), e.strip(), unit,
                         limit=max(c + b, 2 * x)))

    MO = ("month", "months")
    H = ("hour", "hours")
    # 1 phone plan
    nm, he, his, him = P.next()
    solve("%s’s phone plan costs $15 to start, plus $5 per month. So far %s has paid $50. How many months has %s had "
          "the plan?" % (nm, he, he), "5m + 15 = 50",
          [(35, "forgetting to divide by 5"), (13, "adding 15 instead of subtracting it"), (10, "dividing 50 by 5 and forgetting the $15")],
          "", MO, "m", 5, "+", 15, 50, "m")
    # 2 bike rental
    nm, he, his, him = P.next()
    solve("A bike rental near Stanley Park costs $6 per hour, plus an $8 fee for a helmet and lock. %s pays $38. "
          "How many hours did %s rent the bike for?" % (nm, he), "6h + 8 = 38", None, "", H, "m", 6, "+", 8, 38, "h")
    # 3 snowboard lessons
    nm, he, his, him = P.next()
    solve("At Grouse Mountain, %s pays $25 to rent a snowboard for the season, plus $15 for each lesson. "
          "%s spends $100. How many lessons does %s take?" % (nm, cap(he), he), "15n + 25 = 100",
          None, "", ("lesson", "lessons"), "m", 15, "+", 25, 100, "n")
    # 4 ferry
    solve("A family takes BC Ferries to Vancouver Island. They pay $64 for the car and 2 adult tickets that cost the "
          "same. The total is $100. How much is one adult ticket?", "2t + 64 = 100",
          None, "", "$", "m", 2, "+", 64, 100, "t")
    # 5 Terry Fox Run
    solve("A school has raised $120 for the Terry Fox Run. Each student who runs raises $5 more. The goal is $245. "
          "How many students need to run to reach the goal?", "5r + 120 = 245", None, "",
          ("student", "students"), "m", 5, "+", 120, 245, "r")
    # 6 savings
    nm, he, his, him = P.next()
    solve("%s has $35 and saves $12 each week for a new hockey stick. After how many weeks will %s have $119?"
          % (nm, he), "12w + 35 = 119", None, "", ("week", "weeks"), "m", 12, "+", 35, 119, "w")
    # 7 cabin
    solve("4 friends share the cost of a cabin in Whistler equally. Each friend also pays $10 for food. Each friend pays "
          "$85 in all. What is the cost of the cabin?", "c/4 + 10 = 85", None, "", "$", "d", 4, "+", 10, 85, "c")
    # 8 pizza
    solve("6 teammates split the bill for pizza after a lacrosse game equally. Each also pays $2 toward the tip. "
          "Each teammate pays $9. How much was the pizza bill?", "b/6 + 2 = 9", None, "", "$", "d", 6, "+", 2, 9, "b")
    # 9 kayak tour
    solve("A group of 6 books a kayak tour in Victoria. Each person pays the same price, and the group gets $12 off "
          "the total. They pay $138. What is the price for one person?", "6p - 12 = 138", None, "", "$",
          "m", 6, "-", 12, 138, "p")
    # 10 hockey tickets
    nm, he, his, him = P.next()
    solve("%s buys 3 hockey tickets that cost the same and uses a $10 gift card. %s pays $65. How much is one ticket?"
          % (nm, cap(he)), "3t - 10 = 65", None, "", "$", "m", 3, "-", 10, 65, "t")
    # 11 food bank cans
    solve("For the food bank, the Grade 7s collected 8 fewer cans than twice the number the Grade 6s collected. "
          "The Grade 7s collected 152 cans. How many cans did the Grade 6s collect?", "2g - 8 = 152", None, "",
          ("can", "cans"), "m", 2, "-", 8, 152, "g")
    # 12 age
    nm, he, his, him = P.next()
    solve("%s’s aunt is 4 years older than 3 times %s’s age. %s aunt is 40. How old is %s?"
          % (nm, nm, cap(his), nm), "3a + 4 = 40", None, "", ("year old", "years old"), "m", 3, "+", 4, 40, "a")
    # 13 hike
    nm, he, his, him = P.next()
    solve("On a hike near Squamish, %s walks 3 km to the trailhead, then hikes 2 km each hour. %s walks 13 km in all. "
          "How many hours does %s hike on the trail?" % (nm, cap(he), he), "2h + 3 = 13", None, "", H,
          "m", 2, "+", 3, 13, "h")
    # 14 ribbon
    nm, he, his, him = P.next()
    solve("%s cuts a ribbon into 3 equal pieces. Then %s cuts 15 cm off one piece. That piece is now 45 cm long. "
          "How long was the ribbon?" % (nm, he), "r/3 - 15 = 45", None, "", ("cm", "cm"), "d", 3, "-", 15, 45, "r")
    # 15 T-shirts
    solve("A school packs its Sports Day T-shirts equally into 8 boxes. One box gets 4 extra shirts, and then it holds "
          "19 shirts. How many T-shirts were packed at the start?", "s/8 + 4 = 19", None, "", ("shirt", "shirts"),
          "d", 8, "+", 4, 19, "s")
    # 16 pool
    nm, he, his, him = P.next()
    solve("A pool in Surrey charges $30 for a membership card, plus $4 for each swim. %s spends $78. "
          "How many times does %s swim?" % (nm, he), "4s + 30 = 78", None, "", ("time", "times"), "m", 4, "+", 30, 78, "s")
    # 17 music lessons
    nm, he, his, him = P.next()
    solve("A music school in Kelowna charges $45 to sign up, plus $20 for each guitar lesson. %s pays $185 in all. "
          "How many lessons does %s take?" % (nm, he), "20n + 45 = 185", None, "", ("lesson", "lessons"),
          "m", 20, "+", 45, 185, "n")
    # 18 lacrosse sticks
    solve("A lacrosse club buys 12 sticks that cost the same and gets $30 off the total. It pays $510. "
          "How much does one stick cost?", "12s - 30 = 510", None, "", "$", "m", 12, "-", 30, 510, "s")
    # 19 canoe
    nm, he, his, him = P.next()
    solve("%s rents a canoe on a lake in the Okanagan. It costs $12 per hour, plus $20 for life jackets. The bill is $80. "
          "For how many hours does %s rent the canoe?" % (nm, he), "12h + 20 = 80", None, "", H, "m", 12, "+", 20, 80, "h")
    # 20 granola bars
    solve("A Grade 7 class buys packs of granola bars for a field trip. Each pack costs $6. With a $15 coupon, the class "
          "pays $75. How many packs does it buy?", "6p - 15 = 75", None, "", ("pack", "packs"), "m", 6, "-", 15, 75, "p")
    assert len(its) == 20, len(its)
    return {"title": "Two-step equation word problems", "items": its}


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
        "<h2>What is a two-step equation?</h2>"
        "<p>A <b>two-step equation</b> does two things to the unknown. In " + render("3x + 4 = 19") + ", "
        "you multiply " + x + " by 3, then add 4. To find " + x + ", <b>undo the steps in reverse order</b>: "
        "undo the + 4 first, then undo the × 3.</p>"
        "<figure class='sn-fig'>" + flow_svg("x", ["× 3", "+ 4"], "19", undo=True) +
        "<figcaption>Top: build 3" + x + " + 4. Bottom: work back from 19. 19 − 4 = 15, then 15 ÷ 3 = 5.</figcaption></figure>"
        "<h2>Keep the balance level</h2>"
        "<p>An equation is like a level pan balance. Whatever you do to one side, do to the other side too.</p>"
        "<figure class='sn-fig'>" + bal(3, 4, 19) +
        "<figcaption>Take 4 off both pans: 3" + x + " = 15. Each block is 15 ÷ 3 = 5.</figcaption></figure>" +
        table(["Equation", "Step 1", "Step 2", "Answer"], [
            [render("3x + 4 = 19"), "− 4 on both sides: 3" + x + " = 15", "÷ 3", x + " = 5"],
            [render("2x - 5 = 11"), "+ 5 on both sides: 2" + x + " = 16", "÷ 2", x + " = 8"],
            [render("x/4 + 2 = 7"), "− 2 on both sides: " + render("x/4") + " = 5", "× 4", x + " = 20"],
        ]) +
        ex("Example", "Solve " + render("x/4 + 2 = 7") + ".",
           "Undo + 2 first: " + render("x/4") + " = 7 − 2 = 5. Then undo ÷ 4 by multiplying: " + x + " = 5 × 4 = 20. "
           "Check: 20 ÷ 4 + 2 = 7.", x + " = 20") +
        ex("Example", "Solve " + render("2x - 5 = 11") + ".",
           "Undo − 5 by adding 5: 2" + x + " = 16. Then divide by 2: " + x + " = 8. Check: 2 × 8 − 5 = 11.", x + " = 8") +
        "<h2>Write an equation from words</h2>"
        "<p>Let a letter stand for the unknown. “Times” or “per” is ×, “divided” or “shared equally” is ÷, "
        "a one-time fee is + and “off” or “less” is −.</p>"
        "<figure class='sn-fig'>" + tape_svg(5, 15, 50, 7, "m") +
        "<figcaption>$15 to start plus $5 per month, $50 in all: 5" + V("m") + " + 15 = 50.</figcaption></figure>" +
        ex("Example", "A phone plan costs $15 to start, plus $5 per month. Liam has paid $50. How many months?",
           "Equation: 5" + V("m") + " + 15 = 50. Subtract 15: 5" + V("m") + " = 35. Divide by 5: " + V("m") + " = 7. "
           "Check: 5 × 7 + 15 = 50.", "7 months") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            [render("3x + 4 = 19") + ": 19 ÷ 3 first", "Subtract 4 first, then divide: " + x + " = 5"],
            [render("2x - 5 = 11") + ": 11 − 5 = 6", "Use the inverse: add 5, so 2" + x + " = 16"],
            [render("x/4 + 2 = 7") + ": 5 ÷ 4", "÷ 4 is undone by × 4: " + x + " = 20"],
            [render("3x + 4 = 19") + ": stop at 15", "15 is 3" + x + ". Divide by 3 too: " + x + " = 5"],
            ["3 blocks " + x + " written as " + render("x + 3"), "3 blocks " + x + " is 3" + x + " (3 × " + x + ")"],
            ["Not checking", "Put the answer back in: 3 × 5 + 4 = 19"],
        ])
    )


FAQ = [
    {"q": "How do you solve two-step equations in Grade 7?",
     "a": "Undo the operations in reverse order. For 3x + 4 = 19, subtract 4 from both sides (3x = 15), then divide both sides by 3 (x = 5), and check: 3 × 5 + 4 = 19."},
    {"q": "Are two-step equations in the BC Grade 7 math curriculum?",
     "a": "Yes. The BC Grade 7 Patterning standard covers two-step equations with whole-number coefficients, constants and solutions, like 2x − 5 = 11 and x/4 + 2 = 7."},
    {"q": "Why do you subtract before you divide in 3x + 4 = 19?",
     "a": "3x + 4 means multiply by 3, then add 4, so you undo the + 4 first. Dividing first would leave the 4 undivided and give a wrong answer."},
    {"q": "Are equations on the Grade 7 FSA?",
     "a": "The Grade 7 FSA numeracy section checks math skills and problem solving from the BC curriculum. Writing and solving equations for word problems, like the ones here, is good practice for it."},
]


def gen_unit():
    rnd = random.Random(37808)
    P = People(rnd)
    sets = [set_balance(P), set_plus(P), set_minus_div(P), set_write(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len({plain(c) for c in it["c"]}) == 4, it
            assert it["q"].count("<svg") <= 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-7", "slug": "two-step-equations", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 7 Two-Step Equations",
        "seo_title": "Grade 7 Two-Step Equations Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "Two-Step Equations",
        "domain": "Patterning",
        "standard_code": "Grade 7: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/7/core",
        "standard_text": "Two-step equations with whole-number coefficients, constants, and solutions",
        "meta_desc": "Free Grade 7 math worksheets on two-step equations for the BC curriculum: pan balances, solving 3x + 4 = 19, x/4 + 2 = 7 and 2x − 5 = 11, writing equations from words and models, and word problems. 100 questions with an answer key, good FSA practice.",
        "key_big": "Undo the steps in reverse order: undo the + or − first, then undo the × or ÷.",
        "key_sub": "3x + 4 = 19: subtract 4 (3x = 15), then divide by 3 (x = 5). Do the same to both sides, and check your answer.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "bar model|pan balance|number machine")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
